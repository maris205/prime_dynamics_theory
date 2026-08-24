# TPC-231: A Finite-Resonance Sieve Obstruction on Prime Shells

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_ARITHMETIC_OBSTRUCTION_L1 / FIXED_FINITE_RESONANCE_STOP_SCOPED`

TPC-230 证明 first `3--7` matching 能取得的 global saving 不超过 matched row mass，
并把 strict `1/400` 转化为必要条件 `E(Q)/P(Q)>=1/3200`。本篇用 classical
Selberg upper-bound sieve 证明这个必要条件渐近失败。

当 `gcd(Q,21)=1` 时，写 `Q=3t+a`、`a in {1,2}`。共振方程

```text
7p+3r=16Q
```

精确参数化为

```text
p=3k+a,
r=16t+3a-7k,
determinant=16Q.
```

局部坏剩余类数为

```text
nu_Q(ell)=1,  ell in {2,3,7} or ell|Q,
nu_Q(ell)=2,  otherwise.
```

因此标准二维 Selberg 上界筛给出

```text
E_3716(Q) << S_3716(Q) Q/(log Q)^2,
S_3716(Q) << log log(3Q),
E_3716(Q)/P(Q) -> 0.
```

结合 TPC-230 的 exact `M/D<=8E/P`，literal aligned first-resonance matched mass
也趋于零，所以该机制即使每条边 perfect anti-align，也不能在所有充分大尺度支付
任何 fixed `delta>0`，特别不能支付 `1/400`。

同一筛法还证明：任意固定有限组 primitive nondegenerate linear resonance families
的边与 incident-row 密度均为 `o(1)`。这封闭的是 fixed finite resonance / comparable
row model；growing resonance depth 与 actual V59 source crosswalk 保持 `OPEN`。

## Claim firewall

```text
TPC231_ROUTE_ADVANCE = YES
TPC231_3716_PARAMETERIZATION = PROVED_EXACT
TPC231_3716_LOCAL_ROOT_LAW = PROVED_EXACT
TPC231_3716_SELBERG_UPPER_BOUND = PROVED_SOURCE_BACKED
TPC231_3716_SINGULAR_SERIES_GROWTH = PROVED
TPC231_3716_EDGE_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC231_FIXED_FINITE_RESONANCE_SUPPORT_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC231_LITERAL_MATCHED_MASS_DENSITY_ZERO = PROVED_IN_LITERAL_ALIGNED_MODEL
TPC231_FIRST_PRIMITIVE_3_7_FIXED_SAVING = STOP_SCOPED
TPC231_FIXED_FINITE_RESONANCE_COMPARABLE_ROW_ROUTE = STOP_SCOPED
TPC231_GROWING_RESONANCE_DEPTH = OPEN
TPC231_ACTUAL_V59_SOURCE_MASS_CROSSWALK = OPEN
TPC231_ARITHMETIC_ADVANCE = NO
TPC231_ARITHMETIC_OBSTRUCTION = PROVED_SOURCE_BACKED
TPC231_FIXED_ATOM_CREDIT = 0
TPC231_L2 = NONE
TPC231_FULL_GATE_B = OPEN
TPC231_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC231_STATUS = PROVED_ARITHMETIC_OBSTRUCTION_L1
TPC231_ROUND2_CLUE = TEST_GROWING_RESONANCE_DEPTH_OR_RETURN_TO_THE_ACTUAL_V59_SOURCE_MASS_CROSSWALK
```

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/sieve_adversary.py
```

Bridge proof/checker：

```text
research/tpc-big-road/bridge_b_finite_resonance_sieve_obstruction.md
research/tpc-big-road/tpc_bridge_b_finite_resonance_sieve_obstruction_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/finite_resonance_sieve.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/sieve_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
