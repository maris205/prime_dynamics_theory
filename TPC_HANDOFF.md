# TPC HANDOFF

更新时间：2026-08-01
交接状态：`SEALED_FOR_NEW_SESSION`
本轮启动及正式写入前上游同步基线：
`3d191298f45ee9a00768c4fdcb571550102703ac`。该基线已包含第 32 节
RH-340/341 cross-program audit及其 handoff closure；本轮写前 fetch/pull没有
取得新的 remote delta。O161 pointwise current-primary theorem refresh见第 33 节，
最终发布同步与三方 hash核验见第 33.6 节。
第 23 节 TPC source-lock 快照锚定更早基线
`28cafdd5fa96ff948f1520e778c7a2ba65208730`；晚到 RH-330/332 的既有
physical-object type checks、RH-333/334/335 的第 29.6 节 type checks，以及
RH-336/337 的第 30.5 节 type checks、RH-338/339 的第 31.5 节 type checks，
以及 RH-340/341 的第 32.7--32.8 节 type checks，均未改变本轮算术裁决。
当前仓库事实终点：TPC-206
当前编号论文裁决：`SELECTED_SOURCE_LOCKED_13_OF_42_PAIR_REGISTRY_PROJECTION_CERTIFIED_NOT_REOPENED`
最新不编号审计裁决：
`TPC_O161_DIRECT_BAD_ENDPOINT_CURRENT_PRIMARY_ONE_SIGN_OR_AVERAGED_WRONG_OBJECT_NO_FIXED_POWER_TRIGGER_STOP_SCOPED_PARENTS_OPEN`
下一篇：`null`；下一项不编号审计：`null`（仅在第 32.6 节或
第 33.5 节列出的 source-backed reopen trigger，或其他既有独立 trigger
真实出现时重开）
TPC-204 授权并完成：`true`
TPC-205 授权并完成：`true`
TPC-206 授权并完成：`true`
后续同类有限审计与编号工作流授权：`true`
自动通过数学门槛或自动编号：`false`
TPC-207 数学 trigger：`false`；TPC-207 已创建：`false`
下一篇编号论文发布前完整 provenance cascade：`REQUIRED`

上下文节省入口：新会话优先读取本页页首及第 1、6、22、24、29、30、31、32、33 节；
第 23、27、28 节只在第 29--33 节明确引用时展开。第 22 节的 `TRUNCATED_ENTRY_ABSENT`
仍只指 `delta=1/20` exact family；第 23 节审核的是另一条 theorem-valid
high-beta selected packet。两条 source lock 不得拼接。

本文件、仓库内已提交的论文，以及 active payload/audit/schema/checker
是下一会话的事实来源。旧聊天记录不是事实来源。
下文历史审计块中的所有 `tpc205_authorized=false`、`TPC-206 未授权` 与
`USER_CONFIRMATION_REQUIRED` 都是当时的编号前快照，统一由本页页首及
第 14--23 节覆盖；其数学 gate 与 `STOP_SCOPED` 内容仍保留。用户已允许
后续按同一有限、fail-closed 工作流继续，不再设置单独的人为编号授权门；
这不替代 theorem evidence，也不许可跨过任何数学门槛。

## 1. 启动与验证协议

```powershell
Set-Location "D:\26-aimath\理论研究3\prime_dynamics_theory"
git status --short --branch
git pull --rebase origin main
Get-Content -Raw -Encoding UTF8 TPC_HANDOFF.md
$env:PYTHONDONTWRITEBYTECODE = "1"

$d = "papers/tpc-206-selected-lineage-pair-registry-projection/experiments"
python -B "$d/build_tpc206.py" --check
python -B "$d/tpc206_selected_lineage_pair_registry.py" --check
python -B "$d/tpc206_independent_checker.py" --check
$p = "papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments"
python -B "$p/build_tpc205.py" --check
python -B "$p/tpc205_pair_native_registry_interface.py" --check
python -B "$p/tpc205_independent_checker.py" --check
python -B papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_certificate_hardening.py --check
python -B papers/tpc-133-executable-native-entrance/experiments/tpc133_native_entrance.py --check
python -B papers/tpc-134-boundary-complete-dyadic-prefix-tail-archive/experiments/tpc134_branch_archive.py --check
python -B papers/tpc-135-tpc17-tpc18-block-frontier/experiments/tpc135_domain_cover_audit.py --check
python -B papers/tpc-136-complete-native-cut-archive/experiments/tpc136_cut_archive.py --check
python -B papers/tpc-184-bad-endpoint-literal-target-contract/experiments/tpc184_bad_endpoint_literal_target_contract.py --check
python -O -B papers/tpc-184-bad-endpoint-literal-target-contract/experiments/tpc184_bad_endpoint_literal_target_contract.py --check
python -B papers/tpc-189-direct-twist-literal-target-contract/experiments/tpc189_direct_twist_literal_target_contract.py --check
python -O -B papers/tpc-189-direct-twist-literal-target-contract/experiments/tpc189_direct_twist_literal_target_contract.py --check

foreach ($s in @(
  "papers/tpc-173-production-source-claim-inventory/experiments/tpc173_source_claim_inventory.py",
  "papers/tpc-174-local-occurrence-edge-witness-schema/experiments/tpc174_witness_contract.py",
  "papers/tpc-175-declared-corpus-local-edge-family/experiments/tpc175_local_edge_family.py",
  "papers/tpc-176-source-backed-coverage-gluing-audit/experiments/tpc176_coverage_gluing_audit.py",
  "papers/tpc-177-actual-active-support-vacuity-firewall/experiments/tpc177_active_support_audit.py",
  "papers/tpc-178-canonical-minimal-representation-eligibility/experiments/tpc178_representation_audit.py",
  "papers/tpc-179-h1-structural-corpus-exhaustion-integration/experiments/tpc179_h1_integration.py"
)) {
  python -O -B $s --check
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
```

以上是当前完整的 22 项只读启动回归；任一命令非零即 fail closed，不继续
数学升级或正式写入。`git status` 中既有 tracked/untracked 工作属于用户；不得
`reset`、`checkout`、`clean`、自动 `stash`、删除或纳入本轮提交。当前已知须保留
TPC-105 的 `__pycache__/`、TPC-63 构建产物与 `tmp/`。TPC-27--32 legacy
certificates 没有只读 `--check` 且会无条件重写 JSON，在新增真正只读入口前
不得为了启动回归而执行。

随后优先读取：

1. `papers/tpc-206-selected-lineage-pair-registry-projection/README.md`
2. `papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_selected_lineage_pair_registry.json`
3. `papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_selected_lineage_pair_registry_audit.json`
4. `papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_independent_checker.py`
5. `papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments/tpc205_pair_native_registry_interface.json`
6. `papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_maximal_source_backed_direct_prefix.json`
7. `papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/experiments/tpc193_literal_fixed_atom_candidate_mechanism_gate.json`

不得因打开新会话、用户说“继续”、checker 通过或工作流已持续授权而
自动创建 TPC-207。持续授权只移除了重复的人为许可步骤；只有新的
theorem-backed edge 使定理状态发生真实变化时，才可编号。证书通过只说明
当前有限 selected-lineage 边界被可靠冻结，不解除数学门槛。

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

TPC-205 论文提交：

```text
98b3e6c462008b07538b496ed130b1004a84747f
```

TPC-205 稳定 PDF：

```text
papers/tpc-205-pair-native-post-ttstar-registry-interface/tpc-205-pair-native-post-ttstar-registry-interface.pdf
sha256 = b3596e207943132ad48e6a17cfd107421f02b521bc02f617615c860816a1dc1e
pages = 4
page size = A4
```

TPC-205 active release：

```text
release files = 16
manifest-pinned artifacts = 13
payload/audit/L0 exact schemas = 3
source locks = 17
```

TPC-206 论文提交：

```text
85d3d08221101dd125fb07cb5e1929f9d2525a5a
```

TPC-206 稳定 PDF：

```text
papers/tpc-206-selected-lineage-pair-registry-projection/tpc-206-selected-lineage-pair-registry-projection.pdf
sha256 = e6a3ee6df0492daa2aae86de47040e8b0d5f8c75a7abc91208601f945d3bb082
pages = 4
page size = A4
```

TPC-206 active release：

```text
release files = 14
manifest-pinned artifacts = 11
payload/audit exact schemas = 2
source locks = 29
```

TPC-206 的 source theorem/archive 审计快照固定于
`42507087b774d9057ba3794468a4790bf93162d5`。发布前第二次
`git pull --rebase origin main` 仅引入 RH-322 路径并把基线推进到
`b3dc7e5`；没有改动 TPC 路径。因而 29 个 source locks 继续有意针对
审计启动快照，而不是把无关的晚到提交偷换进冻结 census。

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

2026-07-30 的不编号 single-cut 审计新增且仅新增：

```text
TPC18_25_32_93_194_SINGLE_CUT_OCCURRENCE_COMPOSITE_V1 = STOP_SCOPED
```

它只停止以下推断：把 TPC-18/TPC-25 的 opened-row 重标号直接与
TPC-93 的既成 source-child inverse、TPC-194 的既成 resolved-key
公式组合，就得到原 cut coefficient 的 production local-occurrence
edge。它不停止新的 cut-to-parent theorem、pair-native repair、H1
architecture、两个 O161 parents 或任何真正新增的算术 theorem。

2026-07-30 的不编号 pair-native 审计新增且仅新增：

```text
TPC18_TPC93_POST_TTSTAR_PAIR_DIRECT_COMPOSITION_V1 = STOP_SCOPED
```

它只停止以下直接提升：把当前 TPC-18/TPC-25/TPC-32 的公式级
post-TT-star ordered row-pair 直接改名为现成的 TPC-93 retained
`omega`、生产 pair occurrence，或 H1 local-occurrence edge。它不停止
新的 pair registry、pair-to-`omega` theorem crosswalk、cut inverse
aggregation、独立 architecture reroute、两个 O161 parents，或真正新增的
算术 theorem。给定 retained `omega` 后的 source-child inverse，以及
另行给定 downstream fields 后的 content/resolved template 相容性也未被
否定。

2026-07-31 的三项不编号审计新增且仅新增：

```text
DECLARED_SELECTED_103_107_OPENED_D_ATTACHMENT_CORPUS_V1 = STOP_SCOPED
DECLARED_TPC18_25_133_134_LITERAL_PAIR_COEFFICIENT_CROSSWALK_V1 = STOP_SCOPED
DECLARED_TPC149_159_180_184_193_202_BAD_ENDPOINT_TRIGGER_V1 = STOP_SCOPED
```

第一项只停止从 selected 103/107 的现有八条 archived child paths
解释出一个共同 opened-`D` attachment；第二项只停止把现有 TPC-133
single-row AST 与 TPC-134 edge multiplier 重命名为同一 typed `T_D`
上的 literal `B_alpha B_gamma`；第三项只停止把列出的 good-scale、
shadow、空 phase census、target contract 与 averaged-selector records
组合成 scheduled bad-shadow local-increment theorem。三项都不是数学
nonexistence theorem，不停止新 source record、新 theorem、两个 O161
parents、pair-native/H1/global architecture。

`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1` 必须继续
`STOP_SCOPED`；不得把 phase `L2`、Lebesgue-a.e.、size-only、
log-to-natural，或旧 method cells 的重包装记作新 theorem。

2026-07-31 的全仓 H1 local-edge audit 新增且仅新增：

```text
DECLARED_TPC1_206_REACHABLE_LOCAL_OCCURRENCE_EDGE_SOURCE_CORPUS_V2
  = STOP_SCOPED
```

它只停止从 commit `023ccb5959e35b96673117b76add3dcbc3987aca`
的 TPC-1--206 paper corpus，以及当时所有 refs 按第 16 节选择器可达的
历史 blobs，重新包装出 production actual local-occurrence edge。它不
覆盖未来 refs、未 fetch source、真正新增的 source theorem 或独立
architecture reroute。

2026-07-31 的 one-packet source-forward 与自动 fallback census 新增且仅
新增：

```text
DECLARED_SELECTED_ONE_PACKET_SOURCE_FORWARD_PRECUT_TO_ACTUAL_OCCURRENCE_LINEAGE_V1
  = STOP_SCOPED
DECLARED_TPC133_134_136_NONSELECTED_TPC18_GEOMETRY_ORDERED_PAIR_LINEAGE_JOIN_CORPUS_V1
  = STOP_SCOPED
```

第一项只停止第 17 节列举的当前 source universe 中，把现有
native/archive/path/cut 身份改名为 actual physical occurrence 后再声称
source-forward edge；第二项只停止当前 committed TPC-133/134/136
archive 中、排除 exact selected `103 -> 107` orientation 后、满足严格
TPC-18 `NO_TAIL_ROOM` geometry 的 ordered pair join corpus。它们都不是
数学不存在性定理，不停止新 primary theorem、source-locked opened-`D`
attachment、pair-native reroute、两个 O161 parents、H1 或 global
architecture。

2026-07-31 的 positive determinant-two seed carrier audit 新增且仅新增：

```text
DECLARED_X512_H2_ALPHA17_D1_GAMMA16_D1_POSDET2_OPENED_D_PACKET_ATTACHMENT_V1
  = STOP_SCOPED
DECLARED_TPC133_134_136_POSDET2_BOTH_PRIME_PRIMITIVE_MASK_CORPUS_V1
  = STOP_SCOPED
```

第一项只停止把 exact seed
`alpha=(17,1), gamma=(16,1), j=33, block=(4,5,0)` 提升为 TPC-18
prime-source opened-`D` pair；其 `gamma` source `ell=16` 是 prime
power 而不是 prime，故 prime-reduced carrier weight 恰为零。第二项只
停止当前 committed strict archive 中 14 个 positive determinant-two、
both-prime pair-block instances 走 TPC-18/TPC-25 的 primitive mask：
每个实例都恰有一个 even divisor row，故在 `h0=2` 下 joint primitive
mask 为零。它不停止 TPC-18 的 formal constant-mask formula、真正新增的
source-locked physical mask theorem、nonprimitive endpoint reroute、两个
O161 parents、H1 或 global architecture。

2026-07-31 的 `23/11` mixed-`d` actual-mask 审计新增且仅新增：

```text
DECLARED_X512_H2_ALPHA23_D1_GAMMA11_D2_POSDET2_ACTUAL_PHYSICAL_JOINT_MASK_ATTACHMENT_V1
  = STOP_SCOPED
```

它只停止把 exact seed
`alpha=(23,1,k=24), gamma=(11,2,k=48), j=24, block=(4,5,0)`
在当前 TPC-18/21/25/32/93 与 TPC-133/134/136 source locks 下提升为
非零 actual physical joint packet。TPC-18 primitive mask 在两侧都为零；
TPC-25/32 primitive carrier 还排除 `d_gamma=2` 与 `j=24`；TPC-18
`xi=1` 只是 formal admissible mask，没有 formal-to-physical attachment
theorem；`s=2` endpoint 是同一 `k` 的另一对象。它不停止新的
formal-to-physical theorem、新的 named dyadic member、具有非零 common-`k`
endpoint coefficient 的 source record、两个 O161 parents、H1 或 global
architecture。

2026-07-31 的 TPC-18 `s=2` source-forward 审计新增且仅新增：

```text
DECLARED_TPC18_H0_2_COMMON_K_ENDPOINT_SOURCE_FORWARD_RECORD_CORPUS_V1
  = STOP_SCOPED
```

它只停止在 commit `f2f98b0bdc4b56c36292e9211b19c1d2e45ffae0` 可达的
TPC-17/18、TPC-133/134/136/143/153/154 与 TPC-205/206 记录中，把
`D0=0,V=2` 的同偶数 `k` 形式配对，或 TPC-18 的
`D0=6,V=18,h=6` finite identity fixture，改名为 `h0=2,s=2` 的
nonzero actual endpoint/source-forward record。它不停止 TPC-18 的通用
endpoint identity、真正新增的 `h0=2` branch-selection theorem、具名 actual
common-`k` packet、两个 O161 parents、H1 或 global architecture。

2026-07-31 的下一轮 `h0=2` exact-profile / branch-selection 审计新增且仅新增：

```text
DECLARED_TPC18_H0_2_TAIL_FAILURE_A_EXCLUSION_AND_DIRECT_B_CORPUS_V1
  = STOP_SCOPED
```

它只停止在本轮审核的 34 个 git refs、仓库现有 TPC-17/18/19/27/28/108
对象，以及截至 2026-07-31 逐对象核查的 Maynard、Li、Lichtman、Pascadi、
Matomäki--Radziwiłł--Tao、Goldston--Yıldırım、Ramaré--Zúñiga Alterman、
Laporta 与 Coppola--Murty--Saha primary theorem 候选中，把 AP / factorable
平均分布、shift-average、log-average、截断平方、size-only LCM 对角或带
未验证强假设的对象改名为：具名 actual `h0=2` symmetric-tail failure、完整
`r_R r_R` primitive-A 排除，或 `C_{I,2}^{MM,off}` 的 direct lower bound。
它不停止真正新增的 full-residual determinant theorem、theorem-backed
fixed-block tail-failure、direct `s=2` finite-model theorem、两个 O161 parents、
H1 或 global architecture。

2026-07-31 的 full-`r_Rr_R` primitive-A / ultra-complement 审计新增且仅新增：

```text
DECLARED_TPC18_H0_2_FULL_R_R_PRIMITIVE_ULTRA_COMPLEMENT_CORPUS_V1
  = STOP_SCOPED
```

它只停止在审计基线 `HEAD=origin/main=687bc2d44a25efd2a376fd3b363bfac4549b4cb9`
时可达的 346-commit all-ref snapshot、TPC-18--124 ultra-residual
lineage、TPC-125--206 relevant claim/status，以及截至 2026-07-31 审核的
Menon、Ramaré--Zuniga Alterman 与既有 fixed/log/shift/phase-average primary
theorem candidates中，把以下对象改名为 full primitive-A closure：

```text
one selected TPC-28 truncated square
TPC-29/30 content-rich or large-content sectors
TPC-27 additive Poisson zero
TPC-31/32 almost-all nonzero determinant frequencies
TPC-116 conditional complete-tail schema
size-only, logarithmic, exceptional-scale, phase/origin/shift-average results.
```

它不停止新的 `DD_2(theta)` all-slice theorem、同一 TPC-32 packet 上的
small-content matched auxiliary-zero theorem、TPC-111/122 signed-prefix exact
transfer、真正新增的 growing prefix theorem、两个 O161 parents、H1、
pair-native reroute 或 global architecture。

2026-07-31 的 TPC-32 selected-packet signed-prefix transfer 审计新增且仅新增：

```text
DECLARED_TPC32_111_122_SELECTED_PACKET_AUXILIARY_ZERO_SIGNED_PREFIX_TRANSFER_V1
  = STOP_SCOPED
```

它只停止从当前 committed TPC-28--32 selected high-beta packet、TPC-111/122
Abel--BV formulas、TPC-124 determinant/zero-fiber comparison，以及 TPC-126/127
exact prefix transports中，直接重命名出同一个
`A_hat_C,q(0)` 的 source-backed growing signed-prefix theorem。当前缺少实际
coefficientwise fiber intertwiner、共同 factor allocation、`N0=JQ^2` normalization
crosswalk，以及 TPC-122 要求的 growing prefix、outer BV envelope 与 content
remainder estimates。它不停止新的 actual intertwiner、直接控制同一 `A_C` 的
theorem、保留全部 literal data 的新 growing-prefix theorem、两个 O161 parents、
pair-native reroute、H1 或 global architecture。

2026-07-31 的第 23.5 节 named-primary reopen-candidate 审计新增且仅新增：

```text
DECLARED_TPC32_23_5_NAMED_PRIMARY_REOPEN_CANDIDATES_20260731_V1
  = STOP_SCOPED
```

它只停止把 Banks--Shparlinski `arXiv:2506.08787v1`、Verjovsky
`arXiv:2607.25002v1`、Ford--Radziwiłł `arXiv:2605.03349v1`，或
Matomäki--Teräväinen `arXiv:2605.27833v1` 的已审核 theorem statements
改名为同一 actual `A_C` 的 coefficientwise fiber map、直接 distinguished-zero
saving，或带 outer BV/content remainder 的 growing all-prefix theorem。它不扩张
任何旧 `STOP_SCOPED` cell，也不停止这些来源的新版本、真正新增的 actual
corollary/crosswalk、两个 O161 parents、pair-native reroute、H1 或 global
architecture；精确字段审计见第 27 节。

2026-08-01 的第 23.5 节 current-primary theorem-route 审计新增且仅新增：

```text
DECLARED_TPC32_23_5_NAMED_PRIMARY_REOPEN_CANDIDATES_20260801_V1
  = STOP_SCOPED
```

它只停止把 Tao--Teräväinen `arXiv:2512.01739v2`、Cantarini
`arXiv:2607.09110v1`、Kim `arXiv:2603.23250v2`、Grimmelt--Merikoski
`arXiv:2404.08502v2`、Fragkos--Krause--Miheisi--Sun
`arXiv:2607.05560v1`、Lau `arXiv:2509.07556v2`、Koukoulopoulos
`arXiv:2605.01412v1`、Pozdnyakov `arXiv:2604.23427v1` 或 Chavez
`arXiv:2409.02106v10` 的已审核 theorem statements，单独或跨来源拼接后改名为
同一 actual `A_C` 的 coefficientwise fiber map、direct matched-shell saving，或带
outer BV/content remainder 的 growing all-prefix theorem。它不扩张 Higher
Uniformity、Pilatte、single-factor、almost-all/origin-average、logarithmic/cumulative
等旧 `STOP_SCOPED` cells，也不是未审核文献或未来定理的 nonexistence claim；
精确 scope、字段审计与 reopen interface 见第 28 节。

2026-08-01 的 selected-packet common-occurrence compiler 与
Grimmelt--Merikoski Part-I inverse-atom 审计新增且仅新增：

```text
DECLARED_TPC32_SELECTED_PACKET_COMMON_OCCURRENCE_QD_QZ_METADATA_PRESERVING_INTERTWINER_V1
  = STOP_SCOPED
DECLARED_TPC32_GM2505_V2_INVERSE_ATOM_ACTUAL_CROSS_ROW_COMPACT_SELF_KERNEL_V1
  = STOP_SCOPED
```

第一项只停止把当前 TPC-32/TPC-93 的参数化、lossless formula compiler
直接升级为 TPC-144 所需的 metadata-preserving output-record bijection：
both-ultra raw leaf 在 determinant parent 侧聚为一个 record，而 ordered-zero
侧必须保留两个各带 `1/2` 的 `L/R` records；实际 selected schedule 是否含
nonzero both-ultra occurrence仍 `NOT_TESTABLE`。它不停止未来的 actual occurrence
registry、允许正确 typed linear relation 的新架构、或真正新增的 growing-prefix
theorem。

第二项只停止从 Grimmelt--Merikoski `arXiv:2505.00489v2` Part I、本轮
exact inverse-atom attachment 与当前 committed TPC source corpus，直接推出
actual cross-row self-kernel 的 tiny-power bound或 strict `1/400` saving。
inverse placement、atomwise determinant normalization、zero-Haar test 与 fixed-row
`j`-arc escape 本身是 `L1 GO`，没有被此 cell 否定。该 cell 不停止未来的
actual equal-difference four-point autocorrelation theorem、不同 functional
factorization、Part II、新版本 source、两个 O161 parents、pair-native/H1/global
architecture 或任何真正新增的算术输入；精确公式与 scope 见第 29 节。

2026-08-01 的 literal fixed-`D0` TPC-93 transversal、current-primary
four-point transfer 与 cross-`D0` standard-orthogonality 审计新增且仅新增：

```text
DECLARED_TPC32_LITERAL_FIXED_D0_FOURPOINT_STANDARD_TRANSFER_
AND_CROSS_D0_ORTHOGONALITY_CORPUS_V1 = STOP_SCOPED
```

它只停止把第 30 节逐项审核的当前 committed TPC-32/34/38/42/48/84/93/95/108
interfaces、Grimmelt--Merikoski `arXiv:2505.00493v2` application、Tao--Teräväinen
`arXiv:2512.01739v2` 与 `2107.02158v4`、Menon `2607.15574v1`、
Jaskari--Sachpazis `2409.10663v3`、Leng `2212.09635v3`、
Klurman--Mangerel `1708.03176v1`、Lichtman--Teräväinen `2111.08912v3`、
Higher Uniformity II `2411.05770v2`、Kim `2603.23250v2`，以及 ordinary
Schur/Young、additive/Dirichlet large sieve、Fourier/Mellin complete-frequency
identities，直接或跨来源拼接成 literal fixed-`D0` `E_Psi` bound，或再提升成
full `E1`。它不停止直接接受 actual `w_m` 的新 theorem、保留全部 metadata 且
global projective total variation 为 `X^o(1)` 的 source-backed regrouping、完整
two-parameter automorphic self-kernel theorem、actual cross-`D0` block-Bessel
theorem、未来 GM Part II/新版本、两个 O161 parents、pair-native/H1/global
architecture或真正新增的独立算术输入；精确 source locks、第一 fatal 与
reopen interface见第 30 节。

2026-08-01 的 fixed-`D0` theorem-parameter-preserving outer regroup、physical
`m`-coarsening 与 post-第 30 节 direct/frame source 审计新增且仅新增：

```text
DECLARED_TPC32_FIXED_D0_OUTER_REGROUP_AND_POST30_DIRECT_FRAME_
SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

它只停止以下有限对象：TPC-93 decorated children 在 fixed `D0` 下按
`(L/R,ell,ell',j,sigma_aff,v,iota)` 保持同一 affine theorem parameters 的
regroup；这里 `sigma_aff=sigma_theta` 是 TPC-93 的整数 affine slope，不是
selected-packet 参数 `sigma=1/10000`；
按 physical moving row `m` 使用 source-child inverse 的 exact coarsening；Carella
`arXiv:2202.01071v5`、Jiseong Kim `2509.24152v1`、Diao `2506.18065v1`、
Krishnamoorthy `2501.10962v2`；Qi `2404.09085v3` 与 `2407.17711v1`、
Lekkas--Voskou `2405.01056v2`、Pascadi `2404.04239v3`、Hu--Petrow--Young
`2411.05672v3`，以及本轮复核的 GM Part-I/application self-kernel interface。
Carella source因证明链无效而不得注册成 theorem input；其余来源只按各自
source-backed theorem statement 的原 scope冻结。Banks--Shparlinski
`2506.08787v1` 与 Cantarini `2607.09110v1` 的旧 scope仍分别由第 27--28 节
既有 cells管理，本 cell不重复扩张。

该 cell不停止一个直接接受 exact literal `w_m/E_Psi` 的新定理、production
actual-edge census加 coefficientwise intertwiner与 `X^o(1)` global projective
decomposition、允许 row primes/cofactors/slopes/outer labels 随 `m` 变化的
真正 growing theorem、literal full GM self-kernel/cross-`D0` frame theorem、
未来 source版本、两个 O161 parents、pair-native/H1/global architecture或任何
真正新增的独立算术输入；精确二分结构、source proof audit、frame fatal 与
reopen interface见第 31 节。

2026-08-01 的 post-第 31 节 natural binary-Möbius primary-source refresh新增且
仅新增：

```text
DECLARED_TPC32_POST31_NATURAL_BINARY_MOBIUS_PRIMARY_
SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

它只停止把第 32.2 节逐 theorem-body 审核的 Klurman--Mangerel--Teräväinen
`arXiv:2304.05344v2`、Pilatte `2310.19357v2`、Frantzikinakis--Host
`1502.02646v3`、Mangerel `1612.09544v2`、Kravitz--Woo--Xu
`2512.03292v1`、Frantzikinakis--Klurman--Moreira `2407.08360v3` 与
Tao--Teräväinen `1809.02518v2`，直接升级成同一 selected high-beta packet 的
prescribed natural positive-power theorem。KMT 的 determinant
prime `2` support condition可由第 32.2 节的 exact `mu_odd` replacement无损通过；
本 cell不得把 `mu(2)=-1` 重新列为 fatal。真正冻结的只是其 small truncated
pretentious-distance、logarithmic output、fixed/polylog coefficient range、terminal
unweighted sum与 literal physical attachment的当前 source scope。该 cell不停止未来
新版本、直接接受 actual coefficient/weights/prefix/normalization的新 theorem，或其他
真正新增的独立算术输入。

同日的 selected high-beta determinant-zero / additive-metric source refresh新增且
仅新增：

```text
DECLARED_TPC32_SELECTED_HIGH_BETA_METRIC_SCHEDULE_EXCEPTIONAL_
LIMSUP_AVOIDANCE_SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

它只停止把当前 TPC-32 normalized-determinant DFT zero无 intertwiner地改名为
TPC-170/181 additive phase atom，或把第 32.3 节列出的 algorithmic-randomness、
moving-target、dynamical Borel--Cantelli与 divergence-limsup theorems升级成 exact
named packet的 schedule-specific bad-event avoidance。它不停止未来直接作用于
`A_hat_C,q_DFT(0)` 的 pointwise theorem、真正 source-backed additive atom + actual
schedule + same-event avoidance theorem、两个 O161 parents、H1、pair-native reroute
或 global architecture。

同日的 current committed actual-census / intertwiner / projective-cost refresh新增且
仅新增：

```text
DECLARED_TPC32_HIGH_BETA_CURRENT_COMMITTED_CENSUS_
INTERTWINER_XO_PROJECTIVE_CORPUS_V1 = STOP_SCOPED
```

它只停止从当前 committed TPC-32/84/93/124/173--179/193--206 artifacts，借
symbolic formula、future schema、异源 finite fixture、row-only record、one-vector
equality、finite SVD或 atomic triangle，构造同一 high-beta packet的 actual census、
coefficientwise intertwiner或 source-backed `X^o(1)` global projective theorem；也
停止把 TT-star bilinear pair重命名为 H1 linear local-occurrence edge。它不停止未来
同 packet actual parent registry、真实 growing matrices与完整 coefficientwise identity、
新 projective theorem、direct literal theorem或任何开放 architecture。精确 first
fatals与合法 materialization order见第 32.4 节。

发布前远端新增 RH-340 后，只新增下列精确有限 cross-program cell：

```text
DECLARED_TPC32_REMOTE_RH340_SYNCHRONIZED_PREFIX_TRANSFER_V1
  = STOP_SCOPED
```

它只停止把 commit `eb1cf19a28b1d1d38eaece2a6bb0b578f20df969` 中 RH-340
Hardy trace-order 的 `P_u/E_u/D_u` absolute coefficient budgets、条件必要的
two-order orbit--head compensation，或 cancellation-blind separate-absolute
majorant obstruction，直接升级为 TPC-32 同一 high-beta packet 的 ordered
signed-prefix theorem、small-content matched-shell saving或 distinguished
determinant-zero theorem。RH 的 moving orders `2k,2k-2` 不是 fixed physical
`h0=2`，其 `R^n/n` normalization也不是 `N0=JQ^2 asymp XQ`。该 cell不停止未来
真正保留 literal TPC coefficient、fixed `h0=2`、canonical prefix order、actual
masks/weights/outer labels、`N0` normalization与完整 physical-loss ledger的新
theorem，也不停止两个 O161 parents、pair-native reroute、H1/global architecture；
精确 type audit见第 32.7 节。

最终 pull/rebase又取得 RH-341，只新增下列精确有限 cross-program cell：

```text
DECLARED_TPC32_REMOTE_RH341_ACTUAL_FIRST_ALIAS_
SIGNED_COMPLETION_TRANSFER_V1 = STOP_SCOPED
```

它只停止把 commit `6e1478a1a02ff4c3308e829727f8fea1cfbce52c` 的 RH Hardy
trace-order absolute prefix synchronization、条件必要的 moving orders
`2k,2k-2` orbit--head compensation，或 abstract information-class
cancelling/noncancelling completions，升级为 TPC-32 同一 high-beta packet 的
ordered signed-prefix theorem、small-content matched-shell saving或 distinguished
determinant-zero theorem。RH 的 `q_(sigma,k,n)` 是 trace coefficient而不是 TPC
modulus；两个 moving orders相差 `2` 也不构成 fixed physical `h0=2`；`R^n/n`
与 `H_k` normalization均不是 `N0=JQ^2 asymp XQ`。

该 cell不停止未来真正保留 literal TPC coefficient、fixed `h0=2`、canonical
prefix order、actual masks/weights/outer labels、`N0` normalization、uniform
ranges/constants与完整 physical-loss ledger的新 theorem，也不停止两个 O161
parents、pair-native reroute、H1/global architecture；精确 audit见第 32.8 节。

2026-08-01 的 O161 pointwise current-primary version-delta refresh新增且仅新增：

```text
DECLARED_O161_DIRECT_BAD_ENDPOINT_CURRENT_PRIMARY_
VERSION_DELTA_CANDIDATES_20260801_V1 = STOP_SCOPED
```

它只停止把第 33 节逐 theorem-body 审核的 el Abdalaoui--Nerurkar
`arXiv:2006.07646v2`、Grimmelt--Teräväinen `2607.28091v1`、
Matthiesen `1606.04482v4`、Browning--Sofos--Teräväinen
`2212.10373v2`、Burstein--Iosevich--Sant `2604.14482v1`、
Pandey--Radziwiłł `2510.20194v1`、Cantarini--Gambini--Zaccagnini
`2603.10241v1`、el Abdalaoui--Lin `2607.15960v1`、
Pilatte `2604.26564v1` 与 Murty--Vatwani
*A remark on a conjecture of Chowla* 的已审核 statements，单独或跨来源
拼接后升级为 O161 的 literal two-Möbius named-atom fixed-power theorem。

Teräväinen--Walker `2303.12574`、Tao--Teräväinen
`2512.01739v2`、Pilatte `2310.19357v2`、
Klurman--Mangerel--Teräväinen `2304.05344v2` 与
Ramaré--Zúñiga Alterman `2603.25961v3` 只作为既有
`STOP_SCOPED` cells的一致性 countercheck；本 cell不重新包装或扩张
它们的旧 scope。它也不是全局文献 nonexistence claim，不停止未来直接接受
literal coefficient、actual named atom、growing parameters、正确 prefix/
normalization及完整 loss ledger的新 theorem。两个 O161 parents、pair-native
reroute、H1/global architecture继续 `OPEN`；精确公式、第一 fatal与
reopen interface见第 33 节。

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

第 32 节对五类入口作了 post-第 31 节有限刷新；状态仍为：

```text
DIRECT = FAIL
METRIC = FAIL
BAD_ENDPOINT = FAIL
STRUCTURAL = FAIL
DECLARED_CORPUS = FAIL
```

其中 `DIRECT/DECLARED_CORPUS` 没有 prescribed natural positive-power theorem；
`METRIC` 先在 determinant DFT zero与 additive atom的对象类型处失败；
`STRUCTURAL` 仍没有同 packet production carrier，TPC-175 coverage保持 `0/2988`；
`BAD_ENDPOINT` 没有新的 literal fixed-atom local-increment theorem。该刷新不把
failure写成全局不存在定理，也不改变上述未来 trigger定义。

第 33 节又分别按 `q/N` terminal/block DIRECT与 `q/T`
cumulative BAD_ENDPOINT合同审核 current-primary version delta。两路都先缺
source-locked named production atom/actual record；反事实补齐 data后，审核的
single-source theorems仍没有 literal two-sign coefficient、prescribed tuple、
正确 bad-scale local block、uniform fixed power或完整 ledger。因此：

```text
DIRECT = FAIL_CLOSED_PARENT_OPEN
BAD_ENDPOINT = FAIL_CLOSED_PARENT_OPEN
CURRENT_PRIMARY_SINGLE_SOURCE_SURVIVORS = 0
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
TPC207_TRIGGER = false
```

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

## 10. 不编号 single-record extraction audit

2026-07-30 用户选择了 route (1)。本轮只审核当前仓库、全部可达 Git
历史与远端 refs 中能否抽取一个
`SOURCE_LOCKED_NAMED_PRODUCTION_ATOM_RECORD`；没有把授权本身当作
record 或 theorem evidence。

唯一最接近的来源链为：

```text
TPC-18 actual tail/opened-d partition
  -> TPC-25 opened-row provenance
  -> TPC-32 physical matched shell
  -> TPC-93 resolved fixed-h0 packet family
  -> TPC-94 signed phase/conductor
  -> TPC-108 literal generic block
  -> TPC-127 determinant-two specialization/prefix isometry
  -> TPC-194 PHYSICAL_PACKET_PREFIX
```

这条链 source-backed 地给出每个 resolved key 的 literal carrier、
decorated coefficient、symbolic phase、per-key prefix 与 outer
multiplier。但是：

- `Xi_X(K,R)` 只是在 fixed `X,K,R` 下实际 export 中出现的
  `xi=(theta,c,kappa,r)` 的有限集合；它没有跨尺度
  `ambient_scale_id/packet_id/terminal_T/physical_occurrence` rows，
  因而不是 exact all-scale production schedule；
- `alpha_xi_X` 随 `X,theta,c,kappa,r,q_X` 变化。仓库没有
  source-located selector 证明同一个 `alpha_star` 在每个 required
  scale 实际出现；
- TPC-197 排除非零 fixed rational atom 通过无限多个不同 prime
  conductors `q_X` 重复出现；conductor-one 分支仍没有
  occurrence/schedule/range-admissibility theorem；
- 当前 tree、untracked text scope、全部可达 commits、remote heads 与
  tags 中没有非空 `named_physical_atom_id`、
  `phase_value_mod_1` 或 `packet_schedule_source_locator`。TPC-204 后
  没有 TPC 路径变化；RH 中的 `det_2` 命中属于谱 determinant，不是
  `su-ad=2` two-Mobius carrier。

逐字段结果：

```text
literal determinant-two carrier       = COMPLETE_PER_PACKET
physical prefix domain/index          = COMPLETE_PER_PACKET
decorated coefficient                 = COMPLETE_PER_PACKET
outer multiplier                      = COMPLETE_PER_PACKET
symbolic alpha_xi_X                    = COMPLETE_PER_PACKET
named_production_atom                 = MISSING   [first mismatch]
exact_cross_scale_packet_schedule     = MISSING
common_X_N_q_ranges                   = MISSING
uniform_constant_C                    = MISSING
positive_sigma                        = MISSING
target_normalization_selection        = MISSING
complete_physical_loss_ledger         = MISSING
```

禁止把 archive/resolved key 当作 production schedule，禁止令
`q_X=a*s`，也禁止选择一个随尺度变化的 `alpha_xi_X` 后称其为 fixed
named atom。

反事实 theorem crosswalk 也为负：即使七字段全部 supplied，TW25 的
native normalization 仍是 reciprocal/logarithmic 且只有 qualitative
`o(1)`；TT26 仍只给 terminal block、删除 exceptional scales且只有
log saving。因此在本轮已审核的 TPC-193 七源及所列 external
near-neighbor theorem scope 内，不存在可与该 record literal
crosswalk 的 fixed-data uniform positive-`X`-power
all-prefix/all-scale theorem。

最终不编号 verdict：

```text
SOURCE_LOCKED_SINGLE_RECORD_EXTRACTION = FAIL
first_record_mismatch = NAMED_PRODUCTION_ATOM
counterfactual_complete_record_theorem_trigger = FAIL
mathematical_reopen = false
tpc205_authorized = false
```

这只关闭当前 source/history/ref scope，不声称所有未来 production
records 或定理不存在。

## 11. 不编号 single-cut 到 actual packet 审计

2026-07-30 用户选择先审核 structural single-cut 路线。本轮授权仅为：

```text
UNNUMBERED_SINGLE_CUT_TO_ACTUAL_PACKET_CROSSWALK_AUDIT
```

它没有自动授权 TPC-205。用于 fail-fast 的选定 production cut archive
row 为：

```text
cut_path_id
  = cut|X=512|h0=2|ell=103|k=5|d=1|jL=6|jK=3|D0=0|type=TAIL
archive_address = (103,5,1,6,3)
terminal_type = FRONTIER_UNMAPPED
frontier_reason = NO_TAIL_ROOM
physical_normalization = nu_X
support_role = FORMAL_SUPPORT_ENVELOPE
numeric_coefficient_nonzero_status = UNDECIDED
native coefficient
  = -Lambda(103) r_4(517) W(515/512)
```

对应链的 native/path/cut/obligation/shadow/formal records 分别实际
出现于：

```text
TPC-133 sample line 724
  integrity = e550d2d7be48d85076919a8adf86ba446f88f75b404df48c0483d3cf27b59369
TPC-134 sample line 2554
  integrity = fb013b12446318c3f902909a479ddefb8329e771e936e58a2dfcc47a9e450b4f
TPC-136 sample line 2554
  integrity = 2eef9d8670c23ffc10b2a9cab0d488b0908293cfdb482667da824e702a1347cc
TPC-143 obligation line 26
  integrity = 368c72239ffa82bf7cb0731cc55f18bc696ddea7e8d4d6cbf19df374a811f7d5
TPC-153 shadow line 26
  integrity = 4251a4db295bf7f5fef76fd851fbab2899b8606191478ffd3e52e9e77d639c4c
TPC-154 formal fibre line 26
  integrity = 2fc1d9e30e0f23a6e645f9c4fbb335d4e4fec817598e2483e883f0d3a939a14a
```

TPC-143 对该 cut 给出
`actual_map_edges=[]`；TPC-153 的
`partial_occurrence_id=cut-shadow|2ff38d6cc9f3de3eb0b7ed2b`，
`actual_occurrence_id` 与 `actual_branch_count` 均为空；TPC-154 只有
互不唯一的 `FORMAL_ONLY` completions。

上游整数重标号本身成立：

```text
alpha_0 = (ell,d) = (103,1)
j_0 = k/d = 5
m_alpha_0 * j_0 = ell*k = 515
m_alpha_0 * j_0 + h0 = 517
```

因此 TPC-18/TPC-25 的 opened-row 数值、target 与 smooth arguments
相容。甚至可以手工选择

```text
gamma_0 = (107,1)
u = 11
sigma = 47
v = 1
```

使 `517=11*47`，并得到条件式 affine pair

```text
D_theta(t) = 1 + 47*t
U_theta(t) = 11 + 515*t
47*11 - 515*1 = 2.
```

这只证明：若满足 TPC-93 retained-source domain 的完整
`omega=(L,alpha,gamma,j,u)` 已经 supplied，包括未由 cut source-lock
的 `T<u<=U0` schedule，则其 source-child inverse 在代数上相容。再
手工 supplied

```text
c = kappa = B = 1
tau = 0
```

才可进入条件式 content-resolved 分支

```text
D_xi(z) = 1 + 47*z
V_xi(z) = 11 + 515*z.
```

此后 content/progression、TPC-127 pullback 与 TPC-194 per-key formula
可以内部相容。它不证明该 `omega` 由原 cut 产生；手选 `gamma_0`、
`u`、schedule、polarization、`c/kappa/B/tau` 或 content-resolved
template 均不是 theorem evidence。

决定性断点在 TPC-18 的实际公式

```text
|T_D|^2 \ll_W J (E_D + C_D^off).
```

它是 Cauchy/TT-star 后的二次不等式，不是原 cut coefficient 的线性
保守分解。原 cut 只确定 `alpha,j`；off-diagonal parent 还需要
`gamma`，opened ultra layer 还需要 `u`。取 `gamma=alpha` 不能补洞：
它属于独立 diagonal energy，且 generic/off-diagonal mask 删除对角。
TPC-93 的 projector weights 只重构已经 supplied 的 source atom
`omega`，并不逐列重构 Cauchy 之前的 cut coefficient。

因此精确第一缺口为：

```text
CUT_TO_CANONICAL_PARENT_AND_INVERSE_AGGREGATED_COEFFICIENT_CROSSWALK
```

这里的 `CANONICAL_PARENT` 仅指 TPC-143
`canonical_parent_and_QD` 所需的 typed parent-key field；它不证明、
也不得冒充 `H1.canonical_minimal_representation_certificate`。

四项主 fail-fast 结果：

```text
SOURCE_BACKED_CANONICAL_PARENT_GAMMA_U = FAIL
COEFFICIENTWISE_LINEAR_CUT_LIFT = FAIL
EXACT_RATIONAL_EDGE_CONSERVATION_AND_ACTUAL_ID = NOT_TESTABLE
H0_AND_NU_X_LINEAGE
  = FAIL:H0_COMPATIBLE_BUT_END_TO_END_NOT_SOURCE_LOCKED
```

两个 auxiliary patch verdict：

```text
NONEMPTY_CONDITIONAL_AFFINE_PAIR = PASS
NONEMPTY_SOURCE_BACKED_PRODUCTION_PATCH = FAIL
```

TPC-174 不能被用来把这些缺口 schema-complete：其
`actual_occurrence_id` 只是 supplied 非空字符串，未独立验证 archive
membership、具体 occurrence 语义或公式导出的 edge weight；其 production
join 又硬锁 TPC-173 的 TPC-133--172 corpus，而该 corpus 的 qualifying
claim count 为零。opened row、TPC-153 shadow、裸 `omega` 或裸 `xi`
均不得通过字符串改名成为 actual occurrence。

历史核查在 TPC snapshot `1cf3c8f` 覆盖从当时 34 个 enumerated refs
可达的 318 个 commits，并检查相关链的 75 个历史 text blobs。发布前
fetch 新增的 `7429c87`、`e57a0e2` 仅改 RH series 与 `RH_HANDOFF.md`；
单独 diff scan 未发现 TPC corridor 或 `TPC_HANDOFF.md` 变化，相关
75 个 text blobs 不变。候选只命中
native/path/cut/obligation/shadow/formal records；没有 non-null actual
occurrence、nonempty actual edge，或 cut-to-`omega`/`xi` locator。这
不声称 unreachable/pruned objects 或未列 source universe 中不存在新
theorem。

平台检查备注：

```text
TPC-133 --check = PASS
TPC-143 --check = PASS
TPC-153 --check = PASS
TPC-154 --check = PASS
TPC-173/174/179 --check = PASS
TPC-134/135/136 legacy raw-byte checks on LF checkout = FAIL_CRLF_PIN_ONLY
canonical/in-memory regenerated semantic content = MATCH
git diff on those artifacts = EMPTY
```

TPC-134/135/136 的失败来自历史 CRLF raw-hash pins，不是公式、记录或
生成内容漂移；它既不是数学 trigger，也没有在本轮被顺手修改。

最终不编号 verdict：

```text
UNNUMBERED_SINGLE_CUT_TO_ACTUAL_PACKET_CROSSWALK_AUDIT = FAIL_CLOSED
first_missing
  = CUT_TO_CANONICAL_PARENT_AND_INVERSE_AGGREGATED_COEFFICIENT_CROSSWALK
SINGLE_CUT_STRUCTURAL_REOPEN_TRIGGER = FAIL
mathematical_reopen = false
tpc205_authorized = false
```

这只关闭上述 singleton-cut 直接组合 method cell。只有新的 theorem
精确重建原 cut coefficient、逐列 conservation、`gamma/u` 与 `nu_X`
lineage，才可触发 H1 structural reopen。把 source domain 移到
post-TT-star pair-native atoms 属于 architecture reroute；它必须新增
distinct registry 与 theorem-backed crosswalk，不能自动记作 reopen。
H1 architecture 与两个 O161 parents 保持 `OPEN`。

## 12. 不编号 pair-native post-TT-star 审计

2026-07-30 用户授权路线 1。本轮授权仅为：

```text
UNNUMBERED_PAIR_NATIVE_POST_TTSTAR_REPAIR_AUDIT
```

它没有自动授权 TPC-205，也没有解除任何数学门槛。

本节是 TPC-205 编号前的历史审计记录。下文出现的
`tpc205_authorized=false` 仅记录当时的 workflow 状态；该状态现已由用户
后续有限授权和第 13 节的已完成论文取代。公式门槛、失败 gate 与
`STOP_SCOPED` 结论没有被授权动作改写。

### 12.1 公式级 ordered pair 与 exact coefficient

TPC-18 的实际 post-Cauchy/TT-star 公式为

```text
|T_D|^2 \ll_W J (E_D + C_D^off).
```

`C_D^off` 的 ordered summation domain 是同一 opened-`D` packet 内的
`(alpha,gamma,j)`，其中 `alpha != gamma`。`gamma` 是平方展开产生的第二
dummy row，不是 singleton cut 选择或生成的字段。TPC-18 显示的 pair
coefficient carrier 仍含 `B` aliases，其形式为

```text
mu(d_alpha) mu(d_gamma)
(log ell_alpha)(log ell_gamma)
r_R(N_alpha(j)) r_R(N_gamma(j))
B_alpha(j) B_gamma(j).
```

TPC-18 的相关权重为实数；TPC-32 又显式规定 “No complex conjugation is
implicit”。因此若后续采用 Hermitian 记法，第二侧共轭必须显式记录，不能
通过解释性改写暗中补入。diagonal energy `E_D` 与 off-diagonal pair
分离；generic mask 删除 diagonal，但公式 support 仍不等于实际非零
occurrence。

TPC-32/TPC-93 的 matched symbolic parent 为

```text
w_{alpha,gamma,j}
  = gamma_alpha^(1) gamma_gamma^(2)
    A_{alpha,gamma}(j) K^sh_{alpha,gamma}(j),

K^sh_{alpha,gamma}(j)
  = C_{m_alpha}(j) H_{m_gamma}(j)
    + H_{m_alpha}(j) C_{m_gamma}(j).
```

`u` 不是 parent `(alpha,gamma,j)` 字段。它只在打开 ultra increment 后由
两个极化分别产生：

```text
L: T < u <= U0 and u | N_alpha(j)
R: T < u <= U0 and u | N_gamma(j).
```

因此 TT-star 第二行 `gamma` 的来源、以及 supplied parent 上打开
polarization 后的 `u` 枚举，各自在公式层成立；两者之间不存在已经审核
通过的 production `pair -> omega` bridge，也不能回填到原 singleton cut。

### 12.2 TPC-93 source-child reindexing

给定 retained source atom

```text
omega = (L/R,alpha,gamma,j,u),
```

TPC-93 对每个 `v | gcd(d,e)` 给出唯一 child `(theta,t)` 及显式
child-to-source inverse。其 algebraic multiplicity 是 `tau(gcd(d,e))`，
而 projector identity

```text
sum_{v | d,e} lambda_{G_X^row}(v)
  = 1_{gcd(d,e) <= G_X^row}
```

单个 `v`-child 不恢复 source atom；各 child 保留逐项符号与 coefficient，
对 `v` 加权求和后才恢复带 actual row-gcd mask 的 source coefficient。
`gcd(d,e)>G_X^row` 时该 contribution 为零。这里的 `G_X^row` 是 row-gcd
cutoff，不得与后续 target-content 参数混同。两个 polarizations 各出现
一次，符号与 coefficient 精确重组，不增加新的 fiber normalization。若
content、frequency 与 resolved fields 也分别 supplied，则
TPC-93/94/108/127 后续的 content、phase 与 determinant-two pullback
templates 在公式层相容。

因此只有以下分离结论通过：

```text
supplied retained omega -> theta source-child inverse = PASS
separately supplied downstream fields -> xi template
  = CONDITIONAL_FORMULA_COMPATIBLE
pair -> omega production crosswalk = FAIL
```

具体 admissible `xi` 与 concrete production row-pair/`omega`/`xi`
archive join 均未形成。

### 12.3 两个有限见证的严格标签

当前最强 dual archived-row candidate 为

```text
t0 = ((103,1),(107,1),5), h0 = 2
N_alpha = 517 = 11*47
N_gamma = 537 = 3*179
gcd(N_alpha,N_gamma) = 1
Delta# = -4
ordered row determinant = 2*(103-107) = -8
```

TPC-133 sample lines 724 与 736 的 native row integrity 分别为

```text
e550d2d7be48d85076919a8adf86ba446f88f75b404df48c0483d3cf27b59369
633e20ac5a83d425471be3ba095df10a1635c3f45ce5cac6def9d5ba936152d9
```

TPC-136 sample lines 2554 与 2602 的 cut integrity 分别为

```text
2eef9d8670c23ffc10b2a9cab0d488b0908293cfdb482667da824e702a1347cc
cdc0f7363ab88106ce65bb46da800c05c3fba2b391d9490d7b2ca8bab8c816db
```

两条 cut 都是 `FRONTIER_UNMAPPED / NO_TAIL_ROOM`。这个对象只能标记为

```text
DUAL_SOURCE_LOCKED_ROW_PAIR_CANDIDATE
```

不能标记为 production pair occurrence，因为归档中没有共同 pair ID、
实际 joint-mask value、source-locked `delta` 与 row schedule、
`T/U0`、prefix/divisor/polarization children、inverse-aggregated
coefficient、pair nonzero status，或 `nu_X` global-normalization return。
两条 individual row AST 的乘积也不得自动等同于 TPC-18 显示的
`B_alpha B_gamma` pair-coefficient carrier。

TPC-32 certificate 直接归档并检查的 finite primitive witness 只包括
`h=2,j=1,d=1,L=100,R=12,T=50,U0=200,C=30`、rows、targets 与 content
matrix。把其中前两行代入 TPC-93 source-child formulas，可手工推导出
以下严格有限 `L0` affine-child witness：

```text
L=100, R=12, T=50, U0=200, h=2, j=1, d=1
alpha=(59,1), gamma=(71,1), u=61
sigma=1, v=1, d0=0, t=1, u0=2
D(t)=1, U(t)=61, determinant=2, projector weight=1.
```

这些 child fields 不是 TPC-32 certificate 直接检查或输出的字段。组合
对象只能标记为

```text
TPC32_PRIMITIVE_FIXTURE_PLUS_TPC93_FORMULAS_DERIVED_L0_ONLY
```

它只证明 algebraic schema 非空。TPC-32 自身禁止把该 fixture 提升为
production/asymptotic evidence；TPC-93 verifier 的 synthetic `h0=1`
fixture 也不能冒充 production `h0=2`。

### 12.4 归档与 schema fail-closed 审核

在快照
`ad1366d8d4870dc6170a451345df58aec54e8675` 上，历史扫描覆盖 34 refs、
321 reachable commits、11,752 reachable object entries、7,190 text
blobs 与 1,855 record-like data blobs。TPC-18/25/32/93/94/108/127/194
走廊包含 119 reachable entries、112 unique paths、95 text files 与
14 个可解析 JSON。具体 record keys

```text
row_pair
row_pair_id
source_atom
resolved_key
omega
theta
xi
polarization
actual_occurrence_id
physical_occurrence_id
```

均没有形成 concrete source-locked join。TPC-145 的 actual edges 为空；
TPC-153 是 shadow；TPC-154 是 formal；TPC-155/174 是 synthetic，均不能
补 production occurrence。

现有 H1 schema 也不能通过填字符串修补：

- TPC-143 V1 固定 `actual_map_edges=[]` 与 `NOT_TESTABLE`；
- TPC-163/173 硬锁旧 corpus/count，扩展须新建 V2；
- TPC-174 的 occurrence ID 只验证非空字符串，cut address 不验证 archive
  membership 或完整 `X` packet scope，normalization 只做字符串相等，
  edge weight 未与实际公式绑定，AST 只复制不执行；若
  `actual_occurrence_id` 被解释为 target carrier，其 global uniqueness
  会排除 many-to-one，因此新 schema 不能直接复用该约束；
- TPC-178 的 tuple/hash/lex order 不是 canonical/minimal theorem；
- TPC-179 V1 必须保持原样，新路线须用独立 integration/root。

pair registry 必须保持 ordered pair，不得按交换对称 quotient；还必须分离
`edge_instance_id` 与 `target_occurrence_id`，并把 formal support 与
numeric nonzero status 分开。

### 12.5 normalization 与完整 loss ledger

当前 source-backed 公式只能冻结 TPC-18 的 unnormalized `T_D`
inequality。TPC-133/136 中的 `physical_normalization="nu_X"` 只是 scope
字符串；归档没有给出其数值 scalar 定义，也没有 theorem 证明它乘在
`T_D` 上。若未来 theorem supplies multiplicative scalar `c_X`，才可作
条件式推导

```text
|c_X T_D|^2
  <= C_W |c_X|^2 J (E_D + C_D^off).
```

后续 registry 必须分别记录 source/linear/quadratic/target normalization，
不能只复制一个 `nu_X` 字符串。完整 physical-loss ledger 必须区分以下
已量化 terms 与未供应 slots：

```text
prime-power error: X L^(-1/2) X^eps
dyadic-D partition:
  fixed bounded overlap
  O(log X) nonempty D-slices
  reassembly/pigeonhole cost <= one O(log X) factor
Cauchy factor J
diagonal: E_D << X^(1+eps)
same/near/gcd removals:
  same: XQ L^(-1) X^eps
  near: XQ (X^(-kappa)+L^(-1)) X^eps
  gcd:  XQ X^(-kappa+eps)
generic remainder = UNCONTROLLED_HARD_REMAINDER
TPC-25:
  zero: XQ{(log X)^(-A)+X^(-s+kappa+o(1))}
  principal: Q^2 X^eps
  drift: JQ^2 L^(-1) X^eps
  polylog: (log X)^(O(1))
TPC-32 drift: X^eps XQ/L
large content: X^eps XQ(1/J+1/C)
TPC-93 Fourier tail: X^(o(1)) N0 Rwin^(1/2-K)
square-root return = MISSING/UNSUPPLIED
full-block and endpoint reassembly = MISSING/UNSUPPLIED
```

本轮没有为 complete active pair、uncontrolled hard remainder 或目标
theorem 产生 uniform positive-power estimate，故 target
`positive_sigma`、strict-loss、endpoint `1/400` 与 `L2` credit 均不得
记账。已量化的 degenerate/drift savings 不能被提升为 hard-remainder 或
目标 theorem credit。

### 12.6 精确 first missing 与最终裁决

第一项 production 缺口冻结为

```text
SOURCE_LOCKED_POST_TTSTAR_ORDERED_PAIR_REGISTRY_WITH_COMPLETE_PAIR_COEFFICIENT_AND_GLOBAL_NORMALIZATION
```

其内部两个不可省略的 subgates 是：

```text
PAIR_NATIVE_POST_TTSTAR_ACTUAL_REGISTRY_WITH_FULL_LITERAL_SCOPE_AND_COEFFICIENT
TPC18_PAIR_TO_TPC93_RETAINED_SOURCE_ATOM_THEOREM_CROSSWALK
```

H1-E/TPC-143 的 conceptual object 是从 production cut columns 出发的
linear cut-to-occurrence map `L_X`，其 entries 概念上允许 signed/complex。
当前 TPC-174 finite contract 才进一步要求 2,988 个 production cut
columns 上的 nonzero exact-rational weights 与逐 cut column sum 1。
TPC-18 的 ordered pair 则是二次不等式生成的
`TTSTAR_BILINEAR_PAIR_TERM`。两者类型不同；当前没有从 pair registry
线性逆聚合回每条 cut coefficient 的 theorem。

最终 gates：

```text
ORDERED_POST_TTSTAR_PAIR_DOMAIN = PASS_FORMULA
TPC18_DISPLAYED_PAIR_COEFFICIENT_WITH_B_ALIASES = PASS_FORMULA
SECOND_ROW_GAMMA_FROM_TTSTAR_EXPANSION = PASS_FORMULA
U_FROM_SUPPLIED_TPC32_93_PARENT_POLARIZATION = PASS_FORMULA
TPC93_SOURCE_CHILD_REINDEXING = PASS_L1_ON_SUPPLIED_RETAINED_OMEGA
CONCRETE_DUAL_ARCHIVED_ROW_CANDIDATE = PASS_ROW_ONLY
TPC32_TPC93_DERIVED_AFFINE_CHILD = PASS_DERIVED_L0_ONLY

ACTIVE_PRODUCTION_PAIR_OCCURRENCE = NOT_TESTABLE
FULL_LITERAL_PAIR_COEFFICIENT_MATERIALIZATION = NOT_TESTABLE
PAIR_COEFFICIENT_MATERIALIZATION_AND_NONZERO = NOT_TESTABLE
SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK = FAIL
NU_X_NORMALIZED_RETURN_TO_H1 = FAIL
H1_E_REPAIR = FAIL

PAIR_NATIVE_FORMULA_GATE = PASS
PAIR_NATIVE_ARCHITECTURE_REROUTE_CANDIDATE = OPEN
PAIR_NATIVE_PRODUCTION_REOPEN_TRIGGER = FAIL
PAIR_NATIVE_STRUCTURAL_REOPEN_TRIGGER = FAIL
pair_native_mathematical_reopen = false
tpc205_authorized = false
```

结论是：pair-native 路线没有被数学上关闭，但它不是现有 H1-E 的 repair；
它只作为需要新 registry、DAG/root 与 theorem-backed crosswalk 的
architecture reroute 存活。active support `A` 与 canonical/minimal
representation `M` 仍是独立 `NOT_TESTABLE` roots，即使未来补齐上述
crosswalk 也不会自动消失。H1 architecture、两个 O161 pointwise parents
与 global architecture 保持 `OPEN`。

## 13. TPC-205 的精确有限结论

用户后续显式授权的范围仅为：

```text
FINITE_PAIR_NATIVE_POST_TTSTAR_REGISTRY_AND_ARCHITECTURE_REROUTE_INTERFACE
```

授权是 workflow input，不是 theorem evidence；它没有让 production、
structural、arithmetic 或 `L2` reopen trigger 自动通过。TPC-205 的精确
分类、定理状态和裁决是：

```text
classification
  = PAIR_NATIVE_POST_TTSTAR_REGISTRY_INTERFACE_L1
theorem_status
  = PROVED_TYPED_INTERFACE_AND_FIRST_MISSING_L1
verdict
  = PAIR_NATIVE_ARCHITECTURE_REROUTE_INTERFACE_CERTIFIED_NOT_REOPENED
```

### 13.1 typed interface 与 declared-corpus 边界

TPC-205 区分四类不可互换的 relation：

```text
TTSTAR_BILINEAR_PAIR_TERM
LINEAR_CUT_TO_OCCURRENCE_EDGE
TPC93_RETAINED_SOURCE_ATOM
TPC93_SOURCE_CHILD
```

它冻结 42 个 required registry fields，并保持 `(alpha,gamma,j)` 为
ordered pair；不得作交换 quotient。`pair_record_id`、
`edge_instance_id` 与 `target_occurrence_id` 分离；formula support、
evaluated mask、coefficient evaluability 与 nonzero status 分离；
source、linear、quadratic TT-star 与 target-return normalization 分离。

17 个 source locks 支持该有限接口。当前 production count 为：

```text
production_pair_records = 0
scope = DECLARED_TPC205_REGISTRY_SOURCE_LOCK_CORPUS_ONLY
```

该零值不是全仓库、全历史或数学上的 nonexistence theorem。两个有限对象
分别严格标为：

```text
DUAL_SOURCE_LOCKED_ROW_PAIR_CANDIDATE = ROW_ONLY
TPC32_PRIMITIVE_FIXTURE_PLUS_TPC93_FORMULAS_DERIVED_L0_ONLY
  = DERIVED_L0_ONLY
```

它们只用于 `L0` regression，均不构成 production pair occurrence。
TPC-18 显示式 pair carrier 中的 `B` aliases 没有被解释性展开；完整
literal coefficient 仍是缺失字段。TPC-18 pair 也没有被强行等同为
TPC-32/TPC-93 parent，故 `pair -> omega` 仍为 `FAIL`。

### 13.2 normalization 与 loss 防火墙

归档字符串 `"nu_X"` 只保留为 scope label，不是已供应的数值 scalar。
若未来 theorem 供应乘法 scalar `c_X`，当前只许可条件式

```text
|c_X T_D|^2 <= C_W |c_X|^2 J(E_D+C_D^off).
```

17 行 loss ledger 中，每条 TPC-18/25/32/93 bound 都保留各自 theorem
hypotheses；它们没有被组合到一个 production TPC-18 pair 上。TPC-93 的
weighted sign/coefficient reassembly 只在 physical squarefree 与
target-primitive support 上有效。generic hard remainder、
square-root return、full-block 和 endpoint reassembly 仍分别为
uncontrolled 或 unsupplied。

精确 first missing 是：

```text
SOURCE_LOCKED_POST_TTSTAR_ORDERED_PAIR_REGISTRY_WITH_COMPLETE_PAIR_COEFFICIENT_AND_GLOBAL_NORMALIZATION
```

其两个不可省略的 subgates 仍为：

```text
PAIR_NATIVE_POST_TTSTAR_ACTUAL_REGISTRY_WITH_FULL_LITERAL_SCOPE_AND_COEFFICIENT
TPC18_PAIR_TO_TPC93_RETAINED_SOURCE_ATOM_THEOREM_CROSSWALK
```

### 13.3 machine certificate、exploit review 与 PDF QA

active release 含 16 个文件、3 个 exact schemas、13 个 manifest pins、
17 个 source locks、2 个 `L0` fixtures、17 行 loss ledger 与 23 个
gates。独立 checker 不导入 builder 或 materializer，并执行：

```text
active-schema mutations = 12
regenerated-schema semantic mutations = 37
strict bool/int mutations = 6
```

额外 coordinated exploit review 对 regenerated-schema payload
39/39、source rebind 4/4、audit 11/11、L0 7/7、manifest 7/7 全部
fail closed；没有残留的 schema-only 绕过。builder、materializer 与
independent checker 均通过；三者的 `python -O` 路径均按设计 fail
closed。TPC-18/25/32/93/143/174/179/194/204 的相关回归均通过，且没有
改写其 active artifacts。

稳定 PDF 为 4 页 A4；逐页视觉核查、字体嵌入、页旋转、加密、表单与
构建 warning 检查均通过。其 SHA-256 为：

```text
b3596e207943132ad48e6a17cfd107421f02b521bc02f617615c860816a1dc1e
```

### 13.4 当前 gates、开放父节点与停止边界

```text
PAIR_NATIVE_FORMULA_GATE = PASS
ACTIVE_PRODUCTION_PAIR_OCCURRENCE = NOT_TESTABLE
FULL_LITERAL_PAIR_COEFFICIENT_MATERIALIZATION = NOT_TESTABLE
SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK = FAIL
NU_X_NORMALIZED_RETURN_TO_H1 = FAIL
H1_E_REPAIR = FAIL

PAIR_NATIVE_ARCHITECTURE_REROUTE_CANDIDATE = OPEN
PAIR_NATIVE_PRODUCTION_REOPEN_TRIGGER = FAIL
PAIR_NATIVE_STRUCTURAL_REOPEN_TRIGGER = FAIL
pair_native_mathematical_reopen = false
```

继续保持以下 cells 为 `STOP_SCOPED`：

```text
TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1
TPC204_DECLARED_PLAUSIBLE_PRODUCTION_CROSSWALK_CORPUS_V1
TPC18_25_32_93_194_SINGLE_CUT_OCCURRENCE_COMPOSITE_V1
TPC18_TPC93_POST_TTSTAR_PAIR_DIRECT_COMPOSITION_V1
```

这不是对 pair-native architecture 的全局关闭。active support `A` 与
canonical/minimal representation `M` 仍是独立 `NOT_TESTABLE` roots；
两个 O161 pointwise parents、H1 architecture 与 global architecture
保持 `OPEN`。fixed-atom credit 为 0，strict endpoint `1/400` 为
`UNPAID`，`L2=NONE`。该历史块此前的 TPC-206 未授权状态现由页首和
第 14 节取代。

## 14. TPC-206 的精确有限结论

持续工作流授权下，本篇实际形成的有限定理范围仅为：

```text
FINITE_SELECTED_LINEAGE_13_OF_42_PROJECTION_AND_FIRST_MISSING_D_THEOREM
```

它的精确分类、定理状态和裁决是：

```text
classification
  = PAIR_NATIVE_SELECTED_LINEAGE_PROJECTION_L1
theorem_status
  = PROVED_SELECTED_SOURCE_LOCKED_13_OF_42_PROJECTION_AND_FIRST_MISSING_D_L1
verdict
  = SELECTED_SOURCE_LOCKED_13_OF_42_PAIR_REGISTRY_PROJECTION_CERTIFIED_NOT_REOPENED
```

### 14.1 selected graph 与 13/42 closure

选定 ordered pair 为：

```text
alpha = (103,1)
gamma = (107,1)
j = 5
X = 512
h0 = 2
```

显式 `DECLARED_TPC206_SELECTED_103_107_LINEAGE_GRAPH_V1` 由 6 个
source records、4 个 locked typed derivation nodes 和 12 条 dependency
edges 构成。按 TPC-205 的 42-field contract，它精确物化：

```text
X, h0, delta, R, V, D0, L, K,
alpha, gamma, j, N_alpha(j), N_gamma(j)
```

所以：

```text
materialized fields = 13
missing fields = 29
first missing field = D
first missing one-based index = 9
full completions inside the explicit selected graph = 0
```

29 个缺口分为 8 个 identity/packet fields、5 个 ordered-pair fields、
12 个 source/child fields 和 4 个 normalization fields。父级 first
missing 仍是：

```text
SOURCE_LOCKED_POST_TTSTAR_ORDERED_PAIR_REGISTRY_WITH_COMPLETE_PAIR_COEFFICIENT_AND_GLOBAL_NORMALIZATION
```

selected graph 内更细的 first missing semantic 是：

```text
SOURCE_LOCKED_TPC18_OPENED_D_PACKET_LINEAGE_FOR_SELECTED_ORDERED_PAIR
```

上述 `0` 和 first missing 只对显式 selected graph 成立。TPC-206 没有
审核整个仓库中的所有潜在 join，因此：

```text
corpus-wide maximum materialized fields = null
corpus-wide full-join count = null
CORPUS_WIDE_MAXIMALITY = NOT_TESTABLE
```

TPC-32/TPC-93 的独立 `L0` fixture 在自己的谱系里暴露 14 个 contract
slots；它不能拼接进 selected 103/107 graph，也直接排除了把 13 误读成
corpus-wide maximum。

### 14.2 source chain 与符号防火墙

六条选定 source records 由 TPC-133 的两行，经 TPC-134 path rows，
再到 TPC-136 cut rows；两条 cut 都是
`FRONTIER_UNMAPPED/NO_TAIL_ROOM`。manifest 给出的
`delta=1/4` 是在 `X=512` 上、通过 866-row JSONL certificate 锁定的
chosen-manifest provenance lift；它不是从单行唯一恢复的参数，也不是
cross-scale packet schedule。

必须保持三个不可改写的 typed firewalls：

```text
Q_133 = floor(512^(1/4)) = 4  ->  R_18 = 4
Q_18 = L D                    ->  missing

native divisor d = 1          != opened dyadic scale D
native row index k = 5=d*j    != dyadic block scale K = 8
```

其中 `L=64`、`K=8`，两条 target values 为 517 和 537。
`pair_record_id`、edge instance ID 与 target occurrence ID 均仍为
`null`。这个 projection ID 是非 production 的独立标识，不得伪装成
actual pair registry occurrence。

### 14.3 gate、STOP_SCOPED 与开放架构

TPC-206 没有证明 active production occurrence、pair-to-`omega`
crosswalk、global normalization 或 H1-E repair。当前边界为：

```text
ACTIVE_PRODUCTION_PAIR_OCCURRENCE = NOT_TESTABLE
CORPUS_WIDE_MAXIMALITY = NOT_TESTABLE
SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK = FAIL
GLOBAL_NORMALIZATION_RETURN = FAIL
H1_E_REPAIR = FAIL
pair_native_mathematical_reopen = false
```

新增 cell：

```text
DECLARED_TPC206_SELECTED_103_107_LINEAGE_GRAPH_V1=STOP_SCOPED
```

TPC193 V1、TPC204 V1、singleton-cut composite 与
TPC18/TPC93 direct-composition 四个旧 cells 继续 `STOP_SCOPED`。
这不是 pair-native architecture 的全局关闭。pair-native reroute、
两个 O161 pointwise parents、H1 architecture 与 global architecture
保持 `OPEN`；fixed-atom credit 为 0，strict endpoint `1/400` 为
`UNPAID`，`L2=NONE`。

### 14.4 certificate、exploit review 与 PDF QA

active release 含 14 个文件、2 个 exact schemas、11 个 manifest pins
和 29 个 source locks。冻结 archive closure 为 34 refs、28 tips、
12,203 个 Git objects；严格 RFC-8259 `.json` 共有 1,707 个可解析文件
和 17 个因 `NaN`/`Infinity` 被拒文件。该 archive census 只作
reopen-trigger context，不是 JSONL/TeX semantic census，也不支持
corpus-wide maximality。

独立 checker 不导入 builder 或 materializer。12 个 base、52 个
semantic、12 个 strict bool/int mutation rows，共 76 行全部 fail
closed；针对 coordinated payload/schema/audit rewrite 的复测为
`accepted=0, rejected=76`。manifest 的 11/11 bytes 与 SHA-256 新鲜，
但它只是 repository-review pin，不是外部签名。三个正常 `--check`
均通过，三个 `python -O` 入口均按设计非零失败。

稳定 PDF 为 4 页 A4，逐页视觉核查、字体嵌入和构建 warning 检查通过；
SHA-256 为：

```text
e6a3ee6df0492daa2aae86de47040e8b0d5f8c75a7abc91208601f945d3bb082
```

## 15. 2026-07-31 的三项不编号 reopen-trigger 审计

### 15.1 selected 103/107 opened-`D` attachment

执行：

```text
PAIR_NATIVE_SELECTED_LINEAGE_OPENED_D_ATTACHMENT_FEASIBILITY_AUDIT
```

八条 selected child paths 恰落在四个共同 blocks
`(jL,jK)=(6,2),(6,3),(7,2),(7,3)` 的两侧。四条为 `K_TOO_LOW`，
四条为 `NO_TAIL_ROOM`；八条 TPC-136 cut 全是
`FRONTIER_UNMAPPED`。TPC-143 的 actual map edges 为 0，
TPC-153 的 actual completion 全为 `NOT_PRESENT`，TPC-154 的
theorem-backed actual provenance 为 0。reachable-history 没有隐藏的
selected opened-`D` record 或 joint packet locator。

因此八个 attachment 字段仍全部缺失：

```text
D, J, Q, T, U0, G_X_row, packet_id, source_locator
```

closure 保持 `13/42`，首缺仍是 `D`、one-based index 9。若反事实地先
给出合法 attachment，TPC-18 support 只说明唯一相容 `D_open=1`，进而
`J=K/D=8`、`Q_18=LD=64`；这不是字段填充。尤其禁止
`d=1 -> D=1`、`D0=0 -> D=0`、`Q_133=4 -> Q_18=4`。

```text
classification =
  PAIR_NATIVE_SELECTED_LINEAGE_OPENED_D_ATTACHMENT_AUDIT_L1
theorem_status =
  PROVED_DECLARED_SELECTED_103_107_ALL_CHILD_NO_LEGAL_TPC18_OPENED_D_ATTACHMENT_L1
verdict =
  DECLARED_SELECTED_103_107_OPENED_D_ATTACHMENT_FAIL_CLOSED_STOP_SCOPED_NOT_REOPENED
```

### 15.2 literal `B_alpha B_gamma` coefficient expansion

执行：

```text
PAIR_NATIVE_LITERAL_TTSTAR_COEFFICIENT_EXPANSION_AUDIT
```

TPC-18 只允许抽象模板

```text
B_i(j)=omega_D(d_i) psi(ell_i/L) W(ell_i d_i j/X)
       psi(d_i j/K) xi(d_i,j)
```

以及外部的两个 `mu`、两个 `log ell`、两个 `r_R(N)` 因子。它没有冻结
selected/common-`T_D` packet、`omega_D` partition member、cutoff function
instances 或 joint mask。TPC-25 也只给函数类型族。TPC-133 的两条
single-row AST 属于另一 TPC-15 packet；TPC-134 的
`tpc134-exp-bump-orbit-normalization-v1` 只是 block-compiler edge
multiplier。把两条 AST 相乘、按函数名合并或把 edge multiplier 重命名
为 TPC-18 `B_i` 都不是 theorem-backed lineage edge。

第一项 literal 缺失为：

```text
OPENED_D_PARTITION_MEMBER_SOURCE_ID + D + omega_D(d_alpha)
```

其后还缺 gamma 侧、source cutoff、`W` crosswalk、`k` cutoff、`xi`、
joint mask/locator 与 nonzero status。故：

```text
theorem_status =
  ABSTRACT_TPC18_ORDERED_PAIR_B_ALIAS_EXPANSION_TEMPLATE_ONLY_L1
verdict =
  SELECTED_103_107_LITERAL_PAIR_COEFFICIENT_CROSSWALK_FAIL_CLOSED_NOT_REOPENED
FULL_LITERAL_PAIR_COEFFICIENT_MATERIALIZATION = NOT_TESTABLE
```

closure 仍为 `13/42`，首缺仍为 `D`。

### 15.3 O161 bad-endpoint named-atom shadow increment

执行：

```text
O161_BAD_ENDPOINT_NAMED_ATOM_SHADOW_INCREMENT_THEOREM_AUDIT
```

合法的 local-increment reduction 已冻结。令
`J=ceil(A log_2 log X)`；对同一 actual packet 的每个 prescribed `T`
与每个 `N_j=T/2^j in E_X^star`，所需新 theorem 必须直接给出

```text
q=as,  t(z)=ad+qz,
c_z=mu(d+s z)mu(u+a z),  su-ad=2,

(q/N_j) |sum_{N_j<t(z)<=2N_j} c_z rho_star(z)|
  <= C X^(-sigma)
```

其中 named `rho_star`、actual active support、exact `(T,j)` schedule、
共同 `X/N/q` ranges、uniform `C`、positive `sigma`、normalization
attachment 和完整 physical-loss ledger 必须属于同一 source-locked
record。local `q/N_j` block 与 O161 cumulative `q/T` object 不同；唯一
合法桥是 TPC-159 exact telescoping，并在求和前乘
`N_j/T=2^(-j)`。

权威 gate-order 的首阻断是：

```text
PRESCRIBED_BAD_ENDPOINT_ATOM_HAS_NO_SOURCE_LOCKED_VALUE
```

TPC-180 仍有 0 条 value-bearing named-phase record 和 0 条 production
packet-coordinate row。即使反事实补齐 atom/schedule，第一项算术阻断
仍是：

```text
POINTWISE_NAMED_ATOM_Q_OVER_N_POSITIVE_X_POWER_LOCAL_INCREMENT
ON_SCHEDULED_E_X_STAR_ANCESTORS
```

TPC-149/TT26 恰只控制 `E_X^star` 外的 terminal block，并且只有
log-power saving；TPC-159 只在 dyadic shadow 外累积；TPC-167/169 是
phase `L2`；TPC-186 是代数 reduction；TPC-187 是 size-only
`STOP_SCOPED`。TPC-202 审核的 Menon 2026 source 仍分别平均 interval
origin 或 shifts。补充 primary screen 的 arXiv:2204.03754 只含单个
Möbius/nilsequence，arXiv:2506.08787 是不同的多变量几何；均未提供
prescribed determinant-two two-Möbius increment。它们不被加入
TPC-193 V1 source universe。

六轴中只有 abstract actual-core carrier 通过；named atom、bad-shadow
endpoint、deterministic all-scale、positive fixed-`X` power 和 actual
active support 全部失败或 `NOT_TESTABLE`。good blocks 仍只有 log
saving，TPC-159 tail 为 `2^(-J)+q/T`；physical good/bad variation、
phase return 与 four-sign reconnection 均未知。

```text
formula_gate = PASS_L1_REDUCTION
theorem_production_gate = FAIL_CLOSED
verdict = O161_BAD_ENDPOINT_TRIGGER_FAIL_CLOSED_PARENT_OPEN_NOT_REOPENED
TPC207_TRIGGER = NO
```

### 15.4 archive 与 checker exploit review

O161 reachable-history 扫描覆盖 1,940 个 TPC text blobs、
72,608,764 bytes；57 个相关命中中没有正向 theorem-backed fixed-atom
increment 或 local-occurrence edge。四个 historical-only 命中都是旧
TPC-194/203 的 `NOT_TESTABLE/STOP_SCOPED` 版本。

审计发现 TPC-184/189 checker 原先以 Python `assert` 承担关键验证，
`python -O --check` 会错误放行，且只读取预填 mutation verdict。现已
改为显式 `ValueError` gate、实际加载 closed payload/audit schemas，
并现场执行各 8 个 mutation；正常与 `python -O -B` 四个入口均通过。
这只加固验证器，不改变两篇论文的 `TARGET_WELL_TYPED_OPEN` 数学裁决。

### 15.5 边界与下一路线

本轮没有 theorem-state reopen，因此没有创建 TPC-207。
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1` 与第 6 节全部精确
cells 继续 `STOP_SCOPED`。两个 O161 parents、pair-native reroute、
H1 architecture 与 global architecture 继续 `OPEN`；fixed-atom
credit 为 0，strict `1/400` 为 `UNPAID`，`L2=NONE`。

无需单独授权的下一项有限审计是：

```text
CORPUS_WIDE_SOURCE_BACKED_LOCAL_OCCURRENCE_EDGE_FAMILY_AUDIT
```

它只在 TPC-206 selected graph 之外寻找真正 theorem-backed 的 actual
local-occurrence edge family。archive key、formal/shadow row、
TPC-143/153 的零边或形式链、synthetic witness、旧 singleton-cut
`STOP_SCOPED` cell 的包装都不合格。只有同一 source-locked edge family
连同 exact occurrence、schedule、ranges、normalization 与 loss ledger
真实形成时，才可讨论 TPC-207。

## 16. 全仓 source-backed local-occurrence-edge family 审计

### 16.1 精确审计范围与同记录合同

本轮执行的不编号 gate 为：

```text
CORPUS_WIDE_SOURCE_BACKED_LOCAL_OCCURRENCE_EDGE_FAMILY_AUDIT
```

冻结 paper corpus 的快照为：

```text
023ccb5959e35b96673117b76add3dcbc3987aca
```

该快照的 `papers/` 恰有 TPC-1--206 各一目录、各一 `main.tex` 与
`README.md`，无缺号或重号。审计同时覆盖所有 refs 可达的、路径以
`papers/tpc-` 开头且扩展名属于
`.py/.json/.jsonl/.md/.tex/.csv` 的 distinct blobs：

```text
reachable blobs = 1940
reachable bytes = 72619961
blob OIDs present at current HEAD = 1917
historical-only blob OIDs = 23
```

这是一项 finite lexical + typed-contract + semantic-candidate audit，
不是所有数学表述、所有外部文献或所有未来 source universe 的
nonexistence theorem。历史草稿也不因仍可达而自动取得 active production
theorem 身份；扫描历史只用于排除“已有但被当前树漏掉”的正向 candidate。

TPC-173 的最小 H1 edge 合同仍要求同一 source-locked record 同时给出：

```text
source path + canonical hash
resolving theorem locator
resolving formula locator
nonempty derivation AST
literal actual-local-occurrence-edge conclusion
five-field production cut address (ell,k,native_d,jL,jK)
exact nonzero rational edge weight
fixed h0=2 lineage
physical-normalization lineage
```

本轮 reopen gate 还逐项要求 exact actual occurrence identity、
packet/scale schedule、共同 ranges、具有公式语义的 normalization，以及
完整且不重复的 physical-loss ledger。archive key 只能作地址；
formal/shadow row、relation-type 名称、synthetic witness、空 family 与
跨 lineage 数值相等都不能补字段。

### 16.2 精确 census 与 near-candidate 排除

TPC-173 已冻结的 TPC-133--172 四十篇保持：

```text
MAPPED_DISQUALIFIED files = 30
REVIEWED_NO_CANDIDATE files = 10
NOT_MAPPED_YET files = 0
QUALIFYING files = 0
mapped claim records = 32
qualifying claim records = 0
```

其余 166 篇按互斥 source 层分为：

```text
TPC-1--132 pre-cut legacy = 132
TPC-173--179 H1 inventory/schema/extraction layer = 7
TPC-180--193 phase/fixed-atom/direct layer = 14
TPC-194--204 direct/reduction/barrier/audit layer = 11
TPC-205 pair-native interface = 1
TPC-206 selected projection = 1
```

pre-cut legacy 没有在同一 record 中形成具有 TPC-164/TPC-174 语义的
五字段 production source-cut address；phase/direct 对象不是 linear
cut-to-occurrence relation；TPC-205 的
`LINEAR_CUT_TO_OCCURRENCE_EDGE` 只是 relation type，production rows
为 0；TPC-206 的 selected graph 按本 gate 排除，其 nonselected
comparison fixture 仍是 `DERIVED_L0_ONLY` 且
`production_occurrence=false`。

对当前 HEAD 中 TPC-1--206 的 tracked、非-schema `.json/.jsonl`
再作结构化 census：

```text
files = 228
parse errors = 0
audited raw key instances = 26947 in 22 files
nonempty signal instances = 9001 in 7 files
generic occurrence_id instances = 26
physical_occurrence_id instances = 8973
actual_occurrence_id instances = 2
other positive/true/nonempty edge signals = 0
```

全部非空 signal 都被其自身 provenance 排除：

- TPC-141 的 14 个 generic `occurrence_id` 是 integration/ledger stage
  tokens，不是 physical actual edges；
- TPC-143 的 2,988 条 obligations 全部满足
  `actual_map_edges=[]`；TPC-145 的 `actual_occurrence_edges` 与
  `actual_stage_edges` 也都为空；TPC-163 的 13 类 production
  crosswalk coverage 全为 0，`theorem_backed_edge_count=0`；
- TPC-153 的 2,988 条 shadow rows 的 `actual_occurrence_id` 全为
  `null`；其两条最接近 claim 虽有 weight \(1\)、`h0=2` 与 `nu_X`
  lineage，但 theorem conclusion 仍只是 shadow；
- TPC-154 有 2,989 条 completion records、8,967 条 formal edge rows
  与 8,967 个唯一 `FORMAL_ONLY` physical IDs；其中 8,964 条来自当前
  production archive 的自由形式补全、3 条来自 synthetic policy
  regression，且 8,967 条全部显式满足
  `theorem_backed_actual_provenance=false`；
- TPC-155 只有 3 条 `SYNTHETIC_L0_ONLY` occurrence rows；
- TPC-174 只有 2 条 synthetic edges 与两个
  `synthetic-occurrence-{a,b}` IDs，source path/hash、theorem locator
  与 formula locator 均为空；
- TPC-205 的 ID 字符串是接口语义占位，production pair records 为 0；
  TPC-206 的 pair/edge/target occurrence IDs 为 `null`。

reachable-history 中没有 historical-only occurrence-ID-field blob，也
没有 historical-only positive candidate。严格 same-record screen 在
current 与 historical-only 两侧均为 0。

独立 exploit review 对 TPC-143/153/154/155/173/174/175 的七个
`python -O -B --check` 入口全部复核通过，未发现 `assert` 型优化绕过；
TPC-155/174 的关键 integer/fraction 路径也严格排除 bool-as-int。
同时保留以下信任边界：TPC-173 的 qualification flags 未被 schema
强制为 strict bool，TPC-174 不执行外部 theorem truth 或完整
source-label resolution，TPC-175 的 standalone zero-count validator
存在 `False == 0` 型混淆。deterministic rebuild 可阻止 artifact-only
篡改，不能把 coordinated producer/schema/source rewrite 变成外部定理
证明。因此本轮裁决建立在独立 raw census 与逐 source claim 审核上，
不把这些 checker 单独当作 theorem evidence。

因此同记录 gate ledger 为：

```text
source theorem with literal actual-edge conclusion = 0
production actual-occurrence identities = 0
exact nonzero edge/conservation on an actual carrier = 0
same-record packet schedule = 0
same-record ranges = 0
same-record physical normalization = 0
same-record complete physical-loss ledger = 0
complete qualifying H1 local-edge records = 0
```

### 16.3 裁决、停止边界与开放父节点

首致命阻断为：

```text
SOURCE_LOCKED_THEOREM_WITH_ACTUAL_LOCAL_OCCURRENCE_EDGE_CONCLUSION
  = ABSENT
```

它早于 occurrence ID、edge weight、schedule、ranges、normalization 与
loss ledger。故：

```text
classification =
  CORPUS_WIDE_SOURCE_BACKED_LOCAL_OCCURRENCE_EDGE_FAMILY_AUDIT_L1

theorem_status =
  PROVED_DECLARED_TPC1_206_AND_REACHABLE_HISTORY_ZERO_QUALIFYING
  H1_SOURCE_BACKED_LOCAL_OCCURRENCE_EDGE_RECORDS_L1_SCOPED

verdict =
  DECLARED_TPC1_206_REACHABLE_LOCAL_EDGE_CORPUS_V2
  FAIL_CLOSED_STOP_SCOPED_NOT_REOPENED

H1.source_backed_local_occurrence_edge_family = NOT_TESTABLE
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

新增且仅新增：

```text
DECLARED_TPC1_206_REACHABLE_LOCAL_OCCURRENCE_EDGE_SOURCE_CORPUS_V2
  = STOP_SCOPED
```

该 cell 只停止从上述 snapshot 与可达历史重新包装出 production H1 edge；
它不是数学不存在性定理，不关闭新增 source theorem、外部新增 primary
source 或独立 architecture reroute。第 6 节全部旧 cells（尤其
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`）继续精确
`STOP_SCOPED`。

两个 O161 parents、pair-native reroute、H1 architecture 与 global
architecture 继续 `OPEN`。active support 与 canonical/minimal
representation 是 actual carrier 之后的独立 roots；在 carrier 为空时
优先审它们只会继续得到 vacuous `NOT_TESTABLE`。fixed-atom credit 为 0，
strict `1/400` 为 `UNPAID`，`L2=NONE`。

### 16.4 下一有限路线

最直接触碰首缺、且不再重复空 corpus scan 的下一关选为：

```text
ONE_PACKET_SOURCE_FORWARD_PRECUT_TO_ACTUAL_OCCURRENCE_LINEAGE_CONSTRUCTION_GATE
```

它必须选一个 source-locked named upstream physical occurrence，沿正向
map 推到一个具体 TPC-136 cut；禁止从已经丢字段的 cut archive 逆猜
occurrence。一次通过必须在同一 source lock 下同时形成：

```text
named actual physical occurrence ID
literal five-field production cut address
exact nonzero edge weight and per-cut conservation
fixed h0=2
exact packet schedule and parameter ranges
physical normalization with formula semantics
complete nonduplicated loss ledger
```

若该 gate 通过，它会直接产生第一条 production TPC-174 witness，届时
才允许讨论 TPC-207。若首步即证明当前语料没有可选的 named upstream
physical occurrence，则 fail closed 并转入仍开放的备选有限路线：

```text
UNNUMBERED_CORPUS_WIDE_NONSELECTED_PAIR_NATIVE_CONNECTED_LINEAGE_JOIN_CENSUS
```

备选路线只审 103/107 之外、同一 connected lineage 的 ordered row
pairs，禁止 external L0 donor 与 cross-lineage splice，并始终保持
pair reroute 与 H1 linear edge 类型分离。

## 17. one-packet source-forward 与 nonselected pair fallback 审计

### 17.1 冻结语料与 Gate 0 合同

本轮在 source snapshot

```text
3dd4fe67977380289f68dd644cf4d2dba60456b5
```

上先执行：

```text
ONE_PACKET_SOURCE_FORWARD_PRECUT_TO_ACTUAL_OCCURRENCE_LINEAGE_CONSTRUCTION_GATE
```

候选主语料、只按实际 theorem/interface 调用追踪的直接依赖，以及用于
冻结 actual-occurrence 类型边界的 contracts 分别为：

```text
U_main =
{TPC-18, 32, 93, 117, 119, 123, 124, 131, 133, 134, 135, 136}

U_dep =
{TPC-15, 16, 17, 25, 29, 30, 31, 33, 86, 92,
 105, 107, 114, 116, 118, 121, 122, 125, 132}

U_contract =
{TPC-143--146, 153--155, 163--165, 173--175}
```

这是当前仓库的有限 source audit，不是数学上的全局不存在性声明。
`U_main` 的 12 个目录共有 112 个被审 source blobs；所有 refs 可达历史
没有补出该语料的 historical-only positive version。17 个非-schema
JSON/JSONL 均可解析。

Gate 0 要求先选出一个 source-locked、named actual physical
occurrence，再沿已证正向 map 推到具体 TPC-136 cut。它禁止：

```text
native/archive/path ID -> occurrence ID 的解释性改名
block/cumulative conservation -> per-cut occurrence-fibre conservation
symbolic psi path multiplier -> rational local-occurrence edge weight
从 lossy cut archive 逆猜 source occurrence
```

逐 source 类的精确近邻为：

- TPC-18 有真实 symmetric tail block 与 opened-`d` 线性公式，但
  block/row summand 没有独立 actual physical occurrence ID，也没有到
  TPC-136 cut 的 theorem-backed edge；
- TPC-32 有 actual row coefficient、row-pair carrier 与 ranges，但对象是
  二次 pair/orbit，不是一个线性 cut occurrence；
- TPC-93 对另行 supplied 的
  `omega=(L/R,alpha,gamma,j,u)` 有 exact source-child inverse，却没有
  production instance ID、packet ID、到 TPC-136 cut 的 crosswalk，且
  未 source-lock 到 `h0=2`；
- TPC-117 只给 range/residual certificate format，growing `B,w` 与
  stable physical row IDs 未提供；
- TPC-119/123/124 分别缺 complete canonical leaf archive、actual growing
  stage tables 与 actual growing `G,C,z,B`；
- TPC-131 给 occurrence-token/no-double-charge contract，但 sample tokens
  只是 finite regression，`actual_complete_physical_registry=false`；
- TPC-133--136 给完整 native/archive 正向结构链，却没有 actual physical
  occurrence 类型或 ID。

因此两类近邻的关键交集严格为空：

```text
{source-backed actual physical semantics + independent occurrence ID}
intersection
{TPC-119 -> 133 -> 134 -> 135 -> 136 forward lineage}
= empty
```

### 17.2 最近 concrete cut 与八轴结果

当前 committed archive 的结构闭合精确为：

```text
TPC-133 native rows = 866
TPC-133 -> TPC-134 parent-hash joins = 2988 / 2988
TPC-134 paths = 2988
TPC-134 -> TPC-135 block-key coverage = 2988 / 2988 over 26 keys
TPC-134 -> TPC-136 path-ID + upstream-hash joins = 2988 / 2988
TPC-136 unique five-field cuts = 2988
TPC-136 -> actual occurrence bridges = 0
```

TPC-136 的 2,988 个 cuts 全部为 `FRONTIER_UNMAPPED`：

```text
NO_TAIL_ROOM = 1495
L_TOO_LOW = 1020
K_TOO_LOW = 473
```

四张 downstream maps 的 domain 都为空、各缺 2,988 rows，source status
全部 `NOT_TESTABLE`。最近的一条可执行正向链冻结为：

```text
X=512, h0=2, delta=1/4, Q=4, U=V=2
native tuple = (ell,k,d) = (3,171,1)
native_id = X=512|h0=2|ell=3|k=171|d=1
physical_normalization tag = nu_X

TPC-134 child = (jL,jK,D0,type) = (1,7,0,TAIL)
TPC-136 cut kappa = (ell,k,native_d,jL,jK) = (3,171,1,1,7)
TPC-135 reason = L_TOO_LOW
TPC-136 terminal = FRONTIER_UNMAPPED
soft_theorem_source = null
native coefficient nonzero status = UNDECIDED
```

其 native coefficient 与 exact symbolic path term 为：

```text
c_X(3,171,1)
  = -Lambda(3) r_4(515) W(513/512)

path term
  = -Lambda(3) r_4(515) W(513/512)
      psi(3/2) psi(171/128)
```

`psi(3/2)psi(171/128)` 是 exact positive symbolic path multiplier，
并参与
`sum_(children of one native column) m = 1`。它不是 TPC-174 所需的
exact rational occurrence-edge `lambda`，而 native-column conservation
也不是 `sum_(actual occurrences over one cut) lambda = 1`。

八轴 ledger 为：

```text
named actual physical occurrence ID = FAIL
distinct local edge ID = FAIL
literal five-field cut = PASS
exact nonzero occurrence-edge / per-cut conservation = FAIL
h0=2 lineage = PARTIAL: native/cut only
packet schedule and ranges = PARTIAL: no same-lock physical occurrence
formula-semantic physical normalization = FAIL: nu_X is only a copied tag
complete nonduplicated physical-loss ledger = FAIL
```

首致命缺口因此是：

```text
SOURCE_LOCKED_NAMED_ACTUAL_PHYSICAL_OCCURRENCE_RECORD
  IN_THE_TPC119_TO_TPC136_FORWARD_LINEAGE
  = ABSENT
```

故：

```text
ONE_PACKET_SOURCE_FORWARD_PRECUT_TO_ACTUAL_OCCURRENCE_LINEAGE_GATE0
  = FAIL_CLOSED
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

### 17.3 自动 fallback：nonselected ordered-pair census

按第 16.4 节的预定 fallback，本轮随即执行：

```text
UNNUMBERED_CORPUS_WIDE_NONSELECTED_PAIR_NATIVE_CONNECTED_LINEAGE_JOIN_CENSUS
```

pair identity 定义为同一完整 packet scope 下的 ordered
`(alpha,gamma,j)`，其中 `j=k_alpha/d_alpha=k_gamma/d_gamma`；pair-block
instance 再附共同 `(jL,jK,D0=0)`。两条 row 都必须经 parent hash 与
upstream hash 正向 join 到同一 TAIL/FUM block。TPC-205 已冻结
`ordered_pair_quotient=FORBIDDEN`，故只排 exact selected orientation

```text
alpha=(103,1), gamma=(107,1), j=5
```

的全部 4 个共同 block instances；反向 `107 -> 103` 是独立
nonselected pair，必须保留。精确 census 为：

```text
native rows = 866
distinct j groups = 202
groups with at least two rows = 101
all ordered same-j row pairs before common-block screen = 15030

raw same-lineage pair identities after selected-orientation exclusion = 13227
raw common pair-block instances = 31868
raw instance reasons:
  NO_TAIL_ROOM = 14406
  K_TOO_LOW = 16666
  L_TOO_LOW = 796
```

严格 TPC-18 geometry pool 只取 `NO_TAIL_ROOM`：这里 `L>2R` 与
`K>2V` 已通过。`NO_TAIL_ROOM` 是 TPC-135 对 prefix cutoff `D0` 的
分类：当 `V=2` 时不存在正整数 `D0` 满足 `2D0<V`，故 archive 取
`D0=0`。它不是 TPC-18 uppercase opened dyadic `D`，也不证明
uppercase `D` 不存在。TPC-205 contract-order 的独立首缺仍是没有
source-locked locator 的 uppercase `D`。该 pool 为：

```text
strict ordered pair identities = 7157
strict pair-block instances = 14406
identity block multiplicity:
  1 block = 2780
  2 blocks = 2941
  4 blocks = 1436
```

全部 14,406 个 instances 并列满足 TPC-205 的 13/42 maximal closure：

```text
X, h0, delta, R, V, D0, L, K,
alpha, gamma, j, N_alpha, N_gamma
```

`R` 只按 TPC-206 已冻结的 typed `Q_133 -> R_18` alias 填入；不得把
`Q_133` 再偷渡为 `Q_18`。精确 first missing 是 field #9：

```text
D
blocker =
NO_SOURCE_LOCKED_TPC18_OPENED_D_SLICE_LOCATOR
native d is not opened uppercase D
```

因此：

```text
13/42 maximizer instances = 14406
13/42 maximizer identities = 7157
full 42-field completions = 0
pair/edge/target occurrence IDs = 0
production occurrences = 0
```

其中至少一侧 `Lambda(ell)` 已确定为零的 instances 有 13,142；余下
1,264 instances / 669 identities 也只表示两侧 Lambda leaves
potentially nonzero，仍缺 `W/r_R` 取值、joint mask、完整 coefficient
nonzero、pair occurrence 与 normalization return，不能提升为 active
candidate。determinant-two 子池有 2,054 instances / 968 identities；
再限两侧 Lambda leaves potentially nonzero 后只有 124 instances /
106 identities。

审计 ID 的 canonical digests 为：

```text
strict instances:
  count = 14406
  bytes = 759518
  sha256 = ceb4c93791ce1f8a88d2d6ba4adb05dcdc19df045272e3c7a423184f32bcd116

strict identities:
  count = 7157
  bytes = 269967
  sha256 = 167dcd24b0fa7380651719e1792eb1461c51be4ecec474778e162b334106b166
```

ID 使用 UTF-8 字典序、LF join 并带末尾 LF；instance ID 为完整 pair
identity 再附 `jL,jK,D0`。此 digest 冻结 census，不把 formal row
投影变成 production theorem。

### 17.4 schema、checker 与最终裁决

目标 current/history 中这些非空 ID key 的计数全部为零：

```text
actual_occurrence_id
physical_occurrence_id
occurrence_id
packet_id
parent_id / canonical_parent_id
stage_id
group_id / physical_group_id
edge_id / edge_instance_id
```

TPC-131 仅有 6 个 generic finite-regression labels，且
`actual_complete_physical_registry=false`。TPC-133/134/136 schemas 是
archive-shape schemas；`additionalProperties=false` 能拒绝偷偷塞入
occurrence 字段，却不能证明 occurrence。TPC-134 的 symbolic
`edge_multiplier_ast` 也不是 TPC-174 rational occurrence-edge。
TPC-136 对未来 `PROVED` map 的 validator 不解析外部 theorem truth，
因此 source-label self-attestation 仍是独立 trust boundary；当前四图
仍为 empty/`NOT_TESTABLE`。

平台复核为：

```text
TPC-133 normal and python -O --check = PASS
TPC-133 -> 134 semantic joins = 2988 / 2988
TPC-134 -> 136 semantic joins = 2988 / 2988
TPC-134/135 raw-byte archived SHA checks on LF checkout = FAIL_EOL_PIN
TPC-136 archived hash-chain check = FAIL_FROM_UPSTREAM_EOL_PIN
git diff on old artifacts = EMPTY
```

旧 pins 恰好是把当前 LF 文本转为 CRLF 后的 SHA-256；这是
EOL-sensitive raw-byte portability pin，不是公式或逐记录语义 join
漂移。本轮没有修改旧证书，也不把 semantic match 说成当前机器
hash-chain fully reproducible。TPC-173--179、TPC-184、TPC-189、
TPC-205 与 TPC-206 的 required checks 均通过。snapshot 新增的
RH-323/324 分别是 affine Gaussian probability model 与 folded physical
kernel/affine-leg remainder；两者没有 TPC cut、occurrence、Mobius 或
determinant-two source theorem，类型上不能 reopen 本 gate。发布前
rebase 新增的 `a39c434` 只修改 RH-324 的 joint-density support 实现与
测试，也没有改动 TPC corpus 或上述 theorem-state。

本轮最终 verdicts 为：

```text
ONE_PACKET_SOURCE_FORWARD_PRECUT_TO_ACTUAL_OCCURRENCE_LINEAGE_GATE0
  = FAIL_CLOSED_STOP_SCOPED_NOT_REOPENED

NONSELECTED_TPC18_GEOMETRY_ORDERED_PAIR_LINEAGE_JOIN
  = PROVED_FINITE_CORPUS_MAXIMUM_13_OF_42
    FIRST_MISSING_D
    ZERO_FULL_COMPLETIONS
    ZERO_PRODUCTION_OCCURRENCES
    STOP_SCOPED_NOT_REOPENED

TPC207_TRIGGER = NO
TPC207_CREATED = false
```

新增且仅新增第 6 节的两个 cells。第 6 节全部旧 cells，尤其
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`，继续原样
`STOP_SCOPED`。两个 O161 parents、pair-native reroute、H1 与 global
architecture 继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为
`UNPAID`，`L2=NONE`。

### 17.5 下一有限路线

pair census 已把当前唯一最接近 source-side 首缺的有限池从 14,406
instances 收紧到 124 个 determinant-two、two-Lambda-potential
instances。下一关冻结为：

```text
ONE_POSITIVE_DETERMINANT_TWO_NONSELECTED_PAIR_OPENED_D_PACKET_ATTACHMENT_GATE
```

按“先取 positive determinant two、再最大化同 identity 的 strict common
block 数、再最小化尺度与 block”的稳定规则，唯一首选 diagnostic seed
冻结为：

```text
X=512, h0=2, delta=1/4, R=4, V=2
alpha=(17,1), gamma=(16,1), j=33
jL=4, jK=5, D0=0
L=16, K=32
N_alpha=563, N_gamma=530

h0(m_alpha-m_gamma) = 2(17-16) = +2
```

该 ordered identity 另有共同 strict block `(4,6,0)`；冻结 `(4,5,0)`
是上述稳定规则的结果。两侧 `Lambda(17)` 与 `Lambda(16)` 均确切非零，
但 `r_R/W/B`、joint mask 与完整 pair coefficient nonzero 仍未证明。
source locators 为：

```text
alpha row:
  TPC-133 JSONL line 372
  integrity db32fb3628ac124285e65c7f144d1c6000f73777df832b2fdf7bea24e002ab56
gamma row:
  TPC-133 JSONL line 357
  integrity 91cc9c344379273f3463fb25717fe159a2b26e7ed8b07ee6be684c4650ee48ad

alpha path/cut:
  TPC-134 line 1283
  integrity 33d4e8370fcc718efe6b97011e90c7306c4f3edd2d5201a915ddd4b02fbe3cce
  TPC-136 line 1283
  integrity 5a8fd7a715dd473f6f2deb15989425bc7773b7b8b069e24ef9d462ccdcfeb404
gamma path/cut:
  TPC-134 line 1251
  integrity e5d704f9971160e7ae4533caa7829102940524e51aec0cd2dcfae740106296e9
  TPC-136 line 1251
  integrity c3e613844749c161f79fc8673eb8bd67c5339f5d03f161c64be6247af5270769
```

两条链都是 `TAIL/FRONTIER_UNMAPPED/NO_TAIL_ROOM`，
`soft_theorem_source=null`。它们是两个独立 row/path/cut locators，不是
一条 source-locked post-TT-star joint pair locator。

下一 gate 必须在这条具体 nonselected ordered pair 上找到实际 source
theorem，把同一 source lock 的 uppercase opened `D` slice 附到两条
row；只有如此才能合法导出 `J=K/D` 与 `Q_18=LD`。禁止：

```text
native d -> opened D
Q_133 -> Q_18
selected 103/107 stopped-cell repackaging
external L0 donor
cross-lineage splice
potentially nonzero Lambda -> nonzero full coefficient
pair-native object -> H1 linear occurrence edge
```

若首个候选仍没有 theorem-backed `D` attachment，则 fail closed 并冻结
对应 declared candidate cell；不得为了编号而补 schema。只有 source
theorem 同时提供 uppercase `D`、joint packet/source locator、literal
determinant-two coefficient、actual pair occurrence、formula-semantic
normalization 与完整 loss ledger，才可能改变 theorem state并讨论
TPC-207。

## 18. positive determinant-two seed carrier 与 mask 审计

### 18.1 冻结 gate、snapshot 与 formal archive projection

本轮在 source snapshot

```text
0a0dd19d04fb168132f1227758f906aed62c32e5
```

上执行：

```text
ONE_POSITIVE_DETERMINANT_TWO_NONSELECTED_PAIR_OPENED_D_PACKET_ATTACHMENT_GATE
```

冻结 seed 为：

```text
X=512, h0=2, delta=1/4, R=4, V=2
alpha=(ell_alpha,d_alpha)=(17,1), k_alpha=33
gamma=(ell_gamma,d_gamma)=(16,1), k_gamma=33
j=33
(jL,jK,D0)=(4,5,0)
L=16, K=32
N_alpha=563, N_gamma=530
h0(m_alpha-m_gamma)=2(17-16)=+2
```

两条 TPC-133 -> 134 -> 136 archive chains 的 parent/upstream joins 全部
精确通过：

```text
alpha:
  TPC-133 line 372
  db32fb3628ac124285e65c7f144d1c6000f73777df832b2fdf7bea24e002ab56
  TPC-134 line 1283
  33d4e8370fcc718efe6b97011e90c7306c4f3edd2d5201a915ddd4b02fbe3cce
  TPC-136 line 1283
  5a8fd7a715dd473f6f2deb15989425bc7773b7b8b069e24ef9d462ccdcfeb404

gamma:
  TPC-133 line 357
  91cc9c344379273f3463fb25717fe159a2b26e7ed8b07ee6be684c4650ee48ad
  TPC-134 line 1251
  e5d704f9971160e7ae4533caa7829102940524e51aec0cd2dcfae740106296e9
  TPC-136 line 1251
  c3e613844749c161f79fc8673eb8bd67c5339f5d03f161c64be6247af5270769
```

因此 TPC-205 的 field-order archive projection 仍形式 materialize
恰好 13/42：

```text
X, h0, delta, R, V, D0, L, K,
alpha, gamma, j, N_alpha, N_gamma
```

其 contract-order first missing 仍是 field #9 uppercase `D`。这个
`13/42` 只是 source-locked row/path/cut partial projection，不先验保证
该 pair 属于 TPC-18 的求和 carrier。

### 18.2 Gate prerequisite 首先失败：`ell=16` 不是 prime source

TPC-133 的 generator 有意枚举 support-envelope native tuples；其
coefficient AST 使用 `Lambda(ell)`，不要求 `ell` 本身为 prime。因此
`ell=16=2^4` 是合法 TPC-133 native record，并且

```text
Lambda(16)=log 2 != 0.
```

但 TPC-18 在任何 quadraticization 之前先执行 prime-source reduction。
精确 source locators 为：

```text
TPC-18 tail-interface.tex:61--94
  source prime powers are removed before either quadraticization
  lambda_ell = (log ell) 1_(ell prime) psi(ell/L)
  sha256 = 5f50b44fde7e672b28aeb45b1b53e95f90c26bb8d35052081fa3a7e419712389

TPC-18 opened-d-dispersion.tex:17--56
  T_D, J=K/D, Q=LD
  prime and support restrictions remain understood
  sha256 = 36249c8baa2495034acabeb0ba7d5a5f665f2d536b605e9691e2e420e399f1f8

TPC-25 provenance.tex:22--55
  actual row family requires ell in [L/2,2L] prime
  sha256 = 21382acf28d8fc3d3cff499cd767075206ba9e2d24913e95414138b4317f0f00

TPC-32 physical-matched-shell.tex:42--48
  physical opened rows again require ell_alpha prime
  sha256 = b2c3b2b0312db64af5b3151402be929c1671429c1376fe24454a78b4c60d90bd
```

TPC-17 也在 assembled-prefix proof 中整体移除
`ell=p^a, a>=2` 后才 restriction to primes。TPC-93 只 export 另行
supplied、retained 的同一 TPC-32 source atom；其 source-child bijection
不会恢复被 prime-source reduction 移除的 row。

所以本 seed 上：

```text
lambda_17 = log 17 * psi(17/L)
lambda_16 = 0
```

archive determinant `+2` 是正确整数恒等式，却不能产生一个非零 TPC-18
pair term。Gate prerequisite ledger 为：

```text
alpha TPC-133 native membership = PASS
gamma TPC-133 native membership = PASS
alpha TPC-18 prime-source membership = PASS
gamma TPC-18 prime-source membership = FAIL
archive determinant = PASS:+2
joint TPC-18 ordered-pair carrier = FAIL
TPC-18 pair coefficient = ZERO_FROM_LAMBDA_16
```

首致命缺口因此早于 uppercase `D`：

```text
TPC18_PRIME_SOURCE_CARRIER_MEMBERSHIP
  (gamma=(ell=16,d=1))
  = FAIL
```

`Lambda(ell)!=0` 只说明 `ell` 是 prime power，不能解释为
`ell is prime`。这正是原 124-instance candidate filter 必须补上的
类型防火墙。

### 18.3 `D0`/`D`、42-field ledger 与 schema 防偷渡

TPC-135 的 `NO_TAIL_ROOM` 是 prefix-cutoff 判据：

```text
V=2
no positive integer D0 satisfies 2D0<V
therefore canonical D0=0
```

它与 TPC-18 uppercase opened dyadic `D` 不同。对原 seed 的
`d_alpha=d_gamma=1`，公式 support 与 `D=1` 相容，但没有 source-backed
named slice locator；且 carrier 已在 prime-source prerequisite 失败。
故不得把 `NO_TAIL_ROOM` 说成 uppercase `D` 不存在，也不得用 `D0=0`
填写 `D`。

两种 first-missing 必须分开：

```text
formal 42-field contract-order first missing = D at index 9
gate prerequisite first fatal = gamma prime-source membership
```

在当前 exact seed/block selector 下，TPC-133/134/136/143/153/154
各只有两条 single-side records，共 12 条；同时含两个 native IDs 的
joint record 为 0。以下 production fields 的 source-backed count 也
全部为 0：

```text
uppercase D
J
Q_18
packet_id
joint source_locator
pair_record_id
edge_instance_id
target_occurrence_id
```

TPC-143 的 `actual_map_edges=[]`、status 为 `NOT_TESTABLE`；TPC-153 的
`actual_occurrence_id=null` 且 `is_actual_occurrence=false`；TPC-154
匹配到的 physical IDs、formal edge IDs 与 ledger tokens 全部
`FORMAL_ONLY`，并满足
`theorem_backed_actual_provenance=false`。它们不能补 actual pair 或
loss ledger。`Q=4` 仍只是 TPC-133 `r_Q` 的 finite-model scope，并非
`Q_18=LD`；`nu_X` 仍只是 lineage label，不是 scalar normalization。

TPC-205/206 的 strict wrappers 按 exact type identity 检查，并已有
bool/int 与 semantic mutations，能拒绝：

```text
native d -> uppercase D
Q_133 -> Q_18
native/path/cut ID -> pair or occurrence ID
formal/shadow -> actual
nu_X label -> scalar normalization
one normalization -> four normalization fields
```

TPC-133/134/136 的遗留内层 validator 仍有 `isinstance`/equality
bool-int trust boundary；TPC-136 future map validator 也不验证外部
theorem truth，只检查 `PROVED` label、非空 source 与 total domain。
当前固定 artifacts 由 integrity/source pins 与 TPC-205/206 strict
wrappers 保护，且四张 downstream maps 仍为空、`NOT_TESTABLE`。因此
不能用 schema self-attestation 把本 seed 从 13/42 提升到 14/42。

### 18.4 新增 RH sources 与历史 screen

发布基线之后新增：

```text
01e56b9  RH-325 moving-order Duhamel criterion
437d318  RH-326 parity-renormalized alias identity
0a0dd19  RH-326 certification-boundary tightening
```

RH-325 的对象是 nonautonomous Markov path law 与 abstract trace
Duhamel；其 `mu(dx0)` 是 probability entrance measure，不是 Möbius
function。RH-326 的对象是 Hardy-scaled noisy Markov
trace/counterloop first-alias packet；其中 lowercase
`d_(sigma,k)` 是 clearance ratio，不是 TPC divisor scale。

两篇对本 gate 的逐轴结果全部为 `ABSENT/TYPE_MISMATCH`：

```text
uppercase opened D
J=K/D and Q_18=LD
joint post-TT-star pair locator
literal determinant-two Möbius coefficient
actual pair occurrence
TPC packet schedule/ranges
TPC formula-semantic normalization
complete TPC physical-loss ledger
```

RH-326 还显式保持 local probability-to-raw-trace、neighboring shell、
joint trace law、full-trace replacement 与 second physical leg 为
false/open；`0a0dd19` 把 decimal no-go 收紧为 conditional，普通浮点值
不是 interval certificate。`1580823..0a0dd19` 没有 `tpc-*` 或
`TPC_HANDOFF.md` source 改动，也没有新的 TPC theorem source。

### 18.5 both-prime 修正池与 primitive-mask obstruction

把先前 124 instances / 106 identities 的
both-`Lambda`-prime-power-potential pool 改为真正的 source-prime
筛选后：

```text
both ell prime, |det|=2:
  28 instances / 28 identities

both ell prime, det=+2:
  14 instances / 14 identities
```

对 `h0=2` 与 `ell_alpha,ell_gamma>2` prime，两个 source primes 都是
奇数。`det=+2` 等价于

```text
ell_alpha d_alpha - ell_gamma d_gamma = 1.
```

故 `d_alpha,d_gamma` 奇偶性相反。当前 `V=2` 且 `d<=V`，所以每个
positive instance 恰有一个 divisor row 等于 2。于是对 TPC-18/TPC-25
的 primitive mask：

```text
gcd(d*j,h0)=1
```

至少一侧恒失败。14/14 positive instances 的 joint primitive-mask
value 都为 0。canonical ID digest 为：

```text
count = 14
bytes = 963
sha256 = b366115151f5609275ab2483100e968ed4e8b78a67f16f1da0393a3f2fe0d8b5
primitive true = 0
primitive false = 14
```

该结论只停止当前 finite corpus 的 primitive-mask route。TPC-18
opened-`D` 公式也允许 formal constant mask，但 constant mask 不能仅因
“admissible”就改名为 actual physical packet；nonprimitive
`s=(k,h0)=2` endpoint route也是另一 theorem object。

按“positive determinant two、both prime、最小 scale/block/j”的稳定规则，
下一 diagnostic seed 为：

```text
X=512, h0=2, R=4, V=2
alpha=(ell=23,d=1,k=24)
gamma=(ell=11,d=2,k=48)
j=24
(jL,jK,D0)=(4,5,0)
L=16, K=32
m_alpha=23, m_gamma=22
N_alpha=554, N_gamma=530
h0(m_alpha-m_gamma)=2(23-22)=+2
```

其 exact locators 为：

```text
alpha:
  TPC-133 line 429
  b328ec79cf5c1ae88a675053fb9c76d46600d72a2aa36b5ae65a211ee42f599f
  TPC-134 line 1500
  d43e5c3f72be0c6eff2d48a7021892e3f079216395b0cfe981d6f1499c48203f
  TPC-136 line 1500
  7b7bdcdadf50b56bdb08d86ed465a410b24afaaef98f638b7d3ef373e86d62a0

gamma:
  TPC-133 line 283
  cef1da75b09f74ee50cca1f0470a3c2f05fdf99f9b7ccadd018edc4b727bf5a1
  TPC-134 line 963
  c527e8336cba6e0852513001aaba4cf2dba3b57949e298ec9287b2cef6631870
  TPC-136 line 963
  5d76d51cbde9c470e087311c93545285c5201ba721f6a1c21f66f480a77ee146
```

两条 source primes 与全部 parent/upstream joins 都通过。若一个同名
opened slice 同时包含 boundary rows `d=1,2`，support geometry 唯一强制
`D=1`，从而条件给出：

```text
J=K/D=32
Q_18=LD=16
```

但 support containment 不能证明 actual
`omega_1(1),omega_1(2)` 都非零，也不能产生 joint packet locator。更早
还必须决定同一 physical source lock 采用 primitive、constant，还是
nonprimitive endpoint mask/object；三者不得混同。

### 18.6 最终裁决与下一有限路线

本轮 gate verdict 为：

```text
ONE_POSITIVE_DETERMINANT_TWO_NONSELECTED_PAIR_OPENED_D_PACKET_ATTACHMENT_GATE
  = FAIL_CLOSED_AT_PRIME_SOURCE_CARRIER_MEMBERSHIP
    STOP_SCOPED_NOT_REOPENED

formal archive projection = 13/42
formal first missing = D at field 9
gate first fatal = GAMMA_ELL_16_NOT_PRIME
actual joint pair records = 0
production occurrences = 0
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

新增且仅新增第 6 节的两个 cells。第 6 节全部旧 cells，尤其
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`，继续原样
`STOP_SCOPED`。两个 O161 parents、pair-native reroute、H1 与 global
architecture 继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为
`UNPAID`，`L2=NONE`。

下一关冻结为：

```text
ONE_POSITIVE_DETERMINANT_TWO_PRIME_PRIME_MIXED_D_MASK_AND_OPENED_PACKET_ATTACHMENT_GATE
```

其固定顺序是：

1. 对 `23/11` seed source-lock actual joint mask；TPC-25/TPC-32
   primitive mask 会因 `d_gamma=2,h0=2` 把 pair 杀为零，TPC-18 formal
   constant mask不能自动代表 physical packet；
2. 只有 source theorem 选择了同一个 nonzero physical mask/object，才
   审同名 `D=1` slice 的 exact `omega_1(1),omega_1(2)`；
3. 只有前两关通过，才冻结 `J=32,Q_18=16`、joint pair/packet ID、
   coefficient AST、active nonzero、normalization 与完整 loss ledger。

若 primitive/constant physical-mask attachment 不存在，则 fail closed，
下一 architecture reroute 冻结为：

```text
TPC18_S_EQUALS_2_NONPRIMITIVE_ENDPOINT_SOURCE_FORWARD_GATE
```

只有同一 source lock 上的 actual mask、named `D=1` slice、joint packet
与后续全部 production fields 真实形成，才可讨论 TPC-207。

## 19. 不编号 `23/11` mixed-`d` actual-mask 审计

### 19.1 冻结对象

本轮只审核：

```text
ONE_POSITIVE_DETERMINANT_TWO_PRIME_PRIME_MIXED_D_MASK_AND_OPENED_PACKET_ATTACHMENT_GATE
```

诊断 seed 继续原样：

```text
X=512, h0=2, R=4, V=2
alpha=(ell=23,d=1,k=24)
gamma=(ell=11,d=2,k=48)
j=24
(jL,jK,D0)=(4,5,0)
L=16, K=32
m_alpha=23, m_gamma=22
N_alpha=554, N_gamma=530
h0(m_alpha-m_gamma)=+2
```

两条 source primes 与 TPC-133/134/136 parent/upstream joins 仍通过；这只
证明 archive identity，不自动产生 actual physical pair。

### 19.2 actual joint mask 点审

令 `H=rad(h0)=2`。逐对象裁决为：

```text
TPC-18 primitive witness:
  gcd(d_alpha*j,h0)=gcd(24,2)=2
  gcd(d_gamma*j,h0)=gcd(48,2)=2
  joint mask = 0

TPC-25 actual primitive carrier:
  gcd(d_gamma,H)=gcd(2,2)=2
  gcd(j,H)=gcd(24,2)=2
  gamma row absent; orbit support also kills both sides

TPC-32 actual physical carrier:
  gcd(m_gamma,H)=gcd(22,2)=2
  gcd(j,H)=gcd(24,2)=2
  actual physical pair absent

TPC-93:
  exports only an already retained TPC-32 coefficient
  no carrier creation

TPC-18 formal constant mask:
  xi(1,24)=xi(2,24)=1
  FORMAL_COVER = YES
  FORMAL_TO_PHYSICAL_ATTACHMENT_THEOREM = ABSENT
```

所以 gate-level 首致命为：

```text
SOURCE_LOCKED_NONZERO_ACTUAL_JOINT_PHYSICAL_MASK_FOR_TPC23_11_SEED
  = ABSENT
```

在 actual primitive branch 内更具体的首阻断是
`GAMMA_PRIMITIVE_ROW_CARRIER_MEMBERSHIP`。formal `xi=1` 不得改名为
TPC-25/32 actual physical packet。

### 19.3 `D=1` 没有被解锁

按 gate 顺序，nonzero actual mask attachment 失败后不得进入 `D=1`
attachment。独立的
fail-closed source census 仍检查了是否存在会推翻该停止的 exact member：

```text
all-ref declared text-extension blobs = 7,596
extensions = .py,.json,.tex,.md,.bib,.toml,.csv,.txt,.jsonl
TPC text blobs = 2,132
TPC blobs containing dyadic omega_D-style symbols = 33
source theorem/artifact evaluations omega_1(1) = 0
source theorem/artifact evaluations omega_1(2) = 0
same named member with both endpoint values nonzero = 0
```

TPC-18 只给 `supp omega_D subset [D,2D]`、bounded-overlap partition 与
`sum_D omega_D(d)=1`；TPC-55 只继承 support/derivative bounds；TPC-19
和 TPC-54 的 nonzero/bounded-away statements 都是额外 hypothesis。
若同一 member 包含 `d=1,2`，support geometry 的确条件强制 `D=1`，
但 containment 与 partition identity 都不证明
`omega_1(1),omega_1(2)` 同时非零，也不产生 packet locator。

因此：

```text
D1_ATTACHMENT_GATE_REACHED = NO
D = NOT_MATERIALIZED
J = NOT_MATERIALIZED
Q_18 = NOT_MATERIALIZED
formal archive projection = 13/42
formal first missing = D at field 9
actual joint pair records = 0
production occurrences = 0
```

反事实地，若未来 source-locked theorem 把同一 named `D=1` member
theorem-backed attach 到这两条 exact rows，并证明
`omega_1(1),omega_1(2)` 非零，才可真实新增
`D=1,J=32,Q_18=16`，投影变为 `16/42`，contract-order 首缺变为 `T`；
这不自动补 `source_locator`、`packet_id`、pair/edge/target IDs、
coefficient nonzero、normalization 或 loss ledger。

### 19.4 nonprimitive 对象边界

TPC-18 `s=2` endpoint theorem 是两侧共用同一 `k` 的
`beta_I(k)^2` correlation，不是本 seed 的 mixed opened rows
`k_alpha=24,k_gamma=48`。而当前

```text
D0=0, V=2, I={1,2}
beta_I(k)=mu(1)+mu(2)=0  for every even k
beta_I(24)=beta_I(48)=0
```

所以本 seed 也不能偷渡为 nonprimitive endpoint witness。后续
nonprimitive route 的 Gate 0 必须先 source-lock：

```text
one common k
s=gcd(k,h0)=2
beta_I(k) != 0
named endpoint coefficient/object
actual source-forward record
```

### 19.5 新 source 与回归

新 pull 的 RH-327 证明的是 noisy Markov cyclic trace
`T=B+S+R` 与 synthetic exchange cancellation interval。其 `d` 是
clearance ratio、`J` 是 state-space window、`L/D` 是 shell scale/demand，
没有 TPC `omega_D`、Möbius row pair、determinant-two coefficient或
packet occurrence；其 Hardy normalization 与 `B/S/R` trace ledger 属于
RH noisy cyclic-trace 对象，不能提供本 seed 所需的 TPC
formula-semantic normalization 或 complete physical-loss ledger。它不
触发任何 TPC reopen。

随后远端新增的 RH-328 只把 RH-326/327 的 trace slots 写成 conditional
fixed-reference equation
`e=L(c_phys^(2k)-y)+E_obs+R`。其 theorem 明确以 physical shell
representation、scale 与 contrasts 已给定为前提；ledger 继续把 actual
exchange representation、physical fields、remainder little-`o` 与 actual
joint matching 保持 `OPEN`。其中 `d/L/D` 分别是 clearance、shell scale
与 scalar demand，不是 TPC divisor/dyadic scale。它没有
`omega_D`、Möbius row、`23/11` source lock、common-`k` endpoint 或 TPC
packet record，也不触发 reopen。

`d3e21af..24a962f` 的新增内容只有 RH-327/328，没有 primary TPC theorem
source。

TPC-206 三项、TPC-205 三项、TPC-194 hardening、TPC-173--179 optimized、
TPC-184/189 normal/optimized 与 TPC-133 normal/optimized 全部通过。
扩展 source-chain 回归发现 TPC-134--136 的三层 upstream raw-file SHA pins
仍是旧值；生成的 866 atoms、2,988 paths、frontier manifest、cut archive
及全部语义字段均未变化。只刷新下列 provenance pins 后，
TPC-134/135/136 normal/optimized 全部通过：

```text
TPC-134 <- TPC-133 atoms:
  a1956cf182ad219da10d850de7c7e57de69b8c287fb698e44faa5c795c3840a8
TPC-135 <- TPC-134 paths:
  efcacc90e7662fdb41c2e3f86fb37d3bd81b64a107c36dfbbb15bb48bde61712
TPC-136 <- TPC-135 certificate:
  c9e91c7cb69120e4f74554262356b8112061bd9cc9c13d5ce1c7232a54165e0a
TPC-136 <- TPC-135 frontier manifest:
  6655a4c40a57f0a45022ab527b32560a5b2ac3e932368709502cfded43a3fb47
```

### 19.6 最终裁决与下一有限路线

```text
ONE_POSITIVE_DETERMINANT_TWO_PRIME_PRIME_MIXED_D_MASK_AND_OPENED_PACKET_ATTACHMENT_GATE
  = FAIL_CLOSED_AT_NONZERO_ACTUAL_PHYSICAL_JOINT_MASK_ATTACHMENT
    STOP_SCOPED_NOT_REOPENED

TPC207_TRIGGER = NO
TPC207_CREATED = false
```

本轮新增且仅新增第 6 节的一个 seed-scoped cell。全部旧 cells，尤其
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`，继续 `STOP_SCOPED`。
两个 O161 parents、pair-native reroute、H1 与 global architecture
继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为 `UNPAID`，
`L2=NONE`。

下一项不编号 architecture gate 冻结为：

```text
TPC18_S_EQUALS_2_NONPRIMITIVE_ENDPOINT_SOURCE_FORWARD_GATE
```

其 Gate 0 是
`NONZERO_COMMON_K_AND_BETA_I_K_NE_0_NAMED_ENDPOINT_RECORD`。当前
`D0=0,V=2` packet 与 `23/11` seed 均不可复用。只有该 Gate 0 及 actual
source-forward、normalization、loss ledger 后续门槛真实通过，才允许
讨论 TPC-207。

## 20. 不编号 TPC-18 `s=2` source-forward 审计

### 20.1 冻结对象与 gate 顺序

本轮只审核：

```text
TPC18_S_EQUALS_2_NONPRIMITIVE_ENDPOINT_SOURCE_FORWARD_GATE
```

Gate 0 继续严格要求同一 source lock 上同时存在：

```text
one common k
s=gcd(k,h0)=2
beta_I(k) != 0
named endpoint coefficient/object
actual source-forward record
```

不同 `k` 的 opened rows 不得拼成 common-`k`；formal coefficient 不得改名为
actual packet；endpoint support 不得改名为 nonzero 或小量。上一轮
`D0=0,V=2` packet 与 `23/11` mixed-`k` seed 均不自动复用。

### 20.2 TPC-18 精确公式与 `h0=2` 特化

TPC-18 定义

```text
I = (D0,V] intersect N
beta_I(k) = sum_{d|k, d in I} mu(d).
```

若 `s=gcd(k,h0)>1`、`H=rad(s)`，其 endpoint theorem 精确给出

```text
beta_I(k)
  = sum_{e|k,(e,H)=1} mu(e) Omega_H(e),

Omega_H(e)
  = sum_{f|H} mu(f) 1_{D0<ef<=V},

supp Omega_H
  subset (D0/H,D0] union (V/H,V].
```

对 `h0=s=2`，`H=2`、`k` 必须为偶数，并且

```text
Omega_2(e)
  = 1_{D0<e<=V} - 1_{D0<2e<=V}.
```

在 stopping theorem 的 `D0<V/2` 范围内，对每个正整数 `e` 都有

```text
Omega_2(e) = -1  for D0/2 < e <= D0,
Omega_2(e) = +1  for V/2  < e <= V,
Omega_2(e) =  0  otherwise.
```

在 `beta_I(k)` 的 endpoint sum 内还要求 `(e,2)=1`，且 `mu(e)=0` 的项
没有贡献；所以实际贡献者只能是奇数、平方自由的 endpoint divisors。
所以 `beta_I(k)!=0` 当且仅当 `k` 的奇部在两个 endpoint bands 上的带
Möbius 符号 divisor sums 不相等。这是 pointwise exact identity，不是
average cancellation theorem。TPC-18 的 nonprimitive correlation 严格使用
同一个 `k` 上的 `beta_I(k)^2`；TPC-205/206 的
`k_alpha=24,k_gamma=48` 不能改写成该对象。

### 20.3 当前 source-locked packet census

TPC-133 的 866 个 raw `(ell,k,d)` rows 商掉 `d` 后给 585 个 distinct
`(ell,k)`。其中 `h0=2`、`gcd(k,h0)=2` 的偶数 `k` rows 有 281 个；
再要求 `ell` 为 prime 有 91 个。存在 10 个同偶数 `k` 的 prime-source
formal fibers：

```text
k = {4,6,8,10,12,14,18,20,32,48}
ordered formal source pairs = 80
unordered formal source pairs = 40
```

但该 source lock 固定 `D0=0,V=2`，故

```text
I = {1,2}
beta_I(k) = mu(1)+mu(2) = 0  for every even k.
source-locked h0=2 formal beta_I(k)!=0 records = 0
materialized source-locked h0=2 nonzero per-k endpoint records = 0
```

这 40 个 unordered pairs 只证明 same-`k` row combinatorics，不是 nonzero
endpoint coefficient，更不是 actual pair occurrence。其当前 Gate 0
首致命为：

```text
SOURCE_LOCKED_H0_2_COMMON_K_BETA_I_K_NE_0 = ABSENT
```

下游 actual census 同样为零：

```text
TPC-136 downstream maps:
  4/4 domain_cut_path_ids = []
  status = NOT_TESTABLE

TPC-143:
  obligations = 2,988
  actual_map_edges = [] on every obligation

TPC-153:
  shadows = 2,988
  nonnull actual_occurrence_id = 0
  is_actual_occurrence = false on every shadow

TPC-154:
  formal fibers = 2,989
  formal occurrence edges = 8,967
  theorem_backed_actual_provenance = true count = 0
  actual completions = 0
```

因此 42-field registry 新增字段为 0，actual occurrence IDs 为 0；
projection 仍为 `13/42`，field-order first missing 仍是 `D`。

### 20.4 通用公式非零，但不是 actual record

不得把上一小节的 finite-corpus 零结论提升为 TPC-18 通用
nonexistence。精确公式立即给出纯代数候选，例如

```text
h0=2, s=2, D0=6, V=18, k=22, e=11
Omega_2(11)=+1
beta_I(22)=mu(11)=-1
FORMAL_ALGEBRAIC_NONZERO = YES
```

这只说明 `beta_I(k)!=0` 在公式上可实现。它没有 theorem-valid physical
block schedule、具名 source pair、nonzero smooth cutoff value、packet/cut
locator 或 source-forward occurrence，不得获得 actual credit。

TPC-18 自带 certificate 也固定
`h=6,D0=6,V=18,H in {2,3,6}`；`H=2` sector 只做 120 个 `k` 的 exact
finite identity/support regression。certificate 明确记录
`prime_asymptotic_evidence=false`，没有 per-`k` physical source/packet
record，不能改名为 `h0=2` actual witness。

### 20.5 branch-selection 缺口

TPC-18 stopping theorem 对任一满足其 block geometry 的抽象 symmetric
tail block，在额外假设 tail-failure lower bound 后，只推出以下至少一个：

```text
A = primitive generic determinant witness
B = nonprimitive endpoint finite-model witness for some s>1
```

固定 `h0=2` 后，若 B 发生则其 sector 必为 `s=2`；但 theorem 没有排除
A，也没有无条件证明 B、给出具名 source-locked block，或证明本仓库
packet 的 tail failure。具名/source-locked block 是本审计的额外 actual
要求，不是 TPC-18 定理的输出。此前 primitive
seed/mask 的 finite failures 不等于 aggregate alternative A 被 theorem
排除，故不得反推 B。TPC-18 还明确声明 endpoint localization 不推出
endpoint correlation 小量；剩余 finite-model lattice sum 仍需新估计。

因此，放宽到通用 TPC-18 参数后，route-level 缺口依次为：

```text
SOURCE_LOCKED_THEOREM_VALID_H0_2_BLOCK_AND_THEOREM_BACKED_TAIL_FAILURE
  = ABSENT
NONPRIMITIVE_ALTERNATIVE_B_SELECTION_THEOREM = ABSENT
NAMED_ACTUAL_COMMON_K_ENDPOINT_PACKET_ATTACHMENT = ABSENT
```

Gate 0 已 fail closed，normalization 与 complete physical-loss ledger
未进入审核，不能用“尚未审核”改写成“已通过”。

### 20.6 新 source、回归与最终裁决

本轮启动 `git pull --rebase origin main` 为 already up to date；HEAD
`f2f98b0bdc4b56c36292e9211b19c1d2e45ffae0` 之后没有新增 primary
TPC theorem source。RH-327/328 已在上一轮按对象错型排除；本轮没有新的
reopen trigger。

TPC-206 三项、TPC-205 三项、TPC-194 hardening、TPC-133--136、
TPC-184/189 normal/optimized 与 TPC-173--179 optimized 全部通过。

扩展回归发现上一轮刷新 TPC-134--136 upstream SHA pins 后，
TPC-143 committed certificate 尚未级联刷新：

```text
TPC-143 obligations = BYTE_IDENTICAL (2,988 rows)
TPC-143 --check = DRIFT_AT_CERTIFICATE_ONLY
current certificate sha256
  = e398b38b39e8a094123d2830a42ea4806d820655f55a5425f10d985a0783a724
in-memory regenerated certificate sha256
  = de1d191500da4c8de025029c08970709968407f51804b3a2a148e41620764642
semantic/census/claim fields changed = 0
provenance leaf changes = 12
```

12 个 leaves 仅把五条 legacy raw-hash bindings 的 recorded SHA/status 与总
status 从 stale 刷到 canonical UTF-8/LF match；obligations、census、
proved、actual status、first missing 与 claim boundary 全部不变。
隔离副本证明刷新会沿 TPC-143--179，并继续经 source inventories/releases
级联到 TPC-204--206。为避免在本次数学 gate 中静默重写已发布论文与稳定
PDF/source-lock release，本轮不执行该全链 mechanical refresh。它不是
theorem trigger，也不改变上述零 occurrence 裁决；但在下一篇编号论文发布
前必须单独完成完整 provenance cascade、重建受影响 releases 并全链
`--check`：

```text
PROVENANCE_CASCADE_REFRESH_REQUIRED_BEFORE_NEXT_NUMBERED_RELEASE = YES
```

最终裁决：

```text
current D0=0,V=2 source-locked packet
  = FAIL_CLOSED_AT_BETA_I_K_NE_0

general-parameter h0=2 route
  = FAIL_CLOSED_AT_SOURCE_LOCKED_THEOREM_VALID_BLOCK_AND_TAIL_FAILURE
    THEN_B_SELECTION_AND_ACTUAL_PACKET_ATTACHMENT

TPC18_S_EQUALS_2_NONPRIMITIVE_ENDPOINT_SOURCE_FORWARD_GATE
  = STOP_SCOPED_NOT_REOPENED

general TPC-18 formal beta nonzero = YES_L0_ONLY
current source-locked h0=2 beta-nonzero records = 0
actual named common-k endpoint records = 0
actual source-forward records = 0
production occurrences = 0
formal archive projection = 13/42
formal first missing = D at field 9
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

本轮新增且仅新增第 6 节的一个 finite-corpus cell。全部旧 cells，尤其
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`，继续 `STOP_SCOPED`。
两个 O161 parents、pair-native reroute、H1 与 global architecture
继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为 `UNPAID`，
`L2=NONE`。

下一项不编号 architecture gate 冻结为：

```text
TPC18_H0_2_NONPRIMITIVE_ALTERNATIVE_SELECTION_AND_ACTUAL_PACKET_ATTACHMENT_GATE
```

固定顺序是：

1. source-lock 一个 theorem-valid `h0=2` symmetric tail block、exact
   `X,L,K,R,V,D0` schedule 与 actual tail-failure input；
2. 新 theorem 排除 primitive alternative A，或直接给出 `s=2`
   finite-model correlation B 的所需下界；
3. 在同一 source lock 上冻结 named common `k`、`beta_I(k)!=0`、endpoint
   coefficient、source pair 与 actual packet/cut locator；
4. 只有前三关通过，才审 TPC-205/206 source-forward fields、
   normalization 与 complete physical-loss ledger。

`(D0,V,k,e)=(6,18,22,11)` 只可作为 algebraic diagnostic candidate，
不得预记为 physical record。只有上述四关真实通过，才允许讨论 TPC-207。

## 21. 不编号 `h0=2` exact-profile / branch-selection / attachment 审计

### 21.1 冻结对象与裁决

本轮只审核：

```text
TPC18_H0_2_NONPRIMITIVE_ALTERNATIVE_SELECTION_AND_ACTUAL_PACKET_ATTACHMENT_GATE
```

顺序仍是 theorem-valid block、actual tail-failure、排除 primitive A 或直接
选择 `s=2` 的 B、同一 source lock 上的 actual packet attachment。结果是
前置几何与系数层得到真实推进，但任何 actual / L2 trigger 均未成立：

```text
SOURCE_BACKED_EXACT_DYADIC_H0_2_PROFILE
  = YES_THEOREM_SPECIALIZATION

EVEN_K_BETA_I_K_NE_0_ON_SMOOTH_K_SUPPORT
  = YES_EXISTENTIAL_COEFFICIENT_LEVEL_ONLY

SOURCE_BACKED_ACTUAL_H0_2_SYMMETRIC_TAIL_FAILURE_LOWER_BOUND
  = ABSENT

FULL_R_R_PRIMITIVE_GENERIC_DETERMINANT_CORRELATION_BOUND
  = ABSENT

DIRECT_C_I_2_MM_OFF_LOWER_BOUND_OR_OCCURRENCE
  = ABSENT

NAMED_SOURCE_LOCKED_ACTUAL_PACKET_CUT_ATTACHMENT
  = ABSENT
```

因此本轮不能创建 TPC-207。

### 21.2 一条精确 dyadic published-profile family

TPC-17 的 published Maynard theorem 对每个固定 `h!=0` 成立，故可严格
取 `h0=2`。令 `m>=1`，并冻结

```text
sigma = 1/1000
delta = 1/20
eta   = 1/1000

X_m  = 2^(21000 m)
R_m  = 2^(9450 m)
V_m  = 2^(4725 m)
L_m  = 2^(9979 m)
D0_m = 2^(979 m)
K_m  = 2^(11021 m)
I_m  = (D0_m,V_m] intersect N.
```

这不是近似 exponent ledger：所有量都是整数，`L_m,K_m` 是 dyadic，且

```text
R_m = floor(X_m^(1/2-delta))
V_m = floor(sqrt(R_m))
L_m K_m = X_m
L_m/R_m = 2^(529m)
V_m/D0_m = 2^(3746m)
K_m/V_m^2 = 2^(1571m).
```

published-profile 三个 monomial 与 leakage 的精确 bit margins 为

```text
X_m/(D0_m L_m^2)          = 2^(63m)
X_m^4/(D0_m^12 L_m^7)    = 2^(2399m)
X_m^10/(D0_m^20 L_m^19)  = 2^(819m)
X_m/(L_m D0_m R_m)        = 2^(592m).
```

所以 `eta=1/1000` 小于全部固定 power margins；同时
`1/42+3 sigma<delta<1/4`。对充分大 `m`，TPC-17 的 published theorem
确实给该 family 的 prefix cancellation 与 exact symmetric-tail normal form。
这清除了“`h0=2` 几何是否存在”的问题，但不提供 tail 的正性、失败下界、
具名有限 `m` 的 theorem threshold、具体非零 cutoff 值或 actual occurrence。

### 21.3 smooth `k`-support 上的 even-sector 非零系数

固定 TPC-17 的非负 dyadic partition weight `psi`。其正值集包含某个开区间
`J=(a,b)`。由上一小节的 `K_m/V_m^2 -> infinity`，对充分大 `m` 可取奇素数

```text
p_m in (V_m/2,V_m]
q_m in (a K_m/(2p_m), b K_m/(2p_m)),  q_m>V_m,
k_m = 2 p_m q_m.
```

第二个素数由固定比例区间上的 PNT 保证。于是

```text
gcd(k_m,2)=2
k_m/K_m in J
psi(k_m/K_m)>0.
```

`k_m` 在 `I_m` 中唯一的 divisor 是 `p_m`，故 TPC-18 的 literal coefficient
给出

```text
Omega_2(p_m)=1
beta_I_m(k_m)=mu(p_m)=-1.
```

所以一般 `h0=2` route 的障碍不是 even-sector `beta` 恒零。这个结论是由
已冻结公式与 PNT 推出的 coefficient-level existence lemma；它没有给
`ell_1,ell_2`、residual target values、source pair、packet/cut locator、
tail-failure 或 source-forward ID，严禁记为 actual attachment。

### 21.4 旧 finite diagnostic 的修正

上一轮的

```text
(D0,V,h0,k,e)=(6,18,2,22,11)
```

虽有 `Omega_2(11)=1` 与 `beta_I(22)=-1`，却不能进入允许的 dyadic
`k`-cutoff。几何要求 `K>2V=36`；`supp psi subset [1/2,2]` 与
`psi(22/K)!=0` 又要求 `K<=44`，而 `(36,44]` 没有 dyadic `K`。故其精确
状态是

```text
ALGEBRAIC_NONZERO = YES
DYADIC_SMOOTH_SUPPORT_ATTACHMENT = IMPOSSIBLE.
```

较好的有限 L0 diagnostic 是

```text
(D0,V,h0,k,e)=(6,18,2,66,11)
beta_I(66)=-1.
```

dyadic partition 精确给 `psi(66/64)+psi(66/128)=1`，所以 `K=64` 或
`K=128` 至少一个 cutoff 非零，且两者均满足 `K>36`。但它没有唯一 `K`、
`X,L,R`、published-profile source lock、source pair 或 tail failure，仍只准
作 finite L0 diagnostic。

### 21.5 actual attachment census 与 synthetic firewall

当前生产链仍是：

```text
TPC-133 native rows = 866
TPC-134/136/143/153 records = 2,988 each
production h0=2,D0=0 records = 2,988

TPC-136 FRONTIER_UNMAPPED = 2,988/2,988
TPC-143 occurrence lift NOT_TESTABLE = 2,988/2,988
TPC-153 actual occurrence IDs = 0
```

TPC-154 的 2,989 个 fibers 中，唯一正 `D0` 的记录冻结

```text
X=2^84, R=2^21, V=2^10, D0=2, L=2^38, K=2^46, h0=2.
```

TPC-135 deterministic policy 把它分类为 `ELIGIBLE`；但记录本身严格是
`SYNTHETIC_L0_ONLY`，并有

```text
native_tuple = (0,0,0)
actual_active_support = UNDECIDED
theorem_backed_actual_provenance = false.
```

在该 synthetic schedule 上可构造纯 formal 算术候选

```text
k = 521 * 2^37
k/K = 521/512
gcd(k,2)=2
Omega_2(521)=1
beta_(2,1024](k)=-1
source-prime diagnostics = 274877906951, 274877906957.
```

三个数均经独立 deterministic primality check 通过。但 exact `W,psi` 非零、
native row、cut/packet ID、joint source locator 与 actual occurrence 全缺，故
它不能填 42-field registry 的任何 selected-lineage 缺口。

当前 `D0=0,V=2` 档案虽有 10 个 even-`k` prime-source groups 与 40 个
unordered same-`k` source pairs，但全部 `beta_I(k)=mu(1)+mu(2)=0`；同批
pair 的 TPC-18 row determinant `h0(m1-m2)=±2` 命中数也为 0。TPC-206
因此仍为 `13/42`，field-order first missing 仍是 `D`。禁止把 synthetic
`D0=2`、formal prime diagnostics 与 selected `X=512` lineage 拼接。

还须保持三条 schema firewall：TPC-154 line 2,989 虽有 `FORMAL_ONLY det=2`
标签，但 actual affine data 给 `su-ad=1` 且 provenance 为 false；TPC-205 的
determinant-two fixture 是 `DERIVED_L0_ONLY`、`production_occurrence=false`；
TPC-18 的 `s=2` 是 `gcd(k,h0)` content sector，不是 literal `su-ad=2`
two-Möbius atom。三者均不得跨对象拼接。

### 21.6 theorem source audit 与三重 fatal

本轮 all-ref 扫描覆盖 34 refs / 28 unique tips；TPC-18 的三个关键 source
files 各只有 commit `f418ea1` 加入的一个历史 blob，没有更强旧版本。仓库与
primary candidates 的逐对象裁决为：

1. `tail-failure`：TPC-17 只证 prefix cancellation / tail normal form；
   TPC-18 把 `|T_{L,K}(I)|>=eta X/(log X)^a` 明列为额外假设。Lichtman 与
   Matomäki--Radziwiłł--Tao 是 shift-average / log-average 对象；Maynard、
   Li、Pascadi 是 AP 或 factorable-weight 平均分布与上界，均不给同一 actual
   `h0=2` block 的 lower bound。
2. primitive A：TPC-27/28 只控制 selected calibrated truncated square；
   `u,v>T` ultra-long complement 未恢复。TPC-108 的 fixed-`h0` generic
   affine estimate 仍标为未证 L2。现有 AP / spectral large-sieve 定理不等于
   TPC-18 的完整 `r_R(n_1)r_R(n_2)` variable-determinant correlation。
3. direct B：TPC-18 Gram floor 只给 aggregate `sum_k beta_I(k)^2` mass，
   不给 prime source、`Lambda_R` pair、off-diagonal signed correlation 或
   `s=2` selection。Goldston--Yıldırım 使用不同的 truncated-divisor model；
   Ramaré--Zúñiga Alterman 是 scalar LCM diagonal；Laporta 的假设已含
   Hardy--Littlewood 强度；Coppola--Murty--Saha 需要当前未验证的 coefficient
   decay。都不能改名为 `C_{I,2}^{MM,off}` lower bound / occurrence。

因此最早 fatal 是

```text
SOURCE_BACKED_ACTUAL_H0_2_SYMMETRIC_TAIL_FAILURE_LOWER_BOUND = ABSENT.
```

即使暂借该假设，后面仍独立卡在

```text
FULL_R_R_PRIMITIVE_GENERIC_DETERMINANT_CORRELATION_BOUND = ABSENT
DIRECT_C_I_2_MM_OFF_LOWER_BOUND_OR_OCCURRENCE = ABSENT.
```

### 21.7 STOP scope、路线选择与下一关

最终裁决：

```text
TPC18_H0_2_NONPRIMITIVE_ALTERNATIVE_SELECTION_AND_ACTUAL_PACKET_ATTACHMENT_GATE
  = STOP_SCOPED_NOT_REOPENED

exact theorem-valid h0=2 dyadic family = YES
even-k beta nonzero on smooth k-support = YES_L0_COEFFICIENT_ONLY
actual named tail-failure blocks = 0
full primitive-A exclusion theorems = 0
direct s=2 B theorems = 0
actual packet/cut attachments = 0
production occurrences = 0
formal archive projection = 13/42
formal first missing = D at field 9
TPC207_TRIGGER = NO
TPC207_CREATED = false.
```

新增且仅新增第 6 节的
`DECLARED_TPC18_H0_2_TAIL_FAILURE_A_EXCLUSION_AND_DIRECT_B_CORPUS_V1`
cell；所有旧 cells，尤其 `TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`
与上一轮 `DECLARED_TPC18_H0_2_COMMON_K_ENDPOINT_SOURCE_FORWARD_RECORD_CORPUS_V1`，
继续 `STOP_SCOPED`。两个 O161 parents、pair-native reroute、H1 与 global
architecture 继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为
`UNPAID`，`L2=NONE`。

下一条最可能取得真实推进的路线不是把 tail-failure 或 direct B 当作已知，
而是先补 primitive A 的 upper-bound 技术缺口：从 TPC-27/28 的 truncated
square 明确恢复 `u,v>T` ultra-long complement，并核查能否形成完整
`r_R r_R` determinant dispersion theorem。故下一项不编号 gate 冻结为：

```text
TPC18_H0_2_FULL_R_R_PRIMITIVE_A_ULTRA_LONG_COMPLEMENT_GATE
```

这一路线即使跑通，也只会排除 stopping dichotomy 的 A；它仍不自动供应
actual tail-failure、B lower bound、actual packet attachment 或 TPC-207 trigger。

### 21.8 启动、回归与发布边界

本轮启动时执行 `git status --short --branch` 与
`git pull --rebase origin main`；远端已同步，审计基线为
`ea865160f05193047513a8a66665dc989934ae28`。只读回归结果：

```text
TPC-206: 3/3 PASS, projection 13/42, mathematical_reopen=false
TPC-205: 3/3 PASS, production pair records=0
TPC-194 certificate hardening: PASS
TPC-133--136: 4/4 PASS
TPC-184 normal/optimized: 2/2 PASS, TARGET_WELL_TYPED_OPEN
TPC-189 normal/optimized: 2/2 PASS, TARGET_WELL_TYPED_OPEN
TPC-173--179 optimized: 7/7 PASS
git diff --check: PASS
handoff Markdown fences: balanced
```

所有 checker 均设置 `PYTHONDONTWRITEBYTECODE=1`；没有生成新测试产物，既有
TPC-105 `__pycache__`、TPC-63 构建文件与 `tmp/` 均未触碰。本轮没有创建
论文或 PDF，故没有伪造 PDF QA。TPC-143 的 certificate-only 12-leaf drift
仍按第 20 节隔离：它不改变 2,988 obligations 或零 occurrence 裁决，但在
下一篇编号 release 前仍必须完成完整 provenance cascade。

## 22. 不编号 full-`r_Rr_R` primitive-A / ultra-long complement 审计

### 22.1 冻结对象与最终裁决

本轮只执行页首原定 gate：

```text
TPC18_H0_2_FULL_R_R_PRIMITIVE_A_ULTRA_LONG_COMPLEMENT_GATE
```

逐公式审核覆盖 TPC-18、TPC-19、TPC-25--32、TPC-33--124 的实际
ultra-residual lineage，并复核 TPC-125--206 的相关 claim/status。结果不是
“TPC-27/28 之后没有路线”，而是精确定位出了两个互相独立、均未通过的门槛：

```text
CURRENT_EXACT_H0_2_FAMILY_HAS_LEGAL_TPC27_28_TRUNCATED_ENTRY = NO

SELECTED_TPC28_PACKET_FULL_MATCHED_ULTRA_SHELL
  = REDUCED_TO_SMALL_CONTENT_AUXILIARY_ZERO

SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_THEOREM = ABSENT
ALL_RELEVANT_D_SLICES_UNIFORM_ATTACHMENT = ABSENT
ORIGINAL_PHYSICAL_NORMALIZATION_AND_EXACTLY_ONCE_REASSEMBLY = ABSENT

FULL_R_R_PRIMITIVE_GENERIC_DETERMINANT_CORRELATION_BOUND = ABSENT
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

因此精确裁决为：

```text
TPC18_H0_2_FULL_R_R_PRIMITIVE_A_TRUNCATED_ENTRY_AND_
SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_ABSENT_
STOP_SCOPED_NOT_REOPENED
```

### 22.2 TPC-18 literal 对象与完整 complement ledger

TPC-18 一个 dyadic `D`-slice 的 primitive generic 对象是

```text
m_i = ell_i d_i
J = K/D
Q = LD
QJ ~ X

C_D,prim^gen
  = sum_j sum_(alpha_1 != alpha_2)^generic
      mu(d_1)mu(d_2)(log ell_1)(log ell_2)
      r_R(m_1 j + 2) r_R(m_2 j + 2)
      B_alpha_1(j) B_alpha_2(j).
```

`generic` 必须同时保留

```text
ell_1 != ell_2
|m_1-m_2| > Q X^(-kappa)
(d_1,d_2) <= X^kappa
(d_1 j,2)=(d_2 j,2)=1.
```

其 literal determinant、row gcd、natural normalization 与 stopping witness
分别是

```text
det = 2(m_1-m_2)
(m_1,m_2) = (d_1,d_2)
N0 = JQ^2 ~ XQ
C_D,prim^gen >> XQ/(log X)^(2a+2).
```

对 target `N_m=mj+2`，TPC-19、TPC-27--29 的 exact dictionary 是

```text
a(u)   = -mu(u) log u
b_R(u) = a(u)-lambda'_R(u)

A_m,T(j) = sum_(u<=T, u|N_m) b_R(u)
P_m,T(j) = A_m,T(j)-delta_H(m)
C_m(j)   = sum_(T<u<=U0, u|N_m) a(u)

r_R(N_m) = A_m,U0(j) = A_m,T(j)+C_m(j),
```

其中 `U0~X` 大于 physical support 上全部 targets，且 `T>=R` 才保证新 shell
上 `b_R=a`。因此 full raw complement 的 domain 不是只写 `u,v>T`，而是

```text
u,v <= U0 and max(u,v)>T.
```

它恰有三条、不多不少：

```text
A_m,T C_n : u<=T<v<=U0, coefficient b_R(u)a(v)
C_m A_n,T : v<=T<u<=U0, coefficient a(u)b_R(v)
C_m C_n   : T<u,v<=U0,     coefficient a(u)a(v).
```

TPC-29 的 calibrated cutoff difference 是

```text
P_m,U0 P_n,U0 - P_m,T P_n,T
  = A_m,T C_n + C_m A_n,T + C_m C_n
    -delta_H(m)C_n-delta_H(n)C_m.
```

即 `three raw + two drift`；没有 two-drift term，因为它在两个 cutoffs 间
精确相消。两条 drift 已有

```text
O_epsilon(X^epsilon XQ/L)
```

的 fixed-power saving。直接相对 literal full residual，则

```text
r_R(N_m)r_R(N_n)-P_m,T P_n,T
  = A_m,T C_n + C_m A_n,T + C_m C_n
    +delta_H(m)A_n,T+delta_H(n)A_m,T-delta_H(m)delta_H(n).
```

最后一行由旧 base drift bridge 控制；未关闭的 hard arithmetic object 正是
三条 raw channels 的 matched sum。只审 `C_mC_n` 会漏掉两个 mixed
rectangles，不能叫 complete complement。

### 22.3 TPC-29--32 实际关闭到哪里

TPC-28 source-compatible high-`beta` sample 对每个固定 `h!=0` 成立，故可取
`h0=2`：

```text
sigma = 1/10000
lambda = 99979/210000
delta = 7/60

Q = X^(267/400+o(1))
D = X^(10049/52500+o(1))
J = X^(133/400+o(1))
R=S = X^(23/60+o(1))
V = X^(23/120+o(1))
T = X^(193/500+o(1)).
```

它 theorem-backed 地关闭一个 selected calibrated truncated square
`Q_T^phys`，但 TPC-18 Alternative A 是“某个 `D<=V` 存在 witness”。一个
fixed high-`beta` `D`-packet 不能排除其余 slices，更不能与上一轮另一组
`sigma,delta,D0,L,K` source lock 拼接。

后续实际推进为：

1. TPC-29 对三 raw channels 的 content-rich sparse wedge 与 large selected-
   divisor-content sectors给 fixed-power saving；primitive/small-content core 留下。
2. TPC-30 用 full target content
   `c=(N_m,N_n)=(N_m,m-n)|m-n` 关闭 `c>C`：

   ```text
   S_sh(c>C)
     << X^epsilon (Q^2+XQ/C)
      = X^epsilon N0(1/J+1/C).
   ```

3. TPC-31 的 canonical determinant 是
   `Delta#=(m-n)/c`，满足 `mV-nU=2 Delta#`。它只有在 `c=1` 时才等于
   TPC-18 literal determinant divided by the fixed `h0`;不得删去 content。
4. TPC-32 exact matched shell 是

   ```text
   K^sh
     = A_m,U0 A_n,U0 - A_m,T A_n,T
     = A_m,T C_n + C_m A_n,T + C_m C_n,

   S_full^sh
     = A_hat_C,q(0) + S_sh(c>C).
   ```

   因 large-content 项已经关闭，selected packet 的唯一 hard cell 是

   ```text
   A_hat_C,q(0)
     = Phi_D[(A_m,T C_n+C_m A_n,T+C_m C_n)
             1_((N_m,N_n)<=C)].
   ```

这里 `r=0` 是 normalized-determinant auxiliary DFT zero，既不是 orbit-variable
Poisson zero，也不是 TPC-20 centered-divisor zero。TPC-27 已对每个 polynomial
`S>=R` 关闭 additive Poisson zero，因此把该旧结论再对两个 endpoints 作差不是
新 theorem，也不触及 `A_hat_C,q(0)`。

TPC-32 对 `beta=267/400, C~J` 的完整 matched-shell 结论严格条件于

```text
F0(A_C) = |A_hat_C,q(0)|^2 / ||A_C||_2^2
         <= X^(chi+o(1)),
chi <= 1/400.
```

Almost-all nonzero frequencies、Parseval 或 additive large sieve 不证明这个
distinguished coefficient 的 premise。TPC-33--108 将同一门槛依次转写成
physical column energy、four-Mobius same-time Gram、coherent spectrum、literal
low-window affine atom 与 restricted growing fixed-`h0` estimate；TPC-108 的 H3
仍明确是未证 L2。TPC-109--124 的 frame、tail-cover 与 reassembly statements
均是 L0/L1 或条件接口，没有新增该 signed estimate。

TPC-116 的数字也不得偷换：TPC-32 的 `chi<=1/400` 是 squared-flatness loss；
TPC-116 的 `sigma>=1/400` 是完整 outer costs 后的 aggregate physical saving。
前者不能靠字段同名或数值相近填入后者。TPC-116 没有 supplied growing mask
archive，也没有把 packet natural scale `N0=JQ^2\asymp XQ` source-lock 到 original
global physical normalization。

### 22.4 上一轮 exact family 的截断入口实际上为空

上一轮冻结的 published Maynard `h0=2` family 是

```text
lambda = 9979/21000
r0     = 9/20
v      = 9/40
d0     = 979/21000

D = X^d, d in [979/21000,9/40]
beta = lambda+d in [5479/10500,1838/2625].
```

TPC-26/28 的 `M_beta(t)>0` 对应 upper-cutoff supremum 为

```text
t_c(beta) = (1+beta)/4, beta<=3/5
t_c(beta) = (3-beta)/6, beta>=3/5.
```

整个 slice family 上 `t_c` 的最大值仅为 `2/5`，而 `R=X^(9/20)`；且
`t=t_c` 只是 `M=0` 边界，不满足 fixed positive margin。故不存在合法

```text
R <= S < T and M_beta(t)>0.
```

在最有利的 `S=R`，

```text
M_beta(R) = (beta-4/5)/2, beta<=19/30
M_beta(R) = (3/10-beta)/4, beta>=19/30.
```

全部为负；最佳也只有 `-1/12`。低/高 `D` endpoints 分别是
`-2921/21000` 与 `-2101/21000`。强取 `T<R` 不只是 schema 违规：shell 内
`lambda'_R` 不再消失，`b_R=a` 和 calibrated annular identity 都失效。把 shells
切薄或迭代不改善 upper-exponent minimax。

这只证明现有 TPC-26--28 Cauchy/conductor 方法不适用于该 exact family；
`M_beta<=0` 不是 arithmetic impossibility theorem。换 `delta` 是换 block，不能
改写为当前 source lock 已通过；即使换到 TPC-28 selected packet，small-content
matched auxiliary-zero 与 all-`D` uniformity 仍独立开放。

### 22.5 现有 bounds 与新增 primary-source 扫描

TPC-18 diagonal energy、row Cauchy 与 soft divisor bounds 合起来至多给

```text
|C_D^gen| <<_epsilon XQ X^epsilon,
```

即 natural scale，不能反驳 `XQ/log^(2a+2)` 的 positive stopping witness。
TPC-16 residual energy在当前 `delta=1/20` family 上还有主量

```text
sum_n r_R(n)^2 F(n/X)
  = (11/20+o(1)) X log X I0(F),
```

所以不能把 residual energy 当成小系数。reflected unit fiber `r=s=1` 对任何
`T<X` 仍含 ordinary smooth two-point Mobius correlation；固定-divisor large
sieve 在该 fiber 上没有可平均 conductor。它的原 row determinant 是
`2(m-n)`，未经 content extraction、actual packet 与 normalization crosswalk
不得改名为 literal determinant-two atom。

本轮扫描全部 Git refs/history（346 commits）与 TPC-18--206 relevant lineage；
`HEAD=origin/main=687bc2d44a25efd2a376fd3b363bfac4549b4cb9` 时没有新增 repo primary TPC
theorem source。外部截至 2026-07-31 的新增/最近 primary candidates 中：

1. Siddarth Menon, *Improved bounds for multiplicative functions in almost all
   short intervals*, arXiv:2607.15574v1。Theorem 1.1 是对 interval origin 的
   short Liouville/Mobius sum mean square；Theorem 1.4 仍对 origin 作平均；
   Theorem 1.5 对 shifts 作平均。它们没有 prescribed rows、actual masks、
   full `r_Rr_R`、variable determinant 或 all-slice/all-prefix uniformity。
2. Ramaré--Zuniga Alterman, *On a Mobius double sum*, arXiv:2603.25961v3，
   控制静态 `sum mu(d)mu(e)/[d,e]^(1+epsilon)`；这是 size/LCM diagonal
   object，没有 orbit `j`、affine targets 或 matched ultra shell。
3. Tao、MRT、Tao--Teräväinen、Pilatte、Lichtman--Teräväinen 的相关 rigorous
   results 分别在 logarithmic average、shift average、exceptional scale 或
   fixed-form/non-growing quantifier处先行失败；Siegel-zero routes还带额外条件。

未发现 theorem-backed

```text
DD_2(theta) for every actual primitive D-slice
```

或等价的 complete `P_T C+C P_T+CC` theorem。对当前 exact family，直接
`DD_2(theta)` 还须以固定余量覆盖

```text
theta_tail = lambda+v = 1838/2625.
```

若坚持 reflected route，则 theorem 必须包括 `r=s=1`、ordinary weights、
growing slopes、actual masks/outer coefficients 与全部 dyadic cells，并在完整
outer loss 后仍有净正 saving。TPC-108/H3 数字若被调用，还另须
`eta-ell_out>=1/200` 与 physical `TT*` crosswalk；本轮均不存在。

### 22.6 STOP scope 与下一关

本轮新增且仅新增第 6 节的

```text
DECLARED_TPC18_H0_2_FULL_R_R_PRIMITIVE_ULTRA_COMPLEMENT_CORPUS_V1
  = STOP_SCOPED
```

所有旧 cells，尤其 `TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`、
TPC18 common-`k` V1 与 tail-failure/A/B V1，继续 `STOP_SCOPED`。不得把
Menon 的 averages、TPC-27 additive zero、TPC-32 nonzero-frequency density-one
结果或 TPC-116 conditional schema 重新包装成新 method cell。

两个 O161 pointwise parents、pair-native reroute、H1 与 global architecture
继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为 `UNPAID`，`L2=NONE`。
TPC-207 trigger 仍为 false，没有创建论文或 PDF。

下一项最窄、最接近 hard coefficient、且不重复旧 stopped cells 的不编号 gate
冻结为：

```text
TPC32_H0_2_SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_SIGNED_PREFIX_TRANSFER_GATE
```

固定顺序是：

1. source-lock TPC-28/32 的 theorem-valid selected `h0=2` packet、三 raw
   channels、content cutoff `C`、canonical `Delta#`、actual mask/weights 与
   packet natural scale `N0=JQ^2\asymp XQ`；不得拼接上一轮 `delta=1/20` schedule；
2. 逐公式测试 TPC-111/122 的 ordered signed-prefix / bounded-variation 对象能否
   无损映射到同一个 `A_hat_C,q(0)`；determinant、content、outer labels 或
   prefix order 任一不一致即 fail closed；
3. 只有 source-backed growing signed-prefix theorem 真正推出 `chi<=1/400`，
   或直接给 small-content matched-shell saving，才可记 arithmetic advance；
4. 即使 selected packet 通过，仍须另审 all-`D` uniformity、exactly-once
   physical cover、original normalization、loss ledger、tail-failure、B selection
   与 actual packet attachment；任何一项都不自动触发 TPC-207。

下一篇编号 release 前仍必须完成 TPC-143--206 的完整 provenance cascade、
受影响 releases 重建和全链 `--check`；certificate-only drift 不得冒充数学
trigger。

### 22.7 启动、回归与发布边界

本轮启动时执行 `git status --short --branch` 与
`git pull --rebase origin main`；远端 already up to date，审计基线为
`687bc2d44a25efd2a376fd3b363bfac4549b4cb9`。只读启动回归结果：

```text
TPC-206 = 3/3 PASS
TPC-205 = 3/3 PASS
TPC-194 hardening = 1/1 PASS
TPC-133--136 = 4/4 PASS
TPC-184 normal/optimized = 2/2 PASS
TPC-189 normal/optimized = 2/2 PASS
TPC-173--179 optimized = 7/7 PASS
total = 22/22 PASS
```

TPC-27--32 的六个 legacy certificate 脚本均没有 `--check` 入口，且无条件
重写 committed JSON；为保持本轮只读验证边界，逐一审核入口后记为
`6 SKIP / 0 FAIL`，没有运行会写文件的 normal/optimized 模式。它们的 committed
papers/certificates 本轮未修改，SKIP 不得改写成新的 asymptotic evidence。

所有已执行 Python checks 均设置 `PYTHONDONTWRITEBYTECODE=1`，适用处使用
`-B`。`git diff --check` 通过，Markdown fences 为偶数且闭合。没有创建论文、
PDF 或构建日志，因此没有伪造 PDF QA。既有 TPC-105 `__pycache__`、TPC-63
构建文件与 `tmp/` 均未触碰，也没有新增 untracked artifact。TPC-143 的
certificate-only provenance cascade drift 继续按第 20 节隔离。

## 23. 不编号 TPC-32 small-content auxiliary-zero / signed-prefix transfer 审计

### 23.1 同一个 theorem-valid selected packet

本轮只执行：

```text
TPC32_H0_2_SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_SIGNED_PREFIX_TRANSFER_GATE
```

审计基线固定为
`28cafdd5fa96ff948f1520e778c7a2ba65208730`。TPC-28--32 明确沿用同一个
selected high-beta packet，而不是靠相同指数猜测拼接：

```text
sigma  = 1/10000
lambda = 99979/210000
delta  = 7/60
beta   = 267/400

Q = X^(267/400+o(1))
D = X^(10049/52500+o(1))
J = X^(133/400+o(1))
R = S = X^(23/60+o(1))
V = X^(23/120+o(1))
T = X^(193/500+o(1))
C = floor(J) = X^(133/400+o(1))
N0 = JQ^2 asymp XQ.
```

TPC-28 与 TPC-32 的 theorem interface 对每个固定 `h!=0` 陈述，故
`h0=2` 是合法 theorem-level specialization；TPC-28 JSON 没有把 `h=2`
单独序列化，TPC-32 JSON 中的 finite `h=2` coherent witness 也不得冒充
asymptotic packet attachment。

在这个 packet 上，TPC-32 保留 literal row coefficients

```text
gamma_alpha^(i)
  = mu(d_alpha) (log ell_alpha) omega_D^(i)(d_alpha)
    psi_L^(i)(ell_alpha/L) zeta_alpha^(i),

A_frak_(alpha,gamma)(j)
  = m_frak(alpha,gamma) Xi_(alpha,gamma)(j) W_(alpha,gamma)(j/J),
```

以及三条不能拆开的 raw channels

```text
A_m,T C_n,
C_m A_n,T,
C_m C_n.
```

其完整 matched shell 是

```text
K_sh(alpha,gamma,j)
  = A_m,U0 A_n,U0 - A_m,T A_n,T,

u,v <= U0 and max(u,v)>T.
```

full-target content 与 canonical determinant 为

```text
G_(m,n)(j) = gcd(mj+2,nj+2),
Delta#_(m,n)(j) = (m-n)/G_(m,n)(j),

A_C(n)
  = S_sh(G_(m,n)(j)<=C, Delta#_(m,n)(j)=n),

A_hat_C,q(0)
  = sum_n A_C(n)
  = S_sh(G_(m,n)(j)<=C).
```

因此 packet、三 raw channels、`C`、`Delta#`、literal masks/weights 与 `N0`
在 typed formula level source-lock 通过。generic pair mask 仍只知 bounded、
off-diagonal、divisor-independent；TPC-32 没有证明其 controlled projective
或 Schur decomposition。TPC-28 也仍只关闭一个 selected `D`-packet。

### 23.2 TPC-111/122 crosswalk 的第一个 fatal mismatch

TPC-111 正确地把 `r=0` 称为 TPC-32 normalized-determinant DFT 的
distinguished zero，并证明 finite coarsening invariance 与 sharp Abel duality。
但其 actual outer formula从以下条件开始：

```text
Assume content, masks, both polarizations, all native outer keys,
and literal outer reassembly have been verified.
```

随后才写成

```text
Z_X
  = sum_theta c_theta,X sum_r W_theta,X(r) sigma_theta,X(r)
    + E_content,X.
```

TPC-122 再次条件化该 reassembly，并允许把未保留的 outer keys 放入新的
`E_cont,X`。逐字段核对结果是：

| Gate field | TPC-32 selected packet | TPC-111/122 object | Verdict |
|---|---|---|---|
| literal coefficient | complete `a_sh_(alpha,gamma,j)`，含三 raw channels、两 row coefficients 与 actual joint multiplier | `c_theta W_theta sigma_theta`，factor allocation 仅条件给定 | no source-backed equality |
| determinant/content | variable `Delta#=(m-n)/G`，main term保留 `G<=C` | fixed affine determinant `h0`，content另列为 error | role crosswalk absent |
| outer labels | `(alpha,gamma,j)` 与 determinant bin `n` | ordered `(theta,r_i)` fibers | actual bijection/intertwiner absent |
| prefix order | physical orbit triples先按 `Delta#` 聚合；未给 `theta,r_i` order | literal translated-integer order不可重排 | order preservation unproved |
| normalization | `N0=JQ^2 asymp XQ` | `Q_X^2` zero-mode scale | no theorem identifies or pays the factor |

这不是说两套抽象字典数学上必不相容。精确 first missing 是 TPC-124 已经
写出的 coefficientwise fiber-intertwining test：determinant bins 与 ordered
zero-mode fibers 是不同 declared dictionaries；候选 `J` 必须满足

```text
(J Q_D - Q_Z) M = 0
```

而不能从一个 scalar total 或相似符号推出。TPC-124 的 committed audit 明确
`actual_growing_G_C_z_B_archive_present=false`，当前 artifacts 因而不能在同一
selected packet 上执行该 test。故 lossless `A_hat_C,q(0)` 到 TPC-111/122
prefix fibers 的调用在 outer-label/prefix-index 层 fail closed。

### 23.3 即使假设 crosswalk，growing arithmetic input 仍独立缺失

TPC-122 的 exact transfer 是条件式：若

```text
Delta_f <= X^(-delta_prefix+o(1)) A_f,
sum_f A_f ||w_f||_BV* <= X^(ell_Z+o(1)) Q_X^2,
|E_cont,X| <= X^(-eta_cont+o(1)) Q_X^2,
```

且全部对象、factor allocation 与 quantifier range相同，则

```text
eta_Z_cert = min(delta_prefix-ell_Z, eta_cont).
```

当前 committed claim flags 为：

```text
TPC-111 literal_growing_prefix_bound = false
TPC-111 positive_eta_Z = false
TPC-111 fixed_h0_L2_progress = false

TPC-122 actual_growing_prefix_saving = false
TPC-122 actual_outer_bv_envelope = false
TPC-122 actual_content_remainder_bound = false
TPC-122 uniform_subpower_class_hypothesis = false
TPC-122 fixed_h0_L2_saving = false
```

即使未来只补出一个 `eta_Z>0`，也不能靠字段改名直接得到 TPC-32 的
relative flatness `chi`：`F0(A_C)` 以同一个 actual `A_C` 的
`||A_C||_2^2` 为分母，而 TPC-32 当前只给该能量的 upper bound，没有可供
相除的 source-backed lower bound。若改走 direct zero bound，则仍必须先把
TPC-122 的 `Q_X^2`、全部 outer/content losses 与同一 packet 的 `N0` scale
无损 crosswalk；当前同样缺失。

TPC-126/127 的 canonical-order Abel 与 determinant-two pullback 只无损搬运
finite order、mask、weight、phase 和 prefix；它们明确不证明 complete growing
family cancellation。RH-287/RH-294 中名称相近的 rate-free growing-prefix
theorems控制 noisy trace/counterloop coefficients，不含本 gate 的 literal
Möbius coefficient、fixed physical `h0`、content、outer mask、`X/N/q` ranges
或 `N0` normalization，在第一项 physical-coefficient type check 即被排除。

发布前 rebase 另带入上游提交
`cdce55713a81cec09971d217faad154894088e3c` 的 RH-330。其对象是
`H_k=k R^(-2k)` 尺度上的 RH first-alias/full-trace coefficient，以及
`e=B+S+R+P-A` 的 conditional actual/model defect，不是 TPC-32 的
`A_hat_C,q(0)`。其 committed ledger 又明确给出
`actual_critical_packet_identified_with_weighted_prefix_coefficient=false`、
`actual_weighted_full_trace_prefix_vanishing_proved=false`、
`determinant_gluing_activated=false`。因此 RH-330 的 finite signed-prefix
恒等式没有 literal physical coefficient、fixed `h0=2`、content/determinant
fiber map 或 `N0=JQ^2` normalization，不能作为本 gate 的 growing theorem；
late-rebase type check 为 `WRONG_PHYSICAL_OBJECT_CONDITIONAL_INACTIVE`。

TPC-32 的 nonzero-frequency density-one、Parseval、large sieve 与 finite
coherent examples继续不能选择 `r=0`；`A_hat_C,q(0)` 仍可能位于 exceptional
set。没有 source-backed theorem 推出

```text
F0(A_C) <= X^(chi+o(1)), chi<=1/400,
```

也没有直接 small-content matched-shell saving。因此 arithmetic advance 为
`NO`。

### 23.4 精确裁决与 scope

本轮状态是：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
H0_2_SPECIALIZATION = PASS_THEOREM_LEVEL_NOT_JSON_SERIALIZED
THREE_RAW_CHANNELS_CONTENT_DETERMINANT_N0_LOCK = PASS
ACTUAL_GENERIC_PAIR_MASK_DECOMPOSITION = ABSENT

LOSSLESS_A_C_ZERO_TO_ORDERED_PREFIX_INTERTWINER = ABSENT
COMMON_FACTOR_ALLOCATION_AND_PREFIX_ORDER = ABSENT
N0_TO_Q_X_SQUARED_NORMALIZATION_CROSSWALK = ABSENT
GROWING_SIGNED_PREFIX_THEOREM = ABSENT
OUTER_BV_ENVELOPE = ABSENT
CONTENT_REMAINDER_AT_REQUIRED_EXPONENT = ABSENT

CHI_LE_1_OVER_400 = UNPAID
ARITHMETIC_ADVANCE = NO
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

精确裁决为：

```text
TPC32_H0_2_SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_TO_SIGNED_PREFIX_
EXACT_FIBER_INTERTWINER_AND_GROWING_INPUT_ABSENT_
STOP_SCOPED_NOT_REOPENED
```

本轮新增且仅新增第 6 节的

```text
DECLARED_TPC32_111_122_SELECTED_PACKET_AUXILIARY_ZERO_SIGNED_PREFIX_TRANSFER_V1
  = STOP_SCOPED
```

它不是 growing-prefix nonexistence theorem，也不否定新的 direct
`A_hat_C,q(0)` theorem。两个 O161 pointwise parents、pair-native reroute、H1
与 global architecture 继续 `OPEN`；fixed-atom credit 为 0，strict `1/400`
为 `UNPAID`，`L2=NONE`。all-`D` uniformity、exactly-once physical cover、
original/global normalization、tail-failure、A/B selection、actual packet
attachment 与完整 provenance gates 均未进入，更没有自动通过。

### 23.5 Reopen triggers 与验证边界

本 cell 只在出现下列至少一项新的 source-backed 输入时重开：

1. 同一 TPC-28/32 selected packet 上的 actual coefficientwise intertwiner，逐项
   保留三 raw channels、`G<=C`、`Delta#`、outer keys、literal factor allocation、
   canonical prefix order、mask/weights 与 `N0` normalization；
2. 直接对同一 actual `A_C` 证明 `chi<=1/400`，或直接证明 small-content
   matched-shell saving；
3. 对同一 actual ordered fibers 的 growing signed-prefix theorem，并同时给出
   uniform outer BV、content remainder、共同 constants/ranges 与完整 physical-loss
   ledger，足以在 `N0` scale 支付目标。

没有预设下一项不编号 audit；旧 cells 不得换名重开。持续工作流授权仍有效，
但在上述 trigger 出现前不创建 TPC-207。

本轮启动回归为 `22/22 PASS`。追加的只读核对为：

```text
TPC-111 --check = PASS
TPC-124 --check = PASS
TPC-126 --check = PASS
TPC-127 --check = PASS
```

这些 PASS 只认证各自的 finite identities、counterexamples 与 claim boundaries；
它们不产生 L2。TPC-122 当前脚本没有只读 `--check` 且会写 committed JSON，
本轮只审核其 committed source/JSON，没有执行。TPC-27--32 legacy scripts 同样
未执行。没有创建论文、PDF 或构建日志；既有 TPC-105 `__pycache__`、TPC-63
构建产物与 `tmp/` 均保持原样。

## 24. 下一会话可直接粘贴

```text
进入仓库：
D:\26-aimath\理论研究3\prime_dynamics_theory

读取仓库根目录 TPC_HANDOFF.md，以仓库文件和已提交 artifacts 为事实来源，
不要依赖旧聊天记录。为节省上下文，优先读取页首及第 1、6、22、24、29、30、31、32、33 节；
第 23、27、28 节只在第 29--33 节明确引用时展开。

先执行：

git status --short --branch
git pull --rebase origin main
Get-Content -Raw -Encoding UTF8 TPC_HANDOFF.md

保留 git status 中全部既有 tracked/untracked 工作；不得 reset、checkout、
clean、自动 stash、删除或纳入本轮提交。当前已知 TPC-105 __pycache__、
TPC-63 构建产物、tmp/ 与本地 .codex 配置必须原样保留。若现有工作使
rebase 不安全，停止并报告。

$env:PYTHONDONTWRITEBYTECODE = "1"

完整执行第 1 节 22 项只读启动回归；任一 checker 非零即 fail closed。
TPC-27--32 legacy certificates 会无条件重写 committed JSON，在出现真正
只读 --check 入口前不得执行。TPC-122 也没有安全只读 checker，不得执行。

当前编号事实终点是 TPC-206；TPC-207 trigger=false，TPC-207 未创建。
最新不编号裁决是：

TPC_O161_DIRECT_BAD_ENDPOINT_CURRENT_PRIMARY_ONE_SIGN_OR_AVERAGED_WRONG_OBJECT_
NO_FIXED_POWER_TRIGGER_STOP_SCOPED_PARENTS_OPEN

同一 theorem-valid high-beta selected packet 仍固定为：
sigma=1/10000，lambda=99979/210000，delta=7/60，beta=267/400，
Q=X^(267/400+o(1))，J=X^(133/400+o(1))，C=floor(J)，h0=2，
N0=JQ^2~XQ。delta=1/20 truncated-entry family 是另一条 source lock，
绝不可拼接。

对 actual packet 必须恢复 TPC-18/21/22 的 structured residual mask：

1_{ell_alpha != ell_gamma}
1_{|m_alpha-m_gamma| > Q X^{-kappa_row}}
1_{gcd(d_alpha,d_gamma) <= X^{kappa_row}}.

kappa_row 可取任意 fixed positive value；当前 GM 条件路线要求
0<kappa_row<1/400。它不是 TPC-32 content exponent
kappa_C=133/400，也不提供 small-content saving。

TPC-32/TPC-93 已给 formula-level lossless common-occurrence compiler：
三 raw channels、both-ultra 的两个 1/2 polarizations、content、Delta#、
mask、weights、outer metadata 与 inverse 都可保留。QD 与 formal ordered QZ
可参数化 totalize；但 TPC-144 要求的 metadata-preserving J 仍 STOP：
both-ultra 在 determinant parent 侧聚为一个 record，在 zero side 必须保留
两个 L/R records。actual selected schedule 是否有 nonzero both-ultra
occurrence仍 NOT_TESTABLE；不得把 formal compiler 写成 production intertwiner。

Grimmelt--Merikoski arXiv:2505.00489v2 Part I 的 exact inverse-atom
attachment 是本轮真实 L1 正结果。对

B_t=[[m,(mj+2)/G],[n,(nj+2)/G]],
H_t=2|m-n|/G，g_t=H_t^(-1/2) B_t^+ in SL2(R),

取 alpha1=sum_t conjugate(a_t) delta_(g_t^(-1))、alpha2=delta_I，
用 fixed-margin zero-Haar sign test和足够大的 auxiliary principal level，
可精确返回该 cell 的 literal physical sum。同一 row pair 的 j-arc 在
R1~1 第一槽 self-kernel 中真实逃逸；不得继续引用旧的 J/G arc 作为
这项 inverse placement 的 fatal。

但完整第一槽 self-kernel仍含 gamma=I 的 cross-row compact collisions。
所需 actual coefficient为

w_m=gamma_m^(1) gamma_(m-D0)^(2)
    A_(m,m-D0)(j) K_sh_(m,m-D0)(j),

当前必要的 fixed-`D0` reopen subtheorem 是统一控制

E_Psi=sum_(m,m') conjugate(w_m) w_m'
      Psi((m-m')/D0)

于 fixed physical h0=2、D0、G、j、actual mask、matched shell、outer labels
和 one global normalization。若 E1<=P_X sum|a_t|^2，则最坏
M>=QX^(-kappa_row) 只容许

P_X <= X^(1/400-kappa_row-epsilon+o(1)).

当前 committed corpus 与有限 official-primary screen 均没有这样的 theorem。
fixed-difference common row translations给出精确 compact collision family；
另一 `G=1` family 在 sufficiently comparable determinants 间也落入定理允许的
unit outer ball，不能由 support upper bound排除。它们证明 geometry/mask不会
自动给所需 packing，但不是 actual coefficients 大能量的算术反例。

这条 energy gate无损平方展开后是 prescribed-lag、equal-difference 的 literal
weighted four-Mobius autocorrelation。TPC-93 可无损携带 fixed `D0,G,j` 与 Fourier
phase；但每个 affine key固定 opposite row，方程
`M_theta(t)-n_theta=+/-D0` 至多有一个整数 `t`。所以 fixed-`D0` 的增长方向是
outer `theta` keys，而不是 TPC-108 的 one-column prefix。TPC-93 的 local
row-gcd/smooth projective mass为 `X^o(1)`，global fixed-`D0` transversal mass仍
`UNKNOWN`；TPC-108 H3 与 outer normalization仍未证。

第 31 节进一步把 theorem-parameter-preserving outer regroup 的整数解算完。
固定 `(L/R,ell,ell',j,sigma_aff,v,iota)`，其中
`sigma_aff=sigma_theta` 是 TPC-93 的整数 affine slope、不是 packet
`sigma=1/10000`。令 `A=ell v` 与 `g=gcd(A sigma_aff,ell')`；全部解满足

```text
t=t0+(ell'/g)z,
e=e0+(A sigma_aff/g)z.
```

actual `ell!=ell'`、`d,e~D`、`ell,ell'~L` 与 selected scale给 opposite-cofactor
步长至少 `L/2`，而 `D/L<=X^(-341/1200+o(1))`，故 sufficiently large `X`
仍至多一个点。`g=1` 时新 `z`-determinant为 `ell' h0`，已丢 fixed `h0=2`；
`g=ell'` 时 determinant保留但 occupancy仍 singleton。

唯一自然的 growing lossless coarsening是按 physical moving row `m` 使用
TPC-93 source-child inverse；它精确返回原 coefficient `w_m`，所以 `TT*` 后仍是
同一 literal weighted prescribed equal-difference four-Mobius object，不是新的
TPC-108/TPC-122 prefix。formal fixed-`D0` atomic count最多
`Q X^o=X^(267/400+o)`；actual active census未执行，joint row mask只有 entrywise
bound，故 `X^o(1)` global projective/BV cost未证。

不得用 row degree one、Parseval、large sieve、shift/origin average、裸二点相关、
logarithmic theorem或平均所有 shifts的 Chowla theorem升级。当前 first fatal 是：

LITERAL_EQUAL_DIFFERENCE_EDGE_WEIGHT_NOT_IN_ANY_SCREENED_SOURCE_THEOREM_DOMAIN.

2026-08-01 的 reproducible current-primary screen仍无 survivor。最接近的
Tao--Teräväinen 2512 theorem是 exceptional-scale two-point、只另带 small-modulus
residue-class indicator；Menon 2607
是 average-all-shifts naked k-point；Jaskari--Sachpazis fixed-k-point theorem依赖
Landau--Siegel zero；Gowers/linear-forms theorems既不接受 actual `w_m`，也不把
repeated equal-difference directions与 prescribed `D0`变成合格 finite-complexity
system。Grimmelt--Merikoski 2505.00493v2 只为 Heegner/lower-triangular application
借助 level averaging估计专用 self-kernels，不是 arbitrary literal edge theorem。

post-第 30 节 screen另核对 Carella `2202.01071v5`、Jiseong Kim
`2509.24152v1`、Diao `2506.18065v1` 与 Krishnamoorthy `2501.10962v2`。
Carella Theorem 1.1 的 displayed bound与 proof conclusion不同；Lemma 3.1 的
uniform exponentially-small residue-count error有显式反例，proof还把一般 `t`
无依据地换成 `1`，故该 source proof invalid，不能注册为 theorem input。其余
三项分别是 shift-average、metric almost-all binary forms 与 fake-Liouville/
non-extremal bias，均不接收 prescribed literal `w_m/E_Psi`。Qi
`2404.09085v3`/`2407.17711v1`、Lekkas--Voskou、Pascadi与
Hu--Petrow--Young 的大筛平均 spectral Hecke/Fourier/period data，不给 actual
dense compact cross-`D0` evaluation frame bound。

仅当新 source theorem 直接接受同一 `w_m`，或把 singleton affine children无损
regroup成 genuinely growing blocks且 global projective total variation为 `X^o(1)`，
并支付上述 tiny-power threshold、全部 ranges/constants及 physical-loss ledger时，
才重开
TPC32_H0_2_LITERAL_EQUAL_DIFFERENCE_EDGE_WEIGHT_ONE_PARAMETER_FOUR_POINT_
AUTOCORRELATION_THEOREM_GATE。该 fixed-`D0` subgate即使通过，也只允许继续
审核。comparable `D0,D0'` 的 exact `G=1` matrices仍可落在同一 GM compact
self-kernel support；没有 cross-`D0` block-Bessel/orthogonality theorem。故仍须
另行控制 cross-`D0` 与其余完整 self-kernel，并通过全部 downstream physical/
provenance gates，才可能改变 TPC-207 trigger。

RH-333/334/335 分别是连续 Gaussian probability、folded noisy/flat trace
observation map 与 fixed-order Riesz-projector cell ledger；RH-336 是 projector
mass first-alias scale及 nonphysical 3x3 row-stochastic similarity family，其中
`n=2` 是 operator power，不是 physical `h0=2`。它们均为 wrong object，不得按
同名 physical/alias/projector 符号拼接；RH-336 不单独新增 TPC STOP cell。

RH-338 是 RH frozen far set中的 boundary-orbit finite atom与 signed diffuse
compensation obstruction：`R_orb,k=-D_orb,k`，aggregate far verdict仍
`NOT_TESTABLE`。它没有 `m,m',D0,G,j,w_m,E_Psi,N0`、matched shell、determinant
或 TPC normalization；`2k` 是 orbit/operator order，不是 physical `h0=2`。
因此 `RH338_TO_TPC32_LITERAL_FIXED_D0_E_PSI=ABSENT_WRONG_OBJECT`，不新增
TPC method credit或独立 STOP cell。

最终 fetch还新增 RH-339 的 17 个 files。其 exact object是 lower sideband
`n_minus=2k-2` 上的 signed decomposition
`q_minus=-D_(k-1)_orb+C_minus`；它只证明 isolated orbit atom相对
`H_(k-1)` 发散以及 off-alias vanishing所需的 necessary compensation，完整 signed
`C_minus` 未估，vanishing/nonvanishing仍 `NOT_TESTABLE`。这里 RH 的 “physical”
仍指 Hardy full-trace boundary orbit，`2k-2` 仍是 sideband/operator order；没有
TPC literal coefficient、fixed `D0/h0=2`、matched shell、`N0` normalization或
loss ledger。因此
`RH339_TO_TPC32_LITERAL_FIXED_D0_E_PSI=ABSENT_WRONG_OBJECT`，TPC verdict与
TPC-207 trigger均不变。

第 32 节又完成三个互补的有限 refresh。natural binary-Möbius primary screen无
survivor；最接近的 KMT `2304.05344v2` 确实允许 affine syntax，而且 determinant
prime `2` 条件可用 `mu_odd` 在 literal product上无损修复，不得再以 `mu(2)=-1`
误杀。但其 truncated pretentious-distance hypothesis对 `mu_odd`失败，允许的
epsilon只产生 logarithmic而非 fixed-power output，uniform proposition只覆盖
fixed-A/polylog coefficients，并且没有 actual weights、all-prefix/BV与 `N0`
normalization crosswalk。

metric refresh的 first fatal更早：TPC-32 的 `A_hat_C,q_DFT(0)` 是 normalized
determinant变量的 finite DFT zero，TPC-170 的 `alpha` 是 fiber coordinate `z` 的
additive phase；两者没有 literal intertwiner。`q_X`、`q_prog=as` 与 `q_DFT` 必须
分开。即使反事实补上 intertwiner，named additive atom、actual cross-scale schedule、
exact bad sets与 `alpha_star notin limsup E_n` theorem仍全部缺失。

actual-census refresh则确认：TPC-205 production rows=`0`；TPC-206只是
`X=512, delta=1/4, D0=0` 的 `13/42` finite projection且
`production_occurrence=false`，与本 high-beta packet的 join被显式禁止。TPC-93
source-child inverse只在 supplied retained `omega` 上 conditional PASS；TPC-124 的
`(J Q_D-Q_Z)M=0` 没有 actual common leaf basis/matrices可执行；generic joint mask
也没有 source-backed `X^o(1)` projective theorem。不得通过 finite SVD、one-vector
equality或 atomic triangle补写。

发布前 remote又新增 RH-340（commit `eb1cf19`），但它的 exact object是 RH Hardy
trace-order 上的 `p_(sigma,k,n)=q_(sigma,k,n)-d_(sigma,k,n)` 与
`P_u/E_u/D_u` 三个 `R^n/n`-weighted absolute budgets；moving orders
`2k,2k-2` 不是 fixed physical `h0=2`。其 two-order compensation只是在
`P_(4k)->0` 假设下的必要条件，separate-absolute majorant obstruction又明确不
lower-bound fully signed prefix；aggregate signed cancellation、head与 `E_off` 仍
`NOT_TESTABLE`。没有 TPC literal coefficient、三 raw channels、`C/Delta#`、actual
masks/weights/outer labels、`N0`或 `1/400` ledger，故只新增一个有限
cross-program wrong-object STOP cell，不产生 arithmetic credit。RH-340 的
`build_result.py` 是无 `--check` 的 committed-JSON writer，不得作为只读回归执行。

最终 pull/rebase又取得 RH-341（commit `6e1478a`）。它综合 RH-332--341 后仍把
moving noisy all-order coefficient bridge、aggregate signed prefix、head、`E_off`、
physical determinant与 Gates A--E记为 OPEN/`NOT_TESTABLE`。新增的 cancelling与
noncancelling completions只是 abstract information-class ledgers，明确不是两个
physical noisy operators。这里 `q_(sigma,k,n)` 是 Hardy trace coefficient而不是
TPC modulus，`P_u/E_u/D_u`仍是 absolute trace-order budgets；moving orders相差
`2` 不能冒充 fixed physical `h0=2`。该 source没有 TPC literal coefficient、
三 raw channels、content/`Delta#`、actual masks/weights/outer labels、`N0`或
loss ledger，只新增一个有限 wrong-object/underdetermination firewall，credit仍为零。
其五个 build/verify scripts均无 `--check` 且会写 committed JSON，不得作为本轮
只读验证执行。

随后 remote commit `fd0c65e` 只把 `RH_HANDOFF.md` 的 endpoint/batch/route更新到
RH-341 与 `synchronized_actual_first_alias_signed_completion_open`。这是对既有
RH-341 release的 workflow/provenance closure，不新增 TPC literal object、packet、
theorem或 saving，也不改变上述 cross-program裁决。

第 33 节随后独立审核两个仍开放的 O161 pointwise parents。两者只共享
`c_z=mu(d+s*z)mu(u+a*z), su-ad=2` 的 abstract core；当前
production registry仍为 null/empty，没有 named atom、actual all-scale packet
record、weights/masks/outer labels与 normalization attachment。DIRECT 是
`q/N` terminal/block twist；BAD_ENDPOINT 是经 TPC-159 exact telescoping
形成的 `q/T` cumulative prefix，二者绝不可把 `N=T` 后等同。

current-primary theorem-body screen没有 survivor。el Abdalaoui--Nerurkar
`2006.07646v2` 虽给每个 fixed phase的 ordinary-prefix qualitative
convergence，但 coefficient只有一个 Möbius sign加 `mu^2` masks；
Murty--Vatwani的 rate仍作用于同一 one-sign object、fixed shifts且无 phase。
Grimmelt--Teräväinen `2607.28091v1` 的 growing-coefficient结论依赖
整盒平均；把 coefficient weight取为单 actual tuple的 delta时，
`B^k` threshold与 `delta^(-C)<=B` range使 specialization空洞。
不得跨来源拼接 phase、rate与 coefficient averaging。既有
Teräväinen--Walker/Tao--Teräväinen/Pilatte/KMT routes也仍分别卡在
logarithmic prefix、bad-scale exclusion、averaged/one-factor或 named-atom
缺口；没有 fixed `X` power与完整 ledger。

因此新 cell只冻结第 33 节逐 ID/version列出的 current-primary delta，不扩张
任何旧 STOP cell；两个 O161 parents继续 OPEN。fixed-atom credit仍为零，
strict `1/400`仍 UNPAID，`L2=NONE`。

因此没有创建 TPC-207。合法的新入口仅为：直接接受 actual literal coefficient的
positive-power theorem；直接控制 determinant DFT zero的 pointwise theorem；真正的
named additive atom + actual schedule + same-event avoidance theorem；同 high-beta
packet actual parent registry后再通过 full matrix intertwiner与 source-backed
`X^o(1)` projective theorem；或第 31.6 节既有 full self-kernel/cross-`D0` frame
theorem。任一 data materialization本身至多是新的 L1 gate，不自动产生 L2。

strict 1/400 仍 UNPAID，fixed-atom credit=0，L2=NONE。第 6 节全部旧
method cells保持 STOP_SCOPED；两个 O161 parents、pair-native reroute、H1 与
global architecture继续 OPEN。all-D uniformity、exactly-once physical cover、
original/global normalization、tail-failure、A/B selection、actual packet
attachment 与完整 provenance gates仍独立未过。

持续有限工作流授权仍有效，但没有当前 source-backed theorem trigger时只更新
handoff 并发布精确 STOP_SCOPED；不要创建论文、PDF、paper directory或 TPC-207。
若未来 trigger 真实发生，仍须先完成 TPC-143--206 provenance cascade、受影响
releases 重建、全链 --check、PDF build/render/visual QA，并使页首数学 trigger
发生真实 theorem-backed 状态变化。
```

## 25. 上一轮会话粘贴块（历史，仅供审计；不得作为当前入口）

```text
进入仓库：
D:\26-aimath\理论研究3\prime_dynamics_theory

读取仓库根目录 TPC_HANDOFF.md，以仓库文件而不是旧聊天记录为事实来源。
先执行：

git status --short --branch
git pull --rebase origin main

$d = "papers/tpc-206-selected-lineage-pair-registry-projection/experiments"
python "$d/build_tpc206.py" --check
python "$d/tpc206_selected_lineage_pair_registry.py" --check
python "$d/tpc206_independent_checker.py" --check

$p = "papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments"
python "$p/build_tpc205.py" --check
python "$p/tpc205_pair_native_registry_interface.py" --check
python "$p/tpc205_independent_checker.py" --check

python -B papers/tpc-133-executable-native-entrance/experiments/tpc133_native_entrance.py --check
python -B papers/tpc-134-boundary-complete-dyadic-prefix-tail-archive/experiments/tpc134_branch_archive.py --check
python -B papers/tpc-135-tpc17-tpc18-block-frontier/experiments/tpc135_domain_cover_audit.py --check
python -B papers/tpc-136-complete-native-cut-archive/experiments/tpc136_cut_archive.py --check

python papers/tpc-184-bad-endpoint-literal-target-contract/experiments/tpc184_bad_endpoint_literal_target_contract.py --check
python -O -B papers/tpc-184-bad-endpoint-literal-target-contract/experiments/tpc184_bad_endpoint_literal_target_contract.py --check
python papers/tpc-189-direct-twist-literal-target-contract/experiments/tpc189_direct_twist_literal_target_contract.py --check
python -O -B papers/tpc-189-direct-twist-literal-target-contract/experiments/tpc189_direct_twist_literal_target_contract.py --check

foreach ($s in @(
  "papers/tpc-173-production-source-claim-inventory/experiments/tpc173_source_claim_inventory.py",
  "papers/tpc-174-local-occurrence-edge-witness-schema/experiments/tpc174_witness_contract.py",
  "papers/tpc-175-declared-corpus-local-edge-family/experiments/tpc175_local_edge_family.py",
  "papers/tpc-176-source-backed-coverage-gluing-audit/experiments/tpc176_coverage_gluing_audit.py",
  "papers/tpc-177-actual-active-support-vacuity-firewall/experiments/tpc177_active_support_audit.py",
  "papers/tpc-178-canonical-minimal-representation-eligibility/experiments/tpc178_representation_audit.py",
  "papers/tpc-179-h1-structural-corpus-exhaustion-integration/experiments/tpc179_h1_integration.py"
)) {
  python -O -B $s --check
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

当前编号事实终点仍是 TPC-206；TPC-207 trigger=false，TPC-207 未创建。
本轮完成
TPC18_S_EQUALS_2_NONPRIMITIVE_ENDPOINT_SOURCE_FORWARD_GATE。

TPC-18 的精确公式是
beta_I(k)=sum_{d|k,D0<d<=V}mu(d)。对h0=s=2，
Omega_2(e)=1_{D0<e<=V}-1_{D0<2e<=V}，只允许同一common k上的
beta_I(k)^2；different-k opened rows不得合并。

通用公式并不恒零：纯代数候选(D0,V,k,e)=(6,18,22,11)给
Omega_2(11)=1、beta_I(22)=-1。但它没有theorem-valid physical schedule、
具名source pair、cutoff nonzero、packet/cut locator或source-forward
occurrence，只能记为L0 formal candidate。

当前source-locked TPC-133 packet固定D0=0,V=2。虽然有10个同偶数k的
prime-source formal fibers、80 ordered/40 unordered formal pairs，但
I={1,2}，故每个偶数k都有beta_I(k)=mu(1)+mu(2)=0。source-locked
h0=2 beta-nonzero records=0，materialized source-locked h0=2 nonzero
per-k endpoint records=0。

TPC-136四张downstream maps仍空；TPC-143的2,988个actual_map_edges全空；
TPC-153的2,988个actual occurrence IDs全缺；TPC-154的8,967条edges全为
formal，theorem-backed actual provenance=0。TPC-205/206的k=24与48
不得拼接。registry新增字段=0、actual occurrence IDs=0、projection仍
13/42、field-order first missing仍是D。

TPC-18 finite certificate固定h=6,D0=6,V=18，只是exact algebraic regression，
明确prime_asymptotic_evidence=false；它不是h0=2 actual source-forward
record。stopping theorem也只对满足geometry的抽象block，在额外
tail-failure lower bound假设后给primitive A / nonprimitive B至少一个成立；
它不供应具名source-locked block或tail failure。当前没有theorem排除A或
直接选择s=2的B。
endpoint localization本身不推出剩余correlation小量。

新增且仅新增：
DECLARED_TPC18_H0_2_COMMON_K_ENDPOINT_SOURCE_FORWARD_RECORD_CORPUS_V1
=STOP_SCOPED。

保持第 6 节全部旧 cells（尤其 TPC193 V1）为 STOP_SCOPED；保持两个
O161 parents、pair-native reroute、H1 与 global architecture OPEN；
fixed-atom credit=0、strict 1/400 UNPAID、L2=NONE。

本轮pull为already up to date，没有新增primary TPC theorem source。
TPC-206/205/194、TPC-133--136、TPC-184/189 normal/optimized与
TPC-173--179 optimized全部通过。

扩展回归发现TPC-143 --check在certificate-only provenance上DRIFT：
2,988 obligations字节完全相同，12个漂移leaves只把TPC-134--136旧
raw-hash bindings从stale更新为canonical match；semantic/census/claim
字段变化为0。刷新会纯hash级联经过TPC-143--206并触及已发布release
manifests，故本次数学gate没有静默重写它。该漂移不改变零occurrence裁决，
但下一篇编号论文发布前必须完成全链provenance cascade、受影响release
重建和全部--check。
PROVENANCE_CASCADE_REFRESH_REQUIRED_BEFORE_NEXT_NUMBERED_RELEASE=YES。

无需再请求单独工作流授权。下一项有限不编号architecture gate为：
TPC18_H0_2_NONPRIMITIVE_ALTERNATIVE_SELECTION_AND_ACTUAL_PACKET_ATTACHMENT_GATE。
先source-lock theorem-valid h0=2 block与actual tail-failure input；再由
新theorem排除primitive A或直接下界s=2的B；然后才冻结同一common k、
beta_I(k)!=0、named endpoint coefficient、source pair与actual packet/cut
locator。前三关通过后才审source-forward registry、normalization和完整
physical-loss ledger。禁止formal->actual、endpoint localization->smallness。

主会话只保留结论、路线选择、阻断项和最终审核摘要；长扫描、定理原文
核查、schema exploit review、构建日志和逐页 PDF 检查交给分身；所有
正式写入由主会话协调。
```

## 26. 上一轮下一会话粘贴块（历史，仅供审计；不得作为当前入口）

```text
进入仓库：
D:\26-aimath\理论研究3\prime_dynamics_theory

读取仓库根目录 TPC_HANDOFF.md，以仓库文件而不是旧聊天记录为事实来源。
先执行：

git status --short --branch
git pull --rebase origin main
Get-Content -Raw -Encoding UTF8 TPC_HANDOFF.md

保留 git status 中全部既有 tracked/untracked 工作；不得 reset、checkout、clean、
自动 stash、删除或纳入本轮提交。当前已知 TPC-105 __pycache__、TPC-63 构建
产物和 tmp/ 必须原样保留。若这些工作使 rebase 不安全，停止并报告。

$env:PYTHONDONTWRITEBYTECODE = "1"
完整执行 TPC_HANDOFF.md 第 1 节当前列出的完整只读启动回归（现为 22 项）；
任一 checker 非零即 fail closed。TPC-27--32 legacy certificates
会无条件重写 JSON，在出现真正的只读 --check 入口前不要执行。

当前编号事实终点是 TPC-206；TPC-207 trigger=false，TPC-207 未创建。
上一轮不编号裁决是：
TPC18_H0_2_FULL_R_R_PRIMITIVE_A_TRUNCATED_ENTRY_AND_SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_ABSENT_STOP_SCOPED_NOT_REOPENED。

上一轮已纠正“ultra complement 只等于 u,v>T”的不完整说法。若
A_m,T=sum_(u<=T,u|mj+2)b_R(u)，C_m=sum_(T<u<=U0,u|mj+2)a(u)，则
full raw complement 的精确 domain 是 u,v<=U0 且 max(u,v)>T，并含三条：
A_m,T C_n、C_m A_n,T、C_m C_n。TPC-29 calibrated difference 另有两条
power-small drift legs；没有遗漏或重复的 two-drift 项。

TPC-29 关闭 content-rich selected-divisor sectors，TPC-30 关闭 large full-
target-content，TPC-31/32 把 selected packet 的唯一 hard cell 精确压缩为
A_hat_C,q(0)=small-content matched-shell auxiliary determinant zero。它不是
orbit Poisson zero；TPC-27 已关闭的 additive zero 不供应它。TPC-32 只有在
F0(A_C)<=X^(chi+o(1)), chi<=1/400 的额外 premise 下才关闭 complete matched
shell；该 premise 未证。TPC-116 的 aggregate physical saving 1/400 也不是
这个 squared-flatness loss，严禁字段等同。

上一轮 sigma=1/1000、delta=1/20 exact family 还有更早的入口 fatal：
lambda=9979/21000，R exponent=9/20，beta in
[5479/10500,1838/2625]。TPC-26/28 的 positive-minimax upper cutoff 在全部
slices 上最多只有 exponent 2/5<R；不存在 R<=S<T 且 M_beta(t)>0。
S=R 时最佳 M 仍是 -1/12。强取 T<R 会使 lambda'_R 留在 shell 中并破坏
b_R=a，不是合法修补。TPC-28 的 high-beta theorem-valid selected sample 是
另一 source lock，也只关闭一个 D-packet；不得拼接，更不排除 all-D witness。

TPC-18 row-Cauchy/energy 仍只给 XQ X^epsilon natural scale；reflected unit
fiber r=s=1 留下 ordinary two-point Mobius correlation。TPC-108 H3 仍是未证
L2。新增 Menon arXiv:2607.15574 仍是 origin-averaged、phase-uniform short
sums / shift-averaged correlations；Ramaré--
Zuniga Alterman arXiv:2603.25961 是 static LCM double sum。它们与所有复核的
logarithmic、almost-all、exceptional-scale、size-only candidates 均不提供
all-slice full r_R r_R theorem。本轮无 reopen trigger，无 TPC-207。

本轮新增的 DECLARED_TPC18_H0_2_FULL_R_R_PRIMITIVE_ULTRA_COMPLEMENT_CORPUS_V1
为 STOP_SCOPED；第6节所有旧 cells 继续 STOP_SCOPED。两个 O161 parents、
pair-native reroute、H1 与 global architecture OPEN；fixed-atom credit=0、
strict 1/400 UNPAID、L2=NONE。

本轮执行下一项有限不编号 gate：
TPC32_H0_2_SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_SIGNED_PREFIX_TRANSFER_GATE。

先 source-lock TPC-28/32 的同一个 theorem-valid selected h0=2 packet、三 raw
channels、content C、canonical Delta#、actual masks/weights 与 packet natural
scale N0=JQ^2\asymp XQ；再逐式
测试 TPC-111/122 ordered signed-prefix/BV 对象能否无损映射到同一个
A_hat_C,q(0)。determinant、content、outer labels、prefix order 或 normalization
任一不一致即 fail closed。只有 source-backed growing prefix theorem 真正推出
chi<=1/400，或直接给 small-content matched-shell saving，才算 arithmetic
advance。即使 selected packet 通过，all-D uniformity、physical cover、global
normalization、tail-failure、B selection 与 actual attachment 仍须分别审核。

对任何候选 theorem 逐项核查 literal physical coefficient、固定 physical h0、
summation domain、prefix index、X/N/q 与全部参数范围、uniform constants、
normalization 和完整 physical-loss ledger。禁止 block/cumulative 强行等同、
logarithmic-to-natural 偷渡、complete-frequency mean 升级为 prescribed phase，
或把第 6 节旧 STOP_SCOPED cell 重新包装成新方法。

本 gate 即使得到 selected-packet 正面结果，也不自动创建 TPC-207。只有 all-D
uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual attachment 与完整 provenance gates 均通过，
并使页首 `TPC-207 数学 trigger` 发生真实 theorem-backed 状态变化后，才可进入
编号 release。

下一篇编号论文发布前仍必须完成 TPC-143--206 的完整 provenance cascade、
受影响 releases 重建和全链 --check；certificate-only drift 不得冒充数学触发。

主会话只保留结论、路线选择、阻断项和最终审核摘要；长扫描、定理原文
核查、schema exploit review、构建日志和逐页 PDF 检查交给分身；所有正式
写入由主会话协调。若没有真实 theorem trigger，更新本交接并 STOP_SCOPED，
不要创建论文、PDF 或下一编号。

若形成正式编号 release：再次 git pull --rebase origin main，完成 provenance
cascade、受影响 releases 重建、全链 --check、PDF 构建及逐页 render/visual QA；
只提交本轮预期文件，执行 git push origin HEAD:main，并用 git rev-parse HEAD、
git rev-parse origin/main、git ls-remote origin refs/heads/main 核对三个 hash
完全一致。若只形成 STOP_SCOPED 审计结果，也按同样
的提交、推送和三引用核对纪律发布交接记录。
```

## 27. 第 23.5 节 post-seal primary-source reopen-trigger 审计

### 27.1 冻结基线、对象与有限来源集

本轮从下列一致基线启动：

```text
HEAD = origin/main = 3c798823c313bdae1678bb46a9655bac1770f4ff
TPC_HANDOFF_SHA256_BEFORE_EDIT
  = 08ff16ad29f769163951471e19bf6c26ce9d1db24accdaa0ee172265b8167a9f
STARTUP_REGRESSION = 22/22 PASS
TPC111_124_126_127_READ_ONLY_GATE_CHECKS = 4/4 PASS
```

三个只读审核分别覆盖第 23.5 节的 actual intertwiner、direct actual-`A_C`
theorem，以及 growing signed-prefix + outer BV + content remainder 路线；三个审核
的 `files_changed=[]`。同一 selected packet、固定 `h0=2`、三 raw channels、
`C=floor(J)`、`G<=C`、`Delta#`、actual masks/weights、outer labels 与
`N0=JQ^2 asymp XQ` 均继续按第 23.1 节冻结。`delta=1/20` exact family 没有
参与，且不得与此 high-beta packet 拼接。

本轮逐 theorem 核查的有限 primary-source 集为：

1. Banks--Shparlinski, *Multiple sums with the Möbius function*,
   `arXiv:2506.08787v1`, Theorems 2.1/2.4 与第 7.6 节；该来源此前已在第
   15.3 节及 TPC-43 标记为不同对象，本轮只对第 23.5 节三个 trigger 做精确
   re-type-check；
2. Verjovsky, *Local Moments of Möbius Fourier Polynomials and the Riemann
   Hypothesis*, `arXiv:2607.25002v1`, Theorem 1.3 与 Proposition 3.2；
3. Ford--Radziwiłł, *Sign changes of the Liouville function in arithmetic
   progressions*, `arXiv:2605.03349v1`, Theorem 1；
4. Matomäki--Teräväinen, *Linnik's problem for multiplicative functions*,
   `arXiv:2605.27833v1`, Theorems 1.1/1.2 与 Corollary 1.3。

已声明 git refs 的 source-forward 核查仍没有找到 actual `Q_D/Q_Z` map。Tao--
Teräväinen natural-block/log-density、Menon origin/shift-average、Pilatte single-factor
origin-average、fixed/logarithmic Chowla、nilsequence、metric/random-family、
conditional Landau--Siegel-zero 与 static LCM 候选仍落在第 6 节既有
`STOP_SCOPED` cells；本轮没有给这些旧方法换名或扩张 scope。

### 27.2 literal-object 与 theorem-output 字段矩阵

actual target 仍是

```text
A_C(n) = S_sh(G<=C, Delta#=n),
A_hat_C,q(0) = sum_n A_C(n) = S_sh(G<=C),
F0(A_C) <= X^(chi+o(1)), chi<=1/400,
```

或同一 small-content matched shell 在 `N0` scale 上的直接 fixed-power saving。
四个候选逐项结果如下：

| 必核字段 | Banks--Shparlinski | Verjovsky | 两个 AP sign-existence sources |
|---|---|---|---|
| literal physical coefficient | `u_n1 v_n2 mu(n1 n2 n3)`；第三变量位于不可预先因子化的单一 Möbius factor 中，且两权重可分离 | 一般命题为 `sum a_n e(nt)`, `abs(a_n)<=1`；Möbius 特化只有单个 `mu(n)` | 单个 `lambda(n)` 或 squarefree `mu(n)` 的符号 |
| fixed physical `h0=2` | 没有同一 divisibility pair；冻结第三变量会落到来源明确未解决的 `H=1` binary/Chowla 型情形 | 没有 shift 参数 | 只固定 AP residue class，不固定 actual 两条 affine forms |
| domain 与 prefix index | 三区间变量上的一个 additive level set；给 complete/terminal scalar sum，不给每个 canonical prefix | contiguous Fourier index；local moment 到一个 terminal point，不给 actual ordered fibers 的 all-prefix | 只断言某阈值前存在两种符号；没有 signed sum、prefix 或 correlation quantity |
| determinant/content/outer labels | 没有 `G<=C`、`Delta#`、三 raw channels或 `(alpha,gamma,j)` keys | 全部没有 | 全部没有 |
| masks/weights 与 factor allocation | 只有两组 separable bounded weights；不能承载 actual joint pair mask 与三-channel tensor | 只有抽象 bounded coefficients；无 physical lineage | 无 actual weights、masks、factor allocation |
| `X/N/q` ranges | 文献自己的 `A,B,N,H`；short form 要求 growing `H`，不是 singleton physical shift | degree `N`、arc radius `r`、moment order `q`；该 `q` 不是 auxiliary modulus | AP modulus `q`；不得与 TPC no-wrap Fourier modulus同名偷换 |
| uniform constants | 对文献 data 的 uniformity不等于全部 actual outer fibers 的共同常数 | `C_q` 依赖 moment order；没有 actual-family local-moment input | threshold/constants只服务 sign existence，不服务 weighted sums |
| normalization | `(A+B)N(log N)^(-C)` 或相应 short sum；无 `N0` crosswalk | classical `P_N=N^(-1/2) sum mu(n)e(nt)`；无 `N0` crosswalk | 最小 sign witness scale `q^(5/2+eps)` 或 `R(mu;q)<<q^(2+eps)`；不是 shell normalization |
| physical-loss ledger | 只有 fixed-`C` log saving，无 `1/400` credit | deterministic wrapper不提供 local high-moment bound；RH-equivalent specialization不是 unconditional input | 两种符号存在允许其余项几乎全同号，故没有任何 cancellation exponent |

Banks--Shparlinski 的 arbitrary weights 不能修复首项：literal factor 是
`mu(n1 n2 n3)`，`u`、`v` 只依赖前两个变量，故其中的 `n3`-dependence 不能
由这两组 weights 消去；把第三变量冻结到 singleton 正是其第
7.6 节明确仍 out of reach 的 `H=1` 情形。即使反事实存在 literal crosswalk，
固定 `C` 的 log saving 仍是 `X^(-o(1))`，不能选择 `C=C(X)` 偷渡成 fixed
power。

Verjovsky Proposition 3.2 是确定性的 one-way implication。对任意 bounded
trigonometric polynomial，它把已知 local `B_q` 控制转成一个点值控制；它本身
不证明任何 `B_q` upper bound。把 actual `A_C` 平移、zero-pad 并归一化只能得到
一个以 same-actual-`A_C` local high moment 为前提的条件式，而该前提正是未证
算术输入。Theorem 1.3 则是 classical single-Möbius polynomial 的 RH 等价表述，
不是 actual coefficient theorem。Parseval 或 global `L2` 不能制造 distinguished
zero，也不能同时统一控制全部 canonical prefixes。

Ford--Radziwiłł Theorem 1 对 prime AP modulus 给出 `q^(5/2+eps)` 前各一个
Liouville 正、负值。Matomäki--Teräväinen Corollary 1.3 对 Möbius 给出

```text
R(mu;q) << q^2 (L(q)^100 + B(q)) <<_eps q^(2+eps),
```

即每个 reduced residue class 内各有一个 squarefree 正、负值；其一般 theorem
另带 real-character pretentious alternative。两者的 output 都是 existence，严格
弱于 signed-sum balance：一个长度 `L` 的序列即使 `L-1` 项同号、仅一项异号也
满足它们的结论。因此它们对 `F0(A_C)`、matched shell 或 growing maximal prefix
没有定量蕴含。Ford--Radziwiłł Lemma 7 中每个长度 `q` 区间正负各半的结论以
“指定 AP 截至 `N` 全部同号”的反证假设为前提，该假设随后被推翻，不能抽成
unconditional block theorem；即使保留该条件计数，它也不控制区间内部的
canonical order。Matomäki--Teräväinen 证明中的 sign-filtered convolution 是对
正、负目标分别构造的非负 representation count，两套计数没有相减，故也不产生
signed-prefix cancellation。

### 27.3 三个 reopen triggers 与完整 loss 状态

Trigger 1 首先在仓库 actual map input 处失败：

```text
TPC144 Q_D.actual_map_edges = []
TPC144 Q_Z.actual_map_edges = []
TPC144 J_QD_equals_QZ = NOT_TESTABLE
TPC144 literal_fiber_relabeling = NOT_TESTABLE
TPC155 production_witness_present = false
TPC175 qualifying_claim_count = 0
TPC175 eligible_carrier_count = 0
```

所以 `(J Q_D-Q_Z)M=0` 目前连共同 native-leaf matrix 与两组 actual maps 都无法
形成。scalar equality、一般 kernel criterion、local moment inequality或 sign
existence theorem 都不构造 metadata-preserving `J`。精确 first fatal 为：

```text
COMMON_ACTUAL_LEAF_DOMAIN_AND_LITERAL_Q_D_Q_Z_MAPS_ABSENT
```

Trigger 2 也失败。四个来源均不直接控制同一 actual `A_C`；没有同一对象的
denominator lower input，也没有

```text
F0(A_C) <= X^(chi+o(1)), chi<=1/400,
```

或 `N0` scale 上的 direct small-content matched-shell fixed-power saving。

Trigger 3 独立失败。没有候选同时给出：

```text
all actual retained ordered fibers and every canonical prefix,
uniform outer BV envelope,
content remainder with a fixed exponent,
common growing X/N/q ranges and uniform constants,
N0-to-global normalization crosswalk,
complete physical-loss ledger.
```

本轮最终 gate matrix 为：

```text
TRIGGER_1_ACTUAL_COEFFICIENTWISE_INTERTWINER = FAIL_CLOSED_ABSENT
TRIGGER_2_DIRECT_ACTUAL_A_C_OR_MATCHED_SHELL_THEOREM = FAIL_CLOSED_ABSENT
TRIGGER_3_GROWING_PREFIX_BV_CONTENT_LEDGER = FAIL_CLOSED_ABSENT

SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
H0_2_SPECIALIZATION = PASS_THEOREM_LEVEL_NOT_JSON_SERIALIZED
ACTUAL_GENERIC_PAIR_MASK_DECOMPOSITION = ABSENT
N0_TO_Q_X_SQUARED_NORMALIZATION_CROSSWALK = ABSENT
CHI_LE_1_OVER_400 = UNPAID
FIXED_ATOM_CREDIT = 0
ARITHMETIC_ADVANCE = NO
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

### 27.4 精确 STOP scope、开放父节点与发布验证

精确裁决为：

```text
TPC32_23_5_LOCAL_MOMENT_AND_AP_SIGN_EXISTENCE_TO_ACTUAL_ZERO_OR_
GROWING_PREFIX_INPUT_ABSENT_STOP_SCOPED_NOT_REOPENED
```

本轮新增且仅新增第 6 节的：

```text
DECLARED_TPC32_23_5_NAMED_PRIMARY_REOPEN_CANDIDATES_20260731_V1
  = STOP_SCOPED
```

这不是 actual intertwiner、direct `A_C` theorem 或 growing-prefix theorem 的
nonexistence claim；它只冻结第 27.1 节四个来源的已审核版本与上述 exact
crosswalk attempts。来源的新版本、真正逐 coefficient 保留全部 physical data 的
corollary，或第 23.5 节任一原始 trigger 仍可重开。两个 O161 pointwise parents、
pair-native reroute、H1 与 global architecture 继续 `OPEN`。第 6 节全部旧 cells
继续原样 `STOP_SCOPED`，尤其 TPC193 V1、common-`k` V1、tail-failure/A/B V1
与 full-`r_Rr_R` ultra-complement V1。

all-`D` uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual packet attachment 与完整 provenance gates
没有进入，更没有通过。即使第 23.5 节未来出现正面结果，也必须分别支付这些
下游 gates，才可能改变页首 TPC-207 trigger。

发布前已再次执行 22 项只读启动回归，结果为 `22/22 PASS`；TPC-111/124/
126/127 四项 gate checks 为 `4/4 PASS`。TPC-122 与 TPC-27--32 writers 均未
执行。没有创建论文、paper directory、PDF、构建日志或下一编号。根
`AGENTS.md` 已按用户明确授权合并为 RH/TPC scoped 政策，并作为只含该文件的
独立协调提交纳入；本 TPC STOP handoff 提交只含 `TPC_HANDOFF.md`。既有本地
`.codex/config.toml`、`.codex/agents/tpc-*.toml`、TPC-105 `__pycache__`、TPC-63
构建产物与 `tmp/` 仍保持 untracked，未纳入上述任一本地提交。

## 28. 2026-08-01 current-primary theorem-route 与 exact attachment 审计

### 28.1 冻结基线、目标与审计协议

本轮从下列一致基线启动：

```text
HEAD = origin/main = 5e97b52b54d33f2ec34c68efdb9737f8959a3345
TPC_HANDOFF_COMMITTED_BLOB_BEFORE_EDIT
  = 8a5b2ebf37390bcd9b92000938ab1f57c29ff8be
TPC_HANDOFF_SHA256_BEFORE_EDIT
  = b9047e39fdb11f295c8f0510bf6c3b12b24c07c079ecb1bdc4c111b96bf3ff31
STARTUP_REGRESSION = 22/22 PASS
TPC111_124_126_127_READ_ONLY_GATE_CHECKS = 4/4 PASS
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
```

protected manifest 是按 `git ls-files --others --exclude-standard` 排序后，对每个
文件记录 `path<TAB>byte_length<TAB>sha256<LF>`，再对含末尾换行的全部 rows 做
SHA256。三份独立只读审计分别承担 actual source lock/formula crosswalk、
from-actual formula-directed theorem attachment，以及 systematic current-primary
source discovery/adversarial theorem screen；三份结果均为 `files_changed=[]`，
且共同结论为 `NO_NEW_TRIGGER_CANDIDATE`。

同一 theorem-valid selected packet 精确冻结为：

```text
sigma = 1/10000
lambda = 99979/210000
delta = 7/60
beta = 267/400
Q = X^(267/400+o(1))
J = X^(133/400+o(1))
D = X^(10049/52500+o(1))
L = X^(99979/210000+o(1))
R = S = X^(23/60+o(1))
V = X^(23/120+o(1))
T = X^(193/500+o(1))
C = floor(J)
h0 = 2
N0 = J Q^2 asymp X Q
```

literal row coefficient、joint multiplier 与三 raw channels 仍分别是：

```text
gamma_alpha^(i)
  = mu(d_alpha) (log ell_alpha) omega_D^(i)(d_alpha)
    psi_L^(i)(ell_alpha/L) zeta_alpha^(i),

A_frak_(alpha,gamma)(j)
  = m_frak(alpha,gamma) Xi_(alpha,gamma)(j)
    W_(alpha,gamma)(j/J),

A_{m,T} C_n,
C_m A_{n,T},
C_m C_n,
```

并且必须保留 matched difference
`A_{m,U0}A_{n,U0}-A_{m,T}A_{n,T}`、actual masks/weights 与 outer labels。
令 `q_DFT` 表示 TPC-32 的 no-wrap auxiliary determinant-DFT modulus
（`q_DFT asymp Q`；下述 distinguished zero 的值不依赖这个 auxiliary
modulus），并令

```text
G = gcd(m_alpha j+2, m_gamma j+2),
Delta# = (m_alpha-m_gamma)/G,
A_C(n) = physical matched shell restricted by G<=C and Delta#=n,
A_hat_C,q_DFT(0) = sum_n A_C(n)
                 = small-content matched-shell auxiliary zero.
```

本轮所需 output 仍只能是

```text
F0(A_C) = |A_hat_C,q_DFT(0)|^2 / ||A_C||_2^2
        <= X^(chi+o(1)), chi<=1/400,
```

或同一对象的 robust direct form

```text
|sum_n A_C(n)|^2
  << X^(1/400-eta) sum_n |A_C(n)|^2
```

with some fixed `eta>0` and a complete physical-loss ledger。为避免与 TPC-32 的
auxiliary DFT modulus 混淆，以下把 TPC-127 的 progression modulus 记为
`q_prog=as`。TPC-127 的 complete literal pullback 是

```text
S_{xi,X}(alpha)
  = lambda(q_prog) sum_{n in N_I}
      Qcal_{a,s}(n) lambda(n-2) lambda(n)
      Wcal_{xi,X}(n) exp(-2 pi i alpha z(n)).
```

它无损保留同一 progression finite list 上的 canonical prefix 与 comparison mass；
该恒等式本身不是新的 cancellation theorem。
`delta=1/20` truncated-entry-absent family 未参与，且不得与本 packet 拼接。

### 28.2 系统检索、版本审计与有限性边界

截至 2026-08-01，一个只读 discovery station 的未归档运行日志报告：对 arXiv
`math.NT` 的 Möbius/Moebius、Liouville、Chowla、multiplicative functions、
partial sums、variation norm、shifted convolution 与 divisor correlation 查询
得到 394 条重叠 retrieval rows；按 base arXiv ID、normalized title 与 DOI 合并
后，22 条进入 title/abstract relevant set，12 条进入 theorem/main-result screen，
0 条通过 exact attachment 初筛。该站没有提交 raw retrieval roster、22/12-item
source-ID sets 或 query manifest，所以这些数字只作为一次性 process log，不是
可复算的 corpus-completeness certificate。general web 只用于 discovery；正式
判断使用 arXiv abstract/HTML/PDF 与 journal/DOI primary metadata。

另一条从 actual formula 倒推的定向审核还逐式检查了 Tao--Teräväinen
`arXiv:2512.01739v2` Theorem 3.1、Koukoulopoulos `arXiv:2605.01412v1`
Theorems 1.1/1.2 与 Pozdnyakov `arXiv:2604.23427v1` Theorem 1.8。它们未计入
前述 retrieval-pipeline counters；在没有两轨 source-ID roster 时，本节不宣称
两轨互斥，也不把 `12` 与 `3` 相加，只报告两轨合并裁决仍为 0 survivor。本节
只陈述这个明确、有日期和版本号的有限审核集，不声称不存在未发现文献、未来
版本或未来定理。

第 27 节四个 frozen sources 的官方版本历史未改变：Banks--Shparlinski
`2506.08787v1`、Verjovsky `2607.25002v1`、Ford--Radziwiłł
`2605.03349v1` 与 Matomäki--Teräväinen `2605.27833v1` 均仍为 v1；Banks--
Shparlinski 的 QJM publication 与 arXiv work 按 title/DOI 去重，官方摘要仍保留
binary obstruction。第 27 节 dated cell 因而不重开。

### 28.3 最接近来源的 formula-level 排除

1. Tao--Teräväinen `arXiv:2512.01739v2`, Theorem 3.1，确实给两点
   1-bounded multiplicative-function correlation 的小对数幂节省；Liouville
   corollary 允许 distinct affine forms，但 coefficients/moduli 只到
   `log^c N`，且只在一个小 exceptional scale set 外控制 complete terminal sum。
   它的 literal object 是 naked
   `lambda(a1 n+b1)lambda(a2 n+b2)`，没有 `Q_{a,s}`、三 channels、joint
   masks、`G<=C`、`Delta#`、outer labels、prescribed packet scale 或 all-prefix。

2. Matomäki--Radziwiłł--Shao--Tao--Teräväinen Higher Uniformity II
   `arXiv:2411.05770v2`, Theorem 1.1，具有最接近 maximal/all-subprogression 的
   syntax，但其 arithmetic coefficient 是单个 `mu(n)`，或单个近似残差
   `(Lambda-Lambda#)(n)`、`(d_k-d_k#)(n)`，对 bounded-complexity
   nilsequence，并允许 exceptional interval origins。没有 theorem 证明 actual
   complete coefficient
   `Qcal_{a,s}(n)lambda(n-2)lambda(n)Wcal_{xi,X}(n)
   exp(-2 pi i alpha z(n))` 是其同一 admissible coefficient，也没有 fixed-power
   actual-packet saving。

   在没有新增 same-object theorem/crosswalk 时，不得把第 1 项的 naked pair
   theorem 与本项的 single-factor maximal theorem 拼接：两者不是同一个 theorem
   statement，没有共同 literal coefficient、domain、exceptional set、constant、
   normalization 或 loss ledger。

3. Grimmelt--Merikoski `arXiv:2404.08502v2`, Theorem 1.1，最接近 determinant
   geometry：它计数 determinant-one matrices，允许 left-`Gamma`-automorphic
   orbit weight 与 smooth dyadically supported test weight。其 error 为
   `delta^(-O(1)) Z^epsilon sqrt(A D K R)`；当前没有 coefficientwise map 把
   actual three-channel packet、content、outer labels 与 prefix order 送入该
   automorphic object，也没有证明所得 weight 的 `Gamma` invariance。actual
   encoding 的 `K` bound、`R`/range/smoothness crosswalk 与完整 loss ledger
   均未给出，会重新引入未支付的 correlation problem。

4. Kim `arXiv:2603.23250v2`, Theorem 1.6，在 `f1 in F'_k(alpha)`、`f2,f3`
   为 `k`-divisor-bounded，且
   `X^((1+alpha)^2/((1+alpha)^2+1)+100 epsilon) << H << X^(1-epsilon)`
   时，给 Fejer-weighted ternary correlation 的 shift-average power saving；它
   不控制 prescribed physical `h0=2`，也没有 actual masks/channel attachment。

5. Cantarini `arXiv:2607.09110v1`, Theorems 22/24，虽有 fixed-power headline，
   literal coefficient 是带 modulus/character average 的 `Lambda`--`mu` additive
   convolution，且依赖 GRH 与额外 zero conjecture；它不是 actual two-affine
   Möbius joint coefficient。

6. Fragkos--Krause--Miheisi--Sun `arXiv:2607.05560v1` 是 prime Carleson
   operator 的 variation norm；Lau `arXiv:2509.07556v2` 是 generalized-divisor
   shifted convolution；Koukoulopoulos `arXiv:2605.01412v1` 是从 partial-sum
   smallness 假设推出 structure 的 inverse input；Pozdnyakov
   `arXiv:2604.23427v1` 是单 `mu` 对 digital character 的 terminal estimate；
   Chavez `arXiv:2409.02106v10` 是 RH/simple-zero 条件下的 logarithmic
   multiplicative-function-times-cumulative-sum object。它们分别首先失败于 operator/
   kernel、literal coefficient、implication direction、domain/prefix 或 cumulative
   normalization，不能产生 distinguished auxiliary zero。

7. Pilatte `arXiv:2604.26564v1` 的 single-Liouville Fourier theorem 仍平均 interval
   origins；Higher Uniformity I、Menon、Banks--Shparlinski、Verjovsky 与两个 AP
   sign-existence sources 仍由第 6、27 节原有精确 cells 管辖。本轮只做 version/
   trigger type-check，不把这些旧 `STOP_SCOPED` 方法重新包装成新方法。

所有候选均逐项核查 literal physical coefficient、固定 physical `h0`、summation
domain 与 prefix index、`X/N`、auxiliary `q_DFT` 与 progression `q_prog` 的各自
参数范围、uniform constants、normalization 与
完整 physical-loss ledger。任何一项不一致即 fail closed；没有使用 block/cumulative
强行等同、logarithmic-to-natural 转换、averaged-to-prescribed 升级或
complete-frequency-to-distinguished-zero 升级。

### 28.4 仓库 first fatal、trigger matrix 与可重开接口

仓库内部在调用任何候选 theorem 前已经出现 first fatal：

```text
TPC144 Q_D.actual_map_edges = []
TPC144 Q_Z.actual_map_edges = []
TPC144 J_QD_equals_QZ = NOT_TESTABLE
TPC144 literal_fiber_relabeling = NOT_TESTABLE
TPC155 production_witness_present = false
TPC175 qualifying_claim_count = 0
TPC175 eligible_carrier_count = 0

COMMON_ACTUAL_LEAF_DOMAIN_AND_LITERAL_Q_D_Q_Z_MAPS_ABSENT
```

TPC-124 所需的 coefficientwise `(J Q_D-Q_Z)M=0` 因而没有共同 actual leaf
domain、两组 literal maps 或 production witness。即使反事实补齐这一层，content
map、outer labels、factor allocation、prefix order、`N0` normalization、共同
ranges/constants 和完整 loss ledger 仍需逐项证明。

本轮最终 gate matrix 为：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
H0_2_SPECIALIZATION = PASS_THEOREM_LEVEL_NOT_JSON_SERIALIZED

TRIGGER_1_ACTUAL_COEFFICIENTWISE_INTERTWINER = FAIL_CLOSED_ABSENT
TRIGGER_2_DIRECT_ACTUAL_A_C_OR_MATCHED_SHELL_THEOREM = FAIL_CLOSED_ABSENT
TRIGGER_3_GROWING_PREFIX_BV_CONTENT_LEDGER = FAIL_CLOSED_ABSENT

ACTUAL_GENERIC_PAIR_MASK_DECOMPOSITION = ABSENT
N0_TO_Q_X_SQUARED_NORMALIZATION_CROSSWALK = ABSENT
CHI_LE_1_OVER_400 = UNPAID
FIXED_ATOM_CREDIT = 0
ARITHMETIC_ADVANCE = NO
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

精确裁决为：

```text
TPC32_23_5_NAMED_PRIMARY_REOPEN_CANDIDATES_20260801_TO_ACTUAL_ZERO_OR_
GROWING_PREFIX_INPUT_ABSENT_STOP_SCOPED_NOT_REOPENED
```

本轮新增且仅新增第 6 节的：

```text
DECLARED_TPC32_23_5_NAMED_PRIMARY_REOPEN_CANDIDATES_20260801_V1
  = STOP_SCOPED
```

这个 dated cell 只冻结第 6 节列出的九个 exact source versions 单独使用，或仅在
这九个 versions 之间形成的本节已审核 splices。涉及 Higher Uniformity、Pilatte
及其他旧方法的结论仍分别由第 6 节原有 cells 管辖。它不是 theorem
nonexistence claim，不阻止：

1. 保留全部 physical metadata、共同 leaf domain、order 与 mass 的 actual
   coefficientwise `Q_D/Q_Z` intertwiner；
2. 直接控制同一 `A_C` 或 small-content matched shell、并支付 strict `1/400` 的
   source-backed theorem；
3. 对同一 complete literal coefficient（包括 `Qcal_{a,s}`、
   `Wcal_{xi,X}` 与 additive phase）、同一 prescribed outer fibers 和
   generally growing progression modulus `q_prog=as` 同时给出 every canonical
   prefix、outer BV、content remainder、uniform constants/ranges、`N0`
   normalization 与完整 loss ledger 的 theorem；
4. Grimmelt--Merikoski 型 determinant route 的 exact actual automorphic encoding，
   前提是另有 source-backed `Gamma` invariance、orbit `K` bound、range/
   normalization crosswalk 与完整 loss payment。

两个 O161 pointwise parents、pair-native reroute、H1 与 global architecture 继续
`OPEN`。第 6 节全部旧 method cells 保持原样 `STOP_SCOPED`，尤其 TPC193 V1、
common-`k` V1、tail-failure/A/B V1 与 full-`r_Rr_R` ultra-complement V1。
all-`D` uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual packet attachment 与完整 provenance gates
均未进入。没有创建 TPC-207、论文、paper directory、PDF 或构建日志。

### 28.5 晚到 RH-332 source-type check 与发布边界

最终 QA 期间，`origin/main` 从
`5e97b52b54d33f2ec34c68efdb9737f8959a3345` 前进到
`d49ed98bdf294355eeded2a07eeb4f2a5f7a2dc0`。新提交只增加
`papers/RH-332-sharp-physical-repelling-return-affine-leg-remainder/` 下 17 个
files；它没有修改 `TPC_HANDOFF.md`、任何 TPC packet/provenance artifact、
`AGENTS.md` 或本轮 127 个 protected untracked paths，所以同步没有文件级重叠。
但因题名包含 physical/affine/remainder，本轮仍由两份独立只读审计使用
`git show origin/main:path` 做 theorem-output 与 exact source-lock type check。

RH-332 的 actual theorem object 是连续概率核
`mu_{sigma,a}(du)[L_sigma(u,w)-A_u(w)]dw` 的 repelling-return second-hybrid
Duhamel row remainder。它证明 sectorwise remainder 有严格正的 order-`sigma`
主项，并否定 exponential 或 `o(sigma)` hybrid accuracy。这里的 `mu_{sigma,a}`
是 probability marginal，不是 Möbius；“actual physical first-leg prefix”是
path-law prefix，不是 TPC-111/122 canonical signed prefix；`U<0/U>0` 是 repelling
orientations，不是 arithmetic siblings、三 raw channels 或 fixed `h0=2`。

逐字段 type check 为：

```text
literal TPC coefficient/native domain = ABSENT_WRONG_CONTINUOUS_OBJECT
fixed arithmetic h0=2 = ABSENT
three raw channels and joint masks = ABSENT
G<=C, Delta#, A_C and outer labels = ABSENT
ordered arithmetic all-prefix/BV/content ledger = ABSENT
N0=JQ^2 asymp XQ normalization = NO_CROSSWALK
chi<=1/400 cancellation credit = NONE
```

同名符号也不得拼接：RH-332 的 `sigma->0` 是 noise scale，不是 TPC packet 的
固定 `sigma=1/10000`；RH-332 的 dynamical multiplier
`lambda=2u_c r=1.6785...` 不是 TPC 的 `lambda=99979/210000`。RH-332 自身的
README/ledger/result firewall 又明确给出 parity/shell cancellation、full-trace
replacement、determinant gluing 与 all-cycle transport 未证，Gates A--E 全 false。
candidate-specific first fatal 是：

```text
RH332_CONTINUOUS_GAUSSIAN_HYBRID_ROW_COEFFICIENT_AND_NATIVE_DOMAIN_
NOT_EQUAL_TO_TPC28_32_DISCRETE_MOBIUS_DETERMINANT_PACKET
```

所以精确 late-source verdict 为：

```text
RH332_SHARP_PHYSICAL_REPELLING_RETURN_AFFINE_LEG_REMAINDER_IS_WRONG_
PHYSICAL_OBJECT_FOR_TPC28_32_SELECTED_PACKET_NO_23_5_TRIGGER
```

原仓库 first fatal 仍是
`COMMON_ACTUAL_LEAF_DOMAIN_AND_LITERAL_Q_D_Q_Z_MAPS_ABSENT`。三个第 23.5 节
triggers 继续 `FAIL_CLOSED_ABSENT`；`ARITHMETIC_ADVANCE=NO`、strict `1/400`
仍 `UNPAID`、`L2=NONE`、`TPC207_TRIGGER=false`、`TPC207_CREATED=false`。
该 type check 不新增或扩张任何 `STOP_SCOPED` cell；RH-332 是不同 theory object，
不是一个被停止的 TPC arithmetic method。

最终正式写入前，22 项只读启动回归再次为 `22/22 PASS`，TPC-111/124/126/127
追加 gate checks 为 `4/4 PASS`；TPC-122 与 TPC-27--32 writers 均未执行。
三份 theorem audit 和三份修订后复核均为 read-only/PASS。唯一预期 tracked diff
仍为 `TPC_HANDOFF.md`；protected untracked count 仍为 127，manifest SHA256 仍为
`35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f`。

## 29. 2026-08-01 GM inverse-atom exact attachment 与 actual cross-row energy 审计

### 29.1 冻结基线、同步与 fail-closed 协议

三份第一轮只读审计锚定：

```text
FROZEN_HEAD
  = e298266ab79cbe9a5ffcd21ed0002ba7c5c28585
FROZEN_HANDOFF_SHA256
  = c857a18f999622b2ff821e71024ad25d03a11dacb58363e5ab51b3f42add7019
```

它们分别核查 direct weighted-pair/current-primary source、TPC-32/TPC-93
common-occurrence compiler，以及 Grimmelt--Merikoski kernel geometry；
后续 exact-kernel、self-energy、compiler devil's-advocate 与 source-theorem
复核均保持 `files_changed=[]`。正式写入前同步到：

```text
HEAD = origin/main
  = 11581a2f6a583abb5780e266d56b0aed41d7884b
TPC_HANDOFF_COMMITTED_BLOB_BEFORE_EDIT
  = a1d26efe486edcabed13ce6294abfd042dc7d9ea
TPC_HANDOFF_SHA256_BEFORE_EDIT
  = c857a18f999622b2ff821e71024ad25d03a11dacb58363e5ab51b3f42add7019
STARTUP_REGRESSION_AFTER_SYNC = 22/22 PASS
TPC111_124_126_127_READ_ONLY_GATE_CHECKS = 4/4 PASS
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
```

`e298266..11581a2` 只新增 RH-334/335 各 17 个 committed files；没有修改
TPC source、handoff 或根政策。TPC-122 与 TPC-27--32 legacy writers 均未执行。
protected manifest 仍按第 28.1 节的 path/byte-length/file-SHA256 rows 定义；
本轮没有向仓库写入 discovery log、外部 PDF/source、paper directory 或 build
output；GM official PDF/source 只在 repository 外的临时目录用于只读核对。

### 29.2 actual mask 修正与 common-occurrence compiler 裁决

第 28.4 节的 `ACTUAL_GENERIC_PAIR_MASK_DECOMPOSITION=ABSENT` 只描述
TPC-32 abstract interface，不是 actual source lineage 的最终事实。TPC-18/21/22
对本 selected residual packet 实际保留：

```text
m_kappa(alpha,gamma)
  = 1_{ell_alpha != ell_gamma}
    1_{|m_alpha-m_gamma| > Q X^{-kappa_row}}
    1_{gcd(d_alpha,d_gamma) <= X^{kappa_row}}.
```

stopping theorem 允许任意 fixed `kappa_row>0`。当前条件 GM exponent ledger
必须预先取 `0<kappa_row<1/400`。这个参数只管 same-prime/near-row/large-row-gcd
removal；它不是 TPC-32 的 content exponent
`kappa_C=133/400`，也不能冒充 small-content matched-shell saving。
第 23.1、28.4 节关于 generic bounded mask 的历史句子不得再作为 actual packet
的 stronger source lock。

TPC-32 的 pointwise identity与 TPC-93 的 source-child reconstruction 确实给出
一个参数化 `L1` common-occurrence compiler：

1. 三 raw channels 精确重写为两个 polarizations；both-ultra raw leaf 产生
   `L/R` 两个 computational children，系数各 `1/2`，physical multiplicity
   总和为一；
2. 展开 opposite leg并把具体 decoration 加入 source metadata 后，每个 child
   有唯一 source inverse；
3. literal coefficients、fixed `h0=2`、`j`、actual mask/weight、content
   `G`、canonical `Delta#`、polarization、projector、interval component与
   outer provenance均可保留；
4. 在这个 constructed formal ledger 上，`Q_D` 可逐 leaf 聚回 canonical
   determinant parent，formal ordered `Q_Z` 也可按原 `(theta,t)` 顺序
   totalize。

但 TPC-144 要求的 `J` 是 output-record sets 间的 metadata-preserving
bijection，不是任意 linear split。对一个 formal both-ultra raw column，
`Q_D M` 先把两个 halves 聚成一个 determinant record，而 `Q_Z M` 必须保留
两个不同 `L/R` zero records。一个 supported output record不能由 permutation
变成两个 halves；相应 child difference 可落入 `ker Q_D` 而不落入
`ker Q_Z`。所以：

```text
PARAMETRIC_LOSSLESS_COMMON_OCCURRENCE_COMPILER = L1 GO
PARAMETRIC_QD_TOTALITY = L1 GO
FORMAL_ORDERED_QZ_TOTALITY = L1 GO
TPC144_METADATA_PRESERVING_J = STOP_SCOPED
ACTUAL_SELECTED_NONZERO_BOTH_ULTRA_OCCURRENCE = NOT_TESTABLE
PRODUCTION_INTERTWINER = NOT_TESTABLE
```

这没有给 growing signed-prefix theorem、small-content saving 或 `L2`。

### 29.3 GM2505v2 inverse-atom exact kernel：真实 L1 正接口

正式 source lock 是 Grimmelt--Merikoski,
`arXiv:2505.00489v2`, Theorem 1.1，而不是第 28 节审核的旧
`2404.08502v2` determinant-counting theorem。对一个 physical atom
`t=(alpha,gamma,j)`，令 `m=m_alpha`、`n=m_gamma`、

```text
G = gcd(mj+2,nj+2),
U = (mj+2)/G,
V = (nj+2)/G,
B_t = [[m,U],[n,V]],
det(B_t) = 2(m-n)/G.
```

按 determinant sign 分 cell并定向后，置
`H_t=2|m-n|/G`、`g_t=H_t^{-1/2}B_t^+ in SL_2(R)`。
若 `M=|m-n|`，相应 dyadic coordinate ranges 是

```text
A_GM asymp C_GM asymp Q sqrt(G/M),
D_GM asymp X/sqrt(GM),
A_GM D_GM asymp XQ/M = N0/M,
R1=A_GM/C_GM asymp 1,
R2=D_GM/C_GM asymp J/G.
```

令 `a_t` 是保留两条 opened-row signs、actual mask、fixed `h0=2`、
`j,G,Delta#`、三 raw channels的 matched tensor、smooth/periodic factors与
outer labels的 literal coefficient。GM pairing 的精确 convention 是

```text
K_F(tau1,tau2)
  = sum_{gamma in Gamma} conjugate(chi(gamma))
    F(tau1^{-1} gamma tau2),

alpha1 = sum_t conjugate(a_t) delta_{g_t^{-1}},
alpha2 = delta_I.
```

因此 identity translate恰给 `a_t F(g_t)`，无需把 `F` 换成 `F^vee`。
在每个 fixed-margin sign/coordinate cell取
`f(a,c,d)=phi(a,c,d)-phi(-a,c,d)`；Haar matrix-coordinate density
不依赖 `a`，故 `int F=0`，同时 physical sign cell上 `F(g_t)=1`。
一个 bump不能在整个闭 dyadic box恒等于一；必须先做 `O(1)` fixed-margin
partition，这只产生 soft 常数。

为避免 GM proof 中 `-I in Gamma` convention 的歧义，可使用

```text
Gamma_pm(q)
  = {gamma in SL_2(Z): gamma == plus-or-minus I (mod q)}
```

配 principal character `chi=1`，并取 `q` 大于固定常数乘
`max(D_GM^2,A_GM D_GM,A_GM C_GM)`；sign support排除 unwanted `-I`。
等价地，正式使用 literal principal `Gamma(q)` 前必须补写 theorem 对该 subgroup
的 convention extension。actual far-row bound使所需 `q` 至多 polynomial：
`q <= X^{533/400+kappa_row+o(1)}/G`。该 level选择删除所有
`gamma != plus-or-minus I` target/self-kernel translates；它不删除
`gamma=I` 的 physical cross-atom terms。

于是存在 source-backed exact identity：

```text
<alpha1 | Delta F | delta_I>
  = sum_{t in one physical cell} a_t.
```

同一 fixed `(m,n,G)` 的不同 `j,j'` 在第一槽满足
`g_j g_{j'}^{-1}=g_j n(-(j'-j)/G)g_j^{-1}`；其 normalized off-diagonal
entries规模至少 `Q^2|j-j'|/M`，故逃出 `R1 asymp 1` 的 unit support。
所以第 28 节“原始第二槽有完整 `J/G` unipotent arc”的 obstruction 对这项
inverse placement 已被真实修复；不得继续把它列为 first fatal。

若完整第一槽 self-energy满足

```text
E1 <= P_X sum_t |a_t|^2,
```

并授予其余 exact cell return，则 GM with
`X0=1,X1=1,X2=A_GM D_GM` 条件性给

```text
|cell target|
  << N0 sqrt(P_X/M) X^{o(1)}.
```

在 `M>QX^{-kappa_row}` 与 `beta=267/400` 下，为严格越过
`1-beta=133/400`，必须有某个 fixed `epsilon>0` 使

```text
P_X <= X^{1/400-kappa_row-epsilon+o(1)}.
```

当 `P_X=X^{o(1)}` 时条件 margin 是
`1/800-kappa_row/2`。这是条件路线，不是 arithmetic credit。

### 29.4 精确 cross-row compact collisions

inverse placement 只移除了 fixed-row `j`-arc，没有自动对角化完整
`alpha1` self-kernel。存在两个 source-checked exact geometry families。

第一族固定 `D0=m-n=G Delta#`、`G` 与 `j`。对整数 `k` 令

```text
m_k=m+kG,   n_k=n+kG,
U_k=U+kj,   V_k=V+kj,
tau=k/Delta#,
P_tau=[[1+tau,-tau],[tau,1-tau]].
```

当 shifted rows仍在 actual row set且
`gcd(U+kj,Delta# j)=1` 时 exact content仍为 `G`，并有

```text
B_k=P_tau B_0,
g_k g_0^{-1}=P_tau,
u_1(P_tau)=tau^2.
```

所以 `|k|<=|Delta#|/2` 的整个 algebraically admissible family位于
fixed unit ball内。actual mask给
`|Delta#|>QX^{-kappa_row}/G`，并不限制不同 determinant edges间的
共同 row translation。

第二族固定奇数 `n,j`，取偶数 `M` 且 `gcd(M,nj+2)=1`，令
`m=n+M`。此时 `G=1`、`H=2M`，且

```text
g_M g_{M'}^{-1}
 = [[sqrt(M/M'), (M'-M)/sqrt(MM')],
    [0,          sqrt(M'/M)]].
```

当 `M' asymp M` 时相对矩阵位于 fixed compact set；足够接近时落入 theorem
允许的 `u_1<1` 外包球，不能由其 support upper bound排除。这些都是
`gamma=I` terms，auxiliary level不能删除；这里没有断言 kernel必非零。

两族均没有证明 actual prime--squarefree opened rows与 literal matched
coefficients在 polynomially many points上同时 nonzero/coherent；所以本轮不声称
actual large-energy counterexample。它们精确证明的只是：atom injectivity、
near-row removal、TPC-31 row degree one、content cutoff和 GM support geometry
本身不推出所需 tiny-power packing。

### 29.5 actual equal-difference four-point theorem screen

对 fixed `D0,G,j`，定义 actual determinant-edge set

```text
E_{D0,G,j}
 = {m:
      m and m-D0 are actual opened rows,
      actual mask survives,
      gcd(mj+2,(m-D0)j+2)=G}.

w_m
 = gamma_m^(1) gamma_{m-D0}^(2)
   A_{m,m-D0}(j) K_sh_{m,m-D0}(j).
```

GM 所需的必要 subtheorem是对相应 fixed smooth kernels统一控制

```text
E_Psi
 = sum_{m,m' in E_{D0,G,j}}
   conjugate(w_m) w_m' Psi((m-m')/D0)

|E_Psi|
 <= X^{1/400-kappa_row-epsilon+o(1)}
    sum_m |w_m|^2,
```

或给出不更弱、并保留所有 literal metadata的完整 automorphic self-kernel
inequality。

这个 displayed fixed-`D0` bound只控制第一族共同 row-translation，是必要的
reopen subgate，不是完整 `E1` 的充分估计。第 29.4 节第二族让
`D0=M` 与 `D0'=M'` 一起变化，故通过本 subgate 后仍须独立控制 cross-`D0`
及其余完整 self-kernel；它不能单独触发 TPC-207。

仓库内精确 lineage audit得到：

1. TPC-34/38 定位 same-time/identity-bucket four-Mobius autocorrelation，
   但明确未证明相应 operator estimate；
2. TPC-42/48 的 Hilbert large-sieve/tiling bookkeeping不消除 coherent
   actual fiber；
3. TPC-84 把 determinant fiber打开为 literal weighted four-Mobius
   expansion，unpaired remainder仍需 cancellation；
4. TPC-95 是 shared-target/collision census与 conditional diagnostics；
5. TPC-108 的 generic affine `TT^*`/H3 是最近 analytic boundary，但 H3
   本身为未证 `L2`，且 GM collision到同一 actual signed-prefix sum的
   lossless crosswalk与 physical normalization也未提交。

有限 official-primary screen 另逐项排除了：Menon 的 naked `k`-point
shift-average、Kim 的 ternary shift-average、Tao--Teräväinen
`2512.01739v2` 的裸二点/polylog-affine/exceptional-scale terminal sum、
Higher Uniformity II 的 single-factor almost-all-origin nilsequence theorem，
以及 ordinary additive/Dirichlet large sieve、Schur/Young bounds。它们分别缺
literal `w_m`、prescribed parallelogram、matched shell/mask、fixed
`D0,G,j`、natural normalization、power threshold或 uniform loss ledger。
Grimmelt--Merikoski `2505.00489v2` 接收本轮 exact functional，但把同一个
`E_Psi` 留在 RHS self-kernel中，并不估计它。

没有 committed lossless decomposition
`w_m=sum_nu c_nu a_nu(m)`、`sum|c_nu|=X^{o(1)}`，把该对象送入任一
source theorem domain；actual generic mask也不得从 boundedness推出这种
projective decomposition。有限裁决因此是：

```text
FIRST_FATAL
  = LITERAL_EQUAL_DIFFERENCE_EDGE_WEIGHT_NOT_IN_ANY_SOURCE_THEOREM_DOMAIN

SOURCE_THEOREM_SURVIVOR = NONE_IN_FINITE_SCREEN
GLOBAL_OR_FUTURE_THEOREM_NONEXISTENCE_CLAIM = false
```

下一 exact source trigger 命名为：

```text
TPC32_H0_2_LITERAL_EQUAL_DIFFERENCE_EDGE_WEIGHT_ONE_PARAMETER_
FOUR_POINT_AUTOCORRELATION_THEOREM_GATE
```

它必须直接接受同一 `w_m`，或给出 `X^{o(1)}` projective mass的 lossless
source-backed decomposition，并逐项支付 fixed physical `h0`、summation/
lag order、`X/N/Q/D0/G/j` ranges、uniform constants、normalization、
actual mask、three-channel matched shell、outer labels与完整 physical-loss
ledger。shift/origin average、logarithmic theorem、裸 coefficient、
complete-frequency mean或 source splice均不合格。

### 29.6 RH-333/334/335 late-source type firewalls

RH-333 的 raw affine escape对象是连续 Gaussian probability event；没有
TPC determinant gluing、matched shell或 arithmetic normalization。它不触发
本 gate。

RH-334 的 exact object是 `f:[-1,1]` 到 `T=|f|:[0,1]` 的 fixed-point
folding、Gaussian backward-observable localized trace与
`hardy_full_trace_constituent`

```text
q_FT = B+S+R+P-A.
```

这里的 `B/S/R` 是 frozen observation windows的 localized defects，不是
TPC 三 raw channels；fixture `k=2,n=4` 不是 physical `h0=2`。
RH-334 自身锁定 determinant gluing、projectors/Floquet localization与 moving
asymptotics未证。它没有 `m,m',D0,G,j`、`w_m`、`E_Psi` 或 `N0` crosswalk。

RH-335 的 exact object是 rank-one noisy Riesz projector signed measure
`pi_sigma(J)=Tr(M_J E^-_sigma)` 与 fixed-order frozen-cell ledger
`C_{sigma,n}(J)`。它的 `J` 是 measurable cell，`n=2` 是 operator power，
均不是 TPC orbit `j` 或 shift `h0`；其 `3x3` fixture明确非 physical，
determinant closure、moving-order与 physical upper-exponent inputs均 open。

所以：

```text
RH333_334_335_TO_TPC32_EQUAL_DIFFERENCE_ENERGY_CROSSWALK
  = ABSENT_WRONG_OBJECT
STOP_CELL_CHANGE_FROM_RH333_334_335 = NONE
TPC207_TRIGGER_FROM_RH333_334_335 = false
```

这些 type checks只建立对象防火墙；不把 RH methods列为被停止的 TPC arithmetic
methods，也不得按同名 `sigma/lambda/physical/alias/projector` 符号拼接。

### 29.7 最终裁决、reopen interface 与发布边界

本轮精确裁决为：

```text
TPC32_H0_2_GM2505_INVERSE_ATOM_EXACT_KERNEL_TO_LITERAL_EQUAL_DIFFERENCE_
FOUR_POINT_ENERGY_INPUT_ABSENT_STOP_SCOPED_NOT_REOPENED
```

状态矩阵是：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
ACTUAL_STRUCTURED_RESIDUAL_MASK_SOURCE_LOCK = PASS
PARAMETRIC_COMMON_OCCURRENCE_COMPILER = L1 GO
TPC144_METADATA_PRESERVING_J = STOP_SCOPED

GM2505V2_INVERSE_PAIRING = L1 GO
ATOMWISE_DETERMINANT_NORMALIZATION = L1 GO
ZERO_HAAR_FIXED_MARGIN_TEST = L1 GO
AUXILIARY_LEVEL_TRANSLATE_ISOLATION = L1 GO_WITH_SUBGROUP_CONVENTION
FIXED_ROW_J_ARC_ESCAPE = L1 GO

ACTUAL_CROSS_ROW_COMPACT_SELF_KERNEL_BOUND = ABSENT
LITERAL_EQUAL_DIFFERENCE_FOUR_POINT_SOURCE_THEOREM = NONE_IN_FINITE_SCREEN
P_X_LE_X_TO_1_OVER_400_MINUS_KAPPA_MINUS_EPSILON = UNPAID

ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节新增的两个 cells 只冻结本轮 exact compiler upgrade和
GM2505v2 Part-I-to-current-energy inference；`L1 GO` interfaces、未来
source theorem与独立 architectures均保持可重开。第 6 节所有旧 cells继续
原 scope `STOP_SCOPED`，尤其 TPC193 V1、common-`k` V1、tail-failure/A/B V1
与 full-`r_Rr_R` ultra-complement V1。不得把本轮 GM geometry重新包装为
TPC-34/84/95/108 arithmetic theorem。

两个 O161 pointwise parents、pair-native reroute、H1 与 global architecture
继续 `OPEN`。all-`D` uniformity、exactly-once physical cover、original/global
normalization、tail-failure、A/B selection、actual packet attachment与完整
provenance gates均未进入。

没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入只修改
`TPC_HANDOFF.md`；既有 `.codex/config.toml`、四个
`.codex/agents/tpc-*.toml`、TPC-105 `__pycache__`、TPC-63 build artifacts与
`tmp/` 仍为 protected untracked。发布前 22 项只读启动回归为
`22/22 PASS`，TPC-111/124/126/127为 `4/4 PASS`；TPC-122 与 legacy writers
未执行。上述 one-parameter four-point source theorem即使通过，也只重开
下一轮 exact audit；还须控制 cross-`D0`/其余完整 self-kernel，并分别通过
all-`D` uniformity、physical cover/normalization、tail-failure、A/B、actual
attachment与完整 provenance gates。只有所有门槛共同产生真实 theorem-backed
状态变化，或其他独立 architecture 支付同等完整账本后，才允许进入 TPC-207
provenance cascade。

## 30. 2026-08-01 literal fixed-`D0` four-point transfer 与 full-self-kernel 审计

### 30.1 冻结基线、对象与必要子门

本轮启动先执行根 `AGENTS.md` 与第 1 节协议。初始只读快照为：

```text
HEAD = origin/main
     = 33e3073fef6bfb021e3479d2acf8cf6ad75daee6

TPC_HANDOFF_SHA256
     = 51562f27288cc114dbe8da7a9baab36659a4e929010c9f2849d40638097fcfca

PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
     = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f

TRACKED_WORKTREE_DIFF = empty
CACHED_DIFF = empty
STARTUP_REGRESSION = 22/22 PASS
```

相对上一份 handoff commit `d3702b2e92cf85c48c5024758c5293357b2b347f`，
本轮 `git pull --rebase origin main` 只 fast-forward 到 RH-336 commit
`33e3073fef6bfb021e3479d2acf8cf6ad75daee6`。它没有修改本轮 TPC source locks。

同一 theorem-valid selected packet继续严格固定为：

```text
sigma=1/10000
lambda=99979/210000
delta=7/60
beta=267/400
Q=X^(267/400+o(1))
J=X^(133/400+o(1))
C=floor(J)
h0=2
N0=JQ^2 asymp XQ
0<kappa_row<1/400
```

对 fixed physical `D0 != 0`、`G <= C`、`j asymp J` 与全部 actual outer
labels，literal edge coefficient仍是

```text
w_m
 = gamma_m^(1) gamma_(m-D0)^(2)
   A_(m,m-D0)(j) K_sh_(m,m-D0)(j),
```

其中 actual mask逐字保留

```text
1_{ell_m != ell_(m-D0)}
1_{|D0| > Q X^(-kappa_row)}
1_{gcd(d_m,d_(m-D0)) <= X^(kappa_row)},
```

并保留 three raw channels、两条 `1/2` polarizations、matched cutoff、content
`G`、canonical `Delta#=D0/G`、residue/smooth factors、row orientations与 parent
provenance。GM inverse route当前必要但不充分的 fixed-`D0` 子门仍为

```text
E_Psi
 = sum_(m,m') conjugate(w_m) w_m' Psi((m-m')/D0),

|E_Psi|
 <= X^(1/400-kappa_row-epsilon+o(1)) sum_m |w_m|^2.
```

### 30.2 exact autocorrelation 与 TPC-93 singleton-transversal 裁决

令 `k=m-m'`。无损重排给出

```text
E_Psi = sum_k Psi(k/D0) C_(D0,G,j)(k),

C_(D0,G,j)(k)
 = sum_{m,m-k in E_(D0,G,j)} conjugate(w_m) w_(m-k).
```

打开两个 matched shells 后有四个 cutoff cells `(Y,Y') in {U0,T}^2`，总
cutoff variation为 `4`。用 TPC-32 的 primitive sign fusion逐腿合并，exact
arithmetic sign为

```text
mu(d_m u)
mu(d_(m-D0) v)
mu(d_(m-k) u')
mu(d_(m-k-D0) v').
```

四个 `w_R` divisor weights、prime logarithms、两条 edge masks、两个 exact
content条件、target divisibility、conjugation order、physical phases与全部 outer
metadata仍在。因此它的最早诚实算术描述是 prescribed-lag equal-difference
opened-row parallelogram上的 literal weighted four-Mobius autocorrelation；不是
naked Chowla sum。

TPC-93 的 decorated source-child map可把 fixed `D0,G,j` indicator、Fourier
phase与全部 provenance无损带入 affine ledger，故 representation level仍是
`L1 GO`。但每个 TPC-93 affine key `theta` 固定 opposite row `n_theta`，moving row为

```text
M_theta(t)
 = ell_theta v_theta (d_theta + sigma_theta t).
```

fixed ordered difference要求

```text
M_theta(t)-n_theta = D0
```

或在相反 orientation取 `-D0`。由于 slope
`ell_theta v_theta sigma_theta != 0`，每个 affine column至多有一个整数 `t`：

```text
FIXED_D0_SLICE_PER_TPC93_AFFINE_COLUMN = CARDINALITY_AT_MOST_ONE
FIXED_D0_GROWING_DIRECTION = OUTER_THETA_KEYS
```

所以 fixed-`D0` energy是 singleton affine children 的 outer transversal；它不是
TPC-108 one-resolved-block 内的 growing prefix。TPC-108 exact `TT*` 只给四符号
identity；H3、outer mass、physical `TT*` return与 endpoint normalization均仍是
未证 premise。

当前精确 projective ledger是：

```text
Psi Fourier kernel mass                    = O_Psi(1)
matched-shell cutoff variation after square = 4
row-gcd projector mass per affine column    = X^o(1)
smooth/fixed-period local separation        = X^o(1)
source-child inverse                        = exact

GLOBAL_FIXED_D0_OUTER_TRANSVERSAL_PROJECTIVE_MASS = UNKNOWN
```

因此不得把 columnwise `X^o(1)` 绝对求和成 global projective decomposition。

### 30.3 current-primary theorem screen

按 ARS bibliography/source-verification protocol只用 official primary theorem
bodies进行可复现有限检索，并对 literal coefficient、fixed physical `h0`、
summation/prefix order、`X/N/q` ranges、uniform constants、normalization与完整
physical-loss ledger逐项审核。最接近来源均在 exponent accounting前失败：

1. Tao--Teräväinen `arXiv:2512.01739v2`, Theorem 3.1给 natural-average
   two-point multiplicative correlation，并只另允许一个 small-modulus residue-class
   indicator，但排除小 logarithmic-density scale set；它不是四点
   `conjugate(w_m)w_m'`，也不接受 arbitrary actual mask/shell；
2. Menon `arXiv:2607.15574v1`, Theorem 1.5给 naked Liouville `k`-point bound，
   但平均全部 `h_2,...,h_k`，不能限制到 prescribed equal-difference slice；
3. Jaskari--Sachpazis `arXiv:2409.10663v3`, Theorem 1.1最接近 fixed
   `k`-point quantifier，但依赖 Landau--Siegel zero，且仍是 naked Liouville、
   fixed-shift constants与错误 `q/x` range；
4. Tao--Teräväinen `2107.02158v4`、Leng `2212.09635v3` 与
   Klurman--Mangerel `1708.03176v1` 控制 single-factor Gowers norms或
   nondegenerate affine systems；forms
   `(m,m-D0,m-k,m-k-D0)` 含两对 repeated linear directions，global Gowers
   average不控制 prescribed `D0` slice，且 actual `w_m` 不在 theorem domain；
5. Lichtman--Teräväinen `2111.08912v3` 只平均一个 independent shift；本对象
   同时移动 linked pair `(k,k+D0)`，不能由 all-but-exceptional-shifts结论升级；
6. Higher Uniformity II `2411.05770v2` 的 main theorem是 single arithmetic
   factor against nilsequences、almost-all origins；其 derived Gowers estimates仍
   average全部 increments且仍为 almost-all-origin。Kim `2603.23250v2` 是
   ternary/shift-average；两者均不接受 literal edge sequence或 prescribed
   physical phase；
7. ordinary Schur/Young、additive/Dirichlet large sieve与 Fourier/Mellin identity
   只给 coefficient-blind density、frequency average或 exact square representation，
   不给 distinguished physical kernel cancellation。

有限检索没有找到 source-backed decomposition

```text
w_m = sum_nu c_nu a_nu(m),
sum_nu |c_nu| = X^o(1),
```

使每个 `a_nu` 真正进入同一个适用 theorem domain，并精确重建 determinant、
content、mask、shell、outer labels与 global normalization。故第一 fatal保持：

```text
FIRST_FATAL
 = LITERAL_EQUAL_DIFFERENCE_EDGE_WEIGHT_NOT_IN_ANY_SCREENED_SOURCE_
   THEOREM_DOMAIN

SOURCE_THEOREM_SURVIVOR = NONE_IN_REPRODUCIBLE_FINITE_SCREEN
GLOBAL_OR_FUTURE_THEOREM_NONEXISTENCE_CLAIM = false
```

### 30.4 GM application 与 coefficient-blind loss ledger

Grimmelt--Merikoski `arXiv:2505.00493v2` 是 Part I 的正式 application，但其
Type I/II theorems估计的是 roots of `a ell^2+h mod k` 的 distribution。其
self-kernel inputs是 exact Heegner-point functional与 exact lower-triangular
functional；application用 level `d/q` averaging、sparse diagonal和 off-diagonal
divisor absorption。论文还明确在新 short kernel ranges无法证明 cancellation，
而由 positivity丢弃 subtracted integral。

这不是接受 arbitrary actual `w_m` 的 self-kernel theorem，也不把 TPC compact
cross-row collisions变成 application的 sparse diagonal。不得把 Type I/II 中
bounded `alpha_m,beta_n` 的外层 sieve coefficients改名为本轮 automorphic
functional coefficients。

独立的 coefficient-blind检查也无法靠近 endpoint。fixed `(D0,G,j)` block内，
`G | mj+2` 且 primitive support使 `j` 在 `G` 上可逆，所以所有 `m` 落在一个
mod-`G` residue class。Schur/Young至多给

```text
|E_Psi| << (1+|D0|/G) sum_m |w_m|^2
        = (1+|Delta#|) sum_m |w_m|^2.
```

而 actual row-gap 与 `G<=J` 给

```text
|Delta#|
 > Q X^(-kappa_row)/J
 = X^(134/400-kappa_row+o(1)).
```

目标 factor是 `X^(1/400-kappa_row-epsilon+o(1))`，故即使最大 content也差
`X^(133/400+epsilon)`；`G=1` 时差 `X^(266/400+epsilon)`。在这一
coefficient-blind route 后乘任何 published logarithmic/doubly-logarithmic
naked decay仍不能支付 polynomial ledger。这里不是声明所有未来 arithmetic
theorems不可能达到目标；只冻结本轮 direct standard transfer。

### 30.5 full self-kernel、RH-336 与独立第二 fatal

fixed-`D0` 子门即使未来通过，也不控制完整 GM first self-energy。对 exact
`G=1` family、fixed odd `n,j` 与 `m=n+M`，第 29.4 节的相对矩阵精确为

```text
g_M g_(M')^(-1)
 = [[sqrt(M/M'), (M'-M)/sqrt(MM')],
    [0,           sqrt(M'/M)]],

u_1(g_M g_(M')^(-1))
 = (M'-M)^2/(2MM').
```

若 `M'/M in [1/2,2]`，则 `u_1<=1/4`，所以 comparable cross-`D0` blocks可同时
落在 GM unit compact self-kernel support。它不证明 actual literal coefficients
在这些点 coherent/nonzero，因而不是 large-energy arithmetic counterexample；
它严格排除仅靠 dyadic `D0` geometry声称 block orthogonality。

因此第二独立 fatal是：

```text
SECOND_FATAL
 = FIXED_D0_BLOCK_CONTROL_DOES_NOT_CONTROL_CROSS_D0_GM_SELF_KERNEL

CROSS_D0_BLOCK_BESSEL_OR_ALMOST_ORTHOGONALITY_THEOREM = ABSENT
```

应用 fixed-`D0` theorem后按 differences triangle/Cauchy重组，最多引入
`Q^(1/2)=X^(267/800+o(1))` 未支付 linear loss；dyadic grouping不消除同一
dyadic block内的 dense compact interactions。

本轮 pull新增的 RH-336 只处理 projector mass `pi_sigma(J)`、moving operator
order、nonphysical `3x3` positive row-stochastic similarity family与 fixed fixture
`n=2`。其中 `n=2` 是 operator power，不是 TPC physical `h0=2`；该 artifact没有
`m,m',D0,G,j,w_m,E_Psi,N0`、matched shell或 TPC normalization crosswalk：

```text
RH336_TO_TPC32_FIXED_D0_OR_FULL_E1 = ABSENT_WRONG_OBJECT
TPC207_TRIGGER_FROM_RH336 = false
STOP_CELL_CHANGE_FROM_RH336 = NONE
```

最终发布前 rebase 到 `90a25186d5cfd5e541a739e599edfdd797ea48ba` 时，上游只在
RH-336 的 13 个文件中把 `kappa_proj>gamma_star_RH325` 从 decimal diagnostic
强化为 exact rational certificate。这里的两个指数属于 RH projector-gauge 与
Duhamel stability clock；它们不支付 TPC 的 `kappa_row<1/400`、literal
fixed-`D0` energy 或 full self-kernel。三份独立只读 type review 均确认本节
wrong-object 裁决与 TPC-207 trigger 不变。

随后上游 `a7e7c6be880542cdd07614eb11a6af7abf5fa846` 只新增 RH-337 的 17 个
files。该 paper 研究 RH-329 的 `Lambda_hat/lambda` algebraic clock drift、moving
order `k`、parity/alias scalars 与 comparator defect `D_k`；它明示 `D_k` 不是
actual five-slot coefficient 或 full-trace residual，correct-clock remainder仍为
`NOT_TESTABLE`。RH 的 fixed phase、shell、`D_k` 与 `H_k` 分别不是 TPC 的 fixed
physical `h0=2`、matched divisor shell、row difference `D0` 与 natural scale
`N0`，也没有 literal coefficient、normalization 或 loss-ledger crosswalk：

```text
RH337_TO_TPC32_FIXED_D0_OR_FULL_E1 = ABSENT_WRONG_OBJECT
TPC207_TRIGGER_FROM_RH337 = false
STOP_CELL_CHANGE_FROM_RH337 = NONE
```

### 30.6 最终裁决、STOP scope 与合法 reopen interface

本轮精确裁决为：

```text
TPC32_H0_2_LITERAL_EQUAL_DIFFERENCE_FIXED_D0_TPC93_AFFINE_CHILD_
TRANSVERSAL_SINGLETON_COHERENT_OUTER_FOUR_POINT_THEOREM_ABSENT_
STOP_SCOPED_NOT_REOPENED
```

状态矩阵是：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
ACTUAL_W_M_AND_E_PSI_SOURCE_LOCK = PASS
TPC93_DECORATED_REINDEXING = L1 GO
FIXED_D0_SLICE_PER_AFFINE_COLUMN = CARDINALITY_AT_MOST_ONE
FIXED_D0_GROWING_DIRECTION = OUTER_THETA_KEYS
GLOBAL_FIXED_D0_TRANSVERSAL_PROJECTIVE_MASS = UNKNOWN
TPC108_H3_AND_OUTER_NORMALIZATION = UNPROVED

CURRENT_PRIMARY_LITERAL_WEIGHT_THEOREM = NONE_IN_FINITE_SCREEN
GM2505_APPLICATION_TO_LITERAL_W_M = DOMAIN_MISMATCH
P_X_LE_X_TO_1_OVER_400_MINUS_KAPPA_MINUS_EPSILON = UNPAID
CROSS_D0_BLOCK_BESSEL = ABSENT
FULL_E1 = UNCONTROLLED

ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节新增

```text
DECLARED_TPC32_LITERAL_FIXED_D0_FOURPOINT_STANDARD_TRANSFER_
AND_CROSS_D0_ORTHOGONALITY_CORPUS_V1 = STOP_SCOPED
```

只冻结第 30.3--30.5 节列明的有限 primary/current TPC/standard-transfer corpus。
它不停止以下合法 trigger：

1. 一个 source theorem直接接受同一 literal `w_m`，统一控制 fixed
   `(D0,G,j,h0=2)` `E_Psi`，保留 actual mask/content/shell/outer labels，并支付
   strict endpoint与全部 ranges/constants/normalization；
2. 一个 source-backed exact regrouping，把 singleton TPC-93 children组成
   genuinely growing theorem blocks，global projective total variation为 `X^o(1)`，
   再由适用 theorem支付同一完整 ledger；
3. 一个直接控制全部 `(D0,G,j,outer labels)` 的 literal full automorphic
   self-kernel theorem；或在 1/2 之后另有 cross-`D0` block-Bessel theorem，使
   combined total exponent仍严格通过 `1/400`。

仅通过 fixed-`D0` 子门只允许重开 cross-`D0`/full-`E1` 审核，不改变
TPC-207 trigger。此后仍须分别通过 all-`D` uniformity、exactly-once physical
cover、original/global normalization、tail-failure、A/B selection、actual packet
attachment与完整 provenance cascade。

第 6 节全部旧 cells保持原 scope `STOP_SCOPED`，尤其 TPC193 V1、common-`k`
V1、tail-failure/A/B V1 与 full-`r_Rr_R` ultra-complement V1。两个 O161
pointwise parents、pair-native reroute、H1 与 global architecture继续 `OPEN`。

### 30.7 发布边界

没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入只允许
`TPC_HANDOFF.md`；既有 `.codex/config.toml`、四个
`.codex/agents/tpc-*.toml`、TPC-105 `__pycache__`、TPC-63 build artifacts与
`tmp/` 均继续作为 protected untracked，不得纳入本轮提交。

本轮只读启动回归与正式写入后的发布前复跑均为 `22/22 PASS`；
TPC-111/124/126/127 supplemental checks为 `4/4 PASS`。TPC-122 与 legacy
TPC-27--32 writers均未执行。发布前 protected untracked仍为 `127` 个，按
`path<TAB>byte_length<TAB>sha256<LF>` rows 计算的 manifest SHA256仍为
`35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f`。

```text
FINAL_SYNC_ORIGIN_MAIN
  = a7e7c6be880542cdd07614eb11a6af7abf5fa846
FINAL_SYNC_DELTA_FROM_INITIAL_33E3073
  = RH336_STRENGTHENING_13_FILES_PLUS_RH337_NEW_17_FILES
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
FINAL_SYNC_TPC_VERDICT_CHANGE = NONE
```

只提交 `TPC_HANDOFF.md`，再 rebase/push并验证 local `HEAD`、`origin/main` 与
remote `refs/heads/main` 三个 hash一致。

## 31. TPC32 fixed-`D0` outer-regroup / post-§30 direct-and-frame finite gate

### 31.1 source lock、协议与只读基线

本轮从仓库事实重新启动，不把旧聊天当作证明来源。启动时：

```text
INITIAL_HEAD = e1c06611cbf9cb23698c6be3d9244526021f8c1f
INITIAL_ORIGIN_MAIN = e1c06611cbf9cb23698c6be3d9244526021f8c1f
INITIAL_HANDOFF_SHA256
  = 8edee5dc3aebf6cf7ae65f039395f8b5a485a7b2767e8959659658637984ed46
INITIAL_TRACKED_DIFF = EMPTY
INITIAL_CACHED_DIFF = EMPTY
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
STARTUP_REGRESSION = 22/22 PASS
TPC93_LITERAL_EXPORT_READ_ONLY_REGRESSION = PASS
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

启动时的 `git pull --rebase origin main` 新增的唯一上游对象是 RH-338 的 17 个文件；
它没有改动 TPC papers、TPC checkers或本 handoff。仍 source-lock 第 28/32 节
同一个 theorem-valid selected packet：

```text
sigma = 1/10000
lambda = 99979/210000
delta = 7/60
beta = 267/400
Q = X^(267/400+o(1))
J = X^(133/400+o(1))
C = floor(J)
h0 = 2
N0 = J Q^2 asymp X Q
0 < kappa_row < 1/400
```

literal edge与必要 fixed-`D0` gate保持：

```text
w_m = gamma_m^(1) gamma_(m-D0)^(2)
      A_(m,m-D0)(j) K_sh_(m,m-D0)(j),

E_Psi = sum_(m,m') conjugate(w_m) w_(m')
        Psi((m-m')/D0),

|E_Psi| <= X^(1/400-kappa_row-epsilon+o(1)) sum_m |w_m|^2.
```

三条 raw channels、content cutoff、canonical `Delta#`、actual masks/weights、
matched shell、outer labels与 `N0` 均未被删除或平均化。

### 31.2 exact outer-regroup 二分法

TPC-93 child 的固定 theorem key为

```text
theta = (L,gamma,ell,j,sigma_aff,v,iota),   gamma=(ell',e),
M_theta(t) = ell v(d_theta+sigma_aff t),    n_theta=ell' e,
sigma_aff := sigma_theta in Z_(>0).
```

这里 `sigma_aff` 是 TPC-93 provenance key中的 affine slope，绝不是 selected
packet的 real parameter `sigma=1/10000`。

记 `A=ell v`。固定 physical row difference `D0` 等价于

```text
A sigma_aff t - ell' e = D0 - A d_theta.
```

若固定 theorem 参数 `(L/R,ell,ell',j,sigma_aff,v,iota)`，令
`g=gcd(A sigma_aff,ell')`，全部整数解只能沿

```text
t = t0 + (ell'/g) z,
e = e0 + (A sigma_aff/g) z
```

移动。actual packet 有 `ell != ell'`、`v|d,e`、`d,e asymp D`、
`ell,ell' asymp L`，故 `ell'` 是素数且 `g` 只能为 `1` 或 `ell'`。若
`g=1`，opposite-cofactor step是 `A sigma_aff >= L/2`；若 `g=ell'`，由
`ell'` 不整除 `ell v` 可知 `ell'|sigma_aff`，故 step
`A sigma_aff/ell' >= L/2`。同时

```text
R = X^(23/60+o(1)),
D <= X^(23/120+o(1)),
L = Q/D >= X^(571/1200+o(1)),
D/L <= X^(-341/1200+o(1)).
```

因此足够大 `X` 时，固定 theorem-key block 对 fixed `D0` 的 actual occupancy
至多为 `1`。若 `g=1`，新的 `z`-determinant 是 `ell' h0`，不再是 physical
`h0=2`；若 `g=ell'`，determinant虽保留为 `h0`，block仍是 singleton。

```text
ATTEMPT_A_THEOREM_PARAMETER_PRESERVING_REGROUP = OCCUPANCY_AT_MOST_ONE
ATTEMPT_A_GROWING_SIGNED_PREFIX = ABSENT
```

唯一自然的 growing coarsening 是按 physical moving row `m`，通过
source-child inverse 合并全部 `p in P_m`。但 coefficientwise exact identity 是

```text
sum_(p in P_m) a_p = w_m.
```

所以该 regroup无损，却精确返回原 literal four-Möbius coefficient；其 `TT*`
仍是同一个 `E_Psi`，并没有变成 TPC-108/TPC-111/TPC-122 的 fixed-`theta`
ordered prefix：

```text
ATTEMPT_B_SOURCE_CHILD_TO_M_REGROUP = EXACT
ATTEMPT_B_REGROUPED_COEFFICIENT = EXACT_LITERAL_W_M
ATTEMPT_B_NEW_THEOREM_DOMAIN = NONE
```

固定 `D0` 的 formal atomic-key count至多为
`Q X^o = X^(267/400+o(1))`。TPC-84只给 census protocol，未执行 actual
active census；允许的 multipliers可以消失或缩放。因此不能把 formal count写成
actual growing-support lower bound。joint row mask只有 entrywise bound，TPC-32
与 prime-Möbius mask boundary明示没有 generic controlled projective/Schur
decomposition。现有可证状态只有：

```text
ACTUAL_GROWING_SUPPORT = CANNOT_BE_CERTIFIED
GLOBAL_FIXED_D0_PROJECTIVE_TOTAL_VARIATION = UNKNOWN
CERTIFIED_ATOMIC_UPPER = X^(267/400+o(1))
SOURCE_BACKED_X_O_PROJECTIVE_DECOMPOSITION = NO
```

直接对 atomic keys 使用 triangle/BV，至多得到 polynomial
`X^(267/400+o(1))` ledger；这远不是允许的 `X^o(1)`。TPC-124也没有给出
把这个新 `m`-fiber dictionary coefficientwise intertwine回 fixed-`theta` prefix
的 theorem。

### 31.3 post-§30 direct-theorem finite source screen

本轮对 2025-01-01 至 2026-08-01 的两个有限检索集合分别完成 `83/83` 与
`105/105` 标题/摘要筛选，并对 surviving candidates读取 theorem body、ranges与
proof chain。没有把 search snippet当作 theorem。

最接近的表面候选是 Carella, arXiv:2202.01071v5，但其主 proof不能作为
source theorem：Theorem 1.1 的 displayed remainder与 proof结尾相差一个 `x`
因子；Lemma 3.1 的 uniform residue-count remainder可取大奇素数 `x`、
`q=(x+1)/2`、`a=q` 直接反例；proof还把 upper error改作 lower bound、把任意
`t` 无映射地设为 `1`、并在双 Möbius展开中无依据使用 `d1 d2<=x`。即使反事实
接受其结论，它也只是 naked two-point fixed-shift statement，不接受 actual
`w_m`、four Möbius legs、growing `D0`、masks、shell、outer labels或 TPC
normalization。其 periodic extension arXiv:2208.12219也没有修复这个 literal
crosswalk。

其余 primary candidates在更早的 theorem-domain门即失败：

* Jiseong Kim, arXiv:2509.24152，把 shift `h` 再求和；其 multiplicative/
  short-interval coefficient class不包含 `w_m`，不能升级为 prescribed `D0`；
* Diao, arXiv:2506.18065，是 almost-all/random binary-form metric theorem，且
  只有 naked 单 Liouville leg，不是 prescribed selected packet；
* Krishnamoorthy, arXiv:2501.10962，是 fake-Liouville small-prime model或
  bounded-away-from-extremes结果，不给 actual Liouville/Möbius cancellation；
* Banks--Shparlinski arXiv:2506.08787 的 ternary `mu(n1 n2 n3)` 不能融合本对象
  四条可能非互素 Möbius legs，且其适用性已由第 27 节旧 cell冻结；
* Cantarini 的 one-Möbius Goldbach / conditional `q`-average仍属于第 28 节旧
  scope，不能提升为 fixed physical phase。

因此没有 candidate同时通过 literal coefficient、fixed `h0=2`、summation/
prefix domain、`X/N/q` ranges、uniform constants、normalization与完整 loss
ledger：

```text
NEW_LITERAL_FIXED_D0_DIRECT_THEOREM = NONE_IN_FINITE_SCREEN
DIRECT_THEOREM_ARITHMETIC_ADVANCE = NO
```

### 31.4 self-kernel / cross-`D0` frame audit

Grimmelt--Merikoski Part I（arXiv:2505.00489）的 evaluation-distribution large
sieve可以接收某些 literal evaluation points，但其 dual/Cauchy reduction右侧仍
保留两份 self-kernel。Hilbert-space Cauchy--Schwarz只是把 cross term改写为
两份 Gram quadratic forms；它没有证明 actual cloud 的 Gram operator norm为
`X^o(1)`，不能被记作免费的 frame theorem。

本轮逐 theorem-interface核对的附近 spectral large sieves也不是该 Gram对象：

* Qi, arXiv:2404.09085 Theorem 1 与 arXiv:2407.17711 Theorem 1控制
  `PGL_2(Z[i])\\PGL_2(C)` cusp spectrum中的 Gaussian Hecke coefficients；
* Lekkas--Voskou, arXiv:2405.01056 Theorem 3控制 Maass forms 的 hyperbolic
  periods，几何变量是 separated scalar points，不是 dense compact cross-`D0`
  evaluation cloud；
* Pascadi, arXiv:2404.04239 Theorems 2--3控制 exceptional Maass Fourier
  coefficients；Hu--Petrow--Young, arXiv:2411.05672控制由 local components
  选择的 automorphic-representation families。

这些 theorem的系数、index set、normalization与 operator都不同；没有一个给
actual `(D0,G,j,outer labels)` cloud 的 literal full self-kernel或 block-Bessel
constant。dense comparable cross-`D0` collisions也未由 source-backed geometric
packing排除。逐 block使用普通 Cauchy至多暴露

```text
Q^(1/2) = X^(267/800+o(1)),
```

远大于 strict `1/400` budget。orbit Poisson zero、nonzero-frequency
density-one、Parseval或 complete-frequency mean均未被改写成 distinguished zero。

```text
FULL_LITERAL_SELF_KERNEL_THEOREM = ABSENT
CROSS_D0_BLOCK_BESSEL_OR_FRAME_THEOREM = ABSENT
GENERIC_HILBERT_CAUCHY_ENDPOINT_PAYMENT = NO
STRICT_1_OVER_400_FROM_FRAME_ROUTE = UNPAID
```

### 31.5 RH-338/339 wrong-object firewall

上游 RH-338研究 `Omega_k` 的 far-orbit atom obstruction，并给出
`R_orb,k=-D_orb,k` 与 `R_k=R_orb,k+R_rest,k`。其中 `2k` 是 orbit/operator
order，不是 TPC physical `h0=2`。该 artifact没有 `m,m',D0,G,j,w_m,E_Psi,N0`、
matched divisor shell或 TPC normalization；aggregate far contribution仍为
`NOT_TESTABLE`。所以：

```text
RH338_TO_TPC32_FIXED_D0_OR_FULL_E1 = ABSENT_WRONG_OBJECT
TPC207_TRIGGER_FROM_RH338 = false
STOP_CELL_CHANGE_FROM_RH338 = NONE
```

发布同步前的 `git fetch` 又发现远端 RH-339 的 17 个 committed files。其 exact
source object是第一 lower sideband `n_minus=2k-2` 上

```text
q_minus = -D_(k-1)_orb + C_minus,
D_(k-1)_orb/H_(k-1) -> +infinity.
```

它证明 separate-absolute orbit/complement route失败，以及 `E_off->0` 必须有
`C_minus=D_(k-1)_orb+o(H_(k-1))`；它没有估计 signed `C_minus`，所以
`E_off` vanishing/nonvanishing仍为 `NOT_TESTABLE`。RH 文中的 “physical” 是
Hardy full-trace boundary orbit；`2k-2` 是 sideband/operator order，不是 TPC
`h0=2`。该对象仍没有 `m,m',D0,G,j,w_m,E_Psi,N0`、matched divisor shell、
TPC determinant或 TPC normalization/loss ledger：

```text
RH339_TO_TPC32_FIXED_D0_OR_FULL_E1 = ABSENT_WRONG_OBJECT
TPC207_TRIGGER_FROM_RH339 = false
STOP_CELL_CHANGE_FROM_RH339 = NONE
```

### 31.6 最终裁决、STOP scope 与合法 reopen interface

本轮精确裁决为：

```text
TPC32_H0_2_FIXED_D0_THEOREM_PARAMETER_PRESERVING_OUTER_REGROUP_
SINGLETON_OR_EXACT_LITERAL_W_M_RETURN_DIRECT_AND_FRAME_THEOREMS_
ABSENT_STOP_SCOPED_NOT_REOPENED
```

状态矩阵是：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
TPC93_DECORATED_REINDEXING = L1 GO
THEOREM_PARAMETER_PRESERVING_REGROUP_OCCUPANCY = AT_MOST_ONE
SOURCE_TO_M_REGROUP = EXACT
REGROUPED_COEFFICIENT = EXACT_LITERAL_W_M
ACTUAL_EDGE_CENSUS = ABSENT
GLOBAL_PROJECTIVE_TOTAL_VARIATION = UNKNOWN
NEW_DIRECT_THEOREM = NONE
CROSS_D0_FRAME = ABSENT
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节新增

```text
DECLARED_TPC32_FIXED_D0_OUTER_REGROUP_AND_POST30_DIRECT_FRAME_
SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

只冻结第 31.2--31.5 节已逐式核对的两个 exact regroup schemes、列出的有限
direct-source candidates与列出的 spectral/frame interfaces。它不冻结：

1. 一个 source theorem直接接受同一 literal `w_m` 并支付 fixed
   `(D0,G,j,h0=2)`、strict endpoint及完整 physical ledger；
2. actual production census，加上 coefficientwise intertwiner和 source-backed
   `X^o(1)` projective decomposition，把 `m`-fibers变成 genuinely growing
   theorem-admissible blocks；
3. 一个明确允许 row primes/cofactors/slopes/outer labels随 `m` 变化、同时保留
   physical determinant与normalization的新 theorem；
4. 一个直接控制 actual full self-kernel的 theorem，或在 fixed-`D0` theorem后
   提供可核查 operator constant的 cross-`D0` block-Bessel/frame theorem。

第 6 节全部旧 method cells保持原 scope `STOP_SCOPED`，尤其 TPC193 V1、
common-`k` V1、tail-failure/A/B V1 与 full-`r_Rr_R` ultra-complement V1。两个
O161 pointwise parents、pair-native reroute、H1 与 global architecture继续
`OPEN`。本节不把第 6 节旧 cell重新包装成新方法。

即便未来 fixed-`D0` gate转为正面，也不自动创建 TPC-207；还必须分别通过
all-`D` uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual packet attachment与完整 provenance gates，
并使页首数学 trigger真实改变。

### 31.7 发布边界

没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入仅为
`TPC_HANDOFF.md`；全部 127 个 protected untracked保持原样且不纳入提交。

```text
POST_WRITE_RELEASE_REGRESSION = 22/22 PASS
TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = 33b0ae61172ea9e54588e650a7c0109cd8ba49fb
FINAL_SYNC_DELTA_FROM_INITIAL_E1C0661 = RH339_NEW_17_FILES
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
FINAL_SYNC_TPC_VERDICT_CHANGE = NONE
```

正式写入后已重新执行全部 22 项只读启动回归与四项 supplemental checks；
TPC-122与 TPC-27--32 legacy writers均未执行。只提交 `TPC_HANDOFF.md`，随后
pull/rebase、push并验证 local `HEAD`、`origin/main` 与 remote
`refs/heads/main` 三个 hash完全一致。

## 32. TPC32 post-§31 direct / metric / actual-census finite trigger refresh

### 32.1 source lock、协议与只读基线

本轮继续以仓库文件与 committed artifacts为事实来源，不把旧聊天当作证明。
启动与正式写入前状态为：

```text
INITIAL_HEAD = 63cd8a91a97af3a0735bc1a10edc8f67f818df12
INITIAL_ORIGIN_MAIN = 63cd8a91a97af3a0735bc1a10edc8f67f818df12
INITIAL_HANDOFF_SHA256
  = 370d337b9d0664b21a457768f3cf91887b4646dc0a820c94c9caaa705070f3bb
INITIAL_TRACKED_DIFF = EMPTY
INITIAL_CACHED_DIFF = EMPTY
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
STARTUP_REGRESSION = 22/22 PASS
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

启动及写前 `git fetch` 均确认 local `HEAD=origin/main`，没有新 RH/TPC remote
object需要拼接。继续 source-lock第 28/31 节锁定并由本节复核的同一 theorem-valid packet：

```text
sigma = 1/10000
lambda = 99979/210000
delta = 7/60
beta = 267/400
Q = X^(267/400+o(1))
J = X^(133/400+o(1))
C = floor(J)
h0 = 2
N0 = JQ^2 asymp XQ
0 < kappa_row < 1/400
```

三条 raw channels、matched difference、content cutoff、canonical `Delta#`、
actual masks/weights、outer labels与 packet natural scale均未删改。`delta=1/20`
truncated-entry family与 TPC-206 的 finite `delta=1/4` fixture均不是这条 source
lock，绝不可拼接。

第 32.2 节的 natural-source finite STOP corpus精确限于逐 ID/version列出的七个
primary sources；更宽的 official arXiv discovery scan只用于找候选，不把 search
counts、snippet或未逐 ID列出的 residual rows写入该 frozen theorem corpus。只有
theorem body、ranges、quantifiers与 proof interface可作为审核材料。

### 32.2 natural binary-Möbius primary theorem refresh

最接近 literal syntax的来源是 Klurman--Mangerel--Teräväinen
`arXiv:2304.05344v2`。其 Theorem 1.2给 fixed-shift two-point natural average，
但只沿一个未定位的 full-upper-log-density scale set趋零且无 rate；不能选择当前
production scale。Theorem 4.1允许 fixed
`f_1(a_1 n+h_1)f_2(a_2 n+h_2)` syntax，但要求

```text
D(f_j, chi_j n^(it_j); x^epsilon, x) <= epsilon,
max_j D(f_j, chi_j n^(it_j); x) >= 1/epsilon,
1/loglog(x) < epsilon < 1/2,
```

并把 affine forms与 implied constants当作 fixed data。Proposition 4.3另给相应
无条件 upper bound，但对下述 `mu_odd` 其首项不产生 saving；其 uniform
Proposition 4.4只允许 coefficients `<=sqrt(log x)`、slopes由一个 fixed `A`
的素因子组成。

determinant prime `2` 的 support condition不是合法 fatal。由 TPC-127 的 exact
parity classification，`a,s`奇且 `sV-aD=2` 时 `D,V`同奇偶；even--even点至少
一个值被 `4`整除，故原 Möbius product为零。定义

```text
mu_odd(n) = mu(n) 1_(2 does not divide n).
```

则逐 `z` 精确有

```text
mu_odd(D(z)) mu_odd(V(z)) = mu(D(z)) mu(V(z)),
```

且 `mu_odd(2^ell)=0`。所以：

```text
KMT_P2_SUPPORT_REPAIR = EXACT_LOSSLESS_PASS
KMT_MU_2_VALUE_FATAL = RETRACTED
KMT_FIXED_H0_2_SYNTAX = COMPATIBLE
```

真正的第一算术 fatal是 truncated distance。对 `mu_odd`，大 `x` 时截断区间的
奇素数上仍为 `-1`；principal character、`t=0`时

```text
D(mu_odd,1;x^epsilon,x)^2
  = 2 log(1/epsilon) + o(1),
```

其余 fixed character/twist同样有正的 `log(1/epsilon)` 量级，不能小于
`epsilon<1/2`。2-adic修改不影响该区间；full-distance lower condition也不能修复
已经失败的 truncated small-distance。即使反事实赠送 small-distance，
`epsilon>1/loglog x`也至多产生
`sqrt(logloglog x)/loglog x = x^(-o(1))`，不是 fixed positive power。
physical `s,d,a,u` 与 `q_prog=as`又随 packet/global scale增长；令
`A=A(X)`或人为放大 theorem length会改变 implied constant、actual prefix domain
与 normalization，均不合法。

其余 theorem-body survivors逐项失败：

* Pilatte `arXiv:2310.19357v2` Theorem 1.1是 reciprocal/logarithmic
  `lambda(n)lambda(n+1)` log-power saving；Remark 2.8 的 natural statement仍只在
  exceptional logarithmic-density scales之外且只有 log saving；
* Frantzikinakis--Host `1502.02646v3` Theorem 1.1要求 underlying homogeneous
  forms pairwise independent；一维 `sz,az`必有理相关，不能增加辅助平均变量后
  升级回 prescribed slice；
* Mangerel `1612.09544v2` Theorem 1.2控制 truncated small-prime model `mu_y`，
  不是 literal `mu`且不给 fixed positive power；
* Kravitz--Woo--Xu `2512.03292v1` Theorem 1.9平均 random polynomial coefficient
  family，不能选择 `(d+sz)(u+az)` 的 named member；
* Frantzikinakis--Klurman--Moreira `2407.08360v3` 的相关 unconditional object是
  two-variable binary quadratic/partition-regularity interface；所需 two irreducible
  correlation在该 source中明确仍为 conjecture，甚至 Liouville case未证；
* Tao--Teräväinen `1809.02518v2` 的 natural two-point结论只在 zero-log-density
  exceptional scales之外、无 positive-power rate；既有 metric/density firewall
  继续适用，不把它包装成新方法。

近期 random Rademacher function、empirical computation、logarithmic
`Omega` statistics、conditional Elliott application等 residual candidates均在
coefficient或quantifier入口失败。没有 candidate同时保留 literal physical
coefficient、fixed `h0=2`、summation/prefix domain、`X/N/q` ranges、uniform
constants、normalization与完整 physical-loss ledger：

```text
NATURAL_PRESCRIBED_UNIFORM_POSITIVE_POWER_THEOREM = NONE
KMT_CONDITIONAL_AFFINE_SYNTAX = L0_WITH_UNATTACHED_L1_INTERFACE_ONLY
DIRECT_ARITHMETIC_ADVANCE = NO
```

### 32.3 determinant-zero / additive-metric type audit

TPC-32 的 distinguished object是 normalized determinant变量的 finite DFT zero：

```text
A_hat_C,q_DFT(0) = sum_n A_C(n)
                 = small-content matched shell.
```

该 `r=0` 明确不是 orbit-variable Poisson zero，也不是 centered divisor-kernel
zero。TPC-170的对象则是 fiber coordinate `z` 上

```text
S_n,p,k(alpha)
  = sum_(j<=k) mu(d+s z_j) mu(u+a z_j) rho(z_j) e(-alpha z_j),
G_n,p(alpha) = (q_prog/T) max_k |S_n,p,k(alpha)|.
```

因此最早的 type fatal为：

```text
TPC32_NORMALIZED_DETERMINANT_DFT_ZERO
  != TPC170_ADDITIVE_FIBER_PHASE_ATOM
DETERMINANT_ZERO_TO_ADDITIVE_ATOM_INTERTWINER = ABSENT
```

三个模数必须分开：

```text
q_X    = prime phase-conductor modulus,
q_prog = a*s affine-progression modulus,
q_DFT  = auxiliary determinant-DFT modulus, q_DFT asymp Q.
```

TPC-94的 actual additive phase
`alpha_xi=epsilon_theta*r_tilde*Omega_xi/(c q_X) mod 1`不把 determinant index
变成 additive atom。TPC-180又给出 named atom/value/locator rows=`0/0/0`、
production schedule rows=`0`。即使反事实补上类型 intertwiner与 registry，
TPC-181仍独立要求 exact schedule、exact bad sets `E_n`、同一 atom及

```text
alpha_star notin limsup E_n.
```

TPC-170 的第一 Borel--Cantelli theorem不要求 independence，但其 a.e. fixed-phase
结论不能选择 prescribed singleton。

本轮读取 theorem body的 exceptional-set candidates也不提供该 bridge：

* Franklin--McNicholl--Rute `1603.01778v1` 与 Franklin--Rodriguez--Rojas
  `2601.03239v1`只在 Schnorr/Martin-Löf random points给 Fourier convergence；
  rational `0`不是 random atom，且无 rate、packet或 loss ledger；
* Michaud--Ramírez `2506.04187v2`控制 Diophantine moving shrinking targets的
  a.e. limsup hitting，事件与方向均不同；
* Bajović--Petković `2607.11180v2`需要 dynamical centered balls/waiting-time
  hypotheses，输出 a.e. orbit hitting，不是 named TPC bad-event avoidance；
* Beresnevich--Hauke--Velani `2406.19198v1` Theorem 4推出 divergence-event
  full bad-limsup membership，方向仍相反。

```text
NAMED_PRODUCTION_ADDITIVE_ATOM = MISSING
EXACT_CROSS_SCALE_PRODUCTION_SCHEDULE = MISSING
SCHEDULE_SPECIFIC_ATOM_AVOIDANCE = MISSING
METRIC_ARITHMETIC_ADVANCE = NO
```

### 32.4 actual census、coefficientwise intertwiner与 projective cost

第 31.6 节 route 2需要依次通过三个独立阶段；current committed data在每阶段
分别 fail closed。

第一阶段的 first fatal为：

```text
SAME_HIGH_BETA_PACKET_SOURCE_LOCKED_ACTUAL_PARENT_REGISTRY = ABSENT
```

TPC-32只给 symbolic physical coefficient；TPC-84明示不执行 census，也没有
archive/manifest/schema/code/output。TPC-205机器 registry为：

```text
production_row_count = 0
production_pair_records = 0
joint_mask_value = null
production_pair_to_omega_crosswalk = FAIL
```

TPC-206也不是补丁。它唯一 selected projection满足：

```text
X = 512
delta = 1/4
D0 = 0
materialized = 13/42
production_occurrence = false
first_missing = opened-D slice
```

其后 `J,Q,T,U0,G_X_row,packet_id,source_locator`、active mask、literal
coefficient、normalizations等继续缺失。artifact又显式规定：

```text
legal_join_with_selected_projection = false
same_packet_or_source_key_as_selected_projection = false
reason = DISALLOWED_CROSS_LINEAGE_SPLICE_INTO_SELECTED_GRAPH
```

所以不能把有限 `X=512,delta=1/4,D0=0` fixture与本轮 growing
`delta=7/60` high-beta packet拼接。

第二阶段中，TPC-93 source-child inverse与 weighted projector identity是真实 exact
`L1` interface，但只在 supplied retained
`omega=(L/R,alpha,gamma,j,u)` 上成立；当前 pair-to-`omega`为 FAIL。TPC-124
的必要且充分 coefficientwise test是

```text
(J Q_D - Q_Z) M = 0,
```

而 actual common native-leaf basis以及 growing `M,Q_D,Q_Z,J`全部未物化。
一条 vector identity `(J Q_D-Q_Z)M c_X=0`不能替代 matrix identity；按
physical `m` coarsening也只精确返回原 `w_m`，不产生新 theorem domain。

第三阶段中，TPC-32 generic joint row mask仍只有 entrywise bound。finite SVD、
formal atomic count或 triangle inequality不能提供 growing uniform projective norm：

```text
CERTIFIED_ATOMIC_UPPER = X^(267/400+o(1))
GLOBAL_FIXED_D0_PROJECTIVE_TOTAL_VARIATION = UNKNOWN
SOURCE_BACKED_X_O_PROJECTIVE_DECOMPOSITION = NO
```

H1不能补洞：TPC-173 qualifying claims=`0`，TPC-174 production witness absent，
TPC-175 coverage=`0/2988`且 eligible carriers=`0`，TPC-179 first missing仍为
`H1.source_backed_local_occurrence_edge_family`。TT-star bilinear pair与 H1 linear
occurrence edge类型不同。

合法的 data-first下一步必须先新增同一 `delta=7/60` packet的 source-locked
`TPC32_SELECTED_HIGH_BETA_ACTUAL_PARENT_REGISTRY_V1`，逐 record至少物化 packet/
scales/source hash、`alpha,gamma,j,h0,D0,G,Delta#`、三 raw labels、全部 mask
values、matched-shell coefficient、support/nonzero status、完整 source-child key、
multiplicities、三层 normalization与 exactly-once atom attachment。随后才可执行
TPC-93 inverse、物化四个 matrices、验证完整 intertwiner，并另证 source-backed
`X^o(1)` projective theorem。第一步本身至多是新的 actual `L1` data gate。

### 32.5 determinant-two firewall与 claim ceiling

TPC-127/128已经给 exact order-preserving pullback

```text
n = s V(z) = a D(z)+2 = su+as z,
mu(D(z))mu(V(z))
  = lambda(as)lambda(n-2)lambda(n)
    mu^2(D(z))mu^2(V(z)).
```

它把 literal pair变成一条 modulus `as`通常随 packet增长的 arithmetic
progression上的 shift-two Liouville product，并严格保留 quotient-squarefree masks、
physical weight、phase、interval origin、outer key与每个 prefix。TPC-128展开 masks
后 modulus进一步增长为 `as k^2 ell^2`。所以 fixed-form、unrestricted、terminal、
reciprocal-weight或 almost-all-scale theorem均不能无损回填。

反向 sanity ceiling也保持：determinant-two family含例如
`(d,s,u,a)=(1,1,3,1)`，即 `mu(z+1)mu(z+3)`。一个对全部 tuples统一的
prescribed natural positive-power theorem会包含 ordinary binary fixed-shift Chowla的
强特例。该观察只是 type/strength stress test；不证明 actual restricted TPC family与
Chowla等价，也不声称未来 theorem不存在。

### 32.6 direct / metric / actual-census 子审计裁决、STOP scope与合法 reopen interface

RH-340 final-sync拼接前，三路 finite refresh的精确子裁决为：

```text
TPC32_H0_2_SELECTED_HIGH_BETA_POST31_DIRECT_METRIC_ZERO_TYPE_AND_
CURRENT_COMMITTED_CENSUS_REFRESH_NO_THEOREM_TRIGGER_STOP_SCOPED_
NOT_REOPENED
```

状态矩阵为：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
KMT_P2_SUPPORT_REPAIR = EXACT_LOSSLESS_PASS
NEW_NATURAL_PRESCRIBED_POSITIVE_POWER_THEOREM = NONE
DETERMINANT_DFT_ZERO_TO_ADDITIVE_ATOM = ABSENT_WRONG_TYPE
NAMED_ATOM_SCHEDULE_AVOIDANCE_BRIDGE = ABSENT
SAME_PACKET_ACTUAL_PARENT_REGISTRY = ABSENT
TPC205_PRODUCTION_ROWS = 0
TPC206_SELECTED_PROJECTION = DIFFERENT_FINITE_FIXTURE_13_OF_42
COEFFICIENTWISE_INTERTWINER = NOT_INSTANTIABLE
GLOBAL_X_O_PROJECTIVE_THEOREM = ABSENT
H1_SOURCE_BACKED_COVERAGE = 0_OF_2988
DIRECT = FAIL
METRIC = FAIL
BAD_ENDPOINT = FAIL
STRUCTURAL = FAIL
DECLARED_CORPUS = FAIL
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节新增三个相互分离的 finite cells：

```text
DECLARED_TPC32_POST31_NATURAL_BINARY_MOBIUS_PRIMARY_
SOURCE_CANDIDATES_V1 = STOP_SCOPED

DECLARED_TPC32_SELECTED_HIGH_BETA_METRIC_SCHEDULE_EXCEPTIONAL_
LIMSUP_AVOIDANCE_SOURCE_CANDIDATES_V1 = STOP_SCOPED

DECLARED_TPC32_HIGH_BETA_CURRENT_COMMITTED_CENSUS_
INTERTWINER_XO_PROJECTIVE_CORPUS_V1 = STOP_SCOPED
```

它们只冻结第 32.2--32.4 节列出的 current sources、typed bridge与 committed
corpus。合法 reopen interface为：

1. 直接接受同一 literal physical coefficient、all prefixes、actual weights/masks/
   outer labels与 `N0` normalization，并给 uniform fixed positive power的新 theorem；
2. 直接控制 distinguished determinant coefficient `A_hat_C,q_DFT(0)` 的 pointwise
   theorem，不经 additive atom偷换；
3. 真正 source-backed named additive atom、同一 actual cross-scale schedule、exact
   `E_n`与 same-event singleton avoidance theorem；
4. 同一 high-beta packet actual parent registry，加 full common-leaf matrices、
   coefficientwise identity及 source-backed `X^o(1)` global projective theorem；
5. 第 31.6 节仍开放的 growing-parameter literal theorem、full self-kernel或
   cross-`D0` block-Bessel/frame theorem；
6. 两个 O161 pointwise parents、pair-native reroute、H1/global architecture或任何
   真正新增、对象与量词匹配的算术输入。

第 6 节全部旧 method cells保持原 scope `STOP_SCOPED`，尤其 TPC193 V1、
common-`k` V1、tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1。两个
O161 parents、pair-native reroute、H1 与 global architecture继续 `OPEN`。本节不把
旧 STOP cell重新包装成新方法。

即使任一 local gate未来转正，也不自动创建 TPC-207；仍须分别通过 all-`D`
uniformity、exactly-once physical cover、original/global normalization、tail-failure、
A/B selection、actual packet attachment与完整 provenance gates，并使页首数学
trigger发生真实 theorem-backed状态变化。

### 32.7 final-sync RH-340 cross-program transfer audit

正式提交前的 remote-tip复核发现 `origin/main` 从启动基线前进：

```text
REMOTE_PARENT = 63cd8a91a97af3a0735bc1a10edc8f67f818df12
REMOTE_NEW_TIP = eb1cf19a28b1d1d38eaece2a6bb0b578f20df969
REMOTE_COMMIT_SUBJECT = Add RH-340 synchronized prefix obstruction
REMOTE_DELTA = 17 NEW RH340 FILES ONLY
TPC_HANDOFF_OVERLAP = NO
TPC_ARTIFACT_OVERLAP = NO
```

RH-340 的 literal object是 RH Hardy normalization上的

```text
p_(sigma,k,n) = tau_(sigma,n)-a_n
                = q_(sigma,k,n)-d_(sigma,k,n),
P_u = sum_(2<=n<u) |p_n| R^n/n,
E_u = sum_(2<=n<u) |q_n| R^n/n,
D_u = sum_(2<=n<u) |d_n| R^n/n,
u = 4k.
```

它精确证明 `|P_u-E_u|<=D_u`，并在自己的 RH source assumptions下同步 analytic
tails；若 `P_(4k)->0`，则 orders `2k` 与 `2k-2` 必须满足两条 signed
orbit--head compensation laws。若先对 orbit、diffuse complement与 head分别取
绝对值，则 mandatory two-atom submajorant发散。但后一个命题明确不 lower-bound
fully signed prefix；aggregate signed prefix、`E_off`与 head budget仍为
`NOT_TESTABLE`，RH-288 determinant gluing仍 `OPEN/not activated`。

该对象在第一项 literal coefficient/type gate即失败。TPC-32需要的是同一
`delta=7/60` high-beta packet、fixed physical `h0=2` 的 Möbius matched shell、
三条 raw channels、content cutoff、canonical `Delta#`、actual masks/weights、
outer labels、canonical signed-prefix order与 `N0=JQ^2 asymp XQ`。RH 的
trace order `n`、moving `2k,2k-2` 与 `R^n/n` absolute budgets没有任何
coefficientwise map到这些 objects；analytic determinant quotient也不是
`A_hat_C,q_DFT(0)`。所以：

```text
REMOTE_RH340_LITERAL_PHYSICAL_COEFFICIENT = FAIL_WRONG_OBJECT
REMOTE_RH340_FIXED_PHYSICAL_H0_2 = ABSENT
REMOTE_RH340_CANONICAL_ORDERED_SIGNED_PREFIX = ABSENT
REMOTE_RH340_X_N_Q_UNIFORM_RANGE_CROSSWALK = ABSENT
REMOTE_RH340_N0_NORMALIZATION = ABSENT
REMOTE_RH340_FULL_PHYSICAL_LOSS_LEDGER = ABSENT
REMOTE_RH340_GROWING_SIGNED_PREFIX_THEOREM = NONE
REMOTE_RH340_SMALL_CONTENT_MATCHED_SHELL_SAVING = NONE
REMOTE_RH340_DISTINGUISHED_DETERMINANT_ZERO_BRIDGE = NONE
REMOTE_RH340_MAXIMUM_TPC_CLAIM
  = CANCELLATION_BLIND_SEPARATE_ABSOLUTE_MAJORANT_OBSTRUCTION_ONLY
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

artifact层的 commit-object独立核查得到 `dependency_manifest.json` 所列
`15/15` SHA256全部匹配，两个 PDF字节相同，且不写文件的 in-memory
`result_payload()`与 committed `result.json`相等。但这些只是 own-file consistency：
manifest刻意排除自身与 `archive_verification.json`；RH-340 commit/directory内没有
对应 archive verifier、RH-340 JSON schema、producer commit field或 RH-262--339
input-artifact hashes。
`experiments/build_result.py` 没有 `--check`，其 `main()` 会无条件重写 committed
`results/result.json`，因此本轮不执行该 writer。同步后优先尝试禁止
bytecode/cache的 pytest，但当前 Python 3.13没有 pytest，Python 3.10的既有 pytest
又缺 `exceptiongroup`，Python 3.9/3.8也没有 pytest；没有安装或修改依赖。随后以
标准库独立重放两个 test files的全部 `12` 个 test-function assertions，并另做
in-memory payload equality、Git-object manifest/hash与 PDF equality检查。

本节及第 6 节新 cell只冻结 commit `eb1cf19` 中 RH-340 到 TPC-32 的
cross-program transfer；不停止未来真正保留同一 packet、literal coefficient、
fixed `h0=2`、canonical prefix、actual weights/masks/outer labels、`N0`
normalization与完整 loss ledger的新 theorem。

### 32.8 final-sync RH-341 cross-program transfer audit

RH-340 audit完成并提交后，最后一次 pull/rebase又取得：

```text
REMOTE_PARENT = eb1cf19a28b1d1d38eaece2a6bb0b578f20df969
REMOTE_NEW_TIP = 6e1478a1a02ff4c3308e829727f8fea1cfbce52c
REMOTE_COMMIT_SUBJECT = Add RH-341 actual first-alias frontier review
REMOTE_DELTA = 23 NEW RH341 FILES ONLY
TPC_HANDOFF_OVERLAP = NO
TPC_ARTIFACT_OVERLAP = NO
PROTECTED_PATH_OVERLAP = NO
```

RH-341冻结的 literal coordinate为：

```text
k = log(1/sigma)/(2 log(lambda)) + O(1)
u = 4k
H_k = k R^(-2k)
p_(sigma,k,n) = q_(sigma,k,n)-d_(sigma,k,n)
P_u = sum_(2<=n<u) |p_(sigma,k,n)| R^n/n
E_u = sum_(2<=n<u) |q_(sigma,k,n)| R^n/n
D_u = sum_(2<=n<u) |d_(sigma,k,n)| R^n/n
```

它综合 RH-332--341 后重申 exact `|P_u-E_u|<=D_u`，并指出 prefix closure仍需

```text
D_(4k) -> 0
E_off,(4k) -> 0
q_(sigma,k,2k) = o(H_k)
```

三项均未由该 batch证明。orders `2k,2k-2`上的 compensation laws也只是
`P_(4k)->0` 的必要条件；source没有 moving signed combined-complement estimate。
abstract cancelling/noncancelling completions只存在于 information-class ledger，
明确没有构造 physical operator，所以它们只证明当前信息不足以决定 aggregate
closure/nonclosure。

RH-341 的 `q_(sigma,k,n)` 是 Hardy trace coefficient而不是 TPC modulus；absolute
trace-order prefix也不是 TPC-111/122 canonical ordered signed fiber prefix。moving
orders `2k` 与 `2k-2` 的差为 `2` 不得改写成 fixed physical `h0=2`。RH 的
`R^n/n,H_k` normalization没有到 `N0=JQ^2 asymp XQ` 的 crosswalk。故逐项 gate为：

```text
REMOTE_RH341_LITERAL_PHYSICAL_COEFFICIENT = FAIL_WRONG_PROGRAM_OBJECT
REMOTE_RH341_Q_SYMBOL = HARDY_TRACE_COEFFICIENT_NOT_TPC_MODULUS
REMOTE_RH341_FIXED_PHYSICAL_H0_2 = ABSENT_MOVING_2K_AND_2K_MINUS_2
REMOTE_RH341_ADJACENT_ORDER_GAP_2_TO_H0_2 = FORBIDDEN_NAME_COLLISION
REMOTE_RH341_PREFIX_OPERATOR
  = ABSOLUTE_TRACE_ORDER_NOT_CANONICAL_SIGNED_FIBER_PREFIX
REMOTE_RH341_X_N_Q_UNIFORM_RANGE_CROSSWALK = ABSENT
REMOTE_RH341_UNIFORM_TPC_CONSTANTS = ABSENT
REMOTE_RH341_N0_NORMALIZATION = ABSENT_HARDY_HK_AND_R_TO_N_OVER_N_ONLY
REMOTE_RH341_FULL_PHYSICAL_LOSS_LEDGER = ABSENT
REMOTE_RH341_GROWING_SIGNED_PREFIX_THEOREM = NONE
REMOTE_RH341_SMALL_CONTENT_MATCHED_SHELL_SAVING = NONE
REMOTE_RH341_DISTINGUISHED_DETERMINANT_ZERO_BRIDGE = NONE_GATE_A_FALSE
REMOTE_RH341_MAXIMUM_TPC_CLAIM
  = CROSS_PROGRAM_WRONG_OBJECT_INFORMATION_CLASS_UNDERDETERMINATION_FIREWALL_ONLY
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

artifact层只读复核得到：

```text
RH341_STDLIB_ASSERTION_REPLAY = 10_OF_10_TEST_FUNCTIONS_PASS
RH341_RESULT_PAYLOAD_EQUALITY = PASS
RH341_GIT_OBJECT_INDIVIDUAL_MANIFEST = 19_OF_19_PASS
RH332_TO_341_GIT_OBJECT_BATCH_MANIFEST = 154_OF_154_PASS
RH341_PDF_BYTE_EQUALITY = PASS
RH341_PDF_SHA256
  = 161e887bf0f9d5df1c4bd111c9f36f3030b7facc3eedcb8ff8a86b36f75f272a
```

当前环境没有完整 pytest，故仍以标准库独立重放 test assertions而不伪报 pytest。
`build_result.py`、`build_archive.py`、`build_batch_archive.py`、
`verify_archive.py` 与 `verify_batch_archive.py` 均没有 `--check`，且各自会重写
committed JSON；本轮全部未执行。现有 manifests锁定 committed Git blobs，但没有
独立 JSON schema，dict equality还有 Python `bool==int` 的 strict-type缺口；
RH-241/263/267/268也只有 symbolic source anchors，没有 claim-specific input blob
provenance。Windows CRLF worktree又不能直接冒充 manifest的 canonical Git-blob
bytes。

commit `6e1478a` 初到时尚未更新 RH handoff；随后 remote commit
`fd0c65e882341e61d39d84f5e0ac7d32c2d323de` 只修改 `RH_HANDOFF.md`，将
endpoint/batch/publication anchor正确更新为 RH-341、RH-332--341 与 `6e1478a`，
route coordinate更新为
`synchronized_actual_first_alias_signed_completion_open`。该 handoff仍明示 moving
noisy coefficient bridge、three same-clock limits、aggregate prefix、determinant与
Gates A--E未证；RH-342只是 future source-lock/investigation route，不是 theorem或
编号授权。所以：

```text
REMOTE_RH_HANDOFF_CLOSURE_COMMIT
  = fd0c65e882341e61d39d84f5e0ac7d32c2d323de
REMOTE_RH_HANDOFF_DELTA = RH_HANDOFF_MD_ONLY
RH_COMPLETED_ENDPOINT = RH_341
RH_ROUTE_COORDINATE = SYNCHRONIZED_ACTUAL_FIRST_ALIAS_SIGNED_COMPLETION_OPEN
REMOTE_RH_HANDOFF_NEW_TPC_OBJECT = NONE
REMOTE_RH_HANDOFF_NEW_TPC_THEOREM_TRIGGER = false
```

这是对既有 RH-341 release的 workflow/provenance closure，不新增 finite TPC method
cell，也不修复 RH-341 strict schema、只读 checker或 claim-specific source
provenance缺口；这些后续仍属于 RH release owner，不得混入本轮只提交
`TPC_HANDOFF.md` 的 TPC release。

本节及第 6 节新 cell只冻结 commit `6e1478a` 中 RH-341 到 TPC-32 的
cross-program transfer；不停止未来真正保留同一 packet、literal coefficient、
fixed `h0=2`、canonical prefix、actual weights/masks/outer labels、uniform
ranges/constants、`N0` normalization与完整 loss ledger的新 theorem。

### 32.9 发布边界

本轮 TPC gate没有创建 TPC-207、论文、paper directory、PDF或构建日志；
RH-340 的 17 个 files与 RH-341 的 23 个 files是已在 `origin/main` 上独立提交的
remote deltas，不是本轮 TPC release。主控正式写入仅为 `TPC_HANDOFF.md`；全部
127 个 protected untracked保持原样且不纳入提交。

```text
POST_WRITE_RELEASE_REGRESSION = 22/22 PASS
TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = fd0c65e882341e61d39d84f5e0ac7d32c2d323de
FINAL_SYNC_DELTA_FROM_INITIAL
  = REMOTE_RH340_RH341_AND_RH_HANDOFF_CLOSURE_AUDITED_NO_TPC_TRIGGER
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
FINAL_SYNC_TPC_VERDICT_CHANGE
  = RH341_WRONG_OBJECT_INFORMATION_CLASS_UNDERDETERMINATION_NO_THEOREM_TRIGGER
POST_SYNC_RH340_PYTEST
  = NOT_RUN_ENVIRONMENT_HAS_NO_COMPLETE_PYTEST
POST_SYNC_RH340_STDLIB_ASSERTION_REPLAY = 12_OF_12_TEST_FUNCTIONS_PASS
POST_SYNC_RH340_RESULT_PAYLOAD_EQUALITY = PASS
POST_SYNC_RH340_GIT_OBJECT_MANIFEST = 15_OF_15_PASS
POST_SYNC_RH340_PDF_BYTE_EQUALITY = PASS
RH340_BUILD_RESULT_WRITER_EXECUTED = NO
POST_SYNC_RH340_READ_ONLY_VALIDATION = PASS_WITH_PYTEST_DEPENDENCY_ABSENT_RECORDED
POST_SYNC_RH341_PYTEST
  = NOT_RUN_ENVIRONMENT_HAS_NO_COMPLETE_PYTEST
POST_SYNC_RH341_STDLIB_ASSERTION_REPLAY = 10_OF_10_TEST_FUNCTIONS_PASS
POST_SYNC_RH341_RESULT_PAYLOAD_EQUALITY = PASS
POST_SYNC_RH341_GIT_OBJECT_INDIVIDUAL_MANIFEST = 19_OF_19_PASS
POST_SYNC_RH332_TO_341_GIT_OBJECT_BATCH_MANIFEST = 154_OF_154_PASS
POST_SYNC_RH341_PDF_BYTE_EQUALITY = PASS
RH341_RESULT_ARCHIVE_BATCH_BUILD_VERIFY_WRITERS_EXECUTED = NO
POST_SYNC_RH341_READ_ONLY_VALIDATION = PASS_WITH_PYTEST_DEPENDENCY_ABSENT_RECORDED
```

正式写入后重新执行全部 22 项只读启动回归与四项 supplemental checks；TPC-122
与 TPC-27--32 legacy writers均不执行；RH-340/341 writers同样不执行。只提交
`TPC_HANDOFF.md`，随后
pull/rebase、push并验证 local `HEAD`、`origin/main` 与 remote
`refs/heads/main` 三个 hash完全一致。

## 33. O161 pointwise current-primary theorem refresh

### 33.1 协议、基线与有限检索范围

本节从仍为 `OPEN` 的两个 O161 pointwise parents出发，不把第 32 节
selected-packet STOP cell换名为新方法。启动、分身交付及正式写前复核均得到：

```text
INITIAL_HEAD = 3d191298f45ee9a00768c4fdcb571550102703ac
INITIAL_ORIGIN_MAIN = 3d191298f45ee9a00768c4fdcb571550102703ac
INITIAL_HANDOFF_SHA256
  = 5a308c1eefdacbf07c791b1cf6a84bb0038116a5035d7847e4076eac45651946
INITIAL_TRACKED_DIFF = EMPTY
INITIAL_CACHED_DIFF = EMPTY
STARTUP_REGRESSION = 22/22 PASS
TPC184_TPC189_DECLARED_SOURCE_LOCKS = 8/8 PASS
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

检索日为 2026-08-01。主检索使用 official arXiv API/search与
`math.NT/recent`；API在完成 exact/broad queries后返回 HTTP 429，随后只
降级到 official arXiv HTML search/recent page，没有绕过限流。raw hit counts、
abstract snippets与 title screens只用于发现，不作为 theorem evidence；正式
裁决全部回到 exact ID/version 的 theorem body、作者 PDF或期刊 primary
metadata。有限 screen不声称全球文献不存在性。

source-lock、DIRECT scan、BAD_ENDPOINT scan与独立 devil's-advocate transfer
audit全部只读；各分身的 before/after `HEAD`、handoff hash、tracked diff与
cached diff均未变化，`files_changed=[]`。

### 33.2 两个合同的 exact type separation

两路当前唯一可共享的 source-backed core为：

\[
 q=as,\qquad t(z)=ad+qz,\qquad
 c_z=\mu(d+sz)\mu(u+az),
\]
\[
 (a,s)=1,\qquad as\ {\rm odd},\qquad su-ad=2.
\]

determinant identity source-backs fixed physical `h0=2`，但不
source-back cancellation、decay或 production attachment。DIRECT 的 exact core是

\[
 F_N(\alpha)=\frac qN
 \sum_{\substack{z\\N<t(z)\le 2N}}
 c_z\rho_{\rm phys}(z)e(-\alpha z),
\]

并需要同一 actual record上的 named `alpha_star`、deterministic
all-prefix/all-scale及 fixed positive power。BAD_ENDPOINT 的 cumulative object是

\[
 A_\rho(T)=\sum_{\substack{z\\0<t(z)\le T}}c_z\rho(z),
\]

而缺失的 local theorem必须对同一 packet的 prescribed bad ancestors
`N_j=T/2^j in E_X_star` 给出

\[
 \frac q{N_j}
 \left|
 \sum_{\substack{z\\N_j<t(z)\le2N_j}}
 c_z\rho_\star(z)
 \right|
 \le C X^{-\sigma}.
\]

从 local block回到 `q/T` cumulative prefix的唯一合法桥仍是
TPC-159 exact telescoping；每个 block必须乘
`N_j/T=2^{-j}`，tail为 `2^{-J}+q/T`。令 `N=T`
只把 DIRECT domain变为 `T<t(z)<=2T`，绝不会产生
`0<t(z)<=T`。

TPC-180/current production census仍精确为：

```text
registry_id = null
named_physical_atom_id = null
phase_value_mod_1 = null
phase_value_source_locator = null
packet_schedule_locator = null
packet_coordinate_rows = []
fixed_h0 = 2
```

因此两个合同当前共同的 production-data首缺是 named production atom/actual
record，但其后的 arithmetic first missing仍须分开：

```text
DIRECT_FIRST_DATA_FATAL
  = SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK
DIRECT_CROSSWALK_SUBGATE
  = NAMED_PRODUCTION_ATOM
DIRECT_FIRST_COUNTERFACTUAL_ARITHMETIC_FATAL
  = DIRECT_ADDITIVE_TWIST_NAMED_ATOM_POWER_SAVING

BAD_ENDPOINT_FIRST_DATA_FATAL
  = PRESCRIBED_BAD_ENDPOINT_ATOM_HAS_NO_SOURCE_LOCKED_VALUE
BAD_ENDPOINT_FIRST_COUNTERFACTUAL_ARITHMETIC_FATAL
  = POINTWISE_NAMED_ATOM_Q_OVER_N_POSITIVE_X_POWER_LOCAL_INCREMENT_
    ON_SCHEDULED_E_X_STAR_ANCESTORS
```

TPC-167 的 `X^(-1/4+o(1))` envelope只属于 Lebesgue phase
`L2`；TPC-159只在 shadow之外给 logarithmic almost-endpoint。
Parseval、phase-a.e.、exceptional-scale density与 good-scale log saving均不能
支付 source-locked named atom。

### 33.3 current-primary theorem-body matrix

最接近 prescribed phase的新增来源是 el Abdalaoui--Nerurkar
`arXiv:2006.07646v2`。Theorem 3.2与 Corollary 3.3对每个 fixed
`theta` 给

\[
 \frac1N\sum_{n\le N}\mu(n)
 f(S^n\mu^2)e(n\theta)\longrightarrow0,
\]

并可令 `f` 为有限 squarefree cylinder。其第一 fatal不是 phase，而是
literal coefficient：`f(S^n mu^2)`只看 squarefree support，完全丢失
第二条 Möbius sign；它不能无损表示
`mu(d+s z)mu(u+a z)`。Remark 3.4又明确该 corollary
non-quantitative。后续仍无 growing affine parameters、uniform threshold/constant、
`q/N_j` block、actual support或 loss ledger。Corollary 4.4的
Liouville结果分别是有限移位窗的 almost-all count与 fixed shift的非极端
`1-epsilon(h)` bound，也不是趋零的 prescribed physical theorem。

Murty--Vatwani *A remark on a conjecture of Chowla* Theorem 1无条件控制
fixed shifts上的

\[
 \mu^2(n+h_1)\cdots\mu^2(n+h_{k-1})\mu(n+h_k)
\]

到任意 fixed log-power；constant显式依赖 `k,A,h_1,...,h_k`。
Theorem 2在 Dirichlet-GRH下有 power bound，但仍是 one-sign coefficient、
fixed shifts且无 additive phase。因此它不能提供缺失的第二条 sign，也不能把
conditional wrong-object power计入 TPC arithmetic credit。

Grimmelt--Teräväinen `arXiv:2607.28091v1` Theorems 1.1--1.2
给 dense sets/primes中 almost-all coefficient-vector configurations；
Theorems 1.3与 6.7是 growing box上的 averaged counting-operator inverse theorem：

\[
 R_H(\lambda;f_1,\ldots,f_k)
 =\sum_{\boldsymbol b}\lambda(\boldsymbol b)
   \sum_x\sum_{m\in[H]}\prod_i f_i(x+b_i m).
\]

这里 `lambda(b)` 是 generic bounded coefficient weight，不是 Liouville；
结论也不是 signed-correlation upper bound。没有 literal two-Möbius pair、
prescribed atom、determinant-two tuple或 `q/N` normalization。

其余新增/未冻结 version-delta candidates均在更早字段失败：

1. Matthiesen `1606.04482v4` 要求超过二维的 convex-body average及
   nonconstant parts两两独立；一维 `s z,a z` 必然共线，不能从多维
   average切到 prescribed physical slice。
2. Browning--Sofos--Teräväinen `2212.10373v2` 对 random
   polynomial coefficient families给 almost-all theorem；actual tuple membership
   未证，`lambda(f(n))` 又缺 Möbius zero masks、atom与 fixed power。
3. Burstein--Iosevich--Sant `2604.14482v1` 的 proved theorem是
   single-Möbius phase-`L1` lower bound；需要的 pointwise square-root
   upper bound只是 source中明示未知的 assumption。
4. Pandey--Radziwiłł `2510.20194v1` 是 single multiplicative
   coefficient的 inverse/pretentious structure theorem，不是 named-atom upper bound。
5. Cantarini--Gambini--Zaccagnini `2603.10241v1` 控制
   `m_1+m_2=n` additive convolution shells（部分结果还需 RH+SZ），不是
   同一 `z` 上的 affine pair prefix。
6. el Abdalaoui--Lin `2607.15960v1` 是 single-Möbius operator
   averages；定量项只来自 Davenport log powers。
7. Pilatte `2604.26564v1` 是 one-factor、origin-averaged short-interval
   Fourier theorem，不是 prescribed two-affine local block。

Ramaré--Zúñiga Alterman `2603.25961v3` 的 LCM-denominator double
sum已由旧 cell冻结，本节只复核其仍为 wrong literal object，不把它列入新增
version-delta cell。只有 publisher metadata、没有取得 primary theorem body的
Baker--Harman record也未提升为 verified candidate。

### 33.4 既有 close routes与独立 adversarial transfer

既有来源只作为 consistency controls，不重新包装：

* Teräväinen--Walker `2303.12574` Lemma 4.2(1)可对 fixed nonparallel
  affine data与每个 fixed atom控制 logarithmically weighted two-Möbius
  correlation，但只是 qualitative/log prefix，非 natural scheduled
  `q/N_j` local block，且无 growing-uniform constant或 fixed power。
* Tao--Teräväinen `2512.01739v2` 经 TPC-147/148/149确实给 natural
  `q/N` terminal-block log saving，但只在
  `N notin E_X_star`；BAD_ENDPOINT本 gate指定的 ancestors恰在
  `E_X_star` 内。
* Pilatte `2310.19357v2`、KMT `2304.05344v2` 分别仍是
  Liouville/logarithmic或 complete-prefix/pretentious-distance interface；都没有
  同一 `rho_star`、scheduled bad block与 fixed power。

独立 devil's-advocate审计钢人化了三种潜在 transfer。对
`2607.28091v1`，把 coefficient weight取成 actual tuple的 delta selector
仍不产生 pointwise theorem：单 tuple natural scale为 `O(N^2/B)`，
而 theorem threshold为 `delta B^k N^2/B`，故需
`delta about B^(-k)`；定理同时要求 `delta^(-C)<=B`，
即 `B^(kC)<=B`，对 `k>=3,C>=1` 不可能。

把两个 Möbius factors在 coprime support上写为一个 Möbius of a quadratic
product会改成稀疏非线性 reindexing，破坏 physical prefix与 normalization。
TPC-127 determinant-two pullback又精确保留
`lambda(n-2)lambda(n)` 两条 sign及 quotient-squarefree masks；TPC-128
展开后 modulus增长到 `as k^2 ell^2`。它们不能把 second sign消掉。

因此以下拼接全部非法：

```text
PHASE_FROM_2006_07646V2
+ RATE_FROM_MURTY_VATWANI
+ GROWING_COEFFICIENT_AVERAGE_FROM_2607_28091V1
!= SAME_RECORD_LITERAL_TWO_MOBIUS_POINTWISE_THEOREM
```

三项没有共同 coefficient、prefix、exceptional set、constant、normalization、
actual support或 loss ledger。`sum a_n=o(N)` 与
`sum b_n<<N/log^A N` 也不推出逐项乘积序列的相同 bound。

### 33.5 裁决、STOP scope与合法 reopen interface

本有限 gate的精确裁决是：

```text
TPC_O161_DIRECT_BAD_ENDPOINT_CURRENT_PRIMARY_ONE_SIGN_OR_AVERAGED_
WRONG_OBJECT_NO_FIXED_POWER_TRIGGER_STOP_SCOPED_PARENTS_OPEN

COMMON_PRODUCTION_RECORD = ABSENT_NOT_TESTABLE
DIRECT = FAIL_CLOSED_AT_NAMED_PRODUCTION_ATOM_PARENT_OPEN
BAD_ENDPOINT = FAIL_CLOSED_AT_SOURCE_LOCKED_NAMED_ATOM_PARENT_OPEN
CURRENT_PRIMARY_SINGLE_SOURCE_SURVIVORS = 0
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节新 cell只冻结第 33.3 节明确列出的 current-primary
version-delta candidates及本节精确 cross-source splice；有限 no-survivor不提升为
global nonexistence。TPC193 V1、common-`k` V1、
tail-failure/A/B V1、full-`r_R r_R` ultra-complement V1以及第 32 节
全部 method cells继续原 scope `STOP_SCOPED`。两个 O161 pointwise
parents、pair-native reroute、H1与 global architecture继续 `OPEN`。

最窄 data-first reopen input仍是一个 source-locked named production atom record，
同一 record须同时物化：atom ID/value/source locator、actual packet/all-scale
schedule、`a,s,d,u,q` 与 determinant witness、canonical translation、
actual support、literal coefficient及全部 masks/weights/outer labels、prefix
order/endpoints、共同 ranges、uniform `C`、positive `sigma`、
正确 target normalization与 no-double-charge physical-loss ledger。

其后 arithmetic theorem仍分别需要：

1. DIRECT：natural `q/N` named-fixed-atom、all physical prefixes/scales
   的 uniform positive-`X`-power bound；
2. BAD_ENDPOINT：对 scheduled `E_X_star` ancestors的同一
   `rho_star` local `q/N_j` fixed-power theorem，再经 TPC-159
   exact telescoping进入 `q/T` cumulative object。

即使任一 O161 local theorem转正，也不自动创建 TPC-207；all-`D`
uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual packet attachment与完整 provenance gates
仍须分别通过。

### 33.6 发布边界

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入仅为
`TPC_HANDOFF.md`；全部 protected untracked必须原样保留且不纳入提交。

```text
POST_WRITE_RELEASE_REGRESSION = 22/22 PASS
TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_GIT_DIFF_CHECK = PASS
POST_WRITE_MARKDOWN_FENCES = 852 MARKERS BALANCED
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = 3d191298f45ee9a00768c4fdcb571550102703ac
FINAL_SYNC_DELTA_FROM_INITIAL = NONE
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

正式写入后必须重跑第 1 节全部 22 项只读回归、TPC-111/124/126/127 四项
supplemental checks与 protected manifest；只提交 handoff，随后 pull/rebase、
push并验证 local `HEAD`、`origin/main`、remote
`refs/heads/main` 三个 hash完全一致。
