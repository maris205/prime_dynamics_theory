# TPC-235: V59 Physical-Depth Crosswalk

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / SINGLE_CLOCK_AND_OUTPUT_NORMALIZATION_REFUTED_SCOPED`

本篇把实际 V59 row 与 TPC-226--234 modeled rows 逐因子对齐。对 physical denominator
`h`，正确 depth 变量是

```text
lambda_h = hQ/H,
cutoff = floor(lambda_h q/Q),
profile argument = mQ/(lambda_h q),
modulus = h.
```

TPC-226 row 同时匹配 modulus 与 cutoff/profile 当且仅当

```text
h=4LQ and H=4Q^2.
```

但 V59 scales 为 `H=x^(21/32)`, `Q=x^(1/3)`，故
`4Q^2/H=4x^(1/96)`。同 depth 下 modeled modulus 比 physical modulus 大这个
growing factor；exact single-clock attachment 因而 `REFUTED_SCOPED`。

此外，V59 要求同一个 linear transform 作用于 `beta+i^j w`。若把每个 packet output
单独 unit-normalize，则四个 squared norms 都变成一，signed polarization 恒为零；
`(beta,w)=(1,2)` 的原值为 `2`，归一化后为 `0`。因此 TPC-234 output normalization
不是自动 source-valid。

## Claim firewall

```text
TPC235_ROUTE_ADVANCE = YES
TPC235_V59_PHYSICAL_DEPTH_VARIABLE = PROVED_EXACT_LAMBDA_H_EQ_HQ_OVER_H
TPC235_PHYSICAL_ROW_REPARAMETERIZATION = PROVED_EXACT
TPC235_SINGLE_CLOCK_COMPATIBILITY_IFF_H_EQ_4Q_SQUARED = PROVED_EXACT
TPC235_V59_CLOCK_RATIO = PROVED_EXACT_4X_TO_1_OVER_96
TPC235_TPC226_EXACT_SINGLE_CLOCK_ATTACHMENT = REFUTED_SCOPED
TPC235_PHYSICAL_DEPTH_RANGE = PROVED_EXACT_HALF_TO_X_23_OVER_2400
TPC235_PHYSICAL_DENOMINATOR_GRID_PER_DEPTH = PROVED_X_31_OVER_96
TPC235_DIVISOR_WEIGHT_C_H = SOURCE_LOCKED_REQUIRED
TPC235_FULL_H_SUM = SOURCE_LOCKED_REQUIRED
TPC235_COMMON_PACKET_TRANSFORM = SOURCE_LOCKED_REQUIRED
TPC235_OUTPUT_UNIT_NORMALIZATION_POLARIZATION = REFUTED_SCOPED
TPC235_SOURCE_VALID_NORMALIZATION = OPEN_WEIGHTED_LINEAR_ONLY
TPC235_ARITHMETIC_ADVANCE = NO
TPC235_ARITHMETIC_CANCELLATION = NONE
TPC235_FIXED_ATOM_CREDIT = 0
TPC235_L2 = NONE
TPC235_FULL_GATE_B = OPEN
TPC235_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC235_STATUS = PROVED_STRUCTURAL_L1
TPC235_ROUND2_CLUE = BUILD_PHYSICAL_H_FIBER_DIRECT_SUM_WITH_COMMON_PACKET_TRANSFORM_AND_EXPLICIT_WEIGHTS
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/crosswalk_adversary.py
```

Bridge proof/checker：

```text
research/tpc-big-road/bridge_b_v59_physical_depth_crosswalk.md
research/tpc-big-road/tpc_bridge_b_v59_physical_depth_crosswalk_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/v59_crosswalk.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/crosswalk_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
