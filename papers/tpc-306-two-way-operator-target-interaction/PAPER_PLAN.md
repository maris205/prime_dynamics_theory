# TPC-306 paper plan

## Question

TPC-305 isolated a target swap inside each physical-operator row, but its two
rows still have different operators.  Can the four resulting budget cells be
organized into an explicit two-way decomposition that measures the residual
operator interaction before any causal language is used?

## Minimal contribution

1. Arrange the native and transported budgets as a positive `operator x target`
   four-cell table.
2. Define the two row-wise log target effects, their mean target contrast, and
   their difference interaction contrast.
3. Prove the exact identity `m^2-i^2=d_L*d_R`, including the criterion for
   stable target preference versus interaction dominance.
4. Derive and certify the decomposition on all 18 TPC-305 cases and 3 source
   normalizers (54 rows), with hostile ratio-margin controls.

## Acceptance criteria

- TPC-305 producer and certificate hashes are locked;
- all 54 derived rows replay with independent Decimal logarithms;
- the exact squared-contrast identity and positive row-scaling invariance pass
  an independent stress suite;
- the finite census is 12/18 target-main-dominant and 6/18
  interaction-dominant, with the middle transition 5/6 and same-prefix 3/3;
- all main-dominant ratio intervals are below `0.88`, all
  interaction-dominant intervals are above `1.2`, and middle same-prefix
  intervals are below `0.64`;
- normal/optimized producer, independent replay, stress, and Bridge-B outputs
  agree with empty stderr, and `paper/paper.pdf` is clean.
