# TPC-398 — endpoint microgrid on a fresh \(c=1\) family

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

On a fresh coordinate-disjoint affine family, finite origin stability persists
at `lambda=7/8`, `15/16`, and `31/32`, but the endpoint `lambda=1` again
fails the one-percent origin-spread rule.  The finer grid therefore locates a
finite crossing between `31/32` and `1` for the origin-stability diagnostic.
Against the frozen TPC-397 segment baseline, the first two interior points and
the endpoint stay within the three-percent cohort cap, while `31/32` misses it
by about 4.5%.  This is a finite proxy result, not an arithmetic or asymptotic
theorem.

## What is new

TPC-397 replicated the coarse endpoint transition on a new family using
`lambda=3/4`, `5/6`, `11/12`, and `1`.  TPC-398 narrows the unresolved segment
`[3/4,1]` with the response-blind microgrid

```text
lambda in {7/8, 15/16, 31/32, 1}.
```

The current matrices are exactly

```text
M_lambda = (1-lambda) M_all_plus + lambda M_alternating_index.
```

For cross-family comparison, TPC-397's `blend_3_4` and `blend_1` all-origin
means are hash-locked before the current readout.  For a current coefficient
`lambda`, the response-blind parent scalar is

```text
t = (lambda - 3/4)/(1/4),
parent(lambda) = (1-t) parent(3/4) + t parent(1).
```

This parent interpolation is a finite modeling baseline.  Fractional probes
are not asserted to be arithmetic sign laws.

## Frozen protocol

```text
schema = TPC398_C1_INTERPOLATION_ENDPOINT_MICROGRID_V1
parent = TPC-397 finite interpolation certificate (code and JSON hash locked)
candidate grid = a_j = 6800001 + 401 j, 0 <= j < 41
selected indices = 0,8,16,24,32,40
origins = 6800001,6803209,6806417,6809625,6812833,6816041
calibration origins = 6800001,6803209,6806417
holdout origins = 6809625,6812833,6816041
window count = N=1024 at every origin
block length = 128; band mode = fixed_c3; Q = 8192
kernel exponent = 1; beta = 2; height = 66
laws = blend_7_8, blend_15_16, blend_31_32, blend_1
lambda coefficients = 7/8, 15/16, 31/32, 1/1
normalizations = local_diagonal, pooled_train_scalar,
                 origin_scalar, frozen_train_1024_scalar
origin-spread cap = 0.01
parent calibration/holdout caps = 0.03
within-family transfer cap = 0.03
spectral cap = 0.64; Schur cap = 0.83
```

The certificate is the complete 6-origin × 4-law × 4-normalization panel:
96 rows and 16 cells.  Origin roles, coefficients, caps, and the holdout
partition are fixed before reading the current response.

## Finite findings

```text
origin-stable cells by normalization:
  local_diagonal             3/4
  pooled_train_scalar        3/4
  origin_scalar              3/4
  frozen_train_1024_scalar   3/4
total origin-stable cells = 12/16
law-level origin result = blend_7_8, blend_15_16, blend_31_32 pass all 4;
                          blend_1 passes 0/4
parent calibration passes = 3/4 for every normalization
parent holdout passes = 3/4 for every normalization
within-family transfer passes = 4/4 for every normalization
spectral failures = 0/96; Schur failures = 0/96
```

Maximum relative origin spreads, in the order local, pooled, origin, frozen,
are respectively

```text
0.073402226295029099
0.075578056988127071
0.075600654173434007
0.075578056988126863
```

The maxima occur at `lambda=1`.  The maximum absolute parent-relative
calibration errors are approximately `0.04463`, `0.04462`, `0.04463`, and
`0.04462`; the corresponding holdout maxima are approximately `0.04497`,
`0.04497`, `0.04496`, and `0.04497`.  These failures are concentrated at
`lambda=31/32`; the endpoint itself is close to the parent endpoint on the
three-percent cohort test but fails origin stability.  Maximum within-family
transfer errors are approximately `0.02385`, `0.02565`, `0.02567`, and
`0.02565`, all below the declared cap.

At the exact rational anchor `[6800001,6800014)` with `Q=8` and shell
`{11,13}`, geometry is positive, all endpoint matrices are symmetric, and all
four interpolation identities hold over exact fractions.

## Interpretation, obstruction, and next clue

The strongest positive result is a finer finite localization: the new family
retains the origin-stable behavior through `31/32` under all four
normalizations.  The strongest obstruction is that the same `31/32` point is
already about 4.5% below the frozen TPC-397 segment baseline, while `lambda=1`
loses origin stability with a 7.3–7.6% spread.  Thus the two diagnostics do
not identify a single universal transition point on this finite panel.

The reusable structure is a hash-locked two-endpoint interface, exact finite
matrix interpolation, a predeclared calibration/holdout family, independent
reverse-order replay, and separate origin and parent-relative gates.  The
next clue is

```text
ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_REPLICATION
```

The natural continuation is a second fresh-family replication of this finer
grid, with the same endpoint interface and no threshold promotion.  If the
cross-family discrepancy at `31/32` persists, it becomes a scoped obstruction
to treating the parent interpolation as a transferable law; if it moves, the
current crossing remains family-dependent.

## Certification and claim firewall

The producer accumulates the prime shell in ascending order.  The independent
checker rebuilds it in descending order without importing producer functions.
It recomputes all 96 rows, segment-interpolated parent errors, cohort
statistics, and counters.  A 28-case mutation suite rejects altered
certificate contracts.  Normal and optimized executions are required to agree
at their output interfaces; Bridge-B locks the release artifacts.

```text
TPC398_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC398_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC398_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC398_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY
TPC398_INTERPOLATION_PANEL = NUMERICALLY_CERTIFIED_FINITE_96_ROWS
TPC398_ORIGIN_PHASE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC398_PARENT_INTERPOLATED_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC398_SPECTRAL_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
TPC398_SCHUR_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
TPC398_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC398_GROWING_OPERATOR_BOUND = OPEN
TPC398_SOURCE_UNIFORM_L2 = OPEN
TPC398_ARITHMETIC_ADVANCE = NO
TPC398_FIXED_POWER_CREDIT = 0
TPC398_FULL_GATE_B = OPEN
TPC398_TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are absent from this checkout.  The local
proof/checker/Bridge-B chain is fail-closed finite consistency evidence;
Route-A is not officially evaluated and Route-B remains open.  Nothing here
proves source-valid origin uniformity, an arithmetic `L2` estimate, a growing
operator bound, or a twin-prime result.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-398-c1-interpolation-endpoint-microgrid/code/tpc398_c1_interpolation_endpoint_microgrid.py --check
python -O -B papers/tpc-398-c1-interpolation-endpoint-microgrid/code/tpc398_c1_interpolation_endpoint_microgrid.py --check
python -B papers/tpc-398-c1-interpolation-endpoint-microgrid/experiments/tpc398_independent_checker.py --check
python -O -B papers/tpc-398-c1-interpolation-endpoint-microgrid/experiments/tpc398_independent_checker.py --check
python -B papers/tpc-398-c1-interpolation-endpoint-microgrid/experiments/tpc398_adversarial_certificate_stress.py --check
python -O -B papers/tpc-398-c1-interpolation-endpoint-microgrid/experiments/tpc398_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc398_c1_interpolation_endpoint_microgrid_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc398_c1_interpolation_endpoint_microgrid_checker.py --check
```

The required release PDF is `paper/paper.pdf`, byte-identical to
`paper/main.pdf`.
