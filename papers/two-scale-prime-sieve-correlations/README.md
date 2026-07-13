# Two-Scale Correlations in Finite Prime-Sieve Dynamics

This directory contains the source and compiled PDF for the fifth-layer theory paper in the prime-dynamics program.

## Main results

- Over one primorial period, the finite sieve has the exact classical correlation
  \[
  C_y(\mathcal H)=\prod_{p\le y}\left(1-\frac{\nu_p(\mathcal H)}p\right),
  \]
  and `C_y(H) / rho_y^r` converges to the Hardy-Littlewood singular series.
- The same limit holds on growing windows whenever `P_y = o(X rho_y^r)`; in particular, it holds for `y <= (1-delta) log X`.
- Centered, energy-normalized spectral measures converge weakly to Haar measure, while rare-event pair normalization retains the singular-series factor. At displacement two,
  \[
  C_y(2)/\rho_y^2\to 2C_2.
  \]
- A diagonal-renormalized spectral family converges in the distribution space `D'(T)` to an object whose nonzero Fourier coefficients are the pair singular series. The limit is not a finite signed measure.
- Hamming repair has two distinct scales: `epsilon = o(rho_y)` preserves the ordinary centered spectrum, while uniform preservation of an `r`-point rare-event limit is guaranteed by `epsilon = o(rho_y^r)`.
- For pairs, the `rho_y^2` scale is worst-case sharp: a perturbation of that order can remove a chosen pair correlation while preserving the Haar spectral limit.
- The exact composite-survivor remainder isolates the missing survivor-to-prime estimate. At `y = sqrt(X + max H)` the sieve is primality-exact, but the primorial period is exponentially larger than the observation window.

## Scope

The paper does **not** prove a lower bound for twin primes, does not improve the bounded-prime-gap constant, and does not overcome the parity problem. The CRT product, the occurrence of `2C_2`, and the Ramanujan coefficients are classical local facts. The new contribution is their two-scale dynamical formulation, the distributional spectral limit, the repair-stability hierarchy, and an explicit normalization of the remaining prime-sensitive gap. The open benchmarks are Hardy--Littlewood-order restatements, not independently easier estimates.

## Files

- `main.tex` - manuscript source
- `references.bib` - bibliography
- `two-scale-prime-sieve-correlations.pdf` - compiled manuscript

## Build

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
