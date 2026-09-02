# TPC-354 — Higher-origin holdout for masked `L2` polarization

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-354 tests whether the TPC-353 source-native operator polarization transfers
to higher origins.  It attaches the same finite V59 residual
`beta(t)=Lambda(t+2)-b^(2)(t)` directly to the literal two-endpoint
divisibility-masked prime-shell operator.  The exact finite identity

```text
||A beta||_2^2 = ||A Lambda||_2^2 + ||A b||_2^2
               - 2 <A Lambda,A b>
```

is replayed on `216` rows with the TPC-353 counts `256,512,1024`, shell anchors
`Q=24,54,80`, two kernel exponents, and four predeclared sign laws, but with
the origins moved to `21001,23001,25001`.  All `216/216` operator images have
positive output alignment.  For `all_plus`, the normalized output coefficient
`kappa_A` is `0.65076036812307647--0.99135023146539858` (mean
`0.87436211602135017`), while the residual output fraction is
`0.0086497685346015422--0.34923963187692358`.  The source-level coefficient
on the holdout windows is `0.36357606682978283--0.38648419369238701`.

The other laws remain positive on this finite holdout, with output coefficient
ranges `0.00773141--0.669776`, `0.0219470--0.713036`, and
`0.0393483--0.656130` for `alternating_index`, `mod4_character`, and
`half_split`, respectively.  Against the hash-locked TPC-353 parent, the
all-plus minimum changes by `-0.042151146184724153` and the mean by
`-0.021249745559872912`.  Positive transfer therefore survives, but the floor
does not transfer uniformly.

This is a finite higher-origin transfer audit and a scoped floor-stability
obstruction.  It proves no growing bound, power saving, Route-B reassembly, or
twin-prime theorem.

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

An exact rational fourteen-point anchor at `[21001,21014]`, shell `{5,7}`,
checks the identity independently.  The certificate also records the
origins-only comparison with TPC-353 for every law's minimum, mean, and maximum.

## Claim firewall

```text
TPC354_FINITE_OPERATOR_POLARIZATION = PROVED_EXACT_FINITE
TPC354_FINITE_CAUCHY_ENVELOPE = PROVED_EXACT_FINITE
TPC354_SOURCE_NATIVE_MODEL = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC354_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
TPC354_POSITIVE_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_216_OF_216
TPC354_HIGHER_ORIGIN_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
TPC354_OUTPUT_SOURCE_MISMATCH = NUMERICALLY_CERTIFIED_FINITE
TPC354_ALL_PLUS_FLOOR_TRANSFER = REFUTED_SCOPED
TPC354_UNIFORM_L2 = OPEN
TPC354_MASKED_OPERATOR_BOUND = OPEN
TPC354_ARITHMETIC_ADVANCE = NO
TPC354_FIXED_POWER_CREDIT = 0
TPC354_FULL_GATE_B = OPEN
TPC354_TWIN_PRIME_RESULT = NONE
TPC354_ROUND2_CLUE = TEST_POSITION_AWARE_MASKED_BOUND_ORIGIN_SCALE_NORMALIZATION_OR_CONTROLLED_SIGN_LAW_SUBSPACE
```

The Session-named evaluator files are absent from this checkout.  The local
Bridge-B result is fail-closed fallback evidence, not an official Route-A or
Route-B pass.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-354-higher-origin-masked-l2-holdout/code/tpc354_higher_origin_masked_l2_holdout.py --write
python -B papers/tpc-354-higher-origin-masked-l2-holdout/code/tpc354_higher_origin_masked_l2_holdout.py --check
python -O -B papers/tpc-354-higher-origin-masked-l2-holdout/code/tpc354_higher_origin_masked_l2_holdout.py --check
python -B papers/tpc-354-higher-origin-masked-l2-holdout/experiments/tpc354_independent_checker.py --check
python -O -B papers/tpc-354-higher-origin-masked-l2-holdout/experiments/tpc354_independent_checker.py --check
python -B papers/tpc-354-higher-origin-masked-l2-holdout/experiments/tpc354_holdout_stress.py --check
python -O -B papers/tpc-354-higher-origin-masked-l2-holdout/experiments/tpc354_holdout_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc354_higher_origin_masked_l2_holdout_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc354_higher_origin_masked_l2_holdout_checker.py --check
```

The canonical certificate is `results/tpc354_certificate.json`; the compiled
manuscript is `paper/paper.pdf`.  The complete auditable package consists of
`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/`.
