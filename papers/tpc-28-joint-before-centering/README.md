# TPC-28 - Joint before centering at a Poisson-long base

This directory contains:

> **Joint Before Centering at a Poisson-Long Base: Full-Rectangle Exact
> Conductors and High-Beta Initial-Value Closure**

TPC-28 closes the missing initial value for the source-compatible
high-\(\beta\) sample left open by TPC-26 and TPC-27.  Its key device is
to use two exact decompositions of the calibrated prefix at different
additive frequencies.

## Main results

- At additive frequency zero, the complete calibrated kernel satisfies

  \[
  \mathcal R_S^0(m,n)-\delta_H(m)D_{n,S}-\delta_H(n)D_{m,S}
  +\delta_H(m)\delta_H(n)
  =K_S^0(m,n)+E_S(m)E_S(n).
  \]

  Thus the two mixed centered-error legs cancel exactly.  The imported
  Ramanujan-square theorem for \(K_S^0\) has no condition \(S<J\).

- At nonzero frequency, the paper keeps the raw joint product

  \[
  P_{m,S}P_{n,S}
  =\mathsf A_{m,S}\mathsf A_{n,S}
  -\delta_H(m)\mathsf A_{n,S}
  -\delta_H(n)\mathsf A_{m,S}
  +\delta_H(m)\delta_H(n).
  \]

  A newly defined full-base exact-conductor energy gives

  \[
  \mathcal L^{\rm base}_{Y;S}(F_1,F_2)
  \ll QX^\varepsilon
  \sqrt{\mathcal K_Q(F_1)\mathcal K_Q(F_2)}
  \min\{\sqrt{JY},F_1F_2\},
  \qquad \mathcal K_Q(F)=F+Q/F.
  \]

- On the physical target support, the pointwise divisor estimate
  \(\mathsf A_{m,S}(j)\ll_\varepsilon X^\varepsilon\) makes both
  remaining drift legs power-small from the existing condition
  \(L\ge X^{\lambda_0}\).  No factor \(1+S/J\) is needed.

- If the stated physical opened-row, off-diagonal-mask, no-wrap,
  smooth-transfer, Fourier-tail, target-support, and fixed-margin
  interfaces hold and \(M_\beta(s)>0\), then

  \[
  \mathcal Q_S^{\rm phys}
  \ll_B XQ(\log X)^{-B}
  \]

  for every fixed \(B>0\), without assuming \(S<J\).

- For the exact source-compatible sample

  \[
  \beta=\frac{267}{400},\qquad
  s=\frac{23}{60},\qquad
  t=\frac{193}{500},
  \]

  the old centered ledger contains the negative face \(-1/800\), while

  \[
  M_\beta(s)=\frac{13}{1600},\qquad
  M_\beta(t)=\frac{33}{8000}.
  \]

  The new base estimate therefore splices with TPC-26 cutoff stability
  and closes this selected calibrated square through \(T=X^{t+o(1)}\).

## Scope

The result concerns one selected truncated quadratic packet.  It does
not estimate the ultra-long complement beyond \(T\), close the full
TPC-18 residual, prove positivity or a Hardy--Littlewood asymptotic,
imply twin primes, or breach the sieve parity barrier in general.

## Exact certificate

Run from this directory:

```powershell
python experiments\tpc28_certificate.py
python -O experiments\tpc28_certificate.py
```

The script requires Python 3.10 or later and uses only the standard
library.  To compare modes independently, save
`experiments/tpc28_certificate.json` after the first command, run the
second command, and compare the two files with `Get-FileHash` or a
bytewise comparison tool.

Both modes complete 33,299 exception-based exact checks and regenerate
byte-identical JSON.  The certificate uses only the Python standard
library, rational arithmetic, and formal prime-log polynomials.

The subcounts are 18 raw/drift identities, 9 direct and complete-period
zero checks, 747 full-base CRT-density checks, 32,507 finite minimax
grid and witness checks, and 18 exact high-beta ledger checks.  The
minimax grid is regression coverage for representative rational cells;
the continuous piecewise minimax theorem is proved in the paper, not by
finite enumeration.

- Source SHA-256: `c3ad5c993e1823a4752c5c31ef5e348342982607c078e8bc4343697d5dad9948`
- JSON SHA-256: `e75a92e2eb78ce297fa305e5c8ea42eab0a6cec591e3ff989eb5566bd90ab6ec`
- Certificate digest: `3cb8458021bd05d8b04154137a92a068633944679a038db9c5e4f342dff563a3`

The source hash is computed after normalizing source newlines to LF.
The JSON hash is the SHA-256 of the generated LF byte stream.  The
certificate digest hashes the canonical sorted payload before the
digest field is inserted.  The local `.gitattributes` keeps source and
certificate text at LF across platforms.

These checks certify finite algebra and rational bookkeeping only; they
do not verify the analytic conductor theorem and are not numerical
evidence for an asymptotic Mobius or prime-pair claim.

## Files

- `main.tex` - paper entry point
- `sections/` - section sources
- `references.bib` - bibliography
- `main.pdf` - compiled paper
- `experiments/tpc28_certificate.py` - exact certificate
- `experiments/tpc28_certificate.json` - archived certificate output

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
