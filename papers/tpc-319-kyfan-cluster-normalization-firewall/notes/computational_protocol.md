# TPC-319 computational protocol

- Source intervals: `I_X={X/2+1,...,X}`, for `X=640,1280,2560`.
- Height: `H=66`; shell: primes `Q<p<=2Q`, with `Q=24,36,54,80`.
- Kernel exponents: `s=1,2`; rows: `3*4*2=24`.
- Cluster sizes: `k=1,2,4,8,16`; adjacent transitions: `2*4*2*5=80`.
- Every row is accumulated in forward and reverse shell order.
- SciPy `eigh` reads the top 17 eigenvalues; NumPy `eigvalsh` supplies an independent
  full-spectrum scalar path.
- The finite guard uses `|K|<=160`, a binary64 entrywise Gram bound, Weyl's inequality,
  solver spread, residual, and outward padding.  For `F_k`, the spectral term is
  multiplied by `k`.
- Reported slopes and gap/effective-rank values are finite observations; only interval
  separations are called numerically certified.
