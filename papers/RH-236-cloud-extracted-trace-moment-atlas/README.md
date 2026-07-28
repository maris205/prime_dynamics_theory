# RH-236: Cloud-extracted trace-moment atlas

This paper computes exact sparse-matrix traces through order twelve for all
32 RH-222 endpoints and subtracts the Perron mode, parity mode, and selected
shell-complete cloud.

The resulting 384 finite trace cases are small compared with the divergent
Frobenius budget.  On the closed unit-disk logarithmic jet, the largest norm
over all endpoints is `0.07592`; over the fine range `sigma<=0.005` it is
`0.01067`.  The largest observed Cauchy root rate over orders 2--12 is
`0.35989`.

These are finite-order data.  They do not bound order thirteen or the
infinite tail.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_trace_moment_atlas.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf cloud-extracted-trace-moment-atlas.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
