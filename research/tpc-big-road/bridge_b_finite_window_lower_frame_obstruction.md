# Bridge B V91: finite-window lower-frame obstruction

Date: 2026-08-24

Status: `PROVED_STRUCTURAL_OBSTRUCTION_L1 / CROSS_REDUCED_FREQUENCY_CANCELLATION_EXCLUDED`.

TPC-238 reverses the finite-window question left by TPC-237.  Instead of asking
for another upper bound, it proves that the synthesis map on distinct primitive
rational frequencies has a positive lower frame bound on a long consecutive
window.  Consequently, after the prime-shell label has been collapsed into one
coefficient at each reduced frequency, interference among different reduced
frequencies cannot be the source of a fixed-power saving.

## Registry and claim firewall

```text
TPC238_MAXIMUM_CLAIM = FINITE_WINDOW_LOWER_FRAME_OBSTRUCTION_AFTER_Q_COLLAPSE
TPC238_ROUTE_ADVANCE = YES
TPC238_TRIANGULAR_WINDOW_LOWER_FRAME = PROVED_EXACT
TPC238_PRIMITIVE_FAREY_SPACING = PROVED_U_TO_MINUS_2
TPC238_FEJER_OFFDIAGONAL = PROVED_LE_1_OVER_4L_DISTANCE_SQUARED
TPC238_CIRCULAR_PACKING_ROW_SUM = PROVED_LE_PI_SQUARED_U_FOUR_OVER_3
TPC238_LOWER_FRAME = PROVED_L_MINUS_PI_SQUARED_U_FOUR_OVER_12L_POSITIVE_PART
TPC238_NORMALIZED_LOWER_FRAME = PROVED_HALF_MINUS_PI_SQUARED_U_FOUR_OVER_6N_SQUARED_POSITIVE_PART
TPC238_V59_FRAME_DEFECT = PROVED_X_MINUS_67_OVER_100
TPC238_CROSS_REDUCED_FREQUENCY_FIXED_POWER_SAVING = REFUTED_SCOPED_AFTER_Q_COLLAPSE
TPC238_WITHIN_Q_BUCKET_CANCELLATION = OPEN
TPC238_C_H_SIGNED_CANCELLATION = NONE
TPC238_SIGNED_FOUR_PACKET_GATE_B_SCALAR = OPEN
TPC238_SHARPNESS = NOT_CLAIMED
TPC238_ARITHMETIC_ADVANCE = NO
TPC238_FIXED_ATOM_CREDIT = 0
TPC238_L2 = NONE
TPC238_FULL_GATE_B = OPEN
TPC238_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC238_STATUS = PROVED_STRUCTURAL_OBSTRUCTION_L1
TPC238_ROUND2_CLUE = MOVE_THE_POWER_SAVING_SEARCH_INSIDE_THE_LITERAL_C_H_WEIGHTED_Q_COLLISION_BUCKETS
```

The theorem starts only after the `q` rows have been collapsed into coefficients
at distinct primitive frequencies.  It does not estimate those coefficients and
therefore does not exclude cancellation inside a single `q` bucket.

## 1. Frozen reduced-frequency synthesis

Let `I` be any interval of `N>=1` consecutive integers and set

```text
L=floor((N+1)/2).
```

For a finite coefficient family indexed by distinct primitive fractions modulo
one,

```text
F_U={(h,a):1<=h<=U, 0<=a<h, (a,h)=1},
S_z(n)=sum_((h,a) in F_U) z_(h,a) e(na/h),
E_I(z)=sum_(n in I)|S_z(n)|^2,
```

the claim concerns the map `z -> (S_z(n))_(n in I)`.  In the TPC-237
application one may substitute

```text
z_(h,a)^(j)=C_h sum_(q in Q_x) B_(h,q)^(j)(a),
```

but the lower-frame theorem itself is independent of that arithmetic formula.

## 2. Triangular minorant and Fejer matrix

Because `2L-1<=N`, a translated triangular weight

```text
w(c+k)=1-|k|/L  for |k|<L,
w(n)=0 otherwise
```

fits inside `I` and satisfies `0<=w<=1`.  Its Fourier transform is the Fejer
kernel

```text
F_L(theta)
 = sum_(|k|<L)(1-|k|/L)e(k theta)
 = L^(-1)|sum_(r=0)^(L-1)e(r theta)|^2.
```

Thus `F_L(0)=L`, and expansion of the weighted energy gives a Hermitian Gram
form with diagonal `L`.  Off the diagonal,

```text
F_L(theta)
 = sin^2(pi L theta)/(L sin^2(pi theta))
 <= 1/(4L ||theta||^2),
```

using `|sin(pi theta)|>=2||theta||` for circular distance
`||theta||<=1/2`.

## 3. Primitive spacing and inverse-square packing

Distinct reduced fractions `a/h` and `a'/h'` with `h,h'<=U` satisfy

```text
||a/h-a'/h'|| >= 1/(hh') >= U^(-2)=:delta.
```

Around any selected point of a circular `delta`-packing, the `k`-th point in
either direction is at distance at least `k delta`.  Therefore each row obeys

```text
sum_(beta!=alpha) ||alpha-beta||^(-2)
 <= 2 delta^(-2) sum_(k>=1) k^(-2)
 = pi^2/(3 delta^2)
 <= pi^2 U^4/3.                                      (3.1)
```

Combining the Fejer estimate with (3.1), the absolute off-diagonal row sum is
at most

```text
pi^2 U^4/(12L).
```

Schur's test, equivalently the Hermitian Gershgorin bound, then gives the lower
frame theorem

```text
E_I(z)
 >= [L-pi^2 U^4/(12L)]_+ sum_((h,a) in F_U)|z_(h,a)|^2.       (3.2)
```

The positive part is included because energy is nonnegative.  Since `L>=N/2`,
division by `N` yields the simpler exact consequence

```text
E_I(z)/N
 >= [1/2-pi^2 U^4/(6N^2)]_+ sum_((h,a) in F_U)|z_(h,a)|^2.   (3.3)
```

No optimality of either numerical constant is claimed.

## 4. V59 obstruction

On the TPC-237 window `I_x=(x/2,x] intersect Z`, one has `N~x` and
`U=x^(133/400)`.  Hence

```text
U^4/N^2=x^(4*133/400-2+o(1))=x^(-67/100+o(1)),
```

so (3.3) becomes

```text
E_(I_x)(z)/N >= [1/2-O(x^(-67/100+o(1)))] sum|z|^2.          (4.1)
```

For the collapsed TPC-237 coefficients, (4.1) proves that distinct
reduced-frequency interference preserves a fixed positive proportion of their
coefficient energy.  It therefore refutes, in this precisely scoped post-collapse
model, the idea that cross-frequency signs alone can turn the growing TPC-237
upper envelope into a fixed-power saving.

## 5. What remains open

Equation (4.1) says nothing about the size of

```text
z_(h,a)^(j)=C_h sum_q B_(h,q)^(j)(a).
```

The prime rows sharing one rational frequency have already been merged before
the lower frame acts.  Cancellation among those rows, arithmetic sparsity of
their supports, literal `C_h`-weighted average collision energy, cancellation
inside the construction of `C_h`, and the terminal signed four-packet projection
all remain outside the theorem.  No arithmetic `L2`, fixed-atom credit, strict
`1/400` payment, full Gate B, or twin-prime conclusion follows.

The next admissible target is consequently the same-frequency prime-shell
bucket itself, beginning with the strongest uniform arithmetic count available
for primes in the associated reduced residue class and then testing the literal
`C_h`-weighted energy.

```text
STRONGEST_POSITIVE_RESULT = V59_PRIMITIVE_REDUCED_FREQUENCY_SYNTHESIS_HAS_LOWER_FRAME_ONE_HALF_MINUS_O_ONE
STRONGEST_OBSTRUCTION = CROSS_REDUCED_FREQUENCY_CANCELLATION_CANNOT_SUPPLY_FIXED_POWER_SAVING_AFTER_Q_COLLAPSE
OPEN_THEOREM = LITERAL_C_H_WEIGHTED_SAME_FREQUENCY_Q_COLLISION_ENERGY
REUSABLE_STRUCTURE = TRIANGULAR_WINDOW_FEJER_MINORANT_PLUS_CIRCULAR_INVERSE_SQUARE_PACKING
ROUND2_CLUE = MOVE_THE_POWER_SAVING_SEARCH_INSIDE_THE_LITERAL_C_H_WEIGHTED_Q_COLLISION_BUCKETS
```
