# RH-260: Updated Anchored Head--Tail Certificate Ledger

RH-260 updates the exact finite-head/analytic-tail interface after RH-252,
RH-255, RH-258, and RH-259.  RH-252 proves that the deterministic target has
an all-order Cauchy tail interface on the Hardy-scaled zero-free disk, but the
boundary constant `M_S` has no certified numerical upper bound.  RH-255 and
RH-258 give zero passes on the two archived expanded head tests: the
single-use shell box and the unit-cap signed-integer lattice, each at all 32
endpoints.  RH-259 gives a finite 23-endpoint quotient block diagnostic, not a
uniform small-noise theorem.  Consequently the updated complete-certificate
count remains exactly zero.

The paper proves the budgeted gluing estimate with first omitted order `N`,
records the logical component ledger, and states the scoped zero-certificate
obstruction.  The head obstruction is restricted to the two archived classes;
larger caps, signed/complex invariant selectors, a certified `M_S`, a uniform
quotient theorem, and the cloud coefficient bridge remain open.  All Gates
A--E are false/open.  No Hilbert--Polya operator, zeta-divisor equality,
Riemann-zero identification, or RH implication is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_updated_certificate_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf updated-anchored-head-tail-certificate-ledger.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
