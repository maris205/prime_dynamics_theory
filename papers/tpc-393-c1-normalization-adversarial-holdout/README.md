# TPC-393 — Adversarial Holdout Audit of Scalar Normalization

Author: Liang Wang  \\
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

On a fresh coordinate-disjoint finite $c=1$ proxy panel chosen before
readout, the previously exposed high-$Q$ alternating-index/local-diagonal
separation does not disappear: all four declared normalizations pass the
calibration-to-holdout forecast cap in both predeclared laws, while the
alternating-index cells remain origin-unstable at the one-percent diagnostic
level.  The finite spectral cap fails in every cell, whereas the Schur cap
passes in every cell.  This is a targeted numerical audit, not an arithmetic
or twin-prime theorem.

## What is new

TPC-392 exposed a single high-$Q$ alternating-index/local-diagonal forecast
failure inside a larger phase diagram.  TPC-393 makes the smallest useful
adversarial follow-up: a new affine coordinate family, the same fixed band and
normalization definitions, only $Q=8192$, and only the all-plus control and
the alternating-index target.  The roles and panel were fixed before current
responses were read.  Thus the contribution is an independent finite
replication/obstruction audit rather than a reclassification of TPC-392.

## Frozen protocol

```text
schema = TPC393_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_V1
candidate grid = a_j = 4200001 + 401 j, 0 <= j < 41
selected indices = 0,10,20,30,40
origins = 4200001,4204011,4208021,4212031,4216041
calibration origins = 4200001,4204011,4208021
holdout origins = 4212031,4216041
calibration counts = 1024,1280
holdout count = 1536
block length = 128; band mode = fixed_c3
Q = 8192
kernel exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index
normalizations = local_diagonal, pooled_train_scalar,
                 origin_scalar, frozen_train_1024_scalar
forecast cap = 0.03; spectral cap = 0.64; Schur cap = 0.83
```

The certificate contains 64 rows and 8 normalization/law cells.  Each cell
has three calibration-origin observations at each of $N=1024,1280$, and two
terminal holdout observations at $N=1536$.  The TPC-392 parent is referenced
by exact normalized-LF hashes as a frozen provenance/interface record; its
response or slope is not used in the current fit.

## Finite findings

```text
rows / cells = 64 / 8
forecast passes = 2/2 in each normalization (8/8 total cells per normalization)
maximum forecast error by normalization:
  local_diagonal             0.01010300962072197
  pooled_train_scalar        0.0097142554430971195
  origin_scalar              0.011039357664235361
  frozen_train_1024_scalar   0.0097142554430980077
terminal mean ordering = frozen_train_1024_scalar > origin_scalar
                       > pooled_train_scalar > local_diagonal
terminal ratios to local diagonal:
  frozen 1.0369348998, origin 1.0222441465, pooled 1.0209043621
spectral failures by normalization = 8,8,8,8 (32/32 total)
Schur failures by normalization = 0,0,0,0
within-one-percent stable cells at N=1024,1280,1536 = 4/8,4/8,4/8
```

The forecast criterion therefore replicates across the fresh family: the
alternating-index/local-diagonal cell is no longer a forecast-cap failure,
but its origin spread remains above one percent at all three counts.  All
four all-plus cells are one-percent stable, while all four alternating cells
are not.  The scalar choices shift the terminal level by approximately
2.09%--3.69% relative to local diagonal, so the normalization effect remains
finite and measurable.  The universal spectral failure is a stronger
obstruction than the forecast comparison: this panel does not support a
spectral-envelope pass under the declared $0.64$ cap.  The universal Schur
pass is only a finite diagnostic and is not a growing operator bound.

## Exact and independent certification

The producer uses ascending prime-shell accumulation.  The independent
checker does not import the producer and rebuilds the same matrices in
descending shell order.  Both verify finite values, symmetry, row roles,
normalization definitions, phase aggregates, provenance, and canonical JSON
hashes.  A rational 13-point anchor at
$[4200001,4200014)$ with $Q=8$ proves positive row geometry and symmetry for
the two declared laws.  The 25-case mutation suite rejects altered hashes,
roles, row census, summaries, exact anchor, and claim-firewall fields.

The ordinary and optimized producer outputs are identical, as are the
ordinary and optimized independent-checker outputs and stress outputs.  The
Bridge-B checker repeats these checks and locks every release artifact.

## Claim firewall

```text
TPC393_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC393_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC393_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC393_NORMALIZATION_PANEL = NUMERICALLY_CERTIFIED_FINITE_64_ROWS
TPC393_SCALAR_DEFINITIONS = PROVED_EXACT_FINITE_DECLARED
TPC393_PHASE_COMPARISON = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC393_CALIBRATION_FORECAST = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC393_ORIGIN_UNIFORMITY = OPEN
TPC393_COUNT_UNIFORMITY = OPEN
TPC393_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC393_GROWING_OPERATOR_BOUND = OPEN
TPC393_SOURCE_UNIFORM_L2 = OPEN
TPC393_ARITHMETIC_ADVANCE = NO
TPC393_FIXED_POWER_CREDIT = 0
TPC393_FULL_GATE_B = OPEN
TPC393_TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are absent from this checkout.  The
local proof package, independent checker, mutation suite, and Bridge-B
artifact are fail-closed repository evidence; they cannot declare an
official Route-A or Route-B pass.  In particular, no finite spectral or Schur
diagnostic is promoted to an analytic source estimate.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-393-c1-normalization-adversarial-holdout/code/tpc393_c1_normalization_adversarial_holdout.py --check
python -O -B papers/tpc-393-c1-normalization-adversarial-holdout/code/tpc393_c1_normalization_adversarial_holdout.py --check
python -B papers/tpc-393-c1-normalization-adversarial-holdout/experiments/tpc393_independent_checker.py --check
python -O -B papers/tpc-393-c1-normalization-adversarial-holdout/experiments/tpc393_independent_checker.py --check
python -B papers/tpc-393-c1-normalization-adversarial-holdout/experiments/tpc393_adversarial_certificate_stress.py --check
python -O -B papers/tpc-393-c1-normalization-adversarial-holdout/experiments/tpc393_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc393_c1_normalization_adversarial_holdout_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc393_c1_normalization_adversarial_holdout_checker.py --check
```

`paper/main.pdf` and `paper/paper.pdf` are required to be byte-identical.
