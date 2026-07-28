# RH-223: Shell-Complete Edge Selection Stability

A fixed-cardinality modulus prefix can split a conjugate pair even when its
target rank is even. This happens at 23 of the 32 RH-222 endpoints.

The shell-complete rule is the minimal radial prefix containing whole real
singletons and nonreal conjugate pairs. It overshoots the target by at most one
root. Every endpoint has positive resolved radial gap, and candidate prefixes
with margins 4, 8, 12, and 14 recover the same selected multiset with zero
matching error.

The result proves canonicity only inside the resolved Arnoldi window. It does
not certify the ordering of the infinite operator spectrum or canonize the
rank schedule.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_shell_stability_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf shell-complete-edge-selection-stability.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
