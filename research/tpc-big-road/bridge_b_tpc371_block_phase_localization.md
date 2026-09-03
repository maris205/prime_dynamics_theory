# Bridge-B — TPC-371 block-local phase localization

## Scope

This bridge records the finite, fail-closed audit for
`papers/tpc-371-block-phase-localization/`.  It is local repository evidence,
not the absent official Route-A/Route-B evaluator.

## Frozen protocol

The three origins `(1010001,1018021,1026041)` are inherited from the fixed
response-blind grid `1010001+401j` at indices `(0,20,40)`.  Each count-2048
window is partitioned into eight fixed contiguous blocks of length 256.  The
shell anchors `Q=512,2048,8192`, exponent one, four fixed laws, and beta
`0,2` are evaluated on every block, giving 576 rows.  No block or parameter is
selected from a response, source vector, law score, or geometry ranking.  The
exact anchor `[1010346,1010359)` at `Q=4`, shell `{5,7}`, is inherited from
TPC-370 and is not used for main-panel selection.

## Certified finite result

```text
TPC371_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND
TPC371_BLOCK_PARTITION = PROVED_EXACT_FINITE_PREDECLARED
TPC371_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC371_BLOCK_LOCAL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_576_ROWS
TPC371_BETA2_BLOCK_PHASE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC371_BETA2_LOCAL_FAILURE = REFUTED_SCOPED
TPC371_CROSS_BLOCK_COHERENCE = OPEN
TPC371_ORIGIN_UNIFORMITY = OPEN
TPC371_WINDOW_UNIFORMITY = OPEN
TPC371_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC371_GROWING_OPERATOR_BOUND = OPEN
TPC371_SOURCE_UNIFORM_L2 = OPEN
TPC371_ARITHMETIC_ADVANCE = NO
TPC371_FIXED_POWER_CREDIT = 0
TPC371_FULL_GATE_B = OPEN
TPC371_TWIN_PRIME_RESULT = NONE
```

All 288 beta=2 block-local rows are below the spectral cap `0.64` and Schur
cap `0.83`; the maximum normalized spectrum is `0.5536333251967529`.  The
beta=0 control has 72 spectral and 72 Schur violations.  TPC-370 nevertheless
has six beta=2 full-window high-`Q`/all-plus failures.  Therefore the narrow
hypothesis that a parent failure must already occur in one independently
normalized 256-point block is refuted on this declared panel.  Because the
normalization changes with the domain, cross-block causality remains open.

## Local acceptance rule

`tpc_bridge_b_tpc371_block_phase_localization_checker.py` locks every
claim-bearing project file, validates the canonical certificate and inherited
anchor, and runs the producer, independent reverse-shell checker, and
adversarial stress checker in normal and optimized modes.  Each subprocess
must return zero with empty stderr, and normal and optimized stdout must be
byte-identical.  A passing bridge is finite evidence only; it does not pay
arithmetic or fixed-power credit and does not close Gate B.

```text
ROUND2_CLUE = TEST_OFF_BLOCK_COHERENCE_DECOMPOSITION
```
