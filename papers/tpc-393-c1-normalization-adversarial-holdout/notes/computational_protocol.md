# TPC-393 computational protocol

The producer sums the $Q=8192$ prime shell in ascending order.  The
independent checker rebuilds the same finite matrices in descending shell
order and does not import the producer.  Both use the fixed-three-block band,
the all-plus and alternating-index laws, and the four predeclared
normalizations.

The first three origins are calibration origins at both calibration counts.
The last two origins are terminal holdouts at $N=1536$ only.  The affine grid,
roles, counts, law panel, normalization panel, and caps were fixed before
current responses were read.  The TPC-392 parent is read only as a hashed,
frozen interface record; no parent response enters the fit.

The canonical certificate is emitted only after all 64 rows are complete.  It
contains a canonical JSON payload hash, normalized-LF provenance hashes, a
rational exact anchor, row-level envelope flags, and the phase summary.  The
ordinary and optimized producer/checker runs must agree byte-for-byte in their
summary lines.  The 25-mutation stress suite attacks provenance, role
metadata, row census, phase summaries, anchor data, and the claim firewall.

For the release Bridge-B check, all six ordinary/optimized subprocesses are
run with one BLAS/OpenMP thread and with stderr required to be empty.  PDF
identity, compile diagnostics, and all documentation hashes are locked after
the final edit.
