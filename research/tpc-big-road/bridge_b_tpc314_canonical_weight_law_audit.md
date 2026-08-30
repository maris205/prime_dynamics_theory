# Bridge B / TPC-314 — externally motivated weight-law audit

## Route position

TPC-312 supplied a new finite source--shell Gram/sign panel, and TPC-313
closed its finite profile-budget interface with outward-rounded rational
certificates.  TPC-314 audits the next unresolved modeling choice: the
weighting law.  It freezes the eight TPC-312 physical rows and compares
counting weight 1, reduced-residue weight 1/(p-1), and prime
von-Mangoldt weight log(p).

The first two laws are rational.  The logarithmic law is enclosed by a
120-term range-reduced atanh series with a positive geometric tail bound; the
weighted numerator, denominator, and ratio are then propagated on a 10^-36
decimal grid.  There are 48 target/law cases.  All 24 inherited Gram-minimum
targets have ratio interval strictly below one, and all 24 all-positive
controls have ratio interval strictly above one.

The finite class is robust, but the amplitude is not: the minimum-law order
has one counting/log crossover, and the positive-control law order has four
strict order types.  The target labels remain source-first TPC-312 Gram
minima, and the physical panel is not an external holdout.

## Claim firewall

    TPC314_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_EXTERNALLY_MOTIVATED_WEIGHT_LAW_ENCLOSURE_AND_NEW_PANEL_ROBUSTNESS_AUDIT
    TPC314_ROUTE_ADVANCE = YES_SCOPED_FINITE_WEIGHT_CLASS_ROBUSTNESS
    TPC314_WEIGHTED_GRAM_IDENTITY = PROVED_EXACT_FINITE
    TPC314_LOG_ATANH_ENCLOSURE = PROVED_EXACT_FINITE_120_TERMS
    TPC314_DIRECTED_INTERVAL_PROPAGATION = PROVED_EXACT_FINITE_GRID_1E_MINUS_36
    TPC314_MINIMUM_BELOW_ONE = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC314_POSITIVE_ABOVE_ONE = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC314_MINIMUM_ORDER = NUMERICALLY_CERTIFIED_FINITE_7_OF_8_LOG_LT_COUNT_LT_RECIP_ONE_CROSSOVER
    TPC314_POSITIVE_ORDER = NUMERICALLY_CERTIFIED_FINITE_8_OF_8_FOUR_ORDER_TYPES
    TPC314_EXTERNAL_INDEPENDENCE = NONE_SAME_LOCKED_ENGINE
    TPC314_TARGET_GENERATION_LEAKAGE = INHERITED_TPC312_SOURCE_FIRST_GRAM_LABEL
    TPC314_CANONICAL_WEIGHTING = OPEN
    TPC314_FRESH_PHYSICAL_HOLDOUT = OPEN
    TPC314_UNIFORM_GROWING_WEIGHTED_THEOREM = OPEN
    TPC314_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC314_FIXED_POWER_CREDIT = 0
    TPC314_FULL_GATE_B = OPEN
    TPC314_TWIN_PRIME_RESULT = NONE
    TPC314_STATUS = PROVED_EXACT_FINITE_EXTERNALLY_MOTIVATED_WEIGHT_LAW_ENCLOSURE_AND_NEW_PANEL_ROBUSTNESS_AUDIT
    TPC314_STRONGEST_POSITIVE = 24_MINIMUM_PLUS_24_POSITIVE_CASES_RETAIN_CLASS
    TPC314_STRONGEST_OBSTRUCTION = LAW_DEPENDENT_AMPLITUDE_ORDER
    TPC314_OPEN_THEOREM = LOCK_MENU_ON_FRESH_SOURCE_AND_RECOMPUTE_TARGETS
    TPC314_REUSABLE_STRUCTURE = WEIGHTED_GRAM_TO_RATIONAL_LOG_INTERVAL_TO_CLASS_FIREWALL
    TPC314_ROUND2_CLUE = REPLICATE_THE_LOCKED_WEIGHT_LAW_MENU_ON_A_FRESH_SOURCE_INTERVAL_WITH_WEIGHTS_FIXED_BEFORE_TARGET_RECOMPUTATION

The Session-named Route-A/Route-B evaluator files are absent from the
checkout.  The project checker below is a local fail-closed fallback and
makes no official evaluator-pass claim.

## Artifacts

    papers/tpc-314-canonical-weight-law-audit/README.md
    papers/tpc-314-canonical-weight-law-audit/PROOF_PACKAGE.md
    papers/tpc-314-canonical-weight-law-audit/results/tpc314_certificate.json
    papers/tpc-314-canonical-weight-law-audit/paper/paper.pdf
