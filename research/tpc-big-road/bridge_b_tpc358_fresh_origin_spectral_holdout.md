# Bridge-B: TPC-358 fresh-origin spectral holdout

```text
BRIDGE_B_TPC358 = LOCAL_FAIL_CLOSED_FINITE_AUDIT
TPC358_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_FRESH_ORIGIN_SPECTRAL_HOLDOUT
TPC358_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC358_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC358_FRESH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC358_PARENT_CAP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC358_NORMALIZED_SCHUR_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC358_ALL_PLUS_SPECTRAL_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC358_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
TPC358_GROWING_OPERATOR_BOUND = OPEN
TPC358_SOURCE_UNIFORM_L2 = OPEN
TPC358_ARITHMETIC_ADVANCE = NO
TPC358_FIXED_POWER_CREDIT = 0
TPC358_FULL_GATE_B = OPEN
TPC358_TWIN_PRIME_RESULT = NONE
TPC358_ROUTE_A_OFFICIAL_EVALUATOR = ABSENT_FAIL_CLOSED
TPC358_ROUTE_B_OFFICIAL_EVALUATOR = ABSENT_FAIL_CLOSED
```

## Mathematical progress

TPC-358 replays the TPC-357 finite operator protocol on the disjoint,
widely separated origins `(52001,120001,220001)`, fixed by the rule
`52001+100000j` before any matrix is evaluated.  The four sign laws, four
counts, three shell anchors, and two kernel exponents give 288 rows; Schur
and Frobenius envelopes are recorded everywhere and all-plus spectra on 72
raw/normalized rows.  The fresh normalized Schur maximum is
`0.80850510742101689`, the normalized all-plus spectral maximum is
`0.62663944469203836`, and both remain below the frozen parent caps `0.83`
and `0.64` and within `0.001` of the parent values.

The strongest obstruction survives the transfer: normalized all-plus
spectral transitions are `(13 increase,34 decrease,7 flat)` on the declared
four-count ladder.  Thus finite cap transfer is not a growing operator
estimate and does not pay arithmetic, fixed-power, Route-B, or twin-prime
credit.

## Reproducibility

The checker locks the producer, independent reverse-shell replay, mutation
stress test, canonical certificate, final PDF, compile log, and this bridge
record.  It reruns the three executable checks in normal and optimized Python
modes and requires byte-identical stdout.  The Session-named official
Route-A and Route-B evaluator files are absent; no official evaluator pass is
claimed.
