# Bridge B: finite admissible source-control atlas

Date: 2026-08-27

TPC-284 follows the unrestricted zeroing-radius obstruction of TPC-283 by
declaring six local schedule controls around each registered baseline:
`H-2`, `H+2`, `z-1`, `z+1`, `Q-1`, and `Q+1`.  Across six scales and two
kernel exponents this is a 72-row literal-source atlas.  Every controlled
attachment interval is separated from zero (60 negative, 12 positive), but
eight rows flip sign relative to the TPC-283 baseline.  The result is finite
and source-locked; it does not claim that these controls exhaust the physical
source class or that the sign pattern is asymptotically stable.

    TPC284_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_ADMISSIBLE_CONTROL_ATLAS_PLUS_SIGN_FLIP_OBSTRUCTION
    TPC284_ROUTE_ADVANCE = YES_SCOPED_FINITE_CONTROL_ATLAS_AND_SIGN_FLIP_OBSTRUCTION
    TPC284_CONTROL_ATLAS = NUMERICALLY_CERTIFIED_FINITE_72_ROWS
    TPC284_CONTROL_SIGN_CENSUS = 60_NEGATIVE_12_POSITIVE_0_CROSSING
    TPC284_SIGN_FLIP_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_8_FLIPS
    TPC284_ASYMPTOTIC_CONTROL_STABILITY = OPEN
    TPC284_LITERAL_SOURCE_CLASS_THEOREM = OPEN
    TPC284_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC284_FIXED_POWER_CREDIT = 0
    TPC284_FULL_GATE_B = OPEN
    TPC284_TWIN_PRIME_RESULT = NONE
    TPC284_STATUS = NUMERICALLY_CERTIFIED_FINITE_ADMISSIBLE_CONTROL_ATLAS_PLUS_SIGN_FLIP_OBSTRUCTION
    TPC284_ROUND2_CLUE = COMPILE_PRIME_SHELL_CONTROL_CONSTRAINTS_BEFORE_ANY_ASYMPTOTIC_STABILITY_CLAIM

The Session-named evaluator files are absent from this checkout.  The local
proof package, theorem ledger, independent replay, stress audit, and this
fail-closed checker are the scoped Route-B fallback.
