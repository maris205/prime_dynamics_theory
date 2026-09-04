# TPC-389 derivation package

## Finite kernel

For a finite interval `I` and prime shell `q < p <= 2q`, define

```text
K_p(u,t) = p (p/q)^2 H^2/(H^2+(u-t)^2)
           * (1_{u=t (mod p)} - 1/(p-1))
           * 1_{u != t} 1_{p does not divide u} 1_{p does not divide t},
```

with `H=66`.  For each sign law `ell`, the matrix is

```text
M_ell(u,t) = sum_{q < p <= 2q} s_ell(p) K_p(u,t).
```

The row geometry is the exact finite square energy

```text
G(u) = sum_t sum_p K_p(u,t)^2.
```

The local-diagonal normalization is `M(u,t)/sqrt(G(u)G(t))`.  The pooled
normalization divides by the mean of `G` over the three calibration origins at
the same count.  These are modeling choices in the finite proxy; source
validity is open.

## Count-slope interface

For a cell with spectral means `S_768` and `S_1024`, the current-family slope is

```text
alpha_local = log(S_1024/S_768) / log(1024/768).
```

The parent slope `alpha_parent` is read from the hashed TPC-388 certificate
without refitting.  The anchored forecasts are

```text
P_local = S_1024 (1280/1024)^alpha_local,
P_parent = S_1024 (1280/1024)^alpha_parent.
```

The recursive forecast is

```text
P_recursive = S_768 (1280/768)^alpha_parent.
```

For the two holdout origins, `S_1280` is the mean of the observed endpoint
spectral values.  The recorded errors are `S_1280/P - 1`; the predeclared
finite pass condition is absolute error at most `0.03`.

## Status separation

The kernel identities, interval roles, and rational anchor are exact finite
objects.  Matrix values, spectral metrics, and forecast ratios are numerical
finite certificates.  No step supplies a uniform-in-origin, uniform-in-count,
source-native, or arithmetic estimate.
