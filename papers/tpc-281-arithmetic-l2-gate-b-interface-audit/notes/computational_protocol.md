# TPC-281 computational protocol

All arithmetic in the producer and independent checker uses Python
`fractions.Fraction`.  JSON is emitted in a canonical sorted-key form with a
trailing LF.  The producer hash-locks the TPC-280 code and result and copies
only its declared twelve-row coordinates.  The independent checker does not
import the producer: it reconstructs the four packet sums, `D`, `G`, `q`, the
parallel/perpendicular attachments, the four typed budgets, and the parent
transfer.  The stress checker applies six hostile mutations and requires every
one to be rejected.

Normal and optimized (`python`/`python -O`) executions are both required to
pass with empty stderr and byte-identical stdout.  The Bridge-B checker also
checks the complete project layout, marker registry, canonical certificate,
and compiled PDF.  These are reproducibility controls for a finite exact
artifact; they do not add a literal arithmetic estimate.
