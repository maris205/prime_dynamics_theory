# TPC-297 computational protocol

1. Lock the frozen TPC-295 producer/result and TPC-268 engine by normalized
   SHA-256.
2. Build the four exact rational source profiles at cutoffs `3,5,7,11`.
3. Rebuild each physical column in target-first order and form `V=A^T U`.
4. Check the profile-image rank modulo `1000000007` and `998244353`.
5. Use 70 decimal digits and QR least squares for the three target families.
6. Store conservative decimal enclosures for singular values and residuals.
7. Repeat all rows in a source-first independent checker.
8. Run exact synthetic stress tests for projection, nesting, and rank.
9. Require normal and optimized invocations to have empty stderr and equal
   stdout through the Bridge-B checker.

The cutoff family and residual thresholds are finite modeling choices.  No
power saving is charged.
