# TPC-130: A Fejér Four-Sign Gate for H3

Paper title:

> *A Fejér Four-Sign Gate for H3: Sliding-Window TT-star, Diagonal
> Feasibility, and a Non-Circular Sufficient Reduction on the
> Complete Actual Block*

For

\[
S=\sum_{z=1}^N A_z e(-\alpha z),\qquad
C(h)=\sum_zA_{z+h}\overline{A_z},
\]

the paper proves the sliding-window inequality

\[
|S|^2\le\frac{N+H-1}{H}
\sum_{|h|<H}\left(1-\frac{|h|}{H}\right)e(-\alpha h)C(h).
\]

With \(V=\sum|A_z|\), \(E=\sum|A_z|^2\), and
\(\mathfrak p=V^2/(NE)\), this gives

\[
\frac{|S|^2}{V^2}
\le2\left(
\frac1{H\mathfrak p}
+\frac{N}{HV^2}(\mathcal O_H)_+
\right).
\]

In the exact TPC-127 frame the off-diagonal arithmetic factor is

\[
\lambda(n+qh-2)\lambda(n+qh)\lambda(n-2)\lambda(n),
\]

with every shifted mask, phase, physical weight, origin, and prefix
retained.

Status:

- Fejér identity, normalization, and exponent transfer: **L0**;
- crosswalk to the complete literal fixed-2 block: **L1**;
- the uniform growing four-sign estimate: **not proved**.

The paper includes a sharp sparse-support diagonal stop and an
explicit anti-circularity rule.

The local square-root counterpart of a quadratic \(X^{-1/200}\)
target is an amplitude saving \(1/400\).  The older \(1/200\)
termwise amplitude screen is only a stronger sufficient condition;
the final physical normalization and endpoint crosswalk remain
separate.

The audit checks the \(N+H-1\) window count and exact \(H\)-fold
participation with integer arithmetic.  It treats a zero-mass prefix
as a trivial zero case outside the normalized maximum, and records
separately the local \(1/400\) square-root target and the conservative
\(1/200\) termwise screen.

Reproduce:

```powershell
python experiments/tpc130_fejer_audit.py
python experiments/tpc130_fejer_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-130-fejer-four-sign-h3-gate.pdf`

SHA-256:

`4c6957635b23907674a23784a885e469e220926224d2b8ad898e1ea308004da0`
