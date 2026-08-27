# TPC-278 paper plan

## Question

Does the favorable signed gain found in TPC-277 survive small declared changes
to the prime shell and clock on the same physical source?

## Frozen object

- TPC-277 exact source engine and its eight-row gain-floor audit;
- actual beta source, masks, deleted diagonal, four packets, and rank-three
  projection;
- kernel exponent `s=2` and comparison cutoff `z` at each scale.

## Claim-bearing contributions

1. Recompute a 12-row Q/H perturbation matrix with exact rational arithmetic.
2. Certify four sign flips of the net cross term, including three shell flips
   and one clock flip.
3. Preserve three unchanged natural controls as exact transfers from TPC-277;
   add the $N=384$ natural row to keep the clock perturbation audit separate.
4. Close the finite stability shortcut while keeping asymptotic uniformity
   explicitly open.

## Route decision

The result is a scoped finite obstruction.  The next natural problem is to
state the weakest coherence/deficit hypothesis that would be sufficient for a
source-level gain theorem.
