# RH-29: One-Channel Grushin Deflation

This directory contains the manuscript, implementation, tests, archived
triplets, interval witnesses, and figures for:

> **One-Channel Grushin Deflation of a Nonnormal Complement Resolvent:**
> *Exact Lifted-Inverse Budgets at a Quadratic Band-Merging Map and a
> Certified Accretivity Obstruction*

## Main result

RH-28 reduced its remaining arcwise matrix Rouché condition to an external
upper bound for the complement resolvent.  RH-29 isolates one observed
near-singular direction before asking for that bound.

For

\[
A=z_0I-B,\qquad r=Av-\widehat s u,\qquad q=A^*u-\widehat s v,
\]

and the rank-one lift

\[
\widetilde A=A+(\tau-\widehat s)uv^*,
\]

the paper proves that any validated
\(K\geq\|\widetilde A^{-1}\|_2\) satisfying
\(\widehat s-|\tau-\widehat s|K\|r\|_2>0\) gives

\[
\|A^{-1}\|_2
\leq
K+
\frac{|\tau-\widehat s|(1+K\|r\|_2)(1+K\|q\|_2)}
{\tau(\widehat s-|\tau-\widehat s|K\|r\|_2)}.
\]

This yields a downward conditional lifted-inverse budget \(K_*^-\), which
combines with exact center-to-arc Neumann transport.

At the budget-tightest RH-28 arc of each stored scale:

- dimensions range from 2,048 to 204,800;
- normalized stored-factor right and left residuals are at most
  `4.38e-10` and `3.56e-9`;
- the floating lifted bulk singular candidate is 11.1--34.1 times larger
  than the dangerous candidate;
- the conditional lifted-inverse budget exceeds the floating bulk inverse
  candidate by factors 95.0--1,732;
- at `sigma=1e-4`, `K_*^- = 6.2911e4`, versus the floating candidate
  `6.6194e2`.

A separate outward-rounded three-vector certificate proves that the origin
lies in the coarse lifted numerical range.  Therefore no rotation can make
the lifted Hermitian part positive definite: a global accretivity estimate
cannot provide the missing inverse bound.

## Evidence hierarchy

Exact for the stored finite model:

- the one-channel Grushin/Sherman--Morrison identities and inverse bound;
- exact-normalization residual transfer;
- componentwise stored-factor residual enclosures;
- downward center and lifted-inverse budgets;
- the certified numerical-range convex-hull witness.

Conditional:

- if a validated lifted inverse bound lies below the archived `K_*^-`, the
  original inverse satisfies the RH-28 requirement on that selected arc.

Floating evidence only:

- inverse-iteration singular values;
- lifted bulk inverse candidates and singular gap ratios;
- GMRES convergence and candidate arc inverse margins.

RH-29 does **not** prove an upper bound for the lifted inverse, audit every
RH-28 arc, certify a winding/root count, validate the continuous Gaussian
operator, prove a small-noise limit, or make a claim about the Riemann
hypothesis.

## Reproduce

Run the unit tests and regenerate figures:

```bash
/root/math/.venv/bin/python -m pytest -q
/root/math/.venv/bin/python experiments/make_figures.py
```

Regenerate one physical scale in a fresh process:

```bash
OPENBLAS_NUM_THREADS=16 /root/math/.venv/bin/python \
  experiments/run_deflated_certificate.py --sigma 0.0001 --replace
```

The fine-scale inverse iterations are memory-bandwidth limited.  Running one
scale per process avoids retaining multiple large sparse matrices.

Build the manuscript:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

## Contents

- `main.tex`, `references.bib`: manuscript source;
- `src/deflated_resolvent/algebra.py`: lifted inverse theorem, arc transport,
  and downward budgets;
- `src/deflated_resolvent/norms.py`: Arb-backed exact stored-vector norms;
- `experiments/run_deflated_certificate.py`: seven-scale stored-factor audit;
- `experiments/run_rank_one_lift_pilot.py`: lifted bulk gap diagnostics;
- `experiments/run_certified_numerical_range_witness.py`: strict accretivity
  obstruction;
- `results/deflated_scale_summary.csv`: compact seven-scale table;
- `results/triplets/`: archived dangerous directions;
- `figures/`: PDF and PNG figures;
- `tests/`: synthetic inverse-bound, normalization, and budget tests.
