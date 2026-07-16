# TPC-29 - Content-rich reflected fibers

This directory contains:

> **Content-Rich Reflected Fibers in a Primitive Mobius Tail:
> Long-Fiber Pruning, a Sparse Incidence Wedge, and the Primitive-Core
> Barrier**

TPC-29 starts from the exact calibrated cutoff difference beyond the
TPC-28 truncation and closes two explicit content-rich portions of the
reflected ultra-long complement. The proofs use absolute divisor
incidence and opened-row provenance, not Mobius-sign cancellation.

## Main results

- If \(U_0\) contains every physical target, then

  \[
  P_{m,U_0}-P_{m,T}=C_{m;T,U_0}.
  \]

  The joint difference has exactly three raw ultra channels and two
  row-drift legs. The drifts are power-small from the imported
  \(L^{-1}\) factor. This exact identity avoids importing a pointwise
  scalar-tail replacement whose displayed majorants alone do not
  imply arbitrary logarithmic saving.

- For distinct primitive physical rows and dyadic reflected variables
  \(r\asymp A\), \(s\asymp B\), \((r,s)\asymp G\), the paper proves

  \[
  \mathcal N_{m,n}(A,B,G)
  \ll_{\varepsilon,h,\mathscr D}X^\varepsilon
  \min\left\{J,\frac{AB}{G^2}+\frac JG\right\}.
  \]

  Compatibility is equivalent to
  \((r,s)\mid h(m-n)\). On the primitive orbit this reduces to
  \((r,s)\mid m-n\), and each compatible pair occupies one residue
  class modulo \([r,s]\).

- The actual opened-row \(\ell^1\) bounds convert this count into

  \[
  |\mathcal S(A,B,G)|
  \ll_{\varepsilon,h,\mathscr D}Q^2X^\varepsilon
  \min\left\{J,\frac{AB}{G^2}+\frac JG\right\}
  \]

  for every mixed or both-ultra physical block.

- With \(q=[r,s]\) and \(g=(r,s)\), the content-rich sparse wedge

  \[
  q\ge J,\qquad \frac qg\le JX^{-\eta}
  \]

  satisfies

  \[
  \mathcal S_{\rm rich}
  \ll_{\varepsilon,\eta,h,\mathscr D}
  XQX^{-\eta+\varepsilon}.
  \]

- On the long-fiber side, for \(1\le D<Y\le J\),

  \[
  |\mathcal S_{\le Y,>D}|
  \ll_{\varepsilon,h,\mathscr D}X^\varepsilon
  \left\{
  \frac{XQ}{D}\log^2(2Y)+X\log^3(2Y)
  \right\}.
  \]

  Thus every sector with \(D\ge X^\eta\) is power-small, with saving
  exponent \(\min\{\eta,\beta\}\).

- At the TPC-28 high-\(\beta\) sample

  \[
  \beta=\frac{267}{400},\qquad
  J=X^{133/400+o(1)},\qquad
  T=X^{193/500+o(1)},
  \]

  the exponent cell
  \(A=B=X^{1/4}\), \(G=X^{1/10}\) has sparse margin \(27/400\)
  and incidence margin \(13/400\). Consequently every fixed
  \(\eta_0<13/400\) is available after absorbing endpoint constants
  and \(o(1)\) factors. This is distinct from TPC-28's conductor
  margin \(13/1600\).

## What remains

The absolute-incidence method reaches only the natural scale on the
primitive sparse core

\[
[r,s]\ge J,\qquad
\frac{[r,s]}{(r,s)}>JX^{-\eta},
\]

and the long theorem leaves the small-gcd core

\[
[r,s]\le J,\qquad (r,s)\le X^\eta.
\]

Closing these pieces requires a family-level signed dispersion
estimate that is uniform in the polynomially growing affine slopes,
divisor family, physical rows, and weights.

The paper does not close the complete ultra-long difference, the full
TPC-18 residual, or endpoint reassembly. It proves no positivity,
Hardy-Littlewood asymptotic, twin-prime theorem, polynomially uniform
Chowla/Elliott estimate, or general breach of the sieve parity barrier.

## Exact certificate

Run from this directory:

```powershell
python experiments\tpc29_certificate.py
python -O experiments\tpc29_certificate.py
```

The script requires Python 3.10 or later and uses only the standard
library. Both modes complete 37,265 recorded top-level exact checks
and regenerate byte-identical JSON.

The subcounts are:

- 5,526 calibrated-cutoff and five-term checks;
- 13,279 generalized-CRT fiber checks;
- 9,074 direct/CRT incidence and explicit finite-bound checks;
- 3,268 long-fiber bookkeeping checks;
- 6,104 rational exponent-ledger checks;
- 14 scope-flag checks.

The finite incidence regression includes the closed \(G=1\) base cell,
uses an explicit arithmetic multiplicity constant, and does not
interpret the asymptotic \(\ll\) constant as one.

- Source SHA-256:
  `13de31994c18d36f30975121daf485d8aca2f738f5a48dfc31e297130ed136c6`
- JSON SHA-256:
  `0cbe83d578f39246542d6b0480db3d4a3d9b02ed23036dd9f569671dd5e2242d`
- Certificate digest:
  `5c2858662e76278cf3e8b4f1e26a4ac024e3b863ca21a3be8866dcf921a162b1`

The source hash is computed after normalizing source newlines to LF.
The JSON hash is the SHA-256 of the generated LF byte stream. The
certificate digest hashes the canonical sorted payload before the
digest field is inserted. The local `.gitattributes` keeps source and
certificate text at LF across platforms.

These checks certify finite algebra, CRT bookkeeping, and rational
exponent arithmetic only. They are not a numerical proof of an
asymptotic Mobius estimate or a prime-pair statement.

## Files

- `main.tex` - paper entry point
- `sections/` - section sources
- `references.bib` - bibliography
- `main.pdf` - compiled paper
- `experiments/tpc29_certificate.py` - exact certificate
- `experiments/tpc29_certificate.json` - archived certificate output

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
