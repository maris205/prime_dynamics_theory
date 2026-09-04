# TPC-381 proof and audit package: c=1 origin-family replay

1. The affine grid, selected origins, `N=2048` count, eight-block partition,
   four sign laws, Q ladder, beta, exponent, height, caps, and c=1 mask are
   literal constants.  The producer constructs all 36 rows before computing
   the profile summary.
2. Exact integer endpoint inequalities certify disjointness from the largest
   declared TPC-376--380 windows.  This is finite disjointness only.
3. The normalization is one nonnegative square-energy sum shared by all laws.
   The q=8 anchor `[1400001,1400014)` independently checks positive rational
   geometry and symmetry for every law; it is fixed before metric readout.
4. Each row checks finite spectral, Schur, Frobenius, symmetry, eigenvector
   residual, norm, and band-plus-tail Rayleigh identities.
5. The producer locks TPC-380's source and canonical certificate.  The
   independent checker uses a direct sieve through 20000 and reverse shell
   order, reconstructing all rows without importing the producer.
6. The 25-mutation stress suite rejects altered selection, count, law, row,
   census, clue, and firewall fields.  Normal and optimized runs require
   empty stderr and identical summaries.  Local Bridge-B locks stable project
   artifacts and repeats the checks.

Every item above certifies a finite artifact.  No arithmetic gate or twin-prime
claim is promoted.
