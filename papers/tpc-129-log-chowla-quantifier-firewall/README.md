# TPC-129: A Log-Chowla Quantifier Firewall

Paper title:

> *A Log-Chowla Quantifier Firewall: Frozen Squarefree Truncations,
> a Slow Diagonal, and Why They Do Not Prove the Actual Fixed-Two H3
> Gate*

The paper records Tao's proved two-point theorem with its exact
quantifiers: fixed affine forms and a terminal reciprocal window

\[
\sum_{x/\omega(x)<m\le x}
\frac{\lambda(a_1m+b_1)\lambda(a_2m+b_2)}m
=o(\log\omega(x)).
\]

Using TPC-128, it derives an unconditional corollary for each fixed
determinant-two pair and each fixed finite squarefree cutoff. A
countable family can grow on a non-effective slow diagonal.

The paper then proves:

- an exact translated Tauberian identity;
- a finite-window example where reciprocal cancellation coexists
  with an ordinary sum of full order;
- a precise callable theorem for the actual growing modulus,
  origin, cutoff, masks, phase, physical weight, and all prefixes.

The fixed-form result and slow diagonal are not the physical family
and are not labeled L2. No growing actual-family power saving is
proved.

The audit records both the unweighted coefficient mass and the literal
weighted mass required by a callable estimate.  A fiber with zero
literal weighted mass is marked as a trivial zero case and excluded
from normalized positive-mass maxima.  The Tauberian and slow-diagonal
model checks use exact rational arithmetic.

Reproduce:

```powershell
python experiments/tpc129_firewall_audit.py
python experiments/tpc129_firewall_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-129-log-chowla-quantifier-firewall.pdf`

SHA-256:

`b1fc15225032f53afe00de67b9c3289ac507b4dabe197cfa0810b0c3edc0a9c3`
