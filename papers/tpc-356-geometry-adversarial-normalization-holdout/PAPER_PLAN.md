# TPC-356 paper plan

## Question

Does the response-independent position-aware congruence introduced in
TPC-355 survive a deliberately geometry-adversarial origin selection?

## Frozen design

Scan the 51 origins
`38001 + 211 j`, `0 <= j <= 50`, using only the unsigned pilot geometry at
count 256.  Score an origin by the largest value of
`max_u G_u / min_u G_u` over `Q in {24,54,80}` and `s in {1,2}`.  Sort by
descending score, break ties by the origin, and greedily retain three origins
with pairwise separation at least 1536.  The resulting triple is
`(38423,42010,45597)`.

The response replay then uses the complete TPC-355 protocol: counts
`256,512,1024`, the same three shell anchors, two kernel exponents, and four
fixed sign laws.  No source response is used in selection or normalization.

## Decision rule

The paper reports a finite positive or negative result exactly as observed.
An improvement in the all-plus minimum or mean is a scoped numerical result;
it is not promoted to a uniform origin theorem.  A negative row, if found,
is retained as an obstruction rather than removed.

## Claim budget

The exact statements are finite determinism, response-blind selection,
positive finite geometry, and the finite polarization identity.  The
arithmetic advance, fixed-power credit, source-uniform $L^2$ estimate, and
full Gate B remain open.
