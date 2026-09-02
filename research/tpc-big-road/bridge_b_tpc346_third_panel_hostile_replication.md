# Bridge-B fallback: TPC-346 third-panel hostile replication

This is a local, fail-closed bridge record for the TPC-346 finite
third-panel audit. The Session-named Route-A/Route-B evaluator files are
absent in this checkout, so this record is not an official evaluator pass.

```text
TPC346_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION
TPC346_NESTED_MODEL_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC346_FRESH_PANEL_OWN_FIT = REFUTED_SCOPED
TPC346_SHARED_THREE_PANEL = REFUTED_SCOPED
TPC346_PANEL_ADAPTIVE_RAW = NUMERICALLY_CERTIFIED_FINITE_SCOPED_PASS
TPC346_PANEL_ADAPTIVE_EQUAL_ROW = REFUTED_SCOPED
TPC346_PANEL_ADAPTIVE_WEIGHTING_STABILITY = REFUTED_SCOPED
TPC346_THIRD_PANEL_TRANSFER = REFUTED_SCOPED
TPC346_ARITHMETIC_ADVANCE = NO
TPC346_FIXED_POWER_CREDIT = 0
TPC346_SOURCE_UNIFORM_L2 = OPEN
TPC346_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC346_FULL_GATE_B = OPEN
TPC346_TWIN_PRIME_RESULT = NONE
TPC346_ROUND2_CLUE = FREEZE_PANEL_ADAPTIVE_ROUTE_AND_RETURN_TO_ARITHMETIC_L2
TPC346_STATUS = NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION
```

The fresh panel is `[44097,44609,45217]`, disjoint from both parent panels
and cutoff-safe. Its own pooled retentions are `0.3159173453264` (raw) and
`0.3294074740697` (equal-row). The three-panel adaptive retentions are
`0.2999630725662` and `0.3222362713305`; the raw crossing is therefore not
weighting-stable.

All six directed predictions, all three leave-one-panel-out predictions, and
all eighteen fresh control-LOO projections exceed the `0.30` prediction/model
guard under both weightings. The exact nested-model identity is finite linear
algebra only. No arithmetic advance, fixed-power credit, strict `1/400`
payment, or twin-prime conclusion is licensed.
