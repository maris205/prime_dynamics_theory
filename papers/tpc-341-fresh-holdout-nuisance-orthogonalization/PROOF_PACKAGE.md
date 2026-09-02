# TPC-341 proof and scope package

## Proposition 1 - finite orthogonal decomposition

Let `N` be any finite real matrix and let `P_N` be the Euclidean orthogonal
projector onto its column span.  For every finite vector `y`,

```text
||y||_2^2 = ||P_N y||_2^2 + ||(I-P_N)y||_2^2.
```

**Proof.**  Both `P_N y` and `(I-P_N)y` lie in orthogonal subspaces, and their
sum is `y`.  Apply the Pythagorean identity.  `QED`.

## Proposition 2 - holdout statistic

For a nonzero held-out response `y`, the residual fraction

```text
rho_N(y) = ||(I-P_N)y||_2^2 / ||y||_2^2
```

lies in `[0,1]`.  It is invariant under rescaling `y` and measures only the
distance of that finite vector from the declared nuisance span.

**Proof.** Proposition 1 gives nonnegative numerator and denominator, and the
residual energy is no larger than the total energy.  `QED`.

## Finite certificate

The fresh panel has 108 raw class/control records, 90 nonempty records, three
in-sample projections, and 27 leave-one-control-out projections.  All rank and
Pythagorean checks pass.  The nine-control mean retains only
`0.2010894086--0.2560626551` of the twin energy after nuisance projection,
equivalently removes `0.7439373449--0.7989105914`.

The hostile held-out test retains `0.4435267486--0.8904473564` of the omitted
twin-output energy.  Therefore the declared aggregate removal does not
transfer to individual held-out controls on this finite panel.

## Scope boundary

The projection identities are exact finite linear algebra.  The retention
ranges and the control-stability obstruction are finite numerical observations
for three cutoff-safe windows and nine chosen controls.  They provide no
growing arithmetic estimate, no twin-prime theorem, and no fixed-power credit.
The nuisance projection is a modeling choice and must not be advertised as a
canonical arithmetic decomposition.
