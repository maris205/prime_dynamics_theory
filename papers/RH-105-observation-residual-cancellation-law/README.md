# RH-105: observation--residual cancellation law

This directory contains the one-hundred-and-fifth RH-layer paper:

> *Observation–Residual Cancellation in Postblock Hardy Transfer: A
> Signed-Power Theorem and a Sharp Rate-Matching Boundary*

## Main theorem

For a postblock state `B`, a rank-`r` approximation `B_r`, and

```text
Omega = sqrt(||O_M||_2 / (1-q^2)),  q = ||A^M||_2 < 1,
tau_r = ||B-B_r||_F,
```

the complete-future perturbation obeys

```text
|T(B)-T(B_r)| <= Omega tau_r.
```

If `Omega = O(sigma^-o polylog)` and
`tau_r = O(sigma^rho polylog)`, its growth power is

```text
max(0, o-rho).
```

The zero-power threshold is exactly `rho >= o`. The scalar family in the
paper shows this rate boundary is sharp.

## Five-anchor audit

- maximum observation factor: `21.255430`;
- maximum square-root-normalized observation factor: `2.125543`;
- maximum clock residual: `1.231019e-9`;
- maximum residual divided by `sqrt(sigma)`: `3.077547e-9`;
- maximum recomposed weighted residual: `5.043024e-9`;
- maximum recomposition discrepancy: below `5e-16` relative.

The finite audit is strongly green, but uniform observation growth and uniform
clock-residual decay remain independent open laws.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_cancellation_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_cancellation_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf observation-residual-cancellation-law.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
