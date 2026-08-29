# TPC-299 derivation package

Let `U_k` be the first `k` literal source profiles, let `A` contain the
frozen physical shell columns, and write

```
V_k = A^T U_k,       M_k = U_k^T U_k.
```

For a source coefficient vector `c`, the native source budget is

```
||U_k c||_2^2 = c^T M_k c.
```

For `0 <= tau < 1` and a nonzero target `b`, define

```
B_{k,tau}(b)
  = min { c^T M_k c : ||V_k c-b||_2 <= tau ||b||_2 }.
```

The problem is infeasible when the least-squares distance from `b` to
`range(V_k)` exceeds `tau ||b||_2`.  Otherwise put

```
c_lambda = (V_k^T V_k + lambda M_k)^(-1) V_k^T b.
```

After whitening with `y=M_k^(1/2)c` and
`W=V_k M_k^(-1/2)`, this is the ordinary minimum-Euclidean-norm point in
an ellipsoidal target tube.  The KKT equations imply that, whenever the
least-squares residual is strictly below the requested radius and the zero
source is outside it, a unique `lambda>0` makes

```
||V_k c_lambda-b||_2 = tau ||b||_2,
```

and then `B_{k,tau}(b)=c_lambda^T M_k c_lambda`.  At the least-squares
boundary `lambda=0`; if the zero source is already feasible the budget is
zero.

If `U_k` is a prefix of `U_l`, every coefficient vector for `U_k` embeds into
the larger source space without changing its physical output or source
vector.  Therefore

```
B_{l,tau}(b) <= B_{k,tau}(b)
```

whenever both quantities are defined.  This monotonicity is exact, but it
does not say that the budget remains bounded as the shell and profile family
grow.
