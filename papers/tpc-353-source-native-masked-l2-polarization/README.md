# TPC-353 — Source-native masked `L2` polarization

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-353 attaches the finite V59 residual
`beta(t)=Lambda(t+2)-b^(2)(t)` directly to the literal two-endpoint
divisibility-masked prime-shell operator.  The exact finite identity

```text
||A beta||_2^2 = ||A Lambda||_2^2 + ||A b||_2^2
               - 2 <A Lambda,A b>
```

is replayed on `216` rows: three origins `6001,8001,10001`, three source
counts `256,512,1024`, shell anchors `Q=24,54,80`, two kernel exponents, and
four predeclared sign laws.  All `216/216` operator images have positive
output alignment.  For `all_plus`, the normalized output coefficient
`kappa_A` is `0.69291151430780062--0.99626802812598902` (mean
`0.89561186158122308`), while the residual output fraction is only
`0.0037319718740109137--0.30708848569219932`.  The source-level coefficient
on the same windows is only `0.39570365481042707--0.43581376702257324`.

The other laws are less aligned: `alternating_index`, `mod4_character`, and
`half_split` have output coefficient ranges `0.0138671--0.711596`,
`0.00774850--0.739230`, and `0.0626056--0.733296`.  Thus the finite operator
changes the source polarization substantially; source-level cancellation
cannot be promoted silently to a uniform masked arithmetic `L2` estimate.

This is a finite source/operator attachment and an obstruction to a
source-only explanation.  It proves no growing bound, power saving, Route-B
reassembly, or twin-prime theorem.

## Exact finite layer

For any finite real matrix `A` and vectors `L,b`, the polarization identity and
the Cauchy envelope are exact:

```text
kappa_A = 2 <A L,A b>/(||A L||_2^2+||A b||_2^2)
R_A     = ||A(L-b)||_2^2/(||A L||_2^2+||A b||_2^2) = 1-kappa_A,
```

with

```text
(sqrt(E_L)-sqrt(E_b))^2/(E_L+E_b) <= R_A
  <= (sqrt(E_L)+sqrt(E_b))^2/(E_L+E_b).
```

An exact rational fourteen-point anchor at `[6001,6014]`, shell `{5,7}`,
checks the identity independently.

## Claim firewall

```text
TPC353_FINITE_OPERATOR_POLARIZATION = PROVED_EXACT_FINITE
TPC353_FINITE_CAUCHY_ENVELOPE = PROVED_EXACT_FINITE
TPC353_SOURCE_NATIVE_MODEL = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC353_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
TPC353_POSITIVE_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_216_OF_216
TPC353_OUTPUT_SOURCE_MISMATCH = NUMERICALLY_CERTIFIED_FINITE
TPC353_UNIFORM_L2 = OPEN
TPC353_MASKED_OPERATOR_BOUND = OPEN
TPC353_ARITHMETIC_ADVANCE = NO
TPC353_FIXED_POWER_CREDIT = 0
TPC353_FULL_GATE_B = OPEN
TPC353_TWIN_PRIME_RESULT = NONE
TPC353_ROUND2_CLUE = TEST_SOURCE_NATIVE_L2_CROSS_TERM_ON_DISJOINT_HIGHER_ORIGINS_OR_BUILD_POSITION_AWARE_MASKED_BOUND
```

The Session-named evaluator files are absent from this checkout.  The local
Bridge-B result is fail-closed fallback evidence, not an official Route-A or
Route-B pass.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-353-source-native-masked-l2-polarization/code/tpc353_source_native_masked_l2_polarization.py --write
python -B papers/tpc-353-source-native-masked-l2-polarization/code/tpc353_source_native_masked_l2_polarization.py --check
python -O -B papers/tpc-353-source-native-masked-l2-polarization/code/tpc353_source_native_masked_l2_polarization.py --check
python -B papers/tpc-353-source-native-masked-l2-polarization/experiments/tpc353_independent_checker.py --check
python -O -B papers/tpc-353-source-native-masked-l2-polarization/experiments/tpc353_independent_checker.py --check
python -B papers/tpc-353-source-native-masked-l2-polarization/experiments/tpc353_polarization_stress.py --check
python -O -B papers/tpc-353-source-native-masked-l2-polarization/experiments/tpc353_polarization_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc353_source_native_masked_l2_polarization_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc353_source_native_masked_l2_polarization_checker.py --check
```

The canonical certificate is `results/tpc353_certificate.json`; the compiled
manuscript is `paper/paper.pdf`.  The complete auditable package consists of
`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/`.
