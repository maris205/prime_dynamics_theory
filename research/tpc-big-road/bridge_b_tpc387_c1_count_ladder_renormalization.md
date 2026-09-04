# Bridge-B record: TPC-387

```text
PROJECT = papers/tpc-387-c1-count-ladder-renormalization/
SCHEMA = TPC387_C1_COUNT_LADDER_RENORMALIZATION_V1
STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_COUNT_LADDER_RENORMALIZATION
```

TPC-387 tests the natural continuation of the TPC-386 count obstruction.  A
three-level `512 -> 768 -> 1024` ladder is frozen on a fresh affine grid.
Three origins and the first two count levels are calibration-only; two later
origins at the endpoint count are holdout.  The calibration log-count slope is
fit separately for every declared mode, normalization, law, and `Q`, then
extrapolated once to the holdout endpoint.

```text
SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
COUNT_LADDER_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS
CALIBRATION_SLOPE_REPAIR = NUMERICALLY_CERTIFIED_FINITE_SCOPED
RENORM_FORECAST_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
RENORM_ERROR_CAP = 0.03
RENORM_PASS = 32/32
SPECTRAL_CAP = 0.64
SPECTRAL_CAP_FAILURES = 40/256
SCHUR_CAP_FAILURES = 0/256
CALIBRATION_STABLE_CELLS = N512:24/32,N768:24/32
HOLDOUT_STABLE_CELLS = N1024:28/32
FIXED_CAP_REPAIR = OPEN
COUNT_UNIFORMITY = OPEN
SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_COUNT_LADDER_SECOND_HOLDOUT
```

The local checker is fail-closed repository evidence, not an official
Route-A/Route-B evaluator.  It locks the finite source, certificate, proof
and route notes, manuscript and PDF, and this record.  It runs the producer,
reverse-shell independent replay, and 25-mutation stress script in ordinary
and optimized Python modes and requires byte-identical output in each pair.
