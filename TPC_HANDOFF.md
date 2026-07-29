# TPC HANDOFF

更新时间：2026-07-29
当前仓库事实终点：TPC-203 / MVP10，加不编号 `CERTIFICATE_HARDENING_V2`
当前数学裁决：`NOT_TESTABLE`
下一篇：`null`
TPC-204 授权：`false`

本文件、仓库内已提交的论文和当前 active payload/audit/schema/verifier
是下一会话的事实来源。旧聊天记录不是事实来源。

## 1. 启动与验证协议

```powershell
Set-Location "D:\26-aimath\理论研究3\prime_dynamics_theory"
git status --short --branch
git pull --rebase origin main
Get-Content -Raw -Encoding UTF8 TPC_HANDOFF.md
python papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_certificate_hardening.py --check
```

随后优先读取：

1. `papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_certificate_hardening.py`
2. `papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_certificate_hardening_manifest.json`
3. `papers/tpc-203-mvp10-direct-pointwise-route-decision/experiments/tpc203_mvp10_direct_pointwise_route_decision.json`
4. `papers/tpc-203-mvp10-direct-pointwise-route-decision/experiments/tpc203_mvp10_direct_pointwise_route_decision_audit.json`
5. `papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_maximal_source_backed_direct_prefix.json`
6. `papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/experiments/tpc193_literal_fixed_atom_candidate_mechanism_gate.json`

不得因打开新会话、用户说“继续”，或证书检查通过而自动创建 TPC-204。
证书通过只说明当前负向边界被可靠冻结，不解除数学门槛。

## 2. 发布锚点

TPC-194--203 论文提交：

```text
460950090855a49a86e93231902a9674879d6f34
```

不编号证书加固提交：

```text
2e7a38652baff130cdfcbcf83ba05d3ee78a4dcc
```

TPC-203 稳定 PDF 未改变：

```text
papers/tpc-203-mvp10-direct-pointwise-route-decision/tpc-203-mvp10-direct-pointwise-route-decision.pdf
sha256 = 23bc8f5e4a1ee9c51628154c2986defb9109f7c95c63539441d6b31cd92e0992
```

Active schema：

```text
TPC-194 payload/audit = v2
TPC-203 payload/audit = v2
TPC-195--202 payload/audit = v1
TPC-194/TPC-203 superseded v1 schema files = removed
```

批量与独立复核入口：

```powershell
python papers/tpc-194-maximal-source-backed-direct-prefix/experiments/build_tpc194_203.py --check
python papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_certificate_hardening.py --check
```

## 3. 三层第一缺口与全局状态

三个第一缺口必须彼此区分：

```text
GlobalFirstMissing
  = H1.source_backed_local_occurrence_edge_family

SelectedPointwiseFirstMissing
  = LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION

DirectProductionFirstMissing
  = SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK
```

状态保持：

```text
bad_endpoint_O161_parent = OPEN
direct_twist_O161_parent = OPEN
global_architecture = OPEN
fixed_atom_decay_obtained = false
named_atom_endpoint_credit = 0
strict_1/400 = UNPAID
L2_result = NONE
next_route = SEARCH_FOR_NAMED_PACKET_CROSSWALK_OR_GENUINE_FIXED_ATOM_THEOREM
batch_stop = USER_CONFIRMATION_REQUIRED
next_paper = null
tpc204_authorized = false
```

## 4. 2026-07-29 不编号路线点审与 reopen audit

先点审了 TPC-194 direct-production crosswalk 路线：

```text
PER_PACKET_FORMULA_COMPLETE
DIRECT_PRODUCTION_CROSSWALK_NOT_TESTABLE
```

TPC-194 已完成 resolved packet 的实际公式，但没有冻结 production target。
不得把以下三类对象强行等同：

```text
CORE_TERMINAL_BLOCK
  domain = N<t(z)<=2N
  normalization = q/N

CORE_CUMULATIVE_PREFIX
  domain = 0<t(z)<=T
  normalization = q/T

PHYSICAL_PACKET_PREFIX
  domain = z in I_xi_X and z<=T
  normalization = UNNORMALIZED_INSIDE_OUTER_PACKET_SUM
```

随后五类 trigger 的裁决为：

```text
audit_kind = UNNUMBERED_REOPEN_TRIGGER_AUDIT
DIRECT = FAIL
METRIC = FAIL
BAD_ENDPOINT = FAIL
STRUCTURAL = FAIL
DECLARED_CORPUS = FAIL
new_numbered_paper = false
new_stop_cell = NONE
batch_stop = USER_CONFIRMATION_REQUIRED
next_paper = null
tpc204_authorized = false
```

精确阻断项：

- `DIRECT`：首先缺
  `SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK`；同时没有
  theorem-backed natural-`q/N` named fixed-atom positive-power theorem。
- `METRIC`：没有 source-locked named atom、exact schedule，以及该
  schedule 的 exceptional-limsup avoidance theorem。
- `BAD_ENDPOINT`：没有 literal fixed-atom local-increment
  cancellation/power-saving theorem。
- `STRUCTURAL`：没有可填入
  `H1.source_backed_local_occurrence_edge_family` 的 theorem-backed
  local-occurrence edge。
- `DECLARED_CORPUS`：在 TPC-193 七篇加既审 Menon 基线之外没有新增
  eligible primary theorem source；不形成 V2。

新增 primary-corpus 扫描覆盖 2026-01-01 至 2026-07-29 的 arXiv
`math.NT` 元数据，再对筛出的 primary theorem candidates 逐项审核。
Kim 2603.23250 是 shift-averaged ternary correlation；Verjovsky
2607.25002 的 relevant proposition 是 generic inequality，缺少
Möbius moment input；Cantarini 2607.09110 是条件化、平均化的
single-Möbius convolution。它们均不直接控制 prescribed atom 上的

```text
mu(d+s*z) mu(u+a*z),  s*u-a*d=2.
```

本节的五个 `FAIL` 只表示“截至 2026-07-29，在当前仓库与明列扫描语料
内没有满足 exact trigger contract 的正向证书”。它不是数学不可能性
定理，不是全球 source 不存在声明，也不关闭 O161 parents 或全局架构。

## 5. 不编号 `CERTIFICATE_HARDENING_V2`

本轮没有改写数学论文、TeX 或稳定 PDF；只加固机器证书与交接。

TPC-194 独立语义契约现在逐项冻结：

1. 七个 production 字段继续精确为 `MISSING`：

   ```text
   named_production_atom
   packet_schedule
   common_X_N_q_ranges
   uniform_constant_C
   positive_sigma
   target_normalization_selection
   complete_physical_loss_ledger
   ```

2. `verdict`、`first_missing`、route/claim flags、O161/global state、
   L2 和 endpoint ledger。
3. 三个 `(id, domain, normalization)` target tuples，且成对不可混同。
4. 十个 per-packet formula fields，按推导类型精确记为：

   ```text
   literal_or_signed_lift = 7
   specialized = 1
   composed = 2
   ```

   不得把 specialized/composed 字段改称 literal。
5. 十行 formula-field source ledger 和三行 formula-type source ledger。
6. 来源定位不仅检查 source hash 或 label 名，还检查：

   ```text
   unique source anchors = 22
   bounded-neighborhood formula fragments = 36
   ```

7. TPC-203 从锁定路径重新加载 TPC-194，并完整复验七项缺失、十个
   formula fields、三个 target tuples、两套 source ledgers 和全部状态。

攻击矩阵：

```text
base exact-schema mutations = 100/100 rejected
TPC-194 coordinated-regeneration semantic mutations = 35/35 rejected
TPC-203 coordinated upstream/integration mutations = 13/13 rejected
semantic total = 48/48 rejected
python -O fail-closed CLIs = 12/12
positive generator/verifier/standalone entries = 12/12
```

独立 manifest 固定 12 个 active artifacts 的 raw SHA。其信任模式是：

```text
REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE
```

它能阻止不改 verifier/manifest 的 payload+schema+audit+checker
协调重生成；它不是外部签名。若 generator、verifier 和 manifest
本身一起改变，仍必须进行 git diff/commit review，或另加 signed
commit/tag policy。不得把 manifest/hash 当作 theorem evidence。

## 6. 停止单元注册表

全部六个既有单元原样保持：

```text
TPC181_PHASE_METRIC_UNCONTROLLED_ATOMIC = STOP_SCOPED
TPC187_SIZE_ONLY_LOCAL_OSCILLATION_METHOD = STOP_SCOPED
TPC190_PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM = STOP_SCOPED
TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1 = STOP_SCOPED
FACTORWISE_SINGLE_MOBIUS_FOURIER_TO_LITERAL_PRODUCT = STOP_SCOPED
ONE_FUNCTION_PRETENTIOUSNESS_DIRECT_APPLICATION_TO_CZ = STOP_SCOPED
```

本次 audit/hardening 不新增 stop cell。不得把 Menon、Kim、Verjovsky、
Cantarini screening 注册为新停止单元，也不得重新包装旧 stopped
method cells 冒充新路线。

## 7. 精确 reopen triggers

只有以下真正新增、source-backed 且 theorem-backed 的输入才允许提出
reopen；用户授权本身不能代替数学 trigger。

### `DIRECT`

必须同时有：

1. formula-complete production target；
2. source-backed named physical atom；
3. exact packet schedule；
4. common `X/N/q` ranges；
5. uniform `C` 与 positive `sigma`；
6. fixed normalization；
7. complete physical-loss ledger；
8. theorem-backed natural-`q/N` fixed-atom positive-power mechanism；
9. 六轴全部保持。

### `METRIC`

必须同时有 source-locked named atom、exact packet schedule 和
schedule-specific exceptional-limsup avoidance theorem。phase `L2`、
Lebesgue-a.e. phase 均不通过。

### `BAD_ENDPOINT`

必须有 theorem-backed literal fixed-atom local-increment cancellation
theorem，并通过常数、范围、归一化和损失审核。

### `STRUCTURAL`

必须有 theorem-backed local-occurrence edge，直接填补：

```text
H1.source_backed_local_occurrence_edge_family
```

### `DECLARED_CORPUS`

必须有真正新增的 primary theorem source，直接控制 prescribed
determinant-two two-Möbius atom；逐项通过六轴、常数、范围、归一化和
全部损失。phase L2、a.e. phase、size-only、log-to-natural、相关平均、
积分控制、factorwise Fourier norm 或旧 stop-cell 重包装均不得计入。

`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1` 必须继续
`STOP_SCOPED`。

## 8. 验证摘要与未跟踪文件

当前 TPC-194--203 目录内的 Git-tracked active release 摘要（忽略未跟踪
或 `.gitignore` 排除的临时构建产物）：

```text
release files = 113
JSON files = 41
payloads = 10
audits = 10
active exact schemas = 20
source locks = 42
stable PDFs = 10
stable PDF pages = 21
TPC-203 stable PDF hash unchanged = true
TeX/PDF files changed by hardening = 0
hardening comparison boundary = ef4bb4b..2e7a386
```

最终正向复核：

```text
batch generator --check = PASS
independent hardening verifier --check = PASS
TPC-194--203 standalone --check = 10/10 PASS
git diff --check = PASS
```

已保留且不得暂存、修改或删除的无关未跟踪文件：

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

## 9. 下一步选择

没有新 source/corpus 或新 theorem 时，不应机械重跑同一 audit，也不得
创建 TPC-204。下一会话应停下并请求用户从以下范围作新选择：

1. 等待真正新的 theorem/source；
2. 用户指定新增 primary source 或明确定义扩展 corpus，再做不编号审核；
3. 用户另行明确限定一个有限的 TPC-204 目标并授权；但该授权不得被写成
   direct/metric/bad-endpoint/structural 数学 trigger 已通过。

## 10. 下一会话可直接粘贴

```text
进入仓库：
D:\26-aimath\理论研究3\prime_dynamics_theory

读取仓库根目录 TPC_HANDOFF.md，以仓库文件而不是旧聊天记录为事实来源。
先执行：

git status --short --branch
git pull --rebase origin main
python papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_certificate_hardening.py --check

当前事实终点仍是 TPC-203 / MVP10；不编号 REOPEN_TRIGGER_AUDIT 已完成，
DIRECT、METRIC、BAD_ENDPOINT、STRUCTURAL、DECLARED_CORPUS 五类 trigger
均未触发。CERTIFICATE_HARDENING_V2 只冻结当前负向边界，不提供新的数学
credit，也不授权 TPC-204。

保持三个 first-missing 彼此区分；保持两个 O161 pointwise parents 和
global architecture 为 OPEN；保持 fixed-atom credit=0、strict 1/400
UNPAID、L2=NONE；保持六个 STOP_SCOPED 单元原样。

若没有真正新增的 source/corpus/theorem，停止并请求我选择：
(1) 等待新 theorem/source；
(2) 审核我指定的新 source/corpus；
(3) 由我另行限定并授权一个有限的 TPC-204 目标。
授权本身不得替代任何数学 trigger。

主会话只保留结论、路线选择、阻断项和最终审核摘要。长文献扫描、定理
原文核查、schema exploit review、构建日志和逐页 PDF 检查交给分身；
所有正式写入由主会话协调。
```
