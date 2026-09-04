# TPC-388 — Cross-Family Count-Ladder Slope Transfer

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-388 freezes the 32 calibration slopes learned by TPC-387 and transfers
them, without refitting, to a new coordinate-disjoint origin family.  The
new family has three calibration origins at `N=512,768` and two endpoint
holdout origins at `N=1024`.  All 32 parent-slope forecasts and all 32
same-family control forecasts are within the predeclared 3% finite error cap;
the worst parent-transfer error is `0.023402666610706224`.

This is a finite origin-transfer certificate.  It does not establish an
origin-uniform count law, source-valid normalization, arithmetic `L2`, a
Route-A/Route-B pass, or the twin-prime conjecture.

## Frozen protocol

```text
candidate grid = a_j = 2600001 + 401 j, 0 <= j < 41
selected indices = 0,10,20,30,40 -> origins 2600001,2604011,2608021,2612031,2616041
calibration origins = 2600001,2604011,2608021 at N=512 and N=768
holdout origins = 2612031,2616041 at N=1024
block length = 128; modes = fixed_c3, full_relative
Q = 2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar
transfer rule = TPC-387 cell slope, applied to current-family N=768 mean
control rule = current-family 512 -> 768 slope, applied to current-family N=768 mean
transfer error cap = 0.03; spectral cap = 0.64; Schur cap = 0.83
```

The current-family response is never used to choose the origins, roles, band,
law, normalization, or the frozen parent slope.  For pooled normalization,
the current family's geometry scalar is calibrated only from its own
`N=512,768` calibration observations; this isolates the spectral-slope
transfer question from an unproved cross-origin normalization assertion.

## Main finite observations

The certificate has 256 rows and 32 cells.  Stability counts at `N=512`,
`N=768`, and the endpoint holdout are `24/32`, `24/32`, and `28/32`.
There are 40 inherited spectral-cap diagnostics above `0.64` and no Schur
failures.  The parent-family transfer passes `32/32` cells, as does the
same-family recalibration control.  The largest parent/local slope mismatch
over the 32 cells is approximately `0.0595582578690082`; the two forecasts
are nevertheless close on this finite endpoint panel.

For the four all-plus `Q=8192` cells, parent-slope endpoint ratios are:

```text
fixed_c3 / local:       parent alpha=0.10521430967088292, error=-0.0096993952293589203
fixed_c3 / pooled:      parent alpha=0.10719771655467236, error=-0.018788420382920612
full_relative / local:  parent alpha=0.12823547329343729, error=-0.0064932010288080155
full_relative / pooled: parent alpha=0.12430582315319380, error=-0.014451862558032991
```

The largest parent-transfer deviation occurs for the `Q=8192`, fixed-three-
block, pooled, mod-4-character cell.  The result is a positive finite
cross-family check, while the unchanged spectral-cap failures are the main
obstruction to interpreting it as a uniform operator statement.

## Claim firewall

```text
TPC388_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC388_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC388_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC388_CROSS_FAMILY_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS
TPC388_PARENT_SLOPE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC388_LOCAL_CONTROL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC388_ORIGIN_UNIFORMITY = OPEN
TPC388_COUNT_UNIFORMITY = OPEN
TPC388_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC388_GROWING_OPERATOR_BOUND = OPEN
TPC388_SOURCE_UNIFORM_L2 = OPEN
TPC388_ARITHMETIC_ADVANCE = NO
TPC388_FIXED_POWER_CREDIT = 0
TPC388_FULL_GATE_B = OPEN
TPC388_TWIN_PRIME_RESULT = NONE
```

The Session's official `propose.md`, Route-A evaluator, and Route-B evaluator
are absent from this checkout.  The local Bridge-B checker is fail-closed
repository evidence only.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-388-c1-cross-family-slope-transfer/code/tpc388_c1_cross_family_slope_transfer.py --check
python -O -B papers/tpc-388-c1-cross-family-slope-transfer/code/tpc388_c1_cross_family_slope_transfer.py --check
python -B papers/tpc-388-c1-cross-family-slope-transfer/experiments/tpc388_independent_checker.py --check
python -O -B papers/tpc-388-c1-cross-family-slope-transfer/experiments/tpc388_independent_checker.py --check
python -B papers/tpc-388-c1-cross-family-slope-transfer/experiments/tpc388_adversarial_certificate_stress.py --check
python -O -B papers/tpc-388-c1-cross-family-slope-transfer/experiments/tpc388_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc388_c1_cross_family_slope_transfer_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc388_c1_cross_family_slope_transfer_checker.py --check
```

`ROUND2_CLUE = TEST_C1_CROSS_FAMILY_SLOPE_STRESS`.
