# Physical packet-complement Feshbach closure

This directory contains the twenty-third-layer paper in the quadratic
prime-dynamics spectral program:

> *Physical Packet-Complement Feshbach Closure at a Quadratic Band-Merging
> Map: Complex Spectral Targets, Resolvent Compensation, and a Nonuniform
> Conditioning Barrier*

RH-22 ruled out the scalar local dark channel as the missing attenuation.
This paper replaces that local model by the full complement of a canonical
packet projection inside the Perron/parity-extracted physical two-step
operator.

The first correction is conceptual. The outer physical resonance is complex:

```text
K_sigma r_sigma = mu_sigma r_sigma,
nu_sigma = mu_sigma**2.
```

Consequently `abs(mu_sigma)**(2*k)` is a radius target, not an exact return
eigenvalue unless `arg(mu_sigma**(2*k))` vanishes. RH-23 works directly at the
complex two-step target `nu_sigma`.

Let `V,W` be the canonical packet pair, `WV=I`, and put `P=VW`, `Q=I-P`.
For an exact physical eigenmode `A r = nu r`, define

```text
alpha = W r,
q     = Q r.
```

Then the two block equations are exact:

```text
(nu I - W A V) alpha = W A q,
(nu Q - Q A Q) q     = Q A V alpha.
```

When the external block is invertible, these are precisely the Feshbach
self-energy equations. They also give the computable lower bound

```text
||(nu Q-QAQ)^(-1)|| >= ||q|| / ||Q A V alpha||.
```

The seven-scale audit finds:

```text
sigma                              1e-2       1e-4
||P r||                            0.35076     0.06458
||Q r|| / ||P r||                  2.668      15.453
external resolvent lower bound     5.25       37.51
physical eigenvalue condition      9.21      151.06
spectral packet residue |l* P r|   1.181       1.619
||P r|| * resolvent lower bound    1.841       2.423
```

Thus the right packet component shrinks and the complement is not a small,
uniform perturbation. Nevertheless the gauge-invariant compressed-resolvent
residue stays order one: decreasing right capture is compensated by a growing
external resolvent and nonnormal left weight. Independent complex GMRES solves
converge at every scale in 20--56 iterations and reproduce the exact
eigenmode exterior to relative error at most `2.1e-8`.

The packet-route comparison marks three branches:

- merging only the final critical dark coordinate changes no target metric;
- retaining both labels at every slice adds no spectral residue but drives
  the Gram condition from `336.8` to `1750.8`;
- a single-label packet has a closer direct eigenvalue, but a smaller residue
  and a larger complement-resolvent lower bound.

The current viable route is therefore a renormalized, nonuniform Feshbach
construction. A uniform small-self-energy theorem is ruled out by the growing
resolvent lower bound. The next step is a block shifted solve on a contour,
followed by determinant/root-count control.

Run the tests and full seven-scale audit with:

```bash
/root/math/.venv/bin/pytest -q
PYTHONPATH=src OPENBLAS_NUM_THREADS=16 /root/math/.venv/bin/python \
  experiments/run_physical_feshbach_audit.py
```

Regenerate fits and figures from the committed CSV files with:

```bash
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_physical_feshbach_audit.py --reuse
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
