# TPC-357 paper plan

## Question

Does the TPC-355 position-aware congruence admit a finite operator-norm
envelope that is stable along a declared origin/interval scale ladder?

## Frozen design

Use the TPC-356 selected origins `(38423,42010,45597)` without re-selection.
Replay counts `256,512,1024,2048`, shell anchors `Q=24,54,80`, exponents
`1,2`, and four fixed sign laws.  Compute Schur row-sum and Frobenius
envelopes for all 288 law-level rows.  Compute both extreme eigenvalues for
the 72 all-plus rows only.  No source response, source model, or arithmetic
weight enters the protocol.

## Decision rule

The finite Schur and Frobenius inequalities are exact mathematical statements.
Numerical caps are scoped to the declared 288-row replay.  A strict upward
transition in the normalized all-plus spectral ladder is retained as a finite
obstruction to a monotone-decay hypothesis; it is not extrapolated to an
asymptotic counterexample.

## Claim budget

The paper may claim finite envelopes, a finite normalized cap, and a finite
scale nonmonotonicity observation.  It may not claim a uniform origin bound,
source-uniform arithmetic `L2`, fixed-power credit, Route-B passage, or a
twin-prime theorem.
