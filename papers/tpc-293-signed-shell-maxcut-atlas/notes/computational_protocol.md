# TPC-293 computational protocol

The producer imports the frozen TPC-291 physical-output helper, whose source,
deleted diagonal, kernel, and prime list are inherited from TPC-268. It
evaluates the explicit 18-row grid, forms each shell Gram matrix with exact
integer/rational arithmetic, converts nonzero off-diagonal entries to signs,
and enumerates every coefficient-sign labeling after fixing the first label.

The independent checker imports only the frozen TPC-268 engine. It computes
the same source weights and physical outputs with source-coordinate-first
accumulation, reconstructs every signed edge, max-cut witness, triangle count,
and aggregate, and compares the complete row payload to the certificate. It
does not import the TPC-293 producer.

The stress script reads no certificate. It exhaustively enumerates all
33,864 signed graphs on 3--6 vertices, all sign assignments modulo global
reversal, deterministic switching transforms, and the triangle parity test;
it also checks the all-positive formula for `m=3,...,12`.

Normal and optimized Python invocations are required to produce empty stderr
and byte-identical stdout. Parent code/result hashes and the frozen engine
hash are locked in both the producer and independent checker.
