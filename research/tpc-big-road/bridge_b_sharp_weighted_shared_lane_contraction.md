# Bridge B: sharp weighted shared-lane contraction

For the literal fixed-`c` probes `v_cb=A_cb beta_b`, TPC-249 contracts complex
weights inside the one physical output lane:

```text
g_c=sum_b lambda_cb v_cb,
sum_b lambda_cb<W_c,v_cb>=<W_c,g_c>.
```

For independent centered balls `||W_c||<=rho_c`, the exact scalar image is
`R Dbar`, with

```text
R=sum_c rho_c sqrt(lambda_c*G_c lambda_c).
```

Every point has an explicit reverse realization.  A declared affine model
translates the disk by `C=sum_c<W_c^0,g_c>`, while a global direct-sum budget
has exact radius `rho sqrt(sum_c lambda_c*G_c lambda_c)`.

The tagged marginal radius dominates the exact radius, with equality exactly
under common nonnegative-ray alignment on every active group.  Repeated probes
with opposite weights give exact radius zero but positive tagged radius.

```text
TPC249_LITERAL_WEIGHTED_PROBE_CONTRACTION = PROVED_EXACT
TPC249_INDEPENDENT_BALL_AGGREGATE_IMAGE = PROVED_EXACT_DISK
TPC249_GRAM_RADIUS = PROVED_EXACT
TPC249_EXPLICIT_REVERSE_REALIZATION = PROVED_EXACT
TPC249_AFFINE_CENTER_TRANSLATION = PROVED_FOR_DECLARED_MODELING_CHOICE
TPC249_GLOBAL_BUDGET_RADIUS = PROVED_EXACT_DIRECT_SUM_SUPPORT
TPC249_TAGGED_RADIUS_DOMINANCE = PROVED_EXACT
TPC249_TAGGED_RADIUS_EQUALITY = PROVED_IFF_COMMON_NONNEGATIVE_RAY_PER_ACTIVE_GROUP
TPC249_REPEATED_PROBE_CANCELLATION = PROVED_EXACT
TPC249_ACTUAL_GRAM_ASYMPTOTIC = OPEN
TPC249_ARITHMETIC_ADVANCE = NO
TPC249_FIXED_ATOM_CREDIT = 0
TPC249_L2 = NONE
TPC249_FULL_GATE_B = OPEN
TPC249_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC249_TWIN_PRIME_RESULT = NONE
TPC249_STATUS = PROVED_STRUCTURAL_L1_SHARP_WEIGHTED_SHARED_LANE_CONTRACTION
```

The next bridge seeks computable and adversarially sharp bounds for the literal
Gram quadratic forms.  No arithmetic saving is assigned here.
