# TPC-399 — C1 endpoint microgrid: cross-family replication

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-399 repeats the TPC-398 endpoint microgrid on a fresh, coordinate-disjoint
affine family. For every one of the four declared normalizations, the new
family agrees with the frozen same-law TPC-398 all-origin means within the
three-percent cross-family cap in both calibration and holdout cohorts (4/4
laws in each cohort), and all within-family calibration-to-holdout transfers
pass (4/4). The finite endpoint `lambda=1` nevertheless fails the one-percent
origin-spread rule in every normalization. This is a cross-family finite
replication and obstruction map, not an arithmetic or asymptotic theorem.

## Research question and contribution

TPC-398 found a stable finite microgrid through `lambda=31/32` and an
origin-instability signal at `lambda=1` on one family. Its response-blind clue
was to test whether that split survives on a second family. TPC-399 answers
that minimal question with a fresh affine family, a hash-locked parent
interface, independent reverse-order replay, and a complete Cartesian panel.

The new contribution is the separation of two finite statements:

1. same-law cohort means transfer across the two selected families at the
   declared 3% scale;
2. endpoint origin spread remains above the declared 1% scale on the new
   family.

The four fractional coefficients remain matrix probes. They are not claimed
to be arithmetic sign laws or characters.

## Frozen protocol

```text
schema = TPC399_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_V1
status = NUMERICALLY_CERTIFIED_FINITE_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_AUDIT
parent = TPC-398 code and canonical certificate, SHA-256 locked
candidate grid = a_j = 7200001 + 401 j, 0 <= j < 41
selected indices = 0,8,16,24,32,40
origins = 7200001,7203209,7206417,7209625,7212833,7216041
calibration origins = 7200001,7203209,7206417
holdout origins = 7209625,7212833,7216041
window count = N=1024 at every origin
block length = 128; band mode = fixed_c3; Q = 8192
kernel exponent = 1; beta = 2; height = 66
laws = blend_7_8, blend_15_16, blend_31_32, blend_1
normalizations = local_diagonal, pooled_train_scalar,
                 origin_scalar, frozen_train_1024_scalar
origin-spread cap = 0.01
cross-family calibration/holdout cap = 0.03
within-family transfer cap = 0.03
spectral cap = 0.64; Schur cap = 0.83
```

The panel has 6 origins × 4 laws × 4 normalizations = 96 rows and 16 cells.
All roles, candidate indices, laws, coefficients, and caps are fixed before
the current response is read.

The parent code and certificate are locked as follows:

```text
parent code SHA-256        = 10c55a6b9e3c4dc11674780f7d1d98508d223729e18ffde7f27a88d7790a3382
parent certificate SHA-256 = 3f944db8218d8c18a2f2c756dcaf26483afe18e4ac681695beba56b222256150
parent baseline            = direct same-law TPC-398 all-origin mean
```

No current response is used to select origins, laws, normalizations, or the
parent baseline.

## Finite findings

```text
within-family origin-stable cells by normalization:
  local_diagonal             3/4
  pooled_train_scalar        3/4
  origin_scalar              3/4
  frozen_train_1024_scalar   3/4
total origin-stable cells = 12/16
law-level origin result = blend_7_8, blend_15_16, blend_31_32 pass all 4;
                          blend_1 passes 0/4
cross-family calibration passes = 4/4 for every normalization
cross-family holdout passes      = 4/4 for every normalization
within-family transfer passes    = 4/4 for every normalization
spectral failures = 0/96; Schur failures = 0/96
```

The maximum relative origin spreads, in the order local, pooled, origin, and
frozen, are

```text
0.062219451593902582
0.062549688932650407
0.062544618763190271
0.062549688932650421
```

The maximum absolute cross-family calibration errors in that order are
`0.010915543232415503`, `0.010520642314234108`,
`0.010513181511174086`, and `0.010529967847841215`. The corresponding
holdout maxima are `0.0027174217101944009`, `0.002162884458446479`,
`0.0021636109447358276`, and `0.002172132862949594`. Maximum absolute
within-family transfer errors are `0.0081096008238309425`,
`0.0082707443131960767`, `0.0082627032672170087`, and
`0.0082707443131960767`.

The exact rational anchor is `[7200001,7200014)` with `Q=8` and shell
`{11,13}`. Exact `Fraction` arithmetic verifies positive geometry, symmetry,
and all four finite interpolation identities.

## Interpretation and route status

The strongest positive result is a response-blind cross-family replication:
the same-law TPC-398 means predict the second family at substantially tighter
than the declared 3% scale, including all four laws and both cohort roles.
The strongest obstruction is equally clear: the endpoint `blend_1` remains
origin-unstable, with a 6.22–6.25% maximum spread, despite its close parent
cohort agreement. Thus cross-family mean transfer does not imply origin
uniformity.

The reusable structure is a direct hash-locked same-law interface, exact finite
matrix interpolation, coordinate-disjoint calibration/holdout families,
reverse-order replay, and separate origin and transfer gates. The next
response-blind clue is:

```text
ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_THIRD_FAMILY_REPLICATION
```

The next study should test a third fresh family before any threshold or
asymptotic interpretation is entertained.

The claim firewall is deliberately conservative:

```text
TPC399_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC399_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC399_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED_TPC398
TPC399_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY
TPC399_INTERPOLATION_PANEL = NUMERICALLY_CERTIFIED_FINITE_96_ROWS
TPC399_ORIGIN_PHASE = NUMERICALLY CERTIFIED FINITE SCOPED
TPC399_PARENT_CROSS_FAMILY_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED
TPC399_SPECTRAL_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
TPC399_SCHUR_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
TPC399_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC399_GROWING_OPERATOR_BOUND = OPEN
TPC399_SOURCE_UNIFORM_L2 = OPEN
TPC399_ARITHMETIC_ADVANCE = NO
TPC399_FIXED_POWER_CREDIT = 0
TPC399_FULL_GATE_B = OPEN
TPC399_TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are not present in this checkout. The
local proof/checker/Bridge-B chain is fail-closed finite consistency evidence;
it does not constitute an official Route-A or Route-B pass. In particular,
this project proves no source-valid origin-uniform estimate, arithmetic `L2`
bound, growing operator bound, or twin-prime theorem.

## Artifact inventory

This project contains the required `README.md`, `paper/`, `code/`,
`experiments/`, `results/`, and `notes/` directories. The canonical finite
certificate is `results/tpc399_certificate.json`; the release PDF is
`paper/paper.pdf` and is byte-identical to `paper/main.pdf`.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-399-c1-endpoint-microgrid-cross-family/code/tpc399_c1_endpoint_microgrid_cross_family.py --check
python -O -B papers/tpc-399-c1-endpoint-microgrid-cross-family/code/tpc399_c1_endpoint_microgrid_cross_family.py --check
python -B papers/tpc-399-c1-endpoint-microgrid-cross-family/experiments/tpc399_independent_checker.py --check
python -O -B papers/tpc-399-c1-endpoint-microgrid-cross-family/experiments/tpc399_independent_checker.py --check
python -B papers/tpc-399-c1-endpoint-microgrid-cross-family/experiments/tpc399_adversarial_certificate_stress.py --check
python -O -B papers/tpc-399-c1-endpoint-microgrid-cross-family/experiments/tpc399_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc399_c1_endpoint_microgrid_cross_family_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc399_c1_endpoint_microgrid_cross_family_checker.py --check
```
