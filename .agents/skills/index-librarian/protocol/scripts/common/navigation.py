"""Task navigation and receipt validation over adjacent INDEX.md records."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any


_WORDS = re.compile(r"[A-Za-z][A-Za-z0-9_-]{1,}|[\u4e00-\u9fff]{2,}")
_REFERENCE_PATH_FRAGMENT = "/references/"
_ARCHIVE_PATH_FRAGMENT = "/90_archive/"


def _terms(value: str) -> set[str]:
    terms: set[str] = set()
    for item in _WORDS.findall(value):
        terms.add(item.lower())
        if re.fullmatch(r"[\u4e00-\u9fff]+", item):
            terms.update(item[index:index + 2] for index in range(len(item) - 1))
    return terms


def _fingerprint(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _merge_unique(existing: list[str], incoming: list[str]) -> list[str]:
    merged = list(existing)
    seen = set(existing)
    for item in incoming:
        if item not in seen:
            merged.append(item)
            seen.add(item)
    return merged


def _path_penalty(path: str) -> tuple[int, str | None]:
    if _REFERENCE_PATH_FRAGMENT in f"/{path}":
        return 4, "路径降权：references 流程文档"
    if _ARCHIVE_PATH_FRAGMENT in f"/{path}":
        return 3, "路径降权：archive 历史设计"
    return 0, None


def navigate(
    task_intent: str,
    records: list[dict[str, Any]],
    *,
    known_sources: list[str] | None = None,
    missing_questions: list[str] | None = None,
    top_k: int = 5,
) -> dict[str, Any]:
    """Return explainable, bounded candidates or an explicit insufficient result."""
    known_sources = known_sources or []
    missing_questions = missing_questions or []
    if known_sources and not missing_questions:
        return {"status": "not_needed", "candidates": [], "missing_categories": []}

    query_terms = _terms(" ".join([task_intent, *missing_questions]))
    candidates_by_path: dict[str, dict[str, Any]] = {}
    for record in records:
        if record.get("parse_status") != "indexed":
            continue
        fields = {
            "path": _terms(str(record.get("path", ""))),
            "summary": _terms(str(record.get("summary", ""))),
            "topics": set().union(*(_terms(str(value)) for value in record.get("topics", []))) if record.get("topics") else set(),
            "answers": set().union(*(_terms(str(value)) for value in record.get("answers", []))) if record.get("answers") else set(),
        }
        reasons = []
        score = 0
        for name, weight, label in (("topics", 4, "主题"), ("answers", 3, "适用问题"), ("summary", 2, "摘要"), ("path", 1, "路径")):
            matched = sorted(query_terms & fields[name])
            if matched:
                score += weight * len(matched)
                reasons.append(f"{label}匹配：{', '.join(matched)}")
        if score:
            candidate = dict(record)
            penalty, penalty_reason = _path_penalty(candidate["path"])
            adjusted_score = max(1, score - penalty)
            candidate["score"] = score
            candidate["adjusted_score"] = adjusted_score
            candidate["reasons"] = reasons
            if penalty_reason:
                candidate["reasons"].append(penalty_reason)
            candidate["confidence"] = "high" if score >= 8 else "moderate"
            path = candidate["path"]
            existing = candidates_by_path.get(path)
            if not existing:
                candidates_by_path[path] = candidate
                continue
            if candidate["adjusted_score"] > existing["adjusted_score"]:
                candidate["reasons"] = _merge_unique(candidate["reasons"], existing.get("reasons", []))
                candidate["evidence"] = _merge_unique(candidate.get("evidence", []), existing.get("evidence", []))
                candidates_by_path[path] = candidate
            else:
                existing["reasons"] = _merge_unique(existing.get("reasons", []), candidate["reasons"])
                existing["evidence"] = _merge_unique(existing.get("evidence", []), candidate.get("evidence", []))
                if existing["adjusted_score"] == candidate["adjusted_score"]:
                    existing["answers"] = _merge_unique(existing.get("answers", []), candidate.get("answers", []))
                    existing["topics"] = _merge_unique(existing.get("topics", []), candidate.get("topics", []))
    candidates = list(candidates_by_path.values())
    candidates.sort(key=lambda item: (-item["adjusted_score"], -item["score"], item["path"]))
    if not candidates:
        return {
            "status": "insufficient",
            "candidates": [],
            "missing_categories": ["relevant_authoritative_source"],
        }
    selected = candidates[:max(1, top_k)]
    selected_paths = {candidate["path"] for candidate in selected}
    for route in [candidate for candidate in selected if candidate.get("navigation_role") == "route"]:
        descendant = next(
            (
                candidate for candidate in candidates
                if candidate["path"].startswith(route["path"])
                and candidate["path"] != route["path"]
                and candidate["path"] not in selected_paths
            ),
            None,
        )
        if descendant:
            descendant = dict(descendant)
            descendant["via_route"] = route["path"]
            selected.append(descendant)
            selected_paths.add(descendant["path"])
        else:
            route["requires_drilldown"] = True
    return {"status": "queried", "candidates": selected, "missing_categories": []}


def build_receipt(query: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Create a portable receipt; it contains facts, not a success declaration."""
    selected = result.get("candidates", [])
    sources = {item["path"]: item.get("content_fingerprint", "") for item in selected}
    events = [{"event_type": "navigation_decision_made", "status": result["status"]}]
    if result["status"] == "queried":
        events.extend([
            {"event_type": "navigation_query_executed"},
            {"event_type": "navigation_candidates_returned", "candidate_count": len(selected)},
        ])
        events.extend({"event_type": "navigation_source_selected", "path": item["path"]} for item in selected)
    elif result["status"] == "insufficient":
        events.append({"event_type": "navigation_gate_denied", "missing_categories": result.get("missing_categories", [])})
    elif result["status"] in {"escalated", "exhausted"}:
        escalation = dict(result.get("escalation", {}))
        if result["status"] == "escalated":
            events.append({"event_type": "navigation_escalated", **escalation})
        else:
            events.append({
                "event_type": "navigation_escalation_exhausted",
                "missing_categories": result.get("missing_categories", []),
                **escalation,
            })
    return {
        "schema_version": 1,
        "status": result["status"],
        "task_fingerprint": _fingerprint(query),
        "query": query,
        "sources": sources,
        "candidates": selected,
        "missing_categories": result.get("missing_categories", []),
        "escalation": result.get("escalation"),
        "events": events,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def receipt_status(receipt: dict[str, Any], source_fingerprints: dict[str, str], query: dict[str, Any]) -> str:
    """Return valid or stale without claiming that a task was successful."""
    if receipt.get("task_fingerprint") != _fingerprint(query):
        return "stale"
    for path, fingerprint in receipt.get("sources", {}).items():
        if source_fingerprints.get(path) != fingerprint:
            return "stale"
    return "valid"
