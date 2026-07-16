# TPC-23 — Dynamic cutoff and affine parity fibers

This directory contains:

> **Dynamic Cutoffs Beyond the Sieve Range: A Closed Large-Divisor
> Strip and the Remaining Affine Möbius Parity Fibers**

TPC-23 extends the selected residual packet closed in TPC-22 from the
static support `u,v <= R` to a dynamic support `u,v <= S`, where
`S = R X^rho` for an explicit fixed `rho > 0`. The finite Ramanujan
model still ends at `R`; `S` is a cutoff in the exact residual divisor
expansion.

## Main results

- With `Q = X^beta`, `J = X^(1-beta)`, and `S = X^s`, the generalized
  conductor saving is

  \[
  \eta_S=\min\left\{
  1-\frac{3\beta}{2},
  \frac{\beta+1-4s}{2},
  \frac{3-\beta-6s}{4}
  \right\}.
  \]

  Subject to the inherited no-wrap and polynomial Fourier-tail
  hypotheses, the selected packet `u,v <= S` closes whenever
  `s < 1-beta` and `eta_S > 0`, with fixed margins.

- Setting `s = 1/2-delta+rho` gives the explicit hybrid collar

  \[
  0<\rho<\min\left\{
  \frac12+\delta-\beta,
  \frac{\beta+4\delta-1}{4},
  \frac{6\delta-\beta}{6}
  \right\}.
  \]

  The new square includes both mixed support collars and the genuine
  both-large block `(R,S]^2`.

- The Ramanujan mean is re-proved for the dynamic coefficient
  `b_R(u) 1_{u<=S}`. No principal block is silently deleted, and the
  tensor proof does not require `L > 2S`; the separate deterministic
  occupancy alternative does require that stronger source margin.

- The remaining ultra-long tail has the exact complement form

  \[
  \sum_{u\mid n,\ u>S}-\mu(u)\log u
  =\sum_{r\mid n,\ r<n/S}-\mu(n/r)\log(n/r).
  \]

  For two rows and fixed complement divisors `r,s`, the quotient
  variables are affine forms. Compatibility is exactly
  `(r,s) | h(m_1-m_2)`, and their determinant is

  \[
  \frac{h(m_1-m_2)}{(r,s)}\ne0.
  \]

- Tao's proved logarithmically averaged two-point Elliott theorem
  cancels every fixed affine complement fiber. The paper derives a
  fixed finite-complement theorem and an ineffective slowly growing
  diagonal corollary.

- For every fixed unweighted row pair, the absolute value of the
  unit-complement fiber has local mass `>> J (log J)^2`, by
  simultaneous squarefree density. Thus a coefficientwise sign-blind
  estimate cannot make that component power-saving; this is not a
  lower bound for the full weighted packet.

## Scope

This paper does **not** prove the complete TPC-18 residual-dispersion
theorem, a Hardy–Littlewood asymptotic, a twin-prime lower bound, or a
general breach of the sieve parity barrier. The remaining input is a
quantitatively uniform affine-Möbius estimate for polynomially growing
rows and complement fibers, together with a sparse-fiber incidence
estimate and global endpoint reassembly.

## Exact certificate

Run:

```powershell
python experiments\tpc23_certificate.py
python -O experiments\tpc23_certificate.py
```

Both modes perform 56,714 exact checks and regenerate byte-identical
JSON.

- JSON SHA-256: `62e982d5da46d68fcf698f498a2d8fa66cb54ca9422d470f8516bc18f2aa08ab`
- source SHA-256: `51640ec4cbc5c82d792ce40a170ec919ffa2593fade6f92eaffca25d612429be`
- certificate digest: `c5054fcce65ccbdda59dba99c519f5fd9fbe147384f63f6b5d0e17265876be97`

All flags for asymptotic evidence, full residual closure,
Hardy–Littlewood, twin primes, and a general parity breakthrough are
false.

## Files

- `main.tex` — paper entry point
- `sections/` — section sources
- `references.bib` — bibliography
- `main.pdf` — compiled paper
- `experiments/tpc23_certificate.py` — exact certificate
- `experiments/tpc23_certificate.json` — archived output

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
