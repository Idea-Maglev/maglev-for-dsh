"""
index_gen.py — Shared INDEX.md generation utilities for dir-tree type.

Provides directory discovery, child counting, and INDEX.md creation/update
functions used by track_scan for dir-tree generation.

Design authority: specs/20_evolution/active/unified_doc_tree_indexer/02_design.md
"""

from __future__ import annotations

import os
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

from .frontmatter import parse_file, parse_any_frontmatter, write_frontmatter
from .ignore import IndexIgnorePolicy, should_skip_entry
from .knowledge import (
    build_directory_records,
    collapsed_leaf_file,
    replace_navigation_block,
)




def is_index_or_readme(name: str) -> bool:
    """Exclude protocol files even on case-insensitive filesystems."""
    return name.casefold() in {"index.md", "readme.md"}


# ─── Directory Discovery ─────────────────────────────────────────────

def discover_indexable_dirs(
    root_dir: Path,
    ignore: set[str] | IndexIgnorePolicy,
    max_depth: int,
    skip_index_dirs: set[str] | None = None,
    collapse_single_file_dirs: set[str] | None = None,
) -> list[Path]:
    """Recursively find all directories that should get an INDEX.md.

    Returns list sorted deepest-first (bottom-up) for safe processing.
    ``skip_index_dirs`` contains paths relative to ``root_dir`` whose own
    INDEX.md is omitted. Their descendants remain eligible for discovery.
    """
    results: list[Path] = []
    skipped = {path.rstrip("/") or "." for path in (skip_index_dirs or set())}

    def _walk(current: Path, depth: int) -> None:
        relative = "." if current == root_dir else current.relative_to(root_dir).as_posix()
        if current != root_dir and collapsed_leaf_file(
            current, root_dir, ignore, collapse_single_file_dirs
        ) is not None:
            return
        if relative not in skipped:
            results.append(current)
        if depth >= max_depth:
            return
        for child in sorted(current.iterdir()):
            if not child.is_dir():
                continue
            if should_skip_entry(child, ignore):
                continue
            _walk(child, depth + 1)

    if root_dir.is_dir():
        _walk(root_dir, 0)

    # Return bottom-up (deepest dirs first) so children are processed before parents
    results.reverse()
    return results


def find_collapsed_leaf_dirs(
    root_dir: Path,
    ignore: set[str] | IndexIgnorePolicy,
    max_depth: int,
    collapse_single_file_dirs: set[str] | None,
) -> list[Path]:
    """Find configured leaf directories whose generated INDEX.md can be removed."""
    collapsed: list[Path] = []

    def _walk(current: Path, depth: int) -> None:
        if current != root_dir and collapsed_leaf_file(
            current, root_dir, ignore, collapse_single_file_dirs
        ) is not None:
            collapsed.append(current)
            return
        if depth >= max_depth:
            return
        for child in sorted(current.iterdir()):
            if child.is_dir() and not should_skip_entry(child, ignore):
                _walk(child, depth + 1)

    if root_dir.is_dir():
        _walk(root_dir, 0)
    return collapsed


# ─── Child Type Detection ─────────────────────────────────────────────

def detect_child_type(directory: Path, ignore: set[str] | IndexIgnorePolicy) -> str:
    """Auto-detect child type: 'file', 'directory', or 'mixed'."""
    has_dirs = False
    has_files = False
    for child in directory.iterdir():
        if should_skip_entry(child, ignore):
            continue
        if is_index_or_readme(child.name):
            continue
        if child.is_dir():
            has_dirs = True
        elif child.is_file():
            has_files = True
        if has_dirs and has_files:
            return "mixed"
    if has_dirs and not has_files:
        return "directory"
    if has_files and not has_dirs:
        return "file"
    return "mixed" if (has_dirs or has_files) else "directory"


# ─── Counting ─────────────────────────────────────────────────────────

def count_children(directory: Path, child_type: str, ignore: set[str] | IndexIgnorePolicy) -> int:
    """Count direct children based on child_type."""
    count = 0
    for child in directory.iterdir():
        if should_skip_entry(child, ignore):
            continue
        if is_index_or_readme(child.name):
            continue
        if child_type == "file" and child.is_file():
            count += 1
        elif child_type == "directory" and child.is_dir():
            count += 1
        elif child_type == "mixed":
            if child.is_file() or child.is_dir():
                count += 1
    return count


def recursive_leaf_count(directory: Path, ignore: set[str] | IndexIgnorePolicy) -> int:
    """Recursively count all leaf files (non-INDEX, non-README, non-dotfile)."""
    total = 0
    for root, dirs, files in os.walk(directory):
        # Filter dirs in-place
        root_path = Path(root)
        dirs[:] = [d for d in sorted(dirs) if not should_skip_entry(root_path / d, ignore)]
        for f in files:
            file_path = root_path / f
            if should_skip_entry(file_path, ignore) or is_index_or_readme(f):
                continue
            total += 1
    return total


# ─── INDEX.md Generation / Update ────────────────────────────────────

def generate_or_update_index(
    dir_path: Path,
    root_dir: Path,
    entity_type: str,
    child_type_cfg: str,
    ignore: set[str] | IndexIgnorePolicy,
    repository_root: Path | None = None,
    collapse_single_file_dirs: set[str] | None = None,
) -> bool:
    """Generate new or update existing INDEX.md for a directory.

    Returns True if file was written/modified, False if skipped.
    """
    index_path = dir_path / "INDEX.md"

    # Resolve effective child_type
    if child_type_cfg == "auto":
        effective_child_type = detect_child_type(dir_path, ignore)
    else:
        effective_child_type = child_type_cfg

    child_count = count_children(dir_path, effective_child_type, ignore)
    total = recursive_leaf_count(dir_path, ignore)
    knowledge_records = build_directory_records(
        dir_path,
        root_dir,
        ignore,
        repository_root,
        collapse_single_file_dirs,
    )
    today = date.today().isoformat()

    if index_path.exists():
        # INDEX.md is script-owned: refresh its body so deleted children cannot
        # survive as stale links after a structure migration.
        result = parse_any_frontmatter(index_path)
        meta = result.metadata

        if not meta:
            # File exists but no frontmatter — add minimal frontmatter, preserve body
            scope = "root" if dir_path == root_dir else "collection"
            meta = {
                "type": "entity-index",
                "scope": scope,
                "entity_type": entity_type,
                "child_count": child_count,
                "child_type": effective_child_type,
                "stats": {"total": total},
                "updated": today,
                "knowledge_schema_version": 1,
                "knowledge_records": knowledge_records,
            }
            # Preserve original body content
            body = replace_navigation_block(result.content or "", knowledge_records)
            write_frontmatter(index_path, meta, body)
            return True

        candidate_meta = deepcopy(meta)
        candidate_meta["child_count"] = child_count
        if "stats" not in candidate_meta or not isinstance(candidate_meta["stats"], dict):
            candidate_meta["stats"] = {}
        candidate_meta["stats"]["total"] = total
        candidate_meta["knowledge_schema_version"] = 1
        candidate_meta["knowledge_records"] = knowledge_records

        # Preserve authored prose while refreshing both generated index views.
        body = _replace_generated_listing(result.content, dir_path, ignore, effective_child_type)
        candidate_body = replace_navigation_block(body, knowledge_records)
        if (
            "updated" in meta
            and _metadata_without_updated(meta) == _metadata_without_updated(candidate_meta)
            and result.content == candidate_body
        ):
            return False

        candidate_meta["updated"] = today
        write_frontmatter(index_path, candidate_meta, candidate_body)
        return True
    else:
        # CREATE mode: minimal frontmatter + default body
        scope = "root" if dir_path == root_dir else "collection"
        meta: dict[str, Any] = {
            "type": "entity-index",
            "scope": scope,
            "entity_type": entity_type,
            "child_count": child_count,
            "child_type": effective_child_type,
            "stats": {"total": total},
            "updated": today,
            "knowledge_schema_version": 1,
            "knowledge_records": knowledge_records,
        }

        body = replace_navigation_block(
            _generate_default_body(dir_path, ignore, effective_child_type), knowledge_records
        )
        write_frontmatter(index_path, meta, body)
        return True


def _generate_default_body(
    directory: Path,
    ignore: set[str] | IndexIgnorePolicy,
    child_type: str,
) -> str:
    """Generate a simple default body listing children as links."""
    lines: list[str] = []
    lines.append(f"# {directory.name}")

    children: list[tuple[str, bool]] = []  # (name, is_dir)
    for child in sorted(directory.iterdir()):
        if should_skip_entry(child, ignore):
            continue
        if is_index_or_readme(child.name):
            continue
        if child.is_dir():
            children.append((child.name, True))
        elif child.is_file() and child_type in ("file", "mixed"):
            children.append((child.name, False))

    if children:
        lines.append("")
        lines.append("| 名称 | 类型 |")
        lines.append("|:---|:---|")
        for name, is_dir in children:
            if is_dir:
                lines.append(f"| [{name}](./{name}/) | 📁 |")
            else:
                lines.append(f"| [{name}](./{name}) | 📄 |")
    else:
        lines.append("")
        lines.append("（空目录）")

    return "\n".join(lines) + "\n"


def _metadata_without_updated(metadata: dict[str, Any]) -> dict[str, Any]:
    comparable = deepcopy(metadata)
    comparable.pop("updated", None)
    return comparable


def _replace_generated_listing(
    content: str,
    directory: Path,
    ignore: set[str] | IndexIgnorePolicy,
    child_type: str,
) -> str:
    """Refresh only the generator's default pre-navigation listing.

    Generated INDEX files place the default title/table immediately before the
    navigation block. Use deterministic splitting instead of a permissive regex
    so large generated tables cannot trigger catastrophic backtracking.
    """
    listing = _generate_default_body(directory, ignore, child_type).strip()
    marker = "<!-- index-librarian:knowledge-start -->"
    if marker not in content:
        return content

    prefix, suffix = content.split(marker, 1)
    prefix_lines = [line.strip() for line in prefix.splitlines() if line.strip()]
    has_generated_title = (
        bool(prefix_lines)
        and prefix_lines[0].casefold() == f"# {directory.name}".casefold()
    )
    has_generated_listing = (
        any(line == "| 名称 | 类型 |" for line in prefix_lines)
        or any(line == "（空目录）" for line in prefix_lines)
    )
    has_only_generated_table = all(
        line.startswith("# ")
        or line.startswith("|")
        or line == "（空目录）"
        for line in prefix_lines
    )
    if has_generated_title and (has_generated_listing or len(prefix_lines) == 1) and has_only_generated_table:
        return f"{listing}\n{marker}{suffix}".strip()
    return content


# ─── Summary YAML ────────────────────────────────────────────────────

def build_summary(
    track: dict[str, Any],
    root_dir: Path,
    repo_root: Path,
    dirs: list[Path],
) -> dict[str, Any]:
    """Build summary YAML data for the track output file."""
    items: list[dict[str, Any]] = []
    for d in dirs:
        rel = d.relative_to(repo_root).as_posix()
        index_exists = (d / "INDEX.md").exists()
        items.append({
            "path": rel,
            "has_index": index_exists,
        })

    return {
        "track_id": track["id"],
        "track_type": track["type"],
        "root": track["root"],
        "dir_count": len(dirs),
        "items": items,
    }
