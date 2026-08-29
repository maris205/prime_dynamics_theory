# TPC-300 — Native budget dual certificates

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-300 turns the TPC-299 native source-budget frontier into a target-space
dual certificate.  For every positive ridge parameter rho,

    D_rho=(||b||^2-R^2-b^T Vc_rho)/rho <= B_R(b),

where (V^T V+rho M)c_rho=V^T b; at the active frontier the inequality is an
equality and the KKT multiplier is mu=1/rho.  This explicitly corrects the
otherwise ambiguous use of “multiplier” in TPC-299 without changing any
TPC-299 budget value.

On the inherited 18-row, 1,380-edge finite grid, 72 exact rational dual
certificates (three threshold targets and one full-prefix weighted target per
row) all pass independent source-first replay.  Their dual lower bounds retain
the TPC-299 obstruction counts: weighted threshold budgets exceed 9e-5,
5e-4, and 1e-3 on 18/18, 15/18, and 14/18 rows, while full-prefix weighted
budgets exceed 1e-3 on 11/18 rows.  The smallest dual/primal ratio lower bound
is 0.9999999999999623.

## Claim firewall

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

## Reproduction

    export PYTHONDONTWRITEBYTECODE=1
    python -B code/tpc300_native_budget_dual_certificate.py --write
    python -B code/tpc300_native_budget_dual_certificate.py --check
    python -B experiments/tpc300_independent_checker.py
    python -B experiments/tpc300_dual_stress.py

The manuscript is in paper/paper.pdf.  The Session-named Route-A/Route-B
evaluator files are absent from this checkout; the local proof, exact-fraction
hashes, source-first replay, stress suite, PDF audit, and Bridge-B checker are
the available fail-closed validation path.
