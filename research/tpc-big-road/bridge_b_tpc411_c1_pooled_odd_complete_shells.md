# Bridge B: TPC-411 pooled odd complete shells

TPC-411 pools the complete shells `65536<p<=131072` and
`131072<p<=262144`, retaining `5709+10749=16458` primes.  Each prime keeps
the shell-local amplitude scale `Q_i`; the pooled increasing order uses
alternating CRT residues with `H=66`, `N=264=4H`, and has
`m_minus=m_plus=8229`.

The exact producer certificate, independent fresh-sieve replay, and nine-case
adversarial mutation audit are locked below.  The independent replay literally
visits every per-prime/per-coordinate mask for both local rows.  This Bridge-B
checker is fail-closed: it checks normalized SHA-256 provenance, certificate
schema and theorem firewalls, empty stderr, and equality of normal and
optimized stdout.

The result is one finite synthetic adjacent normalized proxy entry.  It does
not prove a full operator norm, a physical `h_0` theorem, arithmetic signs or
`L2`, a fixed-power saving, Route-B closure, or a twin-prime result.

Run from `prime_dynamics_theory`:

```text
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc411_c1_pooled_odd_complete_shells_checker.py --check
```
