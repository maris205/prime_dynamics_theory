# RH-286: Finite-radius monodromy cloud centering

RH-275 compared archived noisy clouds with the limiting monodromy radius
`beta=(0.85 sqrt(lambda))^(-1)`.  The exact RH-17 shell at component period
`k` instead has radius

```text
beta_k = |M_k|^(-1/(2k)) / 0.85,
|M_k| = C_M lambda^k (1+o(1)).
```

Consequently

```text
2(k-1) |beta_k-beta| -> beta |log C_M|,
k * 2 |beta_k^n-beta^n| -> n beta^n |log C_M|
```

for every fixed even moment order `n`.  Thus root-`l1` comparison with the
limiting shell contains an order-one accumulated radial bias whenever
`C_M != 1`, while each fixed Fourier moment sees only an `O(1/k)` bias.  This
supports each fixed coefficientwise comparison, not uniform determinant
convergence; the latter still needs a growing weighted-prefix estimate.

Re-auditing the seven RH-15 rows against archived multiprecision
approximations to the exact finite-cycle radii reduces:

- total root error from `0.6424–1.2481` to `0.2841–0.8992`;
- maximum pre-alias moment defect from `0.5096–1.4573` to
  `0.3640–1.0450`.

The improvement is a frozen floating-point finding.  The archived numerical
value `C_M=1.9463429052...` is not an interval certificate, and seven rows do
not prove aggregate noisy-cloud transport.  Trigger 1 remains inactive.
