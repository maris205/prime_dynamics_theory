# TPC-398 proof package

## Proved finite facts

1. The six selected current intervals are pairwise disjoint and disjoint from
   the declared prior c=1 panels through TPC-397.
2. The TPC-397 producer and certificate are normalized-LF hash-locked before
   either segment endpoint mean is read.
3. Grid indices, calibration/holdout roles, count, coefficients,
   normalizations, and caps are response-blind and fixed before readout.
4. At `[6800001,6800014)` with `Q=8` and shell `{11,13}`, the geometry is
   positive, the endpoint matrices are symmetric, and all four rational
   interpolation identities hold exactly.
5. The certificate contains the complete 96-row/16-cell Cartesian panel with
   canonical JSON and row/payload hashes.
6. The independent checker reconstructs the shell in descending order, and the
   28-case mutation suite rejects altered certificate contracts.

## Numerically certified finite facts

Twelve of sixteen cells pass the one-percent origin-spread rule: all four
normalizations pass for `blend_7_8`, `blend_15_16`, and `blend_31_32`, while
none pass for `blend_1`.  Parent-relative calibration and holdout comparisons
pass in three of four laws for every normalization; the failing law is
`blend_31_32`, with an absolute discrepancy of about 4.5%.  All sixteen
within-family transfers pass.  Spectral and Schur row failures are both
`0/96`.

## Strongest obstruction

The finer panel separates two finite diagnostics.  `blend_31_32` remains
origin-stable but is about 4.5% below the frozen TPC-397 segment interpolation,
whereas `blend_1` is close to the parent endpoint on the cohort comparison but
has a 7.3–7.6% origin spread.  Consequently neither diagnostic supplies a
universal transition location.

## Open theorem and route status

An analytic source-valid explanation, a growing origin-uniform estimate, and
source-uniform arithmetic `L2` remain open.  Route-A is not officially
evaluated because the Session evaluator file is absent from this checkout;
Route-B remains open.  No fixed power credit, arithmetic advance, or
twin-prime conclusion is assigned.

## Reusable structure and next clue

The reusable structure is a hash-locked two-endpoint interface, exact finite
matrix interpolation, a fresh calibration/holdout family, independent
reverse-order replay, and separate origin and parent-relative gates.  The next
clue is

```text
ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_REPLICATION
```
