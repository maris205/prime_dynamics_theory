# TPC-304 computational protocol

The producer locks the normalized-LF SHA-256 digests of the TPC-302 producer
and certificate and the TPC-303 producer and certificate.  It selects only
`axis=GROWTH_PATH`, `(scale,H,z)=(512,58,5)`, `Q=(50,60,70,90)`, and exponents
`1,2`.  For each adjacent pair it intersects the sorted prime lists, computes
the integer label inner product, aligns the global sign, and stores all
intermediate labels and mismatch primes.  It independently reads every TPC-303
series to count the three transition groups.

The JSON certificate is canonical sorted-key JSON with a payload hash.  The
independent checker reimplements the crosswalk without importing the producer;
the stress suite exhausts small binary-label cases, global sign flips, and a
zero-correlation tie.
