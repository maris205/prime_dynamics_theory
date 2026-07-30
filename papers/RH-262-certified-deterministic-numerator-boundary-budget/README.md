# RH-262: Certified Deterministic-Numerator Boundary Budget

RH-262 supplies the first rigorous numerical boundary constant for the
Hardy-scaled deterministic numerator.  It combines the exact RH-15
factorization with the RH-13 Arb-certified reduced Wiener operator bounds.
No angular sampling is used.

On the fixed rational circle `S=7/5`, the normalized logarithm satisfies

```text
M_(7/5) = sup_|z|=7/5 |log G(z/0.85)| < 107.906078 < 108.
```

Because RH-253 anchors the deterministic coefficients through order 28, the
first omitted order is 29.  On the unit disk the clean bound `M_(7/5)<108`
therefore gives

```text
sum_(n>=29) |a_n|/n < 0.021866475,
exp(tail)-1 < 0.022107298.
```

This closes only the certified target-boundary-constant component of the
RH-260 ledger.  The obligation vector becomes `(false, false, false, true,
true)`: legal anchored head, cloud coefficient bridge, and uniform quotient
tail remain open, so the complete-certificate count is still zero.  Gates
A--E remain false/open.  No Hilbert--Polya operator, Riemann-zero
identification, zeta-divisor equality, or RH implication is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_boundary_budget.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf certified-deterministic-numerator-boundary-budget.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
