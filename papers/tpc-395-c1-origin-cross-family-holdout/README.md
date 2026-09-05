# TPC-395 — c=1 origin obstruction across a fresh family

Author: Liang Wang  \\
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

The TPC-394 origin-spread split transfers to a third, coordinate-disjoint
affine family: all-plus remains origin-stable under all four normalizations,
whereas alternating-index fails the one-percent origin-spread rule in every
normalization, with spreads about `0.0671–0.0683`.  The new-family means agree
with the frozen TPC-394 baseline within `2.33%` in all six holdout comparisons,
and all within-family holdout-transfer cells pass the 3% cap.  This is a finite
cross-family replication, not a growing or source-valid theorem.

## What is new

TPC-394 directly reproduced a law-dependent origin obstruction on an
eight-origin family.  TPC-395 tests whether that signal is family-local by
freezing TPC-394's cell means as a response-blind baseline and evaluating a
third family with three calibration and three holdout origins at the same
`N=1024`.  The cross-family comparison and the new-family origin spread are
reported separately.

## Frozen protocol

```text
schema = TPC395_C1_ORIGIN_CROSS_FAMILY_HOLDOUT_V1
parent baseline = TPC-394 all-origin cell means (hash locked)
candidate grid = a_j = 5600001 + 401 j, 0 <= j < 41
selected indices = 0,8,16,24,32,40
origins = 5600001,5603209,5606417,5609625,5612833,5616041
calibration origins = 5600001,5603209,5606417
holdout origins = 5609625,5612833,5616041
window count = N=1024 for every origin
block length = 128; band mode = fixed_c3; Q = 8192
kernel exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index
normalizations = local_diagonal, pooled_train_scalar,
                 origin_scalar, frozen_train_1024_scalar
within-family origin-spread cap = 0.01
cross-family mean cap = 0.03; within-family transfer cap = 0.03
spectral cap = 0.64; Schur cap = 0.83
```

The certificate contains 48 rows and 8 cells.  Parent means are read only
from the exact TPC-394 certificate after its code and certificate hashes are
checked; no current response is used to select a cell, origin, law, or cap.

## Finite findings

```text
rows / cells = 48 / 8
within-family origin-stable cells = 4/8
  all-plus = 4/4; alternating-index = 0/4
cross-family calibration passes = 8/8
cross-family holdout passes = 8/8
within-family holdout-transfer passes = 8/8
maximum cross-family holdout error by normalization:
  local_diagonal             0.019120856868882985
  pooled_train_scalar        0.023261029846088688
  origin_scalar              0.023245265196004006
  frozen_train_1024_scalar   0.023289195722825839
spectral failures = 24/48 (all-plus rows only)
Schur failures = 0/48
```

The alternating-index within-family spreads in local/pooled/origin/frozen
order are `0.068267525703845117`, `0.067105244599520317`,
`0.067101222970965949`, and `0.067105244599520331`.  The all-plus spreads
are at most `5.2094472553133891e-5`.  The largest cross-family holdout error
is `0.023289195722825839`, below the predeclared 3% cap.  Thus the finite
law split transfers across families while the absolute normalized level also
remains close to the TPC-394 baseline.

The finite spectral cap fails in all 24 all-plus rows and in no alternating
row; the Schur cap fails in no row.  Neither diagnostic is promoted to a
growing operator statement.

## Exact and independent certification

The producer accumulates the shell in ascending order.  The independent
checker validates the TPC-394 parent and rebuilds the new matrices in
descending shell order without importing the producer.  It recomputes row
values, parent-relative errors, cohort spreads, and all counters.  A rational
13-point anchor at `[5600001,5600014)` with `Q=8` checks positive geometry and
exact symmetry.  A 25-case mutation suite attacks the certificate contract.
Normal and optimized producer/checker/stress outputs are required to agree;
Bridge-B locks every release artifact.

## Claim firewall

```text
TPC395_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC395_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC395_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC395_CROSS_FAMILY_PANEL = NUMERICALLY CERTIFIED FINITE_48_ROWS
TPC395_CROSS_FAMILY_MEAN_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED
TPC395_WITHIN_FAMILY_ORIGIN_AUDIT = NUMERICALLY CERTIFIED FINITE SCOPED
TPC395_SPECTRAL_ENVELOPE = REFUTED_ON_DECLARED_FINITE_PANEL
TPC395_SCHUR_ENVELOPE = NUMERICALLY CERTIFIED FINITE SCOPED ONLY
TPC395_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC395_GROWING_OPERATOR_BOUND = OPEN
TPC395_SOURCE_UNIFORM_L2 = OPEN
TPC395_ARITHMETIC_ADVANCE = NO
TPC395_FIXED_POWER_CREDIT = 0
TPC395_FULL_GATE_B = OPEN
TPC395_TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are absent from this checkout.  Local
proof/checker/Bridge-B evidence is fail-closed finite consistency only.  The
cross-family replication does not establish source-valid origin uniformity,
an asymptotic law, arithmetic `L2`, Route-A/Route-B closure, or a twin-prime
result.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-395-c1-origin-cross-family-holdout/code/tpc395_c1_origin_cross_family_holdout.py --check
python -O -B papers/tpc-395-c1-origin-cross-family-holdout/code/tpc395_c1_origin_cross_family_holdout.py --check
python -B papers/tpc-395-c1-origin-cross-family-holdout/experiments/tpc395_independent_checker.py --check
python -O -B papers/tpc-395-c1-origin-cross-family-holdout/experiments/tpc395_independent_checker.py --check
python -B papers/tpc-395-c1-origin-cross-family-holdout/experiments/tpc395_adversarial_certificate_stress.py --check
python -O -B papers/tpc-395-c1-origin-cross-family-holdout/experiments/tpc395_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc395_c1_origin_cross_family_holdout_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc395_c1_origin_cross_family_holdout_checker.py --check
```

The required release PDF is `paper/paper.pdf`, byte-identical to
`paper/main.pdf`.
