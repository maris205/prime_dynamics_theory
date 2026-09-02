# TPC-351 — Reciprocal-shell zero-sum contrast and finite scale repair

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-351 tests one predeclared reciprocal-shell contrast,
`gamma_j=1/p_j-(1/r)sum_k 1/p_k`, against the fixed balanced-step witness of
TPC-350 on the identical 192-row fresh panel.  The rational zero-sum rule and
the incidence Gram lower-witness identity remain exact.  All `192/192` rows
have positive response; `180/192` improve the parent response, `111/192`
reach half the defect norm, and `86/192` beat the coordinate baseline.  The
ratio range is `0.0917557319271--0.901734353382`, with the high-shell
`Q=256` block improving from `0/48` to `4/48` half-defect rows.  The minimum
is still below one quarter, so the universal quarter-floor remains
`REFUTED_SCOPED`.

This is a finite scale-repair audit, not an asymptotic theorem.  The claim
firewall leaves source-uniform arithmetic `L2`, a uniform masked-operator
bound, fixed-power credit, and the twin-prime endpoint open.

## Package

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project.
The canonical certificate is
`results/tpc351_certificate.json`; the compiled manuscript is
`paper/paper.pdf`.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-351-reciprocal-shell-contrast/code/tpc351_reciprocal_shell_contrast.py --write
python -B papers/tpc-351-reciprocal-shell-contrast/code/tpc351_reciprocal_shell_contrast.py --check
python -O -B papers/tpc-351-reciprocal-shell-contrast/code/tpc351_reciprocal_shell_contrast.py --check
python -B papers/tpc-351-reciprocal-shell-contrast/experiments/tpc351_independent_checker.py --check
python -O -B papers/tpc-351-reciprocal-shell-contrast/experiments/tpc351_independent_checker.py --check
python -B papers/tpc-351-reciprocal-shell-contrast/experiments/tpc351_contrast_stress.py
python -O -B papers/tpc-351-reciprocal-shell-contrast/experiments/tpc351_contrast_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc351_reciprocal_shell_contrast_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc351_reciprocal_shell_contrast_checker.py --check
```

The official Session-named evaluator files are absent, so the local Bridge-B
assessment is fail-closed and is not an official Route-A/Route-B pass.

## Claim readout

```text
TPC351_RECIPROCAL_ZERO_SUM_RULE = PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE
TPC351_SCALE_REPAIR_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
TPC351_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
TPC351_PARENT_IMPROVEMENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_180_OF_192
TPC351_RECIPROCAL_TO_DEFECT_RANGE = 0.0917557319271--0.901734353382
TPC351_COORDINATE_BASELINE_BEATEN = NUMERICALLY_CERTIFIED_FINITE_86_OF_192
TPC351_HALF_DEFECT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_111_OF_192
TPC351_NONDECREASING_GROWTH_SERIES = NUMERICALLY_CERTIFIED_FINITE_25_OF_48
TPC351_UNIFORM_QUARTER_FLOOR = REFUTED_SCOPED
TPC351_ARITHMETIC_ADVANCE = NO
TPC351_FIXED_POWER_CREDIT = 0
TPC351_FULL_GATE_B = OPEN
TPC351_TWIN_PRIME_RESULT = NONE
TPC351_ROUND2_CLUE = ADVERSARIAL_HOLDOUT_FOR_RECIPROCAL_CONTRAST_BEFORE_BRANCH_FREEZE
```
