# Bridge B / TPC-308 — adversarial exclusive-completion envelope

## Scoped question

TPC-307 found three finite reversals between source-budget orientation and a
native exclusive-shell holdout.  TPC-308 keeps the common ambient operator,
overlap-only fit, coefficients, profile prefix, and budget class frozen, then
enumerates every binary exclusive completion within Hamming radii `0,1,2`.
The question is only whether the finite class survives that explicitly
bounded completion family.

## Exact finite layer

For a fixed prediction and binary target, flip subsets of size at most `r`
are in bijection with the Hamming ball.  Exhaustive enumeration therefore
attains the exact finite minimum and maximum squared holdout loss.  Nested
balls make the lower envelope nonincreasing and the upper envelope
nondecreasing.  Radius zero recovers the native TPC-307 loss, and simultaneous
global sign reversal preserves every loss.  Positive interval division gives
the stated conservative ratio interval and conditional strict class rule.

## Locked numerical atlas

The 18 parent cells and three radii give 54 envelope observations.  The
aggregate candidate totals are `36/186/480`.  Agreement counts
`(concordant,discordant,unresolved)` are

```text
r=0: 13/3/2
r=1: 11/2/5
r=2: 10/1/7.
```

All discordances remain localized to the final `Q=70->90` transition and
exponent one.  The count attenuates `3->2->1`; the completion envelope does
not erase the obstruction by radius two, but it widens seven cells into the
unresolved band.  The producer and standalone NumPy checker reproduce the
finite atlas.  Because the physical construction is float64 and the decimal
enclosures are padded rather than directed-rounded, this is not a formal
interval certificate.

## Claim firewall

```text
TPC308_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_HAMMING_COMPLETION_ENVELOPE_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_HOLDOUT_STABILITY_ATLAS
TPC308_ROUTE_ADVANCE = YES_SCOPED_ADVERSARIAL_EXCLUSIVE_COMPLETION_ENVELOPE_AUDIT
TPC308_HAMMING_ENVELOPE_PROTOCOL = PROVED_EXACT_FINITE
TPC308_FIXED_PREDICTION_EXTREMA = PROVED_EXACT_FINITE
TPC308_RADIUS_MONOTONICITY = PROVED_EXACT_FINITE
TPC308_RADIUS_ZERO_RECOVERY = PROVED_EXACT_FINITE
TPC308_FINITE_STABILITY_ATLAS = NUMERICALLY_REPRODUCED_FINITE_54_ENVELOPE_OBSERVATIONS
TPC308_AGREEMENT_R0 = NUMERICALLY_REPRODUCED_FINITE_13_CONCORDANT_3_DISCORDANT_2_UNRESOLVED
TPC308_AGREEMENT_R1 = NUMERICALLY_REPRODUCED_FINITE_11_CONCORDANT_2_DISCORDANT_5_UNRESOLVED
TPC308_AGREEMENT_R2 = NUMERICALLY_REPRODUCED_FINITE_10_CONCORDANT_1_DISCORDANT_7_UNRESOLVED
TPC308_DISCORDANCE_SURVIVAL = NUMERICALLY_REPRODUCED_FINITE_3_TO_2_TO_1_AS_RADIUS_0_TO_2
TPC308_DISCORDANCE_LOCALIZATION = NUMERICALLY_REPRODUCED_FINITE_FINAL_PAIR_70_TO_90_ONLY
TPC308_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS
TPC308_CAUSAL_IDENTIFICATION = NONE_FIXED_PREDICTION_ENVELOPE_DIAGNOSTIC_ONLY
TPC308_FORMAL_INTERVAL_CERTIFICATE = OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING
TPC308_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC308_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC308_FIXED_POWER_CREDIT = 0
TPC308_FULL_GATE_B = OPEN
TPC308_TWIN_PRIME_RESULT = NONE
TPC308_STATUS = PROVED_EXACT_FINITE_HAMMING_COMPLETION_ENVELOPE_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_HOLDOUT_STABILITY_ATLAS
TPC308_ROUND2_CLUE = TEST_PROFILE_PREFIX_PERTURBATION_AND_COMPLETION_INVARIANCE_ON_THE_SURVIVING_DISCORDANCE_CELLS_BEFORE_ANY_PREFERENCE_CLAIM
```

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` files are absent from this checkout.  This file
does not assert an official Route-A or Route-B pass.  The local fail-closed
assessment consists of the parent locks, exact finite proof package,
independent reconstruction, stress suite, PDF audit, and Bridge-B checker.

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = exact finite completion-envelope protocol with
                            independent 54-observation replay
STRONGEST_OBSTRUCTION = at least one final-transition discordance survives
                        radius two, while seven cells become unresolved
OPEN_THEOREM = profile-prefix invariance of the surviving discordance cells
REUSABLE_STRUCTURE = frozen fit -> binary Hamming balls -> finite extrema ->
                     conservative ratio interval -> radius stability census
ROUND2_CLUE = TEST_PROFILE_PREFIX_PERTURBATION_AND_COMPLETION_INVARIANCE_ON_THE_SURVIVING_DISCORDANCE_CELLS_BEFORE_ANY_PREFERENCE_CLAIM
```
