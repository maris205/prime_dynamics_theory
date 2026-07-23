# TPC-76: divisor-poset content lifts

TPC-76 studies a literal, provenance-compatible nonprimitive
completion of the TPC-74 direct-entry kernels.

## Main results

- If \(L_q(u,v)\) denotes the actual primitive kernel at content
  \(q\mid |\Delta|\), the content lift is
  \[
  F^{\mathrm Z}(du,dv)
  =
  \sum_{d\mid q\mid|\Delta|}L_q(u,v),
  \qquad (u,v)=1.
  \]
- The diagonal profiles are the zeta transform on the divisor lattice and
  are exactly invertible:
  \[
  L_q(u,v)
  =
  \sum_{q\mid d\mid|\Delta|}
  \mu(d/q)F^{\mathrm Z}(du,dv).
  \]
- Every auxiliary diagonal slice with index \(a\nmid|\Delta|\) vanishes
  exactly.  Thus the nonprimitive completion has a finite,
  fixed-shift-compatible diagonal filtration rather than an ambient
  unrestricted tail.
- A general provenance-compatible filter \(W=(w_{d,q})\), with
  \(w_{1,q}=1\) and \(w_{d,q}=0\) unless \(d\mid q\), gives an affine
  completion class containing both the zero and zeta lifts.
- The optimal provenance-compatible cost has an exact reduced dual:
  \[
  \min_\theta\|A(F^0+B_L\theta)\|_1
  =
  \max_{\|z\|_\infty\le1,\ B_L^*A^*z=0}
  \operatorname{Re}\langle z,AF^0\rangle .
  \]

These are L0/L1 carrier and certificate results.  No asymptotic saving,
Perron decay, fixed-\(2\), parity-breaking, prime-pair, or twin-prime
claim is made.

The archival PDF is `divisor-poset-content-lifts.pdf`.

## Build

Run

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
