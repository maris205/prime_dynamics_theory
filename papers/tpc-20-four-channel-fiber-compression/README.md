# TPC-20 — Four-channel fiber compression

This directory contains:

> **Four-Channel Compression in a Primitive Möbius Tail: Centered Divisor
> Kernels, a Single-Leg Completion Wedge, and CRT-Fiber Discrepancy**

TPC-20 supplies the common-channel algebraic reduction left open by TPC-19
and sharpens the long-period spectral interface. It does **not** prove the
TPC-18 residual-dispersion estimate, a fixed-shift Hardy–Littlewood
asymptotic, a twin-prime lower bound, a breach of sieve parity, or a spectral
realization of zeta zeros.

Throughout, \(H=\operatorname{rad}|h|\).

## Main results

- The complete combination **PP - PM - MP + MM** has the exact pointwise
  form
  \[
  Z_m(j)=\varepsilon_U(m)+
  \sum_{\substack{u\le U\\(u,mH)=1}}
  b_R(u)\left(\mathbf1_{u\mid mj+h}-\frac1u\right),
  \qquad b_R(u)=-\mu(u)w_R(u).
  \]
- A uniform Möbius calibration theorem proves
  \[
  \varepsilon_U(m)\ll_A\rho_{P,H}(m)(\log U)^{-A}
  \]
  throughout every fixed polynomial row range. A self-contained \(L^1\)
  argument makes this scalar defect negligible with arbitrary logarithmic
  saving in separated packets in the single-leg completion wedge.
- The primitive-conditional centered-kernel zero mode is
  \[
  \frac{b_R(u)b_R(v)}{uv}
  \left((u,v)\mathbf1_{(u,v)\mid m_1-m_2}-1\right).
  \]
  The zero mode of every coprime divisor pair vanishes termwise before any
  absolute value is taken.
- On the true period \(H[u,v]\), all four compatible Fourier phases align
  and produce
  \[
  B_{g,a,b}(r)
  =g-\mathbf1_{b\mid r}-\mathbf1_{a\mid r}
   +\mathbf1_{[u,v]\mid r},
  \quad u=ga,\ v=gb.
  \]
  The paper gives its exact frequency count, square energy, and the exact
  kernel Plancherel identity.
- Completing the two single legs at periods \(Hu\) and \(Hv\) yields the
  strict-margin range in which all short–short single and constant spectra
  complete,
  \[
  Q\le X^{1/2+\delta-\eta_0},
  \]
  wider than the whole-joint-period range
  \(Q\le X^{2\delta-\eta_0}\). On the genuinely remaining low joint
  frequencies, however, \(B_{g,a,b}(r)=g\), so matching creates no further
  nonzero-frequency cancellation.
- Compatible row pairs are aggregated by one joint CRT class
  \(\kappa\bmod [u,v]\). The three inverse phases of TPC-19 become one
  ordinary finite Fourier transform. Its exact mean/discrepancy split is
  \[
  S_q(r)=\overline Z_qc_q(r)+\widehat D_q(r),\qquad
  \sum_{r\bmod q}|\widehat D_q(r)|^2
  =q\sum_{\kappa\in(\mathbb Z/q\mathbb Z)^\times}|D_q(\kappa)|^2.
  \]
- For the chosen compatible short–short packet, the remaining analytic
  obligations are explicit: control the weighted restricted-frequency
  CRT-fiber discrepancy (or an explicitly normed low-rank substitute), and
  separately control the Ramanujan mean packet. The cited separated
  Kloosterman-fraction and frequency-concentration theorems do not
  automatically supply these inputs for the sharp modulus-dependent Möbius
  fiber vector. The large-divisor legs remain outside this reduction.

## Files

- **main.tex** — paper entry point
- **sections/** — section sources
- **references.bib** — bibliography
- **main.pdf** — compiled paper
- **experiments/tpc20_certificate.py** — exact deterministic certificate
- **experiments/tpc20_certificate.json** — certificate output

## Reproduce the exact certificate

From this directory:

~~~powershell
python experiments\tpc20_certificate.py
python -O experiments\tpc20_certificate.py
~~~

Both modes must pass and regenerate byte-identical JSON. At the archived
version:

- JSON SHA-256:
  **0F994F32950AC68B8249D2F90E7074176106C122A2AE53268370F03584B7C12B**
- script SHA-256:
  **55D9FA7DD4277C541ABE39C53231453F7F6A9107DEF40103F5227373B53E0174**

The standard-library certificate uses exact integers, rational arithmetic,
formal prime-log polynomials, and finite prime fields with roots of the exact
required orders. It checks the common recombination, finite calibration
convolution, full kernel DFT, multiplier count and energy, kernel and fiber
Parseval identities, CRT-fiber compression, sign migration, and the exponent
ledger. Its finite diagnostics are explicitly marked as non-asymptotic and
all twin-prime, residual-dispersion, and asymptotic evidence flags are false.

## Build the paper

~~~powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
~~~
