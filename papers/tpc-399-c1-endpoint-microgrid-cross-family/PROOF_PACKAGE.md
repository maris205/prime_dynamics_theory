# TPC-399 proof package

## Proved finite facts

1. The six selected intervals from the `7200001 + 401j` family are pairwise
   disjoint and disjoint from the declared prior panels.
2. The TPC-398 producer and canonical certificate are normalized-LF
   SHA-256-locked before any parent mean is read.
3. Candidate indices, origins, calibration/holdout roles, count, laws,
   coefficients, normalizations, and caps are fixed response-blind.
4. At `[7200001,7200014)` with `Q=8` and shell `{11,13}`, exact `Fraction`
   arithmetic verifies positive geometry, endpoint symmetry, and all four
   interpolation identities.
5. The canonical certificate contains the complete 96-row/16-cell Cartesian
   panel and row/payload hashes.
6. The independent checker reconstructs the shell in descending order and the
   28-case mutation suite rejects altered certificate contracts.

## Numerically certified finite facts

The second family has 12/16 origin-stable cells: all four normalizations pass
for `7/8`, `15/16`, and `31/32`, while none pass for `1`. Same-law
cross-family calibration and holdout comparisons pass for all 16 cells each,
and all 16 within-family transfers pass. Spectral and Schur row failures are
both `0/96`.

## Strongest positive result

The frozen TPC-398 same-law means transfer to the fresh family with maximum
absolute calibration error at most `0.010916` and maximum absolute holdout
error at most `0.002718`, uniformly over the four normalizations. This is a
finite replication of a transfer diagnostic, not a source-valid theorem.

## Strongest obstruction

The endpoint `lambda=1` remains origin-unstable, with maximum relative spread
between `0.062219` and `0.062550`, even though its cross-family cohort errors
remain below 1.1% in calibration and 0.28% in holdout. Cross-family mean
agreement therefore does not imply origin uniformity.

## Open theorem and route status

An analytic source-valid explanation, a growing origin-uniform estimate, and a
source-uniform arithmetic `L2` bound remain `OPEN`. The official Session
Route-A/Route-B evaluator files are absent from this checkout; local Bridge-B
evidence is fail-closed finite consistency only. No fixed-power credit,
arithmetic advance, or twin-prime conclusion is assigned.

## Reusable structure and next clue

The reusable structure is a direct hash-locked same-law interface, exact finite
matrix interpolation, coordinate-disjoint calibration/holdout families,
independent reverse-order replay, and separate origin and transfer gates.

```text
ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_THIRD_FAMILY_REPLICATION
```
