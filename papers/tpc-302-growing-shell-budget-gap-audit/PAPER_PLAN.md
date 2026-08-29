# TPC-302 paper plan

## Question

Does the native literal-profile budget separation found by TPC-301 survive
when the target labels are regenerated on the full TPC-288 growing-shell and
source-control grid?

## Claim-bearing objects

1. A literal physical prime-shell output Gram matrix.
2. Its exact equal-sign minimum, compiled independently for each row.
3. The first 17 literal Mobius-cutoff source profiles and their physical image.
4. Relative-RMS constrained source budgets at three tolerances.

## Planned result

Report a positive finite stability certificate if the common weighted/positive
gap remains separated, while explicitly retaining the open uniform-budget and
arithmetic gates.  If any row collapses, report that row as the main finite
counterexample instead of averaging it away.

## Follow-on decision rule

If all finite rows remain separated, TPC-303 should attack growth of the
native budget itself.  If a row collapses, TPC-303 should independently
reproduce and localize the first collapse.  Cross-family exploration is out of
scope.
