# TPC-31 - Canonical determinant cells

This directory contains:

> **Canonical Determinant Cells in a Primitive Möbius Tail:
> Support-Cardinality Bounds, All-Content Cell Pruning, and the
> Residue-Cell Zero-Mode Gate**

TPC-31 continues the primitive ultra-long residual after TPC-30. It
constructs a factorization-independent normalized determinant, proves
quantitative cell bounds with power saving under the stated
support-cardinality and modulus-growth conditions, and splices those
estimates with TPC-30 to cover all target contents inside one selected
cell.

## Canonical determinant

For

\[
N_m(j)=mj+h,\qquad N_n(j)=nj+h,
\]

put

\[
c=(N_m(j),N_n(j)),\qquad
\Delta^\#=\frac{m-n}{c}.
\]

On the primitive orbit, \(c\mid m-n\). If

\[
U=N_m(j)/c,\qquad V=N_n(j)/c,
\]

then

\[
\boxed{(U,V)=1,\qquad mV-nU=h\Delta^\#.}
\]

Unlike \((m-n)/(r,s)\), this coordinate does not depend on selecting a
pair of target divisors, so it labels the unexpanded physical raw
kernel.

## Main cell theorem

For exact content \(c\) and an allowed normalized-determinant set
\(\Omega_c\), define its physical cardinality

\[
\mathcal H_c(\Omega_c)
=\#\{\delta\in\Omega_c:|\delta|\ll Q/c\}.
\]

For each of the two mixed raw channels and the both-ultra raw channel,

\[
\boxed{
|\mathcal S(c\le Z,\Delta^\#\in\Omega_c)|
\ll X^\varepsilon Q\log(2L)
\sum_{c\le Z}\left(1+\frac Jc\right)
\mathcal H_c(\Omega_c).
}
\]

The proof combines:

- the unique row match \(n=m-c\delta\);
- a two-sided degree bound and the Schur test;
- the physical row \(\ell^2\) estimate;
- the single exact-content orbit class modulo \(c\);
- the pointwise \(X^\varepsilon\) envelope for each complete raw kernel.

This gives translated-window bounds independent of the window center,
including windows at macroscopic distance from the row diagonal. It
also gives individual normalized-determinant residue-class bounds with
the necessary \(Q^{-1}\) one-match floor.

## All-content splice

Splitting at a threshold \(C\), TPC-30 controls \(c>C\), while the new
cell theorem controls \(c\le C\). For an interval \(I\) of length
\(W\) and one class \(a\pmod q\),

\[
\boxed{
|\mathcal S(\Delta^\#\in I,\Delta^\#\equiv a\pmod q)|
\ll X^\varepsilon XQ
\left[
J^{-1}+C^{-1}
+\left(1+\frac Wq\right)
\left(\frac CX+Q^{-1}\right)
\right].
}
\]

If \(1+W/q=X^{s+o(1)}\) and \(s<\beta\), every fixed saving below

\[
\min\{1-\beta,\beta-s\}
\]

is available after optimizing \(C\).

For one residue class across the full determinant range, if
\(q=X^{\rho+o(1)}\), the relaxed saving is

\[
\min\{1-\beta,\beta,\rho\}.
\]

## High-beta sample

At

\[
\beta=\frac{267}{400},\qquad
J=X^{133/400+o(1)},
\]

the paper proves, cellwise and over all target contents:

- any fixed saving below \(133/400\) for a translated window of length
  \(JX^{o(1)}\);
- any fixed saving below \(67/200\) for the same \(J\)-window when it is
  centered at \(|\Delta^\#|\asymp Q\), because all target contents are
  then automatically bounded;
- any fixed saving below \(67/400\) for a translated window of length
  \(X^{1/2+o(1)}\);
- any fixed saving below \(133/400\) for one class modulo
  \(q=X^{133/400+o(1)}\).

The macro-centered versions are not near-diagonal deletions. They are upper bounds for
support-compatible cells, not nonemptiness or positive-mass results.

## Fourier and zero-mode boundary

For small content \(c\le C\ll J\), the signed residue-cell amplitudes
\(S_a\) satisfy

\[
\sum_{a\pmod q}|S_a|^2
\ll X^\varepsilon(JQ^2)^2
\left(Q^{-1}+q^{-1}\right).
\]

Their discrete Fourier transform therefore has an
exceptional-frequency estimate.  If \(q=X^{\rho+o(1)}\le Q\) and
\(0<\sigma<\rho/2\), all but
\(O(X^{2\sigma+\varepsilon})=o(q)\) frequencies satisfy the associated
fixed-power bound. However,

\[
\widehat S(0)=\sum_{a\pmod q}S_a
\]

is exactly the original unweighted small-content contribution. This is
the zero coefficient of an auxiliary residue-label transform, not an
orbit-variable Poisson zero frequency. Bounds for the nonzero
frequencies do not control it. Likewise,
absolute summation over all residue cells or all windows exactly
restores the full absolute majorant.

One candidate for TPC-32 is therefore to construct a factorable
representation of the prime-Möbius coefficient while retaining the
fixed residue factors, pair mask, and matched cutoff difference, and
then control or cancel the auxiliary zero coefficient. TPC-31
does not prove signed dispersion, the complete residual estimate, a
prime-pair asymptotic, twin primes, or a breach of sieve parity.

## Exact certificate

Run from this directory:

```powershell
python experiments\tpc31_certificate.py
python -O experiments\tpc31_certificate.py
```

Both modes perform `876,320` exact checks and regenerate byte-identical
JSON. The finite checks cover canonical reduction, selected-divisor
dilation, determinant-cell degrees, integer-weight Schur inequalities,
exact-content orbit occupancy, cell partition and absolute reassembly,
the rational splice optimization, high-beta arithmetic, and explicit
scope flags.

Reproducibility values:

- Source SHA-256:
  `7b4c984620ce733e7741d00b3c4b547e7d62efb05947902d91fc9dc54e133ff7`
- JSON SHA-256:
  `5776b4310c04df512c47f940924253d475ab51a2da3c8058a52201a643479fea`
- Certificate digest:
  `cd48ae70d7d5a39b54d128a28c695557f440de37582c7c3cec6405713eae0ab4`

The certificate verifies finite algebra and rational bookkeeping only.
It is not a numerical proof of asymptotic Möbius cancellation or a
prime-pair statement.

## Files

- `main.tex` - paper entry point
- `sections/` - section sources
- `references.bib` - bibliography
- `main.pdf` - compiled paper
- `experiments/tpc31_certificate.py` - exact certificate
- `experiments/tpc31_certificate.json` - archived certificate output

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
