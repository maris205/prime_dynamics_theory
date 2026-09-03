# TPC-361 frozen protocol

1. Candidate origins are exactly `310001+233j`, `0<=j<=50`.
2. At pilot count 256, compute only the unsigned mask-energy geometry for
   `(Q,s) in {24,54,80} x {1,2}`.  Score a candidate by the largest of the
   six `max(G)/min(G)` spreads.
3. Sort by decreasing score and origin, then greedily retain candidates whose
   distance from every retained origin is at least 1536.  Stop at three
   origins and require `(313030,311166,321651)` in that selection order.
4. After selection, replay counts `256,512,1024,2048`, shell anchors
   `Q=24,54,80`, exponents `1,2`, and laws `all_plus`, `alternating_index`,
   `mod4_character`, and `half_split`.
5. Record Schur and Frobenius envelopes for all `3*4*3*2*4=288` law rows.
   Record true spectra for all four laws at counts 256 and 512, and for
   all-plus at counts 1024 and 2048, giving 180 spectral rows.
6. Audit setting-wise law winners on the 36 short-count settings and classify
   the 54 adjacent all-plus spectral transitions with guard `1e-6`.
7. Include the rational `Q=4`, exponent-1 anchor on
   `[313060,313073]`, run the independent reverse-shell checker and the
   15-mutation stress test, compile the PDF, and run the local Bridge-B
   checker in normal and optimized modes.

The selection is response-blind and sign-blind.  Every conclusion is finite
and scoped to this declared protocol.  The missing Session-named official
Route-A/Route-B evaluator files keep the official gate status open.
