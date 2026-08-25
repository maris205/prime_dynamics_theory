# Derivation Package

## 1. Frozen literal source

Let `H=C^I`, where `I` is finite and nonempty.  Declare an exhaustive disjoint
partition `I=disjoint_union_d J_d` into nonempty blocks and let `P_d` be the
coordinate projections.  The same complete partition indexes input blocks
`b` and output blocks `c`.  Import from TPC-247 only

```text
beta_b=P_b beta,
A_cb=P_c A_x P_b,
v_cb=A_cb beta_b,
w_c=P_c w.
```

The literal scalar has `lambda_cb=1`.  Consequently

```text
g_c=sum_b v_cb=P_c A_x beta,
C_x=<w,A_x beta>=sum_c <w_c,g_c>.
```

The hard partition is a modeling choice.  It is not identified with a smooth
V59 partition.

## 2. Declared-block projection

Set

```text
u_c=|J_c|^(-1/2) 1_(J_c),
a_c=<u_c,w_c>,
b_c=<u_c,g_c>,
w_c_perp=w_c-a_c u_c.
```

For each probe set

```text
m_cb=<u_c,v_cb>,
v_cb_perp=v_cb-m_cb u_c,
g_c_perp=sum_b v_cb_perp.
```

Because the inner product is conjugate-linear in its first slot,

```text
<w_c,g_c>=conjugate(a_c)b_c+<w_c_perp,g_c_perp>.
```

Thus

```text
C_long=sum_c conjugate(a_c)b_c,
Q_trans=sum_c <w_c_perp,g_c_perp>,
C_x=C_long+Q_trans.
```

The unit `u_c` is canonical only after the declared block has been chosen.  It
is not V59-canonical and is not the TPC-219 longitudinal object.

## 3. Projected Gram and coherence

Let `G_c(bb')=<v_cb,v_cb'>`.  Expanding the orthogonal projection gives

```text
Gperp_c(bb')
 = <v_cb-m_cb u_c, v_cb'-m_cb' u_c>
 = G_c(bb')-conjugate(m_cb)m_cb'.
```

Set `d_cb=||v_cb_perp||`,

```text
D_c=sum_b d_cb^2,
L_c=sum_b d_cb.
```

Use TPC-250's total convention: `mu_c=0` when fewer than two projected probes
are active; otherwise take the largest normalized absolute off-diagonal entry
of `Gperp_c`.  Then

```text
U_c=sqrt(D_c+mu_c(L_c^2-D_c))>=0,
||g_c_perp||<=U_c.
```

Define both radii explicitly:

```text
R_trans=sum_c ||w_c_perp|| ||g_c_perp||,
R_coh=sum_c ||w_c_perp|| U_c.
```

Cauchy--Schwarz and the coherence upper bound yield

```text
|C_x-C_long|=|Q_trans|<=R_trans<=R_coh.
```

## 4. Conditional external scalar

For any independently certified scalar `F` and `E>=0` satisfying
`|F-C_x|<=E`, the triangle inequality gives

```text
|F-C_long|<=R_coh+E.
```

Reverse triangle then gives

```text
|F|>=(|C_long|-R_coh-E)_+.
```

The strict condition `|C_long|>R_coh+E` implies `F!=0`.  Equality is not
enough.  No exact disk image is claimed for fixed source data.

## 5. Recommended replay arithmetic

For each four-coordinate block use

```text
u=(1,1,1,1)/2,
t1=(1,-1,1,-1)/2,
t2=(1,1,-1,-1)/2.
```

The four probes and lanes specified in the task give

```text
C_long=11/2, Q_trans=-1, C_x=9/2,
R_trans=R_coh=1.
```

Block `c=0` has `(D,L,mu,U)=(1,7/5,0,1)`.  Block `c=1` has
`(2,2,1,2)`, but `w_1_perp=0`.  For `(F,E)=(4,1/2)`, the external upper
bound is attained and the strict lower margin is `4`.  This replay is labeled
`SYNTHETIC_EXACT_FINITE_OPERATOR_REPLAY_NOT_A_LITERAL_V59_ARITHMETIC_INSTANCE`.
