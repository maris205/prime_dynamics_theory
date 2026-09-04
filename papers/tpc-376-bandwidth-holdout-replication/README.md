# TPC-376 — Response-blind holdout replication of the finite \(c=1\) band

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-376 takes the three origins that were reserved, but not used, in the
TPC-370 candidate grid: indices \(j=(5,15,30)\) in
\(a_j=1010001+401j\).  With the TPC-375 rule \(c=1\), count \(2048\), and
the complete \(Q=(512,2048,8192)\) beta-2/all-plus panel, the holdout has
the same spectral failure profile \((0,3,3)\) by \(Q\) as TPC-375:
six failures, all at \(Q=2048,8192\).  Its Schur failure count is zero.

This is a finite grid-index holdout replication.  The two lower-index
holdout windows overlap their neighboring training windows by a few
coordinates, so the paper makes no interval-disjointness claim.  It is not
an origin-uniform theorem, a growing-window result, an arithmetic estimate,
or a twin-prime proof.

## Frozen protocol

~~~text
candidate grid       a_j = 1010001 + 401*j, 0 <= j < 41
training indices     (0, 20, 40)
holdout indices      (5, 15, 30)
holdout origins      (1012006, 1016016, 1022031)
window count         2048
blocks               eight contiguous blocks of length 256
band cutoff          c = 1
Q                    (512, 2048, 8192)
kernel exponent      1
beta                 2
law                  all_plus
height               66
caps                 spectral 0.64, Schur 0.83
~~~

The grid indices and the complete panel were fixed before any signed
response was read.  The full-window square-energy geometry is used for both
the full matrix \(T\) and the band \(B_1\); the tail is \(T-B_1\).  The
selected full mode is the largest-absolute-eigenvalue mode, with the
minimum mode winning ties.

## Finite census

| \(Q\) | rows | band spectral failures | band Schur failures |
|---:|---:|---:|---:|
| 512 | 3 | 0 | 0 |
| 2048 | 3 | 3 | 0 |
| 8192 | 3 | 3 | 0 |
| **total** | **9** | **6** | **0** |

The c=1 band spectral values are
0.50281930544856424--0.50283444162621627 at \(Q=512\),
0.66562825618491772--0.66563867656808429 at \(Q=2048\), and
0.66694245634594918--0.66694502781223552 at \(Q=8192\).
The selected full-mode absolute-Rayleigh retention over all rows is
0.93760019185559207--0.976941204869197, with maximum tail fraction
0.062399808144408715.

## Claim firewall

~~~text
TPC376_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC376_COMMON_NORMALIZATION = PROVED_EXACT_FINITE_INHERITED
TPC376_HOLDOUT_REPLAY = NUMERICALLY_CERTIFIED_FINITE_9_ROWS
TPC376_C1_FAILURE_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC376_PARENT_Q_PROFILE_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC376_RAYLEIGH_TAIL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC376_ORIGIN_UNIFORMITY = OPEN
TPC376_WINDOW_UNIFORMITY = OPEN
TPC376_C1_SCALE_STABILITY = OPEN
TPC376_CROSS_BLOCK_CAUSALITY = OPEN
TPC376_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC376_GROWING_OPERATOR_BOUND = OPEN
TPC376_SOURCE_UNIFORM_L2 = OPEN
TPC376_ARITHMETIC_ADVANCE = NO
TPC376_FIXED_POWER_CREDIT = 0
TPC376_FULL_GATE_B = OPEN
TPC376_TWIN_PRIME_RESULT = NONE
~~~

The official Session-named Route-A/Route-B evaluator files are absent.
The local Bridge-B is therefore fail-closed repository evidence only.

## Package and reproduction

The project contains PAPER_PLAN.md, DERIVATION_PACKAGE.md,
PROOF_PACKAGE.md, notes/, code/, experiments/, results/, and paper/.
The canonical certificate is
results/tpc376_certificate.json; the manuscript is paper/paper.pdf.

~~~bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-376-bandwidth-holdout-replication/code/tpc376_bandwidth_holdout_replication.py --write
python -B papers/tpc-376-bandwidth-holdout-replication/code/tpc376_bandwidth_holdout_replication.py --check
python -O -B papers/tpc-376-bandwidth-holdout-replication/code/tpc376_bandwidth_holdout_replication.py --check
python -B papers/tpc-376-bandwidth-holdout-replication/experiments/tpc376_independent_checker.py --check
python -O -B papers/tpc-376-bandwidth-holdout-replication/experiments/tpc376_independent_checker.py --check
python -B papers/tpc-376-bandwidth-holdout-replication/experiments/tpc376_adversarial_certificate_stress.py --check
python -O -B papers/tpc-376-bandwidth-holdout-replication/experiments/tpc376_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc376_bandwidth_holdout_replication_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc376_bandwidth_holdout_replication_checker.py --check
~~~

ROUND2_CLUE = TEST_C1_WINDOW_SCALE_HOLDOUT.
