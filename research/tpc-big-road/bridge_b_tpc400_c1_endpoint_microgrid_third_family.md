# Bridge-B: TPC-400 third-family endpoint microgrid replication

This local Bridge-B artifact records finite reproducibility and contract
consistency for TPC-400. It is fail-closed repository evidence, not an
official Route-A or Route-B evaluator decision.

```text
TPC400_SCHEMA = TPC400_C1_ENDPOINT_MICROGRID_THIRD_FAMILY_V1
TPC400_STATUS = NUMERICAL_OBSERVATION_FINITE_C1_ENDPOINT_MICROGRID_THIRD_FAMILY_AUDIT
TPC400_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC400_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC400_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED_TPC399
TPC400_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY
TPC400_INTERPOLATION_PANEL = NUMERICAL OBSERVATION FINITE FLOAT64_96_ROWS
TPC400_ORIGIN_PHASE = NUMERICAL OBSERVATION FINITE FLOAT64 SCOPED
TPC400_PARENT_CROSS_FAMILY_TRANSFER = NUMERICAL OBSERVATION FINITE FLOAT64 SCOPED
TPC400_SPECTRAL_ENVELOPE = NUMERICAL_OBSERVATION_FINITE_FLOAT64_SCOPED_ONLY
TPC400_SCHUR_ENVELOPE = NUMERICAL_OBSERVATION_FINITE_FLOAT64_SCOPED_ONLY

The spectral and Schur diagnostics are reproducible float64 observations.  No
interval eigenvalue enclosure or propagated rounding certificate is claimed.
TPC400_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC400_GROWING_OPERATOR_BOUND = OPEN
TPC400_SOURCE_UNIFORM_L2 = OPEN
TPC400_ARITHMETIC_ADVANCE = NO
TPC400_FIXED_POWER_CREDIT = 0
TPC400_FULL_GATE_B = OPEN
TPC400_TWIN_PRIME_RESULT = NONE
TPC400_ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_FOURTH_FAMILY_REPLICATION
```

## Locked finite protocol

TPC-399's direct same-law all-origin means are read from its hash-locked code
and canonical certificate. The current candidate grid is
`a_j=7600001+401j`, `0<=j<41`, with selected indices
`(0,8,16,24,32,40)`. The first three origins are calibration and the last
three are holdout; all use `N=1024`, block length 128, `fixed_c3`, and
`Q=8192`. The four finite probes are `lambda=7/8,15/16,31/32,1`, and the
four normalizations are inherited without response-dependent selection. The
origin-spread and cross-family/transfer caps are fixed at 1%, 3%, and 3%.
The disjointness check includes all prior declared endpoint panels.

## Certificate result

The certificate contains 96 rows and 16 cells. Twelve cells are origin-stable:
all four normalizations pass for `lambda=7/8,15/16,31/32`, while all four fail
at `lambda=1`. Direct same-law cross-family calibration and holdout comparisons
pass in all four laws under every normalization. All 16 within-family
transfers pass. The largest cross-family calibration error is
`0.027781566566057458`; the largest holdout error is
`0.0024091869655593623`; the largest endpoint origin spread is
`0.053890672705770762`. Spectral and Schur caps fail in zero rows. The
rational anchor proves all four interpolation identities exactly. These are
finite proxy observations only.

## Verification commands

Run `tpc_bridge_b_tpc400_c1_endpoint_microgrid_third_family_checker.py --check`
from the repository root. The checker locks every project artifact, validates
the TPC-399 parent provenance, canonical JSON, row/summary contracts, claim
firewall, PDF identity, clean LaTeX diagnostics, and normal/optimized
producer, independent reverse-shell, and mutation jobs.

No arithmetic advance or fixed-power credit is assigned. Official evaluator
files are absent, so Route-A is not officially evaluated and Route-B remains
open.
