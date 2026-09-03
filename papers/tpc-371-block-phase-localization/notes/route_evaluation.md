# TPC-371 route evaluation

## Strongest positive result

The complete predeclared block panel is finite, positive, independently
replayed, and reproducible.  Every beta=2 block-local row stays below both
working envelopes, with maximum normalized spectral value
`0.5536333251967529`.

## Strongest obstruction

The TPC-370 parent has six full-window beta=2 high-Q/all-plus spectral
failures, but none of the 24 declared 256-point blocks has a beta=2 local
failure.  Thus the hypothesis that the parent failure is already contained in
one independently normalized short block is refuted on this panel.  This is
not yet a cross-block causality theorem because the normalization changes.

## Open theorem

For the same full-window normalization, decompose the operator into its fixed
block-diagonal and off-block parts and determine which component carries the
finite high-Q signal.  Any uniform or asymptotic version remains open.

## Reusable structure

```text
full-window failure -> fixed contiguous partition -> exhaustive local replay
  -> local-vs-global normalization warning -> off-block decomposition
```

`ARITHMETIC_ADVANCE=NO`, `FIXED_POWER_CREDIT=0`, and `FULL_GATE_B=OPEN`.
The local Bridge-B is repository evidence only; official evaluator files are
not present.

```text
ROUND2_CLUE = TEST_OFF_BLOCK_COHERENCE_DECOMPOSITION
```
