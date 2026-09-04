# TPC-381 computational protocol: c=1 origin-family replay

## Frozen inputs

```text
grid_start = 1400001; grid_step = 401; grid_count = 41
origin_indices = 0,20,40; origins = 1400001,1408021,1416041
window_count = 2048; block_length = 256; block_count = 8
Q = 512,2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus,alternating_index,mod4_character,half_split
band cutoff = 1; spectral cap = 0.64; Schur cap = 0.83
```

The second origin family and all 36 rows are fixed before the failure census.
The geometry is shared by all laws.  The exact q=8 anchor is
`[1400001,1400014)`; it is the first fixed subinterval of the selected window,
not a metric-selection input.

## Audits

The producer locks the TPC-380 code and canonical certificate and uses shared
components so that the origin-family replay is computationally reproducible.  The
independent checker uses a direct sieve to 20000, reverse-shell accumulation,
independent signs, full/band eigensystems, and exact rational anchor checks.
The stress checker applies 25 semantic/schema mutations.  Bridge-B locks all
stable project artifacts and repeats producer, independent, and stress checks
in normal and optimized modes.

## Recorded result

```text
rows = 36
all_plus profile = (0,3,3), failures = 6/9
alternating_index profile = (0,0,0), failures = 0/9
mod4_character profile = (0,0,0), failures = 0/9
half_split profile = (0,0,0), failures = 0/9
spectral failures = 6/36
Schur failures = 0/36
```

band spectral maxima in law order =
`0.66694427563296521`, `0.0077610039910285299`,
`0.012055505105884349`, `0.21613933977437655`
absolute band-Rayleigh retention = `0.0021890151798274436--0.97694644030159705`
maximum absolute tail fraction = `0.99781098482017305`
q=8 geometry digest =
`bf086c54b42280dda167bc5dc19f53c45afed4c5a51e0338a9555c65a6474d1f`

The profile reproduces TPC-380 on a second origin family at count 2048.  It remains a finite,
law-dependent observation with zero arithmetic and fixed-power credit.
