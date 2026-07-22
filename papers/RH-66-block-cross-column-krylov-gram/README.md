# RH-66: block cross-column Krylov Gram certificates

This directory contains the sixty-sixth RH-layer paper:

> *Block Cross-Column Krylov Gram Certificates for Phase-Fused Stein Tails*

## Main result

For an isometry `V`, block source `Z=VB+E`, projected operator `H=V*AV`,
and Galerkin residual `R=AV-VH`, the exact block identity is

```text
A^L Z = V H^L B
        + sum_(j=0)^(L-1) A^(L-1-j) R H^j B
        + A^L E.
```

If `M-A*MA=I` and `q=||M^(1/2) A M^(-1/2)||<1`, this identity yields two
certificates:

- a coefficient-aware center-radius upper that preserves packet phases;
- a positive-semidefinite Gram envelope valid for every coefficient vector.

The residual Gram uses matrix terms `C_j* R* M R C_j` before any positive
majorization, so cross-column cancellation is retained.

## Model audit

For a two-column source whose slow components cancel under coefficients
`(1,1)` at horizon 32:

- independent-column gain: `2.129e18`;
- block directional gain: `1.0000014`;
- uniform PSD Gram gain in that special direction: `410.16`.

Thus block fusion fixes the catastrophic columnwise loss, while the uniform
PSD envelope exposes the next wall. On the four-step nonnormal chain, one
block level reduces the gain from `11.37` to `3.90`; rank-four block closure
is exact. On the six-mode phase model, the corresponding values are `1.713`
and `1.288`, followed by exact rank-six closure.

A 256-bit Arb audit certifies the cancelling source and proves that the
independent-column lower loss exceeds `1e18`.

## Route consequence

The next paper must replace the trace-global PSD majorant by a
coefficient/packet-adapted residual geometry without losing positivity.
Production-family uniform block depth remains open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_block_gram_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_cancellation_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf block-cross-column-krylov-gram.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
