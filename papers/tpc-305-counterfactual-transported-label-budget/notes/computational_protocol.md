# TPC-305 computational protocol

The producer locks normalized-LF SHA-256 digests of the TPC-302/TPC-303
producer and certificate files.  It extracts only the eight fixed source-first
rows with `(N,H,z)=(512,58,5)` and `Q=(50,60,70,90)`.  For each adjacent pair,
exponent, and tolerance it constructs both transported full-shell targets from
the exact integer overlap inner product.

The physical image matrices and source profile Gram matrix are rational before
conversion to 55-digit `mpmath`.  For each target the first feasible prefix is
found by least squares; both budgets are then solved on the maximum of the two
prefixes by the TPC-302 ridge/KKT frontier.  A relative enclosure of `1e-11`
is stored around each value.  Ratios are classified only when their enclosure
lies strictly on one side of one.  The three normalizers are
`||beta||^2`, the prefix profile-trace mean, and the first profile norm.

The certificate is canonical sorted-key JSON with a payload hash.  The
independent checker does not import the TPC-305 producer: it reconstructs the
parent labels, alignment signs, transported vectors, parent case census, and
checks all stored interval/order logic.  A stress suite exercises binary
transport, negative alignment, off-overlap copying, interval classifications,
and orientation truth tables.
