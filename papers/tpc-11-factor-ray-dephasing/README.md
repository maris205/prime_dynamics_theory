# TPC-11 — Factor-Ray Dephasing of a Prime-Target Residual

This paper studies the continuum Mellin-frequency target proposed at the end
of TPC-10. It groups factor pairs `n = ak`, `m = bk`, `(a,b)=1`, into primitive
ratio rays and separates three logically different levels.

## Main results

- For every prescribed fixed integer shift, Montgomery–Vaughan's continuous
  mean-value theorem reduces the band mean square to the exact ray energy,
  with geometric resolution loss `O(X)`.
- The fixed-shift ray energy is bounded by `O(X log^4 X)`, giving
  density-one cancellation over sufficiently long Mellin intervals. This
  does not select any prescribed frequency.
- A compact-Fourier-support Fejér kernel removes distinct rays exactly at
  bandwidth `T` of order `X`.
- After squaring first and averaging shifts over `H >= X`, the ray energy has
  an unconditional asymptotic with explicit main term. Same-ray
  off-diagonals require only a Selberg upper-bound sieve.
- Determinant layers describe the unresolved mesoscopic band. A smooth
  endpoint selector proves that an absolute `o(X^2)` fixed-shift band error,
  together with a compatible filtered model and `o(X)` Fourier tails, would
  already recover a weighted Hardy–Littlewood endpoint.

The paper does **not** prove a fixed-shift prime-pair asymptotic, a twin-prime
lower bound, a new level of distribution, or a breach of the sieve parity
barrier.

## Build

```powershell
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Reproducibility certificate

The deterministic experiment checks only the finite ray identities and
geometric selectors:

```powershell
python experiments/factor_ray_certificate.py
python -m unittest experiments.test_factor_ray_certificate
```

It uses only the Python standard library. The saved JSON output is
`experiments/data/factor-ray-certificate.json`.
