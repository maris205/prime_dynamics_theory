# RH-28: Arcwise Rational-Arnoldi Enclosures

This directory contains the manuscript, implementation, tests, figures, and
archived data for:

> **Arcwise Primal–Dual Feshbach Enclosures at a Quadratic Band-Merging Map:
> Certified Rational Arnoldi Relations, Adaptive Circular Covers, and a
> Single Remaining Resolvent Gate**

## Main result

RH-27 certified stored-factor residuals at contour nodes. RH-28 extends the
same finite binary64 model from nodes to a complete mathematical circle by
combining:

- componentwise coordinate discs for ((zI-H)^{-1}b) on a disc;
- an exact nested-Hessenberg increment identity,
  \[
  (zI-H_K)(y_K-\iota y_J)
  =h_{J+1,J}(y_J)_J e_{J+1};
  \]
- Arb-backed circular subarc discs and an exact dyadic partition;
- columnwise relation and coupling bounds that retain the small Arnoldi-tail
  structure; and
- a Neumann certificate for the projected (4\times4)–(9\times9) Feshbach
  family on every subarc.

For every accepted arc the code proves, for the stored rational model,

\[
\|\widehat F_J(z)^{-1}(F(z)-\widehat F_J(z))\|_2
\leq \bar\eta_a+M\,\bar c_a,
\qquad z\in\text{arc disc},
\]

where (M) is an *external* upper bound for the complement resolvent

\[
M\geq\|(zI-B)^{-1}\|_2.
\]

The downward threshold

\[
M_{*,a}^-=(1-\bar\eta_a)/\bar c_a
\]

is therefore a conditional gate. It is not an estimate of the complement
resolvent.

The seven-scale adaptive audit gives:

| \(\sigma\) | dimension | packet rank | accepted arcs | max \(\bar\eta\) | min \(M_*^-\) |
|---:|---:|---:|---:|---:|---:|
| \(10^{-2}\) | 2,048 | 4 | 936 | \(4.2264\times10^{-4}\) | \(3.9726\times10^{13}\) |
| \(4\times10^{-3}\) | 5,120 | 5 | 2,065 | \(1.3301\times10^{-2}\) | \(5.9371\times10^{11}\) |
| \(2\times10^{-3}\) | 10,240 | 6 | 6,368 | \(4.2752\times10^{-2}\) | \(9.9689\times10^{10}\) |
| \(10^{-3}\) | 20,480 | 7 | 8,942 | \(4.0328\times10^{-1}\) | \(3.1793\times10^{9}\) |
| \(5\times10^{-4}\) | 40,960 | 7 | 7,160 | \(7.3662\times10^{-1}\) | \(5.0691\times10^{8}\) |
| \(2\times10^{-4}\) | 102,400 | 8 | 13,440 | \(9.3186\times10^{-1}\) | \(4.0368\times10^{7}\) |
| \(10^{-4}\) | 204,800 | 9 | 29,538 | \(9.9959\times10^{-1}\) | \(1.0999\times10^{5}\) |

The last row is a near-boundary success, not a comfortable margin. The
maximum projected-family Neumann product is also close to one on some arcs;
this is why the adaptive cover is necessary.

## What is proved and what is not

The exact theorem-level scope is the finite stored-factor model: binary64
inputs are treated as exact complex numbers and all operation bounds are
propagated outward under the stated round-to-nearest model, assuming finite
intermediates and no harmful underflow.

Conditionally, if a validated upper bound for the complement resolvent is
smaller than the minimum archived threshold, the matrix Rouché inequality
holds on the full stored contour. RH-28 does **not** provide that upper
bound. It also does not validate the continuous Gaussian-kernel
construction, prove convergence of the finite sections, certify a winding
number/root count, or make any statement about the Riemann hypothesis.

## Reproduce

From this directory, with the shared environment used in the repository:

```bash
/root/math/.venv/bin/python -m pytest -q
/root/math/.venv/bin/python experiments/make_figures.py
```

The archived seven-scale tables are already committed. A full audit can be
regenerated one scale at a time (the one-scale form avoids forking and then
continuing an ARPACK process in the same interpreter):

```bash
/root/math/.venv/bin/python experiments/run_arcwise_enclosure.py \
  --sigmas 0.01 --arcs 64 --workers 16 --resume
```

Repeat for the remaining six values in `RH-24` order. `--resume` writes each
completed scale immediately. The process pool uses Linux `fork` so the large
read-only Arnoldi bases and static certificates are shared by copy-on-write;
use `--workers 1` on systems without `fork`.

## Contents

- `main.tex`, `references.bib`: manuscript source;
- `src/arcwise_feshbach/coordinates.py`: disc solves and correlated nested
  increments;
- `src/arcwise_feshbach/geometry.py`: Arb circular covers and dyadic
  bisection;
- `src/arcwise_feshbach/relations.py`: static outward Arnoldi relation and
  coupling certificates;
- `src/arcwise_feshbach/evaluator.py`: arcwise Feshbach budgets;
- `experiments/run_arcwise_enclosure.py`: resumable seven-scale audit;
- `experiments/make_figures.py`: figures from archived CSV data;
- `results/`: arc rows, scale summaries, and metadata;
- `tests/`: arithmetic, nested-increment, geometry, inverse, and archived
  partition tests;
- `figures/`: PDF and PNG plots.
