# TPC-237: Collision-Compressed Finite-Window Reassembly

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1_COMMON_SOURCE_COLLISION_COMPRESSED_FINITE_WINDOW_PACKET_TRACE`

本篇在完全相同的 TPC-218 common-source kernel 上改变两步不等式的顺序：先用
TPC-236 在每个 primitive physical frequency bucket 内压缩 prime-shell label，
再用 TPC-217 reduced-frequency large sieve 连接有限整数窗口。对

```text
K_j(n)
 = sum_(h<=U) sum_((a,h)=1)
     C_h (sum_(q in Q_x) B_(h,q)^(j)(a)) e(na/h),
```

primitive 条件使 TPC-236 的 `g=gcd(a,h)` 精确退化为 `g=1`，从而

```text
R_h(a) <= 4Q^2/H + 4hQ/H
       <= 4Q^2/H + 4UQ/H = R_*.
```

将这个 collision factor 放在 large sieve 之前，得到

```text
N^(-1) sum_(n in I_x) sum_j |K_j(n)|^2
 << J M^2 [x^(1/48)+x^(1/50)](log x)^5.
```

相比 TPC-218 scalar recovery 的 `x^(11/32)`，这里不再支付额外的粗糙
`P=#Q_x` collapse；主结构 exponent 降为 `1/48`。leading unnormalized exponent
为 `49/48+o(1)`，而 window correction `U^2/N=x^(-67/200+o(1))` 为低阶项。

## Claim firewall

```text
TPC237_ROUTE_ADVANCE = YES
TPC237_PRIMITIVE_FREQUENCY_INDEX = REQUIRED_EXACT
TPC237_Q_COLLISION_BEFORE_LARGE_SIEVE = PROVED_EXACT_COMPOSITION
TPC237_PRIMITIVE_BUCKET_FACTOR = PROVED_LE_4Q_SQUARED_OVER_H_PLUS_4UQ_OVER_H
TPC237_DIRECT_COEFFICIENT_ENERGY = PROVED_X_1_OVER_96_LOG_FIVE
TPC237_FINITE_WINDOW_PACKET_TRACE = PROVED_STRUCTURAL
TPC237_NORMALIZED_MAIN_EXPONENT = PROVED_1_OVER_48
TPC237_NORMALIZED_SECONDARY_EXPONENT = PROVED_1_OVER_50
TPC237_UNNORMALIZED_MAIN_EXPONENT = PROVED_49_OVER_48
TPC237_WINDOW_FACTOR = PROVED_1_PLUS_U_SQUARED_OVER_N
TPC237_OLD_P_COLLAPSE = REPLACED_BY_PHYSICAL_COLLISION_FACTOR
TPC237_SIMULTANEOUS_SATURATION = NOT_CLAIMED
TPC237_C_H_SIGNED_CANCELLATION = NONE
TPC237_SIGNED_FOUR_PACKET_GATE_B_SCALAR = OPEN
TPC237_ARITHMETIC_ADVANCE = NO
TPC237_FIXED_ATOM_CREDIT = 0
TPC237_L2 = NONE
TPC237_FULL_GATE_B = OPEN
TPC237_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC237_STATUS = PROVED_STRUCTURAL_L1
TPC237_ROUND2_CLUE = TEST_THE_ACTUAL_WEIGHTED_COLLISION_ENERGY_BEFORE_SEEKING_CROSS_H_SIGN_CANCELLATION
```

`sum_j |K_j|^2` 是 unsigned packet trace，不等于 signed four-packet Gate-B
scalar。定理保留 literal signed `C_h`，但证明随后使用 `|C_h|^2` 与 absolute
harmonic majorant，所以没有宣称任何 divisor-sign cancellation 或 arithmetic
advance。

## Finite reproduction

证书使用 exact V59-shaped fixture

```text
(Q,H,U,h)=(101,8830,99,82), q in {109,137,191}.
```

`h=82` 是平方自由分母，source band 中 `d=82` 给出非零 rational marked-divisor
reproduction weight `C_82^(rat)=1/82`。两个 packet 的 direct energy 为 `3/1681`，
collapsed trace 为 `5/1681`，collision ratio 为 `5/3`；长度 `82` 的完整窗口上
exact energy 为 `10/41`。有限数据只复现代数，不替代 literal `log d` 渐近源。

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B experiments/run_certificate.py --check
python -O -B experiments/run_certificate.py --check
python -B experiments/independent_checker.py
python -O -B experiments/independent_checker.py
python -B experiments/window_stress.py
python -O -B experiments/window_stress.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/references.bib
paper/sections/*.tex
paper/paper.pdf
code/finite_window_physical_reassembly.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/window_stress.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
