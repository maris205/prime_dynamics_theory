# TPC-296 computational protocol

1. Lock TPC-295 producer/result and the frozen TPC-268 engine by normalized
   SHA-256.
2. Reconstruct the 18 physical shell matrices from exact rational entries.
3. Use 70 decimal digits to compute Gram eigenvalues and three least-norm
   target solves per row.
4. Require correlation and norm-identity residuals below `1e-45`.
5. Store conservative decimal enclosures for every cost, energy, condition,
   trade product, and one-ray residual.
6. Recompute every row source-first in an independent checker that does not
   import the producer.
7. Run exact rational stress fixtures for full-rank, singular, budget,
   source-energy, and profile-projection identities.
8. Require normal/optimized invocations to have empty stderr and identical
   stdout.

The two source-control cutoff triples are allowed to coincide because the
frozen physical column construction uses the same rational `beta`; this is a
modeling boundary, not evidence of cutoff-uniform arithmetic control.
