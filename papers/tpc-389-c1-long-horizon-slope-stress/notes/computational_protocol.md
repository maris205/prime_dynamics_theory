# TPC-389 computational protocol

The response-blind panel is:

```text
grid start  = 2800001
grid step   = 401
grid count  = 41
indices     = (0,10,20,30,40)
calibration = origins 0,10,20 at counts 768,1024
holdout     = origins 30,40 at count 1280
Q           = (2048,8192)
bands       = fixed_c3, full_relative
laws        = all_plus, alternating_index, mod4_character, half_split
normalizers = local_diagonal, pooled_train_scalar
```

Every count is a multiple of the block length 128.  The producer accumulates
the prime shell in ascending order; the independent checker uses descending
order and does not import the producer.  Both compare finite floating-point
values to the canonical certificate.  The optimized run is a Python `-O`
replay, not a different mathematical model.

The exact anchor uses `Q=8`, shell `[11,13]`, and interval
`[2800001,2800014)`, with rational arithmetic for positivity and symmetry.
All generated JSON is canonical UTF-8/ASCII JSON with a payload hash.
