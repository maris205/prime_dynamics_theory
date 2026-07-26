# RH-173: Exact Normalized History Cocycle

RH-173 proves the exact rectangular update

```text
F_(t+1) = T_t F_t,
T_t(y_0,...,y_t) = (r_t A y_0, sqrt(eta)y_0, ..., sqrt(eta)y_t).
```

It also computes `T_t^* T_t`, all extreme singular values, and the exact
adjoint.  A two-column example proves that top-Gram reset optimality alone
does not imply packet invariance: the transported and reset ranges can be
orthogonal in one step.

The 160-case implementation audit has maximum formula residual below
`1.5e-15`.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /root/math/.venv/bin/python experiments/run_cocycle_identity_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf normalized-history-cocycle.pdf
```
