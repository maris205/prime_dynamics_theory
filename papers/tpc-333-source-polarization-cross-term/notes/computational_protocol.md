# TPC-333 computational protocol

1. Verify the normalized parent hashes and canonical parent certificate.
2. Recompute the six windows with 100-digit logarithm midpoint arithmetic and
   the inherited finite Euler-tail enclosure.
3. Form `Lambda`, `b`, and `beta` arrays; evaluate four squared/cross terms.
4. Compute `kappa`, residual fraction, correlation, nonzero counts, and four
   nested-scale pair records.
5. Check the rational four-vector anchor and canonical JSON payload digest.
6. Replay using an independent trial sieve, reverse factorization, and reverse
   tail-product order.
7. Run five mutation tests and normal/optimized replay equality.

No dense matrix is used in TPC-333, so the experiment isolates the arithmetic
source layer rather than hiding it behind an operator computation.
