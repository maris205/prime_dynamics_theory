# TPC-221: Collision-Graph Schur Envelope and Literal Saturation

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / COLLISION_GRAPH_SCHUR_ENVELOPE`

TPC-220 将 q-transverse quantity 精确写成 multiplicative collision Gram。TPC-221
完成下一步最小定量推进：把该 Gram 视为正半定矩阵，证明任意 q-weights 的 collision
energy 受其 absolute row-sum（Schur）envelope 控制，并给出 weighted Schur 版本的
可复用接口。

对 literal row vectors `B_q`，令

```text
Gamma(q,q') = <B_q,B_q'>,
E(lambda) = sum_a |sum_q lambda_q B_q(a)|^2.
```

则

```text
E(lambda) = lambda^* Gamma lambda
          <= ||Gamma||_op ||lambda||_2^2
          <= (max_q sum_q' |Gamma(q,q')|) ||lambda||_2^2.
```

这不是 arithmetic cancellation。一个 literal finite fixture（`h=5`, `H=500`,
`q={101,151,181,191}`, constant profile）中所有 q rows 都等于
`e_1+e_4`，所以 `Gamma=2*J_4`，top Rayleigh quotient、Schur row sum 与
`P`-times diagonal energy 完全相等。由此，absolute Schur control 在该 scope 内
不能自动击破 `P` collapse。

## Claim firewall

```text
TPC221_ROUTE_ADVANCE = YES
TPC221_COLLISION_GRAM_PSD = PROVED_EXACT
TPC221_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_WEIGHTED_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_LITERAL_SATURATION = PROVED_EXACT_FINITE
TPC221_ABSOLUTE_SCHUR_SUBP_SAVING = REFUTED_SCOPED
TPC221_ARITHMETIC_ADVANCE = NO
TPC221_FIXED_ATOM_CREDIT = 0
TPC221_L2 = NONE
TPC221_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC221_FULL_GATE_B = OPEN
TPC221_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC221_STATUS = PROVED_STRUCTURAL_L1
TPC221_ROUND2_CLUE = SEEK_SIGNED_PHASE_DISPERSION_BEYOND_ABSOLUTE_COLLISION_DEGREES
```

## Layout

```text
paper/paper.pdf
paper/main.tex
code/collision_schur.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/schur_saturation_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
