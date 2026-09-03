# TPC-366 route evaluation and proof boundary

## Strongest positive result

With beta=2 frozen before the signed replay, every one of 240 beta=2 rows on
the new five-anchor ladder through `Q=8192` stays below both finite working
caps.  The same protocol's beta=0 control has 60 spectral and 60 Schur
violations.  The result is independently reproduced in reverse shell order.

## Strongest obstruction

The beta=2 maximum rises from `0.61633188509480319` to
`0.62448287758976528`; no monotone decay is visible or claimed.  The origins
are geometry-selected, the panel is finite, and the normalization has no
source-valid arithmetic derivation.  Passing a finite ladder therefore does
not close a growing operator bound or source-uniform `L2` gate.

## Route decision

`TPC366_STATUS = NUMERICALLY_CERTIFIED_FINITE_BETA2_HIGHER_Q_LADDER`.

`ARITHMETIC_ADVANCE=NO`, `FIXED_POWER_CREDIT=0`, and
`FULL_GATE_B=OPEN`.  Official Route-A/Route-B evaluator files are absent, so
no official pass is asserted.  The next minimal test is to hold beta=2 fixed
while using longer windows and predeclared or unselected origins, attacking
the remaining geometry-selection and window-length objections.
