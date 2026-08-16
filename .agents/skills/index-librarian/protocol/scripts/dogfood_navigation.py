#!/usr/bin/env python3
"""Run the declared navigation tasks and report Top-K coverage facts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from task_navigate import _records  # noqa: E402
from common.navigation import navigate  # noqa: E402


def evaluate_tasks(records: list[dict], tasks: list[dict]) -> dict:
    results = []
    for task in tasks:
        result = navigate(
            task["intent"],
            records,
            known_sources=task.get("known_sources", []),
            missing_questions=task.get("missing_questions", []),
            top_k=int(task.get("top_k", 5)),
        )
        paths = [candidate["path"] for candidate in result["candidates"]]
        expected = set(task.get("expected_paths", []))
        expected_any = set(task.get("expected_any_paths", []))
        status = task.get("expected_status")
        if status:
            covered = result["status"] == status
        elif expected_any:
            covered = bool(expected_any & set(paths))
        else:
            min_hits = int(task.get("min_expected_hits", len(expected)))
            covered = len(expected & set(paths)) >= min_hits
        results.append({
            "id": task["id"],
            "covered": covered,
            "status": result["status"],
            "candidates": paths,
            "expected_paths": sorted(expected),
            "expected_any_paths": sorted(expected_any),
            "missing_questions": task.get("missing_questions", []),
        })
    return {
        "task_count": len(results),
        "covered_count": sum(item["covered"] for item in results),
        "uncovered": [item for item in results if not item["covered"]],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--tasks", type=Path, default=SCRIPT_DIR.parent / "dogfooding.yaml")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    tasks = yaml.safe_load(args.tasks.read_text(encoding="utf-8")) or {}
    records = _records(Path(args.root).resolve())
    payload = evaluate_tasks(records, tasks.get("tasks", []))
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"[navigation-dogfood] covered={payload['covered_count']}/{payload['task_count']}")
        for item in payload["uncovered"]:
            print(f"  - {item['id']}: status={item['status']} candidates={item['candidates']}")
    return 0 if not payload["uncovered"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
