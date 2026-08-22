# TPC-225: Cutoff-One Shared-Clock Obstruction

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / CUTOFF_ONE_SHARED_CLOCK_OBSTRUCTION`

TPC-224 的下一步是检查 AP marginal 与 polarized marginal 是否能在同一 source clock
上同时产生 saving。本篇先审计 TPC-224 使用的 named source-surrogate clock：

```text
x=Q^3,  H=4Q^2,  h=4Q,  Q<q<=2Q prime.
```

对 literal row family，

```text
floor(hq/H)=floor(q/Q)=1.
```

因此每个 prime row 只含 `m=+1,-1` 两个 residue coordinates。本文证明不同
prime rows 的两个点支持两两不交，从而得到 exact identities

```text
E_AP  = E_diag
E_all = E_pol.
```

第一个 identity 是本篇的核心 obstruction：只要 `E_diag>0`，这个 clock 上不存在
任何严格的 prime-label AP saving `E_AP <= (1-delta) E_diag`。第二个 identity 说明
full reassembly 的变化完全来自 packet direction；packet cancellation 是否发生取决于
profile sums，而不是 AP row dispersion。

## Claim firewall

```text
TPC225_ROUTE_ADVANCE = YES
TPC225_CUTOFF_ONE = PROVED_EXACT
TPC225_SUPPORT_DISJOINTNESS = PROVED_EXACT
TPC225_AP_EQUALS_DIAGONAL = PROVED_EXACT
TPC225_ALL_EQUALS_POLARIZED = PROVED_EXACT
TPC225_AP_SAVING_ON_NAMED_CLOCK = REFUTED_SCOPED
TPC225_POLARIZED_SAVING = PROFILE_DEPENDENT_OPEN
TPC225_V46_CLOCK_TRANSFER = OPEN
TPC225_ARITHMETIC_ADVANCE = NO
TPC225_FIXED_ATOM_CREDIT = 0
TPC225_L2 = NONE
TPC225_FULL_GATE_B = OPEN
TPC225_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC225_STATUS = PROVED_STRUCTURAL_L1
TPC225_ROUND2_CLUE = MOVE_TO_NONTRIVIAL_CUTOFF_CLOCK_BEFORE_CLAIMING_AP_DISPERSION
```

The source clock is explicitly a finite modeling choice inherited from TPC-224. This paper
does not claim that every possible V46 clock has cutoff one, and it does not transfer the
obstruction through an unproved physical synthesis map.

## Exact finite audit

The producer and independent checker both use exact `Fraction` arithmetic. They audit:

1. nine actual-prime affine-profile scales `Q=(11,17,29,43,61,89,127,181,257)`;
2. seven aligned-profile and seven balanced-profile boundary scales;
3. every integer `Q=3,...,99` for cutoff and support-disjointness regression.

The affine profiles are the TPC-224 profiles
`psi_j(t)=1+s_j t` with `s=(0,1,-1,2)/10`. The balanced fixture has zero packet sums,
so it gives `E_pol=E_all=0` while `E_AP=E_diag>0`; the aligned fixture gives the opposite
packet extreme. These are exact profile fixtures, not asymptotic evidence.

## Reproduce

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/boundary_adversary.py
```

The proof record and release checker are:

```text
research/tpc-big-road/bridge_b_cutoff_one_shared_clock_obstruction.md
research/tpc-big-road/tpc_bridge_b_cutoff_one_shared_clock_obstruction_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/cutoff_one_obstruction.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/boundary_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
