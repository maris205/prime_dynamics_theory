# TPC-292 computational protocol

The producer imports the frozen TPC-291 physical output and evaluates the
same 18 explicit rows.  For every unordered three-prime combination it
forms the exact-rational Gram submatrix, its determinant, all three Schur
projections, edge signs, and projection-sign patterns.  The canonical JSON
stores exact fractions and display decimals.

The independent checker does not call the producer's row builder.  It loads
the frozen TPC-268 engine, accumulates each physical output column-first,
reconstructs the rows, and compares the complete row payload and aggregate
census.  Parent code/result and engine hashes are locked.

The stress script generates a deterministic integer-vector corpus and
enumerates all eight coefficient-sign assignments for every nondegenerate
triple.  Normal and optimized invocations are required to have empty stderr;
the certificate and replay outputs must be byte-stable.
