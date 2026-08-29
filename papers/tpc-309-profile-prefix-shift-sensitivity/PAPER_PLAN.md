# TPC-309 paper plan

## Question

TPC-308 showed that a finite common-ambient budget/holdout discordance can
survive bounded exclusive-label completions.  Is the location and survival of
that discordance stable under a minimal, source-backed perturbation of the
chosen profile prefix?

## Minimal contribution

1. Define three contiguous 17-cutoff windows in a fixed 19-prime pool: LOW,
   BASE, and HIGH.  BASE is exactly the TPC-308 profile ladder.
2. Keep the Q spine, physical source interval, shell labels, common-ambient
   row construction, alignment rule, and exclusive completion rule fixed.
3. Recompute each ladder's feasible common prefix and constrained frontier,
   rather than silently reusing the BASE coefficients.
4. Evaluate all 18 `(transition, exponent, tolerance)` cells at Hamming radii
   `0,1,2`, with both profile-recomputed and frozen-parent budget comparisons.
5. Determine whether the TPC-308 final-transition obstruction is profile
   invariant, profile fragile, or unresolved.

## Acceptance criteria

- TPC-308 code and canonical result are provenance-locked.
- The producer, standalone NumPy checker, and exact stress suite agree.
- The three ladders produce 54 profile cases and 162 envelope observations.
- BASE recovers TPC-308's `13/3/2`, `11/2/5`, `10/1/7` class censuses.
- LOW and HIGH produce the locked profile-specific censuses and show that the
  strict discordance location is not invariant.
- The manuscript and Bridge-B checker state that all observations are finite
  numerical diagnostics; no causal, asymptotic, arithmetic, or twin-prime
  claim is made.

## Decision rule for the next paper

The profile ladder changes both the feasible prefix and the holdout geometry.
The next smallest useful audit should compare the same profile perturbations
across alternative holdout aggregation rules, especially pooled versus
directional exclusive rows, before assigning a preference to any one holdout
definition.
