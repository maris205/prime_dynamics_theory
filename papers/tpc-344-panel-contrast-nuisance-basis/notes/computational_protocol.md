# TPC-344 computational protocol

The producer uses the hash-locked TPC-340 source/operator implementation after
checking the TPC-343 parent certificate.  The independent checker does not
import the producer.  It uses the separately hash-locked TPC-340
reverse-shell engine and reimplements source classification, all controls,
row means, projections, panel contrasts, holdouts, and cross-fits.

```text
panels       = TPC341 origins {48097,48609,49217}
               TPC342 origins {40097,40609,41121}
scale        = 1024, source rows of length 512
operator     = all_plus, Q=54, exponent=1, H=66
controls     = nine predeclared coordinate bijections
raw          = 2 x 3 x 9 x 4 = 216
nonempty     = 171
in-sample    = 6
holdout      = 2 weightings x 9 omitted controls = 18
cross-fit    = 2 directions x 2 weightings = 4
contrast     = base plus (+1,-1) panel-sign columns
```

The numerical projection tolerance is `8e-6` relative target energy.  The
certificate is canonical JSON with a SHA-256 payload digest.  Normal and
optimized runs must have empty stderr and byte-identical stdout.  The stress
suite mutates geometry, signs, guard values, provenance semantics, rank, and
the exact anchor.
