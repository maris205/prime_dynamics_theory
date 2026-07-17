# TPC-32 — Matched cutoff frequency gate

This directory contains:

> **Matched Prime–Möbius Cutoff Shells: Rank–Two Factorization,
> Determinant–Frequency Dispersion, and the Distinguished
> Zero–Frequency Gate**

TPC-32 continues the primitive ultra-long residual after TPC-31. It
preserves the signed matching among the two mixed cutoff channels and the
both-ultra channel, restores the actual prime–Möbius row coefficient, proves
unconditional dispersion for almost every determinant frequency, and
compresses the remaining analytic obligation to one quantified
zero-frequency flatness estimate.

## Exact matched shell

For the raw prefix and ultra increment,

\[
\mathsf A_{m,U_0}=\mathsf A_{m,T}+C_m.
\]

Hence the three retained raw channels satisfy

\[
\boxed{
\mathsf A_{m,T}C_n+C_m\mathsf A_{n,T}+C_mC_n
=
\mathsf A_{m,U_0}\mathsf A_{n,U_0}
-\mathsf A_{m,T}\mathsf A_{n,T}.
}
\]

The divisor coefficient is the difference of two rank-one tensors, so it
has algebraic rank at most two and admits an exact symmetric polarization.
This is a matching identity, not an automatic cancellation estimate. The
complete calibrated difference also contains two drift legs, already
bounded by

\[
\ll X^\varepsilon XQ/L.
\]

## Canonical content and prime–Möbius factorization

For

\[
N_m=mj+h,\quad N_n=nj+h,\quad
c=(N_m,N_n),\quad \Delta^\#=(m-n)/c,
\]

the exact-content projector is

\[
\mathbf 1_{(N_m,N_n)=c}
=\sum_{k\ge1}\mu(k)
\mathbf 1_{ck\mid N_m}\mathbf 1_{ck\mid N_n}.
\]

For every modulus \(q\) and frequency \(r\),

\[
\mathbf 1_{(N_m,N_n)\le C}e_q(-r\Delta^\#)
=\sum_{c\le C}\sum_{k\ge1}\mu(k)
\mathbf 1_{ck\mid N_m}\mathbf 1_{ck\mid N_n}
e_{cq}(-r(m-n)).
\]

The lifted phase splits row by row:

\[
e_{cq}(-r(m-n))=e_{cq}(-rm)e_{cq}(rn).
\]

No assumption \((c,q)=1\) is used, and no inverse of \(c\bmod q\) is
introduced.

On the actual squarefree support, if \(w\mid\ell dj+h\), primitivity gives
\((d,w)=1\), so

\[
\boxed{\mu(d)b_R(w)=-\mu(dw)w_R(w).}
\]

This is a genuine prime–Möbius one-leg normal form. It is not, by itself, a
well-factorable sieve weight. The generic row-pair mask is retained as a
joint multiplier; entrywise boundedness does not imply a bounded Schur or
projective norm.

## Unconditional determinant-frequency dispersion

Let \(A_C(n)\) be the signed matched amplitude with canonical content at
most \(C\) and normalized determinant \(n\), and put

\[
N_0=JQ^2\asymp XQ.
\]

For \(C\le J\) and \(C\ll_{\mathscr D}Q\), the inherited physical bounds give

\[
\|A_C\|_1\ll X^\varepsilon N_0,\qquad
\|A_C\|_\infty\ll X^\varepsilon Q(C+J),
\]

\[
\boxed{\|A_C\|_2^2\ll X^\varepsilon N_0^2/Q.}
\]

Choose a prime \(q\asymp Q\) larger than the entire determinant span. Then
there is no residue wrap, and

\[
\boxed{
\frac1q\sum_{r\bmod q}|\widehat A_{C,q}(r)|^2
=\sum_n|A_C(n)|^2.
}
\]

Consequently,

\[
\#\{r\bmod q:|\widehat A_{C,q}(r)|>N_0X^{-\sigma}\}
\ll X^{2\sigma+\varepsilon}.
\]

The classical additive large sieve gives the corresponding Farey-family
estimate. These are unconditional statements and use no unproved Möbius
hypothesis.

## The distinguished zero-frequency gate

Define

\[
\lambda_C(t)=\sum_{\substack{c\mid t\\c\le C}}\mu(t/c).
\]

Then

\[
\mathbf1_{(N_m,N_n)\le C}
=\sum_{t\mid N_m,\ t\mid N_n}\lambda_C(t),
\]

and

\[
\lambda_C(1)=1,\qquad
\sum_{\substack{t\mid g\\t>1}}\lambda_C(t)
=-\mathbf1_{g>C}.
\]

Thus the \(t=1\) term is the untwisted full-content shell, while all \(t>1\)
terms reassemble exactly to minus the already bounded large-content
correction. The cell decomposition does not automatically center the
coefficient needed by the original problem.

The paper defines a zero-frequency flatness exponent by

\[
|\widehat A_{C,q}(0)|^2
\le X^{\chi+o(1)}\sum_n|A_C(n)|^2.
\]

This inequality is an additional hypothesis. If
\(C=X^{\kappa+o(1)}\le J\) and \(C\ll_{\mathscr D}Q\), it rigorously implies every saving below

\[
\min\left\{1-\beta,\ \kappa,\ \frac{\beta-\chi}{2}\right\}
\]

for the complete matched raw shell.

At

\[
\beta=\frac{267}{400},\qquad
C=\lfloor J\rfloor=X^{133/400+o(1)},
\]

the exact threshold is

\[
\boxed{\chi\le\frac1{400}.}
\]

Unconditionally, all but an \(X^{-1/400+o(1)}\) proportion of determinant
frequencies already have every fixed saving below \(133/400\). What remains
is to prove that the distinguished frequency \(r=0\) is not exceptional.

## Sharp boundary

The paper gives two exact obstructions:

- A constant signal on one complete residue system saturates the available
  norm scales, has every nonzero DFT coefficient equal to zero, and still
  has maximal zero coefficient.
- On pairwise coprime targets greater than \(C\), the small-content matrix is
  \(\mathbf J_M-I_M\), with spectrum \(M-1,-1,\ldots,-1\). It retains a
  coherent constant-row mode.

A nine-row primitive finite realization verifies the second obstruction and
the nonzero formal channel polynomial. It is a finite algebraic witness, not
asymptotic evidence for twin primes.

## Exact certificate

Run from this directory:

    python experiments/tpc32_certificate.py
    python -O experiments/tpc32_certificate.py

Both modes perform 488,845 exact checks and regenerate byte-identical JSON.
No floating-point root of unity is used.

Reproducibility values:

- Normalized source SHA-256:
  9ccb7e40d31b4bd23b79df09336fcee6230d95c7a9f1a85da0324fb6eb807d1e
- JSON SHA-256:
  77ac56e2f4f3543224876e8a0374564c81c1b4a9f17800f18ca5249e12954d36
- Certificate digest:
  a890734f5450cda4a7a400f5e1d6379683eb4b9e53a05c8497f256edfdc82c78

The certificate checks finite algebra and exact rational ledgers only. It
does not certify zero-frequency flatness, asymptotic Möbius cancellation, a
Hardy–Littlewood main term, positivity, twin primes, or a breach of sieve
parity.

## Files

- main.tex — paper entry point
- sections/ — section sources
- references.bib — bibliography
- main.pdf — compiled paper
- experiments/tpc32_certificate.py — exact certificate
- experiments/tpc32_certificate.json — archived certificate output

## Build

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
