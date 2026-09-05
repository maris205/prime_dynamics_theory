# TPC-400 paper plan

## Research question

Does the finite C1 endpoint microgrid and its separation between mean transfer
and origin uniformity persist on a third coordinate-disjoint affine family,
when the comparison is made against a frozen same-law parent interface?

## Locked design

Use the response-blind family

```text
a_j = 7600001 + 401j, 0 <= j < 41
selected indices = (0,8,16,24,32,40)
```

The first three selected origins are calibration and the last three are
holdout. Keep `N=1024`, `Q=8192`, `fixed_c3`, beta two, exponent one, height
66, the four existing normalizations, and laws
`{7/8,15/16,31/32,1}` fixed before readout.

Construct the exact finite probes

```text
M_lambda = (1-lambda) M_all_plus + lambda M_alternating_index
```

and compare each current same-law cohort mean directly with the corresponding
all-origin mean from the hash-locked TPC-399 certificate. The parent interface
is response-blind and is not used to choose current origins or laws.

## Claim classes and decision rule

`PROVED_EXACT_FINITE` covers grid arithmetic, interval disjointness against all
declared prior panels, role assignment, parent hashes, exact rational
interpolation identities, and the declared protocol. `NUMERICALLY_CERTIFIED_FINITE`
covers the 96 finite rows, aggregate counters, and independent reverse-order
replay.

The one-percent origin-spread cap and three-percent cross-family and
within-family caps are diagnostic thresholds only. No observation may promote
an asymptotic threshold, source-valid law, arithmetic `L2` estimate, Route A/B
status, or twin-prime conclusion.

## Required artifacts

The project contains README, derivation/proof packages, producer, independent
checker, adversarial stress test, canonical certificate, route and theorem
notes, Bridge-B artifacts, and byte-identical `paper/main.pdf` and
`paper/paper.pdf`.

## Continuation rule

If the transfer and endpoint split replicate, the next minimal question is a
fourth fresh family. If either transfer or endpoint behavior changes, retain
the result as an obstruction and use the smallest adversarial or normalization
control before attempting any broader interpretation.
