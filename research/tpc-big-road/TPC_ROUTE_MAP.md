# TPC 文字路线图：从局部算术结构到孪生素数终点

更新时间：2026-08-24

当前地图版本：V85 / TPC-232

性质：`LIVING_DESCRIPTIVE_MAP / NON_AUTHORITATIVE_SUMMARY`

当前编号锚点：`TPC-232`（`PROVED_ARITHMETIC_OBSTRUCTION_L1 / SUBCRITICAL_GROWING_DEPTH_STOP_SCOPED`）；
对应论文目录为 `papers/tpc-232-subcritical-growing-resonance-depth/`。TPC-232 对
modeled clock `h=4LQ` 建立 exact one-wrap compiler 与 coefficient-uniform Selberg sieve，
证明 `C_L/P->0` whenever `L=o(log Q/loglog Q)`，把 subcritical growing-depth route
渐近封口。critical-depth sufficiency、actual V59 clock attachment 与 full Gate B 仍 OPEN。

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
        +--------------------------------------------------+
        | YOU ARE HERE — V85 / TPC-232                     |
        | SUBCRITICAL GROWING-DEPTH OBSTRUCTION            |
        | critical depth / actual source OPEN              |
        +--------------------------------------------------+
                |
                v
Bridge A 的两个主桥墩
  one full-shell signed fold + one zero-hole prime-BDH compiler = OPEN
  q-transverse row variance = optional maximal-prefix railing
                |
                v
岛 6：TPC 终点岛
  Twin Prime Conjecture

后备线：岛 5 非自治动力学 -> Bridge B distinguished-seed genericity
辅助线：岛 7 Hénon / 几何提升
```

V61 的位置变化建立一个真实 structural pier：zero-hole variance在 nonzero additive
frequencies上是 complete-graph tight frame；同一 edge mass exact删除 `(q-2)`
coefficient diagonal，保留 outer `q` 后

```text
V_0 = 1/[q(q-1)] sum_e |T_e|^2,
qR_0 = 1/(q-1) sum_e E_e^circ,
Delta_(k,k+d)(n)=e_q(-kn)(1-e_q(-dn)).
```

literal two-frequency edges不能 strict sparsify；每个 weight都被强制为 `1/(q-1)`。
所以下一块桥面不再是“如何分开估计 equal/off-equal frequencies”，而是“如何在任何
edge/fiber triangle之前，把完整 oriented `(d,k)` frame集体变换成 source-valid
Kloosterman cells并保留 prime-shell signed reassembly”。

TPC-209 证实了 fixed divisor 内的 shared dual lattice：`n=qr+kD` 对同一
`D` 的 entire edge frame 是 exact bijection。它也精确暴露了跨 divisor 的残余：
`Y=sum_D c_D U_D B_D`，而不是一个公共 scalar packet。multiplicative Fourier
把 `U_D` 对角化为 character multiplier，却通过 Gauss crosswalk 返回 V59
nonprincipal-character interface。sharp alignment (`||L_c||=||c||_2`) 和
`q=5` resonance 说明 frame geometry 本身不给 divisor cancellation。

TPC-210 随后证明 isolated dual nodes 与 `C_c^infty` bumps 可以精确实现任意有限
residue profile；把 `c_D=mu(D)` 和 `B_D=mu(D)U_D^*z` 放回后，coherent-to-diagonal
ratio 恰为 divisor count，profile-aware energy 只能写成 cross-divisor PSD Gram form。
这里的 aligned family 允许独立 `F_D`，不是 literal coupled TPC coefficient family。

一句话定位：**我们仍在岛 2 的 Bridge A / Gate B 接缝；当前位置是 V85 / TPC-232 的
subcritical growing-depth obstruction。exact one-wrap compiler 与 coefficient-uniform
Selberg sieve 已证明每个 `L=o(log Q/loglog Q)` 的 modeled resonance family 只有 `o(P)`
incident rows；fixed-comparability 模型不能支付 fixed saving，故整个 subcritical 支路
`STOP_SCOPED`。下一条大路是 audit critical-depth row mass/degree，再回到 actual V59
source-to-row crosswalk。FULL_GATE_B、global strict `1/400`、`L2` 和 fixed-atom credit
继续 OPEN/UNPAID/NO。**

一句话定位（V61 历史位置）：**我们已经完成从岛 3、岛 4 到 literal analytic object 的结构层搭桥，
当前站在岛 2 通往岛 6 的 Bridge A / Gates A--B 接缝；V38 已完成 canonical
Fourier--Kloosterman emitter，V39 看清 nuclear/Schatten toll，V40 把 scalar 压到
`q`-row，V41 又把每个 row 精确拆成已付的三剩余类模型 `m_q` 与 residual `rho_q`。
V42 再把 residual的最窄目标识别为 positive physical Gram collision，并用 V35
proper-factor identity将 preferred implementation变成 dyadic Möbius--prime directional
cells。V43 又在 outer absolute 之前完成 centered Poisson：`d<=H/(4Q)` 的非零 alias
全部精确消失，但物理 `u=dk` 删除会把 zero axis 原样返回。由此得到
`C=A-L_pr*S+paid errors`，首次把 Gate B 与 terminal Gate A 写成同一 literal scalar
bridge。V44 再把第一段 transition exact gcd-reduce 为 reduced modulus
`Q^(31/32)` 到 `Q^(399/400)` 上的 principal Ramanujan mean 与 centered reciprocal
variance；physical nonunit correction 与 background 都已付。V45 修正了把
imprimitive characters 一概视为 `x^o(1)` 的过粗步骤，按 primitive conductor
`d` 分层。在 `D0=P^(1/2)=x^(1/192)` 以上，second/fourth multiplicative-large-sieve
两界插值严格给 coefficient variance `P^(3/2)`，physical output
`x^(213/128+o(1))`，比 endpoint 留 `1/9600` margin。principal 与
`1<d<D0` 的 induced modes被保留成一个 explicit Gauss--Ramanujan structured major
spectrum。V46 随后回到 original proper-factor modulus，在 outer absolute前以
shifted-prime/hybrid Euler profile作 exact split。local component已由 V29
Bettin--Chandee compiler支付到 normalized exponent `1891/1920`；全部 principal、
low conductor 与 possible exceptional modes统一进入一个 all-residue AP--BDH
variance。reciprocal occupancy energy已初等支付为 `P^2=x^(1/48)`，因此只要
`E_AP^tr << x U^2 x^(rho+o(1))`、`rho<33/100`，完整 transition就条件闭合。
V47 进一步证明 reciprocal occupancy 的 additive zero coordinate精确为空，故 full
all-residue AP energy严格降为 centered residue covariance；再以同一 local profile
逐项拆出 prime error与 hybrid error，首选门成为二者之差的 signed centered
covariance。V48 随后 exact证明 V45 conductor split与 V46 Euler/AP split是同一个
transition scalar的两种 decomposition，并得到
`R_AP=M_low+V_high-L_pf`。high conductor与 local Euler都已付款，故当前红叉进一步
缩成 direct low-conductor signed scalar；更强的 source-native版本是对完整
prime--hybrid character--Ramanujan tower证明 `delta>1/200` 的 energy saving。scalar
splice不允许把两种 energy作正交相减。V49 又选择
`D1=x^(49/9600)`，用 V45 block estimate支付 `D1<=c<D0` 的 critical
collar；全部 `c>=D1` 输出到 `31951/19200`，留出严格
`1/19200` margin。当前唯一 transition 红叉成为 local-centered ultra-low
principal/generic/possible-exceptional 三车道 signed scalar；exceptional primitive
type至多一个，但其 induced cofactor tower不能删除；
V50 将这一固定 midpoint 推广为
`D_delta=x^(1/200+2delta)`、`0<delta<1/9600`。每个 cut 的 complement
都精确付到 `x^(1997/1200-delta+o(1))`。global Siegel quality又穷尽分成
两世界：unbounded world 由 Matomaki--Merikoski 条件性直达无限多 twin primes；
bounded world只留下一个可依赖固定全局界 `B` 的 endpoint-matched signed core
theorem。当前世界未知，bounded core仍无 literal source theorem。
V51 随后把 transition short orientation、long-Möbius reverse Type I 与 balanced
Type II 重新放回同一个无序因子对：mixed 与 balanced logarithmic numerator均至多
rank two，`1/log(s ell)` 由一维 Abel compiler exact移除；补回物理对角后的
pair row又与 V43 Gate-A numerator只差已付款误差。orientation-first Poisson会破坏
exact folded zeros，所以当前首选大跨改成一个 fold-first mixed-plus-balanced
signed theorem。V52 又把这个 scalar 压成 compensated prime dilation，并把
character endpoint 写成 `rho_BW*sqrt(E_B E_W)`。diagonal-scale marginals加普通
Cauchy恰差 `1/400`；首选新桥墩因此是同一 pair/physical packet 的
`kappa>1/400` angular dispersion，或总 saving `>1/200` 的 super-BDH fallback。
V53 再把同一个 compensated scalar按素模数压成 completed pair rows
`A_q^circle`，并证明其 collision diagonal为 `x^(95/48+o(1))`。只要 row energy
相对 diagonal至多损失一个 `Q=x^(1/3)`，Gate A numerator便到
`x^(53/32+o(1))`。V40 Gate B有同尺度 diagonal，于是当前首选大跨成为一个
对两种 literal rows同时成立的 symmetric two-species row-Bessel theorem；它条件性
给 physical output `x^(95/96+o(1))`，到目标剩 `19/2400`。这个 theorem仍未证明，
PAD与MPD保留为独立后备。V54 随后在估计前证明
`P_q-C_q=kappa_q*S_physical-E_q`，且 `sum_q|E_q|^2<<x^(95/48+o(1))`。
因此两种 rows 的 transverse projection只差 paid error，而唯一不同的 longitudinal
coordinate以 `x^(79/96+o(1))` 误差直接抽取 physical residual。V55 又逐模数
证明 `(P_q-C_q)/kappa_q=S_x+O(x^(79/96+o(1)))`，并对任意 q-space operator
证明 exact dichotomy：杀掉 kappa只剩 transverse paid error；保留 kappa就成为
terminal estimator。`kappa/N_kappa` 在 L2 error-ball model内唯一 minimax，
PSD/TT-star也无第三种 preliminary case。当前施工点因此前移到 q-compression之前：
V51 maximal partial-shell或 V52 PAD作为 Gate A，V42/common transverse作为 Gate B；
longitudinal cable只作为终点读出。V56 又把 maximal endpoint motion编译成一棵
预声明 pruned dyadic tree：每个短 leaf由 `q|P_q|<<x^(53/32+o(1))` 绝对支付，
`lambda=19/4800` 时仍留 `19/4800` margin；每个 prefix只需 `O(log Q)` 个 aligned
large nodes加一个 partial leaf。于是 maximal Gate A 与一个 uniform canonical-block
theorem在 power scale上等价。V57 再以 full-shell `K(Y)/K_*` root anchor exact
消去每个 prefix的 physical mode；只要 Gate-B row-Bessel成立，全部 endpoint motion
自动支付。于是 selected route只剩一个 V51 full-shell signed fold与一个 V53 Gate-B
row energy，而 V56 tree降为更强 fallback。V58 随后把 Gate-B row的 terminal
方向 exact识别为 V35 proper-factor centered scalar，selected endpoint burden收窄为
两个 signed scalars。V59 再对 Gate-B scalar作 complex polarization：它精确等于
四个 literal sequences `beta+i^j w` 的 prime-weighted、kernel-localized、
diagonal-corrected reduced-residue BDH余项的 signed组合。mesoscopic block数为
`x/H=x^(11/32)`，每块自然尺度为 `Q^2H=x^(127/96)`，全局尺度恢复
`xQ^2=x^(5/3)`；关键 gap `Q^2/H=x^(1/96)` 与 Blomer--Pascadi fixed-cell
`q^(-1/32)=x^(-1/96)` 的临界时钟 exact对齐。但现有 theorem只估计已发射的
fixed-modulus cells，没有把四个 literal polarized blocks集体编译、保留 prime-only
modulus与 signed reassembly。当前真正未跨过的是 V51 Gate-A root 与这个 V59
collective prime-BDH compiler。核心算术 saving
尚未取得。**

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

它代表从分析消去岛通往终点岛的核心算术估计。V23--V39 的作用不是宣称已经过桥，
而是不断删除过付、修正 Fourier convention、保持 literal coefficients，并把红叉处的
困难压缩到当前两个明确桥墩。V43 进一步证明这两个桥墩由一个 zero-axis
transference scalar精确相连；它们仍需分别给 saving：

1. `B`：V42 positive physical Gram / MPD仍是 Gate-B 的平行充分实现；
2. `A/sequential transition`：V50 对每个 `0<delta<1/9600` 取
   `D_delta=x^(1/200+2delta)`，并支付全部 `c>=D_delta` 到
   `x^(1997/1200-delta+o(1))`；unbounded Siegel quality已有 conditional
   TPC exit，bounded world保留 `B`-dependent direct signed core；
3. `A/pair-row deck`：V51 先折叠 mixed transition/reverse-Type-I 与 balanced
   two-long，V52 写成 compensated prime dilation，V53 再完成每个 `q`-row的
   signed cancellation；V54 证明 pair row与 V40 physical row的 transverse
   projections只差已付款误差，所以一个 common transverse theorem足够覆盖两者；
   V56 再把 V51 moving endpoint精确缩成 large aligned dyadic nodes；V57 随后用
   full-shell longitudinal root anchor把全部 endpoint motion搬到同一个 Gate-B row，
   所以 selected route只需一个 root estimate与一个 transverse row energy；
4. `terminal longitudinal cable`：两 row沿 `kappa_q=(q-2)/(q-1)` 的差直接等于
   physical residual加已付款误差。它必须由 direct signed scalar支付，不能被 centered
   modulus-BDH删除；V53 symmetric two-row theorem是 terminal package而非较易前置门。

Bridge A 当前状态：`OPEN`。

### 4.2 Bridge B：distinguished-seed rare-event 大桥

图像标签：`distinguished-seed genericity`。

它代表从非自治动力学的 metric/rare-event information 转移到指定算术 seed 的 exact
attachment。现有来源没有支付该 attachment。

Bridge B 当前状态：`RESERVE / OPEN_NEW_THEOREM`，不是当前第一优先级。

## 5. 上游精确路线与当前位置：V65 / TPC-212

V59 保留 V58 的 two-scalar terminal compiler，但把第二座桥墩进一步 source-facing
地正规化。对 V35/V58 Gate-B scalar写

\[
 \mathfrak C_x=
 \sum_{q\in\mathcal Q}q
 \sum_{\substack{t\ne u\\q\nmid tu}}
 \beta_x(t)w_x^{(z)}(u)K_H(u-t)u_1(u\bar t;q).
\]

令 `a^(j)=beta+i^j w`，并令 `V_Q,H^circ(a)` 表示 nonprincipal character
energy减去精确的 `(q-2)` reduced-residue diagonal。complex polarization逐项给

\[
 \mathfrak C_x=
 \frac14\sum_{j=0}^3 i^j\mathcal V_{\mathcal Q,H}^{\circ}(a^{(j)}).
\]

因此 Gate B 不再是一个含糊的“双序列相关”口号，而是四个同类型 one-sequence
prime-BDH remainders 的 signed direct sum。这个 exact retype同时锁定三条防火墙：

1. diagonal系数必须是 `q-2`，不能改成 `q-1`，也不能删掉；
2. reduced residues依赖 literal zero class，所以 ordinary translated blocks并不自动
   保持同一个 Harper-type variance；
3. all-moduli BDH cancellation不能推出 prime-only signed remainder，有限
   `R_5=1,R_6=-1` fixture精确否定这种抽取。

在 `H=x^(21/32)`、`Q=x^(1/3)` 下，block count、local scale、global scale分别是
`x^(11/32)`、`x^(127/96)`、`x^(5/3)`，而 `Q^2/H=x^(1/96)`。这恰与
Blomer--Pascadi critical cell saving `q^(-1/32)=x^(-1/96)` 对齐，形成真实的
conditional local engine；但 collective block-to-cell compiler、prime-shell signed
reassembly以及四 packet共同的 hard-shell/tail账本尚无一手定理。故 V59 是
`ROUTE_ADVANCE=YES`，不是 arithmetic advance。

### 5.1 V58 two-scalar endpoint reduction

V58 把 V57 的第二个“整排桥墩”拆开。展开 diagonal-deleted row并代入 V35
proper-factor identity，逐项 exact得到

\[
 C_*=\sum_q qC_q=\mathfrak C_x^{\rm V35}.
\]

令 \(\mathbf v=(q)_q\)、\(V_*=\sum q^2\) 与
\(\mathbf C^\perp=\mathbf C-(C_*/V_*)\mathbf v\)，则

\[
 \sum_q|C_q|^2=\frac{|C_*|^2}{V_*}+\|\mathbf C^\perp\|_2^2.
\]

第一项就是 physical endpoint读取的 V35 signed scalar core；第二项仅支付 moving
prime-shell prefixes。V35 saving `delta` 与纵向 row-loss的精确换算为

\[
 \tau_\parallel=\frac{17}{48}-2\delta.
\]

所以 `delta>1/400` 精确对应 `tau_parallel<419/1200`，而
`delta=1/96` 对应 V57 benchmark `tau_parallel=1/3`。current selected terminal
route因此是：

1. V51 full-shell mixed-plus-balanced signed Gate-A root；
2. V35 proper-factor centered signed Gate-B scalar core。

由 `S=(A_*-C_*+E_*)/K_*`，两项条件性给 strict endpoint；若还要全部 Gate-A
prefixes，才追加 `q`-transverse variance。V57 full row-Bessel仍是合法但更强的
maximal package。两个 scalar piers均未被现有一手来源证明，arithmetic status不变。

### 5.2 V56 fallback：pruned dyadic tree

V56 不再把 `sup_Y` 当作一个额外黑箱。对 prime shell按大小排序，预先分成至多
`M=floor(x^lambda)` 个模数的连续 leaves，其中 `0<lambda<19/2400`。单模数 envelope

\[
 q|P_q|\ll x^{53/32+o(1)}
\]

使每个 leaf自动保留 saving `19/2400-lambda`。完整 leaves再组成 aligned
power-of-two dyadic nodes。任一 prefix精确分解成 `O(log Q)` 个 nodes、至多一个
singleton full leaf和一个 partial leaf。因此，只要对每个至少含两个 leaves的 node
`B` 统一证明

\[
 \left|\sum_{q\in B}qP_q\right|
 \ll x^{1997/1200-\eta_D+o(1)},
\]

就得到任意
`eta_M<min(eta_D,19/2400-lambda)` 的 maximal Gate-A saving。反向每个 node是两个
prefixes之差，所以在短 leaf付款后，两种 theorem在 power scale上等价。这个 compiler
没有证明 node estimate；Lewko--Lewko 与 Ramaré只提供 inner-index maximal/dyadic
architecture，现有 fixed-modulus Kloosterman engines也没有完成 outer-`q` block
reassembly。

下面的 V43--V55 细节继续说明到达这个位置的完整上游链。

V43 把 V35 proper-factor direction 在第一次 outer absolute 之前送进 complete
centered Poisson。冻结 ordered weight 后仍有 exact diagonal

\[
\sum_{d\mid u,\ 2\le d\le x/2}\vartheta_x(d;u)=\beta(u),
\]

而 unit-centered complete alias 为

\[
\mathcal P_{q,d}(u)=\frac H{dq}
\sum_{\substack{m\ne0\\q\nmid m}}
\psi\!\left(\frac{Hm}{dq}\right)
\left(e_d(mu\bar q)+\frac1{q-1}e_{dq}(mu)\right).
\]

令 `Y0=H/(4Q)=x^(31/96+o(1))`。`d<=Y0` 时 nonzero alias 精确为空；但
physical row 删除 (u=dk)，所以 zero axis必须返回，不能计作小因子付款。完整重组给

\[
\mathfrak D_x=\mathfrak A_x-L_{\rm pr}S_x^{\rm physical}
+O\!\left(x^{53/32+o(1)}+x^{79/48+\varepsilon+o(1)}\right),
\]

以及

\[
J(r_x)=\frac{\mathfrak A_x}{L_{\rm pr}}
+O\!\left(x^{95/96+o(1)}+x^{47/48+\varepsilon+o(1)}\right),
\qquad 0<\varepsilon<\frac{11}{600}.
\]

这使 Gate B numerator 与 Gate A major scalar第一次成为同一 literal AND compiler。
V44 对第一段 transition `Y0<d<=U` 进一步写

\[
g=(|m|,d),\qquad d=gs,\qquad m=gn,
\]

从而精确消去 phase 与 cutoff 里的 `g`。reduced modulus 与 numerator 满足

\[
Q^{31/32+o(1)}\le s\le Q^{399/400+o(1)},\qquad
0<|n|\le x^{23/2400+o(1)}.
\]

在 unit residues 上，prime inverse occupancy `C_s(r)` 的 mean--centered split 给

\[
\mathfrak A_x^{\rm tr}=\mathfrak M_x^{\rm tr}+\mathfrak V_x^{\rm tr}
+O\!\left(x^{319/192+o(1)}+x^{7171/4800+o(1)}\right).
\]

V44 的两个 open endpoint gates 是

\[
\mathcal V_{\rm rec}\ll P^2x^{-\kappa+o(1)},\quad
P=x^{1/96},\quad\kappa>1/200,
\]

以及

\[
|\mathfrak M_x^{\rm tr}|\ll x^{5/3-\delta_M+o(1)},
\quad\delta_M>1/400.
\]

generic large sieve 与 principal absolute ceiling 都停在 `x^(5/3+o(1))`，恰差
`1/400`；ideal diagonal variance 给 `x^(319/192+o(1))` 与 `13/4800` margin。
V45 进一步把 character Parseval 按 primitive conductor 分层。令
`D0=P^(1/2)=x^(1/192)`。对 conductor block `d~D`，primitive second moment 与
fourth moment分别给

\[
 \mathcal V_D^{(2)}\ll P^2(D/Q+1/D)x^{o(1)},
\]

\[
 \mathcal V_D^{(4)}\ll
 \begin{cases}P^2/N,&D>N,\\P^2/D,&D\le N,
 \end{cases}
 \qquad N\asymp SQ/H.
\]

在 `D>=D0` 上取两界最小值得

\[
 \mathcal V_{\ge D_0}\ll P^{3/2}x^{o(1)},\qquad
 |\mathfrak V_{\ge D_0}^{\rm tr}|\ll x^{213/128+o(1)},
\]

其 endpoint margin 精确为 `1/9600`。低谱不是丢弃项：若 `s=de` 且 character由
primitive `chi* mod d`诱导，则 physical transform精确含

\[
 \tau(\chi^*)\chi^*(e)
 \sum_u b(u)\overline{\chi^*(u)}c_e(u),
\]

且 `mu(e)c_e(u)=mu((e,u))phi((e,u))`。所以 principal `d=1` 与
`1<d<D0` 共同形成 explicit structured major spectrum。transition 现在只剩一个门：

\[
 |\mathfrak M_{<D_0}^{\rm tr}|
 \ll x^{1997/1200-\eta_<+o(1)},\qquad \eta_<>0.
\]

因此 transition 已经从两门缩成一门，但尚未算术闭合。balanced Type II
`d>U,k>U` 与 long-Möbius reverse Type I `d>U,k<=U` 仍开放。下述 V40--V42
row/energy历史仍是 Gate B 的平行实现与损失账。

V46 不再把这唯一门留成抽象 low-character sum。定义 proper-factor local profile
`Delta_d,z=P_d-B_d,z`；由 `d|t` 得
`Delta_d,z(u-t)=Delta_d,z(u)`。于是 transition exact分成 local Euler carrier
与 AP residual。前者沿 V29 compiler得到

\[
|\mathfrak L_x^{\rm pf}|/L_{\rm pr}
\ll x^{1891/1920+o(1)}
\]

及 `121/9600` margin。后者写为 `A_d(r)` 与 residue residual的 Fourier pairing，
且

\[
\sum_{d,r}|A_d(r)|^2\ll P^2x^{o(1)}.
\]

V46 因此把 transition 的单一 theorem gate写为

\[
\sum_{\substack{Y_0<d\le U\\\mu^2(d)=1}}
d\sum_{a\bmod d}|\mathcal R_d(a)|^2
\ll xU^2x^{\rho+o(1)},\qquad 0\le\rho<33/100.
\]

V47 观察到 \(q/H<1\)，所以 active nonzero \(m\) 总满足 \(0<|m|<d\)；由此
\(A_d(0)=0\) 精确成立。令 \(\mathcal R_d^\circ\) 为 residue-centered residual，则

\[
\mathfrak R_x^{\rm AP}=-H\sum_d\sum_{r\ne0}
A_d(r)\widehat{\mathcal R_d^\circ}(r),\qquad
\sum_{r\ne0}|\widehat{\mathcal R}_d(r)|^2
=d\sum_a|\mathcal R_d^\circ(a)|^2.
\]

再以 exact local profiles定义 prime error \(\mathcal P_d\) 与 hybrid error
\(\mathcal H_d\)，有
\(\mathcal R_d^\circ=\mathcal P_d^\circ-\mathcal H_d^\circ\)。因此 current gate严格缩为

\[
\sum_{\substack{Y_0<d\le U\\\mu^2(d)=1}}d\sum_{a\bmod d}
|\mathcal P_d^\circ(a)-\mathcal H_d^\circ(a)|^2
\ll xU^2x^{\rho+o(1)},\qquad 0\le\rho<33/100.
\]

它是比 V46 full all-residue gate更弱而仍充分的 whole-object theorem，不是现有
BDH theorem的直接 corollary。V48 进一步把 V45 与 V46 对齐：令
`g=(m,D)`, `s=D/g`, `n=m/g`，phase与 cutoff exact约化到 `s`，对 `D=gs`
求和正好生成 V45 的 `lambda_s`。因此

\[
\mathfrak R_x^{\rm AP}
=\mathfrak M_{<D_0}^{\rm tr}
+\mathfrak V_{\ge D_0}^{\rm tr}
-\mathfrak L_x^{\rm pf}.
\]

high conductor与 local Euler给 paid remainder `x^(213/128+o(1))`，margin
`1/9600`。当前首选门是 direct low scalar
`x^(1997/1200-eta_low+o(1))`；更强充分门对同一 signed character tower要求
`delta>1/200`。V45/V47 energies不能相减，因为 gcd aggregation与 squaring不交换。

V49 将 V45 dyadic block bound推到更低 cut
\(D_1=x^{49/9600}\)。critical collar \(D_1\le c<D_0\) 的 coefficient energy为
\(x^{151/9600+o(1)}\)，与 old high range合并后

\[
|\mathfrak V_{\ge D_1}^{\rm tr}|
\ll x^{31951/19200+o(1)},
\qquad
\frac{1997}{1200}-\frac{31951}{19200}=\frac1{19200}.
\]

剩余 scalar为

\[
\mathfrak C_{<D_1}^{\rm ul}
=\mathfrak M_{<D_1}^{\rm tr}-\mathfrak L_x^{\rm pf}
=\mathfrak C_{\rm pr}+\mathfrak C_{\rm gen}+\mathfrak C_{\rm exc}.
\]

Landau--Page只把 exceptional primitive type限制为空或一个 quadratic character；
全部 induced cofactors仍在同一 lane。当前首选门是直接控制三个 lane的 signed sum，
separate marginal bounds只是更强 heuristic fallback。此处就是当前 `YOU ARE HERE`。

V50 不再固定只用 `D1`。对任意预先选择的
`0<delta<1/9600`，令 `D_delta=x^(1/200+2delta)`，则 coefficient energy为
`x^(19/1200-2delta+o(1))`，从而 complementary output精确是
`x^(1997/1200-delta+o(1))`。剩余 core
`C_delta=M_<D_delta-L_pf` 必须在同一 exponent上直接给 saving。

exceptional obstruction现在有一个全局二世界地图。若 primitive quadratic
Siegel-zero quality无界，Matomaki--Merikoski Corollary 1.1(i) 对 `h=2` 直接给
无限多 twin primes；若 qualities由一个有限 `B` 控制，则 Bridge A只要求一族
`forall B exists delta_B` 的 direct signed core theorems，constants允许依赖 `B`。
per-scale empty/singleton Landau--Page set不决定全局世界。bounded theorem仍 OPEN，
但它现在是 sequential route，而不是唯一入口。

V51 对 V43 ordered proper-factor atlas 作 fold-first 重编译。若
`t=s ell`、`s<ell`，两 orientations exact合成

\[
\Omega_U(s,\ell)=
\begin{cases}
(\mu(\ell)-\mu(s))\log s/\log(s\ell),&s\le U,\\
(\mu(s)\log\ell+\mu(\ell)\log s)/\log(s\ell),&s>U.
\end{cases}
\]

第一支正好把 transition short orientation 与 reverse-Type-I long orientation放回
同一个 mixed pair；第二支是 balanced two-long。numerator在每个 product-cut cell
至多 rank two，而 product log denominator由 exact Abel summation处理。补回
`u=t` 对角后的 pair row `F_q` 满足

\[
\mathcal F_q=s_q+c'_q(0)S_q,
\qquad
\mathfrak F_x=\mathfrak A_x+\text{paid errors}.
\]

非主 Dirichlet character projector再给一个保留 common prime shell、physical
`w=Lambda(.+2)-b`、hard shell和 one outer sign的 exact character--Fourier emitter。
当前首选 Gate-A theorem因此是同一个
`F_mix+F_bal` signed aggregate；square row已付到 `x^(143/96+o(1))`。
generic character large sieve只到 `x^(2+o(1))`，距 numerator target缺
`403/1200`。

V52 保留该 fold 并定义 compensated row

\[
\mathcal R_q(t)=\sum_{t+qk\in I_x}w(t+qk)K_H(qk)
-\frac1{q-1}\sum_{q\nmid u}w(u)K_H(u-t).
\]

于是 non-square aggregate exact等于

\[
\mathfrak F_x^\circ=\sum_q q\sum_{q\nmid t}\beta^\circ(t)\mathcal R_q(t).
\]

同一 coefficient 又是 truncated sieve residual，balanced semiprime slice为
`U<p<r -> beta(pr)=-1`。character packet给

\[
|\mathfrak F_x^\circ|=\varrho_{BW}\sqrt{\mathcal E_B\mathcal E_W},
\qquad
\eta_{\rm PAD}=\kappa+\frac{\delta_B+\delta_W}{2}-\frac1{400}.
\]

这里是当前 `YOU ARE HERE`：fold、compensation、natural length与 endpoint simplex
均已 exact；V52 pair-angular theorem仍作为独立 fallback，没有 arithmetic credit。

V53 定义 completed pair row

\[
A_q^\circ=\sum_{q\nmid t}\beta^\circ(t)\mathcal R_q(t),\qquad
\mathcal E_A^{\rm row}=\sum_q|A_q^\circ|^2,
\]

并把 whole scalar exact写成

\[
\mathfrak F_x^\circ=\sum_q qA_q^\circ.
\]

其 collision diagonal已由 divisor envelopes与 compensated kernel bound支付为
`x^(95/48+o(1))`。若 full row energy相对该 diagonal的损失为 `x^tau`，则

\[
|\mathfrak F_x^\circ|\ll x^{143/96+\tau/2+o(1)},
\qquad \tau<419/1200.
\]

选定 `tau=1/3` 正好只损失一个模数尺度，得到 `x^(53/32+o(1))`。V40 Gate B的
diagonal-deleted row有同一个 paid diagonal与同一 endpoint law，所以新的首选大桥是
`H_2RB(1/3,1/3)`：对 pair row和 physical row同时证明 one-`Q` Bessel bound。
V43 reassembly随后条件性给 `|S_physical|<<x^(95/96+o(1))`，严格余量
`19/2400`。V54 进一步定义 `P=(P_q)_q`、`C=(C_q)_q` 与
`kappa_q=(q-2)/(q-1)`，并 exact得到

\[
P_q-C_q=\kappa_qS_x-E_q,
\qquad \sum_q|E_q|^2\ll x^{95/48+o(1)}.
\]

所以

\[
\frac{\langle P-C,\kappa\rangle}{\|\kappa\|_2^2}
=S_x+O(x^{79/96+o(1)}),
\qquad
\Pi_\perp P-\Pi_\perp C=-\Pi_\perp E.
\]

V55 进一步逐模数证明

\[
 \frac{P_q-C_q}{\kappa_q}
 =S_x+O(x^{79/96+o(1)}),
\]

并对任意 q-space operator \(T\) 得到
\[
 T(P-C)=S_xT\kappa-TE.
\]
若 \(T\kappa=0\)，它只控制 paid transverse error；若不为零，它直接读取 terminal
physical scalar。V54 extractor \(\kappa/N_\kappa\) 在当前 L2 information model内
唯一 minimax，PSD/TT-star同样无第三种 case。

这才是当前 `YOU ARE HERE`：longitudinal cable已经分类为 terminal readout，不再是
待造 preliminary pier。真正桥墩前移到 q-compression之前的 V51 maximal fold-first
或 V52 PAD Gate A，以及 V42/common transverse Gate B。

V40 已把 packet 压到每个模数的一条 scalar row

\[
s_q=\sum_{\substack{t,u\in I_x\\t\ne u\\q\nmid tu}}
\beta(t)w(u)K_H(u-t)c'_q(u-t).
\]

V41 用 V30 的三剩余类 profile

\[
\Gamma_q(u)=
\begin{cases}
-q(q-2)/(q-1)^2,&u\equiv-2\pmod q,\\
0,&u\equiv0\pmod q,\\
q/(q-1)^2,&\text{otherwise}
\end{cases}
\]

作 exact split `s_q=m_q+\rho_q`。这里 `m_q` 把 `w(u)` 换成
`\Gamma_q(u)`，`rho_q` 保留 literal residual `w(u)-\Gamma_q(u)`；所有
`+2/-1`、Möbius/log、MASTER/H2、unit、hard shell 与 hybrid 数据仍在同一对象里。

零均值和异常剩余类 `t=-2 (mod q)` 给

\[
|m_q|\ll x^{1+o(1)}\frac H{q^2},\qquad
\sum_q|m_q|^2\ll x^{37/16+o(1)}.
\]

所以模型 scalar 已付到

\[
\left|\sum_q q m_q\right|\ll x^{53/32+o(1)},
\]

并有 strict margin `19/2400`。这是一次真正的 elementary whole-shell payment；
但它没有估计 residual。

当前 primary Gate-B theorem 精确为

\[
\mathcal E_{\rm res}:=\sum_q|\rho_q|^2
\ll x^{7/3-\kappa+o(1)},\qquad\kappa>\frac1{200},
\]

或相对 `\mathcal D_{\rm res}\ll x^{95/48+o(1)}` 的

\[
\mathcal E_{\rm res}\ll x^{\tau+o(1)}\mathcal D_{\rm res},
\qquad\tau<\frac{419}{1200}.
\]

benchmark `tau=1/3` 仍给 `37/16` 能量和 `53/32` 输出。V41 已冻结 one-outer-
absolute L2 dual与 same-index character row。

V42 进一步展开

\[
\mathcal E_{\rm res}=\mathcal D_{\rm res}+\mathcal O_{\rm res},
\]

所以最窄 primary theorem只是

\[
(\mathcal O_{\rm res})_+\ll x^{37/16+o(1)}.
\]

把 V35 identity

\[
\beta(t)=\sum_{dk=t,\ d,k\ge2}\mu(d)\omega_x(d,k)
\]

插入同一 residual后，proper-factor occurrence diagonal仍为
`x^(95/48+o(1))`。对 `O(log x)` 个 disjoint dyadic `d`-cells，若证明

\[
\sum_q|\rho_{q,j}|^2\ll Qx^{o(1)}\mathcal D_j,
\]

则 exact cell reassembly给 benchmark输出和 `19/2400` margin。另一方面，
orientation-blind operator certificate只能给 loss `N_active/#Q`；进入 endpoint要求
`N_active<=x^(273/400-o(1))`。full-active时该 loss为 `x^(2/3)`，比阈值多
`127/400`。因此当前主路必须证明 actual Möbius--prime方向的 collision；现有 local
Kloosterman engine只到单 cell，未付 block atomic budget和跨 `q` 的 L2 reassembly。
所有 row仍删除 `h=0`，所以 Gate B闭合本身不支付 terminal Gate A；V43 只证明两门
由 `D=A_alias-L_pr*S+paid errors` 精确相连，最终仍须同时给 saving。

## 5.3 V62 / TPC-209：whole-frame Poisson profile obstruction

TPC-209 是 V61 complete-graph edge frame 的直接下一站。固定 unit divisor `D` 时，
Poisson 给出 exact reindex `(k,r)->n=qr+kD`，所以同一 `D` 的所有 edge terms 共用
一个 dual lattice。恢复 divisor sum 后，dual packet 被 `U_D:b(k)->b(kD)` 置换。
完整 frame 的 cross terms 必须保留；multiplicative Fourier 只给出带
divisor-dependent profile 的 shared-character form，并由 Gauss sum exact 回到 V59。

frame-only route 的 strongest obstruction 是 sharp alignment theorem：
`||P sum_D c_D U_D B_D||` 的 direct-sum operator norm为 `||c||_2`，aligned
profiles 达到等号。`q=5, D=2,3, c_2=c_3=-1` 的 quadratic character multiplier
等于 coefficient `ell^1` mass，故不能从 frame algebra 推出 scalar collapse 或 power
saving。

```text
TPC209_ROUTE_ADVANCE = YES
TPC209_STRUCTURAL_THRESHOLD_A = PASS
TPC209_SHARED_DUAL_PER_FIXED_DIVISOR = PROVED_EXACT
TPC209_WHOLE_FRAME_VECTOR_COVARIANCE = PROVED_EXACT
TPC209_MULTIPLICATIVE_CHARACTER_DIAGONALIZATION = PROVED_EXACT
TPC209_RETURN_TO_V59_CHARACTER_INTERFACE = PROVED_EXACT
TPC209_SCALAR_COMMON_DUAL_COLLAPSE = REFUTED_SCOPED
TPC209_FRAME_ONLY_POWER_SAVING = STOP_SCOPED
TPC209_SOURCE_VALID_KLOOSTERMAN_ATTACHMENT = OPEN
TPC209_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC209_ARITHMETIC_ADVANCE = NO
TPC209_FIXED_ATOM_CREDIT = 0
TPC209_L2 = NONE
TPC209_TPC_TRIGGER = true
```

地图位置：**V62 / TPC-209 已完成 frame-only structural pier；下一块桥面是
actual Möbius/Poisson dual profiles 的 profile-aware nonprincipal-character bound，
即 TPC-210 候选。**

## 5.4 V63 / TPC-210：Poisson profile realizability and physical coupling obstruction

TPC-210 直接检验上节的最小候选。对每个 prime `q>2`，取 isolated dual nodes
`n_s=s+10qs` 与半径 `rho=1/(4q)` 的 compactly supported smooth bumps；每个 residue
class 的 dual lattice 只命中一个 node，因此有限 Schwartz/Poisson profile map 是满射。
这一步把 TPC-209 的 abstract aligned vector fixture 变成了一个 admissible profile-class
construction。

对 squarefree unit divisor family 取 `c_D=mu(D)`、`B_D=mu(D)U_D^*z`，其中 `z` 为
centered witness，则每个 output 都等于 `z`，coherent whole-frame energy 与 weighted
diagonal energy 的比值恰为 divisor count。因而 profile-aware energy 的自然对象是

```text
G_(D,E) = <P U_D B_D, P U_E B_E>,
sum_(D,E) c_D conjugate(c_E) G_(D,E).
```

这是一个真实的 `PROVED_STRUCTURAL_L1` obstruction，但 scope 必须保持在 independent
admissible profiles：TPC-210 没有证明 literal coupled TPC physical coefficient family
能实现 aligned profiles，也没有反驳该 physical family 可能存在的 cross-divisor
coupling。下一座桥不再是新的 profile norm inequality，而是对 actual coupled profiles
证明 Gram cancellation 或给出 source-valid replacement；在此之前不能宣称
prime-only fixed-saving、Gate B、`L2` 或 twin-prime progress。

```text
TPC210_ROUTE_ADVANCE = YES
TPC210_STRUCTURAL_THRESHOLD_A = PASS
TPC210_PROFILE_CLASS_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC210_ACTUAL_PHYSICAL_PROFILE_BOUND = OPEN
TPC210_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC210_ARITHMETIC_ADVANCE = NO
TPC210_FIXED_ATOM_CREDIT = 0
TPC210_L2 = NONE
```

地图位置：**V63 / TPC-210 已完成 admissible profile-class obstruction；当前桥面是
literal physical cross-divisor coupling/Gram bound，之后才回到 prime-only collective
Kloosterman reassembly。**

## 5.5 V64 / TPC-211：product-coupled profiles and the truncated-boundary handoff

TPC-211 直接把 TPC-210 的 independent profile-class question 换成 V46 literal
product-coupled profiles。对 active primes `p>z`，令

```text
P_S = product_(p in S) F_p
B_S = product_(p in S) G_(p,z)
Delta_S = P_S - B_S
```

共同 CRT lift 后，product cocycle、zero-axis、zero-mean 与 full rank `2^s-1` 都是
exact。完整 Boolean packet 的 `mu(d) log(d)` sum 精确压缩为 marked-prime Euler
derivative，且 active prime 数至少为 2 时 product-frozen common endpoint 取消。

但 finite Gram duality 同时给出 `<w,Delta_S>=mu(d_S)` 的 shared endpoint，因此
product coupling、finite rank、common endpoint 不能单独支付 saving。这不是 actual
`Lambda(u+2)-b_x^(z)(u)` 的 arithmetic counterexample。

实际 transition 使用

```text
A_(Y,U)(t) = {d : d|t, Y0<d<=U, mu^2(d)=1}
```

并让每个 divisor 带有不同的 reciprocal emitter `A_d(r)`。所以完整 packet derivative
与实际 scalar 之间存在一个真实的 boundary-plus-emitter operator；TPC-212 的最小
问题是先精确构造并攻击这个 operator，再决定是否回到 prime-only collective BDH。

```text
TPC211_ROUTE_ADVANCE = YES
TPC211_STRUCTURAL_THRESHOLD_A = PASS
TPC211_PRODUCT_COUPLING_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC211_TRANSITION_BOUNDARY_CONTROL = OPEN
TPC211_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN
TPC211_ARITHMETIC_ADVANCE = NO
TPC211_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V64 / TPC-211 已完成 literal product-coupled structural audit；当前桥面
是 truncated divisor-band boundary 与 reciprocal-emitter coupling，之后才回到
prime-only collective Kloosterman reassembly。**

## 5.6 V65 / TPC-212：truncated boundary and reciprocal-emitter obstruction

TPC-212 直接处理上节留下的 actual transition band，而不是继续使用完整 Boolean packet
derivative 作为物理 bound。对 selected squarefree subset family `A`，endpoint coefficient
是

```text
L(A) = sum_p eta_p(A) log(p),
eta_p(A) = sum_(S in A, p in S) (-1)^|S|.
```

完整 packet 在至少两个 active primes 时逐 prime incidence 为零；cut packet 则精确等于
complete packet 减去 missing-subset boundary。`t=35`, `5<d<=35` 的 literal cut 选择
`{7,35}`，给出 `eta=(1,0)` 与 endpoint leakage `log(5)`，所以 boundary 不是记号上的
小 remainder。

对 finite reciprocal occupancy

```text
(E_d a)(r) = sum_(q,m) a(q,m) 1_(r=m q^(-1) mod d),
```

平方范数 exact 等于 collision condition `d | m1*q2-m2*q1` 的 weighted pair sum。
在按 divisor 分块的 natural direct sum 中，emitter Gram block diagonal 且 nonzero rows
full rank；unit-weight aligned fixtures 达到 coherent-to-diagonal ratios `2,4,3`。
这只 refute 了 cut/emitter interface alone 的 universal saving，不是 literal physical
residual 的反例。

```text
TPC212_ROUTE_ADVANCE = YES
TPC212_STRUCTURAL_THRESHOLD_A = PASS
TPC212_CUT_ENDPOINT_LEAKAGE = PROVED_EXACT
TPC212_BOUNDARY_DECOMPOSITION = PROVED_EXACT
TPC212_RECIPROCAL_COLLISION = PROVED_EXACT_FINITE
TPC212_EMITTER_GRAM = PROVED_EXACT_BLOCK_DIAGONAL
TPC212_EMITTER_ONLY_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC212_LITERAL_PHYSICAL_BOUNDARY_BOUND = OPEN
TPC212_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN
TPC212_ARITHMETIC_ADVANCE = NO
TPC212_FIXED_ATOM_CREDIT = 0
TPC212_L2 = NONE
TPC212_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V65 / TPC-212 已完成 boundary/emitter structural audit；下一座桥是把
literal V46 profile coupling 映射到 emitter blocks，并在任何 direct-sum Cauchy 或 outer
absolute 之前证明 physical cross-divisor Gram bound。**

## 5.7 V66 / TPC-213：physical profile pullback and the cross-divisor Gram

TPC-213 把上节留下的 coupling question 变成一个 exact common-source operator。对有限
physical support `U`、residue lift `C_d`、divisor correction `b_d` 与 emitter pullback
`K_d`，有

```text
R_d = C_d(v-b_d),
sum_d sum_r A_d(r) F_d R_d(r)
  = sum_u v(u) K(u) - sum_d sum_u b_d(u) K_d(u),
K(u)=sum_d K_d(u).
```

在 complete `lcm(d,e)` period 上，CRT 给出

```text
(C_d C_e^*)(a,b) = (L/lcm(d,e)) 1_(a=b mod gcd(d,e)),
```

而 emitter pullback 的 Hermitian Gram 精确等于 shared rational frequencies
`r/d = s/e (mod 1)` 的加权交叠。fixture `d={5,7,35}`、`q={11,13,17}`、`H=40`、
`U={0,...,34}` 的 joint lift rank 为 `35`，cross-Gram 为 `0,560,770`。

```text
TPC213_ROUTE_ADVANCE = YES
TPC213_STRUCTURAL_THRESHOLD_A = PASS
TPC213_PHYSICAL_PROFILE_EMITTER_PULLBACK = PROVED_EXACT
TPC213_RESIDUE_LIFT_GCD_ALIASING = PROVED_EXACT
TPC213_CROSS_DIVISOR_FREQUENCY_GRAM = PROVED_EXACT_FINITE
TPC213_PHYSICAL_DIRECT_SUM_REPLACEMENT = REFUTED_SCOPED
TPC213_LITERAL_V46_ASYMPTOTIC_GRAM_BOUND = OPEN
TPC213_PRIME_SHELL_REASSEMBLY = OPEN
TPC213_ARITHMETIC_ADVANCE = NO
TPC213_FIXED_ATOM_CREDIT = 0
TPC213_L2 = NONE
TPC213_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V66 / TPC-213 已完成 common-source physical coupling construction；下一座
桥是对 shared rational-frequency clusters 保留 smooth `psi`、`mu(d)log(d)/d`、
four-packet signs、zero-axis 与 prime shell，证明 signed cancellation 或更强的
positive-Gram obstruction。**

## 5.8 V67 / TPC-214：Möbius-weighted shared-frequency clusters

TPC-214 完成了上节指定的最小 structural theorem。对

```text
B_d(r) = sum_(q,m) psi(Hm/(dq)) 1_(m q^(-1)=r mod d),
c_d = mu(d) log(d)/d,
```

保留 literal integer cutoff 后，`h|d` 给出 exact
`B_d((d/h)a)=B_h(a)`。因此在 `L=lcm(D)` 的完整 physical period 上，所有相同
reduced rational frequencies 先合并为
`C_h=sum_(d in D:h|d)c_d`，再由 complete-period orthogonality 得到 exact
reduced-denominator cluster factorization。`max(Q)<H` 时 additive zero axis exact
消失；four-packet polarization 在 cluster reduction 后仍保持 exact linearity。

有限 certificate 使用 `Q={11,13,17}`、`H=40`、
`psi(t)=(1+t^2)^(-2)`。`{5,7,35}` 的 exact cross-energy sign 为负，
`{3,5,7,105}` 的 exact sign 为正；对应物理/直和数值比约为
`0.5963435557` 与 `1.2119952513`。因此下一步不能预设 cluster saving sign，
而应直接估计实际 V46 transition band 中的 Möbius-log tails。

```text
TPC214_ROUTE_ADVANCE = YES
TPC214_STRUCTURAL_THRESHOLD_A = PASS
TPC214_EMITTER_DILATION_COVARIANCE = PROVED_EXACT
TPC214_REDUCED_DENOMINATOR_CLUSTER_FACTOR = PROVED_EXACT
TPC214_ZERO_AXIS_SCOPE = PROVED_EXACT
TPC214_FOUR_PACKET_POLARIZATION = PROVED_EXACT_LINEAR_EXTENSION
TPC214_NESTED_CLUSTER_CANCELLATION = PROVED_EXACT_FINITE_SIGN
TPC214_COMPOSITE_QUOTIENT_ENHANCEMENT = PROVED_EXACT_FINITE_SIGN
TPC214_FINITE_ENERGY_RATIOS = NUMERICAL_OBSERVATION
TPC214_UNIVERSAL_CLUSTER_SAVING_SIGN = REFUTED_SCOPED
TPC214_LITERAL_V46_ASYMPTOTIC_CLUSTER_BOUND = OPEN
TPC214_PRIME_SHELL_REASSEMBLY = OPEN
TPC214_ARITHMETIC_ADVANCE = NO
TPC214_FIXED_ATOM_CREDIT = 0
TPC214_L2 = NONE
TPC214_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V67 / TPC-214 已把 shared-frequency coupling 压缩为 Möbius-log
reduced-denominator tails；下一座桥是对这些 tails 做 literal V46 uniform bound，
然后再进行 prime-shell 与 four-packet reassembly。**

## 5.9 V68 / TPC-215：short-quotient Möbius tails and the no-power-loss majorant

TPC-215 完成了上节指定的最小 tail theorem。对 V46
`H=x^(21/32)`, `Q=x^(1/3)`, `Y0=H/(4Q)`, `U=x^(133/400)` 与
`q<=2Q`，若 `B_h` 非零，则整数 cutoff 给出

```text
h >= H/q_max >= H/(2Q) = 2Y0.
```

因此 `h` 自身是完整 transition band 中的 squarefree divisor。写 `d=hk` 后，
`C_h` 成为 exact short-quotient Möbius sum，且

```text
k <= Uq_max/H <= 2UQ/H = 2x^(23/2400+o(1)).
```

`d=h` 使 `D_h=sum_(h|d)|c_d|^2` 有精确对角锚点；harmonic triangle 给出
`|C_h|^2<=A_xD_h`，并且 `A_x=O((log x)^2)=x^(o(1))`。TPC-214 的 cluster
factorization 加上 exact reduced-fraction row partition 后得到

```text
E_cluster <= O((log x)^2) E_direct.
```

有限 fixture `Q={11,13,17}`, `H=40`, `Y0=2`, `U=35` 有 14 个 active rows、7 个
top-shell rows，producer/independent/optimized/sanity/checker 全部通过。有限 global
ratio `0.5969532588` 只作 numerical observation。top-shell rows 的 coefficient ratio
是 exact `1`，所以没有 uniform rowwise fixed-power saving。

```text
TPC215_ROUTE_ADVANCE = YES
TPC215_STRUCTURAL_THRESHOLD_A = PASS
TPC215_ACTIVATION_FLOOR = PROVED_EXACT
TPC215_SHORT_QUOTIENT_NORMAL_FORM = PROVED_EXACT
TPC215_QUOTIENT_LENGTH_EXPONENT = PROVED_23_OVER_2400
TPC215_ROW_NORM_DIVISOR_DECOMPOSITION = PROVED_EXACT
TPC215_CLUSTER_TO_DIRECT_MAJORANT = PROVED_O_LOG_X_SQUARED
TPC215_FIXED_POWER_CLUSTER_AMPLIFICATION = EXCLUDED
TPC215_TOP_SHELL_RATIO_ONE = PROVED_EXACT
TPC215_UNIFORM_ROWWISE_POWER_SAVING = REFUTED_SCOPED
TPC215_FINITE_RATIOS = NUMERICAL_OBSERVATION
TPC215_DIRECT_SUM_ARITHMETIC_ENERGY_BOUND = OPEN
TPC215_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN
TPC215_PRIME_SHELL_REASSEMBLY = OPEN
TPC215_ARITHMETIC_ADVANCE = NO
TPC215_FIXED_ATOM_CREDIT = 0
TPC215_L2 = NONE
TPC215_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V68 / TPC-215 已把 literal shared-frequency cluster 的潜在固定幂放大
压到 `x^(o(1))`；下一座大桥不是再估计 `C_h`，而是控制 source-locked direct-sum
physical row energy，并在 finite window 中重新支付 off-frequency 与 prime-shell/
four-packet reassembly。**

## 5.10 V69 / TPC-216：direct-sum row-energy envelope and the Cauchy bottleneck

TPC-216 完成了上节指定的 direct-sum envelope。保持同一个 literal V46 emitter，令
`B_d=sum_q B_(d,q)`。source exponents 给出

```text
H/(4Q)=x^(31/96)/4 -> infinity,
U/Q=x^(-1/1200) -> 0,
```

所以充分大 `x` 时 `4Q<H` 与 `U<Q` 同时成立。对 fixed `d,q`，cutoff integers
在模 `d` 下不碰撞，故

```text
||B_(d,q)||_2^2 <= 2||psi||_infty^2*dq/H.
```

一次 shell Cauchy 与 elementary `P<=2Q` 给出

```text
||B_d||_2^2 <= 4||psi||_infty^2*P^2*dQ/H
             <= 16||psi||_infty^2*dQ^3/H.
```

加上 `|c_d|^2=mu(d)^2(log d)^2/d^2` 的 divisor sum，得到

```text
L^(-1)E_direct <<_psi (Q^3/H)(log U)^3
                    = x^(11/32)(log x)^3.
```

这是真正的 complete-period normalized direct-sum envelope，但没有使用 Möbius
cancellation、PNT 或 prime-shell cancellation。exact rational adversary 取
`d=5`, `H=500`, `q={101,131,151,181}` 与 `psi(t)=(1+t^2)^(-2)`；四个 fixed-q
rows 都支撑在 `{1,4}`，combined/direct norm ratio 约为 `3.70568607565`。因此
free q-orthogonality 被 `REFUTED_SCOPED`，但该 fixture 不是 V46 asymptotic lower
bound。

```text
TPC216_ROUTE_ADVANCE = YES
TPC216_STRUCTURAL_THRESHOLD_A = PASS
TPC216_FIXED_Q_NO_COLLISION = PROVED_EXACT
TPC216_FIXED_Q_ROW_ENERGY = PROVED_EXACT
TPC216_SHELL_CAUCHY_ENVELOPE = PROVED_EXACT
TPC216_PRIME_SHELL_CARDINALITY = PROVED_P_LE_2Q
TPC216_NORMALIZED_EXPONENT = PROVED_11_OVER_32
TPC216_DIRECT_SUM_ROW_ENERGY_ENVELOPE = PROVED_X_11_OVER_32_LOG_CUBED
TPC216_ARITHMETIC_CANCELLATION = NONE
TPC216_ALIGNED_SUPPORT_ADVERSARY = NUMERICALLY_CERTIFIED_EXACT_RATIONAL
TPC216_FREE_Q_ORTHOGONALITY = REFUTED_SCOPED
TPC216_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN
TPC216_PRIME_SHELL_REASSEMBLY = OPEN
TPC216_FULL_GATE_B = OPEN
TPC216_ARITHMETIC_ADVANCE = NO
TPC216_FIXED_ATOM_CREDIT = 0
TPC216_L2 = NONE
TPC216_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V69 / TPC-216 已把 source-locked complete-period direct-sum row energy
压到 `x^(11/32)(log x)^3` 的结构性 envelope；下一座桥是把这个 envelope 接到
literal finite window，并保留 shell alignment、Möbius signs 与 four-packet
reassembly。**

## 5.11 V70 / TPC-217：finite-window attachment by reduced rational-frequency large sieve

TPC-217 完成了上节指定的 finite-window attachment。对同一个 literal common-source
kernel，按 `r/d` 的 reduced rational frequency 精确重组；不同分母不超过 `U` 的
reduced fractions 具有 Farey spacing `delta>=U^(-2)`。因此 standard additive large
sieve 在 `I_x=(x/2,x]` 上给出

```text
sum_(n in I_x)|K(n)|^2
  <= (N+U^2) S_cluster,
S_cluster <= O((log x)^2) E_direct/L,
E_direct/L <<_psi x^(11/32)(log x)^3.
```

由于 `U^2/x=x^(-67/200)`，得到 normalized finite-window bound
`N^(-1)sum_(n in I_x)|K(n)|^2 <<_psi x^(11/32)(log x)^5`，unnormalized exponent
为 `43/32+o(1)`。这控制了 physical interval 的 off-frequency Gram，但不替换
literal prime rows，不使用 PNT、Möbius cancellation 或 four-packet arithmetic
cancellation。

有限 certificate 覆盖 14 个 active divisors、16 个 reduced denominators 与 3 个
translated windows；aligned one-point fixture 的 exact coherent-to-diagonal ratio
为 `2`，所以 free finite-window orthogonality 仍被 `REFUTED_SCOPED`。

```text
TPC217_ROUTE_ADVANCE = YES
TPC217_STRUCTURAL_THRESHOLD_A = PASS
TPC217_REDUCED_FREQUENCY_REGROUPING = PROVED_EXACT
TPC217_FAREY_SPACING = PROVED_EXACT
TPC217_ADDITIVE_LARGE_SIEVE = PROVED_STANDARD
TPC217_FINITE_WINDOW_ATTACHMENT = PROVED_X_11_OVER_32_LOG_FIVE_NORMALIZED
TPC217_UNNORMALIZED_WINDOW_EXPONENT = PROVED_43_OVER_32
TPC217_WINDOW_LOSS = PROVED_1_PLUS_U2_OVER_N
TPC217_FINITE_WINDOW_OFF_FREQUENCY_GRAM = CONTROLLED_BY_LARGE_SIEVE
TPC217_ALIGNED_ONE_POINT_ORTHOGONALITY = REFUTED_SCOPED
TPC217_PRIME_SHELL_REASSEMBLY = OPEN
TPC217_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC217_ARITHMETIC_CANCELLATION = NONE
TPC217_ARITHMETIC_ADVANCE = NO
TPC217_FIXED_ATOM_CREDIT = 0
TPC217_L2 = NONE
TPC217_FULL_GATE_B = OPEN
TPC217_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V70 / TPC-217 已把 TPC-216 的 complete-period envelope 接到 literal
finite window；下一座桥是保留这份 large-sieve attachment，同时重新引入 literal
prime-shell 与 four-packet signed reassembly。**

## 5.26 V85 / TPC-232：subcritical growing-resonance-depth obstruction

For the TPC-226 modeled clock `h=4LQ`, every collision for `L<Q/4` has exact
opposite-sign one-wrap form

```text
ar+bp=4LQ,  1<=a,b<2L,  gcd(a,b)=1.
```

For fixed `a,b`, the prime solutions are two affine forms with determinant `4LQ` on
an interval of length `O(Q/max(a,b)+1)`.  Separating grazing intervals shorter than
`Q^(1/2)` from the Selberg branch makes the sieve coefficient-uniform.  Together with

```text
sum_(a,b<2L) 1/max(a,b) < 4L,
```

this proves, uniformly for `L<=(log Q)^A`,

```text
C_L(Q) <<_A LQ loglog(3LQ)/(log Q)^2.
```

Hence `L=o(log Q/loglog Q)` gives `C_L/P->0`; TPC-230's unmatched-mass floor rules
out every fixed saving under fixed row-mass comparability throughout this range.

```text
TPC232_GROWING_COLLISION_NORMAL_FORM = PROVED_EXACT
TPC232_UNIFORM_POLYLOG_DEPTH_SIEVE = PROVED_SOURCE_BACKED
TPC232_COLLISION_INCIDENCE_BOUND = PROVED_ASYMPTOTIC
TPC232_SUBCRITICAL_DEPTH_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC232_SUBCRITICAL_FIXED_SAVING = STOP_SCOPED
TPC232_CRITICAL_DEPTH_SUFFICIENCY = OPEN
TPC232_DILATED_CLOCK = MODELING_CHOICE
TPC232_ACTUAL_V59_CLOCK_ATTACHMENT = OPEN
TPC232_ARITHMETIC_ADVANCE = NO
TPC232_ARITHMETIC_OBSTRUCTION = PROVED_SOURCE_BACKED
TPC232_FIXED_ATOM_CREDIT = 0
TPC232_L2 = NONE
TPC232_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
```

地图位置：**V85 / TPC-232 closes every subcritical growing-depth model covered by the
uniform sieve.  The shortest next move is a critical-depth row-mass/degree audit,
followed by the actual V59 source-to-row attachment; the theorem is not a critical
lower bound and not a full Gate-B no-go.**

## 5.25 V84 / TPC-231：finite-resonance sieve obstruction

For `Q=3t+a`, the first primitive resonance has exact parameterization

```text
p=3k+a, r=16t+3a-7k, determinant=16Q.
```

The local bad-residue count is one at `2,3,7` and primes dividing `Q`, and two
otherwise. The classical dimension-two Selberg upper-bound sieve therefore proves

```text
E_3716(Q) << Q log log(3Q)/(log Q)^2,
E_3716(Q)/P(Q) -> 0.
```

The determinant argument applies to every fixed finite primitive nondegenerate linear
resonance family. Such a family has bounded graph degree; for bounded collision
coefficients and row-mass ratio `kappa`, Cauchy--Schwarz gives

```text
(D-E_AP)_+/D <= 2 C Delta kappa E_total/P = o(1).
```

Together with TPC-230, literal first-resonance matched mass also has `M/D->0`.

```text
TPC231_3716_PARAMETERIZATION = PROVED_EXACT
TPC231_3716_LOCAL_ROOT_LAW = PROVED_EXACT
TPC231_3716_SELBERG_UPPER_BOUND = PROVED_SOURCE_BACKED
TPC231_3716_EDGE_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC231_FIXED_FINITE_RESONANCE_SUPPORT_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC231_FIRST_PRIMITIVE_3_7_FIXED_SAVING = STOP_SCOPED
TPC231_FIXED_FINITE_RESONANCE_COMPARABLE_ROW_ROUTE = STOP_SCOPED
TPC231_GROWING_RESONANCE_DEPTH = OPEN
TPC231_ACTUAL_V59_SOURCE_MASS_CROSSWALK = OPEN
TPC231_ARITHMETIC_ADVANCE = NO
TPC231_ARITHMETIC_OBSTRUCTION = PROVED_SOURCE_BACKED
TPC231_FIXED_ATOM_CREDIT = 0
TPC231_L2 = NONE
TPC231_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
```

地图位置：**V84 / TPC-231 has asymptotically closed the first-resonance and fixed-finite
comparable-row branches. 下一条最短大路是 test growing resonance depth, or return to the
actual V59 source-mass crosswalk；不能把 finite-family obstruction 外推成 full Gate-B
no-go。**

## 5.24 V83 / TPC-230：matched-resonance mass ceiling

For total diagonal mass `D` and matched mass `M`, exact matching decomposition gives

```text
E_AP>=D-M, global saving<=M.
```

This is sharp under edgewise anti-alignment. With row-mass ratio `kappa`,
`M/D<=2*kappa*E/P`; literal aligned rows have `kappa<=4`, so strict `1/400` requires
`E/P>=1/3200`.

```text
TPC230_MATCHED_MASS_SAVING_CEILING = PROVED_EXACT_SHARP
TPC230_COMPARABLE_ROW_DENSITY_TOLL = PROVED_EXACT
TPC230_LITERAL_ALIGNED_KAPPA_LE_4 = PROVED_EXACT
TPC230_STRICT_1_OVER_400_EDGE_DENSITY_TOLL = 1/3200
TPC230_ASYMPTOTIC_RESONANCE_EDGE_DENSITY = RESOLVED_BY_TPC231_ZERO
TPC230_ARITHMETIC_ADVANCE = NO
TPC230_FIXED_ATOM_CREDIT = 0
TPC230_L2 = NONE
TPC230_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V83 / TPC-230 has converted fixed saving into a concrete resonance-density
toll. 下一条最短大路是 two-linear-form upper-bound sieve；若 `E/P->0`，first-resonance
mechanism 在 comparable rows 上将被 asymptotically stop-scoped。**

## 5.23 V82 / TPC-229：primitive resonance matching spectrum

Every resonance edge satisfies `10Q/7<p<8Q/5<r<2Q`, so low/high endpoint sets are
disjoint and each endpoint has a unique partner. Hence every graph is a matching. Each
edge swap block has spectrum `(-1,-1,+1,+1)` and exact ledger

```text
E_diag=E_sym+E_anti, E_collision=E_sym-E_anti, E_AP=2E_sym.
```

Thus `delta` saving iff `(1+delta)E_sym<=(1-delta)E_anti`. The source bilinear block has
a sharp half-mass bound. 4089-scale replay checks 13,754 edges and degree one.

```text
TPC229_RESONANCE_GRAPH_MATCHING = PROVED_EXACT
TPC229_EDGE_SPECTRUM = PROVED_EXACT
TPC229_GLOBAL_BLOCK_DIRECT_SUM = PROVED_EXACT
TPC229_DELTA_SAVING_CRITERION = PROVED_EXACT
TPC229_ARITHMETIC_ANTISYMMETRIC_DOMINANCE = OPEN
TPC229_ARITHMETIC_ADVANCE = NO
TPC229_FIXED_ATOM_CREDIT = 0
TPC229_L2 = NONE
TPC229_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V82 / TPC-229 已删除 graph complexity；下一条最短大路是 quantify matched
source mass。若 matching 只承载 vanishing diagonal fraction，逐边完美 cancellation
也不能给 fixed global saving。**

## 5.22 V81 / TPC-228：source-native polarized collision compiler

For common-profile rows `W_q^(j)=U_q+i^jV_q`, TPC-228 proves

```text
1/4 sum_j i^j(E_AP^(j)-E_diag^(j))=sum_(q!=r)<U_q,V_r>.
```

Q25 first `3--7` resonance is the explicit four-term beta-w block over residues
`119,281 mod 400`. Exact controls realize positive, negative, zero, directed and
single-coordinate values. Hence geometry does not choose the source sign, but the
missing arithmetic scalar is now literal and labelled.

```text
TPC228_POLARIZED_AP_MINUS_DIAGONAL_COMPILER = PROVED_EXACT
TPC228_SOURCE_LABELLED_COLLISION_SUM = PROVED_EXACT
TPC228_Q25_3_7_SOURCE_BLOCK = PROVED_EXACT_FINITE
TPC228_ACTUAL_V59_TO_PRIMITIVE_ATOM_CROSSWALK = OPEN
TPC228_ARITHMETIC_SIGN_THEOREM = OPEN
TPC228_ARITHMETIC_ADVANCE = NO
TPC228_FIXED_ATOM_CREDIT = 0
TPC228_L2 = NONE
TPC228_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V81 / TPC-228 已完成正确 source axis 上的 collision compiler；下一条最短
大路是证明 `3--7` resonance graph 的 exact block decomposition，并把 signed source
correlation 缩成 sharp local criterion。**

## 5.21 V80 / TPC-227：packet/profile axis separation

TPC-227 source-lock V59 exact polarization：四相位在 source packets
`a^(j)=beta+i^j w` 上，四个 quadratic functionals 共享一个 `psi_+` transform。对 physical
`T` 与 proposed packet-dependent `T_j`，four-point operator DFT 证明

```text
1/4 sum_j i^j ||T_j(x+i^j y)||^2 = <Tx,Ty> for every x,y
iff T_j^*T_j=T^*T for j=0,1,2,3.
```

global packet signs 不改变 Gram，因而不能制造 squared-energy sign；row-dependent
profile signs 则可改变 collision cross-Gram。TPC-226 `Q=25`, `(37,47)` first-resonance
block 的 aligned/odd maps 为 `(1,1)/400` 与 `(1,-1)/400`，off-diagonal Gram mismatch
exact 是 `-1/80000`。

```text
TPC227_V59_PACKET_AXIS = SOURCE_LOCKED
TPC227_V59_PROFILE_AXIS = SOURCE_LOCKED_COMMON
TPC227_FOUR_GRAM_CRITERION = PROVED_EXACT
TPC227_GLOBAL_PACKET_PHASE_VISIBILITY = GRAM_INVISIBLE
TPC227_Q25_ROW_SIGN_GRAM_MISMATCH = PROVED_EXACT
TPC227_TPC226_AUTOMATIC_SOURCE_TRANSFER = REFUTED_SCOPED
TPC227_SOURCE_NATIVE_COMMON_PROFILE_COMPILER = OPEN
TPC227_ARITHMETIC_ADVANCE = NO
TPC227_FIXED_ATOM_CREDIT = 0
TPC227_L2 = NONE
TPC227_FULL_GATE_B = OPEN
TPC227_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC227_ROUND2_CLUE = KEEP_THE_V59_PACKET_PHASE_ON_THE_SOURCE_SEQUENCE_AND_THE_POISSON_PROFILE_COMMON
```

地图位置：**V80 / TPC-227 已封住“把 finite profile sign 自动改名为 V59 packet phase”
的 typed shortcut。下一条最短大路是保持 common `psi_+`，把 literal coefficient packets
直接穿过 prime/AP collision representation，并识别真实 `3--7` source correlation。**

## 5.20 V79 / TPC-226：first primitive-collision transition

TPC-226 沿 TPC-225 的最小大路测试 finite dilations
`h_L=4LQ`, `L=1,2,3,4`，并保留 literal primitive condition。collision congruence、
cutoff 与 parity sieve 精确证明

```text
L=1,2,3: no legitimate cross-prime collision;
L=4: every collision is 7p+3r=16Q with multipliers (3,-7),
```

差 exchange 与 simultaneous sign change。`Q=25`, `(p,r)=(37,47)` 是 first exact
census witness，共享 residues 为 `{119,281} mod 400`。一个关键 source firewall 是：
若错误删除 primitivity，则 `Q=8,L=3,m=4` 会制造假碰撞；严格 primitive row 会把它
排除。

对每个 legitimate `3--7` resonance，signed cross-term formula 显示：aligned 与
inherited affine profiles 给正 correction，balanced odd-sign profiles 给负 correction，
并且后者有 `E_pol=E_all=0`。完整 `Q=8..512` classification 覆盖 505 scales，
发现 182 个 L4 collision-bearing scales 与 235 个 resonances；30 个 exact profile
records 独立复现。

```text
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
TPC226_ARITHMETIC_ADVANCE = NO
TPC226_FIXED_ATOM_CREDIT = 0
TPC226_L2 = NONE
TPC226_FULL_GATE_B = OPEN
TPC226_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC226_ROUND2_CLUE = SOURCE_LOCK_THE_SIGN_OF_THE_3_7_RESONANCE_BEFORE_ANY_UNIFORM_AP_SAVING
```

地图位置：**V79 / TPC-226 已跨过“nontrivial-cutoff 是否产生合法 overlap”的几何桥墩，
并把全部第一碰撞压成一个 `3--7` resonance family。下一条最短大路不再扩张 clock
geometry，而是把 V46 actual source profile 接入并判定这条 resonance 的 signed
correlation。**

## 5.19 V78 / TPC-225：cutoff-one shared-clock obstruction

TPC-225 审计 TPC-224 source-surrogate clock
`x=Q^3,H=4Q^2,h=4Q,Q<q<=2Q`。对 TPC-220 literal row rule，

```text
floor(hq/H)=floor(q/Q)=1,
support(W_(q,j)) subset {q^(-1),-q^(-1)} mod 4Q.
```

若 distinct active primes 的 supports 相交，则
`q_2=+/-q_1 mod 4Q`。正号由 shell width 强迫 prime equality；负号由
`2Q<q_1+q_2<=4Q` 强迫 `q_1=q_2=2Q`，与 primality 矛盾。
所以 active Hilbert support 是 prime-labelled orthogonal direct sum，且对任意 finite
profile values exact

```text
E_AP  = E_diag
E_all = E_pol.
```

因此当 diagonal energy 非零时，`E_AP<=(1-delta)E_diag` 的任何
`delta>0` 都失败。aligned profile 给 `E_pol/E_diag=4`；
balanced profile 给 `E_pol=E_all=0` 但 `E_AP=E_diag>0`，
说明 packet direction 可变化而 AP direction 在 cutoff-one regime 中刚性不变。

```text
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
TPC225_ROUND2_CLUE = MOVE_TO_NONTRIVIAL_CUTOFF_CLOCK_BEFORE_CLAIMING_AP_DISPERSION
```

地图位置：**V78 / TPC-225 把 TPC-224 的 shared-clock marginal question 精确分叉：
当前 named cutoff-one clock 的 AP lane 已 theorem-level stop-scoped；下一条最短大路是
source-locked nontrivial-cutoff clock 的 collision audit，而不是把 finite block
orthogonality 误称为 arithmetic cancellation。**

## 5.18 V77 / TPC-224：literal two-channel compatibility audit

TPC-224 直接审计 TPC-223 的共同 literal interface。对同一组 prime-label/packet-label
vectors `W_(q,j)`，定义

```text
E_AP  = sum_j ||sum_q W_(q,j)||^2
E_pol = sum_q ||sum_j W_(q,j)||^2
E_all = ||sum_(q,j) W_(q,j)||^2.
```

逐方向 Cauchy 与 exact scalar minimization 给出

```text
E_all <= min(J E_AP, P E_pol)
      <= PJ/(P+J) (E_AP+E_pol).
```

`PJ/(P+J)` exact sharp，所有 vectors 对齐时达到。更重要的是，本篇把这个接口写回
TPC-220 的 literal row rule、共同 `C_h=1/h` normalization 与 actual prime labels，
而不是引入两个互不相干的 surrogate objects。九个 source-surrogate scales 和五个
独立 collision-stress scales 都用 exact rational arithmetic；后者在
`H=5Q, h=5, q=1 (mod 5)` 下五个尺度均达到 sharp factor，因而 scoped-refute
unit-factor shortcut。两个 finite clocks 是分别命名的 audit，不作渐近拼接。

```text
TPC224_COMMON_LITERAL_HILBERT_INTERFACE = PROVED_EXACT
TPC224_SHARP_ADDITIVE_CONSTANT = PROVED_EXACT
TPC224_UNIT_INTERFACE = REFUTED_SCOPED
TPC224_SOURCE_CLOCK_AUDIT = NUMERICALLY_CERTIFIED_EXACT_RATIONAL
TPC224_AP_DISPERSION = OPEN
TPC224_POLARIZED_CROSS_CORRELATION = OPEN
TPC224_LITERAL_V46_TRANSFER = OPEN
TPC224_ARITHMETIC_ADVANCE = NO
TPC224_FIXED_ATOM_CREDIT = 0
TPC224_L2 = NONE
TPC224_FULL_GATE_B = OPEN
TPC224_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V77 / TPC-224 已把“共同 literal interface”从 TPC-223 的条件输入提升为
exact structural theorem，同时用 congruence-aligned stress family 否定 unit-factor
捷径；下一座真正的桥是把 AP dispersion 与 polarized cross-correlation 在同一 V46
clock 上同时证明或反驳。**

## 5.17 V76 / TPC-223：conditional signed-reassembly compiler

TPC-223 把 TPC-220 的 prime-AP/collision channel 与 TPC-222 的 polarized four-packet
channel 接入同一个 conditional interface：

```text
A_x << x^(E0-delta_AP+o(1))
P_x << x^(E0-kappa_pol+o(1))
S_x << x^lambda_struct (A_x+P_x)
```

在这三条输入下，exact algebraic compiler 给出

```text
sigma = min(delta_AP,kappa_pol)-lambda_struct.
```

严格 endpoint 条件是 `sigma>1/400`。`E0=5/3` 的 canonical rational fixture 给出
effective saving `11/1200`、strict margin `1/150`、compiled exponent `663/400`；
certificate 还拒绝 borderline、zero-channel 与 loss-dominated ledgers。三条输入均
是 `OPEN_CONDITIONAL_INPUT`，所以本篇是 conditional theorem，不是 arithmetic L2。

```text
TPC223_TWO_CHANNEL_COMPILER = PROVED_CONDITIONAL_ALGEBRA
TPC223_AP_DISPERSION = OPEN_CONDITIONAL_INPUT
TPC223_POLARIZED_CROSS_CORRELATION = OPEN_CONDITIONAL_INPUT
TPC223_LITERAL_REASSEMBLY_INTERFACE = OPEN_CONDITIONAL_INPUT
TPC223_EFFECTIVE_SAVING = CERTIFIED_EXACT_MIN_MINUS_LOSS
TPC223_STRICT_1_OVER_400 = CONDITIONAL_ONLY
TPC223_ARITHMETIC_ADVANCE = NO
TPC223_FIXED_ATOM_CREDIT = 0
TPC223_L2 = NONE
TPC223_FULL_GATE_B = OPEN
TPC223_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V76 / TPC-223 已把“两个桥墩都必须支付”的直觉压成 exact
minimum-minus-loss compiler；下一座桥不是再做无符号 majorant，而是在同一 literal
prime shell 上证明或反驳 AP dispersion、polarized cross-correlation 与 reassembly
identification 的共同 interface。**

## 5.16 V75 / TPC-222：four-packet polarization and the PSD cross-term obstruction

TPC-222 把 TPC-218--221 的 four-packet signed interface 提炼成一个独立的 exact
Hilbert-space theorem。对 `G_(j,l)=<V_j,V_l>` 与 `V(c)=sum_j c_jV_j`，有

```text
||V(c)||^2 = c^*Gc,
<x,y> = 1/4 sum_(r=0)^3 i^(-r)||x+i^r y||^2,
0 <= c^*Gc <= tr(G)||c||_2^2.
```

四点极化说明 cross-term 只有在保留四个 phase-labelled energies 时才能 exact 恢复。
两组 rank-one fixtures `V_j^+=u` 与 `V_j^-=(-1)^j u` 具有相同 diagonal
`(1,1,1,1)`、相同 trace `4`，但 all-one coefficients 的 signed energies 分别为
`16` 与 `0`。所以 PSD/trace/diagonal 的 unsigned envelope 在该有限 scope 内不能
识别 signed reassembly；这是一项 scoped obstruction，不是 growing prime shell 的
渐近反例。

```text
TPC222_PSD_PACKET_GRAM = PROVED_EXACT
TPC222_FOUR_POINT_POLARIZATION = PROVED_EXACT
TPC222_TRACE_RAYLEIGH_ENVELOPE = PROVED_EXACT
TPC222_SIGNED_CROSS_TERM_IDENTIFIABILITY = REFUTED_SCOPED
TPC222_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC222_ARITHMETIC_ADVANCE = NO
TPC222_FIXED_ATOM_CREDIT = 0
TPC222_L2 = NONE
TPC222_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC222_FULL_GATE_B = OPEN
TPC222_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V75 / TPC-222 已证明 exact polarized compiler，并封住只使用无符号
diagonal/trace/PSD envelope 的捷径；下一篇应把 polarized cross-correlation 假设
组织成条件化 signed-reassembly compiler，同时明确不把条件假设冒充 arithmetic
theorem。**

## 5.15 V74 / TPC-221：collision-graph Schur envelope and literal saturation

TPC-221 把 TPC-220 的 collision Gram 变成 exact PSD operator。对任意 positive q-weights
`p_q` 与 complex shell weights `lambda`，

```text
E(lambda) = lambda^* Gamma lambda
  <= max_q p_q^(-1) sum_q' |Gamma(q,q')| p_q' * ||lambda||_2^2.
```

这一步给出 weighted Schur envelope，完整保留 off-diagonal collision entries，但不
创造 sign/phase cancellation。literal finite saturation fixture 取 `h=5`, `H=500`,
constant profile 与 `q={101,151,181,191}`；所有 rows 都是 `e_1+e_4`，所以
`Gamma=2J_4`，Schur radius/top Rayleigh quotient 为 `8`，equal weights 的
coherent-to-diagonal ratio 恰为 `P=4`。

```text
TPC221_COLLISION_GRAM_PSD = PROVED_EXACT
TPC221_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_WEIGHTED_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_LITERAL_SATURATION = PROVED_EXACT_FINITE
TPC221_ABSOLUTE_SCHUR_SUBP_SAVING = REFUTED_SCOPED
TPC221_ARITHMETIC_ADVANCE = NO
TPC221_FIXED_ATOM_CREDIT = 0
TPC221_L2 = NONE
TPC221_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC221_FULL_GATE_B = OPEN
TPC221_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V74 / TPC-221 已完成 collision-degree 的 exact absolute envelope，同时
用 literal saturation 封住“Schur 自动击破 `P`”这条捷径；下一座桥必须寻找 growing
scale 的 signed/phase-sensitive dispersion。**

## 5.14 V73 / TPC-220：prime-AP collision crosswalk

TPC-220 沿 TPC-219 的 transverse ledger 回到同一个 literal q-labelled row family。
对 primitive residue `a mod h`，row congruence 精确给出 weighted prime-AP packet：

```text
sum_q lambda_q B_(h,q)^(j)(a)
  = sum_(m != 0) Pi_(h,m)^(j)(a^(-1)m; lambda).
```

对两个 q rows 展开 primitive Gram，得到

```text
Gamma_h^(j,l)(q,q')
 = sum_(m,m') w_(h,m,q)^(j) conjugate(w_(h,m',q')^(l))
     1_(m q'=m' q mod h).
```

当 `q=q'` 且 `2L_(h,q)<h` 时，cutoff injectivity 强制 diagonal atom energy；当
`q!=q'` 时，碰撞 congruence 形成非空 off-diagonal graph。exact rational certificate
覆盖 3 个 modulus、4 个 primes、2 个 profiles，所有 crosswalk/Gram/diagonal residual
均为零，并由 adversarial fixture 确认 collision edge 存在。

```text
TPC220_PRIME_AP_CROSSWALK = PROVED_EXACT
TPC220_MULTIPLICATIVE_COLLISION_GRAM = PROVED_EXACT
TPC220_DIAGONAL_REDUCTION = PROVED_EXACT
TPC220_ARITHMETIC_ADVANCE = NO
TPC220_FIXED_ATOM_CREDIT = 0
TPC220_L2 = NONE
TPC220_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC220_FULL_GATE_B = OPEN
TPC220_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V73 / TPC-220 已把 abstract q-transverse target 接回 literal prime-AP
and collision coordinates；下一座桥必须量化 off-diagonal collision graph beyond
absolute Schur，不能把 exact crosswalk 误报成 arithmetic saving。**

## 5.13 V72 / TPC-219：prime-shell longitudinal ledger and the exact P collapse

TPC-219 对 TPC-218 的 q-labelled packet vectors
`Z_q(n)=(K_(j,q)(n))_j` 做 exact constant-mode projection。令
`Zbar=P^(-1)sum_q Z_q`、`R_q=Z_q-Zbar`，并在同一个 interval 上定义
`E_shell`、`E_diag`、`E_perp`，则

```text
E_shell = P(E_diag-E_perp),
0 <= E_perp <= E_diag,
E_shell <= eta P E_diag  <=>  E_perp >= (1-eta)E_diag.
```

这不是另一个 unsigned Cauchy envelope，而是 `P` collapse 的 exact iff ledger。四个
完全 aligned 的 q rows 有 `E_perp=0` 并饱和 `P`；balanced rows 的 shell 能量为零。
这些 fixtures 只说明 abstract Hilbert geometry不能提供 transverse lower bound，不是
literal growing prime shell 的 asymptotic statement。

```text
TPC219_LONGITUDINAL_TRANSVERSE_IDENTITY = PROVED_EXACT
TPC219_P_COLLAPSE_EQUIVALENCE = PROVED_EXACT
TPC219_ALIGNED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_BALANCED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_ARITHMETIC_ADVANCE = NO
TPC219_FIXED_ATOM_CREDIT = 0
TPC219_L2 = NONE
TPC219_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC219_FULL_GATE_B = OPEN
TPC219_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V72 / TPC-219 把 scalar `P` toll 精确转换成 literal q-transverse
energy theorem；下一篇必须沿 congruence collisions 建立 prime-AP/multiplicative
incidence crosswalk，不能把 abstract residual vectors 当成算术 cancellation。**

## 5.12 V71 / TPC-218：prime-shell Hilbert lift and the sharp collapse barrier

TPC-218 执行 TPC-217 的 label-preserving reassembly clue，但只推进可严格证明的
最小结构层。保持 `(q,j)` 两个 labels，Hilbert-valued additive large sieve 给出

```text
N^(-1) sum_(n in I_x)||K_vec(n)||_2^2
  << J M^2 x^(1/96)(log x)^5.
```

其中 fixed-q cutoff injectivity 给 row norm，active denominator 满足
`h>=H/(2Q)`，而 literal cluster coefficient 的 unsigned harmonic bound 为
`sum_h h|C_h|^2 << (log x)^5`。这一步没有用 PNT、Möbius cancellation 或
prime cancellation。

形成 scalar packet shell 时，pointwise q-Cauchy 精确付出 `P=#Q_x<=2Q`，恢复
`x^(11/32)(log x)^5`。finite constant-profile fixture 中四个 q rows 全部等于
`e_1+e_4`，coherent/diagonal ratio 恰为 `4=P`；parallel four-packet fixture 的
unit-projection ratio 为 `1`。所以 free q orthogonality 与 geometry-only packet
cancellation 都被 scoped refute。

```text
TPC218_HILBERT_VALUED_LARGE_SIEVE = PROVED_STANDARD_TENSOR_LIFT
TPC218_PRIME_LABEL_PRESERVATION = PROVED_EXACT
TPC218_PACKET_MATRIX_BOUND = PROVED_EXACT
TPC218_SPLIT_NORMALIZED_EXPONENT = PROVED_1_OVER_96_LOG_FIVE
TPC218_SCALAR_COLLAPSE_RECOVERY = PROVED_X_11_OVER_32_LOG_FIVE
TPC218_Q_COLLAPSE_COST = PROVED_P_FACTOR
TPC218_Q_ORTHOGONALITY = REFUTED_SCOPED
TPC218_PACKET_ALIGNMENT = REFUTED_SCOPED
TPC218_ARITHMETIC_ADVANCE = NO
TPC218_FIXED_ATOM_CREDIT = 0
TPC218_L2 = NONE
TPC218_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC218_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC218_FULL_GATE_B = OPEN
TPC218_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

地图位置：**V71 / TPC-218 已把 prime-shell/four-packet label-preserving interface
做成严格的 finite-window Hilbert lift，并把唯一 generic scalar loss 定位为 `P`；
下一座桥必须对 literal signed coefficient family 真正击破这个 collapse，而不能把
split exponent 当成 arithmetic credit。**

## 6. 图像名称与仓库名称的对应

这里最容易出现的误解，是把图像 Bridge A/B 与仓库内部 A/B/C gate 当成同一套编号。

| 图像语言 | 仓库 V59 语言 | 关系 |
|---|---|---|
| Bridge A：解析 collective saving | `B(positive Gram / MPD / P2 / K / E / X)` 与 `A(alias)` 的 zero-axis transference | 图像的一座大桥被拆成多车道 B、terminal A 及 exact AND compiler |
| Bridge B：distinguished-seed genericity | `C` symmetry-breaking reserve | 都是动力学/指定 seed 后备线 |
| 核心算术估计 | one full-shell fold root + four-packet polarized prime-BDH compiler；V56 tree/PAD为 fallback；`kappa` root anchor作 exact transfer | 当前 red-X 的两座真实桥墩与一根已安装锚索 |

仓库选择路线为：

```text
PROPER_FACTOR_CENTERED_POISSON_TRANSFERENCE
THEN_TRANSITION_GCD_REDUCTION_TO_RAMANUJAN_MEAN_AND_RECIPROCAL_VARIANCE
THEN_ADDITIVE_ZERO_MODE_EXCISION_AND_CENTERED_PRIME_HYBRID_COVARIANCE
THEN_EXACT_CONDUCTOR_EULER_SCALAR_SPLICE
THEN_PAY_CRITICAL_CONDUCTOR_COLLAR_TO_D1
THEN_PROMOTE_TO_SELF_FINANCING_D_DELTA_FOR_0_LT_DELTA_LT_1_OVER_9600
THEN_GLOBAL_SIEGEL_QUALITY_DICHOTOMY
IF_UNBOUNDED_THEN_SOURCE_BACKED_DIRECT_TPC_EXIT
IF_BOUNDED_SEQUENTIAL_ROUTE_THEN_B_DEPENDENT_ENDPOINT_MATCHED_SIGNED_CORE
OR_FOLD_FIRST_UNORDERED_PAIR_GATE_A_BYPASS
THEN_ONE_MIXED_PLUS_BALANCED_LONG_MOBIUS_SIGNED_AGGREGATE
THEN_COMPENSATED_PRIME_DILATION_AND_PAIR_ANGULAR_ENDPOINT_GATE
THEN_COMPLETE_EACH_PRIME_ROW_BEFORE_THE_Q_SHELL_ABSOLUTE
THEN_EXACT_PAIRED_ROW_MODE_DIAGONALIZATION
THEN_CLASSIFY_EVERY_POST_Q_OPERATOR_AS_TRANSVERSE_OR_TERMINAL
THEN_STOP_LONGITUDINAL_QSPACE_PRELIMINARY_ENGINEERING
THEN_RETURN_TO_PRE_Q_MAXIMAL_FOLD_FIRST_OR_PAIR_ANGULAR_GATE_A
THEN_ONE_COMMON_TRANSVERSE_ROW_VARIANCE
AND_USE_LONGITUDINAL_REPLICA_ONLY_AS_TERMINAL_READOUT
THEN_IDENTIFY_THE_GATE_B_TERMINAL_DIRECTION_WITH_THE_V35_CENTERED_SCALAR
THEN_POLARIZE_GATE_B_INTO_FOUR_ONE_SEQUENCE_PRIME_BDH_REMAINDERS
THEN_COMPILE_MESOSCOPIC_BLOCKS_COLLECTIVELY_TO_CRITICAL_KLOOSTERMAN_CELLS
THEN_REASSEMBLE_THE_PRIME_ONLY_SIGNED_PACKET_BEFORE_ANY_OUTER_ABSOLUTE
AND_PHYSICAL_POSITIVE_GRAM_COLLISION_VIA_PROPER_FACTOR_DYADIC_MPD
OR_P2_DIRECT_Q_DEPENDENT_PACKET_ENERGY
OR_K_SPECIALIZED_BLOCK_SCHATTEN_COMPRESSION
OR_E_WHOLE_RESIDUAL_ENERGY
OR_X_JOINT_CHARACTER_DECOUPLING
THEN_A_AND_B_ZERO_AXIS_REASSEMBLY
THEN_C_SYMMETRY_BREAK_RESERVE
```

## 7. 当前状态防火墙

截至 V85 / TPC-232：

```text
ROUTE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
TRANSLATION_SUBGATE_STRICT_1_OVER_400 = PAID
FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_208_TRIGGER = true
TPC_209_TRIGGER = true
TPC_210_TRIGGER = true
TPC_211_TRIGGER = true
TPC_212_TRIGGER = true
TPC_213_TRIGGER = true
TPC212_EMITTER_ONLY_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC212_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = REPLACED_BY_TPC213_OPERATOR
TPC213_PHYSICAL_DIRECT_SUM_REPLACEMENT = REFUTED_SCOPED
TPC213_LITERAL_V46_ASYMPTOTIC_GRAM_BOUND = OPEN
TPC214_EMITTER_DILATION_COVARIANCE = PROVED_EXACT
TPC214_REDUCED_DENOMINATOR_CLUSTER_FACTOR = PROVED_EXACT
TPC214_UNIVERSAL_CLUSTER_SAVING_SIGN = REFUTED_SCOPED
TPC214_LITERAL_V46_ASYMPTOTIC_CLUSTER_BOUND = OPEN
TPC214_PRIME_SHELL_REASSEMBLY = OPEN
TPC214_ARITHMETIC_ADVANCE = NO
TPC214_FIXED_ATOM_CREDIT = 0
TPC214_L2 = NONE
TPC214_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC215_ACTIVATION_FLOOR = PROVED_EXACT
TPC215_SHORT_QUOTIENT_NORMAL_FORM = PROVED_EXACT
TPC215_CLUSTER_TO_DIRECT_MAJORANT = PROVED_O_LOG_X_SQUARED
TPC215_FIXED_POWER_CLUSTER_AMPLIFICATION = EXCLUDED
TPC215_TOP_SHELL_RATIO_ONE = PROVED_EXACT
TPC215_DIRECT_SUM_ARITHMETIC_ENERGY_BOUND = OPEN
TPC215_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN
TPC215_PRIME_SHELL_REASSEMBLY = OPEN
TPC215_ARITHMETIC_ADVANCE = NO
TPC215_FIXED_ATOM_CREDIT = 0
TPC215_L2 = NONE
TPC215_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC216_FIXED_Q_NO_COLLISION = PROVED_EXACT
TPC216_FIXED_Q_ROW_ENERGY = PROVED_EXACT
TPC216_SHELL_CAUCHY_ENVELOPE = PROVED_EXACT
TPC216_PRIME_SHELL_CARDINALITY = PROVED_P_LE_2Q
TPC216_NORMALIZED_EXPONENT = PROVED_11_OVER_32
TPC216_DIRECT_SUM_ROW_ENERGY_ENVELOPE = PROVED_X_11_OVER_32_LOG_CUBED
TPC216_ARITHMETIC_CANCELLATION = NONE
TPC216_ALIGNED_SUPPORT_ADVERSARY = NUMERICALLY_CERTIFIED_EXACT_RATIONAL
TPC216_FREE_Q_ORTHOGONALITY = REFUTED_SCOPED
TPC216_FINITE_WINDOW_OFF_FREQUENCY_GRAM = CONTROLLED_BY_TPC217_LARGE_SIEVE
TPC216_PRIME_SHELL_REASSEMBLY = OPEN
TPC216_ARITHMETIC_ADVANCE = NO
TPC216_FIXED_ATOM_CREDIT = 0
TPC216_L2 = NONE
TPC216_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC217_REDUCED_FREQUENCY_REGROUPING = PROVED_EXACT
TPC217_FAREY_SPACING = PROVED_EXACT
TPC217_ADDITIVE_LARGE_SIEVE = PROVED_STANDARD
TPC217_FINITE_WINDOW_ATTACHMENT = PROVED_X_11_OVER_32_LOG_FIVE_NORMALIZED
TPC217_UNNORMALIZED_WINDOW_EXPONENT = PROVED_43_OVER_32
TPC217_WINDOW_LOSS = PROVED_1_PLUS_U2_OVER_N
TPC217_FINITE_WINDOW_OFF_FREQUENCY_GRAM = CONTROLLED_BY_LARGE_SIEVE
TPC217_ALIGNED_ONE_POINT_ORTHOGONALITY = REFUTED_SCOPED
TPC217_PRIME_SHELL_REASSEMBLY = OPEN
TPC217_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC217_ARITHMETIC_CANCELLATION = NONE
TPC217_ARITHMETIC_ADVANCE = NO
TPC217_FIXED_ATOM_CREDIT = 0
TPC217_L2 = NONE
TPC217_FULL_GATE_B = OPEN
TPC217_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC218_HILBERT_VALUED_LARGE_SIEVE = PROVED_STANDARD_TENSOR_LIFT
TPC218_PRIME_LABEL_PRESERVATION = PROVED_EXACT
TPC218_PACKET_MATRIX_BOUND = PROVED_EXACT
TPC218_SPLIT_NORMALIZED_EXPONENT = PROVED_1_OVER_96_LOG_FIVE
TPC218_SCALAR_COLLAPSE_RECOVERY = PROVED_X_11_OVER_32_LOG_FIVE
TPC218_Q_COLLAPSE_COST = PROVED_P_FACTOR
TPC218_Q_ORTHOGONALITY = REFUTED_SCOPED
TPC218_PACKET_ALIGNMENT = REFUTED_SCOPED
TPC218_ARITHMETIC_ADVANCE = NO
TPC218_FIXED_ATOM_CREDIT = 0
TPC218_L2 = NONE
TPC218_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC218_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC218_FULL_GATE_B = OPEN
TPC218_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC219_LONGITUDINAL_TRANSVERSE_IDENTITY = PROVED_EXACT
TPC219_P_COLLAPSE_EQUIVALENCE = PROVED_EXACT
TPC219_ALIGNED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_BALANCED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_ARITHMETIC_ADVANCE = NO
TPC219_FIXED_ATOM_CREDIT = 0
TPC219_L2 = NONE
TPC219_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC219_FULL_GATE_B = OPEN
TPC219_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC220_PRIME_AP_CROSSWALK = PROVED_EXACT
TPC220_MULTIPLICATIVE_COLLISION_GRAM = PROVED_EXACT
TPC220_DIAGONAL_REDUCTION = PROVED_EXACT
TPC220_ARITHMETIC_ADVANCE = NO
TPC220_FIXED_ATOM_CREDIT = 0
TPC220_L2 = NONE
TPC220_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC220_FULL_GATE_B = OPEN
TPC220_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC221_COLLISION_GRAM_PSD = PROVED_EXACT
TPC221_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_WEIGHTED_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_LITERAL_SATURATION = PROVED_EXACT_FINITE
TPC221_ABSOLUTE_SCHUR_SUBP_SAVING = REFUTED_SCOPED
TPC221_ARITHMETIC_ADVANCE = NO
TPC221_FIXED_ATOM_CREDIT = 0
TPC221_L2 = NONE
TPC221_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC221_FULL_GATE_B = OPEN
TPC221_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC222_PSD_PACKET_GRAM = PROVED_EXACT
TPC222_FOUR_POINT_POLARIZATION = PROVED_EXACT
TPC222_TRACE_RAYLEIGH_ENVELOPE = PROVED_EXACT
TPC222_SIGNED_CROSS_TERM_IDENTIFIABILITY = REFUTED_SCOPED
TPC222_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC222_ARITHMETIC_ADVANCE = NO
TPC222_FIXED_ATOM_CREDIT = 0
TPC222_L2 = NONE
TPC222_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC222_FULL_GATE_B = OPEN
TPC222_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC223_TWO_CHANNEL_COMPILER = PROVED_CONDITIONAL_ALGEBRA
TPC223_AP_DISPERSION = OPEN_CONDITIONAL_INPUT
TPC223_POLARIZED_CROSS_CORRELATION = OPEN_CONDITIONAL_INPUT
TPC223_LITERAL_REASSEMBLY_INTERFACE = OPEN_CONDITIONAL_INPUT
TPC223_EFFECTIVE_SAVING = CERTIFIED_EXACT_MIN_MINUS_LOSS
TPC223_STRICT_1_OVER_400 = CONDITIONAL_ONLY
TPC223_ARITHMETIC_ADVANCE = NO
TPC223_FIXED_ATOM_CREDIT = 0
TPC223_L2 = NONE
TPC223_FULL_GATE_B = OPEN
TPC223_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC224_COMMON_LITERAL_HILBERT_INTERFACE = PROVED_EXACT
TPC224_SHARP_ADDITIVE_CONSTANT = PROVED_EXACT
TPC224_UNIT_INTERFACE = REFUTED_SCOPED
TPC224_SOURCE_CLOCK_AUDIT = NUMERICALLY_CERTIFIED_EXACT_RATIONAL
TPC224_AP_DISPERSION = OPEN
TPC224_POLARIZED_CROSS_CORRELATION = OPEN
TPC224_LITERAL_V46_TRANSFER = OPEN
TPC224_ARITHMETIC_ADVANCE = NO
TPC224_FIXED_ATOM_CREDIT = 0
TPC224_L2 = NONE
TPC224_FULL_GATE_B = OPEN
TPC224_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
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
TPC226_DILATED_CLOCK_FAMILY = MODELING_CHOICE
TPC226_PRIMITIVE_SOURCE_ROW = PROVED_EXACT
TPC226_L_LE_3_DISJOINTNESS = PROVED_EXACT
TPC226_FIRST_PRIMITIVE_COLLISION_DILATION = 4
TPC226_L4_RESONANCE_CLASSIFICATION = PROVED_EXACT
TPC226_UNIFORM_PROFILE_INDEPENDENT_SAVING = REFUTED_SCOPED
TPC226_V46_PROFILE_TRANSFER = OPEN
TPC226_ARITHMETIC_ADVANCE = NO
TPC226_FIXED_ATOM_CREDIT = 0
TPC226_L2 = NONE
TPC226_FULL_GATE_B = OPEN
TPC226_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC227_V59_PACKET_AXIS = SOURCE_LOCKED
TPC227_V59_PROFILE_AXIS = SOURCE_LOCKED_COMMON
TPC227_FOUR_GRAM_CRITERION = PROVED_EXACT
TPC227_Q25_ROW_SIGN_GRAM_MISMATCH = PROVED_EXACT
TPC227_TPC226_AUTOMATIC_SOURCE_TRANSFER = REFUTED_SCOPED
TPC227_SOURCE_NATIVE_COMMON_PROFILE_COMPILER = OPEN
TPC227_ARITHMETIC_ADVANCE = NO
TPC227_FIXED_ATOM_CREDIT = 0
TPC227_L2 = NONE
TPC227_FULL_GATE_B = OPEN
TPC227_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC228_POLARIZED_AP_MINUS_DIAGONAL_COMPILER = PROVED_EXACT
TPC228_SOURCE_LABELLED_COLLISION_SUM = PROVED_EXACT
TPC228_Q25_3_7_SOURCE_BLOCK = PROVED_EXACT_FINITE
TPC228_ACTUAL_V59_TO_PRIMITIVE_ATOM_CROSSWALK = OPEN
TPC228_ARITHMETIC_ADVANCE = NO
TPC228_FIXED_ATOM_CREDIT = 0
TPC228_L2 = NONE
TPC228_FULL_GATE_B = OPEN
TPC228_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC229_RESONANCE_GRAPH_MATCHING = PROVED_EXACT
TPC229_EDGE_SPECTRUM = PROVED_EXACT
TPC229_GLOBAL_BLOCK_DIRECT_SUM = PROVED_EXACT
TPC229_DELTA_SAVING_CRITERION = PROVED_EXACT
TPC229_ARITHMETIC_ANTISYMMETRIC_DOMINANCE = OPEN
TPC229_ARITHMETIC_ADVANCE = NO
TPC229_FIXED_ATOM_CREDIT = 0
TPC229_L2 = NONE
TPC229_FULL_GATE_B = OPEN
TPC229_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC230_MATCHED_MASS_SAVING_CEILING = PROVED_EXACT_SHARP
TPC230_COMPARABLE_ROW_DENSITY_TOLL = PROVED_EXACT
TPC230_LITERAL_ALIGNED_KAPPA_LE_4 = PROVED_EXACT
TPC230_STRICT_1_OVER_400_EDGE_DENSITY_TOLL = 1/3200
TPC230_ASYMPTOTIC_RESONANCE_EDGE_DENSITY = OPEN
TPC230_ARITHMETIC_ADVANCE = NO
TPC230_FIXED_ATOM_CREDIT = 0
TPC230_L2 = NONE
TPC230_FULL_GATE_B = OPEN
TPC230_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC231_3716_PARAMETERIZATION = PROVED_EXACT
TPC231_3716_LOCAL_ROOT_LAW = PROVED_EXACT
TPC231_3716_SELBERG_UPPER_BOUND = PROVED_SOURCE_BACKED
TPC231_3716_EDGE_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC231_FIXED_FINITE_RESONANCE_SUPPORT_DENSITY_ZERO = PROVED_ASYMPTOTIC
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
TPC232_GROWING_COLLISION_NORMAL_FORM = PROVED_EXACT
TPC232_UNIFORM_POLYLOG_DEPTH_SIEVE = PROVED_SOURCE_BACKED
TPC232_COLLISION_INCIDENCE_BOUND = PROVED_ASYMPTOTIC
TPC232_SUBCRITICAL_DEPTH_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC232_SUBCRITICAL_FIXED_SAVING = STOP_SCOPED
TPC232_CRITICAL_DEPTH_SUFFICIENCY = OPEN
TPC232_DILATED_CLOCK = MODELING_CHOICE
TPC232_ACTUAL_V59_CLOCK_ATTACHMENT = OPEN
TPC232_ARITHMETIC_ADVANCE = NO
TPC232_ARITHMETIC_OBSTRUCTION = PROVED_SOURCE_BACKED
TPC232_FIXED_ATOM_CREDIT = 0
TPC232_L2 = NONE
TPC232_FULL_GATE_B = OPEN
TPC232_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
NUMBERED_RELEASE = TPC-232
```

以下事实不得从路线图中推断：

- exact compiler 不等于 arithmetic saving；
- finite fixture 或 checker PASS 不等于渐近定理；
- averaged/a.e. phase 不等于 named fixed atom；
- source-backed local engine 不等于 whole-object reassembly；
- off-zero control 不等于 physical zero-axis payment；
- route advance 不自动创建下一篇编号；TPC-208、TPC-209、TPC-210、TPC-211 与 `TPC-212` 都是由各自
  exact theorem-backed structural edge 或 scoped obstruction 触发，下一编号仍须重新
  检查 theorem edge，不得由本地图箭头自动生成。

## 8. 下一步大路

优先级更新为：

1. **TPC-232 已完成：subcritical growing-depth obstruction**。在 modeled `h=4LQ`
   family 上，uniform sieve 证明所有 `L=o(log Q/loglog Q)` 仍只有 `o(P)` incident
   rows，fixed-comparability saving 已 `STOP_SCOPED`。下一步先审计 critical-depth raw
   row mass 与 collision degree，再检查 actual V59 clock/source attachment。
2. **TPC-231 已完成：finite-resonance sieve obstruction**。first `3--7` 与任意 fixed
   finite primitive resonance family 的 `o(P)` edge density 已 proved；bounded-degree
   comparable-row fixed-saving route 已 `STOP_SCOPED`；其 growing-depth fork 已由
   TPC-232 推进到 critical threshold。
2. **TPC-230 已完成：matched-resonance mass ceiling**。global saving capacity 与
   `1/3200` density toll 已 exact；其 asymptotic density question 已由 TPC-231 回答为零。
2. **TPC-229 已完成：primitive resonance matching spectrum**。all-scale matching、sharp
   edge spectrum 与 exact antisymmetric saving criterion 已证明；下一步 quantify matched
   resonance source mass。
2. **TPC-228 已完成：source-native polarized collision compiler**。common-profile
   packet AP-minus-diagonal exact 编译成 `sum_(q!=r)<U_q,V_r>`，Q25 first resonance
   成为 explicit four-term beta-w block；下一步做 resonance graph 的 exact 2x2 blocks。
2. **TPC-227 已完成：packet/profile axis separation**。V59 packet phase 被锁在
   `a^(j)=beta+i^j w`，Poisson profile 对四包共同；four-Gram iff criterion 与 Q25
   `-1/80000` mismatch 封住 automatic profile-to-source transfer。下一步是 source-native
   common-profile collision compiler。
2. **TPC-226 已完成：first primitive-collision transition**。`L<=3` 的 primitive
   prime rows 仍 disjoint；`L=4` 的全部 overlap 被 exact classified 为
   `7p+3r=16Q` 的 `3--7` resonance。aligned/affine amplification 与 balanced-sign
   cancellation 同时证明 geometry 不决定符号；下一步必须 source-lock actual V46
   profiles。TPC-225 的 cutoff-one obstruction 与 TPC-224 common interface 作为直接
   上游保留。
3. **TPC-225 已完成：cutoff-one shared-clock obstruction**。在 TPC-224 named
   source-surrogate clock 上证明 `E_AP=E_diag`、`E_all=E_pol` 与
   prime-support disjointness，strict AP saving 在该 clock 上 scoped-refuted；这是一项
   structural L1，不支付 arithmetic marginal。其直接上游 TPC-224 已完成共同 literal
   interface `E_all<=min(J E_AP,P E_pol)<=PJ/(P+J)(E_AP+E_pol)` 并用
   congruence-aligned stress scales scoped-refute unit-factor shortcut。
4. **TPC-223 已完成：conditional signed-reassembly compiler**。在共同 literal interface
   假设下，two-channel exponent exact 编译为
   `sigma=min(delta_AP,kappa_pol)-lambda_struct`；canonical ledger 给出 effective
   saving `11/1200` 与 strict margin `1/150`，但三条输入仍为 conditional open。
5. **TPC-222 已完成：four-packet polarization and PSD cross-term obstruction**。四点极化
   exact 恢复 signed cross-term；相同 diagonal/trace 的 rank-one fixtures 给出目标能量
   `16/0`，因此 unsigned PSD/trace envelope 不能识别 signed reassembly。下一步是把
   phase-labelled cross-correlation 写成条件化、可审计的 reassembly compiler。
6. **TPC-221 已完成：collision-graph Schur envelope and literal saturation**。PSD Gram
   identity 与 weighted Schur envelope 已严格证明；`h=5` literal aligned fixture 达到
   `Gamma=2J_4` 与 exact ratio `P=4`，因此 absolute collision-degree control 不能
   单独产生 sub-`P` saving。下一步必须是 signed/phase-sensitive dispersion。
6. **TPC-220 已完成：exact prime-AP / multiplicative collision crosswalk**。literal
   q-row reassembly 已写成带原 cutoff/profile 的 weighted prime-AP packet，two-row Gram
   已写成 `m q'=m' q (mod h)` collision graph；diagonal 在 cutoff injectivity 下精确
   还原，但 off-diagonal 的 Schur-beyond control 仍是开放桥。
7. **TPC-219 已完成：exact longitudinal/transverse prime-shell ledger**。`P` collapse
   满足 `E_shell=P(E_diag-E_perp)`，任何 sub-`P` saving 都等价于 literal q-transverse
   lower bound；aligned/balanced endpoint fixtures 已通过 exact rational certificate。
8. **TPC-218 已完成：prime-shell/packet-preserving Hilbert lift**。split vector envelope
   达到 `x^(1/96)(log x)^5`，scalar recovery 的 `P<=2Q` 成本被显式隔离；q-alignment
   ratio `P=4` 与 packet projection ratio `1` 是 scoped adversarial controls。
9. **TPC-217 已完成：finite-window large-sieve attachment**。reduced rational regrouping、
   Farey spacing 与 standard additive large sieve 将 TPC-216 envelope 接到 actual
   physical interval，得到 `x^(11/32)(log x)^5` normalized bound；ratio-two adversary
   证明短窗不能免费使用 orthogonality。
10. **TPC-216 已完成：direct-sum row-energy envelope**。fixed-q no-collision、shell Cauchy、
   `P<=2Q` 与 `11/32` exponent ledger 已封存；aligned-support adversary 证明 free
   q-orthogonality 不能结构性删除。
11. **TPC-215 已完成：short-quotient Möbius tails**。activation floor、`23/2400` quotient
   clock、harmonic diagonal anchor、row-norm decomposition 与 `O((log x)^2)` complete-
   period cluster-to-direct majorant 已封存；top-shell ratio-one 是精确 obstruction。
12. **TPC-232 的下一步：critical depth / actual source fork**。TPC-232 只给必要尺度，
    不给 critical-depth lower bound。先量化 modeled clock 的 raw row mass、degree 与
    normalization stability；随后返回 actual V59 source-to-row crosswalk，不把 modeled
    critical clock 自动解释成 physical source。
13. **TPC-221 的下一步：signed/phase-sensitive collision dispersion**。在 exact Schur
   envelope 与 saturation obstruction 之后，寻找能使用 literal signs/phases 的
   growing-scale theorem；不能把 absolute row sums当作 arithmetic credit。
14. **TPC-220 的下一步：collision graph beyond Schur**。量化 off-diagonal multiplicative
   collisions，寻找真实的 dispersion/cancellation hypothesis；exact crosswalk 本身
   不产生 arithmetic `L2`。
15. **TPC-219/218 的下一步：literal signed prime-shell/four-packet reassembly**。保持 finite-window
   large-sieve attachment，同时重新引入 literal prime rows、Möbius signs、zero/nonunit
   ledgers；不得把 structural `L1` bound误称为 arithmetic saving。
16. **V59 polarized prime-BDH Gate-B compiler**。若 physical coupling给出可用的 cell interface，
   对四个 `a^(j)=beta+i^j w` 的同一个 prime-only、kernel-localized、
   diagonal-corrected reduced-residue remainder证明集体 fixed-power saving；不得把
   Harper all-moduli variance或 Blomer--Pascadi fixed cell直接当成 global theorem；
17. **V58 full-shell Gate-A root**。直接证明同一个 literal V51
   mixed-plus-balanced fold的 full-shell fixed-power saving；这是与 Gate-B 并行的主
   桥墩，不是 V60 translation payment的自动后果；
18. **按全局 Siegel quality 保留条件分流**。unbounded world可调用已锁定的
   Matomaki--Merikoski `h=2` correlation exit；不得把单尺度 singleton误判为
   unbounded sequence；
19. **V58 Gate-B scalar root（等价终端表述）**。直接对已经 exact识别的 V35
   proper-factor centered core证明
   `|mathfrak C_x|<<x^(5/3-delta+o(1))`、`delta>1/400`；V59只重写对象，
   没有降低这个 terminal burden；
20. **optional q-transverse railing**。只有在同时追求全部 V57 Gate-A prefixes时，
   才证明 `C_perp` 的 one-`Q` variance；不得再把它列为 physical endpoint必需门；
21. **V56 canonical dyadic block Gate A fallback**。若无法得到 selected two-pier
   package，仍可对 pruned tree的 large nodes统一估计；
22. **V52 pre-q PAD Gate A**。在 exact diagonal-completed character packet中同时保留
   signed diagonal/off-diagonal，并支付
   `(delta_B+delta_W)/2+rho>1/400`；fixed-modulus local engine只作条件工具；
23. **common transverse deck fallback**。只需对 `Pi_perp P` 或 `Pi_perp C` 的一种 literal
   row species证明 one-`Q` variance，另一种由 paid difference自动继承；不得先把
   longitudinal mode删掉后声称完整 theorem；
24. **A/sequential bounded-world alternative**。保留 `forall B exists delta_B` 的
   endpoint-matched direct core与三引擎 heuristic fallback，但不再强迫它先于
   reverse-Type-I/balanced lane；
25. **B/PG--MPD 与 B/P2/K/E/X：保留并行 Gate-B 施工**。V42 cellwise MPD仍是
   preferred sufficient gate；P2/K 是 stronger norms，E/X
   分别是 `sigma<13/4800` whole residual energy和
   `kappa>403/1200` joint character theorem，不与 MPD lane叠加 theorem credit；
26. **C：只在前二十五条路线真实阻断或新 source 出现时，重开 distinguished-seed
   symmetry-breaking/dynamics reserve。**

### 8.1 地图式施工顺序

```text
TPC-207 moving-hole payment                         DONE (structural L1)
        |
        +--> TPC-208 zero-hole additive edge frame  DONE (structural L1)
        |          |
        |          +--> TPC-209 whole-frame transform DONE (frame-only obstruction)
        |          |       |
        |          |       +--> TPC-210 profile realizability DONE (profile-class obstruction)
        |          |               |
        |          |               +--> TPC-211 product-coupled packet DONE (full rank / derivative)
        |          |                       |
        |          |                       +--> TPC-212 cut boundary + A_d(r) operator DONE (scoped)
        |          |               -> collective four-packet prime-BDH compiler
        |          |       -> Gate-B scalar saving > 1/400
        |          |
        |          +------> explicit obstruction recorded
        |                  -> smallest repaired zero-hole theorem = physical-coupled profile route
        |
        +--> parallel: V51 full-shell signed Gate-A root
                   -> endpoint matching / loss ledger
                   -> common Bridge-A crossing
                                   |
                                   v
                              TPC endpoint
```

这里的“并行”只表示路线保留，不表示同时创建互相依赖的论文；每篇新论文必须对应
一个真实 theorem、obstruction、反例或可复现 numerical certificate。岛 5/Bridge B
和岛 7 继续作为辅助支路，不与当前 prime-dynamics 主线拼接 claim credit。

最窄 first fatal：

```text
NO_THEOREM_JOINTLY_COMPILES_THE_COMPLETE_ORIENTED_D_K_ADDITIVE_EDGE_FRAME_OF_THE_LITERAL_BLOCK_PACKETS_INTO_SOURCE_VALID_KLOOSTERMAN_CELLS_AND_REASSEMBLES_ALL_BLOCKS_FOUR_PACKET_SIGNS_AND_PRIME_MODULI_WITH_A_FIXED_SAVING
```

## 9. 后续更新协议

每次更新本地图时：

1. 先读取最新 `TPC_HANDOFF.md` 页首和 current section；
2. 只在新的 sealed big-road release 或 numbered theorem 改变状态后移动 `YOU ARE HERE`；
3. 记录版本号、日期、release commit、proof 和 checker 路径；
4. 将“结构完成”“条件完成”“算术完成”分开登记；
5. 保留旧路线的 `STOP_SCOPED` 原因，不把改名当成 reopen；
6. 若只是图片美化、文字澄清或 checker 加固，不改变 arithmetic status；
7. 更新后核对本文件、big-road README、Compass、Handoff 与
   `PAPER_CANDIDATE_LEDGER.md` 不冲突；paper ledger中的 claim class不得因路线图措辞升级。

## 10. 版本记录

| 日期 | 地图版本 | 当前位置 | Release anchor | 变化 |
|---|---|---|---|---|
| 2026-08-24 | V85 / TPC-232 | Bridge A / Gate B：subcritical growing-depth obstruction；critical mass/degree 与 actual source open | `TPC-232` | exact one-wrap compiler、coefficient-uniform Selberg sieve、`C_L<<LQ loglog(3LQ)/log^2Q`、subcritical fixed saving stop-scoped；arithmetic cancellation仍为 NO |
| 2026-08-24 | V84 / TPC-231 | Bridge A / Gate B：finite-resonance sieve obstruction；fixed finite comparable-row route stop-scoped，growing depth/actual source open | `TPC-231` | exact determinant/local-root law、Selberg `E/P->0`、fixed-finite-family extension、bounded-degree energy transfer；arithmetic cancellation仍为 NO |
| 2026-08-24 | V83 / TPC-230 | Bridge A / Gate B：matched-resonance mass ceiling；two-linear-form density open | `TPC-230` | sharp `E_AP>=D-M`、comparability density toll、literal `kappa<=4`、strict endpoint needs `1/3200`；arithmetic仍为 NO |
| 2026-08-24 | V82 / TPC-229 | Bridge A / Gate B：primitive resonance matching spectrum；matched mass/arithmetic dominance open | `TPC-229` | all-scale matching、`(-1,-1,+1,+1)` blocks、sharp AP ratio/delta criterion、4089-scale replay；arithmetic仍为 NO |
| 2026-08-24 | V81 / TPC-228 | Bridge A / Gate B：source-native polarized collision compiler；exact source block，atom crosswalk/arithmetic open | `TPC-228` | AP-minus-diagonal four-phase identity、Q25 four-term beta-w block、positive/negative/zero controls；arithmetic仍为 NO |
| 2026-08-24 | V80 / TPC-227 | Bridge A / Gate B：packet/profile axis separation；source phase 与 common profile exact typed，source-native collision compiler open | `TPC-227` | four-Gram iff theorem、Q25 `-1/80000` row-sign mismatch、automatic profile-to-source transfer scoped-refuted；arithmetic仍为 NO |
| 2026-08-24 | V79 / TPC-226 | Bridge A / Gate B：first primitive-collision transition；`L<=3` disjoint，`L=4` 唯一 `3--7` resonance；source sign 与 arithmetic open | `TPC-226` | exact collision classification、Q25 witness、505-scale census、aligned/affine amplification 与 balanced-sign cancellation；arithmetic仍为 NO |
| 2026-08-22 | V78 / TPC-225 | Bridge A / Gate B：cutoff-one shared-clock obstruction；named source clock 的 prime blocks exact orthogonal，strict AP saving scoped-refuted；nontrivial-cutoff overlap与arithmetic仍 open | `TPC-225` | exact cutoff-one theorem、`E_AP=E_diag`、`E_all=E_pol`、9+14 exact-rational audits、`Q=3..99` boundary replay；arithmetic仍为 NO |
| 2026-08-22 | V77 / TPC-224 | Bridge A / Gate B：literal two-channel compatibility；共同 Hilbert interface exact，unit-factor shortcut scoped-refuted；arithmetic marginals open | `TPC-224` | exact `E_all<=min(J E_AP,P E_pol)<=PJ/(P+J)(E_AP+E_pol)`、9+5 exact-rational finite audits、actual-prime congruence stress；arithmetic仍为 NO |
| 2026-08-22 | V76 / TPC-223 | Bridge A / Gate B：conditional two-channel signed-reassembly compiler；literal AP/polarized/reassembly inputs open | `TPC-223` | exact `min(delta_AP,kappa_pol)-lambda_struct` ledger、strict `1/400` criterion、`11/1200` effective saving fixture与 boundary adversaries；arithmetic仍为 NO |
| 2026-08-22 | V75 / TPC-222 | Bridge A / Gate B：four-packet PSD Gram、四点极化与 trace envelope；signed cross-term identifiability scoped-refuted；literal polarized reassembly open | `TPC-222` | exact four-phase compiler、sharp trace bound、same-diagonal/trace `16/0` rank-one obstruction；arithmetic仍为 NO |
| 2026-08-22 | V74 / TPC-221 | Bridge A / Gate B：collision-graph PSD/weighted-Schur envelope；literal absolute saturation；signed dispersion open | `TPC-221` | exact PSD identity、weighted Schur bound、`h=5` aligned `Gamma=2J_4` fixture with ratio `P=4`；arithmetic仍为 NO |
| 2026-08-22 | V73 / TPC-220 | Bridge A / Gate B：exact prime-AP / multiplicative collision crosswalk；Schur-beyond collision control open | `TPC-220` | weighted prime-AP reassembly、exact collision Gram、cutoff diagonal reduction、nonempty off-diagonal adversary；arithmetic仍为 NO |
| 2026-08-22 | V72 / TPC-219 | Bridge A / Gate B：exact longitudinal/transverse prime-shell ledger；`P` collapse iff q-transverse lower bound；prime-AP collision open | `TPC-219` | exact `E_shell=P(E_diag-E_perp)` identity、aligned/balanced endpoints、literal arithmetic仍为 NO |
| 2026-08-22 | V71 / TPC-218 | Bridge A / Gate B：prime-label/packet-preserving Hilbert lift；split `x^(1/96)`，scalar `P` collapse explicit；signed reassembly open | `TPC-218` | tensor large sieve、PSD packet Gram、exact `P=4` q-alignment 与 projection-ratio-one packet obstruction；arithmetic仍为 NO |
| 2026-08-22 | V70 / TPC-217 | Bridge A / Gate B：finite-window reduced-frequency large-sieve attachment `x^(11/32)(log x)^5`；prime-shell/four-packet reassembly open | `TPC-217` | exact regrouping、Farey spacing、standard additive large sieve、one-point ratio-two obstruction；arithmetic仍为 NO |
| 2026-08-21 | V69 / TPC-216 | Bridge A / Gate B：direct-sum row-energy envelope `x^(11/32)(log x)^3`；finite-window attachment open | `TPC-216` | fixed-q no-collision、shell Cauchy、`P<=2Q`、aligned-support adversary；arithmetic仍为 NO |
| 2026-08-20 | V68 / TPC-215 | Bridge A / Gate B：short-quotient Möbius tails；cluster-to-direct majorant `O((log x)^2)`；direct physical energy open | `TPC-215` | activation floor、`23/2400` quotient bound、exact row-norm decomposition、top-shell ratio-one obstruction；arithmetic仍为 NO |
| 2026-08-20 | V67 / TPC-214 | Bridge A / Gate B：Möbius-log reduced-frequency cluster tails；literal asymptotic bound open | `TPC-214` | exact dilation covariance、reduced-denominator factorization、zero-axis/four-packet compatibility、finite opposite-sign obstruction；arithmetic仍为 NO |
| 2026-08-18 | V65 / TPC-212 | Bridge A / Gate B：truncated boundary/emitter interface；literal physical cross-divisor Gram open | `TPC-212` | exact signed Boolean endpoint incidence、complete-minus-missing boundary、reciprocal collision Gram、block-diagonal alignment obstruction；arithmetic仍为 NO |
| 2026-08-18 | V64 / TPC-211 | Bridge A / Gate B：literal product-coupled profile full-rank and complete-packet derivative；truncated boundary/emitter open | `TPC-211` | product cocycle、full divisor rank、log-Mobius marked-prime derivative、common-endpoint cancellation、finite Gram alignment obstruction；arithmetic仍为 NO |
| 2026-08-18 | V63 / TPC-210 | Bridge A / Gate B：admissible Poisson profile-class obstruction；physical cross-divisor coupling open | `TPC-210` | finite Schwartz/Poisson profile surjectivity、literal Mobius alignment、cross-divisor PSD Gram reduction；arithmetic仍为 NO |
| 2026-08-18 | V62 / TPC-209 | Bridge A / Gate B：whole-frame Poisson profile interface；frame-only route scoped stop | `TPC-209` | fixed-divisor shared dual、whole-frame covariance、character profile normal form、V59 Gauss crosswalk、sharp alignment obstruction；arithmetic仍为 NO |
| 2026-08-17 | V61 | Bridge A / Gate B：zero-hole complete-graph pre-emitter built；whole-frame Kloosterman compiler open | working release；TPC-208 | exact additive projection、edgewise `(q-2)` diagonal deletion、physical-kernel crosswalk、oriented fibers与 literal-edge no-sparsification；arithmetic仍为 NO |
| 2026-08-17 | V60 | Bridge A / Gate B：translation subgate已支付；zero-hole prime-BDH仍 open | `19c57a320c9e572401b8eddd46ba16a4ff7c09d9`；TPC-207 | exact moving-hole projector、`q-2` diagonal lift、four-packet translation compiler与 `x^(53/32+o(1))` defect payment；full Gate B仍未关闭 |
| 2026-08-13 | V59 | Bridge A / Gate B：V35 terminal scalar已极化成四个 one-sequence prime-BDH remainders；collective block-to-cell compiler open | parent `f1ac29aed20e0ab7fbf8eaba3ae6339d9fca946a`; V59=current working release | exact complex polarization、`q-2` diagonal、reduced-residue variance、`Q^2/H=x^(1/96)` clock与 source/interface NO-GO；arithmetic仍为 NO |
| 2026-08-13 | V58 | Bridge A：physical endpoint收窄为 Gate-A root 与 V35 Gate-B scalar 两个 open piers；q-transverse row降为 optional maximal railing | target parent `c80d26e327ef2a979536c0f7dd3f69fe022befac`; V58=current working release | exact V35--V57 scalar crosswalk、q-weight Pythagoras、`tau_parallel=17/48-2delta`、two-scalar endpoint compiler；arithmetic仍为 NO |
| 2026-08-12 | V57 | Bridge A：longitudinal root anchor已安装；full-shell fold与 transverse Gate-B row为两个 open piers | target parent `0771f61e9175c5248d576bb8d42f510492d55209`; V57=current working release | exact prefix anchor、`143/96` error maximum、Gate-B row-Bessel maximalization、root-plus-transverse endpoint compiler；arithmetic仍为 NO |
| 2026-08-12 | V56 | Bridge A：maximal endpoint motion已压成 pruned dyadic large-node theorem；common transverse Gate B仍 open | target parent `4019d48b09ea8f1181953a9480ae66e55c4b10dc`; V56=current working release | one-modulus `53/32` envelope、`19/2400` leaf budget、binary prefix decomposition、tree/maximal power equivalence与 source firewall；arithmetic仍为 NO |
| 2026-08-12 | V55 | Bridge A：longitudinal modulus cable 已分类为 terminal readout；施工点前移到 pre-\(q\) Gate A 与 common transverse Gate B | target parent `7164a9a19fc9e938ee00344f908e369e7b759e13`; V55=current working release | every-modulus replica、一般 modulus-operator dichotomy、minimax extractor、PSD/TT-star firewall 与 V51 maximal-shell transfer；arithmetic仍为 NO |
| 2026-08-11 | V54 | Bridge A：paired rows 的 transverse deck 已识别；terminal longitudinal cable open | target parent `6ac39743d196bafd575014fe0a1cfe4373d723ee`; V54=current working release | exact `P-C=kappa*S-E`、paid difference energy、longitudinal extraction、transverse projection与 two-out-of-three terminal compiler；arithmetic仍为 NO |
| 2026-08-11 | V53 | Bridge A / Gates A--B：pair与physical两种 completed `q`-row桥墩已统一；one-`Q` Bessel theorem open | target parent `6f776d76ee4a1c3948cfd2332056d65dfae0c558`; V53=current working release | exact pair-row compression、`x^(95/48)` collision diagonal、`tau<419/1200` endpoint、symmetric `H_2RB(1/3,1/3)` compiler与 polarized-BDH diagonal-return NO-GO；arithmetic仍为 NO |
| 2026-08-11 | V52 | Bridge A / Gates A--B：compensated pair dilation与 angular endpoint已编译；PAD saving与 Gate B open | target parent `f2ab63730b04b386b2e3e44ad93bf551a2954388`; V52=current working release | dual pair/sieve coefficient、one compensated prime-dilation scalar、Hilbert packet endpoint simplex、marginal-only angle NO-GO与 paper ledger推进；arithmetic仍为 NO |
| 2026-08-11 | V51 | Bridge A / Gates A--B：无序因子对 fold-first pair-native Gate A 已编译；mixed+balanced whole-object saving 与 Gate B open | parent `6d94e300fb646872ff5fb7fa73a770f89180c3ba`; V51=current working release | exact two-orientation fold、rank-two numerator、Abel denominator compiler、diagonal-completed crosswalk与 character/Fourier emitter；orientation-first Poisson NO-GO；阶段性 paper ledger 建立；arithmetic仍为 NO |
| 2026-08-11 | V50 | Bridge A / Gates A--B：self-financing moving cut；unbounded-quality conditional TPC exit；bounded-quality signed core与 long-Mobius open | parent `d26f0ae41fe998431dffeabfc6808bc57e122d19`; V50=current working release | every `0<delta<1/9600` pays its complement at target-minus-delta；global Siegel-quality two-world compiler；arithmetic仍为 NO |
| 2026-08-11 | V49 | Bridge A / Gates A--B：critical conductor collar paid；ultra-low principal/generic/exceptional signed scalar与 long-Mobius open | parent `11643bd5a0f6f5259c5e04f6976cc59fc9e316be`; V49=current working release | paid cut推进到 `D1=x^(49/9600)`，margin `1/19200`；exact three-lane compiler；arithmetic仍为 NO |
| 2026-08-11 | V48 | Bridge A / Gates A--B：high conductor与 local Euler paid；exact scalar splice done；low signed prime--hybrid与 long-Mobius open | parent `30c41d8efee5d4d63cd100f6ec1050826c90051c`; V48=current working release | exact gcd crosswalk与 `R_AP=M_low+V_high-L_pf`；direct low scalar首选；`delta>1/200` signed character energy为更强充分门；arithmetic仍为 NO |
| 2026-08-11 | V47 | Bridge A / Gates A--B：local Euler paid；additive zero mode deleted；centered prime--hybrid covariance与 long-Mobius open | parent `10ad608f5487af3d2497adfbe226ded4f37e64a3`; V47=current working release | exact `A_d(0)=0`；full AP energy降为 centered covariance；prime/hybrid signed split与三车道 atlas；arithmetic仍为 NO |
| 2026-08-10 | V46 | Bridge A / Gates A--B：proper-factor local Euler carrier paid；all-residue AP--BDH residual与 long-Mobius open | parent `9737b62421770ed5f96c08f197488460833550d3`; V46=current working release | exact local-profile split；V29/BC支付 local component到 `1891/1920`；reciprocal occupancy energy `P^2`；新 whole-object AP variance gate `rho<33/100`；arithmetic仍为 NO |
| 2026-08-10 | V45 | Bridge A / Gates A--B：high conductor paid；low structured major与 long-Mobius open | release `9737b62421770ed5f96c08f197488460833550d3`; parent `1e19b2d` | primitive-conductor split；high spectrum `x^(213/128)`、margin `1/9600`；low principal/induced tower保留；arithmetic仍为 NO |
| 2026-08-10 | V44 | Bridge A / Gates A--B：transition split into principal mean and reciprocal variance; long-Möbius span open | rebased parent `d355325e5a287af1cef69509825799c9c6a0b5d5`; initial research baseline `be9d783536eeec36ab1c5a95525523f762c1d4d3` | exact gcd reduction删除 common phase conductor；transition拆成两项 endpoint gate；physical nonunit correction与background分别付到 `319/192`、`7171/4800`；arithmetic仍为 NO |
| 2026-08-10 | V43 | Bridge A / Gates A--B：small-factor alias deleted, zero axis returned, long-Möbius span open | parent `1f17878cfa62c40afab9620ee73536c7b5c9ea1e`; V43=current working release | complete centered Poisson删除 `d<=H/(4Q)` 非零 alias；对角返回给出 `D=A-L_pr*S+paid errors`；transition dual `23/2400`，Type II/reverse Type I whole-object theorem仍 OPEN；arithmetic仍为 NO |
| 2026-08-10 | V42 | Bridge A / Gate B：positive Gram gate exposed, proper-factor directional span open | parent `48b7bca985f35ccd4295b9ce44b55177488eef32`; V42=current working release | exact residual Gram与 spike/background cross term；V35 proper-factor lift、`95/48` occurrence diagonal与 dyadic MPD compiler；generic operator certificate需要 support `<=x^(273/400)`，full-active loss `2/3`；arithmetic仍为 NO |
| 2026-08-10 | V41 | Bridge A / Gate B：q-local model pier paid, residual row-Bessel span open | parent `fa68a37a73fe543983fb9c369498e53321bff080`; V41=current working release | exact split `s_q=m_q+rho_q`；三剩余类模型能量初等支付到 `37/16`、输出 `53/32`；主红叉缩为 residual row energy / row-Bessel，zero-axis A 仍独立；arithmetic 仍为 NO |
| 2026-08-09 | V40 | Bridge A / Gate B：constant-residue direction selected, row-Bessel pier open | parent `d6566e42ef1f5717de4dea5e80a0d4293fb3c712`; V40=current working release | scalar只读取 `s_q=sum_r d_q(r)`；primary norm从 full packet降为 q-row energy，diagonal付至 `95/48`，restricted row-Bessel阈值放宽到 `419/1200`；arithmetic 仍为 NO |
| 2026-08-09 | V39 | Bridge A / Gate B：packet-energy pier selected, Schatten toll exposed | parent `44a681ae29f1c13064fd672073eb7a7cd28694fd`; V39 historical release | exact block duality与absolute-mass barrier揭示 nuclear overpayment；generic/optimistic Schatten continuum均选择 `p=2`，主红叉改为 `kappa>1/200` packet energy；arithmetic 仍为 NO |
| 2026-08-09 | V38 | Bridge A / Gate B / K lane：canonical emitter built, Schatten pier open | parent `c89d3a0fc5201cba2ef27e37cf388ad763c4d59b`; V38 historical release | 以 double orthogonality、zero-axis factor 与 balanced SVD 精确关闭 emitter construction；主红叉收缩为 `omega<19/800` physical block-Schatten aggregate；arithmetic 仍为 NO |
| 2026-08-09 | V37 | Bridge A / Gate B / K lane：loss-budgeted shift packet | parent `2b199a9989f378666e5bc7b9bb8f2952015f75de`; V37 historical release | 将零损耗 `Q^(-31/32)` 口号改写为 exact packet 与 `omega<19/800` emitter contract；状态仍为 arithmetic NO |
| 2026-08-08 | V32 | Bridge A 桥头：single-scale residual oscillation | `66dcd9a08b1adb92b117941aae92b9a17ab6298f` | 首次将岛屿图保存为可更新文字地图并收录配套原图；未改变数学状态 |
