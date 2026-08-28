# TPC-293 derivation package

## Signed-shell objective

Let `g_1,...,g_m` be nonzero physical prime components and let
`G_ij=<g_i,g_j>`. Assume the off-diagonal entries used below are nonzero,
and put `sigma_ij=sign(G_ij)`. For a coefficient-sign vector
`a in {−1,+1}^m`, call an edge favorable when

```text
a_i a_j sigma_ij = -1.
```

The finite signed-shell value and frustration index are

```text
F(sigma) = max_a #{i<j : a_i a_j sigma_ij=-1},
fr(sigma) = binom(m,2) - F(sigma).
```

Global reversal `a -> -a` leaves every edge decision unchanged. More
generally, switching vertex labels by `t_i` replaces `sigma_ij` by
`t_i sigma_ij t_j` and preserves `F`; this is the signed-graph gauge
symmetry proved directly in the proof package.

## All-positive benchmark

When every `sigma_ij=+1`, favorable edges are exactly the edges crossing the
partition `P={i:a_i=+1}` and `P^c`. If `|P|=r`, their number is
`r(m-r)`. Completing the square gives

```text
r(m-r) = m^2/4 - (r-m/2)^2 <= floor(m^2/4),
```

with equality at the two most balanced partitions. Thus the all-positive
frustration benchmark is `binom(m,2)-floor(m^2/4)`.

## Why this is only a sign layer

The physical quadratic form is

```text
||sum_i c_i g_i||^2 = sum_i c_i^2 G_ii
                       + 2 sum_{i<j} c_i c_j G_ij.
```

The signed objective replaces the magnitudes `|G_ij|` by unit weights and
restricts coefficients to signs. Therefore a larger `F` need not imply a
smaller physical norm. TPC-293 intentionally records this separation and
passes the magnitude-weighted question to the next stage.

## Finite construction

For each declared row `(N,H,Q,z,s)`, the frozen source produces exact
rational vectors `g_q` for primes `Q<q<=2Q`. Their pairwise integer/rational
Gram signs define one complete signed graph. The producer enumerates all
`2^(m-1)` labelings after fixing the first label to `+1`, records one optimum,
and counts all optimum classes. The same construction is independently
replayed with the physical accumulation order transposed.

The 18 rows contain 1,380 edges and 5,727 triangles. The only nonzero
finite gain occurs in the `s=1`, `(256,38,27,5,1)` row: its three negative
edges raise `F` from 12 to 15. All other rows are all-positive at the edge
sign level.
