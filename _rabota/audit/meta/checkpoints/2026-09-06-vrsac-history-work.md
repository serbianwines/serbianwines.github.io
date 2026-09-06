# Vršac history work checkpoint — 2026-09-06

## Scope and method

Reviewed exactly four frozen candidates: C0611, C0612, C0624 and C0682. Literal book wording in B0112, B0113 and B0133 was compared with the current decisions, exact candidate rows and every reverse-linked saved source row. No new web search was performed because the dated saved evidence plus precise attribution was sufficient for the editorial advice.

C0624 and C0682 were treated as one evidence question. E000616 and E000719 represent the same travel.rs page and content lineage: exhibition 257/120 in 1875 and reduction 66/22 in 1883. They count as one lineage, not two, and absence of a found second dating was not treated as a refutation.

## Per-ID outcome

| Claim | Outcome |
| --- | --- |
| C0611 | Status remained `расходится`; consensus was reduced to `средний`, and E000610/E000614 were counted as retellings of one 1198 charter record. Remove the national priority while retaining only the bounded Vršac formulation. |
| C0612 | No decision change: `совпадает с уточнением`, high consensus. E000611 is sufficient for the local 1494 formulation; owner and directory repetitions do not add independent confirmation. |
| C0624 | Changed from `расходится` / medium to `непроверяемо по выбранному корпусу` / low. Add the missing public 1883 citation if retaining explicit disagreement, or attribute the single travel.rs chronology. |
| C0682 | Changed consistently with C0624 to `непроверяемо по выбранному корпусу` / low. Preserve the sourced 1875/1883 sequence without claiming archival certainty or refuting an unfound alternative text. |

Three decisions changed (C0611, C0624 and C0682); C0612 remained byte-identical. Independent review accepted the three changes and found C0612 sufficiently supported, with no Critical, Important or Minor findings.

## Preservation and verification

- Exactly four review rows were appended for the frozen candidate keys; pre-existing review rows remained byte-identical.
- Claims, sources, candidates, baseline, priorities and book HTML were unchanged.
- The first 469 review rows retained SHA-256 `5f8591fd640557461a88599a06a30d8eab29de8679fcbf3bd440900745450350`.
- `index.html` retained blob `60caf935aed22dca9054283876f9b8949158fa39`.
- Exact candidate-key verification passed 4/4; exact before/after verification passed 3/3.
- `meta_audit.py validate-review`: passed.
- Full `validate_audit.py --through B0849`: passed.
- `python3 -m unittest discover -s _rabota/audit/tests`: 95 tests, OK.
- `git diff --check`: passed.
