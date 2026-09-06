# Bridge B: TPC-408 complete-shell Q-scale extension

TPC-408 extends the finite TPC-407 local proxy to the complete odd shells at
`Q=65536` and `Q=131072`, with `5709` and `10749` primes.  Every prime is
retained.  The alternating CRT profile uses `m_minus=floor(r/2)` and
`m_plus=ceil(r/2)`, and the exact bound is

```text
0 <= z <= t_1/(a_min sqrt(S_0 S_1)) <= 4/(a_min H) <= 4/H.
```

The certificate is exact rational data.  The independent checker reconstructs
the prime shells, CRT origin, and every per-prime/per-coordinate mask before
comparing both local row energies and the adjacent coefficient.  The stress
checker rejects nine altered contract fields.  The checker below locks every
release artifact by normalized SHA-256, requires empty stderr, and requires
normal and optimized outputs to agree.

This is a finite theorem for one synthetic adjacent normalized proxy entry.
It does not prove a full operator norm, physical `h_0` result, arithmetic sign
or `L2` estimate, fixed-power saving, Route-B closure, or twin-prime result.
