# Bridge B / TPC-384: finite bandwidth--normalization phase diagram

## Scope

TPC-384 is a finite, response-blind audit on the fresh affine grid
\(a_j=1800001+401j\). Indices \(0,20,40\) are frozen before any response or
metric read, giving origins \(1800001,1808021,1816041\). The panel crosses
\(c=0,1,2,3\), local-diagonal and pooled-scalar normalization, four declared
laws, and \(Q=512,2048,8192\), for 288 rows.

The raw centered divisibility components and square-energy geometry are shared
across the bandwidth phase. The exact q=8 anchor is
\([1800001,1800014)\) with shell \([11,13]\), checked rationally.

## Recorded finite result

Stable cells:

    c0 local/pooled = 6/12, 7/12
    c1 local/pooled = 8/12, 7/12
    c2 local/pooled = 8/12, 8/12
    c3 local/pooled = 8/12, 8/12
    spectral failures = 0/288
    Schur failures = 0/288
    all-plus pooled high-Q mean: 0.36656315295619812 -> 0.63888760360944985

This is NUMERICALLY_CERTIFIED finite evidence. It does not prove bandwidth
monotonicity, source-valid normalization, a growing operator bound, arithmetic
L2, fixed-power saving, Route-B reassembly, or a twin-prime result.

## Claim firewall

    TPC384_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
    TPC384_BANDWIDTH_PHASE_PANEL = NUMERICALLY CERTIFIED FINITE_288_ROWS
    TPC384_BANDWIDTH_MONOTONICITY = OPEN
    TPC384_ARITHMETIC_ADVANCE = NO
    TPC384_FIXED_POWER_CREDIT = 0
    TPC384_FULL_GATE_B = OPEN
    TPC384_TWIN_PRIME_RESULT = NONE
    ROUND2_CLUE = TEST_C1_BANDWIDTH_ORIGIN_HOLDOUT

The Session-named Route-A/Route-B evaluator files are absent in this checkout.
The accompanying local checker is deliberately fail-closed and is repository
evidence only.

## Audit contract

The checker locks every source, result, proof note, and PDF; checks the
canonical certificate and exact anchor; then runs producer, independent
reverse-shell replay, and adversarial mutation checks in normal and optimized
Python modes. Normal and optimized outputs must be byte-identical.
