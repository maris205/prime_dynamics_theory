# TPC-308 paper plan

## Question

TPC-307 found three budget/holdout discordances after moving the two
directional tasks into one common ambient operator.  Are those reversals
stable when the native labels on each exclusive holdout are replaced by all
binary completions within a small, explicitly bounded Hamming radius?

## Minimal contribution

1. Define the finite Hamming completion ball for a fixed prediction and prove
   that exhaustive enumeration gives its exact minimum and maximum loss.
2. Prove radius monotonicity and radius-zero recovery, so the native TPC-307
   diagnostic is the first layer of the new envelope rather than a separate
   experiment.
3. Keep the overlap fit, coefficients, profile prefix, common ambient rows,
   and budget preference fixed; vary only the exclusive completion labels.
4. Replay all 18 locked shell-transition cells at radii `0,1,2`, producing 54
   envelope observations and 702 candidate evaluations.
5. Determine whether the TPC-307 discordance is robust, fragile, or
   unresolved under this finite adversarial completion family.

## Acceptance criteria

- The TPC-307 code and canonical certificate are provenance-locked.
- The producer, an independent NumPy checker, and an exact small stress suite
  agree on the protocol and the published census.
- Radius `0` recovers the TPC-307 13/3/2 agreement census.
- The radius-one and radius-two censuses are respectively 11/2/5 and 10/1/7
  (concordant/discordant/unresolved), with every surviving discordance on the
  final `70 -> 90` transition.
- The paper and local Bridge-B checker make the finite/numerical claim ceiling
  explicit; no causal, asymptotic, arithmetic, or twin-prime claim is made.

## Decision rule for the next paper

The surviving final-transition cells are not sufficient to identify a causal
completion law.  The next minimal audit should perturb the *profile prefix*
and test whether the residual discordance is invariant to the selected
finite-dimensional source subspace.  That is a distinct stress axis from the
completion envelope and is more informative than adding more radii alone.
