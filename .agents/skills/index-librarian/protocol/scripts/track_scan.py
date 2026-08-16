#!/usr/bin/env python3
"""
track_scan.py — Generic per-track scan dispatcher.

Reads track config from registry.yaml via _track_resolver, then dispatches
to the appropriate scanner based on track.type:

  - dir-tree    → _scan_dir_tree (recursive INDEX.md generation)
  - repo-entry  → scan_repo_entry (depth_limit=1 hard cap, D8)
  - code-tree   → scan_code_tree (full impl)

Design authority: specs/20_evolution/active/unified_doc_tree_indexer/02_design.md
Execution authority: THIS FILE.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

import _track_resolver  # noqa: E402
import _code_tree_helpers as cth  # noqa: E402
from common.index_gen import (  # noqa: E402
    discover_indexable_dirs,
    find_collapsed_leaf_dirs,
    generate_or_update_index,
    build_summary,
)
from common.ignore import IndexIgnorePolicy  # noqa: E402
from common.profile_layout import profile_managed_directories  # noqa: E402

# Hard caps (D8 / D25)
REPO_ENTRY_MAX_DEPTH = 1


def _find_repo_root() -> Path:
    return _track_resolver._find_repo_root()


def _resolve_output_path(track: dict[str, Any]) -> Path:
    repo_root = _find_repo_root()
    output = track.get("output") or f"{track['root'].rstrip('/')}/_meta/index.yaml"
    return repo_root / output


def _write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        yaml.safe_dump(data, fp, allow_unicode=True, sort_keys=False)


# ---------- dir-tree (unified) ----------

def _scan_dir_tree(track: dict[str, Any]) -> int:
    """Universal directory tree scanner — generates INDEX.md network."""
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-scan] skip: track {track['id']!r} root {track['root']} not found")
        return 0

    max_depth = track.get("max_depth", 4)
    ignore = IndexIgnorePolicy(
        repo_root,
        set(track.get("ignore") or ["_meta"]),
        _track_resolver.get_indexing_config(repo_root),
    )
    skip_index_dirs = set(track.get("skip_index_dirs") or [])
    collapse_single_file_dirs = set(track.get("collapse_single_file_dirs") or [])
    entity_type = track.get("entity_type", "document")
    child_type_cfg = track.get("child_type", "auto")

    # Phase 1: discover all indexable directories
    dirs = discover_indexable_dirs(
        root_dir,
        ignore,
        max_depth,
        skip_index_dirs,
        collapse_single_file_dirs,
    )
    profile_managed = profile_managed_directories(root_dir)
    dirs = [path for path in dirs if path not in profile_managed]

    # Phase 2: generate/update INDEX.md (bottom-up order)
    created = 0
    updated = 0
    for dir_path in dirs:
        index_existed = (dir_path / "INDEX.md").exists()
        wrote = generate_or_update_index(
            dir_path,
            root_dir,
            entity_type,
            child_type_cfg,
            ignore,
            repo_root,
            collapse_single_file_dirs,
        )
        if wrote:
            if index_existed:
                updated += 1
            else:
                created += 1

    # Phase 3: remove obsolete leaf indexes only after parent records collapse them.
    pruned = 0
    for dir_path in find_collapsed_leaf_dirs(
        root_dir, ignore, max_depth, collapse_single_file_dirs
    ):
        index_path = dir_path / "INDEX.md"
        if index_path.is_file():
            index_path.unlink()
            pruned += 1

    # Phase 4: write summary YAML
    summary = build_summary(track, root_dir, repo_root, dirs)
    out_path = _resolve_output_path(track)
    _write_yaml(out_path, summary)

    print(
        f"[track-scan] dir-tree {track['id']}: {len(dirs)} dirs "
        f"(created={created}, updated={updated}, pruned={pruned}) → {out_path}"
    )
    return 0


# ---------- repo-entry (new impl, D8 hard cap) ----------

def _scan_repo_entry(track: dict[str, Any]) -> int:
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-scan] skip: track {track['id']!r} root {track['root']} not found")
        return 0

    # D8: depth_limit hard-capped to 1 regardless of track config
    requested = track.get("depth_limit", 1)
    depth_limit = REPO_ENTRY_MAX_DEPTH
    if requested != REPO_ENTRY_MAX_DEPTH:
        print(
            f"[track-scan] note: repo-entry depth_limit clamped from {requested} to "
            f"{REPO_ENTRY_MAX_DEPTH} (D8 hard cap)"
        )

    patterns = track.get("patterns") or [
        "README.md",
        "AGENTS.md",
        "llms.txt",
        "CHANGELOG.md",
        "package.json",
        "Makefile",
        "Dockerfile",
    ]
    ignore = IndexIgnorePolicy(
        repo_root,
        set(track.get("ignore") or cth.DEFAULT_IGNORE_DIRS),
        _track_resolver.get_indexing_config(repo_root),
    )

    def _path_blocked(p: Path) -> bool:
        # Skip hidden dirs (start with .) and ignored dirs anywhere on path
        rel = p.relative_to(root_dir).as_posix()
        parent = root_dir
        for part in rel.split("/")[:-1]:  # exclude filename itself
            parent /= part
            if ignore.should_ignore_directory(parent):
                return True
        return False

    anchors: list[dict[str, Any]] = []
    seen: set[str] = set()
    for pat in patterns:
        # depth 0 (root)
        for path in sorted(root_dir.glob(pat)):
            if path.is_file() and not _path_blocked(path):
                rel = path.relative_to(repo_root).as_posix()
                if rel not in seen:
                    seen.add(rel)
                    anchors.append({"path": rel, "size": path.stat().st_size})
        # depth 1 (immediate children)
        if depth_limit >= 1:
            for path in sorted(root_dir.glob(f"*/{pat}")):
                if path.is_file() and not _path_blocked(path):
                    rel = path.relative_to(repo_root).as_posix()
                    if rel not in seen:
                        seen.add(rel)
                        anchors.append({"path": rel, "size": path.stat().st_size})

    output = {
        "track_id": track["id"],
        "track_type": track["type"],
        "root": track["root"],
        "depth_limit": depth_limit,
        "anchor_count": len(anchors),
        "anchors": anchors,
    }
    out_path = _resolve_output_path(track)
    _write_yaml(out_path, output)
    print(
        f"[track-scan] repo-entry {track['id']}: wrote {len(anchors)} anchors "
        f"→ {out_path}"
    )
    return 0


# ---------- code-tree (full impl, D24/D25/D26) ----------

def _scan_code_tree(track: dict[str, Any]) -> int:
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-scan] skip: track {track['id']!r} root {track['root']} not found")
        return 0

    # 第一段：锚点导航（继承 smart_map.py 防爆参数 D25）
    ignore_dirs = IndexIgnorePolicy(
        repo_root,
        set(track.get("ignore") or cth.DEFAULT_IGNORE_DIRS),
        _track_resolver.get_indexing_config(repo_root),
    )
    anchor_files = frozenset(
        track.get("anchor_files") or cth.DEFAULT_ANCHOR_FILES
    )
    max_depth = int(track.get("depth_limit", cth.DEFAULT_MAX_DEPTH))

    structure = cth.walk_with_anchors(
        root_dir,
        ignore_dirs=ignore_dirs,
        anchor_files=anchor_files,
        max_depth=max_depth,
        max_lines=cth.DEFAULT_MAX_LINES,
    )
    # Strip empty summaries to keep yaml compact
    anchors = [
        {k: v for k, v in item.items() if v not in ("", [])}
        for item in structure
    ]

    output: dict[str, Any] = {
        "track_id": track["id"],
        "track_type": track["type"],
        "root": track["root"],
        "depth_limit": max_depth,
        "anchor_count": len(anchors),
        "anchors": anchors,
    }

    # 第二段：radar 摘要（按 radar_summary 配置；D24 + D26 容错降级）
    rs_cfg = track.get("radar_summary") or {}
    if rs_cfg.get("enabled"):
        try:
            output["radar_summary"] = cth.invoke_radar_summary(
                root_dir,
                hotspot_top=rs_cfg.get("hotspot_top", 10),
                include_unused=rs_cfg.get("include_unused", False),
                include_cycles_count=rs_cfg.get("include_cycles_count", True),
                max_output_lines=rs_cfg.get("max_output_lines", cth.DEFAULT_MAX_LINES),
            )
        except Exception as exc:  # final guard (D26)
            output["radar_summary"] = {
                "skipped": True,
                "reason": f"unexpected: {exc.__class__.__name__}: {exc}",
            }
            print(
                f"[track-scan] warn: track {track['id']!r} radar summary skipped: {exc}"
            )
    else:
        output["radar_summary"] = {"skipped": True, "reason": "disabled in registry.yaml"}

    out_path = _resolve_output_path(track)
    _write_yaml(out_path, output)
    rs_status = output["radar_summary"]
    rs_note = "skipped" if rs_status.get("skipped") else "ok"
    print(
        f"[track-scan] code-tree {track['id']}: wrote {len(anchors)} anchors + "
        f"radar_summary={rs_note} → {out_path}"
    )
    return 0


# ---------- dispatch ----------

DISPATCH = {
    "dir-tree": _scan_dir_tree,
    "repo-entry": _scan_repo_entry,
    "code-tree": _scan_code_tree,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--track-id")
    target.add_argument("--all", action="store_true", help="scan every enabled track")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    tracks = (
        _track_resolver.list_tracks()
        if args.all
        else [_track_resolver.resolve(args.track_id)]
    )
    exit_code = 0
    for track in (track for track in tracks if track is not None):
        track_type = track["type"]
        handler = DISPATCH.get(track_type)
        if handler is None:
            print(f"[track-scan] warn: no dispatch for type {track_type!r}, skip")
            continue
        if args.debug:
            print(f"[track-scan] debug: track={json.dumps(track, ensure_ascii=False)}")
        exit_code = max(exit_code, handler(track))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
