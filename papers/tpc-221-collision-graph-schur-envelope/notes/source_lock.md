# TPC-221 source lock

- Upstream exact object: `research/tpc-big-road/bridge_b_prime_ap_collision_crosswalk.md`.
- Upstream checker: `research/tpc-big-road/tpc_bridge_b_prime_ap_collision_crosswalk_checker.py`.
- The Schur and PSD arguments are finite-dimensional linear algebra; no external analytic
  estimate is imported.
- The saturation fixture is a literal row construction with `h=5`, `H=500`, and four
  distinct primes congruent to `1 mod 5`.
- Numerical labels in the certificate are exact integers or `Fraction` strings.
