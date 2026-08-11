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

> **Fold-first transference for a signed Möbius pair emitter**

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

这些 source 均未直接证明当前 whole-object theorem。

### 2.3 主猜想

**CONJECTURAL**：

\[
 \left|\mathfrak F_x^{\rm mix}+\mathfrak F_x^{\rm bal}\right|
 \ll x^{1997/1200-\eta_L+o(1)}
 \quad\text{for some }\eta_L>0.
\]

该猜想与 V51 proof 的 literal physical coefficient、prime shell、hard product shell、
hybrid comparator 和 single outer sign 绑定。它不是把目标 scalar 换名；source-facing
emitter、fold order、Abel compiler 与 paid square row 已全部明确。

### 2.4 必须保留的 NO-GO 结果

1. **NO_GO** — orientation-first absolute reassembly destroys exact folded zeros。
2. **NO_GO** — generic multiplicative character large sieve only gives
   $x^{2+o(1)}$，距 numerator target 缺 $403/1200$。
3. **NO_GO** — bounded Siegel quality only gives constant relative decay for
   polynomial conductor，不自动产生 fixed $x$-power。
4. **NO_GO** — Dong--Robles--Zeindler arXiv:2601.00292v2 已撤回；作者记录
   equation (2.53) 漏掉 $L^2$，不能使用 claimed improvement。

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

下一次更新应优先回答：

1. pair-native character emitter能否 exact 编译成 BP/Pascadi 接受的 Kloosterman arrays；
2. mixed 与 balanced 是否必须共同估计，还是 source theorem允许无损 block orthogonality；
3. 能否先得到一个 standalone average theorem，即使暂时弱于 $1997/1200$ endpoint；
4. 哪个候选最先满足“成稿门槛 A”。
