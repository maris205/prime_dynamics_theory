# TPC-30 - Common-target content

This directory contains:

> **Common-Target Content in a Primitive Möbius Tail:
> Row-Orbit Pruning, Cross-Factor Pruning, and the Coprime-Core Gate**

TPC-30 continues the ultra-long complement analysis after TPC-29. It
uses the full gcd of the two affine targets, rather than only the gcd
of two selected reflected divisors, to remove a new unconditional
sector of the physical residual.

## Main results

For

\[
N_m(j)=mj+h,\qquad N_n(j)=nj+h
\]

on the primitive orbit, the paper exploits

\[
\boxed{
(N_m(j),N_n(j))=(N_m(j),m-n)\mid m-n.
}
\]

The Euclidean target-gcd geometry is inherited from TPC-18 and is
credited explicitly. The new result is its insertion into the actual
opened-row packet and all three raw ultra channels.

For a fixed off-diagonal row pair, every exact target gcd is a divisor
of \(|m-n|\). If \(\mathcal I\) is the physical orbit interval of
length \(O_{\mathscr D}(J)\), then

\[
\#\{j\in\mathcal I:(j,h)=1,\ (N_m(j),N_n(j))>Z\}
\ll_\varepsilon X^\varepsilon\left(1+\frac JZ\right).
\]

Using the physical row \(\ell^1\) mass gives

\[
\boxed{
|\mathcal S_{\mathcal G>Z}|
\ll_{\varepsilon,h,\mathscr D}
X^\varepsilon\left(Q^2+\frac{XQ}{Z}\right).
}
\]

If \(Z\ge X^\eta\), every fixed

\[
\eta_0<\min\{\eta,1-\beta\}
\]

is a power-saving exponent relative to the natural scale \(XQ\).

## Exact four-factor content

If

\[
N_m=rU,\qquad N_n=sV,
\]

put

\[
g=(r,s),\qquad e=(U,V),
\]

and write

\[
r=gr_0,\quad s=gs_0,\qquad
U=eU_0,\quad V=eV_0.
\]

Then

\[
\boxed{
(N_m,N_n)
=ge(r_0,V_0)(s_0,U_0).
}
\]

No assumption \((g,e)=1\) is needed. Within the retained physical raw
channels, this gives a power-saving upper bound for every sector with
large quotient content or large normalized cross-content, even when
\((r,s)=1\).

## High-beta sample

At

\[
\beta=\frac{267}{400},\qquad
J=X^{133/400+o(1)},\qquad
T=X^{193/500+o(1)},
\]

take

\[
r,s=X^{1/4+o(1)},\qquad (r,s)=X^{o(1)},
\]

and

\[
U,V=X^{3/4+o(1)},\qquad
(U,V)=X^{2/5+o(1)}.
\]

Formally, the corollary is stated on fixed \(\delta\)-windows around
these exponents; this gives the displayed \(o(1)\) cell an explicit
quantifier. The reflected lcm is \(X^{1/2+o(1)}>J\), while its primitive part has
the same exponent. TPC-29 therefore has zero absolute-incidence
saving on this cell. TPC-30 instead gives every fixed

\[
\eta_0<\boxed{\frac{133}{400}}.
\]

This is an upper bound for a support-compatible formal sector. It does
not assert that the sector carries nonzero asymptotic mass.

## What remains

After removing large full-target content, the residual satisfies

\[
(N_m(j),N_n(j))\le X^\eta.
\]

The sharp model is the fully coprime target core. The next planned
stage is determinant-entropy pruning for translated determinant
windows and individual determinant residue classes, followed by a
genuinely signed family-dispersion problem.

The paper does not close the complete ultra-long difference, the full
TPC-18 residual, or every small-content fiber. It proves no positivity,
Hardy-Littlewood asymptotic, twin-prime theorem, or breach of the sieve
parity barrier.

## Exact certificate

Run from this directory:

~~~powershell
python experiments\tpc30_certificate.py
python -O experiments\tpc30_certificate.py
~~~

The script requires Python 3.10 or later and uses only the standard
library. Both modes complete 773,361 recorded exact checks and
regenerate byte-identical JSON.

The checks include:

- 441,578 primitive target-gcd identity checks;
- 1,924 exact-content occupancy checks;
- 1,135 fixed-row large-content checks;
- 197,313 exact four-factor checks, including all 65,536 quadruples
  \(1\le r,s,U,V\le16\);
- 131,301 row-residue energy checks;
- 90 rational high-beta ledger checks;
- 20 scope and nonoverlap metadata regression assertions.

Reproducibility values:

- Source SHA-256:
  <code>f4813d6e89163098187fe1ce585934b354a384a09b7ca4332e3fad42d1a78610</code>
- JSON SHA-256:
  <code>c466cd747c726d51074c0d8967a950ee0bcfb3e8a4658fcb8d3a81e52615c2e9</code>
- Certificate digest:
  <code>8c52338642c27d2c4dafd6807cb8cc56d52888ae16b27cd9aeda880ccc10f64d</code>

These checks certify finite algebra and rational arithmetic only. They
are not a numerical proof of an asymptotic Mobius estimate or a
prime-pair statement.

## Files

- **main.tex** - paper entry point
- **sections/** - section sources
- **references.bib** - bibliography
- **main.pdf** - compiled paper
- **experiments/tpc30_certificate.py** - exact certificate
- **experiments/tpc30_certificate.json** - archived certificate output

## Build

~~~powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
~~~
