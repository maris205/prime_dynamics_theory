# TPC-314 computational protocol

* Physical source: I={321,...,640}, scale 640, height H=66, exponents s=1,2.
* Shells: primes in (Q,2Q] for Q=24,36,54,80; cardinalities are 6,9,12,15.
* Targets: the TPC-312 exact Gram-minimum sign vector and the all-positive
  vector, read only after the three-law menu is fixed.
* Laws: 1, 1/(p-1), and log(p).
* Arithmetic: Fraction for physical outputs, Gram entries, and the first two
  laws; rational atanh series for logarithms.
* Log enclosure: 120 positive terms, range reduction through z<=1/3, and
  tail 2 z^(2N+1)/((2N+1)(1-z^2)).
* Interval grid: every endpoint is rounded outward to 10^-36.
* Certificate: canonical sorted-key JSON with payload hash, interval hashes,
  and exact ratio hashes for the two rational laws.
* Replays: producer, independent checker, exact stress suite, and local
  Bridge-B checker; normal and optimized Python executions are required.

No random seed, midpoint logarithm, external data feed, or time-dependent
parameter enters the certificate.  The decimal centers in the paper are for
readability only; classifications use interval endpoints.
