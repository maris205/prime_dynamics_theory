# TPC-92: Ten-paper mass--cancellation--cover audit

Paper title:

> *A Ten-Paper Mass--Cancellation--Cover Audit: Exact Closures,
> Independent Arithmetic Gates, and a Stop/Go Roadmap*

## Main results

- Audits TPC-83 through TPC-91 paper by paper and classifies every
  result as `L0` interface algebra, `L1` model/certificate progress,
  or `L2` progress on the literal growing fixed-shift coefficient.
- Records the exact advances on post-bin mass and determinant energy,
  equal-determinant coherence, zero-mode reassembly, the sharp
  logarithmic Tauberian gap, mass--cancellation factorization,
  principal-angle surrogate transfer, primitive affine local
  obstructions, and full-block incidence certificates.
- Separates five remaining gates: post-bin mass/energy, literal
  zero-mode cancellation, TPC-18 full-block reassembly, primitive
  determinant dispersion, and the strict physical loss budget.
- Distinguishes the stronger zero-residual certificate `B c = w`
  from the original TPC-18 alternative with a separately controlled
  physical remainder.
- Proves at the audit level that reassembly and primitive determinant
  dispersion are independent requirements; neither may be inferred
  from the other.
- Keeps the determinant compatibility
  `lambda_D <= 2 eta_Z` separate from the strict physical endpoint
  `Lambda_phys < 1/400`. Determinant equality has no reserve; physical
  equality is a stop condition.
- Gives explicit stop/go tests and a four-priority continuation:
  low-frequency/log-Tauberian/surrogate transfer, post-bin
  mass/energy, primitive affine arithmetic, and literal full-block
  reassembly.

## TPC status

This paper is a rigorous synthesis and route audit. It identifies
exact closures and sharp barriers, but supplies no new `L2` estimate
for the literal growing fixed-`h0` arithmetic coefficient.

All statements preserve one prescribed nonzero `h0`, the actual
support, native keys, masks, relevant prefixes, and the original
global normalization. No result is specialized to `h0 = 2`.

The paper proves no fixed-shift Hardy--Littlewood asymptotic, parity
breakthrough, prime-pair lower bound, twin-prime consequence, or
Riemann-hypothesis consequence.

## Files

- `main.tex` and `sections/*.tex`: source.
- `references.bib`: bibliography.
- `ten-paper-mass-cancellation-cover-audit.pdf`: compiled paper.

## Compile

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
