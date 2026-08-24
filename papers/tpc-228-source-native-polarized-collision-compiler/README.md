# TPC-228: Source-Native Polarized Collision Compiler

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / SOURCE_NATIVE_POLARIZED_COLLISION_COMPILER`

TPC-227 证明 packet phase 必须留在 source sequence。本篇据此冻结共同 profile
operators，并对每个 prime row 写

```text
W_q^(j) = U_q + i^j V_q,
```

其中 `U_q` 与 `V_q` 分别是 `beta` 与 `w` 经过同一个 row transform 的输出。exact
four-phase compiler 给出

```text
1/4 sum_j i^j (E_AP^(j)-E_diag^(j))
  = sum_(q!=r) <U_q,V_r>.
```

这把 packet-energy signed combination 精确变成 source-labelled collision sum，并且
在做极化前删除同 prime diagonal。对 TPC-226 Q25 first `3--7` resonance，右端就是两个
shared residues 上的 `beta_p w_r + beta_r w_p`。exact fixtures 给出正、负、零、单向和
单 coordinate 五种值，证明 geometry 不决定 source sign，但现在缺失的 arithmetic
quantity 已被明确写出。

## Claim firewall

```text
TPC228_ROUTE_ADVANCE = YES
TPC228_COMMON_PROFILE_PACKET_RULE = PROVED_EXACT
TPC228_POLARIZED_AP_MINUS_DIAGONAL_COMPILER = PROVED_EXACT
TPC228_SOURCE_LABELLED_COLLISION_SUM = PROVED_EXACT
TPC228_Q25_3_7_SOURCE_BLOCK = PROVED_EXACT_FINITE
TPC228_ACTUAL_V59_TO_PRIMITIVE_ATOM_CROSSWALK = OPEN
TPC228_ARITHMETIC_SIGN_THEOREM = OPEN
TPC228_ARITHMETIC_CANCELLATION = NONE
TPC228_ARITHMETIC_ADVANCE = NO
TPC228_FIXED_ATOM_CREDIT = 0
TPC228_L2 = NONE
TPC228_FULL_GATE_B = OPEN
TPC228_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC228_STATUS = PROVED_STRUCTURAL_L1
TPC228_ROUND2_CLUE = ANALYZE_THE_SOURCE_NATIVE_3_7_COLLISION_GRAPH_AS_EXACT_TWO_BY_TWO_BLOCKS
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/compiler_adversary.py
```

Bridge proof/checker：

```text
research/tpc-big-road/bridge_b_source_native_polarized_collision_compiler.md
research/tpc-big-road/tpc_bridge_b_source_native_polarized_collision_compiler_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/source_native_compiler.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/compiler_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
