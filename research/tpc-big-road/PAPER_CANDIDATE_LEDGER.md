# TPC big-road paper candidate ledger

更新时间：2026-08-12

状态：**LIVING_PREPUBLICATION_LEDGER / NON_AUTHORITATIVE**

本文件与路线图平行维护，作用是把连续探索中的可发表材料从长篇 handoff 中逐步抽出。
它不是论文、不是 theorem trigger，也不改变 TPC_207_TRIGGER=false。正式数学状态仍以
当前 proof、checker、TPC_HANDOFF.md 页首及 current section 为准。

## 1. 记录规则

每一项只允许落入以下四类之一：

| 标签 | 含义 | 可进入未来论文的位置 |
|---|---|---|
| **PROVED** | exact identity、support、compiler、已付款误差或完整证明 | theorem / lemma / proposition |
| **SOURCE_BACKED_CONDITIONAL** | 一手文献定理可作局部引擎，但全局 attachment 尚有明确假设 | conditional proposition / related work |
| **CONJECTURAL** | 路线真正需要的新渐近定理，量词与推论链已经写清 | conjecture / main open problem |
| **NO_GO** | 某个精确接口被反例、量纲或 source hypotheses 排除 | obstruction / design principle |

禁止把 checker PASS、有限 fixture、路线图箭头、启发式 cancellation 或“目前没找到反例”
写成算术 theorem。

## 2. 第一篇小论文候选

暂定题目：

> **Fold-first transference and compensated dilation for a signed Möbius pair emitter**

候选类型：结构性解析数论短文 / research note。

当前成熟度：**STRUCTURAL_LEMMA_PACKAGE_READY / MAIN_ARITHMETIC_THEOREM_OPEN**。

### 2.1 可直接进入正文的已证骨架

1. **PROVED** — V43 proper-factor centered Poisson transference：
   small-$d$ nonzero aliases exact vanish，但 zero axis 原样返回，并给
   Gate-B = Gate-A - $L_{\rm pr}S$ + paid errors。
2. **PROVED** — V50 saving-matched moving conductor cut：
   每个预声明 $0<\delta<1/9600$ 都自行支付 complement 到
   $x^{1997/1200-\delta+o(1)}$。
3. **PROVED** — V51 unordered two-orientation fold：
   mixed 与 balanced numerator 的 exact formulas、square row、$U^2<x/2$ support。
4. **PROVED** — V51 rank-two numerator plus one-dimensional Abel compiler。
5. **PROVED** — V51 diagonal-completed pair row与 V43 Gate-A numerator 的 exact crosswalk。
6. **PROVED** — V51 nonprincipal-character/Fourier one-aggregate emitter。
7. **PROVED** — finite orientation-support mismatch，证明“先逐方向 Poisson、后折叠”
   不是合法保持 cancellation 的 compiler。
8. **PROVED** — V52 dual coefficient interface：同一 non-square folded coefficient
   同时等于 pair-native `Omega_U` sum与 truncated-sieve residual减 square row。
9. **PROVED** — V52 compensated prime-dilation identity：divisibility row、physical
   diagonal与 unit principal mean进入一个 signed bracket，自然 length为 `H/q`。
10. **PROVED** — V52 character-packet Hilbert identity与 endpoint simplex
    `eta_PAD=kappa+(delta_B+delta_W)/2-1/400`。
11. **PROVED** — V52 reverse-Chen semiprime slice及 equal-norm parallel/orthogonal
    marginal-only obstruction。
12. **PROVED** — V53 completed pair-row compression：先在每个 prime modulus内保留
    physical diagonal、unit principal mean与 signed off-diagonal，再只对 prime shell
    使用 Cauchy。
13. **PROVED** — V53 pair collision diagonal
    `D_A^row<<x^(95/48+o(1))` 与 endpoint law
    `|F_circle|<<x^(143/96+tau_A/2+o(1))`。
14. **PROVED** — V53 selected one-`Q` benchmark：`tau_A=1/3` 给
    row energy `x^(37/16+o(1))`、numerator `x^(53/32+o(1))` 与
    strict margin `19/2400`。
15. **PROVED** — V53 symmetric two-gate compiler：同一 restricted row-Bessel
    theorem species分别作用于 diagonal-completed pair row和 V40 diagonal-deleted
    physical row；若两边 `tau=1/3`，V43 条件性给 physical exponent `95/96`。
16. **PROVED** — V54 paired-row difference identity：
    `P_q-C_q=kappa_q*S_physical-E_q`，其中 full-beta square row与 unit omission均
    逐项保留。
17. **PROVED** — V54 difference error payment：
    `sum_q|E_q|^2<<x^(95/48+o(1))`，unit omission单独只到 `x^(5/3+o(1))`。
18. **PROVED** — V54 longitudinal extractor：沿 `kappa_q=(q-2)/(q-1)` 投影以
    `x^(79/96+o(1))` 误差直接恢复 physical residual。
19. **PROVED** — V54 transverse identity：`Pi_perp P-Pi_perp C=-Pi_perp E`，故
    pair/physical rows共享一个 transverse theorem species。
20. **PROVED** — V54 two-out-of-three terminal compiler：pair row、physical row与
    physical scalar三者任意两个同尺度 bounds推出第三个；V53 symmetric package因此
    是 terminal package而非更容易的双 preliminary gate。
21. **PROVED** — V55 every-modulus replica：对 prime shell内每个预声明模数，
    `S_q^rep=(P_q-C_q)/kappa_q=S_physical+O(x^(79/96+o(1)))`；这是逐模数
    pointwise identity，不借跨模数平均。
22. **PROVED** — V55 general modulus-operator dichotomy：任意线性算子 `T` 满足
    `T(P-C)=S_physical*T(kappa)-T(E)`；`T(kappa)=0` 时只看 transverse paid error，
    `T(kappa)!=0` 时其 longitudinal estimator 已直接估计终点。
23. **PROVED** — V55 minimax linear extraction：在 `l^2` error ball内，约束
    `<a,kappa>=1` 的唯一最优线性权为 `a*=kappa/||kappa||_2^2`，V54 extractor不是
    任意选择，而是当前 information model的 minimax readout。
24. **PROVED** — V55 PSD/TT-star firewall：正半定二次型若 annihilate `kappa`，只控制
    transverse deck；若保留正的 `kappa` energy，其 longitudinal部分与 physical scalar
    terminal-equivalent，不存在第三类 post-`q` preliminary gate。
25. **PROVED** — V55 maximal-shell Abel transfer：若 V51 folded partial prime-shell
    `F(Y)=sum_{Q<q<=Y}qP_q` 对所有 `Y` 有 fixed-power maximal bound，则 Abel summation
    精确转移到最终 longitudinal scalar；只控制 full-shell endpoint不足，有限反例已锁定。
26. **PROVED** — V56 one-modulus absolute envelope：对同一 literal folded row，
    `q|P_q|<<x^(53/32+o(1))`，到 Gate-A numerator target 的精确余量为 `19/2400`。
27. **PROVED** — V56 pruned dyadic maximal compiler：预声明连续 leaves、aligned
    power-of-two nodes后，每个 prime-shell prefix精确分解为 `O(log Q)` 个完整 nodes
    加至多一个 full leaf与一个 partial leaf。
28. **PROVED** — 短 leaf absolute payment：若 `0<lambda<19/2400`，每个含至多
    `x^lambda` 个素模数的 leaf保留 saving `19/2400-lambda`；标准选择
    `lambda=19/4800` 留 `19/4800`。
29. **PROVED** — tree-to-maximal transfer：一个对全部 predeclared large nodes统一的
    signed block theorem只损失 `O(log Q)=x^o(1)`；反向每个 node是两个 prefixes之差，
    故二者在付清短 leaves后 power-equivalent，常数二是 sharp。
30. **PROVED** — V56 endpoint ledger：若 block saving为 `eta_D`，则 maximal saving可取
    `eta_M<min(eta_D,19/2400-lambda)`；再与 square row、boundary strip及 Gate B合并时
    全部 strict margins均显式保留。
31. **PROVED** — tree operations始终作用于完整 folded compensated row；只有在
    whole-node theorem之后才允许 `O(log Q)` triangle，因此不重犯 V51
    orientation-first absolute reassembly。
32. **PROVED** — V57 longitudinal root-anchor identity：对共同带 `q` 权的
    `A(Y),C(Y),E(Y),K(Y)`，令 `r_Y=K(Y)/K_*`，则
    `A(Y)-r_Y A_* = C(Y)-r_Y C_* - E(Y)+r_Y E_*`；physical mode逐 prefix exact取消。
33. **PROVED** — V57 prefix error payment：unit omission贡献 `x^(4/3+o(1))`，
    square row贡献并控制到 `x^(143/96+o(1))`，到 numerator target余量
    `419/2400`。
34. **PROVED** — Gate-B row-Bessel自动 maximalization：若
    `sum_q|C_q|^2<<x^(95/48+tau_B+o(1))`，则统一于全部 endpoints，
    `sup_Y|sum_(q<=Y)qC_q|<<x^(143/96+tau_B/2+o(1))`。
35. **PROVED** — V57 root-plus-transverse conditional compiler：一个 V51 full-shell
    `H_fold(eta_L)` 与一个 `tau_B<419/1200` 的 Gate-B row-Bessel同时推出全部
    Gate-A prefixes与 physical endpoint；saving可取
    `min(eta_L,419/2400-tau_B/2)` 以下任意固定值。
36. **PROVED** — selected benchmark `tau_B=1/3` 给 Gate-B maximum
    `x^(53/32+o(1))` 与 physical output `x^(95/96+o(1))`，strict margin
    `19/2400`；Gate B只使用一次，兼付 full-shell与 prefix。
37. **PROVED / ROUTE RETYPE** — V56 all-node tree仍为合法 Gate-A fallback，但在
    selected root-plus-row package中不再需要；V53 symmetric two-row Bessel在 Gate-A
    轴也比 V57 所需 root scalar更强。三种 sufficient packages不作 exponent拼接。

### 2.2 可写成条件命题的局部引擎

1. **SOURCE_BACKED_CONDITIONAL** —
   Blomer--Pascadi arXiv:2607.24311v1, Theorem 1.1：
   fixed-modulus critical bilinear Kloosterman cell 的 $c^{-1/32+o(1)}$ saving。
2. **SOURCE_BACKED_CONDITIONAL** —
   Pascadi arXiv:2404.04239v3：
   sparse-Fourier exceptional-spectrum large sieve 与 incomplete Kloosterman
   corollaries。
3. **SOURCE_BACKED_CONDITIONAL** —
   Bettin--Chandee arXiv:1502.00769v1：
   exact separated reciprocal-fraction cell；只在 literal coefficient compiler
   和 aggregate norm 已证明后调用。
4. **SOURCE_BACKED_CONDITIONAL** —
   Zheng arXiv:2512.22798v1：simultaneous progression architecture；其 fixed
   residues、`theta<=7/36` 或 `2/23` 与 coefficient hypotheses尚未覆盖 V53。
5. **SOURCE_BACKED_CONDITIONAL** —
   Milićević--Qin--Wu arXiv:2511.07550v1, Theorem 1.1：fixed-`q` separable bilinear
   `Kl_2` cell允许任意局部系数，但尚无 literal pre-`q` fold/packet compiler和 maximal
   prime-shell reassembly。
6. **SOURCE_BACKED_CONDITIONAL** —
   Kerr--Shparlinski--Wu--Xi arXiv:2204.05038v5：fixed-modulus Kloosterman arrays的
   bilinear bounds；同样只可作 post-emitter局部引擎，不能支付 V55 whole-object bridge。
7. **SOURCE_BACKED_CONDITIONAL / ARCHITECTURE ONLY** —
   Lewko--Lewko arXiv:1111.6190v2, Lemmas 16 and 23--24：dyadic interval
   decomposition与 variational maximal large sieve说明 endpoint motion可只付对数；
   其 maximal axis是 inner coefficient index，不是 literal outer-`q` folded row。
8. **SOURCE_BACKED_CONDITIONAL / ARCHITECTURE ONLY** —
   Ramaré arXiv:2303.04409v2, Lemmas 3.1--3.2：inner-index maximal large sieve及
   smooth nonnegative modulus average；没有 V51 signed pair coefficient、physical
   hybrid factor或 canonical outer-`q` block reassembly。
这些 source 均未直接证明当前 whole-object theorem。

### 2.3 主猜想

V51 scalar form仍为 **CONJECTURAL**：

\[
 \left|\mathfrak F_x^{\rm mix}+\mathfrak F_x^{\rm bal}\right|
 \ll x^{1997/1200-\eta_L+o(1)}
 \quad\text{for some }\eta_L>0.
\]

该猜想与 V51 proof 的 literal physical coefficient、prime shell、hard product shell、
hybrid comparator 和 single outer sign 绑定。它不是把目标 scalar 换名；source-facing
emitter、fold order、Abel compiler 与 paid square row 已全部明确。

V52 将它升级成更可审计的 packet package

\[
 \mathsf H_{\rm PAD}(\delta_B,\delta_W,\kappa),
 \qquad
 \kappa+\frac{\delta_B+\delta_W}{2}>\frac1{400}.
\]

首选 heuristic 是 diagonal-scale marginals加 `kappa>1/400` 的 joint angular
dispersion；zero-angle fallback要求 `delta_B+delta_W>1/200`。这是当前第一篇候选
最接近 standalone main conjecture 的版本，但仍没有 primary-source proof。

V53 给出一个 dispersion-native 的条件主猜想：对两个明确的 literal row species证明

\[
 \mathsf H_{2RB}(1/3,1/3):\quad
 \mathcal E_A^{\rm row}\ll x^{1/3+o(1)}\mathcal D_A^{\rm row},
 \qquad
 \mathcal E_B^{\rm row}\ll x^{1/3+o(1)}\mathcal D_B^{\rm row}.
\]

两边 diagonal均已付到 `x^(95/48+o(1))`。V54 证明这个 symmetric package已经
隐含终端 physical scalar，因此它不再被推荐为两个独立 preliminary conjectures。
当前主猜想拆成正交的两项：一个 common transverse row-variance theorem，以及一个
沿 `kappa` 的 direct signed longitudinal theorem；后者在 paid error后与 physical
endpoint等价。V52 PAD与 V51 direct scalar保留为独立猜想，不叠加计算 saving。

V55 把这条判断推进为一般 operator theorem：所有 post-`q` modulus engineering只有
`T(kappa)=0` 与 `T(kappa)!=0` 两类。前者至多支付 common transverse Gate B；后者已经
是 terminal readout。因此当前首选主猜想不再表述为一个新的 `q`-space norm，而是前移为
以下两个 pre-compression 大桥墩之一：

1. **CONJECTURAL** — V51 maximal fold-first theorem：对同一个 signed folded emitter，
   uniformly in `Q<Y<=2Q` 控制 partial prime shell；
2. **CONJECTURAL** — V52 pre-`q` PAD theorem：在压成 modulus coordinate之前证明
   packet angular dispersion，并满足
   `(delta_B+delta_W)/2+kappa>1/400`；
3. **CONJECTURAL** — 与上面任一路共用的 common transverse theorem。

这三项是路线接口，不是新增算术结论；global Siegel-quality unbounded world仍保留为
独立条件出口。

V56 进一步把第 1 项压成单一、可量词化的 **CONJECTURAL** block theorem。令
`lambda in (0,19/2400)`，把按大小排序的 prime shell预先分成至多 `x^lambda`
个模数的 leaves，并令 `B` 遍历至少两个 leaves组成的 aligned dyadic nodes。当前最窄
Gate-A 猜想是存在 fixed `eta_D>0`，uniformly in all such `B`,

\[
 \left|\sum_{q\in B}qP_q\right|
 \ll x^{1997/1200-\eta_D+o(1)}.
\]

它条件性推出 maximal V51 theorem，saving可取
`eta_M<min(eta_D,19/2400-lambda)`；反向 maximal theorem以 factor two控制每个 node。
这不是比 full shell theorem自动更容易的声明，而是精确标识 moving endpoint额外要求的
全部 arithmetic content。V42 common transverse Gate B仍须独立证明；V52 PAD保持平行
后备，三条 route不得拼接 exponent credit。

V57 将 selected package再次收窄。它不再把每个 Gate-A large node当作独立猜想，
而只保留两个 whole-object piers：

1. **CONJECTURAL** — V51 full-shell signed root
   `H_fold(eta_L)`，即 mixed-plus-balanced nonsquare fold有一个 fixed power saving；
2. **CONJECTURAL** — V53 full-beta diagonal-deleted Gate-B restricted row-Bessel
   `H_B-RB(tau_B)`，其中 `tau_B<419/1200`。

V57 exact root anchor证明这两项已足以控制所有 Gate-A prefixes，并由
`S=(A_*-C_*+E_*)/K_*` 直接读出 physical scalar。标准 `tau_B=1/3` 留
`19/2400`。这是真正的 theorem-burden reduction，但两项猜想本身仍未被证明，故
不改变 arithmetic status。V56 tree、V52 PAD与 V53 symmetric two-row package均保留为
平行较强 sufficient formulations。

### 2.4 必须保留的 NO-GO 结果

1. **NO_GO** — orientation-first absolute reassembly destroys exact folded zeros。
2. **NO_GO** — generic multiplicative character large sieve only gives
   $x^{2+o(1)}$，距 numerator target 缺 $403/1200$。
3. **NO_GO** — bounded Siegel quality only gives constant relative decay for
   polynomial conductor，不自动产生 fixed $x$-power。
4. **NO_GO** — Dong--Robles--Zeindler arXiv:2601.00292v2 已撤回；作者记录
   equation (2.53) 漏掉 $L^2$，不能使用 claimed improvement。
5. **NO_GO** — diagonal-scale marginal BDH 加 ordinary Cauchy恰差 `1/400`。
6. **NO_GO** — marginal energies不决定 packet angle；equal-norm finite fixture同时
   允许完全平行与完全正交。
7. **NO_GO** — Zheng/Drappeau/Wright 的 fixed-residue/product interfaces不能直接
   代替 V52 moving compensated product covariance。
8. **NO_GO** — ordinary polarized marginal BDH 会把未知 physical cross-diagonal
   原样作为 main term返回；除非同时证明其与 off-diagonal covariance的 signed
   cancellation，否则不能替代 completed pair-row theorem。
9. **NO_GO** — 小 global scalar或有利 PAD angle不能推出小 row energy；跨模数
   cancellation已被 V53 interface有意舍弃。
10. **NO_GO** — separate character second moments不能推出 V53 所需 joint product
    fourth moment。
11. **NO_GO** — centered-modulus BDH会删除 `kappa` longitudinal mode；它至多
    控制 V54 transverse deck，不能支付 physical residual。
12. **NO_GO** — special Dirichlet-L fourth-moment theorems使用 approximate-functional-
    equation coefficients与自己的 diagonal cancellation，不能直接替代 literal
    folded pair / prime-hybrid packets。
13. **NO_GO** — symmetric two-row Bessel不是“先证明两个容易 row theorem、再到终点”
    的 shortcut；V54 two-out-of-three compiler说明其纵向部分已包含终点本身。
14. **NO_GO** — 任何 annihilate `kappa` 的 centered/BDH/PSD modulus operator都会
    精确删除 terminal mode；它不能从 transverse estimate恢复 physical scalar。
15. **NO_GO** — 任何保留 `kappa` 的 bounded linear/PSD/TT-star modulus operator都没有
    免费 condition-number优势：`||T||/||T(kappa)||>=1/||kappa||`，其估计已是终点等价。
16. **NO_GO** — 只证明 V51 full prime shell的总和小，不能推出 weighted longitudinal
    Abel scalar小；有限 partial-sum反例给出 exact separation。
17. **NO_GO** — Harper centered BDH、Runbo Li prime-AP以及 Zheng simultaneous-AP均是
    wrong object或删掉 longitudinal mode，不能作为 V55 direct attachment。
18. **NO_GO** — Dong--Robles--Zeindler arXiv:2601.00292v2 已由作者撤回；其说明明确
    指出 equation (2.53) 缺失 `L^2` 因子，claimed improvement失效，不计 theorem credit。
19. **NO_GO** — V51 full-shell theorem不能推出 maximal theorem；`q=(5,7)`,
    `P=(7,-5)` 给 `sum qP_q=0`，但 earlier prefix为 `35` 且 longitudinal sum为 `13/12`。
20. **NO_GO** — dyadic decomposition本身不制造 cancellation；若各模数同号，单模数
    envelope在整 shell累积到 `x^(191/96+o(1))`，远高于目标。large-node theorem必须
    使用 literal arithmetic signs与完整 within-row compensation。

## 3. 第二篇候选：endpoint-matched exceptional spectrum compiler

暂定题目：

> **Saving-matched conductor cuts and the two Siegel-quality worlds**

当前成熟度：**CONDITIONAL_NOTE_CANDIDATE**。

可用内容：

1. **PROVED** — V45--V50 moving-cut energy ledger；
2. **PROVED** — bounded/unbounded quality 的逻辑穷尽二分；
3. **SOURCE_BACKED_CONDITIONAL** — Matomäki--Merikoski fixed-$h=2$ correlation
   在 unbounded-quality sequence 上给 direct TPC exit；
4. **CONJECTURAL** — bounded-quality endpoint-matched signed core；
5. **NO_GO** — per-scale Landau--Page singleton 不能提升为 global unbounded sequence。

该候选目前缺一个独立于 TPC endgame、足以构成主定理的 bounded-world结果，所以暂不成稿。

## 4. 第三篇候选：local Euler carrier and inverse-residue corridor

暂定题目：

> **Zero-axis cancellation and a short inverse-residue corridor**

当前成熟度：**NEAR_STRUCTURAL_NOTE**。

核心材料来自 V28--V30：

1. **PROVED** — local Euler profile的 exact zero-axis cancellation；
2. **PROVED** — reduced-radical Fourier/CRT emitter；
3. **PROVED** — selected-MASTER radical $L^2$ envelope；
4. **SOURCE_BACKED_CONDITIONAL** — Bettin--Chandee corridor exponent
   $1891/1920$，到 $399/400$ 有 $121/9600$ margin；
5. **CONJECTURAL** — same tagged residual的 independent major/minor whole-object
   attachment。

如果未来能把第 5 项缩成一个不依赖 TPC 特殊目标的抽象 theorem，这一候选最可能先形成
真正的小论文。

## 5. 成稿门槛

满足下列任一组条件后，启动 paper-plan -> paper-write -> paper-compile，而不是继续只写
handoff。

### 门槛 A：结构性短文

1. 一个 standalone theorem statement；
2. proof 不依赖未声明的 TPC hypothesis；
3. 至少一个非平凡应用或一个 sharp obstruction；
4. 所有 source locators 与版本锁定；
5. checker 只作有限公式 QA，不冒充 theorem proof。

### 门槛 B：条件性路线论文

1. 所有 conjectural hypotheses 列在摘要和主定理中；
2. conditional implication chain完整；
3. 至少一个 source-backed local engine真正附着到 literal object；
4. numerical exponent ledger有 strict positive margin；
5. 明确说明不构成 unconditional TPC proof。

### 门槛 C：完整 Bridge-A 论文

1. Gate A 与 Gate B 对同一 physical scalar均有 fixed-power theorem；
2. exact reassembly、tails、normalization、nonunits、zero axis全部付款；
3. strict $1/400$ endpoint真实支付；
4. 通过独立数学审阅后才允许编号。

## 6. 版本里程碑

| 日期 | 版本 | 新增可发表单元 | 状态 |
|---|---|---|---|
| 2026-08-10 | V43 | proper-factor Poisson transference 与 zero-axis return | **PROVED** |
| 2026-08-11 | V50 | saving-matched moving cut 与 Siegel-quality dichotomy | **PROVED + CONDITIONAL + CONJECTURAL** |
| 2026-08-11 | V51 | fold-first pair emitter、rank-two/Abel compiler、orientation NO-GO | **PROVED + CONJECTURAL** |
| 2026-08-11 | V52 | compensated pair dilation、reverse-Chen slice、endpoint simplex、marginal-only angle obstruction | **PROVED + SOURCE_BACKED_CONDITIONAL + CONJECTURAL + NO_GO** |
| 2026-08-11 | V53 | completed pair rows、paid collision diagonal、one-`Q` endpoint与 symmetric two-gate schema | **PROVED + SOURCE_BACKED_CONDITIONAL + CONJECTURAL + NO_GO** |
| 2026-08-11 | V54 | paired-row mode diagonalization、paid transverse difference、terminal longitudinal firewall | **PROVED + SOURCE_BACKED_CONDITIONAL + CONJECTURAL + NO_GO** |
| 2026-08-12 | V55 | every-modulus replicas、一般 operator/minimax/PSD dichotomy、maximal-shell transfer与 pre-`q` route pivot | **PROVED + SOURCE_BACKED_CONDITIONAL + CONJECTURAL + NO_GO** |
| 2026-08-12 | V56 | one-modulus envelope、pruned dyadic maximalization、leaf margin、reverse interval equivalence与 canonical-block conjecture | **PROVED + SOURCE_BACKED_ARCHITECTURE + SOURCE_BACKED_CONDITIONAL + CONJECTURAL + NO_GO** |

下一次更新应优先回答：

1. 能否对 V56 预声明的全部 large dyadic nodes证明同一个 uniform literal block
   theorem；这是当前 Gate A 的第一大门；
2. 能否在 V52 packet层直接证明
   `(delta_B+delta_W)/2+kappa>1/400` 的 joint angular dispersion；
3. 能否对任一 literal row的 transverse projection证明 one-`Q` variance，并由 V54
   paid difference传给另一 row；
4. BP/MQW/KSWX local cells能否在不拆 compensation与 within-row cancellation的前提下
   合法 reassemble成上述 pre-`q` theorem；
5. unbounded Siegel-quality world能否沿既有 source-backed fixed-`h=2` 通道直接退出；
6. 能否把 V54--V55 exact diagonalization、minimax extractor与 maximal Abel transfer
   抽象成一篇不依赖 TPC终点的 standalone structural note；
7. 能否把 V56 maximalization与一个非 TPC-specific weighted endpoint application组合，
   使其达到 standalone structural note 的“成稿门槛 A”；
8. 哪个候选最先满足“成稿门槛 A”。
