# Bridge B / TPC-311 — declared stratification and tau-slice holdout

## Scoped question

TPC-310 showed that aggregation order can reverse a finite preference.  TPC-311
fixes one explicit two-stage rule: pool LOW/BASE/HIGH profile ladders inside
each design cell, then give every `(transition, exponent, tau, radius)` cell
equal arithmetic weight.  The two tolerance points `0.25,0.5` are used as a
calibration slice and `0.75` as a held-out parameter slice.

Radius zero is the primary native endpoint.  Radii one and two are included as
declared adversarial stress controls.  The confirmation is a slice of the same
locked parent atlas, not a fresh physical sample; the child declaration is not
an externally timestamped preregistration.

## Exact finite layer

The factorial design has `3 x 2 x 3 x 3 = 54` profile-pooled strata and 162
parent observations.  For a stratum `s`, independent completion extrema give

```text
P_s = [sum_j R_{j,s}^- / sum_j L_{j,s}^+,
       sum_j R_{j,s}^+ / sum_j L_{j,s}^-].
```

For a nonempty block `B`, the declared second stage is

```text
S(B) = [mean_s P_s^-, mean_s P_s^+].
```

Positive denominators and arithmetic monotonicity make these finite interval
operations exact relative to the locked decimal inputs.  The strict classes
are RIGHT when the upper endpoint is below `0.9`, LEFT when the lower endpoint
is above `1.1`, and UNRESOLVED otherwise.

## Locked numerical atlas

The primary native calibration block has

```text
[4.061581467640734..., 4.061743934148754...] LEFT
```

and the native confirmation block has

```text
[0.681844232716634..., 0.681871507031426...] RIGHT
```

so the strict class reverses.  With all three radii, calibration is LEFT but
confirmation is `[0.3840496869..., 2.9038163322...]` and therefore unresolved.
Omitting BASE changes the native calibration class to RIGHT; native exponent
one is LEFT while exponent two is RIGHT.

## Claim firewall

```text
TPC311_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_STRATIFIED_HOLDOUT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_TAU_SLICE_NONREPLICATION_ATLAS
TPC311_ROUTE_ADVANCE = YES_SCOPED_TAU_SLICE_HOLDOUT_OBSTRUCTION
TPC311_STRATIFIED_PROTOCOL = PROVED_EXACT_FINITE
TPC311_PROFILE_POOL_EXTREMA = PROVED_EXACT_FINITE
TPC311_EQUAL_STRATUM_INTERVAL_MAP = PROVED_EXACT_FINITE
TPC311_TAU_PARTITION = PROVED_EXACT_FINITE
TPC311_STRATIFIED_ATLAS = NUMERICALLY_REPRODUCED_FINITE_54_STRATA_6_BLOCKS_22_SENSITIVITY_BLOCKS
TPC311_NATIVE_TAU_REPLICATION = REFUTED_FINITE_STRICT_CALIBRATION_LEFT_CONFIRMATION_RIGHT
TPC311_ALL_RADII_TAU_REPLICATION = REFUTED_FINITE_CALIBRATION_LEFT_CONFIRMATION_UNRESOLVED
TPC311_PROFILE_ROBUSTNESS = REFUTED_FINITE_BASE_OMISSION_CHANGES_NATIVE_CALIBRATION_CLASS
TPC311_EXPONENT_ROBUSTNESS = REFUTED_FINITE_NATIVE_CALIBRATION_EXPONENT_1_LEFT_EXPONENT_2_RIGHT
TPC311_REGISTRATION_STATUS = DECLARED_CHILD_PROTOCOL_NOT_EXTERNALLY_TIMESTAMPED_PREREGISTRATION
TPC311_FRESH_PHYSICAL_HOLDOUT = NONE_SAME_LOCKED_PARENT_ATLAS
TPC311_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS
TPC311_CAUSAL_IDENTIFICATION = NONE_PARAMETER_SLICE_DIAGNOSTIC_ONLY
TPC311_FORMAL_INTERVAL_CERTIFICATE = OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING
TPC311_EXTERNAL_WEIGHT_JUSTIFICATION = OPEN
TPC311_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC311_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC311_FIXED_POWER_CREDIT = 0
TPC311_FULL_GATE_B = OPEN
TPC311_TWIN_PRIME_RESULT = NONE
TPC311_STATUS = PROVED_EXACT_FINITE_STRATIFIED_HOLDOUT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_TAU_SLICE_NONREPLICATION_ATLAS
TPC311_ROUND2_CLUE = REQUIRE_FRESH_SOURCE_HOLDOUT_AND_EXTERNALLY_JUSTIFIED_WEIGHT_LAW_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM
```

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` files are absent from this checkout.  This bridge
therefore records a local fail-closed result and asserts no official Route-A
or Route-B pass.

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = exact two-stage finite stratification protocol plus
                            independent 54-stratum replay
STRONGEST_OBSTRUCTION = native calibration LEFT reverses to held-out tau=.75
                        RIGHT under the fixed declared rule
OPEN_THEOREM = externally justified weights plus fresh physical holdout with
               stable profile/exponent/transition/tolerance preference
REUSABLE_STRUCTURE = profile-pooled design cell -> equal-cell interval map ->
                     disjoint parameter slice -> replication classification
ROUND2_CLUE = REQUIRE_FRESH_SOURCE_HOLDOUT_AND_EXTERNALLY_JUSTIFIED_WEIGHT_LAW_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM
```
