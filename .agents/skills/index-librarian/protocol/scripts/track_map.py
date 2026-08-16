#!/usr/bin/env python3
"""
track_map.py — Generic per-track cognitive/structural map dispatcher.

Per type:
  - dir-tree    → INDEX.md network is the map
  - repo-entry  → repo entry map (smart_map.py 行为合并)
  - code-tree   → anchor navigation markdown

Design authority: specs/20_evolution/active/unified_doc_tree_indexer/02_design.md
Execution authority: THIS FILE.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

import _track_resolver  # noqa: E402
import _code_tree_helpers as cth  # noqa: E402
from common.ignore import IndexIgnorePolicy  # noqa: E402


def _find_repo_root() -> Path:
    return _track_resolver._find_repo_root()


def _map_output_path(track: dict[str, Any], repo_root: Path) -> Path:
    """Use an explicit path or derive a unique map next to the scan output."""
    configured = track.get("map_output")
    if configured:
        return repo_root / configured

    output = Path(track.get("output") or f"{track['id']}.yaml")
    stem = output.stem if output.stem.endswith("-map") else f"{output.stem}-map"
    return repo_root / output.with_name(f"{stem}.md")


# ---------- dir-tree ----------

def _map_dir_tree(track: dict[str, Any]) -> int:
    """A dir-tree's adjacent INDEX.md network is its navigational map."""
    print(f"[track-map] dir-tree {track['id']}: INDEX.md network is the navigational map")
    return 0


# ---------- repo-entry (D10: smart_map.py 行为合并) ----------

def _map_repo_entry(track: dict[str, Any]) -> int:
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-map] skip: root {track['root']} not found")
        return 0

    # repo-entry 的 map 走 smart_map.py 移植行为：浅扫 + 锚点导航
    structure = cth.walk_with_anchors(
        root_dir,
        ignore_dirs=IndexIgnorePolicy(
            repo_root,
            set(track.get("ignore") or cth.DEFAULT_IGNORE_DIRS),
            _track_resolver.get_indexing_config(repo_root),
        ),
        anchor_files=frozenset(track.get("anchor_files") or cth.DEFAULT_ANCHOR_FILES),
        max_depth=cth.DEFAULT_MAX_DEPTH,
        max_lines=cth.DEFAULT_MAX_LINES,
    )
    markdown = cth.format_repo_map_markdown(structure, max_lines=cth.DEFAULT_MAX_LINES)

    out_path = _map_output_path(track, repo_root)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    print(
        f"[track-map] repo-entry {track['id']}: wrote {len(structure)} entries "
        f"→ {out_path.relative_to(repo_root)}"
    )
    return 0


# ---------- code-tree ----------

def _map_code_tree(track: dict[str, Any]) -> int:
    """code-tree 的 map = 锚点导航 markdown（不含 radar 摘要，摘要在 track_scan 段）"""
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-map] skip: root {track['root']} not found")
        return 0

    structure = cth.walk_with_anchors(
        root_dir,
        ignore_dirs=IndexIgnorePolicy(
            repo_root,
            set(track.get("ignore") or cth.DEFAULT_IGNORE_DIRS),
            _track_resolver.get_indexing_config(repo_root),
        ),
        anchor_files=frozenset(track.get("anchor_files") or cth.DEFAULT_ANCHOR_FILES),
        max_depth=int(track.get("depth_limit", cth.DEFAULT_MAX_DEPTH)),
        max_lines=cth.DEFAULT_MAX_LINES,
    )
    markdown = cth.format_repo_map_markdown(structure, max_lines=cth.DEFAULT_MAX_LINES)

    out_path = _map_output_path(track, repo_root)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    print(
        f"[track-map] code-tree {track['id']}: wrote {len(structure)} entries "
        f"→ {out_path.relative_to(repo_root)}"
    )
    return 0


DISPATCH = {
    "dir-tree": _map_dir_tree,
    "repo-entry": _map_repo_entry,
    "code-tree": _map_code_tree,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--track-id")
    target.add_argument("--all", action="store_true", help="map every enabled track")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    tracks = (
        _track_resolver.list_tracks()
        if args.all
        else [_track_resolver.resolve(args.track_id)]
    )
    exit_code = 0
    for track in (track for track in tracks if track is not None):
        handler = DISPATCH.get(track["type"])
        if handler is None:
            print(f"[track-map] warn: no dispatch for type {track['type']!r}, skip")
            continue
        exit_code = max(exit_code, handler(track))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
