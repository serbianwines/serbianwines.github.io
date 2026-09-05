# Chronology / false-refutation pack report

Date: 2026-09-05
Baseline: `4d12ec3`
Scope: C0486, C0491, C0509, C0510, plus the bounded evidence-role supplement to existing C0574/M0542.

## Evidence inspected

- Directly read the dated Šapat host article of 29 July 2026. It says James Suckling visited Serbia at Mladen Dragojlović’s invitation and spent a day at Šapat. This is a separate event from E000472’s dated report that Dragojlović visited Suckling in Tuscany in 2022.
- Directly read the vino.rs launch report of 26 March 2026. It identifies Rogoz, Husar and Kolodar as the first three labels and says sales would begin in mid-April 2026.
- Read the saved read-only ratings-branch snapshot `a9d26b3`. Its raw Vinoteka Beograd records identify all three labels: Husar 2024 and Kolodar 2024 at 4100 RSD, Rogoz 2025 at 3650 RSD. This is the same retailer lineage as E000474 and is recorded as checked-only WIP evidence, with its stated collection date of 2026-09-02.
- Downloaded and read the original JP Palić-Ludaš management-program PDF, specifically printed page 6, sections 3.2–3.3. It says Krvavo was transformed in 1971 but remained a water body used for fish stock and as an ecological corridor; Slano was destroyed by construction of the Palić–Ludaš canal in 1971. This closes the original-PDF gap behind E000485, but does not provide a 2026 hydrological survey or refute the historical aeolian origin.
- Read the ratings-branch derived DWWA rows and importer for C0574. They provide exact leads—2018 wine 591497/vintage 2016, 2019 wine 598416/vintage 2017, and 2021 wine 701094/vintage 2019—but no raw API cache. The derived tables are one lineage and were not treated as independent organizer evidence. Failed organizer requests were not repeated.

## Per-ID findings and changes

### C0486

- Finding: the former refutation was false because it substituted the 2022 Tuscany meeting for the separately documented 2026 Serbia visit.
- Decision: `расходится / высокий` → `совпадает / средний`.
- Advice: leave the book sentence. If expanded, attribute the invitation to Šapat and avoid claiming that Dragojlović was the exclusive cause of the trip.
- New source: E003565, supporting. E000472 is checked-only chronology for the separate 2022 event.
- Gap: no independent source was found for who initiated the 2026 visit; the attributed wording does not require one.

### C0491

- Finding: the approximate level around 4000 RSD is supported across all three initial labels, but the retail year 2025 is impossible because the wines launched in spring 2026.
- Decision status remains `расходится / высокий`; comparison, evidence weighting and advice were rewritten.
- Advice: change only the retail year to 2026. An approximate guide price need not enumerate every label; exact prices, if used, should carry retailer, record date and vintage.
- New source: E003566, checked-only WIP snapshot. E000471 and E000474 remain supporting evidence with their original access dates.
- Gap: no fresh 2026-09-05 retailer recheck was claimed; exact values remain dated retail records.

### C0509

- Finding: a present-tense count of four lakes is misleading because Slano was destroyed in 1971. The official document does not disprove the historical aeolian quartet, and Krvavo must not be described as simply gone.
- Decision remains `расходится / высокий`; the comparison and advice now target the modern-number problem precisely.
- Advice: describe a historical system of four aeolian lakes, then state that Krvavo was transformed and Slano destroyed by the canal in 1971.
- New source: E003567, supporting original official PDF. E000484 and E000485 are checked-only context from the same institutional/document chain.
- Gap: no 2026 hydrological survey; one is needed only for a fuller current-status account.

### C0510

- Finding: the historical list is valid, while the auditor’s added proposition that all four are current natural lakes of one status is not a literal claim in the book. Krvavo remains a transformed water body; Slano does not.
- Decision: `расходится / высокий` → `совпадает с уточнением / высокий`.
- Advice: keep the historical-geographic list with the distinct 1971 outcomes; do not inject equal current legal or natural status.
- New source and gap are the same bounded official-document evidence as C0509.

### C0574 / M0542 supplement

- The decision and producer-attributed advice are unchanged.
- E003568 was added as checked-only WIP lead evidence, and the existing review now records the three exact organizer record IDs and vintages.
- Remaining gap is narrowed to direct reading of DWWA records 591497, 598416 and 701094. Until then, the saved producer page remains the only read supporting source.
- Because this is a substantive evidence-role supplement, M0542 is marked `self_checked_pending_independent`.

## Files and preservation

- Changed four rows in `_rabota/audit/decisions.jsonl`.
- Appended E003565–E003568 to `_rabota/audit/sources.jsonl`.
- Appended exactly the four previously unreviewed candidate rows M0455, M0460, M0480 and M0481. The already frozen repeat review M0479 was not duplicated.
- Supplemented the existing M0542 review row without changing its recorded decision change.
- Claims, frozen candidates, baseline and the first 469 review rows are byte-identical to baseline. Every unchanged historical decision and source row is byte-identical. Existing source factual fields were not changed.
- `index.html` is unchanged; blob remains `60caf935aed22dca9054283876f9b8949158fa39`.

## Validation

- 95 audit unit tests: passed.
- `meta_audit.py validate-review` without `--require-complete`: passed.
- Full `validate_audit.py --through B0849`: passed.
- `_rabota/check.py index.html`: passed.
- Exact book blob check: passed.
- Historical-byte preservation check: passed.
- `git diff --check`: passed.

All new substantive review rows, including the C0574 evidence supplement, remain pending independent review as required.
