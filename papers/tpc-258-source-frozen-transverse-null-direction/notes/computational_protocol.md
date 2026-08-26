# TPC-258 computational protocol

All structural calculations use exact `Fraction` arithmetic or formal
logarithm labels.

1. Reconstruct 80 integral and 80 nonintegral real clocks.
2. Build TPC-257's four blocks and verify all three Haar norms, orthogonalities,
   and zero-extension variation identities.
3. Represent `log(3456/3125)` and `log(884736/823543)` by exact prime-factor
   vectors and verify the cross-product cancellation symbolically.
4. Check the normalized null vector numerically only as a diagnostic.
5. Replay the cancellation under swapped/sign-flipped/data-dependent mutation
   records and reject all altered candidates.
6. Evaluate a deterministic adversarial `1/sqrt(log x)` error model to verify
   the distinction between `o(1)` and fixed-power saving.

No finite sample is used as proof of the PNT or of the literal asymptotic.
