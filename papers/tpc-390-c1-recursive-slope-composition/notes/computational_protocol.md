# TPC-390 computational protocol

```text
grid       = 3000001 + 401*j, j=0,...,40
indices    = (0,10,20,30,40)
origins    = (3000001,3004011,3008021,3012031,3016041)
calibration= first three origins at N=(1024,1280)
holdout    = last two origins at N=1536
blocks     = 128
bands      = fixed_c3, full_relative
Q          = 2048, 8192
laws       = all_plus, alternating_index, mod4_character, half_split
normalizers= local_diagonal, pooled_train_scalar
caps       = spread 0.01, spectral 0.64, Schur 0.83, transfer 0.03
```

The producer processes prime shells in ascending order.  The independent
checker processes the identical shell in descending order and does not import
the producer.  Environment variables pin BLAS/OpenMP to one thread for
reproducibility.  The response-blind selection flags are checked in the
certificate and in Bridge-B.
