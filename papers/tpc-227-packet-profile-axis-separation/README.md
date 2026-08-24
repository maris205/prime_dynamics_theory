# TPC-227: Packet/Profile Axis Separation for Source-Native Four-Phase Polarization

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / PACKET_PROFILE_AXIS_SEPARATION`

TPC-226 在有限 `3--7` collision graph 上发现：row-dependent odd profile 可以把
AP cross term 从正号翻成负号。但 V59 的 literal four-packet identity 并不是四个
独立 profile：四相位属于源序列

```text
a^(j) = beta + i^j w,
```

而所有 packet 共用同一个 Poisson profile `psi_+(v)`。本篇把这两个坐标轴严格
分开，并证明 exact operator criterion：若 `T` 是真实共同变换，而第 `j` 个 packet
误用 `T_j`，则

```text
1/4 sum_(j=0)^3 i^j ||T_j(x+i^j y)||^2 = <Tx,Ty>  for every x,y
```

当且仅当

```text
T_j^* T_j = T^* T,  j=0,1,2,3.
```

因此 boundedness、共同 support、甚至四个 packet 彼此拥有相同 Gram 都不够；它们
必须等于 physical target Gram。global packet signs 是 Gram-invisible，但
row-dependent sign 在 TPC-226 的 `Q=25`, `(37,47)` resonance block 上把 off-diagonal
Gram entry 从 `+1/160000` 变成 `-1/160000`，exact mismatch 为 `-1/80000`。

## Claim firewall

```text
TPC227_ROUTE_ADVANCE = YES
TPC227_V59_PACKET_AXIS = SOURCE_LOCKED
TPC227_V59_PROFILE_AXIS = SOURCE_LOCKED_COMMON
TPC227_FOUR_GRAM_CRITERION = PROVED_EXACT
TPC227_GLOBAL_PACKET_PHASE_VISIBILITY = GRAM_INVISIBLE
TPC227_Q25_ROW_SIGN_GRAM_MISMATCH = PROVED_EXACT
TPC227_TPC226_AUTOMATIC_SOURCE_TRANSFER = REFUTED_SCOPED
TPC227_SOURCE_NATIVE_COMMON_PROFILE_COMPILER = OPEN
TPC227_ARITHMETIC_CANCELLATION = NONE
TPC227_ARITHMETIC_ADVANCE = NO
TPC227_FIXED_ATOM_CREDIT = 0
TPC227_L2 = NONE
TPC227_FULL_GATE_B = OPEN
TPC227_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC227_STATUS = PROVED_STRUCTURAL_L1
TPC227_ROUND2_CLUE = KEEP_THE_V59_PACKET_PHASE_ON_THE_SOURCE_SEQUENCE_AND_THE_POISSON_PROFILE_COMMON
```

这里的 scoped refutation 只否定“把 TPC-226 profile sign 自动解释为 V59 packet
sign”这一推理；它不否定 TPC-226 的有限 exact AP saving，也不否定真实源未来可能
产生负 correlation。

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/axis_mutation_adversary.py
```

Bridge proof/checker：

```text
research/tpc-big-road/bridge_b_packet_profile_axis_separation.md
research/tpc-big-road/tpc_bridge_b_packet_profile_axis_separation_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/axis_separation.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/axis_mutation_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
