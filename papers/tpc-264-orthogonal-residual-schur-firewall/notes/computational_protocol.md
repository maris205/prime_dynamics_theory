# TPC-264 computational protocol

All finite checks use Python's `Fraction` and exact Gaussian-rational pairs.
The producer builds the canonical JSON certificate; the independent checker
reimplements the geometry without importing the producer.  The stress checker
enumerates rational radii, phases, block dimensions, and zero-residual cases.

The two PDF copies are required to be byte-identical.  The release checker
also verifies canonical JSON, frozen source hashes, embedded fonts, text
markers, page count, a warning-free LaTeX log, and normal/optimized child
stdout equality.  No finite fixture is used as asymptotic evidence.
