# TPC-396 paper plan

## Research question

Does the law-dependent origin obstruction observed in TPC-395 change
continuously under a response-blind interpolation between its all-plus and
alternating finite matrices, and can a finite transition interval be located
on a fresh coordinate-disjoint family?

## Locked design

Use `a_j=6000001+401j`, selected indices `(0,8,16,24,32,40)`, and three
calibration followed by three holdout origins.  Keep `N=1024`, `Q=8192`,
`fixed_c3`, beta two, exponent one, height 66, and the four existing
normalizations fixed before readout.  Construct the four exact coefficients
`0,1/3,2/3,1` from the two endpoint matrices.  Compare current cohort means
with a frozen linear interpolation of the TPC-395 endpoint means.

## Claim classes

`PROVED_EXACT_FINITE` covers parent hashes, grid arithmetic, interval
disjointness, role assignment, rational interpolation identities, and the
declared definitions.  `NUMERICALLY_CERTIFIED_FINITE` covers the 96 finite
rows and aggregate counters under independent reverse-order replay.  The
statement that an asymptotic transition or universal threshold exists remains
`CONJECTURE`/`OPEN`; no arithmetic or Route credit is claimed.

## Decision rule

Keep the caps fixed at 1% for origin spread and 3% for parent-relative and
within-family transfer.  Report each coefficient separately.  A failure at
`lambda=1` is an obstruction, not evidence that an intermediate coefficient
must fail.  The next paper should refine the transition only if this panel
shows a genuine phase boundary; otherwise it should attack reproducibility on
another fresh family.

## Required artifacts

README, derivation/proof packages, producer and independent checker, mutation
stress, canonical certificate, claim/route/protocol/theorem notes, Bridge-B
checker/note, and byte-identical compiled PDFs.
