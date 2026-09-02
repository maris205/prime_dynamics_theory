# TPC-337 computational protocol

1. Verify the TPC-336 code and certificate hashes and canonical JSON.
2. Rebuild the six source windows and four disjoint masks.
3. Construct the literal all-plus `Q=54`, exponent-1 matrix.
4. Apply each of the five predeclared bijections to every masked source.
5. Record class means, centered energies, pair covariance matrices, and
   eigenvalues; check identities with a relative `5e-6` guard.
6. Recompute the same quantities with reverse shell accumulation and an
   independent trial-factorisation source path.
7. Run semantic mutation stress and normal/optimized replay equality.

All conclusions are finite.  No byte-level floating-point equality is used as
an exact theorem; the rational anchor carries the symbolic identity.
