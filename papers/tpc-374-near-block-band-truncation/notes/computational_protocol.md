# TPC-374 computational protocol

```text
origins       = (1010001, 1018021, 1026041)
window count  = 2048
blocks        = 8 contiguous blocks, each of length 256
band cutoff   = 3 (block distances 0,1,2,3)
Q             = (512, 2048, 8192)
exponent      = 1
law           = all_plus
beta          = (0, 2)
rows          = 18
caps          = spectral 0.64, Schur 0.83
```

The complete Cartesian panel is materialized before mode inspection.  The
producer accumulates the shell in ascending order.  The independent checker
uses a separate sieve and descending order, then rebuilds every full and
band eigensystem.  Environment variables constrain each BLAS process to one
thread; Bridge-B repeats normal and optimized Python invocations with empty
stderr and byte-identical stdout.

The exact anchor is `[1010346,1010359)`, `Q=4`, exponent one, shell `{5,7}`.
It is a separate exact check and not a data-selected panel row.
