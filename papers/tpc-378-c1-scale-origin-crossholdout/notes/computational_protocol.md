# TPC-378 computational protocol

## Frozen inputs

```text
grid_start = 1100001; grid_step = 401; grid_count = 41
origin_indices = 0,20,40; origins = 1100001,1108021,1116041
counts = 1024,2048; block_length = 256; block_counts = 4,8
Q = 512,2048,8192; exponent = 1; beta = 2; law = all_plus
height = 66; band cutoff = 1; spectral cap = 0.64; Schur cap = 0.83
```
The selection protocol does not inspect responses, signed metrics, geometry,
or row outcomes.  All 18 Cartesian rows are constructed before the profile is
read.  Each count uses full-window square-energy normalization, so the
cross-count comparison remains finite and explicitly scale-specific.

## Audits

The producer uses the inherited TPC-377 finite c=1 record to construct the
new panel and locks its source and certificate hashes.  The independent
checker uses a direct sieve to 20000, reverse shell accumulation, independent
full/band eigensystems, and the exact rational anchor.  The stress checker
applies 24 independent document mutations and requires all to be rejected.
The Bridge-B checker locks the stable release files and repeats producer,
independent, and stress checks in normal and optimized Python modes.

## Recorded output

```text
rows = 18
failure profile by count,Q = (0,3,3); (0,3,3)
spectral failures = 12/18
Schur failures = 0/18
retention = 0.93759972206138864--0.98046528117382914
tail fraction <= 0.062400277938610291
```
