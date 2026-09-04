# TPC-392 — A Finite Normalization Phase Diagram

Author: Liang Wang  \
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

On a fresh coordinate-disjoint finite $c=1$ panel, three predeclared scalar
normalizations pass the 3% calibration-to-holdout forecast cap in all 8
law/$Q$ cells, while the local-diagonal normalization passes in 7/8 cells.
The only forecast failure is the alternating-index, $Q=8192$ local-diagonal
cell, with error $0.034106850682897649$.  This is a finite normalization
obstruction/phase comparison, not an arithmetic or twin-prime theorem.

## Frozen protocol

```text
schema = TPC392_C1_NORMALIZATION_PHASE_DIAGRAM_V1
candidate grid = a_j = 3800001 + 401 j, 0 <= j < 41
selected indices = 0,10,20,30,40
origins = 3800001,3804011,3808021,3812031,3816041
calibration origins = first three
holdout origins = last two
calibration counts = 1024,1280
holdout count = 1536
block length = 128
band mode = fixed_c3
Q = 2048,8192
kernel exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar,
                 origin_scalar, frozen_train_1024_scalar
forecast cap = 0.03; spectral cap = 0.64; Schur cap = 0.83
```

The grid, roles, counts, band, laws, and all four normalization choices were
fixed before current responses were read.  The TPC-391 parent is referenced by
hash as a frozen interface record, but its slope is deliberately not used in
the current fit.  The certificate contains 256 rows and 32 phase cells:
each cell has three calibration observations at each of two counts and two
terminal holdout observations.

## Normalization panel

For a matrix $M$ and row geometry $G$, the four choices are:

1. `local_diagonal`: $M_{uv}/\sqrt{G(u)G(v)}$;
2. `pooled_train_scalar`: the calibration-origin mean geometry at each
   calibration count, log-extrapolated to $1536$;
3. `origin_scalar`: the current-origin mean geometry at each count;
4. `frozen_train_1024_scalar`: one calibration-origin mean geometry at
   $N=1024$ used at every count.

The forecast for each phase cell uses the observed mean at $1024$ and the
log2 slope between the two calibration means, then predicts $1536$.  No
normalization is selected after seeing the holdout.

## Finite findings

```text
rows / cells = 256 / 32
forecast passes (local, pooled, origin, frozen) = 7/8, 8/8, 8/8, 8/8
maximum forecast error (local, pooled, origin, frozen) =
  0.034106850682897649, 0.0275714873542654,
  0.028962999969161629, 0.02757148735426429
terminal mean ordering = frozen, origin, pooled, local
terminal mean ratios to local =
  frozen about 1.0369, origin about 1.0222, pooled about 1.0209, local 1
spectral failures by normalization = 16,16,16,16
Schur failures by normalization = 0,0,0,0
within-one-percent stable cells at N=1024,1280,1536 = 25/32,28/32,24/32
```

The positive result is a complete finite pass for every scalar normalization
on the forecast criterion.  The obstruction is selective: local diagonal
scaling leaves one high-$Q$ alternating cell outside the cap, whereas all
three scalar choices remain inside it.  The similar spectral-failure counts
are retained as envelope diagnostics and are not interpreted as evidence that
one normalization changes the underlying matrix source.

## Claim firewall

```text
TPC392_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC392_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC392_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC392_NORMALIZATION_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS
TPC392_SCALAR_DEFINITIONS = PROVED_EXACT_FINITE_DECLARED
TPC392_PHASE_COMPARISON = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC392_CALIBRATION_FORECAST = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC392_ORIGIN_UNIFORMITY = OPEN
TPC392_COUNT_UNIFORMITY = OPEN
TPC392_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC392_GROWING_OPERATOR_BOUND = OPEN
TPC392_SOURCE_UNIFORM_L2 = OPEN
TPC392_ARITHMETIC_ADVANCE = NO
TPC392_FIXED_POWER_CREDIT = 0
TPC392_FULL_GATE_B = OPEN
TPC392_TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are absent from this checkout.  The
local checker and Bridge-B artifact are fail-closed repository evidence; they
cannot declare an official Route-A or Route-B pass.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-392-c1-normalization-phase-diagram/code/tpc392_c1_normalization_phase_diagram.py --check
python -O -B papers/tpc-392-c1-normalization-phase-diagram/code/tpc392_c1_normalization_phase_diagram.py --check
python -B papers/tpc-392-c1-normalization-phase-diagram/experiments/tpc392_independent_checker.py --check
python -O -B papers/tpc-392-c1-normalization-phase-diagram/experiments/tpc392_independent_checker.py --check
python -B papers/tpc-392-c1-normalization-phase-diagram/experiments/tpc392_adversarial_certificate_stress.py --check
python -O -B papers/tpc-392-c1-normalization-phase-diagram/experiments/tpc392_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc392_c1_normalization_phase_diagram_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc392_c1_normalization_phase_diagram_checker.py --check
```

`paper/main.pdf` and `paper/paper.pdf` are required to be byte-identical.
