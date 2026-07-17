# TPC-33 - Primitive affine columns

This directory contains:

> **Primitive Affine Columns at a Distinguished Zero Frequency:
> Fixed-Determinant Projective Plancherel, Structured-Mask
> Disintegration, and the Q3 Energy Gate**

TPC-33 continues the distinguished zero-frequency problem isolated in
TPC-32. It returns to the actual row-pair mask, decomposes each fixed
physical column into primitive fixed-determinant affine Mobius correlations,
proves exact arithmetic and finite-field average theorems for those
correlations, and identifies the remaining collective energy estimate.

## Main unconditional results

### Integral affine normal form

For

\[
sU-aD=h,\qquad (a,s)=1,\qquad(as,h)=1,
\]

choose \(sx-ay=1\). Every integral solution is uniquely

\[
U_t=hx+at,\qquad D_t=hy+st,
\]

and

\[
(D_t,U_t)=(D_t,h)=(U_t,h)=(h,t).
\]

On the primitive layer,

\[
\mu(D_t)\mu(U_t)=\mu(D_tU_t),
\]

where \(D_tU_t\) is a reducible quadratic of discriminant \(h^2\).

### Moving-slope squarefree support

With a balanced Bezout origin and \(K=\max(a,s)\),

\[
\sum_{\substack{T<t\le2T\\(t,h)=1}}
\mu^2(D_t)\mu^2(U_t)
=\mathfrak S_{\rm sf}(a,s;h)T
+O_h\!\left(\frac{T}{\log(2T)}+\sqrt{KT}\right).
\]

The Euler product is explicit and uniformly positive for fixed \(h\).
This controls support, not Mobius signs.

### Actual-mask column disintegration

For the original mask

\[
\mathbf1_{\ell\ne\ell'}
\mathbf1_{|\ell d-\ell'e|>QX^{-\kappa_0}}
\mathbf1_{(d,e)\le X^{\kappa_0}},
\]

the exact identity

\[
\mathbf1_{(d,e)\le G}
=\sum_{v\mid d,e}\lambda_G(v),
\qquad
\sum_{v\mid e}|\lambda_G(v)|\le3^{\omega(e)}=X^{o(1)}
\]

shows that a fixed column has only subpolynomial mask-expansion cost. The
inner sequences are

\[
\sum_{r\in I}
\mu(\widetilde d_0+sr)
\mu(\widetilde u_0+\ell jv r)W(r),
\]

with

\[
s\widetilde u_0-\ell jv\widetilde d_0=h,
\qquad |I|\ll1+\frac{D}{sv}.
\]

This is a columnwise theorem for the actual mask, not a low-rank theorem
for an arbitrary bounded mask.

### Fixed-determinant projective Plancherel

For a prime \(q\), fixed \(h\ne0\pmod q\), and

\[
\mathcal C_{a,s}^{(h)}(f,g)
=\sum_D f(D)g(s^{-1}(aD+h)),
\]

the paper proves

\[
\sum_{a,s\ne0}|\mathcal C_{a,s}^{(h)}-q\bar f\bar g|^2
=q\|f^\circ\|_2^2\|g^\circ\|_2^2
-\sum_{b\ne0}\left|\sum_Df^\circ(D)g^\circ(bD)\right|^2.
\]

The finite Mobius model consequently has \(o(q)\) correlation for all but
\(O(q^{2-2\eta})\) nonzero coefficient pairs \((a,s)\). The exact second
moment averages both \(a/s\) and \(h/s\), so it is not an almost-every-ratio
statement by itself. Complete product slopes
\(a=\ell j\) preserve the energy exactly for every nonzero \(\ell\), even
if the allowed \(\ell\)'s are prime residues.

## Conditional physical transfer

The two exact polarizations define column energies \(E_L,E_R\). The paper
proves

\[
E_L+E_R\ll X^{o(1)}Q^3
\quad\Longrightarrow\quad
|\mathcal S_{\rm sh}^{\rm all}|\ll X^{o(1)}Q^2.
\]

At \(Q=X^{267/400+o(1)}\), this is the full
\(J^{-1}=X^{-133/400+o(1)}\) amplitude saving needed by TPC-32. The Q3
energy estimate itself remains open.

A strategy that proves square-root cancellation separately on every
longest affine fiber but sums all outer variables absolutely still falls
short by

\[
\frac{49727}{210000}=0.236795\ldots.
\]

The next target is therefore a restricted physical projective-energy
theorem across \(\ell,j,s,v\), and the opposite row.

## Exact certificate

Run from this directory:

    python experiments/tpc33_certificate.py
    python -O experiments/tpc33_certificate.py

Both modes perform 506,900 exact checks and regenerate byte-identical JSON.
No floating-point root of unity is used.

Reproducibility values:

- Normalized source SHA-256:
  `a55c3d71c0851870ea0b9bbd1e9ef9384e70885e5de1ddc685c309ec1ec12c67`
- JSON SHA-256:
  `c7d08c9020590d81bc590a6caa7d0f36ad3f553532e580fbdc03553638a0b3b5`
- Certificate digest:
  `e5a28b8dcac36154ff620c2e644eed7fd163d00568fcd90d8e4443beafcfe37b`

The certificate checks finite algebra and rational ledgers only. It does
not prove asymptotic Mobius cancellation, the physical Q3 energy estimate,
zero-frequency flatness, positivity, a Hardy-Littlewood asymptotic, twin
primes, or a breach of sieve parity.

## Files

- `main.tex` - paper entry point
- `sections/` - section sources
- `references.bib` - bibliography
- `main.pdf` - compiled paper
- `experiments/tpc33_certificate.py` - exact certificate
- `experiments/tpc33_certificate.json` - archived certificate output

## Build

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
