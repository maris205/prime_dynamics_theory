# Bridge B — TPC-330 multi-permutation response spectrum

TPC-330 is the finite continuation of TPC-329.  It keeps the same literal
deleted-diagonal centered prime-shell operator, the hash-locked V59
source-native residual, two held-out origins (`28001`, `36001`), two scales
(`4096`, `8192`), four shell anchors, two kernel exponents, and four sign laws.
The single affine placement null is replaced by five predeclared coordinate
bijections: identity, affine `(3i+11)`, affine `(5i+17)`, affine `(7i+29)`,
and reversal, all modulo the source count.

The canonical certificate has `32` rows and `640` law/control observations,
plus `64` inherited two-scale law pairings and all `10` pairwise-control
summaries.  Every control is bijective on source counts `2048` and `4096`, so
it preserves the source multiset and Euclidean `L2` norm exactly.  The finite
classification census (negative/positive) is:

```text
identity      all 31/1   alternating 25/7   mod4 32/0   half 32/0
affine 3,11   all  0/32  alternating 20/12  mod4 27/5   half 31/1
affine 5,17   all  0/32  alternating 30/2   mod4 32/0   half 28/4
affine 7,29   all  0/32  alternating 21/11  mod4 32/0   half 29/3
reversal      all 31/1   alternating 25/7   mod4 32/0   half 32/0
```

Thus all three nontrivial affine controls agree on a positive all-plus result
in `32/32` rows, while identity and reversal retain the actual `31/1`
census.  The all-plus control signatures are
`negative|positive|positive|positive|negative` on `31` rows and all-positive
on one row.  This is a finite position-response spectrum and a scoped
obstruction to source-multiset/L2-only and single-affine-accident explanations.

The exact rational anchor is `[36001,36016]`, `Q=4`, `s=1`, shell `{5,7}`:

```text
E = 306.7544239093389
D = 332.4445614235858
O = -25.69013751424689
```

The producer, independent reverse-order checker, stress suite, PDF audit, and
normal/optimized equality are required by this local fail-closed bridge.

    TPC330_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_MULTI_PERMUTATION_RESPONSE_SPECTRUM
    TPC330_EXACT_GRAM_DECOMPOSITION = PROVED_EXACT_FINITE
    TPC330_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC330_COMPONENT_CONTROLS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC330_MULTI_PERMUTATION_SPECTRUM = NUMERICALLY_CERTIFIED_FINITE_5_CONTROLS
    TPC330_AFFINE_ALL_PLUS_CONSENSUS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC330_SIGN_AT_SCALE_GROWTH = NUMERICALLY_CERTIFIED_FINITE
    TPC330_ARITHMETIC_ADVANCE = NO
    TPC330_FIXED_POWER_CREDIT = 0
    TPC330_GROWING_SOURCE_NATIVE_L2 = OPEN
    TPC330_FULL_GATE_B = OPEN
    TPC330_TWIN_PRIME_RESULT = NONE
    TPC330_STATUS = NUMERICALLY_CERTIFIED_FINITE_MULTI_PERMUTATION_RESPONSE_SPECTRUM
    TPC330_ROUND2_CLUE = DECOMPOSE_POSITION_RESPONSE_INTO_AFFINE_REVERSAL_AND_SOURCE_ALIGNED_COMPONENTS

The finite affine consensus does not supply a source-uniform arithmetic
estimate, strict `1/400` payment, official Route-A/Route-B evaluator pass, or
twin-prime conclusion.  The Session-named evaluator files are absent from
this checkout; this bridge is explicitly a local fallback control.
