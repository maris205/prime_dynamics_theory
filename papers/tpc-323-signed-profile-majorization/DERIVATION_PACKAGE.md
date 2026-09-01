# TPC-323 derivation package

## 1. Direct and coherent operators

Let `B_1,...,B_m` be the finite prime-labelled blocks on a source space of
dimension `N`.  Define the direct-sum operator and a signed coherent operator
by

```text
A_direct v = (B_p v)_p,
C_e       = sum_p e_p B_p,       e_p in {+1,-1}.
```

Their Gram matrices are

```text
G_direct = sum_p B_p^T B_p,
G_e      = C_e^T C_e.
```

The block Frobenius Gram `H_{pq}=<B_p,B_q>_F` gives
`tr(G_e)=e^T H e` and `tr(G_direct)=tr(H)`.

## 2. Shape coordinate

For every positive-semidefinite finite Gram matrix `G` with positive trace,
write

```text
T(G)  = tr(G),
pi(G) = (lambda_1(G)/T(G), ..., lambda_N(G)/T(G)),
```

with eigenvalues in decreasing order.  Define the signed energy ratio

```text
rho_e = T(G_e)/T(G_direct).
```

Then `rho_e` is an amplitude coordinate and `pi(G_e)` is a shape coordinate.
The identity

```text
G_e = T(G_e) V_e diag(pi(G_e)) V_e^T
```

is just the spectral theorem, but it is the bookkeeping separation needed by
the route: changing `T(G_e)` cannot change `pi(G_e)`.

## 3. Exact profile invariance

For `c>0`, the eigenvalues of `cG` and its trace are respectively
`c lambda_j(G)` and `c T(G)`.  Therefore `pi(cG)=pi(G)`.  In particular,
the profile distances and all cumulative Ky Fan comparisons are invariant
under positive rescaling.

## 4. Majorization diagnostic

For probability profiles `p,q`, set

```text
d_r(p,q) = sum_{j<=r} (p_j-q_j),   1<=r<N.
```

The finite label `SIGNED_MAJORISES_DIRECT` means every `d_r(pi(G_e),
pi(G_direct))` is nonnegative up to the declared tolerance and at least one
is positive beyond it.  `MIXED` means both signs occur beyond tolerance.
This is a finite profile diagnostic, not a theorem about an infinite spectral
measure.

## 5. Literal block

For `I_X=(X/2,X]` and `S_Q={p: Q<p<=2Q, p prime}`, the audited block is

```text
B_p(u,t) = 1_{u!=t} 1_{p not|u} 1_{p not|t}
           p H^(2s)/(H^2+(u-t)^2)^s
           (1_{u=t mod p} - 1/(p-1)).
```

No arithmetic theorem is inserted into the derivation.  The four sign laws
are geometric finite probes only.
