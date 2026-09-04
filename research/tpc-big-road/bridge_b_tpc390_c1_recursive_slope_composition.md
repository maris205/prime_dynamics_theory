# Bridge-B note: TPC-390 recursive slope composition

This is the local fail-closed bridge record for
`papers/tpc-390-c1-recursive-slope-composition/`.  The official Session
Route-A and Route-B evaluator files are absent from this checkout, so this
note records repository evidence without declaring an official route pass.

```text
TPC390_SCHEMA = TPC390_C1_RECURSIVE_SLOPE_COMPOSITION_V1
TPC390_STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_RECURSIVE_SLOPE_COMPOSITION_AUDIT
SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED_TPC389
RECURSIVE_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS
PARENT_ONE_STEP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
LOCAL_CONTROL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
RECURSIVE_COMPOSITION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
COMPOSITION_IDENTITY = PROVED_EXACT_FINITE_NUMERICAL_IDENTITY
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = LOCALIZE_C1_RECURSIVE_HORIZON_OBSTRUCTION
```

## Locked panel

```text
grid = 3000001 + 401*j, j=0,...,40
selected indices = (0,10,20,30,40)
calibration origins = 3000001,3004011,3008021
holdout origins = 3012031,3016041
calibration counts = 1024,1280
holdout count = 1536
block length = 128
band modes = fixed_c3, full_relative
Q = 2048,8192
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar
transfer cap = absolute ratio error <= 0.03
```

## Evidence contract

The producer and independent checker each reconstruct all 256 rows and 32
cells.  The independent checker uses descending prime-shell order and does not
import the producer.  The stress program rejects 25 response, provenance,
summary, and firewall mutations.  The Bridge-B checker additionally locks the
source, certificate, proof package, notes, PDF pair, compile log, and this
bridge note, then runs ordinary and optimized producer/independent/stress
jobs and requires byte-identical stdout.

The numerical census is intentionally left to the canonical certificate and
the checker output; no finite observation is promoted to a growing theorem.
