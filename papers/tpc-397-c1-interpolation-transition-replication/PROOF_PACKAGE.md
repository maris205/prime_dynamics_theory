# TPC-397 proof package

## Proved finite facts

1. The six selected current intervals are pairwise disjoint and disjoint from
   the declared prior c=1 panels through TPC-396.
2. The TPC-396 producer and certificate are normalized-LF hash-locked before
   any parent endpoint mean is read.
3. Grid indices, calibration/holdout roles, count, coefficients, laws,
   normalizations, and caps are response-blind and fixed before readout.
4. At `[6400001,6400014)` with `Q=8` and shell `{11,13}`, the geometry is
   positive, the endpoint matrices are symmetric, and all four rational
   interpolation identities hold exactly.
5. The certificate contains the complete 96-row/16-cell Cartesian panel with
   canonical JSON and row/payload hashes.
6. The independent checker reconstructs the shell in descending order, while
   the 28-case mutation suite rejects altered certificate contracts.

## Numerically certified finite facts

Twelve of sixteen cells pass the one-percent origin-spread rule: all four
normalizations pass for `blend_3_4`, `blend_5_6`, and `blend_11_12`, while none
pass for `blend_1`.  Parent-relative calibration and holdout comparisons pass
in all 16 cells, as do all 16 within-family transfers.  Spectral failures are
`0/96` and Schur failures are `0/96`.

## Strongest obstruction

The alternating endpoint retains a four-to-five-percent origin spread on the
fresh family, while the three interior samples remain below the one-percent
cap in every normalization.  The result replicates endpoint localization on a
fifth family; it does not establish a universal threshold.

## Open theorem and route status

An analytic source-valid explanation, a growing origin-uniform estimate, and
source-uniform arithmetic `L2` remain open.  Route-A and Route-B are not
closed; the official evaluator files are absent from this checkout.  No fixed
power credit, arithmetic advance, or twin-prime conclusion is assigned.

## Reusable structure and next clue

The reusable structure is a hash-locked endpoint interface, exact finite
matrix interpolation, a fresh calibration/holdout family, independent
reverse-order replay, and explicit failure caps.  The next clue is

```text
ROUND2_CLUE = TEST_C1_INTERPOLATION_ENDPOINT_MICROGRID
```
