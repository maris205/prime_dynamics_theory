# TPC HANDOFF

更新时间：2026-07-29
当前仓库事实终点：TPC-203 / MVP10
当前裁决：`NOT_TESTABLE`
下一篇：`null`
TPC-204 授权：`false`

本文件和仓库内已提交的论文、payload、audit、schema 是下一会话的事实来源。旧聊天记录不是事实来源。

## 1. 启动协议

```powershell
Set-Location "D:\26-aimath\理论研究3\prime_dynamics_theory"
git status --short --branch
git pull --rebase origin main
Get-Content -Raw TPC_HANDOFF.md
```

随后优先读取：

1. `papers/tpc-203-mvp10-direct-pointwise-route-decision/README.md`
2. `papers/tpc-203-mvp10-direct-pointwise-route-decision/experiments/tpc203_mvp10_direct_pointwise_route_decision.json`
3. `papers/tpc-203-mvp10-direct-pointwise-route-decision/experiments/tpc203_mvp10_direct_pointwise_route_decision_audit.json`
4. `papers/tpc-194-maximal-source-backed-direct-prefix/README.md`
5. `papers/tpc-202-new-primary-double-selector-gate/README.md`

不得因打开新会话而自动创建 TPC-204。先做不编号的 `REOPEN_TRIGGER_AUDIT`；触发器没有通过时，停下并请求用户选择。

## 2. 本轮发布锚点

TPC-194--203 论文提交：

```text
460950090855a49a86e93231902a9674879d6f34
```

TPC-203 稳定 PDF：

```text
papers/tpc-203-mvp10-direct-pointwise-route-decision/tpc-203-mvp10-direct-pointwise-route-decision.pdf
sha256 = 23bc8f5e4a1ee9c51628154c2986defb9109f7c95c63539441d6b31cd92e0992
```

批量生成与复核入口：

```powershell
python papers/tpc-194-maximal-source-backed-direct-prefix/experiments/build_tpc194_203.py --check
```

## 3. 当前三层第一缺口

必须同时保留以下三个彼此不同的第一缺口，不得互相改写或吞并：

```text
GlobalFirstMissing
  = H1.source_backed_local_occurrence_edge_family

SelectedPointwiseFirstMissing
  = LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION

DirectProductionFirstMissing
  = SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK
```

对应状态：

```text
bad_endpoint_O161_parent = OPEN
direct_twist_O161_parent = OPEN
global_architecture = OPEN
fixed_atom_decay_obtained = false
named_atom_endpoint_credit = 0
strict_1/400 = UNPAID
L2_result = NONE
```

## 4. TPC-194--203 结论

### TPC-194 — maximal source-backed direct prefix

裁决：`FORMULA_COMPLETE_PER_PACKET_L1`。

已从 TPC-159、167、183、184、189、193 的实际公式逐字锁定：

```text
xi = (theta,c,kappa,r)
b = c*kappa
B_xi = B_{theta,b}
Omega_xi = ell_theta*v_theta*sigma_theta*B_{theta,b}
alpha_xi,X = epsilon_theta*r_tilde*Omega_xi/(c*q_X)
```

并锁定 exact physical coefficient、带符号的 `r_tilde`、decorated inner prefix、complete contribution，以及外层乘子 `mathfrak m_{K,X}(r)`。

这只完成每包公式，不完成 production target。仍缺：

- source-locked named physical atom；
- exact packet schedule；
- common `X/N/q` ranges；
- uniform constant `C`；
- positive `sigma`；
- normalization choice；
- complete physical-loss ledger。

不得通过解释性改写，或把 block/cumulative 对象强行等同，来补这些字段。

### TPC-195 — block/prefix power-profile transfer

裁决：`PROVED_BIDIRECTIONAL_POWER_PROFILE_TRANSFER`。

对 `0 < sigma < 1`：

```text
block -> prefix constant = 1/(2^(1-sigma)-1)
prefix -> block constant = 2^(1-sigma)+1
```

实数端点采用精确 telescoping。截断 raw tail 为严格 `< 2BM`；归一化安全项为 `2qBM/T`。

### TPC-196 — residue split and determinant ledger

裁决：`PROVED_RESIDUE_SPLIT_WITH_DETERMINANT_2R`。

锁定：

- slope gcd 正好是 `R`，不是 affine content；
- residue split 后 determinant 为 `2R`；
- 一个非零 DFT mode 不等于所有 residue sums 均非零；
- 依赖 TPC-94 与 TPC-108。

### TPC-197 — prime-conductor consistency

固定非零有理 atom 不可能沿无界、互异 prime conductors 重复出现。

conductor-one 路线仍开放，但它仍必须同时提供：

- `q_prog` 的 polylog 范围；
- exceptional set 外的 `N` 范围；
- 全部 good-scale 条件；
- named occurrence；
- exact packet schedule。

### TPC-198 — factorwise Fourier barrier

裁决：`STOP_SCOPED`。

禁止从两个 single-Mobius Fourier black boxes 推出 prescribed atom 上的 literal product bound。Rudin--Shapiro witness 固定了该逻辑缺口。

新停止单元：

```text
FACTORWISE_SINGLE_MOBIUS_FOURIER_TO_LITERAL_PRODUCT = STOP_SCOPED
```

### TPC-199 — pretentiousness firewall

裁决：`STOP_SCOPED`。

禁止把 one-function multiplicative pretentiousness theorem 直接应用到
`mu(n)mu(n+2)`；该乘积不是一个 multiplicative function。

新停止单元：

```text
ONE_FUNCTION_PRETENTIOUSNESS_DIRECT_APPLICATION_TO_CZ = STOP_SCOPED
```

### TPC-200 — four-form determinant refinement

完成四个 affine forms 的 determinant table。

在 positive-slope 约束下，唯一 positive-shift degeneration 是：

```text
q = 1
h = 2
```

并显式继承 TPC-130。

### TPC-201 — degenerate-shift Fejér absorption

对 `V > 0`、`3 <= H <= N` 完成 positive-part split。

degenerate diagonal 的精确系数为：

```text
2 + 4 = 6
```

该部分可吸收；剩余对象是 nondegenerate four-Mobius off-diagonal。来源锁定 TPC-130 与 TPC-200。

### TPC-202 — new-primary double-selector gate

裁决：`SCREENED_NON_DIRECT_ZERO_ELIGIBLE`。

Menon 2026 的 Theorem 1.4/1.5 已按原生 ranges、normalizations、`k` factor 与 logarithmic losses 审核。它们不直接作用于 prescribed atom 上的 literal determinant-two two-Möbius coefficient

```text
mu(d+s*z) mu(u+a*z),  s*u-a*d=2
```

因此 eligible source 数为零。TPC-181 selector lemma 只作为继承的说明，不产生新 stop cell。

外部来源完整性状态是 manual transcription；没有伪造 external hash。

### TPC-203 — MVP10 route decision

裁决：`NOT_TESTABLE`。

```text
next_route
  = SEARCH_FOR_NAMED_PACKET_CROSSWALK_OR_GENUINE_FIXED_ATOM_THEOREM

batch_stop = USER_CONFIRMATION_REQUIRED
next_paper = null
tpc204_authorized = false
```

每包 direct formula 已完成；production crosswalk 与 named-atom positive-power theorem 仍不存在。两条 O161 pointwise parents 和全局架构均保持开放。

## 5. 停止单元注册表

继承的旧停止单元：

```text
TPC181_PHASE_METRIC_UNCONTROLLED_ATOMIC = STOP_SCOPED
TPC187_SIZE_ONLY_LOCAL_OSCILLATION_METHOD = STOP_SCOPED
TPC190_PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM = STOP_SCOPED
TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1 = STOP_SCOPED
```

本轮新增且仅新增：

```text
FACTORWISE_SINGLE_MOBIUS_FOURIER_TO_LITERAL_PRODUCT = STOP_SCOPED
ONE_FUNCTION_PRETENTIOUSNESS_DIRECT_APPLICATION_TO_CZ = STOP_SCOPED
```

不得把 TPC-202 的 Menon screening 或继承的 selector illustration 注册成新停止单元。不得重新包装上述停止单元来冒充新路线。

## 6. 五类精确 reopen triggers

下一轮不编号审计必须逐项检查以下五类触发器。

### `DIRECT`

同时出现：

1. formula-complete production target；
2. source-backed named physical atom；
3. exact packet schedule；
4. common `X/N/q` ranges；
5. uniform `C` 与 positive `sigma`；
6. fixed normalization；
7. complete physical-loss ledger；
8. theorem-backed natural-`q/N` fixed-atom positive-power mechanism；
9. 六轴全部保持。

缺一项即不通过。不得用 block/cumulative 对象替代 literal prefix target。

### `METRIC`

同时出现：

1. source-locked named atom；
2. exact packet schedule；
3. schedule-specific exceptional-limsup avoidance theorem。

phase `L2`、Lebesgue-a.e. phase 或未锁定 schedule 的 metric statement 均不通过。

### `BAD_ENDPOINT`

出现 theorem-backed literal fixed-atom local-increment cancellation theorem，并逐项通过常数、范围、归一化和损失审计。

### `STRUCTURAL`

出现 theorem-backed local-occurrence edge，能够直接填补：

```text
H1.source_backed_local_occurrence_edge_family
```

### `DECLARED_CORPUS`

在 TPC-193 已审核的七篇 primary sources 之外，出现真正新增的 primary theorem source，且定理直接控制 prescribed atom 上的 literal coefficient

```text
mu(d+s*z) mu(u+a*z),  s*u-a*d=2.
```

必须逐项审核六轴、常数、范围、归一化和全部损失。以下均不得计入：

- phase `L2`；
- Lebesgue-a.e. phase；
- size-only；
- log-to-natural 偷渡；
- 三个旧 stopped method cells 的重新包装；
- 只控制相关平均、积分、几乎处处集合或因子级 Fourier norm 的结果。

`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1` 必须继续保持 `STOP_SCOPED`。

## 7. 审核摘要

Release allowlist：

```text
papers = 10
release files = 111
unexpected release files = 0
missing release files = 0
```

Schema 与 payload：

```text
JSON files = 40
payloads = 10
audits = 10
exact recursive schemas = 20
schema objects = 313
schema arrays = 57
const leaves = 1237
source locks = 40
built-in mutations rejected = 100/100
```

每个 standalone checker 在 `--check` 下：

- 加载并执行 payload schema 与 audit schema；
- 核对 payload、audit、两份 schema 的四重 SHA；
- 要求 canonical byte equality；
- 重新计算 `finite(payload)`；
- 要求它与 `audit["finite_check_result"]` 精确相等。

专项攻击复核：

```text
audit top-level extra rejected = 10/10
deleted finite result rejected = 10/10
forged finite result rejected = 10/10
payload-schema extra rejected = 10/10
deep rebind/schema rebuild attacks = rejected
python -O fail-closed CLIs = 11/11
```

PDF：

```text
stable PDFs = 10
pages = 21
page size = A4
embedded-font rows = 140/140
overfull warnings = 0
undefined-reference warnings = 0
all pages rendered and visually inspected = true
```

信任边界：

- batch generator 是共同 trust root；
- generator 与生成物被协调修改并重建时，必须做 git diff/commit review；
- canonical duplicate/format rejection 由 `--check` 路径强制；
- 集成审核必须运行 batch `--check`，不能只运行 TPC-203 standalone checker。

## 8. Claim firewall

本批次只形成 L0/L1 结构与否定性门槛结果。它没有证明：

- prescribed physical atom 的 positive-power decay；
- source-backed fixed-atom local occurrence；
- endpoint credit；
- prime-pair lower bound；
- twin-prime theorem；
- 任意 program-positive L2 结论。

`FORMULA_COMPLETE_PER_PACKET_L1` 不等于 production target complete。
`SCREENED_NON_DIRECT_ZERO_ELIGIBLE` 不等于 exhaustive impossibility theorem。
`STOP_SCOPED` 只停止被点名的方法单元，不关闭 O161 parents 或全局架构。

## 9. 已保留的无关未跟踪文件

本批次没有暂存、修改或删除：

```text
papers/tpc-105-provenance-preserving-affine-map-quotient/experiments/__pycache__/
papers/tpc-63-canonical-cofactor-provenance/main.aux
papers/tpc-63-canonical-cofactor-provenance/main.bbl
papers/tpc-63-canonical-cofactor-provenance/main.blg
papers/tpc-63-canonical-cofactor-provenance/main.log
papers/tpc-63-canonical-cofactor-provenance/main.out
papers/tpc-63-canonical-cofactor-provenance/main.pdf
tmp/
```

它们不属于 TPC-194--203 release。

## 10. 下一会话可直接粘贴

```text
进入仓库：
D:\26-aimath\理论研究3\prime_dynamics_theory

读取仓库根目录 TPC_HANDOFF.md，以仓库文件而不是旧聊天记录为事实来源。先执行：

git status --short --branch
git pull --rebase origin main

从 TPC-203 的 USER_CONFIRMATION_REQUIRED 停止点开始，但这不解除任何数学门槛，也不自动授权创建 TPC-204。

先执行一个不编号的 REOPEN_TRIGGER_AUDIT，逐项审核 TPC_HANDOFF.md 中的五类精确触发器：
DIRECT、METRIC、BAD_ENDPOINT、STRUCTURAL、DECLARED_CORPUS。

保持 TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1 为 STOP_SCOPED；保持两个 O161 pointwise parents 和全局架构开放；不得把 phase L2、Lebesgue-a.e. phase、size-only、log-to-natural 或旧 stopped method cells 的重包装当作新路线。

只有某个触发器 source-backed、theorem-backed 且逐项通过六轴、常数、范围、归一化和完整损失审核时，才提出对应 reopen route。完成审计后停止，并向我请求下一步选择；没有我的新确认，不得创建 TPC-204。

主会话只保留结论、路线选择、阻断项和最终审核摘要。长文献扫描、定理原文核查、schema exploit review、构建日志及逐页 PDF 检查交给分身，只返回紧凑摘要；所有正式写入由主会话协调。
```
