# TPC-224: Literal Two-Channel Compatibility Audit

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / LITERAL_TWO_CHANNEL_COMPATIBILITY`

TPC-223 留下了一个最关键但最容易被偷换的输入：AP/collision channel、four-packet
polarized channel 与完整 shell reassembly 必须作用在同一个 literal object 上。本篇
把这个接口写成一个共同 Hilbert-vector theorem。

对同一组 vectors `W_(q,j)` 定义

```text
E_AP  = sum_j ||sum_q W_(q,j)||^2
E_pol = sum_q ||sum_j W_(q,j)||^2
E_all = ||sum_(q,j) W_(q,j)||^2.
```

则 exact Cauchy 与 scalar min-to-sum identity 给出

```text
E_all <= min(J E_AP, P E_pol)
       <= P J/(P+J) (E_AP+E_pol).
```

`P J/(P+J)` 是 sharp；令所有 `W_(q,j)=u` 即达到等号。因而 `J=4` 固定时，这个
共同结构因子是 `O(1)`，在指数账本中没有 power loss。但朴素的 unit-factor 版本
`E_all <= E_AP+E_pol` 不成立：在独立的 collision-stress clock
`H=5Q, h=5, q=1 (mod 5)` 下，actual prime rows 完全对齐，5 个增长尺度均精确达到
sharp factor 并 refute unit interface。

## Claim firewall

```text
TPC224_ROUTE_ADVANCE = YES
TPC224_COMMON_LITERAL_HILBERT_INTERFACE = PROVED_EXACT
TPC224_SHARP_ADDITIVE_CONSTANT = PROVED_EXACT
TPC224_UNIT_INTERFACE = REFUTED_SCOPED
TPC224_SOURCE_CLOCK_AUDIT = NUMERICALLY_CERTIFIED_EXACT_RATIONAL
TPC224_AP_DISPERSION = OPEN
TPC224_POLARIZED_CROSS_CORRELATION = OPEN
TPC224_LITERAL_V46_TRANSFER = OPEN
TPC224_ARITHMETIC_CANCELLATION = NONE
TPC224_ARITHMETIC_ADVANCE = NO
TPC224_FIXED_ATOM_CREDIT = 0
TPC224_L2 = NONE
TPC224_FULL_GATE_B = OPEN
TPC224_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC224_STATUS = PROVED_STRUCTURAL_L1
TPC224_ROUND2_CLUE = PROVE_SHARED_CLOCK_AP_AND_POLARIZED_MARGINAL_SAVINGS
```

`Route A` is not applicable. `Route B` passes only at structural L1. The paper does not
prove either marginal arithmetic saving, fixed-atom credit, strict `1/400`, or the twin-prime
conjecture.

## Exact finite audit

The producer uses the TPC-220 row rule

```text
B_(h,q)^(j)(a) = sum_m psi_j(Hm/(hq)) 1_(m q^(-1)=a mod h)
```

and freezes the same `C_h=1/h`, support, `m`, `h`, `q`, and `j` before forming all three
energies. Nine source-surrogate scales use actual primes in `(Q,2Q]`; five separately
named stress scales use actual primes congruent to `1 mod 5`. All arithmetic is exact over
`Fraction`, and `experiments/independent_checker.py` reconstructs the rows without importing
the producer.

The two clocks are deliberately not an asymptotic splice. The source-surrogate records are
finite growing observations; the stress records are a scoped adversary for the normalization
interface.

## Reproduce

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/boundary_adversary.py
```

The proof record and fail-closed release checker are
`research/tpc-big-road/bridge_b_literal_two_channel_compatibility_audit.md` and
`research/tpc-big-road/tpc_bridge_b_literal_two_channel_compatibility_audit_checker.py`.

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/literal_compatibility.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/boundary_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
