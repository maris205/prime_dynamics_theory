# TPC-397 — fine-grid replication of the finite interpolation transition

Author: Liang Wang  \\
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

On a fifth coordinate-disjoint affine family, the finite origin-stability
signal persists through `lambda=11/12` but fails at the endpoint `lambda=1`:
12/16 declared cells pass the one-percent origin-spread rule, while every
endpoint-1 cell fails with spread between 4.34% and 4.86%.  All 16
parent-relative holdout comparisons and all 16 within-family transfers pass
the predeclared 3% cap, and no spectral or Schur row fails.  This is a
finite endpoint-localization replication, not a source-valid or asymptotic
theorem.

## What is new

TPC-396 sampled the transition coarsely at `lambda=0,1/3,2/3,1` on a fourth
family.  TPC-397 fills the remaining interval with three response-blind
coefficients and tests four exact finite matrix combinations

```text
M_lambda = (1-lambda) M_all_plus + lambda M_alternating_index
lambda in {3/4, 5/6, 11/12, 1}
```

The intermediate objects are explicitly modeling probes, not new `+/-1`
arithmetic laws.  TPC-396 endpoint means (its `blend_0` and `blend_1`
cells) are hash-locked and linearly interpolated as a response-blind parent
reference.

## Frozen protocol

```text
schema = TPC397_C1_SIGNED_LAW_INTERPOLATION_V1
parent = TPC-396 finite interpolation certificate (code and JSON hash locked)
candidate grid = a_j = 6400001 + 401 j, 0 <= j < 41
selected indices = 0,8,16,24,32,40
origins = 6400001,6403209,6406417,6409625,6412833,6416041
calibration origins = 6400001,6403209,6406417
holdout origins = 6409625,6412833,6416041
window count = N=1024 for every origin
block length = 128; band mode = fixed_c3; Q = 8192
kernel exponent = 1; beta = 2; height = 66
laws = blend_3_4, blend_5_6, blend_11_12, blend_1
lambda coefficients = 3/4, 5/6, 11/12, 1/1
normalizations = local_diagonal, pooled_train_scalar,
                 origin_scalar, frozen_train_1024_scalar
origin-spread cap = 0.01
parent calibration/holdout caps = 0.03; within-family transfer cap = 0.03
spectral cap = 0.64; Schur cap = 0.83
```

The certificate is the complete 6-origin x 4-law x 4-normalization panel:
96 rows and 16 cells.  Selection, cohort roles, interpolation coefficients,
and caps are fixed before current readout.

## Finite findings

```text
origin-stable cells by normalization:
  local_diagonal             3/4
  pooled_train_scalar        3/4
  origin_scalar              3/4
  frozen_train_1024_scalar   3/4
total origin-stable cells = 12/16
law-level result = blend_3_4, blend_5_6, blend_11_12 pass all 4 normalizations;
                   blend_1 passes 0/4
parent calibration passes = 4/4 for every normalization
parent holdout passes = 4/4 for every normalization
within-family transfer passes = 4/4 for every normalization
spectral failures = 0/96; Schur failures = 0/96
```

The maximum all-origin relative spreads by normalization are
`0.048556752880022216`, `0.043399597037557539`,
`0.043414746028399794`, and `0.043399597037557580` in local, pooled, origin,
and frozen order.  These maxima occur at `blend_1`.  The largest parent-
relative calibration error is `0.017838648302480165`, the largest holdout
error is `0.024669590049843704`, and the largest within-family transfer error
is `0.019666773775763424`; all remain below the fixed 3% cap.

At the rational anchor `[6400001,6400014)` with shell `{11,13}`, all four
interpolation identities are exact and all four matrices are symmetric with
positive geometry.  The numerical float64 panel uses the same identity and
records zero construction residual up to machine representation.

## Interpretation and obstruction

The strongest positive result is a finite phase localization: all three
interior samples `lambda=3/4,5/6,11/12` retain the stable origin behavior
under every declared normalization, while all parent-relative holdout and
within-family transfer cells stay below 3%.  The strongest obstruction is the
endpoint `lambda=1`, where every normalization loses origin stability.  Thus
the endpoint-localized behavior replicates on a fifth family, but this does
not establish a universal threshold or an analytic source law.

## Certification and claim firewall

The producer sums the prime shell in ascending order.  The independent checker
rebuilds it in descending order without importing producer functions.  It
recomputes all 96 rows, parent-interpolated errors, cohort statistics, and
counters.  A 28-case mutation suite rejects altered certificate contracts.
Normal and optimized runs are required to agree, and Bridge-B locks every
release artifact.

```text
TPC397_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC397_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC397_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC397_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY
TPC397_INTERPOLATION_PANEL = NUMERICALLY CERTIFIED FINITE_96_ROWS
TPC397_ORIGIN_PHASE = NUMERICALLY CERTIFIED FINITE_SCOPED
TPC397_PARENT_INTERPOLATED_TRANSFER = NUMERICALLY CERTIFIED FINITE_SCOPED
TPC397_SPECTRAL_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
TPC397_SCHUR_ENVELOPE = NUMERICALLY CERTIFIED FINITE SCOPED ONLY
TPC397_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC397_GROWING_OPERATOR_BOUND = OPEN
TPC397_SOURCE_UNIFORM_L2 = OPEN
TPC397_ARITHMETIC_ADVANCE = NO
TPC397_FIXED_POWER_CREDIT = 0
TPC397_FULL_GATE_B = OPEN
TPC397_TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are absent from this checkout.  Local
proof/checker/Bridge-B evidence is fail-closed finite consistency evidence;
Route-A is not officially evaluated and Route-B remains open.  Nothing here
proves source-valid origin uniformity, arithmetic `L2`, a growing operator
bound, or a twin-prime result.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-397-c1-interpolation-transition-replication/code/tpc397_c1_interpolation_transition_replication.py --check
python -O -B papers/tpc-397-c1-interpolation-transition-replication/code/tpc397_c1_interpolation_transition_replication.py --check
python -B papers/tpc-397-c1-interpolation-transition-replication/experiments/tpc397_independent_checker.py --check
python -O -B papers/tpc-397-c1-interpolation-transition-replication/experiments/tpc397_independent_checker.py --check
python -B papers/tpc-397-c1-interpolation-transition-replication/experiments/tpc397_adversarial_certificate_stress.py --check
python -O -B papers/tpc-397-c1-interpolation-transition-replication/experiments/tpc397_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc397_c1_interpolation_transition_replication_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc397_c1_interpolation_transition_replication_checker.py --check
```

The required release PDF is `paper/paper.pdf`, byte-identical to
`paper/main.pdf`.
