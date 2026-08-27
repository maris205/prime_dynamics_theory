# Bridge B: source-attachment stability radius

Date: 2026-08-27

TPC-283 follows the literal source lock of TPC-282.  For a nonzero projected
output S, source representative w, and attachment C=<w,S>, the exact distance
to the zero-attachment hyperplane is

    dist(w,{u:<u,S>=0})^2 = |C|^2/||S||^2,
    relative distance squared = |C|^2/(||w||^2||S||^2).

The nearest zeroing source is w-(C/||S||^2)S.  On all 12 TPC-282 rows the
relative squared radius is below 9/100; on 6 rows it is below 1/100.  This is
an information-model obstruction, not a claim that a prime-shell perturbation
realizes the zeroing direction.

    TPC283_MAXIMUM_CLAIM = PROVED_EXACT_HILBERT_SOURCE_ZEROING_RADIUS_PLUS_NUMERICALLY_CERTIFIED_FINITE_VULNERABILITY_AUDIT
    TPC283_ROUTE_ADVANCE = YES_SCOPED_EXACT_ZEROING_RADIUS_AND_FINITE_VULNERABILITY_AUDIT
    TPC283_ZEROING_RADIUS = PROVED_EXACT
    TPC283_FINITE_VULNERABILITY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
    TPC283_UNRESTRICTED_ADVERSARY = INFORMATION_MODEL_ONLY
    TPC283_ADMISSIBLE_LITERAL_SOURCE_STABILITY = OPEN
    TPC283_FIXED_POWER_CREDIT = 0
    TPC283_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC283_FULL_GATE_B = OPEN
    TPC283_TWIN_PRIME_RESULT = NONE
    TPC283_STATUS = PROVED_EXACT_HILBERT_SOURCE_ZEROING_RADIUS_PLUS_NUMERICALLY_CERTIFIED_FINITE_VULNERABILITY_AUDIT
    TPC283_ROUND2_CLUE = TEST_ADMISSIBLE_LITERAL_SOURCE_CONTROLS_AFTER_UNRESTRICTED_ZEROING_OBSTRUCTION

The Session-named evaluator files are absent from this checkout; the local
proof package, independent replay, stress audit, and this fail-closed checker
are the scoped Route-B fallback.
