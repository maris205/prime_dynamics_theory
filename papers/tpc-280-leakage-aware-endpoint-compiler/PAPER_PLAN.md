# TPC-280 paper plan

## Question

What endpoint budget follows when the reconstructed packet energy has both a
multiplicative saving term and an additive leakage term?

## Claim-driven contributions

1. Prove a two-term normalized bound and its reciprocal gain compiler from
   `D >= d X^a` and `G <= B X^(-gamma) D + ell X^(a-delta)`.
2. Collapse the two terms to the dominant exponent `kappa=min(gamma,delta)`
   and derive the inherited signed-margin compiler.
3. Prove sharpness with an equality family and isolate the
   `delta < gamma` leakage bottleneck.
4. Recompute exact rational budget, margin, endpoint, and TPC-279 transfer
   fixtures with an independent checker and hostile mutations.

## Non-claims

This paper does not supply the growing source estimate, arithmetic `L2`, a
literal additive leakage decomposition for the TPC source, full Gate B, or a
twin-prime theorem.  The finite parent transfer is coordinate bookkeeping only.
