# TPC-385 computational protocol

```text
grid_start = 2000001; grid_step = 401; grid_count = 41
selected indices = 0,10,20,30,40
calibration indices = 0,10,20; holdout indices = 30,40
window_count = 512; block_length = 128; block_count = 4
band_cutoffs = 2,3; Q = 2048,8192
exponent = 1; beta = 2; height = 66
laws = all_plus,alternating_index,mod4_character,half_split
normalizations = local_diagonal,pooled_train_scalar
spread cap = 0.01; forecast-error cap = 0.01
spectral cap = 0.64; Schur cap = 0.83
```

The TPC-384 producer and canonical certificate are hash-locked before the
new panel is read. The parent all-plus high-Q values are forecasts, not
parameters fitted to TPC-385. For pooled normalization, the scalar at each Q
is computed from the three calibration origin geometries only.

The producer, independent reverse-shell replay, and 25-mutation stress test
run with bytecode disabled and one BLAS/OpenMP thread. Normal and optimized
stdout must agree in the Bridge-B cascade.

Recorded finite census:

```text
rows = 160; cells = 32
calibration stable cells = 26/32; holdout stable cells = 28/32
all-plus Q=8192 forecast cells within one percent = 4/4
spectral failures = 0/160; Schur failures = 0/160
```
