# Bridge B V108: exact adjoint diagonal and hard-boundary compiler

Date: 2026-08-26

Status: `PROVED_EXACT_SOURCE_BACKED_L1_ADJOINT_DIAGONAL_HARD_WINDOW_CHILD_JUMP_COMPILER`

TPC-255 pushes the source-frozen rank midpoint through the literal V59
operator adjoint.  The complete-lattice unit-centered row vanishes exactly by
the V43 band-limited Poisson theorem.  What remains is not zero: deleting the
diagonal returns a weighted literal `beta` midpoint moment, while the physical
hard window and the jump between the two rank children produce two explicit
boundary lanes.  Every input/output unit-mask correction is retained.

This is an exact arithmetic-structure compiler, not an estimate.  No sign,
nonzero value, logarithmic saving, power saving, L2 theorem, Gate-B closure,
strict `1/400`, or twin-prime result is claimed.

## 1. Frozen physical operator and rank midpoint

Keep the literal V59 clock

```text
I_x=(x/2,x] intersect Z={n_1<...<n_N},
H=x^(21/32), Q=x^(1/3),
Q_x={q prime: Q<q<=2Q},
K_H(h)=hat(psi_+)(h/H),
beta(t)=Lambda(t)/log(t)
        -sum_(d|t,d^400<=x^133)mu(d).
```

The locked profile satisfies

```text
supp(psi_+) subset [-1,1],
K_H(0)=hat(psi_+)(0)=integral psi_+=1.
```

For `u,t in I_x`, TPC-247 defines

```text
A_x(u,t)
 =1_(u!=t) sum_(q in Q_x)
   q 1_(q does not divide u)1_(q does not divide t)
   K_H(u-t)[1_(u=t mod q)-1/(q-1)].
```

The inner product is conjugate-linear in the first slot.  Retain TPC-253's
coefficient-independent ordered-rank split

```text
ell=floor(N/2), r=N-ell,
L={n_1,...,n_ell}, R={n_(ell+1),...,n_N},
rho^2=ell*r/N,
z=z_mid=rho(1_L/ell-1_R/r).
```

This rank definition is primary for every real `x`.  The integer-only
`floor(3x/4)` crosswalk is not used at nonintegral clocks.

## 2. Unit-centered complete row

Fix `q in Q_x` and `t in I_x` with `q` not dividing `t`.  On the full integer
lattice define

```text
v_(q,t)(u)
 =1_(q does not divide u)
  [1_(u=t mod q)-1/(q-1)].
```

It is `q`-periodic and has exact mean zero.  Define the adjoint-oriented
complete row, exterior leakage, and child-jump term by

```text
P*_(q,t)=sum_(u in Z) conjugate(K_H(u-t)) v_(q,t)(u),

E*_(q,t)=sum_(u not in I_x) conjugate(K_H(u-t)) v_(q,t)(u),

J*_(q,t)=sum_(u in I_x) conjugate(K_H(u-t)) v_(q,t)(u)
          [z(u)-z(t)].
```

The exterior sums converge absolutely because the locked profile is smooth
and compactly supported, hence `K_H` is Schwartz on the physical lattice.

V43 proves exact complete-lattice cancellation for a unit-centered periodic
row when the first nonzero dual frequency lies outside the Fourier support.
Conjugating and reflecting the profile preserves support in `[-1,1]`.  Since

```text
q<=2Q and H>2Q
```

for sufficiently large `x`, its `d=1` case applies in the adjoint direction:

```text
P*_(q,t)=0.                                           (2.1)
```

No evenness, reality, or self-adjointness of `K_H` is used.

## 3. Exact coordinate decomposition of `A_x^* z`

For `q` not dividing `t`, add and subtract `z(t)` before deleting the
diagonal.  Since

```text
v_(q,t)(t)=1-1/(q-1)=(q-2)/(q-1),
```

finite algebra gives

```text
(A_x^*z)(t)
 =sum_(q in Q_x) q 1_(q does not divide t)
  [ z(t)P*_(q,t)-z(t)E*_(q,t)+J*_(q,t)
    -(q-2)/(q-1) conjugate(K_H(0)) z(t) ].           (3.1)
```

Using (2.1) and `K_H(0)=1` yields the source-backed normal form

```text
(A_x^*z)(t)
 =sum_(q in Q_x) q 1_(q does not divide t)
  [ -z(t)E*_(q,t)+J*_(q,t)-(q-2)/(q-1)z(t) ].       (3.2)
```

The last term is the deleted-diagonal return.  Complete-lattice Poisson
cancels only the centered alias; it does not cancel this returned local term.

The jump term is supported only across the rank midpoint.  Indeed,

```text
z_L-z_R=rho(1/ell+1/r)=1/rho,
```

so exactly

```text
J*_(q,t)=
  -rho^(-1) sum_(u in R) conjugate(K_H(u-t))v_(q,t)(u),  t in L,

J*_(q,t)=
  +rho^(-1) sum_(u in L) conjugate(K_H(u-t))v_(q,t)(u),  t in R.  (3.3)
```

Thus the two nonlocal survivors have distinct geometry: `E*` sees the two
outer endpoints of `I_x`, while `J*` sees the internal rank-child boundary.

## 4. Literal `beta` pairing and the `B_Q` return

Because `beta,z` are real and the first inner-product slot is conjugate
linear, conjugating (3.2) inside

```text
<z,A_x beta>=<A_x^*z,beta>
```

replaces `conjugate(K_H)` by `K_H`.  Write the corresponding unstarred
leakage terms as `E_(q,t),J_(q,t)`.  Then

```text
<z,A_x beta>
 =D_(beta,z)
  -sum_(q in Q_x)q sum_(t in I_x,q does not divide t)
      beta(t)z(t)E_(q,t)
  +sum_(q in Q_x)q sum_(t in I_x,q does not divide t)
      beta(t)J_(q,t),                                  (4.1)
```

where the exact diagonal lane is

```text
D_(beta,z)
 =-sum_(q in Q_x) q(q-2)/(q-1)
   sum_(t in I_x,q does not divide t) z(t)beta(t).    (4.2)
```

Put

```text
B_Q=sum_(q in Q_x) q(q-2)/(q-1).
```

Restoring the omitted input multiples gives the equivalent identity

```text
D_(beta,z)
 =-B_Q<z,beta>
  +sum_(q in Q_x) q(q-2)/(q-1)
   sum_(t in I_x,q divides t)z(t)beta(t).             (4.3)
```

The coefficient `B_Q` is exactly the shell coefficient returned by the V43
deleted-diagonal computation.  Formula (4.3) is the first literal reduction
of this lane to a weighted rank-midpoint `beta` moment plus an explicit input
unit-mask correction.  No estimate for either term is supplied here.

## 5. Output-unit correction cannot be dropped

For `q` not dividing `t`, decompose

```text
c_(q,t)(u)=1_(u=t mod q)-1/(q-1),
d_q(u)=1_(q divides u)/(q-1).
```

Then exactly

```text
v_(q,t)=c_(q,t)+d_q.                                  (5.1)
```

The two summands are not separately centered:

```text
sum_(a mod q)c_(q,t)(a)=-1/(q-1),
sum_(a mod q)d_q(a)=+1/(q-1).
```

Their complete-lattice zero-frequency contributions are respectively

```text
-H psi_+(0)/[q(q-1)] and +H psi_+(0)/[q(q-1)].
```

Only their sum vanishes.  Here `H psi_+(0)/q` is the residue-class Poisson
main term, while the deleted diagonal uses the different normalization
`K_H(0)=integral psi_+=1`.  Replacing `psi_+(0)` by
`hat(psi_+)(0)=1` conflates these two normalizations and is invalid.

If `q` divides `t`, the literal input mask makes the whole `q` summand zero.
The unit-centered complete-row theorem is never applied in that case.

## 6. Claim firewall and route evaluation

```text
TPC255_MAXIMUM_CLAIM = EXACT_SOURCE_BACKED_LITERAL_V59_ADJOINT_HAAR_DECOMPOSITION_INTO_BQ_WEIGHTED_BETA_MIDPOINT_INPUT_UNIT_CORRECTION_HARD_WINDOW_LEAKAGE_AND_CHILD_JUMP_LEAKAGE
TPC255_LITERAL_ADJOINT_ORIENTATION = PROVED_EXACT
TPC255_COMPLETE_UNIT_CENTERED_ROW = PROVED_EXACT_SOURCE_BACKED_ZERO_FOR_H_GREATER_THAN_2Q
TPC255_DELETED_DIAGONAL_RETURN = PROVED_EXACT
TPC255_HARD_WINDOW_LEAKAGE = PROVED_EXACT_IDENTITY_NO_ESTIMATE
TPC255_CHILD_JUMP_LEAKAGE = PROVED_EXACT_WITH_COEFFICIENT_PLUS_MINUS_ONE_OVER_RHO
TPC255_BQ_WEIGHTED_BETA_MIDPOINT = PROVED_EXACT_REDUCTION_NO_ESTIMATE
TPC255_INPUT_UNIT_MASK_CORRECTION = PROVED_EXACT_RETAINED
TPC255_OUTPUT_UNIT_MASK_CORRECTION = PROVED_EXACT_RETAINED_AND_JOINTLY_CENTERED_ONLY
TPC255_KERNEL_EVENNESS_OR_SELF_ADJOINTNESS = NOT_ASSUMED
TPC255_ADJOINT_HAAR_SAVING = OPEN
TPC255_DIAGONAL_BOUNDARY_COLLECTIVE_CANCELLATION = OPEN
TPC255_SIGN_OR_NONZERO = OPEN
TPC255_ROUTE_ADVANCE = YES_EXACT_LITERAL_STRUCTURE
TPC255_LITERAL_ARITHMETIC_STRUCTURE_ADVANCE = YES
TPC255_ARITHMETIC_ADVANCE = NO
TPC255_FIXED_ATOM_CREDIT = 0
TPC255_L2 = NONE
TPC255_FULL_GATE_B = OPEN
TPC255_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC255_TWIN_PRIME_RESULT = NONE
TPC255_STATUS = PROVED_EXACT_SOURCE_BACKED_L1_ADJOINT_DIAGONAL_HARD_WINDOW_CHILD_JUMP_COMPILER
```

Strongest positive result: the exact literal form `<z,A_x beta>` is now one
`B_Q`-weighted `beta` midpoint moment plus explicit input-unit, hard-window,
and child-jump corrections; the full-lattice centered alias is rigorously
zero.

Strongest obstruction: the deleted diagonal returns at shell size `B_Q`, and
no locked theorem controls its `beta` Haar moment collectively with the two
boundary lanes.  Triangulating prime by prime or mask by mask would destroy
the cancellation one must seek.

Open theorem: estimate the signed sum in (4.1)--(4.3) on the V59 clock while
retaining the prime shell, both unit masks, hard window, child jump, and
deleted diagonal.

Reusable structure:

```text
literal adjoint test
-> unit-centered complete lattice
-> band-limited Poisson zero
-> deleted-diagonal B_Q return
-> hard-window leakage
-> child-jump leakage
-> one literal beta-linear form.
```

`ROUND2_CLUE`:

```text
ATTACK_THE_BQ_WEIGHTED_LITERAL_BETA_RANK_MIDPOINT_TOGETHER_WITH_THE_HARD_WINDOW_AND_CHILD_JUMP_CORRECTIONS__DO_NOT_DECLARE_THE_POISSON_ZERO_A_PAYMENT_AND_DO_NOT_SEPARATE_THE_UNIT_MASK_OR_PRIME_SHELL
```
