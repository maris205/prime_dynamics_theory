# TPC-387 computational protocol

- Python 3 and NumPy; BLAS/OpenMP threads fixed to one.
- Sieve primes through 20000 and use shells `(Q,2Q]` for `Q=2048,8192`.
- Use three calibration origins at counts 512 and 768, and two fresh holdout
  origins at count 1024.
- Use block length 128, fixed-three-block and full-relative masks, four laws,
  and local or calibration/extrapolated pooled normalization.
- Fit each slope from calibration means only; record raw metrics, prediction,
  ratio, and log2 slope in canonical JSON.
- Replay in reverse shell order, apply 25 mutations, compile the paper three
  times with `pdflatex`, and require byte-identical PDFs.
