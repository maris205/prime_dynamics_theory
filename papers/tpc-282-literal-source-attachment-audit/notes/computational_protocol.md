# TPC-282 computational protocol

The producer hash-locks the TPC-275 producer and result and the TPC-268 source
engine.  It reruns all twelve rows, uses canonical sorted-key JSON, and stores
the source scalar and norm intervals as exact rational encodings of the
outward decimal endpoints.  The independent checker does not import the
TPC-282 producer: it reconstructs the source output, projection, scalar, norm,
and cosine interval directly from the frozen source engine.  The stress checker
mutates signs, intervals, provenance, budget, and census fields.

Both ordinary and optimized Python execution must have empty stderr and
identical stdout.  These controls certify reproducibility of a finite artifact,
not an asymptotic arithmetic estimate.
