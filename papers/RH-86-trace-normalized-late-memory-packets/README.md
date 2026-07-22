# RH-86: Trace-normalized late-memory packets

This directory contains the eighty-sixth RH-layer paper:

> *Trace-Normalized Late-Memory Packets: A Gap-Free Dynamic Gramian and the
> Failure of Angle Perturbation*

## Main theorem

For snapshots `X_t=A^t S`, define the online normalized Gramian

    G_j = X_j*X_j / ||X_j||_HS^2 + eta G_(j-1).

Its leading rank-`r` projector minimizes the exponentially weighted sum of
relative snapshot residuals. In particular, the normalized stacked tail is a
gap-free upper bound for the current relative residual, and RH-85 snapshot
transfer propagates that packet through the unused suffix.

The theorem uses captured energy only. It does not require a spectral gap or
control of principal angles.

## Five-scale audit

With one universal memory parameter `eta=1/512` and packet time
`ceil(2M/3)`, direct 192-bit evaluation gives:

- maximum relative terminal residual below `1.10e-5`;
- minimum captured terminal energy above `0.99999999988`;
- at most `0.196%` normalized trace mass lies before the current snapshot;
- improvement over the unweighted prefix Gramian ranges from `1.04e3` to `4.63e6`;
- every Davis--Kahan perturbation/gap ratio exceeds `8.9e6`.

Thus late-memory energy is stable even where angle perturbation is
quantitatively unusable. The result remains a five-scale certificate rather
than an all-level packet theorem.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_late_memory_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_late_memory_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf trace-normalized-late-memory-packets.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
