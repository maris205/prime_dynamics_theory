# RH-123: defect-stable Rayleigh recurrence

RH-123 proves the additive-error form of the cross-level theorem.  If the
target recent Gram retains an `a(1-eta)` fraction of the gauged source Gram
and the target tail is bounded by `b` times the gauged source tail plus
`delta` times that Gram, then

```text
gamma_next^2 <= (b gamma^2 + delta) / (a(1-eta)).
```

The formula is sharp in dimension one and becomes an affine recurrence.
The 4,096-instance audit has zero failures.  Physical uniform coefficients
are not yet proved.

