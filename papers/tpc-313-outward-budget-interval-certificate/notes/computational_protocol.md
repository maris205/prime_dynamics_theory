# TPC-313 computational protocol

1. Lock the TPC-312 code/result hashes and the TPC-268 arithmetic-engine hash.
2. Rebuild `I={321,...,640}`, the four prime shells, and both kernel
   exponents over `Fraction`.
3. Build the 17-column literal profile matrix and its source Gram.
4. For the TPC-312 minimum label, scan prefixes until normalized residual
   square is at most `|b|^2/4`; retain all earlier strict failures.
5. Use the declared rational ridge seed on that common prefix for both the
   minimum target and the all-positive control.  Shrink by `999/1000` only if
   exact feasibility requires it.
6. Compute primal, dual, residual, and ratio values over `Q`.
7. Propagate each scalar through the outward `10^-36` grid.
8. Run the producer, independent exact replay, stress suite, and Bridge-B
   checker under normal and optimized Python modes.

No random seed, external data file, or floating-point result is an input to
the certificate.
