# RH-194: Physical Edge-Root Matching

The 12 surviving `sigma=0.01, L=4` temporal windows are compared directly
with the base physical operators.  All 48 packet roots match a unique base
eigenvalue inside the predeclared RH-190 root contour.  The maximum root
error is below `1.3e-3`; only four distinct modes occur on each physical
side, and every matched mode has nonzero source--observation residue.

The corresponding temporal and canonical four-mode spectral subspaces are
also close: the maximum principal-angle sine ranges from about `0.035` to
`0.113`.  This is a strong finite positive result.  It shows that the
RH-185 clock did not invent four roots; it approximated a genuine physical
edge quartet.

The eigenanalysis is floating point, not an interval enclosure, and the
quartet is established only at the audited `sigma=0.01` anchor.  Full
Frobenius Riesz multiplicity remains 256 per root; the rank-one statement is
source-channel relative.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_physical_edge_matching.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf physical-edge-root-matching.pdf
```
