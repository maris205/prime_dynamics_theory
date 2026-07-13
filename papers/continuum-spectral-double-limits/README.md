# Continuum Spectral Convergence and Time--Resolution Windows

This directory contains the sixth-layer theory paper in the prime-dynamics
program. It promotes the fixed-dimensional Gaussian response theory to a
compact continuum operator and separates deterministic, weak-observable, and
strong-matrix double limits.

## Main results

- The fixed-width normalized Gaussian quadratic kernel defines a compact,
  strongly positive, analytic Markov family on continuous observables.
- Midpoint Nystrom operators converge collectively compactly. Every nonzero
  isolated resonance is spectrally exact, and a simple resonance, its
  projector, and its parameter derivative converge at second order.
- A logarithmically renormalized deterministic spectral response survives a
  joint limit whenever the midpoint bias is smaller than the response scale.
- Full-probability propagation has no Monte Carlo upper restriction. A weak
  observable estimated from one row has error of order sqrt(d/T), whereas a
  full empirical row in total variation has error of order d/sqrt(T).
- For response scale s_T = (log T)^(-p), the leading windows are

      (log T)^(p/2) << d(T) << T/(log T)^(2p)          weak observable
      (log T)^(p/2) << d(T) << sqrt(T)/(log T)^p       strong matrix

- The numerical experiments recover dimension exponents 0.4827 and 1.0046
  for the weak and strong errors, respectively.

No continuum Markov resonance is identified with a Riemann zero or a
self-adjoint energy.

## Reproduction

    python -m pytest -q
    PYTHONPATH=src python experiments/run_sampling_scaling.py
    python experiments/analyze_spectral_convergence.py

The spectral extrapolation reuses the machine-readable fixed-width benchmark
from the preceding renormalized Gaussian response paper in this repository.
The inherited sigma = 0.00785 benchmark is historically target-informed and
is not presented as a target-independent arithmetic prediction.

## Files

- main.tex: manuscript source
- references.bib: bibliography
- src/continuum_limits: sampling and double-limit utilities
- experiments: sampling and spectral extrapolation scripts
- results: machine-readable outputs
- figures: publication figures
- tests: stochastic-row and window tests
