# Roadmap after RH-192

The literal full-Frobenius Riesz target is removed:

```text
matrix state H_F = C^(n x m), L_A X = AX
  -> m-fold spectral multiplicity
  -> no complement-free rank-1/rank-4 shell
```

The surviving route is source relative:

```text
K_S = span{S, AS, A^2S, ...}                 [next]
  -> source/observation minimal quotient      [open]
  -> physical root matching                   [open]
  -> canonical source-channel packet          [open]
  -> all-level transport and Gate A            [open]
```

Any later use of the full Frobenius operator must retain the `m`-fold Riesz
rank.  A low-rank packet can only be a cyclic/source-observable channel, not
the complete ambient Riesz projection.
