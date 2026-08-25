# Bridge B: weighted covariance-disk reassembly

## Frozen theorem

For any nonempty jointly feasible family whose marginals lie in exact local disks,
the weighted aggregate is contained in the disk below.  For the finite complete
Cartesian product of those disks,

```text
S_h=c_h+r_h Dbar
```

and arbitrary complex weights `lambda_h`,

```text
sum_h lambda_h S_h = C+R Dbar,
C=sum_h lambda_h c_h,
R=sum_h |lambda_h|r_h.
```

The reverse inclusion is explicit: for `R>0` and `|d|<=R`, take

```text
e_h=(conjugate(lambda_h)/|lambda_h|)(r_h/R)d
```

when `lambda_h` is nonzero, and zero otherwise.  Then
`sum_h lambda_h e_h=d`.

## Sharp consequences

```text
0 in S iff |C|<=R
min_(Q in S)|Q|=max(|C|-R,0)
phase half-angle=arcsin(R/|C|) when R<|C|.
```

## TPC-244 common-multiplier specialization

For local TPC-245 disks and common lane multipliers `M_h`,

```text
C_0=sum_h |M_h|^2 c_h,
R_0=sum_h |M_h|^2 r_h.
```

This is exact only when each active local feasible set is a full disk and the
joint feasible family is the complete Cartesian product.  Positive-radius one-dimensional
circles are excluded.

## TPC-243 hard-window transfer

Under the literal common synthesis attachment,

```text
E=epsilon||W||||B||,
Q_I in C_0+(R_0+E)Dbar,
|Q_I|>=max(|C_0|-R_0-E,0).
```

Thus `|C_0|>R_0+E` is a conditional robust-nonvanishing criterion.  The
inflated disk is a containing disk; exact physical attainment is not claimed.

## Obstruction

When `|C_0|<=R_0`, the blockwise product full-disk model has an exact zero
realization.  Therefore local longitudinal moments and transverse energies,
without an additional alignment or coupling theorem, cannot prove a uniform
positive aggregate covariance.

## Claim firewall

```text
TPC246_WEIGHTED_DISK_IDENTITY = PROVED_EXACT
TPC246_COUPLED_FAMILY_CONTAINMENT = PROVED
TPC246_REVERSE_REALIZATION = PROVED_EXPLICIT
TPC246_AGGREGATE_ZERO_CRITERION = PROVED_EXACT
TPC246_COMMON_MULTIPLIER_SPECIALIZATION = PROVED_STRUCTURAL
TPC246_HARD_WINDOW_RADIUS_INFLATION = PROVED_CONDITIONAL_ON_ATTACHMENT
TPC246_HARD_WINDOW_IMAGE_EXACTNESS = NOT_CLAIMED
TPC246_POSITIVE_RADIUS_CIRCLE_AS_DISK = FORBIDDEN
TPC246_ARBITRARY_COMPLEX_WEIGHT_AS_COMMON_MULTIPLIER = FORBIDDEN
TPC246_INDEPENDENT_SOURCE_REALIZABILITY = OPEN
TPC246_LITERAL_V59_TWO_LANE_ATTACHMENT = OPEN
TPC246_CANONICAL_BLOCK_DIRECTIONS = OPEN
TPC246_PAYABLE_ARITHMETIC_MARGIN = OPEN
TPC246_ARITHMETIC_ADVANCE = NO
TPC246_FIXED_ATOM_CREDIT = 0
TPC246_L2 = NONE
TPC246_FULL_GATE_B = OPEN
TPC246_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC246_TWIN_PRIME_RESULT = NONE
TPC246_STATUS = PROVED_STRUCTURAL_L1_WEIGHTED_COVARIANCE_DISK_REASSEMBLY
```

## Verdict

`GO` for the finite structural theorem and conditional hard-window criterion.
`STOP_SCOPED` for arithmetic promotion.

## ROUND2_CLUE

`SOURCE_NATIVE_WEIGHTED_LONGITUDINAL_DOMINANCE_BEYOND_TRANSVERSE_RADIUS_AND_WINDOW_LEAKAGE`.
