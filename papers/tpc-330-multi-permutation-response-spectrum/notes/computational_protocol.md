# TPC-330 computational protocol

1. Verify the TPC-329 producer/certificate and TPC-267 V59 source hashes.
2. Freeze the TPC-329 two-origin/two-scale panel, four shell anchors, two
   exponents, literal masks, source formula, and `5e-8` ratio guard.
3. Freeze five controls before result generation: identity, three odd-affine
   maps `(3i+11)`, `(5i+17)`, `(7i+29)` modulo source count, and reversal.
4. Prove each map bijective on source counts `2048` and `4096`; verify
   source-multiset and `L2` preservation for every row.
5. Build the source vector and four coherent matrices for each of 32 rows.
6. Record `E,D,O,R`, guarded ratio intervals, and classifications for every
   row/control/law combination: `32*5*4=640` observations.
7. Build per-control censuses, per-law response signatures, all 10 pairwise
   control summaries, and retain the inherited 64 two-scale pairings.
8. Rebuild every matrix, source, placement, metric, summary, and exact anchor
   in an independent checker that does not import the producer and accumulates
   shell blocks in reverse order.
9. Run the mutation stress suite, normal and optimized variants, PDF checks,
   and local Bridge-B wrapper; require zero exit status, empty stderr, and
   byte-identical paired stdout.
10. Treat all control and growth readouts as finite.  No finite census creates
    a source-uniform theorem, fixed-power credit, or twin-prime implication.
