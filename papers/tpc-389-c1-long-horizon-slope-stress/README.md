# TPC-389 — Long-Horizon Stress Test for a Frozen Count Slope

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-389 tests the TPC-388 parent slope on the next finite count interval.  On
a third, coordinate-disjoint origin family, three calibration origins at
`N=768,1024` predict two holdout origins at `N=1280`.  The frozen parent
forecast, a same-family local forecast, and a recursive parent forecast all
pass the predeclared 3% finite ratio cap in all 32 cells.  The strongest
positive number is therefore a finite longer-horizon transfer, not a theorem.

The main obstruction is unchanged and becomes more visible: 64 of 256 rows
cross the inherited `0.64` spectral diagnostic, while no Schur row crosses
`0.83`.  No arithmetic credit, Route-A/Route-B pass, or twin-prime result is
claimed.

## Frozen protocol

```text
candidate grid = a_j = 2800001 + 401 j, 0 <= j < 41
selected indices = 0,10,20,30,40
origins = 2800001,2804011,2808021,2812031,2816041
calibration origins = first three at N=768 and N=1024
holdout origins = last two at N=1280
block length = 128; bands = fixed_c3, full_relative
Q = 2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar
parent slope = frozen TPC-388 cell slope; no current-family refit
local control = current-family 768 -> 1024 logarithmic slope
anchored horizon = N=1024 -> N=1280
recursive horizon = N=768 -> N=1280 using the frozen parent slope
finite ratio cap = 0.03; spectral cap = 0.64; Schur cap = 0.83
```

All origins, roles, laws, bands, and normalizations are fixed before current
responses are read.  The parent code and certificate are checked by SHA-256.
The current panel has 256 rows and 32 cells.

## Certified finite observations

| quantity | finite result |
|---|---:|
| parent anchored horizon pass | 32/32 |
| local-control horizon pass | 32/32 |
| recursive parent horizon pass | 32/32 |
| maximum anchored parent error | 0.017615584096739245 |
| maximum local-control error | 0.011997515978539264 |
| maximum recursive parent error | 0.029949940590637381 |
| stable cells at `N=768` / `N=1024` / holdout `N=1280` | 24/32 / 27/32 / 24/32 |
| spectral failures | 64/256 |
| Schur failures | 0/256 |

The recursive maximum is close to the 3% boundary; it is a finite stress
signal, not evidence of an asymptotic law.  The largest anchored error is the
fixed-three-block, pooled, all-plus, `Q=8192` cell.  The largest recursive
error is the fixed-three-block, pooled, half-split, `Q=2048` cell.

## Claim firewall

```text
TPC389_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC389_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC389_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC389_LONG_HORIZON_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS
TPC389_PARENT_HORIZON_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC389_LOCAL_CONTROL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC389_RECURSIVE_PARENT_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC389_ORIGIN_UNIFORMITY = OPEN
TPC389_COUNT_UNIFORMITY = OPEN
TPC389_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC389_GROWING_OPERATOR_BOUND = OPEN
TPC389_SOURCE_UNIFORM_L2 = OPEN
TPC389_ARITHMETIC_ADVANCE = NO
TPC389_FIXED_POWER_CREDIT = 0
TPC389_FULL_GATE_B = OPEN
TPC389_TWIN_PRIME_RESULT = NONE
```

The official Session `propose.md`, Route-A evaluator, and Route-B evaluator are
not present in this checkout.  The local Bridge-B checker is fail-closed
repository evidence only.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-389-c1-long-horizon-slope-stress/code/tpc389_long_horizon_slope_stress.py --check
python -O -B papers/tpc-389-c1-long-horizon-slope-stress/code/tpc389_long_horizon_slope_stress.py --check
python -B papers/tpc-389-c1-long-horizon-slope-stress/experiments/tpc389_independent_checker.py --check
python -O -B papers/tpc-389-c1-long-horizon-slope-stress/experiments/tpc389_independent_checker.py --check
python -B papers/tpc-389-c1-long-horizon-slope-stress/experiments/tpc389_adversarial_certificate_stress.py --check
python -O -B papers/tpc-389-c1-long-horizon-slope-stress/experiments/tpc389_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc389_c1_long_horizon_slope_stress_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc389_c1_long_horizon_slope_stress_checker.py --check
```

`ROUND2_CLUE = TEST_C1_RECURSIVE_SLOPE_COMPOSITION`.
