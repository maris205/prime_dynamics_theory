# TPC-386 — c=1 count-holdout bandwidth audit

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-386 changes the window count, rather than the origin, after the TPC-385
origin transfer. Three fresh `N=512` windows define a pooled training
geometry and two coordinate-disjoint `N=1024` windows are read out without
fitting. At `Q=8192`, the all-plus holdout spectral means are
`0.66128869232935972` (fixed three-block band, local normalization),
`0.70994276045799443` (fixed band, pooled training scalar),
`0.67410095164922046` (full relative band, local), and
`0.72158587088858872` (full relative band, pooled). They are 6.52%--12.94%
above the corresponding `N=512` calibration/reference values. Thus the
TPC-385 origin transfer does not transfer the inherited `0.64` finite
spectral cap to a larger count: all 16 all-plus `N=1024` rows exceed that
diagnostic cap. This is a finite count obstruction, not an asymptotic
counterexample or an arithmetic theorem.

## Frozen protocol

```text
candidate grid = a_j = 2200001 + 401 j, 0 <= j < 41
selected indices = 0,10,20,30,40 -> origins 2200001,2204011,2208021,2212031,2216041
calibration origins = 2200001,2204011,2208021; count N=512
holdout origins = 2212031,2216041; count N=1024
block length = 128; fixed band = |block_i-block_j| <= 3
full relative band = all block pairs at the relevant count
Q = 2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar
spread cap = 0.01; count-transfer cap = 0.20
spectral cap = 0.64; Schur cap = 0.83
```

The count split, origins, and both band modes are fixed before any response
is read. The pooled scalar is computed from the three calibration geometries
only. The parent reference is the hash-locked TPC-385 all-plus `Q=8192`
phase value; it is not fitted to the holdout. The exact rational anchor is
`[2200001,2200014)` with shell `[11,13]`.

## Main finite observations

The complete Cartesian panel contains 160 rows and 32 cells. All Schur rows
remain below `0.83`; 16 rows fail the inherited `0.64` spectral diagnostic,
and every failure is an all-plus `N=1024` row. Calibration and holdout
stability counts are `20/32` and `28/32`. The `Q=8192` all-plus count ratios
are:

```text
fixed_c3 / local:       1.0652156493536045  (log2 ratio 0.09114552881605917)
fixed_c3 / pooled:      1.1112204434769593  (log2 ratio 0.15214504639695708)
full_relative / local:  1.0858538657474437  (log2 ratio 0.11882995825517124)
full_relative / pooled: 1.1294445356950271 (log2 ratio 0.17561342518655618)
```

All four ratios are inside the deliberately broad finite `0.20` transfer
envelope, but that envelope is an operational audit threshold, not a bound
uniform in the count. Comparing fixed and full bands shows that the cap
failure is already present in the fixed three-block band; adding the remote
blocks increases the value but is not the sole cause.

## Claim firewall

```text
TPC386_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC386_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC386_PARENT_PHASE_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC386_COUNT_HOLDOUT_PANEL = NUMERICALLY_CERTIFIED_FINITE_160_ROWS
TPC386_ALL_PLUS_COUNT_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC386_FIXED_SPECTRAL_CAP_TRANSFER = REFUTED_FINITE_SCOPED
TPC386_COUNT_UNIFORMITY = OPEN
TPC386_BANDWIDTH_RENORMALIZATION = OPEN
TPC386_LAW_UNIFORMITY = OPEN
TPC386_ORIGIN_UNIFORMITY = OPEN
TPC386_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC386_GROWING_OPERATOR_BOUND = OPEN
TPC386_SOURCE_UNIFORM_L2 = OPEN
TPC386_ARITHMETIC_ADVANCE = NO
TPC386_FIXED_POWER_CREDIT = 0
TPC386_FULL_GATE_B = OPEN
TPC386_TWIN_PRIME_RESULT = NONE
```

The official Session Route-A/Route-B evaluator files are absent from this
checkout. The local Bridge-B checker is consequently fail-closed repository
evidence, not an official route verdict. No finite count observation pays a
fixed-power gate.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-386-c1-count-holdout-bandwidth/code/tpc386_c1_count_holdout_bandwidth.py --write
python -B papers/tpc-386-c1-count-holdout-bandwidth/code/tpc386_c1_count_holdout_bandwidth.py --check
python -O -B papers/tpc-386-c1-count-holdout-bandwidth/code/tpc386_c1_count_holdout_bandwidth.py --check
python -B papers/tpc-386-c1-count-holdout-bandwidth/experiments/tpc386_independent_checker.py --check
python -O -B papers/tpc-386-c1-count-holdout-bandwidth/experiments/tpc386_independent_checker.py --check
python -B papers/tpc-386-c1-count-holdout-bandwidth/experiments/tpc386_adversarial_certificate_stress.py --check
python -O -B papers/tpc-386-c1-count-holdout-bandwidth/experiments/tpc386_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc386_c1_count_holdout_bandwidth_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc386_c1_count_holdout_bandwidth_checker.py --check
```

`ROUND2_CLUE = TEST_C1_COUNT_LADDER_RENORMALIZATION`.
