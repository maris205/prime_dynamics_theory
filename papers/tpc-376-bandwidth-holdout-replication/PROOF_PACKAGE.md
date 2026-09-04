# TPC-376 proof package

1. The physical finite object is the normalized all-plus matrix \(T\) on
   each of the nine frozen holdout rows.  The producer locks the TPC-375
   engine and parent certificate by LF-normalized SHA-256.
2. The candidate grid \(a_j=1010001+401j\), training indices
   \((0,20,40)\), and holdout indices \((5,15,30)\) are fixed independently
   of holdout response.  The protocol does not claim coordinate-disjoint
   intervals.
3. The row geometry is a finite sum of nonnegative rational squares and is
   positive on the exact rational anchor.  The band mask is fixed before
   metric evaluation.
4. Entrywise \(T=B_1+(T-B_1)\) and the selected-mode Rayleigh decomposition
   are exact finite identities.  Floating-point eigensystems are used only
   for the declared numerical certificate and are checked by residuals,
   symmetry, norm, and metric envelopes.
5. The producer reports six c=1 spectral-cap failures with Q-profile
   \((0,3,3)\), zero Schur failures, and the stated tail range.  The
   independent checker reconstructs the shell in reverse order without
   importing the producer and compares all principal metrics within its
   declared tolerance.
6. The strongest supported conclusion is a finite response-blind
   grid-index holdout replication of the TPC-375 Q-profile.  The result
   does not pay arithmetic \(L^2\), fixed-power, growing-uniformity, or
   Route-B gates.
