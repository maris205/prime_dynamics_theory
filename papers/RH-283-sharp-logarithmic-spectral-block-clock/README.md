# RH-283: Sharp logarithmic spectral block clock

Suppose a normal spectral tail has squared mass
`M_sigma <= C sigma^(-alpha)` and modulus cap `q`, with `q R < 1`.  For
`m_sigma=ceil(a log(1/sigma))`, its logarithmic determinant tail on `|z|<=R`
obeys

```text
Tail <= C q^(-2) sigma^(-alpha) (q R)^m
        / (m (1-q R)).
```

Thus the tail vanishes when

```text
a log(1/(q R)) >= alpha.
```

At equality the decay is only logarithmic.  Below that slope, a diagonal
family consisting of `Theta(sigma^(-alpha))` copies of the eigenvalue `q`
makes the tail diverge.  The mass-and-cap root-rate upper bound is strictly
below one under the strict inequality, so that region uniformly guarantees
the RH-279 condition.  At the repeated-`q` saturation family this boundary
is exact; a particular nonsaturating family may do better.

For the RH-282 constants `alpha=1`, `q=1/2`, `R=7/5`, the critical slope is
`2.803673252...`; the selected slope `4` lies in the strict region.

This is a sharp theorem for the mass-and-cap hypothesis.  It does not assert
that the physical noisy spectrum saturates the counterexample.
