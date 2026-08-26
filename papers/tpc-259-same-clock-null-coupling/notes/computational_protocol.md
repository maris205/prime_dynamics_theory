# TPC-259 computational protocol

1. Reconstruct integral and nonintegral real clocks with exact `Fraction`
   arithmetic and verify all four source blocks cover the clock.
2. Verify Haar norms, disjoint supports, null weights, and the exponent identity
   `1/2+55/48=79/48`.
3. Use symbolic block sums to replay the source-backed `w` contraction and the
   exact rank-one/residual identity for real `w` and complex output vectors.
4. Run independent mutation tests against altered directions and inflated
   claims.
5. Run a stress family including zero-diagonal residual witnesses and both
   signs of the synthetic scale `lambda`.

Finite synthetic matrices are tagged `PROVED_EXACT_SYNTHETIC` or
`NUMERICAL_OBSERVATION`; none is evidence for a literal prime theorem.
