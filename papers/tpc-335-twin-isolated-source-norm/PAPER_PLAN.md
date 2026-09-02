# TPC-335 paper plan

## Claim

Explicit support masks yield an exact finite Pythagorean decomposition of the
source residual, and the twin class has a stable but non-dominant residual
norm share.

## Work package

1. Rebuild the parent-locked source arrays and TPC-334 support labels.
2. Form four disjoint masked residual vectors and compute their squared norms.
3. Compare twin residual share with twin cross-term share.
4. Add an exact rational mask anchor, independent replay, and mutation stress.

## Decision rule

If the twin residual share is stable and materially different from its cross
share, carry all three vectors into an operator-response experiment.  If it is
negligible or unstable, treat the source-level twin isolation as an
obstruction.  No finite share earns arithmetic power credit.
