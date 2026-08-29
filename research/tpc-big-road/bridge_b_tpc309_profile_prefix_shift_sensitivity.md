# Bridge B / TPC-309 — profile-prefix shift sensitivity

## Scoped question

TPC-308 left a finite discordance after adversarial exclusive completions.  This
paper keeps its common ambient operator, shell labels, alignment, and Hamming
completion protocol fixed, and changes only the source-backed 17-coordinate
profile ladder.  The declared LOW/BASE/HIGH ladders are neighboring windows
in one 19-prime cutoff pool.

## Exact finite layer

The three profile ladders are finite contiguous windows, and their adjacent
overlap has size 16.  Enlarging an ordered prefix enlarges its column span, so
least-squares residuals are nested and the maximum of two first-feasible
prefixes is feasible for both targets.  Binary flip-subset enumeration gives
the exact Hamming completion extrema and binomial candidate counts.  A common
positive normalizer cancels from the directional source-energy ratio, and
positive interval division gives the conditional class rule.

## Locked numerical atlas

The producer and an independent NumPy checker reproduce 54 profile cases and
162 envelope observations.  Candidate totals across LOW/BASE/HIGH are
`108/558/1440` at radii `0/1/2`.  BASE recovers TPC-308's agreement classes
`13/3/2`, `11/2/5`, and `10/1/7`.  At radius zero LOW has agreement
`13/4/1`, BASE `13/3/2`, and HIGH `10/5/3`; at radius two they are
`8/1/9`, `10/1/7`, and `5/0/13`.

The strict-discordance locations are not invariant.  At radius zero the
LOW/BASE/HIGH transition counts are respectively `(2,1,1)`, `(0,0,3)`, and
`(2,2,1)` over `50->60`, `60->70`, `70->90`.  At radius two they are
`(1,0,0)`, `(0,0,1)`, and `(0,0,0)`.

## Claim firewall

```text
TPC309_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_PROFILE_LADDER_SHIFT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_PROFILE_SENSITIVITY_ATLAS
TPC309_ROUTE_ADVANCE = YES_SCOPED_PROFILE_SENSITIVITY_OBSTRUCTION
TPC309_WINDOW_PROTOCOL = PROVED_EXACT_FINITE
TPC309_PREFIX_NESTING = PROVED_EXACT_FINITE
TPC309_HAMMING_EXTREMA = PROVED_EXACT_FINITE
TPC309_NORMALIZER_INVARIANCE = PROVED_EXACT_FINITE
TPC309_PROFILE_ATLAS = NUMERICALLY_REPRODUCED_FINITE_54_PROFILE_CASES_162_ENVELOPES
TPC309_BASELINE_RECOVERY = NUMERICALLY_REPRODUCED_FINITE_TPC308_CLASSES
TPC309_PROFILE_ROBUSTNESS = OPEN_PROFILE_INDEPENDENT_PREFERENCE
TPC309_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS
TPC309_CAUSAL_IDENTIFICATION = NONE_PROFILE_SENSITIVITY_DIAGNOSTIC_ONLY
TPC309_FORMAL_INTERVAL_CERTIFICATE = OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING
TPC309_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC309_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC309_FIXED_POWER_CREDIT = 0
TPC309_FULL_GATE_B = OPEN
TPC309_TWIN_PRIME_RESULT = NONE
TPC309_STATUS = PROVED_EXACT_FINITE_PROFILE_LADDER_SHIFT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_PROFILE_SENSITIVITY_ATLAS
TPC309_ROUND2_CLUE = TEST_CROSS_HOLDOUT_AGGREGATION_AND_PROFILE_ROBUSTNESS_BEFORE_ANY_PREFERENCE_CLAIM
```

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` files are absent from this checkout.  No official
Route-A or Route-B pass is asserted.  The local fail-closed assessment is the
locked parent chain, independent replay, exact stress suite, PDF audit, and
this checker.

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = explicit same-dimensional neighboring profile
                            perturbation with independent finite replay
STRONGEST_OBSTRUCTION = strict discordance location and radius-two survival
                        change across LOW/BASE/HIGH
OPEN_THEOREM = profile-independent preference or principled profile-selection law
REUSABLE_STRUCTURE = source-backed cutoff windows -> common prefix frontier ->
                     budget/holdout interval -> completion envelope -> location census
ROUND2_CLUE = TEST_CROSS_HOLDOUT_AGGREGATION_AND_PROFILE_ROBUSTNESS_BEFORE_ANY_PREFERENCE_CLAIM
```
