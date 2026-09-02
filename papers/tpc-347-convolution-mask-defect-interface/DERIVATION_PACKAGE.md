# TPC-347 derivation package

## 1. Literal kernel

Let `S_Q={p prime: Q<p<=2Q}` and let `e_p` be one of the declared finite
sign laws.  For `d in Z`, put

```text
k_p(d) = 0                                      if d=0,
         p H^(2s)/(H^2+d^2)^s (1_(p|d)-1/(p-1)) otherwise.
```

The series is absolutely summable for `s>=1`, since
`|k_p(d)| <= p H^(2s)/|d|^(2s)` away from zero.  Define
`(K_p f)(u)=sum_d k_p(d)f(u-d)` and `K_e=sum_p e_p K_p`.

For a finite interval `I`, `R_I` restricts a sequence to `I`, `E_I` extends
by zero, and `P_p` is multiplication by `1_(p does not divide n)`.  Direct
substitution gives

```text
A_I = sum_p e_p R_I P_p K_p P_p E_I.
```

This is the same physical deleted-diagonal matrix used by the current TPC
line; only the order of its factors has been exposed.

## 2. Exact defect algebra

Set `T_I=R_I K_e E_I` and `D_I=A_I-T_I`.  Since

```text
P K P - K = (P-I) K P + K(P-I),
```

we have the exact expansion

```text
D_I = sum_p e_p R_I ((P_p-I)K_pP_p + K_p(P_p-I)) E_I.
```

No endpoint or divisibility term is lost.  If the two interval endpoints are
translated by the same integer, the entries of `T_I` depend only on `u-t`,
so the ideal matrices are identical after the canonical index translation.

## 3. Fourier `ell^2` interface

For `k_e=sum_p e_p k_p`, absolute summability makes

```text
khat_e(theta) = sum_(d in Z) k_e(d) exp(-i d theta)
```

a continuous `2 pi`-periodic function.  The discrete Fourier transform on
`ell^2(Z)` sends convolution by `k_e` to multiplication by `khat_e`.
Consequently

```text
||K_e||_(2->2) = ess sup_(theta in [-pi,pi]) |khat_e(theta)|.
```

The interval compression is a contraction:
`||T_I|| <= ||K_e||`, because `R_I` and `E_I` have norm one.  Young's
inequality gives the unconditional baseline
`||K_e|| <= sum_d |k_e(d)|`.

## 4. Tail envelope

For `R>=1`, `|1_(p|d)-1/(p-1)|<=1`, and hence

```text
sum_(|d|>R) |k_e(d)|
 <= 2 H^(2s) sum_(p in S_Q) p
    sum_(d>R) d^(-2s)
 <= 2 H^(2s) sum_p p / ((2s-1)R^(2s-1)).
```

The producer evaluates the finite sum for `1<=d<=65536`, adds this analytic
tail majorant, and rounds the displayed floating envelope upward.  This is a
reproducible numerical view of a proved majorant; it is not a claimed sharp
symbol norm.

## 5. Finite norm comparison

The ordinary triangle inequality and `||D_I||_(2->2)<=||D_I||_F` imply

```text
||A_I|| <= ||T_I||+||D_I||
          <= ||K_e||+||D_I||_F.
```

The certificate checks this combined finite envelope on every declared row.
The defect-to-ideal ratios are reported as diagnostics only.  In particular,
their finite range cannot be read as a uniform lower bound in the growing
variable.
