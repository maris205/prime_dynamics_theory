# RH-259: Extended Quotient Block-Power Diagnostic

The ordered-Schur orthogonal-quotient audit is extended from dimension 512 to
1024.  This covers 23 endpoints, including six new ones.  All quotient
12th powers remain contractive, but the finite worst-case root rate worsens
from `0.3932995547` to `0.5056418006`, and the corresponding unit-disk tail
diagnostic worsens to `0.0005654508`.

The first contractive depth expands from `3--7` to `3--9`.  These data preserve
the block-power mechanism but weaken, rather than establish, a uniform
small-noise claim.  Nine archived endpoints and the continuum bridge remain
uncontrolled.

Gates A--E remain false/open.  No Hilbert--Polya operator, zeta-divisor
equality, Riemann-zero identification, or RH implication is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_extended_quotient_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf extended-quotient-block-power-diagnostic.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
