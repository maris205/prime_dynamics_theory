# TPC-67: Determinant Mass on the Actual Collision Core

This paper opens a determinant route for the literal full-output synthesis
matrix identified in TPC-65 and TPC-66.

## Main results

- Iterative two-sided degree-one peeling factors every exposed pivot exactly.
  A residual core without a perfect matching has zero determinant.
- Conditional on a declared core matching, the remaining determinant is an
  exact sum over vertex-disjoint alternating-cycle families. Diagonal gauge
  removes forest phases and leaves only cycle holonomies.
- If
  \[
  \mathcal A_\phi=\operatorname{per}(I+|E_\phi|)-1,
  \]
  then every certified minor satisfies
  \[
  |\det T|
  \ge
  P_{\mathrm{for}}P_\phi(1-\mathcal A_\phi)_+.
  \]
  The threshold one is sharp for this phase-uniform certificate.
- For a matrix \(B\) with \(r\) unit columns and \(K=B^*B\),
  \[
  \mathfrak D(B)=\sum_{|I|=r}|\det B[I]|^2=\det K,
  \qquad
  \lambda_{\min}(K)
  \ge
  \left(\frac{r-1}{r}\right)^{r-1}\mathfrak D(B)
  \ge e^{-1}\mathfrak D(B)
  \]
  for \(r\ge2\), with constant one for \(r=1\). The fixed-dimensional
  constant is sharp.
- The literal full-support collision components are orthogonal blocks, so
  \[
  \beta_X=\min_C\beta_C,
  \qquad
  \beta_X\ge e^{-1}\min_C\mathfrak D_C.
  \]
  This avoids an irrelevant product over mutually orthogonal components.
- A connected path-Gram countermodel has a uniform true gap but exponentially
  small determinant mass. Determinant decay alone therefore does not imply a
  small spectral gap.

## Claim boundary

The finite-dimensional determinant, rank, component, and spectral conversions
are L0. Identifying the matrix and all of its coordinates with the literal
fixed-\(h_0\) carrier is L1.

The paper does **not** prove an L2 polynomial lower bound for the worst actual
component determinant mass or certified-minor mass. It also does not prove a
signed-reassembly gain, parity improvement, fixed-\(2\) estimate, or
prime-pair lower bound.

## Files

- `main.tex` and `sections/`: LaTeX source
- `references.bib`: bibliography
- `actual-collision-core-determinant-mass.pdf`: compiled paper
