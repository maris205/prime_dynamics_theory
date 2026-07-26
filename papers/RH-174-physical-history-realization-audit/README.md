# RH-174: Physical History-Realization Audit

RH-174 evaluates the exact RH-172/RH-173 history construction on all 130
RH-151 reset snapshots and 120 consecutive updates.

Main findings:

- Gram and cocycle identities remain at machine precision.
- Stable SVD polar packets are isometric in 130/130 cases.
- The direct inverse-square-root formula loses up to `1.57e-5` in isometry
  defect because the selected condition number reaches `3.61e12`.
- 95/120 primal residuals are at most `0.10`.
- 0/120 adjoint residuals are at most `0.25`; the minimum is `0.3233`.
- No update passes the symmetric `0.25` two-sided gate.

This is a floating finite-data negative result for the simplest consecutive
reset bundle, not an all-level no-go theorem.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /root/math/.venv/bin/python experiments/run_physical_history_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf physical-history-realization-audit.pdf
```
