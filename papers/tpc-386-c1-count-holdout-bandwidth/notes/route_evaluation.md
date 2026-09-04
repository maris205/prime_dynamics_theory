# TPC-386 route evaluation

`propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` are absent from this checkout. Accordingly this
file records the available fail-closed evidence only.

```text
ROUTE_A = OPEN
ROUTE_B = OPEN
FINITE_CERTIFICATE = PASS (after producer + independent replay)
NUMERIC_RESULT = COUNT_HOLDOUT_AND_FIXED_CAP_OBSTRUCTION
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
```

The result is a finite diagnostic for one `c=1` dynamical-system family. It
does not attach a source theorem or pay an asymptotic exponent.
