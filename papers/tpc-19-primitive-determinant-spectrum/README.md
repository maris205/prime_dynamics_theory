# TPC-19 — Primitive determinant spectrum

This directory contains:

> **Matched-Spectrum Gates in a Primitive Möbius Tail: Exact Determinant–Divisor
> Normal Forms, CRT–Poisson Duality, and a Frequency-Concentration Gate**

TPC-18 leaves a primitive two-row correlation of
\(r_R=\Lambda-\Lambda_R\). TPC-19 turns that opaque remainder into exact
divisor, finite-spectral, and Poisson normal forms. It does **not** prove
the residual dispersion estimate, a fixed-shift Hardy–Littlewood
asymptotic, the twin-prime conjecture, or a breach of sieve parity.

## Main results

- The actual residual has the finite squarefree-divisor identity
  \[
  r_R(n)=-\sum_{\substack{u\mid n\\u\ \mathrm{squarefree}}}
  \mu(u)w_R(u),\qquad w_R(u)>0.
  \]
- In a primitive row pair, writing \(u=ga\), \(v=gb\) removes the common
  Möbius sign and CRT gives the exact determinant condition
  \(g\mid m_1-m_2\).
- Prime and finite-model row densities differ by an explicit
  \(O(L^{-1}X^\varepsilon)\) drift, whose total contribution is
  fixed-power smaller than the \(XQ\) obstruction scale.
- The centered finite-model covariance is
  \[
  \kappa_R(m_1,m_2)=
  \sum_{u,v\le R}\frac{\lambda'_R(u)\lambda'_R(v)}{uv}
  \bigl((u,v)\mathbf1_{(u,v)\mid m_1-m_2}-1\bigr),
  \]
  with the natural primitive coprimality restrictions. Every
  \((u,v)=1\) term vanishes individually.
- The connected factor has the exact nonzero-frequency expansion
  \[
  g\mathbf1_{g\mid\Delta}-1
  =\sum_{0<r<g}e(r\Delta/g).
  \]
- For fixed distinct prime sources, the determinant-difference map is
  injective and its Fourier transform factors into two Möbius
  exponential sums. This isolates a sharp frequency-concentration gate.
- The true periodic orbit modulus is \(H[u,v]\). Smooth Poisson
  completion is exact up to arbitrary power when
  \(H[u,v]\le JX^{-\eta}\); the whole finite model lies in this range
  when \(HR^2\le JX^{-\eta}\). A sufficient strict-margin range is
  \(Q\le X^{2\delta-\eta_0}\): for every fixed
  \(0<\eta<\eta_0\), the completion condition then holds for large
  \(X\) and fixed \(h\).
- The compatible joint residue produces three coupled inverse phases
  of Kloosterman type in the long-lcm range.
- An exact witness gives
  \(\kappa_{12}(93,123)=433/450\). Thus complete-period centering does
  not give rowwise \(MM\) cancellation. A global argument needs either
  extra oscillation over rows or cancellation of matched local spectra.

Two matched-spectrum analytic routes are explicit:

1. a matched four-channel Kuznetsov/dispersion reduction plus sharp
   Möbius frequency concentration; or
2. a joint estimate for the centered long-lcm CRT–Poisson spectrum.

Neither input is claimed here. A separate global estimate exploiting
row-family oscillation is also logically possible, but is not
developed in this paper.

## Files

- **main.tex** — paper entry point
- **sections/** — section sources
- **references.bib** — bibliography
- **main.pdf** — compiled paper
- **experiments/tpc19_certificate.py** — exact certificate
- **experiments/tpc19_certificate.json** — deterministic output

## Reproduce the exact certificate

From this directory:

~~~powershell
python experiments\tpc19_certificate.py
python -O experiments\tpc19_certificate.py
~~~

Both modes must report success and regenerate identical JSON. At the
archived version:

- JSON SHA-256:
  **B141ADC152C38CDABE46528BD872AA4622AFD7A8E9D1E8E719D283247AC05744**
- script SHA-256:
  **60154632DB45B1DB023C8CF5BF6D4084481EEF9154851CD2121567C2DA96F61F**

The certificate uses exact integers, rational arithmetic, and formal
prime-log polynomials for the proof checks. Optional finite prime-data
diagnostics are isolated and explicitly marked
**prime_asymptotic_evidence=false**.

## Build the paper

~~~powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
~~~
