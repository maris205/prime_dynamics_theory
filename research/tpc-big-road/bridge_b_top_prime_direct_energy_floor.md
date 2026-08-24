# Bridge B V93: top-prime direct-energy floor

Date: 2026-08-24

Status: `PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_DIRECT_ENERGY_FLOOR`.

TPC-240 answers the exact top-band question left by TPC-239.  It retains the
literal frozen common profile and the source coefficient on prime
denominators, but deliberately stops before the shell primes are collapsed
into common residue buckets.  On this exact q-split direct object, the
top-prime band has a positive asymptotic of order `Q^2/H=x^(1/96)` with an
explicit profile-dependent constant.  Thus this unsigned factor has no
fixed-power saving to offer.

## Registry and claim firewall

```text
TPC240_MAXIMUM_CLAIM = EXACT_FIXED_PROFILE_TOP_PRIME_Q_SPLIT_UNSIGNED_DIRECT_ENERGY_ASYMPTOTIC
TPC240_ROUTE_ADVANCE = YES_OBSTRUCTION
TPC240_FROZEN_COMMON_PROFILE = REQUIRED_FIXED_NONNEGATIVE_NORMALIZED_C_INFINITY
TPC240_TOP_PRIME_COEFFICIENT = PROVED_C_P_EQUALS_MINUS_LOG_P_OVER_P
TPC240_FIXED_Q_PRIMITIVE_ROW_NORM = PROVED_EXACT
TPC240_RIEMANN_ROW_ASYMPTOTIC = PROVED_UNIFORM_ON_TOP_PRIME_SHELL_FOR_EACH_FIXED_PROFILE
TPC240_KAPPA_RANGE = PROVED_ONE_HALF_LE_KAPPA_LE_ONE
TPC240_DIRECT_ENERGY_CONSTANT = PROVED_1197_KAPPA_LOG_2_OVER_800
TPC240_DIRECT_ENERGY_POWER = PROVED_X_1_OVER_96
TPC240_DIRECT_FIXED_POWER_SAVING = REFUTED_ON_EXACT_Q_SPLIT_UNSIGNED_OBJECT
TPC240_OPTIONAL_FINITE_WINDOW_FLOOR = PROVED_AT_ONE_HALF_TIMES_DIRECT_ENERGY
TPC240_X_1_OVER_48_SHARPNESS = NOT_CLAIMED
TPC240_CLASS_UNIFORM_PROFILE_THRESHOLD = NOT_CLAIMED
TPC240_PLATEAU_PROFILE_SUBSTITUTION = FORBIDDEN
TPC240_C_H_SIGNED_CANCELLATION = NONE
TPC240_SIGNED_FOUR_PACKET_GATE_B_SCALAR = OPEN
TPC240_ARITHMETIC_ADVANCE = NO
TPC240_FIXED_ATOM_CREDIT = 0
TPC240_L2 = NONE
TPC240_FULL_GATE_B = OPEN
TPC240_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC240_STATUS = PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_DIRECT_ENERGY_FLOOR
TPC240_ROUND2_CLUE = TEST_THE_TOP_PRIME_Q_COLLAPSED_COLLISION_EXCESS_OVER_THE_EXACT_DIRECT_FLOOR_BEFORE_CLAIMING_X_1_OVER_48_SHARPNESS
```

The theorem is an exact asymptotic for a q-split unsigned coefficient energy.
It is not the q-collapsed complete-period scalar from TPC-215, and it is not
the signed four-packet Gate-B scalar.  The word `ARITHMETIC_ADVANCE` remains
`NO` in the program's strict sense: no signed arithmetic `L2` estimate has
been proved.

## 1. Frozen object and quantifier

Keep the V59 scales

```text
H=x^(21/32),  Q=x^(1/3),  U=x^(133/400),
Q_x={q prime: Q<q<=2Q}.
```

Fix, independently of `x`, a real profile

```text
psi in C_c^infinity(R),
0<=psi<=1,
support(psi) subset [-1,1],
integral psi=1,
kappa_psi=integral_(-1)^1 |psi(t)|^2 dt.
```

For prime `p` and `q` in

```text
U/2<p<=U,  Q<q<=2Q,
```

put

```text
B_(p,q)^psi(a)
 = sum_(0<|m|<=floor(pq/H))
     psi(Hm/(pq)) 1_(m q^(-1)=a mod p).
```

TPC-215 gives the exact top-shell identity

```text
C_p=-log(p)/p.
```

Define the q-split unsigned top-prime direct energy

```text
D_top^psi
 = sum_(U/2<p<=U, p prime) |C_p|^2
   sum_(Q<q<=2Q, q prime)
   sum_(a mod p,(a,p)=1) |B_(p,q)^psi(a)|^2.         (1.1)
```

All asymptotics below mean: for every fixed admissible `psi` and every
`epsilon>0`, there is `x_0(psi,epsilon)` such that the stated estimate holds
for all `x>=x_0`.  No threshold uniform over the entire profile class is
asserted.

## 2. Exact primitive row and Riemann asymptotic

The scale identities

```text
U/Q=x^(-1/1200),
UQ/H=x^(23/2400)
```

show that eventually `p<q`, `4Q<H`, and

```text
M_(p,q)=floor(pq/H),  2M_(p,q)<p.
```

Thus `q` is invertible modulo `p`; every nonzero admissible `m` maps to a
nonzero, hence primitive, residue; and distinct signed multipliers do not
collide in one fixed q-row.  Consequently

```text
sum_((a,p)=1)|B_(p,q)^psi(a)|^2
 = sum_(0<|m|<=M_(p,q)) |psi(Hm/(pq))|^2.           (2.1)
```

For `T=pq/H`, the endpoint-safe lattice Riemann sum gives

```text
sum_(0<|m|<=floor(T)) |psi(m/T)|^2
 = kappa_psi T+O_psi(1).                             (2.2)
```

Indeed, the compactly supported smooth function `|psi|^2` vanishes at both
endpoints, and omitting `m=0` changes the full lattice sum by only one bounded
term.  The estimate is uniform in the top shells because

```text
T>=UQ/(2H)=(1/2)x^(23/2400) -> infinity.
```

The normalization of the frozen profile also yields the exact range

```text
1/2 <= kappa_psi <= 1.                               (2.3)
```

The lower bound follows from Cauchy on an interval of length two, and the
upper bound from `psi^2<=psi`.

## 3. Weighted-prime aggregation and exact constant

Substituting (2.2) into (1.1) factorizes the main term:

```text
D_top^psi
 = (kappa_psi/H)
   [sum_(Q<q<=2Q) q]
   [sum_(U/2<p<=U) (log p)^2/p]
   + aggregate error.                                (3.1)
```

The aggregate error is smaller than the main term by

```text
O_psi(H/(UQ))=O_psi(x^(-23/2400)).                  (3.2)
```

Partial summation and the prime number theorem give

```text
sum_(Q<q<=2Q) q
 = (3/2+o(1)) Q^2/log Q,

sum_(U/2<p<=U) (log p)^2/p
 = (log 2+o(1)) log U.                               (3.3)
```

Since `log U/log Q=399/400`, equations (3.1)--(3.3) prove

```text
D_top^psi
 = [1197 kappa_psi log(2)/800+o_psi(1)] Q^2/H
 = x^(1/96+o_psi(1)).                                (3.4)
```

In particular, `D_top^psi` is not `o(Q^2/H)`.  More strongly, no upper bound
with a fixed negative power relative to `Q^2/H` can hold for this exact
q-split unsigned object.

## 4. Scoped finite-window consequence

Let

```text
B_p^psi(a)=sum_(q in Q_x) B_(p,q)^psi(a).
```

Because the frozen profile is nonnegative,

```text
sum_a |B_p^psi(a)|^2
 >= sum_(q,a)|B_(p,q)^psi(a)|^2.                    (4.1)
```

Apply the TPC-238 lower frame to the distinct primitive-frequency coefficient
vector containing `z_(p,a)=C_p B_p^psi(a)`.  On any consecutive interval of
`N` comparable to `x` integers,

```text
N^(-1) sum_(n in I) |sum_(p,a) z_(p,a)e(na/p)|^2
 >= [1/2-pi^2 U^4/(6N^2)]_+ sum_(p,a)|z_(p,a)|^2
 >= [1/2-o(1)]D_top^psi.                             (4.2)
```

Here `U^4/N^2=x^(-67/100+o(1))`.  This corollary only transfers the
`x^(1/96)` direct floor.  It neither proves collision saturation nor the
sharpness of the TPC-239 exponent `1/48`.

## 5. Scope boundary and next theorem

TPC-215 already proved the top-shell singleton identity for `C_p`, and TPC-216
already proved fixed-q row injectivity.  TPC-240 does not rebrand either fact
as new.  Its new edge is the source-locked aggregate:

```text
top-prime singleton coefficient
 -> exact primitive fixed-q row
 -> uniform endpoint-safe Riemann asymptotic
 -> two weighted-prime averages
 -> explicit x^(1/96) lower floor.
```

Squaring `C_p` removes its sign.  The theorem also keeps q labels separated,
so it does not measure the same-frequency collision excess after the q-shell
is collapsed.  That collision excess is the next minimal object.  Only after
it is measured is it meaningful to ask whether the structural `x^(1/48)`
upper exponent is sharp.

```text
STRONGEST_POSITIVE_RESULT = EXACT_TOP_PRIME_Q_SPLIT_DIRECT_ENERGY_ASYMPTOTIC_WITH_CONSTANT_1197_KAPPA_LOG_2_OVER_800
STRONGEST_OBSTRUCTION = THE_EXACT_UNSIGNED_DIRECT_FACTOR_HAS_NO_O_Q_SQUARED_OVER_H_OR_FIXED_POWER_SAVING
OPEN_THEOREM = TOP_PRIME_Q_COLLAPSED_COLLISION_ENERGY_AND_ITS_EXCESS_OVER_THE_DIRECT_FLOOR
REUSABLE_STRUCTURE = TOP_PRIME_SINGLETON_PLUS_PRIMITIVE_ROW_RIEMANN_SUM_PLUS_FACTORIZED_WEIGHTED_PNT
ROUND2_CLUE = TEST_THE_TOP_PRIME_Q_COLLAPSED_COLLISION_EXCESS_OVER_THE_EXACT_DIRECT_FLOOR_BEFORE_CLAIMING_X_1_OVER_48_SHARPNESS
```

No signed `C_h` cancellation, signed four-packet projection, arithmetic `L2`,
fixed-atom credit, strict `1/400` payment, full Gate B, or twin-prime theorem
is claimed.
