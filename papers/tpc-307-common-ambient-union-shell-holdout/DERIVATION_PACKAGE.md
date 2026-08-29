# TPC-307 derivation package

## Frozen finite object

For an adjacent pair `(Q_L,Q_R)`, let `S_L` and `S_R` be the two locked prime
shells from TPC-302.  Define

```text
U   = S_L union S_R
O   = S_L intersect S_R
E_L = S_L \ O
E_R = S_R \ O.
```

The four sets are finite, `E_L` and `E_R` are disjoint, and `U` is their
disjoint union with `O`.  A single physical row operator `V_U` is built by
using every prime in `U` in the fixed literal kernel formula.  The profile
matrix and source Gram matrix are frozen from the source window
`[257,512]`, `H=58`, `z=5`, with profile cutoffs
`(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61)`.

## Why there are two directional targets

Let `a_L:S_L -> {-1,+1}` and `a_R:S_R -> {-1,+1}` be the source-first labels.
The optimal global alignment sign is

```text
sigma = sign(sum_{p in O} a_L(p) a_R(p)),
```

with `sigma=+1` at a zero inner product.  The aligned right label is
`a_R^sigma=sigma a_R`.  The left direction fits `a_L|_O` and tests against
`a_L|_{E_L}`; the right direction fits `a_R^sigma|_O` and tests against
`a_R^sigma|_{E_R}`.

There is generally no well-defined union target: on `O`, `a_L` and
`a_R^sigma` can disagree.  Replacing them by an arbitrary coordinate-wise
choice would change the estimand.  TPC-307 therefore shares the ambient
operator and fit geometry, but keeps the two directional target tasks
separate.

## Constrained profile frontier

For a target `b` on the overlap and a prefix length `k`, write `V_{O,k}` for
the corresponding rows of the first `k` profiles and `M_k` for the leading
principal block of the source Gram matrix.  At tolerance `tau`, define

```text
B_k,tau(b) = min c^T M_k c
             subject to ||V_{O,k} c - b||_2 <= tau ||b||_2.
```

The first feasible prefix for each direction is `k_L` or `k_R`.  Since
prefixes are nested, `k=max(k_L,k_R)` is feasible for both.  Both directional
budgets are evaluated at this common `k`; the prediction is then made on all
rows of `U`, while the fit never reads the exclusive rows.

The holdout statistic is

```text
H_X = |E_X|^{-1} sum_{p in E_X} ( (V_U,k c_X)[p] - a_X^sigma(p) )^2,
```

for `X=L,R`.  The budget ratio and holdout ratio are both recorded as
right-over-left.  A ratio below `0.9` is a strict right-lower class, one above
`1.1` is a strict left-lower class, and the interval between is unresolved.

## Data-type boundary

The protocol and partition lemmas are exact finite statements.  The published
atlas is a high-precision numerical replay of a vectorized double-precision
literal formula followed by an `mpmath` frontier solve, with relative padding
`1e-5`.  It is deliberately labelled `NUMERICALLY_REPRODUCED_FINITE`, not a
directed-rounding or formal interval certificate.  The independent NumPy
checker reconstructs the object without importing the producer and verifies
the printed enclosures with an explicit replay slack.
