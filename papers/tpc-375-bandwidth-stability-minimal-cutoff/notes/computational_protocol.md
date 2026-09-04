# TPC-375 computational protocol

```text
origins       = (1010001, 1018021, 1026041)
window count  = 2048
blocks        = 8 contiguous blocks, each of length 256
cutoffs       = (0, 1, 2, 3)
Q             = (512, 2048, 8192)
exponent      = 1
law           = all_plus
beta          = 2
rows          = 9 (complete 3 x 3 beta=2 panel)
caps          = spectral 0.64, Schur 0.83
```

The producer uses ascending prime-shell accumulation.  The independent
checker has its own sieve and descending shell order.  Cutoff zero is
eigensolved block by block and the other bands are dense symmetric
eigensolves; this is an implementation optimization of the same declared
matrices, not a different normalization.  The full eigensystem is formed
before cutoff metrics are inspected.  All checks use one BLAS thread per
worker and Bridge-B requires empty stderr and byte-identical normal/optimized
stdout.

The exact anchor is `[1010346,1010359)`, `Q=4`, exponent one, beta `2`, shell
`{5,7}`; it is separate from the main panel.
