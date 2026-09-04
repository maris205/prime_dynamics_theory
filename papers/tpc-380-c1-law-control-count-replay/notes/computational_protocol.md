# TPC-380 computational protocol

## Frozen inputs

```text
grid_start = 1300001; grid_step = 401; grid_count = 41
origin_indices = 0,20,40; origins = 1300001,1308021,1316041
window_count = 2048; block_length = 256; block_count = 8
Q = 512,2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus,alternating_index,mod4_character,half_split
band cutoff = 1; spectral cap = 0.64; Schur cap = 0.83
```

The 36 rows are built before the failure census.  The geometry is shared by
all laws.  The exact q=8 anchor is `[1300014,1300027)`; it is a finite
positivity check inside the first selected window, not a metric-selection
input.

## Audits

The producer locks the TPC-379 code and canonical certificate and uses shared
components so that the count replay is computationally reproducible.  The
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
`0.66694556698889795`, `0.0077646382652031094`,
`0.012038214320188189`, `0.21613429440676551`
absolute band-Rayleigh retention = `0.0021757978771847777--0.97694432793223085`
maximum absolute tail fraction = `0.99782420212281453`
q=8 geometry digest =
`d17b892caed9169be686d11e0e20cec8397e14834693e47a83fd972cb2423bd5`

The profile reproduces TPC-379 at count 2048.  It remains a finite,
law-dependent observation with zero arithmetic and fixed-power credit.
