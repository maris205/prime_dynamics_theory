# TPC-362 — Shell-scale cap obstruction

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

Keeping the TPC-361 origins fixed and widening the shell ladder to
`Q=12,24,36,54,80,128,256,512`, the four-law replay has 384 rows.  The old
finite caps hold through `Q=80`, but fail first at `Q=128`; the global
normalized Schur and spectral maxima are `1.7172665118910415` and
`1.6398895499394266`.

## Scientific contribution

TPC-361 showed that a geometry-selected high-origin panel reproduces the
finite cap at the original shell anchors.  TPC-362 isolates the next missing
quantifier: shell-scale uniformity.  It freezes origins
`(313030,311166,321651)` and tests every combination of counts `256,512`,
eight shell anchors, exponents `1,2`, and four fixed sign laws.  All 384 rows
record normalized Schur, Frobenius, and true spectral values.

At the inherited low-shell anchors `Q=12,24,36,54,80`, the largest normalized
Schur and spectral values are `0.80830232610282304` and
`0.62690716242733457`, both below the working caps `0.83` and `0.64`.  At
`Q=128` the first violations occur: six spectral rows and nine Schur rows
cross their respective caps.  Across the full ladder there are 30 spectral
and 33 Schur cap-violating rows.  The setting-wise law winner census is
all-plus `78`, alternating-index `4`, mod-4 `14`, half-split `0` out of 96.

The strongest obstruction is therefore a shell-scale failure, not an origin
selection failure.  Across the 336 adjacent Q transitions, 200 increase and
136 decrease, with no flat transitions under the declared guard.  This is a
finite, scoped obstruction to extending the `Q<=80` cap to a shell-uniform
statement.

## Claim firewall

```text
TPC362_SHELL_SCALE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_384_ROWS
TPC362_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC362_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC362_LOW_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC362_HIGH_Q_CAP_EXTENSION = REFUTED_SCOPED_ON_DECLARED_Q_LADDER
TPC362_LAW_WINNER_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC362_GROWING_OPERATOR_BOUND = OPEN
TPC362_SOURCE_UNIFORM_L2 = OPEN
TPC362_ARITHMETIC_ADVANCE = NO
TPC362_FIXED_POWER_CREDIT = 0
TPC362_FULL_GATE_B = OPEN
TPC362_TWIN_PRIME_RESULT = NONE
```

The Session-named official Route-A/Route-B evaluator files are absent from
this checkout.  The local Bridge-B checker is fail-closed finite evidence,
not an official evaluator pass.  No source response, arithmetic reassembly,
or fixed-power credit is used.

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-362-shell-scale-cap-obstruction/code/tpc362_shell_scale_cap_obstruction.py --write
python -B papers/tpc-362-shell-scale-cap-obstruction/code/tpc362_shell_scale_cap_obstruction.py --check
python -O -B papers/tpc-362-shell-scale-cap-obstruction/code/tpc362_shell_scale_cap_obstruction.py --check
python -B papers/tpc-362-shell-scale-cap-obstruction/experiments/tpc362_independent_checker.py --check
python -O -B papers/tpc-362-shell-scale-cap-obstruction/experiments/tpc362_independent_checker.py --check
python -B papers/tpc-362-shell-scale-cap-obstruction/experiments/tpc362_adversarial_certificate_stress.py --check
python -O -B papers/tpc-362-shell-scale-cap-obstruction/experiments/tpc362_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc362_shell_scale_cap_obstruction_checker.py --check
```

The canonical certificate is `results/tpc362_certificate.json`; the compiled
manuscript is `paper/paper.pdf`.  The frozen protocol and route decision are
in `experiments/protocol.md` and `notes/route_evaluation.md`.

## Round-2 clue

`LOCALIZE_HIGH_Q_OBSTRUCTION_BY_LAW_AND_ROW_GEOMETRY`.
