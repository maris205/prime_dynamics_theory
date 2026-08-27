# TPC-285 computational protocol

The producer locks the TPC-284 code/result and the frozen TPC-268 engine.
For each of 20 registered prime/exponent rows it verifies every entry of the
centered factorization, enumerates all nonzero residue classes, records class
sizes, and evaluates the exact determinant-factor inequality with rational
arithmetic.

For rank witnesses, `(q-1)B_q`, `(q-1)D_q`, and the rational kernel-Schur
matrix are reduced modulo `p=1000000007`.  Every kernel denominator is checked
nonzero modulo `p`.  Gaussian elimination is performed without assertions,
so ordinary and optimized Python run the same fail-closed logic.

The independent checker does not import the producer and reconstructs the
entry identities and all three ranks.  The stress audit mutates the theorem,
centered/deleted/kernel ranks, provenance, budget, and row census.
