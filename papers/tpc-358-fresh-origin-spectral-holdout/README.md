# TPC-358 — Fresh-origin spectral holdout

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-358 transfers the TPC-357 finite operator audit to fresh origins
`52001,120001,220001`, spanning `168000` in origin.  On 288 rows the
normalized Schur maximum is `0.80850510742101689` and the all-plus normalized
spectral maximum is `0.62663944469203836`, both inside the parent thresholds
`0.83` and `0.64`; the raw all-plus spectral maximum is
`1542.7492651981368`.  The normalized spectral ladder still has 13 increases,
34 decreases, and 7 flats among 54 adjacent transitions.

## What is new

The origins are fixed by the arithmetic rule `52001+100000j` before any
operator is evaluated and are disjoint from the TPC-356 panel.  All four sign
laws receive Schur/Frobenius envelopes at counts `256,512,1024,2048`, and the
all-plus law receives a true eigenvalue replay.  The parent-cap comparison is
therefore a fresh finite transfer test rather than a re-selection or a fitted
response experiment.

The strongest positive result is finite cap transfer across the declared
origin span: the fresh maxima remain within `0.001` of TPC-357's normalized
maxima.  The strongest obstruction is unchanged in kind: normalized spectral
values do not decay monotonically, and finite transfer supplies no uniform
origin theorem.

## Certified status

```text
TPC358_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC358_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC358_FRESH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC358_PARENT_CAP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC358_NORMALIZED_SCHUR_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC358_ALL_PLUS_SPECTRAL_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC358_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
TPC358_GROWING_OPERATOR_BOUND = OPEN
TPC358_SOURCE_UNIFORM_L2 = OPEN
TPC358_ARITHMETIC_ADVANCE = NO
TPC358_FIXED_POWER_CREDIT = 0
TPC358_FULL_GATE_B = OPEN
TPC358_TWIN_PRIME_RESULT = NONE
```

The Session-named official evaluator files are absent.  The local Bridge-B
checker is fail-closed reproducibility evidence and is not an official
Route-A/Route-B pass.

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-358-fresh-origin-spectral-holdout/code/tpc358_fresh_origin_spectral_holdout.py --write
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-358-fresh-origin-spectral-holdout/code/tpc358_fresh_origin_spectral_holdout.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-358-fresh-origin-spectral-holdout/experiments/tpc358_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-358-fresh-origin-spectral-holdout/experiments/tpc358_adversarial_certificate_stress.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-358-fresh-origin-spectral-holdout/code/tpc358_fresh_origin_spectral_holdout.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-358-fresh-origin-spectral-holdout/experiments/tpc358_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-358-fresh-origin-spectral-holdout/experiments/tpc358_adversarial_certificate_stress.py --check
```

The release certificate is `results/tpc358_certificate.json`; the compiled
manuscript is `paper/paper.pdf`.

## Next clue

The next minimal hostile test is a geometry-adversarial fresh-origin panel or
a Schur-tightness audit, still without source or arithmetic reassembly.
