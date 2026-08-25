# Bridge B V106: source-frozen rank-midpoint contrast compiler

Date: 2026-08-25

Status: `PROVED_STRUCTURAL_L1_SOURCE_FROZEN_RANK_MIDPOINT_CONTRAST_COMPILER`

TPC-253 takes the obstruction isolated by TPC-252 literally: the partition is
now fixed from the ordered physical interval before any coefficient, contrast,
or margin is inspected.  The result is an exact finite compiler, not an
estimate for the resulting V59 contrast.

## 1. Coefficient-independent rank midpoint

Let `x>0` be real and write

```text
I_x=(x/2,x] intersect Z={n_1<...<n_N},
N=floor(x)-floor(x/2)>=2.
```

Put

```text
ell=floor(N/2),
r=ceil(N/2)=N-ell,
L={n_1,...,n_ell},
R={n_(ell+1),...,n_N}.
```

This ordered rank split depends only on the clock `x` and its coordinate set.
It is declared before inspecting `beta`, `w`, `A_x beta`, any margin, or any
sign.  It is a source-frozen modeling choice, not a unique V59-canonical
partition and not V59's smooth bounded-overlap mesoscopic partition.

With the inner product conjugate-linear in the first slot, define

```text
rho=sqrt(ell r/N),
z=rho(1_L/ell-1_R/r).
```

Then

```text
sum_(n in I_x) z(n)=0,
||z||^2=rho^2(1/ell+1/r)=1.
```

Thus `z` is the unique signed normalized child contrast whose sign is positive
on `L`.  If `u_J=|J|^(-1/2)1_J`,

```text
M_coarse=u_(I_x) tensor u_(I_x),
M_mid=u_L tensor u_L+u_R tensor u_R,
M_mid=M_coarse+z tensor z.
```

For integer `x=k>=3`, the first `ell` coordinates end at

```text
floor(k/2)+ell=floor(3k/4).
```

Hence the rank split is exactly

```text
L=(k/2,floor(3k/4)] intersect Z,
R=(floor(3k/4),k] intersect Z.
```

The rank definition, rather than this integer-only threshold formula, remains
the primary definition.

## 2. Partial-sum contrast compiler

For a vector `f` and a coordinate set `J`, write

```text
S_f(J)=sum_(n in J)f(n).
```

Because `z` is real,

```text
<z,f>=rho[S_f(L)/ell-S_f(R)/r].
```

Retain the literal TPC-247 shared-lane object

```text
g=A_x beta,
C_x=<w,g>.
```

Set `W_J=S_w(J)` and `G_J=S_g(J)`.  Direct block averaging gives

```text
C_long(mid)=conjugate(W_L)G_L/ell+conjugate(W_R)G_R/r,
C_long(coarse)=conjugate(W_L+W_R)(G_L+G_R)/N.
```

TPC-252's rank-one transfer now specializes to the coefficient-independent
midpoint:

```text
C_long(mid)-C_long(coarse)
 =conjugate(<z,w>)<z,g>
 =(ell r/N)
   conjugate(W_L/ell-W_R/r)(G_L/ell-G_R/r),

Q_trans(mid)-Q_trans(coarse)
 =-conjugate(<z,w>)<z,g>.
```

Writing `mu_f(J)=S_f(J)/|J|`, the remaining midpoint transverse covariance is

```text
Q_trans(mid)
 =sum_(J in {L,R}) sum_(n in J)
    conjugate(w(n)-mu_w(J))[g(n)-mu_g(J)].
```

Consequently,

```text
C_x=C_long(mid)+Q_trans(mid),
Q_trans(coarse)=conjugate(<z,w>)<z,g>+Q_trans(mid).
```

No sign or monotonicity for either complex longitudinal term follows.

## 3. Literal V59 kernel expansion

Keep the exact V59 data

```text
H=x^(21/32),
Q=x^(1/3),
Q_x={q prime:Q<q<=2Q},
K_H(h)=hat(psi_+)(h/H),

beta(t)=Lambda(t)/log t
        -sum_(d|t, d^400<=x^133)mu(d),
w(u)=Lambda(u+2)-b_x^(z)(u).
```

The TPC-247 source operator is

```text
A_x(u,t)
 =1_(u!=t) sum_(q in Q_x)
    q 1_(q does not divide u)1_(q does not divide t)
    K_H(u-t)[1_(u=t mod q)-1/(q-1)].
```

Substituting this operator into the midpoint moment preserves every literal
factor:

```text
<z,A_x beta>
 =rho sum_(q in Q_x) q sum_(u,t in I_x)
   [1_L(u)/ell-1_R(u)/r]
   1_(u!=t)
   1_(q does not divide u)1_(q does not divide t)
   beta(t)K_H(u-t)
   [1_(u=t mod q)-1/(q-1)].
```

In particular, output/input orientation, outer prime weight, both unit masks,
deleted diagonal, physical kernel, centered residue bracket, and literal
`beta` all remain present.

The safe adjoint identity is

```text
<z,A_x beta>=<A_x^*z,beta>,
(A_x^*z)(t)=sum_(u in I_x)conjugate(A_x(u,t))z(u).
```

No symmetry of `K_H`, equality `A_x^*=A_x`, or self-adjointness of `A_x` is
source-locked here.

## 4. Sharp structural controls

The compiler alone cannot force a sign or nonzero contrast.  On any clock,
constant `w` gives `<z,w>=0`; constant `g` gives `<z,g>=0`.  Conversely, the
synthetic choices

```text
w=z, g=z
```

give transfer `+1`, while

```text
w=z, g=-z
```

give transfer `-1`.  These are exact finite Hilbert-space controls, not
literal numerical V59 instances.  They prove that source-free geometry cannot
decide the arithmetic sign, nonvanishing, or scale.

## 5. Route evaluation

Strongest positive result: the physical coordinate clock now supplies a
coefficient-independent hard two-block direction, and its two literal V59
moments have exact partial-sum, source-kernel, adjoint, covariance-transfer,
and within-child formulas.

Strongest obstruction: no locked source estimates either actual midpoint
imbalance `<z,w>` or `<z,A_x beta>` on one common growing V59 clock.  The exact
compiler therefore supplies no sign, nonzero value, power saving, or payable
margin by itself.

Open theorem: obtain a source-backed bound or sign-sensitive joint estimate
for the two literal rank-midpoint contrasts and the associated projected
radius on a common V59 clock.

Reusable structure: ordered physical interval -> rank midpoint -> normalized
Haar contrast -> partial-sum imbalance -> literal source-kernel imbalance ->
rank-one covariance transfer -> within-child covariance.

`ROUND2_CLUE = AUDIT_THE_TWO_LITERAL_RANK_MIDPOINT_IMBALANCES_WITH_EXISTING_PRIME_AND_HYBRID_MEAN_THEOREMS_BEFORE_ANY_DYADIC_EXTENSION`

## 6. Claim firewall

```text
TPC253_RANK_MIDPOINT_PARTITION = PROVED_SOURCE_ONLY_DETERMINISTIC
TPC253_INTEGER_THREE_QUARTER_CROSSWALK = PROVED_EXACT
TPC253_MIDPOINT_CONTRAST_NORMALIZATION = PROVED_EXACT
TPC253_PARTIAL_SUM_MOMENT_COMPILER = PROVED_EXACT
TPC253_LITERAL_V59_G_MOMENT_EXPANSION = PROVED_EXACT
TPC253_MIDPOINT_LONGITUDINAL_FORMULA = PROVED_EXACT
TPC253_COARSE_TO_MIDPOINT_COVARIANCE_TRANSFER = PROVED_EXACT
TPC253_WITHIN_CHILD_COVARIANCE_DECOMPOSITION = PROVED_EXACT
TPC253_SAFE_ADJOINT_CROSSWALK = PROVED_EXACT
TPC253_A_X_SELF_ADJOINTNESS = NOT_CLAIMED
TPC253_MIDPOINT_V59_CANONICALITY = NOT_CLAIMED_SOURCE_ONLY_MODELING_CHOICE
TPC253_SMOOTH_V59_PARTITION_IDENTIFICATION = NOT_CLAIMED
TPC253_ACTUAL_V59_NUMERICAL_REPLAY = NOT_TESTABLE_FROM_LOCKED_MATERIAL
TPC253_MIDPOINT_CONTRAST_SIGN_OR_NONZERO = OPEN
TPC253_ARITHMETIC_ADVANCE = NO
TPC253_FIXED_ATOM_CREDIT = 0
TPC253_L2 = NONE
TPC253_FULL_GATE_B = OPEN
TPC253_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC253_TWIN_PRIME_RESULT = NONE
TPC253_STATUS = PROVED_STRUCTURAL_L1_SOURCE_FROZEN_RANK_MIDPOINT_CONTRAST_COMPILER
```
