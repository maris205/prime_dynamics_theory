# TPC-299 proof package

## Theorem 1 — native budget frontier

Let `M=U^T U` be positive definite, `V=A^T U`, and let `b != 0`.  For
`0 <= R < ||b||`, define

```
B_R(b) = min { c^T M c : ||V c-b||_2 <= R }.
```

If `dist(b,range(V)) <= R`, the minimum exists and is unique.  If the
least-squares distance is strictly smaller than `R`, then there is a
`lambda > 0` such that

```
(V^T V + lambda M)c_lambda = V^T b,
||V c_lambda-b||_2 = R,
B_R(b) = c_lambda^T M c_lambda.
```

At equality with the least-squares distance, take `lambda=0` and the
least-squares minimizer.  If `R < dist(b,range(V))`, the problem is
infeasible.

### Proof

Set `y=M^(1/2)c` and `W=V M^(-1/2)`.  The problem becomes

```
min ||y||_2^2  subject to  ||Wy-b||_2^2 <= R^2.
```

The feasible set is closed and convex, and the objective is strictly convex,
so the minimizer is unique.  If the constraint is active with a strict
least-squares interior point, the convex KKT conditions are necessary and
sufficient.  With multiplier `lambda`, stationarity is

```
y + lambda W^T(Wy-b) = 0.
```

Returning to `c` gives the displayed normal equation.  Complementary
slackness gives equality in the residual constraint.  If the requested
radius is below the projection distance, no feasible point exists; if it
equals that distance, the least-squares solution is optimal with
`lambda=0`.  The source budget is the objective value after undoing the
whitening.

## Theorem 2 — ridge/spectral frontier

For `lambda>0`, the matrix `V^T V+lambda M` is positive definite.  The
residual of `c_lambda` increases continuously from the least-squares
residual toward `||b||`, while its source norm decreases toward zero, apart
from degenerate components invisible to `V`.  Thus the active multiplier is
unique whenever the target has a nonzero component in `range(V)`.

This follows either by differentiating the whitened singular-value formula
or by diagonalizing `W^T W`.  In an SVD with singular values `sigma_j` and
coordinates `a_j` of the target,

```
||Wy_lambda-b||^2
  = ||b_perp||^2 + sum_j (lambda/(sigma_j^2+lambda))^2 a_j^2,
||y_lambda||^2
  = sum_j (sigma_j/(sigma_j^2+lambda))^2 a_j^2.
```

## Notation erratum recorded by TPC-300

In the displayed ridge path, the parameter called `lambda` is a ridge
parameter `rho`, not the KKT multiplier itself.  If `mu` multiplies the
constraint in the Lagrangian, stationarity is
`M c + mu V^T(Vc-b)=0`, hence the ridge system is
`(V^T V + rho M)c=V^T b` with `rho=1/mu`.  The TPC-299 numerical path uses
`rho`; all of its frontier values remain unchanged.  TPC-300 supplies the
dual formula and an exact rational audit of this reciprocal convention.

## Theorem 3 — nested budget monotonicity

If `U_k` consists of the first columns of `U_l`, then
`range(U_k) subseteq range(U_l)` and the same physical map acts on both
source spaces.  Any feasible `c_k` can be embedded by appending zero
coordinates, preserving both target residual and source vector.  Taking
infima proves `B_{l,R}(b) <= B_{k,R}(b)`.

## Finite numerical consequence

The certificate applies these exact identities to the declared literal
profiles and finite physical operator.  The 70-digit frontier values,
two-stage source-first replay, and exact stress fixtures are numerical
certificates for that finite grid only.  They are not a theorem about a
moving prime shell, a growing cutoff family, arithmetic `L2`, Gate B, or
twin primes.
