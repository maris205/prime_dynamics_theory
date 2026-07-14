# Sector-resolved critical-branch returns

This directory contains the twentieth-layer paper in the quadratic
prime-dynamics spectral program:

> *Sector-Resolved Critical-Branch Returns at a Quadratic Band-Merging Map:
> Exact Two-Channel Factorization, a Dark Antisymmetric Mode, and a
> Conditional Cubic-Phase Law*

RH-19 showed that the omitted critical sibling is an order-one channel and
that a sector-free time lift cannot identify physical resonance
multiplicity. This paper resolves the first finite-dimensional structure of
the corrected target.

If `C` maps the endpoint packet space into the two critical branches, `E`
returns those branches to the endpoint, and

```text
J(theta) = diag(1, exp(i theta)),
```

then the phase-weighted endpoint and branch returns are exactly

```text
R(theta) = E J(theta) C = R_minus + exp(i theta) R_plus,
B(theta) = J(theta) C E.
```

Their nonzero spectra and Fredholm determinants agree by the Sylvester
identity. In a one-packet rank-one reduction, the only nonzero return
eigenvalue is

```text
eta_minus + exp(i theta) eta_plus.
```

Under exact branch equivalence, the unweighted matrix has a bright symmetric
mode and a dark antisymmetric mode. If one additionally insists on
unit-modulus branch weights and asks the two-branch return to retain one
branch modulus, the relative phase is necessarily `theta = +/- 2*pi/3`.
This is a conditional algebraic theorem, not a derivation of the physical
closing phase.

At `sigma = 1e-4`, the audit finds

```text
dark / bright compressed eigenvalue modulus = 1.44734e-5
phase preserving the left modulus / pi       = 0.665704
phase matching the archived bulk edge / pi   = 0.661273
cubic-phase one-step radius                  = 0.756336
archived bulk edge                           = 0.757023
```

The evidence is encouraging but deliberately limited. Across all seven
noise levels the two-profile bright eigenvalue reproduces the full positive
two-branch return near `0.79`; it does not by itself reproduce the physical
bulk edge. At `sigma = 1e-3`, Perron/parity deflation changes the entire
phase family substantially. A real half-weighted sum
`(R_minus + R_plus)/2` also removes the factor of two in the symmetric
rank-one limit. The physical model must therefore derive either a closing
phase or a dual normalization; neither is inserted by hand here.

Run the tests and full audit with:

```bash
/root/math/.venv/bin/pytest -q
PYTHONPATH=src OPENBLAS_NUM_THREADS=16 /root/math/.venv/bin/python \
  experiments/run_sector_branch_audit.py
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
