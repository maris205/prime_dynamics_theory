# Prime Dynamics Program, Volume III

## Deterministic numerator anchors, analytic tails, and counterloops

Volume III synthesizes RH-242--RH-281 while preserving all forty numbered
papers as atomic sources. Its four phases are:

```text
RH-242--251  superloops, coefficient dictionaries, quotient grouping,
             and frozen-anchor obstructions
RH-252--261  analytic target tails and legal-selector barriers
RH-262--271  all-order deterministic envelope, sharp radius, and
             finite-head separation
RH-272--281  resolution-clocked counterloops and quotient limitations
```

The deterministic target side is genuinely all-order. In its stated
normalization it has an exact parity anchor, the envelope

```text
|a_n| < 48 q_*^n,  q_* = 0.7008752258547757...,  n >= 2,
```

the sharp limit `a_n/q_*^n -> 1`, and radius
`rho_*=1.4267874838640739...`. The resolution-clocked monodromy counterloop
also gives an exact all-order coefficientwise deterministic bridge.

These results do not identify a legal actual noisy head. The current physical
route still lacks an operator-derived selector, a cloud-to-anchor coefficient
bridge, aggregate noisy-cloud transport, and an instantiated variable-rank
quotient theorem. Finite fits and deterministic reparameterizations cannot
pay those obligations.

All Gates A--E remain false/open. The volume does not construct a
Hilbert--Polya operator, identify Riemann zeros, prove a von Mangoldt trace,
prove completed-zeta divisor equality, or prove RH.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_volume_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf deterministic-numerator-anchor-counterloop-synthesis.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
