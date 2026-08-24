# Bridge B V94: top-prime collision lower bound and fixed-power sharpness

Date: 2026-08-24

Status: `PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_COLLISION_SHARPNESS`.

TPC-241 completes the unsigned common-profile audit opened by TPC-237 and
narrowed by TPC-238--240.  TPC-240 proved that q-split top-prime direct energy
already has size `x^(1/96)`.  TPC-241 now collapses the shell primes into their
literal common residue buckets.  Profile normalization supplies a positive
first moment, residue Cauchy supplies the collision factor, and the TPC-238
lower frame transfers it to the physical finite window.  The result is an
`x^(1/48)/log x` lower bound, so the structural fixed-power exponent `1/48` is
sharp up to logarithms on this exact unsigned object.

## Registry and claim firewall

```text
TPC241_MAXIMUM_CLAIM = FIXED_PROFILE_UNSIGNED_TOP_PRIME_Q_COLLAPSED_COLLISION_AND_FINITE_WINDOW_LIMINF
TPC241_ROUTE_ADVANCE = YES_OBSTRUCTION
TPC241_FROZEN_COMMON_PROFILE = REQUIRED_FIXED_NONNEGATIVE_NORMALIZED_C_INFINITY
TPC241_TOP_PRIME_ROW_MASS = PROVED_UNIFORM_THREE_OVER_TWO
TPC241_PRIMITIVE_RESIDUE_CAUCHY = PROVED_EXACT
TPC241_COEFFICIENT_LIMINF = PROVED_10773_LOG_2_OVER_1600
TPC241_FINITE_WINDOW_LIMINF = PROVED_10773_LOG_2_OVER_3200
TPC241_NORMALIZED_FIXED_POWER = PROVED_1_OVER_48_SHARP_UP_TO_LOGARITHMS
TPC241_UNSIGNED_FIXED_POWER_IMPROVEMENT = REFUTED_ON_EXACT_FIXED_PROFILE_COMMON_SOURCE_KERNEL
TPC241_FULL_VECTOR_FRAME_BEFORE_TOP_PRIME_RESTRICTION = REQUIRED_EXACT
TPC241_CLASS_UNIFORM_PROFILE_THRESHOLD = NOT_CLAIMED
TPC241_PLATEAU_PROFILE_SUBSTITUTION = FORBIDDEN
TPC241_C_H_SIGNED_CANCELLATION = NONE
TPC241_SIGNED_FOUR_PACKET_GATE_B_SCALAR = OPEN
TPC241_ARITHMETIC_ADVANCE = NO
TPC241_FIXED_ATOM_CREDIT = 0
TPC241_L2 = NONE
TPC241_FULL_GATE_B = OPEN
TPC241_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC241_TWIN_PRIME_RESULT = NONE
TPC241_STATUS = PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_COLLISION_SHARPNESS
TPC241_ROUND2_CLUE = FORCE_THE_NEXT_ARGUMENT_TO_RETAIN_FOUR_PACKET_POLARIZATION_OR_C_H_SIGNS_BEFORE_SQUARING_BECAUSE_THE_UNSIGNED_TOP_PRIME_COLLISION_CHANNEL_IS_FIXED_POWER_SHARP
```

The theorem is lower-bound information for the q-collapsed unsigned
common-profile kernel.  It does not say that the signed four-packet scalar is
large, small, or noncancelling.  `ARITHMETIC_ADVANCE = NO` retains its strict
program meaning: no signed arithmetic `L2` estimate has been proved.

## 1. Frozen full kernel and top-prime subenergy

Keep

```text
H=x^(21/32),  Q=x^(1/3),  U=x^(133/400),
Q_x={q prime: Q<q<=2Q},
D_x={d: H/(4Q)<d<=U, mu(d)^2=1},
C_h=sum_(d in D_x,h|d) mu(d)log(d)/d.
```

Fix, independently of `x`, a real profile

```text
psi in C_c^infinity(R),
0<=psi<=1,
support(psi) subset [-1,1],
integral psi=1.
```

Define

```text
B_(h,q)^psi(a)
 = sum_(0<|m|<=floor(hq/H))
     psi(Hm/(hq)) 1_(m q^(-1)=a mod h),

K_psi(n)
 = sum_(h<=U) sum_((a,h)=1)
     C_h (sum_(q in Q_x)B_(h,q)^psi(a)) e(na/h).    (1.1)
```

The frequency vector in (1.1) is indexed by distinct primitive fractions.
For top primes `U/2<p<=U`, TPC-215 gives `C_p=-log(p)/p`.  Put

```text
B_p^psi(a)=sum_(q in Q_x)B_(p,q)^psi(a),
S_p=sum_((a,p)=1)B_p^psi(a),
E_top^psi=sum_(U/2<p<=U)|C_p|^2
            sum_((a,p)=1)|B_p^psi(a)|^2.           (1.2)
```

## 2. Uniform first moment and residue collision

Eventually `p<q`, `4Q<H`, and every admissible nonzero multiplier has
`|m|<p/2`.  It therefore maps to a primitive residue modulo `p`.  Summing over
all primitive residues counts every multiplier, whether or not different q
rows collide:

```text
S_p
 = sum_(q in Q_x)
   sum_(0<|m|<=floor(pq/H)) psi(Hm/(pq)).            (2.1)
```

For `T=pq/H`, the fixed-profile first-moment lattice sum is

```text
sum_(0<|m|<=floor(T))psi(m/T)=T+O_psi(1).           (2.2)
```

The integral over both signs is already one; no extra factor two occurs.
The estimate is uniform on the top shells because
`T>=(1/2)x^(23/2400)`.  Hence

```text
S_p
 = (p/H)sum_(Q<q<=2Q)q+O_psi(#Q_x)
 = (3/2+o_psi(1))pQ^2/(H log Q),                   (2.3)
```

uniformly for prime `U/2<p<=U`.  The relative lattice error is
`O_psi(H/(pQ))=O_psi(x^(-23/2400))`.

There are exactly `p-1` primitive residues.  Cauchy gives the literal
q-collision lower bound

```text
sum_((a,p)=1)|B_p^psi(a)|^2 >= S_p^2/(p-1).        (2.4)
```

Unlike TPC-240, equation (2.4) acts after q labels have been collapsed.  This
is the new collision edge.

## 3. Weighted top-prime coefficient liminf

Insert (2.3) into (2.4), multiply by
`|C_p|^2=(log p)^2/p^2`, and sum over top primes.  The weighted PNT formula

```text
sum_(U/2<p<=U)(log p)^2/p=(log 2+o(1))log U
```

gives

```text
E_top^psi
 >= (9log(2)/4+o_psi(1))
    (Q^4/H^2) log U/(log Q)^2.                      (3.1)
```

Now

```text
log U/log Q=399/400,
1/log Q=3/log x,
(9/4)(399/400)3=10773/1600,
Q^4/H^2=x^(1/48).
```

The unambiguous theorem statement is

```text
liminf_(x->infinity)
 [(log x)/x^(1/48)] E_top^psi
 >= 10773 log(2)/1600.                              (3.2)
```

The quantifier is profilewise.  No threshold uniform over the entire profile
class is asserted.

## 4. Legal finite-window transfer

Let `I_x=(x/2,x] intersect Z` and `N=#I_x`.  First apply the TPC-238 lower
frame to the complete coefficient vector from (1.1):

```text
N^(-1)sum_(n in I_x)|K_psi(n)|^2
 >= [1/2-pi^2 U^4/(6N^2)]_+
    sum_(h,a)|C_h sum_q B_(h,q)^psi(a)|^2.          (4.1)
```

Only after (4.1) is established may its nonnegative coefficient norm be
restricted to top primes.  No physical-window cross term is deleted.  Since
`U^4/N^2=x^(-67/100+o(1))`, equation (3.2) yields

```text
liminf_(x->infinity)
 [(log x)/x^(1/48)]
 [N^(-1)sum_(n in I_x)|K_psi(n)|^2]
 >= 10773 log(2)/3200.                              (4.2)
```

## 5. Fixed-power sharpness and route closure

For every fixed admissible `psi`, fixed `delta>0`, and fixed real `A`, the
lower bound (4.2) rules out an eventual estimate

```text
N^(-1)sum_(n in I_x)|K_psi(n)|^2
 <= C_(psi,delta,A)x^(1/48-delta)(log x)^A,         (5.1)
```

because the ratio of the lower scale to the right-hand scale is
`x^delta/(log x)^(A+1)`, which tends to infinity.  Thus the TPC-239
fixed-power exponent `1/48` is sharp up to logarithms on every fixed
admissible unsigned common-profile kernel.

This is a structural obstruction, not Gate-B completion.  Taking absolute
squares erases the top-prime Möbius sign, and the proof has no four-packet
polarization.  The unsigned uniform-envelope lane is now structurally closed:
any next power-saving argument must retain a sign-sensitive or
polarization-sensitive object before squaring.

```text
STRONGEST_POSITIVE_RESULT = SOURCE_LOCKED_X_1_OVER_48_OVER_LOG_X_COEFFICIENT_AND_FINITE_WINDOW_LIMINF
STRONGEST_OBSTRUCTION = THE_UNSIGNED_FIXED_PROFILE_COMMON_SOURCE_KERNEL_ATTAINS_FIXED_POWER_1_OVER_48_UP_TO_LOGARITHMS
OPEN_THEOREM = WHETHER_THE_LITERAL_SIGNED_FOUR_PACKET_PROJECTION_CANCELS_OR_ANNIHILATES_THE_TOP_PRIME_COLLISION_MODE_BEFORE_ABSOLUTE_SQUARES
REUSABLE_STRUCTURE = NORMALIZED_NONNEGATIVE_PROFILE_FIRST_MOMENT_PLUS_PRIMITIVE_RESIDUE_CAUCHY_PLUS_WEIGHTED_PNT_PLUS_FINITE_WINDOW_LOWER_FRAME
ROUND2_CLUE = FORCE_THE_NEXT_ARGUMENT_TO_RETAIN_FOUR_PACKET_POLARIZATION_OR_C_H_SIGNS_BEFORE_SQUARING_BECAUSE_THE_UNSIGNED_TOP_PRIME_COLLISION_CHANNEL_IS_FIXED_POWER_SHARP
```

No signed `C_h` cancellation, signed four-packet theorem, arithmetic `L2`,
fixed-atom credit, strict `1/400` payment, full Gate B, or twin-prime theorem
is claimed.
