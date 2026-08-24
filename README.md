# Exploring Prime Distribution via Dynamical Methods

## 1. Exploring the Hilbert–Pólya Conjecture
- **A**: Construct a canonical dynamical spectral determinant.
- **B**: Complete non-self-adjoint dynamical objects into scattering/unitary objects that preserve the time direction.
- **C**: Obtain a genuinely self-adjoint operator and derive the $T \log T$ counting law intrinsically.
- **D**: Extract prime powers and von Mangoldt weights from the dynamical trace.
- **E**: Prove that the spectral divisor coincides exactly with the divisor of the completed zeta function.

## 2. Exploring the Twin Prime Conjecture

当前主线状态：TPC-226 在 TPC-225 cutoff-one obstruction 之后审计有限 dilation
`h_L=4LQ`, `L=1,2,3,4`。保留 literal primitive support 后，`L<=3` 的 distinct
prime rows 仍严格不相交；`L=4` 首次出现合法碰撞，且唯一 resonance type 是
`7p+3r=16Q`、multipliers `(3,-7)`。同一 geometry 对 aligned/affine profiles 放大
`E_AP`，对 balanced sign profile 则严格降低 `E_AP` 并给出 `E_pol=E_all=0`。
因此 geometry 只建立 signed-cancellation interface，不能替代 arithmetic sign theorem。
状态仍是 `PROVED_STRUCTURAL_L1`；V46 profile transfer、arithmetic L2 与 Gate B 均开放。

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
