# TPC-379 computational protocol

## Frozen inputs

```text
grid_start = 1200001; grid_step = 401; grid_count = 41
origin_indices = 0,20,40; origins = 1200001,1208021,1216041
window_count = 1024; block_length = 256; block_count = 4
Q = 512,2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus,alternating_index,mod4_character,half_split
band cutoff = 1; spectral cap = 0.64; Schur cap = 0.83
```

All origins and all four laws are fixed before response readout.  The 36 rows
are constructed before the failure census.  The geometry is shared across
laws, while each law has its own signed normalized matrix.

## Audits

The producer inherits and locks TPC-378's code and certificate, but computes
the four law matrices explicitly.  The independent checker uses a direct sieve
to 20000, reverse-shell accumulation, an independent sign-pattern
implementation, independent full/band eigensystems, and an exact rational
q=8 anchor.  The stress checker applies 25 semantic/schema mutations.  The
Bridge-B checker locks every stable project artifact and repeats producer,
independent, and stress checks in normal and optimized modes.

## Recorded output

```text
rows = 36
all_plus profile = (0,3,3), failures = 6/9
alternating_index profile = (0,0,0), failures = 0/9
mod4_character profile = (0,0,0), failures = 0/9
half_split profile = (0,0,0), failures = 0/9
spectral failures = 6/36
Schur failures = 0/36
band spectral maxima = 0.65334758792533143 / 0.0094084540584888146 /
                       0.011835976723613296 / 0.2117349490215118
```
