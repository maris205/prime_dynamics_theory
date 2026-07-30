# RH-264: Direct Factorwise Deterministic-Tail Certificate

RH-264 avoids the large global boundary constant by bounding the omitted
logarithmic coefficients factor by factor.  The Fredholm terms are grouped
modulo three using the RH-13 nuclear trace bounds; `A_*` and `B` use their
coefficientwise endpoint majorants; the odd factor is summed from its exact
parity formula.

At `R=1`, first omitted order `N=29`, Arb replay at 100/150/200 decimal
places certifies

```text
even tail < 0.000024488616
odd tail  < 0.000002136130
total log tail < 0.000026624745
exp(tail)-1 < 0.000026625100.
```

This is an all-order deterministic target bound, not a finite fit and not a
cloud or quotient certificate.  The legal anchored head, cloud coefficient
bridge, and uniform quotient tail remain open; Gates A--E are false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_direct_tail_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf direct-factorwise-deterministic-tail-certificate.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
