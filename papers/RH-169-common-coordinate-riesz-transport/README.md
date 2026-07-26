# RH-169: Common-Coordinate Riesz Transport

RH-169 moves from one certified scale to a fixed-rank all-scale chain.  After
embedding consecutive operators into one Hilbert space, if

```text
||A_{j+1}-A_j|| <= eta_j,
sup_Gamma ||(z-A_j)^(-1)|| <= M_j,
```

then their Riesz projections satisfy

```text
||Pi_{j+1}-Pi_j|| <= |Gamma| M_j M_{j+1} eta_j /(2 pi).
```

A bound below one yields a stable range transport.  Summability of the step
bounds makes the projections norm-Cauchy and preserves their finite rank in
the limit.

This theorem makes common coordinates and summability explicit.  It applies
only to a fixed-rank cloud.  The moving determinant cloud has growing rank,
so RH-170 must replace global norm convergence by a shellwise construction.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_transport_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf common-coordinate-riesz-transport.pdf
```
