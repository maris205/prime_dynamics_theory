# TPC-344 paper plan

## Question

Does the smallest panel-adaptive relaxation of TPC-343's shared nuisance span
produce a robust finite fit?

## Frozen comparison

Use the hash-locked TPC-341/TPC-342 panels, the all-plus `Q=54`, exponent-one,
`H=66` operator, nine controls, four masks, and the inherited residual guard
`rho < 0.30`.  Compare row-block, one-vector shared, and the six-column
base-plus-panel-contrast basis under raw and equal-row weights.

The panel signs are fixed in advance as `(+1,-1)`.  For nuisance category `j`,
define `b_j` by vertical stacking and `d_j` by signed stacking.  Also run
leave-one-control-out contrast projections and two directional cross-fit
predictions.

## Decision rule

Record a scoped finite pass only if the raw contrast retention is below
`0.30`.  Separately report equal-row sensitivity.  Treat a cross-fit
prediction retention below `0.30` as evidence of transferable low-residual
coefficients; values above it refute that finite transfer criterion.  The
holdout diagnostic remains a hostile test and should retain more than `0.40`.

Regardless of the finite outcome, arithmetic credit remains zero unless a
source-backed growing theorem pays the Route-B losses.

## Deliverables

- exact contrast-to-panel-adaptive span identity and rational anchor;
- 216 raw records, six in-sample rows, 18 contrast holdouts, and four crossfits;
- producer, reverse-shell independent checker, and mutation stress suite;
- proof package, claim firewall, route evaluation, PDF, and local Bridge-B audit;
- explicit next trigger for the principal-angle audit.
