# Bridge B — TPC-322 operator-level signed projector/reassembly

TPC-322 keeps the literal deleted-diagonal centered prime-shell blocks from
TPC-321 and supplies the missing finite output-space typing.  The direct-sum
operator is projected onto a sign-labelled diagonal copy of the source space;
the resulting coherent operator retains all signed cross-block terms.

```text
TPC322_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_REASSEMBLY_ATLAS
TPC322_SIGNED_PROJECTOR_IDENTITY = PROVED_EXACT_FINITE
TPC322_OPERATOR_REASSEMBLY_ATLAS = NUMERICALLY_CERTIFIED_FINITE_24_ROWS
TPC322_MIN_SIGN_EXISTS = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
TPC322_MAX_SIGN_EXISTS = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
TPC322_ALL_PLUS_LAW = REFUTED_FINITE_PANEL
TPC322_ALTERNATING_LAW = REFUTED_FINITE_PANEL
TPC322_ARITHMETIC_ADVANCE = NO
TPC322_FIXED_POWER_CREDIT = 0
TPC322_FULL_GATE_B = OPEN
TPC322_TWIN_PRIME_RESULT = NONE
TPC322_STATUS = NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_REASSEMBLY_ATLAS
TPC322_ROUND2_CLUE = TEST_CANONICAL_SIGN_LAWS_AGAINST_OPERATOR_SPECTRAL_PROFILES_AND_SOURCE_NATIVE_ARITHMETIC_L2
```

## Finite evidence

The panel is `X={640,1280,2560}`, `Q={24,36,54,80}`, and `s={1,2}`.  The
producer and an independent reverse-order/einsum replay certify the same 24
row atlas.  Exhaustive sign search fixes one global sign and finds both
`rho<1` and `rho>1` in every row.  The all-plus law is below one on 3 rows and
above one on 21; index alternation is below one on 21 and above one on 3.
The outward finite ranges for the exhaustive extrema are
`[0.59905756561947343,0.98033069254228578]` and
`[1.0122088324409428,6.8711947177741193]`.

The exact projector identity proves that the actual projected fraction is
`phi=rho/m<=1`; an unnormalised coherent ratio above one is not a violation of
projection contraction.  The sign patterns are finite geometric probes, not
Möbius or von Mangoldt weights.

## Interpretation firewall

This is a local finite Route-B structural edge.  It does not supply a growing
signed reassembly theorem, source-native arithmetic `L2`, fixed-power credit,
the strict `1/400` payment, or a twin-prime conclusion.  The official
Session-named Route-A/Route-B evaluator files are absent from the checkout, so
the local checker is not an official evaluator pass.
