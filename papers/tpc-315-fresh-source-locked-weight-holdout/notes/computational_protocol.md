# TPC-315 computational protocol

* Source interval: `I={641,...,1280}`, scale `1280`, height `H=66`.
* Shells: primes in `(Q,2Q]` for `Q=24,36,54,80`; cardinalities `6,9,12,15`.
* Rows: all eight combinations of `Q` and kernel exponent `s=1,2`.
* Menu lock: verify the exact TPC-314 producer/certificate hashes and the
  three laws before fresh Gram target recomputation.
* Fresh targets: exact Gram minimum modulo global sign and all-positive
  maximum, enumerated by Gray code.
* Arithmetic: `Fraction` for source outputs, Gram entries, extrema, and C/R
  laws; rational atanh series for L.
* Log enclosure: 120 positive terms, `z<=1/3`, and the stated geometric tail.
* Interval grid: floor lower endpoints and ceiling upper endpoints at
  `10^-36` after each operation.
* Certificate: canonical sorted-key JSON with payload hash, exact-rational
  digests, interval hashes, source/target provenance, and claim firewall.
* Replays: producer, independent checker, stress suite, and local Bridge-B;
  normal and optimized Python executions are required.

No random seed, midpoint logarithm, external data feed, or time-dependent
parameter enters the certificate.  Display decimals are for readability;
classifications and law orders use interval endpoints.
