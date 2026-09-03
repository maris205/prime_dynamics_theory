# Bridge-B proof package: TPC-365 beta=2 fresh holdout

## Scope

TPC-365 freezes the beta=2 rule identified by TPC-364 and tests it on a new
finite high-origin panel.  Fifty-one candidate origins
`410001+257j`, `0<=j<51`, are scored on 256-point pilots using only unsigned
weighted square geometry.  The descending-spread, origin-tie-break, greedy
separation rule with minimum distance `2048` selects
`(413342,410258,416940)`.  Signed responses are evaluated only after this
selection.  The holdout compares beta `{0,2}`, counts `{256,512}`, shell
anchors `Q={80,128,256,512}`, exponents `{1,2}`, and four fixed laws, for 384
rows total.

## Finite result

```text
TPC365_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
TPC365_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC365_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_384_ROWS
TPC365_BETA2_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC365_BETA2_CAP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC365_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC365_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC365_GROWING_OPERATOR_BOUND = OPEN
TPC365_SOURCE_UNIFORM_L2 = OPEN
TPC365_ARITHMETIC_ADVANCE = NO
TPC365_FIXED_POWER_CREDIT = 0
TPC365_FULL_GATE_B = OPEN
TPC365_TWIN_PRIME_RESULT = NONE
```

Beta=2 has zero spectral-cap violations in 192 rows and maximum normalized
spectrum `0.61633188509480319`; beta=0 has 30 violations in 192 rows and
maximum `1.6398827540264729`.  The beta=2 maximum differs from the TPC-364
value by `4.4345466941875245e-05`, below the declared finite transfer
tolerance `0.001`.

## Exact and independent controls

The weighted geometry is a finite sum of rational squares and is positive on
all audited rows.  The exact anchor is the half-open interval
`[413372,413385)`, with `Q=4`, shell `{5,7}`, exponent one, checked for both
betas.  The producer uses forward shell accumulation; the independent
checker rebuilds the sieve, response-blind selection, masks, weights, four
laws, envelopes, and spectra in reverse shell order.  The adversarial stress
checker rejects 19 mutations.  The local Bridge-B checker locks all
claim-bearing files, verifies PDF identity and compile diagnostics, and runs
producer, independent, and stress checks in normal and optimized modes with
empty stderr and byte-identical stdout.

## Route boundary

This is finite transfer evidence from a geometry-selected panel.  It is not a
random-sample claim, a source-valid normalization theorem, a growing-`Q`
operator estimate, an arithmetic `L2` bound, a Route-A/Route-B pass, a fixed
power saving, or a twin-prime conclusion.  The official Session-named Route-A
and Route-B evaluator files are absent, so the local check is fail-closed and
does not assert an official evaluator pass.  The next test keeps beta=2 fixed
and extends the shell ladder to higher `Q` on a new scale panel.
