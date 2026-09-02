# Bridge-B proof package: TPC-360

```text
TPC360_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT
TPC360_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC360_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC360_ALL_LAW_SPECTRAL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
TPC360_SCHUR_SLACK = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC360_LAW_UNIFORM_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC360_GROWING_OPERATOR_BOUND = OPEN
TPC360_SOURCE_UNIFORM_L2 = OPEN
TPC360_ARITHMETIC_ADVANCE = NO
TPC360_FIXED_POWER_CREDIT = 0
TPC360_FULL_GATE_B = OPEN
TPC360_TWIN_PRIME_RESULT = NONE
```

TPC-360 replays all four fixed sign laws on the three TPC-359 origins at
counts 256 and 512 (144 rows).  The maximum spectral/Schur ratio is
`0.77628391453148915`; the maximum spectral/Frobenius ratio is
`0.62110877254133434`.  All-plus wins 30 of 36 setting-wise comparisons and
mod-4 wins 6.  These are finite diagnostics only.  The official Session-named
Route-A/Route-B evaluator files are absent, so this package is fail-closed
local evidence and not an official evaluator pass.
