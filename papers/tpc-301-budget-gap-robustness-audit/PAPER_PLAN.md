# TPC-301 paper plan

## Title

Tolerance and source-normalization robustness of the native weighted/positive
budget gap

## Continuation question

TPC-300 converted the TPC-299 native budget frontier into exact finite dual
witnesses at one inherited tolerance.  The next smallest hostile question is
whether the class separation survives:

1. a tolerance ladder tau in {1/4, 1/2, 3/4};
2. a common source prefix, so that the two target classes share the same
   feasible source space;
3. three transparent source-side normalizations.

The primary statistic is the weighted-to-positive budget ratio at the first
prefix that makes the weighted target feasible.  Target-specific-prefix and
full-prefix contexts are secondary controls.

## Claim ceiling

- PROVED_EXACT_FINITE: tolerance monotonicity, target homogeneity under the
  relative RMS constraint, threshold-prefix monotonicity, and common-prefix
  normalization invariance.
- NUMERICALLY_CERTIFIED_FINITE: 18 rows, 219 explicit shell targets,
  324 frontier cases, 54 common-prefix normalization checks, and 36
  full-prefix tolerance checks.
- NUMERICAL_OBSERVATION: the finite weighted/positive gap remains above 10
  at every tested tolerance and row.
- MODELING_CHOICE: literal 17-cutoff profile family, inherited row fixture,
  relative target RMS, target classes, common weighted prefix, and the three
  source normalizers.
- OPEN: growing profile budget, arithmetic L2, fixed-power credit, full Gate B,
  and the twin-prime endpoint.

## Validation design

The producer reconstructs rational physical matrices and profile Grams, solves
the finite ridge frontier at 60 decimal digits, and writes outward decimal
intervals.  The independent checker does not import the producer; it rebuilds
the source-first matrices and checks every recorded case.  An exact scalar
stress suite covers tolerance monotonicity, relative homogeneity, and
normalization cancellation.  The Bridge-B checker runs normal and optimized
modes with empty stderr and identical stdout.
