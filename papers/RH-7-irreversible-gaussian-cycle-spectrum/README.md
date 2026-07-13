# Irreversible resonance geometry and centered cycle spectrum

This directory contains the seventh-layer theory paper in the prime-dynamics
program:

> *Irreversible Resonance Geometry of Gaussian Quadratic Markov Operators:
> Exact Folding, Dobrushin Enclosures, and Centered Cycle Determinants*

## Main results

- The full Gaussian quadratic operator maps every observable to an even
  function. Folding `y` and `-y` gives an operator on `[0,1]` with exactly the
  same nonzero spectrum and generalized eigenspaces.
- The oriented three-cycle affinity is
  `u (x-y)(y-z)(z-x) / sigma^2`. The chain is reversible exactly at `u=0`, so
  for `u != 0` it has no self-adjoint realization obtained from a positive
  stationary weight.
- The one-step Dobrushin coefficient is an explicit endpoint
  truncated-normal distance. The roots of the multistep coefficients converge
  to the non-Perron spectral radius.
- After subtracting the stationary rank-one projector, the operator is
  Hilbert--Schmidt. Its trace-class powers give centered cycle moments
  `c_n = tr(K^n)-1 = sum_j lambda_j^n` for `n >= 2`.
- These moments generate `det_2(I-zN)`, whose zeros are reciprocal Markov
  resonances. Their exact parameter derivatives are cyclic score integrals and
  remain analytic through eigenvalue collisions.
- Midpoint traces and trace derivatives converge as `d^(-2)`. The numerical
  slopes for orders two through six lie between `-1.97` and `-2.01`.
- At the algebraic band-merging parameter, the leading negative resonance is
  the finite-noise remnant of the deterministic parity mode. This last
  interpretation is numerical evidence, not a small-noise theorem.

No Riemann zeros or target-fitted arithmetic scales are loaded. The centered
determinant is a nonself-adjoint Markov determinant, not a Hilbert--Polya
operator.

## Reproduction

Create an environment and install the pinned lower-bound dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run the tests and regenerate all tables and figures:

```bash
.venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python experiments/run_intrinsic_spectrum.py
```

Build the manuscript:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

## Files

- `main.tex` and `references.bib`: manuscript source and bibliography
- `irreversible-gaussian-cycle-spectrum.pdf`: verified compiled manuscript
- `src/cycle_spectrum`: tested folding, affinity, trace, and contraction code
- `experiments/run_intrinsic_spectrum.py`: complete numerical audit
- `results`: machine-readable CSV and JSON output
- `figures`: publication PDF and PNG figures
- `tests`: normalization, folding, affinity, Dobrushin, and trace tests
