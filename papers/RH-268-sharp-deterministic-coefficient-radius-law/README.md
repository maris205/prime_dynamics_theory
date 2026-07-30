# RH-268: Sharp Deterministic Coefficient-Radius Law

RH-268 proves that the RH-267 envelope base is optimal:

```text
a_n / q_*^n -> 1,
q_* = 1/(r_H lambda) = 0.7008752258547757...
```

Consequently the logarithmic coefficient root rate is exactly `q_*`, the
radius is exactly `rho_*=r_H lambda=1.4267874838640739...`, no all-order
geometric envelope with a smaller base can hold, and the absolute logarithmic
series diverges at the critical radius.  This is a deterministic-target
sharpness theorem and a scoped negative result for improving the base; it says
nothing about a moving-cloud rate.

Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_sharp_law_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf sharp-deterministic-coefficient-radius-law.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
