# TPC-10: factor-scale localization of a prime-target residual

This directory contains the manuscript

> *Factor-Scale Localization of a Prime-Target Residual: Hard-Edge Bulk
> Persistence, Type-I Resolution, and Finite-Mellin Minimax Barriers*.

## Main results

For fixed nonzero h, compactly supported smooth W, and

~~~text
nu_X,h
  = sum_{m,n >= 1}
      (Lambda(n)-1) Lambda(m*n+h) W(m*n/X)
      delta_{log(n/m)},
~~~

the paper proves the following.

1. **Two-sided hard-edge bulk persistence.** Uniformly for
   2 <= Y <= X^(1/3),

   ~~~text
   sum_{m,n > Y}
     (Lambda(n)-1) Lambda(m*n+h) W(m*n/X)
   = (1-C_h) I_0(W) X log X + O_h,W(X log(2Y)).
   ~~~

   The analogous form with Lambda(n) in place of Lambda(n)-1 has leading
   coefficient I_0(W). Hence the leading coefficient survives whenever
   log(2Y)=o(log X) and it is nonzero.

2. **Arbitrary fixed smooth scale resolution in the Type-I range.** For
   D <= sqrt(X)/(log X)^B, every fixed V in C_c^1(R), and every center s,
   maximal Bombieri--Vinogradov gives

   ~~~text
   sum_{n <= D,m}
     (Lambda(n)-1) Lambda(m*n+h) W(m*n/X)
     V(log(n/m)-s)

   = X sum_{n <= D,(n,h)=1} (Lambda(n)-1)/phi(n)
       integral W(u) V(log(n^2/(X*u))-s) du
     + O_A(X/(log X)^A),
   ~~~

   uniformly in s.

3. **Exact finite-Mellin minimax boundary.** On a total-variation ball,
   the optimal worst-case error from finitely many Mellin samples or jets
   is exactly the uniform distance of the desired window from the
   corresponding exponential-polynomial space. Nonlinear estimators do not
   improve the radius.

4. **Exact divisor-grid certificate.** On the genuine prime-target row
   3^4+2=83, the profiles

   ~~~text
   (1,0,6,0,1)/8  and  (0,4,0,4,0)/8
   ~~~

   have identical Mellin jets through order three but central-window masses
   3/4 and 0. The exact minimax radius is 3/8.

5. **Arithmetic Taylor interface and exact endpoint reduction.** The first
   nonconstant Taylor coefficients contain two-von-Mangoldt convolutions.
   After a two-Mellin demodulation, an all-frequency sinc-squared kernel
   isolates the m=1 layer exactly. Its predicted asymptotic is equivalent
   to the weighted fixed-shift Hardy--Littlewood problem.

## Strict boundary

The paper proves no localized asymptotic for the complete long-factor tail,
signed Type-II cancellation, fixed-shift prime-pair asymptotic, twin-prime
lower bound, new level of distribution, or breach of the sieve parity
barrier. The minimax witnesses are adversarial coefficient profiles on
genuine divisor nodes; they are not the actual Lambda(n)-1 profile.

## Build

~~~bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
~~~

## Exact certificate

~~~bash
cd experiments
python exact_mellin_certificate.py \
  --output data/exact-mellin-certificate.json
python -m unittest -v test_exact_mellin_certificate.py
~~~

The certificate uses only Python's standard library and exact rational
arithmetic.

## Directory layout

- 'main.tex': manuscript driver and abstract.
- 'factor-scale-localization.pdf': compiled manuscript.
- 'sections/': modular manuscript sections.
- 'references.bib': bibliography.
- 'experiments/exact_mellin_certificate.py': exact certificate generator.
- 'experiments/test_exact_mellin_certificate.py': eight exact tests.
- 'experiments/data/exact-mellin-certificate.json': deterministic artifact.
