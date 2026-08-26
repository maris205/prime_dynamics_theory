# Bridge B V124 / TPC-271: phase--radius decoupling

Date: 2026-08-27

Status: `NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT`

TPC-270 measured the endpoint-normalized residual radius across a finite
growing-cutoff registry and found `DROP_RISE_RISE_DROP`. TPC-271 adds the
signed projected scalar and both residual norm lanes to the same object. This
tests whether the radius variation is a phase effect or a lane-size effect,
while keeping the literal V59 shell, masks, deleted diagonal, beta source,
cutoff rule, convex profile interface, and rank-three projection fixed.

## Exact finite coordinates

```text
C_perp = <(I-P_3)w_N,(I-P_3)g_(N,theta)>
W_perp = ||(I-P_3)w_N||^2
G_perp = ||(I-P_3)g_(N,theta)||^2
R^2    = W_perp G_perp
kappa  = C_perp/sqrt(W_perp G_perp)
```

The rational sixth-power lane coordinates are

```text
Xi   = (R^2)^3/N^10
Xi_W = W_perp^3/N^5
Xi_G = G_perp^3/N^5
Xi_C = |C_perp|^6/N^10.
```

They obey the exact finite identities
`Xi=Xi_W*Xi_G` and `Xi/Xi_C=|kappa|^(-6)`.

## Certified finite result

All six base rows and three matched `theta=1/2` controls have strictly
negative residual scalar intervals, hence the finite phase label is
`ALL_NEGATIVE_REAL_AXIS`. The four dyadic lane records are

```text
64->128:  Xi_W < 1/2, Xi_G < 3/4, Xi < 1/4
96->192:  Xi_W < 1/8, Xi_G > 230, Xi > 23
128->256: Xi_W < 1/2, Xi_G > 15, Xi > 7
192->384: Xi_W > 1,   Xi_G < 3/4, 3/4 < Xi < 1
```

The `96->192` radius spike is therefore output-lane dominated even though
the signed phase remains negative at both endpoints. At the three profile
controls the source lane is invariant, the output lane drops below `9/10`,
the radius ratio lies in `(1/2,3/4)`, and the negative phase is preserved.

```text
TPC271_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT
TPC271_ROUTE_ADVANCE = YES_SCOPED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT
TPC271_LANE_FACTORIZATION = PROVED_EXACT_FINITE
TPC271_PHASE_SIGN_CENSUS = NUMERICALLY_CERTIFIED_FINITE
TPC271_PHASE_RADIUS_DECOUPLING = NUMERICALLY_CERTIFIED_FINITE
TPC271_SOURCE_LANE_PROFILE_INVARIANCE = PROVED_EXACT_FINITE
TPC271_OUTPUT_LANE_SPIKE = NUMERICALLY_CERTIFIED_FINITE
TPC271_SOURCE_LEVEL_SIGNED_PHASE = OPEN_ASYMPTOTIC
TPC271_SOURCE_LEVEL_RADIUS = OPEN_ASYMPTOTIC
TPC271_FIXED_POWER_CREDIT = 0
TPC271_ARITHMETIC_ADVANCE = NO
TPC271_L2 = NONE
TPC271_FULL_GATE_B = OPEN
TPC271_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC271_TWIN_PRIME_RESULT = NONE
TPC271_STATUS = NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT
TPC271_ROUND2_CLUE = TEST_SOURCE_LEVEL_SIGNED_PHASE_BOUND_WITH_EXPLICIT_RADIUS_LANE_CONTROL
```

Strongest positive result: the exact lane factorization separates source and
output contributions, and an independent certificate locks the phase sign over
all nine rows while identifying the `96->192` output-lane spike.

Strongest obstruction: constant finite phase sign does not stabilize the
normalized radius; a greater-than-23 rise coexists with a source-lane drop
below `1/8`.

Open theorem: a source-compatible signed-phase estimate coupled to an explicit
radius-lane bound and uniformity range. No arithmetic Route-B closure or
twin-prime claim is made.

The Session-named `propose.md` and route evaluator files are absent from this
checkout. The project proof package, theorem ledger, certificate, independent
replay, stress audit, bridge checker, and `AGENTS.md` are used as the
fail-closed fallback authority.
