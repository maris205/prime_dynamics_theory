# TPC-400 — C1 endpoint microgrid: third-family replication

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-400 repeats the TPC-399 endpoint-microgrid protocol on a fresh,
coordinate-disjoint affine family. For every one of the four declared
normalizations, the new family agrees with the frozen same-law TPC-399
all-origin means within the three-percent cross-family cap in both calibration
and holdout cohorts (4/4 laws in each cohort), and all within-family
calibration-to-holdout transfers pass (4/4). The finite endpoint `lambda=1`
nevertheless fails the one-percent origin-spread rule in every normalization.
This is a finite third-family replication and obstruction map, not an
arithmetic or asymptotic theorem.

## Research question and contribution

TPC-399 showed that same-law cohort means could transfer across families even
while the endpoint remained origin-unstable. Its response-blind clue was to
test whether this split survives on a third family. TPC-400 answers that
minimal question with a new affine grid, a hash-locked parent interface,
explicit disjointness checks against all earlier endpoint panels, independent
reverse-order replay, and a complete Cartesian panel.

The new contribution is a third-family confirmation of two logically separate
finite statements:

1. same-law cohort means transfer across the parent and current families at
   the declared 3% scale;
2. endpoint origin spread remains above the declared 1% scale on the current
   family.

The four fractional coefficients remain matrix probes. They are not claimed
to be arithmetic sign laws or characters.

## Frozen protocol

```text
schema = TPC400_C1_ENDPOINT_MICROGRID_THIRD_FAMILY_V1
status = NUMERICAL_OBSERVATION_FINITE_C1_ENDPOINT_MICROGRID_THIRD_FAMILY_AUDIT
parent = TPC-399 code and canonical certificate, SHA-256 locked
candidate grid = a_j = 7600001 + 401 j, 0 <= j < 41
selected indices = 0,8,16,24,32,40
origins = 7600001,7603209,7606417,7609625,7612833,7616041
calibration origins = 7600001,7603209,7606417
holdout origins = 7609625,7612833,7616041
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
All roles, candidate indices, laws, and caps are fixed before the current
response is read.

The parent code and certificate are locked as follows:

```text
parent code SHA-256        = 6b65f30fd6aa3f54e58596635a1248c892c01eb71d4156a37578bb71a1079d2b
parent certificate SHA-256 = 6f632add733947838c4268969748068633b2b85fadbd8fba7c21a146d98b7896
parent baseline            = direct same-law TPC-399 all-origin mean
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
spectral failures = 0/96; Schur failures = 0/96 (reproducible float64 observations)
```

The maximum relative origin spreads, in the order local, pooled, origin, and
frozen, are

```text
0.05360449687470719
0.053872109675184521
0.053890672705770762
0.053872109675184458
```

The maximum absolute cross-family calibration errors in that order are
`0.024241880510384561`, `0.027773876023621469`,
`0.027769959109751552`, and `0.027781566566057458`. The corresponding
holdout maxima are `0.0001317871615125199`, `0.0024016862760729563`,
`0.002385057413556213`, and `0.0024091869655593623`. Maximum absolute
within-family transfer errors are `0.023621593273998487`,
`0.024686548607084191`, `0.024699011166062435`, and
`0.024686548607084191`.

The exact rational anchor is `[7600001,7600014)` with `Q=8` and shell
`{11,13}`. Exact `Fraction` arithmetic verifies positive geometry, symmetry,
and all four finite interpolation identities.

## Interpretation and route status

The strongest positive result is a response-blind third-family replication:
the same-law TPC-399 means predict the current family in all 16 cells at both
cohort roles, with the largest calibration discrepancy still below 3%. The
strongest obstruction is equally clear: the endpoint `blend_1` remains
origin-unstable, with a 5.36--5.39% maximum spread, despite close cohort
agreement. Thus cross-family mean transfer does not imply origin uniformity.

The reusable structure is a direct hash-locked same-law interface, exact finite
matrix interpolation, coordinate-disjoint calibration/holdout families with
explicit prior-interval checks, reverse-order replay, and separate origin and
transfer gates. The next response-blind clue is:

```text
ROUND2_CLUE = TEST_C1_ENDPOINT_MICROGRID_FOURTH_FAMILY_REPLICATION
```

The claim firewall is deliberately conservative:

```text
TPC400_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC400_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC400_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED_TPC399
TPC400_INTERPOLATION_IDENTITY = PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY
TPC400_INTERPOLATION_PANEL = NUMERICAL OBSERVATION FINITE FLOAT64_96_ROWS
TPC400_ORIGIN_PHASE = NUMERICAL OBSERVATION FINITE FLOAT64 SCOPED
TPC400_PARENT_CROSS_FAMILY_TRANSFER = NUMERICAL OBSERVATION FINITE FLOAT64 SCOPED
TPC400_SPECTRAL_ENVELOPE = NUMERICAL_OBSERVATION_FINITE_FLOAT64_SCOPED_ONLY
TPC400_SCHUR_ENVELOPE = NUMERICAL_OBSERVATION_FINITE_FLOAT64_SCOPED_ONLY
TPC400_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC400_GROWING_OPERATOR_BOUND = OPEN
TPC400_SOURCE_UNIFORM_L2 = OPEN
TPC400_ARITHMETIC_ADVANCE = NO
TPC400_FIXED_POWER_CREDIT = 0
TPC400_FULL_GATE_B = OPEN
TPC400_TWIN_PRIME_RESULT = NONE
```

The official Session evaluator files are not present in this checkout. The
local proof/checker/Bridge-B chain is fail-closed finite consistency evidence;
it does not constitute an official Route-A or Route-B pass. In particular,
this project proves no source-valid origin-uniform estimate, arithmetic `L2`
bound, growing operator bound, or twin-prime theorem.

## Artifact inventory

This project contains the required `README.md`, `paper/`, `code/`,
`experiments/`, `results/`, and `notes/` directories. The canonical finite
certificate is `results/tpc400_certificate.json`; the release PDF is
`paper/paper.pdf` and is byte-identical to `paper/main.pdf`.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-400-c1-endpoint-microgrid-third-family/code/tpc400_c1_endpoint_microgrid_third_family.py --check
python -O -B papers/tpc-400-c1-endpoint-microgrid-third-family/code/tpc400_c1_endpoint_microgrid_third_family.py --check
python -B papers/tpc-400-c1-endpoint-microgrid-third-family/experiments/tpc400_independent_checker.py --check
python -O -B papers/tpc-400-c1-endpoint-microgrid-third-family/experiments/tpc400_independent_checker.py --check
python -B papers/tpc-400-c1-endpoint-microgrid-third-family/experiments/tpc400_adversarial_certificate_stress.py --check
python -O -B papers/tpc-400-c1-endpoint-microgrid-third-family/experiments/tpc400_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc400_c1_endpoint_microgrid_third_family_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc400_c1_endpoint_microgrid_third_family_checker.py --check
```
