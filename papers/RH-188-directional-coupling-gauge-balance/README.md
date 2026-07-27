# RH-188: Directional Coupling and Gauge Balance

RH-188 keeps the two packet/complement couplings separate.  Under the scalar
biorthogonal gauge `V -> alpha V`, `W -> alpha^{-1} W`, their product is
invariant, while their maximum is minimized when both equal the geometric
mean.  This gives an exact optimal numerical representative without changing
the Schur feedback datum.

Across 126 physical windows, eight have absolute coupling product below one;
all eight lie in the local `sigma=0.01, L=4` branch.  Twelve local windows
have relative product below `0.01`.  Thus the failed maximum-residual budget
does not logically eliminate the sharper directed route.

The coupling product alone is not a Riesz certificate: packet and complement
resolvent factors are still missing.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_directional_balance_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf directional-coupling-gauge-balance.pdf
```
