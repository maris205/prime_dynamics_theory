# TPC-345 paper plan

## Question

Is the TPC-344 panel-contrast repair a property of the nuisance subspaces, or
does it depend on the chosen coordinates and row weighting?

## Frozen comparison

Use the TPC-341 and TPC-342 panels, the all-plus `Q=54`, exponent-one,
`H=66` operator, nine controls, four masks, and the positive-SVD rank rule.
For each panel and each of two declared weightings, stack the three row-mean
nuisance columns into a finite matrix.  Compare the two column spaces by
principal angles and orthogonal-projector distances.  Project each panel's
twin target onto the other panel's nuisance space, and repeat all geometry
after omitting each control.

## Decision rules

- report a dominant alignment only when the raw leading cosine exceeds `0.99`;
- report a transverse separation when the second cosine is below `0.20` in
  both weightings;
- call weighting stability refuted when the leading angle changes by more
  than 10 degrees;
- call mutual transfer refuted when either direction has residual retention
  at least `0.30`;
- certify coordinate invariance by a fixed nonsingular column shear;
- retain zero arithmetic credit regardless of every finite result.

## Deliverables

- exact finite principal-angle and projector identities;
- raw/equal-row geometry, cross-panel transfer, and 18 LOO angle pairs;
- independent reverse-shell checker and nine-mutation stress;
- proof package, claim firewall, route evaluation, PDF, and Bridge-B audit;
- explicit TPC-346 finite no-go/freeze trigger.
