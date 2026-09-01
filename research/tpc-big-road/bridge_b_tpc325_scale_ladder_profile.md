# Bridge B — TPC-325 source-scale ladder profile audit

TPC-325 follows the TPC-324 source-location holdout.  It freezes a new source
origin and changes only the nested source cardinality:

    N=320:  [12001,12160]   count=160
    N=640:  [12001,12320]   count=320
    N=1280: [12001,12640]   count=640
    N=2560: [12001,13280]   count=1280

The same H=66, Q={24,36,54,80}, exponents {1,2}, literal
deleted-diagonal centered blocks, and four declared sign laws are used on all
four rungs.  The finite certificate has 32 rows.  All-plus normalized profile
majorization holds on 32/32 rows; the outward lower TV envelope and outward
upper energy envelope both decrease strictly over the four rungs.  The
alternative profile census is all-plus 32/0, alternating 21/11,
mod-4 26/6, and half-split 23/9 (majorizing/mixed).

    TPC325_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT
    TPC325_SCALE_LADDER = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_4_SCALES
    TPC325_ALL_PLUS_SCALE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC325_ALL_PLUS_PROFILE_MAJORISATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC325_TV_ENVELOPE = NUMERICAL_OBSERVATION_STRICTLY_DESCENDING_4_SCALES
    TPC325_ENERGY_ENVELOPE = NUMERICAL_OBSERVATION_STRICTLY_DESCENDING_4_SCALES
    TPC325_ARITHMETIC_ADVANCE = NO
    TPC325_FIXED_POWER_CREDIT = 0
    TPC325_FULL_GATE_B = OPEN
    TPC325_TWIN_PRIME_RESULT = NONE
    TPC325_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT
    TPC325_ROUND2_CLUE = TEST_SCALE_LADDER_SOURCE_REPLICATION_OR_SOURCE_NATIVE_ARITHMETIC_L2

The local checker verifies the parent lock, canonical full-row JSON, exact
small anchor, independent reverse/einsum replay, stress controls, PDF, and
normal/optimized equality.  The Session-named official evaluator files are
absent from this checkout; this is a fail-closed local Bridge-B record and not
an official Route-A/Route-B pass.  No arithmetic L2, power saving, or
twin-prime conclusion is asserted.
