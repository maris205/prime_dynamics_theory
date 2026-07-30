# RH-267: Certified Unified Deterministic Trace Envelope

RH-267 proves the clean all-order deterministic-target bound

```text
|a_n| < 48 q_*^n  for every n >= 2,
q_* = 1/(r_H lambda) = 0.7008752258547757...
```

The proof combines the exact parity anchor with RH-13 nuclear trace bounds
grouped modulo three.  Arb certifies residue constants below `27.054`,
`47.538`, and `37.062`, so one uniform constant `48` covers every order.
This is the requested deterministic all-order trace envelope.  It is not a
moving-cloud envelope, a coefficient bridge, or a uniform quotient tail.

Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_envelope_certificate.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf certified-unified-deterministic-trace-envelope.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
