# TPC-415 computational protocol

- Pool complete shells `Q=65536,131072,262144`: counts `5709,10749,20390`.
- Use `H=16,32,66,128`, `N=4H`, and origin lower bound `10^6`.
- Alternate CRT residues on the pooled increasing prime order.
- Preserve source-shell labels in every exact rational amplitude.
- Independent replay rebuilds the sieve, CRT, labels, and literal masks.
- Run producer, replay, stress, and Bridge-B in normal and `-O -B` modes.
