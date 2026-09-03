# Bridge-B — TPC-368 second predeclared origin-family replication

## Scope

This bridge records the finite, fail-closed audit for
`papers/tpc-368-predeclared-origin-replication/`.  It is a local repository
bridge, not the absent official Route-A/Route-B evaluator.

## Frozen protocol

The experiment declares the origins `(810001,817061,824121)` as indices
`(0,20,40)` in `810001+353j`, before any signed response, source, law result,
or geometry score is computed.  It evaluates counts `512,1024`, shell
anchors `512,2048,8192`, exponent one, four fixed laws, and beta `0,2`, for
144 rows.

## Certified finite result

```text
TPC368_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC368_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC368_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
TPC368_SECOND_ORIGIN_FAMILY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC368_BETA2_LONG_WINDOW_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC368_BETA2_FAILURE_PATTERN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC368_ORIGIN_UNIFORMITY = OPEN
TPC368_WINDOW_UNIFORMITY = OPEN
TPC368_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC368_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC368_GROWING_OPERATOR_BOUND = OPEN
TPC368_SOURCE_UNIFORM_L2 = OPEN
TPC368_ARITHMETIC_ADVANCE = NO
TPC368_FIXED_POWER_CREDIT = 0
TPC368_FULL_GATE_B = OPEN
TPC368_TWIN_PRIME_RESULT = NONE
```

Beta=2 has 6 spectral-cap and 0 Schur-cap violations in 72 rows; beta=0 has
18 and 18.  The six beta=2 failures are precisely the three declared origins
at count 1024, `Q=2048` and `8192`, exponent one, all-plus law.  The beta=2
maximum is `0.674101905927736` and its maximum Schur value is
`0.70009251108512549`.

## Local acceptance rule

`tpc_bridge_b_tpc368_predeclared_origin_replication_checker.py` locks every
claim-bearing project file, validates the canonical certificate and paper
diagnostics, and runs the producer, independent reverse-order checker, and
adversarial stress checker in normal and optimized modes.  Each subprocess
must return zero with empty stderr, and normal and optimized stdout must be
byte-identical.  A passing bridge is finite evidence only: it does not pay
arithmetic or fixed-power credit and does not close Gate B.
