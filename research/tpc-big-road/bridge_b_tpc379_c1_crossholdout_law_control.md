# Bridge-B — TPC-379 c=1 cross-holdout law control

This is a local fail-closed bridge for TPC-379. It is repository evidence,
not an official Route-A or Route-B evaluator verdict: the official
Session-named evaluator files are absent from this checkout.

## Frozen object

```text
candidate grid = a_j=1200001+401j, 0<=j<41
selected indices = (0,20,40)
origins = 1200001,1208021,1216041
count = 1024; four contiguous blocks of length 256
band = block distance <= 1 (c=1)
Q = 512,2048,8192
kernel = exponent 1, height 66, beta 2
laws = all_plus, alternating_index, mod4_character, half_split
normalization = one common full-window square-energy geometry
caps = spectral 0.64, Schur 0.83
```

The origin grid, four laws, and complete 36-row Cartesian panel are fixed
before any response or metric is read. Exact endpoint inequalities separate
the six current intervals from the largest declared TPC-376--378 intervals.
The exact anchor `[1200001,1200014)` at `Q=8` has shell `[11,13]` and checks
positive common geometry and symmetry for all four laws.

## Finite result and claim firewall

```text
all_plus profile = (0,3,3)
alternating_index profile = (0,0,0)
mod4_character profile = (0,0,0)
half_split profile = (0,0,0)
spectral failures = 6/36
Schur failures = 0/36
band spectral maxima =
  0.65334758792533143 / 0.0094084540584888146 /
  0.011835976723613296 / 0.2117349490215118
```

The strongest positive result is a complete finite, response-blind,
coordinate-disjoint law-control panel on one common geometry. The strongest
obstruction is that the all-plus high-Q signature disappears under every
declared signed control. This refutes only the scoped finite hypothesis that
the signature is law-invariant; it does not identify an arithmetic law.

```text
TPC379_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC379_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC379_COMMON_GEOMETRY = PROVED_EXACT_FINITE_LAW_INDEPENDENT
TPC379_LAW_FAMILY = PROVED_EXACT_FINITE_PREDECLARED
TPC379_LAW_CONTROL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_36_ROWS
TPC379_ALL_PLUS_FAILURE_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC379_SIGNED_CONTROL_SUBCAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC379_RAYLEIGH_TAIL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC379_LAW_UNIFORMITY = OPEN
TPC379_ORIGIN_UNIFORMITY = OPEN
TPC379_WINDOW_SCALE_UNIFORMITY = OPEN
TPC379_CROSS_BLOCK_CAUSALITY = OPEN
TPC379_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC379_GROWING_OPERATOR_BOUND = OPEN
TPC379_SOURCE_UNIFORM_L2 = OPEN
TPC379_ARITHMETIC_ADVANCE = NO
TPC379_FIXED_POWER_CREDIT = 0
TPC379_FULL_GATE_B = OPEN
TPC379_TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_LAW_CONTROL_COUNT_REPLAY
```

## Reproduction contract

The Bridge-B checker locks the producer, independent replay, stress suite,
certificate, proof package, route notes, paper source, both PDF names, the
compile log, and the package README. It then runs producer, independent
reverse-shell replay, and 25-mutation stress in normal and optimized Python
modes. Every subcheck must return zero, emit empty standard error, and have
byte-identical normal/optimized summary output.
