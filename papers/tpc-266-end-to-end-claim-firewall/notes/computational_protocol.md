# Computational protocol

The producer and both experiment programs use exact `Fraction` arithmetic,
canonical JSON, explicit exceptions instead of executable `assert` checks,
and a frozen Git baseline.  The independent checker parses the emitted JSON
without importing the producer.  The hostile matrix mutates type labels,
thresholds, source locks, residual-retention flags, and closure statuses.

Every normal/optimized pair must have empty stderr, exit code zero, and
byte-identical stdout.  The bridge checker additionally verifies the PDF,
source hashes, project manifest, and bridge markers.
