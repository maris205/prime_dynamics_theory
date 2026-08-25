# Proof Package

## Theorem: declared-block margin compiler

Let `H=C^I` with `I` finite and nonempty.  Let `I=disjoint_union_d J_d` be an
exhaustive declared partition into nonempty blocks.  With the literal TPC-247
definitions and `lambda_cb=1`, define `u_c,a_c,b_c,w_c_perp,m_cb,v_cb_perp`,
and `g_c_perp` as in the derivation package.  Define `D_c,L_c,mu_c,U_c` using
the projected probes and TPC-250's empty-pair convention.  Then

```text
C_x=C_long+Q_trans,
|C_x-C_long|<=R_trans<=R_coh.
```

Here

```text
C_long=sum_c conjugate(a_c)b_c,
Q_trans=sum_c <w_c_perp,g_c_perp>,
R_trans=sum_c ||w_c_perp||||g_c_perp||,
R_coh=sum_c ||w_c_perp||U_c.
```

The projected Gram entries are exactly

```text
Gperp_c(bb')=G_c(bb')-conjugate(m_cb)m_cb'.
```

### Proof

Exhaustiveness gives `sum_b P_b=I` and `sum_c P_c=I`; orthogonality of the
coordinate blocks gives

```text
g_c=sum_b P_c A_x P_b beta=P_c A_x beta,
C_x=sum_c <w_c,g_c>.
```

The definitions make `w_c_perp` and every `v_cb_perp` orthogonal to `u_c`.
Since `g_c=b_c u_c+g_c_perp` and `w_c=a_c u_c+w_c_perp`, conjugate linearity
in the first slot yields

```text
<w_c,g_c>=conjugate(a_c)b_c+<w_c_perp,g_c_perp>.
```

Summing proves the decomposition.  Expanding
`<v_cb-m_cb u_c,v_cb'-m_cb' u_c>` and using
`<u_c,v_cb>=m_cb`, `<v_cb,u_c>=conjugate(m_cb)`, and `<u_c,u_c>=1`
proves the projected Gram formula.

TPC-250 applied to the projected family with all weights one gives

```text
||g_c_perp||^2<=D_c+mu_c(L_c^2-D_c)=U_c^2.
```

The right side is nonnegative, so `||g_c_perp||<=U_c`.  Finally,
Cauchy--Schwarz and the triangle inequality give

```text
|Q_trans|<=sum_c ||w_c_perp||||g_c_perp||=R_trans<=R_coh.
```

This proves every assertion.  QED.

## Corollary: independently certified external scalar

If `E>=0` and `|F-C_x|<=E`, then

```text
|F-C_long|<=R_coh+E,
|F|>=(|C_long|-R_coh-E)_+.
```

In particular, `|C_long|>R_coh+E` implies `F!=0`.

### Proof

Apply the triangle inequality to
`F-C_long=(F-C_x)+(C_x-C_long)`.  The reverse triangle inequality gives
`|F|>=|C_long|-|F-C_long|`; intersect with nonnegativity.  Under the strict
hypothesis the lower endpoint is positive.  QED.

## Proposition: equality obstruction

In `R^4`, let

```text
u=(1,1,1,1)/2, t=(1,-1,1,-1)/2,
w=u+t, g=u-t.
```

Then `u,t` are orthonormal,

```text
C_long=1, Q_trans=-1, R_trans=1, C=0.
```

Therefore `|C_long|=R_trans` cannot imply nonvanishing.

### Proof

The longitudinal coefficients are both one, while the transverse vectors are
`t` and `-t`.  Their inner product is `-1`, their norm product is one, and the
two contributions cancel.  QED.

## Edge cases and audit conclusion

For a singleton declared block, `u_c` spans the block and every projected
probe vanishes, so `D_c=L_c=U_c=0`.  If exactly one projected probe is active,
the empty-pair convention sets `mu_c=0`, and `U_c` equals that probe's norm.
Thus every displayed quantity is total.

The theorem is pointwise for the fixed source data.  It does not assert an
exact disk image.  The partition and flat direction are declared modeling
choices, the external error is conditional, and the finite replay supplies no
V59 asymptotic or arithmetic advance.
