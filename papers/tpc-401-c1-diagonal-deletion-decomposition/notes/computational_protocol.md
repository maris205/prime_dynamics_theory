# Computational protocol

The producer uses exact `Fraction` arithmetic for the production sample and
the anchor boundary.  Six existing TPC-400 origins, `Q=8192`, `N=1024`,
`H=66`, the 872-prime shell, and five positions per origin are fixed before
execution.  The independent checker verifies the canonical JSON, the exact
counts, the reverse-order sample identity, and the anchor counterexample.
The stress checker mutates four contract fields.  No floating eigensolver is
used and no numerical certification is claimed.
