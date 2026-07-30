# RH-266: Finite-Sample Quotient Uniformity Obstruction

RH-266 proves a scoped logical negative result: finitely many pointwise
block-power contractions do not imply a uniform parameter theorem without a
modulus of continuity or an interval family enclosure.  RH-259 supplies 23
finite contractions at 13 distinct noise values, but 9 archived endpoints
and the continuum remain outside the calculation.

The finite findings remain useful: 23/23 twelfth powers are contractive,
0/23 one-step blocks are contractive, first contraction occurs at depths
3--9, and `q12` ranges from `0.22185212659640824` to
`0.5056418005507071`.  The theorem says only that these data are logically
insufficient for uniformity; it does not prove that the underlying quotient
family is nonuniform.

All Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_uniformity_obstruction.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf finite-sample-quotient-uniformity-obstruction.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
