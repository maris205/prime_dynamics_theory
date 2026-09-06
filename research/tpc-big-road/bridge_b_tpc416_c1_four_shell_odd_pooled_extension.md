# Bridge B: TPC-416 four-shell odd pooled extension

TPC-416 pools the complete shells `Q=65536,131072,262144,524288`, retaining
`75483` primes.  At `H=66,N=264`, shell-local amplitudes and pooled alternating
CRT give the explicit odd parity counts `m_minus=37741,m_plus=37742`.

The exact certificate, independent fresh-sieve literal replay, and 10-case
mutation audit are locked by the checker.  It verifies normalized SHA-256
provenance, schema and firewalls, empty stderr, and normal/optimized stdout
equality.  This is one finite synthetic proxy entry, not a full operator,
physical, arithmetic, fixed-power, Route-B, or twin-prime theorem.

Run from `prime_dynamics_theory`:

```text
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc416_c1_four_shell_odd_pooled_extension_checker.py --check
```
