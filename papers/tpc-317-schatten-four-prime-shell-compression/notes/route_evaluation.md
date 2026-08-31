# TPC-317 local route evaluation

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` are absent from this checkout.  This is a local
fail-closed assessment using the proof package, canonical certificate,
independent replay, stress suite, and the local Bridge-B checker.

```text
ROUTE_A = NOT_EVALUATED_OFFICIALLY
ROUTE_B = SCOPED_ADVANCE_ONLY
ROUTE_B_SCHATTEN4_FINITE_ENVELOPE = YES
ROUTE_B_FINITE_SPECTRAL_COMPRESSION = YES_16_OF_16
ROUTE_B_FROBENIUS_OPPOSITE_TREND = YES_16_OF_16
ROUTE_B_TRUE_OPERATOR_NORM = OPEN
ROUTE_B_ARITHMETIC_CANCELLATION = OPEN
ROUTE_B_FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
```

Strongest positive: the next trace-power envelope is a mathematically valid
finite `L2` interface and is independently replayed on 24 rows.

Strongest obstruction to overinterpretation: the result is numerical on the
large panels and the true top eigenvalue is not yet certified; finite
Schatten-4 compression cannot be promoted to a power saving.

Open theorem: certify the true top eigenvalue, or a uniform trace-power ladder,
while retaining the literal prime-shell arithmetic.

Reusable structure:

```text
literal matrix -> PSD Gram -> trace-power chain -> outward finite interval
               -> opposite HS/Schatten trend -> no-credit firewall
```

```text
ROUND2_CLUE = AUDIT_THE_TRUE_TOP_EIGENVALUE_OR_A_CERTIFIED_TRACE_POWER_LADDER_BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION
```
