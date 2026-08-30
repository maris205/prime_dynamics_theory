# TPC-312 computational protocol

* Source indices: `321,...,640` (320 entries).
* Divisor cutoff selected by the frozen scale rule: `U=7`.
* Kernel: `K_H(h) = H^(2s)/(H^2+h^2)^s`, with `H=66`, `s=1,2`.
* Shells: primes in `(Q,2Q]` for `Q=24,36,54,80`; cardinalities are
  `6,9,12,15`.
* Arithmetic: Python `Fraction` throughout physical outputs, Gram entries, and
  sign energies.
* Enumeration: first sign fixed to `+1`; reflected Gray traversal; total
  classes `2*(32+256+2048+16384)=37440`.
* Rank check: exact rational outputs reduced modulo the prime `1000000007`.
* Certificate: canonical sorted-key JSON with a payload digest and reduced
  ratio digests.
* Replays: producer check, an independent checker that rebuilds the operator,
  and a small exact stress suite.  Normal and optimized Python runs are
  required at release time.

No random seed, floating-point optimizer, external data feed, or ambient time
enters the certificate.
