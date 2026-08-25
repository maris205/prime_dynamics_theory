# TPC-249: Sharp Weighted Contraction on Shared Gram Lanes

Status: `PROVED_STRUCTURAL_L1_SHARP_WEIGHTED_SHARED_LANE_CONTRACTION`

For each TPC-248 output block, let `v_cb=A_cb beta_b`, choose complex weights
`lambda_cb`, and contract inside the physical shared lane:

```text
g_c=sum_b lambda_cb v_cb.
```

Because the inner product is conjugate-linear first,

```text
sum_b lambda_cb <W_c,v_cb>=<W_c,g_c>.
```

For independent centered lane balls `||W_c||<=rho_c`, the aggregate scalar has
the exact disk image `R Dbar`, where

```text
R=sum_c rho_c||g_c||
 =sum_c rho_c sqrt(lambda_c*G_c lambda_c).
```

Every point of the disk has an explicit preimage.  Under the declared modeling
choice `W_c=W_c^0+U_c`, `||U_c||<=rho_c`, this translates to `C+R Dbar`, with
`C=sum_c<W_c^0,g_c>`.  For one global direct-sum perturbation budget the exact
radius is

```text
rho sqrt(sum_c lambda_c*G_c lambda_c).
```

The old tagged/marginal triangle radius

```text
R_tag=sum_c rho_c sum_b |lambda_cb| ||v_cb||
```

always dominates `R`.  Equality on a positive-radius group holds exactly when
the nonzero vectors `lambda_cb v_cb` lie on one common nonnegative real ray.
Repeated probes with weights `(1,-1)` give `R=0` but positive `R_tag`, so the
shared-lane contraction can recover cancellation erased by tagged copies.

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

Strongest positive result: exact source-oriented weighted support radius with
explicit reverse realization.  Strongest obstruction: its value can range
from the full tagged radius to zero while all marginal norms stay fixed.  Open
theorem: bound the actual V59 Gram quadratic forms.  Reusable structure:
within-lane vector contraction, Gram quadratic form, disk support, and
independent/global budget ledger.

`ROUND2_CLUE = ESTIMATE_LITERAL_GRAM_QUADRATIC_FORMS_OR_BOUND_THEM_FROM_COMPUTABLE_COHERENCE_DATA`
