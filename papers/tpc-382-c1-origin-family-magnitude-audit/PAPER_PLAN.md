# TPC-382 paper plan

## Question

The TPC-381 origin-family replay preserved the finite `(0,3,3)` support profile.
Its declared next question is whether the normalized band magnitude itself is
stable across the two protocol-matched `N=2048` origin families.  TPC-382 fixes
that question as a certificate-level audit before reading any parent metric.

## Design

1. Hash-lock TPC-379, TPC-380, and TPC-381 source/certificate pairs.
2. Use TPC-380 and TPC-381 as the same-count cohort: six origins, three Q
   anchors, and four laws.
3. For every law/Q cell compute `(max-min)/mean` over the six values and compare
   with the predeclared one-percent cap.
4. Recompute the same statistic on TPC-379 as an `N=1024` scale control, then
   compare matched law/Q means between the two counts.
5. Treat all conclusions as finite observations; do not promote a normalized
   diagnostic to an arithmetic source law.

## Claim target

The target is a new finite magnitude certificate: all-plus high-Q stability in
the matched-count cohort, together with a law-dependent spread census and a
finite refutation of one-percent cross-count magnitude invariance.  The latter
is a scoped hypothesis, not a theorem about the underlying operator family.

## Next decision rule

If the all-plus magnitude is stable only under the local normalization, test a
pooled cross-origin normalization.  If it is unstable even there, record the
obstruction and stop promoting magnitude persistence.  In either case keep
origin uniformity, source validity, and the Route-B gates open.
