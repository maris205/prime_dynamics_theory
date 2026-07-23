# Route update after RH-109

## What RH-109 closes

RH-108 asked whether a determinant or volume surrogate could supply physical
fourth-cross support.  RH-109 gives the strongest generic exterior-power
answer:

1. a recent spectral four-volume, after paying the RH-108 tail, is a valid
   lower certificate for `s4/s1`;
2. the reduced matrix `M2-A^2` contains both the spectral and trace exterior
   quantities exactly;
3. the `e4` trace surrogate pays an unavoidable `sqrt(binom(r,4))` factor
   unless exterior concentration is added;
4. both certificates close every fine update at `tau=1e-8` on the archived
   chain.

## The route boundary

The normalized spectral volume factors as

```text
nu4 = (s2/s1)(s3/s1)(s4/s1).
```

The scalar inversion interval `nu4 <= s4/s1 <= nu4^(1/3)` is sharp even in a
trace-one source-seeded normalized-memory class with fixed diagonal blocks.
Therefore a scalar determinant/volume law cannot by itself reproduce the
direct fourth-mode certificate in the undecidable band `tau^3 < nu4 < tau`.
This is an information boundary, not a failure of the fine numerical chain.

## Next candidate layer

The next paper should test the missing factor directly:

- seek a physical upper law for the relative three-mode capacity
  `Lambda23=(s2/s1)(s3/s1)`;
- combine it with a source/observation wedge lower bound to recover
  `s4/s1 = nu4/Lambda23`;
- separately measure exterior concentration
  `e4(K*K)/(s1^2 s2^2 s3^2 s4^2)` to decide whether the reduced trace route
  can avoid the worst binomial penalty.

If neither quantity has a stable fine-scale law, RH-109 marks determinant-only
support as a rigorous route boundary and the route should return to direct
physical transversality.  Moving-cloud, arithmetic trace, zero-identification,
and Hilbert--Polya work remain deferred.
