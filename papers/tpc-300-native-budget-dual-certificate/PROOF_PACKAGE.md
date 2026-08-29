# TPC-300 proof package

## Theorem 1 — weak native-budget dual

Let M be positive definite, let V and b be finite real data, let R>=0, and
let rho>0.  Define c_rho by

    (V^T V+rho M)c_rho=V^T b

and

    D_rho=(||b||^2-R^2-b^T Vc_rho)/rho.

Then D_rho <= B_R(b), where
    B_R(b)=min{c^T M c:||Vc-b||<=R}
whenever the feasible set is nonempty.

### Proof

Put mu=1/rho.  The matrix in the quadratic Lagrangian

    L(c,mu)=c^T M c+mu(||Vc-b||^2-R^2)

is positive definite, and its unique minimizer is c_rho.  Multiplying the
normal equation by c_rho^T gives

    inf_c L(c,mu)=(||b||^2-R^2-b^T Vc_rho)/rho=D_rho.

For every primal-feasible c, L(c,mu)<=c^T M c; taking the infimum on the
left and then the minimum on the right proves the claim.

## Theorem 2 — strong duality at the active frontier

If dist(b,range(V))<R<||b||, there is a unique rho_*>0 such that
||Vc_rho_*-b||=R, and

    D_rho_*=B_R(b)=c_rho_*^T M c_rho_*.

### Proof

Whiten with y=M^(1/2)c and W=VM^(-1/2).  In singular coordinates, the
residual is

    ||b_perp||^2+sum_j (rho/(sigma_j^2+rho))^2 a_j^2.

It is continuous, starts at the least-squares residual, and tends to
||b||^2; strict increase holds when the target has a visible component.  The
intermediate value theorem gives the unique rho_*.  At this point the
constraint is active and mu=1/rho_* satisfies the KKT conditions.  The convex
Slater condition gives equality of primal and dual values.

## Theorem 3 — reciprocal convention

If mu is the KKT multiplier of the squared residual constraint, then
rho=1/mu.  Thus a path written as

    (V^T V+rho M)c=V^T b

uses a ridge parameter, not the KKT multiplier itself.  This follows directly
from stationarity

    M c+mu V^T(Vc-b)=0.

## Theorem 4 — exact rational certificate compiler

If M,V,b,R^2,rho are rational and rho>0, then c_rho and D_rho are rational.
Exact Gaussian elimination over Q computes both, and the identity in Theorem
1 is an exact arithmetic lower-bound certificate.

## Scope

The finite atlas uses R^2=(1/2)^2|S|, literal source profiles, and the frozen
TPC-299 physical shell.  It is not an asymptotic theorem.
