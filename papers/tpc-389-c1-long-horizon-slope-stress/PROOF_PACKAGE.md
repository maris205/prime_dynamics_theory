# TPC-389 proof package

## PROVED_EXACT_FINITE

* The affine candidate grid and selected indices are fixed before readout.
* Calibration and holdout roles are fixed before current responses.
* Current intervals are pairwise disjoint and disjoint from listed prior
  panels.
* The 13-point rational anchor has positive geometry and symmetric matrices for
  all four sign laws.
* The TPC-388 parent code/certificate hashes and schema are checked.

## NUMERICALLY_CERTIFIED_FINITE

* The producer rebuilds 256 rows and 32 cells in ordinary and optimized modes.
* An independent checker rebuilds the same rows in descending shell order.
* Parent anchored, local-control, and recursive parent forecasts pass 32/32
  under the predeclared 3% cap.
* The stability counts are `24/32`, `27/32`, and `24/32` for `N=768`, `N=1024`,
  and the `N=1280` holdout.
* There are 64 spectral-cap failures and zero Schur-cap failures.
* Twenty-five certificate mutations are rejected.

## OPEN

This package does not prove count-uniformity, origin-uniformity, a valid source
normalization, a growing operator bound, source-uniform arithmetic `L2`, Route
reassembly, or any twin-prime theorem.  The recursive finite pass is not an
asymptotic composition law.
