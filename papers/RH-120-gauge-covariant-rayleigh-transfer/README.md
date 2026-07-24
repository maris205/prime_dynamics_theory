# RH-120: gauge-covariant Rayleigh transfer

RH-120 proves the first cross-level theorem on the directional-Rayleigh
branch.  If an invertible frame gauge `S` satisfies

```text
G' >= a S* G S,        D' <= b S* D S,
```

then the target relative tail constant obeys
`gamma' <= sqrt(b/a) gamma`.  In four dimensions the target frame volume is
at least `a^2 |det S|` times the source volume.  Both factors are attained
simultaneously by a scalar-congruence family, so the theorem is sharp for
this information class.

The full audit checks 4,096 random gauges and a sharp family with zero
failures.  This is transfer algebra, not a proof that the archived physical
sequence admits uniform cross-level constants.

