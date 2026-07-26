# RH-172: Canonical Polar Reset-Memory Realization

RH-172 proves that the recursive reset memory has an exact normalized-history
Gram factorization `M_t = F_t^* F_t`.  Every positive reset packet therefore
has a canonical polar isometry into finite history space.

The result closes `X_mem->hist`, not `X_phys`: no map from history space to
the RH-80 transfer/determinant space is constructed.

The 192-case complex audit checks Gram factorization, polar isometry, source
gauge covariance, and packet-frame equivariance with maximum residual below
`5.5e-15`.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /root/math/.venv/bin/python experiments/run_polar_identity_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf canonical-polar-reset-memory-realization.pdf
```
