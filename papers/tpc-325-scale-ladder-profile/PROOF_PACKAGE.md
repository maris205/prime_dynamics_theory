# TPC-325 proof package

## Proposition 1 — positive-semidefinite typing

For every finite rung and every declared sign vector, `G_0` and `G_e` are
positive semidefinite.  Their traces are positive on the frozen panel, so the
ordered normalized profiles are probability vectors.

**Proof.** Each matrix is of the form `A^*A` (or a finite sum of such matrices),
which is positive semidefinite.  The producer and the independent replay check
positive finite traces.  Spectral decomposition then gives nonnegative
eigenvalues summing to the trace, and normalization gives a probability vector.
`[PROVED_EXACT_FINITE]`

## Proposition 2 — amplitude/shape separation

For every `a>0`, `pi(aG)=pi(G)` while `tr(aG)=a tr(G)`.  Consequently a
trace-ratio trend cannot by itself imply a profile trend.

**Proof.** Positive scalar multiplication multiplies every eigenvalue by `a`
and cancels in the normalized quotient.  The trace is multiplied by `a`.
`[PROVED_EXACT_FINITE]`

## Proposition 3 — fixed-origin ladder geometry

The four source intervals are strictly nested, all have the prescribed
cardinalities, and are disjoint from the TPC-323/TPC-324 source panels.

**Proof.** The endpoints are `12001` and `12000+N/2`; increasing `N` strictly
increases the right endpoint.  Direct endpoint comparison gives disjointness
from the earlier frozen intervals. `[PROVED_EXACT_FINITE]`

## Finite certified statement

The locked producer, reverse-order independent replay, stress suite, and local
Bridge-B checker certify all-plus profile majorization on `32/32` rows.  The
outward lower TV envelope and outward upper energy envelope are strictly
descending over the four declared rungs.  Alternative-law counts are recorded
without selecting a canonical arithmetic law.
`[NUMERICALLY_CERTIFIED_FINITE]`

## Non-claims

No statement here proves a growing-X profile limit, a uniform source estimate,
arithmetic cancellation, a source-native `L2` bound, fixed-power credit, the
strict `1/400` payment, Route-A/Route-B official passage, or the twin-prime
conjecture.  The official evaluator files named by the Session are absent, so
the local evaluator remains fail-closed.
