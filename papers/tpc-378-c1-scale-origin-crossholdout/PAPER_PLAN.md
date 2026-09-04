# TPC-378 paper plan

## Question

TPC-377 showed that the finite c=1 failure support survives a nested count
ladder on its established origins.  Does the same support transfer to a new
coordinate-disjoint origin family when the two endpoint scales are tested
together?

## Frozen design

Use the affine candidate grid
`a_j=1100001+401j`, `0<=j<41`, and fix indices `(0,20,40)` before any
response, geometry, or signed metric is read.  This gives origins
`(1100001,1108021,1116041)`, disjoint from the largest TPC-376/TPC-377
intervals.  Freeze counts `(1024,2048)`, contiguous block length 256, the
inherited c=1 band, beta 2, all-plus law, exponent 1, height 66, and
`Q=(512,2048,8192)`.  The panel is the complete 3-by-2-by-3 Cartesian
product, hence 18 rows.

## Decision rule

Compare the count-by-Q profile with the parent profile `(0,3,3)`.  A match is
only a scoped finite transfer of the cap-support pattern.  A mismatch would
be a finite cross-origin or cross-scale obstruction.  Neither outcome is an
asymptotic statement.

## Required audit

1. Check the affine-grid protocol and exact endpoint disjointness.
2. Verify the inherited c=1 mask, positive finite geometry, and exact
   band/tail Rayleigh identity.
3. Evaluate all 18 rows before reading the profile.
4. Rebuild every row with a descending-shell implementation independent of
   the producer.
5. Run normal/optimized replay and 24 schema/firewall mutations.
6. Compile, render, and inspect every PDF page; retain the TPC arithmetic
   claim ceiling.

## Observed decision

The profile is `(0,3,3)` at both counts: 12/18 spectral-cap violations and
0/18 Schur-cap violations.  Thus the parent support transfers on this finite
cross-holdout.  The retention interval is
`0.93759972206138864--0.98046528117382914`; changing magnitudes and
scale-specific normalization prevent a uniformity claim.

The next hostile control is `TEST_C1_CROSSHOLDOUT_LAW_CONTROL`.
