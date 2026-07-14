# TPC-13: Radial completion of factor-ray dynamics

**Paper:** *Radial Completion of Factor-Ray Dynamics: A GCD--Mellin
Joint Spectrum, Exact Anisotropic Dephasing, and the Fixed-Shift
Boundary*

This paper adds the radial coordinate lost by the ratio-only factor-ray
transform:

\[
(n/m)^{it}\quad\longmapsto\quad
(n/m)^{it}(m,n)^{is}.
\]

With \(n=ak\), \(m=bk\), \((a,b)=1\), the joint frequency is
\((\log(a/b),\log k)\), which uniquely labels every factor pair. This is
a direct ray-adapted coordinate, not more information than TPC-10's full
ratio--product two-Mellin continuum.

## Main results

- An exact commuting two-parameter unitary representation of the factor
  coordinates.
- On \(R\le ab<2R\), explicit uniform ray and radial gaps.
- Exact tensor-Fejer coefficient recovery and Parseval dephasing at the
  separate Fejer scale parameters
  \[
  T_{\rm ray}\asymp R,\qquad
  T_{\rm rad}\asymp\sqrt{X/R}.
  \]
- A tensor Montgomery--Vaughan hard-rectangle estimate with an explicit
  anisotropic error. Hard rectangles are asymptotic only when both side
  lengths exceed their reciprocal-gap scales by unbounded factors.
- For \(X^{2/15+\varepsilon}\le H\le X\) and
  \(D\le X^{1-\eta}\),
  \[
  \sum_hG(h/H)\mathcal F_{h,D}(X)
  =
  \frac12HX I_0(G)I_2(W)\log X
  \bigl((\log X)^2-(\log D)^2\bigr)
  +O(HX\log^2X).
  \]
  This is the fully radial diagonal energy. The \(\log\log X\) loss in
  TPC-12 disappears because the new observable has no same-ray
  \(k\ne\ell\) cross terms.
- The parity-centered even-shift ensemble has coefficient \(1/4\).
- The fixed \(m=1\) endpoint energy is equivalent at natural precision
  to a weighted Hardy--Littlewood prime-pair correlation. At \(h=2\)
  this is the weighted twin-prime Hardy--Littlewood asymptotic, which is
  strictly stronger than mere infinitude of twin primes.
- The completed \((6,1)\) ray at \(h=1\) is equivalent at natural
  precision to a weighted prime number theorem for \(6k^2+1\).
- An exact minimax theorem shows that retaining only total radial energy
  again loses the endpoint label, despite injectivity of the full joint
  signal.

The paper does **not** prove a fixed-shift prime-pair asymptotic, a
twin-prime lower bound, a fixed quadratic-prime theorem, a new level of
distribution, or a breach of sieve parity.

## Reproduction

From this directory:

    pdflatex main.tex
    bibtex main
    pdflatex main.tex
    pdflatex main.tex
    python experiments/radial_mellin_certificate.py
    python -m unittest experiments.test_radial_mellin_certificate

The finite certificate checks only exact algebra, frequency gaps,
Fourier-side Fejer dephasing, product-center regrouping, and the minimax
witnesses. It is not evidence for a fixed-shift prime conjecture.

## Files

- main.tex and sections/: paper source.
- references.bib: bibliography.
- radial-mellin-completion.pdf: compiled paper.
- experiments/: deterministic certificate and unit tests.
