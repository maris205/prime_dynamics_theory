# TPC-382 computational protocol

The parent paths, normalized SHA-256 values, schemas, statuses, counts, and
origins are constants in both the producer and independent checker.  TPC-380
and TPC-381 supply the matched `N=2048` cohort; TPC-379 supplies the explicitly
labelled `N=1024` scale control.  All parent panels already have complete
three-origin by three-Q by four-law row keys.

For each law/Q cell, values are sorted by origin and summarized by minimum,
maximum, arithmetic mean, absolute spread, and relative spread.  The cap
`0.01` and high-Q anchor `8192` are fixed in code before parent values are
read.  No parent row is selected after aggregation.

The result is canonical JSON.  The independent checker reads each parent
directly and recomputes the statistics.  The stress checker applies 25 semantic
mutations.  The local Bridge-B runs producer, independent, and stress checks in
both normal and optimized Python modes and compares their byte outputs.
