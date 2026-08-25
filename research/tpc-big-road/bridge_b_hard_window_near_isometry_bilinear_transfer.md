# Bridge B V96: hard-window near-isometry and signed bilinear transfer

Date: 2026-08-25

Status: `PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER`.

TPC-243 strengthens the finite-window geometry used by the current Gate-B
route.  TPC-217 supplies the standard upper large sieve, while TPC-238 supplies
a triangular-minorant lower frame with asymptotic baseline `1/2`.  TPC-243
works directly with the hard rectangular window.  An elementary harmonic
circle-packing argument shows that its normalized synthesis map is a
two-sided `1+o(1)` near-isometry and transports signed coefficient inner
products to physical-window inner products with an explicit error.

The theorem is structural.  It does not estimate the literal arithmetic
coefficients and does not attach a top-prime contribution to the V59 packets.

## Registry and claim firewall

```text
TPC243_MAXIMUM_CLAIM = HARD_RECTANGULAR_WINDOW_TWO_SIDED_NEAR_ISOMETRY_AND_SIGNED_BILINEAR_TRANSFER
TPC243_ROUTE_ADVANCE = YES_STRUCTURAL_INTERFACE
TPC243_HARD_WINDOW_DIRICHLET_GRAM = PROVED_EXACT
TPC243_GEOMETRIC_SUM_BOUND = PROVED_ONE_OVER_TWO_CIRCULAR_DISTANCE
TPC243_HARMONIC_CIRCLE_PACKING = PROVED_DELTA_INVERSE_H_K
TPC243_TWO_SIDED_NEAR_ISOMETRY = PROVED_ONE_PLUS_MINUS_EPSILON
TPC243_SIGNED_BILINEAR_TRANSFER = PROVED_WITH_ERROR_EPSILON_NORM_PRODUCT
TPC243_PRIMITIVE_HEIGHT_SPECIALIZATION = PROVED_R_U_EQUALS_U_SQUARED_H_FLOOR_U_SQUARED_OVER_TWO
TPC243_V59_EPSILON = PROVED_133_OVER_100_PLUS_O_ONE_TIMES_X_MINUS_67_OVER_200_LOG_X
TPC243_TPC242_SELECTED_MODE_TRANSFER = PROVED_CONDITIONAL_ON_COEFFICIENT_LANE_ATTACHMENT
TPC243_TPC217_UPPER_SCALE_NOVELTY = NOT_CLAIMED
TPC243_LITERAL_TOP_PRIME_ATTACHMENT = OPEN
TPC243_LITERAL_C_H_SIGNED_CANCELLATION = NONE
TPC243_ARITHMETIC_ADVANCE = NO
TPC243_FIXED_ATOM_CREDIT = 0
TPC243_L2 = NONE
TPC243_FULL_GATE_B = OPEN
TPC243_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC243_TWIN_PRIME_RESULT = NONE
TPC243_STATUS = PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER
TPC243_ROUND2_CLUE = COMMON_MULTIPLIER_SIGN_AUDIT_FOR_LITERAL_C_H_IN_THE_TWO_POLARIZED_LANES
```

## 1. Hard-window synthesis object

Let `F` be a finite subset of `R/Z` separated in circular distance by
`delta`, where `0<delta<=1/2`.  Let

```text
I={M,M+1,...,M+N-1},  N>=1,
e(t)=exp(2 pi i t),
(Tz)(n)=sum_(alpha in F) z_alpha e(n alpha).
```

The coefficient and window inner products are conjugate-linear in the first
slot.  Define

```text
K_delta=floor(1/(2 delta)),
H_K=sum_(j=1)^K 1/j,
R_delta=delta^(-1) H_(K_delta),
epsilon_delta,N=R_delta/N.
```

For the empty set all claims are vacuous.  For a singleton the Gram matrix is
exactly `[N]`; the bounds below remain valid with a nonnegative unused
`R_delta`.

## 2. Dirichlet kernel and harmonic circle packing

For `theta` not an integer, the translated geometric sum satisfies

```text
D_I(theta)=sum_(n in I)e(n theta),
|D_I(theta)|
 <=1/|sin(pi theta)|
 <=1/(2||theta||).                              (2.1)
```

The first inequality follows from the geometric-series formula and the bound
`|1-e(N theta)|<=2`; the second follows from
`sin(pi t)>=2t` on `0<=t<=1/2`.

Fix one `alpha in F`.  Assign every other frequency to a clockwise or
counterclockwise shortest arc from `alpha`, assigning a possible antipodal
tie to one side only.  On either side list the distances increasingly:

```text
d_1<d_2<... .
```

Circular `delta`-separation gives `d_j>=j delta`.  Since every chosen shortest
distance is at most `1/2`, each side has at most
`K_delta=floor(1/(2delta))` entries.  Combining both sides with (2.1) yields

```text
sum_(beta in F, beta!=alpha)|D_I(beta-alpha)|
 <=2 sum_(j=1)^K_delta 1/(2j delta)
 =delta^(-1)H_(K_delta)
 =R_delta.                                      (2.2)
```

The antipodal convention prevents double counting; the right side is allowed
to be nonsharp when only one antipodal point exists.

## 3. Two-sided near-isometry

The coefficient Gram matrix is

```text
G_(alpha,beta)=D_I(beta-alpha),
<Tz,Tw>=<z,Gw>.
```

The orientation `beta-alpha` follows from
`conjugate(z_alpha) w_beta e(n(beta-alpha))`.  Thus `G` is Hermitian and its
diagonal is exactly `N`.  Put `E=G-NI`.  Equation (2.2), Hermitian symmetry,
and the Schur test give

```text
||E||_(2->2)<=R_delta.                           (3.1)
```

Consequently every coefficient vector satisfies

```text
[1-epsilon_delta,N]_+ ||z||_2^2
 <=N^(-1)||Tz||_2^2
 <=(1+epsilon_delta,N)||z||_2^2.                 (3.2)
```

The positive part in the lower bound combines the spectral estimate with the
independent fact `||Tz||^2>=0`; it is relevant only when the elementary error
exceeds one.

This is a direct hard-rectangular statement.  It does not pass through a
triangular weight and therefore has diagonal baseline one rather than one
half.

## 4. Signed bilinear transfer

The same operator bound, without a polarization loss, gives

```text
|N^(-1)<Tz,Tw>-<z,w>|
 =|<z,(G/N-I)w>|
 <=epsilon_delta,N ||z||_2||w||_2.              (4.1)
```

This retains complex phase and orientation.  It is stronger as an interface
than separate energy bounds: once two literal coefficient lanes have been
source-identified, their signed coefficient covariance can be transported to
the physical hard window with no extra square-root or factor-two loss.

It is not an arithmetic cancellation theorem.  If the desired coefficient
inner product is no larger than the error in (4.1), the theorem alone cannot
determine the sign or phase of the physical-window cross term.

## 5. Primitive rational specialization

Distinct reduced fractions of height at most `U` have circular separation at
least `U^(-2)`.  For `U>=2`, take

```text
delta=U^(-2),
K_U=floor(U^2/2),
R_U=U^2 H_(K_U),
epsilon_U,N=U^2 H_(K_U)/N.                      (5.1)
```

Thus (3.2) and (4.1) apply simultaneously to every finite family of distinct
primitive frequencies of height at most `U`.

For the literal V59 scales

```text
I_x=(x/2,x] intersect Z,
N=x/2+O(1),
U=x^(133/400),
```

the harmonic asymptotic gives

```text
H_floor(U^2/2)=2log U+O(1)
              =(133/200)log x+O(1).
```

Since `U^2=x^(133/200)`, equation (5.1) becomes

```text
epsilon_U,N
 =(133/100+o(1))x^(-67/200)log x
 =x^(-67/200+o(1)).                             (5.2)
```

The coefficient `133/100` includes the factor two from
`N=(1/2+o(1))x`; dropping that factor would be a normalization error.

## 6. Transport of the TPC-242 selected mode

Let `z,w` be two coefficient lanes and normalize their physical images by

```text
X=N^(-1/2)Tz,
Y=N^(-1/2)Tw.
```

TPC-242's literal `i^j` phase convention selects

```text
F_1=<Y,X>=N^(-1)<Tw,Tz>.
```

Applying (4.1) with the same orientation gives

```text
|F_1-<w,z>|<=epsilon_U,N ||w||_2||z||_2.         (6.1)
```

Hence a source-backed coefficient-level signed theorem would pass to the
physical window with the explicit vanishing error (5.2).  No such arithmetic
coefficient theorem or literal top-prime attachment is supplied here.

## 7. Comparison with the upstream window theorems

TPC-217 already proves the standard additive large-sieve upper bound
`N-1+U^2`; TPC-243 does not claim that upper scale or the rational spacing as
new.  TPC-238 proves a triangular-minorant lower frame

```text
1/2-O(U^4/N^2).
```

TPC-243 instead proves the direct hard-window two-sided frame

```text
1+O(U^2 log U/N)
```

and the signed bilinear estimate (4.1).  Its error decays more slowly than the
TPC-238 triangular defect, but its diagonal baseline tends to one and it
controls cross covariances, not only energies.  These are distinct advantages;
neither theorem supplies arithmetic cancellation inside the coefficients.

## 8. Route extraction

```text
STRONGEST_POSITIVE_RESULT = HARD_RECTANGULAR_PRIMITIVE_FREQUENCY_SYNTHESIS_IS_A_TWO_SIDED_ONE_PLUS_O_ONE_NEAR_ISOMETRY_AND_TRANSFERS_SIGNED_INNER_PRODUCTS
STRONGEST_OBSTRUCTION = WINDOW_GEOMETRY_ONLY_PRESERVES_THE_COEFFICIENT_COVARIANCE_UP_TO_EPSILON_NORM_PRODUCT_AND_CANNOT_CREATE_ARITHMETIC_CANCELLATION
OPEN_THEOREM = SOURCE_BACKED_LITERAL_TOP_PRIME_TWO_LANE_COEFFICIENT_ATTACHMENT_AND_SIGNED_COVARIANCE_BOUND_BEYOND_THE_WINDOW_ERROR
REUSABLE_STRUCTURE = DIRICHLET_GRAM_PLUS_HARMONIC_CIRCLE_PACKING_PLUS_TPC242_SELECTED_MODE_TRANSPORT
ROUND2_CLUE = COMMON_MULTIPLIER_SIGN_AUDIT_FOR_LITERAL_C_H_IN_THE_TWO_POLARIZED_LANES
```

Route A is not applicable.  Route B advances only at structural L1.  Literal
`C_h` cancellation, arithmetic `L2`, fixed-atom credit, strict `1/400`, full
Gate B, and the twin-prime endpoint remain open.
