"""Read Profile-owned Reality directories without changing their contract."""

from __future__ import annotations

import json
from pathlib import Path


def _managed_directories_for_profile(reality_root: Path, profile_path: Path) -> set[Path]:
    """Return Profile-owned directories for one Reality root."""
    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return set()

    if profile.get("profile_id") != "maglev-core-v1" or profile.get("layout_version") != 1:
        return set()

    managed: set[Path] = set()
    for domain in profile.get("domains", []):
        domain_root = reality_root / domain
        managed.add(domain_root)
        for entry in profile.get("domain_entry_files", []):
            managed.add(domain_root / Path(entry).parent)

    crosscutting_root = reality_root / "crosscutting"
    for entry in profile.get("crosscutting_entry_files", []):
        managed.add(crosscutting_root / Path(entry).parent)
    return managed


def profile_managed_directories(tree_root: Path) -> set[Path]:
    """Find all maglev-core-v1 Profiles under a track and return their directories."""
    profile_paths = [tree_root / "00_profile.yaml"]
    if not profile_paths[0].exists():
        profile_paths = sorted(tree_root.rglob("00_profile.yaml"))

    managed: set[Path] = set()
    for profile_path in profile_paths:
        managed.update(_managed_directories_for_profile(profile_path.parent, profile_path))
    return managed
