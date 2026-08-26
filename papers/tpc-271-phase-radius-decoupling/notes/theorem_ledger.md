# TPC-271 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T271.1 | `Xi=Xi_W*Xi_G` and `Xi/Xi_C=|kappa|^(-6)` | PROVED_EXACT_FINITE | positive finite rows |
| T271.2 | all nine residual scalar intervals are negative real | NUMERICALLY_CERTIFIED | registered rows |
| T271.3 | four dyadic source/output/radius lane classifications | NUMERICALLY_CERTIFIED | finite pairs |
| T271.4 | normalized radius has `DROP_RISE_RISE_DROP` while phase sign is preserved | NUMERICALLY_CERTIFIED | six base rows |
| T271.5 | `96->192` spike is output-lane dominated (`Xi_W<1/8`, `Xi_G>230`) | NUMERICALLY_CERTIFIED | one finite pair |
| T271.6 | profile controls leave source lane invariant and reduce output lane below `9/10` | NUMERICALLY_CERTIFIED | N=96,128,256 |
| T271.7 | source-level signed phase/radius theorem | OPEN | no asymptotic source estimate |

```text
STRONGEST_POSITIVE_RESULT = EXACT_LANE_FACTORIZATION_PLUS_PHASE_LOCKED_OUTPUT_SPIKE_CERTIFICATE
STRONGEST_OBSTRUCTION = GREATER_THAN_23_RADIUS_RISE_WITH_NEGATIVE_PHASE_PRESERVED
OPEN_THEOREM = SOURCE_LEVEL_SIGNED_PHASE_BOUND_WITH_EXPLICIT_RADIUS_LANE_CONTROL
REUSABLE_STRUCTURE = (C_perp,W_perp,G_perp) -> Xi_C,Xi_W,Xi_G -> LANE_RATIO_ATTRIBUTION
ROUND2_CLUE = TEST_SOURCE_LEVEL_SIGNED_PHASE_BOUND_WITH_EXPLICIT_RADIUS_LANE_CONTROL
```
