# TPC-346 route evaluation

The Session-named `propose.md`, `skills/route-a-evaluator.md`, and
`skills/route-b-evaluator.md` files are absent in this checkout. The result
below is therefore a local fail-closed evaluation, not an official evaluator
pass.

```text
ROUTE_A = OPEN
ROUTE_B = FINITE_CERTIFICATE_ONLY
TPC346_FINITE_RESULT = NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION
TPC346_NESTED_MODEL = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC346_FRESH_OWN_FIT = REFUTED_SCOPED
TPC346_PANEL_ADAPTIVE_RAW = NUMERICALLY_CERTIFIED_FINITE_SCOPED_PASS
TPC346_PANEL_ADAPTIVE_EQUAL_ROW = REFUTED_SCOPED
TPC346_PANEL_ADAPTIVE_WEIGHTING_STABILITY = REFUTED_SCOPED
TPC346_THIRD_PANEL_TRANSFER = REFUTED_SCOPED
TPC346_ARITHMETIC_ADVANCE = NO
TPC346_FIXED_POWER_CREDIT = 0
TPC346_FULL_GATE_B = OPEN
TPC346_TWIN_PRIME_RESULT = NONE
```

Strongest positive: the nested finite model identity and a narrow raw
three-panel adaptive crossing are both independently replayable.

Strongest obstruction: the fresh panel fails its own pooled guard under both
weightings, all transfer diagnostics exceed 0.30, and equal-row weighting
removes the raw adaptive crossing.

Open theorem: a source-uniform arithmetic L2 estimate remains the central
unpaid Gate-B interface.

`ROUND2_CLUE = FREEZE_PANEL_ADAPTIVE_ROUTE_AND_RETURN_TO_ARITHMETIC_L2`.
