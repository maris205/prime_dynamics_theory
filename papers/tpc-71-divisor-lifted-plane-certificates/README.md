# TPC-71: Divisor-Lifted Primitive-Plane Certificates

This directory contains:

> *Divisor-Lifted Möbius Certificates on the Primitive Cofactor Plane:
> Two-Dimensional Abel Summation, Coprimality Tails, and the Physical
> Variation Gate*.

## Main results

- The primitive sign satisfies the exact identity
  \[
  \mathbf 1_{(u,v)=1}\mu(u)\mu(v)=\mu(uv).
  \]
- A diagonal divisor lift converts every finitely supported primitive-plane
  sum into restricted one-variable Möbius sums at fixed divisor \(d\).
- Two-dimensional Abel summation gives an exact certificate in terms of
  restricted Mertens envelopes and the zero-extended mixed variation of
  \(K(da,db)\).
- The diagonal tail is at most
  \[
  \|K\|_\infty UV/D.
  \]
- Since \(M_d(x)=o(x)\) for each fixed \(d\), every family satisfying
  \(\mathcal V_\square(K^{[d]})=O_d(\|K\|_\infty)\) satisfies
  \[
  \sum_{u\le U,v\le V,(u,v)=1}\mu(u)\mu(v)K(u,v)
  =o(\|K\|_\infty UV).
  \]
- The unweighted primitive rectangle therefore cancels unconditionally.
- In the physical TPC-70 cross-key coefficient, the excluded direction is
  one primitive-plane site and is already zero in the literal erasure
  kernel. The certificate controls each anchored four-corner sum and hence
  \(\operatorname{tr}(ER)\).
- The remaining inputs are mass-normalized mixed variation, the diagonal
  and short-ray tails, summability over anchors, and a genuinely new
  trace-to-operator bridge.
- Sign-selected hard masks show that bounded amplitude alone cannot imply
  cancellation.

## Claim boundary

The divisor identities, Abel formula, smooth-kernel theorem, and anchored
trace majorants are L0. The exact TPC-70 primitive-plane crosswalk is L1.
No bound for the actual prime-line kernel's mixed variation, no direct
operator saving, no fixed-\(2\) parity improvement, and no prime-pair or
twin-prime theorem is claimed.

## Build

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archival PDF is `divisor-lifted-plane-certificates.pdf`.
