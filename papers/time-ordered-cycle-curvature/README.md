# Time-ordered cycle curvature

This directory contains the eighth-layer theory paper in the prime-dynamics
program:

> *Time-Ordered Cycle Curvature for Gaussian Quadratic Markov Cocycles:
> Two-Step Spectral Blindness, Commutator Response, and Parity-Compatible
> Directed Traces*

## Main results

- Every two-step product `K_a K_b` is trace class, but `K_a K_b` and
  `K_b K_a` have exactly the same nonzero spectrum and Fredholm determinant.
  Raw two-step eigenvalues therefore cannot detect reversal within a pair.
- Order remains visible outside the eigenvalues:
  `K_(u-e) K_(u+e) - K_(u+e) K_(u-e) = 2e [K,K'] + O(e^3)`.
  The stationary laws and separating state--observable expectations have
  corresponding first-order responses.
- For `u_n = u_c + kappa/(log(n+c))^p`, the paired commutator corrections are
  summable but have the renormalized operator tail
  `(log(2J+c))^p E_J -> -(kappa/4)[K_c,K_c']`.
- The minimal scalar directed trace needs three parameter values:
  `Omega_A(a,b,c) = tr(A_a[A_b,A_c])`. It factors exactly by the Vandermonde
  polynomial, with diagonal quotient
  `chi_A = (1/2) tr(A[A',A''])`.
- Applying the construction to the frozen parity block `Q_u=K_u^2` produces
  the minimal parity-compatible scalar, a six-step directed trace.
- At three macroscopic logarithmic times the scalar orientation scale is
  `(log T)^(-3p-3)`. Consecutive directed traces are
  `O(n^(-3)(log n)^(-3p-3))` and are absolutely summable.
- Both one-step and parity-block curvatures converge under midpoint
  discretization as `d^(-2)`.

The paper is a negative and positive gate: the route through raw paired
eigenphases closes, while a precise commutator and directed-determinant route
remains. No Riemann zero or arithmetic target is loaded.

## Reproduction

Create an environment and install the dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run the tests and regenerate every table and figure:

```bash
.venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python experiments/run_temporal_orientation.py
```

Build the manuscript:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

## Files

- `main.tex` and `references.bib`: manuscript source and bibliography
- `time-ordered-cycle-curvature.pdf`: verified compiled manuscript
- `src/temporal_spectrum`: tested operator and orientation utilities
- `experiments/run_temporal_orientation.py`: complete numerical audit
- `results`: machine-readable CSV and JSON output
- `figures`: publication PDF and PNG figures
- `tests`: spectral-blindness, commutator, curvature, and schedule tests
