# TPC 文字路线图：从局部算术结构到孪生素数终点

更新时间：2026-08-09

当前地图版本：V38

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
        | YOU ARE HERE — V38                      |
        | K lane: canonical Kloosterman emitter   |
        | exact; block-Schatten aggregate OPEN    |
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
当前站在岛 2 通往岛 6 的 Bridge A / Gate B / K 车道；V37 猜想的 exactly-once
physical packet emitter 已由 V38 的 canonical Fourier--Kloosterman 矩阵、零轴消去与
balanced-block SVD 精确构造。最后一段 BP cell bridge 也已有 source engine；现在唯一
主红叉是 literal block-Schatten aggregate，目标 overhead 仍为 `omega<19/800`。
核心算术 saving 尚未证明。**

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

它代表从分析消去岛通往终点岛的核心算术估计。V23--V38 的作用不是宣称已经过桥，
而是不断删除过付、修正 Fourier convention、保持 literal coefficients，并把红叉处的
困难压缩到当前两个明确桥墩；第一个桥墩又保留三条条件车道：

1. `B`：K canonical block-Schatten aggregate优先，E residual energy与 X character route备用；
2. `A`：terminal q-local signed covariance。

Bridge A 当前状态：`OPEN`。

### 4.2 Bridge B：distinguished-seed rare-event 大桥

图像标签：`distinguished-seed genericity`。

它代表从非自治动力学的 metric/rare-event information 转移到指定算术 seed 的 exact
attachment。现有来源没有支付该 attachment。

Bridge B 当前状态：`RESERVE / OPEN_NEW_THEOREM`，不是当前第一优先级。

## 5. 当前精确位置：V38

V36 已把 paid rows之后的 physical numerator压成 prime-only、off-diagonal、coprime
binary ratio core。V37 对每个 prime `q` 与 unit `t` 定义 centered shift packet

\[
F_{q,t}(b)=\sum_{\substack{u\in I_x,\ u\ne t\\u-t\equiv b\pmod q}}
w(u)K_H(u-t),\qquad b\in\mathbb F_q\setminus\{-t\}.
\]

映射 (a\mapsto b=(a-1)t) 给出 exact bijection，并把同一个 core写成

\[
C_x=\sum_q q\sum_{q\nmid t}\beta(t)
\left(F_{q,t}(0)-\frac1{q-1}\sum_{b\ne-t}F_{q,t}(b)\right).
\]

这一步保留完整 compensating background，并只删除 `b=0,ell=0` diagonal。对

\[
Q=x^{1/3},\qquad H=x^{21/32},
\]

每个 residue的有效 shift occupancy是

\[
\frac HQ=x^{31/96}=Q^{31/32}.
\]

V38 先把这个 packet 压成 unit-residue vector `d_q(r)`，再定义 canonical matrix

\[
M_q(m,n)=\frac1{q^2}\sum_{r\in\mathbb F_q^\times}
d_q(r)e_q(-mr-n\bar r).
\]

双重加法正交性精确给出 Kloosterman 发射；删去唯一不满足 prime-unit 条件的
`(m,n)=(0,0)` 后，只产生显式
`lambda_q=(q^2-q+1)/q^2` 自返因子。随后把频率域划成边长约 `sqrt(q)` 的 consecutive
blocks，并逐 block 做 SVD，便得到零余项、每个矩阵元 exactly once 的 BP-admissible
rank-one cells。也就是说，V37 的 emitter 猜想已经关闭。

当前第一条真正开放的新定理是同一个 literal packet 的 canonical block-Schatten
aggregate：

\[
\sum_q\frac{q^2}{\lambda_q}
\sum_{I,J}\|M_q[I,J]\|_{S_1}
\ll x^{5/3+o(1)}Q^\omega,
\qquad \omega<\frac{19}{800}.
\]

再接 Blomer--Pascadi fixed-modulus `(Q^{-1/32})` cell saving，条件输出仍是

\[
x^{53/32+\omega/3+o(1)},
\]

并保留严格 endpoint margin

\[
\frac{19}{2400}-\frac\omega3>0.
\]

generic block nuclear/Frobenius baseline会损失 `Q^(1/4)`，超过 BP 的 `Q^(-1/32)`
收益；若先假设 packet energy，再绕道 BP，反而比直接 Cauchy 多付 `x^(7/96)`。
所以当前 open theorem必须直接利用 literal blocks 的 joint Schatten structure，不能把
普通 packet energy 换名。E lane 与 X lane继续作为独立后备；任何 B lane闭合后，
terminal q-local A仍须另付。

## 6. 图像名称与仓库名称的对应

这里最容易出现的误解，是把图像 Bridge A/B 与仓库内部 A/B/C gate 当成同一套编号。

| 图像语言 | 仓库 V38 语言 | 关系 |
|---|---|---|
| Bridge A：解析 collective saving | `B(K/E/X)` 后接 `A` | 图像的一座大桥被拆成多车道 B 与 terminal A |
| Bridge B：distinguished-seed genericity | `C` symmetry-breaking reserve | 都是动力学/指定 seed 后备线 |
| 核心算术估计 | K block-Schatten aggregate `omega<19/800` + terminal covariance | 当前 red-X 的优先施工方案 |

仓库选择路线为：

```text
K_CANONICAL_BLOCK_SCHATTEN_AGGREGATE
OR_E_WHOLE_RESIDUAL_ENERGY
OR_X_JOINT_CHARACTER_DECOUPLING
THEN_A_TERMINAL_COVARIANCE
THEN_C_SYMMETRY_BREAK_RESERVE
```

## 7. 当前状态防火墙

截至 V38：

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

优先级更新为：

1. **B/K：证明 direct canonical block-Schatten aggregate**，使用已建的 exact
   Fourier--Kloosterman/SVD emitter，并把 aggregate overhead 控制在
   `omega<19/800`；首个 benchmark 为 `omega=1/100`；
2. **B/E 与 B/X：保留并行后备**，分别是 `sigma<13/4800` whole residual energy和
   `kappa>403/1200` joint character theorem，不与 K lane叠加 theorem credit；
3. **A：证明 terminal q-local signed covariance**，不能用 off-zero norm 循环支付
   physical scalar；
4. **C：只在前三条路线真实阻断或新 source 出现时，重开 distinguished-seed
   symmetry-breaking/dynamics reserve。**

最窄 first fatal：

```text
NO_LITERAL_THEOREM_BOUNDS_THE_CANONICAL_PHYSICAL_BLOCK_SCHATTEN_AGGREGATE_WITH_OMEGA_LESS_THAN_19_OVER_800
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
| 2026-08-09 | V38 | Bridge A / Gate B / K lane：canonical emitter built, Schatten pier open | parent `c89d3a0fc5201cba2ef27e37cf388ad763c4d59b`; V38=current working release | 以 double orthogonality、zero-axis factor 与 balanced SVD 精确关闭 emitter construction；主红叉收缩为 `omega<19/800` physical block-Schatten aggregate；arithmetic 仍为 NO |
| 2026-08-09 | V37 | Bridge A / Gate B / K lane：loss-budgeted shift packet | parent `2b199a9989f378666e5bc7b9bb8f2952015f75de`; V37=current release commit | 将零损耗 `Q^(-31/32)` 口号改写为 exact packet 与 `omega<19/800` emitter contract；状态仍为 arithmetic NO |
| 2026-08-08 | V32 | Bridge A 桥头：single-scale residual oscillation | `66dcd9a08b1adb92b117941aae92b9a17ab6298f` | 首次将岛屿图保存为可更新文字地图并收录配套原图；未改变数学状态 |
