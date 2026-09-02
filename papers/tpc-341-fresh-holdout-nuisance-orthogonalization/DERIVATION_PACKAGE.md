# TPC-341 derivation package

For a source class `C` and control `j`, let

```text
y_(C,j) = A P_j beta_C.
```

Let `N` be the matrix whose columns are the control-averaged nuisance
responses

```text
N = [ mean_j y_(B,j), mean_j y_(P,j), mean_j y_(Z,j) ],
```

where `B`, `P`, and `Z` denote non-twin-prime shift, prime-power shift, and
zero-support.  The Euclidean orthogonal projector onto the nuisance span is

```text
P_N = U_r U_r^T,
```

with `U_r` the left singular vectors whose singular values pass the declared
finite rank threshold.  Set

```text
y_T^perp = (I - P_N) y_T,
rho = ||y_T^perp||_2^2 / ||y_T||_2^2.
```

Since `P_N` is an orthogonal projector,

```text
||y_T||_2^2 = ||P_N y_T||_2^2 + ||(I-P_N)y_T||_2^2.       (1)
```

Thus `rho` is a residual-energy fraction.  It is a geometric diagnostic, not
a probability and not a number-theoretic cancellation estimate.

For the hostile leave-one-control-out test, omit control `j`, replace every
nuisance column by its mean over the other eight controls, and apply the
resulting projector to `y_(T,j)` itself.  Denote the resulting fraction by
`rho_j^LOO`.  The training nuisance span and the tested twin output are then
separated by control index, which exposes a mean-fitting artifact if the
in-sample `rho` is small but the held-out `rho_j^LOO` is large.

The numerical rank is the number of singular values larger than
`max(shape)*eps*sigma_max`.  The three fresh rows have effective ranks two,
two, and three: the prime-power nuisance column is exactly zero in the first
two rows and nonzero at `49727` in the third.  This rank variation is retained
in the certificate rather than silently padding a missing class.
