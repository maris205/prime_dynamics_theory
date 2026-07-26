# RH-165: Midgap Normal-Block Contour

RH-165 solves the contour choice exactly under a transparent normal-block
model.  Suppose the packet spectrum lies in `|z-mu| <= rho`, the complement
spectrum lies in `|z-mu| >= R`, and both diagonal blocks are normal.  Among
centered circles, the midpoint radius

```text
s_* = (rho + R)/2
```

minimizes the Schur feedback.  The exact sufficient rank gate is

```text
2 sqrt(b c) < R-rho.
```

This converts four contour quantities into a geometric gap condition and
proves that the midpoint is optimal for rank certification.  It is not valid
for a nonnormal block from spectral location alone; there one must retain
pseudospectral/resolvent bounds.

The finite audit checks 512 normal block systems with zero rank-count or
resolvent-bound failures.  No normality theorem for the physical operator is
claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_midgap_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf midgap-normal-block-contour.pdf
```
