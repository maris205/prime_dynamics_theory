# TPC HANDOFF

更新时间：2026-07-30
当前仓库事实终点：TPC-204
当前数学裁决：`FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE`
下一篇：`null`
TPC-204 授权并完成：`true`
TPC-205 授权：`false`

本文件、仓库内已提交的论文，以及 active payload/audit/schema/checker
是下一会话的事实来源。旧聊天记录不是事实来源。

## 1. 启动与验证协议

```powershell
Set-Location "D:\26-aimath\理论研究3\prime_dynamics_theory"
git status --short --branch
git pull --rebase origin main
Get-Content -Raw -Encoding UTF8 TPC_HANDOFF.md

$d = "papers/tpc-204-source-locked-production-registry-crosswalk/experiments"
python "$d/build_tpc204.py" --check
python "$d/tpc204_source_locked_production_registry_crosswalk.py" --check
python "$d/tpc204_independent_checker.py" --check
python papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_certificate_hardening.py --check
```

随后优先读取：

1. `papers/tpc-204-source-locked-production-registry-crosswalk/README.md`
2. `papers/tpc-204-source-locked-production-registry-crosswalk/experiments/tpc204_source_locked_production_registry_crosswalk.json`
3. `papers/tpc-204-source-locked-production-registry-crosswalk/experiments/tpc204_source_locked_production_registry_crosswalk_audit.json`
4. `papers/tpc-204-source-locked-production-registry-crosswalk/experiments/tpc204_independent_checker.py`
5. `papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_maximal_source_backed_direct_prefix.json`
6. `papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/experiments/tpc193_literal_fixed_atom_candidate_mechanism_gate.json`

不得因打开新会话、用户说“继续”、TPC-204 checker 通过，或 TPC-204
已经编号而自动创建 TPC-205。证书通过只说明当前有限负向边界被可靠冻结，
不解除数学门槛。

## 2. 发布锚点

TPC-194--203 论文提交：

```text
460950090855a49a86e93231902a9674879d6f34
```

TPC-194/203 不编号证书加固提交：

```text
2e7a38652baff130cdfcbcf83ba05d3ee78a4dcc
```

TPC-204 论文提交：

```text
2226193cf726f96c7dbca3e9a1321ed6862f6a4c
```

TPC-204 稳定 PDF：

```text
papers/tpc-204-source-locked-production-registry-crosswalk/tpc-204-source-locked-production-registry-crosswalk.pdf
sha256 = 85d4dcd8436e5b049933584d68407924019c1d82b6b9c85122d84c3e101290f9
pages = 4
page size = A4
```

TPC-204 active release：

```text
release files = 14
manifest-pinned artifacts = 11
payload/audit exact schemas = 2
source locks = 15
```

## 3. TPC-204 的精确有限结论

授权范围仅为：

```text
FINITE_EXACT_MATCHING_OR_FIRST_MISMATCH_CROSSWALK_AUDIT
```

授权是 workflow input，不是 theorem evidence，不让任何 reopen trigger
自动通过。

TPC-204 对 direct-production lineage 中九个互异 plausible objects 作了
固定、source-locked 的有限审核：

1. `H9.phase_cell_registry`：TPC-180 的空 registry slot；
2. `TT26.RATIONAL_PERIODIC_ATOM`：`q/N` terminal-block log-saving theorem；
3. `A159.DYADIC_SHADOW_ALMOST_ENDPOINT_PREFIX`：shadow 外 `q/T` cumulative prefix；
4. `A167.DIRECT_ADDITIVE_TWIST_PHASE_L2`：terminal-block phase `L2` theorem；
5. `TPC183.N_EQUALS_T_SPECIALIZATION_PROPOSAL`：无效的 terminal-to-cumulative proposal；
6. `O161.BAD_ENDPOINT_POINTWISE_FIXED_ATOM_CONTRACT`：TPC-184 verbal `q/T` all-prefix target；
7. `O161.DIRECT_ADDITIVE_TWIST_FIXED_ATOM_CONTRACT`：TPC-189 verbal `q/N` direct target；
8. `TW25.LOG_TWISTED_AFFINE`：log-weighted fixed-atom affine theorem；
9. `PHYSICAL_PACKET_PREFIX`：TPC-194 resolved unnormalized per-packet prefix。

TPC-184 contract 与 TPC-159 shadow-excluding theorem 是不同对象；前者不能
被后者静默代表。这一行是在独立 claim review 中发现并补入，最终不存在
漏计。

四个显式排除对象：

```text
TPC167.prop:grid
TPC167.cor:measure
TPC159.cor:interval
TPC203.tpc194_import_contract
```

它们分别是 auxiliary grid、Lebesgue phase measure、无单一 target
normalization 的 interval difference，以及重复 upstream import，不是
新的 production-crosswalk object。

最终有限计数：

```text
declared candidates = 9
production axes per candidate = 7
production-axis cells = 63
formula types per candidate = 3
formula-crosswalk cells = 27
complete crosswalks = 0
first common mismatch = NAMED_PRODUCTION_ATOM
direct trigger = FAIL
mathematical reopen = false
```

精确 theorem status：

```text
PROVED_LOCKED_REGISTRY_FIRST_MISMATCH_NO_COMPLETE_CROSSWALK_L1
```

精确 verdict：

```text
FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE
```

这是 L0/L1 的 finite-corpus first-mismatch theorem。它不是 fixed-atom
cancellation theorem，不是 production registry 的全球不存在性定理，
不关闭 direct route、任一 O161 parent 或全局架构，也没有 L2 gain。

## 4. 三个不可混同的公式对象

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

令 `N=T` 只把第一行变成 `T<t(z)<=2T`，不会产生
`0<t(z)<=T`。第三行处于 outer physical packet sum 内且本身未归一化。
不得通过改名、解释性改写，或把 block/cumulative/physical 对象强行
等同来补字段。

完整 production record 仍须在同一 source-locked 对象上同时冻结：

```text
named_production_atom
packet_schedule
common_X_N_q_ranges
uniform_constant_C
positive_sigma
target_normalization_selection
complete_physical_loss_ledger
```

当前共同首缺为 `named_production_atom`；`packet_schedule`、
target normalization selection 与其余字段仍有独立缺口。

## 5. 三层第一缺口与开放状态

三个 first-missing 必须彼此区分：

```text
GlobalFirstMissing
  = H1.source_backed_local_occurrence_edge_family

SelectedPointwiseFirstMissing
  = LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION

DirectProductionFirstMissing
  = SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK

DirectCrosswalkSubgate
  = NAMED_PRODUCTION_ATOM
```

状态保持：

```text
bad_endpoint_O161_parent = OPEN
direct_twist_O161_parent = OPEN
global_architecture = OPEN
fixed_atom_decay_obtained = false
literal_fixed_atom_cancellation_obtained = false
named_atom_endpoint_credit = 0
strict_1/400 = UNPAID
program_positive_L2 = false
L2_result = NONE
batch_stop = USER_CONFIRMATION_REQUIRED
next_paper = null
tpc205_authorized = false
```

下一条 direct-production 输入应是：

```text
SOURCE_LOCKED_NAMED_PRODUCTION_ATOM_RECORD
```

并仍须附 exact packet schedule、共同 ranges、uniform `C`、positive
`sigma`、literal normalization、完整 physical-loss ledger，及真正的
fixed-atom theorem。只有 atom 名称或 symbolic `alpha_xi_X` 不够。

## 6. STOP_SCOPED 注册表

既有六个 scoped stop 保持：

```text
TPC181_PHASE_METRIC_UNCONTROLLED_ATOMIC = STOP_SCOPED
TPC187_SIZE_ONLY_LOCAL_OSCILLATION_METHOD = STOP_SCOPED
TPC190_PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM = STOP_SCOPED
TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1 = STOP_SCOPED
FACTORWISE_SINGLE_MOBIUS_FOURIER_TO_LITERAL_PRODUCT = STOP_SCOPED
ONE_FUNCTION_PRETENTIOUSNESS_DIRECT_APPLICATION_TO_CZ = STOP_SCOPED
```

TPC-204 新增且仅新增：

```text
TPC204_DECLARED_PLAUSIBLE_PRODUCTION_CROSSWALK_CORPUS_V1 = STOP_SCOPED
```

它只停止从这九个明确对象中提取完整 crosswalk。不得提升为更大 source
universe 的停止声明。

`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1` 必须继续
`STOP_SCOPED`；不得把 phase `L2`、Lebesgue-a.e.、size-only、
log-to-natural，或旧 method cells 的重包装记作新 theorem。

## 7. Reopen triggers

TPC-204 没有让既有五类 trigger 通过：

```text
DIRECT = FAIL
METRIC = FAIL
BAD_ENDPOINT = FAIL
STRUCTURAL = FAIL
DECLARED_CORPUS = FAIL
```

只有真正新增的 theorem-backed 输入才允许提出 reopen：

- `DIRECT`：同一 source-locked production record 上七字段完整，且有
  natural-`q/N` named fixed-atom positive-power theorem；
- `METRIC`：source-locked named atom + exact packet schedule +
  schedule-specific exceptional-limsup avoidance theorem；
- `BAD_ENDPOINT`：literal fixed-atom local-increment cancellation theorem，
  并通过常数、范围、归一化和损失；
- `STRUCTURAL`：直接填补
  `H1.source_backed_local_occurrence_edge_family` 的 theorem-backed
  local-occurrence edge；
- `DECLARED_CORPUS`：真正新增的 primary theorem source，直接控制
  prescribed determinant-two two-Möbius atom
  `mu(d+s*z)mu(u+a*z), s*u-a*d=2`，并通过六轴、常数、范围、归一化
  和完整损失。

用户授权本身不能替代任一数学 trigger。

## 8. 机器证书与信任边界

TPC-204 有两个分离角色：

```text
tpc204_source_locked_production_registry_crosswalk.py
  = authoritative materializer / primary contract

tpc204_independent_checker.py
  = independent read-only verifier
```

独立 checker 不 import builder、materializer 或 `build_payload`；只 import
Python 标准库。它独立冻结九个 candidate IDs、row digests、source
selectors、mutation 名单和 artifact hashes，防止 producer 的
common-mode 自证。

最终攻击矩阵：

```text
base exact-schema mutations = 12/12 rejected
coordinated regenerated-schema semantic mutations = 45/45 rejected
nested bool/int type-confusion mutations = 5/5 rejected
duplicate JSON keys = rejected
NaN/nonfinite JSON = rejected
python -O fail-closed CLIs = 3/3
source hashes = 15/15 verified
manifest hashes = 11/11 verified
exact schemas = 2/2 verified
```

独立 exploit review 还确认拒绝：

```text
producer-side candidate omission/replacement
mutation-name collapse while preserving advertised counts
source content + source-lock coordinated rebinding
```

manifest 的信任模式：

```text
REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE
```

它是 repository review pin，不是外部签名或 theorem evidence。若代码与
manifest 一起改变，仍必须做普通 git diff/commit review。

## 9. PDF 与最终验证

稳定 PDF：

```text
pages = 4
page size = A4
overfull boxes = 0
undefined references/citations = 0
embedded/subset fonts = 19/19
visual page inspection = 4/4 PASS
```

最终正向复核：

```text
TPC-204 builder --check = PASS
TPC-204 materialization contract --check = PASS
TPC-204 independent checker --check = PASS
TPC-194--203 batch builder --check = PASS
TPC-194 hardening --check = PASS
TPC-203 standalone --check = PASS
git diff --check = PASS
independent mathematical claim review = PASS
independent machine exploit review = PASS
```

保留且不得暂存、修改或删除的无关未跟踪文件：

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

## 10. 下一步选择

本轮必须停在 `USER_CONFIRMATION_REQUIRED`。TPC-205 未授权。

下一会话只允许用户选择：

1. 提供 source-locked named production atom record 与 exact packet
   schedule，审核 direct-production crosswalk；
2. 指定真正新增的 primary theorem source/corpus，先做不编号审核；
3. 提供 theorem-backed fixed-atom local-increment theorem 或
   local-occurrence edge，审核对应 reopen；
4. 等待新的 theorem/source。

没有新 source/corpus/theorem 时，不应机械重复 TPC-204 census，也不得
创建 TPC-205。

## 11. 下一会话可直接粘贴

```text
进入仓库：
D:\26-aimath\理论研究3\prime_dynamics_theory

读取仓库根目录 TPC_HANDOFF.md，以仓库文件而不是旧聊天记录为事实来源。
先执行：

git status --short --branch
git pull --rebase origin main

$d = "papers/tpc-204-source-locked-production-registry-crosswalk/experiments"
python "$d/build_tpc204.py" --check
python "$d/tpc204_source_locked_production_registry_crosswalk.py" --check
python "$d/tpc204_independent_checker.py" --check

当前事实终点是 TPC-204。它只证明明列九对象、63 个 production-axis
cells 和 27 个 formula-crosswalk cells 中不存在完整 crosswalk；共同首缺
是 NAMED_PRODUCTION_ATOM，精确 verdict 为
FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE。

保持 CORE_TERMINAL_BLOCK、CORE_CUMULATIVE_PREFIX 与
PHYSICAL_PACKET_PREFIX 不可混同；保持 TPC193 V1 与 TPC204 V1 两个
corpus cells 为 STOP_SCOPED；保持两个 O161 parents 和 global
architecture OPEN；保持 fixed-atom credit=0、strict 1/400 UNPAID、
L2=NONE。

TPC-205 未授权。停止并请求我从以下范围选择：
(1) source-locked named atom + exact packet schedule；
(2) 新 primary theorem source/corpus；
(3) theorem-backed fixed-atom local increment 或 local-occurrence edge；
(4) 等待新 theorem/source。

授权本身不得替代数学 trigger。主会话只保留结论、路线选择、阻断项和
最终审核摘要；长扫描、定理核查、schema exploit review、构建日志和逐页
PDF 检查交给分身；所有正式写入由主会话协调。
```
