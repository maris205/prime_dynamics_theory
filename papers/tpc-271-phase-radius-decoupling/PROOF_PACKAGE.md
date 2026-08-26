# TPC-271 proof and certificate package

## Exact finite statements

1. The TPC-269 finite operator and rank-three projection are reused without
   changing the physical shell, masks, cutoff registry, or profile interface.
2. The nine residual norm lanes are positive and every stored residual scalar
   interval is strictly negative.
3. The identities
   `Xi=Xi_W*Xi_G` and `Xi/Xi_C=|kappa|^(-6)` are exact on every row.
4. Outward interval cubing and positive division preserve containment.

## Certified dyadic lane table

```text
pair       Xi_W ratio                    Xi_G ratio                    Xi ratio
64->128    [0.365585070520,0.365732732926] [0.633925939307,0.633925939307] [0.231753859227,0.231847466257]
96->192    [0.103825363899,0.103863382316] [230.769819233,230.769819233]    [23.9597604587,23.9685339622]
128->256   [0.466740885639,0.466927278947] [15.3653151604,15.3653151604]    [7.17162080603,7.17448479796]
192->384   [1.10084265028,1.10124579251]   [0.729362778995,0.729362778995]  [0.802913654645,0.803207691586]
```

The corresponding source/output/radius classifications are

```text
64->128:  SOURCE_DROP_BELOW_ONE_HALF / OUTPUT_DROP_BELOW_THREE_QUARTERS / RADIUS_DROP_BELOW_ONE_QUARTER
96->192:  SOURCE_DROP_BELOW_ONE_EIGHTH / OUTPUT_RISE_ABOVE_230 / RADIUS_RISE_ABOVE_23
128->256: SOURCE_DROP_BELOW_ONE_HALF / OUTPUT_RISE_ABOVE_15 / RADIUS_RISE_ABOVE_SEVEN
192->384: SOURCE_RISE_ABOVE_ONE / OUTPUT_DROP_BELOW_THREE_QUARTERS / RADIUS_DROP_BETWEEN_THREE_QUARTERS_AND_ONE
```

## Profile controls

At `N=96,128,256`, the source lane is profile-invariant (the source vector is
unchanged), the output lane ratio is below `9/10`, and the radius ratio lies in
`(1/2,3/4)`. All three controls preserve the negative-real-axis phase.

## Status firewall

- `PROVED_EXACT_FINITE`: lane factorization and endpoint-coordinate identities.
- `NUMERICALLY_CERTIFIED_FINITE`: nine phase records and four dyadic lane
  records.
- `NUMERICALLY_CERTIFIED_FINITE`: output-lane domination of the `96->192`
  normalized-radius spike.
- `OPEN_ASYMPTOTIC`: source-level signed phase, source-level radius, profile or
  cutoff uniformity, arithmetic `L2`, and full Gate B.
- `FIXED_POWER_CREDIT = 0`: no finite ratio is promoted to a power estimate.

The producer imports only the released TPC-269 finite engine. The independent
checker has its own sieve and operator replay; the stress audit rejects altered
threshold metadata and any asymptotic promotion.
