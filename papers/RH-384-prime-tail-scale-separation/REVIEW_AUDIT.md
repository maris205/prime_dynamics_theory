# RH-384 Reviewer Audit

## Editorial verdict

`ACCEPT WITH BOUNDARY LOCKS SATISFIED` for the standalone arithmetic paper. Route A is `GO`; Route B is `STOP_SCOPED`.

## Major mathematical checks

1. **Abel boundary and constant — PASS.** The manuscript displays the exact strict Stieltjes identity with boundary `-pi(p_y)/(p_y^2-1)^r`. The proof reduces to `p^(-2r)`, controls the reduction error, uses a tail supremum for the PNT error, and obtains `-1+2r/(2r-1)=1/(2r-1)`.
2. **Fixed-only quantifiers — PASS.** Every asymptotic is stated for fixed `r` or a fixed finite partition. No growing-degree uniformity is inferred from the finite grid.
3. **Scale separation — PASS.** Constants, `p_y` exponents, log exponents, and all quotient directions were independently reconstructed. In particular `T^3=o(S)` and `S=o(T^2)`.
4. **Inherited gap use — PASS.** The RH-382 expansion is identified as an immutable input. Each of the five limits follows with the correct remainder normalization.
5. **Exact subtraction — PASS.** L2 keeps exact `A*T`; L3–L5 keep exact `A*T+B*T^2`. Genuine mutations of both terms fail. No unstated effective PNT error is used.
6. **Endpoint nuance — PASS.** Strict/inclusive and current/successor changes are disclosed as exact-interface distinctions. The paper does not falsely claim different leading equivalents.
7. **Positive coefficient — PASS.** The interval is labeled as the numerator `Y-2m`, not as `C`. The Bonferroni tail inequality, integer cutoff, directed operations, sign-aware linear form, and outward quantization were reviewed.

## Artifact checks

- 8 fixed-r, 66 partition, 48 successor, 5 scale, 5 gap, 10 interval, and 20 mutation rows.
- Upper tail losses are rounded upward before the lower Bonferroni factor is formed.
- Hostile Decimal ambient precision, rounding, exponent bounds, underflow traps, and clamping traps do not change canonical bytes.
- The certificate fixture is 48,689 bytes with SHA-256 `01c91e57a01de9841f282327ab2f6e1a9368e136393ddab7a2cfe6b019a519c8`.
- 51 live inputs equal both declared SHA-256 values and their release blobs.
- Schema is recursively closed, passes the official Draft 2020-12 metaschema and instance validator, and rejects Boolean/integer aliases, added members, duplicate keys, and nonfinite constants.
- Optimized Python mode reproduces `51 True`.

## Reviewer objections resolved during construction

- Added the previously omitted `u_2`, `Y`, and `m` interval rows.
- Replaced placeholder source digests with release-blob hashes.
- Replaced sentinel provenance tests with real release/hash/DOI validation.
- Added exact algebraic reconstruction of scale and gap ledgers.
- Moved decimal quantum construction inside a fresh directed context.
- Added hostile exponent-range and trap testing.
- Corrected the lower-tail computation so the tail loss is rounded upward before subtraction.
- Added the exact `B*T_y^2` surrogate firewall at the `S_y` scale.
- Relabeled the numeric enclosure as `Y_infinity-2*m_infinity` rather than `C`.

## Remaining limitations

The result is qualitative in the PNT error and therefore gives no effective sign threshold. It does not control active phasewise correlations, growing clocks, growing partitions, or any spectral/RH gate. These are correctly stated limitations rather than revision defects.
