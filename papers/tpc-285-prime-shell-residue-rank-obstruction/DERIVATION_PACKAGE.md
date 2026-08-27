# TPC-285 derivation package

Let `q` be an odd prime, `I` a finite index set, and

```text
m_q(u) = 1_{q does not divide u},
R_q(u,a) = m_q(u) 1_{u=a mod q},  a=1,...,q-1,
u_q = R_q 1.
```

The centered residue block before diagonal deletion is

```text
B_q(u,t)=m_q(u)m_q(t)(1_{u=t mod q}-1/(q-1)),
B_q=R_q P_q R_q^T,
P_q=I_{q-1}-11^T/(q-1).
```

`P_q` is the orthogonal projection onto the zero-sum residue coefficient
space, so `rank(B_q)<=q-2`.  If every nonzero residue class occurs in `I`, the
columns of `R_q` are independent and the rank is exactly `q-2`.

For the physical deleted-diagonal block `D_q=B_q-diag(B_q)`, put `m=q-1` and
restrict to the active indices.  The scaled matrix is

```text
M_q=m D_q=m R_qR_q^T-u_qu_q^T-(m-1)I.
```

If class `a` has size `n_a`, then on the within-class zero-sum subspace
`M_q` acts as `-(m-1)I`.  On block-constant vectors its coefficient matrix is

```text
diag(d_a)-1 n^T,  d_a=m n_a-(m-1).
```

The matrix determinant lemma gives

```text
det = product_a d_a * (1-sum_a n_a/d_a).
```

Every `n_a/d_a>1/m`; summing over the `m` nonzero classes gives a strict value
greater than one.  Hence the determinant factor is negative and nonzero.  Both
invariant pieces are invertible, so `D_q` has full active rank.

The kernel-weighted physical block is `q(K_H o D_q)`.  No general rank theorem
for this Schur product is asserted.  The registered rows are instead reduced
exactly modulo `1000000007`; all denominators are invertible and every active
matrix has full modular rank, which certifies full rational rank on those rows.
