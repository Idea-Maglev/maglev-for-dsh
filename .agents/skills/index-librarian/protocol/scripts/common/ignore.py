"""Project-level directory ignore policy for index tracks."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


DEFAULT_INDEXING_CONFIG: dict[str, Any] = {
    "ignore_dirs": [".agent", ".claude", ".codex", ".github"],
    "ignore_hidden_dirs": True,
    "inherit_gitignore": True,
}
HARD_IGNORED_DIRS = frozenset({".git", ".maglev"})


class IndexIgnorePolicy:
    """Combine project defaults, track additions, and Git ignore semantics."""

    def __init__(
        self,
        repository_root: Path,
        track_ignore_dirs: set[str],
        indexing_config: dict[str, Any] | None = None,
    ) -> None:
        config = {**DEFAULT_INDEXING_CONFIG, **(indexing_config or {})}
        configured = config.get("ignore_dirs") or []
        self.repository_root = repository_root.resolve()
        self.ignore_dirs = frozenset((*track_ignore_dirs, *configured))
        self.ignore_hidden_dirs = bool(config.get("ignore_hidden_dirs", True))
        self.inherit_gitignore = bool(config.get("inherit_gitignore", True))
        self._gitignore_cache: dict[Path, bool] = {}

    def should_ignore_directory(self, directory: Path) -> bool:
        """Return whether a directory and its subtree must stay out of indexes."""
        if directory.name in HARD_IGNORED_DIRS or directory.name in self.ignore_dirs:
            return True
        if self.ignore_hidden_dirs and directory.name.startswith("."):
            return True
        if not self.inherit_gitignore:
            return False
        return self._is_gitignored(directory)

    def _is_gitignored(self, directory: Path) -> bool:
        directory = directory.resolve()
        cached = self._gitignore_cache.get(directory)
        if cached is not None:
            return cached
        try:
            relative = directory.relative_to(self.repository_root).as_posix()
        except ValueError:
            return False

        try:
            result = subprocess.run(
                ["git", "-C", str(self.repository_root), "check-ignore", "--no-index", "-q", "--", f"{relative}/"],
                check=False,
                capture_output=True,
                text=True,
            )
            ignored = result.returncode == 0
        except OSError:
            ignored = False
        self._gitignore_cache[directory] = ignored
        return ignored


def should_skip_entry(path: Path, ignore: set[str] | IndexIgnorePolicy) -> bool:
    """Keep legacy set callers compatible while policies handle directory rules."""
    if isinstance(ignore, IndexIgnorePolicy):
        return path.is_dir() and ignore.should_ignore_directory(path)
    if path.name in ignore:
        return True
    return path.is_dir() and path.name.startswith(".")
