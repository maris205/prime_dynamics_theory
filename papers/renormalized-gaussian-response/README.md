# Renormalized Spectral Response of Gaussian Quadratic Transfer Matrices

This directory contains the fifth-layer theory paper in the prime-dynamics
program, together with tested sparse code and reproducible benchmark data.

## Main results

- Exact first- and second-parameter derivatives are derived for the
  row-normalized Gaussian quadratic kernel.
- Hard Gaussian truncation has the exact rowwise error
  norm equal to twice the omitted probability mass.
- For an unanchored logarithmic drive, arbitrary bounded source-occupation
  weights with positive time density preserve the universal first response.
- For an endpoint-anchored drive, the first surviving response depends on a
  rowwise logarithmic-age moment and is generally not the unweighted response.
- A finite-state non-autonomous Markov estimator inherits the unanchored
  response in probability once every source state has positive occupation
  density.
- Fixed physical Gaussian width gives second-order midpoint convergence but
  quadratic storage growth. Cell-scaled width gives linear storage while
  changing the limiting operator and the response topology.
- Sparse benchmarks through dimension 50,000 validate stochastic row sums,
  analytic eigenvalue response, truncation control, and second-order
  resolution convergence.

The paper makes no claim that the computed Markov resonances are Riemann
zeros, quantum energies, or the spectrum of a Hilbert--Polya operator.

## Reproduction

Create an environment from requirements.txt, then run:

    python -m pytest -q
    PYTHONPATH=src python experiments/run_schedule_scaling.py
    PYTHONPATH=src python experiments/run_operator_benchmarks.py \
      --dimensions 2000 5000 10000 20000 50000
    PYTHONPATH=src python experiments/plot_operator_benchmarks.py

The benchmark was run with a fixed physical width sigma = 0.00785, critical
parameter u_c = 1.5437, and a six-sigma fixed support.
The width is inherited from earlier target-informed exploratory scans; no
Riemann zero is loaded, fitted, or compared in the present benchmark, and the
width is not presented as a target-independent prediction.

## Files

- main.tex: manuscript source
- references.bib: bibliography
- src/gaussian_response: tested sparse operator implementation
- experiments: benchmark and figure scripts
- tests: derivative, truncation, normalization, and schedule tests
- results: machine-readable CSV and JSON outputs
- figures: publication figures
