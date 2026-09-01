# Bridge B — TPC-327 three-origin scale-ladder triangulation

TPC-327 repeats the frozen TPC-325/TPC-326 four-rung source-scale ladder at
the third disjoint origin `20001`.  The new intervals are

    N=320:  [20001,20160]
    N=640:  [20001,20320]
    N=1280: [20001,20640]
    N=2560: [20001,21280]

The literal `H=66` deleted-diagonal centered blocks, shell anchors
`{24,36,54,80}`, exponents `{1,2}`, and four declared sign laws are frozen.
The new certificate has 32 rows.  All-plus profile majorization holds on
32/32 rows; the four-law profile and energy censuses match both earlier
origins.  Pooling origins `12001`, `16001`, and `20001` gives maximum finite
TV range `0.0007970083067065925 < 0.001` and maximum finite energy range
`0.004551841150018276 < 0.005`; each range is nonzero.

    TPC327_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION
    TPC327_THREE_ORIGIN_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_3_ORIGINS
    TPC327_ALL_PLUS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32_NEW_ORIGIN
    TPC327_CENSUS_MATCH = NUMERICALLY_CERTIFIED_FINITE_MATCH_TO_BOTH_PARENTS
    TPC327_ENVELOPE_TRIANGULATION = NUMERICALLY_CERTIFIED_FINITE_WITHIN_DECLARED_THRESHOLDS
    TPC327_ARITHMETIC_ADVANCE = NO
    TPC327_FIXED_POWER_CREDIT = 0
    TPC327_FULL_GATE_B = OPEN
    TPC327_TWIN_PRIME_RESULT = NONE
    TPC327_STATUS = NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION
    TPC327_ROUND2_CLUE = TEST_ORIGIN_ENSEMBLE_SCALE_GROWTH_OR_SOURCE_NATIVE_ARITHMETIC_L2

The producer, independent reverse/einsum checker, stress suite, exact anchor,
PDF audit, and normal/optimized equality are checked locally.  The
Session-named official Route-A and Route-B evaluator files are absent from
this checkout; this is a fail-closed local Bridge-B record, not an official
evaluator pass.  No source-uniform theorem, arithmetic `L2` estimate,
fixed-power saving, or twin-prime conclusion is asserted.
