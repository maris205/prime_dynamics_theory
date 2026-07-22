# TPC-62: Exact Closure Alternatives for a Fixed-Shift Prime Packet

This paper consolidates the TPC-53--TPC-61 fixed-shift interfaces into a
quantifier-safe decision calculus.  Its purpose is to determine which arrows
are exact, which are only sufficient certificates, and which arithmetic
inputs remain genuinely open.

## Main results

- The optimal full-coefficient-space uniform transfer constant from a nonzero
  semidefinite parent form `R` through a final map `F` is an exact
  shorted-Gram eigenvalue.  At each finite scale it is positive exactly when
  `ker(F)` is contained in `ker(R)`.
- Shorting is transitive on nested retained subspaces.  Sequential exact
  nuisance elimination therefore agrees with one master shorting, while
  ordinary compression can create false positive lower bounds.
- Mandatory operator kernels are separated from failed sufficient
  certificates: an actual parent-visible kernel vector kills every final map
  that genuinely factors through that mandatory operator.
- Adaptive selector bounds and frozen-selector bounds have different
  quantifier order.  Retaining all labels by orthogonal direct sum gives an
  exact uniformized map, but erasing those labels is a new reassembly gate.
- The exact shorted reassembly constant dominates reverse-triangle
  certificates.  The restricted native missing Gram dominates both the
  residual-factor and ambient-degree relaxations; those two coarse routes are
  generally incomparable.
- A large missing-alias eigenvalue must leave a row, literal collision-cell,
  and pair/star witness.  Consequently, active row degree
  `X^(delta+o(1))` together with a uniform pair bound
  `X^(-tau+o(1))` yields the deterministic Gram exponent bound
  `nu_M <= (delta-tau)_+`.
- A compatible represented/reassembly/downstream chain closes conditionally
  only when all three bounds concern the same carrier and quantifier scope;
  their fixed-power losses are charged once and must total strictly less than
  `1/400`.

## Arithmetic boundary

The matrix theorems are finite-dimensional L0 results.  Their identification
with the literal TPC-61 two-affine Mobius/determinant entries is an L1
interface.  The paper does **not** prove a favorable pair-correlation bound,
subpower alias norm, fixed-shift parity improvement, prime-pair lower bound,
or twin-prime consequence.

The inherited residual window `39671/210000` is only a conditional test for
zero-cost reassembly; it is not an additive endpoint loss.  Likewise,
`lambda_rep` may enter that test and also belong to the represented-chain
accounting, but it is charged only once in the final strict `1/400` ledger.
The direct ambient gap `67/200` closes only the coarse ambient-degree route.

The next arithmetic alternatives are explicit: prove physical cofactor
exposure and represented transfer on the same carrier, then either control
the localized alias degree/correlation, estimate the exact shorted Gram, or
exhibit a kernel/cell obstruction that rigorously closes that route.

## Build

From this directory, run:

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archived paper is `exact-closure-fixed-shift-alias-obstructions.pdf`.
