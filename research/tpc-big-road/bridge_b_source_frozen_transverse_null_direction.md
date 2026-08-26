# Bridge B V111: source-frozen transverse null direction

Date: 2026-08-26

Status: `PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_FOR_LITERAL_V59_ADJOINT`

TPC-258 is the minimal continuation of TPC-257.  It keeps the literal V59
clock and four-block frame, and chooses a direction from the two explicit
curvature constants before inspecting any coefficient.

```text
L1=log(3456/3125), L2=log(884736/823543),
LT=sqrt(L1^2+L2^2),
z_null=(L2 z1-L1 z2)/LT.
```

Because `kappa1=L1/2` and `kappa2=L2/2`, the TPC-257 leading vector obeys

```text
L2*kappa1-L1*kappa2=0.
```

The exact orthonormality of `z1,z2` then gives `||z_null||=1` and
`z_null` in `z0`-perp.  Linearity applied to the two TPC-257 scalar
asymptotics yields

```text
<z_null,A_x beta>=o(x^(7/6)/log^3(x)).
```

The TPC-255 bounded-variation compiler remains intact: output and input unit
masks, deleted diagonal, hard-window leakage, child-jump leakage, and the
complex kernel are not discarded.  The inherited boundary contribution is
`O_(psi,epsilon)(x^(55/48+epsilon))`, which is lower than the diagonal scale
for fixed `epsilon<1/48`.

If an explicit `O(1/log x)` rate is supplied for both inherited scalar
remainders, the same algebra gives the conditional refinement

```text
|<z_null,A_x beta>|
 << S_x/log x+x^(55/48+epsilon),
 S_x=x^(7/6)/log^3(x).
```

The released unconditional result is deliberately only `o(S_x)`.  A formal
`1/sqrt(log x)` error sequence shows why this does not imply any fixed-power
saving.  Thus this bridge is a finite projected cancellation theorem, not an
arithmetic `L2` upper bound or a full Gate-B payment.

```text
TPC258_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_FOR_LITERAL_V59_ADJOINT
TPC258_ROUTE_ADVANCE = YES_SCOPED_TRANSVERSE_NULL
TPC258_ARITHMETIC_ADVANCE = YES_SCOPED_LOG_CANCELLATION
TPC258_NULL_DIRECTION = PROVED_SOURCE_FROZEN_UNIT_VECTOR
TPC258_LEADING_DIAGONAL_CANCELLATION = PROVED_SOURCE_BACKED
TPC258_RATE_REFINEMENT = CONDITIONAL_THEOREM_LOG_ONE_OVER_X
TPC258_FIXED_POWER_SAVING = NONE
TPC258_L2 = NONE
TPC258_FIXED_ATOM_CREDIT = 0
TPC258_FULL_GATE_B = OPEN
TPC258_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC258_TWIN_PRIME_RESULT = NONE
TPC258_STATUS = PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_FOR_LITERAL_V59_ADJOINT
```

Strongest positive result: the known transverse diagonal has a canonical
source-frozen null direction.  Strongest obstruction: without an explicit
rate, the cancellation is only `o(1)`, not a power saving.  Open theorem:
couple this direction to the signed `w` lane and control the remaining output.
