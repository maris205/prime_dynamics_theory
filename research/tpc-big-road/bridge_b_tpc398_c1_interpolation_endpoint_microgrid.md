# Bridge-B: TPC-398 endpoint microgrid

This local Bridge-B artifact records finite reproducibility and contract
consistency for TPC-398.  It is fail-closed repository evidence, not an
official Route-A or Route-B evaluator decision.

```text
TPC398_SCHEMA = TPC398_C1_INTERPOLATION_ENDPOINT_MICROGRID_V1
TPC398_STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_INTERPOLATION_ENDPOINT_MICROGRID_AUDIT
TPC398_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC398_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC398_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC398_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY
TPC398_INTERPOLATION_PANEL = NUMERICALLY CERTIFIED FINITE_96_ROWS
TPC398_ORIGIN_PHASE = NUMERICALLY CERTIFIED FINITE SCOPED
TPC398_PARENT_INTERPOLATED_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED
TPC398_SPECTRAL_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
TPC398_SCHUR_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
TPC398_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC398_GROWING_OPERATOR_BOUND = OPEN
TPC398_SOURCE_UNIFORM_L2 = OPEN
TPC398_ARITHMETIC_ADVANCE = NO
TPC398_FIXED_POWER_CREDIT = 0
TPC398_FULL_GATE_B = OPEN
TPC398_TWIN_PRIME_RESULT = NONE
TPC398_ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_REPLICATION
```

## Locked finite protocol

The TPC-397 `blend_3_4` and `blend_1` all-origin means are hash-locked.  The
current candidate grid is `a_j=6800001+401j`, `0<=j<41`, with selected indices
`(0,8,16,24,32,40)`.  The first three origins are calibration and the last
three are holdout; all use `N=1024`, block length 128, `fixed_c3`, and
`Q=8192`.  The four finite probes are `lambda=7/8,15/16,31/32,1`, and the
four normalizations are inherited without response-dependent selection.  The
origin-spread and parent/transfer caps are fixed at 1%, 3%, and 3%.

## Certificate result

The certificate contains 96 rows and 16 cells.  Twelve cells are
origin-stable: all four normalizations pass for `lambda=7/8,15/16,31/32`,
while all four fail at `lambda=1`.  Parent-relative calibration and holdout
comparisons pass for three of four laws under every normalization; `31/32`
is the failing law and misses the parent by about 4.5%.  All 16 within-family
transfers pass.  The largest endpoint origin spread is about 7.56%, the
largest parent-relative holdout error is `0.044971523016385406`, and the
finite spectral and Schur caps fail in zero rows.  The rational anchor proves
all four interpolation identities exactly.  These are finite proxy
observations only.

## Verification commands

Use `tpc_bridge_b_tpc398_c1_interpolation_endpoint_microgrid_checker.py
--check` in this directory.  The checker locks every project artifact,
validates parent provenance, canonical JSON, row/summary contracts, claim
firewalls, PDF identity, clean LaTeX diagnostics, and normal/optimized
producer, independent-reverse-shell, and mutation jobs.

No arithmetic advance or fixed-power credit is assigned.  Official evaluator
files are absent, so Route-A is not officially evaluated and Route-B remains
open.
