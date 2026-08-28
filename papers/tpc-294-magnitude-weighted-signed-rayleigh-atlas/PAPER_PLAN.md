# TPC-294 paper plan

## Question

TPC-293 found a small unit-edge signed max-cut anomaly but deliberately threw
away Gram magnitudes.  Does the actual weighted quadratic form admit a finite
equal-sign contraction, and does the sign-only optimizer identify it?

## Claim spine

1. Define the physical shell Gram matrix and the trace-normalized signed
   Rayleigh quotient.
2. Prove the diagonal-plus-cross-term identity and the nonnegativity inherited
   from the Gram representation.
3. Use a common positive denominator and exhaustive Gray traversal to obtain a
   global exact finite optimum over all sign vectors modulo reversal.
4. Recompute the inherited 18-row grid with exact rational arithmetic and an
   independent source-first replay.
5. Compare the weighted optimum with the TPC-293 unit-edge max-cut witness,
   documenting the obstruction to replacing energy by sign combinatorics.
6. Route the next stage toward the source coefficient image and keep all
   asymptotic/arithmetic claims open.

## Claim ceiling

The identity and finite enumeration lemma are proved exactly.  The 18-row
atlas is a finite exact-rational computational certificate with independent
replay and adversarial stress tests.  No growing-shell theorem, source-image
surjectivity, arithmetic $L^2$ estimate, fixed-power credit, Gate-B closure,
or twin-prime conclusion is claimed.
