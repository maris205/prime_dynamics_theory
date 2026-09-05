# TPC-397 derivation package

For `p` in `(Q,2Q]`, `Q=8192`, `H=66`, define the finite kernel

```text
K_p(u,v) = p (p/Q)^2 H^2/(H^2+(u-v)^2)
           (1_{p | u-v} - 1/(p-1))
           1_{u != v} 1_{p not|u} 1_{p not|v}.
```

Let `G(u)=sum_{p,v} K_p(u,v)^2`.  The two endpoint matrices are

```text
M_0 = sum_p K_p,
M_1 = sum_p (-1)^index(p) K_p,
```

where `index(p)` is the ascending shell index.  For the four declared probes,

```text
M_lambda = (1-lambda) M_0 + lambda M_1,
lambda in {3/4, 5/6, 11/12, 1}.
```

This identity is exact over the rationals at the 13-point anchor.  It is a
linear algebra construction, not a claim that fractional coefficients define
an arithmetic character or a new sign law.

For each origin, retain block pairs with block-index difference at most three.
The local normalization divides entries by `sqrt(G(u)G(v))`; the other three
divide the base metrics by the declared calibration-pooled, current-origin,
or first-calibration geometry scalar.  Let `S_lambda(o)` be the resulting
masked spectral diagnostic.  The origin spread is
`(max S-min S)/mean S`.  Parent-relative errors compare cohort means with the
same-coefficient linear interpolation of the two TPC-396 endpoint means
(`blend_0` and `blend_1`).

All current origins have `N=1024`; the first three are calibration and the
last three are holdout.  Every conclusion is scoped to this finite proxy.
