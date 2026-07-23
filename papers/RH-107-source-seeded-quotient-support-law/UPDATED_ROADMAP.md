# Route update after RH-107

## New quotient decomposition

The physical quotient gate no longer needs to be attacked only through an
all-level `c^2/g` exponent. It splits into:

1. a support problem: prove `s4/s1 >= tau` on all sufficiently fine
   source-seeded updates;
2. a finite coarse price problem for the remaining weak events;
3. the already proved stopped fallback if the coarse price exceeds slack.

At the five anchors, every tested threshold has an empty fine support. This
explains why quotient accumulation does not worsen at the last two scales.

## What remains open

The five-anchor support boundary cannot be extrapolated without a structural
theorem. RH-108 should investigate a direct lower bound for the fourth
projected-cross singular ratio, preferably from the reduced moment matrices
of RH-95 and the finite-memory action of RH-101.

If that bound fails, the negative result should identify whether the fourth
mode can re-enter below the cutoff infinitely often. The RH-104 physical
prefix and RH-105 physical residual exponents remain separate open leaves.

Moving-cloud, arithmetic trace, zero-identification, and Hilbert--Polya work
remain deferred until Stage A is genuinely closed.
