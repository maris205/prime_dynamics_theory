# TPC HANDOFF

更新时间：2026-08-06
交接状态：`SEALED_FOR_NEW_SESSION`

第 57 节从已发布 V9 commit
`cd983e193fedfd6a274e52a84be69fecf0f0a26e`继续同一个 canonical
`TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE`。V10 完成 V9 留下的第一段
squarefree/imprimitive CRT，但精确结果要求重写 full-source contract。若
`q=rs`、`r=cond(chi)`、`chi=Ind_r^(rs)psi`，则

```text
tau_q(conjugate(chi),a)
 =psi(a conjugate(s)_r)tau_r(conjugate(psi),1)c_s(a)1_((a,r)=1).
```

恢复 physical `chi(-2)conjugate(chi)(g)` 并乘 source
`mu(gq)/phi(q)` 后，cofactor 的两枚 `mu(s)`精确相消；normalized character
coefficient保留 `mu(g)mu(r)r/[phi(r)phi(s)]`、B-polynomial中的 `c_s(ell)`、
root-number square与强制相位
`psi(-2 ell conjugate(g)_r conjugate(s)_r^2)`。因此
`HB4_EXACT_HALF_LITERAL_MU_GQ_PRESERVATION_THROUGH_IMPRIMITIVE_CRT`
已精确 `STOP_SCOPED_FALSE_EXACT_COFACTOR_SIGN_CANCELLATION`。这不允许把
`c_s(ell)`取绝对值：若 `d_s=(s,ell)`、`t_s=s/d_s`，则
`c_s(ell)/phi(s)=mu(t_s)/phi(t_s)`。

对 composite primitive conductor，primitive orthogonality又把单一 product residue
改成 `rho|r` 的 divisor-projector lattice。打开两枚 primitive Gauss sums并写
`r=rho t` 后，outer `mu(r)`把 projector sign变为 `mu(rho)`，同时
`phi(rho)`与 `phi(r)`中的同一因子精确相消。再展开
`c_s(ell)=sum_(a|s,a|ell)a mu(s/a)`、写 `s=ab, ell=ak`，完整 additive normal
form的关键 cell为

```text
mu(g)mu(rho)mu(b) a/[phi(t)phi(a)phi(b)]
 * mu(e_1)mu(e_2)W(...)c_g(ak)
 * S(1,-2u k conjugate(g e_1e_2 a b^2 t^2);rho).
```

这是真正的 V10 路线推进：三条 coupled signed axes
`mu(g)mu(rho)mu(b)`与一个 literal inverse-square monomial，而不是可自由调用的
`mu(q)`。complex sextic induced-character、composite conductor `r=15`、primitive
projector/Kloosterman lattice、physical
`-2*conjugate(g)_r*conjugate(s)_r^2`与 Ramanujan monomial均由 checker
exact验证并有 mutation tests。

[Earnst](https://arxiv.org/abs/2603.22124) 的 prime-conductor
root-number-square moment与
[Fouvry--Kowalski--Michel--Sawin](https://arxiv.org/abs/2511.09459) 的 prime
monomial trace-function bound是当前最接近的 mechanism/adaptation blueprints；它们
分别缺 actual `E_1E_2HB` coefficients，或缺 varying/composite `rho`、outer
`mu(rho)`与完整重组，故没有 theorem credit。当前 selected construction重写为
`HB4_EXACT_HALF_SIGNED_CONDUCTOR_RAMANUJAN_COFACTOR_PRIMITIVE_PROJECTOR_DUAL_TYPE_IV`。
V10裁决为
`CHANNEL_RETYPE_WITH_EXACT_INDUCED_CRT_AND_PRIMITIVE_PROJECTOR_LATTICE`，不是
arithmetic advance。TPC-207仍为 false；fixed-atom credit=`0`、strict
`1/400=UNPAID`、`L2=NONE`，prime first gate、paired-Voronoi reserve、Bridge B与
第 6 节全部旧 STOP cells均不变。

第 56 节本轮启动基线为
`cfe26af99bed702aad5d346100a39134c3ac8520`，与 `origin/main`一致；启动
`git pull --rebase origin main`返回 already up to date。启动时
`TPC_HANDOFF.md` SHA-256为
`8cf2a59c05f77e270a217a6849bcaba877287cfaf68f116c9e780d24eeb381d8`；
tracked/cached diff为空。130 个既有 protected untracked files原样保留，其 canonical
manifest为 `9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1`。
第 1 节 22 项只读启动回归为 `22/22 PASS`；TPC-27--32 legacy writers与
TPC-122 writer均未执行。

V9 继续同一个 canonical
`TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE`，但不再把 prime first wall停留在
抽象 character angle。对 raw additive dual weights
`U_p^sharp(z)=sum_h U(h)e_p(zh)`、`V_p^sharp`同理，完整 prime cell精确等于

```text
mu(p)Q_p(-2),
Q_p(-2)=sum_(e_1e_2zw=-2 mod p)
 mu(e_1)W_1(e_1)mu(e_2)W_2(e_2)U_p^sharp(z)V_p^sharp(w).
```

nonprincipal Gauss angle精确为
`(p-1)/p[Q_p(-2)-M_p/(p-1)]`。checker在 `Z[zeta_p]`中 exact验证 physical
Kloosterman与 fixed-product两种表示，并冻结 principal、`z,w!=0`、`-2`、inverse、
conjugation与所有 `p/(p-1)` normalization。这是
`PROVED_EXACT_EQUIVALENCE`，不是 arithmetic saving。

V8 的 common-`k` construction不能覆盖完整模比 fiber：相同比例满足
`be-ah=tp`，只有 `t=0`是 rational common-`k` ray，`t!=0`是 coefficient
`mu(e_t+ak)`的 affine wrap。故
`COMMON_K_AS_UNIQUE_MODULAR_RATIO_FIBER=STOP_SCOPED_FALSE_COVER_NONZERO_WRAPS`。
完整 moving-unit Cauchy也有 exact `h_1 ell_1=h_2 ell_2` product-resonance floor，
只返回 endpoint，记为 `STOP_SCOPED_EXACT_ENDPOINT_PRODUCT_RESONANCE`。

当前 first subgate更新为
`HB4_EXACT_HALF_ACTUAL_ATOM_DUAL_PRODUCT_DISPERSION = FIRST_SUBGATE_OPEN_NEW_THEOREM`；目标是对
`p asymp F^2`的 frozen source superclass证明 normalized centered discrepancy
`F^(2-eta)`，等价 physical prime cell `F^(4-eta)`。任意 `eta>0`给 exact-half
power saving；支付旧 strict `1/400`须在全部 polynomial losses后 `eta>1/100`。
actual atom membership与 dual tails仍是显式 attachment gate。Mohammadi与
Bourgain--Garaev只提供 exponent不足的 local inverse-product sublemma；普通
已核查的 `d_4`/BV/BDH source不接受 prescribed residue、两条 literal Möbius rows与
modulus-dependent dual weights。

V9 当时的 selected construction为
`HB4_EXACT_HALF_SIGNED_MODULUS_DUAL_TYPE_IV = SELECTED_CONSTRUCTION_OPEN_NEW_THEOREM`：在 full
squarefree `g,q` average中保留 `mu(gq)`、两条 literal Möbius rows与 centered
product-difference resonance，禁止 prime/outer-variable层先取绝对值。HB4xHB2
paired-Voronoi仍是不可拼接的 independent reserve。本轮裁决为
`CHANNEL_REDESIGN_WITH_EXACT_GAUSS_DUAL_PRODUCT_NORMAL_FORM_AND_TYPED_TYPE_IV_TARGET`，
不是 arithmetic advance。TPC-207仍为 false；fixed-atom credit=`0`、strict
`1/400=UNPAID`、`L2=NONE`，第 6 节全部旧 STOP cells与其余 OPEN parents均不变。

第 53 节本轮启动基线为
`5e277223c025921748681f407861c8555bc50e31`，与 `origin/main` 一致；启动
`git pull --rebase origin main` 返回 already up to date。启动时
`TPC_HANDOFF.md` SHA-256 为
`9b0cf24ee85a21a591a7fbe8027a9396a114c5f74083dcaf7e968d0617d27a23`，
`TPC_COMPASS.md` SHA-256 为
`e871bbdeadb13697e4f02fbf9cd128db32959071343c401a725aff563550f8ef`；
tracked/cached diff为空。130 个既有 protected untracked files 的 manifest为
`9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1`。
第 1 节 22 项只读启动回归为 `22/22 PASS`；TPC-27--32 legacy writers与
TPC-122 writer均未执行，所有既有 untracked原样保留。

第 54 节从已发布 V2 commit
`3b3a39b7816ab5b8848999c2e23577b32de2f360`继续执行，并经 V3 的
coarse comparison与 V4 adversarial audit形成当前大路。最重要的状态修正不是
微小补丁：原先 coarse comparison 的 universal Type II并非 `OPEN`，而是
`STOP_SCOPED_FALSE_MOD3_RANK_ONE`。取合法 `M=X^(1/3)` block并令
`xi_m=1_(m=1 mod 6), kappa_n=1_(n=1 mod 6)`，则支撑上
`mn+2=0 mod 3`；Mangoldt项除 `3^j`外消失，而 comparison在 `asymp X` 个数对上
保持正质量。因此该 bilinear discrepancy为 `-cX+o(X)`，不可能有任意 log saving。

这不撤销 V3 的 one-sided成果：coarse
`b^(2)(n)=2C_2 1_(n odd) product_(p|n,p>2)(p-1)/(p-2)`仍精确匹配每个
multiplier slice的 `m/phi(m)` main，Ford--Maynard `(b.1)/(b.2)/(w)`与每个固定
`gamma<1/2` 的 maximal Type I继续成立。它只说明逐 multiplier matching不足以
控制 arbitrary two-sided tests。

V4 replacement为 tensor-local hybrid：对 `z>=2`，

```text
C_(2,>z)=product_(p>z)(1-1/(p-1)^2),
b^(z)(n)=C_(2,>z)
 product_(p<=z)[p/(p-1) 1_(p does not divide n+2)]
 product_(p|n,p>z)(p-1)/(p-2).
```

它在 `z=2`精确回到 coarse comparison；对每个 `p<=z`保留完整 forbidden
product-residue mode，对 `p>z`保留 divisibility projection。两类 local factor
均值为 `1`，multiplier conditional factor均为 `p/(p-1)`，故 hybrid local Euler
profile与全部 multiplier main terms已经 `PROVED_EXACT`。遗漏 prime `p`的 tensor
cut contribution为 `Theta(X/p)`，所以一次固定 Ford--Maynard saving `B`必须取
`z=log^K X`且 `K`大于完整 loss ledger；fixed cutoff不能工作。

当前严格 ledger为：

```text
COARSE_COMPARISON_TYPE_I = PROVED_SOURCE_BACKED
COARSE_COMPARISON_UNIVERSAL_TYPE_II = STOP_SCOPED_FALSE_MOD3_RANK_ONE
HYBRID_LOCAL_EULER_PROFILE = PROVED_EXACT
HYBRID_b1_w = PROVED_SOURCE_BACKED_FOR_EACH_FIXED_K
HYBRID_b2_AT_P_TPC = VACUOUS_PROVED_R_EMPTY
HYBRID_MAXIMAL_TYPE_I_GAMMA_LT_HALF = PROVED_SOURCE_BACKED
HYBRID_MAXIMAL_TYPE_I_GAMMA_EQUAL_HALF = NOT_PROVED_BY_BV
HYBRID_UNIVERSAL_TYPE_II_J_TO_SQRT = OPEN_HIGH_CONDUCTOR_WALL
H3_U_UNIVERSAL_FORK = OPEN_RESERVE_OVERSTRONG
H3_S_PROP722_GENERIC_CLOSURE = DEPRIORITIZED_BROADER_THAN_NEEDED
DIRECT_HB2_EXTRACTOR = PROVED_EXACT_REDUCTION_TO_SHB_D2
SHB_D2_MASTER = SELECTED_PRIMARY_OPEN_NEW_THEOREM
HB2_B3_MINIMAL_CORE = SELECTED_PROVISIONAL_OPEN_NEW_THEOREM
BC_COROLLARY1_DIRECT_ATTACHMENT = STOP_SCOPED_GROUPED_COR1_SCALE_NO_SAVING
ONE_POISSON_BC1_QUARTER = STOP_SCOPED_FIRST_SUMMAND_NO_NEW_RANGE
NAIVE_NATIVE_TWO_STAGE = STOP_SCOPED_AT_QUADRATIC_DIAGONAL
HB4_QUARTER_COLLECTIVE_MAIN = PROVED_SOURCE_BACKED_ALL_D_ATTACHMENT
HB4_QUARTER_RAMANUJAN_AXES = PROVED_X3_OVER_4_POWER_SAVING
HB4_QUARTER_WEIL_OFFDIAGONAL = PROVED_FOR_1_OVER_4_LT_DELTA_LT_1_OVER_3
HB4_QUARTER_PASCADI_OFFDIAGONAL = PROVED_FOR_1_OVER_3_LE_DELTA_LT_3_OVER_8
HB4_LOW_CONDUCTOR_PROJECTOR = PROVED_GAUSS_CRT_PLUS_PRIMITIVE_LARGE_SIEVE
HB4_HIGH_CONDUCTOR_INCIDENCE = PROVED_FOR_3_OVER_8_LE_DELTA_LT_1_OVER_2
HB4_QUARTER_OFFDIAGONAL = PROVED_FOR_1_OVER_4_LT_DELTA_LT_1_OVER_2
HB4_EXACT_HALF_ENDPOINT = OPEN_LOG_POWER_ENDPOINT
BP2607_FIXED_UNIT_LOCAL_ENGINE = SOURCE_ATTACHED_F_MINUS_1_OVER_16_SAVING
BP2607_AFTER_FREEZE_AND_OUTER_TRIANGLE = STOP_SCOPED_F_15_OVER_16_DEFICIT
BP2607_ARBITRARY_UNIT_VECTOR_LIFT = STOP_SCOPED_FALSE_CHARACTER_EIGENMODE
HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION = SELECTED_PRIMARY_OPEN_NEW_THEOREM
HB4_EXACT_HALF_SOURCE_WEIGHT_ENVELOPE = FROZEN_TESTABLE_SUPERCLASS_CONTRACT
HB4_EXACT_HALF_ACTUAL_ATOM_MEMBERSHIP = OPEN_ATTACHMENT
HB4_EXACT_HALF_PRIME_GAUSS_DUAL_PRODUCT_IDENTITY = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PRIME_CENTERED_DUAL_PRODUCT = PROVED_EXACT_EQUIVALENCE
COMMON_K_AS_UNIQUE_MODULAR_RATIO_FIBER = STOP_SCOPED_FALSE_COVER_NONZERO_WRAPS
GLOBAL_MOVING_UNIT_CAUCHY = STOP_SCOPED_EXACT_ENDPOINT_PRODUCT_RESONANCE
MOHAMMADI_WEIGHTED_A0_ATTACHMENT = SOURCE_BACKED_LOCAL_SUBLEMMA_EXPONENT_INSUFFICIENT
BOURGAIN_GARAEV_N3_ATTACHMENT = SOURCE_BACKED_LOCAL_SUBLEMMA_EXPONENT_INSUFFICIENT
DIRECT_LOCAL_BOX_TO_ENDPOINT_COMPILATION = STOP_SCOPED_NORMALIZATION_AND_EXPONENT_DEFICIT
STANDARD_LEVEL_OF_DISTRIBUTION_ATTACHMENT_IN_CHECKED_SOURCES = ABSENT
HB4_EXACT_HALF_ACTUAL_ATOM_DUAL_PRODUCT_DISPERSION = FIRST_SUBGATE_OPEN_NEW_THEOREM
HB4_EXACT_HALF_INDUCED_GAUSS_CRT_SIGNED_PHASE_IDENTITY = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PHYSICAL_MINUS_TWO_G_S_UNIT_PHASE = PROVED_EXACT_SOURCE_LOCK
HB4_EXACT_HALF_LITERAL_MU_GQ_PRESERVATION_THROUGH_IMPRIMITIVE_CRT = STOP_SCOPED_FALSE_EXACT_COFACTOR_SIGN_CANCELLATION
HB4_EXACT_HALF_RAMANUJAN_COFACTOR_GCD_STRATIFICATION = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PRIMITIVE_PROJECTOR_SINGLE_FIXED_PRODUCT = STOP_SCOPED_FALSE_DIVISOR_LATTICE
HB4_EXACT_HALF_RAMANUJAN_DIVISOR_MONOMIAL_UNFOLDING = PROVED_EXACT_FINITE
EARNST_ROOT_NUMBER_SQUARE_PRIME_MOMENT = SOURCE_BACKED_MECHANISM_ANALOGUE_NOT_ACTUAL_PACKET
FKMS_PRIME_MONOMIAL_TRACE_ENGINE = SOURCE_BACKED_LOCAL_ADAPTATION_BLUEPRINT
HB4_EXACT_HALF_SIGNED_MODULUS_DUAL_TYPE_IV = RETYPED_PRE_CRT_SHORTHAND_ONLY
HB4_EXACT_HALF_SIGNED_CONDUCTOR_RAMANUJAN_COFACTOR_PRIMITIVE_PROJECTOR_DUAL_TYPE_IV = SELECTED_CONSTRUCTION_OPEN_NEW_THEOREM
LARGE_D_HB2_SWITCH = PROVED_EXACT_COEFFICIENTWISE
LARGE_D_QUOTIENT_MOBIUS_GATE = SUPERSEDED
HB4xHB2_NAIVE_RESIDUE_COMPRESSION = STOP_SCOPED_ADDITIVE_DIFFERENCE_KERNEL_NORM_Q
HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI = INDEPENDENT_OPEN_NEW_THEOREM
HB4xHB2_PAIRED_VORONOI_FIRST_TRANSFORM = DERIVED_SOURCE_BACKED
HB4xHB2_COLLECTIVE_POLAR_MAIN_ATTACHMENT = OPEN_NEW_ATTACHMENT
DIRECT_DFI_ROW_BY_ROW = STOP_SCOPED_F7_VERSUS_F4
FM_P_TPC_J_TO_SQRT_TO_Q_COMPILER = PROVED_EXACT_CONDITIONAL
```

Ford--Maynard exact parameter仍为
`(gamma,theta,nu)=(1/2,133/400,67/400)`；其 literal lower window、mirror
`Q=267/400`与 `Q+(Q-J)=1+1/400`全部精确。hybrid H1/H2现已由
fundamental lemma与 maximal Bombieri--Vinogradov闭合；只有 H3真正闭合后才
产生 prime-producing conclusion。strict `1/400`仍为 `UNPAID`。

另有一个 exact formula-level bridge：
`Lambda(mn+2)=sum_(dr-mn=2)mu(d)log r`逐 coefficient命中 TPC-31 next gate的
prime--Möbius core `mu(d)log ell`（`r=ell`）。`omega_D/psi_L`、residue/mask、
three channels、scales与 provenance全部尚未附着；因此这不是 O161 packet theorem。
展开后的 source难点精确为一个 fixed rough `mu(d)`加两组 factor coefficients，
不是三组 independent arbitrary weights。bounded primary scan中没有 literal theorem。
universal high-conductor `U`在合法 `K=K(B)`量词下无已知反例但过宽，保留为
reserve；沿 Proposition 7.22的通用 `S+` closure会保留 largest-prime fragmentation
与至多 `60+19` 个通用 slots，逻辑上可行但已降为 broader-than-needed reserve。

current selected route直接将 modified Heath--Brown identity取最小安全值 `h=2`作用于
`w_x^(z)(n)=Lambda(n+2)-b_x^(z)(n)`。perfect-power branch由该 literal sequence的
`x^(1/2+o(1))` bound吸收，其余只有 `j<=2`、最多四个 variables。first-large
complement与 `R(P_TPC)=empty`把每项 exactly-once送入已证 H2 at `gamma=J`或
exact `(X/2)^J<M<=sqrt(X)`的 structured master `SHB-D2`。direct extractor已经
`PROVED_EXACT_REDUCTION_TO_SHB_D2`；`SHB-D2`本身仍为新的 selected open theorem，
并须自行支付 closed square-root endpoint。

V5 range atlas进一步锁定 `h=2,j=2`的 bare central core
`dr-c e_1e_2=2`，其 literal rough weights为 `mu(d)mu(e_1)mu(e_2)`。BC determinant
corollary在把 `e_1e_2`卷成一个 arbitrary sequence后类型可接，但完整 error为
`X^(11/10)D^(17/20)`而无 saving；HB4 quarter lift的一次 Poisson虽形成
三线性 reciprocal phase，但 published bound第一项在 nonzero range无 saving，故
伪 `D<X^(2/7)` window已 `STOP_SCOPED`。

V6 对 factorized HB4 quarter lift完成了真正的第二段推进。保留两个 smooth quarter
variables作双 Poisson后，full-`D` Möbius Euler germ与 short-fiber fundamental-lemma
compiler逐同一 family闭合 collective `h=0` hybrid main；单个 dyadic `D`仍没有
自然 comparison main。Ramanujan轴为 `X^(3/4+o(1))`，Weil先覆盖
`1/4<delta<1/3`。再把 `a=e_1e_2`卷成 modulus-dependent residue coefficient，
其 `L^2`平方精确化为 `d|(h_1a_2-h_2a_1)`的 multiplicative incidence，合法代入
Pascadi Theorem 10.3 的完整五项 bound后把 source-backed range推进到
`1/4<delta<3/8`。`delta=3/8`没有 saving。naive HB2 second Cauchy已在 quadratic
CRT diagonal `STOP_SCOPED`。

V7 又对同一个 incidence coefficient作 exact conductor projection，而不是误用
all-character large sieve。高导 `cond(chi)>=F`由 primitive large sieve把 coefficient
norm降到 `sqrt(F)D X^o(1)`后进入 Pascadi完整五项；低导连同 principal保留 exact
Kloosterman character transform，squarefree CRT给 primitive Gauss square乘
Ramanujan cofactor，两次 primitive large sieve给 physical `X^(7/8+o(1))`。故同一
HB4 quarter family已对每个 fixed `1/4<delta<1/2`得到 power saving；exact
`delta=1/2`的 high part仍只有 `X^(1+o(1))`，无任意 log saving。

V7 还用 exact order-two Heath--Brown identity `Lambda=2A1-A2`把
`D>sqrt(X)`的 large divisor逐系数改写为 `A1-A2`。旧 quotient-Möbius对象不再是
唯一 first missing；新的 hard cell是四个 literal Möbius slots对两个 ordered
divisor-log/Eisenstein columns的 `ER-AB=2` bilateral determinant。它有合法的
paired divisor-Voronoi/Estermann--Kuznetsov接口；现有 BC在 literal展开后无
balanced-quarter saving，当前 Pascadi map则尚未附着 simultaneous second-row
incidence/range/`L^2`。

因此第 54.8--54.19 节给出覆盖第 54.5--54.7 旧 V3 status段的 V7 theorem base，
第 55 节记录 V8 route priority，第 56 节控制当前 V9 exact normal form与新
STOP/OPEN边界。V7裁决仍是
`ARITHMETIC_HB4_FIXED_SUBHALF_RANGE_ADVANCE_AND_LARGE_D_EXACT_RECOMPILATION_NOT_TPC_TRIGGER`；
V8裁决为 `CHANNEL_REDESIGN_WITH_SOURCE_BACKED_LOCAL_ENGINE_AND_EXACT_OBSTRUCTIONS`。
V9裁决为
`CHANNEL_REDESIGN_WITH_EXACT_GAUSS_DUAL_PRODUCT_NORMAL_FORM_AND_TYPED_TYPE_IV_TARGET`。
TPC-207仍为 false；fixed-atom credit=`0`、strict `1/400=UNPAID`、`L2=NONE`，
第 6 节全部旧 cells及 H3/H4边界不变。以下第 53 节页首叙述是 V2发布快照，
其余 V2 theorem与 STOP/OPEN边界继续有效。

第 53 节参考 `TPC_review3.md` 启动的不是第 52 节又一项微型 source audit，而是
`BOLD_CHANNEL_V2` 大路重构。主控与三个 read-only agents完成 source lock、typed
architecture和 adversarial audit，并建立未编号 working artifact
`research/tpc-big-road/`。本轮发现并修正 V1 的两个关键设计错误：

1. critical physical diagonal不以 full-cycle Haar mean为正确 endpoint中心；标准
   Hardy--Littlewood/Mertens normalization heuristic给 ratio
   `exp(2gamma)/4=0.793054740...`，故 `ell_X(W)=o(a_kX)` 标为
   `HEURISTICALLY_MISCENTERED / DEPRIORITIZED`，不是 theorem target；
2. `W_(k+1)` 含来自 `R_p1` 的逐 prime forcing，mean/complement是 triangular
   forced cocycle，不是 invariant contracting splitting。

正面 theorem-state推进是 exact CRT resonance product现已无条件展开并求和：对任意
integer interval `I`，

```text
|sum_(d in I)(K_q(d)-1)|
  <= 6 product_(5<=p<=q)(1-2/p)^(-2),
```

结合 Abel summation与 exact `alpha(q)^2D(q)=1/6`，得到 profinite Haar moving sum
`Var<=X/2+O(1)`，从而 Haar-a.e. moving recurrence。因此
`H3_METRIC=PROVED_HAAR_MOVING_VARIANCE_O_N`。该结果不包含 distinguished seed
`0`；pointed recurrence由 exact event identity与 TPC等价，继续为
`ENDPOINT_EQUIVALENT_TARGET`，不能由 a.e. statement升级。

Review3 的四路合流也已分型：primorial incidence到 `W_k` 与 TPC-32/O161到
TPC-34/37 Gram energy是两个 exact connected components；packet quadratic data不能
逆生 pre-TT-star linear signs，当前也没有 coefficientwise packet-to-primorial map。
direct composition因此新增一个 broad `STOP_SCOPED`，但 analytic far-copy、两个
O161 pointwise parents、pair-native reroute、legacy H1与 global architecture保持
`OPEN`。新主干只保留
`PARITY_BREAKING_AFFINE_PATTERN_TRANSFERENCE_THEOREM`：general affine
decomposition、uniform Type I、determinant-uniform Type II、target-coupled
reassembly、physical cover/normalization/loss ledger，最后进入 prime-producing
lower bound。

Ford--Maynard source lock确认 Type II确是合格框架，但两个直接 instantiation均先于
`m=2` Type I fail：normalized survivor with `b=1`有 `w_(2n)=-1`；shifted-prime
with `b=1`也有 linear parity bias。locally matched comparison尚未构造；即使修复，
multiplicative `mn` Type II仍为真正 first large wall，不能由本轮 additive covariance
推出。

本轮因此是 `CHANNEL_REDESIGN_WITH_H3_METRIC_ADVANCE`，不是 arithmetic advance。
fixed-atom credit=`0`，strict `1/400=UNPAID`，`L2=NONE`。没有 TPC-207 trigger、
编号论文或 PDF。

上一轮第 52 节启动基线为
`10efbe0de1d08b512ae765d2c30230b23940f72a`，与 `origin/main` 一致；启动
`git pull --rebase origin main` 返回 already up to date。启动时
`TPC_HANDOFF.md` SHA-256 为
`26205b4fda4eb1bb5d1df693514d204558db3e2417c138de3a9223cdddda2ab7`，
tracked/cached diff 均为空；127 个既有 protected untracked files 的 manifest
仍为
`35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f`。
第 1 节 22 项只读启动回归为 `22/22 PASS`；TPC-27--32 legacy writers 与
TPC-122 writer 均未执行。

上一轮正式写入与回归期间，工作区依次晚到启动 manifest中不存在的 untracked
`TPC_review1.md`、`TPC_review2.md` 与 `TPC_review3.md`。用户明确要求参考前两份，
第三份也只读纳入 route-portfolio审阅；主控没有创建、修改、删除或 stage这三份
文件，也不推断其来源，按并行工作保护政策原样保留。故发布前 protected untracked
现为 130 files，manifest为
`9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1`；排除这三份
late files后的原 127-file manifest仍精确等于启动值
`35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f`。

第 52 节执行的是全局路线罗盘，不是第 49--51 节 small-content gate 的又一项
局部修补。它 source-lock RH-1--4、TPC-1、已发表的 prime--logistic heuristic
与非自治 dynamical Borel--Cantelli theorem pattern，并把四个经常被混同的对象
彻底分开：band-merging critical kneading word `RLR^infinity`、`u_c`-ACIP 的
typical orbit、exact prime kneading word、以及随算术 cutoff 移动的 finite-sieve
diagonal orbit。

大胆但精确的结论是：TPC 的动力学路线确实可以压缩成一条短的
nonautonomous rare-event/measure spine；但 literal
“`RLR^infinity` 对应轨道遍历，所以有无穷多个 gap-2”是错误对象。
`RLR^infinity` 的 critical orbit最终固定在 `R`，其 shift orbit closure只有三个点；
`f_(u_c)` 的遍历性属于 ACIP-a.e. typical points，而不是该指定 critical orbit。
相反，typical `u_c` orbit 的 `LRL` cylinder有正 ACIP measure，却没有算术素数
语义。exact prime word上的 `LRL` visit与 twin pair逐点等价，但其普通自然时间
Cesaro measure满足 `pi_2(N)/N <= pi(N)/N -> 0`，不能由固定正测度的普通
Birkhoff/Poincare recurrence推出。

合法的修复是 moving/shrinking target。若同一 stage-preserving nonautonomous
system给出非循环的 exact gap-2 event intertwiner、正确 evolution/path measure、

```text
p_n = mu_n(E_(2,n)) >= c/(log(n+2))^2,
sum_n p_n = infinity,
Var(sum_(n<=N) 1_(E_(2,n))) << N,
```

并且 corresponding Borel--Cantelli full-measure set真实包含指定 arithmetic seed，
则沿平方子序列的 Chebyshev--Borel--Cantelli 已足以推出无穷多 hits，进而推出
无穷多 twin primes。这里“正测度”的正确含义是
`(log n)^2 p_n` 保持正下界或至少 `sum p_n=infinity`，不是 fixed positive
ordinary invariant mass。RH-3 已给 abstract sequential covariance/Birkhoff
architecture；现缺 exact stage/event crosswalk、actual logarithmic schedule 的
moving-target tower/cocycle attachment、noncircular mass law与 distinguished-seed
genericity。Hénon 的 exact area preservation/reversibility不提供 logistic factor、
event pullback或 measure pushforward，因此只保留为 optional auxiliary route。

这条 repaired route保持 `OPEN`，但当前为 `CURRENT_THEORY_GAP`，不是 theorem
advance。第 52 节只新增一个 broad direct-composition `STOP_SCOPED` cell，停止把
当前 RH-1--4/TPC-1 objects直接拼成 twin infinitude；不停止 strengthened
stage isomorphism、nonautonomous tower、rare-event mass/covariance theorem、
distinguished-orbit DBC、Hénon factor theorem或 TPC-1 prime-sensitive bridge。
没有 TPC-207 trigger、编号论文、PDF或 L2 credit。

用户随后要求保留 200+ research nodes的价值但停止论文式碎片化，并把它们压缩为
“major obstruction classes -> two bottlenecks -> one bold channel”。主控据此新增根级
`TPC_COMPASS.md`：它把旧节点蒸馏为 13 类可复用 firewall，把 analytic far-copy与
dynamical pointed recurrence视为同一 physical complement-cancellation问题的两种
坐标，并提出唯一 Primorial Diagonal Renormalization Channel。该文件集中维护
H0--H4、circularity kill tests、direct analytic与 nonautonomous logistic carrier两个
proof engines；不是论文、不是 theorem evidence，也不改变本页 fail-closed状态。
它还在同一 profinite probability system中补齐 typed replication--deletion operators、
Haar mean projector、moving targets与 physical diagonal functional，并由 CRT导出
`Cov(Z_m,Z_n)` 的 exact shifted local-product identity；该 identity是合法 derived
channel progress，但其 resonance sum、one-sided physical discrepancy与 pointed
recurrence仍全部 `OPEN`。

第 51 节继续锁定第 50 节的同一 small-content far-copy 物理对象，并分别审核
source-averaged Mellin、exceptional-character、many-auxiliary-modulus 与 shifted
determinant-fiber 四条真实路线。对一个在选择辅助素数 `q` 前已经固定、且与 `q`
无关的 actual source sequence，primitive multiplicative large sieve 确实给出新的
派生 `L1`：

```text
Avg_(q asymp J) 1/(q-1) sum_(chi!=1) |a_q(chi)|^2
  << X^o (Q/J^2) ||A||_2^2.
```

但 TPC-37 只给 target spectrum 的 unweighted character mean；与 source mean
不能相乘。使用合法的 target maximum 会精确多损一个 `q asymp J`，使理想的
`Q^3/J` 退回 `Q^3`。非主 Jacobi matrix 在 rank-one complement 上是 scaled
unitary；在 coefficient-blind Jacobi operator-norm 意义下，删除有限个 output
characters或有限个 input exceptional coordinates都不产生 bulk contraction；这不
排除 actual coefficient在被删坐标上集中。

对全部 auxiliary triples `M=q_1q_2q_3` 作平均也不修复这一缺口。虽然
`#M=X^(399/400+o(1))` 且非零 determinant只落入至多一个 triple，total alias
`ell^1` mass仍为 `X/J^3=Q/J^2`；更关键的是每个 literal equality atom满足
`F=0`，故在对应的 `M`-regular support `(N,M)=1` 上，ratio phase
`chi(N+F)conjugate(chi(N))=1` 对全部 characters相同；`M`-singular faces由
TPC-37 inherited bound另行闭合。full primitive regular face仍以 `1-O(1/J)`
保留 identity bucket。many-modulus family
dimension因此不能换成 `J` 或 `J^2` saving；其 formal scalar `ell^2` alias gain要
传入 physical row sum，本身正是一个尚未证明的 target-coupled Bessel theorem。

BDH/prime-AP variance首先失败于 literal coefficient：unrestricted
`sum_(u|N)-mu(u)log u=Lambda(N)` 不等于 `T<u<=U0` 的 full ultra increment；
即使反事实修复该对象，scalar residue variance也不控制同一 `(q,chi)` 上的
common-`j`、two-copy、content-weighted source--target covariance。现有
Kloosterman-fraction、dispersion、shifted-convolution、delta-symbol 与 trace-function
theorem也均不提供 raw `F=0` column / identity-bucket recovery或 full physical
Hilbert Gram bound。joint-Mellin 与 shifted-fiber仍是两个独立 `OPEN` parents；
本轮没有 arithmetic advance、`chi<=1/400`、`L2` 或 TPC-207 trigger。

第 50 节沿第 49 节同一 theorem-valid selected packet，把 content cutoff精确放回
TPC-34 orbit-sliced energy。对
`c_(alpha,gamma)(j)=gcd(N_alpha(j),N_gamma(j))`，TPC-30 的 fixed-row
large-content orbit occupancy与 physical row residue degree共同推出新的派生
`L1` 尾项：

```text
V_(L,>Z)+V_(R,>Z)
  << X^epsilon Q^2(1+Q/Z)(1+J/Z).
```

取 `Z=C=floor(J)` 得 `V_>C<<X^epsilon Q^3/J`，再经 TPC-34 exact
orbit-to-column transfer得 `E_>C<<X^epsilon Q^3`。因此在同一 literal
coefficient、actual masks、fixed `h0=2` 与 normalization下，full 与
small-content 的 `V` gate（以及 `E` gate）彼此等价，差别只是一项已经闭合的
large-content tail；这不是 arithmetic cancellation。

第 50 节又把 small-content off-`V` 的 input-copy difference分层。除
`alpha_1=alpha_2` 的已闭合 diagonal外，termwise Schur/row-`ell^2` 给

```text
|V_(L,C,near)(H)|+|V_(R,C,near)(H)|
  << X^epsilon Q^2 J(1+H).
```

故 `H<=Q/J^2=X^(1/400+o(1))` 的 growing near-copy band也闭合于
`Q^3/J` gate。固定 exact double-content `(c1,c2)` 还有合法的 gcd/lcm CRT
incidence bound，但对全部 `(c1,c2)` 作 triangle reassembly会由 `(1,1)` 等
low-content layers使该 upper bound退化到 unsigned ceiling；这不是 actual饱和或
下界，不得升级为 aggregate saving。当前真正首缺已
收缩为 `c_i<=C` 且
`|m_(alpha_1)-m_(alpha_2)|>Q/J^2` 的 far-copy off-diagonal theorem。再移除
已空的 target-collision layer与 TPC-37 已闭合的 auxiliary `q`-singular faces后，
fully-coprime、`q`-regular、distinct-terminal four-Mobius formal eligible cross
layer未被现有 identities排除；其 literal active nonzero/coherent mass未证，但所需
`|V_(L,C,ne)|+|V_(R,C,ne)|<<X^epsilon Q^3/J` 尚未证明。

逐 theorem-body复核仍无 literal survivor。现有 Chowla/correlation、Gowers、
shift-average、inverse、nilsequence与 static sieve sources均先失败于 growing
coefficient、完整 four-Mobius ultra increment、linked actual masks/content、
prescribed family或 natural fixed-power normalization；其 logarithmic/metric输出
也不能支付所需 `J^2` collective saving。没有新增 source/version cell，既有
wrong-object cells继续 `STOP_SCOPED`。

TPC-206 仍为 `13/42`，首缺大写 opened `D`；pair-to-`omega`、linear H1、
两个 O161 pointwise parents 与 actual-cloud frame edge 均未改变。没有
`chi<=1/400`、direct small-content saving 或 TPC-207 trigger。除第 49--51 节明确
覆盖的 content/BV allocation 与 current first-fatal 外，第 33--48 节
source-specific wrong-object verdict、full-`J` absence及全部 STOP/OPEN状态继续
有效；第 50 节只新增上述两个 derived `L1` closure与一个 fixed-layer incidence，
第 51 节只新增 source-averaged marginal `L1` 与 exact identity-bucket obstruction，
不改写任何旧 cell。
当前仓库事实终点：TPC-206
当前编号论文裁决：`SELECTED_SOURCE_LOCKED_13_OF_42_PAIR_REGISTRY_PROJECTION_CERTIFIED_NOT_REOPENED`
最新不编号审计裁决：
`TPC_BIG_ROAD_V9_20260806_PRIME_GAUSS_DUAL_PRODUCT_EXACT_CENTERED_FIXED_RESIDUE_EQUIVALENCE_COMMON_K_UNIQUE_FIBER_FALSE_NONZERO_WRAPS_GLOBAL_MOVING_UNIT_CAUCHY_ENDPOINT_RESONANCE_LOCAL_INVERSE_PRODUCT_EXPONENT_INSUFFICIENT_STANDARD_LOD_ABSENT_SIGNED_MODULUS_DUAL_TYPE_IV_SELECTED_PAIRED_VORONOI_RESERVE_SEPARATE_NO_ARITHMETIC_TRIGGER_CHANNEL_REDESIGN`
下一篇：`null`；下一项不编号大动作：`TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE`
；当前 first subgate：`HB4_EXACT_HALF_ACTUAL_ATOM_DUAL_PRODUCT_DISPERSION`
（第 56 节控制；既有 local source只有在第 32.6 节或
第 33.5、34.6、35.6、36.6、37.6、38.5、39.5、40.7、41.6、42.7、43.7、44.7、
45.6、46.6、47.5、48.6、49.6、50.6、51.6、52.6、53.8、54.6、54.8--54.19、55--56 节列出的 source-backed reopen trigger，
或其他既有独立 trigger真实出现时重开）
TPC-204 授权并完成：`true`
TPC-205 授权并完成：`true`
TPC-206 授权并完成：`true`
后续同类有限审计与编号工作流授权：`true`
自动通过数学门槛或自动编号：`false`
TPC-207 数学 trigger：`false`；TPC-207 已创建：`false`
下一篇编号论文发布前完整 provenance cascade：`REQUIRED`

上下文节省入口：新会话先读 `TPC_COMPASS.md` 与
`research/tpc-big-road/README.md`与
`research/tpc-big-road/fm_local_comparison_compiler.md`，再读本页页首及第
1、6、22、24、54.18--54.19、55--56 节；第 29--53 节与第 54.1--54.17 节只在上述入口明确引用时展开，第 23、27、28 节仍只在后续
审计明确引用时展开。第 22 节的
`TRUNCATED_ENTRY_ABSENT`
仍只指 `delta=1/20` exact family；第 23 节审核的是另一条 theorem-valid
high-beta selected packet。两条 source lock 不得拼接。

本文件、仓库内已提交的论文，以及 active payload/audit/schema/checker
是下一会话的事实来源。旧聊天记录不是事实来源。
下文历史审计块中的所有 `tpc205_authorized=false`、`TPC-206 未授权` 与
`USER_CONFIRMATION_REQUIRED` 都是当时的编号前快照，统一由本页页首及
第 14--23 节覆盖；其数学 gate 与 `STOP_SCOPED` 内容仍保留。用户已允许
后续按同一有限、fail-closed 工作流继续，不再设置单独的人为编号授权门；
这不替代 theorem evidence，也不许可跨过任何数学门槛。

## 1. 启动与验证协议

```powershell
Set-Location "D:\26-aimath\理论研究3\prime_dynamics_theory"
git status --short --branch
git pull --rebase origin main
Get-Content -Raw -Encoding UTF8 TPC_HANDOFF.md
$env:PYTHONDONTWRITEBYTECODE = "1"

$d = "papers/tpc-206-selected-lineage-pair-registry-projection/experiments"
python -B "$d/build_tpc206.py" --check
python -B "$d/tpc206_selected_lineage_pair_registry.py" --check
python -B "$d/tpc206_independent_checker.py" --check
$p = "papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments"
python -B "$p/build_tpc205.py" --check
python -B "$p/tpc205_pair_native_registry_interface.py" --check
python -B "$p/tpc205_independent_checker.py" --check
python -B papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_certificate_hardening.py --check
python -B papers/tpc-133-executable-native-entrance/experiments/tpc133_native_entrance.py --check
python -B papers/tpc-134-boundary-complete-dyadic-prefix-tail-archive/experiments/tpc134_branch_archive.py --check
python -B papers/tpc-135-tpc17-tpc18-block-frontier/experiments/tpc135_domain_cover_audit.py --check
python -B papers/tpc-136-complete-native-cut-archive/experiments/tpc136_cut_archive.py --check
python -B papers/tpc-184-bad-endpoint-literal-target-contract/experiments/tpc184_bad_endpoint_literal_target_contract.py --check
python -O -B papers/tpc-184-bad-endpoint-literal-target-contract/experiments/tpc184_bad_endpoint_literal_target_contract.py --check
python -B papers/tpc-189-direct-twist-literal-target-contract/experiments/tpc189_direct_twist_literal_target_contract.py --check
python -O -B papers/tpc-189-direct-twist-literal-target-contract/experiments/tpc189_direct_twist_literal_target_contract.py --check

foreach ($s in @(
  "papers/tpc-173-production-source-claim-inventory/experiments/tpc173_source_claim_inventory.py",
  "papers/tpc-174-local-occurrence-edge-witness-schema/experiments/tpc174_witness_contract.py",
  "papers/tpc-175-declared-corpus-local-edge-family/experiments/tpc175_local_edge_family.py",
  "papers/tpc-176-source-backed-coverage-gluing-audit/experiments/tpc176_coverage_gluing_audit.py",
  "papers/tpc-177-actual-active-support-vacuity-firewall/experiments/tpc177_active_support_audit.py",
  "papers/tpc-178-canonical-minimal-representation-eligibility/experiments/tpc178_representation_audit.py",
  "papers/tpc-179-h1-structural-corpus-exhaustion-integration/experiments/tpc179_h1_integration.py"
)) {
  python -O -B $s --check
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
```

以上是当前完整的 22 项只读启动回归；任一命令非零即 fail closed，不继续
数学升级或正式写入。`git status` 中既有 tracked/untracked 工作属于用户；不得
`reset`、`checkout`、`clean`、自动 `stash`、删除或纳入本轮提交。当前已知须保留
TPC-105 的 `__pycache__/`、TPC-63 构建产物与 `tmp/`。TPC-27--32 legacy
certificates 没有只读 `--check` 且会无条件重写 JSON，在新增真正只读入口前
不得为了启动回归而执行。

随后优先读取：

1. `papers/tpc-206-selected-lineage-pair-registry-projection/README.md`
2. `papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_selected_lineage_pair_registry.json`
3. `papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_selected_lineage_pair_registry_audit.json`
4. `papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_independent_checker.py`
5. `papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments/tpc205_pair_native_registry_interface.json`
6. `papers/tpc-194-maximal-source-backed-direct-prefix/experiments/tpc194_maximal_source_backed_direct_prefix.json`
7. `papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/experiments/tpc193_literal_fixed_atom_candidate_mechanism_gate.json`

不得因打开新会话、用户说“继续”、checker 通过或工作流已持续授权而
自动创建 TPC-207。持续授权只移除了重复的人为许可步骤；只有新的
theorem-backed edge 使定理状态发生真实变化时，才可编号。证书通过只说明
当前有限 selected-lineage 边界被可靠冻结，不解除数学门槛。

## 2. 发布锚点

TPC-194--203 论文提交：

```text
460950090855a49a86e93231902a9674879d6f34
```

TPC-194/203 不编号证书加固提交：

```text
2e7a38652baff130cdfcbcf83ba05d3ee78a4dcc
```

TPC-204 论文提交：

```text
2226193cf726f96c7dbca3e9a1321ed6862f6a4c
```

TPC-204 稳定 PDF：

```text
papers/tpc-204-source-locked-production-registry-crosswalk/tpc-204-source-locked-production-registry-crosswalk.pdf
sha256 = 85d4dcd8436e5b049933584d68407924019c1d82b6b9c85122d84c3e101290f9
pages = 4
page size = A4
```

TPC-204 active release：

```text
release files = 14
manifest-pinned artifacts = 11
payload/audit exact schemas = 2
source locks = 15
```

TPC-205 论文提交：

```text
98b3e6c462008b07538b496ed130b1004a84747f
```

TPC-205 稳定 PDF：

```text
papers/tpc-205-pair-native-post-ttstar-registry-interface/tpc-205-pair-native-post-ttstar-registry-interface.pdf
sha256 = b3596e207943132ad48e6a17cfd107421f02b521bc02f617615c860816a1dc1e
pages = 4
page size = A4
```

TPC-205 active release：

```text
release files = 16
manifest-pinned artifacts = 13
payload/audit/L0 exact schemas = 3
source locks = 17
```

TPC-206 论文提交：

```text
85d3d08221101dd125fb07cb5e1929f9d2525a5a
```

TPC-206 稳定 PDF：

```text
papers/tpc-206-selected-lineage-pair-registry-projection/tpc-206-selected-lineage-pair-registry-projection.pdf
sha256 = e6a3ee6df0492daa2aae86de47040e8b0d5f8c75a7abc91208601f945d3bb082
pages = 4
page size = A4
```

TPC-206 active release：

```text
release files = 14
manifest-pinned artifacts = 11
payload/audit exact schemas = 2
source locks = 29
```

TPC-206 的 source theorem/archive 审计快照固定于
`42507087b774d9057ba3794468a4790bf93162d5`。发布前第二次
`git pull --rebase origin main` 仅引入 RH-322 路径并把基线推进到
`b3dc7e5`；没有改动 TPC 路径。因而 29 个 source locks 继续有意针对
审计启动快照，而不是把无关的晚到提交偷换进冻结 census。

## 3. TPC-204 的精确有限结论

授权范围仅为：

```text
FINITE_EXACT_MATCHING_OR_FIRST_MISMATCH_CROSSWALK_AUDIT
```

授权是 workflow input，不是 theorem evidence，不让任何 reopen trigger
自动通过。

TPC-204 对 direct-production lineage 中九个互异 plausible objects 作了
固定、source-locked 的有限审核：

1. `H9.phase_cell_registry`：TPC-180 的空 registry slot；
2. `TT26.RATIONAL_PERIODIC_ATOM`：`q/N` terminal-block log-saving theorem；
3. `A159.DYADIC_SHADOW_ALMOST_ENDPOINT_PREFIX`：shadow 外 `q/T` cumulative prefix；
4. `A167.DIRECT_ADDITIVE_TWIST_PHASE_L2`：terminal-block phase `L2` theorem；
5. `TPC183.N_EQUALS_T_SPECIALIZATION_PROPOSAL`：无效的 terminal-to-cumulative proposal；
6. `O161.BAD_ENDPOINT_POINTWISE_FIXED_ATOM_CONTRACT`：TPC-184 verbal `q/T` all-prefix target；
7. `O161.DIRECT_ADDITIVE_TWIST_FIXED_ATOM_CONTRACT`：TPC-189 verbal `q/N` direct target；
8. `TW25.LOG_TWISTED_AFFINE`：log-weighted fixed-atom affine theorem；
9. `PHYSICAL_PACKET_PREFIX`：TPC-194 resolved unnormalized per-packet prefix。

TPC-184 contract 与 TPC-159 shadow-excluding theorem 是不同对象；前者不能
被后者静默代表。这一行是在独立 claim review 中发现并补入，最终不存在
漏计。

四个显式排除对象：

```text
TPC167.prop:grid
TPC167.cor:measure
TPC159.cor:interval
TPC203.tpc194_import_contract
```

它们分别是 auxiliary grid、Lebesgue phase measure、无单一 target
normalization 的 interval difference，以及重复 upstream import，不是
新的 production-crosswalk object。

最终有限计数：

```text
declared candidates = 9
production axes per candidate = 7
production-axis cells = 63
formula types per candidate = 3
formula-crosswalk cells = 27
complete crosswalks = 0
first common mismatch = NAMED_PRODUCTION_ATOM
direct trigger = FAIL
mathematical reopen = false
```

精确 theorem status：

```text
PROVED_LOCKED_REGISTRY_FIRST_MISMATCH_NO_COMPLETE_CROSSWALK_L1
```

精确 verdict：

```text
FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE
```

这是 L0/L1 的 finite-corpus first-mismatch theorem。它不是 fixed-atom
cancellation theorem，不是 production registry 的全球不存在性定理，
不关闭 direct route、任一 O161 parent 或全局架构，也没有 L2 gain。

## 4. 三个不可混同的公式对象

```text
CORE_TERMINAL_BLOCK
  domain = N<t(z)<=2N
  normalization = q/N

CORE_CUMULATIVE_PREFIX
  domain = 0<t(z)<=T
  normalization = q/T

PHYSICAL_PACKET_PREFIX
  domain = z in I_xi_X and z<=T
  normalization = UNNORMALIZED_INSIDE_OUTER_PACKET_SUM
```

令 `N=T` 只把第一行变成 `T<t(z)<=2T`，不会产生
`0<t(z)<=T`。第三行处于 outer physical packet sum 内且本身未归一化。
不得通过改名、解释性改写，或把 block/cumulative/physical 对象强行
等同来补字段。

完整 production record 仍须在同一 source-locked 对象上同时冻结：

```text
named_production_atom
packet_schedule
common_X_N_q_ranges
uniform_constant_C
positive_sigma
target_normalization_selection
complete_physical_loss_ledger
```

当前共同首缺为 `named_production_atom`；`packet_schedule`、
target normalization selection 与其余字段仍有独立缺口。

## 5. 三层第一缺口与开放状态

三个 first-missing 必须彼此区分：

```text
GlobalFirstMissing
  = H1.source_backed_local_occurrence_edge_family

SelectedPointwiseFirstMissing
  = LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION

DirectProductionFirstMissing
  = SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK

DirectCrosswalkSubgate
  = NAMED_PRODUCTION_ATOM
```

状态保持：

```text
bad_endpoint_O161_parent = OPEN
direct_twist_O161_parent = OPEN
global_architecture = OPEN
fixed_atom_decay_obtained = false
literal_fixed_atom_cancellation_obtained = false
named_atom_endpoint_credit = 0
strict_1/400 = UNPAID
program_positive_L2 = false
L2_result = NONE
batch_stop = USER_CONFIRMATION_REQUIRED
next_paper = null
tpc205_authorized = false
```

下一条 direct-production 输入应是：

```text
SOURCE_LOCKED_NAMED_PRODUCTION_ATOM_RECORD
```

并仍须附 exact packet schedule、共同 ranges、uniform `C`、positive
`sigma`、literal normalization、完整 physical-loss ledger，及真正的
fixed-atom theorem。只有 atom 名称或 symbolic `alpha_xi_X` 不够。

## 6. STOP_SCOPED 注册表

既有六个 scoped stop 保持：

```text
TPC181_PHASE_METRIC_UNCONTROLLED_ATOMIC = STOP_SCOPED
TPC187_SIZE_ONLY_LOCAL_OSCILLATION_METHOD = STOP_SCOPED
TPC190_PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM = STOP_SCOPED
TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1 = STOP_SCOPED
FACTORWISE_SINGLE_MOBIUS_FOURIER_TO_LITERAL_PRODUCT = STOP_SCOPED
ONE_FUNCTION_PRETENTIOUSNESS_DIRECT_APPLICATION_TO_CZ = STOP_SCOPED
```

TPC-204 新增且仅新增：

```text
TPC204_DECLARED_PLAUSIBLE_PRODUCTION_CROSSWALK_CORPUS_V1 = STOP_SCOPED
```

它只停止从这九个明确对象中提取完整 crosswalk。不得提升为更大 source
universe 的停止声明。

2026-07-30 的不编号 single-cut 审计新增且仅新增：

```text
TPC18_25_32_93_194_SINGLE_CUT_OCCURRENCE_COMPOSITE_V1 = STOP_SCOPED
```

它只停止以下推断：把 TPC-18/TPC-25 的 opened-row 重标号直接与
TPC-93 的既成 source-child inverse、TPC-194 的既成 resolved-key
公式组合，就得到原 cut coefficient 的 production local-occurrence
edge。它不停止新的 cut-to-parent theorem、pair-native repair、H1
architecture、两个 O161 parents 或任何真正新增的算术 theorem。

2026-07-30 的不编号 pair-native 审计新增且仅新增：

```text
TPC18_TPC93_POST_TTSTAR_PAIR_DIRECT_COMPOSITION_V1 = STOP_SCOPED
```

它只停止以下直接提升：把当前 TPC-18/TPC-25/TPC-32 的公式级
post-TT-star ordered row-pair 直接改名为现成的 TPC-93 retained
`omega`、生产 pair occurrence，或 H1 local-occurrence edge。它不停止
新的 pair registry、pair-to-`omega` theorem crosswalk、cut inverse
aggregation、独立 architecture reroute、两个 O161 parents，或真正新增的
算术 theorem。给定 retained `omega` 后的 source-child inverse，以及
另行给定 downstream fields 后的 content/resolved template 相容性也未被
否定。

2026-07-31 的三项不编号审计新增且仅新增：

```text
DECLARED_SELECTED_103_107_OPENED_D_ATTACHMENT_CORPUS_V1 = STOP_SCOPED
DECLARED_TPC18_25_133_134_LITERAL_PAIR_COEFFICIENT_CROSSWALK_V1 = STOP_SCOPED
DECLARED_TPC149_159_180_184_193_202_BAD_ENDPOINT_TRIGGER_V1 = STOP_SCOPED
```

第一项只停止从 selected 103/107 的现有八条 archived child paths
解释出一个共同 opened-`D` attachment；第二项只停止把现有 TPC-133
single-row AST 与 TPC-134 edge multiplier 重命名为同一 typed `T_D`
上的 literal `B_alpha B_gamma`；第三项只停止把列出的 good-scale、
shadow、空 phase census、target contract 与 averaged-selector records
组合成 scheduled bad-shadow local-increment theorem。三项都不是数学
nonexistence theorem，不停止新 source record、新 theorem、两个 O161
parents、pair-native/H1/global architecture。

`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1` 必须继续
`STOP_SCOPED`；不得把 phase `L2`、Lebesgue-a.e.、size-only、
log-to-natural，或旧 method cells 的重包装记作新 theorem。

2026-07-31 的全仓 H1 local-edge audit 新增且仅新增：

```text
DECLARED_TPC1_206_REACHABLE_LOCAL_OCCURRENCE_EDGE_SOURCE_CORPUS_V2
  = STOP_SCOPED
```

它只停止从 commit `023ccb5959e35b96673117b76add3dcbc3987aca`
的 TPC-1--206 paper corpus，以及当时所有 refs 按第 16 节选择器可达的
历史 blobs，重新包装出 production actual local-occurrence edge。它不
覆盖未来 refs、未 fetch source、真正新增的 source theorem 或独立
architecture reroute。

2026-07-31 的 one-packet source-forward 与自动 fallback census 新增且仅
新增：

```text
DECLARED_SELECTED_ONE_PACKET_SOURCE_FORWARD_PRECUT_TO_ACTUAL_OCCURRENCE_LINEAGE_V1
  = STOP_SCOPED
DECLARED_TPC133_134_136_NONSELECTED_TPC18_GEOMETRY_ORDERED_PAIR_LINEAGE_JOIN_CORPUS_V1
  = STOP_SCOPED
```

第一项只停止第 17 节列举的当前 source universe 中，把现有
native/archive/path/cut 身份改名为 actual physical occurrence 后再声称
source-forward edge；第二项只停止当前 committed TPC-133/134/136
archive 中、排除 exact selected `103 -> 107` orientation 后、满足严格
TPC-18 `NO_TAIL_ROOM` geometry 的 ordered pair join corpus。它们都不是
数学不存在性定理，不停止新 primary theorem、source-locked opened-`D`
attachment、pair-native reroute、两个 O161 parents、H1 或 global
architecture。

2026-07-31 的 positive determinant-two seed carrier audit 新增且仅新增：

```text
DECLARED_X512_H2_ALPHA17_D1_GAMMA16_D1_POSDET2_OPENED_D_PACKET_ATTACHMENT_V1
  = STOP_SCOPED
DECLARED_TPC133_134_136_POSDET2_BOTH_PRIME_PRIMITIVE_MASK_CORPUS_V1
  = STOP_SCOPED
```

第一项只停止把 exact seed
`alpha=(17,1), gamma=(16,1), j=33, block=(4,5,0)` 提升为 TPC-18
prime-source opened-`D` pair；其 `gamma` source `ell=16` 是 prime
power 而不是 prime，故 prime-reduced carrier weight 恰为零。第二项只
停止当前 committed strict archive 中 14 个 positive determinant-two、
both-prime pair-block instances 走 TPC-18/TPC-25 的 primitive mask：
每个实例都恰有一个 even divisor row，故在 `h0=2` 下 joint primitive
mask 为零。它不停止 TPC-18 的 formal constant-mask formula、真正新增的
source-locked physical mask theorem、nonprimitive endpoint reroute、两个
O161 parents、H1 或 global architecture。

2026-07-31 的 `23/11` mixed-`d` actual-mask 审计新增且仅新增：

```text
DECLARED_X512_H2_ALPHA23_D1_GAMMA11_D2_POSDET2_ACTUAL_PHYSICAL_JOINT_MASK_ATTACHMENT_V1
  = STOP_SCOPED
```

它只停止把 exact seed
`alpha=(23,1,k=24), gamma=(11,2,k=48), j=24, block=(4,5,0)`
在当前 TPC-18/21/25/32/93 与 TPC-133/134/136 source locks 下提升为
非零 actual physical joint packet。TPC-18 primitive mask 在两侧都为零；
TPC-25/32 primitive carrier 还排除 `d_gamma=2` 与 `j=24`；TPC-18
`xi=1` 只是 formal admissible mask，没有 formal-to-physical attachment
theorem；`s=2` endpoint 是同一 `k` 的另一对象。它不停止新的
formal-to-physical theorem、新的 named dyadic member、具有非零 common-`k`
endpoint coefficient 的 source record、两个 O161 parents、H1 或 global
architecture。

2026-07-31 的 TPC-18 `s=2` source-forward 审计新增且仅新增：

```text
DECLARED_TPC18_H0_2_COMMON_K_ENDPOINT_SOURCE_FORWARD_RECORD_CORPUS_V1
  = STOP_SCOPED
```

它只停止在 commit `f2f98b0bdc4b56c36292e9211b19c1d2e45ffae0` 可达的
TPC-17/18、TPC-133/134/136/143/153/154 与 TPC-205/206 记录中，把
`D0=0,V=2` 的同偶数 `k` 形式配对，或 TPC-18 的
`D0=6,V=18,h=6` finite identity fixture，改名为 `h0=2,s=2` 的
nonzero actual endpoint/source-forward record。它不停止 TPC-18 的通用
endpoint identity、真正新增的 `h0=2` branch-selection theorem、具名 actual
common-`k` packet、两个 O161 parents、H1 或 global architecture。

2026-07-31 的下一轮 `h0=2` exact-profile / branch-selection 审计新增且仅新增：

```text
DECLARED_TPC18_H0_2_TAIL_FAILURE_A_EXCLUSION_AND_DIRECT_B_CORPUS_V1
  = STOP_SCOPED
```

它只停止在本轮审核的 34 个 git refs、仓库现有 TPC-17/18/19/27/28/108
对象，以及截至 2026-07-31 逐对象核查的 Maynard、Li、Lichtman、Pascadi、
Matomäki--Radziwiłł--Tao、Goldston--Yıldırım、Ramaré--Zúñiga Alterman、
Laporta 与 Coppola--Murty--Saha primary theorem 候选中，把 AP / factorable
平均分布、shift-average、log-average、截断平方、size-only LCM 对角或带
未验证强假设的对象改名为：具名 actual `h0=2` symmetric-tail failure、完整
`r_R r_R` primitive-A 排除，或 `C_{I,2}^{MM,off}` 的 direct lower bound。
它不停止真正新增的 full-residual determinant theorem、theorem-backed
fixed-block tail-failure、direct `s=2` finite-model theorem、两个 O161 parents、
H1 或 global architecture。

2026-07-31 的 full-`r_Rr_R` primitive-A / ultra-complement 审计新增且仅新增：

```text
DECLARED_TPC18_H0_2_FULL_R_R_PRIMITIVE_ULTRA_COMPLEMENT_CORPUS_V1
  = STOP_SCOPED
```

它只停止在审计基线 `HEAD=origin/main=687bc2d44a25efd2a376fd3b363bfac4549b4cb9`
时可达的 346-commit all-ref snapshot、TPC-18--124 ultra-residual
lineage、TPC-125--206 relevant claim/status，以及截至 2026-07-31 审核的
Menon、Ramaré--Zuniga Alterman 与既有 fixed/log/shift/phase-average primary
theorem candidates中，把以下对象改名为 full primitive-A closure：

```text
one selected TPC-28 truncated square
TPC-29/30 content-rich or large-content sectors
TPC-27 additive Poisson zero
TPC-31/32 almost-all nonzero determinant frequencies
TPC-116 conditional complete-tail schema
size-only, logarithmic, exceptional-scale, phase/origin/shift-average results.
```

它不停止新的 `DD_2(theta)` all-slice theorem、同一 TPC-32 packet 上的
small-content matched auxiliary-zero theorem、TPC-111/122 signed-prefix exact
transfer、真正新增的 growing prefix theorem、两个 O161 parents、H1、
pair-native reroute 或 global architecture。

2026-07-31 的 TPC-32 selected-packet signed-prefix transfer 审计新增且仅新增：

```text
DECLARED_TPC32_111_122_SELECTED_PACKET_AUXILIARY_ZERO_SIGNED_PREFIX_TRANSFER_V1
  = STOP_SCOPED
```

它只停止从当前 committed TPC-28--32 selected high-beta packet、TPC-111/122
Abel--BV formulas、TPC-124 determinant/zero-fiber comparison，以及 TPC-126/127
exact prefix transports中，直接重命名出同一个
`A_hat_C,q(0)` 的 source-backed growing signed-prefix theorem。第 48 节 current
correction确认：full post-bin dictionary intertwiner仍缺，但 scalar
common-native refinement、original global normalization与 `N0=JQ^2` /
`Q^2=N0/J` identity 已为 `PRESENT_L1`。第 49 节进一步确认，若把
`chi_theta` 中的 fixed-period/local-coprimality factors与 `1_(G_theta<=C)`
固定留在 signed sequence，并只把 `c_theta,X W_theta,X` 放入 BV weight；其余
actual row-pair masks继续留在 `theta,I_theta,c_theta,X`，则 committed
row-`ell^1`、orbit-support、
projector-mass与 smooth-BV 界给出

```text
SAFE_CONTENT_AWARE_OUTER_BV_ENVELOPE = PRESENT_DERIVED_L1
ell_Z = 133/400.
```

本 cell 仍为 `STOP_SCOPED`：该 allocation 所需的是 exact masked all-prefix theorem，
而逐 fiber + absolute outer reassembly 的最长可见 exponent 只有
`10049/52500`，比 `ell_Z` 少 `29629/210000`；singleton return 与 collective
outer cancellation也均未证。把 content mask留在旧 weight时 `E_cont=0`，但全部
BV jumps仍须支付；改变 factor allocation不得调用旧的 unmasked prefix theorem。
该 cell不停止新的 full actual intertwiner、直接控制同一 `A_C` 的 theorem、
TPC-33 `Q^3` collective energy theorem、保留全部 literal data 的新
masked-prefix/collective theorem、两个 O161 parents、pair-native reroute、H1 或
global architecture。

第 50 节没有新造同义 method/source cell，而是在本 cell 内登记两个严格派生的
`L1` 子门槛。对 TPC-34 orbit slice按 exact target content切分，TPC-30
fixed-row occupancy与 row-residue degree给出

```text
V_(L,>C)+V_(R,>C) << X^epsilon Q^3/J,
E_(L,>C)+E_(R,>C) << X^epsilon Q^3,
C=floor(J).
```

所以 full/small-content `V` 与 `E` gates在目标尺度上等价。small-content
off-`V` 中另有

```text
0<|m_(alpha_1)-m_(alpha_2)|<=Q/J^2
```

的 input-copy near band，由 row-`ell^2`/Schur bound闭合；这里的 two-copy
difference不得与 actual mask中的 input--opposite-row separation混同。fixed exact
`(c1,c2)` gcd/lcm incidence只对单层成立，不能经 absolute reassembly升级为
aggregate saving。故本 cell仍为 `STOP_SCOPED`，首缺进一步限定为 small-content
far-copy off-diagonal `Q^3/J` theorem；target collision与继承的 TPC-37
`q`-singular faces移除后，fully-coprime `q`-regular distinct-terminal four-Mobius
formal eligible cross layer未被现有 identities排除；不主张其 actual active
nonzero/coherent mass。`L2=NONE`，strict `1/400`仍未支付。

2026-07-31 的第 23.5 节 named-primary reopen-candidate 审计新增且仅新增：

```text
DECLARED_TPC32_23_5_NAMED_PRIMARY_REOPEN_CANDIDATES_20260731_V1
  = STOP_SCOPED
```

它只停止把 Banks--Shparlinski `arXiv:2506.08787v1`、Verjovsky
`arXiv:2607.25002v1`、Ford--Radziwiłł `arXiv:2605.03349v1`，或
Matomäki--Teräväinen `arXiv:2605.27833v1` 的已审核 theorem statements
改名为同一 actual `A_C` 的 coefficientwise fiber map、直接 distinguished-zero
saving，或带 outer BV/content remainder 的 growing all-prefix theorem。它不扩张
任何旧 `STOP_SCOPED` cell，也不停止这些来源的新版本、真正新增的 actual
corollary/crosswalk、两个 O161 parents、pair-native reroute、H1 或 global
architecture；精确字段审计见第 27 节。

2026-08-01 的第 23.5 节 current-primary theorem-route 审计新增且仅新增：

```text
DECLARED_TPC32_23_5_NAMED_PRIMARY_REOPEN_CANDIDATES_20260801_V1
  = STOP_SCOPED
```

它只停止把 Tao--Teräväinen `arXiv:2512.01739v2`、Cantarini
`arXiv:2607.09110v1`、Kim `arXiv:2603.23250v2`、Grimmelt--Merikoski
`arXiv:2404.08502v2`、Fragkos--Krause--Miheisi--Sun
`arXiv:2607.05560v1`、Lau `arXiv:2509.07556v2`、Koukoulopoulos
`arXiv:2605.01412v1`、Pozdnyakov `arXiv:2604.23427v1` 或 Chavez
`arXiv:2409.02106v10` 的已审核 theorem statements，单独或跨来源拼接后改名为
同一 actual `A_C` 的 coefficientwise fiber map、direct matched-shell saving，或带
outer BV/content remainder 的 growing all-prefix theorem。它不扩张 Higher
Uniformity、Pilatte、single-factor、almost-all/origin-average、logarithmic/cumulative
等旧 `STOP_SCOPED` cells，也不是未审核文献或未来定理的 nonexistence claim；
精确 scope、字段审计与 reopen interface 见第 28 节。

2026-08-01 的 selected-packet common-occurrence compiler 与
Grimmelt--Merikoski Part-I inverse-atom 审计新增且仅新增：

```text
DECLARED_TPC32_SELECTED_PACKET_COMMON_OCCURRENCE_QD_QZ_METADATA_PRESERVING_INTERTWINER_V1
  = STOP_SCOPED
DECLARED_TPC32_GM2505_V2_INVERSE_ATOM_ACTUAL_CROSS_ROW_COMPACT_SELF_KERNEL_V1
  = STOP_SCOPED
```

第一项只停止把当前 TPC-32/TPC-93 的参数化、lossless formula compiler
直接升级为 TPC-144 所需的 metadata-preserving output-record bijection：
both-ultra raw leaf 在 determinant parent 侧聚为一个 record，而 ordered-zero
侧必须保留两个各带 `1/2` 的 `L/R` records；实际 selected schedule 是否含
nonzero both-ultra occurrence仍 `NOT_TESTABLE`。它不停止未来的 actual occurrence
registry、允许正确 typed linear relation 的新架构、或真正新增的 growing-prefix
theorem。

第二项只停止从 Grimmelt--Merikoski `arXiv:2505.00489v2` Part I、本轮
exact inverse-atom attachment 与当前 committed TPC source corpus，直接推出
actual cross-row self-kernel 的 tiny-power bound或 strict `1/400` saving。
inverse placement、atomwise determinant normalization、zero-Haar test 与 fixed-row
`j`-arc escape 本身是 `L1 GO`，没有被此 cell 否定。该 cell 不停止未来的
actual equal-difference four-point autocorrelation theorem、不同 functional
factorization、Part II、新版本 source、两个 O161 parents、pair-native/H1/global
architecture 或任何真正新增的算术输入；精确公式与 scope 见第 29 节。

2026-08-01 的 literal fixed-`D0` TPC-93 transversal、current-primary
four-point transfer 与 cross-`D0` standard-orthogonality 审计新增且仅新增：

```text
DECLARED_TPC32_LITERAL_FIXED_D0_FOURPOINT_STANDARD_TRANSFER_
AND_CROSS_D0_ORTHOGONALITY_CORPUS_V1 = STOP_SCOPED
```

它只停止把第 30 节逐项审核的当前 committed TPC-32/34/38/42/48/84/93/95/108
interfaces、Grimmelt--Merikoski `arXiv:2505.00493v2` application、Tao--Teräväinen
`arXiv:2512.01739v2` 与 `2107.02158v4`、Menon `2607.15574v1`、
Jaskari--Sachpazis `2409.10663v3`、Leng `2212.09635v3`、
Klurman--Mangerel `1708.03176v1`、Lichtman--Teräväinen `2111.08912v3`、
Higher Uniformity II `2411.05770v2`、Kim `2603.23250v2`，以及 ordinary
Schur/Young、additive/Dirichlet large sieve、Fourier/Mellin complete-frequency
identities，直接或跨来源拼接成 literal fixed-`D0` `E_Psi` bound，或再提升成
full `E1`。它不停止直接接受 actual `w_m` 的新 theorem、保留全部 metadata 且
global projective total variation 为 `X^o(1)` 的 source-backed regrouping、完整
two-parameter automorphic self-kernel theorem、actual cross-`D0` block-Bessel
theorem、未来 GM Part II/新版本、两个 O161 parents、pair-native/H1/global
architecture或真正新增的独立算术输入；精确 source locks、第一 fatal 与
reopen interface见第 30 节。

2026-08-01 的 fixed-`D0` theorem-parameter-preserving outer regroup、physical
`m`-coarsening 与 post-第 30 节 direct/frame source 审计新增且仅新增：

```text
DECLARED_TPC32_FIXED_D0_OUTER_REGROUP_AND_POST30_DIRECT_FRAME_
SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

它只停止以下有限对象：TPC-93 decorated children 在 fixed `D0` 下按
`(L/R,ell,ell',j,sigma_aff,v,iota)` 保持同一 affine theorem parameters 的
regroup；这里 `sigma_aff=sigma_theta` 是 TPC-93 的整数 affine slope，不是
selected-packet 参数 `sigma=1/10000`；
按 physical moving row `m` 使用 source-child inverse 的 exact coarsening；Carella
`arXiv:2202.01071v5`、Jiseong Kim `2509.24152v1`、Diao `2506.18065v1`、
Krishnamoorthy `2501.10962v2`；Qi `2404.09085v3` 与 `2407.17711v1`、
Lekkas--Voskou `2405.01056v2`、Pascadi `2404.04239v3`、Hu--Petrow--Young
`2411.05672v3`，以及本轮复核的 GM Part-I/application self-kernel interface。
Carella source因证明链无效而不得注册成 theorem input；其余来源只按各自
source-backed theorem statement 的原 scope冻结。Banks--Shparlinski
`2506.08787v1` 与 Cantarini `2607.09110v1` 的旧 scope仍分别由第 27--28 节
既有 cells管理，本 cell不重复扩张。

该 cell不停止一个直接接受 exact literal `w_m/E_Psi` 的新定理、production
actual-edge census加 coefficientwise intertwiner与 `X^o(1)` global projective
decomposition、允许 row primes/cofactors/slopes/outer labels 随 `m` 变化的
真正 growing theorem、literal full GM self-kernel/cross-`D0` frame theorem、
未来 source版本、两个 O161 parents、pair-native/H1/global architecture或任何
真正新增的独立算术输入；精确二分结构、source proof audit、frame fatal 与
reopen interface见第 31 节。

2026-08-01 的 post-第 31 节 natural binary-Möbius primary-source refresh新增且
仅新增：

```text
DECLARED_TPC32_POST31_NATURAL_BINARY_MOBIUS_PRIMARY_
SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

它只停止把第 32.2 节逐 theorem-body 审核的 Klurman--Mangerel--Teräväinen
`arXiv:2304.05344v2`、Pilatte `2310.19357v2`、Frantzikinakis--Host
`1502.02646v3`、Mangerel `1612.09544v2`、Kravitz--Woo--Xu
`2512.03292v1`、Frantzikinakis--Klurman--Moreira `2407.08360v3` 与
Tao--Teräväinen `1809.02518v2`，直接升级成同一 selected high-beta packet 的
prescribed natural positive-power theorem。KMT 的 determinant
prime `2` support condition可由第 32.2 节的 exact `mu_odd` replacement无损通过；
本 cell不得把 `mu(2)=-1` 重新列为 fatal。真正冻结的只是其 small truncated
pretentious-distance、logarithmic output、fixed/polylog coefficient range、terminal
unweighted sum与 literal physical attachment的当前 source scope。该 cell不停止未来
新版本、直接接受 actual coefficient/weights/prefix/normalization的新 theorem，或其他
真正新增的独立算术输入。

同日的 selected high-beta determinant-zero / additive-metric source refresh新增且
仅新增：

```text
DECLARED_TPC32_SELECTED_HIGH_BETA_METRIC_SCHEDULE_EXCEPTIONAL_
LIMSUP_AVOIDANCE_SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

它只停止把当前 TPC-32 normalized-determinant DFT zero无 intertwiner地改名为
TPC-170/181 additive phase atom，或把第 32.3 节列出的 algorithmic-randomness、
moving-target、dynamical Borel--Cantelli与 divergence-limsup theorems升级成 exact
named packet的 schedule-specific bad-event avoidance。它不停止未来直接作用于
`A_hat_C,q_DFT(0)` 的 pointwise theorem、真正 source-backed additive atom + actual
schedule + same-event avoidance theorem、两个 O161 parents、H1、pair-native reroute
或 global architecture。

同日的 current committed actual-census / intertwiner / projective-cost refresh新增且
仅新增：

```text
DECLARED_TPC32_HIGH_BETA_CURRENT_COMMITTED_CENSUS_
INTERTWINER_XO_PROJECTIVE_CORPUS_V1 = STOP_SCOPED
```

它只停止从当前 committed TPC-32/84/93/124/173--179/193--206 artifacts，借
symbolic formula、future schema、异源 finite fixture、row-only record、one-vector
equality、finite SVD或 atomic triangle，构造同一 high-beta packet的 actual census、
coefficientwise intertwiner或 source-backed `X^o(1)` global projective theorem；也
停止把 TT-star bilinear pair重命名为 H1 linear local-occurrence edge。它不停止未来
同 packet actual parent registry、真实 growing matrices与完整 coefficientwise identity、
新 projective theorem、direct literal theorem或任何开放 architecture。精确 first
fatals与合法 materialization order见第 32.4 节。

发布前远端新增 RH-340 后，只新增下列精确有限 cross-program cell：

```text
DECLARED_TPC32_REMOTE_RH340_SYNCHRONIZED_PREFIX_TRANSFER_V1
  = STOP_SCOPED
```

它只停止把 commit `eb1cf19a28b1d1d38eaece2a6bb0b578f20df969` 中 RH-340
Hardy trace-order 的 `P_u/E_u/D_u` absolute coefficient budgets、条件必要的
two-order orbit--head compensation，或 cancellation-blind separate-absolute
majorant obstruction，直接升级为 TPC-32 同一 high-beta packet 的 ordered
signed-prefix theorem、small-content matched-shell saving或 distinguished
determinant-zero theorem。RH 的 moving orders `2k,2k-2` 不是 fixed physical
`h0=2`，其 `R^n/n` normalization也不是 `N0=JQ^2 asymp XQ`。该 cell不停止未来
真正保留 literal TPC coefficient、fixed `h0=2`、canonical prefix order、actual
masks/weights/outer labels、`N0` normalization与完整 physical-loss ledger的新
theorem，也不停止两个 O161 parents、pair-native reroute、H1/global architecture；
精确 type audit见第 32.7 节。

最终 pull/rebase又取得 RH-341，只新增下列精确有限 cross-program cell：

```text
DECLARED_TPC32_REMOTE_RH341_ACTUAL_FIRST_ALIAS_
SIGNED_COMPLETION_TRANSFER_V1 = STOP_SCOPED
```

它只停止把 commit `6e1478a1a02ff4c3308e829727f8fea1cfbce52c` 的 RH Hardy
trace-order absolute prefix synchronization、条件必要的 moving orders
`2k,2k-2` orbit--head compensation，或 abstract information-class
cancelling/noncancelling completions，升级为 TPC-32 同一 high-beta packet 的
ordered signed-prefix theorem、small-content matched-shell saving或 distinguished
determinant-zero theorem。RH 的 `q_(sigma,k,n)` 是 trace coefficient而不是 TPC
modulus；两个 moving orders相差 `2` 也不构成 fixed physical `h0=2`；`R^n/n`
与 `H_k` normalization均不是 `N0=JQ^2 asymp XQ`。

该 cell不停止未来真正保留 literal TPC coefficient、fixed `h0=2`、canonical
prefix order、actual masks/weights/outer labels、`N0` normalization、uniform
ranges/constants与完整 physical-loss ledger的新 theorem，也不停止两个 O161
parents、pair-native reroute、H1/global architecture；精确 audit见第 32.8 节。

2026-08-01 的 O161 pointwise current-primary version-delta refresh新增且仅新增：

```text
DECLARED_O161_DIRECT_BAD_ENDPOINT_CURRENT_PRIMARY_
VERSION_DELTA_CANDIDATES_20260801_V1 = STOP_SCOPED
```

它只停止把第 33 节逐 theorem-body 审核的 el Abdalaoui--Nerurkar
`arXiv:2006.07646v2`、Grimmelt--Teräväinen `2607.28091v1`、
Matthiesen `1606.04482v4`、Browning--Sofos--Teräväinen
`2212.10373v2`、Burstein--Iosevich--Sant `2604.14482v1`、
Pandey--Radziwiłł `2510.20194v1`、Cantarini--Gambini--Zaccagnini
`2603.10241v1`、el Abdalaoui--Lin `2607.15960v1`、
Pilatte `2604.26564v1` 与 Murty--Vatwani
*A remark on a conjecture of Chowla* 的已审核 statements，单独或跨来源
拼接后升级为 O161 的 literal two-Möbius named-atom fixed-power theorem。

Teräväinen--Walker `2303.12574`、Tao--Teräväinen
`2512.01739v2`、Pilatte `2310.19357v2`、
Klurman--Mangerel--Teräväinen `2304.05344v2` 与
Ramaré--Zúñiga Alterman `2603.25961v3` 只作为既有
`STOP_SCOPED` cells的一致性 countercheck；本 cell不重新包装或扩张
它们的旧 scope。它也不是全局文献 nonexistence claim，不停止未来直接接受
literal coefficient、actual named atom、growing parameters、正确 prefix/
normalization及完整 loss ledger的新 theorem。两个 O161 parents、pair-native
reroute、H1/global architecture继续 `OPEN`；精确公式、第一 fatal与
reopen interface见第 33 节。

2026-08-03 的 committed RH-342--348 cross-program audit新增且仅新增：

```text
DECLARED_TPC_REMOTE_RH342_348_SPECTRAL_TRACE_LADDER_PREFIX_TRANSFER_V1
  = STOP_SCOPED
```

它只停止把 commits `65dd912f36477448dec804789a93ce9a6ec1cc3a` 至
`af5864a17063adc3084c9ce025878dadb39da05c` 中 RH-342--348 的 spectral
power sums/root shells、Hardy localized orbit traces、moving-order parity scalar
balances、abstract scalar information-class completions或 punctured lower-even
absolute demand/necessary-compensation ladder，直接升级为 TPC 的
literal two-Mobius coefficient、fixed physical `h0=2`、canonical ordered prefix、
same-packet distinguished determinant zero或 42-field production pair/H1 edge。
RH-344/346/348 的 orbit ledgers在 RH program 内确为 physical；本 cell只冻结未经
coefficientwise theorem 的跨程序改名，不把它们误报为 model-only。RH moving orders
`2k,2k-2` 的差 `2` 不是 TPC affine determinant `su-ad=2`，RH clock phase也不是
TPC additive phase。该 cell不是未来 RH/TPC theorem的 nonexistence claim，不停止
新的 literal crosswalk、两个 O161 parents、TPC32 direct route、pair-native reroute、
H1/global architecture或 RH 自身路线；精确 source locks与 first fatals见第 34 节。

同日的 arXiv math.NT current-primary delta screen新增且仅新增：

```text
DECLARED_O161_CURRENT_PRIMARY_ARXIV_2607_29429V1_RANDOM_MODEL_TRANSFER_V1
  = STOP_SCOPED
```

它只停止把 Durkan--Pearce-Crump `arXiv:2607.29429v1` 对 Steinhaus或
Rademacher random multiplicative functions的 almost-sure complete-prefix bound，
改名为 actual deterministic Mobius、literal two-affine Mobius pair、prescribed
production atom、TPC32 matched-shell determinant zero或 pair/H1 theorem。该 source
明确把 Rademacher object称为 Mobius 的 probabilistic model，并以独立随机 prime
signs替代 arithmetic prime values；因此不得用“squarefree support与 signs相同”
跨过 literal coefficient gate。本 cell严格限于 2026-08-03 第 34.5 节审核的
version/source，不扩张第 33 节旧 candidates，也不停止未来 deterministic theorem。

2026-08-03 的扩展 current-primary/unfrozen candidate audit新增且仅新增：

```text
DECLARED_TPC32_20260803_UNFROZEN_SIGNED_PREFIX_AND_AUTOMORPHIC_
LARGE_SIEVE_SOURCE_CANDIDATES_V1 = STOP_SCOPED

DECLARED_O161_CURRENT_PRIMARY_ARXIV_2607_29275V1_
SPECTRAL_PROCESS_TRANSFER_V1 = STOP_SCOPED
```

第一个 cell严格限于第 35.2 节逐 theorem-body审核的 Pascadi--Thorner
`2508.14888v2`、Conrey--Kwan--Lin--Turnage-Butterbaugh `2607.00282v1`、
Schmidt `2604.23517v1`、Harper--Soundararajan--Xu `2606.29040v1` 与
Klurman--Munsch--Sun `2605.04694v1`。它只停止把 automorphic/character-family
large-sieve mean、conditional independence model、Steinhaus random function或
自由构造的 completely multiplicative signs/logarithmic subsequence，改名为同一
high-beta packet的 actual `A_C` distinguished zero、literal weighted four-Mobius
prescribed-lag coefficient或 actual evaluation-cloud full/cross-`D0` frame theorem。
这些 candidates都在 exponent ledger之前先因 coefficient/index/operator、average、
random/conditional model或 normalization mismatch失败；本 cell不是未来来源的
nonexistence claim。

第二个 cell严格限于 el Abdalaoui `arXiv:2607.29275v1` 的 spectral-process
transfer。该 source-stated qualitative average使用一个 Mobius--Sarnak process
weight与 singular-spectrum test sequence；它没有 literal
`mu(d+s*z)mu(u+a*z)`、fixed `su-ad=2`、named production atom、growing affine
parameters、uniform fixed-power error、DIRECT `q/N` terminal block、BAD
`q/T` cumulative prefix或完整 loss ledger。它不关闭两个 O161 pointwise
parents；精确 source lock见第 35.3 节。

同日的 affine-Mobius 与 actual-cloud point-frame定理回溯新增且仅新增：

```text
DECLARED_O161_20260803_NATURAL_FINITE_COMPLEXITY_AND_FIXED_AFFINE_
LOGARITHMIC_MOBIUS_SOURCE_CANDIDATES_V1 = STOP_SCOPED

DECLARED_TPC32_20260803_HYPERBOLIC_POINT_LARGE_SIEVE_SAMPLING_
AND_CONTINUOUS_PROJECTOR_SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

第一个 cell严格限于第 36.2 节逐 theorem-body审核的 Shao--Teräväinen
`arXiv:2006.05954v2` Corollary 11.1、Teräväinen `1710.01195v2`
Theorem 1.4/Remark 1.9与 Mangerel `2306.09929v4` Theorem 1.1/Remark 1.2。
natural theorem要求 finite complexity，而 O161 的两式满足
`s L2-a L1=2`、homogeneous parts平行；fixed-affine theorem则只有 logarithmic
normalization、固定参数与定性 error。两条 source lock不得拼接。本 cell不停止未来
直接接受 growing literal pair、actual packet、正确 natural prefix/normalization
与 fixed positive-power error的新 theorem；两个 O161 pointwise parents继续
`OPEN`。

第二个 cell严格限于第 36.3 节审核的 Chamizo 1996 Theorem 2.1、Pesenson
`arXiv:1104.1710` Theorems 2.5/4.4与 Anker--Germain--Léger
`2306.12827` Theorem 1.2。它只停止把 fixed-quotient weight-zero且分离的
`Gamma\\H` point large sieve、预先设计的 `rho`-lattice sampling frame，或错误
surface class上的 continuous `L2 -> Lp` projector，改名为 moving-level
`Gamma_pm(q)\\G` actual Dirac cloud的 full-`K`-type、full/cross-`D0` Gram bound。
它不停止未来 level-uniform full-group point-frame theorem或直接控制 actual signed
compact-block energy的算术 theorem；TPC32 frame parent继续 `OPEN`。

发布前 remote RH-349/350 delta audit新增且仅新增：

```text
DECLARED_REMOTE_RH349_350_LOWER_SIDEBAND_PHASE_TO_TPC_
LITERAL_OBJECT_TRANSFER_V1 = STOP_SCOPED
```

它严格锁定 commits `c548ba99faaa237c6b886bd07469569a1a37bcbf` 与
`ecad6e7d70c7b1b452ee337f17c060dd0ae790ff`，只停止把 RH noisy-operator
lower-even sideband coefficient、phase/demand minimax及仍依赖未证 actual-`Y`
remainder的 conditional physical conclusion，改名或拼接为 O161 literal
two-Mobius prefix、TPC32 `A_C`/GM cloud、42-field pair或 H1 edge。RH-349/350
在 RH program内的 exact deterministic/scalar statements不是 model-only；本 cell
不关闭 RH 自身路线，也不停止未来真正 source-backed coefficientwise RH/TPC
crosswalk。精确 type audit见第 36.4--36.5 节。

2026-08-03 的 omitted O161 primary-source delta audit新增且仅新增：

```text
DECLARED_O161_20260803_OMITTED_FH1804_HLM2604_
NATURAL_GROWING_TRANSFER_CANDIDATES_V1 = STOP_SCOPED
```

本 cell严格锁定 Frantzikinakis--Host `arXiv:1804.08556v3`
Theorem 1.3/Corollary 1.4 与 He--Liu--Ma `arXiv:2604.16840v1`
Theorems 1.1--1.3。它只停止把 fixed unit-slope shifts上的 logarithmic
multiplicative-product theorem，或 one-Mobius Furstenberg-flow short-interval
theorem，改名或拼接为 O161 literal
`mu(d+s*z)mu(u+a*z)`、fixed `su-ad=2`、growing affine、named-atom、
DIRECT `q/N` 或 BAD `q/T` positive-power theorem。它不停止未来 source版本、
直接接受 literal pair的新定理、两个 O161 pointwise parents、pair-native reroute、
H1或 global architecture；精确 theorem-body与字段审核见第 37.2 节。

同日的 full-group/nontrivial-`K` spectral source backtrace新增且仅新增：

```text
DECLARED_TPC32_20260803_FULL_GROUP_K_TYPE_SPECTRAL_PROJECTOR_
SUPNORM_AND_PRINCIPAL_BUNDLE_LOCAL_WEYL_SOURCE_CANDIDATES_V1
  = STOP_SCOPED
```

本 cell严格锁定 Ramacher--Wakatsuki `arXiv:1703.06973v3`
Proposition 3.3、Remark 3.4(1)、Proposition 4.1、Theorems 5.5/5.8/7.4；
Blomer--Harcos--Maga--Milicevic `arXiv:2107.05973v3`
Theorems 1--3/Remark 2；以及 Cekic--Lefeuvre `arXiv:2405.14846v2`
Theorems 5.1.5/5.1.8/5.1.10、Proposition 5.3.8、Lemma 5.3.10。
它只停止把 fixed closed/cocompact full-group spectral projector、单一 eigenfunction
的 non-spherical supnorm/amplified pre-trace，或 fixed closed principal-bundle 的
local-Weyl/density-one family mean，升级为 moving
`Gamma_pm(q)\\SL_2(R)` actual GM Dirac cloud 的 full/cross-`D0` Gram bound。
这里 nontrivial `K`-type 本身不是 rejection；真正 fatal 是 quotient、operator、
moving-level uniformity、actual coefficients与 global normalization。该 cell不停止
未来直接接受 actual cloud、literal weights/masks、全部 relevant `K`-types、moving
level ranges、one global `N0` normalization并支付所需 `P_X` 的新 theorem；
TPC32 frame parent继续 `OPEN`。精确 source locks见第 37.3 节。

上游 RH-351 delta audit另新增且仅新增：

```text
DECLARED_REMOTE_RH351_AFFINE_SIGNED_COMPLETION_TO_TPC_
LITERAL_OBJECT_TRANSFER_V1 = STOP_SCOPED
```

它严格锁定 commit `99d9fad06d44843ac24b9ccdb15bda09179cccf6`，只停止把
RH-351 对 formal residual arrays 的 affine completion surjectivity、close/far
budget exchange与 coefficient-ledger information-class underdetermination，改名或
拼接为 O161 literal two-Mobius prefix、TPC32 three-channel `A_C`/actual GM cloud、
42-field production pair或 H1 edge。RH-351 在 RH program内的 exact algebraic
information-class theorem是真实 scoped result；但它明确没有构造 physical noisy
operator；在 RH-351 自身的 frozen source boundary内，actual `Y_(k,j)` 仍未估。
后来的 RH-352 actual normalized theorem另由下一 cell与第 38 节管理。本 cell不关闭
RH 自身路线，也不停止未来真正 source-backed literal coefficientwise RH/TPC
crosswalk；精确 type/provenance audit见第 37.5 节。

发布前 remote RH-352 delta audit再新增且仅新增：

```text
DECLARED_REMOTE_RH352_MODULUS_CAP_FORCED_GROWING_LOWER_EVEN_
SIGNED_CANCELLATION_TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

它严格锁定 commit `2724ec0242915c8089212fef0a95f0a0de7bc892` 中
`thm:uniform-cap`、`cor:L`、`thm:Y-tracking` 与 `cor:Yagg`。必须承认 RH-352
在 RH program内真实证明 actual moving lower-even ladder 的 local/natural
normalized exponential cap，并真实否定 RH-350 的 actual aggregate small-`Y`
hypothesis；它不是 formal completion或 conditional model。本 cell只停止把 RH 的
`p=tau-a=Y+P-S`、`n=2m` trace-sideband order、absolute selected budget及
`x^(k-2)` normalization，改名为 TPC32 three-channel distinguished zero/ordered
signed prefix、O161 literal two-Mobius prefix或 H1 production edge。RH-352 自己也
明确把 unnormalized selected prefix保持 `OPEN`。该 cell不关闭 RH 自身路线，
也不停止未来真正给出 coefficientwise RH/TPC intertwiner、correct prefix order与
natural/global normalization的新 theorem；精确 source/type audit见第 38 节。

最终 remote RH-353 delta audit再新增且仅新增：

```text
DECLARED_REMOTE_RH353_CRITICAL_FIRST_LOWER_ACTUAL_PHASE_FREE_
SIGNED_COMPLETION_TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

它严格锁定 commit `bc53f19066eee6032d6cb5850b1c2031453f5893` 的
`thm:cap`、`thm:completion`、`thm:gap` 与 `cor:supply`。必须承认 RH-353
在 RH program内真实补上 RH-352 排除的 critical `2k` 与 first-lower `2k-2`
两个 boundary coordinates，证明 actual natural-scale direct cap、actual
completion laws、phase-free two-coordinate `Y` gap及 switching-coordinate
signed supply。它只停止把该 RH-specific `Y` remainder maximum/lower bound、
trace-order difference `2`与 `x^k` normalization，改名为 fixed physical
`h0=2`、TPC32 distinguished-zero/small-content saving、ordered signed prefix、
O161 literal two-Mobius theorem或 H1 edge。`p_k^0=o(H_k)`与
`p_k^-=o(H_(k-1))`在 source内仍 `OPEN`。该 cell不关闭 RH 自身路线，也不停止
未来真正给出 literal coefficientwise crosswalk、prescribed prefix order及
original/global normalization的新 theorem；精确审核见第 39 节。

本轮 remote RH-354 delta audit新增且仅新增：

```text
DECLARED_REMOTE_RH354_PARITY_FREE_NEAR_ALIAS_ACTUAL_DIRECT_TAIL_
TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

它严格锁定 commit `50fccb3c281eb1f1376e47003f74a05ee8fef534` 中
`thm:W`、`cor:band`、`thm:frontiers`、`prop:critical` 与 raw
normalization boundary。必须承认 RH-354 在 RH program内对 actual
`p_(sigma,k,n)=tau_(sigma,n)-a_n` 证明了 moving lower cut以上包含奇偶
trace orders的 normalized absolute direct-tail 渐近上界。上游 RH-282
`M_sigma<=sigma^(-1)` 只对 sufficiently small `sigma`，故 finite-`k`
boxed bound最强只能 source-backed 解读为 sufficiently large `k`；root/
limsup、linear frontier与 critical `O(1/k)` 结论不受影响。本 cell只停止把
RH trace-order absolute tail、固定 RH `q=1/2`与 `x`-power normalization
改名为 TPC32 three-channel matched zero、TPC-111/122 ordered signed prefix、
O161 literal two-Mobius prefix或 H1 edge。它不关闭 RH low-prefix/head-defect
路线，也不停止未来真正的 coefficientwise RH/TPC intertwiner。精确
theorem/type/artifact audit见第 40.1--40.5 节。

同轮对三个此前未锁定 exact source versions新增且仅新增：

```text
DECLARED_TPC32_20260803_WATT_GAUSSIAN_CUSP_FOURIER_LARGE_SIEVE_
AND_PALM_UNIFORM_MIXED_WEYL_SOURCE_CANDIDATES_V1
  = STOP_SCOPED
```

该 cell严格限于 Watt `arXiv:1302.3112v1` Theorem 1
`(1.9.12)--(1.9.16)`、Watt `1302.3127v3` Theorems 1--5/8--9，以及
Palm `1212.4282v1` Theorem 3.2.1/Corollary 3.2.3。Watt 前者真正允许
moving Gaussian level、arbitrary cusp与 nontrivial `K`-types；Palm 真正给出
level/index-uniform mixed Weyl count。但它们的 literal objects分别是 cusp
Fourier-coefficient spectral moments与 global spectral counts，不是 actual
`Gamma_pm(q)\SL_2(R)` Dirac evaluation cloud的 full/cross-`D0` Gram operator。
本 cell不注册新方法 credit，只冻结这三个 source/version的跨对象改名；
moving-level full-group actual-cloud frame parent继续 `OPEN`。精确审核见
第 40.6 节。

发布前 remote RH-355 delta audit新增且仅新增：

```text
DECLARED_REMOTE_RH355_UPPER_ALIAS_COUNTERLOOP_BURDEN_AND_HEAD_
TRANSFER_PRECISION_TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

它严格锁定 commit `4706eba4b51b3cade9f907b3dd4c93a94683ddc8` 的
`thm:burden`、`thm:conditional`、normalized weak-transfer formulas与
`prop:shell`。必须承认 RH-355 在 RH program内真实证明 deterministic
graded counterloop strict-upper absolute budget的渐近，并将 normalized burden的
`k`th root锁为 `x>1`。但 actual Hardy-head matching全部条件于未证的
same-clock `D_(4k)(R)->0`；complete-root-shell只是 finite conjugation-closed
normal information-class obstruction，不是 actual noisy operator。本 cell只停止把
RH trace-order `s_(k,n),h_(sigma,n),d=h-s` 的 absolute band、conditional
head precision或 finite shell obstruction改名为 TPC32 three-channel distinguished
zero/small-content saving、O161 literal two-Mobius signed prefix或 H1 edge。它不关闭
RH actual-head/direct-to-full routes，也不关闭 TPC32、O161、pair-native、H1
或 global parents。精确审核见第 41 节。

本轮 remote RH-356/RH-357 delta audit新增且仅新增：

```text
DECLARED_REMOTE_RH356_357_POST_ALIAS_COUNTERLOOP_DEPTH_PROFILES_
TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

它严格锁定 commits `9cd3ad606826ad980600ec4eb0963296ea813308` 与
`45ba399d7b7abef39e4fcf17f916d3c6a159936c` 的 exact `A_k,B_k(L)` ledger、
RH-356 `thm:uniform`/`thm:crossover`/`thm:integer-phase` 与 RH-357
`thm:uniform`/`cor:linear`/`thm:phase`。必须承认前者真正证明所有
`L<=ell_k=o(k)` 的 mesoscopic crossover，后者真正证明全部
`1<=L<=k-1` 的 uniform endpoint profile及每个固定
`L/k->alpha in (0,1]` 的 linear-depth rate。两篇的 actual-head结论都严格
条件于尚未证明的 same-clock `D_(4k)(R)->0`。本 cell只停止把 RH
trace-order absolute counterloop band改名为 TPC32 three-channel
small-content matched-shell distinguished zero、TPC-111/122 canonical ordered
signed fiber prefix、O161 literal two-Mobius coefficient或 H1 actual cloud edge；
尤其 `B_k(L)/A_k` 的相对 crossover不是 `N0`-normalized saving，linear-depth
root `x^alpha>1`方向相反。它不关闭 RH actual-head/direct-to-full routes，
也不关闭 TPC32、O161、pair-native、H1或 global parents。精确审核见第 42 节。

本轮 late remote RH-358 delta audit新增且仅新增：

```text
DECLARED_REMOTE_RH358_TERMINAL_LAG_GEOMETRIC_LOCALIZATION_
TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

它严格锁定 commit `a4fd6286c68fb3230e55d8465f89775f0f58fe15` 的
`prop:exact`、`thm:uniform`、`cor:regimes`、`prop:criterion`、
`thm:geometric`与 conditional `thm:conditional`。必须承认 RH-358 在同一
deterministic counterloop内真正证明 complete upper band的全 terminal-lag
relative tail、geometric `ell^1`/total-variation localization与前两矩；但其
`q`只是 trace terminal lag，`P_k(q)/C_k`是先取绝对值后的 positive cumulative
tail。actual inheritance仍条件于未证的 same-clock `D_(4k)(R)->0`。本 cell只
停止把这项 relative trace-mass localization改名为 TPC32 distinguished zero/
small-content saving、TPC-111/122 canonical signed physical-fiber prefix、O161
literal two-Mobius coefficient或 H1 actual occurrence edge。它不关闭 RH
actual-head route，也不关闭 TPC32、O161、pair-native、H1或 global parents。
精确审核见第 43 节。

本轮 late remote RH-359 delta audit新增且仅新增：

```text
DECLARED_REMOTE_RH359_LOGARITHMIC_TERMINAL_WINDOW_ACCURACY_THRESHOLDS_
TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

它严格锁定 commit `b979b87f85795a3cbb2cc4fc334f467355b0acc9` 的
`lem:log-window`、`lem:phase`、`thm:phase-law`、`cor:exponent`、
`thm:inverse`与 conditional actual-accuracy theorem。必须承认 RH-359 在
deterministic counterloop内真实证明 logarithmic terminal window的 `k^(-a)`
relative accuracy、完整 floor-phase interval与 minimal integer width；但这是
RH-358 positive absolute trace-mass tail的再参数化/反演。它的 `q`是 window
width，`Q_k(a,c)`是最小窗口整数，`a`是 model-`k` exponent；均不是 TPC
`q_DFT`、packet `Q`或 `X`-saving exponent。actual inheritance仍条件于未证
`D_(4k)(R)->0`。本 cell只停止这组跨对象/跨尺度升级；不关闭 RH actual-head、
TPC32、O161、pair-native、H1或 global parents。精确审核见第 44 节。

本轮 remote RH-360 delta audit新增且仅新增：

```text
DECLARED_REMOTE_RH360_TERMINAL_LAG_EXPONENTIAL_TILT_PHASE_TRANSITION_
TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

它严格锁定 commit `27b0b46e9f000c3f27a9546192765287734250d8` 的
exact transform quotient、subcritical/critical/supercritical phase diagram、
三个 tilted probability limits与 conditional actual-head transfer。必须承认
RH-360 在 RH program内真实证明 deterministic positive terminal-lag distribution
的 exponential-tilt phase transition；但其 literal summand
`z^r y_k^(2k-1-r)/((2k-1-r)C_k)`非负，`r`是 trace terminal lag，`z`
是人工 tilt，`C_k`是 absolute-budget normalization。它们都不是 TPC32
three-channel signed physical coefficient、determinant-DFT `r=0`、canonical
translated-integer prefix、content/`Delta#`、actual outer metadata或
`N0=JQ^2\asymp XQ`。actual inheritance仍条件于未证的 same-clock
`D_(4k)(R)->0`。本 cell只停止把该具体 positive generating-function theorem
改名为 TPC distinguished zero、growing signed-prefix theorem、O161 literal
two-Mobius theorem或 H1 occurrence edge；它不关闭 RH actual-head route、
TPC32 direct route、两个 O161 parents、pair-native reroute、H1或 global
architecture，也不是未来 literal theorem的 nonexistence claim。精确审核见
第 45 节。

本轮 2026-08-04 current-primary signed-prefix audit新增且仅新增：

```text
DECLARED_TPC32_20260804_ARXIV_2608_00184V1_RANDOM_MULTIPLICATIVE_
PERIODIC_BV_CLT_TO_ACTUAL_SIGNED_PREFIX_TRANSFER_V1
  = STOP_SCOPED
```

它只锁定 Schlitt 2608.00184v1 Theorems 1.3/1.5、prime-filtration
martingale/BDG与 Proposition 6.1 向 TPC32/TPC-111/122 actual signed-prefix
对象的非法 transfer。source coefficient是一个 Steinhaus random completely
multiplicative function，结论是按随机 law 的 CLT/moment statement；TPC对象是
fixed `h0=2` 上 deterministic `mu(d+s*r)mu(u+a*r)`、literal
translated-integer prefix及同一 three-channel
`A_hat_C,q_DFT(0)`。largest-prime filtration、fixed periodic-BV weight与
`V_g(N)` normalization均不保 determinant、content、outer labels、prefix
order或 `N0`。本 cell不关闭 future deterministic literal theorem；精确审核
见第 46 节。

本轮 2026-08-04 Angelo--Xu current-version source lock新增且仅新增：

```text
DECLARED_TPC32_O161_20260804_ARXIV_2411_14447V3_RANDOM_INITIAL_BIAS_
CRITICAL_WEIGHT_SIGN_OSCILLATION_AND_SINGLE_LIOUVILLE_REMARK_
TO_LITERAL_TWO_AFFINE_MOBIUS_PREFIX_TRANSFER_V1
  = STOP_SCOPED
```

它严格锁定 Angelo--Xu `arXiv:2411.14447v3`（2026-08-02 revision）。
Theorem 1.1 是 conditional initial bias 下 random completely multiplicative
Rademacher function 的 nonnegative-partial-sum probability；Theorem 1.2 是
random `f(n)/sqrt(n)` partial sums 的 almost-sure sign changes。v3 对尺度、
multidimensional CLT、second moment 与积分不等式作了实质 proof repairs，
但没有改变上述 theorem types。新增 Remark 3.2 只证明 deterministic single
Liouville weighted sum `sum_(n<=x) lambda(n)/sqrt(n)` 不可能最终恒正，并明确
不排除最终恒负。它们均不是同一 selected packet 上 fixed `h0=2` 的
`mu(D(t))mu(U(t))`、three raw channels、`G<=C`、canonical `Delta#`、actual
outer labels/order、`N0` normalization 或 fixed-power saving。本 cell 只停止
该版本向 TPC32 signed-prefix、O161 pointwise 或 small-content zero 的非法
transfer；不关闭 future literal theorem、两个 O161 parents、TPC32 direct/frame、
pair-native、H1 或 global architecture。精确审核见第 48 节。

第 48 节对 TPC-93 scalar common-native refinement 的 `PRESENT_L1` 修正不
新增 method cell：它是既有 exact reindexing theorem 的窄标量实例化，不是新
growing arithmetic method，更不支付 `1/400`。

第 49 节的 current-primary natural/collective source refresh新增且仅新增：

```text
DECLARED_TPC32_20260804_TAO1509_FRANTZIKINAKIS1606_LICHTMAN2009_
CHINIS2105_NATURAL_COLLECTIVE_PREFIX_TRANSFER_V1 = STOP_SCOPED
```

它严格锁定 Tao `1509.05422v4` Corollary 1.5、Frantzikinakis
`1606.08420v2` Theorem 2.1、Lichtman `2009.08969v2` Theorems 1.1/1.3 与
Chinis `2105.14653v1` Theorem 1.2 向第 49 节 exact masked-prefix/collective
outer-return gate 的非法 transfer。Tao source可接受 fixed determinant-two affine
syntax，但只有 `1/n` logarithmic terminal average；其余 sources分别只有
fixed-slope subsequence/metric outer average、equal-slope shift average或依赖
Siegel-zero subsequence；Lichtman 的 source average本身是 natural/unweighted，
logarithm只出现在 saving rate，不是 logarithmic normalization。
Grimmelt--Teräväinen `2607.28091v1` 与
Klurman--Mangerel `1708.03176v1` 只作为第 33 节及 fixed-`D0` 既有 cells的
一致性 countercheck，不重复扩张。本 cell不停止 future natural growing exact
masked all-prefix theorem、直接 `Z_C` theorem、TPC-33 collective `Q^3` energy
theorem或其他真正 literal source input；精确 theorem-body audit见第 49.5 节。

本轮 2026-08-04 current-primary O161 source lock新增且仅新增：

```text
DECLARED_O161_20260804_ARXIV_2608_00184V1_2608_01399V1_
2608_01498V1_CURRENT_PRIMARY_SOURCE_CANDIDATES_V1
  = STOP_SCOPED
```

2608.00184v1 是 random single-factor object；2608.01399v1 的 Möbius只以
`mu(gcd(k,n))` 或变换后的 `mu(ell)/ell` 出现在 regular-integer
nested averages；2608.01498v1 的 “Mertens sums” 是 prime harmonic sums/products，
不是 Möbius partial sums。三者均未到 fixed physical `h0`、actual
packet/masks/weights、prescribed phase、`q/N` terminal domain、
逐 scheduled ancestor 的 local `q/N_j` theorem、TPC-159
`N_j/T=2^(-j)` telescoping ledger或 fixed-power loss ledger，已在 literal coefficient
gate失败。不得跨三个 sources拼接；两个 O161 pointwise parents保持 `OPEN`。

本轮 2026-08-04 current-primary actual-cloud frame source lock新增且仅新增：

```text
DECLARED_TPC32_20260804_ARXIV_2608_02405V1_2608_00386V1_
2407_17959V3_GEOMETRIC_SPECTRAL_FRAME_TO_ACTUAL_CLOUD_GRAM_TRANSFER_V1
  = STOP_SCOPED
```

Tiwari 2608.02405v1 是 compact manifold 上预先设计 epsilon-discretization的
graph/Laplacian eigenvalue comparison；Magee--Roig-Sanchis--Thomas
2608.00386v1 是 closed hyperbolic three-manifolds/two-torsion line bundles的
existential spectral-gap theorem；Qi 2407.17959v3 是 fixed Picard quotient上
symmetric-square Hecke coefficients的 spectral-family large sieve。三者均不直接
作用于 moving `Gamma_pm(q)\SL_2(R)` actual signed Dirac cloud，不给
point-evaluation full/cross-`D0` Gram、actual separation/local multiplicity、
all relevant right-`K` types、literal weights或 `P_X` threshold。
不得把 compact discretization、closed-manifold gap与 fixed-group spectral mean
跨 source拼成 spatial moving-level frame theorem。TPC32 frame parents保持
`OPEN`；精确审核见第 46 节。

本轮 late remote RH-361 delta audit新增且仅新增：

```text
DECLARED_TPC32_O161_20260804_REMOTE_RH361_COMMIT_91167FE_
TYPED_SIGNED_COMPLETION_FIBER_TO_LITERAL_MOBIUS_ZERO_PREFIX_TRANSFER_V1
  = STOP_SCOPED
```

它严格锁定 commit `91167fe163831d3360b4c4007ed600865610e9ec` 的
Theorem 5.2 `thm:fiber`、Corollary 5.4 `cor:forbidden` 与
Theorem 6.1 `thm:batch`。必须承认 RH-361 在其 exact finite
coefficient-information class内真实证明 `d=e,q=p+e,h=s+e` 的
typed fiber与 nonpromotion，并真实冻结 RH-352--354 actual selected/normalized
`p,Y` branch和 RH-355--360 deterministic counterloop `s` branch。
但 arbitrary signed `e` 不构造 physical operator、determinant、root、
cross-order realization或 actual Möbius sequence；`p,s,d,q,h,Y` 的
trace/moment-order universe也不是 fixed `h0=2` 的
`mu(d+s*r)mu(u+a*r)`、three raw channels、canonical content/
`Delta#`、literal translated-integer prefix或
`A_hat_C,q_DFT(0)`。该 theorem的方向是“batch premises不足以 promotion”，
不是 cancellation、distinguished zero或 saving；same-clock
`D_(4k)(R)->0`仍未证。本 cell只停止这项 commit-specific TPC transfer；
不把 finite information-class theorem升级为 global impossibility，不关闭 RH
actual-head route、TPC32、两个 O161 pointwise parents、pair-native、H1或 global
architecture。精确审核见第 47 节。

同一 selected packet 的 row-reversal/LR-polarization 审计没有新增 method cell。
该 map交换两个 mixed raw channels、固定 both-ultra、保持 content并令
`Delta# -> -Delta#`，但 exact polarization是加号，`r=0` 时 determinant orientation
phase消失，ordered row coefficients/masks/outer keys也没有 source-backed
anti-equivariance；它是第 23 节既有 literal-coefficient/fiber-intertwiner fatal 的
一个 exact实例。不得把它换名注册为新 `STOP_SCOPED` method；详见第 37.4 节。

Carella `arXiv:2208.12219v8` 不新增 method cell。它已属于第 31.3 节及
`DECLARED_TPC32_FIXED_D0_OUTER_REGROUP_AND_POST30_DIRECT_FRAME_SOURCE_CANDIDATES_V1`
的既有 scope；第 35.4 节只补充三项独立 proof-chain fatal与 exact equation
locators，不把旧 STOP 重新包装成新方法。

2026-08-05 的全局 prime-dynamics compass只新增一个 broad cell：

```text
DECLARED_RH1_4_TPC1_20260805_AUTONOMOUS_LIMIT_INVERSE_PRIME_KNEADING_
NONAUTONOMOUS_SCHEDULE_HENON_LIFT_TO_DISTINGUISHED_E2_RECURRENCE_
DIRECT_COMPOSITION_V1 = STOP_SCOPED
```

它只停止把当前 RH-1 的 `RLR^infinity` pointwise limit、RH-2 的 inverse exact-prime
kneading parameter、RH-3 的 conditional sequential Birkhoff architecture、RH-4 的
area-preserving Hénon construction、TPC-1 的 finite primorial local pair mass与已发表
prime--logistic heuristic直接拼接成 distinguished arithmetic orbit的 gap-2 infinite
recurrence。第一处 literal mismatch是：positive ACIP measure与 ergodicity属于
`u_c` 的 typical attractor orbit，arithmetic-faithful coding属于另一个 exact prime
word或 moving finite-sieve diagonal；当前没有保持 stage、time、event、measure与
specified seed的同一 crosswalk。它也停止把 fixed positive ordinary invariant mass
无 normalization 地替代自然尺度 `1/(log n)^2` 的 moving rare-event mass。

本 cell不停止 profinite/primorial moving-target formulation、strengthened exact
stage-preserving isomorphism、nonautonomous matched tower/rank-two cocycle、
rare-event mass与 covariance theorem、distinguished-seed dynamical
Borel--Cantelli/discrepancy theorem、真正 Hénon semiconjugacy/event pullback、
TPC-1 prime-sensitive survivor-to-prime bridge、现有 analytic TPC parents或任何
独立新 theorem。精确对象分离、条件 closure lemma与 reopen interface见第 52 节。

2026-08-05 的 `TPC_review3` big-road V2再新增且仅新增一个 broad crosslink cell：

```text
DECLARED_TPC_REVIEW3_20260805_PAIR_O161_PACKET_TO_PRIMORIAL_
LINEAR_CROSSLINK_DIRECT_COMPOSITION_V1 = STOP_SCOPED
```

它停止把 post-TT-star pair/Gram、O161 affine cofactors或 TPC-32 packet energy直接
改名成 canonical primorial incidence array或 `W_k`。第一处 fatal同时包含 object
alphabet与 linear/quadratic type：O161 affine values一般不是 `P_k` divisors；Gram
data不保留 pre-TT-star signs；两侧 masks、outer labels、prefixes、clocks与
normalization也没有同 source operator支付。本 cell不停止 primorial deletion/Haar
covariance、TPC-32/34/37 analytic parent、两个 O161 pointwise parents、pair-native
reroute、legacy H1或 global architecture。只有第 53.5 节 coefficientwise `J_X`
theorem连同完整 physical return形成，才可重开。

## 7. Reopen triggers

TPC-204 没有让既有五类 trigger 通过：

```text
DIRECT = FAIL
METRIC = FAIL
BAD_ENDPOINT = FAIL
STRUCTURAL = FAIL
DECLARED_CORPUS = FAIL
```

只有真正新增的 theorem-backed 输入才允许提出 reopen：

- `DIRECT`：同一 source-locked production record 上七字段完整，且有
  natural-`q/N` named fixed-atom positive-power theorem；
- `METRIC`：source-locked named atom + exact packet schedule +
  schedule-specific exceptional-limsup avoidance theorem；
- `BAD_ENDPOINT`：literal fixed-atom local-increment cancellation theorem，
  并通过常数、范围、归一化和损失；
- `STRUCTURAL`：直接填补
  `H1.source_backed_local_occurrence_edge_family` 的 theorem-backed
  local-occurrence edge；
- `DECLARED_CORPUS`：真正新增的 primary theorem source，直接控制
  prescribed determinant-two two-Möbius atom
  `mu(d+s*z)mu(u+a*z), s*u-a*d=2`，并通过六轴、常数、范围、归一化
  和完整损失。

第 32 节对五类入口作了 post-第 31 节有限刷新；状态仍为：

```text
DIRECT = FAIL
METRIC = FAIL
BAD_ENDPOINT = FAIL
STRUCTURAL = FAIL
DECLARED_CORPUS = FAIL
```

其中 `DIRECT/DECLARED_CORPUS` 没有 prescribed natural positive-power theorem；
`METRIC` 先在 determinant DFT zero与 additive atom的对象类型处失败；
`STRUCTURAL` 仍没有同 packet production carrier，TPC-175 coverage保持 `0/2988`；
`BAD_ENDPOINT` 没有新的 literal fixed-atom local-increment theorem。该刷新不把
failure写成全局不存在定理，也不改变上述未来 trigger定义。

第 33 节又分别按 `q/N` terminal/block DIRECT与 `q/T`
cumulative BAD_ENDPOINT合同审核 current-primary version delta。两路都先缺
source-locked named production atom/actual record；反事实补齐 data后，审核的
single-source theorems仍没有 literal two-sign coefficient、prescribed tuple、
正确 bad-scale local block、uniform fixed power或完整 ledger。因此：

```text
DIRECT = FAIL_CLOSED_PARENT_OPEN
BAD_ENDPOINT = FAIL_CLOSED_PARENT_OPEN
CURRENT_PRIMARY_SINGLE_SOURCE_SURVIVORS = 0
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
TPC207_TRIGGER = false
```

用户授权本身不能替代任一数学 trigger。

## 8. 机器证书与信任边界

TPC-204 有两个分离角色：

```text
tpc204_source_locked_production_registry_crosswalk.py
  = authoritative materializer / primary contract

tpc204_independent_checker.py
  = independent read-only verifier
```

独立 checker 不 import builder、materializer 或 `build_payload`；只 import
Python 标准库。它独立冻结九个 candidate IDs、row digests、source
selectors、mutation 名单和 artifact hashes，防止 producer 的
common-mode 自证。

最终攻击矩阵：

```text
base exact-schema mutations = 12/12 rejected
coordinated regenerated-schema semantic mutations = 45/45 rejected
nested bool/int type-confusion mutations = 5/5 rejected
duplicate JSON keys = rejected
NaN/nonfinite JSON = rejected
python -O fail-closed CLIs = 3/3
source hashes = 15/15 verified
manifest hashes = 11/11 verified
exact schemas = 2/2 verified
```

独立 exploit review 还确认拒绝：

```text
producer-side candidate omission/replacement
mutation-name collapse while preserving advertised counts
source content + source-lock coordinated rebinding
```

manifest 的信任模式：

```text
REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE
```

它是 repository review pin，不是外部签名或 theorem evidence。若代码与
manifest 一起改变，仍必须做普通 git diff/commit review。

## 9. PDF 与最终验证

稳定 PDF：

```text
pages = 4
page size = A4
overfull boxes = 0
undefined references/citations = 0
embedded/subset fonts = 19/19
visual page inspection = 4/4 PASS
```

最终正向复核：

```text
TPC-204 builder --check = PASS
TPC-204 materialization contract --check = PASS
TPC-204 independent checker --check = PASS
TPC-194--203 batch builder --check = PASS
TPC-194 hardening --check = PASS
TPC-203 standalone --check = PASS
git diff --check = PASS
independent mathematical claim review = PASS
independent machine exploit review = PASS
```

保留且不得暂存、修改或删除的无关未跟踪文件：

```text
papers/tpc-105-provenance-preserving-affine-map-quotient/experiments/__pycache__/
papers/tpc-63-canonical-cofactor-provenance/main.aux
papers/tpc-63-canonical-cofactor-provenance/main.bbl
papers/tpc-63-canonical-cofactor-provenance/main.blg
papers/tpc-63-canonical-cofactor-provenance/main.log
papers/tpc-63-canonical-cofactor-provenance/main.out
papers/tpc-63-canonical-cofactor-provenance/main.pdf
tmp/
```

## 10. 不编号 single-record extraction audit

2026-07-30 用户选择了 route (1)。本轮只审核当前仓库、全部可达 Git
历史与远端 refs 中能否抽取一个
`SOURCE_LOCKED_NAMED_PRODUCTION_ATOM_RECORD`；没有把授权本身当作
record 或 theorem evidence。

唯一最接近的来源链为：

```text
TPC-18 actual tail/opened-d partition
  -> TPC-25 opened-row provenance
  -> TPC-32 physical matched shell
  -> TPC-93 resolved fixed-h0 packet family
  -> TPC-94 signed phase/conductor
  -> TPC-108 literal generic block
  -> TPC-127 determinant-two specialization/prefix isometry
  -> TPC-194 PHYSICAL_PACKET_PREFIX
```

这条链 source-backed 地给出每个 resolved key 的 literal carrier、
decorated coefficient、symbolic phase、per-key prefix 与 outer
multiplier。但是：

- `Xi_X(K,R)` 只是在 fixed `X,K,R` 下实际 export 中出现的
  `xi=(theta,c,kappa,r)` 的有限集合；它没有跨尺度
  `ambient_scale_id/packet_id/terminal_T/physical_occurrence` rows，
  因而不是 exact all-scale production schedule；
- `alpha_xi_X` 随 `X,theta,c,kappa,r,q_X` 变化。仓库没有
  source-located selector 证明同一个 `alpha_star` 在每个 required
  scale 实际出现；
- TPC-197 排除非零 fixed rational atom 通过无限多个不同 prime
  conductors `q_X` 重复出现；conductor-one 分支仍没有
  occurrence/schedule/range-admissibility theorem；
- 当前 tree、untracked text scope、全部可达 commits、remote heads 与
  tags 中没有非空 `named_physical_atom_id`、
  `phase_value_mod_1` 或 `packet_schedule_source_locator`。TPC-204 后
  没有 TPC 路径变化；RH 中的 `det_2` 命中属于谱 determinant，不是
  `su-ad=2` two-Mobius carrier。

逐字段结果：

```text
literal determinant-two carrier       = COMPLETE_PER_PACKET
physical prefix domain/index          = COMPLETE_PER_PACKET
decorated coefficient                 = COMPLETE_PER_PACKET
outer multiplier                      = COMPLETE_PER_PACKET
symbolic alpha_xi_X                    = COMPLETE_PER_PACKET
named_production_atom                 = MISSING   [first mismatch]
exact_cross_scale_packet_schedule     = MISSING
common_X_N_q_ranges                   = MISSING
uniform_constant_C                    = MISSING
positive_sigma                        = MISSING
target_normalization_selection        = MISSING
complete_physical_loss_ledger         = MISSING
```

禁止把 archive/resolved key 当作 production schedule，禁止令
`q_X=a*s`，也禁止选择一个随尺度变化的 `alpha_xi_X` 后称其为 fixed
named atom。

反事实 theorem crosswalk 也为负：即使七字段全部 supplied，TW25 的
native normalization 仍是 reciprocal/logarithmic 且只有 qualitative
`o(1)`；TT26 仍只给 terminal block、删除 exceptional scales且只有
log saving。因此在本轮已审核的 TPC-193 七源及所列 external
near-neighbor theorem scope 内，不存在可与该 record literal
crosswalk 的 fixed-data uniform positive-`X`-power
all-prefix/all-scale theorem。

最终不编号 verdict：

```text
SOURCE_LOCKED_SINGLE_RECORD_EXTRACTION = FAIL
first_record_mismatch = NAMED_PRODUCTION_ATOM
counterfactual_complete_record_theorem_trigger = FAIL
mathematical_reopen = false
tpc205_authorized = false
```

这只关闭当前 source/history/ref scope，不声称所有未来 production
records 或定理不存在。

## 11. 不编号 single-cut 到 actual packet 审计

2026-07-30 用户选择先审核 structural single-cut 路线。本轮授权仅为：

```text
UNNUMBERED_SINGLE_CUT_TO_ACTUAL_PACKET_CROSSWALK_AUDIT
```

它没有自动授权 TPC-205。用于 fail-fast 的选定 production cut archive
row 为：

```text
cut_path_id
  = cut|X=512|h0=2|ell=103|k=5|d=1|jL=6|jK=3|D0=0|type=TAIL
archive_address = (103,5,1,6,3)
terminal_type = FRONTIER_UNMAPPED
frontier_reason = NO_TAIL_ROOM
physical_normalization = nu_X
support_role = FORMAL_SUPPORT_ENVELOPE
numeric_coefficient_nonzero_status = UNDECIDED
native coefficient
  = -Lambda(103) r_4(517) W(515/512)
```

对应链的 native/path/cut/obligation/shadow/formal records 分别实际
出现于：

```text
TPC-133 sample line 724
  integrity = e550d2d7be48d85076919a8adf86ba446f88f75b404df48c0483d3cf27b59369
TPC-134 sample line 2554
  integrity = fb013b12446318c3f902909a479ddefb8329e771e936e58a2dfcc47a9e450b4f
TPC-136 sample line 2554
  integrity = 2eef9d8670c23ffc10b2a9cab0d488b0908293cfdb482667da824e702a1347cc
TPC-143 obligation line 26
  integrity = 368c72239ffa82bf7cb0731cc55f18bc696ddea7e8d4d6cbf19df374a811f7d5
TPC-153 shadow line 26
  integrity = 4251a4db295bf7f5fef76fd851fbab2899b8606191478ffd3e52e9e77d639c4c
TPC-154 formal fibre line 26
  integrity = 2fc1d9e30e0f23a6e645f9c4fbb335d4e4fec817598e2483e883f0d3a939a14a
```

TPC-143 对该 cut 给出
`actual_map_edges=[]`；TPC-153 的
`partial_occurrence_id=cut-shadow|2ff38d6cc9f3de3eb0b7ed2b`，
`actual_occurrence_id` 与 `actual_branch_count` 均为空；TPC-154 只有
互不唯一的 `FORMAL_ONLY` completions。

上游整数重标号本身成立：

```text
alpha_0 = (ell,d) = (103,1)
j_0 = k/d = 5
m_alpha_0 * j_0 = ell*k = 515
m_alpha_0 * j_0 + h0 = 517
```

因此 TPC-18/TPC-25 的 opened-row 数值、target 与 smooth arguments
相容。甚至可以手工选择

```text
gamma_0 = (107,1)
u = 11
sigma = 47
v = 1
```

使 `517=11*47`，并得到条件式 affine pair

```text
D_theta(t) = 1 + 47*t
U_theta(t) = 11 + 515*t
47*11 - 515*1 = 2.
```

这只证明：若满足 TPC-93 retained-source domain 的完整
`omega=(L,alpha,gamma,j,u)` 已经 supplied，包括未由 cut source-lock
的 `T<u<=U0` schedule，则其 source-child inverse 在代数上相容。再
手工 supplied

```text
c = kappa = B = 1
tau = 0
```

才可进入条件式 content-resolved 分支

```text
D_xi(z) = 1 + 47*z
V_xi(z) = 11 + 515*z.
```

此后 content/progression、TPC-127 pullback 与 TPC-194 per-key formula
可以内部相容。它不证明该 `omega` 由原 cut 产生；手选 `gamma_0`、
`u`、schedule、polarization、`c/kappa/B/tau` 或 content-resolved
template 均不是 theorem evidence。

决定性断点在 TPC-18 的实际公式

```text
|T_D|^2 \ll_W J (E_D + C_D^off).
```

它是 Cauchy/TT-star 后的二次不等式，不是原 cut coefficient 的线性
保守分解。原 cut 只确定 `alpha,j`；off-diagonal parent 还需要
`gamma`，opened ultra layer 还需要 `u`。取 `gamma=alpha` 不能补洞：
它属于独立 diagonal energy，且 generic/off-diagonal mask 删除对角。
TPC-93 的 projector weights 只重构已经 supplied 的 source atom
`omega`，并不逐列重构 Cauchy 之前的 cut coefficient。

因此精确第一缺口为：

```text
CUT_TO_CANONICAL_PARENT_AND_INVERSE_AGGREGATED_COEFFICIENT_CROSSWALK
```

这里的 `CANONICAL_PARENT` 仅指 TPC-143
`canonical_parent_and_QD` 所需的 typed parent-key field；它不证明、
也不得冒充 `H1.canonical_minimal_representation_certificate`。

四项主 fail-fast 结果：

```text
SOURCE_BACKED_CANONICAL_PARENT_GAMMA_U = FAIL
COEFFICIENTWISE_LINEAR_CUT_LIFT = FAIL
EXACT_RATIONAL_EDGE_CONSERVATION_AND_ACTUAL_ID = NOT_TESTABLE
H0_AND_NU_X_LINEAGE
  = FAIL:H0_COMPATIBLE_BUT_END_TO_END_NOT_SOURCE_LOCKED
```

两个 auxiliary patch verdict：

```text
NONEMPTY_CONDITIONAL_AFFINE_PAIR = PASS
NONEMPTY_SOURCE_BACKED_PRODUCTION_PATCH = FAIL
```

TPC-174 不能被用来把这些缺口 schema-complete：其
`actual_occurrence_id` 只是 supplied 非空字符串，未独立验证 archive
membership、具体 occurrence 语义或公式导出的 edge weight；其 production
join 又硬锁 TPC-173 的 TPC-133--172 corpus，而该 corpus 的 qualifying
claim count 为零。opened row、TPC-153 shadow、裸 `omega` 或裸 `xi`
均不得通过字符串改名成为 actual occurrence。

历史核查在 TPC snapshot `1cf3c8f` 覆盖从当时 34 个 enumerated refs
可达的 318 个 commits，并检查相关链的 75 个历史 text blobs。发布前
fetch 新增的 `7429c87`、`e57a0e2` 仅改 RH series 与 `RH_HANDOFF.md`；
单独 diff scan 未发现 TPC corridor 或 `TPC_HANDOFF.md` 变化，相关
75 个 text blobs 不变。候选只命中
native/path/cut/obligation/shadow/formal records；没有 non-null actual
occurrence、nonempty actual edge，或 cut-to-`omega`/`xi` locator。这
不声称 unreachable/pruned objects 或未列 source universe 中不存在新
theorem。

平台检查备注：

```text
TPC-133 --check = PASS
TPC-143 --check = PASS
TPC-153 --check = PASS
TPC-154 --check = PASS
TPC-173/174/179 --check = PASS
TPC-134/135/136 legacy raw-byte checks on LF checkout = FAIL_CRLF_PIN_ONLY
canonical/in-memory regenerated semantic content = MATCH
git diff on those artifacts = EMPTY
```

TPC-134/135/136 的失败来自历史 CRLF raw-hash pins，不是公式、记录或
生成内容漂移；它既不是数学 trigger，也没有在本轮被顺手修改。

最终不编号 verdict：

```text
UNNUMBERED_SINGLE_CUT_TO_ACTUAL_PACKET_CROSSWALK_AUDIT = FAIL_CLOSED
first_missing
  = CUT_TO_CANONICAL_PARENT_AND_INVERSE_AGGREGATED_COEFFICIENT_CROSSWALK
SINGLE_CUT_STRUCTURAL_REOPEN_TRIGGER = FAIL
mathematical_reopen = false
tpc205_authorized = false
```

这只关闭上述 singleton-cut 直接组合 method cell。只有新的 theorem
精确重建原 cut coefficient、逐列 conservation、`gamma/u` 与 `nu_X`
lineage，才可触发 H1 structural reopen。把 source domain 移到
post-TT-star pair-native atoms 属于 architecture reroute；它必须新增
distinct registry 与 theorem-backed crosswalk，不能自动记作 reopen。
H1 architecture 与两个 O161 parents 保持 `OPEN`。

## 12. 不编号 pair-native post-TT-star 审计

2026-07-30 用户授权路线 1。本轮授权仅为：

```text
UNNUMBERED_PAIR_NATIVE_POST_TTSTAR_REPAIR_AUDIT
```

它没有自动授权 TPC-205，也没有解除任何数学门槛。

本节是 TPC-205 编号前的历史审计记录。下文出现的
`tpc205_authorized=false` 仅记录当时的 workflow 状态；该状态现已由用户
后续有限授权和第 13 节的已完成论文取代。公式门槛、失败 gate 与
`STOP_SCOPED` 结论没有被授权动作改写。

### 12.1 公式级 ordered pair 与 exact coefficient

TPC-18 的实际 post-Cauchy/TT-star 公式为

```text
|T_D|^2 \ll_W J (E_D + C_D^off).
```

`C_D^off` 的 ordered summation domain 是同一 opened-`D` packet 内的
`(alpha,gamma,j)`，其中 `alpha != gamma`。`gamma` 是平方展开产生的第二
dummy row，不是 singleton cut 选择或生成的字段。TPC-18 显示的 pair
coefficient carrier 仍含 `B` aliases，其形式为

```text
mu(d_alpha) mu(d_gamma)
(log ell_alpha)(log ell_gamma)
r_R(N_alpha(j)) r_R(N_gamma(j))
B_alpha(j) B_gamma(j).
```

TPC-18 的相关权重为实数；TPC-32 又显式规定 “No complex conjugation is
implicit”。因此若后续采用 Hermitian 记法，第二侧共轭必须显式记录，不能
通过解释性改写暗中补入。diagonal energy `E_D` 与 off-diagonal pair
分离；generic mask 删除 diagonal，但公式 support 仍不等于实际非零
occurrence。

TPC-32/TPC-93 的 matched symbolic parent 为

```text
w_{alpha,gamma,j}
  = gamma_alpha^(1) gamma_gamma^(2)
    A_{alpha,gamma}(j) K^sh_{alpha,gamma}(j),

K^sh_{alpha,gamma}(j)
  = C_{m_alpha}(j) H_{m_gamma}(j)
    + H_{m_alpha}(j) C_{m_gamma}(j).
```

`u` 不是 parent `(alpha,gamma,j)` 字段。它只在打开 ultra increment 后由
两个极化分别产生：

```text
L: T < u <= U0 and u | N_alpha(j)
R: T < u <= U0 and u | N_gamma(j).
```

因此 TT-star 第二行 `gamma` 的来源、以及 supplied parent 上打开
polarization 后的 `u` 枚举，各自在公式层成立；两者之间不存在已经审核
通过的 production `pair -> omega` bridge，也不能回填到原 singleton cut。

### 12.2 TPC-93 source-child reindexing

给定 retained source atom

```text
omega = (L/R,alpha,gamma,j,u),
```

TPC-93 对每个 `v | gcd(d,e)` 给出唯一 child `(theta,t)` 及显式
child-to-source inverse。其 algebraic multiplicity 是 `tau(gcd(d,e))`，
而 projector identity

```text
sum_{v | d,e} lambda_{G_X^row}(v)
  = 1_{gcd(d,e) <= G_X^row}
```

单个 `v`-child 不恢复 source atom；各 child 保留逐项符号与 coefficient，
对 `v` 加权求和后才恢复带 actual row-gcd mask 的 source coefficient。
`gcd(d,e)>G_X^row` 时该 contribution 为零。这里的 `G_X^row` 是 row-gcd
cutoff，不得与后续 target-content 参数混同。两个 polarizations 各出现
一次，符号与 coefficient 精确重组，不增加新的 fiber normalization。若
content、frequency 与 resolved fields 也分别 supplied，则
TPC-93/94/108/127 后续的 content、phase 与 determinant-two pullback
templates 在公式层相容。

因此只有以下分离结论通过：

```text
supplied retained omega -> theta source-child inverse = PASS
separately supplied downstream fields -> xi template
  = CONDITIONAL_FORMULA_COMPATIBLE
pair -> omega production crosswalk = FAIL
```

具体 admissible `xi` 与 concrete production row-pair/`omega`/`xi`
archive join 均未形成。

### 12.3 两个有限见证的严格标签

当前最强 dual archived-row candidate 为

```text
t0 = ((103,1),(107,1),5), h0 = 2
N_alpha = 517 = 11*47
N_gamma = 537 = 3*179
gcd(N_alpha,N_gamma) = 1
Delta# = -4
ordered row determinant = 2*(103-107) = -8
```

TPC-133 sample lines 724 与 736 的 native row integrity 分别为

```text
e550d2d7be48d85076919a8adf86ba446f88f75b404df48c0483d3cf27b59369
633e20ac5a83d425471be3ba095df10a1635c3f45ce5cac6def9d5ba936152d9
```

TPC-136 sample lines 2554 与 2602 的 cut integrity 分别为

```text
2eef9d8670c23ffc10b2a9cab0d488b0908293cfdb482667da824e702a1347cc
cdc0f7363ab88106ce65bb46da800c05c3fba2b391d9490d7b2ca8bab8c816db
```

两条 cut 都是 `FRONTIER_UNMAPPED / NO_TAIL_ROOM`。这个对象只能标记为

```text
DUAL_SOURCE_LOCKED_ROW_PAIR_CANDIDATE
```

不能标记为 production pair occurrence，因为归档中没有共同 pair ID、
实际 joint-mask value、source-locked `delta` 与 row schedule、
`T/U0`、prefix/divisor/polarization children、inverse-aggregated
coefficient、pair nonzero status，或 `nu_X` global-normalization return。
两条 individual row AST 的乘积也不得自动等同于 TPC-18 显示的
`B_alpha B_gamma` pair-coefficient carrier。

TPC-32 certificate 直接归档并检查的 finite primitive witness 只包括
`h=2,j=1,d=1,L=100,R=12,T=50,U0=200,C=30`、rows、targets 与 content
matrix。把其中前两行代入 TPC-93 source-child formulas，可手工推导出
以下严格有限 `L0` affine-child witness：

```text
L=100, R=12, T=50, U0=200, h=2, j=1, d=1
alpha=(59,1), gamma=(71,1), u=61
sigma=1, v=1, d0=0, t=1, u0=2
D(t)=1, U(t)=61, determinant=2, projector weight=1.
```

这些 child fields 不是 TPC-32 certificate 直接检查或输出的字段。组合
对象只能标记为

```text
TPC32_PRIMITIVE_FIXTURE_PLUS_TPC93_FORMULAS_DERIVED_L0_ONLY
```

它只证明 algebraic schema 非空。TPC-32 自身禁止把该 fixture 提升为
production/asymptotic evidence；TPC-93 verifier 的 synthetic `h0=1`
fixture 也不能冒充 production `h0=2`。

### 12.4 归档与 schema fail-closed 审核

在快照
`ad1366d8d4870dc6170a451345df58aec54e8675` 上，历史扫描覆盖 34 refs、
321 reachable commits、11,752 reachable object entries、7,190 text
blobs 与 1,855 record-like data blobs。TPC-18/25/32/93/94/108/127/194
走廊包含 119 reachable entries、112 unique paths、95 text files 与
14 个可解析 JSON。具体 record keys

```text
row_pair
row_pair_id
source_atom
resolved_key
omega
theta
xi
polarization
actual_occurrence_id
physical_occurrence_id
```

均没有形成 concrete source-locked join。TPC-145 的 actual edges 为空；
TPC-153 是 shadow；TPC-154 是 formal；TPC-155/174 是 synthetic，均不能
补 production occurrence。

现有 H1 schema 也不能通过填字符串修补：

- TPC-143 V1 固定 `actual_map_edges=[]` 与 `NOT_TESTABLE`；
- TPC-163/173 硬锁旧 corpus/count，扩展须新建 V2；
- TPC-174 的 occurrence ID 只验证非空字符串，cut address 不验证 archive
  membership 或完整 `X` packet scope，normalization 只做字符串相等，
  edge weight 未与实际公式绑定，AST 只复制不执行；若
  `actual_occurrence_id` 被解释为 target carrier，其 global uniqueness
  会排除 many-to-one，因此新 schema 不能直接复用该约束；
- TPC-178 的 tuple/hash/lex order 不是 canonical/minimal theorem；
- TPC-179 V1 必须保持原样，新路线须用独立 integration/root。

pair registry 必须保持 ordered pair，不得按交换对称 quotient；还必须分离
`edge_instance_id` 与 `target_occurrence_id`，并把 formal support 与
numeric nonzero status 分开。

### 12.5 normalization 与完整 loss ledger

当前 source-backed 公式只能冻结 TPC-18 的 unnormalized `T_D`
inequality。TPC-133/136 中的 `physical_normalization="nu_X"` 只是 scope
字符串；归档没有给出其数值 scalar 定义，也没有 theorem 证明它乘在
`T_D` 上。若未来 theorem supplies multiplicative scalar `c_X`，才可作
条件式推导

```text
|c_X T_D|^2
  <= C_W |c_X|^2 J (E_D + C_D^off).
```

后续 registry 必须分别记录 source/linear/quadratic/target normalization，
不能只复制一个 `nu_X` 字符串。完整 physical-loss ledger 必须区分以下
已量化 terms 与未供应 slots：

```text
prime-power error: X L^(-1/2) X^eps
dyadic-D partition:
  fixed bounded overlap
  O(log X) nonempty D-slices
  reassembly/pigeonhole cost <= one O(log X) factor
Cauchy factor J
diagonal: E_D << X^(1+eps)
same/near/gcd removals:
  same: XQ L^(-1) X^eps
  near: XQ (X^(-kappa)+L^(-1)) X^eps
  gcd:  XQ X^(-kappa+eps)
generic remainder = UNCONTROLLED_HARD_REMAINDER
TPC-25:
  zero: XQ{(log X)^(-A)+X^(-s+kappa+o(1))}
  principal: Q^2 X^eps
  drift: JQ^2 L^(-1) X^eps
  polylog: (log X)^(O(1))
TPC-32 drift: X^eps XQ/L
large content: X^eps XQ(1/J+1/C)
TPC-93 Fourier tail: X^(o(1)) N0 Rwin^(1/2-K)
square-root return = MISSING/UNSUPPLIED
full-block and endpoint reassembly = MISSING/UNSUPPLIED
```

本轮没有为 complete active pair、uncontrolled hard remainder 或目标
theorem 产生 uniform positive-power estimate，故 target
`positive_sigma`、strict-loss、endpoint `1/400` 与 `L2` credit 均不得
记账。已量化的 degenerate/drift savings 不能被提升为 hard-remainder 或
目标 theorem credit。

### 12.6 精确 first missing 与最终裁决

第一项 production 缺口冻结为

```text
SOURCE_LOCKED_POST_TTSTAR_ORDERED_PAIR_REGISTRY_WITH_COMPLETE_PAIR_COEFFICIENT_AND_GLOBAL_NORMALIZATION
```

其内部两个不可省略的 subgates 是：

```text
PAIR_NATIVE_POST_TTSTAR_ACTUAL_REGISTRY_WITH_FULL_LITERAL_SCOPE_AND_COEFFICIENT
TPC18_PAIR_TO_TPC93_RETAINED_SOURCE_ATOM_THEOREM_CROSSWALK
```

H1-E/TPC-143 的 conceptual object 是从 production cut columns 出发的
linear cut-to-occurrence map `L_X`，其 entries 概念上允许 signed/complex。
当前 TPC-174 finite contract 才进一步要求 2,988 个 production cut
columns 上的 nonzero exact-rational weights 与逐 cut column sum 1。
TPC-18 的 ordered pair 则是二次不等式生成的
`TTSTAR_BILINEAR_PAIR_TERM`。两者类型不同；当前没有从 pair registry
线性逆聚合回每条 cut coefficient 的 theorem。

最终 gates：

```text
ORDERED_POST_TTSTAR_PAIR_DOMAIN = PASS_FORMULA
TPC18_DISPLAYED_PAIR_COEFFICIENT_WITH_B_ALIASES = PASS_FORMULA
SECOND_ROW_GAMMA_FROM_TTSTAR_EXPANSION = PASS_FORMULA
U_FROM_SUPPLIED_TPC32_93_PARENT_POLARIZATION = PASS_FORMULA
TPC93_SOURCE_CHILD_REINDEXING = PASS_L1_ON_SUPPLIED_RETAINED_OMEGA
CONCRETE_DUAL_ARCHIVED_ROW_CANDIDATE = PASS_ROW_ONLY
TPC32_TPC93_DERIVED_AFFINE_CHILD = PASS_DERIVED_L0_ONLY

ACTIVE_PRODUCTION_PAIR_OCCURRENCE = NOT_TESTABLE
FULL_LITERAL_PAIR_COEFFICIENT_MATERIALIZATION = NOT_TESTABLE
PAIR_COEFFICIENT_MATERIALIZATION_AND_NONZERO = NOT_TESTABLE
SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK = FAIL
NU_X_NORMALIZED_RETURN_TO_H1 = FAIL
H1_E_REPAIR = FAIL

PAIR_NATIVE_FORMULA_GATE = PASS
PAIR_NATIVE_ARCHITECTURE_REROUTE_CANDIDATE = OPEN
PAIR_NATIVE_PRODUCTION_REOPEN_TRIGGER = FAIL
PAIR_NATIVE_STRUCTURAL_REOPEN_TRIGGER = FAIL
pair_native_mathematical_reopen = false
tpc205_authorized = false
```

结论是：pair-native 路线没有被数学上关闭，但它不是现有 H1-E 的 repair；
它只作为需要新 registry、DAG/root 与 theorem-backed crosswalk 的
architecture reroute 存活。active support `A` 与 canonical/minimal
representation `M` 仍是独立 `NOT_TESTABLE` roots，即使未来补齐上述
crosswalk 也不会自动消失。H1 architecture、两个 O161 pointwise parents
与 global architecture 保持 `OPEN`。

## 13. TPC-205 的精确有限结论

用户后续显式授权的范围仅为：

```text
FINITE_PAIR_NATIVE_POST_TTSTAR_REGISTRY_AND_ARCHITECTURE_REROUTE_INTERFACE
```

授权是 workflow input，不是 theorem evidence；它没有让 production、
structural、arithmetic 或 `L2` reopen trigger 自动通过。TPC-205 的精确
分类、定理状态和裁决是：

```text
classification
  = PAIR_NATIVE_POST_TTSTAR_REGISTRY_INTERFACE_L1
theorem_status
  = PROVED_TYPED_INTERFACE_AND_FIRST_MISSING_L1
verdict
  = PAIR_NATIVE_ARCHITECTURE_REROUTE_INTERFACE_CERTIFIED_NOT_REOPENED
```

### 13.1 typed interface 与 declared-corpus 边界

TPC-205 区分四类不可互换的 relation：

```text
TTSTAR_BILINEAR_PAIR_TERM
LINEAR_CUT_TO_OCCURRENCE_EDGE
TPC93_RETAINED_SOURCE_ATOM
TPC93_SOURCE_CHILD
```

它冻结 42 个 required registry fields，并保持 `(alpha,gamma,j)` 为
ordered pair；不得作交换 quotient。`pair_record_id`、
`edge_instance_id` 与 `target_occurrence_id` 分离；formula support、
evaluated mask、coefficient evaluability 与 nonzero status 分离；
source、linear、quadratic TT-star 与 target-return normalization 分离。

17 个 source locks 支持该有限接口。当前 production count 为：

```text
production_pair_records = 0
scope = DECLARED_TPC205_REGISTRY_SOURCE_LOCK_CORPUS_ONLY
```

该零值不是全仓库、全历史或数学上的 nonexistence theorem。两个有限对象
分别严格标为：

```text
DUAL_SOURCE_LOCKED_ROW_PAIR_CANDIDATE = ROW_ONLY
TPC32_PRIMITIVE_FIXTURE_PLUS_TPC93_FORMULAS_DERIVED_L0_ONLY
  = DERIVED_L0_ONLY
```

它们只用于 `L0` regression，均不构成 production pair occurrence。
TPC-18 显示式 pair carrier 中的 `B` aliases 没有被解释性展开；完整
literal coefficient 仍是缺失字段。TPC-18 pair 也没有被强行等同为
TPC-32/TPC-93 parent，故 `pair -> omega` 仍为 `FAIL`。

### 13.2 normalization 与 loss 防火墙

归档字符串 `"nu_X"` 只保留为 scope label，不是已供应的数值 scalar。
若未来 theorem 供应乘法 scalar `c_X`，当前只许可条件式

```text
|c_X T_D|^2 <= C_W |c_X|^2 J(E_D+C_D^off).
```

17 行 loss ledger 中，每条 TPC-18/25/32/93 bound 都保留各自 theorem
hypotheses；它们没有被组合到一个 production TPC-18 pair 上。TPC-93 的
weighted sign/coefficient reassembly 只在 physical squarefree 与
target-primitive support 上有效。generic hard remainder、
square-root return、full-block 和 endpoint reassembly 仍分别为
uncontrolled 或 unsupplied。

精确 first missing 是：

```text
SOURCE_LOCKED_POST_TTSTAR_ORDERED_PAIR_REGISTRY_WITH_COMPLETE_PAIR_COEFFICIENT_AND_GLOBAL_NORMALIZATION
```

其两个不可省略的 subgates 仍为：

```text
PAIR_NATIVE_POST_TTSTAR_ACTUAL_REGISTRY_WITH_FULL_LITERAL_SCOPE_AND_COEFFICIENT
TPC18_PAIR_TO_TPC93_RETAINED_SOURCE_ATOM_THEOREM_CROSSWALK
```

### 13.3 machine certificate、exploit review 与 PDF QA

active release 含 16 个文件、3 个 exact schemas、13 个 manifest pins、
17 个 source locks、2 个 `L0` fixtures、17 行 loss ledger 与 23 个
gates。独立 checker 不导入 builder 或 materializer，并执行：

```text
active-schema mutations = 12
regenerated-schema semantic mutations = 37
strict bool/int mutations = 6
```

额外 coordinated exploit review 对 regenerated-schema payload
39/39、source rebind 4/4、audit 11/11、L0 7/7、manifest 7/7 全部
fail closed；没有残留的 schema-only 绕过。builder、materializer 与
independent checker 均通过；三者的 `python -O` 路径均按设计 fail
closed。TPC-18/25/32/93/143/174/179/194/204 的相关回归均通过，且没有
改写其 active artifacts。

稳定 PDF 为 4 页 A4；逐页视觉核查、字体嵌入、页旋转、加密、表单与
构建 warning 检查均通过。其 SHA-256 为：

```text
b3596e207943132ad48e6a17cfd107421f02b521bc02f617615c860816a1dc1e
```

### 13.4 当前 gates、开放父节点与停止边界

```text
PAIR_NATIVE_FORMULA_GATE = PASS
ACTIVE_PRODUCTION_PAIR_OCCURRENCE = NOT_TESTABLE
FULL_LITERAL_PAIR_COEFFICIENT_MATERIALIZATION = NOT_TESTABLE
SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK = FAIL
NU_X_NORMALIZED_RETURN_TO_H1 = FAIL
H1_E_REPAIR = FAIL

PAIR_NATIVE_ARCHITECTURE_REROUTE_CANDIDATE = OPEN
PAIR_NATIVE_PRODUCTION_REOPEN_TRIGGER = FAIL
PAIR_NATIVE_STRUCTURAL_REOPEN_TRIGGER = FAIL
pair_native_mathematical_reopen = false
```

继续保持以下 cells 为 `STOP_SCOPED`：

```text
TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1
TPC204_DECLARED_PLAUSIBLE_PRODUCTION_CROSSWALK_CORPUS_V1
TPC18_25_32_93_194_SINGLE_CUT_OCCURRENCE_COMPOSITE_V1
TPC18_TPC93_POST_TTSTAR_PAIR_DIRECT_COMPOSITION_V1
```

这不是对 pair-native architecture 的全局关闭。active support `A` 与
canonical/minimal representation `M` 仍是独立 `NOT_TESTABLE` roots；
两个 O161 pointwise parents、H1 architecture 与 global architecture
保持 `OPEN`。fixed-atom credit 为 0，strict endpoint `1/400` 为
`UNPAID`，`L2=NONE`。该历史块此前的 TPC-206 未授权状态现由页首和
第 14 节取代。

## 14. TPC-206 的精确有限结论

持续工作流授权下，本篇实际形成的有限定理范围仅为：

```text
FINITE_SELECTED_LINEAGE_13_OF_42_PROJECTION_AND_FIRST_MISSING_D_THEOREM
```

它的精确分类、定理状态和裁决是：

```text
classification
  = PAIR_NATIVE_SELECTED_LINEAGE_PROJECTION_L1
theorem_status
  = PROVED_SELECTED_SOURCE_LOCKED_13_OF_42_PROJECTION_AND_FIRST_MISSING_D_L1
verdict
  = SELECTED_SOURCE_LOCKED_13_OF_42_PAIR_REGISTRY_PROJECTION_CERTIFIED_NOT_REOPENED
```

### 14.1 selected graph 与 13/42 closure

选定 ordered pair 为：

```text
alpha = (103,1)
gamma = (107,1)
j = 5
X = 512
h0 = 2
```

显式 `DECLARED_TPC206_SELECTED_103_107_LINEAGE_GRAPH_V1` 由 6 个
source records、4 个 locked typed derivation nodes 和 12 条 dependency
edges 构成。按 TPC-205 的 42-field contract，它精确物化：

```text
X, h0, delta, R, V, D0, L, K,
alpha, gamma, j, N_alpha(j), N_gamma(j)
```

所以：

```text
materialized fields = 13
missing fields = 29
first missing field = D
first missing one-based index = 9
full completions inside the explicit selected graph = 0
```

29 个缺口分为 8 个 identity/packet fields、5 个 ordered-pair fields、
12 个 source/child fields 和 4 个 normalization fields。父级 first
missing 仍是：

```text
SOURCE_LOCKED_POST_TTSTAR_ORDERED_PAIR_REGISTRY_WITH_COMPLETE_PAIR_COEFFICIENT_AND_GLOBAL_NORMALIZATION
```

selected graph 内更细的 first missing semantic 是：

```text
SOURCE_LOCKED_TPC18_OPENED_D_PACKET_LINEAGE_FOR_SELECTED_ORDERED_PAIR
```

上述 `0` 和 first missing 只对显式 selected graph 成立。TPC-206 没有
审核整个仓库中的所有潜在 join，因此：

```text
corpus-wide maximum materialized fields = null
corpus-wide full-join count = null
CORPUS_WIDE_MAXIMALITY = NOT_TESTABLE
```

TPC-32/TPC-93 的独立 `L0` fixture 在自己的谱系里暴露 14 个 contract
slots；它不能拼接进 selected 103/107 graph，也直接排除了把 13 误读成
corpus-wide maximum。

### 14.2 source chain 与符号防火墙

六条选定 source records 由 TPC-133 的两行，经 TPC-134 path rows，
再到 TPC-136 cut rows；两条 cut 都是
`FRONTIER_UNMAPPED/NO_TAIL_ROOM`。manifest 给出的
`delta=1/4` 是在 `X=512` 上、通过 866-row JSONL certificate 锁定的
chosen-manifest provenance lift；它不是从单行唯一恢复的参数，也不是
cross-scale packet schedule。

必须保持三个不可改写的 typed firewalls：

```text
Q_133 = floor(512^(1/4)) = 4  ->  R_18 = 4
Q_18 = L D                    ->  missing

native divisor d = 1          != opened dyadic scale D
native row index k = 5=d*j    != dyadic block scale K = 8
```

其中 `L=64`、`K=8`，两条 target values 为 517 和 537。
`pair_record_id`、edge instance ID 与 target occurrence ID 均仍为
`null`。这个 projection ID 是非 production 的独立标识，不得伪装成
actual pair registry occurrence。

### 14.3 gate、STOP_SCOPED 与开放架构

TPC-206 没有证明 active production occurrence、pair-to-`omega`
crosswalk、global normalization 或 H1-E repair。当前边界为：

```text
ACTIVE_PRODUCTION_PAIR_OCCURRENCE = NOT_TESTABLE
CORPUS_WIDE_MAXIMALITY = NOT_TESTABLE
SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK = FAIL
GLOBAL_NORMALIZATION_RETURN = FAIL
H1_E_REPAIR = FAIL
pair_native_mathematical_reopen = false
```

新增 cell：

```text
DECLARED_TPC206_SELECTED_103_107_LINEAGE_GRAPH_V1=STOP_SCOPED
```

TPC193 V1、TPC204 V1、singleton-cut composite 与
TPC18/TPC93 direct-composition 四个旧 cells 继续 `STOP_SCOPED`。
这不是 pair-native architecture 的全局关闭。pair-native reroute、
两个 O161 pointwise parents、H1 architecture 与 global architecture
保持 `OPEN`；fixed-atom credit 为 0，strict endpoint `1/400` 为
`UNPAID`，`L2=NONE`。

### 14.4 certificate、exploit review 与 PDF QA

active release 含 14 个文件、2 个 exact schemas、11 个 manifest pins
和 29 个 source locks。冻结 archive closure 为 34 refs、28 tips、
12,203 个 Git objects；严格 RFC-8259 `.json` 共有 1,707 个可解析文件
和 17 个因 `NaN`/`Infinity` 被拒文件。该 archive census 只作
reopen-trigger context，不是 JSONL/TeX semantic census，也不支持
corpus-wide maximality。

独立 checker 不导入 builder 或 materializer。12 个 base、52 个
semantic、12 个 strict bool/int mutation rows，共 76 行全部 fail
closed；针对 coordinated payload/schema/audit rewrite 的复测为
`accepted=0, rejected=76`。manifest 的 11/11 bytes 与 SHA-256 新鲜，
但它只是 repository-review pin，不是外部签名。三个正常 `--check`
均通过，三个 `python -O` 入口均按设计非零失败。

稳定 PDF 为 4 页 A4，逐页视觉核查、字体嵌入和构建 warning 检查通过；
SHA-256 为：

```text
e6a3ee6df0492daa2aae86de47040e8b0d5f8c75a7abc91208601f945d3bb082
```

## 15. 2026-07-31 的三项不编号 reopen-trigger 审计

### 15.1 selected 103/107 opened-`D` attachment

执行：

```text
PAIR_NATIVE_SELECTED_LINEAGE_OPENED_D_ATTACHMENT_FEASIBILITY_AUDIT
```

八条 selected child paths 恰落在四个共同 blocks
`(jL,jK)=(6,2),(6,3),(7,2),(7,3)` 的两侧。四条为 `K_TOO_LOW`，
四条为 `NO_TAIL_ROOM`；八条 TPC-136 cut 全是
`FRONTIER_UNMAPPED`。TPC-143 的 actual map edges 为 0，
TPC-153 的 actual completion 全为 `NOT_PRESENT`，TPC-154 的
theorem-backed actual provenance 为 0。reachable-history 没有隐藏的
selected opened-`D` record 或 joint packet locator。

因此八个 attachment 字段仍全部缺失：

```text
D, J, Q, T, U0, G_X_row, packet_id, source_locator
```

closure 保持 `13/42`，首缺仍是 `D`、one-based index 9。若反事实地先
给出合法 attachment，TPC-18 support 只说明唯一相容 `D_open=1`，进而
`J=K/D=8`、`Q_18=LD=64`；这不是字段填充。尤其禁止
`d=1 -> D=1`、`D0=0 -> D=0`、`Q_133=4 -> Q_18=4`。

```text
classification =
  PAIR_NATIVE_SELECTED_LINEAGE_OPENED_D_ATTACHMENT_AUDIT_L1
theorem_status =
  PROVED_DECLARED_SELECTED_103_107_ALL_CHILD_NO_LEGAL_TPC18_OPENED_D_ATTACHMENT_L1
verdict =
  DECLARED_SELECTED_103_107_OPENED_D_ATTACHMENT_FAIL_CLOSED_STOP_SCOPED_NOT_REOPENED
```

### 15.2 literal `B_alpha B_gamma` coefficient expansion

执行：

```text
PAIR_NATIVE_LITERAL_TTSTAR_COEFFICIENT_EXPANSION_AUDIT
```

TPC-18 只允许抽象模板

```text
B_i(j)=omega_D(d_i) psi(ell_i/L) W(ell_i d_i j/X)
       psi(d_i j/K) xi(d_i,j)
```

以及外部的两个 `mu`、两个 `log ell`、两个 `r_R(N)` 因子。它没有冻结
selected/common-`T_D` packet、`omega_D` partition member、cutoff function
instances 或 joint mask。TPC-25 也只给函数类型族。TPC-133 的两条
single-row AST 属于另一 TPC-15 packet；TPC-134 的
`tpc134-exp-bump-orbit-normalization-v1` 只是 block-compiler edge
multiplier。把两条 AST 相乘、按函数名合并或把 edge multiplier 重命名
为 TPC-18 `B_i` 都不是 theorem-backed lineage edge。

第一项 literal 缺失为：

```text
OPENED_D_PARTITION_MEMBER_SOURCE_ID + D + omega_D(d_alpha)
```

其后还缺 gamma 侧、source cutoff、`W` crosswalk、`k` cutoff、`xi`、
joint mask/locator 与 nonzero status。故：

```text
theorem_status =
  ABSTRACT_TPC18_ORDERED_PAIR_B_ALIAS_EXPANSION_TEMPLATE_ONLY_L1
verdict =
  SELECTED_103_107_LITERAL_PAIR_COEFFICIENT_CROSSWALK_FAIL_CLOSED_NOT_REOPENED
FULL_LITERAL_PAIR_COEFFICIENT_MATERIALIZATION = NOT_TESTABLE
```

closure 仍为 `13/42`，首缺仍为 `D`。

### 15.3 O161 bad-endpoint named-atom shadow increment

执行：

```text
O161_BAD_ENDPOINT_NAMED_ATOM_SHADOW_INCREMENT_THEOREM_AUDIT
```

合法的 local-increment reduction 已冻结。令
`J=ceil(A log_2 log X)`；对同一 actual packet 的每个 prescribed `T`
与每个 `N_j=T/2^j in E_X^star`，所需新 theorem 必须直接给出

```text
q=as,  t(z)=ad+qz,
c_z=mu(d+s z)mu(u+a z),  su-ad=2,

(q/N_j) |sum_{N_j<t(z)<=2N_j} c_z rho_star(z)|
  <= C X^(-sigma)
```

其中 named `rho_star`、actual active support、exact `(T,j)` schedule、
共同 `X/N/q` ranges、uniform `C`、positive `sigma`、normalization
attachment 和完整 physical-loss ledger 必须属于同一 source-locked
record。local `q/N_j` block 与 O161 cumulative `q/T` object 不同；唯一
合法桥是 TPC-159 exact telescoping，并在求和前乘
`N_j/T=2^(-j)`。

权威 gate-order 的首阻断是：

```text
PRESCRIBED_BAD_ENDPOINT_ATOM_HAS_NO_SOURCE_LOCKED_VALUE
```

TPC-180 仍有 0 条 value-bearing named-phase record 和 0 条 production
packet-coordinate row。即使反事实补齐 atom/schedule，第一项算术阻断
仍是：

```text
POINTWISE_NAMED_ATOM_Q_OVER_N_POSITIVE_X_POWER_LOCAL_INCREMENT
ON_SCHEDULED_E_X_STAR_ANCESTORS
```

TPC-149/TT26 恰只控制 `E_X^star` 外的 terminal block，并且只有
log-power saving；TPC-159 只在 dyadic shadow 外累积；TPC-167/169 是
phase `L2`；TPC-186 是代数 reduction；TPC-187 是 size-only
`STOP_SCOPED`。TPC-202 审核的 Menon 2026 source 仍分别平均 interval
origin 或 shifts。补充 primary screen 的 arXiv:2204.03754 只含单个
Möbius/nilsequence，arXiv:2506.08787 是不同的多变量几何；均未提供
prescribed determinant-two two-Möbius increment。它们不被加入
TPC-193 V1 source universe。

六轴中只有 abstract actual-core carrier 通过；named atom、bad-shadow
endpoint、deterministic all-scale、positive fixed-`X` power 和 actual
active support 全部失败或 `NOT_TESTABLE`。good blocks 仍只有 log
saving，TPC-159 tail 为 `2^(-J)+q/T`；physical good/bad variation、
phase return 与 four-sign reconnection 均未知。

```text
formula_gate = PASS_L1_REDUCTION
theorem_production_gate = FAIL_CLOSED
verdict = O161_BAD_ENDPOINT_TRIGGER_FAIL_CLOSED_PARENT_OPEN_NOT_REOPENED
TPC207_TRIGGER = NO
```

### 15.4 archive 与 checker exploit review

O161 reachable-history 扫描覆盖 1,940 个 TPC text blobs、
72,608,764 bytes；57 个相关命中中没有正向 theorem-backed fixed-atom
increment 或 local-occurrence edge。四个 historical-only 命中都是旧
TPC-194/203 的 `NOT_TESTABLE/STOP_SCOPED` 版本。

审计发现 TPC-184/189 checker 原先以 Python `assert` 承担关键验证，
`python -O --check` 会错误放行，且只读取预填 mutation verdict。现已
改为显式 `ValueError` gate、实际加载 closed payload/audit schemas，
并现场执行各 8 个 mutation；正常与 `python -O -B` 四个入口均通过。
这只加固验证器，不改变两篇论文的 `TARGET_WELL_TYPED_OPEN` 数学裁决。

### 15.5 边界与下一路线

本轮没有 theorem-state reopen，因此没有创建 TPC-207。
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1` 与第 6 节全部精确
cells 继续 `STOP_SCOPED`。两个 O161 parents、pair-native reroute、
H1 architecture 与 global architecture 继续 `OPEN`；fixed-atom
credit 为 0，strict `1/400` 为 `UNPAID`，`L2=NONE`。

无需单独授权的下一项有限审计是：

```text
CORPUS_WIDE_SOURCE_BACKED_LOCAL_OCCURRENCE_EDGE_FAMILY_AUDIT
```

它只在 TPC-206 selected graph 之外寻找真正 theorem-backed 的 actual
local-occurrence edge family。archive key、formal/shadow row、
TPC-143/153 的零边或形式链、synthetic witness、旧 singleton-cut
`STOP_SCOPED` cell 的包装都不合格。只有同一 source-locked edge family
连同 exact occurrence、schedule、ranges、normalization 与 loss ledger
真实形成时，才可讨论 TPC-207。

## 16. 全仓 source-backed local-occurrence-edge family 审计

### 16.1 精确审计范围与同记录合同

本轮执行的不编号 gate 为：

```text
CORPUS_WIDE_SOURCE_BACKED_LOCAL_OCCURRENCE_EDGE_FAMILY_AUDIT
```

冻结 paper corpus 的快照为：

```text
023ccb5959e35b96673117b76add3dcbc3987aca
```

该快照的 `papers/` 恰有 TPC-1--206 各一目录、各一 `main.tex` 与
`README.md`，无缺号或重号。审计同时覆盖所有 refs 可达的、路径以
`papers/tpc-` 开头且扩展名属于
`.py/.json/.jsonl/.md/.tex/.csv` 的 distinct blobs：

```text
reachable blobs = 1940
reachable bytes = 72619961
blob OIDs present at current HEAD = 1917
historical-only blob OIDs = 23
```

这是一项 finite lexical + typed-contract + semantic-candidate audit，
不是所有数学表述、所有外部文献或所有未来 source universe 的
nonexistence theorem。历史草稿也不因仍可达而自动取得 active production
theorem 身份；扫描历史只用于排除“已有但被当前树漏掉”的正向 candidate。

TPC-173 的最小 H1 edge 合同仍要求同一 source-locked record 同时给出：

```text
source path + canonical hash
resolving theorem locator
resolving formula locator
nonempty derivation AST
literal actual-local-occurrence-edge conclusion
five-field production cut address (ell,k,native_d,jL,jK)
exact nonzero rational edge weight
fixed h0=2 lineage
physical-normalization lineage
```

本轮 reopen gate 还逐项要求 exact actual occurrence identity、
packet/scale schedule、共同 ranges、具有公式语义的 normalization，以及
完整且不重复的 physical-loss ledger。archive key 只能作地址；
formal/shadow row、relation-type 名称、synthetic witness、空 family 与
跨 lineage 数值相等都不能补字段。

### 16.2 精确 census 与 near-candidate 排除

TPC-173 已冻结的 TPC-133--172 四十篇保持：

```text
MAPPED_DISQUALIFIED files = 30
REVIEWED_NO_CANDIDATE files = 10
NOT_MAPPED_YET files = 0
QUALIFYING files = 0
mapped claim records = 32
qualifying claim records = 0
```

其余 166 篇按互斥 source 层分为：

```text
TPC-1--132 pre-cut legacy = 132
TPC-173--179 H1 inventory/schema/extraction layer = 7
TPC-180--193 phase/fixed-atom/direct layer = 14
TPC-194--204 direct/reduction/barrier/audit layer = 11
TPC-205 pair-native interface = 1
TPC-206 selected projection = 1
```

pre-cut legacy 没有在同一 record 中形成具有 TPC-164/TPC-174 语义的
五字段 production source-cut address；phase/direct 对象不是 linear
cut-to-occurrence relation；TPC-205 的
`LINEAR_CUT_TO_OCCURRENCE_EDGE` 只是 relation type，production rows
为 0；TPC-206 的 selected graph 按本 gate 排除，其 nonselected
comparison fixture 仍是 `DERIVED_L0_ONLY` 且
`production_occurrence=false`。

对当前 HEAD 中 TPC-1--206 的 tracked、非-schema `.json/.jsonl`
再作结构化 census：

```text
files = 228
parse errors = 0
audited raw key instances = 26947 in 22 files
nonempty signal instances = 9001 in 7 files
generic occurrence_id instances = 26
physical_occurrence_id instances = 8973
actual_occurrence_id instances = 2
other positive/true/nonempty edge signals = 0
```

全部非空 signal 都被其自身 provenance 排除：

- TPC-141 的 14 个 generic `occurrence_id` 是 integration/ledger stage
  tokens，不是 physical actual edges；
- TPC-143 的 2,988 条 obligations 全部满足
  `actual_map_edges=[]`；TPC-145 的 `actual_occurrence_edges` 与
  `actual_stage_edges` 也都为空；TPC-163 的 13 类 production
  crosswalk coverage 全为 0，`theorem_backed_edge_count=0`；
- TPC-153 的 2,988 条 shadow rows 的 `actual_occurrence_id` 全为
  `null`；其两条最接近 claim 虽有 weight \(1\)、`h0=2` 与 `nu_X`
  lineage，但 theorem conclusion 仍只是 shadow；
- TPC-154 有 2,989 条 completion records、8,967 条 formal edge rows
  与 8,967 个唯一 `FORMAL_ONLY` physical IDs；其中 8,964 条来自当前
  production archive 的自由形式补全、3 条来自 synthetic policy
  regression，且 8,967 条全部显式满足
  `theorem_backed_actual_provenance=false`；
- TPC-155 只有 3 条 `SYNTHETIC_L0_ONLY` occurrence rows；
- TPC-174 只有 2 条 synthetic edges 与两个
  `synthetic-occurrence-{a,b}` IDs，source path/hash、theorem locator
  与 formula locator 均为空；
- TPC-205 的 ID 字符串是接口语义占位，production pair records 为 0；
  TPC-206 的 pair/edge/target occurrence IDs 为 `null`。

reachable-history 中没有 historical-only occurrence-ID-field blob，也
没有 historical-only positive candidate。严格 same-record screen 在
current 与 historical-only 两侧均为 0。

独立 exploit review 对 TPC-143/153/154/155/173/174/175 的七个
`python -O -B --check` 入口全部复核通过，未发现 `assert` 型优化绕过；
TPC-155/174 的关键 integer/fraction 路径也严格排除 bool-as-int。
同时保留以下信任边界：TPC-173 的 qualification flags 未被 schema
强制为 strict bool，TPC-174 不执行外部 theorem truth 或完整
source-label resolution，TPC-175 的 standalone zero-count validator
存在 `False == 0` 型混淆。deterministic rebuild 可阻止 artifact-only
篡改，不能把 coordinated producer/schema/source rewrite 变成外部定理
证明。因此本轮裁决建立在独立 raw census 与逐 source claim 审核上，
不把这些 checker 单独当作 theorem evidence。

因此同记录 gate ledger 为：

```text
source theorem with literal actual-edge conclusion = 0
production actual-occurrence identities = 0
exact nonzero edge/conservation on an actual carrier = 0
same-record packet schedule = 0
same-record ranges = 0
same-record physical normalization = 0
same-record complete physical-loss ledger = 0
complete qualifying H1 local-edge records = 0
```

### 16.3 裁决、停止边界与开放父节点

首致命阻断为：

```text
SOURCE_LOCKED_THEOREM_WITH_ACTUAL_LOCAL_OCCURRENCE_EDGE_CONCLUSION
  = ABSENT
```

它早于 occurrence ID、edge weight、schedule、ranges、normalization 与
loss ledger。故：

```text
classification =
  CORPUS_WIDE_SOURCE_BACKED_LOCAL_OCCURRENCE_EDGE_FAMILY_AUDIT_L1

theorem_status =
  PROVED_DECLARED_TPC1_206_AND_REACHABLE_HISTORY_ZERO_QUALIFYING
  H1_SOURCE_BACKED_LOCAL_OCCURRENCE_EDGE_RECORDS_L1_SCOPED

verdict =
  DECLARED_TPC1_206_REACHABLE_LOCAL_EDGE_CORPUS_V2
  FAIL_CLOSED_STOP_SCOPED_NOT_REOPENED

H1.source_backed_local_occurrence_edge_family = NOT_TESTABLE
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

新增且仅新增：

```text
DECLARED_TPC1_206_REACHABLE_LOCAL_OCCURRENCE_EDGE_SOURCE_CORPUS_V2
  = STOP_SCOPED
```

该 cell 只停止从上述 snapshot 与可达历史重新包装出 production H1 edge；
它不是数学不存在性定理，不关闭新增 source theorem、外部新增 primary
source 或独立 architecture reroute。第 6 节全部旧 cells（尤其
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`）继续精确
`STOP_SCOPED`。

两个 O161 parents、pair-native reroute、H1 architecture 与 global
architecture 继续 `OPEN`。active support 与 canonical/minimal
representation 是 actual carrier 之后的独立 roots；在 carrier 为空时
优先审它们只会继续得到 vacuous `NOT_TESTABLE`。fixed-atom credit 为 0，
strict `1/400` 为 `UNPAID`，`L2=NONE`。

### 16.4 下一有限路线

最直接触碰首缺、且不再重复空 corpus scan 的下一关选为：

```text
ONE_PACKET_SOURCE_FORWARD_PRECUT_TO_ACTUAL_OCCURRENCE_LINEAGE_CONSTRUCTION_GATE
```

它必须选一个 source-locked named upstream physical occurrence，沿正向
map 推到一个具体 TPC-136 cut；禁止从已经丢字段的 cut archive 逆猜
occurrence。一次通过必须在同一 source lock 下同时形成：

```text
named actual physical occurrence ID
literal five-field production cut address
exact nonzero edge weight and per-cut conservation
fixed h0=2
exact packet schedule and parameter ranges
physical normalization with formula semantics
complete nonduplicated loss ledger
```

若该 gate 通过，它会直接产生第一条 production TPC-174 witness，届时
才允许讨论 TPC-207。若首步即证明当前语料没有可选的 named upstream
physical occurrence，则 fail closed 并转入仍开放的备选有限路线：

```text
UNNUMBERED_CORPUS_WIDE_NONSELECTED_PAIR_NATIVE_CONNECTED_LINEAGE_JOIN_CENSUS
```

备选路线只审 103/107 之外、同一 connected lineage 的 ordered row
pairs，禁止 external L0 donor 与 cross-lineage splice，并始终保持
pair reroute 与 H1 linear edge 类型分离。

## 17. one-packet source-forward 与 nonselected pair fallback 审计

### 17.1 冻结语料与 Gate 0 合同

本轮在 source snapshot

```text
3dd4fe67977380289f68dd644cf4d2dba60456b5
```

上先执行：

```text
ONE_PACKET_SOURCE_FORWARD_PRECUT_TO_ACTUAL_OCCURRENCE_LINEAGE_CONSTRUCTION_GATE
```

候选主语料、只按实际 theorem/interface 调用追踪的直接依赖，以及用于
冻结 actual-occurrence 类型边界的 contracts 分别为：

```text
U_main =
{TPC-18, 32, 93, 117, 119, 123, 124, 131, 133, 134, 135, 136}

U_dep =
{TPC-15, 16, 17, 25, 29, 30, 31, 33, 86, 92,
 105, 107, 114, 116, 118, 121, 122, 125, 132}

U_contract =
{TPC-143--146, 153--155, 163--165, 173--175}
```

这是当前仓库的有限 source audit，不是数学上的全局不存在性声明。
`U_main` 的 12 个目录共有 112 个被审 source blobs；所有 refs 可达历史
没有补出该语料的 historical-only positive version。17 个非-schema
JSON/JSONL 均可解析。

Gate 0 要求先选出一个 source-locked、named actual physical
occurrence，再沿已证正向 map 推到具体 TPC-136 cut。它禁止：

```text
native/archive/path ID -> occurrence ID 的解释性改名
block/cumulative conservation -> per-cut occurrence-fibre conservation
symbolic psi path multiplier -> rational local-occurrence edge weight
从 lossy cut archive 逆猜 source occurrence
```

逐 source 类的精确近邻为：

- TPC-18 有真实 symmetric tail block 与 opened-`d` 线性公式，但
  block/row summand 没有独立 actual physical occurrence ID，也没有到
  TPC-136 cut 的 theorem-backed edge；
- TPC-32 有 actual row coefficient、row-pair carrier 与 ranges，但对象是
  二次 pair/orbit，不是一个线性 cut occurrence；
- TPC-93 对另行 supplied 的
  `omega=(L/R,alpha,gamma,j,u)` 有 exact source-child inverse，却没有
  production instance ID、packet ID、到 TPC-136 cut 的 crosswalk，且
  未 source-lock 到 `h0=2`；
- TPC-117 只给 range/residual certificate format，growing `B,w` 与
  stable physical row IDs 未提供；
- TPC-119/123/124 分别缺 complete canonical leaf archive、actual growing
  stage tables 与 actual growing `G,C,z,B`；
- TPC-131 给 occurrence-token/no-double-charge contract，但 sample tokens
  只是 finite regression，`actual_complete_physical_registry=false`；
- TPC-133--136 给完整 native/archive 正向结构链，却没有 actual physical
  occurrence 类型或 ID。

因此两类近邻的关键交集严格为空：

```text
{source-backed actual physical semantics + independent occurrence ID}
intersection
{TPC-119 -> 133 -> 134 -> 135 -> 136 forward lineage}
= empty
```

### 17.2 最近 concrete cut 与八轴结果

当前 committed archive 的结构闭合精确为：

```text
TPC-133 native rows = 866
TPC-133 -> TPC-134 parent-hash joins = 2988 / 2988
TPC-134 paths = 2988
TPC-134 -> TPC-135 block-key coverage = 2988 / 2988 over 26 keys
TPC-134 -> TPC-136 path-ID + upstream-hash joins = 2988 / 2988
TPC-136 unique five-field cuts = 2988
TPC-136 -> actual occurrence bridges = 0
```

TPC-136 的 2,988 个 cuts 全部为 `FRONTIER_UNMAPPED`：

```text
NO_TAIL_ROOM = 1495
L_TOO_LOW = 1020
K_TOO_LOW = 473
```

四张 downstream maps 的 domain 都为空、各缺 2,988 rows，source status
全部 `NOT_TESTABLE`。最近的一条可执行正向链冻结为：

```text
X=512, h0=2, delta=1/4, Q=4, U=V=2
native tuple = (ell,k,d) = (3,171,1)
native_id = X=512|h0=2|ell=3|k=171|d=1
physical_normalization tag = nu_X

TPC-134 child = (jL,jK,D0,type) = (1,7,0,TAIL)
TPC-136 cut kappa = (ell,k,native_d,jL,jK) = (3,171,1,1,7)
TPC-135 reason = L_TOO_LOW
TPC-136 terminal = FRONTIER_UNMAPPED
soft_theorem_source = null
native coefficient nonzero status = UNDECIDED
```

其 native coefficient 与 exact symbolic path term 为：

```text
c_X(3,171,1)
  = -Lambda(3) r_4(515) W(513/512)

path term
  = -Lambda(3) r_4(515) W(513/512)
      psi(3/2) psi(171/128)
```

`psi(3/2)psi(171/128)` 是 exact positive symbolic path multiplier，
并参与
`sum_(children of one native column) m = 1`。它不是 TPC-174 所需的
exact rational occurrence-edge `lambda`，而 native-column conservation
也不是 `sum_(actual occurrences over one cut) lambda = 1`。

八轴 ledger 为：

```text
named actual physical occurrence ID = FAIL
distinct local edge ID = FAIL
literal five-field cut = PASS
exact nonzero occurrence-edge / per-cut conservation = FAIL
h0=2 lineage = PARTIAL: native/cut only
packet schedule and ranges = PARTIAL: no same-lock physical occurrence
formula-semantic physical normalization = FAIL: nu_X is only a copied tag
complete nonduplicated physical-loss ledger = FAIL
```

首致命缺口因此是：

```text
SOURCE_LOCKED_NAMED_ACTUAL_PHYSICAL_OCCURRENCE_RECORD
  IN_THE_TPC119_TO_TPC136_FORWARD_LINEAGE
  = ABSENT
```

故：

```text
ONE_PACKET_SOURCE_FORWARD_PRECUT_TO_ACTUAL_OCCURRENCE_LINEAGE_GATE0
  = FAIL_CLOSED
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

### 17.3 自动 fallback：nonselected ordered-pair census

按第 16.4 节的预定 fallback，本轮随即执行：

```text
UNNUMBERED_CORPUS_WIDE_NONSELECTED_PAIR_NATIVE_CONNECTED_LINEAGE_JOIN_CENSUS
```

pair identity 定义为同一完整 packet scope 下的 ordered
`(alpha,gamma,j)`，其中 `j=k_alpha/d_alpha=k_gamma/d_gamma`；pair-block
instance 再附共同 `(jL,jK,D0=0)`。两条 row 都必须经 parent hash 与
upstream hash 正向 join 到同一 TAIL/FUM block。TPC-205 已冻结
`ordered_pair_quotient=FORBIDDEN`，故只排 exact selected orientation

```text
alpha=(103,1), gamma=(107,1), j=5
```

的全部 4 个共同 block instances；反向 `107 -> 103` 是独立
nonselected pair，必须保留。精确 census 为：

```text
native rows = 866
distinct j groups = 202
groups with at least two rows = 101
all ordered same-j row pairs before common-block screen = 15030

raw same-lineage pair identities after selected-orientation exclusion = 13227
raw common pair-block instances = 31868
raw instance reasons:
  NO_TAIL_ROOM = 14406
  K_TOO_LOW = 16666
  L_TOO_LOW = 796
```

严格 TPC-18 geometry pool 只取 `NO_TAIL_ROOM`：这里 `L>2R` 与
`K>2V` 已通过。`NO_TAIL_ROOM` 是 TPC-135 对 prefix cutoff `D0` 的
分类：当 `V=2` 时不存在正整数 `D0` 满足 `2D0<V`，故 archive 取
`D0=0`。它不是 TPC-18 uppercase opened dyadic `D`，也不证明
uppercase `D` 不存在。TPC-205 contract-order 的独立首缺仍是没有
source-locked locator 的 uppercase `D`。该 pool 为：

```text
strict ordered pair identities = 7157
strict pair-block instances = 14406
identity block multiplicity:
  1 block = 2780
  2 blocks = 2941
  4 blocks = 1436
```

全部 14,406 个 instances 并列满足 TPC-205 的 13/42 maximal closure：

```text
X, h0, delta, R, V, D0, L, K,
alpha, gamma, j, N_alpha, N_gamma
```

`R` 只按 TPC-206 已冻结的 typed `Q_133 -> R_18` alias 填入；不得把
`Q_133` 再偷渡为 `Q_18`。精确 first missing 是 field #9：

```text
D
blocker =
NO_SOURCE_LOCKED_TPC18_OPENED_D_SLICE_LOCATOR
native d is not opened uppercase D
```

因此：

```text
13/42 maximizer instances = 14406
13/42 maximizer identities = 7157
full 42-field completions = 0
pair/edge/target occurrence IDs = 0
production occurrences = 0
```

其中至少一侧 `Lambda(ell)` 已确定为零的 instances 有 13,142；余下
1,264 instances / 669 identities 也只表示两侧 Lambda leaves
potentially nonzero，仍缺 `W/r_R` 取值、joint mask、完整 coefficient
nonzero、pair occurrence 与 normalization return，不能提升为 active
candidate。determinant-two 子池有 2,054 instances / 968 identities；
再限两侧 Lambda leaves potentially nonzero 后只有 124 instances /
106 identities。

审计 ID 的 canonical digests 为：

```text
strict instances:
  count = 14406
  bytes = 759518
  sha256 = ceb4c93791ce1f8a88d2d6ba4adb05dcdc19df045272e3c7a423184f32bcd116

strict identities:
  count = 7157
  bytes = 269967
  sha256 = 167dcd24b0fa7380651719e1792eb1461c51be4ecec474778e162b334106b166
```

ID 使用 UTF-8 字典序、LF join 并带末尾 LF；instance ID 为完整 pair
identity 再附 `jL,jK,D0`。此 digest 冻结 census，不把 formal row
投影变成 production theorem。

### 17.4 schema、checker 与最终裁决

目标 current/history 中这些非空 ID key 的计数全部为零：

```text
actual_occurrence_id
physical_occurrence_id
occurrence_id
packet_id
parent_id / canonical_parent_id
stage_id
group_id / physical_group_id
edge_id / edge_instance_id
```

TPC-131 仅有 6 个 generic finite-regression labels，且
`actual_complete_physical_registry=false`。TPC-133/134/136 schemas 是
archive-shape schemas；`additionalProperties=false` 能拒绝偷偷塞入
occurrence 字段，却不能证明 occurrence。TPC-134 的 symbolic
`edge_multiplier_ast` 也不是 TPC-174 rational occurrence-edge。
TPC-136 对未来 `PROVED` map 的 validator 不解析外部 theorem truth，
因此 source-label self-attestation 仍是独立 trust boundary；当前四图
仍为 empty/`NOT_TESTABLE`。

平台复核为：

```text
TPC-133 normal and python -O --check = PASS
TPC-133 -> 134 semantic joins = 2988 / 2988
TPC-134 -> 136 semantic joins = 2988 / 2988
TPC-134/135 raw-byte archived SHA checks on LF checkout = FAIL_EOL_PIN
TPC-136 archived hash-chain check = FAIL_FROM_UPSTREAM_EOL_PIN
git diff on old artifacts = EMPTY
```

旧 pins 恰好是把当前 LF 文本转为 CRLF 后的 SHA-256；这是
EOL-sensitive raw-byte portability pin，不是公式或逐记录语义 join
漂移。本轮没有修改旧证书，也不把 semantic match 说成当前机器
hash-chain fully reproducible。TPC-173--179、TPC-184、TPC-189、
TPC-205 与 TPC-206 的 required checks 均通过。snapshot 新增的
RH-323/324 分别是 affine Gaussian probability model 与 folded physical
kernel/affine-leg remainder；两者没有 TPC cut、occurrence、Mobius 或
determinant-two source theorem，类型上不能 reopen 本 gate。发布前
rebase 新增的 `a39c434` 只修改 RH-324 的 joint-density support 实现与
测试，也没有改动 TPC corpus 或上述 theorem-state。

本轮最终 verdicts 为：

```text
ONE_PACKET_SOURCE_FORWARD_PRECUT_TO_ACTUAL_OCCURRENCE_LINEAGE_GATE0
  = FAIL_CLOSED_STOP_SCOPED_NOT_REOPENED

NONSELECTED_TPC18_GEOMETRY_ORDERED_PAIR_LINEAGE_JOIN
  = PROVED_FINITE_CORPUS_MAXIMUM_13_OF_42
    FIRST_MISSING_D
    ZERO_FULL_COMPLETIONS
    ZERO_PRODUCTION_OCCURRENCES
    STOP_SCOPED_NOT_REOPENED

TPC207_TRIGGER = NO
TPC207_CREATED = false
```

新增且仅新增第 6 节的两个 cells。第 6 节全部旧 cells，尤其
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`，继续原样
`STOP_SCOPED`。两个 O161 parents、pair-native reroute、H1 与 global
architecture 继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为
`UNPAID`，`L2=NONE`。

### 17.5 下一有限路线

pair census 已把当前唯一最接近 source-side 首缺的有限池从 14,406
instances 收紧到 124 个 determinant-two、two-Lambda-potential
instances。下一关冻结为：

```text
ONE_POSITIVE_DETERMINANT_TWO_NONSELECTED_PAIR_OPENED_D_PACKET_ATTACHMENT_GATE
```

按“先取 positive determinant two、再最大化同 identity 的 strict common
block 数、再最小化尺度与 block”的稳定规则，唯一首选 diagnostic seed
冻结为：

```text
X=512, h0=2, delta=1/4, R=4, V=2
alpha=(17,1), gamma=(16,1), j=33
jL=4, jK=5, D0=0
L=16, K=32
N_alpha=563, N_gamma=530

h0(m_alpha-m_gamma) = 2(17-16) = +2
```

该 ordered identity 另有共同 strict block `(4,6,0)`；冻结 `(4,5,0)`
是上述稳定规则的结果。两侧 `Lambda(17)` 与 `Lambda(16)` 均确切非零，
但 `r_R/W/B`、joint mask 与完整 pair coefficient nonzero 仍未证明。
source locators 为：

```text
alpha row:
  TPC-133 JSONL line 372
  integrity db32fb3628ac124285e65c7f144d1c6000f73777df832b2fdf7bea24e002ab56
gamma row:
  TPC-133 JSONL line 357
  integrity 91cc9c344379273f3463fb25717fe159a2b26e7ed8b07ee6be684c4650ee48ad

alpha path/cut:
  TPC-134 line 1283
  integrity 33d4e8370fcc718efe6b97011e90c7306c4f3edd2d5201a915ddd4b02fbe3cce
  TPC-136 line 1283
  integrity 5a8fd7a715dd473f6f2deb15989425bc7773b7b8b069e24ef9d462ccdcfeb404
gamma path/cut:
  TPC-134 line 1251
  integrity e5d704f9971160e7ae4533caa7829102940524e51aec0cd2dcfae740106296e9
  TPC-136 line 1251
  integrity c3e613844749c161f79fc8673eb8bd67c5339f5d03f161c64be6247af5270769
```

两条链都是 `TAIL/FRONTIER_UNMAPPED/NO_TAIL_ROOM`，
`soft_theorem_source=null`。它们是两个独立 row/path/cut locators，不是
一条 source-locked post-TT-star joint pair locator。

下一 gate 必须在这条具体 nonselected ordered pair 上找到实际 source
theorem，把同一 source lock 的 uppercase opened `D` slice 附到两条
row；只有如此才能合法导出 `J=K/D` 与 `Q_18=LD`。禁止：

```text
native d -> opened D
Q_133 -> Q_18
selected 103/107 stopped-cell repackaging
external L0 donor
cross-lineage splice
potentially nonzero Lambda -> nonzero full coefficient
pair-native object -> H1 linear occurrence edge
```

若首个候选仍没有 theorem-backed `D` attachment，则 fail closed 并冻结
对应 declared candidate cell；不得为了编号而补 schema。只有 source
theorem 同时提供 uppercase `D`、joint packet/source locator、literal
determinant-two coefficient、actual pair occurrence、formula-semantic
normalization 与完整 loss ledger，才可能改变 theorem state并讨论
TPC-207。

## 18. positive determinant-two seed carrier 与 mask 审计

### 18.1 冻结 gate、snapshot 与 formal archive projection

本轮在 source snapshot

```text
0a0dd19d04fb168132f1227758f906aed62c32e5
```

上执行：

```text
ONE_POSITIVE_DETERMINANT_TWO_NONSELECTED_PAIR_OPENED_D_PACKET_ATTACHMENT_GATE
```

冻结 seed 为：

```text
X=512, h0=2, delta=1/4, R=4, V=2
alpha=(ell_alpha,d_alpha)=(17,1), k_alpha=33
gamma=(ell_gamma,d_gamma)=(16,1), k_gamma=33
j=33
(jL,jK,D0)=(4,5,0)
L=16, K=32
N_alpha=563, N_gamma=530
h0(m_alpha-m_gamma)=2(17-16)=+2
```

两条 TPC-133 -> 134 -> 136 archive chains 的 parent/upstream joins 全部
精确通过：

```text
alpha:
  TPC-133 line 372
  db32fb3628ac124285e65c7f144d1c6000f73777df832b2fdf7bea24e002ab56
  TPC-134 line 1283
  33d4e8370fcc718efe6b97011e90c7306c4f3edd2d5201a915ddd4b02fbe3cce
  TPC-136 line 1283
  5a8fd7a715dd473f6f2deb15989425bc7773b7b8b069e24ef9d462ccdcfeb404

gamma:
  TPC-133 line 357
  91cc9c344379273f3463fb25717fe159a2b26e7ed8b07ee6be684c4650ee48ad
  TPC-134 line 1251
  e5d704f9971160e7ae4533caa7829102940524e51aec0cd2dcfae740106296e9
  TPC-136 line 1251
  c3e613844749c161f79fc8673eb8bd67c5339f5d03f161c64be6247af5270769
```

因此 TPC-205 的 field-order archive projection 仍形式 materialize
恰好 13/42：

```text
X, h0, delta, R, V, D0, L, K,
alpha, gamma, j, N_alpha, N_gamma
```

其 contract-order first missing 仍是 field #9 uppercase `D`。这个
`13/42` 只是 source-locked row/path/cut partial projection，不先验保证
该 pair 属于 TPC-18 的求和 carrier。

### 18.2 Gate prerequisite 首先失败：`ell=16` 不是 prime source

TPC-133 的 generator 有意枚举 support-envelope native tuples；其
coefficient AST 使用 `Lambda(ell)`，不要求 `ell` 本身为 prime。因此
`ell=16=2^4` 是合法 TPC-133 native record，并且

```text
Lambda(16)=log 2 != 0.
```

但 TPC-18 在任何 quadraticization 之前先执行 prime-source reduction。
精确 source locators 为：

```text
TPC-18 tail-interface.tex:61--94
  source prime powers are removed before either quadraticization
  lambda_ell = (log ell) 1_(ell prime) psi(ell/L)
  sha256 = 5f50b44fde7e672b28aeb45b1b53e95f90c26bb8d35052081fa3a7e419712389

TPC-18 opened-d-dispersion.tex:17--56
  T_D, J=K/D, Q=LD
  prime and support restrictions remain understood
  sha256 = 36249c8baa2495034acabeb0ba7d5a5f665f2d536b605e9691e2e420e399f1f8

TPC-25 provenance.tex:22--55
  actual row family requires ell in [L/2,2L] prime
  sha256 = 21382acf28d8fc3d3cff499cd767075206ba9e2d24913e95414138b4317f0f00

TPC-32 physical-matched-shell.tex:42--48
  physical opened rows again require ell_alpha prime
  sha256 = b2c3b2b0312db64af5b3151402be929c1671429c1376fe24454a78b4c60d90bd
```

TPC-17 也在 assembled-prefix proof 中整体移除
`ell=p^a, a>=2` 后才 restriction to primes。TPC-93 只 export 另行
supplied、retained 的同一 TPC-32 source atom；其 source-child bijection
不会恢复被 prime-source reduction 移除的 row。

所以本 seed 上：

```text
lambda_17 = log 17 * psi(17/L)
lambda_16 = 0
```

archive determinant `+2` 是正确整数恒等式，却不能产生一个非零 TPC-18
pair term。Gate prerequisite ledger 为：

```text
alpha TPC-133 native membership = PASS
gamma TPC-133 native membership = PASS
alpha TPC-18 prime-source membership = PASS
gamma TPC-18 prime-source membership = FAIL
archive determinant = PASS:+2
joint TPC-18 ordered-pair carrier = FAIL
TPC-18 pair coefficient = ZERO_FROM_LAMBDA_16
```

首致命缺口因此早于 uppercase `D`：

```text
TPC18_PRIME_SOURCE_CARRIER_MEMBERSHIP
  (gamma=(ell=16,d=1))
  = FAIL
```

`Lambda(ell)!=0` 只说明 `ell` 是 prime power，不能解释为
`ell is prime`。这正是原 124-instance candidate filter 必须补上的
类型防火墙。

### 18.3 `D0`/`D`、42-field ledger 与 schema 防偷渡

TPC-135 的 `NO_TAIL_ROOM` 是 prefix-cutoff 判据：

```text
V=2
no positive integer D0 satisfies 2D0<V
therefore canonical D0=0
```

它与 TPC-18 uppercase opened dyadic `D` 不同。对原 seed 的
`d_alpha=d_gamma=1`，公式 support 与 `D=1` 相容，但没有 source-backed
named slice locator；且 carrier 已在 prime-source prerequisite 失败。
故不得把 `NO_TAIL_ROOM` 说成 uppercase `D` 不存在，也不得用 `D0=0`
填写 `D`。

两种 first-missing 必须分开：

```text
formal 42-field contract-order first missing = D at index 9
gate prerequisite first fatal = gamma prime-source membership
```

在当前 exact seed/block selector 下，TPC-133/134/136/143/153/154
各只有两条 single-side records，共 12 条；同时含两个 native IDs 的
joint record 为 0。以下 production fields 的 source-backed count 也
全部为 0：

```text
uppercase D
J
Q_18
packet_id
joint source_locator
pair_record_id
edge_instance_id
target_occurrence_id
```

TPC-143 的 `actual_map_edges=[]`、status 为 `NOT_TESTABLE`；TPC-153 的
`actual_occurrence_id=null` 且 `is_actual_occurrence=false`；TPC-154
匹配到的 physical IDs、formal edge IDs 与 ledger tokens 全部
`FORMAL_ONLY`，并满足
`theorem_backed_actual_provenance=false`。它们不能补 actual pair 或
loss ledger。`Q=4` 仍只是 TPC-133 `r_Q` 的 finite-model scope，并非
`Q_18=LD`；`nu_X` 仍只是 lineage label，不是 scalar normalization。

TPC-205/206 的 strict wrappers 按 exact type identity 检查，并已有
bool/int 与 semantic mutations，能拒绝：

```text
native d -> uppercase D
Q_133 -> Q_18
native/path/cut ID -> pair or occurrence ID
formal/shadow -> actual
nu_X label -> scalar normalization
one normalization -> four normalization fields
```

TPC-133/134/136 的遗留内层 validator 仍有 `isinstance`/equality
bool-int trust boundary；TPC-136 future map validator 也不验证外部
theorem truth，只检查 `PROVED` label、非空 source 与 total domain。
当前固定 artifacts 由 integrity/source pins 与 TPC-205/206 strict
wrappers 保护，且四张 downstream maps 仍为空、`NOT_TESTABLE`。因此
不能用 schema self-attestation 把本 seed 从 13/42 提升到 14/42。

### 18.4 新增 RH sources 与历史 screen

发布基线之后新增：

```text
01e56b9  RH-325 moving-order Duhamel criterion
437d318  RH-326 parity-renormalized alias identity
0a0dd19  RH-326 certification-boundary tightening
```

RH-325 的对象是 nonautonomous Markov path law 与 abstract trace
Duhamel；其 `mu(dx0)` 是 probability entrance measure，不是 Möbius
function。RH-326 的对象是 Hardy-scaled noisy Markov
trace/counterloop first-alias packet；其中 lowercase
`d_(sigma,k)` 是 clearance ratio，不是 TPC divisor scale。

两篇对本 gate 的逐轴结果全部为 `ABSENT/TYPE_MISMATCH`：

```text
uppercase opened D
J=K/D and Q_18=LD
joint post-TT-star pair locator
literal determinant-two Möbius coefficient
actual pair occurrence
TPC packet schedule/ranges
TPC formula-semantic normalization
complete TPC physical-loss ledger
```

RH-326 还显式保持 local probability-to-raw-trace、neighboring shell、
joint trace law、full-trace replacement 与 second physical leg 为
false/open；`0a0dd19` 把 decimal no-go 收紧为 conditional，普通浮点值
不是 interval certificate。`1580823..0a0dd19` 没有 `tpc-*` 或
`TPC_HANDOFF.md` source 改动，也没有新的 TPC theorem source。

### 18.5 both-prime 修正池与 primitive-mask obstruction

把先前 124 instances / 106 identities 的
both-`Lambda`-prime-power-potential pool 改为真正的 source-prime
筛选后：

```text
both ell prime, |det|=2:
  28 instances / 28 identities

both ell prime, det=+2:
  14 instances / 14 identities
```

对 `h0=2` 与 `ell_alpha,ell_gamma>2` prime，两个 source primes 都是
奇数。`det=+2` 等价于

```text
ell_alpha d_alpha - ell_gamma d_gamma = 1.
```

故 `d_alpha,d_gamma` 奇偶性相反。当前 `V=2` 且 `d<=V`，所以每个
positive instance 恰有一个 divisor row 等于 2。于是对 TPC-18/TPC-25
的 primitive mask：

```text
gcd(d*j,h0)=1
```

至少一侧恒失败。14/14 positive instances 的 joint primitive-mask
value 都为 0。canonical ID digest 为：

```text
count = 14
bytes = 963
sha256 = b366115151f5609275ab2483100e968ed4e8b78a67f16f1da0393a3f2fe0d8b5
primitive true = 0
primitive false = 14
```

该结论只停止当前 finite corpus 的 primitive-mask route。TPC-18
opened-`D` 公式也允许 formal constant mask，但 constant mask 不能仅因
“admissible”就改名为 actual physical packet；nonprimitive
`s=(k,h0)=2` endpoint route也是另一 theorem object。

按“positive determinant two、both prime、最小 scale/block/j”的稳定规则，
下一 diagnostic seed 为：

```text
X=512, h0=2, R=4, V=2
alpha=(ell=23,d=1,k=24)
gamma=(ell=11,d=2,k=48)
j=24
(jL,jK,D0)=(4,5,0)
L=16, K=32
m_alpha=23, m_gamma=22
N_alpha=554, N_gamma=530
h0(m_alpha-m_gamma)=2(23-22)=+2
```

其 exact locators 为：

```text
alpha:
  TPC-133 line 429
  b328ec79cf5c1ae88a675053fb9c76d46600d72a2aa36b5ae65a211ee42f599f
  TPC-134 line 1500
  d43e5c3f72be0c6eff2d48a7021892e3f079216395b0cfe981d6f1499c48203f
  TPC-136 line 1500
  7b7bdcdadf50b56bdb08d86ed465a410b24afaaef98f638b7d3ef373e86d62a0

gamma:
  TPC-133 line 283
  cef1da75b09f74ee50cca1f0470a3c2f05fdf99f9b7ccadd018edc4b727bf5a1
  TPC-134 line 963
  c527e8336cba6e0852513001aaba4cf2dba3b57949e298ec9287b2cef6631870
  TPC-136 line 963
  5d76d51cbde9c470e087311c93545285c5201ba721f6a1c21f66f480a77ee146
```

两条 source primes 与全部 parent/upstream joins 都通过。若一个同名
opened slice 同时包含 boundary rows `d=1,2`，support geometry 唯一强制
`D=1`，从而条件给出：

```text
J=K/D=32
Q_18=LD=16
```

但 support containment 不能证明 actual
`omega_1(1),omega_1(2)` 都非零，也不能产生 joint packet locator。更早
还必须决定同一 physical source lock 采用 primitive、constant，还是
nonprimitive endpoint mask/object；三者不得混同。

### 18.6 最终裁决与下一有限路线

本轮 gate verdict 为：

```text
ONE_POSITIVE_DETERMINANT_TWO_NONSELECTED_PAIR_OPENED_D_PACKET_ATTACHMENT_GATE
  = FAIL_CLOSED_AT_PRIME_SOURCE_CARRIER_MEMBERSHIP
    STOP_SCOPED_NOT_REOPENED

formal archive projection = 13/42
formal first missing = D at field 9
gate first fatal = GAMMA_ELL_16_NOT_PRIME
actual joint pair records = 0
production occurrences = 0
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

新增且仅新增第 6 节的两个 cells。第 6 节全部旧 cells，尤其
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`，继续原样
`STOP_SCOPED`。两个 O161 parents、pair-native reroute、H1 与 global
architecture 继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为
`UNPAID`，`L2=NONE`。

下一关冻结为：

```text
ONE_POSITIVE_DETERMINANT_TWO_PRIME_PRIME_MIXED_D_MASK_AND_OPENED_PACKET_ATTACHMENT_GATE
```

其固定顺序是：

1. 对 `23/11` seed source-lock actual joint mask；TPC-25/TPC-32
   primitive mask 会因 `d_gamma=2,h0=2` 把 pair 杀为零，TPC-18 formal
   constant mask不能自动代表 physical packet；
2. 只有 source theorem 选择了同一个 nonzero physical mask/object，才
   审同名 `D=1` slice 的 exact `omega_1(1),omega_1(2)`；
3. 只有前两关通过，才冻结 `J=32,Q_18=16`、joint pair/packet ID、
   coefficient AST、active nonzero、normalization 与完整 loss ledger。

若 primitive/constant physical-mask attachment 不存在，则 fail closed，
下一 architecture reroute 冻结为：

```text
TPC18_S_EQUALS_2_NONPRIMITIVE_ENDPOINT_SOURCE_FORWARD_GATE
```

只有同一 source lock 上的 actual mask、named `D=1` slice、joint packet
与后续全部 production fields 真实形成，才可讨论 TPC-207。

## 19. 不编号 `23/11` mixed-`d` actual-mask 审计

### 19.1 冻结对象

本轮只审核：

```text
ONE_POSITIVE_DETERMINANT_TWO_PRIME_PRIME_MIXED_D_MASK_AND_OPENED_PACKET_ATTACHMENT_GATE
```

诊断 seed 继续原样：

```text
X=512, h0=2, R=4, V=2
alpha=(ell=23,d=1,k=24)
gamma=(ell=11,d=2,k=48)
j=24
(jL,jK,D0)=(4,5,0)
L=16, K=32
m_alpha=23, m_gamma=22
N_alpha=554, N_gamma=530
h0(m_alpha-m_gamma)=+2
```

两条 source primes 与 TPC-133/134/136 parent/upstream joins 仍通过；这只
证明 archive identity，不自动产生 actual physical pair。

### 19.2 actual joint mask 点审

令 `H=rad(h0)=2`。逐对象裁决为：

```text
TPC-18 primitive witness:
  gcd(d_alpha*j,h0)=gcd(24,2)=2
  gcd(d_gamma*j,h0)=gcd(48,2)=2
  joint mask = 0

TPC-25 actual primitive carrier:
  gcd(d_gamma,H)=gcd(2,2)=2
  gcd(j,H)=gcd(24,2)=2
  gamma row absent; orbit support also kills both sides

TPC-32 actual physical carrier:
  gcd(m_gamma,H)=gcd(22,2)=2
  gcd(j,H)=gcd(24,2)=2
  actual physical pair absent

TPC-93:
  exports only an already retained TPC-32 coefficient
  no carrier creation

TPC-18 formal constant mask:
  xi(1,24)=xi(2,24)=1
  FORMAL_COVER = YES
  FORMAL_TO_PHYSICAL_ATTACHMENT_THEOREM = ABSENT
```

所以 gate-level 首致命为：

```text
SOURCE_LOCKED_NONZERO_ACTUAL_JOINT_PHYSICAL_MASK_FOR_TPC23_11_SEED
  = ABSENT
```

在 actual primitive branch 内更具体的首阻断是
`GAMMA_PRIMITIVE_ROW_CARRIER_MEMBERSHIP`。formal `xi=1` 不得改名为
TPC-25/32 actual physical packet。

### 19.3 `D=1` 没有被解锁

按 gate 顺序，nonzero actual mask attachment 失败后不得进入 `D=1`
attachment。独立的
fail-closed source census 仍检查了是否存在会推翻该停止的 exact member：

```text
all-ref declared text-extension blobs = 7,596
extensions = .py,.json,.tex,.md,.bib,.toml,.csv,.txt,.jsonl
TPC text blobs = 2,132
TPC blobs containing dyadic omega_D-style symbols = 33
source theorem/artifact evaluations omega_1(1) = 0
source theorem/artifact evaluations omega_1(2) = 0
same named member with both endpoint values nonzero = 0
```

TPC-18 只给 `supp omega_D subset [D,2D]`、bounded-overlap partition 与
`sum_D omega_D(d)=1`；TPC-55 只继承 support/derivative bounds；TPC-19
和 TPC-54 的 nonzero/bounded-away statements 都是额外 hypothesis。
若同一 member 包含 `d=1,2`，support geometry 的确条件强制 `D=1`，
但 containment 与 partition identity 都不证明
`omega_1(1),omega_1(2)` 同时非零，也不产生 packet locator。

因此：

```text
D1_ATTACHMENT_GATE_REACHED = NO
D = NOT_MATERIALIZED
J = NOT_MATERIALIZED
Q_18 = NOT_MATERIALIZED
formal archive projection = 13/42
formal first missing = D at field 9
actual joint pair records = 0
production occurrences = 0
```

反事实地，若未来 source-locked theorem 把同一 named `D=1` member
theorem-backed attach 到这两条 exact rows，并证明
`omega_1(1),omega_1(2)` 非零，才可真实新增
`D=1,J=32,Q_18=16`，投影变为 `16/42`，contract-order 首缺变为 `T`；
这不自动补 `source_locator`、`packet_id`、pair/edge/target IDs、
coefficient nonzero、normalization 或 loss ledger。

### 19.4 nonprimitive 对象边界

TPC-18 `s=2` endpoint theorem 是两侧共用同一 `k` 的
`beta_I(k)^2` correlation，不是本 seed 的 mixed opened rows
`k_alpha=24,k_gamma=48`。而当前

```text
D0=0, V=2, I={1,2}
beta_I(k)=mu(1)+mu(2)=0  for every even k
beta_I(24)=beta_I(48)=0
```

所以本 seed 也不能偷渡为 nonprimitive endpoint witness。后续
nonprimitive route 的 Gate 0 必须先 source-lock：

```text
one common k
s=gcd(k,h0)=2
beta_I(k) != 0
named endpoint coefficient/object
actual source-forward record
```

### 19.5 新 source 与回归

新 pull 的 RH-327 证明的是 noisy Markov cyclic trace
`T=B+S+R` 与 synthetic exchange cancellation interval。其 `d` 是
clearance ratio、`J` 是 state-space window、`L/D` 是 shell scale/demand，
没有 TPC `omega_D`、Möbius row pair、determinant-two coefficient或
packet occurrence；其 Hardy normalization 与 `B/S/R` trace ledger 属于
RH noisy cyclic-trace 对象，不能提供本 seed 所需的 TPC
formula-semantic normalization 或 complete physical-loss ledger。它不
触发任何 TPC reopen。

随后远端新增的 RH-328 只把 RH-326/327 的 trace slots 写成 conditional
fixed-reference equation
`e=L(c_phys^(2k)-y)+E_obs+R`。其 theorem 明确以 physical shell
representation、scale 与 contrasts 已给定为前提；ledger 继续把 actual
exchange representation、physical fields、remainder little-`o` 与 actual
joint matching 保持 `OPEN`。其中 `d/L/D` 分别是 clearance、shell scale
与 scalar demand，不是 TPC divisor/dyadic scale。它没有
`omega_D`、Möbius row、`23/11` source lock、common-`k` endpoint 或 TPC
packet record，也不触发 reopen。

`d3e21af..24a962f` 的新增内容只有 RH-327/328，没有 primary TPC theorem
source。

TPC-206 三项、TPC-205 三项、TPC-194 hardening、TPC-173--179 optimized、
TPC-184/189 normal/optimized 与 TPC-133 normal/optimized 全部通过。
扩展 source-chain 回归发现 TPC-134--136 的三层 upstream raw-file SHA pins
仍是旧值；生成的 866 atoms、2,988 paths、frontier manifest、cut archive
及全部语义字段均未变化。只刷新下列 provenance pins 后，
TPC-134/135/136 normal/optimized 全部通过：

```text
TPC-134 <- TPC-133 atoms:
  a1956cf182ad219da10d850de7c7e57de69b8c287fb698e44faa5c795c3840a8
TPC-135 <- TPC-134 paths:
  efcacc90e7662fdb41c2e3f86fb37d3bd81b64a107c36dfbbb15bb48bde61712
TPC-136 <- TPC-135 certificate:
  c9e91c7cb69120e4f74554262356b8112061bd9cc9c13d5ce1c7232a54165e0a
TPC-136 <- TPC-135 frontier manifest:
  6655a4c40a57f0a45022ab527b32560a5b2ac3e932368709502cfded43a3fb47
```

### 19.6 最终裁决与下一有限路线

```text
ONE_POSITIVE_DETERMINANT_TWO_PRIME_PRIME_MIXED_D_MASK_AND_OPENED_PACKET_ATTACHMENT_GATE
  = FAIL_CLOSED_AT_NONZERO_ACTUAL_PHYSICAL_JOINT_MASK_ATTACHMENT
    STOP_SCOPED_NOT_REOPENED

TPC207_TRIGGER = NO
TPC207_CREATED = false
```

本轮新增且仅新增第 6 节的一个 seed-scoped cell。全部旧 cells，尤其
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`，继续 `STOP_SCOPED`。
两个 O161 parents、pair-native reroute、H1 与 global architecture
继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为 `UNPAID`，
`L2=NONE`。

下一项不编号 architecture gate 冻结为：

```text
TPC18_S_EQUALS_2_NONPRIMITIVE_ENDPOINT_SOURCE_FORWARD_GATE
```

其 Gate 0 是
`NONZERO_COMMON_K_AND_BETA_I_K_NE_0_NAMED_ENDPOINT_RECORD`。当前
`D0=0,V=2` packet 与 `23/11` seed 均不可复用。只有该 Gate 0 及 actual
source-forward、normalization、loss ledger 后续门槛真实通过，才允许
讨论 TPC-207。

## 20. 不编号 TPC-18 `s=2` source-forward 审计

### 20.1 冻结对象与 gate 顺序

本轮只审核：

```text
TPC18_S_EQUALS_2_NONPRIMITIVE_ENDPOINT_SOURCE_FORWARD_GATE
```

Gate 0 继续严格要求同一 source lock 上同时存在：

```text
one common k
s=gcd(k,h0)=2
beta_I(k) != 0
named endpoint coefficient/object
actual source-forward record
```

不同 `k` 的 opened rows 不得拼成 common-`k`；formal coefficient 不得改名为
actual packet；endpoint support 不得改名为 nonzero 或小量。上一轮
`D0=0,V=2` packet 与 `23/11` mixed-`k` seed 均不自动复用。

### 20.2 TPC-18 精确公式与 `h0=2` 特化

TPC-18 定义

```text
I = (D0,V] intersect N
beta_I(k) = sum_{d|k, d in I} mu(d).
```

若 `s=gcd(k,h0)>1`、`H=rad(s)`，其 endpoint theorem 精确给出

```text
beta_I(k)
  = sum_{e|k,(e,H)=1} mu(e) Omega_H(e),

Omega_H(e)
  = sum_{f|H} mu(f) 1_{D0<ef<=V},

supp Omega_H
  subset (D0/H,D0] union (V/H,V].
```

对 `h0=s=2`，`H=2`、`k` 必须为偶数，并且

```text
Omega_2(e)
  = 1_{D0<e<=V} - 1_{D0<2e<=V}.
```

在 stopping theorem 的 `D0<V/2` 范围内，对每个正整数 `e` 都有

```text
Omega_2(e) = -1  for D0/2 < e <= D0,
Omega_2(e) = +1  for V/2  < e <= V,
Omega_2(e) =  0  otherwise.
```

在 `beta_I(k)` 的 endpoint sum 内还要求 `(e,2)=1`，且 `mu(e)=0` 的项
没有贡献；所以实际贡献者只能是奇数、平方自由的 endpoint divisors。
所以 `beta_I(k)!=0` 当且仅当 `k` 的奇部在两个 endpoint bands 上的带
Möbius 符号 divisor sums 不相等。这是 pointwise exact identity，不是
average cancellation theorem。TPC-18 的 nonprimitive correlation 严格使用
同一个 `k` 上的 `beta_I(k)^2`；TPC-205/206 的
`k_alpha=24,k_gamma=48` 不能改写成该对象。

### 20.3 当前 source-locked packet census

TPC-133 的 866 个 raw `(ell,k,d)` rows 商掉 `d` 后给 585 个 distinct
`(ell,k)`。其中 `h0=2`、`gcd(k,h0)=2` 的偶数 `k` rows 有 281 个；
再要求 `ell` 为 prime 有 91 个。存在 10 个同偶数 `k` 的 prime-source
formal fibers：

```text
k = {4,6,8,10,12,14,18,20,32,48}
ordered formal source pairs = 80
unordered formal source pairs = 40
```

但该 source lock 固定 `D0=0,V=2`，故

```text
I = {1,2}
beta_I(k) = mu(1)+mu(2) = 0  for every even k.
source-locked h0=2 formal beta_I(k)!=0 records = 0
materialized source-locked h0=2 nonzero per-k endpoint records = 0
```

这 40 个 unordered pairs 只证明 same-`k` row combinatorics，不是 nonzero
endpoint coefficient，更不是 actual pair occurrence。其当前 Gate 0
首致命为：

```text
SOURCE_LOCKED_H0_2_COMMON_K_BETA_I_K_NE_0 = ABSENT
```

下游 actual census 同样为零：

```text
TPC-136 downstream maps:
  4/4 domain_cut_path_ids = []
  status = NOT_TESTABLE

TPC-143:
  obligations = 2,988
  actual_map_edges = [] on every obligation

TPC-153:
  shadows = 2,988
  nonnull actual_occurrence_id = 0
  is_actual_occurrence = false on every shadow

TPC-154:
  formal fibers = 2,989
  formal occurrence edges = 8,967
  theorem_backed_actual_provenance = true count = 0
  actual completions = 0
```

因此 42-field registry 新增字段为 0，actual occurrence IDs 为 0；
projection 仍为 `13/42`，field-order first missing 仍是 `D`。

### 20.4 通用公式非零，但不是 actual record

不得把上一小节的 finite-corpus 零结论提升为 TPC-18 通用
nonexistence。精确公式立即给出纯代数候选，例如

```text
h0=2, s=2, D0=6, V=18, k=22, e=11
Omega_2(11)=+1
beta_I(22)=mu(11)=-1
FORMAL_ALGEBRAIC_NONZERO = YES
```

这只说明 `beta_I(k)!=0` 在公式上可实现。它没有 theorem-valid physical
block schedule、具名 source pair、nonzero smooth cutoff value、packet/cut
locator 或 source-forward occurrence，不得获得 actual credit。

TPC-18 自带 certificate 也固定
`h=6,D0=6,V=18,H in {2,3,6}`；`H=2` sector 只做 120 个 `k` 的 exact
finite identity/support regression。certificate 明确记录
`prime_asymptotic_evidence=false`，没有 per-`k` physical source/packet
record，不能改名为 `h0=2` actual witness。

### 20.5 branch-selection 缺口

TPC-18 stopping theorem 对任一满足其 block geometry 的抽象 symmetric
tail block，在额外假设 tail-failure lower bound 后，只推出以下至少一个：

```text
A = primitive generic determinant witness
B = nonprimitive endpoint finite-model witness for some s>1
```

固定 `h0=2` 后，若 B 发生则其 sector 必为 `s=2`；但 theorem 没有排除
A，也没有无条件证明 B、给出具名 source-locked block，或证明本仓库
packet 的 tail failure。具名/source-locked block 是本审计的额外 actual
要求，不是 TPC-18 定理的输出。此前 primitive
seed/mask 的 finite failures 不等于 aggregate alternative A 被 theorem
排除，故不得反推 B。TPC-18 还明确声明 endpoint localization 不推出
endpoint correlation 小量；剩余 finite-model lattice sum 仍需新估计。

因此，放宽到通用 TPC-18 参数后，route-level 缺口依次为：

```text
SOURCE_LOCKED_THEOREM_VALID_H0_2_BLOCK_AND_THEOREM_BACKED_TAIL_FAILURE
  = ABSENT
NONPRIMITIVE_ALTERNATIVE_B_SELECTION_THEOREM = ABSENT
NAMED_ACTUAL_COMMON_K_ENDPOINT_PACKET_ATTACHMENT = ABSENT
```

Gate 0 已 fail closed，normalization 与 complete physical-loss ledger
未进入审核，不能用“尚未审核”改写成“已通过”。

### 20.6 新 source、回归与最终裁决

本轮启动 `git pull --rebase origin main` 为 already up to date；HEAD
`f2f98b0bdc4b56c36292e9211b19c1d2e45ffae0` 之后没有新增 primary
TPC theorem source。RH-327/328 已在上一轮按对象错型排除；本轮没有新的
reopen trigger。

TPC-206 三项、TPC-205 三项、TPC-194 hardening、TPC-133--136、
TPC-184/189 normal/optimized 与 TPC-173--179 optimized 全部通过。

扩展回归发现上一轮刷新 TPC-134--136 upstream SHA pins 后，
TPC-143 committed certificate 尚未级联刷新：

```text
TPC-143 obligations = BYTE_IDENTICAL (2,988 rows)
TPC-143 --check = DRIFT_AT_CERTIFICATE_ONLY
current certificate sha256
  = e398b38b39e8a094123d2830a42ea4806d820655f55a5425f10d985a0783a724
in-memory regenerated certificate sha256
  = de1d191500da4c8de025029c08970709968407f51804b3a2a148e41620764642
semantic/census/claim fields changed = 0
provenance leaf changes = 12
```

12 个 leaves 仅把五条 legacy raw-hash bindings 的 recorded SHA/status 与总
status 从 stale 刷到 canonical UTF-8/LF match；obligations、census、
proved、actual status、first missing 与 claim boundary 全部不变。
隔离副本证明刷新会沿 TPC-143--179，并继续经 source inventories/releases
级联到 TPC-204--206。为避免在本次数学 gate 中静默重写已发布论文与稳定
PDF/source-lock release，本轮不执行该全链 mechanical refresh。它不是
theorem trigger，也不改变上述零 occurrence 裁决；但在下一篇编号论文发布
前必须单独完成完整 provenance cascade、重建受影响 releases 并全链
`--check`：

```text
PROVENANCE_CASCADE_REFRESH_REQUIRED_BEFORE_NEXT_NUMBERED_RELEASE = YES
```

最终裁决：

```text
current D0=0,V=2 source-locked packet
  = FAIL_CLOSED_AT_BETA_I_K_NE_0

general-parameter h0=2 route
  = FAIL_CLOSED_AT_SOURCE_LOCKED_THEOREM_VALID_BLOCK_AND_TAIL_FAILURE
    THEN_B_SELECTION_AND_ACTUAL_PACKET_ATTACHMENT

TPC18_S_EQUALS_2_NONPRIMITIVE_ENDPOINT_SOURCE_FORWARD_GATE
  = STOP_SCOPED_NOT_REOPENED

general TPC-18 formal beta nonzero = YES_L0_ONLY
current source-locked h0=2 beta-nonzero records = 0
actual named common-k endpoint records = 0
actual source-forward records = 0
production occurrences = 0
formal archive projection = 13/42
formal first missing = D at field 9
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

本轮新增且仅新增第 6 节的一个 finite-corpus cell。全部旧 cells，尤其
`TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`，继续 `STOP_SCOPED`。
两个 O161 parents、pair-native reroute、H1 与 global architecture
继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为 `UNPAID`，
`L2=NONE`。

下一项不编号 architecture gate 冻结为：

```text
TPC18_H0_2_NONPRIMITIVE_ALTERNATIVE_SELECTION_AND_ACTUAL_PACKET_ATTACHMENT_GATE
```

固定顺序是：

1. source-lock 一个 theorem-valid `h0=2` symmetric tail block、exact
   `X,L,K,R,V,D0` schedule 与 actual tail-failure input；
2. 新 theorem 排除 primitive alternative A，或直接给出 `s=2`
   finite-model correlation B 的所需下界；
3. 在同一 source lock 上冻结 named common `k`、`beta_I(k)!=0`、endpoint
   coefficient、source pair 与 actual packet/cut locator；
4. 只有前三关通过，才审 TPC-205/206 source-forward fields、
   normalization 与 complete physical-loss ledger。

`(D0,V,k,e)=(6,18,22,11)` 只可作为 algebraic diagnostic candidate，
不得预记为 physical record。只有上述四关真实通过，才允许讨论 TPC-207。

## 21. 不编号 `h0=2` exact-profile / branch-selection / attachment 审计

### 21.1 冻结对象与裁决

本轮只审核：

```text
TPC18_H0_2_NONPRIMITIVE_ALTERNATIVE_SELECTION_AND_ACTUAL_PACKET_ATTACHMENT_GATE
```

顺序仍是 theorem-valid block、actual tail-failure、排除 primitive A 或直接
选择 `s=2` 的 B、同一 source lock 上的 actual packet attachment。结果是
前置几何与系数层得到真实推进，但任何 actual / L2 trigger 均未成立：

```text
SOURCE_BACKED_EXACT_DYADIC_H0_2_PROFILE
  = YES_THEOREM_SPECIALIZATION

EVEN_K_BETA_I_K_NE_0_ON_SMOOTH_K_SUPPORT
  = YES_EXISTENTIAL_COEFFICIENT_LEVEL_ONLY

SOURCE_BACKED_ACTUAL_H0_2_SYMMETRIC_TAIL_FAILURE_LOWER_BOUND
  = ABSENT

FULL_R_R_PRIMITIVE_GENERIC_DETERMINANT_CORRELATION_BOUND
  = ABSENT

DIRECT_C_I_2_MM_OFF_LOWER_BOUND_OR_OCCURRENCE
  = ABSENT

NAMED_SOURCE_LOCKED_ACTUAL_PACKET_CUT_ATTACHMENT
  = ABSENT
```

因此本轮不能创建 TPC-207。

### 21.2 一条精确 dyadic published-profile family

TPC-17 的 published Maynard theorem 对每个固定 `h!=0` 成立，故可严格
取 `h0=2`。令 `m>=1`，并冻结

```text
sigma = 1/1000
delta = 1/20
eta   = 1/1000

X_m  = 2^(21000 m)
R_m  = 2^(9450 m)
V_m  = 2^(4725 m)
L_m  = 2^(9979 m)
D0_m = 2^(979 m)
K_m  = 2^(11021 m)
I_m  = (D0_m,V_m] intersect N.
```

这不是近似 exponent ledger：所有量都是整数，`L_m,K_m` 是 dyadic，且

```text
R_m = floor(X_m^(1/2-delta))
V_m = floor(sqrt(R_m))
L_m K_m = X_m
L_m/R_m = 2^(529m)
V_m/D0_m = 2^(3746m)
K_m/V_m^2 = 2^(1571m).
```

published-profile 三个 monomial 与 leakage 的精确 bit margins 为

```text
X_m/(D0_m L_m^2)          = 2^(63m)
X_m^4/(D0_m^12 L_m^7)    = 2^(2399m)
X_m^10/(D0_m^20 L_m^19)  = 2^(819m)
X_m/(L_m D0_m R_m)        = 2^(592m).
```

所以 `eta=1/1000` 小于全部固定 power margins；同时
`1/42+3 sigma<delta<1/4`。对充分大 `m`，TPC-17 的 published theorem
确实给该 family 的 prefix cancellation 与 exact symmetric-tail normal form。
这清除了“`h0=2` 几何是否存在”的问题，但不提供 tail 的正性、失败下界、
具名有限 `m` 的 theorem threshold、具体非零 cutoff 值或 actual occurrence。

### 21.3 smooth `k`-support 上的 even-sector 非零系数

固定 TPC-17 的非负 dyadic partition weight `psi`。其正值集包含某个开区间
`J=(a,b)`。由上一小节的 `K_m/V_m^2 -> infinity`，对充分大 `m` 可取奇素数

```text
p_m in (V_m/2,V_m]
q_m in (a K_m/(2p_m), b K_m/(2p_m)),  q_m>V_m,
k_m = 2 p_m q_m.
```

第二个素数由固定比例区间上的 PNT 保证。于是

```text
gcd(k_m,2)=2
k_m/K_m in J
psi(k_m/K_m)>0.
```

`k_m` 在 `I_m` 中唯一的 divisor 是 `p_m`，故 TPC-18 的 literal coefficient
给出

```text
Omega_2(p_m)=1
beta_I_m(k_m)=mu(p_m)=-1.
```

所以一般 `h0=2` route 的障碍不是 even-sector `beta` 恒零。这个结论是由
已冻结公式与 PNT 推出的 coefficient-level existence lemma；它没有给
`ell_1,ell_2`、residual target values、source pair、packet/cut locator、
tail-failure 或 source-forward ID，严禁记为 actual attachment。

### 21.4 旧 finite diagnostic 的修正

上一轮的

```text
(D0,V,h0,k,e)=(6,18,2,22,11)
```

虽有 `Omega_2(11)=1` 与 `beta_I(22)=-1`，却不能进入允许的 dyadic
`k`-cutoff。几何要求 `K>2V=36`；`supp psi subset [1/2,2]` 与
`psi(22/K)!=0` 又要求 `K<=44`，而 `(36,44]` 没有 dyadic `K`。故其精确
状态是

```text
ALGEBRAIC_NONZERO = YES
DYADIC_SMOOTH_SUPPORT_ATTACHMENT = IMPOSSIBLE.
```

较好的有限 L0 diagnostic 是

```text
(D0,V,h0,k,e)=(6,18,2,66,11)
beta_I(66)=-1.
```

dyadic partition 精确给 `psi(66/64)+psi(66/128)=1`，所以 `K=64` 或
`K=128` 至少一个 cutoff 非零，且两者均满足 `K>36`。但它没有唯一 `K`、
`X,L,R`、published-profile source lock、source pair 或 tail failure，仍只准
作 finite L0 diagnostic。

### 21.5 actual attachment census 与 synthetic firewall

当前生产链仍是：

```text
TPC-133 native rows = 866
TPC-134/136/143/153 records = 2,988 each
production h0=2,D0=0 records = 2,988

TPC-136 FRONTIER_UNMAPPED = 2,988/2,988
TPC-143 occurrence lift NOT_TESTABLE = 2,988/2,988
TPC-153 actual occurrence IDs = 0
```

TPC-154 的 2,989 个 fibers 中，唯一正 `D0` 的记录冻结

```text
X=2^84, R=2^21, V=2^10, D0=2, L=2^38, K=2^46, h0=2.
```

TPC-135 deterministic policy 把它分类为 `ELIGIBLE`；但记录本身严格是
`SYNTHETIC_L0_ONLY`，并有

```text
native_tuple = (0,0,0)
actual_active_support = UNDECIDED
theorem_backed_actual_provenance = false.
```

在该 synthetic schedule 上可构造纯 formal 算术候选

```text
k = 521 * 2^37
k/K = 521/512
gcd(k,2)=2
Omega_2(521)=1
beta_(2,1024](k)=-1
source-prime diagnostics = 274877906951, 274877906957.
```

三个数均经独立 deterministic primality check 通过。但 exact `W,psi` 非零、
native row、cut/packet ID、joint source locator 与 actual occurrence 全缺，故
它不能填 42-field registry 的任何 selected-lineage 缺口。

当前 `D0=0,V=2` 档案虽有 10 个 even-`k` prime-source groups 与 40 个
unordered same-`k` source pairs，但全部 `beta_I(k)=mu(1)+mu(2)=0`；同批
pair 的 TPC-18 row determinant `h0(m1-m2)=±2` 命中数也为 0。TPC-206
因此仍为 `13/42`，field-order first missing 仍是 `D`。禁止把 synthetic
`D0=2`、formal prime diagnostics 与 selected `X=512` lineage 拼接。

还须保持三条 schema firewall：TPC-154 line 2,989 虽有 `FORMAL_ONLY det=2`
标签，但 actual affine data 给 `su-ad=1` 且 provenance 为 false；TPC-205 的
determinant-two fixture 是 `DERIVED_L0_ONLY`、`production_occurrence=false`；
TPC-18 的 `s=2` 是 `gcd(k,h0)` content sector，不是 literal `su-ad=2`
two-Möbius atom。三者均不得跨对象拼接。

### 21.6 theorem source audit 与三重 fatal

本轮 all-ref 扫描覆盖 34 refs / 28 unique tips；TPC-18 的三个关键 source
files 各只有 commit `f418ea1` 加入的一个历史 blob，没有更强旧版本。仓库与
primary candidates 的逐对象裁决为：

1. `tail-failure`：TPC-17 只证 prefix cancellation / tail normal form；
   TPC-18 把 `|T_{L,K}(I)|>=eta X/(log X)^a` 明列为额外假设。Lichtman 与
   Matomäki--Radziwiłł--Tao 是 shift-average / log-average 对象；Maynard、
   Li、Pascadi 是 AP 或 factorable-weight 平均分布与上界，均不给同一 actual
   `h0=2` block 的 lower bound。
2. primitive A：TPC-27/28 只控制 selected calibrated truncated square；
   `u,v>T` ultra-long complement 未恢复。TPC-108 的 fixed-`h0` generic
   affine estimate 仍标为未证 L2。现有 AP / spectral large-sieve 定理不等于
   TPC-18 的完整 `r_R(n_1)r_R(n_2)` variable-determinant correlation。
3. direct B：TPC-18 Gram floor 只给 aggregate `sum_k beta_I(k)^2` mass，
   不给 prime source、`Lambda_R` pair、off-diagonal signed correlation 或
   `s=2` selection。Goldston--Yıldırım 使用不同的 truncated-divisor model；
   Ramaré--Zúñiga Alterman 是 scalar LCM diagonal；Laporta 的假设已含
   Hardy--Littlewood 强度；Coppola--Murty--Saha 需要当前未验证的 coefficient
   decay。都不能改名为 `C_{I,2}^{MM,off}` lower bound / occurrence。

因此最早 fatal 是

```text
SOURCE_BACKED_ACTUAL_H0_2_SYMMETRIC_TAIL_FAILURE_LOWER_BOUND = ABSENT.
```

即使暂借该假设，后面仍独立卡在

```text
FULL_R_R_PRIMITIVE_GENERIC_DETERMINANT_CORRELATION_BOUND = ABSENT
DIRECT_C_I_2_MM_OFF_LOWER_BOUND_OR_OCCURRENCE = ABSENT.
```

### 21.7 STOP scope、路线选择与下一关

最终裁决：

```text
TPC18_H0_2_NONPRIMITIVE_ALTERNATIVE_SELECTION_AND_ACTUAL_PACKET_ATTACHMENT_GATE
  = STOP_SCOPED_NOT_REOPENED

exact theorem-valid h0=2 dyadic family = YES
even-k beta nonzero on smooth k-support = YES_L0_COEFFICIENT_ONLY
actual named tail-failure blocks = 0
full primitive-A exclusion theorems = 0
direct s=2 B theorems = 0
actual packet/cut attachments = 0
production occurrences = 0
formal archive projection = 13/42
formal first missing = D at field 9
TPC207_TRIGGER = NO
TPC207_CREATED = false.
```

新增且仅新增第 6 节的
`DECLARED_TPC18_H0_2_TAIL_FAILURE_A_EXCLUSION_AND_DIRECT_B_CORPUS_V1`
cell；所有旧 cells，尤其 `TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`
与上一轮 `DECLARED_TPC18_H0_2_COMMON_K_ENDPOINT_SOURCE_FORWARD_RECORD_CORPUS_V1`，
继续 `STOP_SCOPED`。两个 O161 parents、pair-native reroute、H1 与 global
architecture 继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为
`UNPAID`，`L2=NONE`。

下一条最可能取得真实推进的路线不是把 tail-failure 或 direct B 当作已知，
而是先补 primitive A 的 upper-bound 技术缺口：从 TPC-27/28 的 truncated
square 明确恢复 `u,v>T` ultra-long complement，并核查能否形成完整
`r_R r_R` determinant dispersion theorem。故下一项不编号 gate 冻结为：

```text
TPC18_H0_2_FULL_R_R_PRIMITIVE_A_ULTRA_LONG_COMPLEMENT_GATE
```

这一路线即使跑通，也只会排除 stopping dichotomy 的 A；它仍不自动供应
actual tail-failure、B lower bound、actual packet attachment 或 TPC-207 trigger。

### 21.8 启动、回归与发布边界

本轮启动时执行 `git status --short --branch` 与
`git pull --rebase origin main`；远端已同步，审计基线为
`ea865160f05193047513a8a66665dc989934ae28`。只读回归结果：

```text
TPC-206: 3/3 PASS, projection 13/42, mathematical_reopen=false
TPC-205: 3/3 PASS, production pair records=0
TPC-194 certificate hardening: PASS
TPC-133--136: 4/4 PASS
TPC-184 normal/optimized: 2/2 PASS, TARGET_WELL_TYPED_OPEN
TPC-189 normal/optimized: 2/2 PASS, TARGET_WELL_TYPED_OPEN
TPC-173--179 optimized: 7/7 PASS
git diff --check: PASS
handoff Markdown fences: balanced
```

所有 checker 均设置 `PYTHONDONTWRITEBYTECODE=1`；没有生成新测试产物，既有
TPC-105 `__pycache__`、TPC-63 构建文件与 `tmp/` 均未触碰。本轮没有创建
论文或 PDF，故没有伪造 PDF QA。TPC-143 的 certificate-only 12-leaf drift
仍按第 20 节隔离：它不改变 2,988 obligations 或零 occurrence 裁决，但在
下一篇编号 release 前仍必须完成完整 provenance cascade。

## 22. 不编号 full-`r_Rr_R` primitive-A / ultra-long complement 审计

### 22.1 冻结对象与最终裁决

本轮只执行页首原定 gate：

```text
TPC18_H0_2_FULL_R_R_PRIMITIVE_A_ULTRA_LONG_COMPLEMENT_GATE
```

逐公式审核覆盖 TPC-18、TPC-19、TPC-25--32、TPC-33--124 的实际
ultra-residual lineage，并复核 TPC-125--206 的相关 claim/status。结果不是
“TPC-27/28 之后没有路线”，而是精确定位出了两个互相独立、均未通过的门槛：

```text
CURRENT_EXACT_H0_2_FAMILY_HAS_LEGAL_TPC27_28_TRUNCATED_ENTRY = NO

SELECTED_TPC28_PACKET_FULL_MATCHED_ULTRA_SHELL
  = REDUCED_TO_SMALL_CONTENT_AUXILIARY_ZERO

SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_THEOREM = ABSENT
ALL_RELEVANT_D_SLICES_UNIFORM_ATTACHMENT = ABSENT
ORIGINAL_PHYSICAL_NORMALIZATION_AND_EXACTLY_ONCE_REASSEMBLY = ABSENT

FULL_R_R_PRIMITIVE_GENERIC_DETERMINANT_CORRELATION_BOUND = ABSENT
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

因此精确裁决为：

```text
TPC18_H0_2_FULL_R_R_PRIMITIVE_A_TRUNCATED_ENTRY_AND_
SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_ABSENT_
STOP_SCOPED_NOT_REOPENED
```

### 22.2 TPC-18 literal 对象与完整 complement ledger

TPC-18 一个 dyadic `D`-slice 的 primitive generic 对象是

```text
m_i = ell_i d_i
J = K/D
Q = LD
QJ ~ X

C_D,prim^gen
  = sum_j sum_(alpha_1 != alpha_2)^generic
      mu(d_1)mu(d_2)(log ell_1)(log ell_2)
      r_R(m_1 j + 2) r_R(m_2 j + 2)
      B_alpha_1(j) B_alpha_2(j).
```

`generic` 必须同时保留

```text
ell_1 != ell_2
|m_1-m_2| > Q X^(-kappa)
(d_1,d_2) <= X^kappa
(d_1 j,2)=(d_2 j,2)=1.
```

其 literal determinant、row gcd、natural normalization 与 stopping witness
分别是

```text
det = 2(m_1-m_2)
(m_1,m_2) = (d_1,d_2)
N0 = JQ^2 ~ XQ
C_D,prim^gen >> XQ/(log X)^(2a+2).
```

对 target `N_m=mj+2`，TPC-19、TPC-27--29 的 exact dictionary 是

```text
a(u)   = -mu(u) log u
b_R(u) = a(u)-lambda'_R(u)

A_m,T(j) = sum_(u<=T, u|N_m) b_R(u)
P_m,T(j) = A_m,T(j)-delta_H(m)
C_m(j)   = sum_(T<u<=U0, u|N_m) a(u)

r_R(N_m) = A_m,U0(j) = A_m,T(j)+C_m(j),
```

其中 `U0~X` 大于 physical support 上全部 targets，且 `T>=R` 才保证新 shell
上 `b_R=a`。因此 full raw complement 的 domain 不是只写 `u,v>T`，而是

```text
u,v <= U0 and max(u,v)>T.
```

它恰有三条、不多不少：

```text
A_m,T C_n : u<=T<v<=U0, coefficient b_R(u)a(v)
C_m A_n,T : v<=T<u<=U0, coefficient a(u)b_R(v)
C_m C_n   : T<u,v<=U0,     coefficient a(u)a(v).
```

TPC-29 的 calibrated cutoff difference 是

```text
P_m,U0 P_n,U0 - P_m,T P_n,T
  = A_m,T C_n + C_m A_n,T + C_m C_n
    -delta_H(m)C_n-delta_H(n)C_m.
```

即 `three raw + two drift`；没有 two-drift term，因为它在两个 cutoffs 间
精确相消。两条 drift 已有

```text
O_epsilon(X^epsilon XQ/L)
```

的 fixed-power saving。直接相对 literal full residual，则

```text
r_R(N_m)r_R(N_n)-P_m,T P_n,T
  = A_m,T C_n + C_m A_n,T + C_m C_n
    +delta_H(m)A_n,T+delta_H(n)A_m,T-delta_H(m)delta_H(n).
```

最后一行由旧 base drift bridge 控制；未关闭的 hard arithmetic object 正是
三条 raw channels 的 matched sum。只审 `C_mC_n` 会漏掉两个 mixed
rectangles，不能叫 complete complement。

### 22.3 TPC-29--32 实际关闭到哪里

TPC-28 source-compatible high-`beta` sample 对每个固定 `h!=0` 成立，故可取
`h0=2`：

```text
sigma = 1/10000
lambda = 99979/210000
delta = 7/60

Q = X^(267/400+o(1))
D = X^(10049/52500+o(1))
J = X^(133/400+o(1))
R=S = X^(23/60+o(1))
V = X^(23/120+o(1))
T = X^(193/500+o(1)).
```

它 theorem-backed 地关闭一个 selected calibrated truncated square
`Q_T^phys`，但 TPC-18 Alternative A 是“某个 `D<=V` 存在 witness”。一个
fixed high-`beta` `D`-packet 不能排除其余 slices，更不能与上一轮另一组
`sigma,delta,D0,L,K` source lock 拼接。

后续实际推进为：

1. TPC-29 对三 raw channels 的 content-rich sparse wedge 与 large selected-
   divisor-content sectors给 fixed-power saving；primitive/small-content core 留下。
2. TPC-30 用 full target content
   `c=(N_m,N_n)=(N_m,m-n)|m-n` 关闭 `c>C`：

   ```text
   S_sh(c>C)
     << X^epsilon (Q^2+XQ/C)
      = X^epsilon N0(1/J+1/C).
   ```

3. TPC-31 的 canonical determinant 是
   `Delta#=(m-n)/c`，满足 `mV-nU=2 Delta#`。它只有在 `c=1` 时才等于
   TPC-18 literal determinant divided by the fixed `h0`;不得删去 content。
4. TPC-32 exact matched shell 是

   ```text
   K^sh
     = A_m,U0 A_n,U0 - A_m,T A_n,T
     = A_m,T C_n + C_m A_n,T + C_m C_n,

   S_full^sh
     = A_hat_C,q(0) + S_sh(c>C).
   ```

   因 large-content 项已经关闭，selected packet 的唯一 hard cell 是

   ```text
   A_hat_C,q(0)
     = Phi_D[(A_m,T C_n+C_m A_n,T+C_m C_n)
             1_((N_m,N_n)<=C)].
   ```

这里 `r=0` 是 normalized-determinant auxiliary DFT zero，既不是 orbit-variable
Poisson zero，也不是 TPC-20 centered-divisor zero。TPC-27 已对每个 polynomial
`S>=R` 关闭 additive Poisson zero，因此把该旧结论再对两个 endpoints 作差不是
新 theorem，也不触及 `A_hat_C,q(0)`。

TPC-32 对 `beta=267/400, C~J` 的完整 matched-shell 结论严格条件于

```text
F0(A_C) = |A_hat_C,q(0)|^2 / ||A_C||_2^2
         <= X^(chi+o(1)),
chi <= 1/400.
```

Almost-all nonzero frequencies、Parseval 或 additive large sieve 不证明这个
distinguished coefficient 的 premise。TPC-33--108 将同一门槛依次转写成
physical column energy、four-Mobius same-time Gram、coherent spectrum、literal
low-window affine atom 与 restricted growing fixed-`h0` estimate；TPC-108 的 H3
仍明确是未证 L2。TPC-109--124 的 frame、tail-cover 与 reassembly statements
均是 L0/L1 或条件接口，没有新增该 signed estimate。

TPC-116 的数字也不得偷换：TPC-32 的 `chi<=1/400` 是 squared-flatness loss；
TPC-116 的 `sigma>=1/400` 是完整 outer costs 后的 aggregate physical saving。
前者不能靠字段同名或数值相近填入后者。TPC-116 没有 supplied growing mask
archive，也没有把 packet natural scale `N0=JQ^2\asymp XQ` source-lock 到 original
global physical normalization。

### 22.4 上一轮 exact family 的截断入口实际上为空

上一轮冻结的 published Maynard `h0=2` family 是

```text
lambda = 9979/21000
r0     = 9/20
v      = 9/40
d0     = 979/21000

D = X^d, d in [979/21000,9/40]
beta = lambda+d in [5479/10500,1838/2625].
```

TPC-26/28 的 `M_beta(t)>0` 对应 upper-cutoff supremum 为

```text
t_c(beta) = (1+beta)/4, beta<=3/5
t_c(beta) = (3-beta)/6, beta>=3/5.
```

整个 slice family 上 `t_c` 的最大值仅为 `2/5`，而 `R=X^(9/20)`；且
`t=t_c` 只是 `M=0` 边界，不满足 fixed positive margin。故不存在合法

```text
R <= S < T and M_beta(t)>0.
```

在最有利的 `S=R`，

```text
M_beta(R) = (beta-4/5)/2, beta<=19/30
M_beta(R) = (3/10-beta)/4, beta>=19/30.
```

全部为负；最佳也只有 `-1/12`。低/高 `D` endpoints 分别是
`-2921/21000` 与 `-2101/21000`。强取 `T<R` 不只是 schema 违规：shell 内
`lambda'_R` 不再消失，`b_R=a` 和 calibrated annular identity 都失效。把 shells
切薄或迭代不改善 upper-exponent minimax。

这只证明现有 TPC-26--28 Cauchy/conductor 方法不适用于该 exact family；
`M_beta<=0` 不是 arithmetic impossibility theorem。换 `delta` 是换 block，不能
改写为当前 source lock 已通过；即使换到 TPC-28 selected packet，small-content
matched auxiliary-zero 与 all-`D` uniformity 仍独立开放。

### 22.5 现有 bounds 与新增 primary-source 扫描

TPC-18 diagonal energy、row Cauchy 与 soft divisor bounds 合起来至多给

```text
|C_D^gen| <<_epsilon XQ X^epsilon,
```

即 natural scale，不能反驳 `XQ/log^(2a+2)` 的 positive stopping witness。
TPC-16 residual energy在当前 `delta=1/20` family 上还有主量

```text
sum_n r_R(n)^2 F(n/X)
  = (11/20+o(1)) X log X I0(F),
```

所以不能把 residual energy 当成小系数。reflected unit fiber `r=s=1` 对任何
`T<X` 仍含 ordinary smooth two-point Mobius correlation；固定-divisor large
sieve 在该 fiber 上没有可平均 conductor。它的原 row determinant 是
`2(m-n)`，未经 content extraction、actual packet 与 normalization crosswalk
不得改名为 literal determinant-two atom。

本轮扫描全部 Git refs/history（346 commits）与 TPC-18--206 relevant lineage；
`HEAD=origin/main=687bc2d44a25efd2a376fd3b363bfac4549b4cb9` 时没有新增 repo primary TPC
theorem source。外部截至 2026-07-31 的新增/最近 primary candidates 中：

1. Siddarth Menon, *Improved bounds for multiplicative functions in almost all
   short intervals*, arXiv:2607.15574v1。Theorem 1.1 是对 interval origin 的
   short Liouville/Mobius sum mean square；Theorem 1.4 仍对 origin 作平均；
   Theorem 1.5 对 shifts 作平均。它们没有 prescribed rows、actual masks、
   full `r_Rr_R`、variable determinant 或 all-slice/all-prefix uniformity。
2. Ramaré--Zuniga Alterman, *On a Mobius double sum*, arXiv:2603.25961v3，
   控制静态 `sum mu(d)mu(e)/[d,e]^(1+epsilon)`；这是 size/LCM diagonal
   object，没有 orbit `j`、affine targets 或 matched ultra shell。
3. Tao、MRT、Tao--Teräväinen、Pilatte、Lichtman--Teräväinen 的相关 rigorous
   results 分别在 logarithmic average、shift average、exceptional scale 或
   fixed-form/non-growing quantifier处先行失败；Siegel-zero routes还带额外条件。

未发现 theorem-backed

```text
DD_2(theta) for every actual primitive D-slice
```

或等价的 complete `P_T C+C P_T+CC` theorem。对当前 exact family，直接
`DD_2(theta)` 还须以固定余量覆盖

```text
theta_tail = lambda+v = 1838/2625.
```

若坚持 reflected route，则 theorem 必须包括 `r=s=1`、ordinary weights、
growing slopes、actual masks/outer coefficients 与全部 dyadic cells，并在完整
outer loss 后仍有净正 saving。TPC-108/H3 数字若被调用，还另须
`eta-ell_out>=1/200` 与 physical `TT*` crosswalk；本轮均不存在。

### 22.6 STOP scope 与下一关

本轮新增且仅新增第 6 节的

```text
DECLARED_TPC18_H0_2_FULL_R_R_PRIMITIVE_ULTRA_COMPLEMENT_CORPUS_V1
  = STOP_SCOPED
```

所有旧 cells，尤其 `TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1`、
TPC18 common-`k` V1 与 tail-failure/A/B V1，继续 `STOP_SCOPED`。不得把
Menon 的 averages、TPC-27 additive zero、TPC-32 nonzero-frequency density-one
结果或 TPC-116 conditional schema 重新包装成新 method cell。

两个 O161 pointwise parents、pair-native reroute、H1 与 global architecture
继续 `OPEN`；fixed-atom credit 为 0，strict `1/400` 为 `UNPAID`，`L2=NONE`。
TPC-207 trigger 仍为 false，没有创建论文或 PDF。

下一项最窄、最接近 hard coefficient、且不重复旧 stopped cells 的不编号 gate
冻结为：

```text
TPC32_H0_2_SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_SIGNED_PREFIX_TRANSFER_GATE
```

固定顺序是：

1. source-lock TPC-28/32 的 theorem-valid selected `h0=2` packet、三 raw
   channels、content cutoff `C`、canonical `Delta#`、actual mask/weights 与
   packet natural scale `N0=JQ^2\asymp XQ`；不得拼接上一轮 `delta=1/20` schedule；
2. 逐公式测试 TPC-111/122 的 ordered signed-prefix / bounded-variation 对象能否
   无损映射到同一个 `A_hat_C,q(0)`；determinant、content、outer labels 或
   prefix order 任一不一致即 fail closed；
3. 只有 source-backed growing signed-prefix theorem 真正推出 `chi<=1/400`，
   或直接给 small-content matched-shell saving，才可记 arithmetic advance；
4. 即使 selected packet 通过，仍须另审 all-`D` uniformity、exactly-once
   physical cover、original normalization、loss ledger、tail-failure、B selection
   与 actual packet attachment；任何一项都不自动触发 TPC-207。

下一篇编号 release 前仍必须完成 TPC-143--206 的完整 provenance cascade、
受影响 releases 重建和全链 `--check`；certificate-only drift 不得冒充数学
trigger。

### 22.7 启动、回归与发布边界

本轮启动时执行 `git status --short --branch` 与
`git pull --rebase origin main`；远端 already up to date，审计基线为
`687bc2d44a25efd2a376fd3b363bfac4549b4cb9`。只读启动回归结果：

```text
TPC-206 = 3/3 PASS
TPC-205 = 3/3 PASS
TPC-194 hardening = 1/1 PASS
TPC-133--136 = 4/4 PASS
TPC-184 normal/optimized = 2/2 PASS
TPC-189 normal/optimized = 2/2 PASS
TPC-173--179 optimized = 7/7 PASS
total = 22/22 PASS
```

TPC-27--32 的六个 legacy certificate 脚本均没有 `--check` 入口，且无条件
重写 committed JSON；为保持本轮只读验证边界，逐一审核入口后记为
`6 SKIP / 0 FAIL`，没有运行会写文件的 normal/optimized 模式。它们的 committed
papers/certificates 本轮未修改，SKIP 不得改写成新的 asymptotic evidence。

所有已执行 Python checks 均设置 `PYTHONDONTWRITEBYTECODE=1`，适用处使用
`-B`。`git diff --check` 通过，Markdown fences 为偶数且闭合。没有创建论文、
PDF 或构建日志，因此没有伪造 PDF QA。既有 TPC-105 `__pycache__`、TPC-63
构建文件与 `tmp/` 均未触碰，也没有新增 untracked artifact。TPC-143 的
certificate-only provenance cascade drift 继续按第 20 节隔离。

## 23. 不编号 TPC-32 small-content auxiliary-zero / signed-prefix transfer 审计

2026-08-04 current correction：第 48 节只覆盖本节 23.2--23.4 中“完整
post-bin dictionary intertwiner 缺失，所以 scalar zero mode 不能无损进入
ordered fibers”的 first-fatal 判断。第 48 节证明 TPC-93 已供应更窄的
source-atom common-native refinement，故 scalar transfer 为 `PRESENT_L1`；
本节的 selected-packet source lock、完整 dictionary `J` 仍缺、growing
prefix/BV 仍缺、`NO_L2` 与 `TPC207=false` 结论全部继续有效。

### 23.1 同一个 theorem-valid selected packet

本轮只执行：

```text
TPC32_H0_2_SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_SIGNED_PREFIX_TRANSFER_GATE
```

审计基线固定为
`28cafdd5fa96ff948f1520e778c7a2ba65208730`。TPC-28--32 明确沿用同一个
selected high-beta packet，而不是靠相同指数猜测拼接：

```text
sigma  = 1/10000
lambda = 99979/210000
delta  = 7/60
beta   = 267/400

Q = X^(267/400+o(1))
D = X^(10049/52500+o(1))
J = X^(133/400+o(1))
R = S = X^(23/60+o(1))
V = X^(23/120+o(1))
T = X^(193/500+o(1))
C = floor(J) = X^(133/400+o(1))
N0 = JQ^2 asymp XQ.
```

TPC-28 与 TPC-32 的 theorem interface 对每个固定 `h!=0` 陈述，故
`h0=2` 是合法 theorem-level specialization；TPC-28 JSON 没有把 `h=2`
单独序列化，TPC-32 JSON 中的 finite `h=2` coherent witness 也不得冒充
asymptotic packet attachment。

在这个 packet 上，TPC-32 保留 literal row coefficients

```text
gamma_alpha^(i)
  = mu(d_alpha) (log ell_alpha) omega_D^(i)(d_alpha)
    psi_L^(i)(ell_alpha/L) zeta_alpha^(i),

A_frak_(alpha,gamma)(j)
  = m_frak(alpha,gamma) Xi_(alpha,gamma)(j) W_(alpha,gamma)(j/J),
```

以及三条不能拆开的 raw channels

```text
A_m,T C_n,
C_m A_n,T,
C_m C_n.
```

其完整 matched shell 是

```text
K_sh(alpha,gamma,j)
  = A_m,U0 A_n,U0 - A_m,T A_n,T,

u,v <= U0 and max(u,v)>T.
```

full-target content 与 canonical determinant 为

```text
G_(m,n)(j) = gcd(mj+2,nj+2),
Delta#_(m,n)(j) = (m-n)/G_(m,n)(j),

A_C(n)
  = S_sh(G_(m,n)(j)<=C, Delta#_(m,n)(j)=n),

A_hat_C,q(0)
  = sum_n A_C(n)
  = S_sh(G_(m,n)(j)<=C).
```

因此 packet、三 raw channels、`C`、`Delta#`、literal masks/weights 与 `N0`
在 typed formula level source-lock 通过。generic pair mask 仍只知 bounded、
off-diagonal、divisor-independent；TPC-32 没有证明其 controlled projective
或 Schur decomposition。TPC-28 也仍只关闭一个 selected `D`-packet。

### 23.2 TPC-111/122 crosswalk 的第一个 fatal mismatch

TPC-111 正确地把 `r=0` 称为 TPC-32 normalized-determinant DFT 的
distinguished zero，并证明 finite coarsening invariance 与 sharp Abel duality。
但其 actual outer formula从以下条件开始：

```text
Assume content, masks, both polarizations, all native outer keys,
and literal outer reassembly have been verified.
```

随后才写成

```text
Z_X
  = sum_theta c_theta,X sum_r W_theta,X(r) sigma_theta,X(r)
    + E_content,X.
```

TPC-122 再次条件化该 reassembly，并允许把未保留的 outer keys 放入新的
`E_cont,X`。逐字段核对结果是：

| Gate field | TPC-32 selected packet | TPC-111/122 object | Verdict |
|---|---|---|---|
| literal coefficient | complete `a_sh_(alpha,gamma,j)`，含三 raw channels、两 row coefficients 与 actual joint multiplier | `c_theta W_theta sigma_theta`，factor allocation 仅条件给定 | no source-backed equality |
| determinant/content | variable `Delta#=(m-n)/G`，main term保留 `G<=C` | fixed affine determinant `h0`，content另列为 error | role crosswalk absent |
| outer labels | `(alpha,gamma,j)` 与 determinant bin `n` | ordered `(theta,r_i)` fibers | actual bijection/intertwiner absent |
| prefix order | physical orbit triples先按 `Delta#` 聚合；未给 `theta,r_i` order | literal translated-integer order不可重排 | order preservation unproved |
| normalization | `N0=JQ^2 asymp XQ` | `Q_X^2` zero-mode scale | no theorem identifies or pays the factor |

这不是说两套抽象字典数学上必不相容。精确 first missing 是 TPC-124 已经
写出的 coefficientwise fiber-intertwining test：determinant bins 与 ordered
zero-mode fibers 是不同 declared dictionaries；候选 `J` 必须满足

```text
(J Q_D - Q_Z) M = 0
```

而不能从一个 scalar total 或相似符号推出。TPC-124 的 committed audit 明确
`actual_growing_G_C_z_B_archive_present=false`，当前 artifacts 因而不能在同一
selected packet 上执行该 test。故 lossless `A_hat_C,q(0)` 到 TPC-111/122
prefix fibers 的调用在 outer-label/prefix-index 层 fail closed。

### 23.3 即使假设 crosswalk，growing arithmetic input 仍独立缺失

TPC-122 的 exact transfer 是条件式：若

```text
Delta_f <= X^(-delta_prefix+o(1)) A_f,
sum_f A_f ||w_f||_BV* <= X^(ell_Z+o(1)) Q_X^2,
|E_cont,X| <= X^(-eta_cont+o(1)) Q_X^2,
```

且全部对象、factor allocation 与 quantifier range相同，则

```text
eta_Z_cert = min(delta_prefix-ell_Z, eta_cont).
```

当前 committed claim flags 为：

```text
TPC-111 literal_growing_prefix_bound = false
TPC-111 positive_eta_Z = false
TPC-111 fixed_h0_L2_progress = false

TPC-122 actual_growing_prefix_saving = false
TPC-122 actual_outer_bv_envelope = false
TPC-122 actual_content_remainder_bound = false
TPC-122 uniform_subpower_class_hypothesis = false
TPC-122 fixed_h0_L2_saving = false
```

即使未来只补出一个 `eta_Z>0`，也不能靠字段改名直接得到 TPC-32 的
relative flatness `chi`：`F0(A_C)` 以同一个 actual `A_C` 的
`||A_C||_2^2` 为分母，而 TPC-32 当前只给该能量的 upper bound，没有可供
相除的 source-backed lower bound。若改走 direct zero bound，则仍必须先把
TPC-122 的 `Q_X^2`、全部 outer/content losses 与同一 packet 的 `N0` scale
无损 crosswalk；当前同样缺失。

TPC-126/127 的 canonical-order Abel 与 determinant-two pullback 只无损搬运
finite order、mask、weight、phase 和 prefix；它们明确不证明 complete growing
family cancellation。RH-287/RH-294 中名称相近的 rate-free growing-prefix
theorems控制 noisy trace/counterloop coefficients，不含本 gate 的 literal
Möbius coefficient、fixed physical `h0`、content、outer mask、`X/N/q` ranges
或 `N0` normalization，在第一项 physical-coefficient type check 即被排除。

发布前 rebase 另带入上游提交
`cdce55713a81cec09971d217faad154894088e3c` 的 RH-330。其对象是
`H_k=k R^(-2k)` 尺度上的 RH first-alias/full-trace coefficient，以及
`e=B+S+R+P-A` 的 conditional actual/model defect，不是 TPC-32 的
`A_hat_C,q(0)`。其 committed ledger 又明确给出
`actual_critical_packet_identified_with_weighted_prefix_coefficient=false`、
`actual_weighted_full_trace_prefix_vanishing_proved=false`、
`determinant_gluing_activated=false`。因此 RH-330 的 finite signed-prefix
恒等式没有 literal physical coefficient、fixed `h0=2`、content/determinant
fiber map 或 `N0=JQ^2` normalization，不能作为本 gate 的 growing theorem；
late-rebase type check 为 `WRONG_PHYSICAL_OBJECT_CONDITIONAL_INACTIVE`。

TPC-32 的 nonzero-frequency density-one、Parseval、large sieve 与 finite
coherent examples继续不能选择 `r=0`；`A_hat_C,q(0)` 仍可能位于 exceptional
set。没有 source-backed theorem 推出

```text
F0(A_C) <= X^(chi+o(1)), chi<=1/400,
```

也没有直接 small-content matched-shell saving。因此 arithmetic advance 为
`NO`。

### 23.4 精确裁决与 scope

本轮状态是：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
H0_2_SPECIALIZATION = PASS_THEOREM_LEVEL_NOT_JSON_SERIALIZED
THREE_RAW_CHANNELS_CONTENT_DETERMINANT_N0_LOCK = PASS
ACTUAL_GENERIC_PAIR_MASK_DECOMPOSITION = ABSENT

LOSSLESS_A_C_ZERO_TO_ORDERED_PREFIX_INTERTWINER = ABSENT
COMMON_FACTOR_ALLOCATION_AND_PREFIX_ORDER = ABSENT
N0_TO_Q_X_SQUARED_NORMALIZATION_CROSSWALK = ABSENT
GROWING_SIGNED_PREFIX_THEOREM = ABSENT
OUTER_BV_ENVELOPE = ABSENT
CONTENT_REMAINDER_AT_REQUIRED_EXPONENT = ABSENT

CHI_LE_1_OVER_400 = UNPAID
ARITHMETIC_ADVANCE = NO
TPC207_TRIGGER = NO
TPC207_CREATED = false
```

精确裁决为：

```text
TPC32_H0_2_SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_TO_SIGNED_PREFIX_
EXACT_FIBER_INTERTWINER_AND_GROWING_INPUT_ABSENT_
STOP_SCOPED_NOT_REOPENED
```

本轮新增且仅新增第 6 节的

```text
DECLARED_TPC32_111_122_SELECTED_PACKET_AUXILIARY_ZERO_SIGNED_PREFIX_TRANSFER_V1
  = STOP_SCOPED
```

它不是 growing-prefix nonexistence theorem，也不否定新的 direct
`A_hat_C,q(0)` theorem。两个 O161 pointwise parents、pair-native reroute、H1
与 global architecture 继续 `OPEN`；fixed-atom credit 为 0，strict `1/400`
为 `UNPAID`，`L2=NONE`。all-`D` uniformity、exactly-once physical cover、
original/global normalization、tail-failure、A/B selection、actual packet
attachment 与完整 provenance gates 均未进入，更没有自动通过。

### 23.5 Reopen triggers 与验证边界

本 cell 只在出现下列至少一项新的 source-backed 输入时重开：

1. 同一 TPC-28/32 selected packet 上的 actual coefficientwise intertwiner，逐项
   保留三 raw channels、`G<=C`、`Delta#`、outer keys、literal factor allocation、
   canonical prefix order、mask/weights 与 `N0` normalization；
2. 直接对同一 actual `A_C` 证明 `chi<=1/400`，或直接证明 small-content
   matched-shell saving；
3. 对同一 actual ordered fibers 的 growing signed-prefix theorem，并同时给出
   uniform outer BV、content remainder、共同 constants/ranges 与完整 physical-loss
   ledger，足以在 `N0` scale 支付目标。

没有预设下一项不编号 audit；旧 cells 不得换名重开。持续工作流授权仍有效，
但在上述 trigger 出现前不创建 TPC-207。

本轮启动回归为 `22/22 PASS`。追加的只读核对为：

```text
TPC-111 --check = PASS
TPC-124 --check = PASS
TPC-126 --check = PASS
TPC-127 --check = PASS
```

这些 PASS 只认证各自的 finite identities、counterexamples 与 claim boundaries；
它们不产生 L2。TPC-122 当前脚本没有只读 `--check` 且会写 committed JSON，
本轮只审核其 committed source/JSON，没有执行。TPC-27--32 legacy scripts 同样
未执行。没有创建论文、PDF 或构建日志；既有 TPC-105 `__pycache__`、TPC-63
构建产物与 `tmp/` 均保持原样。

## 24. 下一会话可直接粘贴（BOLD_CHANNEL_V10 current）

```text
进入仓库：
D:\26-aimath\理论研究3\prime_dynamics_theory

以仓库文件和 committed artifacts 为事实来源，不依赖旧聊天记录。先读
TPC_COMPASS.md、research/tpc-big-road/README.md、
research/tpc-big-road/fm_local_comparison_compiler.md、TPC_HANDOFF.md 页首及
第 1、6、22、24、54.18--54.19、55--57 节；其他历史块只在这些入口明确引用时展开。

先执行：

git status --short --branch
git pull --rebase origin main
Get-Content -Raw -Encoding UTF8 TPC_HANDOFF.md
$env:PYTHONDONTWRITEBYTECODE = "1"

保留全部既有 tracked/untracked；不得 reset、checkout、clean、自动 stash、删除
或纳入本轮提交。若 existing work使 rebase不安全，停止并报告。完整执行第 1 节
22 项只读回归；任一 checker非零即 fail closed。TPC-27--32 legacy与 TPC-122
writers不得执行。

当前编号事实终点 TPC-206；TPC-207 trigger=false，TPC-207未创建。当前大路状态：

H3_METRIC = PROVED_HAAR_MOVING_VARIANCE_O_N
H4_POINTED_x0 = ENDPOINT_EQUIVALENT_TARGET_OPEN
PAIR_O161_PACKET_TO_PRIMORIAL_DIRECT_COMPOSITION = STOP_SCOPED
PBAPT_TYPE_I_TYPE_II_REASSEMBLY_HIGHWAY = OPEN
COARSE_COMPARISON_TYPE_I = PROVED_SOURCE_BACKED
COARSE_COMPARISON_UNIVERSAL_TYPE_II = STOP_SCOPED_FALSE_MOD3_RANK_ONE
HYBRID_LOCAL_EULER_PROFILE = PROVED_EXACT
HYBRID_b1_w = PROVED_SOURCE_BACKED_FOR_EACH_FIXED_K
HYBRID_b2_AT_P_TPC = VACUOUS_PROVED_R_EMPTY
HYBRID_MAXIMAL_TYPE_I_GAMMA_LT_HALF = PROVED_SOURCE_BACKED
HYBRID_MAXIMAL_TYPE_I_GAMMA_EQUAL_HALF = NOT_PROVED_BY_BV
HYBRID_UNIVERSAL_TYPE_II_J_TO_SQRT = OPEN_HIGH_CONDUCTOR_WALL
H3_U_UNIVERSAL_FORK = OPEN_RESERVE_OVERSTRONG
H3_S_PROP722_GENERIC_CLOSURE = DEPRIORITIZED_BROADER_THAN_NEEDED
DIRECT_HB2_EXTRACTOR = PROVED_EXACT_REDUCTION_TO_SHB_D2
SHB_D2_MASTER = SELECTED_PRIMARY_OPEN_NEW_THEOREM
HB2_B3_MINIMAL_CORE = SELECTED_PROVISIONAL_OPEN_NEW_THEOREM
BC_COROLLARY1_DIRECT_ATTACHMENT = STOP_SCOPED_GROUPED_COR1_SCALE_NO_SAVING
ONE_POISSON_BC1_QUARTER = STOP_SCOPED_FIRST_SUMMAND_NO_NEW_RANGE
NAIVE_NATIVE_TWO_STAGE = STOP_SCOPED_AT_QUADRATIC_DIAGONAL
HB4_QUARTER_COLLECTIVE_MAIN = PROVED_SOURCE_BACKED_ALL_D_ATTACHMENT
HB4_QUARTER_RAMANUJAN_AXES = PROVED_X3_OVER_4_POWER_SAVING
HB4_QUARTER_WEIL_OFFDIAGONAL = PROVED_FOR_1_OVER_4_LT_DELTA_LT_1_OVER_3
HB4_QUARTER_PASCADI_OFFDIAGONAL = PROVED_FOR_1_OVER_3_LE_DELTA_LT_3_OVER_8
HB4_LOW_CONDUCTOR_PROJECTOR = PROVED_GAUSS_CRT_PLUS_PRIMITIVE_LARGE_SIEVE
HB4_HIGH_CONDUCTOR_INCIDENCE = PROVED_FOR_3_OVER_8_LE_DELTA_LT_1_OVER_2
HB4_QUARTER_OFFDIAGONAL = PROVED_FOR_1_OVER_4_LT_DELTA_LT_1_OVER_2
HB4_EXACT_HALF_ENDPOINT = OPEN_LOG_POWER_ENDPOINT
BP2607_FIXED_UNIT_LOCAL_ENGINE = SOURCE_ATTACHED_F_MINUS_1_OVER_16_SAVING
BP2607_AFTER_FREEZE_AND_OUTER_TRIANGLE = STOP_SCOPED_F_15_OVER_16_DEFICIT
BP2607_ARBITRARY_UNIT_VECTOR_LIFT = STOP_SCOPED_FALSE_CHARACTER_EIGENMODE
HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION = SELECTED_PRIMARY_OPEN_NEW_THEOREM
HB4_EXACT_HALF_SOURCE_WEIGHT_ENVELOPE = FROZEN_TESTABLE_SUPERCLASS_CONTRACT
HB4_EXACT_HALF_ACTUAL_ATOM_MEMBERSHIP = OPEN_ATTACHMENT
HB4_EXACT_HALF_PRIME_GAUSS_DUAL_PRODUCT_IDENTITY = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PRIME_CENTERED_DUAL_PRODUCT = PROVED_EXACT_EQUIVALENCE
COMMON_K_AS_UNIQUE_MODULAR_RATIO_FIBER = STOP_SCOPED_FALSE_COVER_NONZERO_WRAPS
GLOBAL_MOVING_UNIT_CAUCHY = STOP_SCOPED_EXACT_ENDPOINT_PRODUCT_RESONANCE
MOHAMMADI_WEIGHTED_A0_ATTACHMENT = SOURCE_BACKED_LOCAL_SUBLEMMA_EXPONENT_INSUFFICIENT
BOURGAIN_GARAEV_N3_ATTACHMENT = SOURCE_BACKED_LOCAL_SUBLEMMA_EXPONENT_INSUFFICIENT
DIRECT_LOCAL_BOX_TO_ENDPOINT_COMPILATION = STOP_SCOPED_NORMALIZATION_AND_EXPONENT_DEFICIT
STANDARD_LEVEL_OF_DISTRIBUTION_ATTACHMENT_IN_CHECKED_SOURCES = ABSENT
HB4_EXACT_HALF_ACTUAL_ATOM_DUAL_PRODUCT_DISPERSION = FIRST_SUBGATE_OPEN_NEW_THEOREM
HB4_EXACT_HALF_INDUCED_GAUSS_CRT_SIGNED_PHASE_IDENTITY = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PHYSICAL_MINUS_TWO_G_S_UNIT_PHASE = PROVED_EXACT_SOURCE_LOCK
HB4_EXACT_HALF_LITERAL_MU_GQ_PRESERVATION_THROUGH_IMPRIMITIVE_CRT = STOP_SCOPED_FALSE_EXACT_COFACTOR_SIGN_CANCELLATION
HB4_EXACT_HALF_RAMANUJAN_COFACTOR_GCD_STRATIFICATION = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PRIMITIVE_PROJECTOR_SINGLE_FIXED_PRODUCT = STOP_SCOPED_FALSE_DIVISOR_LATTICE
HB4_EXACT_HALF_RAMANUJAN_DIVISOR_MONOMIAL_UNFOLDING = PROVED_EXACT_FINITE
EARNST_ROOT_NUMBER_SQUARE_PRIME_MOMENT = SOURCE_BACKED_MECHANISM_ANALOGUE_NOT_ACTUAL_PACKET
FKMS_PRIME_MONOMIAL_TRACE_ENGINE = SOURCE_BACKED_LOCAL_ADAPTATION_BLUEPRINT
HB4_EXACT_HALF_SIGNED_MODULUS_DUAL_TYPE_IV = RETYPED_PRE_CRT_SHORTHAND_ONLY
HB4_EXACT_HALF_SIGNED_CONDUCTOR_RAMANUJAN_COFACTOR_PRIMITIVE_PROJECTOR_DUAL_TYPE_IV = SELECTED_CONSTRUCTION_OPEN_NEW_THEOREM
LARGE_D_HB2_SWITCH = PROVED_EXACT_COEFFICIENTWISE
LARGE_D_QUOTIENT_MOBIUS_GATE = SUPERSEDED
HB4xHB2_NAIVE_RESIDUE_COMPRESSION = STOP_SCOPED_ADDITIVE_DIFFERENCE_KERNEL_NORM_Q
HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI = INDEPENDENT_OPEN_NEW_THEOREM
HB4xHB2_PAIRED_VORONOI_FIRST_TRANSFORM = DERIVED_SOURCE_BACKED
HB4xHB2_COLLECTIVE_POLAR_MAIN_ATTACHMENT = OPEN_NEW_ATTACHMENT
DIRECT_DFI_ROW_BY_ROW = STOP_SCOPED_F7_VERSUS_F4
FM_J_TO_SQRT_TO_Q_PARAMETER_COMPILER = PROVED_EXACT_CONDITIONAL
FM_TO_TPC31_PRIME_MOBIUS_CORE = PROVED_FORMULA_LEVEL
FM_TO_CURRENT_PACKET_PHYSICAL_ATTACHMENT = ABSENT
ARITHMETIC_ROUTE_ADVANCE = HB4_COLLECTIVE_MAIN_PLUS_SOURCE_BACKED_OFFDIAGONAL_FOR_EVERY_FIXED_DELTA_LT_HALF
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE

不要恢复 ell_X(W)=o(a_kX)；该 target已因 critical endpoint centering在标准
HL/Mertens heuristic下错位而降级。不要把 Haar-a.e. recurrence升级到 seed 0，
不要把 post-TT-star pair/Gram逆生 linear H1，也不要把 additive covariance改写成
Ford--Maynard multiplicative Type II。

coarse comparison不得重开为 Type II：合法 `M=X^(1/3)`、
`xi_m=1_(m=1 mod6)`、`kappa_n=1_(n=1 mod6)`已给线性 mod-3反例。

下一轮只执行第 57 节控制的同一个 canonical umbrella：

TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE

当前 primary subgate为
`HB4_EXACT_HALF_ACTUAL_ATOM_DUAL_PRODUCT_DISPERSION`。先冻结 actual atom membership
与 dual-tail ledger，再对 prime `p asymp F^2`的 centered prescribed-product residue
`e_1e_2zw=-2`证明或否定 `F^(2-eta)` normalized discrepancy；其 character-angle版本
只是 exact等价坐标，二者 saving不得相乘。common-`k` unique-fiber与 global
moving-unit Cauchy已由 exact wrap/resonance identity `STOP_SCOPED`，不得重开。若 prime
gate存活时，不得再声称 squarefree CRT原样保留 literal `mu(gq)`。V10 的 full
construction必须使用 exact conductor/cofactor/projector normal form：character坐标保留
`mu(g)mu(r)epsilon_r(conjugate(psi))^2`与 physical
`psi(-2 conjugate(g)conjugate(s)^2)`；additive坐标保留
`mu(g)mu(rho)mu(b)`和
`S(1,-2u k conjugate(g e_1e_2 a b^2 t^2);rho)`。先按 large prime-like `rho`、
large complementary conductor `t`与 balanced varying/composite `rho`三段攻击
`V10-COLLECTIVE-MONOMIAL-PROJECTOR-TYPE-IV`；不得逐 `(g,rho,t,a,b)` cell取绝对值后
再认领 signed saving，也不得把 ordinary `d_4` averaged-residue theorem升级为
prescribed `-2`。Earnst与 FKMS只分别是 mechanism analogue和 local adaptation
blueprint，不是 actual packet theorem。HB4xHB2 structured two-row paired-Voronoi只作独立 reserve，
不得和 exact-half source lock拼接，也不得先压成 operator norm为 `q`的 arbitrary
additive-difference residue kernel。

对 `z=log^K X` 的同一 tensor-local hybrid，H1/H2 classical compiler已经闭合，
不得重复。合法量词始终是 target saving `-> B -> fixed K(B) -> x_0`；不得把 fixed
`K`升级为 all-`B` uniform object。direct modified-HB2 extractor、determinant range
atlas、HB4 collective main、Ramanujan axes与每个 fixed `1/4<delta<1/2`
off-diagonal均已完成，不得重复。令 `F=X^(1/4)`；下一步只攻击 exact
`D=F^2=X^(1/2)` high-conductor endpoint的真实 `log^-A X` gain，以及 exact
HB2 switch后两条 `mu_F*mu_F` rows对两条 Eisenstein columns的 `ER-AB=2`
bilateral determinant。必须保留 conductor projector、四个 literal Möbius slots、
ordered/swapped-shell exactly-once ledger与同一 collective hybrid main；不得使用
all-character大筛、把 `mu(e1)mu(e2)`压成 `mu(e1e2)`，或把 divisor convolution
冒充 smooth slot。universal U、通用 Prop. 7.22、HB2 quadratic CRT
diagonal、BC Corollary-1 direct attachment及 one-Poisson `2/7`伪 window均不得重开。
不得把 formula-level `dr-mn=2` / TPC-31 core升级为 packet attachment。若这两个
structured gates不能闭合，发布一个 broad STOP/OPEN map，不生微型论文。

并行只读 agents可分别承担 source lock、proof audit与 architecture/reassembly；
正式写入只由主控完成。两个工作包 checker为：

python research/tpc-big-road/tpc_big_road_lab.py --check
python research/tpc-big-road/tpc_big_road_independent_checker.py --check
python research/tpc-big-road/tpc_fm_local_comparison_checker.py --check

第 6 节全部旧 STOP_SCOPED cells保持；两个 O161 parents、pair-native reroute、
legacy H1与 global architecture保持 OPEN。即使一个 subgate转正也不自动创建
TPC-207；必须有真实 arithmetic theorem trigger并另过全部 provenance/physical
gates。没有 trigger时只更新 compass/handoff/unnumbered big-road artifact，不创建
paper、PDF或下一编号。
```

## 24H. 2026-08-04--05 历史粘贴块（不得作为当前入口）

```text
进入仓库：
D:\26-aimath\理论研究3\prime_dynamics_theory

读取仓库根目录 TPC_HANDOFF.md，以仓库文件和已提交 artifacts 为事实来源，
不要依赖旧聊天记录。为节省上下文，优先读取页首及第 1、6、22、24、29、30、
31、32、33、34、35、36、37、38、39、40、41、42、43、44、45、46、47、48、49、50 节；
第 23、27、28 节只在第 29--50 节明确引用时展开。

先执行：

git status --short --branch
git pull --rebase origin main
Get-Content -Raw -Encoding UTF8 TPC_HANDOFF.md

保留 git status 中全部既有 tracked/untracked 工作；不得 reset、checkout、
clean、自动 stash、删除或纳入本轮提交。当前已知 TPC-105 __pycache__、
TPC-63 构建产物、tmp/ 与本地 .codex 配置必须原样保留。若现有工作使
rebase 不安全，停止并报告。

$env:PYTHONDONTWRITEBYTECODE = "1"

完整执行第 1 节 22 项只读启动回归；任一 checker 非零即 fail closed。
TPC-27--32 legacy certificates 会无条件重写 committed JSON，在出现真正
只读 --check 入口前不得执行。TPC-122 也没有安全只读 checker，不得执行。

当前编号事实终点是 TPC-206；TPC-207 trigger=false，TPC-207 未创建。
最新不编号裁决是：

TPC32_34_H0_2_20260804_LARGE_CONTENT_ORBIT_ENERGY_AND_INPUT_COPY_Q_OVER_J2_
NEAR_BAND_CLOSED_DERIVED_L1_SMALL_FULL_V_E_EQUIVALENT_FULLY_COPRIME_FAR_COPY_
REGULAR_DISTINCT_TERMINAL_FOUR_MOBIUS_Q3_OVER_J_THEOREM_ABSENT_NO_TRIGGER_
STOP_SCOPED_PARENTS_OPEN

第 37--50 节当前登记的 source-specific cells与相邻 source/type verdict如下；
第 46 节新增第 13--15 项，第 47 节新增第 16 项，第 48 节新增第 17 项，
第 49 节新增第 18 项，第 50 节新增第 19 项：

1. Frantzikinakis--Host 1804.08556v3 与 He--Liu--Ma 2604.16840v1
   没有 O161 literal growing two-Mobius natural fixed-power theorem；
2. Ramacher--Wakatsuki 1703.06973v3、BHHM 2107.05973v3 与
   Cekic--Lefeuvre 2405.14846v2 虽含 full-group/nontrivial-K 邻近对象，
   但没有 moving noncompact level actual cloud full/cross-D0 Gram theorem；
3. RH-351 的 close/far completions 是 formal coefficient ledgers；在该 frozen
   source boundary内 actual Y 未估，不能跨程序升级；
4. RH-352 后来对 RH actual lower-even ladder证明 normalized growing theorem，
   且否定 RH-350 actual small-Y hypothesis；但其 `p=tau-a`、trace even-order
   index与 `x^(k-2)` normalization均没有 literal TPC intertwiner。该正结果只计入
   RH program；unnormalized selected prefix仍 OPEN；
5. RH-353 又对 RH actual critical/first-lower boundary证明 phase-free two-coordinate
   `Y` gap与 signed supply，但这是 switching maximum的下界，不是 saving；trace
   orders相差 `2`也不是 physical `h0=2`。direct unnormalized closure仍 OPEN，
   TPC theorem trigger不变。
6. RH-354 对 actual `p=tau-a` 证明 moving-cut以上全奇偶 trace-order的
   normalized absolute direct-tail root theorem。RH-282 source cap只对 sufficiently
   small `sigma`，故 finite-`k` boxed bound必须读成 sufficiently large `k`；
   asymptotic/root结论不受影响。这仍没有 literal TPC coefficient/index/
   `N0` map，不产生 TPC credit。
7. Watt `1302.3112v1`/`1302.3127v3` 虽有 moving Gaussian level、arbitrary
   cusp与部分 nontrivial `K`-types，其 operator是 cusp Fourier-coefficient
   spectral moment；Palm `1212.4282v1` 是 level-uniform Weyl count。两者都不是
   actual point-cloud full/cross-`D0` Gram。Namazi `2607.29319v1` 只是既有
   fixed-closed-quotient STOP 的新实例，不另起同义 method cell。
8. RH-355 无条件证明 deterministic graded counterloop 的 strict-upper absolute
   budget以 normalized root `x>1` 增长；actual Hardy-head matching却全部条件于
   未证的 same-clock `D_(4k)(R)->0`，finite complete-shell 也只属于 normal
   information class。其 trace-order coefficient、absolute band、方向和
   normalization均不能映射为 TPC distinguished zero或 small-content saving。
9. RH-356 无条件证明 post-first-alias mesoscopic crossover；RH-357 无条件证明
   complete strict-upper band的 uniform endpoint formula与 fixed
   `L/k->alpha in (0,1]` linear-depth profile。两者仍是同一 deterministic
   trace-order absolute counterloop；actual-head inheritance条件于未证
   `D_(4k)(R)->0`。它们不含 fixed physical `h0=2`、TPC three raw channels、
   canonical content/`Delta#` signed prefix、actual masks/outer labels或 `N0`，
   且 linear-depth root `x^alpha>1`是 burden而非 saving，因此无 TPC trigger。
10. RH-358 无条件证明该 complete upper band的全 terminal-lag relative-tail
    profile、geometric `ell^1`/total-variation localization与前两矩。其 `q`只是
    terminal trace lag，`P_k(q)/C_k`是 positive cumulative absolute mass；
    actual inheritance仍条件于未证 `D_(4k)(R)->0`。它没有 TPC literal
    coefficient、fixed `h0=2`、signed physical-fiber prefix、content/
    `Delta#`/matched determinant、actual metadata或 `N0`，故无 arithmetic trigger。
11. RH-359正确反演该 positive tail：logarithmic window给 model变量 `k`的
    polynomial accuracy，并保留完整 floor-phase与 minimal-width correction set。
    物理换元后 `k^(-a)`只成为 `log(1/sigma)^(-a)`，不是 `X^(-a)`；RH
    `sigma`也不是 selected packet固定 `sigma=1/10000`。没有 literal coefficient/
    `N0`/content determinant map，故即使形式取 `a=1/400`也不支付 TPC threshold。
12. RH-360 对同一 positive terminal-lag distribution 的 exponential transform
    真正证明 subcritical geometric transform、critical `1/k` Riemann-integral law、
    supercritical opposite-endpoint dominance及三种 tilted-law limits；但
    `z^r pi_k(r)`始终非负，RH `r`是 terminal lag、`z`是 artificial tilt，
    normalized free energy不是 TPC signed coefficient或 saving。actual transfer仍
    条件于未证 `D_(4k)(R)->0`；没有 fixed `h0=2`、content/`Delta#`、outer
     metadata、`A_hat_C,q_DFT(0)`、`N0`或 `chi<=1/400` theorem。
13. Schlitt `2608.00184v1` 的 Steinhaus random multiplicative periodic-BV
    CLT、prime filtration与 BDG/moment bounds是真实随机模型 theorem，但其
    single random factor、largest-prime order与 `V_g(N)` variance均不是
    deterministic two-affine Möbius sign、literal translated-integer prefixes或
    同一 `A_hat_C,q_DFT(0)`；不产生 TPC32 signed-prefix credit。
14. Alass--Saad Eddin `2608.01399v1` 只有 single Möbius factor的
    regular-integer averages；Broadbent--Fiori--Kadiri--Ng--Wilk
    `2608.01498v1` 的 “Mertens sums” 是 prime harmonic sums/products。
    二者连同 Schlitt source均不含 O161 literal growing two-affine coefficient，
    不得跨来源拼接。
15. Tiwari `2608.02405v1`、Magee--Roig-Sanchis--Thomas
    `2608.00386v1` 与 Qi `2407.17959v3` 分别给 compact graph
    discretization eigenvalue comparison、closed H3 line-bundle spectral gap与
    fixed Picard spectral Hecke-family mean；均不是 moving
     `Gamma_pm(q)\SL_2(R)` actual spatial Dirac cloud的 full/cross-`D0`
     Gram theorem，不能支付 `P_X`。
16. RH-361 commit `91167fe` 真正证明 fixed finite coefficient information
    class上的 typed fiber/nonpromotion及 RH-352--361 batch separation：
    `d=e,q=p+e,h=s+e`，fixed `p,s` 不决定 `q,h` budgets；但 arbitrary
    `e` 不构造 physical operator/determinant/asymptotic realization，actual
    `p,Y`与 deterministic counterloop `s` 仍不得 promotion。其 trace-order
    arrays不是 fixed `h0=2` 的 two-affine Möbius sign或
    `A_hat_C,q_DFT(0)`；方向是 nonpromotion而不是 saving，无 TPC trigger。
17. Angelo--Xu `2411.14447v3` 保留 random initial-bias nonnegative-prefix
    probability与 random `f(n)/sqrt(n)` almost-sure sign-change theorems；v3的
    2026-08-02 scale/CLT/second-moment/integration proof repairs是真实版本增量，
    新 Remark 3.2 也只排除 deterministic single-Liouville weighted sum最终恒正。
    random single factor或 weighted single Liouville sequence都不是 fixed `h0=2`
    的 actual two-affine Möbius coefficient、canonical fiber prefix或 matched-shell
    zero，故无 TPC trigger。
18. 第 49 节把 rough content与 `chi_theta` local masks固定移入 signed sequence、
    并把其余 actual row-pair masks留在 outer key/interval/coefficient后，仓库界真实
    给出 `ell_Z=133/400` 的 safe BV envelope；但最长 fiber exponent只有
    `10049/52500`，逐 fiber prefix + absolute outer template仍缺
    `29629/210000`。Tao `1509.05422v4`、Frantzikinakis `1606.08420v2`、
    Lichtman `2009.08969v2`、Chinis `2105.14653v1` 与既有
    Grimmelt--Teräväinen `2607.28091v1` 均在 fixed/subsequence/metric/
    prescribed-family/conditional/operator-object gate失败；Lichtman 的 natural
    shift average只有 logarithmic/`psi` saving。下一条非重复数学入口是
    TPC-33 `E_L+E_R<<X^epsilon Q^3` collective theorem或同一 `Z_C` direct bound。
19. 第 50 节把同一 literal packet的 orbit slices按
    `c_(alpha,gamma)(j)=gcd(N_alpha(j),N_gamma(j))` 切分。TPC-30 fixed-row
    occupancy与 row residue degree无条件给
    `V_>C<<X^epsilon Q^3/J`、`E_>C<<X^epsilon Q^3`，故 full/small
    `V,E` gate等价；input-copy near band
    `0<|m_(alpha_1)-m_(alpha_2)|<=Q/J^2=X^(1/400+o(1))` 也由
    Schur/row-`ell^2`闭合。fixed exact `(c1,c2)` 的 gcd/lcm CRT bound只是
    单层 incidence；对全部 contents作 absolute reassembly时，该 bound在 `(1,1)`
    退化到 `Q^3J` ceiling，但不证明 actual饱和或下界。官方 theorem-body refresh
    没有接受 complete four-Mobius
    ultra increments、two-copy content masks、linked actual family与 natural
    fixed-power normalization的 source。target collision off-diagonal严格为空，
    重跑 TPC-37 absolute degree/Cauchy proof后 `q`-singular faces继承闭合；剩余
    非重复入口是未被 identities排除的 formal eligible fully-coprime、far-copy、
    `q`-regular、distinct-terminal four-Mobius off-`V` 的 `Q^3/J` theorem；
    没有新 source cell或 TPC-207 trigger。

发布前 `ace004d..1b3513f` 的 late remote delta只修改 `RH_HANDOFF.md`：
RH completed endpoint仍为 RH-361，RH-362 source lock与独立 adversarial audit
均为 `NOT_TESTABLE`，RH-362未创建。其首缺仍是 actual same-clock
unnormalized head transport的 `D_(4k)(R)->0`；没有 theorem body、external
source或 TPC32 prefix/BV、O161、frame、pair、H1 edge。该 handoff-only delta
不新增第 6 节 method cell，也不改变本节 route priority；精确 type audit见第
48.4--48.6 节。

同一 packet 的 row-reversal 不是新 method：它在 r=0 是 sign-preserving plus
pair，并跨 distinct outer/prefix fibers。保持第 23 节既有 STOP，不得另起名字；
scalar attachment first-fatal 已由第 48 节校正；第 49 节又把 allocation-independent
BV absence校正为 `ell_Z=133/400` safe envelope present，并把真正 first fatal收缩为
逐-fiber natural-scale exact masked prefix alone无法克服 absolute outer geometry、
collective outer-return缺失。第 50 节进一步在 TPC-34 energy interface闭合
large-content tail及 `Q/J^2` input-copy near band；因此当前最窄未闭合对象是
small-content far-copy off-`V`，不是完整 `V` 的 sign-blind envelope。

同一 theorem-valid high-beta selected packet 仍固定为：
sigma=1/10000，lambda=99979/210000，delta=7/60，beta=267/400，
Q=X^(267/400+o(1))，J=X^(133/400+o(1))，C=floor(J)，h0=2，
N0=JQ^2~XQ。delta=1/20 truncated-entry family 是另一条 source lock，
绝不可拼接。

对 actual packet 必须恢复 TPC-18/21/22 的 structured residual mask：

1_{ell_alpha != ell_gamma}
1_{|m_alpha-m_gamma| > Q X^{-kappa_row}}
1_{gcd(d_alpha,d_gamma) <= X^{kappa_row}}.

kappa_row 可取任意 fixed positive value；当前 GM 条件路线要求
0<kappa_row<1/400。它不是 TPC-32 content exponent
kappa_C=133/400，也不提供 small-content saving。

TPC-32/TPC-93 已给 formula-level lossless scalar common-native source--child
reassembly：三 raw channels、both-ultra 的两个 1/2 polarizations、content、
`Delta#`、mask、weights、outer metadata 与 inverse均可在同一 scalar evaluator
中保留；这不等于 literal `Q_D/Q_Z` totality，也不 materialize full ordered
occurrence dictionaries。TPC-144 要求的 metadata-preserving `J` 仍
`STOP/NOT_TESTABLE`：both-ultra 在 determinant parent侧聚为一个 record，
在 zero side必须保留两个 L/R records；actual selected schedule是否有 nonzero
both-ultra occurrence仍 `NOT_TESTABLE`。不得把这项 scalar reassembly写成
production full-dictionary intertwiner。对 scalar `A_hat_C,q_DFT(0)` 则不需要
反演完整 determinant bins：
TPC-93 arbitrary-decoration theorem取 `F=1_(G<=C)`，配合显式 source-child
inverse，已无损给出 ordered two-affine Möbius fibers与原 global normalization，
故 scalar common-native refinement为 `PRESENT_L1`。第 49 节固定新的合法 allocation：
`mu(D)mu(U)chi 1_(G<=C)` 是 exact masked signed sequence，
`c_theta,X W_theta,X` 是 BV weight。由已提交 bounds派生的 safe envelope为
`X^(o(1))JQ^2`，即 `ell_Z=133/400`；但 exact masked prefix theorem、singleton
return、collective outer cancellation与 direct `Z_C` bound均缺。不得把这项 L1
allocation/envelope升级为 L2，也不得再把 rough cutoff jumps记入另一个 allocation后
跨 gate拼接。第 50 节的 energy split另给
`V_>C<<X^epsilon Q^3/J` 与 `E_>C<<X^epsilon Q^3`，所以 future collective
theorem可等价瞄准 `c<=C`；它仍须对 far-copy off-diagonal创造真实 signed
cancellation。

Grimmelt--Merikoski arXiv:2505.00489v2 Part I 的 exact inverse-atom
attachment 是本轮真实 L1 正结果。对

B_t=[[m,(mj+2)/G],[n,(nj+2)/G]],
H_t=2|m-n|/G，g_t=H_t^(-1/2) B_t^+ in SL2(R),

取 alpha1=sum_t conjugate(a_t) delta_(g_t^(-1))、alpha2=delta_I，
用 fixed-margin zero-Haar sign test和足够大的 auxiliary principal level，
可精确返回该 cell 的 literal physical sum。同一 row pair 的 j-arc 在
R1~1 第一槽 self-kernel 中真实逃逸；不得继续引用旧的 J/G arc 作为
这项 inverse placement 的 fatal。

但完整第一槽 self-kernel仍含 gamma=I 的 cross-row compact collisions。
所需 actual coefficient为

w_m=gamma_m^(1) gamma_(m-D0)^(2)
    A_(m,m-D0)(j) K_sh_(m,m-D0)(j),

当前必要的 fixed-`D0` reopen subtheorem 是统一控制

E_Psi=sum_(m,m') conjugate(w_m) w_m'
      Psi((m-m')/D0)

于 fixed physical h0=2、D0、G、j、actual mask、matched shell、outer labels
和 one global normalization。若 E1<=P_X sum|a_t|^2，则最坏
M>=QX^(-kappa_row) 只容许

P_X <= X^(1/400-kappa_row-epsilon+o(1)).

当前 committed corpus 与有限 official-primary screen 均没有这样的 theorem。
fixed-difference common row translations给出精确 compact collision family；
另一 `G=1` family 在 sufficiently comparable determinants 间也落入定理允许的
unit outer ball，不能由 support upper bound排除。它们证明 geometry/mask不会
自动给所需 packing，但不是 actual coefficients 大能量的算术反例。

这条 energy gate无损平方展开后是 prescribed-lag、equal-difference 的 literal
weighted four-Mobius autocorrelation。TPC-93 可无损携带 fixed `D0,G,j` 与 Fourier
phase；但每个 affine key固定 opposite row，方程
`M_theta(t)-n_theta=+/-D0` 至多有一个整数 `t`。所以 fixed-`D0` 的增长方向是
outer `theta` keys，而不是 TPC-108 的 one-column prefix。TPC-93 的 local
row-gcd/smooth projective mass为 `X^o(1)`，global fixed-`D0` transversal mass仍
`UNKNOWN`；TPC-108 H3 与 outer normalization仍未证。

第 31 节进一步把 theorem-parameter-preserving outer regroup 的整数解算完。
固定 `(L/R,ell,ell',j,sigma_aff,v,iota)`，其中
`sigma_aff=sigma_theta` 是 TPC-93 的整数 affine slope、不是 packet
`sigma=1/10000`。令 `A=ell v` 与 `g=gcd(A sigma_aff,ell')`；全部解满足

```text
t=t0+(ell'/g)z,
e=e0+(A sigma_aff/g)z.
```

actual `ell!=ell'`、`d,e~D`、`ell,ell'~L` 与 selected scale给 opposite-cofactor
步长至少 `L/2`，而 `D/L<=X^(-341/1200+o(1))`，故 sufficiently large `X`
仍至多一个点。`g=1` 时新 `z`-determinant为 `ell' h0`，已丢 fixed `h0=2`；
`g=ell'` 时 determinant保留但 occupancy仍 singleton。

唯一自然的 growing lossless coarsening是按 physical moving row `m` 使用
TPC-93 source-child inverse；它精确返回原 coefficient `w_m`，所以 `TT*` 后仍是
同一 literal weighted prescribed equal-difference four-Mobius object，不是新的
TPC-108/TPC-122 prefix。formal fixed-`D0` atomic count最多
`Q X^o=X^(267/400+o)`；actual active census未执行，joint row mask只有 entrywise
bound，故 `X^o(1)` global projective/BV cost未证。

不得用 row degree one、Parseval、large sieve、shift/origin average、裸二点相关、
logarithmic theorem或平均所有 shifts的 Chowla theorem升级。当前 first fatal 是：

LITERAL_EQUAL_DIFFERENCE_EDGE_WEIGHT_NOT_IN_ANY_SCREENED_SOURCE_THEOREM_DOMAIN.

2026-08-01 的 reproducible current-primary screen仍无 survivor。最接近的
Tao--Teräväinen 2512 theorem是 exceptional-scale two-point、只另带 small-modulus
residue-class indicator；Menon 2607
是 average-all-shifts naked k-point；Jaskari--Sachpazis fixed-k-point theorem依赖
Landau--Siegel zero；Gowers/linear-forms theorems既不接受 actual `w_m`，也不把
repeated equal-difference directions与 prescribed `D0`变成合格 finite-complexity
system。Grimmelt--Merikoski 2505.00493v2 只为 Heegner/lower-triangular application
借助 level averaging估计专用 self-kernels，不是 arbitrary literal edge theorem。

post-第 30 节 screen另核对 Carella `2202.01071v5`、Jiseong Kim
`2509.24152v1`、Diao `2506.18065v1` 与 Krishnamoorthy `2501.10962v2`。
Carella Theorem 1.1 的 displayed bound与 proof conclusion不同；Lemma 3.1 的
uniform exponentially-small residue-count error有显式反例，proof还把一般 `t`
无依据地换成 `1`，故该 source proof invalid，不能注册为 theorem input。其余
三项分别是 shift-average、metric almost-all binary forms 与 fake-Liouville/
non-extremal bias，均不接收 prescribed literal `w_m/E_Psi`。Qi
`2404.09085v3`/`2407.17711v1`、Lekkas--Voskou、Pascadi与
Hu--Petrow--Young 的大筛平均 spectral Hecke/Fourier/period data，不给 actual
dense compact cross-`D0` evaluation frame bound。

仅当新 source theorem 直接接受同一 `w_m`，或把 singleton affine children无损
regroup成 genuinely growing blocks且 global projective total variation为 `X^o(1)`，
并支付上述 tiny-power threshold、全部 ranges/constants及 physical-loss ledger时，
才重开
TPC32_H0_2_LITERAL_EQUAL_DIFFERENCE_EDGE_WEIGHT_ONE_PARAMETER_FOUR_POINT_
AUTOCORRELATION_THEOREM_GATE。该 fixed-`D0` subgate即使通过，也只允许继续
审核。comparable `D0,D0'` 的 exact `G=1` matrices仍可落在同一 GM compact
self-kernel support；没有 cross-`D0` block-Bessel/orthogonality theorem。故仍须
另行控制 cross-`D0` 与其余完整 self-kernel，并通过全部 downstream physical/
provenance gates，才可能改变 TPC-207 trigger。

RH-333/334/335 分别是连续 Gaussian probability、folded noisy/flat trace
observation map 与 fixed-order Riesz-projector cell ledger；RH-336 是 projector
mass first-alias scale及 nonphysical 3x3 row-stochastic similarity family，其中
`n=2` 是 operator power，不是 physical `h0=2`。它们均为 wrong object，不得按
同名 physical/alias/projector 符号拼接；RH-336 不单独新增 TPC STOP cell。

RH-338 是 RH frozen far set中的 boundary-orbit finite atom与 signed diffuse
compensation obstruction：`R_orb,k=-D_orb,k`，aggregate far verdict仍
`NOT_TESTABLE`。它没有 `m,m',D0,G,j,w_m,E_Psi,N0`、matched shell、determinant
或 TPC normalization；`2k` 是 orbit/operator order，不是 physical `h0=2`。
因此 `RH338_TO_TPC32_LITERAL_FIXED_D0_E_PSI=ABSENT_WRONG_OBJECT`，不新增
TPC method credit或独立 STOP cell。

最终 fetch还新增 RH-339 的 17 个 files。其 exact object是 lower sideband
`n_minus=2k-2` 上的 signed decomposition
`q_minus=-D_(k-1)_orb+C_minus`；它只证明 isolated orbit atom相对
`H_(k-1)` 发散以及 off-alias vanishing所需的 necessary compensation，完整 signed
`C_minus` 未估，vanishing/nonvanishing仍 `NOT_TESTABLE`。这里 RH 的 “physical”
仍指 Hardy full-trace boundary orbit，`2k-2` 仍是 sideband/operator order；没有
TPC literal coefficient、fixed `D0/h0=2`、matched shell、`N0` normalization或
loss ledger。因此
`RH339_TO_TPC32_LITERAL_FIXED_D0_E_PSI=ABSENT_WRONG_OBJECT`，TPC verdict与
TPC-207 trigger均不变。

第 32 节又完成三个互补的有限 refresh。natural binary-Möbius primary screen无
survivor；最接近的 KMT `2304.05344v2` 确实允许 affine syntax，而且 determinant
prime `2` 条件可用 `mu_odd` 在 literal product上无损修复，不得再以 `mu(2)=-1`
误杀。但其 truncated pretentious-distance hypothesis对 `mu_odd`失败，允许的
epsilon只产生 logarithmic而非 fixed-power output，uniform proposition只覆盖
fixed-A/polylog coefficients，并且没有 actual weights、all-prefix/BV与 `N0`
normalization crosswalk。

metric refresh的 first fatal更早：TPC-32 的 `A_hat_C,q_DFT(0)` 是 normalized
determinant变量的 finite DFT zero，TPC-170 的 `alpha` 是 fiber coordinate `z` 的
additive phase；两者没有 literal intertwiner。`q_X`、`q_prog=as` 与 `q_DFT` 必须
分开。即使反事实补上 intertwiner，named additive atom、actual cross-scale schedule、
exact bad sets与 `alpha_star notin limsup E_n` theorem仍全部缺失。

actual-census refresh则确认：TPC-205 production rows=`0`；TPC-206只是
`X=512, delta=1/4, D0=0` 的 `13/42` finite projection且
`production_occurrence=false`，与本 high-beta packet的 join被显式禁止。TPC-93
source-child inverse只在 supplied retained `omega` 上 conditional PASS；TPC-124 的
`(J Q_D-Q_Z)M=0` 没有 actual common leaf basis/matrices可执行；generic joint mask
也没有 source-backed `X^o(1)` projective theorem。不得通过 finite SVD、one-vector
equality或 atomic triangle补写。

发布前 remote又新增 RH-340（commit `eb1cf19`），但它的 exact object是 RH Hardy
trace-order 上的 `p_(sigma,k,n)=q_(sigma,k,n)-d_(sigma,k,n)` 与
`P_u/E_u/D_u` 三个 `R^n/n`-weighted absolute budgets；moving orders
`2k,2k-2` 不是 fixed physical `h0=2`。其 two-order compensation只是在
`P_(4k)->0` 假设下的必要条件，separate-absolute majorant obstruction又明确不
lower-bound fully signed prefix；aggregate signed cancellation、head与 `E_off` 仍
`NOT_TESTABLE`。没有 TPC literal coefficient、三 raw channels、`C/Delta#`、actual
masks/weights/outer labels、`N0`或 `1/400` ledger，故只新增一个有限
cross-program wrong-object STOP cell，不产生 arithmetic credit。RH-340 的
`build_result.py` 是无 `--check` 的 committed-JSON writer，不得作为只读回归执行。

最终 pull/rebase又取得 RH-341（commit `6e1478a`）。它综合 RH-332--341 后仍把
moving noisy all-order coefficient bridge、aggregate signed prefix、head、`E_off`、
physical determinant与 Gates A--E记为 OPEN/`NOT_TESTABLE`。新增的 cancelling与
noncancelling completions只是 abstract information-class ledgers，明确不是两个
physical noisy operators。这里 `q_(sigma,k,n)` 是 Hardy trace coefficient而不是
TPC modulus，`P_u/E_u/D_u`仍是 absolute trace-order budgets；moving orders相差
`2` 不能冒充 fixed physical `h0=2`。该 source没有 TPC literal coefficient、
三 raw channels、content/`Delta#`、actual masks/weights/outer labels、`N0`或
loss ledger，只新增一个有限 wrong-object/underdetermination firewall，credit仍为零。
其五个 build/verify scripts均无 `--check` 且会写 committed JSON，不得作为本轮
只读验证执行。

随后 remote commit `fd0c65e` 只把 `RH_HANDOFF.md` 的 endpoint/batch/route更新到
RH-341 与 `synchronized_actual_first_alias_signed_completion_open`。这是对既有
RH-341 release的 workflow/provenance closure，不新增 TPC literal object、packet、
theorem或 saving，也不改变上述 cross-program裁决。

第 33 节随后独立审核两个仍开放的 O161 pointwise parents。两者只共享
`c_z=mu(d+s*z)mu(u+a*z), su-ad=2` 的 abstract core；当前
production registry仍为 null/empty，没有 named atom、actual all-scale packet
record、weights/masks/outer labels与 normalization attachment。DIRECT 是
`q/N` terminal/block twist；BAD_ENDPOINT 是经 TPC-159 exact telescoping
形成的 `q/T` cumulative prefix，二者绝不可把 `N=T` 后等同。

current-primary theorem-body screen没有 survivor。el Abdalaoui--Nerurkar
`2006.07646v2` 虽给每个 fixed phase的 ordinary-prefix qualitative
convergence，但 coefficient只有一个 Möbius sign加 `mu^2` masks；
Murty--Vatwani的 rate仍作用于同一 one-sign object、fixed shifts且无 phase。
Grimmelt--Teräväinen `2607.28091v1` 的 growing-coefficient结论依赖
整盒平均；把 coefficient weight取为单 actual tuple的 delta时，
`B^k` threshold与 `delta^(-C)<=B` range使 specialization空洞。
不得跨来源拼接 phase、rate与 coefficient averaging。既有
Teräväinen--Walker/Tao--Teräväinen/Pilatte/KMT routes也仍分别卡在
logarithmic prefix、bad-scale exclusion、averaged/one-factor或 named-atom
缺口；没有 fixed `X` power与完整 ledger。

因此新 cell只冻结第 33 节逐 ID/version列出的 current-primary delta，不扩张
任何旧 STOP cell；两个 O161 parents继续 OPEN。fixed-atom credit仍为零，
strict `1/400`仍 UNPAID，`L2=NONE`。

第 34 节又审核远端 commits `65dd912`--`af5864a` 的 RH-342--348。
RH-342/343 是 spectral-root/model information objects；RH-344/346 是 RH program
内部真实 physical orbit-trace subledgers，但没有估计 signed rest；RH-345/347
只给 conditional off-balance scalar obstruction及非 physical scalar completions。
RH-348 首次把 RH physical orbit demand扩成 growing punctured lower-even ladder，
但只证明 absolute deterministic demand与 reverse-triangle必要补偿质量；actual
signed supply仍 `NOT_TESTABLE`，closure/nonclosure均未证明。
所有 route在 literal coefficient/index crosswalk先失败：RH trace order不是
translated-integer prefix，RH `q`/`sigma`/`eta`/`H_m`不是 TPC modulus/packet
parameter/additive atom/`N0` normalization；`2k-(2k-2)=2`也绝不等于 fixed
physical `h0=2`。当前 `RH_HANDOFF.md` 仍停在 RH-341，且七份 release payload
没有 source hashes/producer commit schema；这些 provenance/schema ceilings不比
literal-object fatal更早。

2026-08-03 arXiv math.NT new listing共 29 项；唯一需要 theorem-body 深查的
`2607.29429v1` 证明 random multiplicative function的 almost-sure complete-prefix
upper bound。Rademacher source明确用 independent random prime signs替换 Mobius
arithmetic prime values；因此它既不是 deterministic Mobius theorem，也没有
literal two-Mobius pair、fixed atom、packet、determinant/content、`X/N/q` ranges、
normalization或 loss ledger。有限 current-primary screen无 survivor，但这不声称
全局文献不存在。

第 35 节把有限 source screen扩到此前未冻结的 signed-prefix/automorphic
large-sieve候选与 math.DS recent。Pascadi--Thorner `2508.14888v2`、
Conrey--Kwan--Lin--Turnage-Butterbaugh `2607.00282v1`、Schmidt
`2604.23517v1`、Harper--Soundararajan--Xu `2606.29040v1` 与
Klurman--Munsch--Sun `2605.04694v1` 分别在 automorphic/character-family mean、
conditional model、random function或 freely constructed signs处先失配；没有一个
接受 actual `A_C`、literal `w_m`或 actual evaluation-cloud Gram operator。

math.DS新增 el Abdalaoui `2607.29275v1`。其最接近结论是单一
Mobius--Sarnak process weight对 singular-spectrum test的定性
`N^{-1} sum_(n<=N) omega_n a_n -> 0`；它没有
`mu(d+s*z)mu(u+a*z)`、fixed `su-ad=2`、named production atom、fixed positive
power、DIRECT `q/N`或 BAD `q/T` normalization，不能触发两个 O161 parents。

第 31.3 节已提及的 Carella `2208.12219v8` 本轮又做 proof-chain adversarial
复核：Theorem 6.2 的 `(6.7)->(6.8)` 非法在逐频率 modulus bound后保留未知
Fourier coefficients的 root-of-unity cancellation；Lemma 3.1 的 uniform
exponentially-small residue-count error被 `q=x-1,a=1` 直接反例否定；Lemma 6.2
的 `(6.24)` 又把 coprime-restricted double sum非法因子化为 unrestricted square。
故该 preprint不能作为 theorem input；这只是旧 STOP scope的证明完整性加固，
不是新 method cell。

第 36 节又沿三个未关闭 parent做了不重复回溯。O161 最强自然平均候选
Shao--Teräväinen `2006.05954v2` Corollary 11.1要求 finite complexity；实际
`L1=d+s z,L2=u+a z` 满足 `s L2-a L1=2`，是一维 parallel/twin-prime型，故在
hypothesis gate即失败。Teräväinen `1710.01195v2`虽允许 fixed affine forms，
但只有 logarithmic average、固定参数与定性 `o(1)`；Mangerel
`2306.09929v4` Remark 1.2还明确指出相应 Cesaro binary-correlation升级当前
无条件不可用。natural/wrong-domain与 logarithmic/correct-syntax sources不得拼接。

actual GM cloud的最接近 theorem是 Chamizo 1996 Theorem 2.1 的 spatial-point
large sieve；它只作用于 fixed `Gamma\\H=Gamma\\G/K`、weight zero、pairwise
`delta`-separated points，常数依赖 `Gamma`与 cusp height。Pesenson
`1104.1710`只覆盖预先设计的 `rho`-lattice，Anker--Germain--Léger
`2306.12827`只给错误 surface class上的 continuous projector。三者都不接收
moving `Gamma_pm(q)\\G` full-`K` actual Dirac cloud、full/cross-`D0` blocks与
global normalization。即使反事实投影到 Chamizo 的 spherical setting，未证的
actual separation会带来 `delta^(-2)`；相邻 common-translation atoms若同时 active，
该条件性成本约为 `|Delta#|^2`，远超 strict `1/400` budget。这不是 actual
large-energy反例，因为 simultaneous nonzero/coherence仍未证。

post-`023ccb5959e35b96673117b76add3dcbc3987aca` 的 current-ref pair/H1
delta只有三个 certificate source-hash pin更新，没有新 theorem body或 occurrence
edge。TPC-206 selected projection仍为 `13/42`，首缺字段仍是 uppercase opened
`D`；row divisor `d=1`不得改名为 `D=1`。TT-star/Cauchy pair是 quadratic carrier，
不能自动逆变为 H1 要求的 linear coefficientwise-conservative occurrence lift。
pair-native reroute与独立 pre-TT-star H1 parent均继续 OPEN。

发布前 fetch新增 RH-349/350，但它们的 literal object是 RH noisy-operator
lower-even sideband direct coefficient `p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j)`。
RH-349 对 `j=2,3`、RH-350 对 `2<=j<=J_k` 给出真实的 phase/demand scalar laws；
后者的 growing-depth physical conclusion仍明确假设未证的 aggregate `Y` remainder
趋零。RH sideband `j`、absolute residual lower bound与 `x^(-(k-2))`
normalization没有 source-backed map到 TPC arithmetic `z` prefix、fixed physical
`h0=2`、signed cancellation、`q/N`/`q/T`或 `N0`。这两个 RH sources在自身
program内不是 model-only，但跨程序 first fatal仍是 literal coefficient/index
universe mismatch；只新增一个严格锁定 commits `c548ba9`/`ecad6e7` 的
cross-program transfer cell，不把它记为 TPC method credit，也不扩张第 34 节
严格限于 RH-342--348 的旧 cell。

因此没有创建 TPC-207。合法的新入口仅为：直接证明第 50 节 literal
small-content far-copy off-`V` 的
`|V_(L,C,ne)|+|V_(R,C,ne)|<<X^epsilon Q^3/J`；TPC-33 actual collective
`E_L+E_R<<X^epsilon Q^3` theorem或等价 literal outer-return；直接接受 actual
literal coefficient的 positive-power theorem；直接控制 determinant DFT zero的 pointwise theorem；真正的
named additive atom + actual schedule + same-event avoidance theorem；同 high-beta
packet actual parent registry后再通过 full matrix intertwiner与 source-backed
`X^o(1)` projective theorem；或第 31.6 节既有 full self-kernel/cross-`D0` frame
theorem。任一 data materialization本身至多是新的 L1 gate，不自动产生 L2。

strict 1/400 仍 UNPAID，fixed-atom credit=0，L2=NONE。第 6 节全部旧
method cells保持 STOP_SCOPED；两个 O161 parents、pair-native reroute、H1 与
global architecture继续 OPEN。all-D uniformity、exactly-once physical cover、
original/global normalization、tail-failure、A/B selection、actual packet
attachment 与完整 provenance gates仍独立未过。

持续有限工作流授权仍有效，但没有当前 source-backed theorem trigger时只更新
handoff 并发布精确 STOP_SCOPED；不要创建论文、PDF、paper directory或 TPC-207。
若未来 trigger 真实发生，仍须先完成 TPC-143--206 provenance cascade、受影响
releases 重建、全链 --check、PDF build/render/visual QA，并使页首数学 trigger
发生真实 theorem-backed 状态变化。
```

## 25. 上一轮会话粘贴块（历史，仅供审计；不得作为当前入口）

```text
进入仓库：
D:\26-aimath\理论研究3\prime_dynamics_theory

读取仓库根目录 TPC_HANDOFF.md，以仓库文件而不是旧聊天记录为事实来源。
先执行：

git status --short --branch
git pull --rebase origin main

$d = "papers/tpc-206-selected-lineage-pair-registry-projection/experiments"
python "$d/build_tpc206.py" --check
python "$d/tpc206_selected_lineage_pair_registry.py" --check
python "$d/tpc206_independent_checker.py" --check

$p = "papers/tpc-205-pair-native-post-ttstar-registry-interface/experiments"
python "$p/build_tpc205.py" --check
python "$p/tpc205_pair_native_registry_interface.py" --check
python "$p/tpc205_independent_checker.py" --check

python -B papers/tpc-133-executable-native-entrance/experiments/tpc133_native_entrance.py --check
python -B papers/tpc-134-boundary-complete-dyadic-prefix-tail-archive/experiments/tpc134_branch_archive.py --check
python -B papers/tpc-135-tpc17-tpc18-block-frontier/experiments/tpc135_domain_cover_audit.py --check
python -B papers/tpc-136-complete-native-cut-archive/experiments/tpc136_cut_archive.py --check

python papers/tpc-184-bad-endpoint-literal-target-contract/experiments/tpc184_bad_endpoint_literal_target_contract.py --check
python -O -B papers/tpc-184-bad-endpoint-literal-target-contract/experiments/tpc184_bad_endpoint_literal_target_contract.py --check
python papers/tpc-189-direct-twist-literal-target-contract/experiments/tpc189_direct_twist_literal_target_contract.py --check
python -O -B papers/tpc-189-direct-twist-literal-target-contract/experiments/tpc189_direct_twist_literal_target_contract.py --check

foreach ($s in @(
  "papers/tpc-173-production-source-claim-inventory/experiments/tpc173_source_claim_inventory.py",
  "papers/tpc-174-local-occurrence-edge-witness-schema/experiments/tpc174_witness_contract.py",
  "papers/tpc-175-declared-corpus-local-edge-family/experiments/tpc175_local_edge_family.py",
  "papers/tpc-176-source-backed-coverage-gluing-audit/experiments/tpc176_coverage_gluing_audit.py",
  "papers/tpc-177-actual-active-support-vacuity-firewall/experiments/tpc177_active_support_audit.py",
  "papers/tpc-178-canonical-minimal-representation-eligibility/experiments/tpc178_representation_audit.py",
  "papers/tpc-179-h1-structural-corpus-exhaustion-integration/experiments/tpc179_h1_integration.py"
)) {
  python -O -B $s --check
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

当前编号事实终点仍是 TPC-206；TPC-207 trigger=false，TPC-207 未创建。
本轮完成
TPC18_S_EQUALS_2_NONPRIMITIVE_ENDPOINT_SOURCE_FORWARD_GATE。

TPC-18 的精确公式是
beta_I(k)=sum_{d|k,D0<d<=V}mu(d)。对h0=s=2，
Omega_2(e)=1_{D0<e<=V}-1_{D0<2e<=V}，只允许同一common k上的
beta_I(k)^2；different-k opened rows不得合并。

通用公式并不恒零：纯代数候选(D0,V,k,e)=(6,18,22,11)给
Omega_2(11)=1、beta_I(22)=-1。但它没有theorem-valid physical schedule、
具名source pair、cutoff nonzero、packet/cut locator或source-forward
occurrence，只能记为L0 formal candidate。

当前source-locked TPC-133 packet固定D0=0,V=2。虽然有10个同偶数k的
prime-source formal fibers、80 ordered/40 unordered formal pairs，但
I={1,2}，故每个偶数k都有beta_I(k)=mu(1)+mu(2)=0。source-locked
h0=2 beta-nonzero records=0，materialized source-locked h0=2 nonzero
per-k endpoint records=0。

TPC-136四张downstream maps仍空；TPC-143的2,988个actual_map_edges全空；
TPC-153的2,988个actual occurrence IDs全缺；TPC-154的8,967条edges全为
formal，theorem-backed actual provenance=0。TPC-205/206的k=24与48
不得拼接。registry新增字段=0、actual occurrence IDs=0、projection仍
13/42、field-order first missing仍是D。

TPC-18 finite certificate固定h=6,D0=6,V=18，只是exact algebraic regression，
明确prime_asymptotic_evidence=false；它不是h0=2 actual source-forward
record。stopping theorem也只对满足geometry的抽象block，在额外
tail-failure lower bound假设后给primitive A / nonprimitive B至少一个成立；
它不供应具名source-locked block或tail failure。当前没有theorem排除A或
直接选择s=2的B。
endpoint localization本身不推出剩余correlation小量。

新增且仅新增：
DECLARED_TPC18_H0_2_COMMON_K_ENDPOINT_SOURCE_FORWARD_RECORD_CORPUS_V1
=STOP_SCOPED。

保持第 6 节全部旧 cells（尤其 TPC193 V1）为 STOP_SCOPED；保持两个
O161 parents、pair-native reroute、H1 与 global architecture OPEN；
fixed-atom credit=0、strict 1/400 UNPAID、L2=NONE。

本轮pull为already up to date，没有新增primary TPC theorem source。
TPC-206/205/194、TPC-133--136、TPC-184/189 normal/optimized与
TPC-173--179 optimized全部通过。

扩展回归发现TPC-143 --check在certificate-only provenance上DRIFT：
2,988 obligations字节完全相同，12个漂移leaves只把TPC-134--136旧
raw-hash bindings从stale更新为canonical match；semantic/census/claim
字段变化为0。刷新会纯hash级联经过TPC-143--206并触及已发布release
manifests，故本次数学gate没有静默重写它。该漂移不改变零occurrence裁决，
但下一篇编号论文发布前必须完成全链provenance cascade、受影响release
重建和全部--check。
PROVENANCE_CASCADE_REFRESH_REQUIRED_BEFORE_NEXT_NUMBERED_RELEASE=YES。

无需再请求单独工作流授权。下一项有限不编号architecture gate为：
TPC18_H0_2_NONPRIMITIVE_ALTERNATIVE_SELECTION_AND_ACTUAL_PACKET_ATTACHMENT_GATE。
先source-lock theorem-valid h0=2 block与actual tail-failure input；再由
新theorem排除primitive A或直接下界s=2的B；然后才冻结同一common k、
beta_I(k)!=0、named endpoint coefficient、source pair与actual packet/cut
locator。前三关通过后才审source-forward registry、normalization和完整
physical-loss ledger。禁止formal->actual、endpoint localization->smallness。

主会话只保留结论、路线选择、阻断项和最终审核摘要；长扫描、定理原文
核查、schema exploit review、构建日志和逐页 PDF 检查交给分身；所有
正式写入由主会话协调。
```

## 26. 上一轮下一会话粘贴块（历史，仅供审计；不得作为当前入口）

```text
进入仓库：
D:\26-aimath\理论研究3\prime_dynamics_theory

读取仓库根目录 TPC_HANDOFF.md，以仓库文件而不是旧聊天记录为事实来源。
先执行：

git status --short --branch
git pull --rebase origin main
Get-Content -Raw -Encoding UTF8 TPC_HANDOFF.md

保留 git status 中全部既有 tracked/untracked 工作；不得 reset、checkout、clean、
自动 stash、删除或纳入本轮提交。当前已知 TPC-105 __pycache__、TPC-63 构建
产物和 tmp/ 必须原样保留。若这些工作使 rebase 不安全，停止并报告。

$env:PYTHONDONTWRITEBYTECODE = "1"
完整执行 TPC_HANDOFF.md 第 1 节当前列出的完整只读启动回归（现为 22 项）；
任一 checker 非零即 fail closed。TPC-27--32 legacy certificates
会无条件重写 JSON，在出现真正的只读 --check 入口前不要执行。

当前编号事实终点是 TPC-206；TPC-207 trigger=false，TPC-207 未创建。
上一轮不编号裁决是：
TPC18_H0_2_FULL_R_R_PRIMITIVE_A_TRUNCATED_ENTRY_AND_SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_ABSENT_STOP_SCOPED_NOT_REOPENED。

上一轮已纠正“ultra complement 只等于 u,v>T”的不完整说法。若
A_m,T=sum_(u<=T,u|mj+2)b_R(u)，C_m=sum_(T<u<=U0,u|mj+2)a(u)，则
full raw complement 的精确 domain 是 u,v<=U0 且 max(u,v)>T，并含三条：
A_m,T C_n、C_m A_n,T、C_m C_n。TPC-29 calibrated difference 另有两条
power-small drift legs；没有遗漏或重复的 two-drift 项。

TPC-29 关闭 content-rich selected-divisor sectors，TPC-30 关闭 large full-
target-content，TPC-31/32 把 selected packet 的唯一 hard cell 精确压缩为
A_hat_C,q(0)=small-content matched-shell auxiliary determinant zero。它不是
orbit Poisson zero；TPC-27 已关闭的 additive zero 不供应它。TPC-32 只有在
F0(A_C)<=X^(chi+o(1)), chi<=1/400 的额外 premise 下才关闭 complete matched
shell；该 premise 未证。TPC-116 的 aggregate physical saving 1/400 也不是
这个 squared-flatness loss，严禁字段等同。

上一轮 sigma=1/1000、delta=1/20 exact family 还有更早的入口 fatal：
lambda=9979/21000，R exponent=9/20，beta in
[5479/10500,1838/2625]。TPC-26/28 的 positive-minimax upper cutoff 在全部
slices 上最多只有 exponent 2/5<R；不存在 R<=S<T 且 M_beta(t)>0。
S=R 时最佳 M 仍是 -1/12。强取 T<R 会使 lambda'_R 留在 shell 中并破坏
b_R=a，不是合法修补。TPC-28 的 high-beta theorem-valid selected sample 是
另一 source lock，也只关闭一个 D-packet；不得拼接，更不排除 all-D witness。

TPC-18 row-Cauchy/energy 仍只给 XQ X^epsilon natural scale；reflected unit
fiber r=s=1 留下 ordinary two-point Mobius correlation。TPC-108 H3 仍是未证
L2。新增 Menon arXiv:2607.15574 仍是 origin-averaged、phase-uniform short
sums / shift-averaged correlations；Ramaré--
Zuniga Alterman arXiv:2603.25961 是 static LCM double sum。它们与所有复核的
logarithmic、almost-all、exceptional-scale、size-only candidates 均不提供
all-slice full r_R r_R theorem。本轮无 reopen trigger，无 TPC-207。

本轮新增的 DECLARED_TPC18_H0_2_FULL_R_R_PRIMITIVE_ULTRA_COMPLEMENT_CORPUS_V1
为 STOP_SCOPED；第6节所有旧 cells 继续 STOP_SCOPED。两个 O161 parents、
pair-native reroute、H1 与 global architecture OPEN；fixed-atom credit=0、
strict 1/400 UNPAID、L2=NONE。

本轮执行下一项有限不编号 gate：
TPC32_H0_2_SMALL_CONTENT_MATCHED_AUXILIARY_ZERO_SIGNED_PREFIX_TRANSFER_GATE。

先 source-lock TPC-28/32 的同一个 theorem-valid selected h0=2 packet、三 raw
channels、content C、canonical Delta#、actual masks/weights 与 packet natural
scale N0=JQ^2\asymp XQ；再逐式
测试 TPC-111/122 ordered signed-prefix/BV 对象能否无损映射到同一个
A_hat_C,q(0)。determinant、content、outer labels、prefix order 或 normalization
任一不一致即 fail closed。只有 source-backed growing prefix theorem 真正推出
chi<=1/400，或直接给 small-content matched-shell saving，才算 arithmetic
advance。即使 selected packet 通过，all-D uniformity、physical cover、global
normalization、tail-failure、B selection 与 actual attachment 仍须分别审核。

对任何候选 theorem 逐项核查 literal physical coefficient、固定 physical h0、
summation domain、prefix index、X/N/q 与全部参数范围、uniform constants、
normalization 和完整 physical-loss ledger。禁止 block/cumulative 强行等同、
logarithmic-to-natural 偷渡、complete-frequency mean 升级为 prescribed phase，
或把第 6 节旧 STOP_SCOPED cell 重新包装成新方法。

本 gate 即使得到 selected-packet 正面结果，也不自动创建 TPC-207。只有 all-D
uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual attachment 与完整 provenance gates 均通过，
并使页首 `TPC-207 数学 trigger` 发生真实 theorem-backed 状态变化后，才可进入
编号 release。

下一篇编号论文发布前仍必须完成 TPC-143--206 的完整 provenance cascade、
受影响 releases 重建和全链 --check；certificate-only drift 不得冒充数学触发。

主会话只保留结论、路线选择、阻断项和最终审核摘要；长扫描、定理原文
核查、schema exploit review、构建日志和逐页 PDF 检查交给分身；所有正式
写入由主会话协调。若没有真实 theorem trigger，更新本交接并 STOP_SCOPED，
不要创建论文、PDF 或下一编号。

若形成正式编号 release：再次 git pull --rebase origin main，完成 provenance
cascade、受影响 releases 重建、全链 --check、PDF 构建及逐页 render/visual QA；
只提交本轮预期文件，执行 git push origin HEAD:main，并用 git rev-parse HEAD、
git rev-parse origin/main、git ls-remote origin refs/heads/main 核对三个 hash
完全一致。若只形成 STOP_SCOPED 审计结果，也按同样
的提交、推送和三引用核对纪律发布交接记录。
```

## 27. 第 23.5 节 post-seal primary-source reopen-trigger 审计

### 27.1 冻结基线、对象与有限来源集

本轮从下列一致基线启动：

```text
HEAD = origin/main = 3c798823c313bdae1678bb46a9655bac1770f4ff
TPC_HANDOFF_SHA256_BEFORE_EDIT
  = 08ff16ad29f769163951471e19bf6c26ce9d1db24accdaa0ee172265b8167a9f
STARTUP_REGRESSION = 22/22 PASS
TPC111_124_126_127_READ_ONLY_GATE_CHECKS = 4/4 PASS
```

三个只读审核分别覆盖第 23.5 节的 actual intertwiner、direct actual-`A_C`
theorem，以及 growing signed-prefix + outer BV + content remainder 路线；三个审核
的 `files_changed=[]`。同一 selected packet、固定 `h0=2`、三 raw channels、
`C=floor(J)`、`G<=C`、`Delta#`、actual masks/weights、outer labels 与
`N0=JQ^2 asymp XQ` 均继续按第 23.1 节冻结。`delta=1/20` exact family 没有
参与，且不得与此 high-beta packet 拼接。

本轮逐 theorem 核查的有限 primary-source 集为：

1. Banks--Shparlinski, *Multiple sums with the Möbius function*,
   `arXiv:2506.08787v1`, Theorems 2.1/2.4 与第 7.6 节；该来源此前已在第
   15.3 节及 TPC-43 标记为不同对象，本轮只对第 23.5 节三个 trigger 做精确
   re-type-check；
2. Verjovsky, *Local Moments of Möbius Fourier Polynomials and the Riemann
   Hypothesis*, `arXiv:2607.25002v1`, Theorem 1.3 与 Proposition 3.2；
3. Ford--Radziwiłł, *Sign changes of the Liouville function in arithmetic
   progressions*, `arXiv:2605.03349v1`, Theorem 1；
4. Matomäki--Teräväinen, *Linnik's problem for multiplicative functions*,
   `arXiv:2605.27833v1`, Theorems 1.1/1.2 与 Corollary 1.3。

已声明 git refs 的 source-forward 核查仍没有找到 actual `Q_D/Q_Z` map。Tao--
Teräväinen natural-block/log-density、Menon origin/shift-average、Pilatte single-factor
origin-average、fixed/logarithmic Chowla、nilsequence、metric/random-family、
conditional Landau--Siegel-zero 与 static LCM 候选仍落在第 6 节既有
`STOP_SCOPED` cells；本轮没有给这些旧方法换名或扩张 scope。

### 27.2 literal-object 与 theorem-output 字段矩阵

actual target 仍是

```text
A_C(n) = S_sh(G<=C, Delta#=n),
A_hat_C,q(0) = sum_n A_C(n) = S_sh(G<=C),
F0(A_C) <= X^(chi+o(1)), chi<=1/400,
```

或同一 small-content matched shell 在 `N0` scale 上的直接 fixed-power saving。
四个候选逐项结果如下：

| 必核字段 | Banks--Shparlinski | Verjovsky | 两个 AP sign-existence sources |
|---|---|---|---|
| literal physical coefficient | `u_n1 v_n2 mu(n1 n2 n3)`；第三变量位于不可预先因子化的单一 Möbius factor 中，且两权重可分离 | 一般命题为 `sum a_n e(nt)`, `abs(a_n)<=1`；Möbius 特化只有单个 `mu(n)` | 单个 `lambda(n)` 或 squarefree `mu(n)` 的符号 |
| fixed physical `h0=2` | 没有同一 divisibility pair；冻结第三变量会落到来源明确未解决的 `H=1` binary/Chowla 型情形 | 没有 shift 参数 | 只固定 AP residue class，不固定 actual 两条 affine forms |
| domain 与 prefix index | 三区间变量上的一个 additive level set；给 complete/terminal scalar sum，不给每个 canonical prefix | contiguous Fourier index；local moment 到一个 terminal point，不给 actual ordered fibers 的 all-prefix | 只断言某阈值前存在两种符号；没有 signed sum、prefix 或 correlation quantity |
| determinant/content/outer labels | 没有 `G<=C`、`Delta#`、三 raw channels或 `(alpha,gamma,j)` keys | 全部没有 | 全部没有 |
| masks/weights 与 factor allocation | 只有两组 separable bounded weights；不能承载 actual joint pair mask 与三-channel tensor | 只有抽象 bounded coefficients；无 physical lineage | 无 actual weights、masks、factor allocation |
| `X/N/q` ranges | 文献自己的 `A,B,N,H`；short form 要求 growing `H`，不是 singleton physical shift | degree `N`、arc radius `r`、moment order `q`；该 `q` 不是 auxiliary modulus | AP modulus `q`；不得与 TPC no-wrap Fourier modulus同名偷换 |
| uniform constants | 对文献 data 的 uniformity不等于全部 actual outer fibers 的共同常数 | `C_q` 依赖 moment order；没有 actual-family local-moment input | threshold/constants只服务 sign existence，不服务 weighted sums |
| normalization | `(A+B)N(log N)^(-C)` 或相应 short sum；无 `N0` crosswalk | classical `P_N=N^(-1/2) sum mu(n)e(nt)`；无 `N0` crosswalk | 最小 sign witness scale `q^(5/2+eps)` 或 `R(mu;q)<<q^(2+eps)`；不是 shell normalization |
| physical-loss ledger | 只有 fixed-`C` log saving，无 `1/400` credit | deterministic wrapper不提供 local high-moment bound；RH-equivalent specialization不是 unconditional input | 两种符号存在允许其余项几乎全同号，故没有任何 cancellation exponent |

Banks--Shparlinski 的 arbitrary weights 不能修复首项：literal factor 是
`mu(n1 n2 n3)`，`u`、`v` 只依赖前两个变量，故其中的 `n3`-dependence 不能
由这两组 weights 消去；把第三变量冻结到 singleton 正是其第
7.6 节明确仍 out of reach 的 `H=1` 情形。即使反事实存在 literal crosswalk，
固定 `C` 的 log saving 仍是 `X^(-o(1))`，不能选择 `C=C(X)` 偷渡成 fixed
power。

Verjovsky Proposition 3.2 是确定性的 one-way implication。对任意 bounded
trigonometric polynomial，它把已知 local `B_q` 控制转成一个点值控制；它本身
不证明任何 `B_q` upper bound。把 actual `A_C` 平移、zero-pad 并归一化只能得到
一个以 same-actual-`A_C` local high moment 为前提的条件式，而该前提正是未证
算术输入。Theorem 1.3 则是 classical single-Möbius polynomial 的 RH 等价表述，
不是 actual coefficient theorem。Parseval 或 global `L2` 不能制造 distinguished
zero，也不能同时统一控制全部 canonical prefixes。

Ford--Radziwiłł Theorem 1 对 prime AP modulus 给出 `q^(5/2+eps)` 前各一个
Liouville 正、负值。Matomäki--Teräväinen Corollary 1.3 对 Möbius 给出

```text
R(mu;q) << q^2 (L(q)^100 + B(q)) <<_eps q^(2+eps),
```

即每个 reduced residue class 内各有一个 squarefree 正、负值；其一般 theorem
另带 real-character pretentious alternative。两者的 output 都是 existence，严格
弱于 signed-sum balance：一个长度 `L` 的序列即使 `L-1` 项同号、仅一项异号也
满足它们的结论。因此它们对 `F0(A_C)`、matched shell 或 growing maximal prefix
没有定量蕴含。Ford--Radziwiłł Lemma 7 中每个长度 `q` 区间正负各半的结论以
“指定 AP 截至 `N` 全部同号”的反证假设为前提，该假设随后被推翻，不能抽成
unconditional block theorem；即使保留该条件计数，它也不控制区间内部的
canonical order。Matomäki--Teräväinen 证明中的 sign-filtered convolution 是对
正、负目标分别构造的非负 representation count，两套计数没有相减，故也不产生
signed-prefix cancellation。

### 27.3 三个 reopen triggers 与完整 loss 状态

Trigger 1 首先在仓库 actual map input 处失败：

```text
TPC144 Q_D.actual_map_edges = []
TPC144 Q_Z.actual_map_edges = []
TPC144 J_QD_equals_QZ = NOT_TESTABLE
TPC144 literal_fiber_relabeling = NOT_TESTABLE
TPC155 production_witness_present = false
TPC175 qualifying_claim_count = 0
TPC175 eligible_carrier_count = 0
```

所以 `(J Q_D-Q_Z)M=0` 目前连共同 native-leaf matrix 与两组 actual maps 都无法
形成。scalar equality、一般 kernel criterion、local moment inequality或 sign
existence theorem 都不构造 metadata-preserving `J`。精确 first fatal 为：

```text
COMMON_ACTUAL_LEAF_DOMAIN_AND_LITERAL_Q_D_Q_Z_MAPS_ABSENT
```

Trigger 2 也失败。四个来源均不直接控制同一 actual `A_C`；没有同一对象的
denominator lower input，也没有

```text
F0(A_C) <= X^(chi+o(1)), chi<=1/400,
```

或 `N0` scale 上的 direct small-content matched-shell fixed-power saving。

Trigger 3 独立失败。没有候选同时给出：

```text
all actual retained ordered fibers and every canonical prefix,
uniform outer BV envelope,
content remainder with a fixed exponent,
common growing X/N/q ranges and uniform constants,
N0-to-global normalization crosswalk,
complete physical-loss ledger.
```

本轮最终 gate matrix 为：

```text
TRIGGER_1_ACTUAL_COEFFICIENTWISE_INTERTWINER = FAIL_CLOSED_ABSENT
TRIGGER_2_DIRECT_ACTUAL_A_C_OR_MATCHED_SHELL_THEOREM = FAIL_CLOSED_ABSENT
TRIGGER_3_GROWING_PREFIX_BV_CONTENT_LEDGER = FAIL_CLOSED_ABSENT

SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
H0_2_SPECIALIZATION = PASS_THEOREM_LEVEL_NOT_JSON_SERIALIZED
ACTUAL_GENERIC_PAIR_MASK_DECOMPOSITION = ABSENT
N0_TO_Q_X_SQUARED_NORMALIZATION_CROSSWALK = ABSENT
CHI_LE_1_OVER_400 = UNPAID
FIXED_ATOM_CREDIT = 0
ARITHMETIC_ADVANCE = NO
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

### 27.4 精确 STOP scope、开放父节点与发布验证

精确裁决为：

```text
TPC32_23_5_LOCAL_MOMENT_AND_AP_SIGN_EXISTENCE_TO_ACTUAL_ZERO_OR_
GROWING_PREFIX_INPUT_ABSENT_STOP_SCOPED_NOT_REOPENED
```

本轮新增且仅新增第 6 节的：

```text
DECLARED_TPC32_23_5_NAMED_PRIMARY_REOPEN_CANDIDATES_20260731_V1
  = STOP_SCOPED
```

这不是 actual intertwiner、direct `A_C` theorem 或 growing-prefix theorem 的
nonexistence claim；它只冻结第 27.1 节四个来源的已审核版本与上述 exact
crosswalk attempts。来源的新版本、真正逐 coefficient 保留全部 physical data 的
corollary，或第 23.5 节任一原始 trigger 仍可重开。两个 O161 pointwise parents、
pair-native reroute、H1 与 global architecture 继续 `OPEN`。第 6 节全部旧 cells
继续原样 `STOP_SCOPED`，尤其 TPC193 V1、common-`k` V1、tail-failure/A/B V1
与 full-`r_Rr_R` ultra-complement V1。

all-`D` uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual packet attachment 与完整 provenance gates
没有进入，更没有通过。即使第 23.5 节未来出现正面结果，也必须分别支付这些
下游 gates，才可能改变页首 TPC-207 trigger。

发布前已再次执行 22 项只读启动回归，结果为 `22/22 PASS`；TPC-111/124/
126/127 四项 gate checks 为 `4/4 PASS`。TPC-122 与 TPC-27--32 writers 均未
执行。没有创建论文、paper directory、PDF、构建日志或下一编号。根
`AGENTS.md` 已按用户明确授权合并为 RH/TPC scoped 政策，并作为只含该文件的
独立协调提交纳入；本 TPC STOP handoff 提交只含 `TPC_HANDOFF.md`。既有本地
`.codex/config.toml`、`.codex/agents/tpc-*.toml`、TPC-105 `__pycache__`、TPC-63
构建产物与 `tmp/` 仍保持 untracked，未纳入上述任一本地提交。

## 28. 2026-08-01 current-primary theorem-route 与 exact attachment 审计

### 28.1 冻结基线、目标与审计协议

本轮从下列一致基线启动：

```text
HEAD = origin/main = 5e97b52b54d33f2ec34c68efdb9737f8959a3345
TPC_HANDOFF_COMMITTED_BLOB_BEFORE_EDIT
  = 8a5b2ebf37390bcd9b92000938ab1f57c29ff8be
TPC_HANDOFF_SHA256_BEFORE_EDIT
  = b9047e39fdb11f295c8f0510bf6c3b12b24c07c079ecb1bdc4c111b96bf3ff31
STARTUP_REGRESSION = 22/22 PASS
TPC111_124_126_127_READ_ONLY_GATE_CHECKS = 4/4 PASS
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
```

protected manifest 是按 `git ls-files --others --exclude-standard` 排序后，对每个
文件记录 `path<TAB>byte_length<TAB>sha256<LF>`，再对含末尾换行的全部 rows 做
SHA256。三份独立只读审计分别承担 actual source lock/formula crosswalk、
from-actual formula-directed theorem attachment，以及 systematic current-primary
source discovery/adversarial theorem screen；三份结果均为 `files_changed=[]`，
且共同结论为 `NO_NEW_TRIGGER_CANDIDATE`。

同一 theorem-valid selected packet 精确冻结为：

```text
sigma = 1/10000
lambda = 99979/210000
delta = 7/60
beta = 267/400
Q = X^(267/400+o(1))
J = X^(133/400+o(1))
D = X^(10049/52500+o(1))
L = X^(99979/210000+o(1))
R = S = X^(23/60+o(1))
V = X^(23/120+o(1))
T = X^(193/500+o(1))
C = floor(J)
h0 = 2
N0 = J Q^2 asymp X Q
```

literal row coefficient、joint multiplier 与三 raw channels 仍分别是：

```text
gamma_alpha^(i)
  = mu(d_alpha) (log ell_alpha) omega_D^(i)(d_alpha)
    psi_L^(i)(ell_alpha/L) zeta_alpha^(i),

A_frak_(alpha,gamma)(j)
  = m_frak(alpha,gamma) Xi_(alpha,gamma)(j)
    W_(alpha,gamma)(j/J),

A_{m,T} C_n,
C_m A_{n,T},
C_m C_n,
```

并且必须保留 matched difference
`A_{m,U0}A_{n,U0}-A_{m,T}A_{n,T}`、actual masks/weights 与 outer labels。
令 `q_DFT` 表示 TPC-32 的 no-wrap auxiliary determinant-DFT modulus
（`q_DFT asymp Q`；下述 distinguished zero 的值不依赖这个 auxiliary
modulus），并令

```text
G = gcd(m_alpha j+2, m_gamma j+2),
Delta# = (m_alpha-m_gamma)/G,
A_C(n) = physical matched shell restricted by G<=C and Delta#=n,
A_hat_C,q_DFT(0) = sum_n A_C(n)
                 = small-content matched-shell auxiliary zero.
```

本轮所需 output 仍只能是

```text
F0(A_C) = |A_hat_C,q_DFT(0)|^2 / ||A_C||_2^2
        <= X^(chi+o(1)), chi<=1/400,
```

或同一对象的 robust direct form

```text
|sum_n A_C(n)|^2
  << X^(1/400-eta) sum_n |A_C(n)|^2
```

with some fixed `eta>0` and a complete physical-loss ledger。为避免与 TPC-32 的
auxiliary DFT modulus 混淆，以下把 TPC-127 的 progression modulus 记为
`q_prog=as`。TPC-127 的 complete literal pullback 是

```text
S_{xi,X}(alpha)
  = lambda(q_prog) sum_{n in N_I}
      Qcal_{a,s}(n) lambda(n-2) lambda(n)
      Wcal_{xi,X}(n) exp(-2 pi i alpha z(n)).
```

它无损保留同一 progression finite list 上的 canonical prefix 与 comparison mass；
该恒等式本身不是新的 cancellation theorem。
`delta=1/20` truncated-entry-absent family 未参与，且不得与本 packet 拼接。

### 28.2 系统检索、版本审计与有限性边界

截至 2026-08-01，一个只读 discovery station 的未归档运行日志报告：对 arXiv
`math.NT` 的 Möbius/Moebius、Liouville、Chowla、multiplicative functions、
partial sums、variation norm、shifted convolution 与 divisor correlation 查询
得到 394 条重叠 retrieval rows；按 base arXiv ID、normalized title 与 DOI 合并
后，22 条进入 title/abstract relevant set，12 条进入 theorem/main-result screen，
0 条通过 exact attachment 初筛。该站没有提交 raw retrieval roster、22/12-item
source-ID sets 或 query manifest，所以这些数字只作为一次性 process log，不是
可复算的 corpus-completeness certificate。general web 只用于 discovery；正式
判断使用 arXiv abstract/HTML/PDF 与 journal/DOI primary metadata。

另一条从 actual formula 倒推的定向审核还逐式检查了 Tao--Teräväinen
`arXiv:2512.01739v2` Theorem 3.1、Koukoulopoulos `arXiv:2605.01412v1`
Theorems 1.1/1.2 与 Pozdnyakov `arXiv:2604.23427v1` Theorem 1.8。它们未计入
前述 retrieval-pipeline counters；在没有两轨 source-ID roster 时，本节不宣称
两轨互斥，也不把 `12` 与 `3` 相加，只报告两轨合并裁决仍为 0 survivor。本节
只陈述这个明确、有日期和版本号的有限审核集，不声称不存在未发现文献、未来
版本或未来定理。

第 27 节四个 frozen sources 的官方版本历史未改变：Banks--Shparlinski
`2506.08787v1`、Verjovsky `2607.25002v1`、Ford--Radziwiłł
`2605.03349v1` 与 Matomäki--Teräväinen `2605.27833v1` 均仍为 v1；Banks--
Shparlinski 的 QJM publication 与 arXiv work 按 title/DOI 去重，官方摘要仍保留
binary obstruction。第 27 节 dated cell 因而不重开。

### 28.3 最接近来源的 formula-level 排除

1. Tao--Teräväinen `arXiv:2512.01739v2`, Theorem 3.1，确实给两点
   1-bounded multiplicative-function correlation 的小对数幂节省；Liouville
   corollary 允许 distinct affine forms，但 coefficients/moduli 只到
   `log^c N`，且只在一个小 exceptional scale set 外控制 complete terminal sum。
   它的 literal object 是 naked
   `lambda(a1 n+b1)lambda(a2 n+b2)`，没有 `Q_{a,s}`、三 channels、joint
   masks、`G<=C`、`Delta#`、outer labels、prescribed packet scale 或 all-prefix。

2. Matomäki--Radziwiłł--Shao--Tao--Teräväinen Higher Uniformity II
   `arXiv:2411.05770v2`, Theorem 1.1，具有最接近 maximal/all-subprogression 的
   syntax，但其 arithmetic coefficient 是单个 `mu(n)`，或单个近似残差
   `(Lambda-Lambda#)(n)`、`(d_k-d_k#)(n)`，对 bounded-complexity
   nilsequence，并允许 exceptional interval origins。没有 theorem 证明 actual
   complete coefficient
   `Qcal_{a,s}(n)lambda(n-2)lambda(n)Wcal_{xi,X}(n)
   exp(-2 pi i alpha z(n))` 是其同一 admissible coefficient，也没有 fixed-power
   actual-packet saving。

   在没有新增 same-object theorem/crosswalk 时，不得把第 1 项的 naked pair
   theorem 与本项的 single-factor maximal theorem 拼接：两者不是同一个 theorem
   statement，没有共同 literal coefficient、domain、exceptional set、constant、
   normalization 或 loss ledger。

3. Grimmelt--Merikoski `arXiv:2404.08502v2`, Theorem 1.1，最接近 determinant
   geometry：它计数 determinant-one matrices，允许 left-`Gamma`-automorphic
   orbit weight 与 smooth dyadically supported test weight。其 error 为
   `delta^(-O(1)) Z^epsilon sqrt(A D K R)`；当前没有 coefficientwise map 把
   actual three-channel packet、content、outer labels 与 prefix order 送入该
   automorphic object，也没有证明所得 weight 的 `Gamma` invariance。actual
   encoding 的 `K` bound、`R`/range/smoothness crosswalk 与完整 loss ledger
   均未给出，会重新引入未支付的 correlation problem。

4. Kim `arXiv:2603.23250v2`, Theorem 1.6，在 `f1 in F'_k(alpha)`、`f2,f3`
   为 `k`-divisor-bounded，且
   `X^((1+alpha)^2/((1+alpha)^2+1)+100 epsilon) << H << X^(1-epsilon)`
   时，给 Fejer-weighted ternary correlation 的 shift-average power saving；它
   不控制 prescribed physical `h0=2`，也没有 actual masks/channel attachment。

5. Cantarini `arXiv:2607.09110v1`, Theorems 22/24，虽有 fixed-power headline，
   literal coefficient 是带 modulus/character average 的 `Lambda`--`mu` additive
   convolution，且依赖 GRH 与额外 zero conjecture；它不是 actual two-affine
   Möbius joint coefficient。

6. Fragkos--Krause--Miheisi--Sun `arXiv:2607.05560v1` 是 prime Carleson
   operator 的 variation norm；Lau `arXiv:2509.07556v2` 是 generalized-divisor
   shifted convolution；Koukoulopoulos `arXiv:2605.01412v1` 是从 partial-sum
   smallness 假设推出 structure 的 inverse input；Pozdnyakov
   `arXiv:2604.23427v1` 是单 `mu` 对 digital character 的 terminal estimate；
   Chavez `arXiv:2409.02106v10` 是 RH/simple-zero 条件下的 logarithmic
   multiplicative-function-times-cumulative-sum object。它们分别首先失败于 operator/
   kernel、literal coefficient、implication direction、domain/prefix 或 cumulative
   normalization，不能产生 distinguished auxiliary zero。

7. Pilatte `arXiv:2604.26564v1` 的 single-Liouville Fourier theorem 仍平均 interval
   origins；Higher Uniformity I、Menon、Banks--Shparlinski、Verjovsky 与两个 AP
   sign-existence sources 仍由第 6、27 节原有精确 cells 管辖。本轮只做 version/
   trigger type-check，不把这些旧 `STOP_SCOPED` 方法重新包装成新方法。

所有候选均逐项核查 literal physical coefficient、固定 physical `h0`、summation
domain 与 prefix index、`X/N`、auxiliary `q_DFT` 与 progression `q_prog` 的各自
参数范围、uniform constants、normalization 与
完整 physical-loss ledger。任何一项不一致即 fail closed；没有使用 block/cumulative
强行等同、logarithmic-to-natural 转换、averaged-to-prescribed 升级或
complete-frequency-to-distinguished-zero 升级。

### 28.4 仓库 first fatal、trigger matrix 与可重开接口

仓库内部在调用任何候选 theorem 前已经出现 first fatal：

```text
TPC144 Q_D.actual_map_edges = []
TPC144 Q_Z.actual_map_edges = []
TPC144 J_QD_equals_QZ = NOT_TESTABLE
TPC144 literal_fiber_relabeling = NOT_TESTABLE
TPC155 production_witness_present = false
TPC175 qualifying_claim_count = 0
TPC175 eligible_carrier_count = 0

COMMON_ACTUAL_LEAF_DOMAIN_AND_LITERAL_Q_D_Q_Z_MAPS_ABSENT
```

TPC-124 所需的 coefficientwise `(J Q_D-Q_Z)M=0` 因而没有共同 actual leaf
domain、两组 literal maps 或 production witness。即使反事实补齐这一层，content
map、outer labels、factor allocation、prefix order、`N0` normalization、共同
ranges/constants 和完整 loss ledger 仍需逐项证明。

本轮最终 gate matrix 为：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
H0_2_SPECIALIZATION = PASS_THEOREM_LEVEL_NOT_JSON_SERIALIZED

TRIGGER_1_ACTUAL_COEFFICIENTWISE_INTERTWINER = FAIL_CLOSED_ABSENT
TRIGGER_2_DIRECT_ACTUAL_A_C_OR_MATCHED_SHELL_THEOREM = FAIL_CLOSED_ABSENT
TRIGGER_3_GROWING_PREFIX_BV_CONTENT_LEDGER = FAIL_CLOSED_ABSENT

ACTUAL_GENERIC_PAIR_MASK_DECOMPOSITION = ABSENT
N0_TO_Q_X_SQUARED_NORMALIZATION_CROSSWALK = ABSENT
CHI_LE_1_OVER_400 = UNPAID
FIXED_ATOM_CREDIT = 0
ARITHMETIC_ADVANCE = NO
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

精确裁决为：

```text
TPC32_23_5_NAMED_PRIMARY_REOPEN_CANDIDATES_20260801_TO_ACTUAL_ZERO_OR_
GROWING_PREFIX_INPUT_ABSENT_STOP_SCOPED_NOT_REOPENED
```

本轮新增且仅新增第 6 节的：

```text
DECLARED_TPC32_23_5_NAMED_PRIMARY_REOPEN_CANDIDATES_20260801_V1
  = STOP_SCOPED
```

这个 dated cell 只冻结第 6 节列出的九个 exact source versions 单独使用，或仅在
这九个 versions 之间形成的本节已审核 splices。涉及 Higher Uniformity、Pilatte
及其他旧方法的结论仍分别由第 6 节原有 cells 管辖。它不是 theorem
nonexistence claim，不阻止：

1. 保留全部 physical metadata、共同 leaf domain、order 与 mass 的 actual
   coefficientwise `Q_D/Q_Z` intertwiner；
2. 直接控制同一 `A_C` 或 small-content matched shell、并支付 strict `1/400` 的
   source-backed theorem；
3. 对同一 complete literal coefficient（包括 `Qcal_{a,s}`、
   `Wcal_{xi,X}` 与 additive phase）、同一 prescribed outer fibers 和
   generally growing progression modulus `q_prog=as` 同时给出 every canonical
   prefix、outer BV、content remainder、uniform constants/ranges、`N0`
   normalization 与完整 loss ledger 的 theorem；
4. Grimmelt--Merikoski 型 determinant route 的 exact actual automorphic encoding，
   前提是另有 source-backed `Gamma` invariance、orbit `K` bound、range/
   normalization crosswalk 与完整 loss payment。

两个 O161 pointwise parents、pair-native reroute、H1 与 global architecture 继续
`OPEN`。第 6 节全部旧 method cells 保持原样 `STOP_SCOPED`，尤其 TPC193 V1、
common-`k` V1、tail-failure/A/B V1 与 full-`r_Rr_R` ultra-complement V1。
all-`D` uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual packet attachment 与完整 provenance gates
均未进入。没有创建 TPC-207、论文、paper directory、PDF 或构建日志。

### 28.5 晚到 RH-332 source-type check 与发布边界

最终 QA 期间，`origin/main` 从
`5e97b52b54d33f2ec34c68efdb9737f8959a3345` 前进到
`d49ed98bdf294355eeded2a07eeb4f2a5f7a2dc0`。新提交只增加
`papers/RH-332-sharp-physical-repelling-return-affine-leg-remainder/` 下 17 个
files；它没有修改 `TPC_HANDOFF.md`、任何 TPC packet/provenance artifact、
`AGENTS.md` 或本轮 127 个 protected untracked paths，所以同步没有文件级重叠。
但因题名包含 physical/affine/remainder，本轮仍由两份独立只读审计使用
`git show origin/main:path` 做 theorem-output 与 exact source-lock type check。

RH-332 的 actual theorem object 是连续概率核
`mu_{sigma,a}(du)[L_sigma(u,w)-A_u(w)]dw` 的 repelling-return second-hybrid
Duhamel row remainder。它证明 sectorwise remainder 有严格正的 order-`sigma`
主项，并否定 exponential 或 `o(sigma)` hybrid accuracy。这里的 `mu_{sigma,a}`
是 probability marginal，不是 Möbius；“actual physical first-leg prefix”是
path-law prefix，不是 TPC-111/122 canonical signed prefix；`U<0/U>0` 是 repelling
orientations，不是 arithmetic siblings、三 raw channels 或 fixed `h0=2`。

逐字段 type check 为：

```text
literal TPC coefficient/native domain = ABSENT_WRONG_CONTINUOUS_OBJECT
fixed arithmetic h0=2 = ABSENT
three raw channels and joint masks = ABSENT
G<=C, Delta#, A_C and outer labels = ABSENT
ordered arithmetic all-prefix/BV/content ledger = ABSENT
N0=JQ^2 asymp XQ normalization = NO_CROSSWALK
chi<=1/400 cancellation credit = NONE
```

同名符号也不得拼接：RH-332 的 `sigma->0` 是 noise scale，不是 TPC packet 的
固定 `sigma=1/10000`；RH-332 的 dynamical multiplier
`lambda=2u_c r=1.6785...` 不是 TPC 的 `lambda=99979/210000`。RH-332 自身的
README/ledger/result firewall 又明确给出 parity/shell cancellation、full-trace
replacement、determinant gluing 与 all-cycle transport 未证，Gates A--E 全 false。
candidate-specific first fatal 是：

```text
RH332_CONTINUOUS_GAUSSIAN_HYBRID_ROW_COEFFICIENT_AND_NATIVE_DOMAIN_
NOT_EQUAL_TO_TPC28_32_DISCRETE_MOBIUS_DETERMINANT_PACKET
```

所以精确 late-source verdict 为：

```text
RH332_SHARP_PHYSICAL_REPELLING_RETURN_AFFINE_LEG_REMAINDER_IS_WRONG_
PHYSICAL_OBJECT_FOR_TPC28_32_SELECTED_PACKET_NO_23_5_TRIGGER
```

原仓库 first fatal 仍是
`COMMON_ACTUAL_LEAF_DOMAIN_AND_LITERAL_Q_D_Q_Z_MAPS_ABSENT`。三个第 23.5 节
triggers 继续 `FAIL_CLOSED_ABSENT`；`ARITHMETIC_ADVANCE=NO`、strict `1/400`
仍 `UNPAID`、`L2=NONE`、`TPC207_TRIGGER=false`、`TPC207_CREATED=false`。
该 type check 不新增或扩张任何 `STOP_SCOPED` cell；RH-332 是不同 theory object，
不是一个被停止的 TPC arithmetic method。

最终正式写入前，22 项只读启动回归再次为 `22/22 PASS`，TPC-111/124/126/127
追加 gate checks 为 `4/4 PASS`；TPC-122 与 TPC-27--32 writers 均未执行。
三份 theorem audit 和三份修订后复核均为 read-only/PASS。唯一预期 tracked diff
仍为 `TPC_HANDOFF.md`；protected untracked count 仍为 127，manifest SHA256 仍为
`35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f`。

## 29. 2026-08-01 GM inverse-atom exact attachment 与 actual cross-row energy 审计

### 29.1 冻结基线、同步与 fail-closed 协议

三份第一轮只读审计锚定：

```text
FROZEN_HEAD
  = e298266ab79cbe9a5ffcd21ed0002ba7c5c28585
FROZEN_HANDOFF_SHA256
  = c857a18f999622b2ff821e71024ad25d03a11dacb58363e5ab51b3f42add7019
```

它们分别核查 direct weighted-pair/current-primary source、TPC-32/TPC-93
common-occurrence compiler，以及 Grimmelt--Merikoski kernel geometry；
后续 exact-kernel、self-energy、compiler devil's-advocate 与 source-theorem
复核均保持 `files_changed=[]`。正式写入前同步到：

```text
HEAD = origin/main
  = 11581a2f6a583abb5780e266d56b0aed41d7884b
TPC_HANDOFF_COMMITTED_BLOB_BEFORE_EDIT
  = a1d26efe486edcabed13ce6294abfd042dc7d9ea
TPC_HANDOFF_SHA256_BEFORE_EDIT
  = c857a18f999622b2ff821e71024ad25d03a11dacb58363e5ab51b3f42add7019
STARTUP_REGRESSION_AFTER_SYNC = 22/22 PASS
TPC111_124_126_127_READ_ONLY_GATE_CHECKS = 4/4 PASS
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
```

`e298266..11581a2` 只新增 RH-334/335 各 17 个 committed files；没有修改
TPC source、handoff 或根政策。TPC-122 与 TPC-27--32 legacy writers 均未执行。
protected manifest 仍按第 28.1 节的 path/byte-length/file-SHA256 rows 定义；
本轮没有向仓库写入 discovery log、外部 PDF/source、paper directory 或 build
output；GM official PDF/source 只在 repository 外的临时目录用于只读核对。

### 29.2 actual mask 修正与 common-occurrence compiler 裁决

第 28.4 节的 `ACTUAL_GENERIC_PAIR_MASK_DECOMPOSITION=ABSENT` 只描述
TPC-32 abstract interface，不是 actual source lineage 的最终事实。TPC-18/21/22
对本 selected residual packet 实际保留：

```text
m_kappa(alpha,gamma)
  = 1_{ell_alpha != ell_gamma}
    1_{|m_alpha-m_gamma| > Q X^{-kappa_row}}
    1_{gcd(d_alpha,d_gamma) <= X^{kappa_row}}.
```

stopping theorem 允许任意 fixed `kappa_row>0`。当前条件 GM exponent ledger
必须预先取 `0<kappa_row<1/400`。这个参数只管 same-prime/near-row/large-row-gcd
removal；它不是 TPC-32 的 content exponent
`kappa_C=133/400`，也不能冒充 small-content matched-shell saving。
第 23.1、28.4 节关于 generic bounded mask 的历史句子不得再作为 actual packet
的 stronger source lock。

TPC-32 的 pointwise identity与 TPC-93 的 source-child reconstruction 确实给出
一个参数化 `L1` common-occurrence compiler：

1. 三 raw channels 精确重写为两个 polarizations；both-ultra raw leaf 产生
   `L/R` 两个 computational children，系数各 `1/2`，physical multiplicity
   总和为一；
2. 展开 opposite leg并把具体 decoration 加入 source metadata 后，每个 child
   有唯一 source inverse；
3. literal coefficients、fixed `h0=2`、`j`、actual mask/weight、content
   `G`、canonical `Delta#`、polarization、projector、interval component与
   outer provenance均可保留；
4. 在这个 constructed formal ledger 上，`Q_D` 可逐 leaf 聚回 canonical
   determinant parent，formal ordered `Q_Z` 也可按原 `(theta,t)` 顺序
   totalize。

但 TPC-144 要求的 `J` 是 output-record sets 间的 metadata-preserving
bijection，不是任意 linear split。对一个 formal both-ultra raw column，
`Q_D M` 先把两个 halves 聚成一个 determinant record，而 `Q_Z M` 必须保留
两个不同 `L/R` zero records。一个 supported output record不能由 permutation
变成两个 halves；相应 child difference 可落入 `ker Q_D` 而不落入
`ker Q_Z`。所以：

```text
PARAMETRIC_LOSSLESS_COMMON_OCCURRENCE_COMPILER = L1 GO
PARAMETRIC_QD_TOTALITY = L1 GO
FORMAL_ORDERED_QZ_TOTALITY = L1 GO
TPC144_METADATA_PRESERVING_J = STOP_SCOPED
ACTUAL_SELECTED_NONZERO_BOTH_ULTRA_OCCURRENCE = NOT_TESTABLE
PRODUCTION_INTERTWINER = NOT_TESTABLE
```

这没有给 growing signed-prefix theorem、small-content saving 或 `L2`。

### 29.3 GM2505v2 inverse-atom exact kernel：真实 L1 正接口

正式 source lock 是 Grimmelt--Merikoski,
`arXiv:2505.00489v2`, Theorem 1.1，而不是第 28 节审核的旧
`2404.08502v2` determinant-counting theorem。对一个 physical atom
`t=(alpha,gamma,j)`，令 `m=m_alpha`、`n=m_gamma`、

```text
G = gcd(mj+2,nj+2),
U = (mj+2)/G,
V = (nj+2)/G,
B_t = [[m,U],[n,V]],
det(B_t) = 2(m-n)/G.
```

按 determinant sign 分 cell并定向后，置
`H_t=2|m-n|/G`、`g_t=H_t^{-1/2}B_t^+ in SL_2(R)`。
若 `M=|m-n|`，相应 dyadic coordinate ranges 是

```text
A_GM asymp C_GM asymp Q sqrt(G/M),
D_GM asymp X/sqrt(GM),
A_GM D_GM asymp XQ/M = N0/M,
R1=A_GM/C_GM asymp 1,
R2=D_GM/C_GM asymp J/G.
```

令 `a_t` 是保留两条 opened-row signs、actual mask、fixed `h0=2`、
`j,G,Delta#`、三 raw channels的 matched tensor、smooth/periodic factors与
outer labels的 literal coefficient。GM pairing 的精确 convention 是

```text
K_F(tau1,tau2)
  = sum_{gamma in Gamma} conjugate(chi(gamma))
    F(tau1^{-1} gamma tau2),

alpha1 = sum_t conjugate(a_t) delta_{g_t^{-1}},
alpha2 = delta_I.
```

因此 identity translate恰给 `a_t F(g_t)`，无需把 `F` 换成 `F^vee`。
在每个 fixed-margin sign/coordinate cell取
`f(a,c,d)=phi(a,c,d)-phi(-a,c,d)`；Haar matrix-coordinate density
不依赖 `a`，故 `int F=0`，同时 physical sign cell上 `F(g_t)=1`。
一个 bump不能在整个闭 dyadic box恒等于一；必须先做 `O(1)` fixed-margin
partition，这只产生 soft 常数。

为避免 GM proof 中 `-I in Gamma` convention 的歧义，可使用

```text
Gamma_pm(q)
  = {gamma in SL_2(Z): gamma == plus-or-minus I (mod q)}
```

配 principal character `chi=1`，并取 `q` 大于固定常数乘
`max(D_GM^2,A_GM D_GM,A_GM C_GM)`；sign support排除 unwanted `-I`。
等价地，正式使用 literal principal `Gamma(q)` 前必须补写 theorem 对该 subgroup
的 convention extension。actual far-row bound使所需 `q` 至多 polynomial：
`q <= X^{533/400+kappa_row+o(1)}/G`。该 level选择删除所有
`gamma != plus-or-minus I` target/self-kernel translates；它不删除
`gamma=I` 的 physical cross-atom terms。

于是存在 source-backed exact identity：

```text
<alpha1 | Delta F | delta_I>
  = sum_{t in one physical cell} a_t.
```

同一 fixed `(m,n,G)` 的不同 `j,j'` 在第一槽满足
`g_j g_{j'}^{-1}=g_j n(-(j'-j)/G)g_j^{-1}`；其 normalized off-diagonal
entries规模至少 `Q^2|j-j'|/M`，故逃出 `R1 asymp 1` 的 unit support。
所以第 28 节“原始第二槽有完整 `J/G` unipotent arc”的 obstruction 对这项
inverse placement 已被真实修复；不得继续把它列为 first fatal。

若完整第一槽 self-energy满足

```text
E1 <= P_X sum_t |a_t|^2,
```

并授予其余 exact cell return，则 GM with
`X0=1,X1=1,X2=A_GM D_GM` 条件性给

```text
|cell target|
  << N0 sqrt(P_X/M) X^{o(1)}.
```

在 `M>QX^{-kappa_row}` 与 `beta=267/400` 下，为严格越过
`1-beta=133/400`，必须有某个 fixed `epsilon>0` 使

```text
P_X <= X^{1/400-kappa_row-epsilon+o(1)}.
```

当 `P_X=X^{o(1)}` 时条件 margin 是
`1/800-kappa_row/2`。这是条件路线，不是 arithmetic credit。

### 29.4 精确 cross-row compact collisions

inverse placement 只移除了 fixed-row `j`-arc，没有自动对角化完整
`alpha1` self-kernel。存在两个 source-checked exact geometry families。

第一族固定 `D0=m-n=G Delta#`、`G` 与 `j`。对整数 `k` 令

```text
m_k=m+kG,   n_k=n+kG,
U_k=U+kj,   V_k=V+kj,
tau=k/Delta#,
P_tau=[[1+tau,-tau],[tau,1-tau]].
```

当 shifted rows仍在 actual row set且
`gcd(U+kj,Delta# j)=1` 时 exact content仍为 `G`，并有

```text
B_k=P_tau B_0,
g_k g_0^{-1}=P_tau,
u_1(P_tau)=tau^2.
```

所以 `|k|<=|Delta#|/2` 的整个 algebraically admissible family位于
fixed unit ball内。actual mask给
`|Delta#|>QX^{-kappa_row}/G`，并不限制不同 determinant edges间的
共同 row translation。

第二族固定奇数 `n,j`，取偶数 `M` 且 `gcd(M,nj+2)=1`，令
`m=n+M`。此时 `G=1`、`H=2M`，且

```text
g_M g_{M'}^{-1}
 = [[sqrt(M/M'), (M'-M)/sqrt(MM')],
    [0,          sqrt(M'/M)]].
```

当 `M' asymp M` 时相对矩阵位于 fixed compact set；足够接近时落入 theorem
允许的 `u_1<1` 外包球，不能由其 support upper bound排除。这些都是
`gamma=I` terms，auxiliary level不能删除；这里没有断言 kernel必非零。

两族均没有证明 actual prime--squarefree opened rows与 literal matched
coefficients在 polynomially many points上同时 nonzero/coherent；所以本轮不声称
actual large-energy counterexample。它们精确证明的只是：atom injectivity、
near-row removal、TPC-31 row degree one、content cutoff和 GM support geometry
本身不推出所需 tiny-power packing。

### 29.5 actual equal-difference four-point theorem screen

对 fixed `D0,G,j`，定义 actual determinant-edge set

```text
E_{D0,G,j}
 = {m:
      m and m-D0 are actual opened rows,
      actual mask survives,
      gcd(mj+2,(m-D0)j+2)=G}.

w_m
 = gamma_m^(1) gamma_{m-D0}^(2)
   A_{m,m-D0}(j) K_sh_{m,m-D0}(j).
```

GM 所需的必要 subtheorem是对相应 fixed smooth kernels统一控制

```text
E_Psi
 = sum_{m,m' in E_{D0,G,j}}
   conjugate(w_m) w_m' Psi((m-m')/D0)

|E_Psi|
 <= X^{1/400-kappa_row-epsilon+o(1)}
    sum_m |w_m|^2,
```

或给出不更弱、并保留所有 literal metadata的完整 automorphic self-kernel
inequality。

这个 displayed fixed-`D0` bound只控制第一族共同 row-translation，是必要的
reopen subgate，不是完整 `E1` 的充分估计。第 29.4 节第二族让
`D0=M` 与 `D0'=M'` 一起变化，故通过本 subgate 后仍须独立控制 cross-`D0`
及其余完整 self-kernel；它不能单独触发 TPC-207。

仓库内精确 lineage audit得到：

1. TPC-34/38 定位 same-time/identity-bucket four-Mobius autocorrelation，
   但明确未证明相应 operator estimate；
2. TPC-42/48 的 Hilbert large-sieve/tiling bookkeeping不消除 coherent
   actual fiber；
3. TPC-84 把 determinant fiber打开为 literal weighted four-Mobius
   expansion，unpaired remainder仍需 cancellation；
4. TPC-95 是 shared-target/collision census与 conditional diagnostics；
5. TPC-108 的 generic affine `TT^*`/H3 是最近 analytic boundary，但 H3
   本身为未证 `L2`，且 GM collision到同一 actual signed-prefix sum的
   lossless crosswalk与 physical normalization也未提交。

有限 official-primary screen 另逐项排除了：Menon 的 naked `k`-point
shift-average、Kim 的 ternary shift-average、Tao--Teräväinen
`2512.01739v2` 的裸二点/polylog-affine/exceptional-scale terminal sum、
Higher Uniformity II 的 single-factor almost-all-origin nilsequence theorem，
以及 ordinary additive/Dirichlet large sieve、Schur/Young bounds。它们分别缺
literal `w_m`、prescribed parallelogram、matched shell/mask、fixed
`D0,G,j`、natural normalization、power threshold或 uniform loss ledger。
Grimmelt--Merikoski `2505.00489v2` 接收本轮 exact functional，但把同一个
`E_Psi` 留在 RHS self-kernel中，并不估计它。

没有 committed lossless decomposition
`w_m=sum_nu c_nu a_nu(m)`、`sum|c_nu|=X^{o(1)}`，把该对象送入任一
source theorem domain；actual generic mask也不得从 boundedness推出这种
projective decomposition。有限裁决因此是：

```text
FIRST_FATAL
  = LITERAL_EQUAL_DIFFERENCE_EDGE_WEIGHT_NOT_IN_ANY_SOURCE_THEOREM_DOMAIN

SOURCE_THEOREM_SURVIVOR = NONE_IN_FINITE_SCREEN
GLOBAL_OR_FUTURE_THEOREM_NONEXISTENCE_CLAIM = false
```

下一 exact source trigger 命名为：

```text
TPC32_H0_2_LITERAL_EQUAL_DIFFERENCE_EDGE_WEIGHT_ONE_PARAMETER_
FOUR_POINT_AUTOCORRELATION_THEOREM_GATE
```

它必须直接接受同一 `w_m`，或给出 `X^{o(1)}` projective mass的 lossless
source-backed decomposition，并逐项支付 fixed physical `h0`、summation/
lag order、`X/N/Q/D0/G/j` ranges、uniform constants、normalization、
actual mask、three-channel matched shell、outer labels与完整 physical-loss
ledger。shift/origin average、logarithmic theorem、裸 coefficient、
complete-frequency mean或 source splice均不合格。

### 29.6 RH-333/334/335 late-source type firewalls

RH-333 的 raw affine escape对象是连续 Gaussian probability event；没有
TPC determinant gluing、matched shell或 arithmetic normalization。它不触发
本 gate。

RH-334 的 exact object是 `f:[-1,1]` 到 `T=|f|:[0,1]` 的 fixed-point
folding、Gaussian backward-observable localized trace与
`hardy_full_trace_constituent`

```text
q_FT = B+S+R+P-A.
```

这里的 `B/S/R` 是 frozen observation windows的 localized defects，不是
TPC 三 raw channels；fixture `k=2,n=4` 不是 physical `h0=2`。
RH-334 自身锁定 determinant gluing、projectors/Floquet localization与 moving
asymptotics未证。它没有 `m,m',D0,G,j`、`w_m`、`E_Psi` 或 `N0` crosswalk。

RH-335 的 exact object是 rank-one noisy Riesz projector signed measure
`pi_sigma(J)=Tr(M_J E^-_sigma)` 与 fixed-order frozen-cell ledger
`C_{sigma,n}(J)`。它的 `J` 是 measurable cell，`n=2` 是 operator power，
均不是 TPC orbit `j` 或 shift `h0`；其 `3x3` fixture明确非 physical，
determinant closure、moving-order与 physical upper-exponent inputs均 open。

所以：

```text
RH333_334_335_TO_TPC32_EQUAL_DIFFERENCE_ENERGY_CROSSWALK
  = ABSENT_WRONG_OBJECT
STOP_CELL_CHANGE_FROM_RH333_334_335 = NONE
TPC207_TRIGGER_FROM_RH333_334_335 = false
```

这些 type checks只建立对象防火墙；不把 RH methods列为被停止的 TPC arithmetic
methods，也不得按同名 `sigma/lambda/physical/alias/projector` 符号拼接。

### 29.7 最终裁决、reopen interface 与发布边界

本轮精确裁决为：

```text
TPC32_H0_2_GM2505_INVERSE_ATOM_EXACT_KERNEL_TO_LITERAL_EQUAL_DIFFERENCE_
FOUR_POINT_ENERGY_INPUT_ABSENT_STOP_SCOPED_NOT_REOPENED
```

状态矩阵是：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
ACTUAL_STRUCTURED_RESIDUAL_MASK_SOURCE_LOCK = PASS
PARAMETRIC_COMMON_OCCURRENCE_COMPILER = L1 GO
TPC144_METADATA_PRESERVING_J = STOP_SCOPED

GM2505V2_INVERSE_PAIRING = L1 GO
ATOMWISE_DETERMINANT_NORMALIZATION = L1 GO
ZERO_HAAR_FIXED_MARGIN_TEST = L1 GO
AUXILIARY_LEVEL_TRANSLATE_ISOLATION = L1 GO_WITH_SUBGROUP_CONVENTION
FIXED_ROW_J_ARC_ESCAPE = L1 GO

ACTUAL_CROSS_ROW_COMPACT_SELF_KERNEL_BOUND = ABSENT
LITERAL_EQUAL_DIFFERENCE_FOUR_POINT_SOURCE_THEOREM = NONE_IN_FINITE_SCREEN
P_X_LE_X_TO_1_OVER_400_MINUS_KAPPA_MINUS_EPSILON = UNPAID

ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节新增的两个 cells 只冻结本轮 exact compiler upgrade和
GM2505v2 Part-I-to-current-energy inference；`L1 GO` interfaces、未来
source theorem与独立 architectures均保持可重开。第 6 节所有旧 cells继续
原 scope `STOP_SCOPED`，尤其 TPC193 V1、common-`k` V1、tail-failure/A/B V1
与 full-`r_Rr_R` ultra-complement V1。不得把本轮 GM geometry重新包装为
TPC-34/84/95/108 arithmetic theorem。

两个 O161 pointwise parents、pair-native reroute、H1 与 global architecture
继续 `OPEN`。all-`D` uniformity、exactly-once physical cover、original/global
normalization、tail-failure、A/B selection、actual packet attachment与完整
provenance gates均未进入。

没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入只修改
`TPC_HANDOFF.md`；既有 `.codex/config.toml`、四个
`.codex/agents/tpc-*.toml`、TPC-105 `__pycache__`、TPC-63 build artifacts与
`tmp/` 仍为 protected untracked。发布前 22 项只读启动回归为
`22/22 PASS`，TPC-111/124/126/127为 `4/4 PASS`；TPC-122 与 legacy writers
未执行。上述 one-parameter four-point source theorem即使通过，也只重开
下一轮 exact audit；还须控制 cross-`D0`/其余完整 self-kernel，并分别通过
all-`D` uniformity、physical cover/normalization、tail-failure、A/B、actual
attachment与完整 provenance gates。只有所有门槛共同产生真实 theorem-backed
状态变化，或其他独立 architecture 支付同等完整账本后，才允许进入 TPC-207
provenance cascade。

## 30. 2026-08-01 literal fixed-`D0` four-point transfer 与 full-self-kernel 审计

### 30.1 冻结基线、对象与必要子门

本轮启动先执行根 `AGENTS.md` 与第 1 节协议。初始只读快照为：

```text
HEAD = origin/main
     = 33e3073fef6bfb021e3479d2acf8cf6ad75daee6

TPC_HANDOFF_SHA256
     = 51562f27288cc114dbe8da7a9baab36659a4e929010c9f2849d40638097fcfca

PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
     = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f

TRACKED_WORKTREE_DIFF = empty
CACHED_DIFF = empty
STARTUP_REGRESSION = 22/22 PASS
```

相对上一份 handoff commit `d3702b2e92cf85c48c5024758c5293357b2b347f`，
本轮 `git pull --rebase origin main` 只 fast-forward 到 RH-336 commit
`33e3073fef6bfb021e3479d2acf8cf6ad75daee6`。它没有修改本轮 TPC source locks。

同一 theorem-valid selected packet继续严格固定为：

```text
sigma=1/10000
lambda=99979/210000
delta=7/60
beta=267/400
Q=X^(267/400+o(1))
J=X^(133/400+o(1))
C=floor(J)
h0=2
N0=JQ^2 asymp XQ
0<kappa_row<1/400
```

对 fixed physical `D0 != 0`、`G <= C`、`j asymp J` 与全部 actual outer
labels，literal edge coefficient仍是

```text
w_m
 = gamma_m^(1) gamma_(m-D0)^(2)
   A_(m,m-D0)(j) K_sh_(m,m-D0)(j),
```

其中 actual mask逐字保留

```text
1_{ell_m != ell_(m-D0)}
1_{|D0| > Q X^(-kappa_row)}
1_{gcd(d_m,d_(m-D0)) <= X^(kappa_row)},
```

并保留 three raw channels、两条 `1/2` polarizations、matched cutoff、content
`G`、canonical `Delta#=D0/G`、residue/smooth factors、row orientations与 parent
provenance。GM inverse route当前必要但不充分的 fixed-`D0` 子门仍为

```text
E_Psi
 = sum_(m,m') conjugate(w_m) w_m' Psi((m-m')/D0),

|E_Psi|
 <= X^(1/400-kappa_row-epsilon+o(1)) sum_m |w_m|^2.
```

### 30.2 exact autocorrelation 与 TPC-93 singleton-transversal 裁决

令 `k=m-m'`。无损重排给出

```text
E_Psi = sum_k Psi(k/D0) C_(D0,G,j)(k),

C_(D0,G,j)(k)
 = sum_{m,m-k in E_(D0,G,j)} conjugate(w_m) w_(m-k).
```

打开两个 matched shells 后有四个 cutoff cells `(Y,Y') in {U0,T}^2`，总
cutoff variation为 `4`。用 TPC-32 的 primitive sign fusion逐腿合并，exact
arithmetic sign为

```text
mu(d_m u)
mu(d_(m-D0) v)
mu(d_(m-k) u')
mu(d_(m-k-D0) v').
```

四个 `w_R` divisor weights、prime logarithms、两条 edge masks、两个 exact
content条件、target divisibility、conjugation order、physical phases与全部 outer
metadata仍在。因此它的最早诚实算术描述是 prescribed-lag equal-difference
opened-row parallelogram上的 literal weighted four-Mobius autocorrelation；不是
naked Chowla sum。

TPC-93 的 decorated source-child map可把 fixed `D0,G,j` indicator、Fourier
phase与全部 provenance无损带入 affine ledger，故 representation level仍是
`L1 GO`。但每个 TPC-93 affine key `theta` 固定 opposite row `n_theta`，moving row为

```text
M_theta(t)
 = ell_theta v_theta (d_theta + sigma_theta t).
```

fixed ordered difference要求

```text
M_theta(t)-n_theta = D0
```

或在相反 orientation取 `-D0`。由于 slope
`ell_theta v_theta sigma_theta != 0`，每个 affine column至多有一个整数 `t`：

```text
FIXED_D0_SLICE_PER_TPC93_AFFINE_COLUMN = CARDINALITY_AT_MOST_ONE
FIXED_D0_GROWING_DIRECTION = OUTER_THETA_KEYS
```

所以 fixed-`D0` energy是 singleton affine children 的 outer transversal；它不是
TPC-108 one-resolved-block 内的 growing prefix。TPC-108 exact `TT*` 只给四符号
identity；H3、outer mass、physical `TT*` return与 endpoint normalization均仍是
未证 premise。

当前精确 projective ledger是：

```text
Psi Fourier kernel mass                    = O_Psi(1)
matched-shell cutoff variation after square = 4
row-gcd projector mass per affine column    = X^o(1)
smooth/fixed-period local separation        = X^o(1)
source-child inverse                        = exact

GLOBAL_FIXED_D0_OUTER_TRANSVERSAL_PROJECTIVE_MASS = UNKNOWN
```

因此不得把 columnwise `X^o(1)` 绝对求和成 global projective decomposition。

### 30.3 current-primary theorem screen

按 ARS bibliography/source-verification protocol只用 official primary theorem
bodies进行可复现有限检索，并对 literal coefficient、fixed physical `h0`、
summation/prefix order、`X/N/q` ranges、uniform constants、normalization与完整
physical-loss ledger逐项审核。最接近来源均在 exponent accounting前失败：

1. Tao--Teräväinen `arXiv:2512.01739v2`, Theorem 3.1给 natural-average
   two-point multiplicative correlation，并只另允许一个 small-modulus residue-class
   indicator，但排除小 logarithmic-density scale set；它不是四点
   `conjugate(w_m)w_m'`，也不接受 arbitrary actual mask/shell；
2. Menon `arXiv:2607.15574v1`, Theorem 1.5给 naked Liouville `k`-point bound，
   但平均全部 `h_2,...,h_k`，不能限制到 prescribed equal-difference slice；
3. Jaskari--Sachpazis `arXiv:2409.10663v3`, Theorem 1.1最接近 fixed
   `k`-point quantifier，但依赖 Landau--Siegel zero，且仍是 naked Liouville、
   fixed-shift constants与错误 `q/x` range；
4. Tao--Teräväinen `2107.02158v4`、Leng `2212.09635v3` 与
   Klurman--Mangerel `1708.03176v1` 控制 single-factor Gowers norms或
   nondegenerate affine systems；forms
   `(m,m-D0,m-k,m-k-D0)` 含两对 repeated linear directions，global Gowers
   average不控制 prescribed `D0` slice，且 actual `w_m` 不在 theorem domain；
5. Lichtman--Teräväinen `2111.08912v3` 只平均一个 independent shift；本对象
   同时移动 linked pair `(k,k+D0)`，不能由 all-but-exceptional-shifts结论升级；
6. Higher Uniformity II `2411.05770v2` 的 main theorem是 single arithmetic
   factor against nilsequences、almost-all origins；其 derived Gowers estimates仍
   average全部 increments且仍为 almost-all-origin。Kim `2603.23250v2` 是
   ternary/shift-average；两者均不接受 literal edge sequence或 prescribed
   physical phase；
7. ordinary Schur/Young、additive/Dirichlet large sieve与 Fourier/Mellin identity
   只给 coefficient-blind density、frequency average或 exact square representation，
   不给 distinguished physical kernel cancellation。

有限检索没有找到 source-backed decomposition

```text
w_m = sum_nu c_nu a_nu(m),
sum_nu |c_nu| = X^o(1),
```

使每个 `a_nu` 真正进入同一个适用 theorem domain，并精确重建 determinant、
content、mask、shell、outer labels与 global normalization。故第一 fatal保持：

```text
FIRST_FATAL
 = LITERAL_EQUAL_DIFFERENCE_EDGE_WEIGHT_NOT_IN_ANY_SCREENED_SOURCE_
   THEOREM_DOMAIN

SOURCE_THEOREM_SURVIVOR = NONE_IN_REPRODUCIBLE_FINITE_SCREEN
GLOBAL_OR_FUTURE_THEOREM_NONEXISTENCE_CLAIM = false
```

### 30.4 GM application 与 coefficient-blind loss ledger

Grimmelt--Merikoski `arXiv:2505.00493v2` 是 Part I 的正式 application，但其
Type I/II theorems估计的是 roots of `a ell^2+h mod k` 的 distribution。其
self-kernel inputs是 exact Heegner-point functional与 exact lower-triangular
functional；application用 level `d/q` averaging、sparse diagonal和 off-diagonal
divisor absorption。论文还明确在新 short kernel ranges无法证明 cancellation，
而由 positivity丢弃 subtracted integral。

这不是接受 arbitrary actual `w_m` 的 self-kernel theorem，也不把 TPC compact
cross-row collisions变成 application的 sparse diagonal。不得把 Type I/II 中
bounded `alpha_m,beta_n` 的外层 sieve coefficients改名为本轮 automorphic
functional coefficients。

独立的 coefficient-blind检查也无法靠近 endpoint。fixed `(D0,G,j)` block内，
`G | mj+2` 且 primitive support使 `j` 在 `G` 上可逆，所以所有 `m` 落在一个
mod-`G` residue class。Schur/Young至多给

```text
|E_Psi| << (1+|D0|/G) sum_m |w_m|^2
        = (1+|Delta#|) sum_m |w_m|^2.
```

而 actual row-gap 与 `G<=J` 给

```text
|Delta#|
 > Q X^(-kappa_row)/J
 = X^(134/400-kappa_row+o(1)).
```

目标 factor是 `X^(1/400-kappa_row-epsilon+o(1))`，故即使最大 content也差
`X^(133/400+epsilon)`；`G=1` 时差 `X^(266/400+epsilon)`。在这一
coefficient-blind route 后乘任何 published logarithmic/doubly-logarithmic
naked decay仍不能支付 polynomial ledger。这里不是声明所有未来 arithmetic
theorems不可能达到目标；只冻结本轮 direct standard transfer。

### 30.5 full self-kernel、RH-336 与独立第二 fatal

fixed-`D0` 子门即使未来通过，也不控制完整 GM first self-energy。对 exact
`G=1` family、fixed odd `n,j` 与 `m=n+M`，第 29.4 节的相对矩阵精确为

```text
g_M g_(M')^(-1)
 = [[sqrt(M/M'), (M'-M)/sqrt(MM')],
    [0,           sqrt(M'/M)]],

u_1(g_M g_(M')^(-1))
 = (M'-M)^2/(2MM').
```

若 `M'/M in [1/2,2]`，则 `u_1<=1/4`，所以 comparable cross-`D0` blocks可同时
落在 GM unit compact self-kernel support。它不证明 actual literal coefficients
在这些点 coherent/nonzero，因而不是 large-energy arithmetic counterexample；
它严格排除仅靠 dyadic `D0` geometry声称 block orthogonality。

因此第二独立 fatal是：

```text
SECOND_FATAL
 = FIXED_D0_BLOCK_CONTROL_DOES_NOT_CONTROL_CROSS_D0_GM_SELF_KERNEL

CROSS_D0_BLOCK_BESSEL_OR_ALMOST_ORTHOGONALITY_THEOREM = ABSENT
```

应用 fixed-`D0` theorem后按 differences triangle/Cauchy重组，最多引入
`Q^(1/2)=X^(267/800+o(1))` 未支付 linear loss；dyadic grouping不消除同一
dyadic block内的 dense compact interactions。

本轮 pull新增的 RH-336 只处理 projector mass `pi_sigma(J)`、moving operator
order、nonphysical `3x3` positive row-stochastic similarity family与 fixed fixture
`n=2`。其中 `n=2` 是 operator power，不是 TPC physical `h0=2`；该 artifact没有
`m,m',D0,G,j,w_m,E_Psi,N0`、matched shell或 TPC normalization crosswalk：

```text
RH336_TO_TPC32_FIXED_D0_OR_FULL_E1 = ABSENT_WRONG_OBJECT
TPC207_TRIGGER_FROM_RH336 = false
STOP_CELL_CHANGE_FROM_RH336 = NONE
```

最终发布前 rebase 到 `90a25186d5cfd5e541a739e599edfdd797ea48ba` 时，上游只在
RH-336 的 13 个文件中把 `kappa_proj>gamma_star_RH325` 从 decimal diagnostic
强化为 exact rational certificate。这里的两个指数属于 RH projector-gauge 与
Duhamel stability clock；它们不支付 TPC 的 `kappa_row<1/400`、literal
fixed-`D0` energy 或 full self-kernel。三份独立只读 type review 均确认本节
wrong-object 裁决与 TPC-207 trigger 不变。

随后上游 `a7e7c6be880542cdd07614eb11a6af7abf5fa846` 只新增 RH-337 的 17 个
files。该 paper 研究 RH-329 的 `Lambda_hat/lambda` algebraic clock drift、moving
order `k`、parity/alias scalars 与 comparator defect `D_k`；它明示 `D_k` 不是
actual five-slot coefficient 或 full-trace residual，correct-clock remainder仍为
`NOT_TESTABLE`。RH 的 fixed phase、shell、`D_k` 与 `H_k` 分别不是 TPC 的 fixed
physical `h0=2`、matched divisor shell、row difference `D0` 与 natural scale
`N0`，也没有 literal coefficient、normalization 或 loss-ledger crosswalk：

```text
RH337_TO_TPC32_FIXED_D0_OR_FULL_E1 = ABSENT_WRONG_OBJECT
TPC207_TRIGGER_FROM_RH337 = false
STOP_CELL_CHANGE_FROM_RH337 = NONE
```

### 30.6 最终裁决、STOP scope 与合法 reopen interface

本轮精确裁决为：

```text
TPC32_H0_2_LITERAL_EQUAL_DIFFERENCE_FIXED_D0_TPC93_AFFINE_CHILD_
TRANSVERSAL_SINGLETON_COHERENT_OUTER_FOUR_POINT_THEOREM_ABSENT_
STOP_SCOPED_NOT_REOPENED
```

状态矩阵是：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
ACTUAL_W_M_AND_E_PSI_SOURCE_LOCK = PASS
TPC93_DECORATED_REINDEXING = L1 GO
FIXED_D0_SLICE_PER_AFFINE_COLUMN = CARDINALITY_AT_MOST_ONE
FIXED_D0_GROWING_DIRECTION = OUTER_THETA_KEYS
GLOBAL_FIXED_D0_TRANSVERSAL_PROJECTIVE_MASS = UNKNOWN
TPC108_H3_AND_OUTER_NORMALIZATION = UNPROVED

CURRENT_PRIMARY_LITERAL_WEIGHT_THEOREM = NONE_IN_FINITE_SCREEN
GM2505_APPLICATION_TO_LITERAL_W_M = DOMAIN_MISMATCH
P_X_LE_X_TO_1_OVER_400_MINUS_KAPPA_MINUS_EPSILON = UNPAID
CROSS_D0_BLOCK_BESSEL = ABSENT
FULL_E1 = UNCONTROLLED

ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节新增

```text
DECLARED_TPC32_LITERAL_FIXED_D0_FOURPOINT_STANDARD_TRANSFER_
AND_CROSS_D0_ORTHOGONALITY_CORPUS_V1 = STOP_SCOPED
```

只冻结第 30.3--30.5 节列明的有限 primary/current TPC/standard-transfer corpus。
它不停止以下合法 trigger：

1. 一个 source theorem直接接受同一 literal `w_m`，统一控制 fixed
   `(D0,G,j,h0=2)` `E_Psi`，保留 actual mask/content/shell/outer labels，并支付
   strict endpoint与全部 ranges/constants/normalization；
2. 一个 source-backed exact regrouping，把 singleton TPC-93 children组成
   genuinely growing theorem blocks，global projective total variation为 `X^o(1)`，
   再由适用 theorem支付同一完整 ledger；
3. 一个直接控制全部 `(D0,G,j,outer labels)` 的 literal full automorphic
   self-kernel theorem；或在 1/2 之后另有 cross-`D0` block-Bessel theorem，使
   combined total exponent仍严格通过 `1/400`。

仅通过 fixed-`D0` 子门只允许重开 cross-`D0`/full-`E1` 审核，不改变
TPC-207 trigger。此后仍须分别通过 all-`D` uniformity、exactly-once physical
cover、original/global normalization、tail-failure、A/B selection、actual packet
attachment与完整 provenance cascade。

第 6 节全部旧 cells保持原 scope `STOP_SCOPED`，尤其 TPC193 V1、common-`k`
V1、tail-failure/A/B V1 与 full-`r_Rr_R` ultra-complement V1。两个 O161
pointwise parents、pair-native reroute、H1 与 global architecture继续 `OPEN`。

### 30.7 发布边界

没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入只允许
`TPC_HANDOFF.md`；既有 `.codex/config.toml`、四个
`.codex/agents/tpc-*.toml`、TPC-105 `__pycache__`、TPC-63 build artifacts与
`tmp/` 均继续作为 protected untracked，不得纳入本轮提交。

本轮只读启动回归与正式写入后的发布前复跑均为 `22/22 PASS`；
TPC-111/124/126/127 supplemental checks为 `4/4 PASS`。TPC-122 与 legacy
TPC-27--32 writers均未执行。发布前 protected untracked仍为 `127` 个，按
`path<TAB>byte_length<TAB>sha256<LF>` rows 计算的 manifest SHA256仍为
`35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f`。

```text
FINAL_SYNC_ORIGIN_MAIN
  = a7e7c6be880542cdd07614eb11a6af7abf5fa846
FINAL_SYNC_DELTA_FROM_INITIAL_33E3073
  = RH336_STRENGTHENING_13_FILES_PLUS_RH337_NEW_17_FILES
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
FINAL_SYNC_TPC_VERDICT_CHANGE = NONE
```

只提交 `TPC_HANDOFF.md`，再 rebase/push并验证 local `HEAD`、`origin/main` 与
remote `refs/heads/main` 三个 hash一致。

## 31. TPC32 fixed-`D0` outer-regroup / post-§30 direct-and-frame finite gate

### 31.1 source lock、协议与只读基线

本轮从仓库事实重新启动，不把旧聊天当作证明来源。启动时：

```text
INITIAL_HEAD = e1c06611cbf9cb23698c6be3d9244526021f8c1f
INITIAL_ORIGIN_MAIN = e1c06611cbf9cb23698c6be3d9244526021f8c1f
INITIAL_HANDOFF_SHA256
  = 8edee5dc3aebf6cf7ae65f039395f8b5a485a7b2767e8959659658637984ed46
INITIAL_TRACKED_DIFF = EMPTY
INITIAL_CACHED_DIFF = EMPTY
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
STARTUP_REGRESSION = 22/22 PASS
TPC93_LITERAL_EXPORT_READ_ONLY_REGRESSION = PASS
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

启动时的 `git pull --rebase origin main` 新增的唯一上游对象是 RH-338 的 17 个文件；
它没有改动 TPC papers、TPC checkers或本 handoff。仍 source-lock 第 28/32 节
同一个 theorem-valid selected packet：

```text
sigma = 1/10000
lambda = 99979/210000
delta = 7/60
beta = 267/400
Q = X^(267/400+o(1))
J = X^(133/400+o(1))
C = floor(J)
h0 = 2
N0 = J Q^2 asymp X Q
0 < kappa_row < 1/400
```

literal edge与必要 fixed-`D0` gate保持：

```text
w_m = gamma_m^(1) gamma_(m-D0)^(2)
      A_(m,m-D0)(j) K_sh_(m,m-D0)(j),

E_Psi = sum_(m,m') conjugate(w_m) w_(m')
        Psi((m-m')/D0),

|E_Psi| <= X^(1/400-kappa_row-epsilon+o(1)) sum_m |w_m|^2.
```

三条 raw channels、content cutoff、canonical `Delta#`、actual masks/weights、
matched shell、outer labels与 `N0` 均未被删除或平均化。

### 31.2 exact outer-regroup 二分法

TPC-93 child 的固定 theorem key为

```text
theta = (L,gamma,ell,j,sigma_aff,v,iota),   gamma=(ell',e),
M_theta(t) = ell v(d_theta+sigma_aff t),    n_theta=ell' e,
sigma_aff := sigma_theta in Z_(>0).
```

这里 `sigma_aff` 是 TPC-93 provenance key中的 affine slope，绝不是 selected
packet的 real parameter `sigma=1/10000`。

记 `A=ell v`。固定 physical row difference `D0` 等价于

```text
A sigma_aff t - ell' e = D0 - A d_theta.
```

若固定 theorem 参数 `(L/R,ell,ell',j,sigma_aff,v,iota)`，令
`g=gcd(A sigma_aff,ell')`，全部整数解只能沿

```text
t = t0 + (ell'/g) z,
e = e0 + (A sigma_aff/g) z
```

移动。actual packet 有 `ell != ell'`、`v|d,e`、`d,e asymp D`、
`ell,ell' asymp L`，故 `ell'` 是素数且 `g` 只能为 `1` 或 `ell'`。若
`g=1`，opposite-cofactor step是 `A sigma_aff >= L/2`；若 `g=ell'`，由
`ell'` 不整除 `ell v` 可知 `ell'|sigma_aff`，故 step
`A sigma_aff/ell' >= L/2`。同时

```text
R = X^(23/60+o(1)),
D <= X^(23/120+o(1)),
L = Q/D >= X^(571/1200+o(1)),
D/L <= X^(-341/1200+o(1)).
```

因此足够大 `X` 时，固定 theorem-key block 对 fixed `D0` 的 actual occupancy
至多为 `1`。若 `g=1`，新的 `z`-determinant 是 `ell' h0`，不再是 physical
`h0=2`；若 `g=ell'`，determinant虽保留为 `h0`，block仍是 singleton。

```text
ATTEMPT_A_THEOREM_PARAMETER_PRESERVING_REGROUP = OCCUPANCY_AT_MOST_ONE
ATTEMPT_A_GROWING_SIGNED_PREFIX = ABSENT
```

唯一自然的 growing coarsening 是按 physical moving row `m`，通过
source-child inverse 合并全部 `p in P_m`。但 coefficientwise exact identity 是

```text
sum_(p in P_m) a_p = w_m.
```

所以该 regroup无损，却精确返回原 literal four-Möbius coefficient；其 `TT*`
仍是同一个 `E_Psi`，并没有变成 TPC-108/TPC-111/TPC-122 的 fixed-`theta`
ordered prefix：

```text
ATTEMPT_B_SOURCE_CHILD_TO_M_REGROUP = EXACT
ATTEMPT_B_REGROUPED_COEFFICIENT = EXACT_LITERAL_W_M
ATTEMPT_B_NEW_THEOREM_DOMAIN = NONE
```

固定 `D0` 的 formal atomic-key count至多为
`Q X^o = X^(267/400+o(1))`。TPC-84只给 census protocol，未执行 actual
active census；允许的 multipliers可以消失或缩放。因此不能把 formal count写成
actual growing-support lower bound。joint row mask只有 entrywise bound，TPC-32
与 prime-Möbius mask boundary明示没有 generic controlled projective/Schur
decomposition。现有可证状态只有：

```text
ACTUAL_GROWING_SUPPORT = CANNOT_BE_CERTIFIED
GLOBAL_FIXED_D0_PROJECTIVE_TOTAL_VARIATION = UNKNOWN
CERTIFIED_ATOMIC_UPPER = X^(267/400+o(1))
SOURCE_BACKED_X_O_PROJECTIVE_DECOMPOSITION = NO
```

直接对 atomic keys 使用 triangle/BV，至多得到 polynomial
`X^(267/400+o(1))` ledger；这远不是允许的 `X^o(1)`。TPC-124也没有给出
把这个新 `m`-fiber dictionary coefficientwise intertwine回 fixed-`theta` prefix
的 theorem。

### 31.3 post-§30 direct-theorem finite source screen

本轮对 2025-01-01 至 2026-08-01 的两个有限检索集合分别完成 `83/83` 与
`105/105` 标题/摘要筛选，并对 surviving candidates读取 theorem body、ranges与
proof chain。没有把 search snippet当作 theorem。

最接近的表面候选是 Carella, arXiv:2202.01071v5，但其主 proof不能作为
source theorem：Theorem 1.1 的 displayed remainder与 proof结尾相差一个 `x`
因子；Lemma 3.1 的 uniform residue-count remainder可取大奇素数 `x`、
`q=(x+1)/2`、`a=q` 直接反例；proof还把 upper error改作 lower bound、把任意
`t` 无映射地设为 `1`、并在双 Möbius展开中无依据使用 `d1 d2<=x`。即使反事实
接受其结论，它也只是 naked two-point fixed-shift statement，不接受 actual
`w_m`、four Möbius legs、growing `D0`、masks、shell、outer labels或 TPC
normalization。其 periodic extension arXiv:2208.12219也没有修复这个 literal
crosswalk。

其余 primary candidates在更早的 theorem-domain门即失败：

* Jiseong Kim, arXiv:2509.24152，把 shift `h` 再求和；其 multiplicative/
  short-interval coefficient class不包含 `w_m`，不能升级为 prescribed `D0`；
* Diao, arXiv:2506.18065，是 almost-all/random binary-form metric theorem，且
  只有 naked 单 Liouville leg，不是 prescribed selected packet；
* Krishnamoorthy, arXiv:2501.10962，是 fake-Liouville small-prime model或
  bounded-away-from-extremes结果，不给 actual Liouville/Möbius cancellation；
* Banks--Shparlinski arXiv:2506.08787 的 ternary `mu(n1 n2 n3)` 不能融合本对象
  四条可能非互素 Möbius legs，且其适用性已由第 27 节旧 cell冻结；
* Cantarini 的 one-Möbius Goldbach / conditional `q`-average仍属于第 28 节旧
  scope，不能提升为 fixed physical phase。

因此没有 candidate同时通过 literal coefficient、fixed `h0=2`、summation/
prefix domain、`X/N/q` ranges、uniform constants、normalization与完整 loss
ledger：

```text
NEW_LITERAL_FIXED_D0_DIRECT_THEOREM = NONE_IN_FINITE_SCREEN
DIRECT_THEOREM_ARITHMETIC_ADVANCE = NO
```

### 31.4 self-kernel / cross-`D0` frame audit

Grimmelt--Merikoski Part I（arXiv:2505.00489）的 evaluation-distribution large
sieve可以接收某些 literal evaluation points，但其 dual/Cauchy reduction右侧仍
保留两份 self-kernel。Hilbert-space Cauchy--Schwarz只是把 cross term改写为
两份 Gram quadratic forms；它没有证明 actual cloud 的 Gram operator norm为
`X^o(1)`，不能被记作免费的 frame theorem。

本轮逐 theorem-interface核对的附近 spectral large sieves也不是该 Gram对象：

* Qi, arXiv:2404.09085 Theorem 1 与 arXiv:2407.17711 Theorem 1控制
  `PGL_2(Z[i])\\PGL_2(C)` cusp spectrum中的 Gaussian Hecke coefficients；
* Lekkas--Voskou, arXiv:2405.01056 Theorem 3控制 Maass forms 的 hyperbolic
  periods，几何变量是 separated scalar points，不是 dense compact cross-`D0`
  evaluation cloud；
* Pascadi, arXiv:2404.04239 Theorems 2--3控制 exceptional Maass Fourier
  coefficients；Hu--Petrow--Young, arXiv:2411.05672控制由 local components
  选择的 automorphic-representation families。

这些 theorem的系数、index set、normalization与 operator都不同；没有一个给
actual `(D0,G,j,outer labels)` cloud 的 literal full self-kernel或 block-Bessel
constant。dense comparable cross-`D0` collisions也未由 source-backed geometric
packing排除。逐 block使用普通 Cauchy至多暴露

```text
Q^(1/2) = X^(267/800+o(1)),
```

远大于 strict `1/400` budget。orbit Poisson zero、nonzero-frequency
density-one、Parseval或 complete-frequency mean均未被改写成 distinguished zero。

```text
FULL_LITERAL_SELF_KERNEL_THEOREM = ABSENT
CROSS_D0_BLOCK_BESSEL_OR_FRAME_THEOREM = ABSENT
GENERIC_HILBERT_CAUCHY_ENDPOINT_PAYMENT = NO
STRICT_1_OVER_400_FROM_FRAME_ROUTE = UNPAID
```

### 31.5 RH-338/339 wrong-object firewall

上游 RH-338研究 `Omega_k` 的 far-orbit atom obstruction，并给出
`R_orb,k=-D_orb,k` 与 `R_k=R_orb,k+R_rest,k`。其中 `2k` 是 orbit/operator
order，不是 TPC physical `h0=2`。该 artifact没有 `m,m',D0,G,j,w_m,E_Psi,N0`、
matched divisor shell或 TPC normalization；aggregate far contribution仍为
`NOT_TESTABLE`。所以：

```text
RH338_TO_TPC32_FIXED_D0_OR_FULL_E1 = ABSENT_WRONG_OBJECT
TPC207_TRIGGER_FROM_RH338 = false
STOP_CELL_CHANGE_FROM_RH338 = NONE
```

发布同步前的 `git fetch` 又发现远端 RH-339 的 17 个 committed files。其 exact
source object是第一 lower sideband `n_minus=2k-2` 上

```text
q_minus = -D_(k-1)_orb + C_minus,
D_(k-1)_orb/H_(k-1) -> +infinity.
```

它证明 separate-absolute orbit/complement route失败，以及 `E_off->0` 必须有
`C_minus=D_(k-1)_orb+o(H_(k-1))`；它没有估计 signed `C_minus`，所以
`E_off` vanishing/nonvanishing仍为 `NOT_TESTABLE`。RH 文中的 “physical” 是
Hardy full-trace boundary orbit；`2k-2` 是 sideband/operator order，不是 TPC
`h0=2`。该对象仍没有 `m,m',D0,G,j,w_m,E_Psi,N0`、matched divisor shell、
TPC determinant或 TPC normalization/loss ledger：

```text
RH339_TO_TPC32_FIXED_D0_OR_FULL_E1 = ABSENT_WRONG_OBJECT
TPC207_TRIGGER_FROM_RH339 = false
STOP_CELL_CHANGE_FROM_RH339 = NONE
```

### 31.6 最终裁决、STOP scope 与合法 reopen interface

本轮精确裁决为：

```text
TPC32_H0_2_FIXED_D0_THEOREM_PARAMETER_PRESERVING_OUTER_REGROUP_
SINGLETON_OR_EXACT_LITERAL_W_M_RETURN_DIRECT_AND_FRAME_THEOREMS_
ABSENT_STOP_SCOPED_NOT_REOPENED
```

状态矩阵是：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
TPC93_DECORATED_REINDEXING = L1 GO
THEOREM_PARAMETER_PRESERVING_REGROUP_OCCUPANCY = AT_MOST_ONE
SOURCE_TO_M_REGROUP = EXACT
REGROUPED_COEFFICIENT = EXACT_LITERAL_W_M
ACTUAL_EDGE_CENSUS = ABSENT
GLOBAL_PROJECTIVE_TOTAL_VARIATION = UNKNOWN
NEW_DIRECT_THEOREM = NONE
CROSS_D0_FRAME = ABSENT
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节新增

```text
DECLARED_TPC32_FIXED_D0_OUTER_REGROUP_AND_POST30_DIRECT_FRAME_
SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

只冻结第 31.2--31.5 节已逐式核对的两个 exact regroup schemes、列出的有限
direct-source candidates与列出的 spectral/frame interfaces。它不冻结：

1. 一个 source theorem直接接受同一 literal `w_m` 并支付 fixed
   `(D0,G,j,h0=2)`、strict endpoint及完整 physical ledger；
2. actual production census，加上 coefficientwise intertwiner和 source-backed
   `X^o(1)` projective decomposition，把 `m`-fibers变成 genuinely growing
   theorem-admissible blocks；
3. 一个明确允许 row primes/cofactors/slopes/outer labels随 `m` 变化、同时保留
   physical determinant与normalization的新 theorem；
4. 一个直接控制 actual full self-kernel的 theorem，或在 fixed-`D0` theorem后
   提供可核查 operator constant的 cross-`D0` block-Bessel/frame theorem。

第 6 节全部旧 method cells保持原 scope `STOP_SCOPED`，尤其 TPC193 V1、
common-`k` V1、tail-failure/A/B V1 与 full-`r_Rr_R` ultra-complement V1。两个
O161 pointwise parents、pair-native reroute、H1 与 global architecture继续
`OPEN`。本节不把第 6 节旧 cell重新包装成新方法。

即便未来 fixed-`D0` gate转为正面，也不自动创建 TPC-207；还必须分别通过
all-`D` uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual packet attachment与完整 provenance gates，
并使页首数学 trigger真实改变。

### 31.7 发布边界

没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入仅为
`TPC_HANDOFF.md`；全部 127 个 protected untracked保持原样且不纳入提交。

```text
POST_WRITE_RELEASE_REGRESSION = 22/22 PASS
TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = 33b0ae61172ea9e54588e650a7c0109cd8ba49fb
FINAL_SYNC_DELTA_FROM_INITIAL_E1C0661 = RH339_NEW_17_FILES
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
FINAL_SYNC_TPC_VERDICT_CHANGE = NONE
```

正式写入后已重新执行全部 22 项只读启动回归与四项 supplemental checks；
TPC-122与 TPC-27--32 legacy writers均未执行。只提交 `TPC_HANDOFF.md`，随后
pull/rebase、push并验证 local `HEAD`、`origin/main` 与 remote
`refs/heads/main` 三个 hash完全一致。

## 32. TPC32 post-§31 direct / metric / actual-census finite trigger refresh

### 32.1 source lock、协议与只读基线

本轮继续以仓库文件与 committed artifacts为事实来源，不把旧聊天当作证明。
启动与正式写入前状态为：

```text
INITIAL_HEAD = 63cd8a91a97af3a0735bc1a10edc8f67f818df12
INITIAL_ORIGIN_MAIN = 63cd8a91a97af3a0735bc1a10edc8f67f818df12
INITIAL_HANDOFF_SHA256
  = 370d337b9d0664b21a457768f3cf91887b4646dc0a820c94c9caaa705070f3bb
INITIAL_TRACKED_DIFF = EMPTY
INITIAL_CACHED_DIFF = EMPTY
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
STARTUP_REGRESSION = 22/22 PASS
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

启动及写前 `git fetch` 均确认 local `HEAD=origin/main`，没有新 RH/TPC remote
object需要拼接。继续 source-lock第 28/31 节锁定并由本节复核的同一 theorem-valid packet：

```text
sigma = 1/10000
lambda = 99979/210000
delta = 7/60
beta = 267/400
Q = X^(267/400+o(1))
J = X^(133/400+o(1))
C = floor(J)
h0 = 2
N0 = JQ^2 asymp XQ
0 < kappa_row < 1/400
```

三条 raw channels、matched difference、content cutoff、canonical `Delta#`、
actual masks/weights、outer labels与 packet natural scale均未删改。`delta=1/20`
truncated-entry family与 TPC-206 的 finite `delta=1/4` fixture均不是这条 source
lock，绝不可拼接。

第 32.2 节的 natural-source finite STOP corpus精确限于逐 ID/version列出的七个
primary sources；更宽的 official arXiv discovery scan只用于找候选，不把 search
counts、snippet或未逐 ID列出的 residual rows写入该 frozen theorem corpus。只有
theorem body、ranges、quantifiers与 proof interface可作为审核材料。

### 32.2 natural binary-Möbius primary theorem refresh

最接近 literal syntax的来源是 Klurman--Mangerel--Teräväinen
`arXiv:2304.05344v2`。其 Theorem 1.2给 fixed-shift two-point natural average，
但只沿一个未定位的 full-upper-log-density scale set趋零且无 rate；不能选择当前
production scale。Theorem 4.1允许 fixed
`f_1(a_1 n+h_1)f_2(a_2 n+h_2)` syntax，但要求

```text
D(f_j, chi_j n^(it_j); x^epsilon, x) <= epsilon,
max_j D(f_j, chi_j n^(it_j); x) >= 1/epsilon,
1/loglog(x) < epsilon < 1/2,
```

并把 affine forms与 implied constants当作 fixed data。Proposition 4.3另给相应
无条件 upper bound，但对下述 `mu_odd` 其首项不产生 saving；其 uniform
Proposition 4.4只允许 coefficients `<=sqrt(log x)`、slopes由一个 fixed `A`
的素因子组成。

determinant prime `2` 的 support condition不是合法 fatal。由 TPC-127 的 exact
parity classification，`a,s`奇且 `sV-aD=2` 时 `D,V`同奇偶；even--even点至少
一个值被 `4`整除，故原 Möbius product为零。定义

```text
mu_odd(n) = mu(n) 1_(2 does not divide n).
```

则逐 `z` 精确有

```text
mu_odd(D(z)) mu_odd(V(z)) = mu(D(z)) mu(V(z)),
```

且 `mu_odd(2^ell)=0`。所以：

```text
KMT_P2_SUPPORT_REPAIR = EXACT_LOSSLESS_PASS
KMT_MU_2_VALUE_FATAL = RETRACTED
KMT_FIXED_H0_2_SYNTAX = COMPATIBLE
```

真正的第一算术 fatal是 truncated distance。对 `mu_odd`，大 `x` 时截断区间的
奇素数上仍为 `-1`；principal character、`t=0`时

```text
D(mu_odd,1;x^epsilon,x)^2
  = 2 log(1/epsilon) + o(1),
```

其余 fixed character/twist同样有正的 `log(1/epsilon)` 量级，不能小于
`epsilon<1/2`。2-adic修改不影响该区间；full-distance lower condition也不能修复
已经失败的 truncated small-distance。即使反事实赠送 small-distance，
`epsilon>1/loglog x`也至多产生
`sqrt(logloglog x)/loglog x = x^(-o(1))`，不是 fixed positive power。
physical `s,d,a,u` 与 `q_prog=as`又随 packet/global scale增长；令
`A=A(X)`或人为放大 theorem length会改变 implied constant、actual prefix domain
与 normalization，均不合法。

其余 theorem-body survivors逐项失败：

* Pilatte `arXiv:2310.19357v2` Theorem 1.1是 reciprocal/logarithmic
  `lambda(n)lambda(n+1)` log-power saving；Remark 2.8 的 natural statement仍只在
  exceptional logarithmic-density scales之外且只有 log saving；
* Frantzikinakis--Host `1502.02646v3` Theorem 1.1要求 underlying homogeneous
  forms pairwise independent；一维 `sz,az`必有理相关，不能增加辅助平均变量后
  升级回 prescribed slice；
* Mangerel `1612.09544v2` Theorem 1.2控制 truncated small-prime model `mu_y`，
  不是 literal `mu`且不给 fixed positive power；
* Kravitz--Woo--Xu `2512.03292v1` Theorem 1.9平均 random polynomial coefficient
  family，不能选择 `(d+sz)(u+az)` 的 named member；
* Frantzikinakis--Klurman--Moreira `2407.08360v3` 的相关 unconditional object是
  two-variable binary quadratic/partition-regularity interface；所需 two irreducible
  correlation在该 source中明确仍为 conjecture，甚至 Liouville case未证；
* Tao--Teräväinen `1809.02518v2` 的 natural two-point结论只在 zero-log-density
  exceptional scales之外、无 positive-power rate；既有 metric/density firewall
  继续适用，不把它包装成新方法。

近期 random Rademacher function、empirical computation、logarithmic
`Omega` statistics、conditional Elliott application等 residual candidates均在
coefficient或quantifier入口失败。没有 candidate同时保留 literal physical
coefficient、fixed `h0=2`、summation/prefix domain、`X/N/q` ranges、uniform
constants、normalization与完整 physical-loss ledger：

```text
NATURAL_PRESCRIBED_UNIFORM_POSITIVE_POWER_THEOREM = NONE
KMT_CONDITIONAL_AFFINE_SYNTAX = L0_WITH_UNATTACHED_L1_INTERFACE_ONLY
DIRECT_ARITHMETIC_ADVANCE = NO
```

### 32.3 determinant-zero / additive-metric type audit

TPC-32 的 distinguished object是 normalized determinant变量的 finite DFT zero：

```text
A_hat_C,q_DFT(0) = sum_n A_C(n)
                 = small-content matched shell.
```

该 `r=0` 明确不是 orbit-variable Poisson zero，也不是 centered divisor-kernel
zero。TPC-170的对象则是 fiber coordinate `z` 上

```text
S_n,p,k(alpha)
  = sum_(j<=k) mu(d+s z_j) mu(u+a z_j) rho(z_j) e(-alpha z_j),
G_n,p(alpha) = (q_prog/T) max_k |S_n,p,k(alpha)|.
```

因此最早的 type fatal为：

```text
TPC32_NORMALIZED_DETERMINANT_DFT_ZERO
  != TPC170_ADDITIVE_FIBER_PHASE_ATOM
DETERMINANT_ZERO_TO_ADDITIVE_ATOM_INTERTWINER = ABSENT
```

三个模数必须分开：

```text
q_X    = prime phase-conductor modulus,
q_prog = a*s affine-progression modulus,
q_DFT  = auxiliary determinant-DFT modulus, q_DFT asymp Q.
```

TPC-94的 actual additive phase
`alpha_xi=epsilon_theta*r_tilde*Omega_xi/(c q_X) mod 1`不把 determinant index
变成 additive atom。TPC-180又给出 named atom/value/locator rows=`0/0/0`、
production schedule rows=`0`。即使反事实补上类型 intertwiner与 registry，
TPC-181仍独立要求 exact schedule、exact bad sets `E_n`、同一 atom及

```text
alpha_star notin limsup E_n.
```

TPC-170 的第一 Borel--Cantelli theorem不要求 independence，但其 a.e. fixed-phase
结论不能选择 prescribed singleton。

本轮读取 theorem body的 exceptional-set candidates也不提供该 bridge：

* Franklin--McNicholl--Rute `1603.01778v1` 与 Franklin--Rodriguez--Rojas
  `2601.03239v1`只在 Schnorr/Martin-Löf random points给 Fourier convergence；
  rational `0`不是 random atom，且无 rate、packet或 loss ledger；
* Michaud--Ramírez `2506.04187v2`控制 Diophantine moving shrinking targets的
  a.e. limsup hitting，事件与方向均不同；
* Bajović--Petković `2607.11180v2`需要 dynamical centered balls/waiting-time
  hypotheses，输出 a.e. orbit hitting，不是 named TPC bad-event avoidance；
* Beresnevich--Hauke--Velani `2406.19198v1` Theorem 4推出 divergence-event
  full bad-limsup membership，方向仍相反。

```text
NAMED_PRODUCTION_ADDITIVE_ATOM = MISSING
EXACT_CROSS_SCALE_PRODUCTION_SCHEDULE = MISSING
SCHEDULE_SPECIFIC_ATOM_AVOIDANCE = MISSING
METRIC_ARITHMETIC_ADVANCE = NO
```

### 32.4 actual census、coefficientwise intertwiner与 projective cost

第 31.6 节 route 2需要依次通过三个独立阶段；current committed data在每阶段
分别 fail closed。

第一阶段的 first fatal为：

```text
SAME_HIGH_BETA_PACKET_SOURCE_LOCKED_ACTUAL_PARENT_REGISTRY = ABSENT
```

TPC-32只给 symbolic physical coefficient；TPC-84明示不执行 census，也没有
archive/manifest/schema/code/output。TPC-205机器 registry为：

```text
production_row_count = 0
production_pair_records = 0
joint_mask_value = null
production_pair_to_omega_crosswalk = FAIL
```

TPC-206也不是补丁。它唯一 selected projection满足：

```text
X = 512
delta = 1/4
D0 = 0
materialized = 13/42
production_occurrence = false
first_missing = opened-D slice
```

其后 `J,Q,T,U0,G_X_row,packet_id,source_locator`、active mask、literal
coefficient、normalizations等继续缺失。artifact又显式规定：

```text
legal_join_with_selected_projection = false
same_packet_or_source_key_as_selected_projection = false
reason = DISALLOWED_CROSS_LINEAGE_SPLICE_INTO_SELECTED_GRAPH
```

所以不能把有限 `X=512,delta=1/4,D0=0` fixture与本轮 growing
`delta=7/60` high-beta packet拼接。

第二阶段中，TPC-93 source-child inverse与 weighted projector identity是真实 exact
`L1` interface，但只在 supplied retained
`omega=(L/R,alpha,gamma,j,u)` 上成立；当前 pair-to-`omega`为 FAIL。TPC-124
的必要且充分 coefficientwise test是

```text
(J Q_D - Q_Z) M = 0,
```

而 actual common native-leaf basis以及 growing `M,Q_D,Q_Z,J`全部未物化。
一条 vector identity `(J Q_D-Q_Z)M c_X=0`不能替代 matrix identity；按
physical `m` coarsening也只精确返回原 `w_m`，不产生新 theorem domain。

第三阶段中，TPC-32 generic joint row mask仍只有 entrywise bound。finite SVD、
formal atomic count或 triangle inequality不能提供 growing uniform projective norm：

```text
CERTIFIED_ATOMIC_UPPER = X^(267/400+o(1))
GLOBAL_FIXED_D0_PROJECTIVE_TOTAL_VARIATION = UNKNOWN
SOURCE_BACKED_X_O_PROJECTIVE_DECOMPOSITION = NO
```

H1不能补洞：TPC-173 qualifying claims=`0`，TPC-174 production witness absent，
TPC-175 coverage=`0/2988`且 eligible carriers=`0`，TPC-179 first missing仍为
`H1.source_backed_local_occurrence_edge_family`。TT-star bilinear pair与 H1 linear
occurrence edge类型不同。

合法的 data-first下一步必须先新增同一 `delta=7/60` packet的 source-locked
`TPC32_SELECTED_HIGH_BETA_ACTUAL_PARENT_REGISTRY_V1`，逐 record至少物化 packet/
scales/source hash、`alpha,gamma,j,h0,D0,G,Delta#`、三 raw labels、全部 mask
values、matched-shell coefficient、support/nonzero status、完整 source-child key、
multiplicities、三层 normalization与 exactly-once atom attachment。随后才可执行
TPC-93 inverse、物化四个 matrices、验证完整 intertwiner，并另证 source-backed
`X^o(1)` projective theorem。第一步本身至多是新的 actual `L1` data gate。

### 32.5 determinant-two firewall与 claim ceiling

TPC-127/128已经给 exact order-preserving pullback

```text
n = s V(z) = a D(z)+2 = su+as z,
mu(D(z))mu(V(z))
  = lambda(as)lambda(n-2)lambda(n)
    mu^2(D(z))mu^2(V(z)).
```

它把 literal pair变成一条 modulus `as`通常随 packet增长的 arithmetic
progression上的 shift-two Liouville product，并严格保留 quotient-squarefree masks、
physical weight、phase、interval origin、outer key与每个 prefix。TPC-128展开 masks
后 modulus进一步增长为 `as k^2 ell^2`。所以 fixed-form、unrestricted、terminal、
reciprocal-weight或 almost-all-scale theorem均不能无损回填。

反向 sanity ceiling也保持：determinant-two family含例如
`(d,s,u,a)=(1,1,3,1)`，即 `mu(z+1)mu(z+3)`。一个对全部 tuples统一的
prescribed natural positive-power theorem会包含 ordinary binary fixed-shift Chowla的
强特例。该观察只是 type/strength stress test；不证明 actual restricted TPC family与
Chowla等价，也不声称未来 theorem不存在。

### 32.6 direct / metric / actual-census 子审计裁决、STOP scope与合法 reopen interface

RH-340 final-sync拼接前，三路 finite refresh的精确子裁决为：

```text
TPC32_H0_2_SELECTED_HIGH_BETA_POST31_DIRECT_METRIC_ZERO_TYPE_AND_
CURRENT_COMMITTED_CENSUS_REFRESH_NO_THEOREM_TRIGGER_STOP_SCOPED_
NOT_REOPENED
```

状态矩阵为：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
KMT_P2_SUPPORT_REPAIR = EXACT_LOSSLESS_PASS
NEW_NATURAL_PRESCRIBED_POSITIVE_POWER_THEOREM = NONE
DETERMINANT_DFT_ZERO_TO_ADDITIVE_ATOM = ABSENT_WRONG_TYPE
NAMED_ATOM_SCHEDULE_AVOIDANCE_BRIDGE = ABSENT
SAME_PACKET_ACTUAL_PARENT_REGISTRY = ABSENT
TPC205_PRODUCTION_ROWS = 0
TPC206_SELECTED_PROJECTION = DIFFERENT_FINITE_FIXTURE_13_OF_42
COEFFICIENTWISE_INTERTWINER = NOT_INSTANTIABLE
GLOBAL_X_O_PROJECTIVE_THEOREM = ABSENT
H1_SOURCE_BACKED_COVERAGE = 0_OF_2988
DIRECT = FAIL
METRIC = FAIL
BAD_ENDPOINT = FAIL
STRUCTURAL = FAIL
DECLARED_CORPUS = FAIL
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节新增三个相互分离的 finite cells：

```text
DECLARED_TPC32_POST31_NATURAL_BINARY_MOBIUS_PRIMARY_
SOURCE_CANDIDATES_V1 = STOP_SCOPED

DECLARED_TPC32_SELECTED_HIGH_BETA_METRIC_SCHEDULE_EXCEPTIONAL_
LIMSUP_AVOIDANCE_SOURCE_CANDIDATES_V1 = STOP_SCOPED

DECLARED_TPC32_HIGH_BETA_CURRENT_COMMITTED_CENSUS_
INTERTWINER_XO_PROJECTIVE_CORPUS_V1 = STOP_SCOPED
```

它们只冻结第 32.2--32.4 节列出的 current sources、typed bridge与 committed
corpus。合法 reopen interface为：

1. 直接接受同一 literal physical coefficient、all prefixes、actual weights/masks/
   outer labels与 `N0` normalization，并给 uniform fixed positive power的新 theorem；
2. 直接控制 distinguished determinant coefficient `A_hat_C,q_DFT(0)` 的 pointwise
   theorem，不经 additive atom偷换；
3. 真正 source-backed named additive atom、同一 actual cross-scale schedule、exact
   `E_n`与 same-event singleton avoidance theorem；
4. 同一 high-beta packet actual parent registry，加 full common-leaf matrices、
   coefficientwise identity及 source-backed `X^o(1)` global projective theorem；
5. 第 31.6 节仍开放的 growing-parameter literal theorem、full self-kernel或
   cross-`D0` block-Bessel/frame theorem；
6. 两个 O161 pointwise parents、pair-native reroute、H1/global architecture或任何
   真正新增、对象与量词匹配的算术输入。

第 6 节全部旧 method cells保持原 scope `STOP_SCOPED`，尤其 TPC193 V1、
common-`k` V1、tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1。两个
O161 parents、pair-native reroute、H1 与 global architecture继续 `OPEN`。本节不把
旧 STOP cell重新包装成新方法。

即使任一 local gate未来转正，也不自动创建 TPC-207；仍须分别通过 all-`D`
uniformity、exactly-once physical cover、original/global normalization、tail-failure、
A/B selection、actual packet attachment与完整 provenance gates，并使页首数学
trigger发生真实 theorem-backed状态变化。

### 32.7 final-sync RH-340 cross-program transfer audit

正式提交前的 remote-tip复核发现 `origin/main` 从启动基线前进：

```text
REMOTE_PARENT = 63cd8a91a97af3a0735bc1a10edc8f67f818df12
REMOTE_NEW_TIP = eb1cf19a28b1d1d38eaece2a6bb0b578f20df969
REMOTE_COMMIT_SUBJECT = Add RH-340 synchronized prefix obstruction
REMOTE_DELTA = 17 NEW RH340 FILES ONLY
TPC_HANDOFF_OVERLAP = NO
TPC_ARTIFACT_OVERLAP = NO
```

RH-340 的 literal object是 RH Hardy normalization上的

```text
p_(sigma,k,n) = tau_(sigma,n)-a_n
                = q_(sigma,k,n)-d_(sigma,k,n),
P_u = sum_(2<=n<u) |p_n| R^n/n,
E_u = sum_(2<=n<u) |q_n| R^n/n,
D_u = sum_(2<=n<u) |d_n| R^n/n,
u = 4k.
```

它精确证明 `|P_u-E_u|<=D_u`，并在自己的 RH source assumptions下同步 analytic
tails；若 `P_(4k)->0`，则 orders `2k` 与 `2k-2` 必须满足两条 signed
orbit--head compensation laws。若先对 orbit、diffuse complement与 head分别取
绝对值，则 mandatory two-atom submajorant发散。但后一个命题明确不 lower-bound
fully signed prefix；aggregate signed prefix、`E_off`与 head budget仍为
`NOT_TESTABLE`，RH-288 determinant gluing仍 `OPEN/not activated`。

该对象在第一项 literal coefficient/type gate即失败。TPC-32需要的是同一
`delta=7/60` high-beta packet、fixed physical `h0=2` 的 Möbius matched shell、
三条 raw channels、content cutoff、canonical `Delta#`、actual masks/weights、
outer labels、canonical signed-prefix order与 `N0=JQ^2 asymp XQ`。RH 的
trace order `n`、moving `2k,2k-2` 与 `R^n/n` absolute budgets没有任何
coefficientwise map到这些 objects；analytic determinant quotient也不是
`A_hat_C,q_DFT(0)`。所以：

```text
REMOTE_RH340_LITERAL_PHYSICAL_COEFFICIENT = FAIL_WRONG_OBJECT
REMOTE_RH340_FIXED_PHYSICAL_H0_2 = ABSENT
REMOTE_RH340_CANONICAL_ORDERED_SIGNED_PREFIX = ABSENT
REMOTE_RH340_X_N_Q_UNIFORM_RANGE_CROSSWALK = ABSENT
REMOTE_RH340_N0_NORMALIZATION = ABSENT
REMOTE_RH340_FULL_PHYSICAL_LOSS_LEDGER = ABSENT
REMOTE_RH340_GROWING_SIGNED_PREFIX_THEOREM = NONE
REMOTE_RH340_SMALL_CONTENT_MATCHED_SHELL_SAVING = NONE
REMOTE_RH340_DISTINGUISHED_DETERMINANT_ZERO_BRIDGE = NONE
REMOTE_RH340_MAXIMUM_TPC_CLAIM
  = CANCELLATION_BLIND_SEPARATE_ABSOLUTE_MAJORANT_OBSTRUCTION_ONLY
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

artifact层的 commit-object独立核查得到 `dependency_manifest.json` 所列
`15/15` SHA256全部匹配，两个 PDF字节相同，且不写文件的 in-memory
`result_payload()`与 committed `result.json`相等。但这些只是 own-file consistency：
manifest刻意排除自身与 `archive_verification.json`；RH-340 commit/directory内没有
对应 archive verifier、RH-340 JSON schema、producer commit field或 RH-262--339
input-artifact hashes。
`experiments/build_result.py` 没有 `--check`，其 `main()` 会无条件重写 committed
`results/result.json`，因此本轮不执行该 writer。同步后优先尝试禁止
bytecode/cache的 pytest，但当前 Python 3.13没有 pytest，Python 3.10的既有 pytest
又缺 `exceptiongroup`，Python 3.9/3.8也没有 pytest；没有安装或修改依赖。随后以
标准库独立重放两个 test files的全部 `12` 个 test-function assertions，并另做
in-memory payload equality、Git-object manifest/hash与 PDF equality检查。

本节及第 6 节新 cell只冻结 commit `eb1cf19` 中 RH-340 到 TPC-32 的
cross-program transfer；不停止未来真正保留同一 packet、literal coefficient、
fixed `h0=2`、canonical prefix、actual weights/masks/outer labels、`N0`
normalization与完整 loss ledger的新 theorem。

### 32.8 final-sync RH-341 cross-program transfer audit

RH-340 audit完成并提交后，最后一次 pull/rebase又取得：

```text
REMOTE_PARENT = eb1cf19a28b1d1d38eaece2a6bb0b578f20df969
REMOTE_NEW_TIP = 6e1478a1a02ff4c3308e829727f8fea1cfbce52c
REMOTE_COMMIT_SUBJECT = Add RH-341 actual first-alias frontier review
REMOTE_DELTA = 23 NEW RH341 FILES ONLY
TPC_HANDOFF_OVERLAP = NO
TPC_ARTIFACT_OVERLAP = NO
PROTECTED_PATH_OVERLAP = NO
```

RH-341冻结的 literal coordinate为：

```text
k = log(1/sigma)/(2 log(lambda)) + O(1)
u = 4k
H_k = k R^(-2k)
p_(sigma,k,n) = q_(sigma,k,n)-d_(sigma,k,n)
P_u = sum_(2<=n<u) |p_(sigma,k,n)| R^n/n
E_u = sum_(2<=n<u) |q_(sigma,k,n)| R^n/n
D_u = sum_(2<=n<u) |d_(sigma,k,n)| R^n/n
```

它综合 RH-332--341 后重申 exact `|P_u-E_u|<=D_u`，并指出 prefix closure仍需

```text
D_(4k) -> 0
E_off,(4k) -> 0
q_(sigma,k,2k) = o(H_k)
```

三项均未由该 batch证明。orders `2k,2k-2`上的 compensation laws也只是
`P_(4k)->0` 的必要条件；source没有 moving signed combined-complement estimate。
abstract cancelling/noncancelling completions只存在于 information-class ledger，
明确没有构造 physical operator，所以它们只证明当前信息不足以决定 aggregate
closure/nonclosure。

RH-341 的 `q_(sigma,k,n)` 是 Hardy trace coefficient而不是 TPC modulus；absolute
trace-order prefix也不是 TPC-111/122 canonical ordered signed fiber prefix。moving
orders `2k` 与 `2k-2` 的差为 `2` 不得改写成 fixed physical `h0=2`。RH 的
`R^n/n,H_k` normalization没有到 `N0=JQ^2 asymp XQ` 的 crosswalk。故逐项 gate为：

```text
REMOTE_RH341_LITERAL_PHYSICAL_COEFFICIENT = FAIL_WRONG_PROGRAM_OBJECT
REMOTE_RH341_Q_SYMBOL = HARDY_TRACE_COEFFICIENT_NOT_TPC_MODULUS
REMOTE_RH341_FIXED_PHYSICAL_H0_2 = ABSENT_MOVING_2K_AND_2K_MINUS_2
REMOTE_RH341_ADJACENT_ORDER_GAP_2_TO_H0_2 = FORBIDDEN_NAME_COLLISION
REMOTE_RH341_PREFIX_OPERATOR
  = ABSOLUTE_TRACE_ORDER_NOT_CANONICAL_SIGNED_FIBER_PREFIX
REMOTE_RH341_X_N_Q_UNIFORM_RANGE_CROSSWALK = ABSENT
REMOTE_RH341_UNIFORM_TPC_CONSTANTS = ABSENT
REMOTE_RH341_N0_NORMALIZATION = ABSENT_HARDY_HK_AND_R_TO_N_OVER_N_ONLY
REMOTE_RH341_FULL_PHYSICAL_LOSS_LEDGER = ABSENT
REMOTE_RH341_GROWING_SIGNED_PREFIX_THEOREM = NONE
REMOTE_RH341_SMALL_CONTENT_MATCHED_SHELL_SAVING = NONE
REMOTE_RH341_DISTINGUISHED_DETERMINANT_ZERO_BRIDGE = NONE_GATE_A_FALSE
REMOTE_RH341_MAXIMUM_TPC_CLAIM
  = CROSS_PROGRAM_WRONG_OBJECT_INFORMATION_CLASS_UNDERDETERMINATION_FIREWALL_ONLY
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

artifact层只读复核得到：

```text
RH341_STDLIB_ASSERTION_REPLAY = 10_OF_10_TEST_FUNCTIONS_PASS
RH341_RESULT_PAYLOAD_EQUALITY = PASS
RH341_GIT_OBJECT_INDIVIDUAL_MANIFEST = 19_OF_19_PASS
RH332_TO_341_GIT_OBJECT_BATCH_MANIFEST = 154_OF_154_PASS
RH341_PDF_BYTE_EQUALITY = PASS
RH341_PDF_SHA256
  = 161e887bf0f9d5df1c4bd111c9f36f3030b7facc3eedcb8ff8a86b36f75f272a
```

当前环境没有完整 pytest，故仍以标准库独立重放 test assertions而不伪报 pytest。
`build_result.py`、`build_archive.py`、`build_batch_archive.py`、
`verify_archive.py` 与 `verify_batch_archive.py` 均没有 `--check`，且各自会重写
committed JSON；本轮全部未执行。现有 manifests锁定 committed Git blobs，但没有
独立 JSON schema，dict equality还有 Python `bool==int` 的 strict-type缺口；
RH-241/263/267/268也只有 symbolic source anchors，没有 claim-specific input blob
provenance。Windows CRLF worktree又不能直接冒充 manifest的 canonical Git-blob
bytes。

commit `6e1478a` 初到时尚未更新 RH handoff；随后 remote commit
`fd0c65e882341e61d39d84f5e0ac7d32c2d323de` 只修改 `RH_HANDOFF.md`，将
endpoint/batch/publication anchor正确更新为 RH-341、RH-332--341 与 `6e1478a`，
route coordinate更新为
`synchronized_actual_first_alias_signed_completion_open`。该 handoff仍明示 moving
noisy coefficient bridge、three same-clock limits、aggregate prefix、determinant与
Gates A--E未证；RH-342只是 future source-lock/investigation route，不是 theorem或
编号授权。所以：

```text
REMOTE_RH_HANDOFF_CLOSURE_COMMIT
  = fd0c65e882341e61d39d84f5e0ac7d32c2d323de
REMOTE_RH_HANDOFF_DELTA = RH_HANDOFF_MD_ONLY
RH_COMPLETED_ENDPOINT = RH_341
RH_ROUTE_COORDINATE = SYNCHRONIZED_ACTUAL_FIRST_ALIAS_SIGNED_COMPLETION_OPEN
REMOTE_RH_HANDOFF_NEW_TPC_OBJECT = NONE
REMOTE_RH_HANDOFF_NEW_TPC_THEOREM_TRIGGER = false
```

这是对既有 RH-341 release的 workflow/provenance closure，不新增 finite TPC method
cell，也不修复 RH-341 strict schema、只读 checker或 claim-specific source
provenance缺口；这些后续仍属于 RH release owner，不得混入本轮只提交
`TPC_HANDOFF.md` 的 TPC release。

本节及第 6 节新 cell只冻结 commit `6e1478a` 中 RH-341 到 TPC-32 的
cross-program transfer；不停止未来真正保留同一 packet、literal coefficient、
fixed `h0=2`、canonical prefix、actual weights/masks/outer labels、uniform
ranges/constants、`N0` normalization与完整 loss ledger的新 theorem。

### 32.9 发布边界

本轮 TPC gate没有创建 TPC-207、论文、paper directory、PDF或构建日志；
RH-340 的 17 个 files与 RH-341 的 23 个 files是已在 `origin/main` 上独立提交的
remote deltas，不是本轮 TPC release。主控正式写入仅为 `TPC_HANDOFF.md`；全部
127 个 protected untracked保持原样且不纳入提交。

```text
POST_WRITE_RELEASE_REGRESSION = 22/22 PASS
TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = fd0c65e882341e61d39d84f5e0ac7d32c2d323de
FINAL_SYNC_DELTA_FROM_INITIAL
  = REMOTE_RH340_RH341_AND_RH_HANDOFF_CLOSURE_AUDITED_NO_TPC_TRIGGER
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
FINAL_SYNC_TPC_VERDICT_CHANGE
  = RH341_WRONG_OBJECT_INFORMATION_CLASS_UNDERDETERMINATION_NO_THEOREM_TRIGGER
POST_SYNC_RH340_PYTEST
  = NOT_RUN_ENVIRONMENT_HAS_NO_COMPLETE_PYTEST
POST_SYNC_RH340_STDLIB_ASSERTION_REPLAY = 12_OF_12_TEST_FUNCTIONS_PASS
POST_SYNC_RH340_RESULT_PAYLOAD_EQUALITY = PASS
POST_SYNC_RH340_GIT_OBJECT_MANIFEST = 15_OF_15_PASS
POST_SYNC_RH340_PDF_BYTE_EQUALITY = PASS
RH340_BUILD_RESULT_WRITER_EXECUTED = NO
POST_SYNC_RH340_READ_ONLY_VALIDATION = PASS_WITH_PYTEST_DEPENDENCY_ABSENT_RECORDED
POST_SYNC_RH341_PYTEST
  = NOT_RUN_ENVIRONMENT_HAS_NO_COMPLETE_PYTEST
POST_SYNC_RH341_STDLIB_ASSERTION_REPLAY = 10_OF_10_TEST_FUNCTIONS_PASS
POST_SYNC_RH341_RESULT_PAYLOAD_EQUALITY = PASS
POST_SYNC_RH341_GIT_OBJECT_INDIVIDUAL_MANIFEST = 19_OF_19_PASS
POST_SYNC_RH332_TO_341_GIT_OBJECT_BATCH_MANIFEST = 154_OF_154_PASS
POST_SYNC_RH341_PDF_BYTE_EQUALITY = PASS
RH341_RESULT_ARCHIVE_BATCH_BUILD_VERIFY_WRITERS_EXECUTED = NO
POST_SYNC_RH341_READ_ONLY_VALIDATION = PASS_WITH_PYTEST_DEPENDENCY_ABSENT_RECORDED
```

正式写入后重新执行全部 22 项只读启动回归与四项 supplemental checks；TPC-122
与 TPC-27--32 legacy writers均不执行；RH-340/341 writers同样不执行。只提交
`TPC_HANDOFF.md`，随后
pull/rebase、push并验证 local `HEAD`、`origin/main` 与 remote
`refs/heads/main` 三个 hash完全一致。

## 33. O161 pointwise current-primary theorem refresh

### 33.1 协议、基线与有限检索范围

本节从仍为 `OPEN` 的两个 O161 pointwise parents出发，不把第 32 节
selected-packet STOP cell换名为新方法。启动、分身交付及正式写前复核均得到：

```text
INITIAL_HEAD = 3d191298f45ee9a00768c4fdcb571550102703ac
INITIAL_ORIGIN_MAIN = 3d191298f45ee9a00768c4fdcb571550102703ac
INITIAL_HANDOFF_SHA256
  = 5a308c1eefdacbf07c791b1cf6a84bb0038116a5035d7847e4076eac45651946
INITIAL_TRACKED_DIFF = EMPTY
INITIAL_CACHED_DIFF = EMPTY
STARTUP_REGRESSION = 22/22 PASS
TPC184_TPC189_DECLARED_SOURCE_LOCKS = 8/8 PASS
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

检索日为 2026-08-01。主检索使用 official arXiv API/search与
`math.NT/recent`；API在完成 exact/broad queries后返回 HTTP 429，随后只
降级到 official arXiv HTML search/recent page，没有绕过限流。raw hit counts、
abstract snippets与 title screens只用于发现，不作为 theorem evidence；正式
裁决全部回到 exact ID/version 的 theorem body、作者 PDF或期刊 primary
metadata。有限 screen不声称全球文献不存在性。

source-lock、DIRECT scan、BAD_ENDPOINT scan与独立 devil's-advocate transfer
audit全部只读；各分身的 before/after `HEAD`、handoff hash、tracked diff与
cached diff均未变化，`files_changed=[]`。

### 33.2 两个合同的 exact type separation

两路当前唯一可共享的 source-backed core为：

\[
 q=as,\qquad t(z)=ad+qz,\qquad
 c_z=\mu(d+sz)\mu(u+az),
\]
\[
 (a,s)=1,\qquad as\ {\rm odd},\qquad su-ad=2.
\]

determinant identity source-backs fixed physical `h0=2`，但不
source-back cancellation、decay或 production attachment。DIRECT 的 exact core是

\[
 F_N(\alpha)=\frac qN
 \sum_{\substack{z\\N<t(z)\le 2N}}
 c_z\rho_{\rm phys}(z)e(-\alpha z),
\]

并需要同一 actual record上的 named `alpha_star`、deterministic
all-prefix/all-scale及 fixed positive power。BAD_ENDPOINT 的 cumulative object是

\[
 A_\rho(T)=\sum_{\substack{z\\0<t(z)\le T}}c_z\rho(z),
\]

而缺失的 local theorem必须对同一 packet的 prescribed bad ancestors
`N_j=T/2^j in E_X_star` 给出

\[
 \frac q{N_j}
 \left|
 \sum_{\substack{z\\N_j<t(z)\le2N_j}}
 c_z\rho_\star(z)
 \right|
 \le C X^{-\sigma}.
\]

从 local block回到 `q/T` cumulative prefix的唯一合法桥仍是
TPC-159 exact telescoping；每个 block必须乘
`N_j/T=2^{-j}`，tail为 `2^{-J}+q/T`。令 `N=T`
只把 DIRECT domain变为 `T<t(z)<=2T`，绝不会产生
`0<t(z)<=T`。

TPC-180/current production census仍精确为：

```text
registry_id = null
named_physical_atom_id = null
phase_value_mod_1 = null
phase_value_source_locator = null
packet_schedule_locator = null
packet_coordinate_rows = []
fixed_h0 = 2
```

因此两个合同当前共同的 production-data首缺是 named production atom/actual
record，但其后的 arithmetic first missing仍须分开：

```text
DIRECT_FIRST_DATA_FATAL
  = SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK
DIRECT_CROSSWALK_SUBGATE
  = NAMED_PRODUCTION_ATOM
DIRECT_FIRST_COUNTERFACTUAL_ARITHMETIC_FATAL
  = DIRECT_ADDITIVE_TWIST_NAMED_ATOM_POWER_SAVING

BAD_ENDPOINT_FIRST_DATA_FATAL
  = PRESCRIBED_BAD_ENDPOINT_ATOM_HAS_NO_SOURCE_LOCKED_VALUE
BAD_ENDPOINT_FIRST_COUNTERFACTUAL_ARITHMETIC_FATAL
  = POINTWISE_NAMED_ATOM_Q_OVER_N_POSITIVE_X_POWER_LOCAL_INCREMENT_
    ON_SCHEDULED_E_X_STAR_ANCESTORS
```

TPC-167 的 `X^(-1/4+o(1))` envelope只属于 Lebesgue phase
`L2`；TPC-159只在 shadow之外给 logarithmic almost-endpoint。
Parseval、phase-a.e.、exceptional-scale density与 good-scale log saving均不能
支付 source-locked named atom。

### 33.3 current-primary theorem-body matrix

最接近 prescribed phase的新增来源是 el Abdalaoui--Nerurkar
`arXiv:2006.07646v2`。Theorem 3.2与 Corollary 3.3对每个 fixed
`theta` 给

\[
 \frac1N\sum_{n\le N}\mu(n)
 f(S^n\mu^2)e(n\theta)\longrightarrow0,
\]

并可令 `f` 为有限 squarefree cylinder。其第一 fatal不是 phase，而是
literal coefficient：`f(S^n mu^2)`只看 squarefree support，完全丢失
第二条 Möbius sign；它不能无损表示
`mu(d+s z)mu(u+a z)`。Remark 3.4又明确该 corollary
non-quantitative。后续仍无 growing affine parameters、uniform threshold/constant、
`q/N_j` block、actual support或 loss ledger。Corollary 4.4的
Liouville结果分别是有限移位窗的 almost-all count与 fixed shift的非极端
`1-epsilon(h)` bound，也不是趋零的 prescribed physical theorem。

Murty--Vatwani *A remark on a conjecture of Chowla* Theorem 1无条件控制
fixed shifts上的

\[
 \mu^2(n+h_1)\cdots\mu^2(n+h_{k-1})\mu(n+h_k)
\]

到任意 fixed log-power；constant显式依赖 `k,A,h_1,...,h_k`。
Theorem 2在 Dirichlet-GRH下有 power bound，但仍是 one-sign coefficient、
fixed shifts且无 additive phase。因此它不能提供缺失的第二条 sign，也不能把
conditional wrong-object power计入 TPC arithmetic credit。

Grimmelt--Teräväinen `arXiv:2607.28091v1` Theorems 1.1--1.2
给 dense sets/primes中 almost-all coefficient-vector configurations；
Theorems 1.3与 6.7是 growing box上的 averaged counting-operator inverse theorem：

\[
 R_H(\lambda;f_1,\ldots,f_k)
 =\sum_{\boldsymbol b}\lambda(\boldsymbol b)
   \sum_x\sum_{m\in[H]}\prod_i f_i(x+b_i m).
\]

这里 `lambda(b)` 是 generic bounded coefficient weight，不是 Liouville；
结论也不是 signed-correlation upper bound。没有 literal two-Möbius pair、
prescribed atom、determinant-two tuple或 `q/N` normalization。

其余新增/未冻结 version-delta candidates均在更早字段失败：

1. Matthiesen `1606.04482v4` 要求超过二维的 convex-body average及
   nonconstant parts两两独立；一维 `s z,a z` 必然共线，不能从多维
   average切到 prescribed physical slice。
2. Browning--Sofos--Teräväinen `2212.10373v2` 对 random
   polynomial coefficient families给 almost-all theorem；actual tuple membership
   未证，`lambda(f(n))` 又缺 Möbius zero masks、atom与 fixed power。
3. Burstein--Iosevich--Sant `2604.14482v1` 的 proved theorem是
   single-Möbius phase-`L1` lower bound；需要的 pointwise square-root
   upper bound只是 source中明示未知的 assumption。
4. Pandey--Radziwiłł `2510.20194v1` 是 single multiplicative
   coefficient的 inverse/pretentious structure theorem，不是 named-atom upper bound。
5. Cantarini--Gambini--Zaccagnini `2603.10241v1` 控制
   `m_1+m_2=n` additive convolution shells（部分结果还需 RH+SZ），不是
   同一 `z` 上的 affine pair prefix。
6. el Abdalaoui--Lin `2607.15960v1` 是 single-Möbius operator
   averages；定量项只来自 Davenport log powers。
7. Pilatte `2604.26564v1` 是 one-factor、origin-averaged short-interval
   Fourier theorem，不是 prescribed two-affine local block。

Ramaré--Zúñiga Alterman `2603.25961v3` 的 LCM-denominator double
sum已由旧 cell冻结，本节只复核其仍为 wrong literal object，不把它列入新增
version-delta cell。只有 publisher metadata、没有取得 primary theorem body的
Baker--Harman record也未提升为 verified candidate。

### 33.4 既有 close routes与独立 adversarial transfer

既有来源只作为 consistency controls，不重新包装：

* Teräväinen--Walker `2303.12574` Lemma 4.2(1)可对 fixed nonparallel
  affine data与每个 fixed atom控制 logarithmically weighted two-Möbius
  correlation，但只是 qualitative/log prefix，非 natural scheduled
  `q/N_j` local block，且无 growing-uniform constant或 fixed power。
* Tao--Teräväinen `2512.01739v2` 经 TPC-147/148/149确实给 natural
  `q/N` terminal-block log saving，但只在
  `N notin E_X_star`；BAD_ENDPOINT本 gate指定的 ancestors恰在
  `E_X_star` 内。
* Pilatte `2310.19357v2`、KMT `2304.05344v2` 分别仍是
  Liouville/logarithmic或 complete-prefix/pretentious-distance interface；都没有
  同一 `rho_star`、scheduled bad block与 fixed power。

独立 devil's-advocate审计钢人化了三种潜在 transfer。对
`2607.28091v1`，把 coefficient weight取成 actual tuple的 delta selector
仍不产生 pointwise theorem：单 tuple natural scale为 `O(N^2/B)`，
而 theorem threshold为 `delta B^k N^2/B`，故需
`delta about B^(-k)`；定理同时要求 `delta^(-C)<=B`，
即 `B^(kC)<=B`，对 `k>=3,C>=1` 不可能。

把两个 Möbius factors在 coprime support上写为一个 Möbius of a quadratic
product会改成稀疏非线性 reindexing，破坏 physical prefix与 normalization。
TPC-127 determinant-two pullback又精确保留
`lambda(n-2)lambda(n)` 两条 sign及 quotient-squarefree masks；TPC-128
展开后 modulus增长到 `as k^2 ell^2`。它们不能把 second sign消掉。

因此以下拼接全部非法：

```text
PHASE_FROM_2006_07646V2
+ RATE_FROM_MURTY_VATWANI
+ GROWING_COEFFICIENT_AVERAGE_FROM_2607_28091V1
!= SAME_RECORD_LITERAL_TWO_MOBIUS_POINTWISE_THEOREM
```

三项没有共同 coefficient、prefix、exceptional set、constant、normalization、
actual support或 loss ledger。`sum a_n=o(N)` 与
`sum b_n<<N/log^A N` 也不推出逐项乘积序列的相同 bound。

### 33.5 裁决、STOP scope与合法 reopen interface

本有限 gate的精确裁决是：

```text
TPC_O161_DIRECT_BAD_ENDPOINT_CURRENT_PRIMARY_ONE_SIGN_OR_AVERAGED_
WRONG_OBJECT_NO_FIXED_POWER_TRIGGER_STOP_SCOPED_PARENTS_OPEN

COMMON_PRODUCTION_RECORD = ABSENT_NOT_TESTABLE
DIRECT = FAIL_CLOSED_AT_NAMED_PRODUCTION_ATOM_PARENT_OPEN
BAD_ENDPOINT = FAIL_CLOSED_AT_SOURCE_LOCKED_NAMED_ATOM_PARENT_OPEN
CURRENT_PRIMARY_SINGLE_SOURCE_SURVIVORS = 0
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节新 cell只冻结第 33.3 节明确列出的 current-primary
version-delta candidates及本节精确 cross-source splice；有限 no-survivor不提升为
global nonexistence。TPC193 V1、common-`k` V1、
tail-failure/A/B V1、full-`r_R r_R` ultra-complement V1以及第 32 节
全部 method cells继续原 scope `STOP_SCOPED`。两个 O161 pointwise
parents、pair-native reroute、H1与 global architecture继续 `OPEN`。

最窄 data-first reopen input仍是一个 source-locked named production atom record，
同一 record须同时物化：atom ID/value/source locator、actual packet/all-scale
schedule、`a,s,d,u,q` 与 determinant witness、canonical translation、
actual support、literal coefficient及全部 masks/weights/outer labels、prefix
order/endpoints、共同 ranges、uniform `C`、positive `sigma`、
正确 target normalization与 no-double-charge physical-loss ledger。

其后 arithmetic theorem仍分别需要：

1. DIRECT：natural `q/N` named-fixed-atom、all physical prefixes/scales
   的 uniform positive-`X`-power bound；
2. BAD_ENDPOINT：对 scheduled `E_X_star` ancestors的同一
   `rho_star` local `q/N_j` fixed-power theorem，再经 TPC-159
   exact telescoping进入 `q/T` cumulative object。

即使任一 O161 local theorem转正，也不自动创建 TPC-207；all-`D`
uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual packet attachment与完整 provenance gates
仍须分别通过。

### 33.6 发布边界

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入仅为
`TPC_HANDOFF.md`；全部 protected untracked必须原样保留且不纳入提交。

```text
POST_WRITE_RELEASE_REGRESSION = 22/22 PASS
TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_GIT_DIFF_CHECK = PASS
POST_WRITE_MARKDOWN_FENCES = 852 MARKERS BALANCED
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = 3d191298f45ee9a00768c4fdcb571550102703ac
FINAL_SYNC_DELTA_FROM_INITIAL = NONE
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

正式写入后必须重跑第 1 节全部 22 项只读回归、TPC-111/124/126/127 四项
supplemental checks与 protected manifest；只提交 handoff，随后 pull/rebase、
push并验证 local `HEAD`、`origin/main`、remote
`refs/heads/main` 三个 hash完全一致。

## 34. 2026-08-03 RH-342--348 cross-program 与 current-primary delta 审计

### 34.1 审计范围、同步基线与 fail-closed 协议

本轮启动时 working tree没有 tracked/cached diff，只有第 1 节明示必须保留的
protected untracked。第一次 `git pull --rebase origin main` 从
`4c8fc56b173aede3d5a086353b5b12bd53b99f40` 前进到
`8216bdbde7700d5863405f4aaaef9ded6b819c2e`，取得 RH-342--346；所有只读
source-lock完成并停掉分身后，第二次安全 pull又取得 RH-347，达到
`9a33bba1e456bf5a6d1b81f45d7ebc9e257c3a11`。正式写入后只读 fetch发现
RH-348 commit `af5864a17063adc3084c9ce025878dadb39da05c`；主控没有 stash或
在 dirty tree强行 rebase，而是先审核 canonical remote blobs，再将 handoff commit
正常 rebase到该 RH-only commit。七项各含 17 个 files，共 119 个 RH-only files；
没有 TPC path、`TPC_HANDOFF.md` 或根政策 overlap。

同步后的第 1 节启动回归为 `22/22 PASS`；TPC-111/124/126/127 supplemental
为 `4/4 PASS`。没有执行会重写 committed JSON 的 TPC-27--32 legacy writers、
TPC-122 writer或任何 RH builder。所有 subagent均为 read-only；正式写入只由
主控完成。

远端线性 source provenance为：

```text
RH-342  65dd912f36477448dec804789a93ce9a6ec1cc3a
RH-343  3d8562fb59811c09535b65df0d7999c75cfa0c7c
RH-344  0b71f771849090ab020f5d6dc0d777d50d3082da
RH-345  be5321656e69e9d0b6efb4a829b7f2957566e15c
RH-346  8216bdbde7700d5863405f4aaaef9ded6b819c2e
RH-347  9a33bba1e456bf5a6d1b81f45d7ebc9e257c3a11
RH-348  af5864a17063adc3084c9ce025878dadb39da05c
```

当前 `RH_HANDOFF.md` 仍以 `Decision after RH-341` 与未来 RH-342--351 路线
叙述，未闭合到已提交的 RH-342--348。故它不能作为 TPC theorem activation或
完整 upstream provenance closure；但该 drift不是第一数学 fatal，所有 TPC
transfer在 literal-object gate更早失败。

### 34.2 RH-342--348 theorem-body source locks

RH-342 的 actual source object是 noisy-head/counterloop spectral power sums与
genus-one root germ。它证明 exact finite algebra、conditional rank consequence及
finite-normal hidden-shell model；没有 actual two-Mobius coefficient、physical
determinant decomposition或 moving signed-prefix estimate。

RH-343 构造 equal-rank/equal-spectral-mass但 first-alias行为不同的 complete-root
shell models。它是 source-backed information-class underdetermination，并明确
没有 actual noisy-operator realization；不得把一个 shell或 first-alias moment
选择为 TPC packet atom。

RH-344 在 RH program 内确实给出 physical critical-order raw trace ledger：

```text
F_k^orb = 2k G_k,
p_(sigma,k,2k)
  = T_k^rest + P_(sigma,2k) - d_(sigma,k,2k)
    - A_(k,2k) - F_k^orb.
```

它只给 necessary compensation identity；signed orbit-free rest没有估计，故既不
证明 RH closure/nonclosure，也更不证明 TPC cancellation。这里的 “physical”
必须保持 program-relative，不能误写成 TPC production physical atom。

RH-345 将上述 ledger压成 critical scalar balance。off-balance conclusion条件于
尚未证明的 actual `Y_k=o(H_k)`；balance phase只由 relative `o(1)` law定位，
而 target需要 exponentially smaller relative error。close/far scalar completions
只证明 information-class underdetermination，正文明确说它们不是 physical noisy
operators。

RH-346 对 `m=k-1`、`n_-=2m=2k-2` 给出同一 physical clock上的 lower
sideband raw trace ledger：

```text
F_m^orb = 2m G_m,
p_(sigma,k,2m)
  = T_(k,m)^rest + P_(sigma,2m) - d_(sigma,k,2m)
    - A_(k,2m) - F_m^orb.
```

它仍只给 necessary compensation；actual lower rest、head transport、`E_off`
与 full punctured prefix均未控制。

RH-347 的 strongest honest physical statement是：沿
`eta_sigma -> eta != eta_-`，若额外假设 actual
`Y_m^-=o(H_m)`，则

```text
|p_(sigma,k,2m)|/(2H_m)
  = |C_star*C_M*lambda^(eta-1)-1|/C_M
    * (beta*R)^(2m) * (1+o(1)) -> infinity.
```

仓库没有证明该 hypothesis。balance phase
`eta_-=1-log(C_star*C_M)/log(lambda)` 上，即使反事实加入该 hypothesis，
closure仍要求

```text
P_(sigma,2m) = S_m^- + o(H_m),
relative error = o((beta*R)^(-2m)),
```

而 source只给 relative `o(1)`。RH-347 的 exact inverse scalar map构造
zero-residual与 divergent-residual两条 envelope；它们仍不是 actual noisy operator。
因此 source-backed新事实只停止 lower scalar information route，actual lower
compensation、punctured aggregate与 RH 自身下一路线继续 OPEN。

RH-348 随后在同一 RH physical clock上取 genuinely growing index set
`I_k={m_star,...,k-2}`、`n=2m`，同时提取 punctured lower-even complete
orbit ladder。令 `w_m=R^(2m)/(2m)` 与 `x=(beta R)^2>1`，它证明

```text
L_k^orb = sum_(m in I_k) G_m R^(2m)
        = x^(k-1)/(C_M*(x-1)) * (1+o(1)),
sum_(m in I_k) |A_(k,2m)| w_m = O(1/k) L_k^orb,
sum_(m in I_k) |S_(k,m)| w_m = L_k^orb * (1+o(1)).
```

对 actual RH supply `Z_(k,m)=Y_(k,m)+P_(sigma,2m)` 与 residual
`p=Z-S`，source只用 pointwise reverse triangle得到

```text
sum |Z| w_m + sum |p| w_m >= sum |S| w_m.
```

因此 `sum |p|w_m -> 0` 只会迫使 supply mass至少同阶发散；repository没有
actual moving-order signed supply bound。该 theorem是 RH 内部真实 growing
necessary-compensation进展，但既不证明 lower-even closure/nonclosure，也不控制
odd/upper orders或 full `E_off`。它更不是 TPC literal coefficient上的 signed-prefix
saving；不得把 divergent absolute demand或必要 supply mass改写为 cancellation。

### 34.3 literal field firewall与最强 transfer 的第一 fatal

RH 与 TPC 的同名符号逐项冻结如下：

| field | RH-342--348 | TPC所需 | first fatal |
|---|---|---|---|
| coefficient | spectral moments或 localized Hardy trace scalar | literal two-Mobius affine pair/three raw channels/TT-star pair | no coefficientwise identity |
| physical order | moving `2k,2k-2` | fixed affine `h0=su-ad=2` | moving-order gap is not determinant |
| prefix index | trace/moment order `n` | translated-integer/fiber order或 scheduled local blocks | domain and order mismatch |
| phase | noise-clock `eta` | prescribed additive `alpha_star`或 determinant DFT `r=0` | phase type mismatch |
| `q` | RH trace coefficient或 spectral cutoff | progression modulus `as` / separate `q_DFT` | notation collision |
| scale | `sigma,k,m,lambda,H_m,R^n/n` | `X,N,q,Q,J,D0,G,N0` | no range/normalization map |
| labels | root shells/orbit cells/parity scalar | content, `Delta#`, masks, weights, outer labels | packet fields absent |

由此四条 strongest attempted bridge均 fail closed：

1. O161 DIRECT/BAD：`p_(sigma,k,2m)`不是
   `mu(d+sz)mu(u+az) rho(z)e(-alpha z)`；没有 named production atom、actual
   schedule、`q/N` terminal block或 TPC-159 `q/T` cumulative normalization。
2. TPC-111/122/TPC32：一个 RH trace coefficient等于零，尤其非physical
   scalar close model中的零，绝不是 normalized determinant DFT
   `A_hat_(C,q_DFT)(0)`；没有同 packet raw channels、content、`Delta#`、
   prefix intertwiner、BV/content envelope或 `N0=JQ^2 asymp XQ`。
3. TPC-205/206 pair-native：RH orbit points、two orders或 close/far alternative
   models都不是同一 production occurrence中的 ordered TT-star pair；无法填写
   42-field record、pair-to-`omega` theorem或 global normalization。TPC-206仍为
   selected `13/42`，first missing `D`。
4. H1：没有 linear、coefficientwise-conservative、source-cut可追溯的 local
   occurrence edge；aggregate scalar identity不能升级成 occurrence transport。

特别地，以下两个 tempting splice被精确禁止：

```text
2k - (2k-2) = 2
  != fixed physical h0 = su-ad = 2

RH eta_minus scalar balance phase
  != TPC alpha_star
  != q_DFT distinguished zero frequency
```

### 34.4 artifact、schema与 provenance ceilings

`pytest` 在当前环境不可用；没有安装依赖或改变环境。主控以 standard-library
只读 loader重放七份 release的非-manifest tests，共 `129/129 PASS`；以
`git show HEAD:<path>` 读取 canonical committed bytes核验 dependency manifests，
共 `105/105 blobs PASS`。RH-348尚未进入 local tree时，主控直接从 commit
`af5864a` 注入 canonical source modules并重放其 `17/17` assertions；其余工作树
文本受 Windows CRLF转换影响，故 canonical Git
blob才是 manifest hash的合法字节来源。

RH-344--348 的 claim-firewall存在同一弱类型 schema缺口：将
`false_claims`/`gates` 中 JSON boolean `false` 在内存改为整数 `0`，Python dict
equality与 `not any(...)` 仍接受；RH-347 单独有 24 个此类字段。部分显式
`is False` assertions能拒绝对应字段的整数替换，但没有覆盖这些 dictionaries；
RH-348 对应弱类型字段为 23 个。七份 payload均没有独立 JSON schema、
theorem-source hashes或 producer commit；
各自 15-file manifest只 pin release文件，没有 pin referenced RH theorem bodies。

这些 PASS只证明 committed finite artifacts可复现；schema/provenance ceilings也
不能补写数学 theorem。第一跨程序 fatal仍是 literal coefficient/data type。

### 34.5 2026-08-03 current-primary theorem-body delta

官方 arXiv math.NT new listing在 Monday, 3 August 2026 共 29 项：9 new、
1 cross-list、19 replacements。listing中没有 `Mobius`、`Liouville` 或
`correlation` match；唯一需要进入 theorem-body 的 nearby candidate是
Durkan--Pearce-Crump `arXiv:2607.29429v1`。

其 Theorem 1对 Steinhaus或 Rademacher random multiplicative function `f`
证明 almost surely

```text
|sum_(n<=x) f(n)|
  <<_(epsilon,f) sqrt(x) (log log x)^(1/4+epsilon).
```

source定义 Rademacher model为独立随机 prime signs、squarefree support，并明确
说它只是 Mobius的 probabilistic model：它保留 support/sign形式，却用 independent
values替代 arithmetic prime values。故第一 fatal是 random model而不是 actual
deterministic Mobius；下一层仍是 single complete-prefix coefficient，而非同一
`z` 的 two-affine Mobius pair。它还没有 fixed `h0`、packet atom、`q/N`、
`X/N/q` uniform ranges、matched-shell determinant、pair registry、normalization或
physical-loss ledger。有限 screen因此无 survivor；这不是未来版本或全局文献的
nonexistence claim。

### 34.6 裁决与合法 reopen interface

本轮精确有限裁决为：

```text
TPC_REMOTE_RH342_348_SPECTRAL_TRACE_LADDER_OBJECTS_AND_ARXIV_2607_29429_
RANDOM_MODEL_HAVE_NO_LITERAL_TPC_CROSSWALK_OR_THEOREM_TRIGGER_
STOP_SCOPED_PARENTS_OPEN

THEOREM_TRIGGER = false
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_CREATED = false
```

第 6 节新 cells只冻结上述七个 committed RH theorem bodies与
`arXiv:2607.29429v1` 的精确跨程序改名。它们不重开或扩张 TPC193 V1、
common-`k` V1、tail-failure/A/B V1、full-`r_Rr_R` ultra-complement V1或
第 29--33 节其他 cells。两个 O161 pointwise parents、TPC32 direct theorem
interface、pair-native reroute、H1与 global architecture继续 OPEN。

合法 reopen必须由单一 source-backed theorem/crosswalk逐项保留：literal physical
coefficient、fixed physical `h0=2`、same actual packet、summation domain与 prefix
order、content/`Delta#`/outer labels、masks/weights、全部 `X/N/q` ranges、uniform
constants、正确 normalization及完整 physical-loss ledger。算术输出还必须直接给
same-object growing signed-prefix/BV或 matched-shell saving，并支付 strict `1/400`；
pair/H1路线则必须实际 materialize 42-field production record及 linear occurrence
edge。只有符号相似、随机模型、条件 necessary identity、finite scalar completion、
complete-frequency mean或 averaged/metric statement均不得触发。

即使上述 local gate未来转正，all-`D` uniformity、exactly-once physical cover、
original/global normalization、tail-failure、A/B selection、actual packet attachment
与完整 provenance gates仍须独立通过；不得自动创建 TPC-207。

### 34.7 发布边界

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入仅为
`TPC_HANDOFF.md`；全部 protected untracked原样保留且不纳入提交。

```text
POST_WRITE_RELEASE_REGRESSION = 22/22 PASS
TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_GIT_DIFF_CHECK = PASS
POST_WRITE_MARKDOWN_FENCES = 872 MARKERS BALANCED
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = af5864a17063adc3084c9ce025878dadb39da05c
FINAL_SYNC_DELTA_FROM_INITIAL_4C8FC56
  = RH342_TO_RH348_119_RH_ONLY_FILES
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
RH_HANDOFF_CLOSURE = STALE_AT_RH341
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
RH_BUILDERS_EXECUTED = NO
```

正式写入后必须重跑第 1 节全部 22 项只读回归、TPC-111/124/126/127 四项
supplemental checks与 protected manifest；停掉所有分身后再 pull/rebase。只 stage
本 handoff，commit/push后必须验证 local `HEAD`、`origin/main`、remote
`refs/heads/main` 三个 hash完全一致。

## 35. 2026-08-03 TPC32/O161 扩展 primary-source 与 proof-integrity 审计

### 35.1 基线、有限范围与 fail-closed 协议

本轮启动时 HEAD 为
`86e4412feb82f72d0f9964ac337e1676fd325d1b`，`TPC_HANDOFF.md` 的启动
SHA-256 为
`5a2080964700b89e3a23d1187307614ebb1260e1e30d6594b5409cb8d9de648a`。
working tree没有 tracked/cached diff；只有第 1 节列出的五个本地 `.codex`
配置、TPC-105 `__pycache__`、TPC-63 构建产物与 `tmp/`。启动
`git pull --rebase origin main` 返回 already up to date；第 1 节 22 项只读启动
回归为 `22/22 PASS`。没有执行 TPC-27--32 legacy writers或 TPC-122 writer。

本轮由主控统一 source contract，并把长 theorem-body scan、proof adversarial
audit与候选排除交给三个 read-only agents；三者均回报同一 HEAD/handoff hash、
`files_changed=[]`、tracked/cached diff为空。正式写入仍只由主控完成。

有限检索以官方 arXiv source为准，覆盖：

1. 2026-08-03 `math.NT/new` 及 Mobius/Liouville/correlation/signed-prefix关键词；
2. 此前未冻结的 automorphic large-sieve、character-family mean、random或
   constructed multiplicative-function候选；
3. `math.DS/recent` 与第 33 节 O161 candidate IDs的官方 version delta；
4. Grimmelt--Merikoski新版本/Part II与 actual evaluation-cloud frame theorem；
5. Carella `arXiv:2208.12219v8` 的 primary PDF proof chain。

这是截至本日、对这些明示来源与版本的有限审计；不是全局文献
nonexistence claim。任何 checker、source type或公式合同非零/不一致均 fail closed。

### 35.2 TPC32 三个开放接口的未冻结候选 source lock

同一 theorem-valid selected packet仍固定为

```text
sigma=1/10000, lambda=99979/210000, delta=7/60, beta=267/400,
Q=X^(267/400+o(1)), J=X^(133/400+o(1)), C=floor(J),
h0=2, N0=JQ^2 asymp XQ.
```

三个互不替代的目标仍是：

1. actual three-channel `A_C` 的 distinguished determinant DFT zero；
2. fixed-`D0` literal weighted equal-difference four-Mobius energy `E_Psi`；
3. actual GM evaluation Dirac cloud的 full self-kernel/cross-`D0` block-Bessel。

逐 theorem-body结果如下：

| source/version | source-stated strongest nearby object | first fatal for TPC |
|---|---|---|
| Pascadi--Thorner `2508.14888v2` | automorphic representation families的 GL_n large sieve与 Dirichlet coefficients | `a(n),lambda_pi(n)`不是 actual `g_t` evaluation cloud或其 Gram kernel；无 coefficientwise index/operator intertwiner |
| Conrey--Kwan--Lin--Turnage-Butterbaugh `2607.00282v1` | 对 moduli、primitive even characters与 spectral parameter作 harmonic-family mean | family average不是 actual cloud的 pointwise full/cross-`D0` operator bound |
| Schmidt `2604.23517v1` | 在文中 independence assumptions下研究 Mertens/auxiliary partial sums | conditional single-sum model不是 literal two-affine packet，输出方向也不是所需统一 upper cancellation |
| Harper--Soundararajan--Xu `2606.29040v1` | Steinhaus random multiplicative function的 short-interval distribution theorem | independent random prime values不是 deterministic Mobius或 prescribed packet/phase |
| Klurman--Munsch--Sun `2605.04694v1` | 构造 completely multiplicative `f:{N}->{+/-1}` 或自由 signs，使 logarithmic sums沿子列很小 | constructed coefficients、`1/n` normalization与 subsequence existence都不是 actual `A_C,w_m` natural growing prefix |

因此五项都在 exponent audit之前失败。没有一项同时接受 literal physical
coefficient、fixed `h0=2`、actual prefix order、全部 `X/N/q/J/Q/C` ranges、
uniform constants、actual masks/weights/content/`Delta#`/outer labels、`N0`
normalization与完整 physical-loss ledger。

特别地：

* TPC-111/122只给 ordered prefix/BV transfer的 exact conditional calculus；当前
  仍没有把 TPC-32 physical triples coefficientwise映到同一 ordered fibers、同时
  保留三 raw channels、content、`Delta#`、masks/weights、outer labels与 `N0` 的
  production intertwiner；
* TPC-124 的 abstract `(J Q_D-Q_Z)M=0` 没有 actual common-leaf basis/matrices；
  finite one-vector equality不能补写为 production map；
* 通用 large sieve或 Hilbert-space Cauchy不能把裸
  `Q^(1/2)=X^(267/800+o(1))` 损失降为 strict `1/400` 可支付的 actual frame常数；
* random、conditional、freely constructed或 logarithmically normalized sources
  不得跨 coefficient/normalization gate。

所以本轮新增的 TPC32 source-version scope为：

```text
DECLARED_TPC32_20260803_UNFROZEN_SIGNED_PREFIX_AND_AUTOMORPHIC_
LARGE_SIEVE_SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

它不关闭 TPC32 direct theorem interface、fixed-`D0` literal theorem route或
full/cross-`D0` frame parent。

### 35.3 O161 `arXiv:2607.29275v1` spectral-process transfer

官方 `math.DS/recent` 新增 el Abdalaoui
`arXiv:2607.29275v1`，提交于 2026-07-31；第 34 节只筛
`math.NT/new`，故该 source此前未冻结。对第 33 节全部既有 candidate IDs的官方
version复核没有发现 2026-08-01 后新版本；本项是唯一新的 O161 delta。

其最接近 statements为 Theorem 3.1/Proposition 3.3的 countable-Lebesgue/
absolute-continuity spectral assertions，以及 Corollary 4.4中 source-stated

```text
(1/N) sum_(n<=N) omega_n a_n(phi,T,v,(n_r)) -> 0
```

for a singular-spectrum operator and one Mobius--Sarnak process coordinate weight
`omega_n=f1(T^n x)`。正文没有给用于 TPC 的定量 error；Question 6.4 的 moving
short interval仍只是 question。

O161 actual core却是

```text
q=as,
t(z)=ad+qz,
c_z=mu(d+s*z) mu(u+a*z),
su-ad=2.
```

第一 fatal是 literal coefficient：单 process weight没有被 source-backed theorem
识别为该 two-affine product。其后还依次缺 fixed physical `h0`、growing
`a,s,d,u` ranges、named production atom、actual masks/weights/outer labels、
uniform fixed positive-power error与 loss ledger。完整 `1/N` process prefix既不是
DIRECT 的 `q/N` terminal block，也不是经 TPC-159 exact telescoping后的 BAD
`q/T` cumulative prefix。

把 `omega_z` 直接设为 `c_z`没有 theorem依据；把第二个 Mobius factor塞入
singular-spectrum test也没有 affine-subsequence或 spectral-class证明。即使反事实
先接受该 mapping，由定性 `o(1)`作 block difference仍不能生成 uniform
`X^{-sigma}`、正确 `q/N`/`q/T` normalization或完整 telescoping ledger。

因此新增且仅新增：

```text
DECLARED_O161_CURRENT_PRIMARY_ARXIV_2607_29275V1_
SPECTRAL_PROCESS_TRANSFER_V1 = STOP_SCOPED
```

两个 O161 pointwise parents继续 `OPEN`。

### 35.4 Carella v8 proof-chain integrity hardening

Carella `arXiv:2208.12219v8` 已在第 31.3 节作为 periodic extension进入既有
source-candidate scope。本轮直接复核 official v8 PDF后，确认至少三项彼此独立的
critical proof failure。

第一，Theorem 6.2 的 `(6.6)` 只给每个频率

```text
|R_hat(s)| <= C x^2/(log x)^(2c).
```

inverse DFT `(6.7)` 为

```text
R(t)=(1/x) sum_(s<=x) R_hat(s) e(-st/x).
```

从逐频率 modulus bound合法得到的 triangle bound至多仍是
`C x^2/(log x)^(2c)`。论文在 `(6.8)` 中把随 `s` 变化、相位未知的
`R_hat(s)`替换成共同正上界后，却继续利用 root-of-unity cancellation得到
`x/(log x)^c`；该不等式无效。取
`R_hat(s)=M e(st/x)`即可显式看到共同 modulus bound不能保留该 cancellation。

第二，Lemma 3.1 `(3.1)--(3.2)` 声称对全部 `1<=a<q<=x`，residue count相对
`x/q` 的 error为 `O((x/q) exp(-c sqrt(log x)))`。取任意大整数 `x`、
`q=x-1,a=1`，`n<=x` 且 `n=1 mod q` 的解为 `1,x`；左侧 error趋于 `1`，
右侧趋于 `0`。故该 lemma为假，且不能由 large-sieve aggregate upper bound推出
逐 residue exponentially-small error。

第三，Lemma 6.2 `(6.24)` 先使用 compatibility
`d1|n,d2|n+1` 推得 `gcd(d1,d2)=1`，随后却把相应 coupled/coprime-restricted
double sum因子化为 unrestricted square

```text
x (sum_(d<=x) mu(d)/d)^2.
```

若 double sum保留 compatibility/coprimality，该因子化非法；若按 displayed
unrestricted ranges理解，则前述 compatibility premise已被丢弃。两种读法都不能
推出 `(6.24)`。

故 `2208.12219v8` 不能注册为 theorem input。即使反事实接受其结论，对象仍是
人工 prime-periodic finite Mobius vector上的 bare complete-period shifts，缺 actual
affine slopes/intercepts、progression、masks/weights、phase、canonical all-prefix、
packet labels与 normalization；固定 `c` 的 `(log X)^(-c)=X^(-o(1))` 也不是
支付 strict `1/400` 的 fixed positive-power saving。

这一结果只加固第 31.3 节既有
`DECLARED_TPC32_FIXED_D0_OUTER_REGROUP_AND_POST30_DIRECT_FRAME_SOURCE_CANDIDATES_V1`
scope；不新增 Carella method cell，不重开第 6 节旧 STOP，也不把 proof error
包装成新的 arithmetic method。

### 35.5 committed edge、pair/H1 与状态防火墙

对 TPC-32/111/122/124/126/127、TPC-18/205/206与 O161 相关 committed
artifacts做 adversarial crosscheck后，没有发现漏掉的 theorem edge：

```text
LOSSLESS_A_C_ZERO_TO_ORDERED_PREFIX_COEFFICIENTWISE_INTERTWINER = ABSENT
ACTUAL_GROWING_PREFIX_SAVING = ABSENT
ACTUAL_OUTER_BV_AND_CONTENT_REMAINDER_THEOREM = ABSENT
PAIR_NATIVE_42_FIELD_PRODUCTION_RECORD = ABSENT
PAIR_TO_OMEGA_THEOREM = ABSENT
H1_LINEAR_OCCURRENCE_EDGE = ABSENT
O161_NAMED_ATOM_FIXED_POWER_THEOREM = ABSENT
```

TPC-206仍只是 selected `13/42` finite projection，first missing field为 `D`，且
`production_occurrence=false`；`d=1` row divisor不能被改名为 source-locked
opened dyadic scale `D=1`。即使擅自补 `D,J,Q`，其余 packet/source、mask、
coefficient AST、support/nonzero、source-child与四阶段 normalization fields仍缺。

TPC-205 pair carrier是 TT-star/Cauchy后的 bilinear object；H1要求 linear、
coefficientwise-conservative occurrence lift。没有 inverse aggregation theorem时，
pair-native carrier不得改写为 H1 edge。pair-native reroute与 H1 parent继续 `OPEN`。

### 35.6 精确裁决与合法 reopen interface

本轮精确有限裁决为：

```text
TPC32_O161_20260803_EXTENDED_PRIMARY_SCREEN_UNFROZEN_CANDIDATES_HAVE_
LITERAL_OBJECT_MISMATCH_AND_CARELLA_2208_12219V8_PROOF_CHAIN_IS_INVALID_
NO_TRIGGER_STOP_SCOPED_PARENTS_OPEN

THEOREM_TRIGGER = false
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_CREATED = false
```

第 6 节新增两个 source/version-scoped cells；Carella只加固旧 cell。所有旧
method cells保持 `STOP_SCOPED`，尤其 TPC193 V1、common-`k` V1、
tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1。两个 O161 pointwise
parents、TPC32 direct/fixed-`D0`/frame parents、pair-native reroute、H1与 global
architecture继续 `OPEN`。

只在出现下列任一 source-backed输入时重开对应 local parent：

1. 直接接受同一 high-beta packet的 literal `A_C`，并给 growing signed-prefix、
   BV/content envelope或 matched-shell distinguished-zero fixed-power saving；
2. 直接接受 literal `w_m/E_Psi` 的 deterministic prescribed-lag four-Mobius
   theorem，并支付 fixed-`D0` tiny-power threshold；
3. 直接控制 actual GM evaluation-cloud Gram operator的 full/cross-`D0` frame
   theorem，常数足以支付 strict `1/400`；
4. 在 named production atom上直接控制 O161 literal `c_z` 的 DIRECT `q/N`
   terminal blocks，或以 uniform fixed-power local theorem接入 TPC-159 BAD
   `q/T` telescoping；
5. materialize source-backed complete 42-field production pair及 pair-to-`omega`/
   normalization theorem，或给出真正 linear H1 occurrence edge。

任一 local gate转正也不自动创建 TPC-207；all-`D` uniformity、exactly-once
physical cover、original/global normalization、tail-failure、A/B selection、actual
packet attachment与完整 provenance gates仍须分别通过，并使页首数学 trigger
发生真实 theorem-backed状态变化。

### 35.7 发布边界

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入只允许
`TPC_HANDOFF.md`；全部 protected untracked必须原样保留且不纳入提交。

```text
POST_WRITE_RELEASE_REGRESSION = 22/22 PASS
TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_GIT_DIFF_CHECK = PASS
POST_WRITE_MARKDOWN_FENCES = 896 MARKERS BALANCED
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = 86e4412feb82f72d0f9964ac337e1676fd325d1b
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
SUBAGENT_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

正式写入后必须重跑第 1 节全部 22 项只读回归、TPC-111/124/126/127 四项
supplemental checks与 protected manifest。只 stage本 handoff；commit/push后必须
验证 local `HEAD`、`origin/main`、remote `refs/heads/main` 三个 hash完全一致。

## 54. 2026-08-05 大路 V3/V4：coarse audit、tensor-local redesign 与 `J -> sqrt(X) -> Q` compiler

### 54.1 目标、分工与非编号 scope

本 checkpoint 从已发布的 V2 commit
`3b3a39b7816ab5b8848999c2e23577b32de2f360`继续，不创建论文、PDF、paper
directory或 TPC-207。用户要求再次参考 `TPC_review3.md` 并“开始造大路”；主控据此
停止扩展微型 source cells，只做 literal Ford--Maynard prime-producing compiler。
三个 read-only agents分别完成：primary-source contract、locally matched comparison
architecture与 adversarial endpoint/composition audit，均回报 `files_changed=[]`。

V2 的两个 `b=1` candidate继续 `STOP_SCOPED`：normalized survivor与
`Lambda(n+2)`均在 multiplier `m=2`有 linear Type-I discrepancy。V3 不重开它们，
而是构造一个包含全部 local primes的 comparison，避免 fixed/growing `W` 的 residual
local-factor与 comparison-regularity分叉。

正式新增的未编号 working files为

```text
research/tpc-big-road/fm_local_comparison_compiler.md
research/tpc-big-road/tpc_fm_local_comparison_checker.py
```

并只更新 `research/tpc-big-road/README.md`、`TPC_COMPASS.md` 与本 handoff。checker
只验证 exact local algebra、exponent geometry与 endpoint mutations；它不把 open
Type II变成数值 theorem。

### 54.2 All-prime locally matched comparison

令

```text
C_2 = product_(p>2)(1-1/(p-1)^2),

a_x(n)=Lambda(n+2),

b_x(n)=2 C_2 1_(2 does not divide n)
       product_(p|n,p>2)(p-1)/(p-2),

w_x(n)=a_x(n)-b_x(n),
```

三者均截断到 `x/2<n<=x`。它不使用 twin locations、Hardy--Littlewood lower
bound或 future prime word；`C_2`只来自 convergent local Euler product。

对 `p>2`，`b` 的 local factor为

```text
v_p=p(p-2)/(p-1)^2       (p does not divide n),
u_p=p/(p-1)              (p divides n),
```

且 `(1-1/p)v_p+(1/p)u_p=1`；`p=2` 的 factors为 odd上 `2`、even上 `0`，
均值同样为 `1`。因此 comparison在 unconditional local model中精确 centered。

更强地，写

```text
g(d)=mu^2(d) product_(p|d)1/(p-2)       (d odd),
A(m)=product_(p|m,p>2)(p-1)/(p-2).
```

divisor expansion逐项给

```text
b_x(n)=2C_2 1_(n odd) sum_(d|n,d odd)g(d),

b_x(mr)=2C_2 A(m)1_(r odd)
         sum_(d|r,(d,2m)=1)g(d)          (m odd).
```

数 odd multiples与 Euler identity

```text
1+1/(p(p-2))=(p-1)^2/(p(p-2))
```

遂对任意位于 active quotient support
`I subset {r:x/2<mr<=x}` 的 integer interval给

```text
sum_(r in I)b_x(mr)
  =(m/phi(m))|I|+O(A(m)log^K(2+max I))   (m odd),

b_x(mr)=0                                 (m even),
```

其中一个固定 nonoptimized `K`足够。主常数与 `Lambda(mr+2)`在 reduced class
`2 mod m`的 AP main逐 multiplier完全一致；even `m`时 real side只余 powers of
two，累加为 `x^o(1)`。因此 V2 的 `m=2` fatal不是被 heuristic平滑，而是被 exact
local factor消除。

### 54.3 Ford--Maynard comparison gates 与 Type I

primary source为 Ford--Maynard, *On the theory of prime-producing sieves*,
`arXiv:2407.14368`：literal `(I)/(II)`见印刷页 2，`(w)`与 Theorem 2.2见印刷页
4，`(b.1)/(b.2)`与 Lemma 4.6见印刷页 12--13，Proposition 4.11见印刷页
14--15。

comparison gates逐项闭合：

1. 对 prime index `r asymp x`，
   `b_x(r)=2C_2(r-1)/(r-2)=2C_2+O(1/x)`，PNT给
   `sum_(prime r)b_x(r)~C_2x/log x`，故 `(b.1)`；
2. `(b.2)` 的 vector region有 `p_i>=(x/2)^nu`与 bounded `k`，故
   `b_x(p_1...p_k)=2C_2+O_nu(x^-nu)`，包括 repeated factors。对
   Ford--Maynard Lemma 4.6取 `q=1,y=x/2`所得完整 constant-comparison
   generalized PNT（不是只用 ordinary one-dimensional PNT），uniform perturbation
   即给全部 convex `T`与 Lipschitz `f`量词；
3. `b_x(n)<<tau(n)`、`a_x(n)<=log(2x)`与 fixed divisor moments给 `(w)`；
4. 对任意固定 `gamma<1/2`，maximal Bombieri--Vinogradov控制 odd multiplier的
   AP remainder。其无权版本可通过 divisor-level split推出 literal `tau(m)^B`
   weight：低 divisor层由增大 BV log saving吸收；高 divisor层用 trivial row bound
   `E_m<<x tau(m)log x/m`、Markov与更高 fixed divisor moment吸收。comparison
   endpoint errors总和为 `O(x^gamma log^Kx)`。

故当前 theorem ledger为

```text
FM_LOCALLY_MATCHED_COMPARISON = PROVED_EXACT
FM_COMPARISON_b1_b2_w = PROVED
FM_MAXIMAL_TYPE_I_EVERY_FIXED_GAMMA_LT_1_2 = PROVED_SOURCE_BACKED
```

这里 Type I是现有 classical distribution input的严格推论，不是新 level of
distribution，也不覆盖 exact `gamma=1/2`。

untruncated comparison还具有 exact Ramanujan normal form

```text
b^(2,circ)(n)=S(2n)=sum_(q>=1)mu(q)^2/phi(q)^2 c_q(2n),
b_x(n)=1_(x/2<n<=x)b^(2,circ)(n),
```

其 prime-local factor恰为 `1+c_p(2n)/(p-1)^2`。因此它是同一 `mn` product上的
complete local major-arc model，不是只匹配 scalar mean。

### 54.4 `P_TPC` exponent compiler

取

```text
J=133/400,
nu=67/400,
Q=267/400,

P_TPC=(gamma,theta,nu)=(1/2,J,nu).
```

exact identities为

```text
J+nu=1/2,
1-J=Q,
1/3-J=Q-2/3=1/1200.
```

mirror后的 full-window ledger另有

```text
gamma_sharp=Q=267/400,
nu_sharp=Q-J=134/400,
gamma_sharp+nu_sharp=401/400=1+1/400.
```

Ford--Maynard引言的 Vaughan sufficient condition是 `gamma+nu>1`，故 literal
full `J/Q` Type II恰以 strict `1/400`越过该门槛。Proposition 4.11的 complementary
upper endpoint为 `(x/2)^Q`；若采用 full-window Vaughan shortcut，仍须显式做有限
rescaling/reblocking以覆盖到 `x^Q`。下述 exact-half-window Theorem 2.2 route不依赖
这个 presentation shortcut。无论采用哪一表述，未证 Type II都不给 current
`1/400` credit。

Ford--Maynard Theorem 2.2中 `M=floor(1/(1-gamma))=2`。`A1` 对所有
`n>=3`可取 `a/n`于 `[1/3,1/2] subset [J,1/2]`；`A2`取 `h=1`，
`h(1-gamma)=1/2`恰为 closed endpoint。故 `P_TPC`在 asymptotic region，无需
另行数值优化 `C_minus`。

若 literal Type II在

```text
(x/2)^J < m <= x^(1/2)
```

成立，Proposition 4.11自动给 complementary window

```text
x^(1/2) <= m <= (x/2)^Q
```

与对应 maximal Type-I rows，只损一个可预付的 log power。它尤其填补 classical
BV 的 `sqrt(x)/log^Lx`到 exact `sqrt(x)` fringe；于是 Theorem 2.2给

```text
sum_(x/2<r<=x,r prime)w_x(r)<<_A x/log^A x.
```

外层 `r+2=q^j,j>=2` prime-power tail为 `O(sqrt(x)log x)`，故条件式地得到

```text
#{x/2<r<=x : r and r+2 prime}
  ~ C_2 x/log^2x.
```

这说明 compiler若闭合会真正推出 TPC；它不说明其最后输入已经证明。

### 54.5 唯一 direct-compiler大墙与 typed no-go

本小节保留 V3 的原始 candidate contract作为历史记录；第 54.8 节已经用合法
mod-3 rank-one witness证明该 contract对 coarse comparison为 false。因此以下
`OPEN`字样不得再作为 current state；current replacement由第 54.9--54.11 节控制。

当前首缺精确命名为

```text
TPC_J_TO_SQRT_UNIVERSAL_MULTIPLICATIVE_TYPE_II:

sup_(|xi_m|<=tau(m)^B, |kappa_n|<=tau(n)^B)
|sum_((x/2)^J<m<=sqrt(x), x/2<mn<=x)
 xi_m kappa_n
 [Lambda(mn+2)
  -2C_2 1_(mn odd)product_(p|mn,p>2)(p-1)/(p-2)]|
 <<_B x/log^B x.
```

它要求同一 `w_(mn)`、full literal window、exact square-root endpoint与全部 arbitrary
divisor-bounded coefficients。任何 `x^(J+delta)` lower loss、
`x^(1/2-delta)` upper loss、terminal block、single selected coefficient、additive
`n-m` covariance或 averaged phase statement都不够。

现有 TPC-32/34/37与 O161不能直接登记为这个 Type II：前者是 post-TT-star
Gram/energy，后者是 determinant-two affine double-Mobius atom；它们与 FM的
multiplicative `mn` product domain、arbitrary `xi/kappa`、linear `w_(mn)`及
normalization不同。特别是 packet natural scale `N0=JQ^2 asymp XQ`，而 FM
domain为 `mn asymp x`。`J/Q`指数对齐只使这些对象成为候选证明 engine，不产生
coefficientwise crosslink。

因此新增 broad direct-composition verdict为

```text
DECLARED_TPC_REVIEW3_20260805_CURRENT_O161_PACKET_TO_FM_UNIVERSAL_TYPE_II_
DIRECT_COMPOSITION_V1 = STOP_SCOPED
```

该 STOP只封锁“凭指数相同直接等同”；不封锁从 Vaughan/Heath--Brown identity
逐 coefficient导出同一 FM bilinear form，再经 actual occurrence、ranges、masks、
signs、multiplicities与 normalization证明一个合法 operator map。

### 54.6 first exact decomposition bridge：`dr-mn=2`

在进入下一轮 source search前，两种等价 exact identities

```text
Lambda(N)= sum_(d r=N)mu(d)log r
         =-sum_(d|N)mu(d)log d
```

已把 FM prime part逐项写成

```text
Lambda(mn+2)= sum_(d r-m n=2)mu(d)log r
            =-sum_(d r-m n=2)mu(d)log d.
```

非 negligible odd sector中 `gcd(d,m)|2`迫使 `gcd(d,m)=1`。固定 `(d,m)`与一组
base solution `d r0-m n0=2`后，全部 solutions精确为

```text
n=n0+d z,
r=r0+m z,
d(r0+mz)-m(n0+dz)=2.
```

这给 FM shifted-prime wall到 O161 abstract determinant-two geometry的第一个
source-forward exact bridge，不再只是 `J/Q` numerology。第一种写法还逐 coefficient
命中已提交 TPC-31 `comparison-next-gate.tex`要求的 prime--Möbius core
`mu(d)(log ell)`，只需 rename `r=ell`。这项吻合发生在 physical cutoffs与 `TT*`
之前，故是 exact formula-level bridge。但完整 coefficient仍不一致：TPC-31的
`omega_D(d)psi_L(ell/L)`、fixed residue factors、bounded pair mask、three-channel
physical weights都未附着；它也不是 O161 literal
`mu(d0+s z)mu(u0+a z)`。arbitrary `xi/kappa`、growing scales、prefix与 packet
normalization同样未附着。因此登记

```text
FM_TO_PRIMITIVE_DETERMINANT_TWO_GEOMETRY = PROVED_EXACT
FM_TO_TPC31_PRIME_MOBIUS_CORE = PROVED_FORMULA_LEVEL
FM_TO_O161_LITERAL_TWO_MOBIUS_COEFFICIENT = OPEN
FM_TO_CURRENT_PACKET_PHYSICAL_ATTACHMENT = ABSENT
```

下一 gate应先对 outer prime detector作 coefficientwise Vaughan/Heath--Brown
decomposition，判断其中的 Mobius factor能否与上述 inner determinant lift组成同一
two-Mobius affine atom；不得从 post-TT-star Gram逆造该 factor。

source lock随后把 Section 54.5 universal Type II的 prime part写成

```text
sum_(d r-m n=2) mu(d)(log r) xi_m kappa_n.
```

第一处 theorem mismatch不在 fixed shift `+2`，也不在 arbitrary log saving，而在
一个 fixed rough `mu(d)`与两组 arbitrary rough `xi_m,kappa_n`。ABL/Titchmarsh与 BFI只覆盖
unweighted、fixed-character或 well-factorable modulus structures；DFI/Kuznetsov
允许 arbitrary two-sided coefficients时 kernel已经是 dispersion后的 reciprocal
exponential；Bettin--Chandee fixed-determinant corollary只有两个 arbitrary-weight
slots，其余坐标要求 smooth；asymptotic sieve则把专门的 Mobius bilinear estimate
作为输入公理。因此当前精确状态是

```text
CURRENT_FIXED_MOBIUS_PLUS_TWO_ARBITRARY_ROUGH_DETERMINANT_SOURCE = ABSENT
CURRENT_UNIVERSAL_TYPE_II_CLOSED_SQRT_ENDPOINT = OPEN_SECOND_LEVEL
```

这是 primary-theorem source lock，不是 no-go theorem。它把下一轮从“继续扫一个
现成万能定理”改成“对实际 Vaughan/Heath--Brown输出的 structured coefficient
families重编译 dispersion”；不得把 arbitrary `xi/kappa`悄悄降格，也不得把
两 arbitrary plus smooth的 determinant theorem升级为三 rough weights。

### 54.7 状态、路线与下一项大动作

本小节是 V3 checkpoint的历史状态，已由第 54.8--54.19 节的反例、hybrid
redesign覆盖；尤其不得继续把 coarse universal Type II记为 `OPEN`。

本 checkpoint是 `ARITHMETIC_ROUTE_ADVANCE`：comparison selection、comparison
regularity与 sub-square-root Type I从 `NOT_CONSTRUCTED/OPEN`推进为 proved。它不是
TPC theorem trigger，因为 universal Type II仍完全 `OPEN`，existing fixed-atom
credit仍为 `0`。

第 6 节全部既有 method cells继续 `STOP_SCOPED`，尤其 TPC193 V1、common-k V1、
tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1。两个 O161 pointwise
parents、pair-native reroute、legacy H1与 global architecture继续 `OPEN`；
fixed-atom credit=`0`、strict `1/400=UNPAID`、`L2=NONE`。H3 metric theorem继续
有效，但对本 FM Type II不给 arithmetic credit。

下一项只做一个大动作：

```text
TPC_FM_J_TO_SQRT_TYPE_II_DECOMPOSITION_GATE
```

即对 Section 54.5 的同一 `w_(mn)`做 coefficientwise Vaughan/Heath--Brown/Buchstab
decomposition，枚举覆盖 `[J,1/2]` 的全部 bilinear shapes，并只寻找能对 arbitrary
coefficients给 uniform log-power norm的 dispersion/spectral入口。若分解后存在一个
不可由当前 analytic engines覆盖的 shape，发布一个 broad decomposition STOP/OPEN
map；不得为每个 shape生成微型论文。即使 Section 54.5将来转正，也必须另过全部
actual attachment、physical cover、tail/A-B、normalization与 provenance gates，
方可判断是否创建 TPC-207。

### 54.8 V4 fatal audit：coarse universal Type II为 false

第 54.5 节的 coarse candidate不是一个尚待 source填补的 theorem，而有 elementary
local rank-one反例。取 `M=X^(1/3)`，在 product完全落入 `(X/2,X]` 的两个固定
constant-ratio boxes上取

```text
xi_m    = 1_(m=1 mod 6),
kappa_n = 1_(n=1 mod 6).
```

由于 `J=133/400<1/3<1/2`，该 `m`-box位于 literal Ford--Maynard Type II window。
支撑上的每个 `mn`为 odd且 `mn+2=0 mod 3`。所以 `Lambda(mn+2)`仅在
`mn+2=3^j`时非零；全部此类 exceptional factor pairs的 weighted contribution为
`X^o(1)`。但 coarse `b^(2)(mn)>=2C_2`，且所选 residue pairs有
`cX+o(X)`个，故 bilinear discrepancy为

```text
-c' X+o(X).
```

这否定任意 `X/log^B X` saving，并登记

```text
DECLARED_COARSE_SINGULAR_SERIES_COMPARISON_UNIVERSAL_TYPE_II_
MOD3_RANK_ONE_V1 = STOP_SCOPED_FALSE
```

fatal type是“slice mean不等于 tensor-local mean”：固定 `m`后对 `n`平均确实只看
`m/phi(m)`，但 arbitrary `xi_m kappa_n`可同时选两边 residue class并探测
`mn=-2 mod p`。coarse comparison的 exact multiplier constants、comparison
regularity与每个固定 `gamma<1/2` 的 Type I不受此反例影响；只有它的 two-sided
universal Type II被永久封锁。

### 54.9 Tensor-local hybrid replacement

对 `z>=2`定义

```text
C_(2,>z)=product_(p>z)(1-1/(p-1)^2),

b^(z,circ)(n)
 = C_(2,>z)
   product_(p<=z)[p/(p-1) 1_(p does not divide n+2)]
   product_(p|n,p>z)(p-1)/(p-2),

b_x^(z)(n)=1_(X/2<n<=X)b^(z,circ)(n).
```

`z=2`精确给回 coarse `b^(2)`。对 `p<=z`与 `p>z`，local factors分别为

```text
F_p(t)=p/(p-1) 1_(t!=-2 mod p),

G_p(t)=p/(p-1)                    if t=0,
       p(p-2)/(p-1)^2            otherwise.
```

两者在 `F_p`上平均均为 `1`。若 `p|m`，则 `mr=0 mod p`且两者都给
`p/(p-1)`；若 `p`不整除 `m`，对 `r`平均仍为 `1`。`p=2`给 exact parity。
因此 hybrid同时保持所有 multiplier main term，并精确匹配每个 `p<=z` 的
product-residue condition `mn!=-2 mod p`。这是无条件 finite Euler theorem。

遗漏 odd prime `p>z`时，在 `F_p^* x F_p^*`上的 residual为

```text
D_p(a,b)=p/(p-1)^2 [1-(p-1)1_(ab=-2 mod p)].
```

其 bounded bilinear norm为 `Theta(p)`：任一 nontrivial quadratic character给
绝对值恰为 `p`的 witness，row `ell^1`给 `O(p)` upper bound。乘每个 residue cell
的 `asymp X/p^2` mass，单 prime obstruction为 `Theta(X/p)`。故一次固定 saving
`B`至少要求 `z>=log^(B+O(1))X`。可以对该固定 application取
`z=log^K X,K=K(B)`；不得把一个 fixed `K`说成同时支付全部 `B`。

当前 replacement package为

```text
H0  exact hybrid local Euler profile                 PROVED_EXACT
H1  hybrid (b.1)/(w), each fixed z=log^K X          PROVED_SOURCE_BACKED
    hybrid (b.2) at exact P_TPC                     VACUOUS_PROVED_R_EMPTY
H2  hybrid maximal Type I, every fixed gamma<1/2    PROVED_SOURCE_BACKED
    hybrid maximal Type I at gamma=1/2              NOT_PROVED_BY_BV
H3  hybrid universal Type II on [J,1/2]             OPEN_HIGH_CONDUCTOR_WALL
```

H1/H2已由 polylogarithmic small-prime sieve的 fundamental lemma加 maximal
Bombieri--Vinogradov闭合。对 prime indices，local density为 `1/(p-1)`，sieve
normalization精确乘回 `2C_2`，给 `sum_(r prime)b_x^(z)(r)~C_2X/log X`；`(w)`由
`b_x^(z)(n)<<_K(log z)tau(n)`与 fixed divisor moments得到。对 odd multiplier，exact
slice expansion为

```text
b_x^(z)(mr)=C_(2,>z)W_z A_z(m)h_(m,z)(r)
            1_((mr+2,P(z))=1),
```

且 sieve density与 high-prime Euler factor逐 prime乘成 `m/phi(m)`。长 interval用
power-level fundamental lemma，短 interval用 trivial bound；外层 `tau(m)^B`尾由
higher fixed divisor moments吸收。real side用 maximal BV；even `m`仅余
`mr+2=2^j`，总计 `X^o(1)`。结论只对每个 fixed `K`、每个 fixed
`gamma<1/2`成立，constants可在 `gamma->1/2`时爆炸；不得升级 exact half。

H3已没有 fixed-prime rank-one反例，但仍须 collectively控制所有 `p>z`及
shifted-prime determinant dispersion。

### 54.10 Exact determinant bridge与两个诚实 analytic forks

exact Mangoldt identity继续给

```text
Lambda(mn+2)=sum_(dr-mn=2)mu(d)log r
            =-sum_(dr-mn=2)mu(d)log d.
```

odd sector中固定 coprime `(d,m)`后，全部 solutions为
`n=n_0+dz,r=r_0+mz`，determinant恒为 `2`。第一式在 `r=ell`后与 TPC-31
next gate的 `mu(d)log ell`逐 coefficient相同，故

```text
FM_TO_PRIMITIVE_DETERMINANT_TWO_GEOMETRY = PROVED_EXACT
FM_TO_TPC31_PRIME_MOBIUS_CORE = PROVED_FORMULA_LEVEL
FM_TO_CURRENT_PACKET_PHYSICAL_ATTACHMENT = ABSENT
```

这里缺的不是命名，而是 `omega_D(d)psi_L(ell/L)`、fixed residues、actual masks、
三条 raw channels、physical scales、outer decomposition coefficients与完整
provenance。不得从 post-`TT*` Gram逆造这些 linear factors。

published Ford--Maynard direct route的 Type II假设确实对 arbitrary two-sided
divisor-bounded sequences取 supremum；在其 proof中，modified Heath--Brown atoms
最终被包进 arbitrary beta envelope。因此不能把 published hypothesis直接改称
“structured”。但在该 supremum之前，actual atoms只有 bounded-depth truncated
Mobius、至多一个 log、interval/Mellin factors与 perfect-power remainder。由此只留
两个诚实 fork：

```text
U: 对 hybrid comparison证明 published universal H3；

S: 在 arbitrary-beta supremum之前重做 Ford--Maynard extraction，保留 actual
   Mobius/log/truncation atoms，并另证 structured determinant estimates及 exact
   square-root Type-I fringe。
```

Fork S是新 compiler lemma，不是 Ford--Maynard原文的 corollary。把参数镜像成
`P#=(Q,J,Q-J)`虽显式露出 `1/400` surplus，却同时要求 Type I直到 `X^Q`，普通
Bombieri--Vinogradov不够；primary redesign仍应使用 exact-half `P_TPC`。

bounded primary scan中，Assing--Blomer--Li/BFI、DFI reciprocal-exponential estimates、
Bettin--Chandee fixed-determinant bounds与 asymptotic sieve各覆盖相邻结构，但没有
literal给出 product-domain上 fixed `mu(d)`加两组 arbitrary rough `xi_m,kappa_n`
的 closed-square-root norm。这是 scoped source lock，不是全局 no-go theorem。

### 54.11 V4 current verdict与下一 gate

V4的真实推进有四项：发现并永久封锁 coarse Type II伪公路；构造并精确验证
tensor-local hybrid local profile；用 fundamental lemma与 maximal BV闭合 hybrid
H1/H2 classical compiler；把 shifted Mangoldt到 TPC-31 prime--Mobius core的联系
提升为 formula-level exact bridge。它尚未证明 hybrid H3，因此不是 TPC theorem
trigger。

```text
TPC_BIG_ROAD_V4 = ARITHMETIC_ROUTE_CORRECTION_AND_TENSOR_LOCAL_ADVANCE
COARSE_TYPE_II = STOP_SCOPED_FALSE_MOD3_RANK_ONE
HYBRID_H0 = PROVED_EXACT
HYBRID_H1_H2 = PROVED_SOURCE_BACKED_FOR_EACH_FIXED_K_AND_GAMMA_LT_HALF
HYBRID_GAMMA_EQUAL_HALF = NOT_PROVED_BY_BV
HYBRID_H3 = OPEN_HIGH_CONDUCTOR_WALL
TPC31_ATTACHMENT = FORMULA_MATCH_ONLY
STRICT_1_OVER_400 = UNPAID
FIXED_ATOM_CREDIT = 0
L2 = NONE
TPC_207_TRIGGER = false
```

本 checkpoint当时的下一项大动作为（现已由第 54.12--54.13 节完成 fork决策并覆盖）

```text
TPC_FM_HIGH_CONDUCTOR_TYPE_II_FORK_DECISION_GATE = SUPERSEDED_BY_DIRECT_HB2_SHB_D2.
```

H1/H2不再重复；只选择 U/S一个 fork推进 H3，不为每个 decomposition shape生成
paper。第 6 节全部旧 `STOP_SCOPED`
cells保持，尤其 TPC193 V1、common-k V1、tail-failure/A/B V1与 full-`r_Rr_R`
ultra-complement V1。两个 O161 pointwise parents、pair-native reroute、H1与 global
architecture保持 `OPEN`。即使 selected analytic gate转正，也须另过 all-D
uniformity、exactly-once physical cover、original/global normalization、tail-failure、
A/B selection、actual packet attachment与 provenance，方可重新判断 TPC-207。

### 54.12 Direct modified-HB2 shortcut：从通用 79-slot closure降到四槽

第 54.10--54.11 节的 fork决策经 source/proof/adversarial三重审计后进一步收缩。
沿 Ford--Maynard Proposition 7.22的通用 proof重做 structured `S+`虽逻辑上可能，
但即使 `R(P_TPC)=empty`删除 nontrivial `lambda` branch，仍保留最多 `k ell<=60`
个 prime-decomposition slots与至多 `19` 个 rough largest-prime blocks。只证明 raw
`mu/log` atoms不足；证明完整 closure则远宽于本题。故

```text
S_PROP722_RAW_HB = FAIL_INCOMPLETE_COEFFICIENT_LANGUAGE
S_PROP722_FULL_STRUCTURED_CLOSURE = DEPRIORITIZED_BROADER_THAN_NEEDED
```

selected shortcut直接令

```text
w_x^(z)(n)=Lambda(n+2)-b_x^(z)(n)
```

并对 prime residual使用 Ford--Maynard Lemma 5.2的 modified Heath--Brown identity，
取最小安全值 `h=2`。乘以 `w_x^(z)(n)/log n`后，这是 dyadic prime sum的 exact identity。
`r>=2`只支撑 exact perfect powers；固定 `K`时
`|w_x^(z)(n)|<=log(2x)+O(log z tau(n))=x^o(1)`，连同 bounded factorization
multiplicity总计 `x^(1/2+o(1))`。这一 disposal只对当前 literal sequence成立，
不得升级为 abstract `(w)` theorem。

`r=1`时 `1<=j<=2`，每项只有

```text
n=e_1...e_j f_1...f_j,   e_i<=x^(1/2),
coefficient=product_i mu(e_i) * log(f_1)/log(n),
```

故最多四个 literal variables、两个 HB Möbius slots与一个原始 log slot。按固定顺序
取第一个 factor `u>=sqrt(n)`。若它是 smooth `f_q`，补乘积 `D=n/f_q<=sqrt(n)`，
其中 `D<=x^J`由已证 H2 at fixed `gamma=J`支付，其余进入 structured master。若它
是 `e_i`，则 `e_i<=sqrt(x)`与 `n>x/2`强制 `e_i`及补乘积都位于 constant-factor
square-root corridor，直接进入同一 master。若不存在 large factor，删除 unit slots后
所有 normalized log exponents严格小于 `1/2`；
`R(P_TPC)=empty`保证某个 subset exponent sum落在 `[J,1/2]`。固定 first-admissible
subset并 exactly-once分割，所得乘积满足 literal

```text
(x/2)^J<M<=sqrt(x).
```

`h=1`不安全：它允许带 Möbius weight的 `e`远大于 `sqrt(x)`，而其补因子可低于
`x^J`；该项既不能由 unweighted inner Type I支付，也不落 `[J,1/2]` master。
joint failed-subset cutoffs须用有限 Perron/Mellin或等价 bounded partition分离；
`rho_x(t)=log x/log t`须保留为唯一 global smooth factor，或作任意所需固定阶的
dyadic log expansion并把完整 remainder记入 ledger。不得无损替换成常数。

### 54.13 Selected master `SHB-D2`与 current route state

令 `C_HB2`为上述至多四槽 actual atoms在 hard interval/product selectors、real
power twists、bounded log powers与 bounded-depth grouping下的 finite emitted closure。
它由 source decomposition固定，不依赖 future prime outcomes。selected analytic
master为

```text
(SHB-D2)
sup_((Xi,Kappa) emitted by C_HB2)
| sum_((x/2)^J<m<=sqrt(x), x/2<mn<=x)
    rho_x(mn)Xi(m)Kappa(n)
    [sum_(dr-mn=2)mu(d)log r-b_x^(z)(mn)] |
 <<_(A,K) x/log^A x.
```

direct identity、perfect-power disposal、large-complement/H2 split与
`R(P_TPC)=empty` cover共同给出

```text
DIRECT_HB2_EXTRACTOR = PROVED_EXACT_REDUCTION_TO_SHB_D2
C_HB2_TEMPLATE_LANGUAGE = PROVED_FINITE_SOURCE_EMITTED
SHB_D2 = SELECTED_PRIMARY_OPEN_NEW_THEOREM
H3_U = OPEN_RESERVE_NO_COUNTEREXAMPLE_BUT_OVERSTRONG
```

这是真实路线压缩，不是 H3 theorem。Bettin--Chandee/DFI型 reciprocal fractions、
unbalanced prime-convolution与 asymptotic-sieve sources只有在 determinant range
atlas逐项匹配 coefficients、variables、smoothness、ranges及 uniform constants后才可
调用；当前没有 black-box theorem覆盖完整 master。published Proposition 4.11或
Theorem 2.2本身都以 universal `(II)`为输入，调用它们支付 exact square-root fringe
会循环。

本 checkpoint的 range-atlas gate为（现已由第 54.14--54.15 节完成并覆盖）

```text
TPC_FM_SHB_D2_DETERMINANT_RANGE_ATLAS_GATE = COMPLETED_TO_HB2_B3_AND_ONE_POISSON_STOP.
```

它只把 actual HB2 templates分为 comparison main、small-divisor/degenerate与
high-conductor determinant ranges，寻找最小中央未覆盖类；不再扩张 generic closure，
不为各 shape生成论文。即使 `SHB-D2`转正，也只闭合 arithmetic prime-producing
engine；TPC-31 packet attachment、all-D cover、physical normalization、tail/A/B与
provenance仍须分别通过，TPC-207不会自动触发。

### 54.14 V5 determinant range atlas：最小 three-rough core与 source边界

range atlas先验证了正控制。对 `h=2,j=1`的 `dr-ef=2`，把 `mu(e),mu(d)`放入
Bettin--Chandee Corollary 1的两个 arbitrary slots，并把 `log r,log f`放入两个
smooth slots。若 `E=x^a,D=x^v`，published error exponent为

```text
Gamma(a,v)=17(a+v)/20+max(a,v)/4.
```

在 `a,v<=1/2`上最坏为 `39/40`，确有 fixed power saving；`h=3`的
`J<a<=1/3,v<=1/2`邻接 cell最坏为 `5/6`。这证明现有 determinant theory真正接触
大路边缘，而不是完全无关。但 Corollary main仍须另与 hybrid comparison逐 cell
对齐，且 theorem本身不把 full Möbius divisor截到 `D<=sqrt(x)`。

首个 fatal coefficient cell已压到 `h=2,j=2`。固定 odd `c>1`，取
`f_1=c,f_2=1`及 `e_1,e_2`在 constant-factor square-root ranges，prime side含

```text
(HB2-B3)
sum_(dr-c e_1e_2=2)
  mu(d)mu(e_1)mu(e_2)log(r)W(d,r,e_1,e_2)
 - the same hybrid-comparison cell.
```

它有 `d,e_1,e_2`三个 primitive rough coordinates、只有 `r`一个 long smooth
coordinate；但可将 `e_1e_2`卷成一个 arbitrary sequence，并将 fixed `c`置于
compact smooth slot，所以 Corollary 1的 literal slot interface并不失败。真正失败
是 grouped scales：`N_1 asymp X,N_2=D`及两个 `L^2` norms使完整 error为
`X^(11/10+o(1))D^(17/20)`，从 bounded `D`起已经超过主尺度。因此

```text
BC_COROLLARY1_TO_HB2_B3
 = STOP_SCOPED_GROUPED_COR1_SCALE_NO_SAVING.
```

更一般地，若最大 smooth `f` exponent为 `b`，在 `D=sqrt(x)`处 Corollary error只有
`b>21/44`才省；quarter `b=1/4`与 bare `b=0`均失败。`h=2`因此只是
minimal-slot obstruction normal form；HB3/HB4可能因 extra factorization更利于
Type-III方法，analytic optimum尚未证明：

```text
HB_H_OPTIMIZATION = OPEN_THREE_ROUGH_CELL_COMPARISON.
```

### 54.15 V5 historical checkpoint：One-Poisson STOP与 superseded native two-stage gate

HB4 `j=2` quarter lift保留四个 `x^(1/4)` factors，表面上可先 Poisson一个 smooth
`f`再调用 Bettin--Chandee Theorem 1的 three-arbitrary reciprocal phase。完整误差
复核否掉了这一捷径。写 `D=x^v`，nonzero Poisson从 `v>1/4`开始；乘回 literal
Poisson prefactor后，source bound两项分别为

```text
E_1=x^(69/80+7v/10+o(1)),
E_2=x^(3/4+7v/8+o(1)).
```

`E_2`单独看似允许 `v<2/7`，但 theorem给两项之和；`E_1`只在
`v<11/56<1/4`节省，与新 nonzero range不相交。故

```text
ONE_POISSON_BC1_QUARTER
 = STOP_SCOPED_FIRST_SUMMAND_NO_NEW_RANGE.
```

不得再选择性删除第一项或发布伪 `2/7` advance。DFI只在 reciprocal kernel已经
形成后给 two-arbitrary bound；Fouvry--Radziwill/Wright仍需 Siegel--Walfisz短因子且
不含 balanced three-rough cell；Assing--Blomer--Li没有 literal HB2 coefficient
interface。withdrawn `2601.00292`因 author-recorded missing `L^2` factor完全排除。

range atlas完成时的 selected attack为（现已由第 54.16--54.17 节的
quadratic STOP、collective-main proof与 Pascadi `3/8`窗口覆盖）

```text
TPC_FM_NATIVE_TWO_STAGE_D2_DISPERSION_GATE
 = SUPERSEDED_BY_SECTIONS_54_16_54_17.
```

它必须从 `(HB2-B3)`或 exact HB3/HB4 factorized lift出发，在把 variables卷成
arbitrary `Xi/Kappa`之前做 Cauchy/dispersion；然后同时证明：

1. zero frequency逐 coefficient等于同一 tensor-local `b_x^(z)` main；
2. low/high conductor split使用 actual `z=log^K x` factors；
3. second transform产生 source-legal separated reciprocal phase；
4. invoked DFI/BC完整 bound的每一项都给 saving；
5. gcd/diagonal/transform tails及 `K(B)` losses全部支付；
6. `d>sqrt(x)`由 explicit outer-Lambda dual/switching identity处理，不能将
   `mu(d)log r`通过改名偷换成 `mu(r)log d`。

这把“证明 universal Type II”的模糊墙压成一个 native three-Möbius two-stage
dispersion theorem。它是有 source接触面的大胆路线，但仍是 `OPEN_NEW_THEOREM`；
strict `1/400`未支付，TPC-207 trigger保持 false。

### 54.16 V6 HB4 collective main与 source-backed `3/8`窗口

第 54.15 节的 generic two-stage gate经实际展开后不再是 current target。HB2 bare
cell若先对 `e_2`作 Cauchy，会引入 `d_1,d_2`与
`q=[d_1,d_2]`；zero mode密度为

```text
E_2/q=E_2(d_1,d_2)/(d_1d_2),
```

并要求 `e_1=e'_1 mod (d_1,d_2)`。它是 signed quadratic Möbius covariance，
不是 linear hybrid main；absolute summation返回原尺度。HB4再作 generic second
Cauchy则产生 rank-two reciprocal numerator，任意化 spectral coefficient会破坏
source tensor。因此

```text
NAIVE_NATIVE_TWO_STAGE = STOP_SCOPED_AT_QUADRATIC_DIAGONAL
HB2_CAUCHY_ZERO_MODE = OPEN_MOBIUS_WEIGHTED_CRT_BDH_COVARIANCE
HB4_GENERIC_SECOND_CAUCHY = OPEN_RANK2_RECIPROCAL_PHASE.
```

真正的推进来自保留 HB4 `h=4,j=2` quarter lift的两条 smooth variables。写

```text
F_1 asymp F_2 asymp F=X^(1/4),
a=e_1e_2 asymp F^2,
u=a f_1 asymp X^(3/4),
D=X^delta.
```

先对 `f_2`模 `d`作 Poisson。`h=0`必须在全部 signed `d/r` dyads重组后只扣一次
comparison main。对 odd `u`，physical `f_2` lattice的密度为 `1/2`，且
`(d,2u)=1`。令

```text
G_q(Y)=sum_(d<=Y,(d,q)=1) mu(d)/d log(Y/d).
```

Vinogradov--Korobov zero-free region加 Perron的 logarithmic kernel，统一于
`u<=Y^(3/4+o(1))`给

```text
(1/2)G_(2u)(Y)
 =u/phi(u)+O_(A,C)(tau(u)^C log^(-A)Y).
```

zero-free输入可取 Kevin Ford 的
[现代显式版本](https://arxiv.org/abs/1910.08205)；Ramaré 2014 的明文 coprime
Möbius bound只有一重 log，不能单独支付这里的 arbitrary `A`。even
`u=2^v u_o`时，gcd=`1,2`两层在 full truncation中精确成为

```text
G_(2u_o)(Y)-G_(2u_o)(Y/2),
```

主常数相消，与 `b_x^(z)(u f_2)=0`吻合。逐 `D` triangle会破坏这项配对。

comparison侧不需要 BV。对长度 `F=X^(1/4)`的 `f_2` fiber取 sieve level
`F^eta,0<eta<1`，用
[Iwaniec Rosser sieve](https://doi.org/10.4064/aa-36-2-171-202)的 fundamental
lemma，并将 `p>z` rough-divisor expansion截在 `log^L X`。lattice remainder在
全部 emitted outer representations上总计
`X^(3/4+eta/4+o(1))`，divisor tail由选择 `L`给任意 log saving；fixed-log
Mellin/partition norms一并支付。故

```text
HB4_QUARTER_COLLECTIVE_H0_TO_HYBRID_MAIN
 = PROVED_SOURCE_BACKED_ALL_D_ATTACHMENT
HB4_PER_D_H0_TO_bz = STOP_SCOPED_NO_NATURAL_D_LABEL.
```

对 `h!=0`再 complete/Poisson `f_1`。`ell=0` Ramanujan轴由

```text
sum_(h<=D/F)|c_d(2h)| << (D/F)d^o
```

给总 `X^(3/4+o(1))`。全非零轴的 termwise Weil总量为

```text
X^(1/2+o(1))D^(3/2),
```

所以严格覆盖 `1/4<delta<1/3`。

第二个真窗口来自 Pascadi 的
[DI/Kuznetsov型 Theorem 10.3](https://doi.org/10.1112/S0010437X2500747X)。
不要把 `e_1`放进 theorem的 `r`槽；最优 literal map先卷
`a=e_1e_2`，再定义 modulus-dependent coefficient

```text
b_(n,d)=mu(d)
 sum_(a,h: n=-4h conjugate(a) mod d) alpha_a Gamma(a,d;h).
```

其平方的 exact collision为 `d|(h_1a_2-h_2a_1)`。nonzero difference用 divisor
count，zero difference用 interval multiplicative energy，得到

```text
||b||_2^2 << F^2D^2 X^o(1),
||b||_2 << FD X^o(1).
```

双 Poisson smooth weight也逐项保留：split `ell/n`的 sign与 dyadic ranges后，
`w(e_1,e_2,h,d)`进入 `b_(n,d)`，`hat W_1(ell F/d)`进入 source的五变量 smooth
test；一般 fixed product cut用 bounded Fourier/Mellin separation，transform `L^1`
只损 `log^O(1)X`且 tails rapid。gcd strata在调用前分别 reduce；目标条件
`(d,2e_1e_2)=1`已经使 active `d`为 odd，故 `K_D`内部没有 off-diagonal two-adic
stratum，更早外层的有限 two-adic separation不属于这个 family。source约定
`r_src asymp R_src`为 `R_src<r_src<=2R_src`，故 `R_src=1`的 singleton是
`r_src=2`；source kernel为 `S(m conjugate(r_src),+n;sc)`。令
`m=ell,n=-4h conjugate(a),s=d,c=1,r_src=2`，再用
`S(ell conjugate(2),-4h conjugate(a);d)=S(ell,-2h conjugate(a);d)`
精确回到目标 kernel。`c=1`由第一 smooth coordinate隔离。因此下述调用是
literal map，不是只代 exponent。

在 source theorem取 `C=R_src=1,S=D,M=D/F,N<=D`；exceptional factor为 `O(1)`。
乘回双 Poisson prefactor `F^2/D^2`后，完整五项依次为

```text
F^(5/2)D, F^2D, F^2D, F^(5/2)D, F^2D.
```

所有项对 fixed `delta<3/8`同时有 power saving；`delta=3/8`没有 saving。故

```text
HB4_QUARTER_RAMANUJAN_AXES = PROVED_X3_OVER_4_POWER_SAVING
HB4_QUARTER_WEIL_OFFDIAGONAL_1/4<delta<1/3 = PROVED_SOURCE_BACKED
HB4_QUARTER_PASCADI_OFFDIAGONAL_1/3<=delta<3/8 = PROVED_SOURCE_BACKED
HB4_QUARTER_OFFDIAGONAL_1/4<delta<3/8 = PROVED_SOURCE_BACKED_POWER_SAVING.
```

这是 arithmetic route advance：现有 published source不只“接触边缘”，而是合法
关闭了一个 growing high-conductor interval。它只针对 factorized HB4 quarter
family，不自动证明全部 `SHB-D2` templates。

### 54.17 V6 historical first missing（由第 54.18--54.19 节覆盖）

提出双 Poisson prefactor后，未覆盖的 raw family记为

```text
K_D=sum_(e_1,e_2 asymp F)mu(e_1)mu(e_2)
    sum_(d asymp D,(d,2e_1e_2)=1)mu(d)
    sum_(0<|h|,|ell|<<D/F)
      Gamma(e_1,e_2,d;h,ell)
      S(ell,-2h conjugate(e_1e_2);d).
```

V6 当时的中央 first missing曾缩到

```text
HB4_QTR_INCIDENT_KUZNETSOV_REFINEMENT_[3/8,1/2]:

|K_D| <<_A F^2D^2/log^A X,
F=X^(1/4), X^(3/8)<=D<=F^2=X^(1/2),
```

只量化 source-emitted `Gamma`与 fixed-log transform parameters。Pascadi现有 bound
距此合同的额外 relative gain为 `D/F^(3/2)`，在最坏 `D=F^2`只为
`F^(1/2)=X^(1/8)`。一个充分接口是针对上述 special incidence coefficient，
把 source complete bound中的两个 `D`-scale terms同时降到 `D/sqrt(F)`；不得把
这一 structured gain改写成 arbitrary coefficient theorem。

`D>sqrt(X)`是独立 range。divisor switching只产生

```text
mu((mn+2)/r)log r, r<sqrt(X),
```

不是 `mu(r)log d`；checked sources没有 literal quotient-Möbius theorem。故 V6
历史 umbrella gate为

```text
TPC_FM_HB4_SIGNED_MODULUS_AND_LARGE_D_DUAL_GATE_V6_HISTORICAL,

HB4_SIGNED_MODULUS_CENTRAL_V6 = SUPERSEDED_BY_54_18
LARGE_D_DUAL_V6 = SUPERSEDED_BY_54_19_EXACT_HB2_SWITCH.
```

第 6 节全部 method cells继续 `STOP_SCOPED`，尤其 TPC193 V1、common-k V1、
tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1。两个 O161 pointwise
parents、pair-native reroute、H1与 global architecture保持 `OPEN`；fixed-atom
credit=`0`、strict `1/400=UNPAID`、`L2=NONE`。formula-level TPC-31 match仍无
packet attachment。上述 quarter-family推进不等于 all-D/all-shape physical cover，
也没有 original/global normalization、tail/A/B、actual packet或 provenance
closure。因此 `TPC_207_TRIGGER=false`，不创建论文、PDF或下一编号。

### 54.18 V7 conductor-projected HB4：每个 fixed `delta<1/2` 已闭合

V6 的 raw coefficient norm不应对全部 nonprincipal characters直接套 multiplicative
large sieve。固定 primitive real `psi (mod 3)`并令 `c_t=conjugate(psi(t))`；诱导到
每个 `q=3p asymp Q`后，长度 `N=FQ`的 character sum仍为 `asymp N`。全 family的
伪 large-sieve左侧为 `asymp F^2Q^2/log Q`，右侧只有 `O(FQ^2)`，相差
`F/log Q -> infinity`。checker用 `F=Q=2000`的 96 个 induced moduli给出超过十倍的
finite growth witness。故

```text
ALL_CHARACTER_CONDUCTOR_COLLAPSE = STOP_SCOPED_FALSE_INDUCED_MOD3.
```

合法 proof按 conductor分开。仍令 `F=X^(1/4),H=D/F`，并在 odd squarefree层写

```text
g=(h,d), d=gq, h=gu, Q=D/g, U=H/g=Q/F.
```

因 `mu(d)!=0`，有 `(g,q)=1`。`ell`的 physical长度始终是 `H`；只有 `u`缩到
`U`。先把完整 gcd stratum的 least residue `n_0 (mod d)`提升到
`n=d+n_0 in [d,2d)`，作 conductor projection后才切 bounded `N asymp D` blocks；
Pascadi smooth test对 `n`取常数，全部 physical `n` weight进入 arbitrary
coefficient。不得对带权 partial residue sum宣称 zero mean。

在 conductor/cofactor dyad `cond(chi)=r_chi asymp R_chi`、
`q=r_chi s_chi`、`s_chi asymp S_chi=Q/R_chi`上，冻结 sign、gcd及全部 dyads后，
同一 source-emitted weight逐 atom写成

```text
Gamma=integral_(t in T) A_t^P(e_1,e_2;g)A_t^U(u;g)
 W_t^ell(ell/H)W_t^q(q/Q)W_t^s(s_chi/S_chi)dmu(t)+O_A(X^(-A)),
integral_(t in T)|dmu(t)|<=log^C X.                    (54.18.0)
```

这是逐 factor product atom，不是仍可耦合各变量的 placeholder。coprimality divisor
expansion后，fixed `(g,s_chi,t)`的 arithmetic polynomial coefficients不依赖
primitive modulus `r_chi`；剩余 smooth scalar
`W_t^q(r_chi s_chi/Q)`由 ordinary partial summation移除，其 total variation已计入
`log^C X`，其余 `r_chi`依赖只在 character evaluation。
conductor projection先在完整 residue group完成，随后 `N`-block restriction只会降低
`L^2`；低导则先重组完整 residue group再用 projector，绝不对 partial/weighted
residues称 zero mean。

对 `cond(chi)>=F`，将 `E_1E_2U`卷成长 `FQ`且 square norm `FQX^o(1)`的
character polynomial。conductor reduction、coprimality divisor expansion与
[Pascadi Lemma 3.4](https://doi.org/10.1112/S0010437X2500747X) 的 primitive
multiplicative large sieve（原始来源可取
[Montgomery--Vaughan](https://doi.org/10.1112/S0025579300004708)）逐 conductor dyad给

```text
sum_g V_g^(hi) << F D^2 X^o(1),
||b^(hi)||_2 << sqrt(F)D X^o(1).                        (54.18.1)
```

把 `(54.18.1)`放入 Pascadi Theorem 10.3的**完整五项**并乘回 double-Poisson
prefactor，五项依次为

```text
F^2D, F^(3/2)D, F^(3/2)D, F^2D, F^(3/2)D;
E_hi(D) << F^2D X^o(1).                                 (54.18.2)
```

低导连同 principal不进入这个 norm。Kloosterman乘法性给

```text
S(ell,gv;gq)=c_g(ell)S(ell conjugate(g),v;q).
```

按当前 conjugation convention展开 Kloosterman sum并交换有限求和，elementary
identity为

```text
tau_q(eta,a)=sum_(v mod q)^*eta(v)e(av/q),
T_q(chi;ell)=tau_q(conjugate(chi),1)tau_q(conjugate(chi),ell)
```

（已显示的 unit scaling只改参数；相反 convention同时共轭两个 factors，最终只改
unit phase）。若 `chi mod q`由
primitive `psi mod r_chi`诱导且 `q=r_chi s_chi`，elementary CRT再给 exact
absolute identity

```text
|T_q(chi;ell)|=r_chi|c_(s_chi)(ell)|1_((ell,r_chi)=1)
               <=r_chi(s_chi,ell),
1/phi(q) * r_chi=(r_chi/phi(r_chi))/phi(s_chi).          (54.18.3)
```

exact equality是上述 finite CRT/Gauss推导；
[Pascadi Lemmas 3.7--3.8](https://doi.org/10.1112/S0010437X2500747X)只支付后续
generalized-Gauss与 Weil--Ramanujan bounds，不冒充 projector statement。这正把
primitive conductor权与 cofactor lift分开。固定 `g`与
`r_chi asymp R_chi<F`，
把两条 `e_i`卷成长 `F^2`的 `P_psi`，把 `u`与带
`c_g(ell)c_(s_chi)(ell)`的 `ell`卷成长 `UH=H^2/g`的第二条 polynomial。两次 primitive
large sieve、Cauchy与

```text
sum_(s_chi asymp Q/R_chi) 1/phi(s_chi)
sum_(|ell|<<H)|c_g(ell)c_(s_chi)(ell)|^2 << H^2g X^o(1)
```

给 fixed `(g,R_chi)` bound

```text
F^2H^(3/2)sqrt(R_chi^2+H^2/g)X^o(1)
 << F^3H^(3/2)X^o(1).                                  (54.18.4)
```

conductor dyads只损 logarithms，粗和 `g<=H`并乘回 `F^2/D^2=H^(-2)`后

```text
E_low(D) << F^3sqrt(H)X^o(1)
          <=F^(7/2)X^o(1)=X^(7/8+o(1)).                (54.18.5)
```

目标条件令 `d`及 `g,q,r_chi,s_chi`在 `K_D`上均为 odd；更早外层若有有限 two-adic
types，已经在进入本 off-diagonal family前分离。source-emitted `Gamma`按
`(54.18.0)`作同一个 multivariable Mellin/Fourier separation，总
`L^1=log^O(1)X`；fixed power margin吸收全部 losses。
因此

```text
HB4_LOW_CONDUCTOR_KLOOSTERMAN_PROJECTOR
 = PROVED_GAUSS_CRT_PLUS_PRIMITIVE_LARGE_SIEVE

HB4_HIGH_CONDUCTOR_INCIDENCE_3/8<=delta<1/2
 = PROVED_PRIMITIVE_LARGE_SIEVE_PLUS_COMPLETE_PASCADI

HB4_QUARTER_OFFDIAGONAL_1/4<delta<1/2
 = PROVED_SOURCE_BACKED_POWER_SAVING

HB4_EXACT_HALF_ENDPOINT = OPEN_LOG_POWER_ENDPOINT.      (54.18.6)
```

在 exact `D=F^2=X^(1/2)`，`(54.18.2)`只有 `X^(1+o(1))`，没有任意
`log^-A X`。所以 `(54.18.6)`逐 fixed `delta<1/2`成立，不能把极限升级为 closed
endpoint。它也只闭合 factorized HB4 quarter family，不自动覆盖全部 `SHB-D2`
shapes。

### 54.19 V7 exact large-`D` recompilation、next gate与 release裁决

旧 quotient-Möbius形态不是不可绕过。对 dyadic top `Z`取
`Y=floor(sqrt(Z))`，并对 `N<=Z`定义

```text
A1(N)=sum_(ef=N,e<=Y)mu(e)log f,
A2(N)=sum_(e1,e2<=Y,e1e2f1f2=N)mu(e1)mu(e2)log f1.
```

[Ford--Maynard Lemma 5.2](https://arxiv.org/abs/2407.14368) proof中的
`r=1` logarithmic-derivative precursor给 exact HB order-two identity

```text
Lambda(N)=2A1(N)-A2(N),
sum_(d|N,d>Y)mu(d)log(N/d)=A1(N)-A2(N).                 (54.19.1)
```

不得把 Lemma statement中 isolated `r=1`单项误称 prime indicator；`(54.19.1)`来自
其 proof内标准 `-zeta'/zeta` identity。closed `d=Y`只进入 `A1`，large side严格
`d>Y`，无 half weight；prime powers也逐点精确。checker在 510 个 `(Z,N)` cases上
逐 formal `log p` coefficient验证两个等式，并以 `Z=N=36`检测把 square-root endpoint
误放 large side的 mutation。

代回 outer HB4 `h=4,j=2,r=1` quarter，outer coefficient为

```text
-6mu(a1)mu(a2)[log b1/log t], t=a1a2b1b2.
```

`A2` correction的 literal determinant与 coefficient为

```text
e1e2f1f2-a1a2b1b2=2,

+6mu(a1)mu(a2)mu(e1)mu(e2)
  [log b1/log t]log f1.                                 (54.19.2)
```

首个 symmetric hard cell的八个 variables均为 `F=X^(1/4)`：四个 Möbius slots
`a1,a2,e1,e2`与四个 smooth/log slots `b1,b2,f1,f2`。令
`A=a1a2,E=e1e2,B=b1b2,R=f1f2`，则 `ER-AB=2`且 grouped scales均为
`sqrt(X)`。严禁把 `mu(e1)mu(e2)`压成 `mu(E)`：`e1=e2=p`时两者分别为 `+1`
与 `0`；literal row是 truncated convolution `mu_F*mu_F`。

完整 ordered factorization有

```text
sum_(f1f2=R)log f1=(1/2)tau(R)log R,
```

但单个 unequal smooth/dyadic shell不能直接使用；必须与 exact swapped shell配对并
同步交换 weights。单个 shell只能使用 literal truncated ordered convolution

```text
c_Eis^(I,J)(R)=sum_(f1f2=R)W_I(f1)W_J(f2)log f1.
```

paired off-diagonal shells给
`c_Eis^(I,J)+c_Eis^(J,I)=log(R)c_div^(I,J)`；diagonal shell有相应 `1/2`，
两者都不能升级成 full `tau(R)`。fixed-log separation后的 `A2` correction
contribution normal form为

```text
(6/log X)sum_(ER-AB=2)
 c_mu(E)c_mu(A)c_Eis^in(R)c_Eis^out(B)rho_X(AB)W,

c_mu=truncated weighted mu_F*mu_F,
c_Eis=truncated ordered (log W_I)*W_J.                  (54.19.3)
```

`6/log X`由 `rho_X(AB)=log X/log(AB)`与 `(54.19.2)`的 literal `+6`强制，
不得吸收到未声明 normalization。

完整 switched error是 coefficientwise `A1-A2`，不是单独中心化的 `A2`项；必须在
triangle inequality之前联合。预先分配的 comparison contribution，其 all-`D`总和
就是 collective hybrid main，只从这个组合误差中减一次。

现有 Bettin--Chandee不能把两条 divisor convolutions同时当作 `C^infinity` slots；
展开 literal variables后 balanced-quarter完整 error无 saving。Pascadi的
`b_(n,r,s)`虽可依赖三个 displayed indices，但第 54.17--54.18 节的 literal source
map只压一条 row，尚无 simultaneous second-row incidence/range/`L^2` map。因此

```text
LARGE_D_HB2_SWITCH = PROVED_EXACT_COEFFICIENTWISE
LARGE_D_QUOTIENT_MOBIUS_GATE = SUPERSEDED
LARGE_D_TO_CURRENT_BETTIN_CHANDEE
 = STOP_SCOPED_NONSMOOTH_COLUMNS_OR_EXPANDED_SCALE_NO_SAVING
LARGE_D_TO_CURRENT_PASCADI
 = NOT_ATTACHED_SECOND_ROW_INCIDENCE_MAP
HB4xHB2_SIGNED_DIVISOR_VORONOI_DETERMINANT
 = OPEN_NEW_THEOREM.                                   (54.19.4)
```

当前下一项不编号大动作为

```text
TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE.
```

它只造两段主路：给 `(54.18.2)` exact half一个真实 log-power gain；以及对
`(54.19.3)`在 triangle前联合处理 `A1-A2`，用 paired divisor-Voronoi/Estermann加
outer double-Poisson/Kuznetsov证明同一 collective error。必须覆盖所有未支付 scale
vectors、exactly-once shell pairing、moving/fixed cutoff corridor、gcd/two-adic、
Mellin/tail与同一 hybrid main，不能只证 symmetric示例。

第 6 节全部 method cells继续 `STOP_SCOPED`，尤其 TPC193 V1、common-k V1、
tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1。两个 O161 pointwise
parents、pair-native reroute、H1与 global architecture保持 `OPEN`；fixed-atom
credit=`0`、strict `1/400=UNPAID`、`L2=NONE`。quarter family仍没有 all-shape
cover、original/global normalization、tail/A/B、actual packet attachment或完整
provenance。因此 `TPC_207_TRIGGER=false`，不创建论文、PDF或下一编号。

V7 正式冻结前的只读验证为：

```text
POST_WRITE_STARTUP_REGRESSION = 22/22 PASS
POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_BIG_ROAD_CHECKS = 3/3 PASS
  LAB = 16 exact cases
  INDEPENDENT = 170 local cases + N=50 variance fixture
  FM_COMPILER = PASS; HB2 switch 510; Pascadi source map 675;
                induced-character 96; Gauss projector 28
FM_MUTATIONS = endpoint + prime-power + four-Mobius + 6/logX +
               Pascadi-r_src=2 + all-character collapse DETECTED
GIT_DIFF_CHECK = PASS
MARKDOWN_FENCES = HANDOFF 1824; COMPASS 68; README 126; COMPILER 336;
                  ALL BALANCED
PROTECTED_UNTRACKED = 130 FILES
PROTECTED_MANIFEST
  = 9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
FROZEN_AGENT_R3 = SUPERSEDED_BY_R4_AFTER_COMMONMARK_FENCE_COUNT_FIX
FROZEN_AGENT_R4 = SUPERSEDED_BY_R5_AFTER_RELEASE_LABEL_FIX
FROZEN_AGENT_R5 = PENDING_BEFORE_STAGE
```

final fetch显示 `origin/main=ba4d11aab349d3301a713e4a6e4f16c0cd84d45a`，领先本地
两个 commits `863aeaa`、`ba4d11a`；delta只改 `RH_HANDOFF.md`并新增 RH-363/364
release files，与本轮五个 TPC allowlist paths无 overlap。RH已由用户宣布 out of
scope，本轮不运行其 builders/tests；必须在 allowlist commit后安全 rebase，并重跑
上述全部 checks。三份 R2 read-only audits发现的 source-kernel、Gauss conjugation、
product-atom separation、`A1-A2` main ownership、`6/log X`、truncated shell与
BC/Pascadi status问题均已由主控修正；正式 stage前仍以本段写入后的 frozen hash
执行 R5，任一 non-PASS即 fail closed。

## 55. 2026-08-06 V8：fixed-unit Kloosterman引擎、character obstruction与两车道定向

### 55.1 基线、分工与 claim level

本轮启动 `HEAD=origin/main`：

```text
a7306753f0af4bf02448f2833fa4015aad6d623f
```

启动 `TPC_HANDOFF.md` SHA-256为
`dbef7fb0781d844aa172bbae0e02d698aeae605685c1c8ecafb30c4598ae0316`；
tracked/cached diff为空，130 个 protected untracked files原样保留。启动 pull返回
already up to date，第 1 节 22 项只读 regression为 `22/22 PASS`。主控按
`AGENTS.md`调度三个 `READ_ONLY_FROZEN` agent：exact-half source architect、
large-`D` theorem architect与 devil's-advocate/release QA；所有正式写入只由主控完成。

本节只登记 source-backed local engine、exact finite obstruction与新的 theorem
contracts。它没有证明 arithmetic endpoint，不提供 fixed-atom、strict `1/400`、
`L2`或 TPC-207 credit。

### 55.2 Blomer--Pascadi fixed-unit theorem的 literal map与完整 deficit

[Blomer--Pascadi Theorem 1.1](https://arxiv.org/abs/2607.24311)在 fixed arbitrary
modulus `c`、fixed unit与两条临界长度 `sqrt(c)` sequences上给

```text
||alpha||_2||beta||_2 c^(31/32+o(1)).                  (55.2.1)
```

在 exact half令 `D=F^2`，并按第 54.18 节取

```text
g=(h,d), d=gq, h=gu, q asymp F^2/g, u<<F/g.
```

odd squarefree `d`给 `(g,q)=1`，Kloosterman乘法性把 fixed
`(e_1,e_2,d,g)` cell化为 modulus `q`、unit
`-2 conjugate(g e_1e_2)`、长度 `F`与 `F/g`的 `(55.2.1)`输入。squarefree版本逐
`g`的 local bound为

```text
F^(47/16)g^(-15/16),
```

求和 `g|d`后仍为 `F^(47/16+o(1))` per fixed `(e_1,e_2,d)`。这确认

```text
q^(-1/32)=F^(-1/16)=X^(-1/64)                         (55.2.2)
```

是真实 supporting engine。

但是冻结并绝对求和 `F^2`个 `e`-pairs与 `F^2`个 moduli给

```text
F^4 F^(47/16)=F^(111/16),
raw endpoint target=F^6,
deficit=F^(15/16).                                     (55.2.3)
```

乘回 physical prefactor `F^(-2)`仍为 `F^(5-1/16)`，高于 `F^4=X`。因此

```text
BP2607_FIXED_UNIT_EXACT_HALF_LOCAL_ENGINE
 = SOURCE_ATTACHED_LOCAL_F^(-1/16)_SAVING,
BP2607_AFTER_FREEZE_AND_OUTER_TRIANGLE
 = STOP_SCOPED_F^(15/16)_DEFICIT.                       (55.2.4)
```

[Pascadi 2511.08445](https://arxiv.org/abs/2511.08445)的 fixed-unit input与短
modulus average不补这个外层：后者在 modulus外先取绝对值，丢掉 `mu(d)`；按 actual
`C=F^2,M=N=F`代入也没有额外 power saving。

### 55.3 arbitrary moving-unit lift的 exact rank-one反例

冻结 convention：

```text
e_p(t)=exp(2 pi i t/p),
S(m,n;p)=sum_(x mod p)^*e_p(mx+n x^(-1)),
tau(psi)=sum_(y mod p)^*psi(y)e_p(y).
```

对 prime `p`与 nonprincipal `chi`，两次 finite Gauss substitution给 exact identity

```text
sum_(A mod p)^*chi(A)S(ell,-2h A^(-1);p)
 =tau(conjugate(chi))^2 chi(-2h ell).                   (55.3.1)
```

取 `P(A)=chi(A)`及长度 `sqrt(p)`的 character-matched `h,ell` vectors，左侧为
`p^2`；无额外代价的 `L_A^2`-valued BP lift却只给

```text
p^(1/2)p^(1/4)p^(1/4)p^(31/32)=p^(63/32),
2-63/32=1/32.                                          (55.3.2)
```

故

```text
BP2607_ARBITRARY_UNIT_VECTOR_LIFT
 = STOP_SCOPED_FALSE_CHARACTER_EIGENMODE.               (55.3.3)
```

checker取 `p=13`、primitive root `2`与 `chi(2)=i`，在 exact
`Z[i][Z/13Z]` group ring验证 16 个 `(h,ell)` cases；并以 `h=3,ell=5`冻结绝对
coefficient tuple，防止同时改变 `-2`或 conjugation convention后协变地误 PASS。
character-matched `H={1,2,3},L={4,5,6}` fixture的 exact magnitude ledger为 `117`。

这不是 actual Möbius atom的反例。其 product-unit Fourier coefficient精确为

```text
P_hat_p(chi)=E_1(chi)E_2(chi),
E_i(chi)=sum_(e_i asymp F)mu(e_i)W_i(e_i)chi(e_i).      (55.3.4)
```

所以 `(55.3.3)`的作用是禁止 arbitrary-coefficient theorem，并迫使 proof使用
`(55.3.4)`与 `mu(d)`的 special signed structure。只证单个
`P_hat_p(chi)` nonconcentration仍不够；complete character fourth moment/
ratio-incidence具有 broad-spectrum diagonal floor，必须在其形成前利用 Gauss
root-number phase与 modulus sign。

[Pascadi 2404.04239 Theorem 3](https://arxiv.org/abs/2404.04239)也不直接附着：其
coefficient在平方前就是 fixed multipliers的 integer equality，而 actual coefficient是
moving `e_1e_2` products加 modular inverse的 residue fiber；取 product作为 multiplier
又违反 `q>>L^2` range。更决定性地，该 theorem改善 exceptional-spectrum factor，
exact-half饱和的是 regular第一、第四 majorants，不能把它们当成两个 signed physical
terms相消。

### 55.4 selected primary：Gauss-twisted signed correlation

对每个第 54.18 节 source-emitted product atom定义

```text
C_(g,q)(chi)=E_1(conjugate chi)E_2(conjugate chi)H_g(chi),

L_(g,q)(chi)=tau_q(conjugate chi,1)
 sum_ell W^ell(ell/F)c_g(ell)tau_q(conjugate chi,ell).
```

当前最窄、非循环的新 theorem contract是在 `D=F^2`、Pascadi triangle/Cauchy之前，
对某个 fixed `eta>0`证明

```text
|sum_(g<=F)sum_(q asymp F^2/g) mu(gq)/phi(q)
 sum_(chi mod q,cond(chi)>=F)C_(g,q)(chi)L_(g,q)(chi)|
 <<F^2D^2D^(-eta)X^o(1).                              (55.4.1)
```

量词只覆盖 actual source product atoms、actual masks、odd-squarefree gcd/conductor/
cofactor dyads与完整 transform parameters；不得升级为 arbitrary `P(A)`。projector必须
先作用于 complete residue group，low conductors继续使用已证 Gauss--CRT分支。
`mu(gq)`、Gauss-square phase、moving unit与 fixed physical `h0=2`必须保持到 saving
真实产生之后。

任意 fixed `eta>0`均足够吸收 polylog/Mellin/BV losses；若 `(55.2.2)`的
`eta=1/32`在这个 restricted signed family中存活，则 physical scale为
`X D^(-1/32)=X^(63/64+o(1))`。这是 target ledger，不是 theorem claim。状态为

```text
HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION
 = SELECTED_PRIMARY_OPEN_NEW_THEOREM.                   (55.4.2)
```

第一 proof-or-refutation stage只取 prime modulus、`g=1`与单个 source product atom，
但必须审核 broad character spectrum而非只排除一个 spike。prime stage若只能回到
absolute complete-character large sieve，则发布精确 STOP；若 Gauss/root-number与
literal Möbius ratio-incidence出现 signed saving，再扩展到 squarefree
conductor/cofactor strata。

该 prime stage已进一步编译。写

```text
H(chi)=sum_(|h|<<F)U(h)chi(h),
L(chi)=sum_(|ell|<<F)V(ell)chi(ell).
```

complete projector在 Cauchy前给 exact formula

```text
G_p=mu(p)/(p-1)sum_(chi mod p)tau(chi)^2 conjugate(chi)(-2)
 E_1(chi)E_2(chi)H(conjugate chi)L(conjugate chi).       (55.4.3)
```

principal项为 `O(F^2)`。对 `chi!=1`令
`m_p(chi)=p^(-1)tau(chi)^2 conjugate(chi)(-2)`，则 `|m_p(chi)|=1`。
再定义 literal ratio vectors

```text
C_1(r)=sum_(e conjugate(h)=r)mu(e)W_1(e)U(h),
C_2(r)=sum_(e conjugate(ell)=r)mu(e)W_2(e)V(ell),
```

便有 `C_hat_1=E_1H_bar,C_hat_2=E_2L_bar`。critical ratio-incidence给
`||C_hat_i||_2<<F^(2+o(1))`，plain Cauchy精确回到每 prime `F^(4+o(1))`
endpoint；Gauss multiplier在 arbitrary ratio space上是 unitary，故 generic angle
theorem同样为假。

但 single-character coherent mode不能饱和 actual source。source-smooth长度
`F=sqrt(p)`的 `H,L`由 [Heath--Brown所述 Burgess bound](https://arxiv.org/abs/1203.5219)
的 `r=2` case给 `F^(7/8+o(1))`；即使 `|E_1E_2|<=F^2`，单个 character也只有
`F^(15/4+o(1))=o(F^4)`。所以真正 first wall是 broad-spectrum Gauss-phase
alignment，不是一个 character spike。unsigned fourth moments已有 `F^4` diagonal
floor，不能靠更小 unsigned norm关闭。

最窄 first subgate因此为

```text
HB4_EXACT_HALF_PRIME_MOBIUS_RATIO_GAUSS_ANGLE:

|sum_(chi!=1)m_p(chi)C_hat_1(chi)C_hat_2(chi)|
 <<F^(-eta)||C_hat_1||_2||C_hat_2||_2.                 (55.4.4)
```

它只量化 actual source-emitted ratio vectors。若成立，per prime为
`F^(4-eta)`，求和 `F^2` prime moduli并乘回 `F^(-2)`后为
`X^(1-eta/4+o(1))`。prime cell上 `mu(p)=-1`恒定，不能把 saving归给 modulus sign。
现有 source无此 theorem，也未发现 actual Möbius class反例；状态为

```text
HB4_EXACT_HALF_PRIME_MOBIUS_RATIO_GAUSS_ANGLE
 = FIRST_SUBGATE_OPEN_NEW_THEOREM_PLAUSIBLE.            (55.4.5)
```

具体 construction顺序也已收缩：以 reduced ratio写 `e=ak,h=bk`；long common-`k`
fibers先在移除 `(k,a)=1`后提取 smooth Möbius cancellation，primitive/short fibers则
必须把两条 literal quotient-incidence vectors一起保留到 Blomer--Pascadi式
quadratic-character fourth-moment步骤，最后证明 Gauss multiplier下的 restricted
principal angle saving。[Korolev--Shparlinski](https://arxiv.org/abs/1804.01337)在
`N>=p^(1/2+epsilon)`给 Möbius--trace cancellation，但不含 exact `sqrt(p)`或当前
four-factor Gauss correlation，只能作机制证据，不能附着。

### 55.5 independent reserve：structured two-row paired-Voronoi

第 54.19 节 `A_1-A_2` exact HB2 switch具有不同 source lock。circle/delta展开后对
两个 ordered divisor-log columns同步 Voronoi，coprime dual branch出现

```text
S(-2,conjugate(A)b* - conjugate(E)r*;q).                (55.5.1)
```

独立 source audit进一步导出完整 first-transform skeleton，并修正一个必须冻结的
非对称性。对 exactly-swapped shell `sigma`，outer `-6`乘 exact `A_1-A_2`
switch后，联合对象为

```text
H_sigma=(6/log X)sum_(ER-AB=2)
 C_A^(2)(A)D_B^(2)(B)rho_X(AB)Omega_sigma
 [C_E^(2)(E)D_R^(2)(R)-C_E^(1)(E)D_R^(1)(R)],          (55.5.1a)

C_A^(2),C_E^(2)=literal weighted mu_F*mu_F,
D_B^(2),D_R^(2)=ordered truncated divisor-log,
C_E^(1)(E)=mu(E)W_E(E),
D_R^(1)(R)=W_R(R)log R.
```

所以 `A_2`是 double Estermann/Voronoi，`A_1`只能对 `B`作一次 Voronoi并保留
smooth-log `R`列。把 `A_1`的 `log R`冒充第二条 divisor/Eisenstein column会改变
literal coefficient，新增 firewall：

```text
A1_INNER_LOG_TO_SECOND_EISENSTEIN_COLUMN = STOP_SCOPED_WRONG_COEFFICIENT.
```

ordered column使用 generalized
[Estermann functional equation](https://arxiv.org/abs/2110.08974)；exactly-swapped
shell对应对 `tau_(u,v)`施加 `-(partial_u+partial_v)`，diagonal shell保留 `1/2`。
derivative必须同时作用 poles、`q` powers、Gamma/Bessel kernels与 dual coefficients，
不能只给 dual coefficient补 `log m`。

determinant还给 exact gcd reduction：

```text
(A,E)|2,
A=gA_0,E=gE_0,(A_0,E_0)=1,g in {1,2},
E_0R-A_0B=h_g, h_g=2/g.                                (55.5.1b)
```

因此只有 ordinary shift-`2` branch与唯一 two-adic reduced shift-`1` branch。
按 [Duke--Friedlander--Iwaniec reduced inverse](https://www.math.ucla.edu/~wdduke/preprints/quadraticdiv.pdf)
先约分再提升，`A_2` first transform逐字包含 polar×polar、两个 one-polar families与
四个 dual×dual Bessel-sign families；后者 Kloosterman核为

```text
S(h_g,eta_R E_q^sharp r* - eta_B A_q^sharp b*;q).       (55.5.1c)
```

`A_1`则只有 Ramanujan/progression zero column与完整 one-Voronoi branch

```text
sum_R c_q(E_0R-h_g)J^0(R)
+sum_(eta_B,b*,R)S(E_0R-h_g,eta_B A_q^sharp b*;q)J^eta. (55.5.1d)
```

令 `Z_2`为 `A_2` polar×polar，`Z_1`为 `A_1` zero column；唯一合法 main bracket是

```text
Z_joint=sum_(sigma,D)(Z_(2,sigma)-Z_(1,sigma))-M_cmp^(all-D). (55.5.1e)
```

两项均不能单独认领 hybrid main。balanced `q asymp D_0=F^2`时 dual lengths为
`F^2`；DFI fixed-row error为 `F^(3+o(1))`，两条 literal Möbius rows的 absolute
`L^1` product为 `F^(4+o(1))`。所以 row-by-row DFI只有 `F^7`，而 physical target为
`F^4 log^(-A)X`。first new family estimate必须联合回收 `F^3`：

```text
sum_(sigma,D)[O_(2,sigma)-O_(1,sigma)]<<_A F^4/log^A X. (55.5.1f)

HB4xHB2_PAIRED_VORONOI_FIRST_TRANSFORM = DERIVED_SOURCE_BACKED
HB4xHB2_COLLECTIVE_POLAR_MAIN_ATTACHMENT = OPEN_NEW_ATTACHMENT
DIRECT_DFI_ROW_BY_ROW = STOP_SCOPED_F7_VERSUS_F4
HB4xHB2_STRUCTURED_TWO_ROW_KLOOSTERMAN_FAMILY = OPEN_NEW_THEOREM.
```

若先把两条 row压成 arbitrary residue sequences `Gamma_q(u),Delta_q(v)`，核退化为

```text
K_q(u,v)=S(-2,u-v;q).
```

其 additive Fourier eigenvalues精确为

```text
lambda_k=q e_q(-2k^(-1))  (k unit),
lambda_k=0                 (otherwise),                (55.5.2)
```

故 operator norm为 `q`，没有 generic `L^2` saving。checker在 `q=5,7,11,13`的
36 个 frequencies exact验证并检测 `u+v` mutation。因此

```text
BP2607_AFTER_NAIVE_RESIDUE_COMPRESSION
 = STOP_SCOPED_ADDITIVE_DIFFERENCE_KERNEL_NORM_Q.       (55.5.3)
```

surviving reserve必须在 compression前同时保留四个 literal Möbius slots、两条
reciprocal-incidence rows、两个 ordered divisor-log Voronoi columns、exactly-swapped
shell pairing、shift `2`与 outer `-6`强制的 physical `A_2-A_1` combination（source
switch本身仍为 `A_1-A_2`）。对 paired shell tuple
`sigma`令

```text
E_sigma=(A_(2,sigma)-A_(1,sigma))-M_(cmp,sigma),
sum_sigma E_sigma <<X^(1-eta)(log X)^C,                 (55.5.4)
```

其中 collective main只减一次；uniform ledger必须含 moving/fixed square-root
corridor、gcd/two-adic branches、Estermann poles/zero modes、Bessel tails、Mellin
loss与原始 `6/log X` normalization。当前状态：

```text
HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI
 = OPEN_NEW_THEOREM_PLAUSIBLE_INDEPENDENT_PARENT.       (55.5.5)
```

`(55.4.2)`与 `(55.5.5)`不得拼接；调度上先攻前者，后者保持独立 reserve。

### 55.6 route/release裁决

canonical umbrella名保持

```text
TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE;
```

只新增 primary/reserve priority，不破坏第 54.19 节 source lock。V8 checker显式断言：

```text
primary_route=HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION
first_subgate=HB4_EXACT_HALF_PRIME_MOBIUS_RATIO_GAUSS_ANGLE
independent_reserve=HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI
independent_first_transform=DERIVED_SOURCE_BACKED
independent_polar_main_attachment=OPEN_NEW_ATTACHMENT
direct_dfi_row_by_row=STOP_SCOPED_F7_VERSUS_F4
source_lock_merge=false
fixed_physical_h0=2
fixed_atom_credit=0
strict_1_over_400=UNPAID
L2=NONE
TPC_207_TRIGGER=false.
```

本轮正式裁决为

```text
TPC_BIG_ROAD_V8_20260806_FIXED_UNIT_CRITICAL_KLOOSTERMAN_ENGINE_REAL_
GENERIC_MOVING_UNIT_LIFT_FALSE_CHARACTER_EIGENMODE_ACTUAL_MOBIUS_GAUSS_
SIGNED_CORRELATION_SELECTED_PRIMARY_TWO_ROW_PAIRED_VORONOI_FIRST_TRANSFORM_
DERIVED_POLAR_MAIN_AND_F3_FAMILY_SAVING_OPEN_NAIVE_RESIDUE_COMPRESSION_
NORM_Q_STOP_NO_ARITHMETIC_TRIGGER_CHANNEL_REDESIGN
```

第 6 节所有 method cells继续 `STOP_SCOPED`，尤其 TPC193 V1、common-k V1、
tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1。两个 O161 pointwise
parents、pair-native reroute、H1、global architecture与 dynamics portfolio保持
`OPEN`。本地 exact checker PASS不产生 theorem credit；all-`D` uniformity、
exactly-once physical cover、original/global normalization、tail/A/B、actual packet
attachment与 provenance仍全部未过。因此不创建 TPC-207、论文、paper directory或
PDF。

### 55.7 post-write fail-closed verification

本节冻结前的只读验证为：

```text
POST_WRITE_STARTUP_REGRESSION = 22/22 PASS
POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_BIG_ROAD_CHECKS = 3/3 PASS
  LAB = 16 exact cases
  INDEPENDENT = 170 local cases + N=50 variance fixture
  FM = PASS; quartic moving-unit 16; character-matched magnitude 117;
       additive-difference spectrum 36
FM_ROUTE_FREEZE
  umbrella = TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE
  primary = HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION
  first_subgate = HB4_EXACT_HALF_PRIME_MOBIUS_RATIO_GAUSS_ANGLE
  reserve = HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI
  source_lock_merge = false
  physical_order = A2_MINUS_A1
GIT_DIFF_CHECK = PASS
MARKDOWN_FENCES = ALL BALANCED
EXPECTED_TRACKED_DIFF = 5/5 EXACT
CACHED_DIFF = EMPTY
PROTECTED_UNTRACKED = 130 FILES
PROTECTED_MANIFEST
  = 9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
PAPER_PDF_NUMBERED_RELEASE_CREATED = NO
```

## 56. 2026-08-06 V9：Gauss dual product、exact resonance firewalls与 signed Type-IV主路

### 56.1 基线、分工与 claim level

本轮启动 `HEAD=origin/main`：

```text
cfe26af99bed702aad5d346100a39134c3ac8520
```

启动 `TPC_HANDOFF.md` SHA-256为
`8cf2a59c05f77e270a217a6849bcaba877287cfaf68f116c9e780d24eeb381d8`；
tracked/cached diff为空。130 个 protected untracked files按 canonical PowerShell
manifest为
`9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1`，均原样
保留。启动 pull返回 already up to date，第 1 节 22 项只读 regression为
`22/22 PASS`；TPC-27--32与 TPC-122 writers未执行。

主控按 `AGENTS.md`与 ARS source/proof审计流程调度三个 `READ_ONLY_FROZEN`
agents：source-lock/common-`k` audit、physical-kernel/architecture audit与
devil's-advocate exact-duality audit。三者均回报同一 baseline、
`files_changed=[]`、`TPC207_TRIGGER=false`；正式写入只由主控完成。

本节的最高 claim为 `POSITIVE_DERIVED_SUBLEMMA`：它证明 exact finite normal
form并封闭两个 broad shortcuts，但没有证明 power saving。fixed-atom credit=`0`、
strict `1/400=UNPAID`、`L2=NONE`。

### 56.2 frozen source-weight theorem contract

第 55 节的 `actual source atom`若不说明函数类，无法独立证伪。V9冻结一个更宽的
testable superclass：`p asymp F^2`；`a_i(e)=mu(e)W_i(e)`支撑于 fixed dyadic
`F`-shell；`U,V`支撑于有限个 signed nonzero `F`-shell；physical `h0=2`、
所有 sign/mask、gcd/conductor/cofactor dyads与 common transform parameters固定；
每个 fixed derivative order满足 inert/log-Mellin seminorm `log^O(1)X`，总 product-
atom decomposition `L1<=log^O(1)X`。第二个 dual factor不取 conjugate，constants须
uniform于全部显示参数。

block/cumulative、logarithmic/natural、arbitrary residue vectors均不在该 class。
但当前 tracked source未生成逐 atom registry，所以 fail-closed状态为

```text
HB4_EXACT_HALF_SOURCE_WEIGHT_ENVELOPE
 = FROZEN_TESTABLE_SUPERCLASS_CONTRACT
HB4_EXACT_HALF_ACTUAL_ATOM_MEMBERSHIP
 = OPEN_ATTACHMENT.                                    (56.2.1)
```

这解决 theorem statement可测试性，不产生 arithmetic credit；任何实际 atom若不在
envelope内，必须扩展 contract并重审，不能默认为已覆盖。

### 56.3 exact Gauss-square to fixed-product duality

在 prime `p`上令

```text
a_i(e)=mu(e)W_i(e),
A_i=sum_e a_i(e), H_0=sum_h U(h), L_0=sum_ell V(ell),
U_p^sharp(z)=sum_(h!=0)U(h)e_p(zh),
V_p^sharp(w)=sum_(ell!=0)V(ell)e_p(w ell),
M_p=A_1A_2H_0L_0.
```

所有 multiplicative characters包括 `chi_0`均满足

```text
sum_(z!=0)chi(z)U_p^sharp(z)=tau(chi)H(conjugate chi). (56.3.1)
```

其中 positive phase、`z!=0`与 `tau(chi_0)=-1`全部强制。定义

```text
Q_p(-2)=sum_(e_1e_2zw=-2 mod p)
 a_1(e_1)a_2(e_2)U_p^sharp(z)V_p^sharp(w).              (56.3.2)
```

complete character orthogonality给 exact nonprincipal identity

```text
sum_(chi!=chi_0)p^(-1)tau(chi)^2 conjugate(chi)(-2)
 E_1(chi)E_2(chi)H(conjugate chi)L(conjugate chi)
 = (p-1)/p [Q_p(-2)-M_p/(p-1)].                        (56.3.3)
```

并且

```text
Q_p(-2)=sum_(e_1,e_2,h,ell)
 a_1(e_1)a_2(e_2)U(h)V(ell)
 S(1,-2h ell conjugate(e_1e_2);p),
G_p=mu(p)Q_p(-2).                                      (56.3.4)
```

principal项与 `(56.3.3)` subtraction只是在 full cell中 exact重组，不能记为 saving。
以 normalized dual weights `U_tilde=p^(-1/2)U^sharp`定义

```text
D_p(-2)=sum_(e_1,e_2,z,w)a_1a_2 U_tilde(z)V_tilde(w)
 [1_(e_1e_2zw=-2)-1/(p-1)],                            (56.3.5)
```

则 character gate精确为 `(p-1)D_p(-2)`。因此第 55 节
`HB4_EXACT_HALF_PRIME_MOBIUS_RATIO_GAUSS_ANGLE`与 `(56.3.5)`只是同一 gate的两种
坐标，saving不得相乘。checker在 `Z[zeta_p]`中以两个独立 integer-weight fixtures
验证 `(56.3.4)`，并检测 principal sign、`-2 -> +2`与 nonzero-frequency mutations。

状态为

```text
HB4_EXACT_HALF_PRIME_GAUSS_DUAL_PRODUCT_IDENTITY
 = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PRIME_CENTERED_DUAL_PRODUCT
 = PROVED_EXACT_EQUIVALENCE.                           (56.3.6)
```

最窄 source-class theorem target是

```text
|D_p(-2)| << F^(2-eta)log^C X,
equivalently |prime cell| << F^(4-eta)log^C X.          (56.3.7)
```

physical ledger为

```text
F^(-2) * F^2 prime moduli * F^(4-eta)
 = X^(1-eta/4).                                        (56.3.8)
```

任意 `eta>0`给 exact-half power saving；支付既有 strict `1/400`必须在全部
polynomial losses后 `eta>1/100`。当前已核查 sources没有这样的 theorem。

### 56.4 two exact firewalls

第一，modular ratio equality不是单一 rational ray。相对 primitive direction
`(a,b)`，同 residue fiber满足

```text
b e-a h=t p.                                           (56.4.1)
```

只有 `t=0`给 `(e,h)=(ak,bk)`与 common-`k` Möbius factorization；`t!=0`是 affine
translate，coefficient为 `mu(e_t+ak)`。每个 wrap虽短，aggregate仍可 endpoint-sized。
mod `13`中 `(5,3)`与 `(4,5)`同 modular ratio而 determinant=`13`；checker在
`[3,7]^2` exact计得 11 个 nonzero-wrap与 10 个 zero-wrap unordered collisions。
故

```text
COMMON_K_AS_UNIQUE_MODULAR_RATIO_FIBER
 = STOP_SCOPED_FALSE_COVER_NONZERO_WRAPS
COMMON_K_LONG_INTEGER_RAYS
 = PLAUSIBLE_LOCAL_MOBIUS_SUBLEMMA_ONLY.                (56.4.2)
```

这不重开第 6 节 TPC-18/TPC193 common-`k` cells。

第二，对 `K_A(h,ell)=S(ell,-2h conjugate(A);p)`有 exact complete-unit covariance

```text
sum_A K_A(h_1,ell_1)conjugate(K_A(h_2,ell_2))
 = p^2-p-1, if h_1ell_1=h_2ell_2 mod p,
 = -p-1, otherwise;
sum_A K_A(h,ell)=1.                                    (56.4.3)
```

centered moving-unit norm因此含 exact product-resonance floor，只返回临界
`F^4` endpoint。checker以 1,552 个 covariance cases与 52 个 mean cases exact
验证。因此

```text
GLOBAL_MOVING_UNIT_CAUCHY
 = STOP_SCOPED_EXACT_ENDPOINT_PRODUCT_RESONANCE.        (56.4.4)
```

它是 method obstruction，不是 actual signed correlation的 lower-bound反例。

### 56.5 source screen与 full loss ledger

对 `(56.3.4)`在 `ell`作 Poisson，保留 essential outer factor，得到结构

```text
F sum_(h,x,e_1,e_2 asymp F)
 U(h)V_x(x)mu(e_1)W_1(e_1)mu(e_2)W_2(e_2)
 e_p(-2h conjugate(xe_1e_2)).                           (56.5.1)
```

raw scale为 `F^5`，physical target为 `F^(4-eta)`。
[Mohammadi Theorem 1](https://arxiv.org/abs/2608.01203)可在 fixed outer
`(h,e_2)`后 literal取 `A=0`；
[Bourgain--Garaev Theorem 13](https://arxiv.org/abs/1211.4184)可在 fixed `h`后
literal附着 three-variable inverse product。但 outer triangle后两者均只给
`F^(5-2delta)`；关闭目标需 `delta>=(1+eta)/2`，source只给 unspecified positive
`delta`。已有 Gauss/Cauchy gain不能在 signed `h` correlation已被 triangle消费后再乘。

已核查的普通 divisor-in-progressions source也不附着。[Nguyen](https://arxiv.org/abs/2308.06839)
处理特殊 factorable/smooth composite modulus average，prime critical modulus与两条
Möbius rows不在 class；[Parry](https://arxiv.org/abs/2404.04749)的 `d_4`结果额外
平均 residue `a`，不能升级为 prescribed `a=-2`。这里 dual weights显式依赖 `p`，
且 dispersion重回 balanced resonance

```text
e_1e_2zw-e'_1e'_2z'w'=nu p.                            (56.5.2)
```

裁决为

```text
MOHAMMADI_WEIGHTED_A0_ATTACHMENT
 = SOURCE_BACKED_LOCAL_SUBLEMMA_EXPONENT_INSUFFICIENT
BOURGAIN_GARAEV_N3_ATTACHMENT
 = SOURCE_BACKED_LOCAL_SUBLEMMA_EXPONENT_INSUFFICIENT
DIRECT_LOCAL_BOX_TO_ENDPOINT_COMPILATION
 = STOP_SCOPED_NORMALIZATION_AND_EXPONENT_DEFICIT
STANDARD_LEVEL_OF_DISTRIBUTION_ATTACHMENT_IN_CHECKED_SOURCES
 = ABSENT.                                              (56.5.3)
```

### 56.6 selected construction、reserve与 release裁决

新的 first subgate与 construction priority为

```text
HB4_EXACT_HALF_ACTUAL_ATOM_DUAL_PRODUCT_DISPERSION
 = FIRST_SUBGATE_OPEN_NEW_THEOREM
HB4_EXACT_HALF_SIGNED_MODULUS_DUAL_TYPE_IV
 = SELECTED_CONSTRUCTION_OPEN_NEW_THEOREM.              (56.6.1)
```

执行顺序：

1. 给每个 emitted atom生成 `(56.2.1)` membership与 uniform dual-tail ledger；
2. 在 triangle前导出 squarefree `g,q`、imprimitive character、CRT与 Ramanujan
   cofactor版本的 `(56.3.3)`，保持 `mu(gq)`；
3. 只 square完整 centered modulus average，保留两条 literal Möbius rows并分离
   `(56.5.2)`的 exact diagonal/nonzero wraps；
4. 寻找 coefficient-sensitive determinant/Kuznetsov或 dispersion theorem，同时回收
  完整 `F^(-1)` signed Fourier cancellation与额外 power saving；
5. 按第 55.4 节 full contract重组所有 conductor/cofactor strata、Mellin tails与
   physical normalization。

prime family上 `mu(p)=-1`恒定，signed-modulus construction只从 full squarefree
average开始；不得给 prime subgate偷记 modulus-sign saving。HB4xHB2
`STRUCTURED_TWO_ROW_PAIRED_VORONOI`保持独立 reserve，第 55.5 节 first transform、
polar-main attachment与 `F^3` family deficit不变；两条 source lock不得拼接。

正式裁决为

```text
TPC_BIG_ROAD_V9_20260806_PRIME_GAUSS_DUAL_PRODUCT_EXACT_CENTERED_FIXED_
RESIDUE_EQUIVALENCE_COMMON_K_UNIQUE_FIBER_FALSE_NONZERO_WRAPS_GLOBAL_
MOVING_UNIT_CAUCHY_ENDPOINT_RESONANCE_LOCAL_INVERSE_PRODUCT_EXPONENT_
INSUFFICIENT_STANDARD_LOD_ABSENT_SIGNED_MODULUS_DUAL_TYPE_IV_SELECTED_
PAIRED_VORONOI_RESERVE_SEPARATE_NO_ARITHMETIC_TRIGGER_CHANNEL_REDESIGN
```

这是
`CHANNEL_REDESIGN_WITH_EXACT_GAUSS_DUAL_PRODUCT_NORMAL_FORM_AND_TYPED_TYPE_IV_TARGET`，
不是 arithmetic advance。all-`D`
uniformity、exactly-once physical cover、original/global normalization、tail/A/B、
actual packet attachment与 provenance全部未过；第 6 节 STOP cells、两个 O161
parents、pair-native reroute、H1、global architecture与 dynamics portfolio状态不变。
不创建 TPC-207、论文、paper directory或 PDF。

### 56.7 post-write fail-closed verification

本节发布前必须满足：

```text
POST_WRITE_STARTUP_REGRESSION = 22/22 PASS
POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_BIG_ROAD_CHECKS = 3/3 PASS
FM_V9_EXACT_ADDITIONS
  GAUSS_DUAL_FIXED_PRODUCT = 2 cases
  PRINCIPAL_NONZERO_FREQUENCY = 2 cases
  COMMON_K_WRAPS = 11 nonzero + 10 zero
  MOVING_UNIT_COVARIANCE = 1552 cases
  MOVING_UNIT_COMPLETE_MEAN = 52 cases
FM_ROUTE_FREEZE
  primary = HB4_EXACT_HALF_GAUSS_TWISTED_SIGNED_CORRELATION
  first_subgate = HB4_EXACT_HALF_ACTUAL_ATOM_DUAL_PRODUCT_DISPERSION
  selected_construction = HB4_EXACT_HALF_SIGNED_MODULUS_DUAL_TYPE_IV
  reserve = HB4xHB2_STRUCTURED_TWO_ROW_PAIRED_VORONOI
  source_lock_merge = false
  fixed_physical_h0 = 2
  fixed_atom_credit = 0
  strict_1_over_400 = UNPAID
  L2 = NONE
  TPC_207_TRIGGER = false
GIT_DIFF_CHECK = PASS
MARKDOWN_FENCES = ALL BALANCED
EXPECTED_TRACKED_DIFF = 5/5 EXACT
CACHED_DIFF = EMPTY
PROTECTED_UNTRACKED = 130 FILES
PROTECTED_MANIFEST
  = 9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
PAPER_PDF_NUMBERED_RELEASE_CREATED = NO
```

## 57. 2026-08-06 V10：induced CRT、primitive-projector lattice 与 monomial trace 大路

### 57.1 基线、分工与 claim boundary

V10 从已发布并三重 hash一致的 V9 commit启动：

```text
cd983e193fedfd6a274e52a84be69fecf0f0a26e
```

启动 tracked/index为空；130 个 protected untracked files保持原样，canonical
manifest仍为
`9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1`。
主控继续按根 `AGENTS.md`与 ARS source/proof/integrity流程调度三个
`READ_ONLY_FROZEN` agents：exact induced-Gauss proof audit、full physical source
attachment audit、conductor-native Type-IV source screen。三者均基于同一 commit，
`files_changed=[]`；正式写入只由主控完成。

V10 的最高 claim仍是 `POSITIVE_DERIVED_SUBLEMMA / CHANNEL_RETYPE`：证明了 full
squarefree lift的精确 finite normal form，修正一个错误 coefficient contract，并找到
两个 source-backed mechanism blueprints；没有证明 analytic power saving。

### 57.2 physical phase与 exact induced CRT

令 `g=(h,d)`、`d=gq`、`h=gu`、`A=e_1e_2`。active `d` squarefree，故
`(g,q)=1`，physical kernel精确分解为

```text
S(ell,-2gu conjugate(A);gq)
 =c_g(ell)S(ell conjugate(g),-2u conjugate(A);q).       (57.2.1)
```

对第二参数作 complete multiplicative inversion后，若继续使用 V8/V9 的
`tau_q(conjugate(chi),ell)` convention，则 summand必须显式保留

```text
chi(-2)conjugate(chi)(g).                              (57.2.2)
```

`-4`只属于 Pascadi `r_source=2` coordinate，与 first-coordinate unit scaling合并
后正好回到 `(57.2.1)`的 physical `-2`；两者不得拼接成另一个 shift。

写

```text
q=rs, r=cond(chi), chi=Ind_r^(rs)psi,
```

其中 `psi (mod r)` primitive，`g,r,s`两两互素。当前 Gauss convention下，exact
CRT为

```text
tau_(rs)(conjugate(chi),a)
 =psi(a conjugate(s)_r)tau_r(conjugate(psi),1)c_s(a)
  1_((a,r)=1).                                        (57.2.3)
```

所以

```text
chi(-2)conjugate(chi)(g)
 tau_q(conjugate(chi),1)tau_q(conjugate(chi),ell)

 =mu(s)c_s(ell)tau_r(conjugate(psi),1)^2
  psi(-2 ell conjugate(g)_r conjugate(s)_r^2)
  1_((ell,r)=1).                                      (57.2.4)
```

外乘 source `mu(gq)/phi(q)` 后，outer `mu(s)`与 Gauss-lift
`c_s(1)=mu(s)`精确相消：

```text
mu(g)mu(r)c_s(ell)/[phi(r)phi(s)]
 * tau_r(conjugate(psi),1)^2
 * psi(-2 ell conjugate(g)_r conjugate(s)_r^2)
 * 1_((ell,r)=1).                                     (57.2.5)
```

因此 V9 Step 2 若按 literal coefficient理解是 false：

```text
HB4_EXACT_HALF_LITERAL_MU_GQ_PRESERVATION_THROUGH_IMPRIMITIVE_CRT
 = STOP_SCOPED_FALSE_EXACT_COFACTOR_SIGN_CANCELLATION. (57.2.6)
```

但 cofactor不能取绝对值。若 `d_s=(s,ell)`、`t_s=s/d_s`，则

```text
c_s(ell)=mu(t_s)phi(d_s),
c_s(ell)/phi(s)=mu(t_s)/phi(t_s).                      (57.2.7)
```

故 `(57.2.5)`保留一个与 gcd stratum和复相位耦合的 reduced-cofactor sign。

### 57.3 character normal form与 primitive-projector lattice

令 `epsilon_r(conjugate(psi))=r^(-1/2)tau_r(conjugate(psi),1)`。一个 frozen
actual source atom的 character form为

```text
mu(g)mu(r)/phi(s) * r/phi(r)
 sum_(psi mod r)^* epsilon_r(conjugate(psi))^2
  psi(-2 conjugate(g)_r conjugate(s)_r^2)
  E_(1,g,s,t)(conjugate(psi))E_(2,g,s,t)(conjugate(psi))
  H_(g,s,t)(psi)B_(g,s,t)(psi),                       (57.3.1)
```

其中

```text
E_i: length F, literal mu(e_i), mask (e_i,gs)=1;
H:   length F/g, mask (u,s)=1;
B:   ell length F, coefficient c_g(ell)c_s(ell);
r asymp R>=F, s asymp F^2/(gr), g r s asymp F^2.        (57.3.2)
```

所有 actual signs/masks、`W^q(rs/Q)`、`W^s(s/S)`、common transform parameter、
product-atom `L1`、`r` partial-summation BV、tails与 unequal-length ranges均属于
contract。V9 prime superclass只是 `g=s=1` slice。

对 composite squarefree `r`，不能把 primitive characters换成全部 characters：

```text
sum_(psi mod r)^* psi(x)conjugate(psi)(a_0)
 =sum_(rho|r)mu(r/rho)phi(rho)1_(x=a_0 mod rho).       (57.3.3)
```

外乘 `mu(r)`后，sign变成 `mu(rho)`。进一步打开两枚 primitive Gauss sums，令
`t=r/rho`，则

```text
sum_(psi mod r)^* tau_r(conjugate(psi),1)^2 psi(A)
 =sum_(rho|r)mu(r/rho)phi(rho)
  S(1,A conjugate(t)_rho^2;rho).                       (57.3.4)
```

因此 full dual object不是 modulo `r`的一个 fixed-product residue，而是所有
`rho|r`的 Kloosterman projector lattice。prime `r=p`只有 `rho=1,p`，恰好退化成
V9 centered prime identity；prime gate不受影响。scoped firewall为

```text
HB4_EXACT_HALF_PRIMITIVE_PROJECTOR_SINGLE_FIXED_PRODUCT
 = STOP_SCOPED_FALSE_DIVISOR_LATTICE.                  (57.3.5)
```

### 57.4 exact monomial Type-IV normal form

在 `(57.3.4)`中 `phi(rho)`与
`phi(r)=phi(rho)phi(t)`的对应因子相消。打开全部 polynomials后，high-conductor
cell为

```text
sum_(g,rho,t,s: g rho t s asymp F^2, rho t>=F)
 mu(g)mu(rho)/[phi(t)phi(s)]
 sum_(e_1,e_2,u,ell)mu(e_1)mu(e_2)W(...)c_g(ell)c_s(ell)
 S(1,-2u ell conjugate(g e_1e_2(s t)^2);rho).          (57.4.1)
```

这里 `g,rho,t,s`两两互素、odd squarefree；`e_i asymp F`且
`(e_i,g rho t s)=1`；`u asymp F/g`且 `(u,rho t s)=1`；
`0<|ell|<<F`且 `(ell,rho t)=1`；`s asymp F^2/(g rho t)`。primitive
character消失后，这些 masks必须显式保留，不能继续由 zero extension代管。

必须在 norm前展开

```text
c_s(ell)=sum_(a|s,a|ell)a mu(s/a).
```

写 `s=ab`、`ell=ak`后得到 V10 clean normal form：

```text
sum_(g,rho,t,a,b: g rho t a b asymp F^2, rho t>=F)
 mu(g)mu(rho)mu(b)a/[phi(t)phi(a)phi(b)]
 sum_(e_1,e_2,u,k)mu(e_1)mu(e_2)W(...)c_g(ak)
 S(1,-2u k conjugate(g e_1e_2 a b^2 t^2);rho).        (57.4.2)
```

在 `(57.4.2)`中 `g,rho,t,a,b`两两互素、odd squarefree，
`ab asymp F^2/(g rho t)`，`0<|ak|<<F`、`(k,rho t)=1`，所以 literal
`k`-length为 `F/a`；并且 `(e_i,g rho t a b)=1`、`(u,rho t a b)=1`。
任何 fixed-prime trace engine都必须接受这些 actual masks与 unequal lengths。

所以 current analytic bridge有三条 coupled signed axes

```text
mu(g) mu(rho) mu(b),                                  (57.4.3)
```

和 literal monomial `u k/(g e_1e_2 a b^2 t^2) (mod rho)`。这比 V9 的
“signed modulus”名称更窄也更可证伪。

### 57.5 五篇 source screen与下一条 theorem contract

本轮逐 theorem核查五篇 primary sources，结论仅限这些 checked statements，不作
universal absence claim：

1. [Blomer--Pascadi](https://arxiv.org/abs/2607.24311)：fixed `rho` critical
   Kloosterman engine，local `rho^(-1/32)`；逐 cell使用会丢 `(57.4.3)`，不足 full
   outer ledger。
2. [Milićević--Qin--Wu](https://arxiv.org/abs/2511.07550)：fixed-modulus
   bilinear `Kl_2` engine；length hypotheses不覆盖全部 projector dyads，论文内部
   divisor不是 V10 averaged cofactor。
3. [Kerr--Shparlinski--Wu--Xi](https://arxiv.org/abs/2204.05038)：fixed-modulus
   Type-I/incomplete inverse-phase sublemma；不能同时保留两条 Möbius rows、
   Ramanujan axis与 primitive projector。
4. [Earnst](https://arxiv.org/abs/2603.22124)：prime conductor、`k=2`
   root-number-square moment真正有 power saving，是 `(57.3.1)`的 mechanism
   evidence；但 theorem是由 approximate functional equation打开的 fixed-twist
   `|L(1/2,psi)|^2` moment，mollifier coefficients只进入后续 application，二者都
   不能替换 actual `E_1E_2HB`。
5. [Fouvry--Kowalski--Michel--Sawin](https://arxiv.org/abs/2511.09459)：prime
   modulus arbitrary-coefficient monomial trace-function engine，和 `(57.4.2)`形状
   literal相容（仍须满足 source的 monodromy与 length hypotheses）；但没有
   varying/composite `rho`、outer `mu(rho)`及 `(g,a,b,t)` collective reassembly。

最接近的 positive source cells只能记为

```text
EARNST_ROOT_NUMBER_SQUARE_PRIME_MOMENT
 = SOURCE_BACKED_MECHANISM_ANALOGUE_NOT_ACTUAL_PACKET
FKMS_PRIME_MONOMIAL_TRACE_ENGINE
 = SOURCE_BACKED_LOCAL_ADAPTATION_BLUEPRINT.           (57.5.1)
```

下一条 central theorem必须直接声明：

```text
V10-COLLECTIVE-MONOMIAL-PROJECTOR-TYPE-IV

对完整 actual-source (57.4.2)，uniform于全部 admissible dyads、masks、
transform parameters、unequal source lengths与 physical-loss ledger，有

|V| << F^2 D^2 D^(-eta_D)X^o(1), D=F^2,              (57.5.2)

并且证明过程保留 mu(g)mu(rho)mu(b)，不得先逐
(g,rho,t,a,b) cell取绝对值再重组。
```

任意 `eta_D>0`给 exact-half arithmetic advance。因 `D=F^2=X^(1/2)`，等价
`F`-saving exponent为 `eta_F=2eta_D`；支付 strict `1/400`必须在完整
polynomial-loss ledger后 `eta_D>1/200`，等价 `eta_F>1/100`。proof engineering按三段进行：large
prime-like `rho`测试 FKMS；large complementary conductor `t`回到 Earnst型
root-number coordinate；balanced varying/composite `rho`才是需要新
dispersion/Kuznetsov/composite trace-family theorem的核心墙。

canonical V10 registry为

```text
HB4_EXACT_HALF_SOURCE_WEIGHT_ENVELOPE = FROZEN_TESTABLE_SUPERCLASS_CONTRACT
HB4_EXACT_HALF_ACTUAL_ATOM_MEMBERSHIP = OPEN_ATTACHMENT
HB4_EXACT_HALF_PRIME_GAUSS_DUAL_PRODUCT_IDENTITY = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PRIME_CENTERED_DUAL_PRODUCT = PROVED_EXACT_EQUIVALENCE
COMMON_K_AS_UNIQUE_MODULAR_RATIO_FIBER = STOP_SCOPED_FALSE_COVER_NONZERO_WRAPS
GLOBAL_MOVING_UNIT_CAUCHY = STOP_SCOPED_EXACT_ENDPOINT_PRODUCT_RESONANCE
MOHAMMADI_WEIGHTED_A0_ATTACHMENT = SOURCE_BACKED_LOCAL_SUBLEMMA_EXPONENT_INSUFFICIENT
BOURGAIN_GARAEV_N3_ATTACHMENT = SOURCE_BACKED_LOCAL_SUBLEMMA_EXPONENT_INSUFFICIENT
DIRECT_LOCAL_BOX_TO_ENDPOINT_COMPILATION = STOP_SCOPED_NORMALIZATION_AND_EXPONENT_DEFICIT
STANDARD_LEVEL_OF_DISTRIBUTION_ATTACHMENT_IN_CHECKED_SOURCES = ABSENT
HB4_EXACT_HALF_ACTUAL_ATOM_DUAL_PRODUCT_DISPERSION = FIRST_SUBGATE_OPEN_NEW_THEOREM
HB4_EXACT_HALF_INDUCED_GAUSS_CRT_SIGNED_PHASE_IDENTITY = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PHYSICAL_MINUS_TWO_G_S_UNIT_PHASE = PROVED_EXACT_SOURCE_LOCK
HB4_EXACT_HALF_LITERAL_MU_GQ_PRESERVATION_THROUGH_IMPRIMITIVE_CRT = STOP_SCOPED_FALSE_EXACT_COFACTOR_SIGN_CANCELLATION
HB4_EXACT_HALF_RAMANUJAN_COFACTOR_GCD_STRATIFICATION = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PRIMITIVE_PROJECTOR_SINGLE_FIXED_PRODUCT = STOP_SCOPED_FALSE_DIVISOR_LATTICE
HB4_EXACT_HALF_RAMANUJAN_DIVISOR_MONOMIAL_UNFOLDING = PROVED_EXACT_FINITE
EARNST_ROOT_NUMBER_SQUARE_PRIME_MOMENT = SOURCE_BACKED_MECHANISM_ANALOGUE_NOT_ACTUAL_PACKET
FKMS_PRIME_MONOMIAL_TRACE_ENGINE = SOURCE_BACKED_LOCAL_ADAPTATION_BLUEPRINT
HB4_EXACT_HALF_SIGNED_MODULUS_DUAL_TYPE_IV = RETYPED_PRE_CRT_SHORTHAND_ONLY
HB4_EXACT_HALF_SIGNED_CONDUCTOR_RAMANUJAN_COFACTOR_PRIMITIVE_PROJECTOR_DUAL_TYPE_IV = SELECTED_CONSTRUCTION_OPEN_NEW_THEOREM
```

### 57.6 compass映射、裁决与 release boundary

按用户给出的 `TPC岛屿地图`，Bridge A1现在从 prime centered-product桥进一步细分为
character/conductor坐标与 primitive-projector/monomial坐标；A2 paired-Voronoi仍是
独立 reserve。固定原子岛与 Pair-native/H1岛只负责 attachment，不自动提供 saving。
Bridge B distinguished-seed genericity、非自治 dynamics岛及 Hénon/几何辅助岛均保持
独立 OPEN，不给本解析 ledger记 credit。

V10正式 verdict为

```text
TPC_BIG_ROAD_V10_20260806_INDUCED_GAUSS_CRT_EXACT_PHYSICAL_MINUS_TWO_GBAR_
SBAR_SQUARED_PHASE_LITERAL_MU_GQ_PRESERVATION_FALSE_COFACTOR_SIGN_CANCELLATION_
RAMANUJAN_REDUCED_COFACTOR_SIGN_PRIMITIVE_PROJECTOR_SINGLE_FIXED_PRODUCT_FALSE_
SIGNED_KLOOSTERMAN_DIVISOR_LATTICE_RAMANUJAN_MONOMIAL_UNFOLDING_EXACT_EARNST_
ROOT_NUMBER_MECHANISM_FKMS_PRIME_TRACE_BLUEPRINT_NO_DIRECT_UNFROZEN_ATTACHMENT_
SIGNED_CONDUCTOR_RAMANUJAN_COFACTOR_PRIMITIVE_PROJECTOR_TYPE_IV_SELECTED_NO_
ARITHMETIC_TRIGGER_CHANNEL_RETYPE
```

即
`CHANNEL_RETYPE_WITH_EXACT_INDUCED_CRT_AND_PRIMITIVE_PROJECTOR_LATTICE`。
prime first gate、actual atom membership、paired-Voronoi reserve与全部 downstream
physical/provenance gates仍未过。fixed-atom credit=`0`、strict
`1/400=UNPAID`、`L2=NONE`、`TPC207_TRIGGER=false`。没有创建 TPC-207、论文、
paper directory、PDF或 build logs；TPC-27--32与 TPC-122 writers未执行。

### 57.7 post-write fail-closed verification

本节发布前必须满足并在最终同步后冻结：

```text
POST_WRITE_STARTUP_REGRESSION = 22/22 PASS
POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_BIG_ROAD_CHECKS = 3/3 PASS
POST_WRITE_INDEPENDENT_READ_ONLY_AUDITS = 3/3 PASS
FM_V10_EXACT_ADDITIONS
  INDUCED_COMPLEX_GAUSS_CRT = 4 cases
  INDUCED_OUTER_COFACTOR_CANCELLATION = 2 cases
  PHYSICAL_MINUS_TWO_G_S_PHASE = 1 case
  ACTUAL_E_H_SOURCE_MASKS = 2 cases
  COMPOSITE_PRIMITIVE_PROJECTOR = 64 cases
  PRIMITIVE_GAUSS_KLOOSTERMAN_LATTICE = 3 cases
  INDUCED_COMPOSITE_END_TO_END = 3 cases
  RAMANUJAN_GCD_STRATIFICATION = 160 cases
  RAMANUJAN_DIVISOR_MONOMIAL = 435 cases
  PHI_NORMALIZATION = 40 cases
  STRICT_ETA_D = 1/200
  STRICT_ETA_F = 1/100
GIT_DIFF_CHECK = PASS
MARKDOWN_RAW_MARKER_BALANCE
  HANDOFF = 1982 EVEN
  COMPASS = 70 EVEN
  README = 136 EVEN
  COMPILER = 512 EVEN
V10_NEW_REGIONS_STRICT_FENCE_ALTERNATION = PASS
PREEXISTING_24H_NESTED_TRIPLE_FENCE = RETAINED_NOT_REOPENED
EXPECTED_TRACKED_DIFF = 5/5 EXACT
CACHED_DIFF = EMPTY
PROTECTED_UNTRACKED = 130 FILES
PROTECTED_MANIFEST
  = 9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1
SUBAGENT_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
PAPER_PDF_NUMBERED_RELEASE_CREATED = NO
POST_REBASE_REMOTE_DELTA
  ORIGIN_MAIN_BASE = af10d4caf5f5291073bda473f3631fe94152ee7b
  RH_368_ONLY = ebcf29a + af10d4c
  TPC_SOURCE_LOCK_CHANGE = NONE
POST_REBASE_V10_COMMIT_BEFORE_FINAL_HANDOFF_AMEND
  = 9bbfbfe8e22b6f91e17298a8f953519ec3339559
POST_REBASE_STARTUP_REGRESSION = 22/22 PASS
POST_REBASE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_REBASE_BIG_ROAD_CHECKS = 3/3 PASS
POST_REBASE_GIT_DIFF_CHECK = PASS
POST_REBASE_PROTECTED_UNTRACKED = 130 FILES
POST_REBASE_PROTECTED_MANIFEST
  = 9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1
FINAL_REBASE_AND_REMOTE_HASH_SYNC = READY_FOR_FINAL_PULL_PUSH_VERIFICATION
```

## 53. 2026-08-05 `TPC_review3` 大路 V2：forced deletion cocycle、Haar variance theorem 与 PBAPT

### 53.1 基线、分工与 artifact scope

本轮启动 HEAD 与 `origin/main` 均为
`5e277223c025921748681f407861c8555bc50e31`。启动 `TPC_HANDOFF.md` 与
`TPC_COMPASS.md` hashes分别为

```text
9b0cf24ee85a21a591a7fbe8027a9396a114c5f74083dcaf7e968d0617d27a23
e871bbdeadb13697e4f02fbf9cd128db32959071343c401a725aff563550f8ef
```

`git pull --rebase origin main` 返回 already up to date；tracked/cached diff为空；
protected untracked为 130 files、manifest
`9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1`。
第 1 节 22 项只读回归 `22/22 PASS`。没有执行 TPC-27--32 legacy writers或
TPC-122 writer。

本轮使用 ARS research architecture、source verification与 devil's-advocate流程，
并由三个 read-only agents执行：

```text
TPC-BIGROAD-20260805-H3-RESONANCE
TPC-BIGROAD-20260805-H1-TYPED-ARCHITECTURE
TPC-BIGROAD-20260805-H4-DEVILS-AUDIT
```

三者都回报相同 baseline、`files_changed=[]` 与 tracked/cached diff为空；正式写入只
由主控完成。`TPC_review1/2/3.md` 与全部既有 protected untracked保持未修改、未
stage。新建 `research/tpc-big-road/` 是一个未编号 working artifact，不是 paper
directory、TPC-207或 theorem release bundle；其中包含完整 V2 contract、一个 exact
finite stress lab与一个不 import主 lab的 independent checker。

### 53.2 V1 的两个 broad redesign verdicts

第一，V1 的

```text
ell_X(W_(k_X))=o(a_(k_X)X)
```

不再作为 success target。critical cutoff `y asymp sqrt(2X)` 下，full-cycle local
mass满足 `a_y~8C_2e^(-2gamma)/log^2X`，而 Hardy--Littlewood standard heuristic
给 dyadic physical main `2C_2X/log^2X`；两者 ratio为

```text
exp(2gamma)/4 = 0.793054740... .
```

因此 V1 centering在标准预期下有 order-`a_yX` bias。这里 HL只用于检出错误
normalization，不作 premise或 arithmetic evidence；该 target正式标为
`HEURISTICALLY_MISCENTERED / DEPRIORITIZED`，不是无条件反例 theorem。

第二，mean/complement并不形成 homogeneous invariant splitting。`R_p1` 是 deletion
mask而非常数，故

```text
W_(k+1)=R_pW_k+a_k(R_p1-(1-2/p)1).
```

任何 logistic/Hénon carrier必须证明 forced-triangular evolution、uniform evaluation
norm与 accumulated physical forcing；只给 abstract complement contraction将按 broad
scope停止。正确的 profile target写成

```text
C_k(X)=a_kX Phi_2(log X/log p_k)+Error_k(X),
```

但 `Phi_2` 当前未构造为 theorem object，其 endpoint也未证。

### 53.3 Exact physical deletion-bias cocycle与 Fourier入口

对 `I_X=(X,2X]`，令

```text
C_k=sum_(n in I_X)B_k(n),
D_(k,p)=sum_(n in I_X)B_k(n)1_(p|n(n+2)),
epsilon_(k,p)=D_(k,p)-(2/p)C_k,
p=p_(k+1)>2.
```

逐项 deletion给

```text
C_(k+1)=C_k-D_(k,p),
E_(k+1)=(1-2/p)E_k-epsilon_(k,p),

C_(k+1)/(a_(k+1)|I_X|)
  = C_k/(a_k|I_X|)-epsilon_(k,p)/(a_(k+1)|I_X|).
```

最后一式可逐 stage exact telescope。加法正交性又给

```text
epsilon_(k,p)
  = (1/p)sum_(1<=a<p)(1+e_p(2a))
      sum_(n in I_X)B_k(n)e_p(an).
```

所以 physical renormalization与非零 additive Fourier modes已有 exact bridge；但
它没有 TPC-32 的 packet signs、actual masks、outer labels、content、copy order或
`JQ^2 asymp XQ` normalization，不能升级为 packet crosslink。

`tpc_big_road_lab.py` 以 exact rational recurrence核验该 telescope与 critical-cutoff
primality identity。`X=10^4,10^5,10^6` 的 finite h0=2 ratios分别为

```text
0.8356729807
0.8495112539
0.8499075188
```

只作 normalization stress，不作渐近或 TPC claim。

### 53.4 H3-metric 的真实 theorem advance

沿第 52 节 exact profinite system，令

```text
Z_n(x)=1_(E_n)(T^n x),
alpha_n=mu(E_n),
y_n=sqrt(n+2).
```

对 `m<n`、`d=n-m`、`q=y_m`，已有

```text
Cov(Z_m,Z_n)=alpha_m alpha_n(K_q(d)-1).
```

本轮把每个 local factor完整展开。`p=2,3` 必须单列：

```text
k_2(d)=2*1_(2|d),
k_3(d)=3*1_(3|d).
```

对 `p>=5`，

```text
k_p(d)
 = 1-4/(p-2)^2
   +2p/(p-2)^2*1_(p|d)
   +p/(p-2)^2*(1_(p|d-2)+1_(p|d+2)).
```

其 local coefficient `ell^1` norms分别为
`2,3,(1-2/p)^(-2)`，完整 residue mean均为 `1`。把 product展开为 compatible CRT
classes，每个 class在任意 integer interval的 endpoint error至多 `1`，得到 exact
uniform theorem

```text
|sum_(d in I)(K_q(d)-1)|
  <= D(q):=6 product_(5<=p<=q)(1-2/p)^(-2).              (53.1)
```

固定 `m` 后对 monotone `alpha_(m+d)` 作 Abel summation，右侧为
`alpha_(m+1)D(y_m)`。由于对 `y>=3` 有 exact

```text
alpha(y)=(1/6)product_(5<=p<=y)(1-2/p),
alpha(y)^2D(y)=1/6,                                      (53.2)
```

每个 grouped off-diagonal contribution至多 `1/6`。加上 diagonal并记 variance中
off-diagonal出现两次，得到

```text
Var_mu(sum_(X<n<=2X)Z_n) <= X/2+O(1),
Var_mu(sum_(3<=n<=N)Z_n) << N.                           (53.3)
```

Mertens lower scale给 expectation `asymp N/log^2N`，Chebyshev加平方子序列
Borel--Cantelli于是推出 Haar-a.e. seed无穷次命中。

该结论精确记录为

```text
H3_METRIC = PROVED_HAAR_MOVING_VARIANCE_O_N
H4_POINTED_x0 = ENDPOINT_EQUIVALENT_TARGET_OPEN
ARITHMETIC_ADVANCE = NO.
```

independent checker在 finite fixtures上逐 residue核验 local formula、完整周期 mean、
sampled interval endpoint bound、two-cutoff CRT joint probability、(53.2) 与 brute
moving variance；universal `q/I`、Abel及 Borel--Cantelli结论由上面的符号证明承担，
不把有限 checker冒充机器证明。它拒绝 missing `d+2` resonance与 subcritical
primality cutoff mutations，并另核验 `p|h` 时 local rank为一的 control fixture。

### 53.5 Review3 四路汇流的 typed stop与唯一 crosslink gate

目前精确连通的 primorial component为：令

```text
c_k^sieve(d,e)=mu(d)mu(e),
(M_kc)(r)=sum_(d,e|P_k)c(d,e)1_(d|r)1_(e|r+2),
Sigma_k=(I-Pi_k)M_k.
```

有限 Möbius inversion给逐 residue identities

```text
M_k c_k^sieve=B_k,
Sigma_k c_k^sieve=W_k.
```

另一 component是 TPC-32 literal determinant-two atom经 TPC-34/37 TT-star/Gram
进入 far-copy energy。其 O161 affine values一般含大于 `p_(k_X)` 的素因子，不能
改名为 `(d,e)|P_k`；截 smooth part不保持 Möbius sign。更根本地，post-TT-star
pair/Gram由 `c` 与 `-c` 得到相同 quadratic data，却对应相反 linear pushforward，
所以 pair-native不能逆生 legacy H1或 `W_k`。

因此新增 broad cell：

```text
DECLARED_TPC_REVIEW3_20260805_PAIR_O161_PACKET_TO_PRIMORIAL_
LINEAR_CROSSLINK_DIRECT_COMPOSITION_V1
  = STOP_SCOPED_OBJECT_ALPHABET_LINEAR_QUADRATIC_AND_NORMALIZATION_MISMATCH.
```

只允许以下大型 theorem重开：在 complete actual `h0=2` packet family上构造
pre-TT-star occurrence lift `L_X` 与 source-backed `J_X`，使

```text
Sigma_k J_X L_X c_X = nu_X W_k+R_X
```

在 `V_k` 中逐 residue成立，同时保留 signs、masks、weights、outer labels、
multiplicities、prefix order、clocks及 normalization，并给

```text
ell_X Sigma_k J_X L_X c_X
  = NormReturn_X(PhysicalReassembly_X(c_X)),
|ell_X(R_X)|=o(nu_X a_kX).
```

只得到 scalar equality、formal packet、post-TT-star inverse或 unpaid normalization，
均 fail closed。

### 53.6 Ford--Maynard prime-producing source lock与 first fatal

Ford--Maynard, *On the theory of prime-producing sieves*, `arXiv:2407.14368`
对 nonnegative `a_n`、comparison `b_n` 与 `w_n=a_n-b_n`建立 Type I/II框架，
并明确 substantial Type II是 prime lower bound所必需；`nu=0` 可容纳 prime-free
parity伪序列。该 source支持 PBAPT的 theorem contract，不支持把现有 packet宣布为
已满足 hypotheses。经典 Friedlander--Iwaniec asymptotic sieve的 bilinear axiom也
支持同一 parity-breaking定位。

两个直接 candidates都 fail closed：

1. `a_r=B_(k_X)(r)/a_(k_X), b_r=1`：`B_(k_X)(2n)=0`，故 Type I在
   multiplier `m=2` 给 linear negative bias；
2. `a_r=Lambda(r+2)` 或 `(log X)1_(r+2 prime), b_r=1`：在 primes上求和时后者是
   exact weighted twin count，前者另有 `r+2` 为高次 prime power的标准低阶 tail；
   但 `m=2` 同样给
   `sum(Lambda(2n+2)-1)=-X/4+O(log^2X)`。

locally matched comparison或 `W`-trick可能先移除有限 local biases，但本轮没有
构造。即使修复，Ford--Maynard所需 arbitrary-coefficient multiplicative `mn`
Type II仍为 `OPEN`；(53.1)--(53.3) 的 additive shift covariance不推出它。

### 53.7 新主干、状态 ledger与 STOP 防火墙

V2 唯一 master class为

```text
PARITY_BREAKING_AFFINE_PATTERN_TRANSFERENCE_THEOREM (PBAPT):

general affine decomposition
  + uniform Type I
  + determinant-uniform natural-scale fixed-atom Type II
  + target-coupled Gram/Bessel reassembly
  + all-D / tail / A-B / exactly-once cover
  + original/global normalization and complete loss ledger
  -> prime-producing lower bound.
```

它必须先对与 prime outcomes无关的一类 admissible affine patterns陈述；`h0=2`
只能是 application。当前 ledger为：

| gate | status |
|---|---|
| exact primorial/event/deletion algebra | `PROVED` |
| H3 metric Haar variance | `PROVED_HAAR_VARIANCE_O_N` |
| legacy H1 / pre-TT-star occurrence | `OPEN / NOT_TESTABLE` |
| forced-triangular dynamical carrier | `HYPOTHESIS` |
| determinant-uniform fixed-atom Type II | `OPEN`; credit `0` |
| target-coupled reassembly / `Q^3/J` | `OPEN` |
| Ford--Maynard locally matched Type I | `NOT_CONSTRUCTED` |
| Ford--Maynard multiplicative Type II | `OPEN` |
| distinguished seed `0` | `ENDPOINT_EQUIVALENT_TARGET` |
| strict `1/400` | `UNPAID` |
| `L2` | `NONE` |
| TPC-207 trigger | `false` |

第 6 节全部旧 method cells保持 `STOP_SCOPED`；尤其 TPC193 V1、common-k V1、
tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1均未重开。两个 O161
pointwise parents、pair-native reroute、legacy H1与 global architecture保持 `OPEN`。

### 53.8 下一轮只执行三个大动作

```text
A. FM/Buchstab compiler:
   construct or rule out a locally matched comparison;
   align the first literal Type-I/II formula and ranges.

B. General fixed-atom Type-II attack:
   prove or broadly stop determinant-uniform natural-scale saving
   for a prime-outcome-independent affine class.

C. Target-coupled reassembly/crosslink:
   construct or broadly rule out the coefficientwise J_X gate,
   with exactly-once cover and full normalization ledger.
```

不再把邻近 source mismatch、schema字段或有限数值补丁各自生成为 paper。只有
`H_occ/H_dyn/H3_phys` 发生 theorem-backed变化才记 `CHANNEL_ADVANCE`；若上述三项
都失败一个 named master criterion，则记一次 broad `CHANNEL_STOP`。即使局部 gate
转正，也不自动创建 TPC-207；现有编号 provenance cascade与所有 downstream gates
仍须另行通过。

### 53.9 verification与 publication boundary

本轮预期正式 files只有：

```text
TPC_HANDOFF.md
TPC_COMPASS.md
research/tpc-big-road/README.md
research/tpc-big-road/tpc_big_road_lab.py
research/tpc-big-road/tpc_big_road_independent_checker.py
```

没有 paper/PDF/build log。发布前必须重跑第 1 节 22 项、TPC-111/124/126/127 四项
supplemental、两个新 `--check`、Markdown fences、protected manifest与 staged-file
allowlist。只 stage上述五个 files。commit/push后确认 local HEAD、`origin/main` 与
remote `refs/heads/main` 三 hash完全一致。

pre-rebase final audit为：

```text
POST_WRITE_STARTUP_REGRESSION = 22/22 PASS
POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
BIG_ROAD_LAB_CHECK = PASS; 16 exact cases
BIG_ROAD_INDEPENDENT_CHECK = PASS; 170 local cases + N=50 variance fixture
BIG_ROAD_STRESS_X_1E4_1E5_1E6_1E7 = PASS; FINITE_DIAGNOSTIC_NOT_THEOREM
GIT_DIFF_CHECK = PASS
MARKDOWN_FENCES = HANDOFF 1628; COMPASS 50; BIG_ROAD_README 92; ALL BALANCED
NUMBERED_SECTIONS = 53 UNIQUE; DUPLICATES=0; MISSING=0
PROTECTED_UNTRACKED = 130 FILES
PROTECTED_MANIFEST
  = 9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1
SUBAGENT_FINAL_FORMULA_AUDIT = PASS
SUBAGENT_FINAL_ADVERSARIAL_AUDIT = PASS_WITH_NOTES; ALL NOTES RESOLVED
SUBAGENT_FINAL_ARCHITECTURE_AUDIT = PASS_AFTER_H_OCC_PAIR_NATIVE_SPLIT
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

发布前 `git fetch origin main` 把 `origin/main` 从启动值推进至
`54709f1c0b30e7970ebca010973a24a1d2656c7e`。该单一 remote commit只修改
`RH_HANDOFF.md` 并新增 RH-362 的 22 个 release files；与上述五个 TPC目标文件无
重叠。按用户已声明的 RH out-of-scope边界，本轮不审核或执行 RH-362 writers，
只在本轮 allowlist commit后安全 rebase并重跑全部 TPC checks。

allowlist commit在旧 base上为 `96a49e3`；`git pull --rebase origin main` 成功把它
重放到 RH-362 tip之上，未发生冲突，临时 post-rebase tip为 `498b219`。post-rebase
结果为：

```text
POST_REBASE_BASE = 54709f1c0b30e7970ebca010973a24a1d2656c7e
POST_REBASE_STARTUP_REGRESSION = 22/22 PASS
POST_REBASE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_REBASE_BIG_ROAD_CHECKS = 2/2 PASS
POST_REBASE_GIT_DIFF_CHECK = PASS
POST_REBASE_MARKDOWN_FENCES = 1628 + 50 + 92; ALL BALANCED
POST_REBASE_NUMBERED_SECTIONS = 53 UNIQUE; DUPLICATES=0; MISSING=0
POST_REBASE_PROTECTED_UNTRACKED = 130 FILES
POST_REBASE_PROTECTED_MANIFEST
  = 9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1
POST_REBASE_EXPECTED_TRACKED_FILES = 5/5 EXACT
RH362_WRITERS_OR_TESTS_EXECUTED = NO
```

## 52. 2026-08-05 prime-dynamics 全局罗盘：从 `RLR^infinity` 正测度误区到 pointed shrinking-target 主路线

### 52.1 基线、任务范围与 source locks

本轮启动时 HEAD 与 `origin/main` 均为
`10efbe0de1d08b512ae765d2c30230b23940f72a`，`TPC_HANDOFF.md` 的启动
SHA-256 为
`26205b4fda4eb1bb5d1df693514d204558db3e2417c138de3a9223cdddda2ab7`。
working tree没有 tracked/cached diff；127 个既有 protected untracked files 的
manifest仍为
`35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f`。
启动 `git pull --rebase origin main` 返回 already up to date；第 1 节 22 项只读
回归为 `22/22 PASS`。TPC-27--32 legacy writers与 TPC-122 writer均未执行。

本轮不继续穷举 small-content far-copy 的微型变体，而执行一个有限的 global
compass gate：判断“prime/sieve symbolic dynamics + logistic/Hénon + gap-2
measure/recurrence”究竟是通路、启发桥、当前理论缺口还是结构死路。三个 read-only
agents按根 `AGENTS.md` 完成：

```text
TPC-COMPASS-20260805-DYNAMICS-SOURCE-LOCK
TPC-COMPASS-20260805-DYNAMICS-ARCHITECT
TPC-COMPASS-20260805-DYNAMICS-DA
```

三者回报同一 HEAD/handoff hash、`files_changed=[]`、tracked/cached diff为空；所有
正式写入只由主控完成。仓库内 theorem anchors为：

1. RH-1 `main.tex:154--219,226--325,503--569`：cumulative sieve words、
   `RLR^infinity` pointwise limit、band-merging critical orbit、entropy obstruction；
2. RH-2 `main.tex:193--205,213--279,305--328,778--791`：natural prime word的
   unique inverse kneading realization及其 nonpredictive boundary；
3. RH-3 `main.tex:148--245,738--747,749--904`：`u_c` ACIP/ergodicity、
   conditional rank-two sequential Birkhoff architecture及 actual schedule缺口；
4. RH-4 `main.tex:685--766`：nonautonomous memory-loss boundary与 Hénon exact
   symplectic/reversible structure；
5. TPC-1 `main.tex:99--127,194--233,625--684,703--846`：finite primorial
   pair cylinder、exact primality cutoff、period mismatch与 prime-sensitive lower-bound
   barrier。

已发表的 Wang, *The emergence of prime distribution from low-dimensional
deterministic chaos*, DOI `10.1080/27684830.2026.2684334` 把 dynamical sieve
isomorphism与 twin-prime fixed point明确列为 Conjecture A/B及 heuristic/numerical
framework；本轮按其实际 claim strength使用，不把发表状态升级成 theorem。
Haydn--Nicol--Persson--Vaienti `arXiv:1103.2113`、Haydn--Nicol--Török--Vaienti
`arXiv:1406.4266` 与 Fishman--Mance--Simmons--Urbański `arXiv:1409.7950`
只证明 dynamical/nonautonomous shrinking-target theorem这一“工具类型”真实存在；
它们的 map class、target class与 a.e. initial laws没有 literal attachment到本轮
arithmetic seed或 quadratic/Hénon schedule，因而不给 TPC theorem credit。

只读 remote source refresh得到：

```text
maris205/riemann_logistic main
  = 9584407bf5bf2488b1b06ba97178ada679a66549
maris205/riemann_henon main
  = f86bf21a32ad5bcb21ba81d312cc68e91bcc7db0
```

`D:/26-aimath/logistic_riemann` 与 `D:/26-aimath/henon_riemann` 本地镜像都不是
Git worktree；未建立其 bytes与上述 remote heads的 crosswalk，故只作 heuristic
context，不计 committed theorem evidence。本轮不触及 RH zero-spectrum 或
Hilbert--Pólya路线。

### 52.2 四个不能拼接的 orbit/measure 对象

令 `f_u(x)=1-u*x^2`，`u_c` 为第一 band-merging 参数，`b=u_c-1`。当前精确
source-backed对象为：

| object | exact fact | status for TPC |
|---|---|---|
| cumulative sieve pointwise limit | 对每个固定 `n>=2`，一旦其某个素因子进入 sieve，`Q_k(n)=R` 永久成立；故 `Q_k -> RLR^infinity` | `PROVED_SEGMENT`，但逐点极限擦除全部固定素数 |
| band-merging critical orbit | `0 -> 1 -> -b -> b -> b`，critical-value itinerary为 `RLR^infinity`；其 shift orbit closure是 `{RLR^infinity,LR^infinity,R^infinity}`、entropy `0` | direct arithmetic recurrence为 `STRUCTURAL_DEAD_END`；该指定 orbit没有无穷多个 `LRL` |
| full `u_c` attractor with ACIP `mu_c` | `f_(u_c)` 有唯一 ACIP，遍历但不 mixing；由 full-branch Markov geometry，autonomous `LRL` cylinder包含非退化区间并有正 `mu_c` measure | positive measure是合法 dynamical fact，但 typical orbit没有 prime semantics |
| natural prime word `P` | `P(n)=L` iff `n` prime (`n>=2`)；存在唯一 `u_P` 使 critical itinerary等于 `P` | exact inverse encoding为 `PROVED_SEGMENT`；作为独立 generator是 circular/wrong direction |

这给出对本轮大胆命题的精确裁决：

```text
ERGODIC_MAP != GENERIC_DISTINGUISHED_CRITICAL_ORBIT
POSITIVE_UC_ACIP_LRL_CYLINDER != ARITHMETIC_TWIN_CYLINDER
RLR_INFINITY_CRITICAL_ITINERARY != TYPICAL_UC_ATTRACTOR_ITINERARY
```

对 exact prime word则有完全正确但不产生新下界的 identity：对 `n>=3`，

```text
sigma^n(P) in [LRL]
  iff n and n+2 are both prime.
```

其普通 natural-time cylinder measure必为零，因为

```text
(1/N) sum_(n<N) 1_[LRL](sigma^n(P))
  = pi_2(N)/N
  <= pi(N)/N
  -> 0.
```

因此 fixed positive ordinary invariant measure加普通 Birkhoff若真能无损作用于
arithmetic word，会给正自然密度 `c*N`，远强于预期 `N/(log N)^2`；这不是
“尚缺一个小 lemma”，而是 normalization/object mismatch。合法的“正测度”必须
解释成随 stage缩小但不可求和的 rare-event mass，或显式改用
`ds=dn/(log n)^2` 的 aging clock。用公式说，正确候选是

```text
p_n > 0,
(log n)^2 p_n >= c > 0,
sum_n p_n = infinity,
```

而不是 `p_n >= c > 0`。

### 52.3 非循环的 arithmetic base 与最短主路线

本轮最强的非循环 formulation不需要先用完整 prime word选择 `u_P`。令

```text
X_arith = inverse_limit_q Z/qZ = Z_hat,
T(x) = x+1,
m = Haar probability on Z_hat,
rho_y = product_(p<=y) (1-1/p),
E_2(y) = {x : p does not divide x(x+2) for every prime p<=y}.
```

CRT给出 exact finite-stage mass

```text
m(E_2(y))
  = (1/2) product_(2<p<=y) (1-2/p) > 0,
m(E_2(y))/rho_y^2 -> 2*C_2.
```

令 `y_n=sqrt(n+2)`、`E_n=E_2(y_n)`，并取 distinguished arithmetic orbit
`x_n=T^n(0)=n`。对每个 `n>=3`，任一 `m in {n,n+2}` 若 composite就有一个
prime divisor不超过 `sqrt(m)<=sqrt(n+2)`，故

```text
T^n(0) in E_n
  iff n and n+2 are both prime.
```

这是只用有限整除关系的 exact stage identity，没有把未来 twin-prime答案写入
parameter。Mertens product又给

```text
m(E_n) asymp 1/(log n)^2,
sum_n m(E_n) = infinity.
```

所以用户所说“归根到底是测度问题”有一个完全准确的 repaired版本；其依赖 DAG为：

```text
finite primorial systems + CRT local pair mass                 [PROVED]
                    |
                    v
(Z_hat, x->x+1, Haar) + E_n=E_2(sqrt(n+2))                    [PROVED]
                    |
                    +--> positive nonsummable moving mass      [PROVED]
                    |
                    +--> T^n(0) in E_n iff twin at n           [PROVED]
                                      |
                                      v
POINTED_CRITICAL_SHRINKING_TARGET_RECURRENCE_AT_0               [OPEN]
                                      |
                                      v
infinitely many twin primes
```

唯一主墙不是定义或 local measure，而是

```text
CRITICAL_SCALE_POINTED_ODOMETER_SHRINKING_TARGET_RECURRENCE
```

即从一个独立可核验的 discrepancy/correlation criterion证明

```text
sum_(n>=3) 1_(E_n)(T^n(0)) = infinity.
```

普通 Poincaré recurrence不能处理 moving targets；ordinary ergodic theorem不能
处理 complexity随 `P_(sqrt n)=exp((1+o(1))*sqrt n)` 增长而 observation time只有
`n` 的 diagonal family；odometer本身也不 mixing。TPC-1 的完整 primorial period
与 primality-exact physical window不重叠，正是同一 endpoint/period mismatch。
因此“每个 `E_n` 正测度”与“总 mass发散”都还不能单独控制指定点 `0`。

### 52.4 logistic/Hénon 应放在 DAG 的哪里

nonautonomous logistic route只有在它增加一个独立的 pointed recurrence mechanism
时才有证明价值。所需 strengthened hypothesis不能只是 limit kneading word equality，
而必须在同一 construction上给：

```text
H_STAGE_EVENT:
  pi_(n+1) o F_n = S_n o pi_n,
  1_(E^dyn_n)(F_(n-1)...F_0(z_*)) = 1_(E_n)(T^n(0));

H_EVOLUTION_MEASURE:
  (F_n)_* mu_n = mu_(n+1)
  or an exact path-space law, with no ACIP/Haar/empirical-measure swap;

H_RARE_MASS:
  p_n=mu_n(E^dyn_n) >= c/(log(n+2))^2
  from an independent source, not calibration to Hardy--Littlewood;

H_MOVING_MIX:
  uniform tower/mixed-block/rank-two complement contraction and
  moving-target multiplier/covariance bounds for the actual schedule;

H_POINTED:
  the distinguished arithmetic seed z_* belongs to the resulting
  Borel--Cantelli set, or satisfies a direct deterministic discrepancy bound.
```

RH-3 的 sequential theorem证明了 `H_MOVING_MIX` 一类结论在 uniform block-memory
loss、bounded multipliers与 common paired means下如何导出 exponential covariance，
但 actual logarithmic quadratic schedule仍缺 matched tower、mixed-block isolated
rank-two cluster、arbitrary-product contraction、moving phase labels与 internal
`2 by 2` cocycle；其结论也只对 allowed initial densities的 almost every point，
不是 `H_POINTED`。published Conjecture A/B 可作为 `H_STAGE_EVENT/H_RARE_MASS`
的启发来源，不能作已证明 attachment。

Hénon若加入路线，还必须先有真正 factor theorem：

```text
rho_(n+1) o H_n = f_n o rho_n,
E^Henon_n = rho_n^(-1)(E^logistic_n),
rho_*(mu^Henon_n) = mu^logistic_n,
```

并保持同一 stage、seed与 event。当前

```text
H_a(x,y)=(1-a*x^2-y,x),
x_(n+1)=1-a*x_n^2-x_(n-1),
det(DH_a)=1
```

只给 exact symplecticity与 reversibility；`pi_x o H_a` 不等于 logistic map，
`y=0` 也不是 invariant graph。area preservation不能自动传递 prime itinerary、
gap-2 event或 pointed genericity。因此 Hénon是 `OPTIONAL_AUXILIARY_OPEN`，不是
当前主 spine，更不绕过 pointed recurrence node。

### 52.5 条件 closure lemma：一旦真正成为测度问题，最后一步很短

令 `Z_n=1_(E^dyn_n) o Phi_n` 定义在同一 initial probability space上，
`p_n=E[Z_n]`，`S_N=sum_(n<=N) Z_n`，`A_N=sum_(n<=N) p_n`。若 source-backed
theorem真正给出

```text
p_n >= c/(log(n+2))^2,
Var(S_N) <= C*N,
```

则 `A_N >> N/(log N)^2`。取 `N_j=j^2`，Chebyshev给

```text
P(|S_(N_j)-A_(N_j)| > A_(N_j)/2)
  << N_j/A_(N_j)^2
  << (log j)^4/j^2.
```

右侧可求和，故 Borel--Cantelli推出 almost every initial point沿 `N_j` 最终满足
`S_(N_j)>=A_(N_j)/2 -> infinity`。所以无需先证明完整 Hardy--Littlewood
asymptotic；一个 natural rare-mass lower bound与 `O(N)` variance已经足够得到
infinitely many hits。

这项 closure是 elementary derived theorem pattern，不是 arithmetic advance，原因
正是 almost-everywhere set尚未证明包含 `z_*`。不得把

```text
mu_0(BC_set)=1
```

改写成

```text
z_* in BC_set.
```

若 exact event factor只依赖 arithmetic base，那么同一 fiber上的额外 Hénon/logistic
coordinates也不能改变 base event sequence；extension中的 generic lift不能替代
arithmetic seed的 pointed theorem。这是对“加一个更混合的高维 lift即可自动完成”
的 no-free-promotion firewall，不是对未来 transversality/pointed discrepancy theorem
的 nonexistence claim。

### 52.6 路线分类、精确 verdict 与唯一高杠杆 reopen

| route | current classification | first fatal / next theorem |
|---|---|---|
| literal `RLR^infinity` critical orbit + ordinary recurrence | `STRUCTURAL_DEAD_END` | orbit eventually fixed；没有 infinite `LRL` |
| typical `u_c` ACIP orbit + positive `LRL` mass | `PROVED_DYNAMICS_WRONG_ARITHMETIC_OBJECT` | no prime/event/seed crosswalk |
| exact `u_P` prime kneading orbit | `PROVED_INVERSE_ENCODING_ONLY` | independent generator/prediction is circular |
| profinite/primorial moving target | `BEST_OPEN_ROUTE / CURRENT_THEORY_GAP` | pointed critical shrinking-target recurrence at `0` |
| nonautonomous logarithmic logistic | `PLAUSIBLE_HEURISTIC_BRIDGE` | exact stage/event factor、actual tower/cocycle、rare mass、pointed seed |
| Hénon lift | `OPTIONAL_AUXILIARY_OPEN` | semiconjugacy/event/measure/seed transfer absent |
| TPC-32 analytic small-content far-copy parent | `OPEN_BACKUP` | 第 51 节 extra `J` / raw zero-column Bessel wall unchanged |

第 6 节 broad cell

```text
DECLARED_RH1_4_TPC1_20260805_AUTONOMOUS_LIMIT_INVERSE_PRIME_KNEADING_
NONAUTONOMOUS_SCHEDULE_HENON_LIFT_TO_DISTINGUISHED_E2_RECURRENCE_
DIRECT_COMPOSITION_V1 = STOP_SCOPED
```

只停止把当前 objects直接拼成 TPC。所有 strengthened gates保持 `OPEN`。

本轮精确有限 verdict为：

```text
TPC_DYNAMICS_COMPASS_20260805_RLR_INFINITY_CRITICAL_ORBIT_EVENTUALLY_FIXED_
UC_ACIP_LRL_POSITIVE_BUT_ARITHMETICALLY_WRONG_OBJECT_
EXACT_PRIME_LRL_ORDINARY_MEASURE_ZERO_
PROFINITE_NONAUTONOMOUS_RARE_EVENT_ROUTE_EXACT_THROUGH_MOVING_MASS_
POINTED_CRITICAL_RECURRENCE_ABSENT_
LOGISTIC_HENON_STAGE_EVENT_MEASURE_SEED_ATTACHMENTS_ABSENT_
NO_TRIGGER_STOP_SCOPED_ROUTE_OPEN

THEOREM_TRIGGER = false
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_CREATED = false
```

唯一值得投入下一大轮、且不是微型补丁的 theorem target为：

```text
CRITICAL_SCALE_POINTED_ODOMETER_SHRINKING_TARGET_RECURRENCE
```

可接受的 reopen evidence必须给独立、可核验的 endpoint discrepancy/covariance
criterion并证明它适用于 `x=0`；或给一个 exact stage-preserving nonautonomous
logistic/Hénon factor，加 actual rare-event mass、moving covariance与 distinguished
seed theorem。不得把 `m(E_n)>0`、`sum m(E_n)=infinity`、ordinary a.e. DBC、
complete-period Haar mean、inverse `u_P` encoding或 Conjecture A/B本身当成该结论。

任一 dynamics subgate转正可记为真实路线进展，但不自动创建 TPC-207。只有
prime-sensitive pointed recurrence真正改变 arithmetic theorem state，且另行通过
all-`D` uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual packet attachment与完整 provenance gates，才进入
现有 numbered release pipeline。第 6 节全部旧 method cells、两个 O161 parents、
pair-native、H1与 global architecture状态不变。

### 52.7 distilled bold-channel controller 与 publication boundary

本轮没有创建 TPC-207、论文、paper directory、PDF、数值模型或构建日志。没有修改
RH/TPC paper artifacts，也没有把 external local mirrors纳入 source locks。用户要求
压缩 200+ research nodes并切换到 bold-channel mode后，正式预期 tracked writes仅为
`TPC_HANDOFF.md` 与根级 `TPC_COMPASS.md`；后者是 controller/route ledger，不是
paper或 theorem artifact。所有 protected untracked必须原样保留且不得纳入提交。

正式写入后必须重跑第 1 节 22 项只读回归、supplemental checks、Markdown fence与
protected manifest；只 stage上述两个预期 files。commit/push后必须验证 local `HEAD`、
`origin/main` 与 remote `refs/heads/main` 三个 hash完全一致。

发布前只读结果为：

```text
POST_WRITE_BOOTSTRAP_REGRESSION = 22/22 PASS
POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_GIT_DIFF_CHECK = PASS; TPC_HANDOFF.md + TPC_COMPASS.md ONLY
POST_WRITE_MARKDOWN_FENCES = 1566 MARKERS BALANCED
POST_WRITE_COMPASS_FENCES = 44 MARKERS BALANCED
TPC_COMPASS_SHA256
  = e871bbdeadb13697e4f02fbf9cd128db32959071343c401a725aff563550f8ef
POST_WRITE_NUMBERED_SECTIONS = 52 UNIQUE; DUPLICATES=0
STARTUP_PROTECTED_UNTRACKED = 127 FILES
STARTUP_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
LATE_UNTRACKED_PRESERVED_NOT_STAGED
  = TPC_review1.md + TPC_review2.md + TPC_review3.md
POST_WRITE_PROTECTED_UNTRACKED = 130 FILES
POST_WRITE_PROTECTED_MANIFEST
  = 9c46e2112b0c71d0fbfae0282f3bf7ecc7d8ea5f2437a06dfbcee8a7909230e1
PRE_COMMIT_FINAL_FETCH_ORIGIN_MAIN
  = 10efbe0de1d08b512ae765d2c30230b23940f72a
PRE_COMMIT_FINAL_FETCH_DELTA = NONE
SUBAGENT_REPORTED_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILES = TPC_HANDOFF.md + TPC_COMPASS.md
```

## 51. 2026-08-05 source-averaged Mellin、exceptional characters 与 identity-bucket gate

### 51.1 baseline、同一 packet 与 literal target

本节启动时 `HEAD=origin/main=c0743f42bf7e6fd6eed7b7b50ab70b7a7abdda32`，
`TPC_HANDOFF.md` SHA-256 为
`ddeba2f0b502c9fef8291e34c05b54402bb3714e9e8145f5791674cd9de7a849`；
tracked/cached diff均为空。第 1 节 22 项只读启动回归全部通过。127 个 protected
untracked files及其 manifest
`35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f`
原样保留；TPC-27--32 legacy writers与 TPC-122 writer均未执行。

冻结的 theorem-valid selected packet仍为

```text
sigma  = 1/10000
lambda = 99979/210000
delta  = 7/60
beta   = 267/400
h0     = 2

Q  = X^(267/400+o(1))
J  = C = X^(133/400+o(1))
T  = X^(193/500+o(1))
N0 = JQ^2 asymp XQ
H_cp = Q/J^2 = X^(1/400+o(1)).
```

本节不更换第 50.6 节的 coefficient。left side仍为

```text
V_(L,C,ne,far)
 = sum_(gamma,j) sum_(alpha_1!=alpha_2; far)
     gamma_(alpha_1)^(1) conjugate(gamma_(alpha_2)^(1))
     A^act_(alpha_1,gamma)(j) conjugate(A^act_(alpha_2,gamma)(j))
     C_(m_(alpha_1))(j) conjugate(C_(m_(alpha_2))(j))
     product_(i=1)^2 1_(gcd(N_(alpha_i)(j),N_gamma(j))<=C),
```

其中 `far` 明文为
`|m_(alpha_1)-m_(alpha_2)|>Q/J^2`，right side对称，且

```text
C_m(j)=sum_(T<u<=U0; u|mj+2) -mu(u)log u.
```

三条 raw channels、canonical `Delta#`、actual masks/content、outer labels、common
physical `j`、两份 Gram copies及 terminal/proper interference全部保留。目标仍为

```text
|V_(L,C,ne,far)|+|V_(R,C,ne,far)| << X^epsilon Q^3/J.
```

sign-erased scale为 `Q^3J`，所以需要完整 `J^2` collective saving。

### 51.2 source-averaged Mellin：一个真实 marginal L1 与一个未付的 J

取固定 dilate中的 auxiliary prime family `P_X={q:q asymp J}`，并先固定一个在
选择 `q` 前已经完成的、与 `q` 无关的 actual outer source sequence

```text
a_(q,Omega)(chi)=sum_(m asymp Q) A_Omega(m) chi(m).
```

`A_Omega` 保留 literal `mu(d)log ell`、fixed `h0=2`、content source
congruence、actual static/moving masks及 residue/Mellin phases。TPC-22 primitive
multiplicative large sieve合法给出

```text
sum_(q in P_X) sum_(chi!=1) |a_(q,Omega)(chi)|^2
  << X^o (Q+J^2)||A_Omega||_2^2,

Avg_(q in P_X) 1/(q-1) sum_(chi!=1)|a_(q,Omega)(chi)|^2
  << X^o (Q/J^2)||A_Omega||_2^2.
```

这是新的 `PRESENT_DERIVED_L1_SOURCE_AVERAGED_ONLY`。它只控制未加 target
spectral weight的 common source sequence；不能逐 outer cell选择不同的好 `q`，
也不控制 full physical energy。

对一个已经合法 product-ready且 punctured的 target cell，TPC-37的 exact block为

```text
q^2/(q-1)|r_0|^2
 + 1/(q-1) sum_(chi!=1)|a_q(chi)|^2|C_q(chi)|^2.
```

TPC-37只给 target unweighted mean；用 `B` 表示 complementary-weight Mellin
bound，其合法尺度为

```text
1/(q-1) sum_(chi!=1)|C_q(chi)|^2 <= B^2||g||_2^2,
max_(chi!=1)|C_q(chi)|^2 <= (q-1)B^2||g||_2^2.
```

两个同一 `chi` 上的 marginal means不能相乘。source average与 target maximum的
合法组合相对理想 weighted overlap精确多出 `q-1 asymp J`。在 physical ledger中

```text
ideal:     (Q/J^2) * J   * Q^2 = Q^3/J,
available: (Q/J^2) * J^2 * Q^2 = Q^3.
```

故本路线的 first fatal为

```text
ACTUAL_TARGET_WEIGHTED_OUTER_SPECTRAL_OVERLAP
  = NOT_IN_COMMON_SEQUENCE_MULTIPLICATIVE_LARGE_SIEVE_DOMAIN
MISSING_FACTOR = J
```

### 51.3 exceptional-character deletion不收缩 Jacobi bulk

TPC-37 nonprincipal Jacobi matrix `K_(chi,psi)=J(psi,conjugate(chi))`满足

```text
K^*K=KK^*=(q-1)^2 I-q 1 1^*,
```

在 `1^perp` 上 `K/(q-1)` 是酉算子。因而删去 rank-one direction后留下的是
无收缩 bulk。更强地，对任意删除集合 `E`，只要 complement至少二维，就可在
`E^c` 中取 `y perpendicular 1` 并令 `z=(q-1)^(-1)K^*y`；此时 normalized output
恰为 `y`。所以删除固定个数的 output characters后 coefficient-blind operator norm
仍为一。

普通 Landau--Siegel/pretentious exception位于 input twist `psi`。单个 input spike
经 generic Jacobi entries扩散到几乎全部 output `chi`，不是一个可删除的 output
character。prime modulus上也没有 imprimitive conductor bulk可剥离。以上是严格的
method obstruction，不是 actual Möbius coefficient的反例；真正缺失的仍是 actual
source spectrum与 shifted target spectrum在同一 `(q,chi)` 上的 nonconcentration
theorem。

### 51.4 BDH、many auxiliary triples 与 exact ratio bucket

unrestricted identity

```text
sum_(u|N)-mu(u)log u=Lambda(N)
```

不等于 literal `T<u<=U0` coefficient。写成 `Lambda(N)-P_T(N)` 也没有帮助：
低截断 remainder仍处于原 physical scale，且 terminal/proper cross-cancellation不能
由 triangle reassembly倒推。即使反事实把 full ultra修复成 `Lambda`，普通 BDH
仍只控制一个一元 sequence的 centered progression variance，不控制

```text
Avg_q 1/(q-1) sum_chi |a_q(chi)|^2|C_q(chi)|^2
```

中的 common-`j` two-copy covariance、content/moving masks或 outer labels。Harper
`2412.19644v1` 的 general-sequence BDH也明文要求一元 sequence的 progression、
multiples与 interval结构；它不是该 moving ratio operator。

再令 `P={q:KJ<q<2KJ}`，`M` 遍历其中 unordered triples。则

```text
#P = J^(1+o(1)),       #M = J^(3+o(1)),
M = q_1q_2q_3 = J^(3+o(1)) = X^(399/400+o(1)).
```

对 `A(F)=#M^(-1)sum_M 1_(M|F)`，`J^4>X`给出

```text
A(0)=1,
A(F)<=J^(-3+o(1))  (0<|F|<<X),
sum_(0<|F|<<X) A(F)=X^o X/J^3=X^(1/400+o(1)).
```

所以 many-triple average不改善 fixed-triple coherent `ell^1` alias count。非零
triple-alias supports的 disjointness确实给很小的 formal scalar `ell^2` mass；但把
该 scalar gain传入 physical row sum，正是一个新的 target-coupled Hilbert/Bessel
theorem，不能由 character orthogonality自动完成。

根本 fatal发生在 exact equality。TPC-38的正确 phase是 ratio

```text
e_(M,chi)(N,F)=chi(N+F)conjugate(chi(N)).
```

每个 literal ultra atom都有 `su=N`，即 `F=0`。在对应的 `M`-regular support
`(N,M)=1` 上，

```text
e_(M,chi)(N,0)=1
```

对全部 characters成立。对 common-`j` 的两份 Gram copies，即使 `m_1!=m_2`且
属于 far band，在 common regular subfamily上两个 phase仍都为一。all-character
normalized regular family在 identity bucket上恰为一，full primitive regular face为
`1-O(1/J)`；`#M*phi(M)` family dimension与 normalization精确抵消。固定两个
equality atoms后，至多 `X^o` 个 `q asymp J` 除其 targets，故在全部 triples平均后
normalized Gram entry仍为 `1-O(J^(-1+o(1)))`。common regular subframe的 Gram是
all-ones matrix，加入 singular triples后仍是 unsuppressed near-all-ones matrix，
不是近似 identity；singular complement沿用 TPC-37 face closure。small-content
masks只删项，不改变 regular phase。

因此 ordinary large sieve、BDH与 many-modulus averaging都不能在 equality bucket
提供 `J^(-2)`。这只排除 coefficient-blind proof mechanism，不声称 actual coefficient
存在下界。

### 51.5 shifted determinant-fiber primary-source lock

TPC-37的 conditional raw-fiber输入为

```text
||sum_F Z_F[kappa]||_(H_phys)^2
  << X^o Q^2J sup_N sum_F |kappa_N(F)|^2,
```

其 formal ledger `Q^2J*(Q/J^2)=Q^3/J` 正确；但 TPC-38证明 completion只控制
`sum_k Z_(kM)`，不恢复 distinguished raw zero column `Z_0`。all aliases `F=kM`
仍在 ratio `r=1`，所以 nonprincipal Mellin theorem也不推出 raw alias Gram bound。

current-primary有效 theorem screen包括 DFI bilinear Kloosterman fractions、
Bettin--Chandee `1502.00769v1`、Drappeau `1504.05549v4`、Blomer--Harcos
`math/0703246v2`、Heath--Brown delta method与
Fouvry--Kowalski--Michel--Sawin `2511.09459v3`。这些 sources覆盖 scalar
separated Kloosterman-fraction forms、fixed nonzero determinant、smooth quintilinear
dispersion、fixed Hecke shifted convolution、exact delta representation及 nontrivial
gallant trace kernels；均不同时接受：

```text
literal Lambda(ell)mu(d) and two -mu(u)log u copies;
fixed physical h0=2 and common j;
two small-content projectors and far-copy condition;
actual outer masks/labels and full terminal/proper C_m;
F=kM aliases plus raw F=0 recovery;
Hilbert base Q^2J and final normalization Q^3/J.
```

Bettin--Chandee的 determinant application要求 separated/fixed nonzero determinant；
消去 TPC common `j` 后的 shift `2(m_2-m_1)`与 row variables耦合。Drappeau的
hard variables需 smooth product-scale weight。FKMS theorem要求 oscillatory、
geometrically nontrivial bounded-complexity trace kernel；TPC identity bucket的 kernel
为常数一。Heath--Brown delta symbol可以精确检测 `F=0`，但只是 identity，不提供
缺失的 `J^2` cancellation。任何跨 source拼接 coefficient domain与 saving exponent的
做法均不合法。

Dong--Robles--Zeindler `2601.00292v1` 的 claimed improvement不能作为 theorem
input：current `v2` 已撤回，并明文说明遗漏一个 `L^2` factor，原 improved bound不再
成立。本节将其排除，不把 `v1` 的 saving写入任何 physical ledger。

joint-Mellin 与 shifted-fiber在 first fatal处相互独立。前者缺 actual same-character
weighted overlap；后者缺 `r=1` 内 ordinary Hilbert Gram / zero-column recovery。
任一局部 positive theorem都不能自动替另一 parent结算 principal、corrections、
aliases、full reassembly或 global normalization。

### 51.6 verdict 与唯一合法 reopen theorem interfaces

本轮精确状态为

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
SOURCE_Q_AVERAGED_MARGINAL_LARGE_SIEVE = PRESENT_DERIVED_L1_ONLY
ACTUAL_SOURCE_TARGET_WEIGHTED_MELLIN_OVERLAP = ABSENT
WEIGHTED_MELLIN_CURRENT_EXTRA_LOSS = J
FINITE_EXCEPTIONAL_OUTPUT_DELETION_BULK_GAIN = NONE
BDH_LITERAL_ULTRA_ATTACHMENT = FAIL
MANY_AUXILIARY_TRIPLES_IDENTITY_BUCKET_GAIN = NONE
RAW_F0_ZERO_COLUMN_BESSEL_THEOREM = ABSENT
EXISTING_SHIFTED_FIBER_SPECTRAL_THEOREM = ABSENT_IN_SCREENED_FAMILIES

ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
CHI_LE_1_OVER_400 = UNPAID
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

精确裁决为

```text
TPC32_34_37_38_H0_2_20260805_SOURCE_AVERAGED_MELLIN_L1_PRESENT_TARGET_WEIGHTED_
OVERLAP_EXTRA_J_UNPAID_EXCEPTIONAL_DELETION_NO_BULK_GAIN_MULTI_AUXILIARY_MODULUS_
IDENTITY_RATIO_BUCKET_UNSUPPRESSED_RAW_ZERO_COLUMN_BESSEL_THEOREM_ABSENT_NO_TRIGGER_
STOP_SCOPED_PARENTS_OPEN
```

合法 reopen必须直接满足下列二者之一。

1. actual-coefficient joint Mellin theorem：在同一 `(q,chi)` 上控制

   ```text
   Avg_(q asymp J) 1/(q-1) sum_(chi!=1)
     |a_q^act(chi)|^2 |C_(q,full)^act(chi)|^2
     << X^o Q^3/J,
   ```

   并在同一 theorem中保留 full ultra、content、actual masks/outer labels、common
   `j`、two-copy order、both polarizations与 uniform packet constants；principal
   `r_0`、punctured corrections和 singular faces仍须分别闭合。

2. raw alias/zero-column theorem：直接证明 literal small-content far-copy
   `||Z_0^act||^2<<X^oQ^3/J`，或更强地对任意 alias vector证明

   ```text
   ||sum_(|k|<=Q/J^2) a_k Z_k^act||_(H_phys)^2
     << X^o Q^2J sum_k |a_k|^2,
   ```

   其中每个 `Z_k` 保留 actual coefficient、masks、common `j`、content cutoff、
   full terminal/proper layers及 equation `su=N_alpha(j)+kM`。

除此之外，最直接的 reopen仍是第 50.6 节 literal far-copy `Q^3/J` theorem。
ordinary BDH、大筛、finite exceptional deletion、nonidentity trace cancellation、
terminal-only theorem或 scalar alias `ell^2` identity均不是 reopen trigger。

第 6 节全部 method cells继续 `STOP_SCOPED`，尤其 TPC193 V1、common-`k` V1、
tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1。两个 O161 pointwise
parents、TPC32 direct/fixed-`D0`/frame、TPC33 collective、pair-native reroute、
独立 pre-TT-star H1与 global architecture全部保持 `OPEN`。

### 51.7 publication boundary

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志；正式写入只允许
`TPC_HANDOFF.md`。全部 protected untracked files必须原样保留且不得纳入提交。

正式写入后的只读状态为

```text
POST_WRITE_BOOTSTRAP_REGRESSION = 22/22 PASS
POST_WRITE_GIT_DIFF_CHECK = PASS; TPC_HANDOFF.md ONLY
POST_WRITE_EOL = i/lf w/lf
POST_WRITE_MARKDOWN_FENCES = 1514 MARKERS BALANCED
POST_WRITE_NUMBERED_SECTIONS = 51 UNIQUE; DUPLICATES=0
POST_WRITE_PROTECTED_UNTRACKED = 127 FILES
POST_WRITE_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
PRE_COMMIT_FINAL_FETCH_ORIGIN_MAIN
  = b7e70dbff6bc4aad8c25a4fbfff849a416e8c806
PRE_COMMIT_FINAL_FETCH_DELTA = 2 REMOTE NON_TPC COMMITS
PRE_COMMIT_FINAL_FETCH_TPC_HANDOFF_OVERLAP = NONE
SUBAGENT_FILES_CHANGED = 0
RH_SCOPE_USED = NO
LEGACY_TPC27_TO_32_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md_ONLY
```

## 50. 2026-08-04 orbit-energy content split、input-copy near band 与 far-copy off-diagonal gate

### 50.1 冻结基线、执行边界与 literal packet

本轮启动时

```text
HEAD = origin/main
  = fe55988891837a2b2e48f1b6bec4ac98c6ff6c60
TPC_HANDOFF_SHA256
  = fdb24343ac2909a69e613708e77f6b2e2ee7f3f8fe70f750391adc80b4050b40
tracked diff = 0
cached diff = 0
protected untracked files = 127
protected manifest
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
```

`git pull --rebase origin main` 返回 already up to date；第 1 节 22 项只读启动
回归为 `22/22 PASS`。三个 read-only agents分别完成 content/orbit-energy公式审计、
literal theorem-body source lock与 adversarial route audit，均回报
`files_changed=[]`。TPC-27--32 legacy writers、TPC-122 writer、builder与任何
artifact materializer均未执行。

本节只使用第 49 节已经 source-lock 的同一 theorem-valid selected packet：

```text
sigma  = 1/10000
lambda = 99979/210000
delta  = 7/60
beta   = 267/400

Q  = X^(267/400+o(1))
J  = X^(133/400+o(1))
C  = floor(J)
h0 = 2
N0 = J Q^2 asymp X Q.
```

三条 raw channels、canonical `Delta#`、actual row-pair masks、outer labels、
weights、两 polarizations与原 global normalization全部保留。第 22 节
`delta=1/20` 的 `TRUNCATED_ENTRY_ABSENT` family仍是另一条 source lock，不得
拼接。

### 50.2 exact small/large-content orbit slices

沿 TPC-30/34 记

```text
N_alpha(j) = m_alpha j+h0,
c_(alpha,gamma)(j) = gcd(N_alpha(j),N_gamma(j)).
```

对 left polarization定义完全保留 actual multiplier与 ultra increment的两部分

```text
Y^L_(gamma,j,<=C)
  = sum_alpha gamma_alpha^(1) A^act_(alpha,gamma)(j) C_(m_alpha)(j)
      1_(c_(alpha,gamma)(j)<=C),

Y^L_(gamma,j,>C)
  = sum_alpha gamma_alpha^(1) A^act_(alpha,gamma)(j) C_(m_alpha)(j)
      1_(c_(alpha,gamma)(j)>C),

V_(L,<=C) = sum_(gamma,j) |Y^L_(gamma,j,<=C)|^2,
V_(L,>C)  = sum_(gamma,j) |Y^L_(gamma,j,>C)|^2.
```

right polarization交换 `alpha,gamma` 与两 coefficient systems。再令

```text
B^L_(gamma,<=C) = sum_j H_(m_gamma)(j)Y^L_(gamma,j,<=C),
E_(L,<=C)       = sum_gamma |B^L_(gamma,<=C)|^2,
```

并对 `>C` 与 right side同样定义。于是两 content layers分别保留 TPC-34
orbit-to-column transfer；small-content layer另保留 determinant-zero scalar transfer：

```text
E_(L,*)+E_(R,*)
  << X^epsilon J (V_(L,*)+V_(R,*)),

|Z_C| = |A_hat_(C,q)^DFT(0)|
  << sqrt(Q log(2L)) (sqrt(E_(L,<=C))+sqrt(E_(R,<=C)))
  << X^epsilon sqrt(JQ log(2L))
       (sqrt(V_(L,<=C))+sqrt(V_(R,<=C))).
```

第一式的 `*` 可取 `<=C` 或 `>C`，后两式只指 literal small-content `Z_C`。因此

```text
V_(L,<=C)+V_(R,<=C) << X^epsilon Q^3/J
```

仍是同一个 small-content matched-shell auxiliary determinant zero的充分 gate；
没有把 orbit Poisson zero、nonzero-frequency density-one、Parseval或
complete-frequency mean改写为 distinguished zero。

### 50.3 large-content orbit energy无条件闭合

令一般 cutoff `Z>=1`。固定 `(gamma,j)` 后，若
`c_(alpha,gamma)(j)>Z`，则某个 `c|N_gamma(j)`、`c>Z` 满足
`m_alpha=m_gamma (mod c)`。physical row integers互异且位于长度 `O(Q)` 的区间，
故 divisor bound给

```text
# {alpha: c_(alpha,gamma)(j)>Z}
  <= sum_(c|N_gamma(j), c>Z) O(1+Q/c)
  << X^epsilon (1+Q/Z).
```

反向固定不同 rows `(alpha,gamma)`，TPC-30 fixed-row large-content occupancy给

```text
# {j: c_(alpha,gamma)(j)>Z}
  << X^epsilon (1+J/Z).
```

对 inner row sum作 degree Cauchy，使用
`sum_alpha |gamma_alpha^(i)|^2<<Q log(2L)`、`O(Q)` opposite rows以及
TPC-34 pointwise prefix/multiplier envelope，得到新的派生 `L1` theorem

```text
V_(L,>Z)+V_(R,>Z)
  << X^epsilon Q^2(1+Q/Z)(1+J/Z).
```

取 `Z=C=floor(J)`，因 `J<<Q`，即

```text
V_(L,>C)+V_(R,>C) << X^epsilon Q^3/J,
E_(L,>C)+E_(R,>C) << X^epsilon Q^3.
```

第一式组合了 TPC-30 已提交的 occupancy与 TPC-34 orbit slicing；它未在此前
TPC-31--49 正文中单独命名，但不需要新的 arithmetic theorem。第二式只调用
exact Cauchy transfer，仍是 `PRESENT_DERIVED_L1`，不是 `L2`。

### 50.4 full/small gate等价与 growing input-copy near band

逐点有 `Y_all=Y_<=C+Y_>C`。triangle-square inequality双向给

```text
V_all <= 2V_<=C+2V_>C,
V_<=C <= 2V_all+2V_>C,
```

而 `B_all=B_<=C+B_>C` 对 `E` 给同样结论。结合第 50.3 节，目标尺度上

```text
FULL_V_Q3_OVER_J_GATE <=> SMALL_CONTENT_V_Q3_OVER_J_GATE,
FULL_E_Q3_GATE        <=> SMALL_CONTENT_E_Q3_GATE,
```

其中只断言 up to constants/soft losses的 theorem-gate equivalence，不断言两
energies相等。

展开 `V_(L,<=C)` 的两个 input copies `alpha_1,alpha_2`。TPC-34 已证明

```text
V_(L,<=C,Delta)+V_(R,<=C,Delta)
  << X^epsilon Q^2J,

(Q^3/J)/(Q^2J)=Q/J^2=X^(1/400+o(1)).
```

对 off-diagonal再限制

```text
0<|m_(alpha_1)-m_(alpha_2)|<=H_cp.
```

固定一份 input row时另一份 row的 degree为 `O(1+H_cp)`。Schur与 physical
row `ell^2` bound给 weighted input-pair mass
`O(X^epsilon Q(1+H_cp))`；再乘 `O(Q)` opposite rows与 `O(J)` orbit support，
actual masks/content indicators只删项，故

```text
|V_(L,<=C,near)(H_cp)|+|V_(R,<=C,near)(H_cp)|
  << X^epsilon Q^2J(1+H_cp).
```

因此取

```text
H_cp <= floor(Q/J^2)=X^(1/400+o(1))
```

便闭合于 `X^epsilon Q^3/J`。这里比较的是两份 Gram input copies；actual mask
原有的 `|m_alpha-m_gamma|>QX^(-kappa_0)` 比较 input row与 opposite row，两个
difference绝不可混同。该 near-band lemma虽与 TPC-35/36 的 CRT allowance出现
同一数值 `Q/J^2`，但索引与结论不同，是新的窄 `L1` closure，不是新 method paper。

剩余最窄 gate可严格限制为

```text
c_(alpha_i,gamma)(j)<=C,  i=1,2,
|m_(alpha_1)-m_(alpha_2)|>Q/J^2,

|V_(L,<=C,ne,far)|+|V_(R,<=C,ne,far)|
  << X^epsilon Q^3/J.
```

公共物理 `j>0` 时

```text
N_(alpha_1)(j)=N_(alpha_2)(j)
  => (m_(alpha_1)-m_(alpha_2))j=0
  => alpha_1=alpha_2,
```

所以 target-collision 的 literal off-diagonal严格为空。TPC-37 已有 auxiliary
`q`-singular-face bound在 `q asymp J` 达到 `Q^3/J`。不能用 energy monotonicity
直接删除 indicator；但重跑 TPC-37 同一个 absolute degree/Cauchy proof时，额外
small-content indicators只在 proof summands中删项，故同界继续成立，不计为本节
新结果。移除这些 layers后，`c_1=c_2=1`、`q_i` regular、distinct terminal的
far-copy formal eligible cross layer未被现有 identities排除；其 current unsigned
envelope/ceiling为 `X^epsilon Q^3J`，但 literal active nonzero support与 coherent
mass均未证明。

### 50.5 fixed double-content CRT incidence及 aggregate边界

固定两个 exact contents

```text
c_i = gcd(N_(alpha_i)(j),N_gamma(j)),
g   = gcd(c_1,c_2),
ell = lcm(c_1,c_2).
```

exact conditions蕴含

```text
g | m_(alpha_1)-m_(alpha_2),
m_gamma lies in one compatible residue class (mod ell),
j lies in one compatible residue class (mod ell).
```

故该 fixed layer的 termwise absolute incidence mass满足

```text
M_H(c_1,c_2)
  << X^epsilon Q(1+H_cp/g)(1+Q/ell)(1+J/ell),

M(c_1,c_2)
  << X^epsilon Q(1+Q/g)(1+Q/ell)(1+J/ell).
```

这里只用了 exact gcd条件的 necessary congruences；额外 exactness只会删项，且
`g ell=c_1c_2`。每个 physical tuple属于唯一 exact pair，所以没有 hidden
multiplicity；但 fixed-pair saving不等于 aggregate saving。尤其
该 upper bound在 `(c_1,c_2)=(1,1)` 退化为 near-band Schur bound，无 band时
退化为 `Q^3J` unsigned ceiling；这不是 actual饱和或下界。对全部 pairs作
triangle reassembly不能保留单层的 gcd/lcm gain。

还必须区分：exact physical content `c_i=1` 是 coprime event；content-projector
inversion的 principal key `t_i=1` 是 unrestricted full-shell summand。后者的
nonprincipal terms重组为 large-content subtraction，二者不能互换。因此本节只登记

```text
FIXED_DOUBLE_EXACT_CONTENT_CRT_INCIDENCE = PRESENT_DERIVED_L1
AGGREGATE_SMALL_CONTENT_FAR_COPY_SAVING = ABSENT
```

### 50.6 literal theorem target、source refresh与裁决

left side未闭合 coefficient逐字为

```text
V_(L,C,ne,far)
 = sum_(gamma,j) sum_(alpha_1!=alpha_2; far)
     gamma_(alpha_1)^(1) conjugate(gamma_(alpha_2)^(1))
     A^act_(alpha_1,gamma)(j) conjugate(A^act_(alpha_2,gamma)(j))
     C_(m_(alpha_1))(j) conjugate(C_(m_(alpha_2))(j))
     product_(i=1)^2 1_(gcd(N_(alpha_i)(j),N_gamma(j))<=C),
```

right side对称。所需 bound为 `X^epsilon Q^3/J`；absolute orbit-sliced scale
`Q^3J`，故必须支付完整 `J^2` collective saving。terminal--terminal展开含四个
Möbius factors；完整 `C_m` 还含 terminal/proper与 proper/proper layers，naked
terminal theorem不能控制原 operator。

2026-08-04 current-primary theorem-body refresh审查了 Tao
`1509.05422v4`、Matomäki--Radziwiłł--Tao `1503.05121v3`、Menon
`2607.15574v1`、Tao--Teräväinen `2512.01739v2` 与 `2107.02158v4`、
Jaskari--Sachpazis `2409.10663v3`、Leng `2212.09635v3`、
Klurman--Mangerel `1708.03176v1`、Lichtman--Teräväinen `2111.08912v3`、
Higher Uniformity II `2411.05770v2`、Kim `2603.23250v2`、
Klurman--Mangerel--Teräväinen `2304.05344v2`、Grimmelt--Teräväinen
`2607.28091v1` 与 Ramaré--Zúñiga Alterman `2603.25961v3`。

全部 first fatal发生在 literal theorem domain/range：fixed或 polylog coefficients、
average independent shifts、logarithmic average、metric/subsequence、global
additive cube/nilsequence、conditional hypothesis、错误 arity/operator，或不接受
two-copy content masks与 full ultra increments。即使反事实移除 object fatal，现有
logarithmic savings也不能支付 `J^2`。这是有限 source lock，不是文献全局
nonexistence claim；sharper cutoff只收紧 TPC-34/第 6 节既有 source cells，没有
产生新 source/version cell。

本轮精确状态为

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
LARGE_CONTENT_ORBIT_V_Q3_OVER_J = PRESENT_DERIVED_L1
LARGE_CONTENT_COLUMN_E_Q3 = PRESENT_DERIVED_L1
FULL_SMALL_V_E_GATE_EQUIVALENCE = PRESENT_DERIVED_L1
INPUT_COPY_NEAR_BAND_H_LE_Q_OVER_J2 = PRESENT_DERIVED_L1_CLOSED
FIXED_DOUBLE_EXACT_CONTENT_CRT_INCIDENCE = PRESENT_DERIVED_L1

SMALL_CONTENT_FAR_COPY_OFF_V_Q3_OVER_J_THEOREM = ABSENT
TARGET_COLLISION_OFF_DIAGONAL = EMPTY
Q_SINGULAR_FACE = PRESENT_L1_INHERITED_TPC37
FULLY_COPRIME_FAR_COPY_Q_REGULAR_DISTINCT_TERMINAL_LAYER = OPEN
DIRECT_SMALL_CONTENT_ZERO_BOUND = ABSENT
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
CHI_LE_1_OVER_400 = UNPAID
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

精确裁决为

```text
TPC32_34_H0_2_20260804_LARGE_CONTENT_ORBIT_ENERGY_AND_INPUT_COPY_Q_OVER_J2_
NEAR_BAND_CLOSED_DERIVED_L1_SMALL_FULL_V_E_EQUIVALENT_FULLY_COPRIME_FAR_COPY_
REGULAR_DISTINCT_TERMINAL_FOUR_MOBIUS_Q3_OVER_J_THEOREM_ABSENT_NO_TRIGGER_
STOP_SCOPED_PARENTS_OPEN
```

本节不新造 arithmetic method cell或 source cell；它只把两个派生 closures与一个
fixed-layer incidence登记进既有 selected-packet/TPC-34 cell。第 6 节全部旧
method cells保持 `STOP_SCOPED`，尤其 TPC193 V1、common-`k` V1、
tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1。两个 O161 pointwise
parents、TPC32 direct/fixed-`D0`/frame、TPC33 collective、pair-native reroute、
独立 pre-TT-star H1与 global architecture全部保持 `OPEN`。

合法 reopen条件为：直接对上式 literal small-content far-copy coefficient证明
`Q^3/J`；或直接证明同一 `Z_C<<X^(o(1))Q^2`；或给出保留 full ultra layers、
actual masks/content与全部 ranges/normalization的 coefficientwise等价 collective
theorem。任何 local positive result仍不自动创建 TPC-207；all-`D` uniformity、
exactly-once physical cover、original/global normalization、tail-failure、A/B
selection、actual packet attachment、production occurrence、完整 provenance与
strict physical-loss ledger仍须分别通过。

### 50.7 publication boundary

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志；正式写入只允许
`TPC_HANDOFF.md`。全部 protected untracked files必须原样保留且不得纳入提交。

正式写入后的只读状态为

```text
POST_WRITE_BOOTSTRAP_REGRESSION = 22/22 PASS
POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_GIT_DIFF_CHECK = PASS; TPC_HANDOFF.md ONLY
POST_WRITE_EOL = i/lf w/lf
POST_WRITE_MARKDOWN_FENCES = 1468 MARKERS BALANCED
POST_WRITE_NUMBERED_SECTIONS = 50 UNIQUE; DUPLICATES=0
POST_WRITE_PROTECTED_UNTRACKED = 127 FILES
POST_WRITE_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
PRE_COMMIT_FINAL_FETCH_ORIGIN_MAIN
  = fe55988891837a2b2e48f1b6bec4ac98c6ff6c60
PRE_COMMIT_FINAL_FETCH_DELTA = 0
PRE_COMMIT_FINAL_FETCH_TPC_EDGE = NONE
SUBAGENT_FILES_CHANGED = 0
LEGACY_TPC27_TO_32_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md_ONLY
```

## 49. 2026-08-04 content-mask signed allocation、safe BV envelope 与 collective-return gate

### 49.1 冻结基线、执行边界与 selected packet

本轮启动时

```text
HEAD = origin/main
  = ca9fe7ab11c82a8dfb272c63b2f7940717282704
TPC_HANDOFF_SHA256
  = 9567009e27e779198875496a56bd8057d233568f5d06f908d7583d2313bb9b0b
tracked diff = 0
cached diff = 0
protected untracked files = 127
protected manifest
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
```

`git pull --rebase origin main` 返回 already up to date；第 1 节 22 项只读启动
回归为 `22/22 PASS`。三个 read-only agents 分别完成 content/BV proof audit、
current-primary theorem-body source lock 与全部 OPEN parents route ranking，均回报
`files_changed=[]`。TPC-27--32 legacy writers、TPC-122 writer、builder与任何
artifact materializer均未执行。

本节继续锁定第 48 节同一个 theorem-valid selected packet：

```text
sigma  = 1/10000
lambda = 99979/210000
delta  = 7/60
beta   = 267/400

Q  = X^(267/400+o(1))
J  = X^(133/400+o(1))
C  = floor(J)
h0 = 2
N0 = J Q^2 asymp X Q.
```

第 22 节 `delta=1/20` 的 `TRUNCATED_ENTRY_ABSENT` family没有重开，且绝不与
本 packet拼接。三条 raw channels、canonical `Delta#`、actual row-pair mask、
outer labels、weights与原 global normalization均沿第 48 节 source lock保留。

### 49.2 content不是 affine-pair gcd；exact progression不删除 masks

TPC-93 actual affine child满足

```text
D_theta(t) = d_theta + sigma_theta t,
U_theta(t) = u_theta + a_theta t,
sigma_theta u_theta-a_theta d_theta = h0 = 2,

P_theta = n_theta j_theta+h0,
G_theta(t) = gcd(sigma_theta U_theta(t),P_theta).
```

因此 `gcd(D_theta(t),U_theta(t))|2` 不使 `G_theta(t)<=C` 自动成立；两个 gcd
是不同对象。把 primitive affine-pair gcd改名为 target content会改变 literal
coefficient，故 fail closed。

TPC-93 的 exact content inversion为

```text
1_(G_theta(t)<=C)
 = sum_(1<=c<=C) sum_(kappa>=1)
     mu(kappa)
     1_(c kappa | P_theta)
     1_(c kappa | sigma_theta U_theta(t)).
```

这里 `c` 是 candidate exact content，`kappa` 是 signed inversion key，二者不得
合并。令

```text
b = c kappa,
g = gcd(b,sigma_theta),
B = b/g.
```

则 `b|sigma_theta U_theta(t)` 等价于 `B|U_theta(t)`；soluble branch恰是一条
positive-step progression

```text
t = tau_(theta,b)+Bz.
```

写

```text
U_theta(tau+Bz) = B V_(theta,b)(z),
D*_(theta,b)(z) = D_theta(tau+Bz),
```

则非 squarefree `B` branch为零，其余 branch精确给出

```text
mu(U_theta(tau+Bz))
  = mu(B) mu(V_(theta,b)(z)) 1_(gcd(B,V_(theta,b)(z))=1),

det(D*_(theta,b),V_(theta,b)) = h0 = 2.
```

所以 exact content-resolved scalar可写为

```text
Z_C = sum_f C_f sum_(z in I_f) s_f(z) W_f(z),

f = (theta,c,kappa,tau),
1 <= c <= C,
b = c kappa | P_theta,
gcd(a_theta,B) = 1,
I_f nonempty,
tau = tau_(theta,b) mod B,
C_f = c_theta,X mu(kappa)mu(B) 1_(c kappa|P_theta),
s_f(z)
  = mu(D*_f(z))mu(V_f(z))
    1_(gcd(B,V_f(z))=1) chi_theta(tau+Bz),
W_f(z) = W_theta,X(tau+Bz).
```

positive `B`保持 within-progression order，但它把 original prefix family改为
progression-prefix family，并且只会缩短 fiber。`mu(B)`、新 coprimality mask、
`chi_theta`、content keys、polarization与 source--child provenance任何一项都不得
删除。将任意 periodic/local mask再强行分成 residue progressions通常把 unreduced
determinant改为 modulus乘 `h0`；没有 forced factor时不得静默仍标 `h0=2`。

对 fixed `P_theta asymp X`，content branch的 absolute multiplicity满足

```text
sum_(c,kappa: c kappa|P_theta) |mu(kappa)|
  <= sum_(b|P_theta) tau(b)
  = tau_3(P_theta)
  = X^(o(1)).
```

这证明 exact progression不会单独引入 fixed-power branch loss；它没有证明新的
Möbius cancellation。

### 49.3 mask-in-sign factor allocation 与 source-backed safe envelope

对原始 ordered `t` fibers，最强 metadata-safe factor allocation是

```text
a_theta(t)
  = mu(D_theta(t))mu(U_theta(t))
    chi_theta(t) 1_(G_theta(t)<=C),

w_theta(t)
  = c_theta,X W_theta,X(t),

Z_C = sum_theta sum_(t in I_theta) a_theta(t)w_theta(t),
E_cont,X = 0.
```

`a_theta`保留 `chi_theta` 中的 fixed-period/local-coprimality factors与 content
cutoff；其余 actual row-pair mask components继续按既有 decomposition保留在
`theta`、`I_theta` 与 `c_theta,X` 中。它是 bounded complex signed sequence。
TPC-111/122 的 finite Abel identity对 complex
sequences成立。TPC-122也明确规定：rough factor在 sign与weight之间移动会改变
theorem gate，必须预先登记。故本 allocation可以无损调用 finite duality，但未来
定理必须估计上式 exact masked prefixes

```text
Delta_theta
  = max_(k<=|I_theta|)
      |sum_(i<=k) a_theta(t_i)|,
```

不能调用只估计 unmasked `mu(D)mu(U)` 的 theorem。

这个 allocation把所有 content jumps移出 BV weight。TPC-32/33 已提交的界为：

1. 两侧 physical row coefficient各有 `ell^1` mass `O(Q)`；
2. joint orbit/target support为 `O(J)`；
3. raw divisor prefixes、row-gcd projector与 local-mask divisor mass均为
   `X^(o(1))`；
4. `W_theta,X` 的 logarithmic/smooth/Mellin-BV seminorm为 `X^(o(1))`；
5. 每个 affine key至多两个 interval components。

取 literal comparison scale

```text
A_theta = |I_theta|,
```

逐 source atom用 TPC-93 projector-weighted child reassembly，并对 above finite
expansions取 absolute mass，得到 source-backed derived envelope

```text
sum_theta A_theta ||c_theta,X W_theta,X||_BV*
  << X^(o(1)) J Q^2
  = X^(133/400+o(1)) Q^2.
```

因此本 allocation的精确字段是

```text
CONTENT_AND_CHI_MASKS_IN_SIGN = PRESENT_L1
REMAINING_ACTUAL_MASKS_IN_THETA_I_C = PRESENT_L1
SMOOTH_WEIGHT_ONLY_BV = PRESENT_L1
SAFE_CONTENT_AWARE_OUTER_BV_ENVELOPE = PRESENT_DERIVED_L1
ell_Z = 133/400
E_cont,X = 0
SCALAR_GLOBAL_NORMALIZATION = PRESERVED
```

该 inequality由 committed bounds逐项派生，虽不是既有论文中单独命名的 theorem，
但不需要新的 arithmetic input。故第 48.5 节 allocation-independent 的
`ACTUAL_OUTER_BV_ENVELOPE=ABSENT` 由本节 supersede。若仍把 cutoff留在旧 weight，
则每个 entering/leaving transition都在 endpoint-anchored variation中收费；粗界只有
`||v 1_(G<=C)||_BV*<=2 sum|v|`，不得把本 allocation的 envelope跨 gate搬回旧
unmasked prefix对象。

### 49.4 fiberwise absolute-reassembly 的精确 strategy ceiling

TPC-33 selected scale给

```text
|I_theta| <= 1 + D/(sigma_theta v_theta),
D = X^(d_*+o(1)),
d_* = 10049/52500 = 40196/210000.
```

exact content progression进一步除以 `B`，不会产生更长 fiber。natural envelope
exponent为

```text
ell_Z = 133/400 = 69825/210000.
```

在指定策略“每条 fiber用 signed-prefix/BV，再对全部 outer keys取绝对值”内，
即使每条 active nonzero unit-scale signed sequence有理想 `O(1)` prefix
discrepancy，可见的
最大 relative fiber saving也只有 `D^(-1)`。因此

```text
delta_pre-ell_Z
  <= 10049/52500 - 133/400
  = -29629/210000
  < 0.
```

active singleton fiber更只能给 classwise `delta=0`；除非另有 exact enumeration、
physical counting或 collective return，不能称其 negligible。把 comparison scale
统一乘 `X^a` 只会同时作

```text
delta_pre -> delta_pre+a,
ell_Z     -> ell_Z+a,
```

所以净差不变。square-root prefix更只给 `d_*/2`，留下第 33 节已记录的
`49727/210000` gap。

这只是上述 fiberwise/absolute-reassembly certificate的 rigorous ceiling，不是
`Z_C` actual value的下界，也不是所有未来方法的 nonexistence theorem。TPC-111
明确允许 future proof使用 outer cancellation。当前最窄且不重复的 collective
OPEN target仍是 TPC-33 已命名的

```text
E_L+E_R <<_(epsilon,h,mathscr D) X^epsilon Q^3.
```

其 committed transfer在同一 selected packet上给

```text
|S_sh^all| <= X^epsilon Q^2,
|Z_C|      <= X^epsilon Q^2
```

（第二式再用既有 large-content splice），并保留两 polarizations、actual mask、
fixed `h0=2`、`+1` sparse occupancy与原 normalization。该 `Q^3` estimate本身仍
`ABSENT_L2`。直接证明同一 literal `Z_C` bound也是合法并列入口。

### 49.5 current-primary theorem-body source lock

2026-08-04 official arXiv `math.NT` new/cross-list/replacement listing及组合检索没有
新增 literal survivor。逐 theorem body的最接近结果为：

| source/version | strongest legitimate nearby statement | first fatal |
|---|---|---|
| Tao `1509.05422v4`, Corollary 1.5 | fixed `d,u,s,a` 可逐字取 `mu(d+st)mu(u+at)` 且 `su-ad=2` | `1/n` logarithmic terminal average，不是 natural every-prefix；无 growing coefficients/fixed power/outer ledger |
| Grimmelt--Teräväinen `2607.28091v1`, Theorem 1.3 | growing coefficient-box collective inverse theorem | source operator为 shared-origin `x+b_i m` counting/inverse object；不含 actual independent origins、determinant-two constraint、outer keys、masks/weights或 signed `Z_C` upper bound |
| Frantzikinakis `1606.08420v2`, Theorem 2.1 | fixed multiplicative functions/polynomials 的 natural inner correlations，沿 selected subsequence在 outer shift上 uniform-density趋零 | fixed slopes、subsequence与 metric outer average；无 finite-`X` uniform power或 prescribed actual family |
| Lichtman `2009.08969v2`, Theorems 1.1/1.3 | growing equal-slope shift boxes的 natural shift-averaged correlations，带 logarithmic/`psi` savings | averaged/almost-all shifts与 equal slopes，不能提升为 prescribed growing determinant-two family；saving rate也不支付 required fixed power |
| Chinis `2105.14653v1`, Theorem 1.2 | Siegel-zero sequence假设下，对 fixed distinct unit-slope shifts在一段 growing `x` window逐 `x` uniform 的 natural Liouville correlation | unavailable conditional sequence与 fixed unit-slope family；无 actual growing slopes/origins、masked outer family、BV/content或 physical-loss ledger |
| Klurman--Mangerel `1708.03176v1`, Proposition 1.6 | fixed-height primitive multidimensional affine system的 natural box average | constant依赖 fixed height；让 slopes增长后 actual forms对 `(s,t)` 为 bilinear，非 source affine system |

Tao source的 correct literal affine syntax不得与其他 source的 natural/collective
normalization拼接；metric、averaged shift、subsequence、conditional与 inverse theorem
均不得升级为 prescribed actual family。有限 scan的精确字段为

```text
POINTWISE_EXACT_MASKED_ALL_PREFIX_CANDIDATE = NONE_VERIFIED
COLLECTIVE_ACTUAL_OUTER_FAMILY_CANDIDATE = NONE_VERIFIED
DIRECT_SMALL_CONTENT_ZERO_CANDIDATE = NONE_VERIFIED
PASS_CANDIDATE = 0
```

这不是全局文献不存在性命题。第 6 节新 source-specific cell只冻结上述 versions
向本 gate的非法 transfer，不关闭 future literal theorem。

### 49.6 精确裁决、STOP scope 与合法 reopen

本轮状态为：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
THREE_RAW_CHANNELS_CONTENT_DELTA_SHARP_N0_LOCK = PASS
LOSSLESS_SCALAR_COMMON_NATIVE_REFINEMENT = PRESENT_L1

CONTENT_IS_GCD_D_U_OR_AUTOMATIC_FROM_H0_2 = FALSE
EXACT_CONTENT_PROGRESSION_AND_DETERMINANT_RESTORATION = PRESENT_L1
CONTENT_AND_CHI_MASKS_IN_EXACT_SIGNED_SEQUENCE = PRESENT_L1
REMAINING_ACTUAL_MASKS_IN_THETA_I_C = PRESENT_L1
SAFE_CONTENT_AWARE_OUTER_BV_ENVELOPE = PRESENT_DERIVED_L1
ell_Z = 133/400

EXACT_MASKED_GROWING_ALL_PREFIX_THEOREM = ABSENT
FIBERWISE_PREFIX_PLUS_ABSOLUTE_OUTER_ENDPOINT = FAIL_SCOPED
FIBERWISE_ENDPOINT_DEFICIT = 29629/210000
SINGLETON_RETURN_THEOREM = ABSENT
TPC33_COLLECTIVE_Q3_ENERGY_THEOREM = ABSENT
DIRECT_SMALL_CONTENT_ZERO_BOUND = ABSENT

ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
CHI_LE_1_OVER_400 = UNPAID
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

精确裁决为：

```text
TPC32_H0_2_20260804_CONTENT_MASK_IN_SIGN_SAFE_BV_ENVELOPE_ELL_Z_133_400_
PRESENT_L1_FIBERWISE_PREFIX_ABSOLUTE_OUTER_DEFICIT_29629_210000_
COLLECTIVE_Q3_OR_DIRECT_ZERO_REQUIRED_NO_TRIGGER_STOP_SCOPED_PARENTS_OPEN
```

本节不新造 arithmetic method cell；它修正既有 selected-packet cell的 factor
allocation/envelope字段，并新增一个严格 source/version-specific wrong-transfer
cell。第 6 节全部旧 method cells继续 `STOP_SCOPED`，尤其 TPC193 V1、common-`k`
V1、tail-failure/A/B V1 与 full-`r_Rr_R` ultra-complement V1。两个 O161
pointwise parents、TPC32 direct/fixed-`D0`/frame、TPC-33 collective Q3、
pair-native reroute、独立 pre-TT-star H1 与 global architecture全部保持 `OPEN`。

只在以下任一 source-backed状态真实变化时重开本 route：

1. 直接对同一 selected packet、three raw channels、`G<=C`、actual masks/weights/
   outer labels与原 global normalization证明 `|Z_C|<=X^(o(1))Q^2` 或更强；
2. 证明 TPC-33 actual `E_L+E_R<<X^epsilon Q^3` collective energy gate，或一个
   coefficientwise等价、保留全部 metadata的 collective outer-return theorem；
3. 对第 49.3 节 exact masked sequences给 growing all-prefix theorem，并另给
   singleton/classwise return与 outer cancellation，使 actual classwise
   `delta-ell>=0`；只有加强单 fiber theorem而不返回 outer deficit不够；
4. 若目标改为完整 dictionary，再 materialize actual archive并证明
   `(J Q_D-Q_Z)M=0`；这仍不是 scalar route的前置门。

任一 local positive result仍不自动创建 TPC-207。all-`D` uniformity、
exactly-once physical cover、original/global normalization、tail-failure、A/B
selection、actual packet attachment、production occurrence、完整 provenance与
strict physical-loss ledger必须分别通过，并使页首 trigger发生真实
theorem-backed状态变化。

### 49.7 publication boundary

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志；正式写入只允许
`TPC_HANDOFF.md`。全部 protected untracked files必须原样保留且不得纳入提交。

```text
POST_WRITE_BOOTSTRAP_REGRESSION = 22/22 PASS
POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_GIT_DIFF_CHECK = PASS; TPC_HANDOFF.md ONLY
POST_WRITE_EOL = i/lf w/lf
POST_WRITE_MARKDOWN_FENCES = 1410 MARKERS BALANCED
POST_WRITE_NUMBERED_SECTIONS = 49 UNIQUE; DUPLICATES=0
POST_WRITE_PROTECTED_UNTRACKED = 127 FILES
POST_WRITE_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
PRE_COMMIT_FINAL_FETCH_ORIGIN_MAIN
  = 33c9ec6fd7baf7c983de2b0fecc8b959ba0237c1
PRE_COMMIT_FINAL_FETCH_DELTA = RH_HANDOFF.md ONLY
PRE_COMMIT_FINAL_FETCH_TPC_EDGE = NONE
POST_COMMIT_REBASE_ORIGIN_MAIN
  = c46d4acd9a3b74bb87a3dedab3a93b7c99067188
POST_COMMIT_REBASE_ADDITIONAL_DELTA = RH_HANDOFF.md ONLY
POST_COMMIT_REBASE_TPC_EDGE = NONE
SUBAGENT_FILES_CHANGED = 0
LEGACY_TPC27_TO_32_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md_ONLY
```

## 48. 2026-08-04 TPC-93 scalar zero-mode common refinement 与 current-version signed-prefix source 审计

### 48.1 冻结基线、selected packet 与 scalar target

本轮启动时 `HEAD=origin/main` 为
`ace004df0b39f62b4de747656932fd316acdfbe9`；
`git pull --rebase origin main` 返回 already up to date。启动
`TPC_HANDOFF.md` SHA-256 为
`e62e397dda09ae6b6f608972ce0d5eb4968dae5c35f4d406a7c77a464c059d99`。
tracked/cached diff 均为空；127 个 protected untracked files 的 manifest 为

```text
35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
```

第 1 节 22 项只读启动回归为 `22/22 PASS`。三个 read-only agents 分别审核
scalar proof、current primary source/version 与其余 OPEN parents，
`files_changed=[]`；TPC-27--32 legacy writers、TPC-122 writer 与任何 builder
均未执行。

本节只重审同一 theorem-valid TPC-28/32 selected packet：

```text
sigma  = 1/10000
lambda = 99979/210000
delta  = 7/60
beta   = 267/400

Q  = X^(267/400+o(1))
J  = X^(133/400+o(1))
C  = floor(J)
h0 = 2
N0 = J Q^2 asymp X Q.
```

它与第 22 节 `delta=1/20` 的 `TRUNCATED_ENTRY_ABSENT` family 分离，
不得拼接。TPC-32 的 complete matched shell保留三个 raw channels

```text
A_m,T C_n,
C_m A_n,T,
C_m C_n,
```

等价地

```text
K_sh = A_m,U0 A_n,U0 - A_m,T A_n,T
     = C_m H_n + H_m C_n.
```

对原始 off-diagonal base atom `omega_0=(alpha,gamma,j)`，令

```text
G_omega_0      = gcd(m_alpha j+2,m_gamma j+2),
Delta#_omega_0 = (m_alpha-m_gamma)/G_omega_0.
```

记

```text
a^sh_omega_0 := mathfrak a^sh_(alpha,gamma,j),
```

即 TPC-32 已定义的 complete signed physical summand；它包含两条 opened-row
coefficients、actual row-pair mask、fixed-period/smooth factors与完整 `K_sh`。

同一 small-content distinguished zero 是

```text
Z_C := A_hat_C,q_DFT(0)
     = sum_n A_C(n)
     = sum_omega_0 a^sh_omega_0 1_(G_omega_0<=C).
```

`q_DFT asymp Q` 只提供 no-wrap DFT；`r=0` 的 scalar 与 modulus选择无关。

### 48.2 TPC-93 已供应的 lossless scalar common-native refinement

TPC-93 的 decorated-reindexing lemma 对附着在每个原始 physical atom上的
任意 finite scalar decoration成立。打开 polarization与 ultra divisor后写

```text
omega_tilde = (L/R,alpha,gamma,j,u),
G_omega_tilde := G_omega_0.
```

其 source--child theorem给出显式双向 provenance map：每个
`(omega_tilde,row-gcd projector layer v)` 有唯一 child `(theta,t)`；反向 map
恢复 polarization、两行、opposite row、
`j` 与 ultra divisor。projector-weighted multiplicity和 Möbius sign逐项重组
原始 coefficient，左右两个 polarizations各出现一次，全部 masks/weights及
一个 global normalization 均保留。

因此在该 theorem中直接取

```text
F(omega_tilde) = 1_(G_omega_0<=C)
```

得到严格的 selected-packet scalar corollary

```text
Z_C
 = sum_(theta in Theta_X) c_theta,X
     sum_(t in I_theta)
       mu(D_theta(t)) mu(U_theta(t))
       chi_theta(t) W_theta,X(t) 1_(G_theta(t)<=C),

D_theta(t) = d_theta + s_theta^aff t,
U_theta(t) = u_theta + a_theta t,
s_theta^aff u_theta-a_theta d_theta = h0 = 2.
```

这是同一个 literal coefficient的 exact `L1` attachment，不是只在一个
chosen vector上偶合：lemma逐 source atom且逐任意 decoration成立，child-to-source
inverse显式可逆。ledger保留 `G_theta(t)`、`M_theta(t)`、opposite row、
`j_theta` 与 orientation，因此可恢复

```text
Delta#_theta(t)
  = epsilon_theta (M_theta(t)-n_theta)/G_theta(t).
```

`I_theta` 是 literal integer interval；按 `t_1<...<t_m` 的顺序就是
TPC-111/122所需 canonical translated-integer order。若继续作 exact-content
progression `t=tau+Bz`，其 positive step `B` 也保持顺序。并且在
`D_theta(t),U_theta(t)` 为 positive physical integers 的 support上逐点有

```text
mu(D) mu(U)
  = mu^2(D) mu^2(U) lambda(D) lambda(U),
```

正是 TPC-111 的 signed sequence。

TPC-124 的完整 dictionary test

```text
(J Q_D-Q_Z) M = 0
```

仍未由 actual growing archive执行或证明；所以不得声称完整 determinant-bin
dictionary 与全部 ordered-fiber dictionary 已经 intertwine。但这个 full `J`
是完整字典同一性的测试，不是计算单个 distinguished scalar的必要条件。
scalar只需在 common native source basis上保持 total evaluator；TPC-93的
逐 source--projector-layer 双射及 projector-weighted coefficient reassembly
正好供应该窄 scalar 条件。故第 23.2 节以 full `J` 缺失阻断 scalar
transfer 的判断过强，同时 full-dictionary 缺口本身仍真实存在。

### 48.3 TPC-111/122 的 exact factor allocation、BV gate 与 natural scale

在保留全部 `theta` 时，可作以下无损 factor allocation：

```text
epsilon_theta^Mob(t) = mu(D_theta(t)) mu(U_theta(t)),
w_theta(t)
  = c_theta,X chi_theta(t) W_theta,X(t) 1_(G_theta(t)<=C),
E_cont,X = 0.
```

这里 `E_cont,X=0` 不是免费删除 content：`G<=C` 的每个真实跳变全部留在
`w_theta`，必须计入 endpoint-anchored variation

```text
||w_theta||_BV*
  = |w_theta(t_m)|
    + sum_(i<m) |w_theta(t_i)-w_theta(t_(i+1))|.
```

TPC-111 的 finite Abel identity因此可以无损调用。真正未证的 growing inputs为

```text
Delta_theta
  := max_(k<=m) |sum_(i<=k) epsilon_theta^Mob(t_i)|
  <= X^(-delta_pre+o(1)) A_theta

sum_theta A_theta ||w_theta||_BV*
  <= X^(ell_Z+o(1)) Q^2,
```

这里 `A_theta>=0` 是预先声明的 literal comparison scale，
`delta_pre,ell_Z>=0`；全部 `o(1)`、implied constants、factor allocation与
quantifier ranges必须对同一 declared actual-fiber family统一。

其中必须是全部 actual selected-packet fibers、同一 fixed `h0=2`、同一 literal
order/factor allocation、共同 parameter ranges 与 uniform constants。TPC-122
只在这些 hypotheses成立且 `delta_pre>=ell_Z` 时推出

```text
|Z_C| <= X^(-(delta_pre-ell_Z)+o(1)) Q^2.
```

selected packet 上的 normalization没有额外 renormalization：TPC-93已证明
original global coefficient被重组，而

```text
Q^2 = N0/J = N0 X^(-133/400+o(1)).
```

所以若上述 actual prefix与BV theorem真实给出 `delta_pre>=ell_Z`，则

```text
|Z_C| <= N0 X^(-133/400+o(1)).
```

这到达 `133/400` endpoint的 strict-margin form，因而对每个固定
`sigma_save<133/400` 给出 small-content fixed-power saving；再用 TPC-32 的
large-content splice，完整 matched shell同样得到每个严格
`sigma_save<133/400` 的 saving，不声称无 `o(1)` 的 endpoint equality。这个
direct zero-bound route不需要先下界 flatness denominator。

若目标改为证明 `F0(A_C)<=X^(1/400+o(1))`，则仍须另给同一 actual
coefficient的 determinant-energy lower bound，并满足 TPC-112 compatibility：

```text
D_X >= X^(-lambda_D+o(1)) Q^3 J^2,
lambda_D <= 2 eta_Z,
eta_Z = delta_pre-ell_Z.
```

TPC-32 当前只有 energy upper bound，所以不能把 positive `eta_Z` 字段改名为
`chi<=1/400`。当前第一 arithmetic fatal精确移动为 growing deterministic
two-affine Möbius prefix theorem与 actual outer BV envelope同时缺失。

### 48.4 Angelo--Xu v3 与其余 current route delta

official arXiv version history确认 Angelo--Xu
`arXiv:2411.14447v3` 于 2026-08-02 修订。v3保留两条 theorem statements：

1. conditional `f(p)=1` for `p<=y` 的 random completely multiplicative
   Rademacher function，在 `y=o((log x/loglog x)^2)` 时，全部 partial sums
   到 `x` 非负的概率为 `o(1)`；
2. random weighted sums `sum f(n)/sqrt(n)` almost surely infinitely often
   change sign。

v3 对 `t_i` scale、multidimensional Berry--Esseen/Lyapunov步骤、transition
second moment与末段积分不等式作了实质修复。新增 Remark 3.2证明
deterministic `sum_(n<=x) lambda(n)/sqrt(n)` 不可能最终恒正，但明确不排除
最终恒负。v2到v3的 proof修复必须承认，然而 theorem-object gate仍先失败：

```text
RANDOM_SINGLE_COMPLETELY_MULTIPLICATIVE_RADEMACHER_COEFFICIENT
  !=
ACTUAL_DETERMINISTIC_TWO_AFFINE_H0_2_MOBIUS_COEFFICIENT.
```

deterministic remark也只有 single Liouville factor、`n^(-1/2)` weight与
natural-integer terminal sign，不给 two affine forms、actual packet、three raw
channels、content/`Delta#`、outer labels、canonical fiber all-prefix magnitude、
`Q/J/N0` range、uniform constants或 physical-loss ledger。因此该 source没有
growing prefix/BV theorem、direct `Z_C` bound、O161 pointwise theorem或
`1/400` payment。

其余 read-only refresh未发现第 46/47 节之后的新 route edge：两个 O161
pointwise parents的首缺仍是 named production atom / literal same-record theorem；
actual-cloud frame仍缺 source-backed separation或 signed local multiplicity及
moving full/cross-`D0` Gram；TPC-206仍为 selected `13/42`，首缺 uppercase
opened `D`，pair-to-`omega`与 linear H1 occurrence edge仍缺。

发布前只读 fetch又确认一个完全 disjoint 的 late remote delta：
`ace004df0b39f62b4de747656932fd316acdfbe9..`
`1b3513ffde611b26f050fac02006b82c3799021a` 的三个 commits
`99026999bb13c91bea9d5239cdf2ca5a8a5e2885`、
`94951c3f3408cfd2032537a1cb1f29288cb7d164`、
`1b3513ffde611b26f050fac02006b82c3799021a` 只修改 `RH_HANDOFF.md`。
RH completed endpoint仍为 RH-361，RH-362没有 paper/artifact且未创建；其
source lock与独立 adversarial audit均为 `NOT_TESTABLE`。当前 route coordinate
是 `actual_same_clock_unnormalized_head_transport_open`，首个 physical leaf仍为

```text
D_(4k)(R)
  = sum_(2<=n<4k) |h_(sigma,n)-s_(k,n)| R^n/n -> 0.
```

RH-361 的 `d=e,q=p+e,h=s+e` 只给 fixed finite coefficient-information-class
nonpromotion；它没有把 arbitrary defect物化为 physical operator、determinant
或 spectral conclusion。RH-362同样没有 fixed physical `h0=2` two-affine
Möbius coefficient、actual ordered prefix、content/`Delta#`、BV envelope、
`X/Q/J/N0` ledger、small-content zero saving、O161 theorem、actual-cloud frame、
pair-to-`omega`或 H1 occurrence edge。normalized-to-unnormalized、selected-window-
to-full-prefix与 absolute-majorant-to-signed-obstruction promotion仍被禁止。

精确 late-delta verdict为：

```text
RH362_9902699_94951C3_1B3513F_HANDOFF_ONLY_SOURCE_LOCK_AND_ADVERSARIAL_
NOT_TESTABLE_NO_NEW_THEOREM_BODY_EXTERNAL_SOURCE_PHYSICAL_D_EDGE_OR_
TPC32_PREFIX_BV_O161_FRAME_PAIR_H1_TRANSFER_NO_TRIGGER_STOP_SCOPED_
PARENTS_OPEN
```

因此该 delta既不新增第 6 节 method cell，也不重开任何 TPC parent；本节
`PRESENT_L1` scalar refinement与 `NO_L2/STOP_SCOPED/PARENTS_OPEN`裁决不变。

### 48.5 精确状态、裁决与 STOP scope

本轮状态为：

```text
SAME_SELECTED_HIGH_BETA_PACKET_SOURCE_LOCK = PASS
H0_2_SPECIALIZATION = PASS_THEOREM_LEVEL
THREE_RAW_CHANNELS_CONTENT_DELTA_SHARP_N0_LOCK = PASS

FULL_POSTBIN_DICTIONARY_INTERTWINER_JQ_D_TO_Q_Z = ABSENT
LOSSLESS_SCALAR_ZERO_MODE_COMMON_NATIVE_REFINEMENT_VIA_TPC93 = PRESENT_L1
SCALAR_FACTOR_ALLOCATION_AND_LITERAL_PREFIX_ORDER = PRESENT_L1
SCALAR_GLOBAL_NORMALIZATION = PRESERVED
N0_TO_Q_SQUARED_SCALE_IDENTITY = PRESENT
E_CONT_ZERO_WITH_CONTENT_MASK_IN_WEIGHT
  = PRESENT_EXACT_FOR_DECLARED_ALL_THETA_FACTOR_ALLOCATION

GROWING_DETERMINISTIC_TWO_AFFINE_MOBIUS_PREFIX_THEOREM = ABSENT
ACTUAL_OUTER_BV_ENVELOPE = ABSENT
DIRECT_SMALL_CONTENT_ZERO_BOUND = ABSENT
FLATNESS_ENERGY_LOWER_BOUND = ABSENT

ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
CHI_LE_1_OVER_400 = UNPAID
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false

LATE_REMOTE_RH362_SOURCE_LOCK_AND_ADVERSARIAL = NOT_TESTABLE
LATE_REMOTE_RH362_CREATED = false
LATE_REMOTE_RH362_TO_TPC_EDGE = NONE
```

当前 scalar supersession ledger 为：

```text
CURRENT_SCALAR_SUPERSESSION_LEDGER

SECTION_6_SELECTED_PACKET_CELL_OLD_SCALAR_PREREQUISITES
  = SUPERSEDED_BY_SECTION_48
SECTION_23_2_TO_23_4_SCALAR_INTERTWINER_FACTOR_ORDER_NORMALIZATION
  = SUPERSEDED_BY_SECTION_48
SECTION_27_3_N0_SCALAR_CROSSWALK_FIELD
  = SUPERSEDED_BY_SECTION_48
SECTION_28_4_N0_SCALAR_CROSSWALK_FIELD
  = SUPERSEDED_BY_SECTION_48
SECTION_35_5_LOSSLESS_A_C_ZERO_COEFFICIENTWISE_FIELD
  = FULL_DICTIONARY_ABSENT_BUT_SCALAR_COMMON_REFINEMENT_PRESENT_L1
SECTION_37_4_N0_AND_LOSSLESS_SCALAR_MAP_FIELDS
  = SUPERSEDED_BY_SECTION_48
SECTION_45_5_LOSSLESS_A_C_ZERO_TO_ORDERED_PREFIX_FIELD
  = SUPERSEDED_BY_SECTION_48
```

这些旧段落保留为当时 audit snapshots，但不得再作为 current scalar first fatal。
它们的 source-specific wrong-object排除、candidate theorem缺失、
`(J Q_D-Q_Z)M=0` full-dictionary absence、growing prefix/BV/direct-zero缺失、
`NO_L2`、STOP/OPEN与 TPC-207状态均未被覆盖。特别地，§27.3/28.4 的 actual
`Q_D/Q_Z/J` maps为空仍阻断 full dictionary；只是不再阻断同一 zero-mode scalar
经 TPC-93 common native source basis进入 ordered Abel fibers。

精确裁决为：

```text
TPC32_H0_2_20260804_TPC93_SCALAR_ZERO_MODE_COMMON_NATIVE_REFINEMENT_
PRESENT_L1_GROWING_TWO_AFFINE_MOBIUS_PREFIX_AND_ACTUAL_BV_ENVELOPE_
ABSENT_ANGELO_XU_2411_14447V3_WRONG_OBJECT_NO_TRIGGER_STOP_SCOPED_
PARENTS_OPEN
```

第 6 节全部旧 method cells继续 `STOP_SCOPED`，尤其是 TPC193 V1、common-`k`
V1、tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1。第 48 节不为
TPC-93另造 method cell；只新增 Angelo--Xu v3的 source/version-specific
wrong-object transfer cell。两个 O161 pointwise parents、TPC32 direct/
fixed-`D0`/frame、pair-native reroute、独立 pre-TT-star H1 与 global
architecture全部保持 `OPEN`。

### 48.6 合法 reopen、下游 gates 与 publication boundary

下一次只在以下任一 source-backed状态真实变化时重开本 route：

1. 直接对同一 selected packet、three raw channels、`G<=C`、actual
   masks/weights/outer labels与原 global normalization证明
   `|A_hat_C,q_DFT(0)|<=X^(o(1))Q^2` 或更强 small-content saving；
2. 对第 48.2 节同一 actual ordered fibers证明 uniform growing deterministic
   two-affine Möbius prefix theorem与完整 BV envelope，并真实满足
   `delta_pre>=ell_Z`；content mask的全部 variation必须支付；
3. 若未来目标需要完整 fiber dictionary而非 scalar evaluator，再物化 actual
   growing archive并证明 `(J Q_D-Q_Z)M=0`，但 full `J` 不再是 scalar route
   的前置门。

任何 local positive result仍不自动创建 TPC-207。all-`D` uniformity、
exactly-once physical cover、original/global normalization、tail-failure、A/B
selection、actual packet attachment、production occurrence、完整 provenance及
strict physical-loss ledger仍须分别通过，并使页首 TPC-207 trigger发生真实
theorem-backed状态变化。

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志；正式写入只允许
`TPC_HANDOFF.md`。全部 protected untracked必须原样保留且不得纳入提交。
正式写入后的 22 项全回归、TPC-111/124/126/127 supplemental、diff/fence、
protected manifest与 final sync/push hashes在本节封口前复核。

```text
LATE_REMOTE_FETCH_ORIGIN_MAIN
  = 1b3513ffde611b26f050fac02006b82c3799021a
LATE_REMOTE_CHANGED_PATH = RH_HANDOFF.md_ONLY
LATE_REMOTE_TPC_TRIGGER = NO
POST_LATE_DELTA_FINAL_BOOTSTRAP_REGRESSION = 22/22 PASS
POST_LATE_DELTA_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_LATE_DELTA_GIT_DIFF_CHECK = PASS
POST_LATE_DELTA_EOL = i/lf w/lf
POST_LATE_DELTA_MARKDOWN_FENCES = 1358 MARKERS BALANCED
POST_LATE_DELTA_NUMBERED_SECTIONS = 48 UNIQUE; DUPLICATES=0
POST_LATE_DELTA_PROTECTED_UNTRACKED = 127 FILES
POST_LATE_DELTA_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
SUBAGENT_FILES_CHANGED = 0
LEGACY_TPC27_TO_32_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md_ONLY
```

## 47. 2026-08-04 RH-361 typed coefficient-fiber nonpromotion 与 TPC literal-transfer 审计

### 47.1 late remote delta、tree boundary 与只读 source lock

第46节完成写入与 pre-release checks后，`git fetch origin main` 把
`origin/main` 从
`75217b84242a54615af406f0fd3a5489b0be941c` 推进一个 commit至

```text
91167fe163831d3360b4c4007ed600865610e9ec
Add RH-361 signed-completion counterloop review
```

delta严格新增目录
`papers/RH-361-ten-layer-signed-completion-and-upper-counterloop-review/`
下24个 committed files；没有覆盖 TPC source、`TPC_HANDOFF.md`、
`AGENTS.md`、`.codex`或根 scoped policy。由于主控已有本轮
`TPC_HANDOFF.md` 修改，未在 dirty tracked tree上强行 rebase、stash或
checkout；先直接对 `origin/main` tree作 read-only theorem/artifact audit。
三个 read-only agents分别复核 exact theorem、source/version lock及
artifact/release boundary，均保持 `files_changed=[]`。

primary source lock为该 commit的 `main.tex`、`README.md`、
`THEOREM_LEDGER.md` 与 committed `results/result.json`。
本节承认 RH-361在 RH program内的最大合法正结果，但只审核它是否逐 literal
field附着到同一 TPC selected packet；不是对 RH program作降级。

### 47.2 RH-361 exact typed theorem

同一 Hardy clock的 source identities为

```text
p = tau-a = q-d,
d = h-s,
q = p+d,
h = s+d.
```

RH-361 Theorem 5.2（`thm:fiber`）固定非空 finite order set
`I`、positive weights `w_n` 及 signed arrays `p,s`。
对每个 arbitrary signed array `e` 定义

```text
d^[e] = e,
q^[e] = p+e,
h^[e] = s+e.
```

则两条 identities coordinatewise exact。若 `e=t*v` 且
`v!=0`，`q^[e],h^[e]` 的 weighted `ell^1` budgets随
`|t|` 无界，而 `p,s` 固定；取 `e=-p` 或 `e=-s`
又分别令 `q` 或 `h` 为0。因此只从 fixed `p,s` 与
coefficient identities不能给 `q,h` budget的 uniform upper/lower
promotion。

这是一个真实、exact的 finite coefficient-information-class theorem。source
同时明确排除 operator、determinant、root、rank、cross-order realizability与
physical counterexample construction；arbitrary `e` 不声称由 noisy
quadratic operator实现。Corollary 5.4（`cor:forbidden`）据此证明两项
batch-premise nonpromotion：

1. selected/normalized actual direct `p` 不能在没有 same-clock defect
   `d` control时升级为 full-trace `q/E_off`；
2. deterministic counterloop `s` 的大 budget不能升级为 actual-head
   budget、root、rank或 spectral-submultiset statement。

Theorem 6.1（`thm:batch`）进一步 source-lock十层 type：

- RH-352--354无条件 actual conclusions只属于 selected natural/alias
  normalizations的 `p,Y`；
- RH-355--360无条件 conclusions只属于 deterministic counterloop
  `s` 及其 normalized budgets；
- 六篇 actual-head transfer全都仍条件于未证的 unnormalized same-clock
  `D_(4k)(R)->0`；
- deterministic terminal-lag route只在其 declared budget type闭合；
  `q/E_off`、actual root/rank/spectrum/determinant、RH-241 bridge与
  RH-288 activation均未形成。

所以 RH-361 的最大合法 verdict为
`GO_SCOPED_TYPED_BATCH_SEPARATION`。它是新的 RH theorem-backed
type-separation/nonimplication，不是 physical cancellation theorem。

### 47.3 TPC32/O161 literal field audit

RH-361 的 actual signed completion变量 `Y` 是 Hardy trace/moment-order
remainder；`p,s,d,q,h` 也都以 trace order `n` 或 ladder index
`j` 排列。第一致命不匹配为：

```text
RH361_TRACE_ORDER_P_Y_AND_FORMAL_TYPED_FIBER
  !=
ACTUAL_DETERMINISTIC_TWO_AFFINE_H0_2_MOBIUS_SIGN
```

逐 required field核对如下：

| field | TPC actual requirement | RH-361 source | verdict |
|---|---|---|---|
| coefficient | `mu(d+s*r)mu(u+a*r)` 及 TPC32 three raw physical channels | Hardy `p,Y`、counterloop `s` 与 arbitrary formal `e` | FAIL, first fatal |
| fixed shift | prescribed physical `h0=2` | trace-order/ladder parameters；相邻 order差2不是 `h0=2` | FAIL |
| domain/order | every actual outer fiber的 literal translated-integer all-prefix order | finite order set或 selected trace/moment tail | FAIL |
| determinant/content | actual `G<=C`、`Delta#`、same-channel `A_C` | no TPC determinant bin、content projector或 channel registry | FAIL |
| masks/outer labels | selected packet actual masks、weights、`(alpha,gamma,j)` | no coefficientwise TPC attachment | FAIL |
| normalization | `N0=JQ^2 asymp XQ`，或 O161 terminal `q/N` 与 scheduled BAD ledger | RH source scales/weighted finite `ell^1` budgets；source符号 `q` 是 full-trace coefficient | FAIL |
| ranges/constants | common `X,J,Q,C,q_DFT`、all actual fibers、uniform constants | no TPC `X/N/q` parameter range | FAIL |
| conclusion/direction | `chi<=1/400` 或 direct small-content matched-shell saving | premises不足以 promotion的 non-determination theorem | FAIL / UNPAID |

尤其不得把 RH full-trace coefficient `q` 改名为 determinant modulus
`q_DFT`、O161 Jacobian或 prefix normalization；不得把 arbitrary
formal fiber `e` 选择成 Möbius realization；不得把“不能从这些 premises
推出”改写为 TPC zero/cancellation或 global impossibility theorem。

即使把 RH-352/353 actual selected signed-`Y` result作最有利 steelman，
它仍是不同 index、不同 coefficient、不同 selected normalization及 gap/supply
direction；没有 same-packet coefficientwise intertwiner到
`A_hat_(C,q_DFT)(0)`。RH-361反而明确证明 source branches不可仅凭
现有 identities拼接。故它加强 claim firewall，但不支付任何 arithmetic loss。

### 47.4 committed artifact 与既有 TPC state

committed `result.json`、archive verifications与 theorem ledger一致记录：

```text
RH361_VERDICT = GO_SCOPED_TYPED_BATCH_SEPARATION
RH352_TO_RH361_GATE_VALUES = 50/50 FALSE
RH352_TO_RH361_FORBIDDEN_CLAIM_VALUES = 149/149 FALSE
RH361_INDIVIDUAL_ARCHIVE = 20 FILES, 0 FAILURES
RH352_TO_RH361_BATCH_ARCHIVE = 176 FILES, 0 FAILURES
PHYSICAL_COUNTEREXAMPLE_CONSTRUCTED = false
BRIDGE_PROVED_IN_BATCH = false
SAME_CLOCK_D_4K_TRANSPORT_PROVED = false
```

这些 artifacts认证 source type、finite identities与 manifest consistency；
它们不是 TPC theorem evidence。late delta没有任何 TPC source/blob变化，所以
TPC-206 selected pair仍是 `13/42`、首缺 field #9 uppercase opened
`D`，production occurrence、pair-to-`omega` 与 linear H1 edge
仍为 false/absent in current TPC tree。第46节 signed-prefix/O161/frame
current-primary verdict与三个 source-specific cells亦未被 RH-361改变。

### 47.5 精确 TPC 裁决与合法 reopen

本轮 late-delta精确裁决为：

```text
TPC32_O161_RH361_20260804_TYPED_COEFFICIENT_FIBER_AND_BATCH_SEPARATION_IS_
VALID_NONPROMOTION_ONLY_FAILS_LITERAL_TWO_AFFINE_H0_2_MOBIUS_SIGN_CANONICAL_
PREFIX_CONTENT_DETERMINANT_X_SCALE_AND_NORMALIZATION_TRANSFER_NO_TRIGGER_
STOP_SCOPED_PARENTS_OPEN

RH361_RH_PROGRAM_ADVANCE = GO_SCOPED_TYPED_BATCH_SEPARATION
RH361_TO_TPC_LITERAL_CROSSWALK = NOT_SUPPLIED
RH361_TO_TPC_SIGNED_PREFIX_THEOREM = NOT_SUPPLIED
RH361_TO_TPC_SMALL_CONTENT_SAVING = NOT_SUPPLIED
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第6节全部旧 method cells继续 `STOP_SCOPED`；新增 RH-361
commit-specific cell只冻结上述跨类型 transfer。两个 O161 pointwise parents、
TPC32 direct/fixed-`D0`/frame parents、pair-native reroute、独立
pre-TT-star H1、RH actual-head route与 global architecture保持 `OPEN`。

只有以下任一真正新的 source-backed输入才重开相应 parent：

1. 对 RH source：证明 actual unnormalized same-clock
   `D_(4k)(R)->0`，或直接给 typed `q/E_off` theorem；这仍不自动
   映射到 TPC；
2. 对 TPC32：同一 selected packet上的 deterministic growing
   two-affine Möbius signed-prefix theorem或 direct small-content matched-shell
   saving，保留 fixed `h0=2`、three raw channels、content/
   `Delta#`、actual masks/outer labels与 one `N0` ledger；
3. 对 O161：literal `mu(d+s*z)mu(u+a*z)`、prescribed phase及 actual
   packet上 terminal `q/N` fixed-power theorem，或逐 scheduled ancestor
   的 local `q/N_j` theorem加 TPC-159
   `N_j/T=2^(-j)` exact telescoping；
4. actual moving-level full/cross-`D0` cloud Gram、same-source complete
   42-field pair、pair-to-`omega` 或 linear H1 occurrence edge。

任一 local gate转正仍不自动创建 TPC-207；all-`D` uniformity、
exactly-once physical cover、original/global normalization、tail-failure、A/B
selection、actual packet attachment、production occurrence、完整 provenance与
strict `1/400` payment仍须分别通过。

### 47.6 publication boundary

RH-361是新的 RH type-separation theorem，不是 TPC arithmetic advance。本轮仍只
允许发布 `TPC_HANDOFF.md`；不得创建 TPC-207、论文、paper directory、
PDF或下一编号。全部 protected untracked必须原样保留且不纳入提交。当前
handoff commit后才允许在 clean tracked tree上
`git pull --rebase origin main`，随后必须重跑第1节22项回归、
TPC-111/124/126/127四项 supplemental、diff/fence与 protected manifest。

```text
POST_REBASE_BASE
  = 91167fe163831d3360b4c4007ed600865610e9ec
POST_REBASE_BOOTSTRAP_REGRESSION = 22/22 PASS
POST_REBASE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_REBASE_GIT_DIFF_CHECK = PASS
POST_REBASE_MARKDOWN_FENCES = 1296 MARKERS BALANCED
POST_REBASE_PROTECTED_UNTRACKED = 127 FILES
POST_REBASE_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
SUBAGENT_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
RH361_BUILDERS_VERIFIERS_TESTS_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md
```

## 46. 2026-08-04 current-primary signed-prefix、O161、actual-cloud frame 与 pair/H1 审计（late RH-361 fetch 前快照）

### 46.1 基线、只读分工与有限 source scope

本轮启动时 HEAD 与 `origin/main` 同为
`75217b84242a54615af406f0fd3a5489b0be941c`，
`git pull --rebase origin main` 返回 already up to date；
`TPC_HANDOFF.md` 启动 SHA-256 为
`ef23b2a2193b230ca3c8276fa5d2305e874c6826ccf2a9ad7f4d2c1e7ad06e6f`。
tracked/cached diff均为空；127个 protected untracked files的 manifest为
`35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f`。
第 1 节全部 22 项只读启动回归为 `22/22 PASS`；TPC-27--32 legacy
writers与 TPC-122 writer均未执行。

主控按根 `AGENTS.md` 冻结同一 selected packet与 literal theorem gates。
三个 read-only agents分别完成：

```text
TPC-REOPEN-20260804-E-TPC32-SIGNED-PREFIX
TPC-REOPEN-20260804-E-O161-CURRENT-PRIMARY
TPC-REOPEN-20260804-E-PAIR-H1-FRAME-RH361
```

三者均回报同一 HEAD/handoff hash、`files_changed=[]`、
`generated_outputs=[]`；正式写入仍只由主控完成。source evidence只采用
official arXiv versioned theorem body/PDF与 reachable committed tree。2026-08-04
official `math.NT/new` finite screen有 84 entries（39 new submissions、
15 cross-lists、30 replacements）；另作 `math.DS`、`math.SP`
有限邻近扫描。本节只裁决下列明示 sources/versions与 current refs，不声称全局
文献不存在。

### 46.2 同一 selected packet 与不可更换的 physical object

第 23、29--45 节冻结的 theorem-valid packet没有改变：

```text
sigma  = 1/10000
lambda = 99979/210000
delta  = 7/60
beta   = 267/400
Q      = X^(267/400+o(1))
J      = X^(133/400+o(1))
C      = floor(J) = X^(133/400+o(1))
h0     = 2
N0     = J Q^2 asymp X Q
```

第 22 节 `delta=1/20` truncated-entry family仍是另一条 source lock；
`TRUNCATED_ENTRY_ABSENT` 只适用于该 family，绝不与本 packet拼接。

TPC-32 actual small-content zero-mode对象仍由同一 physical shell内不可拆的三条
raw channels

```text
A_(m,T) C_n,  C_m A_(n,T),  C_m C_n
```

在 actual masks、smooth/fixed-period weights与 outer `(alpha,gamma,j)`
labels下构成。canonical content/determinant为

```text
G      = gcd(m_alpha*j+h0, m_gamma*j+h0) <= C
Delta# = (m_alpha-m_gamma)/G
A_hat_(C,q_DFT)(0) = sum_n A_C(n)
F_0(A_C) = |A_hat_(C,q_DFT)(0)|^2 / sum_n |A_C(n)|^2.
```

TPC-111 actual sign与 TPC-122 actual all-prefix object分别为

```text
sigma_(theta,X)(r) = mu(d+s*r) mu(u+a*r),  s*u-a*d=h0=2,
Delta_f = max_(k<=m_f) |sum_(i<=k) sigma_(f,i)|,
```

其中 prefix order必须是每个预声明 actual outer fiber上的 literal translated-
integer order。ordered signed-prefix、outer bounded variation与 content remainder
还必须在同一 factor allocation及 one `N0` normalization下同时给出
positive fixed power；最终需要 `chi<=1/400` 或直接的 small-content
matched-shell saving。

TPC-124 的 lossless dictionary gate仍要求 coefficientwise identity
`(JQ_D-Q_Z)M=0`。committed audits仍给：

```text
actual_growing_G_C_z_B_archive_present = false
actual_growing_prefix_saving           = false
actual_outer_bv_envelope               = false
actual_content_remainder_bound         = false
positive_eta_Z                         = false
fixed_h0_L2_saving                     = false
```

因此候选 theorem必须先在 literal coefficient、fixed physical `h0`、
summation domain/prefix index、`X/N/q` ranges、uniform constants、
normalization与完整 physical-loss ledger全部逐项相等；相似 vocabulary不构成
intertwiner。

### 46.3 Schlitt random periodic-BV theorem 对 signed-prefix gate

Schlitt `2608.00184v1` Theorem 1.3研究

```text
S_g(N) = V_g(N)^(-1/2) sum_(n<=N) f(n) g(theta*n),
V_g(N) = sum_(n<=N) |g(theta*n)|^2,
```

其中 `f(p)` 是独立、单位圆均匀的 Steinhaus random variables，
`f` 完全乘法，`theta` 是满足 source Diophantine condition (1.2) 的 fixed
irrational；Theorem 1.3 的 `g` 是 nonconstant one-periodic BV function，
并证明 CLT恰当且仅当 source dilation-correlation condition成立（等价于 source
`Delta(g)=0`），不是对每个 nonconstant BV weight的无条件 CLT。Theorem 1.5
另要求 nonconstant mean-zero `g in BV_0` 与 source-stated `xi(N)` growth
conditions，并对 `P^-(n)>xi(N)` rough support给相应 Gaussian limit。
source的 Fourier/dilation defect `Delta(g)` 不是
TPC canonical `Delta#`、prefix discrepancy `Delta_f`、content
projector或 `F_0(A_C)`。

source martingale按 largest-prime filtration
`F_p=sigma(f(q):q<=p)` 组织；martingale difference来自 random prime
independence与 conditional mean zero。BDG supremum因此按 prime filtration，
不是 TPC actual translated-integer order。Proposition 6.1也只给 random
expectation的 moment bound和 polylog-range Fourier polynomial uniformity，
不是 deterministic growing outer-fiber all-prefix theorem。

第一致命不匹配为：

```text
RANDOM_STEINHAUS_SINGLE_FACTOR
  !=
ACTUAL_DETERMINISTIC_TWO_AFFINE_H0_2_MOBIUS_SIGN
```

即使把 CLT作最有利 steelman，它也只描述 law over random `f`。source
没有把 prescribed Möbius realization识别为 typical sample，没有 one-realization/
all-`X` theorem、summable exceptional probabilities或 Borel--Cantelli
ledger；`V_g(N)` 也不是 determinant binning后的
`sum_n |A_C(n)|^2`。将第二个 Möbius factor塞入 `g` 会把 fixed
periodic-BV weight改成 `X`-dependent arithmetic weight；rough-number
restriction则删除 actual support atoms且没有 exactly-once reassembly。

故 Abel summation、martingale/Doob/BDG、Carleson/variation、Parseval、
complete-frequency mean、pretentious inverse或 entropy decrement均不能把该
source升级为 prescribed zero mode。maximum justified claim只是一项 random-model
analogy；TPC credit为零。本 source/version-specific transfer严格由第 6 节新 cell
停止。

### 46.4 O161 与 actual-cloud frame current-primary source lock

O161 literal core保持：

```text
L1(z)=d+s*z, L2(z)=u+a*z,
c_z=mu(L1(z))*mu(L2(z)),
s*u-a*d=2.
```

DIRECT parent需要 prescribed phase上的 terminal `q/N` fixed-power theorem；
BAD parent需要每个 scheduled ancestor上的 local `q/N_j` theorem，再由
TPC-159 的 `N_j/T=2^(-j)` exact telescoping得到 cumulative `q/T`。current
source结果为：

| source/version | strongest nearby object | first fatal |
|---|---|---|
| Schlitt `2608.00184v1` | random Steinhaus single-factor periodic-BV CLT/moments | random single factor，不是 deterministic `c_z` |
| Alass--Saad Eddin `2608.01399v1` | regular-integer nested averages，含 `mu(gcd(k,n))` 或 `mu(ell)/ell` | 一个 Möbius factor与不同 summation/normalization |
| Broadbent--Fiori--Kadiri--Ng--Wilk `2608.01498v1` | prime harmonic “Mertens sums”/products | 正文对象不是 Möbius coefficient或 partial sum |

三者在 fixed `h0`、actual packet/masks/weights、natural prefix、
uniform growing ranges与 loss ledger之前已失败；不得把不同 sources的
coefficient syntax、normalization或 conclusion拼接。

actual GM cloud仍为

```text
B_t = [[m,(m*j+2)/G],[n,(n*j+2)/G]]
H_t = 2*|m-n|/G
g_t = H_t^(-1/2) B_t^+ in SL_2(R).
```

目标是 moving `Gamma_pm(q)\SL_2(R)` 上 actual signed Dirac cloud的
first-slot full与 cross-`D0` Gram blocks、全部 relevant right-`K`
types及 literal weights，并须 source-backed地满足

```text
E1 <= P_X * sum_t |a_t|^2,
P_X <= X^(1/400-kappa_row-epsilon+o(1)),
0 < kappa_row < 1/400.
```

current source结果为：

| source/version | source theorem | first fatal |
|---|---|---|
| Tiwari `2608.02405v1`, Theorem 1.1 | connected compact manifold上 maximal epsilon-net weighted graph Laplacian与 Laplace--Beltrami eigenvalues比较；constants对 injectivity radius独立 | designed compact discretization/eigenvalue comparison，不是 signed spatial cloud Gram |
| Magee--Roig-Sanchis--Thomas `2608.00386v1`, Theorems 1.1/1.4 | closed hyperbolic 3-manifolds/two-torsion line bundles的 spectral-gap存在性及 representation strong convergence | closed H3 existential gap，不是 moving congruence surface point frame；two-torsion不是 physical `h0=2` |
| Qi `2407.17959v3`, Theorem 1 | fixed Picard full group上 symmetric-square Hecke coefficients的 spectral large sieve，含 non-spherical representation parameter | fixed `PSL_2(C)` spectral family mean，不是 moving `SL_2(R)` spatial point evaluation |

三项 theorem均为真实 source结果，但没有 actual cloud separation/local
multiplicity、full/cross-`D0` block、coefficientwise `a_t`
intertwiner或 `P_X` exponent。Qi的 full-group/non-spherical syntax最接近，
但 group、coefficient space、averaging direction与 operator均不同；不得与
Tiwari discretization或既有 Chamizo fixed-surface theorem拼接。

### 46.5 pair/H1 initial refs 与 RH-361 pre-fetch absence

TPC-206冻结时的 all-ref census为 34 refs、28 unique tips；本轮 current repo
仍为同样数量。相对 all-ref H1 freeze
`023ccb5959e35b96673117b76add3dcbc3987aca` 的 reachable TPC-paper
delta只有 TPC-134/135/136三个 certificate JSON 的 upstream SHA-256 pins；
没有新 theorem body、pair record、opened-`D`、production occurrence、
normalization、retained `omega`或 H1 edge。raw reachable-text scan的
complete-42/opened-`D`/pair-to-`omega`/linear-H1 hits只出现在
handoff历史 obstruction叙述，没有 non-handoff source witness。

selected TPC-206 object仍精确为：

```text
alpha=(103,1), gamma=(107,1), j=5, X=512, h0=2
materialized = 13/42
production_occurrence = false
first_missing_field_index = 9
first_missing_field_id = D
```

row divisor `d=1` 不是 source-locked uppercase opened scale
`D=1`。即使未来供应 `D`，同一 source record仍须供应
`J,Q,T,U0,G_X_row`、packet/source locator、joint mask、literal pair AST、
active/nonzero support、retained `omega`、child inverse与四阶段
normalization。TT-star pair carrier对 source coefficient二次齐次；H1
`L_X` edge必须线性且 coefficientwise conservative。没有 source-backed
inverse aggregation theorem时，二者不能互换。

所有 reachable objects、paths与 commit messages均没有 `RH-361`；
`git rev-list --all --objects` 的 `papers/RH-361-*` 匹配为 0。
RH-360 roadmap只说 next paper应为 RH-361，不是 fetched theorem delta；
`RH_HANDOFF.md` 的旧 endpoint文字也不能替代 tree evidence。
这是 `origin/main=75217b8` 时的精确 pre-fetch快照；发布前 late fetch随后
取得 RH-361 commit `91167fe`，其 current-state裁决由第 47 节覆盖。

### 46.6 精确裁决、状态防火墙与 reopen interface

本轮 finite theorem audit的精确裁决为：

```text
TPC32_O161_PAIR_H1_20260804_CURRENT_PRIMARY_RANDOM_MULTIPLICATIVE_BV_AND_
GEOMETRIC_SPECTRAL_FRAME_SOURCES_FAIL_LITERAL_DETERMINISTIC_TWO_AFFINE_
COEFFICIENT_CANONICAL_PREFIX_ACTUAL_MOVING_CLOUD_GRAM_OPENED_D_H1_EDGE_OR_
NORMALIZATION_GATES_NO_TRIGGER_STOP_SCOPED_PARENTS_OPEN

GROWING_TPC_SIGNED_PREFIX_THEOREM
  = NOT_SUPPLIED_BY_DECLARED_20260804_SOURCE_SET
DIRECT_SMALL_CONTENT_MATCHED_SHELL_SAVING
  = NOT_SUPPLIED_BY_DECLARED_20260804_SOURCE_SET
O161_LITERAL_GROWING_FIXED_POWER_THEOREM
  = NOT_SUPPLIED_BY_DECLARED_20260804_SOURCE_SET
ACTUAL_FULL_CROSS_D0_CLOUD_GRAM_THEOREM
  = NOT_SUPPLIED_BY_DECLARED_20260804_SOURCE_SET
SAME_SOURCE_COMPLETE_42_FIELD_PAIR
  = NOT_SUPPLIED_BY_CURRENT_REACHABLE_TPC_TREE
PAIR_TO_OMEGA_THEOREM
  = NOT_SUPPLIED_BY_CURRENT_REACHABLE_TPC_TREE
H1_LINEAR_OCCURRENCE_EDGE
  = NOT_SUPPLIED_BY_CURRENT_REACHABLE_TPC_TREE
RH361_FETCHED_THEOREM_DELTA = NONE_AT_SECTION_46_SNAPSHOT
THEOREM_TRIGGER = false
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节全部旧 method cells保持 `STOP_SCOPED`，尤其 TPC193 V1、
common-`k` V1、tail-failure/A/B V1与 full-`r_R r_R`
ultra-complement V1；本轮只新增三个 source/version-specific cells。两个 O161
pointwise parents、TPC32 direct/fixed-`D0`/frame parents、pair-native
reroute、独立 pre-TT-star H1、RH actual-head route与 global architecture保持
`OPEN`。

只在出现下列 source-backed输入时重开相应 local parent：

1. 同一 actual selected packet上 deterministic growing signed-prefix theorem，
   coefficientwise保留 three raw channels、fixed `h0=2`、content/
   `Delta#`、outer labels、literal prefix order、masks/weights、one
   `N0` normalization与完整 loss ledger，并给
   `chi<=1/400`；或直接证明 small-content matched-shell saving；
2. 对 O161 literal `mu(d+s*z)mu(u+a*z)`、actual packet与 prescribed
   phase直接给 natural terminal `q/N` fixed-power theorem，或逐 ancestor
   满足 local `q/N_j` theorem并经 TPC-159
   `N_j/T=2^(-j)` exact telescoping形成 cumulative `q/T`；
3. 直接作用于 moving `Gamma_pm(q)\SL_2(R)` actual signed cloud、
   all relevant `K` types与 full/cross-`D0` blocks的 spatial
   level-uniform Gram theorem，并支付 displayed `P_X` threshold；
4. materialize same-source complete 42-field production pair、opened
   uppercase `D`、pair-to-`omega`与四阶段 normalization，或从
   named pre-TT-star source cut正向给出 linear H1 occurrence edge；
5. 实际 fetch到 RH-361或其他新 tree后，逐 theorem body重新审核 literal object；
   roadmap文字、schema或 artifact alone均不是 trigger。RH-361已由第47节完成该
   审核并得到 commit-specific `STOP_SCOPED_NO_TPC_TRIGGER`。

任一 local gate转正也不自动创建 TPC-207。all-`D` uniformity、
exactly-once physical cover、original/global normalization、tail-failure、A/B
selection、actual packet attachment、production occurrence、完整 provenance与
strict `1/400` payment仍须分别通过，并使页首 trigger发生真实
theorem-backed状态变化。

### 46.7 publication boundary

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入只允许
`TPC_HANDOFF.md`；全部 protected untracked保持原样且不纳入提交。
以下是第46节写完、RH-361 late fetch发生前的 historical closure；current release
closure见第47.6节：

```text
POST_WRITE_BOOTSTRAP_REGRESSION = 22/22 PASS
POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_GIT_DIFF_CHECK = PASS
POST_WRITE_MARKDOWN_FENCES = 1280 MARKERS BALANCED
POST_WRITE_PROTECTED_UNTRACKED = 127 FILES
POST_WRITE_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
SUBAGENT_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md
```

## 45. 2026-08-04 RH-360 terminal-lag exponential-tilt phase transition 与 TPC literal-transfer 审计

### 45.1 remote delta、只读基线与分工

本轮启动时 tracked/cached diff为空，只有 127 个既有 protected untracked files。
`git pull --rebase origin main` 将

```text
02037a772d358cda246c8d1202df1a1a883e4e49
```

安全 fast-forward 至

```text
27b0b46e9f000c3f27a9546192765287734250d8
  Add RH-360 terminal-lag tilt phase transition
```

delta严格为
`papers/RH-360-terminal-lag-exponential-tilt-phase-transition/` 下 20 个
new files；没有修改 TPC source、handoff、`AGENTS.md`或 `.codex` policy。
启动 `TPC_HANDOFF.md` SHA-256为
`e45b9991abe0a63785b82b593fee9bbd322d8858e68e8bb8f071b97037b3ff33`。
第 1 节 22 项只读启动回归为 `22/22 PASS`。

三个只读分工分别审核 source/TPC crosswalk、逐式 proof/quantifiers与 raw
Git-object artifacts/schema/provenance，全部锚定同一 HEAD/handoff hash并报告
`files_changed=[]`、`generated_outputs=[]`。主控另行读取 RH-360 全文、RH-358
conditional source及 TPC-28/32/111/122 literal interfaces，并独立重建关键公式和
Git-blob archive。没有运行 RH-360 builders、verifier mains、tests或 PDF build；
没有执行 TPC-27--32 legacy writers或 TPC-122 writer。

### 45.2 exact transform theorem 与量词边界

RH-360锁定 RH-358 的同一 deterministic terminal-lag probability：

```text
y_k=x exp[-log(C_M)/k+o(1/k)],  x>1, C_M>0,

pi_k(r)
  =[y_k^(2k-1-r)/(2k-1-r)]/C_k,
  0<=r<=k-2,

G_k(z)=sum_(r=0)^(k-2) z^r pi_k(r),  z>=0.
```

令

```text
A_k(u)=sum_(r=0)^(k-2) u^r (2k-1)/(2k-1-r).
```

exact quotient为

```text
G_k(z)=A_k(z/y_k)/A_k(1/y_k),
A_k(1/y_k)->1/(1-x^(-1)).
```

逐式 proof audit得到 `first_internal_fatal=NONE`。三个 transform regimes为：

```text
fixed 0<=z<x:
  G_k(z)->(1-x^(-1))/(1-z/x),
  locally uniformly on compact subsets below x;

z_k=x exp(tau/k), fixed tau in R:
  G_k(z_k)/k
    ->2(1-x^(-1)) integral_0^1
         exp[(tau+log C_M)s]/(2-s) ds;

fixed z>x:
  G_k(z)
    ~[2 C_M(1-x^(-1))/(1-x/z)](z/x)^(k-2).
```

critical proof中

```text
k log(z_k/y_k)->tau+log C_M
```

并对完整 `0<=r<=k-2` grid给一致 Riemann-sum approximation；bounded endpoint
integrand使两个缺失 mesh intervals只有 `O(1/k)`，没有 floor-phase偷渡。
supercritical proof反转 `r=k-2-ell`，保留

```text
(z/y_k)^(k-2)~C_M(z/x)^(k-2),
```

所以 leading `C_M`不可删除。结论进一步正确给出 fixed `z>=0` 的

```text
(1/k)log G_k(z)->max(0,log(z/x)).
```

这里 `tau`固定，subcritical convergence不跨越临界点，supercritical `z`固定；
论文没有声称对 unbounded moving `tau_k`或 arbitrary moving `z_k-x`一致。
finite artifact只取 `C_M=1`，没有数值测试 nontrivial drift，但它明文只作公式
reproduction，不构成 analytic proof fatal。

### 45.3 tilted laws 与 conditional actual boundary

对

```text
pi_(k,z)(r)=z^r pi_k(r)/G_k(z)
```

RH-360正确证明：

1. fixed `z<x` 时，terminal lag在 total variation下趋于 ratio `z/x` 的
   geometric law；`z=0`单独为 `delta_0`；
2. `z_k=x exp(tau/k)` 时，`r/k`弱收敛到 `[0,1]` 上密度
   proportional to `exp[(tau+log C_M)s]/(2-s)`；
3. fixed `z>x` 时，opposite-endpoint distance `ell=k-2-r`在 total variation
   下趋于 ratio `x/z` 的 geometric law。

这些都是 normalized deterministic positive-budget laws。它们不是 eigenvalue、
root-counting、noisy stochastic或 arithmetic sign distributions。

RH-358在未证的 same-clock hypothesis

```text
D_(4k)(R)
  =sum_(2<=n<4k)|h_(sigma,n)-s_(k,n)|R^n/n ->0
```

下给出

```text
delta_k=sup_(0<=r<=k-2)|pi_k^H(r)/pi_k(r)-1|->0.
```

因此对任意 nonnegative tilt sequence，`G_k^H/G_k-1`确实是由
`delta_k`控制的 positive weighted average；coordinatewise relative bound也足以
条件转移 exponentially growing tilts与 tilted laws。该论证合法，但仍只转移
RH actual Hardy-head absolute budget，且完全条件于 `D_(4k)(R)->0`。它不转移
roots、rank、spectrum、determinant、RH-241/RH-288或 Gates A--E。

### 45.4 TPC literal coefficient、index 与 normalization crosswalk

selected theorem-valid packet继续严格固定为：

```text
sigma=1/10000, lambda=99979/210000, delta=7/60, beta=267/400,
Q=X^(267/400+o(1)), J=X^(133/400+o(1)), C=floor(J),
h0=2, N0=JQ^2 asymp XQ.
```

`delta=1/20` truncated-entry family仍是另一条 source lock，不得拼接。逐字段结果：

| gate | RH-360 literal object | TPC32/O161/H1 required object | verdict |
|---|---|---|---|
| physical coefficient | `z^r pi_k(r)>=0`，来自 absolute trace mass | two row coefficients、joint multiplier与不可拆的 `A_(m,T)C_n+C_mA_(n,T)+C_mC_n` signed shell；O161 two-Mobius atom；H1 actual edge | `MISMATCH` |
| fixed atom | moving trace orders与 terminal lag `r`，无 affine shift | fixed physical `h0=2`、targets `mj+2` | `ABSENT` |
| domain/order | `0<=r<=k-2` 上完整 positive moment | actual triples与 canonical translated-integer all-prefix order | `MISMATCH` |
| determinant/content | 无 `G<=C`、canonical `Delta#`或 DFT coefficient | same small-content `A_hat_C,q_DFT(0)` | `ABSENT` |
| support/metadata | deterministic probability；actual仅条件 transfer | structured residual masks、actual weights、outer labels与 occurrence attachment | `ABSENT / CONDITIONAL_ONLY` |
| ranges | `k,z,tau,x,C_M` | selected `X,Q,J,C,N0,q_DFT`及全部 packet ranges | `NO_CROSSWALK` |
| normalization/loss | 除以 `C_k` 的 dimensionless generating function；critical为 order `k`，supercritical方向为增长 | one original/global `N0` normalization、signed saving与完整 strict `1/400` ledger | `WRONG_OBJECT / UNPAID` |

第一处 fatal为：

```text
LITERAL_PHYSICAL_COEFFICIENT_AND_INDEX_UNIVERSE_MISMATCH
```

RH 的 `r`是 terminal lag，不是 determinant-DFT frequency；`z=x`是 exponential
moment的 uniform-integrability boundary，不是 distinguished auxiliary zero。
即使反事实把 RH first-alias clock

```text
k=log(1/sigma)/(2log lambda)+O(1)
```

换入，critical `G_k~k`也只给 `log(1/sigma)`量级；fixed supercritical regime
则给 positive moment增长。没有 source-backed map到 TPC固定 `sigma=1/10000`
packet的 growing `X,N0,q_DFT`，更没有 arithmetic saving方向。

### 45.5 TPC-111/122 prefix gate 与 committed artifact ceiling

TPC-111/122需要同一 actual outer fiber上的 literal signed sequence、canonical
physical order与全部 prefixes：

```text
S_(f,k)=sum_(i<=k)sigma_(f,i),
Delta_f=max_k |S_(f,k)|,

sum_i sigma_(f,i)w_(f,i)
  =S_(f,m)w_(f,m)+sum_(k<m)S_(f,k)(w_(f,k)-w_(f,k+1)).
```

它还要求 source-backed growing prefix saving、outer `BV_*` envelope、content
remainder、共同 factor allocation与 uniform ranges。RH-360只有 one complete
positive weighted sum，没有该 signed sequence或任何 prefixes。把它改名为
signed cancellation正是 TPC-111 unsigned-data obstruction排除的升级。因此

```text
LOSSLESS_A_C_ZERO_TO_ORDERED_PREFIX_INTERTWINER = ABSENT
GROWING_SIGNED_PREFIX_THEOREM = ABSENT
DIRECT_SMALL_CONTENT_MATCHED_SHELL_SAVING = ABSENT
CHI_LE_1_OVER_400 = UNPAID
```

raw Git-object artifact audit为：

```text
TREE_FILES/BYTES = 20 / 624750
PUBLICATION_FILES/BYTES = 18 / 622727
MANIFEST_MISSING/EXTRA/HASH_MISMATCH = 0 / 0 / 0
MANIFEST_KEY_SORTED_PATH_SIZE_HASH_AGGREGATE
  = ed6b7b18ec1b1a57a51f06da2506e8249f5eb860d172a9b03c570282b3ef5f7e
```

两 PDF是同一 Git blob：5页、279718 bytes、未加密、SHA-256
`e9c0b36ff3d485e16046522f65f77944e932ccfc3b1a56de106c3d21b9071c59`；
每页均可提取非空文本，总计 7645 characters，18 个 font resources已嵌入。
本轮未 render pages或做 visual QA，不声称视觉闭环。

三个 committed JSON均通过 duplicate-key、nonfinite与 UTF-8 strict parse。
`result.json`为 19194 bytes、16 top-level keys，recursive census为 28 dict、
6 list、130 str、48 bool、20 int，无 float/null；五组 finite rows各 4 条，
5 gates与 16 forbidden claims全为 strict false。

当前 raw manifest恰好完整，但 shipped verifier assurance仅 `PARTIAL`：它不独立
枚举 18-path allowlist，不核 manifest `file_count/status`，不拒绝 missing/extra
publication paths，也没有 resolved-path confinement、exact schema或 digest grammar；
empty `files` object即可得到零 failure，`../`/absolute path也未被拒绝。result test
又复用 producer；五个 production `json.dumps` call均未设 `allow_nan=False`。
production asserts为 0，tests有 54 assertions但本轮未运行。

Windows `core.autocrlf=true`。当前 checkout 18个 publication files为 624285
bytes，16个文本相对 committed manifest mismatch，只有两 PDF匹配；checkout
aggregate为
`9a2159da9ffdce0525d4bcbea2703af8cd11eae3288bc246d1c9e439f1198d83`。
所以 committed raw-Git byte snapshot为真实 PASS，但自带 checkout-byte verifier
既不是跨平台确定的只读验证，也不绑定 RH-358/RH-359 source commits/blob hashes。
这些 schema/provenance ceilings不改变更早的 literal-object fatal，也不提供 theorem
evidence。

### 45.6 exact stop、parents 与 reopen trigger

本轮新增且仅新增：

```text
DECLARED_REMOTE_RH360_TERMINAL_LAG_EXPONENTIAL_TILT_PHASE_TRANSITION_
TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED

RH360_DETERMINISTIC_EXPONENTIAL_TILT_PHASE_TRANSITION = PROVED
RH360_ACTUAL_HEAD_INHERITANCE = CONDITIONAL_ON_UNPROVED_D_(4k)(R)_TO_0
TPC32_O161_H1_RH360_20260804_TERMINAL_LAG_EXPONENTIAL_TILT_PHASE_TRANSITION_
FAILS_LITERAL_OBJECT_FIXED_H0_SIGNED_PREFIX_CONTENT_DETERMINANT_ACTUALITY_
X_SCALE_DIRECTION_OR_NORMALIZATION_GATES_NO_TRIGGER_
STOP_SCOPED_PARENTS_OPEN
GROWING_TPC_SIGNED_PREFIX_THEOREM = ABSENT
DIRECT_SMALL_CONTENT_MATCHED_SHELL_SAVING = ABSENT
ARITHMETIC_ADVANCE = NONE
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节全部旧 cells保持 `STOP_SCOPED`。两个 O161 pointwise parents、TPC32
direct/fixed-`D0`/frame parents、pair-native reroute、H1、RH actual-head route与
global architecture保持 `OPEN`。

RH-360只能在同一 positive tilt/clock内继续精化，不能靠换 tilt、取导数、
Legendre transform或 clock substitution重开 TPC gate。合法 arithmetic reopen
仍须直接接受同一 selected actual packet的 literal coefficient，保留 fixed
`h0=2`、three raw channels、canonical prefix/content/`Delta#`、actual masks/
weights/outer labels、one `N0` normalization与完整 loss ledger，并 source-backed
地证明 `chi<=1/400`或 direct small-content matched-shell saving。即使该 local
gate通过，all-`D` uniformity、exactly-once physical cover、original/global
normalization、tail-failure、A/B selection、actual packet attachment、production
occurrence与完整 provenance仍须分别通过，才可能改变 TPC-207 trigger。

### 45.7 publication boundary

RH-360是新的 RH model-side deterministic theorem，不是 TPC arithmetic advance。
本轮仍只允许发布 `TPC_HANDOFF.md`；不得创建 TPC-207、论文、PDF、paper
directory或下一编号。正式写入后必须重跑第 1 节 22 项只读回归、TPC-111/
124/126/127 四项 supplemental checks、diff/fence与 protected manifest；随后
再次同步 remote。remote若出现 RH-361或其他 theorem delta，必须先按相同
literal gate审计，不得由 RH-360 roadmap中的“next paper”文字自动产生 TPC编号。

本轮 final handoff write后的只读 closure为：

```text
RH360_POST_WRITE_BOOTSTRAP_REGRESSION = 22/22 PASS
RH360_POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
RH360_POST_WRITE_GIT_DIFF_CHECK = PASS
RH360_POST_WRITE_MARKDOWN_FENCES = 1246 MARKERS BALANCED
RH360_POST_WRITE_PROTECTED_UNTRACKED = 127 FILES
RH360_POST_WRITE_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
SUBAGENT_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
RH360_BUILDERS_VERIFIERS_TESTS_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md
```

## 44. 2026-08-04 RH-359 logarithmic terminal-window accuracy 与 TPC scale-transfer 审计

### 44.1 remote delta、rebase 与 source lock

第 43 节完成 22/22 bootstrap、4/4 supplemental、diff/fence与 protected-manifest
核对后，final fetch将 remote tip推进到：

```text
b979b87f85795a3cbb2cc4fc334f467355b0acc9
  Add RH-359 logarithmic terminal-window thresholds
```

delta严格为 `papers/RH-359-logarithmic-terminal-window-accuracy-thresholds/`
下 20 个 new files，不修改 TPC/handoff/policy。第 42、43 节两个 local handoff
commits在 tracked/cached clean、127个 protected untracked不变时安全 rebase；
当前 HEAD `11298cbafdc61f4e47246513bdd997047c8fb1cf`包含 RH-359 source及两个
协调 commits。三个只读分工分别审核 source/TPC transfer、proof/quantifiers及
artifacts/schema，均报告 `files_changed=[]`；没有运行 RH-359 builders、
verifiers或 tests。

RH-359没有新建 arithmetic coefficient。它直接锁定 RH-358 的

```text
E_k(q)=P_k(q)/C_k, 0<=q<=k-2,
E_k(q)=x^(-q) C_M^(q/k) (2k-1)/(2k-1-q)
       [1-x^(-(k-1-q))]/[1-x^(-(k-1))] (1+o(1)),
```

其中误差对全 lag range一致，`q`只是 terminal-window width。

### 44.2 logarithmic-window theorem 与 floor phase

`lem:log-window`正确证明：对每个固定 `A>0`，

```text
sup_(0<=q<=A log k) |x^q E_k(q)-1| -> 0
```

（sup只取 admissible integers）。在该范围内 `q/k=O(log k/k)`，故
`C_M^(q/k)`、denominator correction与 finite-tail quotient均一致趋 1；没有把
full-range theorem越界使用。

对 fixed `a>0,c in R`定义

```text
t_k=a log(k)/log(x)+c,
q_k=floor(t_k), theta_k={t_k}.
```

`lem:phase`的显式 subsequences证明 `theta_k`完整 limit set为 `[0,1]`，包括
两个 endpoints。`thm:phase-law`保留整数 phase并给

```text
k^a E_k(q_k)=x^(theta_k-c)(1+o(1)),
complete cluster set=[x^(-c),x^(1-c)],
liminf=x^(-c), limsup=x^(1-c).
```

所以不存在唯一 leading constant；不得删 floor phase。

### 44.3 exponent classification、minimal window 与 physical scale

对任意 admissible `q_k=o(k)`，`cor:exponent`正确给出

```text
log E_k(q_k)=-q_k log x+o(1).
```

若 `q_k log x/log k -> a in [0,infinity]`，则 polynomial exponent为 `-a`；
ratio趋 infinity时得到对每个 fixed `A`的 `o(k^(-A))`。这仍只是在 model变量
`k`上的 relative truncation accuracy。

令 target `epsilon_k=x^(-c)k^(-a)=x^(-t_k)`与 exact minimal width

```text
Q_k(a,c)=min{0<=q<=k-2:E_k(q)<=epsilon_k}.
```

positive weights使 tail严格递减，minimum eventually存在。`thm:inverse`对
`j=-1,0,1,2`逐项使用

```text
E_k(floor(t_k)+j)/epsilon_k=x^(theta_k-j)(1+o(1))
```

得到

```text
Q_k=t_k+O(1),
complete limit set of Q_k-t_k=[0,1].
```

只有 phase留在 `(0,1)`的 fixed compact subset时，才 eventually有
`Q_k=ceil(t_k)`；endpoint source remainder可决定相邻整数，论文没有越级声称
universal choice。

RH-355 clock只允许

```text
k=log(1/sigma)/(2log lambda)+O(1),
t_k=[a/log x]log log(1/sigma)
    +c-[a/log x]log(2log lambda)+o(1).
```

因此 `k^(-a)`换元后只是 `log(1/sigma)^(-a)`，不是 `X^(-a)`；RH 的动态
`sigma->0`也不是 selected packet固定 `sigma=1/10000`。形式选择
`a=1/400`绝不支付 TPC strict `1/400`。

### 44.4 proof integrity 与 conditional actual boundary

内部逐式结论为 `PASS`，`first_internal_fatal=NONE`。phase-density、四整数
bracket、cluster-set闭性、`a=0/infinity` endpoints与 physical clock换元均核对
成立。独立 strict JSON/producer reproduction及 finite certificate反算无 mismatch；
全部 5 gates与 15 forbidden claims仍 false。

actual tail只在同一 physical clock的未证假设

```text
D_(4k)(R)=sum_(2<=n<4k)|h_(sigma,n)-s_(k,n)|R^n/n ->0
```

下继承。RH-358给出的 uniform actual/deterministic multiplicative tail ratio足以
条件转移 phase、exponent与 minimal-width cluster comparisons；但不转移 roots、
rank、eigenvalues、determinant、RH-241/RH-288或 Gates A--E。

### 44.5 TPC literal coefficient、index 与 scale crosswalk

selected packet仍是

```text
sigma=1/10000, lambda=99979/210000, delta=7/60, beta=267/400,
Q=X^(267/400+o(1)), J=X^(133/400+o(1)), C=floor(J),
h0=2, N0=JQ^2 asymp XQ.
```

RH-359在第一字段即失败：

```text
LITERAL_PHYSICAL_COEFFICIENT_AND_INDEX_UNIVERSE_MISMATCH
```

具体地：

- `E_k(q)`是 RH-358 positive absolute trace-mass tail的再参数化与反演，没有
  新 signed coefficient；
- RH `q`是 terminal-window width，`Q_k(a,c)`是最小整数宽度，分别不是
  TPC `q_DFT`/direct `q`与 packet `Q=X^(267/400+o(1))`；
- `theta_k`是 floor remainder，不是 O161 named additive phase；
- 无 fixed physical `h0=2`、three raw channels、`G<=C`、canonical `Delta#`、
  content remainder、actual masks/weights/outer labels或 matched determinant zero；
- 无 `k,log(1/sigma)`到同一 packet `X,N0`的 coefficientwise ranges/constants/
  normalization map，`k^(-a)`不是 arithmetic power saving；
- TPC-111/122仍只有 finite Abel/BV duality与 conditional transfer，positive
  monotone tail不能冒充 growing signed-prefix cancellation；
- O161仍缺 `c_z=mu(d+sz)mu(u+az)`、physical `z`-order与 `q/N`或 `q/T`
  theorem；H1仍缺 source-cut address、actual occurrence edge与 lineage。

因此没有 `chi<=1/400`或 direct small-content matched-shell saving。

### 44.6 committed artifacts、schema 与 Windows portability

raw Git-object closure为：

```text
TREE_FILES/BYTES = 20 / 618171
PUBLICATION_FILES/BYTES = 18 / 616149
MANIFEST_MISSING/EXTRA/HASH_MISMATCH = 0 / 0 / 0
MANIFEST_KEY_SORTED_PATH_SIZE_HASH_AGGREGATE
  = af3875ad753a5c6cc0cd6eb9a2c1ac8ab82af9d67c8cc7e5cf4f96dbb818d48e
```

两 PDF是同一 Git blob：5页、277222 bytes、未加密、SHA-256
`f7dcb4b4d47dfb9a58480b47a0eba1a85c71eb716a88f91122f5d72bc3055682`；
可提取 9414 characters。未 render/visual QA，不声称视觉闭环。

三个 committed JSON strict/canonical且无 duplicate/nonfinite。`result.json`为
13631 bytes、16 top-level keys，recursive census为 21 dict、7 list、90 str、
58 bool、70 int，无 float/null；row groups为 `4/4/3`且非空唯一，5 gates与
15 false claims全为 strict false。

schema/verifier assurance仍 `PARTIAL`：result test复用 producer；verifier只遍历
manifest declared paths，不独立枚举 allowlist/核 file_count/path confinement/
digest schema；无独立 JSON Schema；writers未设 `allow_nan=False`。production
asserts为 0并有显式 raises，tests的 51 assertions未运行。

Windows `core.autocrlf=true`且无 `.gitattributes`。当前 18 publication files为
617804 bytes，16个文本相对 committed manifest mismatch，只有两 PDF匹配；
manifest-key POSIX/codepoint aggregate为
`62e9492acab911aabad1b8025f87923d18f9c63bda6b29b161029ba2494e674e`。
builder还会用 Windows反斜杠生成 manifest keys。因此 committed-tree closure为
PASS，但 checkout-byte archive不是跨平台确定的只读验证；本轮未重建。

### 44.7 exact stop、parents 与 reopen trigger

本轮新增且仅新增：

```text
DECLARED_REMOTE_RH359_LOGARITHMIC_TERMINAL_WINDOW_ACCURACY_THRESHOLDS_
TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED

RH359_DETERMINISTIC_LOG_WINDOW_THEOREM = PROVED
RH359_ACTUAL_HEAD_INHERITANCE = CONDITIONAL_ON_UNPROVED_D_(4k)(R)_TO_0
TPC32_O161_H1_RH359_20260804_LOGARITHMIC_TERMINAL_WINDOW_ACCURACY_THRESHOLDS_
FAIL_LITERAL_OBJECT_FIXED_H0_SIGNED_PREFIX_CONTENT_DETERMINANT_ACTUALITY_
X_SCALE_DIRECTION_OR_NORMALIZATION_GATES_NO_TRIGGER_STOP_SCOPED_PARENTS_OPEN
GROWING_TPC_SIGNED_PREFIX_THEOREM = ABSENT
DIRECT_SMALL_CONTENT_MATCHED_SHELL_SAVING = ABSENT
ARITHMETIC_ADVANCE = NONE
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节全部旧 cells保持 `STOP_SCOPED`。两个 O161 parents、TPC32
direct/fixed-`D0`/frame parents、pair-native reroute、H1、RH actual-head route与
global architecture保持 `OPEN`。合法 reopen仍须给同一 actual packet的 literal
coefficient、fixed `h0=2`、canonical signed prefix/content/`Delta#`、actual
metadata、one `N0` normalization与完整 loss ledger，并真正推出
`chi<=1/400`或 direct matched-shell saving；logarithmic-to-natural、model-`k`
to packet-`X`或 positive cumulative-to-signed prefix替换均禁止。

### 44.8 publication boundary

RH-359是新的 RH model-side theorem，不是 TPC arithmetic advance。本轮仍只允许
发布 `TPC_HANDOFF.md`；不得创建 TPC-207、论文、PDF或下一编号，也不得执行
TPC-27--32/TPC-122 writers。写入后重跑 22+4、diff/fence/protected manifest；
再次 fetch若出现 RH-360等 theorem delta，先审计再发布。remote稳定时只 stage
handoff，commit/push后核对 local `HEAD`、`origin/main`与 remote ref三 hash。

remote稳定时的 pre-commit closure为：

```text
RH359_POST_WRITE_BOOTSTRAP_REGRESSION = 22/22 PASS
RH359_POST_WRITE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
RH359_POST_WRITE_GIT_DIFF_CHECK = PASS
RH359_POST_WRITE_MARKDOWN_FENCES = 1202 MARKERS BALANCED
RH359_POST_WRITE_PROTECTED_UNTRACKED = 127 FILES
RH359_POST_WRITE_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = b979b87f85795a3cbb2cc4fc334f467355b0acc9
SUBAGENT_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
RH358_359_BUILDERS_VERIFIERS_TESTS_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md
```

## 43. 2026-08-04 RH-358 terminal-lag geometric localization 与 TPC literal-transfer 审计

### 43.1 late remote delta、rebase 与只读 envelope

第 42 节写入并完成 22/22 bootstrap、4/4 supplemental、diff/fence与
protected-manifest核对后，final fetch将 `origin/main`从 RH-357 tip推进至：

```text
a4fd6286c68fb3230e55d8465f89775f0f58fe15
  Add RH-358 terminal-lag geometric localization
```

delta严格为 `papers/RH-358-terminal-lag-geometric-localization/`下 20 个
new files；没有修改 TPC source、`TPC_HANDOFF.md`、`AGENTS.md`、`.codex`
或 scoped policy。主控先将第 42 节的唯一 tracked修改固定为本地协调 commit
`b32b2b9`，再在 tracked/cached clean、127 个 protected untracked不变时安全
rebase；当前协调 commit成为
`db7386695c61c3e5ed37f1ec1355c08495982075`，位于 RH-358 source commit之上。
没有 stash、reset、checkout、clean或删除任何用户文件。

三个 read-only分工分别审核 RH-358 source/TPC transfer、逐式 proof/quantifiers与
committed artifacts/schema/provenance，均锚定上述 source commit与 HEAD，并报告
`files_changed=[]`、`generated_outputs=[]`。主控另行读取全文并独立重建 Git blob
archive与关键 endpoint。没有运行 RH-358 builders/verifiers/tests；`pytest`在本
环境仍不可用，也没有安装依赖。

### 43.2 exact terminal ledger 与 strongest unconditional theorem

RH-358锁定 RH-17/RH-342与 RH-355--357的同一 deterministic counterloop：

```text
r_H=17/20, R=7/5, 28/17<lambda<17/10,
x=(R/r_H)^2/lambda>1,
y_k=x exp[-log(C_M)/k+o(1/k)],
B_k(L)=sum_(j=1)^L y_k^(k+j)/(k+j), 1<=L<=k-1.
```

定义 complete strict-upper budget、移除 top `q` terminal coordinates后的 lower
residual及 terminal-lag probability：

```text
C_k=B_k(k-1),
P_k(q)=B_k(k-1-q), 0<=q<=k-2,
pi_k(r)=[y_k^(2k-1-r)/(2k-1-r)]/C_k, 0<=r<=k-2.
```

这里 `q`明文只表示 terminal lag；不是项目中 direct/full-trace `q`，也不是
TPC modulus或 `q_DFT`。`prop:exact`精确给出

```text
P_k(q)/C_k=sum_(r=q)^(k-2) pi_k(r).
```

RH-358 `thm:uniform`无条件证明下式相对误差对全部整数
`0<=q<=k-2`一致：

```text
P_k(q)/C_k
 = y_k^(-q) (2k-1)/(2k-1-q)
   [1-y_k^(-(k-1-q))]/[1-y_k^(-(k-1))] (1+O(1/k))

 = x^(-q) C_M^(q/k) (2k-1)/(2k-1-q)
   [1-x^(-(k-1-q))]/[1-x^(-(k-1))] (1+o(1)).
```

`x^(-q)`单独不是 full-range uniform asymptotic；`C_M^(q/k)`、denominator
correction与 residual-depth factor都不得删去。`cor:regimes`正确区分：

```text
q=o(k):
  P_k(q)/C_k=x^(-q)(1+o(1));
q/k->theta in [0,1):
  P_k(q)/C_k~[2C_M^theta/(2-theta)]x^(-q);
q=k-1-ell, fixed ell>=1:
  P_k(q)/C_k~2C_M x^(-q)(1-x^(-ell)).
```

`prop:criterion`还精确证明，对每个 admissible sequence，

```text
P_k(q_k)/C_k -> 0  iff  q_k -> infinity.
```

固定 terminal window因此只保留极限 mass `1-x^(-q)`，不能捕获全部 budget。
若以后专门令 `q=floor(theta k+c)`并把 `x^(-q)`拆成 `x^(-theta k)`，floor
phase必须显式保留；RH-358没有做该替换，故当前定理没有 phase偷渡。

### 43.3 geometric localization 与 conditional actual inheritance

将 `pi_k`在 finite support之外补零，`thm:geometric`无条件证明

```text
pi_k -> pi(r)=(1-x^(-1))x^(-r) in ell^1,
d_TV(pi_k,pi)->0,
E_(pi_k) r -> 1/(x-1),
Var_(pi_k)(r) -> x/(x-1)^2.
```

moment convergence不是由 total variation越级推出。证明分别用
`2 r^m xi^(-r)`、`m=0,1,2`做 summable domination，真实支付 uniform
integrability。

actual Hardy-head只在同一 physical clock假设

```text
D_(4k)(R)
 = sum_(2<=n<4k)|h_(sigma,n)-s_(k,n)|R^n/n ->0
```

时继承。该 leaf仍未证明。条件下 reverse triangle inequality给 full/partial
budgets的 uniform relative error；最小 deterministic coordinate
`y_k^(k+1)/(2k-1)`指数增长，因而还可得到 uniform coordinatewise relative
control，再合法转移 `ell^1`与前两矩。这个论证不转移 roots、rank、spectrum、
determinant，不关闭 RH-241/RH-288或 Gates A--E。

### 43.4 proof、endpoint 与 source-stitch adversarial audit

内部逐式结论为 `PASS`，`first_internal_fatal=NONE`。关键 checks为：

- reverse geometric sum的最小 denominator为 `k+1`，weighted correction对全
  lag range一致 `O(1/k)`；
- `y_k>1` eventually，所有 probability/tail denominators正且一致远离零；
- `q=0`恢复 exact ratio `1`，`q=k-2`精确留下
  `B_k(1)=y_k^(k+1)/(k+1)`，无 endpoint collapse；
- 对 `2<=k<=400`、每个 `0<=q<=k-2`的独立纯内存 sweep未发现 denominator、
  probability normalization或 tail monotonicity失败；
- committed result的 exact、uniform-envelope、distribution、linear与
  residual diagnostics各 4 rows均可独立重建；没有把 finite rows升级为 theorem。

source stitching也保持同一 clock/object：RH-342固定 physical first-alias clock与
`s_(k,n)`，RH-17给 multiplier law与 `C_M>0`，RH-355给 complete upper band，
RH-357给同一 all-depth endpoint theorem。令 `L=k-1-q`时，linear-lag regime
正是 RH-357的 `alpha=1-theta`；fixed residual depth与 RH-356 fixed-`L`
numerator/RH-355 denominator一致。没有拼接 RH-354 actual coefficient、不同
normalization、multiplier branch或 actual/model source。

### 43.5 TPC32/111/122、O161 与 H1 literal crosswalk

selected packet仍严格固定为：

```text
sigma=1/10000, lambda=99979/210000, delta=7/60, beta=267/400,
Q=X^(267/400+o(1)), J=X^(133/400+o(1)), C=floor(J),
h0=2, N0=JQ^2 asymp XQ.
```

`delta=1/20` family继续是不可拼接的另一条 source lock。逐项 audit：

| gate | RH-358 literal object | TPC32/O161/H1 required object | verdict |
|---|---|---|---|
| physical coefficient | deterministic `s_(k,n)`的 positive absolute trace weights | TPC三 raw signed channels；O161 two-Mobius atom；H1 actual edge coefficient | `MISMATCH` |
| fixed atom | trace orders `4k-2-2r`，无 physical `h0` | fixed physical `h0=2` | `ABSENT` |
| domain/order | terminal lag `r,q`与 lower cumulative tail | actual affine fibers上的 canonical ordered signed prefixes | `MISMATCH` |
| determinant/content | 无 `G<=C`、canonical `Delta#`、content remainder或 DFT zero | same small-content matched-shell `Ahat_(C,q_DFT)(0)` | `ABSENT` |
| support/metadata | 无 actual masks、weights、outer labels或 source-cut address | complete actual metadata与 coefficientwise-conservative occurrence edge | `ABSENT` |
| ranges | `k,lambda,R,r,q` | selected `X,Q,J,C,N0`及全部 packet ranges | `NO_CROSSWALK` |
| normalization/loss | dimensionless `P_k(q)/C_k`；`x^(-q)`来自删正 mass | one original/global `N0` normalization与 signed saving | `MISMATCH / WRONG_OBJECT / UNPAID` |
| actuality | 仅条件于未证 `D_(4k)(R)->0` | unconditional same actual packet theorem | `CONDITIONAL_ONLY` |

第一处 fatal仍为：

```text
LITERAL_PHYSICAL_COEFFICIENT_AND_INDEX_UNIVERSE_MISMATCH
```

TPC-111/122只有 exact finite Abel/BV duality与 conditional transfer；growing
actual signed prefix、outer envelope、content remainder及 positive zero-mode
exponent都未证明。把 RH-358 constant-sign/absolute tail当成 cancellation正是
被 TPC-111排除的 unsigned-mass升级。`x^(-q)`是删除 terminal positive mass后的
relative truncation，不是 `N0`-normalized arithmetic cancellation。

O161要求 `c_z=mu(d+sz)mu(u+az)`、`su-ad=2`在 physical `z`-order上的
DIRECT `q/N` block或 BAD-ENDPOINT `q/T` cumulative prefix；RH terminal `q`
没有两 Mobius signs、named atom、phase、schedule或相应 normalization。H1也未得到
source-cut address、linear actual occurrence edge、exact edge weight、fixed `h0=2`
或 physical-normalization lineage；TPC-173 qualifying inventory仍为 0。

### 43.6 committed artifacts、schema、checkout portability 与 provenance drift

raw Git-object独立重建结果：

```text
TREE_FILES/BYTES = 20 / 717496
PUBLICATION_FILES/BYTES = 18 / 715498
MANIFEST_MISSING/EXTRA/HASH_MISMATCH = 0 / 0 / 0
MANIFEST_KEY_SORTED_PATH_SIZE_HASH_AGGREGATE
  = e8a6c37f6022b02b81c1c35d3bafde262efbe688d16867fff3ed121b05bf83fd
```

两份 PDF为同一 Git blob，6页、307752 bytes、未加密，SHA-256均为
`4d92ca82662534c0d7b1b33df1e178198f3422a97dba7de8bc1c7ac59a52023a`；
六页均可提取非空文本。本轮是 transfer gate而非编号 release，且严格禁止产生
输出，故未 render PNG或做逐页 visual QA；不得声称视觉闭环。

三个 committed JSON由独立 strict parser确认 duplicate/nonfinite均为 0。
`result.json`有 19 top-level keys、31 dict、6 list、196 str、70 bool、56 int，
无 float/null；五组 diagnostics各 4 个 nonvacuous unique rows，并覆盖 `q=0`、
`q=k-2`与 fixed residual endpoint。`gates`为 5/5 strict false，
`false_claims`为 14/14 strict false。

schema/verifier assurance仍仅 `PARTIAL`：无独立 JSON Schema/exact allowlist，
result test复用同一 `result_status()` producer；writers未设 `allow_nan=False`；
archive verifier使用普通 `json.loads`并复用 builder的 root/enumeration/digest；
manifest test只重哈希 declared paths，没有独立 expected-path allowlist。
production code无 `assert`、有显式 raise，因此没有直接 `python -O` production
bypass；但 71 个 test asserts未在 optimized mode或本环境执行。

Windows `core.autocrlf=true`且无适用 `.gitattributes`。当前 checkout的 18 个
publication files中 16个文本相对 committed manifest hash mismatch，只有两 PDF
匹配；worktree bytes为 717450。按 manifest-key paper-relative POSIX/codepoint
排序的 `path<TAB>size<TAB>sha256<LF>` aggregate为
`87d08ed78c8933faa069f76e87bb49f437575f5c4d296481f74c4a78a18a0915`。
所以 committed Git-tree archive closure为真实 PASS，但 checkout-byte verifier
在当前 Windows配置不可移植。运行 builder重绑环境 bytes不是对 committed
manifest的只读验证，本轮未这样做。

另有独立 coordination drift：当前 `RH_HANDOFF.md`页首仍把 RH-351写为 completed
endpoint、后文仍将 RH-352列为 default investigation，尚未吸收 RH-352--358。
这不推翻 RH-358 source theorem，但属于 RH-side handoff provenance ceiling；
TPC本轮无权静默重写该文件，只在此记录。

### 43.7 exact stop、开放 parents 与 reopen trigger

本轮新增且仅新增一个 source-specific cell：

```text
DECLARED_REMOTE_RH358_TERMINAL_LAG_GEOMETRIC_LOCALIZATION_
TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED

RH358_DETERMINISTIC_TERMINAL_LAG_THEOREM = PROVED
RH358_ACTUAL_HEAD_INHERITANCE = CONDITIONAL_ON_UNPROVED_D_(4k)(R)_TO_0
TPC32_O161_H1_RH358_20260804_TERMINAL_LAG_GEOMETRIC_LOCALIZATION_FAILS_LITERAL_
OBJECT_FIXED_H0_SIGNED_PREFIX_CONTENT_DETERMINANT_ACTUALITY_DIRECTION_OR_
NORMALIZATION_GATES_NO_TRIGGER_STOP_SCOPED_PARENTS_OPEN
GROWING_SIGNED_PREFIX_THEOREM = ABSENT
DIRECT_SMALL_CONTENT_MATCHED_SHELL_SAVING = ABSENT
ARITHMETIC_ADVANCE = NONE
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节全部旧 method cells保持 `STOP_SCOPED`，尤其 TPC193 V1、common-`k`
V1、tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1不重开。两个 O161
pointwise parents、TPC32 direct/fixed-`D0`/frame parents、pair-native reroute、
H1、RH actual-head route与 global architecture均保持 `OPEN`。

合法 reopen必须给出同一 actual selected packet的 coefficientwise theorem：同时
保留三 raw channels、fixed physical `h0=2`、canonical `Delta#`/content/prefix
order、actual masks/weights/outer labels、同一 `N0` normalization与完整
physical-loss ledger，并 source-backed推出 `chi<=1/400`或 direct small-content
matched-shell saving。positive absolute trace-mass localization、block/cumulative
tail或 terminal-window accuracy本身均不满足。即使局部 gate转正，仍须分别通过
all-`D` uniformity、exactly-once physical cover、original/global normalization、
tail-failure、A/B selection、actual packet attachment与完整 provenance cascade，
才可改变 TPC-207 trigger。

### 43.8 publication boundary

RH-358形成真实 RH model-side theorem，但没有 TPC theorem trigger。本轮仍只允许
发布更新后的 `TPC_HANDOFF.md`；不得创建 TPC-207、论文目录、PDF或下一编号，
也不得运行 TPC-27--32/TPC-122 writers。正式写入后重跑第 1 节全部 22项只读
回归、TPC-111/124/126/127四项 supplemental checks、`git diff --check`、
Markdown fence与 protected manifest；只 stage handoff。再次 final fetch若出现
新 remote theorem delta，必须先审计该 delta；remote稳定后才可 commit/push并
验证 local `HEAD`、`origin/main`、remote `refs/heads/main`三个 hash完全一致。

RH-359 late fetch出现前的只读 closure为：

```text
PRE_RH359_FETCH_BOOTSTRAP_REGRESSION = 22/22 PASS
PRE_RH359_FETCH_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
PRE_RH359_FETCH_GIT_DIFF_CHECK = PASS
PRE_RH359_FETCH_MARKDOWN_FENCES = 1168 MARKERS BALANCED
PRE_RH359_FETCH_PROTECTED_UNTRACKED = 127 FILES
PRE_RH359_FETCH_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
LATE_REMOTE_TIP
  = b979b87f85795a3cbb2cc4fc334f467355b0acc9
LATE_REMOTE_DELTA = RH359_ONLY_20_NEW_FILES
```

该 delta不修改 TPC/handoff/policy。第 43 节先固定为只含本 handoff的本地协调
提交，再安全 rebase取得 RH-359；不得把 RH-358的 `next_candidate` machine row
当作 RH-359 theorem evidence，必须对新 committed source重新执行同等级审计。

## 42. 2026-08-04 RH-356/357 post-alias depth profiles 与 TPC literal-transfer 审计

### 42.1 remote delta、启动 envelope 与 source lock

本轮按第 1 节从已发布的 TPC handoff commit
`599c5eac8ebc50700ce6395c252feaca6490c335`启动。tracked/cached diff均为空；
127 个既有 protected untracked files的 manifest保持：

```text
35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
```

`git pull --rebase origin main` 安全 fast-forward至：

```text
9cd3ad606826ad980600ec4eb0963296ea813308
  Add RH-356 post-first-alias mesoscopic crossover
45ba399d7b7abef39e4fcf17f916d3c6a159936c
  Add RH-357 uniform linear-depth counterloop profile
```

delta严格为 RH-356与 RH-357各 19 个、共 38 个 committed files；没有修改
TPC source、旧 handoff、`AGENTS.md`或 scoped policy。rebase后第 1 节完整
22/22只读启动回归通过，且未执行 TPC-27--32 legacy writers或 TPC-122
writer。三个 read-only分工分别锁定 RH-356 source、RH-357 source及两篇
proof/artifact/schema；它们均报告 `files_changed=[]`。本节所有数学判断重新来自
上述 commits的 source与 Git objects，不来自旧聊天记录。

两篇锁定同一个 deterministic graded counterloop：

```text
r_H = 17/20,  R = 7/5,  28/17 < lambda < 17/10,
sigma -> 0,  k = log(1/sigma)/(2 log lambda) + O(1),
|M_k| = C_M lambda^k(1+o(1)),
beta_k = |M_k|^(-1/(2k))/r_H,
beta = (r_H sqrt(lambda))^(-1),
x = (beta R)^2 > 1,
y_k = (beta_k R)^2
    = x exp[-log(C_M)/k + o(1/k)].
```

其 literal trace-order ledger为

```text
s_(k,n) = beta_k^n (2k 1_(2k|n) - 1 - (-1)^n),
A_k = |s_(k,2k)| R^(2k)/(2k) = (1-1/k)y_k^k,
B_k(L) = sum_(j=1)^L y_k^(k+j)/(k+j),  1 <= L <= k-1,
B_k(L)/A_k = [k/(k-1)] sum_(j=1)^L y_k^j/(k+j).
```

这是后续所有正结果和跨程序否定的共同 source lock；不得用 RH-354 的
actual coefficient `p=tau-a`、RH-355 shell或 TPC symbols替换它。

### 42.2 RH-356 的 sharp mesoscopic theorem

RH-356 `thm:uniform` 无条件证明：对每一个整数 envelope
`ell_k=o(k)`，下式对全部 `1<=L<=ell_k` 一致：

```text
B_k(L)/A_k
  = x(x^L-1)/(k(x-1)) (1+o(1)).
```

证明中的 `y_k^j/x^j` 与 `k/(k+j)`误差均在该量词下统一。固定
`L>=1`时必须保留 subtraction：

```text
k B_k(L)/A_k -> x(x^L-1)/(x-1).
```

只有同时 `L->infinity`且 `L=o(k)`时，才允许删去 finite-radius factor并写成

```text
B_k(L)/A_k
  = [x/(x-1)] x^(L-log_x k) (1+o(1)).
```

令 `delta_k=L-log_x k`，RH-356 `thm:crossover`给出 ratio在
`delta_k->-infinity,c,+infinity`时分别趋于 `0`、
`x^(c+1)/(x-1)`、`infinity`；连续 balance offset为
`log_x((x-1)/x)`。对整数

```text
L_k(c)=floor(log_x k+c),
theta_k(c)={log_x k+c},
```

`thm:integer-phase`保留

```text
B_k(L_k(c))/A_k
  = x^(c+1-theta_k(c))/(x-1) (1+o(1)),
phase limit set = [0,1],
liminf = x^c/(x-1),  limsup = x^(c+1)/(x-1).
```

因此不存在单一 full-sequence floor constant。physical noise clock上该
crossover只在 first alias以上
`n-2k=(2/log x)log log(1/sigma)+O(1)`个 trace orders处发生。逐式审计未发现
内部 theorem fatal；honest ceiling是 deterministic counterloop
`GO_SCOPED`。

### 42.3 RH-357 的 complete-band 与 linear-depth theorem

RH-357 `thm:uniform`从同一 exact ledger独立证明下式相对误差对全部整数
`1<=L<=k-1`一致：

```text
B_k(L)
  = y_k^(k+L+1)(1-y_k^(-L))
    /[(k+L)(y_k-1)] (1+O(1/k))
  = x^(k+L+1)(1-x^(-L))
    /[C_M^(1+L/k)(k+L)(x-1)] (1+o(1)),

B_k(L)/A_k
  = x^(L+1)(1-x^(-L))
    /[C_M^(L/k)(k+L)(x-1)] (1+o(1)).
```

terminal reverse sum的余项由可和的 `sum r x^(-r)`一致控制，且
`rho_k=k log(y_k/x)+log C_M ->0`允许对全部 `L/k`一致替换 source；误差不会在
`L=k-1`恶化。对任何给定序列 `L_k/k->alpha in (0,1]`，
`cor:linear`进一步给出

```text
B_k(L_k)
  ~ x^(k+L_k+1)/[C_M^(1+alpha) k(1+alpha)(x-1)],
B_k(L_k)/A_k
  ~ x^(L_k+1)/[C_M^alpha k(1+alpha)(x-1)],
kth-root rates = x^(1+alpha), x^alpha.
```

对应的 physical log-rates分别为
`(1+alpha)log x/(2log lambda)`与 `alpha log x/(2log lambda)`。
`L=floor(alpha k+c)`时必须保留 phase `theta_k={alpha k+c}`及
`C_M`/`1+alpha` factors；rational `alpha`给 finite periodic orbit，irrational
`alpha`给闭 phase interval。`alpha=1,c in [-1,0)`恢复 RH-355 complete upper
band；`alpha=0`是 RH-356 的独立 boundary，绝不能把 fixed positive
`alpha`结论假称为对 `alpha->0`一致。逐式审计也未发现内部 theorem fatal；
honest ceiling仍是 deterministic counterloop `GO_SCOPED`。

### 42.4 conditional actuality 与量词 firewall

两篇唯一的 actual Hardy-head transfer均显式假设同一 physical clock上的

```text
D_(4k)(R)
  = sum_(2<=n<4k) |h_(sigma,n)-s_(k,n)| R^n/n -> 0.
```

该 leaf尚未证明。只在此假设下，reverse triangle inequality才给
`A_k^H/A_k->1`、even `B_k^H(L)/B_k(L)->1`对完整允许带一致，且 odd actual
budget趋零。它没有转移 roots/rank，也没有证明 RH-241/RH-288、
direct-to-full closure或 Gates A--E。

以下 boundary均 fail closed：fixed `L`不得删 `x^L-1`；growing
mesoscopic law必须同时满足 `L->infinity,L=o(k)`；linear simplification只对固定
limit `alpha in (0,1]`；floor phase不得折叠；conditional actual statement不得升级为
unconditional actual theorem。RH-357 line 237将 physical clock简称为 RH-355
record，但 literal source chain直接由 RH-17/RH-342支撑，属于 locator精度问题，
不构成 theorem fatal。

### 42.5 TPC-111/122 与 selected-packet literal crosswalk

TPC source lock仍是同一个 theorem-valid selected packet：

```text
sigma=1/10000, lambda=99979/210000, delta=7/60, beta=267/400,
Q=X^(267/400+o(1)), J=X^(133/400+o(1)), C=floor(J),
h0=2, N0=JQ^2 asymp XQ.
```

`delta=1/20` truncated-entry family是另一条 source lock，绝不拼接。对
RH-356/357逐项执行七字段 audit如下：

| gate | RH-356/357 literal object | TPC32/O161/H1 required object | verdict |
|---|---|---|---|
| physical coefficient | `s_(k,n)`的 trace-order absolute budgets；`h_(sigma,n)`仅条件出现 | 同一 packet三条 signed raw channels；O161 literal two-Mobius atom；H1 actual cloud coefficient | `MISMATCH` |
| fixed physical atom | 没有 physical `h0`；`2k+2j`是 trace order | fixed physical `h0=2` | `ABSENT` |
| summation/prefix | `1<=j<=L`的 even upper trace orders，先取 absolute value | actual fibers上的 canonical ordered signed prefix | `MISMATCH` |
| determinant/content | 无 `G<=C`、canonical `Delta#`、DFT zero或 three-channel determinant | same small-content matched-shell `Ahat_(C,q)(0)` | `ABSENT` |
| support/metadata | 无 actual masks、weights、outer labels | 全部实际 support与 labels逐项保留 | `ABSENT` |
| parameter range | `k,sigma,lambda,R,L` | `X,Q,J,C,q,N0`及同一 packet ranges | `NO_CROSSWALK` |
| normalization/loss | `R^n/n`、`B/A`；linear root `x^alpha>1` | `N0=JQ^2 asymp XQ`与 `chi<=1/400`或 direct saving | `MISMATCH / WRONG_DIRECTION / UNPAID` |

第一处 fatal因此精确为：

```text
LITERAL_PHYSICAL_COEFFICIENT_AND_INDEX_UNIVERSE_MISMATCH
```

TPC-111/122只给 ordered signed-prefix的 finite duality/conditional transfer，
没有证明同一 actual fiber上的 growing signed-prefix saving。RH trace-order prefix
不能因其长度增长而改名成该对象；`B/A->0`只表示相对于指数大的 first alias的
relative crossover，不是 `N0`-normalized small-content saving。orbit Poisson zero、
nonzero-frequency density-one、Parseval与 complete-frequency mean仍均不能升级为
distinguished zero。

### 42.6 committed artifacts、checkout portability 与 schema ceiling

对 raw committed Git blobs的独立重建得到：

| release | tree/publication files | missing/extra/hash mismatch | publication bytes | sorted path-size-hash aggregate |
|---|---:|---:|---:|---|
| RH-356 | `19/17` | `0/0/0` | `629878` | `7755009f53aae9ee2e4f1d8e64eca6e669626bb4f395754ba2d3bd953b349da4` |
| RH-357 | `19/17` | `0/0/0` | `636717` | `96645e9d8f4c5eab1e290bc8f4c474112ee320392d5dfa17711fda71d7af8b5c` |

每篇两份 PDF分别 byte-identical；RH-356为 6页/285793 bytes、SHA-256
`c4ee68cab09965fea03157186b7d15819bcc513511df7186db7ae36c21b58eed`，
RH-357为 6页/280765 bytes、SHA-256
`7654b51731c2dbb6141e09e492b94d33a86c282ad216d949aa5fc4d2e702ebca`。
独立 exact-row/nonvacuity重建覆盖 RH-356全部 4 exact与 4 phase rows，及
RH-357全部 4 exact、4 error-envelope、4 linear diagnostics、3 rational phase
orbits；RH-357 envelope实际覆盖 116 个 depths并含 `L=1,k-1`。没有把 finite
diagnostic row升级为渐近 theorem。

当前 Windows checkout有 `core.autocrlf=true`，且这些 papers没有适用的 EOL
attribute。committed manifest锁的是 Git blob bytes；worktree中每篇 17 个
publication files里 15 个文本因 CRLF转换而 hash mismatch，只有两份 PDF保持。
RH-356 worktree为 631440 bytes、aggregate
`b49ec932f2f210608e60cc22accb11b4d4314bb397c7ae41672413296b9c75ac`；
RH-357为 638517 bytes、aggregate
`dd1afbf42182afafa8e93bb7548d4c2a5a84c0a2247490d390bc7680ef776226`。
所以 archive从 committed tree可复核，但现有 checkout-byte verifier在此 Windows
配置下不可移植；这是 provenance portability ceiling，不是数学 fatal。

当前 committed JSON由独立 strict parser确认无 duplicate keys/nonfinite values，
但 production producers未设 `allow_nan=False`，archive verifier使用普通
`json.loads`并与 builder共享 root/enumeration/digest，tests还复用 producer的
`result_status`；没有 whole-payload exact-key/type schema。因此 schema assurance仅为
`PARTIAL_ONLY`。production code无 `assert`；tests分别有 48与 59 个 assertions。
主控尝试只读 targeted pytest时在 collection前因环境无 `pytest`
（`No module named pytest`, exit 1）终止；没有安装依赖、没有运行 tests，且未生成
文件。builders/archive verifiers也未执行。

### 42.7 exact stop、开放 parents 与 reopen trigger

本轮新增且仅新增一个跨程序 cell：

```text
DECLARED_REMOTE_RH356_357_POST_ALIAS_COUNTERLOOP_DEPTH_PROFILES_
TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED

RH356_MESOSCOPIC_COUNTERLOOP_THEOREM = PROVED
RH357_COMPLETE_BAND_COUNTERLOOP_THEOREM = PROVED
RH356_357_ACTUAL_HEAD_INHERITANCE = CONDITIONAL_ON_UNPROVED_D_(4k)(R)_TO_0
TPC32_O161_H1_RH356_357_20260804_COUNTERLOOP_DEPTH_PROFILES_FAIL_LITERAL_OBJECT_
FIXED_H0_SIGNED_PREFIX_ACTUALITY_DIRECTION_OR_NORMALIZATION_GATES_NO_TRIGGER_
STOP_SCOPED_PARENTS_OPEN
TPC_ARITHMETIC_ADVANCE = NONE
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_TRIGGER = false
TPC207_CREATED = false
```

第 6 节全部旧 method cells保持 `STOP_SCOPED`，尤其 TPC193 V1、common-`k`
V1、tail-failure/A/B V1与 full-`r_Rr_R` ultra-complement V1不重开。两个 O161
pointwise parents、TPC32 direct/fixed-`D0`/frame parents、pair-native reroute、
H1、RH actual-head/direct-to-full与 global architecture均保持 `OPEN`；fixed-atom
credit仍为 0。

本 cell的合法 reopen必须给出同一 actual selected packet的 coefficientwise
theorem：同时保留三 raw channels、fixed physical `h0=2`、canonical
`Delta#`/content与 prefix order、actual masks/weights/outer labels、同一
`N0` normalization及完整 physical-loss ledger，并 source-backed推出
`chi<=1/400`或 direct small-content matched-shell saving。即使局部 gate转正，
仍须分别通过 all-`D` uniformity、exactly-once physical cover、original/global
normalization、tail-failure、A/B selection、actual packet attachment与完整
provenance cascade，才可改变 TPC-207 trigger。

### 42.8 publication boundary

RH-356/357是 RH program内真实 model-side advances，却没有形成 TPC theorem
trigger。本轮因此只允许发布更新后的 `TPC_HANDOFF.md`；不得创建 TPC-207、论文
目录、PDF或下一编号，也不得运行 TPC-27--32/TPC-122 writers。正式写入后必须
重跑第 1 节全部 22项只读回归、TPC-111/124/126/127四项 supplemental checks、
`git diff --check`、Markdown fence与 protected manifest；只 stage本 handoff。
最终 pull/rebase、push后必须验证 local `HEAD`、`origin/main`、remote
`refs/heads/main`三个 hash完全一致。

RH-358 late fetch出现前的只读 closure为：

```text
PRE_RH358_FETCH_BOOTSTRAP_REGRESSION = 22/22 PASS
PRE_RH358_FETCH_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
PRE_RH358_FETCH_GIT_DIFF_CHECK = PASS
PRE_RH358_FETCH_MARKDOWN_FENCES = 1138 MARKERS BALANCED
PRE_RH358_FETCH_PROTECTED_UNTRACKED = 127 FILES
PRE_RH358_FETCH_PROTECTED_MANIFEST
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
LATE_REMOTE_TIP
  = a4fd6286c68fb3230e55d8465f89775f0f58fe15
LATE_REMOTE_DELTA = RH358_ONLY_20_NEW_FILES
```

该 late delta不修改 handoff/TPC source/policy。为避免把旧 tip误报为最终 remote，
RH-356/357审计先固定为仅含本 handoff的本地协调提交，再安全 rebase取得 RH-358；
RH-358必须在后续最新节完成同等级审计后方可最终发布。

## 41. 2026-08-03 RH-355 upper-alias counterloop burden 与 conditional actual-head transfer 审计

### 41.1 late remote delta、source lock 与只读 envelope

RH-354/Watt/Palm/current-primary handoff 写入后，发布前执行
`git fetch origin main`，remote tip从本地
`50fccb3c281eb1f1376e47003f74a05ee8fef534`推进到：

```text
4706eba4b51b3cade9f907b3dd4c93a94683ddc8
  Add RH-355 upper-alias head-transfer burden
  19 new files, all under
  papers/RH-355-upper-alias-counterloop-burden-and-head-transfer-precision/
```

该 delta没有覆盖 TPC source、`TPC_HANDOFF.md`、`AGENTS.md`或 protected
untracked。本地 handoff当时已有 tracked diff，所以主控没有自动 stash或在脏树上
rebase；三路 read-only agents改从 commit `4706eba...` 的 raw Git blobs分别完成：

1. strongest theorem与 upstream source lock；
2. 逐式 proof/quantifier/normalization adversarial audit；
3. publication closure、JSON exactness、producer/checker independence与
   finite-fixture nonvacuity重建。

三路均报告 `files_changed=[]`、`generated_outputs=[]`，且未执行 RH builders、
verifiers或 tests。所有正式写入仍由主控完成。

本节及裁决字符串的 `2026-08-03`/`20260803` 标签按 RH-355 source commit
`2026-08-03T23:53:03+08:00` 与本次 audit batch的 source-lock日期记载；
不把跨午夜的本地墙钟差异解释为另一个数学审计版本。

### 41.2 strongest unconditional theorem 与 proof audit

RH-355 固定：

```text
r_H=17/20, R=7/5, 28/17<lambda<17/10,
|M_k|=C_M lambda^k(1+o(1)),
beta_k=|M_k|^(-1/(2k))/r_H,
beta=(r_H sqrt(lambda))^(-1),
x=(beta R)^2>1,
y_k=(beta_k R)^2=x exp[-log(C_M)/k+o(1/k)].
```

由 RH-342 的 exact graded counterloop ledger：

```text
Y_k={beta_k exp(+/- i j pi/k): 1<=j<=k-1},
s_(k,n)=sum_(nu in Y_k) nu^n
       =beta_k^n(2k 1_(2k|n)-1-(-1)^n).
```

在 strict upper trace-order band `2k<n<4k`，odd orders为零；写
`n=2m`、`k+1<=m<=2k-1`，则

```text
|s_(k,2m)|R^(2m)/(2m)=y_k^m/m.
```

因此 RH-355 无条件证明：

```text
C_k^up
  =sum_(2k<n<4k)|s_(k,n)|R^n/n
  =sum_(m=k+1)^(2k-1)y_k^m/m
  ~x^(2k)/(2 C_M^2 k(x-1)),

x^(-k)C_k^up
  ~x^k/(2 C_M^2 k(x-1)),

lim_(k->infinity)(x^(-k)C_k^up)^(1/k)=x>1.
```

terminal order `n=4k-2` 的 contribution `T_k`满足：

```text
x^(-k)T_k~x^(k-1)/(2 C_M^2 k),
T_k/C_k^up -> (x-1)/x.
```

逐式复核确认：`y_k` 的 `C_M` exponent、upper-band reindex、终端主项、
dominated-convergence majorant、terminal share与所有不等号方向都正确。这个
`GO_SCOPED` theorem的数学内容是 deterministic counterloop 的 normalized
absolute burden仍以 root `x>1` 增长；它是 obstruction/burden theorem，不是
cancellation或 saving theorem。

### 41.3 conditional actual-head firewall 与 normalized shortcut obstruction

定义 actual Hardy-head moments及 defect：

```text
h_(sigma,n)=sum_(mu in H_sigma)mu^n,
d_(sigma,k,n)=h_(sigma,n)-s_(k,n),
D_(4k)(R)=sum_(2<=n<4k)|d_(sigma,k,n)|R^n/n.
```

只有额外假设同一 physical clock上

```text
D_(4k)(R)->0
```

才推出 actual upper aggregate与 `C_k^up` asymptotic matching、odd upper
budget趋零，以及：

```text
max_(k+1<=m<=2k-1)
  |h_(sigma,2m)-s_(k,2m)|/|s_(k,2m)|=o(kx^(-k)),

|h_(sigma,4k-2)-s_(k,4k-2)|/|s_(k,4k-2)|=o(kx^(-2k)).
```

RH-355 明示没有证明 `D_(4k)(R)->0`。RH-354控制的是
`p=tau-a=q-d`，不是 `d`、`q`或 full `E_off`，所以两篇不得拼接成该输入。

较弱的 normalized condition

```text
Delta_k^up=x^(-k)sum_(2k<n<4k)|h_(sigma,n)-s_(k,n)|R^n/n ->0
```

只传递 normalized aggregate，并在 terminal给 `o(kx^(-k))`；它不推出
lower-to-upper uniform matching。RH-355 的 complete-shell construction取
`N_k=2k+2`，在 finite conjugation-closed normal information class中给出：

```text
relative defect at n=N_k = 1,
normalized defect ~x/(C_M k)->0,
raw defect ~x^(k+1)/(C_M k)->infinity.
```

这是真正的 normalized-shortcut obstruction，但不是 actual noisy operator、
actual rank law或 actual-head nonmatching theorem。finite executable rows只复现
exact formulas，不是 actual observation或 asymptotic experiment。

### 41.4 literal TPC32/O161/H1 crosswalk 与 first fatal

TPC source lock仍是第 28/32 节同一 theorem-valid selected packet：

```text
sigma=1/10000, lambda=99979/210000, delta=7/60, beta=267/400,
Q=X^(267/400+o(1)), J=X^(133/400+o(1)), C=floor(J),
h0=2, N0=JQ^2 asymp XQ.
```

`delta=1/20` truncated-entry family仍是另一条 source lock，不得拼接。
逐项 source/type audit为：

| gate | RH-355 object | TPC32/O161/H1 required object | verdict |
|---|---|---|---|
| literal coefficient | trace-order `s_(k,n)`、conditional `h_(sigma,n)`与 `d=h-s`；upper budget先取绝对值 | three raw channels的 matched `A_C`、O161 `mu(d+sz)mu(u+az)` actual coefficient，或 H1 actual GM-cloud coefficient | mismatch |
| fixed physical `h0` | even trace orders、`2k+2` shell order | prescribed arithmetic shift `h0=2` | absent |
| domain/prefix | complete strict upper trace-order band | canonical `Delta#`/content ordered signed prefix over actual outer fibers | mismatch |
| determinant/content | none | `G,Delta#,C`及 L/R metadata | absent |
| masks/weights/labels | no TPC row masks、weights或 `(alpha,gamma,j)` keys | actual masks/weights/outer labels且 exactly once | absent |
| parameters/uniformity | RH moving clock `sigma->0,k=k_sigma->infinity`；fixed `r_H,R,lambda,C_M`及 spectral cutoff `q_RH=1/2` | all `X,Q,J,D,C,q_DFT,q_prog` packet ranges uniform；TPC `q`不得与 `q_RH`混同 | mismatch |
| normalization | `R^n/n`、`x^(-k)` | `N0=JQ^2 asymp XQ`、O161 `q/N`,`q/T`及 original/global scale | absent |
| direction/loss ledger | normalized burden root `x>1`; actual input unproved | `chi<=1/400`或 direct same-object small-content saving及完整 physical losses | direction mismatch / unpaid |

第一处 fatal已经发生在：

```text
LITERAL_PHYSICAL_COEFFICIENT_AND_INDEX_UNIVERSE_MISMATCH.
```

它早于 fixed `h0`、prefix、normalization与 endpoint ledger，且后四项仍各自
独立失败。尤其不得把 even trace order中的数字 `2`改名为 physical
`h0=2`，不得把 upper absolute band改名为 ordered signed content prefix，
不得把 normalized defect convergence改写为 distinguished auxiliary zero，
也不得把 root `x>1` 的 burden改写成 small-content saving。

### 41.5 committed artifact、schema 与 provenance ceiling

从 commit `4706eba4b51b3cade9f907b3dd4c93a94683ddc8` 的 raw blobs独立重建：

```text
TREE_FILE_COUNT = 19
PUBLICATION_FILE_COUNT = 17
MANIFEST_DECLARED_FILE_COUNT = 17
MISSING = 0
EXTRA = 0
SHA256_MISMATCH = 0
PUBLICATION_BYTES = 622995
PDF_BYTE_IDENTICAL = true
SORTED_PATH_SIZE_HASH_AGGREGATE_SHA256
  = e123038ad0f33fb42468c34c4a6271699bf0bc9401d029c24bdc14f87b1d53f9
```

三个 JSON blobs以 strict duplicate-key/nonfinite parser读取时均干净且为
producer-deterministic sorted-key serialization。`result.json` 递归 census为 27 dict、5 list、
122 str、59 bool、28 int。当前数据没有 corruption；但 checker/provenance
ceiling必须保留：

1. result test与 producer共享 `result_payload()`；只有 `5/59` bool leaves
   使用 strict identity，余下 bool/int及 int/float可受 Python equality混淆；
2. archive verifier复用 builder的 root、enumeration与 digest helpers；manifest/
   verification没有 exact-key schema；
3. JSON consumers使用普通 `json.loads`，writers未设 `allow_nan=False`；
4. tests共 67 个 bare assertions，production asserts为 0；production core使用
   explicit exceptions，未发现 production `python -O` bypass；
5. RH-17/288/297/336/340/342/354 七个 upstream anchors是 narrative
   provenance，不在 manifest内作 cryptographic binding；外部 trust anchor是 Git。

四组 rational/synthetic rows均可由独立公式重现，complete-shell在所有
`k>=2`非空。这些 artifact结果支持 committed publication-tree reproducibility，不会把
conditional actual-head输入或 TPC transfer升级为定理。

### 41.6 精确裁决、开放 parents 与合法 reopen

第 6 节新增且仅新增：

```text
DECLARED_REMOTE_RH355_UPPER_ALIAS_COUNTERLOOP_BURDEN_AND_HEAD_
TRANSFER_PRECISION_TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

当前最窄裁决为：

```text
RH355_DETERMINISTIC_COUNTERLOOP_BURDEN_THEOREM = PROVED
RH355_ACTUAL_HEAD_MATCHING = CONDITIONAL_ON_UNPROVED_D_(4k)(R)_TO_0
RH355_FINITE_COMPLETE_SHELL = NORMAL_INFORMATION_CLASS_ONLY

TPC32_O161_RH355_20260803_COUNTERLOOP_BURDEN_CONDITIONAL_ACTUAL_HEAD_TRANSFER_
FAILS_LITERAL_OBJECT_FIXED_H0_PREFIX_DIRECTION_OR_NORMALIZATION_GATES_NO_TRIGGER_
STOP_SCOPED_PARENTS_OPEN

THEOREM_TRIGGER = false
ARITHMETIC_ADVANCE_FOR_TPC = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_CREATED = false
```

第 6 节全部旧 method cells仍 `STOP_SCOPED`。两个 O161 pointwise parents、
TPC32 direct/fixed-`D0`/full-cloud frame parents、pair-native reroute、H1 与
global architecture仍 `OPEN`；RH actual-head/direct-to-full gates也仍 `OPEN`。
更具体地，RH-241 moving noisy envelope、RH-288 activation、actual
rank/common-cap/rate root matching与 Gates A--E 均仍 `OPEN`；RH-355 没有为
其中任何一项提供 actual input。

本 RH-355 transfer cell或 TPC32 direct branch的合法 reopen必须给出同一 actual
selected packet的 coefficientwise theorem：
保留三 raw channels、actual masks/weights/outer labels、fixed physical `h0=2`、
canonical `Delta#`/content order与 `N0`，并 source-backed推出
`chi<=1/400`或 direct small-content matched-shell saving。即使局部 gate转正，
仍需分别通过 all-`D` uniformity、exactly-once physical cover、original/global
normalization、tail-failure、A/B selection、actual packet attachment与完整
provenance cascade，才可改变 TPC-207 trigger。
独立 O161、pair-native、H1 与 global routes仍分别遵循第 32.6--40.7 节的
route-specific triggers；本 RH-355 cell不向它们附加 TPC32-specific入口，
也不关闭它们。

### 41.7 publication boundary

RH-355 形成新的跨程序 source lock，但没有真实 TPC theorem trigger。本轮因此
只允许发布更新后的 `TPC_HANDOFF.md`；不得创建 TPC-207、论文目录、PDF或下一
编号，也不得运行 TPC-27--32/TPC-122 writers。最终 rebase、全链只读回归、
protected-untracked identity记录在本节的 release closure中；push之后才可取得的
local `HEAD`、`origin/main`、remote `refs/heads/main` 三 hash将在最终会话报告中
逐一验证，不在尚未存在的 commit内预写结果。

正式 rebase前的 fail-closed validation为：

```text
PRE_REBASE_BOOTSTRAP_REGRESSION = 22/22 PASS
PRE_REBASE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
PRE_REBASE_GIT_DIFF_CHECK = PASS
PRE_REBASE_MARKDOWN_FENCES = 1106 MARKERS BALANCED
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = 4706eba4b51b3cade9f907b3dd4c93a94683ddc8
POST_REBASE_BASE_ORIGIN_MAIN
  = 4706eba4b51b3cade9f907b3dd4c93a94683ddc8
POST_REBASE_PRE_CLOSURE_HEAD
  = f4ec77cfd9ddb1ab70293be314cca30bb054111c
POST_REBASE_RH355_TRACKED_FILES = 19
POST_REBASE_BOOTSTRAP_REGRESSION = 22/22 PASS
POST_REBASE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_REBASE_GIT_DIFF_CHECK = PASS
POST_REBASE_MARKDOWN_FENCES = 1106 MARKERS BALANCED
POST_REBASE_TRACKED_DIFF = EMPTY
POST_REBASE_CACHED_DIFF = EMPTY
POST_REBASE_PROTECTED_UNTRACKED_RECHECK = 127 FILES
POST_REBASE_PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
RH355_SUBAGENT_TASKS_COMPLETED = 3
TOTAL_SUBAGENT_TASKS_COMPLETED = 8
SUBAGENT_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
RH355_BUILDERS_VERIFIERS_OR_TESTS_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md
```

## 40. 2026-08-03 RH-354 parity-free direct tail、moving-level spectral candidates 与 current-primary delta

### 40.1 启动基线、remote delta 与 fail-closed envelope

本轮启动时的只读基线为：

```text
INITIAL_HEAD
  = 8ac9eb659a669f387327d5427727e51e9980d966
POST_PULL_HEAD
  = 50fccb3c281eb1f1376e47003f74a05ee8fef534
INITIAL_TPC_HANDOFF_SHA256
  = 59dede26dda40f3f189cdb0a0474b9dcbe819532b31624af091e0405394d1e63
INITIAL_BOOTSTRAP_REGRESSION = 22/22 PASS
INITIAL_TRACKED_DIFF = EMPTY
INITIAL_CACHED_DIFF = EMPTY
PROTECTED_UNTRACKED_COUNT = 127
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
```

`git pull --rebase origin main` 安全 fast-forward；唯一 delta 是
`50fccb3c281eb1f1376e47003f74a05ee8fef534` 的 19 个 RH-354 files，全部位于
`papers/RH-354-parity-free-near-alias-direct-tail-envelope/`。它没有覆盖
TPC source、本 handoff或根政策。本轮运行第 1 节 22 项只读 checker，
没有运行 TPC-27--32 legacy writers、TPC-122 writer或 RH builders/
verifiers。

主控把 RH-354 source lock、proof adversarial audit、artifact/schema
reconstruction，以及两路额外 primary-source scan交给四个 read-only agents。
全部回报同一 HEAD/handoff hash、`files_changed=[]`、
`generated_outputs=[]`；正式写入仍只由主控完成。

### 40.2 RH-354 strongest source-backed theorem

固定 RH physical clock与常数：

```text
r_H=17/20, q=1/2, R=7/5, 28/17<lambda<17/10,
beta=(r_H sqrt(lambda))^(-1), q_*=(r_H lambda)^(-1),
x=(beta R)^2>1,
sigma_k^(-1)=lambda^(2(k-eta_k)), sup_k |eta_k|<infinity.
```

RH-282/RH-267/RH-340 的 actual common-type source lock为

```text
p_(sigma,k,n)=tau_(sigma,n)-a_n=q_(sigma,k,n)-d_(sigma,k,n),
|tau_(sigma,n)| <= sigma^(-1) q^(n-2),
|a_n| < 48 q_*^n,  n>=2.
```

对任意 `0<=L_k<=2k-2`、`N_k=2k-L_k>=2`，定义

```text
W_k(L_k)=x^(-N_k/2) sum_(n>=N_k) |p_(sigma,k,n)| R^n.
```

令

```text
s=qR=7/10,
t=q_*R=28/(17lambda),
u=s/sqrt(x)=q r_H sqrt(lambda),
v=t/sqrt(x)=lambda^(-1/2),
rho_N=lambda^2 u^2=r_H^2 lambda^3/4,
rho_T=v^2=1/lambda.
```

`thm:W` 的 triangle/geometric-series 计算给出

```text
W_k <= [q^(-2) lambda^(-2eta_k)/(1-s)] rho_N^k u^(-L_k)
     + [48/(1-t)] rho_T^k v^(-L_k).
```

逐式审计确认两项几何级数、`rho_T<rho_N<1419857/1600000<1`、
bounded-phase prefactor与 `L_k=o(k)` 的 root passage全部成立，因而

```text
limsup_(k->infinity) W_k(L_k)^(1/k) <= rho_N < 1.
```

`cor:band` 的 logarithmic tail/band

```text
T_k=x^(-k) sum_(n>=N_k) |p_(sigma,k,n)| R^n/n,
B_k=x^(-k) sum_(N_k<=n<4k) |p_(sigma,k,n)| R^n/n
```

满足 `B_k<=T_k<=x^(-L_k/2)W_k/N_k`。`thm:frontiers` 对
`ell=limsup L_k/k` 正确给出

```text
limsup W_k^(1/k) <= max(rho_N u^(-ell),rho_T v^(-ell)),
limsup T_k^(1/k) <= max(rho_N s^(-ell),rho_T t^(-ell)).
```

`prop:critical` 在 `L_k=alpha_alias k+O(1)` 时给 `T_k=O(1/k)`。去掉
`x^(-k)` 后，separate noisy majorant的 root为

```text
lambda^2(qR)^2=x rho_N>9604/7225>1.
```

这只是 unnormalized source-cap method boundary，不是 actual `p` 的下界。
low prefix、same-clock head defect `d`、full `E_off`、RH-241/RH-288与
Gates A--E 仍 `OPEN`。

### 40.3 eventual 量词、uniform constants 与 nonvacuity

RH-282 `main.tex:33--37` 的 `M_sigma<=sigma^(-1)` 明示只对
``for sufficiently small sigma''。RH-354 `main.tex:91--94,150--159` 把它
引入 boxed finite-`k` bound时未重写该 qualifier。因此本轮的 fail-closed
最强裁决是：

```text
ALL_K_FINITE_BOUND_AS_LITERALLY_READ = NOT_SOURCE_BACKED
EVENTUAL_W_BOUND_FOR_ALL_SUFFICIENTLY_LARGE_K = PROVED
ROOT_THEOREM_AND_ASYMPTOTIC_COROLLARIES = UNAFFECTED
```

因为 `sigma_k->0`，此量词只影响有限多个初始 `k`。另外：

1. `1/(1-t)` 在 `lambda` 趋近开区间左端时发散，所以常数是
   fixed-`lambda`，不是整个 `28/17<lambda<17/10` 上一致；
2. finite prefactor依赖实际 bounded-phase bound，而 root ceiling不依赖它；
3. 显式非空 witness可取 `lambda=5/3`、`eta_k=0`、
   `sigma_k=lambda^(-2k)` 与 `L_k=0`或
   `floor(alpha_alias k)`；充分大 `k` 时 `N_k>=2`。

所以 RH-354 最大诚实级别是
`GO_SCOPED_ACTUAL_NORMALIZED_DIRECT_COEFFICIENT_ASYMPTOTIC_THEOREM`，不是
all-`k` finite certificate、signed cancellation theorem或 unnormalized closure。

### 40.4 literal TPC crosswalk 与 first fatal

仍 source-lock第 28/32 节同一 theorem-valid selected packet：

```text
sigma=1/10000, lambda=99979/210000, delta=7/60, beta=267/400,
Q=X^(267/400+o(1)), J=X^(133/400+o(1)), C=floor(J),
h0=2, N0=JQ^2 asymp XQ.
```

`delta=1/20` truncated-entry family仍是另一条 source lock，不得拼接。
逐字段对照为：

| gate | RH-354 actual object | TPC32/O161 required object | verdict |
|---|---|---|---|
| literal coefficient | `p=tau-a=q-d` | three raw channels的 matched `A_C`，或 `mu(d+sz)mu(u+az)` | mismatch |
| fixed physical shift | odd/even trace orders | prescribed prime shift `h0=2` | absent |
| prefix/index | `n>=2k-L_k` absolute tail | canonical ordered affine/content prefix | mismatch |
| determinant/content | none | `G,Delta#,C`, L/R, masks/weights, outer keys | absent |
| parameters | RH `q=1/2,k,sigma,lambda` | `X,Q,J,D,C,q_DFT,q_prog` | mismatch |
| normalization | `x^(-N_k/2)`/`x^(-k)` | `N0=JQ^2`, `q/N`, `q/T`, original/global scale | absent |
| endpoint ledger | RH root ceiling | all-`D`, cover, tail/A/B, attachment, provenance, strict `1/400` | unpaid |

第一处 fatal为

```text
LITERAL_PHYSICAL_COEFFICIENT_AND_INDEX_UNIVERSE_MISMATCH.
```

`parity-free` 只是 RH trace-order的 odd/even coverage；`near-alias` 只是
RH order band；`direct-tail` 只是 RH `p` 的 normalized absolute tail。任何一个
都不是 physical `h0=2`、TPC determinant/content fiber、ordered signed
prefix、named tail-failure或 distinguished zero。选 `n=2k,2k-2` 也不能把
trace-order gap `2` 改名为 prime shift `2`。

### 40.5 artifact、schema、independence 与 finite-fixture firewall

从 commit `50fccb3c281eb1f1376e47003f74a05ee8fef534` 的 raw Git blobs独立重建
publication closure：

```text
TREE_FILE_COUNT = 19
MANIFEST_DECLARED_FILE_COUNT = 17
INDEPENDENT_ELIGIBLE_BLOB_COUNT = 17
MISSING = 0
EXTRA = 0
SHA256_MISMATCH = 0
PDF_BYTE_IDENTICAL = true
COMMITTED_GIT_BLOB_ARCHIVE_SELF_CONSISTENT = YES
```

三个 committed JSON blobs 当前都是 zero duplicate keys、zero nonfinite
tokens。`result.json` 递归 census为 15 top-level keys、32 bool、16 int、57 str。
当前内容干净，但 schema/independence ceiling为：

1. file-backed tests只对 `4/32` bool leaves使用 strict identity；另 `28/32`
   在 producer/payload协调更改时可被 Python bool/int equality混淆；
2. 四个 finite rows的 `eta=0` 与 archive `failure_count=0` 共 5 个 zero-int
   leaves可与 `False` 混淆；
3. JSON writers未设 `allow_nan=False`，consumers使用普通 `json.loads`；
4. result checker与 producer共用 `result_status()`；archive verifier复用
   producer的 root/enumeration/digest helpers；外层不可变 binding是 Git commit；
5. tests共 66 个 bare asserts，production builder/verifier为 0；verifier使用
   explicit failure ledger与 `SystemExit(1)`，未发现 production `python -O` bypass。

finite fixtures明示只复现 rational identities/formulas，不是 `p,tau,a` 的
observation或 asymptotic evidence。这些 schema limitations不否定 RH-354 的
scoped theorem，也不产生 TPC map。

### 40.6 Watt/Palm source-specific backtrace 与 current-primary delta

对 moving-level actual-cloud parent的三个此前未冻结 source versions，逐 theorem-body
核对如下：

| source | strongest honest theorem | first fatal for actual cloud |
|---|---|---|
| Watt `1302.3112v1`, Theorem 1 `(1.9.12)--(1.9.16)` | `SL_2(C)` Gaussian congruence level、arbitrary cusp、`|p_V|<=P`的 cusp Fourier-coefficient spectral moments，含显式 cusp-width/level factor | ambient group与 literal operator mismatch；无 common norm-preserving map到 prescribed Dirac point evaluations |
| Watt `1302.3127v3`, Theorems 1--5/8--9 | fixed或 averaged Gaussian level的 exceptional-spectrum Fourier-coefficient moments | Fourier-frequency columns不是 points；部分 theorem还只 spherical或 level-averaged |
| Palm `1212.4282v1`, Theorem 3.2.1/Corollary 3.2.3 | 对 congruence index/level uniform的 mixed Weyl spectral count | global count不控制 prescribed local kernel、off-diagonal coherence或 cloud Gram norm |

因此第 6 节新增的 Watt/Palm cell只是 exact source/version lock，不是
新 method credit。一个 cusp Fourier expansion可以形式表示 point value，但 Jacquet/
Whittaker weights依赖 spectral parameter、`K`-type与 point；Watt theorem接收的
却是一个 fixed common frequency sequence。没有 source-backed intertwiner就不得从
前者推出后者。

另外的当日官方 arXiv 有限 delta覆盖 `math.NT/new` 29 项与
`math.DS/new` 22 项；去除 3 个跨分类重复后共 48 个 source/version
records。`2607.29275v1`与 `2607.29429v1` 已由第 35 节冻结。
唯一进入 theorem-body 复核的新邻近项是 Namazi
`arXiv:2607.29319v1` Theorem 1.3/Corollary 1.4/Theorem 4.8：它在固定
closed cocompact hyperbolic manifold的 `SO(n-1)` frame bundle上控制
`(-X_FM-z)^(-1)` resolvent并推出 smooth correlations的 exponential mixing。
nontrivial `K`-types本身不是 rejection；第一 fatal是

```text
FIXED_CLOSED_COCOMPACT_FRAME_FLOW_RESOLVENT_CORRELATION_IS_NOT_
MOVING_LEVEL_ARBITRARY_POINT_EVALUATION_CLOUD_GRAM_OR_BESSEL.
```

它是第 37 节已有 fixed closed/full-group source cell的严格实例，故只记录
source/version与 exact fatal，不新建同义 method cell。该有限检索不是全球
literature nonexistence claim。

### 40.7 精确裁决、开放 parents 与合法 reopen

本轮新增且仅新增第 6 节的两个 source-specific cells：

```text
DECLARED_REMOTE_RH354_PARITY_FREE_NEAR_ALIAS_ACTUAL_DIRECT_TAIL_
TO_TPC_LITERAL_OBJECT_TRANSFER_V1 = STOP_SCOPED

DECLARED_TPC32_20260803_WATT_GAUSSIAN_CUSP_FOURIER_LARGE_SIEVE_
AND_PALM_UNIFORM_MIXED_WEYL_SOURCE_CANDIDATES_V1 = STOP_SCOPED
```

当前裁决为：

```text
RH354_EVENTUAL_NORMALIZED_DIRECT_TAIL_ROOT_THEOREM = PROVED
RH354_ALL_K_BOXED_W_BOUND = NOT_SOURCE_BACKED_WITHOUT_EVENTUAL_QUALIFIER

TPC_LITERAL_COEFFICIENT_MAP = ABSENT
TPC_FIXED_PHYSICAL_H0_2 = ABSENT
TPC_ORDERED_SIGNED_PREFIX = ABSENT
TPC_DISTINGUISHED_ZERO_SAVING = ABSENT
TPC_ORIGINAL_GLOBAL_NORMALIZATION = ABSENT

TPC32_O161_RH354_20260803_ACTUAL_NORMALIZED_PARITY_FREE_DIRECT_TAIL_
FAILS_LITERAL_OBJECT_FIXED_H0_PREFIX_OR_NORMALIZATION_GATES_NO_TRIGGER_
STOP_SCOPED_PARENTS_OPEN

THEOREM_TRIGGER = false
ARITHMETIC_ADVANCE_FOR_TPC = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_CREATED = false
```

第 6 节全部旧 method cells仍 `STOP_SCOPED`；两个 O161 pointwise
parents、TPC32 direct/fixed-`D0`/full-cloud frame parents、pair-native reroute、
H1 与 global architecture仍 `OPEN`。合法 reopen必须首先给出同一
actual TPC object的 literal theorem：或 source-backed growing signed-prefix theorem
并支付 `chi<=1/400`，或 direct small-content matched-shell saving，或
level-uniform noncompact full-group actual-cloud full/cross-`D0` Gram theorem。

即使此一局部 gate未来转正，仍须分别通过 all-`D` uniformity、
exactly-once physical cover、original/global normalization、tail-failure、
A/B selection、actual packet attachment、完整 provenance cascade与 strict
`1/400` payment，才可改变 TPC-207 trigger。本轮没有创建论文、
paper directory、PDF或 TPC-207。

RH-354/Watt/Palm 写入完成、但尚未发现 RH-355 remote delta时的只读快照为：

```text
PRE_RH355_FETCH_BOOTSTRAP_REGRESSION = 22/22 PASS
PRE_RH355_FETCH_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
PRE_RH355_FETCH_GIT_DIFF_CHECK = PASS
PRE_RH355_FETCH_MARKDOWN_FENCES = 1076 MARKERS BALANCED
PRE_RH355_FETCH_PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
PRE_RH355_FETCH_SUBAGENT_TASKS_COMPLETED = 5
SUBAGENT_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
RH354_BUILDERS_OR_VERIFIERS_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md
```

## 39. 2026-08-03 RH-353 actual boundary phase-free gap 与 TPC literal-transfer 审计

### 39.1 final remote delta 与 source lock

在仅含 handoff 的 coordination commit准备阶段，最后一次只读
`git fetch origin main` 又将 remote tip从
`2724ec0242915c8089212fef0a95f0a0de7bc892`推进到：

```text
bc53f19066eee6032d6cb5850b1c2031453f5893
  Add RH-353 boundary signed-completion gap
  19 new files, all under
  papers/RH-353-critical-first-lower-actual-signed-completion-gap/
```

该 delta没有覆盖 TPC source、`TPC_HANDOFF.md`、`AGENTS.md`或根 scoped policy。
本节从 `origin/main` 的 committed Git blobs只读审核，不运行 RH builders、tests或
archive verifier。source lock为 `main.tex` 的：

```text
eq:critical, eq:lower, eq:tau-a, eq:source-caps,
thm:cap, thm:completion, thm:gap, cor:supply.
```

### 39.2 strongest honest RH theorem 与 proof audit

RH-353在 RH-352 growing lower-even window之外处理两个 boundary orders。固定同一
bounded-phase physical clock及 RH constants

```text
r_H=17/20, q=1/2, R=7/5, 28/17<lambda<17/10,
beta=(r_H sqrt(lambda))^(-1),
q_*=(r_H lambda)^(-1),
x=(beta R)^2>1,
H_l=l R^(-2l), m=k-1.
```

两个 actual direct coefficients与 remainders为：

```text
p_k^0=p_(sigma,k,2k)
     =tau_(sigma,2k)-a_(2k)
     =Y_k^0+P_k^0-S_k^0,

p_k^-=p_(sigma,k,2k-2)
     =tau_(sigma,2k-2)-a_(2k-2)
     =Y_k^-+P_k^--S_k^-.
```

RH-282/RH-267的 same-source caps

```text
|tau_(sigma,n)| <= sigma^(-1)q^(n-2),
|a_n| < 48q_*^n
```

经 `thm:cap` 对 `l=k,k-1` 合法 specialization后给：

```text
V_k=max(
  |p_k^0|/(2H_k x^k),
  |p_k^-|/(2H_(k-1) x^(k-1)) ),

limsup V_k^(1/k)
  <= max(r_H^2 lambda^3/4,1/lambda)<1.
```

这里 `k`换成 `k-1`只改变 fixed factors，proof仍是 separate absolute caps加
triangle inequality。定义

```text
gamma_k=C_*C_M lambda^(eta_k),
Z_k^0=C_M Y_k^0/(2H_k x^k),
Z_k^-=C_M Y_k^-/(2H_(k-1) x^(k-1)).
```

critical与 first-lower source laws以及 `p` natural-scale smallness给
`thm:completion`：

```text
Z_k^0=2-gamma_k+o(1),
Z_k^-=1-gamma_k/lambda+o(1).
```

两项使用同一个 physical phase scalar；`thm:gap`精确消去它：

```text
Z_k^0-lambda Z_k^- -> 2-lambda > 3/10,

liminf max(|Z_k^0|,|Z_k^-|)
  >= (2-lambda)/(1+lambda) > 1/9.
```

leading affine minimax constant在
`gamma_*=3lambda/(1+lambda)`处达到。因 `x>1`，`cor:supply`进一步严格给：

```text
liminf [C_M/x^(k-1)] max(
  |Y_k^0|/(2H_k),
  |Y_k^-|/(2H_(k-1)) )
  >= (2-lambda)/(1+lambda)>1/9.
```

逐式 adversarial audit没有发现内部 proof fatal：同一 clock、共同 phase、两个
`o(1)`、minimax inequality及 `x>1` scale conversion均一致。故必须承认 RH-353
在 RH program内是非空的 `GO_STRICT_SCOPED_THEOREM`。它真实补上 RH-352排除的
`j=0,1` boundary coordinates，并证明 actual `Y` pair不能同时小。

严格边界同样重要：maximizing coordinate可以随 `k`切换；结论是 actual `Y`
signed supply的下界，不是 direct `p`的下界或 upper-bound saving。source明确保持：

```text
p_k^0=o(H_k) = OPEN
p_k^-=o(H_(k-1)) = OPEN
ODD_AND_UPPER_ALIAS_ORDERS = OPEN
FULL_E_OFF_AND_HEAD_TRANSPORT = OPEN
RH288_AND_GATES_A_TO_E = OPEN
```

### 39.3 TPC crosswalk、方向审计与 first fatal

表面上 `2k`与 `2k-2`相差 `2`、且 theorem “phase-free”，但这两点都不是 TPC
physical interface。逐字段结果为：

| TPC requirement | RH-353 object | exact mismatch |
|---|---|---|
| literal coefficient | `p=tau-a`及 `Y=T^rest-d` | 无 O161 `mu(d+s*z)mu(u+a*z)`、TPC32 three raw channels、matched `A_hat_(C,q)(0)`、GM cloud、pair或 H1 coefficient map |
| fixed physical `h0=2` | trace orders `2k,2k-2` | order-index difference `2`不是 arithmetic determinant/prime shift；没有 source-backed intertwiner |
| prefix/domain | 两个 boundary coordinates的 switching maximum | 不是 growing ordered prefix、same-fiber order、matched shell或 named fixed atom |
| theorem direction | `max(|Z0|,|Z-|)`的严格正下界 | 不是 distinguished-zero/small-content upper-bound saving；方向相反 |
| modulus/ranges | frozen RH `q=1/2`, `k,sigma,lambda` | 不是 TPC `q_prog=as`、`q_DFT`、`X,Q,J,C,D` ranges |
| normalization | `2H_l x^l`与 `x^(k-1)` | 无 `N0=JQ^2 asymp XQ`、`q/N`、`q/T`或 original/global physical normalization |
| packet metadata | 无 `G,Delta#`, L/R, masks/weights或 outer keys | content、determinant、actual attachment与 exactly-once cover均缺 |
| endpoint ledger | RH fixed positive constants | 无 `P_X`、all-`D` uniformity、tail/A/B losses或 strict `1/400` payment |

第一处 fatal仍是：

```text
LITERAL_PHYSICAL_COEFFICIENT_AND_INDEX_UNIVERSE_MISMATCH.
```

即使反事实补上该 map，仍有三个独立 fatal：

```text
TWO_COORDINATE_SWITCHING_MAX_IS_NOT_ORDERED_SIGNED_PREFIX
LOWER_BOUND_ON_Y_IS_NOT_SAVING_FOR_AHAT_CQ_ZERO
RH_X_TO_TPC_N0_NORMALIZATION_MAP = ABSENT
```

不得把 phase elimination升级为 TPC prescribed phase theorem，不得把 trace-order
gap `2`改名为 physical `h0=2`，也不得把至少一个坐标大的 switching maximum记为
named fixed atom。fixed-atom credit仍为 0。

### 39.4 artifact、schema、independence 与 nonvacuity audit

从 commit `bc53f19066eee6032d6cb5850b1c2031453f5893` 的 raw Git blobs独立重建
publication closure并逐个计算 SHA-256：

```text
MANIFEST_DECLARED_FILE_COUNT = 17
INDEPENDENT_ELIGIBLE_BLOB_COUNT = 17
MISSING = 0
EXTRA = 0
SHA256_MISMATCH = 0
COMMITTED_GIT_BLOB_ARCHIVE_SELF_CONSISTENT = YES
```

当前三个 committed JSON blobs均有 zero duplicate keys、zero nonfinite tokens。
`result.json`递归 census为 15 top-level keys、31 bool、0 int、66 str。schema与
independence ceiling为：

1. file-backed checker只对 5/31 bool leaves使用严格 `is True/False`；另 26 个在
   producer/payload协调修改时可接受 Python `bool/int`等值替换；
2. `archive_verification.failure_count=0`用 `==0`检查，可与 `False`混淆；普通
   `json.loads`允许 last-wins duplicate keys与 `NaN/Infinity`，writers未设置
   `allow_nan=False`；
3. result checker与 producer共享 `result_status()`；archive verifier复用 producer的
   root、enumeration与 digest helper。manifest/verification records不自哈希，外层
   immutable binding是 Git commit，不是可重生成的 manifest；
4. tests有 63 个 bare assert lines，production builder/verifier有 0 个；verifier用
   explicit failure ledger与 `SystemExit(1)`，未发现 production `python -O` bypass。

这些限制不改变 paper theorem，也不产生 TPC map。nonvacuity witness可取
`lambda=5/3`、`sigma_k=lambda^(-2k)`、`eta_k=0`；充分大 `k`时 orders `2k`与
`2k-2`都在 source cap的 `n>=2` domain。finite fixtures只复现 affine/minimax
formulas，明确不是 `p,Y,tau` observation或 asymptotic evidence。

### 39.5 精确 cell、TPC 裁决与合法 reopen

RH-353新增且仅新增：

```text
DECLARED_REMOTE_RH353_CRITICAL_FIRST_LOWER_ACTUAL_PHASE_FREE_
SIGNED_COMPLETION_TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

```text
RH353_ACTUAL_BOUNDARY_NATURAL_SCALE_CAP = PROVED
RH353_ACTUAL_PHASE_FREE_Y_GAP = PROVED
RH353_ACTUAL_SWITCHING_COORDINATE_Y_SUPPLY = PROVED

TPC_LITERAL_COEFFICIENT_MAP = ABSENT
TPC_ORDERED_SIGNED_PREFIX = ABSENT
TPC_DISTINGUISHED_ZERO_SAVING = ABSENT
TPC_FIXED_ATOM = ABSENT
TPC_ORIGINAL_GLOBAL_NORMALIZATION = ABSENT

TPC32_O161_RH353_20260803_ACTUAL_BOUNDARY_PHASE_FREE_RH_GAP_FAILS_
LITERAL_OBJECT_FIXED_H0_PREFIX_OR_NORMALIZATION_GATES_NO_TRIGGER_
STOP_SCOPED_PARENTS_OPEN

THEOREM_TRIGGER = false
ARITHMETIC_ADVANCE_FOR_TPC = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_CREATED = false
```

本 cell只停止跨程序改名/拼接，不停止 RH 自身路线。只有未来 source同时给出
literal coefficientwise RH/TPC map、fixed physical `h0=2`、same-packet
determinant/content/labels/masks、prescribed growing prefix、correct `X/N0`
normalization、uniform constants及完整 loss ledger，才可重开。

第 6 节全部旧 method cells仍 `STOP_SCOPED`；两个 O161 pointwise parents、TPC32
direct/fixed-`D0`/frame parents、pair-native reroute、H1与 global architecture仍
`OPEN`。即使本 transfer cell转正，也仍须分别通过 all-`D` uniformity、
exactly-once physical cover、tail-failure、A/B selection、actual packet attachment、
完整 provenance与 strict `1/400` payment，才可能改变 TPC-207 trigger。

### 39.6 发布边界

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入仅为
`TPC_HANDOFF.md`；三个 RH-353 subagents均以 `files_changed=[]`结束。最终 rebase、
post-rebase regressions与 protected manifest为：

```text
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_AMEND
  = bc53f19066eee6032d6cb5850b1c2031453f5893
FINAL_SYNC_DELTA_FROM_INITIAL_992FE4F
  = RH352_TO_RH353_38_RH_ONLY_FILES
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
POST_REBASE_BOOTSTRAP_REGRESSION = 22/22 PASS
POST_REBASE_TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_REBASE_GIT_DIFF_CHECK = PASS
POST_REBASE_MARKDOWN_FENCES = 1030 MARKERS BALANCED
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
SUBAGENT_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
RH351_TO_RH353_WRITERS_OR_VERIFIERS_EXECUTED = NO
EXPECTED_TRACKED_RELEASE_FILE = TPC_HANDOFF.md
```

final handoff amend后还须再次执行上述只读 checks与 protected manifest；push前再次
`git pull --rebase origin main`。push后必须验证 local `HEAD`、`origin/main`、remote
`refs/heads/main`三个 hash完全一致。

## 38. 2026-08-03 RH-352 actual normalized ladder theorem 与 TPC literal-transfer 审计

### 38.1 late remote delta、source lock 与审核边界

第 37 节写入期间的只读 `git fetch origin main` 将 remote tip从
`992fe4fc1f6fbb54163f8d7bd10e498762d028b5`推进到：

```text
2724ec0242915c8089212fef0a95f0a0de7bc892
  Add RH-352 modulus-cap signed cancellation
  19 new files, all under
  papers/RH-352-modulus-cap-forced-growing-ladder-signed-cancellation/
```

该 commit没有覆盖 TPC source、`TPC_HANDOFF.md`、`AGENTS.md`或根 scoped policy。
因本 handoff已有 tracked修改且政策禁止自动 stash，正式整合必须等本 handoff形成
单独 coordination commit后再用 `git pull --rebase origin main`完成；数学审核直接从
`origin/main` 的 committed Git blobs读取，不运行任何会写 RH artifacts的 builder或
verifier。

本节 source lock固定为 RH-352 `main.tex` 的以下 exact interfaces：

```text
eq:tau-bound, eq:a-bound, eq:p-tau-a, eq:p-YPS,
thm:uniform-cap, cor:L, thm:Y-tracking, cor:Yagg,
eq:raw-root, eq:raw-superunit, eq:scale-conversion.
```

`result.json`、`THEOREM_LEDGER.md`、`README.md`与 executable fixtures只作为
claim/artifact cross-check；数学强度以 committed theorem body及其逐式证明为准。

### 38.2 RH-352 的 strongest honest theorem

固定 RH physical parameters与 clock：

```text
r_H=17/20, q=1/2, R=7/5, 28/17<lambda<17/10,
beta=(r_H sqrt(lambda))^(-1),
q_*=(r_H lambda)^(-1),
H_m=m R^(-2m), x=(beta R)^2,
eta_k=k-log(1/sigma_k)/(2 log lambda), sup_k |eta_k|<infinity,
J_k->infinity, J_k=o(k), J_k>=3,
m_(k,j)=k-j, n_(k,j)=2m_(k,j), 2<=j<=J_k.
```

actual direct coefficient有两个 source-locked表示：

```text
p_(k,j)=tau_(sigma,2m_(k,j))-a_(2m_(k,j))
       =Y_(k,j)+P_(k,j)-S_(k,j),
Y_(k,j)=T_(k,m_(k,j))^rest-d_(sigma,k,2m_(k,j)).
```

RH-282 与 RH-267 分别给：

```text
|tau_(sigma,n)| <= sigma^(-1) q^(n-2),
|a_n| < 48 q_*^n.
```

定义

```text
U_k=sup_(2<=j<=J_k)
    |p_(k,j)|/(2 H_(m_(k,j)) x^(m_(k,j))),
rho_N=r_H^2 lambda^3/4,
rho_T=1/lambda.
```

`thm:uniform-cap`通过分别估计 `tau` 与 `a` 后使用 triangle inequality，严格证明：

```text
limsup_(k->infinity) U_k^(1/k)
  <= max(rho_N,rho_T)<1,
rho_N<1419857/1600000,
rho_T<17/28.
```

这是真正 uniform于 growing `J_k=o(k)` window的 actual coefficient theorem；
`J_k`产生的 factor只有 `exp(o(k))`，不是把有限多个 fixed-`j` limits升级而来。
由此 `cor:L` 对 actual normalized selected direct budget

```text
L_k^act=x^(-(k-2))
        sum_(j=2)^(J_k) |p_(k,j)|/(2H_(m_(k,j)))
```

给出相同 root ceiling及指数趋零。再用 exact identity `Y=S-P+p` 与 RH-350 的
uniform `S/P` laws，`thm:Y-tracking`、`cor:Yagg`得到：

```text
sup_j | C_M Y_(k,j)/(2H_m x^m)
        -(1-a_k lambda^(2-j)) | -> 0,

Yagg_k^act
  =x^(-(k-2)) sum_j |Y_(k,j)|/(2H_m)
  =F_(J_k-2)(a_k)/C_M+o(1),

liminf Yagg_k^act
  >= [1/(x-1)-1/(x lambda-1)]/C_M > 0.
```

因此必须承认：RH-352 是 RH program内真实
`GO_STRICT_SCOPED_THEOREM`；它无条件关闭 actual normalized selected direct
budget，并否定 RH-350 的 actual aggregate small-`Y` hypothesis。它不是 RH-351
formal completion的重复包装，也不是 conditional physical model。

同一 source也明确给出 method boundary。去掉 `x^m` 后，noisy separate-modulus
majorant的 uniform root为

```text
lambda^2(qR)^2 > 9604/7225 > 1.
```

所以不能把 normalized theorem乘回被移除的 `x^k` 并声称 unnormalized selected
prefix趋零。unnormalized actual verdict、full off-alias aggregate、RH-288及 Gates
A--E仍 `OPEN`。

### 38.3 TPC literal-object crosswalk 与 first fatal

RH 标题中的 “signed cancellation” 不等于 TPC ordered signed-prefix theorem。
RH-352 的 proof input是两个 separate absolute modulus caps，输出也是
`sup |p|` 与 absolute selected budget；它不建立 prescribed phase上的 prefix
cancellation。逐字段 crosswalk为：

| required TPC field | RH-352 actual field | exact result |
|---|---|---|
| literal physical coefficient | `p=tau-a=Y+P-S`，trace/noisy-operator coefficient | 不是 O161 `mu(d+s*z)mu(u+a*z)`，也不是 TPC32 three raw channels、matched `A_hat_(C,q)(0)`或 actual GM cloud coefficient |
| fixed physical `h0=2` | `n=2m` lower-even trace order | factor `2` 是 operator/trace order doubling，不是 physical shift；`FAIL` |
| summation domain/prefix index | `2<=j<=J_k`, `m=k-j`, `J_k=o(k)` | 不是 TPC-111/122 ordered `z`/archive prefix，也没有 same-fiber order-preserving map |
| modulus/ranges | RH spectral contraction `q=1/2`, `k,sigma,lambda` | 不是 TPC modulus `q_prog=as`、`q_DFT`或 packet `Q`; ranges不可换名 |
| normalization | local `2H_m x^m`、aggregate `x^(k-2)` | 没有 `N0=JQ^2 asymp XQ`、DIRECT `q/N`、BAD `q/T`或 original/global packet normalization |
| determinant/content/labels | 无 `G,Delta#`, content cutoff `C`, L/R polarization或 outer keys | distinguished determinant zero与 matched shell未出现 |
| actual masks/weights | RH lower-even window indicator | 无 TPC structured residual mask、row coefficients、smooth/periodic factors或 actual packet attachment |
| uniform constants/loss ledger | RH rates只依赖 frozen RH constants | 无 all-`D`、tail-failure、A/B selection、`P_X`或 strict `1/400` ledger |

因此跨程序的第一个 fatal为：

```text
LITERAL_PHYSICAL_COEFFICIENT_AND_INDEX_UNIVERSE_MISMATCH.
```

在这个 fatal后，ordered prefix、determinant/content、actual masks、normalization与
physical-loss ledger又分别失败。不得把 RH 的 orbit/operator zero、absolute
normalized budget、complete-window bound或 aggregate law改写为 TPC distinguished
zero；也不得将 RH-351 的 formal close/far ledger与 RH-352 actual normalized
theorem拼接出一个不存在的 TPC coefficientwise intertwiner。

```text
RH352_ACTUAL_NORMALIZED_GROWING_THEOREM = YES
RH352_UNNORMALIZED_SELECTED_PREFIX_THEOREM = NO_OPEN
RH352_PHASE_SENSITIVE_SIGNED_PREFIX_THEOREM = NO
RH352_TO_TPC_LITERAL_COEFFICIENT_INTERTWINER = ABSENT
RH352_TO_TPC_SMALL_CONTENT_MATCHED_SHELL_SAVING = ABSENT
RH352_TO_TPC_STRICT_1_OVER_400_PAYMENT = ABSENT
```

### 38.4 artifact、schema、independence 与 nonvacuity audit

RH-352 的 dependency manifest列出 17 个 publication files。本轮从 commit
`2724ec0242915c8089212fef0a95f0a0de7bc892` 逐个读取 raw Git blob并独立计算
SHA-256，结果为：

```text
MANIFEST_DECLARED_FILE_COUNT = 17
COMMITTED_BLOBS_REHASHED = 17
MISSING = 0
EXTRA_MANIFEST_ROWS = 0
SHA256_MISMATCH = 0
```

两个 PDF的 blob digest相同；manifest与当前 committed archive
self-consistent。没有用 Windows checkout bytes替代 Git blobs，也没有执行
RH builders、tests或会重写 JSON的 archive verifier。

当前三个 committed JSON blobs没有 duplicate keys或 nonfinite numeric tokens；
但 schema/provenance ceiling为：

1. `result.json`递归类型 census为 16 个 top-level keys、32 bool、15 int、79 str、
   0 float；file-backed tests只有 5/32 bool leaves使用严格 identity/type约束，另
   27 个在协调修改 producer/payload时仍可能接受 Python `bool/int`等值替换；
2. `archive_verification.json.failure_count=0`与 `False`等值；普通
   `json.loads`没有 duplicate-key hook或 `parse_constant` rejection，writers也没有
   `allow_nan=False`；
3. result test与 producer共享 `result_payload()`；archive verifier从 producer共享
   digest/enumeration helper。dependency manifest与 archive verification record不在
   自己的 17-file manifest内，也没有 independently pinned outer root；真正外部绑定
   仍是 Git commit；
4. tests中有 65 个 bare `assert`，production builder/verifier paths没有 bare
   `assert`，失败使用 explicit condition/raise/exit；未发现 production `python -O`
   bypass。

这些弱点限制 executable certificate的独立 schema强度，但不推翻 paper theorem。
反向 vacuity check也通过：source允许例如 `lambda=5/3`、`eta_k=0`、
`J_k=max(3,floor(sqrt(k)))`，committed fixtures在 `k=64,144,256`给出非空 growing
coordinate rows；theorem domain不是空集，`max(rho_N,rho_T)<1`不是 vacuous branch。

### 38.5 精确 cell、TPC 裁决与合法 reopen

本轮针对 RH-352 新增且仅新增：

```text
DECLARED_REMOTE_RH352_MODULUS_CAP_FORCED_GROWING_LOWER_EVEN_
SIGNED_CANCELLATION_TO_TPC_LITERAL_OBJECT_TRANSFER_V1
  = STOP_SCOPED
```

该 cell只冻结把 RH-352 actual normalized theorem改名或拼接为 TPC literal
coefficient、distinguished determinant zero、ordered signed prefix或 physical
`1/400` payment。它不冻结 RH program内部进展，也不阻止未来真正 source-backed
coefficientwise RH/TPC intertwiner。

```text
TPC32_O161_RH352_20260803_OMITTED_MOBIUS_FULL_GROUP_K_TYPE_AND_
ACTUAL_NORMALIZED_RH_LADDER_BACKTRACE_FAILS_LITERAL_OBJECT_MOVING_LEVEL_
OR_NORMALIZATION_GATES_NO_TRIGGER_STOP_SCOPED_PARENTS_OPEN

THEOREM_TRIGGER = false
ARITHMETIC_ADVANCE_FOR_TPC = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_CREATED = false
```

第 6 节全部旧 method cells保持 `STOP_SCOPED`，尤其 TPC193 V1、common-`k` V1、
tail-failure/A/B V1、full-`r_R r_R` ultra-complement V1及第 23 节 signed-prefix
transfer V1。两个 O161 pointwise parents、TPC32 direct/fixed-`D0`/frame parents、
pair-native reroute、H1与 global architecture继续 `OPEN`。

只有新 source同时给出下列 data，才允许重开本 transfer cell：

1. literal coefficientwise map把 RH actual `p_(k,j)`送到同一 TPC packet的 exact
   raw coefficient，并保留 fixed physical `h0=2`、determinant/content、outer labels、
   masks/weights与 prefix order；
2. 显式证明 RH `k,j,m,x,H_m` 与 TPC `X,N0,Q,J,q` 的 full range及 normalization
   intertwiner，uniform constants不随 hidden packet data恶化；
3. 在该同一 physical object上给出 growing phase-sensitive signed-prefix theorem或
   direct small-content matched-shell saving，并支付完整 loss ledger与 strict `1/400`。

即使本 local transfer gate将来转正，也不自动创建 TPC-207。all-`D` uniformity、
exactly-once physical cover、original/global normalization、tail-failure、A/B
selection、actual packet attachment、完整 provenance与页首 theorem trigger仍必须
分别发生真实 source-backed状态变化。

### 38.6 发布边界

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入仅为
`TPC_HANDOFF.md`；全部 protected untracked保持原样且不得纳入提交。最终 sync、
post-rebase regressions与 protected manifest的最终记录见第 39.6 节。

## 37. 2026-08-03 omitted O161、full-group K-type、row-reversal 与 RH-351 delta 审计

### 37.1 启动、上游 delta 与冻结接口

本轮启动前 status只有既有 protected untracked；tracked/cached diff均为空。
`git pull --rebase origin main` 将本地从
`f60ee11346b129eb7775366edb72c5c35aa4bcab` 安全 fast-forward 到
`992fe4fc1f6fbb54163f8d7bd10e498762d028b5`。delta严格为：

```text
99d9fad06d44843ac24b9ccdb15bda09179cccf6
  Add RH-351 signed-completion frontier review
  23 new RH-351 files

992fe4fc1f6fbb54163f8d7bd10e498762d028b5
  Update RH handoff through RH-351
  RH_HANDOFF.md only
```

没有上游文件覆盖 TPC source、`TPC_HANDOFF.md`或根 scoped policy。设置
`PYTHONDONTWRITEBYTECODE=1` 后，第 1 节全部只读启动回归为 `22/22 PASS`；
没有执行 TPC-27--32 legacy JSON writers或 TPC-122 writer。

同一 theorem-valid selected packet继续冻结为：

```text
sigma=1/10000, lambda=99979/210000, delta=7/60, beta=267/400,
Q=X^(267/400+o(1)), J=X^(133/400+o(1)), C=floor(J),
h0=2, N0=JQ^2 asymp XQ.
```

`delta=1/20` truncated-entry family仍是另一条 source lock，绝不可拼接。

### 37.2 O161 两项 omitted-primary theorem-body source lock

两个 pointwise parents的 literal core与 normalization仍分别是：

```text
c_z=mu(d+s*z)mu(u+a*z), su-ad=2,
q=as, t(z)=ad+qz, (a,s)=1, as odd.

DIRECT:
  (q/N) sum_(N<t(z)<=2N)
    c_z rho_phys(z) e(-alpha_star*z).

BAD local ancestor:
  (q/N_j) |sum_(N_j<t(z)<=2N_j)c_z rho_star(z)|
    <= C X^(-sigma),
  N_j=T/2^j in E_X_star;
  only then may TPC-159 telescope to q/T.
```

有限 current-primary delta新增两个此前未显式登记的近邻：

| source/version | source-backed strongest statement | first fatal for O161 |
|---|---|---|
| Frantzikinakis--Host `arXiv:1804.08556v3`, Theorem 1.3/Corollary 1.4 | fixed unit-slope shifts `prod_i f_i(n+h_i)` 对 totally ergodic zero-mean deterministic sequence不相关；固定 irrational additive twist只给 logarithmic convergence | 只接受 fixed `n+h_i`，不接受 growing `d+s*z,u+a*z`；输出是 logarithmic、qualitative、无 fixed power、actual atom或 `q/N`/`q/T` contract |
| He--Liu--Ma `arXiv:2604.16840v1`, Theorems 1.1--1.3 | 一个 `mu(n)` 对特定 Furstenberg flow observable 的 short-interval `o(M)`；rational-flow branch给 `M/log^A N` | literal coefficient只有一个 Mobius；没有 theorem把 `mu(u+a*z)` realization成该 observable。flow denominator也不是 `q=as`；无 `su-ad=2`、growing affine uniformity、actual packet或 fixed-power ledger |

逐项结果为：

```text
LITERAL_TWO_MOBIUS_COEFFICIENT = FAIL
FIXED_PHYSICAL_H0_2 = ABSENT_AS_THEOREM_PARAMETER
NATURAL_TERMINAL_OR_SCHEDULED_ANCESTOR_DOMAIN = FAIL
GROWING_A_S_D_U_Q_RANGES = ABSENT
UNIFORM_CONSTANTS = ABSENT
Q_OVER_N_OR_Q_OVER_T_NORMALIZATION = FAIL
NAMED_PRODUCTION_ATOM_AND_ACTUAL_MASKS = ABSENT
FIXED_POWER_AND_COMPLETE_LOSS_LEDGER = ABSENT
```

不得把 Frantzikinakis--Host 的 correct-product/wrong-logarithmic-domain branch与
其他 natural theorem拼接，也不得把 He--Liu--Ma 的 one-Mobius theorem通过选择
一个含第二个 Mobius sign的 observable升级成 binary arithmetic theorem。
2026-08-03 official `math.NT/new` 的 29 项 listing没有另一个 post-第 36 节
O161 survivor；random multiplicative `2607.29429v1` 已由第 34.5 节旧 cell冻结。
这只是有限扫描结论，不是全局文献不存在性声明。

### 37.3 full-group/nontrivial-`K` actual-cloud source backtrace

actual GM interface不是 ordinary spectral family mean。它要求：

```text
Gamma_pm(q)={gamma in SL_2(Z): gamma=plus-or-minus I (mod q)},
B_t=[[m,(m*j+2)/G],[n,(n*j+2)/G]],
H_t=2*|m-n|/G,
g_t=H_t^(-1/2)*B_t^+ in SL_2(R),

E1 <= P_X sum_t |a_t|^2,
P_X <= X^(1/400-kappa_row-epsilon+o(1)),
0<kappa_row<1/400.
```

每个 `a_t`还必须保留 opened-row signs、fixed `h0=2`、三 raw channels、
`G,Delta#`、actual masks、matched shell、smooth/periodic factors、outer labels与
one global `N0` normalization。source必须覆盖 first-slot identity self-kernel、
full/cross-`D0` blocks、全部 relevant right-`K` types与 moving level ranges。

本轮不以“有 K-type”误杀候选；exact theorem-body结果是：

| source/version | 真正接近之处 | first fatal与后续 object mismatch |
|---|---|---|
| Ramacher--Wakatsuki `arXiv:1703.06973v3`, Proposition 3.3、Remark 3.4(1)、Proposition 4.1、Theorems 5.5/5.8/7.4 | 确有 full `Gamma\\G`、reduced spectral kernel与 nontrivial `SO(2)` K-types；Theorem 5.8覆盖 `SL_2(R)` | 基本假设是 fixed closed/cocompact arithmetic quotient；actual `Gamma_pm(q)\\SL_2(R)` 是 moving finite-volume cuspidal quotient。结论是 smoothed spectral/Hecke kernel或单 eigenfunction point bound，不是 arbitrary literal Dirac-cloud Gram；无 moving-level uniform constants、cross-`D0`或 `N0/P_X` ledger |
| Blomer--Harcos--Maga--Milicevic `arXiv:2107.05973v3`, Theorems 1--3/Remark 2 | non-spherical K-type supnorm与 amplified pre-trace | fixed `SL_2(C)`, `SU(2)`, `SL_2(Z[i])`；文中 `q` 是 K-type component，不是 TPC level。结论是 compact-set per-eigenform supnorm，不是 actual cloud Bessel/Gram theorem |
| Cekic--Lefeuvre `arXiv:2405.14846v2`, Theorems 5.1.5/5.1.8/5.1.10、Proposition 5.3.8、Lemma 5.3.10 | compact principal-bundle horizontal spectral theory、local Weyl与 density-one quantum ergodicity | 该 `G` 是 fixed closed base上的 compact structure group，不是 ambient `SL_2(R)`；输出是 eigenfamily count/average，不是 prescribed point cloud，且没有 level、literal coefficient、cross-`D0`或 physical normalization |

Ramacher--Wakatsuki 的 entrywise reduced-kernel bound若只用 Schur/Cauchy搬到任意
cloud，会引入 cloud-cardinality loss。仓库已有 fixed-`D0` common-translation 与
`G=1` cross-`D0` compact collision families；它们不证明 actual coefficients同时
非零或 coherent，故不是 large-energy反例，但足以阻止偷加 separation。

```text
MOVING_NONCOMPACT_LEVEL_QUOTIENT_THEOREM = ABSENT
LITERAL_ACTUAL_CLOUD_COEFFICIENT_ATTACHMENT = ABSENT
ACTUAL_CLOUD_SEPARATION = ABSENT
FULL_SELF_KERNEL = UNCONTROLLED
CROSS_D0_BLOCK_BESSEL = ABSENT
ORIGINAL_GLOBAL_NORMALIZATION = ABSENT
P_X_TINY_POWER_LEDGER = UNPAID
```

### 37.4 same-packet row-reversal不是 sign-reversing involution

唯一自然且此前未逐式排除的候选是

```text
iota:(alpha,gamma,j,u,v,nu,L/R)
  -> (gamma,alpha,j,v,u,nu',R/L).
```

它在 set level交换两个 mixed channels、固定 both-ultra、保持 cutoff tensor与
content，并使 `Delta#_(gamma,alpha)=-Delta#_(alpha,gamma)`。但 literal amplitude

```text
a_sh_(alpha,gamma,j)
  = gamma_alpha^(1) gamma_gamma^(2)
    A_(alpha,gamma)(j) K_sh_(alpha,gamma)(j)
```

被送到

```text
gamma_gamma^(1) gamma_alpha^(2)
A_(gamma,alpha)(j) K_sh_(alpha,gamma)(j).
```

TPC-25/32只给两 row families与 joint multiplier的 bounded/off-diagonal provenance，
既没有相等关系，更没有负相等关系。更早的 sign fatal为：

1. exact matched polarization是 `C_m H_n + H_m C_n`，中间是加号；
2. each-leg Mobius fusion各给一个负号，two-leg raw channel得到两个负号后仍为正；
3. orientation sign只在 determinant argument中，`A_hat_C,q(0)` 的 phase恒为 1；
4. TPC-93必须保留 opposite row、content与 L/R polarization outer keys；swap跨过
   distinct TPC-111/122 canonical prefix fibers，不能作为 fiber内 order-preserving pairing。

故即使反事实强加 symmetric outer coefficients，row-reversal通常是 double而不是
cancellation。TPC-124的 growing archive/matrix intertwiner仍不存在，`N0`到
`Q_X^2` normalization也未证。

```text
GENUINELY_NEW_SIGN_REVERSING_INVOLUTION = NO
LOSSLESS_A_C_ZERO_TO_SIGNED_PREFIX_MAP = ABSENT
GENUINELY_NEW_OPEN_SUBLEMMA = NONE
```

这严格落在第 23 节已有 literal-coefficient/fiber-intertwiner STOP scope中；本轮
没有给它另注册一个换名 method cell。

### 37.5 RH-351 literal type、artifact 与 schema/provenance audit

RH-351 的 exact source object是

```text
p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j),
m_(k,j)=k-j, 2<=j<=J_k, J_k->infinity, J_k=o(k),
Y_actual=T_(k,m_(k,j))^rest-d_(sigma,k,2m_(k,j)).
```

对任意 formal residual array `r`，algebraic completion
`Y=S-P+r` 确实给 `p=r`。因此同一 proved `S/P` arrays有

```text
close: Y=S-P, p=0,
far:   Y=0,   p=P-S,
Yagg(close)=L(far),
Yagg(far)=L(close)=0,
liminf L(far)>0.
```

这是 RH program内真实的 growing-depth coefficient-ledger information-class
theorem，不得误报为 model-only。可是 paper与 RH handoff都明确：两个 completions
不是 physical noisy operators、Markov kernels、raw trace partitions或 determinant
realizations；在 RH-351 source boundary内，actual `Y` family完全未估。所以它只
证明当时的 deterministic/scalar premises不决定 physical selected-window verdict。
RH-352 后来在 RH 自己的 normalized selected-ladder scale上估计 actual `Y`；该后续
事实与仍缺的 TPC literal crosswalk另见第 38 节。

跨到 TPC 时第一个 fatal仍是：

```text
LITERAL_PHYSICAL_COEFFICIENT_AND_INDEX_UNIVERSE_MISMATCH
```

RH 的 trace-order coefficient、moving `m=k-j`、doubling `n=2m`、absolute-residual
budget与 `x^(-(k-2))/(2H_m)` normalization，不是 O161 `z` prefix，也不是 TPC32
three raw channels、fixed physical `h0=2`、`G/Delta#`、actual GM cloud、42-field
pair或 H1 edge。RH 的 factor `2`仍是 trace order doubling，不得改名为 physical shift。

artifact audit另确认：RH-351 dependency manifest的 19 个 committed Git blobs为
`19/19` SHA-256 self-consistent。当前 Windows checkout设置 `core.autocrlf=true`，
17 个 text working-tree files因 LF/CRLF conversion与 raw-byte manifest hash不同，
两个 PDF不受影响；这是 checkout-byte portability，不是 committed blob变化，也不是
数学证据。没有运行会写 verification JSON的 RH builders/verifiers。

schema/provenance反方审计得到：

1. 五个 committed JSON blobs当前均无 duplicate key或 nonfinite token；
2. `result.json` 有 80 个 bool leaves，但 file-backed tests只有两个字段用严格
   `is True/False`；其余 78 个主要依赖 `data==result_payload()`、truthiness或
   `not any(...)`，在 producer与payload协调变更时不拒绝 Python `bool/int`
   等值替换；三个 zero integer counters也可与 `False`混淆；
3. ordinary `json.loads` 没有 duplicate-key hook或 `parse_constant` rejection；
   manifests/verification records也没有 exact-key schema；
4. result checker导入同一 `result_payload()` producer，archive verifiers又从
   `build_archive.py`共享 `digest/paper_directories/publication_files`；两个 manifests
   不自哈希且没有外部 root digest，所以证明的是 current-tree self-consistency，
   不是独立 theorem witness；
5. pytest共有 69 个 bare assertions，但 production/verifier paths用 explicit
   raises/conditionals与 `SystemExit(1)`；未发现 production `python -O` bypass。

这些是 schema/provenance ceiling。它们不推翻 RH-351 的 paper-level exact algebra，
也不提供 physical realization、actual growing signed-remainder theorem或任何 TPC
literal transfer。

### 37.6 精确裁决、状态防火墙与合法 reopen

本轮新增三个且仅三个 source-specific cells：

```text
DECLARED_O161_20260803_OMITTED_FH1804_HLM2604_
NATURAL_GROWING_TRANSFER_CANDIDATES_V1 = STOP_SCOPED

DECLARED_TPC32_20260803_FULL_GROUP_K_TYPE_SPECTRAL_PROJECTOR_
SUPNORM_AND_PRINCIPAL_BUNDLE_LOCAL_WEYL_SOURCE_CANDIDATES_V1
  = STOP_SCOPED

DECLARED_REMOTE_RH351_AFFINE_SIGNED_COMPLETION_TO_TPC_
LITERAL_OBJECT_TRANSFER_V1 = STOP_SCOPED
```

row-reversal没有新 method cell；第 6 节全部旧 cells继续 `STOP_SCOPED`，尤其
TPC193 V1、common-`k` V1、tail-failure/A/B V1、full-`r_R r_R`
ultra-complement V1与第 23 节 signed-prefix V1。

```text
O161_LITERAL_NATURAL_GROWING_FIXED_POWER_THEOREM = ABSENT
ACTUAL_FULL_GROUP_MOVING_LEVEL_CLOUD_FRAME_THEOREM = ABSENT
SAME_PACKET_SIGN_REVERSING_INVOLUTION = ABSENT
RH351_TO_TPC_LITERAL_CROSSWALK = ABSENT
PAIR_NATIVE_42_FIELD_PRODUCTION_RECORD = ABSENT
H1_LINEAR_OCCURRENCE_EDGE = ABSENT

TPC32_O161_RH351_20260803_OMITTED_MOBIUS_FULL_GROUP_K_TYPE_AND_
SIGNED_COMPLETION_BACKTRACE_FAILS_LITERAL_OBJECT_MOVING_LEVEL_OR_PREFIX_
GATES_NO_TRIGGER_STOP_SCOPED_PARENTS_OPEN

THEOREM_TRIGGER = false
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_CREATED = false
```

两个 O161 pointwise parents、TPC32 direct/fixed-`D0`/frame parents、pair-native
reroute、独立 pre-TT-star H1与 global architecture继续 `OPEN`。有限扫描不声称
全局文献不存在。

只在出现下列新的 source-backed输入时重开对应 parent：

1. 直接接受 O161 literal growing two-Mobius coefficient、actual packet/masks、
   prescribed phase及正确 `q/N` terminal domain并给 fixed positive-power error；
   或逐 ancestor满足 BAD `q/T` telescoping contract；
2. 直接作用于 moving noncompact `Gamma_pm(q)\\SL_2(R)` actual Dirac cloud、
   全部 relevant K-types、full/cross-`D0` blocks与 literal weights的 level-uniform
   frame/Gram theorem，并在 one global `N0` normalization支付所需 `P_X`；
3. 同一 selected packet上 source-backed anti-equivariant literal involution，逐项保留
   determinant、content、outer labels、prefix order、coefficient、mask/weight与
   normalization；或直接证明 `A_hat_C,q(0)`/small-content matched-shell saving；
4. actual RH `Y_(k,j)` theorem与一个真正 literal coefficientwise RH/TPC crosswalk；
5. same-source complete 42-field production pair、pair-to-`omega`与四阶段
   normalization，或从 named upstream cut正向给出 linear H1 occurrence edge。

任一 local gate转正仍不自动创建 TPC-207。all-`D` uniformity、exactly-once
physical cover、original/global normalization、tail-failure、A/B selection、actual
packet attachment、完整 provenance与 strict `1/400` payment必须分别通过，并使
页首 trigger发生真实 theorem-backed状态变化。

## 36. 2026-08-03 O161 affine-Mobius、actual-cloud frame 与 pair/H1 delta 回溯

### 36.1 基线、范围与只读分工

本轮启动时 HEAD 为
`cc9e047a196bd1e96fe472cfbaf5b0beb5399466`，`TPC_HANDOFF.md` 的启动
SHA-256 为
`7bbd94275dca8ed19e731db1538f0464fb3bdc742c32fa9a1b340b9aa4e783e7`。
working tree没有 tracked/cached diff；只有五个本地 `.codex` 文件、TPC-105
`__pycache__`、TPC-63 构建产物与 `tmp/`。启动
`git pull --rebase origin main` 返回 already up to date；第 1 节 22 项只读启动
回归为 `22/22 PASS`。TPC-27--32 legacy writers与 TPC-122 writer均未执行。

主控读取页首及第 1、6、22、24、35 节，冻结同一 high-beta selected packet、
O161 literal source contract、actual GM cloud与 pair/H1 schemas。三个 read-only
agents分别完成：

```text
TPC-REOPEN-20260803-D-AFFINE-MOBIUS
TPC-REOPEN-20260803-D-ACTUAL-CLOUD-FRAME
TPC-REOPEN-20260803-D-PAIR-H1
```

三者均回报同一 HEAD/handoff hash、`files_changed=[]`、tracked/cached diff为空；
所有正式写入仍由主控完成。外部 source evidence只采用 official arXiv theorem
body或 official journal PDF。本节是对明示 sources/versions与 current refs的有限
审计，不是全局文献 nonexistence claim。

同一 theorem-valid packet始终为：

```text
sigma=1/10000, lambda=99979/210000, delta=7/60, beta=267/400,
Q=X^(267/400+o(1)), J=X^(133/400+o(1)), C=floor(J),
h0=2, N0=JQ^2 asymp XQ.
```

第 22 节 `delta=1/20` truncated-entry source lock没有重开，也没有与该 packet拼接。

### 36.2 O161 natural/fixed-affine source backtrace

literal core仍为

```text
L1(z)=d+s*z, L2(z)=u+a*z,
c_z=mu(L1(z))*mu(L2(z)), q_O161=a*s,
s*u-a*d=2, hence s*L2-a*L1=2.
```

逐 theorem-body结果如下：

| source/version | source-stated strongest nearby theorem | first fatal for O161 |
|---|---|---|
| Shao--Teräväinen `2006.05954v2`, Corollary 11.1 | fixed `epsilon,A,t,d,M`、`Q<=x^(1/3-epsilon)`，除 `O(Q/log^A x)` 个 external moduli外，对 size `<=M` finite-complexity affine tuple给 natural Mobius-product box sum `o_(t,d,M)(x^d)` | O161 homogeneous parts `s*z,a*z`在一维平行，且 `s*L2-a*L1=2`；这是 source明确排除的 twin-prime型 non-finite-complexity system |
| Teräväinen `1710.01195v2`, Theorem 1.4/Remark 1.9 | fixed shifts的 logarithmic binary correlation；Remark 1.9允许 fixed affine forms | normalization是 logarithmic，forms/parameters固定，error定性；没有 growing packet uniformity或 fixed `X` power |
| Mangerel `2306.09929v4`, Theorem 1.1/Remark 1.2 | fixed affine forms上 multiplicative-value equality event的 logarithmic density；Remark 1.2明确指出相应 Cesaro binary-correlation升级无条件不可用 | equality event不是 signed Mobius correlation，主 hypotheses也不接收 Mobius；该 remark只能作 limitation，不能作新 cancellation theorem |

Corollary 11.1 的 external modulus不是 O161 Jacobian/normalization `q_O161=as`；
令二者同名不能恢复 literal slopes。即使反事实忽略 finite-complexity fatal，source
仍只对 fixed form-size `M`定性有效，而 terminal-block translation保留
`M` 至少为 growing `a+s`量级。其 `o(H)` 经 `q_O161/N asymp 1/H`
至多给 `o(1)`，不能支付 fixed positive `X` power，也没有 named phase、actual
masks/weights或 packet attachment。

Teräväinen source的正确 fixed-affine syntax不得与 Shao--Teräväinen source的
natural normalization拼接。Mangerel的 source-stated Cesaro limitation进一步确认
缺口，但不证明全局不存在。故既不能控制 DIRECT 的 `q/N` terminal blocks，也不能
供应 TPC-159 BAD `q/T` telescoping所需的每个 scheduled local ancestor。

### 36.3 actual GM cloud 与 hyperbolic point-frame theorem

actual inverse placement保持：

```text
B_t=[[m,(m*j+2)/G],[n,(n*j+2)/G]],
H_t=2*|m-n|/G, g_t=H_t^(-1/2)*B_t^+ in SL2(R),
alpha1=sum_t conjugate(a_t)*delta_(g_t^(-1)), alpha2=delta_I.
```

目标不是 ordinary spectral family mean，而是 actual cloud的 full first-slot
self-kernel以及 cross-`D0` blocks。需要

```text
E1 <= P_X * sum_t |a_t|^2,
P_X <= X^(1/400-kappa_row-epsilon+o(1)),
0 < kappa_row < 1/400.
```

逐 source结果为：

| source/version | 最强合法 specialization | first fatal for actual cloud |
|---|---|---|
| Chamizo, *The large sieve in Riemann surfaces*, Acta Arith. 77 (1996), Theorem 2.1 | fixed `Gamma` 的 `Gamma\\H=Gamma\\G/K` 上，对 pairwise `delta`-separated weight-zero points给 spectral point large sieve；对偶后形似 spherical evaluation-cloud Gram bound，成本 `T^2+delta^(-2)` | actual kernel在 moving `Gamma_pm(q)\\G` 上保留 right-`K` direction/multiple `K`-types；source无 full-group intertwiner，常数依赖 `Gamma`及 cusp height，actual all-block separation未证 |
| Pesenson `1104.1710`, Theorems 2.5/4.4 | bounded-geometry manifold或 `H=G/K` 上预先设计、covering且分离的 `rho`-lattice Paley--Wiener sampling frame | actual signed moving cloud没有 `rho`-lattice theorem；无 congruence level、outer labels、cross-`D0`或 TPC normalization |
| Anker--Germain--Léger `2306.12827`, Theorem 1.2 | 无 cusp、infinite-area geometrically finite surface上的 continuous spectral projector `L2->Lp` | Dirac cloud不在 source input class；finite-area cusp case不在 theorem中，且无 discrete Gram/frame statement |

Chamizo 是本轮真正最接近 operator形状的 primary theorem，但三个额外假设

```text
fixed Gamma, spherical weight zero, actual projected cloud delta-separated
```

都没有 source-backed attachment。更强地，fixed-`D0,G,j` common-translation
algebra给 `g_k*g_0^(-1)=P_(k/Delta#)`。若相邻 projected atoms确实 distinct、
simultaneously active，则条件性地

```text
delta^(-2) asymp |Delta#|^2
  >= X^(268/400-2*kappa_row+o(1))
```

在最坏 `G=C` 边界远大于允许的
`X^(1/400-kappa_row-epsilon+o(1))`。这是 theorem-ledger exclusion，不是
actual large-energy counterexample：仓库没有证明相邻 algebraically admissible
coefficients同时非零或 coherent。cross-`D0` comparable-determinant compact
collisions也仍需独立 block theorem。

因此 screened spatial frames既未无损映射到 actual determinant/content/outer
labels/prefix order/normalization，也没有支付 strict endpoint budget。

### 36.4 pair-native 与 H1 current-ref delta

冻结的 all-ref H1 census基线为
`023ccb5959e35b96673117b76add3dcbc3987aca`。此后 current refs中唯一触及允许
TPC source/artifact范围的数学邻近提交为
`f2f98b0bdc4b56c36292e9211b19c1d2e45ffae0`；它只刷新 TPC-134/135/136
三个 certificate的上游 SHA-256 pins，没有新增 theorem body、pair registry、
occurrence record、normalization或 H1 edge。TPC-18、TPC-93、TPC-133/134/136、
TPC-143、TPC-173/174/179与 TPC-205/206关键 source blobs相对 snapshot没有数学
delta。

TPC-206 selected `103 -> 107` projection仍只有 `13/42` fields。逐字段首 fatal仍是：

```text
field #9 D = ABSENT
NO_SELECTED_PAIR_OPENED_D_SLICE_LOCATOR
ROW_DIVISOR d=1 IS NOT SOURCE_LOCKED OPENED SCALE D=1
```

后续 `J,Q,T,U0,G_X_row`、joint packet/source locator、joint mask、literal pair AST、
support/nonzero、retained `omega`、child inverse与四阶段 normalization也均未供应。
TPC-205 ledger的 generic remainder、square-root return与 full-block endpoint
reassembly仍未关闭，strict `1/400`不能由 schema completion自动取得。

H1仍须从 original nonsoft cuts正向构造 source-backed linear occurrence map；TPC-93
只给 supplied retained `omega`后的 conditional inverse，没有 cut-to-`omega` theorem。
TT-star pair formation对 source coefficient二次齐次，H1 lift则必须线性且
coefficientwise conservative；所以 current pair/Cauchy carrier不能自动逆变为 H1
edge。这是有限 type obstruction，只停止 direct pair-to-H1 promotion，不停止未来
独立 pre-TT-star `L_X` construction。

发布前只读 fetch把 `origin/main` 从本轮启动基线推进到
`ecad6e7d70c7b1b452ee337f17c060dd0ae790ff`。delta仅含 commits
`c548ba9`、`ecad6e7` 的 RH-349/350 共 34 个 RH-only files，没有覆盖 TPC source、
`TPC_HANDOFF.md`或根 scoped policy。两篇的 exact RH coefficient为

```text
p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j),
m_(k,j)=k-j, n_(k,j)=2*m_(k,j).
```

RH-349无条件证明 fixed `j=2,3` scalar minimax identity，但 physical weighted
nonvanishing结论假设未证的 `Y_2=o(H_m2),Y_3=o(H_m3)`。RH-350无条件证明
selected lower-even growing window上的 uniform `S/P` laws与 weighted minimax；
其 physical direct-subprefix结论仍假设未证的

```text
x^(-(k-2))*sum_(2<=j<=J_k) |Y_(k,j)|/(2*H_(m_(k,j))) -> 0.
```

这些在 RH program内是 exact physical/scalar results，不得误报为纯模型。但它们的
sideband index、positive phase ratio、absolute-residual lower bound、`H_m`与
`x^(-(k-2))` normalization均没有 source-backed map到 O161 `c_z`、TPC32
three-channel `A_C`/content/`Delta#`、actual GM cloud、42-field pair或 H1 edge。
RH 的 `n=2m`与 starting `j=2`也不是 fixed physical `h0=2`。first fatal为
`LITERAL_PHYSICAL_COEFFICIENT_AND_INDEX_UNIVERSE_MISMATCH`；abstract“单一 scalar
不能同时平衡多个坐标”的类比只是 inference，不能作 theorem crosswalk。

本 delta只新增第 6 节一个 source-specific cross-program transfer cell，不产生
TPC method credit；第 34 节旧 cell仍严格限于 RH-342--348。新 cell只冻结
commits `c548ba9`/`ecad6e7` 的当前 transfer审核。未来若出现 literal
coefficientwise RH/TPC theorem，仍可独立重开。

### 36.5 状态防火墙

本轮没有得到以下任一真实输入：

```text
O161_NATURAL_GROWING_LITERAL_PAIR_FIXED_POWER_THEOREM = ABSENT
ACTUAL_FULL_GROUP_LEVEL_UNIFORM_CLOUD_FRAME_THEOREM = ABSENT
ACTUAL_CLOUD_SEPARATION_OR_SIGNED_LOCAL_MULTIPLICITY_THEOREM = ABSENT
PAIR_NATIVE_42_FIELD_PRODUCTION_RECORD = ABSENT
PAIR_TO_OMEGA_THEOREM = ABSENT
H1_LINEAR_OCCURRENCE_EDGE = ABSENT
RH349_350_TO_TPC_LITERAL_CROSSWALK = ABSENT
```

第 6 节全部旧 method cells继续 `STOP_SCOPED`，尤其 TPC193 V1、common-`k` V1、
tail-failure/A/B V1与 full-`r_R r_R` ultra-complement V1。两个 O161 pointwise
parents、TPC32 direct/fixed-`D0`/frame parents、pair-native reroute、H1与 global
architecture继续 `OPEN`。fixed-atom credit=`0`，strict `1/400=UNPAID`，
`L2=NONE`。

### 36.6 精确裁决与合法 reopen interface

本轮精确有限裁决为：

```text
TPC32_O161_PAIR_H1_20260803_AFFINE_MOBIUS_AND_HYPERBOLIC_FRAME_BACKTRACE_
FAILS_DOMAIN_NORMALIZATION_OR_PRODUCTION_EDGE_GATES_NO_TRIGGER_
STOP_SCOPED_PARENTS_OPEN

THEOREM_TRIGGER = false
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC207_CREATED = false
```

只在出现下列 source-backed输入时重开对应 local parent：

1. 对 growing O161 literal pair直接给 natural terminal-block fixed-power theorem，
   同时接受 prescribed phase、actual masks/weights、packet schedule与正确 `q/N`；
   或逐 ancestor满足 TPC-159 BAD `q/T` telescoping contract；
2. 直接作用于 moving `Gamma_pm(q)\\G` actual Dirac cloud、全部相关 `K`-types及
   full/cross-`D0` blocks的 level-uniform frame theorem，或直接控制 actual signed
   compact-block energy/local multiplicity并支付完整 exponent ledger；
3. materialize same-source complete 42-field production pair、pair-to-`omega`与四阶段
   normalization，或从 named actual upstream cut正向给出首条 linear H1 occurrence
   edge及全 cut conservation。

任一 local gate转正也不自动创建 TPC-207。all-`D` uniformity、exactly-once
physical cover、original/global normalization、tail-failure、A/B selection、actual
packet attachment、完整 provenance与 strict `1/400` payment仍须分别通过，并使
页首 trigger发生真实 theorem-backed状态变化。

### 36.7 发布边界

本轮没有创建 TPC-207、论文、paper directory、PDF或构建日志。正式写入只允许
`TPC_HANDOFF.md`；全部 protected untracked必须原样保留且不纳入提交。

```text
POST_WRITE_RELEASE_REGRESSION = 22/22 PASS
TPC111_124_126_127_SUPPLEMENTAL = 4/4 PASS
POST_WRITE_GIT_DIFF_CHECK = PASS
POST_WRITE_MARKDOWN_FENCES = 926 MARKERS BALANCED
PROTECTED_UNTRACKED_RECHECK = 127 FILES
PROTECTED_UNTRACKED_MANIFEST_SHA256
  = 35ad4ac2d5def3ecec536bf3943fd0279cbea23b332ed5d7fff659cd6f673f2f
FINAL_SYNC_ORIGIN_MAIN_BEFORE_HANDOFF_COMMIT
  = ecad6e7d70c7b1b452ee337f17c060dd0ae790ff
FINAL_SYNC_DELTA_FROM_INITIAL_CC9E047
  = RH349_TO_RH350_34_RH_ONLY_FILES
FINAL_SYNC_TPC_SOURCE_LOCK_CHANGE = NONE
SUBAGENT_FILES_CHANGED = 0
TPC27_TO_32_LEGACY_WRITERS_EXECUTED = NO
TPC122_WRITER_EXECUTED = NO
```

正式写入后必须重跑第 1 节全部 22 项只读回归、TPC-111/124/126/127 四项
supplemental checks与 protected manifest。只 stage本 handoff；commit/push后必须
验证 local `HEAD`、`origin/main`、remote `refs/heads/main` 三个 hash完全一致。
