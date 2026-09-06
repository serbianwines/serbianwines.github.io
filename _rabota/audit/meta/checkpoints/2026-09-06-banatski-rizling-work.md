# Banatski rizling work checkpoint — 2026-09-06

## Scope and outcome

The bounded package covered exactly six frozen candidates: M0607/C0644, M0623/C0662, M0624/C0663, M0626/C0664, M0630/C0670 and M0632/C0671. Independent acceptance is recorded for the five substantive decision changes; M0624/C0663 remains byte-identical as `self_checked_no_decision_change` because its existing qualified decision was found sufficiently supported.

Five review rows changed only from `self_checked_pending_independent` to `independently_reviewed` and gained claim-specific `independent_review` records dated 2026-09-06 with verdict `spec_pass_quality_pass`. No operational review fields, source accounting, exact before/after records or decisions changed.

## Per-ID outcome

| Review / claim | Accepted outcome |
| --- | --- |
| M0607 / C0644 | Absence of Temišvarka from the checked synonym lists is not a positive refutation; retain the requirement for an exact registry, ampelographic or local documentary source. |
| M0623 / C0662 | Remove the literal linkage “именно они”, retain medium consensus and do not extend any one composition across the full history of the brand. |
| M0624 / C0663 | No decision change; the qualified distinction between a non-monovarietal wine and the broader Riesling connection is sufficiently supported. The row remains byte-identical and has no `independent_review` object. |
| M0626 / C0664 | The categorical “never a variety name” claim is contradicted by the official, registry and ampelographic record, with each source role stated separately. |
| M0630 / C0670 | Rhine Riesling is positively present in two fixed product versions, without implying monovarietal status, genetic identity or an unchanged recipe. |
| M0632 / C0671 | High consensus for the historical Kreaca synonym rests on official, registry and scientific roles rather than a count of Wikipedia versions. |

## Provenance correction and source reverse links

Implementation commit `2cb6874658e18102cd7b0b80cb0437b20f2150a4` introduced the six bounded review rows and five substantive decision changes. The first independent review found one Important provenance defect: blocked, not directly read E000748 had been used as the VIVC authority for C0664/C0671.

Fix commit `a054c80dbb5a24654e135cc000effae9112d1702` replaced that role with directly read E000651. Its `claim_ids` reverse links were expanded from C0644/C0645 to C0644/C0645/C0664/C0671, while E000748 was narrowed from C0664/C0671/C0706 to C0706. M0626 and M0632 were updated consistently in `source_ids`, `supporting_source_ids`, source-weight wording and verification wording. A fresh independent scoped re-review found no Critical, Important or Minor issues and declared the provenance finding fully addressed.

## Preservation and verification

- Five changed review rows and one unchanged review row were checked mechanically against baseline `a054c80`.
- M0624/C0663 and every other pre-existing review row remained byte-identical.
- Versioned changes were exactly `_rabota/audit/meta/review.jsonl` plus the two Banatski checkpoint files.
- No fresh web access occurred, and the ratings branch was neither read nor modified.
- `meta_audit.py validate-review`: passed.
- `git diff --check`: passed.
- The full suite was not run, as required by the scoped acceptance brief.
