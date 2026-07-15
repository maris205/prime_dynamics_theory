# Directional Rouché closure

This directory contains the twenty-fifth-layer paper in the quadratic
prime-dynamics spectral program:

> *Directional Rouché Closure Beyond a Global Resolvent Barrier at a
> Quadratic Band-Merging Map: Exact Residual Identities, Low-Rank
> Corrections, and a Small-Noise Stress Test*

RH-24 reduced its missing rigorous transfer to a bound on the external
resolvent. RH-25 shows that the full norm is sufficient but not intrinsic.
For

```text
R_J(z) = C - (zI - B) X_J(z),
F_J(z) = zI - D - E X_J(z),
```

the exact finite-dimensional identity is

```text
F(z) - F_J(z) = -E (zI - B)^(-1) R_J(z).
```

Hence the matrix-Rouché transfer needs only the resolvent action on the
low-rank residual block:

```text
sup_Gamma ||F_J(z)^(-1) E (zI - B)^(-1) R_J(z)||_2 < 1.
```

The paper also proves an inexact two-level correction identity, a
conditional geometric depth-tail majorant, and a circular singular-value
Lipschitz extension.

## Main finite-matrix results

Across seven scales from `sigma=1e-2` to `1e-4`:

- dimensions range from 2,048 to 204,800 and packet ranks from 4 to 9;
- determinant windings at depths `J`, `J+8`, and `J+16` are all 1;
- the maximum `J -> J+16` directional ratio is `4.9642e-11`;
- at the two informative smallest scales, direct residual corrections agree
  with the extended-Krylov changes to within 0.80% and 0.23%;
- every attempted correction solve converges, and corrected ambient
  residuals are at most `1.66e-14`;
- only the two smallest scales rise above the declared `1e-12` increment
  interpretation floor. The reported geometric tails remain conditional.

At `sigma=1e-2`, a separate 32-node global probe gives a minimum ambient
shifted-complement singular-value candidate `3.05054e-3`, maximum candidate
inverse norm `327.81`, and maximum nodal scalar Rouché candidate
`8.6305e-11`. The elementary full-circle Lipschitz lower candidate is zero,
so this is not a continuous certificate. A 64-node direct full-forcing
GMRES approximation has winding 1 and maximum directional difference
`7.2586e-12`.

At `sigma=1e-3`, four cardinal global singular-value probes each exhaust a
20-second wall-clock budget. This records a scalability limitation of the
chosen normal-equation algorithm, not a spectral counterexample.

The distinction between theorem and evidence is essential. The algebraic
identities and conditional criteria are exact finite-dimensional results.
The reported windings, GMRES corrections, and singular values are
floating-point evidence for finite sparse matrices. There is no completed
computer-assisted contour proof, continuum theorem, or small-noise theorem.

## Reproduction

Run the unit tests:

```bash
PYTHONPATH=src /root/math/.venv/bin/pytest -q
```

Run the complete seven-scale audit:

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=16 /root/math/.venv/bin/python \
  experiments/run_directional_closure_audit.py
```

Run the global and direct probes:

```bash
PYTHONPATH=src:experiments OPENBLAS_NUM_THREADS=16 \
  /root/math/.venv/bin/python experiments/run_global_resolvent_probe.py
```

Regenerate figures and metadata from committed results:

```bash
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_directional_closure_audit.py --reuse
PYTHONPATH=src:experiments /root/math/.venv/bin/python \
  experiments/run_global_resolvent_probe.py --reuse
```

Build the manuscript:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The result tables, source hashes, software versions, figures, and fixed
budget records are committed under `results/` and `figures/`.
