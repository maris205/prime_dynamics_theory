# TPC-234: Normalized Collision-Bessel Stability

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / DEPTH_UNIFORM_NORMALIZED_BESSEL_BOUND`

TPC-233 证明 raw row masses 在临界深度可不可比。本篇执行最小修复：将每条非零
row vector 归一化为单位范数。TPC-232 one-wrap geometry 保证每个 residue bucket
最多包含两条 prime rows，因此对 synthesis operator `Tc=sum_q c_q u_q`，

```text
0 <= G=T* T <= 2I,
-I <= K=G-I <= I,
||K|| <= 1,
0 <= ||Tc||^2/sum|c_q|^2 <= 2.
```

常数 `2` 与 depth、row masses、profile amplitudes 无关。它在 abstract
multiplicity-two support class 中 sharp；但 literal clock `Q=39,L=7`, rows `67,71`
给出 exact symmetric ratio `4/3>1` 与 antisymmetric ratio `2/3<1`。所以
normalization 修复 conditioning，却不提供自动 sub-diagonal saving。

## Claim firewall

```text
TPC234_ROUTE_ADVANCE = YES
TPC234_BUCKET_MULTIPLICITY_TWO = INHERITED_PROVED_EXACT
TPC234_UNIT_ROW_NORMALIZATION = MODELING_TRANSFORM
TPC234_NORMALIZED_SYNTHESIS_BESSEL_BOUND = PROVED_EXACT_2
TPC234_NORMALIZED_GRAM_SPECTRUM = PROVED_EXACT_IN_0_2
TPC234_OFFDIAGONAL_GRAM_NORM = PROVED_EXACT_LE_1
TPC234_DEPTH_UNIFORM_CONDITIONING = PROVED_EXACT
TPC234_AMBIENT_CONSTANT_TWO = PROVED_EXACT_SHARP
TPC234_Q39_LITERAL_NORMALIZED_RATIOS = PROVED_EXACT_4_OVER_3_AND_2_OVER_3
TPC234_NORMALIZATION_AUTOMATIC_SAVING = REFUTED_SCOPED
TPC234_SOURCE_VALID_NORMALIZATION = OPEN
TPC234_ACTUAL_V59_CROSSWALK = OPEN
TPC234_ARITHMETIC_ADVANCE = NO
TPC234_ARITHMETIC_CANCELLATION = NONE
TPC234_FIXED_ATOM_CREDIT = 0
TPC234_L2 = NONE
TPC234_FULL_GATE_B = OPEN
TPC234_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC234_STATUS = PROVED_STRUCTURAL_L1
TPC234_ROUND2_CLUE = TRACE_ACTUAL_V59_ROW_WEIGHTS_AND_TEST_SOURCE_VALID_NORMALIZATION
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/operator_adversary.py
```

Bridge proof/checker：

```text
research/tpc-big-road/bridge_b_normalized_collision_bessel_stability.md
research/tpc-big-road/tpc_bridge_b_normalized_collision_bessel_stability_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/normalized_collision.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/operator_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
