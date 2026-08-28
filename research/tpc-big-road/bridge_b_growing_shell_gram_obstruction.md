# Bridge B: growing prime shells and the scalar--energy firewall

Date: 2026-08-28

TPC-288 follows TPC-287's finite cancellation ledger on the same literal
deleted-diagonal prime-shell operator.  It retains the full output vector of
each prime component, forms the source-output Gram matrix, and audits the
aggregate physical matrix on its actual active coordinates.  The exact finite
identities are

```text
A_S = sum_q A_q
g_S = sum_q g_q
C_S = sum_q C_q
G_(q,r) = <g_q,g_r>
1^T G 1 = ||g_S||_2^2
```

The finite grid has 34 rows: 16 growth-path rows and 18 source-control rows.
Its largest shell contains 17 primes.  Every output Gram is full rank modulo
`1000000007`, hence positive definite by the exact Gram identity; six selected
aggregate physical active matrices are also full rank.  All 34 rows have
energy ratio `||g_S||^2 / sum_q||g_q||^2 > 1`; in 13 rows the interval-certified
scalar retention upper bound is below `1/10` at the same time.

```text
TPC288_MAXIMUM_CLAIM = PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_SHELL_FULL_RANK_OBSTRUCTION
TPC288_ROUTE_ADVANCE = YES_SCOPED_GROWING_SHELL_GRAM_OBSTRUCTION_AND_FULL_RANK_AUDIT
TPC288_EXACT_OPERATOR_ADDITIVITY = PROVED_EXACT_FINITE
TPC288_EXACT_OUTPUT_GRAM_IDENTITY = PROVED_EXACT_FINITE
TPC288_GRAM_PSD = PROVED_EXACT_FINITE
TPC288_GRAM_FULL_RANK = NUMERICALLY_CERTIFIED_FINITE_34_OF_34
TPC288_OPERATOR_FULL_ACTIVE_RANK = NUMERICALLY_CERTIFIED_FINITE_6_OF_6_SELECTED
TPC288_SCALAR_ENERGY_MISMATCH = NUMERICALLY_CERTIFIED_FINITE_13_ROWS
TPC288_ENERGY_AMPLIFIED = NUMERICALLY_CERTIFIED_FINITE_34_OF_34
TPC288_MAX_SHELL_CARDINALITY = 17
TPC288_GROWING_SHELL_STABILITY = OPEN
TPC288_SOURCE_CONTROL_UNIFORMITY = OPEN
TPC288_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC288_FIXED_POWER_CREDIT = 0
TPC288_FULL_GATE_B = OPEN
TPC288_TWIN_PRIME_RESULT = NONE
TPC288_STATUS = PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_SHELL_FULL_RANK_OBSTRUCTION
TPC288_ROUND2_CLUE = TEST_SOURCE_NATIVE_CROSS_PRIME_GRAM_BOUNDS_BEYOND_FINITE_FULL_RANK_OBSTRUCTION
```

## Claim boundary

The 13-row intersection is a finite obstruction to the shortcut
`small scalar attachment => small physical output energy`.  It is not an
asymptotic counterexample to every collective prime-shell estimate.  Full
rank supplies no uniform smallest-eigenvalue bound, and the finite grid is a
declared modeling choice.  The Session-named Route-A/Route-B evaluator files
are absent from this checkout; the local proof package, independent replay,
stress audit, and fail-closed checker are the scoped fallback.

The next live bridge is a source-native estimate for the cross-prime Gram form,
with the literal source and physical normalization preserved.
