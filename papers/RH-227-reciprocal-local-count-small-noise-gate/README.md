# RH-227: Reciprocal Local-Count Small-Noise Gate

Local uniform convergence of holomorphic functions to a nonzero limit forces
zero counts to stabilize on every contour avoiding the limiting divisor. This
Rouche/Hurwitz consequence gives a necessary small-noise determinant gate.

Reciprocal cloud counts are audited on radii `1.2,1.5,2,3,5`. Every finite
contour has positive clearance, but none of the five left-channel counts and
only one right-channel count are constant over the last four scales. The
largest first-to-last count growth is 18.

This fails a finite diagnostic. It does not prove that counts cannot stabilize
at smaller noise, nor does it disprove a renormalized relative determinant.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_local_count_gate.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf reciprocal-local-count-small-noise-gate.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
