# TPC-73: Primitive-Support Collapse and the Analytic Completion Gate

This paper begins the TPC-73--TPC-82 block at the first live gate isolated
by TPC-72.

## Main results

- The literal erasure coordinates are canonical:
  \(q=(S_m,S_n)\), \(S_m=qu\), \(S_n=qv\), and \((u,v)=1\).
  Therefore the support-faithful physical kernel is identically zero away
  from the primitive lattice.
- For that canonical zero completion, every diagonal dilation
  \(K^{[d]}(x,y)=K(dx,dy)\) with \(d\ge2\) vanishes.  The auxiliary
  diagonal tail of TPC-71 is exactly zero for this extension, and the
  divisor-lifted expansion collapses to its \(d=1\) slice.
- The physical anchored coefficient has the exact tail-free Abel form
  \[
  \mathfrak X_{\mathfrak a}
  =
  \mu(a)\mu(b)
  \sum_{x,y}M(x)M(y)\Delta_{12}K_{\mathfrak a}^{0}(x,y).
  \]
- Mixed variation is the coefficient mass in the unique terminal-rectangle
  decomposition of a finitely supported kernel.  Diagonal downsampling is
  a contraction for this norm.
- The physical sum depends only on primitive data, but an analytic
  completion away from the primitive lattice can trade a smaller \(d=1\)
  variation against nonzero higher diagonal slices.  Completion cost is
  therefore an analytic gauge, not a new physical mass.
- The canonical completion closes its auxiliary diagonal-tail bookkeeping
  exactly.  It does not prove that the remaining mixed variation is small,
  and it gives no operator-norm estimate.

## Claim boundary

The finite-kernel identities are L0.  The canonical primitive-support
identification for the literal fixed-\(h_0\) erasure kernel is L1.  No
mass-normalized variation saving for the physical kernel, no completed
first-mixed-trace estimate, no operator saving, no parity-breaking estimate,
and no prime-pair or twin-prime theorem is proved.

## Build

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archival PDF is `primitive-support-completion-gate.pdf`.
