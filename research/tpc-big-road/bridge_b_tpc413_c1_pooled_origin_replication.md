# Bridge B: TPC-413 pooled CRT-origin replication

TPC-413 tests three distinct representatives `o_s=r+sL`, `s=1,2,3`, of the
pooled two-shell CRT profile.  Each representative is audited at
`H=16,32,66,128`, `N=4H`, giving 12 exact rows.  All `16458` primes remain,
shell-local amplitudes are retained, and `m_minus=m_plus=8229`.

Because the representatives differ by the CRT period, every prime residue and
literal mask is identical.  The producer certificate, independent fresh-sieve
replay, and 12-case mutation audit are locked below.  This fail-closed checker
verifies normalized SHA-256 provenance, schema and firewalls, empty stderr, and
normal/optimized stdout equality.

This is finite synthetic proxy invariance, not a full operator, physical,
arithmetic, fixed-power, Route-B, or twin-prime theorem.

Run from `prime_dynamics_theory`:

```text
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc413_c1_pooled_origin_replication_checker.py --check
```
