# Spectral Obstructions and Renormalized Limits for Quadratic Models of Riemann-Zero Statistics

This directory contains the source and compiled PDF for the fourth-layer theory paper in the prime-dynamics program.

## Main results

- The empirical pair-occupation matrix is distinguished from its row-normalized conditional transition estimator; the two generally have different spectra.
- Sorted upper-half-plane phase unwrapping telescopes exactly and adds no winding information.
- Regression on conjugate pairs `(phi, gamma)` and `(-phi, -gamma)` forces the fitted intercept to zero.
- The unconditional Riemann-von Mangoldt formula gives
  \[
  \gamma_n=\frac{2\pi n}{W(n/e)}+O(1),
  \]
  so raw relative error and Pearson correlation can be asymptotically excellent without encoding zero fluctuations.
- A fixed-resolution logarithmic operator average freezes at the critical operator. Under differentiability,
  \[
  (\log T)^p(\overline A_T-A(u_c))\to\kappa A'(u_c).
  \]
  Endpoint anchoring cancels the leading average and shifts the response to order `(log T)^(-p-1)`.
- The area-preserving Henon recurrence is exactly symplectic and reversible and admits a direct unitary Fourier-integral quantization.
- The quartic confining Hamiltonian has `N_H(E) ~ C E^(3/4)`, which is incompatible with `N_zeta(T) ~ T log T` under every fixed affine energy rescaling.

## Scope

The paper neither assumes nor proves the Riemann hypothesis and does not construct a Hilbert-Polya operator. The finite-dimensional Gaussian-kernel results are rigorous for the displayed matrix family. Continuum transfer-operator and single-orbit empirical applications require the additional uniform estimates stated in the paper.

## Files

- `main.tex` - manuscript source
- `references.bib` - bibliography
- `spectral-obstructions-renormalized-limits.pdf` - compiled manuscript

## Build

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
