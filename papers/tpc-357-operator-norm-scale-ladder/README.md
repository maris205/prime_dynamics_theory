# TPC-357 — Operator-norm scale ladder

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-357 extends the TPC-356 frozen geometry-adversarial origins to four
interval lengths and certifies finite operator envelopes on 288 rows.  The
normalized all-plus Schur maximum is `0.8077815961017315`, the all-plus true
spectral maximum is `0.62665294142584216`, and the raw all-plus spectral
maximum is `1542.7455490253569`.  The normalized spectral ladder is not
monotone: among 54 adjacent count transitions it has 15 increases, 35
decreases, and 4 flats under guard `10^-6`.

## What is new

The experiment separates an exact finite norm envelope from a numerical
spectral readout.  All four sign laws receive Schur and Frobenius bounds at
counts `256,512,1024,2048`, while all-plus receives a symmetric
`eigvalsh` replay at every row.  The origins `(38423,42010,45597)` and all
geometry definitions are inherited and hash-locked from TPC-356; no source
response is used.

The strongest positive result is a finite normalized Schur cap below `0.83`
and an all-plus spectral cap below `0.64` on the declared panel.  The
strongest obstruction is that the normalized spectral values do not decay
monotonically with interval length; for example, at origin `42010`, `Q=80`,
exponent `2`, they are
`0.6263543507, 0.6032097319, 0.6033370730, 0.6036446871`.

## Certified status

```text
TPC357_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC357_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC357_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC357_NORMALIZED_SCHUR_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC357_ALL_PLUS_SPECTRAL_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC357_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
TPC357_GROWING_OPERATOR_BOUND = OPEN
TPC357_SOURCE_UNIFORM_L2 = OPEN
TPC357_ARITHMETIC_ADVANCE = NO
TPC357_FIXED_POWER_CREDIT = 0
TPC357_FULL_GATE_B = OPEN
TPC357_TWIN_PRIME_RESULT = NONE
```

The Session-named official Route-A/Route-B evaluator files are absent from
this checkout.  The local Bridge-B checker is fail-closed reproducibility
evidence, not an official evaluator pass.

## Reproduce

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-357-operator-norm-scale-ladder/code/tpc357_operator_norm_scale_ladder.py --write
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-357-operator-norm-scale-ladder/code/tpc357_operator_norm_scale_ladder.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-357-operator-norm-scale-ladder/experiments/tpc357_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-357-operator-norm-scale-ladder/experiments/tpc357_adversarial_certificate_stress.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-357-operator-norm-scale-ladder/code/tpc357_operator_norm_scale_ladder.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-357-operator-norm-scale-ladder/experiments/tpc357_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B papers/tpc-357-operator-norm-scale-ladder/experiments/tpc357_adversarial_certificate_stress.py --check
```

The release certificate is `results/tpc357_certificate.json`, and the
compiled manuscript is `paper/paper.pdf`.

## Next clue

The next minimal test is a fresh, pre-registered origin-scale holdout aimed at
the normalized spectral cap and the observed nonmonotonic transitions.  It
must remain operator-only until a uniform bound is actually proved.
