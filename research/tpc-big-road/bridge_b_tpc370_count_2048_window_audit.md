# Bridge-B — TPC-370 count-2048 finite-window audit

## Scope

This bridge records the finite, fail-closed audit for
`papers/tpc-370-count-2048-window-audit/`. It is a local repository bridge,
not the absent official Route-A/Route-B evaluator.

## Frozen protocol

The candidate origins `(1010001,1018021,1026041)` are indices `(0,20,40)` in
the response-blind grid `1010001+401j`. The grid, indices, count 2048, shell
anchors `512,2048,8192`, exponent one, four fixed laws, and beta `0,2` are
fixed before signed response, source data, law scores, or geometry ranking.
The Cartesian product has 72 rows. The exact anchor
`[1010346,1010359)` at `Q=4` and shell `{5,7}` is inherited from TPC-369 by
hash-locked declaration and is not used for main-panel selection.

## Certified finite result

```text
TPC370_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND
TPC370_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC370_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_72_ROWS
TPC370_COUNT_2048_WINDOW = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC370_BETA2_PHASE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC370_BETA2_PARENT_SIGNATURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC370_ORIGIN_UNIFORMITY = OPEN
TPC370_WINDOW_UNIFORMITY = OPEN
TPC370_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC370_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC370_GROWING_OPERATOR_BOUND = OPEN
TPC370_SOURCE_UNIFORM_L2 = OPEN
TPC370_ARITHMETIC_ADVANCE = NO
TPC370_FIXED_POWER_CREDIT = 0
TPC370_FULL_GATE_B = OPEN
TPC370_TWIN_PRIME_RESULT = NONE
```

Beta=2 has 6 spectral-cap and 0 Schur-cap violations in 36 rows; beta=0 has
9 and 9. The six beta=2 failures are precisely the three declared origins at
count 2048, `Q=2048` and `8192`, exponent one, all-plus law. After removing
the count coordinate, this support matches the TPC-369 parent signature. The
beta=2 maximum is `0.71099989528234753`, compared with the parent value
`0.67410489800609708`; the finite difference is
`0.036894997276250452`. Support persistence therefore does not establish
magnitude stability or an asymptotic statement.

## Local acceptance rule

`tpc_bridge_b_tpc370_count_2048_window_audit_checker.py` locks every
claim-bearing project file, validates the canonical certificate, parent
signature, inherited exact anchor, and paper diagnostics, and runs the
producer, independent reverse-shell checker, and adversarial stress checker
in normal and optimized modes. Each subprocess must return zero with empty
stderr, and normal and optimized stdout must be byte-identical. A passing
bridge is finite evidence only: it does not pay arithmetic or fixed-power
credit and does not close Gate B.

```text
ROUND2_CLUE = TEST_COUNT_2048_PHASE_LOCALIZATION
```
