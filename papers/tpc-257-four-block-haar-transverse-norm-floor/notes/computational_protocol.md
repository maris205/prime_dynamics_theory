# TPC-257 computational protocol

All programs are deterministic and use exact `Fraction` arithmetic for the
structural checks.

1. Build 64 real clocks, half integral and half nonintegral.
2. Reconstruct the ordered rank interval and its four consecutive blocks.
3. Check positive block lengths, exact unit norms, all three pairwise inner
   products, zero-extension variation, and divisor endpoint discrepancies.
4. Check the rational logarithm vectors for the three limiting curvature
   pairs and the exponent identities `-67/400`, `5/6`, `55/48`, `7/6`, and
   `1/48`.
5. Independently evaluate two finite beta samples and label them
   `NUMERICAL_OBSERVATION`.
6. Run a second implementation without importing the producer.  It performs
   semantic equality checks and deterministic mutation rejection.
7. Run the 192-family integer/noninteger stress suite, including arbitrary
   balanced child splits and variation identities.

The finite prime-power and Möbius calculations are diagnostic only.  They are
never substituted for the PNT or for the exact TPC-255 source theorem.
