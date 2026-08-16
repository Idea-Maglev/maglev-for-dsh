#!/usr/bin/env python3
"""
track_verify.py — Generic per-track health check dispatcher.

Per type:
  - dir-tree    → verify INDEX.md existence + frontmatter validity
  - repo-entry  → verify all declared anchor patterns hit at least once
  - code-tree   → verify root exists
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
from common.index_gen import discover_indexable_dirs  # noqa: E402
from common.ignore import IndexIgnorePolicy  # noqa: E402
from common.knowledge import build_directory_records  # noqa: E402
from common.frontmatter import parse_file  # noqa: E402
from common.profile_layout import profile_managed_directories  # noqa: E402


def _find_repo_root() -> Path:
    return _track_resolver._find_repo_root()


# ---------- dir-tree ----------

def _verify_dir_tree(track: dict[str, Any]) -> int:
    """Verify dir-tree: INDEX.md existence + frontmatter validity."""
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-verify] dir-tree {track['id']}: root {track['root']} not found")
        return 1

    issues: list[str] = []

    # 1. Output file existence
    output = track.get("output")
    if output:
        output_path = repo_root / output
        if not output_path.exists():
            issues.append(f"scan output missing: {output} (run scan first)")

    # 2. Discover dirs and check INDEX.md existence
    ignore = IndexIgnorePolicy(
        repo_root,
        set(track.get("ignore") or ["_meta"]),
        _track_resolver.get_indexing_config(repo_root),
    )
    max_depth = track.get("max_depth", 4)
    skip_index_dirs = set(track.get("skip_index_dirs") or [])
    collapse_single_file_dirs = set(track.get("collapse_single_file_dirs") or [])
    dirs = discover_indexable_dirs(
        root_dir,
        ignore,
        max_depth,
        skip_index_dirs,
        collapse_single_file_dirs,
    )
    profile_managed = profile_managed_directories(root_dir)

    for dir_path in dirs:
        if dir_path in profile_managed:
            continue
        idx = dir_path / "INDEX.md"
        if not idx.exists():
            rel = dir_path.relative_to(repo_root)
            issues.append(f"missing INDEX.md: {rel}/")
            continue

        # 3. Frontmatter validation (relaxed: just check type field)
        result = parse_file(idx)
        if not result.is_valid:
            rel = idx.relative_to(repo_root)
            # Only report critical errors, not missing optional fields
            critical = [e for e in result.errors if "type must be" in e or "No YAML" in e or "YAML parse" in e]
            if critical:
                issues.append(f"invalid frontmatter: {rel} ({critical[0]})")

        # Knowledge records are script-owned and must exactly reflect direct files.
        records = result.metadata.get("knowledge_records")
        if result.metadata.get("knowledge_schema_version") != 1 or not isinstance(records, list):
            rel = idx.relative_to(repo_root)
            issues.append(f"missing knowledge records: {rel} (run scan first)")
            continue
        expected = {
            item["path"]: item["content_fingerprint"]
            for item in build_directory_records(
                dir_path,
                root_dir,
                ignore,
                repo_root,
                collapse_single_file_dirs,
            )
        }
        actual = {
            item.get("path"): item.get("content_fingerprint")
            for item in records if isinstance(item, dict)
        }
        if expected != actual:
            rel = idx.relative_to(repo_root)
            issues.append(f"stale knowledge records: {rel} (run scan first)")
        for record in records:
            if not isinstance(record, dict):
                continue
            path = record.get("path")
            evidence = record.get("evidence") or []
            if not isinstance(path, str) or not isinstance(evidence, list):
                rel = idx.relative_to(repo_root)
                issues.append(f"invalid knowledge record: {rel} (run scan first)")
                break
            if any(not isinstance(item, str) or not item.startswith(path) for item in evidence):
                rel = idx.relative_to(repo_root)
                issues.append(f"unreachable knowledge evidence: {rel} (run scan first)")
                break

    if issues:
        print(f"[track-verify] dir-tree {track['id']}: {len(issues)} issue(s)")
        for s in issues[:15]:
            print(f"  - {s}")
        return 1
    print(f"[track-verify] dir-tree {track['id']}: ok ({len(dirs)} dirs checked)")
    return 0


# ---------- repo-entry ----------

def _verify_repo_entry(track: dict[str, Any]) -> int:
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        return 0

    patterns = track.get("patterns") or []
    misses = [pat for pat in patterns if not any(root_dir.glob(pat))]
    if misses:
        print(
            f"[track-verify] repo-entry {track['id']}: {len(misses)} pattern(s) "
            f"matched zero files (informational, not a failure)"
        )
        for m in misses:
            print(f"  - {m}")
    print(f"[track-verify] repo-entry {track['id']}: ok")
    return 0


# ---------- code-tree ----------

def _verify_code_tree(track: dict[str, Any]) -> int:
    repo_root = _find_repo_root()
    root_dir = repo_root / track["root"]
    if not root_dir.is_dir():
        print(f"[track-verify] code-tree {track['id']}: root {track['root']} not found")
        return 1
    print(f"[track-verify] code-tree {track['id']}: ok")
    return 0


DISPATCH = {
    "dir-tree": _verify_dir_tree,
    "repo-entry": _verify_repo_entry,
    "code-tree": _verify_code_tree,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--track-id")
    target.add_argument("--all", action="store_true", help="verify every enabled track")
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
            print(f"[track-verify] warn: no dispatch for type {track['type']!r}, skip")
            continue
        exit_code = max(exit_code, handler(track))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
