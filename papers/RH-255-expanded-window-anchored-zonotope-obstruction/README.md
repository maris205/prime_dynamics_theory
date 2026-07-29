# RH-255: Expanded-Window Anchored Zonotope Obstruction

The RH-254 expanded windows are tested directly against the RH-243
deterministic anchor.  Only conjugate-complete shells are used.  The convex
single-use box `0 <= w_j <= 1`, which contains every prefix and every binary
shell subset, has zero passes at all 32 endpoints.

The box distance range is `0.1435849351--0.4239980037`, at least `10.17` times
the local tolerance.  The duality gap is at most `5.83e-15`.  The expanded
windows improve every endpoint relative to RH-248, but still exclude
62,030,604,700 eligible binary subsets in aggregate.

This is a scoped obstruction for the margin-32 single-use shell class.  It
does not exclude signed/complex invariant selectors, larger windows,
unbounded reweighting, or other operator realizations.

Gates A--E remain false/open.  No Hilbert--Polya operator, zeta-divisor
equality, Riemann-zero identification, or RH implication is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_expanded_reachability_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf expanded-window-anchored-zonotope-obstruction.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
