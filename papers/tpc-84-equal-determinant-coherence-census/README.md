# TPC-84: Conditional Equal-Determinant Coherence Gate

This directory contains:

> *Equal-Determinant Coherence: Sharp Fiber Phase Envelopes, a
> Conditional Positive-Coherence Gate, and a Census Schema*.

## Main result

Let \(u_t\) be the literal native triplet weights in the matched
TPC-32 packet, let \(F_n=\{t:\nu_t=n\}\), and set

\[
A(n)=\sum_{t\in F_n}u_t,\qquad
R=\sum_t|u_t|,\qquad
M=\sum_n|A(n)|,\qquad
D=\sum_n|A(n)|^2.
\]

For a fiber with moduli \(r_1,\ldots,r_m\), total
\(R_f=\sum_i r_i\), and maximum \(r_{\max}\), the exact set of
possible resultant magnitudes is

\[
\left[(2r_{\max}-R_f)_+,\,R_f\right].
\]

Consequently, magnitude data alone give the sharp global lower
envelope

\[
M\ge M_{\min}^{\rm mag}
 :=\sum_n(2r_{\max,n}-R_n)_+,
\]

and no stronger phase-blind lower bound is possible.
Endpoint sharpness is in the unrestricted free-phase comparison class;
it does not assert that the coupled phases of the literal physical
packet realize either extremizer.

The determinant energy decomposes exactly as

\[
D=E_{\rm trip}+C_{\rm eq},
\]

where

\[
E_{\rm trip}=\sum_t|u_t|^2
\]

and \(C_{\rm eq}\) is the ordered off-diagonal correlation inside
equal-determinant fibers. In the high-\(\beta\) regime
\(C=\lfloor J\rfloor\ll Q\), the inherited TPC-32 L1 bounds give

\[
E_{\rm trip}\ll_\varepsilon X^\varepsilon JQ^2
\asymp X^{-1+\varepsilon}Q^3J^2.
\]

Thus any determinant-energy lower bound with a fixed loss
\(\lambda_D<1\) forces a positive off-diagonal contribution
\(C_{\rm eq}=(1-o(1))D\). Complete decorrelation is therefore not the
desired mechanism: the diagonal upper bound is at least one full
power below the natural scale, up to soft factors. This is a
conditional necessity statement, not a positive-coherence lower
bound.

If

\[
R\ge X^{-\lambda_R+o(1)}N_0,\qquad
M\ge X^{-\lambda_{\rm fib}+o(1)}R
\]

and the actual determinant support has size \(O(Q)\), then

\[
D\ge X^{-2(\lambda_R+\lambda_{\rm fib})+o(1)}
Q^3J^2.
\]

The paper converts this formula into an audit-ready proposed census
schema for testing exact duplicates, determinant-preserving
symmetries, shared-target/shared-divisor pairings, and the unpaired
remainder. It also specifies a scalable determinant aggregation:
external sort or streaming by the exact determinant key, computation
of \(C_{\rm eq}=D-E_{\rm trip}\), and class-specific compressed joins.
No census has been executed, and this directory contains no native
archive or census data.

## Scope

- The sharp phase envelope and the identity
  \(D=E_{\rm trip}+C_{\rm eq}\) are finite-dimensional L0 results.
- The TPC-32 support and diagonal estimates are L1 physical imports,
  valid here only in the high-\(\beta\) domain
  \(C=\lfloor J\rfloor\ll Q\).
- The archive schema and proposed census protocol form an L1
  interface; they are not an executed census.
- A growing-scale lower bound for \(R\), \(M\), or \(C_{\rm eq}\) is
  L2 and is not proved here.
- Existing TPC-32 axioms provide upper bounds only. Bounded
  coefficients may vanish or be rescaled, so they cannot imply a
  uniform raw-mass lower bound.
- The physical fixed-power loss must remain strictly below `1/400`;
  equality is a stop.
- The certified determinant-energy condition
  \(\lambda_D^{\rm cert}\le 2\eta_Z\) and the physical endpoint
  condition \(\Lambda_{\rm phys}<1/400\) are separate ledgers.
  The former is not automatically added to the latter without a
  proved crosswalk.

## Claim boundary

The paper proves no fixed-\(2\) estimate, no parity breakthrough, no
Hardy--Littlewood asymptotic, no prime-pair lower bound, and no
twin-prime conclusion. A broad affine theorem that contains
\(\mu(t)\mu(t+1)\) as a specialization would include an unproved
two-point Chowla case; the restricted high-row packet is not claimed
equivalent to classical Chowla.

## Build

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archival filename is
`equal-determinant-coherence-census.pdf`.
