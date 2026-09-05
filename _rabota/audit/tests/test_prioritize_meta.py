import json
import tempfile
import unittest
from pathlib import Path

from _rabota.audit.prioritize_meta import build_queue


class PrioritizeMetaTests(unittest.TestCase):
    def make_corpus(self, claims, decisions, candidates, reviews=()):
        temporary = tempfile.TemporaryDirectory()
        base = Path(temporary.name)
        (base / "meta").mkdir()

        files = {
            "claims.jsonl": claims,
            "decisions.jsonl": decisions,
            "meta/candidates.jsonl": candidates,
            "meta/review.jsonl": reviews,
            "sources.jsonl": [],
        }
        for name, rows in files.items():
            (base / name).write_text(
                "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                encoding="utf-8",
            )
        (base / "meta/source_policy.json").write_text(
            json.dumps({"tier_order": ["authoritative", "specialist"]}),
            encoding="utf-8",
        )
        self.addCleanup(temporary.cleanup)
        return base

    @staticmethod
    def claim(claim_id, statement, category="описание", quote="Цитата"):
        return {
            "claim_id": claim_id,
            "block_id": "B0001",
            "location": "Раздел",
            "book_quote": quote,
            "statement": statement,
            "category": category,
            "entity_keys": [],
        }

    @staticmethod
    def decision(claim_id, status="совпадает", consensus="высокий", conclusion="Оставить."):
        return {
            "claim_id": claim_id,
            "status": status,
            "consensus": consensus,
            "comparison": "Сопоставлено.",
            "independence": "Две линии.",
            "missing_definition": None,
            "missing_descriptors": None,
            "editor_conclusion": conclusion,
        }

    @staticmethod
    def candidate(meta_id, key, claim_ids, reasons=(), tiers=("authoritative",)):
        return {
            "meta_id": meta_id,
            "candidate_key": key,
            "kind": "риск решения",
            "claim_ids": claim_ids,
            "original_statuses": [],
            "risk_reasons": list(reasons),
            "source_profile": {"tiers": list(tiers), "sources": []},
        }

    def test_disagreement_cannot_be_demoted_by_strong_source(self):
        base = self.make_corpus(
            [self.claim("C0001", "Нейтральное утверждение")],
            [self.decision("C0001", status="расходится")],
            [self.candidate("M0010", "risk:C0001", ["C0001"])],
        )

        item = build_queue(base)["items"][0]

        self.assertEqual(item["priority"], "P1")
        self.assertIn("decision_status_disagrees", item["reasons"])

    def test_single_number_and_medium_consensus_do_not_force_p1(self):
        base = self.make_corpus(
            [self.claim("C0001", "В регионе 12 хозяйств", category="число")],
            [self.decision("C0001", consensus="средний")],
            [self.candidate("M0001", "risk:C0001", ["C0001"], ["non_high_consensus"])],
        )

        self.assertEqual(build_queue(base)["items"][0]["priority"], "P2")

    def test_unresolved_cultivar_origin_is_p1(self):
        base = self.make_corpus(
            [self.claim("C0001", "Сорт происходит из Сербии", category="происхождение сорта")],
            [self.decision("C0001", status="подтверждено частично")],
            [self.candidate("M0001", "risk:C0001", ["C0001"], ["disputed_status"])],
        )

        item = build_queue(base)["items"][0]
        self.assertEqual(item["priority"], "P1")
        self.assertIn("sensitive_topic_with_evidence_risk", item["reasons"])
        self.assertEqual(item["topic"], "variety identity/origin")

    def test_qualified_sensory_candidate_is_pending_p3(self):
        base = self.make_corpus(
            [self.claim("C0001", "Вино может подойти к рыбе", category="сочетание с едой")],
            [self.decision("C0001", conclusion="Оставить как рекомендацию, с оговоркой о субъективности.")],
            [self.candidate("M0001", "risk:C0001", ["C0001"])],
        )

        item = build_queue(base)["items"][0]
        self.assertEqual((item["priority"], item["state"]), ("P3", "pending"))
        self.assertEqual(item["next_action"], "sample editorial check")

    def test_categorical_sensory_candidate_cannot_be_p3(self):
        base = self.make_corpus(
            [self.claim("C0001", "Это лучшее вино к любой рыбе", category="сочетание с едой")],
            [self.decision("C0001", conclusion="Оставить как рекомендацию, с оговоркой о субъективности.")],
            [self.candidate("M0001", "risk:C0001", ["C0001"], ["categorical_or_superlative"])],
        )

        self.assertEqual(build_queue(base)["items"][0]["priority"], "P2")

    def test_physiology_with_sensory_words_cannot_be_p3(self):
        base = self.make_corpus(
            [self.claim("C0001", "Созревание меняет кислотность и аромат", category="физиология лозы")],
            [self.decision("C0001", conclusion="Оставить с оговоркой: эффект может меняться.")],
            [self.candidate("M0001", "risk:C0001", ["C0001"])],
        )
        self.assertEqual(build_queue(base)["items"][0]["priority"], "P2")

    def test_causal_viticulture_claim_with_taste_word_cannot_be_p3(self):
        base = self.make_corpus(
            [self.claim("C0001", "Рост лозы причинно делает вкус пустым", category="недоказанная причинная цепочка")],
            [self.decision("C0001", conclusion="Допустимо оговорить: может зависеть от участка.")],
            [self.candidate("M0001", "risk:C0001", ["C0001"])],
        )
        self.assertEqual(build_queue(base)["items"][0]["priority"], "P2")

    def test_cultivar_pedigree_stem_is_sensitive(self):
        base = self.make_corpus(
            [self.claim("C0001", "Родословная сорта связана с селекцией и скрещиванием")],
            [self.decision("C0001", status="подтверждено частично")],
            [self.candidate("M0001", "risk:C0001", ["C0001"], ["disputed_status"])],
        )
        self.assertEqual(build_queue(base)["items"][0]["priority"], "P1")

    def test_inflected_registration_stem_is_sensitive(self):
        base = self.make_corpus(
            [self.claim("C0001", "Регистрационная запись вина не найдена")],
            [self.decision("C0001", status="непроверяемо по выбранному корпусу")],
            [self.candidate("M0001", "risk:C0001", ["C0001"], ["disputed_status"])],
        )
        self.assertEqual(build_queue(base)["items"][0]["priority"], "P1")

    def test_only_exact_reviewed_candidate_keys_are_excluded(self):
        claims = [self.claim("C0001", "Аромат ягод")]
        decisions = [self.decision("C0001")]
        candidates = [
            self.candidate("M0010", "risk:C0001:a", ["C0001"]),
            self.candidate("M0002", "risk:C0001:b", ["C0001"]),
        ]
        base = self.make_corpus(
            claims,
            decisions,
            candidates,
            [{"candidate_key": "risk:C0001:a"}],
        )

        result = build_queue(base)

        self.assertEqual([row["candidate_key"] for row in result["items"]], ["risk:C0001:b"])
        self.assertEqual(result["counts"]["pending"], 1)

    def test_output_is_deterministic_and_hash_tracks_input_bytes(self):
        base = self.make_corpus(
            [self.claim("C0001", "Аромат ягод")],
            [self.decision("C0001")],
            [self.candidate("M0010", "risk:C0001", ["C0001"])],
        )
        first = build_queue(base)
        second = build_queue(base)
        self.assertEqual(first, second)
        self.assertEqual(
            set(first["inputs_sha256"]),
            {"claims", "decisions", "candidates", "review", "source_policy", "sources"},
        )

        with (base / "claims.jsonl").open("a", encoding="utf-8") as stream:
            stream.write("\n")
        changed = build_queue(base)

        self.assertNotEqual(first["inputs_sha256"]["claims"], changed["inputs_sha256"]["claims"])
        self.assertEqual(first["items"], changed["items"])

    def test_authored_correction_awaiting_review_remains_actionable(self):
        candidate = self.candidate("M0001", "risk:C0001", ["C0001"])
        base = self.make_corpus(
            [self.claim("C0001", "Название вина")],
            [self.decision("C0001")],
            [candidate],
            [{"candidate_key": "risk:C0001", "validation_status": "self_checked_pending_independent"}],
        )
        result = build_queue(base)
        self.assertEqual(result["counts"]["pending_independent_review"], 1)
        self.assertEqual(result["pending_independent_reviews"][0]["claim_ids"], ["C0001"])
        self.assertEqual(result["pending_independent_reviews"][0]["state"], "pending_independent_review")

    def test_invalid_unknown_claim_fails_instead_of_dropping_candidate(self):
        base = self.make_corpus(
            [self.claim("C0001", "Аромат ягод")],
            [self.decision("C0001")],
            [self.candidate("M0001", "risk:C9999", ["C9999"])],
        )

        with self.assertRaisesRegex(ValueError, "unknown claim C9999"):
            build_queue(base)

    def test_duplicate_candidate_or_review_key_is_rejected(self):
        claim = self.claim("C0001", "Аромат ягод")
        decision = self.decision("C0001")
        candidate = self.candidate("M0001", "risk:C0001", ["C0001"])
        for candidates, reviews, message in (
            ([candidate, candidate], [], "duplicate candidate key"),
            ([candidate], [{"candidate_key": "risk:C0001"}] * 2, "duplicate review key"),
            ([candidate], [{"candidate_key": "missing"}], "unknown review key"),
        ):
            with self.subTest(message=message):
                base = self.make_corpus([claim], [decision], candidates, reviews)
                with self.assertRaisesRegex(ValueError, message):
                    build_queue(base)


if __name__ == "__main__":
    unittest.main()
