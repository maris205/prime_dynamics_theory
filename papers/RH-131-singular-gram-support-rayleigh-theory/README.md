# RH-131: Rayleigh Transport on Singular Gram Supports

This paper proves the floor-free singular-Gram theory needed after RH-130:

- finite full-space Rayleigh control iff `ker(G) subset ker(D)`;
- the sharp support constant from the Moore–Penrose relative pencil;
- a sharp `(1-gamma)^r sqrt(pdet(G))` supported-volume theorem;
- an outward support correction from Gram/tail spectral radii;
- no relaxation from merely small kernel leakage.

The audit verifies 4,096 compatible and 1,024 obstructed examples.  On the
RH-130 archive, 54 tails have rank zero and 66 rank four; all 24 rank-creating
edges coincide with the 24 infinite multiplicative factors.

Reproduction:

```bash
/root/math/.venv/bin/python experiments/build_support_audit.py --smoke
/root/math/.venv/bin/python experiments/build_support_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf singular-gram-support-rayleigh-theory.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```
