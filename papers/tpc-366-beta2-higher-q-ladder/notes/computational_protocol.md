# TPC-366 computational protocol

The producer scans 41 candidate origins using only beta=2 unsigned weighted
square geometry on 256-point pilots.  It evaluates the five Q anchors and
two exponents, ranks by maximum geometry spread, applies the origin tie-break
and 2048 separation rule, and freezes `(623071,631360,629211)` before any
signed row is built.

The frozen replay evaluates beta `{0,2}`, counts `{256,512}`, Q
`{512,1024,2048,4096,8192}`, exponents `{1,2}`, and four fixed sign laws.
There are `480` rows and a true spectrum for every law.  The producer uses
increasing prime order; the independent checker uses reverse order and an
independently implemented sieve and exact rational anchor.

The spectral and Schur thresholds `0.64` and `0.83` are finite working caps.
The stress protocol applies 23 mutations.  Local Bridge-B locks all
claim-bearing files, checks the PDF and compile log, and runs producer,
independent, and stress checks in normal and optimized modes with empty
stderr and byte-identical stdout.
