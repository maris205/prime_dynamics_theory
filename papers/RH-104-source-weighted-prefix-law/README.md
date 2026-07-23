# RH-104: source-weighted finite-prefix law

This directory contains the one-hundred-and-fourth RH-layer paper:

> *Source-Weighted Finite-Prefix Laws: Directional Certificates and a
> Block-Contraction Barrier*

## Main result

For a finite directional triple `(A,X,Y)` and horizon `M`, define

```text
S_M   = sum_{r<M} ||A^r X||_F^2,
P_M^2 = sum_{r<M} ||Y A^r X||_F^2.
```

The exact source-weighted identity is

```text
P_M^2 = tr(X* G_M X),
G_M   = sum_{r<M} (A^r)* Y*Y A^r.
```

If `q=||A^M||_2<1`, then

```text
tail_M^2 <= ||Y||_F^2 q^2 S_M / (1-q^2).
```

Therefore a polylogarithmic directional prefix law, together with the
square-root block law and a polylogarithmic source block, gives a
polylogarithmic full Hardy bound.

## Independent boundary result

The nilpotent family

```text
A_sigma = [[0,sigma^-a],[0,0]],
X       = e2,
Y_sigma = sigma^-b e1*,  0 <= b <= 1/2
```

has `A_sigma^2=0`, zero postblock state, perfect normalized one-column packet
Gramians, and valid observation scaling, while its prefix power is `a+b`.
Thus block contraction and normalized packet success do not imply the
physical finite-prefix law.

## Five-anchor audit

- maximum directional prefix upper: `1.760309`;
- maximum source-block upper: `3.099254`;
- maximum crude norm-product upper: `28.081536`;
- maximum crude/directional loss factor: `16.055390`.

These are finite certificates, not an all-level proof. Uniform directional
prefix control, Stage A, Hilbert--Polya, zero identification, and RH remain
open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_prefix_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_prefix_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf source-weighted-prefix-law.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
