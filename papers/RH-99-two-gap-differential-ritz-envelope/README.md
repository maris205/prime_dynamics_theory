# RH-99: two-gap differential Ritz envelope

This directory contains the ninety-ninth RH-layer paper:

> *Two-Gap Differential Envelopes for Adaptive Projected-Cross Ritz Refresh*

## Main theorem

Write the invariant cross covariance as

    C(P) = (I-P) G P G (I-P).

If its selected k-dimensional spectral projector has gap delta_c, and the
leading rank-r projector of the enriched Ritz operator has gap delta_r, then
the one-refresh projector derivative satisfies

    ||D F(P)|| <= 4 ||G|| / delta_r * (1 + 6 ||G||^2 / delta_c).

The two gaps correspond to two independent branches: cross-direction
selection and output Ritz selection.

## Audit

- 120 adaptive source-seeded updates and 720 tangent probes.
- 115 updates have both gaps certified; every probe lies below the theorem
  bound there.
- Five fine-scale output Ritz gaps cannot be certified positive under the
  binary64 residual guard.
- The largest available bound is `1.44e40`; it can exceed probes by `1.03e36`.
- Quotienting improves the formal bound at all five weak-mode updates, by as
  much as `9.44e9` relative to width four.
- None of the five actual quotient displacements lies inside the first-order
  separation radius.

Thus the differential formula is correct but does not yet produce a finite
neighborhood Lipschitz tube. This is the central open gate entering the RH-100
route review.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_two_gap_differential_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_two_gap_differential_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf two-gap-differential-ritz-envelope.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
