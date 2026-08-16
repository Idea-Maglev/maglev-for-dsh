"""
Track Resolver — 读 registry.yaml / schema 校验 / 返回 track config

Design authority: specs/20_evolution/active/unified_doc_tree_indexer/02_design.md
Execution authority: THIS FILE.

Used by: track_scan.py / track_verify.py / track_map.py
Project config: .maglev/config.json 的 indexing 段提供所有 track 继承的目录忽略策略。
Schema:
  必填: id (str) / type (str, enum: dir-tree/repo-entry/code-tree) / root (str)
  可选: output (str) / entity_type (str) / child_type (str) / max_depth (int)
        / ignore (list[str]) / skip_index_dirs (list[str]) / collapse_single_file_dirs (list[str])
        / patterns (list[str]) / thresholds (dict) / depth_limit (int) / radar_summary (dict)
        / enabled (bool, default true)

Behavior on errors:
  - registry.yaml not found / unparseable → exit code 2 + JSON error
  - track_id not found → return None (caller decides exit 0 vs error)
  - schema invalid (missing required / unknown type) → return None + warn log
"""

from __future__ import annotations

import sys
import json
from pathlib import Path
from typing import Any, Optional

import yaml

from common.ignore import DEFAULT_INDEXING_CONFIG

REGISTRY_REL_PATH = ".agents/skills/index-librarian/protocol/registry.yaml"

REQUIRED_FIELDS = ("id", "type", "root")
KNOWN_TYPES = frozenset({"dir-tree", "repo-entry", "code-tree"})


def get_indexing_config(repository_root: Path) -> dict[str, Any]:
    """Load project-owned indexing defaults without making config mandatory."""
    config = dict(DEFAULT_INDEXING_CONFIG)
    config_path = repository_root / ".maglev" / "config.json"
    if not config_path.is_file():
        return config
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[track-resolver] warn: cannot read {config_path}: {exc}")
        return config
    indexing = data.get("indexing") if isinstance(data, dict) else None
    if not isinstance(indexing, dict):
        return config
    if isinstance(indexing.get("ignore_dirs"), list) and all(
        isinstance(item, str) for item in indexing["ignore_dirs"]
    ):
        config["ignore_dirs"] = indexing["ignore_dirs"]
    for key in ("ignore_hidden_dirs", "inherit_gitignore"):
        if isinstance(indexing.get(key), bool):
            config[key] = indexing[key]
    return config


def _find_repo_root(start: Optional[Path] = None) -> Path:
    """Walk up from given path (or cwd) to find .git directory."""
    current = (start or Path.cwd()).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def _load_registry(registry_path: Optional[Path] = None) -> dict[str, Any]:
    """Load registry.yaml. Returns parsed dict; exits with code 2 on hard errors."""
    if registry_path is None:
        registry_path = _find_repo_root() / REGISTRY_REL_PATH

    if not registry_path.is_file():
        print(
            f"[track-resolver] error: registry.yaml not found at {registry_path}",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        with registry_path.open("r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp) or {}
    except yaml.YAMLError as exc:
        print(
            f"[track-resolver] error: failed to parse {registry_path}: {exc}",
            file=sys.stderr,
        )
        sys.exit(2)

    if not isinstance(data, dict):
        print(
            f"[track-resolver] error: registry.yaml top level must be a mapping",
            file=sys.stderr,
        )
        sys.exit(2)

    return data


def _validate_track(track: Any, *, log_prefix: str = "[track-resolver]") -> bool:
    """Return True if track passes schema check; print warn and return False otherwise."""
    if not isinstance(track, dict):
        print(f"{log_prefix} warn: track entry not a mapping, skipped: {track!r}")
        return False

    for field in REQUIRED_FIELDS:
        if field not in track or track[field] in (None, ""):
            print(
                f"{log_prefix} warn: track {track.get('id', '?')!r} missing required "
                f"field {field!r}, skipped"
            )
            return False

    track_type = track["type"]
    if track_type not in KNOWN_TYPES:
        print(
            f"{log_prefix} warn: track {track['id']!r} has unknown type {track_type!r} "
            f"(known: {sorted(KNOWN_TYPES)}), skipped"
        )
        return False

    if "enabled" in track and not isinstance(track["enabled"], bool):
        print(
            f"{log_prefix} warn: track {track['id']!r} has non-boolean "
            "'enabled', skipped"
        )
        return False

    for field in ("output", "map_output"):
        if field in track and not isinstance(track[field], str):
            print(
                f"{log_prefix} warn: track {track['id']!r} has non-string "
                f"{field!r}, skipped"
            )
            return False

    return True


def list_tracks(
    registry_path: Optional[Path] = None,
    *,
    include_disabled: bool = False,
) -> list[dict[str, Any]]:
    """Return valid tracks, excluding disabled tracks unless explicitly requested."""
    data = _load_registry(registry_path)
    raw_tracks = data.get("tracks") or []
    if not isinstance(raw_tracks, list):
        print("[track-resolver] warn: 'tracks' field is not a list, treating as empty")
        return []
    tracks = [t for t in raw_tracks if _validate_track(t)]
    seen_ids: set[str] = set()
    seen_outputs: set[str] = set()
    seen_map_outputs: set[str] = set()
    unique_tracks: list[dict[str, Any]] = []
    for track in tracks:
        track_id = track["id"]
        output = track.get("output") or f"{track['root'].rstrip('/')}/_meta/index.yaml"
        if track_id in seen_ids:
            print(f"[track-resolver] warn: duplicate track id {track_id!r}, skipped")
            continue
        if output in seen_outputs:
            print(f"[track-resolver] warn: duplicate track output {output!r}, skipped")
            continue
        map_output = track.get("map_output")
        if map_output and map_output in seen_map_outputs:
            print(f"[track-resolver] warn: duplicate track map_output {map_output!r}, skipped")
            continue
        seen_ids.add(track_id)
        seen_outputs.add(output)
        if map_output:
            seen_map_outputs.add(map_output)
        unique_tracks.append(track)
    if include_disabled:
        return unique_tracks
    return [t for t in unique_tracks if t.get("enabled", True)]


def resolve(
    track_id: str,
    *,
    registry_path: Optional[Path] = None,
) -> Optional[dict[str, Any]]:
    """Return validated track config for track_id, or None if not found / invalid.

    Caller convention:
      - None → caller should exit 0 (skip gracefully); user error or absent track is not fatal
      - dict → caller proceeds with track-specific scan
    """
    for track in list_tracks(registry_path):
        if track["id"] == track_id:
            return track

    print(f"[track-resolver] info: track {track_id!r} not found in registry.yaml, skip")
    return None


if __name__ == "__main__":
    # Diagnostic CLI: python _track_resolver.py [<track-id>]
    if len(sys.argv) == 1:
        tracks = list_tracks()
        print(f"found {len(tracks)} valid tracks:")
        for t in tracks:
            print(f"  - {t['id']:<16} type={t['type']:<12} root={t['root']}")
        sys.exit(0)

    track_id = sys.argv[1]
    track = resolve(track_id)
    if track is None:
        sys.exit(0)
    import json

    print(json.dumps(track, indent=2, ensure_ascii=False))
