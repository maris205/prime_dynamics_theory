# TPC-352 — Adversarial holdout for the reciprocal-shell contrast

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-352 evaluates the TPC-351 reciprocal-shell rule on a predeclared disjoint
holdout: origins `96097,120097,144097`, lengths `256,512,1024`, and shell
anchors `Q=64,128,256,512`.  The exact zero-sum incidence witness survives,
with positive response on `144/144` rows, but improves the balanced parent on
only `118/144` rows.  Its response/defect ratio is
`0.0801262572786--0.829632172143`, versus the parent range
`0.099642909832--0.806767399067`; the reciprocal witness reaches half-defect
on `49/144` rows and beats the coordinate baseline on `47/144`.  At `Q=256`
the reciprocal floor is worse than the parent, so the finite repair does not
transfer uniformly.

This is an adversarial finite transfer audit.  It proves no asymptotic lower
bound, source-uniform arithmetic `L2` estimate, fixed-power credit, or
twin-prime conclusion.  The natural finite reciprocal branch is therefore
marked for freeze while the source-native masked `L2` gate remains open.

## Package

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project.
The canonical certificate is `results/tpc352_certificate.json`; the compiled
manuscript is `paper/paper.pdf`.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-352-reciprocal-shell-adversarial-holdout/code/tpc352_reciprocal_shell_adversarial_holdout.py --write
python -B papers/tpc-352-reciprocal-shell-adversarial-holdout/code/tpc352_reciprocal_shell_adversarial_holdout.py --check
python -O -B papers/tpc-352-reciprocal-shell-adversarial-holdout/code/tpc352_reciprocal_shell_adversarial_holdout.py --check
python -B papers/tpc-352-reciprocal-shell-adversarial-holdout/experiments/tpc352_independent_checker.py --check
python -O -B papers/tpc-352-reciprocal-shell-adversarial-holdout/experiments/tpc352_independent_checker.py --check
python -B papers/tpc-352-reciprocal-shell-adversarial-holdout/experiments/tpc352_holdout_stress.py
python -O -B papers/tpc-352-reciprocal-shell-adversarial-holdout/experiments/tpc352_holdout_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc352_reciprocal_shell_adversarial_holdout_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc352_reciprocal_shell_adversarial_holdout_checker.py --check
```

The official Session-named evaluator files are absent.  The local Bridge-B
assessment is fail-closed and is not an official Route-A/Route-B pass.

## Claim readout

```text
TPC352_RECIPROCAL_RULE = PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE
TPC352_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
TPC352_DISJOINT_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
TPC352_RECIPROCAL_POSITIVE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_144_OF_144
TPC352_PARENT_IMPROVEMENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_118_OF_144
TPC352_RECIPROCAL_TO_DEFECT_RANGE = 0.0801262572786--0.829632172143
TPC352_UNIFORM_REPAIR_TRANSFER = REFUTED_SCOPED
TPC352_HIGH_SHELL_REPAIR = REFUTED_SCOPED
TPC352_ARITHMETIC_ADVANCE = NO
TPC352_FIXED_POWER_CREDIT = 0
TPC352_FULL_GATE_B = OPEN
TPC352_TWIN_PRIME_RESULT = NONE
TPC352_ROUND2_CLUE = FREEZE_FINITE_RECIPROCAL_BRANCH_AND_RETURN_TO_SOURCE_NATIVE_L2
```
