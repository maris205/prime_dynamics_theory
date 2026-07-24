# TPC-91 - Overlap-Corrected Full-Block Cover

Paper title:

> *Overlap-Corrected Full-Block Cover Certificates: Incidence
> Geometry, Dual Obstructions, and the TPC-18 Interface*

## Main results

- Models the actual physical atoms and exact candidate block
  coefficients by a weighted incidence matrix `B`. The identity
  `B c = w` is a sufficient zero-remainder certificate; bounded
  overlap is only a support diagnostic.
- Proves the exact unrestricted residual and dual certificate
  `||(I-BB^dagger)w||_2`.
- Gives the nonnegative Farkas alternative and the exact cone-distance
  dual formula. Convex coefficient rules whose attainable images are
  closed have an analogous support-function formula.
- Constructs a disjoint full-support family with overlap one whose
  relative least-squares defect is exactly `1/sqrt(10)` for every
  size. Thus bounded overlap does not imply even asymptotic coverage.
- Constructs a two-column system with a signed exact cover but no
  nonnegative cover; its cone distance is exactly `1/sqrt(2)`.
- Proves that a cover after collapsing native determinant keys need
  not lift to a literal cover.
- Records least-squares conditioning, residual stability, and the
  exact coefficient-amplification cost under the original global
  normalization.
- Shows why an approximate Euclidean cover leaves an independent
  physical remainder and cannot replace an exact cover without a new
  theorem.
- Separates that exact route from the original TPC-18 asymptotic
  route, which may also close if the prescribed residual has physical
  image `o(X)`.

## TPC status

This is an exact `L0` linear-algebra result and an `L1` certificate
schema for the zero-remainder route through the TPC-18 all-block
interface. It does **not** construct the full physical incidence
system, prove a controlled-residual theorem, or close the original
asymptotic TPC-18 representation.

The following gates remain independent:

- literal exact cover: `w in B C` (equivalently `eps_cov = 0` for a
  closed attainable image), or a separate controlled physical
  residual theorem for the asymptotic route;
- TPC-18 primitive generic determinant dispersion;
- post-bin determinant/zero-mode ledger: `lambda_D <= 2 eta_Z`;
- strict physical loss: `Lambda_phys < 1/400`.

Equality or excess in the physical-loss ledger is a stop condition.
The same loss is never charged twice.

All statements retain one prescribed nonzero `h0`, the actual support,
native keys, and the original global normalization. Nothing is
specialized to `h0 = 2`. The paper proves no fixed-shift
Hardy-Littlewood asymptotic, parity breakthrough, prime-pair lower
bound, or twin-prime consequence.

## Files

- `main.tex` and `sections/*.tex`: source.
- `references.bib`: bibliography.
- `overlap-corrected-full-block-cover.pdf`: compiled paper.

## Compile

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
