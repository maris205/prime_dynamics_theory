# TPC-355 derivation package

## 1. Literal component and geometry diagonal

For a finite interval `I`, shell `S_Q`, exponent `s`, and `u,t in I`, define

```text
B_p(u,t) = 1_(u!=t) 1_(p not divide u) 1_(p not divide t)
            p H^(2s)/(H^2+(u-t)^2)^s
            (1_(u=t mod p)-1/(p-1)).
```

The signed operator for a predeclared law `e` is `A_e=sum_p e_p B_p`.  The
position-aware geometry energy is

```text
G_u = sum_(p in S_Q) sum_(t in I) B_p(u,t)^2.
```

It is deliberately built from unsigned component squares, so it is
independent of the sign law and cannot use cancellation in `A_e`.

## 2. Finite diagonal congruence

On a declared finite row, `G_u>0` is checked.  Therefore

```text
D_G = diag(G_u),       A# = D_G^(-1/2) A_e D_G^(-1/2)
```

is a well-defined finite real matrix.  This is a diagonal congruence, not an
assertion that it is a bounded operator uniformly in the source or in `X`.

## 3. Polarization after normalization

For `T=A_e` or `T=A#` and `beta=Lambda-b`, put

```text
E_L=||T Lambda||_2^2,   E_b=||T b||_2^2,
kappa_T=2<T Lambda,T b>/(E_L+E_b).
```

Finite bilinearity gives

```text
||T beta||_2^2 = E_L + E_b - 2<T Lambda,T b>,
R_T=||T beta||_2^2/(E_L+E_b)=1-kappa_T.
```

When the denominator is positive, Cauchy--Schwarz gives

```text
(sqrt(E_L)-sqrt(E_b))^2/(E_L+E_b) <= R_T
  <= (sqrt(E_L)+sqrt(E_b))^2/(E_L+E_b).
```

These are exact finite identities and inequalities.  They do not turn a
finite diagonal scaling into a source-uniform arithmetic estimate.

## 4. Transfer statistic

For the all-plus law let `m_raw(P)` and `m_norm(P)` be the minimum `kappa`
over the 54 rows of panel `P`.  The declared finite floor-drop reduction is

```text
rho = 1 - (m_norm(low)-m_norm(higher)) /
          (m_raw(low)-m_raw(higher)).
```

On this fixed panel `rho=0.37754982894688971`.  It is a descriptive statistic
of three finite panels, not an asymptotic constant or a theorem.
