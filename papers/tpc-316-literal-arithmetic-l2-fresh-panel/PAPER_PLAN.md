# TPC-316 paper plan

## Research question

Can the literal deleted-diagonal prime-shell formula be instantiated as a
source-level `L2` operator on the fresh TPC-315 panel, and does its exact
finite envelope provide any defensible negative-power credit?

## Claims to establish

1. Define the source-to-output matrix on `I_X` and prove entry rationality.
2. Derive an exact signed-difference and residue-count formula for its
   Hilbert--Schmidt mass.
3. Prove the finite Frobenius interface and the coordinate-column lower
   witness inequality.
4. Recompute both disjoint panels `X=640` and `X=1280` for all eight
   `(Q,s)` rows using exact rational arithmetic.
5. Compare normalized Hilbert--Schmidt envelopes and record the upper/lower
   gap without identifying either envelope with the true operator norm.
6. Independently replay the certificate and attack the counting reduction and
   finite `L2` inequality with direct small-panel checks.

## Deliberate non-claims

The two-panel comparison is finite and same-engine.  It is not a growing
theorem, an estimate for the spectral operator norm, an external holdout, a
canonical weighting law, an arithmetic cancellation result, a fixed-power
credit, a Route-B Gate-B passage, or a twin-prime conclusion.

## Planned artifacts

The producer stores exact rational digests and decimal views in canonical JSON.
The independent checker reimplements the count formula and coordinate columns
without importing the producer.  The stress suite checks every signed
difference on a small interval, compares compressed and direct masses, and
verifies the Frobenius inequality for nontrivial signed vectors.
