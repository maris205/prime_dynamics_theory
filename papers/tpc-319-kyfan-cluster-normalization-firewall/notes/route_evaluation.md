# TPC-319 local route evaluation

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` are absent from this checkout.  This is a local
fail-closed assessment using the proof package, certificate, independent replay,
stress suite, and Bridge-B checker.

```text
ROUTE_A = NOT_EVALUATED_OFFICIALLY
ROUTE_B = SCOPED_ADVANCE_ONLY
ROUTE_B_KY_FAN_AUDIT = YES_24_ROWS_5_K_VALUES
ROUTE_B_NORMALIZATION_FLIP = YES_80_OF_80_FINITE_TRANSITIONS
ROUTE_B_UNIFORM_NORMALIZATION_LAW = OPEN
ROUTE_B_ARITHMETIC_CANCELLATION = OPEN
ROUTE_B_FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
```

Strongest positive: the finite top-eigenvalue result is upgraded to a variational
top-cluster mass, with all tested normalized and unnormalized directions certified.

Strongest obstruction: the normalized direction is exactly compatible with unnormalized
growth because the source count doubles; the finite data therefore supplies a firewall,
not a saving.

Reusable structure:

```text
literal matrix -> PSD Gram -> Ky Fan mass -> dual interval -> normalization identity
               -> cluster-gap firewall
```

```text
ROUND2_CLUE = AUDIT_A_SCALE_INVARIANT_SPECTRAL_MEASURE_OR_PROVE_A_SOURCE_NORMALIZATION_LAW_BEFORE_ANY_POWER_CLAIM
```
