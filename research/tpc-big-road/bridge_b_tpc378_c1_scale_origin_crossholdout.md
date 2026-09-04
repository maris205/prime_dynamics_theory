# Bridge-B — TPC-378 c=1 scale–origin cross-holdout

This is a local fail-closed bridge for TPC-378.  It is repository evidence,
not an official Route-A or Route-B evaluator verdict: the official
Session-named evaluator files are absent from this checkout.

## Frozen object

```text
candidate grid = a_j=1100001+401j, 0<=j<41
selected indices = (0,20,40)
origins = 1100001,1108021,1116041
counts = 1024,2048; nested prefixes; blocks of length 256
band = block distance <= 1 (inherited c=1)
Q = 512,2048,8192
kernel = exponent 1, height 66
law = all_plus, beta 2
normalization = scale-wise full-window square-energy geometry
caps = spectral 0.64, Schur 0.83
```

The selection is response-blind and the full 18-row Cartesian panel is built
before its profile is read.  Exact integer endpoint comparisons separate the
current intervals from the largest declared TPC-376/TPC-377 intervals.

## Finite result and firewall

```text
profile by count and Q = (0,3,3); (0,3,3)
spectral failures = 12/18
Schur failures = 0/18
absolute retention = 0.93759972206138864--0.98046528117382914
maximum tail fraction = 0.062400277938610291
```

The parent support pattern therefore transfers to this finite fresh-origin
panel.  The result remains a threshold census with count-specific
normalization and does not establish origin/scale uniformity, a causal
cross-block interpretation, a growing operator theorem, an arithmetic
estimate, Route-B reassembly, or a twin-prime result.

```text
TPC378_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC378_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC378_COMMON_BAND_RULE = PROVED_EXACT_FINITE_INHERITED
TPC378_SCALE_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC378_C1_PROFILE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC378_PARENT_PROFILE_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC378_RAYLEIGH_TAIL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC378_ORIGIN_UNIFORMITY = OPEN
TPC378_WINDOW_SCALE_UNIFORMITY = OPEN
TPC378_SPECTRAL_MAGNITUDE_UNIFORMITY = OPEN
TPC378_CROSS_BLOCK_CAUSALITY = OPEN
TPC378_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC378_GROWING_OPERATOR_BOUND = OPEN
TPC378_SOURCE_UNIFORM_L2 = OPEN
TPC378_ARITHMETIC_ADVANCE = NO
TPC378_FIXED_POWER_CREDIT = 0
TPC378_FULL_GATE_B = OPEN
TPC378_TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_CROSSHOLDOUT_LAW_CONTROL
```

## Reproduction contract

The Bridge-B checker locks the producer, independent checker, stress suite,
certificate, proof package, route notes, paper source, both PDF names, the
compile log, and the package README.  It then runs producer, independent
reverse-shell replay, and mutation stress in normal and optimized Python
modes.  Every subcheck must return zero, emit empty standard error, and have
byte-identical normal/optimized summary output.
