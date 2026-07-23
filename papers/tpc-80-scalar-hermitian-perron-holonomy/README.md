# TPC-80: Scalar Hermitian Perron saturation

This paper classifies exactly when a scalar Hermitian carrier saturates
an entrywise nonnegative Perron majorant.

For a connected symmetric nonnegative matrix `P` and Hermitian `H`
with `|H| <= P`, it proves that

```text
||H|| = rho(P)
```

iff, for one of the two extremal sectors `sigma = +/-1`,

```text
|H| = P,  H = sigma D P D*
```

for a diagonal unitary `D`.

In the saturated case, this is equivalent to a cycle-holonomy
condition. Trees have no phase-frustration saving; in the saturated
case `P = |H|`, genuine phase-frustration strictness requires both the
positive and negative sectors to contain defective cycles. The paper
supplies:

- an exact Perron-weighted sum-of-squares identity;
- switching and fundamental-cycle classification;
- quantitative weighted upper and lower defect bounds;
- the exact flux spectrum of a cycle;
- reducible-component and amplitude/phase gap decompositions;
- explicit scalar/block and incidence/row-graph stop rules.

These are exact L0 spectral-algebra results advancing an L1 operator
interface. They do not exhibit a nontrivial holonomy on a growing
literal fixed-shift carrier or prove an arithmetic exponent gain.

Build with:

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
