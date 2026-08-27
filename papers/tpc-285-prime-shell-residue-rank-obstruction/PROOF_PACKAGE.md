# TPC-285 proof package

## Theorem 1: centered residue factorization

For an odd prime `q`, define `R_q` and `P_q` as in the derivation package.
Entrywise,

```text
(R_qR_q^T)(u,t)=m_q(u)m_q(t)1_{u=t mod q},
(R_q11^TR_q^T)(u,t)=m_q(u)m_q(t).
```

Therefore `B_q=R_qP_qR_q^T`.  Since `P_q` has rank `q-2`,
`rank(B_q)<=q-2`.  If all nonzero residue classes occur, `R_q` has full column
rank and `B_q=(R_qP_q)(R_qP_q)^T` has rank exactly `q-2`.

## Theorem 2: deleted-diagonal full rank

Assume every nonzero residue class occurs and write `m=q-1`.  On active
indices,

```text
mD_q=mR_qR_q^T-u_qu_q^T-(m-1)I.
```

Split the active space into the direct sum of the within-class zero-sum
subspaces and the block-constant subspace.  The first summand has eigenvalue
`-(m-1)`, hence is invertible.  If the class sizes are `n_a`, the second
summand has matrix `diag(d_a)-1n^T`, where `d_a=mn_a-(m-1)>0`.  Its determinant
is

```text
product_a d_a * (1-sum_a n_a/d_a).
```

Since `d_a<mn_a`, every ratio is greater than `1/m`, and the sum over `m`
classes is greater than one.  The determinant is nonzero.  Thus the whole
active block is invertible and `rank(D_q)` equals the active index count.

## Finite kernel-Schur proposition

On the 20 registered `(X,H,Q,s,q)` rows, the active rational matrix
`K_H o D_q` reduces to a full-rank matrix modulo `1000000007`; no denominator
vanishes modulo that prime.  A nonzero determinant after valid reduction is a
nonzero rational determinant.  Hence every registered kernel-Schur block has
full active rational rank.

## Obstruction and scope

The low-rank object `B_q` includes its diagonal.  The physical operator uses
`D_q`, and the exact theorem shows that this diagonal deletion can increase
rank from `q-2` to the entire active dimension.  Schur kernel weighting remains
full rank on the finite rows.  This blocks a direct low-rank shortcut, but does
not refute cancellation estimates based on signs, singular values, or
cross-prime interactions.  Literal arithmetic `L2` and full Gate B remain open.
