# RH-176: Finite Cyclic History Closure

For the length-`L` cycle `C_L`, RH-176 proves

```text
det(I-q C_L) = 1-q^L,
det(I-q C_L | 1^perp) = (1-q^L)/(1-q) = Pi_(L-1)(q).
```

The cycle differs from the nilpotent finite shift by one wrap edge of norm
one.  Natural cyclic extensions converge strongly to the unilateral shift on
fixed vectors, but never in operator norm.  The remote wrap carries the
entire nontrivial determinant.

The 240-case complex audit has maximum determinant error `7.99e-15`.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /root/math/.venv/bin/python experiments/run_cyclic_closure_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf finite-cyclic-history-closure.pdf
```
