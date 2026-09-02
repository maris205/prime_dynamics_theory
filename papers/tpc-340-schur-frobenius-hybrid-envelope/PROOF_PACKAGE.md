# TPC-340 proof and scope package

## Proposition 1 — Schur envelope

For every finite symmetric matrix `A`, `||Ax||_2^2 <= R^2||x||_2^2`, where
`R=max_i sum_j |A(i,j)|`.

**Proof.** For a symmetric matrix the induced 1- and infinity-norms are both
`R`.  The inequality `||A||_2^2 <= ||A||_1||A||_infty` proves the claim. `QED`.

## Proposition 2 — hybrid envelope

For vectors supported on `S`,
`||Ax||^2 <= min(F(S)^2,R^2)||x||^2`.

**Proof.** Apply the TPC-339 support Frobenius inequality and Proposition 1,
then take their minimum. `QED`.

## Finite certificate

All 216 records pass the hybrid bound.  The Schur branch is active in 54
records, exactly the nine zero-support placements in each of six windows;
the Frobenius branch is active in the other 162 records.  The zero-support
Frobenius gain is reduced by factors `1.250245--4.698443`.  Broad-mask hybrid
occupancy remains below `0.1868550366`, so the sharpening does not close the
uniform tightness gate.

## Scope boundary

The norm inequalities are general finite statements.  Branch counts and
occupancy ranges are finite observations for the declared panel and do not
provide a growing arithmetic estimate or fixed-power credit.
