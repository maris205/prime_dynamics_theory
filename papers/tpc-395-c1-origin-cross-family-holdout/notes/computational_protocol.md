# TPC-395 computational protocol

The producer uses ascending prime-shell order and the independent checker uses
descending order.  Both use float64 finite matrices and one BLAS/OpenMP
thread per process.  The parent certificate is parsed canonically and its
eight cell means are checked before they are used as the baseline.

The current family has six origins from `5600001+401j` at indices
`(0,8,16,24,32,40)`, with three calibration and three holdout origins.  All
origins have `N=1024`; the panel is the complete 2-law x 4-normalization x
6-origin Cartesian product.  Numeric replay tolerates only
`8e-8*max(1,|a|,|b|)` for reverse summation order.  Normal/optimized producer,
checker, and stress outputs are compared by Bridge-B.
