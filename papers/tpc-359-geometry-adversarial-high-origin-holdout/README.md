# TPC-359 — Geometry-adversarial high-origin holdout

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-359 pre-registered 51 high-origin candidates
`260001+211j` and selected `(267175,261267,269074)` using only the unsigned
pilot geometry spread.  The complete 288-row replay transferred the finite
TPC-358 caps: normalized Schur maximum `0.80834744529310265` and normalized
all-plus spectral maximum `0.6271657593674812`, while the raw all-plus spectral
maximum was `1542.7354827195263`.

## Scientific contribution

This is a hostile, response-blind finite holdout.  The selection score is
`max(G)/min(G)` for the unsigned mask-energy diagonal at count 256, maximized
over `Q=24,54,80` and kernel exponents `1,2`; a greedy separation of 1536 is
then applied.  No source response, sign law, or signed spectral value enters
the selection.  The selected panel is disjoint from the TPC-356 and TPC-358
origin panels.

The positive result is scoped cap transfer under this high-origin adversarial
rule.  The obstruction is equally important: the normalized all-plus scale
ladder has `12` increases, `36` decreases, and `6` flats among 54 adjacent
transitions.  Thus the finite cap does not become a monotone or growing
operator theorem.

## Claim firewall

```text
TPC359_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
TPC359_HIGH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC359_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC359_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC359_PARENT_CAP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC359_NORMALIZED_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC359_SPECTRAL_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
TPC359_GROWING_OPERATOR_BOUND = OPEN
TPC359_SOURCE_UNIFORM_L2 = OPEN
TPC359_ARITHMETIC_ADVANCE = NO
TPC359_FIXED_POWER_CREDIT = 0
TPC359_FULL_GATE_B = OPEN
TPC359_TWIN_PRIME_RESULT = NONE
```

The Session-named official Route-A/Route-B evaluator files are absent from
this checkout.  The local Bridge-B checker is fail-closed reproducibility
evidence only; it is not an official evaluator pass.

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-359-geometry-adversarial-high-origin-holdout/code/tpc359_geometry_adversarial_high_origin_holdout.py --write
python -B papers/tpc-359-geometry-adversarial-high-origin-holdout/code/tpc359_geometry_adversarial_high_origin_holdout.py --check
python -O -B papers/tpc-359-geometry-adversarial-high-origin-holdout/code/tpc359_geometry_adversarial_high_origin_holdout.py --check
python -B papers/tpc-359-geometry-adversarial-high-origin-holdout/experiments/tpc359_independent_checker.py --check
python -O -B papers/tpc-359-geometry-adversarial-high-origin-holdout/experiments/tpc359_independent_checker.py --check
python -B papers/tpc-359-geometry-adversarial-high-origin-holdout/experiments/tpc359_adversarial_certificate_stress.py --check
python -O -B papers/tpc-359-geometry-adversarial-high-origin-holdout/experiments/tpc359_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc359_geometry_adversarial_high_origin_holdout_checker.py --check
```

The canonical certificate is `results/tpc359_certificate.json`; the manuscript
is `paper/paper.pdf`.  The proof package and route decision are in
`notes/route_evaluation.md` and `research/tpc-big-road/bridge_b_tpc359_geometry_adversarial_high_origin_holdout.md`.

## Round-2 clue

`TEST_SCHUR_TIGHTNESS_AND_INDEPENDENT_HIGH_ORIGIN_REPLICATION`.
