# TPC-290 computational protocol

The frozen TPC-289 grid is replayed exactly: 18 rows, the same source
vectors, and the same deleted-diagonal prime components.  Gram entries and
all ratios use `Fraction`; decimal strings are presentation only.

Each row is checked under `uniform`, `inverse_diagonal`, and `linear_taper`
weights.  Every equal two-prime support and every leave-one-out uniform
support is also evaluated.  The producer, reverse-order independent replay,
and ten-case mutation audit must agree; normal and optimized Python runs must
have byte-identical stdout.
