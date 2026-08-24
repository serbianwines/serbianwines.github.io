import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from _rabota.audit.validate_audit import main, validate_all


LANGUAGES = ("en", "de", "hu", "sr", "ru", "hr")


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def _valid_records() -> dict[str, list[dict]]:
    manifest = [
        {"block_id": "B0001", "order": 1, "text": "Факт один."},
        {"block_id": "B0002", "order": 2, "text": "Факт два."},
    ]
    claims = [
        {
            "claim_id": "C0001",
            "block_id": "B0001",
            "location": "Карта",
            "book_quote": "Факт один.",
            "statement": "Первое утверждение",
            "category": "география",
            "entity_keys": ["entity-one"],
        },
        {
            "claim_id": "C0002",
            "block_id": "B0002",
            "location": "Карта",
            "book_quote": "Факт два.",
            "statement": "Второе утверждение",
            "category": "история",
            "entity_keys": ["entity-two"],
        },
    ]
    sources = [
        {
            "source_id": f"E{index:06d}",
            "claim_ids": ["C0001", "C0002"],
            "resource": "wikipedia",
            "language": language,
            "title": "Подходящий материал не найден",
            "url": None,
            "accessed": "2026-08-15",
            "access_level": "public",
            "provenance": f"wikipedia-{language}-search",
            "summary": "В выбранной языковой версии релевантное утверждение не найдено.",
            "relation": "no_relevant_material",
            "notes": "Проверены название сущности и известный синоним.",
        }
        for index, language in enumerate(LANGUAGES, start=1)
    ]
    decisions = [
        {
            "claim_id": claim_id,
            "status": "в Википедиях отсутствует",
            "consensus": "отсутствует",
            "comparison": "Шесть Википедий не дают релевантного материала.",
            "independence": "Независимые подтверждающие линии отсутствуют.",
            "missing_definition": None,
            "missing_descriptors": None,
            "editor_conclusion": "Оставить для проверки по профильным источникам.",
        }
        for claim_id in ("C0001", "C0002")
    ]
    gaps = [
        {
            "gap_id": "G0001",
            "object_type": "винодельня",
            "canonical_name": "Primer Winery",
            "aliases": ["Primer"],
            "region": "Сербия",
            "producer": "Primer Winery",
            "resource": "wein.plus",
            "url": "https://example.com/primer",
            "accessed": "2026-08-15",
            "access_level": "public",
            "summary": "В источнике есть карточка производителя.",
            "book_search": "Название и вариант Primer в манифесте не найдены.",
            "absence_status": "точно отсутствует",
            "reliability": "средняя",
            "significance": "Кандидат для редакторского разбора.",
            "concerns": None,
        }
    ]
    return {
        "manifest.jsonl": manifest,
        "claims.jsonl": claims,
        "coverage.jsonl": [],
        "sources.jsonl": sources,
        "decisions.jsonl": decisions,
        "gaps.jsonl": gaps,
    }


class ValidateAuditTests(unittest.TestCase):
    def _validate(
        self,
        records: dict[str, list[dict]],
        mode: str = "full",
        through_block: str | None = None,
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for filename, rows in records.items():
                _write_jsonl(base / filename, rows)
            return validate_all(base, mode=mode, through_block=through_block)

    def test_accepts_complete_minimal_audit(self):
        self.assertEqual(self._validate(_valid_records()), [])

    def test_rejects_non_contiguous_claim_ids(self):
        records = _valid_records()
        records["claims.jsonl"][1]["claim_id"] = "C0003"

        errors = self._validate(records)

        self.assertIn("claim IDs must be contiguous: expected C0002, got C0003", errors)

    def test_rejects_claim_link_to_missing_manifest_block(self):
        records = _valid_records()
        records["claims.jsonl"][0]["block_id"] = "B9999"

        errors = self._validate(records)

        self.assertIn("C0001 references missing block B9999", errors)

    def test_requires_explicit_result_for_all_six_wikipedias(self):
        records = _valid_records()
        records["sources.jsonl"] = [
            row for row in records["sources.jsonl"] if row["language"] != "hr"
        ]

        errors = self._validate(records)

        self.assertIn("C0001 has no Wikipedia result for hr", errors)
        self.assertIn("C0002 has no Wikipedia result for hr", errors)

    def test_rejects_empty_required_decision_field(self):
        records = deepcopy(_valid_records())
        records["decisions.jsonl"][0]["editor_conclusion"] = ""

        errors = self._validate(records)

        self.assertIn("decision C0001 has empty editor_conclusion", errors)

    def test_manifest_mode_ignores_unfinished_sources_and_decisions(self):
        records = _valid_records()
        records["sources.jsonl"] = []
        records["decisions.jsonl"] = []
        records["gaps.jsonl"] = []

        self.assertEqual(self._validate(records, mode="manifest"), [])

    def test_command_line_manifest_mode_returns_success(self):
        records = _valid_records()
        records["sources.jsonl"] = []
        records["decisions.jsonl"] = []
        records["gaps.jsonl"] = []

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for filename, rows in records.items():
                _write_jsonl(base / filename, rows)
            exit_code = main(["--manifest-only", str(base)])

        self.assertEqual(exit_code, 0)

    def test_manifest_mode_can_validate_only_a_completed_prefix(self):
        records = _valid_records()
        records["manifest.jsonl"].append(
            {"block_id": "B0003", "order": 3, "text": "Еще не обработан."}
        )
        records["sources.jsonl"] = []
        records["decisions.jsonl"] = []
        records["gaps.jsonl"] = []

        self.assertEqual(self._validate(records, mode="manifest", through_block="B0002"), [])

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for filename, rows in records.items():
                _write_jsonl(base / filename, rows)
            exit_code = main(["--manifest-only", "--through", "B0002", str(base)])

        self.assertEqual(exit_code, 0)

    def test_sources_mode_can_validate_only_a_completed_prefix(self):
        records = _valid_records()
        records["sources.jsonl"] = [
            row
            for row in records["sources.jsonl"]
            if "C0001" in row["claim_ids"]
        ]
        for row in records["sources.jsonl"]:
            row["claim_ids"] = ["C0001"]

        self.assertEqual(
            self._validate(records, mode="sources", through_block="B0001"),
            [],
        )


if __name__ == "__main__":
    unittest.main()
