# Bridge B — TPC-326 cross-origin scale-ladder replication

TPC-326 repeats the complete TPC-325 source-scale ladder at a second,
disjoint origin.  The origin changes from 12001 to 16001; the four source
counts remain 160, 320, 640, 1280, with

    N=320:  [16001,16160]
    N=640:  [16001,16320]
    N=1280: [16001,16640]
    N=2560: [16001,17280]

The literal H=66 deleted-diagonal centered blocks, shell anchors
{24,36,54,80}, exponents {1,2}, and four declared sign laws are frozen.
The new certificate has 32 rows.  All-plus profile majorization holds on
32/32 rows; the full profile and energy-side censuses match TPC-325; and the
new all-plus TV and energy envelopes agree with the parent under finite
thresholds 0.001 and 0.005.

    TPC326_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_ORIGIN_SCALE_LADDER_REPLICATION
    TPC326_CROSS_ORIGIN_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_2_ORIGINS
    TPC326_ALL_PLUS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC326_CENSUS_MATCH = NUMERICALLY_CERTIFIED_FINITE_PARENT_MATCH
    TPC326_ENVELOPE_AGREEMENT = NUMERICALLY_CERTIFIED_FINITE_WITHIN_DECLARED_THRESHOLDS
    TPC326_ARITHMETIC_ADVANCE = NO
    TPC326_FIXED_POWER_CREDIT = 0
    TPC326_FULL_GATE_B = OPEN
    TPC326_TWIN_PRIME_RESULT = NONE
    TPC326_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_ORIGIN_SCALE_LADDER_REPLICATION
    TPC326_ROUND2_CLUE = TEST_CROSS_ORIGIN_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2

The local checker verifies both parent and child provenance, canonical
full-row JSON, the exact rational anchor, independent reverse/einsum replay,
cross-origin stress controls, PDF hygiene, and normal/optimized equality.
The Session-named official evaluator files are absent from this checkout, so
this remains a fail-closed local Bridge-B record rather than an official
Route-A/Route-B pass.  No source-uniform theorem, arithmetic L2 estimate,
power saving, or twin-prime conclusion is asserted.
