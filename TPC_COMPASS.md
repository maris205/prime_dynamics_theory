# TPC distilled map and bold channel

更新时间：2026-08-05
状态：`BOLD_CHANNEL_V1`
claim level：`ROUTE_CONSTRUCTION_NOT_TWIN_PRIME_THEOREM`
编号事实终点：TPC-206；TPC-207 trigger：`false`

本文件把 TPC-1--206 看成 200 多个可审计研究节点，而不是 200 多篇彼此独立的
传统论文。它只做三件事：压缩旧地图、选一条主干、集中管理大胆假设。正式 theorem
事实仍以 `TPC_HANDOFF.md`、已提交 papers、artifacts与 checkers为准；本文件本身
不是新 theorem evidence，也不解除任何 `STOP_SCOPED` 或 release gate。

## 1. 一句话决策

```text
200+ local research nodes
  -> 13 major obstruction classes
  -> 2 visible bottlenecks
  -> 1 primorial-diagonal / pointed-recurrence bold channel.
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

精确 finite-sieve moving targets已有正 mass、总 mass发散及 twin-event identity；
所缺是指定 arithmetic point的

```text
CRITICAL_SCALE_POINTED_ODOMETER_SHRINKING_TARGET_RECURRENCE.
```

ordinary a.e. dynamical Borel--Cantelli不能代替这个 pointed theorem。

本文件的工作假说是：A 与 B 可能是同一个“distinguished physical functional看见
centered complement cancellation”的两种坐标。大胆通道的目标是验证这一统一，而
不是继续平行制造局部论文。

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
`p|d(d-2)(d+2)` 产生。这是 `DERIVED_EXACT_COVARIANCE_IDENTITY`，把 H3 从模糊
“需要 decorrelation”推进为一个明确的 shifted local-product summation problem；
它没有给 covariance总和或 pointed discrepancy bound。

## 5. 一个大胆主通道：Primorial Diagonal Renormalization Channel

把

```text
B_k = Pi_k B_k + W_k = a_k * 1 + W_k,
Pi_k f = mean_(G_k)(f) * 1,
W_k=(I-Pi_k)B_k,
mean_(G_k)(W_k)=0
```

作为 exact Haar mean/complement decomposition。physical count满足

```text
ell_X(B_(k_X))
  = a_(k_X) * X + ell_X(W_(k_X)) + O(1).
```

因为 `a_(k_X) asymp 1/(log X)^2`，下面的一侧 pointed discrepancy theorem足以
给大量 twin hits：存在 fixed `eta>0`，对所有充分大 `X`，

```text
ell_X(W_(k_X)) >= -(1-eta) a_(k_X) X.
```

更强而更自然的 working target是

```text
ell_X(W_(k_X)) = o(a_(k_X) X).
```

它可命名为

```text
POINTED_PRIMORIAL_DIAGONAL_COMPLEMENT_DISCREPANCY.
```

这是 `CRITICAL GAP`，不能被写成已证；它本身承载 prime-sensitive endpoint难点。
但它给出了一个可攻击的 operator object：新素数逐 stage 的 replication--deletion
cocycle、一个已知 mean mode、一个 centered complement，以及一个明确的 physical
diagonal functional。解析 far-copy theorem、sequential transfer operators、large
sieve/dispersion与 symbolic dynamics现在都可以围绕同一 object竞争，而不是各说
各话。

该 bound一旦成立就给

```text
ell_X(B_(k_X)) >= eta * a_(k_X) * X + O(1) > 0
```

对所有充分大 `X`，从而每个充分大的 dyadic window都有 twin pair。这里
`DISCREPANCY` 是精确 conclusion；one-sided cone、projective norm或 operator
contraction只是可能的 proof mechanisms，在真正给出 normed spaces与 uniform
estimate前不得与 conclusion混名。

依赖图为：

```text
exact sieve replication--deletion cocycle                     [PROVED]
          |
          +--> full-cycle mean mode a_k and 2C2 ratio          [PROVED]
          |
          +--> physical ell_X is exact twin count              [PROVED]
          |
          v
pointed diagonal complement discrepancy                        [CRITICAL GAP]
          |
          +--> moving-target variance / recurrence             [DERIVED TARGET]
          |
          v
infinitely many twin primes                                   [CONDITIONAL]
```

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
5. `Q_k` 的 complement须对 actual schedule满足 uniform arbitrary-product memory
   loss；
6. 结论必须作用于 distinguished arithmetic section，而不只是 ACIP-a.e. fibers。

如果这些成立，RH-3 类型的 sequential covariance可望把 logistic complement
contraction传回 `ell_X(W_(k_X))`。这是大胆的 `HYPOTHESIS`，不是现有 isomorphism的
改名。若无法构造保持 physical functional的 `J_k`，就立即停止 logistic carrier，
回到 direct arithmetic/analytic attack；不再用数值相似性续命。

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

## 7. H0--H4 集中 ledger

| gate | exact statement | current status | promotion test |
|---|---|---|---|
| H0 arithmetic base | typed `R_p` cocycle、Haar pair mass、odometer moving event与 twin identity | `PROVED` | locked to TPC-1/RH-1--3 objects |
| H1 stage/event carrier | same stage/time/event/seed intertwiner from sieve cocycle to nonautonomous dynamics | `HYPOTHESIS` | coefficientwise operator identity plus physical functional preservation |
| H2 rare mass | full-cycle `a_k asymp log^-2 N` | `PROVED_FULL_CYCLE`; physical evolution attachment `OPEN` | no use of `pi_2(N)` or Hardy--Littlewood lower bound |
| H3 complement covariance | exact CRT two-time identity plus a summable covariance/one-sided discrepancy theorem at natural scale | identity `DERIVED_EXACT`; summation/actual attachment `OPEN` | uniform constants, growing targets, complete loss ledger |
| H4 distinguished seed | pointed arithmetic section satisfies recurrence/discrepancy theorem | `CRITICAL GAP` | direct theorem for the named seed; a.e. membership is insufficient |
| HC closure | H0--H4 imply infinitely many twin primes | `DERIVED_CONDITIONAL` | Chebyshev--Borel--Cantelli or direct one-sided count |

Theorem-state progress只按这张表记录。新增 source或 certificate若不改变 H1--H4，
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

任何一项失败就标记该 construction `STOP_SCOPED`；不再衍生一串微型修补论文。

## 9. 两种 proof engine，只服务同一主通道

TPC并非只剩一张彩票。当前仍有四个 `OPEN` interfaces，但它们不再各自扩张为一条
编号 paper chain，而按下面的合流图服务同一主通道：

```text
pair-native / linear H1 carrier
          |
          v
literal fixed-atom O161 cancellation
          |
          v
small-content far-copy / covariance theorem
          |
          v
pointed moving-target recurrence
          |
          v
TPC
```

其中任一箭头也可能被一个更强的 direct theorem跳过。四个活接口的精确角色是：

| live interface | role | current first missing |
|---|---|---|
| analytic far-copy | 产生 target-coupled collective cancellation/covariance | `Q^3/J` saving / raw zero-column Bessel |
| nonautonomous pointed dynamics | 把 mass与 covariance升级成 infinitely many physical hits | distinguished arithmetic seed recurrence |
| two O161 fixed-atom parents | 提供 determinant-two literal local arithmetic cancellation | growing natural prescribed-atom fixed-power theorem |
| pair-native / H1 | 保证估计作用在同一 actual physical carrier | opened `D`、pair-to-`omega`、linear occurrence与 normalization |

这四项保持 route portfolio意义上的 `OPEN`；主控资源优先给能改变 H1--H4或把上述
合流图缩短的 theorem。只补接口字段但不改变主 ledger，仍不编号。

### Engine A: direct arithmetic/analytic

把 TPC-32 small-content far-copy target重写为对 `W_k` 或其 exact coefficientwise
image的 physical Gram/Bessel bound。成功标准是直接支付 `o(a_(k_X)X)` 或上述 one-sided
margin；普通 marginal large sieve不算成功。

### Engine B: nonautonomous dynamical carrier

构造 `J_k,Q_k,Err_k`，先在 model schedule上证明 moving target covariance，再验证
actual sieve-driven schedule与 distinguished section。成功标准是把 operator
contraction无损传回 `ell_X(W_(k_X))`；只证明 typical logistic orbit有正 `LRL` mass
不算成功。

两个 engines可以并行，但不得生成两个互不相干的 paper chains。它们都必须在 H3
或 H4 上产生状态变化。

## 10. 下一轮只做四个大动作

1. **Exact operator/covariance build**：在一个未编号 working artifact中正式定义
   `R_p`、mean projector、centered complement、copy labels与 `ell_X`；证明
   full-cycle `p-2` law和 physical twin identity，把上节 exact CRT covariance
   product展开成 character/Ramanujan resonance formula并建立独立 checker。这里
   不重复 TPC-1，而是形成同一 operator API。
2. **Stress experiment**：对 actual first many prime stages测量
   `ell_X(W_(k_X))/(a_(k_X)X)`、copy-deletion discrepancy、complement singular values，加入
   random-translation、wrong-shift与scrambled-copy controls。结果只用于判断
   contraction ansatz是否值得证明，不作 theorem claim。
3. **Master theorem attack**：优先寻找 one-sided cone/projective contraction、
   martingale approximation或 target-coupled Bessel theorem；所有文献必须 literal
   接受 growing diagonal functional。
4. **Carrier kill-or-build**：给 logistic intertwiner一个有限期限。若不能同时保持
   event与 physical functional，就记录一个 broad STOP并退出；若能，则集中证明
   actual paired cocycle memory loss与 pointed section theorem。

下一轮结束时只允许三种高层结果：

```text
CHANNEL_ADVANCE: one of H1--H4 genuinely improved;
CHANNEL_REDESIGN: stress/circularity test found a fatal and the spine changed;
CHANNEL_STOP: both engines fail a named master criterion.
```

“又审核了若干相近 source，但主 ledger未变”不再作为独立研究 release。

## 11. 对外成果的最终压缩目标

如果主通道存活，TPC-1--206 的最终外部形态应压缩为：

1. 一篇 obstruction/type-system synthesis，解释为何常见伪桥失败；
2. 一篇 primorial-diagonal bold-channel paper，明确 H0--H4与 master theorem；
3. 只为真正关闭 H1--H4 的少数技术论文；
4. 一个可复现 repository，保留 200+ research nodes作为审计证据库。

在形成 theorem-backed channel advance前，不创建 TPC-207，不构建 paper/PDF。
