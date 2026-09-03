# TPC-369 computational protocol

## Frozen inputs

```text
candidate grid: 1010001 + 401*j, j=0,...,40
predeclared indices: 0,20,40
origins: 1010001,1018021,1026041
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
rows total.  The family and main-panel fields are fixed before signed replay;
no source, response, law score, or geometry ranking is consulted for origin
selection.

## Exact-anchor amendment

The initial half-open interval `[1010342,1010355)` at `Q=4`, exponent one,
and shell `{5,7}` has a zero geometry row for both betas.  Before any main
panel spectrum was evaluated, the deterministic first-valid scan selected
`[1010346,1010359)`.  Both intervals and the exact positivity flags are
recorded in the certificate.

## Reproducibility controls

Use `python -B` with `PYTHONDONTWRITEBYTECODE=1` and set
`OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and `MKL_NUM_THREADS=1`.
The certificate is canonical JSON with payload and row digests.  Bridge-B
reruns producer, independent replay, and mutation stress in normal and
optimized modes, requiring empty stderr and byte-identical stdout.
