# Contour Feshbach root counting

This directory contains the twenty-fourth-layer paper in the quadratic
prime-dynamics spectral program:

> *Contour Feshbach Root Counting at a Quadratic Band-Merging Map: Blind
> Resonance Prediction, Holomorphic Shifted Krylov Reduction, and a Narrow
> Isolation Corridor*

RH-23 verified the exact packet/complement equations by inserting an already
known physical eigenpair. RH-24 upgrades that closure test to an independent
finite-matrix spectral prediction.

For `WV = I`, `P = VW`, `Q = I-P`, and the physical two-step operator `A`, set

```text
D = W A V,   C = Q A V,   E = W A Q,   B = Q A Q | Ran(Q).
```

The exact Feshbach matrix is

```text
F(z) = z I - D - E (z I - B)^(-1) C.
```

The paper proves the finite-dimensional identities

```text
det(z I - A) = det(z I - B) det F(z),
wind_Gamma det F = N_Gamma(A) - N_Gamma(B).
```

Every column of `C` is reduced in its own shift-invariant Arnoldi space. This
produces one holomorphic rational model `F_J(z)` for the whole contour, not a
collection of unrelated pointwise solves. It is the exact Schur complement
of an explicit augmented matrix `M_J`, so its winding is independently
checked by an ordinary zero-minus-pole eigenvalue count.

The target-blind protocol uses only the two real Perron/parity modes and the
rightmost lower-half-plane eigenvalue of `D`. The nonreal outer eigensystem is
computed by a separate reference call only after the contour root is frozen.

Across seven scales from `sigma=1e-2` to `1e-4`:

- all selected determinant windings are `1`;
- all selected projected pole counts are `0`;
- all augmented zero counts and captured outer reference counts are `1`;
- direct packet errors are `0.0471--0.248`;
- contour-Feshbach prediction errors are `1.36e-15--3.47e-14`;
- the maximum floating Arnoldi residual bound is `1.93e-11`;
- the maximum sampled depth-change Rouché ratio is `4.59e-6`;
- the pole-free one-root corridor remains open, with width `0.0101--0.0288`.

Packet half-widths `5, 6, 7` were also tested at `sigma=1e-3` and `1e-4`.
All six variants retain winding/poles/zeros `= 1/0/1`; the largest prediction
error is `6.01e-13`.

The distinction between theorem and evidence is essential. The Schur,
argument-principle, augmented-determinant, residual, and conditional
matrix-Rouché statements are exact finite-dimensional results. The reported
root counts and comparisons are floating-point evidence for finite sparse
matrices. A validated upper bound for the exact external resolvent is still
missing, so this is not a computer-assisted continuum or small-noise theorem.

Run the unit tests with:

```bash
PYTHONPATH=src /root/math/.venv/bin/pytest -q
```

Run the complete seven-scale audit with:

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=16 /root/math/.venv/bin/python \
  experiments/run_contour_feshbach_audit.py
```

Run the packet-window audit with:

```bash
PYTHONPATH=src:experiments OPENBLAS_NUM_THREADS=16 \
  /root/math/.venv/bin/python experiments/run_packet_window_audit.py
```

Regenerate figures and metadata from committed results with:

```bash
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_contour_feshbach_audit.py --reuse
PYTHONPATH=src:experiments /root/math/.venv/bin/python \
  experiments/run_packet_window_audit.py --reuse
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
