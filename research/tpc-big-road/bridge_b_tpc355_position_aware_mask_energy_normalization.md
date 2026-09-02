# Bridge-B fallback: TPC-355 position-aware mask-energy normalization

This is the local, fail-closed bridge record for TPC-355.  The Session-named
official `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` are absent from this checkout; this file and its
checker do not infer an official Route-A or Route-B verdict.

TPC-355 inserts a response-independent unsigned mask-energy diagonal between
the literal two-endpoint masked shell operator and the finite polarization
interface.  Three panels are audited: TPC-353 low origins
`6001,8001,10001`, TPC-354 higher origins `21001,23001,25001`, and a fresh
holdout `29001,33001,37001`.  Counts `256,512,1024`, shell anchors
`Q=24,54,80`, exponents `1,2`, height `H=66`, source cutoff `50000`, and the
four predeclared sign laws are frozen.

The geometry is

```text
B_p(u,t) = unsigned literal masked prime component
G_u      = sum_(p in S_Q) sum_(t in I) B_p(u,t)^2
A#       = D_G^(-1/2) A D_G^(-1/2),  D_G=diag(G_u).
```

The canonical certificate contains `648` rows, with raw and normalized
metrics.  Each family has `647` positive, `1` negative, and `0` unresolved
alignments.  The all-plus minimum drop from the TPC-353 panel to the TPC-354
panel decreases from `0.042151146184724153` (raw) to
`0.026236988152766205` (normalized), a finite descriptive reduction fraction
of `0.37754982894688971`.  The all-plus mean drop goes the other way,
`0.021249745559872912` raw versus `0.024839744603963321` normalized; this is
`REFUTED_SCOPED` mean repair.  The fresh normalized mod-4 minimum is
`-0.0041082466600667307`, so law-uniform positive alignment is also
`REFUTED_SCOPED`.

```text
TPC355_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_AUDIT
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
TPC355_ROUND2_CLUE = TEST_ADVERSARIAL_POSITION_NORMALIZATION_OR_LAW_INVARIANT_BOUND_ON_FRESH_ORIGINS
TPC355_STATUS = NUMERICALLY_CERTIFIED_FINITE_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_AUDIT
```

## Local verification

From the repository root, the checker requires explicit read-only mode:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-355-position-aware-mask-energy-normalization/code/tpc355_position_aware_mask_energy_normalization.py --check
python -O -B papers/tpc-355-position-aware-mask-energy-normalization/code/tpc355_position_aware_mask_energy_normalization.py --check
python -B papers/tpc-355-position-aware-mask-energy-normalization/experiments/tpc355_independent_checker.py --check
python -O -B papers/tpc-355-position-aware-mask-energy-normalization/experiments/tpc355_independent_checker.py --check
python -B papers/tpc-355-position-aware-mask-energy-normalization/experiments/tpc355_normalization_stress.py --check
python -O -B papers/tpc-355-position-aware-mask-energy-normalization/experiments/tpc355_normalization_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc355_position_aware_mask_energy_normalization_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc355_position_aware_mask_energy_normalization_checker.py --check
```

The local Bridge-B result is fallback evidence only.  It does not close the
source-uniform arithmetic `L2` gate, pay fixed-power credit, reassemble Route B,
or imply a twin-prime result.
