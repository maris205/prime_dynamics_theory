# TPC-218 — Prime-Shell Hilbert Lift and the Sharp Collapse Barrier

作者：Liang Wang（Huazhong University of Science and Technology）

状态：PROVED_STRUCTURAL_L1 / PRIME_LABEL_AND_PACKET_PRESERVING_LIFT

TPC-217 已经把 common-source kernel 接到 literal finite window，但在 large-sieve
之前把 prime shell 合并了。本篇保留两个外层标签：prime label q 与 four-packet
label j。结果是一个可直接复用的 Hilbert-valued additive large-sieve lift：

~~~
N^(-1) sum_(n in I_x)||K_vec(n)||_2^2
  << J M^2 x^(1/96)(log x)^5,

K_vec(n)=(K_(j,q)(n))_(j,q).
~~~

对 packet shell 再做唯一必要的 scalar collapse，逐点 Cauchy 付出
P=#Q_x<=2Q，于是恢复

~~~
N^(-1) sum_(n in I_x) sum_j |K_j(n)|^2
  << J M^2 x^(11/32)(log x)^5.
~~~

这不是 arithmetic cancellation。它的价值在于把 TPC-217 的瓶颈精确拆成一个
可审计的 P 因子：后续若要取得真正的 signed prime-shell saving，必须明确击破这一
collapse，而不能把分裂坐标的 x^(1/96) 误报成最终 scalar 进展。

本篇还提供两个 adversarial controls：

- d=5, H=500, q={101,131,151,181}, psi=1 时所有 q rows 都支撑在 {1,4}，
  coherent/diagonal ratio 精确为 4=P；
- 四个 packet 向量平行时，相应 unit projection 可捕获全部能量，ratio 精确为 1。

两者都是 scoped structural obstructions，不是 V46 渐近反例。

## Claim firewall

~~~
TPC218_HILBERT_VALUED_LARGE_SIEVE = PROVED_STANDARD_TENSOR_LIFT
TPC218_PRIME_LABEL_PRESERVATION = PROVED_EXACT
TPC218_PACKET_MATRIX_BOUND = PROVED_EXACT
TPC218_SPLIT_NORMALIZED_EXPONENT = PROVED_1_OVER_96_LOG_FIVE
TPC218_SCALAR_COLLAPSE_RECOVERY = PROVED_X_11_OVER_32_LOG_FIVE
TPC218_Q_COLLAPSE_COST = PROVED_P_FACTOR
TPC218_Q_ORTHOGONALITY = REFUTED_SCOPED
TPC218_PACKET_ALIGNMENT = REFUTED_SCOPED
TPC218_ARITHMETIC_ADVANCE = NO
TPC218_FIXED_ATOM_CREDIT = 0
TPC218_L2 = NONE
TPC218_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC218_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC218_FULL_GATE_B = OPEN
TPC218_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
~~~

Route A is not applicable. Route-B structural threshold A passes. The current
open theorem is a literal signed prime-shell/four-packet reassembly that beats
the exact P collapse while preserving all physical masks, zero/nonunit terms,
and normalization.

## Files

~~~
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/prime_shell_packet_lift.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/adversarial_alignment.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
~~~

The main proof record is research/tpc-big-road/bridge_b_prime_shell_packet_lift.md,
with the fail-closed release checker at
research/tpc-big-road/tpc_bridge_b_prime_shell_packet_lift_checker.py.

## Reproduce

From this project directory:

~~~
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/adversarial_alignment.py --check
~~~

All finite coefficients are exact rational values before exponential evaluation.
The fixture uses mu(d)/d only as an exact index-map surrogate; the theorem and
proof retain the literal mu(d)log(d)/d source coefficient.
