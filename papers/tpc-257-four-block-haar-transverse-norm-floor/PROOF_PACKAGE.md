# TPC-257 proof package

## Theorem

Let `x` tend to infinity through real values.  On
`I_x=(x/2,x] intersect Z`, retain

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
beta(t)=Lambda(t)/log(t)-sum_(d|t,d<=U) mu(d),
```

and the literal V59 operator `A_x`.  Form the four ordered blocks from the
two TPC-256 rank children and let `z0,z1,z2` be the three contrasts in the
derivation package.  Define

```text
kappa0 = log(32/27)/sqrt(2),
kappa1 = log(3456/3125)/2,
kappa2 = log(884736/823543)/2.
```

Then `z0,z1,z2` are an exact orthonormal family and, for `i=0,1,2`,

```text
<zi,A_x beta>
 = -(9/2 kappa_i+o(1)) x^(7/6)/log^3(x)       (C).
```

Consequently, with `Z=span(z0,z1,z2)` and `T=span(z1,z2)`,

```text
||P_Z A_x beta||_2
 = ((9/2) sqrt(kappa0^2+kappa1^2+kappa2^2)+o(1)) x^(7/6)/log^3(x),

||P_T A_x beta||_2
 = ((9/2) sqrt(kappa1^2+kappa2^2)+o(1)) x^(7/6)/log^3(x).
```

In particular `T` is contained in `z0`-perp, so the second display is a
same-order lower floor for the component transverse to the TPC-256 midpoint.

Maximum status:

```text
PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR_FOR_LITERAL_V59_ADJOINT
```

This is a lower-bound theorem.  It is not an upper `L2` estimate and does not
close full Gate B.

## 1. Four-block lemma

Let `p,q` be positive integers and define
`h_{p,q}=sqrt(pq/(p+q))(1_A/p-1_B/q)` on adjacent sets of sizes `p,q`.
Writing `rho^2=pq/(p+q)`, direct counting gives

```text
||h_{p,q}||_2^2 = rho^2(1/p+1/q)=1.
```

For the four blocks, use the coefficient table below.  The entries omit the
corresponding square-root normalization; the block lengths multiply the
products.

| vector | `B1` | `B2` | `B3` | `B4` | normalization squared |
|---|---:|---:|---:|---:|---:|
| `z0` | `1/ell` | `1/ell` | `-1/r` | `-1/r` | `ell*r/(ell+r)` |
| `z1` | `1/s1` | `-1/s2` | `0` | `0` | `s1*s2/(s1+s2)` |
| `z2` | `0` | `0` | `1/s3` | `-1/s4` | `s3*s4/(s3+s4)` |

For `z0` against `z1`, the block-length-weighted coefficient product is

```text
s1*(1/ell)*(1/s1)+s2*(1/ell)*(-1/s2)=0.
```

The `z0,z2` computation is identical, and `z1,z2` have disjoint support.
Thus the three vectors are pairwise orthogonal.  The preceding norm identity
proves exact orthonormality, including the case of odd `N` or odd child
lengths.

For a normalized contrast, its zero-extended values have the order
`0,+rho/p,-rho/q,0`.  Hence

```text
V(h_{p,q})
 =rho/p+rho(1/p+1/q)+rho/q
 =2/rho.
```

This proves the frame and variation assertions.

## 2. Divisor lane

For a consecutive interval `J` of length `s`,

```text
#(J intersect dZ)=s/d+theta_(J,d), |theta_(J,d)|<=1.
```

Every pair defining `z_i` consists of equal leading-width intervals.  Insert
this identity into each pair of means.  The two `s/d` terms cancel for each
fixed `d`, before summing over `d` and before applying a triangle inequality.
Since `|mu(d)|<=1` and `rho_i(1/p_i+1/q_i)=1/rho_i`,

```text
|<zi,sum_(d|dot,d<=U)mu(d)>|
 <= U/rho_i = O(x^(-67/400)).                         (2.1)
```

The estimate is uniform for the three fixed macro pairs because
`rho_i asymp sqrt(x)`.

## 3. Prime-power curvature lemma

Set
`F(y)=sum_(2<=n<=y) Lambda(n)/log(n)`.  Separating prime powers gives

```text
F(y)=pi(y)+sum_(k>=2) pi(y^(1/k))/k.
```

The prime-power tail is `O(sqrt(y) log y)`.  The source-locked strong PNT
therefore gives

```text
F(y)=Li(y)+O(y exp(-c sqrt(log y))).                  (3.1)
```

Consider equal-width limiting intervals `A=[a_0,a_1]` and
`B=[b_0,b_1]`, width `d`.  Replacing rank endpoints by their scaled limits
costs `O(1/(x log x))` after normalization.  Uniformly on `[1/2,1]`,

```text
1/log(xy)=1/log(x)-log(y)/log^2(x)+O(log^(-3)(x)).
```

Using (3.1), the constant terms cancel between the two means and the
coefficient of `log^(-2)(x)` is

```text
C(A,B)=(1/d)(integral_B log(y)dy-integral_A log(y)dy).  (3.2)
```

Applying (3.2) to the three pairs gives

```text
C0=2 log(32/27),
C1=2 log(3456/3125),
C2=2 log(884736/823543).                              (3.3)
```

The normalizations satisfy

```text
rho0/sqrt(x)=1/(2sqrt(2))+O(1/x),
rho1/sqrt(x)=1/4+O(1/x),
rho2/sqrt(x)=1/4+O(1/x).                              (3.4)
```

Multiplying (3.2)--(3.4) and using (2.1) proves

```text
<zi,beta>=(kappa_i+O(1/log x))sqrt(x)/log^2(x),        (3.5)
```

where the three `kappa_i` in the theorem are positive.  The positivity follows
from `32/27>1`, `3456/3125>1`, and `884736/823543>1`.

## 4. Bounded-variation adjoint lemma

For `q` prime in `(Q,2Q]` and `q` not dividing `t`, set

```text
v_(q,t)(u)=1_(q does not divide u)
            (1_(u=t mod q)-1/(q-1)).
```

The complete period of this combined row is zero.  TPC-255 applies the
band-limited Poisson identity to the reflected-conjugate kernel row.  If a
zero-extended step function `z` is written as the sum of its constant pieces,
the complete-lattice terms telescope at every internal jump.  Deleting the
physical diagonal and restoring the `q|t` inputs gives the exact identity

```text
<z,A_x beta>=-B_Q<z,beta>+R_unit(z)+R_boundary(z),
B_Q=sum_(Q<q<=2Q, q prime) q(q-2)/(q-1).              (4.1)
```

The term `R_boundary` includes the two outer jumps of the zero extension and
all internal jumps.  This extension is algebraic: it makes no assertion that
the boundary is small until the next estimate.

For `h=u-t`, direct residue inspection gives

```text
|v_(q,t)(t+h)|<=1_(q|h)+2/q.                          (4.2)
```

Schwartz decay of `K_H` and `q<H` give

```text
sum_h |h K_H(h)|(1_(q|h)+2/q) <<_psi H^2/q.            (4.3)
```

For a fixed `h`, at most `|h|` source points cross any one step boundary.
Summing the jump heights in the zero extension and applying (4.2)--(4.3)
therefore gives

```text
|R_boundary(z)| <<_(psi,epsilon) Q H^2 V(z) x^epsilon. (4.4)
```

The input-unit restoration obeys

```text
|R_unit(z)| <<_epsilon x^(5/6+epsilon)                (4.5)
```

for each of the three contrasts, since `||z||_infty=O(x^(-1/2))`, there are at
most `x/q+1` multiples of `q`, and `|beta(t)|<<_epsilon x^epsilon`.

## 5. Coefficient asymptotics

The weighted prime number theorem and
`q(q-2)/(q-1)=q-1-1/(q-1)` give

```text
B_Q=(9/2+o(1))x^(2/3)/log(x).                         (5.1)
```

For each `z_i`, (4.1), (4.4), (4.5), and (3.5) give

```text
<zi,A_x beta>
 =-[(9/2+o(1))x^(2/3)/log(x)]
   [(kappa_i+o(1))sqrt(x)/log^2(x)]
   +O_(psi,epsilon)(x^(55/48+epsilon)).               (5.2)
```

The diagonal exponent in (5.2) is `2/3+1/2=7/6=56/48`.  The boundary exponent
is

```text
1/3+2(21/32)-1/2=55/48,
```

and the input-unit exponent is `5/6`.  Choosing a fixed
`0<epsilon<1/48` makes every remainder in (5.2) lower order than its diagonal
term.  This proves the three complex asymptotics in the theorem.  The argument
only uses a modulus bound on the remainder, so no reality of the kernel or of
the exact coefficients is inferred.

## 6. Parseval and the transverse lower floor

For an orthonormal family, finite-dimensional Parseval is an identity:

```text
||P_Z g||_2^2=sum_(i=0)^2 |<zi,g>|^2,
||P_T g||_2^2=sum_(i=1)^2 |<zi,g>|^2.
```

Insert (5.2).  Each leading constant is a positive real number, so taking
the square root is legitimate and gives the two norm asymptotics stated in
the theorem.  The inclusion `T subset z0-perp` follows from the exact
orthogonality already proved.  Thus the second norm is a lower bound for the
full transverse component, not an upper bound for it.

## 7. Quantifiers and claim firewall

- `x` is a real clock tending to infinity; all floor definitions remain in
  force.
- The profile is fixed, smooth, compactly supported on the Fourier side, and
  normalized as in TPC-255.
- Every `epsilon` in a remainder is fixed before taking `x` large; choose one
  below `1/48` only for the final dominance step.
- The frame is chosen from coordinates alone.  No coefficient-dependent
  direction is used.
- The theorem supplies lower floors for two projections.  It supplies no
  upper `L2` estimate, no full-output asymptotic, no `1/400` payment, no
  fixed-atom credit, and no twin-prime conclusion.

## Refuted shortcut

```text
REFUTED_SCOPED: after the TPC-256 midpoint coefficient is nonzero, the
orthogonal output can be assumed lower order without a separate theorem.
```

TPC-257 exhibits a source-only orthogonal plane whose projected output is of
the same power.  This obstruction is precisely why the next route should seek
a null direction or a genuinely collective upper estimate.
