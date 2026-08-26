# TPC-270 paper plan

## Question

TPC-269 left the residual radius unnormalized: a finite quarter-sector ratio does
not say how the Schur radius grows. The next minimal question is whether the
source-compatible finite registry has a stable radius after normalization by
the endpoint scale `N^(5/3)` inherited from the TPC-265 budget.

## Frozen object

Use the exact finite operator of TPC-269: prime shell, outer `q` weight, unit
masks, deleted diagonal, source beta, registered `z_N=floor(log(N))` cutoff,
and the rank-three four-block projection. Use `theta=0` as the base profile and
`theta=1/2` at three matched control scales.

## New observable

For the positive finite radius product

```text
R_(N,theta)^2 = ||(I-P_3)w_N||^2 ||(I-P_3)g_(N,theta)||^2,
Xi_(N,theta) = (R_(N,theta)^2)^3 / N^10
              = (R_(N,theta)/N^(5/3))^6.
```

The sixth-power form keeps every finite normalization and ratio rational once
the upstream interval has been certified. It is a monotone encoding of the
endpoint-normalized radius, not an asymptotic exponent assertion.

## Claim-bearing registry

Six base rows, four dyadic scale ratios, five adjacent-scale ratios, and three
profile-to-base ratios are certified. The dyadic ratios for
`64->128->256` and `96->192->384` expose a separated
`DROP_RISE_RISE_DROP` pattern; the three profile controls lie in
`1/2 < Xi_(theta=1/2)/Xi_(theta=0) < 3/4`.

## Intended result class

`NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT`.
The finite registry can refute a stability claim over that registry. It cannot
prove or disprove a source-level asymptotic radius bound, pay fixed-power
credit, establish arithmetic `L2`, or close Gate B.

## Follow-up

Use the measured finite variation to formulate an explicit source-level radius
upper-bound target with a declared power and uniformity range; do not infer it
from the finite ratios.
