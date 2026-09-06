# Bridge B: TPC-415 three-shell height extension

TPC-415 audits the three complete shells `Q=65536,131072,262144` at
`H=16,32,66,128`, with `N=4H`.  All `36848` primes are retained, amplitudes
remain shell-local, and pooled alternating CRT has `m_minus=m_plus=18424`.

The exact certificate, independent fresh-sieve literal replay, and 11-case
mutation audit are locked by the checker.  It verifies normalized SHA-256
provenance, schema and firewalls, empty stderr, and normal/optimized stdout
equality.  This is finite synthetic proxy evidence, not a full operator,
physical, arithmetic, fixed-power, Route-B, or twin-prime theorem.

Run from `prime_dynamics_theory`:

```text
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc415_c1_three_shell_height_extension_checker.py --check
```
