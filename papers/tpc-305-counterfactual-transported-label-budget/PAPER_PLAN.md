# TPC-305 paper plan

## Question

TPC-304 localized the middle overlap-label fracture, but its crosswalk changed
the physical shell/operator and the source-first target at the same time.  Can
the target-label component be tested while each physical operator is held
fixed?

## Minimal contribution

1. Define a full-shell counterfactual extension: replace labels on an adjacent
   overlap by the optimally globally aligned neighboring label and retain the
   native label off the overlap.
2. Prove the finite protocol and its global-sign invariance exactly.
3. Recompute the constrained native profile budget on each fixed operator for
   the native and transported targets, using a common feasible profile prefix.
4. Certify an 18-case, 36-operator-table atlas and test the target/operator
   orientation at the TPC-304 fracture.

## Frozen scope

The source scale, height, cutoff, moving-shell spine, exponents, tolerances,
profile cutoffs, and parent source-first labels are inherited and hash-locked
from TPC-302 and TPC-303.  The calculation is finite; it is not an asymptotic
statement and does not claim a causal effect.

## Acceptance criteria

- the parent hashes and all 18 counterfactual cases are locked;
- the transported target is reconstructed independently, including the
  off-overlap extension and negative alignment-sign case;
- all 36 operator tables have positive ordered enclosures and normalizer-
  invariant orientation;
- the central `Q=60->70` census is reproduced as 5/6 right-label-cheaper,
  1/6 home-operator-favored, with 3/3 same-prefix cases right-label-cheaper;
- normal/optimized producer, independent replay, stress, and Bridge-B outputs
  agree with empty stderr;
- a clean PDF is stored as `paper/paper.pdf`.
