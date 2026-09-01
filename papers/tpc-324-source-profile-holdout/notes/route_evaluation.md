# TPC-324 route evaluation

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` are absent from this checkout.  No official
Route-A or Route-B pass is asserted.

Available fail-closed evidence:

1. exact conditional covariance proof;
2. producer certificate locked to TPC-323;
3. independent reverse/einsum replay on both holdout panels;
4. disjointness, covariance, and nontrivial-offset stress suite;
5. local Bridge-B checker with sealed hashes and normal/optimized equality.

```text
ROUTE_B_LOCAL = YES_SCOPED_SOURCE_LOCATION_HOLDOUT_REPLICATION
ARITHMETIC_ROUTE_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
```
