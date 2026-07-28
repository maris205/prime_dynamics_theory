# RH-249: Unbounded Shell-Multiplicity Pathology

RH-248 allowed each frozen conjugate shell at most once.  This paper removes
the upper bound and solves the nonnegative cone problem `w_j>=0`.

The cone has an exact LP dual.  Six of 32 endpoints remain outside the
anchored tolerance even with arbitrarily large nonnegative weights.  The
other 26 become reachable, but only through multiplicity explosion: the
minimum possible cap on the largest shell weight ranges from
`40.58443731031147` to `58018432630.629776`.  Imposing `w_j<=40` leaves
0/32 passes; `w_j<=41` produces only the first single pass.

Arbitrary real shell weights do not represent the fixed algebraic
multiplicities of a spectral cloud.  Thus the 26 formal LP successes are a
moment-reweighting pathology, not a coefficient-anchor construction.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_cone_reachability_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf unbounded-shell-multiplicity-pathology.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
