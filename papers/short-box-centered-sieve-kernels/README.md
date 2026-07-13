# Centered local sieve kernels and subperiod shift means

This directory contains the manuscript and reproducible reference experiments
for the next paper in the rough-pair/parity branch.

## Rigorous scope

The paper proves finite and asymptotic statements for a centered local sieve
kernel on unit factor boxes:

- the exact character and conductor decomposition for general even shifts;
- a discrepancy-product bound for fixed subperiod factor boxes;
- an exact complete-shift Parseval identity;
- a deterministic fully-active subperiod-shift completion estimate with cost
  `kappa^-2 4^omega(Q) + 2 kappa^-1 3^omega(Q) + 2^omega(Q)`;
- a regime in which the factor intervals are
  `Q/(log Q)^(3/4+o(1))` and the shift interval is `Q^o(1)`, while the shift
  root mean square is `o(MN)` for arbitrary bounded coefficients;
- sharp low-conductor and sparse-support obstructions.

The result averages fully active even shifts. It does not reach power-short
factor boxes, estimate the fixed shift `h=2`, contain a von Mangoldt weight,
or give a Type-II estimate for primes or a twin-prime theorem.

## Files

- `main.tex` - manuscript source
- `references.bib` - bibliography
- `experiments/` - exact small-box reference implementation and tests
- `centered-local-sieve-kernels-subperiod-shifts.pdf` - compiled manuscript

## Build

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Test

From the repository root:

```bash
python -m unittest discover \
  -s papers/short-box-centered-sieve-kernels/experiments \
  -p 'test_*.py' -v
```

The numerical singular values are diagnostics for exact finite matrices. They
are not certified asymptotic bounds and are never used to infer a statement
about fixed prime pairs.
