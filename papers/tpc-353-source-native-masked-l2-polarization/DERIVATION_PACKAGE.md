# TPC-353 derivation package

## 1. Literal operator

For a finite interval `I`, shell `S_Q`, exponent `s`, and a declared sign law
`e`, let

```text
A_e(u,t) = sum_(p in S_Q) e_p 1_(u!=t) 1_(p not divide u t)
            p H^(2s)/(H^2+(u-t)^2)^s
            (1_(u=t mod p)-1/(p-1)).
```

All sums are finite.  The two endpoint indicators are part of the operator;
they are not discarded in this release.

## 2. Source-native vector

The declared finite source is

```text
beta(t)=Lambda(t+2)-b^(2)(t),
b^(2)(t)=2 C_2 1_(2 not divide t)
          product_(p|t,p>2)(p-1)/(p-2).
```

The finite Euler tail and logarithm midpoint protocol are inherited from the
locked V59 source.  This is a declared finite model, not an asymptotic
identity about twin primes.

## 3. Operator polarization

Put `y_L=A_e Lambda`, `y_b=A_e b`, and `y_beta=A_e beta=y_L-y_b`.  Bilinearity
of the finite Euclidean inner product gives

```text
||y_beta||_2^2 = ||y_L||_2^2 + ||y_b||_2^2 - 2 <y_L,y_b>.
```

When `E_L+E_b>0`, define

```text
kappa_A = 2 <y_L,y_b>/(E_L+E_b),
R_A     = ||y_beta||_2^2/(E_L+E_b).
```

Then `R_A=1-kappa_A` exactly in the finite real model.

## 4. Cauchy envelope

The finite Cauchy--Schwarz inequality gives

```text
-sqrt(E_L E_b) <= <y_L,y_b> <= sqrt(E_L E_b),
```

and therefore

```text
(sqrt(E_L)-sqrt(E_b))^2/(E_L+E_b) <= R_A
  <= (sqrt(E_L)+sqrt(E_b))^2/(E_L+E_b).
```

This is an exact finite interface.  It controls a given finite vector after
the operator is specified; it does not supply a source-uniform bound for
`A_e` or for the V59 family.

## 5. Audit interpretation

The certificate reports `kappa_A`, `R_A`, the output cosine, the source-level
polarization coefficient, and their difference.  A positive output
coefficient means alignment of the two *operator images* and hence destructive
subtraction in the residual output.  It does not select a canonical law and
does not pay a power of `X`.
