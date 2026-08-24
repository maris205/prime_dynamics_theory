# TPC-232: Subcritical Growing Resonance Depth on Prime Shells

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_ARITHMETIC_OBSTRUCTION_L1 / SUBCRITICAL_GROWING_DEPTH_STOP_SCOPED`

TPC-231 封闭了 fixed finite resonance families。本篇允许 TPC-226 dilated
shared-clock depth \(L=L(Q)\) 增长，并证明 uniform upper bound

```text
C_L(Q) <<_A L Q loglog(3LQ)/(log Q)^2,
C_L(Q)/P(Q) <<_A L loglog(3LQ)/log Q
```

for `L <= (log Q)^A`.  因而

```text
L=o(log Q/loglog Q)  =>  C_L(Q)/P(Q)->0.
```

在 fixed-comparability row model 中，incident mass 也趋于零，所以任何 fixed
positive saving（包括 `1/400`）仍然不可能。这个结论给出第一个严格的 growing-depth
必要门槛；它没有证明 critical depth 有足够多 resonance。

代数上，`h=4LQ` 在 `L<Q/4` 时仍保持 row invertibility、internal injectivity、
opposite-sign one-wrap normal form 和每个 channel 两个 sign residues。但这个 dilated
clock 仍是 `MODELING_CHOICE`，actual V59 source attachment 保持 `OPEN`。

## Claim firewall

```text
TPC232_ROUTE_ADVANCE = YES
TPC232_GROWING_COLLISION_NORMAL_FORM = PROVED_EXACT
TPC232_UNIFORM_POLYLOG_DEPTH_SIEVE = PROVED_SOURCE_BACKED
TPC232_COLLISION_INCIDENCE_BOUND = PROVED_ASYMPTOTIC
TPC232_SUBCRITICAL_DEPTH_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC232_SUBCRITICAL_FIXED_SAVING = STOP_SCOPED
TPC232_CRITICAL_DEPTH_SUFFICIENCY = OPEN
TPC232_DILATED_CLOCK = MODELING_CHOICE
TPC232_ACTUAL_V59_CLOCK_ATTACHMENT = OPEN
TPC232_ARITHMETIC_ADVANCE = NO
TPC232_ARITHMETIC_OBSTRUCTION = PROVED_SOURCE_BACKED
TPC232_FIXED_ATOM_CREDIT = 0
TPC232_L2 = NONE
TPC232_FULL_GATE_B = OPEN
TPC232_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC232_STATUS = PROVED_ARITHMETIC_OBSTRUCTION_L1
TPC232_ROUND2_CLUE = TEST_CRITICAL_DEPTH_CLOCK_MASS_AND_DEGREE_BEFORE_V59_ATTACHMENT
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/depth_adversary.py
```

Bridge proof/checker：

```text
research/tpc-big-road/bridge_b_subcritical_growing_resonance_depth.md
research/tpc-big-road/tpc_bridge_b_subcritical_growing_resonance_depth_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/growing_resonance_depth.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/depth_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
