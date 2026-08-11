# TPC big-road paper candidate ledger

更新时间：2026-08-11

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

当前成熟度：**OUTLINE_ONLY**。

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

V53 给出当前首选、更加 dispersion-native 的条件主猜想：对两个明确的 literal
row species证明

\[
 \mathsf H_{2RB}(1/3,1/3):\quad
 \mathcal E_A^{\rm row}\ll x^{1/3+o(1)}\mathcal D_A^{\rm row},
 \qquad
 \mathcal E_B^{\rm row}\ll x^{1/3+o(1)}\mathcal D_B^{\rm row}.
\]

两边 diagonal均已付到 `x^(95/48+o(1))`。该猜想条件性闭合 Bridge A 的 A、B
两桥墩，但它不对 arbitrary divisor-bounded arrays作断言，也不从有限 fixture取得
算术 credit。V52 PAD保留为独立猜想，不与 V53 假设叠加计算 saving。

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

下一次更新应优先回答：

1. 能否对 diagonal-completed pair row证明 one-`Q` restricted Bessel bound；
2. 能否对 V40 diagonal-deleted physical row证明同一 theorem species；
3. 能否从 joint character fourth moment或 dispersion identity导出上述两条 row bound；
4. BP/Pascadi local cells能否在不拆 compensation与 within-row cancellation的前提下
   合法 reassemble；
5. 若 row route失败，能否回到 V52 PAD取得 `kappa>1/400` 或总 saving `>1/200`；
6. 能否先得到一个 standalone row-energy average theorem，即使暂时弱于 endpoint；
7. 哪个候选最先满足“成稿门槛 A”。
