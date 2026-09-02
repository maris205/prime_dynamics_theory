# TPC-339 computational protocol

1. Verify the TPC-338 producer and certificate locks.
2. Rebuild six matrices, four masks, and nine coordinate controls.
3. For every record compute source norm, response gain, support-restricted
   Frobenius gain, gap, and occupancy.
4. Check the bound with a relative `2e-10` guard and retain empty masks.
5. Recompute with the hash-locked TPC-338 reverse-shell engine.
6. Run semantic mutation stress, PDF diagnostics, and normal/optimized replay.

The envelope is sign-free and finite.  Its slack statistics are descriptive;
they are not asymptotic exponents.
