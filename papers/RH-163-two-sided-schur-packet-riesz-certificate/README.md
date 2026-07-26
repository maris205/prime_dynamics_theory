# RH-163: Two-Sided Schur Packet--Riesz Certificate

RH-163 replaces the symmetric RH-161 Neumann gate by a directed feedback
product.  On a separating contour let `a,d` bound the packet and complement
resolvents and let `b,c` bound the complement-to-packet and
packet-to-complement couplings.  Then

```text
kappa = a d b c < 1
```

keeps the contour in the resolvent throughout the off-diagonal homotopy and
preserves the enclosed spectral rank.  An explicit 2-by-2 scalar block gives
a Riesz-projector error bound.

The product gate can certify strongly imbalanced systems rejected by
`max(a,d) max(b,c) < 1`.  In particular, triangular coupling has `kappa=0`
regardless of the size of the nonfeedback block.  This is a strict theorem,
not a physical all-level estimate; the actual four quantities remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_schur_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf two-sided-schur-packet-riesz-certificate.pdf
```
