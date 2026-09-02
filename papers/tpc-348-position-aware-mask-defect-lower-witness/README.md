# TPC-348 — Position-aware lower witnesses for the divisibility-mask defect

**Author:** Liang Wang

**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-348 keeps the literal masked prime-shell object from TPC-347 and proves an
exact coordinate lower-witness inequality.  If `J_I` is the set of interval
positions divisible by at least one active shell prime, then

```text
||D_I||_(2->2) >= W_I(D) := max_(t in J_I) ||D_I e_t||_2.
```

The position-aware formula for `D_I e_t` retains both the left and right mask
defects.  On the locked two-origin, three-count, four-anchor, two-exponent,
four-law panel, all `192/192` rows have a positive mask-hit witness.  The best
hit-column witness is between `0.453958762219` and `0.897148966365` of the
defect spectral norm, and between `0.0183057714619` and `0.336311065586` of
the unmasked ideal norm.

This is a finite, auditable obstruction to silently deleting the masks.  The
ratios are not growing lower bounds, and the release supplies no arithmetic
`L2` estimate or twin-prime conclusion.

## What is new

* An exact mask-hit coordinate selector and induced-norm lower-witness theorem.
* An exact position-aware split of a defect column according to `p divides t`
  or `p does not divide t`.
* A 192-row finite audit with first-hit and best-hit controls, including a
  `2.0872192863e-14` maximum floating replay discrepancy for the formula.
* An exact rational six-point anchor whose unique mask-hit position is `5`.
* An independent reverse-shell replay and hostile mutation stress suite.

## Claim firewall

```text
PROVED_EXACT_FINITE_LINEAR_ALGEBRA = coordinate lower-witness inequality
PROVED_EXACT_FINITE_DECLARED_MODEL = mask-hit selector and two-sided position formula
NUMERICALLY_CERTIFIED_FINITE = 192 positive witnesses and formula checks
REFUTED_SCOPED = mask-discard shortcut on the declared finite panel
OPEN = source-uniform arithmetic L2; uniform masked operator bound; canonical
       sign law; fixed-power payment; full Route-B Gate B; twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The coordinate functional is declared before the audit and does not use a
leading eigenvector.  The finite ratios remain observations on the stated
panel only.  The Session-named `propose.md` and Route-A/Route-B evaluator files
are absent from this checkout; `notes/route_evaluation.md` records the local
fail-closed assessment.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-348-position-aware-mask-defect-lower-witness/code/tpc348_position_aware_mask_defect_lower_witness.py --write
python -B papers/tpc-348-position-aware-mask-defect-lower-witness/code/tpc348_position_aware_mask_defect_lower_witness.py --check
python -O -B papers/tpc-348-position-aware-mask-defect-lower-witness/code/tpc348_position_aware_mask_defect_lower_witness.py --check
python -B papers/tpc-348-position-aware-mask-defect-lower-witness/experiments/tpc348_independent_checker.py --check
python -O -B papers/tpc-348-position-aware-mask-defect-lower-witness/experiments/tpc348_independent_checker.py --check
python -B papers/tpc-348-position-aware-mask-defect-lower-witness/experiments/tpc348_witness_stress.py
python -O -B papers/tpc-348-position-aware-mask-defect-lower-witness/experiments/tpc348_witness_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc348_position_aware_mask_defect_lower_witness_checker.py --check
```

The canonical result is
[results/tpc348_certificate.json](results/tpc348_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project
package.  The next route question is whether prime-balanced signed defect
witnesses reveal any structure beyond this coordinate lower bound, before a
source-native arithmetic `L2` attempt.
