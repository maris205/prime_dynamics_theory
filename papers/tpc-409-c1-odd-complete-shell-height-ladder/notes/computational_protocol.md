# TPC-409 computational protocol

- Fixed shell: every prime `65536<p<=131072`, count `5709`.
- Heights: `H=16,32,66,128`; windows `N=4H`; origin lower bound `10^6`.
- CRT profile: zero on even indices and `-N` on odd indices; all primes retained.
- Exact producer: integer CRT, `Fraction` arithmetic, canonical JSON digest.
- Independent checker: fresh sieve/CRT and literal per-prime, per-coordinate
  masks for both local rows at all four heights.
- Release QA: normal and `-O -B` producer, independent, stress, and Bridge-B
  checks with empty stderr and identical outputs.
