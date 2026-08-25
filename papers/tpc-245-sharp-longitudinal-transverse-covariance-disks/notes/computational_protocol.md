# TPC-245 computational protocol

- All certificate arithmetic is exact over Gaussian rationals.
- The producer and independent checker use separate implementations.
- JSON parsing rejects duplicate keys, floats, nonfinite constants, noncanonical
  bytes, and `bool`/`int` confusion.
- Normal and optimized-mode stdout must be byte-identical.
- The stress script exhausts a finite Gaussian alphabet and computes its census.
- The release checker locks sources, certificate bytes, proof files, and PDF bytes.
- Finite fixtures are `NUMERICAL_FINITE_ILLUSTRATION_ONLY`.
