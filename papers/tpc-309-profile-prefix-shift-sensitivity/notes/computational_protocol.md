# TPC-309 computational protocol

1. Lock the TPC-308 producer and canonical certificate by normalized SHA-256.
2. Reconstruct the TPC-302 literal source rows and binary labels through the
   parent chain.
3. Build LOW, BASE, and HIGH profile matrices from the same literal-beta
   formula, using float64 physical rows and a 70-digit decimal frontier solve.
4. For each of 18 `(Q transition, exponent, tau)` cells, fit both aligned
   overlap targets at the first common feasible prefix for that ladder.
5. Recompute the profile-dependent right/left source-budget interval and also
   retain the TPC-308 budget class as an isolation control.
6. Enumerate every exclusive completion within Hamming radii 0, 1, and 2.
7. Store padded relative-`1e-5` decimal enclosures and canonical JSON.
8. Rebuild all rows and fits in a standalone NumPy checker; use relative
   `2e-3` replay slack only for cross-implementation floating-point checks.

The physical replay is not directed-rounded.  The result is consequently a
finite numerical reproduction and sensitivity observation, not a formal
interval or asymptotic certificate.
