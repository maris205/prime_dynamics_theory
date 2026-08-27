# TPC-284 computational protocol

The producer locks the TPC-283 code and result and the frozen TPC-268 engine
with normalized LF SHA-256 hashes.  It reads the twelve parent signs, reruns
the operator for each of six controls and two exponents at each of six scales,
and writes canonical sorted-key JSON.  Outward decimal endpoints are stored as
strings and converted to exact `Fraction` values by every checker.

The independent checker does not import the TPC-284 producer.  It loads only
the frozen TPC-268 engine, reconstructs all 72 parameter maps, and compares the
source and `rho^2` intervals, signs, baseline flips, and census.  The stress
checker builds six hostile mutations (interval, sign, control, budget,
provenance, and row deletion) and verifies rejection.

The Bridge-B checker requires all project artifacts, the PDF, normal and
optimized producer/independent/stress runs, empty stderr, and byte-identical
stdout.  These are reproducibility controls for a finite computational result,
not a substitute for an asymptotic proof.
