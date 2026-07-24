# TPC-86: Stable zero-arc Fourier reassembly

This paper corrects and sharpens the role of nonzero determinant
frequencies in the fixed-shift TPC route.

For a finite coefficient \(A:\mathbb Z/q\mathbb Z\to\mathbb C\),
write

\[
Z=\widehat A(0)=\sum_n A(n),\qquad
D=\sum_n|A(n)|^2.
\]

If \(A(0)=0\), Fourier inversion gives

\[
Z=-\sum_{r\ne0}\widehat A(r).
\]

Thus nonzero frequencies can control the distinguished zero mode,
but only through their coherent signed reassembly.

## Main results

- If \(K\) is the actual zero set, every normalized weight \(w\)
  supported on \(K\) gives

  \[
  Z=-\sum_{r\ne0}m_w(r)\widehat A(r).
  \]

- Within the zero-set-averaged class, the unique
  minimum-\(\ell^2\) kernel is uniform on \(K\), with

  \[
  \sum_{r\ne0}|m_K(r)|^2
  =\frac{|\operatorname{supp}A|}
  {q-|\operatorname{supp}A|}.
  \]

- Parseval then recovers exactly the sharp support bound

  \[
  |Z|^2\le |\operatorname{supp}A|D.
  \]

- Positive-density zero-arc padding permits a fixed \(k\)-fold
  interval filter satisfying

  \[
  \sum_{r\ne0}|m_k(r)|=O_k(1),\qquad
  |m_k(r)|\ll_k d_q(r,0)^{-k}.
  \]

- For the literal TPC-32 packet,

  \[
  |Z_X|\ll_k
  \max_{0<d_q(r,0)\le R}|\widehat A_X(r)|
  +X^{o(1)}N_{0,X}R^{1/2-k}.
  \]

- At \(\beta=267/400\), the triangular filter \(k=2\) needs only

  \[
  R=X^{133/600+\varepsilon},
  \]

  for sufficiently small fixed \(\varepsilon>0\), rather than all
  \(q=X^{267/400+o(1)}\) nonzero frequencies.

- Exceptional frequencies are charged by reconstruction-multiplier
  mass and Fourier energy. Cardinality alone is not the relevant
  currency.

- Mean-square dispersion alone cannot improve the sharp support
  bound.

## Physical status

The stronger auxiliary padding leaves a zero arc of positive density
without changing the literal high-\(\beta\), fixed-\(h_0\)
coefficient. The finite filter and its attachment to the inherited
TPC-32 energy upper bound form an exact L0/L1 reduction. The required
low-frequency fixed-shift Möbius cancellation remains L2.

The paper does not specialize to \(h_0=2\), prove a parity
breakthrough, establish a prime-pair lower bound, or imply the twin
prime conjecture.

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

```text
stable-zero-arc-fourier-reassembly.pdf
```
