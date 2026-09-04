# TPC-383 paper plan

## Motivation

TPC-382 found very small all-plus origin spread at matched `N=2048`, but that
observation used row-wise diagonal normalization.  The next minimal question
is whether the spread survives a common scalar geometry normalization.

## Design

1. Freeze a new affine grid and three indices before reading any response.
2. Use a fresh `N=512` window, four 128-point blocks, three Q anchors, and the
   four inherited laws.
3. Build the common raw prime-shell matrices and geometry once per origin/Q.
4. Compare `A_ij/sqrt(g_i g_j)` with `A_ij/G_Q`, where `G_Q` is the pooled mean
   geometry over all three origins at that Q.
5. Audit the origin spread of every law/Q cell under both choices with a fixed
   one-percent cap.

## Decision rule

If all-plus high-Q stability transfers while its mean moves, retain a
shape-versus-calibration separation and test the bandwidth phase diagram.  If
it fails, treat local-normalization magnitude persistence as an obstruction.
In either case keep source validity and Route-B gates open.
