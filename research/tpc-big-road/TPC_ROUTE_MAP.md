# TPC 文字路线图：从局部算术结构到孪生素数终点

更新时间：2026-08-08

当前地图版本：V32

性质：`LIVING_DESCRIPTIVE_MAP / NON_AUTHORITATIVE_SUMMARY`

> 仅供路线导航与沟通参考，不构成 theorem evidence、算术进展证明或编号触发。

配套原图（同样仅作高层导航参考）：

![TPC 岛屿地图：通往孪生素数猜想的大致路线](figures/tpc_route_cn.png)

本文件把“TPC 岛屿地图”的图像语言保存成可搜索、可版本化、可持续更新的
Markdown。它用于回答三个问题：已经走过哪些结构层、当前站在哪里、下一座真正需要
证明的桥是什么。

本文件不是定理状态的最终权威。若这里与其他文件发生差异，按以下顺序取当前事实：

1. 仓库根目录的 [`TPC_HANDOFF.md`](../../TPC_HANDOFF.md) 页首及其 current section；
2. 当前 big-road proof 与 fail-closed checker；
3. [`README.md`](README.md) 的当前版本节；
4. 本文字地图；
5. 历史图片、旧聊天和历史 handoff cells。

## 1. 一眼看懂当前路线

```text
岛 1：基础算术岛
  端法、Möbius 相关符号、筛法基线、低维动力学类比
                |
                v
岛 3：固定原子岛
  fixed h0=2、named atom、determinant-two 双 Möbius 原子
  [对象与类型已经锁定；尚无 fixed-atom arithmetic credit]
                |
                v
岛 4：Pair-native / H1 结构岛
  literal occurrence carrier、MASTER mask、ordered +2/-1、hybrid、hard shell
  [exact L0 carrier 已经建立]
                |
                v
岛 2：分析消去岛
  local source engines、Jutila/Farey、Kloosterman/BC、collective residual
                |
                v
        +------------------------------------------+
        | YOU ARE HERE — V32                      |
        | 单尺度 whole-residual oscillation gate   |
        | Q^osc_Y0(R_x) bound = OPEN               |
        +------------------------------------------+
                |
                v
Bridge A 的 terminal 桥墩
  q-local signed covariance = OPEN
                |
                v
岛 6：TPC 终点岛
  Twin Prime Conjecture

后备线：岛 5 非自治动力学 -> Bridge B distinguished-seed genericity
辅助线：岛 7 Hénon / 几何提升
```

一句话定位：**我们已经完成从岛 3、岛 4 到 literal analytic object 的结构层搭桥，
当前站在岛 2 通往岛 6 的 Bridge A 桥头；困难已被压缩成一个精确单尺度估计，但核心
算术 saving 尚未证明。**

## 2. 图例与状态语言

| 标记 | 含义 |
|---|---|
| `DONE_L0` | exact algebra、对象、符号、support 或 compiler 已经证明 |
| `SOURCE_BACKED_LOCAL` | 有 primary-source theorem 支持局部 engine，但未付全局 reassembly |
| `ACTIVE_OPEN` | 当前主路线真正需要的新定理 |
| `RESERVE` | 合法后备路线，当前不优先 |
| `STOP_SCOPED` | 精确到某个接口的失败，不是全局不可能性结论 |
| `GOAL` | 最终数学目标，不能由 checker 或有限 fixture 自动触发 |

地图中的“到达某岛”必须区分结构到达与算术到达。尤其是固定原子岛：fixed
`h0=2`、normalization 和 literal carrier 已经严格冻结，但这不等于已经获得固定原子的
点态衰减或 endpoint credit。

## 3. 七座岛屿

### 3.1 岛 1：基础算术岛

角色：提供端法、Möbius 权、筛法分解、素数分布基线，以及与低维动力系统之间的启发式
类比。

当前状态：`DONE_BASELINE`。这些材料是出发点，不是孪生素数结论。

### 3.2 岛 2：分析消去岛

角色：容纳 large sieve、shifted convolution、Bessel/Gram、Jutila/Farey、Poisson、
Kloosterman-fraction 与 collective cancellation 等解析工具。

当前状态：`ACTIVE`。很多局部 engine 已经 source-backed，真正缺少的是对同一个 literal
whole object 的 collective bound，而不是再增加一个与物理系数脱节的局部估计。

### 3.3 岛 3：固定原子岛

角色：把目标锁定为 fixed physical `h0=2`、指定原子、精确 signs/masks/weights，而不是
平均 shift、a.e. phase 或可移动的 model atom。

当前状态：`DONE_L0 / ARITHMETIC_OPEN`。对象和量词已经合法化，但
`FIXED_ATOM_CREDIT=0`。

### 3.4 岛 4：Pair-native / H1 结构岛

角色：保存 actual occurrence carrier、pair-to-omega crosswalk、opened-D packet、MASTER
selector、ordered `+2/-1`、Möbius/log、units、hybrid 和 hard shell。

当前状态：`DONE_L0`。这是当前 analytic residual 能够被称为“同一个 literal object”的
基础。

### 3.5 岛 5：非自治动力学岛

角色：尝试 stage-preserving exact encoding、moving gap-2 rare events、covariance/variance、
dynamical Borel--Cantelli 和 distinguished arithmetic seed。

当前状态：`RESERVE / STOP_SCOPED_AT_CURRENT_SOURCE_INTERFACE`。现有 a.e.、ASIP 或
uniform-observable 结果不能自动命中同一个 prescribed arithmetic seed；不能由 Fubini、
generic parameter 或 metric statement 偷换固定算术截面。

### 3.6 岛 6：TPC 终点岛

角色：孪生素数猜想的无穷多个素数对结论。

当前状态：`GOAL_NOT_REACHED`。`TPC_207_TRIGGER=false`，不得因为路线图、checker PASS
或持续工作流授权而自动编号。

### 3.7 岛 7：Hénon / 几何提升岛

角色：提供 semiconjugacy、保持排列和几何可视化等辅助提升。

当前状态：`OPTIONAL_RESERVE`。它可以帮助理解或提供条件路线，但不是当前支付解析
endpoint 的主桥。

## 4. 两座图像大桥

### 4.1 Bridge A：解析 collective-saving 大桥

图像标签：`four-Möbius collective saving`。

它代表从分析消去岛通往终点岛的核心算术估计。V23--V32 的作用不是宣称已经过桥，
而是不断删除过付、修正 Fourier convention、保持 literal coefficients，并把红叉处的
困难压缩到当前两个明确桥墩：

1. `B`：base-scale whole-residual oscillation；
2. `A`：terminal q-local signed covariance。

Bridge A 当前状态：`OPEN`。

### 4.2 Bridge B：distinguished-seed rare-event 大桥

图像标签：`distinguished-seed genericity`。

它代表从非自治动力学的 metric/rare-event information 转移到指定算术 seed 的 exact
attachment。现有来源没有支付该 attachment。

Bridge B 当前状态：`RESERVE / OPEN_NEW_THEOREM`，不是当前第一优先级。

## 5. 当前精确位置：V32

令

\[
P_x(\alpha)=B_x(\alpha)\overline{W_x(\alpha)},\qquad
L_x(\alpha)=\sum_h M_x^{\rm loc}(h)e(-h\alpha),
\]

并定义同一个 literal whole residual

\[
R_x(\alpha)=P_x(\alpha)-L_x(\alpha),\qquad
\widehat R_x(h)=e_x(h).
\]

取

\[
H=x^{21/32},\qquad Y_0=2^{\lceil\log_2 H\rceil},
\qquad H\le Y_0<2H.
\]

把圆周分成 `2Y` 个 aligned half-open cells，并只模掉一个 global complex constant：

\[
\mathfrak Q_Y^{\rm osc}(R)
=\inf_{c\in\mathbb C}Y\sum_{j=0}^{2Y-1}
\left(\int_{I_{Y,j}}|R(\alpha)-c|\,d\alpha\right)^2.
\]

V32 已证明 exact compiler：

\[
\sum_{0<|h|\le Y}|\widehat R(h)|^2
\le 16\mathfrak Q_Y^{\rm osc}(R),
\qquad
\mathfrak Q_{2Y}^{\rm osc}(R)\le2\mathfrak Q_Y^{\rm osc}(R).
\]

因此当前第一条真正开放的新定理是

\[
\boxed{
\mathfrak Q_{Y_0}^{\rm osc}(R_x)
\ll x^{2+2\sigma+o(1)},
\qquad 0\le\sigma<\frac{13}{4800}.}
\]

它一旦证明，就通过 Schwartz shells 支付完整 off-zero residual：

\[
\mathcal N_e\ll x^{1+\sigma+o(1)},\qquad
|E(e_x)|\ll x^{191/192+\sigma+o(1)}.
\]

但 global constant quotient 不改变 Fourier zero mode。若 `R_x` 是任意常数，
`Q^osc=0` 而 physical axis 仍可任意。因此 terminal q-local covariance 必须独立支付。

条件 endpoint ledger 为

\[
0<\eta_*<\min\left\{
\eta_R,\frac{19}{2400},\frac{13}{4800}-\sigma
\right\}.
\]

## 6. 图像名称与仓库名称的对应

这里最容易出现的误解，是把图像 Bridge A/B 与仓库内部 A/B/C gate 当成同一套编号。

| 图像语言 | 仓库 V32 语言 | 关系 |
|---|---|---|
| Bridge A：解析 collective saving | `B` 后接 `A` | 图像的一座大桥被拆成两个可审核桥墩 |
| Bridge B：distinguished-seed genericity | `C` symmetry-breaking reserve | 都是动力学/指定 seed 后备线 |
| 核心算术估计 | `Q^osc_Y0` bound + terminal covariance | 当前 red-X 的精确数学化 |

仓库选择路线为：

```text
B_SINGLE_SCALE_RESIDUAL_OSCILLATION
THEN_A_TERMINAL_COVARIANCE
THEN_C_SYMMETRY_BREAK_RESERVE
```

## 7. 当前状态防火墙

截至 V32：

```text
ROUTE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
NUMBERED_RELEASE = NO
```

以下事实不得从路线图中推断：

- exact compiler 不等于 arithmetic saving；
- finite fixture 或 checker PASS 不等于渐近定理；
- averaged/a.e. phase 不等于 named fixed atom；
- source-backed local engine 不等于 whole-object reassembly；
- off-zero control 不等于 physical zero-axis payment；
- route advance 不自动创建 TPC-207。

## 8. 下一步大路

优先级保持：

1. **B：证明 base-scale collective oscillation**，对象必须是保留 MASTER mask、ordered
   `+2/-1`、Möbius/log、hybrid 与 hard shell 的 literal occurrence emitter；
2. **A：证明 terminal q-local signed covariance**，不能用 off-zero norm 循环支付
   physical scalar；
3. **C：只在前两条路线真实阻断或新 source 出现时，重开 distinguished-seed
   symmetry-breaking/dynamics reserve。**

最窄 first fatal：

```text
BASE_SCALE_COLLECTIVE_OSCILLATION_BOUND_FOR_LITERAL_MASTER_HYBRID_OCCURRENCE_EMITTER
```

## 9. 后续更新协议

每次更新本地图时：

1. 先读取最新 `TPC_HANDOFF.md` 页首和 current section；
2. 只在新的 sealed big-road release 或 numbered theorem 改变状态后移动 `YOU ARE HERE`；
3. 记录版本号、日期、release commit、proof 和 checker 路径；
4. 将“结构完成”“条件完成”“算术完成”分开登记；
5. 保留旧路线的 `STOP_SCOPED` 原因，不把改名当成 reopen；
6. 若只是图片美化、文字澄清或 checker 加固，不改变 arithmetic status；
7. 更新后核对本文件、big-road README 与 Handoff 不冲突。

## 10. 版本记录

| 日期 | 地图版本 | 当前位置 | Release anchor | 变化 |
|---|---|---|---|---|
| 2026-08-08 | V32 | Bridge A 桥头：single-scale residual oscillation | `66dcd9a08b1adb92b117941aae92b9a17ab6298f` | 首次将岛屿图保存为可更新文字地图并收录配套原图；未改变数学状态 |
