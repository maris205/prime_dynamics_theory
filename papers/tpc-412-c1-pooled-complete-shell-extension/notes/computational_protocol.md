# TPC-412 computational protocol

- Pool all primes in `(65536,131072]` and `(131072,262144]`: 5709 and 10749.
- Use `H=16,32,66,128`, `N=4H`, and origin lower bound `10^6`.
- Alternate CRT residues on the pooled increasing prime order.
- Use each prime's source-shell `Q_i` in its exact rational amplitude.
- Independent replay uses a fresh sieve, CRT, shell labels, and literal masks.
- Run producer, replay, stress, and Bridge-B in normal and `-O -B` modes.
