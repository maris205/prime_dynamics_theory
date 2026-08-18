# TPC big-road paper candidate ledger

更新时间：2026-08-18

状态：**TPC212_STRUCTURAL_THRESHOLD_A_RELEASED / BOUNDARY_EMITTER_STOP_SCOPED / PHYSICAL_CROSS_DIVISOR_BOUND_OPEN**

本文件与路线图平行维护，作用是把连续探索中的可发表材料从长篇 handoff 中逐步抽出。
它不是 theorem evidence；正式数学状态仍以
当前 proof、checker、TPC_HANDOFF.md 页首及 current section 为准。

## 0.1 已发布：TPC-208 zero-hole additive edge frame

项目：`papers/tpc-208-zero-hole-additive-edge-frame/`

类型：**PROVED_STRUCTURAL_L1 / THRESHOLD_A**。

TPC-208 攻击 V60 留下的 standard-zero-hole remainder。原候选把 additive DFT拆成
equal/off-equal frequency pieces后分别估计；residue-zero spike证明这种估计顺序会把
exact zero制造成两个大项。修正后的 invariant object是 nonzero additive frequencies
上的 complete-graph Laplacian：

1. **PROVED** — `V_0=q^-1 y*P_(q-1)y`，projection rank为 `q-2`；
2. **PROVED** — complete graph给 `(q-1)(q-2)/2` 个 literal edge transforms，
   `V_0=1/[q(q-1)] sum_e |T_e|^2`；
3. **PROVED** — `sum_e|Delta_e(n)|^2=q(q-2)1_(q does not divide n)`，所以
   mandatory `(q-2)/(q-1)` coefficient diagonal在每个 edge cell内 exact删除；
4. **PROVED** — four-packet polarization逐 edge成立，contracted physical kernel为
   `0 / q(q-2) / -q`，exact返回 V59 literal scalar；
5. **PROVED** — oriented fiber
   `Delta_(k,k+d)(n)=e_q(-kn)(1-e_q(-dn))`，带 mandatory factor `1/2`；
6. **PROVED / SCOPED OBSTRUCTION** — 任意 scalar-weighted literal
   `(e_k-e_l)` decomposition中每个 edge weight都被 off-diagonal matrix entry强制为
   `1/(q-1)`，strict edge subset不可能表示 projector；
7. **REFUTED** — equal/off-equal pieces分别作 absolute estimate；residue-zero spike给
   `+(q-1)|L|^2/q` 与 `-(q-1)|L|^2/q`，总和为零；
8. **OPEN** — complete oriented `(d,k)` frame到 source-valid Kloosterman cells的
   collective transform，以及 blocks、four-packet signs与 prime shell的 fixed-saving
   reassembly。

```text
STRONGEST_POSITIVE_RESULT = EXACT_COMPLETE_GRAPH_TIGHT_FRAME_WITH_EDGEWISE_Q_MINUS_2_DIAGONAL_DELETION_AND_LITERAL_PHYSICAL_KERNEL_CROSSWALK
STRONGEST_OBSTRUCTION = EVERY_LITERAL_TWO_FREQUENCY_EDGE_IS_FORCED_SO_STRICT_EDGE_SUBSET_SPARSIFICATION_IS_IMPOSSIBLE
OPEN_THEOREM = JOINT_WHOLE_FRAME_POISSON_KLOOSTERMAN_COMPILER_WITH_FIXED_SAVING_AND_PRIME_SHELL_REASSEMBLY
REUSABLE_STRUCTURE = ZERO_HOLE_PROJECTOR_AS_COMPLETE_GRAPH_LAPLACIAN_PLUS_UNIT_ANNIHILATING_ORIENTED_DIFFERENCE_FIBERS
ROUND2_CLUE = TRANSFORM_THE_WHOLE_D_K_FRAME_BEFORE_ANY_EDGE_TRIANGLE_AND_TEST_FOR_ONE_SHARED_DUAL_VARIABLE
```

## 0.2 已发布：TPC-207 moving-hole BDH translation defect

项目：`papers/tpc-207-critical-moving-hole-bdh-defect/`

类型：**PROVED_STRUCTURAL_L1 / THRESHOLD_A**。

TPC-207 将 V59 的 translated-block distinguished-zero obstruction从 raw NO-GO升级为
一个 exact且已付款的 two-term compiler：

1. **PROVED** — `V_h=V_all-q/(q-1)|z_h-mu|^2`；changing hole是 rank-two
   projector defect，nonzero spectrum为
   `+/-sqrt(q(q-2))/(q-1)`。
2. **PROVED** — exact `(q-2)` diagonal lift：
   `R_h-R_0=q/(q-1)(|z_0-mu|^2-|z_h-mu|^2)+kappa_q(E_h-E_0)`。
3. **PROVED** — physical translation sign `h_q=-s mod q`，以及 common-origin
   four-packet polarized defect。
4. **PROVED** — centered selector `l1` mass `H/q+1`、Schwartz block separation与
   bounded overlap共同给
   `sum_(b,c)|M_(b,c)|<<J(H^2+HQ+Q^2)x^o(1)`。
5. **PROVED** — literal scales给
   `x^(53/32+o(1))=x^(5/3-1/96+o(1))`，故 translation subgate strict
   `1/400`已支付。
6. **SOURCE-LOCKED** — Harper prime row等于 standard zero-hole variance；source
   仍不证明 zero-hole prime-only signed four-packet theorem。
7. **NO_GO / SHARP OBSTRUCTION** — rank-two norm趋于一；若不使用 localized residue
   counts与 block geometry，finite rank不产生 saving。

```text
STRONGEST_POSITIVE_RESULT = PROVED_X_POWER_53_OVER_32_COLLECTIVE_MOVING_HOLE_DEFECT_BOUND
STRONGEST_OBSTRUCTION = RANK_TWO_OPERATOR_NORM_TENDS_TO_ONE_AND_ZERO_HOLE_PRIME_SIGNED_BDH_THEOREM_IS_OPEN
OPEN_THEOREM = STANDARD_ZERO_HOLE_PRIME_ONLY_Q_WEIGHTED_KERNEL_LOCALIZED_Q_MINUS_2_DIAGONAL_SUBTRACTED_SIGNED_FOUR_PACKET_BDH_POWER_SAVING
REUSABLE_STRUCTURE = NORMALIZED_CENTERED_RESIDUE_SELECTOR_PLUS_POLARIZE_THEN_INTEGRATE_THEN_ESTIMATE
ROUND2_CLUE = EXPAND_ZERO_HOLE_LEVERAGE_IN_ADDITIVE_FREQUENCIES_AND_TARGET_ONLY_OFF_EQUAL_FREQUENCIES_WHILE_RETAINING_THE_SEPARATE_DIAGONAL_F_TERM
```

## 0.3 已发布：TPC-209 whole-frame Poisson Möbius-dilation obstruction

项目：`papers/tpc-209-whole-frame-poisson-mobius-obstruction/`

类型：**PROVED_STRUCTURAL_L1 / STOP_SCOPED_FRAME_ONLY_SAVING**。

TPC-209 对 V61 的 complete additive edge frame 先做 fixed-divisor Poisson，再恢复
Möbius divisor sum。主要结果为：

1. **PROVED** — `(k,r) -> n=qr+kD` 是 fixed unit divisor 下的 exact whole-frame
   dual reindex；
2. **PROVED** — 跨 divisor 的完整 frame covariance 保留 `D,E` cross terms，并由
   multiplicative permutation `U_D` 精确描述；
3. **PROVED** — multiplicative Fourier 给出 shared-character、divisor-dependent
   profile normal form；Gauss sum exact 返回 V59 nonprincipal-character interface；
4. **PROVED / SHARP OBSTRUCTION** — `L_c` 的 operator norm 为 `||c||_2`，aligned
   profiles 达到等号；`q=5` resonance 达到 coefficient `ell^1` mass；
5. **REFUTED_SCOPED** — frame-only Poisson algebra 不推出 scalar common dual packet
   或 power saving；
6. **OPEN** — actual Möbius/Poisson profiles 的 prime-only、diagonal-corrected、
   block-reassembled nonprincipal-character bound。

```text
TPC209_ROUTE_ADVANCE = YES
TPC209_ARITHMETIC_ADVANCE = NO
TPC209_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC209_FIXED_ATOM_CREDIT = 0
TPC209_L2 = NONE
TPC209_TPC_TRIGGER = true
```

完整 proof/checker/PDF 已生成；finite QA 不是渐近证据。下一自然候选是 TPC-210
profile-aware nonprincipal-character theorem，不假设公共 scalar dual packet。

## 0.4 已发布：TPC-210 Poisson profile realizability and Mobius alignment obstruction

项目：`papers/tpc-210-poisson-profile-realizability/`

类型：**PROVED_STRUCTURAL_L1 / STOP_SCOPED_PROFILE_CLASS**。

TPC-210 检验 TPC-209 的 profile-aware 窄门：Schwartz regularity、有限 Poisson
reindexing 和 literal Mobius signs 是否已经足以排除跨 divisor 的 coherent alignment。
答案是否定的，但结论严格限定在 independent admissible profile class：

1. **PROVED** — 对每个 prime `q>2`，任意 `C^(F_q^*)` target profile 都可由 compactly
   supported smooth Fourier packet 精确实现；isolated dual nodes 与 `C_c^infty` bump
   给出有限族同时插值。
2. **PROVED** — 对 squarefree unit divisors 取 `c_D=mu(D)`、
   `B_D=mu(D)U_D^*z`，得到 exact aligned family，所有 coherent outputs 都等于同一
   centered witness `z`。
3. **PROVED** — coherent whole-frame energy 与 weighted diagonal energy 的比值恰为
   divisor component 数；`q=5` 的 two-divisor witness 精确达到 ratio `2`。
4. **PROVED** — profile-aware energy 精确化为 cross-divisor PSD Gram quadratic form
   `sum_(D,E)c_D conjugate(c_E) G_(D,E)`。
5. **REFUTED_SCOPED** — 仅凭 Schwartz/Poisson/Mobius profile admissibility，不能推出
   universal profile-level power saving。
6. **OPEN** — literal coupled TPC physical profiles 的 cross-divisor Gram bound，仍须
   保留 `(q-2)` diagonal、prime shell、kernel localization、four-packet signs 与 block
   reassembly。

```text
TPC210_ROUTE_ADVANCE = YES
TPC210_STRUCTURAL_THRESHOLD_A = PASS
TPC210_FINITE_PROFILE_INTERPOLATION = PROVED_EXACT
TPC210_MOBIUS_WEIGHTED_ALIGNED_FAMILY = PROVED_EXACT
TPC210_CROSS_DIVISOR_GRAM_REDUCTION = PROVED_EXACT
TPC210_PROFILE_CLASS_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC210_ACTUAL_PHYSICAL_PROFILE_BOUND = OPEN
TPC210_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC210_ARITHMETIC_ADVANCE = NO
TPC210_FIXED_ATOM_CREDIT = 0
TPC210_L2 = NONE
TPC210_TPC_TRIGGER = true
```

```text
STRONGEST_POSITIVE_RESULT = EXACT_FINITE_SCHWARTZ_POISSON_PROFILE_SURJECTIVITY_WITH_LITERAL_MOBIUS_ALIGNED_REALIZABLE_FAMILY
STRONGEST_OBSTRUCTION = CROSS_DIVISOR_GRAM_RATIO_EQUALS_DIVISOR_COUNT_ON_AN_ADMISSIBLE_PROFILE_CLASS
OPEN_THEOREM = ACTUAL_COUPLED_PHYSICAL_MOBIUS_POISSON_CROSS_DIVISOR_GRAM_BOUND_WITH_EXACT_DIAGONAL_AND_PRIME_SHELL_REASSEMBLY
REUSABLE_STRUCTURE = ISOLATED_FOURIER_NODE_INTERPOLATION_PLUS_MOBIUS_ADJOINT_ALIGNMENT_PLUS_PSD_CROSS_DIVISOR_GRAM
ROUND2_CLUE = FIND_A_LITERAL_PHYSICAL_CROSS_DIVISOR_COUPLING_BEFORE_ANY_NEW_PRIME_BDH_ATTACHMENT
```

The alignment construction is not claimed to be the literal coupled TPC coefficient family;
it is an interface obstruction for independent admissible profiles. Finite certificate rows
remain QA only and do not create arithmetic `L2` progress.

## 0.5 已发布：TPC-211 product-coupled Euler profiles and the truncated-boundary handoff

项目：`papers/tpc-211-product-coupled-euler-gram/`

类型：**PROVED_STRUCTURAL_L1 / STOP_SCOPED_PHYSICAL_COUPLING**。

TPC-211 把 TPC-210 的 independent profile obstruction 推进到 V46 literal product
coupling。对共同 CRT lift 的 Euler profiles，已 exact 证明：

1. **PROVED** — product cocycle、zero-axis 和 zero-mean；
2. **PROVED** — 非空 squarefree divisor family 的 rank 恰为 `2^s-1`；
3. **PROVED** — 完整 packet 的 `mu(d) log(d)` 权重压缩为 marked-prime Euler derivative；
4. **PROVED** — active prime 数至少为 2 时 common endpoint 完整取消；
5. **PROVED_STRUCTURAL_FINITE** — Gram duality 可构造 shared endpoint 实现
   `\langle w,Delta_S\rangle=mu(d_S)`；
6. **REFUTED_SCOPED** — product coupling、finite rank 和 common endpoint alone 不保证
   cross-divisor saving；
7. **OPEN** — actual transition band `Y0<d<=U` 的 boundary 与 divisor-dependent
   reciprocal emitter `A_d(r)` 的 joint Gram bound。

```text
TPC211_ROUTE_ADVANCE = YES
TPC211_STRUCTURAL_THRESHOLD_A = PASS
TPC211_PRODUCT_COUPLING_COCYCLE = PROVED_EXACT
TPC211_LITERAL_PRODUCT_PROFILE_FULL_RANK = PROVED_EXACT
TPC211_LOG_MOBIUS_PACKET_DERIVATIVE = PROVED_EXACT
TPC211_COMPLETE_PACKET_ENDPOINT_CANCELLATION = PROVED_EXACT
TPC211_SHARED_ENDPOINT_ALIGNMENT = PROVED_STRUCTURAL_FINITE
TPC211_PRODUCT_COUPLING_UNIVERSAL_SAVING = REFUTED_SCOPED
TPC211_TRANSITION_BOUNDARY_CONTROL = OPEN
TPC211_PHYSICAL_CROSS_DIVISOR_GRAM_BOUND = OPEN
TPC211_ARITHMETIC_ADVANCE = NO
TPC211_FIXED_ATOM_CREDIT = 0
TPC211_L2 = NONE
TPC211_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC211_TPC_TRIGGER = true
```

```text
STRONGEST_POSITIVE_RESULT = COMPLETE_PACKET_LOG_MOBIUS_DERIVATIVE_WITH_EXACT_COMMON_ENDPOINT_CANCELLATION
STRONGEST_OBSTRUCTION = LITERAL_PRODUCT_DEFECTS_HAVE_FULL_DIVISOR_RANK_AND_GRAM_DUALITY_REALIZES_MOBIUS_ALIGNMENT
OPEN_THEOREM = BOUND_THE_TRUNCATED_DIVISOR_BAND_AFTER_RETAINING_THE_RECIPROCAL_EMITTER_A_D
REUSABLE_STRUCTURE = BOOLEAN_PACKET_DERIVATIVE_PLUS_CUT_INCidence_PLUS_PHYSICAL_EMITTER_HANDOFF
ROUND2_CLUE = BUILD_A_BOUNDARY_WEIGHTED_DIVISOR_BAND_OPERATOR_BEFORE_ANY_NEW_PRIME_BDH_ATTACHMENT
```

完整 Bridge-B proof/checker 为
`research/tpc-big-road/bridge_b_product_coupled_physical_profiles.md` 与
`research/tpc-big-road/tpc_bridge_b_product_coupled_checker.py`。certificate 仅作有限
structural QA；不构成 arithmetic `L2`、Gate B 或 twin-prime progress。

## 0.6 已发布：TPC-212 truncated divisor bands and the reciprocal-emitter boundary operator

项目：`papers/tpc-212-truncated-boundary-emitter/`

类型：**PROVED_STRUCTURAL_L1 / STOP_SCOPED_BOUNDARY_EMITTER**。

TPC-212 把 TPC-211 留下的 actual transition band 与 divisor-dependent reciprocal emitter
拆成两个可审计的 exact interface：

1. **PROVED** — selected squarefree divisor bands 的 endpoint coefficient 是 signed
   Boolean incidence `eta_p(A)`，完整 packet 的 incidence 在至少两个 active primes 时为零；
2. **PROVED** — selected packet 等于 complete packet minus the missing-subset boundary，
   且 `t=35`, `5<d<=35` 给出 active divisors `{7,35}`、incidence `(1,0)` 与 endpoint
   leakage `log(5)`；
3. **PROVED_FINITE** — reciprocal occupancy 的平方范数等于
   `d | m1*q2-m2*q1` 的 collision sum；
4. **PROVED_STRUCTURAL_FINITE** — natural direct-sum emitter Gram 是 block diagonal，
   非零 rows full rank；
5. **REFUTED_SCOPED** — cut 与 reciprocal emitter interface alone 不产生 universal
   cross-divisor saving；unit-weight fixtures 的 coherent-to-diagonal ratios 为 `2,4,3`；
6. **OPEN** — literal physical profile coupling、smooth `psi`、prime shell 与 Gate-B
   reassembly 的共同 Gram bound。

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
TPC212_TPC_TRIGGER = true
```

```text
STRONGEST_POSITIVE_RESULT = EXACT_SIGNED_BOOLEAN_BOUNDARY_AND_RECIPROCAL_COLLISION_GRAM
STRONGEST_OBSTRUCTION = CROSS_DIVISOR_GRAM_IS_BLOCK_DIAGONAL_WITH_UNIT_WEIGHT_ALIGNMENT
OPEN_THEOREM = LITERAL_PHYSICAL_BOUNDARY_EMITTER_CROSS_DIVISOR_GRAM_BOUND
REUSABLE_STRUCTURE = CUT_BOUNDARY_OPERATOR_PLUS_RECIPROCAL_OCCUPANCY_COLLISION_GRAM
ROUND2_CLUE = COUPLE_THE_LITERAL_V46_PROFILE_AT_DIVISOR_d_TO_THE_EMITTER_BLOCK_BEFORE_CAUCHY
```

The finite certificate covers four boundary cuts, 5,810 profile coordinates, three emitter
fixtures, and nine divisor rows.  The `psi=1` emitter fixture is a modeling choice; none of
these finite rows is arithmetic `L2` evidence.

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
38. **PROVED** — V58 V35--V57 scalar crosswalk：展开 diagonal-deleted
    `G_q(t)` 并代入 exact proper-factor identity后，full-shell
    `C_*=sum_q qC_q` 逐项等于 V35 surviving centered ratio core
    `mathfrak C_x`；principal/nonunit remainders属于更大的 compensated numerator，
    不属于已 centered 的 `C_*`。
39. **PROVED** — q-weight orthogonal split：对 `v=(q)_q`、`V_*=sum q^2` 与
    `C_perp=C-(C_*/V_*)v`，exact有
    `sum|C_q|^2=|C_*|^2/V_*+||Cperp||^2`。这是 terminal scalar direction与
    maximal-prefix transverse variance的正交直和。
40. **PROVED** — exponent crosswalk：V35 scalar saving `delta`对应纵向绝对
    row-loss `tau_parallel=17/48-2delta`，故
    `delta>1/400 <=> tau_parallel<419/1200`；benchmark
    `delta=1/96 <=> tau_parallel=1/3`。
41. **PROVED** — V58 two-scalar conditional endpoint compiler：V51 full-shell
    Gate-A root与 V35 Gate-B scalar core已足以通过
    `S=(A_*-C_*+E_*)/K_*` 支付 physical endpoint；saving可取
    `min(eta_A,delta-1/400,419/2400)` 以下任意固定值，完全不使用
    `Cperp`。
42. **PROVED / ROUTE RETYPE** — Gate-B transverse row theorem只在追求全部 V57
    moving prefixes时追加。V53/V57 full row-Bessel仍是合法、更强的 maximal package，
    但不再列为 selected TPC endpoint 的必需桥墩。
43. **PROVED** — V59 complex polarization compiler：对任意 complex `x,y`，
    `x*conj(y)=(1/4)sum_(j=0)^3 i^j|x+i^j y|^2`。应用于 V36 character form后，
    V35/V58 Gate-B scalar逐项等于四个 literal sequences
    `a^(j)=beta+i^j w` 的 signed one-sequence remainders。
44. **PROVED** — V59 reduced-residue offdiagonal BDH normal form：每个 packet的
    nonprincipal character energy必须减去精确的 `(q-2)` diagonal；于是
    `mathfrak C_x=(1/4)sum_j i^j V_Q,H^circ(a^(j))`，没有 free principal、diagonal
    或 nonunit deletion。
45. **PROVED** — mesoscopic block ledger：block count `x/H=x^(11/32)`、每块
    q-weighted natural scale `Q^2H=x^(127/96)`、全局 natural scale
    `xQ^2=x^(5/3)`，并且 exact conductor gap `Q^2/H=x^(1/96)`。
46. **PROVED / SOURCE-INTERFACE CROSSWALK** — Blomer--Pascadi critical local saving
    `q^(-1/32)=x^(-1/96)` 与 V59 block gap exact对齐；这是可信的 post-emitter
    engine时钟，不是 collective theorem credit。
47. **PROVED / ROUTE RETYPE** — Gate-B当前主猜想可等价表述为四 packet的
    prime-only、kernel-localized、diagonal-corrected BDH signed remainder theorem；
    它仍须与 V51 full-shell Gate-A root共同闭合 physical endpoint。

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
9. **SOURCE_BACKED_CONDITIONAL / ARCHITECTURE ONLY** —
   Harper arXiv:2412.19644v1, Theorems 1--2：对 general complex sequences给
   reduced-residue progressions/non-concentration框架，但要求 `sqrt(2X)<Q`、使用完整
   dyadic modulus family，并带额外结构假设。把 `X` 形式上取成 `H` 暴露
   `Q^2/H=x^(1/96)`，却不提供 literal translated-block、prime-only signed remainder
   或四 packet reassembly。
10. **SOURCE_BACKED_CONDITIONAL** —
    Blomer--Pascadi arXiv:2607.24311v1, Theorem 1.1 与 Pascadi
    arXiv:2404.04239v3, Corollaries 17--18：已发射 fixed-modulus
    Kloosterman cells上存在临界 power saving；尚无从 V59 occurrence blocks到这些
    cells的 collective compiler。
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

V58 再把第二项拆成 endpoint 与 maximal 两个逻辑层。selected terminal package现在只
保留：

1. **CONJECTURAL** — V51 full-shell signed Gate-A root
   `H_A,*(eta_A)`；
2. **CONJECTURAL** — 与 `C_*` exact相同的 V35 proper-factor centered scalar
   `|mathfrak C_x|<<x^(5/3-delta+o(1))`，其中 `delta>1/400`。

`q`-transverse variance改为追求全部 prefixes时才增加的第三项 optional theorem。
这把当前终点 burden从“一 scalar + 一 whole row”收窄为“两个 signed scalars”，但
两项仍都没有 source theorem，故没有 arithmetic credit或 numbered paper trigger。

V59 把第 2 项进一步改写成一个统一的 **CONJECTURAL** polarized local-BDH theorem。
令 `a^(j)=beta+i^j w`，并令 `V_Q,H^circ(a)` 为 V59 proof中冻结的 prime-weighted、
kernel-localized、reduced-residue offdiagonal remainder。当前 Gate-B conjecture可写成

\[
 \left|\frac14\sum_{j=0}^3 i^j
 \mathcal V_{\mathcal Q,H}^{\circ}(a^{(j)})\right|
 \ll x^{5/3-\delta+o(1)},
 \qquad \delta>\frac1{400}.
\]

benchmark `delta=1/96` 与 critical fixed-cell clock对齐。真正缺少的不是第五个局部
Kloosterman bound，而是一个保留四个 literal packets、prime-only modulus shell、
`q-2` diagonal、hard kernel与 single signed reassembly的 collective block-to-cell
compiler。这个 conjecture与 V58 scalar完全相同，不叠加两份 theorem credit。

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
21. **NO_GO** — 将 reduced-residue diagonal从 `q-2` 改成 `q-1`，或直接删除
    diagonal，会改变 polarized cross term；`q=5` finite fixture分别给 `-12` 与
    `-24`，而 literal值为 `-15`。
22. **HISTORICAL NO_GO / RESOLVED BY V60 COMPILER** — ordinary block translation确实
    不保持 distinguished zero residue；模 5 raw variance fixture仍有效。但 V60 已把
    physical row exact分成 standard zero-hole row与 explicit moving-hole defect，并把
    collective defect支付到 `x^(53/32+o(1))`。因此 translation本身不再是 fatal；
    standard zero-hole prime-only signed theorem仍 OPEN。
23. **NO_GO** — all-moduli signed cancellation不能抽取 prime-only remainder：有限 rows
    `R_5=1,R_6=-1` 的 all-moduli sum为 0，而 prime subset sum为 1。
24. **NO_GO** — Blomer--Pascadi/Pascadi fixed-cell saving只在 coefficients与
    Kloosterman arrays已经发射后生效；它不自动生成 V59 occurrence-to-cell compiler、
    block norms、tails或 collective signed reassembly。
25. **NO_GO** — zero-hole DFT的 equal/off-equal pieces不能分别作 absolute estimate；
    residue-zero spike的两项分别为 `+(q-1)|L|^2/q` 与
    `-(q-1)|L|^2/q`，而 true variance exact为零。
26. **NO_GO / SCOPED** — literal two-frequency edge family不能用 strict subset
    sparsify。projection的每个 off-diagonal entry只由对应唯一 edge贡献，强制全部
    weights为 `1/(q-1)`。dense basis或 whole-frame theorem未被排除。

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
| 2026-08-12 | V57 | longitudinal root anchor、uniform prefix-error payment、Gate-B row maximalization与 root-plus-transverse package | **PROVED + SOURCE_BACKED_ARCHITECTURE + CONJECTURAL + NO_GO** |
| 2026-08-13 | V58 | V35--V57 scalar crosswalk、q-weight direct sum、delta/tau translation与 two-scalar endpoint compiler | **PROVED + SOURCE_BACKED_ARCHITECTURE + CONJECTURAL + NO_GO** |
| 2026-08-13 | V59 | four-packet complex polarization、reduced-residue BDH normal form、mesoscopic `1/96` clock与 collective compiler obstruction | **PROVED + SOURCE_BACKED_CONDITIONAL + CONJECTURAL + NO_GO** |
| 2026-08-17 | V60 | moving-hole projector、exact diagonal lift与 `x^(53/32+o(1))` collective translation payment | **PROVED_STRUCTURAL_L1 / TPC-207** |
| 2026-08-17 | V61 | complete-graph zero-hole additive edge frame、edgewise diagonal deletion与 literal-edge no-sparsification | **PROVED_STRUCTURAL_L1 / TPC-208** |
| 2026-08-18 | V65 | truncated divisor-band Boolean boundary、reciprocal occupancy collision Gram 与 scoped emitter-only obstruction | **PROVED_STRUCTURAL_L1 / TPC-212** |

下一次更新应优先回答：

1. 能否把 literal V46 product-coupled profile、truncated boundary 与 smooth reciprocal
   emitter编成一个真实的 cross-divisor Gram theorem；必须先于 direct-sum Cauchy与任何
   outer absolute，并保留 prime shell、four-packet signs与zero-axis normalization；
2. 在上述 coupling theorem 成立后，能否对完整 oriented `(d,k)` tight frame统一作 Möbius/Poisson transform，并在任何
   edge/fiber triangle之前暴露一个 shared dual variable，从而集体编译到同一批
   Blomer--Pascadi/Pascadi cells并完成 prime-shell signed reassembly；
3. 能否对 V51 full-shell mixed-plus-balanced signed root证明一个 fixed-power saving；
4. 能否对 exact相同的 V35/V58/V59 proper-factor centered scalar证明
   `delta>1/400`，优先瞄准 benchmark `delta=1/96`；
5. 若需要 maximal Gate-A，能否只对 `Cperp` 证明 one-`Q` transverse variance，
   而不重新要求完整 Gate-B row；
6. 能否对 V56 预声明的全部 large dyadic nodes证明同一个 uniform literal block
   theorem，作为 Gate-A maximal fallback；
6. 能否在 V52 packet层直接证明
   `(delta_B+delta_W)/2+kappa>1/400` 的 joint angular dispersion；
7. 能否对任一 literal row的 transverse projection证明 one-`Q` variance，并由 V54
   paid difference传给另一 row；
8. BP/MQW/KSWX local cells能否在不拆 compensation与 within-row cancellation的前提下
   合法 reassemble成上述 pre-`q` theorem；
9. unbounded Siegel-quality world能否沿既有 source-backed fixed-`h=2` 通道直接退出；
10. 能否把 V54--V59 exact diagonalization、polarization、scalar crosswalk与 maximal transfer
   抽象成一篇不依赖 TPC终点的 standalone structural note；
11. 能否把 V56 maximalization与一个非 TPC-specific weighted endpoint application组合，
   使其达到 standalone structural note 的“成稿门槛 A”；
12. 哪个候选最先满足“成稿门槛 A”。
