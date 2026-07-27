# RH-187: Regularized Cross-Gram Tradeoffs

RH-187 derives the exact cost of clipping small singular values of the
right/left cross Gram.  If `gamma` is its smallest singular value, `epsilon`
is the larger directed residual, and `d=max(gamma,tau)`, then the combined
duality and coordinate budget is

```text
(1-gamma/d) + epsilon/d = 1 + (epsilon-gamma)/d.
```

Consequently this clipping family has a strict contraction exactly when
`epsilon < gamma`.  The 126-window, 13-threshold audit contains 1,638 sweep
records.  Its minimum residual/cross-angle ratio is `10.253`, so no audited
window passes; the best finite-grid budget is `1.00904`.

This closes singular-value clipping with the stated additive budget.  It
does not exclude dynamics-aware regularization, directional Schur products,
or contour cancellation.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_regularization_tradeoff.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf regularized-cross-gram-tradeoff.pdf
```
