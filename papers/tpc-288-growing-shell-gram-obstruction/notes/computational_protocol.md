# TPC-288 computational protocol

1. Lock TPC-287's normalized-LF producer/result and the frozen TPC-268 engine.
2. Enumerate the eight growth-path anchors and the 18-row height/cutoff
   control grid; verify the expected row count and shell cardinalities.
3. Rebuild each literal prime component with exact rational arithmetic.
4. Recompute component and shell scalar intervals, exact component/shell
   energies, scalar retention bounds, and the output Gram matrix.
5. Reduce rational Gram matrices modulo `1000000007` and require full rank on
   every row.  On six declared rows, independently reduce the aggregate
   active physical matrix and require full active rank.
6. Verify the finite mismatch census and canonical JSON payload hash.
7. The independent checker repeats the arithmetic without importing the
   producer.  The stress script mutates theorem text, grid, energy, Gram rank,
   operator rank, flags, counts, budget, provenance, and row membership.
8. The Bridge-B checker verifies all required files, PDF/log hygiene, the
   certificate digest, and ordinary/optimized byte-identical subchecks.

The grid is a finite declared probe.  No count is interpreted as a density,
limit, or arithmetic `L2` estimate.
