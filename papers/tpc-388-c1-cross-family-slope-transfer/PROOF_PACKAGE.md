# TPC-388 proof package

## PROVED_EXACT_FINITE

- The candidate grid, selected indices, origin roles, count roles, bands, and
  parent-slope freeze are fixed before current-family endpoint readout.
- The current intervals are pairwise disjoint and disjoint from all listed
  prior panels.
- The 13-point rational anchor has positive geometry and symmetric matrices
  for all four laws.
- The TPC-387 parent certificate hash and cell-slope interface are checked.

## NUMERICALLY_CERTIFIED_FINITE

- 256 rows and 32 cells replay in ordinary and optimized Python modes.
- All 32 frozen parent-slope forecasts and all 32 local controls pass the 3%
  finite transfer cap.
- The stability census is `24/32`, `24/32`, `28/32`; the spectral diagnostic
  has 40 finite failures and the Schur diagnostic has none.
- Twenty-five structural certificate mutations are rejected.

## OPEN

The finite transfer does not establish origin-uniformity, count-uniformity,
source-valid normalization, a growing operator bound, or arithmetic `L2`.
Route reassembly and any twin-prime conclusion remain open.
