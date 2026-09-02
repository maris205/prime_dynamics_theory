# TPC-356 — Geometry-adversarial normalization holdout

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-356 freezes the TPC-355 response-independent normalization, selects three
origins solely by an unsigned geometry-spread score, and certifies a
216-row holdout.  Raw and normalized alignment are both positive in all
216 rows; on this deliberately selected panel the all-plus minimum rises from
`0.63140161782616067` to `0.65046429467683675` and the mean rises from
`0.8687258535297816` to `0.87560762679420479`.

## What is new

The finite selection protocol scans 51 candidate origins and chooses
`(38423,42010,45597)` by descending pilot `max(G)/min(G)`, with separation at
least 1536.  The source response and sign law are not consulted during this
selection.  This is an adversarial transfer test of the TPC-355 geometry
preconditioner, not a fitted response experiment.

## Certified status

```text
TPC356_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_DETERMINISTIC
TPC356_SELECTION_RESPONSE_INDEPENDENCE = PROVED_EXACT_FINITE
TPC356_PANEL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
TPC356_ALL_PLUS_MIN_GAIN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC356_ALL_PLUS_MEAN_GAIN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC356_UNIFORM_TRANSFER = OPEN
TPC356_SOURCE_UNIFORM_L2 = OPEN
TPC356_MASKED_OPERATOR_BOUND = OPEN
TPC356_ARITHMETIC_ADVANCE = NO
TPC356_FIXED_POWER_CREDIT = 0
TPC356_FULL_GATE_B = OPEN
TPC356_TWIN_PRIME_RESULT = NONE
```

The official Session-named Route A/Route B evaluator files are not present in
this checkout.  The local Bridge-B checker is therefore fail-closed fallback
evidence and is not an official evaluator pass.

## Reproduce

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-356-geometry-adversarial-normalization-holdout/code/tpc356_geometry_adversarial_normalization_holdout.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-356-geometry-adversarial-normalization-holdout/experiments/tpc356_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-356-geometry-adversarial-normalization-holdout/experiments/tpc356_adversarial_selection_stress.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-356-geometry-adversarial-normalization-holdout/code/tpc356_geometry_adversarial_normalization_holdout.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-356-geometry-adversarial-normalization-holdout/experiments/tpc356_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-356-geometry-adversarial-normalization-holdout/experiments/tpc356_adversarial_selection_stress.py --check
```

The release certificate is `results/tpc356_certificate.json`, and the
compiled manuscript is `paper/paper.pdf`.

## Next clue

The next useful test is origin-scale stability or an operator-norm certificate
that is fixed before any arithmetic reassembly.  The current finite gains
must not be extrapolated without that test.
