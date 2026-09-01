# TPC-327 paper plan

## Question

Does the finite TPC-325/TPC-326 scale-ladder readout survive a third,
independent source origin, and can the finite stability be expressed as a
three-origin envelope range rather than a parent-child comparison?

## Frozen design

Add the disjoint origin `20001` and repeat the four nested source counts
`160,320,640,1280`.  Keep the literal deleted-diagonal centered blocks,
`H=66`, `Q={24,36,54,80}`, exponents `{1,2}`, and all four predeclared sign
laws unchanged.  Compare the new panel with both released origins
`12001` and `16001`.

## Release-bearing progress

1. A new 32-row all-plus profile-majorization certificate.
2. Exact agreement of the four-law profile and energy censuses with both
   earlier origins.
3. A non-vacuous three-origin per-scale envelope range under the already
   frozen TV `<0.001` and energy `<0.005` controls.
4. Independent reverse/einsum reconstruction, residue perturbation stress,
   and a new exact rational anchor.

## Failure policy

Any row mismatch, source overlap, unresolved profile, threshold violation,
zero origin spread, or normal/optimized disagreement is an obstruction and
does not receive a positive triangulation marker.
