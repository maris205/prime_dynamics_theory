# Bridge-B: TPC-399 C1 endpoint microgrid cross-family replication

This local Bridge-B artifact records finite reproducibility and contract
consistency for TPC-399. It is fail-closed repository evidence, not an
official Route-A or Route-B evaluator decision.

```text
TPC399_SCHEMA = TPC399_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_V1
TPC399_STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_AUDIT
TPC399_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC399_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC399_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED_TPC398
TPC399_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY
TPC399_INTERPOLATION_PANEL = NUMERICALLY CERTIFIED FINITE_96_ROWS
TPC399_ORIGIN_PHASE = NUMERICALLY CERTIFIED FINITE SCOPED
TPC399_PARENT_CROSS_FAMILY_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED
TPC399_SPECTRAL_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
TPC399_SCHUR_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
TPC399_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC399_GROWING_OPERATOR_BOUND = OPEN
TPC399_SOURCE_UNIFORM_L2 = OPEN
TPC399_ARITHMETIC_ADVANCE = NO
TPC399_FIXED_POWER_CREDIT = 0
TPC399_FULL_GATE_B = OPEN
TPC399_TWIN_PRIME_RESULT = NONE
TPC399_ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_THIRD_FAMILY_REPLICATION
```

## Locked finite protocol

TPC-398's direct same-law all-origin means are read from its hash-locked code
and canonical certificate. The current candidate grid is
`a_j=7200001+401j`, `0<=j<41`, with selected indices
`(0,8,16,24,32,40)`. The first three origins are calibration and the last
three are holdout; all use `N=1024`, block length 128, `fixed_c3`, and
`Q=8192`. The four finite probes are `lambda=7/8,15/16,31/32,1`, and the
four normalizations are inherited without response-dependent selection. The
origin-spread and cross-family/transfer caps are fixed at 1%, 3%, and 3%.

## Certificate result

The certificate contains 96 rows and 16 cells. Twelve cells are origin-stable:
all four normalizations pass for `lambda=7/8,15/16,31/32`, while all four fail
at `lambda=1`. Direct same-law cross-family calibration and holdout comparisons
pass in all four laws under every normalization. All 16 within-family
transfers pass. The largest cross-family holdout error is
`0.0027174217101944009`; the largest endpoint origin spread is
`0.062549688932650421`. Spectral and Schur caps fail in zero rows. The
rational anchor proves all four interpolation identities exactly. These are
finite proxy observations only.

## Verification commands

Run `tpc_bridge_b_tpc399_c1_endpoint_microgrid_cross_family_checker.py --check`
from the repository root. The checker locks every project artifact, validates
the TPC-398 parent provenance, canonical JSON, row/summary contracts, claim
firewall, PDF identity, clean LaTeX diagnostics, and normal/optimized producer,
independent reverse-shell, and mutation jobs.

No arithmetic advance or fixed-power credit is assigned. Official evaluator
files are absent, so Route-A is not officially evaluated and Route-B remains
open.
