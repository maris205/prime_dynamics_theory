# TPC-340 computational protocol

1. Verify the TPC-339 producer and certificate hashes.
2. Rebuild six matrices, their absolute row sums, column energies, masks, and
   nine controls.
3. Compute the Frobenius, Schur, and hybrid gains for all 216 records.
4. Check every hybrid gap with a relative `3e-10` guard and classify the
   active branch.
5. Recompute with the hash-locked TPC-339 reverse-shell engine.
6. Run mutation stress, PDF diagnostics, and normal/optimized replay.

All norm statements are finite and sign-free.
