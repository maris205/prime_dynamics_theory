# TPC-381 derivation package: c=1 origin-family replay

## 1. Finite operator

For `I=[a,a+N-1]` and `Q<p<=2Q`, define

```text
K_p(u,t) = p (p/Q)^2 66^2/(66^2+(u-t)^2)
            (1_{p|(u-t)} - 1/(p-1))
            1_{u!=t} 1_{p not|u} 1_{p not|t}.
```

For each declared law `ell`,

```text
A_ell(u,t) = sum_p s_p(ell) K_p(u,t)
G(u)       = sum_t sum_p K_p(u,t)^2
T_ell      = A_ell / sqrt(G(u)G(t)).
```

The four sign vectors are all-plus, alternating shell index, the prime
modulo-4 sign, and the first-half/second-half shell split.  The geometry is
identical for every law.  With eight blocks
`b(u)=floor((u-a)/256)`, the c=1 band is `T_ell` restricted to
`|b(u)-b(t)|<=1`, and the tail is its complement.

## 2. Exact finite statements

The affine grid, selected indices, eight-block partition, law family, and
complete Cartesian panel are literal finite definitions.  The current
2048-point intervals are disjoint from the declared TPC-376--380 intervals by
integer endpoint comparison.  The q=8 anchor `[1400001,1400014)` has shell
`{11,13}`; its geometry is a positive rational sum and every law matrix is
symmetric.  It is the first fixed subinterval of the selected window and is
not a panel-selection rule or a response-dependent repair.

For every selected unit eigenvector `v` of `T_ell`,

```text
v^T B_ell v + v^T R_ell v = v^T T_ell v.
```

This is an exact finite identity, not an asymptotic estimate.

## 3. Origin-family result

The second 36-row `N=2048` origin-family panel has the same failure profiles as
TPC-380:

```text
all_plus          = (0,3,3)
alternating_index = (0,0,0)
mod4_character    = (0,0,0)
half_split        = (0,0,0).
```

There are 6/36 spectral-cap failures and 0/36 Schur-cap failures.  The
all-plus band maximum is about `0.66694427563`; the three signed maxima are
about `0.00776100399`, `0.01205550511`, and `0.21613933977` in declaration
order.  Thus the finite high-Q signature persists across the second origin
family at the same count while
remaining strongly law-dependent.

## 4. Boundary

This result is finite origin-family persistence only.  It does not establish law,
origin, or scale uniformity; source validity of the normalization; cross-block
causality; a growing operator bound; source-uniform arithmetic `L2`; a power
saving; Route-A/Route-B reassembly; or a twin-prime theorem.  The fixed-power
credit remains zero.
