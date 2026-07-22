# RH-84: Ky Fan tail majorization

This directory contains the eighty-fourth RH-layer paper:

> *Ky Fan Tail Majorization and a Weaker Endpoint Corridor to Stage A*

## Main theorem

For a Hilbert--Schmidt operator `B`, the optimal rank-`r` residual is

    tau_r(B)^2 = tr(B*B) - sum_(j<=r) lambda_j(B*B).

For every rank-`r` orthogonal projector `P`, Ky Fan's principle gives the
certifiable upper

    tau_r(B)^2 <= ||B(I-P)||_HS^2.

If a physical postblock state and the RH-82 endpoint mediator satisfy only

    tau_(J_sigma+ell)(B_sigma)
       <= alpha_sigma tau_(J_sigma+ell)(R_sigma) + epsilon_sigma,

then the endpoint exponential tail immediately transfers. This condition is
strictly weaker than RH-83's termwise singular majorization or full operator
factorization and is already sufficient for the RH-78 effective-rank
corridor.

## Seven-scale audit

The first five scales reuse the 192-bit RH-82 interval residuals. Two new
out-of-sample stress levels use dimensions 1024 and 2048 with log-square
horizons 49 and 64.

- clock ranks range from 4 to 8 while ambient dimension reaches 2048;
- maximum physical/endpoint tail ratio is `0.013921`;
- maximum interval-certified relative tail is `2.340e-7`;
- at the two new stress levels, relative tails are below `1.56e-15`.

The extended levels are binary64 diagnostics, not an all-level theorem.

## Route consequence

The remaining analytic target can be weakened again: prove a uniform lower
bound for the energy captured by a clock-dimensional postcritical packet
space. Individual singular values and coordinate alignment need not be
controlled.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_tail_majorization_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_tail_majorization_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf ky-fan-tail-majorization.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```

