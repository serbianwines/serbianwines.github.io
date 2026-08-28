#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
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


def source_lineage_key(source: dict) -> str:
    provenance = str(source.get("provenance") or "")
    provenance_folded = provenance.casefold()
    wikipedia_parent = WIKIPEDIA_TRANSLATION_PATTERN.search(provenance)
    if wikipedia_parent:
        return f"wikipedia:{wikipedia_parent.group(1).casefold()}"
    if any(marker in provenance_folded for marker in TRANSLATION_MARKERS):
        match = URL_PATTERN.search(provenance)
        if match:
            return f"url:{_canonical_url(match.group(0))}"

    url = str(source.get("url") or "").strip()
    if url:
        host = (urlsplit(url).hostname or "").casefold()
        if host.endswith(".wikipedia.org"):
            return f"wikipedia:{host.split('.', maxsplit=1)[0]}"
        return f"url:{_canonical_url(url)}"

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
