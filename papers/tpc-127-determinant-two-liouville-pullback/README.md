# TPC-127: Determinant-Two Liouville Pullback

Paper title:

> *Determinant-Two Liouville Pullback: An Exact Shift-Two Frame for
> Literal Affine Möbius Pairs and the Growing-Progression Barrier*

For positive primitive affine forms

\[
D(z)=d+sz,\qquad V(z)=u+az,\qquad su-ad=2,
\]

put \(n=sV(z)=aD(z)+2=su+as z\). The paper proves the exact identity

\[
\mu(D(z))\mu(V(z))
=\mu^2(D(z))\mu^2(V(z))\lambda(as)
\lambda(n-2)\lambda(n).
\]

It then transports the complete literal TPC-108 block, including its
progression, quotient-squarefree masks, coprimality mask, periodic
factor, physical weight, phase, interval origin, and prefixes.

Status:

- pullback algebra, order, prefix, and mass preservation: **L0**;
- attachment to verified actual primitive branches: **L1**;
- growing-progression fixed-\(2\) cancellation: **not proved (L2
  only if a future theorem establishes it)**.

The result does not replace the actual progression by an unrestricted
shift-two correlation and claims no parity breakthrough or twin-prime
conclusion.

The finite audit uses an interval that is not indexed as `[1,N]`, checks
every prefix at its actual endpoint \(T\in I\), and verifies with exact
Gaussian-integer arithmetic that the pullback preserves a weighted
oscillatory sum.  It also records the parity obstruction showing that
the simultaneous squarefree support cannot contain an even-even pair.

Reproduce:

```powershell
python experiments/tpc127_pullback_audit.py
python experiments/tpc127_pullback_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-127-determinant-two-liouville-pullback.pdf`

SHA-256:

`9241f6eb1e15749cd6af3c83afaaeb49b285d0657db3f0d60bd23cae17f5037c`
