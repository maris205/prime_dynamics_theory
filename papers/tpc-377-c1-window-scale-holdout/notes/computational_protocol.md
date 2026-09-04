# TPC-377 computational protocol

The three TPC-376 holdout origins are retained without response-based
selection. Counts 1024,1536,2048 and their block counts 4,6,8 are fixed
before any row metric is read. The complete 27-row Cartesian panel uses
Q 512,2048,8192, exponent one, beta two, all-plus signs, height 66, and
spectral/Schur caps 0.64/0.83.

The producer locks the TPC-376 code and certificate. The independent
checker rebuilds the shell up to 20000 in descending order and constructs
the all-plus matrix directly. Normal and optimized modes must have empty
stderr and byte-identical summary output.
