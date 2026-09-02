# Bridge-B: TPC-356 geometry-adversarial normalization holdout

```text
BRIDGE_B_TPC356 = LOCAL_FAIL_CLOSED_FINITE_AUDIT
TPC356_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT
TPC356_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_DETERMINISTIC
TPC356_SELECTION_RESPONSE_INDEPENDENCE = PROVED_EXACT_FINITE
TPC356_PANEL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
TPC356_RAW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
TPC356_NORMALIZED_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
TPC356_ALL_PLUS_MIN_GAIN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC356_ALL_PLUS_MEAN_GAIN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC356_UNIFORM_TRANSFER = OPEN
TPC356_SOURCE_UNIFORM_L2 = OPEN
TPC356_MASKED_OPERATOR_BOUND = OPEN
TPC356_ARITHMETIC_ADVANCE = NO
TPC356_FIXED_POWER_CREDIT = 0
TPC356_FULL_GATE_B = OPEN
TPC356_TWIN_PRIME_RESULT = NONE
TPC356_ROUTE_A_OFFICIAL_EVALUATOR = ABSENT_FAIL_CLOSED
TPC356_ROUTE_B_OFFICIAL_EVALUATOR = ABSENT_FAIL_CLOSED
```

## Mathematical progress

The TPC-355 unsigned mask-energy congruence is held fixed.  A finite scan of
51 late origins ranks by the maximum pilot `max(G)/min(G)` over six geometry
settings; the declared greedy separation rule selects `(38423,42010,45597)`.
This selection reads neither the V59 source response nor a sign law.  On the
three selected origins, counts `(256,512,1024)`, anchors `(24,54,80)`,
exponents `(1,2)`, and four sign laws produce 216 rows.  Raw and normalized
alignment are each `216/216` positive.  The all-plus minimum gain is
`0.019062676850676086`; the mean gain is `0.0068817732644231855`.

The strongest obstruction is that this finite geometry-adversarial result
does not control the score or normalized operator for growing origins.  It
therefore pays no arithmetic or fixed-power credit and leaves full Gate B
open.

## Reproducibility commands

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-356-geometry-adversarial-normalization-holdout/code/tpc356_geometry_adversarial_normalization_holdout.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-356-geometry-adversarial-normalization-holdout/experiments/tpc356_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-356-geometry-adversarial-normalization-holdout/experiments/tpc356_adversarial_selection_stress.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-356-geometry-adversarial-normalization-holdout/code/tpc356_geometry_adversarial_normalization_holdout.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-356-geometry-adversarial-normalization-holdout/experiments/tpc356_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-356-geometry-adversarial-normalization-holdout/experiments/tpc356_adversarial_selection_stress.py --check
```

The local Bridge-B checker reruns these six commands, verifies canonical
certificate and PDF/provenance hashes, and requires byte-identical normal and
optimized stdout.  The official Session evaluator files are absent, so no
official Route-A or Route-B pass is asserted.
