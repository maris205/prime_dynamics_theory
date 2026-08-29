# Bridge B / TPC-310 — cross-holdout aggregation order

## Scoped question

TPC-309 showed that a profile-prefix shift can relocate finite discordance.  This
release freezes that entire parent atlas and asks whether a cross-holdout
summary can be treated as profile-independent.  It enumerates every nonempty
subset of the three profile ladders and every nonempty subset of the three
completion radii, then applies three declared positive aggregation maps.

## Exact finite layer

There are `7 x 7 = 49` selectors.  For a selector `S`, pooled MSE sums the
right and left completion extrema before division; balanced ratio averages the
row-ratio intervals; geometric ratio averages their logarithms and
exponentiates.  Independent finite completion choices make the extrema of a
sum additive.  Positivity makes all three interval maps monotone.  For point
values, the identity

```text
sum(a_i) / sum(b_i) = sum(b_i * (a_i/b_i)) / sum(b_i)
```

shows that pooled aggregation is denominator-weighted, while balanced ratio is
equal-case weighting.

## Locked numerical atlas

The TPC-309 parent contributes 162 envelope observations and 2,106 inherited
candidate evaluations.  TPC-310 produces 147 aggregate observations.  Over all
49 selectors the class counts are:

```text
POOLED_MSE       = RIGHT 42 / LEFT 1 / UNRESOLVED 6
BALANCED_RATIO   = RIGHT 1  / LEFT 32 / UNRESOLVED 16
GEOMETRIC_RATIO  = RIGHT 26 / LEFT 0 / UNRESOLVED 23
```

On the full selector (all ladders and all radii), the intervals are:

```text
POOLED_MSE       = [0.2423655855..., 0.3112477031...] RIGHT
BALANCED_RATIO   = [5.2417686281..., 14.4871333704...] LEFT
GEOMETRIC_RATIO  = [0.1993188213..., 0.8609189559...] RIGHT
```

The first two intervals are separated from both strict thresholds.  Thus the
finite record refutes only the universal claim that these declared aggregation
maps must share one strict class; it does not choose a canonical weighting.

## Claim firewall

```text
TPC310_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_CROSS_HOLDOUT_AGGREGATION_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_AGGREGATION_ORDER_OBSTRUCTION_ATLAS
TPC310_ROUTE_ADVANCE = YES_SCOPED_AGGREGATION_ORDER_OBSTRUCTION
TPC310_SELECTOR_PROTOCOL = PROVED_EXACT_FINITE
TPC310_POOLED_EXTREMA = PROVED_EXACT_FINITE
TPC310_POSITIVE_INTERVAL_MAPS = PROVED_EXACT_FINITE
TPC310_WEIGHTED_MEAN_IDENTITY = PROVED_EXACT_FINITE
TPC310_AGGREGATION_ATLAS = NUMERICALLY_REPRODUCED_FINITE_49_SELECTORS_147_AGGREGATES
TPC310_FULL_SELECTOR_REVERSAL = NUMERICALLY_REPRODUCED_FINITE_POOLED_RIGHT_BALANCED_LEFT_GEOMETRIC_RIGHT
TPC310_PROFILE_ROBUSTNESS = REFUTED_FINITE_NO_UNIVERSAL_AGGREGATION_CLASS
TPC310_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS
TPC310_CAUSAL_IDENTIFICATION = NONE_AGGREGATION_DIAGNOSTIC_ONLY
TPC310_FORMAL_INTERVAL_CERTIFICATE = OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING
TPC310_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC310_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC310_FIXED_POWER_CREDIT = 0
TPC310_FULL_GATE_B = OPEN
TPC310_TWIN_PRIME_RESULT = NONE
TPC310_STATUS = PROVED_EXACT_FINITE_CROSS_HOLDOUT_AGGREGATION_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_AGGREGATION_ORDER_OBSTRUCTION_ATLAS
TPC310_ROUND2_CLUE = TEST_PREREGISTERED_STRATIFIED_WEIGHTS_AND_HOLDOUT_REPLICATION_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM
```

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` files are absent from this checkout.  No official
Route-A or Route-B pass is asserted.  The local fail-closed evidence is the
locked TPC-309 parent, canonical certificate, independent replay, exact stress
suite, theorem ledger, claim firewall, PDF audit, and this Bridge-B checker.

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = exact finite cross-holdout selector algebra plus
                            weighted-mean identity
STRONGEST_OBSTRUCTION = pooled and equal-case arithmetic maps reverse the
                        full-selector class; no universal aggregation class
OPEN_THEOREM = independently justified weighting/stratification law with
               stable growing-regime holdout preference
REUSABLE_STRUCTURE = parent interval atlas -> nonempty selector lattice ->
                     pooled/balanced/geometric maps -> class and reversal census
ROUND2_CLUE = TEST_PREREGISTERED_STRATIFIED_WEIGHTS_AND_HOLDOUT_REPLICATION_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM
```
