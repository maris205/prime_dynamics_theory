# TPC-263 proof package

## Main theorem

Let `x` be a real V59 clock, let `A_x` and `beta` be the literal operator and
coefficient from TPC-257, and let `w` be the literal hybrid residual from
TPC-254.  Let `z0,z1,z2` be the source-only four-block frame and let `P3` be
the orthogonal projection onto their span.  For every fixed admissible `K` and
every fixed `M>0`,

```text
C_3(x)=<P3 w,P3 A_x beta>
       =O_(M,K)(x^(5/3)/(log x)^(M+3)).
```

Moreover, with `C_perp(x)=<(I-P3)w,(I-P3)A_x beta>`,

```text
<w,A_x beta> = C_3(x)+C_perp(x)
```

exactly.  No estimate for `C_perp` is part of the theorem.

## Lemma 1 — exact projection geometry

For adjacent blocks `A,B` of sizes `p,q`, set

```text
h(A,B)=sqrt(pq/(p+q))(1_A/p-1_B/q).
```

With the four blocks from TPC-257,

```text
z0=h(B1 union B2,B3 union B4),
z1=h(B1,B2),
z2=h(B3,B4)
```

are pairwise orthonormal.

### Proof

The squared norm of `h(A,B)` is
`pq/(p+q) * (p/p^2+q/q^2)=1`.  The block-weighted coefficient product of
`z0` with `z1` is

```text
s1*(1/ell)*(1/s1)+s2*(1/ell)*(-1/s2)=0.
```

The `z0,z2` calculation is identical and `z1,z2` have disjoint support.
Thus the three vectors are orthonormal for every admissible integer or real
clock.  The operator
`P3=sum_i z_i tensor z_i` is consequently self-adjoint and idempotent.
`(square)`

## Lemma 2 — blockwise hybrid moments

For each fixed `M,K`,

```text
|<z_i,w>| <<_(M,K) x^(1/2)/(log x)^M,  i=0,1,2.
```

### Proof

Write `W_j=sum_(u in B_j)w(u)`.  The maximal Type-I source theorem used in
TPC-254 is a nonnegative sum over active intervals.  Freezing its `m=1` row
therefore bounds each of the four consecutive block sums by
`O_(M,K)(x/(log x)^M)`.  Each `z_i` is a normalized difference of two such
means.  Since each block size is comparable with `x` and each normalization
factor is comparable with `sqrt(x)`, substitution gives the displayed bound.
No whole-shell average is substituted for an individual block sum. `(square)`

## Lemma 3 — inherited adjoint coefficients

TPC-257's source-backed curvature and bounded-variation compiler gives

```text
<z_i,A_x beta>=-(9/2 kappa_i+o(1))x^(7/6)/(log x)^3,
```

for `i=0,1,2`, with

```text
kappa0=log(32/27)/sqrt(2),
kappa1=log(3456/3125)/2,
kappa2=log(884736/823543)/2.
```

The constants are positive because each displayed rational ratio exceeds one.
This is an explicitly frozen source input, not a numerical inference.

## Proof of the main theorem

Orthogonal projection gives the exact identity

```text
<w,A_x beta>
 =<P3 w,P3 A_x beta>
  +<(I-P3)w,(I-P3)A_x beta>.
```

Expanding in the orthonormal frame gives, with the conjugate-linear-first
inner-product convention,

```text
C_3(x)=sum_(i=0)^2 conjugate(<z_i,w>) <z_i,A_x beta>.
```

Apply Lemmas 2 and 3 and sum the three fixed terms.  The leading product has
size

```text
x^(1/2)/(log x)^M * x^(7/6)/(log x)^3
=x^(5/3)/(log x)^(M+3).
```

The `o(1)` factors are harmless after fixing `M,K` and taking `x` large.
This proves the rank-three channel estimate.  The first displayed projection
identity proves the residual statement. `(square)`

## Logarithmic and endpoint firewall

For every fixed `eta>0`,

```text
[x^(5/3)/(log x)^(M+3)] / x^(5/3-eta)
=x^eta/(log x)^(M+3) -> infinity.
```

Hence this paper contributes no fixed-power credit.  In particular it does
not pay TPC-261's strict `1/400` endpoint obligation.  The orthogonal residual
could in principle be smaller or larger; the current theorem is silent about
it and therefore cannot be promoted to a full coupling estimate. `(square)`

## Scope firewall

```text
PROVED = exact P3/Pperp decomposition and rank-three cross-Gram formula
PROVED_SOURCE_BACKED = blockwise w control, inherited adjoint coefficients,
                       rank-three logarithmic channel bound
OPEN = C_perp; fixed-power saving; arithmetic L2; full Gate B; twin primes
NUMERICALLY_CERTIFIED = finite frame/projection/exponent replay
REFUTED_SCOPED = dropping the orthogonal residual after controlling P3
```
