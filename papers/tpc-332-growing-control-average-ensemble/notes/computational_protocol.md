# TPC-332 computational protocol

1. Verify the hash-locked TPC-331 producer and certificate.
2. Freeze origins `42001,44001`, scales `2048,4096,8192`, four laws, five
   controls, and the `50000` source cutoff.
3. Rebuild each source vector and literal deleted-diagonal shell matrix.
4. Form the five placed vectors, their mean, and centered residuals.
5. Compute energy, coordinate diagonal, and off-diagonal values separately
   for mean and centered components; never average ratios.
6. Recompute source polarization terms and the four adjacent scale pairs.
7. Apply the outward ratio guard `5e-8`; reject unresolved rows.
8. Replay in reverse shell order with an independent factorization path.
9. Run exact-anchor, canonical-JSON, mutation-stress, and normal/optimized
   Bridge-B checks.

The largest source polarization replay error is
`1.4551915228366852e-11`.  The exact small anchor, not floating-point
roundoff, carries the algebraic identity evidence.
