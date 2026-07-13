# Low-conductor suppression and power-short rough boxes

This directory contains the manuscript and exact finite certificates for the
next paper in the centered local-sieve-kernel branch.

## Rigorous scope

For the squarefree product `Q` of primes in `(w, w^2]`, the paper combines the
exact conductor multipliers of the centered CRT pair kernel with classical
Polya--Vinogradov and Burgess character-sum bounds. It proves:

- normalized complete fully-active-shift RMS cancellation for interval boxes
  of length `L = ceil(Q^(1-eta))` for every fixed `0 < eta < 1`;
- the same result on `H = floor(Q^(1/log w))` consecutive shift parameters;
- fixed local-shift cancellation at `h = 2` for every fixed
  `0 < eta < 4/5`;
- an exact nonnegative shifted-divisor Selberg-form square whose nonconstant
  Fourier spectrum lies only on two-prime conductors.

The character-sum reduction and Burgess theorem are classical. The paper's
contribution is their conductor-by-conductor aggregation against this exact
finite pair kernel and the resulting explicit power-short ranges.

The paper contains no von Mangoldt weight, no prime-sensitive Type-II
estimate, no prime-pair lower bound, and no implication toward the twin-prime
conjecture. The strict exponents above are method ranges, not claimed
barriers or endpoints.

## Files

- `main.tex` and `sections/` -- manuscript source
- `references.bib` -- bibliography
- `experiments/` -- pure integer/rational reference implementation and tests
- `low-conductor-power-short-rough-boxes.pdf` -- compiled manuscript

## Build

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Test

From `experiments/`:

```bash
python exact_diagnostics.py --output data/exact-certificate.json
python -m unittest -v test_exact_diagnostics.py
```
