# RH-323: Oriented paired affine Gaussian chain

Starting from the RH-322 endpoint profile

```text
V ~ g_d(v) = phi(v-d) / Phi(d),  v >= 0,
```

this paper retains the signs of the next two tangent legs:

```text
U = -alpha*V - Z1,
W = -lambda*U + Z2
  = kappa_aff*V + beta*Z,
```

where `alpha = 2*u_c`, `kappa_aff = 2*u_c*lambda`, and
`beta^2 = 1 + lambda^2`.  The joint density is

```text
J_d(v,u,w) = g_d(v) phi(u+alpha*v) phi(w+lambda*u).
```

The affine Markov lift is an exact `L1` isometry while the entrance variable
is retained.  Seeding it with the exact finite RH-322 folded row gives

```text
||J_(sigma,a) - J_d||_1
  = ||h_(sigma,a) - g_d||_1
  <= |a-d| + 2*normal_survival(1/sigma-a)/Phi(a).
```

Every marginal obeys the same upper bound by Markov contraction.  The
intermediate and output marginals are explicit extended-skew-normal
densities, and the output is not an ordinary Gaussian for any finite
clearance phase.  At `d=0`, the two unconditional orientation-leakage
probabilities are

```text
P(U > 0) = 0.0997061646699731...
P(W < 0) = 0.1147638712758368...
```

These are local probability statements, not parity weights.  The affine
lift is not the actual finite-noise two-step physical kernel: curvature,
fold-switch, and row-normalization remainders remain for RH-324.  The
neighboring sibling, parity cancellation, moving-order remainder, and full
trace replacement are not combined.  Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf oriented-paired-affine-gaussian-chain.pdf
```
