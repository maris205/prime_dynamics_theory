# TPC-364 — Prime-shell tilt phase diagram

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

On the frozen TPC-361 high-origin panel, a complete five-beta, four-law
replay has 960 rows.  The explicit shell tilt
`w_(p,beta)=(p/Q)^beta` with its matching weighted geometry has spectral-cap
violations `63,36,30,30,0` for `beta=-2,-1,0,1,2`, respectively.  Thus
`beta=2` is the unique member of the declared finite menu with zero failures,
with maximum normalized spectrum `0.61628753962786131` and minimum effective
shell fraction `0.66938300094026681`.

## Scientific contribution

TPC-362 located the first shell-scale failure of the inherited normalized cap,
and TPC-363 showed that five-percent row and eigenvector restrictions do not
remove it.  TPC-364 tests a different, explicitly declared modeling choice:
each prime block is tilted by `(p/Q)^beta`, and the diagonal normalizer is
rebuilt from the squares of those same weighted blocks.  The full Cartesian
product uses the TPC-361 origins `(313030,311166,321651)`, counts `256,512`,
shell anchors `Q=80,128,256,512`, exponents `1,2`, four fixed sign laws, and
the symmetric integer menu `{-2,-1,0,1,2}`.

The positive result is a finite phase point: beta=2 removes all 192 spectral
cap failures on this panel, while the other menu values do not.  The
effective shell count remains at least 66.9% of the literal shell size in the
same finite audit, so the observation is not described as a one-prime
truncation.  The result is still a modeling choice on a reused panel; it is
not a source-valid or asymptotic repair.

## Claim firewall

```text
TPC364_WEIGHTED_BLOCK_DEFINITION = PROVED_EXACT_FINITE
TPC364_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC364_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_960_ROWS
TPC364_PHASE_DIAGRAM = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC364_BETA2_PANEL_CAP_REPAIR = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC364_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC364_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC364_GROWING_OPERATOR_BOUND = OPEN
TPC364_SOURCE_UNIFORM_L2 = OPEN
TPC364_ARITHMETIC_ADVANCE = NO
TPC364_FIXED_POWER_CREDIT = 0
TPC364_FULL_GATE_B = OPEN
TPC364_TWIN_PRIME_RESULT = NONE
```

The Session-named official Route-A/Route-B evaluator files are absent from
this checkout.  The local Bridge-B checker is fail-closed finite evidence
only, not an official evaluator pass.

## Package

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable package.
The canonical certificate is
`results/tpc364_certificate.json`; the compiled manuscript is
`paper/paper.pdf`.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-364-shell-tilt-phase-diagram/code/tpc364_shell_tilt_phase_diagram.py --write
python -B papers/tpc-364-shell-tilt-phase-diagram/code/tpc364_shell_tilt_phase_diagram.py --check
python -O -B papers/tpc-364-shell-tilt-phase-diagram/code/tpc364_shell_tilt_phase_diagram.py --check
python -B papers/tpc-364-shell-tilt-phase-diagram/experiments/tpc364_independent_checker.py --check
python -O -B papers/tpc-364-shell-tilt-phase-diagram/experiments/tpc364_independent_checker.py --check
python -B papers/tpc-364-shell-tilt-phase-diagram/experiments/tpc364_adversarial_certificate_stress.py --check
python -O -B papers/tpc-364-shell-tilt-phase-diagram/experiments/tpc364_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc364_shell_tilt_phase_diagram_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc364_shell_tilt_phase_diagram_checker.py --check
```

## Round-2 clue

`TEST_BETA2_ON_RESPONSE_BLIND_FRESH_HOLDOUT`.
