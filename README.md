# Exploring Prime Distribution via Dynamical Methods

## 1. Exploring the Hilbert–Pólya Conjecture
- **A**: Construct a canonical dynamical spectral determinant.
- **B**: Complete non-self-adjoint dynamical objects into scattering/unitary objects that preserve the time direction.
- **C**: Obtain a genuinely self-adjoint operator and derive the $T \log T$ counting law intrinsically.
- **D**: Extract prime powers and von Mangoldt weights from the dynamical trace.
- **E**: Prove that the spectral divisor coincides exactly with the divisor of the completed zeta function.

## 2. Exploring the Twin Prime Conjecture

当前主线状态：TPC-287 承接 TPC-286，把 physical deleted-diagonal prime shell 按素数
拆成可审计的 signed components。对七个明确声明的 shell anchor（恰含 1--7 个素数）、
六个 frozen source baselines 与两个 kernel exponents，形成 84 rows / 336 components：
所有 component intervals 均 sign-separated，57 行为 mixed-sign，retention upper bound
低于 `1/2`、`1/4`、`1/10` 的行数分别为 31、22、8；leave-one-prime-out 有 48 个非零
sign flips 与 12 个 zero remainders。TPC-287 严格证明 finite shell/linear attachment
的 `g_shell=sum_q g_q`、`C_shell=sum_q C_q`，并给出 conditional interval envelope。
这是新的 `PROVED_EXACT` additive structure 加 `NUMERICALLY_CERTIFIED_FINITE` cancellation
depth ledger；growing-shell stability、source-control uniformity、arithmetic `L2`、
fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC287_SHELL_ADDITIVITY = PROVED_EXACT_FINITE
TPC287_ATTACHMENT_ADDITIVITY = PROVED_EXACT_FINITE
TPC287_COMPONENT_LEDGER = NUMERICALLY_CERTIFIED_FINITE_336_COMPONENTS
TPC287_MIXED_SIGN_ROWS = NUMERICALLY_CERTIFIED_FINITE_57_OF_84
TPC287_RETENTION_THRESHOLDS = NUMERICALLY_CERTIFIED_FINITE_31_22_8
TPC287_LEAVE_ONE_OUT = NUMERICALLY_CERTIFIED_FINITE_48_FLIPS_12_ZERO
TPC287_GROWING_SHELL_STABILITY = OPEN
TPC287_SOURCE_CONTROL_UNIFORMITY = OPEN
TPC287_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC287_FIXED_POWER_CREDIT = 0
TPC287_FULL_GATE_B = OPEN
TPC287_TWIN_PRIME_RESULT = NONE
```

当前主线状态：TPC-286 承接 TPC-285，把 centered residue block 与 physical
deleted-diagonal operator 之间的缺项精确拆开。对有限 prime shell，定义含对角项的
`g_full`、显式对角修正 `g_diag` 与物理输出 `g_phys`，严格证明
`g_phys=g_full-g_diag`，并由 attachment 的线性得到 `C_phys=C_full-C_diag`。
在 TPC-284 的全部 72 个 schedule-control rows 上，三类 component interval 全部
sign-separated：full 49 negative/23 positive，diagonal 34/38，physical 60/12；
full-versus-physical 有 15 个 sign flips，对角修正与 physical 相反 30 行，严格
大于 physical 绝对幅度 21 行。这是新的 `PROVED_EXACT` diagonal-split structure
加 `NUMERICALLY_CERTIFIED_FINITE` sensitivity ledger；asymptotic diagonal dominance、
signed full-shell cancellation、arithmetic `L2`、fixed-power credit、full Gate B 与
twin-prime conclusion 仍 OPEN/NONE。

```text
TPC286_ATTACHMENT_SPLIT = PROVED_EXACT_LINEARITY
TPC286_COMPONENT_SIGN_LEDGER = NUMERICALLY_CERTIFIED_FINITE_72_ROWS
TPC286_FULL_VS_PHYSICAL_FLIPS = NUMERICALLY_CERTIFIED_FINITE_15_ROWS
TPC286_DIAGONAL_OPPOSITION = NUMERICALLY_CERTIFIED_FINITE_30_ROWS
TPC286_DIAGONAL_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_21_ROWS
TPC286_ASYMPTOTIC_DIAGONAL_DOMINANCE = OPEN
TPC286_FIXED_POWER_CREDIT = 0
TPC286_FULL_GATE_B = OPEN
```

当前主线状态：TPC-285 承接 TPC-284，解释 prime-shell 控制敏感性背后的局部结构。
对奇素数 `q`，centered residue block 精确分解为
`B_q=R_q(I-11^T/(q-1))R_q^T`，rank 至多 `q-2`；但物理算子删除 diagonal 后，
在所有非零 residue class 出现时，active block 精确恢复 full rank。对 20 个
registered prime/exponent rows，kernel Schur product 也由模 `1000000007` 的独立
精确证书认证为 full active rank。这是新的 `PROVED_EXACT` analytic structure 加
`NUMERICALLY_CERTIFIED_FINITE` rank obstruction；它不提供 signed full-shell cancellation、
arithmetic `L2`、fixed-power credit、full Gate B 或 twin-prime conclusion。

```text
TPC285_RESIDUE_FACTORIZATION = PROVED_EXACT
TPC285_DELETED_DIAGONAL_FULL_RANK = PROVED_EXACT_UNDER_FULL_CLASS_COVERAGE
TPC285_KERNEL_SCHUR_FULL_RANK = NUMERICALLY_CERTIFIED_FINITE_20_ROWS
TPC285_LOW_RANK_TRANSFER = REFUTED_AS_DIRECT_SHORTCUT
TPC285_FIXED_POWER_CREDIT = 0
TPC285_FULL_GATE_B = OPEN
```

当前主线状态：TPC-284 承接 TPC-283，把 unrestricted zeroing obstruction 收紧为六类
明确的 finite schedule controls：`H-2/H+2`、`z-1/z+1`、`Q-1/Q+1`。在六个
registered scales 与两个 kernel exponents 上形成 72 行 literal-source control atlas，
outward interval replay 认证 60 个负附着、12 个正附着、0 个 crossing；但有 8 行相对
TPC-283 baseline 发生 sign flip，最弱 controlled `rho^2` 下界约为 `1.4118e-5`。
这是真实的 `NUMERICALLY_CERTIFIED_FINITE` 控制图谱与 sign-stability obstruction，
不是 exhaustive admissible-source theorem 或渐近稳定性定理；arithmetic `L2`、
fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC284_CONTROL_ATLAS = NUMERICALLY_CERTIFIED_FINITE_72_ROWS
TPC284_CONTROL_SIGN_CENSUS = 60_NEGATIVE_12_POSITIVE_0_CROSSING
TPC284_SIGN_FLIP_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_8_FLIPS
TPC284_ASYMPTOTIC_CONTROL_STABILITY = OPEN
TPC284_FIXED_POWER_CREDIT = 0
TPC284_FULL_GATE_B = OPEN
```

当前主线状态：TPC-283 承接 TPC-282，将有限 attachment 读成一个精确的 stability
radius。对非零 `S`，若 `C=<w,S>`、`W=||w||^2`、`Y=||S||^2`，则到零附着超平面的
最短相对距离平方严格等于 `C^2/(WY)`，唯一归零点为 `w-(C/Y)S`。转移 TPC-282 的
12 行后，所有行的归零半径都小于 `3/10`，其中 6 行小于 `1/10`。这是
`PROVED_EXACT` 几何定理加 `NUMERICALLY_CERTIFIED_FINITE` 脆弱性审计；归零方向不
保证属于 literal prime source，因此 admissible-source stability、arithmetic `L2`、
fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。下一关只扫描
cutoff/clock/shell 等自然 source controls。

```text
TPC283_ZEROING_RADIUS = PROVED_EXACT
TPC283_FINITE_VULNERABILITY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC283_UNRESTRICTED_ADVERSARY = INFORMATION_MODEL_ONLY
TPC283_ADMISSIBLE_LITERAL_SOURCE_STABILITY = OPEN
TPC283_FIXED_POWER_CREDIT = 0
TPC283_FULL_GATE_B = OPEN
```

当前主线状态：TPC-282 承接 TPC-281，首次把 arithmetic interface 的 readout 换回
literal V59 source 本身。对 `S=(I-P_3)A beta`、`w_perp=(I-P_3)w` 定义
`C=<w_perp,S>` 与 `rho^2=C^2/(||w_perp||^2||S||^2)`，在六个 registered scales、
两个 kernel exponents 的 12 行上，outward interval replay 认证 `C` 全部与零分离
（11 negative、1 positive），但最弱 `rho^2` 仅约 `3.36e-5`。这是
`NUMERICALLY_CERTIFIED_FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK` 的明确 source-level
进展；不升级为 uniform asymptotic nondegeneracy、arithmetic `L2`、fixed-power credit、
full Gate B 或 twin-prime conclusion。下一关是量化 attachment 的最小归零扰动与符号稳定性。

```text
TPC282_SOURCE_ATTACHMENT = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC282_SOURCE_SIGN = 11_NEGATIVE_1_POSITIVE_FINITE
TPC282_UNIFORM_ASYMPTOTIC_NONDEGENERACY = OPEN
TPC282_FIXED_POWER_CREDIT = 0
TPC282_FULL_GATE_B = OPEN
```

当前主线状态：TPC-281 承接 TPC-280，把假设性的 arithmetic `L2` 明确类型化为
`A_X:H_X -> ell^2(I_X)` 的 operator interface。若
`||A_X||_(2->2)<=K X^(-sigma)`、`G/D<=Q_X` 且 `D<=d_+X^a`，则严格得到
`||A_X S||_2^2<=K^2 X^(-2sigma)Q_XD`；代入 TPC-280 的 two-term budget 后得到
`K^2 d_+(B+ell/d)X^(a-2sigma-kappa)`，其中 `kappa=min(gamma,delta)`，scalar
readout 再由 contraction 控制。另一方面，`R^2` 中 equal-norm 的 parallel/perpendicular
rank-one functionals 对同一 packet sum 给出 `G^2` 与 `0` 的 attachment，精确否定
“geometry/operator norm 自动识别 arithmetic attachment”。4 个 packet、4 个 interface
cases 与 TPC-280 的 12-row transfer 已通过 independent/stress/Bridge-B checks；literal
source arithmetic `L2`、typed nondegeneracy、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。

当前主线状态：TPC-280 承接 TPC-279 的 exact deficit criterion，研究 source bound
中同时出现的 multiplicative main term 与 additive leakage。若
`D>=dX^a` 且 `G<=B X^(-gamma)D+ell X^(a-delta)`，证明归一化后的 exact two-term
bound `G/D<=B X^(-gamma)+(ell/d)X^(-delta)`，并将可用 exponent 限制为
`kappa=min(gamma,delta)`；同一编译器给出 `eta_eff=max(0,eta_D-kappa/2)` 与 strict
endpoint test。等号 family 证明 two-term denominator 在给定信息模型下 sharp，
`delta<gamma` 的慢 leakage 是明确 obstruction。6+4+4 个 exact rational fixtures
及 TPC-279 的 12-row coordinate transfer 已通过 independent/stress checks，但仍
不产生 literal arithmetic `L2` 或 fixed-power credit。下一关是 typed arithmetic
`L2`/full Gate-B interface audit；full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

TPC-279 将 TPC-278 暴露的缺口精确化为四包 Hilbert 空间中的
coherence-to-gain theorem。证明 `q=G/D`、`Delta=1-q=-2E/D` 给出的 gain
条件是充要的，并证明 pairwise absolute coherence 的 sharp envelope
`q<=min(4,1+3mu)`；正交包与 near-cancellation scalar family 分别构成 no-power
与 arbitrarily-large-gain adversaries。对 TPC-278 的 12 行做 exact reciprocal
interval transfer，得到 8 个 positive-deficit、4 个 negative-deficit rows，完成
坐标级验证但不产生渐近或 arithmetic credit。下一关是把 additive leakage 纳入
source-to-margin endpoint compiler；fixed-power credit 仍为 0，arithmetic `L2`、
full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

当前主线状态：TPC-275 承接 TPC-274，在同一个锁定的 literal V59 finite physical
operator 上把四个实际 source-block 输出包保留下来，定义 packet Gram、四点 DFT 与
polarization，并以 exact rational replay 认证 12 rows 的 `G-D<0`、`1<D/G<12/5`、
`F/G>50` 与 packet-diagonal proxy `m_D^2<1/16`。这是
`NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT` 的
`YES_SCOPED_LITERAL_SIGNED_FOUR_PACKET_REASSEMBLY` 进展；source-level signed
cross-Gram、margin/endpoint payment、fixed-power credit、arithmetic `L2`、full Gate B
与 twin-prime conclusion 仍 OPEN/NONE。

当前主线状态：TPC-274 承接 TPC-273，在同一个锁定的 literal V59 finite physical
operator 上把三块 Haar projection 后的输出写成 `A_perp=(I-P_3)A`，并证明精确的
projected Frobenius envelope `G_perp <= ||A_perp||_F^2 ||beta||_2^2`。在 6 个
registered growing-cutoff scales 与 `s=1,2` 的 12 rows 上，exact rational matrix
replay 认证 envelope/actual output-energy gap `>50` 全部成立，envelope-induced
`m_F^2<1/64` 全部成立；phase census 为 11 negative-real、1 positive-real、0
crossing。这是 `NUMERICALLY_CERTIFIED_FINITE` 的 cancellation-free route
`INSUFFICIENT_SCOPED` obstruction，不是 actual margin 的上界、渐近反例或 source-level
theorem；signed output reassembly、fixed-power credit、arithmetic `L2`、full Gate B
与 twin-prime conclusion 仍 OPEN/NONE。

当前主线状态：TPC-273 承接 TPC-272，在同一个锁定的 literal V59 finite physical
operator 上对 4 个尺度、4 个 comparison cutoff 和 2 个 kernel exponent 做 32-row
outward rational margin matrix。精确转移 `m^2=rho^2`、`m^6=(rho^2)^3`，得到 12 个
`m<1/8`、11 个 middle-band、9 个 `m>1/4` rows；固定尺度的 cutoff-only 变化在
`N=64` 与 `N=128` 各产生一次跨带 flip，phase census 为 30 negative-real、2
positive-real、0 crossing。该结果是 `NUMERICALLY_CERTIFIED_FINITE` 的
`REFUTED_SCOPED` stability obstruction，不是渐近反例或 source-level theorem；
source-level margin uniformity、fixed-power credit、arithmetic `L2`、full Gate B 与
twin-prime conclusion 仍 OPEN/NONE。

当前主线状态：TPC-272 在同一个 literal V59 finite physical operator 上，将 TPC-271
的 phase--radius 坐标编译成一个严格的条件预算：若 signed scalar 有 effective saving
`sigma` 且相关性裕量 `m=|C_perp|/R` 只损失 `eta`，则 endpoint saving 为 `sigma-eta`，
严格目标支付为 `sigma-eta>1/400`。二维 exact converse 证明负相位本身不能给出正的
margin 下界；由 TPC-271 继承的 9 行有限证书显示 `96->192` 的 `m^6` 比值低于
`(1/32)^6` 而 phase sign 保持不变。这是 `PROVED_CONDITIONAL` 加
`NUMERICALLY_CERTIFIED` finite audit，不是 source-level margin theorem；fixed-power
credit、arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

TPC-271 在同一个 literal V59 finite physical operator 上，把 TPC-270
留下的 normalized radius 与 signed scalar、source lane、output lane 放进同一个
联合坐标系。六个 base rows 与三个 profile controls 的 residual scalar 全部锁定在
负实轴；但 `96->192` 的归一化半径比超过 23，source lane 低于 `1/8`、output lane
高于 230，说明这次有限 spike 是 output-lane dominated。精确恒等式
`Xi=Xi_W*Xi_G` 与 `Xi/Xi_C=|kappa|^(-6)` 已通过独立重算和 stress audit。
这是 finite phase-radius decoupling audit，不是 source-level phase/radius theorem；
fixed-power credit、arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

TPC-270 在同一个 literal V59 finite physical operator 上，把 TPC-269
留下的 residual radius 跨尺度问题写成 exact endpoint-normalized observable
`Xi=(R_squared)^3/N^10=(R/N^(5/3))^6`。六个 base rows、四个 dyadic ratios、五个
adjacent ratios 与三个 profile controls 均完成 outward interval 证书；dyadic pattern
为 `DROP_RISE_RISE_DROP`，其中 `96->192` 超过 23 倍而 `64->128` 低于 `1/4`。
这是 finite normalization audit，不是 source-level radius theorem；fixed-power credit、
arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

TPC-269 是 TPC-270 的上游：它在同一对象上完成 registered `z_N=floor(log N)` proxy 与
exact convex-profile transfer，12 行中 8 个 contraction、4 个 obstruction；中心
`theta=9/10`/`24/25` 翻过 `rho=1/4`。TPC-270 说明即使 endpoint normalization
固定，有限尺度仍出现强烈非稳定性，但不把有限比值升级为渐近结论。

TPC-268 在 TPC-267 的有限 residual census 之后，固定同一个 literal V59 physical
operator，只改变声明的有限 local cutoff、rounded clock 与 kernel exponent。16 个
rows 中 10 个 contraction、6 个 obstruction；同一 central row 的 `z=2`/`z=3`
翻转给出 scoped finite obstruction，不支付 fixed-power credit。

TPC-266 在 TPC-265 的 Schur endpoint-budget compiler 之后，
对 TPC-263→TPC-264→TPC-265 做了 typed end-to-end hostile audit，精确证明
fixed-log center 不能升级为 fixed-power lane、Schur residual 不能删除，且只有
center/radius 两条 effective saving 都严格大于 `1/400` 时才可返回 conditional
closure。actual V59 radius/phase、arithmetic `L2`、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。

TPC-265 在 TPC-264 的 orthogonal-residual Schur firewall 之后，
把 residual disk 的 sharp worst-case `|c|+R` 接入 endpoint ledger，并证明中心 lane
与 radius lane 各自都必须有严格大于 `1/400` 的 effective power saving；fixed-log
control 仍是零 fixed-power credit。actual V59 radius/phase、arithmetic `L2`、full
Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

TPC-264 在 TPC-263 的 rank-three physical channel 之后，精确求出
正交残差的 Schur 可实现集合：二维以上补空间是闭圆盘，一维是圆，退化情形是单点。
这把 `C_perp` 的缺失信息从“未估计”推进为一个 sharp finite firewall；endpoint-scale
synthetic radius 仍可达 `x^(5/3)`，因此没有 fixed-power `1/400` credit。actual V59
residual、arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

TPC-263 在 TPC-262 的 signed-operator interface 之后，把
source-backed rank-three Haar channel 与四个物理 block sums 接到同一个 literal
V59 coupling，严格得到 `C_3=O(x^(5/3)/(log x)^(M+3))`；exact
`C_perp` residual 被保留并明确成为下一关。该结果是 fixed-log-only，不能支付
fixed-power `1/400`，arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍
OPEN/UNPAID/NONE。

TPC-262 在 TPC-261 的 endpoint compiler 之后，把 literal
reduced-residue signed remainder operator、deleted diagonal、weighted cross-Gram
与 packet-index phase-character firewall 精确锁定在同一个有限对象上，并用
actual prime unit-class matrices 做了 finite operator-image adversarial audit。
这一步确认 diagonal/PSD 数据不能替代 signed cross-Gram；actual growing V59
`beta,w` character estimate、arithmetic `L2`、full Gate B、strict global credit 与
twin-prime conclusion 仍 OPEN/UNPAID/NONE。

TPC-261 在 TPC-260 的 four-packet mode-zero audit 之后，把
baseline `E0=5/3` 到 target `E*=1997/1200` 的端点义务编译成严格的
`1/400` effective fixed-power threshold，并证明 fixed-log suppression 不产生
fixed-power credit。缩放后的 null-compatible plus/alternating witness 仍可在相同
marginals 与 Haar/null data 下产生 baseline-scale residual `16*x^(5/3)` 或 `0`；
这是 scoped structural obstruction。literal common-clock mode-zero/cross-Gram、
arithmetic `L2`、full Gate B、strict global credit 与 twin-prime conclusion 仍
OPEN/UNPAID/NONE。

1. **Goal Reduction** *(Completed)*: Reduce the fixed-gap prime pair problem to proving $B_{h_0,\delta}(X) = o(X)$.
2. **Carrier Construction** *(Mostly Completed)*: Establish a dynamical-arithmetic decomposition that preserves the fixed gap $h_0$, Möbius sign, actual support, and physical normalization.
3. **Branch Classification** *(Mostly Completed)*: Identify two anomalous resonant branches and derive the three-ledger inequality for the remainder.
4. **Low-Cost Route Screening** *(TPC-103–107, Next Step)*: Test $(W_X, \mathfrak{P}_X, \mathfrak{X}_X)$ to determine whether to proceed with the positive resonance route or switch to the signed-filter route.
5. **Core Arithmetic Attack** *(TPC-108–109)*: Prove the signed Möbius cancellation $H3$ on the actual fixed-$h_0$ carrier. This will be the first genuine $L^2$ advance.
6. **Energy and Zero Mode** *(TPC-110–112)*: Control the determinant energy and the distinguished zero mode separately to avoid conflating total energy with arithmetic cancellation.
7. **Physical Reassembly** *(TPC-113–117)*: Complete the canonical frame, fixed-$h_0$ localization, high-frequency and ultra-tail returns, and full-block cover.
8. **Endpoint Accounting** *(TPC-118)*: Prove that all physical reassembly losses strictly satisfy $\Lambda_{\mathrm{phys}} < 1/400$.
9. **Return to the Original Problem** *(TPC-119)*: Stitch all local results back into the original hard packet to rigorously obtain $B_{h_0,\delta}(X) = o(X)$.
10. **MVP2 Global Audit** *(TPC-120)*: If all gates pass, the conditional Hardy–Littlewood asymptotic for fixed $h_0$ is obtained; the twin prime conclusion follows only if the framework applies completely to $h_0 = 2$.

## 3. Latest Paper
tpc-287-prime-shell-cancellation-depth - 当前阶段 - 严格证明 finite shell component
additivity 与 conditional retention envelope；完成 84-row / 336-component ladder，
57 mixed-sign rows、retention upper `<1/2/<1/4/<1/10` 为 31/22/8，48 个 leave-one-out
sign flips 与 12 个 zero remainders；growing-shell stability、literal `L2`、full Gate B
仍 OPEN，fixed-power credit 为 0。
tpc-286-diagonal-deletion-attachment-ledger - 当前阶段 - 精确证明
`g_phys=g_full-g_diag` 与 `C_phys=C_full-C_diag`，并完成 72-row full/diagonal/physical
component ledger：15 个 full/physical sign flips、30 个 diagonal-opposition rows、
21 个严格 diagonal-dominance rows；asymptotic dominance、signed full-shell cancellation、
literal `L2`、full Gate B 仍 OPEN，fixed-power credit 为 0。
tpc-285-prime-shell-residue-rank-obstruction - 当前阶段 - 精确证明 centered residue
factorization 与 deleted-diagonal full active rank；20 个 registered prime/exponent rows
的 kernel Schur blocks 均通过模素数 rank witness，关闭“仅靠 `q-2` 低秩即可得到
physical arithmetic `L2`”的直接捷径；signed full-shell cancellation、literal `L2`、
full Gate B 仍 OPEN，fixed-power credit 为 0。
tpc-284-admissible-source-control-atlas - 当前阶段 - 完成六类 declared schedule controls
的 72-row literal-source atlas：60 negative、12 positive、0 crossing，8 个相对基线
sign flips，最弱 controlled `rho^2` 下界约 `1.4118e-5`；这是有限控制图谱与
sign-stability obstruction，exhaustive source class、asymptotic stability、literal
arithmetic `L2`、full Gate B 仍 OPEN，fixed-power credit 为 0。
tpc-281-arithmetic-l2-gate-b-interface-audit - 当前阶段 - 证明 typed arithmetic
`L2` 到 Gate-B output-energy 的 exact conditional interface，并以 `R^2` 中 equal-norm
orthogonal functional 给出 full/zero attachment obstruction；4 个 exact packet fixtures、
4 个 interface cases 与 TPC-280 全部 12 行 transfer 通过，literal source `L2`、typed
attachment nondegeneracy、full Gate B 仍 OPEN，fixed-power credit 为 0。
tpc-280-leakage-aware-endpoint-compiler - 当前阶段 - 证明带 additive leakage 的
two-term gain/margin compiler：`G/D<=B X^(-gamma)+(ell/d)X^(-delta)`，collapsed
exponent 为 `min(gamma,delta)`，并以 equality family 认证 sharpness；6+4+4 个
exact fixtures 与 TPC-279 12-row transfer 通过，literal arithmetic `L2`、full Gate B
仍 OPEN，fixed-power credit 为 0。
tpc-279-coherence-to-gain-theorem - 当前阶段 - 证明四包 reassembly 的 exact
minimal deficit criterion 与 sharp pairwise-coherence envelope；正交包 refute
coherence-only power promotion，near-cancellation family 给出 sharp adversarial
scale，并完成 TPC-278 全部 12 行的 exact reciprocal transfer；source-level
asymptotic deficit、arithmetic `L2` 与 full Gate B 仍 OPEN，fixed-power credit 为 0。
tpc-278-cross-scale-gain-stability - 当前阶段 - 在同一 literal source 上仅改变有限
prime-shell endpoint 或 clock，12 行 exact rational replay 认证 8/4 cross-sign census
与 4 次符号翻转，有限 `D/G>=1` stability 被 scoped 否定；growing source theorem、
arithmetic `L2` 与 full Gate B 仍 OPEN，fixed-power credit 为 0。
tpc-277-four-packet-gain-floor - 当前阶段 - 证明四包几何的 sharp gain floor `D/G>=1/4`，
在非正 signed cross term 下证明 `D/G>=1`，并以 8 个 exact source rows 发现
`D/G>1` 但 `r>=1.01` 的 finite obstruction；正幂 source theorem、arithmetic `L2`
与 full Gate B 仍 OPEN，fixed-power credit 为 0。
tpc-276-signed-gain-endpoint-budget - 当前阶段 - 证明 exact `m^2=(D/G)m_D^2` 与
conditional strict budget `sigma-eta_eff>1/400`（`eta_eff=max(0,eta_D-gamma/2)`），
并以 12 行 exact rational transfer 认证 `D/G>1` 全部成立、3 行超过 quarter、5 行
超过 eighth；finite gain 的 fixed-power credit 明确为 0，source-level lower bound
仍 OPEN。
tpc-275-signed-four-packet-reassembly - 当前阶段 - 对四个实际 source-block 输出包建立 exact signed Gram、四点 DFT 与 polarization ledger，并在 12 个 growing-cutoff rows 上认证 `G-D<0`、`1<D/G<12/5`、`F/G>50`、`m_D^2<1/16`；source-level signed cross-Gram 与 endpoint payment 仍 OPEN。
tpc-274-projected-output-frobenius-envelope - 当前阶段 - 证明 projected Frobenius
envelope，并在 12 个 growing-cutoff rows 上以 exact rational replay 认证 `G_F/G_perp>50`
与 `m_F^2<1/64`；关闭 cancellation-free output shortcut，但 signed reassembly 与
source-level output theorem 仍 OPEN。
tpc-273-margin-stability-matrix - 当前阶段 - 在 32-row literal V59 margin matrix 中以 exact `m^2=rho^2` 转移认证 12 low/11 middle/9 high，发现两个 cutoff-only finite stability flips 与 30/2 phase census；source-level margin uniformity仍 OPEN，fixed-power credit为0。
tpc-272-correlation-margin-budget-compiler - 当前阶段 - 证明 `sigma-eta>1/400` 的条件 correlation-margin endpoint compiler，并用二维 sharp converse 否定 sign-only margin；9 行/4 个 dyadic finite margin audit 通过，source-level margin 与 full Gate B 仍 OPEN。
tpc-271-phase-radius-decoupling - 当前阶段 - 在同一 finite literal V59 operator 上建立 `Xi=Xi_W*Xi_G` 与 `Xi/Xi_C=|kappa|^(-6)` 的 exact lane factorization；9 行 phase 全为负实轴，但 `96->192` 半径比 `>23` 由 output lane `>230` 驱动，仍不构成渐近 theorem。
tpc-270-cross-scale-radius-normalization - 当前阶段 - 在同一 finite literal V59 operator 上建立 exact `Xi=(R_squared)^3/N^10` endpoint normalization，认证 4 个 dyadic 与 5 个 adjacent scale ratios，得到 `DROP_RISE_RISE_DROP`；profile controls 落在 `(1/2,3/4)`，source-level radius、arithmetic `L2` 与 full Gate B 仍 OPEN。
tpc-269-growing-cutoff-profile-transfer - 当前阶段 - 在同一 finite literal V59 operator 上引入注册的 growing-cutoff proxy 与 exact convex-profile transfer；12 行中 8 个 contraction、4 个 obstruction，中心 `theta=9/10`/`24/25` 翻转表明 profile-uniform quarter bound 失败，cross-scale radius theorem 仍 OPEN。

tpc-268-finite-cutoff-sensitivity-obstruction - 当前阶段 - 在同一 finite literal V59 operator 上完成 cutoff/clock/kernel sensitivity audit，16 行中 10 个 contraction、6 个 outward-certified obstruction；中心 `z=2`/`z=3` 翻转是 scoped finite result，渐近 theorem 与 full Gate B 仍 OPEN。

tpc-267-literal-v59-residual-radius-census - 当前阶段 - 在实际 prime shell、unit masks、deleted diagonal、beta 与 shifted-prime comparison 上完成 12 行有限区间 residual-radius/signed-phase census，全部得到 `|C_perp|/R<1/4`，但仅为 finite certificate；渐近 radius/phase 与 full Gate B 仍 OPEN。
tpc-266-end-to-end-claim-firewall - 当前阶段 - 对 TPC-263→TPC-264→TPC-265 建立 exact typed end-to-end claim firewall，完成 fixed-log non-promotion、residual-retention firewall 与 strict `1/400` 六状态 hostile matrix；literal V59 radius/phase 仍 OPEN。
tpc-265-schur-endpoint-budget-compiler - 当前阶段 - 将 Schur residual radius 编译成 sharp `|c|+R` endpoint lane，给出严格 `1/400` 两 lane 支付条件并封住 norm-only cancellation credit；literal V59 radius/phase 仍 OPEN。
tpc-264-orthogonal-residual-schur-firewall - 当前阶段 - 精确分类 `C_perp` 的 disk/circle/singleton Schur feasible set，量化 rank-three channel 之后仍缺少的 residual radius/phase；synthetic endpoint witness 不产生 arithmetic credit。
tpc-263-rank-three-physical-cross-gram - 当前阶段 - 将四块 hybrid `w` 的 fixed-log 控制与 TPC-257 三个 adjoint asymptotic 在 exact `P3` 上相乘，支付 rank-three physical cross-Gram channel；正交残差仍 OPEN。
tpc-262-literal-mode-zero-cross-gram - 当前阶段 - literal signed reduced-residue operator、cross-Gram/DFT ledger 与 phase-character firewall 已精确闭合；growing-shell arithmetic estimate 仍开放。
`tpc-262-literal-mode-zero-cross-gram` - `PROVED_EXACT_LITERAL_SIGNED_REDUCED_RESIDUE_OPERATOR_AND_PHASE_CHARACTER_FIREWALL` - 精确给出 `J_(q,v)=S_(q,v)^*C_qS_(q,v)-((q-2)/(q-1))P_q`、四 packet signed cross-Gram/DFT 恒等式和 phase-character separation；finite operator-image witness 显示相同 diagonals 可有 mode-zero `16||Y||^2` 或 `0`，但 growing `beta,w` estimate 与 arithmetic `L2` 仍 open。
`tpc-261-strict-endpoint-budget-compiler` - `PROVED_STRUCTURAL_ENDPOINT_BUDGET_OBSTRUCTION_FOR_LITERAL_V59_REASSEMBLY` - 将 `E0-E*=1/400` 编译为 lane saving-minus-loss 的严格阈值，证明 log-only suppression 无固定幂 credit，并缩放 TPC-260 witness；literal mode-zero/cross-Gram estimate、arithmetic `L2` 与 full Gate B 仍 OPEN。
`tpc-260-four-packet-residual-reassembly` - `PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION` - 将 TPC-258/259 的 null direction 放入实际四块 Haar complement，证明四 packet residual 的 sharp polygon completion 和 DFT mode-zero identity；相同 marginals 与 null/Haar 数据仍允许 energy `0` 与 `16`，故 literal mode-zero/cross-Gram estimate 仍是 OPEN。
`tpc-259-same-clock-null-coupling` - `PROVED_SOURCE_BACKED_SAME_CLOCK_NULL_CHANNEL_SUPPRESSION_FOR_LITERAL_V59_SIGNED_COUPLING` - 在同一 literal V59 clock 上将 TPC-258 的 source-frozen null direction 与四块 hybrid `w` moment 精确耦合，证明 signed scalar 的 rank-one null channel 对任意固定 log power 都被压低；同时用 zero-diagonal witness 明确保留 `w_perp` residual，未宣称 full scalar、fixed-power 或 `L2`。
`tpc-258-source-frozen-transverse-null-direction` - `PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_FOR_LITERAL_V59_ADJOINT` - 在 TPC-257 的四块 Haar frame 中以预先冻结的曲率向量构造单位 null direction，证明 transverse `B_Q` diagonal 的 `o(1)` cancellation；明确保留 boundary/rate firewall，未宣称 fixed-power、arithmetic `L2` 或 Gate B。

`tpc-257-four-block-haar-transverse-norm-floor` - `PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR_FOR_LITERAL_V59_ADJOINT` - 将 TPC-256 的两个 rank children 各再 source-only 二分，证明三向 Haar frame exact orthonormal、三个 literal `beta` curvature constants 显式为正，并由 bounded-variation adjoint compiler 得到 `span(z1,z2)` 的同阶 transverse norm floor；这是下界/obstruction，不是 `L2` 上界或 full Gate-B payment。

`tpc-256-literal-beta-haar-adjoint-asymptotic` - `PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC` - 以 consecutive-interval divisor-density cancellation 和强 PNT 二阶曲率证明 literal `beta` rank-midpoint 的显式正渐近式，再用 TPC-255 的 `B_Q` deleted-diagonal return 与 `H^2/q` boundary first moment 得到 adjoint Haar scalar 的显式负实主项、eventual nonzero 与 normalized phase `->-1`；boundary 有 `1/48` power separation，但仅为一条 Haar 投影，`L2` 与 full Gate B 未支付。

`tpc-255-exact-adjoint-diagonal-boundary-compiler` - `PROVED_EXACT_SOURCE_BACKED_L1_ADJOINT_DIAGONAL_HARD_WINDOW_CHILD_JUMP_COMPILER` - 将 ordered-rank Haar vector 穿过 literal V59 adjoint，证明 complete unit-centered lattice alias 在 `H>2Q` 时由 Poisson 精确消失，并把 deleted diagonal、input/output unit masks、hard-window leakage 与 child-jump leakage 全部原样返回；最终得到 `-B_Q<z_mid,beta>` 加三个 explicit correction lanes，但无 lane estimate、arithmetic `L2` 或 Gate-B credit。

`tpc-254-source-backed-rank-midpoint-hybrid-mean-closure` - `PROVED_SOURCE_BACKED_L1_RANK_MIDPOINT_HYBRID_MEAN_CLOSURE_WITH_ADJOINT_LANE_SOURCE_GAP` - 从冻结 hybrid maximal Type-I theorem 的非负和中合法抽取 `m=1`，对每个实数 clock 的两个 rank children 证明任意固定 log-power mean control，并得到 literal `w` midpoint Haar moment `x^(1/2)(log x)^(-M)`；adjoint `beta` lane 仍无 source estimate，zero-diagonal derangement 证明 norm-only Cauchy sharp，full Gate B 仍开放。

`tpc-253-source-frozen-rank-midpoint-contrast-compiler` - `PROVED_STRUCTURAL_L1_SOURCE_FROZEN_RANK_MIDPOINT_CONTRAST_COMPILER` - 从 ordered physical interval 在观察任何 coefficient/margin/sign 前冻结 rank midpoint，证明 normalized Haar projector、integer `floor(3x/4)` crosswalk、partial-sum longitudinal/transverse covariance transfer、within-child remainder、literal TPC-247 kernel expansion 与安全 adjoint identity；midpoint 的实际符号、非零性、算术尺度与 Gate-B margin 仍开放。

`tpc-252-declared-partition-refinement-degeneracy` - `PROVED_STRUCTURAL_L1_DECLARED_PARTITION_REFINEMENT_DEGENERACY` - 证明 binary refinement 的 exact rank-one covariance transfer、true transverse radius monotonicity、fixed-probe Gram subtraction 与 universal singleton collapse，并严格给出 all-partition margin optimization 等于 direct external bound；自由 partition 优化因而被封口，actual V59 非零 contrast 与算术 saving 仍开放。

`tpc-251-literal-v59-declared-block-longitudinal-transverse-margin-compiler` - `PROVED_STRUCTURAL_L1_LITERAL_V59_DECLARED_BLOCK_LONGITUDINAL_TRANSVERSE_MARGIN_COMPILER` - 将 actual `lambda_cb=1` probes 在 exhaustive declared blocks 内精确收缩并作 block-flat longitudinal/transverse 分解，证明 projected Gram rank-one subtraction、TPC-250 coherence radius、conditional external lower margin 与 strict-endpoint obstruction；partition/direction 与 external error 均未冒充 source-canonical arithmetic input。

`tpc-250-coherence-controlled-gram-quadratic-sharpness` - `PROVED_STRUCTURAL_L1_COHERENCE_CONTROLLED_GRAM_QUADRATIC_SHARPNESS` - 从 diagonal weighted energy、weighted one-norm 与 active coherence 导出 exact Gram quadratic 的 sharp two-sided envelope，并继承到 independent/global TPC-249 radii；PSD equicorrelation、anti-correlation、simplex 与同 marginal 对抗样例证明常数、zero floor 与 marginal-only obstruction 全部 sharp，actual V59 coherence arithmetic 仍开放。

`tpc-249-sharp-weighted-shared-lane-contraction` - `PROVED_STRUCTURAL_L1_SHARP_WEIGHTED_SHARED_LANE_CONTRACTION` - 将 complex weights 在每个 physical shared lane 内精确收缩为 `g_c`，证明 independent/global budget 的 sharp Gram support radius、explicit reverse realization、tagged triangle dominance 与 common-ray equality criterion；repeated-probe opposite-weight fixture 精确恢复 tagged copies 丢失的 cancellation，actual Gram arithmetic 仍开放。

`tpc-248-shared-lane-gram-ellipsoid-feasible-set` - `PROVED_STRUCTURAL_L1_SHARED_LANE_GRAM_ELLIPSOID_FEASIBLE_SET` - 将 TPC-247 固定 output block 上的多 probe/单 shared lane 联合像精确分类为 range-restricted pseudoinverse Gram 椭球，证明 sphere/slack 二分、physical conjugate orientation 与 global-budget sum-energy law，并以 diagonal-disk 反例严格否定 marginal-to-polydisk promotion；arithmetic L2 仍开放。

`tpc-247-literal-v59-source-operator-attachment` - `PROVED_STRUCTURAL_L1_LITERAL_V59_SOURCE_OPERATOR_ATTACHMENT_WITH_NORM_OBSTRUCTION` - 将完整 V59 prime weight、unit masks、deleted diagonal 与 `K_H(u-t)` 锁入 source operator，证明 hard source blocks exactly-once 与 tagged two-lane covariance；同时精确证明 `sqrt(m)` output-copy toll 并反例否定 `B`-norm preservation，primitive-frequency attachment 与 arithmetic L2 仍开放。

`tpc-246-weighted-covariance-disk-reassembly` - `PROVED_STRUCTURAL_L1_WEIGHTED_COVARIANCE_DISK_REASSEMBLY` - 证明任意复权重下 coupled local families 的 aggregate disk containment 与 complete Cartesian disk product 的 exact Minkowski identity，给出 explicit reverse realization、sharp zero/margin criterion，并把 TPC-243 hard-window leakage 作为单次 additive radius；literal source attachment、product realizability 与 arithmetic L2 仍开放。

`tpc-245-sharp-longitudinal-transverse-covariance-disks` - `PROVED_STRUCTURAL_L1_SHARP_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISKS` - 对固定一维 longitudinal moments 与 transverse energies 给出 dimension-sensitive exact covariance feasible set：维数至少二为 closed disk、维数一为 circle/singleton、维数零为 singleton/unrealizable，并证明 sharp zero margin 与 phase cone；canonical block direction、literal V59 attachment 与 arithmetic L2 仍开放。

`tpc-244-common-multiplier-sign-localization` - `PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION` - 证明共同 block multiplier 的外层 sign/phase 在正交 coefficient covariance 中精确退化为 `|C_h|^2`，给出 nonorthogonal sign-cut polynomial 与 all-sign iff criterion，并由 TPC-243 得到 `2epsilon||W||||B||` hard-window leakage；literal V59 two-lane attachment 与 arithmetic L2 仍开放。

`tpc-243-hard-window-near-isometry-bilinear-transfer` - `PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER` - 对有限 separated circle frequencies 证明 hard rectangular synthesis 的双边 near-isometry 与 oriented signed bilinear transfer；在 V59 尺度误差为 `(133/100+o(1))x^(-67/200)log x`，但 literal top-prime coefficient attachment、signed `C_h` theorem 与 arithmetic L2 仍开放。

`tpc-242-phase-fourier-collision-separation` - `PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER` - 证明 literal `i^j` convention 下完整 `C_4` 能量谱、固定总能量的 sharp cross-term closed disk 与 imbalance/Gram exact defect；并 source-type 地证明 TPC-241 unsigned floor 对 V59 signed `F_1` 无直接定量转移，但不宣称物理 top-prime mode 消失。

`tpc-241-top-prime-collision-sharpness` - `PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_COLLISION_SHARPNESS` - 利用冻结 profile 的 normalized first moment、top-prime primitive-residue Cauchy、weighted PNT 与 TPC-238 full-vector lower frame，证明 coefficient/finite-window liminf 常数 `10773log(2)/1600`、`10773log(2)/3200` 及 `x^(1/48)/log x` 下界；从而严格否定 unsigned common-profile kernel 的任何 fixed-power 改进，但 signed four-packet Gate-B scalar 仍开放。

`tpc-240-top-prime-direct-energy-floor` - `PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_DIRECT_ENERGY_FLOOR` - 在 literal frozen common profile 下，将 TPC-215 的 top-prime singleton coefficient 与 TPC-216 的 fixed-q primitive row identity 通过 endpoint-safe Riemann sum 和两条 weighted PNT 精确聚合，得到 `D_top^psi=[1197 kappa_psi log(2)/800+o_psi(1)]Q^2/H=x^(1/96+o(1))`；因此 q-split unsigned direct factor 不可能提供 fixed-power saving；其 q-collapsed unsigned sharpness 已由 TPC-241 解决，signed Gate-B scalar 仍开放。

`tpc-239-brun-titchmarsh-primitive-bucket-envelope` - `PROVED_SOURCE_BACKED_PRIME_DENSITY_L1 / LOGARITHMIC_ONLY` - 将每个 primitive physical frequency bucket 的 shell-prime incidence 上界为 reduced residue classes 中的 prime counts，并以 Brun--Titchmarsh 证明 `R_h(a)<<x^(1/96)loglog x/log x`；代入 TPC-237 composition 得 normalized `x^(1/48)(log x)^4loglog x`，但没有 fixed-power、signed `C_h` 或 Gate-B advance。

`tpc-238-finite-window-lower-frame-obstruction` - `PROVED_STRUCTURAL_OBSTRUCTION_L1 / CROSS_REDUCED_FREQUENCY_CANCELLATION_REFUTED_SCOPED` - 用 translated triangular minorant、Fejér kernel、primitive Farey spacing 与 circular inverse-square packing 证明 normalized lower frame `[1/2-pi^2 U^4/(6N^2)]_+`；V59 上为 `1/2-O(x^(-67/100))`，从而严格排除 `q`-collapse 后跨 reduced-frequency 的 fixed-power cancellation，下一步进入 literal `C_h`-weighted same-frequency prime buckets。

`tpc-237-collision-compressed-finite-window-reassembly` - `PROVED_STRUCTURAL_L1 / COLLISION_COMPRESSED_FINITE_WINDOW_PACKET_TRACE` - 在 primitive reduced frequencies 上先使用 TPC-236 physical collision factor `4Q^2/H+4UQ/H` 合并 prime shell，再使用 TPC-217 finite-window large sieve，严格把旧 `P` collapse 改进为 normalized `x^(1/48)+x^(1/50)` envelope；`C_h` signs、signed four-packet scalar、arithmetic L2 与 Gate B 仍开放。

`tpc-236-physical-multiwrap-collision-envelope` - `PROVED_STRUCTURAL_L1 / SOURCE_VALID_PHYSICAL_FIBER_BESSEL_ENVELOPE` - 证明 physical residue bucket 的 exact gcd-fiber bound 与 unnormalized weighted Bessel envelope，V59 loss 为 `(4+o(1))x^(1/96)`；exact Q101 floor fixture 的三条 identical rows 给出 ratio `3`，严格否定 multiplicity-two 的 physical transfer，下一步是带 signed `C_h` 的 cross-`h` reduced-frequency reassembly。

`tpc-235-v59-physical-depth-crosswalk` - `PROVED_STRUCTURAL_L1 / SINGLE_CLOCK_AND_OUTPUT_NORMALIZATION_REFUTED_SCOPED` - 精确证明 V59 physical depth 为 `lambda_h=hQ/H`，single-clock simultaneous attachment iff `H=4Q^2`，故 V59 存在 `4x^(1/96)` growing mismatch；同时证明逐 output unit normalization 会把 four-phase polarization 从非零值抹为零，下一合法对象是保留 `C_h` 与 common linear packet transform 的 weighted physical `h`-fiber。

`tpc-234-normalized-collision-bessel-stability` - `PROVED_STRUCTURAL_L1 / DEPTH_UNIFORM_NORMALIZED_BESSEL_BOUND` - 利用 residue multiplicity two 证明任意 unit rows 的 `0<=T*T<=2I` 与 `||T*T-I||<=1`，彻底移除 depth-dependent conditioning；literal Q39 block 的 `4/3,2/3` ratios 证明 normalization 不自动产生 saving，actual V59 source validity 仍开放。

`tpc-233-critical-depth-row-mass-obstruction` - `PROVED_ARITHMETIC_OBSTRUCTION_L1 / RAW_ROW_COMPARABILITY_REFUTED_SCOPED` - 构造 `L~log Q/loglog Q` 的 primorial-saturated clocks，证明 low/high prime rows 的 raw atom ratio 至少 `(1+o(1))L/log L` 并发散，从而否定 fixed comparability 是 clock geometry 自动结论；row normalization 与 actual V59 weights 仍开放。

`tpc-232-subcritical-growing-resonance-depth` - `PROVED_ARITHMETIC_OBSTRUCTION_L1 / SUBCRITICAL_GROWING_DEPTH_STOP_SCOPED` - 对 `h=4LQ` 建立 exact one-wrap collision compiler 与 coefficient-uniform Selberg sieve，证明 `C_L/P->0` whenever `L=o(log Q/log log Q)`；首次给出增长 resonance 深度的严格必要门槛，critical depth 与 actual V59 attachment 仍开放。

`tpc-231-finite-resonance-sieve-obstruction` - `PROVED_ARITHMETIC_OBSTRUCTION_L1 / FIXED_FINITE_RESONANCE_STOP_SCOPED` - 计算 first `3--7` resonance 的 exact local root law 与 moving-determinant singular series，用 Selberg upper-bound sieve 证明 `E/P->0`，并经有界度能量引理推出 fixed finite comparable-row resonance families 不能支付任何 fixed saving；growing depth 与 actual V59 source mass crosswalk 仍开放。

`tpc-230-matched-resonance-mass-ceiling` - `PROVED_STRUCTURAL_L1 / MATCHED_RESONANCE_MASS_CEILING` - 证明 global AP saving 不超过 matched diagonal mass，给出 sharp anti-aligned extremizer、`M/D<=2*kappa*E/P` 与 literal `kappa<=4`，从而提取 strict `1/400` 所需 `E/P>=1/3200` density toll；该 asymptotic density toll 已由 TPC-231 证明失败，actual source concentration 仍开放。

`tpc-229-primitive-resonance-matching-spectrum` - `PROVED_STRUCTURAL_L1 / PRIMITIVE_RESONANCE_MATCHING_SPECTRUM` - 证明所有 primitive `3--7` resonance graphs 都是 matching，给出 `(-1,-1,+1,+1)` sharp edge spectrum、`0..2` AP ratio 与 exact antisymmetric saving criterion；4089-scale census 通过，matched source mass 与 arithmetic dominance 仍开放。

`tpc-228-source-native-polarized-collision-compiler` - `PROVED_STRUCTURAL_L1 / SOURCE_NATIVE_POLARIZED_COLLISION_COMPILER` - 证明共同 profile 下四相位 `E_AP-E_diag` 精确编译为 source-labelled off-diagonal collision sum，并把 Q25 `3--7` resonance 写成四项 `beta-w` block；五类 exact sign controls 与两个 graph controls 通过，actual V59 atom crosswalk 和 arithmetic sign 仍开放。

`tpc-227-packet-profile-axis-separation` - `PROVED_STRUCTURAL_L1 / PACKET_PROFILE_AXIS_SEPARATION` - 证明 four-phase packet-dependent transforms 精确恢复 V59 physical bilinear form当且仅当四个 packet Gram 全等于 physical Gram；Q25 first-collision block 的 row-dependent odd sign 给出 `-1/80000` off-diagonal mismatch，封住 profile sign 自动冒充 source phase 的捷径，common-profile source compiler 与 arithmetic L2 仍开放。

`tpc-226-first-primitive-collision-transition` - `PROVED_STRUCTURAL_L1 / FIRST_PRIMITIVE_COLLISION_TRANSITION` - 证明 primitive shared-clock rows 在 `L<=3` 两两不交、`L=4` 首次且仅出现 `7p+3r=16Q` 的 `(3,-7)` resonance；同一 collision 对 aligned/affine profiles 放大、对 balanced sign profile 抵消，505 个尺度分类与 30 个 exact-rational profile records 通过独立复现，V46 transfer 与 arithmetic L2 仍开放。

`tpc-225-cutoff-one-shared-clock-obstruction` - `PROVED_STRUCTURAL_L1 / CUTOFF_ONE_SHARED_CLOCK_OBSTRUCTION` - 证明 TPC-224 named source clock 的 cutoff-one prime rows 具有 pairwise disjoint support，精确得到 E_AP=E_diag、E_all=E_pol，从而在该 clock 上 refute strict AP saving；完成 9 个 affine scales、14 个 adversarial profile records 与 Q=3..99 boundary replay，算术 L2、V46 transfer、Gate B 仍开放。

`tpc-224-literal-two-channel-compatibility-audit` - `PROVED_STRUCTURAL_L1 / LITERAL_TWO_CHANNEL_COMPATIBILITY` - 证明共同 literal Hilbert-vector interface 与 sharp constant `PJ/(P+J)`，并用五个 exact-rational collision-stress scales scoped-refute unit-factor shortcut；算术 marginal savings 与 V46 transfer 仍开放。

`tpc-223-conditional-signed-reassembly-compiler` - `CONDITIONAL_THEOREM / TWO_CHANNEL_SIGNED_REASSEMBLY_COMPILER` - 在共同 literal interface 假设下证明 `sigma=min(delta_AP,kappa_pol)-lambda_struct`，exact rational certificate 区分 strict/borderline/fail/missing-channel/loss-dominated cases；AP dispersion、polarized cross-correlation 与 literal reassembly 仍开放。

`tpc-222-four-packet-cross-term-obstruction` - `PROVED_STRUCTURAL_L1 / FOUR_PACKET_CROSS_TERM_OBSTRUCTION` - 证明四点极化精确恢复 signed cross-term，并以相同 diagonal/trace、目标 energy `16/0` 的 rank-one fixtures 说明 PSD/trace 无符号包络不能识别 signed reassembly；算术 `L2` 仍开放。

`tpc-221-collision-graph-schur-envelope` - `PROVED_STRUCTURAL_L1 / COLLISION_GRAPH_SCHUR_ENVELOPE` - 将 TPC-220 collision Gram 组织成 PSD quadratic form，证明 weighted Schur row-sum envelope，并用 `h=5`, `q={101,151,181,191}` 的 literal fixture 得到 `Gamma=2J_4` 与 exact ratio `P=4`；绝对 Schur 不能单独产生 sub-`P` saving。

`tpc-220-prime-ap-collision-crosswalk` - `PROVED_STRUCTURAL_L1 / EXACT_PRIME_AP_MULTIPLICATIVE_CROSSWALK` - 将 TPC-219 的 q-transverse target 精确改写为 literal weighted prime-AP operator 与 multiplicative collision Gram；diagonal 在 cutoff injectivity 下还原为 fixed-q atom energy，off-diagonal collision graph 被明确保留，算术 `L2` 仍开放。

`tpc-219-prime-shell-longitudinal-ledger` - `PROVED_STRUCTURAL_L1 / EXACT_LONGITUDINAL_TRANSVERSE_LEDGER` - The exact identity `E_shell=P(E_diag-E_perp)` converts the scalar `P` collapse into an iff transverse-energy condition; aligned and balanced rational fixtures attain the two endpoints, while literal prime-shell cancellation remains open.

`tpc-218-prime-shell-packet-lift` - `PROVED_STRUCTURAL_L1 / PRIME_LABEL_AND_PACKET_PRESERVING_LIFT` - Retaining prime and packet labels in a Hilbert-valued finite-window lift gives normalized split envelope `x^(1/96)(log x)^5`; scalar recovery pays the explicit `P<=2Q` factor and returns `x^(11/32)(log x)^5`; an exact q-aligned fixture saturates `P=4` and packet alignment has projection ratio `1`, while arithmetic signed reassembly remains open.

`tpc-217-finite-window-rational-large-sieve` - `PROVED_STRUCTURAL_L1 / FINITE_WINDOW_ATTACHMENT` - Exact reduced-frequency regrouping, Farey spacing, and the standard additive large sieve attach the TPC-216 direct-sum envelope to `I_x=(x/2,x]` with normalized bound `x^(11/32)(log x)^5` and unnormalized exponent `43/32`; a one-point aligned fixture gives exact coherent-to-diagonal ratio `2`, while prime-shell reassembly and arithmetic cancellation remain open.

`tpc-216-direct-sum-row-energy-envelope` - `PROVED_STRUCTURAL_L1 / DIRECT_SUM_ROW_ENERGY_ENVELOPE` - Fixed-q cutoff injectivity and one shell Cauchy step give the literal complete-period bound `L^(-1)E_direct <<_psi x^(11/32)(log x)^3`; an exact aligned-support fixture refutes free q-orthogonality, while finite-window reassembly and arithmetic cancellation remain open.

`tpc-215-short-quotient-mobius-majorant` - `PROVED_STRUCTURAL_L1 / SHORT_QUOTIENT_CLUSTER_MAJORANT` - V46 activation forces every emitter-visible reduced denominator into the full transition band; the resulting short-quotient Möbius tails give an explicit `O((log x)^2)=x^(o(1))` complete-period cluster-to-direct majorant, while top-shell rows have exact ratio one and the physical direct-sum energy remains open.

`tpc-214-mobius-frequency-clusters` - `PROVED_STRUCTURAL_L1 / MOBIUS_CLUSTER_REDUCTION` - Exact dilation covariance and reduced-denominator factorization of the common-source Gram with literal Möbius-log tails; finite cancellation and enhancement signs are both certified, while the asymptotic V46 cluster bound remains open.

`tpc-213-physical-profile-cross-gram` - `PROVED_STRUCTURAL_L1 / CROSS_DIVISOR_COUPLING` - Exact common-source profile-to-emitter pullback, gcd/lcm residue aliasing, and frequency-intersection cross-Gram; direct-sum physical replacement is refuted in scope, while the literal V46 asymptotic Gram bound remains open.

`tpc-212-truncated-boundary-emitter` - `PROVED_STRUCTURAL_L1 / STOP_SCOPED_BOUNDARY_EMITTER` - Exact signed Boolean endpoint leakage and complete-minus-missing boundary decomposition; reciprocal occupancy has a block-diagonal full-rank Gram and a scoped emitter-only alignment obstruction.
`tpc-211-product-coupled-euler-gram` - `PROVED_STRUCTURAL_L1 / STOP_SCOPED_PHYSICAL_COUPLING` - Literal product-coupled Euler profiles have full divisor rank; the complete `mu(d) log d` packet compresses to marked-prime derivatives, while the truncated transition boundary and reciprocal emitter remain open.
`tpc-210-poisson-profile-realizability` - `PROVED_STRUCTURAL_L1 / STOP_SCOPED` - Exact finite Schwartz/Poisson profile interpolation, literal Mobius-weighted aligned profiles, and cross-divisor Gram obstruction; the coupled physical profile theorem remains open.

`tpc-209-whole-frame-poisson-mobius-obstruction` - `PROVED_STRUCTURAL_L1 / STOP_SCOPED` - Fixed-divisor whole-frame Poisson reindexing, multiplicative profile normal form, exact V59 character crosswalk, and sharp frame-only alignment obstruction; profile-aware prime-only bound remains open.
`tpc-207-critical-moving-hole-bdh-defect` - `PROVED_STRUCTURAL_L1` - Exact rank-two moving-hole compiler and a collective $x^{53/32+o(1)}$ translation-defect bound at the $1/96$ clock; the zero-hole prime-only signed BDH theorem remains open.

`tpc-208-zero-hole-additive-edge-frame` - `PROVED_STRUCTURAL_L1` - Exact complete-graph additive tight frame for the zero-hole remainder, edgewise $(q-2)$ diagonal deletion, and a scoped literal-edge no-sparsification theorem; the collective Kloosterman compiler remains open.
