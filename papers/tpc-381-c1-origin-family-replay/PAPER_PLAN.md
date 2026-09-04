# TPC-381 paper plan: c=1 origin-family replay

## Research question

Does the TPC-380 separation between the all-plus prime-shell law and three
diagnostic signed laws survive on a second predeclared origin family when the
same c=1 construction is held at the fixed count `N=2048`?

## Frozen design

Use the second response-blind affine grid `a_j=1400001+401j`, `0<=j<41`, and indices
`(0,20,40)`, giving `(1400001,1408021,1416041)`.  Use eight contiguous
256-point blocks, the inherited block-distance-one mask, beta 2, exponent 1,
height 66, and `Q=(512,2048,8192)`.  Compare the four predeclared laws in the
same order as TPC-380.  The complete panel is `3*3*4=36` rows.

## Decision rule

All rows are constructed before the failure profile is read.  Reappearance of
the parent profile is recorded as finite origin-family persistence; disappearance
or law convergence is a finite obstruction to that interpretation.  No finite
outcome is promoted to origin/scale uniformity or arithmetic source validity.

## Required evidence

1. Exact endpoint disjointness from TPC-376--380.
2. One common square-energy geometry for all four laws.
3. Exact q=8 rational anchor inside the selected first window.
4. Full and c=1 band spectra, Schur/Frobenius envelopes, and Rayleigh split.
5. Direct-sieve reverse-shell replay without importing the producer.
6. Normal/optimized replay, 25 semantic/schema mutations, and local Bridge-B.
7. A compiled PDF and explicit Route-A/Route-B claim firewall.

## Observed target

The predeclared hypothesis is parent-profile replay: all-plus `(0,3,3)` and
signed-control profiles `(0,0,0)`, with 6/36 spectral failures and no Schur
failures.  The formal certificate is the authority for the final rounded
values; a failure of this hypothesis is itself a valid scoped obstruction.

## Next decision

If the profile persists, the smallest next question is an origin-family
magnitude/normalization audit:
`TEST_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT`.
