# Bridge-B — TPC-381 c=1 law-control origin-family replay

This local bridge is fail-closed repository evidence for the finite TPC-381
origin-family replay.  It is not an official Route-A or Route-B evaluator.

```text
candidate grid = a_j=1400001+401j, 0<=j<41
selected indices = 0,20,40
origins = 1400001,1408021,1416041
count = 2048; eight contiguous blocks of length 256
band = block distance <= 1; beta=2; exponent=1; height=66
Q = 512,2048,8192
laws = all_plus, alternating_index, mod4_character, half_split
rows = 36
```

TPC-381 locks the TPC-380 producer and canonical certificate.  The complete
panel is constructed before the failure census.  The all-plus profile is
`(0,3,3)` and every signed-control profile is `(0,0,0)`, yielding 6/36
spectral-cap failures and 0/36 Schur-cap failures.  The exact q=8 anchor is
`[1400001,1400014)` with shell `[11,13]`; its geometry digest is
`bf086c54b42280dda167bc5dc19f53c45afed4c5a51e0338a9555c65a6474d1f`.

The strongest positive result is finite persistence of the parent profile on a
second fresh coordinate-disjoint panel at count 2048.  The observed law maxima
are `0.66694427563296521`, `0.0077610039910285299`, `0.012055505105884349`,
and `0.21613933977437655` in declaration order.  The strongest obstruction
is that the separation remains specific to the all-plus law.  The result does
not establish law/origin/scale uniformity, source-valid normalization,
cross-block causality, a growing operator bound, arithmetic `L2`, a power
saving, Route-B reassembly, or a twin-prime theorem.

```text
TPC381_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC381_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC381_COMMON_GEOMETRY = PROVED_EXACT_FINITE_LAW_INDEPENDENT
TPC381_LAW_FAMILY = PROVED_EXACT_FINITE_PREDECLARED
TPC381_ORIGIN_FAMILY_REPLAY = NUMERICALLY_CERTIFIED_FINITE_36_ROWS
TPC381_ALL_PLUS_FAILURE_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC381_SIGNED_CONTROL_SUBCAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC381_RAYLEIGH_TAIL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC381_LAW_UNIFORMITY = OPEN
TPC381_ORIGIN_UNIFORMITY = OPEN
TPC381_WINDOW_SCALE_UNIFORMITY = OPEN
TPC381_CROSS_BLOCK_CAUSALITY = OPEN
TPC381_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC381_GROWING_OPERATOR_BOUND = OPEN
TPC381_SOURCE_UNIFORM_L2 = OPEN
TPC381_ARITHMETIC_ADVANCE = NO
TPC381_FIXED_POWER_CREDIT = 0
TPC381_FULL_GATE_B = OPEN
TPC381_TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT
```

The accompanying checker locks this bridge, the project source, certificate,
proof/route notes, and PDF artifacts, then reruns producer, independent
reverse-shell replay, and adversarial stress in normal and optimized modes.
