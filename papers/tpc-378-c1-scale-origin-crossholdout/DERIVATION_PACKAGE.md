# TPC-378 derivation package

## 1. Finite normalized prime-shell object

For `I=[a,a+N-1]` and `p` in `(Q,2Q]`, define

```text
K_p(u,t) = p (p/Q)^2 66^2/(66^2+(u-t)^2)
            (1_{p|(u-t)} - 1/(p-1))
            1_{u!=t} 1_{p not|u} 1_{p not|t}.
```

The all-plus matrix and full-window square-energy geometry are

```text
A(u,t) = sum_p K_p(u,t)
G(u)   = sum_t sum_p K_p(u,t)^2
T(u,t) = A(u,t)/sqrt(G(u)G(t)).
```

For block length 256, let `b(u)=floor((u-a)/256)`.  The inherited c=1
band and its complement are

```text
B_1(u,t) = T(u,t) 1_{|b(u)-b(t)| <= 1},
R_1      = T-B_1.
```

## 2. Exact finite relations

The geometry is a finite sum of nonnegative rational squares.  The exact
13-point anchor at origin 1100001 and `Q=4` verifies positive geometry and
matrix symmetry by rational arithmetic.  The affine-grid indices, endpoint
counts, and all interval-disjointness inequalities are literal finite
integer checks.  Within each origin, the count-1024 interval is a prefix of
the count-2048 interval.  The mask gives `T=B_1+R_1` entrywise.  Therefore,
for a selected unit eigenvector `v` of `T`,

```text
v^T B_1 v + v^T R_1 v = v^T T v.
```

These identities are exact finite algebra and do not imply a bound uniform
in N, a causal direction between blocks, or source validity of G.

## 3. Finite cross-holdout result

The complete panel has rows `(origin,count,Q)` in the Cartesian product of
three origins, two counts, and three Q anchors.  Its failure profile by
count and Q is

```text
[[0,3,3],
 [0,3,3]].
```

Thus 12 of 18 band spectral values exceed 0.64 and none of the 18 band Schur
values exceed 0.83.  The certificate records each full/band spectral,
Frobenius, Schur, eigenmode, residual, and Rayleigh value.

## 4. What this does not derive

The result does not derive origin uniformity, window-scale uniformity,
spectral-magnitude stability, cross-block causality, a growing masked
operator estimate, a source-uniform arithmetic `L2` estimate, a power saving,
Route-B reassembly, or a twin-prime theorem.  It pays zero fixed-power
credit; the finite profile is evidence about this declared model and panel.
