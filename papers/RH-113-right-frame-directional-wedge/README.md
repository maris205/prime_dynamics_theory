# RH-113: right-frame directional wedge

RH-112 ruled out global norm-only exterior perturbation.  RH-113 keeps the
recent top-four right singular frame and acts on only those four directions.

For every orthonormal four-frame `Q`,

```text
sqrt(det((KQ)^*(KQ))) <= ||wedge^4 K||_2.
```

If `Yhat` approximates `KQ` within operator radius `epsilon`, the product of
`(sigma_j(Yhat)-epsilon)_+`, divided by a fourth power leading upper bound,
is a rigorous normalized exterior certificate.  Taking `Q` from the recent
right singular vectors and `epsilon=delta` exactly recovers product Weyl.
The framework can improve as soon as the four directional residuals admit a
smaller radius than the global tail.

The scalar action bound is sharp on diagonal contractions.  Conversely, an
arbitrary stale frame can be exactly blind to a nonzero four-volume, so the
recent-frame choice is a necessary structural input rather than bookkeeping.

The five-scale audit has 360 records, no variational or denominator failures,
and no product-formula discrepancies.  The recent frame captures at least
`0.99999531005` of the optimal full four-volume; on all fine packets it is
exact to `3.9e-15`.  The measured frame-tail radius improves the global radius
by as much as `2.40578`, although threshold counts remain unchanged.

This is a reduced directional certificate, not an all-level tail law.  RH-114
will seek a PSD-Rayleigh bound for the directional tail Gramian.
