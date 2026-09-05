# Bridge-B: TPC-396 finite c=1 signed-law interpolation

This local Bridge-B artifact records finite reproducibility and contract
consistency for TPC-396.  It is fail-closed repository evidence, not an
official Route-A or Route-B evaluator decision.

```text
TPC396_SCHEMA = TPC396_C1_SIGNED_LAW_INTERPOLATION_V1
TPC396_STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_SIGNED_LAW_INTERPOLATION_AUDIT
TPC396_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC396_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC396_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC396_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY
TPC396_INTERPOLATION_PANEL = NUMERICALLY CERTIFIED FINITE_96_ROWS
TPC396_ORIGIN_PHASE = NUMERICALLY CERTIFIED FINITE SCOPED
TPC396_PARENT_INTERPOLATED_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED
TPC396_SPECTRAL_ENVELOPE = REFUTED_ON_DECLARED_FINITE_PANEL
TPC396_SCHUR_ENVELOPE = NUMERICALLY CERTIFIED FINITE SCOPED ONLY
TPC396_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC396_GROWING_OPERATOR_BOUND = OPEN
TPC396_SOURCE_UNIFORM_L2 = OPEN
TPC396_ARITHMETIC_ADVANCE = NO
TPC396_FIXED_POWER_CREDIT = 0
TPC396_FULL_GATE_B = OPEN
TPC396_TWIN_PRIME_RESULT = NONE
TPC396_ROUND2_CLUE = TEST_C1_INTERPOLATION_TRANSITION_REPLICATION
```

## Locked finite protocol

The TPC-395 all-plus and alternating endpoint means are hash-locked.  The
current candidate grid is `a_j=6000001+401j`, `0<=j<41`, with selected indices
`(0,8,16,24,32,40)`.  The first three origins are calibration and the last
three are holdout; all use `N=1024`, block length 128, `fixed_c3`, and
`Q=8192`.  The four finite probes are `lambda=0,1/3,2/3,1`, and the four
normalizations are inherited without response-dependent selection.  The
origin-spread and transfer caps are fixed at 1%, 3%, and 3%.

## Certificate result

The certificate contains 96 rows and 16 cells.  Twelve cells are origin-stable:
all four normalizations pass for `lambda=0,1/3,2/3`, while all four fail at
`lambda=1`, with maximum endpoint spreads from `0.089422016482946329` to
`0.094070438394687927`.  Parent-relative holdout comparisons pass in all 16
cells.  Within-family transfer passes locally in 4/4 cells and in 3/4 cells
for each scalar normalization; the largest error is
`0.030792985412898766`.  The finite spectral cap fails in 24 rows and Schur
fails in zero.  The rational anchor proves all four interpolation identities
exactly.  These are finite proxy observations only.

## Verification commands

Use `tpc_bridge_b_tpc396_c1_signed_law_interpolation_checker.py --check` in
this directory.  The checker locks every project artifact, validates parent
provenance, canonical JSON, row/summary contracts, claim firewalls, PDF
identity, clean LaTeX diagnostics, and normal/optimized producer,
independent-reverse-shell, and mutation jobs.

No arithmetic advance or fixed-power credit is assigned.  Official evaluator
files are absent, so Route-A is not officially evaluated and Route-B remains
open.
