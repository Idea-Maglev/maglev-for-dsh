"""
_code_tree_helpers.py — Shared anchor-walk + radar-summary infrastructure.

Constants inherited from the now-removed maglev-librarian/scripts/smart_map.py
(D25 evidence; see git history before commit removing maglev-librarian for the
original source):
  DEFAULT_IGNORE_DIRS / DEFAULT_ANCHOR_FILES / DEFAULT_MAX_DEPTH / DEFAULT_MAX_LINES

Functions:
  walk_with_anchors(root, ignore_dirs, anchor_files, max_depth, max_lines)
    → list of {path, depth, name, anchors, summary}
    Used by both _scan_code_tree (track_scan.py) and _map_repo_entry (track_map.py).

  invoke_radar_summary(root, hotspot_top, include_unused, include_cycles_count,
                       max_output_lines, timeout)
    → dict {hotspot, unused_count?, cycles_count?, _truncated?} on success
    → dict {skipped: True, reason: <str>}              on failure (D26 容错降级)

  format_repo_map_markdown(structure, max_lines) → str
    Inherited rendering from smart_map.py generate_markdown.

Design authority: spec 02_design v5.2 §3.2.2 (D24/D25/D26 + D10)
Execution authority: THIS FILE.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

from common.ignore import IndexIgnorePolicy

# v5 D25: 防爆参数继承 smart_map.py 常量
DEFAULT_IGNORE_DIRS: frozenset[str] = frozenset({
    "node_modules", ".git", ".idea", ".vscode", "__pycache__",
    "dist", "build", "coverage", ".venv", "venv",
    ".pytest_cache", ".maglev_build", ".maglev",
})
DEFAULT_ANCHOR_FILES: frozenset[str] = frozenset({
    "package.json", "pom.xml", "go.mod", "Cargo.toml",
    "requirements.txt", "README.md", "Dockerfile", "Makefile",
    "AGENTS.md", "llms.txt",
})
DEFAULT_MAX_DEPTH: int = 5
DEFAULT_MAX_LINES: int = 200

# v5 D26: radar 调用超时上限（避免大仓库分析挂死）
RADAR_TIMEOUT_SECONDS: int = 30


def _is_ignored(path: str, ignore_dirs: frozenset[str]) -> bool:
    parts = path.split(os.sep)
    return any(p in ignore_dirs for p in parts)


def _readme_summary(dir_path: Path) -> str:
    readme = dir_path / "README.md"
    if not readme.is_file():
        return ""
    try:
        with readme.open("r", encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line[:100]
                if line.startswith("#") and len(line) > 2:
                    return line.lstrip("#").strip()[:100]
    except OSError:
        return ""
    return ""


def walk_with_anchors(
    root: Path | str,
    *,
    ignore_dirs: Optional[frozenset[str] | set[str] | list[str] | IndexIgnorePolicy] = None,
    anchor_files: Optional[frozenset[str] | set[str] | list[str]] = None,
    max_depth: int = DEFAULT_MAX_DEPTH,
    max_lines: int = DEFAULT_MAX_LINES,
) -> list[dict[str, Any]]:
    """Walk root; record dirs that are root, contain anchor files, or sit at depth 1.

    Output is a list of {path, depth, name, anchors, summary} entries, capped by
    max_lines (which approximates output size in markdown lines, see
    format_repo_map_markdown).
    """
    root_path = Path(root)
    ignore = (
        ignore_dirs
        if isinstance(ignore_dirs, IndexIgnorePolicy)
        else frozenset(ignore_dirs) if ignore_dirs is not None else DEFAULT_IGNORE_DIRS
    )
    anchors = frozenset(anchor_files) if anchor_files is not None else DEFAULT_ANCHOR_FILES

    structure: list[dict[str, Any]] = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # In-place pruning to skip ignored / hidden dirs
        if isinstance(ignore, IndexIgnorePolicy):
            dirnames[:] = [
                name for name in dirnames
                if not ignore.should_ignore_directory(Path(dirpath) / name)
            ]
        else:
            dirnames[:] = [
                name for name in dirnames
                if name not in ignore and not name.startswith(".")
            ]

        rel = os.path.relpath(dirpath, root_path)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        if depth > max_depth:
            continue

        anchors_found = sorted(f for f in filenames if f in anchors)
        # Record if root, contains anchors, or is depth-1 child
        if depth == 0 or anchors_found or depth == 1:
            structure.append({
                "path": rel,
                "depth": depth,
                "name": os.path.basename(dirpath) if depth > 0 else "ROOT",
                "anchors": anchors_found,
                "summary": _readme_summary(Path(dirpath)),
            })
            if len(structure) >= max_lines:
                break
    return structure


def format_repo_map_markdown(
    structure: list[dict[str, Any]], max_lines: int = DEFAULT_MAX_LINES
) -> str:
    """Render walk_with_anchors output as repository map markdown."""
    lines: list[str] = [
        "# 代码仓库地图 (Repository Map)",
        "",
        "> 由 index-protocol track_map.py 生成。仅显示包含关键文件的模块。",
        "",
        "## 目录结构",
        "",
    ]
    for item in structure:
        if len(lines) >= max_lines:
            lines.append(f"\n... (已截断: 超过 {max_lines} 行限制)")
            break
        indent = "    " * item["depth"]
        icon = "📂"
        if "package.json" in item["anchors"]:
            icon = "📦"
        elif "go.mod" in item["anchors"]:
            icon = "🐹"
        elif "pom.xml" in item["anchors"]:
            icon = "☕"
        line = f"{indent}- {icon} `{item['name']}/`"
        if item["summary"]:
            line += f" — *{item['summary']}*"
        lines.append(line)
    return "\n".join(lines) + "\n"


# ---------------- radar invocation (D24 / D26) ----------------

class RadarInvocationError(RuntimeError):
    """Raised when radar binary execution fails in a recoverable way."""


def _radar_binary() -> Optional[str]:
    return shutil.which("radar")


def _run_radar(args: list[str], cwd: Path) -> dict[str, Any]:
    """Run radar with given args; return parsed JSON output."""
    binary = _radar_binary()
    if binary is None:
        raise FileNotFoundError("radar binary not on PATH")

    proc = subprocess.run(
        [binary, *args, "--json"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=RADAR_TIMEOUT_SECONDS,
    )
    if proc.returncode != 0:
        raise RadarInvocationError(
            f"radar {' '.join(args)} exit={proc.returncode}: "
            f"{proc.stderr.strip()[:200]}"
        )
    import json
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RadarInvocationError(f"radar output not valid JSON: {exc}") from exc


def invoke_radar_summary(
    root: Path | str,
    *,
    hotspot_top: int = 10,
    include_unused: bool = False,
    include_cycles_count: bool = True,
    max_output_lines: int = DEFAULT_MAX_LINES,
) -> dict[str, Any]:
    """Subprocess invoke radar, collect summary, truncate by max_output_lines.

    On any radar-side failure (binary missing / timeout / non-zero / parse error),
    return {"skipped": True, "reason": <str>} per D26.

    Output schema on success:
      {
        "hotspot": [{path, score}, ...]            # length ≤ hotspot_top
        "cycles_count": <int>                      # if include_cycles_count
        "unused_count": <int>                      # if include_unused
        "_truncated": True                         # if max_output_lines hit
      }
    """
    root_path = Path(root)
    summary: dict[str, Any] = {}

    try:
        # 1. hotspot Top N
        try:
            data = _run_radar(["hotspot", "--top", str(hotspot_top)], cwd=root_path)
            hotspot = data.get("hotspot") or data.get("items") or []
            summary["hotspot"] = hotspot[:hotspot_top]
        except (FileNotFoundError, subprocess.TimeoutExpired,
                RadarInvocationError) as exc:
            return {"skipped": True, "reason": f"hotspot: {exc}"}

        # 2. cycles count
        if include_cycles_count:
            try:
                data = _run_radar(["cycles"], cwd=root_path)
                cycles = data.get("cycles") or data.get("items") or []
                summary["cycles_count"] = len(cycles)
            except (subprocess.TimeoutExpired, RadarInvocationError) as exc:
                summary["cycles_count"] = None
                summary["_cycles_skipped"] = str(exc)

        # 3. unused count
        if include_unused:
            try:
                data = _run_radar(["unused"], cwd=root_path)
                unused = data.get("unused") or data.get("items") or []
                summary["unused_count"] = len(unused)
            except (subprocess.TimeoutExpired, RadarInvocationError) as exc:
                summary["unused_count"] = None
                summary["_unused_skipped"] = str(exc)

    except Exception as exc:  # final safety net
        return {"skipped": True, "reason": f"unexpected: {exc.__class__.__name__}: {exc}"}

    # Truncation: max_output_lines is line-budget for the final yaml dump
    if len(summary.get("hotspot", [])) > 0:
        approx_lines = (
            len(summary.get("hotspot", [])) * 3
            + (3 if "cycles_count" in summary else 0)
            + (3 if "unused_count" in summary else 0)
        )
        if approx_lines > max_output_lines:
            keep = max(1, hotspot_top - (approx_lines - max_output_lines) // 3)
            summary["hotspot"] = summary["hotspot"][:keep]
            summary["_truncated"] = True
            summary["_truncated_reason"] = (
                f"approx_lines {approx_lines} > max_output_lines {max_output_lines}"
            )

    return summary


__all__ = [
    "DEFAULT_IGNORE_DIRS",
    "DEFAULT_ANCHOR_FILES",
    "DEFAULT_MAX_DEPTH",
    "DEFAULT_MAX_LINES",
    "RADAR_TIMEOUT_SECONDS",
    "RadarInvocationError",
    "walk_with_anchors",
    "format_repo_map_markdown",
    "invoke_radar_summary",
]
