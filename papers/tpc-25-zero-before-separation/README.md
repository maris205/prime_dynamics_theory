# TPC-25 — Zero before separation

This directory contains:

> **Zero Before Separation in a Primitive Möbius Tail: Provenance-Weighted
> Closure and the Principal Row-Mode Boundary**

TPC-25 closes the physical zero-frequency mass gate left explicit in
TPC-24 for the actual primitive opened-\(d\) packet. It also proves why
the same conclusion cannot be obtained from the abstract soft row-energy
interface alone.

## Main results

- In one opened-\(d\) slice, the actual row coefficient is
  \(\mu(d)\log\ell\) times bounded smooth and fixed-residue factors, with
  \(m=\ell d\), \(Q=LD\). Chebyshev's estimate gives

  \[
  \sum_{\ell\asymp L,\ \ell\ {\rm prime}}\log\ell
  \sum_{d\asymp D}|\mu(d)|\ll LD=Q.
  \]

- Extracting Poisson frequency zero before Mellin–Fourier separation
  turns the original row-dependent orbit amplitude into a uniformly
  bounded integral. Hence the physical zero-mode row-pair mass is
  \(O(Q^2)\), not \(Q^2X^\varepsilon\).

- Combining that provenance bound with the TPC-24 pointwise shell kernel
  gives, for \(S=X^{s+o(1)}\) and \(0<\kappa<s\),

  \[
  |\mathcal Z^0_{S,T}|\ll
  JQ^2\{(\log X)^{-A}+X^{-s+\kappa+o(1)}\}.
  \]

  Therefore the extra fixed-projective-mass hypothesis in TPC-24 is
  automatic for the actual one-sided opened-\(d\) packet.

- Under the remaining inherited row, no-wrap, Fourier-tail, and
  conductor interfaces, positivity of

  \[
  \eta_{\rm asym}(\beta;s,t)=\min\left\{
  1-\frac{3\beta}{2},
  \frac{\beta+1-2s-2t}{2},
  \frac{3-\beta-s-5t}{4}\right\}
  \]

  with fixed margin yields arbitrary logarithmic saving for the actual
  calibrated one-sided mixed increment with a general nonzero-mean
  fixed smooth test in the factorable provenance class. No mean-zero
  hypothesis on the fixed physical test is needed.

- The abstract soft-\(L^2\) interface cannot imply this result. A dense
  constant row mode with entry size
  \(\rho_X=\exp(-\sqrt{\log X})\) obeys every fixed logarithmic pointwise
  bound and the soft row norms, yet its bilinear form remains of order
  \(Q^2\).

- The coherent mode occurs in exact finite Möbius algebra. For
  \(H=1\), \(R=S=2\), \(T=3\), and distinct prime rows greater than
  \(3\), the raw kernel is

  \[
  K^0_{2,3}(m,n)=\kappa_0=\frac{(\log2-2)\log3}{6}.
  \]

  After off-diagonal masking its matrix is
  \(\kappa_0(\mathbf1\mathbf1^{\mathsf T}-I)\). Its operator and
  Hilbert–Schmidt norms are of the same order; a direct
  Hilbert–Schmidt upgrade has no dimension gain.

- In a prime-row no-long-wrap model, the full zero kernel has an exact
  congruence skeleton assembled from residue-class constant spaces
  modulo the shared factor \(g\). Projecting those spaces away gives a
  deflated operator bound and identifies the row-balance statistics a
  future both-new-shell argument would need.

## Scope

The positive theorem applies to the actual factorable row provenance,
not to arbitrary matrices satisfying only \(X^\varepsilon\) row bounds.
It closes one calibrated mixed shell and its transpose. It does not close
the both-new square, the ultra-long complement fibers, the full residual,
or the positivity/main-term stages. It proves no Hardy–Littlewood
asymptotic, twin-prime lower bound, or general breach of sieve parity.

## Exact certificate

Run:

    python experiments\tpc25_certificate.py
    python -O experiments\tpc25_certificate.py

Both modes perform 119 exact checks and must regenerate byte-identical
JSON. Final hashes:

- JSON SHA-256: 7a69c1ddac15ee3d9b7cd499f9e9e1259014559ee74d36d289acb50a32b40604
- source SHA-256: c818160b8aa928180db5044974ceac5b84d2d2ecf21bc42760f69773cec498c8
- certificate digest: c6450e1b3cb5e47c2f5b23a4456b752a56775c688646527e8363e9b3362727f1

The certificate uses rational arithmetic and formal prime logarithms.
It checks finite kernel/skeleton identities, congruence-matrix ranks, the
principal eigenmode, a rational soft-interface saturation model, and the
rational exponent sample. It is not asymptotic numerical evidence.

## Files

- main.tex — paper entry point
- sections/ — section sources
- references.bib — bibliography
- main.pdf — compiled paper
- experiments/tpc25_certificate.py — exact certificate
- experiments/tpc25_certificate.json — archived output

## Build

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
