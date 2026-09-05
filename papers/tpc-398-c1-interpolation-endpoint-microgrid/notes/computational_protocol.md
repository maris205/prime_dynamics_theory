# TPC-398 computational protocol

The producer accumulates the prime shell in ascending order.  The independent
checker accumulates it in descending order and independently forms the same
four finite matrix probes.  Both use float64 matrices and one
BLAS/OpenMP thread per process.  Before any current response is summarized,
the TPC-397 producer and canonical certificate are checked against their
normalized-LF SHA-256 locks.

The current family is `a_j=6800001+401j`, with selected indices
`(0,8,16,24,32,40)`, three calibration origins, and three holdout origins.
The complete panel is 6 origins × 4 coefficients × 4 normalizations = 96
rows.  The parent comparison uses the exact rational coordinate
`t=(lambda-3/4)/(1/4)` and TPC-397's frozen `blend_3_4`/`blend_1` means.
Reverse-order numeric replay uses the declared `8e-8` relative tolerance.
The rational anchor separately checks the interpolation identity over exact
fractions.  Normal and optimized producer, checker, stress, and Bridge-B
outputs must agree byte-for-byte at their declared output interfaces.
