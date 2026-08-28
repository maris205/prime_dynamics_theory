# TPC-292 proof package

## Theorem 1 — triangle sign parity

Let `G_12,G_13,G_23` be nonzero real numbers.  There are signs
`a_1,a_2,a_3` in `{−1,+1}` satisfying
`a_i a_j sign(G_ij)=-1` on all three edges if and only if
`sign(G_12 G_13 G_23)=-1`.

**Proof.** Necessity follows by multiplying the three required equations:
the coefficient signs occur twice and disappear, leaving the product of the
edge signs equal to `(-1)^3=-1`.  For sufficiency set
`a_1=1`, `a_2=-sign(G_12)`, and `a_3=-sign(G_13)`.  The first two edges have
the required sign.  On the third edge,
`a_2 a_3 sign(G_23)=sign(G_12 G_13 G_23)=-1`. ∎

The complementary case, product `+1`, is called sign-frustrated here: at
least one of the three pairwise cross terms remains positive for every
coefficient-sign assignment.

## Theorem 2 — three-vector Schur identity

Let `g_1,g_2,g_3` be vectors, let `G` be their Gram matrix, and assume the
two-vector Gram minor on the non-target vectors is positive.  For target `i`,

```text
min_{alpha,beta} ||g_i-alpha*g_j-beta*g_k||^2 / ||g_i||^2
 = det(G)/(G_ii det(G_(j,k),(j,k))).
```

**Proof.** Write the square as
`d_i-2 v^T c+c^T M c`, where `M` is the two-vector Gram block and `v` is
the target cross vector.  Positive definiteness of `M` gives the unique
minimizer `c=M^(-1)v` and minimum `d_i-v^T M^(-1)v`.  The block determinant
formula gives `det(G)=det(M)(d_i-v^T M^(-1)v)`.  Divide by `d_i det(M)`.
∎

## Corollary — normalized volume

`det(G)/(d_1 d_2 d_3)` is the squared normalized three-volume.  It is
nonnegative for every Gram matrix, and is positive exactly when the three
vectors are linearly independent.

## Finite certificate consequence

The producer and reverse-order checker evaluate 5,727 triples in 18 frozen
rows.  The exact census is:

```text
positive volume = 5727, zero volume = 0, negative volume = 0
anti-alignable = 9, sign-frustrated = 5718
edge patterns: +++ = 5715, ++- = 1, +-+ = 8, +-- = 3
minimum-target residual <= 1/2,1/4,1/10: 5313, 4413, 3620
```

These are certified finite data.  The growing compatibility theorem and
source-native arithmetic `L2` remain open.
