# Bridge B / Gate B TPC-244: common-multiplier sign localization

Date: 2026-08-25

Status: `PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION`.

TPC-243 proved that a supplied coefficient covariance is transported to the
hard physical window with relative error
`epsilon=x^(-67/200+o(1))`.  TPC-244 answers the next source question: if the
same literal clustered multiplier `C_h` is placed on both polarized lanes, can
its aggregate outer sign drive the selected same-bucket covariance?

## Registry and claim firewall

```text
TPC244_MAXIMUM_CLAIM = EXACT_COMMON_MULTIPLIER_PHASE_BLINDNESS_SIGN_CUT_LOCALIZATION_AND_HARD_WINDOW_LEAKAGE
TPC244_ROUTE_ADVANCE = YES_STRUCTURAL_OBSTRUCTION
TPC244_COMMON_MULTIPLIER_COVARIANCE = PROVED_SUM_ABS_C_H_SQUARED_LOCAL_COVARIANCE
TPC244_COMMON_UNIT_PHASE_INVARIANCE = PROVED_EXACT_COVARIANCE_AND_BOTH_NORMS
TPC244_INTERNAL_MOBIUS_CANCELLATION = PRESERVED_NOT_ESTIMATED
TPC244_NONORTHOGONAL_SIGN_CUT = PROVED_EXACT
TPC244_ALL_SIGN_INVARIANCE = PROVED_IFF_EVERY_SYMMETRIZED_EDGE_ZERO
TPC244_COMPLEX_MULTIPLIER_EDGE = PROVED_WITH_CONJUGATED_CROSS_FACTORS
TPC244_HARD_WINDOW_PAIRWISE_VARIATION = PROVED_AT_MOST_TWO_EPSILON_COEFFICIENT_NORM_PRODUCT
TPC244_V59_SPECIALIZATION = CONDITIONAL_ON_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT
TPC244_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT = OPEN
TPC244_COEFFICIENT_NORM_PAYMENT = OPEN
TPC244_SIGNED_C_H_CANCELLATION = NONE
TPC244_ARITHMETIC_ADVANCE = NO
TPC244_FIXED_ATOM_CREDIT = 0
TPC244_L2 = NONE
TPC244_FULL_GATE_B = OPEN
TPC244_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC244_TWIN_PRIME_RESULT = NONE
TPC244_TPC_TRIGGER = true
TPC244_NUMBERED_RELEASE = YES
TPC244_STATUS = PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION
TPC244_ROUND2_CLUE = WITHIN_BLOCK_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISK_BEFORE_ANY_OUTER_SIGN_ARGUMENT
```

The theorem is structural.  It does not prove a literal V59 two-lane
attachment, a signed `C_h` cancellation estimate, or an arithmetic advance.

## Frozen source interface

Keep the literal V59 scales and cluster tail

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
C_h=sum_(d in D_x,h|d) mu(d)log(d)/d.
```

TPC-214 proves exact reduced-frequency clustering and displays `|C_h|^2` in
the complete-period unsigned energy.  TPC-237 retains primitive rational
frequencies exactly once and keeps the same outer `C_h` in every frozen packet.
TPC-228 explicitly leaves open the literal map from the V59 `beta,w` sequences
to two primitive coefficient lanes.

Accordingly, the coefficient-space theorem below is unconditional, while its
literal V59 interpretation is conditional on the missing attachment.

## Orthogonal common-multiplier theorem

Let

```text
H_coeff=direct_sum_(h in A) H_h,
B=direct_sum_h C_h b_h,
W=direct_sum_h C_h w_h.
```

The inner product is conjugate-linear in the first slot.  Orthogonality gives

```text
<W,B>=sum_h conjugate(C_h)C_h<w_h,b_h>
     =sum_h |C_h|^2<w_h,b_h>,

||B||^2=sum_h |C_h|^2||b_h||^2,
||W||^2=sum_h |C_h|^2||w_h||^2.
```

Thus any simultaneous blockwise replacement

```text
C_h -> eta_h C_h, |eta_h|=1,
```

leaves covariance and both norms exactly invariant.  Real sign flips are a
special case.

This statement erases only an **aggregate outer phase** after `C_h` has been
formed.  The internal Möbius signs in

```text
C_h=sum_(h|d)mu(d)log(d)/d
```

still change `|C_h|`; no internal arithmetic cancellation is removed or
estimated.  If the two lanes have different multipliers, the local factor is
`conjugate(C_h^(W))C_h^(B)` and can retain phase.

## Nonorthogonal sign-cut theorem

Let `J_h:H_h->K` be arbitrary linear maps into one common Hilbert space.  For
real `C_h` and signs `s_h`, define

```text
W(s)=sum_h s_h C_h J_h w_h,
B(s)=sum_h s_h C_h J_h b_h,
Q(s)=<W(s),B(s)>.
```

With

```text
M_hk=<J_h w_h,J_k b_k>,
D=sum_h C_h^2 M_hh,
S_hk=C_hC_k(M_hk+M_kh), h<k,
```

finite expansion gives

```text
Q(s)=D+sum_(h<k)s_hs_k S_hk,
Q(s)-Q(1)=-2sum_(h<k,s_h!=s_k)S_hk.
```

The functions `s_hs_k` are distinct Walsh characters.  Hence

```text
Q(s) is invariant for every sign pattern
iff
S_hk=0 for every unordered pair.
```

Each `S_hk` may be complex.  Its vanishing requires only cancellation of the
two directed terms in the symmetrized edge, not their separate vanishing.  For
complex baseline multipliers the correct edge is

```text
conjugate(C_h)C_k M_hk + conjugate(C_k)C_h M_kh.
```

## TPC-243 hard-window transfer

Assume the direct-sum coefficient lanes are supplied on one finite separated
frequency set and enter the same TPC-243 synthesis map `T`.  Write

```text
Q_I(eta)=N^(-1)<T W(eta),T B(eta)>.
```

The selected orientation agrees with TPC-242:

```text
X=N^(-1/2)TB, Y=N^(-1/2)TW,
F_1=<Y,X>=Q_I.
```

TPC-243 gives

```text
|Q_I(eta)-<W(eta),B(eta)>|
 <=epsilon||W||||B||.
```

The coefficient covariance and norms are common to every unit-phase pattern,
so two applications and the triangle inequality prove

```text
|Q_I(eta)-Q_I(xi)|<=2epsilon||W||||B||.
```

For primitive V59 height,

```text
epsilon=(133/100+o(1))x^(-67/200)log x
       =x^(-67/200+o(1)).
```

The norms are coefficient-space norms.  Without the missing literal two-lane
attachment and a payable bound for their product, this decay cannot be promoted
to an arithmetic saving.

## Exact certificates

The canonical certificate contains:

- an orthogonal three-block fixture checking all eight common sign patterns;
- a nonorthogonal two-dimensional fixture with
  `D=-12`, `S_5,7=-12`, `S_5,35=20`, and `S_7,35=-15`;
- an exact quarter-frequency hard-window fixture checking all eight patterns
  and all 64 ordered sign-pattern pairs.

The independent checker reimplements all Gaussian-rational arithmetic and
source hashing without importing the producer.  The stress census verifies
`104976` common-sign direct-sum covariances and `216` sign-cut identities.  All
finite records are `NUMERICAL_FINITE_ILLUSTRATION_ONLY`.

## Route-B evaluation

```text
STRONGEST_POSITIVE_RESULT = COMMON_OUTER_PHASE_INVISIBLE_AND_ALL_NONORTHOGONAL_SIGN_SENSITIVITY_LOCALIZED_TO_CUT_EDGES
STRONGEST_OBSTRUCTION = OUTER_C_H_SIGN_CANNOT_CONTROL_SAME_BLOCK_MAIN_COVARIANCE
OPEN_THEOREM = LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT_WITH_PAYABLE_NORMS
REUSABLE_STRUCTURE = COMMON_MULTIPLIER_DIAGONAL_TO_SIGN_CUT_TO_HARD_WINDOW_LEAKAGE
ROUND2_CLUE = DECOMPOSE_WITHIN_BLOCK_COVARIANCE_INTO_LONGITUDINAL_AND_TRANSVERSE_PARTS
```

The next paper should analyze the exact feasible set of the local covariance
`<w_h,b_h>` from longitudinal moments and transverse energies.  This follows
the obstruction rather than attempting to reuse an outer sign already proved
invisible.
