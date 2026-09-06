# TPC-408 computational protocol

- Fixed integers: `H=66`, `N=264`; origin lower bound `10^6`.
- Shells: every prime `Q<p<=2Q` for `Q=65536,131072`.
- Profile: CRT residue `0` for even index and `-N` for odd index; all primes
  are retained even when the shell count is odd.
- Exact arithmetic: Python `Fraction`, integer CRT, canonical JSON SHA-256.
- Independent validation: fresh sieve, CRT replay, per-prime/per-coordinate
  literal masks, exact row-energy and adjacent-coefficient comparison.
- Release QA: normal and `-O -B` producer, independent, stress, and Bridge-B
  runs must have identical stdout and empty stderr.
