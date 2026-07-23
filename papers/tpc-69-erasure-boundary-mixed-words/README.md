# TPC-69 — Erasure-Boundary Expansions

**Title:** *Erasure-Boundary Expansions in a Fixed-Shift Native Gram: Mixed Words, Residual Parity, and Cross-Key Holonomy*

This paper continues the fixed-shift missing-native operator route of
TPC-61 and TPC-68. It makes no arithmetic cancellation assumption and no
twin-prime claim.

## Main exact results

- The same-residual and unequal-residual defects decompose over complete
  native keys:
  \[
  R=\sum_iR_i,\qquad E=\sum_iE_i.
  \]
- At one key, \(R_i\) is block diagonal in residual labels and \(E_i\) is
  off block. Therefore
  \[
  \operatorname{tr}(E_iP(R_i))=0.
  \]
- The half-sector in the first mixed second-moment coefficient is
  necessarily a two-key rectangle:
  \[
  S_{2,1}=2\operatorname{tr}(ER),\qquad
  \operatorname{tr}(ER)=\sum_{i\ne j}\operatorname{tr}(E_iR_j).
  \]
- Its four literal coefficients form a gauge-invariant cross-key holonomy.
  The four target Möbius signs reduce exactly to the two residual signs on
  the unequal-residual edge.
- The coefficient \(S_{k,b}\) of \(t^b\) in
  \(\operatorname{tr}(R+tE)^k\) has an exact noncommutative cyclic
  composition formula.
- On every decorated closed walk, all row gauges and same-residual signs
  telescope. The remaining target sign is the product over the odd-degree
  boundary of the residual-label multigraph formed by erasure edges.
- For every \(q\ge1\), the full exactly-two-erasure sector satisfies
  \[
  S_{2q,2}\ge0.
  \]
  The proof is an exact divided-difference calculation for the increasing
  odd power \(x^{2q-1}\).

## Claim boundary

The paper proves finite-dimensional algebra (L0) and its identification
with the complete fixed-\(h_0\) carrier (L1). It does **not** prove:

- a saving for the cross-key rectangle sum;
- a uniform star or even-moment bound;
- a subpower native defect;
- missing-mass, represented-frame, or nuisance-shorting estimates;
- a parity-breaking, prime-pair, or twin-prime theorem.

Every future arithmetic input must retain the complete native keys, use the
one fixed physical shift, and fit the strict \(1/400\) endpoint ledger.

## Build

Run:

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The archival PDF is `erasure-boundary-mixed-words.pdf`.
