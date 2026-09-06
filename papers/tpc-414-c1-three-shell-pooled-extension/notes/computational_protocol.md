# TPC-414 computational protocol

- Pool complete shells `Q=65536,131072,262144`: counts `5709,10749,20390`.
- Use `H=66`, `N=264`, origin lower bound `10^6`.
- Alternate CRT residues on the pooled increasing prime order.
- Preserve every source-shell label in exact rational amplitudes.
- Independent replay rebuilds the sieve, CRT, shell labels, and literal masks.
- Run producer, replay, stress, and Bridge-B in normal and `-O -B` modes.
