# Proof package

## Theorem T249.1

For finite output groups, complex weights, and independent balls
`||W_c||<=rho_c`,

```text
{sum_(c,b)lambda_cb<W_c,v_cb>} = R Dbar,
R=sum_c rho_c sqrt(lambda_c*G_c lambda_c).
```

Proof.  Put `g_c=sum_b lambda_cbv_cb`.  The scalar is
`sum_c<W_c,g_c>`.  Cauchy gives each local disk radius
`r_c=rho_c||g_c||`.  Conversely, for `g_c!=0`,
`W_c=conjugate(d_c)g_c/||g_c||^2` realizes any `|d_c|<=r_c`.  The Minkowski
sum of centered disks is the radius-`R` disk, with explicit allocation
`d_c=(r_c/R)d` when `R>0`.  If `R=0`, every active functional is zero.

## Corollary T249.2

For explicitly declared affine balls `W_c=W_c^0+U_c`, the exact image is
`C+R Dbar`, `C=sum_c<W_c^0,g_c>`.  Hence zero is feasible iff `|C|<=R` and
the exact minimum modulus is `max(|C|-R,0)`.  The affine domain is a modeling
choice, not a source theorem.

## Theorem T249.3

For the global budget `sum_c||U_c||^2<=rho^2`, the exact centered image is the
disk of radius

```text
rho sqrt(sum_c lambda_c*G_c lambda_c).
```

Proof.  Apply the one-functional ball theorem to the direct-sum vector
`g_ext=direct_sum_c g_c`; the same explicit preimage proves sharpness.

## Theorem T249.4

The exact independent radius is at most

```text
R_tag=sum_c rho_c sum_b|lambda_cb|||v_cb||.
```

For every group with `rho_c>0`, equality holds iff all nonzero
`lambda_cbv_cb` are nonnegative multiples of one common vector.  This is the
complex Hilbert-space equality condition in the triangle inequality.  Groups
with `rho_c=0` are irrelevant.

Repeated probes with opposite weights give `g_c=0` while `R_tag>0`; orthogonal
equal-weight probes give the strict ratio `sqrt(2)/2`; aligned probes attain
equality.  None of these structural identities estimates the literal
large-scale V59 Gram entries.
