# TPC-396 — finite signed-law interpolation on a fresh c=1 family

Author: Liang Wang  \\
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

On a fourth coordinate-disjoint affine family, the finite origin-stability
signal persists for the three interpolants `lambda=0,1/3,2/3` but not at the
alternating endpoint `lambda=1`: 12/16 declared cells pass the one-percent
origin-spread rule, while every endpoint-1 cell fails with spread about 8.94%
to 9.41%.  The parent-relative holdout comparison passes in all 16 cells;
three scalar-normalized endpoint transfer cells narrowly exceed the predeclared
3% within-family cap.  This locates a finite transition obstruction; it is not
a source-valid or asymptotic theorem.

## What is new

TPC-395 showed that the all-plus/alternating split survives a third family.
TPC-396 tests the most economical mechanism probe: form four exact finite
matrix combinations

```text
M_lambda = (1-lambda) M_all_plus + lambda M_alternating_index
lambda in {0, 1/3, 2/3, 1}
```

The intermediate objects are explicitly modeling probes, not new `+/-1`
arithmetic laws.  TPC-395 endpoint means are hash-locked and linearly
interpolated as a response-blind parent reference.

## Frozen protocol

```text
schema = TPC396_C1_SIGNED_LAW_INTERPOLATION_V1
parent = TPC-395 finite cross-family certificate (code and JSON hash locked)
candidate grid = a_j = 6000001 + 401 j, 0 <= j < 41
selected indices = 0,8,16,24,32,40
origins = 6000001,6003209,6006417,6009625,6012833,6016041
calibration origins = 6000001,6003209,6006417
holdout origins = 6009625,6012833,6016041
window count = N=1024 for every origin
block length = 128; band mode = fixed_c3; Q = 8192
kernel exponent = 1; beta = 2; height = 66
laws = blend_0, blend_1_3, blend_2_3, blend_1
lambda coefficients = 0/1, 1/3, 2/3, 1/1
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
law-level result = blend_0, blend_1_3, blend_2_3 pass all 4 normalizations;
                   blend_1 passes 0/4
parent calibration passes = local 4/4; pooled/origin/frozen 3/4
parent holdout passes = 4/4 for every normalization
within-family transfer passes = local 4/4; pooled/origin/frozen 3/4
spectral failures = 24/96; Schur failures = 0/96
```

The maximum all-origin relative spreads by normalization are
`0.089422016482946329`, `0.094028626026475742`,
`0.094070438394687927`, and `0.094028626026475617` in local, pooled, origin,
and frozen order.  These maxima occur at `blend_1`.  The corresponding
`blend_1` scalar transfer errors are approximately `0.0307810`, `0.0307930`,
and `0.0307810`; they are retained as failures rather than repaired by
changing the cap.  The largest parent-relative holdout error over all cells is
`0.0033105775404086435`.

At the rational anchor `[6000001,6000014)` with shell `{11,13}`, all four
interpolation identities are exact and all four matrices are symmetric with
positive geometry.  The numerical float64 panel uses the same identity and
records zero construction residual up to machine representation.

## Interpretation and obstruction

The strongest positive result is a finite phase localization: the three
interior samples through `lambda=2/3` retain the stable origin behavior across
the declared normalizations, and all parent-relative holdout means remain
close.  The strongest obstruction is at the endpoint `lambda=1`, where every
normalization loses origin stability and three scalar transfer cells cross the
3% cap.  This supports only the scoped statement that the transition lies in
the tested endpoint behavior changes between `lambda=2/3` and `lambda=1`
for this finite family; the interior interval `(2/3,1)` remains untested.
No universal threshold or analytic source law is claimed.

## Certification and claim firewall

The producer sums the prime shell in ascending order.  The independent checker
rebuilds it in descending order without importing producer functions.  It
recomputes all 96 rows, parent-interpolated errors, cohort statistics, and
counters.  A 28-case mutation suite rejects altered certificate contracts.
Normal and optimized runs are required to agree, and Bridge-B locks every
release artifact.

```text
TPC396_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC396_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC396_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC396_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY
TPC396_INTERPOLATION_PANEL = NUMERICALLY CERTIFIED FINITE_96_ROWS
TPC396_ORIGIN_PHASE = NUMERICALLY CERTIFIED FINITE_SCOPED
TPC396_PARENT_INTERPOLATED_TRANSFER = NUMERICALLY CERTIFIED FINITE_SCOPED
TPC396_SPECTRAL_ENVELOPE = REFUTED_ON_DECLARED_FINITE_PANEL
TPC396_SCHUR_ENVELOPE = NUMERICALLY CERTIFIED FINITE SCOPED ONLY
TPC396_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC396_GROWING_OPERATOR_BOUND = OPEN
TPC396_SOURCE_UNIFORM_L2 = OPEN
TPC396_ARITHMETIC_ADVANCE = NO
TPC396_FIXED_POWER_CREDIT = 0
TPC396_FULL_GATE_B = OPEN
TPC396_TWIN_PRIME_RESULT = NONE
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
python -B papers/tpc-396-c1-signed-law-interpolation/code/tpc396_c1_signed_law_interpolation.py --check
python -O -B papers/tpc-396-c1-signed-law-interpolation/code/tpc396_c1_signed_law_interpolation.py --check
python -B papers/tpc-396-c1-signed-law-interpolation/experiments/tpc396_independent_checker.py --check
python -O -B papers/tpc-396-c1-signed-law-interpolation/experiments/tpc396_independent_checker.py --check
python -B papers/tpc-396-c1-signed-law-interpolation/experiments/tpc396_adversarial_certificate_stress.py --check
python -O -B papers/tpc-396-c1-signed-law-interpolation/experiments/tpc396_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc396_c1_signed_law_interpolation_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc396_c1_signed_law_interpolation_checker.py --check
```

The required release PDF is `paper/paper.pdf`, byte-identical to
`paper/main.pdf`.
