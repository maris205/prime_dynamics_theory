# Bridge B V116: rank-three physical cross-Gram channel

Date: 2026-08-26

Status: `PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL`

TPC-263 is the direct continuation of TPC-262's literal signed-operator
interface.  It uses the source-only four-block frame from TPC-257 and the
blockwise maximal-interval input from TPC-254 on the same V59 clock.

Let `z0,z1,z2` be the exact orthonormal contrasts and let

```text
P3=sum_(i=0)^2 z_i tensor z_i,
g_x=A_x beta,
C_x=<w,g_x>.
```

The source-backed maximal Type-I `m=1` row controls each of the four
consecutive block sums.  Consequently, for every fixed admissible `K` and
every fixed `M`,

```text
|<z_i,w>| <<_(M,K) x^(1/2)/(log x)^M,  i=0,1,2.
```

TPC-257 supplies the matching adjoint coefficients

```text
<z_i,A_x beta>=-(9/2*kappa_i+o(1))x^(7/6)/(log x)^3.
```

The exact orthogonal decomposition is

```text
C_x=C_3(x)+C_perp(x),
C_3(x)=<P3 w,P3 g_x>
     =sum_(i=0)^2 conjugate(<z_i,w>)<z_i,g_x>,
C_perp(x)=<(I-P3)w,(I-P3)g_x>.
```

Therefore

```text
|C_3(x)|=O_(M,K)(x^(5/3)/(log x)^(M+3)).
```

This is a new physical cross-Gram channel result.  It is logarithmic only:
it supplies no fixed-power credit, and it does not estimate `C_perp`.

```text
TPC263_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL
TPC263_ROUTE_ADVANCE = YES_SCOPED_RANK_THREE_LOG_CHANNEL
TPC263_W_FRAME_MOMENTS = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER
TPC263_ADJOINT_FRAME_COEFFICIENTS = PROVED_SOURCE_BACKED_TPC257
TPC263_PROJECTION_SPLIT = PROVED_EXACT
TPC263_RANK_THREE_CHANNEL = PROVED_SOURCE_BACKED_X_5_OVER_3_LOG_M_PLUS_3
TPC263_ORTHOGONAL_RESIDUAL = OPEN
TPC263_FIXED_POWER_CREDIT = 0
TPC263_ARITHMETIC_ADVANCE = YES_SCOPED_FIXED_LOG_ONLY
TPC263_L2 = NONE
TPC263_FULL_GATE_B = OPEN
TPC263_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC263_TWIN_PRIME_RESULT = NONE
TPC263_STATUS = PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL
TPC263_ROUND2_CLUE = ATTACK_THE_ORTHOGONAL_COMPLEMENT_AFTER_PAYING_THE_RANK_THREE_LOG_CHANNEL
```

Strongest positive result: a source-backed rank-three physical channel is
removed with arbitrary fixed logarithmic strength while preserving the actual
operator and frame.

Strongest obstruction: the exact orthogonal complement remains in the full
coupling and may not be discarded.

Open theorem: estimate or structurally refute the orthogonal-complement
cross-Gram with enough power to exceed the strict `1/400` obligation.

The named Session evaluator files are absent from this checkout.  The local
proof package, theorem ledger, certificate, bridge checker, and `AGENTS.md`
are the fail-closed fallback authority.
