# TPC-416 computational protocol

- Pool complete shells `Q=65536,131072,262144,524288`: counts `5709,10749,20390,38635`.
- Use `H=66`, `N=264`, and origin lower bound `10^6`.
- Alternate CRT residues on the pooled increasing prime order.
- Preserve source-shell labels and explicit `m_minus=37741,m_plus=37742`.
- Independent replay rebuilds the sieve, CRT, labels, and literal masks.
- Run producer, replay, stress, and Bridge-B in normal and `-O -B` modes.
