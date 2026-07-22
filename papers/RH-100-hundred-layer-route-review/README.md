# RH-100: hundred-layer route review

This directory contains the centennial RH-layer paper:

> *A Hundred-Layer Audit of Prime Dynamics: Exact Theorems, Negative Routes, and the Minimal Stage-A/A5 Frontier*

## Inventory

- 99 prior RH directories, all with README, main TeX, and at least one PDF.
- 70 machine-readable summary archives.
- Nine research phases from rigorous symbolic reformulation through recursive
  packet propagation.
- Nineteen representative exact milestones and fifteen explicit negative
  route markers.

## Revised Stage-A frontier

The finite five-anchor chain is closed. The inclusion-minimal all-level
completion bundles are:

1. `{L}`: prove the RH-75 all-level full-block law;
2. `{Q,G,H_stop,O}`: uniform gap-aware quotient, structured packet Gram
   action, stopped hybrid horizon law, and prefix/observability bridge;
3. `{Q,G,H_tube,O}`: the same packet corridor with a finite differential
   tube instead of the stopped law.

RH-95--RH-99 make `H_stop` the preferred packet option. The smooth tube is
mathematically valid infinitesimally but currently blocked by unavailable
Ritz gaps and unusable constants.

Stage A5 still requires three additional gates in every bundle: an actual
moving-cloud Riesz projection, its coefficient bridge, and a uniform
trace-class complement.

## Selected next papers

- RH-101: finite-memory realization of the normalized Gram action on packets;
- RH-102: stopped quotient clock with an exact remaining endpoint budget;
- RH-103: prefix, normalization, and observability composition ledger.

No unconditional Stage A, Hilbert--Polya operator, zero identification, or RH
proof is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_hundred_layer_review.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_hundred_layer_review.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf hundred-layer-route-review.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
