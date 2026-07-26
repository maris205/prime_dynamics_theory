# RH-167: Finite-Mesh Resolvent Envelope

RH-167 converts finitely many certified inverse bounds into a continuous
contour bound.  If every point of a contour is within `h` of a sample and
the sample resolvent norms are at most `m`, then

```text
h m < 1  =>  sup_Gamma ||(z-T)^(-1)|| <= m/(1-hm).
```

For `n` equally spaced nodes on a circle of radius `s`, the exact covering
radius is `2 s sin(pi/(2n))`.  Applying the envelope separately to packet and
complement blocks produces finite-input Schur and directional graph
certificates.

A dense-grid audit of 256 nonnormal matrices finds no envelope failure.  The
audit uses floating-point sample inverses only as diagnostics; a physical
proof still needs validated sample bounds.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_mesh_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf finite-mesh-resolvent-envelope.pdf
```
