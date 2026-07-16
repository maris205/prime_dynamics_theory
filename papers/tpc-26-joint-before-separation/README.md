# TPC-26 — Joint before separation

This directory contains:

> **Joint Before Separation in a Primitive Möbius Tail: Both-New Annuli,
> Sharp Symmetric Conductor Ledgers, and Cutoff Stability**

TPC-26 treats the quadratic cutoff difference as one raw annular joint
divisor lattice before smooth, Fourier, or conductor separation. This
recombination joins the two mixed rectangles and the previously open
both-new square, while retaining the two calibrated row drifts with
their correct negative signs.

## Main results

- For the calibrated prefix

  \[
  P_{m,W}(j)=
  \sum_{\substack{u\le W\\u\mid mj+h}}b_R(u)-\delta_H(m),
  \qquad R\le S<T,
  \]

  the paper proves the exact annular identity

  \[
  \begin{aligned}
  P_{m,T}P_{n,T}-P_{m,S}P_{n,S}
  ={}&
  \sum_{\substack{u,v\le T\\\max(u,v)>S}}
  b_R(u)b_R(v)
  \mathbf 1_{u\mid mj+h}\mathbf 1_{v\mid nj+h}\\
  &-\delta_H(m)L_{n;S,T}
  -\delta_H(n)L_{m;S,T}.
  \end{aligned}
  \]

  The \(\delta_H(m)\delta_H(n)\) terms cancel exactly.

- The both-new physical zero kernel has the exact shared-factor form

  \[
  \begin{aligned}
  K^{\square,0}_{S,T}(m,n)
  ={}&
  \sum_{\substack{g\mid m-n\\(g,mnH)=1}}\frac1g
  \sum_{\substack{S/g<c\le T/g\\(c,gmH)=1}}\frac{a(gc)}c\\
  &\times
  \sum_{\substack{S/g<d\le T/g\\(d,gcnH)=1}}\frac{a(gd)}d.
  \end{aligned}
  \]

  Splitting at \(g=SX^{-\kappa}\), endpoint calibration closes the
  small-\(g\) part and determinant divisibility closes the large-\(g\)
  part:

  \[
  K^{\square,0}_{S,T}(m,n)
  \ll_A(\log X)^{-A}+X^{-s+\kappa+o(1)}.
  \]

- TPC-25's actual opened-\(d\) provenance gives \(O(Q^2)\) absolute
  row-pair mass. Consequently the complete physical annular zero mode
  has arbitrary logarithmic saving without a mean-zero test or a new
  projective-mass hypothesis.

- At nonzero frequency, two exact-conductor estimates give the cell
  bound

  \[
  \mathfrak L^{\rm ann}_{Y;S,T}(F_1,F_2)
  \ll QX^\varepsilon
  \sqrt{K_Q(F_1)K_Q(F_2)}
  \min\{\sqrt{JY},F_1F_2\}.
  \]

  For \(1/2\le\beta<1\), the exact relaxed-box minimax is

  \[
  M_\beta(t)=
  \begin{cases}
  1-\beta-t,
  &0\le t\le(1-\beta)/2,\\
  (3-3\beta-2t)/4,
  &(1-\beta)/2\le t\le\beta/2,\\
  (3-\beta-6t)/4,
  &\beta/2\le t\le(3\beta-1)/2,\\
  (\beta+1-4t)/2,
  &t\ge(3\beta-1)/2.
  \end{cases}
  \]

  A nonempty beyond-Poisson annular range survives for every
  \(3/5<\beta<1\). This removes the former \(\beta<2/3\) face only from
  the annular conductor argument.

- Under the stated primitive row, common-weight, off-diagonal-mask,
  no-wrap, support, and fixed-margin hypotheses,

  \[
  \mathcal Q_T^{\rm phys}-\mathcal Q_S^{\rm phys}
  \ll_B XQ(\log X)^{-B}.
  \]

  If an independent matching calibrated \(S\)-cutoff estimate is
  supplied, this also closes the selected calibrated square at \(T\).
  The scalar reassembly from the earlier centered base packet is not
  proved here.

- The strict crossing sample

  \[
  \delta=\frac3{20},\quad
  \beta=\frac{31}{50},\quad
  s=\frac7{20},\quad
  t=\frac{39}{100}
  \]

  has \(S<J<T\) and saving \(1/100\).

- A second sample with

  \[
  \beta=\frac{267}{400}>\frac23,\quad
  s=\frac{23}{60},\quad
  t=\frac{193}{500}
  \]

  lies in the published opened-\(d\) source geometry and has saving
  \(33/8000\). Both endpoints exceed \(J\), so this sample proves
  annular cutoff stability only, not base-square closure.

## Scope

The theorem concerns one selected physical cutoff difference with the
same physical weight and mask at both cutoffs. It does not estimate the
ultra-long \((T,U]\) complement, close the full TPC-18 residual, prove
positivity or a Hardy–Littlewood asymptotic, imply twin primes, or
establish a general breach of sieve parity.

The next explicit wall is a polynomially uniform two-point
affine-Möbius cancellation problem after divisor reflection.

## Exact certificate

Run:

    python experiments\tpc26_certificate.py
    python -O experiments\tpc26_certificate.py

Both modes perform 33,532 explicit exact checks and must regenerate
byte-identical JSON. The certificate uses only the Python standard
library, rational arithmetic, and formal prime-log vectors.

Final hashes:

- JSON SHA-256: 8d751c455635a40ae263e4e61a2cc5edd75a66b28029de89839f2e42d09e0416
- source SHA-256: ddfb3903e86ddb11a29123850e177bd097e622e98a27681c762649c80fccbe1f
- certificate digest: 3dd1bd6ec034009bb7d70525a5f141a6de766a4f99dc0d3824835422c0883337

The certificate checks finite annular identities, the both-new gcd
normal form, formal \(a(gd)\) splitting, CRT densities, the sharp
minimax witnesses and boundaries, and both rational parameter samples.
It is regression control for exact algebra, not numerical evidence for
an asymptotic prime-pair claim.

## Files

- main.tex — paper entry point
- sections/ — section sources
- references.bib — bibliography
- main.pdf — compiled paper
- experiments/tpc26_certificate.py — exact certificate
- experiments/tpc26_certificate.json — archived output

## Build

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
