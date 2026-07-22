# RH-94: source-seeded four-direction horizon refresh

This directory contains the ninety-fourth RH-layer paper:

> *Source-Seeded Four-Direction Horizon Refresh: Removing the Late Ambient Seed*

## Main result

The leading rank-r packet of the initial normalized memory Gramian

    G_0 = S* S / ||S||_F^2

is exactly the leading right singular subspace of the source S. Starting from
that packet at time zero, projected-cross Ritz refresh can be iterated through
the complete frozen prefix without inserting a later ambient leading
eigenspace.

The 384-bit audit covers 120 primary updates in ten channels. Width four:

- passes all ten endpoint gates;
- has worst endpoint/reference tail ratio 1.00117243;
- captures at least 97.536% of projected-cross energy at every update;
- uses compressed dimension at most 11.

Widths two and three have worst endpoint/reference ratios 11.39799 and
1.44894, respectively. Thus width four is the first tested width that robustly
tracks the complete prefix. The source-coordinate SVD and ambient Gram action
on the packet remain open reductions.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_source_seeded_horizon_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_source_seeded_horizon_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf source-seeded-four-direction-horizon-refresh.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
