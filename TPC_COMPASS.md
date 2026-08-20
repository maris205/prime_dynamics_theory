# TPC distilled map and bold channel

更新时间：2026-08-20
状态：`BOLD_CHANNEL_V68 / SHORT_QUOTIENT_CLUSTER_MAJORANT_BUILT_DIRECT_PHYSICAL_ENERGY_OPEN`
claim level：`PROVED_STRUCTURAL_L1_SHORT_QUOTIENT_CLUSTER_MAJORANT_WITH_TOP_SHELL_NO_SAVING_OBSTRUCTION`
编号事实终点：TPC-215；TPC-216 trigger：`false`

当前 TPC-215 入口：proof 为
`research/tpc-big-road/bridge_b_short_quotient_mobius_majorant.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_short_quotient_mobius_majorant_checker.py`，编号论文为
`papers/tpc-215-short-quotient-mobius-majorant/`。V46 activation floor、short-quotient
normal form、exact row-norm divisor decomposition 与 `O((log x)^2)=x^(o(1))`
complete-period cluster-to-direct majorant 已证明；top-shell ratio one 是 scoped
obstruction。direct-sum physical row energy、finite-window Gram、prime-shell/four-packet
reassembly、full Gate B、`L2`、fixed-atom credit 与 TPC endpoint 仍 OPEN。

V61 当前入口：proof 为
`research/tpc-big-road/bridge_b_zero_hole_additive_edge_frame.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_zero_hole_additive_edge_checker.py`，编号论文为
`papers/tpc-208-zero-hole-additive-edge-frame/`。V61 证明 standard-zero-hole variance
是 nonzero additive frequencies上的 complete-graph tight frame，并把强制的 `(q-2)`
coefficient diagonal exact分配到同一 edge cells：

```text
V_0 = 1/[q(q-1)] sum_e |T_e|^2,
q R_0 = 1/(q-1) sum_e E_e^circ,
Delta_(k,k+d)(n)=e_q(-kn)(1-e_q(-dn)).
```

任意 scalar-weighted literal `(e_k-e_l)` representation又被每个 off-diagonal entry
强制使用全部 edges、weight `1/(q-1)`，所以 strict edge-subset sparsification停止。
remaining first fatal是把 complete oriented `(d,k)` frame集体变换为 source-valid
Kloosterman cells，并保留 blocks、four-packet signs与 prime shell的 fixed-saving
reassembly。完整 Gate B、`L2`、fixed-atom credit与 TPC仍 OPEN。

本文件把 TPC-1--208 看成 200 多个可审计研究节点，而不是 200 多篇彼此独立的
传统论文。它只做三件事：压缩旧地图、选一条主干、集中管理大胆假设。V60 的完整
proof、scope与独立 checker位于
`research/tpc-big-road/bridge_b_moving_hole_bdh_translation_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_moving_hole_bdh_translation_checker.py`；V58 的完整
proof、scope与独立 checker位于
`research/tpc-big-road/bridge_b_terminal_scalar_root_and_q_transverse_split.md`及
`research/tpc-big-road/tpc_bridge_b_terminal_scalar_root_checker.py`；V57 位于
`research/tpc-big-road/bridge_b_longitudinal_anchor_transverse_maximal_transfer.md`及
`research/tpc-big-road/tpc_bridge_b_longitudinal_anchor_checker.py`；V56 的完整
proof、scope与独立 checker位于
`research/tpc-big-road/bridge_b_pruned_dyadic_maximal_fold_first_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_pruned_dyadic_maximal_checker.py`；V55 位于
`research/tpc-big-road/bridge_b_longitudinal_replication_and_modulus_operator_dichotomy.md`及
`research/tpc-big-road/tpc_bridge_b_longitudinal_operator_checker.py`；V54 位于
`research/tpc-big-road/bridge_b_paired_row_longitudinal_mode_and_terminal_equivalence.md`及
`research/tpc-big-road/tpc_bridge_b_paired_row_mode_checker.py`；V53 位于
`research/tpc-big-road/bridge_b_pair_row_bessel_and_symmetric_two_gate_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_pair_row_bessel_checker.py`；V51 位于
`research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_fold_first_long_mobius_checker.py`；阶段性论文轨位于
`research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md`。V50 位于
`research/tpc-big-road/bridge_b_endpoint_matched_siegel_world_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_endpoint_matched_siegel_world_checker.py`；V49 位于
`research/tpc-big-road/bridge_b_ultralow_conductor_three_lane_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_ultralow_conductor_three_lane_checker.py`；V48 位于
`research/tpc-big-road/bridge_b_low_conductor_signed_covariance_splice.md`及
`research/tpc-big-road/tpc_bridge_b_low_conductor_signed_covariance_checker.py`；V47 位于
`research/tpc-big-road/bridge_b_centered_ap_covariance_and_prime_hybrid_atlas.md`及
`research/tpc-big-road/tpc_bridge_b_centered_ap_covariance_checker.py`；V46 位于
`research/tpc-big-road/bridge_b_transition_native_euler_bdh_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_transition_native_euler_bdh_checker.py`；V45 位于
`research/tpc-big-road/bridge_b_conductor_stratified_transition_spectrum.md`及
`research/tpc-big-road/tpc_bridge_b_conductor_stratified_transition_checker.py`；V44 位于
`research/tpc-big-road/bridge_b_transition_reciprocal_variance_and_ramanujan_mean.md`及
`research/tpc-big-road/tpc_bridge_b_transition_reciprocal_variance_checker.py`；V43 位于
`research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md`及
`research/tpc-big-road/tpc_bridge_b_proper_factor_poisson_transference_checker.py`；V42 位于
`research/tpc-big-road/bridge_b_mobius_directional_dispersion_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_mobius_directional_dispersion_checker.py`；V41 位于
`research/tpc-big-road/bridge_b_qlocal_residual_row_bessel_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_qlocal_residual_row_bessel_checker.py`；V40 位于
其上游 artifact 位于
`research/tpc-big-road/bridge_b_row_energy_and_packet_route_atlas.md`及
`research/tpc-big-road/tpc_bridge_b_row_energy_route_atlas_checker.py`；V39 位于
`research/tpc-big-road/bridge_b_schatten_duality_and_packet_energy_pivot.md`及
`research/tpc-big-road/tpc_bridge_b_schatten_packet_energy_checker.py`；V38 位于
`research/tpc-big-road/bridge_b_canonical_packet_schatten_emitter.md`及
`research/tpc-big-road/tpc_bridge_b_canonical_packet_schatten_checker.py`；V37 位于
`research/tpc-big-road/bridge_b_loss_budgeted_shift_packet_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_loss_budgeted_shift_packet_checker.py`；V36 位于
`research/tpc-big-road/bridge_b_multiroute_ratio_core_atlas.md`及
`research/tpc-big-road/tpc_bridge_b_multiroute_ratio_core_checker.py`；V35 位于
`research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md`及
`research/tpc-big-road/tpc_bridge_b_proper_factor_unit_ratio_checker.py`；V32 的完整
compiler位于
`research/tpc-big-road/bridge_b_base_scale_residual_oscillation_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_residual_oscillation_checker.py`；V31 位于
`research/tpc-big-road/bridge_b_whole_object_major_mismatch_and_terminal_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_whole_object_major_mismatch_checker.py`；V30 位于
`research/tpc-big-road/bridge_b_terminal_major_cross_flatness_and_equivariant_quotient.md`及
`research/tpc-big-road/tpc_bridge_b_terminal_major_cross_flatness_checker.py`；V29 位于
`research/tpc-big-road/bridge_b_joint_major_minor_and_low_christoffel.md`及
`research/tpc-big-road/tpc_bridge_b_joint_major_minor_checker.py`；V28 位于
`research/tpc-big-road/bridge_b_euler_zero_axis_and_kernel_carrier.md`及
`research/tpc-big-road/tpc_bridge_b_euler_kernel_checker.py`；V27 位于
`research/tpc-big-road/bridge_b_ramanujan_energy_and_pointed_block_gate.md`及
`research/tpc-big-road/tpc_bridge_b_ramanujan_energy_checker.py`；V26 compensated
dilation位于
`research/tpc-big-road/bridge_b_compensated_dilation_and_block_highway.md`及
`research/tpc-big-road/tpc_bridge_b_compensated_dilation_block_checker.py`；V25 corrected
emitter位于
`research/tpc-big-road/bridge_b_corrected_fourier_factorable_emitter.md`及
`research/tpc-big-road/tpc_bridge_b_corrected_fourier_factorable_checker.py`；V24 atom
compiler位于
`research/tpc-big-road/bridge_b_literal_jutila_farey_atom_compiler.md`及
`research/tpc-big-road/tpc_bridge_b_literal_jutila_farey_atom_checker.py`；V23 prime-shell
Jutila interface、V22 projector firewall、V21 wrapped mean、V20 terminal
innovation、V19 raw-row/source
innovation、V18 typed
backward-dual、V17 rank与 V16 common-return contracts继续冻结于各自 artifacts。正式 theorem
事实仍以 `TPC_HANDOFF.md`、已提交 papers、artifacts与 checkers为准；本文件本身
不是新 theorem evidence，也不解除任何 `STOP_SCOPED` 或 release gate。

## 1. 一句话决策

```text
200+ local research nodes
  -> 13 major obstruction classes
  -> 2 visible bottlenecks
  -> exact literal determinant
  -> Jutila main/error split
  -> complete Farey/Kloosterman atoms
  -> corrected Fourier nonzero-shift emitter
  -> exact compensated prime-dilation covariance
  -> weighted Ramanujan Hilbert gate + zero-axis main firewall
  -> occurrence-native Euler carrier + reduced-radical BC corridor
  -> q-local x^(95/96) model + cell-product MRT reduction
  -> whole-object model-level major mismatch + minor cross-flatness
  -> exact proper-factor re-collapse to binary ratio covariance
  -> three conditional lanes: K collective compiler / E energy / X characters
  -> K lane exact centered shift packet + admissible overhead omega<19/800
  -> q-local model paid + positive physical Gram gate
  -> proper-factor directional dispersion cells
  -> complete centered Poisson: d<=H/(4Q) nonzero aliases deleted
  -> exact zero-axis transfer: C=A-L_pr*S+paid errors
  -> transition / Type-II / reverse-Type-I inverse-residue alias
  -> exact additive-zero-mode excision in the transition occupancy
  -> centered signed prime--hybrid AP covariance atlas
  -> exact conductor--Euler scalar splice
  -> direct low-conductor signed scalar
     or stronger signed character--Ramanujan energy
  -> saving-matched moving cut + global Siegel-quality dichotomy
  -> fold-first unordered long-Möbius pair emitter
  -> compensated pair dilation and completed prime rows
  -> exact paired-row mode diagonalization
  -> one common transverse row theorem OPEN
  -> terminal signed longitudinal scalar OPEN
  -> terminal q-local covariance
     + 1 symmetry-breaking low-Christoffel dynamical reserve
     + 2 independent analytic reserves (A1/A2).
```

不再因为一个新 schema、一个新 source mismatch或一个有限 certificate自动生成下一篇
编号论文。只有核心通道的 theorem state发生变化，才值得形成新 release。

## 2. 旧工作的 13 类蒸馏

| class | 200+ nodes 已建立的可复用结论 | 保留的 firewall |
|---|---|---|
| O1 object/domain typing | terminal block、cumulative prefix、physical packet prefix是不同对象 | block不能改名为 cumulative；physical outer sum不能偷加 normalization |
| O2 physical labels | fixed physical `h0=2`、determinant、content、outer labels与 prefix order必须同源 | 同名数字、`d=1`、`D0=0`或 RH order gap不能替代 opened `D`/physical `h0` |
| O3 actuality/provenance | symbolic AST、formal support、shadow、synthetic fixture与 actual active occurrence已分层 | formal record不能升级为 actual coefficient/nonzero/support |
| O4 linear versus bilinear | pre-TT-star H1 occurrence edge是线性对象；post-TT-star pair是二次对象 | pair不能直接逆变为 H1 edge或 retained `omega` |
| O5 average versus pointed | phase `L2`、Lebesgue-a.e.、density-one与 family mean不等于指定 atom/seed | metric statement不能升级成 prescribed phase或 arithmetic point |
| O6 clocks/normalizations | logarithmic、natural、terminal `q/N`、cumulative `q/T`与 aging clock已分开 | logarithmic-to-natural、complete-frequency-to-zero-mode、fixed-clock-to-moving-clock transfer禁止 |
| O7 period versus diagonal | finite primorial full-period mass与 primality-exact physical window不重叠 | complete-period Haar average不能当 growing diagonal prefix theorem |
| O8 local density versus primes | CRT/local singular series `2C2`是 proved local geometry | survivor mass不能自动升级成 prime-sensitive lower bound |
| O9 source/target coupling | source marginal large sieve与 target marginal mean不能无权相乘 | target maximum多损一个 `J`；identity bucket/raw zero column仍须 literal theorem |
| O10 uniformity/loss ledger | growing coefficients、actual masks/weights、packet ranges、uniform constants与全部 losses必须同一 theorem支付 | fixed/polylog theorem、定性 `o(1)`或异源拼接不给 strict `1/400` |
| O11 coding versus measure | `RLR^infinity` critical orbit、`u_c`-ACIP typical orbit、exact prime word与 finite-sieve diagonal已分开 | critical kneading equality不等于 typicality、prime coding或 event recurrence |
| O12 higher-dimensional lift | Hénon exact symplecticity/reversibility与 arithmetic factor是不同层 | area preservation/unitarity不能自动传递 prime event或 pointed genericity |
| O13 release/provenance | L0/L1/L2、source locks、mutation tests、all-`D` cover与 physical reassembly形成可复核基础设施 | checker PASS或授权不等于 theorem trigger |

这些不是失败清单，而是后续大胆构造的类型系统。新路线若碰到其中一类，必须显式
说明它提供了什么新 object/theorem，不能再靠改名绕过。

## 3. 两个可见瓶颈

### A. 解析表示

当前第 49--51 节把外围项压缩到同一 small-content far-copy off-diagonal target：

```text
|V_(L,C,far)| + |V_(R,C,far)|
  << X^epsilon Q^3/J.
```

所缺不是又一个 marginal mean，而是 target-coupled collective
Bessel/Gram/raw-zero-column theorem。source-averaged Mellin已有一个合法边际 `L1`，
但与 target overlap结合时仍多损一个 `J`。

### B. 动力学表示

精确 finite-sieve moving targets已有正 mass、总 mass发散及 twin-event identity。
V2 又证明 Haar moving sum的 `O(N)` variance与 a.e. recurrence；但所缺仍是指定
arithmetic point的

```text
CRITICAL_SCALE_POINTED_ODOMETER_SHRINKING_TARGET_RECURRENCE.
```

ordinary a.e. dynamical Borel--Cantelli不能代替这个 pointed theorem。更准确地，
该 pointed conclusion由 exact event identity与 TPC等价；它是 endpoint，不是一个
逻辑上更弱的新 bridge。

V16 因此不再直接把 H4当作中间施工门。exact replication--deletion geometry给出
`R_p^*R_p=(1-2/p)I`与正交 deletion forcing；full centered space只有 logarithmic
prime-scale衰减，不能 uniformly coercively exact intertwine到 uniformly exponential
memory-loss carrier。surviving Bridge B改为 physical-observable quotient：先让
nonautonomous dynamics产生 deterministic `H_dyn/H3_phys` estimate，再进入 PBAPT，
而不是把 a.e. genericity升级到 seed `0`。

V1 把 A 与 B 暂视为同一个 centered-complement问题。V2 的 adversarial audit证明
这个说法必须分型：primorial incidence与 TPC-32/O161 packet目前是两个 exact
connected components，中间没有 coefficientwise linear map；Haar centering也不是
critical physical endpoint的正确 main term。大胆通道现在只允许用一个显式
Type-I/Type-II/reassembly theorem连接它们，不再靠 diagram命名制造统一。

## 4. 精确 arithmetic base：已经完成的地基

令

```text
P_k = product_(j<=k) p_j,
G_k = Z/P_k Z,
V_k = R^(G_k),
A_k(r) = 1_((r,P_k)=1),
B_k(r) = A_k(r) A_k(r+2),
rho_(p_k) = product_(p<=p_k) (1-1/p),
C_2 = product_(p>2) p(p-2)/(p-1)^2.
```

当 `p=p_(k+1)>2` 时，定义线性 pair replication--deletion operator
`R_p:V_k -> V_(k+1)`：

```text
(R_p f)(r+jP_k)
  = f(r)
    1_(p does not divide r+jP_k)
    1_(p does not divide r+jP_k+2),
r in G_k, 0<=j<p.
```

于是 `B_(k+1)=R_p B_k`。若 `B_k(r)=1`，恰有两个不同 copy indices被新素数
`p` 删除，故 full-cycle pair count精确乘以 `p-2`；这些 `R_p` 在 changing spaces
`V_k` 上组成 exact nonautonomous cocycle。等价地，Haar mean为

```text
a_k = (1/|G_k|) sum_(r in G_k) B_k(r)
    = (1/2) product_(2<p<=p_k) (1-2/p),
a_k/rho_(p_k)^2 -> 2C2.
```

同一对象有一个 exact inverse-limit moving-target formulation。令

```text
X_arith = Z_hat,
T(x)=x+1,
mu = Haar probability,
pi_k:X_arith -> G_k,
kappa(n)=max{k:p_k<=sqrt(n+2)},
E_n = {x:B_(kappa(n))(pi_(kappa(n))(x))=1}.
```

则

```text
T^n(0) in E_n
  iff B_(kappa(n))(n)=1
  iff n and n+2 are both prime                 (n>=3),
mu(E_n)=a_(kappa(n)) asymp 1/(log n)^2,
sum_n mu(E_n)=infinity.
```

这里 positive moving mass、总 mass发散与 distinguished seed/event identity已经在
同一 probability system中闭合；尚未闭合的是该 seed的 recurrence。

对 physical dyadic scale `X`，另取 `k_X` 使

```text
p_(k_X) <= sqrt(2X+2) < p_(k_X+1),
ell_X(f) = sum_(X<n<=2X) f(n mod P_(k_X)),
f in V_(k_X).
```

对充分大 `X`，`ell_X(B_(k_X))`就是该物理窗口中的 twin-prime count：在
`n,n+2<=2X+2` 上，没有不超过 `sqrt(2X+2)` 的素因子就等价于 primality。
因此 arithmetic base、stage、event与 distinguished point都是非循环且 exact 的。

CRT还立即给出 exact two-time covariance identity。令

```text
y_n=sqrt(n+2),
r_p = cardinality({0,2} mod p),
nu_p(d) = cardinality({0,2,d,d+2} mod p),
alpha(y)=product_(p<=y) (1-r_p/p),
Z_n(x)=1_(E_n)(T^n x).
```

若 `d=n-m`、`q=min(y_m,y_n)`、`Y=max(y_m,y_n)`，则 independent CRT coordinates
给

```text
E_mu[Z_m Z_n]
  = product_(p<=q) (1-nu_p(d)/p)
    product_(q<p<=Y) (1-r_p/p),

Cov_mu(Z_m,Z_n)
  = alpha(y_m) alpha(y_n) (K_q(d)-1),

K_q(d)
  = product_(p<=q)
      (1-nu_p(d)/p)/(1-r_p/p)^2.
```

当某个 local joint factor为零时，第二式按第一式直接解释。特别地，`p=2` 在
`d` odd时给 joint zero，在 `d` even时给 ratio `2`；奇素数的 resonances只由
`p|d(d-2)(d+2)` 产生。V2 已进一步把该 product展开成 compatible CRT residue
classes，证明任意 integer interval `I` 上

```text
|sum_(d in I)(K_q(d)-1)|
  <= 6 product_(5<=p<=q)(1-2/p)^(-2).
```

Abel summation与 exact identity
`alpha(q)^2*6*product_(5<=p<=q)(1-2/p)^(-2)=1/6`
随即给 dyadic Haar moving sum `Var<=X/2+O(1)`。因此
`H3_METRIC=PROVED_HAAR_MOVING_VARIANCE_O_N`；pointed discrepancy仍完全没有得到。

## 5. 大胆主通道 V4：PBAPT 与 tensor-local Ford--Maynard redesign

Haar decomposition

```text
B_k=a_k*1+W_k,
mean(W_k)=0
```

仍是 exact，但它不是一个封闭的 contracting complement。若 `p=p_(k+1)>2`，则

```text
W_(k+1)
  = R_p W_k+a_k(R_p1-(1-2/p)1),
```

即 constant mode每 stage都向 complement注入 forcing。对 physical interval令

```text
C_k=sum_(X<n<=2X)B_k(n),
D_(k,p)=sum_(X<n<=2X)B_k(n)1_(p|n(n+2)),
epsilon_(k,p)=D_(k,p)-(2/p)C_k.
```

则有 exact deletion-bias cocycle

```text
C_(k+1)=C_k-D_(k,p),
E_(k+1)=(1-2/p)E_k-epsilon_(k,p),

C_(k+1)/(a_(k+1)X)
  = C_k/(a_kX)-epsilon_(k,p)/(a_(k+1)X).                  (5.1)
```

此外加法正交性逐式给

```text
epsilon_(k,p)
  = (1/p)sum_(1<=a<p)(1+e_p(2a))
      sum_(X<n<=2X)B_k(n)e_p(an).                         (5.2)
```

这使 stage renormalization与 additive Fourier/dispersion合法相接；但 (5.2) 还不是
TPC-32 packet coefficient，actual crosslink仍缺。

V1 的 strong target

```text
ell_X(W_(k_X))=o(a_(k_X)X)
```

现标记为 `HEURISTICALLY_MISCENTERED / DEPRIORITIZED`。临界 cutoff下，Mertens与
Hardy--Littlewood标准主项预测 physical/Haar ratio趋于
`exp(2gamma)/4=0.793054740...`，不是 `1`。这里 HL只作 normalization stress，
不作 theorem premise。正确的新未知对象是 pair-sieve/Buchstab profile

```text
C_k(X)=a_k X Phi_2(log X/log p_k)+Error_k(X),              (5.3)
```

`Phi_2` 尚未定义成已证函数，更没有 endpoint theorem。

因此 V2 不再把 pointed recurrence叫“中间桥”。主 theorem class改为

```text
PARITY_BREAKING_AFFINE_PATTERN_TRANSFERENCE_THEOREM (PBAPT),
```

其 spine为

```text
general admissible affine-pattern decomposition
       + uniform Type I
       + determinant-uniform fixed-atom Type II
                         |
                         v
             target-coupled Gram/Bessel reassembly
                         |
                         v
             exactly-once cover + complete loss ledger
                         |
                         v
                 prime-producing lower bound
                         |
                         v
                      h0=2 / TPC.
```

PBAPT必须对一类与 prime outcomes无关的 patterns陈述，并统一支付 literal
coefficients、fixed physical shift、domains、parameter ranges、uniform constants、
normalization及全部 losses。否则它只是 TPC endpoint的改名。

V3 的 coarse specialization取

```text
a(n)=Lambda(n+2),
b(n)=2 C2 1_(n odd) product_(p|n,p>2)(p-1)/(p-2).
```

则 local Euler mean、所有 multiplier slice main term、Ford--Maynard
comparison regularity与每个固定 `gamma<1/2` 的 maximal Type I已经闭合。但 V4
adversarial audit证明其 universal Type II为 false：在合法 `M=X^(1/3)` block取
`xi_m=1_(m=1 mod6),kappa_n=1_(n=1 mod6)`，支撑上 `mn+2=0 mod3`；Mangoldt项除
`3^j`外消失而 `b(mn)>=2C2`，故 bilinear sum为 `-cX+o(X)`。因此

```text
COARSE_b2_UNIVERSAL_TYPE_II = STOP_SCOPED_FALSE_MOD3_RANK_ONE
```

V4 replacement对 `z>=2`定义

```text
C_(2,>z)=product_(p>z)(1-1/(p-1)^2),
b^(z)(n)=C_(2,>z)
 product_(p<=z)[p/(p-1)1_(p does not divide n+2)]
 product_(p|n,p>z)(p-1)/(p-2).
```

`z=2`回到 coarse `b`。对 `p<=z`，new factor精确杀掉 `mn=-2 mod p`；对 `p>z`
保留 divisibility projection。两者 local mean均为 `1`且 multiplier conditional
factor均为 `p/(p-1)`。遗漏 prime `p`的 tensor cut contribution为 `Theta(X/p)`，
所以一次固定 saving `B`必须取 `z=log^K X,K>B+margin`；fixed `z`或 fixed `K`
不能支付 all-`B` ledger。

当前 exact parameter仍为

```text
P_TPC=(gamma,theta,nu)=(1/2,133/400,67/400).
```

其 `A1/A2`与 `J -> sqrt(X) -> Q` mirror均精确。对每个 fixed `K`，fundamental
lemma加 Bombieri--Vinogradov已经闭合 `(b.1)/(w)`与每个固定 `gamma<1/2` 的
maximal Type I；`(b.2)`在 `R(P_TPC)=empty`时 vacuous proved。ordinary BV不覆盖
exact `gamma=1/2`，该 fringe只在 H3成立后由 Ford--Maynard mirror补齐。当前唯一
direct analytic大墙是 high-conductor Type II。完整证明与 checker见
`research/tpc-big-road/fm_local_comparison_compiler.md`。

镜像 full-window的另一组 ledger是

```text
(gamma,theta,nu)=(Q,J,Q-J),
gamma+nu=267/400+134/400=1+1/400.
```

所以 strict `1/400`仍有一个精确的 conditional付款位置：它是 full `J/Q`
Type II进入 Vaughan `gamma+nu>1`区间的 surplus；coarse route已 false，hybrid
global gates与 literal physical attachment未证，故 charge继续 `UNPAID`。

V3还找到一个合法但未闭合的 structural bridge：

```text
b^(2,circ)(n)=S(2n)=sum_q mu(q)^2/phi(q)^2 c_q(2n),
Lambda(mn+2)= sum_(dr-mn=2)mu(d)log r
            =-sum_(dr-mn=2)mu(d)log d.
```

第一式只是 coarse divisibility projection的 Ramanujan profile，mod-3 witness证明它
并非 arbitrary factored tests的完整 local model。第二式把 shifted prime逐项落在
determinant-two surface；odd sector固定 coprime `(d,m)`后，`n=n0+d z,r=r0+m z`
保持 determinant `2`。它与 TPC-31
已提交 next gate的 prime--Möbius core `mu(d)log ell`在 `r=ell`后逐 coefficient相同，
故 `FM_TO_TPC31_PRIME_MOBIUS_CORE=PROVED_FORMULA_LEVEL`。但 `omega_D/psi_L`、fixed
residue factors、pair mask、three-channel physical weights、outer HB coefficients、
O161 two-Mobius atom与 packet normalization尚未形成同一 source ledger，direct
attachment仍 `ABSENT`。付清 local tensor gate后，determinant核含一个 fixed rough
`mu(d)`与两组 arbitrary rough `xi_m,kappa_n`；bounded primary scan没有 literal
theorem。hybrid classical sieve ledger现已闭合；当前排序是 high-conductor
determinant dispersion在先，closed `sqrt(X)` endpoint必须包含在同一 master gate。

high-conductor fork现已作 broad route选择。universal `U`在合法 `K=K(B)`下没有
已知反例，但要求 arbitrary two-sided operator norm，作为 reserve保留。通用
Proposition 7.22 `S+` closure会保留 largest-prime fragmentation与至多 `60+19`
个通用 slots，逻辑上足够但过宽，已降为 reserve。

primary route直接把 modified Heath--Brown identity取最小安全值 `h=2`作用于
prime residual。perfect powers由当前 literal sequence的 `x^(1/2+o(1))` bound吸收；
其余只有 `j<=2`、最多四个 variables与两个 HB Möbius slots。large smooth factor、
constant-factor square-root rough factor与 `R(P_TPC)=empty` cover把每项 exactly-once
送入已证 H2或 exact `(X/2)^J<M<=sqrt(X)`的 structured master `SHB-D2`。`h=1`
会产生超 square-root large-Möbius escape branch，故不合法。
该 direct extractor已经 `PROVED_EXACT_REDUCTION_TO_SHB_D2`；新的 determinant estimate
本身仍 `SELECTED_PRIMARY_OPEN_NEW_THEOREM`。published Proposition 4.11/Theorem 2.2
不能用于支付 closed square-root endpoint，否则会循环回 universal `(II)`。

source-locked range atlas又把 `SHB-D2`压到最小中央 cell：`h=2,j=2`、fixed odd
`f_1=c,f_2=1`给 `dr-c e_1e_2=2`上的
`mu(d)mu(e_1)mu(e_2)log r`。把 `e_1e_2`卷成一个 arbitrary coefficient并把 fixed
`c`放入 compact smooth slot后，Bettin--Chandee Corollary 1的类型其实匹配；真正
STOP是完整 error为 `X^(11/10)D^(17/20)`，从 bounded `D`起就没有 saving。
HB4 quarter lift的一次 Poisson虽能形成 BC三线性 phase，但完整 error的第一项要求
`delta<11/56`，而新非零区从 `delta>1/4`开始，故没有新 window；第二项单独显示的
`2/7`不得使用。`HB2`只作为 minimal-slot normal form；HB4 factorized lift现已证明
解析上更有力。保留两个 smooth quarter variables作双 Poisson后，full-`D` Euler germ
与短 comparison slice把 collective principal精确附着到 `b_x^(z)`；单个 dyadic
`D`仍不得单独认领 comparison main。Ramanujan轴为 `X^(3/4+o(1))`，Weil先覆盖
`1/4<delta<1/3`。

进一步把 `a=e_1e_2`卷成 residue coefficient
`b_(n,d)`，其平方是 `d|(h_1a_2-h_2a_1)`的 exact multiplicative incidence，给
`||b||_2<<FDX^o(1)`。Pascadi Theorem 10.3 的完整五项因此再覆盖
`1/3<=delta<3/8`，不是选择性删项。V7 随后不对全部 characters误用 large
sieve，而是按 primitive conductor切开同一个 incidence coefficient。
`cond(chi)>=F`的部分由 primitive multiplicative large sieve把 norm降为
`sqrt(F)D X^o(1)`；`cond(chi)<F`保留 exact Kloosterman projector。squarefree CRT、
Gauss square、Ramanujan cofactor与两次 primitive large sieve给

```text
(F^2/D^2)|K_D^(low)| << X^(7/8+o(1)),
(F^2/D^2)|K_D^(high)| << F^2D X^o(1).
```

所以 factorized HB4 quarter的完整 off-diagonal窗口已经推进到每个 fixed
`1/4<delta<1/2`。exact `delta=1/2`时 high part只有 `X^(1+o(1))`，仍缺任意
`log^-A X`；不得用 fixed-`delta`结论取极限。固定 mod-3 character的 induced family
给出 `F/log Q`增长，继续阻止 all-character shortcut。

`D>X^(1/2)`也不再以 quotient-Möbius为唯一对象。exact HB2 identity
`Lambda=2A1-A2`把 large divisor逐系数切成 `A1-A2`；代回 outer HB4 quarter后，
首个 hard cell为

```text
e1e2f1f2-a1a2b1b2=2,
```

含四个 literal Möbius slots与两个 ordered divisor-log/Eisenstein columns。exact
swapped-shell pairing后，它是两条 weighted `mu_F*mu_F` rows对两条 truncated
ordered `(log W_I)*W_J` columns的 `ER-AB=2` determinant，并保留全局 `6/log X`。
这是 paired divisor-Voronoi/Estermann加外层 Kuznetsov的
合法新接口；现有 BC在展开后无 balanced-quarter saving，当前 Pascadi source map则
未附着 simultaneous second-row incidence/range/`L^2`。generic HB2 second Cauchy继续停在 quadratic
CRT diagonal，不再作为 selected route。

## 6. Logistic 的新角色：carrier，不是 prime orbit

`RLR^infinity` 保留为 band-merging/parity coordinate与可能的 rank-two model，不再
被当作 arithmetic orbit。一个真正有证明价值的 logistic construction必须寻找
operators/intertwiners，而不是比较两条二进制 word：

```text
J_(k+1) R_(p_(k+1))
  = Q_k J_k + Err_k,

R_(p_(k+1)): V_k -> V_(k+1),
J_k: V_k -> B_k^dyn,
Q_k=PF_(2k) PF_(2k-1): B_k^dyn -> B_(k+1)^dyn,
Err_k: V_k -> B_(k+1)^dyn.
```

这里 `P_k` 始终是 primorial；`PF_n` 才是 Perron--Frobenius operator，
`B_k^dyn` 是待构造的 paired logistic Banach space。本 display只是 typed target
`HYPOTHESIS`，不是已有 map。

其中：

1. `R_p` 是上节 exact sieve pair replication--deletion operator；
2. `Q_k` 是 actual nonautonomous paired logistic transfer block；
3. `J_k` 同时保持 mean mode、pair event与整个 declared physical dual family：对
   预先声明 class的 active `A in A_X`及带 literal normalization的
   `ell in L_(k_X,X,A)`，必须有
   `Lambda_(X,A,ell)^dyn` 使
   `ell(f)=Lambda_(X,A,ell)^dyn(J_(k_X)f)` 对每个 `f in V_(k_X)`成立，而不只保持
   一个 symbolic word或 fitted trajectory；对充分大 `X`，`A_X`须非空，且 arithmetic
   promotion前必须含 separately source-locked 的 actual `h0=2` application；
4. 写 `f_(j,X,A)`为 exact stage source trajectory，并约定
   不依赖 `X,A`的 common predeclared `j_0`，要求对充分大 `X`有 `k_X>j_0`且
   `f_(j+1,X,A)=R_(p_(j+1))f_(j,X,A)`；另约定
   `Q_(b:a)=Q_(b-1)...Q_a`、`Q_(a:a)=I`。`Err_k` 的 accumulated physical loss必须由
   一个对全部 active `A,ell`共同的 `epsilon(X)->0`支付：

   ```text
   sup_(A in A_X, ell in L_(k_X,X,A)) sum_(j_0<=j<k_X)
     |Lambda_(X,A,ell)^dyn(
        Q_(k_X:j+1) Err_j f_(j,X,A))|
       <= epsilon(X) X/(log X)^2;
   ```

   不能只给 abstract operator norm而不支付 physical evaluation；
5. `Q_k` 必须实现 forced-triangular cocycle，而非假设 complement invariant；除
   arbitrary-product memory loss外，还须逐 stage传递 (5.1) 的 deletion forcing；
6. 结论必须作用于 actual deterministic physical evaluation，而不只是 ACIP-a.e.
   fibers；本条不得改写成免费解决 pointed H4。

如果这些成立，RH-3 类型的 sequential covariance才可能把 logistic estimates传回
physical innovation/profile或 PBAPT 的 Type-II input；不得再把抽象 complement
contraction直接宣布为 `ell_X(W)=o(a_kX)`。这是大胆的 `HYPOTHESIS`，不是现有
isomorphism的改名。若无法构造保持 physical functional与 forcing的 `J_k`，就立即
停止 logistic carrier，回到 direct arithmetic/analytic attack；不再用数值相似性续命。

V16 对这个 display 加入一个 exact scope firewall。在 normalized Haar `L2` 上，

```text
R_p^*R_p=(1-2/p)I,
g_(k,p)=R_p1-(1-2/p)1 orthogonal to R_p(V_k^0).
```

故 uniformly lower-coercive full-centered-space `J_k` 加 uniformly exponential
memory-loss `Q_k` 的 exact intertwiner已 `STOP_SCOPED`；telescoped full-operator
defect相对 raw product norm可忽略的版本也同样停止。合法的 `J_k` 必须是
noncoercive/observable quotient或只在 physical dual seminorm中控制误差，且不能丢
actual evaluation。完整 theorem与 scope见
`research/tpc-big-road/bridge_b_physical_intertwiner.md`。

还有一个早停 no-go：在 stationary measure-preserving category中，mixing system的
factor仍然 mixing，故真正 mixing的 logistic system不可能把 nonmixing odometer当作
同测度意义下的 stationary factor。可保留的候选只能是 nonautonomous evolution
family、非平凡 operator quasi-intertwiner，或不把 arithmetic base作为 stationary
factor的 construction；每一种都必须显式证明，不能用“chaotic carrier”四个字跳过。

Hénon只在存在 exact natural-extension diagram时加入：

```text
rho_(k+1) H_k = F_k rho_k,
event_H = rho_k^(-1)(event_F),
rho_*(mu_H,k)=mu_F,k.
```

否则 Hénon继续是可解释结构，不占主通道预算。

## 7. H0/H_occ/H_dyn/H2/H3_metric/H3_phys/H4 typed ledger

| gate | exact statement | current status | promotion test |
|---|---|---|---|
| H0 arithmetic base | typed `R_p` cocycle、Haar pair mass、odometer moving event与 twin identity | `PROVED` | locked to TPC-1/RH-1--3 objects |
| H_occ (legacy H1) | pre-TT-star source-backed linear occurrence edge family | `OPEN / NOT_TESTABLE` | actual edges、schedule、ranges、normalization；不得由 quadratic pair逆生 |
| H_dyn | same stage/time/event/physical-functional forced-triangular intertwiner to nonautonomous dynamics | full-centered coercive exponential-mix version `STOP_SCOPED`; physical-observable quotient `SELECTED OPEN` | target-independent coefficientwise identity、physical dual family、forcing与 uniform evaluation |
| H2 rare mass | full-cycle `a_k asymp log^-2 N` | `PROVED_FULL_CYCLE`; physical evolution attachment `OPEN` | no use of `pi_2(N)` or Hardy--Littlewood lower bound |
| H3_metric | Haar moving covariance/variance for exact primorial targets | `PROVED_HAAR_VARIANCE_O_N` | explicit resonance expansion与 independent checker；不产生 arithmetic credit |
| H3_phys | Type II/far-copy cancellation attached to actual physical carrier | `OPEN`; factorized HB4 quarter fixed `delta<1/2` `PROVED_PARTIAL` | literal coefficients、all shapes、target-coupled reassembly、full ledger |
| H_FM_coarse | divisibility-projected comparison、regularity与 sub-square-root Type I | `PROVED_ONE_SIDED`; direct Type II `STOP_FALSE_MOD3` | 不得把 multiplier matching升级为 tensor matching |
| H_FM_hybrid_local | growing-`z` full product-residue factors与 omitted-prime `X/p` ledger | `PROVED_EXACT_LOCAL` | fixed saving先选 `B`再取 `K>B+margin` |
| H_FM_hybrid_sieve | hybrid `(b.1)/(w)`与 sub-half maximal Type I | `PROVED_SOURCE_BACKED`; `(b.2)` `VACUOUS_PROVED` at `P_TPC` | fixed `B`后选 fixed `K(B)`；不得升级 exact half |
| H_FM_hybrid_II | high-conductor multiplicative Type II on literal `[J,1/2]` | `OPEN_MAJOR_WALL` | arbitrary divisor-bounded coefficients、exact endpoints与 log-power norm |
| H_FM_U | universal arbitrary-coefficient H3 | `OPEN_RESERVE_OVERSTRONG` | 无已知反例，但不作 primary target |
| H_FM_SHB_D2 | actual `E_FM(P_TPC)` emitted-multilinear determinant umbrella | `OPEN`; generic Prop. 7.22 fork `DEPRIORITIZED` | source completeness、all shapes、Mellin uniformity与 closed `sqrt(X)` |
| H_FM_HB4_QTR | factorized HB4 quarter collective main and off-diagonal | `PROVED` for every fixed `1/4<delta<1/2`; exact half `OPEN` | conductor projection、complete Pascadi bound、closed endpoint log saving |
| H_FM_HB4xHB2 | exact large-divisor switch to bilateral divisor-log determinant | switch `PROVED_EXACT`; analytic closure `OPEN` | four literal Möbius slots、paired shells、collective main、Voronoi/Kuznetsov ledger |
| H4 distinguished seed | pointed arithmetic section satisfies recurrence/discrepancy theorem | `ENDPOINT_EQUIVALENT_TARGET` | direct theorem for named seed；a.e. membership is insufficient |
| HC closure | PBAPT physical lower bound或 H4 pointed endpoint推出 infinitely many twin primes | `DERIVED_CONDITIONAL` | complete arithmetic carrier、cover、normalization与 loss ledger |

Theorem-state progress只按这张表记录。新增 source或 certificate若不改变
`H_occ/H_dyn/H3_phys/H4`，
只进入 handoff log，不编号。

## 8. Circularity kill tests

任一候选 construction在开始大规模证明前先过以下 tests：

1. `NO_FUTURE_PRIME_PARAMETER`：schedule/intertwiner不得由完整 prime word或 twin
   locations反向选择；有限 sieve divisibility data可以使用。
2. `NO_HL_CALIBRATION`：rare mass lower bound不得把目标 Hardy--Littlewood lower
   bound当输入；`2C2` 只能来自 finite local product或独立 theorem。
3. `NO_AE_TO_POINT`：不得把 full-measure set自动包含 arithmetic seed。
4. `NO_FULL_PERIOD_TO_DIAGONAL`：不得把 `G_k` full-cycle mean直接赋给长度 `N`
   的 physical prefix。
5. `NO_WORD_ONLY_ISOMORPHISM`：必须保持 stage、event、measure、seed、physical
   functional与 loss ledger。
6. `NO_EXTENSION_MAGIC`：若 event只依赖 arithmetic base，generic fiber/Hénon lift
   不能改变 base hit sequence。
7. `NO_WEAKER_NORMALIZATION`：logarithmic、averaged或 renormalized model result必须
   显式支付回 natural physical count的全部 losses。
8. `NO_HAAR_ENDPOINT_CENTERING`：full-cycle Haar mean不得默认成为 critical physical
   main；必须给 pair-sieve/Buchstab profile或独立 endpoint theorem。
9. `NO_QUADRATIC_INVERSE`：post-TT-star pair/Gram数据不得逆生 pre-TT-star signs或
   linear occurrence carrier。

任何一项失败就标记该 construction `STOP_SCOPED`；不再衍生一串微型修补论文。

## 9. 两种 proof engine，只服务同一 endpoint

Review3 的四路汇流现在按 typed graph解释。实线只有各 component内部的 exact arrows；
packet/O161到 primorial/physical carrier的箭头仍是虚线：

```text
pre-TT-star actual linear carrier                        [H_occ OPEN]
          |
          v
determinant-uniform fixed-atom Type II                  [OPEN]
          |
          v
small-content far-copy / target-coupled reassembly     [OPEN]
          |
          v
prime-producing lower bound                            [OPEN]
          |
          v
h0=2 endpoint / TPC

exact CRT resonance -> Haar Var=O(N) -> a.e. hits       [PROVED METRIC]
                                      -X-> seed 0       [NO FREE ARROW]
```

五个活接口的精确角色是：

| live interface | role | current first missing |
|---|---|---|
| analytic far-copy | 产生 target-coupled collective cancellation/covariance | `Q^3/J` saving / raw zero-column Bessel |
| nonautonomous dynamics | 若能保持 forcing与 physical evaluation，提供 Type-II/physical transfer机制 | target-independent forced-triangular intertwiner |
| two O161 fixed-atom parents | 提供 determinant-two literal local arithmetic cancellation | growing natural prescribed-atom fixed-power theorem |
| H_occ (legacy H1) | pre-TT-star source-backed linear occurrence carrier | actual edges、schedule、ranges与 normalization |
| pair-native | H_occ附着后的 post-TT-star quadratic analytic shadow | actual pair、opened `D`、pair-to-`omega`与 normalized return；无逆箭头到 H_occ |

这五项保持 route portfolio意义上的 `OPEN`；主控资源优先给能改变
`H_occ/H_dyn/H3_phys/H4`或把上述
合流图缩短的 theorem。只补接口字段但不改变主 ledger，仍不编号。

### Engine A: direct arithmetic/analytic

先构造 locally matched prime-producing comparison，再对 actual affine packets证明
uniform Type I、multiplicative Type II与 target-coupled Gram/Bessel reassembly。
TPC-32 small-content far-copy只有在 coefficientwise physical return完整支付后才给
credit；普通 marginal large sieve不算成功。

### Engine B: nonautonomous dynamical carrier

构造 observable-quotient `J_k,Q_k,Err_k`，显式处理 deletion forcing，先在一般
affine pattern class上产生可送入 Engine A 的 Type-II或 physical-evaluation estimate。
不得要求它在 full centered Haar space上同时 uniformly coercive与 uniformly
exponentially mixing；V16 exact scaled-isometry theorem已停止该版本。Haar variance
已经独立闭合，重复证明 typical recurrence不算成功；只证明 typical logistic orbit有
正 `LRL` mass也不算成功。

两个 engines可以并行，但不得生成两个互不相干的 paper chains。它们必须在
`H_occ/H_dyn/H3_phys`上产生状态变化；H4只是最终 arithmetic endpoint。

## 10. 当前 umbrella gate：primary 与 independent reserve

canonical umbrella继续是

```text
TPC_FM_EXACT_HALF_AND_HB4xHB2_VORONOI_GATE.
```

按岛屿地图的导航语义，Bridge A现在必须拆成两座 source-lock不同的桥：A1 是
两条 literal Möbius rows加两条 Gauss-dual rows的 centered Type-IV主桥；A2 是
四 Möbius rows加双 divisor-log columns的 paired-Voronoi reserve。固定原子岛与
Pair-native/H1岛是 attachment层，不自动提供桥梁 saving。Bridge B仍是
distinguished-seed genericity动力学大桥；Hénon/几何岛只作辅助提升，不给解析桥
credit。V15 canonical状态表为：

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
HB4_EXACT_HALF_ACTUAL_ATOM_DUAL_PRODUCT_DISPERSION = ANCESTOR_OPEN_REDUCED_TO_PROJECTOR_CORE
HB4_EXACT_HALF_INDUCED_GAUSS_CRT_SIGNED_PHASE_IDENTITY = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PHYSICAL_MINUS_TWO_G_S_UNIT_PHASE = PROVED_EXACT_SOURCE_LOCK
HB4_EXACT_HALF_LITERAL_MU_GQ_PRESERVATION_THROUGH_IMPRIMITIVE_CRT = STOP_SCOPED_FALSE_EXACT_COFACTOR_SIGN_CANCELLATION
HB4_EXACT_HALF_RAMANUJAN_COFACTOR_GCD_STRATIFICATION = PROVED_EXACT_FINITE
HB4_EXACT_HALF_PRIMITIVE_PROJECTOR_SINGLE_FIXED_PRODUCT = STOP_SCOPED_FALSE_DIVISOR_LATTICE
HB4_EXACT_HALF_RAMANUJAN_DIVISOR_MONOMIAL_UNFOLDING = PROVED_EXACT_FINITE
EARNST_ROOT_NUMBER_SQUARE_PRIME_MOMENT = SOURCE_BACKED_MECHANISM_ANALOGUE_NOT_ACTUAL_PACKET
FKMS_PRIME_MONOMIAL_TRACE_ENGINE = SOURCE_BACKED_LOCAL_PRIME_PROJECTOR_ATTACHMENT
HB4_EXACT_HALF_SIGNED_MODULUS_DUAL_TYPE_IV = RETYPED_PRE_CRT_SHORTHAND_ONLY
HB4_EXACT_HALF_SIGNED_CONDUCTOR_RAMANUJAN_COFACTOR_PRIMITIVE_PROJECTOR_DUAL_TYPE_IV = SELECTED_CONSTRUCTION_OPEN_NEW_THEOREM
HB4_EXACT_HALF_SMALL_PROJECTOR_ABSOLUTE_WEIL_DYADIC_BOUND = PROVED_CONTRACT_LEVEL_PARTIAL_THEOREM
HB4_EXACT_HALF_LARGE_COMPLEMENTARY_T_SMALL_PROJECTOR_WINDOW = PROVED_CONTRACT_LEVEL_POWER_SAVING
HB4_EXACT_HALF_LARGE_COMPLEMENTARY_T_STRICT_ENDPOINT_BUDGET = LOCAL_ONLY_DELTA_GT_1_OVER_150_PLUS_LEDGER_MARGIN
HB4_EXACT_HALF_LARGE_T_DIRECT_EARNST_TRANSFER = STOP_SCOPED_PRIME_EVEN_AFE_COEFFICIENT_AND_REASSEMBLY_MISMATCH
HB4_EXACT_HALF_LARGE_T_PHASE_BLIND_CHARACTER_LARGE_SIEVE = STOP_SCOPED_ROOT_NUMBER_AND_PROJECTOR_GEOMETRY_ERASED
HB4_EXACT_HALF_LARGE_T_AFE_REPLACEMENT_OF_ACTUAL_FOUR_POLYNOMIALS = STOP_SCOPED_FALSE_COEFFICIENT_SUBSTITUTION
HB4_EXACT_HALF_LARGE_T_CHARACTER_SIDE_PROJECTOR_COMPLEMENT_SELECTION = STOP_SCOPED_T_NOT_INTRINSIC_BEFORE_PROJECTOR_EXPANSION
HB4_EXACT_HALF_PRIME_PROJECTOR_FKMS_E1E2_WINDOW = PROVED_CONTRACT_LEVEL_FOUR_THIRDS_TO_FORTY_TWO_OVER_THIRTY_ONE_MINUS_EPSILON
HB4_EXACT_HALF_PRIME_PROJECTOR_FKMS_STRICT_ENDPOINT_BUDGET = LOCAL_ONLY_EPSILON_GT_9_OVER_1550_PLUS_LEDGER_MARGIN
HB4_EXACT_HALF_COMPOSITE_PROJECTOR_ABOVE_FOUR_THIRDS = ANCESTOR_OPEN_REDUCED_TO_THREE_HALVES_CORE
HB4_EXACT_HALF_PRIME_PROJECTOR_AT_OR_ABOVE_FORTY_TWO_OVER_THIRTY_ONE = ANCESTOR_OPEN_REDUCED_TO_THREE_HALVES_CORE
HB4_EXACT_HALF_REDUCED_PROJECTOR_CORE_DISPERSION = ANCESTOR_OPEN_REDUCED_TO_THREE_HALVES_CORE
BP2607_COMPLETE_BILINEAR_KLOOSTERMAN_L2 = SOURCE_BACKED_ANY_MODULUS_UNNORMALIZED
HB4_EXACT_HALF_INVERSE_RESIDUE_TWO_ROW_TRANSFER = PROVED_EXACT_NORM_PRESERVING
HB4_EXACT_HALF_ALL_SQUAREFREE_INVERSE_RESIDUE_WINDOW = PROVED_CONTRACT_LEVEL_FOUR_THIRDS_TO_THREE_HALVES_MINUS_DELTA
HB4_EXACT_HALF_ALL_SQUAREFREE_INVERSE_RESIDUE_STRICT_BUDGET = LOCAL_ONLY_DELTA_GT_1_OVER_200_PLUS_LEDGER_MARGIN
BP2607_NONTRIVIAL_INTERVAL_BOUND_AFTER_INVERSION = STOP_SCOPED_INVERSE_SUPPORT_NOT_SHORT_INTERVAL
HB4_EXACT_HALF_THREE_HALVES_PROJECTOR_CORE_DISPERSION = ANCESTOR_OPEN_REDUCED_TO_TOP_PROJECTOR_COLLAR
HB4_EXACT_HALF_RAMANUJAN_DIVISOR_PRODUCT_FIBER_TRANSFER = PROVED_EXACT_FINITE
HB4_EXACT_HALF_MULTIPLICATIVE_GAUSS_SQUARE_OPERATOR = PROVED_EXACT_ANY_ODD_SQUAREFREE
HB4_EXACT_HALF_PRODUCT_FIBER_COLLISION_ENERGY = PROVED_ELEMENTARY_COMPOSITE_UNIFORM
HB4_EXACT_HALF_ALL_SQUAREFREE_PRODUCT_FIBER_WINDOW = PROVED_CONTRACT_LEVEL_TO_TWO_MINUS_DELTA
HB4_EXACT_HALF_ALL_SQUAREFREE_PRODUCT_FIBER_STRICT_BUDGET = LOCAL_ONLY_DELTA_GT_1_OVER_50_PLUS_FOUR_LEDGER_MARGIN
PASCADI_DI_TOP_PROJECTOR_ATTACHMENT = STOP_SCOPED_ENDPOINT_OR_MODULUS_WEIGHT_LOCATION_MISMATCH
BRS_MODULUS_SECOND_MOMENT_TOP_PROJECTOR_ATTACHMENT = STOP_SCOPED_MOVING_INDEX_AND_MOBIUS_WEIGHT_MISMATCH
HB4_EXACT_HALF_TOP_PROJECTOR_MOBIUS_GAUSS_SQUARE_FOUR_POLYNOMIAL_DISPERSION = ANCESTOR_OPEN_REDUCED_TO_NEAR_PRIMITIVE_COLLAR
HB4_EXACT_HALF_TOP_INDUCED_CONDUCTOR_DECOMPOSITION = PROVED_EXACT_FINITE
HB4_EXACT_HALF_TOP_COMMON_COEFFICIENT_PRIMITIVE_LARGE_SIEVE = PROVED_SOURCE_BACKED_CONTRACT_LEVEL
HB4_EXACT_HALF_TOP_LARGE_SECONDARY_COFACTOR_CUTOFF = PROVED_CONTRACT_LEVEL_P_MINUS_MIN_ONE_TWO_KAPPA
HB4_EXACT_HALF_TOP_LARGE_SECONDARY_COFACTOR_STRICT_BUDGET = LOCAL_ONLY_MIN_ONE_TWO_KAPPA_MINUS_LEDGER_GT_ONE_OVER_200
HB4_EXACT_HALF_TOP_FROZEN_SUPERCLASS_PRIMITIVE_AVOIDANCE = STOP_SCOPED_FALSE_LITERAL_MOBIUS_SMOOTH_EQUAL_ROW
HB4_EXACT_HALF_TOP_ACTUAL_ATOM_PRIMITIVE_AVOIDANCE = OPEN_ATTACHMENT
HB4_EXACT_HALF_TOP_PHASE_BLIND_FOURTH_MOMENT_LARGE_SIEVE = STOP_SCOPED_EXACT_PRIME_DIAGONAL_FLOOR
HB4_EXACT_HALF_TOP_OUTER_MU_ALONE = STOP_SCOPED_PRIME_SIGN_CONSTANT
HB4_EXACT_HALF_TOP_NEAR_PRIMITIVE_GAUSS_SQUARE_FOUR_POLYNOMIAL_ANGLE = SELECTED_CORE_OPEN_NEW_THEOREM
HB4_EXACT_HALF_TOP_BOUNDED_SUBPOWER_M_PRIMITIVE_ROOT_NUMBER_ANGLE_RETYPE = PROVED_EXACT_FINITE
HB4_EXACT_HALF_TOP_PRIME_GAUSS_ROOT_RECIPROCAL_ADDITIVE_FACTORIZATION = PROVED_EXACT_FINITE_REFINEMENT_OF_V9_NO_SAVING
HB4_EXACT_HALF_TOP_GAUSS_ROOT_SPLIT_PHASE_BLIND_L2_TTSTAR = STOP_SCOPED_EXACT_NONPRINCIPAL_ISOMETRY_ENDPOINT
HB4_EXACT_HALF_TOP_COMPLETE_PHASE_C_SECOND_MOMENT = PROVED_EXACT_FINITE
HB4_EXACT_HALF_TOP_COMPLETE_PHASE_C_AVERAGE_TO_PRESCRIBED_CV = STOP_SCOPED_PRESCRIBED_PHASE_AND_SHORT_FAMILY_MISMATCH
HB4_EXACT_HALF_TOP_GENERIC_PRIME_TRACE_BILINEAR_RELATIVE_TO_GAUSS_UNITARY = STOP_SCOPED_SOURCE_SAVING_BELOW_EXACT_OPERATOR_BASELINE
HB4_EXACT_HALF_TOP_EARNST_ACTUAL_PACKET_ATTACHMENT = STOP_SCOPED_PRIME_EVEN_AFE_COEFFICIENT_FIXED_TWIST_L1_AND_PARITY_MISMATCH
HB4_EXACT_HALF_TOP_FIXED_M_TO_SUBPOWER_M_SUMMATION = CONDITIONAL_POLYNOMIAL_UNIFORM_CONSTANTS_SUFFICE
HB4_EXACT_HALF_TOP_PRIME_DOMINATED_SQUAREFREE_CONDUCTOR = CONDITIONAL_ON_TENSOR_STABLE_ACTUAL_PRIME_ANGLE
HB4_EXACT_HALF_TOP_SMOOTH_SQUAREFREE_CONDUCTOR_COMPLETION = OPEN_NEW_COMPOSITE_OR_COMPLETELY_BOUNDED_TENSOR_THEOREM
HB4_EXACT_HALF_TOP_ACTUAL_FOUR_POLYNOMIAL_ROOT_NUMBER_SQUARE_MASTER = SELECTED_CORE_OPEN_NEW_THEOREM
```

1. **Primary：HB4 exact-half dual-product dispersion**。V9 已把 Gauss-square
   character angle精确化为 prescribed residue的 centered product convolution：

   ```text
   Q_p(-2)=sum_(e_1e_2zw=-2 mod p)
     mu(e_1)W_1(e_1)mu(e_2)W_2(e_2)U_p^sharp(z)V_p^sharp(w).
   ```

   完整 prime cell为 `mu(p)Q_p(-2)`，nonprincipal gate为
   `(p-1)/p[Q_p(-2)-M_p/(p-1)]`。这是 exact finite equivalence，不是 arithmetic
   saving。V9 当时的 first subgate是
   `HB4_EXACT_HALF_ACTUAL_ATOM_DUAL_PRODUCT_DISPERSION`：在冻结、可测试的 source
   superclass上证明 normalized discrepancy `F^(2-eta)`，等价 prime cell
   `F^(4-eta)`；支付 strict `1/400`需最终 `eta>1/100`。actual atom逐项 membership、
   dual tails与 full source reassembly仍须显式支付。common-`k` unique-fiber因
   `be-ah=tp`的 `t!=0` wraps而 `STOP_SCOPED`；global moving-unit Cauchy也被 exact
   product-resonance endpoint floor封死。V10 已完成 squarefree/imprimitive exact
   lift，并证明 literal `mu(gq)`不会原样穿过 CRT：cofactor sign精确相消；剩余对象
   是 conductor root-number-square coordinate，或等价的 `rho|r` primitive-projector
   divisor lattice。进一步展开 `c_s(ell)`后，选中的构造目标变为
   `HB4_EXACT_HALF_SIGNED_CONDUCTOR_RAMANUJAN_COFACTOR_PRIMITIVE_PROJECTOR_DUAL_TYPE_IV`，
   保留 `mu(g)mu(rho)mu(b)`与 monomial
   `u k/(g e_1e_2 a b^2 t^2) (mod rho)`，不在 unresolved outer-variable层先取
   绝对值。Earnst root-number-square moment仍只是机制蓝图。V11 已先闭合
   all-squarefree small-projector段与 prime FKMS段；V12进一步在
   `rho>=F^(4/3)`把两条 literal `e_i`行按 modular inverse单射重排，并在完整
   residue hull中补零。Blomer--Pascadi Lemma 5.1/complete additive Parseval给
   unnormalized local bound `F rho`，完整 outer ledger为
   `F^3rho^(2+o(1))`。因此 prime与 composite统一在
   `F^(4/3)<=rho<=F^(3/2-delta)`闭合，`eta_D<delta`；局部 strict budget需
   `delta>1/200`加 margin。剩余 first subgate已缩成
   `HB4_EXACT_HALF_THREE_HALVES_PROJECTOR_CORE_DISPERSION`。restricted windows可因
   自己已支付 target而取 outer绝对值；未解 `3/2` core仍不得丢掉三条 signs再
   声称 collective credit。
2. **Independent reserve：HB4xHB2 structured two-row paired-Voronoi**。在
   exactly-swapped shells上联合处理 source `A1-A2`；乘 outer `-6`后 physical顺序
   为 `A2-A1`。它对两条 weighted `mu_F*mu_F` rows与
   两条 truncated ordered Eisenstein columns的 `ER-AB=2`（含全局 `6/log X`）
   collective error建立新 theorem。先压成 arbitrary residue rows会得到 operator
   norm精确为 `q`的 additive-difference Kloosterman kernel，因此该 shortcut已
   `STOP_SCOPED`；reserve必须保留四个 literal Möbius slots、双行 incidence与两个
   ordered divisor-log columns。legal first transform已经导出并显示 `A_2`为 double
   Voronoi、`A_1`为 single Voronoi加未变换 smooth-log列；当前先缺 collective
   polar-main attachment，随后须从 direct DFI的 `F^7` ledger联合回收 `F^3`到
   physical `F^4`。

两条 source lock不得拼接。调度上保留 prime modulus、`g=1`、单个 source atom的
centered dual-product theorem作为 first falsifier；full bridge现在不再重做已闭合的
small-projector、FKMS或 inverse-residue Parseval窗口，而是直接攻
`rho=F^(3/2-o(1))` collar及全部 `rho>=F^(3/2)` core，尝试把 outer modulus、
`u,k`与三条 signed axes编译成 collective theorem。
同时独立展开 paired-Voronoi的 polar/zero/Bessel ledger。
Target-coupled reassembly/crosslink继续作为 portfolio-level `OPEN/RESERVE`，不属于
本轮 current umbrella gate。只有上述两个解析门之一先发生 theorem-backed变化，才另行
要求逐 coefficient operator `Sigma_k J_X L_X c_X=nu_X W_k+R_X`与 paid physical
norm return；不得提前把这条历史动作计成当前第三 target。

下一轮结束时只允许三种高层结果：

```text
CHANNEL_ADVANCE: H_occ, H_dyn or H3_phys genuinely improved;
CHANNEL_REDESIGN: stress/circularity test found a fatal and the spine changed;
CHANNEL_STOP: both engines fail a named master criterion.
```

“又审核了若干相近 source，但主 ledger未变”不再作为独立研究 release。

## 11. V11 后的罗盘：红色断桥已经向前移动

按用户给出的 TPC 岛屿地图，Bridge A1 现在有两段黄色实桥：

```text
all squarefree projector P <= F^(4/3-delta)
    -- Ramanujan L1 + composite Weil --> contract-level saving;

prime projector F^(4/3) <= P <= F^(42/31-epsilon)
    -- FKMS l=3 on literal e1,e2 rows --> contract-level saving.
```

第一段 dyadic bound为 `F^4P^(3/2+o(1))`，第二段为
`F^(11/3)P^(31/18+o(1))`。这不是数值启发，也不是把摘要改写成 theorem；两段都在
V10 exact normal form、actual masks与 physical raw target `F^6`上逐项核算。
所有 `asymp`常数只在缩小任意 fixed exponent margin后吸收；dyadic scale `P`
不得在 exact identity中替换 literal modulus `rho`。

地图上的 Bridge A红色断点现在移到：

```text
all-squarefree lower collar P=F^(4/3-o(1)) below F^(4/3),
composite squarefree P >= F^(4/3),
or prime upper collar/core P >= F^(42/31-o(1)).
```

这里的 `o(1)`只表示下一轮必须处理临界窄带，不能冒充固定 saving。下一条大路是
`HB4_EXACT_HALF_REDUCED_PROJECTOR_CORE_DISPERSION`，优先寻找以下两种之一：

1. 对 varying/composite `P`保留 `mu(P)`的 Kuznetsov/dispersion/trace-family theorem；
2. 在 prime core中把 `u,k`或 outer modulus纳入真正的 multilinear grouping，把
   `42/31`墙向前推。

Earnst large-`t` direct transfer、phase-blind primitive large sieve与 AFE coefficient
replacement均已精确 `STOP_SCOPED`。Bridge A2、Bridge B和 Hénon辅助路线仍独立；它们
没有因 V11 自动取得 credit。actual atom与全局 physical gates未闭合，所以这张地图
显示的是“已有一段可走的大路”，不是 TPC proof。

## 12. V12 后的罗盘：两堵旧墙合并为 `3/2` 新墙

V12在 V10 exact packet上冻结

```text
C=-2uk conjugate(g a b^2 t^2)_rho,
m=conjugate(e_1)_rho,
n=conjugate(e_2)_rho.
```

对 `rho>=F^(4/3)`，两条 actual `e_i~F`支撑短于 `rho`，所以 modular inverse
逐条单射；complete-residue zero padding精确保留两条 `L2` norm，且

```text
S(1,C conjugate(e_1e_2);rho)=S(Cm,n;rho).
```

[Blomer--Pascadi Lemma 5.1](https://arxiv.org/abs/2607.24311)或其 complete
additive Parseval证明给出任意模数、unnormalized estimate

```text
local e_1,e_2 sum << rho ||alpha||_2||beta||_2 << F P X^o(1),
full dyadic cell   << F^3P^(2+o(1)).
```

故所有 squarefree projectors统一获得

```text
F^(4/3)<=P<=F^(3/2-delta)
  ==> any eta_D<delta.
```

旧 `4/3` transition与 prime `42/31`墙不再属于 current core。新红色断桥是

```text
P=F^(3/2-o(1)) below F^(3/2),
and all squarefree P>=F^(3/2).
```

BP2607 的 nontrivial short-interval theorem不能把 scattered inverse support的
cardinality `F`偷换成 interval length；这个 direct extension精确 `STOP_SCOPED`。
下一轮只寻找保留 moving inverse phase并利用 varying `rho`、`u/k`或 outer Möbius
signs的 collective theorem。`GLOBAL_MOVING_UNIT_CAUCHY`仍是另一条全域 shortcut的
historical STOP，不因本段重开。

岛屿地图上只有 Bridge A1 的红色断点向前移动。A2 paired-Voronoi、Bridge B
distinguished-seed genericity与 Hénon辅助岛继续独立；actual atom、all-`D`、exact
cover、tails、A/B、global normalization与 provenance仍 OPEN。因此 fixed-atom
credit=`0`、global strict `1/400=UNPAID`、`L2=NONE`、TPC-207 trigger=`false`。

## 13. V13 后的罗盘：只剩 projector 轴的顶端 `2` 墙

V13在 V10 exact packet上把此前只作为 nuisance支付的 Ramanujan row改造成
真正的乘法结构。squarefree `g`与 `(a,g)=1`给

```text
mu(g)c_g(ak)=sum_(v|g,v|k)mu(v)v,
```

再把 `e_1e_2`与 `uj`压成 `H=(Z/rho Z)^*`上的两个 product fibers。对应
Kloosterman kernel的乘法 Fourier eigenvalue精确为

```text
chi(c_v)tau_rho(conjugate chi)^2,
```

故 odd-squarefree/imprimitive operator norm至多 `rho`。ordinary integer product
collision energy支付两个 fiber后，完整 outer ledger是

```text
|V(P)| << F^5P^(1/2)X^o(1).                          (13.1)
```

这把 V12 的 common `3/2`墙整体穿过：

```text
P<=F^(2-delta)
  ==> every fixed eta_D<delta/4.
```

在旧 `P=F^(3/2)`处已有 supremal local budget `1/8`；支付 downstream
`D^lambda_D`后，local strict `eta_D>1/200`要求
`delta>1/50+4lambda_D`。

新的红色断桥只剩

```text
P=F^(2-o(1)) top-projector collar.
```

exact `P=F^2`时 phase-blind product-fiber operator恰返回 `F^6`。下一步必须利用
outer `mu(rho)`、primitive projection或 actual fibers对 maximal Gauss-square
eigenspaces的避让，而不是再堆一个局部 Kloosterman bound。Pascadi DI top cell与
BRS fixed-index modulus second moment均已 scoped screen：前者仍 endpoint，后者不接受
随 `rho`移动的 inverse index及 literal `mu(rho)`。

`GLOBAL_MOVING_UNIT_CAUCHY`保持历史 STOP；V13只在 exact top endpoint与其
resonance会合。岛屿地图上只有 Bridge A1断点前移到最大 projector端；A2、Bridge B
和 Hénon辅助岛保持独立。actual atom、all-`D`、exact cover、tails、A/B、global
normalization与 provenance仍 OPEN，故 TPC-207 trigger仍为 `false`。

## 14. 对外成果的最终压缩目标

如果主通道存活，TPC-1--206 的最终外部形态应压缩为：

1. 一篇 obstruction/type-system synthesis，解释为何常见伪桥失败；
2. 一篇 parity-breaking affine-transference bold-channel paper，明确 typed gates与
   PBAPT master theorem；
3. 只为真正关闭 `H_occ/H_dyn/H3_phys/H4` 的少数技术论文；
4. 一个可复现 repository，保留 200+ research nodes作为审计证据库。

在形成 theorem-backed channel advance前，不创建 TPC-207，不构建 paper/PDF。

## 15. V14 后的罗盘：墙已缩成 near-primitive phase collar

V14把 V13 的 top-projector wall再分型一次。写

```text
rho=fm,  f=cond(chi),  chi=Ind_f^(fm)psi.
```

Gauss-square eigenvalue大小为 `f`，但更重要的是 exact phase与 sign为

```text
mu(f)mu(m)/[phi(f)phi(m)]
  * psi(c_v)conjugate(psi)(m)^2 tau_f(conjugate psi)^2.
```

每条 polynomial还带 `(n,m)=1`。对 common-coefficient source contract，固定
`m`后的 primitive large sieve给出

```text
V_(m>=M)<<[F^4+F^2P^2/M^2]X^o(1).
```

因此对任意 fixed `kappa>0`，`m>=P^kappa`全部成为已支付海域；在
`P=F^2=D`上的 saving为 `D^(-min(1,2kappa)+o(1))`。罗盘上的红色断点不再覆盖
整个 `P=F^2`谱面，而只覆盖

```text
m<P^kappa for every fixed kappa>0:
primitive + bounded/subpower-cofactor induced collar.
```

这里“subpower collar”是 exponent-topological说法：每个 fixed-power cofactor尾都
已闭合，并不声称存在一个对 `kappa->0`一致的 quantitative theorem。

两条看似自然的路已被 exact firewall排除：

1. conductor/primitive projection本身不够。`rho=51,f=17,m=3`的 normalized
   coefficient精确为 `17/32`；bounded cofactor没有 fixed power。
2. phase-blind spectral avoidance不够。prime modulus的 nonprincipal谱全部是 maximal
   Gauss-square eigenspace，literal Möbius/smooth equal rows已有 endpoint fourth-moment
   floor；`mu(p)=-1`在 prime sector又是常数。

这两个 STOP都只是 mechanism/superclass结论，不是 actual signed packet下界。
未提交的探索性 numerical proxy不作为本轮证据；罗盘只依据上述 exact firewalls
选择保留 phase，而不是放弃解析桥。

所以 Bridge A1 当前唯一主关是

```text
HB4_EXACT_HALF_TOP_NEAR_PRIMITIVE_GAUSS_SQUARE_FOUR_POLYNOMIAL_ANGLE.
```

它有两个可接受出口：fixed-prime/near-primitive actual angle theorem，或完整
varying-squarefree outer-`mu` collective theorem。二者都必须保留 actual coefficients、
fixed physical `h0=2`、physical `c_v`、masks、signed shells、orientation、uniform
parameters与全部 losses。A2 paired-Voronoi、Bridge B distinguished seed与 Hénon
辅助岛仍是独立桥，不拼接 credit。当前仍是 contract-level partial advance；
fixed atom=`0`、global `1/400=UNPAID`、`L2=NONE`、TPC-207=`false`。

## 16. V15 后的罗盘：不是再找“非平凡界”，而是越过 unitary 基线

V15把 A1 红色断点从一句宽泛的 “Gauss-square angle” 压成两扇有顺序的门：

```text
A1.1 actual prescribed-phase prime root-number-square moment
  -> A1.2 tensor-stable smooth-squarefree conductor completion.
```

第一扇门的 exact对象是 `(15.1)` 的四 polynomials；它必须相对仓库已有
Gauss-unitary Cauchy基线再赢 `p^(-sigma_D)`，而不是只相对 Weil逐项估计非平凡。
这是本轮最重要的罗盘修正。现有 KMS/FKMS trace bounds与 Earnst AFE moment都没有
literal支付这条差额，所以它们被精确 `STOP_SCOPED`，但不否定未来的
coefficient-sensitive theorem。

Gauss-root factorization给出一个更大胆、也更具体的构造视角：actual Möbius/smooth
rows经过两枚 reciprocal additive transforms后，问题成为一个 prescribed inverse-pair
correlation。完整 phase平均只有 exact second-moment/RMS identity导航；只有额外
spectral spread时才启发式呈 square-root型。physical `c_v`不是随机 phase，不能靠
平均直接得到。因而可继续探索的 theorem形态只有两类：

1. 直接利用 literal Möbius rows证明 uniform prescribed-phase high moment / dispersion；
2. 在 outer variables或 moduli上建立仍保留 moving inverse index与 literal signs的
   collective theorem，使 physical短 phase family本身获得 genericity。

第二扇 composite门要求 completely bounded/tensor-stable uniformity。若
`f=ps`、`ms=P^o(1)`，prime theorem可条件处理 prime-dominated层；若 `f` smooth，逐
prime scalar bounds不够，必须有真正 composite theorem。

这意味着解析 A1 已经从“搜索现成估计”进入“定义新主定理”的阶段。下一轮的大路
探索优先级转向 Bridge B 的 moving rare-event mass、covariance与 distinguished-seed
genericity：不是把遍历性直接改写成孪生素数，而是看动力学桥能否产生 A1缺少的
prescribed-phase genericity。A1、A2与 Bridge B仍不拼接 theorem credit；这里改变的
只是探索优先级。全局状态仍为 fixed atom=`0`、strict `1/400=UNPAID`、`L2=NONE`、
TPC-207=`false`。

## 61. V60 后的罗盘：zero-hole complete-graph edge frame替代不稳定 DFT split

V60 已把 physical moving-hole defect支付到 `x^(53/32+o(1))`，所以 Gate-B剩余对象是
standard-zero-hole、prime-only、`q`-weighted、kernel-localized、exact-diagonal-
subtracted signed four-packet remainder。V60 `ROUND2_CLUE`建议分别处理 additive DFT
equal/off-equal frequencies；V61 的 residue-zero spike反例证明该估计顺序不稳定：

```text
equal piece     = +(q-1)|L|^2/q,
off-equal piece = -(q-1)|L|^2/q,
true V_0        = 0.
```

正确 invariant object是 nonzero frequencies上的 complete-graph Laplacian。令
`y=(A_hat(k))_(k!=0)`、`P=I-11*/(q-1)`，则

```text
V_0 = q^-1 y*Py
    = 1/[q(q-1)] sum_{{k,l} in E(K_(q-1))} |T_(k,l)|^2.
```

edge mass exact为 `q(q-2)1_(q does not divide n)`，所以 V59 mandatory
`(q-2)/(q-1)` diagonal逐 edge删除，保留 outer `q` 后

```text
qR_0 = 1/(q-1) sum_e E_e^circ.
```

four-packet polarization逐 cell成立；contracted physical kernel在 nonunit为 `0`、
equal units为 `q(q-2)`、distinct units为 `-q`，除以 `q-1` 后 exact返回 V59
`q u_1` coefficient。oriented fibers满足

```text
Delta_(k,k+d)(n)=e_q(-kn)(1-e_q(-dn)),
weight = 1/[2(q-1)], d!=0, k!=0,-d.
```

V61 又证明 literal edge no-sparsification：projection的 `(k,l)` entry只由 edge
`{k,l}`贡献，故每个 weight都强制为 `1/(q-1)`。这只停止 strict literal edge subset；
dense basis与 whole-frame joint theorem仍 OPEN。

```text
V61_ROUTE_ADVANCE = YES
V61_STRUCTURAL_THRESHOLD_A = PASS
V61_ZERO_HOLE_ADDITIVE_EDGE_FRAME = PROVED_EXACT
V61_CELLWISE_Q_MINUS_2_DIAGONAL_CANCELLATION = PROVED_EXACT
V61_LITERAL_EDGE_SPARSIFICATION = REFUTED
V61_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
V61_ARITHMETIC_ADVANCE = NO
V61_FIXED_ATOM_CREDIT = 0
V61_L2 = NONE
V61_TPC_208_TRIGGER = true
```

当前最窄施工命令是：对完整 `(d,k)` tight frame先作 Möbius/Poisson transform，禁止
在 edge或 fiber层提前 triangle；测试 transformed cells是否共享一个 dual variable。
若 shared variable成立，才接 Blomer--Pascadi/Pascadi post-emitter engine；若不成立，
把 multiplicity loss写成 precise obstruction。TPC-208是 structural L1 release，不是
arithmetic advance；TPC-209尚未触发。

## 60. V59 后的罗盘：Gate-B joint product 极化为四个 prime-BDH packets

V59 保留 V58 exact `C_*=mathfrak C_x^(V35)`，并用
`x conjugate(y)=(1/4)sum_(j=0)^3 i^j|x+i^j y|^2` 把 character product
逐字重写为四个单序列 `a^(j)=beta+i^j w` 的 prime-weighted、kernel-localized、
diagonal-subtracted BDH remainders。每个 prime row必须扣 `(q-2)` 份 diagonal；
四个 remainders有正有负，不能先逐项绝对值再声称 exact endpoint。

physical length `H=x^(21/32)` 的 smooth block compiler给 natural ledger

```text
block count          = x^(11/32+o(1))
q-weighted block     = x^(127/96)
collective baseline  = x^(5/3)
Q^2/H                = x^(1/96).
```

Blomer--Pascadi critical fixed-q saving `q^(-1/32)` 在 `q~x^(1/3)` 上也恰为
`x^(-1/96)`。这是精确 clock match，但 source从 already-emitted bilinear
Kloosterman cell开始；literal four-packet BDH、prime-only shell、zero/nonunit axes、
block tails与 collective signed reassembly尚无 compiler。

Harper general-sequence BDH修复了“必须是特殊系数”的 architecture mismatch，却没有
直接附着：global ambient range不对；改用 block length后，平移会移动 source
`(a,q)` grouping中的 distinguished zero residue；all-moduli signed remainder也不能
抽取 prime subset。KMT、Pascadi、Wright分别仍有 coefficient、post-emitter、
fixed-residue type mismatch。

当前位置：**岛 2 / Bridge A / Gate B 的 polarized prime-BDH construction zone**。
下一大步不是再找一个 fixed-q 微估计，而是证明一个 collective compiler，把四个
literal packets送入 local engine后以总损耗 `<19/2400` 拼回。Gate-A full-shell root
仍是另一座独立 pier；q-transverse variance仍只服务 moving prefixes。

```text
V59_MAXIMUM_CLAIM = EXACT_COMPLEX_POLARIZATION_REPRESENTS_THE_V35_V58_GATE_B_SCALAR_AS_A_SIGNED_FOUR_PACKET_PRIME_WEIGHTED_KERNEL_LOCALIZED_OFFDIAGONAL_BDH_REMAINDER_AND_IDENTIFIES_THE_MISSING_COLLECTIVE_POWER_SAVING_COMPILER
V59_ROUTE_ADVANCE = YES
V59_CONDITIONAL_BRIDGE_ADVANCE = YES
V59_ARITHMETIC_ADVANCE = NO
V59_FIXED_ATOM_CREDIT = 0
V59_STRICT_1_OVER_400 = UNPAID
V59_L2 = NONE
V59_TPC_207_TRIGGER = false
V59_NUMBERED_RELEASE = NO
V59_DERIVATION_STATUS = COHERENT_AFTER_V35_V58_SCALAR_FREEZE_V36_CHARACTER_FORM_EXACT_COMPLEX_POLARIZATION_REDUCED_RESIDUE_BDH_CROSSWALK_BLOCK_SCALE_LEDGER_SOURCE_AUDIT_AND_FINITE_FALSIFIERS
V59_ASSUMPTION_POLICY = NO_BDH_OR_KLOOSTERMAN_POWER_BOUND_IS_ASSUMED__THE_FOUR_PACKET_AND_LOCAL_COLLECTIVE_THEOREMS_REMAIN_OPEN
V59_SELECTED_RESEARCH_ROUTE = FOUR_LITERAL_POLARIZED_PRIME_BDH_PACKETS_THEN_MESOSCOPIC_BLOCK_COMPILER_THEN_BLOMER_PASCADI_CELLS_THEN_COLLECTIVE_SIGNED_REASSEMBLY
V59_CLAIM_CLASS_POLICY = PROVED_EXACT_COMPILER__SOURCE_BACKED_ARCHITECTURE__SOURCE_BACKED_LOCAL_ENGINE__CONJECTURAL__NO_GO
V59_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__TARGET_5_OVER_3_MINUS_DELTA__DELTA_STRICTLY_GREATER_THAN_1_OVER_400
V59_GATE_B_SCALAR = RETAINED_EXACT_C_STAR_EQUALS_MATHFRAK_C_V35
V59_V36_CHARACTER_FORM = RETAINED_EXACT_B_TIMES_W_MINUS_ONE_Z_PER_NONPRINCIPAL_CHARACTER
V59_CONJUGATE_PACKET = PROVED_EXACT_W_Q_CHI_EQUALS_CONJUGATE_D_Q_CHI_FOR_REAL_PHYSICAL_W
V59_COMPLEX_POLARIZATION = PROVED_EXACT_X_CONJUGATE_Y_EQUALS_ONE_QUARTER_SUM_IJ_ABS_X_PLUS_IJ_Y_SQUARED
V59_FOUR_LITERAL_SEQUENCES = DEFINED_A_J_EQUALS_BETA_PLUS_I_POWER_J_W_FOR_J_ZERO_TO_THREE
V59_REDUCED_RESIDUE_VARIANCE = PROVED_EXACT_NONPRINCIPAL_CHARACTER_PARSEVAL_ON_UNIT_CLASSES
V59_DIAGONAL_MULTIPLICITY = PROVED_EXACT_Q_MINUS_2_NONPRINCIPAL_CHARACTERS
V59_OFFDIAGONAL_BDH_REMAINDER = DEFINED_PRIME_WEIGHTED_KERNEL_LOCALIZED_VARIANCE_MINUS_EXACT_DIAGONAL
V59_GLOBAL_FOUR_PACKET_IDENTITY = PROVED_EXACT_MATHFRAK_C_EQUALS_ONE_QUARTER_SUM_IJ_V_CIRCLE_A_J
V59_DIAGONAL_POLARIZATION = PROVED_EXACT_ONE_QUARTER_SUM_IJ_ABS_BETA_PLUS_IJ_W_SQUARED_EQUALS_BETA_W
V59_REMAINDER_SIGN = PROVED_FINITE_FIXTURES_SHOW_BOTH_POSITIVE_AND_NEGATIVE_VALUES
V59_FOUR_ABSOLUTE_BDH_THEOREM = OPEN_STRONGER_SUFFICIENT_H_4BDH_DELTA
V59_FOUR_ABSOLUTE_POLICY = NOT_EQUIVALENT_TO_THE_SIGNED_ENDPOINT_SCALAR_AND_NO_FREE_TRIANGLE_CREDIT
V59_BLOCK_PARTITION = PROVED_EXACT_ORDERED_PAIR_PARTITION_BEFORE_POLARIZATION_AND_ABSOLUTE_VALUES
V59_LOCAL_POLARIZED_PACKETS = DEFINED_A_BC_J_EQUALS_ETA_B_BETA_PLUS_IJ_ETA_C_W
V59_EFFECTIVE_BLOCK_COUNT = PROVED_X_POWER_11_OVER_32_PLUS_O1_AFTER_SCHWARTZ_TAIL
V59_LOCAL_Q_WEIGHTED_BDH_SCALE = PROVED_X_POWER_127_OVER_96
V59_GLOBAL_NATURAL_SCALE = PROVED_X_Q_SQUARED_EQUALS_X_POWER_5_OVER_3
V59_MESOSCOPIC_CONDUCTOR_GAP = PROVED_Q_SQUARED_OVER_H_EQUALS_X_POWER_1_OVER_96
V59_BLOMER_PASCADI_CRITICAL_SAVING = SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_EQUALS_X_POWER_MINUS_1_OVER_96
V59_BLOMER_PASCADI_ATTACHMENT = SOURCE_BACKED_LOCAL_ENGINE_AFTER_FIXED_Q_BILINEAR_KLOOSTERMAN_CELL_EMISSION_ONLY
V59_SELECTED_LOCAL_COLLECTIVE_THEOREM = OPEN_H_LOC_POL_DELTA_ON_THE_LITERAL_BLOCK_PRIME_PACKET_FAMILY
V59_REQUIRED_DELTA = STRICTLY_GREATER_THAN_1_OVER_400
V59_SELECTED_DELTA = 1_OVER_96
V59_SELECTED_GATE_B_NUMERATOR = X_POWER_53_OVER_32_PLUS_O1
V59_SELECTED_PHYSICAL_OUTPUT = X_POWER_95_OVER_96_PLUS_O1
V59_SELECTED_GATE_B_MARGIN = 19_OVER_2400
V59_TWO_SCALAR_ENDPOINT_COMPILER = RETAINED_V58_GATE_A_ROOT_PLUS_GATE_B_DELTA_IMPLIES_STRICT_PHYSICAL_SAVING
V59_Q_TRANSVERSE_PREFIX_THEOREM = RETAINED_OPTIONAL_ONLY_FOR_MOVING_PREFIXES
V59_HARPER_GENERAL_SEQUENCE_BDH = SOURCE_BACKED_CLOSEST_QUADRATIC_ARCHITECTURE_WITH_GENERAL_COMPLEX_SEQUENCE
V59_HARPER_GLOBAL_RANGE = STOP_SCOPED_UNSHIFTED_LITERAL_AMBIENT_X_HAS_Q_LESS_THAN_SQRT_X
V59_HARPER_BLOCK_NUMERICAL_WINDOW = PROVED_FORMAL_Q_SQUARED_OVER_H_EQUALS_X_POWER_1_OVER_96
V59_HARPER_TRANSLATION_ATTACHMENT = STOP_SCOPED_BLOCK_SHIFT_CHANGES_THE_DISTINGUISHED_ZERO_RESIDUE_IN_GCD_GROUPED_VARIANCE
V59_HARPER_MODULUS_SUBSET = STOP_SCOPED_ALL_DYADIC_MODULI_SIGNED_REMAINDER_DOES_NOT_CONTROL_PRIME_SUBSET
V59_HARPER_INPUT_CONDITIONS = OPEN_UNPROVED_FOR_FOUR_LITERAL_PACKETS_UNIFORMLY_IN_V_AND_BLOCK
V59_KLURMAN_MANGEREL_TERAVAINEN = SOURCE_BACKED_SHORT_PRIME_MODULUS_VARIANCE_FOR_BOUNDED_MULTIPLICATIVE_FUNCTIONS_WRONG_COEFFICIENT_CLASS
V59_PASCADI_EXCEPTIONAL_LARGE_SIEVE = SOURCE_BACKED_POST_EMITTER_SPARSE_FOURIER_KLOOSTERMAN_ENGINE_WRONG_PRE_EMITTER_OBJECT
V59_WRIGHT_CONVOLUTION = SOURCE_BACKED_TWO_Q_INDEPENDENT_FIXED_RESIDUE_ARRAYS_WITH_SIEGEL_WALFISZ_INPUT_WRONG_QUADRATIC_PACKET
V59_DIRECT_PRIMARY_SOURCE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_13
V59_FIRST_FATAL = NO_PRIMARY_THEOREM_PROVES_A_POWER_SAVING_PRIME_MODULUS_KERNEL_LOCALIZED_OFFDIAGONAL_BDH_REMAINDER_FOR_THE_FOUR_LITERAL_POLARIZED_SEQUENCES_OR_COMPILES_THEIR_BLOCKS_COLLECTIVELY_TO_THE_BLOMER_PASCADI_CELLS
V59_FINITE_COMPLEX_POLARIZATION_FIXTURE = PROVED_2_PLUS_3I_AND_MINUS_1_PLUS_2I_GIVE_4_MINUS_7I
V59_FINITE_Q5_CROSS_FIXTURE = PROVED_BETA_1_MINUS2_3_0_AND_W_2_1_MINUS1_4_GIVE_MINUS15
V59_FINITE_Q5_SIGN_FIXTURE = PROVED_EQUAL_PAIR_GIVES_MINUS2_AND_OPPOSITE_PAIR_GIVES_PLUS2
V59_FINITE_Q5_DIAGONAL_FIXTURE = PROVED_CORRECT_MINUS15_WRONG_Q_MINUS1_GIVES_MINUS12_AND_OMITTED_SUBTRACTION_GIVES_MINUS24
V59_FINITE_TRANSLATION_FIXTURE = PROVED_Q5_EXCLUDING_ZERO_GIVES_3_OVER_4_WHILE_EXCLUDING_ONE_GIVES_75
V59_FINITE_PRIME_SUBSET_FIXTURE = PROVED_SIGNED_ROWS_R5_1_R6_MINUS1_HAVE_ALL_SUM_ZERO_AND_PRIME_SUBSET_ONE
V59_GENERIC_SEQUENCE_THEOREM = NO_GO_DIVISOR_ENVELOPES_ALONE_ALLOW_COHERENT_ONE_RESIDUE_NATURAL_SCALE
V59_PER_BLOCK_PRIME_PACKET_TRIANGLE = NO_GO_RETURNS_X_POWER_5_OVER_3_NATURAL_SCALE
V59_DIAGONAL_RESTORATION = NO_GO_RETURNS_UNKNOWN_PHYSICAL_SCALAR_AT_X_POWER_5_OVER_3_SCALE
V59_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED_NO_NUMERICAL_CLOCK_TO_ATTACHMENT_PROMOTION
V59_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_POLARIZED_PRIME_BDH_NORMAL_FORM_MESOSCOPIC_CLOCK_AND_COLLECTIVE_COMPILER
V59_SMALL_PAPER_STATUS = STRUCTURAL_NOTE_CANDIDATE_STRENGTHENED__POWER_REMAINDER_THEOREM_REMAINS_OPEN
V59_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_JOINT_PRODUCT_WALL_REPLACED_BY_FOUR_ONE_SEQUENCE_PRIME_BDH_PACKETS_AND_ONE_COLLECTIVE_COMPILER
V59_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_POLARIZED_PRIME_BDH_CONSTRUCTION_ZONE
```

## 59. V58 后的罗盘：终点只需两个 scalar piers，transverse row 降为 railing

V58 发现 V57 的 full-shell Gate-B scalar并不是新对象。展开
`G_q(t)` 的 unit/off-diagonal centered kernel并代入 V35 proper-factor identity，逐项
得到

\[
 C_*=\sum_q qC_q=\mathfrak C_x^{\rm V35}.
\]

再令 `v=(q)_q`、`V_*=sum_q q^2` 与
`C_perp=C-(C_*/V_*)v`，exact有

\[
 \sum_q|C_q|^2=\frac{|C_*|^2}{V_*}+\|C^\perp\|_2^2.
\]

第一项是 physical endpoint真正读取的 Gate-B scalar root；第二项只在要求全部
prime-shell prefixes时才需要。V35 scalar saving `delta` 与 V57 的纵向绝对 row-loss
精确对应为 `tau_parallel=17/48-2delta`，所以
`delta>1/400` 当且仅当 `tau_parallel<419/1200`；标准
`delta=1/96` 等于 `tau_parallel=1/3`。

selected terminal route因此收窄成两个有符号标量定理：V51 full-shell Gate-A root与
V35 proper-factor Gate-B core。由
`S=(A_*-C_*+E_*)/K_*`，saving可取
`min(eta_A,delta-1/400,419/2400)` 以下任意固定值。若还要 V57 maximal prefixes，
再添加 `q`-transverse variance；它不再是 TPC endpoint 的必需桥墩。两项 scalar
theorem均仍 OPEN，算术状态不升级。

```text
V58_MAXIMUM_CLAIM = EXACT_V35_V57_CROSSWALK_IDENTIFIES_THE_GATE_B_FULL_SHELL_WITH_THE_PROPER_FACTOR_RATIO_CORE_AND_SPLITS_THE_CONSUMED_ROW_ENERGY_INTO_A_TERMINAL_SCALAR_ROOT_PLUS_OPTIONAL_Q_TRANSVERSE_VARIANCE
V58_ROUTE_ADVANCE = YES
V58_CONDITIONAL_BRIDGE_ADVANCE = YES
V58_ARITHMETIC_ADVANCE = NO
V58_FIXED_ATOM_CREDIT = 0
V58_STRICT_1_OVER_400 = UNPAID
V58_L2 = NONE
V58_TPC_207_TRIGGER = false
V58_NUMBERED_RELEASE = NO
V58_DERIVATION_STATUS = COHERENT_AFTER_LITERAL_ROW_FREEZE_EXACT_V35_V57_CROSSWALK_Q_WEIGHT_ORTHOGONAL_SPLIT_EXPONENT_TRANSLATION_TWO_SCALAR_ENDPOINT_COMPILER_AND_OPTIONAL_PREFIX_VARIANCE
V58_ASSUMPTION_POLICY = V51_GATE_A_ROOT_AND_V35_GATE_B_SCALAR_CORE_REMAIN_CONJECTURAL__TRANSVERSE_ROW_IS_OPTIONAL_FOR_MAXIMAL_PREFIXES_ONLY
V58_SELECTED_RESEARCH_ROUTE = V51_FULL_SHELL_GATE_A_ROOT_PLUS_V35_PROPER_FACTOR_GATE_B_SCALAR_CORE__ADD_Q_TRANSVERSE_VARIANCE_ONLY_FOR_MAXIMAL_GATE_A_PREFIXES
V58_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_ARCHITECTURE__CONJECTURAL__NO_GO
V58_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__T_NUM_1997_OVER_1200
V58_PAIR_ROW = RETAINED_EXACT_V54_NONSQUARE_DIAGONAL_COMPLETED_P_Q
V58_PHYSICAL_ROW = RETAINED_EXACT_V54_FULL_BETA_DIAGONAL_DELETED_C_Q
V58_PAIRED_ROW_DIFFERENCE = RETAINED_EXACT_P_Q_MINUS_C_Q_EQUALS_KAPPA_Q_S_PHYSICAL_MINUS_E_Q
V58_FULL_SHELL_SCALARS = DEFINED_A_STAR_C_STAR_E_STAR_K_STAR_WITH_COMMON_Q_WEIGHT
V58_DIRECT_PHYSICAL_READOUT = RETAINED_EXACT_S_EQUALS_A_STAR_MINUS_C_STAR_PLUS_E_STAR_OVER_K_STAR
V58_DIAGONAL_DELETED_KERNEL = PROVED_EXACT_G_Q_SUMS_UNIT_OFFDIAGONAL_W_K_H_C_PRIME_Q
V58_PROPER_FACTOR_IDENTITY = RETAINED_EXACT_BETA_EQUALS_SUM_DK_MU_D_OMEGA_DK_WITH_D_K_AT_LEAST_TWO
V58_V35_V57_SCALAR_CROSSWALK = PROVED_EXACT_C_STAR_EQUALS_MATHFRAK_C_V35_TERM_BY_TERM
V58_CROSSWALK_REMAINDER_POLICY = V35_PRINCIPAL_AND_NONUNIT_TERMS_BELONG_TO_LARGER_D_NOT_TO_ALREADY_CENTERED_C_STAR
V58_GATE_B_WEIGHT_VECTOR = DEFINED_V_Q_EQUALS_Q_AND_V_STAR_EQUALS_SUM_Q_SQUARED
V58_GATE_B_WEIGHT_NORM = PROVED_V_STAR_EQUALS_X_1_PLUS_O1
V58_Q_TRANSVERSE_ROW = DEFINED_C_PERP_EQUALS_C_MINUS_C_STAR_OVER_V_STAR_TIMES_V
V58_Q_TRANSVERSE_ORTHOGONALITY = PROVED_EXACT_INNER_C_PERP_V_EQUALS_ZERO
V58_GATE_B_PYTHAGORAS = PROVED_EXACT_SUM_ABS_C_Q_SQUARED_EQUALS_ABS_C_STAR_SQUARED_OVER_V_STAR_PLUS_NORM_C_PERP_SQUARED
V58_V53_RELATIVE_ROW_BESSEL = RETAINED_STRONGER_THAN_THE_ABSOLUTE_POWER_ENVELOPE_CONSUMED_BY_V57
V58_ABSOLUTE_ROW_DIRECT_SUM = PROVED_POWER_EQUIVALENT_TO_LONGITUDINAL_PLUS_TRANSVERSE_COMPONENT_BOUNDS_WITH_NO_EXPONENT_LOSS
V58_RELATIVE_CONVERSE = NOT_CLAIMED_WITHOUT_A_LOWER_BOUND_FOR_THE_COLLISION_DIAGONAL
V58_LONGITUDINAL_ENERGY = DEFINED_ABS_C_STAR_SQUARED_OVER_V_STAR
V58_LONGITUDINAL_DELTA_TO_TAU = PROVED_TAU_PARALLEL_EQUALS_17_OVER_48_MINUS_TWO_DELTA
V58_STRICT_THRESHOLD_EQUIVALENCE = PROVED_DELTA_GREATER_THAN_1_OVER_400_IFF_TAU_PARALLEL_LESS_THAN_419_OVER_1200
V58_BENCHMARK_TRANSLATION = PROVED_DELTA_1_OVER_96_EQUALS_TAU_PARALLEL_1_OVER_3
V58_GATE_A_ROOT_THEOREM = CONJECTURAL_V51_H_FOLD_ETA_A_ON_FULL_SHELL_NONSQUARE_ROW
V58_GATE_B_SCALAR_ROOT_THEOREM = CONJECTURAL_V35_MATHFRAK_C_X_5_OVER_3_MINUS_DELTA_WITH_DELTA_GREATER_THAN_1_OVER_400
V58_PREFIX_ERROR = RETAINED_PROVED_E_STAR_X_143_OVER_96_PLUS_O1
V58_FULL_SHELL_KAPPA_MASS = RETAINED_PROVED_K_STAR_X_2_OVER_3_PLUS_O1
V58_TWO_SCALAR_ENDPOINT_COMPILER = PROVED_CONDITIONAL_H_A_STAR_PLUS_V35_SCALAR_ROOT_IMPLIES_STRICT_PHYSICAL_ENDPOINT
V58_ENDPOINT_SAVING = ETA_LESS_THAN_MIN_ETA_A_AND_DELTA_MINUS_1_OVER_400_AND_419_OVER_2400
V58_SELECTED_GATE_B_DELTA = 1_OVER_96
V58_SELECTED_GATE_B_NUMERATOR = X_53_OVER_32_PLUS_O1
V58_SELECTED_PHYSICAL_OUTPUT = X_95_OVER_96_PLUS_O1
V58_SELECTED_PHYSICAL_MARGIN = 19_OVER_2400
V58_PREFIX_PROJECTION = PROVED_EXACT_C_Y_MINUS_S_Y_C_STAR_EQUALS_INNER_C_PERP_V_Y
V58_PREFIX_PROJECTED_NORM = PROVED_V_Y_NORM_SQUARED_EQUALS_V_OF_Y_TIMES_ONE_MINUS_V_OF_Y_OVER_V_STAR_LE_V_STAR_OVER_FOUR
V58_OPTIONAL_TRANSVERSE_MAXIMALIZATION = PROVED_TRANSVERSE_ENERGY_CONTROLS_ALL_CENTERED_GATE_B_PREFIXES
V58_ROOT_RATIO_CONVERSION = PROVED_EXACT_C_Y_MINUS_R_Y_C_STAR_EQUALS_C_Y_MINUS_S_Y_C_STAR_PLUS_S_Y_MINUS_R_Y_TIMES_C_STAR
V58_TERMINAL_GATE_B_TRANSVERSE_REQUIREMENT = NONE
V58_MAXIMAL_GATE_A_TRANSVERSE_REQUIREMENT = OPEN_OPTIONAL_Q_TRANSVERSE_VARIANCE_THEOREM
V58_V57_ROW_BESSEL = RETYPED_VALID_STRONGER_PACKAGE_BUNDLING_TERMINAL_SCALAR_AND_PREFIX_VARIANCE
V58_SCALAR_ROOT_ALONE = NO_GO_FOR_UNIFORM_MOVING_PREFIXES_WITHOUT_TRANSVERSE_CONTROL
V58_DIRECT_A_MINUS_C_THEOREM = NO_GO_AS_PRELIMINARY_BECAUSE_TERMINAL_EQUIVALENT_TO_PHYSICAL_S_UP_TO_PAID_ERROR
V58_FINITE_ORTHOGONAL_FIXTURE = PROVED_Q_5_7_11_ENERGY_77_EQUALS_867_OVER_65_PLUS_4138_OVER_65
V58_FINITE_PREFIX_FIXTURE = PROVED_CENTERED_PREFIXES_175_OVER_13_AND_MINUS_2233_OVER_65
V58_FINITE_RATIO_KERNEL_FIXTURE = PROVED_Q5_UNIT_CONGRUENT_3_OVER_4_AND_NONCONGRUENT_MINUS_1_OVER_4
V58_WRIGHT_UNBALANCED_CONVOLUTION = SOURCE_BACKED_ARCHITECTURE_TWO_Q_INDEPENDENT_ARRAYS_FIXED_RESIDUE_AND_SIEGEL_WALFISZ_WRONG_LITERAL_CORE
V58_DRAPPEAU_DISPERSION = SOURCE_BACKED_ARCHITECTURE_CONVOLUTION_KLOOSTERMAN_FRAME_WITHOUT_LITERAL_THREE_ARRAY_OCCURRENCE_CORE
V58_FOUVRY_RADZIWILL = SOURCE_BACKED_ARCHITECTURE_UNBALANCED_TWO_SEQUENCE_CONVOLUTION_WITH_TINY_SIEGEL_WALFISZ_FACTOR
V58_BLOMER_PASCADI = SOURCE_BACKED_CONDITIONAL_FIXED_MODULUS_POST_EMITTER_BILINEAR_KLOOSTERMAN_ENGINE
V58_HARPER_BDH = SOURCE_BACKED_ARCHITECTURE_ONE_FIXED_SEQUENCE_WRONG_MODULUS_AND_MOVING_RATIO
V58_DIRECT_PRIMARY_SOURCE_FOR_H_A_STAR_OR_V35_SCALAR_CORE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_13
V58_FIRST_FATAL = NO_PRIMARY_THEOREM_PROVES_EITHER_THE_LITERAL_V51_FULL_SHELL_SIGNED_FOLD_OR_THE_IDENTICAL_V35_V57_PROPER_FACTOR_CENTERED_GATE_B_SCALAR_CORE
V58_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_EXACT_SCALAR_CROSSWALK_DIRECT_SUM_AND_TWO_SCALAR_ENDPOINT_COMPILER
V58_SMALL_PAPER_STATUS = STRUCTURAL_LEMMA_PACKAGE_STRENGTHENED__TWO_SIGNED_SCALAR_ROOT_THEOREMS_REMAIN_OPEN
V58_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_TERMINAL_ROUTE_NOW_TWO_SCALAR_PIERS__Q_TRANSVERSE_ROW_MOVED_TO_OPTIONAL_MAXIMAL_RAILING
V58_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED_NO_ARCHITECTURE_TO_ATTACHMENT_PROMOTION
V58_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_TWO_SCALAR_PIERS_AND_OPTIONAL_TRANSVERSE_RAILING
```

## 58. V57 后的罗盘：root anchor 已把 endpoint motion 搬到 transverse Gate B

对 V54 exact rows逐 prefix写

\[
 A(Y)-C(Y)=K(Y)S_x-E(Y),
 \qquad r_Y=K(Y)/K_*.
\]

减去 \(r_Y\) 倍 full-shell identity后，physical mode exact取消：

\[
 A(Y)-r_YA_*=[C(Y)-r_YC_*]-[E(Y)-r_YE_*].
\]

已付款误差 uniformly为 `x^(143/96+o(1))`。Gate-B restricted row-Bessel
`sum_q|C_q|^2<<x^(95/48+tau_B+o(1))` 又自动给全部 prefixes
`sup_Y|C(Y)|<<x^(143/96+tau_B/2+o(1))`。所以 selected route只需一个 V51
full-shell `H_fold(eta_L)` 根估计和一个 `tau_B<419/1200` 的 Gate-B row theorem。
benchmark `tau_B=1/3` 给 numerator `53/32`、physical `95/96` 与 margin
`19/2400`。V56 tree保留为更强 Gate-A fallback；两项 open theorem仍无一手证明。

```text
V57_MAXIMUM_CLAIM = EXACT_LONGITUDINAL_ROOT_ANCHOR_CANCELS_THE_PHYSICAL_MODE_FROM_EVERY_GATE_A_PREFIX_AND_TRANSFERS_ALL_ENDPOINT_MOTION_TO_ONE_GATE_B_ROW_BESSEL_THEOREM_PLUS_PAID_ERROR
V57_ROUTE_ADVANCE = YES
V57_CONDITIONAL_BRIDGE_ADVANCE = YES
V57_ARITHMETIC_ADVANCE = NO
V57_FIXED_ATOM_CREDIT = 0
V57_STRICT_1_OVER_400 = UNPAID
V57_L2 = NONE
V57_TPC_207_TRIGGER = false
V57_NUMBERED_RELEASE = NO
V57_DERIVATION_STATUS = COHERENT_AFTER_PAIRED_ROW_PREFIX_SUM_LONGITUDINAL_ROOT_ANCHOR_PREFIX_ERROR_PAYMENT_GATE_B_ROW_BESSEL_MAXIMALIZATION_AND_DIRECT_PHYSICAL_READOUT
V57_ASSUMPTION_POLICY = H_FOLD_AND_H_B_RB_REMAIN_CONJECTURAL__EXACT_TRANSFER_RECEIVES_ONLY_L0_ROUTE_CREDIT
V57_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_V51_FULL_SHELL_ROOT_PLUS_V53_GATE_B_ROW_BESSEL__V56_TREE_AND_V52_PAD_PARALLEL_FALLBACKS
V57_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_ARCHITECTURE__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO
V57_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__T_NUM_1997_OVER_1200
V57_PAIR_ROW = RETAINED_EXACT_V54_NONSQUARE_DIAGONAL_COMPLETED_P_Q
V57_PHYSICAL_ROW = RETAINED_EXACT_V54_FULL_BETA_DIAGONAL_DELETED_C_Q
V57_PAIRED_ROW_DIFFERENCE = RETAINED_EXACT_P_Q_MINUS_C_Q_EQUALS_KAPPA_Q_S_PHYSICAL_MINUS_E_Q
V57_WEIGHTED_PREFIXES = DEFINED_A_Y_C_Y_E_Y_K_Y_WITH_COMMON_Q_WEIGHT
V57_PREFIX_LONGITUDINAL_IDENTITY = PROVED_EXACT_A_Y_MINUS_C_Y_EQUALS_K_Y_S_PHYSICAL_MINUS_E_Y
V57_ROOT_RATIO = DEFINED_R_Y_EQUALS_K_Y_OVER_K_STAR_IN_ZERO_ONE
V57_LONGITUDINAL_ROOT_ANCHOR = PROVED_EXACT_A_Y_MINUS_R_Y_A_STAR_EQUALS_C_Y_MINUS_R_Y_C_STAR_MINUS_E_Y_PLUS_R_Y_E_STAR
V57_PHYSICAL_PREFIX_MODE = PROVED_CANCELS_IDENTICALLY_AFTER_ROOT_ANCHOR
V57_MAXIMAL_TRANSFER_BOUND = PROVED_SUP_A_LE_ABS_A_STAR_PLUS_TWO_SUP_C_PLUS_TWO_SUP_E
V57_CONSECUTIVE_BLOCK_TRANSFER = PROVED_BY_DIFFERENCE_OF_ANCHORED_PREFIXES
V57_WRONG_COUNT_RATIO = NO_GO_DOES_NOT_CANCEL_KAPPA_LONGITUDINAL_MODE
V57_UNIT_OMISSION_PREFIX = PROVED_X_4_OVER_3_PLUS_O1
V57_SQUARE_ROW_PREFIX = PROVED_X_143_OVER_96_PLUS_O1
V57_PREFIX_ERROR_MAXIMUM = PROVED_X_143_OVER_96_PLUS_O1
V57_PREFIX_ERROR_MARGIN = 419_OVER_2400
V57_GATE_B_COLLISION_DIAGONAL = RETAINED_PROVED_X_95_OVER_48_PLUS_O1
V57_GATE_B_ROW_BESSEL = CONJECTURAL_H_B_RB_TAU_B_ON_LITERAL_FULL_BETA_DIAGONAL_DELETED_ROW
V57_GATE_B_PREFIX_CAUCHY = PROVED_UNIFORM_OVER_ALL_ENDPOINTS
V57_GATE_B_MAXIMAL_EXPONENT = 143_OVER_96_PLUS_TAU_B_OVER_2
V57_GATE_B_STRICT_ROW_LOSS = TAU_B_STRICTLY_LESS_THAN_419_OVER_1200
V57_GATE_B_SAVING = ETA_C_LT_419_OVER_2400_MINUS_TAU_B_OVER_2
V57_SELECTED_GATE_B_LOSS = TAU_B_EQUALS_1_OVER_3
V57_SELECTED_GATE_B_MAXIMUM = X_53_OVER_32_PLUS_O1
V57_SELECTED_GATE_B_MARGIN = 19_OVER_2400
V57_EQUALITY_ROW_LOSS = NO_GO_ZERO_FIXED_POWER_MARGIN
V57_GATE_A_ROOT_THEOREM = CONJECTURAL_V51_H_FOLD_ETA_L_ON_MIXED_PLUS_BALANCED_NONSQUARE_ROW
V57_ROOT_PLUS_TRANSVERSE_COMPILER = PROVED_CONDITIONAL_H_FOLD_PLUS_H_B_RB_IMPLIES_ALL_GATE_A_PREFIXES
V57_MAXIMAL_GATE_A_SAVING = ETA_M_LT_MIN_ETA_L_AND_419_OVER_2400_MINUS_TAU_B_OVER_2
V57_FULL_SHELL_KAPPA_MASS = PROVED_X_2_OVER_3_PLUS_O1
V57_DIRECT_PHYSICAL_READOUT = PROVED_EXACT_S_EQUALS_A_STAR_MINUS_C_STAR_PLUS_E_STAR_OVER_K_STAR
V57_GENERAL_PHYSICAL_SAVING = ETA_LT_MIN_ETA_L_AND_419_OVER_2400_MINUS_TAU_B_OVER_2
V57_SELECTED_PHYSICAL_OUTPUT = X_95_OVER_96_PLUS_O1
V57_SELECTED_PHYSICAL_MARGIN = 19_OVER_2400
V57_GATE_B_USAGE = PROVED_EXACTLY_ONCE_ROW_ENERGY_PAYS_BOTH_FULL_SHELL_AND_PREFIX_C
V57_V43_BOUNDARY = BYPASSED_IN_THIS_COMPILER_BY_EXACT_V54_PAIRED_ROW_IDENTITY
V57_V56_TREE = RETAINED_VALID_STRONGER_GATE_A_FALLBACK_NOT_REQUIRED_ON_SELECTED_ROOT_PLUS_ROW_ROUTE
V57_V53_SYMMETRIC_TWO_ROW_BESSEL = RETYPED_STRONGER_THAN_NEEDED_ON_GATE_A_AXIS
V57_V52_PAD = RETAINED_PARALLEL_CONJECTURAL_GATE_A_FALLBACK_NO_CREDIT_SPLICING
V57_PACKAGE_COMPARISON = NONCOMPARABLE_GLOBALLY__WEAKER_GATE_A_ROOT_BUT_STRONGER_GATE_B_ROW_THAN_SCALAR_ONLY
V57_FULL_SHELL_A_ALONE = NO_GO_PREFIXES_AND_PHYSICAL_ENDPOINT_REQUIRE_INDEPENDENT_GATE_B_CONTROL
V57_TRANSVERSE_PROJECTION_ALONE = NO_GO_ANNIHILATES_ARBITRARILY_LARGE_KAPPA_PHYSICAL_MODE
V57_PREFIX_FIXTURE = PROVED_Q_5_7_11_EXACT_TWO_NONTRIVIAL_ENDPOINTS_AND_S_RECOVERY_13
V57_HARPER_BDH = SOURCE_BACKED_ARCHITECTURE_FIXED_SEQUENCE_WRONG_Q_RANGE_AND_Q_DEPENDENT_ROW
V57_LEWKO_LEWKO_VARIATIONAL_BDH = SOURCE_BACKED_ARCHITECTURE_WRONG_INNER_VARIATION_AXIS_AND_LITERAL_ROW
V57_RAMARE_SPECTRAL_LARGE_SIEVE = SOURCE_BACKED_ARCHITECTURE_NONNEGATIVE_QUADRATIC_FORM_WRONG_SIGNED_PACKET
V57_PASCADI_TRIPLY_FACTORABLE_AP = NO_GO_DIRECT_FIXED_PROGRESSION_ARRAYS_NOT_LITERAL_ROW
V57_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_POST_EMITTER_KLOOSTERMAN_CELL_ONLY
V57_DIRECT_PRIMARY_SOURCE_FOR_H_FOLD_OR_H_B_RB = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_12
V57_FIRST_FATAL = NO_PRIMARY_THEOREM_PROVES_EITHER_THE_LITERAL_V51_FULL_SHELL_MIXED_PLUS_BALANCED_FOLD_OR_THE_V53_GATE_B_RESTRICTED_ROW_BESSEL_ENERGY__THE_EXACT_LONGITUDINAL_ANCHOR_DOES_NOT_ESTIMATE_EITHER_PREMISE
V57_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_LONGITUDINAL_ANCHOR_MAXIMAL_TRANSFER_AND_ROOT_PLUS_TRANSVERSE_TWO_PIER_COMPILER
V57_SMALL_PAPER_STATUS = STRUCTURAL_LEMMA_PACKAGE_MATERIALLY_STRENGTHENED__MAIN_SIGNED_ROOT_AND_TRANSVERSE_ROW_THEOREMS_OPEN
V57_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_ROOT_ANCHOR_INSTALLED__FULL_SHELL_FOLD_AND_TRANSVERSE_GATE_B_ROW_BESSEL_ARE_THE_TWO_OPEN_PIERS
V57_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED_NO_ARCHITECTURE_TO_ATTACHMENT_PROMOTION
V57_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_LONGITUDINAL_ROOT_ANCHOR_AND_TRANSVERSE_ROW
```

## 57. V56 后的罗盘：maximal endpoint 已压成 pruned dyadic large blocks

V56 继承 V51/V54 的完整 folded compensated row，先逐模数证明
`q|P_q|<<x^(53/32+o(1))`。Gate-A numerator target 与该 exponent 的精确差为
`19/2400`。固定 `0<lambda<19/2400`，把按大小排序的 prime shell预先分成
至多 `x^lambda` 个模数的连续 leaves；所有短 leaves可绝对支付。

完整 leaves组成 aligned power-of-two dyadic nodes。每个 prefix精确分解为
`O(log Q)` 个 nodes、至多一个 full leaf和一个 partial leaf。故若每个至少含两个
leaves的 node `B` 都统一满足

\[
 \left|\sum_{q\in B}qP_q\right|
 \ll x^{1997/1200-\eta_D+o(1)},
\]

则 maximal saving可取
`eta_M<min(eta_D,19/2400-lambda)`；反向 node是两个 prefixes之差。标准 cut
`lambda=19/4800` 留同样的 `19/4800` leaf margin。这个 exact compiler没有证明
large-node cancellation；V42 common transverse Gate B也仍独立 OPEN。现有
Lewko--Lewko/Ramaré只支持 dyadic/maximal architecture，fixed-modulus
Kloosterman sources也没有 literal outer-`q` block reassembly。

```text
V56_MAXIMUM_CLAIM = EXACT_PRUNED_DYADIC_TREE_COMPILER_REDUCES_THE_V51_MAXIMAL_FOLD_FIRST_PARTIAL_PRIME_SHELL_TO_ONE_UNIFORM_CANONICAL_BLOCK_THEOREM_WITH_TRIVIAL_LEAF_MARGIN_AND_NO_POWER_LOSS
V56_ROUTE_ADVANCE = YES
V56_CONDITIONAL_BRIDGE_ADVANCE = YES
V56_ARITHMETIC_ADVANCE = NO
V56_FIXED_ATOM_CREDIT = 0
V56_STRICT_1_OVER_400 = UNPAID
V56_L2 = NONE
V56_TPC_207_TRIGGER = false
V56_NUMBERED_RELEASE = NO
V56_DERIVATION_STATUS = COHERENT_AFTER_LITERAL_ROW_FREEZE_SINGLE_Q_PAYMENT_PRUNED_DYADIC_TREE_MAXIMALIZATION_REVERSE_INTERVAL_BOUND_TWO_WORLD_COMPILER_AND_SOURCE_FIREWALL
V56_ASSUMPTION_POLICY = CANONICAL_BLOCK_THEOREM_AND_COMMON_TRANSVERSE_GATE_REMAIN_CONJECTURAL__MAXIMALIZATION_AND_LEAF_PAYMENT_RECEIVE_ONLY_L0_ROUTE_CREDIT
V56_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_SOURCE_BACKED_CONDITIONAL_EXIT__OTHERWISE_PRUNED_DYADIC_FOLD_FIRST_GATE_A_PLUS_V42_COMMON_TRANSVERSE_GATE_B__V52_PAD_PARALLEL_FALLBACK
V56_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_ARCHITECTURE__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO
V56_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__T_NUM_1997_OVER_1200
V56_INHERITED_FOLD_FIRST_ROW = RETAINED_EXACT_P_Q_EQUALS_SUM_BETA_CIRCLE_TIMES_COMPENSATED_R_Q
V56_LITERAL_DATA_RETENTION = PROVED_SAME_PAIR_FOLD_PHYSICAL_W_DIAGONAL_COMPENSATION_UNIT_MASK_HARD_SHELL_AND_ONE_BLOCK_SIGN
V56_SINGLE_MODULUS_ABSOLUTE_ROW = PROVED_Q_ABS_P_Q_LE_X_H_X_O1
V56_SINGLE_MODULUS_EXPONENT = 53_OVER_32
V56_SINGLE_MODULUS_MARGIN_TO_GATE_A = 19_OVER_2400
V56_PRUNE_EXPONENT_RANGE = ZERO_LT_LAMBDA_LT_19_OVER_2400
V56_CANONICAL_PRUNE_BENCHMARK = LAMBDA_19_OVER_4800
V56_ORDERED_PRIME_SHELL = PREDECLARED_BEFORE_ROW_VALUES
V56_LEAF_PARTITION = PROVED_CONSECUTIVE_AT_MOST_X_LAMBDA_PRIMES
V56_DYADIC_NODE_FAMILY = DEFINED_ALIGNED_UNIONS_OF_POWER_OF_TWO_LEAVES
V56_BLOCK_FUNCTIONAL = DEFINED_T_X_B_EQUALS_SUM_Q_IN_B_Q_P_Q
V56_PREFIX_BINARY_DECOMPOSITION = PROVED_EXACT_DISJOINT_CANONICAL_NODES_PLUS_ONE_PARTIAL_LEAF
V56_PREFIX_NODE_COUNT = PROVED_O_LOG_Q
V56_PREFIX_SINGLETON_COUNT = PROVED_AT_MOST_ONE_FULL_LEAF_PLUS_ONE_PARTIAL_LEAF
V56_TRIVIAL_LEAF_BOUND = PROVED_X_T_NUM_MINUS_19_OVER_2400_PLUS_LAMBDA_PLUS_O1
V56_TRIVIAL_LEAF_MARGIN = PROVED_19_OVER_2400_MINUS_LAMBDA
V56_CANONICAL_BLOCK_THEOREM = CONJECTURAL_H_TREE_LAMBDA_ETA_D
V56_CANONICAL_BLOCK_UNIFORMITY = REQUIRED_ONE_CONSTANT_THRESHOLD_AND_O1_OVER_ALL_PREDECLARED_NODES
V56_TREE_TO_MAXIMAL = PROVED_CONDITIONAL_WITH_ONLY_LOG_Q_LOSS
V56_MAXIMAL_SAVING_LAW = ETA_M_LT_MIN_ETA_D_AND_19_OVER_2400_MINUS_LAMBDA
V56_MAXIMAL_TO_INTERVAL = PROVED_FACTOR_TWO_DIFFERENCE_OF_PREFIXES
V56_TREE_MAXIMAL_POWER_EQUIVALENCE = PROVED_AFTER_SHORT_LEAF_PAYMENT
V56_FULL_SHELL_ONLY = NO_GO_DOES_NOT_CONTROL_MAXIMAL_PREFIX_OR_LONGITUDINAL_ABEL_WEIGHT
V56_FULL_SHELL_COUNTEREXAMPLE = PROVED_Q5_Q7_ZERO_FINAL_WITH_PREFIX_35_AND_NONZERO_KAPPA_SUM
V56_INTERVAL_FACTOR_TWO_FIXTURE = PROVED_SEQUENCE_1_MINUS2_1_SHARP
V56_DYADIC_PREFIX_FIXTURE = PROVED_13_TERM_LEAF3_PREFIX11_EXACT
V56_COEFFICIENT_UNIFORM_SHORTCUT = NO_GO_COMMON_SIGN_REACHES_X_191_OVER_96_PLUS_O1
V56_FOLD_BEFORE_TREE_TRIANGLE = PROVED_REQUIRED_EACH_NODE_RETAINS_COMPLETE_FOLDED_COMPENSATED_ROW
V56_BLOCK_LEVEL_TRIANGLE = PROVED_LEGAL_O_LOG_Q_AFTER_WHOLE_NODE_ESTIMATES
V56_SMOOTH_MODULUS_WEIGHT_TRANSFER = OPEN_REQUIRES_BOUNDARY_STRIP_AND_DERIVATIVE_NORM_PAYMENT
V56_TREE_IMPLIES_V51_GATE_A = PROVED_CONDITIONAL_FULL_SHELL_SPECIALIZATION
V56_SQUARE_ROW_PAYMENT = RETAINED_X_143_OVER_96_PLUS_O1
V56_GATE_A_SAVING_LAW = ETA_A_LT_MIN_ETA_D_19_OVER_2400_MINUS_LAMBDA_419_OVER_2400_11_OVER_600_MINUS_EPSILON
V56_V42_COMMON_TRANSVERSE_GATE_B = RETAINED_INDEPENDENT_OPEN_THEOREM
V56_TWO_GATE_ENDPOINT_LAW = PROVED_CONDITIONAL_MIN_INCLUDES_ETA_B_AND_19_OVER_2400
V56_MAXIMAL_ABEL_TRANSFER = RETAINED_PROVED_TO_LONGITUDINAL_X_1597_OVER_1200_MINUS_ETA_M
V56_LONGITUDINAL_READOUT = RETYPED_TERMINAL_INTERFACE_NOT_GATE_B
V56_UNBOUNDED_SIEGEL_QUALITY_WORLD = RETAINED_SOURCE_BACKED_CONDITIONAL_DIRECT_TPC_EXIT
V56_BOUNDED_SIEGEL_QUALITY_TREE_FAMILY = CONJECTURAL_FORALL_B_EXISTS_ETA_D_B_UNIFORM_ALL_NODES_ALL_LARGE_X
V56_TWO_WORLD_COMPILER = PROVED_CONDITIONAL_UNBOUNDED_EXIT_OR_BOUNDED_TREE_PLUS_GATE_B
V56_V52_PAD_GATE_A = RETAINED_PARALLEL_CONJECTURAL_FALLBACK_NO_CREDIT_SPLICING
V56_LEWKO_LEWKO_VARIATIONAL_LARGE_SIEVE = SOURCE_BACKED_ARCHITECTURE_DYADIC_ENDPOINT_COMPILER_ON_INNER_INDEX
V56_LEWKO_LEWKO_DIRECT_ATTACHMENT = NO_GO_WRONG_MAXIMAL_AXIS_AND_WRONG_LITERAL_COEFFICIENT
V56_RAMARE_SPECTRAL_LARGE_SIEVE = SOURCE_BACKED_ARCHITECTURE_SMOOTH_NONNEGATIVE_Q_AVERAGE_AND_INNER_MAXIMALITY
V56_RAMARE_DIRECT_ATTACHMENT = NO_GO_SIGNED_OUTER_Q_FOLD_FIRST_PACKET_MISSING
V56_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_POST_EMITTER_KLOOSTERMAN_CELL_ONLY
V56_MQW_KSWX_FIXED_MODULUS = NO_GO_DIRECT_NO_CANONICAL_Q_BLOCK_REASSEMBLY
V56_RUNBO_LI_LARGE_MODULI = NO_GO_DIRECT_HARMAN_PRIME_ARRAY_AND_FOLDED_PAIR_PACKET_MISMATCH
V56_BAZIN_PRODUCT_OF_K_PRIMES = NO_GO_DIRECT_WRONG_ENDPOINT_COEFFICIENT_AND_DIRECTION
V56_DIRECT_PRIMARY_SOURCE_FOR_H_TREE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_12
V56_FIRST_FATAL = NO_PRIMARY_THEOREM_PROVES_THE_UNIFORM_CANONICAL_DYADIC_BLOCK_BOUND_FOR_THE_LITERAL_V51_FOLD_FIRST_DIAGONAL_COMPLETED_COMPENSATED_PAIR_PRIME_HYBRID_ROW__AND_V42_COMMON_TRANSVERSE_GATE_B_REMAINS_OPEN
V56_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_PRUNED_DYADIC_MAXIMALIZATION_LEAF_MARGIN_AND_POWER_EQUIVALENCE
V56_SMALL_PAPER_STATUS = STRUCTURAL_LEMMA_PACKAGE_READY_BUT_ELEMENTARY_MAXIMALIZATION_IS_NOT_A_STANDALONE_ASYMPTOTIC_MAIN_THEOREM
V56_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_MAXIMAL_GATE_A_ENDPOINT_MOTION_COMPILED__CANONICAL_LARGE_BLOCK_CANCELLATION_AND_COMMON_TRANSVERSE_PIER_OPEN
V56_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED_NO_ARCHITECTURE_TO_ATTACHMENT_PROMOTION
V56_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_PRUNED_DYADIC_GATE_A_AND_COMMON_TRANSVERSE_GATE_B
```

## 56. V55 后的罗盘：terminal readout classified，pre-q piers open

V55 把 V54 的 \(\kappa\)-longitudinal cable彻底分类。逐模数 exact有
\[
 \frac{P_q-C_q}{\kappa_q}
 =S_x+O(x^{79/96+o(1)}),
\]
所以 physical scalar在每个预声明 prime modulus上复制。对任意 q-space线性算子
\(T\)，\(T(P-C)=S_xT\kappa-TE\)：若 \(T\kappa=0\)，只剩已付款 transverse
error；若 \(T\kappa\ne0\)，该坐标就是 terminal physical estimator。V54
\(\kappa/N_\kappa\) extractor在仅知 L2 error ball时唯一 minimax；PSD/TT-star也
没有第三种 case。

因此地图上的 longitudinal cable不再作为待造桥墩，而是已经识别的终点读出器。
下一大路前移到 q-compression之前：

1. V51 maximal partial-shell fold-first theorem；
2. V52 signed diagonal+off-diagonal PAD theorem；
3. V42/common transverse Gate-B theorem；
4. unbounded Siegel-quality conditional exit；
5. dynamics只作独立 reserve。

V51 full-shell scalar不能代替 maximal theorem；有限 Abel fixture给
\(\sum qP_q=0\) 而 \(\sum\kappa_qP_q=13/12\)。若
\[
 \sup_{Q<Y\le2Q}\left|\sum_{Q<q\le Y}qP_q\right|
 \ll x^{1997/1200-\eta+o(1)},
\]
则 Abel summation把它传到 longitudinal scale
\(x^{1597/1200-\eta+o(1)}\)。character packet自然尺度 \(x^{4/3}\) 到该目标恰缺
\(1/400\)。

`PROVED`、`SOURCE_BACKED_CONDITIONAL`、`CONJECTURAL` 与
`NO_GO` 仍严格分开；算术状态仍为 NO。

```text
V55_MAXIMUM_CLAIM = EXACT_POINTWISE_REPLICATION_OF_THE_PHYSICAL_SCALAR_ACROSS_EVERY_PRIME_MODULUS_PLUS_MINIMAX_LINEAR_EXTRACTOR_AND_MODULUS_OPERATOR_TTSTAR_DICHOTOMY_WITH_MAXIMAL_GATE_A_TRANSFER_INTERFACE
V55_ROUTE_ADVANCE = YES
V55_CONDITIONAL_BRIDGE_ADVANCE = YES
V55_ARITHMETIC_ADVANCE = NO
V55_FIXED_ATOM_CREDIT = 0
V55_STRICT_1_OVER_400 = UNPAID
V55_L2 = NONE
V55_TPC_207_TRIGGER = false
V55_NUMBERED_RELEASE = NO
V55_DERIVATION_STATUS = COHERENT_AFTER_POINTWISE_ERROR_PAYMENT_OPERATOR_DICHOTOMY_MINIMAX_EXTRACTION_TTSTAR_FIREWALL_AND_MAXIMAL_ABEL_TRANSFER
V55_ASSUMPTION_POLICY = MAXIMAL_PARTIAL_SHELL_AND_PRE_Q_PACKET_SAVINGS_REMAIN_CONJECTURAL__EXACT_OPERATOR_RESULTS_RECEIVE_NO_ARITHMETIC_CREDIT
V55_SELECTED_RESEARCH_ROUTE = STOP_LONGITUDINAL_QSPACE_PRELIMINARY_ENGINEERING__PIVOT_TO_V51_MAXIMAL_FOLD_FIRST_OR_V52_PAD_FOR_GATE_A_AND_V42_COMMON_TRANSVERSE_FOR_GATE_B__RETAIN_V55_LONGITUDINAL_READOUT_AS_TERMINAL_ONLY
V55_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO
V55_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400
V55_INHERITED_PAIRED_DIFFERENCE = RETAINED_EXACT_D_Q_EQUALS_KAPPA_Q_S_PHYSICAL_MINUS_E_Q
V55_INHERITED_DIFFERENCE_ERROR_ENERGY = RETAINED_PROVED_X_95_OVER_48_PLUS_O1
V55_POINTWISE_UNIT_OMISSION = PROVED_X_2_OVER_3_PLUS_O1_EACH_Q
V55_POINTWISE_SQUARE_COMPLETION = PROVED_X_79_OVER_96_PLUS_O1_EACH_Q
V55_POINTWISE_DIFFERENCE_ERROR = PROVED_X_79_OVER_96_PLUS_O1_EACH_Q
V55_SINGLE_MODULUS_REPLICA = PROVED_EXACT_S_Q_REP_EQUALS_D_Q_OVER_KAPPA_Q_EQUALS_S_PHYSICAL_MINUS_E_Q_OVER_KAPPA_Q
V55_SINGLE_MODULUS_REPLICA_ERROR = PROVED_X_79_OVER_96_PLUS_O1
V55_PAIRWISE_REPLICA_CONSISTENCY = PROVED_X_79_OVER_96_PLUS_O1
V55_SINGLE_Q_DIFFERENCE_THEOREM = RETYPED_TERMINAL_EQUIVALENT_TO_PHYSICAL_ENDPOINT_UP_TO_PAID_ERROR
V55_GENERAL_MODULUS_OPERATOR_IDENTITY = PROVED_EXACT_TD_EQUALS_S_TKAPPA_MINUS_TE
V55_TRANSVERSE_OPERATOR_CASE = PROVED_TKAPPA_ZERO_IMPLIES_TD_EQUALS_MINUS_TE
V55_LONGITUDINAL_OPERATOR_CASE = PROVED_NONZERO_TKAPPA_GIVES_EXACT_PHYSICAL_ESTIMATOR
V55_OPERATOR_ESTIMATOR_ERROR = PROVED_NORM_T_OVER_NORM_TKAPPA_TIMES_NORM_E
V55_OPERATOR_CONDITION_LOWER_BOUND = PROVED_NORM_T_OVER_NORM_TKAPPA_AT_LEAST_ONE_OVER_NORM_KAPPA
V55_LINEAR_UNBIASED_CLASS = DEFINED_INNER_A_KAPPA_EQUALS_ONE
V55_MINIMAX_LINEAR_EXTRACTOR = PROVED_UNIQUE_A_STAR_EQUALS_KAPPA_OVER_N_KAPPA
V55_MINIMAX_WORST_CASE_ERROR = PROVED_NORM_E_OVER_SQRT_N_KAPPA
V55_MINIMAX_EXTRACTION_EXPONENT = PROVED_X_79_OVER_96_PLUS_O1
V55_PSD_TTSTAR_IDENTITY = PROVED_EXACT_QUADRATIC_EXPANSION
V55_PSD_TRANSVERSE_CASE = PROVED_AKAPPA_ZERO_DELETES_PHYSICAL_MODE
V55_PSD_LONGITUDINAL_CASE = PROVED_POSITIVE_KAPPA_ENERGY_IS_TERMINAL_EQUIVALENT
V55_CENTERED_MODULUS_BDH = NO_GO_POST_Q_PRELIMINARY_DELETES_KAPPA_MODE
V55_POST_Q_TTSTAR_SHORTCUT = NO_GO_EITHER_TRANSVERSE_OR_TERMINAL_NO_THIRD_CASE
V55_CHARACTER_FIXED_Q_PACKET = RETAINED_EXACT_NONPRINCIPAL_PRODUCT_PACKET
V55_TTSTAR_EXACT_RATIO_RAY = RETAINED_EXACT_PHYSICAL_U_EQUALS_T_MODE
V55_PRE_Q_COMPRESSION_REQUIREMENT = OPEN_SIGNED_DIAGONAL_PLUS_OFFDIAGONAL_LITERAL_PACKET_THEOREM
V55_MAXIMAL_GATE_A_PARTIAL_SUM = DEFINED_F_OF_Y_EQUALS_SUM_Q_LE_Y_Q_P_Q
V55_MAXIMAL_GATE_A_ABEL_IDENTITY = PROVED_EXACT_LONGITUDINAL_WEIGHT_TRANSFER
V55_MAXIMAL_GATE_A_TRANSFER = PROVED_CONDITIONAL_SUP_F_X_1997_OVER_1200_IMPLIES_L_A_X_1597_OVER_1200
V55_FULL_SHELL_GATE_A_SCALAR = NO_GO_DOES_NOT_CONTROL_LONGITUDINAL_WEIGHTED_SUM
V55_FULL_SHELL_COUNTEREXAMPLE = PROVED_EXACT_ZERO_Q_WEIGHTED_SUM_WITH_NONZERO_KAPPA_WEIGHTED_SUM
V55_MAXIMAL_GATE_A_THEOREM = OPEN_NEW_WHOLE_OBJECT_THEOREM
V55_LONGITUDINAL_PACKET_NATURAL_SCALE = X_4_OVER_3_PLUS_O1
V55_LONGITUDINAL_PACKET_TARGET_SCALE = X_1597_OVER_1200_MINUS_ETA_PLUS_O1
V55_LONGITUDINAL_PACKET_GAP = 1_OVER_400
V55_LONGITUDINAL_ANGULAR_SAVING_LAW = DELTA_B_PLUS_DELTA_W_OVER_2_PLUS_RHO_STRICTLY_GREATER_THAN_1_OVER_400
V55_NARROW_PRIME_SHELL = NO_FREE_EXPONENT_CREDIT_SIGNAL_PACKET_AND_TARGET_SCALE_TOGETHER
V55_MILICEVIC_QIN_WU_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_POST_EMITTER_KLOOSTERMAN_CELL_ONLY
V55_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_POST_EMITTER_KLOOSTERMAN_CELL_ONLY
V55_KERR_SHPARLINSKI_WU_XI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_POST_EMITTER_KLOOSTERMAN_CELL_ONLY
V55_HARPER_GENERAL_BDH = NO_GO_DIRECT_CENTERED_VARIANCE_AND_LONGITUDINAL_MODE_MISMATCH
V55_RUNBO_LI_LARGE_MODULI = NO_GO_DIRECT_PRIME_AP_FIRST_MOMENT_AND_PAIRED_PACKET_MISMATCH
V55_ZHENG_SIMULTANEOUS_AP = NO_GO_DIRECT_SOURCE_SPECIFIC_PROGRESSIONS_AND_COMPENSATED_PACKET_MISMATCH
V55_DONG_ROBLES_ZEINDLER = EXCLUDED_WITHDRAWN_MISSING_L2_FACTOR_NO_THEOREM_CREDIT
V55_DIRECT_PRIMARY_SOURCE_FOR_LONGITUDINAL_PACKET = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_12
V55_Q5_Q7_REPLICA_FIXTURE = PROVED_EXACT_POINTWISE_REPLICATION_AND_PAIRWISE_DIFFERENCE
V55_OPERATOR_DICHOTOMY_FIXTURE = PROVED_EXACT_TRANSVERSE_AND_DIAGONAL_KEEP_CASES
V55_MINIMAX_FIXTURE = PROVED_EXACT_A_STAR_NORM_BEATS_COORDINATE_ESTIMATOR
V55_PSD_TERMINAL_DELETION_FIXTURE = PROVED_EXACT_ARBITRARY_LONGITUDINAL_ZERO_ENERGY
V55_MAXIMAL_ABEL_FIXTURE = PROVED_EXACT_PARTIAL_SUM_IDENTITY_AND_FULL_SHELL_NO_GO
V55_FIRST_FATAL = NO_PRIMARY_THEOREM_CONTROLS_THE_LITERAL_PRE_Q_PROJECTION_SIGNED_DIAGONAL_OFFDIAGONAL_PACKET_OR_THE_V51_MAXIMAL_PARTIAL_PRIME_SHELL__ANY_POST_Q_OPERATOR_RETAINING_KAPPA_IS_TERMINAL_EQUIVALENT_AND_THE_COMMON_TRANSVERSE_THEOREM_REMAINS_OPEN
V55_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_REPLICATION_MINIMAX_OPERATOR_DICHOTOMY_AND_MAXIMAL_SHELL_INTERFACE
V55_SMALL_PAPER_STATUS = STRUCTURAL_LEMMA_PACKAGE_READY_NO_STANDALONE_ASYMPTOTIC_THEOREM
V55_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_LONGITUDINAL_CABLE_RECLASSIFIED_AS_TERMINAL_READOUT__PRE_Q_GATE_A_AND_COMMON_TRANSVERSE_PIERS_OPEN
V55_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED_WITH_WITHDRAWN_SOURCES_EXCLUDED
V55_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_PRE_Q_PIERS_AND_TERMINAL_READOUT
```


## 55. V54 后的罗盘：paired-row transverse deck 与 terminal longitudinal cable

V54 仍在解析消去岛 / Bridge A，但把 V53 的 symmetric two-row theorem重新
对角化。若 `P_q` 是 diagonal-completed pair row，`C_q` 是 diagonal-deleted
physical row，`kappa_q=(q-2)/(q-1)`，则 exact有

\[
 P_q-C_q=\kappa_qS_x-E_q,
 \qquad \sum_q|E_q|^2\ll x^{95/48+o(1)}.
\]

因此 transverse projections只差已付款误差，而 `kappa` longitudinal coordinate以
`O(x^(79/96+o(1)))` 误差直接抽取 physical residual。V53 的双 row-Bessel package
是有效 terminal package，不再被视为两个独立 preliminary gates。当前优先级为：
direct signed longitudinal scalar、一个 common transverse theorem、再保留 V51/V52/V42
与 dynamics reserves。算术状态仍为 NO。

```text
V54_MAXIMUM_CLAIM = EXACT_PAIRED_ROW_DIAGONALIZATION_PAID_TRANSVERSE_DIFFERENCE_AND_TERMINAL_LONGITUDINAL_EXTRACTION_RETYPE_SYMMETRIC_TWO_ROW_BESSEL_AS_ONE_ROW_PLUS_PHYSICAL_ENDPOINT
V54_ROUTE_ADVANCE = YES
V54_CONDITIONAL_BRIDGE_ADVANCE = YES
V54_ARITHMETIC_ADVANCE = NO
V54_FIXED_ATOM_CREDIT = 0
V54_STRICT_1_OVER_400 = UNPAID
V54_L2 = NONE
V54_TPC_207_TRIGGER = false
V54_NUMBERED_RELEASE = NO
V54_DERIVATION_STATUS = COHERENT_AFTER_FULL_BETA_SPLIT_ROW_DIFFERENCE_ERROR_PAYMENT_KAPPA_PROJECTION_AND_TWO_OUT_OF_THREE_COMPILER
V54_ASSUMPTION_POLICY = TRANSVERSE_ROW_AND_LONGITUDINAL_SCALAR_ESTIMATES_REMAIN_CONJECTURAL__EXACT_DIAGONALIZATION_RECEIVES_NO_ARITHMETIC_CREDIT
V54_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_DIRECT_SIGNED_LONGITUDINAL_SCALAR_AND_ONE_COMMON_TRANSVERSE_ROW__V51_V52_V42_FALLBACKS__DYNAMICS_RESERVE
V54_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO
V54_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400
V54_FULL_BETA_SPLIT = RETAINED_EXACT_BETA_EQUALS_BETA_CIRCLE_PLUS_BETA_SQUARE
V54_PAIR_ROW = RETAINED_EXACT_V53_DIAGONAL_COMPLETED_P_Q
V54_PHYSICAL_ROW = RETAINED_EXACT_V40_DIAGONAL_DELETED_C_Q
V54_KERNEL_TOGGLE = RETAINED_EXACT_R_Q_EQUALS_G_Q_PLUS_KAPPA_Q_W
V54_SQUARE_COMPLETED_ROW = DEFINED_EXACT_Y_Q_SQUARE
V54_UNIT_OMISSION_ROW = DEFINED_EXACT_U_Q
V54_UNIT_PHYSICAL_DIAGONAL = PROVED_EXACT_Z_Q_EQUALS_S_PHYSICAL_MINUS_U_Q
V54_PAIRED_ROW_DIFFERENCE = PROVED_EXACT_P_Q_MINUS_C_Q_EQUALS_KAPPA_Q_S_PHYSICAL_MINUS_E_Q
V54_DIFFERENCE_ERROR = PROVED_EXACT_E_Q_EQUALS_KAPPA_Q_U_Q_PLUS_Y_Q_SQUARE
V54_UNIT_OMISSION_ENERGY = PROVED_X_5_OVER_3_PLUS_O1
V54_SQUARE_COMPLETED_ROW_ENERGY = PROVED_X_95_OVER_48_PLUS_O1
V54_DIFFERENCE_ERROR_ENERGY = PROVED_X_95_OVER_48_PLUS_O1
V54_KAPPA_VECTOR_NORM = PROVED_X_1_OVER_3_PLUS_O1
V54_LONGITUDINAL_EXTRACTOR = PROVED_EXACT_S_HAT_EQUALS_INNER_P_MINUS_C_KAPPA_OVER_N_KAPPA
V54_LONGITUDINAL_EXTRACTION_ERROR = PROVED_X_79_OVER_96_PLUS_O1
V54_EXTRACTION_ERROR_MARGIN = 419_OVER_2400
V54_TRANSVERSE_ROW_DIFFERENCE = PROVED_EXACT_PI_PERP_P_MINUS_PI_PERP_C_EQUALS_MINUS_PI_PERP_E
V54_TRANSVERSE_DIFFERENCE_ENERGY = PROVED_X_95_OVER_48_PLUS_O1
V54_TWO_OUT_OF_THREE_COMPILER = PROVED_H_A_PLUS_H_B_IMPLIES_H_S__H_S_PLUS_EITHER_ROW_IMPLIES_THE_OTHER
V54_GENERAL_PHYSICAL_OUTPUT = X_79_OVER_96_PLUS_TAU_OVER_2_PLUS_O1
V54_ROW_LOSS_ENDPOINT = TAU_STRICTLY_LESS_THAN_419_OVER_1200
V54_SELECTED_ONE_Q_LOSS = TAU_EQUALS_1_OVER_3
V54_SELECTED_PHYSICAL_OUTPUT = X_95_OVER_96_PLUS_O1
V54_SELECTED_PHYSICAL_MARGIN = 19_OVER_2400
V54_V43_JOIN = BYPASSED_BY_DIRECT_UNWEIGHTED_KAPPA_PROJECTION_FOR_THIS_CONDITIONAL_COMPILER
V54_LONGITUDINAL_SCALARS = DEFINED_L_A_AND_L_B_AS_KAPPA_PROJECTIONS
V54_LONGITUDINAL_DIFFERENCE = PROVED_EXACT_L_A_MINUS_L_B_EQUALS_N_KAPPA_S_PHYSICAL_MINUS_INNER_E_KAPPA
V54_SELECTED_LONGITUDINAL_SCALE = X_127_OVER_96_PLUS_O1
V54_COMMON_TRANSVERSE_THEOREM = OPEN_ONE_LITERAL_Q_ROW_VARIANCE_SPECIES_SUFFICES_FOR_BOTH_ROWS_UP_TO_PAID_ERROR
V54_LONGITUDINAL_THEOREM = OPEN_TERMINAL_SIGNED_SCALAR_EQUIVALENT_TO_PHYSICAL_ENDPOINT_UP_TO_PAID_ERROR
V54_SYMMETRIC_TWO_ROW_BESSEL = RETYPED_VALID_TERMINAL_PACKAGE_NOT_PREFERRED_PRELIMINARY
V54_CENTERED_MODULUS_BDH_ONLY = NO_GO_CONTROLS_TRANSVERSE_VARIANCE_BUT_DELETES_TERMINAL_LONGITUDINAL_MODE
V54_CHARACTER_DIAGONAL_PACKET = PROVED_EXACT_Z_Q_CIRCLE_INDEPENDENT_OF_CHI_AND_V
V54_TTSTAR_DETERMINANT_CONGRUENCE = PROVED_EXACT_U1_T2_CONGRUENT_U2_T1_MOD_Q
V54_TTSTAR_EXACT_RATIO_RAY = RETAINS_PHYSICAL_U_EQUALS_T_MODE
V54_SPECIAL_L_FUNCTION_FOURTH_MOMENTS = NO_GO_DIRECT_COEFFICIENT_AND_DIAGONAL_CANCELLATION_MISMATCH
V54_HARPER_GENERAL_BDH = NO_GO_DIRECT_FIXED_SEQUENCE_AND_LONGITUDINAL_MODE_MISMATCH
V54_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_TRANSVERSE_CELL_ONLY
V54_RUNBO_LI_LARGE_MODULI = NO_GO_DIRECT_FIXED_RESIDUE_FIRST_MOMENT_AND_PAIRED_ROW_MISMATCH
V54_Q5_Q7_ROW_FIXTURE = PROVED_EXACT_PAIRED_DIFFERENCE_PROJECTION_AND_TRANSVERSE_IDENTITY
V54_TERMINAL_MODE_FIXTURE = PROVED_TRANSVERSE_ZERO_WITH_ARBITRARY_LONGITUDINAL_COORDINATE
V54_V51_DIRECT_SCALAR = RETAINED_WEAKER_CONJECTURAL_GATE_A_ALTERNATIVE
V54_V52_PAD_ROUTE = RETAINED_WEAKER_CONJECTURAL_GATE_A_ALTERNATIVE
V54_V42_MPD_ROUTE = RETAINED_INDEPENDENT_CONJECTURAL_GATE_B_ALTERNATIVE
V54_DIRECT_PRIMARY_SOURCE_FOR_LONGITUDINAL_MODE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V54_DIRECT_PRIMARY_SOURCE_FOR_TRANSVERSE_REASSEMBLY = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V54_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_THE_KAPPA_LONGITUDINAL_PAIRED_ROW_MODE_EQUIVALENT_UP_TO_PAID_ERROR_TO_THE_PHYSICAL_TWIN_PRIME_RESIDUAL__AND_THE_COMMON_TRANSVERSE_ROW_VARIANCE_REMAINS_INDEPENDENTLY_OPEN
V54_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_PAIRED_ROW_MODE_DIAGONALIZATION_AND_TERMINAL_PACKAGE_FIREWALL
V54_SMALL_PAPER_STATUS = UNNUMBERED_OUTLINE_ONLY_NO_STANDALONE_ASYMPTOTIC_THEOREM
V54_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_PAIRED_ROW_TRANSVERSE_DECK_IDENTIFIED_LONGITUDINAL_TERMINAL_CABLE_OPEN
V54_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V54_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
```

## 54. V53 后的罗盘：pair-row Bessel 与 symmetric two-gate bridge

V53 仍位于解析消去岛 / Bridge A，但把 V52 的 global pair-angle首选路改成更
BDH/dispersion-native 的 completed prime-row接口。令

\[
 A_q^\circ=\sum_{q\nmid t}\beta^\circ(t)\mathcal R_q(t),\qquad
 \mathcal E_A^{\rm row}=\sum_q|A_q^\circ|^2,
\]

则 frozen Gate-A scalar exact为
\(\mathfrak F_x^\circ=\sum_q qA_q^\circ\)。V53 已无条件支付 collision diagonal

\[
 \mathcal D_A^{\rm row}\ll x^{95/48+o(1)}.
\]

若 full row energy相对 diagonal只损失 \(x^{\tau_A}\)，则

\[
 |\mathfrak F_x^\circ|\ll x^{143/96+\tau_A/2+o(1)},
 \qquad \tau_A<419/1200.
\]

选定 `tau_A=1/3` 即 one-`Q` loss，给 row energy `x^(37/16+o(1))`、
numerator `x^(53/32+o(1))` 与 margin `19/2400`。V40 Gate-B row的 collision
diagonal有相同 `x^(95/48+o(1))` 尺度，因此新主桥是 literal two-species theorem
`H_2RB(1/3,1/3)`：pair row保留 physical diagonal，physical row删除 diagonal；
两者都必须在每个 `q` 内先完成 signed cancellation，再作 prime-shell Cauchy。

普通 polarized marginal BDH会把未知 physical cross-diagonal作为 main term原样返回；
small global scalar或有利 PAD angle也不能推出小 row energy。Harper、Runbo Li、Pascadi、
Zheng与 Blomer--Pascadi均不直接接受上述 q-dependent two-row second moment；最后一个只
保留为合法 emitter之后的 fixed-modulus local engine。

V53 选择路线为：global Siegel quality若无界则沿 V50 conditional exit；否则优先
symmetric pair/physical row Bessel，再保留 V52 PAD、V42 MPD与 V50 bounded core
作为彼此独立的 fallback，最后只经 V43 exact join。该路线若证明可条件性给
`|S_physical|<<x^(95/96+o(1))`；当前 arithmetic advance仍为 NO。

~~~text
V53_MAXIMUM_CLAIM = EXACT_PAIR_ROW_COMPRESSION_PAID_COLLISION_DIAGONAL_AND_SYMMETRIC_TWO_GATE_ROW_BESSEL_COMPILER_REDUCE_BRIDGE_A_TO_ONE_Q_LOSS_FOR_TWO_LITERAL_ROW_SPECIES
V53_ROUTE_ADVANCE = YES
V53_CONDITIONAL_BRIDGE_ADVANCE = YES
V53_ARITHMETIC_ADVANCE = NO
V53_FIXED_ATOM_CREDIT = 0
V53_STRICT_1_OVER_400 = UNPAID
V53_L2 = NONE
V53_TPC_207_TRIGGER = false
V53_NUMBERED_RELEASE = NO
V53_DERIVATION_STATUS = COHERENT_AFTER_PAIR_ROW_COMPRESSION_COLLISION_DIAGONAL_ENDPOINT_LAW_AND_TWO_GATE_CROSSWALK
V53_ASSUMPTION_POLICY = ROW_BESSEL_AND_CHARACTER_FOURTH_MOMENT_REMAIN_CONJECTURAL__PAID_DIAGONALS_AND_FINITE_FIXTURES_RECEIVE_NO_ASYMPTOTIC_CREDIT
V53_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_SYMMETRIC_TWO_SPECIES_ROW_BESSEL__PAD_AND_MPD_FALLBACKS__V43_JOIN__DYNAMICS_RESERVE
V53_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO
V53_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__DILATION_31_OVER_96
V53_FROZEN_GATE_A_OBJECT = RETAINED_EXACT_V52_COMPENSATED_PAIR_DILATION
V53_PAIR_ROW_SCALAR = PROVED_EXACT_A_Q_CIRCLE_SUMS_BETA_CIRCLE_TIMES_R_Q
V53_PAIR_ROW_SHELL_IDENTITY = PROVED_EXACT_F_CIRCLE_EQUALS_SUM_Q_Q_A_Q_CIRCLE
V53_Q_SHELL_CAUCHY = PROVED_EXACT_SUM_Q_SQUARED_FACTOR_X_1_PLUS_O1
V53_PAIR_ROW_ENERGY = DEFINED_EXACT_SUM_Q_ABS_A_Q_CIRCLE_SQUARED
V53_PAIR_COLLISION_EXPANSION = PROVED_EXACT_DIAGONAL_PLUS_SIGNED_OFFDIAGONAL
V53_PAIR_COLLISION_OFFDIAGONAL = SIGNED_NOT_POSITIVE_AND_MUST_REMAIN_INSIDE_ROW_ENERGY
V53_PAIR_ROW_POINTWISE_KERNEL = PROVED_H_OVER_Q_TIMES_X_O1_WITH_BOTH_COMPENSATED_LINES_INCLUDED
V53_PAIR_ROW_DIAGONAL = PROVED_X_95_OVER_48_PLUS_O1
V53_PAIR_ROW_BESSEL_HYPOTHESIS = CONJECTURAL_H_A_RB_TAU_A
V53_PAIR_ROW_BESSEL_ENDPOINT = TAU_A_STRICTLY_LESS_THAN_419_OVER_1200
V53_PAIR_ROW_OUTPUT_LAW = X_143_OVER_96_PLUS_TAU_A_OVER_2_PLUS_O1
V53_SELECTED_ONE_Q_LOSS = TAU_A_EQUALS_1_OVER_3
V53_SELECTED_PAIR_ROW_ENERGY = X_37_OVER_16_PLUS_O1
V53_SELECTED_PAIR_ROW_OUTPUT = X_53_OVER_32_PLUS_O1
V53_SELECTED_PAIR_ROW_MARGIN = 19_OVER_2400
V53_TRIVIAL_FULL_X_ROW_LOSS = TAU_A_EQUALS_1
V53_TRIVIAL_ROW_OUTPUT = X_191_OVER_96_PLUS_O1
V53_TRIVIAL_ROW_DEFICIT = 781_OVER_2400
V53_PHYSICAL_DIAGONAL_TOGGLE = PROVED_EXACT_R_Q_EQUALS_G_Q_PLUS_C_PRIME_Q_ZERO_W
V53_PHYSICAL_DIAGONAL_POLICY = RETAINED_INSIDE_A_Q_BEFORE_SQUARE_AND_OUTER_ABSOLUTE
V53_POLARIZED_GENERIC_BDH = NO_GO_RETURNS_THE_UNKNOWN_PHYSICAL_CROSS_DIAGONAL_AS_MAIN
V53_Q5_DIAGONAL_FIXTURE = PROVED_EXACT_35_OVER_2_MINUS_15_OVER_2_EQUALS_10
V53_PAIR_CHARACTER_ROW = PROVED_EXACT_ONE_OVER_Q_MINUS_1_NONPRINCIPAL_PRODUCT_AVERAGE
V53_PAIR_CHARACTER_FOURTH_MOMENT = CONJECTURAL_STRONGER_SUFFICIENT_INTERFACE_AT_X_37_OVER_16
V53_SEPARATE_CHARACTER_SECOND_MOMENTS = NO_GO_DO_NOT_PROVE_THE_JOINT_PRODUCT_FOURTH_MOMENT
V53_GATE_B_ROW = RETAINED_EXACT_V40_DIAGONAL_DELETED_COMPENSATED_ROW
V53_GATE_B_COLLISION_DIAGONAL = RETAINED_PROVED_X_95_OVER_48_PLUS_O1
V53_TWO_SPECIES_ROW_BESSEL = CONJECTURAL_H_2RB_TAU_A_TAU_B_FOR_TWO_LITERAL_ROWS_ONLY
V53_TWO_SPECIES_ENDPOINT = PROVED_CONDITIONAL_IF_MAX_TAU_STRICTLY_LESS_THAN_419_OVER_1200
V53_SYMMETRIC_ONE_Q_BENCHMARK = TAU_A_EQUALS_TAU_B_EQUALS_1_OVER_3
V53_SYMMETRIC_TWO_GATE_OUTPUTS = BOTH_X_53_OVER_32_PLUS_O1
V53_SYMMETRIC_PHYSICAL_ENDPOINT_MARGIN = ANY_ETA_STRICTLY_BETWEEN_0_AND_19_OVER_2400_AFTER_V43
V53_SQUARE_ROW = RETAINED_PAID_X_143_OVER_96_PLUS_O1
V53_HARD_SHELL_BOUNDARY = RETAINED_PAID_WITH_11_OVER_600_MINUS_EPSILON_MARGIN
V53_ROW_BESSEL_VERSUS_DIRECT_SCALAR = STRICTLY_STRONGER_SUFFICIENT_INTERFACE_CROSS_Q_CANCELLATION_DISCARDED
V53_CROSS_Q_FIXTURE = PROVED_FORMAL_5_TIMES_7_PLUS_7_TIMES_MINUS_5_EQUALS_0_WITH_ROW_ENERGY_74
V53_SIGNED_COLLISION_FIXTURE = PROVED_FORMAL_ROW_ENERGY_4_DIAGONAL_22_OFFDIAGONAL_MINUS_18
V53_ALIGNED_ROW_FIXTURE = PROVED_FORMAL_ROW_ENERGY_16_DIAGONAL_4
V53_V52_PAD_ROUTE = RETAINED_INDEPENDENT_CONJECTURAL_ALTERNATIVE
V53_V42_MPD_ROUTE = RETAINED_INDEPENDENT_CONJECTURAL_GATE_B_ALTERNATIVE
V53_V50_BOUNDED_CORE = RETAINED_SEQUENTIAL_CONJECTURAL_ALTERNATIVE
V53_HARPER_GENERAL_BDH = NO_GO_DIRECT_FIXED_SEQUENCE_Q_ABOVE_SQRT_2X_AND_DILATION_HYPOTHESIS_MISMATCH
V53_RUNBO_LI_LARGE_MODULI = NO_GO_DIRECT_FIXED_RESIDUE_FIRST_MOMENT_AND_FACTORIZABLE_MODULUS_WEIGHT_MISMATCH
V53_PASCADI_TRIPLY_FACTORABLE = NO_GO_DIRECT_FIXED_RESIDUE_PRIME_AP_AND_MODULUS_WEIGHT_MISMATCH
V53_ZHENG_SIMULTANEOUS_AP = NO_GO_DIRECT_FIXED_RESIDUE_AND_MOVING_PRODUCT_ROW_MISMATCH
V53_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_LOCAL_CELL_ONLY
V53_DIRECT_PRIMARY_SOURCE_FOR_H_A_RB = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V53_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_THE_ONE_Q_RESTRICTED_ROW_BESSEL_BOUND_FOR_THE_DIAGONAL_COMPLETED_FOLDED_PAIR_ROW__AND_THE_MATCHING_GATE_B_ROW_BOUND_REMAINS_INDEPENDENTLY_OPEN
V53_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_PAIR_ROW_DIAGONAL_ONE_Q_ENDPOINT_AND_SYMMETRIC_TWO_GATE_SCHEMA
V53_SMALL_PAPER_STATUS = UNNUMBERED_OUTLINE_ONLY_NO_STANDALONE_ASYMPTOTIC_THEOREM
V53_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_SYMMETRIC_PAIR_AND_PHYSICAL_ROW_BESSEL_PIERS_OPEN
V53_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V53_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~


## 53. V52 后的罗盘：compensated pair dilation 与 angular Gate A

V52 继续位于解析消去岛 / Bridge A。V51 已把 mixed、reverse Type I 与 balanced
orientations先折叠成一个无序因子对；V52 进一步证明同一个 non-square scalar 是

\[
 \mathfrak F_x^\circ
 =\sum_{q\in\mathcal Q}q
 \sum_{\substack{t\in I_x\\q\nmid t}}
 \beta^\circ(t)\mathcal R_q(t),
\]

其中

\[
 \mathcal R_q(t)=
 \sum_{t+qk\in I_x}w(t+qk)K_H(qk)
 -\frac1{q-1}\sum_{\substack{u\in I_x\\q\nmid u}}
  w(u)K_H(u-t).
\]

第一项保留 $k=0$ diagonal，第二项保留 unit principal mean；自然 smooth length
$H/q=x^{31/96+o(1)}$。pair coefficient 也有 exact truncated-sieve interface：

\[
 \beta^\circ(t)=\frac{\Lambda(t)}{\log t}
 -\sum_{d\mid t,\,d\le U}\mu(d)
 -\mathbf1_{t=r^2}\frac{\mu(r)}2.
\]

所以 balanced lane 含有 $U<p<r$ semiprimes的 signed reverse-Chen slice；它只是
subchannel，不可脱离 Möbius parity 与 hybrid comparator单独估计。

character packet exact给
\[
 |\mathfrak F_x^\circ|
 =\varrho_{BW}\sqrt{\mathcal E_B\mathcal E_W}.
\]
若 marginal savings为 $\delta_B,\delta_W$，angular saving为 $\kappa$，则 Gate-A
saving margin为
\[
 \eta_{\rm PAD}
 =\kappa+\frac{\delta_B+\delta_W}{2}-\frac1{400}.
\]
diagonal-scale BDH 加普通 Cauchy恰缺 $1/400$；因此首选新定理是同一 literal packet
的 $\kappa>1/400$ joint angular dispersion。zero-angle fallback必须有
$\delta_B+\delta_W>1/200$。equal-norm parallel/orthogonal fixture证明 marginal
norms本身不决定 angle。

当前 source screen 只有 architecture analogues与 conditional local engines：
Zheng的 simultaneous AP ranges停在 $7/36$、$2/23$ 且 residues固定；Drappeau 与
Wright对象也固定；Blomer--Pascadi/Pascadi只可在合法 emitter 与 norms之后作局部
engine。没有 source证明 $\mathsf H_{\rm PAD}$。

当前位置：

~~~text
UNBOUNDED_SIEGEL_QUALITY -> CONDITIONAL_DIRECT_TPC_EXIT
OTHERWISE V52 PAIR-ANGULAR GATE A -> OPEN
V42 POSITIVE-GRAM GATE B -> OPEN IN PARALLEL
V43 ZERO-AXIS AND COMPILER -> EXACT
DYNAMICS / DISTINGUISHED SEED -> RESERVE
~~~

V52 仍是路线级 advance，不是 arithmetic advance；阶段性 paper ledger新增
compensated dilation、reverse-Chen slice、endpoint simplex与 marginal-only no-go。

~~~text
V52_MAXIMUM_CLAIM = EXACT_COMPENSATED_PAIR_DILATION_AND_PACKET_ENDPOINT_COMPILER_IDENTIFIES_THE_FOLDED_GATE_A_AS_A_REVERSE_CHEN_PARITY_RESIDUAL_AND_PROVES_THE_MARGINAL_BDH_PLUS_CAUCHY_COMPILER_MISSES_BY_1_OVER_400
V52_ROUTE_ADVANCE = YES
V52_CONDITIONAL_BRIDGE_ADVANCE = YES
V52_ARITHMETIC_ADVANCE = NO
V52_FIXED_ATOM_CREDIT = 0
V52_STRICT_1_OVER_400 = UNPAID
V52_L2 = NONE
V52_TPC_207_TRIGGER = false
V52_NUMBERED_RELEASE = NO
V52_DERIVATION_STATUS = COHERENT_AFTER_DUAL_PAIR_SIEVE_IDENTITY_COMPENSATED_DILATION_HILBERT_PACKET_AND_ENDPOINT_SIMPLEX
V52_ASSUMPTION_POLICY = PAIR_ANGULAR_DISPERSION_IS_CONJECTURAL__MARGINAL_AND_LOCAL_SOURCE_RESULTS_RECEIVE_NO_JOINT_CREDIT
V52_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_PAIR_ANGULAR_GATE_A__V42_GATE_B__V43_JOIN__DYNAMICS_RESERVE
V52_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO
V52_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__DILATION_31_OVER_96
V52_FOLDED_PAIR_INTERFACE = RETAINED_EXACT_MIXED_PLUS_BALANCED_OMEGA_U
V52_TRUNCATED_SIEVE_INTERFACE = RETAINED_EXACT_LAMBDA_OVER_LOG_MINUS_MU_LE_U_CONVOLUTION
V52_DUAL_COEFFICIENT_INTERFACE = PROVED_EXACT_SAME_BETA_AFTER_SQUARE_ROW_SUBTRACTION
V52_PRIME_ROW_CANCELLATION = PROVED_EXACT_ONE_MINUS_ONE_EQUALS_ZERO
V52_MIXED_SEMIPRIME_SLICE = PROVED_EXACT_ZERO_FOR_P_LE_U_LT_R
V52_BALANCED_SEMIPRIME_SLICE = PROVED_EXACT_MINUS_ONE_FOR_U_LT_P_LT_R
V52_SQUARE_PRIME_SLICE = PROVED_EXACT_MINUS_ONE_HALF
V52_REVERSE_CHEN_INTERPRETATION = PROVED_EXACT_SUBCHANNEL_NOT_A_STANDALONE_ESTIMATE
V52_MULTI_PAIR_T12_FIXTURE = PROVED_FORMAL_LOG_COLLAPSE_TO_ONE
V52_COMPENSATED_PAIR_DILATION_ROW = PROVED_EXACT_DIVISIBILITY_MINUS_UNIT_PRINCIPAL_MEAN
V52_COMPENSATED_PAIR_DILATION_SCALAR = PROVED_EXACT_ONE_COMMON_PRIME_SHELL_AND_ONE_SIGNED_AGGREGATE
V52_DILATION_NATURAL_LENGTH = H_OVER_Q_EQUALS_X_31_OVER_96
V52_DILATION_HARD_SUPPORT_POLICY = EXACT_T_PLUS_QK_IN_I_WITH_SCHWARTZ_NOT_COMPACT_K_TAIL
V52_DILATION_SPLIT_ABSOLUTE_CEILING = X_191_OVER_96_PLUS_O1
V52_DILATION_SPLIT_DEFICIT = 781_OVER_2400
V52_Q5_DILATION_FIXTURE = PROVED_EXACT_20_MINUS_10_EQUALS_10
V52_PAIR_CHARACTER_PACKET = RETAINED_EXACT_NONPRINCIPAL_CHARACTER_FOURIER_AGGREGATE
V52_HILBERT_PACKET_IDENTITY = PROVED_EXACT_F_CIRCLE_EQUALS_INNER_PRODUCT_X_Y
V52_PACKET_COHERENCE = DEFINED_EXACT_ZERO_TO_ONE_NO_ARITHMETIC_CREDIT
V52_CHARACTER_DIAGONAL_FORMULA = PROVED_EXACT_Q_Q_MINUS_2_OVER_Q_MINUS_1_WEIGHT
V52_DIAGONAL_SCALE = X_5_OVER_3_PLUS_O1_UPPER_BENCHMARK
V52_DIAGONAL_SCALE_LOWER_BOUND = NOT_ASSERTED_OFFDIAGONAL_CAN_HAVE_EITHER_SIGN
V52_MARGINAL_BDH_BASELINE = CONJECTURAL_E_B_AND_E_W_LE_X_5_OVER_3_PLUS_O1
V52_MARGINAL_BDH_PLUS_CAUCHY = NO_GO_MISSES_TARGET_BY_EXACT_1_OVER_400
V52_PACKET_ENDPOINT_LAW = PROVED_CONDITIONAL_KAPPA_PLUS_HALF_DELTA_SUM_MINUS_1_OVER_400
V52_BASELINE_MARGINAL_ANGULAR_THRESHOLD = KAPPA_GT_1_OVER_400
V52_ZERO_ANGLE_TOTAL_SUPER_BDH_THRESHOLD = DELTA_B_PLUS_DELTA_W_GT_1_OVER_200
V52_ONE_SIDED_SUPER_BDH_THRESHOLD = DELTA_GT_1_OVER_200
V52_ONE_GENERIC_ONE_BDH_DEFICIT = 203_OVER_1200
V52_TWO_GENERIC_CHARACTER_DEFICIT = 403_OVER_1200
V52_MARGINAL_NORMS_DETERMINE_ANGLE = NO_GO_PARALLEL_ORTHOGONAL_EQUAL_NORM_FIXTURE
V52_PAIR_ANGULAR_DISPERSION_GATE = CONJECTURAL_H_PAD_DELTA_B_DELTA_W_KAPPA
V52_PREFERRED_PAD_REGIME = DIAGONAL_SCALE_MARGINALS_AND_KAPPA_GT_1_OVER_400
V52_SUPER_BDH_REGIME = RETAINED_LEGAL_ALTERNATIVE_IF_TOTAL_SAVING_GT_1_OVER_200
V52_PAD_TO_V51_H_FOLD = PROVED_CONDITIONAL_WITH_ETA_PAD_POSITIVE
V52_PAD_TO_PHYSICAL_ENDPOINT = PROVED_CONDITIONAL_AFTER_INDEPENDENT_V42_GATE_B_AND_V43_JOIN
V52_TWO_GATE_MARGIN = MIN_ETA_PAD_ETA_B_419_OVER_2400_19_OVER_2400_AND_11_OVER_600_MINUS_EPSILON
V52_ZHENG_SIMULTANEOUS_AP = NO_GO_DIRECT_THETA_FIXED_RESIDUE_SIEGEL_WALFISZ_AND_MOVING_PRODUCT_MISMATCH
V52_DRAPPEAU_DISPERSION = NO_GO_DIRECT_FIXED_PRODUCT_AND_MODULUS_INDEPENDENT_ARRAY_MISMATCH
V52_WRIGHT_UNBALANCED_CONVOLUTION = NO_GO_DIRECT_FIXED_RESIDUE_AND_SHORT_SIEGEL_WALFISZ_SEQUENCE_MISMATCH
V52_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_LOCAL_CELL_ONLY
V52_PASCADI_EXCEPTIONAL_SIEVE = SOURCE_BACKED_CONDITIONAL_AFTER_LITERAL_TRANSFORM_AND_NORM
V52_DIRECT_PRIMARY_SOURCE_FOR_H_PAD = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V52_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_A_POWER_SAVING_PAIR_ENDPOINT_ANGLE_OR_TOTAL_SUPER_BDH_SAVING_ABOVE_1_OVER_200_FOR_THE_COMPENSATED_MOVING_PRODUCT_PRIME_DILATION
V52_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V52_V50_BOUNDED_CORE = RETAINED_SEQUENTIAL_CONJECTURAL_ALTERNATIVE
V52_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_COMPENSATED_DILATION_REVERSE_CHEN_SLICE_ENDPOINT_SIMPLEX_AND_MARGINAL_NO_GO
V52_SMALL_PAPER_STATUS = UNNUMBERED_OUTLINE_ONLY_NO_STANDALONE_ASYMPTOTIC_THEOREM
V52_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_PAIR_ANGULAR_GATE_A_MAPPED_ARITHMETIC_BOUND_OPEN
V52_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V52_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~


## 52. V51 后的罗盘：fold-first pair-native Gate A 与阶段性论文轨

V51 把 V43 的 ordered proper-factor atlas 在第一道 outer absolute 之前重新按无序
因子对折叠。对 \(t=s\ell\)、\(s<\ell\)，两个 orientation 的 logarithmic numerator
在 mixed 区 \(s\le U<\ell\) 精确变成
\((\mu(\ell)-\mu(s))\log s\)，在 balanced 区 \(U<s<\ell\) 精确变成
\(\mu(s)\log\ell+\mu(\ell)\log s\)。square row为 \(\mu(s)/2\)，而
\(1/\log(s\ell)\) 有 exact Abel compiler。因此 mixed+balanced numerator 的变量分离
rank至多二，不再需要把 reverse Type I 与 Type II 当成两个互不相干的桥。

对角补全后的 pair row与 V43 Gate-A numerator只差已付的 shell、unit与 square项；
nonprincipal-character/Fourier projector又把它写成一个保留 physical \(W\)、prime shell、
hard product shell、sign、nonunit与 zero-axis 的 signed aggregate。当前位置为：

~~~text
Bridge A / analytic-elimination island
fold-first pair-native Gate-A compiler DONE_L0
mixed + balanced whole-object fixed-power theorem CONJECTURAL OPEN
square lane PAID at x^(143/96+o(1))
orientation-first Poisson NO_GO
V50 bounded-quality core RETAINED SEQUENTIAL ALTERNATIVE
V42 Gate B PARALLEL OPEN
paper candidate ledger CREATED, no standalone theorem package yet
arithmetic advance NO
~~~

如果 global Siegel quality无界，V50 source-backed conditional exit仍优先；否则当前主攻
是

\[
|\mathfrak F_x^{\rm mix}+\mathfrak F_x^{\rm bal}|
\ll x^{1997/1200-\eta_L+o(1)}.
\]

Blomer--Pascadi 与 Pascadi是可复用 local engines，但尚无 source theorem接受完整
fold-first literal object。阶段性成果按 PROVED、SOURCE_BACKED_CONDITIONAL、
CONJECTURAL、NO_GO 四类进入 `research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md`，避免
把桥梁蓝图误写成已完成算术定理。

canonical registry：

~~~text
V51_MAXIMUM_CLAIM = EXACT_FOLD_FIRST_UNORDERED_PAIR_DIAGONAL_COMPLETED_EMITTER_REPRESENTS_THE_V43_GATE_A_NUMERATOR_UP_TO_PAID_ERRORS_AND_REDUCES_MIXED_PLUS_BALANCED_LONG_MOBIUS_TO_ONE_CONJECTURAL_SIGNED_THEOREM
V51_ROUTE_ADVANCE = YES
V51_CONDITIONAL_BRIDGE_ADVANCE = YES
V51_ARITHMETIC_ADVANCE = NO
V51_FIXED_ATOM_CREDIT = 0
V51_STRICT_1_OVER_400 = UNPAID
V51_L2 = NONE
V51_TPC_207_TRIGGER = false
V51_NUMBERED_RELEASE = NO
V51_DERIVATION_STATUS = COHERENT_AFTER_UNORDERED_FOLD_RANK_TWO_NUMERATOR_ABEL_COMPILER_DIAGONAL_COMPLETED_CROSSWALK_AND_CHARACTER_FOURIER_EMITTER
V51_ASSUMPTION_POLICY = FOLD_FIRST_MIXED_PLUS_BALANCED_BOUND_IS_CONJECTURAL__LOCAL_SPECTRAL_RESULTS_ARE_SOURCE_BACKED_CONDITIONAL__ORIENTATION_FIRST_TRIANGLE_IS_NO_GO
V51_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_FOLD_FIRST_GATE_A_WHOLE_OBJECT__V42_GATE_B__V43_JOIN__DYNAMICS_RESERVE
V51_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO
V51_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__Y0_31_OVER_96
V51_ORDERED_PROPER_FACTOR_IDENTITY = RETAINED_EXACT_FROM_V43
V51_FOLDED_NONSQUARE_IDENTITY = PROVED_EXACT_TWO_ORIENTATION_SUM
V51_FOLDED_SQUARE_IDENTITY = PROVED_EXACT_MU_S_OVER_2
V51_U_SQUARED_SUPPORT = PROVED_X_133_OVER_200_LT_X_OVER_2
V51_MIXED_PAIR_NUMERATOR = PROVED_EXACT_MU_L_MINUS_MU_S_TIMES_LOG_S
V51_BALANCED_PAIR_NUMERATOR = PROVED_EXACT_MU_S_LOG_L_PLUS_MU_L_LOG_S
V51_PAIR_NUMERATOR_SEPARATION_RANK = PROVED_AT_MOST_TWO_BEFORE_PRODUCT_LOG_DENOMINATOR
V51_PRODUCT_LOG_DENOMINATOR = PROVED_EXACT_ONE_DIMENSIONAL_ABEL_COMPILER
V51_PAIR_DIAGONAL_COMPLETED_ROW = DEFINED_WITH_DIAGONAL_AND_LITERAL_PHYSICAL_DATA
V51_PAIR_ROW_CROSSWALK = PROVED_EXACT_F_Q_EQUALS_S_Q_PLUS_C_Q_ZERO_TIMES_S_Q_UNIT
V51_PAIR_SCALAR_CROSSWALK = PROVED_F_EQUALS_C_PLUS_B_Q_S_PHYSICAL_PLUS_UNIT_ERROR
V51_PAIR_TO_V43_GATE_A = PROVED_UP_TO_X_79_OVER_48_PLUS_EPSILON_X_4_OVER_3_AND_X_1_ERRORS
V51_UNIT_OMISSION = RETAINED_PAID_X_4_OVER_3_PLUS_O1
V51_SHELL_FREEZE_ERROR = RETAINED_PAID_X_79_OVER_48_PLUS_EPSILON_PLUS_O1
V51_NONPRINCIPAL_CHARACTER_PROJECTOR = PROVED_EXACT_FOR_UNIT_RESIDUES
V51_FOURIER_KERNEL_SEPARATION = PROVED_EXACT_FROM_PSI_TRANSFORM_CONVENTION
V51_PAIR_CHARACTER_FOURIER_EMITTER = PROVED_EXACT_ONE_OUTER_SIGNED_AGGREGATE
V51_LITERAL_DATA_RETENTION = PROVED_COMMON_Q_SHELL_W_HARD_PRODUCT_SHELL_SIGNS_PHYSICAL_UNIT_RESTRICTIONS_AND_ZERO_AXIS
V51_PAIR_LANE_SPLIT = PROVED_EXACT_MIXED_PLUS_BALANCED_PLUS_SQUARE
V51_SQUARE_SCALAR_PAYMENT = RETAINED_X_143_OVER_96_PLUS_O1
V51_SQUARE_MARGIN_TO_TARGET = 419_OVER_2400
V51_FOLD_FIRST_WHOLE_OBJECT_GATE = CONJECTURAL_H_FOLD_ETA_L
V51_FOLD_FIRST_GATE_IMPLIES_V43_GATE_A = PROVED_CONDITIONAL_WITH_PAID_ERROR_MARGINS
V51_FOLD_FIRST_BYPASS = SELECTED_BROAD_ALTERNATIVE_TO_SEQUENTIAL_BOUNDED_CORE_REVERSE_TYPE_I_AND_BALANCED_TYPE_II
V51_BOUNDED_QUALITY_CORE = RETAINED_V50_CONJECTURAL_ALTERNATIVE
V51_BOUNDED_QUALITY_POINTWISE_POWER = NO_GO_CONSTANT_RELATIVE_DECAY_NOT_X_POWER
V51_SEMIPRIME_FOLD_CANCELLATION = PROVED_EXACT_ZERO_WITH_NONZERO_ORIENTATION_ABSOLUTE_MASS
V51_ORIENTATION_SUPPORT_MISMATCH = PROVED_FINITE_6_10_Q11_H50_LENGTHS_1_AND_2
V51_ORIENTATION_FIRST_POISSON = NO_GO_DESTROYS_EXACT_FOLD_BEFORE_OUTER_ABSOLUTE
V51_POST_TRANSFORM_ORIENTATION_REASSEMBLY = NO_GO_NO_TERMWISE_RECOVERY_OF_FOLDED_ZERO
V51_GENERIC_CHARACTER_LARGE_SIEVE = PROVED_CEILING_X_2_PLUS_O1
V51_GENERIC_CHARACTER_LARGE_SIEVE_DEFICIT = 403_OVER_1200
V51_BLOMER_PASCADI_FIXED_MODULUS_CELL = SOURCE_BACKED_CONDITIONAL_C_MINUS_1_OVER_32_CRITICAL_SAVING
V51_PASCADI_HORIZONTAL_EXCEPTIONAL_SIEVE = SOURCE_BACKED_CONDITIONAL_AFTER_LITERAL_PAIR_EMITTER_AND_NORM
V51_WRIGHT_UNBALANCED_CONVOLUTION = NO_GO_SIEGEL_WALFISZ_SHORT_SEQUENCE_AND_WRONG_JOINT_OBJECT
V51_MILICEVIC_QIN_WU_FIXED_MODULUS = NO_GO_POST_TRANSFORM_CELL_WITHOUT_COMMON_Q_PAIR_EMITTER_OR_REASSEMBLY
V51_DONG_ROBLES_ZEINDLER_2601_00292 = NO_GO_WITHDRAWN_MISSING_L_SQUARED_FACTOR
V51_DIRECT_PRIMARY_SOURCE_FOR_H_FOLD = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V51_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_THE_FOLD_FIRST_MIXED_PLUS_BALANCED_PAIR_NATIVE_GATE_A_AGGREGATE_WITH_PHYSICAL_W_AND_ONE_OUTER_SIGN_AT_FIXED_POWER
V51_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V51_TWO_GATE_COMPILER = RETAINED_V43_GATE_A_AND_GATE_B
V51_TWO_GATE_MARGIN = MIN_ETA_L_ETA_B_419_OVER_2400_19_OVER_2400_AND_11_OVER_600_MINUS_EPSILON
V51_PAPER_CANDIDATE_LEDGER = CREATED_PARALLEL_PROVED_CONDITIONAL_CONJECTURAL_NO_GO_TRACK
V51_SMALL_PAPER_STATUS = UNNUMBERED_OUTLINE_ONLY_NO_STANDALONE_THEOREM_PACKAGE_YET
V51_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_FOLD_FIRST_PAIR_NATIVE_GATE_A_MAPPED_ARITHMETIC_BOUND_OPEN
V51_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V51_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~

## 51. V50 后的罗盘：self-financing endpoint core 与 Siegel-quality 二世界

V50 把 V49 的单一 midpoint 推广成严格开区间。对任意
\(0<\delta<1/9600\)，定义

\[
D_\delta=x^{1/200+2\delta}.
\]

V45 block bound 于是把 complementary conductor range 精确支付到

\[
|\mathfrak V_{\ge D_\delta}^{\rm tr}|
\ll x^{1997/1200-\delta+o(1)}.
\]

剩余 core 为

\[
\mathfrak C_\delta=\mathfrak M_{<D_\delta}^{\rm tr}-\mathfrak L_x^{\rm pf},
\qquad
\mathfrak R_x^{\rm AP}=\mathfrak C_\delta+
\mathfrak V_{\ge D_\delta}^{\rm tr}.
\]

第二个大路推进是 global Siegel-quality dichotomy。若 primitive quadratic
Siegel-zero qualities 无界，Matomaki--Merikoski Corollary 1.1(i) 对 \(h=2\)
给 source-backed direct twin-prime exit；若全局有界于某个有限 \(B\)，则只需证明
一个允许 \(\delta_B\)、threshold 与 implied constant 依赖 \(B\) 的 direct signed
endpoint core theorem。per-scale Landau--Page singleton 不能提升成全局无界质量。

当前位置：

~~~text
Bridge A / analytic-elimination island
moving conductor complement SELF-FINANCING for every 0<delta<1/9600
unbounded Siegel quality -> source-backed conditional TPC exit
bounded Siegel quality -> B-dependent signed endpoint core OPEN
long balanced and reverse-Type-I windows OPEN
V42 Gate B PARALLEL OPEN
arithmetic advance NO
~~~

canonical registry：

~~~text
V50_MAXIMUM_CLAIM = AN_OPEN_SAVING_PARAMETER_DELTA_IN_0_1_OVER_9600_GENERATES_AN_EXACT_SELF_FINANCING_CONDUCTOR_CUT_AND_THE_GLOBAL_SIEGEL_QUALITY_DICHOTOMY_SENDS_UNBOUNDED_QUALITY_TO_A_SOURCE_BACKED_TWIN_PRIME_EXIT_OR_REDUCES_BRIDGE_A_TO_A_BOUNDED_QUALITY_SIGNED_CORE_THEOREM
V50_ROUTE_ADVANCE = YES
V50_CONDITIONAL_BRIDGE_ADVANCE = YES
V50_ARITHMETIC_ADVANCE = NO
V50_FIXED_ATOM_CREDIT = 0
V50_STRICT_1_OVER_400 = UNPAID
V50_L2 = NONE
V50_TPC_207_TRIGGER = false
V50_NUMBERED_RELEASE = NO
V50_DERIVATION_STATUS = COHERENT_AFTER_SAVING_MATCHED_MOVING_CUT_GLOBAL_SIEGEL_QUALITY_DICHOTOMY_AND_SOURCE_BACKED_UNBOUNDED_QUALITY_EXIT
V50_ASSUMPTION_POLICY = BOUNDED_QUALITY_DIRECT_SIGNED_CORE_IS_PRIMARY_HEURISTIC_THEOREM__UNBOUNDED_QUALITY_IS_SOURCE_BACKED_CONDITIONAL_EXIT__MARGINAL_ENGINES_ARE_STRONGER_FALLBACKS
V50_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_DIRECT_TPC_EXIT__OTHERWISE_BOUNDED_QUALITY_ENDPOINT_CORE__THEN_LONG_MOBIUS__V42_GATE_B__V43_JOIN__C_RESERVE
V50_SAVING_PARAMETER_DOMAIN = OPEN_0_LT_DELTA_LT_1_OVER_9600
V50_BETA_DELTA = 1_OVER_200_PLUS_2_DELTA
V50_CUT_ORDER = PROVED_STRICT_1_OVER_200_LT_BETA_DELTA_LT_1_OVER_192
V50_V49_RECOVERY = DELTA_1_OVER_19200_GIVES_BETA_49_OVER_9600
V50_MOVING_CONDUCTOR_SPLIT = PROVED_EXACT_T_COMMON_EQUALS_M_BELOW_D_DELTA_PLUS_V_AT_LEAST_D_DELTA
V50_COLLAR_BLOCK_BOUND = RETAINED_V45_P_SQUARED_TIMES_D_OVER_Q_PLUS_ONE_OVER_D
V50_COLLAR_COEFFICIENT_ENERGY = PROVED_X_POWER_19_OVER_1200_MINUS_2_DELTA_PLUS_O1
V50_OLD_HIGH_COEFFICIENT_ENERGY = RETAINED_X_POWER_1_OVER_64_PLUS_O1
V50_COMBINED_COEFFICIENT_ENERGY = PROVED_X_POWER_19_OVER_1200_MINUS_2_DELTA_PLUS_O1
V50_PAID_CONDUCTOR_REMAINDER = PROVED_V_AT_LEAST_D_DELTA_X_POWER_1997_OVER_1200_MINUS_DELTA_PLUS_O1
V50_PAID_CONDUCTOR_REMAINDER_MARGIN = DELTA
V50_DELTA_ZERO_ENDPOINT = STOP_SCOPED_ZERO_STRICT_MARGIN
V50_DELTA_UPPER_ENDPOINT = V48_D0_BOUNDARY_OUTSIDE_OPEN_V50_INTERIOR
V50_ENDPOINT_CORE = DEFINED_C_DELTA_EQUALS_M_BELOW_D_DELTA_MINUS_L_PF
V50_ENDPOINT_CORE_SPLICE = PROVED_EXACT_R_AP_EQUALS_C_DELTA_PLUS_V_AT_LEAST_D_DELTA
V50_BUDGET_MATCHED_CORE_GATE = OPEN_X_POWER_1997_OVER_1200_MINUS_DELTA_PLUS_O1
V50_TRANSITION_COMPILER = PROVED_BUDGET_MATCHED_CORE_GATE_PAYS_AP_TRANSITION
V50_TRANSITION_MARGIN = ANY_FIXED_DELTA_TR_STRICTLY_LESS_THAN_DELTA
V50_THREE_LANE_REASSEMBLY = RETAINED_EXACT_C_DELTA_EQUALS_C_PR_DELTA_PLUS_C_GEN_DELTA_PLUS_C_EXC_DELTA
V50_LANDAU_PAGE_EXCEPTION_SET = DEFINED_BEFORE_ESTIMATE_AT_LEVEL_D_DELTA
V50_LANDAU_PAGE_EXCEPTION_CARDINALITY = SOURCE_BACKED_EMPTY_OR_SINGLETON
V50_EXCEPTIONAL_INDUCED_TOWER = RETAINED_ALL_COFACTORS
V50_SIEGEL_QUALITY = DEFINED_ETA_CHI_TIMES_ONE_MINUS_BETA_TIMES_LOG_D_EQUALS_ONE
V50_GLOBAL_SIEGEL_QUALITY_DICHOTOMY = PROVED_EXHAUSTIVE_BOUNDED_OR_UNBOUNDED
V50_UNBOUNDED_QUALITY_WORLD = SOURCE_BACKED_CONDITIONAL_DIRECT_TWIN_PRIME_EXIT
V50_MATOMAKI_MERIKOSKI_COROLLARY_1_1 = SOURCE_BACKED_FIXED_H2_X_IN_D_POWER_10_TO_D_POWER_10_LOG_QUALITY_WITH_EXP_MINUS_C_SQRT_LOG_QUALITY_ERROR
V50_H2_SINGULAR_SERIES = PROVED_STRICTLY_POSITIVE
V50_PROPER_PRIME_POWER_CONTAMINATION = PROVED_O_X_POWER_1_OVER_2_LOG_CUBED_X
V50_UNBOUNDED_QUALITY_TO_TPC = PROVED_CONDITIONAL_FROM_SOURCE_CORRELATION_AND_PRIME_POWER_REMOVAL
V50_PER_SCALE_SINGLETON_TO_GLOBAL_UNBOUNDED = STOP_SCOPED_FALSE_QUANTIFIER_PROMOTION
V50_BOUNDED_QUALITY_WORLD = REDUCED_TO_FOR_EVERY_FIXED_B_ONE_B_DEPENDENT_ENDPOINT_MATCHED_DIRECT_SIGNED_CORE_GATE
V50_BOUNDED_QUALITY_GATE = OPEN_FOR_EVERY_FINITE_B_EXISTS_DELTA_B_WITH_DIRECT_SIGNED_CORE_X_POWER_TARGET_MINUS_DELTA_B
V50_BOUNDED_QUALITY_GATE_QUANTIFIERS = FOR_EVERY_FINITE_B__EXISTS_DELTA_B__EXISTS_C_B_X0_B__FOR_ALL_X_AT_LEAST_X0_B
V50_B_DEPENDENCE = ALLOWED_IN_DELTA_B_THRESHOLD_AND_IMPLIED_CONSTANT_NOT_IN_LATER_X
V50_DIRECT_SIGNED_GATE = SELECTED_ONE_SCALAR_BEFORE_OUTER_ABSOLUTE
V50_MARGINAL_THREE_ENGINE_PACKAGE = OPEN_STRONGER_SUFFICIENT_HEURISTIC_THEOREM
V50_MARGINAL_THREE_ENGINE_STRENGTH = STRONGER_NOT_EQUIVALENT_TO_DIRECT_SIGNED_GATE
V50_TRIANGLE_OVERPAY_FIREWALL = RETAINED_FINITE_SIGNED_CANCELLATION_FIXTURE_19_VERSUS_5
V50_DELETE_EXCEPTIONAL_LANE = STOP_SCOPED_CHANGES_LITERAL_SCALAR
V50_BFI_MOVING_COLLAR = SOURCE_BACKED_VIA_V45_PRIMITIVE_BLOCK_ESTIMATE
V50_FGKMT_LANDAU_PAGE = SOURCE_BACKED_PER_SCALE_EXCEPTIONAL_TYPE_AND_CARDINALITY_ONLY
V50_MATOMAKI_MERIKOSKI_UNBOUNDED_EXIT = SOURCE_BACKED_LITERAL_FIXED_SHIFT_CORRELATION
V50_SACHPAZIS_LARGE_MODULUS_AP = STOP_SCOPED_REQUIRES_X_EQUALS_D_POWER_V_WITH_V_AT_LEAST_200_OVER_EPSILON_AND_FIXED_AP_OBJECT
V50_WRIGHT_LARGE_MODULUS_AP = STOP_SCOPED_SUBPOWER_EXCEPTIONAL_CONDUCTOR_AND_AP_RESIDUE_OBJECT
V50_DIRECT_PRIMARY_SOURCE_FOR_BOUNDED_CORE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V50_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_THE_B_DEPENDENT_ENDPOINT_MATCHED_LOCAL_CENTERED_PRINCIPAL_GENERIC_EXCEPTIONAL_SIGNED_CORE_WITH_FIXED_POWER
V50_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U
V50_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U
V50_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V50_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_SELF_FINANCING_ENDPOINT_CORE_AND_TWO_SIEGEL_QUALITY_WORLDS_MAPPED_LONG_MOBIUS_OPEN
V50_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V50_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~

## 50. V49 后的罗盘：critical collar 已付，ultra-low three-lane scalar 开放

V49 把 V48 的 \(c<D_0=x^{1/192}\) 低导体红区再压缩一格。取
\(D_1=x^{49/9600}\)，V45 block bound支付全部 \(c\ge D_1\)，并给

\[
|\mathfrak V_{\ge D_1}^{\rm tr}|
\ll x^{31951/19200+o(1)},\qquad
\text{margin}=\frac1{19200}.
\]

剩余 theorem object不再是未分类的 low spectrum，而是

\[
\mathfrak C_{<D_1}^{\rm ul}
=\mathfrak M_{<D_1}^{\rm tr}-\mathfrak L_x^{\rm pf}
=\mathfrak C_{\rm pr}+\mathfrak C_{\rm gen}+\mathfrak C_{\rm exc}.
\]

exceptional set在估计前由 Landau--Page level \(D_1\) 声明，为空或 singleton
primitive quadratic type；全部 induced cofactors继续保留。主路直接估计三车道
signed sum，分别估计三个 marginal只是更强 heuristic fallback。

当前位置：

~~~text
Bridge A / analytic-elimination island
critical conductor collar PAID through D1
direct local-centered ultra-low three-lane scalar OPEN
long balanced and reverse-Type-I windows OPEN
V42 Gate B PARALLEL OPEN
arithmetic advance NO
~~~

canonical registry：

~~~text
V49_MAXIMUM_CLAIM = V45_SECOND_MOMENT_PAYS_THE_CRITICAL_CONDUCTOR_COLLAR_TO_D1_AND_THE_REMAINING_LOCAL_CENTERED_ULTRALOW_SCALAR_SPLITS_EXACTLY_INTO_PRINCIPAL_GENERIC_AND_UNIQUE_POSSIBLE_EXCEPTIONAL_LANES_BEFORE_OUTER_ABSOLUTE
V49_ROUTE_ADVANCE = YES
V49_CONDITIONAL_BRIDGE_ADVANCE = YES
V49_ARITHMETIC_ADVANCE = NO
V49_FIXED_ATOM_CREDIT = 0
V49_STRICT_1_OVER_400 = UNPAID
V49_L2 = NONE
V49_TPC_207_TRIGGER = false
V49_NUMBERED_RELEASE = NO
V49_DERIVATION_STATUS = COHERENT_AFTER_CRITICAL_COLLAR_PAYMENT_LOCAL_CENTERING_AND_EXCEPTIONAL_AWARE_THREE_LANE_SPLIT
V49_ASSUMPTION_POLICY = DIRECT_THREE_LANE_SIGNED_SCALAR_IS_PRIMARY_HEURISTIC_THEOREM_AND_SEPARATE_PRINCIPAL_GENERIC_EXCEPTIONAL_BOUNDS_ARE_STRONGER_FALLBACKS
V49_SELECTED_RESEARCH_ROUTE = PAY_CRITICAL_CONDUCTOR_COLLAR__ATTACK_DIRECT_LOCAL_CENTERED_ULTRALOW_THREE_LANE_SCALAR__THEN_LONG_MOBIUS__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE
V49_V48_COMMON_TRANSITION = RETAINED_EXACT_BEFORE_FIRST_OUTER_ABSOLUTE
V49_D1_DEFINITION = X_POWER_49_OVER_9600
V49_D1_THRESHOLD_ORDER = PROVED_STRICT_1_OVER_200_LT_49_OVER_9600_LT_1_OVER_192
V49_MOVING_CONDUCTOR_SPLIT = PROVED_EXACT_T_COMMON_EQUALS_M_BELOW_D1_PLUS_V_AT_LEAST_D1
V49_COLLAR_BLOCK_BOUND = RETAINED_V45_P_SQUARED_TIMES_D_OVER_Q_PLUS_ONE_OVER_D
V49_COLLAR_COEFFICIENT_ENERGY = PROVED_X_POWER_151_OVER_9600_PLUS_O1
V49_OLD_HIGH_COEFFICIENT_ENERGY = RETAINED_X_POWER_150_OVER_9600_PLUS_O1
V49_COMBINED_COEFFICIENT_ENERGY = PROVED_X_POWER_151_OVER_9600_PLUS_O1
V49_PAID_CONDUCTOR_REMAINDER = PROVED_V_AT_LEAST_D1_X_POWER_31951_OVER_19200_PLUS_O1
V49_PAID_CONDUCTOR_REMAINDER_MARGIN = 1_OVER_19200
V49_ULTRALOW_CENTERED_SCALAR = DEFINED_C_UL_EQUALS_M_BELOW_D1_MINUS_L_PF
V49_CENTERED_SCALAR_SPLICE = PROVED_EXACT_R_AP_EQUALS_C_UL_PLUS_V_AT_LEAST_D1
V49_LOCAL_EULER_LOCATION = RETAINED_INSIDE_SELECTED_ULTRALOW_SCALAR
V49_LOCAL_EULER_DOUBLE_COUNTING = STOP_SCOPED_DO_NOT_CHARGE_L_PF_BOTH_INSIDE_C_UL_AND_AS_EXTERNAL_ERROR
V49_DIRECT_ULTRALOW_GATE = OPEN_X_POWER_1997_OVER_1200_MINUS_ETA_UL_WITH_ETA_UL_POSITIVE
V49_ULTRALOW_TO_AP_RESIDUAL = PROVED_TERMINAL_EQUIVALENT_MODULO_PAID_CONDUCTOR_REMAINDER
V49_TRANSITION_CONDITIONAL_COMPILER = PROVED_DIRECT_ULTRALOW_GATE_PAYS_TRANSITION_WITH_CORRECTIONS
V49_TRANSITION_CONDITIONAL_MARGIN = MIN_ETA_UL_1_OVER_19200_13_OVER_4800_817_OVER_4800
V49_PRINCIPAL_LANE = PROVED_EXACT_CONDUCTOR_ONE_COMPONENT_MINUS_LOCAL_EULER_SCALAR
V49_GENERIC_LANE = PROVED_EXACT_ALL_NONPRINCIPAL_NONEXCEPTIONAL_PRIMITIVE_CONDUCTORS_BELOW_D1
V49_LANDAU_PAGE_EXCEPTION_SET = DEFINED_BEFORE_ESTIMATE_AT_LEVEL_D1
V49_LANDAU_PAGE_EXCEPTION_CARDINALITY = SOURCE_BACKED_EMPTY_OR_SINGLETON
V49_LANDAU_PAGE_EXCEPTION_TYPE = SOURCE_BACKED_UNIQUE_PRIMITIVE_QUADRATIC_CHARACTER_IF_PRESENT
V49_EXCEPTIONAL_LANE = PROVED_EXACT_POSSIBLE_EXCEPTIONAL_PRIMITIVE_ROW_WITH_ALL_INDUCED_COFACTORS
V49_THREE_LANE_REASSEMBLY = PROVED_EXACT_C_UL_EQUALS_C_PR_PLUS_C_GEN_PLUS_C_EXC
V49_DIRECT_THREE_LANE_GATE = SELECTED_ONE_SIGNED_SCALAR_BEFORE_OUTER_ABSOLUTE
V49_MARGINAL_THREE_ENGINE_PACKAGE = OPEN_STRONGER_SUFFICIENT_HEURISTIC_THEOREM
V49_MARGINAL_THREE_ENGINE_STRENGTH = STRONGER_NOT_EQUIVALENT_TO_DIRECT_SIGNED_GATE
V49_TRIANGLE_OVERPAY_FIREWALL = PROVED_FINITE_SIGNED_CANCELLATION_FIXTURE_19_VERSUS_5
V49_PRINCIPAL_LOCAL_RELATION = RETAINED_SCALAR_SUBTRACTION_ONLY
V49_PRINCIPAL_LOCAL_TERMWISE_PROJECTION = STOP_SCOPED_FALSE_EQUAL_SUM_DIFFERENT_VECTOR_FIXTURE
V49_EXCEPTIONAL_PRIMITIVE_RANK = AT_MOST_ONE_PRIMITIVE_CHARACTER_TYPE
V49_EXCEPTIONAL_INDUCED_TOWER = RETAINED_ALL_E_COFACTORS_NOT_ONE_SUMMAND
V49_DELETE_EXCEPTIONAL_PRIME_AFTER_FREEZE = STOP_SCOPED_CHANGES_COMMON_ENSEMBLE
V49_GENERIC_ZERO_FREE_REGION_TO_LITERAL_POWER = STOP_SCOPED_WRONG_NORM_AND_NO_SIGNED_RAMANUJAN_ATTACHMENT
V49_BFI_CRITICAL_COLLAR = SOURCE_BACKED_VIA_V45_PRIMITIVE_BLOCK_ESTIMATE
V49_FGKMT_LANDAU_PAGE = SOURCE_BACKED_EXCEPTIONAL_TYPE_AND_CARDINALITY_ONLY
V49_DRAPPEAU_FIORILLI_EXCEPTIONAL_BIAS = SOURCE_BACKED_WARNING_WRONG_FIXED_RESIDUE_FIRST_MOMENT_OBJECT
V49_BAKER_FEW_EXCEPTIONAL_MODULI = STOP_SCOPED_PAIRWISE_COPRIME_AND_DISCARDABLE_EXCEPTION_SET_WRONG_OBJECT
V49_PRODUCTS_OF_PRIMES_DENSE_MODEL = STOP_SCOPED_TERNARY_PRODUCT_AND_QUADRATIC_OBSTRUCTION_WRONG_OBJECT
V49_DIRECT_PRIMARY_SOURCE_FOR_ULTRALOW_SIGNED_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V49_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_THE_LOCAL_CENTERED_ULTRALOW_PRINCIPAL_GENERIC_EXCEPTIONAL_SIGNED_SCALAR_WITH_FIXED_POWER
V49_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U
V49_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U
V49_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V49_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_CRITICAL_CONDUCTOR_COLLAR_PAID_ULTRALOW_THREE_LANE_SCALAR_OPEN_LONG_MOBIUS_OPEN
V49_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V49_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~

## 49. V48 后的罗盘：conductor--Euler scalar splice完成，低导子 signed gate开放

V48 证明 V45 与 V46 不是两条需要 projection 对接的近似路线，而是同一个
transition scalar 的两种 exact decomposition。对 original square-free modulus
`D` 与 frequency `m`，令 `g=(m,D)`, `s=D/g`, `n=m/g`，则 exact

~~~text
e_D(m u qbar_D)=e_s(n u qbar_s),
psi(Hm/(Dq))=psi(Hn/(sq)).
~~~

把 original fibers `D=gs` 对 `g` 求和，正好给 V45 的 `lambda_s`。因此

~~~text
T_common=M_low+V_high=L_pf+R_AP,
R_AP=M_low+V_high-L_pf.
~~~

V45 high conductor为 `x^(213/128+o(1))`，V46 local Euler为
`x^(1057/640+o(1))`，故 paid splice remainder仍为
`x^(213/128+o(1))`，距 numerator endpoint余 `1/9600`。这关闭了 V47 的
splice-open，但不能把两种 energy相减：gcd aggregation 与 squaring不交换。

首选新 theorem 是最弱 scalar gate

~~~text
|M_low| << x^(1997/1200-eta_low+o(1)), eta_low>0.
~~~

一个更强、较 source-native 的充分门保留 exact prime--hybrid sign：若 low-character
physical energy满足 `W_low << x^(2-delta+o(1))` 且 `delta>1/200`，则
`|M_low|<<x^(5/3-delta/2+o(1))`。principal、全部 induced low conductors与
possible exceptional real row均留在同一 tower。现有 primary sources没有证明该
literal signed block的固定幂；arithmetic仍为 NO。

~~~text
V48_MAXIMUM_CLAIM = EXACT_GCD_REDUCTION_IDENTIFIES_V45_AND_V46_AS_TWO_DECOMPOSITIONS_OF_ONE_TRANSITION_SCALAR_AND_REPLACES_V47_FULL_CENTERED_ENERGY_BY_ONE_LOW_CONDUCTOR_SIGNED_PRIME_HYBRID_GATE_WITH_PAID_SPLICE
V48_ROUTE_ADVANCE = YES
V48_CONDITIONAL_BRIDGE_ADVANCE = YES
V48_ARITHMETIC_ADVANCE = NO
V48_FIXED_ATOM_CREDIT = 0
V48_STRICT_1_OVER_400 = UNPAID
V48_L2 = NONE
V48_TPC_207_TRIGGER = false
V48_NUMBERED_RELEASE = NO
V48_DERIVATION_STATUS = COHERENT_AFTER_EXACT_GCD_REDUCTION_SCALAR_SPLICE_LOW_PRIMITIVE_BLOCK_AND_GCD_STRATUM_ANOVA
V48_ASSUMPTION_POLICY = DIRECT_LOW_SCALAR_IS_PRIMARY_OPEN_GATE_AND_DELTA_GREATER_THAN_1_OVER_200_SIGNED_CHARACTER_ENERGY_IS_A_STRONGER_EXPLICIT_HEURISTIC_THEOREM
V48_SELECTED_RESEARCH_ROUTE = DIRECT_LOW_CONDUCTOR_SIGNED_SCALAR_FIRST__SIGNED_CHARACTER_ENERGY_SECOND__PRINCIPAL_AND_EXCEPTIONAL_ROWS_RETAINED__LONG_MOBIUS_NEXT__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE
V48_V45_COMMON_TRANSITION = RETAINED_EXACT_BEFORE_FIRST_OUTER_ABSOLUTE
V48_V46_COMMON_TRANSITION = RETAINED_EXACT_BEFORE_FIRST_OUTER_ABSOLUTE
V48_V47_ADDITIVE_ZERO_MODE = RETAINED_PROVED_EXACT_EMPTY
V48_GCD_REDUCTION = PROVED_EXACT_D_EQUALS_G_S_AND_M_EQUALS_G_N
V48_SQUAREFREE_GCD_COPRIMALITY = PROVED_EXACT_G_COPRIME_S_AND_N_COPRIME_S
V48_REDUCED_PHASE = PROVED_EXACT_E_D_M_U_QBAR_EQUALS_E_S_N_U_QBAR
V48_REDUCED_CUTOFF = PROVED_EXACT_H_M_OVER_D_Q_EQUALS_H_N_OVER_S_Q
V48_LAMBDA_AGGREGATION = PROVED_EXACT_NEGATIVE_SUM_OVER_G_OF_MU_GS_LOG_GS_OVER_GS
V48_COMMON_SCALAR_CROSSWALK = PROVED_EXACT_V45_REDUCED_OBJECT_EQUALS_V46_ORIGINAL_PROPER_FACTOR_OBJECT
V48_SCALAR_SPLICE = PROVED_EXACT_R_AP_EQUALS_M_LOW_PLUS_V_HIGH_MINUS_L_PF
V48_PAID_SPLICE_REMAINDER = DEFINED_E_SPLICE_EQUALS_V_HIGH_MINUS_L_PF
V48_V45_HIGH_CONDUCTOR_PAYMENT = RETAINED_SOURCE_BACKED_X_POWER_213_OVER_128
V48_V46_LOCAL_EULER_PAYMENT = RETAINED_SOURCE_BACKED_X_POWER_1057_OVER_640
V48_SPLICE_REMAINDER_BOUND = PROVED_X_POWER_213_OVER_128_PLUS_O1
V48_SPLICE_ENDPOINT_MARGIN = 1_OVER_9600
V48_NO_DOUBLE_COUNTING = PROVED_USE_SIGNED_SCALAR_IDENTITY_BEFORE_OUTER_ABSOLUTE
V48_ENERGY_SUBTRACTION = STOP_SCOPED_GCD_AGGREGATION_AND_SQUARING_DO_NOT_COMMUTE
V48_V45_HIGH_AS_V47_ORTHOGONAL_PROJECTION = STOP_SCOPED_FALSE_TWO_FIBER_CANCELLATION
V48_LOW_PRIMITIVE_BLOCK = PROVED_EXACT_GAUSS_RAMANUJAN_CHARACTER_FORM
V48_LOW_PHYSICAL_BLOCK = PROVED_EXACT_LAMBDA_U_PLUS_2_MINUS_B_Z_TIMES_CHIBAR_U_C_E_U_OVER_LOG_U
V48_SIGNED_PRIME_HYBRID_SPLIT = PROVED_EXACT_W_EQUALS_W_LAMBDA_MINUS_W_B
V48_LOW_PRINCIPAL_ROW = RETAINED_INSIDE_C_EQUALS_1
V48_LOW_INDUCED_ROWS = RETAINED_ALL_1_LT_C_LT_D0
V48_LOW_EXCEPTIONAL_FIREWALL = RETAIN_POSSIBLE_REAL_EXCEPTIONAL_ROW_NO_POWER_BORROWED
V48_LOW_COEFFICIENT_ENERGY = RETAINED_PROVED_P_SQUARED_X_O1
V48_LOW_COEFFICIENT_ENERGY_EXPONENT = 1_OVER_48
V48_LOW_SIGNED_PHYSICAL_ENERGY = DEFINED_CHARACTER_PARSEVAL_TOWER_W_LOW
V48_LOW_SIGNED_PHYSICAL_ENERGY_CEILING = X_POWER_2_PLUS_O1
V48_LOW_TRIVIAL_SCALAR_OUTPUT = X_POWER_5_OVER_3_PLUS_O1
V48_LOW_TRIVIAL_ENDPOINT_DEFICIT = 1_OVER_400
V48_LOW_SIGNED_CHARACTER_ENERGY_GATE = OPEN_X_POWER_2_MINUS_DELTA_WITH_DELTA_GREATER_THAN_1_OVER_200
V48_LOW_SIGNED_CHARACTER_ENERGY_THRESHOLD = DELTA_GREATER_THAN_1_OVER_200_STRICT
V48_LOW_SIGNED_CHARACTER_ENERGY_OUTPUT = CONDITIONAL_X_POWER_5_OVER_3_MINUS_DELTA_OVER_2_PLUS_O1
V48_LOW_SIGNED_CHARACTER_ENERGY_MARGIN = DELTA_OVER_2_MINUS_1_OVER_400
V48_DIRECT_LOW_SCALAR_GATE = OPEN_X_POWER_1997_OVER_1200_MINUS_ETA_LOW_WITH_ETA_LOW_POSITIVE
V48_CHARACTER_ENERGY_COMPILER = PROVED_SUFFICIENT_FOR_DIRECT_LOW_SCALAR_GATE
V48_DIRECT_SCALAR_STRENGTH = SELECTED_WEAKER_THAN_FULL_SIGNED_CHARACTER_ENERGY
V48_V47_CENTERED_GATE_TO_LOW_SCALAR = PROVED_CONDITIONAL_VIA_PAID_SPLICE
V48_LOW_SCALAR_TO_V47_RESIDUAL = PROVED_CONDITIONAL_VIA_PAID_SPLICE
V48_TRANSITION_CONDITIONAL_COMPILER = PROVED_LOW_SCALAR_GATE_PAYS_FULL_TRANSITION_WITH_HIGH_SPECTRUM_AND_CORRECTIONS
V48_TRANSITION_CONDITIONAL_MARGIN = MIN_ETA_LOW_1_OVER_9600_13_OVER_4800_817_OVER_4800
V48_GCD_STRATUM_ANOVA = PROVED_EXACT_WITHIN_NONPRINCIPAL_PLUS_BETWEEN_PRINCIPAL_ENERGY
V48_GLOBAL_CENTERING_CONSTRAINT = PROVED_ONLY_WEIGHTED_SUM_OF_STRATUM_MEANS_EQUALS_ZERO
V48_STRATUM_PRINCIPAL_SURVIVAL = PROVED_EXACT_GLOBAL_CENTERING_DOES_NOT_DELETE_EACH_STRATUM_MEAN
V48_ANOVA_VERSUS_GCD_AGGREGATION = PROVED_DISTINCT_WITHIN_D_AND_CROSS_D_OPERATIONS
V48_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U
V48_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U
V48_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V48_BFI_HIGH_CONDUCTOR = SOURCE_BACKED_RETAINED
V48_BFI_LOW_CONDUCTOR_TO_FIXED_POWER = STOP_SCOPED_SIEGEL_WALFISZ_LOG_SAVING_DOES_NOT_PAY_1_OVER_400
V48_CIS_ASYMPTOTIC_LARGE_SIEVE = STOP_SCOPED_WRONG_PHYSICAL_SIGNED_COEFFICIENT_CLASS
V48_PRODUCTS_OF_PRIMES_DENSE_MODEL = STOP_SCOPED_TERNARY_PRODUCT_AND_BURGESS_INTERFACE_WRONG_OBJECT
V48_RUNBO_LI_AP_MEAN_VALUE = STOP_SCOPED_SEPARATE_MAJORANT_MINORANT_AND_AVERAGED_RESIDUE_DO_NOT_PROVE_LITERAL_SIGNED_CHARACTER_ENERGY
V48_JOHNSTON_EFFECTIVE_BV = STOP_SCOPED_EFFECTIVITY_DOES_NOT_STRENGTHEN_TO_FIXED_POWER_LITERAL_SIGNED_GATE
V48_DIRECT_PRIMARY_SOURCE_FOR_LOW_SIGNED_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V48_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_LOW_CONDUCTOR_SIGNED_PRIME_HYBRID_CHARACTER_RAMANUJAN_ENERGY_WITH_DELTA_GREATER_THAN_1_OVER_200_OR_THE_DIRECT_LOW_SCALAR_FIXED_POWER
V48_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_HIGH_CONDUCTOR_AND_LOCAL_EULER_PAID_EXACT_SCALAR_SPLICE_DONE_LOW_CONDUCTOR_SIGNED_GATE_OPEN_LONG_MOBIUS_SPAN_OPEN
V48_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V48_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~

## 48. V47 后的罗盘：加法零频删除，首选门缩为 centered prime--hybrid covariance

V47 不改 V46 已付的 proper-factor local Euler carrier，也不改 reciprocal occupancy
energy。因为 \(0<|m|\le dq/H<d\) 且 \(q\) 在模 \(d\) 下可逆，V46 occupancy
对每个 active modulus 都有 \(A_d(0)=0\)。因此 physical residual只读取非零加法
频率。令

\[
\mathcal R_d^\circ(a)=\mathcal R_d(a)-\frac1d\sum_{b\bmod d}\mathcal R_d(b),
\]

则 exact

\[
\mathfrak R_x^{\rm AP}=-H\sum_d\sum_{r\ne0}
A_d(r)\widehat{\mathcal R_d^\circ}(r),\qquad
\sum_{r\ne0}|\widehat{\mathcal R}_d(r)|^2
=d\sum_a|\mathcal R_d^\circ(a)|^2.
\]

这只删除 additive constant direction；multiplicative principal、induced low
conductor、exceptional real row及 nonunit frequencies都仍在。

把 V46 local profile拆成 prime error与 hybrid error后又有 exact

\[
\mathcal R_d^\circ=\mathcal P_d^\circ-\mathcal H_d^\circ.
\]

首选新定理因此严格缩成

\[
\sum_{Y_0<d\le U}d\sum_{a\bmod d}
|\mathcal P_d^\circ(a)-\mathcal H_d^\circ(a)|^2
\ll xU^2x^{\rho+o(1)},\qquad 0\le\rho<33/100.
\]

payoff仍为 numerator \(x^{1799/1200+\rho/2+o(1)}\)，margin为
\(33/200-\rho/2\)。`rho=0` 是明确标注的 natural-scale conjecture，不是现有
source theorem。路线按优先级分为三车道：signed centered covariance；分别控制
prime/hybrid marginals的更强 fallback；以及需要 projection splice才能接回的 V45
high-conductor atlas。现有 Hooley、sparse-modulus、most-moduli与 sifted-restriction
sources都不直接覆盖 literal gate。

~~~text
V47_MAXIMUM_CLAIM = EXACT_ADDITIVE_ZERO_MODE_EXCISION_STRICTLY_REDUCES_V46_ALL_RESIDUE_AP_BDH_TO_ONE_CENTERED_SIGNED_PRIME_HYBRID_COVARIANCE_GATE_AND_RANKS_TWO_EXPLICIT_FALLBACK_LANES
V47_ROUTE_ADVANCE = YES
V47_CONDITIONAL_BRIDGE_ADVANCE = YES
V47_ARITHMETIC_ADVANCE = NO
V47_FIXED_ATOM_CREDIT = 0
V47_STRICT_1_OVER_400 = UNPAID
V47_L2 = NONE
V47_TPC_207_TRIGGER = false
V47_NUMBERED_RELEASE = NO
V47_DERIVATION_STATUS = COHERENT_AFTER_EXACT_ADDITIVE_ZERO_MODE_EXCISION_CENTERED_PARSEVAL_AND_PRIME_HYBRID_LOCAL_ERROR_SPLIT
V47_ASSUMPTION_POLICY = CENTERED_SIGNED_COVARIANCE_IS_OPEN_AND_NATURAL_SCALE_RHO_ZERO_IS_EXPLICITLY_CONJECTURAL
V47_SELECTED_RESEARCH_ROUTE = CENTERED_SIGNED_PRIME_HYBRID_COVARIANCE_FIRST__SEPARATE_MARGINALS_SECOND__V45_CONDUCTOR_ATLAS_INDEPENDENT_FALLBACK__LONG_MOBIUS_NEXT__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE
V47_V46_LOCAL_EULER_PAYMENT = RETAINED_SOURCE_BACKED_NORMALIZED_X_POWER_1891_OVER_1920
V47_V46_LOCAL_ENDPOINT_MARGIN = RETAINED_121_OVER_9600
V47_V46_RECIPROCAL_OCCUPANCY_ENERGY = RETAINED_PROVED_P_SQUARED_X_O1
V47_ADDITIVE_ZERO_MODE_SUPPORT = PROVED_EXACT_A_D_ZERO_EQUALS_ZERO
V47_ADDITIVE_ZERO_MODE_REASON = PROVED_ZERO_LT_ABS_M_LT_D_AND_Q_INVERTIBLE_MOD_D
V47_NONZERO_FREQUENCY_PAIRING = PROVED_EXACT_BEFORE_OUTER_ABSOLUTE
V47_CENTERED_RESIDUAL = DEFINED_R_D_CIRCLE_EQUALS_R_D_MINUS_RESIDUE_AVERAGE
V47_CENTERED_PARSEVAL = PROVED_EXACT_NONZERO_FOURIER_ENERGY_EQUALS_D_TIMES_CENTERED_RESIDUE_ENERGY
V47_CONSTANT_RESIDUE_SHIFT_INVARIANCE = PROVED_EXACT_FOR_PHYSICAL_PAIRING
V47_ZERO_MODE_SCOPE_FIREWALL = ADDITIVE_CONSTANT_ONLY_DOES_NOT_DELETE_MULTIPLICATIVE_PRINCIPAL_LOW_CONDUCTOR_EXCEPTIONAL_OR_NONUNIT_MODES
V47_CENTERED_GATE_STRENGTH = STRICTLY_WEAKER_THAN_V46_FULL_ENERGY_IN_AMBIENT_SPACE_AND_SUFFICIENT_FOR_THE_LITERAL_PAIRING
V47_LITERAL_FAMILY_STRICTNESS = NOT_CLAIMED_BY_FINITE_AMBIENT_FIXTURE
V47_SHIFTED_PRIME_LOCAL_ERROR = DEFINED_LAMBDA_U_PLUS_2_MINUS_P_D_A_OVER_LOG_U
V47_HYBRID_LOCAL_ERROR = DEFINED_B_Z_U_MINUS_B_D_Z_A_OVER_LOG_U
V47_SIGNED_LOCAL_ERROR_SPLIT = PROVED_EXACT_R_D_EQUALS_P_D_ERROR_MINUS_H_D_ERROR
V47_CENTERED_SIGNED_SPLIT = PROVED_EXACT_R_D_CIRCLE_EQUALS_P_D_CIRCLE_MINUS_H_D_CIRCLE
V47_PRIME_HYBRID_COVARIANCE_IDENTITY = PROVED_EXACT_E_R_EQUALS_E_P_PLUS_E_H_MINUS_TWO_REAL_COVARIANCE
V47_CENTERED_COVARIANCE_ENERGY = DEFINED_SUM_D_D_SUM_A_ABS_R_D_CIRCLE_SQUARED
V47_CENTERED_COVARIANCE_NATURAL_SCALE = X_TIMES_U_SQUARED_EQUALS_X_POWER_333_OVER_200
V47_CENTERED_COVARIANCE_GATE = OPEN_X_U_SQUARED_X_POWER_RHO_WITH_ZERO_LE_RHO_LT_33_OVER_100
V47_CENTERED_COVARIANCE_BENCHMARK = CONJECTURAL_RHO_EQUALS_ZERO
V47_CENTERED_RESIDUAL_NUMERATOR_OUTPUT = CONDITIONAL_X_POWER_1799_OVER_1200_PLUS_RHO_OVER_2_PLUS_O1
V47_CENTERED_RESIDUAL_NORMALIZED_OUTPUT = CONDITIONAL_X_POWER_333_OVER_400_PLUS_RHO_OVER_2_PLUS_O1
V47_CENTERED_RESIDUAL_MARGIN = 33_OVER_200_MINUS_RHO_OVER_2
V47_TRANSITION_CONDITIONAL_COMPILER = PROVED_CENTERED_COVARIANCE_GATE_PAYS_FULL_TRANSITION_WITH_V46_LOCAL_AND_V44_CORRECTIONS
V47_TRANSITION_CONDITIONAL_MARGIN = MIN_121_OVER_9600_33_OVER_200_MINUS_RHO_OVER_2_13_OVER_4800_817_OVER_4800
V47_SEPARATE_PRIME_VARIANCE = OPEN_HEURISTIC_HOOLEY_PROFILE_WRONG_LITERAL_SOURCE_INTERFACE
V47_SEPARATE_HYBRID_VARIANCE = OPEN_NEW_SIEVE_AP_VARIANCE_THEOREM
V47_SEPARATE_MARGINAL_COMPILER = PROVED_SUFFICIENT_BY_CENTERED_L2_TRIANGLE
V47_SEPARATE_MARGINAL_STRENGTH = STRICTLY_STRONGER_IN_FINITE_AMBIENT_SPACE_NOT_CLAIMED_FOR_LITERAL_FAMILY
V47_CLASSICAL_MAIN_MESH = OPTIONAL_PROVED_U_CUBED_X_O1
V47_CLASSICAL_MAIN_MESH_EXPONENT = 399_OVER_400
V47_EXACT_LOCAL_PROFILE_PREFERENCE = SELECTED_NO_MESH_AND_NO_LOG_DENOMINATOR_REPLACEMENT
V47_V45_HIGH_CONDUCTOR_PAYMENT = RETAINED_INDEPENDENT_SOURCE_BACKED_X_POWER_213_OVER_128
V47_V45_TO_CENTERED_SPLICE = OPEN_EXACT_PROJECTION_COMPILER_NO_DOUBLE_COUNTING
V47_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U
V47_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U
V47_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V47_FIORILLI_HOOLEY_VARIANCE = HEURISTIC_SUPPORT_ONLY_NO_UNIFORM_LITERAL_THEOREM_BELOW_SQUARE_ROOT
V47_BAKER_FREIBERG_DIRECT_ATTACHMENT = STOP_SCOPED_SPARSE_MODULUS_SEQUENCE_NOT_COMPLETE_SQUAREFREE_TRANSITION_FAMILY
V47_KOUKOULOPOULOS_DIRECT_ATTACHMENT = STOP_SCOPED_MOST_MODULI_AND_INTERVAL_ORIGINS_NOT_ONE_FIXED_COMPLETE_LITERAL_FAMILY
V47_SIFTED_RESTRICTION_DIRECT_ATTACHMENT = STOP_SCOPED_WRONG_NORM_AND_NO_LITERAL_B_Z_CENTERED_AP_COVARIANCE
V47_CLASSICAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_RANGE_AND_MODULUS_DEPENDENT_PROFILE_MISMATCH_RETAINED_FROM_V46
V47_DIRECT_PRIMARY_SOURCE_FOR_CENTERED_COVARIANCE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V47_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_NATURAL_SCALE_CENTERED_SIGNED_PRIME_HYBRID_AP_COVARIANCE_UNIFORMLY_FOR_X_POWER_31_OVER_96_LT_D_LE_X_POWER_133_OVER_400
V47_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_LOCAL_EULER_PAID_ADDITIVE_ZERO_MODE_DELETED_CENTERED_PRIME_HYBRID_COVARIANCE_OPEN_LONG_MOBIUS_SPAN_OPEN
V47_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V47_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~

## 47. V46 后的罗盘：proper-factor local Euler 已付，AP--BDH whole-object 门开放

V46 在 V43/V44 的 common transition scalar 内、第一道 outer absolute 之前，以
proper-factor modulus \(d\) 的 local shifted-prime/hybrid profile
\(\Delta_{d,z}=P_d-B_{d,z}\) 做精确拆分。由 \(d\mid t\) 得
\(\Delta_{d,z}(u-t)=\Delta_{d,z}(u)\)，且 \(\Delta_{d,z}(0)=0\)。

local component沿 V29 reduced-radical Bettin--Chandee compiler得到

\[
 |\mathfrak L_x^{\rm pf}|/L_{\rm pr}
 \ll x^{1891/1920+o(1)},\qquad
 |\mathfrak L_x^{\rm pf}|\ll x^{1057/640+o(1)},
\]

endpoint margin为 \(121/9600\)。剩余 physical object被统一写成

\[
 \mathcal E_{\rm AP}^{\rm tr}
 =\sum_{Y_0<d\le U}d\sum_{a\bmod d}|\mathcal R_d(a)|^2.
\]

V46 初等证明 reciprocal occupancy energy为
\(P^2x^{o(1)}=x^{1/48+o(1)}\)。若

\[
 \mathcal E_{\rm AP}^{\rm tr}\ll xU^2x^{\rho+o(1)},
 \qquad 0\le\rho<33/100,
\]

则 residual numerator为 \(x^{1799/1200+\rho/2+o(1)}\)，完整 transition
条件闭合。现有 BDH/general-sequence/multiplicative-function theorem都没有覆盖
\(x^{31/96}<d\le x^{133/400}\) 上随 \(d\) 变化的 literal shifted-prime minus
hybrid residual。因此地图位置是 route-level GO、arithmetic NO：

~~~text
proper-factor local Euler carrier                PAID
all-residue transition AP--BDH energy            OPEN NEW THEOREM
balanced / reverse-Type-I long-Mobius            OPEN
V42 positive-Gram Gate B                         OPEN IN PARALLEL
V43 A+B zero-axis reassembly                     EXACT COMPILER
distinguished-seed dynamics                      RESERVE
~~~

Canonical registry：

~~~text
V46_MAXIMUM_CLAIM = EXACT_PROPER_FACTOR_LOCAL_PROFILE_SPLIT_PAYS_THE_TRANSITION_NATIVE_EULER_CARRIER_AND_REPLACES_THE_V45_LOW_CONDUCTOR_MAJOR_BY_ONE_LITERAL_ALL_RESIDUE_AP_BDH_ENERGY_GATE
V46_ROUTE_ADVANCE = YES
V46_CONDITIONAL_BRIDGE_ADVANCE = YES
V46_ARITHMETIC_ADVANCE = NO
V46_FIXED_ATOM_CREDIT = 0
V46_STRICT_1_OVER_400 = UNPAID
V46_L2 = NONE
V46_TPC_207_TRIGGER = false
V46_NUMBERED_RELEASE = NO
V46_DERIVATION_STATUS = COHERENT_AFTER_EXACT_PROPER_FACTOR_EULER_SPLIT_RECIPROCAL_OCCUPANCY_ENERGY_AND_AP_PARSEVAL_COMPILER
V46_ASSUMPTION_POLICY = ONE_LITERAL_TRANSITION_AP_BDH_ENERGY_REMAINS_OPEN_AND_IS_NOT_CALLED_AN_EQUIVALENT_OR_WEAKEST_REFORMULATION
V46_SELECTED_RESEARCH_ROUTE = TRANSITION_NATIVE_EULER_PAID__ALL_RESIDUE_AP_BDH_NEXT__LONG_MOBIUS_SECOND__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE
V46_V43_TRANSITION_ALIAS = RETAINED_EXACT_PROPER_FACTOR_POISSON_SCALAR_BEFORE_OUTER_ABSOLUTE
V46_V44_CORRECTION_LEDGER = RETAINED_Q_DIVIDES_U_AND_CENTERED_BACKGROUND_PAID
V46_V45_HIGH_CONDUCTOR_PAYMENT = RETAINED_INDEPENDENT_SOURCE_BACKED_X_POWER_213_OVER_128
V46_PROPER_FACTOR_SQUAREFREE = PROVED_EXACT_FROM_MU_D_NONZERO
V46_SHIFTED_PRIME_LOCAL_PROFILE = PROVED_EXACT_PRODUCT_OF_F_P
V46_HYBRID_LOCAL_PROFILE = PROVED_EXACT_PRODUCT_OF_G_P_Z
V46_LOCAL_PROFILE_DIFFERENCE = DELTA_D_Z_EQUALS_P_D_MINUS_B_D_Z
V46_LOCAL_PROFILE_ZERO_AXIS = PROVED_DELTA_D_Z_ZERO_EQUALS_ZERO
V46_LOCAL_PROFILE_ZERO_MEAN = PROVED_SUM_A_MOD_D_DELTA_D_Z_A_EQUALS_ZERO
V46_PROPER_FACTOR_CONGRUENCE = PROVED_D_DIVIDES_T_IMPLIES_DELTA_D_Z_U_MINUS_T_EQUALS_DELTA_D_Z_U
V46_COMMON_TRANSITION_SPLIT = PROVED_EXACT_LOCAL_PLUS_AP_RESIDUAL_BEFORE_OUTER_ABSOLUTE
V46_TRANSITION_NATIVE_CARRIER = PROVED_EXACT_WITH_LOG_T_PLUS_H_DENOMINATOR
V46_TRANSITION_NATIVE_CARRIER_ZERO_AXIS = PROVED_EXACT_ZERO
V46_LOCAL_RADICAL_ACTIVE_RANGE = PROVED_R_GE_H_OVER_Q_EQUALS_X_POWER_31_OVER_96
V46_LOCAL_P_BRANCH = PROVED_EXACT_MU_R_OVER_PHI_R_TIMES_E_R_2_A_QBAR
V46_LOCAL_B_BRANCH = PROVED_EXACT_MU_R0_OVER_PHI_R0_PHI_R1_SQUARED_TIMES_E_R0_2_A_QR1_BAR
V46_LOCAL_COEFFICIENT_L2_P_BRANCH = PROVED_X_OVER_S_POWER_3_OVER_2
V46_LOCAL_COEFFICIENT_L2_B_BRANCH = PROVED_X_OVER_S_POWER_3_OVER_2_R1_CUBED
V46_LOCAL_BETTIN_CHANDEE_ATTACHMENT = SOURCE_BACKED_BY_V29_COMPILER_WITH_PROPER_FACTOR_AS_SELECTED_GROUP
V46_LOCAL_NORMALIZED_OUTPUT = PROVED_X_POWER_1891_OVER_1920_PLUS_O1
V46_LOCAL_NUMERATOR_OUTPUT = PROVED_X_POWER_1057_OVER_640_PLUS_O1
V46_LOCAL_ENDPOINT_MARGIN = 121_OVER_9600
V46_AP_RESIDUAL = PROVED_EXACT_W_MINUS_DELTA_D_Z_OVER_LOG_U_IN_EACH_RESIDUE_CLASS
V46_AP_PARSEVAL = PROVED_EXACT_SUM_R_FOURIER_SQUARED_EQUALS_D_SUM_A_RESIDUAL_SQUARED
V46_RECIPROCAL_OCCUPANCY = PROVED_EXACT_A_D_R_WITH_M_QBAR_MOD_D
V46_RECIPROCAL_COLLISION = PROVED_M1_Q2_MINUS_M2_Q1_EQUALS_ELL_D_WITH_ABS_ELL_LE_P_X_O1
V46_RECIPROCAL_OCCUPANCY_ENERGY = PROVED_ELEMENTARY_P_SQUARED_X_O1
V46_RECIPROCAL_OCCUPANCY_ENERGY_EXPONENT = 1_OVER_48
V46_TRANSITION_AP_BDH_ENERGY = DEFINED_SUM_D_SUM_A_D_TIMES_ABS_RESIDUAL_SQUARED
V46_TRANSITION_AP_BDH_NATURAL_SCALE = X_TIMES_U_SQUARED_EQUALS_X_POWER_333_OVER_200
V46_TRANSITION_AP_BDH_GATE = OPEN_X_U_SQUARED_X_POWER_RHO_WITH_ZERO_LE_RHO_LT_33_OVER_100
V46_AP_RESIDUAL_NUMERATOR_OUTPUT = CONDITIONAL_X_POWER_1799_OVER_1200_PLUS_RHO_OVER_2_PLUS_O1
V46_AP_RESIDUAL_NORMALIZED_OUTPUT = CONDITIONAL_X_POWER_333_OVER_400_PLUS_RHO_OVER_2_PLUS_O1
V46_AP_RESIDUAL_MARGIN = 33_OVER_200_MINUS_RHO_OVER_2
V46_TRANSITION_CONDITIONAL_COMPILER = PROVED_AP_BDH_GATE_PAYS_FULL_TRANSITION_WITH_LOCAL_AND_V44_CORRECTIONS
V46_TRANSITION_CONDITIONAL_MARGIN = MIN_121_OVER_9600_33_OVER_200_MINUS_RHO_OVER_2_13_OVER_4800_817_OVER_4800
V46_AP_GATE_STRENGTH = SUFFICIENT_WHOLE_OBJECT_THEOREM_STRONGER_THAN_ONLY_V45_LOW_CONDUCTOR_GATE
V46_LOW_EXCEPTIONAL_CHARACTER_FIREWALL = RETAINED_INSIDE_AP_RESIDUAL_NO_LANDAU_PAGE_POWER_BORROWED
V46_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U
V46_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U
V46_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V46_BETTIN_CHANDEE_LOCAL_ATTACHMENT = SOURCE_BACKED_TRANSITION_NATIVE_EULER_COMPONENT_ONLY
V46_CLASSICAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_REQUIRES_MODULUS_SCALE_X_LOG_POWER_MINUS_A_NOT_U_X_POWER_133_OVER_400
V46_HARPER_GENERAL_SEQUENCE_DIRECT_ATTACHMENT = STOP_SCOPED_REQUIRES_Q_GREATER_THAN_SQRT_2X_AND_MODULUS_INDEPENDENT_SEQUENCE_HYPOTHESES
V46_KMT_MULTIPLICATIVE_AP_DIRECT_ATTACHMENT = STOP_SCOPED_BOUNDED_MULTIPLICATIVE_ALMOST_ALL_MODULI_NOT_SHIFTED_LAMBDA_MINUS_D_DEPENDENT_HYBRID_PROFILE
V46_FIORILLI_HOOLEY_VARIANCE = HEURISTIC_SUPPORT_ONLY_NO_UNIFORM_LITERAL_THEOREM_BELOW_SQUARE_ROOT
V46_DIRECT_PRIMARY_SOURCE_FOR_AP_BDH_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10
V46_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_THE_NATURAL_SCALE_ALL_RESIDUE_AP_VARIANCE_FOR_LAMBDA_U_PLUS_2_MINUS_B_Z_U_MINUS_THE_PROPER_FACTOR_LOCAL_PROFILE_UNIFORMLY_FOR_X_POWER_31_OVER_96_LT_D_LE_X_POWER_133_OVER_400
V46_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_TRANSITION_LOCAL_EULER_PAID_AP_BDH_RESIDUAL_OPEN_LONG_MOBIUS_SPAN_OPEN
V46_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V46_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~

## 46. V45 后的罗盘：高导子谱已付，只剩低导子结构化 major

V45 对 V44 reciprocal variance 做 primitive-conductor audit。V44 把 imprimitive
characters 的 induction 一概记成 `x^o(1)`，这对 aggregate ceiling 足够，但不能用来
寻找 endpoint power：同一小导子 character会被诱导到许多 reduced moduli `s`。

令 `P=Q^2/H=x^(1/96)`、`D0=P^(1/2)=x^(1/192)`。若 conductor `d~D`、
`s~S`、`N~SQ/H`，correct induced weight 与 primitive large sieve 给

\[
\mathcal V_D^{(2)}\ll P^2(D/Q+1/D)x^{o(1)},
\]

\[
\mathcal V_D^{(4)}\ll
\begin{cases}P^2/N,&D>N,\\P^2/D,&D\le N.
\end{cases}
\]

在 `D>=D0` 上逐块取两界最小值，得到

\[
\mathcal V_{\ge D_0}\ll P^{3/2}x^{o(1)},\qquad
|\mathfrak V_{\ge D_0}^{\rm tr}|\ll x^{213/128+o(1)}.
\]

后者比 strict transition endpoint 留精确 `1/9600` margin，因而 high-conductor
spectrum 已 source-backed 支付。

低谱不能删除。对 `s=de` 上由 primitive `chi* mod d` 诱导的 character，physical
transform 精确为

\[
\tau(\chi^*)\chi^*(e)
\sum_u b(u)\overline{\chi^*(u)}c_e(u),
\]

且 `mu(e)c_e(u)=mu((e,u))phi((e,u))`。所以 principal `d=1` 与
`1<d<D0` 共同构成一个 Gauss--Ramanujan/Euler structured major spectrum。
transition 从 V44 的“两门”缩成唯一一门

\[
|\mathfrak M_{<D_0}^{\rm tr}|
\ll x^{1997/1200-\eta_<+o(1)},\qquad\eta_<>0.
\]

BFI 的 low-conductor Siegel--Walfisz lane只有 log saving；现有 asymptotic large
sieve 与 products-of-primes dense model也不接受这条 literal physical polynomial。
因此 arithmetic advance仍为 `NO`。下一段主跨是 low structured major，然后才是
balanced/reverse-Type-I long-Möbius；V42 Gate B 平行，V43 继续做最终 A+B AND
reassembly。

~~~text
V45_MAXIMUM_CLAIM = EXACT_CONDUCTOR_STRATIFICATION_REPLACES_THE_V44_CENTERED_VARIANCE_GATE_BY_A_SOURCE_BACKED_HIGH_CONDUCTOR_PAYMENT_AND_ONE_STRUCTURED_LOW_CONDUCTOR_MAJOR_SPECTRUM_GATE
V45_ROUTE_ADVANCE = YES
V45_CONDITIONAL_BRIDGE_ADVANCE = YES
V45_ARITHMETIC_ADVANCE = NO
V45_FIXED_ATOM_CREDIT = 0
V45_STRICT_1_OVER_400 = UNPAID
V45_L2 = NONE
V45_TPC_207_TRIGGER = false
V45_NUMBERED_RELEASE = NO
V45_DERIVATION_STATUS = COHERENT_AFTER_EXACT_CONDUCTOR_SPLIT_GAUSS_RAMANUJAN_RETYPE_AND_HIGH_CONDUCTOR_PAYMENT
V45_ASSUMPTION_POLICY = ONLY_THE_PRINCIPAL_PLUS_LOW_CONDUCTOR_STRUCTURED_MAJOR_SPECTRUM_REMAINS_OPEN_IN_THE_TRANSITION_WINDOW
V45_SELECTED_RESEARCH_ROUTE = LOW_CONDUCTOR_STRUCTURED_MAJOR_FIRST__BALANCED_AND_REVERSE_TYPE_I_SECOND__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE
V45_V44_COMMON_TRANSITION = RETAINED_EXACT_BEFORE_FIRST_OUTER_ABSOLUTE
V45_V44_IMPRIMITIVE_X_O1_SHORTCUT = RETYPED_AS_FALSE_UNIFORM_LEDGER_FOR_LOW_CONDUCTORS
V45_SQUAREFREE_REDUCED_MODULUS = PROVED_EXACT_FROM_LAMBDA_S_SUPPORT
V45_CHARACTER_INVERSION = PROVED_EXACT_ALL_CHARACTERS_BEFORE_OUTER_ABSOLUTE
V45_CONDUCTOR_SPLIT = PROVED_EXACT_AT_D0_EQUALS_P_POWER_1_OVER_2
V45_CONDUCTOR_THRESHOLD = D0_EQUALS_P_POWER_1_OVER_2_EQUALS_X_POWER_1_OVER_192
V45_PRINCIPAL_MODE_LOCATION = PROVED_EXACT_INSIDE_LOW_CONDUCTOR_SPECTRUM_D_EQUALS_1
V45_LOW_NONPRINCIPAL_TOWER = PROVED_EXACT_INDUCED_PRIMITIVE_CONDUCTORS_1_LT_D_LT_D0
V45_HIGH_SPECTRUM = PROVED_EXACT_PRIMITIVE_CONDUCTORS_D_GE_D0
V45_GAUSS_RAMANUJAN_TRANSFORM = PROVED_EXACT_TAU_CHI_TIMES_CHI_E_TIMES_PHYSICAL_CHIBAR_U_C_E_U
V45_GAUSS_RAMANUJAN_PHASE = PROVED_CHI_STAR_E_NOT_ITS_CONJUGATE
V45_RAMANUJAN_LOCAL_DENSITY = PROVED_MU_E_C_E_U_EQUALS_MU_GCD_TIMES_PHI_GCD
V45_RECIPROCAL_COLLISION = PROVED_N1_Q2_MINUS_N2_Q1_EQUALS_ELL_S_WITH_ABS_ELL_LE_P_X_O1
V45_DYADIC_SHORT_LENGTH = N_ASYMPTOTIC_S_Q_OVER_H
V45_INDUCED_EXTENSION_WEIGHT = PROVED_X_O1_OVER_D_S_SQUARED
V45_PRIMITIVE_SECOND_MOMENT = SOURCE_BACKED_P_SQUARED_TIMES_D_OVER_Q_PLUS_1_OVER_D
V45_PRIMITIVE_FOURTH_MOMENT_D_GT_N = SOURCE_BACKED_P_SQUARED_OVER_N
V45_PRIMITIVE_FOURTH_MOMENT_D_LE_N = SOURCE_BACKED_P_SQUARED_OVER_D
V45_HIGH_CONDUCTOR_LOW_D_REGION = PROVED_SECOND_MOMENT_LE_P_POWER_3_OVER_2
V45_HIGH_CONDUCTOR_HIGH_D_REGION = PROVED_FOURTH_MOMENT_LE_P_POWER_3_OVER_2
V45_HIGH_CONDUCTOR_VARIANCE = PROVED_SOURCE_BACKED_P_POWER_3_OVER_2_X_O1
V45_HIGH_CONDUCTOR_VARIANCE_EXPONENT = 1_OVER_64
V45_HIGH_CONDUCTOR_OUTPUT = PROVED_X_POWER_213_OVER_128_PLUS_O1
V45_HIGH_CONDUCTOR_ENDPOINT_MARGIN = 1_OVER_9600
V45_LOW_STRUCTURED_ABSOLUTE_CEILING = X_POWER_5_OVER_3_PLUS_O1
V45_LOW_STRUCTURED_MAJOR_GATE = OPEN_X_POWER_1997_OVER_1200_MINUS_ETA_LOW_WITH_ETA_LOW_POSITIVE
V45_TRANSITION_CONDITIONAL_COMPILER = PROVED_LOW_STRUCTURED_GATE_PAYS_FULL_TRANSITION_WITH_HIGH_SPECTRUM_AND_CORRECTIONS
V45_TRANSITION_CONDITIONAL_MARGIN = MIN_ETA_LOW_1_OVER_9600_13_OVER_4800_817_OVER_4800
V45_PHYSICAL_Q_DIVIDES_U_CORRECTION = RETAINED_PAID_X_POWER_319_OVER_192_PLUS_O1
V45_BACKGROUND_OUTPUT = RETAINED_PAID_X_POWER_7171_OVER_4800_PLUS_O1
V45_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U
V45_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U
V45_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V45_BFI_PRIMITIVE_LARGE_SIEVE = SOURCE_BACKED_HIGH_CONDUCTOR_SECOND_AND_FOURTH_MOMENTS
V45_BFI_INDUCED_CHARACTER_SPLIT = SOURCE_BACKED_ARCHITECTURE_LOW_SIEGEL_WALFISZ_HIGH_LARGE_SIEVE
V45_BFI_LOW_CONDUCTOR_TO_FIXED_POWER = STOP_SCOPED_LOG_SAVING_DOES_NOT_PAY_1_OVER_400
V45_CIS_ASYMPTOTIC_LARGE_SIEVE_DIRECT_ATTACHMENT = STOP_SCOPED_PRIMITIVE_ASYMPTOTIC_FORM_DOES_NOT_IDENTIFY_LITERAL_PHYSICAL_LOW_SPECTRUM
V45_PRODUCTS_OF_PRIMES_DENSE_MODEL_DIRECT_ATTACHMENT = STOP_SCOPED_TERNARY_PRODUCT_AND_BURGESS_LENGTH_WRONG_PHYSICAL_OBJECT
V45_LOW_EXCEPTIONAL_CHARACTER_FIREWALL = RETAIN_STRUCTURED_MODE_NO_UNIFORM_POWER_BORROWED
V45_DIRECT_PRIMARY_SOURCE_FOR_LOW_STRUCTURED_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10
V45_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_THE_PRINCIPAL_PLUS_LOW_CONDUCTOR_INDUCED_CHARACTER_GAUSS_RAMANUJAN_SPECTRUM_WITH_PHYSICAL_LAMBDA_MINUS_B_AT_THE_STRICT_TRANSITION_POWER
V45_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_TRANSITION_HIGH_CONDUCTOR_PAID_LOW_STRUCTURED_MAJOR_OPEN_LONG_MOBIUS_SPAN_OPEN
V45_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V45_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~

## 45. V44 后的罗盘：transition 已拆成 principal mean 与 reciprocal variance

V44 选择 V43 三个 open windows 中最短、最有结构的 transition
`H/(4Q)<d<=U`。对 `(m,d)` 作 exact gcd reduction

\[
d=gs,\qquad m=gn,qquad e_d(mu\bar q)=e_s(nu\bar q),
\]

把 reduced modulus 收缩到

\[
Q^{31/32+o(1)}\le s\le Q^{399/400+o(1)},qquad
0<|n|\le x^{23/2400+o(1)}.
\]

短 numerator 与 prime inverse 的 occupancy `C_s(r)` 在 unit residues 上作
mean--centered split；principal character 精确成为 Ramanujan mean，nonprincipal
characters 精确成为 reciprocal-ratio variance。两个 generic ceiling 都给
`x^(5/3+o(1))`，比 strict numerator endpoint 差恰好 `1/400`，所以不能靠改名、
log saving 或 generic large sieve 过桥。

现在 transition 的大胆但清楚的 theorem pair 是：

1. `V44_RECIPROCAL_VARIANCE_GATE`：相对 generic `P^2` 赢
   `x^(-kappa)`，`kappa>1/200`；
2. `V44_PRINCIPAL_MEAN_GATE`：Ramanujan/AP mean 从 `x^(5/3)` 赢
   `x^(-delta_M)`，`delta_M>1/400`。

physical `q|u` correction 已付到 `319/192`，background 已付到
`7171/4800`。两门一旦同时成立，完整 transition window 在一个 outer absolute
下闭合。之后才进入 balanced 与 reverse-Type-I long-Möbius span；V42 positive-Gram
Gate B 仍平行施工，V43 zero-axis transference 仍负责最终 A+B AND reassembly。

~~~text
V44_MAXIMUM_CLAIM = EXACT_TRANSITION_GCD_REDUCTION_SPLITS_THE_PRIMARY_ALIAS_INTO_PRINCIPAL_RAMANUJAN_MEAN_CENTERED_RECIPROCAL_VARIANCE_PAID_UNIT_CORRECTION_AND_PAID_BACKGROUND_WITH_THE_STRICT_ENDPOINT_CLOCK
V44_ROUTE_ADVANCE = YES
V44_CONDITIONAL_BRIDGE_ADVANCE = YES
V44_ARITHMETIC_ADVANCE = NO
V44_FIXED_ATOM_CREDIT = 0
V44_STRICT_1_OVER_400 = UNPAID
V44_L2 = NONE
V44_TPC_207_TRIGGER = false
V44_NUMBERED_RELEASE = NO
V44_DERIVATION_STATUS = COHERENT_AFTER_TRANSITION_EXTRACTION_GCD_REDUCTION_MEAN_VARIANCE_SPLIT_AND_TWO_CORRECTION_PAYMENTS
V44_ASSUMPTION_POLICY = PRINCIPAL_MEAN_AND_RECIPROCAL_VARIANCE_REMAIN_TWO_EXPLICIT_OPEN_ENDPOINT_THEOREMS
V44_SELECTED_RESEARCH_ROUTE = TRANSITION_MEAN_AND_VARIANCE_FIRST__BALANCED_AND_REVERSE_TYPE_I_SECOND__V42_GATE_B_PARALLEL__V43_A_B_JOIN__C_RESERVE
V44_V43_TRANSITION_ALIAS = RETAINED_EXACT_BEFORE_FIRST_OUTER_ABSOLUTE
V44_Q_NONUNIT_IN_D = ABSENT_EXACT_BECAUSE_D_LE_U_LT_Q
V44_Q_NONUNIT_IN_M = ABSENT_EXACT_BECAUSE_ABS_M_LE_2UQ_OVER_H_LT_Q
V44_GCD_REDUCTION = PROVED_EXACT_D_EQUALS_GS_M_EQUALS_GN
V44_GCD_PHASE_CANCELLATION = PROVED_E_D_MU_QBAR_EQUALS_E_S_NU_QBAR
V44_GCD_CUTOFF_CANCELLATION = PROVED_PSI_HM_OVER_DQ_EQUALS_PSI_HN_OVER_SQ
V44_REDUCED_MODULUS_RANGE = Q_POWER_31_OVER_32_TO_Q_POWER_399_OVER_400
V44_REDUCED_DUAL_LENGTH = X_POWER_23_OVER_2400_PLUS_O1
V44_LAMBDA_S_ENVELOPE = X_O1_OVER_S
V44_RECIPROCAL_OCCUPANCY = PROVED_EXACT_R_EQUALS_N_Q_INVERSE_MOD_S
V44_MEAN_CENTERED_SPLIT = PROVED_EXACT_BEFORE_OUTER_ABSOLUTE
V44_PRINCIPAL_TERM = PROVED_EXACT_RAMANUJAN_SUM_PAIRING
V44_CENTERED_CHARACTER_PARSEVAL = PROVED_EXACT_NONPRINCIPAL_CHARACTER_ENERGY
V44_RECIPROCAL_VARIANCE_GENERIC = PROVED_LARGE_SIEVE_P_SQUARED_X_O1
V44_RECIPROCAL_VARIANCE_GENERIC_EXPONENT = 1_OVER_48
V44_CENTERED_GENERIC_OUTPUT = X_POWER_5_OVER_3_PLUS_O1
V44_CENTERED_GENERIC_ENDPOINT_DEFICIT = 1_OVER_400
V44_RECIPROCAL_VARIANCE_GATE = OPEN_P_SQUARED_X_MINUS_KAPPA_WITH_KAPPA_GREATER_THAN_1_OVER_200
V44_RECIPROCAL_VARIANCE_IDEAL = P_X_O1
V44_RECIPROCAL_VARIANCE_IDEAL_OUTPUT = X_POWER_319_OVER_192_PLUS_O1
V44_RECIPROCAL_VARIANCE_IDEAL_MARGIN = 13_OVER_4800
V44_PHYSICAL_Q_DIVIDES_U_CORRECTION = PROVED_ADDITIVE_LARGE_SIEVE_X_POWER_319_OVER_192_PLUS_O1
V44_BACKGROUND_Q_RETENTION = PROVED_EXACT_REDUCED_DENOMINATOR_STILL_CONTAINS_Q
V44_BACKGROUND_COEFFICIENT_ENERGY = H_INVERSE_X_O1
V44_BACKGROUND_OUTPUT = PROVED_X_POWER_7171_OVER_4800_PLUS_O1
V44_BACKGROUND_MARGIN = 817_OVER_4800
V44_PRINCIPAL_MEAN_AP_FORM = PROVED_EXACT_C_S_DIVISOR_EXPANSION
V44_PRINCIPAL_MEAN_ABSOLUTE_CEILING = X_POWER_5_OVER_3_PLUS_O1
V44_PRINCIPAL_MEAN_ENDPOINT_DEFICIT = 1_OVER_400
V44_PRINCIPAL_MEAN_GATE = OPEN_X_POWER_5_OVER_3_MINUS_DELTA_M_WITH_DELTA_M_GREATER_THAN_1_OVER_400
V44_TRANSITION_CONDITIONAL_COMPILER = PROVED_MEAN_AND_VARIANCE_GATES_PAY_FULL_TRANSITION
V44_LONG_BALANCED_WINDOW = OPEN_D_GT_U_AND_K_GT_U
V44_LONG_REVERSE_TYPE_I_WINDOW = OPEN_D_GT_U_AND_K_LE_U
V44_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V44_BFI_GENERIC_LARGE_SIEVE = SOURCE_BACKED_GENERIC_P_SQUARED_CEILING_ONLY
V44_BFI_BDH_TO_FIXED_POWER = STOP_SCOPED_LOG_SAVING_DOES_NOT_PAY_1_OVER_400
V44_MAYNARD_LARGE_MODULI_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_RESIDUE_FACTORIZED_MODULI_MAX_RELATIVE_EXPONENT_11_OVER_21_NOT_ALL_RESIDUE_VARIANCE_AT_31_OVER_32_TO_399_OVER_400
V44_DONG_ROBLES_ZEINDLER_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_A_B_TWO_ARRAY_FORM_NOT_MOVING_NU_OR_RECIPROCAL_FOURTH_MOMENT
V44_PASCADI_HORIZONTAL_DIRECT_ATTACHMENT = STOP_SCOPED_POST_EMITTER_LOCAL_FORM_NOT_TRANSITION_MEAN_OR_VARIANCE_COMPILER
V44_DIRECT_PRIMARY_SOURCE_FOR_TWO_TRANSITION_GATES = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10
V44_FIRST_FATAL = NO_LITERAL_THEOREM_GIVES_FIXED_POWER_FOR_THE_PRINCIPAL_RAMANUJAN_MEAN_OR_CENTERED_PRIME_SHORT_INTEGER_RECIPROCAL_VARIANCE_AT_REDUCED_MODULI_Q_POWER_31_OVER_32_TO_Q_POWER_399_OVER_400
V44_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B_TRANSITION_SPLIT_INTO_TWO_ENDPOINT_GATES_LONG_MOBIUS_SPAN_OPEN
V44_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V44_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~

## 44. V43 后的罗盘：小因子 alias 已清空，零轴被精确搬到 Gate A

V43 没有继续堆一个 dyadic MPD 小引理，而是对 V35 proper-factor 方向先做完整
centered Poisson。把 ordered coefficient 在 physical endpoint (u) 冻结为
`vartheta_x(d;u)` 后，对角仍逐字满足

```text
sum_(d|u,2<=d<=x/2) vartheta_x(d;u)=beta_raw(u).      (44.1)
```

对 `q`-periodic unit-centered row，完整 Poisson alias 为

```text
P_(q,d)(u)=H/(dq) sum_(m!=0,q not divide m) psi(Hm/(dq))
  [e_d(m*u*inverse(q))+(q-1)^(-1)e_(dq)(m*u)].       (44.2)
```

因此在

```text
Y0=H/(4Q)=x^(31/96+o(1))
```

以下，所有非零 alias 由 `supp psi subset [-1,1]` 精确消失。关键是不能把这误报为
physical row 已付：原 row 删除 `u=dk`，故完整格的零均值恰好返回负的 physical
diagonal。逐 row、逐 prime shell 重组后得到新的宏观桥

```text
C_x=A_x-L_pr*S_physical
    +O(x^(79/48+epsilon+o(1))+x^(4/3+o(1))),         (44.3)
D_x=A_x-L_pr*S_physical
    +O(x^(53/32+o(1))+x^(79/48+epsilon+o(1))),       (44.4)
J(r_x)=A_x/L_pr+O(x^(95/96+o(1))+x^(47/48+epsilon+o(1))).
```

这里 `epsilon<11/600`，hard-shell numerator error 留有 `11/600-epsilon`
margin。于是 Gate B 与 Gate A 不再是两个不透明红叉：它们由同一个 scalar alias
精确相连；但仍是 AND gate，任何一门都不能借另一门的 credit。

Poisson 后只剩三段：`Y0<d<=U` 的 transition dual 长度仅
`x^(23/2400+o(1))`；`d>U,k>U` 是 balanced Type II；`d>U,k<=U` 是 Möbius
落在长变量上的 reverse Type I。现有 Bettin--Chandee、Pascadi、
Blomer--Pascadi、Runbo Li 与 Bazin 都没有直接接受这一 whole physical alias。
所以新 first fatal 是同一条长 Möbius/四变量 inverse-residue theorem，而不是小因子
Poisson 或对角符号。

正式 status 为

```text
V43_MAXIMUM_CLAIM = EXACT_PROPER_FACTOR_POISSON_TRANSFERENCE_DELETES_ALL_SMALL_D_NONZERO_ALIASES_AND_IDENTIFIES_THE_D_GT_H_OVER_4Q_INVERSE_RESIDUE_GATE_A_FRONTIER_WITH_ZERO_AXIS_RETURN
V43_ROUTE_ADVANCE = YES
V43_CONDITIONAL_BRIDGE_ADVANCE = YES
V43_ARITHMETIC_ADVANCE = NO
V43_FIXED_ATOM_CREDIT = 0
V43_STRICT_1_OVER_400 = UNPAID
V43_L2 = NONE
V43_TPC_207_TRIGGER = false
V43_NUMBERED_RELEASE = NO
V43_DERIVATION_STATUS = COHERENT_AFTER_ORDERED_WEIGHT_FREEZE_CENTERED_POISSON_HARD_SHELL_DIAGONAL_AND_SCALAR_REASSEMBLY
V43_ASSUMPTION_POLICY = GATE_A_ALIAS_AND_GATE_B_NUMERATOR_REMAIN_TWO_EXPLICIT_OPEN_THEOREMS
V43_SELECTED_RESEARCH_ROUTE = PROPER_FACTOR_POISSON_TRANSFERENCE_FIRST__TRANSITION_TYPE_II_REVERSE_TYPE_I_ALIAS_SECOND__V42_MPD_PARALLEL__A_AND_B_JOIN__C_RESERVE
V43_V35_PROPER_FACTOR_IDENTITY = RETAINED_EXACT_BETA_EQUALS_SUM_MU_TIMES_OMEGA
V43_ORDERED_WEIGHT_FREEZE = PROVED_UNIFORM_ERROR_ABS_U_MINUS_DK_OVER_X_LOG_X
V43_WEIGHT_FREEZE_DIAGONAL = PROVED_EXACT_SUM_D_DIVIDES_U_THETA_FROZEN_EQUALS_BETA_U
V43_FOLDED_NONSQUARE_IDENTITY = PROVED_EXACT_TWO_ORIENTATION_FORM
V43_FOLDED_SQUARE_IDENTITY = PROVED_EXACT_MU_S_OVER_2
V43_SEMIPRIME_ORIENTATION_CANCELLATION = PROVED_EXACT_ZERO_WHEN_BOTH_MU_EQUAL_MINUS_1_IN_SHORT_FACTOR_BRANCH
V43_CENTERED_UNIT_VECTOR = PROVED_EXACT_Q_PERIODIC_PHYSICAL_U1_ROW
V43_CENTERED_UNIT_VECTOR_MEAN = PROVED_EXACT_ZERO
V43_CENTERED_UNIT_VECTOR_DFT = PROVED_EXACT_NONZERO_FREQUENCY_E_MINUS_AR_PLUS_ONE_OVER_Q_MINUS_1_OVER_Q
V43_COMPLETE_POISSON_ALIAS = PROVED_EXACT_H_OVER_DQ_TIMES_INVERSE_RESIDUE_PLUS_BACKGROUND_SUM
V43_POISSON_PHASE_RECIPROCITY = PROVED_EXACT_E_Q_MINUS_MU_DBAR_TIMES_E_DQ_MU_EQUALS_E_D_MU_QBAR
V43_SMALL_D_CUTOFF = H_OVER_4Q_EQUALS_X_POWER_31_OVER_96_PLUS_O1
V43_SMALL_D_NONZERO_ALIAS = PROVED_EXACT_ZERO_BY_PSI_SUPPORT
V43_OFFZERO_DELETION_EFFECT = PROVED_EXACT_NEGATIVE_PHYSICAL_DIAGONAL_RETURN
V43_ROW_TRANSFERENCE = PROVED_S_Q_EQUALS_ALIAS_Q_MINUS_CENTERED_UNIT_DIAGONAL_PLUS_ERROR
V43_ROW_TRANSFERENCE_ERROR = X_POWER_H_SQUARED_OVER_Q_TIMES_X_EPSILON_PLUS_O1
V43_SCALAR_ALIAS = PROVED_EXACT_ONE_OUTER_SIGNED_SUM_Q_Q_ALIAS_Q
V43_DIAGONAL_SHELL_COEFFICIENT = Q_TIMES_Q_MINUS_2_OVER_Q_MINUS_1
V43_DIAGONAL_SHELL_COEFFICIENT_SUM = L_PR_PLUS_X_O1
V43_UNIT_OMISSION_CORRECTION = PROVED_ABSOLUTE_X_POWER_4_OVER_3_PLUS_O1
V43_CORE_SCALAR_TRANSFERENCE = PROVED_C_EQUALS_ALIAS_MINUS_L_PR_S_PHYSICAL_PLUS_PAID_ERRORS
V43_SHELL_FREEZE_ERROR_NUMERATOR = X_POWER_79_OVER_48_PLUS_EPSILON_PLUS_O1
V43_SHELL_FREEZE_ERROR_MARGIN = 11_OVER_600_MINUS_EPSILON
V43_V35_PRINCIPAL_NONUNIT_REMAINDERS = RETAINED_PAID_X_POWER_53_OVER_32_PLUS_O1
V43_DIRECT_NUMERATOR_TRANSFERENCE = PROVED_D_EQUALS_ALIAS_MINUS_L_PR_S_PHYSICAL_PLUS_PAID_ERRORS
V43_J_MAJOR_ALIAS = PROVED_J_R_EQUALS_ALIAS_OVER_L_PR_PLUS_X_95_OVER_96_AND_X_47_OVER_48_ERRORS
V43_GATE_B_TO_GATE_A_ZERO_AXIS_TRANSFER = PROVED_EXACT_UP_TO_PAID_ERRORS
V43_SMALL_FACTOR_TYPE_I_ALIAS = DELETED_EXACT_NONZERO_FREQUENCIES_BUT_ZERO_AXIS_NOT_PAID
V43_TRANSITION_RANGE = H_OVER_4Q_LT_D_LE_X_POWER_133_OVER_400
V43_TRANSITION_DUAL_LENGTH = X_POWER_23_OVER_2400_PLUS_O1
V43_TYPE_II_RANGE = D_GT_U_AND_K_GT_U
V43_REVERSE_TYPE_I_RANGE = D_GT_U_AND_K_LE_U_WITH_MOBIUS_ON_LONG_D
V43_SQUARE_ROW_ENERGY = PROVED_ABSOLUTE_X_POWER_95_OVER_48_PLUS_O1
V43_SQUARE_ROW_ENERGY_MARGIN = 1_OVER_3
V43_SQUARE_SCALAR_OUTPUT = PROVED_ABSOLUTE_X_POWER_143_OVER_96_PLUS_O1
V43_CONDITIONAL_TWO_GATE_COMPILER = PROVED_H_A_AND_H_B_IMPLY_PHYSICAL_X_POWER_399_OVER_400_MINUS_ETA
V43_CONDITIONAL_TWO_GATE_MARGIN = MIN_ETA_A_ETA_B_19_OVER_2400_AND_11_OVER_600_MINUS_EPSILON
V43_V42_MPD_GATE = RETAINED_PARALLEL_SUFFICIENT_IMPLEMENTATION_OF_GATE_B
V43_BETTIN_CHANDEE_DIRECT_ATTACHMENT = STOP_SCOPED_PHYSICAL_U_COUPLED_TO_NUMERATOR_DENOMINATOR_AND_MOVING_DUAL_CUTOFF
V43_BLOMER_PASCADI_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_MODULUS_LOCAL_CELL_NO_VARYING_D_Q_U_AGGREGATE
V43_PASCADI_HORIZONTAL_KUZNETSOV = OPEN_STRONGEST_ALTERNATIVE_COMPILER_CANDIDATE_AFTER_EXACT_ALIAS_EMITTER
V43_RUNBO_LI_FIRST_SIZE_CONDITIONS = PASS_599_OVER_600_AND_1199_OVER_1200
V43_RUNBO_LI_SECOND_SIZE_CONDITIONS = FAIL_2531_OVER_400_AND_1897_OVER_300_GREATER_THAN_4
V43_RUNBO_LI_DIRECT_ATTACHMENT = STOP_SCOPED_MODULUS_FACTORS_FIXED_RESIDUE_AND_NO_PHYSICAL_W_ALIAS
V43_BAZIN_DIRECT_ATTACHMENT = STOP_SCOPED_COLLAPSED_BETA_MARGINAL_NOT_JOINT_PROPER_FACTOR_POISSON_ALIAS
V43_DIRECT_PRIMARY_SOURCE_FOR_HARD_ALIAS = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10
V43_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_THE_FULL_CENTERED_TRANSITION_OR_LONG_MOBIUS_REVERSE_TYPE_I_AND_BALANCED_FOUR_VARIABLE_INVERSE_RESIDUE_ALIAS_WITH_PHYSICAL_W_AT_THE_STRICT_NUMERATOR_POWER
V43_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B_SMALL_FACTOR_ALIAS_REMOVED_ZERO_AXIS_RETURNED_LONG_MOBIUS_SPAN_OPEN
V43_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V43_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
```

## 43. V42 后的罗盘：主跨必须保留 Möbius 方向

V42 把 V41 的 residual row精确写成

```text
E_res=D_res+O_res,
(O_res)_+ << x^(37/16+o(1))                          (V42 primary open)
```

并把 V35 proper-factor identity插入同一 q-local residual，得到

```text
rho_q=sum_(dk,u)mu(d)omega_x(d,k)(w(u)-Gamma_q(u))
      K_H(u-dk)c'_q(u-dk).                            (43.1)
```

post-`u` occurrence diagonal仍为 `x^(95/48+o(1))`。因此 source-facing首选实现只需
对每个不交 dyadic `d`-cell证明 fixed physical direction estimate

```text
sum_q|rho_(q,j)|^2 <= Q*x^o*D_j.                     (43.2)
```

`O(log x)` cell reassembly不改幂，条件输出为 `x^(53/32+o(1))`，margin
`19/2400`。

路线选择也被一个精确维数墙约束。只看 operator/HS/stable-rank 的 certificate损失
至少为 `N_active/x^(1/3)`；所以它必须先证

```text
N_active <= x^(273/400-o(1)).                         (43.3)
```

full-active情况下 generic loss为 `x^(2/3)`，比 endpoint allowance多
`127/400`。这不否定 actual Möbius方向可能抵消；它只停止 orientation-blind
Schatten路。当前大路因此是

```text
positive physical Gram collision
  -> proper-factor dyadic MPD implementation
  -> coefficient-native Type-I/II transform
  -> terminal q-local Gate A.
```

正式 status为

```text
V42_MAXIMUM_CLAIM = EXACT_QLOCAL_POSITIVE_GRAM_GATE_PROPER_FACTOR_LIFT_PAID_OCCURRENCE_DIAGONAL_DYADIC_DIRECTIONAL_COMPILER_AND_OPERATOR_ONLY_CERTIFICATE_NO_GO
V42_ROUTE_ADVANCE = YES
V42_CONDITIONAL_BRIDGE_ADVANCE = YES
V42_ARITHMETIC_ADVANCE = NO
V42_FIXED_ATOM_CREDIT = 0
V42_STRICT_1_OVER_400 = UNPAID
V42_L2 = NONE
V42_TPC_207_TRIGGER = false
V42_NUMBERED_RELEASE = NO
V42_DERIVATION_STATUS = COHERENT_AFTER_EXACT_PROPER_FACTOR_LIFT_OCCURRENCE_DIAGONAL_DYADIC_REASSEMBLY_DIRECTIONAL_AND_ZERO_AXIS_FIREWALLS
V42_ASSUMPTION_POLICY = CELLWISE_PHYSICAL_MOBIUS_PRIME_DIRECTIONAL_DISPERSION_REMAINS_EXPLICIT_OPEN_THEOREM
V42_SELECTED_RESEARCH_ROUTE = PROPER_FACTOR_DIRECTIONAL_DISPERSION_FIRST__SOURCE_NATIVE_TYPE_I_II_TRANSFORM_SECOND__GENERIC_OPERATOR_AND_MARGINAL_ROADS_STOP__A_TERMINAL__C_RESERVE
V42_V41_QLOCAL_SPLIT = RETAINED_EXACT_MODEL_PAID_RESIDUAL_OPEN
V42_V35_PROPER_FACTOR_IDENTITY = RETAINED_EXACT_BETA_EQUALS_SUM_MU_TIMES_OMEGA
V42_PROPER_FACTOR_SUPPORT = PROVED_EXACT_D_AND_K_AT_LEAST_2
V42_PRIME_ROW_CANCELLATION = PROVED_EXACT_EMPTY_PROPER_FACTOR_SUM
V42_RESIDUAL_PROPER_FACTOR_LIFT = PROVED_EXACT_BEFORE_ANY_OUTER_ABSOLUTE
V42_PROPER_FACTOR_OCCURRENCE_DIAGONAL = PROVED_X_POWER_95_OVER_48
V42_COLLAPSED_TO_OCCURRENCE_DIAGONAL = PROVED_WITH_DIVISOR_X_O1_LOSS
V42_RESIDUAL_GRAM_IDENTITY = PROVED_EXACT_E_RES_EQUALS_D_RES_PLUS_REAL_SIGNED_O_RES
V42_PRIMARY_POSITIVE_GRAM_GATE = OPEN_CONJECTURE_POSITIVE_O_RES_LE_X_POWER_37_OVER_16
V42_SPIKE_BACKGROUND_ENERGY = PROVED_EXACT_WITH_SIGNED_CROSS_TERM_RETAINED
V42_DYADIC_D_CELLS = PROVED_EXACT_DISJOINT_O_LOG_X_PARTITION
V42_DYADIC_RESIDUAL_REASSEMBLY = PROVED_EXACT_RHO_EQUALS_SUM_J_RHO_J
V42_CELLWISE_MOBIUS_PRIME_DIRECTIONAL_GATE = OPEN_CONJECTURE_E_J_LE_Q_X_O1_D_J
V42_CELLWISE_DIRECTIONAL_LOSS = Q_EQUALS_X_POWER_1_OVER_3
V42_CELLWISE_TO_GLOBAL_COMPILER = PROVED_BY_L2_TRIANGLE_AND_CELL_CAUCHY
V42_CONDITIONAL_RESIDUAL_ENERGY = X_POWER_37_OVER_16
V42_CONDITIONAL_RESIDUAL_DUAL_NORM = X_POWER_37_OVER_32
V42_CONDITIONAL_SCALAR_OUTPUT = X_POWER_53_OVER_32
V42_CONDITIONAL_ENDPOINT_MARGIN = 19_OVER_2400
V42_CONDITIONAL_KAPPA = 1_OVER_48
V42_CELLWISE_L2_DUAL = PROVED_ONE_OUTER_ABSOLUTE_MODULUS_FAMILY
V42_OMEGA_TWO_BRANCH_FORM = PROVED_EXACT_MU_LOG_D_OR_MU_LOG_K_OVER_LOG_DK
V42_LOG_DENOMINATOR_ABEL_COMPILER = PROVED_EXACT_UNIFORM_PRODUCT_CUTOFF_INTERFACE
V42_OPERATOR_MATRIX_IDENTITY = PROVED_E_RES_EQUALS_NORM_A_ONE_ACTIVE_SQUARED_AND_D_RES_EQUALS_HS_SQUARED
V42_STABLE_RANK_CEILING = PROVED_AT_MOST_NUMBER_OF_Q_ROWS_X_POWER_1_OVER_3
V42_OPERATOR_ONLY_CERTIFICATE_LOSS_FLOOR = N_ACTIVE_OVER_X_POWER_1_OVER_3
V42_OPERATOR_ONLY_THRESHOLD_SUPPORT_CEILING = X_POWER_273_OVER_400
V42_OPERATOR_ONLY_FULL_ACTIVE_LOSS = X_POWER_2_OVER_3
V42_OPERATOR_ONLY_ENDPOINT_EXCESS = 127_OVER_400
V42_MAXIMAL_STABLE_RANK_FIXTURE = PROVED_2_BY_8_HADAMARD_ROWS_RATIO_4
V42_GENERIC_CENTERED_KERNEL_Q_LOSS = STOP_SCOPED_Q5_M3_COUNTEREXAMPLE_RATIO_75_OVER_7
V42_COEFFICIENT_BLIND_ROW_BESSEL = STOP_SCOPED_PHYSICAL_DIRECTION_REQUIRED
V42_SPLIT_BETA_CHANNELS_BEFORE_OUTER_ABSOLUTE = STOP_SCOPED_PRIME_ROW_EXACT_CANCELLATION_DESTROYED
V42_OFFZERO_DIRECTIONAL_GATE_TO_ZERO_AXIS = STOP_SCOPED_DELTA_ZERO_FIREWALL_RETAINED
V42_TERMINAL_QLOCAL_GATE_A = OPEN_INDEPENDENT_SIGNED_COVARIANCE
V42_MRT_DIRECT_ATTACHMENT = STOP_SCOPED_SOURCE_COEFFICIENTS_AND_Q_DEPENDENT_RESIDUAL_MISMATCH
V42_HARPER_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_FIXED_SEQUENCE_AND_MODULUS_HYPOTHESES_MISMATCH
V42_BAZIN_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_SIDED_BETA_MARGINAL_NOT_JOINT_ROW_SQUARE
V42_RUNBO_LI_DIRECT_ATTACHMENT = STOP_SCOPED_FACTORED_MODULUS_PRIME_DISTRIBUTION_NOT_PROPER_FACTOR_RESIDUAL_DIRECTION
V42_BLOMER_PASCADI_BALANCED_CELL = SOURCE_BACKED_LOCAL_ENGINE_Q_MINUS_1_OVER_32_AFTER_V38_EXACT_EMITTER
V42_LOCAL_KLOOSTERMAN_ENGINE_TO_MPD = STOP_SCOPED_BLOCK_ATOMIC_BUDGET_AND_Q_L2_REASSEMBLY_UNPAID
V42_MILICEVIC_QIN_WU_DIRECT_ATTACHMENT = STOP_SCOPED_POST_TRANSFORM_FIXED_MODULUS_KLOOSTERMAN_ARRAYS_ONLY
V42_DIRECT_PRIMARY_SOURCE_FOR_MPD_CELL_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10
V42_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_POSITIVE_PHYSICAL_OFFDIAGONAL_GRAM_COLLISION_AT_X_POWER_37_OVER_16_WHILE_RETAINING_CENTERED_SPIKE_BACKGROUND_CROSS_TERM
V42_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_QLOCAL_MODEL_PIER_PAID_PROPER_FACTOR_DIRECTIONAL_SPAN_OPEN
V42_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V42_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
```

## 42. V41 后的罗盘：q-local 模型桥墩已付，主跨缩为 residual row-Bessel

V41 没有再换一个抽象 norm，而是直接打开 V40 的 literal row。对每个
`q~Q=x^(1/3)`，用 V30 的三剩余类局部密度 `Gamma_q` 作 exact 分解

```text
s_q = m_q + rho_q.
```

`m_q` 保留全部 physical `beta_x^raw(t)`、hard shell、unit deletion 与
`c'_q(u-t)`。三剩余类的零均值及唯一异常类 `t=-2 (mod q)` 给

```text
|m_q| << x^(1+o(1)) H/q^2,
sum_q |m_q|^2 << x^(37/16+o(1)).
```

所以模型 scalar 已付到 `x^(53/32+o(1))`，比 strict `399/400` numerator
门槛多出 `19/2400` margin。V40 的 `rowwise local carrier unpaid` 因而在这个
benchmark 上关闭；这仍只是 exact/elementary route advance。

真正剩余的 Gate-B 主跨是

```text
E_res = sum_q |rho_q|^2 << x^(7/3-kappa+o(1)),
kappa > 1/200,
```

或相对已付 diagonal `D_res<<x^(95/48+o(1))` 的 restricted row-Bessel

```text
E_res << x^(tau+o(1)) D_res,  tau < 419/1200.
```

样例 `tau=1/3` 同样落在 `37/16` 能量与 `53/32` 输出。exact L2 dual 和
same-index character row 已经给出施工接口，但单独 marginal large sieve 不控制这个
乘积残差。更重要的是所有这些 row 都删掉 `h=0`；`delta_0` fixture 强制 terminal
Gate A 仍独立开放，不能从 residual energy 偷取 fixed-atom credit。

```text
V41_MAXIMUM_CLAIM = EXACT_QLOCAL_ROW_SPLIT_AND_ELEMENTARY_MODEL_ENERGY_PAYMENT_REDUCE_GATE_B_TO_RESIDUAL_ROW_BESSEL_WITH_ZERO_AXIS_FIREWALL
V41_ROUTE_ADVANCE = YES
V41_CONDITIONAL_BRIDGE_ADVANCE = YES
V41_ARITHMETIC_ADVANCE = NO
V41_FIXED_ATOM_CREDIT = 0
V41_STRICT_1_OVER_400 = UNPAID
V41_L2 = NONE
V41_TPC_207_TRIGGER = false
V41_NUMBERED_RELEASE = NO
V41_DERIVATION_STATUS = COHERENT_AFTER_EXACT_QLOCAL_SPLIT_THREE_RESIDUE_MODEL_PAYMENT_RESIDUAL_ENDPOINT_AND_ZERO_AXIS_FIREWALL
V41_ASSUMPTION_POLICY = RESIDUAL_ROW_ENERGY_OR_RESTRICTED_RESIDUAL_ROW_BESSEL_REMAINS_EXPLICIT_OPEN_THEOREM
V41_SELECTED_RESEARCH_ROUTE = QLR_RESIDUAL_Q_ROW_ENERGY_FIRST__RBR_RESTRICTED_RESIDUAL_ROW_BESSEL_IMPLEMENTATION__DUAL_AND_CHARACTER_FORMS_SECOND__P2_K_E_X_RESERVES__A_TERMINAL__C_RESERVE
V41_V40_CONSTANT_RESIDUE_SCALAR = RETAINED_EXACT_ZERO_REMAINDER
V41_QLOCAL_PROFILE = GAMMA_Q_THREE_RESIDUE_FORM_REUSED_FROM_V30
V41_QLOCAL_PROFILE_MEAN = PROVED_EXACT_ZERO_MOD_Q
V41_EXACT_ROW_SPLIT = S_Q_EQUALS_M_Q_PLUS_RHO_Q
V41_MODEL_ROW_POINTWISE = PROVED_X_POWER_1_TIMES_H_OVER_Q_SQUARED
V41_MODEL_EXCEPTIONAL_RESIDUE = T_CONGRUENT_MINUS_2_COUNT_X_OVER_Q
V41_MODEL_ROW_ENERGY = PROVED_X_POWER_37_OVER_16
V41_MODEL_SCALAR_OUTPUT = PROVED_X_POWER_53_OVER_32
V41_MODEL_ENDPOINT_MARGIN = 19_OVER_2400
V41_V40_LOCAL_CARRIER_ROWWISE_STATUS = PAID_AT_ROW_BENCHMARK
V41_RESIDUAL_ROW_ENERGY = SUM_Q_ABS_RHO_Q_SQUARED
V41_RESIDUAL_ROW_ENERGY_GATE = OPEN_CONJECTURE_X_POWER_7_OVER_3_MINUS_KAPPA
V41_RESIDUAL_KAPPA_THRESHOLD = KAPPA_STRICTLY_GREATER_THAN_1_OVER_200
V41_RESIDUAL_CONDITIONAL_OUTPUT = MAX_OF_X_POWER_53_OVER_32_AND_X_POWER_5_OVER_3_MINUS_KAPPA_OVER_2
V41_RESIDUAL_ENDPOINT_MARGIN = MIN_OF_19_OVER_2400_AND_KAPPA_OVER_2_MINUS_1_OVER_400
V41_FULL_ROW_FROM_RESIDUAL = PROVED_TRIANGLE_WITH_PAID_MODEL
V41_RESIDUAL_ROW_DIAGONAL = PROVED_X_POWER_95_OVER_48
V41_RESTRICTED_RESIDUAL_ROW_BESSEL_GATE = OPEN_CONJECTURE_E_RES_LE_X_POWER_TAU_TIMES_D_RES
V41_RESTRICTED_RESIDUAL_ROW_BESSEL_TAU_THRESHOLD = TAU_STRICTLY_LESS_THAN_419_OVER_1200
V41_SAMPLE_RESIDUAL_TAU = 1_OVER_3
V41_SAMPLE_RESIDUAL_ENERGY = X_POWER_37_OVER_16
V41_SAMPLE_RESIDUAL_OUTPUT = X_POWER_53_OVER_32
V41_SAMPLE_RESIDUAL_MARGIN = 19_OVER_2400
V41_RESIDUAL_L2_DUAL = PROVED_ONE_OUTER_ABSOLUTE_MODULUS_FAMILY
V41_RESIDUAL_CHARACTER_ROW = PROVED_EXACT_CENTERED_BW_RES_MINUS_Z_RES
V41_SEPARATE_MARGINAL_LARGE_SIEVE = STOP_SCOPED_DOES_NOT_CONTROL_SAME_INDEX_RESIDUAL_PRODUCT
V41_OFFZERO_RESIDUAL_TO_ZERO_AXIS = STOP_SCOPED_DELTA_ZERO_FIXTURE
V41_AUGMENTED_ROW_WITH_ZERO_AXIS = TERMINAL_EQUIVALENT_NOT_PRELIMINARY
V41_TERMINAL_QLOCAL_GATE_A = OPEN_INDEPENDENT_SIGNED_COVARIANCE
V41_MRT_DIRECT_ATTACHMENT = STOP_SCOPED_SOURCE_COEFFICIENTS_LOG_SAVING_AND_Q_DEPENDENT_RESIDUAL_MISMATCH
V41_MERIKOSKI_DIRECT_ATTACHMENT = STOP_SCOPED_UNWEIGHTED_FIRST_SHIFT_AVERAGE_NOT_CENTERED_ROW_SQUARE
V41_LICHTMAN_TERAVAINEN_DIRECT_ATTACHMENT = STOP_SCOPED_QUALITATIVE_EXCEPTIONAL_SET_CAN_CONTAIN_SPARSE_QK_SUPPORT_AND_COEFFICIENTS_MISMATCH
V41_EVANS_DIRECT_ATTACHMENT = STOP_SCOPED_E2_FACTOR_WINDOWS_AND_ALMOST_ALL_SHIFT_OUTPUT_MISMATCH
V41_KOUKOULOPOULOS_SHORT_AP_ATTACHMENT = STOP_SCOPED_Q_SQUARED_EXCEEDS_H_AND_ONE_SEQUENCE_MARGINAL
V41_HARPER_GENERAL_BDH_ATTACHMENT = STOP_SCOPED_FIXED_SEQUENCE_LARGE_MODULUS_AND_DISTRIBUTION_HYPOTHESES_MISMATCH
V41_BAZIN_BETA_MARGINAL_TO_RESIDUAL_ROW = STOP_SCOPED_ONE_SIDED_MARGINAL_AND_H_QUARTER_LOSS
V41_DIRECT_PRIMARY_SOURCE_FOR_RESIDUAL_ROW_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_10
V41_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_SUM_Q_ABS_RHO_Q_SQUARED_AT_X_POWER_7_OVER_3_MINUS_KAPPA_FOR_KAPPA_GREATER_THAN_1_OVER_200
V41_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_QLOCAL_MODEL_PIER_PAID_RESIDUAL_ROW_BESSEL_SPAN_OPEN
V41_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V41_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
```

## 41. V40 后的罗盘：只读 constant residue direction，主桥转向 q-row energy

V40 对 V39 packet norm作了一次 whole-object 投影审计。目标 scalar只含
`s_q=sum_r d_q(r)`，因此

```text
E_row=sum_q|s_q|^2,
|C_x|<<Q^(3/2)E_row^(1/2).
```

新 gate `E_row<<x^(7/3-kappa+o(1))` 的 strict threshold仍是
`kappa>1/200`，但它不再支付 transverse residue modes。V39 packet P2通过一个 `Q`
factor推出 row gate；q=5 alternating packet证明反向不成立。

物理 coefficient `a_q(t)=beta(t)G_(q,t)` 的 diagonal 已有
`D_row<<x^(95/48+o(1))`。于是 current preferred theorem 变为

```text
E_row<<x^(tau+o(1))D_row, tau<419/1200.
```

benchmark `tau=1/3` 给 `E_row=x^(37/16+o(1))`、`kappa=1/48`、output
`53/32` 与 margin `19/2400`。这是 route advance，不是 arithmetic saving。exact
shift normal form与 character form给出两个实现接口；V36 residual不能在未付 rowwise
local carrier时偷换 full shift。Harper、Zheng、Pascadi、BFKMM与 Blomer--Pascadi都没有
literal row-energy theorem。

```text
V40_MAXIMUM_CLAIM = EXACT_CONSTANT_RESIDUE_COMPRESSION_DIAGONAL_PACKET_PAYMENT_AND_ROW_BESSEL_THRESHOLD_SELECT_Q_ROW_ENERGY_AS_WEAKER_PRIMARY_BRIDGE
V40_ROUTE_ADVANCE = YES
V40_CONDITIONAL_BRIDGE_ADVANCE = YES
V40_ARITHMETIC_ADVANCE = NO
V40_FIXED_ATOM_CREDIT = 0
V40_STRICT_1_OVER_400 = UNPAID
V40_L2 = NONE
V40_TPC_207_TRIGGER = false
V40_NUMBERED_RELEASE = NO
V40_DERIVATION_STATUS = COHERENT_AFTER_CONSTANT_RESIDUE_COMPRESSION_COLLISION_EXPANSION_DIAGONAL_PAYMENT_AND_THREE_NORMAL_FORMS
V40_ASSUMPTION_POLICY = ROW_ENERGY_ROW_BESSEL_FULL_SHIFT_AND_JOINT_CHARACTER_BOUNDS_REMAIN_EXPLICIT_OPEN_THEOREMS
V40_SELECTED_RESEARCH_ROUTE = R2_Q_ROW_ENERGY_FIRST__RB_RESTRICTED_ROW_BESSEL_IMPLEMENTATION__SHIFT_AND_CHARACTER_NORMAL_FORMS_SECOND__P2_PACKET_ENERGY_K_SCHATTEN_E_RESIDUAL_X_CHARACTER_RESERVES__A_TERMINAL__C_RESERVE
V40_V39_PACKET_SCALAR = RETAINED_EXACT_ZERO_REMAINDER
V40_CONSTANT_RESIDUE_ROW_SCALAR = S_Q_EQUALS_SUM_R_D_Q_R
V40_ROW_ENERGY = SUM_Q_ABS_S_Q_SQUARED
V40_DIRECT_ROW_ENERGY_CAUCHY = PROVED_Q_POWER_3_OVER_2_TIMES_ROW_ENERGY_SQUARE_ROOT
V40_ROW_ENERGY_GATE = OPEN_CONJECTURE_X_POWER_7_OVER_3_MINUS_KAPPA
V40_ROW_ENERGY_KAPPA_THRESHOLD = KAPPA_STRICTLY_GREATER_THAN_1_OVER_200
V40_ROW_ENERGY_CONDITIONAL_OUTPUT = X_POWER_5_OVER_3_MINUS_KAPPA_OVER_2
V40_ROW_ENERGY_ENDPOINT_MARGIN = KAPPA_OVER_2_MINUS_1_OVER_400
V40_PACKET_ENERGY_IMPLIES_ROW_ENERGY = PROVED_CAUCHY_WITH_ONE_Q_FACTOR
V40_ROW_ENERGY_IMPLIES_PACKET_ENERGY = STOP_SCOPED_Q5_ALTERNATING_TRANSVERSE_PACKET
V40_V39_PACKET_P2_STATUS = RETAINED_STRONGER_RESERVE_NOT_PRIMARY_NORM
V40_PHYSICAL_ROW_COEFFICIENT = A_Q_T_EQUALS_BETA_T_TIMES_G_Q_T
V40_ROW_COLLISION_IDENTITY = PROVED_EXACT_DIAGONAL_PLUS_SIGNED_OFFDIAGONAL
V40_ROW_OFFDIAGONAL_POSITIVITY = STOP_SCOPED_SIGN_INDEFINITE_FINITE_FIXTURE
V40_CENTERED_PACKET_POINTWISE_ENVELOPE = PROVED_H_OVER_Q_TIMES_X_O1
V40_ROW_DIAGONAL_PAYMENT = PROVED_X_POWER_95_OVER_48
V40_RESTRICTED_ROW_BESSEL_GATE = OPEN_CONJECTURE_E_ROW_LE_X_POWER_TAU_TIMES_D_ROW
V40_RESTRICTED_ROW_BESSEL_TAU_THRESHOLD = TAU_STRICTLY_LESS_THAN_419_OVER_1200
V40_SAMPLE_ROW_BESSEL_TAU = 1_OVER_3
V40_SAMPLE_ROW_ENERGY = X_POWER_37_OVER_16
V40_SAMPLE_ROW_KAPPA = 1_OVER_48
V40_SAMPLE_ROW_OUTPUT = X_POWER_53_OVER_32
V40_SAMPLE_ROW_ENDPOINT_MARGIN = 19_OVER_2400
V40_UNIT_FREE_SHIFT_ROW = PROVED_EXACT_CENTERED_DIVISIBILITY_MULTIPLIER
V40_UNIT_DELETION_POINTWISE = PROVED_X_POWER_1_TIMES_H_OVER_Q_SQUARED
V40_UNIT_DELETION_ENERGY = PROVED_X_POWER_37_OVER_16
V40_EFFECTIVE_SHIFT_BELOW_Q_SQUARED = PROVED_SCHWARTZ_WITH_EXPONENT_GAP_1_OVER_96
V40_UNIQUE_PRIME_DIVISOR_SUPPORT = PROVED_FOR_NONZERO_ABS_H_STRICTLY_BELOW_Q_SQUARED
V40_SHIFT_ENERGY_COMPILER = PROVED_H_OVER_Q_TIMES_FULL_SHIFT_WEIGHTED_ENERGY_PLUS_UNIT_PAYMENT
V40_FULL_SHIFT_ENERGY_GATE = OPEN_STRONGER_CONJECTURE_X_POWER_2_PLUS_2_SIGMA
V40_FULL_SHIFT_SIGMA_THRESHOLD = SIGMA_STRICTLY_LESS_THAN_13_OVER_4800
V40_V36_RESIDUAL_TO_FULL_SHIFT_ATTACHMENT = STOP_SCOPED_LOCAL_CARRIER_ROWWISE_REASSEMBLY_UNPAID
V40_JOINT_CHARACTER_ROW_IDENTITY = PROVED_EXACT_CENTERED_BW_MINUS_Z
V40_JOINT_CHARACTER_FOURTH_MOMENT = OPEN_STRONGER_THEOREM_INTERFACE
V40_SEPARATE_MARGINAL_CHARACTER_LARGE_SIEVE = STOP_SCOPED_DOES_NOT_CONTROL_SAME_INDEX_PRODUCT_COVARIANCE
V40_HARPER_GENERAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_SEQUENCE_LARGE_MODULUS_AND_DISTRIBUTION_HYPOTHESES_MISMATCH
V40_ZHENG_SIMULTANEOUS_AP_DIRECT_ATTACHMENT = STOP_SCOPED_SOURCE_ARRAYS_MODULUS_RANGE_AND_LITERAL_ROW_MISMATCH
V40_PASCADI_SMOOTH_AP_DIRECT_ATTACHMENT = STOP_SCOPED_SMOOTH_TRIPLE_CONVOLUTION_NOT_ORDERED_MASTER_HYBRID_ROW
V40_BFKMM_SHIFTED_CONVOLUTION_DIRECT_ATTACHMENT = STOP_SCOPED_AUTOMORPHIC_COEFFICIENT_AND_SHIFT_FAMILY_MISMATCH
V40_BLOMER_PASCADI_DIRECT_ATTACHMENT = STOP_SCOPED_POST_EMITTER_SEPARABLE_FIXED_MODULUS_ENGINE_NOT_ROW_ENERGY
V40_DIRECT_PRIMARY_SOURCE_FOR_ROW_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V40_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_SUM_Q_ABS_SUM_T_BETA_T_G_Q_T_SQUARED_AT_X_POWER_7_OVER_3_MINUS_KAPPA_FOR_KAPPA_GREATER_THAN_1_OVER_200
V40_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_CONSTANT_RESIDUE_DIRECTION_SELECTED_ROW_BESSEL_PIER_OPEN
V40_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V40_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
```

## 40. V39 后的罗盘：Schatten 收费站已看清，主桥转向 packet energy

V39 对 V38 canonical atomic budget 作 blockwise nuclear/operator duality，得到 exact
curve-test 表达：V38 Schatten gate 等价于对全部 block-contraction test family 的统一
估计。full matrix singular values 又给出不可绕过的绝对质量下界

```text
A_q(d_q) >= lambda_q^(-1)(q||d_q||_1-|sum_r d_q(r)|).
```

因此 scalar cancellation 可以已经发生，而 nuclear atomic budget 仍然很大。V39 再把
所有 generic Schatten endpoints 连成连续谱。仅用 BP 正式 operator theorem 时，
`p=2` 的 admissible energy ceiling 为 `399/200`，`p=4` 降为 `4613/2400`，
`p=infinity` 只剩 `2219/1200`。即使反事实白送所有 ordered blocks 一个最有利的
`S4<=q^(31/32)`，`p=4` 也只有 `773/400`，仍劣于 `p=2`。

所以 primary B bridge 改为 literal packet energy

```text
E_pack=sum_(q,r)|d_q(r)|^2 << x^(2-kappa+o(1)),
kappa>1/200.
```

direct Cauchy 给 `|C_x|<<Q^2 E_pack^(1/2)=x^(5/3-kappa/2+o(1))`；benchmark
`kappa=1/100` 输出 `997/600`，margin `1/400`。V38 Schatten gate不删除，而是降为
必须使用特殊 physical cross-block compression 的第二车道。E/X、terminal A 与 dynamics
C 依次保留。当前仍无 source证明 literal `q`-dependent centered packet energy，故
arithmetic advance 仍为 `NO`。

```text
V39_MAXIMUM_CLAIM = EXACT_BLOCK_PROJECTIVE_DUALITY_ABSOLUTE_MASS_LOWER_BARRIER_AND_GENERIC_SCHATTEN_CONTINUUM_SELECT_DIRECT_PACKET_ENERGY_AS_PRIMARY_OPEN_BRIDGE
V39_ROUTE_ADVANCE = YES
V39_CONDITIONAL_BRIDGE_ADVANCE = YES
V39_ARITHMETIC_ADVANCE = NO
V39_FIXED_ATOM_CREDIT = 0
V39_STRICT_1_OVER_400 = UNPAID
V39_L2 = NONE
V39_TPC_207_TRIGGER = false
V39_NUMBERED_RELEASE = NO
V39_DERIVATION_STATUS = COHERENT_AFTER_BLOCK_NUCLEAR_DUALITY_MASS_BARRIER_CERTIFIED_AND_OPTIMISTIC_SCHATTEN_COMPARISON
V39_ASSUMPTION_POLICY = PACKET_ENERGY_AND_SPECIALIZED_SCHATTEN_COMPRESSION_REMAIN_EXPLICIT_OPEN_THEOREMS
V39_SELECTED_RESEARCH_ROUTE = P2_DIRECT_PACKET_ENERGY_FIRST__K_SPECIALIZED_SCHATTEN_SECOND__E_THIRD__X_FOURTH__A_TERMINAL_AFTER_B__C_RESERVE
V39_V38_CANONICAL_EMITTER = RETAINED_EXACT_ZERO_REMAINDER
V39_BLOCK_PROJECTIVE_DUALITY = PROVED_EXACT_PRODUCT_OF_BLOCK_OPERATOR_BALLS
V39_BLOCK_DUAL_CURVE_TEST = PROVED_EXACT_PHI_Q_T_ON_R_AND_R_INVERSE
V39_PHYSICAL_DUAL_EXPANSION = PROVED_EXACT_BETA_TIMES_CENTERED_G_TIMES_PHI
V39_ATOMIC_ABSOLUTE_MASS_LOWER_BARRIER = PROVED_LAMBDA_INVERSE_TIMES_Q_D_L1_MINUS_ABS_SUM_D
V39_SCALAR_ZERO_ATOMIC_ZERO_IMPLICATION = STOP_SCOPED_Q5_ALTERNATING_PACKET_COUNTEREXAMPLE
V39_CANONICAL_SCHATTEN_GATE = RETAINED_OPEN_SPECIALIZED_NON_GENERIC_COMPRESSION_LANE
V39_BLOMER_PASCADI_FORMAL_INTERFACE = SOURCE_BACKED_SEPARABLE_BILINEAR_OPERATOR_NORM_Q_MINUS_1_OVER_32
V39_BLOMER_PASCADI_FOURTH_MOMENT = PROOF_ARCHITECTURE_NOT_STANDALONE_ALL_BLOCK_S4_THEOREM
V39_OPTIMISTIC_S4_POLICY = COUNTERFACTUAL_GRANT_FOR_ROUTE_STRESS_TEST_NO_THEOREM_CREDIT
V39_CERTIFIED_SCHATTEN_ALPHA = 71_OVER_32_MINUS_7_OVER_16P
V39_CERTIFIED_SCHATTEN_ENERGY_CEILING = 2219_OVER_1200_PLUS_7_OVER_24P
V39_CERTIFIED_P2_ENERGY_CEILING = 399_OVER_200
V39_CERTIFIED_P4_ENERGY_CEILING = 4613_OVER_2400
V39_CERTIFIED_PINFINITY_ENERGY_CEILING = 2219_OVER_1200
V39_OPTIMISTIC_S4_P4_ENERGY_CEILING = 773_OVER_400
V39_GENERIC_SCHATTEN_OPTIMUM = PROVED_P_EQUALS_2_EVEN_AFTER_OPTIMISTIC_S4_GRANT
V39_PACKET_ENERGY = SUM_Q_SUM_R_ABS_D_Q_R_SQUARED
V39_DIRECT_PACKET_ENERGY_CAUCHY = PROVED_Q_SQUARED_TIMES_PACKET_ENERGY_SQUARE_ROOT
V39_PACKET_ENERGY_GATE = OPEN_CONJECTURE_X_POWER_2_MINUS_KAPPA
V39_PACKET_ENERGY_KAPPA_THRESHOLD = KAPPA_STRICTLY_GREATER_THAN_1_OVER_200
V39_PACKET_ENERGY_CONDITIONAL_OUTPUT = X_POWER_5_OVER_3_MINUS_KAPPA_OVER_2
V39_PACKET_ENERGY_ENDPOINT_MARGIN = KAPPA_OVER_2_MINUS_1_OVER_400
V39_SAMPLE_KAPPA = 1_OVER_100
V39_SAMPLE_OUTPUT = 997_OVER_600
V39_SAMPLE_ENDPOINT_MARGIN = 1_OVER_400
V39_KERR_SHPARLINSKI_WU_XI_DIRECT_ATTACHMENT = STOP_SCOPED_SEPARABLE_BILINEAR_ARRAYS_NO_LITERAL_Q_DEPENDENT_PACKET_ENERGY
V39_KOWALSKI_MICHEL_SAWIN_DIRECT_ATTACHMENT = STOP_SCOPED_SEPARABLE_HYPER_KLOOSTERMAN_BILINEAR_WRONG_MATRIX_AND_PACKET_NORM
V39_HARPER_GENERAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_Q_INDEPENDENT_SEQUENCE_MODULUS_RANGE_AND_DISTRIBUTION_HYPOTHESES_MISMATCH
V39_DIRECT_PRIMARY_SOURCE_FOR_PACKET_ENERGY_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V39_ROUTE_E = RETAINED_OPEN_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800
V39_ROUTE_X = RETAINED_OPEN_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200
V39_TERMINAL_A = OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B
V39_DYNAMICS_C = RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN
V39_NEXT_THEOREM = DIRECT_LITERAL_Q_DEPENDENT_CENTERED_PACKET_ENERGY_WITH_KAPPA_1_OVER_100_BENCHMARK
V39_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_SUM_Q_R_ABS_D_Q_R_SQUARED_BY_X_POWER_2_MINUS_KAPPA_FOR_KAPPA_GREATER_THAN_1_OVER_200
V39_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_CANONICAL_EMITTER_BUILT_PACKET_ENERGY_PIER_SELECTED_SCHATTEN_TOLL_EXPOSED
V39_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V39_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
```

## 39. V38 后的罗盘：canonical emitter 已建，Schatten aggregate 成为单一红叉

V38 对 V37 packet 做 final-scalar residue regrouping，定义
`M_q(m,n)=q^(-2)sum_r d_q(r)e_q(-mr-n rbar)`。双重 additive orthogonality、唯一
zero-axis 的 `lambda_q=(q^2-q+1)/q^2` 修正，以及 balanced-block SVD，给出一个
zero-remainder、every-entry-exactly-once、`a=1` 的 BP-admissible canonical emitter。
因此“找一个 emitter”不再是 open construction。

当前 K lane 的唯一主红叉是

~~~text
sum_q q^2/lambda_q sum_(I,J)||M_q[I,J]||_(S1)
  << x^(5/3+o(1))Q^omega,
omega<19/800.
~~~

BP cell engine随后给 `Q^(-1/32)`；benchmark `omega=1/100` 的输出为
`3983/2400`，margin `11/2400`。generic block Schatten/Frobenius baseline会损失
`Q^(1/4)`，把 packet energy 绕道 BP 反而比 direct Cauchy 多付 `x^(7/96)`；故不能
把普通 `L2` 换名成新 theorem。主路线为 direct Schatten aggregate first，E/X 为
独立备线，terminal A 与 dynamics C 均未支付。

~~~text
V38_MAXIMUM_CLAIM = EXACT_CANONICAL_FOURIER_KLOOSTERMAN_BALANCED_BLOCK_SVD_EMITTER_PLUS_OPEN_PHYSICAL_SCHATTEN_AGGREGATE_AND_SOURCE_BACKED_BP_CELL_ENGINE
V38_ROUTE_ADVANCE = YES
V38_CONDITIONAL_BRIDGE_ADVANCE = YES
V38_ARITHMETIC_ADVANCE = NO
V38_FIXED_ATOM_CREDIT = 0
V38_STRICT_1_OVER_400 = UNPAID
V38_L2 = NONE
V38_TPC_207_TRIGGER = false
V38_NUMBERED_RELEASE = NO
V38_DERIVATION_STATUS = COHERENT_AFTER_EXACT_SCALAR_RECOLLAPSE_DOUBLE_ORTHOGONALITY_ZERO_AXIS_REMOVAL_AND_BLOCK_SVD
V38_ASSUMPTION_POLICY = ONLY_CANONICAL_PHYSICAL_SCHATTEN_AGGREGATE_IS_OPEN_AND_NEVER_PROMOTED
V38_SELECTED_RESEARCH_ROUTE = K_CANONICAL_SCHATTEN_AGGREGATE_FIRST__E_SECOND__X_THIRD__A_TERMINAL_AFTER_B__C_RESERVE
V38_V37_CENTERED_PACKET = RETAINED_EXACT_WITH_FULL_BACKGROUND_AND_DELETED_DIAGONAL
V38_PHYSICAL_RESIDUE_VECTOR = PROVED_EXACT_FINAL_SCALAR_REGROUPING
V38_CANONICAL_FOURIER_KLOOSTERMAN_MATRIX = PROVED_EXACT_DOUBLE_ADDITIVE_ORTHOGONALITY
V38_ZERO_AXIS_SELF_RETURN = PROVED_EXACT_LAMBDA_Q_FACTOR
V38_ZERO_AXIS_FACTOR = LAMBDA_Q_EQUALS_Q_SQUARED_MINUS_Q_PLUS_ONE_OVER_Q_SQUARED
V38_PRIME_COPRIMALITY_AFTER_ZERO_REMOVAL = PROVED_EXACT_ONLY_ZERO_ZERO_EXCLUDED
V38_BALANCED_FREQUENCY_PARTITION = PROVED_EXACT_CONSECUTIVE_BLOCKS_OF_LENGTH_ASYMPTOTIC_SQRT_Q
V38_BLOCK_SVD = PROVED_EXACT_RANK_ONE_BP_ARRAY_DECOMPOSITION
V38_CANONICAL_SCALAR_EMITTER = PROVED_EXACT_ZERO_REMAINDER
V38_EXACTLY_ONCE_POLICY = FINAL_PHYSICAL_SCALAR_AND_EVERY_MATRIX_ENTRY_EXACTLY_ONCE
V38_TEMPLATE_LABEL_RELAXATION = VALID_ONLY_AFTER_V35_V36_FINAL_SCALAR_RECOLLAPSE_NOT_FOR_LOCAL_CARRIER
V38_CELL_TRIVIAL_SCALE = Q_SQUARED_OVER_LAMBDA_Q_TIMES_SINGULAR_VALUE
V38_CANONICAL_ATOMIC_BUDGET = Q_SQUARED_OVER_LAMBDA_Q_TIMES_SUM_BLOCK_SCHATTEN_ONE
V38_CANONICAL_SCHATTEN_GATE = OPEN_CONJECTURE_AGGREGATE_X_POWER_5_OVER_3_TIMES_Q_POWER_OMEGA
V38_PACKET_OVERHEAD_THRESHOLD = OMEGA_STRICTLY_LESS_THAN_19_OVER_800
V38_BLOMER_PASCADI_CELL_ENGINE = SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_AFTER_EXACT_EMISSION
V38_CONDITIONAL_OUTPUT = X_POWER_53_OVER_32_PLUS_OMEGA_OVER_3
V38_CONDITIONAL_ENDPOINT_MARGIN = 19_OVER_2400_MINUS_OMEGA_OVER_3
V38_SAMPLE_OMEGA = 1_OVER_100
V38_SAMPLE_OUTPUT = 3983_OVER_2400
V38_SAMPLE_ENDPOINT_MARGIN = 11_OVER_2400
V38_FULL_MATRIX_SINGULAR_VALUES = PROVED_EXACT_ABS_D_R_OVER_Q
V38_FULL_MATRIX_FROBENIUS = PROVED_EXACT_Q_INVERSE_TIMES_D_L2
V38_GENERIC_BLOCK_SCHATTEN_BASELINE = Q_POWER_MINUS_1_OVER_4_TIMES_D_L2
V38_GENERIC_ATOMIC_L2_BASELINE = Q_POWER_7_OVER_4_TIMES_D_L2
V38_GENERIC_ATOMIC_L1_BASELINE = Q_POWER_3_OVER_2_TIMES_D_L1
V38_PACKET_ENERGY_TO_ATOMIC = PROVED_Q_POWER_9_OVER_4_TIMES_ENERGY_SQUARE_ROOT
V38_PACKET_ENERGY_REQUIRED_BY_GENERIC_ATOMIC_ROUTE = X_POWER_11_OVER_6_PLUS_2_OMEGA_OVER_3
V38_SAMPLE_PACKET_ENERGY_EXPONENT = 46_OVER_25
V38_DIRECT_PACKET_ENERGY_CAUCHY = PROVED_Q_SQUARED_TIMES_ENERGY_SQUARE_ROOT
V38_DIRECT_PACKET_ENERGY_OUTPUT = X_POWER_19_OVER_12_PLUS_OMEGA_OVER_3
V38_PACKET_ENERGY_VIA_BP = STOP_SCOPED_GENERIC_BLOCK_LOSS_Q_1_OVER_4_EXCEEDS_BP_GAIN_Q_1_OVER_32
V38_PACKET_ENERGY_BP_OVERPAY = X_POWER_7_OVER_96
V38_HARPER_GENERAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_Q_INDEPENDENT_SEQUENCE_Q_RANGE_AND_DISTRIBUTION_HYPOTHESES_MISMATCH
V38_LEWKO_VARIATIONAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_PRIME_COUNTING_ONE_SEQUENCE_WRONG_PACKET_AND_NORM
V38_HIEU_SHORT_INTERVAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_SINGLE_LAMBDA_SEQUENCE_NO_BETA_CENTERED_INVERSE_BLOCK
V38_DIRECT_PRIMARY_SOURCE_FOR_CANONICAL_SCHATTEN_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V38_ROUTE_E = RETAINED_OPEN_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800
V38_ROUTE_X = RETAINED_OPEN_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200
V38_TERMINAL_A = OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B
V38_DYNAMICS_C = RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN
V38_NEXT_THEOREM = DIRECT_LITERAL_CANONICAL_BLOCK_SCHATTEN_AGGREGATE_WITH_OMEGA_1_OVER_100_BENCHMARK
V38_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_THE_CANONICAL_PHYSICAL_BLOCK_SCHATTEN_AGGREGATE_WITH_OMEGA_LESS_THAN_19_OVER_800
V38_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_K_LANE_CANONICAL_EMITTER_BUILT_ATOMIC_PIER_OPEN
V38_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V38_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
~~~

## 38. V37 后的罗盘：K 车道改成可容忍损耗的 shift-packet 桥墩

V37 没有宣称跨过 Bridge A；它把 V36 的 hard pier改成可证伪的工程合同。对每个
prime `q` 与 unit `t`，ratio core精确变成 centered residue packet

~~~text
q beta(t) [F_(q,t)(0)-average_(b!=-t)F_(q,t)(b)].
~~~

有效 occupancy为 `H/Q=Q^(31/32)`。若 exactly-once BP-admissible emitter的
aggregate source-native trivial budget只损失 `Q^omega`，则 BP fixed-modulus
cell saving之后的输出为 `x^(53/32+omega/3+o(1))`。因此 K lane真正允许的施工
误差是

~~~text
omega<19/800,
margin=19/2400-omega/3.
~~~

V36 的零损耗 `omega=0` 只是充分特例。generic per-shift Cauchy只给
`rho=31/64`，输出 `x^(349/192)`，所以不能用“随机平方根消去”冒充 emitter。
主路线继续是 K first、E second、X third；任一 B lane闭合后仍须独立支付 terminal A，
dynamics C仍是 reserve。

~~~text
V37_MAXIMUM_CLAIM = EXACT_CENTERED_RESIDUE_PACKETIZATION_PLUS_LOSS_BUDGETED_K_ROUTE_THRESHOLD_AND_SOURCE_BACKED_CELL_ENGINE_AFTER_CONJECTURAL_EMISSION
V37_ROUTE_ADVANCE = YES
V37_CONDITIONAL_BRIDGE_ADVANCE = YES
V37_ARITHMETIC_ADVANCE = NO
V37_FIXED_ATOM_CREDIT = 0
V37_STRICT_1_OVER_400 = UNPAID
V37_L2 = NONE
V37_TPC_207_TRIGGER = false
V37_NUMBERED_RELEASE = NO
V37_DERIVATION_STATUS = COHERENT_AFTER_EXACT_PACKETIZATION_AND_LOSS_BUDGETING
V37_ASSUMPTION_POLICY = PACKET_EMITTER_IS_EXPLICIT_CONJECTURE_AND_NEVER_PROMOTED_TO_THEOREM
V37_SELECTED_RESEARCH_ROUTE = K_LOSS_BUDGETED_PACKET_EMITTER_FIRST__E_SECOND__X_THIRD__A_TERMINAL_AFTER_B__C_RESERVE
V37_V36_BINARY_CORE = RETAINED_EXACT_OFF_DIAGONAL_COPRIME_RATIO_COVARIANCE
V37_CENTERED_RESIDUE_PACKET = PROVED_EXACT_BINARY_CORE_PACKET_IDENTITY
V37_UNIT_TO_DIFFERENCE_BIJECTION = PROVED_EXACT_A_TO_B_EQUALS_A_MINUS_ONE_TIMES_T
V37_PACKET_DIAGONAL = PROVED_EXACT_ONLY_B_ZERO_ELL_ZERO_ROW_DELETED
V37_PACKET_BACKGROUND = PROVED_EXACT_ALL_B_NOT_EQUAL_MINUS_T_REQUIRED
V37_CONSTANT_PACKET = PROVED_EXACT_ANNIHILATED
V37_SCHWARTZ_TAIL = PROVED_NEGLIGIBLE_AFTER_H_X_EPSILON_TRUNCATION
V37_SHIFT_OCCUPANCY = Q_POWER_31_OVER_32
V37_RAW_POSITIVE_COMPENSATING_TRIANGLE = X_POWER_191_OVER_96
V37_PACKET_EMITTER_STATUS = OPEN_CONJECTURE_BP_ADMISSIBLE_EXACTLY_ONCE_JOINT_PACKET
V37_PACKET_EXACTLY_ONCE_POLICY = PHYSICAL_BETA_W_K_PRIME_SHELL_ZERO_DELETION_AND_ALL_TEMPLATE_LABELS_PRESERVED
V37_PACKET_PRE_CELL_BUDGET = X_POWER_5_OVER_3_TIMES_Q_POWER_OMEGA
V37_PACKET_EFFECTIVE_GAIN = Q_POWER_MINUS_31_OVER_32_PLUS_OMEGA
V37_PACKET_OVERHEAD_THRESHOLD = OMEGA_STRICTLY_LESS_THAN_19_OVER_800
V37_BLOMER_PASCADI_CELL_ENGINE = SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_AT_CRITICAL_SQUARE_ROOT_RANGE
V37_CONDITIONAL_OUTPUT = X_POWER_53_OVER_32_PLUS_OMEGA_OVER_3
V37_CONDITIONAL_DELTA = 1_OVER_96_MINUS_OMEGA_OVER_3
V37_CONDITIONAL_ENDPOINT_MARGIN = 19_OVER_2400_MINUS_OMEGA_OVER_3
V37_GENERAL_GAIN_CONDITION = RHO_PLUS_GAMMA_STRICTLY_GREATER_THAN_781_OVER_800
V37_WITH_BP_RHO_THRESHOLD = RHO_STRICTLY_GREATER_THAN_189_OVER_200
V37_V36_ZERO_LOSS_COMPILER = SUFFICIENT_SPECIAL_CASE_OMEGA_ZERO_NOT_NECESSARY
V37_ELL_CAUCHY = STOP_SCOPED_EFFECTIVE_RHO_31_OVER_64_INSUFFICIENT
V37_ELL_CAUCHY_OUTPUT = X_POWER_349_OVER_192
V37_ELL_CAUCHY_ENDPOINT_DEFICIT = 737_OVER_4800
V37_PACKET_COMPILER_NOT_RANDOM_CANCELLATION = PROVED_STATUS_FIREWALL
V37_GLOBAL_RANDOM_PHASE_BENCHMARK = RETAINED_HEURISTIC_ONLY_X_POWER_223_OVER_192
V37_BLOMER_PASCADI_DIRECT_ATTACHMENT = STOP_SCOPED_REQUIRES_PRIOR_PHYSICAL_PACKET_EMISSION_AND_AGGREGATE_NORM
V37_PASCADI_FREQUENCY_CONCENTRATION_DIRECT_ATTACHMENT = STOP_SCOPED_ASSUMPTION14_AND_SMOOTH_LEVEL_SEQUENCE_NOT_VERIFIED_FOR_LITERAL_PACKET
V37_WRIGHT_PARTIALLY_FIXED_MODULUS_DIRECT_ATTACHMENT = STOP_SCOPED_WRONG_DISPERSION_ARRAYS_AND_NO_CENTERED_PACKET_REASSEMBLY
V37_BETTIN_CHANDEE_DIRECT_ATTACHMENT = STOP_SCOPED_LOCAL_TRILINEAR_FRACTION_NO_PRIME_SHELL_PACKET_NORM
V37_BLOMER_RISAGER_SHPARLINSKI_DIRECT_ATTACHMENT = STOP_SCOPED_SPECIFIED_TRIPLE_MODULAR_INVERSE_FAMILY_WRONG_PHYSICAL_COEFFICIENTS
V37_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V37_ROUTE_E = RETAINED_OPEN_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800
V37_ROUTE_X = RETAINED_OPEN_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200
V37_TERMINAL_A = OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B
V37_DYNAMICS_C = RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN
V37_NEXT_THEOREM = EXACTLY_ONCE_BP_ADMISSIBLE_CENTERED_SHIFT_PACKET_EMITTER_WITH_AGGREGATE_OVERHEAD_OMEGA_LT_19_OVER_800
V37_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_THE_BP_ADMISSIBLE_PACKET_EMITTER_AND_AGGREGATE_NORM_WITH_OMEGA_LT_19_OVER_800
V37_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_K_LANE_LOSS_BUDGETED_PIER_MARKED
V37_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V37_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
~~~

## 37. V36 后的罗盘：同一红叉铺成 E/K/X 三条条件车道

V36 没有跨过 Bridge A，但把 V35 three-array presentation精确重合并为 binary
off-diagonal ratio covariance，并给出 compulsory diagonal-subtracted hybrid-character
normal form。当前不再押注一条唯一技术路线：

- K 路优先：先猜想并构造 collective \(Q^{-31/32}\) emitter/reassembly，再接
  Blomer--Pascadi source-backed \(Q^{-1/32}\) fixed-modulus cell engine；
- E 路备用：直接证明 whole tagged residual energy，\(\sigma<13/4800\)；
- X 路备用：证明 joint hybrid-character decoupling，\(\kappa>403/1200\)。

三条 lane 是 exact conditional OR，不是三份可相加的 theorem credit。任何一条若被
真实证明，都只支付 B；terminal A仍 open，dynamics C仍 reserve。random-phase
\(x^{223/192+o(1)}\) 只作 heuristic，arithmetic advance仍为 NO。

~~~text
V36_MAXIMUM_CLAIM = EXACT_PROPER_FACTOR_RECOLLAPSE_TO_BINARY_OFF_DIAGONAL_HYBRID_CHARACTER_COVARIANCE_PLUS_ONE_OF_THREE_CONDITIONAL_GATE_B_COMPILER_AND_EXPLICIT_HEURISTIC_CHARTER
V36_ROUTE_ADVANCE = YES
V36_CONDITIONAL_BRIDGE_ADVANCE = YES
V36_ARITHMETIC_ADVANCE = NO
V36_FIXED_ATOM_CREDIT = 0
V36_STRICT_1_OVER_400 = UNPAID
V36_L2 = NONE
V36_TPC_207_TRIGGER = false
V36_NUMBERED_RELEASE = NO
V36_DERIVATION_STATUS = COHERENT_AFTER_REFRAMING_AND_EXPLICIT_EXTRA_ASSUMPTIONS
V36_ASSUMPTION_POLICY = CONJECTURES_EXPLICIT_AND_NEVER_PROMOTED_TO_THEOREMS
V36_SELECTED_RESEARCH_ROUTE = K_COLLECTIVE_COMPILER_FIRST__E_ENERGY_SECOND__X_CHARACTER_THIRD__A_TERMINAL_AFTER_B__C_DYNAMICS_RESERVE
V36_V35_CORE = RETAINED_EXACT_PRIME_ONLY_ZERO_DELETED_COPRIME_RATIO_CORE
V36_PROPER_FACTOR_RECOLLAPSE = PROVED_EXACT_SUM_OCCURRENCES_BACK_TO_BETA_OF_T
V36_BINARY_RATIO_CORE = PROVED_EXACT_TWO_ARRAY_OFF_DIAGONAL_FORM
V36_HYBRID_CHARACTER_INVERSION = PROVED_EXACT_FOURIER_CHARACTER_NORMAL_FORM
V36_CHARACTER_DIAGONAL_SUBTRACTION = PROVED_EXACT_Z_Q_REQUIRED
V36_ONE_OF_THREE_COMPILER = PROVED_EXACT_CONDITIONAL_OR_GATE
V36_ROUTE_E_STATUS = OPEN_CONJECTURE_WHOLE_OBJECT_WEIGHTED_RESIDUAL_ENERGY
V36_ROUTE_E_INPUT = N_E_LE_X_POWER_1_PLUS_SIGMA_WITH_SIGMA_LT_13_OVER_4800
V36_ROUTE_E_DELTA = 1_OVER_192_MINUS_SIGMA
V36_ROUTE_E_ENDPOINT_MARGIN = 13_OVER_4800_MINUS_SIGMA
V36_ROUTE_K0_STATUS = OPEN_CONJECTURE_COLLECTIVE_Q_ELL_EMITTER_AND_REASSEMBLY
V36_ROUTE_K0_STRUCTURAL_GAIN = Q_POWER_MINUS_31_OVER_32
V36_ROUTE_K1_STATUS = SOURCE_BACKED_FIXED_MODULUS_CELL_ENGINE_AFTER_EXACT_EMISSION
V36_ROUTE_K1_CELL_GAIN = Q_POWER_MINUS_1_OVER_32
V36_ROUTE_K_TOTAL_GAIN = Q_POWER_MINUS_1_EQUALS_X_POWER_MINUS_1_OVER_3
V36_ROUTE_K_DELTA = 1_OVER_96
V36_ROUTE_K_ENDPOINT_MARGIN = 19_OVER_2400
V36_ROUTE_X_STATUS = OPEN_CONJECTURE_JOINT_HYBRID_CHARACTER_DECOUPLING
V36_ROUTE_X_BASELINE = X_POWER_2_PLUS_O1_FROM_SEPARATE_LARGE_SIEVE_CAUCHY
V36_ROUTE_X_REQUIRED_KAPPA = STRICTLY_GREATER_THAN_403_OVER_1200
V36_ROUTE_X_DELTA = KAPPA_MINUS_1_OVER_3
V36_ROUTE_X_ENDPOINT_MARGIN = KAPPA_MINUS_403_OVER_1200
V36_RANDOM_PHASE_BENCHMARK = HEURISTIC_ONLY_X_POWER_223_OVER_192
V36_RANDOM_PHASE_GAP_TO_X_5_OVER_3 = 97_OVER_192
V36_SEPARATE_MARGINAL_LARGE_SIEVE = STOP_SCOPED_X_POWER_2_DEFICIT_403_OVER_1200
V36_FIXED_Q_TRIANGLE = STOP_SCOPED_REQUIRES_Q_POWER_MINUS_31_OVER_32_MINUS_3_DELTA_BEFORE_MODULUS_SUM
V36_BLOMER_PASCADI_CELL_ENGINE = SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_AT_CRITICAL_FIXED_MODULUS_RANGE
V36_BLOMER_PASCADI_DIRECT_ATTACHMENT = STOP_SCOPED_NO_COLLECTIVE_Q_ELL_EMITTER_COEFFICIENT_COMPILER_OR_REASSEMBLY
V36_FOUVRY_SHPARLINSKI_XI_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_PRIME_SHORT_VARIABLES_WRONG_CROSS_WEIGHT_AND_NO_MODULUS_REASSEMBLY
V36_DONG_ROBLES_ZEINDLER_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_BILINEAR_FRACTION_NO_PHYSICAL_JOINT_COVARIANCE
V36_RUNBO_LI_DIRECT_ATTACHMENT = STOP_SCOPED_SPECIAL_HARMAN_MAJORANTS_AND_MODULUS_FORMS_WRONG_SIGNED_OBJECT
V36_TERMINAL_A = OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B
V36_DYNAMICS_C = RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN
V36_HEURISTIC_DOES_NOT_IMPLY_ARITHMETIC_ADVANCE = PROVED_STATUS_FIREWALL
V36_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V36_NEXT_THEOREM = COLLECTIVE_Q_POWER_MINUS_31_OVER_32_DETERMINANT_EMITTER_OR_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800_OR_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200
V36_FIRST_FATAL = NO_LITERAL_THEOREM_SUPPLIES_ANY_ONE_OF_THE_THREE_CONJECTURAL_BRIDGE_INPUTS
V36_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_THREE_CONDITIONAL_LANES_MARKED
V36_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
~~~

地图位置仍是解析消去岛通向 Bridge A 的红叉。不同之处是现在有三条标明施工状态的
车道：K 有最后一段 source-backed 桥面，E 最短，X object最干净；三条都还缺关键桥墩。

## 36. V35 后的罗盘：endpoint 与坏模数行已清空，红叉缩成 coprime ratio core

V35 继续沿 B -> A -> C 大路推进，但仍未跨过 Bridge A。collapsed marginal现在
有 endpoint-free proper-factor identity：

~~~text
beta_raw(t)=sum_(dk=t,d>=2,k>=2)mu(d)omega_x(d,k),
|omega_x(d,k)|<=1.
~~~

d=1、k=1 coefficients均为零，故 prime rows为空。对 prime unit rows，
q 1_(u=dk)-1=q u1(u inverse(dk);q)+1/(q-1)，所以 V34 numerator精确分成
coprime centered core、unit-principal与 nonunit三项。后两项均为
x^(53/32+o(1))，到 strict numerator endpoint仍有 19/2400 margin。

当前唯一红叉是保留 u!=dk 的 prime-only three-array ratio core。写 n=u+2，
它是 n=dk+2 (mod q)、physical Lambda(n)-b(n-2) 与 short difference共同组成的
fixed-shift-two frame。所需 theorem仍是 x^(5/3-delta)、delta>1/400。Drappeau
在 R=1 的 unit kernel局部同形，但 theorem量词是 binary fixed product/all moduli，
不能接受第三个 physical array、prime selector和 zero deletion；其他已筛来源亦无
literal attachment。

~~~text
V35_MAXIMUM_CLAIM = EXACT_ENDPOINT_FREE_PROPER_FACTOR_AND_PAID_NONUNIT_PRINCIPAL_REDUCTION_TO_ZERO_DELETED_COPRIME_FIXED_SHIFT_TWO_TERNARY_RATIO_CORE
V35_ROUTE_ADVANCE = YES
V35_ARITHMETIC_ADVANCE = NO
V35_FIXED_ATOM_CREDIT = 0
V35_STRICT_1_OVER_400 = UNPAID
V35_L2 = NONE
V35_TPC_207_TRIGGER = false
V35_NUMBERED_RELEASE = NO
V35_SELECTED_RESEARCH_ROUTE = B_COPRIME_FIXED_SHIFT_RATIO_CORE_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK
V35_V34_COMPENSATED_FRAME = RETAINED_EXACT_ZERO_DELETED_ONE_OUTER_SIGNED_SCALAR
V35_PROPER_FACTOR_IDENTITY = PROVED_EXACT_BETA_EQUALS_SUM_MU_TIMES_OMEGA
V35_D_EQ_1_ENDPOINT = PROVED_EXACT_ZERO_COEFFICIENT
V35_K_EQ_1_ENDPOINT = PROVED_EXACT_ZERO_COEFFICIENT
V35_PROPER_FACTOR_SUPPORT = PROVED_EXACT_D_AND_K_AT_LEAST_2
V35_PROPER_FACTOR_WEIGHT = PROVED_EXACT_PIECEWISE_NEG_LOG_D_OR_POS_LOG_K_OVER_LOG_DK
V35_PROPER_FACTOR_WEIGHT_BOUND = PROVED_EXACT_ABSOLUTE_VALUE_AT_MOST_1
V35_PRIME_ROWS = PROVED_EXACT_EMPTY
V35_UNIT_RATIO_VECTOR = PROVED_EXACT_Q_U1_PLUS_ONE_OVER_Q_MINUS_1
V35_UNIT_CHARACTER_EXPANSION = PROVED_EXACT_NONPRINCIPAL_CHARACTER_AVERAGE
V35_EXACT_DECOMPOSITION = PROVED_EXACT_D_EQUALS_CORE_PLUS_PRINCIPAL_PLUS_NONUNIT
V35_NONUNIT_PAYMENT = PROVED_ABSOLUTE_X_POWER_53_OVER_32_PLUS_O1
V35_UNIT_PRINCIPAL_PAYMENT = PROVED_ABSOLUTE_X_POWER_53_OVER_32_PLUS_O1
V35_PAID_REMAINDER_E_EXPONENT = X_POWER_95_OVER_96_PLUS_O1
V35_PAID_REMAINDER_NUMERATOR_SAVING = 1_OVER_96
V35_PAID_REMAINDER_ENDPOINT_MARGIN = 19_OVER_2400
V35_COPRIME_CORE = PROVED_EXACT_PRIME_ONLY_ZERO_DELETED_THREE_ARRAY_RATIO_FRAME
V35_FIXED_SHIFT_TWO_FORM = PROVED_EXACT_N_CONGRUENT_DK_PLUS_2
V35_CORE_NUMERATOR_TARGET = X_POWER_5_OVER_3_MINUS_DELTA_PLUS_O1
V35_REQUIRED_DELTA = STRICTLY_GREATER_THAN_1_OVER_400
V35_CORE_E_EXPONENT = X_POWER_1_MINUS_DELTA_PLUS_O1
V35_LOCAL_CARRIER_PAYMENT = RETAINED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1
V35_LOCAL_CARRIER_ENDPOINT_MARGIN = 121_OVER_9600
V35_COMBINED_B_MARGIN = MIN_DELTA_MINUS_1_OVER_400_AND_19_OVER_2400_AND_121_OVER_9600
V35_FULL_DIAGONAL_REINSERTION = STOP_SCOPED_CIRCULAR_L_PR_TIMES_PHYSICAL_SCALAR
V35_CORE_DIAGONAL_CORRECTION = STOP_SCOPED_ABSOLUTE_X_POWER_5_OVER_3
V35_RAW_POSITIVE_COMPENSATION_TRIANGLE = STOP_SCOPED_X_POWER_191_OVER_96
V35_DRAPPEAU_UNIT_KERNEL = MATCHES_U1_ONLY_AT_R_EQUALS_1_ON_PRIME_UNITS
V35_DRAPPEAU_DIRECT_ATTACHMENT = STOP_SCOPED_BINARY_FIXED_PRODUCT_ALL_MODULI_NO_THIRD_PHYSICAL_ARRAY_OR_ZERO_DELETION
V35_FOUVRY_RADZIWILL_DIRECT_ATTACHMENT = STOP_SCOPED_BINARY_FIXED_RESIDUE_WRONG_OBJECT_AND_SUBPOWER_OUTPUT
V35_WRIGHT_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_RESIDUE_SIEGEL_WALFISZ_ARRAY_NO_MOVING_RATIO
V35_BETTIN_CHANDEE_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_DETERMINANT_NO_COLLECTIVE_Q_ELL_REASSEMBLY
V35_BETTIN_CHANDEE_PER_SHIFT_TRIANGLE_EXPONENT = 943_OVER_480
V35_BETTIN_CHANDEE_PER_SHIFT_TRIANGLE_DEFICIT = 721_OVER_2400
V35_BAZIN_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_MARGINAL_NO_PHYSICAL_PRODUCT
V35_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V35_NEXT_THEOREM = DELTA_GT_1_OVER_400_POWER_SAVING_FOR_PRIME_ONLY_ZERO_DELETED_THREE_ARRAY_FIXED_SHIFT_TWO_RATIO_CORE
V35_FIRST_FATAL = NO_BINARY_SOURCE_PARAMETERIZATION_PRESERVES_Q_INDEPENDENT_COEFFICIENTS_PRIME_ONLY_ZERO_DELETION_AND_PHYSICAL_THIRD_ARRAY
V35_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
V35_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
~~~

路线图位置没有变化：仍在解析消去岛通向 Bridge A 的红叉处。变化的是红叉已经不再
包含 endpoint、prime、nonunit或 principal rows；下一关只打 coprime fixed-shift
ratio core。arithmetic advance=NO、atom=0、strict 1/400=UNPAID、
L2=NONE、TPC-207=false。


## 35. V34 后的罗盘：local carrier scalar 已付，红叉缩成 compensated prime frame

V34 没有跨过 Bridge A，但把 Gate B 的 theorem statement进一步收窄。V33 marginal
精确等于

~~~text
beta_raw(t)=Lambda(t)/log(t)+sum_(d|t,d^400>x^133)mu(d)
           =rho(t)+sum_(dk=t,k>=2,d^400>x^133)mu(d),
rho(t)=Lambda(t)/log(t)+mu(t), rho(p)=0.
~~~

V29 已给 `|E(Mloc)|,|J(Mloc)|<<x^(1891/1920+o(1))`，故

~~~text
E(e)=E(r)-E(Mloc)
~~~

允许新 B theorem直接作用在 collapsed scalar `r`，无需 occurrence label。对
`Q=x^(1/3)`、`H=x^(21/32)`，唯一选中目标为

~~~text
D=sum_(q prime,Q<q<=2Q) sum_(t!=u)
  beta_raw(t) w^(z)(u) hatpsi_+((u-t)/H)
  (q 1_(u=t mod q)-1),
|D|<<x^(5/3-delta+o(1)), delta>1/400.
~~~

这给任意 `eta_B<min(delta-1/400,121/9600)`。Bazin在 actual frame只给单
marginal exponent `75/64`，没有 physical second factor；MRT/Evans/MRSTT II也
没有 literal all-frame power theorem。路线仍是 `B -> A -> C`，但当前红叉不再是
whole occurrence-native mean square，而是一个 signed compensated scalar covariance。

~~~text
V34_MAXIMUM_CLAIM = EXACT_PAID_LOCAL_CARRIER_ELIMINATION_TO_COLLAPSED_COMPENSATED_PRIME_FRAME_COVARIANCE_WITH_STRICT_DELTA_GT_1_OVER_400_GATE
V34_ROUTE_ADVANCE = YES
V34_ARITHMETIC_ADVANCE = NO
V34_FIXED_ATOM_CREDIT = 0
V34_STRICT_1_OVER_400 = UNPAID
V34_L2 = NONE
V34_TPC_207_TRIGGER = false
V34_NUMBERED_RELEASE = NO
V34_SELECTED_RESEARCH_ROUTE = B_DIRECT_COLLAPSED_PRIME_FRAME_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK
V34_BETA_MASTER_MARGINAL = RETAINED_EXACT_V33_LAMBDA_OVER_LOG_MINUS_TRUNCATED_MU_CONV_ONE
V34_BETA_LARGE_DIVISOR_TAIL = PROVED_EXACT_LAMBDA_OVER_LOG_PLUS_MU_ABOVE_CUTOFF
V34_PRIME_DELETED_ENDPOINT = PROVED_EXACT_RHO_EQUALS_LAMBDA_OVER_LOG_PLUS_MU_AND_RHO_P_EQUALS_ZERO
V34_GENUINE_BILINEAR_TAIL = PROVED_EXACT_K_GE_2_D_ABOVE_CUTOFF
V34_LOCAL_CARRIER_E_PAYMENT = RETAINED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1
V34_LOCAL_CARRIER_J_PAYMENT = RETAINED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1
V34_DIRECT_SCALAR_ELIMINATION = PROVED_EXACT_E_OF_E_EQUALS_E_OF_R_MINUS_E_OF_MLOC
V34_OCCURRENCE_LABEL_IN_NEW_B_THEOREM = REMOVED_BY_SEPARATELY_PAID_SCALAR_LOCAL_CARRIER
V34_QOSC_P_REPLACEMENT = STOP_SCOPED_REINTRODUCES_LARGE_OFFZERO_LOCAL_MAIN
V34_V32_QOSC_P_MINUS_L = RETAINED_VALID_STRONGER_ALTERNATIVE
V34_RAMANUJAN_PRIME_VECTOR = PROVED_EXACT_C_Q_EQUALS_Q_DIVISIBILITY_MINUS_ONE
V34_ZERO_DELETED_SMOOTH_CORRELATION = PROVED_EXACT_PHI_H
V34_COMPENSATED_DILATION_FORM = PROVED_EXACT_QK_MINUS_ALL_H
V34_COMPENSATED_PAIR_FORM = PROVED_EXACT_ONE_OUTER_SIGNED_SCALAR
V34_L_PR_NORMALIZATION = X_POWER_2_OVER_3_PLUS_O1
V34_DIRECT_NUMERATOR_TARGET = X_POWER_5_OVER_3_MINUS_DELTA_PLUS_O1
V34_REQUIRED_DELTA = STRICTLY_GREATER_THAN_1_OVER_400
V34_DIRECT_E_R_EXPONENT = X_POWER_1_MINUS_DELTA_PLUS_O1
V34_DIRECT_ENDPOINT_MARGIN = DELTA_MINUS_1_OVER_400
V34_LOCAL_CARRIER_ENDPOINT_MARGIN = 121_OVER_9600
V34_COMBINED_B_MARGIN = MIN_DELTA_MINUS_1_OVER_400_AND_121_OVER_9600
V34_BAZIN_ACTUAL_FRAME_Q = X_POWER_1_OVER_3
V34_BAZIN_ACTUAL_FRAME_THETA = X_POWER_MINUS_21_OVER_32
V34_BAZIN_ACTUAL_FRAME_XI_EXPONENT = 257_OVER_192
V34_BAZIN_ACTUAL_FRAME_ADDITIVE_EXPONENT = 75_OVER_64
V34_BAZIN_TO_DIRECT_COVARIANCE = STOP_SCOPED_ONE_MARGINAL_NO_PHYSICAL_PRODUCT
V34_MRT_TO_DIRECT_COVARIANCE = STOP_SCOPED_LOGARITHMIC_SHIFT_ENERGY_WRONG_COEFFICIENT_AND_FRAME
V34_EVANS_TO_DIRECT_COVARIANCE = STOP_SCOPED_FIXED_E2_ALMOST_ALL_SHIFTS_WRONG_COEFFICIENT
V34_MRSTT_TO_DIRECT_COVARIANCE = STOP_SCOPED_DENSITY_ONE_NO_QUANTITATIVE_FRAME_POWER
V34_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V34_NEXT_THEOREM = DELTA_GT_1_OVER_400_POWER_SAVING_FOR_COLLAPSED_SIEVE_REMAINDER_TIMES_PHYSICAL_HYBRID_IN_COMPENSATED_PRIME_FRAME
V34_FIRST_FATAL = NO_POWER_SAVING_BEYOND_X_5_OVER_3_FOR_COLLAPSED_PHYSICAL_COMPENSATED_PRIME_FRAME
V34_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
V34_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
~~~

V34 是 exact compiler/source-ceiling advance，不是 arithmetic theorem；fixed atom仍为
0、strict `1/400`仍 UNPAID、`L2=NONE`、TPC-207=false。

## 34. V33 后的罗盘：prime-side marginal 已塌缩，联合 local carrier 仍是红叉

V33 没有另造一套 HB decomposition；它在 V19 已冻结的 ordered root-one HB2 rows与
deterministic H2/MASTER route上做 collective aggregation。对
\(x\geq8\)、\(t\in(x/2,x]\cap\mathbb Z\)，精确得到

~~~text
beta_raw_x(t)
 = Lambda(t)/log(t)-sum_(d|t,d^400<=x^133)mu(d).
~~~

因此 prime-side marginal不再是 opaque occurrence sum，而是
\(\Lambda/\log-(\mu_{U_x}*1)\)。Bazin 2607.15137v1 Theorem 8真实接受这个
Type-I/II marginal；但在 V32 natural cell参数上，source advertised additive-tube
route给 norm exponent \(149/128\)，相对 endpoint仍差 \(1549/9600\)。

关键 firewall没有后退。\(x=121,t=77,z=5\) 的两条 MASTER occurrences在 scalar
\(\log7\) marginal中相消，却分别携带 selected groups \(7,11\)，且
\(\Delta_{7,5}(5)=-35/36\)、\(\Delta_{11,5}(5)=11/100\)。所以 marginal theorem
不能控制 occurrence-native \(L_x\) 或 whole residual \(R_x=P_x-L_x\)。在 V33
快照中，位置仍是解析消去岛 / Bridge A / Gate B，留下的红叉是 joint residual
power mean square；该历史红叉现由上方 V34 的 paid scalar reduction进一步收窄。

~~~text
V33_MAXIMUM_CLAIM = EXACT_ROOT_ONE_MASTER_MARGINAL_COLLAPSE_TO_TRUNCATED_MOBIUS_SIEVE_REMAINDER_PLUS_BAZIN_MARGINAL_INTERFACE_AND_LOCAL_CARRIER_FIREWALL
V33_ROUTE_ADVANCE = YES
V33_ARITHMETIC_ADVANCE = NO
V33_FIXED_ATOM_CREDIT = 0
V33_STRICT_1_OVER_400 = UNPAID
V33_L2 = NONE
V33_TPC_207_TRIGGER = false
V33_NUMBERED_RELEASE = NO
V33_SELECTED_RESEARCH_ROUTE = B_JOINT_RESIDUAL_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK
V33_ROOT_ONE_SCOPE = EXACT_MASTER_MARGINAL_ONLY
V33_PHYSICAL_SHELL = X_OVER_2_LT_T_LE_X_WITH_X_GE_8
V33_EXACT_CUTOFF = D_POWER_400_LE_X_POWER_133
V33_CUTOFF_BELOW_SQRT_T = PROVED_EXACT_FROM_67_OVER_400_AND_X_GE_8
V33_HB2_FULL_ROOT_ONE_NUMERATOR = RETAINED_SOURCE_LOCKED_LAMBDA_T
V33_H2_J1_BRANCH = PROVED_EXACT_2_MU_D_LOG_T_OVER_D
V33_H2_J2_LARGE_F1_BRANCH = PROVED_EXACT_MINUS_MU_D_LOG_T_OVER_D
V33_H2_J2_LARGE_F2_BRANCH = PROVED_EXACT_PLUS_MU_D_LOG_D
V33_MU_MU_ONE_IDENTITY = PROVED_EXACT_MU
V33_MU_MU_LOG_IDENTITY = PROVED_EXACT_MINUS_MU_LOG
V33_TWO_J2_H2_BRANCHES = PROVED_DISJOINT_ON_X_GE_8
V33_MASTER_MARGINAL_IDENTITY = PROVED_EXACT_LAMBDA_OVER_LOG_MINUS_TRUNCATED_MU_CONV_ONE
V33_PRIME_MASTER_MARGINAL = PROVED_EXACT_ZERO
V33_ROOT_ONE_PRIME_POWER_TERM = RETAINED_EXACT_LAMBDA_OVER_LOG
V33_ROOT_GE_2_PERFECT_POWER_REMAINDER = RETAINED_SEPARATE_X_1_OVER_2_PLUS_O1
V33_FINITE_ROUTING_RECOMPUTATION = PROVED_25744_SHELL_CASES_422101_MASTER_257830_H2
V33_WRONG_J2_SIGN = STOP_SCOPED_X8_T6_FORMAL_LOG_VECTOR
V33_WRONG_CUTOFF_132 = STOP_SCOPED_X127_T65_FORMAL_LOG_VECTOR
V33_OCCURRENCE_LOCAL_COLLISION = PROVED_EXACT_X121_T77_Z5_GROUPS_7_AND_11
V33_MARGINAL_TO_OCCURRENCE_LOCAL_CARRIER = STOP_SCOPED_SELECTED_GROUP_DATA_NOT_ACCEPTED_BY_MARGINAL_THEOREM
V33_BAZIN_BETA_MARGINAL = SOURCE_BACKED_TYPE_I_II_XI_ATTACHMENT
V33_BAZIN_BASE_CELL_Q = X_POWER_21_OVER_64
V33_BAZIN_BASE_CELL_THETA = X_POWER_MINUS_21_OVER_32
V33_BAZIN_XI_DOMINANT_EXPONENT = 85_OVER_64
V33_BAZIN_ADDITIVE_TUBE_EXPONENT = 149_OVER_128
V33_BAZIN_ENDPOINT_DEFICIT = 1549_OVER_9600
V33_BAZIN_TO_V32_QOSC = STOP_SCOPED_MARGINAL_WRONG_NORM_AND_H_QUARTER_LOSS
V33_EVANS_PRIME_E2_TO_LITERAL_RESIDUAL = STOP_SCOPED_FIXED_E2_LOG_SAVING_AND_NO_LOCAL_CARRIER
V33_MRSTT_ALMOST_ALL_SHIFT_TO_LITERAL_RESIDUAL_L2 = STOP_SCOPED_QUALITATIVE_DENSITY_ONE_WRONG_NORM
V33_DIRECT_PRIMARY_SOURCE_ATTACHMENT_TO_QOSC = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V33_NEXT_THEOREM = POWER_MEAN_SQUARE_FOR_COLLAPSED_SIEVE_REMAINDER_TIMES_PHYSICAL_HYBRID_WITH_OCCURRENCE_NATIVE_LOCAL_CARRIER
V33_FIRST_FATAL = NO_JOINT_POWER_MEAN_SQUARE_FOR_COLLAPSED_SIEVE_REMAINDER_TIMES_PHYSICAL_HYBRID_WITH_OCCURRENCE_NATIVE_LOCAL_CARRIER
V33_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
V33_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
~~~

本轮是 exact compiler与 source-boundary advance，不是 arithmetic theorem；
fixed atom仍为 0，strict \(1/400\)仍 UNPAID，\(L^2\)仍 NONE，TPC-207=false。

## 33. V32 后的罗盘：只攻一个 base-scale whole-residual oscillation theorem

V32 把 V31 的 model-major mismatch 与 marginal cell cross-flatness严格压成同一
literal residual `R=P-L` 的一个单尺度 quotient Wiener gate。取

~~~text
H=x^(21/32), Y0=2^ceil(log2 H), H<=Y0<2H,
Q_Y^osc(R)=inf_(c in C) Y sum_j (int_(I_Y,j)|R-c|)^2.
~~~

只允许每个 scale一个 global complex constant。Fejer/Schur与 aligned dyadic refinement
已经 exact证明

~~~text
sum_(0<|h|<=Y)|hat R(h)|^2 <=16 Q_Y^osc(R),
Q_(2Y)^osc(R)<=2Q_Y^osc(R).
~~~

因此唯一新 B 定理是

~~~text
Q_Y0^osc(R_x)<<x^(2+2sigma+o(1)), 0<=sigma<13/4800.
~~~

它自动支付所有 Schwartz shells，并给 `|E(e)|<<x^(191/192+sigma+o(1))`；不必把门
推到 `Y~x` 或 full Parseval。常数 residual使 `Q=0`但 zero axis任意，故 terminal
`V32_A_TERMINAL_COVARIANCE`仍独立 OPEN。路线排序继续 `B > A > C`；这里的 `>`只表示
研究优先级，不表示 theorem credit。

~~~text
V32_MAXIMUM_CLAIM = EXACT_SINGLE_SCALE_ZERO_AXIS_QUOTIENTED_WIENER_CELL_COMPILER_FOR_THE_LITERAL_WHOLE_RESIDUAL
V32_ROUTE_ADVANCE = YES
V32_ARITHMETIC_ADVANCE = NO
V32_FIXED_ATOM_CREDIT = 0
V32_STRICT_1_OVER_400 = UNPAID
V32_L2 = NONE
V32_TPC_207_TRIGGER = false
V32_NUMBERED_RELEASE = NO
V32_SELECTED_RESEARCH_ROUTE = B_SINGLE_SCALE_RESIDUAL_OSCILLATION_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK
V32_WHOLE_OBJECT_SPACE = SAME_LITERAL_TAGGED_P_MINUS_OCCURRENCE_NATIVE_L
V32_LITERAL_OCCURRENCE_EMITTER = PROVED_EXACT_MASTER_MASKED_PLUS2_MINUS1_MOBIUS_LOG_HYBRID_FORM
V32_FOURIER_COEFFICIENT_IDENTITY = PROVED_EXACT_HAT_R_PLUS_H_EQUALS_E_H
V32_PHYSICAL_DIFFERENCE_SUPPORT = PROVED_EXACT_ABS_H_LESS_THAN_X_OVER_2
V32_BASE_SCALE = Y0_SMALLEST_DYADIC_WITH_H_LE_Y0_LESS_THAN_2H
V32_ALIGNED_CELL_PARTITION = PROVED_EXACT_2Y_HALF_OPEN_CELLS
V32_GLOBAL_CONSTANT_QUOTIENT = PROVED_EXACT_COMPLEX_ONE_CONSTANT_PER_SCALE
V32_QUOTIENT_INFIMUM = PROVED_ATTAINED_CONTINUOUS_COERCIVE
V32_QUOTIENT_TRANSLATION_INVARIANCE = PROVED_EXACT_ZERO_FOURIER_ONLY
V32_CELL_DEPENDENT_CONSTANTS = STOP_SCOPED_NONZERO_FOURIER_CONTAMINATION
V32_FEJER_KERNEL = PROVED_EXACT_POSITIVE_TRIANGULAR_KERNEL
V32_FEJER_BAND_CELL_BOUND = PROVED_EXACT_SAFE_CONSTANT_16
V32_DYADIC_REFINEMENT = PROVED_EXACT_Q_2Y_LE_2_Q_Y
V32_SINGLE_SCALE_TO_ALL_SCHWARTZ_SHELLS = PROVED_EXACT_A_GREATER_THAN_1_GEOMETRIC_REASSEMBLY
V32_BASE_SCALE_OSCILLATION_BOUND = SELECTED_PRIMARY_OPEN_NEW_THEOREM
V32_BASE_SCALE_OSCILLATION_EXPONENT = OPEN_SIGMA_STRICTLY_BELOW_13_OVER_4800
V32_WEIGHTED_RESIDUAL_NORM = PROVED_CONDITIONAL_X_1_PLUS_SIGMA
V32_E_ERROR_EXPONENT = PROVED_CONDITIONAL_191_OVER_192_PLUS_SIGMA
V32_E_ENDPOINT_MARGIN = PROVED_EXACT_13_OVER_4800_MINUS_SIGMA
V32_V31_PAIR_IMPLIES_V32_GATE = PROVED_EXACT_MINKOWSKI_CELL_COMPILER
V32_V32_GATE_IMPLIES_V31_PAIR = STOP_SCOPED_DISJOINT_FACTOR_AND_NARROW_SPIKE_FALSIFIERS
V32_FULL_PARSEVAL_EQUIVALENCE = STOP_SCOPED_SINGLE_BASE_SCALE_ONLY
V32_UNIFORM_ALL_SCALE_SAME_BOUND = STOP_SCOPED_TERMINAL_SCALE_OVERPAYMENT
V32_ZERO_AXIS_FIREWALL = PROVED_EXACT_CONSTANT_RESIDUAL_HAS_Q_ZERO_AND_AXIS_ARBITRARY
V32_OFFZERO_B_ALONE = STOP_SCOPED_TERMINAL_A_SURVIVES
V32_QLOCAL_MODEL_BOUND = RETAINED_PROVED_ELEMENTARY_X_95_OVER_96_PLUS_O1
V32_A_TERMINAL_COVARIANCE = RETAINED_SELECTED_TERMINAL_OPEN_NEW_THEOREM
V32_CONDITIONAL_ENDPOINT_FORMULA = MIN_ETA_R_19_OVER_2400_13_OVER_4800_MINUS_SIGMA
V32_MRT_DIRECT_ATTACHMENT = STOP_SCOPED_NO_LITERAL_RESIDUAL_OSCILLATION_BOUND
V32_GUTH_MAYNARD_DIRECT_ATTACHMENT = STOP_SCOPED_MULTIPLICATIVE_PHASE_MARGINAL_LARGE_VALUES
V32_HARPER_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_SINGLE_SEQUENCE_MODULUS_AVERAGE_WRONG_NORM
V32_BAZIN_DIRECT_ATTACHMENT = STOP_SCOPED_TYPE_I_II_RATIONAL_TUBES_NO_LITERAL_EMITTER
V32_GRANVILLE_LAMZOURI_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_BOUNDED_MULTIPLICATIVE_WRONG_COEFFICIENT
V32_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V32_NEXT_THEOREM = BASE_SCALE_COLLECTIVE_OSCILLATION_FOR_LITERAL_MASTER_HYBRID_OCCURRENCE_EMITTER
V32_FIRST_FATAL = BASE_SCALE_COLLECTIVE_OSCILLATION_BOUND_FOR_LITERAL_MASTER_HYBRID_OCCURRENCE_EMITTER
V32_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
V32_PROVENANCE_CASCADE = REQUIRED
~~~

MRT、Guth--Maynard、Harper BDH、Bazin Type-I/II与 Granville--Lamzouri只提供不同对象的
reduction或 marginal theorem；当前没有 source theorem接受 ordered MASTER/hybrid
occurrence emitter并证明上述 base-scale quotient bound。故本轮是 route advance，不是
arithmetic advance，也不触发 TPC-207。

## 32. V31 后的罗盘：同一个 model level set 上支付 whole-object B 门

V31 没有再增加一个局部 cell lemma，而是把 V30 的 `Mloc+a` attachment 与 minor
cross-flatness固定到同一个 whole object。令

~~~text
P=B*conjugate(W),
L=sum_h Mloc(h)e(-h alpha),
M_lambda={|L|>x^(1+nu)}, 0<nu<13/4800.
~~~

在查看 mismatch或 cell spikes之前冻结 `M_lambda`，并定义

~~~text
MT=hat(1_M P),
a=hat(1_M P-L),
n=hat(1_m P).
~~~

于是 `MT=Mloc+a` 与 `e=n+a` 在完整频率格 exact成立，而且 Parseval精确把
attachment energy写成 `int_M|P-L|^2+int_m|L|^2`。新主定理是前一项的
`x^(2+2nu+o(1))` bound；后一项由 level threshold支付。对同一 complement，MRT
Proposition 3.1与 V30 cell compiler把 minor压到
`3Y||c||_1||c||_infinity`，而完整 Schwartz dyadic reassembly把所有
`0<|h|<x/2` 重新装回。

因此 B 门只剩两个共同对象上的 estimate：major mismatch energy 与 cell-product
cross-flatness，且 `sigma_B=max(nu,sigma_c)<13/4800`。支付 B 后，A 仍是 terminal
q-local covariance；最终条件 margin为

~~~text
eta_* < min(eta_R,19/2400,13/4800-sigma_B).
~~~

W-dependent formula-predeclared large-spectrum set能 pointwise支付 minor flatness，但只保留为
zero-credit scoped survivor；它不能冒充 model-only theorem。C 的 equivariant quotient
no-go与 q=5 finite low-Christoffel channel均不变。

V31 atlas：

~~~text
V31_MAXIMUM_CLAIM = EXACT_WHOLE_OBJECT_MODEL_LEVEL_MAJOR_ATTACHMENT_COMPILER_PLUS_CONDITIONAL_ENDPOINT_BUDGET_PLUS_EQUIVARIANT_QUOTIENT_NO_GO
V31_ROUTE_ADVANCE = YES
V31_ARITHMETIC_ADVANCE = NO
V31_FIXED_ATOM_CREDIT = 0
V31_STRICT_1_OVER_400 = UNPAID
V31_L2 = NONE
V31_TPC_207_TRIGGER = false
V31_NUMBERED_RELEASE = NO
V31_SELECTED_RESEARCH_ROUTE = B_MODEL_MAJOR_MISMATCH_AND_MINOR_CROSS_FLATNESS_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK
V31_WHOLE_OBJECT_SPACE = SAME_LITERAL_TAGGED_P_EQUALS_B_TIMES_WBAR_AND_OCCURRENCE_NATIVE_MLOC
V31_FOURIER_COEFFICIENT_CONVENTION = PROVED_EXACT_PLUS_H_COEFFICIENT
V31_MODEL_SPECTRUM = L_X_EQUALS_SUM_H_MLOC_H_E_MINUS_H_ALPHA
V31_MODEL_ONLY_LEVEL_MAJOR = PROVED_EXACT_PREDECLARED_FROM_FROZEN_MODEL
V31_MAJOR_PREDECLARATION = REQUIRED_BEFORE_MISMATCH_OR_CELL_INSPECTION
V31_MT_DEFINITION = MT_M_H_EQUALS_HAT_OF_ONE_M_P_H
V31_ATTACHMENT_IDENTITY = PROVED_EXACT_MT_EQUALS_MLOC_PLUS_A
V31_ATTACHMENT_PARSEVAL_IDENTITY = PROVED_EXACT_MAJOR_MISMATCH_PLUS_MINOR_MODEL_ENERGY
V31_MAJOR_MISMATCH_ENERGY = SELECTED_PRIMARY_OPEN_NEW_THEOREM
V31_ACTUAL_ATTACHMENT_BOUND = OPEN_X_1_PLUS_NU_WITH_NU_BELOW_13_OVER_4800
V31_MINOR_COEFFICIENT_IDENTITY = PROVED_EXACT_E_EQUALS_N_PLUS_A
V31_MRT_PRODUCT_LOCAL_REDUCTION = SOURCE_BACKED_REDUCTION_ONLY_PROP_3_1_EQ_54
V31_CELL_PRODUCT_COMPILER = PROVED_EXACT_3Y_L1_LINF
V31_CELL_L1_GLOBAL_BOUND = PROVED_ELEMENTARY_X_1_PLUS_O1
V31_CELL_LINF_CROSS_FLATNESS = OPEN_ACTUAL_TAGGED_UNIFORM_THEOREM
V31_B_AGGREGATE_EXPONENT = PROVED_EXACT_SIGMA_B_EQUALS_MAX_NU_SIGMA_C
V31_B_ENDPOINT_CONDITION = SIGMA_B_STRICTLY_LESS_THAN_13_OVER_4800
V31_FORMULA_PREDECLARED_LARGE_SPECTRUM = SURVIVES_SCOPED_W_DEPENDENT_ZERO_CREDIT
V31_FORMULA_PREDECLARED_MINOR_FLATNESS = PROVED_EXACT_POINTWISE_THRESHOLD_COMPILER
V31_ZERO_AXIS_REASSEMBLY = PROVED_EXACT_S_EQUALS_N_ZERO_PLUS_A_ZERO
V31_OFFZERO_B_ALONE = STOP_SCOPED_AXIS_SURVIVES_ATTACHMENT_AND_MINOR_SPLIT
V31_QLOCAL_MODEL_BOUND = PROVED_ELEMENTARY_X_95_OVER_96_PLUS_O1
V31_A_TERMINAL_COVARIANCE = SELECTED_TERMINAL_OPEN_NEW_THEOREM
V31_A_B_TERMINAL_EQUIVALENCE = PROVED_EXACT_AFTER_B_STRICT_EXPONENT_CLASS
V31_WHOLE_OBJECT_CLOSURE_THEOREM = PROVED_EXACT_CONDITIONAL_ETA_STAR
V31_ENDPOINT_MARGIN_FORMULA = MIN_ETA_R_19_OVER_2400_13_OVER_4800_MINUS_SIGMA_B
V31_C_EQUIVARIANT_WHOLE_SHELL_QUOTIENT = STOP_SCOPED_TRANSLATION_INVARIANCE_FORCES_INJECTIVITY
V31_C_FULL_COORDINATE_CHRISTOFFEL = PROVED_EXACT_KAPPA_N_KAPPA0_N_MINUS_1
V31_Q5_GAP2_LOCAL_DENSITY_KERNEL = PROVED_EXACT_FINITE_LOW_CHRISTOFFEL_CARRIER
V31_Q5_TO_PHYSICAL_POSITIVE_MAIN = STOP_SCOPED_LOCAL_ADMISSIBILITY_DOES_NOT_FORCE_PRIME_MASS
V31_FIXED_HARD_SET_ALONE = STOP_SCOPED_MAJOR_MINOR_MASS_RELOCATION
V31_MRT_APPLIED_MAJOR_ATTACHMENT = STOP_SCOPED_STANDARD_LAMBDA_DK_OBJECTS_NOT_LITERAL_MASTER
V31_MRSTT_NILSEQUENCE_ATTACHMENT = STOP_SCOPED_WRONG_PROXY_PAIR_FIXED_COMPLEXITY_AND_LOGARITHMIC_SAVING
V31_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V31_NEXT_THEOREM = MODEL_LEVEL_MAJOR_MISMATCH_ENERGY_AND_MINOR_CROSS_FLATNESS_AT_COMMON_SIGMA_BELOW_13_OVER_4800
V31_FIRST_FATAL = MODEL_LEVEL_MAJOR_MISMATCH_ENERGY_FOR_LITERAL_P_MINUS_L
V31_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
V31_PROVENANCE_CASCADE = REQUIRED
~~~

Proof与 checker分别为
`research/tpc-big-road/bridge_b_whole_object_major_mismatch_and_terminal_compiler.md`、
`research/tpc-big-road/tpc_bridge_b_whole_object_major_mismatch_checker.py`。直接 source
attachment仍为 NONE；算术状态保持 NO/0/UNPAID/NONE/false。

## 31. V30 后的罗盘：先攻共同谱峰，major 已成为 terminal gate

V30 对 V29 的两门没有做假合并，而是分别推进到当前可诚实到达的最深层。对
q in (Q,2Q]、Q=x^(1/3)，shifted-prime 与 hybrid 的外部 q-local density差
Delta_(q,a)(h)逐模满足

~~~text
mean_h Delta_(q,a)(h)=0,
mean_h c_q(h)Delta_(q,a)(h)=Delta_(q,a)(0).
~~~

若 H=x^(21/32)>2Q，完整格 Poisson 的常数精确是
H psi(0) Delta_(q,a)(0)，不是 H hatpsi(0)。ordered occurrence envelope、
hard-shell exact cover与 V29 boundary ledger于是给

~~~text
M_q-local << x^(95/96+o(1)),
399/400-95/96=19/2400,
J(e_x)=R_q-local+O(x^(95/96+o(1))).
~~~

这是真正付清的 major-side model支路，但 residual diagonal仍是
S_x+O(x^(2/3+o(1)))；故 actual R_q-local signed covariance仍是 terminal
open theorem。

更高杠杆的新 reduction位于 minor。固定预声明 hard major set，并把其 minor complement分成 2Y 个 cells，
令 u_j=||B||_(2,I_j)、v_j=||W||_(2,I_j)、c_j=u_jv_j，则

~~~text
P0<=||c||_1,
PY<=3||c||_infinity,
sum_|h-h*|<=Y |r(h)-MT_M,h|^2
  << 3Y||c||_1||c||_infinity.
~~~

全局 ||c||_1<<x^(1+o(1)) 已有 elementary envelope，所以只需新证
||c||_infinity<<x^(1+2theta+2epsilon)/Y，并独立证明
MT_M,h=Mloc_x(h)+a_x(h)及同一 a_x 的 weighted L2 bound。反相 spikes
u=(R,R^-1),v=(R^-1,R)说明 joint cross-flatness严格弱于两侧分别 flat。

一旦 minor门给 |E(e_x)|<<x^(399/400-eta_E)，由
S=J+E 与 J=S-E，strict-power J(e_x) bound与 physical S_x bound双向等价。
所以合理研究排序更新为

~~~text
B: tagged cell cross-flatness + literal Mloc+a attachment;
A: terminal q-local residual major covariance;
C: symmetry-breaking low-Christoffel arithmetic quotient.
~~~

动力学侧还有一个严格 scoped no-go：在 full cyclic coordinate space上，
translation-equivariant quotient若能 exact factor point evaluation，就必须 injective；
其 kappa=N,kappa0=N-1，不满足 o(x/log^4x)。这不停止 distinguished arithmetic
seed或 restricted source class。q=5 的 admissible kernel
K5=(5/3)1_{1,2,4} 有 kappa=5/3,kappa0=2/3，证明低范数 finite carrier通道非空，
但 local admissibility不推出 prime mass。

V30 atlas：

~~~text
V30_MAXIMUM_CLAIM = EXACT_QLOCAL_MAJOR_MODEL_X_95_OVER_96_PLUS_CELL_PRODUCT_MRT_REDUCTION_PLUS_ENDPOINT_EQUIVALENCE_PLUS_EQUIVARIANT_QUOTIENT_NO_GO
V30_ROUTE_ADVANCE = YES
V30_ARITHMETIC_ADVANCE = NO
V30_FIXED_ATOM_CREDIT = 0
V30_STRICT_1_OVER_400 = UNPAID
V30_L2 = NONE
V30_TPC_207_TRIGGER = false
V30_NUMBERED_RELEASE = NO
V30_SELECTED_RESEARCH_ROUTE = B_TAGGED_HARD_MAJOR_CELL_PRODUCT_AND_MLOC_ATTACHMENT
V30_LOGICAL_TERMINAL_GATE = A_TAGGED_QLOCAL_RESIDUAL_MAJOR_AFTER_B
V30_LITERAL_JUTILA_MAJOR_SCALAR = PROVED_EXACT_L0_WITH_REFLECTED_KERNEL_SIGN
V30_J_ZERO_AXIS_SELF_RETURN = PROVED_EXACT_S_PLUS_OFFZERO
V30_OFFZERO_GATE_TO_E_MARGIN = PROVED_EXACT_CONDITIONAL_13_OVER_4800_MINUS_THETA_MINUS_EPSILON
V30_A_B_ENDPOINT_EQUIVALENCE = PROVED_EXACT_STRICT_EXPONENT_CLASS
V30_A_AS_EASIER_PRELIMINARY = STOP_SCOPED_TERMINAL_EQUIVALENCE_AFTER_B
V30_A_ADJOINT_CONVOLUTION_IDENTITY = PROVED_EXACT_ALGEBRAIC
V30_QLOCAL_F_G_DELTA_PROFILE = PROVED_EXACT_FINITE_PERIOD
V30_QLOCAL_RAMANUJAN_PAIRING = PROVED_EXACT_NORMALIZED_MEAN_EQUALS_DELTA_AT_ZERO
V30_QLOCAL_POISSON_CONSTANT = PROVED_EXACT_H_TIMES_PSI_AT_ZERO
V30_QLOCAL_UNIT_NONUNIT_LEDGER = PROVED_EXACT_ZERO_NUMERATOR_ADDED_AND_SUBTRACTED_ONCE
V30_QLOCAL_MODEL_RESIDUAL_REASSEMBLY = PROVED_EXACT_OCCURRENCEWISE
V30_QLOCAL_MODEL_BOUND = PROVED_ELEMENTARY_X_95_OVER_96_PLUS_O1
V30_QLOCAL_MODEL_MARGIN_TO_399_400 = 19/2400
V30_QLOCAL_BOUNDARY = PROVED_X_47_OVER_48_PLUS_EPSILON
V30_QLOCAL_DIAGONAL_MODEL_BOUND = PROVED_X_2_OVER_3_PLUS_O1
V30_QLOCAL_PHYSICAL_DIAGONAL_SURVIVES = PROVED_EXACT_COEFFICIENT_ONE_MINUS_SMALL_MODEL
V30_TAGGED_QLOCAL_RESIDUAL_MAJOR_COVARIANCE = SELECTED_TERMINAL_OPEN_NEW_THEOREM
V30_A_FIRST_FATAL = TAGGED_QLOCAL_RESIDUAL_MAJOR_COVARIANCE
V30_DIRECT_BV_BDH_ATTACHMENT = STOP_SCOPED_WRONG_SIGNED_COVARIANCE_OBJECT
V30_LOCAL_BC_CARRIER = PROVED_SOURCE_BACKED_X_1891_OVER_1920_BUT_ZERO_GLOBAL_CREDIT
V30_B_MRT_PRODUCT_LOCAL_REDUCTION = SOURCE_BACKED_REDUCTION_ONLY
V30_B_HARD_MAJOR_PREDECLARATION = REQUIRED_CIRCULARITY_FIREWALL
V30_B_CELL_PRODUCT_CERTIFICATE = PROVED_EXACT_PARTITION_AND_CAUCHY_SCHWARZ
V30_B_CELL_L1_GLOBAL_BOUND = PROVED_ELEMENTARY_X_1_PLUS_O1
V30_B_CELL_LINF_CROSS_FLATNESS = OPEN_ACTUAL_TAGGED_LOCAL_THEOREM
V30_B_ACTUAL_CELL_ENERGY_BOUND = OPEN_NEW_THEOREM
V30_B_MLOC_PLUS_A_ATTACHMENT = OPEN_WEIGHTED_AP_ATTACHMENT
V30_B_CROSS_FLATNESS_STRICTLY_WEAKER = PROVED_EXACT_ANTISPIKE_FAMILY
V30_B_ADAPTIVE_LARGE_SPECTRUM_EXCISION = STOP_SCOPED_MAJOR_ABSORBS_TARGET_WITHOUT_MLOC_ATTACHMENT
V30_MRT_FOURIER_UNIFORMITY_ATTACHMENT = STOP_SCOPED_LIOUVILLE_OR_NONPRETENTIOUS_1_BOUNDED_AVERAGED_WRONG_QUANTIFIERS
V30_GUTH_MAYNARD_LARGE_VALUES_ATTACHMENT = STOP_SCOPED_MULTIPLICATIVE_FREQUENCY_WRONG_TRANSFORM
V30_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V30_C_EQUIVARIANT_WHOLE_SHELL_QUOTIENT = STOP_SCOPED_TRANSLATION_INVARIANCE_FORCES_INJECTIVITY
V30_C_FULL_COORDINATE_CHRISTOFFEL = PROVED_EXACT_KAPPA_N_KAPPA0_N_MINUS_1
V30_C_DISTINGUISHED_SEED_SYMMETRY_BREAK = SURVIVES_SCOPED_OPEN
V30_C_ACTUAL_ARITHMETIC_QUOTIENT = OPEN_NEW_THEOREM
V30_Q5_GAP2_LOCAL_DENSITY_KERNEL = PROVED_EXACT_FINITE_LOW_CHRISTOFFEL_CARRIER
V30_Q5_TO_PHYSICAL_POSITIVE_MAIN = STOP_SCOPED_LOCAL_ADMISSIBILITY_DOES_NOT_FORCE_PRIME_MASS
V30_NEXT_THEOREM = TAGGED_HARD_MAJOR_CELL_CROSS_FLATNESS_PLUS_MLOC_WEIGHTED_ATTACHMENT
V30_FIRST_FATAL = MISSING_LITERAL_MT_EQUALS_MLOC_PLUS_A_AND_TAGGED_CELL_CROSS_FLATNESS
V30_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
V30_PROVENANCE_CASCADE = REQUIRED
~~~

proof与 checker分别为
research/tpc-big-road/bridge_b_terminal_major_cross_flatness_and_equivariant_quotient.md、
research/tpc-big-road/tpc_bridge_b_terminal_major_cross_flatness_checker.py。checker冻结
49/52/7/6 contract/registry/source/dependency rows，registry digest为
acead73d0c6e12b03d30d40f35ea345c32d859bea5106456f33b4724fdf23563，并执行
100/107/16/14/155 mutations，共 392 个 unique reject actions。

## 30. V29 后的罗盘：local corridor 已付，全局必须过独立 major/minor 两门

V29 先钉死一个容易被隐藏的逻辑点。对同一个 tagged residual

~~~text
e_x=r_x-Mloc_x,
Mloc_x(0)=0,
S_x=J(e_x)+E(e_x).
~~~

有限对象 `e=T delta_0` 有 `E(e)=0` 且全部 off-zero energy为零，却有
`J(e)=S=T`。所以 analytic primary不再写成模糊的 joint residual estimate，而是
严格分成

~~~text
|J(e_x)| << x^(399/400-eta_M), eta_M>0,
|| |hatpsi|^(1/2)e_x ||_(h!=0,2)
  << x^(1+theta+epsilon_N), theta<13/4800.
~~~

第二门只支付 `E(e_x)<<x^(191/192+theta+epsilon_N+o(1))`；两门共同 fixed margin
要求 `epsilon_*<min(eta_M,(13/4800-theta)/2)`。MRT Proposition 3.1仍只是
`Y P0 PY` reduction；它不证明 actual `MT_M=Mloc+a` attachment，也不碰零坐标。

与此同时，V28 的 conditional reduced-radical corridor已经在 V29 变成真正完成的
local theorem。exact interior/boundary cover给 boundary `x^(47/48+epsilon)`，
`epsilon<11/1920`；`q|D`在绝对值前消去，而 active rows有
`g<=x^(17/96)<q`，故不存在 `q|g` correction。F/G 的 Möbius coprimality costs为
`d^-2`、`d0^-2 d1^-3`；fixed-
`R1` triangle与 log-Fourier separation的全部 loss已进入 ledger。Bettin--Chandee
因此给

~~~text
J(Mloc_x), E(Mloc_x) << x^(1891/1920+o(1)),
margin to 399/400 = 121/9600.
~~~

但 `J(Mloc)+E(Mloc)=0`，所以这是 reusable local subgate，不是 arithmetic credit。

动力学 reserve现在有精确宽度。预声明 target-blind subspace的最小 Riesz kernel若
`kappa=||K*||_2^2`、`kappa0=kappa-1`，则

~~~text
L(S)>=mean(S)-sqrt(kappa0)||S-mean(S)||_2.
~~~

在 positive main `>>x/log^2x`、variance `O(x)` 下，uniform L2 sharp threshold是
`kappa0=o(x/log^4x)`。`Z/4Z` 的三频 finite model证明通道非空；full coordinates、
coarse cells、martingale level count、target-calibrated fit与 skew tags均有 exact scoped
no-go。真正缺的是 actual whole-shell low-Christoffel quotient与独立 positive main。

V29 atlas：

~~~text
V29_MAXIMUM_CLAIM = EXACT_LOCAL_CARRIER_BETTIN_CHANDEE_COMPILER_PLUS_ZERO_AXIS_TWO_GATE_FIREWALL_PLUS_LOW_CHRISTOFFEL_RIESZ_CRITERION
V29_ROUTE_ADVANCE = YES
V29_ARITHMETIC_ADVANCE = NO
V29_FIXED_ATOM_CREDIT = 0
V29_STRICT_1_OVER_400 = UNPAID
V29_L2 = NONE
V29_TPC_207_TRIGGER = false
V29_NUMBERED_RELEASE = NO
V29_ZERO_AXIS_RESIDUAL_IDENTITY = PROVED_EXACT_FROM_V28_TAGGED_DEFINITION
V29_ZERO_AXIS_DIRAC_FIREWALL = PROVED_EXACT_FINITE_E_ZERO_J_FULL_EXAMPLE
V29_OFFZERO_RESIDUAL_ENERGY_ALONE = STOP_SCOPED_DELTA_ZERO_SELF_RETURN
V29_TAGGED_RESIDUAL_INDEPENDENT_JUTILA_MAJOR = SELECTED_PRIMARY_OPEN_NEW_THEOREM
V29_TAGGED_RESIDUAL_OFFZERO_WEIGHTED_L2 = OPEN_NEW_THEOREM
V29_TAGGED_RESIDUAL_TWO_GATE_CLOSURE = OPEN_MAJOR_AND_MINOR_THEOREM
V29_MRT_ABSTRACT_PRODUCT_LOCAL_L2 = SOURCE_BACKED_REDUCTION_ONLY
V29_WEAKEST_PRODUCT_LOCAL_CONDITION = PRODUCT_P0_TIMES_PY_WITH_HARD_MAJOR_ATTACHMENT
V29_ACTUAL_MAJOR_COEFFICIENT_MLOC_PLUS_A = OPEN_WEIGHTED_AP_ATTACHMENT
V29_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V29_MASTER_INTERIOR_BOUNDARY_EXACT_COVER = PROVED_WITH_X_47_OVER_48_PLUS_EPSILON
V29_Q_DIVIDES_D_PRE_ABSOLUTE_CANCELLATION = PROVED_EXACT_FULL_LATTICE_BULK
V29_Q_DIVIDES_G_CORRECTION = PROVED_EMPTY_BY_G_LT_Q
V29_F_G_SIGNED_REDUCED_RADICAL_EMITTER = PROVED_EXACT
V29_R1_EQUAL_ONE_PRE_ABSOLUTE_CANCELLATION = PROVED_EXACT
V29_F_COPRIMALITY_MOBIUS_COMPILER = PROVED_D_MINUS_2_SUMMABLE
V29_G_COPRIMALITY_MOBIUS_COMPILER = PROVED_D0_MINUS_2_D1_MINUS_3_SUMMABLE
V29_EXACT_R1_LOCAL_TRIANGLE = PROVED_L_FACTOR_PAID_IN_EXPONENT_LEDGER
V29_SMOOTH_DYADIC_SEPARATION = PROVED_EXACT_LOG_FOURIER_X_O1
V29_LOCAL_CARRIER_BC_BOUND = PROVED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1
V29_LOCAL_CARRIER_BC_EXPONENT = 1891/1920
V29_LOCAL_CARRIER_BC_MARGIN_TO_399_400 = 121/9600
V29_LOCAL_EULER_TENSOR_AS_ACTUAL_AP_MAIN = OPEN_ATTACHMENT
V29_PREDECLARED_SUBSPACE_MINIMUM_RIESZ_KERNEL = PROVED_EXACT_FINITE_HILBERT
V29_EVALUATION_FACTORIZATION_GATE = PROVED_EXACT_KER_Q_SUBSET_KER_L_IFF
V29_VARIANCE_O_X_CHRISTOFFEL_THRESHOLD = PROVED_EXACT_KAPPA0_O_X_OVER_LOG4
V29_FINITE_CYCLIC_SPECTRAL_KERNEL = PROVED_EXACT_KAPPA_EQUALS_FREQUENCY_DIMENSION
V29_NONCONSTANT_LOW_NORM_KERNEL_CHANNEL = PROVED_NONEMPTY_EXACT_FINITE_MODEL
V29_COARSE_CELL_AS_POINT_EVALUATION = STOP_SCOPED_EXACT_FOUR_POINT_COUNTEREXAMPLE
V29_SPARSE_MARTINGALE_LEVEL_COUNT = STOP_SCOPED_ORTHOGONAL_ENERGY_REASSEMBLES_SINGLETON_NORM
V29_TARGET_CALIBRATED_SINGLE_BLOCK_KERNEL = STOP_SCOPED_EXACT_CIRCULAR_ONE_VECTOR_FIT
V29_STAGE_TAG_SKEW_PRODUCT_NORM_GAIN = STOP_SCOPED_EXACT_KAPPA_DIVIDED_BY_FIBER_MASS
V29_ACTUAL_WHOLE_SHELL_LOW_CHRISTOFFEL_QUOTIENT = SELECTED_DYNAMICS_OPEN_NEW_THEOREM
V29_INDEPENDENT_POSITIVE_KERNEL_MAIN = OPEN_ATTACHMENT_NOT_SAME_OUTPUT_MEAN
~~~

proof与 checker分别为
`research/tpc-big-road/bridge_b_joint_major_minor_and_low_christoffel.md`、
`research/tpc-big-road/tpc_bridge_b_joint_major_minor_checker.py`。checker冻结
44/42/4/6 contract/registry/source/dependency rows，registry digest为
`39b3aaf04f28763bca249ef874f07ade304e71d3e4eb390613fa1870455826a6`，并执行
134/87/10/15/149 mutations。

路线排序：independent major第一；same-residual minor/L2第二；已付 local BC作为工具；
actual low-Christoffel quotient第三条新 construction。四者不互借 theorem credit。

## 29. V28 后的罗盘：循环零轴已拆开，reduced-radical corridor 接上真引擎

V28 把 V27 的 `-F(0)` wall重型为两个不能混同的 main。generic smooth
interpolant若强制 `M(0)=S_x`，仍把原目标以系数一返回；但 actual selected
MASTER occurrence产生的 local Euler tensor满足

~~~text
Delta_m,z(0)=0,
mean_(h mod rad(m)) Delta_m,z(h)=0,
mean_(h mod lcm(q,rad(m))) c_q(h)Delta_m,z(h)=0,
Mloc_x(0)=0,
J(Mloc_x)+E(Mloc_x)=0.
~~~

这是 exact occurrence-native algebra，不是 finite-interval weighted AP theorem。
把 \(g=(n,D)\)、\(D=gR\)、\(n=ga\) 后，composite DFT 中 \(g\) 精确消失：

~~~text
P_hat_D(n qbar)=mu(R)/phi(R)e_R(2a qbar),
B_hat_D,z(n qbar)
 =mu(R0)/(phi(R0)phi(R1)^2)e_R0(2a overline(qR1)).
~~~

真正 dual corridor因此只有
`R>=H/q=x^(31/96+o(1))`、`|a|<=qR/H<=x^(17/96+o(1))`。
selected-group mass与 radical Euler sum给 dyadic norm
`x^(1+o(1))R^(-3/2)`。Bettin--Chandee Theorem 1在 exact smooth emitter
完成后产生

~~~text
CORRIDOR_EXPONENT = 1891/1920,
399/400-CORRIDOR_EXPONENT = 121/9600.
~~~

这是第一条真正越过 endpoint的 source-backed conditional corridor engine；但
moving \(R_0/R_1\) emitter、`q|D` collective cancellation、both signs、
hard-shell partial summation与 exactly-once reassembly未完，所以不记 arithmetic
credit。解析主路仍是同一个 tagged residual的 joint J/E compiler与 two-sided
product-local flatness；MRT Proposition 3.1只是 reduction，one-sided input损失
`H^(1/4)`并差 `1549/9600`。

动力学地图也更干净：stationary mixing system不能 exact factor到 rotation/odometer，
否则出现 root-of-unity eigenfunction。合法 reserve改为 nonautonomous、
target-independent low-norm kernel，要求
`||K_j||_2 V_j=o(x_j/log^2 x_j)`；full primorial point kernel的 norm
`sqrt(P)=exp((1/2+o(1))sqrt x)`，因此停止。

V28 atlas：

~~~text
V28_MAXIMUM_CLAIM = EXACT_OCCURRENCE_NATIVE_EULER_ZERO_AXIS_AND_REDUCED_RADICAL_CORRIDOR_PLUS_SOURCE_BACKED_CONDITIONAL_BETTIN_CHANDEE_ENGINE_PLUS_STATIONARY_FACTOR_NO_GO_AND_COMPRESSED_KERNEL_ROUTE
V28_ROUTE_ADVANCE = YES
V28_ARITHMETIC_ADVANCE = NO
V28_FIXED_ATOM_CREDIT = 0
V28_STRICT_1_OVER_400 = UNPAID
V28_L2 = NONE
V28_TPC_207_TRIGGER = false
V28_NUMBERED_RELEASE = NO
V28_MASTER_OCCURRENCE_LOCAL_EULER_TENSOR = PROVED_EXACT_ALGEBRAIC
V28_LOCAL_EULER_ZERO_MEAN_RAMANUJAN_ORTHOGONALITY = PROVED_EXACT_ALGEBRAIC
V28_LOCAL_EULER_TENSOR_AS_ACTUAL_WEIGHTED_AP_MAIN = OPEN_ATTACHMENT
V28_SMOOTH_MAIN_WITH_M0_EQUAL_PHYSICAL_TARGET
  = STOP_SCOPED_CIRCULAR_ZERO_AXIS_COEFFICIENT_ONE
V28_LOCAL_MAIN_JUTILA_J_PLUS_E_CANCELLATION = PROVED_EXACT_ALGEBRAIC
V28_REDUCED_RADICAL_CRT_PHASE
  = PROVED_EXACT_G_CANCELLATION_AND_PLUS_TWO_PHASE
V28_LOCAL_MAIN_SHARED_Q_DIVIDES_RADICAL_BRANCH
  = PROVED_EXACT_AFTER_FULL_UNIT_FREQUENCY_SUM
V28_SELECTED_MASTER_RADICAL_L2_ENVELOPE
  = PROVED_ELEMENTARY_FROM_ORDERED_D2_D4_AND_RADICAL_EULER_SUM
V28_SHORT_INVERSE_RESIDUE_BETTIN_CHANDEE_CORRIDOR
  = SOURCE_BACKED_POWER_SAVING_AFTER_EXACT_COMPILER
V28_SHORT_INVERSE_RESIDUE_CORRIDOR_EXPONENT = 1891/1920
V28_SHORT_INVERSE_RESIDUE_CORRIDOR_MARGIN_TO_399_400 = 121/9600
V28_LITERAL_MASTER_CORRIDOR_SMOOTH_EMITTER_AND_G_REASSEMBLY
  = OPEN_EXACT_COMPILER
V28_LOCAL_MAIN_HARD_SHELL_ENDPOINT
  = PROVED_ELEMENTARY_X_47_OVER_48_PLUS_EPSILON
V28_MRT_ABSTRACT_PRODUCT_LOCAL_L2_REDUCTION = SOURCE_BACKED_ABSTRACT_INTERFACE_ONLY
V28_LITERAL_BILINEAR_PRODUCT_LOCAL_FLATNESS = OPEN_NEW_THEOREM
V28_ONE_SIDED_MRT_TO_ENDPOINT = STOP_SCOPED_H_QUARTER_LOSS
V28_TAGGED_RESIDUAL_JUTILA_MAIN_ERROR_REASSEMBLY
  = SELECTED_PRIMARY_OPEN_ATTACHMENT
V28_STATIONARY_MIXING_TO_ROTATION_ODOMETER_FACTOR
  = STOP_SCOPED_ROOT_OF_UNITY_EIGENFUNCTION_NO_GO
V28_NONAUTONOMOUS_POINTED_ESCAPE
  = LOGICALLY_OPEN_EXACT_STAGE_DIAGRAM_REQUIRED
V28_LOW_NORM_POINT_EVALUATION_KERNEL_CRITERION = PROVED_EXACT_ALGEBRAIC
V28_POSITIVE_MEAN_WITHOUT_KERNEL_COVARIANCE_CONTROL
  = STOP_SCOPED_EXACT_TWO_POINT_FALSIFIERS
V28_FULL_PRIMORIAL_POINT_RIESZ_NORM
  = PROVED_EXACT_FINITE_PLUS_STANDARD_PNT_ASYMPTOTIC
V28_COMPRESSED_TARGET_INDEPENDENT_KERNEL_WHOLE_SHELL_COMPILER
  = SELECTED_DYNAMICS_OPEN_NEW_THEOREM
V28_ABP_HNTV_INTERFACES = SOURCE_BACKED_TOOL_CLASSES_ONLY
V28_HENON_WANG_YOUNG_DENSE_TREE_NATURAL_EXTENSION
  = SOURCE_BACKED_TOPOLOGICAL_GEOMETRY_ONLY
V28_HENON_TPC_STAGE_EVENT_MEASURE_SEED_FUNCTIONAL_DIAGRAM = OPEN_ATTACHMENT
V28_O161_PARENTS_PAIR_NATIVE_H1_GLOBAL = OPEN_UNCHANGED
V28_A1_A2_TAIL_SELECTION_PACKET_PROVENANCE = INDEPENDENT_AND_UNPAID
~~~

proof 与 checker分别为
`research/tpc-big-road/bridge_b_euler_zero_axis_and_kernel_carrier.md`、
`research/tpc-big-road/tpc_bridge_b_euler_kernel_checker.py`。checker冻结
49-field contract、36-row registry、digest
`2926e4dc94080ff3179970dc134c1a1edb76bcb5b7f64be783b4bc747d5c7a0b`，
并执行 149/75/12/15/149 个 contract/registry/source/dependency/result mutations。

路线排序：joint tagged residual theorem第一；BC reduced-radical compiler第二；
nonautonomous compressed kernel第三。三者不互借 theorem credit。

## 28. V27 后的罗盘：能量门已精确，零轴和 pointed seed 是真墙

V27 把 V26 的 square-root heuristic变成一个精确、tail-safe 的 Hilbert theorem
contract。令

~~~text
A_Q(h)=sum_(q prime~x^(1/3)) c_q(h),
r_x(h)=sum_(t,t+h in I_x) beta_x^raw(t)w_x^(z)(t+h),
H=x^(21/32).
~~~

对 `N` 小于两个不同 shell primes的首个乘积，

~~~text
sum_(0<|h|<=N)|A_Q(h)|^2
 =2[N R^2+sum_q floor(N/q)(q^2-2qR)].
~~~

Schwartz tails与双素因子 cross terms全部保留后，

~~~text
|| |hatpsi|^(1/2) A_Q ||_2 / L_pr = x^(-1/192+o(1)).
~~~

原 scalar只有一个 `hatpsi`，所以 Cauchy必须把 `|hatpsi|^(1/2)`各放一侧；不能
给两侧各塞一个完整 `hatpsi`。真正的解析主定理已压成

~~~text
V27_LITERAL_PRIME_SHELL_RAMANUJAN_VECTOR_COVARIANCE
  = SELECTED_OPEN_NEW_THEOREM,

(sum_(0<|h|<x/2)|hatpsi(h/H)| |r_x(h)|^2)^(1/2)
  <= x^(1+theta+o(1)), theta<13/4800.
~~~

该 theorem一旦成立，normalized exponent为 `191/192+theta`。等号
`theta=13/4800`不够；所有损失后必须保留固定正 margin。

V27 同时发现一个先行 firewall。对任意 uniformly smooth `F`，

~~~text
1/L_pr sum_(h!=0) A_Q(h)F(h/H)
 = -F(0)+O_s(||F^(s)||_1(Q/H)^(s-1)).
~~~

删除 correlation zero shift后，smooth main不会免费消失，而留下精确
`-F(0)` axis。只把一个 lattice value改成零会把损失转移到 derivative ledger。
因此 residual energy之前必须另证 signed local-main/zero-axis reassembly。

Primary-source screen也已定量闭合：MRT proof-level energy与目标差
`781/2400`，MRSTT Higher Uniformity只给单 phase/AP的 logarithmic input，triangle
power scale为 `223/96`；Leung arbitrary-shift-weight theorem是有价值的 automorphic
architecture analogue，但仍差 `181/2400`且 coefficient不匹配。它们都不能直接
认领 arithmetic credit。

动力学 reserve进一步 fail closed。若 exact carrier在正测度参数集上对每个参数都等于
同一个 arithmetic block count，则 normalized conditional parameter mean就是待证
count、variance为零；若
carrier只在 arithmetic phase的单点/null graph成立，a.e.-parameter theorem又选不中。
因此这两种 candidate parameter designs STOP；本轮保留的 reserve是

~~~text
V27_POINTED_CRITICAL_SECTION_WHOLE_SHELL_DISCREPANCY
  = OPEN_NEW_THEOREM_AFTER_EXACT_SINGLE_PARAMETER_FACTOR.
~~~

V27 atlas：

~~~text
V27_PRIME_SHELL_HARD_WINDOW_RAMANUJAN_L2_IDENTITY
  = PROVED_EXACT_L0_FOR_N_LT_FIRST_DISTINCT_PRIME_PRODUCT
V27_PRIME_SHELL_RAMANUJAN_WEIGHTED_ENERGY
  = PROVED_EXACT_FINITE_PLUS_SCHWARTZ_ASYMPTOTIC
V27_EFFECTIVE_HORIZON_AS_HARD_SUPPORT
  = STOP_SCOPED_FALSE_SCHWARTZ_TAIL_AND_DOUBLE_DIVISOR_CROSS_TERMS
V27_ONE_PSI_WEIGHTED_CAUCHY_INTERFACE
  = PROVED_EXACT_ABS_PSI_HALF_WEIGHT_ON_BOTH_FACTORS
V27_LITERAL_PRIME_SHELL_RAMANUJAN_VECTOR_COVARIANCE = SELECTED_OPEN_NEW_THEOREM
V27_FULL_LATTICE_SMOOTH_MAIN_POISSON_IDENTITY
  = PROVED_EXACT_DETERMINISTIC_INTERFACE
V27_AUTOMATIC_SMOOTH_LOCAL_MAIN_ANNIHILATION_AFTER_CORRELATION_ZERO_SHIFT_DELETION
  = STOP_SCOPED_ZERO_AXIS_MINUS_F_OF_ZERO
V27_SIGNED_LOCAL_MAIN_ZERO_AXIS_AND_RESIDUAL_REASSEMBLY = OPEN_NEW_THEOREM
V27_MRT_MRSTT_TO_LITERAL_PRIME_RAMANUJAN_WEIGHTED_NUMERATOR
  = STOP_SCOPED_NO_COLLECTIVE_POWER_NORM
V27_EXISTING_SHIFTED_CONVOLUTION_SPECTRAL_CORPUS_DIRECT_ATTACHMENT
  = STOP_SCOPED_NO_LITERAL_WHOLE_PHYSICAL_SCALAR
V27_MIXED_HB2_ONE_COMMON_SOURCE_ARRAY
  = STOP_SCOPED_FINITE_SELECTOR_MINOR_ONE
V27_TAGGED_VECTOR_MIXED_HB2_DETERMINANT_REASSEMBLY = OPEN_NEW_THEOREM
V27_PARAMETER_AVERAGED_EXACT_SAME_ARITHMETIC_OUTPUT_CARRIER
  = STOP_SCOPED_TAUTOLOGICAL_MEAN_OR_NULL_GRAPH
V27_STAGEWISE_TRANSVERSE_PARAMETER_RESELECTION = STOP_SCOPED_NO_COMMON_PARAMETER
V27_POINTED_CRITICAL_SECTION_WHOLE_SHELL_DISCREPANCY
  = OPEN_NEW_THEOREM_AFTER_EXACT_SINGLE_PARAMETER_FACTOR
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
~~~

路线顺序是：literal vector covariance与zero-axis reassembly并列第一；tagged
mixed-HB theorem是解析 construction reserve；pointed whole-shell theorem是动力学
reserve。三者不互借 theorem credit。

## 27. V26 后的罗盘：两条大桥，不再堆 fixed cells

V26 把当前迷宫压缩成一个解析主桥、一个动力学主桥和一个 mixed-HB construction。
解析主桥不再从 Farey/Kloosterman cell向外猜，而直接控制 exact compensated object

```text
E_x=-1/L_pr [sum_(q prime~x^(1/3)) q sum_(k!=0) C_x(qk)
             -R sum_(h!=0) C_x(h)],
C_x(h)=hatpsi_+(x^(-21/32)h)
       sum_(t,t+h in I_x) beta_x^raw(t)w_x^(z)(t+h).
```

这里 `h`是 correlation shift，physical gap仍固定为 `h0=2`并已经包含在
`w_x^(z)(u)=Lambda(u+2)-b_x^(z)(u)`。两个 summands是一枚 Ramanujan
multiplier，不能分开取绝对值，也不能再换名为 V21/V22 centered projector。

若 joint family达到完整 square-root cancellation，则 normalized exponent为
`191/192`，相对 strict `399/400` 有 `13/4800`正 margin。这给出一个尺寸正确、
对象正确、可以证伪的 theorem contract：

```text
V26_PRIME_SHELL_RAMANUJAN_COMPENSATED_DILATION_COVARIANCE
  = OPEN_NEW_THEOREM.
```

它不是既有 source theorem。Drappeau/DI/Kuznetsov/BP/Pascadi等最近对象在 modulus
ensemble、product/additive congruence、coefficient independence、axes或 outer norm上
不匹配，故 declared direct corpus attachment STOP_SCOPED。

factorable reserve里真正的正面结果只属于 smooth J1-by-J1 determinant
`RS-EF=2`，其中两个 J1 rows各自的 `+2` coefficient给 literal product `+4`。
Bettin--Chandee Corollary 1给 local error exponent至多 `39/40`，
其前提包括 balance ratio `O(1)`、`eta=x^(o(1))` smooth derivative ledger及 natural
outer `L2` envelopes；common-`q` Poisson又给 short-dual relation
`KR+HM=0 mod q`与长度 `x^(1/14)`。
这是 rank-1 bridge pier，不是整座桥。ordered J2的 dual area为 `x^(1/7)E`，
zero/nonunit axes不可删，hybrid又使用 `lcm(q,d_rough)` progression；所以 whole
factorable compiler必须 STOP，而

```text
V26_MIXED_HB_DETERMINANT_COMPILER = OPEN_NEW_THEOREM_RANK1
```

只允许作为一个统一 J1/J2/hybrid mains与 reassembly的宏观 theorem，不再拆成一串
局部论文。

动力学路线也发生了真正的方向修正。safe lacunary `x_n~8^n` 上每段只取一个 event时，
mass约为 `1/n^2`，总和有限；single-event DBC不会推出无穷多个 gaps。正确 object是
整个 shell count：mean约 `x_n/log^2x_n`、variance `O(x_n)`，故 Haar bad mass
`O(log^4x_n/x_n)`可求和。缺口集中为

```text
V26_SAFE_LACUNARY_CRITICAL_SECTION_BLOCK_TRANSFER_THEOREM
  = OPEN_NEW_THEOREM.
```

Aspenberg--Baladi--Persson已对 Logistic critical seed `1/2`证明 fixed-observable
parameter ASIP；所以 distinguished critical seed不再是 blanket impossibility。
但 exact arithmetic seed carrier、same return locus、growing triangular norms与
positive physical block output仍全部要由新 theorem支付。Hénon只在 exact natural-
section factor之后进入同一 gate。

V26 atlas：

```text
V26_PRIME_SHELL_COMPENSATED_DILATION_IDENTITY = PROVED_EXACT_L0
V26_PRIME_SHELL_SQUARE_ROOT_ENDPOINT_LEDGER = PROVED_EXACT_RATIONAL_POSITIVE_MARGIN
V26_PRIME_SHELL_RAMANUJAN_COMPENSATED_DILATION_COVARIANCE = OPEN_NEW_THEOREM
V26_J1xJ1_SMOOTH_DETERMINANT_CELL
  = SOURCE_BACKED_CONDITIONAL_LOCAL_ENGINE_ERROR_39_OVER_40_BEFORE_MAIN_REASSEMBLY
V26_COMMON_FACTORABLE_J1_SHORT_DUAL_DETERMINANT = PROVED_EXACT_L0_COPRIME_SMOOTH_CELL
V26_COMMON_ENSEMBLE_GOOD_BAD_p_INCIDENCE = PROVED_EXACT_L0_ANALYTIC_COST_OPEN
V26_SINGLE_TEMPLATE_MASTER_FACTORIZATION = STOP_SCOPED_FINITE_2X2_MINOR
V26_ALL_HB2_TYPES_ONE_COMMON_SOURCE_ARRAY
  = STOP_SCOPED_J2_DEGENERATE_AXIS_AND_NORMALIZATION_MISMATCH
V26_HYBRID_TO_SAME_ARRAYS
  = STOP_SCOPED_PROGRESS_MODULUS_MAIN_REASSEMBLY_MISMATCH
V26_FACTORIZABLE_LITERAL_TRANSFORM_COMPILER
  = STOP_SCOPED_PARTIAL_J1_ONLY_NO_WHOLE_OBJECT
V26_MIXED_HB_DETERMINANT_COMPILER = OPEN_NEW_THEOREM_RANK1
V26_LACUNARY_SINGLE_EVENT_DBC = STOP_SCOPED_FINITE_TOTAL_EVENT_MASS
V26_WHOLE_SHELL_BLOCK_CHEBYSHEV = PROVED_ELEMENTARY_SUMMABLE_HAAR_BAD_MASS
V26_LOGISTIC_CRITICAL_SEED_PARAMETER_ASIP = SOURCE_BACKED_FIXED_HOLDER_OBSERVABLE
V26_ARITHMETIC_SEED_TO_CRITICAL_SECTION_INTERTWINER = ABSENT
V26_GROWING_TRIANGULAR_CRITICAL_SECTION_THEOREM = ABSENT
V26_SAFE_LACUNARY_CRITICAL_SECTION_BLOCK_TRANSFER_THEOREM = OPEN_NEW_THEOREM
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
```

当前排序是：compensated covariance第一，whole-shell dynamical transfer第二，mixed
HB compiler第三。A1/A2、O161 parents、pair-native/H1与 global architecture仍是独立
reserves；任何局部 margin都不能互借 theorem credit。

## 26. V25 后的罗盘：Fourier emitter 已纠正，主墙是 literal weighted shift

V24把 determinant送到了 corrected Farey atoms，但沿用了 Blomer--Li v1 (2.2)
第一行的 printed Fourier phase。V25发现这行少了 divisor `d`：从
`r_q(n)=sum_(d|(q,n))d mu(q/d)`写 `n=dm`，phase必须是 `e(-alpha d m)`。
`q=2` 的 frequency-one coefficient给出立即反例；当前公开 source未见修订。因此合法
路线只使用仓库从 Lemma 1重推的 corrected kernel，并严格区分 Fourier frequency
`n=dm`与 rational Poisson dummy。

完成 full-ensemble zero cancellation与 V24 corrected Farey reassembly后，Jutila error
不再是模糊的 `(q,c,b)` cloud，而精确压缩为

```text
E_x=-sum_(D!=0) B_x(D) kappa(D),
complete atom=S(D-n,sigma(z)u;c)e(z(D-n)).
```

这是真正的路线压缩：`V25_NONZERO_SHIFT_SIGNED_FAREY_KLOOSTERMAN_EMITTER` 已经
`PROVED_EXACT_L0`。同时它说明继续逐 cell套 Blomer--Pascadi没有意义；第一项未付量是
physical convolution `||(1-chi)G_x||_2`，再加长变量、nonunit/axes、tails与唯一 outer
reassembly。fixed `c,z` short coprime cell保留 source-backed conditional engine，但
physical credit仍为零。

第二条 reserve也不再模糊。另设 source-native
`Q1=x^(4/21),Q2=x^(8/21),q_aux=p t`，保留 unrestricted smooth `t`及所有
`(p,t)` multiplicities，可对同一 macro shift `(1,1,2)`建立 common exact split，且

```text
||1-chi_aux||_2 <<_(psi,rho) x^(-1/14+o(1)).
```

这是有用的更宽 conditional window，但不是 arithmetic saving。现有 crude energy只给
`x^(10/7+o(1))`；纯 energy闭合必须新证
`||G_x||_2<=x^(1+theta+o(1))`, `theta<193/2800`。source `41/42` theorem依赖
GL(3)/divisor coefficients与 Voronoi chain，不能替换 literal Möbius/log ×
`Lambda-b`。atomwise改变 good-prime set也破坏 common normalization。

因此当前路线排序为

```text
1. V25_RAMANUJAN_WEIGHTED_NONZERO_SHIFT_PHYSICAL_THEOREM
     = OPEN_NEW_THEOREM;
2. V25_FACTORIZABLE_LITERAL_TRANSFORM_COMPILER
     = OPEN_NEW_CONSTRUCTION;
3. fixed-c,z BP/Pascadi cells
     = CONDITIONAL_LOCAL_ENGINES_ONLY;
4. V23 stable-block/summable-bad-set dynamics reserve;
5. A1/A2 independent reserves.
```

精确 atlas为

```text
V25_BLOMER_LI_2_2_FIRST_LINE_AS_PRINTED_MISSING_d_PHASE
  = STOP_SCOPED_LITERAL_q2_FOURIER_COUNTEREXAMPLE
V25_CORRECTED_JUTILA_DIVISOR_FOURIER_EXPANSION
  = PROVED_EXACT_L0_REPOSITORY_DERIVATION
V25_FOURIER_RATIONAL_DUMMY_INDEX_IDENTIFICATION
  = STOP_SCOPED_POISSON_DUAL_TYPE_ERROR
V25_FULL_ENSEMBLE_ZERO_MODE_CANCELLATION = PROVED_EXACT_L0
V25_NONZERO_SHIFT_SIGNED_FAREY_KLOOSTERMAN_EMITTER = PROVED_EXACT_L0
V25_PRIME_SHELL_GROUPED_RAMANUJAN_KERNEL = PROVED_EXACT_L0
V25_DIRECT_CELLWISE_BP_FROM_EXACT_EMITTER
  = STOP_SCOPED_OUTER_NORM_LONG_RANGE_AND_REASSEMBLY_UNPAID
V25_FIXED_c_z_COPRIME_SHORT_BP_CELL = SOURCE_BACKED_CONDITIONAL_ENGINE
V25_FIXED_c_z_NONUNIT_PASCADI_CELL
  = CONDITIONAL_BV_FOURIER_MEASURE_NORM_UNPAID
V25_FACTORIZABLE_AUXILIARY_JUTILA_SPLIT = PROVED_EXACT_L0
V25_FACTORIZABLE_AUXILIARY_L2_GAIN
  = PROVED_SOURCE_BACKED_DERIVED_UPPER_BOUND_X_MINUS_1_OVER_14
V25_DIRECT_BLOMER_LI_41_OVER_42_TO_LITERAL_TPC_TRANSFER
  = STOP_SCOPED_COEFFICIENT_VORONOI_AND_REASSEMBLY_MISMATCH
V25_ATOMWISE_COMMON_GOOD_PRIME_ENSEMBLE
  = STOP_SCOPED_MOVING_SLOPE_GCD_AND_REASSEMBLY_MISMATCH
V25_RAMANUJAN_WEIGHTED_NONZERO_SHIFT_PHYSICAL_THEOREM = OPEN_NEW_THEOREM
V25_FACTORIZABLE_LITERAL_TRANSFORM_COMPILER = OPEN_NEW_CONSTRUCTION
```

停止项不停止 corrected L0 emitter或 factorable exact split。overall arithmetic
advance=`NO`、fixed atom=`0`、strict `1/400=UNPAID`、`L2=NONE`、TPC-207=false。

## 25. V24 后的罗盘：原子已经落地，缺的是 collective emitter

V23留下的不是一句模糊的“也许能用第二 circle method”。V24已经把同一个 fixed
`h0=2` literal physical scalar逐 occurrence展开为 determinant atoms。Blomer--Li
Lemma 1 source-backed给 Jutila split；其 printed Lemma 2 却把 Farey interval写成
`max`并在左右半弧都用 fixed-plus inverse phase。两个 finite counterexamples锁定该
source typo，随后由 Farey neighbors独立证明 `min`/`sigma(z)` corrected identity，得到

```text
literal V19 determinant
  -> exact Jutila main/error split
  -> corrected signed Farey representation
  -> bare identity branch S(D,sigma(z)u;c).
V24_BARE_FAREY_B_SUM_TO_COMPLETE_KLOOSTERMAN_BILINEAR = PROVED_EXACT_L0
```

其中 `d_phys,d_rough,e_sieve,q_J,d_J,c_F,b_F,u_F,t_F,ell_J,d_BL`全部分型；
`q_J`不能改名为 `c_F`，physical divisor也不能改名为 Jutila divisor。打开
`chi(b_F/c_F+z_F)`后，真正未解对象是一个在外层取绝对值之前保留
identity/`-chi`、`d_J=1/q_J`、prime/hybrid、zero/nonunit/axes/tails及左右半弧的完整
signed `(q_J,c_F,b_F,sigma)` ensemble。

因此解析主路已经分成两个明确 theorem：

```text
V24_SIGNED_q_c_b_COLLECTIVE_PHYSICAL_EMITTER
  = OPEN_NEW_CONSTRUCTION
V24_PRIME_SHELL_JUTILA_ERROR_SIGNED_FAREY_KLOOSTERMAN_THEOREM
  = OPEN_NEW_THEOREM
V24_PRIME_SHELL_JUTILA_MAIN_TO_BP_COLLECTIVE_EMITTER
  = OPEN_NEW_THEOREM.
```

Blomer--Pascadi在真正发射出 fixed-modulus、fixed-unit short arrays后仍可提供 local
`q^(-11/512)` ledger；在 `q=x^(1/3)`上对应 `x^(-11/1536)`，compiler losses之前的
strict margin仍为 `179/38400`。但 source theorem不负责发射 TPC arrays，也不支付
outer labels与 exactly-once reassembly。

三条 scoped错误路线已经停止：printed Lemma 2 的 `max`/fixed-plus literal transfer；
direct GL(3)-divisor theorem transfer；prime-only/factorable splice。Blomer--Li最终
`41/42` theorem使用
`A(n,1)tau(m)`、divisor/GL(3) Voronoi与自己的 clock，不是 literal Möbius/log row；
其 factorable weight为 `q=pt`且 `t`必须 unrestricted smooth，不能与 V23 prime-only
shell拼成同一个 source lock。保留的第三条解析 reserve只能是独立声明的 source-native
factorable auxiliary ensemble，并重新支付 normalizer、error、clock与 physical
reassembly。

所以 V24不是 arithmetic advance，却是路线推进：旧墙“缺第二 refinement”已经压缩为
两个可写定理、一个可构造 auxiliary architecture以及三个明确 STOP。优先级为

```text
1. signed prime-shell error emitter theorem;
2. Jutila main -> BP collective short-array emitter;
3. independent factorable auxiliary ensemble;
4. V23 stable-block dynamics reserve;
5. A1/A2 independent reserves.
```

overall arithmetic advance=`NO`、fixed atom=`0`、strict `1/400=UNPAID`、`L2=NONE`、
TPC-207=false。

## 24. V23 后的罗盘：prime-shell 入口合法，第二 Kloosterman compiler 接棒

V22已经证明 projector branch只重写 V21 paid mean，original diagonal仍是
`S_x`。V23不再从 centered residue marginal找信息，而先冻结 exact Fourier diagonal

```text
S_x=int_0^1 B_x(alpha)W_x(alpha)dalpha.
```

single `q` congruence只检测 determinant被 `q`整除；standard delta也没有
prime-only exactly-once TPC specialization。这两类 shortcut均停止。

新的合法入口是 Blomer--Li `2511.03294v1` §2.1 Lemma 1：令
`Q_mes=x^(1/3)`、source cutoff `Q_src=2Q_mes`，在
`Q_mes<q<=2Q_mes` prime shell上取 `delta=Q_mes^(-2+eta)`，得到 source-backed
Jutila `L2` approximation及 exact main/error split；smooth
`psi:R->[0,1]`、nonempty `L`与
`0<delta<1/2`保持 source hypotheses。它不是 exact delta。当前 crude
`||G_x||_2<=x^(3/2+o(1))`不能支付 error；纯 energy theorem在 `eta=1/32`须达到
`||G_x||_2<=x^(1+theta+o(1))`、`theta<13/4800`。

真正选中的主干是在 Cauchy之前交织第二个 Kloosterman-sensitive major-arc
refinement。Blomer--Pascadi ledger在 `eta=1/32`给

```text
dual support = Q^(17/32),
q-saving = 11/512,
x-saving = 11/1536,
pre-compiler strict margin = 179/38400.
```

所以当前解析 gate为

```text
V23_PRIME_SHELL_JUTILA_KLOOSTERMAN_INTERTWINED_PHYSICAL_COMPILER_GATE
  = OPEN_CONDITIONAL.
```

它必须支付 literal arrays、major-arc second refinement、unit/nonunit/axes、hybrid
zero mode、smoothing/tails、`1/L`、`1/delta`、whole prime ensemble及 one-outer-
absolute exactly-once reassembly。正 margin不是 arithmetic advance；strict
`1/400`仍未付。

动力学侧，`166->168` exact core beta stable但 `q=11`出生，且新模数有十个全部
nonzero DFT frequencies。150个 finite transitions只有 143 个同时 source/carrier
stable；stable scheduling不消除 fiber-wide renormalization。更重要的是，同一个
parameter-independent exact physical return的参数导数恒为零，不能同时充当
transversality function。保留的 reserve必须把 transversality放到独立 critical
relation，并给 fixed parameter/seed、growing affine carrier、summable bad sets与
uniform pointed power bound：

```text
V23_LACUNARY_STABLE_BLOCK_AFFINE_COCYCLE_WITH_SUMMABLE_TRANSVERSAL_BAD_SETS
  = OPEN_NEW_THEOREM.
```

路线排序现在是：V23 analytic compiler第一，V23 dynamics reserve第二，A1/A2保持
独立。overall arithmetic advance=`NO`、fixed atom=`0`、strict
`1/400=UNPAID`、`L2=NONE`、TPC-207=false。

## 23. V22 后的罗盘：projector 不是色散入口，对角编译器与横截回返分叉

V21把原 target精确写成 `S_x=Hbar_Q+Cbar_Q`并支付 `Hbar_Q`。V22把 actual-fiber
conditional expectations记为正交投影 `E_q`，令

```text
Pbar_Q=R_x^(-1)sum_(q in Q_x)E_q,
Cbar_Q=<beta_x^raw,(I-Pbar_Q)w_x^(z)>
      =S_x-Hbar_Q.                                  (23.1)
```

这个式子是新的大路 firewall。对 `r_q=(I-E_q)w`，每个 residue fiber内的和为零，
所以对全部 `h mod q`都有

```text
sum_(t in I_x)r_q(t)e_q(ht)=0.                      (23.2)
```

因此 mod-`q` residue Fourier或直接 additive congruence展开完全看不见 centered
directions；而 `C_q`仍可非零，因为 `beta`在同一 fiber内变化。完整 ensemble也没有
低秩化这一对象：

```text
rank(Pbar_Q)<=sum_q q=O(x^(2/3)),
dim ker(Pbar_Q)>=|I_x|-sum_q q=x/2-o(x),             (23.3)
```

且 `I-Pbar_Q`在该空间上就是恒等。`x=1000`、`q=11,13,17,19`的 exact fixture给
mean-span rank `57`、identity multiplicity `443`。另取 literal coefficient
`beta_166^raw`但刻意设置 synthetic second vector `w_syn=beta_166^raw`，则
全部 residue marginals为零而
`<beta,(I-E_7)w_syn>=2359675/77616`。这只是 operator information-loss witness，
不是 actual `w_166^(z)` covariance或 arithmetic evidence。所以“center后直接 Fourier/Kloosterman”以及
“完整 mesoscopic ensemble自动压缩”都正式 `STOP_SCOPED`。

shift-comb展开进一步给

```text
Cbar_Q=(S_x-Abar_Q)+(Abar_Q-Hbar_Q),
Abar_Q=R_x^(-1)sum_(q,t)beta(t)w(t)/n_q(t)
      =O(x^(1/3+o(1))).                             (23.4)
```

第二项由 V21 paid mean反解；第一项的 diagonal仍是 `S_x`。因此真正解析入口不能从
paid projector branch开始，而必须从 literal SHB-D2 determinant diagonal开始，完成
Möbius/log展开、coprime inversion、Poisson、zero/nonunit/diagonal/tail ledger及
exactly-once reassembly后，才可能调用 Kloosterman engine。Blomer--Pascadi 的 balanced
local theorem若得到无损编译，可提供 `q^(-1/32)=x^(-1/96)`，在未计 compiler losses前
超过 strict `1/400`的 margin为 `19/2400`。但 full-`q` Fourier completion再切
`sqrt(q)` blocks、且只用 black-box Cauchy时，uniform proof会引入可能 sharp 的
`q^(1/4)` factor，因而在没有额外 block structure时不能认证 net gain；只停止这个
Cauchy-only版本。当前解析 gate是

```text
V22_LITERAL_SHBD2_DIAGONAL_POST_POISSON_COMPILER_GATE
  = OPEN_CONDITIONAL.                                (23.5)
```

动力学侧有一个同样 exact但不自带 cancellation的 `L0` 编码。在 profinite odometer
`T(r)=r+1`、distinguished seed `0`上，取

```text
Phi_x(T^t0):=beta_x^raw(t)R_x^(-1)sum_q(I-E_q)w_x^(z)(t),
Cbar_Q=sum_(t in I_x)Phi_x(T^t0).                    (23.6)
```

这证明 exact orbit-sum/Bratteli return，不证明 Logistic mixing estimate。普通 ergodicity
只 center了 `w`，没有 center `beta*w`；observable随 `x`增长且 pointed seed固定，现有
a.e.-seed ASIP/DBC或 a.e.-parameter typicality均不能升级为需要的定理。保留的大胆动力学
gate是构造 positive-measure transversal family，使同一 arithmetic return成为独立于参数的
common-return carrier，并给 coefficientwise exact intertwiner、small carrier mean和同一
good parameter上的 uniform triangular pointed bound：

```text
V22_TRANSVERSAL_COMMON_RETURN_CENTERED_PHYSICAL_CARRIER_GATE
  = OPEN_NEW_CONSTRUCTION.                           (23.7)
```

V22没有 arithmetic advance；它删除一条貌似最直接、实际只绕回 paid mean的伪路，并把
剩余“大路”压成两个可证伪接口。fixed atom=`0`、strict `1/400=UNPAID`、`L2=NONE`、
TPC-207=`false`。下一有限解析关检查 literal diagonal是否能产生 `sqrt(q)`-scale short
support而不付 full-`q` completion loss；下一有限动力学关检查相邻 physical stages的
common-return transversality/parameter derivative。两关独立，不拼接 theorem credit。

## 22. V21 后的罗盘：均值支路已付，中心化协方差成为唯一正面墙

V20说明 terminal innovation不会自动变小；V21因此换到 wrapped mesoscopic clock。
取完整预声明素模 ensemble

```text
Q_mes=x^(1/3),
Q_x={q prime:Q_mes<q<=2Q_mes},
R_x=#Q_x,                                             (22.1)
```

并对同一个 V19 literal `beta_x^raw`与 residual `w_x^(z)`作 actual residue-fiber
分解。逐 `q` exact有

```text
S_x=H_q+C_q,
H_q=sum_a B_(q,a)W_(q,a)/n_(q,a),
C_q=sum_a sum_(t in I_(q,a))beta(t)[w(t)-W_(q,a)/n_(q,a)]. (22.2)
```

这里 `n_(q,a)`是 strict shell中的 actual `floor/ceiling` count，不是 `x/q`；平均整个
ensemble后左边仍是同一个 `S_x`。centered branch又有 exact pair kernel

```text
q divides t-u.                                       (22.3)
```

真正的正面推进在 mean branch。对 sufficiently large `x`有 `q>z=(log x)^K`；
`Lambda(t+2)`与 tensor-local hybrid comparison的 local profiles之差为

```text
d_q(0)=0,
d_q(-2)=-q(q-2)/(q-1)^2,
d_q(a)=q/(q-1)^2 otherwise,
sum_a d_q(a)=0.                                      (22.4)
```

最大型 Bombieri--Vinogradov支付 `Lambda`的 complete-modulus average；exact `q` Euler
factor extraction、rough-divisor truncation、Rosser--Iwaniec fundamental lemma与 CRT
lattice counting另给 hybrid comparison的 uniform all-residue AP remainder。保留
`|beta|<=3d_4`、全部 actual `n_(q,a)`与 `1/R_x`后，完整 loss ledger得到

```text
Hbar_Q=R_x^(-1)sum_(q in Q_x)H_q
 <<_(A,K)x/log^A x                                    (22.5)
```

对每个 fixed target `A`成立。整个 `Q_x`都保留，没有挑选 good `q`。这是

```text
ARITHMETIC_SUBGATE_ADVANCE = YES_F12_ONLY.            (22.6)
```

它不是 TPC arithmetic trigger，因为 exact equivalence现在只是

```text
S_x=Cbar_Q+O_(A,K)(x/log^A x).                        (22.7)
```

六类最接近 primary theorem均不能 literal attachment：现有 AP/BDH结果控制单序列
discrepancy，Ford--Maynard Prop. 4.11假设缺失 Type II，Maynard/Pascadi需要不同
convolution，Zheng的 arbitrary-`q` exponent止于 `7/36`，Blomer--Pascadi仍缺从 physical
sum到 Kloosterman form的 exactly-once reduction/reassembly。因此 current primary是

```text
BRIDGE_B_SHBD2_Q_AVERAGED_CENTERED_PHYSICAL_COVARIANCE
 = OPEN_NEW_ARITHMETIC_THEOREM.                       (22.8)
```

它要求外层唯一绝对值、完整 equal-weight prime ensemble、literal `+2,-1` raw row、
fixed `h0=2`、`x=2X`、actual shell counts与全部 parameter/loss ledger。不得把 separate
AP discrepancy、complete-frequency mean或 good-modulus selection改写成 (22.8)。

centering也不是自动 smoothing。counting-measure projection的 norm为一；对 shell
长度 `H>=q`，centered projection rank精确为 `H-q`，不是 fixed-low-rank bypass。literal
`x=166` raw row在 `M=30,35`的 centered-energy ratios分别为
`16340/192531`与 `3544/6639`。而 `E_30(e_84-e_114)=0`，应用 `p=7` deletion后其
mean在同 fiber变成 `-1/3`，所以 mean-only state不闭合。V21新增 narrow STOP：

```text
DECLARED_TPC_BRIDGE_B_20260807_MESOSCOPIC_WRAPPED_RESIDUE_FIBER_
AUTOMATIC_SIGNED_SMOOTHING_FIXED_LOW_RANK_OR_MEAN_ONLY_DELETION_CARRIER_V1
 = STOP_SCOPED_EXACT_PROJECTION_NORM_ONE_RANK_H_MINUS_q_AND_
   DELETION_NONCOMMUTATION.                            (22.9)
```

真正 signed covariance、合法 martingale/path carrier、A1/A2、O161 parents、pair-native、
H1与 global architecture仍 OPEN。Logistic/Hénon若要取得 credit，必须直接返回 (22.8)
的 distinguished-seed physical scalar，而不是只给正测度、遍历性或 a.e. recurrence。
全局 fixed atom=`0`、strict `1/400=UNPAID`、`L2=NONE`、TPC-207=`false`。

## 21. V20 后的罗盘：innovation 是入口，不是免费降阶

V19把 homogeneous source改成 affine source，这是正确的类型修复；V20进一步证明，
不能把这项修复误读成一个自动变小的 error term。对 terminal no-wrap stage，canonical
innovation满足 exact floor

```text
||eta_p(V)||^2 >= (p-3)/(p-2)||V||^2,                (21.1)
```

而 `p asymp sqrt(x)`，所以它保留趋近全部 physical energy。对 source-locked combined
raw MASTER row还有更强的 exact target comparison：

```text
L_(beta_x^raw)(eta_p(w_x^(z)))
 =sum_(x/2<t<=x)beta_x^raw(t)w_x^(z)(t)
  +O_K(x^(1/2)log^C x).                              (21.2)
```

因此任意 fixed log-power saving在两边等价。把 growing horizon展开也不会产生符号
telescope：各 stage weights逐 coordinate非负且总和为一，terminal stage已带走
`1-O(1/p)`。path-space carrier是 full-dimensional weighted isometry，不是压缩；第一
fixture的 raw/base/terminal-eta/all-eta/union exact ranks为
`65/56/50/54/76`，也没有 finite collapse。

这关闭的是一个足够大的伪大路，而非细节：

```text
DECLARED_TPC_BRIDGE_B_20260807_SHBD2_LONG_HORIZON_SOURCE_INNOVATION_
SMALL_NORM_AUTOMATIC_TELESCOPE_OR_LOW_RANK_BYPASS_V1
  = STOP_SCOPED_EXACT_TERMINAL_NEAR_IDENTITY.         (21.3)
```

真正保留下来的 Bridge B highway变得更干净：

```text
BRIDGE_B_SHBD2_TERMINAL_INNOVATION_SIGNED_PHYSICAL_EVALUATION
  = OPEN_NEW_ARITHMETIC_THEOREM.                      (21.4)
```

也就是说，动力学若要过桥，必须直接证明 prescribed physical signed scalar的 log-power
saving；它可以提供新的机制，但不能靠“innovation”“遍历”“正测度”或“高维编码”这些
名字取得算术 credit。一个合格的 nonautonomous Logistic/symbolic theorem至少要给
target-independent affine input-output law、exact arithmetic event coding、distinguished
seed return与 (21.2) 的 uniform signed bound。Hénon natural extension只在 exact factor
确实保留同一 scalar时作辅助，不独立支付墙。

这也是当前路线图的关键分叉：Bridge B不再寻找自动 smoothing，而直接寻找 signed
physical evaluation theorem；若该 theorem没有新结构，就回到同一个 SHB-D2 arithmetic
core。A1/A2继续独立，不拼接 theorem credit。全局状态保持 fixed atom=`0`、strict
`1/400=UNPAID`、`L2=NONE`、TPC-207=`false`。

## 20. V19 后的罗盘：combined raw row可载，source innovation不可省

V18把下一关写成 `SHB-D2 -> V_k^vee`。V19证明这条箭头必须分成两层。
Ford--Maynard Lemma 5.2的 `h=2,s=1`部分只有两类 ordered raw occurrences，exact
outer constants为 `+2,-1`。冻结一个 derived source-slot/bitmask routing后，每个
nonzero occurrence exactly once落入 H2或 MASTER。于是无需先虚构 Mellin template，
就能定义 canonical combined physical row

```text
beta_x^raw(t)
 =1_(x/2<t<=x)
  sum_(MASTER occurrences over t)
    c_j product_i mu(e_i) log(f_1)/log t.              (20.1)
```

取 `x=2X`，它是 actual physical-window primorial covector；backward pullback先乘新
prime deletion masks，再按 base residue periodize；仅在 no-wrap regime才是 pointwise
mask公式。第一 `k=5,b=7` fixture因此真正非空：120 rows、92 active
coordinates、cumulative exact rank 56，incremental ranks为 `(17,27,12)`。这说明

```text
HB2_RAW_MASTER_TO_PRIMORIAL_COVECTOR = PROVED_EXACT.   (20.2)
```

但 combined raw row不是 separated analytic family。此前失败 subsets的 joint cutoffs
仍缺 literal Perron/Mellin domain、measure、`Xi/Kappa`、free/integrated semantics、
`L1` norm与tails。因此

```text
SHB_D2_SEPARATED_TEMPLATE_REGISTRY = ABSENT,
SHB_D2_ANALYTIC_SAVING = OPEN_NEW_THEOREM.             (20.3)
```

V19对 primal side取得更重要的罗盘修正。对 `gcd(P,p)=1`，`R_p`的 range恰由两条 fiber条件刻画：
deleted copies为零、survivor copies常值。projection与 source innovation为

```text
Pi_p=alpha_p^(-1)R_pR_p^*,
eta_p(V)=(I-Pi_p)V.                                   (20.4)
```

literal residual `w_x^(z)=Lambda(.+2)-b_x^(z)`不满足 homogeneous range。最小
no-wrap same-shell two-survivor constancy witness为 `P_2=6,p_3=5,x=26`：同一
parent的 survivors `14,26`有
residual values `log2,0`。arbitrarily large反例由 sufficiently large distinct primes
`a,b>z=(log x)^K`及 `x=ab+1,t=ab-2`给出。因此

```text
LITERAL_SHB_D2_RESIDUAL_AS_HOMOGENEOUS_R_SOURCE
 = STOP_SCOPED_EXACT_FIBER_RANGE_VIOLATION.            (20.5)
```

source innovation `eta in V_child`与 V16 intertwiner defect
`Err:V_k->B_(k+1)^dyn`不是同型。对任何 raw row只有 exact

```text
L_beta(V)
 =L_(R_p^vee beta)(alpha_p^(-1)R_p^*V)
  +L_beta(eta_p(V)).                                   (20.6)
```

所以“允许 nonzero Err”不自动支付 source innovation。下一主路是

```text
BRIDGE_B_SHBD2_LONG_HORIZON_SOURCE_INNOVATION_RETURN
  = SELECTED_OPEN_NEW_THEOREM.                         (20.7)
```

它要么构造 typed affine source cocycle
`V_(j+1)=R_(p_(j+1))V_j+eta_(j+1)`，要么扩大 state使 residual只作 observable；
随后在 primes `z=(log x)^K`到 physical square-root clock的 growing horizon上统一控制
pulled raw rows对 `eta`的 deterministic physical evaluation，并把 eta-to-dynamics与
V16 `Err`分别付账。这个 target可能很难，但它已经是一个精确可证伪的新定理，而不是
“遍历性推出 seed 0”的换名。

V19仍是 exact L0 architecture advance，不是 arithmetic advance。A1/A2、两个 O161
parents、pair-native、H1与 global architecture保持独立 OPEN；fixed atom=`0`、strict
`1/400=UNPAID`、`L2=NONE`、TPC-207=`false`。

## 19. V18 后的罗盘：typed windowed innovation，而不是 placeholder full hull

V18先修正 dual类型：raw functional用 `R^vee`，normalized-Haar vector用 `R^*`，两者
相差 source/target modulus ratio。精确公式显示 backward survivor atom只塌回一个
parent atom或零，later deletion forcing只塌成 mean；V17担心的反向 atom explosion为
错误方向。

canonical mean/interval core的 exact ranks包括

```text
dim H_(4,6)^IM=119,  dim V_4=P_4=210,
dim H_(5,6)^IM=85,   dim V_5=P_5=2310,
dim H_(6,6)^IM=61,   dim V_6=P_6=30030.
```

全部 pulled increments仍至多三稀疏。对每个 fixed horizon `h`，任意真正物化为
physical-window rows的 typed family（加 Haar mean）满足 upper bound

```text
dim H_(k,k+h)^vee<=1+4^(h+1)p_k^2=o(P_k).             (19.1)
```

若 `k>=4`且该 family还包含 V17 canonical mean/interval core，才另有
`BANDCOUNT_k+1<=dim H_(k,k+h)^vee`。所以 required core-containing exact-return
family的 fixed rank死，而任意 fixed-horizon family的 full-primorial explosion也死；
growing sparse carrier仍有路。即便条件性加入同 stage全部 windowed deletion modes，
rank upper bound仍为 `q+3(BANDCOUNT_k-1)=o(P_k)`。

但完整 hull当前不合法。repo只给 deletion innovation aggregate的 exact Fourier/
adjacent-stage identity，没有 active mode registry；PBAPT与 selected `SHB-D2`仍是
analytic forms，未成为 `V_k^vee` rows。TPC-32 packet frequency又是另一 modulus与
normalization。因此

```text
UNTYPED_PLACEHOLDER_TO_COMPLETE_HULL = STOP_SCOPED,
COMPLETE_HULL_RANK = NOT_TESTABLE_FAIL_CLOSED.         (19.2)
```

global complete characters作为 control会立即给 full rank `P_k`，但不能改写成 actual
windowed family。zero-defect exact intertwiner受 hull rank必要条件约束；V16 nonzero
physical `Err`版本只把 hull当 diagnostic，missing directions由 innovation port进入并在
actual trajectory上支付。

current primary为

```text
BRIDGE_B_TYPED_WINDOWED_FORCED_INNOVATION
  = SELECTED_OPEN_NEW_THEOREM.                         (19.3)
```

下一关不是继续算空 family，而是把 selected `SHB-D2`逐式 materialize为 primorial
covectors；冻结 stage、physical `X`、`A`、fixed `h0=2`、frequency、coefficient class、
normalization与 source locator，再对 `k=5,b=7`算 rank/support/norm/conditioning/loss。

proof/checker见 `bridge_b_backward_hull.md`与
`tpc_bridge_b_backward_hull_checker.py`。V18 registry为 32 rows、SHA-256
`57ddfe6635fe56020516680d9be5732ea39196d0bac5f6d4492a9c7d7890cd9b`。
arithmetic advance=`NO`；fixed atom=`0`、strict `1/400=UNPAID`、`L2=NONE`、
TPC-207=`false`。A1/A2仍是独立 reserves。

## 18. V17 后的罗盘：common fixed rank 停止，sparse dual hull 开工

V16 的 `J_k`是 common stage map：它先于 `X,A,ell`选择，并对每个 `f in V_k`
exact return declared physical duals。固定 `k>=2`、`p=p_k`、`q=p_(k+1)`，同一 stage
包含的整数 physical scales恰为

```text
X_k^int={(p^2-1)/2,...,(q^2-3)/2},
BANDCOUNT_k=(q^2-p^2)/2>=2p_k+2.                        (18.1)
```

对 `k>=4`，`q^2-3<P_k`，所以这些窗口全部无 wrap。actual interval coefficient rows
`w_(k,X)`的 endpoint minor `w_(k,X)(2Y)`为 unit lower triangular；加上 Haar mean后

```text
rank span{mean,w_(k,X):X in X_k^int}=BANDCOUNT_k+1.     (18.2)
```

因此

```text
BRIDGE_B_COMMON_STAGE_FIXED_RANK_EXACT_RETURN
  = STOP_SCOPED_STAGE_BAND_RANK_GROWTH.                 (18.3)
```

这条 STOP不依赖 PNT，也不把 nearby real scales误算为不同 windows。只取整数子族已经
足够。它还封锁 `forall X exists J_(k,X)`冒充 `exists J_k forall X`的量词偷渡。

正面结构为

```text
w_(k,X)-w_(k,X-1)=-e_X+e_(2X-1)+e_(2X),               (18.4)
```

所以 current primary更新为

```text
BRIDGE_B_COMMON_STAGE_GROWING_RANK_SPARSE_CARRIER
  = SELECTED_OPEN_NEW_THEOREM.                          (18.5)
```

下一 gate构造 finite-horizon backward-closed physical dual hull：从 mean、base interval、
三稀疏 increments出发，加入 deletion forcing、additive-Fourier、PBAPT Type-II duals及
`R_p^*` pullbacks。若 hull rank迅速达到 `asymp P_k`，Bridge B sparse road停止；若
dimension、transition sparsity、dual norms与 physical loss均受控，则开始 actual
nonautonomous Logistic construction。

all-translations family有 exact circulant rank `P-gcd(P,L)+1`，但 current gate不含该
family，不能偷加。approximate low-rank return也保持 OPEN，必须给 physical norm中的
width/singular-value theorem。

fixed finite Markov/Ulam dictionary在 common exact return下停止；Logistic infinite-
dimensional transfer space、fixed alphabet加 unbounded memory、未经过 finite level-state
factorization的 Bratteli及 growing Hénon observable family均未被停止。phase-space
dimension不得改写成 observable rank。

proof与 checker见 `research/tpc-big-road/bridge_b_observable_rank.md`及
`research/tpc-big-road/tpc_bridge_b_rank_growth_checker.py`。canonical V17 registry为
24 rows、final-LF SHA-256
`8edf44c0af0146acfe9f0cb7e9c1a72f53bc2a05dc852cac11e547db478f2aac`。

V17是 `EXACT_ACTUAL_PHYSICAL_DUAL_RANK_GEOMETRY_AND_ARCHITECTURE_RETYPE`，不是
arithmetic advance。fixed atom=`0`、strict `1/400=UNPAID`、`L2=NONE`、
TPC-207=`false`；A1/A2仍是独立 reserves。

## 17. V16 后的罗盘：Bridge B 改接 `H_dyn/H3_phys`，不再伪装 H4

V16 对 exact primorial pair cocycle证明

```text
R_p^*R_p=(1-2/p)I,
mean(R_pf)=(1-2/p)mean(f),
(1-2/p)^(-1/2)R_p is an isometric injection.
```

deletion forcing

```text
g_(k,p)=R_p1-(1-2/p)1
```

又与 `R_p(V_k^0)`正交，故

```text
W_(k+1)=R_pW_k+a_k g_(k,p),
||W_k/a_k||^2=1/a_k-1 asymp(log p_k)^2.
```

这不是一个微型谱计算，而是直接决定岛屿地图的桥型：exact sieve centered dynamics
本身没有隐藏的 uniformly contracting complement。任何在全部 centered space上
uniformly lower-coercive的 `J_k`，都不能把 raw logarithmic-rate product exact
intertwine到 uniformly exponentially memory-losing Logistic transfer products；
相对 raw product norm可忽略的 full-operator Duhamel defect也不可能。该 broad cell
只停止 full-space版本，不停止 physical quotient。

当前 Bridge B 主门因此更新为

```text
BRIDGE_B_PHYSICAL_OBSERVABLE_QUOTIENT_INTERTWINER
  = SELECTED_OPEN_NEW_THEOREM.
```

它必须对 target-independent affine class建立 forced-triangular nonautonomous
evolution，并保留 fixed `h0=2`、event、stage/clock、deletion forcing、actual physical
dual family及 accumulated physical error。目标输出是 deterministic Type-II/
physical-evaluation estimate，先改变 `H_dyn/H3_phys`，再接 PBAPT；不是再给一个
ACIP-a.e. 或 Haar-a.e. recurrence theorem。

Bridge B 的 reserve次序是：

1. observable quotient / physical cyclic subspace；
2. Bratteli--Vershik/S-adic aging-clock compression的 rank-growth falsifier；
3. deterministic shadowing，且必须支付 moving-boundary margins；
4. Hénon natural extension，只有 exact factor/event/measure/functional diagram后加入。

proof与 checker见
`research/tpc-big-road/bridge_b_physical_intertwiner.md`及
`research/tpc-big-road/tpc_bridge_b_carrier_checker.py`。canonical V16 registry为
20 rows、final-LF SHA-256
`cc63154e3a1bb21513ed7b86fe30236133d110d48eef191bc3bfab7841bc9fb1`。

V16是 `EXACT_FINITE_OPERATOR_GEOMETRY_AND_ROUTE_REDESIGN`，不是 arithmetic
advance。A1 actual root-number-square master与 A2 paired-Voronoi继续作为独立 reserves；
Bridge B不给它们自动 credit。fixed atom=`0`、strict `1/400=UNPAID`、`L2=NONE`、
TPC-207=`false`。
