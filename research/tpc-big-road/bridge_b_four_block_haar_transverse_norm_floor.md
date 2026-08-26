# Bridge B V110: four-block Haar lift and a transverse norm floor

Date: 2026-08-26

Status: `PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR_FOR_LITERAL_V59_ADJOINT`

TPC-257 keeps the exact literal V59 clock, coefficient, prime shell, output
unit masks, deleted diagonal, and complex kernel from TPC-256.  It makes the
next smallest source-only refinement: each ordered-rank child is split once
more, producing a four-block Haar frame before any coefficient or sign is
examined.

The result is deliberately a lower-bound theorem.  It proves that the two
within-child Haar directions carry same-order adjoint energy.  It does not
provide the missing full-vector upper `L2` estimate.

## 1. Frozen object and frame

```text
a=floor(x/2), b=floor(x), N=b-a,
ell=floor(N/2), r=N-ell, m=a+ell,
I_x={a+1,...,b}, L={a+1,...,m}, R={m+1,...,b},
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
beta(t)=Lambda(t)/log(t)-sum_(d|t,d<=U)mu(d).
```

Set `s1=floor(ell/2)`, `s2=ell-s1`, `s3=floor(r/2)`, and `s4=r-s3`.
The four consecutive blocks `B1,...,B4` have these lengths.  For adjacent
sets of sizes `p,q`, write

```text
h(A,B)=sqrt(pq/(p+q))(1_A/p-1_B/q).
```

The source-only frame is

```text
z0=h(B1 union B2,B3 union B4),
z1=h(B1,B2),
z2=h(B3,B4).
```

`z0` is the TPC-256 midpoint.  Exact block-length arithmetic gives

```text
<zi,zj>=delta_ij,
TV(zi)=2/rho_i,
rho_i^2=p_i q_i/(p_i+q_i).
```

In particular `T=span(z1,z2)` is contained in `z0`-perp.

## 2. Three literal beta moments

For every divisor layer, consecutive-interval endpoint counting cancels the
common `1/d` density before any triangle.  Thus

```text
|<zi,sum_(d|dot,d<=U)mu(d)>| <= U/rho_i=O(x^(-67/400)).
```

The strong PNT and second-order expansion of `Li` give

```text
<zi,beta>=(kappa_i+O(1/log x))sqrt(x)/log^2(x),
```

where

```text
kappa0=log(32/27)/sqrt(2),
kappa1=log(3456/3125)/2,
kappa2=log(884736/823543)/2.
```

All three constants are strictly positive.  The three logarithmic ratios are
the exact elementary integrals over `[1/2,3/4]` versus `[3/4,1]`, over
`[1/2,5/8]` versus `[5/8,3/4]`, and over `[3/4,7/8]` versus `[7/8,1]`.

## 3. Adjoint compiler and exponent ledger

For the complete combined unit row

```text
v_(q,t)(u)=1_(q does not divide u)
            [1_(u=t mod q)-1/(q-1)],
```

the TPC-255 Poisson argument extends by finite linearity to every
zero-extended piecewise-constant test function:

```text
<z,A_x beta>=-B_Q<z,beta>+R_unit(z)+R_boundary(z),
B_Q=sum_(Q<q<=2Q,q prime)q(q-2)/(q-1).
```

The combined mask remains intact.  Its pointwise bound and Schwartz first
moment are

```text
|v_(q,t)(t+h)|<=1_(q|h)+2/q,
sum_h |h K_H(h)|(1_(q|h)+2/q)<<_psi H^2/q.
```

The zero extension of each frame vector has total variation `O(x^(-1/2))`.
At a fixed shift, each jump is crossed by at most `|h|` source points, so

```text
R_boundary(zi)=O_(psi,epsilon)(x^(55/48+epsilon)),
R_unit(zi)=O_epsilon(x^(5/6+epsilon)).
```

Weighted PNT gives `B_Q=(9/2+o(1))x^(2/3)/log x`.  The diagonal exponent is
`7/6=56/48`, while the boundary exponent is `55/48`; the gap is exactly
`1/48`.  Hence, for each `i`,

```text
<zi,A_x beta>=-(9/2*kappa_i+o(1))x^(7/6)/log^3(x)  in C.
```

## 4. New norm floor

Finite Parseval now gives

```text
||P_span(z0,z1,z2) A_x beta||_2
 =((9/2)sqrt(kappa0^2+kappa1^2+kappa2^2)+o(1))
   x^(7/6)/log^3(x),

||P_T A_x beta||_2
 =((9/2)sqrt(kappa1^2+kappa2^2)+o(1))
   x^(7/6)/log^3(x).
```

The factors before `9/2` are respectively
`0.135096662713318...` and `0.061792126717520...`.  Since `T` is orthogonal
to the old midpoint, the second line is a same-order lower floor for the
midpoint-transverse component.

## 5. Claim firewall and route decision

```text
TPC257_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR_FOR_LITERAL_V59_ADJOINT
TPC257_ROUTE_ADVANCE = YES_SCOPED_TRANSVERSE_HAAR
TPC257_ARITHMETIC_ADVANCE = YES_SCOPED_TRANSVERSE_LOWER_FLOOR
TPC257_THREE_MODE_HAAR_ORTHOGONALITY = PROVED_EXACT
TPC257_TRANSVERSE_OUTPUT_FLOOR = PROVED_SOURCE_BACKED
TPC257_FULL_OUTPUT_NORM_FLOOR = PROVED_SOURCE_BACKED
TPC257_L2 = NONE
TPC257_FIXED_ATOM_CREDIT = 0
TPC257_FULL_GATE_B = OPEN
TPC257_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC257_TWIN_PRIME_RESULT = NONE
TPC257_STATUS = PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR
```

`FULL_OUTPUT_NORM_FLOOR` is a lower bound for a finite projection.  It is not
an upper bound for `||A_x beta||_2`, and it does not pay full Gate B.

Strongest positive result: a source-only two-dimensional transverse plane has
an explicit same-order literal adjoint lower floor.

Strongest obstruction: one midpoint coefficient cannot be promoted to a
lower-order transverse remainder.

Open theorem: find a source-frozen transverse null direction, or prove a
collective upper estimate while retaining all literal masks, the deleted
diagonal, and both boundary lanes.

Reusable structure:

```text
four-block rank Haar frame
 -> exact orthonormality and variation
 -> divisor-density cancellation
 -> second-order PNT curvature table
 -> B_Q diagonal amplification
 -> bounded-variation boundary compiler
 -> Parseval transverse floor.
```

`ROUND2_CLUE`:

```text
USE_THE_EXPLICIT_TWO_DIMENSIONAL_TRANSVERSE_HAAR_FLOOR_TO_SEARCH_FOR_A_SOURCE_FROZEN_DIAGONAL_NULL_DIRECTION_BEFORE_ATTEMPTING_ANY_FULL_GATE_B_UPPER_BOUND
```
