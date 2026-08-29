# Bridge-B TPC-302 - source-first growing-shell budget gap

    TPC302_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_SOURCE_FIRST_SIGN_ENUMERATION_AND_BUDGET_MONOTONICITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_GRID_AUDIT
    TPC302_ROUTE_ADVANCE = YES_SCOPED_FINITE_GROWING_GRID_SOURCE_FIRST_EXTENSION
    TPC302_SOURCE_FIRST_SIGN_ENUMERATION = PROVED_EXACT_FINITE
    TPC302_PHYSICAL_GRAM_PSD = PROVED_EXACT_FINITE
    TPC302_BUDGET_MONOTONICITY = PROVED_EXACT_FINITE
    TPC302_COMMON_GAP_TAU_025 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10
    TPC302_COMMON_GAP_TAU_050 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10
    TPC302_COMMON_GAP_TAU_075 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10
    TPC302_FULL_GAP_TAU_075 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10
    TPC302_SOURCE_FIRST_LABELS = NUMERICALLY_CERTIFIED_FINITE_34_OF_34
    TPC302_COMMON_BUDGET_FLOOR = NUMERICALLY_CERTIFIED_FINITE_102_OF_102_PER_NORMALIZATION
    TPC302_EXPLICIT_SHELL_TARGET_COUNT = 430
    TPC302_INHERITED_GRID_EDGE_COUNT = 1380
    TPC302_UNIFORM_GROWING_PROFILE_BUDGET = OPEN
    TPC302_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC302_FIXED_POWER_CREDIT = 0
    TPC302_FULL_GATE_B = OPEN
    TPC302_TWIN_PRIME_RESULT = NONE
    TPC302_STATUS = PROVED_EXACT_FINITE_SOURCE_FIRST_SIGN_ENUMERATION_AND_BUDGET_MONOTONICITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_GRID_AUDIT
    TPC302_ROUND2_CLUE = TEST_UNIFORM_NATIVE_BUDGET_GROWTH_OR_CONSTRUCT_A_GROWING_SHELL_COUNTEREXAMPLE

TPC-302 is the source-first continuation of TPC-301.  It rebuilds the
literal physical output Gram on all 34 rows of the TPC-288 growth/control
grid, exhaustively compiles the weighted sign target on each row, and then
repeats the three-tolerance native budget audit.  The common-prefix gap is
above 10 on all rows at all three tolerances.  The explicit shell target count
is 430; the inherited 1,380-edge metadata count is retained separately.

This is a finite structural/numerical advance.  It does not pay a uniform
growing profile-budget theorem, arithmetic L2, fixed-power credit, full Gate B,
or a twin-prime conclusion.  The Session-named evaluator files are absent;
the project proof package, independent source-first replay, stress suite,
PDF audit, and this checker are the local fail-closed validation path.
