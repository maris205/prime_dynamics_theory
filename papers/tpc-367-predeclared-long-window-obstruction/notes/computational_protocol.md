# TPC-367 computational protocol

## Frozen inputs

```text
candidate grid: 620001 + 307*j, j=0,...,40
predeclared indices: 0,20,40
origins: 620001,626141,632281
counts: 512,1024
Q: 512,2048,8192
kernel exponents: 1,2
laws: all_plus, alternating_index, mod4_character, half_split
betas: 0,2
height: 66
spectral cap: 0.64
Schur cap: 0.83
```

The complete Cartesian product contains 288 rows.  Origin declaration occurs
before signed matrices and does not inspect a source, response, geometry
score, or law result.  The producer traverses each shell in increasing order;
the independent checker traverses it in decreasing order.

## Exact anchor

The half-open interval `[620362,620375)` with `Q=4`, exponent one, and shell
`{5,7}` is evaluated with `Fraction` arithmetic for beta 0 and 2.  Symmetry,
positive geometry, and canonical matrix/geometry digests are required.

## Reproducibility controls

Use `python -B` and set `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and
`MKL_NUM_THREADS=1`.  The certificate is canonical JSON with a payload hash
and row digest.  The Bridge-B checker reruns producer, independent replay, and
mutation stress in normal and optimized modes, requiring empty stderr and
byte-identical stdout.
