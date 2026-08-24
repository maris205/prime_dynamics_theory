# TPC-229: Matching and Sharp Block Spectrum of the Primitive 3--7 Resonance Graph

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / PRIMITIVE_RESONANCE_MATCHING_SPECTRUM`

TPC-228 把 source-native signed quantity 写成 `3--7` collision sum。本篇证明该 graph
远比一般 collision graph 刚性：对每条 edge `(p,r)`，

```text
7p+3r=16Q, p<r
```

强迫

```text
10Q/7 < p < 8Q/5 < r < 2Q.
```

低、高 endpoint intervals 不交；同时 `p` 或 `r` 都唯一决定 counterpart。因此对每个
`Q>=8`，primitive resonance graph 是 matching。每条 edge 的 two-coordinate swap
operator spectrum 为 `(-1,-1,+1,+1)`，全局 operator 是这些 blocks 与 isolated zeros
的 direct sum。

对 symmetric source row vectors `u,v`，exact

```text
E_diag = E_sym + E_anti
E_collision = E_sym - E_anti
E_AP = 2 E_sym
0 <= E_AP/E_diag <= 2.
```

`E_AP <= (1-delta)E_diag` 当且仅当
`(1+delta)E_sym <= (1-delta)E_anti`。因此 signed saving 的缺口被压成逐 block
antisymmetric dominance。`Q=8..4096` 的 4089-scale replay 覆盖 13,754 条 edges，
maximum degree 始终为 one。

## Claim firewall

```text
TPC229_ROUTE_ADVANCE = YES
TPC229_RESONANCE_GRAPH_MATCHING = PROVED_EXACT
TPC229_LOW_HIGH_ENDPOINT_SEPARATION = PROVED_EXACT
TPC229_EDGE_SPECTRUM = PROVED_EXACT
TPC229_GLOBAL_BLOCK_DIRECT_SUM = PROVED_EXACT
TPC229_SHARP_AP_RATIO_RANGE = PROVED_EXACT
TPC229_DELTA_SAVING_CRITERION = PROVED_EXACT
TPC229_SOURCE_BILINEAR_BLOCK_BOUND = PROVED_EXACT_SHARP
TPC229_ARITHMETIC_ANTISYMMETRIC_DOMINANCE = OPEN
TPC229_ACTUAL_V59_ATOM_CROSSWALK = OPEN
TPC229_ARITHMETIC_ADVANCE = NO
TPC229_FIXED_ATOM_CREDIT = 0
TPC229_L2 = NONE
TPC229_FULL_GATE_B = OPEN
TPC229_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC229_STATUS = PROVED_STRUCTURAL_L1
TPC229_ROUND2_CLUE = QUANTIFY_MATCHED_RESONANCE_MASS_BEFORE_SEEKING_A_FIXED_PROPORTIONAL_SAVING
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/matching_adversary.py
```

Bridge proof/checker：

```text
research/tpc-big-road/bridge_b_primitive_resonance_matching_spectrum.md
research/tpc-big-road/tpc_bridge_b_primitive_resonance_matching_spectrum_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/resonance_matching.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/matching_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
