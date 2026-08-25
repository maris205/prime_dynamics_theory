# Computational protocol

The producer writes one canonical strict JSON certificate from exact rational
and Gaussian-rational fixtures.  The independent checker imports no producer
code, reconstructs the Gram and pseudoinverse identities, validates strict
types and canonical bytes, and rejects semantic and digest-rebound mutations.

The stress checker enumerates full-row-rank integer probe matrices, computes
their Gram pseudoinverses by exact rational arithmetic, and verifies the four
Moore--Penrose identities and minimum-energy law.  Normal and optimized runs
must have empty stderr and byte-identical stdout.
