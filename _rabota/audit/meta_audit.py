#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


URL_PATTERN = re.compile(r"https?://[^\s;,]+", re.IGNORECASE)
WIKIPEDIA_TRANSLATION_PATTERN = re.compile(
    r"(?:translation|translated)[^;\n]*?wikipedia[-_ ]([a-z]{2,3})",
    re.IGNORECASE,
)
TRANSLATION_MARKERS = (
    "translation of",
    "translated from",
    "translation from",
    "syndicated from",
    "reprint of",
    "republication of",
)

GENERIC_ENTITY_KEYS = {
    "serbia",
    "wine",
    "winery",
    "grape",
    "vineyard",
    "history",
    "climate",
    "geography",
    "style",
    "producer",
    "current",
}
GENERIC_TOPIC_KEYS = {
    "elevation",
    "oenologist",
    "vineyard_area",
}
PROPERTY_ALIASES = {
    "identity": {
        "alias",
        "identity",
        "name",
        "naming",
        "synonym",
        "идентичность",
        "имя",
        "название",
        "синоним",
    },
    "yield": {"harvest", "yield", "урожай", "урожайность"},
    "composition": {
        "blend",
        "composition",
        "varietal_composition",
        "купаж",
        "состав",
        "сортовой_состав",
    },
    "origin": {
        "ancestry",
        "origin",
        "parentage",
        "происхождение",
        "родство",
    },
    "geography": {
        "area",
        "geography",
        "location",
        "region",
        "territory",
        "география",
        "местоположение",
        "регион",
        "территория",
    },
    "chronology": {
        "chronology",
        "date",
        "period",
        "year",
        "дата",
        "период",
        "хронология",
    },
    "law": {
        "decree",
        "edict",
        "law",
        "legal_status",
        "regulation",
        "закон",
        "правовой_статус",
        "регламент",
        "указ",
    },
}
PROPERTY_TOKENS = frozenset(
    token for aliases in PROPERTY_ALIASES.values() for token in aliases
)
RISK_REASON_ORDER = (
    "duplicate_decision_variance",
    "wikipedia_disagreement",
    "wikipedia_absence",
    "disputed_status",
    "non_high_consensus",
    "high_consensus_without_strong_source",
    "high_risk_fact_type",
    "categorical_or_superlative",
    "late_source_recheck",
    "unknown_source_classification",
)
ALLOWED_RESOLUTIONS = {
    "согласован",
    "исправлен",
    "различается по охвату",
    "остаётся неразрешённым",
}
CANDIDATE_FIELDS = (
    "meta_id",
    "candidate_key",
    "kind",
    "claim_ids",
    "risk_reasons",
    "source_profile",
    "original_statuses",
)
REVIEW_FIELDS = (
    "meta_id",
    "candidate_key",
    "kind",
    "claim_ids",
    "canonical_question",
    "risk_reasons",
    "scope",
    "source_lines",
    "source_weight",
    "resolution",
    "resolution_notes",
    "changes",
    "remaining_gap",
)
DISPUTED_STATUSES = {
    "подтверждено частично",
    "расходится",
    "между Википедиями нет согласия",
    "в Википедиях отсутствует",
    "непроверяемо по выбранному корпусу",
}
NEGATIVE_RELATION_MARKERS = (
    "context_only",
    "gap",
    "limited_context",
    "no_direct",
    "no_relevant",
    "no_specific",
    "no_sufficient",
    "not_found",
    "search_result",
    "silence",
)
POSITIVE_RELATION_MARKERS = (
    "authoritative",
    "authority",
    "comparison",
    "confirmation",
    "contradiction",
    "direct",
    "evidence",
    "official",
    "primary",
    "qualification",
    "scientific",
    "snapshot",
    "support",
)
DECISIVE_REGISTRY_MARKERS = (
    "cultivar_register",
    "grape_registry",
    "international_variety_catalogue",
    "national_vine_variety_catalogue",
    "serbian_cultivar_register",
    "university_grape_registry",
    "variety_catalogue",
    "vivc",
)
DECISIVE_COMPETITION_MARKERS = (
    "competition_official",
    "competition_organiser",
    "competition_primary",
    "official_competition",
)
DECISIVE_LEGAL_MARKERS = (
    "government_zoning",
    "law",
    "official_register",
    "official_regional_specification",
    "regulation",
    "rulebook",
    "serbian_regulation",
)
DECISIVE_STATISTICS_MARKERS = (
    "official_statistics",
)
DECISIVE_STANDARD_MARKERS = (
    "fao_land_cover_standard",
    "fao_soil_reference",
    "international_standard",
    "iso",
    "oiv",
    "soil_classification_reference",
)
LANGUAGE_MARKERS = {
    "en": (r"\ben\b", r"\benglish\b", r"\bанглийск\w*"),
    "de": (r"\bde\b", r"\bgerman\b", r"\bнемецк\w*"),
    "hu": (r"\bhu\b", r"\bhungarian\b", r"\bвенгерск\w*"),
    "sr": (r"\bsr\b", r"\bserbian\b", r"\bсербск\w*"),
    "hr": (r"\bhr\b", r"\bcroatian\b", r"\bхорватск\w*"),
    "ru": (r"\bru\b", r"\brussian\b", r"\bрусск\w*"),
}
GENERIC_SCOPE_NAMES = {
    "area",
    "cellar",
    "country",
    "district",
    "estate",
    "municipality",
    "podrum",
    "producer",
    "region",
    "rejon",
    "territory",
    "village",
    "vinarija",
    "vinogorje",
    "wine_cellar",
    "wine_district",
    "wine_region",
    "winery",
}
KNOWN_TERRITORY_KEYS = {
    "negotinska_krajina",
}
GENERIC_PRODUCER_QUALIFIERS = {
    "address",
    "building",
    "claims",
    "count",
    "equipment",
    "identity",
    "name",
    "only",
    "order",
    "owner",
    "page",
    "quality",
    "records",
    "reference",
    "register",
    "reputation",
    "sites",
    "style",
    "system_membership",
    "tour",
    "tours",
    "variation",
    "visits",
}
YEAR_PATTERN = re.compile(r"(?<!\d)(?:1\d{3}|20\d{2}|21\d{2})(?!\d)")
EVIDENCE_YEAR_PATTERN = re.compile(
    r"\b(?:award\w*|competition\w*|publication\w*|published\w*|ranking\w*|"
    r"report\w*|selection\w*|source\w*|выбор\w*|конкурс\w*|наград\w*|"
    r"отбор\w*|преми\w*|публикац\w*|рейтинг\w*|стать\w*|источник\w*)\b",
    flags=re.IGNORECASE,
)
COMMON_SECOND_LEVEL_SUFFIXES = {"ac", "co", "com", "edu", "gov", "net", "org"}
MULTI_TENANT_SUFFIXES = {
    "blogspot.com",
    "github.io",
    "medium.com",
    "substack.com",
    "wordpress.com",
}


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {error.msg}") from error
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            records.append(record)
    return records


def load_source_policy(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        policy = json.load(handle)
    if not isinstance(policy, dict):
        raise ValueError(f"{path}: expected a JSON object")
    tier_order = policy.get("tier_order")
    if not isinstance(tier_order, list) or not all(
        isinstance(tier, str) for tier in tier_order
    ):
        raise ValueError(f"{path}: tier_order must be a list of strings")
    exact_tier_overrides = policy.get("exact_tier_overrides", {})
    if not isinstance(exact_tier_overrides, dict):
        raise ValueError(f"{path}: exact_tier_overrides must be an object")
    normalized_overrides: dict[str, str] = {}
    for resource_name, tier in exact_tier_overrides.items():
        normalized_resource = _normalize_token(resource_name)
        if not normalized_resource:
            raise ValueError(
                f"{path}: exact_tier_overrides contains an empty resource name"
            )
        if not isinstance(tier, str) or tier not in tier_order:
            raise ValueError(
                f"{path}: exact_tier_overrides[{resource_name!r}] has unknown tier {tier!r}"
            )
        normalized_overrides[normalized_resource] = tier
    policy["exact_tier_overrides"] = normalized_overrides
    return policy


def _normalize_token(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).casefold()
    text = "".join(character for character in text if not unicodedata.combining(character))
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def _contains_token(resource: str, token: str) -> bool:
    normalized = _normalize_token(token)
    if not normalized:
        return False
    return normalized in resource


def _independence_for(resource: str, policy: dict) -> str:
    exact = policy.get("independence_overrides", {})
    if resource in exact:
        return str(exact[resource])
    token_overrides = policy.get("independence_token_overrides", {})
    for token in sorted(token_overrides, key=len, reverse=True):
        if _contains_token(resource, token):
            return str(token_overrides[token])
    return "editorially_independent"


def classify_source(source: dict, policy: dict) -> dict:
    resource = _normalize_token(source.get("resource"))
    relation = _normalize_token(source.get("relation"))
    wikipedia_resource = _normalize_token(policy["wikipedia_resource"])
    if resource == wikipedia_resource:
        return {
            "tier": "wikipedia",
            "independence": "encyclopedic_secondary",
            "competence": "within_encyclopedic_scope",
            "needs_policy_review": False,
        }

    exact_tier = policy.get("exact_tier_overrides", {}).get(resource)
    if exact_tier is not None:
        return {
            "tier": exact_tier,
            "independence": _independence_for(resource, policy),
            "competence": policy.get("relation_rules", {}).get(
                relation, "role_unspecified"
            ),
            "needs_policy_review": False,
        }

    for tier, policy_key in (
        ("authoritative", "authoritative_tokens"),
        ("specialist", "specialist_tokens"),
        ("limited", "limited_tokens"),
        ("weak", "weak_tokens"),
    ):
        if any(_contains_token(resource, token) for token in policy[policy_key]):
            return {
                "tier": tier,
                "independence": _independence_for(resource, policy),
                "competence": policy.get("relation_rules", {}).get(
                    relation, "role_unspecified"
                ),
                "needs_policy_review": False,
            }

    return {
        "tier": "weak",
        "independence": "unknown",
        "competence": "role_unspecified",
        "needs_policy_review": True,
    }


def _canonical_url(value: str) -> str:
    parsed = urlsplit(value.strip().rstrip(".)]}>\"'"))
    scheme = parsed.scheme.casefold() or "https"
    host = (parsed.hostname or "").casefold()
    port = parsed.port
    netloc = host if port is None else f"{host}:{port}"
    path = re.sub(r"/+", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((scheme, netloc, path, parsed.query, ""))


def _content_fingerprint(source: dict) -> str:
    title = _normalize_token(source.get("title"))
    for marker in ("translated", "translation", "reprint", "republished"):
        title = title.replace(marker, "")
    summary = _normalize_token(source.get("summary"))
    payload = f"{title.strip('_')}|{summary}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:20]


def _url_lineage_key(value: str) -> str:
    canonical_url = _canonical_url(value)
    host = (urlsplit(canonical_url).hostname or "").casefold()
    if host.endswith(".wikipedia.org"):
        return f"wikipedia:{host.split('.', maxsplit=1)[0]}"
    if host in {"doi.org", "dx.doi.org"}:
        return f"url:{canonical_url}"
    publisher_host = host.removeprefix("www.")
    labels = publisher_host.split(".")
    if any(publisher_host.endswith(f".{suffix}") for suffix in MULTI_TENANT_SUFFIXES):
        publisher_domain = ".".join(labels[-3:])
    elif (
        len(labels) >= 3
        and len(labels[-1]) == 2
        and labels[-2] in COMMON_SECOND_LEVEL_SUFFIXES
    ):
        publisher_domain = ".".join(labels[-3:])
    elif len(labels) >= 2:
        publisher_domain = ".".join(labels[-2:])
    else:
        publisher_domain = publisher_host
    return f"publisher:{publisher_domain}"


def source_lineage_key(source: dict) -> str:
    provenance = str(source.get("provenance") or "")
    provenance_folded = provenance.casefold()
    wikipedia_parent = WIKIPEDIA_TRANSLATION_PATTERN.search(provenance)
    if wikipedia_parent:
        return f"wikipedia:{wikipedia_parent.group(1).casefold()}"
    if any(marker in provenance_folded for marker in TRANSLATION_MARKERS):
        match = URL_PATTERN.search(provenance)
        if match:
            return _url_lineage_key(match.group(0))

    url = str(source.get("url") or "").strip()
    if url:
        return _url_lineage_key(url)

    return f"content:{_content_fingerprint(source)}"


def build_source_profiles(sources: list[dict], policy: dict) -> dict[str, dict]:
    profiles: dict[str, dict] = {}
    tier_order = {tier: index for index, tier in enumerate(policy["tier_order"])}
    for source in sources:
        assessment = classify_source(source, policy)
        lineage = source_lineage_key(source)
        for claim_id in source.get("claim_ids", []):
            profile = profiles.setdefault(
                claim_id,
                {
                    "tiers": set(),
                    "lineages": set(),
                    "unknown_source_ids": [],
                    "sources": [],
                },
            )
            profile["tiers"].add(assessment["tier"])
            profile["lineages"].add(lineage)
            if assessment["needs_policy_review"]:
                profile["unknown_source_ids"].append(source.get("source_id"))
            profile["sources"].append(
                {
                    "source_id": source.get("source_id"),
                    "lineage": lineage,
                    "resource": source.get("resource"),
                    "relation": source.get("relation"),
                    "language": source.get("language"),
                    **assessment,
                }
            )

    finalized: dict[str, dict] = {}
    for claim_id, profile in profiles.items():
        finalized[claim_id] = {
            "tiers": sorted(profile["tiers"], key=lambda tier: tier_order[tier]),
            "independent_lineages": len(profile["lineages"]),
            "lineages": sorted(profile["lineages"]),
            "unknown_source_ids": sorted(
                source_id for source_id in profile["unknown_source_ids"] if source_id
            ),
            "sources": profile["sources"],
        }
    return finalized


def _normalize_fact_token(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).casefold()
    text = "".join(character for character in text if not unicodedata.combining(character))
    return re.sub(r"[^\w]+", "_", text, flags=re.UNICODE).strip("_")


def normalize_keys(claim: dict) -> frozenset[str]:
    return frozenset(
        normalized
        for value in claim.get("entity_keys", [])
        if (normalized := _normalize_fact_token(value))
    )


def _property_for(claim: dict, keys: frozenset[str]) -> str:
    category = _normalize_fact_token(claim.get("category"))
    searchable = {category, *keys}
    for canonical, aliases in PROPERTY_ALIASES.items():
        if any(
            alias == value or alias in value.split("_")
            for alias in aliases
            for value in searchable
        ):
            return canonical
    return category


def _is_territory_key(key: str) -> bool:
    if key in GENERIC_SCOPE_NAMES:
        return False
    if key in KNOWN_TERRITORY_KEYS:
        return True
    if re.search(
        r"_(?:wine_)?(?:districts?|regions?|territor(?:y|ies)|municipalit(?:y|ies)|villages?|vinogorje|rejon)$",
        key,
    ):
        return True
    prefix_match = re.match(
        r"^(?:country|district|region|territory|municipality|village)_(.+)$",
        key,
    )
    return bool(prefix_match and prefix_match.group(1) not in {"of_origin", "rank", "count"})


def _is_producer_key(key: str) -> bool:
    if key in GENERIC_SCOPE_NAMES:
        return False
    suffix_match = re.match(r"^(.+)_(?:winery|estate|cellar|producer)$", key)
    if suffix_match:
        subject = suffix_match.group(1)
        return subject not in {
            "current",
            "family",
            "historic",
            "official",
            "royal",
            "small",
            "traditional",
            "wine",
            "young",
        }
    prefix_match = re.match(r"^(?:podrum|vinarija|winery|estate|cellar|producer)_(.+)$", key)
    return bool(
        prefix_match and prefix_match.group(1) not in GENERIC_PRODUCER_QUALIFIERS
    )


def _canonical_measurement_unit(value: str) -> str | None:
    token = _normalize_fact_token(value)
    if token in {"t", "т"} or token.startswith(("ton", "тонн")):
        return "tonne"
    if token in {"hl", "гл"} or token.startswith(("hectolit", "гектолит")):
        return "hectolitre"
    if token in {"l", "л"} or token.startswith(("lit", "литр")):
        return "litre"
    if token in {"kg", "кг"} or token.startswith(("kilogram", "килограмм")):
        return "kilogram"
    if token in {"g", "г"} or token.startswith(("gram", "грамм")):
        return "gram"
    if token in {"ha", "га"} or token.startswith(("hectare", "гектар")):
        return "hectare"
    if token in {"km", "км"} or token.startswith(("kilomet", "километр")):
        return "kilometre"
    if token in {"m", "м"} or token.startswith(("met", "метр")):
        return "metre"
    if token in {"mm", "мм"} or token.startswith(("millimet", "миллиметр")):
        return "millimetre"
    if token in {"c", "°c"} or token.startswith(("celsius", "градус")):
        return "celsius"
    if token in {"percent", "процент"} or value == "%":
        return "percent"
    if token.startswith(("point", "балл")):
        return "point"
    if token.startswith(("bottle", "бутыл")):
        return "bottle"
    if token in {"bar", "бар"}:
        return "bar"
    return None


def _extract_measurements(raw_text: str) -> list[dict[str, str]]:
    unit_expression = (
        r"ton(?:ne)?s?|тонн\w*|[тt](?=\s*/)|"
        r"hectolit(?:er|re)s?|гектолитр\w*|[гh][лl]|"
        r"lit(?:er|re)s?|литр\w*|[лl]|"
        r"kilograms?|килограмм\w*|[кk][гg]|grams?|грамм\w*|[гg](?=\s*/\s*[лl])|"
        r"hectares?|гектар\w*|ha|га|kilomet(?:er|re)s?|километр\w*|km|км|"
        r"millimet(?:er|re)s?|миллиметр\w*|mm|мм|met(?:er|re)s?|метр\w*|m|м|"
        r"°\s*[cс]|celsius|градус\w*|%|percent|процент\w*|"
        r"points?|балл\w*|bottles?|бутыл\w*|bar|бар"
    )
    pattern = re.compile(
        rf"(?<![\w.])(?P<value>\d+(?:[.,]\d+)?)\s*(?P<unit>{unit_expression})"
        rf"(?P<denominator>\s*/\s*(?:ha|га|l|л))?(?!\w)",
        flags=re.IGNORECASE,
    )
    measurements: set[tuple[str, str, str]] = set()
    for match in pattern.finditer(raw_text):
        unit = _canonical_measurement_unit(match.group("unit"))
        if not unit:
            continue
        denominator_text = _normalize_fact_token(match.group("denominator"))
        denominator = ""
        if denominator_text in {"ha", "га"}:
            denominator = "per_hectare"
        elif denominator_text in {"l", "л"}:
            denominator = "per_litre"
        value = match.group("value").replace(",", ".")
        measurements.add((value, unit, denominator))
    return [
        {"value": value, "unit": unit, "denominator": denominator}
        for value, unit, denominator in sorted(measurements)
    ]


def _year_is_measurement_value(text: str, match: re.Match[str]) -> bool:
    suffix = text[match.end() : match.end() + 32]
    return bool(
        re.match(
            r"^[\s_/-]*(?:(?:about|approximately|own|registered|общ\w*|примерн\w*|"
            r"собственн\w*|зарегистрированн\w*)[\s_/-]+)?"
            r"(?:ton(?:ne)?s?|тонн\w*|hectolit(?:er|re)s?|гектолитр\w*|"
            r"lit(?:er|re)s?|литр\w*|kilograms?|килограмм\w*|grams?|грамм\w*|"
            r"hectares?|гектар\w*|ha|га|kilomet(?:er|re)s?|километр\w*|km|км|"
            r"millimet(?:er|re)s?|миллиметр\w*|mm|мм|met(?:er|re)s?|метр\w*|m|м)\b",
            suffix,
            flags=re.IGNORECASE,
        )
    )


def _extract_scope_years(claim: dict) -> list[str]:
    key_years: set[str] = set()
    for key in claim.get("entity_keys", []):
        normalized_key = _normalize_fact_token(key).replace("_", " ")
        if EVIDENCE_YEAR_PATTERN.search(normalized_key):
            continue
        key_text = str(key)
        key_years.update(
            match.group(0)
            for match in YEAR_PATTERN.finditer(key_text)
            if not _year_is_measurement_value(key_text, match)
        )

    narrative = " ".join(
        str(claim.get(field) or "") for field in ("statement", "book_quote", "category")
    )
    years = set(key_years)
    for match in YEAR_PATTERN.finditer(narrative):
        year = match.group(0)
        if year in key_years:
            continue
        if _year_is_measurement_value(narrative, match):
            continue
        window = narrative[max(0, match.start() - 40) : match.end() + 40]
        if EVIDENCE_YEAR_PATTERN.search(window):
            continue
        years.add(year)
    return sorted(years)


def fact_signature(claim: dict) -> dict:
    keys = normalize_keys(claim)
    raw_text = " ".join(
        str(value or "")
        for value in (
            *claim.get("entity_keys", []),
            claim.get("statement"),
            claim.get("book_quote"),
            claim.get("category"),
        )
    )
    folded = _normalize_fact_token(raw_text)
    years = _extract_scope_years(claim)

    unit_patterns = {
        "tonne": (
            r"\bton(?:ne)?s?\b",
            r"\bтонн\w*\b",
            r"\bт\s*/\s*га\b",
            r"\bt\s*/\s*ha\b",
        ),
        "hectolitre": (
            r"\bhectolit(?:er|re)s?\b",
            r"\bhl\b",
            r"\bгектолитр\w*\b",
            r"\bгл\b",
        ),
        "kilogram": (r"\bkilograms?\b", r"\bkg\b", r"\bкг\b", r"\bкилограмм\w*\b"),
        "gram": (r"\bgrams?\b", r"\bграмм\w*\b", r"\b[гg]\s*/\s*[лl]\b"),
        "litre": (r"\blit(?:er|re)s?\b", r"\bлитр\w*\b"),
        "percent": (r"%", r"\bpercent\b", r"\bпроцент\w*\b"),
        "hectare": (r"\bhectares?\b", r"\bha\b", r"\bгектар\w*\b"),
        "kilometre": (r"\bkilomet(?:er|re)s?\b", r"\bkm\b", r"\bкм\b", r"\bкилометр\w*\b"),
        "millimetre": (r"\bmillimet(?:er|re)s?\b", r"\bmm\b", r"\bмм\b", r"\bмиллиметр\w*\b"),
        "metre": (r"\bmet(?:er|re)s?\b", r"\bметр\w*\b"),
        "celsius": (r"°\s*[cс]", r"\bcelsius\b", r"\bградус\w*\b"),
        "point": (r"\bpoints?\b", r"\bбалл\w*\b"),
        "bottle": (r"\bbottles?\b", r"\bбутыл\w*\b"),
        "bar": (r"\bbar\b", r"\bбар\b"),
    }
    units = sorted(
        unit
        for unit, patterns in unit_patterns.items()
        if any(re.search(pattern, raw_text, flags=re.IGNORECASE) for pattern in patterns)
    )

    measurements = _extract_measurements(raw_text)
    units = sorted(set(units) | {measurement["unit"] for measurement in measurements})
    denominators: set[str] = {
        measurement["denominator"]
        for measurement in measurements
        if measurement["denominator"]
    }
    if (
        re.search(r"(?:per|po)[-_ ]hectare", raw_text, flags=re.IGNORECASE)
        or re.search(r"(?:с|на)\s+гектар\w*", raw_text, flags=re.IGNORECASE)
        or re.search(r"(?:\w+|%)\s*/\s*(?:га|ha)\b", raw_text, flags=re.IGNORECASE)
        or "per_hectare" in folded
    ):
        denominators.add("per_hectare")
    if re.search(r"\b(?:total|overall|общ\w*|всего)\b", raw_text, flags=re.IGNORECASE):
        denominators.add("total")

    vintages = sorted(
        year
        for year in years
        if re.search(
            rf"(?:vintage|винтаж|берб\w*)[^\d]{{0,16}}{year}|{year}[^\w]{{0,8}}(?:vintage|винтаж|берб\w*)",
            raw_text,
            flags=re.IGNORECASE,
        )
    )
    object_keys = sorted(
        key
        for key in keys
        if key not in GENERIC_ENTITY_KEYS
        and key not in PROPERTY_TOKENS
        and not re.fullmatch(r"\d+(?:_\d+)?", key)
        and not _is_territory_key(key)
        and not _is_producer_key(key)
        and key not in {"per_hectare", "total"}
    )
    named_entity_keys = sorted(
        key
        for key in keys
        if key not in GENERIC_ENTITY_KEYS
        and key not in GENERIC_TOPIC_KEYS
        and key not in PROPERTY_TOKENS
        and not re.fullmatch(r"\d+(?:_\d+)?", key)
        and key not in {"per_hectare", "total"}
    )
    return {
        "keys": sorted(keys),
        "object_keys": object_keys,
        "named_entity_keys": named_entity_keys,
        "property": _property_for(claim, keys),
        "years": years,
        "vintages": vintages,
        "units": units,
        "denominators": sorted(denominators),
        "measurements": measurements,
        "territories": sorted(key for key in keys if _is_territory_key(key)),
        "producers": sorted(key for key in keys if _is_producer_key(key)),
    }


def _claim_sort_key(claim_id: object) -> tuple[int, str]:
    value = str(claim_id or "")
    match = re.search(r"\d+", value)
    return (int(match.group(0)) if match else 10**12, value)


def _scope_compatible(left: dict, right: dict) -> bool:
    # An omitted scope is intentionally a wildcard: broad and scoped versions of
    # one fact must reach manual review, where they can be resolved as coverage
    # differences. Two explicit, incompatible scopes are never clustered.
    for field in ("years", "vintages", "units", "denominators", "territories", "producers"):
        left_values = set(left[field])
        right_values = set(right[field])
        if left_values and right_values and left_values != right_values:
            return False
    return True


def _near_duplicate(left: dict, right: dict) -> bool:
    left_objects = set(left["object_keys"])
    right_objects = set(right["object_keys"])
    overlap = left_objects & right_objects
    if len(overlap) < 2:
        return False
    if len(overlap) / min(len(left_objects), len(right_objects)) < 0.75:
        return False
    if left_objects - right_objects and right_objects - left_objects:
        return False
    if not left["property"] or left["property"] != right["property"]:
        return False
    return _scope_compatible(left, right)


def duplicate_candidates(claims: list[dict]) -> list[dict]:
    ordered_claims = sorted(claims, key=lambda claim: _claim_sort_key(claim.get("claim_id")))
    signatures = {
        str(claim.get("claim_id")): fact_signature(claim) for claim in ordered_claims
    }
    adjacency: dict[str, set[str]] = defaultdict(set)

    def add_edge(left_id: str, right_id: str) -> None:
        adjacency[left_id].add(right_id)
        adjacency[right_id].add(left_id)

    exact_groups: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for claim in ordered_claims:
        claim_id = str(claim.get("claim_id"))
        fingerprint = tuple(signatures[claim_id]["keys"])
        if len(fingerprint) >= 2:
            exact_groups[fingerprint].append(claim_id)
    for claim_ids in exact_groups.values():
        for left_id, right_id in itertools.combinations(claim_ids, 2):
            if _scope_compatible(signatures[left_id], signatures[right_id]):
                add_edge(left_id, right_id)

    object_index: dict[str, list[str]] = defaultdict(list)
    for claim_id, signature in signatures.items():
        for key in signature["object_keys"]:
            object_index[key].append(claim_id)
    overlap_counts: dict[tuple[str, str], int] = defaultdict(int)
    for claim_ids in object_index.values():
        for left_id, right_id in itertools.combinations(
            sorted(set(claim_ids), key=_claim_sort_key), 2
        ):
            overlap_counts[(left_id, right_id)] += 1

    for (left_id, right_id), overlap_count in overlap_counts.items():
        if overlap_count < 2:
            continue
        left = signatures[left_id]
        right = signatures[right_id]
        if not _near_duplicate(left, right):
            continue
        add_edge(left_id, right_id)

    maximal_cliques: list[set[str]] = []

    def visit_cliques(selected: set[str], possible: set[str], excluded: set[str]) -> None:
        if not possible and not excluded:
            if len(selected) >= 2:
                maximal_cliques.append(set(selected))
            return
        pivot_pool = possible | excluded
        if pivot_pool:
            pivot = min(
                pivot_pool,
                key=lambda claim_id: (
                    -len(possible & adjacency[claim_id]),
                    _claim_sort_key(claim_id),
                ),
            )
            branch_vertices = possible - adjacency[pivot]
        else:
            branch_vertices = set(possible)
        for claim_id in sorted(branch_vertices, key=_claim_sort_key):
            neighbours = adjacency[claim_id]
            visit_cliques(
                selected | {claim_id},
                possible & neighbours,
                excluded & neighbours,
            )
            possible.remove(claim_id)
            excluded.add(claim_id)

    duplicate_ids = {
        claim_id for claim_id, neighbours in adjacency.items() if neighbours
    }
    visit_cliques(set(), set(duplicate_ids), set())

    candidates: list[dict] = []
    for claim_ids in maximal_cliques:
        sorted_ids = sorted(claim_ids, key=_claim_sort_key)
        fingerprints = {
            tuple(signatures[claim_id]["keys"]) for claim_id in sorted_ids
        }
        match = "exact" if len(fingerprints) == 1 else "near"
        if match == "exact":
            shared_keys = list(next(iter(fingerprints)))
        else:
            shared = set(signatures[sorted_ids[0]]["object_keys"])
            for claim_id in sorted_ids[1:]:
                shared.intersection_update(signatures[claim_id]["object_keys"])
            shared_keys = sorted(shared)
        candidates.append(
            {
                "kind": "смысловой повтор",
                "match": match,
                "claim_ids": sorted_ids,
                "shared_keys": shared_keys,
                "risk_reasons": [],
            }
        )

    return sorted(
        candidates,
        key=lambda candidate: (
            _claim_sort_key(candidate["claim_ids"][0]),
            0 if candidate["match"] == "exact" else 1,
            tuple(_claim_sort_key(claim_id) for claim_id in candidate["claim_ids"]),
        ),
    )


def _source_supports_fact(source: dict) -> bool:
    relation = _normalize_fact_token(source.get("relation"))
    if not relation:
        return False
    if any(marker in relation for marker in NEGATIVE_RELATION_MARKERS):
        return False
    return any(marker in relation for marker in POSITIVE_RELATION_MARKERS)


def _is_decisive_source(source: dict, claim: dict) -> bool:
    if source.get("tier") != "authoritative":
        return False
    resource = _normalize_token(source.get("resource"))
    property_name = fact_signature(claim)["property"]
    claim_text = _normalize_fact_token(_claim_text(claim)).replace("_", " ")

    if any(marker in resource for marker in DECISIVE_REGISTRY_MARKERS):
        return property_name in {"identity", "origin"} or bool(
            re.search(
                r"\b(?:identity|name|synonym|origin|parentage|pedigree|cross\w*|"
                r"идентичн\w*|назван\w*|синоним\w*|происхожд\w*|родословн\w*|"
                r"родител\w*|скрещиван\w*)\b",
                claim_text,
                flags=re.IGNORECASE,
            )
        )

    if any(marker in resource for marker in DECISIVE_COMPETITION_MARKERS):
        return bool(
            re.search(
                r"\b(?:award\w*|competition\w*|medal\w*|prize\w*|score\w*|"
                r"winner\w*|наград\w*|конкурс\w*|медал\w*|преми\w*|балл\w*|"
                r"победител\w*)\b",
                claim_text,
                flags=re.IGNORECASE,
            )
        )

    if any(marker in resource for marker in DECISIVE_LEGAL_MARKERS):
        if "official_regional_specification" in resource or "government_zoning" in resource:
            if property_name == "geography":
                return True
        return property_name == "law" or bool(
            re.search(
                r"\b(?:law|legal|regulation\w*|rulebook|protected|official zoning|"
                r"appellation|закон\w*|регламент\w*|право|правов\w*|маркировк\w*|"
                r"защищенн\w*|районир\w*|официальн\w* зон\w*)\b",
                claim_text,
                flags=re.IGNORECASE,
            )
        )

    if any(marker in resource for marker in DECISIVE_STATISTICS_MARKERS):
        return bool(re.search(r"\d", claim_text)) and bool(
            re.search(
                r"\b(?:statistic\w*|census|official count|area|production|yield|"
                r"статистик\w*|перепис\w*|площад\w*|производств\w*|урожай\w*|"
                r"количеств\w*)\b",
                claim_text,
                flags=re.IGNORECASE,
            )
        )

    if any(marker in resource for marker in DECISIVE_STANDARD_MARKERS):
        return bool(
            re.search(
                r"\b(?:definition|standard|classification|category|method\w*|process|"
                r"определен\w*|дефиниц\w*|стандарт\w*|классификац\w*|категор\w*|"
                r"метод\w*|процесс\w*)\b",
                claim_text,
                flags=re.IGNORECASE,
            )
        )

    return False


def _source_sufficiency(claim: dict, source_profile: dict) -> str:
    strong_tiers = {"authoritative", "specialist"}
    disallowed_independence = {"commercial_secondary", "interested_primary", "unknown"}
    supporting_sources: list[dict] = []
    for source in source_profile.get("sources", []):
        if source.get("tier") not in strong_tiers:
            continue
        if source.get("competence") == "interested_only":
            continue
        if source.get("independence") in disallowed_independence:
            continue
        if not _source_supports_fact(source):
            continue
        supporting_sources.append(source)

    if any(_is_decisive_source(source, claim) for source in supporting_sources):
        return "strong"
    lineages = {
        str(source.get("lineage") or source.get("source_id"))
        for source in supporting_sources
        if source.get("lineage") or source.get("source_id")
    }
    if len(lineages) >= 2:
        return "strong"
    if source_profile.get("unknown_source_ids"):
        return "unknown"
    return "weak"


def _claim_text(claim: dict) -> str:
    return " ".join(
        str(value or "")
        for value in (
            claim.get("statement"),
            claim.get("book_quote"),
            claim.get("category"),
            *claim.get("entity_keys", []),
        )
    )


def _is_high_risk_fact(claim: dict) -> bool:
    text = _normalize_fact_token(_claim_text(claim)).replace("_", " ")
    patterns = (
        r"\d",
        r"\b(?:law|legal|regulation\w*|rulebook|decree|edict|excise|customs|food safety control|control points|declaration|protected geographical name|protected designation|закон\w*|регламент\w*|регулир\w*|указ\w*|право|правов\w*|маркировк\w*|защищенн\w* географическ\w* наименован\w*|акциз\w*|тамож\w*|пограничн\w*)\b",
        r"\b(?:award\w*|prize\w*|medal\w*|record\w*|first|преми\w*|наград\w*|медал\w*|рекорд\w*|первенств\w*|перв(?:ый|ая|ое|ые|ого|ой|ых|ому|ым|ую|ыми|ом))\b",
        r"\b(?:origin|parentage|pedigree|ancestor|cross|crossed|crossing|breed\w*|происхожд\w*|родословн\w*|родств\w*|родител\w*|скрещиван\w*|селекц\w*)\b",
        r"\b(?:official zoning|zoning|wine district\w*|wine region\w*|viticultural zone\w*|appellation|protected designation|районир\w*|официальн\w* (?:винодельческ\w*|виноградск\w*|виноградарск\w*) район\w*|классификац\w* зон\w*)\b",
        r"\b(?:caused|led to|because of|due to|вызван\w*|обусловлен\w*|причин\w*|привел\w*|привёл\w*|благодаря|из за|вследствие)\b",
    )
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _is_categorical(claim: dict) -> bool:
    return bool(
        re.search(
            r"\b(?:first|only|always|never|most|unique|largest|oldest|best|highest|lowest|earliest|latest|перв(?:ый|ая|ое|ые|ого|ой|ых|ому|ым|ую|ыми|ом)|единственн\w*|всегда|никогда|только|сам(?:ый|ая|ое|ые|ого|ой|ых|ому|ым|ую|ыми|ом)|крупнейш\w*|старейш\w*|лучш\w*|наибольш\w*|наиболее)\b",
            _claim_text(claim),
            flags=re.IGNORECASE,
        )
    )


def _wikipedia_languages_in_text(text: str) -> set[str]:
    languages: set[str] = set()
    for language, patterns in LANGUAGE_MARKERS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                window = text[max(0, match.start() - 50) : match.end() + 50]
                sentence_start = max(
                    text.rfind(delimiter, 0, match.start())
                    for delimiter in (".", "!", "?", ";", "\n")
                )
                sentence_ends = [
                    position
                    for delimiter in (".", "!", "?", ";", "\n")
                    if (position := text.find(delimiter, match.end())) >= 0
                ]
                sentence_end = min(sentence_ends) if sentence_ends else len(text)
                sentence = text[sentence_start + 1 : sentence_end]
                if re.search(r"wikiped|википед", sentence, flags=re.IGNORECASE) or re.search(
                    rf"{pattern}[^.;:]{{0,30}}(?:article|edition|version|стать\w*|верси\w*)",
                    window,
                    flags=re.IGNORECASE,
                ):
                    languages.add(language)
                    break
            if language in languages:
                break
    return languages


def _has_wikipedia_disagreement(
    claim: dict, decision: dict, source_profile: dict
) -> bool:
    if decision.get("status") == "между Википедиями нет согласия":
        return True

    wikipedia_sources = [
        source
        for source in source_profile.get("sources", [])
        if source.get("tier") == "wikipedia"
    ]
    wikipedia_languages = {
        str(source.get("language"))
        for source in wikipedia_sources
        if source.get("language")
    }
    if len(wikipedia_languages) < 2:
        return False

    decision_text = " ".join(
        str(decision.get(field) or "") for field in ("comparison", "independence")
    ).casefold()
    if not re.search(r"wikiped|википед", decision_text):
        return False
    if re.search(
        r"(?:wikiped\w*|википед\w*)[^.]{0,100}(?:no comparable|no relevant|do not (?:give|provide)|does not (?:give|provide)|не (?:дают|даёт|дает|содержат)|нет|отсутств\w*)",
        decision_text,
        flags=re.IGNORECASE,
    ):
        return False
    mentioned_languages = _wikipedia_languages_in_text(decision_text)
    mentioned_languages.intersection_update(wikipedia_languages)
    if len(mentioned_languages) < 2:
        return False

    structural_contrast = re.compile(
        r"\b(?:while|whereas|conflict\w*|disagree\w*|тогда как|напротив|расход\w*|противореч\w*|устарел\w*)\b",
        flags=re.IGNORECASE,
    )
    for match in structural_contrast.finditer(decision_text):
        before_text = decision_text[max(0, match.start() - 240) : match.start()]
        after_text = decision_text[match.end() : match.end() + 240]
        before_languages = _wikipedia_languages_in_text(before_text)
        after_languages = _wikipedia_languages_in_text(after_text)
        before_languages.update(
            language
            for language, patterns in LANGUAGE_MARKERS.items()
            if re.search(patterns[0], before_text, flags=re.IGNORECASE)
        )
        after_languages.update(
            language
            for language, patterns in LANGUAGE_MARKERS.items()
            if re.search(patterns[0], after_text, flags=re.IGNORECASE)
        )
        before_languages.intersection_update(wikipedia_languages)
        after_languages.intersection_update(wikipedia_languages)
        if before_languages and after_languages and before_languages != after_languages:
            return True

    parameter_conflict = re.search(
        r"(?:числ\w*\s+диапазон\w*|высот\w*|температур\w*|направлен\w*)\s+различ\w*|различ\w*\s+(?:в\s+направлен\w*|по\s+(?:высот\w*|температур\w*))",
        decision_text,
        flags=re.IGNORECASE,
    )
    if parameter_conflict:
        return True

    if decision.get("consensus") != "конфликт":
        return False
    property_name = fact_signature(claim)["property"]
    topic_markers = {
        "identity": ("identity", "name", "synonym"),
        "origin": ("ancestry", "origin", "parentage"),
        "chronology": ("chronology", "date", "period"),
        "geography": ("altitude", "geography", "location"),
        "law": ("law", "legal", "regulation"),
    }.get(property_name, ())
    return bool(
        topic_markers
        and any(
            source.get("tier") == "wikipedia"
            and any(
                conflict_marker in _normalize_fact_token(source.get("relation"))
                for conflict_marker in ("conflict", "contradiction", "disagreement")
            )
            and any(
                topic_marker in _normalize_fact_token(source.get("relation"))
                for topic_marker in topic_markers
            )
            for source in wikipedia_sources
        )
    )


def risk_reasons(claim: dict, decision: dict, source_profile: dict) -> list[str]:
    reasons: set[str] = set()
    status = decision.get("status")
    consensus = decision.get("consensus")
    if _has_wikipedia_disagreement(claim, decision, source_profile):
        reasons.add("wikipedia_disagreement")
    if status == "в Википедиях отсутствует":
        reasons.add("wikipedia_absence")
    if status in DISPUTED_STATUSES:
        reasons.add("disputed_status")
    if consensus != "высокий":
        reasons.add("non_high_consensus")
    if consensus == "высокий" and _source_sufficiency(claim, source_profile) == "weak":
        reasons.add("high_consensus_without_strong_source")
    if _is_high_risk_fact(claim):
        reasons.add("high_risk_fact_type")
    if _is_categorical(claim):
        reasons.add("categorical_or_superlative")
    if source_profile.get("unknown_source_ids"):
        reasons.add("unknown_source_classification")
    return [reason for reason in RISK_REASON_ORDER if reason in reasons]


def _empty_source_profile() -> dict:
    return {
        "tiers": [],
        "independent_lineages": 0,
        "lineages": [],
        "unknown_source_ids": [],
        "sources": [],
    }


def _claim_number(claim_id: object) -> int:
    return _claim_sort_key(claim_id)[0]


def _build_late_source_index(
    claims: list[dict], sources: list[dict], policy: dict
) -> dict[tuple[str, str], list[dict]]:
    claims_by_id = {str(claim.get("claim_id")): claim for claim in claims}
    resource_first_claim: dict[str, int] = {}
    for source in sources:
        resource = _normalize_token(source.get("resource"))
        numbers = [
            _claim_number(claim_id)
            for claim_id in source.get("claim_ids", [])
            if str(claim_id) in claims_by_id
        ]
        if not resource or not numbers:
            continue
        resource_first_claim[resource] = min(
            min(numbers), resource_first_claim.get(resource, 10**12)
        )

    index: dict[tuple[str, str], list[dict]] = defaultdict(list)
    disallowed_independence = {"commercial_secondary", "interested_primary", "unknown"}
    for source in sources:
        assessment = classify_source(source, policy)
        resource_key = _normalize_token(source.get("resource"))
        if assessment["tier"] not in {"authoritative", "specialist"}:
            continue
        if assessment["needs_policy_review"]:
            continue
        if assessment["independence"] in disallowed_independence:
            continue
        if assessment["competence"] == "interested_only":
            continue
        if not _source_supports_fact({**source, **assessment}):
            continue
        for claim_id_value in source.get("claim_ids", []):
            claim_id = str(claim_id_value)
            claim = claims_by_id.get(claim_id)
            if not claim:
                continue
            signature = fact_signature(claim)
            entry = {
                "resource": source.get("resource"),
                "resource_key": resource_key,
                "source_id": source.get("source_id"),
                "later_claim_id": claim_id,
                "later_claim_number": _claim_number(claim_id),
                "first_claim_number": resource_first_claim.get(resource_key, 10**12),
                "tier": assessment["tier"],
            }
            for named_entity_key in signature["named_entity_keys"]:
                index[(signature["property"], named_entity_key)].append(entry)

    for entries in index.values():
        entries.sort(
            key=lambda entry: (
                entry["later_claim_number"],
                str(entry.get("resource") or ""),
                str(entry.get("source_id") or ""),
            )
        )
    return index


def _late_source_matches(
    claim: dict, source_profile: dict, late_source_index: dict[tuple[str, str], list[dict]]
) -> list[dict]:
    claim_number = _claim_number(claim.get("claim_id"))
    signature = fact_signature(claim)
    current_resources = {
        _normalize_token(source.get("resource"))
        for source in source_profile.get("sources", [])
        if source.get("resource")
    }
    matches: dict[str, dict] = {}
    for named_entity_key in signature["named_entity_keys"]:
        for entry in late_source_index.get(
            (signature["property"], named_entity_key), []
        ):
            if entry["first_claim_number"] - claim_number < 250:
                continue
            if entry["later_claim_number"] - claim_number < 250:
                continue
            if entry["resource_key"] in current_resources:
                continue
            match_key = str(entry.get("resource_key") or "")
            match = matches.setdefault(
                match_key,
                {
                    "resource": entry.get("resource"),
                    "source_id": entry.get("source_id"),
                    "later_claim_id": entry["later_claim_id"],
                    "tier": entry["tier"],
                    "shared_keys": [],
                },
            )
            match["shared_keys"].append(named_entity_key)
    for match in matches.values():
        match["shared_keys"] = sorted(set(match["shared_keys"]))
    return sorted(
        matches.values(),
        key=lambda match: (
            _claim_sort_key(match["later_claim_id"]),
            str(match.get("resource") or ""),
            str(match.get("source_id") or ""),
        ),
    )


def _decision_variance_fields(decisions: list[dict]) -> list[str]:
    fields = ("status", "consensus", "independence", "editor_conclusion")
    return [
        field
        for field in fields
        if len({_normalize_fact_token(decision.get(field)) for decision in decisions}) > 1
    ]


def scan_audit(base_dir: Path, policy_path: Path) -> dict:
    claims = load_jsonl(base_dir / "claims.jsonl")
    decisions = load_jsonl(base_dir / "decisions.jsonl")
    sources = load_jsonl(base_dir / "sources.jsonl")
    decisions_by_id = {
        str(decision.get("claim_id")): decision for decision in decisions
    }
    policy = load_source_policy(policy_path)
    profiles = build_source_profiles(sources, policy)
    late_source_index = _build_late_source_index(claims, sources, policy)

    duplicates = duplicate_candidates(claims)
    for candidate in duplicates:
        member_decisions = [
            decisions_by_id.get(claim_id, {}) for claim_id in candidate["claim_ids"]
        ]
        variance_fields = _decision_variance_fields(member_decisions)
        if variance_fields:
            candidate["risk_reasons"] = ["duplicate_decision_variance"]
            candidate["variance_fields"] = variance_fields

    claim_risks: list[dict] = []
    for claim in sorted(claims, key=lambda item: _claim_sort_key(item.get("claim_id"))):
        claim_id = str(claim.get("claim_id"))
        decision = decisions_by_id.get(claim_id, {})
        profile = profiles.get(claim_id, _empty_source_profile())
        reasons = risk_reasons(claim, decision, profile)
        if not reasons or reasons == ["unknown_source_classification"]:
            continue
        late_matches = _late_source_matches(claim, profile, late_source_index)
        if late_matches:
            reasons = [
                reason
                for reason in RISK_REASON_ORDER
                if reason in {*reasons, "late_source_recheck"}
            ]
        risk_record = {
            "kind": "риск решения",
            "claim_ids": [claim_id],
            "risk_reasons": reasons,
            "source_profile": profile,
            "original_statuses": [
                {
                    "claim_id": claim_id,
                    "status": decision.get("status"),
                    "consensus": decision.get("consensus"),
                }
            ],
        }
        if late_matches:
            risk_record["late_source_matches"] = late_matches
        claim_risks.append(risk_record)

    return {
        "claims": len(claims),
        "decisions": len(decisions),
        "sources": len(sources),
        "duplicates": duplicates,
        "claim_risks": claim_risks,
        "source_profiles": profiles,
        "decisions_by_id": decisions_by_id,
        "source_records": sources,
    }


def _candidate_key(candidate: dict) -> str:
    claim_ids = ",".join(
        sorted((str(claim_id) for claim_id in candidate.get("claim_ids", [])), key=_claim_sort_key)
    )
    if candidate.get("kind") == "смысловой повтор":
        scope = ",".join(sorted(str(key) for key in candidate.get("shared_keys", [])))
        return f"repeat:{claim_ids}:{candidate.get('match', 'unknown')}:{scope}"
    reasons = ",".join(str(reason) for reason in candidate.get("risk_reasons", []))
    return f"risk:{claim_ids}:{reasons}"


def _candidate_sort_key(candidate: dict) -> tuple[tuple[int, str], int, str]:
    claim_ids = candidate.get("claim_ids", [])
    first_claim = min((_claim_sort_key(claim_id) for claim_id in claim_ids), default=(10**12, ""))
    return (
        first_claim,
        0 if candidate.get("kind") == "смысловой повтор" else 1,
        _candidate_key(candidate),
    )


def _candidate_source_profile(candidate: dict, scan: dict) -> dict:
    if candidate.get("source_profile"):
        return candidate["source_profile"]
    profiles = scan.get("source_profiles", {})
    return {
        str(claim_id): profiles.get(str(claim_id), _empty_source_profile())
        for claim_id in candidate.get("claim_ids", [])
    }


def _candidate_original_statuses(candidate: dict, scan: dict) -> list[dict]:
    if "original_statuses" in candidate:
        return candidate["original_statuses"]
    decisions = scan.get("decisions_by_id", {})
    return [
        {
            "claim_id": str(claim_id),
            "status": decisions.get(str(claim_id), {}).get("status"),
            "consensus": decisions.get(str(claim_id), {}).get("consensus"),
        }
        for claim_id in candidate.get("claim_ids", [])
    ]


def _frozen_candidates(scan: dict) -> list[dict]:
    raw_candidates = [*scan.get("duplicates", []), *scan.get("claim_risks", [])]
    candidates: list[dict] = []
    for raw in sorted(raw_candidates, key=_candidate_sort_key):
        candidates.append(
            {
                "candidate_key": _candidate_key(raw),
                "kind": raw.get("kind"),
                "claim_ids": sorted(
                    (str(claim_id) for claim_id in raw.get("claim_ids", [])),
                    key=_claim_sort_key,
                ),
                "risk_reasons": list(raw.get("risk_reasons", [])),
                "source_profile": _candidate_source_profile(raw, scan),
                "original_statuses": _candidate_original_statuses(raw, scan),
            }
        )
    for index, candidate in enumerate(candidates, start=1):
        candidate["meta_id"] = f"M{index:04d}"
    return candidates


def _candidate_validation_errors(candidates: list[dict], strict: bool) -> list[str]:
    errors: list[str] = []
    seen_meta_ids: set[str] = set()
    seen_keys: set[str] = set()
    for index, candidate in enumerate(candidates, start=1):
        if not isinstance(candidate, dict):
            errors.append(f"candidate {index}: expected a JSON object")
            continue
        if strict:
            for field in CANDIDATE_FIELDS:
                if field not in candidate:
                    errors.append(f"candidate {index}: missing {field}")
        meta_id = candidate.get("meta_id")
        if "meta_id" in candidate:
            if not isinstance(meta_id, str):
                errors.append(f"invalid meta_id {meta_id}")
            elif not re.fullmatch(r"M\d{4,}", meta_id):
                errors.append(f"invalid meta_id {meta_id}")
            elif meta_id in seen_meta_ids:
                errors.append(f"duplicate meta_id {meta_id}")
            else:
                seen_meta_ids.add(meta_id)
        elif strict:
            errors.append(f"candidate {index}: empty meta_id")
        key = candidate.get("candidate_key")
        if not isinstance(key, str):
            errors.append("invalid candidate_key")
        elif not key.strip():
            errors.append(f"candidate {index}: empty candidate_key")
        elif key in seen_keys:
            errors.append(f"duplicate candidate_key {key}")
        else:
            seen_keys.add(key)
        claim_ids = candidate.get("claim_ids")
        if strict or "claim_ids" in candidate:
            if not isinstance(claim_ids, list):
                errors.append("invalid claim_ids")
            elif strict and not claim_ids:
                errors.append(f"candidate {key or index}: missing claim_ids")
            elif any(not isinstance(claim_id, str) or not claim_id for claim_id in claim_ids):
                errors.append(f"candidate {key or index}: invalid claim_ids")
        if strict:
            for field in ("kind",):
                if not isinstance(candidate.get(field), str) or not candidate[field].strip():
                    errors.append(f"candidate {key or index}: empty {field}")
            for field in ("risk_reasons", "original_statuses"):
                if not isinstance(candidate.get(field), list):
                    errors.append(f"candidate {key or index}: invalid {field}")
            if not isinstance(candidate.get("source_profile"), dict):
                errors.append(f"candidate {key or index}: invalid source_profile")
    if strict:
        expected_ids = [f"M{index:04d}" for index in range(1, len(candidates) + 1)]
        actual_ids = [candidate.get("meta_id") for candidate in candidates if isinstance(candidate, dict)]
        if actual_ids != expected_ids:
            errors.append("candidate meta_id values must be contiguous from M0001")
    return errors


def write_candidates(scan: dict, path: Path) -> None:
    candidates = _frozen_candidates(scan)
    errors = _candidate_validation_errors(candidates, strict=True)
    if errors:
        raise ValueError("; ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(candidate, ensure_ascii=False, sort_keys=True) + "\n"
            for candidate in candidates
        ),
        encoding="utf-8",
    )


def load_candidates(path: Path) -> list[dict]:
    candidates = load_jsonl(path)
    errors = _candidate_validation_errors(candidates, strict=True)
    if errors:
        raise ValueError("; ".join(errors))
    return candidates


def validate_review(
    candidates: list[dict],
    claim_ids: set[str],
    records: list[dict],
    require_complete: bool,
    source_claim_ids: dict[str, set[str]] | None = None,
) -> list[str]:
    errors = _candidate_validation_errors(candidates, strict=False)
    candidates_by_key = {
        candidate.get("candidate_key"): candidate
        for candidate in candidates
        if isinstance(candidate, dict) and isinstance(candidate.get("candidate_key"), str)
    }
    for candidate in candidates:
        if isinstance(candidate, dict) and isinstance(candidate.get("claim_ids"), list):
            for claim_id in candidate["claim_ids"]:
                if str(claim_id) not in claim_ids:
                    errors.append(f"unknown claim {claim_id}")

    reviewed_keys: set[str] = set()
    prose_fields = ("canonical_question", "scope", "source_weight", "resolution_notes")
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"review {index}: expected a JSON object")
            continue
        for field in REVIEW_FIELDS:
            if field not in record:
                errors.append(f"review {index}: missing {field}")
        key = record.get("candidate_key")
        candidate = candidates_by_key.get(key) if isinstance(key, str) else None
        if not isinstance(key, str):
            errors.append("invalid candidate_key")
        elif not key:
            errors.append("empty candidate_key")
        elif key in reviewed_keys:
            errors.append(f"duplicate review candidate_key {key}")
        else:
            reviewed_keys.add(key)
        if key and candidate is None:
            errors.append(f"unknown candidate {key}")
        for field in prose_fields:
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"empty {field}")
        if not isinstance(record.get("source_lines"), list):
            errors.append("invalid source_lines")
        elif source_claim_ids is not None:
            review_id = record.get("meta_id", index)
            for source_line in record["source_lines"]:
                if not isinstance(source_line, dict):
                    continue
                if isinstance(source_line.get("claim_id"), str):
                    line_claim_ids = [source_line["claim_id"]]
                elif isinstance(source_line.get("claim_ids"), list):
                    line_claim_ids = [str(claim_id) for claim_id in source_line["claim_ids"]]
                else:
                    continue
                for field in ("source_ids", "checked_only_source_ids"):
                    source_ids = source_line.get(field, [])
                    if not isinstance(source_ids, list):
                        continue
                    for source_id in source_ids:
                        source_id = str(source_id)
                        reverse_claim_ids = source_claim_ids.get(source_id)
                        if reverse_claim_ids is None:
                            errors.append(f"review {review_id} source {source_id} is unknown")
                            continue
                        for line_claim_id in line_claim_ids:
                            if line_claim_id not in reverse_claim_ids:
                                errors.append(
                                    f"review {review_id} source {source_id} missing reverse claim {line_claim_id}"
                                )
        if not isinstance(record.get("changes"), list):
            errors.append("invalid changes")
        resolution = record.get("resolution")
        if not isinstance(resolution, str) or resolution not in ALLOWED_RESOLUTIONS:
            errors.append(f"invalid resolution {resolution}")
        if resolution == "остаётся неразрешённым" and (
            not isinstance(record.get("remaining_gap"), str)
            or not record["remaining_gap"].strip()
        ):
            errors.append("empty remaining_gap")
        record_claim_ids = record.get("claim_ids")
        if not isinstance(record_claim_ids, list):
            errors.append("invalid claim_ids")
        else:
            for claim_id in record_claim_ids:
                if str(claim_id) not in claim_ids:
                    errors.append(f"unknown claim {claim_id}")
        if candidate is not None:
            for field in ("meta_id", "kind", "claim_ids", "risk_reasons"):
                if record.get(field) != candidate.get(field):
                    errors.append(f"candidate {key}: {field} does not match frozen candidate")
    if require_complete:
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            key = candidate.get("candidate_key")
            if isinstance(key, str) and key and key not in reviewed_keys:
                errors.append(f"unreviewed candidate {key}")
    return errors


def _claim_band(claim_id: str) -> str:
    claim_number = _claim_number(claim_id)
    band_start = ((claim_number - 1) // 250) * 250 + 1
    return f"C{band_start:04d}-C{band_start + 249:04d}"


def build_baseline(scan: dict, candidates: list[dict]) -> dict:
    status_counts: dict[str, int] = defaultdict(int)
    consensus_counts: dict[str, int] = defaultdict(int)
    source_tier_counts: dict[str, int] = defaultdict(int)
    risk_reason_counts: dict[str, int] = defaultdict(int)
    bands: dict[str, dict] = {}

    def band_counts(band: str) -> dict:
        return bands.setdefault(
            band,
            {
                "candidates": 0,
                "status": defaultdict(int),
                "consensus": defaultdict(int),
                "source_tier": defaultdict(int),
                "risk_reasons": defaultdict(int),
            },
        )

    for claim_id, decision in scan.get("decisions_by_id", {}).items():
        counts = band_counts(_claim_band(str(claim_id)))
        status_counts[str(decision.get("status"))] += 1
        consensus_counts[str(decision.get("consensus"))] += 1
        counts["status"][str(decision.get("status"))] += 1
        counts["consensus"][str(decision.get("consensus"))] += 1
    for claim_id, profile in scan.get("source_profiles", {}).items():
        counts = band_counts(_claim_band(str(claim_id)))
        for tier in profile.get("tiers", []):
            source_tier_counts[str(tier)] += 1
            counts["source_tier"][str(tier)] += 1
    for candidate in candidates:
        claim_ids = candidate.get("claim_ids", [])
        if not claim_ids:
            continue
        band = _claim_band(min((str(claim_id) for claim_id in claim_ids), key=_claim_sort_key))
        counts = band_counts(band)
        counts["candidates"] += 1
        for reason in candidate.get("risk_reasons", []):
            risk_reason_counts[str(reason)] += 1
            counts["risk_reasons"][str(reason)] += 1
    return {
        "claims": scan.get("claims", 0),
        "decisions": scan.get("decisions", 0),
        "sources": scan.get("sources", 0),
        "candidates": len(candidates),
        "by_claim_band": {
            band: {
                "candidates": values["candidates"],
                "status": dict(sorted(values["status"].items())),
                "consensus": dict(sorted(values["consensus"].items())),
                "source_tier": dict(sorted(values["source_tier"].items())),
                "risk_reasons": dict(sorted(values["risk_reasons"].items())),
            }
            for band, values in sorted(bands.items())
        },
        "status": dict(sorted(status_counts.items())),
        "consensus": dict(sorted(consensus_counts.items())),
        "source_tier": dict(sorted(source_tier_counts.items())),
        "risk_reason": dict(sorted(risk_reason_counts.items())),
        "totals": dict(sorted(risk_reason_counts.items())),
    }


def _write_baseline(scan: dict, candidates: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_baseline(scan, candidates), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cross-audit candidate scanner and review validator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("base_dir", type=Path)
    scan_parser.add_argument("--policy", required=True, type=Path)
    scan_parser.add_argument("--candidates", required=True, type=Path)
    scan_parser.add_argument("--baseline", required=True, type=Path)
    review_parser = subparsers.add_parser("validate-review")
    review_parser.add_argument("base_dir", type=Path)
    review_parser.add_argument("--policy", required=True, type=Path)
    review_parser.add_argument("--candidates", required=True, type=Path)
    review_parser.add_argument("--review", required=True, type=Path)
    review_parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "scan":
            scan = scan_audit(args.base_dir, args.policy)
            write_candidates(scan, args.candidates)
            candidates = load_candidates(args.candidates)
            _write_baseline(scan, candidates, args.baseline)
            print(f"wrote {len(candidates)} candidates")
            return 0
        load_source_policy(args.policy)
        candidates = load_candidates(args.candidates)
        claim_ids = {
            str(claim.get("claim_id")) for claim in load_jsonl(args.base_dir / "claims.jsonl")
        }
        source_claim_ids = {
            str(source.get("source_id")): {
                str(claim_id) for claim_id in source.get("claim_ids", [])
            }
            for source in load_jsonl(args.base_dir / "sources.jsonl")
            if isinstance(source.get("source_id"), str)
        }
        records = load_jsonl(args.review) if args.review.exists() else []
        errors = validate_review(
            candidates,
            claim_ids,
            records,
            args.require_complete,
            source_claim_ids,
        )
    except (OSError, ValueError) as error:
        print(str(error), file=__import__("sys").stderr)
        return 2
    if errors:
        print("\n".join(errors), file=__import__("sys").stderr)
        return 1
    print("review validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
