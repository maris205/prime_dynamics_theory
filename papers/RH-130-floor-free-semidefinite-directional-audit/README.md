# RH-130: Floor-Free Semidefinite Directional Transport

This paper removes the positive Gram/tail floors used in RH-121 and RH-125.
It proves the semidefinite exact-Gram minimax theorem, identifies tail-rank
creation as an infinite-factor obstruction, and rebuilds the five-scale
audit through one common assembly.

Main finite result: all 120 local recent actions retain four supported
directions and 118 local candidates are positive, but only 67/96 adjacent
transfers are positive and 0/24 complete chains survive.  Twenty-four edges
have infinite multiplicative factor because the target tail creates rank.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_floor_free_audit.py --smoke
/root/math/.venv/bin/python experiments/build_floor_free_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf floor-free-semidefinite-directional-audit.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```

The result redirects the route toward an affine tail recurrence with an
explicit additive forcing term.  It makes no all-level, Hilbert--Polya,
zeta-zero, or Riemann Hypothesis claim.
