# Square-root parity boundary layer

This directory contains the fourteenth-layer theory paper in the quadratic
prime-dynamics program:

> *Square-Root Parity Splitting at a Quadratic Band-Merging Map: Coupled
> Critical-Value Boundary Layers and a Corrected Small-Noise Law*

The paper resolves the stochastic parity question left by RH-10. The negative
finite-noise resonance satisfies

```text
1 + lambda_-(sigma) = C_* sqrt(sigma) + o(sqrt(sigma)),
C_* = 0.105258535936908...
```

The constant is not fitted. It is the solvability pairing between two exact
small-noise layers:

- the repelling component-boundary observable
  `H(xi) = -erf(kappa*xi)`;
- the critical-value endpoint density
  `R(xi) = rho_c integral phi(u*q^2-xi)/Phi(u*q^2) dq`.

Consequently the parity lifetime is asymptotic to
`1/(C_* sqrt(sigma))`. The previously reported `sigma^(2/3)` law is a
reproducible intermediate-window fit, not the asymptotic exponent.

## Reproduction

Run the tests and full sparse audit:

```bash
/root/math/.venv/bin/python -m pytest -q
PYTHONPATH=src OPENBLAS_NUM_THREADS=16 \
  /root/math/.venv/bin/python experiments/run_boundary_layer_audit.py
```

The full audit reaches `sigma=1e-4` with a `204800`-state sparse matrix and
about `6.77e7` nonzeros. To regenerate only figures and the JSON summary from
the archived CSV data, use:

```bash
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_boundary_layer_audit.py --reuse-results
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The matrix calculations are floating-point diagnostics. The square-root
exponent and positive integral formula for `C_*` are analytic results; the
displayed decimal value is numerical quadrature.
