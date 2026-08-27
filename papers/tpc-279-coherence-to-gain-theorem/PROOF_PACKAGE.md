# TPC-279 proof package

## Theorem 1 — exact deficit criterion

For four vectors with `D>0`,

```text
0 <= G/D <= 4,
G-D = 2E,
Delta = (D-G)/D = -2E/D.
```

If `G>0`, `r=D/G=(1-Delta)^(-1)`.  Hence
`r>=b X^gamma` is equivalent to `G/D<=b^(-1)X^(-gamma)`, and to
`Delta>=1-b^(-1)X^(-gamma)`.  The proof is expansion, Cauchy--Schwarz, and
positive reciprocal order.  The case `G=0` is the exact zero-sum endpoint and
has infinite extended gain.

## Theorem 2 — sharp pairwise envelope

With `a_j=||V_j||` and pairwise absolute coherence `mu`,

```text
G <= D + 2 mu sum_{j<k} a_j a_k
  = D + mu*((sum_j a_j)^2-D)
  <= (1+3mu)D.
```

Together with `G<=4D`, this proves the stated envelope and reciprocal floor.
The Gram matrix `(1-mu)I+mu 11*` is positive semidefinite with eigenvalues
`1-mu` (three times) and `1+3mu`; its four unit-vector realization attains
every bound.  Thus the constants are sharp.

## Theorem 3 — coherence firewall

The orthogonal witness has `mu=0` and `r=1` at every scale, so no theorem using
only a bounded absolute pairwise coherence can imply a positive-power gain.
The near-cancellation scalar family shows that large gain requires the
aggregate ratio `G/D` to be small even when `mu=1`.

## Transfer certificate

The exact TPC-278 parent result is hash-locked in the producer.  Its outward
gain intervals are inverted with reversed endpoints, and the resulting
deficit intervals are intersected with the parent cancellation intervals.
An independent checker recomputes every reciprocal and overlap using
`Fraction`; a six-mutation stress test rejects theorem, interval, parent,
sharpness, and power-credit tampering.
