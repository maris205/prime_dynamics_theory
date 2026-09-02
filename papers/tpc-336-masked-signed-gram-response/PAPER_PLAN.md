# TPC-336 paper plan

## Claim

A fixed signed-Gram operator can change the apparent importance of source
support classes through output cross interactions, even when the source norm
partition is exact.

## Work package

1. Rebuild the four TPC-335 masked residual vectors.
2. Apply one predeclared all-plus operator at `Q=54`, `s=1`.
3. Record self response gains and every pairwise output inner product.
4. Verify the full-output Gram expansion, an exact rational anchor, independent
   reverse-shell replay, and mutation stress.

## Decision rule

If the gain ordering is stable but self energies do not add to the full
response, record an output-interference obstruction and stop this batch.  Do
not interpret a fixed operator's finite ordering as a growing estimate.
