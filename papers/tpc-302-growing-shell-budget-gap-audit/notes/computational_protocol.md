# TPC-302 computational protocol

1. Lock TPC-288 code/result and TPC-301 code/result by normalized LF SHA-256.
2. Rebuild each literal source and physical prime output with exact fractions.
3. Form the physical Gram, clear denominators, and enumerate all
   (2^{|S|-1}) equal-sign classes by Gray code.
4. Build the first 17 literal cutoff profiles and the source image.
5. For each target, tolerance, context, and prefix, solve the constrained
   source budget with 60-digit mpmath ridge bisection (180 steps).
6. Store outward decimal intervals and canonical JSON.
7. Independently replay all 34 exact sign labels and ratios without importing
   the TPC-302 producer; run theorem stress fixtures in normal and optimized
   modes.

The producer uses at most eight forked workers by default (`TPC302_WORKERS`)
to bound memory.  No random sampling is used.  The 430 explicit shell target
count and the inherited 1,380-edge metadata count are intentionally separate.
