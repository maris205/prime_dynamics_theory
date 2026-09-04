# Bridge B / TPC-385: c=1 bandwidth-phase origin holdout

## Scope

TPC-385 is a finite, response-blind holdout audit on the fresh affine grid
`a_j=2000001+401j`. Indices `(0,10,20,30,40)` are frozen before any response
or metric read. The first three origins define a calibration-only pooled
geometry scalar; the last two origins are held out. The panel crosses
`c=2,3`, `Q=2048,8192`, four declared laws, and local or calibration-pooled
normalization, for 160 rows.

The all-plus `Q=8192` parent phase values from the hash-locked TPC-384
certificate are forecasts. The four holdout forecast errors are all below the
predeclared one-percent cap. The largest holdout spread is
`0.033223638943350384`, from the alternating-index law at `(c,Q)=(3,2048)`
under local normalization, so the transfer is not law-uniform.

## Recorded finite result

    calibration stable cells = 26/32
    holdout stable cells = 28/32
    all-plus high-Q forecast cells = 4/4 within one percent
    spectral failures = 0/160
    Schur failures = 0/160

This is NUMERICALLY_CERTIFIED finite evidence. It does not prove bandwidth,
origin, count, or law uniformity; source-valid normalization; a growing
operator bound; arithmetic `L2`; fixed-power saving; Route-B reassembly; or a
twin-prime result.

## Claim firewall

    TPC385_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
    TPC385_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
    TPC385_PARENT_PHASE_REFERENCE = PROVED_EXACT_FINITE_HASHED
    TPC385_ORIGIN_HOLDOUT_PANEL = NUMERICALLY_CERTIFIED_FINITE_160_ROWS
    TPC385_HOLDOUT_HIGH_Q_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC385_FORECAST_ERROR_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC385_BANDWIDTH_MONOTONICITY = OPEN
    TPC385_LAW_UNIFORMITY = OPEN
    TPC385_ORIGIN_UNIFORMITY = OPEN
    TPC385_COUNT_SCALE_UNIFORMITY = OPEN
    TPC385_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
    TPC385_GROWING_OPERATOR_BOUND = OPEN
    TPC385_SOURCE_UNIFORM_L2 = OPEN
    TPC385_ARITHMETIC_ADVANCE = NO
    TPC385_FIXED_POWER_CREDIT = 0
    TPC385_FULL_GATE_B = OPEN
    TPC385_TWIN_PRIME_RESULT = NONE
    ROUND2_CLUE = TEST_C1_HOLDOUT_COUNT_BANDWIDTH

The Session-named Route-A/Route-B evaluator files are absent in this
checkout. This local Bridge-B is fail-closed repository evidence only.
