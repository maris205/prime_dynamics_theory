# TPC-219: Prime-Shell Longitudinal Ledger and the Exact P Collapse

作者：Liang Wang（Huazhong University of Science and Technology）
更新时间：2026-08-22

状态：`PROVED_STRUCTURAL_L1 / EXACT_LONGITUDINAL_TRANSVERSE_LEDGER`

TPC-218 保留了 prime label `q`，但 scalar recovery 只记录了一个 `P`-factor
upper bound. TPC-219 把这一步改写成一个 exact Hilbert-space identity。令
`Z_q(n)=(K_(j,q)(n))_j`，`P=#Q_x`，以及

```text
Zbar(n) = P^(-1) sum_q Z_q(n),
R_q(n) = Z_q(n)-Zbar(n).
```

则对任意有限 interval `I`，有

```text
E_shell = P (E_diag - E_perp),

E_shell = sum_(n in I)||sum_q Z_q(n)||_2^2,
E_diag  = sum_(n in I)sum_q ||Z_q(n)||_2^2,
E_perp  = sum_(n in I)sum_q ||R_q(n)||_2^2.
```

因此 `P` collapse 的严格改善不是一个泛化的 Cauchy 技巧，而是等价于对
literal prime labels 证明一个 transverse lower bound：若目标是
`E_shell <= eta P E_diag`，充要条件是
`E_perp >= (1-eta) E_diag`。

本篇的明确进展是把下一条算术问题从“希望 q 有 cancellation”改成了一个精确的
longitudinal/transverse theorem。aligned rows 使 `E_perp=0` 并饱和 `P`；balanced
rows 使 shell 能量为零并达到另一端点。两者是有限结构性控制，不是渐近素数反例。

## Claim firewall

```text
TPC219_ROUTE_ADVANCE = YES
TPC219_LONGITUDINAL_TRANSVERSE_IDENTITY = PROVED_EXACT
TPC219_P_COLLAPSE_EQUIVALENCE = PROVED_EXACT
TPC219_ALIGNED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_BALANCED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_ARITHMETIC_ADVANCE = NO
TPC219_FIXED_ATOM_CREDIT = 0
TPC219_L2 = NONE
TPC219_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC219_FULL_GATE_B = OPEN
TPC219_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC219_STATUS = PROVED_STRUCTURAL_L1
TPC219_ROUND2_CLUE = REEXPRESS_TRANSVERSE_ENERGY_AS_LITERAL_PRIME_AP_COLLISION_DATA
```

Route A is not applicable. Route-B structural threshold A passes. No arithmetic `L2`,
fixed-atom credit, strict `1/400` payment, or twin-prime conclusion is claimed.

## Layout

```text
paper/paper.pdf
paper/main.tex
code/longitudinal_transverse.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/adversarial_alignment.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```

The bridge proof and fail-closed release checker are in
`research/tpc-big-road/bridge_b_prime_shell_longitudinal_transverse_ledger.md` and
`research/tpc-big-road/tpc_bridge_b_prime_shell_longitudinal_transverse_ledger_checker.py`.

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/adversarial_alignment.py
```

All fixture arithmetic uses exact rational vectors. The certificate is a structural
identity check, not an asymptotic estimate for the literal twin-prime kernel.
