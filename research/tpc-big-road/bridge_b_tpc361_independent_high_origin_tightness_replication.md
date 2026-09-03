# Bridge-B proof package: TPC-361

```text
TPC361_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION
TPC361_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
TPC361_HIGH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC361_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC361_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC361_TIGHTNESS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC361_LAW_UNIFORM_SHORT_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC361_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
TPC361_GROWING_OPERATOR_BOUND = OPEN
TPC361_SOURCE_UNIFORM_L2 = OPEN
TPC361_ARITHMETIC_ADVANCE = NO
TPC361_FIXED_POWER_CREDIT = 0
TPC361_FULL_GATE_B = OPEN
TPC361_TWIN_PRIME_RESULT = NONE
```

TPC-361 independently selects three origins from the frozen 51-candidate grid
`310001+233j` using only the six unsigned geometry spreads at pilot count 256.
The deterministic separated selection is `(313030,311166,321651)`.  The
post-selection replay records 288 finite law rows; 180 rows also record true
spectra (all four laws at counts 256 and 512, all-plus at counts 1024 and
2048).  The normalized Schur and spectral maxima are
`0.80830232610282304` and `0.62690716242733457`; the largest spectral/Schur
ratio is `0.77585950058997`.

The all-plus ladder has 12 increases, 36 decreases, and 6 flats among 54
adjacent transitions, and the short four-law winner census is all-plus 30,
mod-4 6, alternating 0, half-split 0.  These are finite observations only.
They do not establish a growing operator bound, source-uniform arithmetic
`L2`, a fixed-power saving, Route-B reassembly, or a twin-prime result.

The Session-named official Route-A/Route-B evaluator files are absent from the
checkout.  This package is therefore fail-closed local finite evidence, not an
official evaluator pass.
