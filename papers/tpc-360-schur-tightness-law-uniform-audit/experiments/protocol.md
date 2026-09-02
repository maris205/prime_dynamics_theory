# TPC-360 frozen protocol

1. Inherit exactly the three TPC-359 origins `(267175,261267,269074)`.
2. Use counts `256,512`, `Q=24,54,80`, exponents `1,2`, and the four fixed
   laws `all_plus`, `alternating_index`, `mod4_character`, `half_split`.
3. For every one of the 144 rows compute normalized Schur row sum, Frobenius
   norm, extreme eigenvalue norm, and the two ratios spectral/Schur and
   spectral/Frobenius.
4. Compare the four laws within each of the 36 `(origin,count,Q,exponent)`
   settings; do not select a law based on a response.
5. Lock the finite inequalities and rational anchor, run reverse-shell replay,
   14 mutation tests, and normal/optimized Bridge-B.

All conclusions are finite and scoped; no source response is used.
