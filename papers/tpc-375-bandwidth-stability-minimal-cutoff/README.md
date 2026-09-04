# TPC-375 — Bandwidth stability and the minimal finite cutoff

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-375 compares nested bands `B_c` with block-distance cutoffs
`c=0,1,2,3` under the inherited count-2048 full-window normalization.  On
the complete beta=2 panel of three origins and three `Q` anchors (9 rows),
cutoff `c=0` has no spectral-cap failure, while each of `c=1,2,3` has exactly
the six inherited high-`Q`/all-plus failure keys.  Thus the first matching
cutoff in the declared finite list is `c=1`.

This is a finite minimal-cutoff certificate, not a global bandwidth optimum,
uniform theorem, causal explanation, or twin-prime result.

## Frozen protocol

```text
origins       = (1010001, 1018021, 1026041)
window count  = 2048
blocks        = eight contiguous blocks of length 256
cutoffs       = (0, 1, 2, 3)
Q             = (512, 2048, 8192)
exponent      = 1
law           = all_plus
beta          = 2
rows          = 9 (complete origin-by-Q panel)
caps          = spectral 0.64, Schur 0.83
```

For every cutoff, `B_c` retains entries with block distance at most `c` and
uses the same full-window square-energy geometry as `T`; the complement is
`R_c=T-B_c`.  The full eigensystem and its deterministic largest-absolute
mode rule are fixed before cutoff results are read.  No row or cutoff is
selected adaptively.

## Finite census

| cutoff `c` | spectral failures | Schur failures | first-hit interpretation |
|---:|---:|---:|---|
| 0 | 0/9 | 0/9 | no parent failure |
| 1 | 6/9 | 0/9 | first complete parent-support match |
| 2 | 6/9 | 0/9 | same support |
| 3 | 6/9 | 0/9 | inherited TPC-374 band |

The six failures at `c=1` are all three origins at `Q=2048` and `Q=8192`.
The three `Q=512` rows never cross the spectral cap in the declared cutoff
list.  Selected full-mode absolute-Rayleigh retention over all nine rows is
`0.65584607757721647--0.69054412955975686` for `c=0`,
`0.93759913028905661--0.9769476322189844` for `c=1`,
`0.97819886633128827--1.0059123454463856` for `c=2`, and
`0.99157117644491055--1.0016823596918929` for `c=3`.

## Claim firewall

```text
TPC375_FULL_WINDOW_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND
TPC375_COMMON_NORMALIZATION = PROVED_EXACT_FINITE
TPC375_NESTED_BAND_MASKS = PROVED_EXACT_FINITE_PREDECLARED
TPC375_BANDWIDTH_REPLAY = NUMERICALLY_CERTIFIED_FINITE_9_ROWS
TPC375_FAILURE_CUTOFF_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC375_PARENT_SUPPORT_REPRODUCTION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC375_RAYLEIGH_RETENTION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC375_MINIMAL_CUTOFF = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC375_BANDWIDTH_UNIFORMITY = OPEN
TPC375_CROSS_BLOCK_CAUSALITY = OPEN
TPC375_ORIGIN_UNIFORMITY = OPEN
TPC375_WINDOW_UNIFORMITY = OPEN
TPC375_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC375_GROWING_OPERATOR_BOUND = OPEN
TPC375_SOURCE_UNIFORM_L2 = OPEN
TPC375_ARITHMETIC_ADVANCE = NO
TPC375_FIXED_POWER_CREDIT = 0
TPC375_FULL_GATE_B = OPEN
TPC375_TWIN_PRIME_RESULT = NONE
```

Official Route-A/Route-B evaluator files named by the Session are absent.
The local Bridge-B checker is fail-closed repository evidence only.

## Package and reproduction

The project contains `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`,
`PROOF_PACKAGE.md`, `notes/`, `code/`, `experiments/`, `results/`, and
`paper/`.  The canonical certificate is
`results/tpc375_certificate.json`; the manuscript is `paper/paper.pdf`.

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-375-bandwidth-stability-minimal-cutoff/code/tpc375_bandwidth_stability_minimal_cutoff.py --write
python -B papers/tpc-375-bandwidth-stability-minimal-cutoff/code/tpc375_bandwidth_stability_minimal_cutoff.py --check
python -O -B papers/tpc-375-bandwidth-stability-minimal-cutoff/code/tpc375_bandwidth_stability_minimal_cutoff.py --check
python -B papers/tpc-375-bandwidth-stability-minimal-cutoff/experiments/tpc375_independent_checker.py --check
python -O -B papers/tpc-375-bandwidth-stability-minimal-cutoff/experiments/tpc375_independent_checker.py --check
python -B papers/tpc-375-bandwidth-stability-minimal-cutoff/experiments/tpc375_adversarial_certificate_stress.py --check
python -O -B papers/tpc-375-bandwidth-stability-minimal-cutoff/experiments/tpc375_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc375_bandwidth_stability_minimal_cutoff_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc375_bandwidth_stability_minimal_cutoff_checker.py --check
```

```text
ROUND2_CLUE = TEST_BANDWIDTH_HOLDOUT
```
