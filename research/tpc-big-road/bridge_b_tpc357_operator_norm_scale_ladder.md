# Bridge-B: TPC-357 operator-norm scale ladder

```text
BRIDGE_B_TPC357 = LOCAL_FAIL_CLOSED_FINITE_AUDIT
TPC357_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_OPERATOR_NORM_SCALE_LADDER
TPC357_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC357_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC357_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC357_NORMALIZED_SCHUR_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC357_ALL_PLUS_SPECTRAL_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC357_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
TPC357_GROWING_OPERATOR_BOUND = OPEN
TPC357_SOURCE_UNIFORM_L2 = OPEN
TPC357_ARITHMETIC_ADVANCE = NO
TPC357_FIXED_POWER_CREDIT = 0
TPC357_FULL_GATE_B = OPEN
TPC357_TWIN_PRIME_RESULT = NONE
TPC357_ROUTE_A_OFFICIAL_EVALUATOR = ABSENT_FAIL_CLOSED
TPC357_ROUTE_B_OFFICIAL_EVALUATOR = ABSENT_FAIL_CLOSED
```

## Mathematical progress

TPC-357 freezes the three TPC-356 geometry-adversarial origins and extends
the count ladder to `256,512,1024,2048`.  All four sign laws are audited with
Schur and Frobenius envelopes on 288 rows; all-plus receives a true spectral
readout on 72 rows.  The normalized Schur maximum is
`0.8077815961017315`, the normalized all-plus spectral maximum is
`0.62665294142584216`, and the raw all-plus spectral maximum is
`1542.7455490253569`.

The finite obstruction is equally important: normalized all-plus spectral
transitions are `(15 increase,35 decrease,4 flat)` under guard `1e-6`.
Hence a monotone-decay statement fails on this declared ladder, while no
origin-uniform or growing operator theorem follows.

## Reproducibility

The Bridge-B checker verifies canonical certificate and PDF identity, locks
all claim-bearing files, runs producer/independent/stress checks in normal and
optimized Python modes, and requires byte-identical outputs.  The official
Session evaluator files are absent; no official Route-A or Route-B pass is
claimed.
