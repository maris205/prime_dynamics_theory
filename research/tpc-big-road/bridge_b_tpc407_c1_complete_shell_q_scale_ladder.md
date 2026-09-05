# Bridge B: TPC-407 complete-shell Q-scale ladder

TPC-407 extends TPC-406 along a finite prime-shell scale ladder.  At fixed
`H=66`, `N=264`, and origin lower bound `10^6`, the certificate selects all
primes in the even complete shells at `Q=4096,8192,16384,32768`.  The shell
counts are `464,872,1612,3030`.

For the explicit alternating CRT profile, the exact local identity and
Cauchy--Schwarz proof give

```text
0 <= z <= t_1/(a_min sqrt(S_0 S_1)) <= 4/(a_min H) <= 4/H.
```

The four rows store exact rational CRT periods, amplitudes, energies, and
squared bounds.  The independent checker literally rebuilds each shell and
replays both masked row energies.  Eight mutation tests reject altered
scales, shell counts, domain, bound, case, and firewall fields.

This is a finite one-entry synthetic-proxy result.  It is not a full
normalized operator theorem, a physical `h_0` theorem, an arithmetic sign or
`L2` estimate, a fixed-power saving, Route-B closure, or a twin-prime result.
