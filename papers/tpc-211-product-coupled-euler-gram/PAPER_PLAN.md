# TPC-211 Paper Plan

## Question

Does the literal V46 product coupling of the shifted-prime and hybrid Euler
profiles prevent the cross-divisor alignment obstruction found in TPC-210?

## Claim ceiling

The paper proves finite algebraic statements for the exact local factors and
their common CRT lifts.  It does not estimate the literal shifted-prime
sequence, the AP residual, the reciprocal occupancy, or the prime shell.

## Theorem sequence

1. Define the common CRT lift of `P_S`, `B_S`, and `Delta_S`.
2. Prove the exact product cocycle and the zero-axis/zero-mean identities.
3. Use Fourier support triangularity to prove full divisor rank.
4. Prove the logarithmic Mobius packet derivative identity.
5. Show exact common-endpoint cancellation for complete packets and isolate
   the truncated transition boundary.
6. Use the positive definite Gram matrix to construct a shared endpoint that
   realizes Mobius-aligned correlations.
7. State the resulting scoped obstruction and the next arithmetic theorem.

## Experiments

The producer and independent checker use exact `Fraction` arithmetic on three
active-prime sets.  They verify profile rank, Gram determinant, the cocycle,
the coefficientwise marked-prime derivative identity, complete-packet endpoint
cancellation, and the shared-endpoint alignment ratio.

## Route decision

`Route A` is not applicable to this analytic prime/twin-prime session.  The
TPC Route B structural threshold advances.  Product coupling alone is
insufficient for a saving; the next theorem must control the truncated packet
boundary together with the reciprocal physical emitter.
