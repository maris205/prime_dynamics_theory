# TPC-336 computational protocol

1. Verify TPC-335 parent hashes and canonical certificate.
2. Rebuild six source windows and four disjoint support masks.
3. Construct the all-plus `Q=54`, exponent-1, height-66 matrix.
4. Compute each masked self response, diagonal, off-diagonal, gain, and the
   complete upper-triangular output Gram matrix.
5. Check the full response expansion and exact rational output anchor.
6. Replay with reverse shell accumulation and independent source arithmetic.
7. Run five mutation tests and normal/optimized equality.

The response identity is checked with an explicit finite floating-point guard;
no floating-point equality is labeled symbolic.
