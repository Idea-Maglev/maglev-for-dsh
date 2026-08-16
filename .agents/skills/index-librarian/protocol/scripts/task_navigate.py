#!/usr/bin/env python3
"""Query adjacent INDEX.md knowledge records and emit a navigation receipt."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from common.frontmatter import parse_file  # noqa: E402
from common.navigation import build_receipt, navigate, receipt_status  # noqa: E402


def _records(root: Path) -> list[dict]:
    records: list[dict] = []
    for index in sorted(root.rglob("INDEX.md")):
        parsed = parse_file(index)
        values = parsed.metadata.get("knowledge_records", [])
        if isinstance(values, list):
            records.extend(item for item in values if isinstance(item, dict))
    return records


def _apply_escalation(
    result: dict,
    *,
    step: str | None,
    attempt: int | None,
    scope_hint: str | None,
    known_source_hint: str | None,
    note: str | None,
    exhausted: bool,
) -> dict:
    if result.get("status") != "insufficient" or not step:
        return result
    escalation: dict[str, object] = {
        "step": step,
        "attempt": attempt or 1,
        "basis": {},
    }
    if scope_hint:
        escalation["basis"]["scope_hint"] = scope_hint
    if known_source_hint:
        escalation["basis"]["known_source_hint"] = known_source_hint
    if note:
        escalation["note"] = note
    status = "exhausted" if exhausted else "escalated"
    return {**result, "status": status, "escalation": escalation}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root or scoped subtree")
    parser.add_argument("--intent", required=True)
    parser.add_argument("--known-source", action="append", default=[])
    parser.add_argument("--missing-question", action="append", default=[])
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--receipt-out", type=Path)
    parser.add_argument("--validate-receipt", type=Path)
    parser.add_argument("--escalation-step", choices=["refine_scope", "reuse_hint", "ask_user_hint", "controlled_deep_scan"])
    parser.add_argument("--escalation-attempt", type=int)
    parser.add_argument("--scope-hint")
    parser.add_argument("--known-source-hint")
    parser.add_argument("--escalation-note")
    parser.add_argument("--exhausted", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    query = {
        "task_intent": args.intent,
        "known_sources": args.known_source,
        "missing_questions": args.missing_question,
        "scope": args.root,
    }
    records = _records(root)
    if args.validate_receipt:
        receipt = json.loads(args.validate_receipt.read_text(encoding="utf-8"))
        fingerprints = {item["path"]: item.get("content_fingerprint", "") for item in records}
        print(json.dumps({"receipt_status": receipt_status(receipt, fingerprints, query)}, ensure_ascii=False))
        return 0

    result = navigate(
        args.intent,
        records,
        known_sources=args.known_source,
        missing_questions=args.missing_question,
        top_k=args.top_k,
    )
    result = _apply_escalation(
        result,
        step=args.escalation_step,
        attempt=args.escalation_attempt,
        scope_hint=args.scope_hint,
        known_source_hint=args.known_source_hint,
        note=args.escalation_note,
        exhausted=args.exhausted,
    )
    receipt = build_receipt(query, result)
    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        args.receipt_out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if receipt["status"] not in {"insufficient", "exhausted"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
