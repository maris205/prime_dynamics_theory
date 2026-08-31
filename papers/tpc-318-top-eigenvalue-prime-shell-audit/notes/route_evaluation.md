# TPC-318 local route evaluation

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` are absent from this checkout.  This is a local
fail-closed assessment using the project proof package, certificate,
independent replay, stress suite, and Bridge-B checker.

```text
ROUTE_A = NOT_EVALUATED_OFFICIALLY
ROUTE_B = SCOPED_ADVANCE_ONLY
ROUTE_B_TOP_EIGENVALUE_FINITE = YES_16_OF_16
ROUTE_B_DUAL_SOLVER = YES_24_OF_24
ROUTE_B_TRUE_GROWING_LAW = OPEN
ROUTE_B_CLUSTERED_EIGENSPACE = OPEN
ROUTE_B_ARITHMETIC_CANCELLATION = OPEN
ROUTE_B_FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
```

Strongest positive: a finite top-eigenvalue readout is materially sharper than
the TPC-317 trace-power envelope and decreases on all 16 adjacent comparisons.

Strongest obstruction: 10/24 rows have relative top gap below `0.01`, and the
finite normalized convention does not itself pay an unnormalized power saving.

Reusable structure:

```text
literal matrix -> PSD Gram -> dual top spectrum -> Weyl interval
               -> normalized trend -> eigenspace-gap firewall
```

```text
ROUND2_CLUE = AUDIT_THE_TOP_EIGENSPACE_CLUSTER_AND_NORMALIZATION_LAW_BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION
```
