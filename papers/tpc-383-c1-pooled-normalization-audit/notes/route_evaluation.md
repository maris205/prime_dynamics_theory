# TPC-383 route evaluation

The official Session evaluator files are absent from this checkout.  This is
local fail-closed evidence, not an official Route-A/Route-B verdict.

```text
rows = 72 (3 origins x 3 Q x 4 laws x 2 normalizations)
local stable cells = 9/12
pooled stable cells = 9/12
all-plus high-Q transfer = TRUE
pooled/local all-plus high-Q relative shift = 0.036457251256851203
arithmetic advance = NO
fixed power credit = 0
full Gate B = OPEN
```

The strongest positive result is transfer of all-plus high-Q origin stability
to a common pooled scalar normalization.  The strongest obstruction is the
nonzero absolute calibration shift and the continuing law-dependent instability
of alternating-index.  Reusable structure: fresh affine holdout, common raw
geometry, two law-independent normalizations, complete law/Q panel, and
reverse-shell replay.  Next clue:
`TEST_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM`.
