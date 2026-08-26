# TPC-262 computational protocol

1. Recompute all `C_q` entries with exact `Fraction` arithmetic for
   `q=5,7,11,13`.
2. Check symmetry, idempotence, row sums, trace/rank proxy, and positivity by
   exact quadratic-form identities.
3. Build the weighted direct-sum Gram table and verify the DFT Parseval and
   mode-zero formulas for aligned, alternating, and mixed signs.
4. Run the independent checker without importing the producer and reject
   schema, prime-shell, matrix, witness, and firewall mutations.
5. Run a rational stress grid over odd primes and source coordinates.

These are finite algebra checks. They do not approximate the smooth V59
kernel or infer an asymptotic prime theorem.
