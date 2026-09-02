# TPC-346 paper plan

## Question

Does the panel-adaptive nuisance relaxation observed on the two locked panels
survive a genuinely fresh, disjoint panel, or is its raw crossing a finite
overfit?

## Frozen protocol

Add the cutoff-safe origins [44097,44609,45217] as a fresh third panel to the
TPC-341 and TPC-342 panels. Keep scale 1024, row length 512, all-plus
Q=54, exponent one, H=66, four source categories, and the nine
hash-locked bijective controls. Evaluate raw and equal-row weighting.

## Decision rules

- a fresh own-fit is accepted only when its pooled residual retention is below
  0.30 under both weightings;
- a three-panel adaptive fit is called weighting-stable only when it is below
  0.30 under both weightings;
- a transfer law is rejected when every directed panel prediction is above
  0.30, including the leave-one-panel-out fit;
- fresh control stability is rejected when all nine omitted-control projections
  retain at least 0.30;
- all results remain finite and scoped; arithmetic credit stays zero.

## Deliverables

- a fresh third-panel certificate with 324 raw records and 261 nonempty records;
- exact nested-model and projection identities;
- pairwise geometry, directed transfer, leave-one-panel-out, and fresh
  control-LOO readouts;
- an independent reverse-shell replay and ten-mutation hostile stress suite;
- proof package, claim firewall, route evaluation, PDF, and local Bridge-B audit;
- an explicit finite freeze trigger for the panel-adaptive route.
