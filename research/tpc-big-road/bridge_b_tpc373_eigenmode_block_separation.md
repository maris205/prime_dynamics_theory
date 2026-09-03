# Local Bridge-B: TPC-373 eigenmode block separation

This file records the local, fail-closed bridge for TPC-373.  It is not the
official Route-A/Route-B evaluator; those Session-named files are absent from
this checkout.

## Fixed claim boundary

```text
TPC373_FULL_WINDOW_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND
TPC373_COMMON_NORMALIZATION = PROVED_EXACT_FINITE
TPC373_BLOCK_DISTANCE_PARTITION = PROVED_EXACT_FINITE_PREDECLARED
TPC373_EIGENMODE_SELECTION_RULE = PROVED_EXACT_FINITE_DETERMINISTIC
TPC373_EIGENMODE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC373_LAYER_RECONSTRUCTION = NUMERICALLY_CERTIFIED_FINITE
TPC373_RAYLEIGH_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC373_CROSS_BLOCK_DECAY = OPEN
TPC373_CROSS_BLOCK_CAUSALITY = OPEN
TPC373_ORIGIN_UNIFORMITY = OPEN
TPC373_WINDOW_UNIFORMITY = OPEN
TPC373_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC373_GROWING_OPERATOR_BOUND = OPEN
TPC373_SOURCE_UNIFORM_L2 = OPEN
TPC373_ARITHMETIC_ADVANCE = NO
TPC373_FIXED_POWER_CREDIT = 0
TPC373_FULL_GATE_B = OPEN
TPC373_TWIN_PRIME_RESULT = NONE
```

The finite result is that all 18 selected modes are minimum-eigenvalue modes
with distance zero dominant.  On the six beta=2 parent failure rows all eight
layer Rayleigh terms are negative; distances 0--3 carry at least 99.157% of
absolute mass and distances 4--7 at most 0.843%.  This is scoped profile
evidence only and does not establish causality or a decay theorem.

## Required artifacts

The bridge locks the producer, independent checker, adversarial stress suite,
canonical certificate, manuscript source and both PDF copies, final LaTeX
log, all proof/notes files, and this record.  It runs each executable in
normal and optimized Python modes with one BLAS thread per worker, requires
empty standard error, and requires normal/optimized stdout identity.

```text
ROUND2_CLUE = TEST_LAYERWISE_CROSS_BLOCK_DECAY
```
