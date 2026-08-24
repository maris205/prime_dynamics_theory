# Bridge B V90: collision-compressed finite-window reassembly

Date: 2026-08-24

Status: `PROVED_STRUCTURAL_L1 / COMMON_SOURCE_PACKET_TRACE`.

TPC-237 composes two previously separate structural edges on the exact
TPC-218 common-source kernel.  TPC-236 first compresses the prime-shell label
inside each primitive physical frequency bucket.  TPC-217 then attaches the
resulting reduced-frequency coefficients to a finite integer window.  The
order matters: it replaces the coarse prime-shell collapse factor
`P=#Q_x` by the physical collision factor before the additive large sieve is
used.

## Registry and claim firewall

```text
TPC237_MAXIMUM_CLAIM = COLLISION_COMPRESSED_FINITE_WINDOW_COMMON_SOURCE_PACKET_TRACE_AT_X_1_OVER_48
TPC237_ROUTE_ADVANCE = YES
TPC237_PRIMITIVE_FREQUENCY_INDEX = REQUIRED_EXACT
TPC237_Q_COLLISION_BEFORE_LARGE_SIEVE = PROVED_EXACT_COMPOSITION
TPC237_PRIMITIVE_BUCKET_FACTOR = PROVED_LE_4Q_SQUARED_OVER_H_PLUS_4UQ_OVER_H
TPC237_FINITE_WINDOW_PACKET_TRACE = PROVED_STRUCTURAL
TPC237_NORMALIZED_MAIN_EXPONENT = PROVED_1_OVER_48
TPC237_NORMALIZED_SECONDARY_EXPONENT = PROVED_1_OVER_50
TPC237_UNNORMALIZED_MAIN_EXPONENT = PROVED_49_OVER_48
TPC237_WINDOW_FACTOR = PROVED_1_PLUS_U_SQUARED_OVER_N
TPC237_OLD_P_COLLAPSE = REPLACED_BY_PHYSICAL_COLLISION_FACTOR
TPC237_SIMULTANEOUS_SATURATION = NOT_CLAIMED
TPC237_C_H_SIGNED_CANCELLATION = NONE
TPC237_SIGNED_FOUR_PACKET_GATE_B_SCALAR = OPEN
TPC237_ARITHMETIC_ADVANCE = NO
TPC237_FIXED_ATOM_CREDIT = 0
TPC237_L2 = NONE
TPC237_FULL_GATE_B = OPEN
TPC237_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC237_STATUS = PROVED_STRUCTURAL_L1
TPC237_ROUND2_CLUE = TEST_THE_ACTUAL_WEIGHTED_COLLISION_ENERGY_BEFORE_SEEKING_CROSS_H_SIGN_CANCELLATION
```

The packet trace below is unsigned.  It is not the signed four-packet Gate-B
scalar, and the literal signs in `C_h` are retained but not exploited.

## 1. Frozen common-source object

Keep the V59 scales

```text
H=x^(21/32),  Q=x^(1/3),  U=x^(133/400),
Q_x={q prime:Q<q<=2Q},
D_x={d:H/(4Q)<d<=U, mu(d)^2=1},
C_h=sum_(d in D_x,h|d) mu(d)log(d)/d.
```

For a fixed finite number `J` of profiles with
`M=max_j ||psi_j||_infty`, define

```text
B_(h,q)^(j)(a)
 = sum_(0<|m|<=floor(hq/H))
     psi_j(Hm/(hq)) 1_(m q^(-1)=a mod h),

K_j(n)
 = sum_(h<=U) sum_(a mod h,(a,h)=1)
     C_h (sum_(q in Q_x) B_(h,q)^(j)(a)) e(na/h).
```

The outer `q` weight is one.  No row-dependent normalization or
packet-dependent transform is inserted.  The large-sieve index is explicitly
the primitive pair `(h,a)`; passing unreduced residues directly to that step
would duplicate frequencies and is forbidden.

## 2. Prime-shell collision compression

For sufficiently large `x`, `4Q<H` and `U<Q`.  TPC-236 gives, for a fixed
residue, the row-incidence bound

```text
R_h(a) <= 4Q^2/H + 4hQ/(gH),  g=(a,h).
```

The physical frequency sum retains only `(a,h)=1`, so `g=1`.  Hence

```text
R_h(a) <= 4Q^2/H+4hQ/H
       <= 4Q^2/H+4UQ/H =: R_*.
```

Coordinatewise Cauchy, followed by summation in `h,a,j`, yields

```text
sum_(h,a,j) |C_h|^2 |sum_q B_(h,q)^(j)(a)|^2
 <= R_* sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2.       (2.1)
```

TPC-218 supplies the source-matched direct coefficient-energy estimate

```text
sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2
 << J M^2 (Q^2/H)(log x)^5.                         (2.2)
```

Indeed, fixed-`q` injectivity gives row energy at most
`2M^2 hq/H`, while the active-denominator harmonic estimate is
`sum_h h|C_h|^2 << (log x)^5`.  Equation (2.1) is the new placement of
the TPC-236 theorem: the old scalar recovery used an additional coarse
factor `P`, whereas (2.1) uses the physical bucket multiplicity.

## 3. Reduced-frequency finite-window attachment

Distinct primitive fractions `a/h` with `h<=U` have circular spacing at
least `U^(-2)`.  For any consecutive interval `I` of `N` integers, the
standard additive large sieve therefore gives

```text
sum_(n in I) sum_j |K_j(n)|^2
 <= (N-1+U^2)
    sum_(h,a,j) |C_h|^2 |sum_q B_(h,q)^(j)(a)|^2.    (3.1)
```

Combining (2.1), (2.2), and (3.1),

```text
N^(-1) sum_(n in I) sum_j |K_j(n)|^2
 << J M^2 (1+U^2/N)
    [(Q^2/H)^2 + (UQ/H)(Q^2/H)] (log x)^5.           (3.2)
```

For `I=I_x=(x/2,x] intersect Z`, `N` is comparable to `x`, and

```text
Q^2/H=x^(1/96),
UQ/H=x^(23/2400),
(Q^2/H)^2=x^(1/48),
(UQ/H)(Q^2/H)=x^(1/50),
U^2/N=x^(-67/200+o(1)).
```

Thus

```text
N^(-1) sum_(n in I_x) sum_j |K_j(n)|^2
 << J M^2 [x^(1/48)+x^(1/50)](log x)^5
 << J M^2 x^(1/48)(log x)^5.                         (3.3)
```

The leading unnormalized exponent is `49/48+o(1)`.  No simultaneous
saturation statement is made: sequentially composing valid upper bounds does
not prove that one physical source saturates both.

## 4. What the theorem does not do

The exact signed coefficients `C_h` enter (3.1), but the proof then uses
`|C_h|^2` and an absolute harmonic majorant.  Likewise, summing the positive
packet energies is not the signed four-phase polarization needed by the
terminal Gate-B scalar.  Consequently no Möbius cancellation, prime-shell
signed cancellation, fixed-atom credit, arithmetic `L2`, strict `1/400`
payment, full Gate B, or twin-prime conclusion is claimed.

The strongest positive result is the normalized `x^(1/48)+x^(1/50)`
finite-window packet-trace envelope.  The strongest obstruction is that every
step is unsigned, so the theorem neither uses `C_h` signs nor proves the
exponent sharp.  The next theorem should test the literal weighted collision
energy

```text
sum_(h,j) sum_((a,h)=1) |C_h|^2 |sum_q B_(h,q)^(j)(a)|^2
```

against the uniform `R_*` product before attempting a cross-`h` signed
promotion.

```text
STRONGEST_POSITIVE_RESULT = FINITE_WINDOW_COMMON_SOURCE_PACKET_TRACE_AT_X_1_OVER_48_PLUS_X_1_OVER_50
STRONGEST_OBSTRUCTION = THE_COMPOSITION_IS_UNSIGNED_AND_PROVES_NO_SIMULTANEOUS_SATURATION_OR_C_H_CANCELLATION
OPEN_THEOREM = ACTUAL_WEIGHTED_COLLISION_ENERGY_BEYOND_THE_UNIFORM_R_STAR_PRODUCT
REUSABLE_STRUCTURE = PRIMITIVE_BUCKET_COLLISION_COMPRESSION_BEFORE_REDUCED_FREQUENCY_LARGE_SIEVE
ROUND2_CLUE = TEST_THE_ACTUAL_WEIGHTED_COLLISION_ENERGY_BEFORE_SEEKING_CROSS_H_SIGN_CANCELLATION
```
