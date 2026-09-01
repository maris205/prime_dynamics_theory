# Bridge B — TPC-328 source-native arithmetic `L2` cancellation

TPC-328 inserts the finite V59 source-native residual into the literal
deleted-diagonal centered prime-shell operator.  For each declared sign law it
records the exact finite decomposition

    E_e(v) = D_e(v) + O_e(v),

where `D_e` is the source-coordinate diagonal Gram term and `O_e` is the
off-diagonal term.  The panel uses origins `12001`, `16001`, `20001`, scales
`320,640,1280,2560`, `H=66`, `Q={24,36,54,80}`, and exponents `{1,2}`.

The canonical certificate has 96 rows.  For the all-plus residual, `O<0` on
81 rows and `O>0` on 15 rows; the other three declared laws have censuses
`73/23`, `74/22`, and `61/35` (negative/positive), with no unresolved row.
The positive Lambda and comparison component controls are `96/96`.  The exact
anchor `[20001,20016]`, `Q=4`, `s=1` stores all three rational Gram digests.

    TPC328_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_L2_CANCELLATION_ATLAS
    TPC328_EXACT_GRAM_DECOMPOSITION = PROVED_EXACT_FINITE
    TPC328_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC328_COMPONENT_CONTROLS = NUMERICALLY_CERTIFIED_FINITE_96_OF_96
    TPC328_ALL_PLUS_CANCELLATION = NUMERICALLY_CERTIFIED_FINITE_81_OF_96
    TPC328_ALL_PLUS_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_15_OF_96
    TPC328_NO_UNIFORM_SIGNED_CONTRACTION = REFUTED_SCOPED_FOUR_DECLARED_LAWS
    TPC328_ARITHMETIC_ADVANCE = NO
    TPC328_FIXED_POWER_CREDIT = 0
    TPC328_GROWING_SOURCE_NATIVE_L2 = OPEN
    TPC328_FULL_GATE_B = OPEN
    TPC328_TWIN_PRIME_RESULT = NONE
    TPC328_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_L2_CANCELLATION_ATLAS
    TPC328_ROUND2_CLUE = TEST_SOURCE_NATIVE_L2_ON_GROWING_ORIGIN_ENSEMBLE_OR_PROVE_SIGNED_GRAM_BOUND

The producer, independent checker, stress suite, exact rational anchor, PDF
audit, and normal/optimized equality are required by the local fail-closed
Bridge-B checker.  The Session-named official Route-A and Route-B evaluator
files are absent from this checkout, so this record is not an official
evaluator pass.  No growing arithmetic theorem, fixed-power saving, strict
`1/400` payment, or twin-prime conclusion is asserted.
