# TPC-316 derivation package

## 1. Literal operator

For an even scale `X`, put

```text
I_X={X/2+1,...,X},       N_X=|I_X|=X/2,
S_Q={p prime: Q<p<=2Q}.
```

With `H=66` and `s in {1,2}`, define

```text
K_(p,u,t) = 1_(t!=u, p does not divide ut)
             p H^(2s)/(H^2+(u-t)^2)^s
             (1_(u==t mod p)-1/(p-1)).
```

The literal source operator is

```text
(A_(Q,s,X) beta)_(p,u) = sum_(t in I_X) K_(p,u,t) beta_t.
```

It maps `ell^2(I_X)` to `ell^2(S_Q x I_X)`.  This is the same centered,
deleted-diagonal physical kernel used in the TPC-268/TPC-315 line; no source
coefficient is inserted into the operator definition.

## 2. Exact finite Frobenius interface

Every entry is rational.  For any real or complex source vector `beta`, rowwise
Cauchy--Schwarz gives

```text
||A beta||_2^2
 <= (sum_(p,u,t) |K_(p,u,t)|^2) ||beta||_2^2
 = ||A||_HS^2 ||beta||_2^2.
```

Therefore

```text
N_X^(-1)||A beta||_2^2
 <= (||A||_HS^2/N_X)||beta||_2^2.
```

This is a finite literal statement.  It is not the desired growing estimate
`||A_X||_(2->2)<=K X^(-sigma)`.

For a coordinate vector `e_t`,

```text
||A e_t||_2^2 = sum_(p,u) |K_(p,u,t)|^2 <= ||A||_(2->2)^2.
```

Thus every explicitly evaluated column is a rigorous lower witness for the
unknown operator norm.

## 3. Difference/residue compression

Fix `p` and a signed nonzero difference `delta=u-t`.  The allowed `t` values
form

```text
J_delta = [max(L,L-delta), min(U,U-delta)] intersect Z,
```

where `[L,U]=I_X`; its cardinality is `m_delta=N_X-|delta|`.

If `p | delta`, the endpoints have the same residue.  Removing the forbidden
zero residue leaves

```text
v_(delta,p)=m_delta-#(t in J_delta: t==0 mod p),
c_(delta,p)^2=(p-2)^2/(p-1)^2.
```

If `p` does not divide `delta`, the two forbidden residues are distinct and

```text
v_(delta,p)=m_delta-#(t in J_delta: t==0 mod p)
                  -#(t in J_delta: t==-delta mod p),
c_(delta,p)^2=1/(p-1)^2.
```

Consequently the exact Hilbert--Schmidt mass is

```text
||A_(Q,s,X)||_HS^2
 = sum_(p in S_Q) sum_(0<|delta|<N_X)
     p^2 [H^(2s)/(H^2+delta^2)^s]^2
     c_(delta,p)^2 v_(delta,p).
```

The residue count is computed by the first integer in `J_delta` with the
requested residue and then an arithmetic progression count.  All terms are
`Fraction` values, so this formula is exact.

## 4. Finite comparison protocol

The declared panels are `X=640`, with `I={321,...,640}`, and `X=1280`, with
`I={641,...,1280}`.  For each `Q in {24,36,54,80}` and `s in {1,2}`, the
certificate records `||A||_HS^2/N`, five coordinate-column energies divided
by `N`, the strongest five-point lower witness, and the exact ratio of the two
normalized Hilbert--Schmidt masses across scales.

The five columns are the endpoint-inclusive positions at offsets
`0, floor((N-1)/4), floor((N-1)/2), floor(3(N-1)/4), N-1`.  The best column is
selected by exact rational comparison.  The scale comparison is labelled a
finite observation; no logarithm or asymptotic exponent is fitted.

## 5. Route interpretation

The calculation pays a finite source-level `L2` envelope, which was absent in
TPC-315.  It does not pay a useful growing power: the normalized Frobenius
upper envelope rises in all eight matched rows, and its fresh-panel gap over
the available coordinate lower witnesses is very large.  The missing object
is a sharper arithmetic cancellation or spectral estimate for the true
operator norm.
