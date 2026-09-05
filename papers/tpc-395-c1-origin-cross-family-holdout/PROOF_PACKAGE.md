# TPC-395 proof package

## Proved finite facts

1. The six selected intervals are pairwise disjoint and disjoint from the
   declared TPC-394, TPC-393, and earlier recent c=1 panels.
2. The parent code and certificate are exact normalized-LF hash locks, and
   the parent cell means are frozen before current readout.
3. The new grid, origin roles, same count, laws, normalizations, and caps are
   response-blind and predeclared.
4. The rational 13-point anchor has positive geometry and exact symmetry for
   both laws.
5. The Cartesian panel has exactly 48 rows and 8 cells, and the certificate
   has canonical JSON and row/payload hashes.
6. The independent checker reconstructs the rows in descending shell order;
   the 25-case stress suite rejects altered contracts.

## Numerically certified finite facts

The new family has 4/8 within-family origin-stable cells: all four all-plus
cells pass and all four alternating cells fail.  Alternating spreads are
`0.068267525703845117`, `0.067105244599520317`,
`0.067101222970965949`, and `0.067105244599520331` in local/pooled/origin/
frozen order.  Cross-family calibration and holdout comparisons pass in all
8 cells, with maximum holdout error `0.023289195722825839`.  Within-family
holdout transfer also passes in all 8 cells.  Spectral failures are 24/48 and
Schur failures are 0/48.

## Strongest obstruction

The alternating-index origin-spread obstruction transfers from TPC-394 to a
third family and survives all four declared normalizations.  This rules out a
simple explanation based only on one selected origin family or one scalar
normalization, but remains a finite law-dependent observation.

## Open theorem and route status

An analytic source-valid explanation or a growing origin-uniform bound remains
open.  Source-uniform arithmetic `L2`, prime-shell reassembly, Route-A,
Route-B, and the twin-prime endpoint remain open.  No fixed-power credit is
assigned.  Official evaluator files are absent; local Bridge-B is fail-closed
artifact evidence only.

## Reusable structure and next clue

The reusable structure is a hashed parent mean interface plus a fresh
same-count calibration/holdout family, with a law control and independent
reverse-order replay.  The next clue is

```text
ROUND2_CLUE = TEST_C1_SIGNED_LAW_INTERPOLATION
```
