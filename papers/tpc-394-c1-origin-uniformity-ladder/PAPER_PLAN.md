# TPC-394 paper plan

## Research question

Does the alternating-index origin-spread signal observed in TPC-393 survive
an independently selected, same-count origin ladder, and is it removed by any
of the four already declared scalar/diagonal normalizations?

## Locked design

Use the eight-origin affine grid and the five-calibration/three-holdout roles
recorded in `code/tpc394_c1_origin_uniformity_ladder.py`.  Keep `N=1024`,
`Q=8192`, `fixed_c3`, the two laws, and four normalizations fixed before
readout.  Define the primary origin statistic as `(max-min)/mean` over all
eight origins, with a one-percent cap.  Define a secondary holdout transfer
statistic as holdout mean/calibration mean minus one, with a three-percent cap.

## Claim classes

* `PROVED_EXACT_FINITE`: grid arithmetic, interval disjointness, role
  assignment, matrix symmetry/positive rational anchor, and certificate
  definitions.
* `NUMERICALLY_CERTIFIED`: finite row values, origin-spread census,
  calibration/holdout transfer, and envelope failure/pass counts.
* `OPEN`: source validity, growing origin uniformity, source-uniform
  arithmetic `L2`, Route-A/Route-B closure, and twin-prime consequences.

## Decision rule for TPC-395

If the alternating spread persists on this fresh family, test it on a third
family with a cross-family holdout.  If it disappears, record the obstruction
as family-local and target a minimal replacement for the failed spectral cap.
The current observed result selects the first branch:
`ROUND2_CLUE=TEST_C1_ORIGIN_CROSS_FAMILY_HOLDOUT`.

## Required artifacts

README, this plan, derivation and proof packages, code, independent checker,
stress experiment, canonical certificate, route/claim/protocol/theorem notes,
Bridge-B checker/note, and byte-identical compiled PDFs.
