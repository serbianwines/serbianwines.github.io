# Independent regional style review — 2026-09-05

## Independent scope

The reviewer assessed the seven substantive decision changes for C0547, C0549, C0553, C0563, C0565, C0567 and C0576, and separately checked the evidentiary sufficiency of unchanged C0577, C0593 and C0594. The review covered literal claim scope, source competence and independence, wine/vintage identity, exact before/after records, preservation constraints and the recorded validation evidence.

## Accepted substantive decisions

- C0547: accepted removal of the false objective refutation and the attributed-impression advice. The word “контрпример” in the comparison was noted as a deferred Minor; the decision and advice remain accepted.
- C0549: accepted that individual producer notes do not establish or refute a regional three-variety style.
- C0553: accepted separation of grape presence outside the region from proof of the same light-red style.
- C0563: accepted the bounded food-pairing conclusion without replacement pseudo-science.
- C0565: accepted the refusal to infer terroir causality from one soil label and nonoverlapping source domains.
- C0567: accepted the vintage/identity qualification and removal of the unsupported 2024 transfer.
- C0576: accepted the DWWA result and corrected source-role statement; the ratings snapshot is not a second independent source.

## Unchanged decisions

- C0577 is sufficiently supported by the official DWWA 2026 table.
- C0593 is sufficiently supported as an attributed Vino.rs editorial choice.
- C0594 is sufficiently supported as an attributed Vino.rs selection entry, not a unique competition winner.

## Review finding and fix

The initial review found one Important metadata defect: the seven changed review rows used `pending_independent` instead of the required `self_checked_pending_independent`. Commit `2fee1c7b914def497fa5f3eeba493fd7d87d3846` corrected exactly those seven status values; focused JSON verification, `validate-review` and `git diff --check` passed. The subsequent independent review accepted all seven substantive decisions, so their final status is `independently_reviewed` with claim-specific acceptance records.

The C0547 wording observation about “контрпример” is explicitly deferred and non-blocking.

## Verdict

**SPEC PASS / QUALITY PASS**
