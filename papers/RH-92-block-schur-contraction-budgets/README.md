# RH-92: block Schur contraction budgets

This directory contains the ninety-second RH-layer paper:

> *Block Schur-Secular Contraction Budgets: Exact Threshold Geometry and a
> Four-Step Replacement for Pointwise Sub-Quarter Decay*

## Main analytic result

For

```text
H = [[A,b],[b*,d]],
Delta = d - lambda_min(H),
M_delta = A - (d-delta) I,
```

the requested gain `Delta >= delta` holds exactly when either

1. `lambda_min(M_delta) <= 0`, or
2. `M_delta` is positive definite and `b* M_delta^{-1} b >= delta`.

In the coercive branch, a trial solve has the exact defect formula

```text
Phi_delta(x)
  = delta - b* M_delta^{-1} b
    + (M_delta x-b)* M_delta^{-1} (M_delta x-b).
```

The variable-budget theorem allows one-step factors to vary. If a refresh
packet is no worse than the small corrected packet, the packet tails multiply
by the product of those factors. A repeated length-`L` block product `Q < 1`
therefore replaces pointwise fixed-factor contraction.

## 384-bit audit

The archived four-step audit has:

- 5 scales, 10 channels, and 40 updates;
- 40 strictly negative Schur forms;
- 40 direct target contractions and refresh-dominance checks;
- largest exact rational block product `0.003219969564 < 0.24^4`;
- largest block geometric mean `0.2382116195`;
- 7 individual updates whose `0.24` threshold matrices are rigorously
  positive definite;
- minimum obstructed contraction `0.2504283221`;
- maximum compressed dimension 8.

Thus pointwise sub-quarter contraction is too strong on the selected frozen
windows, while the four-step budget remains green. A repeated all-level block
law and a polylogarithmic reduced refresh remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_block_schur_budget_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_block_schur_budget_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf block-schur-contraction-budgets.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
