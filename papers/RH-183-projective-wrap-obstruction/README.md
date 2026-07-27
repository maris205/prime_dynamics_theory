# RH-183: Projective Wrap Obstruction

RH-183 proves the exact best phase and best scalar endpoint-to-seed wrap
formulas. The arbitrary-scalar residual is the physical edge amplitude times
the projective return distance.

The 80-case formula audit has zero failures. Replaying RH-182, 43 orientation
marks improve the chord, but none of 126 projective returns is at most `0.25`.
Phase or amplitude repair therefore cannot rescue the declared orthogonal
temporal spans.

This is a finite span obstruction, not an all-level no-go theorem and not a
rejection of biorthogonal packets.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_wrap_obstruction_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf projective-wrap-obstruction.pdf
```
