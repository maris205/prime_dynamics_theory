# TPC-384 — c=1 bandwidth/normalization phase diagram

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-384 holds the raw prime-shell matrix and its square-energy geometry fixed
and crosses four predeclared block-distance bandwidths `c=0,1,2,3` with local
diagonal and pooled-scalar normalizations on a fresh response-blind `N=512`
origin panel. The complete 288-row phase diagram shows that origin-spread
stability is law- and bandwidth-dependent, while the all-plus high-Q magnitude
approaches the fixed spectral cap as bandwidth widens. The pooled/local
calibration shift is negative at `c=0` (`-9.7684465801723214%`) and positive
at `c=1,2,3` (`3.6462270672765848%`, `3.2356403125121616%`,
`2.9136439325271071%`). This is finite model-relative evidence only; it does
not prove bandwidth monotonicity, source-valid normalization, arithmetic
cancellation, or a twin-prime theorem.

## Frozen protocol

```text
candidate grid = a_j = 1800001 + 401 j, 0 <= j < 41
selected indices = 0,20,40 -> origins 1800001,1808021,1816041
window count = 512 (four contiguous blocks of length 128)
band cutoffs = c=0,1,2,3, fixed before metric readout
Q = 512,2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_scalar
origin-spread cap = (max-min)/mean <= 0.01
spectral cap = 0.64; Schur cap = 0.83
```

For each origin and shell anchor, the raw law matrices are assembled from the
same centered divisibility components. The geometry is the sum of squared
components before any bandwidth or law is applied. `local_diagonal` divides by
the corresponding geometric row factors; `pooled_scalar` divides by the mean
geometry over the three fixed origins at that `Q`. The bandwidth mask keeps
entries whose block indices differ by at most `c`.

The exact q=8 anchor is `[1800001,1800014)` with shell `[11,13]`. Rational
arithmetic verifies positive geometry and symmetry for every declared law; all
four bandwidth masks are represented because the anchor lies in one block.
The current intervals are endpoint-disjoint from all earlier coordinate panels.

## Main finite observations

The diagram contains 288 rows and 96 origin-spread cells. Stable-cell counts
(out of 12 law/Q cells for each bandwidth and normalization) are:

```text
c=0: local 6/12, pooled 7/12
c=1: local 8/12, pooled 7/12
c=2: local 8/12, pooled 8/12
c=3: local 8/12, pooled 8/12
```

All 288 rows are below the fixed spectral and Schur caps on this finite panel;
this is a scoped census, not an asymptotic norm theorem. The alternating-index
law supplies the persistent instability (for example, its c=3 pooled high-Q
spread is `0.039758700305072295`), whereas all-plus is stable in every listed
high-Q cell. The all-plus pooled high-Q mean rises from `0.36656315295619812`
at `c=0` to `0.63888760360944985` at `c=3`, close to but below the `0.64`
cap.

## Claim firewall

```text
TPC384_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC384_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC384_BANDWIDTH_PHASE_PANEL = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC384_LOCAL_POOLED_NORMALIZATION_CROSSING = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC384_ORIGIN_SPREAD_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC384_ALL_PLUS_HIGH_Q_BAND_PHASE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC384_SCHUR_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC384_BANDWIDTH_MONOTONICITY = OPEN
TPC384_ORIGIN_UNIFORMITY = OPEN
TPC384_WINDOW_SCALE_UNIFORMITY = OPEN
TPC384_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC384_GROWING_OPERATOR_BOUND = OPEN
TPC384_SOURCE_UNIFORM_L2 = OPEN
TPC384_ARITHMETIC_ADVANCE = NO
TPC384_FIXED_POWER_CREDIT = 0
TPC384_FULL_GATE_B = OPEN
TPC384_TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are absent from this checkout. The local
Bridge-B checker is therefore fail-closed repository evidence, not an official
Route-A or Route-B verdict. No value in this paper pays the fixed-power gate.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-384-c1-bandwidth-normalization-phase-diagram/code/tpc384_c1_bandwidth_normalization_phase_diagram.py --write
python -B papers/tpc-384-c1-bandwidth-normalization-phase-diagram/code/tpc384_c1_bandwidth_normalization_phase_diagram.py --check
python -O -B papers/tpc-384-c1-bandwidth-normalization-phase-diagram/code/tpc384_c1_bandwidth_normalization_phase_diagram.py --check
python -B papers/tpc-384-c1-bandwidth-normalization-phase-diagram/experiments/tpc384_independent_checker.py --check
python -O -B papers/tpc-384-c1-bandwidth-normalization-phase-diagram/experiments/tpc384_independent_checker.py --check
python -B papers/tpc-384-c1-bandwidth-normalization-phase-diagram/experiments/tpc384_adversarial_certificate_stress.py --check
python -O -B papers/tpc-384-c1-bandwidth-normalization-phase-diagram/experiments/tpc384_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc384_c1_bandwidth_normalization_phase_diagram_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc384_c1_bandwidth_normalization_phase_diagram_checker.py --check
```

`ROUND2_CLUE = TEST_C1_BANDWIDTH_ORIGIN_HOLDOUT`.
