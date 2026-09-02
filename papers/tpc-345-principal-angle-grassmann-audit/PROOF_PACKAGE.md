# TPC-345 proof package

## Proposition 1 — finite principal-angle definition

For finite matrices `N_1,N_2`, let `Q_1,Q_2` have orthonormal columns spanning
their column spaces.  The singular values of `Q_1^T Q_2` are independent of
the chosen orthonormal bases and define the principal cosines of the two
subspaces.  This is a statement about finite Euclidean spaces.

### Proof

Replacing `Q_i` by `Q_i U_i` for orthogonal `U_i` changes the overlap to
`U_1^T(Q_1^TQ_2)U_2`, which has the same singular values.  A nonsingular
column reparameterization does not change the column space, so its
orthogonal projector is unchanged.  The angles are the arccosines of the
singular values.

## Proposition 2 — finite projection identity

For every finite target `Y` and orthogonal projector `P`,

`text
||Y||_2^2 = ||PY||_2^2 + ||(I-P)Y||_2^2.
`

### Proof

`PY` and `(I-P)Y` are orthogonal, and their sum is `Y`.  The producer and
reverse-shell checker verify the numerical decomposition gap for every
cross-panel and leave-one-control-out projection.

## Proposition 3 — finite geometric certificate

Conditional on the hash-locked source/operator and the declared rank rule,
the six rows produce 216 raw records and 18 LOO angle pairs.  The main
principal cosines, projector distances, transfer retentions, and LOO ranges
are the values in the canonical certificate.  The fixed column shear changes
projector entries by at most `7.65e-15` and principal cosines by at most
`5.56e-16` in the raw audit (the equal-row errors are smaller).

This is a numerically certified finite observation, not an asymptotic
theorem or an arithmetic estimate.

## Explicit non-implications

The package does not prove a canonical nuisance basis, a source-uniform
arithmetic `L2` bound, a uniform masked operator bound, a fixed-power saving,
payment of the strict `1/400` endpoint, an official Route-A/Route-B pass, or
the twin-prime conjecture.
