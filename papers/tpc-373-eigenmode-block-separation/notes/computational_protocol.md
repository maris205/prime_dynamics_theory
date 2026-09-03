# TPC-373 computational protocol

The complete fixed Cartesian panel is:

```text
origins       = (1010001, 1018021, 1026041)
window count  = 2048
blocks        = 8 contiguous blocks, each of length 256
Q             = (512, 2048, 8192)
exponent      = 1
law           = all_plus
beta          = (0, 2)
rows          = 18
layers        = absolute block-index distance 0,...,7
```

Rows are constructed before the extremal mode is read.  The producer sums
primes in ascending order; the independent checker uses an independent
sieve and descending order.  Both use one BLAS thread per worker.  The
certificate is canonical JSON.  Normal and optimized subprocess output must
be byte-identical, with no stderr.
