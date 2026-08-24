from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


WIKIPEDIA_LANGUAGES = ("en", "de", "hu", "sr", "ru", "hr")
CLAIM_STATUSES = {
    "совпадает",
    "совпадает с уточнением",
    "подтверждено частично",
    "расходится",
    "между Википедиями нет согласия",
    "в Википедиях отсутствует",
    "непроверяемо по выбранному корпусу",
}
CONSENSUS_LEVELS = {"высокий", "средний", "низкий", "отсутствует", "конфликт"}
COVERAGE_CLASSES = {"navigation", "pure_recommendation", "non_factual_copy"}
ABSENCE_STATUSES = {
    "точно отсутствует",
    "присутствует только косвенно",
    "возможное совпадение под другим названием",
    "источниковая запись сомнительна или устарела",
    "вне заявленного охвата книги",
}


def _read_jsonl(path: Path, errors: list[str]) -> list[dict]:
    if not path.exists():
        errors.append(f"missing file {path.name}")
        return []

    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"{path.name}:{line_number}: invalid JSON: {error.msg}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path.name}:{line_number}: record must be an object")
            continue
        records.append(value)
    return records


def _check_contiguous_ids(
    records: list[dict], field: str, prefix: str, width: int, label: str, errors: list[str]
) -> None:
    seen = set()
    for index, record in enumerate(records, start=1):
        actual = record.get(field)
        expected = f"{prefix}{index:0{width}d}"
        if actual != expected:
            errors.append(f"{label} IDs must be contiguous: expected {expected}, got {actual}")
        if actual in seen:
            errors.append(f"duplicate {label} ID {actual}")
        seen.add(actual)


def _require(record: dict, fields: tuple[str, ...], label: str, errors: list[str]) -> None:
    for field in fields:
        if field not in record or record[field] == "" or record[field] == []:
            errors.append(f"{label} has empty {field}")


def _check_date(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{label} has invalid accessed date {value}")
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label} has invalid accessed date {value}")


def _check_url(value: object, label: str, *, allow_none: bool, errors: list[str]) -> None:
    if value is None and allow_none:
        return
    if not isinstance(value, str) or not value.startswith("https://"):
        errors.append(f"{label} has invalid HTTPS URL {value}")


def validate_all(
    base_dir: Path,
    *,
    mode: str = "full",
    through_block: str | None = None,
) -> list[str]:
    if mode not in {"manifest", "sources", "full"}:
        raise ValueError(f"unsupported validation mode {mode}")

    errors: list[str] = []
    manifest = _read_jsonl(base_dir / "manifest.jsonl", errors)
    claims = _read_jsonl(base_dir / "claims.jsonl", errors)
    coverage = _read_jsonl(base_dir / "coverage.jsonl", errors)
    sources = _read_jsonl(base_dir / "sources.jsonl", errors) if mode in {"sources", "full"} else []
    decisions = _read_jsonl(base_dir / "decisions.jsonl", errors) if mode == "full" else []
    gaps = _read_jsonl(base_dir / "gaps.jsonl", errors) if mode == "full" else []

    _check_contiguous_ids(manifest, "block_id", "B", 4, "block", errors)
    _check_contiguous_ids(claims, "claim_id", "C", 4, "claim", errors)
    if mode in {"sources", "full"}:
        _check_contiguous_ids(sources, "source_id", "E", 6, "source", errors)
    if mode == "full":
        _check_contiguous_ids(gaps, "gap_id", "G", 4, "gap", errors)

    block_ids = {record.get("block_id") for record in manifest}
    claim_ids = {record.get("claim_id") for record in claims}
    checked_block_ids = set(block_ids)
    if through_block is not None:
        if through_block not in block_ids:
            errors.append(f"through block {through_block} does not exist")
            checked_block_ids = set()
        else:
            limit = int(through_block[1:])
            checked_block_ids = {
                block_id
                for block_id in block_ids
                if isinstance(block_id, str) and int(block_id[1:]) <= limit
            }

    claims_by_block: defaultdict[str, list[str]] = defaultdict(list)
    for claim in claims:
        label = str(claim.get("claim_id"))
        _require(
            claim,
            ("claim_id", "block_id", "location", "book_quote", "statement", "category", "entity_keys"),
            label,
            errors,
        )
        block_id = claim.get("block_id")
        if block_id not in block_ids:
            errors.append(f"{label} references missing block {block_id}")
        else:
            claims_by_block[str(block_id)].append(label)

    checked_claim_ids = {
        str(claim.get("claim_id"))
        for claim in claims
        if claim.get("claim_id") is not None and claim.get("block_id") in checked_block_ids
    }

    coverage_by_block = Counter()
    for record in coverage:
        block_id = record.get("block_id")
        _require(record, ("block_id", "classification", "rationale"), f"coverage {block_id}", errors)
        coverage_by_block[block_id] += 1
        if block_id not in block_ids:
            errors.append(f"coverage references missing block {block_id}")
        if record.get("classification") not in COVERAGE_CLASSES:
            errors.append(f"coverage {block_id} has invalid classification {record.get('classification')}")

    for block_id in checked_block_ids:
        if block_id is None:
            continue
        has_claim = bool(claims_by_block.get(str(block_id)))
        coverage_count = coverage_by_block[block_id]
        if not has_claim and coverage_count == 0:
            errors.append(f"{block_id} has neither claims nor no-fact coverage")
        if has_claim and coverage_count:
            errors.append(f"{block_id} has both claims and no-fact coverage")
        if coverage_count > 1:
            errors.append(f"{block_id} has duplicate no-fact coverage")

    wikipedia_results: defaultdict[str, set[str]] = defaultdict(set)
    for source in sources:
        source_id = str(source.get("source_id"))
        _require(
            source,
            (
                "source_id",
                "claim_ids",
                "resource",
                "language",
                "title",
                "accessed",
                "access_level",
                "provenance",
                "summary",
                "relation",
                "notes",
            ),
            source_id,
            errors,
        )
        _check_date(source.get("accessed"), source_id, errors)
        allow_none = source.get("relation") == "no_relevant_material"
        _check_url(source.get("url"), source_id, allow_none=allow_none, errors=errors)
        for claim_id in source.get("claim_ids", []):
            if claim_id not in claim_ids:
                errors.append(f"{source_id} references missing claim {claim_id}")
                continue
            if source.get("resource") == "wikipedia" and source.get("language") in WIKIPEDIA_LANGUAGES:
                wikipedia_results[str(claim_id)].add(str(source["language"]))

    decisions_by_claim: defaultdict[str, list[dict]] = defaultdict(list)
    for decision in decisions:
        claim_id = decision.get("claim_id")
        label = f"decision {claim_id}"
        _require(
            decision,
            ("claim_id", "status", "consensus", "comparison", "independence", "editor_conclusion"),
            label,
            errors,
        )
        if claim_id not in claim_ids:
            errors.append(f"{label} references missing claim")
        decisions_by_claim[str(claim_id)].append(decision)
        if decision.get("status") not in CLAIM_STATUSES:
            errors.append(f"{label} has invalid status {decision.get('status')}")
        if decision.get("consensus") not in CONSENSUS_LEVELS:
            errors.append(f"{label} has invalid consensus {decision.get('consensus')}")

    for claim_id in checked_claim_ids:
        if mode in {"sources", "full"}:
            for language in WIKIPEDIA_LANGUAGES:
                if language not in wikipedia_results[claim_id]:
                    errors.append(f"{claim_id} has no Wikipedia result for {language}")
        if mode == "full":
            decision_count = len(decisions_by_claim[claim_id])
            if decision_count == 0:
                errors.append(f"{claim_id} has no decision")
            elif decision_count > 1:
                errors.append(f"{claim_id} has multiple decisions")

    for gap in gaps:
        gap_id = str(gap.get("gap_id"))
        _require(
            gap,
            (
                "gap_id",
                "object_type",
                "canonical_name",
                "aliases",
                "region",
                "producer",
                "resource",
                "url",
                "accessed",
                "access_level",
                "summary",
                "book_search",
                "absence_status",
                "reliability",
                "significance",
            ),
            gap_id,
            errors,
        )
        _check_date(gap.get("accessed"), gap_id, errors)
        _check_url(gap.get("url"), gap_id, allow_none=False, errors=errors)
        if gap.get("absence_status") not in ABSENCE_STATUSES:
            errors.append(f"{gap_id} has invalid absence_status {gap.get('absence_status')}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the multilingual book audit")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--manifest-only", action="store_true")
    group.add_argument("--sources", action="store_true")
    parser.add_argument("--through", dest="through_block")
    parser.add_argument("base_dir", type=Path)
    arguments = parser.parse_args(argv)

    mode = "manifest" if arguments.manifest_only else "sources" if arguments.sources else "full"
    errors = validate_all(
        arguments.base_dir,
        mode=mode,
        through_block=arguments.through_block,
    )
    if errors:
        for error in errors:
            print(error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
