# TPC-291 computational protocol

The exact-rational producer replays the 18 TPC-289 rows and forms every
cross-prime Gram pair.  For each pair it records the sign, exact squared
coherence, exact Schur residual, and exact projection coefficient, and counts
three residual and two coherence thresholds.

The independent checker uses a column-first reverse accumulation order and
compares every row summary and exceptional-pair record.  The stress script
rejects ten mutations.  Normal and optimized invocations must have empty
stderr and byte-identical stdout.
