#!/usr/bin/env python3
"""Resolve enabled extension candidates for the code-execution slot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


DEFAULT_LOCK = Path(".maglev/extensions.lock")


def resolve(workspace_root: Path, lock_file: Path, slot: str) -> dict[str, Any]:
    path = lock_file if lock_file.is_absolute() else workspace_root / lock_file
    if not path.exists():
        return _success(slot, [])
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return _failure("lock_invalid", f"failed to read extension lock: {exc}", path)
    if not isinstance(document, dict) or document.get("version") != 1:
        return _failure("lock_invalid", "extension lock must be a version 1 mapping", path)
    installed = document.get("installed")
    if not isinstance(installed, list):
        return _failure("lock_invalid", "extension lock installed field must be a list", path)

    candidates: list[dict[str, Any]] = []
    for record in installed:
        if not isinstance(record, dict) or not record.get("enabled"):
            continue
        if record.get("kind") == "external_integration" and record.get("detected") is not True:
            continue
        for registration in record.get("plugin_slots") or []:
            if not isinstance(registration, dict) or registration.get("slot") != slot:
                continue
            entry_skill = registration.get("entry_skill")
            if not isinstance(entry_skill, str) or not entry_skill.strip():
                continue
            priority = registration.get("priority", 50)
            candidates.append(
                {
                    "extension_id": record.get("id"),
                    "kind": record.get("kind", "asset_pack"),
                    "provider": record.get("provider"),
                    "entry_skill": entry_skill,
                    "selection_hint": registration.get("selection_hint", ""),
                    "priority": priority if isinstance(priority, int) else 50,
                }
            )
    candidates.sort(key=lambda candidate: (-candidate["priority"], str(candidate["extension_id"])))
    return _success(slot, candidates)


def _success(slot: str, candidates: list[dict[str, Any]]) -> dict[str, Any]:
    reason = "candidate_not_selected" if candidates else "no_enabled_candidate"
    return {
        "status": "pass",
        "result": {
            "slot": slot,
            "candidates": candidates,
            "fallback": {"mode": "agent-native", "reason": reason},
        },
        "issues": [],
    }


def _failure(code: str, message: str, path: Path) -> dict[str, Any]:
    return {
        "status": "fail",
        "result": None,
        "issues": [{"level": "error", "code": code, "message": message, "path": str(path)}],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve Maglev code execution slot candidates")
    parser.add_argument("--workspace-root", type=Path, default=Path.cwd())
    parser.add_argument("--lock-file", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--slot", choices=["code-execution"], default="code-execution")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = resolve(args.workspace_root.resolve(), args.lock_file, args.slot)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True).rstrip())
    return 1 if payload["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
