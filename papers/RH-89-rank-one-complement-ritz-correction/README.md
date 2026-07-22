# RH-89: Rank-one complement Ritz correction

This directory contains the eighty-ninth RH-layer paper:

> *Rank-One Complement Ritz Correction for Dynamic Packet Energy*

## Main theorem

Let `G` be a positive Gramian, `V` an old rank-`r` packet, and `q` one unit
direction orthogonal to `V`. In the enriched space

    Z = span(V,q),

the leading rank-`r` Ritz subspace never captures less energy than `V` and
gives a certified upper bound on the full optimal tail. The correction only
requires an `(r+1) x (r+1)` eigenproblem.

Choosing `q` as the leading left singular direction of the cross block

    (I-VV*) G V

maximizes its coupling to the old packet among all single complement
directions.

## Ten-channel audit

At the final RH-88 predictor-corrector update:

- one complement direction plus a small Ritz solve captures at least `96%`
  of the full reference correction dividend in every channel;
- the corrected/reference tail ratio is below `3.28`;
- the corrected memory contraction factor remains below `0.24` in every
  channel;
- ranks 4--7 require only compressed dimensions 5--8;
- a 256-bit exact-binary-lift audit certifies the correction fraction and
  contraction gates.

The result identifies a concrete low-dimensional corrector. The all-level
problem is now to prove a uniform cross-block enrichment bound.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_ritz_correction_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_ritz_correction_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf rank-one-complement-ritz-correction.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
