# TPC-316 local route evaluation

The Session-named `propose.md` and `skills/route-a-evaluator.md` /
`skills/route-b-evaluator.md` are absent from this checkout.  This is therefore
a local fail-closed assessment using the proof package, canonical certificate,
independent replay, stress suite, and Bridge-B checker.

```text
ROUTE_A = NOT_EVALUATED_OFFICIALLY
ROUTE_B = SCOPED_ADVANCE_ONLY
ROUTE_B_LITERAL_FINITE_L2_ENVELOPE = YES
ROUTE_B_GROWING_ARITHMETIC_L2 = NO
ROUTE_B_TWO_SCALE_OBSTRUCTION = YES_FINITE_8_OF_8
ROUTE_B_OPERATOR_NORM_DECAY = OPEN
ROUTE_B_FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
```

Strongest positive: the actual literal source-to-output matrix now has an
exact finite `L2` envelope and independent replay.

Strongest obstruction: the normalized Frobenius envelope rises on all eight
matched rows and is separated from the coordinate lower witnesses by a large
finite gap on the fresh panel.

Open theorem: replace this loose envelope with a growing true operator-norm or
arithmetic-cancellation estimate.

```text
ROUND2_CLUE = REPLACE_THE_FROBENIUS_ENVELOPE_BY_A_GROWING_OPERATOR_OR_ARITHMETIC_CANCELLATION_ESTIMATE_WITHOUT_IMPORTING_A_POWER_CLAIM
```
