# TPC-386 computational protocol

- Python 3 with NumPy; BLAS/OpenMP threads fixed to one.
- Sieve primes through 20000 and use `(Q,2Q]` for `Q=2048,8192`.
- Use origins `2200001,2204011,2208021` for calibration at `N=512` and
  `2212031,2216041` for holdout at `N=1024`.
- Use block length 128, the four fixed sign laws, and local or calibration-only
  pooled normalization.
- `fixed_c3` uses three adjacent block distances at both counts;
  `full_relative` uses all block pairs at each count.
- Store canonical JSON, replay it in reverse prime order, and run 25 mutation
  checks. Compile the paper twice with `pdflatex`; `main.pdf` and `paper.pdf`
  must be byte-identical.
