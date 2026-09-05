# TPC-399 route evaluation

The official Session evaluator files `propose.md`,
`skills/route-a-evaluator.md`, and `skills/route-b-evaluator.md` are absent
from this checkout. Available evidence is the hash-locked TPC-398 parent, the
exact rational anchor, the canonical certificate, independent reverse-shell
replay, mutation stress, PDF QA, and Bridge-B locks.

```text
ROUTE_A = NOT_EVALUATED_OFFICIALLY
ROUTE_B = OPEN
FINITE_RESULT = NUMERICALLY_CERTIFIED_FINITE_SCOPED_CROSS_FAMILY_REPLICATION
INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE
ORIGIN_PHASE = NUMERICALLY CERTIFIED FINITE SCOPED
PARENT_CROSS_FAMILY_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED
SPECTRAL_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
SCHUR_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_THIRD_FAMILY_REPLICATION
```

## Strongest positive result

The frozen same-law TPC-398 means pass both current calibration and holdout
cross-family tests in all 16 cells. The maximum absolute errors are about
`0.010916` and `0.002718`, respectively. All 16 within-family transfers also
pass, and no spectral or Schur row fails.

## Strongest obstruction

The endpoint `blend_1` fails origin stability in all four normalizations, with
maximum spread about 6.22–6.25%, despite close cross-family cohort agreement.
The finite transfer diagnostic and origin-uniformity diagnostic therefore
remain logically separate.

## Open theorem and route status

Source-valid uniformity, a growing operator estimate, and source-uniform
arithmetic `L2` remain open. No fixed-power credit, arithmetic advance, or
twin-prime conclusion is assigned.

## Reusable structure and next clue

The reusable structure is a direct hash-locked same-law interface, exact finite
interpolation, coordinate-disjoint families, reverse-order replay, and separate
origin/transfer gates. The next clue is the third-family replication shown
above.
