# TPC-394 — c=1 origin-uniformity ladder

Author: Liang Wang  \\
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

On a fresh, response-blind eight-origin finite `c=1` proxy ladder with a
common `N=1024` window, all four declared normalizations are origin-stable
for the all-plus control (relative spread below `4.4e-5`), while every
normalization is origin-unstable for the alternating-index law (relative
spread `0.084824884787110394` to `0.092863374514779065`).  The result is a
finite law-dependent obstruction/replication, not an origin-uniform or
arithmetic theorem.

## What is new

TPC-393 left `TEST_C1_ORIGIN_UNIFORMITY_AFTER_REPLICATION` after a fresh
normalization holdout.  TPC-394 directly tests that clue with eight selected
origins from a new affine grid, five calibration origins and three holdout
origins, all at the same count.  The same-count design removes count-transfer
from the primary statistic.  The panel retains an all-plus control, an
alternating-index target, the fixed `Q=8192` shell, the fixed `c=3` band, and
the four previously declared normalization choices.

## Frozen protocol

```text
schema = TPC394_C1_ORIGIN_UNIFORMITY_LADDER_V1
candidate grid = a_j = 5000001 + 401 j, 0 <= j < 41
selected indices = 0,5,10,15,20,25,30,35
origins = 5000001,5002006,5004011,5006016,
          5008021,5010026,5012031,5014036
calibration origins = first five; holdout origins = last three
window count = N=1024 for every origin
block length = 128; band mode = fixed_c3
Q = 8192; kernel exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index
normalizations = local_diagonal, pooled_train_scalar,
                 origin_scalar, frozen_train_1024_scalar
origin-spread cap = 0.01; holdout-transfer cap = 0.03
spectral cap = 0.64; Schur cap = 0.83
```

The certificate has 64 rows and 8 law/normalization cells.  Each cell has
eight origin values, with the first five used for calibration summaries and
the last three reserved as holdout summaries.  The roles, caps, and origins
were fixed before current responses were read.  TPC-393 is a hashed,
read-only parent interface; no parent response or fitted slope enters the
current statistic.

## Finite findings

```text
rows / cells = 64 / 8
all-origin stable cells = 4/8
all-plus cells = 4/4 stable; alternating-index cells = 0/4 stable
all-origin relative spreads:
  local_diagonal           0.084824884787110394 (alternating maximum)
  pooled_train_scalar      0.092862570673886716
  origin_scalar            0.092863374514779065
  frozen_train_1024_scalar 0.092862570673886591
calibration and holdout spread stable cells = 4/8 for each cohort
holdout-transfer passes = 2/2 for every normalization
spectral failures = 32/64 (all-plus rows only)
Schur failures = 0/64
```

The four all-plus relative spreads are `1.5006633030031748e-5`,
`4.3100829567952307e-5`, `2.2682851215503215e-5`, and
`4.3100829568062604e-5` in local/pooled/origin/frozen order.  The
alternating-index spread remains above eight percent under every
normalization.  The holdout means remain within the predeclared three-percent
calibration-transfer cap, so the obstruction is an origin spread at fixed
count, not a detected count extrapolation failure.  The alternating/all-plus
mean ratio is about `8.7e-4`, recording strong finite law cancellation; it is
not interpreted as an asymptotic cancellation theorem.

## Exact and independent certification

The producer accumulates the prime shell in ascending order.  The independent
checker rebuilds the matrices in descending order without importing the
producer, checks every row and aggregate, and allows only a small floating
summation tolerance.  A rational 13-point anchor at `[5000001,5000014)` with
`Q=8` proves positive geometry and exact symmetry for both laws.  The
25-case mutation suite rejects altered hashes, roles, row census, summary,
anchor, and claim-firewall fields.  Ordinary and optimized runs are required
to be byte-identical at the certificate/output layer.

## Claim firewall

```text
TPC394_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC394_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC394_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC394_ORIGIN_LADDER_PANEL = NUMERICALLY_CERTIFIED_FINITE_64_ROWS
TPC394_ORIGIN_UNIFORMITY_AUDIT = NUMERICALLY CERTIFIED FINITE SCOPED
TPC394_CALIBRATION_HOLDOUT_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED
TPC394_SPECTRAL_ENVELOPE = REFUTED_ON_DECLARED_FINITE_PANEL
TPC394_SCHUR_ENVELOPE = NUMERICALLY CERTIFIED FINITE SCOPED ONLY
TPC394_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC394_GROWING_OPERATOR_BOUND = OPEN
TPC394_SOURCE_UNIFORM_L2 = OPEN
TPC394_ARITHMETIC_ADVANCE = NO
TPC394_FIXED_POWER_CREDIT = 0
TPC394_FULL_GATE_B = OPEN
TPC394_TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are absent from this checkout.  The
local proof package, reverse-shell checker, mutation suite, and Bridge-B
checker are fail-closed repository evidence only; they cannot declare an
official Route-A or Route-B pass.  In particular, the finite origin split
does not establish source-valid origin uniformity, a growing operator bound,
arithmetic `L2`, or a twin-prime result.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-394-c1-origin-uniformity-ladder/code/tpc394_c1_origin_uniformity_ladder.py --check
python -O -B papers/tpc-394-c1-origin-uniformity-ladder/code/tpc394_c1_origin_uniformity_ladder.py --check
python -B papers/tpc-394-c1-origin-uniformity-ladder/experiments/tpc394_independent_checker.py --check
python -O -B papers/tpc-394-c1-origin-uniformity-ladder/experiments/tpc394_independent_checker.py --check
python -B papers/tpc-394-c1-origin-uniformity-ladder/experiments/tpc394_adversarial_certificate_stress.py --check
python -O -B papers/tpc-394-c1-origin-uniformity-ladder/experiments/tpc394_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc394_c1_origin_uniformity_ladder_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc394_c1_origin_uniformity_ladder_checker.py --check
```

The required release PDF is `paper/paper.pdf`; it must be byte-identical to
`paper/main.pdf`.
