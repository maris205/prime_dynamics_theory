# TPC-370 computational protocol

## Frozen inputs

```text
candidate grid: 1010001 + 401*j, j=0,...,40
predeclared indices: 0,20,40
origins: 1010001,1018021,1026041
count: 2048
Q: 512,2048,8192
kernel exponent: 1
laws: all_plus, alternating_index, mod4_character, half_split
betas: 0,2
height: 66
spectral cap: 0.64
Schur cap: 0.83
inherited exact interval: [1010346,1010359)
```

There are 18 non-law settings per beta and 36 law rows per beta, hence 72
rows total. The origin family, count, shell anchors, laws, and beta values
are fixed before signed replay; no source, response, law score, or geometry
ranking is consulted.

## Reproducibility controls

Use `PYTHONDONTWRITEBYTECODE=1`, `python -B`, and
`OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and `MKL_NUM_THREADS=1` for
the canonical producer. The certificate is canonical JSON with payload and
row digests. The independent checker uses a separately implemented sieve and
descending shell accumulation. The stress checker mutates the certificate
without changing the baseline document.

## Decision rule

If the parent six-key support persists, the next project localizes the
count-2048 phase across a predeclared origin/residue partition. If it changes,
the same localization protocol records the changed support. Neither outcome
receives arithmetic or fixed-power credit.
