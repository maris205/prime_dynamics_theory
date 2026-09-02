# TPC-355 — Position-aware mask-energy normalization

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-355 introduces a response-independent position-aware diagonal congruence
for the literal masked shell operator.  On three frozen panels (`648` rows),
it reduces the TPC-353-to-TPC-354 all-plus minimum-floor drop by the finite
amount `0.042151146184724153 -> 0.026236988152766205`, a reduction fraction of
`0.37754982894688971`.  The effect is only partial: the all-plus mean drop
increases, and a fresh mod-4 row remains negatively aligned after
normalization.

## Finite object

For the unsigned prime component `B_p`, define

```text
G_u = sum_(p in S_Q) sum_(t in I) B_p(u,t)^2,
A#  = D_G^(-1/2) A D_G^(-1/2),  D_G=diag(G_u).
```

The geometry diagonal uses the interval, shell, endpoint masks, kernel and
centered congruence only.  It does not use `Lambda`, `b`, `beta`, a sign law,
or a response.  Finite positivity and the polarization/Cauchy identities are
proved in `PROOF_PACKAGE.md`.

## Frozen audit protocol

The low parent is TPC-353 origins `6001,8001,10001`; the higher parent is
TPC-354 origins `21001,23001,25001`; the fresh holdout is
`29001,33001,37001`.  All three use counts `256,512,1024`, shell anchors
`Q=24,54,80`, exponents `1,2`, `H=66`, source cutoff `50000`, and the four
predeclared laws `all_plus`, `alternating_index`, `mod4_character`, and
`half_split`.

The canonical certificate reports:

```text
raw rows = 648; positive/negative/unresolved = 647/1/0
normalized rows = 648; positive/negative/unresolved = 647/1/0
all-plus raw minima (low/higher/fresh) =
  0.69291151430780062 / 0.65076036812307647 / 0.65445758459868297
all-plus normalized minima (low/higher/fresh) =
  0.69097110464200440 / 0.66473411648923819 / 0.66413980630867930
raw higher-panel minimum drop = 0.042151146184724153
normalized higher-panel minimum drop = 0.026236988152766205
finite drop-reduction fraction = 0.37754982894688971
```

The normalized all-plus mean drop is `0.024839744603963321`, larger than the
raw mean drop `0.021249745559872912`; this is recorded as
`REFUTED_SCOPED` mean repair.  The fresh mod-4 minimum is
`-0.0041082466600667307`, so universal positive alignment is also not claimed.

## Claim firewall

```text
TPC355_GEOMETRY_DEFINITION = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC355_DIAGONAL_CONGRUENCE = PROVED_EXACT_FINITE
TPC355_OPERATOR_POLARIZATION = PROVED_EXACT_FINITE
TPC355_PANEL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_648_ROWS
TPC355_RAW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_648_ROWS
TPC355_NORMALIZED_REPLAY = NUMERICALLY_CERTIFIED_FINITE_648_ROWS
TPC355_ALL_PLUS_FLOOR_REPAIR = NUMERICALLY_CERTIFIED_FINITE_PARTIAL
TPC355_ALL_PLUS_MEAN_REPAIR = REFUTED_SCOPED
TPC355_ALL_LAW_POSITIVE_ALIGNMENT = REFUTED_SCOPED
TPC355_SOURCE_UNIFORM_L2 = OPEN
TPC355_MASKED_OPERATOR_BOUND = OPEN
TPC355_ARITHMETIC_ADVANCE = NO
TPC355_FIXED_POWER_CREDIT = 0
TPC355_FULL_GATE_B = OPEN
TPC355_TWIN_PRIME_RESULT = NONE
```

The Session-named official evaluator files are absent from this checkout.
Local Bridge-B is therefore fail-closed fallback evidence, not an official
Route-A or Route-B pass.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-355-position-aware-mask-energy-normalization/code/tpc355_position_aware_mask_energy_normalization.py --write
python -B papers/tpc-355-position-aware-mask-energy-normalization/code/tpc355_position_aware_mask_energy_normalization.py --check
python -O -B papers/tpc-355-position-aware-mask-energy-normalization/code/tpc355_position_aware_mask_energy_normalization.py --check
python -B papers/tpc-355-position-aware-mask-energy-normalization/experiments/tpc355_independent_checker.py --check
python -O -B papers/tpc-355-position-aware-mask-energy-normalization/experiments/tpc355_independent_checker.py --check
python -B papers/tpc-355-position-aware-mask-energy-normalization/experiments/tpc355_normalization_stress.py --check
python -O -B papers/tpc-355-position-aware-mask-energy-normalization/experiments/tpc355_normalization_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc355_position_aware_mask_energy_normalization_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc355_position_aware_mask_energy_normalization_checker.py --check
```

The complete auditable package is organized as `README.md`, `PAPER_PLAN.md`,
`DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `code/`, `experiments/`,
`results/`, `notes/`, and `paper/`; the final manuscript is
`paper/paper.pdf`.
