# Bridge-B — TPC-367 predeclared long-window obstruction

## Scope

This bridge records the finite, fail-closed audit for
`papers/tpc-367-predeclared-long-window-obstruction/`.  It is a local
repository bridge, not the absent official Route-A/Route-B evaluator.

## Frozen protocol

The experiment declares origins `(620001,626141,632281)` as indices
`(0,20,40)` in `620001+307j`, before any signed response or geometry score is
computed.  It evaluates counts `512,1024`, shell anchors `512,2048,8192`,
kernel exponents `1,2`, four fixed laws, and beta `0,2`, for 288 rows.

## Certified finite result

```text
TPC367_ORIGIN_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC367_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC367_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC367_LONG_WINDOW_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC367_UNSELECTED_ORIGIN_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC367_BETA2_LONG_WINDOW_TRANSFER = REFUTED_SCOPED
TPC367_BETA2_EXPONENT_SENSITIVITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC367_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC367_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC367_GROWING_OPERATOR_BOUND = OPEN
TPC367_SOURCE_UNIFORM_L2 = OPEN
TPC367_ARITHMETIC_ADVANCE = NO
TPC367_FIXED_POWER_CREDIT = 0
TPC367_FULL_GATE_B = OPEN
TPC367_TWIN_PRIME_RESULT = NONE
```

Beta=2 has 6 spectral-cap and 0 Schur-cap violations in 144 rows; beta=0 has
36 and 36.  The six beta=2 failures are precisely the three origins at
count 1024, `Q=2048` and `Q=8192`, exponent one, all-plus law.  The maximum
beta=2 spectrum is `0.67410738070824539` and the maximum beta=2 Schur value is
`0.70009945776422788`.

## Local acceptance rule

`tpc_bridge_b_tpc367_predeclared_long_window_obstruction_checker.py` locks
every claim-bearing project file, validates the canonical certificate and
paper diagnostics, and runs the producer, independent reverse-order checker,
and adversarial stress checker in normal and optimized modes.  Each subprocess
must return zero with empty stderr, and normal and optimized stdout must be
byte-identical.  A passing bridge is finite evidence only; it does not pay
arithmetic or fixed-power credit.
