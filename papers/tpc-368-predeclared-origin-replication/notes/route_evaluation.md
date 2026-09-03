# TPC-368 route evaluation

## Strongest positive result

The localized beta=2 failure pattern from TPC-367 is reproduced on all three
origins of a second predeclared grid.  Beta=2 has no spectral failure at
count 512, and no Schur failure on any of its 72 rows.  The reverse-shell
implementation independently reproduces all 144 rows.

## Strongest obstruction

The count-1024 beta=2 spectral cap still fails at `Q=2048` and `Q=8192`
under the all-plus law at every declared origin.  There are six failures;
the maximum is `0.674101905927736` against cap `0.64`.  The replication rules
out the narrow explanation that TPC-367's pattern was unique to its first
origin family, but it does not establish origin uniformity.

## Route decision

`TPC368_STATUS = NUMERICALLY_CERTIFIED_FINITE_PREDECLARED_ORIGIN_REPLICATION`.

`TPC368_BETA2_LONG_WINDOW_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED`,
`ARITHMETIC_ADVANCE=NO`, `FIXED_POWER_CREDIT=0`, and `FULL_GATE_B=OPEN`.
The next natural finite attack is a third predeclared origin family or a
count-2048 window.  If the pattern breaks, residue-phase localization is the
minimal follow-up.

No official Route-A/Route-B evaluator is available in this checkout; local
Bridge-B is fail-closed finite evidence only.

```text
ROUND2_CLUE = TEST_BETA2_THIRD_ORIGIN_FAMILY_OR_COUNT_2048
```
