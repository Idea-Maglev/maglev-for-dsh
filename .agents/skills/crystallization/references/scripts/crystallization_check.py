#!/usr/bin/env python3
"""crystallization_check.py — 结晶产物自检脚本

用法:
    maglev-python crystallization_check.py <reality_dir> [--json]

退出码:
    0  无 FAIL
    1  存在 FAIL
    2  参数/路径错误

基于通用结构信号自适配检查，不硬编码特定目录名。
检查项以注册式组织，可扩展。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"

Result = Tuple[str, str, str]  # (level, check_name, detail)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _collect_md_files(root: Path) -> List[Path]:
    """Recursively collect all .md files under root."""
    return sorted(root.rglob("*.md"))


def _non_blank_line_count(path: Path) -> int:
    """Count non-blank lines in a file."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0
    return sum(1 for line in text.splitlines() if line.strip())


def _is_inside_code_fence(lines: List[str], target_idx: int) -> bool:
    """Check if a line index is inside a fenced code block."""
    inside = False
    for i, line in enumerate(lines):
        if i == target_idx:
            return inside
        if line.strip().startswith("```"):
            inside = not inside
    return inside


# ---------------------------------------------------------------------------
# Universal checks (always run)
# ---------------------------------------------------------------------------

def check_placeholder_free(root: Path) -> List[Result]:
    """Check for placeholder text outside code fences."""
    results: List[Result] = []
    pattern = re.compile(r"\b(TODO|TBD|FIXME)\b|待补充|^\.{3}$")
    for md in _collect_md_files(root):
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        found = False
        for i, line in enumerate(lines):
            if pattern.search(line) and not _is_inside_code_fence(lines, i):
                results.append((FAIL, "placeholder_free",
                                f"{md.relative_to(root)}:{i+1}"))
                found = True
        if not found:
            results.append((PASS, "placeholder_free",
                            str(md.relative_to(root))))
    return results


def check_mermaid_fence_balanced(root: Path) -> List[Result]:
    """Check that ```mermaid fences are properly closed."""
    results: List[Result] = []
    for md in _collect_md_files(root):
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        open_line = None
        has_mermaid = False
        fence_depth = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("```mermaid"):
                has_mermaid = True
                if fence_depth == 0:
                    open_line = i + 1
                fence_depth += 1
            elif stripped == "```" and fence_depth > 0:
                fence_depth -= 1
                open_line = None
        rel = str(md.relative_to(root))
        if fence_depth > 0:
            results.append((FAIL, "mermaid_fence_balanced",
                            f"{rel}:{open_line} (unclosed fence)"))
        elif has_mermaid:
            results.append((PASS, "mermaid_fence_balanced", rel))
    return results


def check_internal_links_reachable(root: Path) -> List[Result]:
    """Check that relative markdown links point to existing files."""
    results: List[Result] = []
    link_pattern = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    for md in _collect_md_files(root):
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        rel_path = md.relative_to(root)
        all_ok = True
        for match in link_pattern.finditer(text):
            target = match.group(2)
            # Skip external links, anchors, and absolute paths
            if target.startswith(("http://", "https://", "#", "/")):
                continue
            # Strip anchor
            target_path = target.split("#")[0]
            if not target_path:
                continue
            resolved = (md.parent / target_path).resolve()
            if not resolved.exists():
                results.append((FAIL, "internal_links_reachable",
                                f"{rel_path} -> {target_path} (not found)"))
                all_ok = False
        if all_ok and link_pattern.search(text):
            results.append((PASS, "internal_links_reachable", str(rel_path)))
    return results


def check_min_density(root: Path) -> List[Result]:
    """Warn about .md files with fewer than 5 non-blank lines."""
    results: List[Result] = []
    for md in _collect_md_files(root):
        count = _non_blank_line_count(md)
        rel = str(md.relative_to(root))
        if count < 5:
            results.append((WARN, "min_density",
                            f"{rel} ({count} lines)"))
        else:
            results.append((PASS, "min_density", rel))
    return results


# ---------------------------------------------------------------------------
# Structural-signal checks (conditionally triggered)
# ---------------------------------------------------------------------------

def _detect_module_dirs(root: Path) -> List[Path]:
    """Detect multi-module structure: ≥2 sibling subdirs each containing README.md."""
    # Check each directory level for sibling dirs with README
    candidates: List[Path] = []
    for dirpath in sorted(set(p.parent for p in root.rglob("README.md"))):
        if dirpath == root:
            continue
        # Check siblings at the same level
        parent = dirpath.parent
        sibling_readmes = [
            d for d in parent.iterdir()
            if d.is_dir() and (d / "README.md").exists() and d != root
        ]
        if len(sibling_readmes) >= 2:
            candidates.extend(sibling_readmes)
    return sorted(set(candidates))


def check_module_readme_nonempty(root: Path) -> List[Result]:
    """When multi-module structure detected, check each module README is non-empty."""
    module_dirs = _detect_module_dirs(root)
    if not module_dirs:
        return []
    results: List[Result] = []
    for d in module_dirs:
        readme = d / "README.md"
        rel = str(readme.relative_to(root))
        if _non_blank_line_count(readme) < 3:
            results.append((FAIL, "module_readme_nonempty",
                            f"{rel} (empty or near-empty)"))
        else:
            results.append((PASS, "module_readme_nonempty", rel))
    return results


def check_cross_module_rtag_reachable(root: Path) -> List[Result]:
    """When multi-module structure detected, check R-tag cross-references resolve."""
    module_dirs = _detect_module_dirs(root)
    if not module_dirs:
        return []

    # Collect all R-tags defined across all files
    rtag_pattern = re.compile(r"`(R-[A-Z0-9]+-[A-Z0-9]+-\d+)`")
    defined_tags: set = set()
    referenced_tags: dict = {}  # tag -> list of (file, line)

    for md in _collect_md_files(root):
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for i, line in enumerate(lines):
            for m in rtag_pattern.finditer(line):
                tag = m.group(1)
                # A tag in a heading = definition
                if line.strip().startswith("#"):
                    defined_tags.add(tag)
                else:
                    referenced_tags.setdefault(tag, []).append(
                        (md.relative_to(root), i + 1))

    results: List[Result] = []
    for tag, refs in referenced_tags.items():
        if tag not in defined_tags:
            for ref_file, ref_line in refs:
                results.append((FAIL, "cross_module_rtag_reachable",
                                f"{ref_file}:{ref_line} references {tag} (not defined)"))
        else:
            results.append((PASS, "cross_module_rtag_reachable", tag))
    return results


def check_rtag_format_valid(root: Path) -> List[Result]:
    """When R-tag text detected, validate format."""
    results: List[Result] = []
    # Broader pattern to catch malformed tags
    broad_pattern = re.compile(r"`(R-[^\s`]+)`")
    strict_pattern = re.compile(r"^R-[A-Z0-9]+-[A-Z0-9]+-\d+$")

    found_any = False
    for md in _collect_md_files(root):
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        rel = str(md.relative_to(root))
        for i, line in enumerate(lines):
            for m in broad_pattern.finditer(line):
                found_any = True
                tag = m.group(1)
                if strict_pattern.match(tag):
                    results.append((PASS, "rtag_format_valid",
                                    f"{rel}:{i+1} {tag}"))
                else:
                    results.append((FAIL, "rtag_format_valid",
                                    f"{rel}:{i+1} {tag} (invalid format)"))
    return results if found_any else []


def check_arch_doc_nonempty(root: Path) -> List[Result]:
    """When architecture.md or overview.md found in subdirs, check non-empty."""
    results: List[Result] = []
    arch_names = {"architecture.md", "overview.md"}
    for md in _collect_md_files(root):
        if md.name in arch_names and md.parent != root:
            rel = str(md.relative_to(root))
            if _non_blank_line_count(md) < 3:
                results.append((FAIL, "arch_doc_nonempty",
                                f"{rel} (empty or near-empty)"))
            else:
                results.append((PASS, "arch_doc_nonempty", rel))
    return results


# ---------------------------------------------------------------------------
# Versioned Reality Profile checks (only when 00_profile.yaml exists)
# ---------------------------------------------------------------------------

def _profile_path(root: Path) -> Path:
    return root / "00_profile.yaml"


def _load_profile(root: Path) -> tuple[dict | None, List[Result]]:
    path = _profile_path(root)
    if not path.exists():
        return None, []  # Legacy Reality remains supported until migration completes.
    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return None, [(FAIL, "profile_parseable", str(error))]
    if profile.get("profile_id") != "maglev-core-v1" or profile.get("layout_version") != 1:
        return None, [(FAIL, "profile_parseable", "unsupported profile_id or layout_version")]
    return profile, [(PASS, "profile_parseable", "maglev-core-v1")]


def _required_profile_paths(profile: dict) -> set[str]:
    paths = set(profile.get("root_entries", []))
    for domain in profile.get("domains", []):
        for entry in profile.get("domain_entry_files", []):
            paths.add(f"{domain}/{entry}")
    for entry in profile.get("crosscutting_entry_files", []):
        paths.add(f"crosscutting/{entry}")
    return paths


def _metadata_value(path: Path, field: str) -> str | None:
    try:
        match = re.search(rf"^{re.escape(field)}:\s*(.+?)\s*$", path.read_text(encoding="utf-8"), re.MULTILINE)
    except (OSError, UnicodeDecodeError):
        return None
    return match.group(1).strip() if match else None


def _has_evidence(path: Path) -> bool:
    value = _metadata_value(path, "evidence_refs")
    return value not in (None, "", "[]")


def check_profile_gate(root: Path) -> List[Result]:
    """Validate the fixed Maglev Reality schema without affecting legacy roots."""
    profile, results = _load_profile(root)
    if profile is None:
        return results

    required_paths = _required_profile_paths(profile)
    missing = sorted(path for path in required_paths if not (root / path).exists())
    if missing:
        results.extend((FAIL, "profile_required_paths", path) for path in missing)
    else:
        results.append((PASS, "profile_required_paths", f"{len(required_paths)} paths"))

    allowed_statuses = set(profile.get("knowledge_statuses", []))
    for rel_path in sorted(required_paths):
        is_domain_slot = any(rel_path.startswith(f"{domain}/") and rel_path.endswith("/INDEX.md") for domain in profile.get("domains", []))
        is_crosscutting_slot = rel_path.startswith("crosscutting/") and rel_path.endswith("/INDEX.md")
        if not (is_domain_slot or is_crosscutting_slot):
            continue
        path = root / rel_path
        if not path.exists():
            continue
        status = _metadata_value(path, "knowledge_status")
        if status not in allowed_statuses:
            results.append((FAIL, "knowledge_status_valid", rel_path))
        elif status == "not_applicable" and not _has_evidence(path):
            results.append((FAIL, "not_applicable_evidenced", rel_path))

    registry = profile.get("document_registry", {})
    required_fields = set(registry.get("required_fields", []))
    domains = set(profile.get("domains", []))
    domain_slots = set(registry.get("owner_slots", []))
    crosscutting_slots = set(registry.get("crosscutting_slots", []))
    registered_paths = set()
    for document in profile.get("documents", []):
        registered_paths.add(document.get("path", ""))
        missing_fields = required_fields - set(document)
        owner_domain = document.get("owner_domain")
        owner_slot = document.get("owner_slot")
        is_domain_document = owner_domain in domains and owner_slot in domain_slots
        is_crosscutting_document = owner_domain == "crosscutting" and owner_slot in crosscutting_slots
        if missing_fields or not (is_domain_document or is_crosscutting_document):
            results.append((FAIL, "profile_document_registry", document.get("path", "invalid document entry")))
            continue
        rel_path = document["path"]
        expected_prefix = f"{owner_domain}/{owner_slot}/"
        if not rel_path.startswith(expected_prefix) or not (root / rel_path).is_file():
            results.append((FAIL, "profile_document_registry", rel_path))
        status = document.get("knowledge_status")
        if status not in allowed_statuses:
            results.append((FAIL, "knowledge_status_valid", rel_path))
        elif status == "not_applicable" and not document.get("evidence_refs"):
            results.append((FAIL, "not_applicable_evidenced", rel_path))

    state_registry = profile.get("state_file_registry", {})
    state_required_fields = set(state_registry.get("required_fields", []))
    state_slots = set(state_registry.get("owner_slots", []))
    for state_file in profile.get("state_files", []):
        rel_path = state_file.get("path", "")
        missing_fields = state_required_fields - set(state_file)
        expected_prefix = f"{state_file.get('owner_domain', '')}/{state_file.get('owner_slot', '')}/"
        if (
            missing_fields
            or state_file.get("owner_domain") not in domains
            or state_file.get("owner_slot") not in state_slots
            or not rel_path.startswith(expected_prefix)
            or not (root / rel_path).is_file()
        ):
            results.append((FAIL, "profile_state_file_registry", rel_path or "invalid state file entry"))

    legacy_paths = set(profile.get("migration", {}).get("legacy_paths", []))
    for markdown in _collect_md_files(root):
        rel_path = str(markdown.relative_to(root))
        if rel_path in required_paths or rel_path in registered_paths:
            continue
        if any(rel_path == legacy.rstrip("/") or rel_path.startswith(legacy.rstrip("/") + "/") for legacy in legacy_paths):
            continue
        results.append((FAIL, "profile_document_registry", rel_path))
    return results


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

UNIVERSAL_CHECKS = [
    check_placeholder_free,
    check_mermaid_fence_balanced,
    check_internal_links_reachable,
    check_min_density,
]

STRUCTURAL_CHECKS = [
    check_module_readme_nonempty,
    check_cross_module_rtag_reachable,
    check_rtag_format_valid,
    check_arch_doc_nonempty,
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_checks(root: Path) -> List[Result]:
    """Run all applicable checks and return results."""
    results: List[Result] = []
    results.extend(check_profile_gate(root))
    for check_fn in UNIVERSAL_CHECKS:
        results.extend(check_fn(root))
    for check_fn in STRUCTURAL_CHECKS:
        results.extend(check_fn(root))
    return results


def _count_modules(root: Path) -> int:
    """Count detected module directories."""
    return len(_detect_module_dirs(root))


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def format_text(results: List[Result], modules_detected: int) -> str:
    """Format results as human-readable text."""
    lines: List[str] = []
    for level, name, detail in results:
        lines.append(f"[{level}] {name}   {detail}")
    lines.append("---")
    counts = {PASS: 0, WARN: 0, FAIL: 0}
    for level, _, _ in results:
        counts[level] = counts.get(level, 0) + 1
    lines.append(
        f"summary: pass={counts[PASS]} warn={counts[WARN]} "
        f"fail={counts[FAIL]} modules_detected={modules_detected}"
    )
    return "\n".join(lines)


def format_json(results: List[Result], modules_detected: int) -> str:
    """Format results as JSON."""
    output = {
        "results": [
            {"level": level, "check": name, "detail": detail}
            for level, name, detail in results
        ],
        "summary": {
            "pass": sum(1 for r in results if r[0] == PASS),
            "warn": sum(1 for r in results if r[0] == WARN),
            "fail": sum(1 for r in results if r[0] == FAIL),
            "modules_detected": modules_detected,
        },
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Crystallization self-check: validate reality directory structure and content."
    )
    parser.add_argument("reality_dir", help="Path to the reality directory to check")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    root = Path(args.reality_dir)
    if not root.is_dir():
        print(f"Error: '{args.reality_dir}' is not a directory", file=sys.stderr)
        return 2

    results = run_checks(root)
    modules_detected = _count_modules(root)

    if args.json:
        print(format_json(results, modules_detected))
    else:
        print(format_text(results, modules_detected))

    has_fail = any(r[0] == FAIL for r in results)
    return 1 if has_fail else 0


if __name__ == "__main__":
    sys.exit(main())
