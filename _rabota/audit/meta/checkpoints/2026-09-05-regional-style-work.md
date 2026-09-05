# Regional style and awards work checkpoint — 2026-09-05

## Scope and method

Reviewed exactly 10 frozen candidates from the regional package: C0547, C0549, C0553, C0563, C0565, C0567, C0576, C0577, C0593 and C0594. Literal book wording was compared with the dated saved evidence and the user-authorized read-only ratings snapshot. Source competence, independence, wine identity, vintage and claim scope were assessed separately. No new web search was needed: the remaining gaps could be handled by precise attribution or editorial qualification.

## Per-ID outcome

| Claim | Outcome |
| --- | --- |
| C0547 | Changed from `расходится` to `непроверяемо по выбранному корпусу`; one producer Chardonnay does not disprove a regional relative tendency. Preserve only as an attributed author impression. |
| C0549 | Changed from `расходится` to `непроверяемо по выбранному корпусу`; producer notes for individual wines do not objectively refute or establish a unified three-variety regional profile. |
| C0553 | Changed to `непроверяемо по выбранному корпусу`, low consensus; Kadarka outside the region does not prove the same light-red style there. Remove categorical exclusivity. |
| C0563 | Changed to `непроверяемо по выбранному корпусу`, low consensus; one wine column does not establish a universal food-pairing rule or its universal refutation. |
| C0565 | Changed to `непроверяемо по выбранному корпусу`, low consensus; soil description and wine description do not establish sand causality or its absence. |
| C0567 | Changed to `непроверяемо по выбранному корпусу`, low consensus; the producer's 2019 descriptor cannot refute an unidentified vintage and the 2024 transfer was removed. |
| C0576 | Award result and advice retained; source-role text corrected so the official DWWA record is decisive and ratings WIP is only an identity cross-check. |
| C0577 | No decision change; official DWWA 2026 evidence sufficiently confirms both Gold wines were white. |
| C0593 | No decision change; Vino.rs sufficiently supports its own attributed 2025 editorial brand choice. |
| C0594 | No decision change; Vino.rs sufficiently supports Karom 2023 in its attributed local-variety white selection and the organic label. |

Seven decisions changed (C0547, C0549, C0553, C0563, C0565, C0567, C0576); three remained unchanged (C0577, C0593, C0594). All seven substantive changes were independently accepted as `spec_pass_quality_pass` after the status-field correction in commit `2fee1c7`.

## Preservation and verification

- Only the 10 exact candidate keys were reviewed; one review row was appended per key.
- Claims, sources, frozen candidates, baseline, priorities, book HTML and the ratings branch were not edited.
- Unchanged JSONL rows retained their original bytes. The first 469 review rows retained SHA-256 `5f8591fd640557461a88599a06a30d8eab29de8679fcbf3bd440900745450350`.
- `index.html` retained blob `60caf935aed22dca9054283876f9b8949158fa39`.
- Exact before/after verification passed 7/7; exact candidate-key verification passed 10/10.
- `python3 -m unittest discover -s _rabota/audit/tests`: 95 tests, OK.
- `meta_audit.py validate-review`: passed.
- Full `validate_audit.py --through B0849`: passed.
- `git diff --check`: passed.

The deferred Minor wording note for C0547 concerns the term “контрпример” only; it does not alter the accepted decision or editorial advice.
