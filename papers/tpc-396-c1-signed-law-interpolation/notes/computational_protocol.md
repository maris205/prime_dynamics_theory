# TPC-396 computational protocol

The producer accumulates the shell in ascending order.  The independent
checker accumulates it in descending order and forms the same four matrix
interpolants independently.  Both use float64 matrices and one BLAS/OpenMP
thread per process.  The parent TPC-395 certificate is parsed canonically and
its code and JSON hashes are checked before endpoint means are used.

The current family is `a_j=6000001+401j`, with selected indices
`(0,8,16,24,32,40)`, three calibration origins, and three holdout origins.
The complete panel is 6 origins x 4 coefficients x 4 normalizations = 96
rows.  Reverse-order numeric replay uses the existing `8e-8` relative
tolerance.  The rational anchor separately proves the interpolation identity
over exact fractions.  Normal and optimized producer, checker, stress, and
Bridge-B outputs must agree byte-for-byte at their declared output interfaces.
