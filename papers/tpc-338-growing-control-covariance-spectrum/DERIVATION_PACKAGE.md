# TPC-338 derivation package

Let `y_(C,j)=A P_j beta_C` and, for an ensemble `J`, define

```text
ybar_(C,J) = |J|^(-1) sum_(j in J) y_(C,j),
z_(C,j,J) = y_(C,j)-ybar_(C,J).
```

Finite expansion gives

```text
mean_(j in J) ||y_(C,j)||^2
 = ||ybar_(C,J)||^2 + mean_(j in J) ||z_(C,j,J)||^2.          (1)
```

The class covariance matrix

```text
K_J(C,D) = mean_(j in J) <z_(C,j,J),z_(D,j,J)>
```

is positive semidefinite because

```text
a^T K_J a = mean_(j in J) ||sum_C a_C z_(C,j,J)||^2 >= 0.  (2)
```

The five-control set is nested in the nine-control set, but the centering
vectors differ.  Consequently there is no algebraic reason for an individual
off-diagonal entry of `K_5` to have the same sign as the corresponding entry
of `K_9`; the certificate tests this directly rather than assuming it.

For a nonzero trace, the normalized covariance spectrum is
`lambda(K_J)/trace(K_J)`.  Its finite `L1` distance between the two ensembles
is a descriptive comparison only; it is not a spectral convergence theorem.
