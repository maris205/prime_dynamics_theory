# TPC-347 computational protocol

```text
origins       = 40097, 48097
source counts = 256, 512, 1024
Q             = 24, 36, 54, 80
exponents     = 1, 2
height H      = 66
laws          = all_plus, alternating_index, mod4_character, half_split
Young radius  = 65536
rows          = 2*3*4*2*4 = 192
```

The producer builds the physical matrix and the unmasked matrix independently,
uses a symmetric eigensolver for the induced finite `2`-norm, and stores twelve
significant digits.  The finite Young sum is accumulated with `math.fsum` and
an upward `nextafter` step.  All subprocesses set `PYTHONDONTWRITEBYTECODE=1`
and single-threaded BLAS variables.

The independent checker reverses shell accumulation order and reconstructs all
192 rows.  The stress suite tests exact rational decomposition, projection
contraction, and the analytic tail scale.  Normal and optimized invocations
must have identical stdout and empty stderr.
