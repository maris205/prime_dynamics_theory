# TPC distilled map and bold channel

更新时间：2026-08-06
状态：`BOLD_CHANNEL_V10 / INDUCED_CRT_PRIMITIVE_PROJECTOR_ROUTE_RETYPE`
claim level：`EXACT_CONDUCTOR_PROJECTOR_NORMAL_FORM_PLUS_MONOMIAL_TRACE_BLUEPRINT_WITH_TYPE_IV_AND_PAIRED_VORONOI_OPEN`
编号事实终点：TPC-206；TPC-207 trigger：`false`

本文件把 TPC-1--206 看成 200 多个可审计研究节点，而不是 200 多篇彼此独立的
传统论文。它只做三件事：压缩旧地图、选一条主干、集中管理大胆假设。V10 的完整
公式、proof与独立 checker位于 `research/tpc-big-road/`。正式 theorem
事实仍以 `TPC_HANDOFF.md`、已提交 papers、artifacts与 checkers为准；本文件本身
不是新 theorem evidence，也不解除任何 `STOP_SCOPED` 或 release gate。

## 1. 一句话决策

```text
200+ local research nodes
  -> 13 major obstruction classes
  -> 2 visible bottlenecks
  -> 1 tensor-local hybrid J-to-sqrt(X) prime-producing highway.
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
3. `J_k` 同时保持 mean mode、pair event与 physical functional：必须另有
   `Lambda_X^dyn` 使 `ell_X(f)=Lambda_X^dyn(J_(k_X)f)`，而不只保持一个 symbolic
   word；
4. `Err_k` 的 accumulated physical loss必须满足

   ```text
   sum_(j<k_X)
     |Lambda_X^dyn(Q_(k_X-1)...Q_(j+1) Err_j B_j)|
       = o(a_(k_X) X);
   ```

   不能只给 abstract operator norm而不支付 physical evaluation；
5. `Q_k` 必须实现 forced-triangular cocycle，而非假设 complement invariant；除
   arbitrary-product memory loss外，还须逐 stage传递 (5.1) 的 deletion forcing；
6. 结论必须作用于 distinguished arithmetic section，而不只是 ACIP-a.e. fibers。

如果这些成立，RH-3 类型的 sequential covariance才可能把 logistic estimates传回
physical innovation/profile或 PBAPT 的 Type-II input；不得再把抽象 complement
contraction直接宣布为 `ell_X(W)=o(a_kX)`。这是大胆的 `HYPOTHESIS`，不是现有
isomorphism的改名。若无法构造保持 physical functional与 forcing的 `J_k`，就立即
停止 logistic carrier，回到 direct arithmetic/analytic attack；不再用数值相似性续命。

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
| H_dyn | same stage/time/event/seed forced-triangular intertwiner to nonautonomous dynamics | `HYPOTHESIS` | coefficientwise identity、physical functional、forcing与 uniform evaluation |
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

构造 `J_k,Q_k,Err_k`，显式处理 deletion forcing，先在一般 affine pattern class上
产生可送入 Engine A 的 Type-II或 physical-evaluation estimate。Haar variance已经
独立闭合，重复证明 typical recurrence不算成功；只证明 typical logistic orbit有正
`LRL` mass也不算成功。

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
credit。V10 canonical状态表为：

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

1. **Primary：HB4 exact-half dual-product dispersion**。V9 已把 Gauss-square
   character angle精确化为 prescribed residue的 centered product convolution：

   ```text
   Q_p(-2)=sum_(e_1e_2zw=-2 mod p)
     mu(e_1)W_1(e_1)mu(e_2)W_2(e_2)U_p^sharp(z)V_p^sharp(w).
   ```

   完整 prime cell为 `mu(p)Q_p(-2)`，nonprincipal gate为
   `(p-1)/p[Q_p(-2)-M_p/(p-1)]`。这是 exact finite equivalence，不是 arithmetic
   saving。当前 first subgate是
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
   `u k/(g e_1e_2 a b^2 t^2) (mod rho)`，不在 outer-variable层先取绝对值。Earnst
   root-number-square moment与 Fouvry--Kowalski--Michel--Sawin monomial trace bound
   是合法机制蓝图，但都没有附着 full varying/composite projector gate。
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
centered dual-product theorem作为 first falsifier；full bridge则先按 projector
modulus `rho`分 large prime-like、large complementary conductor与 balanced
varying/composite三段，尝试把 local monomial trace engine编译成 collective theorem。
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

## 11. 对外成果的最终压缩目标

如果主通道存活，TPC-1--206 的最终外部形态应压缩为：

1. 一篇 obstruction/type-system synthesis，解释为何常见伪桥失败；
2. 一篇 parity-breaking affine-transference bold-channel paper，明确 typed gates与
   PBAPT master theorem；
3. 只为真正关闭 `H_occ/H_dyn/H3_phys/H4` 的少数技术论文；
4. 一个可复现 repository，保留 200+ research nodes作为审计证据库。

在形成 theorem-backed channel advance前，不创建 TPC-207，不构建 paper/PDF。
