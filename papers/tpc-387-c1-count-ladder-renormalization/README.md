# TPC-387 — c=1 count-ladder renormalization

Author: Liang Wang

Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-387 follows the TPC-386 count obstruction with a predeclared three-level
ladder. Three fresh origins are evaluated at `N=512` and `N=768` for
calibration; two later, coordinate-disjoint origins at `N=1024` are holdout.
For each fixed law, bandwidth mode, normalization, and `Q`, the calibration
means define a log-count slope, which is extrapolated once to `N=1024`.
All 32 holdout prediction cells fall within the 3% finite extrapolation cap;
the worst error is `2.6051162042932119e-2`. This is a finite calibration repair
and a useful obstruction localizer, not a count-uniform theorem.

## Frozen protocol

```text
candidate grid = a_j = 2400001 + 401 j, 0 <= j < 41
selected indices = 0,10,20,30,40 -> origins 2400001,2404011,2408021,2412031,2416041
calibration origins = 2400001,2404011,2408021 at N=512 and N=768
holdout origins = 2412031,2416041 at N=1024
block length = 128; bands = fixed_c3 and full_relative
Q = 2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar
spread cap = 0.01; renormalization-error cap = 0.03
spectral cap = 0.64; Schur cap = 0.83
```

The slope fit uses only calibration means at `N=512,768`; the holdout count
and response are never used to choose the slope, band, law, or normalization.
For pooled normalization, the geometry scalar itself is extrapolated from
the two calibration counts before any holdout matrix is normalized. The exact
anchor is `[2400001,2400014)` with shell `[11,13]`.

## Main finite observations

The certificate contains 256 rows and 32 cells. Stability counts for the
`N=512`, `N=768`, and `N=1024` holdout levels are respectively `24/32`,
`24/32`, and `28/32`. There are 40 inherited spectral-cap failures and no
Schur-cap failures; the failures are the expected finite cap diagnostic and
do not invalidate the slope replay. The four all-plus `Q=8192` cells are:

```text
fixed_c3 / local:       alpha=0.10521430967088292, prediction=0.66776895312565909,
                         holdout/prediction=0.99029616174013824
fixed_c3 / pooled:      alpha=0.10719771655467236, prediction=0.68817196243541745,
                         holdout/prediction=0.98120548997303492
full_relative / local:  alpha=0.12823547329343729, prediction=0.67851004902290069,
                         holdout/prediction=0.99350291942760782
full_relative / pooled: alpha=0.12430582315319380, prediction=0.69638118356936107,
                         holdout/prediction=0.98554136956324923
```

The largest absolute error over all 32 law/mode/normalization/Q cells is
`0.026051162042932119`, from `Q=2048`, alternating-index, fixed-c3, pooled
normalization. Thus the 3% cap is a panel-wide statement, not an all-plus-only
fit. The all-plus endpoint is predicted substantially better, with errors
between `0.006497` and `0.018795` in the four high-Q cells.

## Claim firewall

```text
TPC387_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC387_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC387_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC387_COUNT_LADDER_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS
TPC387_CALIBRATION_SLOPE_REPAIR = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC387_RENORM_FORECAST_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC387_FIXED_CAP_REPAIR = OPEN
TPC387_COUNT_UNIFORMITY = OPEN
TPC387_BANDWIDTH_RENORMALIZATION = OPEN
TPC387_LAW_UNIFORMITY = OPEN
TPC387_ORIGIN_UNIFORMITY = OPEN
TPC387_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC387_GROWING_OPERATOR_BOUND = OPEN
TPC387_SOURCE_UNIFORM_L2 = OPEN
TPC387_ARITHMETIC_ADVANCE = NO
TPC387_FIXED_POWER_CREDIT = 0
TPC387_FULL_GATE_B = OPEN
TPC387_TWIN_PRIME_RESULT = NONE
```

The official Session Route-A/Route-B evaluator files are absent from this
checkout. The local Bridge-B checker is fail-closed repository evidence, not
an official route verdict. No finite slope fit pays a fixed-power gate.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-387-c1-count-ladder-renormalization/code/tpc387_c1_count_ladder_renormalization.py --write
python -B papers/tpc-387-c1-count-ladder-renormalization/code/tpc387_c1_count_ladder_renormalization.py --check
python -O -B papers/tpc-387-c1-count-ladder-renormalization/code/tpc387_c1_count_ladder_renormalization.py --check
python -B papers/tpc-387-c1-count-ladder-renormalization/experiments/tpc387_independent_checker.py --check
python -O -B papers/tpc-387-c1-count-ladder-renormalization/experiments/tpc387_independent_checker.py --check
python -B papers/tpc-387-c1-count-ladder-renormalization/experiments/tpc387_adversarial_certificate_stress.py --check
python -O -B papers/tpc-387-c1-count-ladder-renormalization/experiments/tpc387_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc387_c1_count_ladder_renormalization_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc387_c1_count_ladder_renormalization_checker.py --check
```

`ROUND2_CLUE = TEST_C1_COUNT_LADDER_SECOND_HOLDOUT`.
