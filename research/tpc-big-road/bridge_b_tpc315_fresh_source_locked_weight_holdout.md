# Bridge B / TPC-315 — fresh-source locked-weight holdout

## Route position

TPC-314 showed that the finite below/above-one class survived three positive
weight laws, but its target labels were inherited from the TPC-312 panel and
its amplitude order was not canonical.  TPC-315 freezes that three-law menu
first, then moves the literal rational engine to the fresh source interval
`I=(640,1280]` and recomputes every Gram minimum and all-positive control from
the new physical panel.

The eight rows use `Q={24,36,54,80}` and kernel exponents `{1,2}`.  The three
laws are counting `1`, reduced-residue `1/(p-1)`, and prime von Mangoldt
`log(p)`.  The logarithm is enclosed by a 120-term range-reduced atanh series
with a positive rational tail, and all weighted quadratic forms are propagated
outward on a `10^-36` decimal grid.  This gives 48 finite law/target cases:
24 fresh minima are strictly below one and 24 all-positive controls are
strictly above one.

The holdout reproduces the coarse class on all eight fresh rows, but the
fine law ordering changes.  Minimum orders have three strict types
(`L<C<R` on six rows, one `R<C<L`, and one `C<L<R`); positive controls have
two strict types (`R<C<L` on six rows and `L<R<C` on two).  Thus the robust
finite statement is a class replication, while a canonical amplitude law is
obstructed.  The physical engine is the same locked TPC-268 engine, so this
is not an external data holdout and carries no asymptotic or twin-prime
credit.

## Claim firewall

    TPC315_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_FRESH_SOURCE_LOCKED_WEIGHT_MENU_HOLDOUT_REPLICATION_AND_LAW_ORDER_SHIFT
    TPC315_ROUTE_ADVANCE = YES_SCOPED_FRESH_SOURCE_CLASS_REPLICATION_AND_ORDER_OBSTRUCTION
    TPC315_FRESH_SOURCE_TARGET_RECOMPUTATION = PROVED_EXACT_FINITE_8_ROWS
    TPC315_LOCKED_WEIGHT_MENU = PROVED_EXACT_FINITE_PRE_TARGET
    TPC315_LOG_ATANH_ENCLOSURE = PROVED_EXACT_FINITE_120_TERMS
    TPC315_DIRECTED_INTERVAL_PROPAGATION = PROVED_EXACT_FINITE_GRID_1E_MINUS_36
    TPC315_MINIMUM_BELOW_ONE = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC315_POSITIVE_ABOVE_ONE = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC315_HOLDOUT_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_8_OF_8
    TPC315_MINIMUM_LAW_ORDER_SHIFT = NUMERICALLY_CERTIFIED_FINITE_3_TYPES
    TPC315_POSITIVE_LAW_ORDER_SHIFT = NUMERICALLY_CERTIFIED_FINITE_2_TYPES
    TPC315_EXTERNAL_INDEPENDENCE = NONE_SAME_LOCKED_ENGINE
    TPC315_TARGET_GENERATION_LEAKAGE = FRESH_SOURCE_GRAM_DEPENDENT_LABELS
    TPC315_CANONICAL_WEIGHTING = OPEN
    TPC315_FRESH_PHYSICAL_HOLDOUT = NONE_SAME_LOCKED_ENGINE
    TPC315_UNIFORM_GROWING_WEIGHTED_THEOREM = OPEN
    TPC315_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC315_FIXED_POWER_CREDIT = 0
    TPC315_FULL_GATE_B = OPEN
    TPC315_TWIN_PRIME_RESULT = NONE
    TPC315_STATUS = PROVED_EXACT_FINITE_FRESH_SOURCE_LOCKED_WEIGHT_MENU_HOLDOUT_REPLICATION_AND_LAW_ORDER_SHIFT
    TPC315_STRONGEST_POSITIVE = FRESH_8_OF_8_CLASS_REPLICATION_WITH_48_EXACT_INTERVAL_CASES
    TPC315_STRONGEST_OBSTRUCTION = FRESH_LAW_ORDER_IS_NOT_STABLE_OR_CANONICAL
    TPC315_OPEN_THEOREM = LITERAL_ARITHMETIC_L2_BOUND_FOR_THE_FRESH_PHYSICAL_PANEL
    TPC315_REUSABLE_STRUCTURE = PRE_TARGET_MENU_LOCK_PLUS_FRESH_GRAM_EXTREMUM_AND_OUTWARD_LAW_AUDIT
    TPC315_ROUND2_CLUE = PROBE_LITERAL_ARITHMETIC_L2_INTERFACE_ON_THE_FRESH_PANEL_BEFORE_ANY_GROWING_CLAIM

The Session-named Route-A/Route-B evaluator files are absent from the
checkout.  The project checker below is a local fail-closed fallback and
makes no official evaluator-pass claim.

## Artifacts

    papers/tpc-315-fresh-source-locked-weight-holdout/README.md
    papers/tpc-315-fresh-source-locked-weight-holdout/PROOF_PACKAGE.md
    papers/tpc-315-fresh-source-locked-weight-holdout/results/tpc315_certificate.json
    papers/tpc-315-fresh-source-locked-weight-holdout/paper/paper.pdf
