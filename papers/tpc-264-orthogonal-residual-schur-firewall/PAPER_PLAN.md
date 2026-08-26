# TPC-264 paper plan

## Research question

TPC-263 proves a source-backed estimate for the rank-three projection
`C_3=<P_3w,P_3g_x>` but leaves
`C_perp=<(I-P_3)w,(I-P_3)g_x>` in the exact identity.  The present paper asks
what the already exposed projection data and residual norms can, and cannot,
determine about that missing scalar.

## Exact target

For an orthogonal projection `P`, fixed projected vectors `p=Pw`, `q=Pg`, and
fixed residual norms `a=||(I-P)w||`, `b=||(I-P)g||`, prove the complete Schur
feasible set for the residual Gram entry
`z=<(I-P)w,(I-P)g>`.

The answer must distinguish complement dimensions zero, one, and at least two.
For complement dimension at least two it is the closed disk `|z|<=ab`; for
dimension one it is the circle `|z|=ab` (when `ab>0`); zero residual norm gives
a singleton.  Consequently the full scalar lies in the disk centered at
`<p,q>` with radius `ab` in the two-dimensional-complement case.

## Deliverables

1. A proof package with the projection decomposition and Schur-complement
   realization theorem.
2. An exact rational producer checking all dimension cases and endpoint/
   interior witnesses.
3. An independent checker and a stress checker with no producer import.
4. A PDF and claim firewall that explicitly labels the result structural and
   does not call the synthetic family a literal prime-shell counterexample.

## Route decision

This is the minimal natural continuation of TPC-263.  It does not attempt to
estimate the actual V59 residual.  Its new contribution is a sharp missing-data
theorem: a future literal result must either shrink the residual norm product
by a fixed power or control its phase/cross-Gram directly.  The endpoint
obligation remains `1/400`.
