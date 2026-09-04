# Bridge-B note: TPC-391 recursive horizon localization

This is the local fail-closed bridge record for
papers/tpc-391-c1-recursive-horizon-localization/.  The official Session
Route-A and Route-B evaluator files are absent from this checkout, so this
note records repository evidence without declaring an official route pass.

~~~text
TPC391_SCHEMA = TPC391_C1_RECURSIVE_HORIZON_LOCALIZATION_V1
TPC391_STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_RECURSIVE_HORIZON_LOCALIZATION_AUDIT
SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED_TPC390
HORIZON_PANEL = NUMERICALLY_CERTIFIED_FINITE_448_ROWS
PARENT_HORIZON_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
LOCAL_CONTROL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
HORIZON_TRAJECTORY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
RECURSIVE_COMPOSITION = PROVED_EXACT_FINITE_NUMERICAL_IDENTITY
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_NORMALIZATION_PHASE_DIAGRAM
~~~

## Locked panel

~~~text
grid = 3400001 + 401*j, j=0,...,40
selected indices = (0,10,20,30,40)
calibration origins = 3400001,3404011,3408021
holdout origins = 3412031,3416041
calibration counts = 1024,1152,1280,1408
holdout count = 1536
block length = 128
band modes = fixed_c3, full_relative
Q = 2048,8192
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar
transfer cap = absolute ratio error <= 0.03
~~~

## Evidence contract

The producer and independent checker each reconstruct all 448 rows and 32
cells.  The independent checker uses descending prime-shell order and does not
import the producer.  The stress program rejects 25 response, provenance,
trajectory, summary, and firewall mutations.  The Bridge-B checker additionally
locks the source, certificate, proof package, notes, PDF pair, compile log, and
this bridge note, then runs ordinary and optimized producer/independent/stress
jobs and requires byte-identical stdout.

The certificate records parent/local/recursive pass counts at each horizon:
32/32,32/32,32/32,23/32 for the parent through 1536, and 32/32 at every
local horizon.  Nine parent cells cross for the first time at 1536.  The
numerical census is intentionally left to the canonical certificate and
checker output; no finite observation is promoted to a growing theorem.
