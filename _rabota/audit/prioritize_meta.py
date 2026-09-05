#!/usr/bin/env python3
"""Build a deterministic, provisional editorial-risk queue."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


INPUTS = {
    "claims": Path("claims.jsonl"),
    "decisions": Path("decisions.jsonl"),
    "candidates": Path("meta/candidates.jsonl"),
    "review": Path("meta/review.jsonl"),
    "source_policy": Path("meta/source_policy.json"),
    "sources": Path("sources.jsonl"),
}

DISPUTED_STATUSES = {
    "расходится",
    "подтверждено частично",
    "непроверяемо по выбранному корпусу",
    "disputed",
    "partial",
    "unverifiable",
}

SENSITIVE_PATTERNS = (
    (
        "variety identity/origin",
        re.compile(
            r"(?:\b(?:сорт(?:а|ов|у|ом|е)?|культивар(?:а|ов)?|виноград(?:а|ный)?|"
            r"variet(?:y|ies)|cultivar|grape)\b.{0,70}\b(?:происхожд|родств|родител|родослов|селекци|скрещив|"
            r"синоним|идентич|origin|parentage|parent|synonym|identit)|"
            r"\b(?:происхожд|родств|родител|родослов|селекци|скрещив|синоним|идентич|origin|parentage|parent|"
            r"synonym|identit)\w*\b.{0,70}\b(?:сорт|культивар|виноград|variet|cultivar|grape)\w*\b)",
            re.I,
        ),
    ),
    (
        "legal/GI/registry",
        re.compile(
            r"\b(?:правов(?:ой|ая|ое|ые|ого)|закон(?:ный|одательство)?|реестр(?:е|а)?|"
            r"регистрац\w*|географическ\w* указани\w*|наименовани.{0,20}происхожд\w*|"
            r"legal|law|registry|registered|geographical indication|protected designation|GI)\b",
            re.I,
        ),
    ),
    (
        "awards/firsts/records",
        re.compile(
            r"\b(?:наград|медал|перв(?:ый|ая|ое|ые|енств)|рекорд|award|medal|first|record)\w*\b",
            re.I,
        ),
    ),
    (
        "historical causality",
        re.compile(
            r"\b(?:историческ\w*|history|historical)\b.{0,80}\b(?:причин|привел|"
            r"обуслов|вследстви|caus|led to|resulted)\w*\b",
            re.I,
        ),
    ),
    (
        "regional rank/statistics",
        re.compile(
            r"\b(?:регион|стран|област|region|country)\w*\b.{0,80}\b(?:место|ранг|"
            r"площад|посад|производств|rank|planting|production|hectare|тонн)\w*\b",
            re.I,
        ),
    ),
)

SENSORY_PATTERN = re.compile(
    r"\b(?:аромат|вкус|букет|тело|танин|кислот|подач|сервиров|сочетани.{0,15}ед|"
    r"блюд|рыб|мяс|sensory|aroma|flavou?r|taste|serving|food pairing)\w*\b",
    re.I,
)
SENSORY_CATEGORY_PATTERN = re.compile(
    r"\b(?:сенсор|дескриптор|вкусов|гастроном|подач|сервиров|сервис|аэраци|"
    r"сочетани.{0,15}ед|sensory|serving|food pairing)\w*\b", re.I,
)
FACTUAL_CATEGORY_PATTERN = re.compile(
    r"\b(?:физиолог|причин|микроклимат|созрева|управлен|нормирован|рецептур|"
    r"идентич|географ|состав|определени|технолог|агро|селекц|истори|производств|"
    r"physiolog|causal|viticultur|composition|identity|definition)\w*\b", re.I,
)
QUALIFIED_PATTERN = re.compile(
    r"\b(?:оговорк|субъектив|рекомендац|может|обычно|предпочтени|"
    r"qualif|subjective|recommend|may|might|preference)\w*\b",
    re.I,
)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: expected object")
        rows.append(value)
    return rows


def _unique_index(rows: list[dict[str, Any]], field: str, label: str) -> dict[str, dict[str, Any]]:
    result = {}
    for row in rows:
        key = row.get(field)
        if not isinstance(key, str) or not key:
            raise ValueError(f"{label} missing {field}")
        if key in result:
            raise ValueError(f"duplicate {label} key {key}")
        result[key] = row
    return result


def _topic(claims: list[dict[str, Any]]) -> str:
    text = " ".join(
        str(claim.get(field, ""))
        for claim in claims
        for field in ("category", "book_quote", "statement")
    )
    for label, pattern in SENSITIVE_PATTERNS:
        if pattern.search(text):
            return label
    if SENSORY_PATTERN.search(text):
        return "sensory/serving recommendation"
    return "general editorial claim"


def _priority(candidate: dict[str, Any], claims: list[dict[str, Any]], decisions: list[dict[str, Any]]):
    signals = set(candidate.get("risk_reasons", []))
    statuses = {decision.get("status") for decision in decisions}
    topic = _topic(claims)

    if "расходится" in statuses:
        return "P1", ["decision_status_disagrees"], topic
    conflicts = signals & {"wikipedia_disagreement", "duplicate_decision_variance", "duplicate_decision_conflict"}
    if conflicts:
        return "P1", [f"explicit_{name}" for name in sorted(conflicts)], topic

    evidence_risk = bool(statuses & DISPUTED_STATUSES)
    evidence_risk = evidence_risk or (
        any(decision.get("consensus") == "высокий" for decision in decisions)
        and "high_consensus_without_strong_source" in signals
    )
    if topic in {label for label, _ in SENSITIVE_PATTERNS} and evidence_risk:
        return "P1", ["sensitive_topic_with_evidence_risk"], topic

    high_risk_signal = bool(signals & {"categorical_or_superlative", "high_risk_fact_type"})
    explicitly_sensory = all(
        SENSORY_CATEGORY_PATTERN.search(str(claim.get("category", "")))
        and not FACTUAL_CATEGORY_PATTERN.search(str(claim.get("category", "")))
        for claim in claims
    )
    all_qualified = all(
        QUALIFIED_PATTERN.search(str(decision.get("editor_conclusion", "")))
        for decision in decisions
    )
    if topic == "sensory/serving recommendation" and explicitly_sensory and all_qualified and not high_risk_signal:
        return "P3", ["qualified_sensory_recommendation"], topic

    return "P2", ["editorial_evidence_check"], topic


def _meta_number(meta_id: str) -> int:
    match = re.fullmatch(r"M(\d+)", meta_id)
    if not match:
        raise ValueError(f"invalid meta_id {meta_id}")
    return int(match.group(1))


def build_queue(base_dir: Path) -> dict[str, Any]:
    """Return every unreviewed frozen candidate in a provisional priority queue."""
    base_dir = Path(base_dir)
    paths = {name: base_dir / relative for name, relative in INPUTS.items()}
    hashes = {
        name: hashlib.sha256(path.read_bytes()).hexdigest()
        for name, path in paths.items()
    }

    claims = _unique_index(_load_jsonl(paths["claims"]), "claim_id", "claim")
    decisions = _unique_index(_load_jsonl(paths["decisions"]), "claim_id", "decision")
    candidate_rows = _load_jsonl(paths["candidates"])
    candidates = _unique_index(candidate_rows, "candidate_key", "candidate")
    review_rows = _load_jsonl(paths["review"])
    reviews = _unique_index(review_rows, "candidate_key", "review")

    unknown_reviews = sorted(set(reviews) - set(candidates))
    if unknown_reviews:
        raise ValueError(f"unknown review key {unknown_reviews[0]}")

    items = []
    pending_independent_reviews = []
    for key, candidate in candidates.items():
        claim_ids = candidate.get("claim_ids")
        if not isinstance(claim_ids, list) or not claim_ids:
            raise ValueError(f"candidate {key} has no claim_ids")
        for claim_id in claim_ids:
            if claim_id not in claims:
                raise ValueError(f"candidate {key} references unknown claim {claim_id}")
            if claim_id not in decisions:
                raise ValueError(f"candidate {key} references unknown decision {claim_id}")
        meta_id = candidate.get("meta_id")
        if not isinstance(meta_id, str):
            raise ValueError(f"candidate {key} missing meta_id")
        _meta_number(meta_id)
        if key in reviews:
            if reviews[key].get("validation_status") == "self_checked_pending_independent":
                pending_independent_reviews.append({
                    "candidate_key": key,
                    "meta_id": meta_id,
                    "claim_ids": list(claim_ids),
                    "state": "pending_independent_review",
                    "next_action": "independent check of changed editorial advice",
                })
            continue
        linked_claims = [claims[claim_id] for claim_id in claim_ids]
        linked_decisions = [decisions[claim_id] for claim_id in claim_ids]
        priority, reasons, topic = _priority(candidate, linked_claims, linked_decisions)
        next_action = {
            "P1": "substantive editorial review",
            "P2": "evidence sufficiency check",
            "P3": "sample editorial check",
        }[priority]
        items.append(
            {
                "candidate_key": key,
                "meta_id": meta_id,
                "claim_ids": list(claim_ids),
                "priority": priority,
                "reasons": reasons,
                "topic": topic,
                "state": "pending",
                "next_action": next_action,
            }
        )

    priority_order = {"P1": 1, "P2": 2, "P3": 3}
    items.sort(key=lambda item: (priority_order[item["priority"]], _meta_number(item["meta_id"]), item["candidate_key"]))
    pending_independent_reviews.sort(key=lambda item: _meta_number(item["meta_id"]))
    counts = {
        "candidates": len(candidates),
        "reviewed": len(reviews),
        "pending": len(items),
        "pending_independent_review": len(pending_independent_reviews),
        "P1": sum(item["priority"] == "P1" for item in items),
        "P2": sum(item["priority"] == "P2" for item in items),
        "P3": sum(item["priority"] == "P3" for item in items),
    }
    if counts["reviewed"] + counts["pending"] != counts["candidates"]:
        raise AssertionError("candidate accounting mismatch")
    return {
        "schema_version": 1, "inputs_sha256": hashes, "counts": counts,
        "pending_independent_reviews": pending_independent_reviews, "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_queue(args.base_dir)
    if args.output:
        args.output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result["counts"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
