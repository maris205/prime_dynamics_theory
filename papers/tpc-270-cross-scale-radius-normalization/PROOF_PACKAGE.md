# TPC-270 proof and certificate package

## Exact finite identities

1. TPC-269's source-compatible finite operator and rank-three projection are
   reused without changing the physical shell or masks.
2. The residual radius product is positive on all nine registered rows.
3. The endpoint-normalized identity
   `Xi=(R_squared)^3/N^10=(R/N^(5/3))^6` is exact.
4. Cubing positive rational intervals and dividing positive intervals preserve
   outward containment.

## Certified finite result

The base registry has six rows. The derived dyadic ratio intervals are:

```text
64->128:  [0.231753859227, 0.231847466257]  DROP_BELOW_ONE_QUARTER
96->192:  [23.9597604587, 23.9685339622]    RISE_ABOVE_SIXTEEN
128->256: [7.17162080603, 7.17448479796]    RISE_ABOVE_SEVEN
192->384: [0.802913654645, 0.803207691586]  DROP_BETWEEN_THREE_QUARTERS_AND_ONE
```

The three same-scale profile ratios are respectively enclosed in
`(0.5,0.75)`. The adjacent base ratios give the additional finite pattern
`DROP, DROP, RISE, DROP, RISE`.

## Status firewall

- `PROVED_EXACT_FINITE_IDENTITY`: endpoint normalization and interval transfer.
- `NUMERICALLY_CERTIFIED`: all base, derived, and profile-control intervals.
- `REFUTED_SCOPED`: endpoint-normalized radius stability over this finite registry.
- `OPEN`: source-level radius growth, source-level profile/cutoff uniformity,
  arithmetic `L2`, full Gate B, and the twin-prime conclusion.

The producer imports the released TPC-269 finite engine only for exact finite
arithmetic. The independent checker has its own prime sieve, source, operator,
projection, and floating-point normalization replay. It is an audit, not a
replacement for the outward interval enclosure.
