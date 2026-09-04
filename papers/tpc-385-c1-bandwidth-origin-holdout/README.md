# TPC-385 — c=1 bandwidth-phase origin holdout

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-385 freezes the TPC-384 high-bandwidth phase forecast, uses three fresh
origins only to define a pooled training geometry, and tests two later origins
as a response-blind holdout. On a new coordinate-disjoint panel with
`c=2,3`, `Q=2048,8192`, four laws, and local versus calibration-pooled
normalization, the all-plus `Q=8192` holdout means miss the locked parent
forecasts by at most `2.4194960054838229e-5` in relative value (all four
forecast cells pass the predeclared one-percent cap). The signed controls
remain unstable at lower Q, so this is a finite all-plus transfer result plus
a law-uniformity obstruction, not an arithmetic theorem.

## Frozen protocol

```text
candidate grid = a_j = 2000001 + 401 j, 0 <= j < 41
selected indices = 0,10,20,30,40 -> origins 2000001,2004011,2008021,2012031,2016041
calibration origins = 2000001,2004011,2008021
holdout origins = 2012031,2016041
window count = 512 (four contiguous blocks of length 128)
band cutoffs = c=2,3; Q = 2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar
spread cap = 0.01; forecast-error cap = 0.01
spectral cap = 0.64; Schur cap = 0.83
```

The calibration/holdout split and the bandwidth menu are fixed before any
response, signed metric, or geometry score is read. The pooled scalar is the
mean row geometry over the three calibration origins only, so the holdout
does not enter its denominator. The parent forecasts are copied from the
hash-locked TPC-384 all-plus `Q=8192` phase means; no TPC-385 response is used
to fit or select them.

The exact `q=8` anchor is `[2000001,2000014)` with shell `[11,13]`. Rational
arithmetic verifies positive geometry and symmetry for all four declared laws.
All current intervals are disjoint from the prior coordinate panels.

## Main finite observations

The complete Cartesian panel contains 160 rows and 32 cells. Calibration and
holdout stability counts are respectively `26/32` and `28/32`. Every row is
below the fixed spectral and Schur caps. The largest holdout spread is
`0.033223638943350384`, attained by the alternating-index law at `c=3,
Q=2048` under local normalization; hence the holdout is not law-uniform.

For the all-plus `Q=8192` forecast cells, the locked parent value and the new
holdout mean are:

```text
c=2 local:  parent 0.61397411407532332 -> holdout 0.61397983891736552
c=2 pooled: parent 0.63384010801912960 -> holdout 0.63382483811179768
c=3 local:  parent 0.62079971051100025 -> holdout 0.62080564043709352
c=3 pooled: parent 0.63888760360944985 -> holdout 0.63887214574940099
```

The corresponding relative forecast errors are
`9.3242400794378472e-06`, `-2.4091103006462619e-05`,
`9.5520761251517647e-06`, and `-2.4194960054838229e-05`.

## Claim firewall

```text
TPC385_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC385_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC385_PARENT_PHASE_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC385_ORIGIN_HOLDOUT_PANEL = NUMERICALLY_CERTIFIED_FINITE_160_ROWS
TPC385_HOLDOUT_HIGH_Q_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC385_FORECAST_ERROR_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC385_BANDWIDTH_MONOTONICITY = OPEN
TPC385_LAW_UNIFORMITY = OPEN
TPC385_ORIGIN_UNIFORMITY = OPEN
TPC385_COUNT_SCALE_UNIFORMITY = OPEN
TPC385_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC385_GROWING_OPERATOR_BOUND = OPEN
TPC385_SOURCE_UNIFORM_L2 = OPEN
TPC385_ARITHMETIC_ADVANCE = NO
TPC385_FIXED_POWER_CREDIT = 0
TPC385_FULL_GATE_B = OPEN
TPC385_TWIN_PRIME_RESULT = NONE
```

The official Session Route-A/Route-B evaluator files are absent from this
checkout. The local Bridge-B checker is therefore fail-closed repository
evidence, not an official route verdict. No finite transfer value pays a
fixed-power gate.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-385-c1-bandwidth-origin-holdout/code/tpc385_c1_bandwidth_origin_holdout.py --write
python -B papers/tpc-385-c1-bandwidth-origin-holdout/code/tpc385_c1_bandwidth_origin_holdout.py --check
python -O -B papers/tpc-385-c1-bandwidth-origin-holdout/code/tpc385_c1_bandwidth_origin_holdout.py --check
python -B papers/tpc-385-c1-bandwidth-origin-holdout/experiments/tpc385_independent_checker.py --check
python -O -B papers/tpc-385-c1-bandwidth-origin-holdout/experiments/tpc385_independent_checker.py --check
python -B papers/tpc-385-c1-bandwidth-origin-holdout/experiments/tpc385_adversarial_certificate_stress.py --check
python -O -B papers/tpc-385-c1-bandwidth-origin-holdout/experiments/tpc385_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc385_c1_bandwidth_origin_holdout_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc385_c1_bandwidth_origin_holdout_checker.py --check
```

`ROUND2_CLUE = TEST_C1_HOLDOUT_COUNT_BANDWIDTH`.
