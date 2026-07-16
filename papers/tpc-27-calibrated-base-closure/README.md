# TPC-27 — Calibrated base closure

This paper closes the missing calibrated base value in the strict
Poisson-short overlap of the TPC-26 cutoff-stability theorem.

Its new exact identity is the Ramanujan-square factorization

\[
K_S^0(m,n)=\sum_{k>1}c_k(m-n)B_{k,S}(m)B_{k,S}(n).
\]

An exact finite-model multiple identity and uniform prime-coefficient
calibration control small \(k\); an absolute cofactor estimate and the
off-diagonal row mask control large \(k\).  After extracting physical
frequency zero before continuous separation, restoring the scalar
channels \(EZ,ZE,EE\), and importing only the nonzero spectrum from
TPC-22/TPC-23, the paper proves

\[
\mathcal Q_S^{\mathrm{phys}}
\ll_B XQ(\log X)^{-B}.
\]

Combining this base estimate with TPC-26 closes the selected calibrated
square at the strict rational sample

\[
(\delta,\beta,s,t)=
\left(\frac3{20},\frac{31}{50},\frac7{20},\frac{39}{100}\right),
\qquad S<J<T.
\]

Here \(7/100\) is the centered nonzero conductor ledger margin and
\(1/100\) is the annular minimax margin; the complete calibrated conclusion has arbitrary
logarithmic saving.  The higher-\(\beta\) sample, ultra-long complement,
full residual, positivity, Hardy–Littlewood asymptotic, twin primes,
and any general parity breakthrough remain open.

## Exact certificate

Run from this directory:

```powershell
python experiments\tpc27_certificate.py
python -O experiments\tpc27_certificate.py
```

Both modes complete 20,540 exact checks and write identical JSON.

- Source SHA-256: `59afa0a8f94bc208297478d1fcc41e856cf88351c03bae3ef0e51690676a8e3d`
- JSON SHA-256: `dd7033c1a170a6ba968d4bc478841e19978a5cbb38401a9c7d64681889bd2a48`
- Certificate digest: `ae5b89520111cf8be04cc193e85cd197b8159cbed1b9e0421b9d8f2a1af0e6c4`

The certificate checks finite algebra only; it is not asymptotic
evidence.

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
