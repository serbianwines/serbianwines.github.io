import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import _rabota.audit.meta_audit as meta_audit

from _rabota.audit.meta_audit import (
    build_source_profiles,
    classify_source,
    duplicate_candidates,
    fact_signature,
    load_jsonl,
    load_source_policy,
    normalize_keys,
    risk_reasons,
    scan_audit,
    source_lineage_key,
)


POLICY_PATH = Path(__file__).resolve().parents[1] / "meta" / "source_policy.json"


class SourcePolicyTests(unittest.TestCase):
    def test_load_jsonl_preserves_utf8_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            path.write_text(
                json.dumps({"title": "Прокупац"}, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            self.assertEqual(load_jsonl(path), [{"title": "Прокупац"}])

    def test_peer_reviewed_source_is_authoritative(self):
        source = {
            "resource": "peer_reviewed_genetics",
            "relation": "direct_identity_evidence",
            "provenance": "journal article",
            "url": "https://doi.org/10.1/example",
            "title": "Genetics",
            "summary": "Direct result",
        }

        result = classify_source(source, load_source_policy(POLICY_PATH))

        self.assertEqual(result["tier"], "authoritative")
        self.assertEqual(result["independence"], "editorially_independent")
        self.assertFalse(result["needs_policy_review"])

    def test_unreviewed_university_extension_is_specialist(self):
        source = {
            "resource": "university_extension",
            "relation": "viticulture_guidance",
            "provenance": "extension factsheet",
            "url": "https://extension.example/grapes",
            "title": "Grape guide",
            "summary": "Viticulture guidance",
        }

        result = classify_source(source, load_source_policy(POLICY_PATH))

        self.assertEqual(result["tier"], "specialist")
        self.assertEqual(result["competence"], "role_unspecified")

    def test_official_austrian_wine_body_is_authoritative(self):
        source = {
            "resource": "official_austrian_wine_body",
            "relation": "primary_current_protection_origin_and_sweet_style_evidence",
            "provenance": "Official Austrian Wine Marketing Board regional and legal-category guide",
            "url": "https://www.austrianwine.com/our-wine/winegrowing-regions/burgenland/leithaberg-incl-rust",
            "title": "Austrian Wine — Leithaberg including Ruster Ausbruch DAC",
            "summary": "Ruster Ausbruch DAC is a protected Rust-origin wine.",
        }

        result = classify_source(source, load_source_policy(POLICY_PATH))

        self.assertEqual(result["tier"], "authoritative")
        self.assertFalse(result["needs_policy_review"])

    def test_official_austrian_wine_body_archive_requires_policy_review(self):
        source = {
            "resource": "official_austrian_wine_body_archive",
            "relation": "primary_current_protection_origin_and_sweet_style_evidence",
            "provenance": "Archived Austrian Wine Marketing Board snapshot",
            "url": "https://archive.example/austrian-wine",
            "title": "Archived Austrian Wine regional guide",
            "summary": "Archive copy of regional material.",
        }

        result = classify_source(source, load_source_policy(POLICY_PATH))

        self.assertEqual(result["tier"], "weak")
        self.assertEqual(result["independence"], "unknown")
        self.assertTrue(result["needs_policy_review"])

    def test_producer_first_claim_is_interested_only(self):
        source = {
            "resource": "official_producer",
            "relation": "producer_first_claim",
            "provenance": "producer website",
            "url": "https://producer.example/history",
            "title": "Our history",
            "summary": "We were first",
        }

        result = classify_source(source, load_source_policy(POLICY_PATH))

        self.assertEqual(result["tier"], "limited")
        self.assertEqual(result["independence"], "interested_primary")
        self.assertEqual(result["competence"], "interested_only")

    def test_producer_product_composition_is_within_primary_scope(self):
        source = {
            "resource": "official_producer",
            "relation": "producer_composition",
            "provenance": "producer technical sheet",
            "url": "https://producer.example/wine",
            "title": "Wine technical sheet",
            "summary": "The blend is 80/20",
        }

        result = classify_source(source, load_source_policy(POLICY_PATH))

        self.assertEqual(result["tier"], "limited")
        self.assertEqual(result["competence"], "within_scope_primary")

    def test_unknown_resource_requires_policy_review(self):
        source = {
            "resource": "uncatalogued_source_kind",
            "relation": "supports",
            "provenance": "unknown",
            "url": "https://unknown.example/item",
            "title": "Item",
            "summary": "Claim",
        }

        result = classify_source(source, load_source_policy(POLICY_PATH))

        self.assertEqual(result["tier"], "weak")
        self.assertEqual(result["independence"], "unknown")
        self.assertTrue(result["needs_policy_review"])

    def test_load_source_policy_rejects_invalid_exact_tier_override(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source_policy.json"
            policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
            policy["exact_tier_overrides"] = {
                "official_austrian_wine_body": "Authoritative"
            }
            path.write_text(json.dumps(policy), encoding="utf-8")

            with self.assertRaisesRegex(
                ValueError, "exact_tier_overrides\\['official_austrian_wine_body'\\]"
            ):
                load_source_policy(path)

    def test_classifies_common_audit_resource_roles(self):
        expected_tiers = {
            "academic_article": "authoritative",
            "competition_primary": "authoritative",
            "fao_soil_reference": "authoritative",
            "official_regional_specification": "authoritative",
            "national_wine_portal": "specialist",
            "wine_media": "specialist",
            "public_broadcaster": "specialist",
            "wine_product_description": "limited",
            "news_report": "weak",
            "wine_database": "specialist",
            "specialist_press": "specialist",
            "wine_dictionary": "specialist",
            "competition_organiser_platinum_list": "authoritative",
            "international_soil_standard": "authoritative",
            "national_encyclopedia": "specialist",
            "historical_viticulture_manual": "authoritative",
            "current_specialist_tasting_guide": "specialist",
            "expert_interview": "specialist",
            "competition_database": "authoritative",
            "regional_wine_route": "limited",
            "wine_encyclopedia": "specialist",
            "research_paper": "authoritative",
            "unesco_tentative_list": "authoritative",
            "official_hungarian_wine_portal": "specialist",
            "national_vine_variety_catalogue": "authoritative",
            "wine_competition_result": "authoritative",
            "international_grapevine_catalogue": "authoritative",
            "wine_monograph": "specialist",
            "official_viticulture_publication": "authoritative",
            "regional_wine_guide": "specialist",
            "business_press": "weak",
            "official_museum": "authoritative",
            "wine_competition": "specialist",
            "independent_wine_review": "specialist",
            "language_dictionary": "specialist",
            "specialist_grape_reference": "specialist",
            "official_agricultural_annual_report": "authoritative",
            "current_winery_product_page": "limited",
            "official_champagne_method": "authoritative",
            "ives_open_science": "authoritative",
            "agricultural_media": "specialist",
            "regional_press": "weak",
            "national_newspaper": "weak",
            "protected_origin_association": "authoritative",
            "usgs_hydrology": "authoritative",
            "national_grape_catalogue": "authoritative",
            "international_oenological_standard": "authoritative",
            "iso": "authoritative",
            "ancient_source": "specialist",
            "industry_interview": "limited",
            "geographic_summary": "weak",
            "specialist_review": "specialist",
            "official_viticulture_monograph": "authoritative",
            "official_agriculture_report": "authoritative",
            "serbian_wine_industry_profile": "specialist",
            "official_appellation_consortium": "authoritative",
            "book_snapshot": "weak",
            "serbian_ministry_of_agriculture": "authoritative",
            "government": "authoritative",
            "official_wine_region": "specialist",
            "professional_media": "specialist",
            "official_inventory": "authoritative",
            "professional_association": "specialist",
            "official_product_page": "limited",
            "sensory_science": "specialist",
            "official_winery": "limited",
            "historical_wine_handbook": "specialist",
            "wine_education": "specialist",
            "variety_database": "authoritative",
            "national_press": "weak",
            "scholarly_historical_gis": "authoritative",
            "international_standard": "authoritative",
            "government_guidance": "authoritative",
            "national_wine_guide": "specialist",
            "market_search": "weak",
            "serbian_wine_catalogue": "limited",
            "regional_news": "weak",
            "national_viticulture_sector_study": "authoritative",
            "official_government_report": "authoritative",
            "climate_reference": "specialist",
            "soil_classification_reference": "authoritative",
            "noaa": "authoritative",
            "wine_industry_best_practice": "specialist",
            "competition_official_results": "authoritative",
            "competition_editorial": "specialist",
            "chamber_of_commerce_release_republication": "weak",
            "current_winery_first_party_site": "limited",
            "business_journalism": "weak",
            "national_library_bibliography": "authoritative",
            "frontiers_in_plant_science": "authoritative",
            "scientific_database": "authoritative",
            "library_catalog": "authoritative",
        }
        policy = load_source_policy(POLICY_PATH)

        for resource, expected_tier in expected_tiers.items():
            with self.subTest(resource=resource):
                source = {
                    "resource": resource,
                    "relation": "supports",
                    "provenance": resource,
                    "url": f"https://example.org/{resource}",
                    "title": resource,
                    "summary": "Evidence",
                }

                result = classify_source(source, policy)

                self.assertEqual(result["tier"], expected_tier)
                self.assertFalse(result["needs_policy_review"])

    def test_declared_translation_shares_parent_lineage(self):
        original = {
            "url": "https://example.org/report",
            "title": "Official report",
            "provenance": "original report",
            "summary": "same evidence",
        }
        translation = {
            "url": "https://mirror.example/translation",
            "title": "Official report translated",
            "provenance": "translation of https://example.org/report",
            "summary": "same evidence",
        }

        self.assertEqual(source_lineage_key(original), source_lineage_key(translation))

    def test_declared_wikipedia_translation_shares_language_lineage(self):
        original = {
            "resource": "wikipedia",
            "language": "en",
            "url": "https://en.wikipedia.org/wiki/Terroir",
            "title": "Terroir",
            "provenance": "wikipedia-en; broad synthesis",
            "summary": "English summary",
        }
        translation = {
            "resource": "wikipedia",
            "language": "hu",
            "url": "https://hu.wikipedia.org/wiki/Terroir",
            "title": "Terroir",
            "provenance": "wikipedia-hu; article explicitly states partial translation from wikipedia-en",
            "summary": "Hungarian summary",
        }

        self.assertEqual(source_lineage_key(original), source_lineage_key(translation))

    def test_source_profiles_do_not_count_translation_as_independent(self):
        sources = [
            {
                "source_id": "E000001",
                "claim_ids": ["C0001"],
                "resource": "official_register",
                "relation": "supports",
                "provenance": "original report",
                "url": "https://example.org/report",
                "title": "Official report",
                "summary": "same evidence",
            },
            {
                "source_id": "E000002",
                "claim_ids": ["C0001"],
                "resource": "professional_editorial",
                "relation": "supports",
                "provenance": "translation of https://example.org/report",
                "url": "https://mirror.example/translation",
                "title": "Official report translated",
                "summary": "same evidence",
            },
        ]

        profiles = build_source_profiles(sources, load_source_policy(POLICY_PATH))

        self.assertEqual(profiles["C0001"]["independent_lineages"], 1)
        self.assertEqual(profiles["C0001"]["tiers"], ["authoritative", "specialist"])

    def test_source_profiles_group_pages_from_one_editorial_publisher(self):
        sources = [
            {
                "source_id": "E000001",
                "claim_ids": ["C0001"],
                "resource": "wine_dictionary",
                "relation": "direct_sensory_support",
                "url": "https://glossary.wein.plus/gewuerztraminer",
                "title": "Gewürztraminer",
            },
            {
                "source_id": "E000002",
                "claim_ids": ["C0001"],
                "resource": "wine_dictionary",
                "relation": "direct_sensory_support",
                "url": "https://glossary.wein.plus/bouquet-varieties",
                "title": "Bouquet varieties",
            },
        ]

        profiles = build_source_profiles(sources, load_source_policy(POLICY_PATH))

        self.assertEqual(profiles["C0001"]["independent_lineages"], 1)

    def test_source_profiles_group_subdomains_from_one_editorial_publisher(self):
        sources = [
            {
                "source_id": "E000001",
                "claim_ids": ["C0001"],
                "resource": "wine_dictionary",
                "relation": "direct_support",
                "url": "https://glossary.wein.plus/gewuerztraminer",
                "title": "Gewürztraminer",
            },
            {
                "source_id": "E000002",
                "claim_ids": ["C0001"],
                "resource": "wine_guide",
                "relation": "direct_support",
                "url": "https://wineguide.wein.plus/wine-regions/traminer",
                "title": "Traminer region guide",
            },
        ]

        profiles = build_source_profiles(sources, load_source_policy(POLICY_PATH))

        self.assertEqual(profiles["C0001"]["independent_lineages"], 1)


class CandidateTests(unittest.TestCase):
    def test_normalize_keys_folds_case_diacritics_and_separators(self):
        claim = {"entity_keys": ["Župa", "PROKUPAC", "vineyard-aspect"]}

        self.assertEqual(
            normalize_keys(claim),
            frozenset({"zupa", "prokupac", "vineyard_aspect"}),
        )

    def test_fact_signature_extracts_year_unit_and_denominator(self):
        claim = {
            "entity_keys": ["winery-x", "2020", "yield", "per-hectare"],
            "statement": "В 2020 году урожайность составляла 5 тонн с гектара.",
            "book_quote": "5 т/га",
            "category": "урожайность",
        }

        signature = fact_signature(claim)

        self.assertEqual(signature["years"], ["2020"])
        self.assertIn("tonne", signature["units"])
        self.assertEqual(signature["denominators"], ["per_hectare"])

    def test_corpus_measurement_values_are_not_scope_years(self):
        claims = {
            claim["claim_id"]: claim
            for claim in load_jsonl(POLICY_PATH.parents[1] / "claims.jsonl")
        }

        expected_years = {
            "C0694": [],
            "C0770": ["1903"],
            "C0926": [],
            "C1450": ["2012"],
        }
        for claim_id, expected in expected_years.items():
            with self.subTest(claim_id=claim_id):
                self.assertEqual(fact_signature(claims[claim_id])["years"], expected)

    def test_fact_signature_recognizes_tonnes_per_hectare_abbreviation(self):
        signature = fact_signature(
            {
                "entity_keys": ["yield", "per-hectare"],
                "statement": "Урожайность: 5 т/га.",
                "category": "урожайность",
            }
        )

        self.assertIn("tonne", signature["units"])
        self.assertIn("per_hectare", signature["denominators"])

    def test_fact_signature_extracts_role_scopes_and_measurements(self):
        signature = fact_signature(
            {
                "entity_keys": [
                    "erdevik-winery",
                    "belgrade-wine-region",
                    "producer-variation",
                    "area-rank",
                    "country-of-origin",
                    "yield",
                ],
                "statement": "Урожайность составляла 45 гл/га.",
                "category": "урожайность",
            }
        )

        self.assertEqual(signature["producers"], ["erdevik_winery"])
        self.assertEqual(signature["territories"], ["belgrade_wine_region"])
        self.assertIn("hectolitre", signature["units"])
        self.assertIn("per_hectare", signature["denominators"])
        self.assertIn(
            {"value": "45", "unit": "hectolitre", "denominator": "per_hectare"},
            signature["measurements"],
        )

    def test_fact_signature_separates_named_entities_from_generic_topics(self):
        cases = (
            (
                ["erdevik-winery", "tatjana-djuricic", "oenologist"],
                ["erdevik_winery", "tatjana_djuricic"],
            ),
            (
                ["fruska-gora", "crveni-cot", "elevation"],
                ["crveni_cot", "fruska_gora"],
            ),
            (
                ["petra-winery", "palic-lake", "vineyard-area"],
                ["palic_lake", "petra_winery"],
            ),
        )

        for entity_keys, expected in cases:
            with self.subTest(entity_keys=entity_keys):
                signature = fact_signature(
                    {
                        "entity_keys": entity_keys,
                        "category": "описание",
                        "statement": "Факт.",
                    }
                )
                self.assertEqual(signature["named_entity_keys"], expected)

    def test_exact_entity_fingerprint_is_duplicate_candidate(self):
        claims = [
            {
                "claim_id": "C0001",
                "entity_keys": ["prokupac", "kamenicarka", "synonym"],
                "category": "синоним",
            },
            {
                "claim_id": "C0002",
                "entity_keys": ["synonym", "kamenicarka", "prokupac"],
                "category": "название",
            },
        ]

        candidates = duplicate_candidates(claims)

        self.assertEqual(candidates[0]["claim_ids"], ["C0001", "C0002"])
        self.assertEqual(candidates[0]["match"], "exact")

    def test_one_generic_key_is_not_duplicate_candidate(self):
        claims = [
            {
                "claim_id": "C0001",
                "entity_keys": ["serbia", "climate", "rainfall"],
                "category": "климат",
            },
            {
                "claim_id": "C0002",
                "entity_keys": ["serbia", "probus", "grape"],
                "category": "история",
            },
        ]

        self.assertEqual(duplicate_candidates(claims), [])

    def test_near_duplicate_requires_two_specific_objects_and_property_match(self):
        claims = [
            {
                "claim_id": "C0001",
                "entity_keys": ["prokupac", "kamenicarka", "synonym"],
                "category": "синоним сорта",
                "statement": "Каменичарка является синонимом Прокупца.",
            },
            {
                "claim_id": "C0002",
                "entity_keys": ["prokupac", "kamenicarka", "name"],
                "category": "название сорта",
                "statement": "Название Каменичарка относится к Прокупцу.",
            },
        ]

        candidates = duplicate_candidates(claims)

        self.assertEqual(candidates[0]["claim_ids"], ["C0001", "C0002"])
        self.assertEqual(candidates[0]["match"], "near")

    def test_vintage_or_denominator_difference_is_scope_barrier(self):
        claims = [
            {
                "claim_id": "C0001",
                "entity_keys": ["winery-x", "2020", "yield", "per-hectare"],
                "category": "урожайность",
                "statement": "В 2020 году урожайность составляла 5 тонн с гектара.",
            },
            {
                "claim_id": "C0002",
                "entity_keys": ["winery-x", "2021", "yield", "total"],
                "category": "урожайность",
                "statement": "В 2021 году общий урожай составлял 5 тонн.",
            },
        ]

        self.assertEqual(duplicate_candidates(claims), [])

    def test_same_keys_with_different_statement_years_do_not_cluster(self):
        claims = [
            {
                "claim_id": "C0001",
                "entity_keys": ["winery-x", "yield", "total"],
                "category": "урожайность",
                "statement": "Общий урожай 2020 года составил 5 тонн.",
            },
            {
                "claim_id": "C0002",
                "entity_keys": ["winery-x", "yield", "total"],
                "category": "урожайность",
                "statement": "Общий урожай 2021 года составил 5 тонн.",
            },
        ]

        self.assertEqual(duplicate_candidates(claims), [])

    def test_corpus_evidence_year_does_not_hide_vintage_repeat(self):
        claims = {
            claim["claim_id"]: claim
            for claim in load_jsonl(POLICY_PATH.parents[1] / "claims.jsonl")
        }

        candidates = duplicate_candidates([claims["C1356"], claims["C2290"]])

        self.assertEqual(
            [candidate["claim_ids"] for candidate in candidates],
            [["C1356", "C2290"]],
        )

    def test_distinct_territories_producers_and_units_are_scope_barriers(self):
        cases = (
            (
                {
                    "entity_keys": ["alpha", "beta", "gamma", "zupa-region", "yield"],
                    "category": "урожайность",
                    "statement": "Урожайность составила 5 тонн.",
                },
                {
                    "entity_keys": ["alpha", "beta", "gamma", "srem-region", "yield"],
                    "category": "урожайность",
                    "statement": "Урожайность составила 5 тонн.",
                },
            ),
            (
                {
                    "entity_keys": ["alpha", "beta", "gamma", "erdevik-winery", "yield"],
                    "category": "урожайность",
                    "statement": "Урожайность составила 5 тонн.",
                },
                {
                    "entity_keys": ["alpha", "beta", "gamma", "kis-winery", "yield"],
                    "category": "урожайность",
                    "statement": "Урожайность составила 5 тонн.",
                },
            ),
            (
                {
                    "entity_keys": ["alpha", "beta", "gamma", "yield"],
                    "category": "урожайность",
                    "statement": "Объём составил 5 тонн.",
                },
                {
                    "entity_keys": ["alpha", "beta", "gamma", "yield"],
                    "category": "урожайность",
                    "statement": "Объём составил 5 литров.",
                },
            ),
        )

        for index, (left, right) in enumerate(cases):
            with self.subTest(case=index):
                left = {"claim_id": "C0001", **left}
                right = {"claim_id": "C0002", **right}
                self.assertEqual(duplicate_candidates([left, right]), [])

    def test_corpus_distinct_soil_territories_do_not_cluster(self):
        claims = {
            claim["claim_id"]: claim
            for claim in load_jsonl(POLICY_PATH.parents[1] / "claims.jsonl")
        }

        self.assertEqual(
            duplicate_candidates([claims["C0066"], claims["C1220"]]),
            [],
        )

    def test_distinct_specific_objects_on_both_sides_do_not_cluster(self):
        base = POLICY_PATH.parents[1]
        wanted = {"C0240", "C0241", "C0242", "C0243"}
        claims = [
            claim for claim in load_jsonl(base / "claims.jsonl") if claim["claim_id"] in wanted
        ]

        self.assertEqual(duplicate_candidates(claims), [])

    def test_candidate_order_is_deterministic_by_first_claim(self):
        claims = [
            {"claim_id": "C0010", "entity_keys": ["gamma", "delta", "identity"], "category": "идентичность"},
            {"claim_id": "C0011", "entity_keys": ["delta", "gamma", "identity"], "category": "идентичность"},
            {"claim_id": "C0002", "entity_keys": ["alpha", "beta", "identity"], "category": "идентичность"},
            {"claim_id": "C0003", "entity_keys": ["beta", "alpha", "identity"], "category": "идентичность"},
        ]

        candidates = duplicate_candidates(claims)

        self.assertEqual(
            [candidate["claim_ids"] for candidate in candidates],
            [["C0002", "C0003"], ["C0010", "C0011"]],
        )

    def test_overlapping_exact_and_near_matches_form_one_cluster(self):
        claims = [
            {
                "claim_id": "C0001",
                "entity_keys": ["alpha", "beta", "identity"],
                "category": "идентичность",
            },
            {
                "claim_id": "C0002",
                "entity_keys": ["identity", "beta", "alpha"],
                "category": "идентичность",
            },
            {
                "claim_id": "C0003",
                "entity_keys": ["alpha", "beta", "name", "variant"],
                "category": "название",
            },
        ]

        candidates = duplicate_candidates(claims)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["claim_ids"], ["C0001", "C0002", "C0003"])
        self.assertEqual(candidates[0]["match"], "near")

    def test_bridge_claim_cannot_merge_semantically_incompatible_endpoints(self):
        claims = [
            {
                "claim_id": "C0001",
                "entity_keys": ["alpha", "beta", "identity"],
                "category": "идентичность",
            },
            {
                "claim_id": "C0002",
                "entity_keys": ["alpha", "beta", "gamma", "identity"],
                "category": "идентичность",
            },
            {
                "claim_id": "C0003",
                "entity_keys": ["beta", "gamma", "identity"],
                "category": "идентичность",
            },
        ]

        candidates = duplicate_candidates(claims)

        self.assertFalse(
            any({"C0001", "C0003"}.issubset(candidate["claim_ids"]) for candidate in candidates)
        )

    def test_wildcard_scope_preserves_each_compatible_duplicate_edge(self):
        claims = [
            {
                "claim_id": "C0001",
                "entity_keys": ["alpha", "beta", "yield"],
                "category": "урожайность",
                "statement": "Урожайность составляла 5 тонн.",
            },
            {
                "claim_id": "C0002",
                "entity_keys": ["alpha", "beta", "yield", "2020"],
                "category": "урожайность",
                "statement": "В 2020 году урожайность составляла 5 тонн.",
            },
            {
                "claim_id": "C0003",
                "entity_keys": ["alpha", "beta", "yield", "2021"],
                "category": "урожайность",
                "statement": "В 2021 году урожайность составляла 5 тонн.",
            },
        ]

        candidates = duplicate_candidates(claims)

        self.assertEqual(
            [candidate["claim_ids"] for candidate in candidates],
            [["C0001", "C0002"], ["C0001", "C0003"]],
        )

    def test_flags_high_consensus_supported_only_by_wikipedia(self):
        reasons = risk_reasons(
            {
                "claim_id": "C0001",
                "statement": "Это был первый виноградник.",
                "book_quote": "первый виноградник",
                "category": "история",
                "entity_keys": ["first"],
            },
            {"status": "совпадает", "consensus": "высокий"},
            {
                "tiers": ["wikipedia"],
                "independent_lineages": 1,
                "unknown_source_ids": [],
                "sources": [
                    {
                        "tier": "wikipedia",
                        "independence": "encyclopedic_secondary",
                        "competence": "within_encyclopedic_scope",
                    }
                ],
            },
        )

        self.assertIn("high_consensus_without_strong_source", reasons)
        self.assertIn("high_risk_fact_type", reasons)
        self.assertIn("categorical_or_superlative", reasons)

    def test_corpus_required_fact_classes_are_high_risk(self):
        claims = {
            claim["claim_id"]: claim
            for claim in load_jsonl(POLICY_PATH.parents[1] / "claims.jsonl")
        }
        strong_profile = {
            "tiers": ["authoritative"],
            "independent_lineages": 1,
            "unknown_source_ids": [],
            "sources": [
                {
                    "tier": "authoritative",
                    "independence": "institutional_primary",
                    "competence": "within_scope_primary",
                }
            ],
        }

        for claim_id in (
            "C0010",
            "C0407",
            "C0688",
            "C1048",
            "C1205",
            "C1330",
            "C1534",
            "C1587",
            "C1588",
        ):
            with self.subTest(claim_id=claim_id):
                reasons = risk_reasons(
                    claims[claim_id],
                    {"status": "совпадает", "consensus": "высокий"},
                    strong_profile,
                )
                self.assertIn("high_risk_fact_type", reasons)

    def test_two_independent_specialist_lines_prevent_weak_high_consensus_flag(self):
        reasons = risk_reasons(
            {"claim_id": "C0001", "statement": "Обычный факт.", "category": "описание", "entity_keys": []},
            {"status": "совпадает", "consensus": "высокий"},
            {
                "tiers": ["specialist"],
                "independent_lineages": 2,
                "unknown_source_ids": [],
                "sources": [
                    {
                        "tier": "specialist",
                        "independence": "editorially_independent",
                        "competence": "role_unspecified",
                        "relation": "direct_support",
                        "lineage": "url:https://one.example/evidence",
                    },
                    {
                        "tier": "specialist",
                        "independence": "editorially_independent",
                        "competence": "role_unspecified",
                        "relation": "supports_with_qualification",
                        "lineage": "url:https://two.example/evidence",
                    }
                ],
            },
        )

        self.assertNotIn("high_consensus_without_strong_source", reasons)

    def test_one_ordinary_specialist_line_is_not_enough_for_high_consensus(self):
        reasons = risk_reasons(
            {"claim_id": "C0001", "statement": "Обычный факт.", "category": "описание", "entity_keys": []},
            {"status": "совпадает", "consensus": "высокий"},
            {
                "tiers": ["specialist"],
                "independent_lineages": 1,
                "unknown_source_ids": [],
                "sources": [
                    {
                        "tier": "specialist",
                        "independence": "editorially_independent",
                        "competence": "role_unspecified",
                        "relation": "direct_support",
                        "lineage": "url:https://one.example/evidence",
                    }
                ],
            },
        )

        self.assertIn("high_consensus_without_strong_source", reasons)

    def test_one_decisive_registry_source_is_enough_for_high_consensus(self):
        reasons = risk_reasons(
            {"claim_id": "C0001", "statement": "Синоним сорта.", "category": "синоним", "entity_keys": []},
            {"status": "совпадает", "consensus": "высокий"},
            {
                "tiers": ["authoritative"],
                "independent_lineages": 1,
                "unknown_source_ids": [],
                "sources": [
                    {
                        "tier": "authoritative",
                        "independence": "editorially_independent",
                        "competence": "role_unspecified",
                        "resource": "vivc",
                        "relation": "direct_identity_evidence",
                        "lineage": "url:https://www.vivc.de/variety/1",
                    }
                ],
            },
        )

        self.assertNotIn("high_consensus_without_strong_source", reasons)

    def test_decisive_sources_are_not_decisive_outside_their_fact_domain(self):
        cases = (
            (
                "vivc",
                "direct_sensory_support",
                "Для вина типичен аромат розы.",
                "сортовой сенсорный дескриптор",
            ),
            (
                "current_national_wine_labelling_rulebook",
                "direct_sensory_support",
                "Для вина типичен аромат розы.",
                "сортовой сенсорный дескриптор",
            ),
            (
                "competition_official_results",
                "direct_origin_support",
                "Сорт происходит из Сербии.",
                "происхождение сорта",
            ),
            (
                "official_statistics",
                "direct_identity_support",
                "Каменичарка является синонимом Прокупца.",
                "синоним сорта",
            ),
            (
                "oiv_standard",
                "direct_history_support",
                "Хозяйство было основано семьёй виноградарей.",
                "история хозяйства",
            ),
        )

        for resource, relation, statement, category in cases:
            with self.subTest(resource=resource):
                reasons = risk_reasons(
                    {
                        "claim_id": "C0001",
                        "statement": statement,
                        "category": category,
                        "entity_keys": ["subject", "fact"],
                    },
                    {"status": "совпадает", "consensus": "высокий"},
                    {
                        "tiers": ["authoritative"],
                        "independent_lineages": 1,
                        "unknown_source_ids": [],
                        "sources": [
                            {
                                "tier": "authoritative",
                                "independence": "editorially_independent",
                                "competence": "role_unspecified",
                                "resource": resource,
                                "relation": relation,
                                "lineage": f"publisher:{resource}.example",
                            }
                        ],
                    },
                )

                self.assertIn("high_consensus_without_strong_source", reasons)

    def test_corpus_registry_identity_is_decisive_but_same_publisher_sensory_is_not(self):
        base = POLICY_PATH.parents[1]
        claims = {claim["claim_id"]: claim for claim in load_jsonl(base / "claims.jsonl")}
        decisions = {
            decision["claim_id"]: decision
            for decision in load_jsonl(base / "decisions.jsonl")
        }
        profiles = build_source_profiles(
            load_jsonl(base / "sources.jsonl"),
            load_source_policy(POLICY_PATH),
        )

        identity_reasons = risk_reasons(
            claims["C0673"], decisions["C0673"], profiles["C0673"]
        )
        sensory_reasons = risk_reasons(
            claims["C0674"], decisions["C0674"], profiles["C0674"]
        )

        self.assertNotIn("high_consensus_without_strong_source", identity_reasons)
        self.assertIn("high_consensus_without_strong_source", sensory_reasons)

    def test_negative_specialist_relation_is_not_strong_support(self):
        reasons = risk_reasons(
            {"claim_id": "C0001", "statement": "Обычный факт.", "category": "описание", "entity_keys": []},
            {"status": "совпадает", "consensus": "высокий"},
            {
                "tiers": ["specialist"],
                "independent_lineages": 2,
                "unknown_source_ids": [],
                "sources": [
                    {
                        "tier": "specialist",
                        "independence": "editorially_independent",
                        "competence": "role_unspecified",
                        "relation": "no_sufficient_public_record",
                        "lineage": "url:https://one.example/search",
                    },
                    {
                        "tier": "specialist",
                        "independence": "editorially_independent",
                        "competence": "role_unspecified",
                        "relation": "no_relevant_material",
                        "lineage": "url:https://two.example/search",
                    },
                ],
            },
        )

        self.assertIn("high_consensus_without_strong_source", reasons)

    def test_unknown_classification_does_not_derive_weak_support_reason(self):
        reasons = risk_reasons(
            {"claim_id": "C0001", "statement": "Обычный факт.", "category": "описание", "entity_keys": []},
            {"status": "совпадает", "consensus": "высокий"},
            {
                "tiers": ["weak"],
                "independent_lineages": 1,
                "unknown_source_ids": ["E000001"],
                "sources": [
                    {
                        "source_id": "E000001",
                        "tier": "weak",
                        "independence": "unknown",
                        "competence": "role_unspecified",
                        "resource": "unclassified_research_centre",
                        "relation": "direct_support",
                        "lineage": "url:https://research.example/evidence",
                    }
                ],
            },
        )

        self.assertEqual(reasons, ["unknown_source_classification"])

    def test_interested_source_does_not_count_as_strong_support(self):
        reasons = risk_reasons(
            {"claim_id": "C0001", "statement": "Факт.", "category": "описание", "entity_keys": []},
            {"status": "совпадает", "consensus": "высокий"},
            {
                "tiers": ["authoritative"],
                "independent_lineages": 1,
                "unknown_source_ids": [],
                "sources": [
                    {
                        "tier": "authoritative",
                        "independence": "interested_primary",
                        "competence": "interested_only",
                    }
                ],
            },
        )

        self.assertIn("high_consensus_without_strong_source", reasons)

    def test_categorical_pattern_distinguishes_samyj_from_samobytnyj(self):
        strong_profile = {
            "tiers": ["specialist"],
            "independent_lineages": 1,
            "unknown_source_ids": [],
            "sources": [
                {
                    "tier": "specialist",
                    "independence": "editorially_independent",
                    "competence": "role_unspecified",
                }
            ],
        }
        ordinary = risk_reasons(
            {"statement": "У вина самобытный стиль.", "category": "описание", "entity_keys": []},
            {"status": "совпадает", "consensus": "высокий"},
            strong_profile,
        )
        superlative = risk_reasons(
            {"statement": "Это самый старый виноградник.", "category": "история", "entity_keys": []},
            {"status": "совпадает", "consensus": "высокий"},
            strong_profile,
        )

        self.assertNotIn("categorical_or_superlative", ordinary)
        self.assertIn("categorical_or_superlative", superlative)

    def test_flags_wikipedia_conflict_and_absence_separately(self):
        empty_profile = {
            "tiers": [],
            "independent_lineages": 0,
            "unknown_source_ids": [],
            "sources": [],
        }

        conflict = risk_reasons(
            {"claim_id": "C0001", "statement": "Факт", "category": "история", "entity_keys": []},
            {"status": "между Википедиями нет согласия", "consensus": "конфликт"},
            empty_profile,
        )
        absent = risk_reasons(
            {"claim_id": "C0002", "statement": "Факт", "category": "история", "entity_keys": []},
            {"status": "в Википедиях отсутствует", "consensus": "отсутствует"},
            empty_profile,
        )

        self.assertIn("wikipedia_disagreement", conflict)
        self.assertNotIn("wikipedia_absence", conflict)
        self.assertIn("wikipedia_absence", absent)

    def test_resolved_multilingual_wikipedia_conflicts_keep_reason_code(self):
        base = POLICY_PATH.parents[1]
        claims = {claim["claim_id"]: claim for claim in load_jsonl(base / "claims.jsonl")}
        decisions = {
            decision["claim_id"]: decision
            for decision in load_jsonl(base / "decisions.jsonl")
        }
        profiles = build_source_profiles(
            load_jsonl(base / "sources.jsonl"),
            load_source_policy(POLICY_PATH),
        )

        for claim_id in ("C0040", "C0184", "C1951"):
            with self.subTest(claim_id=claim_id):
                self.assertIn(
                    "wikipedia_disagreement",
                    risk_reasons(claims[claim_id], decisions[claim_id], profiles[claim_id]),
                )

        for claim_id in ("C0395", "C0419", "C0647", "C0660"):
            with self.subTest(negative_claim_id=claim_id):
                self.assertNotIn(
                    "wikipedia_disagreement",
                    risk_reasons(claims[claim_id], decisions[claim_id], profiles[claim_id]),
                )

    def test_wikipedia_disagreement_uses_only_attached_language_editions(self):
        reasons = risk_reasons(
            {
                "claim_id": "C0001",
                "statement": "Факт.",
                "category": "идентичность",
                "entity_keys": ["subject", "identity"],
            },
            {
                "status": "совпадает",
                "consensus": "конфликт",
                "comparison": (
                    "English Wikipedia gives one identity, whereas German Wikipedia "
                    "gives another."
                ),
                "independence": "Compared Wikipedia EN and DE.",
            },
            {
                "tiers": ["wikipedia"],
                "independent_lineages": 2,
                "unknown_source_ids": [],
                "sources": [
                    {
                        "tier": "wikipedia",
                        "language": "sr",
                        "relation": "wikipedia_sr_comparison",
                    },
                    {
                        "tier": "wikipedia",
                        "language": "ru",
                        "relation": "wikipedia_ru_comparison",
                    },
                ],
            },
        )

        self.assertNotIn("wikipedia_disagreement", reasons)

    def test_scan_marks_duplicate_status_variance(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            rows = {
                "claims.jsonl": [
                    {"claim_id": "C0001", "entity_keys": ["prokupac", "kamenicarka", "synonym"], "category": "синоним", "statement": "Факт один", "book_quote": "Факт один"},
                    {"claim_id": "C0002", "entity_keys": ["synonym", "kamenicarka", "prokupac"], "category": "синоним", "statement": "Факт два", "book_quote": "Факт два"},
                ],
                "decisions.jsonl": [
                    {"claim_id": "C0001", "status": "совпадает", "consensus": "высокий", "editor_conclusion": "Подтверждено."},
                    {"claim_id": "C0002", "status": "подтверждено частично", "consensus": "средний", "editor_conclusion": "Требуется оговорка."},
                ],
                "sources.jsonl": [],
            }
            for filename, records in rows.items():
                (base / filename).write_text(
                    "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
                    encoding="utf-8",
                )

            scan = scan_audit(base, POLICY_PATH)

        self.assertEqual(scan["duplicates"][0]["claim_ids"], ["C0001", "C0002"])
        self.assertIn(
            "duplicate_decision_variance",
            scan["duplicates"][0]["risk_reasons"],
        )

    def test_scan_marks_duplicate_editor_conclusion_variance(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            rows = {
                "claims.jsonl": [
                    {
                        "claim_id": "C0001",
                        "entity_keys": ["prokupac", "kamenicarka", "synonym"],
                        "category": "синоним",
                        "statement": "Факт один",
                        "book_quote": "Факт один",
                    },
                    {
                        "claim_id": "C0002",
                        "entity_keys": ["synonym", "kamenicarka", "prokupac"],
                        "category": "синоним",
                        "statement": "Факт два",
                        "book_quote": "Факт два",
                    },
                ],
                "decisions.jsonl": [
                    {
                        "claim_id": "C0001",
                        "status": "совпадает",
                        "consensus": "высокий",
                        "independence": "Две независимые линии.",
                        "editor_conclusion": "Оставить без оговорки.",
                    },
                    {
                        "claim_id": "C0002",
                        "status": "совпадает",
                        "consensus": "высокий",
                        "independence": "Две независимые линии.",
                        "editor_conclusion": "Оставить только с оговоркой.",
                    },
                ],
                "sources.jsonl": [],
            }
            for filename, records in rows.items():
                (base / filename).write_text(
                    "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
                    encoding="utf-8",
                )

            scan = scan_audit(base, POLICY_PATH)

        duplicate = scan["duplicates"][0]
        self.assertIn("duplicate_decision_variance", duplicate["risk_reasons"])
        self.assertEqual(duplicate["variance_fields"], ["editor_conclusion"])

    def test_scan_does_not_select_unknown_classification_alone(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            rows = {
                "claims.jsonl": [
                    {
                        "claim_id": "C0001",
                        "entity_keys": ["ordinary"],
                        "category": "описание",
                        "statement": "Обычный факт.",
                        "book_quote": "Обычный факт.",
                    }
                ],
                "decisions.jsonl": [
                    {
                        "claim_id": "C0001",
                        "status": "совпадает",
                        "consensus": "высокий",
                        "editor_conclusion": "Подтверждено.",
                    }
                ],
                "sources.jsonl": [
                    {
                        "source_id": "E000001",
                        "claim_ids": ["C0001"],
                        "resource": "unclassified_research_centre",
                        "relation": "direct_support",
                        "url": "https://research.example/evidence",
                        "title": "Evidence",
                    }
                ],
            }
            for filename, records in rows.items():
                (base / filename).write_text(
                    "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
                    encoding="utf-8",
                )

            scan = scan_audit(base, POLICY_PATH)

        self.assertEqual(scan["claim_risks"], [])

    def test_scan_derives_late_source_recheck_for_eligible_early_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            rows = {
                "claims.jsonl": [
                    {
                        "claim_id": "C0001",
                        "entity_keys": ["prokupac", "kamenicarka", "synonym"],
                        "category": "синоним сорта",
                        "statement": "Каменичарка является синонимом Прокупца.",
                        "book_quote": "Синоним.",
                    },
                    {
                        "claim_id": "C0301",
                        "entity_keys": ["prokupac", "kamenicarka", "name"],
                        "category": "название сорта",
                        "statement": "Название Каменичарка относится к Прокупцу.",
                        "book_quote": "Название.",
                    },
                ],
                "decisions.jsonl": [
                    {
                        "claim_id": "C0001",
                        "status": "подтверждено частично",
                        "consensus": "средний",
                        "editor_conclusion": "Нужна проверка.",
                    },
                    {
                        "claim_id": "C0301",
                        "status": "совпадает",
                        "consensus": "высокий",
                        "editor_conclusion": "Подтверждено.",
                    },
                ],
                "sources.jsonl": [
                    {
                        "source_id": "E000001",
                        "claim_ids": ["C0001"],
                        "resource": "wikipedia",
                        "language": "en",
                        "relation": "supports_with_qualification",
                        "url": "https://en.wikipedia.org/wiki/Prokupac",
                        "title": "Prokupac",
                    },
                    {
                        "source_id": "E000002",
                        "claim_ids": ["C0301"],
                        "resource": "vivc",
                        "language": "en",
                        "relation": "direct_identity_evidence",
                        "url": "https://www.vivc.de/variety/1",
                        "title": "VIVC variety record",
                    },
                ],
            }
            for filename, records in rows.items():
                (base / filename).write_text(
                    "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
                    encoding="utf-8",
                )

            scan = scan_audit(base, POLICY_PATH)

        early = next(item for item in scan["claim_risks"] if item["claim_ids"] == ["C0001"])
        self.assertIn("late_source_recheck", early["risk_reasons"])
        self.assertEqual(
            early["late_source_matches"][0]["resource"],
            "vivc",
        )

    def test_late_source_recheck_requires_shared_named_entity(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            rows = {
                "claims.jsonl": [
                    {
                        "claim_id": "C0001",
                        "entity_keys": ["erdevik-winery", "tatjana-djuricic", "oenologist"],
                        "category": "персона и роль",
                        "statement": "Главным энологом Erdevik является Tatjana Đuričić.",
                        "book_quote": "Энолог — Татьяна Джуричич.",
                    },
                    {
                        "claim_id": "C0301",
                        "entity_keys": ["tarpos", "jelena-zivanovic", "oenologist"],
                        "category": "персона и роль",
                        "statement": "Энологом Tarpoš является Jelena Živanović.",
                        "book_quote": "Энолог — Елена Живанович.",
                    },
                ],
                "decisions.jsonl": [
                    {
                        "claim_id": "C0001",
                        "status": "подтверждено частично",
                        "consensus": "средний",
                        "editor_conclusion": "Нужна проверка.",
                    },
                    {
                        "claim_id": "C0301",
                        "status": "совпадает",
                        "consensus": "высокий",
                        "editor_conclusion": "Подтверждено.",
                    },
                ],
                "sources.jsonl": [
                    {
                        "source_id": "E000001",
                        "claim_ids": ["C0001"],
                        "resource": "wikipedia",
                        "language": "en",
                        "relation": "supports_with_qualification",
                        "url": "https://en.wikipedia.org/wiki/Winemaking",
                        "title": "Winemaking",
                    },
                    {
                        "source_id": "E000002",
                        "claim_ids": ["C0301"],
                        "resource": "government",
                        "language": "sr",
                        "relation": "direct_support",
                        "url": "https://government.example/tarpos-oenologist",
                        "title": "Tarpoš record",
                    },
                ],
            }
            for filename, records in rows.items():
                (base / filename).write_text(
                    "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
                    encoding="utf-8",
                )

            scan = scan_audit(base, POLICY_PATH)

        early = next(item for item in scan["claim_risks"] if item["claim_ids"] == ["C0001"])
        self.assertNotIn("late_source_recheck", early["risk_reasons"])
        self.assertNotIn("late_source_matches", early)


class ReviewValidationTests(unittest.TestCase):
    def _validation_errors_without_exception(self, callback):
        try:
            return callback()
        except (TypeError, KeyError) as error:
            return [f"unexpected exception: {type(error).__name__}: {error}"]

    def _candidate(self, **overrides):
        candidate = {
            "meta_id": "M0001",
            "candidate_key": "risk:C0001:disputed_status",
            "kind": "риск решения",
            "claim_ids": ["C0001"],
            "risk_reasons": ["disputed_status"],
            "source_profile": {"C0001": {"tiers": []}},
            "original_statuses": [
                {"claim_id": "C0001", "status": "расходится", "consensus": "конфликт"}
            ],
        }
        candidate.update(overrides)
        return candidate

    def _review(self, **overrides):
        record = {
            "meta_id": "M0001",
            "candidate_key": "risk:C0001:disputed_status",
            "kind": "риск решения",
            "claim_ids": ["C0001"],
            "canonical_question": "Какой статус подтверждён для этого утверждения?",
            "risk_reasons": ["disputed_status"],
            "scope": "Утверждение C0001 без изменения временного или территориального охвата.",
            "source_lines": ["E000001"],
            "source_weight": "Независимая профильная линия имеет достаточный вес.",
            "resolution": "согласован",
            "resolution_notes": "Сопоставление источников не выявило противоречия.",
            "changes": [],
            "remaining_gap": "",
        }
        record.update(overrides)
        return record

    def test_write_candidates_assigns_contiguous_stable_identifiers(self):
        scan = {
            "duplicates": [{"kind": "смысловой повтор", "match": "exact", "claim_ids": ["C0001", "C0002"], "shared_keys": ["prokupac", "synonym"], "risk_reasons": []}],
            "claim_risks": [{"kind": "риск решения", "claim_ids": ["C0001"], "risk_reasons": ["disputed_status"], "source_profile": {"tiers": ["wikipedia"]}, "original_statuses": []}],
            "source_profiles": {"C0001": {"tiers": []}, "C0002": {"tiers": []}},
            "decisions_by_id": {},
        }
        self.assertTrue(hasattr(meta_audit, "write_candidates"))
        self.assertTrue(hasattr(meta_audit, "load_candidates"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidates.jsonl"
            meta_audit.write_candidates(scan, path)
            candidates = meta_audit.load_candidates(path)

        self.assertEqual([item["meta_id"] for item in candidates], ["M0001", "M0002"])
        self.assertEqual(len({item["candidate_key"] for item in candidates}), 2)
        self.assertEqual(candidates[0]["claim_ids"], ["C0001", "C0002"])

    def test_load_candidates_rejects_duplicate_meta_id_and_candidate_key(self):
        self.assertTrue(hasattr(meta_audit, "load_candidates"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidates.jsonl"
            path.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in (self._candidate(), self._candidate(claim_ids=["C0002"], original_statuses=[]))) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate meta_id M0001"):
                meta_audit.load_candidates(path)
            path.write_text(
                "\n".join(json.dumps(record, ensure_ascii=False) for record in (self._candidate(), self._candidate(meta_id="M0002", claim_ids=["C0002"], original_statuses=[]))) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate candidate_key risk:C0001:disputed_status"):
                meta_audit.load_candidates(path)

    def test_validate_review_rejects_missing_current_claim(self):
        self.assertTrue(hasattr(meta_audit, "validate_review"))
        errors = meta_audit.validate_review([self._candidate()], {"C0001"}, [self._review(claim_ids=["C9999"])], False)
        self.assertIn("unknown claim C9999", errors)

    def test_validate_review_rejects_supporting_and_checked_only_sources_without_reverse_claim_links(self):
        review = self._review(
            source_lines=[
                {
                    "claim_id": "C0001",
                    "source_ids": ["E000001"],
                    "checked_only_source_ids": ["E000002", "E000003"],
                }
            ]
        )

        errors = meta_audit.validate_review(
            [self._candidate()],
            {"C0001"},
            [review],
            False,
            {"E000001": {"C9999"}, "E000002": {"C9999"}},
        )

        self.assertIn("review M0001 source E000001 missing reverse claim C0001", errors)
        self.assertIn("review M0001 source E000002 missing reverse claim C0001", errors)
        self.assertIn("review M0001 source E000003 is unknown", errors)

    def test_validate_review_accepts_combined_source_line_when_every_reverse_link_exists(self):
        candidate = self._candidate(
            claim_ids=["C0001", "C0002"],
            candidate_key="repeat:C0001,C0002:exact:test",
            kind="смысловой повтор",
            risk_reasons=["duplicate_decision_variance"],
        )
        review = self._review(
            meta_id="M0001",
            candidate_key="repeat:C0001,C0002:exact:test",
            kind="смысловой повтор",
            claim_ids=["C0001", "C0002"],
            risk_reasons=["duplicate_decision_variance"],
            source_lines=[
                {
                    "claim_ids": ["C0001", "C0002"],
                    "source_ids": ["E000001", "E000002"],
                }
            ],
        )

        errors = meta_audit.validate_review(
            [candidate],
            {"C0001", "C0002"},
            [review],
            False,
            {"E000001": {"C0001", "C0002"}, "E000002": {"C0001", "C0002"}},
        )

        self.assertEqual(errors, [])

    def test_validate_review_rejects_invalid_resolution_and_empty_prose(self):
        self.assertTrue(hasattr(meta_audit, "validate_review"))
        errors = meta_audit.validate_review([self._candidate()], {"C0001"}, [self._review(resolution="неизвестно", canonical_question=" ", resolution_notes="")], False)
        self.assertIn("invalid resolution неизвестно", errors)
        self.assertIn("empty canonical_question", errors)
        self.assertIn("empty resolution_notes", errors)

    def test_validate_review_reports_wrong_json_types_without_exceptions(self):
        malformed_candidate_errors = self._validation_errors_without_exception(
            lambda: meta_audit.validate_review(
                [
                    self._candidate(
                        meta_id=[],
                        candidate_key={"not": "a string"},
                        claim_ids=None,
                    )
                ],
                {"C0001"},
                [],
                False,
            )
        )
        malformed_review_errors = self._validation_errors_without_exception(
            lambda: meta_audit.validate_review(
                [self._candidate()],
                {"C0001"},
                [
                    self._review(
                        candidate_key=["not-a-string"],
                        resolution={"not": "a string"},
                        claim_ids=None,
                    )
                ],
                False,
            )
        )

        self.assertNotIn("unexpected exception", "\n".join(malformed_candidate_errors))
        self.assertNotIn("unexpected exception", "\n".join(malformed_review_errors))
        self.assertIn("invalid meta_id []", malformed_candidate_errors)
        self.assertIn("invalid candidate_key", malformed_candidate_errors)
        self.assertIn("invalid claim_ids", malformed_candidate_errors)
        self.assertIn("invalid candidate_key", malformed_review_errors)
        self.assertIn("invalid resolution", "\n".join(malformed_review_errors))
        self.assertIn("invalid claim_ids", malformed_review_errors)

    def test_require_complete_reports_unreviewed_candidate(self):
        candidates = [{"candidate_key": "risk:C0001"}]
        self.assertTrue(hasattr(meta_audit, "validate_review"))
        self.assertIn("unreviewed candidate risk:C0001", meta_audit.validate_review(candidates, {"C0001"}, [], True))

    def test_cli_scans_and_accepts_missing_optional_review_file(self):
        script = POLICY_PATH.parents[1] / "meta_audit.py"
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "audit"
            base.mkdir()
            (base / "claims.jsonl").write_text(json.dumps({"claim_id": "C0001", "entity_keys": ["prokupac", "synonym"], "category": "синоним", "statement": "Каменичарка — синоним Прокупца.", "book_quote": "Каменичарка."}, ensure_ascii=False) + "\n", encoding="utf-8")
            (base / "decisions.jsonl").write_text(json.dumps({"claim_id": "C0001", "status": "подтверждено частично", "consensus": "средний"}, ensure_ascii=False) + "\n", encoding="utf-8")
            (base / "sources.jsonl").write_text("", encoding="utf-8")
            candidates = base / "candidates.jsonl"
            baseline = base / "baseline.json"
            scan = subprocess.run([sys.executable, str(script), "scan", str(base), "--policy", str(POLICY_PATH), "--candidates", str(candidates), "--baseline", str(baseline)], capture_output=True, text=True)
            self.assertEqual(scan.returncode, 0, scan.stderr)
            self.assertTrue(candidates.exists())
            self.assertTrue(baseline.exists())
            validate = subprocess.run([sys.executable, str(script), "validate-review", str(base), "--policy", str(POLICY_PATH), "--candidates", str(candidates), "--review", str(base / "review.jsonl")], capture_output=True, text=True)
            require_complete = subprocess.run([sys.executable, str(script), "validate-review", str(base), "--policy", str(POLICY_PATH), "--candidates", str(candidates), "--review", str(base / "review.jsonl"), "--require-complete"], capture_output=True, text=True)

        self.assertEqual(validate.returncode, 0, validate.stderr)
        self.assertEqual(require_complete.returncode, 1, require_complete.stderr)
        self.assertIn("unreviewed candidate", require_complete.stderr)


class BaselineTests(unittest.TestCase):
    def test_each_claim_band_includes_reconcilable_methodology_counts(self):
        scan = {
            "claims": 500,
            "decisions": 2,
            "sources": 3,
            "decisions_by_id": {
                "C0001": {"status": "совпадает", "consensus": "высокий"},
                "C0251": {"status": "расходится", "consensus": "конфликт"},
            },
            "source_profiles": {
                "C0001": {"tiers": ["authoritative", "wikipedia"]},
                "C0251": {"tiers": ["specialist"]},
            },
        }
        candidates = [
            {"candidate_key": "risk:C0001", "claim_ids": ["C0001"], "risk_reasons": ["disputed_status"]},
            {"candidate_key": "risk:C0251", "claim_ids": ["C0251"], "risk_reasons": ["high_risk_fact_type"]},
        ]

        baseline = meta_audit.build_baseline(scan, candidates)

        self.assertEqual(set(baseline["by_claim_band"]), {"C0001-C0250", "C0251-C0500"})
        for counts in baseline["by_claim_band"].values():
            self.assertIn("status", counts)
            self.assertIn("consensus", counts)
            self.assertIn("source_tier", counts)
            self.assertIn("risk_reasons", counts)
        self.assertEqual(
            baseline["status"],
            {
                key: sum(band["status"].get(key, 0) for band in baseline["by_claim_band"].values())
                for key in baseline["status"]
            },
        )
        self.assertEqual(
            baseline["consensus"],
            {
                key: sum(band["consensus"].get(key, 0) for band in baseline["by_claim_band"].values())
                for key in baseline["consensus"]
            },
        )
        self.assertEqual(
            baseline["source_tier"],
            {
                key: sum(band["source_tier"].get(key, 0) for band in baseline["by_claim_band"].values())
                for key in baseline["source_tier"]
            },
        )
        self.assertEqual(
            baseline["risk_reason"],
            {
                key: sum(band["risk_reasons"].get(key, 0) for band in baseline["by_claim_band"].values())
                for key in baseline["risk_reason"]
            },
        )


if __name__ == "__main__":
    unittest.main()
