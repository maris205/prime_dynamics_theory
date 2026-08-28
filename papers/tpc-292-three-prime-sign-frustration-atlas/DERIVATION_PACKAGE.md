# TPC-292 derivation package

## 1. Signed triangle compatibility

For three nonzero Gram edges put
`s_12=sign(G_12)`, `s_13=sign(G_13)`, and `s_23=sign(G_23)`.  A coefficient
sign assignment `a_1,a_2,a_3` makes every pairwise cross contribution
nonpositive precisely when

```text
a_i a_j s_ij = -1       for (i,j)=(1,2),(1,3),(2,3).
```

Multiplying the three equations gives `s_12 s_13 s_23=-1`, since every
`a_i` occurs twice.  Conversely, if the product is `-1`, take
`a_1=1`, `a_2=-s_12`, and `a_3=-s_13`; the third equation follows from the
product condition.  Thus the criterion is both necessary and sufficient.

## 2. Three-vector projection

Let `g_i,g_j,g_k` have Gram matrix `G`, and write `d_r=G_rr`.  For target
`g_i`, let `M=G_{(j,k),(j,k)}` and `v=(G_ij,G_ik)^T`.  The least-squares
coefficients solve `M(alpha,beta)^T=v`, and the normalized residual is

```text
min_{alpha,beta} ||g_i-alpha*g_j-beta*g_k||^2 / d_i
  = (d_i-v^T M^(-1)v)/d_i
  = det(G)/(d_i det(M)).
```

The last equality is the block determinant identity.  A positive pair minor
is enough for uniqueness; Gram positive semidefiniteness makes the residual
nonnegative.

## 3. Volume normalization

For the three vectors, `det(G)/(d_i d_j d_k)` is the squared volume after
normalizing each vector to unit length.  It is independent of the target
chosen for the Schur calculation.  It is a geometric rank diagnostic, not
an arithmetic density estimate.

## 4. Route consequence

Pairwise low residuals do not imply a common signed direction.  On a triangle,
the exact parity rule identifies the obstruction before coefficient
magnitudes are optimized.  The next natural test is therefore a signed-graph
max-cut/frustration calculation on whole prime shells, followed by a test of
whether the actual literal source coefficient image can realize the surviving
sign pattern.
