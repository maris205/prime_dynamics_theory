# Bridge B: TPC-412 pooled complete-shell extension

TPC-412 extends the pooled complete shells `65536<p<=131072` and
`131072<p<=262144` across `H=16,32,66,128`, with `N=4H`.  All
`5709+10749=16458` primes are retained, each amplitude keeps its source-shell
scale, and the pooled alternating CRT profile has `m_minus=m_plus=8229`.

The exact producer certificate, independent fresh-sieve replay, and 11-case
adversarial mutation audit are locked below.  The independent replay literally
visits every per-prime/per-coordinate mask for both local rows at all four
heights.  The fail-closed checker verifies normalized SHA-256 provenance,
certificate schema and theorem firewalls, empty stderr, and normal/optimized
stdout equality.

This is a finite four-height synthetic adjacent normalized proxy extension.  It
does not prove a full operator norm, physical `h_0`, arithmetic signs or
`L2`, a fixed-power saving, Route-B closure, or a twin-prime result.

Run from `prime_dynamics_theory`:

```text
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc412_c1_pooled_complete_shell_extension_checker.py --check
```
