# TPC-400 proof package

## Proved finite facts

1. The six selected intervals from the `7600001 + 401j` family are pairwise
   disjoint and disjoint from every prior declared panel, including the
   TPC-399 and TPC-398 endpoint families.
2. The TPC-399 producer and canonical certificate are normalized-LF SHA-256
   locked before any parent mean is read.
3. Candidate indices, origins, calibration/holdout roles, count, laws,
   coefficients, normalizations, and caps are fixed response-blind.
4. At `[7600001,7600014)` with `Q=8` and shell `{11,13}`, exact `Fraction`
   arithmetic verifies positive geometry, endpoint symmetry, and all four
   interpolation identities.
5. The canonical certificate contains the complete 96-row/16-cell Cartesian
   panel and row/payload hashes.
6. The independent checker reconstructs the shell in descending order and the
   28-case mutation suite rejects altered certificate contracts.

## Numerically certified finite facts

The third family has 12/16 origin-stable cells: all four normalizations pass
for `lambda=7/8`, `15/16`, and `31/32`, while none pass for `lambda=1`.
Same-law cross-family calibration and holdout comparisons pass for all 16
cells in each cohort, and all 16 within-family transfers pass.  Spectral and
Schur row failures are both `0/96`.

The maximum absolute cross-family calibration errors, in local, pooled, origin,
and frozen order, are respectively
`0.024241880510384561`, `0.027773876023621469`,
`0.027769959109751552`, and `0.027781566566057458`.  The corresponding
holdout maxima are `0.0001317871615125199`, `0.0024016862760729563`,
`0.002385057413556213`, and `0.0024091869655593623`.  The worst within-family
transfer errors are `0.023621593273998487`, `0.024686548607084191`,
`0.024699011166062435`, and `0.024686548607084191`.

## Strongest positive result

The frozen TPC-399 same-law means transfer to the third family in all 16 cells
under both cohort roles and all four normalizations.  Even the largest finite
calibration discrepancy remains just below the declared 3% cap.  This is a
replication of a finite transfer diagnostic, not a source-valid theorem.

## Strongest obstruction

The endpoint `lambda=1` remains origin-unstable in every normalization, with
maximum relative spread between `0.05360449687470719` and
`0.053890672705770762`.  The endpoint calibration error is also the closest
to the 3% cross-family boundary (about 2.78%), showing that cohort agreement
and origin uniformity are separate finite tests.

## Open theorem and route status

An analytic source-valid explanation, a growing origin-uniform estimate, and a
source-uniform arithmetic `L2` bound remain `OPEN`.  The official Session
Route-A/Route-B evaluator files are absent from this checkout; local Bridge-B
evidence is fail-closed finite consistency only.  No fixed-power credit,
arithmetic advance, or twin-prime conclusion is assigned.

## Reusable structure and next clue

The reusable structure is a direct hash-locked same-law interface, exact finite
matrix interpolation, coordinate-disjoint calibration/holdout families,
explicit all-prior interval checking, independent reverse-order replay, and
separate origin and transfer gates.

```text
ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_FOURTH_FAMILY_REPLICATION
```
