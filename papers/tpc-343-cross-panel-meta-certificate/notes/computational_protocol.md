# TPC-343 computational protocol

The producer uses the TPC-340 source/operator implementation.  The independent
checker uses the separately hash-locked TPC-340 reverse-shell engine and
reimplements the row, leave-one-control-out, row-block, shared, and equal-row
projection calculations.

```text
panels  = TPC341 origins {48097,48609,49217}; TPC342 origins {40097,40609,41121}
scale   = 1024
operator= all_plus, Q=54, exponent=1, H=66
controls= nine TPC-338/TPC-340 controls
raw     = 2 x 3 x 9 x 4 = 216
holdout = 2 x 3 x 9 = 54
```

Every shifted source argument is below `50000`.  Floating projection checks use
the declared `8e-6` relative energy tolerance; normal and optimized runs must
emit byte-identical output with empty stderr.
