# TPC-390 derivation package

## Finite object

For each interval `I=[a,a+N)` and prime shell `(Q,2Q]`, define

```text
K_p(u,v) = p (p/Q)^2 H^2/(H^2+(u-v)^2)
            * (1_{p | u-v} - 1/(p-1))
            * 1_{u != v} 1_{p does not divide u} 1_{p does not divide v},
```

with `H=66`.  The row geometry is `G(u)=sum_{p,v} K_p(u,v)^2`.  Each sign
law produces `M_l=sum_p s_l(p)K_p`.  The reported spectral quantity is the
largest absolute eigenvalue after either local-diagonal or calibration-pooled
normalization and the declared block mask.

## Slope interface

Let `S_N` denote the calibration-origin mean of the masked spectral quantity.
The frozen parent exponent `alpha_P` is read from TPC-389.  The local exponent
is

```text
alpha_L = log(S_1280/S_1024) / log(1280/1024).
```

The one-step parent and local predictions are

```text
P_1536 = S_1280 (1536/1280)^alpha_P,
L_1536 = S_1280 (1536/1280)^alpha_L.
```

The recursive composition is explicitly evaluated in two stages:

```text
P_1280^(1) = S_1024 (1280/1024)^alpha_P,
P_1536^(2) = P_1280^(1) (1536/1280)^alpha_P.
```

The direct control is `S_1024 (1536/1024)^alpha_P`.  In exact real
arithmetic these two parent expressions agree; the certificate records their
finite floating-point composition residual as an audit field.  The holdout
ratio is `S_1536/P - 1`, and the cap is `|ratio| <= 0.03`.

## Selection and disjointness

The candidate origins are the affine grid `3000001+401j`, with indices
`0,10,20,30,40` selected before readout.  Calibration and holdout roles are
fixed before response computation.  The producer checks disjointness against
all listed prior panels, including TPC-389's `N=1280` intervals.
