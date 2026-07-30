# RH-265: Certified Deterministic-Tail Ladder

RH-265 packages the direct factorwise majorant into a first-omitted-order
ladder.  Arb replays certify both the logarithmic and multiplicative budgets
at orders 13, 21, 29, 37, 45, 53, and 61:

```text
N=13:  log < 2.3243607e-2,  multiplicative < 2.3515845e-2
N=21:  log < 8.73261e-4,   multiplicative < 8.73642e-4
N=29:  log < 2.6624745e-5, multiplicative < 2.6625100e-5
N=37:  log < 9.32147e-7,   multiplicative < 9.32147e-7
N=45:  log < 4.432615e-8,  multiplicative < 4.432615e-8
N=53:  log < 1.705725e-9,  multiplicative < 1.705725e-9
N=61:  log < 7.175542e-11, multiplicative < 7.175542e-11.
```

Only `N=29` is aligned with the currently archived RH-253 order-28 anchor.
The higher rows are rigorous conditional interfaces for a future head and
must not be read as claims that those heads have been constructed.  The cloud
bridge, legal head, uniform quotient tail, and Gates A--E remain open/false.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_tail_ladder.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf certified-deterministic-tail-ladder.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
