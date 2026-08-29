# Bridge-B TPC-300 — native budget dual certificate

    TPC300_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_NATIVE_BUDGET_DUALITY_AND_RECIPROCAL_MULTIPLIER_CORRECTION_PLUS_NUMERICALLY_CERTIFIED_FINITE_RATIONAL_DUAL_WITNESS_ATLAS
    TPC300_ROUTE_ADVANCE = YES_SCOPED_PRIMAL_FRONTIER_TO_RATIONAL_DUAL_CERTIFICATE
    TPC300_DUAL_LOWER_BOUND = PROVED_EXACT_FINITE
    TPC300_STRONG_DUALITY_ACTIVE_FRONTIER = PROVED_EXACT_FINITE_SLATER
    TPC300_RIDGE_KKT_RECIPROCITY = PROVED_EXACT_FINITE
    TPC300_TPC299_PARAMETER_LABEL = CORRECTED_SCOPED_RIDGE_PARAMETER_NOT_KKT_MULTIPLIER
    TPC300_RATIONAL_DUAL_WITNESSES = NUMERICALLY_CERTIFIED_FINITE_72_OF_72
    TPC300_DUAL_TIGHTNESS = NUMERICALLY_CERTIFIED_FINITE_72_OF_72_ABOVE_0_999999999
    TPC300_WEIGHTED_THRESHOLD_DUAL_FLOOR = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_9E_MINUS_5
    TPC300_WEIGHTED_THRESHOLD_DUAL_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_14_OF_18_ABOVE_1E_MINUS_3
    TPC300_WEIGHTED_FULL_PREFIX_DUAL_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_11_OF_18_ABOVE_1E_MINUS_3
    TPC300_PROFILE_BUDGET_GROWTH = OPEN
    TPC300_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC300_FIXED_POWER_CREDIT = 0
    TPC300_FULL_GATE_B = OPEN
    TPC300_TWIN_PRIME_RESULT = NONE
    TPC300_STATUS = PROVED_EXACT_FINITE_NATIVE_BUDGET_DUALITY_AND_RECIPROCAL_MULTIPLIER_CORRECTION_PLUS_NUMERICALLY_CERTIFIED_FINITE_RATIONAL_DUAL_WITNESS_ATLAS
    TPC300_ROUND2_CLUE = HOSTILE_TEST_THE_DUAL_BUDGET_GAP_ACROSS_TOLERANCE_AND_SOURCE_NORMALIZATION_LADDERS

TPC-300 is the direct continuation of TPC-299.  It derives a weak dual
lower bound for the native source budget and proves equality at an active
finite frontier.  The KKT multiplier mu and ridge parameter rho satisfy
mu=1/rho.  The frozen TPC-299 ridge interval is converted to a rational rho,
then the exact Fraction linear system and dual fraction are replayed.

The finite audit contains 18 rows, 1,380 shell edges, and 72 cases:
threshold minimum, max-cut, and all-positive targets, plus the weighted
full-prefix target.  All 72 exact fraction and coefficient hashes replay;
the smallest dual-to-parent-primal lower bound is
0.999999999999962310666478.  The weighted dual obstruction counts are
18/18 above 9e-5, 15/18 above 5e-4, 14/18 above 1e-3 at threshold, and
11/18 above 1e-3 at the full prefix.

This is a restricted finite structural certificate.  It does not establish
a growing native budget theorem, arithmetic L2, fixed-power credit, full
Gate B, or the twin-prime conjecture.  The Session-named evaluator files
are absent; the local proof package, exact hashes, independent replay,
stress suite, PDF audit, and this checker are the fail-closed path.

## Local validation

    export PYTHONDONTWRITEBYTECODE=1
    python -B research/tpc-big-road/tpc_bridge_b_tpc300_native_budget_dual_certificate_checker.py --check
