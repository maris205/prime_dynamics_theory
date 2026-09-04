# TPC-384 computational protocol

```text
grid_start = 1800001; grid_step = 401; grid_count = 41
origin_indices = 0,20,40; origins = 1800001,1808021,1816041
window_count = 512; block_length = 128; block_count = 4
band_cutoffs = 0,1,2,3; Q = 512,2048,8192
exponent = 1; beta = 2; height = 66
laws = all_plus,alternating_index,mod4_character,half_split
normalizations = local_diagonal,pooled_scalar
spread cap = 0.01; spectral cap = 0.64; Schur cap = 0.83
```

The grid, indices, laws, cutoffs, and normalization menu are fixed before any
response or metric read. The current intervals are checked against all prior
coordinate panels. The q=8 anchor is `[1800001,1800014)` with shell `[11,13]`.

The producer, independent reverse-shell replay, and 25-mutation stress test
are run with Python bytecode disabled and one BLAS/OpenMP thread. Normal and
optimized stdout must be byte-identical in the Bridge-B cascade.

Recorded finite census:

```text
rows = 288; cells = 96
stable cells = c0 (6,7), c1 (8,7), c2 (8,8), c3 (8,8)
spectral failures = 0/288; Schur failures = 0/288
```
