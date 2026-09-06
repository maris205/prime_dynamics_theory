# Bridge B: TPC-410 odd complete-shell height replication

TPC-410 fixes `Q=131072`, retains all `10749` primes in the complete odd shell,
and tests `H=16,32,66,128` with `N=4H`.  The explicit profile has
`m_minus=5374` and `m_plus=5375`.  At every height the exact proxy entry obeys

```text
0 <= z <= t_1/(a_min sqrt(S_0 S_1)) <= 4/(a_min H) <= 4/H.
```

The independent checker rebuilds the sieve and CRT for every height and
literally replays every per-prime/per-coordinate mask.  The fail-closed
checker below locks all release files by normalized SHA-256, requires empty
stderr, and requires normal and optimized outputs to agree.

The finite result concerns one synthetic adjacent normalized proxy entry.  It
does not prove a full operator norm, physical `h_0` theorem, arithmetic sign
or `L2` estimate, fixed-power saving, Route-B closure, or twin-prime result.
