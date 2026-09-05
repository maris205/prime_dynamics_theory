# TPC-395 paper plan

## Research question

Does the TPC-394 alternating-index origin-spread obstruction transfer to a
third fresh affine family when the TPC-394 normalized cell means are frozen as
a parent baseline?

## Locked design

Use the six-origin grid and cohort roles in the producer.  Keep `N=1024`,
`Q=8192`, `fixed_c3`, two laws, and four normalizations fixed before readout.
Measure (i) new-family all-origin spread, (ii) calibration and holdout means
relative to the TPC-394 baseline, and (iii) new-family holdout versus
calibration transfer.  Use 1%, 3%, and 3% caps respectively.

## Claim classes

`PROVED_EXACT_FINITE` covers parent hashes, grid arithmetic, interval
disjointness, role assignment, and definitions.  `NUMERICALLY_CERTIFIED`
covers the 48 finite rows and all aggregate counters.  `OPEN` remains the
source-valid growing origin theorem, arithmetic `L2`, Route closure, and the
twin-prime endpoint.

## Next decision

Because the alternating split transfers across families and normalizations,
the next minimal question is mechanism localization through a predeclared
signed-law interpolation/density panel:
`ROUND2_CLUE=TEST_C1_SIGNED_LAW_INTERPOLATION`.

## Required artifacts

README, derivation/proof packages, source and independent checker, stress
experiment, canonical certificate, claim/route/protocol/theorem notes,
Bridge-B checker/note, and byte-identical compiled PDFs.
