# TPC-353 computational protocol

The panel is frozen before reading the certificate:

```text
origins       = 6001, 8001, 10001
source counts = 256, 512, 1024
Q anchors     = 24, 54, 80
exponents     = 1, 2
laws          = all_plus, alternating_index, mod4_character, half_split
height        = 66
tail cutoff   = 50000
alignment guard = 1e-7
```

The producer uses exact Decimal/Fraction source enclosures followed by a
float64 matrix replay.  The independent checker uses a separate trial sieve,
reverse shell accumulation, and independent output calculations.  Stress
mutations operate only on in-memory certificate copies.  Normal and optimized
executions must return zero, emit empty stderr, and have byte-identical output.

The certificate, source code, independent checker, stress script, PDF, compile
log, and Bridge-B markdown are hash-locked by the local bridge.
