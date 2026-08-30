# Task 5 — Wikipedia conflicts and absences

## Result

All 18 frozen Wikipedia-risk candidates were reviewed exactly once and appended after the 64 Task 4 records (82 total). Outcomes: 4 `согласован`, 10 `исправлен`, 1 `различается по охвату`, and 3 `остаётся неразрешённым`. The frozen candidate file is byte-identical to `d811103`; `index.html` remains blob `60caf935aed22dca9054283876f9b8949158fa39`.

| Claim | Specialist result | Review result | Evidence |
|---|---|---|---|
| C0001 | OIV supports the place/nature/practice definition. | согласован | E003521, authoritative, OIV |
| C0004 | Basin climate context does not prove a shore frost effect. | остаётся неразрешённым | E003554, authoritative, ICPDR |
| C0010 | Serbian zoning regulation lists Subotički rejon. | согласован | E000046, authoritative, Serbian regulation |
| C0040 | Metohija aggregates two official regions; map is not a full register. | различается по охвату | E000046 |
| C0184 | Genetics leaves crossing location open; early local record is not origin proof. | исправлен | E000146, E000149, E000150 |
| C0305 | 140 m is the winery site; 121 m is the settlement reference. | исправлен | E000247, E000250 |
| C0985 | OIV gives variable, purpose-adapted maceration—not a 24-hour ceiling. | исправлен | E003555, authoritative, OIV |
| C1229 | Local snow/wind is supported; Carpathian contrast is not. | исправлен | E001405, E001410 |
| C1249 | No source gives the precise 1887–89 export series. | остаётся неразрешённым | E003504, specialist history context only |
| C1265 | CEVVIN confirms present regional Gamay, not a 1960s start. | остаётся неразрешённым | E002456, authoritative, CEVVIN |
| C1851 | Neutral basic profile and aromatic modern wines are compatible scopes. | исправлен | E002051, E002052 |
| C1876 | Typical pale Kadarka and darker technical expressions coexist. | исправлен | E002064, E002072 |
| C1889 | Drinking window depends on style, not a universal 2–3 years. | исправлен | E002063, E002064 |
| C1951 | Karlovci is an early documented centre/candidate, not proven birthplace. | исправлен | E002146, E002147 |
| C2183 | 16–18°C dessert service is a supported option, not exclusive. | согласован | E002540, E002541, E002542 |
| C2318 | Light and structured Kadarka have different ageing windows. | исправлен | E002818, E002827, E002819 |
| C2524 | Serbian law uses optional vintage information and 85%, while `berba` is idiomatic. | согласован | E003172, E003224, E003229 |
| C2689 | Cool dessert service is valid, but not universal. | исправлен | E002540, E002541 |

## Changes and sources

- Claim changed: C0985 (removed the false universal 24-hour cap).
- Decision changes: C0184, C0305, C0985, C1229, C1851, C1876, C1889, C1951, C2183, C2318, C2689.
- Existing evidence linked by `claim_ids`: E003521→C0001, E003504→C1249, E002456→C1265, E002540→C2183, E002541→C2689.
- New contiguous evidence IDs: E003554 (ICPDR climate assessment, authoritative; https://www.icpdr.org/publications/future-danube-river-basin) and E003555 (OIV maceration definition, authoritative; https://www.oiv.int/standards/international-code-of-oenological-practices/part-ii-oenological-treatments-and-practices/grapes).

## Verification

`python3 _rabota/audit/meta_audit.py validate-review _rabota/audit --policy _rabota/audit/meta/source_policy.json --candidates _rabota/audit/meta/candidates.jsonl --review _rabota/audit/meta/review.jsonl` — passed.

`python3 -m unittest discover -s _rabota/audit/tests -v` — 76 tests passed after preserving explicit Wikipedia-conflict wording for C0184/C1951.

Coverage checks: 18 frozen queue candidates; 18 matching Task 5 reviews; 64 prior reviews retained; 82 total reviews. Candidate SHA-256 before/after: `812f30bdc7ac9593d211354c4bb66650312884c62d45f9b0223e510d0f586c2d`.

## Self-review and concerns

The review keeps Wikipedia conflicts in comparison rather than treating translations or retellings as independent support. Producer pages are used only for their current own products. C0004, C1249, and C1265 remain unresolved: no local station-pair dataset, primary export ledger, or dated planting register was found. The ICPDR source is context only, not a local frost finding; OIV is a definition, not a rosé recipe prescription.
