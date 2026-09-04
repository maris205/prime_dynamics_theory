# TPC-390 — Recursive Composition of a Frozen Count Slope

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-390 is a response-blind finite audit of the next count layer after
TPC-389.  It freezes the TPC-389 slope interface, calibrates a fresh
coordinate-disjoint family at `N=1024,1280`, and tests two holdout origins at
`N=1536`.  The audit separates a one-step parent forecast, a same-family
control, and a two-step recursive composition.  The certificate is finite and
does not claim a growing operator bound or an arithmetic improvement.

## Frozen protocol

```text
candidate grid = a_j = 3000001 + 401 j, 0 <= j < 41
selected indices = 0,10,20,30,40 -> origins 3000001,3004011,3008021,3012031,3016041
calibration origins = 3000001,3004011,3008021 at N=1024 and N=1280
holdout origins = 3012031,3016041 at N=1536
block length = 128; modes = fixed_c3, full_relative
Q = 2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar
parent = frozen TPC-389 cell slope; no current-family refit
transfer error cap = 0.03; spectral cap = 0.64; Schur cap = 0.83
```

All origins, roles, bands, laws, normalizations, and the parent hash are fixed
before current-family responses are read.  The panel has 256 rows and 32
cells.  The pooled scalar is computed from calibration-origin geometry only;
it is not a source-valid normalization theorem.

## Forecast definitions

For each cell, `S_N` is the mean band spectral diagnostic over the relevant
origins.  The parent slope is read from the sealed TPC-389 certificate.  The
local slope is fitted only from the current `1024 -> 1280` calibration pair.
The one-step forecasts use the observed `N=1280` mean and extrapolate to
`N=1536`.  The recursive forecast first predicts `N=1280` from `N=1024` and
then applies the same frozen parent slope to `N=1536`.  A direct
`1024 -> 1536` evaluation is retained as an algebraic composition control.

## Current finite findings

The certificate has 256 rows and 32 cells.  The one-step parent forecast passes
`30/32`; the local control passes `32/32`; the two-step recursive parent
forecast passes only `23/32`.  Their maximum absolute ratio errors are
`0.03633754623843255`, `0.025804438647033412`, and
`0.049074165168337847`, respectively.  The sequential/direct composition
identity residual is at most `3.3306690738754696e-16`.

Stability counts at `N=1024`, `N=1280`, and the `N=1536` holdout are
`28/32`, `25/32`, and `26/32`.  There are `64/256` spectral-cap failures and
zero Schur failures.  The recursive cap failures are not scattered noise:
they include fixed-`c3`, pooled `Q=2048` all-plus, alternating-index,
mod-4-character, and half-split cells; their largest value is the
fixed-`c3`, pooled, alternating-index, `Q=2048` cell.  Alternating-index at
`Q=2048` also crosses the recursive cap under local-diagonal and full-relative
normalizations.  One-step parent failures occur in the fixed-`c3`, pooled and
full-relative pooled alternating-index `Q=2048` cells.

The principal decision rule is deliberately fixed: a recursive ratio error
above `0.03` is a finite horizon obstruction, not something repaired by
changing the cap, removing a cell, or choosing a favorable normalization.
The result does not establish that all recursive uses of the interface fail;
it localizes a concrete failure set on this declared panel.

## Claim firewall

```text
TPC390_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC390_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC390_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC390_RECURSIVE_PANEL = NUMERICALLY_CERTIFIED_FINITE_256_ROWS
TPC390_PARENT_ONE_STEP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC390_LOCAL_CONTROL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC390_RECURSIVE_COMPOSITION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC390_COMPOSITION_IDENTITY = PROVED_EXACT_FINITE_NUMERICAL_IDENTITY
TPC390_ORIGIN_UNIFORMITY = OPEN
TPC390_COUNT_UNIFORMITY = OPEN
TPC390_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC390_GROWING_OPERATOR_BOUND = OPEN
TPC390_SOURCE_UNIFORM_L2 = OPEN
TPC390_ARITHMETIC_ADVANCE = NO
TPC390_FIXED_POWER_CREDIT = 0
TPC390_FULL_GATE_B = OPEN
TPC390_TWIN_PRIME_RESULT = NONE
```

The official Session `propose.md`, Route-A evaluator, and Route-B evaluator are
absent from this checkout.  The local Bridge-B checker is fail-closed
repository evidence only; it cannot declare an official Route-A or Route-B
pass.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-390-c1-recursive-slope-composition/code/tpc390_recursive_slope_composition.py --check
python -O -B papers/tpc-390-c1-recursive-slope-composition/code/tpc390_recursive_slope_composition.py --check
python -B papers/tpc-390-c1-recursive-slope-composition/experiments/tpc390_independent_checker.py --check
python -O -B papers/tpc-390-c1-recursive-slope-composition/experiments/tpc390_independent_checker.py --check
python -B papers/tpc-390-c1-recursive-slope-composition/experiments/tpc390_adversarial_certificate_stress.py --check
python -O -B papers/tpc-390-c1-recursive-slope-composition/experiments/tpc390_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc390_c1_recursive_slope_composition_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc390_c1_recursive_slope_composition_checker.py --check
```

`paper/main.pdf` and `paper/paper.pdf` are the byte-identical release PDFs.
