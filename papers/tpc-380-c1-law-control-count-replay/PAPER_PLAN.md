# TPC-380 paper plan

## Research question

Does the TPC-379 separation between the all-plus prime-shell law and three
diagnostic signed laws survive when the same c=1 construction is replayed at
the larger fixed count `N=2048`?

## Frozen design

Use the response-blind affine grid `a_j=1300001+401j`, `0<=j<41`, and indices
`(0,20,40)`, giving `(1300001,1308021,1316041)`.  Use eight contiguous
256-point blocks, the inherited block-distance-one mask, beta 2, exponent 1,
height 66, and `Q=(512,2048,8192)`.  Compare the four predeclared laws in the
same order as TPC-379.  The complete panel is `3*3*4=36` rows.

## Decision rule

All rows are constructed before the failure profile is read.  Reappearance of
the parent profile is recorded as finite count persistence; disappearance or
law convergence would be a finite obstruction to that interpretation.  No
finite outcome is promoted to scale uniformity or arithmetic source validity.

## Required evidence

1. Exact endpoint disjointness from TPC-376--379.
2. One common square-energy geometry for all four laws.
3. Exact q=8 rational anchor inside the selected first window.
4. Full and c=1 band spectra, Schur/Frobenius envelopes, and Rayleigh split.
5. Direct-sieve reverse-shell replay without importing the producer.
6. Normal/optimized replay, 25 semantic/schema mutations, and local Bridge-B.
7. A compiled PDF and explicit Route-A/Route-B claim firewall.

## Observed target

The response-blind probe gives all-plus profile `(0,3,3)` and signed-control
profiles `(0,0,0)`, with 6/36 spectral failures and no Schur failures.  The
formal certificate is the authority for the final rounded values.

## Next decision

If the profile persists, the smallest next question is a fresh origin-family
replay at the same count and law panel:
`TEST_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY`.
