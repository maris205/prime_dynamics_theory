# TPC-295 computational protocol

The producer imports the hash-locked TPC-294 physical construction, forms
each exact rational shell Gram matrix, and computes rank/determinant over
`1000000007` and `998244353`.  Every denominator is checked invertible before
reduction.  It also solves the three target systems modulo each prime for the
TPC-294 minimum, max-cut, and all-positive labels; all residuals must be zero.

The independent checker imports only the frozen TPC-268 engine.  It accumulates
each physical column source-coordinate first, reads the hash-locked TPC-294
target labels, and independently reconstructs the modular matrices and
target solves.  It does not import the TPC-295 producer.

The stress test checks the linear-algebra implication on deterministic full
rank and singular rational matrices, verifies modular rank against exact
small-matrix rank, and checks the explicit witness identity over $\mathbb Q$.

Normal and optimized invocations must have empty standard error and
byte-identical standard output; bytecode generation is disabled.
