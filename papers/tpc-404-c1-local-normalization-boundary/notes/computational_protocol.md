# Computational protocol

Parameters are `Q=8192`, `N=1024`, `H=66`, and origin lower bound `B=10^6`.
The first 8 primes in the shell `Q<p<=2Q` are used, with cases `m=1,2,3,4`.
The producer uses Python `Fraction` arithmetic and serializes a canonical JSON
digest.  The independent checker reconstructs the formulas without importing
the producer.  The stress checker mutates normalization, identities, case
census, exact-identity flags, and the claim firewall; all five mutations must
be rejected.  Both normal and optimized Python modes are required.
