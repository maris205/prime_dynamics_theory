# Bridge-B — TPC-369 third predeclared origin-family audit

## Scope

This bridge records the finite, fail-closed audit for
`papers/tpc-369-third-origin-family-audit/`.  It is a local repository
bridge, not the absent official Route-A/Route-B evaluator.

## Frozen protocol

The candidate origins `(1010001,1018021,1026041)` are indices `(0,20,40)` in
the response-blind grid `1010001+401j`, with the grid and indices fixed before
any signed response, source, law result, or geometry score is computed.  The
audit evaluates counts `512,1024`, shell anchors `512,2048,8192`, exponent
one, four fixed laws, and beta `0,2`, for 144 rows.

The first exact proof anchor `[1010342,1010355)` is deliberately recorded as
a scoped failure: both beta values have a zero geometry row.  The deterministic
unsigned first-positive scan selects `[1010346,1010359)` at offset four.  No
main-panel response is used by this repair.

## Certified finite result

```text
TPC369_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC369_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC369_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
TPC369_THIRD_ORIGIN_FAMILY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC369_BETA2_PHASE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC369_BETA2_FAILURE_PATTERN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC369_INITIAL_ANCHOR_POSITIVITY = REFUTED_SCOPED
TPC369_REPAIRED_ANCHOR_RULE = PROVED_EXACT_FINITE
TPC369_ORIGIN_UNIFORMITY = OPEN
TPC369_WINDOW_UNIFORMITY = OPEN
TPC369_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC369_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC369_GROWING_OPERATOR_BOUND = OPEN
TPC369_SOURCE_UNIFORM_L2 = OPEN
TPC369_ARITHMETIC_ADVANCE = NO
TPC369_FIXED_POWER_CREDIT = 0
TPC369_FULL_GATE_B = OPEN
TPC369_TWIN_PRIME_RESULT = NONE
```

Beta=2 has 6 spectral-cap and 0 Schur-cap violations in 72 rows; beta=0 has
18 and 18.  The six beta=2 failures are precisely the three declared origins
at count 1024, `Q=2048` and `8192`, exponent one, all-plus law.  The beta=2
maximum is `0.67410489800609708`, and its maximum Schur value is
`0.7000873870755715`.  The failure keys agree with the TPC-368 parent
template.  The finite comparison is not an origin-uniform or asymptotic
claim.

## Local acceptance rule

`tpc_bridge_b_tpc369_third_origin_family_audit_checker.py` locks every
claim-bearing project file, validates the canonical certificate, the exact
anchor obstruction/repair, and the paper diagnostics, and runs the producer,
independent reverse-shell checker, and adversarial stress checker in normal
and optimized modes.  Each subprocess must return zero with empty stderr, and
normal and optimized stdout must be byte-identical.  A passing bridge is finite
evidence only: it does not pay arithmetic or fixed-power credit and does not
close Gate B.

```text
ROUND2_CLUE = TEST_COUNT_2048_ORIGIN_PHASE_OR_RESIDUE_PHASE
```
