# TPC-335 proof and scope package

## Proposition 1 — finite masked norm identity

For a disjoint exhaustive finite partition `I=disjoint_union_C I_C` and
`beta_C=beta 1_{I_C}`,

```text
||beta||_2^2 = sum_C ||beta_C||_2^2.
```

**Proof.**  Expand both sides as finite sums.  Each coordinate occurs exactly
once and all cross terms between distinct coordinate supports are zero. `QED`.

## Proposition 2 — source support partition

The four TPC-334 labels form such a partition for the declared source array:
the first three separate nonzero cross support, and `zero_support` contains
the complement. `QED` follows from the prime-power support implication in
TPC-334.

## Proposition 3 — finite certificate

The six rows satisfy the exact masked norm identity to the recorded replay
guard.  Twin norm fractions lie in `(0.09,0.13)` and background fractions in
`(0.65,0.72)` for all six rows.  This is `NUMERICALLY_CERTIFIED_FINITE` and
does not imply a source-uniform bound.
