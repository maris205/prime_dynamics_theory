# TPC-350 paper plan

## Research question

Does the exact zero-sum prime-incidence lower witness from TPC-349 retain a
nontrivial finite response when both the interval length and the shell scale
are moved to fresh panels?

## Minimal continuation

TPC-349 used two origins, three lengths, and a shell ladder ending at `Q=80`.
TPC-350 keeps its literal matrix and beta rule, but freezes three unused origins,
four lengths, and the wider ladder `Q=36,80,128,256`.  The two source laws are
`all_plus` and `alternating_index`; the kernel exponents remain one and two.
This separates a fresh-position replication from a high-shell stress test.

## Primary outputs

1. Rebuild the exact incidence Gram identity and induced-norm lower witness.
2. Certify positivity, support, defect ratio, and coordinate-baseline comparison
   on all 192 rows.
3. Record the four-length ratio series for each fixed origin, shell, exponent,
   and source law; monotonicity is descriptive only.
4. Use an exact rational multi-hit anchor at the fresh interval `[97,110]`.

## Decision rule

If positivity survives, record a finite fresh-growth replication.  If the lower
ratio falls at high shell scale or the length series is nonmonotone, record that
as a scoped obstruction to a universal quarter-floor or monotonicity claim.  In
either case, do not infer a source-uniform arithmetic `L2` theorem, a fixed
power of `x`, or a twin-prime result.

## Planned next question

Use the measured scale dependence to decide whether a predeclared
scale-adaptive zero-sum contrast is worth testing, or whether the incidence
route should be frozen and the main effort returned to source-native arithmetic
`L2`.
