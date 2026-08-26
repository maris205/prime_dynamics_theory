# TPC-271 computational protocol

The producer imports the exact finite engine released with TPC-269 and computes
`C_perp`, `W_perp`, `G_perp`, `R^2`, `Xi`, `Xi_W`, `Xi_G`, and `Xi_C` using
outward rational intervals. The independent checker has no producer import: it
rebuilds the prime sieve, factorization, Mobius values, beta source,
shifted-prime comparison, prime shell, two kernels, projection, and normalized
coordinates in floating point.

The stress script rechecks all four lane threshold classes, all nine negative
phase labels, the `96->192` output spike, and three deliberate metadata or
asymptotic-promotion mutations. Normal and optimized Python outputs must be
byte-identical with empty stderr.
