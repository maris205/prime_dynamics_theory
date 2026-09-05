# Bridge-B: TPC-397 finite c=1 interpolation transition replication

This local Bridge-B artifact records finite reproducibility and contract
consistency for TPC-397.  It is fail-closed repository evidence, not an
official Route-A or Route-B evaluator decision.

```text
TPC397_SCHEMA = TPC397_C1_SIGNED_LAW_INTERPOLATION_V1
TPC397_STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_INTERPOLATION_TRANSITION_REPLICATION_AUDIT
TPC397_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC397_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC397_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC397_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY
TPC397_INTERPOLATION_PANEL = NUMERICALLY CERTIFIED FINITE_96_ROWS
TPC397_ORIGIN_PHASE = NUMERICALLY CERTIFIED FINITE SCOPED
TPC397_PARENT_INTERPOLATED_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED
TPC397_SPECTRAL_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
TPC397_SCHUR_ENVELOPE = NUMERICALLY CERTIFIED FINITE SCOPED ONLY
TPC397_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC397_GROWING_OPERATOR_BOUND = OPEN
TPC397_SOURCE_UNIFORM_L2 = OPEN
TPC397_ARITHMETIC_ADVANCE = NO
TPC397_FIXED_POWER_CREDIT = 0
TPC397_FULL_GATE_B = OPEN
TPC397_TWIN_PRIME_RESULT = NONE
TPC397_ROUND2_CLUE = TEST_C1_INTERPOLATION_ENDPOINT_MICROGRID
```

## Locked finite protocol

The TPC-396 `blend_0` and `blend_1` endpoint means are hash-locked.  The
current candidate grid is `a_j=6400001+401j`, `0<=j<41`, with selected indices
`(0,8,16,24,32,40)`.  The first three origins are calibration and the last
three are holdout; all use `N=1024`, block length 128, `fixed_c3`, and
`Q=8192`.  The four finite probes are `lambda=3/4,5/6,11/12,1`, and the four
normalizations are inherited without response-dependent selection.  The
origin-spread and transfer caps are fixed at 1%, 3%, and 3%.

## Certificate result

The certificate contains 96 rows and 16 cells.  Twelve cells are origin-stable:
all four normalizations pass for `lambda=3/4,5/6,11/12`, while all four fail at
`lambda=1`, with maximum endpoint spreads from `0.043399597037557539` to
`0.048556752880022216`.  Parent-relative calibration and holdout comparisons
pass in all 16 cells.  Within-family transfer also passes in all 16 cells;
the largest holdout error is `0.024669590049843704`, and the finite spectral
and Schur caps fail in zero rows.  The rational anchor proves all four
interpolation identities exactly.  These are finite proxy observations only.

## Verification commands

Use `tpc_bridge_b_tpc397_c1_interpolation_transition_replication_checker.py --check` in
this directory.  The checker locks every project artifact, validates parent
provenance, canonical JSON, row/summary contracts, claim firewalls, PDF
identity, clean LaTeX diagnostics, and normal/optimized producer,
independent-reverse-shell, and mutation jobs.

No arithmetic advance or fixed-power credit is assigned.  Official evaluator
files are absent, so Route-A is not officially evaluated and Route-B remains
open.
