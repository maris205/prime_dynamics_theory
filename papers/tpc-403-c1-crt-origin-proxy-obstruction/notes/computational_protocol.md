# Computational protocol

The producer uses exact `Fraction` arithmetic and an integer CRT solver.  It
uses the first eight primes in the fixed `Q=8192` shell and tests `m=1,2,3,4`.
For each case it checks the CRT residues, origin bound, positive/negative
mask pattern, direct masked signed coefficient, reduced coefficient, and the
exact identity `direct=reduced=T_1 P_-`.  The independent checker repeats the
same cases with reversed CRT summation and reversed shell coefficient order.
The stress checker validates the contract after three response-blind
mutations.  No floating point or numerical eigensolver is used.
