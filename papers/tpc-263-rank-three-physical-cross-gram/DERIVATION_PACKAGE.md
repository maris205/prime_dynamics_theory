# TPC-263 derivation package

## 1. Source-only rank-three frame

Let

```text
I_x=(x/2,x] intersect Z,  N=|I_x|,
ell=floor(N/2), r=N-ell,
```

and split the two rank children into four consecutive blocks
`B1,B2,B3,B4` of sizes `s1,s2,s3,s4`.  For adjacent blocks of sizes `p,q`,
write

```text
h(A,B)=sqrt(pq/(p+q)) (1_A/p-1_B/q).
```

The three source-only contrasts are

```text
z0=h(B1 union B2,B3 union B4),
z1=h(B1,B2),
z2=h(B3,B4).
```

TPC-257 proves that these are exactly orthonormal, independently of the
coefficient and of the signs being tested.  Put

```text
P3=sum_(i=0)^2 z_i tensor z_i.
```

`P3` is therefore an orthogonal projection.

## 2. Four block sums pay all three `w` moments

Let `W_j=sum_(u in B_j) w(u)`.  TPC-254's nonnegative maximal Type-I row at
`m=1` bounds every active consecutive block sum by
`O_(M,K)(x/(log x)^M)` for every fixed `M`.  Substitution into the three
contrast formulas gives

```text
|<z_i,w>| <<_(M,K) x^(1/2)/(log x)^M,  i=0,1,2.
```

The important point is that `z1,z2` are not inferred from a whole-shell mean:
their four block sums are individually controlled before the signed
combination is formed.

## 3. The exact channel split

Set `g_x=A_x beta` and

```text
C_x=<w,g_x>,
C_3(x)=<P3 w,P3 g_x>,
C_perp(x)=<(I-P3)w,(I-P3)g_x>.
```

Orthogonality gives the exact identity

```text
C_x=C_3(x)+C_perp(x),
C_3(x)=sum_(i=0)^2 conjugate(<z_i,w>) <z_i,g_x>.
```

There are no mixed terms.  This is a decomposition of the actual common
V59 object, not a replacement by an abstract diagonal model.

## 4. Rank-three channel estimate

TPC-257 supplies

```text
<z_i,g_x>=-(9/2 kappa_i+o(1)) x^(7/6)/(log x)^3,
```

where

```text
kappa0=log(32/27)/sqrt(2),
kappa1=log(3456/3125)/2,
kappa2=log(884736/823543)/2.
```

For every fixed `M`, finite summation and the preceding `w` estimates imply

```text
|C_3(x)| <<_(M,K) x^(1/2)/(log x)^M
                  * x^(7/6)/(log x)^3
              = O_(M,K)(x^(5/3)/(log x)^(M+3)).
```

This is a source-backed rank-three physical cross-Gram channel.  It is
logarithmic only: for every fixed `eta>0`,
`x^(5/3)/(log x)^(M+3)` is not `O(x^(5/3-eta))`.

## 5. What remains

The residual `C_perp(x)` is not bounded by the rank-three theorem.  TPC-260
already shows why packet marginals and a finite collection of null/Haar
coordinates cannot identify a four-packet residual.  TPC-263 removes exactly
one new physical channel and leaves the orthogonal complement explicit for the
next adversarial study.
