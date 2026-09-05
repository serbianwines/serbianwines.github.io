# Мета-аудит аудита: план выполнения

> **Изменение от 2026-09-05, согласовано пользователем:** дальнейшая работа определяется [планом редакторских приоритетов](2026-09-05-meta-audit-editorial-priority.md). Нижеследующий план сохраняется как история. Обязательный сплошной ручной обход замороженной очереди и повторяющиеся полные циклы review заменены явной сортировкой рисков, сверкой переноса выводов и контролем по влиянию на редакторские решения. Выполнение старого плана не объявляется полным.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** построить воспроизводимый мета-аудит 2 744 решений, устранить настоящие противоречия, ретроспективно усилить спорные и высокорисковые ранние выводы и разрешить пробелы или конфликты Википедий профильными источниками.

**Architecture:** детерминированный Python-анализатор читает существующие JSONL, классифицирует источники по роли, формирует смысловые кластеры и замороженную очередь риска, но не меняет решения автоматически. Содержательные исправления выполняются после ручного чтения и исследования; `review.jsonl` и итоговый отчёт обеспечивают прослеживаемость.

**Tech Stack:** Python 3.12 и стандартная библиотека, `unittest`, JSON/JSONL, Markdown, `jq`, Git, публичные первичные и специализированные веб-источники.

**Spec:** `_rabota/specs/2026-08-28-audit-of-audit-design.md`

## Global Constraints

- Автоматический анализ охватывает все `C0001`-`C2744`; новый поиск обязателен только для спорных и высокорисковых кандидатов и утверждений без согласия между Википедиями.
- `index.html` не изменяется; его Git blob всегда равен `60caf935aed22dca9054283876f9b8949158fa39`.
- Исходный чекпоинт метрик: `a16b1d3c3c8468d5c2d66f15575766545385ae4a`.
- Источник оценивается по компетенции для конкретного факта. Производитель является первичным источником состава собственного продукта, но заинтересованным источником собственного первенства, рекорда или репутации.
- Переводы, синдикация, пресс-релиз и его пересказы считаются одной источниковой линией. Неясная зависимость не повышает число независимых линий.
- Отсутствие материала означает только отсутствие в выбранном корпусе и не превращается в опровержение.
- Новые записи `sources.jsonl` получают непрерывные `E`-идентификаторы. Исходные записи не переписываются по содержанию; при новой проверке добавляется новая запись, а у старой допустимо менять только `claim_ids`.
- После каждого содержательного пакета выполняются тесты, три режима валидатора, HTML-проверка, контроль blob, проверка исходных источников, `git diff --check`, commit, push и сверка SHA.

Полная проверка пакета:

```bash
python3 -m unittest discover -s _rabota/audit/tests -v
python3 _rabota/audit/validate_audit.py --manifest-only --through B0849 _rabota/audit
python3 _rabota/audit/validate_audit.py --sources --through B0849 _rabota/audit
python3 _rabota/audit/validate_audit.py --through B0849 _rabota/audit
python3 _rabota/check.py index.html
test "$(git hash-object index.html)" = "60caf935aed22dca9054283876f9b8949158fa39"
baseline_source_count=$(git show a16b1d3c3c8468d5c2d66f15575766545385ae4a:_rabota/audit/sources.jsonl | wc -l)
diff <(git show a16b1d3c3c8468d5c2d66f15575766545385ae4a:_rabota/audit/sources.jsonl | jq -S 'del(.claim_ids)') <(head -n "$baseline_source_count" _rabota/audit/sources.jsonl | jq -S 'del(.claim_ids)')
git diff --check
```

После каждого push:

```bash
test "$(git rev-parse HEAD)" = "$(git ls-remote origin refs/heads/audit/polnyj-wikipedia-audit | cut -f1)"
```

---

### Task 1: Политика веса, компетенции и независимости источников

**Files:**
- Create: `_rabota/audit/meta/source_policy.json`
- Create: `_rabota/audit/meta_audit.py`
- Create: `_rabota/audit/tests/test_meta_audit.py`

**Interfaces:**
- Consumes: записи `sources.jsonl`.
- Produces: `load_jsonl(path: Path) -> list[dict]`, `load_source_policy(path: Path) -> dict`, `classify_source(source: dict, policy: dict) -> dict`, `source_lineage_key(source: dict) -> str`, `build_source_profiles(sources: list[dict], policy: dict) -> dict[str, dict]`.

- [ ] **Step 1: Write failing tests for role-aware classification**

```python
class SourcePolicyTests(unittest.TestCase):
    def test_peer_reviewed_source_is_authoritative(self):
        source = {"resource": "peer_reviewed_genetics", "relation": "direct_identity_evidence", "provenance": "journal article", "url": "https://doi.org/10.1/x", "title": "Genetics", "summary": "Direct result"}
        result = classify_source(source, load_source_policy(POLICY_PATH))
        self.assertEqual(result["tier"], "authoritative")
        self.assertEqual(result["independence"], "editorially_independent")

    def test_unreviewed_university_extension_is_specialist(self):
        source = {"resource": "university_extension", "relation": "viticulture_guidance", "provenance": "extension", "url": "https://extension.example/x", "title": "Guide", "summary": "Guide"}
        self.assertEqual(classify_source(source, load_source_policy(POLICY_PATH))["tier"], "specialist")

    def test_producer_first_claim_is_interested_only(self):
        source = {"resource": "official_producer", "relation": "producer_first_claim", "provenance": "producer", "url": "https://producer.example/x", "title": "History", "summary": "We were first"}
        result = classify_source(source, load_source_policy(POLICY_PATH))
        self.assertEqual(result["tier"], "limited")
        self.assertEqual(result["independence"], "interested_primary")
        self.assertEqual(result["competence"], "interested_only")

    def test_declared_translation_shares_parent_lineage(self):
        original = {"url": "https://example.org/report", "title": "Official report", "provenance": "original report", "summary": "same evidence"}
        translation = {"url": "https://mirror.example/translation", "title": "Official report translated", "provenance": "translation of https://example.org/report", "summary": "same evidence"}
        self.assertEqual(source_lineage_key(original), source_lineage_key(translation))
```

- [ ] **Step 2: Run tests and verify import failure**

```bash
python3 -m unittest _rabota.audit.tests.test_meta_audit.SourcePolicyTests -v
```

Expected: import failure because the module and functions do not exist.

- [ ] **Step 3: Create explicit policy JSON**

The policy defines these base tiers and relation rules:

```json
{
  "tier_order": ["authoritative", "specialist", "limited", "weak", "wikipedia"],
  "authoritative_tokens": ["peer_reviewed", "academic_monograph", "critical_edition", "intergovernmental", "regulation", "rulebook", "law", "official_register", "official_statistics", "official_competition_database", "vivc", "international_variety_catalogue", "oiv", "inao", "national_viticulture_centre", "research_institute"],
  "specialist_tokens": ["university", "extension", "wein_plus_lexicon", "wine_lexicon", "specialist_wine", "national_wine_body", "professional_editorial"],
  "limited_tokens": ["official_producer", "producer", "serbianwine", "tourism", "retail", "directory", "commercial"],
  "weak_tokens": ["aggregator", "blog", "search_snippet", "marketplace", "social_media"],
  "wikipedia_resource": "wikipedia",
  "independence_overrides": {"official_producer": "interested_primary", "retailer": "commercial_secondary", "serbianwine_rs": "local_secondary"},
  "relation_rules": {"producer_current_product": "within_scope_primary", "producer_composition": "within_scope_primary", "producer_technology": "within_scope_primary", "producer_vintage": "within_scope_primary", "producer_first_claim": "interested_only", "producer_record_claim": "interested_only", "producer_reputation_claim": "interested_only"}
}
```

- [ ] **Step 4: Implement minimal classification and conservative lineage grouping**

Normalize `resource` and `relation`; apply the exact Wikipedia rule first; apply token tiers in order; unknown resources receive `weak`, `unknown`, `role_unspecified`, `needs_policy_review: true`. `source_lineage_key` first extracts an explicitly declared parent URL or translation/syndication marker from `provenance`, then uses normalized host/title/summary. Different `source_id` never proves independence.

- [ ] **Step 5: Run tests, full verification, commit and push**

```bash
python3 -m unittest _rabota.audit.tests.test_meta_audit.SourcePolicyTests -v
# run the full package verification block from Global Constraints
git add _rabota/audit/meta/source_policy.json _rabota/audit/meta_audit.py _rabota/audit/tests/test_meta_audit.py
git commit -m "audit: classify evidence source roles"
git push origin HEAD:refs/heads/audit/polnyj-wikipedia-audit
# run the post-push SHA check
```

### Task 2: Смысловые кластеры и очередь риска

**Files:**
- Modify: `_rabota/audit/meta_audit.py`
- Modify: `_rabota/audit/tests/test_meta_audit.py`

**Interfaces:**
- Produces: `normalize_keys(claim: dict) -> frozenset[str]`, `fact_signature(claim: dict) -> dict`, `duplicate_candidates(claims: list[dict]) -> list[dict]`, `risk_reasons(claim: dict, decision: dict, source_profile: dict) -> list[str]`, `scan_audit(base_dir: Path, policy_path: Path) -> dict`.

- [ ] **Step 1: Write failing candidate tests**

Tests must prove: reordered identical `entity_keys` cluster; one generic key does not cluster; near duplicates require at least two specific keys and compatible property; different year, vintage, territory, unit or denominator is a scope barrier; high consensus with only Wikipedia is flagged; Wikipedia conflict and Wikipedia absence receive different reason codes; ordering is deterministic.

```python
def test_exact_fingerprint_clusters(self):
    claims = [{"claim_id": "C0001", "entity_keys": ["prokupac", "kamenicarka", "synonym"], "category": "синоним"}, {"claim_id": "C0002", "entity_keys": ["synonym", "kamenicarka", "prokupac"], "category": "название"}]
    self.assertEqual(duplicate_candidates(claims)[0]["claim_ids"], ["C0001", "C0002"])

def test_vintage_and_denominator_are_scope_barriers(self):
    claims = [{"claim_id": "C0001", "entity_keys": ["winery-x", "2020", "yield", "per-hectare"], "category": "урожайность", "statement": "5 тонн с гектара"}, {"claim_id": "C0002", "entity_keys": ["winery-x", "2021", "yield", "total"], "category": "урожайность", "statement": "5 тонн всего"}]
    self.assertEqual(duplicate_candidates(claims), [])
```

- [ ] **Step 2: Run tests and verify failures**

```bash
python3 -m unittest _rabota.audit.tests.test_meta_audit.CandidateTests -v
```

- [ ] **Step 3: Implement deterministic signatures and clustering**

Exact fingerprints use normalized `entity_keys`. Near candidates require two non-generic overlapping keys, containment at least `0.75`, and compatible normalized object/property or category. `fact_signature` extracts dates, numbers with units and denominators, territories, producers and vintages from `entity_keys`, `statement` and `book_quote`; differing scope fields block automatic clustering.

```python
GENERIC_ENTITY_KEYS = {"serbia", "wine", "winery", "grape", "vineyard", "history", "climate", "geography", "style", "producer", "current"}
```

- [ ] **Step 4: Implement stable risk reason codes**

```python
RISK_REASON_ORDER = ("duplicate_decision_variance", "wikipedia_disagreement", "wikipedia_absence", "disputed_status", "non_high_consensus", "high_consensus_without_strong_source", "high_risk_fact_type", "categorical_or_superlative", "late_source_recheck", "unknown_source_classification")
```

High-risk types include exact numbers/dates, law/regulation, awards, records, firsts, cultivar origin/parentage, official zoning and historical causation. Strong evidence means an authoritative or specialist source competent for the fact, with independent lineage or a decisive registry/normative source.

- [ ] **Step 5: Run tests, full verification, commit and push**

```bash
python3 -m unittest _rabota.audit.tests.test_meta_audit -v
# full package verification
git add _rabota/audit/meta_audit.py _rabota/audit/tests/test_meta_audit.py
git commit -m "audit: detect repeated and high-risk findings"
git push origin HEAD:refs/heads/audit/polnyj-wikipedia-audit
# post-push SHA check
```

### Task 3: CLI, frozen baseline and review validation

**Files:**
- Modify: `_rabota/audit/meta_audit.py`
- Modify: `_rabota/audit/tests/test_meta_audit.py`
- Create: `_rabota/audit/meta/candidates.jsonl`
- Create: `_rabota/audit/meta/baseline.json`

**Interfaces:**
- Produces: `write_candidates(scan: dict, path: Path) -> None`, `load_candidates(path: Path) -> list[dict]`, `validate_review(candidates: list[dict], claim_ids: set[str], records: list[dict], require_complete: bool) -> list[str]`; CLI commands `scan` and `validate-review`.

- [ ] **Step 1: Write failing schema and CLI tests**

Tests reject missing claims, duplicate `meta_id`, duplicate `candidate_key`, invalid resolution, empty required prose and unreviewed frozen candidates under `--require-complete`.

```python
def test_require_complete_reports_unreviewed_candidate(self):
    candidates = [{"candidate_key": "risk:C0001"}]
    self.assertIn("unreviewed candidate risk:C0001", validate_review(candidates, {"C0001"}, [], True))
```

- [ ] **Step 2: Run tests and verify failures**

```bash
python3 -m unittest _rabota.audit.tests.test_meta_audit.ReviewValidationTests -v
```

- [ ] **Step 3: Implement frozen candidate and review schemas**

Candidates receive contiguous stable `M0001` identifiers in deterministic order and fields `candidate_key`, `kind`, `claim_ids`, `risk_reasons`, `source_profile`, `original_statuses`. Review records contain `meta_id`, `candidate_key`, `kind`, `claim_ids`, `canonical_question`, `risk_reasons`, `scope`, `source_lines`, `source_weight`, `resolution`, `resolution_notes`, `changes`, `remaining_gap`.

Allowed resolutions: `согласован`, `исправлен`, `различается по охвату`, `остаётся неразрешённым`.

- [ ] **Step 4: Implement CLI and freeze the baseline**

```bash
python3 _rabota/audit/meta_audit.py scan _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --baseline _rabota/audit/meta/baseline.json
python3 _rabota/audit/meta_audit.py validate-review _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --review _rabota/audit/meta/review.jsonl
```

The baseline records counts by 250-claim band, status, consensus, source tier and risk reason. `validate-review` always checks coverage against frozen `candidates.jsonl`, while claim references are checked against the current corpus, so corrections cannot erase their own review obligation.

- [ ] **Step 5: Run all tests, generate artifacts, full verification, commit and push**

```bash
python3 -m unittest discover -s _rabota/audit/tests -v
python3 _rabota/audit/meta_audit.py scan _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --baseline _rabota/audit/meta/baseline.json
jq -e . _rabota/audit/meta/baseline.json >/dev/null
jq -e . _rabota/audit/meta/candidates.jsonl >/dev/null
# full package verification
git add _rabota/audit/meta_audit.py _rabota/audit/tests/test_meta_audit.py _rabota/audit/meta/candidates.jsonl _rabota/audit/meta/baseline.json
git commit -m "audit: freeze cross-audit risk baseline"
git push origin HEAD:refs/heads/audit/polnyj-wikipedia-audit
# post-push SHA check
```

### Task 4: Разрешить повторные факты

**Files:**
- Create: `_rabota/audit/meta/review.jsonl`
- Modify: `_rabota/audit/claims.jsonl`
- Modify: `_rabota/audit/decisions.jsonl`
- Modify: `_rabota/audit/sources.jsonl`

- [ ] **Step 1: Extract every repeated-fact candidate and linked records**

```bash
jq -c 'select(.kind == "смысловой повтор")' _rabota/audit/meta/candidates.jsonl
```

- [ ] **Step 2: Compare object, property, scope, status, consensus and source lineage for each cluster**

`различается по охвату` names the year, territory, vintage, producer, denominator, legal regime or categorical wording. `согласован` explains compatibility. `исправлен` lists every changed claim. `остаётся неразрешённым` names the evidence still missing.

- [ ] **Step 3: Research only true conflicts and selected high-risk repeats**

Use VIVC/CEVVIN for cultivar identity, official regulations for legal geography, official competition databases for awards, primary/academic sources for history, OIV for definitions, and producer pages only for current own-product facts.

- [ ] **Step 4: Apply corrections with `apply_patch` and append review/source records**

Preserve atomic claim boundaries. Append a new `E` record for newly read evidence. Do not rewrite the factual summary of an old source record.

- [ ] **Step 5: Validate, commit and push**

```bash
python3 _rabota/audit/meta_audit.py validate-review _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --review _rabota/audit/meta/review.jsonl
# full package verification
git add _rabota/audit/meta/review.jsonl _rabota/audit/claims.jsonl _rabota/audit/decisions.jsonl _rabota/audit/sources.jsonl
git commit -m "audit: reconcile repeated factual findings"
git push origin HEAD:refs/heads/audit/polnyj-wikipedia-audit
# post-push SHA check
```

### Task 5: Разрешить конфликты и пробелы Википедий

**Files:**
- Modify: `_rabota/audit/meta/review.jsonl`
- Modify: `_rabota/audit/claims.jsonl`
- Modify: `_rabota/audit/decisions.jsonl`
- Modify: `_rabota/audit/sources.jsonl`

- [ ] **Step 1: Extract the Wikipedia queue**

```bash
jq -c 'select((.risk_reasons | index("wikipedia_disagreement")) or (.risk_reasons | index("wikipedia_absence")))' _rabota/audit/meta/candidates.jsonl
```

- [ ] **Step 2: Recheck each item with a role-matched specialist source**

Use VIVC/CEVVIN for varieties, OIV for definitions, Serbian/EU legal texts for classifications, organiser databases for competitions, academic sources for history, and current technical pages for named products.

- [ ] **Step 3: Reconcile status and consensus**

If a stronger source resolves conflicting Wikipedias, the main status follows the best evidence and the Wikipedia conflict remains in `comparison`. If Wikipedias are silent but specialist evidence is decisive, retain the coverage status `в Википедиях отсутствует`, adjust `consensus` where warranted and state the substantive verdict in `editor_conclusion`.

- [ ] **Step 4: Record exact remaining gaps and apply corrections**

Unresolved records name the missing registry snapshot, ledger, genotype, trademark record, planting register or bottle-specific technical sheet.

- [ ] **Step 5: Validate, commit and push**

```bash
python3 _rabota/audit/meta_audit.py validate-review _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --review _rabota/audit/meta/review.jsonl
# full package verification
git add _rabota/audit/meta/review.jsonl _rabota/audit/claims.jsonl _rabota/audit/decisions.jsonl _rabota/audit/sources.jsonl
git commit -m "audit: resolve wikipedia evidence gaps"
git push origin HEAD:refs/heads/audit/polnyj-wikipedia-audit
# post-push SHA check
```

### Task 6: Ретроспективная проверка `C0001`-`C0686`

**Files:** modify the four audit/review JSONL files from Tasks 4-5.

- [ ] **Step 1: Extract unresolved candidates touching the band**

```bash
jq -c --slurpfile review _rabota/audit/meta/review.jsonl '($review | map(.candidate_key)) as $done | select((.candidate_key as $key | $done | index($key)) == null) | select(any(.claim_ids[]; ((.[1:] | tonumber) >= 1 and (.[1:] | tonumber) <= 686)))' _rabota/audit/meta/candidates.jsonl
```

- [ ] **Step 2: Review in stable risk order**

First inspect `high_consensus_without_strong_source`, then legal/number/date/first/record/origin/parentage claims, then remaining disputed statuses. For each candidate record the canonical question and exact scope before searching.

- [ ] **Step 3: Run the late-source retroactive sweep**

Search relevant early entities against OIV, VIVC, CEVVIN, official Serbian/EU law and statistics, archives, peer-reviewed literature, competition databases, wein.plus and documented national wine bodies. Reuse a source only when it addresses the same object, property, time and territory.

- [ ] **Step 4: Apply and record resolutions**

Use `apply_patch`; narrow negative conclusions to the selected corpus; append new `E` records and one review record for every selected candidate.

- [ ] **Step 5: Validate, commit and push**

```bash
python3 _rabota/audit/meta_audit.py validate-review _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --review _rabota/audit/meta/review.jsonl
# full package verification
git add _rabota/audit/meta/review.jsonl _rabota/audit/claims.jsonl _rabota/audit/decisions.jsonl _rabota/audit/sources.jsonl
git commit -m "audit: strengthen early high-risk findings"
git push origin HEAD:refs/heads/audit/polnyj-wikipedia-audit
# post-push SHA check
```

### Task 7: Ретроспективная проверка `C0687`-`C1372`

**Files:** modify the four audit/review JSONL files from Tasks 4-5.

- [ ] **Step 1: Extract unresolved candidates touching the band**

```bash
jq -c --slurpfile review _rabota/audit/meta/review.jsonl '($review | map(.candidate_key)) as $done | select((.candidate_key as $key | $done | index($key)) == null) | select(any(.claim_ids[]; ((.[1:] | tonumber) >= 687 and (.[1:] | tonumber) <= 1372)))' _rabota/audit/meta/candidates.jsonl
```

- [ ] **Step 2: Review in stable risk order**

Process decision variance, Wikipedia conflicts, weak high consensus, numbers/dates/legal facts and other disputed statuses. Treat producer assertions of firsts and records as interested unless independently registered; preserve bottle, vintage, region and period scope.

- [ ] **Step 3: Apply and record resolutions**

Use role-matched specialist evidence, `apply_patch`, new `E` records and one review record for every selected candidate.

- [ ] **Step 4: Validate, commit and push**

```bash
python3 _rabota/audit/meta_audit.py validate-review _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --review _rabota/audit/meta/review.jsonl
# full package verification
git add _rabota/audit/meta/review.jsonl _rabota/audit/claims.jsonl _rabota/audit/decisions.jsonl _rabota/audit/sources.jsonl
git commit -m "audit: reconcile second-band high-risk findings"
git push origin HEAD:refs/heads/audit/polnyj-wikipedia-audit
# post-push SHA check
```

### Task 8: Ретроспективная проверка `C1373`-`C2058`

**Files:** modify the four audit/review JSONL files from Tasks 4-5.

- [ ] **Step 1: Extract unresolved candidates touching the band**

```bash
jq -c --slurpfile review _rabota/audit/meta/review.jsonl '($review | map(.candidate_key)) as $done | select((.candidate_key as $key | $done | index($key)) == null) | select(any(.claim_ids[]; ((.[1:] | tonumber) >= 1373 and (.[1:] | tonumber) <= 2058)))' _rabota/audit/meta/candidates.jsonl
```

- [ ] **Step 2: Review descriptor and identity boundaries**

Keep cultivar profiles separate from individual bottles/vintages; one tasting note remains one observation, not consensus. Use VIVC/CEVVIN/genetics for identity and synonymy; correct source-line inflation, status variance and categorical language.

- [ ] **Step 3: Apply and record resolutions**

Use `apply_patch`, append new evidence as new `E` records and add one review record for every selected candidate.

- [ ] **Step 4: Validate, commit and push**

```bash
python3 _rabota/audit/meta_audit.py validate-review _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --review _rabota/audit/meta/review.jsonl
# full package verification
git add _rabota/audit/meta/review.jsonl _rabota/audit/claims.jsonl _rabota/audit/decisions.jsonl _rabota/audit/sources.jsonl
git commit -m "audit: reconcile third-band high-risk findings"
git push origin HEAD:refs/heads/audit/polnyj-wikipedia-audit
# post-push SHA check
```

### Task 9: Ретроспективная проверка `C2059`-`C2744`

**Files:** modify the four audit/review JSONL files from Tasks 4-5.

- [ ] **Step 1: Extract unresolved candidates touching the band**

```bash
jq -c --slurpfile review _rabota/audit/meta/review.jsonl '($review | map(.candidate_key)) as $done | select((.candidate_key as $key | $done | index($key)) == null) | select(any(.claim_ids[]; ((.[1:] | tonumber) >= 2059 and (.[1:] | tonumber) <= 2744)))' _rabota/audit/meta/candidates.jsonl
```

- [ ] **Step 2: Recheck late decisions under the common policy**

Verify legal, current, quantitative, superlative and weak-source high-consensus claims. Preserve exact object, property, territory, time, producer, vintage, denominator and source-line independence.

- [ ] **Step 3: Apply and record resolutions**

Use role-matched evidence and `apply_patch`; append new evidence as new `E` records and add one review record for every selected candidate.

- [ ] **Step 4: Validate, commit and push**

```bash
python3 _rabota/audit/meta_audit.py validate-review _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --review _rabota/audit/meta/review.jsonl
# full package verification
git add _rabota/audit/meta/review.jsonl _rabota/audit/claims.jsonl _rabota/audit/decisions.jsonl _rabota/audit/sources.jsonl
git commit -m "audit: reconcile final-band high-risk findings"
git push origin HEAD:refs/heads/audit/polnyj-wikipedia-audit
# post-push SHA check
```

### Task 10: Методологический дрейф и итоговый отчёт

**Files:**
- Modify: `_rabota/audit/meta_audit.py`
- Modify: `_rabota/audit/tests/test_meta_audit.py`
- Modify: `_rabota/audit/meta/review.jsonl`
- Create: `_rabota/audit/meta/report.md`

**Interfaces:**
- Produces: `methodology_comparison(baseline: dict, current_scan: dict) -> dict` and CLI complete-review validation.

- [ ] **Step 1: Write a failing comparison test**

```python
def test_reports_reduction_in_weak_high_consensus(self):
    baseline = {"totals": {"high_consensus_without_strong_source": 10}}
    current = {"totals": {"high_consensus_without_strong_source": 3}}
    result = methodology_comparison(baseline, current)
    self.assertEqual(result["resolved_weak_high_consensus"], 7)
    self.assertEqual(result["remaining_weak_high_consensus"], 3)
```

- [ ] **Step 2: Run the test and verify failure**

```bash
python3 -m unittest _rabota.audit.tests.test_meta_audit.MethodologyComparisonTests -v
```

- [ ] **Step 3: Implement comparison and complete-review validation**

Report baseline/final counts by claim band, risk reason, source tier, status and consensus. `--require-complete` passes only when every frozen candidate has a review record; unresolved risks require a non-empty `remaining_gap`.

- [ ] **Step 4: Write `report.md`**

The report covers initial scale/method, repeated facts, true contradictions and corrections, scope differences, Wikipedia conflicts, specialist resolutions, Wikipedia gaps, early/late comparison, changed source weights, unresolved questions, changed `claim_id` values and package commits.

- [ ] **Step 5: Run final verification**

```bash
python3 -m unittest discover -s _rabota/audit/tests -v
python3 _rabota/audit/meta_audit.py validate-review _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --review _rabota/audit/meta/review.jsonl --require-complete
python3 _rabota/audit/validate_audit.py --manifest-only --through B0849 _rabota/audit
python3 _rabota/audit/validate_audit.py --sources --through B0849 _rabota/audit
python3 _rabota/audit/validate_audit.py --through B0849 _rabota/audit
python3 _rabota/check.py index.html
test "$(git hash-object index.html)" = "60caf935aed22dca9054283876f9b8949158fa39"
baseline_source_count=$(git show a16b1d3c3c8468d5c2d66f15575766545385ae4a:_rabota/audit/sources.jsonl | wc -l)
diff <(git show a16b1d3c3c8468d5c2d66f15575766545385ae4a:_rabota/audit/sources.jsonl | jq -S 'del(.claim_ids)') <(head -n "$baseline_source_count" _rabota/audit/sources.jsonl | jq -S 'del(.claim_ids)')
git diff --check
```

- [ ] **Step 6: Commit, push and verify final checkpoint**

```bash
git add _rabota/audit/meta_audit.py _rabota/audit/tests/test_meta_audit.py _rabota/audit/meta/review.jsonl _rabota/audit/meta/report.md _rabota/audit/claims.jsonl _rabota/audit/decisions.jsonl _rabota/audit/sources.jsonl
git commit -m "audit: complete cross-audit consistency review"
git push origin HEAD:refs/heads/audit/polnyj-wikipedia-audit
test "$(git rev-parse HEAD)" = "$(git ls-remote origin refs/heads/audit/polnyj-wikipedia-audit | cut -f1)"
```
