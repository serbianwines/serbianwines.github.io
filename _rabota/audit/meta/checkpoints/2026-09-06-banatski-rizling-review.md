# Independent Banatski rizling review — 2026-09-06

## Independent scope

The reviewer assessed the five substantive decision changes for C0644, C0662, C0664, C0670 and C0671 and separately checked the evidentiary sufficiency of unchanged C0663. The review covered literal claim scope, the separation of product or brand identity from grape synonymy and period-specific blend composition, source competence and independence, exact before/after records, source reverse links and preservation constraints.

## Original finding and correction

The first review of implementation commit `2cb6874658e18102cd7b0b80cb0437b20f2150a4` found one Important provenance issue. E000748 had crawler-blocked access and had not been directly read, so it could not support the exact VIVC synonym claims assigned to C0664 and C0671.

Fix commit `a054c80dbb5a24654e135cc000effae9112d1702` removed E000748 from C0664/C0671 and restored its reverse links to C0706 only. It added C0664/C0671 reverse links to the directly read VIVC record E000651 and updated M0626/M0632 consistently. The fresh scoped re-review found the Important issue fully addressed and reported no Critical, Important or Minor findings.

## Accepted decisions

- C0644: accepted that omission of Temišvarka from checked lists is not evidence of nonexistence; the bounded sourcing caution is appropriate.
- C0662: accepted the removal of “именно они”, the reduced consensus and the refusal to substitute an undated universal recipe.
- C0664: accepted rejection of the categorical “never” claim based on E000747 official nomenclature, directly read E000651 registry evidence and E000749 ampelographic evidence.
- C0670: accepted the two-period evidence for Rhine Riesling in the product while preserving the distinctions from monovarietal status and genetic identity.
- C0671: accepted high consensus for the historical Kreaca synonym based on the separate official, registry and scientific evidence roles.

## Unchanged decision

- C0663/M0624 is sufficiently supported as a qualified product-name conclusion. It remains byte-identical as `self_checked_no_decision_change`, with no `independent_review` object.

## Verdict

**SPEC PASS / QUALITY PASS**
