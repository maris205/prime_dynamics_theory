# TPC-377 proof and audit package

1. The count ladder, origins, Q anchors, signs, beta, exponent, block
   length, and c=1 mask are literal constants in the producer and checker.
2. The full-window square-energy diagonal is positive because it is a
   finite sum of nonnegative rational squares; the exact anchor checks this
   with rational arithmetic.
3. The three windows at each origin are nested prefixes, so the scale
   relation is proved exactly at the protocol level.
4. The band/tail decomposition is an entrywise finite mask identity.
5. The selected full eigenvector gives the exact finite Rayleigh
   decomposition; residual, norm, symmetry, and Schur/Frobenius envelopes
   are checked numerically.
6. A reverse-shell independent replay and mutation stress test certify only
   the declared 27-row finite certificate. No arithmetic or asymptotic
   gate is promoted.
