# Bridge-B record: TPC-389 long-horizon slope stress

```text
PROJECT = papers/tpc-389-c1-long-horizon-slope-stress
SCHEMA = TPC389_C1_LONG_HORIZON_SLOPE_STRESS_V1
STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_LONG_HORIZON_SLOPE_STRESS
```

## Frozen interface

TPC-389 locks the TPC-388 producer/certificate hashes before reading a third
coordinate-disjoint family.  The response-blind grid is
`a_j=2800001+401j`, with indices `(0,10,20,30,40)`.  The first three origins
are calibration at `N=768,1024`; the final two are holdout at `N=1280`.
The panel crosses `fixed_c3` and `full_relative`, `Q=2048,8192`, four sign
laws, and local/pooled normalization, giving 256 rows and 32 cells.

The parent slope is frozen.  The local control fits only the current
`768 -> 1024` means.  The anchored parent and local forecasts start at
`N=1024`; the recursive parent forecast starts at `N=768`.  Every role and
forecast rule is fixed before endpoint readout.

## Claim firewall

```text
SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
LONG_HORIZON_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS
PARENT_HORIZON_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
PARENT_HORIZON_PASS = 32/32
LOCAL_CONTROL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
LOCAL_CONTROL_PASS = 32/32
RECURSIVE_PARENT_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
RECURSIVE_PARENT_PASS = 32/32
PARENT_MAX_ABS_ERROR = 0.017615584096739245
LOCAL_MAX_ABS_ERROR = 0.011997515978539264
RECURSIVE_MAX_ABS_ERROR = 0.029949940590637381
STABILITY = N768:24/32,N1024:27/32,N1280_HOLDOUT:24/32
SPECTRAL_FAILURES = 64/256
SCHUR_FAILURES = 0/256
ORIGIN_UNIFORMITY = OPEN
COUNT_UNIFORMITY = OPEN
SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
GROWING_OPERATOR_BOUND = OPEN
SOURCE_UNIFORM_L2 = OPEN
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_RECURSIVE_SLOPE_COMPOSITION
```

The recursive maximum lies just below the finite 3% cap.  This is a stress
observation, not an asymptotic margin.  The 64 spectral failures coexist with
zero Schur failures and remain an obstruction to any operator-norm reading.

## Local verification

The local Bridge-B checker locks every project artifact, verifies canonical
certificate semantics, runs ordinary and optimized producer/checker/stress
subchecks, and requires byte-identical `paper/main.pdf` and `paper/paper.pdf`.
It is fail-closed repository evidence, not the absent official Route-B
evaluator.  Therefore this record does not close Route A, Route B, arithmetic
reassembly, or the twin-prime endpoint.
