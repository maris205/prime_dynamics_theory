# Bridge B: sharp longitudinal--transverse covariance disks

## 1. Route question

TPC-244 proves that a common block multiplier enters the orthogonal two-lane
covariance through

```text
sum_h |C_h|^2 <w_h,b_h>.
```

The outer sign is therefore unavailable in the same-block main term.  The next
minimal structural question is the exact range of one local covariance after
fixing a longitudinal direction, its two moments, and the two transverse
energies.

This bridge answers that abstract Hilbert-space question completely.  It does
not attach the abstract data to the literal V59 source.

## 2. Exact object and orientation

Let `H` be a complex Hilbert space with inner product conjugate-linear in the
first slot.  Fix a unit vector `u`, put `K=u^perp`, and define

```text
b=<u,B>,
w=<u,W>,
B_perp=B-bu,
W_perp=W-wu,
E_B=||B_perp||^2,
E_W=||W_perp||^2.
```

The exact decomposition is

```text
<W,B>=conjugate(w)b+<W_perp,B_perp>.
```

Thus

```text
c=conjugate(w)b,
r=sqrt(E_B E_W),
|<W_perp,B_perp>|<=r.
```

The center orientation is `conjugate(w)b`; reversing the conjugation contradicts
the repository convention and the TPC-243 selected mode.

## 3. Complete dimension classification

Let `S` be the set of all `<W,B>` at fixed `(b,w,E_B,E_W)`, and let
`m=dim_C(u^perp)`.

### 3.1 At least two transverse directions

If `m>=2`, then

```text
S={z:|z-c|<=r}=c+r Dbar.
```

The inclusion is Cauchy--Schwarz.  For the reverse inclusion, choose
orthonormal `e1,e2` and, for any `|q|<=r`, set

```text
W_perp=sqrt(E_W)e1,
B_perp=sqrt(E_B)[(q/r)e1+sqrt(1-|q|^2/r^2)e2].
```

Then `<W_perp,B_perp>=q`.  The `r=0` branch is the singleton center.

### 3.2 One transverse direction

If `m=1` and `r>0`, fixed nonzero transverse norms force

```text
S={z:|z-c|=r}=c+r T.
```

The disk interior is unavailable.  If `r=0`, the set is `{c}`.

### 3.3 No transverse direction

If `m=0`, then positive transverse energy is unrealizable.  When
`E_B=E_W=0`, the set is `{c}`.

## 4. Exact cancellation and phase geometry

For `m>=2`,

```text
min_(z in S)|z|=max(|c|-r,0),
0 in S iff |c|<=r.
```

For `m=1,r>0`,

```text
min_(z in S)|z|=||c|-r|,
0 in S iff |c|=r.
```

Every realizable branch obeys the universal lower bound

```text
|<W,B>|>=max(|c|-r,0).
```

When `0<=r<|c|`, all feasible covariances lie in the sharp cone

```text
principal_angle(z,c)<=arcsin(r/|c|).
```

The tangent points make the angle sharp for both the disk and the nondegenerate
circle.

## 5. TPC-219 type audit

TPC-219's exact longitudinal object is the constant-prime-label subspace of
`V^P`.  It is generally `dim V` dimensional and is not a committed
one-dimensional unit vector inside a TPC-244 block.  Therefore

```text
TPC245_TPC219_RELATION = PROJECTION_LINEAGE_ONLY_NOT_LITERAL_OBJECT_IDENTITY.
```

Choosing an all-ones coefficient vector or another canonical block direction
would currently be a modeling choice, not a source-backed physical field.

## 6. Physical claim firewall

The theorem is existential over all vectors realizing prescribed abstract
moments and energies.  It does not prove that a physical local covariance can
choose a favorable point of the disk.  It also does not provide the moments or
energies themselves.

The first inherited fatal remains

```text
NO_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_COEFFICIENT_ATTACHMENT.
```

The next TPC-245-specific fatal is

```text
NO_SOURCE_BACKED_CANONICAL_ONE_DIMENSIONAL_U_H_IN_H_H.
```

Accordingly,

```text
TPC245_MAXIMUM_CLAIM = EXACT_DIMENSION_SENSITIVE_LONGITUDINAL_TRANSVERSE_COVARIANCE_FEASIBLE_SET_AND_SHARP_PHASE_SECTOR
TPC245_ROUTE_ADVANCE = YES_STRUCTURAL_CLASSIFICATION
TPC245_EXACT_DECOMPOSITION = PROVED_CENTER_PLUS_TRANSVERSE_COVARIANCE
TPC245_DIM_GE_2_FEASIBLE_SET = PROVED_CLOSED_DISK
TPC245_DIM_EQ_1_FEASIBLE_SET = PROVED_CIRCLE_OR_SINGLETON
TPC245_DIM_EQ_0_FEASIBLE_SET = PROVED_SINGLETON_OR_UNREALIZABLE
TPC245_ZERO_FEASIBILITY = PROVED_DIMENSION_SENSITIVE
TPC245_MINIMUM_MODULUS = PROVED_EXACT
TPC245_PHASE_SECTOR = PROVED_SHARP_WHEN_RADIUS_LT_CENTER
TPC245_TPC219_RELATION = PROJECTION_LINEAGE_ONLY_NOT_LITERAL_OBJECT_IDENTITY
TPC245_CANONICAL_BLOCK_DIRECTION = OPEN
TPC245_LITERAL_V59_TWO_LANE_ATTACHMENT = OPEN
TPC245_PAYABLE_MOMENTS_AND_ENERGIES = OPEN
TPC245_SIGNED_ARITHMETIC_MARGIN = NONE
TPC245_ARITHMETIC_ADVANCE = NO
TPC245_FIXED_ATOM_CREDIT = 0
TPC245_L2 = NONE
TPC245_FULL_GATE_B = OPEN
TPC245_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC245_TWIN_PRIME_RESULT = NONE
TPC245_STATUS = PROVED_STRUCTURAL_L1_SHARP_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISKS
TPC245_ROUND2_CLUE = WEIGHTED_MINKOWSKI_REASSEMBLY_OF_INDEPENDENT_LOCAL_DISKS_WITH_HARD_WINDOW_ERROR
```

## 7. Finite certificate

The exact-rational certificate includes a radius-six disk fixture, a
one-dimensional radius-six circle, zero-radius and zero-dimensional branches,
and a sharp `3--4--5` tangent fixture.  The independent stress census verifies
`15625` ordered pairs in transverse dimension two and `625` in dimension one.
These are finite illustrations only.

## 8. Next theorem

The next minimal structural problem is to reassemble independently realizable
local disks with weights `|C_h|^2`.  Their Minkowski sum should have center
`sum_h |C_h|^2 c_h` and radius `sum_h |C_h|^2 r_h`, with a robust physical
margin only after subtracting the TPC-243 hard-window error.  Literal
independence, source attachment, and arithmetic estimates remain separate open
gates.
