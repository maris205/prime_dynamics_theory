# TPC-257 derivation package

## 1. Target and status

The object is unchanged from TPC-256: the literal V59 coefficient `beta` and
the literal prime-shell operator `A_x`.  The only new ingredient is a frame
chosen from the ordered physical clock before any coefficient or sign is
inspected.  The target is a lower bound for the output of `A_x beta` in a
transverse subspace.

The derivation is coherent as stated.  The source-backed analytic input is the
same de la Vallée Poussin PNT, weighted prime-shell asymptotic, and exact
TPC-255 adjoint normal form already locked by TPC-256.  The new finite
dimensional geometry and the three curvature constants are proved here.

## 2. Frozen clock and four blocks

For a real clock `x`, write

```text
a=floor(x/2), b=floor(x), N=b-a,
ell=floor(N/2), r=N-ell, m=a+ell.
```

Let `L={a+1,...,m}` and `R={m+1,...,b}`.  Split each rank child in its
ordered coordinate order:

```text
s1=floor(ell/2), s2=ell-s1,
s3=floor(r/2),   s4=r-s3.
```

The consecutive blocks `B_1,...,B_4` have these lengths.  For all sufficiently
large `x` they are nonempty, and their scaled endpoint limits are

```text
B1=[1/2,5/8], B2=[5/8,3/4],
B3=[3/4,7/8], B4=[7/8,1].
```

If `A,B` are disjoint consecutive intervals with lengths `p,q`, define

```text
h(A,B)=sqrt(pq/(p+q)) (1_A/p-1_B/q).
```

The three source-only vectors are

```text
z0=h(B1 union B2,B3 union B4),
z1=h(B1,B2),
z2=h(B3,B4).
```

Thus `z0` is exactly the TPC-256 midpoint vector.  The construction depends
only on `x` and rank, not on `beta`, `A_x beta`, a sign, or an observed
quantity.

## 3. Exact frame geometry

For a pair with lengths `p,q`, put `rho^2=pq/(p+q)`.  Then

```text
rho^2(1/p+1/q)=1,
rho(1/p+1/q)=1/rho.
```

The first identity gives unit norm.  The vector `z1` has zero sum on
`B1 union B2`, while `z0` is constant on that macro-block; the analogous
statement holds for `z2` and the right macro-block.  The supports of `z1`
and `z2` are disjoint.  Therefore

```text
<zi,zj>=delta_ij,  0<=i,j<=2.
```

Extend each vector by zero outside `I_x`.  Its total variation is exactly

```text
V(zi)=2/rho_i,
```

where `rho_i` is the normalization of its defining pair.  Indeed, the two
outer jumps contribute `rho_i/p_i` and `rho_i/q_i`, and the internal jump is
`rho_i(1/p_i+1/q_i)=1/rho_i`.  The four-block construction has
`rho_i` comparable with `sqrt(x)`, so `V(zi)=O(x^(-1/2))`.

This is the smallest frame that contains a nonzero subspace orthogonal to the
old midpoint: `span(z1,z2)` is contained in `z0`-perp.

## 4. Curvature of the three beta contrasts

Put `P(t)=Lambda(t)/log(t)` and
`D_U(t)=sum_(d|t,d<=U) mu(d)`.  Consecutive interval counting gives, for
every interval `J` of length `s`,

```text
#(J intersect dZ)=s/d+theta_(J,d), |theta_(J,d)|<=1.
```

For each of the three contrasts the two child intervals have the same
leading density `1/d`; this cancels separately for every divisor before a
triangle inequality.  Hence

```text
|<zi,D_U>| <= U/rho_i = O(x^(-67/400)).
```

The strong PNT gives

```text
F(y)=sum_(2<=n<=y) Lambda(n)/log(n)
    =Li(y)+O(y exp(-c sqrt(log y))).
```

For two equal-width limiting intervals `A=[a_0,a_1]` and
`B=[b_0,b_1]`, with width `d`, expansion of `1/log(xy)` gives

```text
mean_A(P)-mean_B(P)
 = (1/d)(integral_B log(y)dy-integral_A log(y)dy)/log^2(x)
   +O(log^(-3)(x)).
```

The resulting exact logarithmic table is:

| vector | limiting pair `(A,B)` | curvature of means | `rho_i/sqrt(x)` | `kappa_i` |
|---|---|---|---|---|
| `z0` | `[1/2,3/4]`, `[3/4,1]` | `2 log(32/27)` | `1/(2 sqrt(2))` | `log(32/27)/sqrt(2)` |
| `z1` | `[1/2,5/8]`, `[5/8,3/4]` | `2 log(3456/3125)` | `1/4` | `log(3456/3125)/2` |
| `z2` | `[3/4,7/8]`, `[7/8,1]` | `2 log(884736/823543)` | `1/4` | `log(884736/823543)/2` |

All three ratios inside the logarithms exceed one.  Endpoint floors change
the normalized means by `O(1/(x log x))`, so the table yields

```text
<zi,beta> = (kappa_i+O(1/log x)) sqrt(x)/log^2(x),
```

with `kappa_i>0`.  The decimal values used only for orientation are

```text
kappa0 = 0.120136761035088...
kappa1 = 0.050338783876722...
kappa2 = 0.035836765508158...
```

## 5. Bounded-variation adjoint normal form

For `q` in the shell and `q` not dividing `t`, retain the complete combined
unit row

```text
v_(q,t)(u)=1_(q does not divide u)
            (1_(u=t mod q)-1/(q-1)).
```

Its complete period is centered only after the two displayed pieces are
recombined.  The TPC-255 Poisson calculation can be applied to each constant
piece of a zero-extended step function and then summed.  For any real or
complex piecewise-constant `z` supported in `I_x`, this gives the exact shape

```text
<z,A_x beta>=-B_Q<z,beta>+R_unit(z)+R_boundary(z),
B_Q=sum_(q in Q_x) q(q-2)/(q-1).
```

Here `R_unit` restores inputs divisible by `q`, and `R_boundary` contains all
outer endpoint and internal jump crossings.  No kernel reality, evenness, or
self-adjointness is introduced.

For `h=u-t`, the combined row obeys

```text
|v_(q,t)(t+h)| <= 1_(q|h)+2/q,
sum_h |h K_H(h)|(1_(q|h)+2/q) <<_psi H^2/q.
```

At displacement `h`, a step boundary can be crossed by at most `|h|`
source points.  Summing the jumps of the zero extension therefore gives

```text
|R_boundary(z)| <<_(psi,epsilon) Q H^2 V(z) x^epsilon.
```

For the three normalized contrasts this is
`O_(psi,epsilon)(x^(55/48+epsilon))`.  The input-unit term is
`O_epsilon(x^(5/6+epsilon))`, using `|beta(t)|<<_epsilon x^epsilon` and
`||z||_infty=O(x^(-1/2))`.

## 6. Three-mode and transverse floors

Weighted PNT gives

```text
B_Q=(9/2+o(1)) x^(2/3)/log(x).
```

Since the beta contrast error and the boundary error are both lower order
than `x^(7/6)/log^3(x)`, for each fixed `i` we obtain in `C`

```text
<zi,A_x beta>
 =-(9/2 kappa_i+o(1)) x^(7/6)/log^3(x).
```

Let `Z=span{z0,z1,z2}` and `T=span{z1,z2}`.  Exact orthonormality and
Parseval in this finite frame imply

```text
||P_Z A_x beta||_2
 =((9/2) sqrt(kappa0^2+kappa1^2+kappa2^2)+o(1)) x^(7/6)/log^3(x),

||P_T A_x beta||_2
 =((9/2) sqrt(kappa1^2+kappa2^2)+o(1)) x^(7/6)/log^3(x).
```

Numerically the two coefficient factors before `9/2` are approximately
`0.135096662713318` and `0.061792126717520`.  Since `T` is contained in
`z0`-perp, the second display is also a lower floor for the transverse
component `(I-z0 tensor z0)A_x beta`.

## 7. Boundary, epistemic and route firewall

The result is a source-backed lower-bound theorem for a three-dimensional
Haar projection.  It is not an upper estimate for `||A_x beta||_2`, and it
does not estimate the unprojected transverse component from above.  In
particular, the following remain open or unpaid:

```text
arithmetic L2 upper bound = NONE
full Gate B = OPEN
strict global 1/400 = UNPAID
fixed-atom credit = 0
twin-prime conclusion = NONE
```

The strongest obstruction is now sharper than the one-coordinate obstruction:
even the smallest source-only transverse Haar plane carries a same-order
literal adjoint floor.  The natural next experiment is therefore to form a
source-fixed linear combination in `span(z1,z2)` whose leading curvature
coefficient cancels, and to determine whether its remainder is genuinely
smaller or merely boundary-sized.
