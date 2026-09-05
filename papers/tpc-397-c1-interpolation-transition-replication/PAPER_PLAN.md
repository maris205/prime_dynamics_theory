# TPC-397 paper plan

## Research question

Does the finite transition seen between `lambda=2/3` and `lambda=1` in
TPC-396 persist when the interior is sampled at `3/4`, `5/6`, and `11/12` on
an independent coordinate-disjoint family?

## Locked design

Use `a_j=6400001+401j`, selected indices `(0,8,16,24,32,40)`, and three
calibration followed by three holdout origins.  Keep `N=1024`, `Q=8192`,
`fixed_c3`, beta two, exponent one, height 66, and the four existing
normalizations fixed before readout.  Construct the four exact coefficients
`3/4,5/6,11/12,1` from the two endpoint matrices.  Compare current cohort
means with a frozen linear interpolation of the TPC-396 `blend_0` and
`blend_1` endpoint means.

## Claim classes

`PROVED_EXACT_FINITE` covers parent hashes, grid arithmetic, interval
disjointness, role assignment, rational interpolation identities, and the
declared definitions.  `NUMERICALLY_CERTIFIED_FINITE` covers the 96 finite
rows and aggregate counters under independent reverse-order replay.  The
statement that an asymptotic endpoint transition or universal threshold exists remains
`CONJECTURE`/`OPEN`; no arithmetic or Route credit is claimed.

## Decision rule

Keep the caps fixed at 1% for origin spread and 3% for parent-relative and
within-family transfer.  Report each coefficient separately.  If the three
interior coefficients pass while `lambda=1` fails again, the next paper
should use an endpoint microgrid; if an interior coefficient fails, the next
paper should reproduce that first crossing on a fresh family.

## Required artifacts

README, derivation/proof packages, producer and independent checker, mutation
stress, canonical certificate, claim/route/protocol/theorem notes, Bridge-B
checker/note, and byte-identical compiled PDFs.
