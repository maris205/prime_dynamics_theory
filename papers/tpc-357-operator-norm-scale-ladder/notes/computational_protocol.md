# TPC-357 computational protocol

## Frozen inputs

- origins: `38423,42010,45597` (inherited from TPC-356)
- counts: `256,512,1024,2048`
- shell anchors: `24,54,80`
- kernel exponents: `1,2`
- height: `66`
- laws: `all_plus`, `alternating_index`, `mod4_character`, `half_split`
- source response: not used
- scale guard: `1e-6`

The Cartesian product has 288 rows.  Schur and Frobenius metrics are
calculated for every raw and normalized law matrix.  Eigenvalue extremes are
calculated for raw and normalized all-plus matrices, producing 144 spectral
metrics.  The producer accumulates shell components in forward order; the
independent checker accumulates them in reverse order.

## Controls

The JSON certificate is canonical and content-hashed.  Parent TPC-355 code,
TPC-356 code, and the TPC-356 certificate are hash-locked.  A rational
two-prime anchor checks symmetry, positive geometry, and exact row-sum data.
The mutation stress test applies 12 altered-document attacks.  Bridge-B later
requires normal/optimized byte-identical checker output.
