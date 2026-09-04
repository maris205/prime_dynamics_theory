# TPC-378 proof and audit package

1. The affine candidate grid, selected indices, origins, endpoint counts,
   signs, beta, exponent, height, Q anchors, and c=1 mask are literal
   constants in the producer and independent checker.  Selection is declared
   response-blind and the complete panel is built before metrics are read.
2. Current intervals and the inherited largest intervals are disjoint by
   exact integer endpoint inequalities.  This proves only the finite
   coordinate separation recorded in the protocol.
3. The full-window geometry is a finite sum of nonnegative rational squares;
   the exact anchor checks positivity and symmetry.
4. The c=1 band/tail decomposition is an entrywise finite mask identity.  For
   each computed extremal eigenvector, residual, norm, symmetry, and the
   band-plus-tail Rayleigh identity are checked numerically.
5. The producer locks TPC-377's code and canonical certificate.  A separate
   reverse-shell checker rebuilds the prime shell and all 18 eigensystems
   without importing the TPC-378 producer.  A 24-mutation stress suite rejects
   altered protocol, result, and firewall documents.
6. Normal and optimized runs must return zero, write no stderr, and emit
   byte-identical summaries.  These checks certify the finite artifact only;
   they do not promote an arithmetic or asymptotic gate.
