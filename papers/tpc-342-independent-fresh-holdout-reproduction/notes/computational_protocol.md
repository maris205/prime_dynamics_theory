# TPC-342 computational protocol

The producer locks the TPC-341 protocol and TPC-340 source/operator artifacts,
then evaluates the three rows (origin, scale) = (40097,1024), (40609,1024),
(41121,1024).  It classifies the four disjoint source masks, applies nine
coordinate bijections, forms the all-control nuisance projection, and evaluates
all nine leave-one-control-out fits per row.

The certificate uses canonical JSON and a payload SHA-256.  The reverse-shell
checker uses the TPC-340 independent engine and reimplements the projection
statistics.  Normal and optimized Python runs must have empty stderr and
byte-identical stdout.  Mutation stress must reject row deletion, cutoff
flips, guard falsification, rank-census tampering, and arithmetic-claim
promotion.
