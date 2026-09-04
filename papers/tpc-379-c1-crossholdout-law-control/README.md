# TPC-379 — c=1 cross-holdout law control

**Author:** Liang Wang<br>
**Affiliation:** School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-379 freezes a new coordinate-disjoint affine origin family and compares
four sign laws on the same finite normalized `c=1` prime-shell operator.  The
36-row panel uses three origins, `N=1024`, and `Q=512,2048,8192`.  The all-plus
law has profile `(0,3,3)` and 6/9 spectral-cap failures; the three signed
controls (`alternating_index`, `mod4_character`, `half_split`) each have
profile `(0,0,0)`.  All 36 Schur values are below the working cap.

This is a finite law-dependence obstruction.  It shows that the inherited
high-Q band signature is not invariant across the declared sign family; it
does not prove that any law is the correct arithmetic object, nor does it
provide an asymptotic or twin-prime result.

## Frozen protocol

```text
candidate grid = a_j = 1200001 + 401 j, 0 <= j < 41
selected indices = 0,20,40  -> origins 1200001,1208021,1216041
window count    = 1024 (four contiguous blocks of length 256)
band            = block distance <= 1 (inherited c=1)
Q              = 512,2048,8192
kernel         = exponent 1, height 66, beta 2
laws           = all_plus, alternating_index, mod4_character, half_split
caps           = spectral 0.64, Schur 0.83
normalization  = one common square-energy geometry for all four laws
```

The grid indices, all four laws, and the complete Cartesian panel are fixed
before any response, geometry score, or signed metric is read.  The six
current intervals are disjoint from the largest declared TPC-376, TPC-377,
and TPC-378 intervals by exact integer endpoint inequalities.

The observed band spectral maxima are:

```text
all_plus           0.65334758792533143
alternating_index  0.0094084540584888146
mod4_character     0.011835976723613296
half_split         0.2117349490215118
```

The exact rational anchor is the 13-point interval `[1200001,1200014)` at
`Q=8`; it verifies positive common geometry, symmetry, and the four signed
matrix constructions.  Its law-specific digests are stored in the
certificate.

## Claim firewall

```text
TPC379_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC379_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC379_COMMON_GEOMETRY = PROVED_EXACT_FINITE_LAW_INDEPENDENT
TPC379_LAW_FAMILY = PROVED_EXACT_FINITE_PREDECLARED
TPC379_LAW_CONTROL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_36_ROWS
TPC379_ALL_PLUS_FAILURE_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC379_SIGNED_CONTROL_SUBCAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC379_RAYLEIGH_TAIL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC379_LAW_UNIFORMITY = OPEN
TPC379_ORIGIN_UNIFORMITY = OPEN
TPC379_WINDOW_SCALE_UNIFORMITY = OPEN
TPC379_CROSS_BLOCK_CAUSALITY = OPEN
TPC379_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC379_GROWING_OPERATOR_BOUND = OPEN
TPC379_SOURCE_UNIFORM_L2 = OPEN
TPC379_ARITHMETIC_ADVANCE = NO
TPC379_FIXED_POWER_CREDIT = 0
TPC379_FULL_GATE_B = OPEN
TPC379_TWIN_PRIME_RESULT = NONE
```

No arithmetic power saving, Route-B reassembly, or twin-prime conclusion is
claimed.  The official Session-named Route-A/Route-B evaluator files are not
present in this checkout; the local Bridge-B is fail-closed repository
evidence only.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-379-c1-crossholdout-law-control/code/tpc379_c1_crossholdout_law_control.py --write
python -B papers/tpc-379-c1-crossholdout-law-control/code/tpc379_c1_crossholdout_law_control.py --check
python -O -B papers/tpc-379-c1-crossholdout-law-control/code/tpc379_c1_crossholdout_law_control.py --check
python -B papers/tpc-379-c1-crossholdout-law-control/experiments/tpc379_independent_checker.py --check
python -O -B papers/tpc-379-c1-crossholdout-law-control/experiments/tpc379_independent_checker.py --check
python -B papers/tpc-379-c1-crossholdout-law-control/experiments/tpc379_adversarial_certificate_stress.py --check
python -O -B papers/tpc-379-c1-crossholdout-law-control/experiments/tpc379_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc379_c1_crossholdout_law_control_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc379_c1_crossholdout_law_control_checker.py --check
```

The independent checker uses a direct sieve to 20000, reverse-shell
accumulation, independent common-geometry construction, and independent
full/band eigensystems.  The stress checker applies 25 semantic and schema
mutations and requires every one to be rejected.

## Route evaluation

The strongest positive result is a complete finite, response-blind,
coordinate-disjoint law panel with an exact common normalization and a
reproducible all-plus/control separation.  The strongest obstruction is that
the high-Q all-plus threshold profile disappears under every one of the three
declared signed controls, so the profile cannot be treated as a law-invariant
operator phenomenon.  The reusable structure is a common-geometry,
common-band law-control panel with an exact rational anchor and selected-mode
band/tail audit.

`ROUND2_CLUE = TEST_C1_LAW_CONTROL_COUNT_REPLAY`.
