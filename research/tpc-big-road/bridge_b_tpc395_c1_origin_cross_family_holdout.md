# Bridge-B: TPC-395 c=1 cross-family origin holdout

This local Bridge-B artifact records finite reproducibility and contract
consistency for TPC-395.  It is fail-closed repository evidence, not an
official Route-A or Route-B evaluator decision.

```text
TPC395_SCHEMA = TPC395_C1_ORIGIN_CROSS_FAMILY_HOLDOUT_V1
TPC395_STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_CROSS_FAMILY_HOLDOUT_AUDIT
TPC395_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC395_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC395_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC395_CROSS_FAMILY_PANEL = NUMERICALLY CERTIFIED FINITE_48_ROWS
TPC395_CROSS_FAMILY_MEAN_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED
TPC395_WITHIN_FAMILY_ORIGIN_AUDIT = NUMERICALLY CERTIFIED FINITE SCOPED
TPC395_SPECTRAL_ENVELOPE = REFUTED_ON_DECLARED_FINITE_PANEL
TPC395_SCHUR_ENVELOPE = NUMERICALLY CERTIFIED FINITE SCOPED ONLY
TPC395_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC395_GROWING_OPERATOR_BOUND = OPEN
TPC395_SOURCE_UNIFORM_L2 = OPEN
TPC395_ARITHMETIC_ADVANCE = NO
TPC395_FIXED_POWER_CREDIT = 0
TPC395_FULL_GATE_B = OPEN
TPC395_TWIN_PRIME_RESULT = NONE
TPC395_ROUND2_CLUE = TEST_C1_SIGNED_LAW_INTERPOLATION
```

## Locked finite protocol

The TPC-394 all-origin cell means are the hashed parent baseline.  The new
candidate grid is `a_j=5600001+401j`, `0<=j<41`, with selected indices
`(0,8,16,24,32,40)`.  The first three origins are calibration and the last
three are holdout; all use `N=1024`, block length 128, `fixed_c3`, and
`Q=8192`.  The laws are all-plus and alternating-index, and the four
normalizations are inherited without refitting.  The within-family spread and
both cross-family/transfer caps are fixed at 1%, 3%, and 3%.

## Certificate result

The certificate contains 48 rows and 8 cells.  All-plus is origin-stable in
the new family under all four normalizations; alternating-index fails the 1%
origin rule in all four cells, with maximum spread
`0.068267525703845117`.  Cross-family holdout transfer passes in all 8 cells,
with maximum absolute error `0.023289195722825839`; within-family transfer is
also `8/8`.  The finite spectral cap fails in 24 rows and Schur fails in zero.
These are finite proxy observations only.

## Verification commands

Use `tpc_bridge_b_tpc395_c1_origin_cross_family_holdout_checker.py --check`
in this directory.  The checker validates parent hashes, canonical JSON,
row/summary contracts, claim firewalls, PDF identity, clean LaTeX diagnostics,
and normal/optimized producer, independent reverse-shell, and mutation jobs.

No arithmetic advance or fixed-power credit is assigned.  Official evaluator
files are absent, so Route-A is not officially evaluated and Route-B remains
open.
