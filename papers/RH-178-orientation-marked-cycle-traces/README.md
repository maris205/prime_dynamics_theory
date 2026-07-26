# RH-178: Orientation-Marked Cycle Traces

Forward and reverse cycles have identical determinants and ordinary power
traces.  RH-178 proves that the compressed rank-one edge marker separates
them by exactly one:

```text
Tr(J^o C_L^o)       = 1 - 1/L,
Tr(J^o (C_L^o)^-1)  =    - 1/L.
```

The paper also proves the marked-power perturbation bound
`|Tr J(A^m-B^m)| <= ||J||_1 m R^(m-1) ||A-B||`.

All 120 complex perturbation cases satisfy the bound.  Physical marker
identification and marked-trace convergence remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /root/math/.venv/bin/python experiments/run_orientation_mark_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf orientation-marked-cycle-traces.pdf
```
