# TPC-236: Physical Multi-Wrap Collision Envelope

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / SOURCE_VALID_PHYSICAL_FIBER_BESSEL_ENVELOPE`

本篇在 TPC-235 exact V59 crosswalk 后，直接研究真实 row

```text
0<|m|<=floor(hq/H),
a=mq^(-1) mod h,
Q<q<=2Q prime.
```

对固定 residue `a`，令 `g=gcd(a,h)` 和 `M_h=floor(2hQ/H)`。精确 gcd-fiber counting
给出 row bucket multiplicity

```text
R_h(a)
 <= 2 floor(M_h/g) ceil(Qg/h)
 <= 4Q^2/H + 4hQ/(gH)
 <= 8Q^2/H.
```

因此无需逐 row unit-normalize，对每个 physical `h` 已有 source-valid Bessel bound；
保留任意显式 `C_h` 后，physical `h`-direct-sum 仍只付上述 factor。V59 下它精确至
`4x^(1/96)+4x^(23/2400)=(4+o(1))x^(1/96)` 的 energy-level toll。

另一方面，`Q=101,H=8830,h=80` 的 V59-shaped exact fixture 中，
`H=floor(Q^(63/32))`、`h<=floor(Q^(399/400))=99` 均由整数幂比较认证；prime rows
`q=113,127,193` 都支撑在 `{17,63}`，故 bucket multiplicity 为 `3`，equal-row
Bessel ratio exact 为 `3`。TPC-234 multiplicity-two theorem 不能直接 transfer 到
physical rows。

## Claim firewall

```text
TPC236_ROUTE_ADVANCE = YES
TPC236_PHYSICAL_ROW_INTERNAL_INJECTIVITY = PROVED_FOR_H_GT_4Q
TPC236_BUCKET_GCD_FIBER_BOUND = PROVED_EXACT
TPC236_BUCKET_MULTIPLICITY = PROVED_LE_8Q_SQUARED_OVER_H
TPC236_WEIGHTED_FIXED_H_BESSEL = PROVED_EXACT_WITHOUT_ROW_NORMALIZATION
TPC236_WEIGHTED_PHYSICAL_H_DIRECT_SUM = PROVED_EXACT
TPC236_COMMON_LINEAR_PACKET_TRANSFORM = PRESERVED_WITH_OPERATOR_NORM
TPC236_DIVISOR_WEIGHT_C_H = PRESERVED_EXPLICITLY
TPC236_V59_MULTIPLICITY_TOLL = PROVED_4X_1_OVER_96_PLUS_4X_23_OVER_2400
TPC236_Q101_TRIPLE_COLLISION = PROVED_EXACT
TPC236_Q101_EQUAL_ROW_RATIO = PROVED_EXACT_3
TPC236_PHYSICAL_MULTIPLICITY_TWO_TRANSFER = REFUTED_SCOPED
TPC236_GCD_FIBER_REDUCTION = REQUIRED
TPC236_CROSS_H_RATIONAL_FREQUENCY_REASSEMBLY = OPEN
TPC236_C_H_WEIGHTED_CANCELLATION = OPEN
TPC236_ARITHMETIC_ADVANCE = NO
TPC236_ARITHMETIC_CANCELLATION = NONE
TPC236_FIXED_ATOM_CREDIT = 0
TPC236_L2 = NONE
TPC236_FULL_GATE_B = OPEN
TPC236_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC236_STATUS = PROVED_STRUCTURAL_L1
TPC236_ROUND2_CLUE = COMBINE_PHYSICAL_H_FIBER_ENVELOPE_WITH_REDUCED_FREQUENCY_LARGE_SIEVE_AND_TEST_C_H_WEIGHTED_CANCELLATION
```

`(4+o(1))x^(1/96)` 与 V59 benchmark local saving `x^(-1/96)` 在同一 energy ledger 中相乘
时 margin 为零；这里只记录 exact exponent collision，不宣称所有尚未完成的 reassembly
必然按这一方式相乘。

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/multiwrap_adversary.py
```

Bridge proof/checker：

```text
research/tpc-big-road/bridge_b_physical_multiwrap_collision_envelope.md
research/tpc-big-road/tpc_bridge_b_physical_multiwrap_collision_envelope_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/physical_multiwrap.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/multiwrap_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
