# TPC-379 proof and audit package

1. The affine grid, selected indices, three origins, count, block partition,
   four laws, beta, exponent, height, Q anchors, caps, and c=1 mask are
   literal constants in the producer and independent checker.  The complete
   panel is constructed before the law profile is read.
2. Current intervals and all declared prior largest intervals are separated by
   exact integer endpoint inequalities.  This proves only finite coordinate
   disjointness.
3. The common normalization is a finite sum of nonnegative rational squares;
   the q=8 exact anchor checks positivity and symmetry for every law.
4. Each law uses the same entrywise band/tail mask.  Full eigensystems,
   residuals, norms, Schur/Frobenius/spectral envelopes, and the band-plus-tail
   Rayleigh identity are checked for every row.
5. The producer locks TPC-378's code and canonical certificate.  A separate
   direct-sieve reverse-shell checker rebuilds all 36 law rows without
   importing the TPC-379 producer.  A 25-mutation stress suite rejects altered
   selection, law, result, and firewall documents.
6. Normal and optimized runs must return zero, write no stderr, and emit
   byte-identical summaries.  These checks certify the finite artifact only;
   they do not promote a Route-A or Route-B arithmetic gate.
