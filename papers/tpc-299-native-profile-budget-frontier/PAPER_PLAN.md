# TPC-299 paper plan

## Question

Once a literal profile prefix reaches a prescribed target angle, how much
native source norm has been spent?  The answer must use the source norm
`||U_k c||_2`, rather than the Euclidean norm of the profile coordinates.

## Frozen objects

- the TPC-298 physical operator, source profiles, and 18-row grid;
- the ordered literal cutoffs
  `3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61`;
- the TPC-295 weighted-minimum, max-cut, and all-positive controls;
- target tolerance `tau=1/2` in normalized shell RMS.

## Planned contributions

1. Derive the exact quadratically constrained least-norm frontier
   `B_{k,tau}(b)` and its ridge/KKT representation.
2. Prove budget feasibility and monotonicity under nested source prefixes.
3. Certify a finite source-budget atlas, including the weighted/positive
   budget gap and the obstruction that survives the full available prefix.
4. Keep all arithmetic `L2`, moving-shell, fixed-power, Gate-B, and
   twin-prime claims outside the certificate.

## Falsification tests

- rebuild every physical column source-first with exact rational accumulation;
- replay every prefix residual and source norm at 70 decimal digits;
- solve the threshold frontier independently by a separate KKT replay;
- test exact one-dimensional, nested-image, infeasible, and zero-budget
  fixtures;
- require normal/optimized byte-identical checks, canonical JSON, provenance
  locks, and a warning-free embedded-font PDF.

## Next decision rule

If weighted source budget remains much larger than the positive control,
continue to a budget-constrained frontier on an enlarged/growing shell.  If
the gap collapses under a richer profile family, attack that apparent escape
before assigning any asymptotic credit.
