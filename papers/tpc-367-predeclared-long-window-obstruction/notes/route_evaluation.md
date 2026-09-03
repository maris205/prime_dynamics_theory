# TPC-367 route evaluation

## Strongest positive result

The frozen beta=2 rule has no spectral-cap failure for any of the 72 count-512
law rows, and no Schur-cap failure in any of its 144 rows.  The complete
finite replay is independently reproduced in reverse shell order.

## Strongest obstruction

The longer count-1024 rows break the beta=2 spectral cap at `Q=2048` and
`Q=8192` for all three predeclared origins and the all-plus law.  There are
six such rows; the maximum is `0.67410738070824539` against cap `0.64`.

## Route decision

`TPC367_STATUS = NUMERICALLY_CERTIFIED_FINITE_PREDECLARED_LONG_WINDOW_OBSTRUCTION`.

`TPC367_BETA2_LONG_WINDOW_TRANSFER = REFUTED_SCOPED`,
`ARITHMETIC_ADVANCE=NO`, `FIXED_POWER_CREDIT=0`, and `FULL_GATE_B=OPEN`.
The next paper should replicate the failure on a second predeclared origin
family, keeping the failing exponent and window scale fixed.  If replication
fails, the natural follow-up is residue-phase localization.

No official Route-A/Route-B evaluator is available in this checkout; local
Bridge-B is fail-closed finite evidence only.
