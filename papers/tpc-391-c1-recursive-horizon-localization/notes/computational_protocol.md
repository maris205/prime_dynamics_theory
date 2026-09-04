# TPC-391 computational protocol

The producer uses ascending prime-shell order.  The independent checker uses
descending shell order and does not import the producer.  Both implementations
use the same declared finite kernel, bands, laws, and normalizations.

The calibration origins are measured at all four calibration lengths.  The two
holdout origins are measured only at N=1536; their role is fixed before any
response is read.  Parent slopes are read from the hashed TPC-390 certificate
and never refit.

The canonical certificate is written only after the complete 448-row panel is
computed.  Ordinary and optimized Python runs must emit byte-identical
summary lines.  The stress suite applies 25 mutations to provenance, roles,
rows, trajectory fields, summary counts, and firewall values.
