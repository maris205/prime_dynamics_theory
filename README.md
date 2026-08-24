# Exploring Prime Distribution via Dynamical Methods

## 1. Exploring the Hilbert–Pólya Conjecture
- **A**: Construct a canonical dynamical spectral determinant.
- **B**: Complete non-self-adjoint dynamical objects into scattering/unitary objects that preserve the time direction.
- **C**: Obtain a genuinely self-adjoint operator and derive the $T \log T$ counting law intrinsically.
- **D**: Extract prime powers and von Mangoldt weights from the dynamical trace.
- **E**: Prove that the spectral divisor coincides exactly with the divisor of the completed zeta function.

## 2. Exploring the Twin Prime Conjecture

当前主线状态：TPC-241 已在每个固定冻结非负归一化 common profile 上证明 top-prime
q-collapsed coefficient energy 与 normalized finite-window kernel 都有
`x^(1/48)/log x` 级 liminf，显式常数分别为 `10773log(2)/1600` 与
`10773log(2)/3200`。因此 TPC-239 的 fixed-power `1/48` 在 exact unsigned
common-profile 对象上仅差对数即尖锐；下一步必须在平方前保留 literal `C_h` signs 或
four-packet polarization。arithmetic L2、signed Gate B 与 strict `1/400` 仍开放。

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
