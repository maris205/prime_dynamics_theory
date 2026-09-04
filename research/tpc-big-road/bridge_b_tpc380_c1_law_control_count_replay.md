# Bridge-B — TPC-380 c=1 law-control count replay

This local bridge is fail-closed repository evidence for the finite TPC-380
count replay.  It is not an official Route-A or Route-B evaluator.

```text
candidate grid = a_j=1300001+401j, 0<=j<41
selected indices = 0,20,40
origins = 1300001,1308021,1316041
count = 2048; eight contiguous blocks of length 256
band = block distance <= 1; beta=2; exponent=1; height=66
Q = 512,2048,8192
laws = all_plus, alternating_index, mod4_character, half_split
rows = 36
```

TPC-380 locks the TPC-379 producer and canonical certificate.  The complete
panel is constructed before the failure census.  The all-plus profile is
`(0,3,3)` and every signed-control profile is `(0,0,0)`, yielding 6/36
spectral-cap failures and 0/36 Schur-cap failures.  The exact q=8 anchor is
`[1300014,1300027)` with shell `[11,13]`; its geometry digest is
`d17b892caed9169be686d11e0e20cec8397e14834693e47a83fd972cb2423bd5`.

The strongest positive result is finite persistence of the parent profile at
count 2048 on a fresh coordinate-disjoint panel.  The strongest obstruction
is that the separation remains specific to the all-plus law.  The result does
not establish law/origin/scale uniformity, source-valid normalization,
cross-block causality, a growing operator bound, arithmetic `L2`, a power
saving, Route-B reassembly, or a twin-prime theorem.

```text
TPC380_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC380_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC380_COMMON_GEOMETRY = PROVED_EXACT_FINITE_LAW_INDEPENDENT
TPC380_LAW_FAMILY = PROVED_EXACT_FINITE_PREDECLARED
TPC380_COUNT_REPLAY = NUMERICALLY_CERTIFIED_FINITE_36_ROWS
TPC380_ALL_PLUS_FAILURE_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC380_SIGNED_CONTROL_SUBCAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC380_RAYLEIGH_TAIL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC380_LAW_UNIFORMITY = OPEN
TPC380_ORIGIN_UNIFORMITY = OPEN
TPC380_WINDOW_SCALE_UNIFORMITY = OPEN
TPC380_CROSS_BLOCK_CAUSALITY = OPEN
TPC380_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC380_GROWING_OPERATOR_BOUND = OPEN
TPC380_SOURCE_UNIFORM_L2 = OPEN
TPC380_ARITHMETIC_ADVANCE = NO
TPC380_FIXED_POWER_CREDIT = 0
TPC380_FULL_GATE_B = OPEN
TPC380_TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY
```

The accompanying checker locks this bridge, the project source, certificate,
proof/route notes, and PDF artifacts, then reruns producer, independent
reverse-shell replay, and adversarial stress in normal and optimized modes.
