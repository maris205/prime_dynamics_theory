# Bridge-B proof package: TPC-366 fixed beta=2 higher-Q ladder

## Scope

TPC-366 freezes the beta=2 rule carried by TPC-365 and tests scale rather
than refitting the weight.  Forty-one candidate origins
`620001+307j`, `0<=j<41`, are scored on 256-point pilots using only unsigned
weighted square geometry over `Q={512,1024,2048,4096,8192}` and exponents
`{1,2}`.  The descending-spread, origin-tie-break, greedy separation rule
with minimum distance `2048` selects `(623071,631360,629211)`.  Signed
responses are evaluated only after this selection.  The frozen replay has
two counts, five shell anchors, two exponents, four fixed laws, and betas
`{0,2}`, for 480 rows total.

## Finite result

```text
TPC366_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
TPC366_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC366_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_480_ROWS
TPC366_HIGHER_Q_LADDER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC366_BETA2_HIGHER_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC366_BETA2_SCALE_UNIFORMITY = OPEN
TPC366_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC366_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC366_GROWING_OPERATOR_BOUND = OPEN
TPC366_SOURCE_UNIFORM_L2 = OPEN
TPC366_ARITHMETIC_ADVANCE = NO
TPC366_FIXED_POWER_CREDIT = 0
TPC366_FULL_GATE_B = OPEN
TPC366_TWIN_PRIME_RESULT = NONE
```

On the selected finite panel, beta=2 has zero spectral-cap and zero
Schur-cap violations in all 240 rows.  Its maximum normalized spectrum is
`0.62448287758976528` and its maximum normalized Schur value is
`0.65368278287004711`.  The beta=0 control has 60 violations of each cap in
240 rows, with maximum spectrum `1.6419614115857373`.

The beta=2 maximum is not asserted to decay: it exceeds the TPC-365 value
`0.61633188509480319` by `0.0081509924949620949`.  This is a finite
higher-Q observation on a geometry-selected panel, not a shell-uniform
operator theorem, a source-valid arithmetic normalization, a fixed-power
credit, or a twin-prime result.

## Exact and independent controls

The weighted geometry is a finite sum of rational squares and is positive on
all audited rows.  The exact anchor is the half-open interval
`[623372,623385)`, with `Q=4`, exponent one, and shell `{5,7}`, checked for
both betas.  The producer accumulates the shell in increasing order.  An
independently written checker rebuilds the sieve, response-blind selection,
masks, weights, four laws, geometry, finite envelopes, and true spectra in
reverse shell order, comparing every row and the exact anchor.  A separate
adversarial checker rejects 23 mutations of the protocol, selection, scale
limits, phase counts, and claim-firewall fields.

The local Bridge-B checker locks every claim-bearing source, certificate,
manuscript, PDF, log, and project note.  It runs producer, independent, and
stress checks in normal and optimized modes, requiring empty stderr and
byte-identical stdout.  The official Session-named Route-A and Route-B
evaluator files are absent from this checkout; this local check is
fail-closed reproducibility evidence only and does not assert an official
evaluator pass.

## Route boundary and next probe

The finite ladder removes the tested shell size as the immediate obstruction,
but it does not remove geometry selection, finite-window dependence, or the
missing source-valid arithmetic bridge.  The next minimal probe therefore
keeps beta=2 fixed while testing longer windows and predeclared or unselected
origins.  Any failure is to be localized by window length, origin, shell
anchor, and sign law before changing the model.
