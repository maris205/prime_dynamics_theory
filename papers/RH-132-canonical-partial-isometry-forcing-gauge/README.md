# RH-132: Canonical Partial-Isometry Gauges

This paper constructs the polar partial isometry between changing supports,
proves its principal-angle/Procrustes optimality, and proves that
`(D' - b W D W*)_+` is the trace-minimal positive forcing.  Target mass
outside the final space of `W` is an unavoidable additive lower bound.

The 4,096-case audit has zero failures.  RH-130's 96 edges split into 30
vacuous `0→0`, 42 transport-eligible `4→4`, and 24 forcing-only `0→4`
transitions.  Twenty-two of the 24 normalized birth strengths are subunit.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_partial_isometry_audit.py --smoke
/root/math/.venv/bin/python experiments/build_partial_isometry_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf canonical-partial-isometry-forcing-gauge.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```
