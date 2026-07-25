# Roadmap after RH-156

The native reset architecture now closes at finite horizon: packet existence,
overlap coherence, correlated transport, delayed conditioning, native tail,
and a positive support floor all compose.  The terminal-half common floor is
`3.262e-8`.

1. **RH-157: directional bridge audit.** Compare native recent-memory support
   with the projected-cross Gram/wedge support used in RH-130--RH-148.  Prove
   a transfer theorem if a singular-value gate holds, otherwise isolate the
   exact mismatch.
2. **RH-158: analytic block criterion.** State the minimal all-level laws for
   selected eigenvalues, overlap suffixes, and bridge constants.
3. **RH-159: ten-layer review.** Decide whether the native route replaces or
   supplements the older recursive directional route.

No finite native-support floor is promoted to Stage A or a spectral-zero
claim.
