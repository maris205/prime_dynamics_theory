# TPC-274 computational protocol

The producer imports only the released TPC-268 finite engine for the literal
source, kernel, and parent residual intervals.  It rebuilds the operator matrix
entry by entry, applies the three exact Haar projection vectors columnwise, and
checks `A_perp beta` against the engine output.

All matrix, beta, Frobenius, and envelope quantities are exact `Fraction`
values.  The scalar, source-lane, and output-lane values inherited from the
parent are treated as outward decimal intervals.  The independent checker
repeats the matrix/projection construction without importing the TPC-274
producer.  The stress script rejects five altered claims or thresholds.

Normal and optimized Python executions must have identical stdout and empty
stderr.  No finite row is promoted to an asymptotic exponent.
