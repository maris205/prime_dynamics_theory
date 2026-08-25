# Bridge B V109: literal beta Haar and diagonal-dominant adjoint asymptotic

Date: 2026-08-26

Status: `PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC`

TPC-256 estimates the literal adjoint lane isolated by TPC-255.  The truncated
Möbius divisor density cancels between the two consecutive rank children up to
an endpoint discrepancy.  The second-order curvature of the prime density
therefore gives an explicit positive main term for the literal beta Haar
moment.  TPC-255's deleted-diagonal coefficient amplifies that moment, while
the input-unit, hard-window and child-jump lanes are smaller by a fixed power.

This is a scoped arithmetic advance for one ordered-rank Haar projection.  It
does not give full output control, an arithmetic `L2` estimate, full Gate B,
the strict `1/400` payment, fixed-atom credit, or a twin-prime theorem.

## 1. Frozen clock, coefficient and operator

Let real `x` tend to infinity and put

```text
a=floor(x/2),  b=floor(x),
I_x=(x/2,x] intersect Z={a+1,...,b},
N=b-a,  ell=floor(N/2),  r=N-ell,
m=a+ell,
L={a+1,...,m},  R={m+1,...,b},
rho^2=ell*r/N,
z=z_mid=rho(1_L/ell-1_R/r).
```

Thus the two rank children are consecutive integer intervals for every real
`x`, and

```text
N=x/2+O(1),  ell=x/4+O(1),  r=x/4+O(1),
rho=sqrt(x)/(2sqrt(2))+O(x^(-1/2)).                  (1.1)
```

Retain the literal V35 coefficient and the V59 clocks

```text
U=x^(133/400),  H=x^(21/32),  Q=x^(1/3),
beta(t)=Lambda(t)/log(t)-sum_(d|t,d<=U)mu(d),
Q_x={q prime: Q<q<=2Q}.
```

The inner product is conjugate-linear in its first slot.  The operator `A_x`
and kernel `K_H(h)=hat(psi_+)(h/H)` are exactly those frozen in TPC-247 and
TPC-255.  The profile is fixed, smooth and compactly supported on the Fourier
side, with `integral psi_+=1`.  Neither reality nor evenness of `K_H` is
assumed.

## 2. Exact cancellation of the divisor-density main term

Define

```text
D_U(t)=sum_(d|t,d<=U)mu(d).
```

For every positive integer `d` and every consecutive integer interval `J` of
length `s`, elementary endpoint counting gives

```text
# {n in J: d|n}=s/d+O(1),                            (2.1)
```

with an absolute constant.  Consequently

```text
mean_L(D_U)=sum_(d<=U)mu(d)/d+O(U/ell),
mean_R(D_U)=sum_(d<=U)mu(d)/d+O(U/r).
```

The common density cancels layer by layer; no cancellation theorem for the
Möbius function is used.  Since

```text
rho(1/ell+1/r)=1/rho,                                (2.2)
```

we obtain

```text
|<z,D_U>|<=U/rho=O(x^(-67/400)).                     (2.3)
```

This endpoint term is much smaller than the main term below.

## 3. Second-order prime-density curvature

Set

```text
A(y)=sum_(2<=n<=y)Lambda(n)/log(n).
```

Writing every prime power separately gives

```text
A(y)=pi(y)+sum_(k>=2)(1/k)pi(y^(1/k)).                (3.1)
```

The prime-power tail is `O(sqrt(y)log y)`.  The classical de la Vallée
Poussin prime number theorem frozen in TPC-233 therefore implies, for some
fixed `c>0`,

```text
A(y)=Li(y)+O(y exp(-c sqrt(log y))).                  (3.2)
```

The `O(1)` motions of `a,m,b` relative to `x/2,3x/4,x` contribute only a
negligible endpoint error after division by `ell` or `r`.  Uniformly for
`y` in `[1/2,1]`,

```text
1/(log x+log y)
 =1/log x-(log y)/log^2 x+O(1/log^3 x).              (3.3)
```

The constant terms in the two child means cancel.  The next term is

```text
4[ integral_(3/4)^1 log y dy
   -integral_(1/2)^(3/4) log y dy ]
 =2log(32/27).                                       (3.4)
```

Equations (3.2)--(3.4) yield

```text
mean_L(Lambda/log)-mean_R(Lambda/log)
 =2log(32/27)/log^2 x+O(1/log^3 x).                  (3.5)
```

Combining (1.1), (2.3) and (3.5) proves the first main theorem:

```text
<z,beta>
 =[log(32/27)/sqrt(2)]sqrt(x)/log^2 x
  +O(sqrt(x)/log^3 x).                               (3.6)
```

In particular `<z,beta>` is real, positive and nonzero for every sufficiently
large real `x`.

## 4. TPC-255 diagonal and boundary ledger

For `q` in `Q_x` and `q` not dividing `t`, retain the combined output-unit row

```text
v_(q,t)(u)=1_(q does not divide u)
            [1_(u=t mod q)-1/(q-1)].                 (4.1)
```

TPC-255 proves the exact identity

```text
<z,A_x beta>
 =-B_Q<z,beta>+R_unit+R_hard+R_jump,                 (4.2)

B_Q=sum_(q in Q_x)q(q-2)/(q-1).                     (4.3)
```

The three remainders are, respectively, the restoration of inputs divisible
by `q`, the two outer endpoints of `I_x`, and the internal boundary between
the rank children.  All outer `q` weights, both unit masks, the deleted
diagonal and the original complex kernel remain attached.

The exact algebraic identity

```text
q(q-2)/(q-1)=q-1-1/(q-1)
```

and weighted prime number theorem give

```text
B_Q=(3/2+o(1))Q^2/log Q
   =(9/2+o(1))x^(2/3)/log x.                         (4.4)
```

## 5. First-moment localization of both boundaries

If `q` does not divide `t` and `h=u-t`, direct residue inspection of the
combined row (4.1) gives

```text
|v_(q,t)(t+h)|<=1_(q|h)+2/q.                         (5.1)
```

The two pieces used to define (4.1) are not separately centered; (5.1) is
applied only after they have been recombined.  Schwartz decay of the fixed
profile gives

```text
sum_(h in Z)|h K_H(h)|[1_(q|h)+2/q]
 <<_psi H^2/q.                                       (5.2)
```

Indeed, the unrestricted first moment is `O_psi(H^2)`, while the substitution
`h=qk` gives `O_psi(H^2/q)` on the divisible sublattice.

For each fixed shift `h`, at most `|h|` inputs cross either outer endpoint of
`I_x`, and at most `|h|` ordered pairs cross the internal rank boundary.
Moreover

```text
|z(t)|<=1/rho,
|z(u)-z(t)|=1/rho  on a cross-child pair.             (5.3)
```

The standard divisor bound and the exact definition of `beta` give, for every
fixed `epsilon>0`,

```text
|beta(t)|<=1+tau(t)<<_epsilon x^epsilon.              (5.4)
```

Applying (5.2)--(5.4) before summing the common prime shell proves

```text
R_hard,R_jump
 <<_(psi,epsilon) QH^2 x^epsilon/rho
 <<_(psi,epsilon) x^(55/48+epsilon).                 (5.5)
```

For the input-unit correction, the number of multiples of `q` in `I_x` is at
most `x/q+1`.  Thus

```text
R_unit
 <<_epsilon x^epsilon/rho
    sum_(q in Q_x)q(x/q+1)
 <<_epsilon x^(5/6+epsilon).                         (5.6)
```

No cancellation between distinct primes is required for (5.5) or (5.6).
The prohibition is earlier: the output-unit row cannot be split before its
exact recentering and Poisson cancellation.

## 6. Diagonal-dominant complex asymptotic

The diagonal term from (3.6) and (4.4) has exponent

```text
2/3+1/2=7/6=56/48.
```

The hard-window and child-jump bounds have exponent `55/48`; hence the
boundary separation is exactly

```text
7/6-55/48=1/48.                                     (6.1)
```

Choose any fixed `0<epsilon<1/48`.  Equations (3.6), (4.2), (4.4),
(5.5) and (5.6) prove in the complex plane

```text
<z,A_x beta>
 =-[9log(32/27)/(2sqrt(2))+o(1)]x^(7/6)/log^3 x.     (6.2)
```

The main term is negative real, but the exact scalar need not be real.  The
safe consequences for the real part, nonzero value and normalized phase are

```text
Re <z,A_x beta><0                 eventually,
<z,A_x beta> != 0                 eventually,
<z,A_x beta>/|<z,A_x beta>| -> -1.                  (6.3)
```

An unqualified assertion that the principal argument tends to `+pi` is not
made: a complex error may approach the negative axis from either side.  No
self-adjointness or kernel evenness is inferred.

## 7. Source and claim firewall

The literal coefficient and `x^(133/400)` cutoff are frozen by the V35
proper-factor reduction and the V52 compensated-pair compiler.  TPC-253 fixes
the real-clock ordered-rank Haar vector.  TPC-233 supplies the classical strong
PNT input.  The weighted prime-shell asymptotic is already used in TPC-240.
TPC-255 supplies (4.2) with the masks and boundaries intact.  The V43
first-moment calculation supplies the `H^2/q` scaling in (5.2).

```text
TPC256_LITERAL_BETA_DIVISOR_DENSITY_CANCELLATION = PROVED_EXACT_ENDPOINT_BOUND
TPC256_LITERAL_BETA_HAAR_ASYMPTOTIC = PROVED_SOURCE_BACKED
TPC256_BQ_WEIGHTED_PRIME_ASYMPTOTIC = PROVED_SOURCE_BACKED
TPC256_COMBINED_UNIT_ROW_FIRST_MOMENT = PROVED_SOURCE_BACKED
TPC256_INPUT_UNIT_BOUND = PROVED_SOURCE_BACKED
TPC256_HARD_WINDOW_BOUND = PROVED_SOURCE_BACKED
TPC256_CHILD_JUMP_BOUND = PROVED_SOURCE_BACKED
TPC256_BOUNDARY_POWER_SEPARATION = PROVED_EXACT_ONE_OVER_48
TPC256_ADJOINT_NORMALIZED_COMPLEX_ASYMPTOTIC = PROVED_SOURCE_BACKED
TPC256_REAL_PART_EVENTUALLY_NEGATIVE = PROVED
TPC256_SCALAR_EVENTUALLY_NONZERO = PROVED
TPC256_NORMALIZED_PHASE_TO_MINUS_ONE = PROVED
TPC256_SCALAR_IS_REAL = NOT_CLAIMED
TPC256_UNQUALIFIED_PRINCIPAL_ARGUMENT_TO_PLUS_PI = NOT_CLAIMED
TPC256_ROUTE_ADVANCE = YES_LITERAL_ARITHMETIC
TPC256_ARITHMETIC_ADVANCE = YES_SCOPED_LITERAL_BETA_ADJOINT_HAAR_LANE
TPC256_FIXED_ATOM_CREDIT = 0
TPC256_L2 = NONE
TPC256_FULL_GATE_B = OPEN
TPC256_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC256_TWIN_PRIME_RESULT = NONE
TPC256_STATUS = PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC
```

Strongest positive result: the literal beta midpoint has an explicit positive
asymptotic, and the returned diagonal forces a nonzero negative-real leading
asymptotic for the literal adjoint Haar scalar.

Strongest obstruction: this is one fixed Haar projection.  It does not control
the transverse/full-output component of `A_x beta`, and the output-unit pieces
still cannot be Poisson-split before exact recentering.

Open theorem: control the transverse/full-output component and couple it to the
physical `w` lane on the same V59 clock while retaining the prime shell, both
unit masks, deleted diagonal and hard window.

Reusable structure:

```text
consecutive-interval divisor-density cancellation
-> second-order PNT curvature
-> explicit beta Haar main term
-> B_Q diagonal amplification
-> first-moment hard/jump localization
-> boundary power separation.
```

`ROUND2_CLUE`:

```text
EXPLOIT_EXACT_DIVISOR_DENSITY_CANCELLATION_BEFORE_ANY_TRIANGLE__THEN_USE_THE_BQ_DIAGONAL_MAIN_AND_H2_OVER_Q_BOUNDARY_MOMENT_TO_ISOLATE_THE_TRANSVERSE_FULL_GATE_B_REMAINDER
```
