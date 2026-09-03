# Bridge-B — TPC-372 full-window block/off-block decomposition

## Scope

This bridge records the finite, fail-closed audit for
`papers/tpc-372-full-window-offblock-decomposition/`.  It is local repository
evidence, not the absent official Route-A/Route-B evaluator.

## Frozen protocol

TPC-372 inherits the three response-blind origins and the count-2048 window
from TPC-371/TPC-370.  The eight contiguous 256-point blocks are fixed before
any component metric is read.  For each origin and each `Q=512,2048,8192`,
with exponent one, the all-plus law and beta `0,2`, the full-window normalized
matrix `T` is decomposed as

```text
D = P_same-block \odot T,
R = (1-P_same-block) \odot T,
T = D + R.
```

The same full-window square-energy geometry is used for `T`, `D`, and `R`.
The complete panel has 18 rows; no row or component is selected from a
response, source vector, or observed metric.  The exact anchor
`[1010346,1010359)` at `Q=4`, shell `{5,7}`, is inherited and is not a
main-panel selection.

## Certified finite result

```text
TPC372_FULL_WINDOW_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND
TPC372_COMMON_NORMALIZATION = PROVED_EXACT_FINITE
TPC372_DECOMPOSITION_IDENTITY = NUMERICALLY_CERTIFIED_FINITE
TPC372_FULL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC372_BETA2_FULL_FAILURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC372_BLOCK_DIAGONAL_PHASE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC372_OFF_BLOCK_NECESSITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC372_CROSS_BLOCK_CAUSALITY = OPEN
TPC372_ORIGIN_UNIFORMITY = OPEN
TPC372_WINDOW_UNIFORMITY = OPEN
TPC372_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC372_GROWING_OPERATOR_BOUND = OPEN
TPC372_SOURCE_UNIFORM_L2 = OPEN
TPC372_ARITHMETIC_ADVANCE = NO
TPC372_FIXED_POWER_CREDIT = 0
TPC372_FULL_GATE_B = OPEN
TPC372_TWIN_PRIME_RESULT = NONE
```

For beta=2, the full matrix has six high-`Q` spectral-cap failures, while
both `D` and `R` have zero spectral-cap failures.  On each of the six failure
rows, the reverse triangle inequality gives a positive finite lower bound
`||R||_2 >= ||T||_2-||D||_2`; the maximum recorded lower bound is
`0.19398264343312976`.  This identifies a common-normalization sum/coherence
requirement on the declared panel.  It does not establish that `R` is a
causal mechanism, positive, or asymptotically dominant.

## Local acceptance rule

`tpc_bridge_b_tpc372_full_window_offblock_decomposition_checker.py` locks all
claim-bearing project files, validates the canonical certificate and inherited
parent provenance, and runs the producer, independent reverse-shell replay,
and adversarial stress checker in normal and optimized modes.  Every
subprocess must return zero with empty stderr, and normal and optimized stdout
must be byte-identical.  A passing bridge is finite evidence only; it does not
pay arithmetic or fixed-power credit and does not close Gate B.

```text
ROUND2_CLUE = TEST_EIGENMODE_BLOCK_SEPARATION
```
