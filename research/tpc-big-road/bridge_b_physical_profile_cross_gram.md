# Bridge A / Gate B TPC-213: physical profile pullback and the cross-divisor Gram

Date: 2026-08-18

Status: `PROVED_STRUCTURAL_L1 / CROSS_DIVISOR_COUPLING`.

TPC-212 showed that the reciprocal-emitter Gram is block diagonal only in a
natural direct sum in which divisor residuals are treated as independent.  The
literal V46 residuals instead come from one common physical sequence.  TPC-213
constructs that common-source map before Cauchy and identifies its exact
cross-divisor Gram.

## Common-source pullback theorem

Let `U` be a finite set of integer indices.  For every modulus `d`, define

```text
(C_d f)(a) = sum_(u in U, u == a mod d) f(u)
(F_d g)(r) = sum_(a mod d) g(a) exp(2*pi*i*r*a/d)
K_d(u) = sum_(r mod d) A_d(r) exp(2*pi*i*r*u/d)
```

For a common source `v` and divisor-dependent profile correction `b_d`, put
`R_d=C_d(v-b_d)`.  Direct finite expansion gives

```text
sum_d sum_r A_d(r) (F_d R_d)(r)
 = sum_u v(u) K(u) - sum_d sum_u b_d(u) K_d(u),
K(u)=sum_d K_d(u).
```

The first term uses one common physical source; it is not a direct sum of
independent divisor variables.  The second term retains the literal
divisor-dependent Euler correction.

## Residue-lift cross block

If `U={0,...,L-1}` and `L` is a multiple of `lcm(d,e)`, the CRT count is

```text
(C_d C_e^*)(a,b)
 = (L/lcm(d,e)) 1_(a == b mod gcd(d,e)).
```

Thus nested or non-coprime divisor lifts have deterministic cross blocks.  The
common-source map is generally not an orthogonal direct sum.

## Emitter pullback frequency-intersection Gram theorem

For arbitrary finite `U`, expansion gives

```text
sum_(u in U) K_d(u) conjugate(K_e(u))
 = sum_(r,s) A_d(r) conjugate(A_e(s))
   sum_(u in U) exp(2*pi*i*u*(r/d-s/e)).
```

For one complete period `L=lcm(d,e)`, finite geometric-series orthogonality
reduces this to

```text
sum_(u mod L) K_d(u) conjugate(K_e(u))
 = L sum_(r/d == s/e mod 1) A_d(r) conjugate(A_e(s)).
```

This is the exact physical cross-divisor Gram.  It does not assert that its
off-diagonal terms have a favorable sign.

## Finite release certificate

The numbered project is `papers/tpc-213-physical-profile-cross-gram/`.  Its
fixture uses `d={5,7,35}`, `U={0,...,34}`, `z=3`, `q={11,13,17}`, and `H=40`.
The joint residue lift has `47` rows, rank `35`, and twelve codomain
dependencies.  The unit-weight emitter has exact cross-Gram values

```text
(d,e)=(5,7)   : 0
(d,e)=(5,35)  : 560
(d,e)=(7,35)  : 770
```

The producer and independent checker use exact integer/rational arithmetic.
The unit reciprocal weights and omitted logarithmic scalar are a finite
modeling choice, not a replacement for the smooth physical `psi` or
`mu(d) log(d)/d` coefficient.

## Claim firewall

```text
TPC213_MAXIMUM_CLAIM = EXACT_COMMON_SOURCE_PROFILE_PULLBACK_AND_FINITE_CROSS_DIVISOR_GRAM
TPC213_ROUTE_ADVANCE = YES
TPC213_STRUCTURAL_THRESHOLD_A = PASS
TPC213_PHYSICAL_PROFILE_EMITTER_PULLBACK = PROVED_EXACT
TPC213_RESIDUE_LIFT_GCD_ALIASING = PROVED_EXACT
TPC213_CROSS_DIVISOR_FREQUENCY_GRAM = PROVED_EXACT_FINITE
TPC213_PHYSICAL_DIRECT_SUM_REPLACEMENT = REFUTED_SCOPED
TPC213_LITERAL_V46_ASYMPTOTIC_GRAM_BOUND = OPEN
TPC213_PRIME_SHELL_REASSEMBLY = OPEN
TPC213_ARITHMETIC_ADVANCE = NO
TPC213_FIXED_ATOM_CREDIT = 0
TPC213_L2 = NONE
TPC213_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC213_TPC_TRIGGER = true
```

The scoped refutation concerns only the replacement of the common-source
physical map by an orthogonal direct sum.  It is not an arithmetic
counterexample and does not refute a future signed physical Gram estimate.

## Route position

```text
V65 / TPC-212: cut boundary + reciprocal emitter direct-sum obstruction
        |
        v
V66 / TPC-213: common-source profile pullback + cross-divisor Gram
        |
        +-- gcd/lcm residue aliasing                         PROVED
        +-- shared-frequency emitter cross Gram              PROVED finite
        +-- direct-sum physical replacement                   REFUTED scoped
        +-- literal smooth joint Gram estimate                OPEN
        +-- prime-shell signed reassembly                     OPEN
        +-- strict 1/400 and twin-prime endpoint              UNPAID
```

The next theorem should group the literal V46 emitter by shared rational
frequency, retain `mu(d) log(d)`, `psi`, four-packet signs, and the zero axis,
and determine whether the resulting clusters cancel or form a positive-Gram
obstruction.
