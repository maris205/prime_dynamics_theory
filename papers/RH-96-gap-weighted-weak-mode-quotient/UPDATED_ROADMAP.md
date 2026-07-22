# Updated roadmap after RH-96

## What is now resolved

RH-95 showed that the fourth cross direction can be geometrically unstable.
RH-96 proves that such a direction can instead be quotiented by an energy
bound. At cutoff 1e-8, exactly the five ill-conditioned fourth modes are
omitted and every endpoint remains green.

## New frontier: composition, not local selection

The 1e-6 and 1e-4 experiments are the key warning. Every omitted update has a
valid local gap certificate, yet the recursive endpoint target fails. The
remaining problem is to propagate additive local tail losses through later
Ritz contractions.

RH-97 should establish a recurrence such as

    e_t <= rho_t e_{t-1} + epsilon_t,

where `epsilon_t` is the quotient loss certified here and `rho_t` is a
predictor/refresh sensitivity factor. Iteration would give

    e_N <= sum_j epsilon_j product_{l>j} rho_l.

This will identify a global cutoff budget and explain the observed threshold
frontier.

## Route after composition

1. Turn the finite horizon recurrence into repeated block or stopped-clock
   control.
2. Prove a uniform burn-in/source bridge.
3. Build normalization and observability gate `O`.
4. Revisit moving-cloud spectral determinants only after those gates.

No Hilbert--Polya operator, zero identification, or RH proof is asserted.
