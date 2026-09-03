# TPC-373 derivation package

## Full-window object

For `Q<p<=2Q`, define

```text
B_p(u,t) = p * 66^2/(66^2+(u-t)^2)
            * (1_{p|(u-t)} - 1/(p-1))
            * 1_{u!=t} 1_{p not|u} 1_{p not|t}.
```

With `w_p=(p/Q)^beta`, the raw matrix and row geometry are

```text
A(u,t) = sum_p w_p B_p(u,t),
G(u)   = sum_p sum_{s in I} (w_p B_p(u,s))^2,
T(u,t) = A(u,t)/sqrt(G(u)G(t)).
```

The full-window geometry is held fixed for the entire decomposition.

## Block-distance partition

Let `b(i)=floor(i/256)` for the 2048 indices.  Define

```text
L_d(i,j) = 1_{|b(i)-b(j)|=d} T(i,j),   d=0,...,7.
```

The masks are disjoint and exhaustive, so the finite identity
`T=sum_{d=0}^7 L_d` holds entrywise.  For a unit eigenvector `v` selected
by the declared rule and eigenvalue `lambda`, set

```text
c_d = v^T L_d v.
```

Then `sum_d c_d=lambda` follows by linearity.  We also report
`|c_d|/sum_e |c_e|` to distinguish signed reconstruction from absolute
contribution mass.  This latter quantity is descriptive, not a norm
decomposition theorem.

## Numerical checks

The producer checks symmetry, positive finite geometry, spectral envelopes,
unit-vector error, eigen-residual, layer reconstruction, and Rayleigh-sum
error.  A separate checker constructs the shell using its own sieve and
descending accumulation order, then recomputes the full eigensystem and all
layer records.  Tolerances are used only for floating-point replay; the
protocol and certificate hashes are exact.

## Inherited exact anchor

The interval `[1010346,1010359)` at `Q=4`, exponent one, shell `{5,7}` is
rechecked with rational arithmetic for both beta values.  It is inherited
from TPC-372 and is not a selected main-panel row.
