# Bridge B: TPC-265 Schur radius to endpoint-budget compiler

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## Continuation

TPC-264 identified the exact residual feasible set after the TPC-263 rank-three
projection.  TPC-265 supplies the missing endpoint interface.  For a projected
center `c` and a Schur residual radius `R`, define

```text
F(c,R)={c+z: |z|<=R}.
```

The exact radial support is

```text
sup_{y in F(c,R)} |y| = |c|+R,
inf_{y in F(c,R)} |y| = max(|c|-R,0).
```

For the free-phase circle `|z|=R`, the supremum is still `|c|+R`.  Alignment
attains the upper endpoint, so norm-only residual information cannot be given a
hidden cancellation discount.

## Endpoint ledger

With

```text
E0=5/3, E*=1997/1200, Delta*=1/400,
```

if both the center and radius lanes have power savings after loss strictly
larger than `Delta*`, the exact Schur envelope is `o(x^E*)`.  Equality is only
power-level borderline and a smaller effective saving does not close the
target.  A fixed logarithmic estimate has zero fixed-power credit because
`x^delta/(log x)^M -> infinity`.

This is a conditional endpoint compiler.  It does not assert that the literal
V59 center or residual radius satisfies the needed power hypotheses.

```text
TPC265_MAXIMUM_CLAIM = PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER
TPC265_ROUTE_ADVANCE = YES_SCOPED_RESIDUAL_RADIUS_BUDGET_COMPILER
TPC265_SCHUR_RADIAL_ENVELOPE = PROVED_EXACT
TPC265_DISK_WORST_CASE = PROVED_EXACT
TPC265_CIRCLE_WORST_CASE = PROVED_EXACT
TPC265_TWO_LANE_ENDPOINT_COMPILER = PROVED_EXACT_CONDITIONAL
TPC265_STRICT_PAYMENT_THRESHOLD = PROVED_EXACT_ONE_OVER_400
TPC265_LOG_CENTER_CREDIT = 0
TPC265_LOG_RADIUS_CREDIT = 0
TPC265_ACTUAL_V59_RADIUS = OPEN
TPC265_ACTUAL_V59_PHASE = OPEN
TPC265_FIXED_POWER_CREDIT = 0
TPC265_ARITHMETIC_ADVANCE = NO
TPC265_L2 = NONE
TPC265_FULL_GATE_B = OPEN
TPC265_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC265_TWIN_PRIME_RESULT = NONE
TPC265_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC265_STATUS = PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER
TPC265_ROUND2_CLUE = TEST_LITERAL_RESIDUAL_RADIUS_OR_PHASE_AGAINST_THE_TWO_LANE_BUDGET
```

The reusable structure is `Schur set -> radial support -> center/radius lanes ->
strict endpoint test`.  The actual V59 residual radius and signed phase remain
open.
