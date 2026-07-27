# RH-189: Oblique Feshbach Determinant Factorization

RH-189 gives exact packet/complement coordinates for any finite
biorthogonal pair `W^*V=I`.  Extending `V` by a frame `Z` for `ker(W^*)`
produces an invertible similarity `S=[V,Z]` and a block operator

```text
S^{-1} A S = [[K,B],[C,D]].
```

Whenever `zI-D` is invertible, the determinant factors exactly through the
Feshbach self-energy:

```text
det(zI-A) = det(zI-D) det(zI-K-B(zI-D)^{-1}C).
```

A 240-case complex random audit has zero failures; its largest relative
determinant error is `1.85e-11`.  This proves the finite algebra and makes the
physical complement inverse a well-typed next target.  It does not validate
that inverse on any physical contour.

With an orthonormal complement frame, the block also satisfies the sharper
elementary bound `||D|| <= ||I-VW^*|| ||A||`.  Under a uniform Schur margin,
the exact count is `N_A=N_K+N_D`; equality with the packet count alone still
requires a zero complement count inside the contour.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_feshbach_identity_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf oblique-feshbach-determinant-factorization.pdf
```
