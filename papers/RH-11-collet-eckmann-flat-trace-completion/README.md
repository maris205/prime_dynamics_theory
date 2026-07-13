# Collet--Eckmann flat-trace completion

This directory contains the eleventh-layer theory paper in the quadratic
prime-dynamics program:

> *Unconditional Parity-Centered Flat Traces at a Quadratic Band-Merging Map:
> Collet--Eckmann Weighted Zeta Continuation and Completion of the Small-Noise
> Double Limit*

The paper removes the deterministic flat-trace hypothesis isolated in the
preceding long-cycle paper. It applies the Keller--Nowicki weighted-zeta
theorem to the two mixing components of the square map and compares the
standard Perron periodic weight with the physical flat trace.

## Reproduction

```bash
/root/math/.venv/bin/python -m pytest -q
PYTHONPATH=src /root/math/.venv/bin/python experiments/run_flat_trace_completion.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
