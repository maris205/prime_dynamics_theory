# TPC-271 paper plan

## Question

TPC-270 found a `DROP_RISE_RISE_DROP` pattern for the endpoint-normalized
residual radius, but its scalar phase was not recorded in the same certificate.
The next minimal question is whether a radius spike is explained by phase
alignment or by one of the two residual norm lanes.

## Frozen object

Use the exact finite TPC-269 interface: the prime shell, outer `q` weight, unit
masks, deleted diagonal, source beta, registered `z_N=floor(log N)` cutoff,
the two-kernel convex profile, and the rank-three four-block projection. Keep
the six base rows and the three matched `theta=1/2` controls from TPC-270.

## New coordinates

Write

```text
C_perp = <(I-P_3)w,(I-P_3)g>,
W_perp = ||(I-P_3)w||^2,
G_perp = ||(I-P_3)g||^2,
R^2 = W_perp G_perp,
kappa = C_perp/sqrt(W_perp G_perp).
```

Introduce rational sixth-power coordinates

```text
Xi_W = W_perp^3/N^5,
Xi_G = G_perp^3/N^5,
Xi_C = |C_perp|^6/N^10,
Xi   = (R^2)^3/N^10.
```

The exact identities are `Xi=Xi_W*Xi_G` and
`Xi/Xi_C=|kappa|^(-6)`. They separate radius size, source/output lane
attribution, and signed phase alignment without introducing `N^(5/3)` into a
finite rational certificate.

## Claim-bearing registry

Four dyadic lane records are certified. Their source/output/radius threshold
classes are respectively:

```text
64->128:  source < 1/2, output < 3/4, radius < 1/4
96->192:  source < 1/8, output > 230, radius > 23
128->256: source < 1/2, output > 15, radius > 7
192->384: source > 1,   output < 3/4, radius in (3/4,1)
```

All six base rows and all three profile controls have outward-certified
negative-real-axis scalar phase. The profile controls leave the source lane
invariant while reducing the output lane below `9/10`.

## Intended result class

`NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT`.

The finite claim says that, on this declared registry, phase sign does not
track normalized radius variation and the `96->192` radius spike is output-lane
dominated. It is not an asymptotic phase theorem, an independence theorem, a
source-level radius bound, an arithmetic `L2` estimate, or a twin-prime result.

## Validation

The producer uses the released TPC-269 exact interval engine. The independent
checker reimplements the sieve, Mobius weights, comparison factor, prime shell,
two kernels, projection, and all lane coordinates in floating point. A separate
stress audit attacks the threshold metadata, phase lock, and forbidden
asymptotic promotion.
