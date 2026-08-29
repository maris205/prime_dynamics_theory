# Bridge-B TPC-303 - fixed-source cardinality monotonicity obstruction

    TPC303_MAXIMUM_CLAIM = PROVED_EXACT_INTERVAL_DESCENT_CRITERION_PLUS_NUMERICALLY_CERTIFIED_FIXED_SOURCE_CARDINALITY_MONOTONICITY_OBSTRUCTION
    TPC303_ROUTE_ADVANCE = YES_SCOPED_CARDINALITY_ONLY_GROWTH_REFUTATION
    TPC303_INTERVAL_ORDER = PROVED_EXACT_FINITE
    TPC303_CARDINALITY_MONOTONICITY = REFUTED_SCOPED_DECLARED_FINITE_SPINE
    TPC303_TRANSITION_CENSUS = NUMERICALLY_CERTIFIED_FINITE_21_DESCENTS_33_ASCENTS_0_UNRESOLVED
    TPC303_NONMONOTONE_SERIES = NUMERICALLY_CERTIFIED_FINITE_18_OF_18
    TPC303_SAME_PREFIX_DESCENTS = NUMERICALLY_CERTIFIED_FINITE_9
    TPC303_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
    TPC303_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC303_FIXED_POWER_CREDIT = 0
    TPC303_FULL_GATE_B = OPEN
    TPC303_TWIN_PRIME_RESULT = NONE
    TPC303_STATUS = PROVED_EXACT_INTERVAL_DESCENT_CRITERION_PLUS_NUMERICALLY_CERTIFIED_FIXED_SOURCE_CARDINALITY_MONOTONICITY_OBSTRUCTION
    TPC303_ROUND2_CLUE = LOCALIZE_BUDGET_DESCENTS_BY_TRANSPORTING_SIGN_LABELS_ACROSS_OVERLAPPING_SHELLS

TPC-303 freezes `(N,H,z)=(512,58,5)` and compares the moving Q-spine
`50,60,70,90` (shell cardinalities `10,13,15,17`) using TPC-302 common-prefix
weighted budgets.  Across two exponents, three tolerances, and three source
normalizers, 21 of 54 adjacent transitions are strict interval-certified
descents; nine descents have unchanged profile prefix.  This is a controlled
finite obstruction to cardinality-only monotonicity, not an asymptotic
refutation.

The Session-named evaluator files are absent.  The proof package, frozen
interval replay, stress suite, PDF audit, and this checker are the local
fail-closed validation path.
