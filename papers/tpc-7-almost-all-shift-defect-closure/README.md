# TPC-7: Almost-all-shift defect closure

This directory contains the seventh paper in the twin-prime-correlation
(`tpc`) theory branch.

## Rigorous scope

TPC-6 isolated the exact large-source-divisor defect

```text
T_{h,>D}(X) = sum_{X<n<=2X} (Lambda(n)-a_D(n)) Lambda(n+h).
```

For a prescribed even shift, proving that this quantity is `o(X)` remains
equivalent to the expected prime-pair asymptotic. This paper changes the
shift quantifier, while retaining the complete defect. It proves:

- a singular-series coefficient estimate uniform for polynomially growing
  shifts;
- a Bombieri--Vinogradov evaluation of the short source-divisor correlation,
  uniform throughout the relevant shift windows;
- after importing the Matomaki--Radziwill--Tao averaged Hardy--Littlewood
  theorem, arbitrary logarithmic decay of the complete TPC-6 defect for all
  but a logarithmically sparse set of shifts in windows
  `X^(8/33+epsilon) <= H <= X^(1-epsilon)`, centered at
  `0 <= h0 <= X^(1-epsilon)`, with
  `D=floor(X^(1/2)/(log X)^B)`;
- fixed-`Lp` shift-density closure for every fixed finite `p`;
- exact translation-matrix-coefficient and Fourier-energy identities for the
  defect correlations;
- a finite-conductor energy-escape theorem: one periodic space of modulus
  `q <= N^(1-delta)` captures only a vanishing fraction of the `L2` energy of
  `Lambda-1`;
- an exact outer divisor slice that exposes a shifted-prime Moebius
  correlation at the fixed-shift boundary.

The exponent `8/33` and the deep almost-all prime-pair theorem are due to
Matomaki, Radziwill, and Tao. The Fourier formulas are identities, not new
cancellation estimates. The paper proves no complete-defect estimate at a
prescribed nonzero even shift, no result for `h=2`, no twin-prime lower bound,
and no new Type-II, dispersion, or level-of-distribution theorem.

## Files

- `main.tex` and `sections/` -- manuscript source
- `references.bib` -- bibliography
- `experiments/` -- deterministic FFT and periodic-projection diagnostics
- `almost-all-shift-prime-pair-defect.pdf` -- compiled manuscript

## Build

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Reproduce the finite certificate

From `experiments/`:

```bash
python defect_shift_diagnostics.py --output data/defect-shift-certificate.json
python -m unittest -v test_defect_shift_diagnostics.py
```

The diagnostic requires Python 3 and NumPy. The committed JSON records the
SHA-256 of its canonical payload (sorted keys and compact JSON separators,
before the hash field is inserted):

```text
6F822312CE0699722A0830F98E91189823F3AB9ABE1F47810340E081AFFDAB30
```

The finite computation validates algebraic and FFT conventions only; it is
not evidence that a specified shift lies outside the analytic exceptional
set.
