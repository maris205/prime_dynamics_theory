# Bridge-B: TPC-382 finite origin-family magnitude audit

This is a local, fail-closed repository bridge for the TPC-382 certificate
aggregation.  The Session-named official evaluator files are absent from this
checkout, so this bridge does not assert an official Route-A or Route-B pass.

```text
finite object = hash-locked aggregation of TPC379, TPC380, and TPC381 rows
same-count cohort = TPC380/TPC381, N=2048, 72 values, 12 cells
scale control = TPC379, N=1024, 36 values
relative-spread cap = 0.01, fixed before aggregation
all-plus high-Q same-count spread = 8.0645464844910632e-06
same-count stable cells = 8/12
all-plus high-Q scale contrast = 0.020813995160269608
```

The positive result is finite all-plus high-Q magnitude stability across six
protocol-matched origins.  The obstruction is law-dependent spread together
with failure of the narrowly stated one-percent cross-count hypothesis.  No
source-valid law, origin/scale uniformity, arithmetic power credit, growing
operator estimate, or twin-prime result is claimed.

```text
TPC382_PARENT_LOCKS = PROVED_EXACT_FINITE_HASHED
TPC382_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_CERTIFICATE_BLIND
TPC382_SAME_N_ORIGIN_MAGNITUDE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_72_VALUES
TPC382_ALL_PLUS_HIGH_Q_STABILITY_1PCT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC382_LAW_DEPENDENT_MAGNITUDE_SPREAD = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC382_CROSS_COUNT_MAGNITUDE_INVARIANCE = REFUTED_FINITE_SCOPED
TPC382_ORIGIN_UNIFORMITY = OPEN
TPC382_WINDOW_SCALE_UNIFORMITY = OPEN
TPC382_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC382_GROWING_OPERATOR_BOUND = OPEN
TPC382_SOURCE_UNIFORM_L2 = OPEN
TPC382_ARITHMETIC_ADVANCE = NO
TPC382_FIXED_POWER_CREDIT = 0
TPC382_FULL_GATE_B = OPEN
TPC382_TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_POOLED_NORMALIZATION_CROSS_ORIGIN
```

The checker below locks every project artifact except its own source, runs the
producer, independent checker, and adversarial stress suite in normal and
optimized modes, and requires byte-identical outputs.
