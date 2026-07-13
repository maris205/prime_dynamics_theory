# Fixed-length small-noise cycle localization

This directory contains the ninth-layer theory paper in the quadratic
prime-dynamics program:

> *Fixed-Length Small-Noise Localization for Gaussian Quadratic Markov
> Cocycles: Directed Periodic-Orbit Traces and Delayed Six-Step Asymptotics*

## Main results

- For every fixed parameter word of length `m >= 2`, if all deterministic
  closed orbits are interior and satisfy `F'(x) != 1`, then

      tr(K_u1,sigma ... K_um,sigma)
        = sum_{F(x)=x} 1 / abs(1-F'(x)) + O(sigma^2).

- The exact closed-path action is one half of the squared deterministic
  residual. Its Jacobian satisfies
  `abs(det J) = abs(1-F'(x))`, which gives the orbit weight after the Gaussian
  volume and row normalizers cancel.
- The expansion is uniform under quantitative interiority and nondegeneracy.
  Parameter derivatives contain a delayed term of the form
  `sigma^(-N) exp(-Gamma/sigma^2)`, explaining severe finite-noise crossover.
- The directed three-step trace and the parity-compatible directed six-step
  trace both have deterministic ordered periodic-orbit limits.
- At `u_c = 1.543689012692`, the deterministic targets are
  `-1.7114657240e-5` and `0.004290861044`; both are nonzero.
- Three-step trace and orientation errors recover powers `2.00071` and
  `2.00222`. The six-step trace is strongly nonmonotone but returns toward its
  predicted target and correct sign by `sigma = 0.004`.
- A fixed-`sigma=0.004` resolution audit through full dimension `15360` shows
  that the residual six-step discrepancy is a noise effect, not grid error.
- The theorem is fixed-length. It does not prove a uniform long-cycle or full
  deterministic Fredholm-determinant limit.

## Reproduction

Create an environment and install the dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run the unit tests:

```bash
.venv/bin/python -m pytest -q
```

Regenerate every numerical table and figure:

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=16 \
  .venv/bin/python experiments/run_small_noise_localization.py
```

The last command uses dense matrices through folded dimension `7680`; it is
intended for a high-memory machine. The tests themselves are lightweight.

Build the manuscript:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

## Files

- `main.tex` and `references.bib`: manuscript source and bibliography
- `small-noise-cycle-localization.pdf`: verified compiled manuscript
- `src/small_noise_cycles`: deterministic roots, action geometry, and folded
  Gaussian matrices
- `experiments/run_small_noise_localization.py`: complete numerical audit
- `results`: machine-readable CSV and JSON results
- `figures`: publication PDF and PNG figures
- `tests`: fixed-point, Jacobian, action-gradient, trace, and orientation tests
