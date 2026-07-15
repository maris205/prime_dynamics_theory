# RH-27: Outward-Rounded Primal–Dual Residual Enclosures

This directory contains the paper, code, data, tests, and figures for:

> **Outward-Rounded Primal–Dual Residual Enclosures at a Quadratic
> Band-Merging Map: Stored-Factor Error Graphs, a Normwise False Failure,
> and Componentwise Recovery**

## Main result

For the exact finite model defined by the stored binary64 factors,

\[
U=M-R\Lambda L^*,\qquad Q=I-VW,
\]

\[
B=QU^2Q,\quad C=QU^2V,\quad D=WU^2V,\quad E=WU^2Q,
\]

the paper retains the base reconstruction defect

\[
\delta_J=zI-D-EX_J-F_J
\]

and proves

\[
F-F_J
=\delta_J-E(X_K-X_J)-Z^*r-s^*(zI-B)^{-1}r,
\]

where

\[
r=C-(zI-B)X_K,
\qquad
s=E^*-(\bar z I-B^*)Z.
\]

The complete sparse/dense graph is enclosed under a conservative binary64
round-to-nearest model. Small packet inverses are bounded by a Neumann
defect, yielding

\[
\|F_J^{-1}(F-F_J)\|_2
\le \bar\eta+\|(zI-B)^{-1}\|_2\bar c
\]

and a downward-rounded conditional inverse budget.

Key numerical findings:

- the global normwise enclosure succeeds at six of seven scales;
- at `sigma=1e-4`, it has a transparent false failure with maximum
  `eta_upper = 5.657508823134548`, despite a floating-centre ratio near
  `4.97e-11`;
- componentwise refinement lowers the worst finest-scale bound to
  `1.3173300056563153e-3` and restores a minimum conditional budget
  `4.7841283215183484e11`;
- over the seven-scale hybrid audit, the maximum outward correction ratio is
  `2.3254412133238377e-2` and the minimum budget is
  `6.301272823167764e8`;
- independent 63-bit-significand reevaluation uses at most
  `9.296710442919465e-5` of a componentwise radius.

These are stored-finite-matrix, standard-floating-model results. They do
not provide a complement-resolvent upper bound, validate contour arcs,
enclose construction error from the continuous Gaussian kernel, or prove a
continuous-operator root count.

## Contents

- `main.tex` and `outward-rounded-primal-dual-residuals.pdf`: paper source
  and compiled manuscript;
- `src/outward_residuals/enclosures.py`: normwise outward balls, Neumann
  inverse certificates, and downward budgets;
- `src/outward_residuals/componentwise.py`: componentwise complex-disc
  arithmetic;
- `src/outward_residuals/factor_graph.py` and `componentwise_graph.py`:
  complete stored-factor primal/dual graphs;
- `experiments/run_outward_residual_audit.py`: seven-scale normwise audit;
- `experiments/run_componentwise_refinement.py`: finest-scale refinement and
  hybrid summary;
- `experiments/run_componentwise_longdouble_crosscheck.py`: independent
  physical extended-precision diagnostic;
- `results/`: 224 normwise contour rows, 64 componentwise rows, summaries,
  metadata, and source/input hashes;
- `figures/`: PDF and PNG figures;
- `tests/`: seven unit tests for arithmetic, sparse/dense actions, full
  factor graphs, and inverse certificates.

## Reproduce

From this directory:

```bash
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Regenerate figures and metadata from archived CSV files:

```bash
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_outward_residual_audit.py --reuse
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_componentwise_refinement.py --reuse
```

Omit `--reuse` for a full matrix/Arnoldi recomputation. The two finest
scales retain large primal and dual Arnoldi bases and are the expensive
part of the audit.
