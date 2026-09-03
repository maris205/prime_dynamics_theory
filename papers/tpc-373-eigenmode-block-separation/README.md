# TPC-373 — Extremal-eigenmode block separation

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-373 decomposes the selected extremal eigenmode of every TPC-372
count-2048 matrix into eight fixed block-distance Rayleigh layers.  All 18
rows select the minimum-eigenvalue mode and have block distance zero as the
largest individual layer.  On the six beta=2 high-`Q` failure rows, all eight
Rayleigh terms have the same negative sign: about 65.585% of the absolute
mass lies at distance zero, 28.175% at distance one, and at least 99.157% at
distances zero through three.  This is a finite near-block signed-coherence
profile, not a causal or asymptotic theorem.

## Frozen protocol

```text
origins       = (1010001, 1018021, 1026041)
window count  = 2048
block mask    = eight contiguous blocks of length 256
Q             = (512, 2048, 8192)
exponent      = 1
law           = all_plus
beta          = (0, 2)
rows          = 3 * 3 * 2 = 18
layers        = absolute block-index distance 0,...,7
```

All rows are fixed before any eigenmode is read.  For each symmetric matrix,
the eigenvector associated with the largest absolute eigenvalue is selected;
an exact tie is resolved in favor of the minimum eigenvalue.  This rule is
also fixed before any layer contribution is inspected.  The inherited exact
anchor is `[1010346,1010359)` at `Q=4`, exponent one, shell `{5,7}`; it is
not used to select a panel row.

## Finite census

| beta | rows | minimum mode | distance-0 dominant | full spectral failures | full Schur failures |
|---:|---:|---:|---:|---:|---:|
| 0 | 9 | 9 | 9 | 9 | 9 |
| 2 | 9 | 9 | 9 | 6 | 0 |

For beta=2, the cross-block share of absolute Rayleigh mass ranges from
`0.32041765385537019` to `0.34415392242278348`; the share at block distances
four through seven is at most `0.0084288235550895561`.  The six parent
failure rows are exactly the three origins at `Q=2048,8192`.  On those six
rows every layer term is negative and the approximate absolute-mass ranges
are:

| layer group | range over six failure rows |
|---|---:|
| distance 0 | 65.5846%--65.5853% |
| distance 1 | 28.1747%--28.1753% |
| distance 2 | 4.05997%--4.06004% |
| distance 3 | 1.33717%--1.33723% |
| distances 4--7 | 0.84264%--0.84288% |

The layer reconstruction error is zero in the stored double-precision
arrays, the maximum Rayleigh-sum error is
`2.6645352591003757e-15`, and the maximum infinity-norm eigen-residual is
`8.0838113980519211e-16`.

## Mathematical object

Let `b(i)` be the fixed 256-point block index and let `T` be the normalized
full-window matrix.  Define

```text
L_d(i,j) = 1_{|b(i)-b(j)|=d} T(i,j),    d=0,...,7.
```

Then `T=sum_d L_d` entrywise.  For the selected unit eigenvector `v` with
eigenvalue `lambda`, the recorded terms `c_d=v^T L_d v` satisfy
`sum_d c_d=lambda`.  Signed fractions use `c_d/lambda`; absolute fractions
use `|c_d|/sum_e |c_e|`.

## Claim firewall

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

The finite signed-coherence profile does not prove that near-block entries
cause the parent failure and does not establish a decay estimate, a banded
operator theorem, or transfer to other windows.  Official Route-A/Route-B
evaluator files are absent; local Bridge-B is repository evidence only.

## Auditable package and reproduction

The project contains `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`,
`PROOF_PACKAGE.md`, `notes/`, `code/`, `experiments/`, `results/`, and
`paper/`.  The canonical result is `results/tpc373_certificate.json`, and the
manuscript is `paper/paper.pdf`.

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-373-eigenmode-block-separation/code/tpc373_eigenmode_block_separation.py --write
python -B papers/tpc-373-eigenmode-block-separation/code/tpc373_eigenmode_block_separation.py --check
python -O -B papers/tpc-373-eigenmode-block-separation/code/tpc373_eigenmode_block_separation.py --check
python -B papers/tpc-373-eigenmode-block-separation/experiments/tpc373_independent_checker.py --check
python -O -B papers/tpc-373-eigenmode-block-separation/experiments/tpc373_independent_checker.py --check
python -B papers/tpc-373-eigenmode-block-separation/experiments/tpc373_adversarial_certificate_stress.py --check
python -O -B papers/tpc-373-eigenmode-block-separation/experiments/tpc373_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc373_eigenmode_block_separation_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc373_eigenmode_block_separation_checker.py --check
```

```text
ROUND2_CLUE = TEST_LAYERWISE_CROSS_BLOCK_DECAY
```
