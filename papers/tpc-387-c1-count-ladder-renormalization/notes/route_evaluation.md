# TPC-387 route evaluation

The Session evaluator files `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` are absent from this checkout. Available local
evidence is recorded fail-closed:

```text
ROUTE_A = OPEN
ROUTE_B = OPEN
FINITE_CERTIFICATE = PASS (producer + independent replay + stress)
NUMERIC_RESULT = FINITE_COUNT_LADDER_SLOPE_REPAIR
FIXED_CAP_TRANSFER = OPEN
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
```
