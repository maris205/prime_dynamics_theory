# TPC-277 computational protocol

The producer uses `PYTHONDONTWRITEBYTECODE=1 python -B` and imports only the
frozen TPC-268 engine.  It evaluates the rows

```text
(192,32,6,5), (256,38,6,6), (384,50,7,7),
(512,64,8,7), (768,86,9,9), (1024,108,10,10),
(1536,150,12,12), (2048,170,12,12),
```

with kernel exponent `s=2`.  All source, shell, projection, packet, `D`, and
`G` operations use `fractions.Fraction`.  The JSON stores outward grid
`10^15` intervals and a digest of the exact `D,G` pair.  A second checker
accumulates by source column rather than by row and verifies every digest and
interval.  The stress script mutates theorem counts, floor labels, and source
classifications and requires rejection.

No floating-point result is used as evidence; compact decimals in the paper
are display-only.
