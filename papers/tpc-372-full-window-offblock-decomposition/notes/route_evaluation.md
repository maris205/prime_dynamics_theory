# TPC-372 route evaluation

## Strongest positive result

The common-normalization identity `T=D+R` is reproduced on all 18 declared
rows.  For beta=2, every full-window failure row has a positive finite
reverse-triangle lower bound for the off-block norm.

## Strongest obstruction

On beta=2, the full matrix has 6 spectral-cap failures, but the block-diagonal
and off-block components each have zero spectral-cap failures.  The finite
excess is therefore a sum/coherence phenomenon for this common normalization,
not a single-component cap crossing.  This does not establish causality.

## Open theorem

Resolve the eigenmode/block-separation profile of the six full beta=2 failure
rows, using the same full-window normalization and a predeclared block-pair
partition.

## Reusable structure

```text
local normalized obstruction -> common full normalization -> D+R identity
  -> reverse-triangle necessity -> eigenmode phase audit
```

`ARITHMETIC_ADVANCE=NO`, `FIXED_POWER_CREDIT=0`, and `FULL_GATE_B=OPEN`.

```text
ROUND2_CLUE = TEST_EIGENMODE_BLOCK_SEPARATION
```
