# TPC-233: Critical-Depth Row-Mass Comparability Obstruction

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_ARITHMETIC_OBSTRUCTION_L1 / RAW_ROW_COMPARABILITY_REFUTED_SCOPED`

TPC-232 的 saving transfer 假设 row masses 具有固定可比常数。本篇证明这个常数
并不由 dilated-clock geometry 自动保证，甚至在临界深度也会无界增长。

令

```text
P_L = product_(prime ell<=L) ell,
Q_L = 2^j P_L,
log Q_L = L log L + O(1),
h_L = 4LQ_L.
```

经典带误差项素数定理保证 shell `(Q_L,2Q_L)` 内存在 cutoff 分别为 `L` 与
`2L-1` 的两条 prime rows。若 `N_q` 是 uniform-atom row 的原子数，则

```text
N_low = 2,
N_high = 2(1 + pi(2L-1)-pi(L)),
kappa_raw >= 1 + pi(2L-1)-pi(L) ~ L/log L -> infinity.
```

同时所有 clocks 都有 universal bound `1<=kappa_raw<=2L-1`。因此
`fixed row-mass comparability` 是额外建模/源假设，不能从 TPC-226/232 support
定义推出。该结论不否定 row normalization，也不涉及 actual V59 weights。

## Claim firewall

```text
TPC233_ROUTE_ADVANCE = YES
TPC233_CRITICAL_PRIMORIAL_CLOCK = PROVED_EXACT
TPC233_CRITICAL_SCALE_RELATION = PROVED_ASYMPTOTIC
TPC233_LOW_HIGH_PRIME_ROWS = PROVED_SOURCE_BACKED
TPC233_LOW_ROW_ATOMS = PROVED_EXACT_2
TPC233_HIGH_ROW_ATOMS = PROVED_EXACT_PRIME_INTERVAL_COUNT
TPC233_RAW_COMPARABILITY_DIVERGES = PROVED_ASYMPTOTIC
TPC233_UNIVERSAL_KAPPA_UPPER_BOUND = PROVED_EXACT_2L_MINUS_1
TPC233_FIXED_COMPARABILITY_FROM_GEOMETRY = REFUTED_SCOPED
TPC233_ROW_NORMALIZATION_REPAIR = OPEN
TPC233_ACTUAL_V59_ROW_WEIGHTS = OPEN
TPC233_ARITHMETIC_ADVANCE = NO
TPC233_ARITHMETIC_OBSTRUCTION = PROVED_SOURCE_BACKED
TPC233_FIXED_ATOM_CREDIT = 0
TPC233_L2 = NONE
TPC233_FULL_GATE_B = OPEN
TPC233_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC233_STATUS = PROVED_ARITHMETIC_OBSTRUCTION_L1
TPC233_ROUND2_CLUE = NORMALIZE_ROWS_THEN_TEST_COLLISION_OPERATOR_BEFORE_V59_ATTACHMENT
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/mass_adversary.py
```

Bridge proof/checker：

```text
research/tpc-big-road/bridge_b_critical_depth_row_mass_obstruction.md
research/tpc-big-road/tpc_bridge_b_critical_depth_row_mass_obstruction_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/critical_row_mass.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/mass_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
