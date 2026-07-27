# RH-182: Finite Temporal Clock Physical Audit

RH-182 constructs a target-independent weighted cycle from normalized source
orbits and tests the predeclared lengths `L=r-3` and `L=r-4`.

Main results:

- the open temporal chain intertwines exactly and all error is one rank-one
  wrap column;
- the weighted cycle has an exact rotated root grid and a telescoping radius;
- 126 physical windows give zero formula failures;
- minimum projective/primal/adjoint defects are `0.3720`, `0.2711`, and
  `0.7143`;
- no window passes the common `0.25` three-way gate.

This rejects the simplest orthogonal physical clock on the audited anchors,
not every finite-cycle or biorthogonal realization.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /root/math/.venv/bin/python experiments/run_temporal_clock_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf finite-temporal-clock-physical-audit.pdf
```
