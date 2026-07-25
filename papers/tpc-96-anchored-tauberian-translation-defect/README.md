# TPC-96: Anchored logarithmic primitives on translated fibers

Paper title:

> *Anchored Logarithmic Primitives on Translated Fibers: Exact
> Tauberian Defects, Uniformity Regimes, and the Literal Reassembly
> Gate*

## Main results

For

\[
S_N=\sum_{n\le N}a_n,\qquad
L_{r,N}=\sum_{n\le N}\frac{a_n}{r+n},
\]

the exact translated Tauberian identity is

\[
\frac{S_N}{N}
=
\left(1+\frac rN\right)L_{r,N}
-\frac1N\sum_{m<N}L_{r,m}.
\]

Thus the correct signed defect contains the anchor term
\((r/N)L_{r,N}\). It cannot be replaced by the unshifted Cesaro
defect after translating a physical affine fiber.

The paper proves:

- the exact terminal criterion
  \((r/N)L_{r,N}=o(1)\) once the unshifted signed defect is
  \(o(1)\), with its regime-specific corollaries;
- a prefix-uniform relative logarithmic criterion for \(r\ge N\);
- exact counterexamples showing that \(L_{r,N}=o(1)\) and an
  anchor-free defect can coexist with \(S_N/N=1\);
- an outer-mass counterexample showing that per-fiber \(o(1)\) need
  not aggregate;
- the exact literal packet identity

  \[
  Z_X=\sum_\theta c_{\theta,X}N_{\theta,X}
  \mathcal T_{\rho_{\theta,X},N_{\theta,X}}(L_{\theta,X})
  +E_{\mathrm{ret},X};
  \]

- the corresponding quantitative zero-mode certificate with all
  origins, prefixes, native keys, masks, polarizations, and outer
  weights retained.

## Scope

The identities and counterexamples are `L0`. Attaching them to a
complete exported native packet is an `L1` certificate. The paper
does not prove a uniform anchored-defect estimate for the growing
fixed-\(h0\) affine Mobius family and therefore supplies no new `L2`
arithmetic saving.

The determinant condition `lambda_D <= 2 eta_Z` and the strict
physical ledger `Lambda_phys < 1/400` remain independent. No shift is
specialized to 2.

## Files

- `main.tex` and `sections/*.tex`: source.
- `references.bib`: bibliography.
- `anchored-tauberian-translation-defect.pdf`: compiled paper.

## Compile

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
