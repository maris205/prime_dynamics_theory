# TPC-226: First Primitive-Collision Transition in Dilated Shared Clocks

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / FIRST_PRIMITIVE_COLLISION_TRANSITION`

TPC-225 证明 base clock `h=4Q` 的 cutoff-one prime rows 两两不交。本篇保留
TPC-220 primitive literal row、`H=4Q^2`、prime shell 与 `C_h=1/h`，只引入有限
integer dilation

```text
h_L=4LQ,  L=1,2,3,4,  Q>=8.
```

严格分类得到：`L=1,2,3` 仍无 legitimate cross-prime collision；`L=4` 首次出现，
且所有碰撞只能是

```text
7p+3r=16Q,
m_p=+/-3,
m_r=-/+7.
```

最小稳定 exact witness 是 `Q=25`, `(p,r)=(37,47)`，共享 residue 为 `119` 与
`281 mod 400`。同一 collision geometry 的符号并不固定：aligned 与 TPC-224 affine
profiles 都严格放大 `E_AP`，balanced sign profiles 则严格降低 `E_AP`，并 exact 给出
`E_pol=E_all=0`。因此“有碰撞”只建立 cancellation interface，不能替代 signed
arithmetic theorem。

## Claim firewall

```text
TPC226_ROUTE_ADVANCE = YES
TPC226_DILATED_CLOCK_FAMILY = MODELING_CHOICE
TPC226_PRIMITIVE_SOURCE_ROW = PROVED_EXACT
TPC226_L_LE_3_DISJOINTNESS = PROVED_EXACT
TPC226_FIRST_PRIMITIVE_COLLISION_DILATION = 4
TPC226_L4_RESONANCE_CLASSIFICATION = PROVED_EXACT
TPC226_Q25_RESONANCE = PROVED_EXACT
TPC226_ALIGNED_AP_SAVING = REFUTED_SCOPED
TPC226_AFFINE_AP_SAVING = REFUTED_SCOPED
TPC226_BALANCED_SIGN_AP_SAVING = PROVED_EXACT_FINITE_PROFILE
TPC226_BALANCED_SIGN_POLARIZED_CANCELLATION = PROVED_EXACT_FINITE_PROFILE
TPC226_UNIFORM_PROFILE_INDEPENDENT_SAVING = REFUTED_SCOPED
TPC226_V46_PROFILE_TRANSFER = OPEN
TPC226_ARITHMETIC_CANCELLATION = NONE
TPC226_ARITHMETIC_ADVANCE = NO
TPC226_FIXED_ATOM_CREDIT = 0
TPC226_L2 = NONE
TPC226_FULL_GATE_B = OPEN
TPC226_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC226_STATUS = PROVED_STRUCTURAL_L1
TPC226_ROUND2_CLUE = SOURCE_LOCK_THE_SIGN_OF_THE_3_7_RESONANCE_BEFORE_ANY_UNIFORM_AP_SAVING
```

## Exact witness energies

At `Q=25`, exact rational arithmetic gives

```text
aligned:       E_AP/E_diag = 15/13
affine:        E_AP/E_diag = 14610396266802411880605/12679409642889136447511
balanced_sign: E_AP/E_diag = 11/13
balanced_sign: E_pol = E_all = 0
```

The balanced sign profile is the finite restriction of a smooth compactly supported odd
plateau that equals `sign(t)` on every sampled nonzero argument.  It is a structural
fixture, not a claim that the physical packets have these signs.

## Reproduce

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/nonprimitive_adversary.py
```

The bridge proof/checker are:

```text
research/tpc-big-road/bridge_b_first_primitive_collision_transition.md
research/tpc-big-road/tpc_bridge_b_first_primitive_collision_transition_checker.py
```

## Layout

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/paper.pdf
code/primitive_collision_transition.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/nonprimitive_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
