# TPC-383 — c=1 pooled-normalization cross-origin audit

**Author:** Liang Wang<br>
**Affiliation:** School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-383 tests whether the TPC-382 magnitude observation is an artifact of
row-wise diagonal normalization.  On a fresh, response-blind `N=512` panel
with origins `(1600001,1608021,1616041)`, three Q anchors, four laws, and the
same `c=1` band, it compares local diagonal whitening with a scalar pooled
geometry normalization.  All-plus remains within the fixed one-percent
origin-spread cap at high Q under both normalizations; the pooled value is
shifted upward by `3.6457251256851203%` at `Q=8192`.  Alternating-index remains
the least stable law (pooled high-Q spread `0.10104585338571119`).  This
separates finite profile transfer from absolute magnitude calibration; it does
not supply a source-valid normalization or an arithmetic theorem.

## Frozen protocol

```text
candidate grid = a_j = 1600001 + 401 j, 0 <= j < 41
selected indices = 0,20,40 -> origins 1600001,1608021,1616041
window count = 512 (four contiguous blocks of length 128)
band = block distance <= 1
Q = 512,2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_scalar
spread cap = (max-min)/mean <= 0.01, fixed before metric readout
```

The pooled scalar at each Q is the mean of all coordinate geometries over the
three preselected origins.  It is common to all laws at that Q.  The first
13-point interval `[1600001,1600014)` gives the exact q=8 shell `[11,13]`
anchor; exact rational geometry is positive and symmetric for all four laws.
The current intervals are endpoint-disjoint from the prior coordinate panels.

The all-plus high-Q relative spreads are
`1.1394111498671383e-5` (local) and `4.6321361430822112e-5` (pooled).  The
local and pooled stability censuses are both `9/12`; the three failures in
each census are the alternating-index cells.

## Claim firewall

```text
TPC383_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC383_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC383_NORMALIZATION_FAMILY = PROVED_EXACT_FINITE_LAW_INDEPENDENT
TPC383_LOCAL_POOLED_PANEL = NUMERICALLY_CERTIFIED_FINITE_72_ROWS
TPC383_ALL_PLUS_HIGH_Q_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC383_NORMALIZATION_MAGNITUDE_SHIFT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC383_LAW_SPREAD_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC383_ORIGIN_UNIFORMITY = OPEN
TPC383_WINDOW_SCALE_UNIFORMITY = OPEN
TPC383_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC383_GROWING_OPERATOR_BOUND = OPEN
TPC383_SOURCE_UNIFORM_L2 = OPEN
TPC383_ARITHMETIC_ADVANCE = NO
TPC383_FIXED_POWER_CREDIT = 0
TPC383_FULL_GATE_B = OPEN
TPC383_TWIN_PRIME_RESULT = NONE
```

The local/pooled comparison is a finite modelling audit.  It cannot validate
that either normalization is the arithmetic source normalization, and it does
not close Route A or Route B.  The official Session evaluator files are absent
from this checkout; the local Bridge-B is fail-closed repository evidence only.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-383-c1-pooled-normalization-audit/code/tpc383_c1_pooled_normalization_audit.py --write
python -B papers/tpc-383-c1-pooled-normalization-audit/code/tpc383_c1_pooled_normalization_audit.py --check
python -O -B papers/tpc-383-c1-pooled-normalization-audit/code/tpc383_c1_pooled_normalization_audit.py --check
python -B papers/tpc-383-c1-pooled-normalization-audit/experiments/tpc383_independent_checker.py --check
python -O -B papers/tpc-383-c1-pooled-normalization-audit/experiments/tpc383_independent_checker.py --check
python -B papers/tpc-383-c1-pooled-normalization-audit/experiments/tpc383_adversarial_certificate_stress.py --check
python -O -B papers/tpc-383-c1-pooled-normalization-audit/experiments/tpc383_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc383_c1_pooled_normalization_audit_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc383_c1_pooled_normalization_audit_checker.py --check
```

`ROUND2_CLUE = TEST_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM`.
