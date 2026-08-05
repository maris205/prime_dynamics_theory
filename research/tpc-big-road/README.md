# TPC big road V2: parity-breaking affine transference

更新时间：2026-08-05

状态：`UNNUMBERED_WORKING_ARTIFACT / CHANNEL_REDESIGN_WITH_H3_METRIC_ADVANCE`

```text
ARITHMETIC_ADVANCE = NO
TPC_207_TRIGGER = false
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
```

本目录不是 TPC-207，也不是论文。它把 `TPC_review3.md` 的四条活路压成一条可证伪
的主干，并记录一个新的无条件 metric theorem。所有 TPC-1--206 的 source locks、
`STOP_SCOPED` cells、actuality/provenance 与 normalization firewalls继续有效。

## 1. 先给大胆结论

当前最值得造的“大路”不是

```text
positive Haar mass -> a.e. recurrence -> arithmetic seed 0,
```

因为最后一箭不存在；也不是把 TPC-32/O161 的 quadratic packet直接改名成 primorial
complement，因为两侧尚无 coefficientwise crosslink。可存活的主干是：

```text
general affine-pattern decomposition
        |
        +--> uniform Type I remainder
        |
        +--> determinant-uniform fixed-atom Type II
                         |
                         v
              target-coupled Gram/Bessel reassembly
                         |
                         v
              exactly-once physical cover + full loss ledger
                         |
                         v
                 prime-producing lower bound
                         |
                         v
                     h0 = 2 / TPC.
```

它的 master target命名为

```text
PARITY_BREAKING_AFFINE_PATTERN_TRANSFERENCE_THEOREM (PBAPT).
```

PBAPT必须先对一类与 prime outcomes无关的 admissible affine patterns陈述；孪生素数
只能作为 `H={0,2}` specialization。这样 Type II 与 reassembly是独立、可证伪的
中间定理，而不是把“seed 0 infinitely often”重新命名。

动力学路线保留为第二条同根支路：本轮已把 exact CRT covariance推进成
`H3_METRIC_PROVED`，可推出 Haar-a.e. profinite seed无穷命中；但没有从 Haar-a.e.
到 distinguished arithmetic seed `0` 的箭头。它是结构诊断和 covariance模型，
不是 TPC credit。

## 2. Exact physical deletion-bias cocycle

固定整数区间

```text
I_X = (X,2X] intersect Z,
L_X = |I_X|,
C_k(X) = sum_(n in I_X) B_k(n).
```

令 `p=p_(k+1)>2`。在 stage `k` 的 survivors中，新素数删除

```text
D_(k,p)(X)
  = sum_(n in I_X) B_k(n) 1_(p divides n(n+2)).
```

于是逐项恒等式给

```text
C_(k+1) = C_k - D_(k,p),
a_(k+1) = (1-2/p) a_k.
```

定义实际删失相对 Haar删失的 innovation

```text
epsilon_(k,p)
  = D_(k,p) - (2/p) C_k.
```

若 `E_k=C_k-a_k L_X`，则

```text
E_(k+1) = (1-2/p) E_k - epsilon_(k,p).                 (2.1)
```

更重要的是，对 normalized physical survivor ratio

```text
R_k = C_k/(a_k L_X)
```

有 exact telescope

```text
R_(k+1)
  = R_k - epsilon_(k,p)/(a_(k+1)L_X),

R_K
  = R_(k0)
    - (1/L_X) sum_(k0<=j<K) epsilon_(j,p_(j+1))/a_(j+1).   (2.2)
```

这才是临界 diagonal 的正确 cocycle：不是齐次“mean mode + contracting
complement”，而是每个新 prime都向 complement注入一个 forcing。事实上

```text
W_(k+1)
  = R_p W_k
    + a_k (R_p 1 - (1-2/p)1),                            (2.3)
```

所以任何 logistic/Hénon carrier若不控制该 forcing经 physical functional累积后的
损失，就没有 arithmetic内容。

### 2.1 Exact additive-Fourier bridge

对 `p>2`，加法正交性给

```text
epsilon_(k,p)
  = (1/p) sum_(1<=a<p) (1+e_p(2a))
      sum_(n in I_X) B_k(n)e_p(an).                       (2.4)
```

因此 stage innovation不是一个新发明的统计量；它精确等于 survivor sequence的
非零加法 Fourier modes在两个 deleted residues上的加权和。这是把 primorial
renormalization 接到 dispersion/large-sieve/Type-II技术的合法入口。

式 (2.4) 仍不等于 TPC-32 的 raw channels。后者保留 packet signs、actual masks、
outer labels、content、copy order与 `JQ^2 asymp XQ` normalization；在逐 coefficient
intertwiner出现前，两者只能画成虚线。

## 3. 临界中心修正：V1 strong target降级

V1 曾把

```text
ell_X(W_(k_X)) = o(a_(k_X)X)
```

称为“更自然”的 working target。该中心现在撤销。理由不是数值反例证明 TPC，而是
标准 endpoint heuristic已经显示 full-cycle Haar mean与 critical physical main不是
同一个 main term：

```text
a_(k_X) X
  ~ 8 C_2 exp(-2 gamma) X/log^2 X,

HL predicted twin count in (X,2X]
  ~ 2 C_2 X/log^2 X,

predicted ratio
  = exp(2 gamma)/4
  = 0.793054740... .
```

故标准预期为

```text
ell_X(W_(k_X))
  ~ (exp(2 gamma)/4-1) a_(k_X)X,
```

不是小 `o`。这里 Hardy--Littlewood只用于诊断 normalization，绝不作为 theorem
premise或 TPC evidence。`tpc_big_road_lab.py --stress` 对有限 `X` 的 exact sieve
profile也直接报告该 ratio；有限计算不作渐近结论。

正确的中间对象应是 critical pair-sieve/Buchstab profile

```text
C_k(X) = a_k X Phi_2(log X/log p_k) + Error_k(X),          (3.1)
```

其中 `Phi_2` 目前只是待定义/待证明的 renormalized profile；不得从 single-pattern
heuristic倒推出它，更不得断言 `Phi_2(2)=exp(2 gamma)/4` 为已证。真正充分但很强的
one-sided endpoint仍是

```text
C_(k_X)(X) >= eta a_(k_X)X
```

对所有充分大 `X`；它会给每个大 dyadic block的正确量级下界，因而比“无穷多个”
更强，不能伪装成弱 bridge。

## 4. 新的无条件结果：Haar moving variance `O(N)`

令

```text
X_arith = Z_hat,
T(x)=x+1,
y_n=sqrt(n+2),
E_n={x:p does not divide x(x+2) for every p<=y_n},
Z_n(x)=1_(E_n)(T^n x),
alpha_n=mu(E_n).
```

这里 `mu` 为 Haar probability。对 `m<n`、`d=n-m`、`q=y_m`，CRT exact identity为

```text
Cov_mu(Z_m,Z_n)
  = alpha_m alpha_n (K_q(d)-1).
```

### Theorem 4.1 (uniform resonance partial sums)

对所有 `q>=2` 与所有整数 interval `I`，有 explicit bound

```text
|sum_(d in I)(K_q(d)-1)|
  <= D(q)
  := 6 product_(5<=p<=q)(1-2/p)^(-2)
  << (log(2q))^4.                                          (4.1)
```

证明是完全有限的 local expansion。记 `k_p(d)` 为 `K_q` 的 `p`-factor。则

```text
k_2(d) = 2 1_(2|d),
k_3(d) = 3 1_(3|d),
```

而对 `p>=5`，

```text
k_p(d)
 = 1 - 4/(p-2)^2
   + 2p/(p-2)^2 1_(p|d)
   + p/(p-2)^2
       (1_(p|d-2)+1_(p|d+2)).                             (4.2)
```

每个 local factor在完整 residue system上的 mean为 `1`，其 coefficient `l1` norm为

```text
2                         (p=2),
3                         (p=3),
(1-2/p)^(-2)              (p>=5).
```

把 product展开成 compatible CRT residue classes。每个 class在任意 interval中的
count与 `|I|/modulus` 相差至多 `1`；完整周期 mean又恰为 `1`，所以左侧至多

```text
6 product_(5<=p<=q)(1-2/p)^(-2) << (log(2q))^4,
```

其中最后一步只是 Mertens product upper bound。这证明 (4.1)。

### Theorem 4.2 (Haar moving-target variance)

若

```text
S_N=sum_(3<=n<=N) Z_n,
A_N=E_mu S_N=sum_(3<=n<=N) alpha_n,
```

则

```text
Var_mu(S_N) << N.                                         (4.3)
```

证明：对固定 `m`，置 `g_m(d)=K_(y_m)(d)-1`。Theorem 4.1 对其所有 partial sums给
`D(y_m)`；`alpha_(m+d)` 单调不增。Abel summation于是给

```text
|sum_(1<=d<=N-m) alpha_(m+d)g_m(d)|
  <= alpha_(m+1)D(y_m).
```

这里不需要留下 logarithmic loss。对 `y>=3`，

```text
alpha(y)=(1/6) product_(5<=p<=y)(1-2/p),
alpha(y)^2 D(y)=1/6.                                      (4.3a)
```

因此乘上外面的 `alpha_m` 后，每个 `m` 的 grouped off-diagonal contribution
至多 `1/6`。对 dyadic block
`S_X=sum_(X<n<=2X)Z_n`，diagonal也至多 `X/6+O(1)`，并注意 variance中
off-diagonal出现两次，得到更明确的

```text
Var_mu(S_X) <= X/2+O(1).                                  (4.3b)
```

累积版本 (4.3) 随即成立。

又因 `A_N >> N/log^2N`，Chebyshev与平方子序列 Borel--Cantelli给

```text
S_N -> infinity along a subsequence for mu-a.e. x.         (4.4)
```

这是 theorem-state 的真实推进：

```text
H3_METRIC = PROVED_HAAR_MOVING_VARIANCE_O_N.
```

但 (4.4) 对 distinguished `x=0` 没有结论。含 `0` 的 level cylinder质量约
`exp(-(1+o(1))sqrt N)`，远小于 Chebyshev exceptional bound；坏集完全可能在每层
都包含 `0`。因此不存在

```text
H3_METRIC -> H4_POINTED
```

的免费箭头。

## 5. Review3 四路汇流后的 typed map

目前有两个 exact connected components，而不是一个已经交换的 diagram。

### 5.1 Primorial component

令

```text
D_k={(d,e):d|P_k,e|P_k},
c_k^sieve(d,e)=mu(d)mu(e),

(M_k c)(r)
  = sum_(d,e|P_k)c(d,e)1_(d|r)1_(e|r+2),
Sigma_k=(I-Pi_k)M_k.
```

有限 Möbius inversion逐 residue给

```text
M_k c_k^sieve = B_k,
Sigma_k c_k^sieve = W_k.                                  (5.1)
```

所以 primorial side已经有 literal signs、masks、fixed `h0=2`、physical interval、
stage、natural normalization与 centering。

### 5.2 Packet/O161 component

TPC-32 的合法 local specialization为

```text
d=d_0+st,
U(t)=u_*+ell*j*t,
s*u_*-ell*j*d_0=2,
coefficient=mu(d_0+st)mu(u_*+ell*j*t).
```

它经 TPC-34/37 TT-star/Gram/orbit slicing通向 small-content far-copy energy；该链
内部合法，但输出是 quadratic energy/residual，不是 (5.1) 的 linear coefficient
array。O161 affine values一般也不是 `P_k` 的 divisors；取 smooth part不保持 Möbius
sign。

因此当前 broad verdict为

```text
PAIR/O161/PACKET_TO_PRIMORIAL_DIRECT_COMPOSITION_V1
  = STOP_SCOPED_OBJECT_AND_LINEAR_QUADRATIC_MISMATCH.
```

这不停止两侧各自推进；它停止画一条没有 source-backed operator的实线。

### 5.3 唯一允许重开该 crosslink 的大型命题

对完整 actual `h0=2` packet family，必须构造 pre-TT-star linear occurrence lift
`L_X` 与 source-backed operator `J_X`，使

```text
Sigma_k J_X L_X c_X = nu_X W_k + R_X                 (5.2)
```

在 `V_k` 中逐 residue成立，并且

```text
ell_X Sigma_k J_X L_X c_X
  = NormReturn_X(PhysicalReassembly_X(c_X)),

|ell_X(R_X)| = o(nu_X a_k X).                            (5.3)
```

所有 signs、masks、weights、outer labels、multiplicities、prefix order、clocks与
normalizations必须同一 source ledger支付。只得到 scalar equality、post-TT-star
pair inversion或把 `XQ` 改名为 `a_kX`，均判失败。

## 6. PBAPT 的 theorem contract

PBAPT不预先声称为真；它是未来所有“大路”工作的唯一总合同。

输入是一类预先声明的 affine systems

```text
L_1(z)=d+sz,
L_2(z)=u+az,
s*u-a*d=D != 0,
```

以及 independently specified physical packets。一个合格 theorem必须同时给：

1. literal physical coefficients和 fixed physical pattern；
2. coefficientwise Buchstab/Heath--Brown/Möbius decomposition；
3. 统一 `X/N/q`、prefix domain与全部参数范围；
4. uniform Type I remainder；
5. determinant-uniform natural-scale Type II saving；
6. actual masks、weights、outer labels与 multiplicities；
7. target-coupled Gram/Bessel reassembly，不丢 raw zero column；
8. all-`D` uniformity、tail-failure、A/B selection与 exactly-once cover；
9. original/global normalization return；
10. 完整 physical-loss ledger，并在 TPC specialization支付 strict endpoint。

现代 prime-producing sieve框架明确把 Type I 与非平凡 Type II作为素数下界机制；
无 Type II 时 parity obstruction可产生完全没有 primes的伪序列。这里采用
Ford--Maynard, *On the theory of prime-producing sieves*,
<https://arxiv.org/abs/2407.14368> 作为框架 source lock，而不是声称其现成 theorem
已经验证 TPC packet hypotheses。经典 asymptotic sieve同样把额外 bilinear axiom作为
突破 parity 的关键，见 Friedlander--Iwaniec,
<https://annals.math.princeton.edu/articles/13036>。

### 6.1 Ford--Maynard 两个直接候选的 fail-closed 结果

这个 framework给主路提供合同，但两个最直观的代入都尚未进入其 theorem。

候选 A 取

```text
a_r=B_(k_X)(r)/a_(k_X),
b_r=1,
w_r=a_r-b_r.
```

它在 multiplier `m=2` 已失败：`B_(k_X)(2n)=0`，故相应 Type I sum为
`-X/4+O(1)`，不是任意 log-power saving。

候选 B 取

```text
a_r=Lambda(r+2)          or (log X)1_(r+2 prime),
b_r=1.
```

在 prime `r` 上求和时，prime-indicator版本是 exact weighted twin count；
von Mangoldt版本还含 `r+2` 为高次 prime power的标准低阶 tail。故若完整 hypotheses
成立，它仍会给干净的 conditional TPC bridge。但它同样在 `m=2` 失败；
von Mangoldt版本有

```text
sum_(X/2<2n<=X)(Lambda(2n+2)-1)
  = -X/4+O((log X)^2),
```

因为非零项只可能来自 `2n+2` 为 2 的幂。一个 locally matched comparison或
`W`-trick或许能先消除这些有限 local biases，但本轮没有构造它。即使修复，首个
真正大墙仍是 arbitrary divisor-bounded coefficients下的 multiplicative Type II；
第 4 节 additive shift covariance不推出该 `mn`-bilinear estimate。

```text
FM_DIRECT_SURVIVOR_WITH_b_1 = FAIL_TYPE_I_AT_m_2
FM_SHIFTED_PRIME_WITH_b_1 = FAIL_TYPE_I_AT_m_2
FM_LOCALLY_MATCHED_COMPARISON = NOT_CONSTRUCTED
FM_MULTIPLICATIVE_TYPE_II = OPEN
```

## 7. 两个 engine，只有一个 endpoint

```text
Engine A (primary)
  actual linear carrier
    -> fixed-atom Type II
    -> target-coupled far-copy reassembly
    -> prime-producing sieve lower bound
    -> physical h0=2 endpoint.

Engine B (proved metric diagnostic)
  exact CRT local product
    -> uniform resonance partial sums
    -> Haar Var(S_N)=O(N)
    -> a.e. moving recurrence
    -X-> distinguished seed 0.
```

Logistic/Hénon只有在构造 target-independent、uniformly bounded、forced-triangular
quasi-intertwiner，并保持 event、seed与 physical evaluation时才重新进入 Engine A。
`RLR^infinity`、typical ACIP、positive fixed cylinder measure或 area preservation本身
都不占 proof credit。

## 8. 接下来只做三个大动作

1. **FM/Buchstab compiler**：把 shifted-prime candidate与 actual TPC decomposition
   对齐到明确 Type I/II hypotheses；第一处缺失必须定位为一个 formula/range，而不是
   “parity barrier”四个字。
2. **General fixed-atom theorem attack**：先证明或否证 determinant-uniform Type II
   class，再谈 TPC specialization；不得用 block/cumulative、metric/prescribed或
   logarithmic/natural互换。
3. **Target-coupled reassembly**：以 (5.2)--(5.3) 为唯一 crosslink gate，构造或
   广义否证 packet到 primorial/physical carrier的线性 pushforward。

若三者均没有 theorem-state变化，发布一个 broad `CHANNEL_STOP`，不要再生成小论文。
若 `H_occ/H_dyn/H3_phys` 任一发生 theorem-backed推进，更新本 artifact与
`TPC_COMPASS.md`；它仍不自动
触发 TPC-207。

## 9. 可复核工具

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python research/tpc-big-road/tpc_big_road_lab.py --check
python research/tpc-big-road/tpc_big_road_independent_checker.py --check
python research/tpc-big-road/tpc_big_road_lab.py --stress --x 10000 100000 1000000
```

两个 `--check` 入口只读且互相独立；不会修改 committed artifacts。independent
checker提供 finite exact fixtures与 mutations，universal `q/I`、Abel及
Borel--Cantelli量词仍由第 4 节符号证明承担。`--stress` 只把 JSON写到 stdout，
不创建文件。
