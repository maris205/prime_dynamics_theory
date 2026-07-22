# RH-85: Midblock snapshot packets

This directory contains the eighty-fifth RH-layer paper:

> *Midblock Snapshot Packets and Prefix-Only Captured-Energy Certificates*

## Main theorem

For `X_j=A^j S`, let `V` be any rank-`r` right packet constructed at time
`j<M`. Then

    ||X_M(I-VV*)||_HS
      <= ||A^(M-j)|| ||X_j(I-VV*)||_HS.

Thus a packet built strictly before the terminal horizon gives a valid
rank-`r` certificate for the final state. No final-state singular vectors are
needed to construct the approximation.

An explicit two-channel diagonal family also proves that the leading packet
of the unweighted prefix Gramian can miss asymptotically all terminal energy.
Early transient energy must therefore be discounted.

## Five-scale audit

At each archived scale, the packet is the clock-rank right singular space of
the strict-prefix snapshot `X_ceil(2M/3)`. Its final residual is evaluated directly
in 192-bit Arb arithmetic.

- ranks range from 4 to 7;
- maximum certified relative terminal residual is below `4.5e-6`;
- minimum certified terminal energy capture exceeds `0.99999999997`;
- the packet uses only roughly the first two thirds of the production horizon;
- source-only packets can leave over 84% relative residual;
- unweighted prefix-Gramian packets can leave over 32%.

This is a finite-scale prefix certificate, not an all-level packet theorem.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_snapshot_packet_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_snapshot_packet_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf midblock-snapshot-packets.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
