# RH-177: Double-Cycle Geometric Cloud

For `L=N+1`, let `C_L^o` be the cycle restricted to the zero-mean space.
RH-177 proves that

```text
K_N = lambda^(-1) (C_L^o direct-sum C_L^o)
det(I-w K_N) = Pi_N(w/lambda)^2.
```

This is exactly the RH-80 canonical moving cloud factor.  The paper also
gives the complete power-trace ledger and the geometric scattering limit.

The 192 determinant cases and 104 trace cases validate the implementation.
Actual noisy-cloud identification and physical Riesz projection remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /root/math/.venv/bin/python experiments/run_double_cycle_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf double-cycle-geometric-cloud.pdf
```
