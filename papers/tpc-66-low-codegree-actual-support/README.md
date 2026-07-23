# TPC-66: Actual Exposure and Low Pair Codegree

This paper opens the literal row geometry of the activated fixed-shift
residual Gram from TPC-65.

## Main results

- A fixed physical row contributes at most one terminal atom to a fixed
  residual output key. After normalization, every active row column therefore
  has Gram diagonal exactly one.
- For two distinct literal rows, factor exchange and simultaneous CRT give
  \[
  c^{\mathrm{red}}_{m_1,m_2}(R)
  \ll X^{o(1)}\left(1+\frac{J}{R}\right).
  \]
  Hence the reduced pair codegree is \(X^{o(1)}\) on the critical block
  \(R\asymp J\), although a right fiber may still contain polynomially many
  rows.
- The decorated Gram obeys the exact codegree--diffuseness bridge
  \[
  |K_X(m,n)|
  \le C^{\mathrm{red}}_{m,n}(R)
      \sqrt{\rho_m(R)\rho_n(R)}.
  \]
- Private output energy, comparison matrices, weighted diagonal dominance,
  forest gauges, star spectra, and unique-matching minors give rigorous
  finite-dimensional lower-frame certificates.
- A cycle model with fixed supports, degrees, codegrees, and entry magnitudes
  can be singular or nonsingular according only to its holonomy phase. Thus
  pair sparsity alone is not a physical lower-frame theorem.

## Claim boundary

The row singleton, factor-exchange summation, CRT spacing, divisor thinning,
and critical reduced-codegree bound are L1 statements on one literal fixed
nonzero-shift carrier. The general matrix results are L0.

The paper does **not** prove row activation, polynomial energy diffuseness, a
physical smallest-singular-value bound, signed reassembly cancellation, a
parity improvement, or a prime-pair lower bound. The shift is not specialized
to \(2\).

## Files

- `main.tex` and `sections/`: LaTeX source
- `references.bib`: bibliography
- `actual-exposure-low-codegree.pdf`: compiled paper
