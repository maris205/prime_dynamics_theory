# Bridge-B note: TPC-393 adversarial normalization holdout

This is the local fail-closed bridge record for
`papers/tpc-393-c1-normalization-adversarial-holdout/`.  The official Session
Route-A and Route-B evaluator files are absent from this checkout, so this
note records repository evidence without declaring an official route pass.

```text
TPC393_SCHEMA = TPC393_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_V1
TPC393_STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_AUDIT
SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED_TPC392
NORMALIZATION_PANEL = NUMERICALLY_CERTIFIED_FINITE_64_ROWS
SCALAR_DEFINITIONS = PROVED_EXACT_FINITE_DECLARED
PHASE_COMPARISON = NUMERICALLY_CERTIFIED_FINITE_SCOPED
CALIBRATION_FORECAST = NUMERICALLY_CERTIFIED_FINITE_SCOPED
ORIGIN_UNIFORMITY = OPEN
SPECTRAL_ENVELOPE = REFUTED_ON_DECLARED_FINITE_PANEL
SCHUR_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_ORIGIN_UNIFORMITY_AFTER_REPLICATION
```

## Locked panel

```text
grid = 4200001 + 401*j, j=0,...,40
selected indices = (0,10,20,30,40)
calibration origins = 4200001,4204011,4208021
holdout origins = 4212031,4216041
calibration counts = 1024,1280
holdout count = 1536
block length = 128
band mode = fixed_c3
Q = 8192
laws = all_plus, alternating_index
normalizations = local_diagonal, pooled_train_scalar, origin_scalar,
                 frozen_train_1024_scalar
forecast cap = absolute ratio error <= 0.03
spectral cap = 0.64; Schur cap = 0.83
```

## Evidence contract

The producer and independent checker reconstruct 64 rows and 8 cells.  The
independent checker uses descending prime-shell order and does not import the
producer.  The stress program rejects 25 response, provenance, role, summary,
anchor, and firewall mutations.  The Bridge-B checker additionally locks the
source, certificate, proof package, notes, PDF pair, compile log, README, and
this bridge note, then runs ordinary and optimized producer/independent/stress
jobs and requires matching output within each implementation.

The sealed finite census is:

```text
forecast passes (each normalization, all-plus/alternating) = 2/2
maximum forecast errors =
  local 0.01010300962072197
  pooled 0.0097142554430971195
  origin 0.011039357664235361
  frozen 0.0097142554430980077
spectral failures = 32/32; Schur failures = 0/32
stable cells at N=1024,1280,1536 = 4/8,4/8,4/8
terminal ordering = frozen > origin > pooled > local
```

All four all-plus cells pass the one-percent origin-spread diagnostic, while
all four alternating-index cells fail it.  The earlier forecast anomaly is
therefore not reproduced on this fresh family, but the origin diagnostic
survives.  These are finite observations; no source-valid growing
normalization, arithmetic advance, Route-A closure, Route-B reassembly, or
twin-prime conclusion is claimed.
