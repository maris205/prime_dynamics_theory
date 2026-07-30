# RH-302: Annular tail reduction to the moving head

For every fixed `1.4 < rho < rho_star`, the actual noisy-complement and
deterministic-anchor tails beyond `ceil(4 log(1/sigma))` vanish in both
`H-infinity(rho)` and `H2(rho)`.  Thus full annular convergence is equivalent
to convergence of the moving polynomial head.  The moving head itself is
not controlled.

At `rho=1.41`, the certified noisy and target powers are respectively
`0.3982299046794737` and `0.04734279160561648`.

Reproduce with:

```text
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Gates A--E remain false/open.
