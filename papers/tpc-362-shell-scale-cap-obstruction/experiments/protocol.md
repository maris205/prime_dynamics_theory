# TPC-362 frozen protocol

1. Inherit exactly the TPC-361 ordered origin panel
   `(313030,311166,321651)`; no new origin selection is performed.
2. Use counts `256,512`, shell anchors
   `Q={12,24,36,54,80,128,256,512}`, exponents `s={1,2}`, and the four
   fixed laws `all_plus`, `alternating_index`, `mod4_character`, and
   `half_split`.
3. Record the literal shell, geometry range, normalized Schur row-sum,
   normalized Frobenius norm, and true spectral norm for every
   `3*2*8*2*4=384` law row.
4. Treat `0.83` (Schur) and `0.64` (spectral) as finite working caps inherited
   from the prior anchor range.  Report separately the low-shell set
   `{12,24,36,54,80}` and high-shell set `{128,256,512}`; do not infer a
   shell-uniform theorem from either set.
5. Compare the four laws at all 96 fixed settings and classify all 336 adjacent
   Q transitions using guard `1e-8`.
6. Include the rational `Q=4`, exponent-1 anchor on
   `[313060,313073]`; run the independent reverse-shell checker, the
   certificate mutation stress, PDF QA, and the local Bridge-B checker in
   normal and optimized modes.

The shell ladder is a finite diagnostic of the cap's missing Q-quantifier.
The high-Q failure is allowed and is recorded as `REFUTED_SCOPED`, not treated
as an arithmetic result.  The official Session-named evaluator files remain
absent, so official Route-A/Route-B status stays open.
