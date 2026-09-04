# Bridge-B note: TPC-392 normalization phase diagram

This is the local fail-closed bridge record for
`papers/tpc-392-c1-normalization-phase-diagram/`.  The official Session
Route-A and Route-B evaluator files are absent from this checkout, so this
note records repository evidence without declaring an official route pass.

```text
TPC392_SCHEMA = TPC392_C1_NORMALIZATION_PHASE_DIAGRAM_V1
TPC392_STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_NORMALIZATION_PHASE_DIAGRAM_AUDIT
SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED_TPC391
NORMALIZATION_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS
SCALAR_DEFINITIONS = PROVED_EXACT_FINITE_DECLARED
PHASE_COMPARISON = NUMERICALLY_CERTIFIED_FINITE_SCOPED
CALIBRATION_FORECAST = NUMERICALLY_CERTIFIED_FINITE_SCOPED
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT
```

## Locked panel

```text
grid = 3800001 + 401*j, j=0,...,40
selected indices = (0,10,20,30,40)
calibration origins = 3800001,3804011,3808021
holdout origins = 3812031,3816041
calibration counts = 1024,1280
holdout count = 1536
block length = 128
band mode = fixed_c3
Q = 2048,8192
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar, origin_scalar,
                 frozen_train_1024_scalar
forecast cap = absolute ratio error <= 0.03
```

## Evidence contract

The producer and independent checker reconstruct all 256 rows and 32 phase
cells.  The independent checker uses descending prime-shell order and does
not import the producer.  The stress program rejects 25 response, provenance,
role, summary, and firewall mutations.  The Bridge-B checker additionally
locks the source, certificate, proof package, notes, PDF pair, compile log,
README, and this bridge note, then runs ordinary and optimized
producer/independent/stress jobs and requires matching output within each
implementation.

The sealed finite census is:

```text
forecast passes (local, pooled, origin, frozen) = 7/8,8/8,8/8,8/8
maximum forecast errors =
  0.034106850682897649, 0.0275714873542654,
  0.028962999969161629, 0.02757148735426429
spectral failures = 64/256; Schur failures = 0/256
stable holdout cells = 24/32
```

The one failing cell is local diagonal, alternating-index, $Q=8192$.
These are finite diagnostics; no source-valid growing normalization,
arithmetic advance, Route-A closure, Route-B reassembly, or twin-prime
conclusion is claimed.
