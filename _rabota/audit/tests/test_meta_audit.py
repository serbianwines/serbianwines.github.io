import json
import tempfile
import unittest
from pathlib import Path

from _rabota.audit.meta_audit import (
    build_source_profiles,
    classify_source,
    load_jsonl,
    load_source_policy,
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


if __name__ == "__main__":
    unittest.main()
