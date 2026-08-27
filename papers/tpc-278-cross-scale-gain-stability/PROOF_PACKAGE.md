# TPC-278 proof package

## Proposition 1 — sign/gain equivalence

For `D>0,G>0`, expansion gives `G=D+2E`.  Hence `E<0` iff `D/G>1`, and
`E>0` iff `D/G<1`.

## Proposition 2 — finite shell/clock instability

On the twelve declared rows in the certificate, exact rational replay gives
eight `E<0` rows and four `E>0` rows.  The sign changes occur in the fixed-
scale shell paths

```text
(128,Q=5)->(128,Q=6),
(192,Q=6)->(192,Q=7),
(256,Q=5)->(256,Q=6),
```

and the clock path `(192,H=29)->(192,H=32)`.  All other listed parameters
are held fixed along each path.

## Proposition 3 — scope firewall

The finite flips do not imply that the actual growing TPC schedule flips
infinitely often.  Conversely, the three natural controls do not prove
uniform stability.  Both the source-level schedule and any asymptotic
coherence estimate remain open.

The exact replay uses the TPC-277 source code locked by SHA-256; an independent
column-major checker verifies every row digest and interval.
