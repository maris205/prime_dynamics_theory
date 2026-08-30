# TPC-313 proof package

## Proposition 1: finite profile positivity

For every scanned prefix, `M_k=U_k^T U_k` is a rational Gram matrix.  The
exact checker verifies its diagonal positivity and the nonsingularity of each
normal system used by the prefix scan and ridge witnesses.

## Proposition 2: first-feasible-prefix certificate

The exact least-squares coefficient on prefix `k` minimizes the residual in
the column image of `W_k`.  The checker records its rational residual square.
For every prefix before `k*` this value is strictly larger than
`R^2=||b||^2/4`; at `k*` it is at most `R^2`.  Therefore `k*` is the first
feasible prefix for the weighted target.  The positive control is checked on
the same prefix and is feasible there.

## Proposition 3: rational primal witness

The stored vector `c_rho` is obtained by exact Gauss--Jordan elimination in
the rational system (1).  Its residual square is checked to be at most `R^2`,
so `c_rho^T M_k c_rho` is an upper bound for the constrained budget.

## Proposition 4: rational dual lower bound

For `mu=1/rho`, the Lagrangian is bounded below by its value at the exact
stationary point `c_rho`.  Expanding the square yields (2).  Weak duality
then gives
`D_rho <= B_{k,tau}(b) <= c_rho^T M_k c_rho`.
The checker verifies the two rational endpoints and their ordering for all 16
cases.

## Proposition 5: directed interval containment

The interval evaluator rounds every operation to the declared `10^-36`
decimal grid.  Endpoint-extrema arithmetic and the positive-denominator
check imply, inductively, that each stored interval contains its exact
rational scalar.  The independent checker recomputes all six interval types
(residual, primal, primal ratio, dual, dual ratio, and gap) and compares their
endpoints.

## Proposition 6: finite threshold separation

The exact dual ratios for all eight weighted targets exceed `1/20000`, and
the exact primal ratios for all eight all-positive controls are below
`1/100000`.  The corresponding outward intervals preserve these strict
inequalities.  This is a finite source-profile statement only.
