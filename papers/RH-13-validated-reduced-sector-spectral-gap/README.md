# Validated reduced-sector spectral gap

This directory contains the thirteenth-layer theory paper in the quadratic
prime-dynamics program:

> *Validated Reduced-Sector Spectral Gaps at a Quadratic Band-Merging Map: A
> Computer-Assisted Proof of Postcritical Zeta Noncancellation*

The paper resolves the reduced-sector disk-bound conjecture left by RH-12.
Deck parity converts the two analytic circle transfer sectors into explicit
coefficient-decimating Wiener--Taylor operators. A finite Taylor matrix and
rigorous Cauchy tails, evaluated with 100-decimal Arb balls, certify

```text
||T_(1,0)^3|| < lambda^(-6)
||T_(2,-)^2|| < lambda^(-4).
```

Consequently both reduced spectral radii are below `lambda^(-2)`. This proves
that the postcritical zero at `z=lambda` and pole at `z=lambda^2` are
uncanceled and gives

```text
q_n = 1 - lambda^(-n) + lambda^(-2n) + O(3^(-n)).
```

The theorem is computer-assisted. The analytic infinite-dimensional tail
bounds are stated in the manuscript, and the JSON certificate records every
interval, software version, and source hash. Floating-point eigenvalues are
diagnostics only.

## Reproduction

```bash
/root/math/.venv/bin/python -m pytest -q
PYTHONPATH=src /root/math/.venv/bin/python experiments/run_validated_certificate.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The primary interval certificate completes in under one second on the
reported machine. The experiment also repeats the proof at dimensions
`30, 40, 50, 60, 70` and regenerates the audit figure.
