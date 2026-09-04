# Bridge-B record: TPC-388

```text
PROJECT = papers/tpc-388-c1-cross-family-slope-transfer/
SCHEMA = TPC388_C1_CROSS_FAMILY_SLOPE_TRANSFER_V1
STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_CROSS_FAMILY_SLOPE_TRANSFER
```

TPC-388 freezes the 32 cell-wise count slopes from TPC-387 and applies them
without refitting to a new coordinate-disjoint family.  Three origins at
`N=512,768` are calibration and two origins at `N=1024` are holdout.  A
same-family slope fit is retained as a predeclared control.

```text
SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
CROSS_FAMILY_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS
PARENT_SLOPE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
LOCAL_CONTROL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
PARENT_TRANSFER_PASS = 32/32
LOCAL_CONTROL_PASS = 32/32
PARENT_TRANSFER_MAX_ABS_ERROR = 0.023402666610706224
SPECTRAL_CAP_FAILURES = 40/256
SCHUR_CAP_FAILURES = 0/256
STABLE_HOLDOUT_CELLS = N1024:28/32
ORIGIN_UNIFORMITY = OPEN
COUNT_UNIFORMITY = OPEN
SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_CROSS_FAMILY_SLOPE_STRESS
```

The local checker is fail-closed repository evidence, not an official
Route-A/Route-B evaluator.  It locks the source, parent interface,
certificate, proof package, manuscript, PDF, and route notes, and runs the
producer, descending-shell independent replay, and 25-mutation stress in
ordinary and optimized Python modes.
