# TPC-392 computational protocol

The producer sums the prime shell in ascending order.  The independent
checker rebuilds the same finite matrices in descending shell order and does
not import the producer.  Both use one fixed near-block band, two Q anchors,
four laws, and the four normalization choices.

The first three origins are calibration origins at both calibration counts.
The last two origins are terminal holdouts at 1536 only.  All roles and
normalizations are fixed before current responses are read.

The canonical certificate is emitted only after all 256 rows are complete.
Ordinary and optimized producer/checker runs must agree with the canonical
payload within the checker contract and emit identical summary lines.  The
25-mutation stress suite attacks provenance, role metadata, rows, phase
summary fields, and the firewall.
