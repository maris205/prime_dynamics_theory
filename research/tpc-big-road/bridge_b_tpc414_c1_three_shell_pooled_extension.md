# Bridge B: TPC-414 three-shell pooled extension

TPC-414 pools the complete shells at `Q=65536,131072,262144`, retaining
`5709+10749+20390=36848` primes.  At `H=66,N=264`, shell-local amplitudes and
pooled alternating CRT give `m_minus=m_plus=18424`.

The exact certificate, independent fresh-sieve literal replay, and nine-case
mutation audit are locked by the checker below.  It verifies normalized
SHA-256 provenance, certificate schema and firewalls, empty stderr, and normal
and optimized stdout equality.  The result is one finite synthetic proxy entry,
not a full operator, physical, arithmetic, fixed-power, Route-B, or twin-prime
theorem.

Run from `prime_dynamics_theory`:

```text
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc414_c1_three_shell_pooled_extension_checker.py --check
```
