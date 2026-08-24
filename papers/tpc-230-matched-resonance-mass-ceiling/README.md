# TPC-230: Matched-Resonance Mass Ceiling for Global AP Saving

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / MATCHED_RESONANCE_MASS_CEILING`

TPC-229 证明 `3--7` graph 是 matching。本篇证明一个 sharp global obstruction。设
`D` 为总 diagonal mass、`M` 为 matched vertices 上的 diagonal mass。因为 unmatched
rows 完全不参与 collision，而每个 matched block 的 AP energy 非负，

```text
E_AP >= D-M,
D-E_AP <= M.
```

所以任何 fixed saving

```text
E_AP <= (1-delta)D
```

都必要地要求 `M/D>=delta`。这个 ceiling sharp：每条 matched edge 完全 anti-align 时
达到 `E_AP=D-M`。

若 row masses 的最大/最小比为 `kappa`，`P` 是 prime count、`E` 是 resonance edge
count，则

```text
M/D <= 2 kappa E/P.
```

TPC-226 literal aligned rows 每行 primitive atom count 在 `2..8`，故 `kappa<=4`；
支付 strict `1/400` 的必要 density toll 是

```text
E/P >= 1/3200.
```

Q25 的 uniform matched fraction 是 `1/3`，literal aligned fraction 是 `5/13`。
4089-scale scan 包含 1821 个 zero-edge scales，但有限 scan 不作渐近结论。

## Claim firewall

```text
TPC230_ROUTE_ADVANCE = YES
TPC230_UNMATCHED_ENERGY_FLOOR = PROVED_EXACT
TPC230_MATCHED_MASS_SAVING_CEILING = PROVED_EXACT_SHARP
TPC230_NECESSARY_MASS_FRACTION = PROVED_EXACT
TPC230_COMPARABLE_ROW_DENSITY_TOLL = PROVED_EXACT
TPC230_LITERAL_ALIGNED_KAPPA_LE_4 = PROVED_EXACT
TPC230_STRICT_1_OVER_400_EDGE_DENSITY_TOLL = 1/3200
TPC230_ASYMPTOTIC_RESONANCE_EDGE_DENSITY = OPEN
TPC230_ACTUAL_V59_SOURCE_MASS_COMPARABILITY = OPEN
TPC230_ARITHMETIC_ADVANCE = NO
TPC230_FIXED_ATOM_CREDIT = 0
TPC230_L2 = NONE
TPC230_FULL_GATE_B = OPEN
TPC230_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC230_STATUS = PROVED_STRUCTURAL_L1
TPC230_ROUND2_CLUE = APPLY_A_TWO_LINEAR_FORM_UPPER_BOUND_SIEVE_TO_THE_3_7_RESONANCE_COUNT
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
research/tpc-big-road/bridge_b_matched_resonance_mass_ceiling.md
research/tpc-big-road/tpc_bridge_b_matched_resonance_mass_ceiling_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/matched_mass_ceiling.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/mass_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
