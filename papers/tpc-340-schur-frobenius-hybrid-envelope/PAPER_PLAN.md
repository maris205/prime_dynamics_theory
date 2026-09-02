# TPC-340 paper plan

## Research question

Can the loose sign-free support Frobenius envelope of TPC-339 be sharpened by
combining it with a global Schur bound, without reintroducing covariance signs?

## Frozen design

- Parent: TPC-339 producer and certificate, both hash-locked.
- Six parent windows, the all-plus `Q=54`, exponent-1, `H=66` operator, and
  all nine controls are unchanged.
- For symmetric `A`, set
  `R=max_i sum_j |A(i,j)|`, so `||A||_2^2 <= R^2`.
- Use the hybrid envelope `min(||A[:,S]||_F^2, R^2)` for a vector supported
  on `S`.

## Decision rule

Require zero violations in all 216 records.  Record which branch is active
and whether the Schur branch materially improves the Frobenius envelope.  If
the hybrid remains loose on broad masks, leave the uniform bound open and move
to a structural nuisance-removal test rather than claim a sharp estimate.
