# TPC-370 route evaluation

## Strongest positive result

The count-2048 replay preserves the TPC-369 beta=2 failure support: exactly
the all-plus rows at `Q=2048` and `Q=8192` fail at all three predeclared
origins. After removing the count coordinate, the six-key signature matches
the parent certificate. Beta=2 has no spectral failure at `Q=512` and no
Schur-cap failure in any of its 36 rows.

## Strongest obstruction

The support persistence does not establish magnitude stability. The beta=2
maximum rises from the TPC-369 value `0.67410489800609708` to
`0.71099989528234753`, a finite difference of
`0.036894997276250452`. Thus the observed support can be persistent while
the normalized size remains window-dependent. The beta=0 control also has 9
spectral and 9 Schur violations at count 2048.

## Open theorem

A theorem controlling the beta=2 normalized operator uniformly in origin,
window length, and shell scale remains open. In particular, the finite
support signature cannot be promoted to an asymptotic all-plus obstruction or
to a source-uniform arithmetic `L2` estimate.

## Reusable structure

The useful reusable object is the two-level audit: compare failure-key support
after quotienting out the changing count coordinate, while retaining the raw
and normalized maxima as separate diagnostics. The exact anchor is inherited
through a hash-locked, response-blind declaration.

## Route decision

`TPC370_STATUS = NUMERICALLY_CERTIFIED_FINITE_COUNT_2048_WINDOW_AUDIT`.

`ARITHMETIC_ADVANCE=NO`, `FIXED_POWER_CREDIT=0`, and `FULL_GATE_B=OPEN`.
The next minimal project should localize which origin/residue/high-Q phase
produces the persistent count-2048 support. It must use a new predeclared
partition and must not rank cells by observed response.

No official Route-A/Route-B evaluator is available in this checkout; local
Bridge-B is fail-closed finite evidence only.

```text
ROUND2_CLUE = TEST_COUNT_2048_PHASE_LOCALIZATION
```
