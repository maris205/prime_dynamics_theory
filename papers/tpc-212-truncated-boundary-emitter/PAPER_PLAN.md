# TPC-212 Paper Plan

## Question

After the complete product packet is compressed by the TPC-211 logarithmic
Mobius derivative, does the actual divisor band `Y0<d<=U` together with the
reciprocal emitter `A_d(r)` force a cross-divisor cancellation?

## Claim ceiling

The paper proves exact finite operator identities for a squarefree divisor
lattice and a finite reciprocal occupancy map.  It does not estimate the
physical shifted-prime sequence, the smooth `psi`, the prime shell, or the
asymptotic transition range.

## Theorem sequence

1. Define a divisor selector and its signed Boolean endpoint incidence.
2. Prove the complete-minus-missing boundary decomposition coefficientwise in
   the independent `log(p)` basis.
3. Show that a nonzero incidence vector is an exact endpoint leakage witness;
   use the `t=35`, `5<d<=35` band as the smallest literal example.
4. Define the reciprocal occupancy operator and prove its collision Gram
   identity by reindexing the congruence.
5. Prove that the natural direct-sum emitter Gram is block diagonal and that
   arbitrary nonzero emitter rows admit finite aligned residuals.
6. State the scoped obstruction and the physical theorem that remains open.

## Experiments

The producer and independent checker use exact rational arithmetic.  Boundary
fixtures use deterministic rational profiles only to verify the algebraic
decomposition.  Emitter fixtures use unit reciprocal weights on finite
`(q,m)` sets; they verify occupancy counts, collision counts, Gram rank, and
aligned coherent-to-diagonal ratios.

## Route decision

`Route A` is not applicable to this analytic prime/twin-prime session.  The
Route-B structural threshold advances.  The cut and reciprocal emitter alone
are insufficient for saving; the next theorem must impose the literal
physical coupling between the residual profiles at different divisors.
