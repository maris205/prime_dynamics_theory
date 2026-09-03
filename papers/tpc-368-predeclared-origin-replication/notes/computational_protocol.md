# TPC-368 computational protocol

## Frozen inputs

```text
candidate grid: 810001 + 353*j, j=0,...,40
predeclared indices: 0,20,40
origins: 810001,817061,824121
counts: 512,1024
Q: 512,2048,8192
kernel exponent: 1
laws: all_plus, alternating_index, mod4_character, half_split
betas: 0,2
height: 66
spectral cap: 0.64
Schur cap: 0.83
```

There are 36 non-law settings per beta and 72 law rows per beta, hence 144
rows total.  Origin declaration occurs before signed matrices and does not
inspect a source, response, geometry score, or law result.  The producer
traverses each shell in increasing order; the independent checker traverses
it in decreasing order.

## Exact anchor

The half-open interval `[810342,810355)` with `Q=4`, exponent one, and shell
`{5,7}` is evaluated with `Fraction` arithmetic for beta 0 and 2.
Symmetry, positive geometry, and canonical matrix/geometry digests are
required.

## Reproducibility controls

Use `python -B` with `PYTHONDONTWRITEBYTECODE=1` and set
`OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and `MKL_NUM_THREADS=1`.
The certificate is canonical JSON with a payload hash and row digest.  The
Bridge-B checker reruns producer, independent replay, and mutation stress in
normal and optimized modes, requiring empty stderr and byte-identical
stdout.
