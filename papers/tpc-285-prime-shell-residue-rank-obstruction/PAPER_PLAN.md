# TPC-285 paper plan

## Question

Can the sign sensitivity in the finite source-control atlas be explained or
controlled by a low-rank prime-residue decomposition of the literal operator?

## Claim-driven contributions

1. Factor the centered residue matrix through the nonzero residue indicators.
2. Prove the exact `q-2` rank bound (and equality when all classes occur).
3. Track the physical deleted diagonal instead of silently discarding it.
4. Prove that diagonal deletion makes the active residue block full rank when
   all nonzero classes occur.
5. Audit the rational kernel Schur product on all 20 registered prime/exponent
   rows with an independently replayable modular rank witness.
6. State the obstruction cleanly: residue-mode low rank alone cannot supply
   literal arithmetic `L2` for the physical matrix.

## Non-claims

Full rank does not preclude cancellation, small singular values, or a useful
arithmetic estimate.  Conversely, the centered rank bound does not transfer
through diagonal deletion.  No fixed-power, Gate-B, or twin-prime conclusion
is claimed.
