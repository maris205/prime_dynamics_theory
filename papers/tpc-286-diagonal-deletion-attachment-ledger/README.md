# TPC-286 — A diagonal-deletion attachment ledger for the literal prime-shell operator

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

For the literal finite source model, the attachment of the physical
diagonal-deleted operator is exactly the attachment of the diagonal-including
operator minus an explicit diagonal correction.  On all 72 TPC-284 schedule
controls, the three components are sign-separated; the full-versus-physical
sign changes in 15 rows, the diagonal correction opposes the physical term in
30 rows, and its certified absolute magnitude is strictly larger in 21 rows.

## What advances

- states and proves the exact linear decomposition needed after the
  TPC-285 rank obstruction;
- gives the diagonal output in closed form,
  `Delta_diag(u) = sum_q q K_H(0)(q-2)/(q-1) m_q(u) beta(u)`;
- replays the complete six-control, six-baseline, two-exponent atlas rather
  than selecting only the earlier sign-flip rows;
- separates a structural identity from a finite sensitivity ledger, with
  outward interval arithmetic and an independent checker;
- identifies a concrete next question: whether the diagonal-corrected,
  signed full-shell sum admits cancellation that survives the physical
  convention.

## Claim ceiling

```text
PROVED_EXACT = A_phys = A_full - Delta_diag and C_phys = C_full - C_diag
NUMERICALLY_CERTIFIED_FINITE = 72-row component/sign/sensitivity ledger
NUMERICALLY_CERTIFIED_FINITE = 15 full-versus-physical sign flips
NUMERICALLY_CERTIFIED_FINITE = 21 strict diagonal-dominance rows
OPEN = asymptotic diagonal dominance
OPEN = signed full-shell cancellation or literal arithmetic L2
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The finite counts are not asymptotic evidence.  In particular, a diagonal
term that dominates a registered row does not imply uniform dominance as the
source scale grows.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc286_diagonal_deletion_attachment_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc286_diagonal_deletion_attachment_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc286_diagonal_deletion_attachment_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc286_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc286_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc286_diagonal_sensitivity_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The certificate locks
the TPC-284 control atlas, the TPC-285 rank release, and the frozen TPC-268
finite operator.  The Session evaluator files named in the wider workflow are
not present in this checkout; `notes/route_evaluation.md` records the
fail-closed local Route-B fallback.
