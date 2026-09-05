# Independent chronology review

Date: 2026-09-05
Scope: C0486, C0491, C0509, C0510, and the checked-only C0574/M0542 supplement.

## Verdicts

**SPEC: FAIL (one bounded correction required).** The pack respects the requested candidate scope, preserves the book and frozen inputs, distinguishes the 2022 Tuscany meeting from the 2026 Serbia visit, separates retail vintage from retail observation year, and treats the ratings-branch rows as checked-only WIP leads. However, C0510's revised `comparison` and `editor_conclusion` still use present-tense claims about Krvavo (`остаётся`, `сохраняется`) while the cited official program is a March 2016 historical/management document for 2010–2019. This exceeds the brief's explicit limit that the PDF is not a current-2026 hydrological survey.

**QUALITY: FAIL pending the same correction; otherwise the pack is editorially strong.** Source roles and lineages are handled conservatively. The remaining defect matters because the review itself correctly states the temporal limitation but the operative finding and advice then cross it.

## Findings and remedies

### C0486 — pass

The literal book claim is deliberately weak: «Приезд ... тоже связывают с ним». A dated report by the host winery is competent evidence that the host attributes the invitation to Dragojlović. It does not establish independent truth about exclusive causation, and the revision correctly says so. Changing `расходится / высокий` to `совпадает / средний` is justified. E000472 is properly retained only to distinguish the separate 2022 Tuscany event.

### C0491 — pass

The book explicitly labels the figure as an approximate Belgrade-retail guide and explicitly assigns it to 2025. The March 2026 launch report supports correcting that observation year to 2026; the 2024/2025 numbers in the retailer rows are wine vintages, not launch or price-snapshot dates. The three saved listings (3650, 4100, 4100 RSD) adequately support «около 4000» as a dated approximation. The revision properly avoids turning a guide price into a mandatory per-label table and does not misstate the 2026-09-02 WIP snapshot as a fresh 2026-09-05 retailer read.

The wording «поэтому ... 2025 года ошибочно» is preferable to a universal claim that no private or pre-release sale could possibly have occurred; the current operative text uses the appropriately narrower framing tied to the three first labels and the book's retail annotation.

### C0509 — pass, with a scope caution

The surrounding book prose is present-tense («Центр жизни — озеро Палич, одно из четырёх...»), so treating the unqualified modern count as misleading is reasonable. The official PDF establishes the distinct 1971 outcomes: Krvavo was transformed and Slano destroyed by the canal. It does not refute historical aeolian origin, and the revision correctly stops using changed modern status as such a refutation.

The remedy should remain exactly a temporal qualification. The phrase «историческая система четырёх местных эоловых озёр» preserves the book's origin classification; E003567 itself supports the transformation/destruction chronology, not independently the aeolian classification. The review should not imply that this PDF newly proves that origin.

### C0510 — correction required

Changing the decision from `расходится` to `совпадает с уточнением` correctly removes the auditor-invented proposition that the book asserted equal current legal/natural status. The literal text merely completes the four-name list.

The after-state then says Krvavo «остаётся водоёмом, рыбоводным объектом и экологическим коридором» and advises that it «сохраняется как водоём». Those are current-tense claims. E003567 can safely support that the transformed water body was described in the March 2016 program as serving fish-stock and ecological-corridor functions; it cannot by itself establish those functions or even the same hydrological condition on 2026-09-05.

Remedy: rewrite the operative wording with source time, for example: «В программе, согласованной в 2016 году, преобразованное Krvavo описано как водоём, использовавшийся для рыбной молоди и как экологический коридор; Slano было уничтожено каналом в 1971 году». In the editorial advice, retain only the durable documented history («Кровавое преобразовано в 1971 году; Сланое тогда же уничтожено каналом») unless a current source is read. If present status is retained, add a current authoritative source and reassess confidence. Mirror the corrected after-state exactly in M0481.

### C0574 / M0542 — pass

E003568 is accurately classified as a checked-only branch snapshot. The two derived JSONL views are one provenance chain, the importer is not evidence that the organizer records were read, and absence of the raw API cache prevents organizer-level verification. Keeping the producer-attributed advice, reducing confidence to medium, recording IDs 591497/598416/701094 as leads, and marking the substantive supplement pending independent review are all appropriate. Award year and vintage remain correctly separated.

## Before/after and preservation assessment

The four requested new reviews use the frozen candidate keys and record exact decision before/after objects. M0542 preserves its earlier substantive decision change and adds only the bounded evidence-role supplement. The observed working-tree diff affects only `_rabota/audit/decisions.jsonl`, `_rabota/audit/meta/review.jsonl`, and `_rabota/audit/sources.jsonl`; no diff was observed for `index.html`, claims, candidates, or baseline. I did not rerun the reported validations.

## Sources inspected

- `chronology-brief.md`, `chronology-report.md`, and `chronology-review.diff` in this review directory.
- `chronology-input.json` and `ratings-leads.json` in this review directory.
- Current repository rows for C0486, C0491, C0509, C0510, C0574; M0455, M0460, M0480, M0481, M0542; and E000471, E000472, E000474, E000475, E000484, E000485, E000560, E003565–E003568.
- Exact surrounding book HTML for the Dragojlović and lake passages.
- Read-only `git status`, diff summary, and preservation-target diff. No live source requests, branch checkout, test reruns, or ratings-branch writes were performed.
