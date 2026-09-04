# Bridge-B record: TPC-386

```text
PROJECT = papers/tpc-386-c1-count-holdout-bandwidth/
SCHEMA = TPC386_C1_COUNT_HOLDOUT_BANDWIDTH_V1
STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_COUNT_HOLDOUT_BANDWIDTH
```

TPC-386 is a response-blind count holdout following TPC-385.  Three fresh
`N=512` origins define calibration-only pooled geometry; two fresh `N=1024`
origins are holdout.  The panel has 160 rows and 32 cells, with fixed
three-block and full-relative bands, `Q=2048,8192`, four sign laws, and two
normalizations.

```text
SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
COUNT_HOLDOUT_PANEL = NUMERICALLY_CERTIFIED_FINITE_160_ROWS
ALL_PLUS_COUNT_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
FIXED_SPECTRAL_CAP_TRANSFER = REFUTED_FINITE_SCOPED
SPECTRAL_CAP = 0.64
SPECTRAL_CAP_FAILURES = 16/160 (all-plus N=1024 rows)
SCHUR_CAP_FAILURES = 0/160
CALIBRATION_STABLE_CELLS = 20/32
HOLDOUT_STABLE_CELLS = 28/32
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_COUNT_LADDER_RENORMALIZATION
```

The local checker below is fail-closed repository evidence.  It locks the
producer, independent replay, stress script, certificate, paper source and
PDFs, all proof/route notes, and this bridge record.  It runs ordinary and
optimized Python modes and requires byte-identical output from each pair.
