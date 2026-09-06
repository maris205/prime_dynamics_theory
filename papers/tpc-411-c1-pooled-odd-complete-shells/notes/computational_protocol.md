# TPC-411 computational protocol

- Pool all primes in `(65536,131072]` and `(131072,262144]`: 5709 and 10749.
- Fixed `H=66`, `N=264`, origin lower bound `10^6`.
- CRT profile is alternating on the pooled increasing prime order.
- Amplitudes use each prime's source-shell `Q_i`; all arithmetic is exact.
- Independent checker uses a fresh sieve, CRT, shell labels, and literal masks.
- Normal and `-O -B` producer, replay, stress, and Bridge-B runs are required.
