
# TPC big-road paper candidate ledger

更新时间：2026-09-03

状态：**TPC357_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_NORM_SCALE_LADDER / FIXED_POWER_CREDIT_NONE / FULL_GATE_B_OPEN**

本文件与路线图平行维护，作用是把连续探索中的可发表材料从长篇 handoff 中逐步抽出。
它不是 theorem evidence；正式数学状态仍以当前 proof、checker、TPC_HANDOFF.md 页首
及 current section 为准。

## 0.151 current：TPC-357 operator-norm scale ladder

项目：papers/tpc-357-operator-norm-scale-ladder/

类型：**NUMERICALLY_CERTIFIED_FINITE_OPERATOR_NORM_SCALE_LADDER**。

TPC-357 冻结 TPC-356 geometry-only adversarial selection 得到的三个 origins
`38423,42010,45597`，把 count ladder 扩展为 `256,512,1024,2048`，并在
`Q=24,54,80`、kernel exponents `1,2` 与四种 sign laws 上完成 operator-only
replay。每个 raw/normalized law matrix 都记录 Schur row-sum 与 Frobenius envelope，
共 `288` rows；all-plus raw/normalized matrix 的极端 eigenvalues 另在 `72` rows
上重放。父代代码与证书均 hash-locked，选择与本篇均不使用 source response。

最强正结果：normalized Schur maximum 为 `0.8077815961017315`，all-plus normalized
spectral maximum 为 `0.62665294142584216`，而 raw all-plus spectral maximum 为
`1542.7455490253569`；所有记录的 spectral values 均满足有限 Schur/Frobenius
envelopes。有限 transition audit 给出 54 个相邻 count transitions 中 normalized
all-plus spectral `15` 增、`35` 降、`4` 平（guard `1e-6`）。

最强 obstruction：normalized spectral decay 并不单调，且有限 cap 没有 origin/scale
uniformity。于是 `TPC357_SCALE_MONOTONE_DECAY=REFUTED_SCOPED_ON_DECLARED_LADDER`，
而不是 asymptotic refutation；growing operator bound、source-uniform arithmetic
`L2`、Route-B reassembly 与 twin-prime endpoint 仍 open。

开放定理：fresh origin-scale spectral holdout 或 uniform masked-operator theorem。
`ARITHMETIC_ADVANCE=NO`、`FIXED_POWER_CREDIT=0`、`FULL_GATE_B=OPEN`、
`TWIN_PRIME_RESULT=NONE`；official evaluator files absent，local Bridge-B 为
fail-closed fallback。

可复用结构：

    frozen geometry normalization -> all-law Schur/Frobenius envelope
      -> all-plus spectral scale ladder -> independent reverse-shell replay
      -> finite cap plus explicit monotonicity obstruction

ROUND2_CLUE：`ATTACK_THE_FINITE_NORMALIZED_SPECTRAL_CAP_ON_A_PREREGISTERED_FRESH_ORIGIN_SCALE_HOLDOUT_BEFORE_ANY_UNIFORM_CLAIM`。

    TPC357_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_OPERATOR_NORM_SCALE_LADDER
    TPC357_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
    TPC357_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
    TPC357_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
    TPC357_NORMALIZED_SCHUR_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC357_ALL_PLUS_SPECTRAL_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC357_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
    TPC357_GROWING_OPERATOR_BOUND = OPEN
    TPC357_SOURCE_UNIFORM_L2 = OPEN
    TPC357_ARITHMETIC_ADVANCE = NO
    TPC357_FIXED_POWER_CREDIT = 0
    TPC357_FULL_GATE_B = OPEN
    TPC357_TWIN_PRIME_RESULT = NONE
    TPC357_STATUS = NUMERICALLY_CERTIFIED_FINITE_OPERATOR_NORM_SCALE_LADDER

## 0.150 previous：TPC-356 geometry-adversarial normalization holdout

项目：papers/tpc-356-geometry-adversarial-normalization-holdout/

类型：**NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT**。

TPC-356 冻结 TPC-355 的 unsigned mask-energy diagonal congruence，并把 origin
selection 预先固定为 geometry-only adversarial rule：在 `38001+211j`、`0<=j<=50`
的 51 个候选上，以 count `256` 的六个 `(Q,s)` geometry spread 最大值排序，再用
最小间隔 `1536` 的 greedy rule 选出 `38423,42010,45597`。该过程不读取 V59
source response 或 sign law；随后按父代 counts、shell anchors、exponents 与四种
laws 重放 `216` rows。

最强正结果：raw 与 normalized alignment 均为 `216/216` positive；all-plus minimum
从 `0.63140161782616067` 升至 `0.65046429467683675`，mean 从
`0.8687258535297816` 升至 `0.87560762679420479`，有限 gains 分别为
`0.019062676850676086` 与 `0.0068817732644231855`。选择规则的确定性与
response-blindness 为 `PROVED_EXACT_FINITE`，回放为
`NUMERICALLY_CERTIFIED_FINITE`。

最强 obstruction：几何 spread、归一化对角与 normalized operator 没有 growing-origin
控制；selected panel 的 normalized all-plus minimum 仍低于 TPC-355 higher-panel
minimum。因此 finite adversarial gain 不能升级为 uniform transfer 或 arithmetic
bound。

开放定理：origin/scale stability、source-uniform literal masked arithmetic `L2`、
growing masked operator bound 与 Route-B typed reassembly。`ARITHMETIC_ADVANCE=NO`、
`FIXED_POWER_CREDIT=0`、`FULL_GATE_B=OPEN`、`TWIN_PRIME_RESULT=NONE`；official
evaluator files absent，local Bridge-B 只是 fail-closed fallback。

可复用结构：

    frozen response-blind normalization -> geometry-only candidate scan
      -> separated adversarial origins -> raw/normalized paired replay
      -> finite gain plus explicit uniformity firewall

ROUND2_CLUE：`TEST_ORIGIN_SCALE_STABILITY_OR_OPERATOR_NORM_CERTIFICATE_BEFORE_ANY_ARITHMETIC_REASSEMBLY`。

    TPC356_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT
    TPC356_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_DETERMINISTIC
    TPC356_SELECTION_RESPONSE_INDEPENDENCE = PROVED_EXACT_FINITE
    TPC356_PANEL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
    TPC356_RAW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
    TPC356_NORMALIZED_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
    TPC356_ALL_PLUS_MIN_GAIN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC356_ALL_PLUS_MEAN_GAIN = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC356_UNIFORM_TRANSFER = OPEN
    TPC356_SOURCE_UNIFORM_L2 = OPEN
    TPC356_MASKED_OPERATOR_BOUND = OPEN
    TPC356_ARITHMETIC_ADVANCE = NO
    TPC356_FIXED_POWER_CREDIT = 0
    TPC356_FULL_GATE_B = OPEN
    TPC356_TWIN_PRIME_RESULT = NONE
    TPC356_STATUS = NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT

## 0.149 previous：TPC-355 position-aware mask-energy normalization

项目：papers/tpc-355-position-aware-mask-energy-normalization/

类型：**NUMERICALLY_CERTIFIED_FINITE_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_AUDIT**。

TPC-355 承接 TPC-354 的 higher-origin floor obstruction，预先定义一个只依赖
unsigned literal mask geometry 的对称 diagonal congruence。对每个 prime component
`B_p` 取 `G_u=sum_(p,t)B_p(u,t)^2`，再令
`A#=D_G^(-1/2) A D_G^(-1/2)`。该 geometry 不使用 V59 source、response 或
sign law。TPC-353 low parent、TPC-354 higher parent 与 fresh origins
`29001,33001,37001` 三面板均冻结 counts `256,512,1024`、shell anchors
`Q=24,54,80`、exponents `1,2`、四种 sign laws、`H=66` 与 cutoff `50000`，共
`648` law-level rows。

最强正结果：raw 与 normalized 两套 replay 各有 `647/648` positive、`1/648`
negative、`0` unresolved；all-plus minimum 的 TPC-353→TPC-354 drop 从
`0.042151146184724153` 降至 `0.026236988152766205`，有限 reduction fraction
为 `0.37754982894688971`，且 fresh normalized minimum 为
`0.66413980630867930`。

最强 obstruction：normalized all-plus mean drop 为
`0.024839744603963321`，高于 raw 的 `0.021249745559872912`；fresh panel 的
mod-4 normalization 仍有负 row，higher-panel half-split minimum 也下降。因此
minimum-floor repair 只能记为 finite partial，mean/law-uniform repair 为
`REFUTED_SCOPED`，不能外推为 uniform masked bound。

开放定理：source-uniform literal masked arithmetic `L2`、growing position-aware
operator bound、canonical sign law 及 Route-B typed reassembly。`ARITHMETIC_ADVANCE=NO`、
`FIXED_POWER_CREDIT=0`、`FULL_GATE_B=OPEN`、`TWIN_PRIME_RESULT=NONE`；official
evaluator files absent，local Bridge-B fail-closed。

可复用结构：

    literal masked component -> unsigned geometry diagonal -> finite congruence
      -> raw/normalized polarization -> parent + fresh holdout -> repair firewall

ROUND2_CLUE：`TEST_ADVERSARIAL_POSITION_NORMALIZATION_OR_LAW_INVARIANT_BOUND_ON_FRESH_ORIGINS`。

    TPC355_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_AUDIT
    TPC355_GEOMETRY_DEFINITION = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC355_DIAGONAL_CONGRUENCE = PROVED_EXACT_FINITE
    TPC355_OPERATOR_POLARIZATION = PROVED_EXACT_FINITE
    TPC355_PANEL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_648_ROWS
    TPC355_RAW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_648_ROWS
    TPC355_NORMALIZED_REPLAY = NUMERICALLY_CERTIFIED_FINITE_648_ROWS
    TPC355_ALL_PLUS_FLOOR_REPAIR = NUMERICALLY_CERTIFIED_FINITE_PARTIAL
    TPC355_ALL_PLUS_MEAN_REPAIR = REFUTED_SCOPED
    TPC355_ALL_LAW_POSITIVE_ALIGNMENT = REFUTED_SCOPED
    TPC355_SOURCE_UNIFORM_L2 = OPEN
    TPC355_MASKED_OPERATOR_BOUND = OPEN
    TPC355_ARITHMETIC_ADVANCE = NO
    TPC355_FIXED_POWER_CREDIT = 0
    TPC355_FULL_GATE_B = OPEN
    TPC355_TWIN_PRIME_RESULT = NONE
    TPC355_STATUS = NUMERICALLY_CERTIFIED_FINITE_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_AUDIT

## 0.148 previous：TPC-354 higher-origin masked L2 holdout

项目：papers/tpc-354-higher-origin-masked-l2-holdout/

类型：**NUMERICALLY_CERTIFIED_FINITE_HIGHER_ORIGIN_MASKED_L2_HOLDOUT**。

TPC-354 是 TPC-353 的 origins-only disjoint holdout。它保持同一个 finite V59
source `beta=Lambda-b`、literal two-endpoint divisibility-masked operator、三个
source counts `256,512,1024`、shell anchors `Q=24,54,80`、两种 exponent、四种
预声明 sign laws、`H=66` 与 source cutoff `50000`，只把 origins 从
`6001,8001,10001` 移到 `21001,23001,25001`。有限 operator polarization identity
与 normalized Cauchy envelope 仍为 `PROVED_EXACT_FINITE`；source attachment 是
声明模型内的 exact finite construction。

最强正结果：独立 reverse-shell replay 在 `216/216` rows 上复现 operator output，
所有 rows 都有正 alignment；exact rational anchor、8-mutation stress 和
normal/optimized local Bridge-B 均通过。all-plus output coefficient 的范围为
`0.65076036812307647--0.99135023146539858`，mean 为
`0.87436211602135017`；holdout 上 source coefficient 为
`0.36357606682978283--0.38648419369238701`。

最强 obstruction：相对 hash-locked TPC-353 parent，all-plus minimum shift 为
`-0.042151146184724153`，mean shift 为 `-0.021249745559872912`。因此正 transfer
保留，但低-origin all-plus floor 不能被当作 uniform higher-origin floor；同时
output coefficient 仍显著依赖 sign law，source coefficient 不能单独控制 masked
output。该 floor-transfer 命题记为 `REFUTED_SCOPED`。

开放定理：source-uniform literal masked arithmetic `L2`、position-aware uniform
masked-operator bound、canonical sign law，以及它们与 Route-B typed reassembly
的连接。`ARITHMETIC_ADVANCE=NO`、`FIXED_POWER_CREDIT=0`、`FULL_GATE_B=OPEN`、
`TWIN_PRIME_RESULT=NONE`；official evaluator files absent，local Bridge-B
fail-closed。

可复用结构：

    source residual -> literal masked operator -> exact polarization
      -> disjoint origin holdout -> parent-locked floor firewall

ROUND2_CLUE：`TEST_POSITION_AWARE_MASKED_BOUND_ORIGIN_SCALE_NORMALIZATION_OR_CONTROLLED_SIGN_LAW_SUBSPACE`。

    TPC354_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_HIGHER_ORIGIN_MASKED_L2_HOLDOUT
    TPC354_FINITE_OPERATOR_POLARIZATION = PROVED_EXACT_FINITE
    TPC354_FINITE_CAUCHY_ENVELOPE = PROVED_EXACT_FINITE
    TPC354_SOURCE_NATIVE_MODEL = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC354_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
    TPC354_POSITIVE_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_216_OF_216
    TPC354_HIGHER_ORIGIN_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
    TPC354_OUTPUT_SOURCE_MISMATCH = NUMERICALLY_CERTIFIED_FINITE
    TPC354_ALL_PLUS_FLOOR_TRANSFER = REFUTED_SCOPED
    TPC354_UNIFORM_L2 = OPEN
    TPC354_MASKED_OPERATOR_BOUND = OPEN
    TPC354_ARITHMETIC_ADVANCE = NO
    TPC354_FIXED_POWER_CREDIT = 0
    TPC354_FULL_GATE_B = OPEN
    TPC354_TWIN_PRIME_RESULT = NONE
    TPC354_STATUS = NUMERICALLY_CERTIFIED_FINITE_HIGHER_ORIGIN_MASKED_L2_HOLDOUT

## 0.147 previous：TPC-353 source-native masked L2 polarization

项目：papers/tpc-353-source-native-masked-l2-polarization/

类型：**NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_MASKED_L2_POLARIZATION_AUDIT**。

TPC-353 承接 TPC-352 冻结 incidence branch 后的 source-native `L2` 路线。它把
继承的 V59 finite residual `beta=Lambda-b` 直接送入 literal two-endpoint
divisibility-masked operator，而不是只在 source vector 上读取 polarization。对任意
有限实矩阵 `A`，精确恒等式

```text
||A(L-b)||_2^2 = ||AL||_2^2 + ||Ab||_2^2 - 2 <AL,Ab>
```

以及相应的 normalized coefficient `kappa_A` 与 Cauchy envelope 均为
`PROVED_EXACT_FINITE`。冻结面板为 origins `6001,8001,10001`、source counts
`256,512,1024`、shell anchors `Q=24,54,80`、exponents `1,2`、四种预声明 sign
laws、`H=66` 和 source cutoff `50000`，共 `216` rows；该面板声明为与
TPC-328--TPC-352 active panels disjoint 的 fresh low-origin panel。

最强正结果：literal operator attachment 的 `216/216` rows 都有正 output
alignment，且 exact anchor、independent reverse-shell replay、8-mutation stress
和 normal/optimized Bridge-B 均通过。all-plus output coefficient 的范围为
`0.69291151430780062--0.99626802812598902`，同窗 source coefficient 只有
`0.39570365481042707--0.43581376702257324`；这把 source residual 与 physical
operator cross term 接上了一个可复核的有限 interface。

最强 obstruction：output coefficient 依赖 sign law 且不由 source coefficient 决定。
全体 output range 为 `0.007748502598008385--0.99626802812598902`，
output-minus-source range 为 `-0.41063272009685658--0.59337758362080639`；
因此 source-level cancellation 不能升级为 source-uniform masked arithmetic `L2`。

开放定理：source-uniform literal masked arithmetic `L2`、canonical sign law 或
position-aware uniform masked-operator bound，以及其 Route-B typed reassembly。
`ARITHMETIC_ADVANCE=NO`、`FIXED_POWER_CREDIT=0`、`FULL_GATE_B=OPEN`、
`TWIN_PRIME_RESULT=NONE`；official evaluator files absent，local Bridge-B
fail-closed。

可复用结构：

    inherited source residual -> literal masked operator -> exact polarization
      -> Cauchy envelope -> law/origin holdout -> source/operator firewall

ROUND2_CLUE：`TEST_SOURCE_NATIVE_L2_CROSS_TERM_ON_DISJOINT_HIGHER_ORIGINS_OR_BUILD_POSITION_AWARE_MASKED_BOUND`。

    TPC353_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_MASKED_L2_POLARIZATION_AUDIT
    TPC353_FINITE_OPERATOR_POLARIZATION = PROVED_EXACT_FINITE
    TPC353_FINITE_CAUCHY_ENVELOPE = PROVED_EXACT_FINITE
    TPC353_SOURCE_NATIVE_MODEL = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC353_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_ROWS
    TPC353_POSITIVE_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_216_OF_216
    TPC353_OUTPUT_SOURCE_MISMATCH = NUMERICALLY_CERTIFIED_FINITE
    TPC353_UNIFORM_L2 = OPEN
    TPC353_MASKED_OPERATOR_BOUND = OPEN
    TPC353_ARITHMETIC_ADVANCE = NO
    TPC353_FIXED_POWER_CREDIT = 0
    TPC353_FULL_GATE_B = OPEN
    TPC353_TWIN_PRIME_RESULT = NONE
    TPC353_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_MASKED_L2_POLARIZATION_AUDIT

## 0.146 previous：TPC-352 adversarial reciprocal-shell holdout

项目：papers/tpc-352-reciprocal-shell-adversarial-holdout/

类型：**PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT**。

TPC-352 是 TPC-351 的预声明 disjoint holdout。冻结 origins
`96097,120097,144097`、长度 `256,512,1024`、shell anchors
`Q=64,128,256,512`、两种 source law 与两种 exponent；保持同一 reciprocal rule
`gamma_j=1/p_j-r^(-1)sum_k1/p_k`，并在每行同时计算 TPC-350 balanced parent。
exact coefficient balance、incidence identity、Gram expansion 与 induced-norm
lower witness 不变，均为 `PROVED_EXACT_FINITE`。

新的 `144` rows、`48` 条 length series 中，reciprocal witness `144/144` 有正响应，
但只在 `118/144` rows 改善 balanced parent。reciprocal/defect ratio 为
`0.0801262572786--0.829632172143`，mean 为 `0.397491684421`；parent ratio 为
`0.099642909832--0.806767399067`，mean 为 `0.361474079935`。reciprocal witness
在 `49/144` rows 达到 half-defect、`47/144` 超过 coordinate baseline，双方均有
`22/48` nondecreasing series，Gram replay 最大误差为 `1.15463194561e-14`。

最强正结果：在完全新 origins 与新 shell ladder 上，固定 reciprocal contrast 仍
产生 `144/144` 正的 finite lower witnesses，并在 `118/144` rows 保留相对 balanced
parent 的 response gain；这确认了部分而非零 transfer。

最强 obstruction：transfer 不是 uniform。`Q=256` 的 reciprocal floor
`0.0801262572786` 低于 balanced parent 的 `0.099642909832`，整体有 26 个 parent
非劣行，且只有 `22/48` series 单调。因此 TPC-351 的 scale repair 不能升级为
uniform shell-scale principle，记为 `REFUTED_SCOPED`。

开放定理：源原生 literal masked aggregate 的 uniform arithmetic `L2` 估计，以及
其与 Route-B reassembly 的 typed attachment；finite reciprocal incidence branch
冻结，不再以新面板重复包装同一 repair claim。

可复用结构：

    predeclared reciprocal rule -> disjoint holdout -> paired parent comparison
      -> scale-specific transfer test -> finite branch freeze

ROUND2_CLUE：`FREEZE_FINITE_RECIPROCAL_BRANCH_AND_RETURN_TO_SOURCE_NATIVE_L2`。

声明上限：`ARITHMETIC_ADVANCE=NO`、`FIXED_POWER_CREDIT=0`、`FULL_GATE_B=OPEN`、
`TWIN_PRIME_RESULT=NONE`；official evaluator files absent，local Bridge-B fail-closed。

    TPC352_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT
    TPC352_RECIPROCAL_RULE = PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE
    TPC352_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
    TPC352_DISJOINT_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
    TPC352_RECIPROCAL_POSITIVE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_144_OF_144
    TPC352_PARENT_IMPROVEMENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_118_OF_144
    TPC352_RECIPROCAL_TO_DEFECT_RANGE = 0.0801262572786--0.829632172143
    TPC352_RECIPROCAL_HALF_DEFECT = NUMERICALLY_CERTIFIED_FINITE_49_OF_144
    TPC352_RECIPROCAL_COORDINATE_BASELINE = NUMERICALLY_CERTIFIED_FINITE_47_OF_144
    TPC352_NONDECREASING_SERIES = NUMERICALLY_CERTIFIED_FINITE_22_OF_48
    TPC352_UNIFORM_REPAIR_TRANSFER = REFUTED_SCOPED
    TPC352_HIGH_SHELL_REPAIR = REFUTED_SCOPED
    TPC352_ARITHMETIC_ADVANCE = NO
    TPC352_FIXED_POWER_CREDIT = 0
    TPC352_FULL_GATE_B = OPEN
    TPC352_TWIN_PRIME_RESULT = NONE
    TPC352_STATUS = PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT
    TPC352_ROUND2_CLUE = FREEZE_FINITE_RECIPROCAL_BRANCH_AND_RETURN_TO_SOURCE_NATIVE_L2

## 0.145 previous：TPC-351 reciprocal-shell zero-sum contrast

项目：papers/tpc-351-reciprocal-shell-contrast/

类型：**PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT**。

TPC-351 承接 TPC-350 的 high-shell scale obstruction，并只测试一个预声明、
不按 row 拟合的替代：对升序 shell primes `Q<p_j<=2Q` 令
`gamma_j=1/p_j-r^(-1)sum_k 1/p_k`，再定义
`c_I(t)=sum_j gamma_j 1_(p_j|t)`。系数是 exact rationals 且
`sum_j gamma_j=0`；线性与双线性精确给出

```text
||D_I c_I||_2^2
 = sum_(j,k) gamma_j gamma_k <D_I h_(p_j,I),D_I h_(p_k,I)>,
||D_I||_(2->2) >= ||D_I c_I||_2 / ||c_I||_2.
```

冻结 protocol 与 TPC-350 完全相同，共 `192` rows、`48` 条 length series。
所有 reciprocal witnesses 非零且响应为正；reciprocal/defect ratio 为
`0.0917557319271--0.901734353382`，mean 为 `0.539037202287`，support 为
`24--339`。`180/192` rows 改善 parent，`86/192` 超过 coordinate baseline，
`111/192` 达到 half-defect；incidence-Gram replay 最大误差为
`1.42108547152e-14`。按 shell 分层，`Q=256` 的 half-defect census 从 parent 的
0 提升到 4，floor 从 `0.0657381187306` 提升到 `0.0917557319271`。

最强正结果：一个固定、scale-aware、exact zero-sum 的 reciprocal coefficient rule
在相同 panel 的 `180/192` rows 改善 TPC-350，并将总体 half-defect census 从 91
提升到 111；这是明确的 finite scale repair，而不是 response-fitted artifact。

最强 obstruction：改善并非 universal；12 rows 退化，`Q=256` 仍有 44/48 rows
低于 half-defect，总体 floor 仍低于 `1/4`，且只有 `25/48` length series
nondecreasing。因此 universal quarter-floor 与 monotone-growth 叙述仍为
`REFUTED_SCOPED`，并未获得 arithmetic credit。

开放定理：在完全 disjoint origins 与新的 length/shell ladder 上 adversarially
hold out 同一 reciprocal rule；若 transfer 失败则冻结 finite incidence branch，若
transfer 成立也仍需 source-native masked arithmetic `L2` 才能进入 Route-B reassembly。

可复用结构：

    shell reciprocal profile -> exact rational centering -> incidence Gram
      -> paired parent comparison -> scale-resolved repair/obstruction ledger

ROUND2_CLUE：`ADVERSARIAL_HOLDOUT_FOR_RECIPROCAL_CONTRAST_BEFORE_BRANCH_FREEZE`。

声明上限：`ARITHMETIC_ADVANCE=NO`、`FIXED_POWER_CREDIT=0`、`FULL_GATE_B=OPEN`、
`TWIN_PRIME_RESULT=NONE`；official evaluator files absent，local Bridge-B fail-closed。

    TPC351_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT
    TPC351_RECIPROCAL_ZERO_SUM_RULE = PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE
    TPC351_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
    TPC351_SCALE_REPAIR_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
    TPC351_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
    TPC351_PARENT_IMPROVEMENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_180_OF_192
    TPC351_RECIPROCAL_TO_DEFECT_RANGE = 0.0917557319271--0.901734353382
    TPC351_COORDINATE_BASELINE_BEATEN = NUMERICALLY_CERTIFIED_FINITE_86_OF_192
    TPC351_HALF_DEFECT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_111_OF_192
    TPC351_NONDECREASING_GROWTH_SERIES = NUMERICALLY_CERTIFIED_FINITE_25_OF_48
    TPC351_UNIFORM_QUARTER_FLOOR = REFUTED_SCOPED
    TPC351_ARITHMETIC_ADVANCE = NO
    TPC351_FIXED_POWER_CREDIT = 0
    TPC351_FULL_GATE_B = OPEN
    TPC351_TWIN_PRIME_RESULT = NONE
    TPC351_STATUS = PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT
    TPC351_ROUND2_CLUE = ADVERSARIAL_HOLDOUT_FOR_RECIPROCAL_CONTRAST_BEFORE_BRANCH_FREEZE

## 0.144 previous：TPC-350 fresh-growth and shell-scale signed incidence audit

项目：papers/tpc-350-fresh-growth-signed-incidence/

类型：**PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT**。

TPC-350 直接承接 TPC-349 的 zero-sum prime-incidence Gram interface，但不复用其
origin/length/scale panel。冻结三个 fresh origins `60097,72097,84097`，四个长度
`256,512,1024,2048`，四级 shell ladder `Q=36,80,128,256`，两种 source law
`all_plus, alternating_index` 与两种 kernel exponent，共 `192` rows、`48` 条
固定 `(origin,Q,exponent,law)` length series。所有 rows 的 signed incidence
witness 均非零且响应为正；signed/defect ratio 为
`0.0657381187306--0.8797933448`，mean 为 `0.492863038063`，support 为
`24--294`，`70/192` rows 超过 coordinate baseline，`91/192` rows 达到
half-defect，incidence-Gram replay 最大误差为 `1.06581410364e-14`。

最强正结果：TPC-349 的 exact lower-witness interface 在三个全新位置、四个有限
长度和两种 shell law 上保持 `192/192` 正响应；这是 fresh finite replication，
不是 growing theorem。

最强 obstruction：按 Q 分层，`Q=256` 的 48 rows 的 ratio 范围为
`0.0657381187306--0.456967381039`，没有一行达到 half-defect；长度序列只有
`24/48` nondecreasing。因此 universal quarter-floor 与 universal monotone-growth
叙述在该声明面板上均只能记为 `REFUTED_SCOPED`。

开放定理：寻找不对每一行拟合的 scale-adaptive zero-sum contrast，或冻结 incidence
branch 并回到保留 literal masks 的 source-native arithmetic `L2`。两者都尚未给出
fixed-power credit、Route-B reassembly 或 twin-prime endpoint。

可复用结构：

    fresh origins + length ladder + shell ladder
      -> balanced incidence Gram -> series ledger -> scale obstruction

ROUND2_CLUE：`TEST_SCALE_ADAPTIVE_ZERO_SUM_CONTRAST_ON_HIGH_SHELLS`。

声明上限：`ARITHMETIC_ADVANCE=NO`、`FIXED_POWER_CREDIT=0`、`FULL_GATE_B=OPEN`、
`TWIN_PRIME_RESULT=NONE`；official evaluator files absent，local Bridge-B fail-closed。

    TPC350_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT
    TPC350_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
    TPC350_FRESH_GROWTH_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
    TPC350_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
    TPC350_SIGNED_TO_DEFECT_FLOOR = NUMERICALLY_CERTIFIED_FINITE_0.0657381187306
    TPC350_COORDINATE_BASELINE_BEATEN = NUMERICALLY_CERTIFIED_FINITE_70_OF_192
    TPC350_HALF_DEFECT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_91_OF_192
    TPC350_NONDECREASING_GROWTH_SERIES = NUMERICALLY_CERTIFIED_FINITE_24_OF_48
    TPC350_UNIFORM_QUARTER_FLOOR = REFUTED_SCOPED
    TPC350_ARITHMETIC_ADVANCE = NO
    TPC350_FIXED_POWER_CREDIT = 0
    TPC350_FULL_GATE_B = OPEN
    TPC350_TWIN_PRIME_RESULT = NONE
    TPC350_STATUS = PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT
    TPC350_ROUND2_CLUE = TEST_SCALE_ADAPTIVE_ZERO_SUM_CONTRAST_ON_HIGH_SHELLS

## 0.143 previous：TPC-349 prime-balanced signed defect witness

项目：papers/tpc-349-prime-balanced-signed-defect-witness/

类型：**PROVED_EXACT_FINITE_PRIME_BALANCED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_AUDIT**。

TPC-349 承接 TPC-348 的 coordinate lower-witness interface。对升序 shell
`p_0<...<p_(r-1)`，前后各 `floor(r/2)` 个 primes 取 `+1/-1`，奇数 shell 的
中间 prime 取 `0`，从而 `sum_j beta_j=0`。定义 interval incidence vectors
`h_(p_j,I)(t)=1_(p_j|t)` 与 `b_I=sum_j beta_j h_(p_j,I)`。线性与双线性精确给出

```text
||D_I b_I||_2^2
 = sum_(j,k) beta_j beta_k <D_I h_(p_j,I),D_I h_(p_k,I)>,
||D_I||_(2->2) >= ||D_I b_I||_2 / ||b_I||_2.
```

冻结 protocol 与 TPC-348 相同，共 `192` rows。所有 rows 的 signed incidence
vector 非零且响应为正；signed/defect ratio 为
`0.39083565842--0.954375010719`，signed/ideal ratio 为
`0.0125941959067--0.430061305156`，signed/coordinate ratio 为
`0.542800508699--2.04702542827`。`136/192` rows 超过最佳 mask-hit coordinate
baseline，`175/192` rows 达到 defect norm 的一半；signed support 为 `28--150`。
producer、reverse-shell independent replay、six-mutation stress 与 exact `[1,14]`
multi-hit anchor 均通过。

最强正结果：零和 prime-incidence contrast 获得 exact cross-prime Gram interface 与
deterministic lower witness；它在多数声明 rows 上比单坐标 witness 更强。

最强 obstruction：signed/coordinate ratio 的有限下界只有 `0.542800508699`，56
rows 未超过 coordinate baseline，所以 universal balanced gain 即使在当前 panel
也被 scoped refute；这不否定其他预声明 sign rules 或 growing theorem。

开放定理：在 fresh/growing panels 上重放并控制 signed incidence Gram，区分
same-prime energy 与 cross-prime interference，同时保留 literal masks；若无稳定性，
则应冻结该 finite sign rule 并回到 source-native arithmetic `L2`。

可复用结构：

    ordered shell -> zero-sum beta -> incidence contrast -> prime Gram
                  -> normalized lower witness -> finite baseline audit

ROUND2_CLUE：`REPLICATE_SIGNED_INCIDENCE_GRAM_ON_GROWING_FRESH_PANELS`。

声明上限：`ARITHMETIC_ADVANCE=NO`、`FIXED_POWER_CREDIT=0`、`FULL_GATE_B=OPEN`、
`TWIN_PRIME_RESULT=NONE`；official evaluator files absent，local Bridge-B fail-closed。

    TPC349_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_PRIME_BALANCED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_AUDIT
    TPC349_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
    TPC349_PRIME_BALANCE_RULE = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC349_INCIDENCE_GRAM_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC349_FINITE_SIGNED_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
    TPC349_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
    TPC349_COORDINATE_BASELINE_BEATEN = NUMERICALLY_CERTIFIED_FINITE_136_OF_192
    TPC349_HALF_DEFECT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_175_OF_192
    TPC349_UNIVERSAL_BALANCED_GAIN = REFUTED_SCOPED
    TPC349_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
    TPC349_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
    TPC349_ARITHMETIC_ADVANCE = NO
    TPC349_FIXED_POWER_CREDIT = 0
    TPC349_FULL_GATE_B = OPEN
    TPC349_TWIN_PRIME_RESULT = NONE
    TPC349_STATUS = PROVED_EXACT_FINITE_PRIME_BALANCED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_AUDIT
    TPC349_ROUND2_CLUE = REPLICATE_SIGNED_INCIDENCE_GRAM_ON_GROWING_FRESH_PANELS

## 0.142 previous：TPC-348 position-aware mask-defect lower witness

项目：papers/tpc-348-position-aware-mask-defect-lower-witness/

类型：**PROVED_EXACT_FINITE_COORDINATE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_POSITION_AUDIT**。

TPC-348 承接 TPC-347 的 literal masked prime-shell object。令 `D_I=A_I-T_I` 为
physical block 与 unmasked convolution compression 的 defect，并定义
`J_I={t in I: exists active shell prime p with p|t}`。对每个单位坐标列精确得到
左右 projection defect 的 position formula；于是有限维 induced Euclidean norm 满足
`||D_I||_(2->2)>=max_(t in J_I)||D_I e_t||_2`。这是 coordinate lower-witness
theorem，不需要 positivity、symmetry、leading eigenvector 或 sign heuristic。

冻结 protocol 为 origins `[40097,48097]`、source counts `[256,512,1024]`、
`Q=[24,36,54,80]`、exponents `[1,2]`、四个 sign laws 与 `H=66`，共 `192` 条
finite rows。producer、reverse-shell independent checker 与 mutation stress 共同
重建每一行；`192/192` rows 有正 best-hit witness，mask-hit count 为 `30--169`，
best-hit/defect ratio 为 `0.453958762219--0.897148966365`，best-hit/ideal ratio
为 `0.0183057714619--0.336311065586`，position formula 最大 replay discrepancy
为 `2.0872192863e-14`。另有 exact rational six-point anchor：`I=[1,6]`、shell
`{5,7}`、唯一 hit position `5`。

最强正结果：把 TPC-347 的 mask defect 从整体 spectral observation 变成一个可复用的
position-aware finite lower-witness interface，并在全部声明行上完成独立可审计的正
witness census。

最强 obstruction：mask-hit columns 在声明面板上不能被当作零 defect；但这是 finite
scoped obstruction，不能外推为 growing lower bound，也不能替代 source-native
arithmetic `L2` cancellation。

开放定理：在保留所有 residue masks 的情况下，证明 source-uniform position-aware
defect bound，或构造 prime-balanced signed witnesses 后获得可支付的 arithmetic `L2`
estimate；Route-B reassembly、fixed-power payment 与 twin-prime endpoint 仍 open。

可复用结构：

    literal masked block -> two-sided projection defect -> mask-hit set
                       -> coordinate lower witness -> finite audit -> firewall

ROUND2_CLUE：`TEST_PRIME_BALANCED_DEFECT_WITNESSES_BEFORE_SOURCE_NATIVE_L2`。

声明上限：`ARITHMETIC_ADVANCE=NO`、`FIXED_POWER_CREDIT=0`、`FULL_GATE_B=OPEN`、
`TWIN_PRIME_RESULT=NONE`；Session-named official evaluator files absent，故 local
Bridge-B 仍 fail-closed。

    TPC348_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_COORDINATE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_POSITION_AUDIT
    TPC348_COORDINATE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
    TPC348_MASK_HIT_SELECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC348_POSITION_FORMULA = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC348_FINITE_POSITION_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
    TPC348_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
    TPC348_MASK_DISCARDABILITY = REFUTED_SCOPED
    TPC348_BEST_HIT_TO_DEFECT_RATIO = 0.453958762219--0.897148966365
    TPC348_BEST_HIT_TO_IDEAL_RATIO = 0.0183057714619--0.336311065586
    TPC348_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
    TPC348_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
    TPC348_ARITHMETIC_ADVANCE = NO
    TPC348_FIXED_POWER_CREDIT = 0
    TPC348_FULL_GATE_B = OPEN
    TPC348_TWIN_PRIME_RESULT = NONE
    TPC348_STATUS = PROVED_EXACT_FINITE_COORDINATE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_POSITION_AUDIT
    TPC348_ROUND2_CLUE = TEST_PRIME_BALANCED_DEFECT_WITNESSES_BEFORE_SOURCE_NATIVE_L2

## 0.141 previous：TPC-347 convolution interface and mask defect

项目：papers/tpc-347-convolution-mask-defect-interface/

类型：**PROVED_EXACT_FINITE_CONVOLUTION_MASK_DEFECT_INTERFACE_PLUS_NUMERICALLY_CERTIFIED_FINITE_SPECTRAL_AUDIT**。

TPC-347 承接 TPC-346 的 arithmetic-L2 回归方向，在 literal prime-shell family
中保留 endpoint divisibility masks。对 `k_p(d)` 及 signed coherent sum `K_e`，
物理 block 精确写成
`A_I=sum_p e_p R_I P_p K_p P_p E_I=T_I+D_I`，其中
`T_I=R_I K_e E_I` 是 unmasked convolution 的 interval compression，`D_I` 是
显式 projection defect。绝对可和条件下，Fourier multiplier norm
`||K_e||=ess sup |khat_e|`、compression inequality 与 Young tail majorant 都
给出 exact interface；它们没有把 physical masked operator 偷换成 ideal operator。

预声明 protocol 为 origins `[40097,48097]`、source counts `[256,512,1024]`、
`Q=[24,36,54,80]`、exponents `[1,2]`、四个 sign laws、`H=66`。共 `192` 条
finite spectral rows、`96/96` ideal translation checks 与 `192/192` combined
envelope checks，另有 exact rational six-point anchor。mask defect/ideal spectral
ratio 范围为 `0.0312337689685--0.467075645603`，`93/192` 条超过 `1/4`。

最强正结果：literal masked object 获得了可复用的 convolution-plus-defect
factorisation；ideal comparison 在全部 `96` 个 two-origin groups 上保持 exact
translation pattern，且生产者、reverse-order independent replay、mutation stress
与正常/优化 Bridge-B 均通过。

最强 obstruction：在声明面板上，mask defect 不是可统一丢弃的 finite remainder；
但该比例是有限数值审计，不是 growing lower bound，也不否定未来的 position-aware
cancellation。

开放定理：在保留 residue masks 的前提下，对 `D_I` 给出 source-uniform、
position-aware operator bound，或直接证明 masked coherent sum 的 arithmetic `L2`
cancellation；随后仍需完成 Route-B reassembly 与 endpoint payment。

可复用结构：

    literal block -> P_p K_p P_p -> unmasked convolution -> Fourier interface
                  -> exact defect -> finite spectral audit -> claim firewall

ROUND2_CLUE：`QUANTIFY_MASK_DEFECT_LOWER_WITNESSES_BEFORE_SOURCE_NATIVE_L2`。

    TPC347_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_CONVOLUTION_MASK_DEFECT_INTERFACE_PLUS_NUMERICALLY_CERTIFIED_FINITE_SPECTRAL_AUDIT
    TPC347_MASK_FACTORISATION = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC347_UNMASKED_FOURIER_INTERFACE = PROVED_EXACT_CONDITIONAL
    TPC347_COMPRESSION_INEQUALITY = PROVED_EXACT
    TPC347_YOUNG_ENVELOPE = PROVED_EXACT_FOR_UNMASKED_KERNEL
    TPC347_TRANSLATION_INVARIANCE = NUMERICALLY_CERTIFIED_FINITE_96_OF_96
    TPC347_MASK_DEFECT_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
    TPC347_DEFECT_DISCARDABILITY = REFUTED_SCOPED
    TPC347_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
    TPC347_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
    TPC347_ARITHMETIC_ADVANCE = NO
    TPC347_FIXED_POWER_CREDIT = 0
    TPC347_FULL_GATE_B = OPEN
    TPC347_TWIN_PRIME_RESULT = NONE
    TPC347_STATUS = PROVED_EXACT_FINITE_CONVOLUTION_MASK_DEFECT_INTERFACE_PLUS_NUMERICALLY_CERTIFIED_FINITE_SPECTRAL_AUDIT
    TPC347_ROUND2_CLUE = QUANTIFY_MASK_DEFECT_LOWER_WITNESSES_BEFORE_SOURCE_NATIVE_L2

## 0.140 previous：TPC-346 third-panel hostile replication

项目：papers/tpc-346-third-panel-hostile-replication/

类型：**NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION**。

TPC-346 承接 TPC-345 的 basis-invariant finite geometry，加入预声明、disjoint、
cutoff-safe 的第三 panel `[44097,44609,45217]`，并保持 TPC-340 的 all-plus
`Q=54`、kernel exponent `1`、`H=66`、scale `1024`、9 controls、4 source
categories 与两个 row weightings。三 panel 共 9 rows、324 raw records，261 条
nonempty。fresh panel own-fit retention 为 `0.3159173453264`（raw）与
`0.3294074740697`（equal-row）；shared three-panel retention 为
`0.3419067441273` 与 `0.356412350685`。

panel-adaptive block model 的 raw retention 为 `0.2999630725662`，但 equal-row
为 `0.3222362713305`，所以 raw crossing 不是 weighting-stable law。6 个 directed
panel predictions、3 个 leave-one-panel-out predictions 与 9 个 fresh control-LOO
projections 在两种 weighting 下均超过 `0.30`。shared-to-adaptive nesting、
projection/Pythagorean identities 与有限模型的 exact algebra 已在 proof package
中写明；这不赋予额外 arithmetic meaning。

最强正结果：一个完全独立 fresh third panel 的全量 hostile protocol、nested finite
identity、raw narrow crossing 与 reverse-shell replay 均可复现。

最强 obstruction：fresh own-fit、equal-row adaptive fit、第三面板 transfer、
leave-one-panel-out 与 fresh control-LOO 全部拒绝稳定低残差解释；因此只对声明的
panel-adaptive branch 做 finite scoped freeze，不外推 universal no-go。

开放定理：source-uniform arithmetic `L2`、uniform masked operator bound、strict
`1/400` payment、fixed-power saving 与 full Route-B Gate B。fixed-power credit 为
`0`，twin-prime conclusion 为 `NONE`；官方 evaluator 文件缺失，仅有 local
fail-closed Bridge-B。

可复用结构：

    parent panels -> fresh disjoint panel -> shared/adaptive nesting
                    -> weighting audit -> transfer and control-LOO freeze

ROUND2_CLUE：`FREEZE_PANEL_ADAPTIVE_ROUTE_AND_RETURN_TO_ARITHMETIC_L2`。

    TPC346_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION
    TPC346_NESTED_MODEL_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC346_FRESH_PANEL_OWN_FIT = REFUTED_SCOPED
    TPC346_PANEL_ADAPTIVE_RAW = NUMERICALLY_CERTIFIED_FINITE_SCOPED_PASS
    TPC346_PANEL_ADAPTIVE_EQUAL_ROW = REFUTED_SCOPED
    TPC346_PANEL_ADAPTIVE_WEIGHTING_STABILITY = REFUTED_SCOPED
    TPC346_THIRD_PANEL_TRANSFER = REFUTED_SCOPED
    TPC346_ARITHMETIC_ADVANCE = NO
    TPC346_FIXED_POWER_CREDIT = 0
    TPC346_SOURCE_UNIFORM_L2 = OPEN
    TPC346_FULL_GATE_B = OPEN
    TPC346_TWIN_PRIME_RESULT = NONE
    TPC346_STATUS = NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION
    TPC346_ROUND2_CLUE = FREEZE_PANEL_ADAPTIVE_ROUTE_AND_RETURN_TO_ARITHMETIC_L2

## 0.139 current：TPC-345 principal-angle / Grassmann stability audit

项目：papers/tpc-345-principal-angle-grassmann-audit/

类型：**NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT**。

TPC-345 承接 TPC-344 的 weighting-sensitive panel-contrast partial repair，不再比较
base/contrast 坐标系，而是比较 TPC-341 与 TPC-342 两个 hash-locked nuisance
column spaces。每个 panel 的三条 length-512 rows 依协议堆叠；raw weighting
直接堆叠，equal-row weighting 以各 row twin-target 的 `L2` norm 同时归一化
target 与 nuisance columns。positive-SVD rank rule 给出 TPC-341 rank 3、TPC-342
rank 2。

raw principal cosines 为 `0.99570180102754502, 0.079945679326165323`，对应
angles `5.3141837612792102°`, `85.414556610305894°`；equal-row cosines 为
`0.91445198603192213, 0.078708449294248611`，angles 为
`23.871978700026663°`, `85.485668773878913°`。第一主角移动
`18.557794938747453°`，所以 dominant alignment 不具 weighting stability。

双向 target-transfer retentions 在 raw 下为 `0.2306119635213958` 与
`0.35887708996182843`，equal-row 下为 `0.27459500882916554` 与
`0.32345205001638844`；要求两方向同时 `<0.30` 的 criterion 在两种 weighting
下均失败。18 个 leave-one-control-out angle pairs 保留 raw dominant cosine
minimum `0.99470019507217156`，raw/equal transverse maxima 分别为
`0.15497512764427687` 与 `0.16757600960516528`。固定 nonsingular shear 下
projector 与 principal-cosine errors 均低于 `8e-15`。

最强正结果：一个 dominant alignment 与一个 persistent near-orthogonal transverse
direction 在 basis change 与所有 18 个 control omissions 下可独立重放。

最强 obstruction：dominant angle 对 row weighting 发生 `18.56°` 位移，且双向
target transfer 在 raw/equal 两种预声明 weighting 下均不能同时通过。

开放定理：canonical weighting-stable nuisance structure、source-uniform arithmetic
`L2`、uniform masked operator bound、strict `1/400` payment 与 full Route-B Gate B。
fixed-power credit 为 `0`，twin-prime conclusion 为 `NONE`；官方 evaluator 文件缺失，
仅有 local fail-closed Bridge-B。

可复用结构：

    panel-adaptive spans -> positive-SVD bases -> principal angles/projectors
                         -> weighting audit -> mutual transfer obstruction

ROUND2_CLUE：`FINITE_NO_GO_OR_FREEZE_PANEL_ADAPTIVE_ROUTE`。

    TPC345_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT
    TPC345_PRINCIPAL_ANGLE_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC345_BASIS_INVARIANCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC345_RAW_DOMINANT_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC345_TRANSVERSE_ALIGNMENT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC345_WEIGHTING_STABILITY = REFUTED_SCOPED
    TPC345_MUTUAL_TRANSFER = REFUTED_SCOPED
    TPC345_RANK_MISMATCH = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC345_ARITHMETIC_ADVANCE = NO
    TPC345_FIXED_POWER_CREDIT = 0
    TPC345_SOURCE_UNIFORM_L2 = OPEN
    TPC345_FULL_GATE_B = OPEN
    TPC345_TWIN_PRIME_RESULT = NONE
    TPC345_STATUS = NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT
    TPC345_ROUND2_CLUE = FINITE_NO_GO_OR_FREEZE_PANEL_ADAPTIVE_ROUTE

## 0.138 released：TPC-344 panel-contrast nuisance basis audit

项目：papers/tpc-344-panel-contrast-nuisance-basis/

类型：**NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT**。

TPC-344 承接 TPC-343 的 scoped shared-coefficient obstruction，测试最小的
panel-adaptive 结构：对三个 nuisance categories 分别加入一个预声明的
panel-contrast column。六列 basis 在 exact finite linear algebra 上满足
`u_1j=(b_j+d_j)/2`、`u_2j=(b_j-d_j)/2`，等价于每个 panel 内共享、panel
之间允许不同的 nuisance coefficient vector；这不是 canonical arithmetic basis。

六 rows 产生 216 个 raw records、171 个 nonempty records、6 个 in-sample
projections、18 个 contrast holdouts 与 4 个 directional cross-fits。panel-contrast
raw residual retention 为 `0.29621892474890171`，首次在该 declared raw weighting
下通过 inherited `<0.30` guard；equal-row retention 为 `0.31865066996095742`，
因此该 crossing 对 weighting 不稳定。contrast positive rank 为 5（TPC-342 的
prime-power nuisance column 在其三 rows 上为空），raw positive-condition diagnostic
为 `141.98499924473342`。

最强正结果：panel-contrast span 对 raw pooled finite fit 提供了一个可重放的、
但很窄的 partial repair，并与 panel-adaptive shared span exact 等价。

最强 obstruction：equal-row weighting 删除 raw crossing；四个 cross-fit prediction
retentions 为 `0.37594867338366317--0.63429341965475916`，全部高于低残差
`<0.30` transfer criterion。18 个 contrast holdouts 为
`0.6372238668391691--0.91285435474891141`。

开放定理：canonical/source-uniform nuisance structure、arithmetic `L2`、uniform
masked operator bound、strict `1/400` payment 与 full Route-B Gate B。fixed-power
credit 为 `0`，twin-prime conclusion 为 `NONE`；官方 evaluator 文件缺失，仅有
local fail-closed Bridge-B。

可复用结构：

    shared span -> signed panel contrast -> panel-adaptive reparameterization
                -> weighting sensitivity -> cross-fit transfer audit

ROUND2_CLUE：`PRINCIPAL_ANGLE_GRASSMANN_STABILITY_AUDIT`。

    TPC344_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT
    TPC344_CONTRAST_SPAN_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC344_RAW_CONTRAST_GUARD = NUMERICALLY_CERTIFIED_FINITE_SCOPED_PASS
    TPC344_EQUAL_ROW_CONTRAST_GUARD = REFUTED_SCOPED
    TPC344_WEIGHTING_STABILITY = REFUTED_SCOPED
    TPC344_CROSSFIT_TRANSFER = REFUTED_SCOPED
    TPC344_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_18_RECORDS
    TPC344_ARITHMETIC_ADVANCE = NO
    TPC344_FIXED_POWER_CREDIT = 0
    TPC344_SOURCE_UNIFORM_L2 = OPEN
    TPC344_FULL_GATE_B = OPEN
    TPC344_TWIN_PRIME_RESULT = NONE
    TPC344_STATUS = NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT
    TPC344_ROUND2_CLUE = PRINCIPAL_ANGLE_GRASSMANN_STABILITY_AUDIT

## 0.137 released：TPC-343 cross-panel shared-nuisance meta-certificate

项目：papers/tpc-343-cross-panel-meta-certificate/

类型：**NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE**。

TPC-343 承接 TPC-342 的真实结论：TPC-341 的 aggregate-versus-holdout split 已在
独立 panel 上复现，但这还没有说明 nuisance projection 存在一个跨 panel 的共同
系数律。本项目锁定 TPC-341 与 TPC-342 的两个三窗口 panels，共六个
cutoff-safe rows，并比较两个明确的 finite stacking models：row-block model 允许
每个 row 使用独立 nuisance coefficients；shared model 强制六个 rows 共用一个
三维 nuisance coefficient vector。

六 rows 产生 216 个 raw records、171 个 nonempty records、6 个 in-sample projections
与 54 个 leave-one-control-out records。row-block raw-energy pooled residual retention
为 `0.23254291005354055`，equal-row 版本为 `0.25028569537510303`，均通过继承的
`<0.30` guard。shared raw-energy retention 为 `0.31980131035540693`，equal-row
retention 为 `0.35493358014194187`，两者均超过同一 guard；九个 shared cross-panel
holdout stacks 的 raw retention 为 `0.64083061957187526--0.90909482975034406`。

最强正结果：row-block projection 的 stacked Pythagorean identity 与 energy additivity
是 exact finite；两个独立 panels 的 row-local fit 在 pooled certificate 中仍然可重放。

最强 obstruction：single shared nuisance coefficient law 在 raw 与 equal-row 两种
预声明权重下都失败。这是对该 finite basis/model 的 scoped refutation，不是对所有
nuisance bases 的否定。

开放定理：canonical nuisance basis、source-uniform arithmetic `L2`、uniform masked
operator bound、strict `1/400` payment 与 full Route-B Gate B。fixed-power credit 为
`0`，twin-prime conclusion 为 `NONE`。

可复用结构：

    independent panels -> row-block direct sum -> shared-column stack
                       -> weighting sensitivity -> scoped coefficient-stability test

ROUND2_CLUE：`ALTERNATIVE_NUISANCE_BASIS_OR_PRINCIPAL_ANGLE_AUDIT`。

    TPC343_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE
    TPC343_STACKED_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC343_ROW_BLOCK_META = NUMERICALLY_CERTIFIED_FINITE_6_ROW_POOLED_PROJECTION
    TPC343_SHARED_COEFFICIENT_RAW = NUMERICAL_OBSERVATION_0.319_TO_0.320
    TPC343_SHARED_COEFFICIENT_EQUAL_ROW = NUMERICAL_OBSERVATION_0.354_TO_0.355
    TPC343_SHARED_COEFFICIENT_STABILITY = REFUTED_SCOPED
    TPC343_HOLDOUT_META = NUMERICALLY_CERTIFIED_FINITE_54_RECORDS
    TPC343_ARITHMETIC_ADVANCE = NO
    TPC343_FIXED_POWER_CREDIT = 0
    TPC343_SOURCE_UNIFORM_L2 = OPEN
    TPC343_FULL_GATE_B = OPEN
    TPC343_TWIN_PRIME_RESULT = NONE
    TPC343_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE
    TPC343_ROUND2_CLUE = ALTERNATIVE_NUISANCE_BASIS_OR_PRINCIPAL_ANGLE_AUDIT

## 0.136 released：TPC-342 independent fresh-panel reproduction

项目：papers/tpc-342-independent-fresh-holdout-reproduction/

类型：**NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION**。

TPC-342 锁定 TPC-341 producer/certificate 所定义的九-control nuisance-projection
protocol，并把 source panel 独立迁移到三个互不重叠、cutoff-safe 的 windows
`[40097,40608]`、`[40609,41120]`、`[41121,41632]`。同一 all-plus `Q=54`、
exponent `1`、`H=66` operator、四类 masks、SVD rank rule 与预声明 guards 均保持
不变；因此本项目是 protocol reproduction，而不是向 TPC-341 certificate 追加样本。

三个 rows 共形成 108 个 raw records、81 个 nonempty records、3 个 in-sample fits 与
27 个 leave-one-control-out fits。样本内 residual retention 为
`0.27014105207549899--0.29510061195372306`，27 个 held-out retention 为
`0.58948424759670548--0.94291652960635697`。prime-power mask 在这三个窗口均为空，
故 nuisance rank 统一为 2；该有限退化被显式记录，rank/Pythagorean failures 为 0。

最强正结果：TPC-341 的 aggregate-versus-holdout split 在完全 disjoint source panel
上独立复现，producer 与 reverse-shell checker 在 parent/protocol hash locks 下给出
一致的 finite readout。

最强 obstruction：27/27 held-out tests 仍高于预声明的 `0.40` residual guard；因此
mean-only nuisance removal 在该独立面板上依然不能升级为 control-invariant twin
component。

开放定理：source-uniform arithmetic `L2`、uniform masked operator bound、canonical
nuisance decomposition、strict `1/400` payment 与 full Route-B Gate B。fixed-power
credit 为 0，twin-prime conclusion 为 NONE。

可复用结构：

    protocol hash lock -> disjoint cutoff-safe source panel -> reverse-shell replay
                       -> in-sample/held-out separation -> scoped non-transfer certificate

ROUND2_CLUE：`CROSS_PANEL_META_CERTIFICATE_OR_ALTERNATIVE_NUISANCE_BASIS`。

    TPC342_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION
    TPC342_PROJECTION_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC342_INDEPENDENT_FRESH_REPLAY = NUMERICALLY_CERTIFIED_FINITE_108_RAW_RECORDS
    TPC342_IN_SAMPLE_PROJECTION = NUMERICALLY_CERTIFIED_FINITE_3_ROWS
    TPC342_HOLDOUT_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_27_RECORDS
    TPC342_IN_SAMPLE_RETENTION = NUMERICAL_OBSERVATION_0.270_TO_0.296
    TPC342_HOLDOUT_RETENTION = NUMERICAL_OBSERVATION_0.589_TO_0.943
    TPC342_CONTROL_STABILITY = REFUTED_SCOPED
    TPC342_ARITHMETIC_ADVANCE = NO
    TPC342_FIXED_POWER_CREDIT = 0
    TPC342_SOURCE_UNIFORM_L2 = OPEN
    TPC342_FULL_GATE_B = OPEN
    TPC342_TWIN_PRIME_RESULT = NONE
    TPC342_STATUS = NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION
    TPC342_ROUND2_CLUE = CROSS_PANEL_META_CERTIFICATE_OR_ALTERNATIVE_NUISANCE_BASIS

## 0.135 released：TPC-341 fresh holdout nuisance orthogonalization

项目：papers/tpc-341-fresh-holdout-nuisance-orthogonalization/

类型：**NUMERICALLY_CERTIFIED_FINITE_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION**。

TPC-341 承接 TPC-340 的真实 obstruction：通用 sign-free hybrid envelope 仍无法解释
广掩码 alignment。它不再增加 generic norm，而是在三个与当前 parent panel 不重叠的
cutoff-safe windows
`[48097,48608]`、`[48609,49120]`、`[49217,49728]` 上，固定同一
all-plus `Q=54`、exponent `1`、`H=66` operator 与九个 controls，测试 nuisance
orthogonalization 是否跨 control 稳定。

九-control twin mean 投影到 non-twin、prime-power、zero-support 三个 nuisance mean
的 residual retention 为 `0.20108940861155286--0.2560626550992825`，即有限面板上
去掉 `0.7439373449007175--0.79891059138844711` 的 mean energy；但 leave-one-control-
out projection 用其余八个 controls 训练、对被省略 twin output 测试，27/27 个 residual
retentions 都位于 `0.4435267486381384--0.89044735643479045`。effective nuisance rank
为 `2,2,3`，rank 与 Pythagorean checks 全部通过。

最强正结果：fresh panel 将 aggregate mean fit 与 held-out control test 分离为两个
可重放的几何对象；正交分解 identity 是 exact finite。

最强 obstruction：mean-only nuisance removal 在样本内看起来很强，但在所有 27 个
held-out control tests 都没有通过预声明的 `<0.40` residual-transfer criterion；因此
它不能被升级为 control-invariant twin-prime component。

开放定理：source-uniform arithmetic `L2`、uniform masked operator bound、canonical
nuisance decomposition、strict `1/400` payment 与 Route-B Gate B。fixed-power credit
为 `0`，twin-prime conclusion 为 `NONE`。官方 Route-A/Route-B evaluator files 仍缺失，
本关只使用 local fail-closed Bridge-B。

可复用结构：

    locked source -> fresh disjoint windows -> class/control response means
                  -> nuisance span projection -> leave-one-control-out obstruction

ROUND2_CLUE：`INDEPENDENT_REPRODUCTION_OR_FREEZE_NUISANCE_PROJECTION`。

    TPC341_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION
    TPC341_PROJECTION_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC341_FRESH_HOLDOUT_REPLAY = NUMERICALLY_CERTIFIED_FINITE_108_RAW_RECORDS
    TPC341_IN_SAMPLE_PROJECTION = NUMERICALLY_CERTIFIED_FINITE_3_ROWS
    TPC341_HOLDOUT_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_27_RECORDS
    TPC341_IN_SAMPLE_RETENTION = NUMERICAL_OBSERVATION_0.201_TO_0.256
    TPC341_HOLDOUT_RETENTION = NUMERICAL_OBSERVATION_0.444_TO_0.890
    TPC341_CONTROL_STABILITY = REFUTED_SCOPED
    TPC341_ARITHMETIC_ADVANCE = NO
    TPC341_FIXED_POWER_CREDIT = 0
    TPC341_SOURCE_UNIFORM_L2 = OPEN
    TPC341_FULL_GATE_B = OPEN
    TPC341_TWIN_PRIME_RESULT = NONE
    TPC341_STATUS = NUMERICALLY_CERTIFIED_FINITE_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION
    TPC341_ROUND2_CLUE = INDEPENDENT_REPRODUCTION_OR_FREEZE_NUISANCE_PROJECTION

## 0.134 released：TPC-340 Schur/Frobenius hybrid envelope

项目：papers/tpc-340-schur-frobenius-hybrid-envelope/

类型：**NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE**。

TPC-340 将 TPC-339 的 support-restricted Frobenius envelope 与 symmetric operator 的
global Schur envelope 合并为
`||Ax||^2 <= min(F(supp(x))^2,R^2)||x||^2`，其中
`R=max_i sum_j |A(i,j)|`。同一六 windows、四 masks、九 controls 共 216 条记录全部
通过，Schur branch 为 54 条、Frobenius branch 为 162 条；zero-support 的有限
Frobenius gain 改善因子为 `1.2502450344698024--4.6984425635778768`。

最强正结果：得到一个不依赖 covariance sign 的、exact finite 的混合上界，并明确
定位 Schur branch 的有限收益。

最强 obstruction：broad twin/non-twin/zero masks 的 hybrid occupancy 仍低于
`0.18685503656580477`，故 support information 加 global row-sum bound 仍不能形成
sharp uniform response estimate。

开放定理：growing masked operator bound、source-uniform arithmetic `L2`、strict
`1/400` payment 与 Route-B Gate B；arithmetic advance 仍为 `NO`。

可复用结构：`support Frobenius -> global Schur -> branch-audited hybrid envelope`。

ROUND2_CLUE：`TEST_NUISANCE_ORTHOGONALIZATION_OR_ADVERSARIAL_HOLDOUT`。

    TPC340_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE
    TPC340_HYBRID_BOUND = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC340_HYBRID_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_RECORDS
    TPC340_BOUND_CENSUS = NUMERICALLY_CERTIFIED_FINITE_0_VIOLATIONS
    TPC340_SCHUR_BRANCH_CENSUS = NUMERICALLY_CERTIFIED_FINITE_54_RECORDS
    TPC340_FROBENIUS_BRANCH_CENSUS = NUMERICALLY_CERTIFIED_FINITE_162_RECORDS
    TPC340_ZERO_SUPPORT_IMPROVEMENT = NUMERICALLY_CERTIFIED_FINITE_FACTOR_1.25_TO_4.70
    TPC340_BROAD_TIGHTNESS = REFUTED_SCOPED
    TPC340_ARITHMETIC_ADVANCE = NO
    TPC340_FIXED_POWER_CREDIT = 0
    TPC340_SOURCE_UNIFORM_L2 = OPEN
    TPC340_FULL_GATE_B = OPEN
    TPC340_TWIN_PRIME_RESULT = NONE
    TPC340_STATUS = NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE
    TPC340_ROUND2_CLUE = TEST_NUISANCE_ORTHOGONALIZATION_OR_ADVERSARIAL_HOLDOUT

## 0.133 released：TPC-339 mask-aware Frobenius envelope

项目：papers/tpc-339-mask-aware-frobenius-envelope/

类型：**NUMERICALLY_CERTIFIED_FINITE_MASK_AWARE_FROBENIUS_ENVELOPE**。

TPC-339 在 TPC-338 的九-control panel 上将 signed covariance heuristic 替换为
support-restricted sign-free bound
`||Ax||^2 <= ||A[:,S]||_F^2 ||x||^2`。216 条记录中 198 条非空，bound violations 为
0；broad masks 的 occupancy 全部低于 `0.2`，而 prime-power singleton-like records
可以达到 equality。

最强正结果：把控制依赖的 covariance sign 换成 universally valid 的 finite support
operator envelope。

最强 obstruction：broad-mask occupancy 仅为 `0.0074766258--0.1868550366`，elementary
envelope 明显偏松，不能作为 sharp response theorem。

开放定理：masked Gram sharpening、source-uniform arithmetic `L2`、fixed-power credit
与 Route-B Gate B；arithmetic advance 为 `NO`。

可复用结构：`support mask -> column submatrix -> sign-free Frobenius gain -> occupancy`。

ROUND2_CLUE：`COMBINE_SUPPORT_FROBENIUS_WITH_A_GLOBAL_SCHUR_BOUND`。

    TPC339_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_MASK_AWARE_FROBENIUS_ENVELOPE
    TPC339_SUPPORT_FROBENIUS_BOUND = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC339_MASKED_CONTROL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_RECORDS
    TPC339_BOUND_CENSUS = NUMERICALLY_CERTIFIED_FINITE_0_VIOLATIONS
    TPC339_BROAD_MASK_SLACK = NUMERICALLY_CERTIFIED_FINITE_OCCUPANCY_BELOW_0.2
    TPC339_SIMPLE_ENVELOPE_TIGHTNESS = REFUTED_SCOPED
    TPC339_ARITHMETIC_ADVANCE = NO
    TPC339_FIXED_POWER_CREDIT = 0
    TPC339_SOURCE_UNIFORM_L2 = OPEN
    TPC339_FULL_GATE_B = OPEN
    TPC339_TWIN_PRIME_RESULT = NONE
    TPC339_STATUS = NUMERICALLY_CERTIFIED_FINITE_MASK_AWARE_FROBENIUS_ENVELOPE
    TPC339_ROUND2_CLUE = COMBINE_SUPPORT_FROBENIUS_WITH_A_GLOBAL_SCHUR_BOUND

## 0.132 released：TPC-338 growing-control covariance spectrum

项目：papers/tpc-338-growing-control-covariance-spectrum/

类型：**NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_COVARIANCE_SPECTRUM**。

TPC-338 在固定 source/operator 上从五个 controls 扩展到九个 controls。六行的 nine-
control centered fraction 为 `0.8771801838--0.8972635786`；normalized covariance
spectrum 的 `L1` 距离为 `0.0264396313--0.0440591812`。但 twin/zero covariance 在
五-control ensemble 的 6/6 行为负、九-control ensemble 的 6/6 行为正，显示 signed
interaction 不是 canonical。

最强正结果：centered energy dominance 在 growing finite control ensemble 中保持，
并可由 normalized spectrum 描述。

最强 obstruction：nested control enlargement 造成稳定的 twin/zero sign reversal，
因此任何依赖该符号的 reassembly 都被 refute scoped。

开放定理：canonical signed covariance、uniform masked bound、source-uniform arithmetic
`L2` 与 Route-B Gate B；arithmetic advance 为 `NO`。

可复用结构：`nested control orbit -> exact mean/center split -> covariance Gram PSD -> sign audit`。

ROUND2_CLUE：`REPLACE_SIGNED_COVARIANCE_BY_A_SIGN_FREE_MASKED_BOUND`。

    TPC338_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_COVARIANCE_SPECTRUM
    TPC338_NESTED_COVARIANCE_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC338_COVARIANCE_GRAM_PSD = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC338_ENERGY_DOMINANCE_STABILITY = NUMERICALLY_CERTIFIED_FINITE_6_OF_6
    TPC338_TWIN_ZERO_SIGN_STABILITY = REFUTED_SCOPED
    TPC338_TWIN_ZERO_SIGN_REVERSAL = NUMERICALLY_CERTIFIED_FINITE_6_OF_6_NESTED_COMPARISON
    TPC338_ARITHMETIC_ADVANCE = NO
    TPC338_FIXED_POWER_CREDIT = 0
    TPC338_SOURCE_UNIFORM_L2 = OPEN
    TPC338_FULL_GATE_B = OPEN
    TPC338_TWIN_PRIME_RESULT = NONE
    TPC338_STATUS = NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_COVARIANCE_SPECTRUM
    TPC338_ROUND2_CLUE = REPLACE_SIGNED_COVARIANCE_BY_A_SIGN_FREE_MASKED_BOUND

## 0.131 released：TPC-337 control covariance of masked responses

项目：papers/tpc-337-control-covariance-masked-response/

类型：**NUMERICALLY_CERTIFIED_FINITE_CONTROL_COVARIANCE_MASKED_RESPONSE**。

TPC-337 将 TPC-336 的四个 source masks 在五个 coordinate controls 下分别送入固定
operator，建立 class-output covariance Gram ledger。六行中 twin/background covariance
为正、twin/zero 与 background/zero 为负；full centered fraction 为
`0.7850322548--0.8552982168`，coherent fraction 为 `0.1447017832--0.2149677452`。
所有 covariance Gram matrices 的 PSD identity 与 finite mean/center decomposition
均通过独立重放。

最强正结果：source masks、control orbit 与 output covariance 被接到同一可复用 finite
interface。

最强 obstruction：signed off-diagonal covariance 对 control family 敏感，不能直接
作为 arithmetic cancellation law；这引出了 TPC-338 的 growing-control test。

开放定理：control-uniform covariance sign、source-uniform arithmetic `L2`、uniform
masked operator bound 与 Route-B Gate B；arithmetic advance 为 `NO`。

可复用结构：`masked source classes -> control orbit -> covariance Gram PSD -> sign firewall`。

ROUND2_CLUE：`GROW_THE_CONTROL_ORBIT_AND_TEST_SIGN_STABILITY`。

    TPC337_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CONTROL_COVARIANCE_MASKED_RESPONSE
    TPC337_COVARIANCE_GRAM_PSD = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC337_MASKED_RESPONSE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_ROWS
    TPC337_CENTERED_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_6_OF_6
    TPC337_SIGNED_COVARIANCE_CANONICALITY = OPEN
    TPC337_ARITHMETIC_ADVANCE = NO
    TPC337_FIXED_POWER_CREDIT = 0
    TPC337_SOURCE_UNIFORM_L2 = OPEN
    TPC337_FULL_GATE_B = OPEN
    TPC337_TWIN_PRIME_RESULT = NONE
    TPC337_STATUS = NUMERICALLY_CERTIFIED_FINITE_CONTROL_COVARIANCE_MASKED_RESPONSE
    TPC337_ROUND2_CLUE = GROW_THE_CONTROL_ORBIT_AND_TEST_SIGN_STABILITY

## 0.130 released：TPC-336 masked signed-Gram response and output interference

项目：papers/tpc-336-masked-signed-gram-response/

类型：**NUMERICALLY_CERTIFIED_FINITE_MASKED_SIGNED_GRAM_RESPONSE**。

TPC-336 承接 TPC-335，把 twin、non-twin、prime-power 与 zero-support 四个 disjoint
source masks 送入固定的 all-plus deleted-diagonal signed-Gram operator（`Q=54`、
exponent `1`、`H=66`）。六个 parent-locked windows 上，四类 self-response gain 的
排序在 `6/6` 行一致：

    zero_support > non_twin_prime_shift > twin_prime > prime_power_shift

对应 gain ranges 分别为 `393547.76798--419768.84446`、`117431.36298--127558.56125`、
`37443.58626--44607.77342` 与 `0--34676.06051`。每一行的 full output response
都需要 destructive cross terms；self-energy sum/full-response energy ratio 为
`[4.8538535937774503,5.4814134328177246]`。这是把 TPC-334/335 的 source ledger
推进到 operator-output 层的独立有限证书，不是 source-uniform operator theorem。

最强正结果：source support、source norm 与 output Gram interaction 已串成同一条
可复用、可独立重放的四 mask interface；六行 gain ordering 和 destructive interaction
均通过 producer、independent replay 与 mutation stress。

最强 obstruction：source-level twin share/norm 不能直接传递为 operator-response
dominance；background/zero-support output pair 的 inner product 全部为负，且输出
interference 显著大于 component self-energy 的简单相加。因而任何 twin-prime
transfer 必须先控制 position-aware cross-class covariance。

开放定理：uniform-in-origin/scale masked operator bound、source-uniform arithmetic
`L2`、strict `1/400` payment 与 Route-B Gate B。fixed-power credit 为 `0`，twin-prime
conclusion 为 `NONE`。官方 Route-A/Route-B evaluator files 在 checkout 中缺失，
local Bridge-B 仍只是 fail-closed fallback。

可复用结构：

    locked source -> support masks -> exact norm split -> masked output Gram
                  -> cross-class covariance ledger -> independent replay/firewall

ROUND2_CLUE：`RETURN_TO_CONTROL_COVARIANCE_OR_SEEK_UNIFORM_MASKED_OPERATOR_BOUND`。

    TPC336_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_MASKED_SIGNED_GRAM_RESPONSE
    TPC336_MASK_RESPONSE_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC336_FIXED_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_ROWS
    TPC336_GAIN_ORDERING = NUMERICALLY_CERTIFIED_FINITE_6_OF_6
    TPC336_DESTRUCTIVE_OUTPUT_INTERACTION = NUMERICALLY_CERTIFIED_FINITE_6_OF_6
    TPC336_TWIN_RESPONSE_DOMINANCE = REFUTED_SCOPED_FINITE_PANEL
    TPC336_ARITHMETIC_ADVANCE = NO
    TPC336_FIXED_POWER_CREDIT = 0
    TPC336_SOURCE_UNIFORM_L2 = OPEN
    TPC336_FULL_GATE_B = OPEN
    TPC336_TWIN_PRIME_RESULT = NONE
    TPC336_STATUS = NUMERICALLY_CERTIFIED_FINITE_MASKED_SIGNED_GRAM_RESPONSE
    TPC336_ROUND2_CLUE = RETURN_TO_CONTROL_COVARIANCE_OR_SEEK_UNIFORM_MASKED_OPERATOR_BOUND

## 0.129 released：TPC-335 twin-isolated source norm decomposition

项目：papers/tpc-335-twin-isolated-source-norm/

类型：**NUMERICALLY_CERTIFIED_FINITE_TWIN_ISOLATED_SOURCE_NORM**。

TPC-335 将 TPC-334 的四个 support masks 作用于完整 residual `beta=Lambda-b`，在
有限数组上给出 exact disjoint norm split。六个 windows 的 twin residual-norm fraction
为 `0.095561720872944358--0.12241598178733512`，non-twin background 为
`0.67049701649956917--0.69656908745054080`，prime-power fraction 至多
`0.0018737060121997208`；twin norm share 相对 raw cross share 的 amplification
为 `1.7065194950664935--1.7705815591117822`。

最强正结果：twin signal 在 source norm 中确实非零且可分离，四 mask 的正交 norm
identity 与六行 independent replay 均通过。

最强 obstruction：twin 不是 residual-energy 主导类，non-twin background 仍占
`65%--72%`；source-level amplification 也不足以支付 arithmetic power。

开放定理：masked operator response、source-uniform `L2`、strict `1/400` payment 与
Route-B Gate B；fixed-power credit 为 `0`，twin-prime conclusion 为 `NONE`。

可复用结构：`cross-term support -> disjoint residual masks -> exact norm ledger`。

ROUND2_CLUE：`TEST_TWIN_ISOLATED_SOURCE_THROUGH_FIXED_SIGNED_GRAM_OPERATOR`。

    TPC335_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_TWIN_ISOLATED_SOURCE_NORM
    TPC335_MASK_NORM_SPLIT = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC335_TWIN_NORM_SHARE = NUMERICALLY_CERTIFIED_FINITE_6_ROWS
    TPC335_BACKGROUND_NORM_SHARE = NUMERICALLY_CERTIFIED_FINITE_6_ROWS
    TPC335_ARITHMETIC_ADVANCE = NO
    TPC335_FIXED_POWER_CREDIT = 0
    TPC335_SOURCE_UNIFORM_L2 = OPEN
    TPC335_FULL_GATE_B = OPEN
    TPC335_TWIN_PRIME_RESULT = NONE
    TPC335_STATUS = NUMERICALLY_CERTIFIED_FINITE_TWIN_ISOLATED_SOURCE_NORM
    TPC335_ROUND2_CLUE = TEST_TWIN_ISOLATED_SOURCE_THROUGH_FIXED_SIGNED_GRAM_OPERATOR

## 0.128 released：TPC-334 cross-term support ledger

项目：papers/tpc-334-cross-term-support-ledger/

类型：**NUMERICALLY_CERTIFIED_FINITE_CROSS_TERM_SUPPORT_LEDGER**。

TPC-334 承接 TPC-333，把 `<Lambda,b>` 按 `twin_prime`、`non_twin_prime_shift`、
`prime_power_shift` 与 `zero_support` 四类 exact finite support 分账。六个 parent-locked
windows 上，twin share 为 `0.054296754369378503--0.071734300218214184`，non-twin
prime-shift share 为 `0.92826569978178597--0.94419571979139760`，prime-power share
至多 `0.0028651911963981512`；六行都满足 twin `<10%`、non-twin `>90%`。

最强正结果：cross term 的 support attribution 已从总量读数推进为可审计的 prime-class
分解，且 exact partition、independent replay 与 stress 均通过。

最强 obstruction：raw polarization cross term 主要来自 `t+2` 为 prime 而 `t` 为奇
合数的 background，不能直接作为 twin-prime proxy；这只是 scoped finite obstruction，
不否定任何其他 twin-prime route。

开放定理：twin-isolated source norm、masked response、source-uniform arithmetic `L2`、
strict `1/400` payment 与 Route-B Gate B；fixed-power credit 为 `0`，twin-prime
conclusion 为 `NONE`。

可复用结构：`polarization cross term -> exact prime-power support partition -> twin/background masks`。

ROUND2_CLUE：`BUILD_TWIN_ISOLATED_RESIDUAL_NORM_LEDGER`。

    TPC334_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_TERM_SUPPORT_LEDGER
    TPC334_SUPPORT_PARTITION = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC334_TWIN_SHARE = NUMERICALLY_CERTIFIED_FINITE_6_ROWS
    TPC334_NON_TWIN_SHARE = NUMERICALLY_CERTIFIED_FINITE_6_ROWS
    TPC334_ARITHMETIC_ADVANCE = NO
    TPC334_FIXED_POWER_CREDIT = 0
    TPC334_SOURCE_UNIFORM_L2 = OPEN
    TPC334_FULL_GATE_B = OPEN
    TPC334_TWIN_PRIME_RESULT = NONE
    TPC334_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_TERM_SUPPORT_LEDGER
    TPC334_ROUND2_CLUE = BUILD_TWIN_ISOLATED_RESIDUAL_NORM_LEDGER

## 0.127 released：TPC-333 source polarization and cross-term ledger

项目：papers/tpc-333-source-polarization-cross-term/

类型：**NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER**。

TPC-333 承接 TPC-332 的真实结论：control-average 分解在 growing finite ensemble 上
复现，但 arithmetic source layer 仍是 live gate。它在同一两个新 origins `42001,44001`
与三个 scales `2048,4096,8192` 上去掉 dense operator，只记录
`||Lambda-b||^2=||Lambda||^2+||b||^2-2<Lambda,b>` 的四项、四个 nested-scale pairs
与 dimensionless coefficient
`kappa=2<Lambda,b>/(||Lambda||^2+||b||^2)`。六个 rows 的 `kappa` 全部位于
`[0.35486589921455675,0.36250235375855522]`，residual fraction 位于
`[0.63749764624144467,0.64513410078544309]`；独立 reverse-factorization replay 与
mutation stress 均通过。

最强正结果：source polarization 被拆成可复用、可审计的 finite interface，且六个窗口
均落入预声明的 mixed-cancellation interval。

最强 obstruction：本面板同时 `REFUTED_SCOPED` 了 near-orthogonality 与 near-total
cancellation 两个极端解释；这不是任意 origin/scale 的 uniform bound。

开放定理：source-uniform arithmetic `L2`、交叉项的 twin-prime support attribution、
strict `1/400` payment 与 Route-B Gate B。fixed-power credit 为 `0`，twin-prime
conclusion 为 `NONE`。官方 Route-A/Route-B evaluator files absent，local Bridge-B
仍仅是 fail-closed fallback。

可复用结构：

    locked source -> four-term polarization ledger -> dimensionless kappa/rho
                  -> nested-scale comparison -> support attribution

ROUND2_CLUE：`CLASSIFY_CROSS_TERM_SUPPORT_BY_PRIME_POWER_AND_TWIN_MASK`。

    TPC333_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER
    TPC333_POLARIZATION_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC333_SIX_WINDOW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS
    TPC333_CANCELLATION_COEFFICIENT = NUMERICALLY_CERTIFIED_FINITE_0.35_TO_0.37
    TPC333_NEAR_ORTHOGONALITY = REFUTED_SCOPED_FINITE_PANEL
    TPC333_NEAR_TOTAL_CANCELLATION = REFUTED_SCOPED_FINITE_PANEL
    TPC333_ARITHMETIC_ADVANCE = NO
    TPC333_FIXED_POWER_CREDIT = 0
    TPC333_SOURCE_UNIFORM_L2 = OPEN
    TPC333_FULL_GATE_B = OPEN
    TPC333_TWIN_PRIME_RESULT = NONE
    TPC333_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER
    TPC333_ROUND2_CLUE = CLASSIFY_CROSS_TERM_SUPPORT_BY_PRIME_POWER_AND_TWIN_MASK

## 0.126 released：TPC-332 growing control-average ensemble

项目：papers/tpc-332-growing-control-average-ensemble/

类型：**NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_AVERAGE_ENSEMBLE**。

TPC-332 将 TPC-331 的五-control mean/centered identity 搬到 disjoint origins
`42001,44001` 与 scales `2048,4096,8192`，得到 `48` rows、`192` law-level
decompositions，并额外记录六个 source-L2 polarization rows。all-plus control-average
与 centered components 为 `48/48` positive，coherent mean 为 `47/48`；unpermuted
residual 为 `27 negative / 21 positive`。这是 growing finite replication 与
position-aware obstruction，不是 source-uniform arithmetic theorem。

    TPC332_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_AVERAGE_ENSEMBLE
    TPC332_EXACT_MEAN_CENTERED_DECOMPOSITION = PROVED_EXACT_FINITE
    TPC332_CONTROL_AVERAGE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_48_OF_48
    TPC332_CENTERED_POSITION_CENSUS = NUMERICALLY_CERTIFIED_FINITE_48_OF_48
    TPC332_COHERENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_47_OF_48
    TPC332_ARITHMETIC_ADVANCE = NO
    TPC332_FIXED_POWER_CREDIT = 0
    TPC332_FULL_GATE_B = OPEN
    TPC332_TWIN_PRIME_RESULT = NONE
    TPC332_ROUND2_CLUE = SEPARATE_SOURCE_L2_CROSS_TERM_AND_TEST_CONTROL_COVARIANCE_SPECTRUM

## 0.125 current：TPC-331 control-average and centered response decomposition

项目：papers/tpc-331-control-average-centered-response-decomposition/

类型：**NUMERICALLY_CERTIFIED_FINITE_CONTROL_AVERAGE_CENTERED_RESPONSE_DECOMPOSITION**。

TPC-331 承接 TPC-330，把 identity、三个 odd-affine bijections 与 reversal 组成一个
五元素 finite control orbit。对 `w_j=P_jv`、`̄v=mean_j w_j`、`z_j=w_j-̄v`，任意
有限 quadratic form 都有
`mean_j q(w_j)=q(̄v)+mean_j q(z_j)`；这同时应用于 signed-Gram energy `E`、
coordinate diagonal `D` 与 off-diagonal `O=E-D`。同一两个 held-out origins
`28001,36001`、两个 scales `4096,8192`、四个 shell anchors、两个 exponents、
四个 sign laws 与锁定的 V59 source-native residual 全部保持不变，得到 `32` rows、
`128` 个 law-level decompositions 与一个 exact rational anchor。

最强正结果：all-plus 的 control-average 与 centered-position components 均为
`32/32` positive，coherent mean 为 `31/32` positive；平均项与 centered 项分别
承载约 `14.8%--39.7%` 与 `60.3%--85.2%` 的有限 all-plus energy。三种分解身份的
exact rational anchor 全部通过，float64 identity residual 仍在声明的 guard 内。

最强 obstruction：有限 positive response 不能被简化为“只有 coherent source-average”
或“只有 centered position”之一；coherent component 有一个 negative row，而
centered component 仍占主要 energy。因而下一条 source-uniform theorem 必须同时控制
source-aligned 与 position-aware 两个 component；control averaging 本身不是 arithmetic
`L2` cancellation。

开放定理：growing source-native `L2`、uniform position-response bound、canonical sign
law、strict `1/400` payment 与 Route-B Gate B。fixed-power credit 仍为 `0`，twin-prime
conclusion 为 `NONE`。Session-named evaluator files absent，local Bridge-B 仅作
fail-closed fallback，不宣称 official Route-A/Route-B pass。

可复用结构：

    locked source -> finite control orbit -> exact quadratic mean/center split
                  -> E/D/O component census -> independent replay/firewall

ROUND2_CLUE：
TEST_CONTROL_AVERAGE_ON_GROWING_SOURCE_ENSEMBLE_AND_SEPARATE_ARITHMETIC_L2。

    TPC331_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CONTROL_AVERAGE_CENTERED_RESPONSE_DECOMPOSITION
    TPC331_EXACT_MEAN_CENTERED_DECOMPOSITION = PROVED_EXACT_FINITE
    TPC331_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC331_CONTROL_AVERAGE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC331_CENTERED_POSITION_CENSUS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC331_COHERENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_31_OF_32
    TPC331_NUMERIC_IDENTITY = NUMERICALLY_CERTIFIED_FINITE
    TPC331_ARITHMETIC_ADVANCE = NO
    TPC331_FIXED_POWER_CREDIT = 0
    TPC331_GROWING_SOURCE_NATIVE_L2 = OPEN
    TPC331_FULL_GATE_B = OPEN
    TPC331_TWIN_PRIME_RESULT = NONE
    TPC331_STATUS = NUMERICALLY_CERTIFIED_FINITE_CONTROL_AVERAGE_CENTERED_RESPONSE_DECOMPOSITION
    TPC331_ROUND2_CLUE = TEST_CONTROL_AVERAGE_ON_GROWING_SOURCE_ENSEMBLE_AND_SEPARATE_ARITHMETIC_L2

## 0.124 previous：TPC-330 multi-permutation response spectrum

项目：papers/tpc-330-multi-permutation-response-spectrum/

类型：**NUMERICALLY_CERTIFIED_FINITE_MULTI_PERMUTATION_RESPONSE_SPECTRUM**。

TPC-330 承接 TPC-329，保留两个 held-out origins `28001,36001`、两个 scales
`4096,8192`、四个 shell anchors、两个 exponents、四个 sign laws 与锁定的 V59
source-native residual。新增五个预声明的 coordinate bijections：identity、
`(3i+11) mod M`、`(5i+17) mod M`、`(7i+29) mod M` 与 reversal `M-1-i`，其中
`M=N/2`。五个 controls 在 source counts `2048,4096` 上都保持 source multiset
与 `L2` norm，形成 `640` 个 law/control observations、`10` 组 pairwise summaries，
并保留 `64` 个 two-scale pairings。

最强正结果：三个非平凡 affine controls 的 all-plus off-diagonal sign 都是
`32/32` positive；identity 与 reversal 都是 `31/32` negative、`1/32` positive。
因此 TPC-329 的 `(5,17)` effect 在两个新 affine controls 上复现，而不是单一
permutation 的孤立现象。all-plus 的五-control signatures 为
`negative|positive|positive|positive|negative`（`31` rows）与全 positive（`1` row）。

最强 obstruction：source multiset 或 source `L2` norm 仍不能决定该 physical
diagnostic 的 sign；同时“单一 `(5,17)` permutation accident”在本 finite panel
上被 `REFUTED_SCOPED`。identity/reversal classification 相同但 ratio 仍有差异，
所以不宣称 exact reflection symmetry。producer、independent reverse-order replay、
stress、PDF 与 local Bridge-B 组成 finite certificate stack。

开放定理：控制均值与 centered position response 的 exact structural decomposition，
以及其 source-uniform bound；growing source-native `L2`、canonical sign、strict
`1/400` payment 与 Route-B Gate B。fixed-power credit 仍为 `0`，twin-prime
conclusion 为 `NONE`。Session-named evaluator files absent，故不宣称 official
Route-A/Route-B pass。

可复用结构：

    locked source -> coherent signed Gram -> finite control orbit
                  -> response spectrum/pairwise geometry -> independent replay/firewall

ROUND2_CLUE：
DECOMPOSE_POSITION_RESPONSE_INTO_AFFINE_REVERSAL_AND_SOURCE_ALIGNED_COMPONENTS。

    TPC330_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_MULTI_PERMUTATION_RESPONSE_SPECTRUM
    TPC330_EXACT_GRAM_DECOMPOSITION = PROVED_EXACT_FINITE
    TPC330_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC330_COMPONENT_CONTROLS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC330_MULTI_PERMUTATION_SPECTRUM = NUMERICALLY_CERTIFIED_FINITE_5_CONTROLS
    TPC330_AFFINE_ALL_PLUS_CONSENSUS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC330_SIGN_AT_SCALE_GROWTH = NUMERICALLY_CERTIFIED_FINITE
    TPC330_ARITHMETIC_ADVANCE = NO
    TPC330_FIXED_POWER_CREDIT = 0
    TPC330_GROWING_SOURCE_NATIVE_L2 = OPEN
    TPC330_FULL_GATE_B = OPEN
    TPC330_TWIN_PRIME_RESULT = NONE
    TPC330_STATUS = NUMERICALLY_CERTIFIED_FINITE_MULTI_PERMUTATION_RESPONSE_SPECTRUM
    TPC330_ROUND2_CLUE = DECOMPOSE_POSITION_RESPONSE_INTO_AFFINE_REVERSAL_AND_SOURCE_ALIGNED_COMPONENTS

## 0.123 previous：TPC-329 held-out growing source-native placement audit

项目：papers/tpc-329-heldout-growing-source-native-audit/

类型：**NUMERICALLY_CERTIFIED_FINITE_HELDOUT_GROWING_SOURCE_NATIVE_AUDIT**。

TPC-329 承接 TPC-328，在两个此前未使用的 origins `28001,36001` 与两个更大
scales `4096,8192` 上重放锁定的 V59 source-native residual。保留
`H=66`、`Q={24,36,54,80}`、`s={1,2}`、literal masks 与四个 sign laws，形成
`32` 个 rows，并在固定 origin/Q/s 下形成 `64` 个 scale-paired records。

最强正结果：实际 all-plus 的 off-diagonal census 为 `31` negative / `1` positive；
两个 component controls 为 `32/32` positive；all-plus scale signs 在 `15/16`
pairings 中保持，energy growth factor 为 `1.9663131482...`--`2.1432646657...`。
更关键的是预声明 affine placement null
`pi(i)=(5*i+17) mod source_count` 在两个 source counts 上都是 bijection，保持
source multiset 与 `L2` norm。置换后的 all-plus census 为 `0` negative / `32`
positive，`31/32` 个 classifications 改变；共完成 `128` 个 placement comparisons。

最强 obstruction：在该 finite panel 上，all-plus off-diagonal sign 不能由 source
multiset 或 source `L2` norm 单独决定。这个结论是 `REFUTED_SCOPED`，只针对声明的
operator、source model、permutation 与 finite rows，不外推为随机置换定理或 growing
arithmetic theorem。

开放定理：position-aware 的 source-uniform signed-Gram bound、canonical arithmetic
sign、growing source-native `L2` estimate、strict `1/400` payment 与 Route-B Gate B。
fixed-power credit 仍为 `0`，twin-prime conclusion 为 `NONE`。Session-named
evaluator files absent，故不宣称 official Route-A/Route-B pass。

可复用结构：

    locked source -> coherent signed Gram -> actual/null placement pair
                  -> two-scale growth audit -> independent replay/firewall

ROUND2_CLUE：
SEPARATE_SOURCE_NORM_FROM_ARITHMETIC_PLACEMENT_WITH_MULTIPLE_PREDECLARED_CONTROLS。

    TPC329_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_HELDOUT_GROWING_SOURCE_NATIVE_AUDIT
    TPC329_EXACT_GRAM_DECOMPOSITION = PROVED_EXACT_FINITE
    TPC329_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC329_COMPONENT_CONTROLS = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC329_PLACEMENT_NULL = NUMERICALLY_CERTIFIED_FINITE_MULTISET_PRESERVING_CONTROL
    TPC329_ALL_PLUS_ACTUAL = NUMERICALLY_CERTIFIED_FINITE_31_NEGATIVE_1_POSITIVE
    TPC329_ALL_PLUS_PERMUTED = NUMERICALLY_CERTIFIED_FINITE_0_NEGATIVE_32_POSITIVE
    TPC329_PLACEMENT_CHANGES = NUMERICALLY_CERTIFIED_FINITE_31_OF_32
    TPC329_ARITHMETIC_ADVANCE = NO
    TPC329_FIXED_POWER_CREDIT = 0
    TPC329_GROWING_SOURCE_NATIVE_L2 = OPEN
    TPC329_FULL_GATE_B = OPEN
    TPC329_TWIN_PRIME_RESULT = NONE
    TPC329_STATUS = NUMERICALLY_CERTIFIED_FINITE_HELDOUT_GROWING_SOURCE_NATIVE_AUDIT
    TPC329_ROUND2_CLUE = SEPARATE_SOURCE_NORM_FROM_ARITHMETIC_PLACEMENT_WITH_MULTIPLE_PREDECLARED_CONTROLS

## 0.122 previous：TPC-328 source-native arithmetic `L2` cancellation

项目：papers/tpc-328-source-native-l2-cancellation/

类型：**NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_L2_CANCELLATION_ATLAS**。

TPC-328 承接 TPC-327，把锁定的 V59 source-native residual
`beta_o^(2)(t)=Lambda(t+2)-b^(2)(t)` 直接送入同一 literal deleted-diagonal
centered prime-shell operator。对 origins `12001,16001,20001`、scales
`320,640,1280,2560`、`Q={24,36,54,80}` 与 `s={1,2}`，共完成 `96` 个
source-native rows。对任意有限 vector，`E_e(v)=D_e(v)+O_e(v)` 的 source-coordinate
Gram decomposition 是 `PROVED_EXACT_FINITE`；V59 source formula 在声明的有限
Euler/log enclosure 下是 `PROVED_EXACT_FINITE_DECLARED_MODEL`。

最强正结果：实际 arithmetic residual 首次接入 coherent operator；四个 declared
sign laws 的 `E/D` 与 off-diagonal sign 全部由独立 reverse-order replay 重算。all-plus
residual 的 `O<0/O>0` 为 `81/15`，alternating、mod-4、half-split 分别为
`73/23`、`74/22`、`61/35`，均无 unresolved row；Lambda 与 comparison component
controls 均为 `96/96` positive。exact anchor `[20001,20016]`, `Q=4`, `s=1`
保存三项有理 Gram digest，stress、PDF 与 local Bridge-B normal/optimized equality
均通过。

最强 obstruction：四个预注册 sign laws 都有 positive off-diagonal rows，因此
`E_e(beta)<=D_e(beta)` 不能作为该有限面板上的 uniform contraction；all-plus 的
`15/96` positive rows 尤其直接。这个结论是 `REFUTED_SCOPED`，不否定其他 sign、
其他 normalization 或 growing theorem。

开放定理：source-uniform growing arithmetic `L2` bound、canonical arithmetic sign、
literal operator-norm estimate、strict `1/400` payment 与 Route-B Gate B。fixed-power
credit 仍为 `0`，twin-prime conclusion 为 `NONE`。Session-named evaluator files absent，
故不宣称 official Route-A/Route-B pass。

可复用结构：

    source-native V59 residual
        + coherent prime-shell matrix
        -> exact coordinate Gram split and guarded finite sign atlas

ROUND2_CLUE：
TEST_SOURCE_NATIVE_L2_ON_GROWING_ORIGIN_ENSEMBLE_OR_PROVE_SIGNED_GRAM_BOUND。

    TPC328_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_L2_CANCELLATION_ATLAS
    TPC328_EXACT_GRAM_DECOMPOSITION = PROVED_EXACT_FINITE
    TPC328_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC328_COMPONENT_CONTROLS = NUMERICALLY_CERTIFIED_FINITE_96_OF_96
    TPC328_ALL_PLUS_CANCELLATION = NUMERICALLY_CERTIFIED_FINITE_81_OF_96
    TPC328_ALL_PLUS_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_15_OF_96
    TPC328_NO_UNIFORM_SIGNED_CONTRACTION = REFUTED_SCOPED_FOUR_DECLARED_LAWS
    TPC328_ARITHMETIC_ADVANCE = NO
    TPC328_FIXED_POWER_CREDIT = 0
    TPC328_GROWING_SOURCE_NATIVE_L2 = OPEN
    TPC328_FULL_GATE_B = OPEN
    TPC328_TWIN_PRIME_RESULT = NONE
    TPC328_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_L2_CANCELLATION_ATLAS
    TPC328_ROUND2_CLUE = TEST_SOURCE_NATIVE_L2_ON_GROWING_ORIGIN_ENSEMBLE_OR_PROVE_SIGNED_GRAM_BOUND

## 0.121 previous：TPC-327 three-origin scale-ladder triangulation

项目：papers/tpc-327-three-origin-scale-triangulation/

类型：**NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION**。

TPC-327 承接 TPC-326，在第三个完全 disjoint 的 source origin `20001` 上复制同一
literal deleted-diagonal centered prime-shell operator 的四档 source-scale ladder。
新 origin 的 source counts 仍为 `160,320,640,1280`；`H=66`、`Q={24,36,54,80}`、
`s={1,2}` 与四个 predeclared sign laws 全部冻结，总计 32 个新 rows。与前两个
origin `12001`、`16001` 合并后，首次得到三-origin pooled envelope range。

最强正结果：新 origin 的 all-plus normalized profile 在 32/32 行 majorizes direct
profile；四种 profile-majorization 与 energy-side census 同时匹配两个 parent。
三-origin 各尺度 range 均非零，最大 TV range 为 `0.0007970083<0.001`，最大 energy
range 为 `0.0045518412<0.005`。producer、independent reverse/einsum、stress、exact
rational anchor、PDF 与 local Bridge-B normal/optimized equality 均通过。

最强 obstruction：三组有限 origins 和四组有限 rungs 只给出 finite triangulation，
不能升级为 source-uniform 或 growing theorem；继承阈值是 finite controls，不是
analytic error term。没有 canonical arithmetic sign 或 source-native cancellation。

开放定理：origin-ensemble 的 growing-scale uniform bound，或者真正 source-native
signed arithmetic `L2` bound。fixed-power credit、strict `1/400` payment、full Gate B
与 twin-prime conclusion 仍 OPEN/NONE。Session-named evaluator files absent，故不宣称
official Route-A/Route-B pass。

可复用结构：

    parent-locked finite ladders at three disjoint origins
        + pooled per-scale ranges
        -> non-vacuous finite triangulation firewall

ROUND2_CLUE：
TEST_ORIGIN_ENSEMBLE_SCALE_GROWTH_OR_SOURCE_NATIVE_ARITHMETIC_L2。

    TPC327_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION
    TPC327_THREE_ORIGIN_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_3_ORIGINS
    TPC327_ALL_PLUS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32_NEW_ORIGIN
    TPC327_CENSUS_MATCH = NUMERICALLY_CERTIFIED_FINITE_MATCH_TO_BOTH_PARENTS
    TPC327_ENVELOPE_TRIANGULATION = NUMERICALLY_CERTIFIED_FINITE_WITHIN_DECLARED_THRESHOLDS
    TPC327_ARITHMETIC_ADVANCE = NO
    TPC327_FIXED_POWER_CREDIT = 0
    TPC327_FULL_GATE_B = OPEN
    TPC327_TWIN_PRIME_RESULT = NONE
    TPC327_STATUS = NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION
    TPC327_ROUND2_CLUE = TEST_ORIGIN_ENSEMBLE_SCALE_GROWTH_OR_SOURCE_NATIVE_ARITHMETIC_L2

## 0.120 previous：TPC-326 cross-origin scale-ladder replication

项目：papers/tpc-326-cross-origin-scale-replication/

类型：**NUMERICALLY_CERTIFIED_FINITE_CROSS_ORIGIN_SCALE_LADDER_REPLICATION**。

TPC-326 承接 TPC-325 的 fixed-origin source-scale ladder，在完全 disjoint 的第二个
source origin 16001 上复制同一 literal deleted-diagonal centered prime-shell operator。
四个 nested rungs 的 source counts 仍为 160,320,640,1280；H=66、Q={24,36,54,80}、
s={1,2} 与四个 predeclared sign laws 全部冻结，总计 32 个新 rows。

最强正结果：新的 all-plus normalized profile 在 32/32 行 majorizes direct profile；
四种 profile-majorization census 与 TPC-325 完全匹配（all-plus 32/0、alternating
21/11、mod-4 26/6、half-split 23/9），energy-side census 也匹配。新的 TV lower
envelope 与 energy upper envelope 相对 parent 的最大差分别为
0.000797...<0.001 与 0.004552...<0.005；producer、independent reverse/einsum、
cross-origin stress、exact rational anchor、PDF 与 local Bridge-B normal/optimized
equality 均通过。

最强 obstruction：这是两个有限 origins、四个有限 rungs 的 replication，不是
uniform-in-source 或 growing-scale theorem。阈值是实验控制而非 analytic error term；
没有出现 canonical arithmetic sign 或 source-native cancellation。

开放定理：多 origin 的 growing-scale uniform statement，或者真正 source-native signed
arithmetic L2 bound。fixed-power credit、strict 1/400 payment、full Gate B 与
twin-prime conclusion 仍 OPEN/NONE。Session-named evaluator files absent，故不宣称
official Route-A/Route-B pass。

可复用结构：

    parent-locked finite scale ladder
        + disjoint-origin replication
        -> census / envelope agreement firewall

ROUND2_CLUE：
TEST_CROSS_ORIGIN_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2。

    TPC326_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_ORIGIN_SCALE_LADDER_REPLICATION
    TPC326_CROSS_ORIGIN_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_2_ORIGINS
    TPC326_ALL_PLUS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC326_CENSUS_MATCH = NUMERICALLY_CERTIFIED_FINITE_PARENT_MATCH
    TPC326_ENVELOPE_AGREEMENT = NUMERICALLY_CERTIFIED_FINITE_WITHIN_DECLARED_THRESHOLDS
    TPC326_ARITHMETIC_ADVANCE = NO
    TPC326_FIXED_POWER_CREDIT = 0
    TPC326_FULL_GATE_B = OPEN
    TPC326_TWIN_PRIME_RESULT = NONE
    TPC326_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_ORIGIN_SCALE_LADDER_REPLICATION
    TPC326_ROUND2_CLUE = TEST_CROSS_ORIGIN_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2

## 0.119 previous：TPC-325 source-scale ladder profile audit

项目：papers/tpc-325-scale-ladder-profile/

类型：**NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT**。

TPC-325 承接 TPC-324 的 source-location holdout，在同一 literal
deleted-diagonal centered prime-shell block family 上冻结新 source origin `12001`，
只改变 nested source cardinality。四个 rungs 为 `N={320,640,1280,2560}`，实际
source counts 为 `160,320,640,1280`；`H=66`、`Q={24,36,54,80}`、`s={1,2}`
与四个 predeclared sign laws 保持不变，总计 32 rows。all-plus normalized profile
在 32/32 行 majorizes direct profile。每个 rung 的 all-plus profile prefix lower
endpoint 均为正；outward lower TV envelope 与 outward upper energy envelope 都沿
四档严格下降。

最强正结果：固定 origin 的四档 scale ladder 给出 all-plus `32/32` profile
majorization，并由三路径 producer、independent reverse/einsum replay、stress suite、
exact rational anchor、PDF 与 local Bridge-B normal/optimized equality 共同封存。

最强 obstruction：四个有限 rungs 改变了 Hilbert-space dimension；严格下降的 envelope
只是有限 numerical observation，不能升级为 growing-X limit、uniform-in-source law 或
arithmetic cancellation。alternative laws 的 majorizing/mixed 计数为 alternating
`21/11`、mod-4 `26/6`、half-split `23/9`，没有选出 canonical arithmetic sign。

开放定理：disjoint scale replication 或 source-native signed arithmetic `L2`，随后才
能讨论 uniform promotion。fixed-power credit、strict `1/400` payment、full Gate B 与
twin-prime conclusion 仍 OPEN/NONE。Session-named evaluator files absent，故不宣称
official Route-A/Route-B pass。

可复用结构：

    fixed-origin nested source ladder
        + trace-normalized signed/direct profiles
        -> finite scale-envelope firewall

ROUND2_CLUE：
TEST_SCALE_LADDER_SOURCE_REPLICATION_OR_SOURCE_NATIVE_ARITHMETIC_L2。

    TPC325_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT
    TPC325_ROUTE_ADVANCE = YES_SCOPED_SOURCE_SCALE_LADDER_AUDIT
    TPC325_SCALE_LADDER = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_4_SCALES
    TPC325_ALL_PLUS_SCALE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC325_ALL_PLUS_PROFILE_MAJORISATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
    TPC325_TV_ENVELOPE = NUMERICAL_OBSERVATION_STRICTLY_DESCENDING_4_SCALES
    TPC325_ENERGY_ENVELOPE = NUMERICAL_OBSERVATION_STRICTLY_DESCENDING_4_SCALES
    TPC325_ARITHMETIC_ADVANCE = NO
    TPC325_FIXED_POWER_CREDIT = 0
    TPC325_FULL_GATE_B = OPEN
    TPC325_TWIN_PRIME_RESULT = NONE
    TPC325_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT
    TPC325_ROUND2_CLUE = TEST_SCALE_LADDER_SOURCE_REPLICATION_OR_SOURCE_NATIVE_ARITHMETIC_L2

## 0.118 previous：TPC-324 source-location profile holdout

项目：papers/tpc-324-source-profile-holdout/

类型：**NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION**。

TPC-324 承接 TPC-323 的 signed profile majorization，在同一 literal
deleted-diagonal centered prime-shell block family 上冻结两个新的、彼此以及与
TPC-323 training union 完全 disjoint 的 source panels。每个 panel 的 source counts
为 `320,640,1280`，并保留 `H=66`、`Q={24,36,54,80}`、`s={1,2}` 与四个
predeclared sign laws；总计 48 rows。all-plus normalized profile 在两个 panel
各自 24/24、合计 48/48 行 majorizes direct profile；alternating、mod-4、half-split
的合计 majorizing/mixed 计数为 `34/14`、`42/6`、`36/12`，all-plus energy ratio
为 `6/48` below、`42/48` above。

最强正结果：两个 source-location holdout 对 parent profile-majorization 读数给出
同一有限 census，且由 producer、independent replay、stress suite、PDF 与 local
Bridge-B normal/optimized equality 共同封存。

最强 obstruction：这是有限 source-location replication，而不是 uniform-in-source
或 growing-X theorem；conditional translation covariance 只覆盖共同被所有 shell
素数整除的位移，所选 gap-offset 改变了至少一个 active residue mask。结果仍没有
canonical arithmetic sign、source-native arithmetic `L2`、渐近 power saving、
fixed-power credit 或 twin-prime conclusion。

开放定理：holdout scale ladder 或 source-native signed arithmetic bound，随后才可
讨论 arithmetic promotion。Session-named evaluator files absent，故不宣称 official
Route-A/Route-B pass。

可复用结构：

    conditional translation covariance
        + residue-sensitive source-location holdout
        -> profile replication / arithmetic-uniformity firewall

ROUND2_CLUE：
TEST_HOLDOUT_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2。

    TPC324_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION
    TPC324_ROUTE_ADVANCE = YES_SCOPED_SOURCE_LOCATION_HOLDOUT_REPLICATION
    TPC324_SOURCE_LOCATION_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_48_ROWS_2_PANELS
    TPC324_ALL_PLUS_PROFILE_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_48_OF_48
    TPC324_PER_PANEL_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_24_OF_24_EACH
    TPC324_ALTERNATIVE_PROFILE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_48_ROWS
    TPC324_TRANSLATION_COVARIANCE = PROVED_EXACT_FINITE_CONDITIONAL
    TPC324_ARITHMETIC_ADVANCE = NO
    TPC324_FIXED_POWER_CREDIT = 0
    TPC324_FULL_GATE_B = OPEN
    TPC324_TWIN_PRIME_RESULT = NONE
    TPC324_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION
    TPC324_ROUND2_CLUE = TEST_HOLDOUT_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2

## 0.117 previous：TPC-323 signed profile majorization and amplitude--shape separation

项目：papers/tpc-323-signed-profile-majorization/

类型：**NUMERICALLY_CERTIFIED_FINITE_SIGNED_PROFILE_MAJORISATION_AUDIT**。

TPC-323 承接 TPC-322 的 signed-projector interface，仍使用同一 literal
deleted-diagonal centered prime-shell block family。对 direct Gram
`G_direct=sum_p B_p^T B_p` 与 coherent signed Gram
`G_e=(sum_p e_pB_p)^T(sum_p e_pB_p)`，同时记录能量比
`rho_e=tr(G_e)/tr(G_direct)` 与归一化 profile
`pi(G)=spectrum(G)/tr(G)`。exact trace/profile factorisation 证明总振幅与谱形状
是两个不同坐标。

在 `X={640,1280,2560}`、`Q={24,36,54,80}`、`s={1,2}` 的 24 rows 上，all-plus
profile 在 24/24 行严格 majorizes direct profile；alternating、mod-4、half-split
三条 declared laws 的 majorizing/mixed 计数分别为 17/7、21/3、18/6。all-plus
未归一化 energy ratio 却为 3/24 below、21/24 above，故有限面板明确显示
amplitude/shape decoupling。

最强正结果：exact finite trace/profile factorisation 与 all-plus 24/24 profile
majorization certificate，并由 producer、independent reverse/einsum replay、stress
suite、PDF 和 local Bridge-B normal/optimized equality 共同封存。

最强 obstruction：profile selection 仍只是四个预声明有限 sign laws 与一个有限面板
上的 numerical observation；它没有构造 canonical Möbius/von Mangoldt sign，也没有
source-native arithmetic `L2`、渐近增长 bound 或 twin-prime conclusion。

开放定理：fresh source/profile holdout 或 source-native signed arithmetic bound，随后
才能讨论 fixed-power credit、strict `1/400` payment 与 full Gate B。Session-named
evaluator files absent，故不宣称 official Route-A/Route-B pass。

可复用结构：

    signed projector -> coherent Gram -> trace ratio (amplitude)
                         + normalized ordered spectrum (shape)
                         -> majorization / law-selection firewall

ROUND2_CLUE：
TEST_PROFILE_MAJORISATION_HOLDOUT_OR_SOURCE_NATIVE_ARITHMETIC_L2。

    TPC323_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SIGNED_PROFILE_MAJORISATION_AUDIT
    TPC323_ROUTE_ADVANCE = YES_SCOPED_FINITE_SIGNED_PROFILE_READOUT
    TPC323_SIGNED_PROFILE_FACTORISATION = PROVED_EXACT_FINITE
    TPC323_ALL_PLUS_PROFILE_MAJORISATION = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC323_ALTERNATIVE_PROFILE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_24_ROWS
    TPC323_NAMED_LAW_SELECTION = NUMERICAL_OBSERVATION_ALL_PLUS_UNIQUE_ON_PANEL
    TPC323_AMPLITUDE_SHAPE_DECOUPLING = NUMERICALLY_CERTIFIED_FINITE_ALL_PLUS_3_BELOW_21_ABOVE
    TPC323_ARITHMETIC_ADVANCE = NO
    TPC323_FIXED_POWER_CREDIT = 0
    TPC323_FULL_GATE_B = OPEN
    TPC323_TWIN_PRIME_RESULT = NONE
    TPC323_STATUS = NUMERICALLY_CERTIFIED_FINITE_SIGNED_PROFILE_MAJORISATION_AUDIT

## 0.116 previous：TPC-322 operator-level signed projector and prime-shell reassembly

项目：papers/tpc-322-signed-projector-reassembly/

类型：**NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_REASSEMBLY_ATLAS**。

TPC-322 承接 TPC-321 的 cross-shell profile obstruction，保留同一 literal
deleted-diagonal centered prime-shell block family。令 `A_\oplus v=(B_pv)_p`，并令
`E_e v=m^{-1/2}(e_pv)_p` 为 sign-labelled diagonal isometry，则
`P_e=E_eE_e^*` 是正交 projector，且精确有
`||P_eA_\oplus||_HS^2=m^{-1}||C_e||_F^2`，其中
`C_e=sum_p e_pB_p`。这把 direct-sum energy、coherent signed energy 与 sign law
分开，形成可复用的 operator-level reassembly interface。

在 `X={640,1280,2560}`、`Q={24,36,54,80}`、`s={1,2}` 的 24 rows 上，producer、
independent reverse/einsum replay 与 stress suite 共同认证 exhaustive sign atlas：
每行均存在 `rho<1` 与 `rho>1` 的 sign；极值 ratio 的有限范围分别为
`[0.59905756561947343,0.98033069254228578]` 与
`[1.0122088324409428,6.8711947177741193]`。四个 declared laws 中，all-plus
为 `3/24` below、`21/24` above，index-alternating 为 `21/24` below、`3/24`
above；因此不存在可由该面板选出的 canonical sign law。

最强正结果：signed diagonal projector 的 exact finite identity 与 full-source-column
finite reassembly atlas。

最强 obstruction：sign choice 具有真实有限几何自由度；`rho>1` 是未归一化 coherent
ratio，并不违反 projector contraction，因为实际 projected fraction 是 `rho/m<=1`。
这不是 Möbius/von Mangoldt 权重，也没有 arithmetic `L2` 或渐近增长结论。

开放定理：canonical sign law 的 source-native arithmetic realization、growing signed
reassembly bound、fixed-power credit、strict `1/400` payment、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。Session-named evaluator files absent，故不宣称 official
Route-A/Route-B pass。

可复用结构：

    direct sum blocks -> diagonal isometry -> orthogonal projector
                         -> coherent signed operator -> block Gram sign atlas

ROUND2_CLUE：
TEST_CANONICAL_SIGN_LAWS_AGAINST_OPERATOR_SPECTRAL_PROFILES_AND_SOURCE_NATIVE_ARITHMETIC_L2。

    TPC322_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_REASSEMBLY_ATLAS
    TPC322_ROUTE_ADVANCE = YES_SCOPED_OPERATOR_LEVEL_SIGNED_REASSEMBLY_INTERFACE
    TPC322_SIGNED_PROJECTOR_IDENTITY = PROVED_EXACT_FINITE
    TPC322_OPERATOR_REASSEMBLY_ATLAS = NUMERICALLY_CERTIFIED_FINITE_24_ROWS
    TPC322_MIN_SIGN_EXISTS = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC322_MAX_SIGN_EXISTS = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC322_ALL_PLUS_LAW = REFUTED_FINITE_PANEL
    TPC322_ALTERNATING_LAW = REFUTED_FINITE_PANEL
    TPC322_ARITHMETIC_ADVANCE = NO
    TPC322_FIXED_POWER_CREDIT = 0
    TPC322_FULL_GATE_B = OPEN
    TPC322_TWIN_PRIME_RESULT = NONE
    TPC322_STATUS = NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_REASSEMBLY_ATLAS

## 0.115 previous：TPC-321 cross-shell spectral-profile stability

项目：papers/tpc-321-cross-shell-profile-stability/

类型：**NUMERICALLY_CERTIFIED_FINITE_CROSS_SHELL_PROFILE_SEPARATION_AUDIT**。

TPC-321 承接 TPC-320 的 trace-normalized readout，仍使用同一 literal
deleted-diagonal centered prime-shell Gram；比较固定 X、s 下相邻 Q 壳层的完整排序
profile (p_j=\lambda_j/\operatorname{tr}(G))。在
X=640,1280,2560、Q={24,36,54,80}、s={1,2} 的 24 rows 上形成 18 个
adjacent-Q comparisons。对每一对，三条 producer profile path 的九种组合和
independent reverse/einsum replay 均支持 outward profile-distance intervals；TV 与
Lorenz/Ky Fan cumulative distance 在 18/18 上分别严格超过 0.03 与 0.02。

最强正结果：去除全局振幅后，完整 ordered spectral profile 仍对壳层选择敏感；
最小 TV lower endpoint 为 `0.03212981290619634`，最小 cumulative lower endpoint
为 `0.02339722207455566`。

最强 obstruction：majorization 方向不统一，3 个 comparison 为 forward、2 个为
reverse、13 个为 mixed。因此 `UNIFORM_SHELL_PROFILE` 与
`UNIFORM_MAJORISATION` 只在该有限面板上 `REFUTED_FINITE_PANEL`，不能外推成
所有 X、Q 的否定定理。

开放定理：uniform cross-shell profile bound/limit、signed prime-shell projector
reassembly、arithmetic cancellation、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。Session-named evaluator files absent，故不宣称 official
Route-A/Route-B pass。

可复用结构：

    literal blocks -> PSD Gram -> trace-normalized ordered profile
                     -> cross-shell distance -> majorization firewall

ROUND2_CLUE：
TEST_SIGNED_PROJECTOR_REASSEMBLY_OR_PROVE_A_UNIFORM_SHELL_PROFILE_BOUND_BEFORE_ANY_ARITHMETIC_POWER_CLAIM。

    TPC321_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_SHELL_PROFILE_SEPARATION_AUDIT
    TPC321_ROUTE_ADVANCE = YES_SCOPED_CROSS_SHELL_PROFILE_OBSTRUCTION
    TPC321_PROFILE_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18
    TPC321_TV_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_ALL_GT_0_03
    TPC321_LORENZ_KS_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_ALL_GT_0_02
    TPC321_MAJORISATION_PATTERN = NUMERICAL_OBSERVATION_3_FORWARD_2_REVERSE_13_MIXED
    TPC321_UNIFORM_SHELL_PROFILE = REFUTED_FINITE_PANEL
    TPC321_UNIFORM_MAJORISATION = REFUTED_FINITE_PANEL
    TPC321_ARITHMETIC_ADVANCE = NO
    TPC321_FIXED_POWER_CREDIT = 0
    TPC321_FULL_GATE_B = OPEN
    TPC321_TWIN_PRIME_RESULT = NONE
    TPC321_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_SHELL_PROFILE_SEPARATION_AUDIT

## 0.114 previous：TPC-320 scale-invariant spectral concentration

项目：papers/tpc-320-trace-normalized-spectral-concentration/

类型：**NUMERICALLY_CERTIFIED_FINITE_TRACE_NORMALIZED_SPECTRAL_CONCENTRATION_AUDIT**。

TPC-320 承接 TPC-319 的 normalization firewall，保留同一 literal
deleted-diagonal centered prime-shell Gram，改用
C_k=F_k/trace(G) 的 trace-normalized spectral measure。positive-scalar
invariance、stable rank、participation rank 与 normalized entropy 的代数关系
被分开记账：前者为 exact finite identity，后三者的跨尺度读数是有限观察。
在 X=640,1280,2560、Q={24,36,54,80}、s={1,2} 的 24 rows 和
k={1,2,4,8,16} 五层簇大小上，双 shell 顺序、双谱路径与有限 Weyl quotient
guard 给出 120 个 concentration intervals；80/80 相邻 intervals 严格下降。

最强正结果：去除全局振幅与 source-count bookkeeping 后，五层 top-k spectral
shares 仍在全部 80 个声明 transition 上严格下降；这是一个可复用的
scale-invariant spectral-shape obstruction。

最强 obstruction：stable rank 与 participation rank 虽在 16/16 transitions
上升，normalized entropy 却是 mixed（14 增、2 减），且面板只有三个 source
scales。因此不能从单一谱标量推出 limiting profile、uniform theorem 或
arithmetic cancellation。

开放定理：uniform spectral-profile law、trace/source normalization 的 arithmetic
接口、signed prime-shell reassembly、fixed-power credit、full Gate B 与
twin-prime conclusion 仍 OPEN/NONE。Session-named evaluator files absent，
故不宣称 official Route-A/Route-B pass。

可复用结构：

    literal matrix -> PSD Gram -> trace-normalized spectral measure
                   -> outward quotient interval -> adversarial control

ROUND2_CLUE：
AUDIT_SPECTRAL_PROFILE_STABILITY_ACROSS_SHELLS_OR_TEST_SIGNED_PROJECTOR_REASSEMBLY_BEFORE_ANY_ARITHMETIC_POWER_CLAIM。

    TPC320_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_TRACE_NORMALIZED_SPECTRAL_CONCENTRATION_AUDIT
    TPC320_ROUTE_ADVANCE = YES_SCOPED_SCALE_INVARIANT_SPECTRAL_READOUT
    TPC320_CONCENTRATION_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_ROWS_5_K
    TPC320_CONCENTRATION_DECREASES = NUMERICALLY_CERTIFIED_FINITE_80_OF_80
    TPC320_SCALE_INVARIANCE = PROVED_EXACT_FINITE
    TPC320_STABLE_RANK_GROWTH = NUMERICAL_OBSERVATION_FINITE_16_OF_16
    TPC320_PARTICIPATION_GROWTH = NUMERICAL_OBSERVATION_FINITE_16_OF_16
    TPC320_ENTROPY_CONTROL = NUMERICAL_OBSERVATION_MIXED
    TPC320_ARITHMETIC_ADVANCE = NO
    TPC320_FIXED_POWER_CREDIT = 0
    TPC320_FULL_GATE_B = OPEN
    TPC320_TWIN_PRIME_RESULT = NONE
    TPC320_STATUS = NUMERICALLY_CERTIFIED_FINITE_TRACE_NORMALIZED_SPECTRAL_CONCENTRATION_AUDIT

## 0.113 current：TPC-319 Ky Fan cluster masses and normalization firewall

项目：papers/tpc-319-kyfan-cluster-normalization-firewall/

类型：**NUMERICALLY_CERTIFIED_FINITE_KY_FAN_CLUSTER_NORMALIZATION_AUDIT**。

TPC-319 承接 TPC-318 的 clustered-top-eigenvalue 与 normalization open gates，在同一
deleted-diagonal centered prime-shell Gram 上定义 Ky Fan 簇质量
`F_k=sum_{j<=k}lambda_j`，审计 `k={1,2,4,8,16}`。固定
`X=640,1280,2560`、`Q={24,36,54,80}`、`s={1,2}` 的 24 rows，双 shell 顺序、双
solver、残差与有限 Weyl guard 给出 120 个 cluster intervals。80/80 adjacent
normalized `F_k/N` intervals 严格下降，同时 80/80 unnormalized `F_k` intervals 严格
上升。

最强正结果：Ky Fan 量是 rank-k subspace 的 exact variational maximum，因此把单一
eigenvector readout 提升为具有明确几何意义的 spectral cluster；双向趋势在五个 k
层级上都得到 finite interval 支持。

最强 obstruction：source count 每次加倍，且所有未归一化倍率都落在 `(1,2)`；精确
恒等式 `M_k(2N)/M_k(N)=F_k(2N)/(2F_k(N))` 说明 normalized decrease 是
normalization firewall，不是 arithmetic power saving。edge-gap/effective-rank 仍显示
一维 canonical eigenspace 不稳定。该结果是 same-engine finite audit，非 external
physical holdout。

开放定理：scale-invariant spectral measure、uniform cluster normalization law、signed
prime-shell reassembly、fixed-power credit、full Gate B 与 twin-prime conclusion 仍
OPEN/NONE。Session-named evaluator files absent，故不宣称 official Route-A/Route-B pass。

可复用结构：`literal matrix -> PSD Gram -> Ky Fan cluster mass -> dual interval ->
normalization flip -> gap firewall`。

ROUND2_CLUE：`AUDIT_A_SCALE_INVARIANT_SPECTRAL_MEASURE_OR_PROVE_A_SOURCE_NORMALIZATION_LAW_BEFORE_ANY_POWER_CLAIM`。

    TPC319_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_KY_FAN_CLUSTER_NORMALIZATION_AUDIT
    TPC319_ROUTE_ADVANCE = YES_SCOPED_KY_FAN_CLUSTER_AND_NORMALIZATION_FIREWALL
    TPC319_KY_FAN_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_ROWS_5_K
    TPC319_NORMALIZED_DECREASES = NUMERICALLY_CERTIFIED_FINITE_80_OF_80
    TPC319_UNNORMALIZED_INCREASES = NUMERICALLY_CERTIFIED_FINITE_80_OF_80
    TPC319_NORMALIZATION_FLIP = PROVED_EXACT_FINITE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_80
    TPC319_CLUSTER_GAP_CENSUS = NUMERICAL_OBSERVATION_FINITE
    TPC319_EFFECTIVE_RANK = NUMERICAL_OBSERVATION_FINITE
    TPC319_ARITHMETIC_ADVANCE = NO
    TPC319_FIXED_POWER_CREDIT = 0
    TPC319_FULL_GATE_B = OPEN
    TPC319_TWIN_PRIME_RESULT = NONE
    TPC319_STATUS = NUMERICALLY_CERTIFIED_FINITE_KY_FAN_CLUSTER_NORMALIZATION_AUDIT

## 0.112 previous：TPC-318 finite top-eigenvalue prime-shell audit

项目：papers/tpc-318-top-eigenvalue-prime-shell-audit/

类型：**NUMERICALLY_CERTIFIED_FINITE_TOP_EIGENVALUE_AUDIT**。

TPC-318 承接 TPC-317 留下的 true operator-norm open gate，保留同一
deleted-diagonal centered prime-shell operator，直接计算 PSD Gram `G=A^*A` 的最大
特征值，而不再以 trace power 作为代理。在 `X=640,1280,2560`、
`Q={24,36,54,80}`、`s={1,2}` 的 24 rows 上，正向/反向 shell 累加、SciPy 对称
top-two 求解器与 NumPy full `eigvalsh` 均重放；残差与安全 `|K|<=160` 的有限 Weyl
guard 给出 24/24 finite intervals，16/16 相邻 normalized top-eigenvalue intervals
严格分离且下降。

最强正结果：真实 top-eigenvalue readout 在有限面板上比 Schatten-4 envelope 更贴近
目标，并由双 solver、反向 shell 和 a-posteriori residual 三重审计支持。

最强 obstruction：10/24 rows 的相对 top/second gap 小于 `0.01`，最小约
`0.001704`；因此 top eigenspace 可能成簇，且按 source count 归一化的有限下降不能
转化为 unnormalized growing power 或 canonical arithmetic eigenvector。该结果是
same-engine finite numerical audit，不是 external physical holdout。

开放定理：clustered eigenspace 的 uniform stability、normalization-invariant growing
law、prime-shell signed reassembly、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。Session-named evaluator files absent，故不宣称 official
Route-A/Route-B pass。

可复用结构：`literal matrix -> PSD Gram -> dual top spectrum -> residual/Weyl interval
-> normalized trend -> eigenspace-gap firewall`。

ROUND2_CLUE：`AUDIT_THE_TOP_EIGENSPACE_CLUSTER_AND_NORMALIZATION_LAW_BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION`。

    TPC318_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_TOP_EIGENVALUE_AUDIT
    TPC318_ROUTE_ADVANCE = YES_SCOPED_TOP_EIGENVALUE_READOUT
    TPC318_TOP_EIGENVALUE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC318_TOP_EIGENVALUE_DECREASE = NUMERICALLY_CERTIFIED_FINITE_16_OF_16
    TPC318_DUAL_SOLVER_AGREEMENT = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC318_RESIDUAL_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC318_NEAR_DEGENERACY = NUMERICALLY_CERTIFIED_FINITE_CENSUS
    TPC318_NORMALIZED_TREND = NUMERICAL_OBSERVATION_FINITE_ONLY
    TPC318_UNNORMALIZED_POWER = OPEN
    TPC318_CLUSTERED_EIGENSPACE = OPEN
    TPC318_ARITHMETIC_CANCELLATION = OPEN
    TPC318_ARITHMETIC_ADVANCE = NO
    TPC318_FIXED_POWER_CREDIT = 0
    TPC318_FULL_GATE_B = OPEN
    TPC318_TWIN_PRIME_RESULT = NONE
    TPC318_STATUS = NUMERICALLY_CERTIFIED_FINITE_TOP_EIGENVALUE_AUDIT

## 0.111 previous：TPC-317 Schatten-4 finite prime-shell compression

项目：papers/tpc-317-schatten-four-prime-shell-compression/

类型：**NUMERICALLY_CERTIFIED_FINITE_SCHATTEN4_COMPRESSION_AND_OPERATOR_ENVELOPE**。

TPC-317 承接 TPC-316 的 Frobenius/operator-norm 分离，保留同一
deleted-diagonal centered prime-shell source operator，并对其 PSD Gram
`G=A^*A` 使用 trace-power 链
`lambda_max(G) <= sqrt(trace(G^2)) <= trace(G)`。在
`X=640,1280,2560`、`Q={24,36,54,80}`、`s={1,2}` 的 24 个 finite rows 上，
正向与反向 shell 累加分别重放；16 个相邻尺度的 normalized Schatten-4 intervals
全部严格下降，而同一 16 个 normalized Frobenius intervals 全部严格上升。小面板
`I={17,...,32}`, `p=5`, `s=1` 的 `trace(G)` 与 `trace(G^2)` 由 exact rational
arithmetic 锚定。

最强正结果：得到一个严格有限的、比 Frobenius 更紧的 PSD trace-power `L2`
envelope，并以 24-row dual-accumulation certificate、independent replay 与 stress
suite 支持；这是真实的 finite spectral compression，而非把 Frobenius 当作谱范数。

最强 obstruction：大面板的 Schatten-4 结果仍是 declared numerical error model
下的有限证书，尚未给出 true top eigenvalue 或 uniform growing estimate；因此不能
把 16/16 的下降升级为 arithmetic power saving。Frobenius 的 opposite trend 只在
声明面板上 REFUTED_SCOPED 其作为 sharp spectral proxy 的用法。

开放定理：true top-eigenvalue/trace-power growing bound、prime-shell arithmetic
cancellation、canonical normalization、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。该项目沿用同一 locked engine，非 external physical holdout；
Session-named evaluator files absent，故不宣称 official Route-A/Route-B pass。

可复用结构：`literal matrix -> PSD Gram -> trace-power sandwich -> outward finite
interval -> trend firewall`。

ROUND2_CLUE：`AUDIT_THE_TRUE_TOP_EIGENVALUE_OR_A_CERTIFIED_TRACE_POWER_LADDER_BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION`。

    TPC317_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SCHATTEN4_COMPRESSION_AND_OPERATOR_ENVELOPE
    TPC317_ROUTE_ADVANCE = YES_SCOPED_TRACE_POWER_ENVELOPE
    TPC317_SCHATTEN4_IDENTITY = PROVED_EXACT_FINITE
    TPC317_FINITE_L2_ENVELOPE = PROVED_EXACT_FINITE
    TPC317_SMALL_RATIONAL_TRACE_AUDIT = PROVED_EXACT_FINITE
    TPC317_DUAL_PRECISION_ROWS = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC317_SCHATTEN4_DECREASE = NUMERICALLY_CERTIFIED_FINITE_16_OF_16
    TPC317_FROBENIUS_INCREASE = NUMERICALLY_CERTIFIED_FINITE_16_OF_16
    TPC317_FROBENIUS_PROXY = REFUTED_SCOPED_AS_A_SHARP_SPECTRAL_PROXY
    TPC317_TRUE_OPERATOR_NORM = OPEN
    TPC317_ARITHMETIC_CANCELLATION = OPEN
    TPC317_ARITHMETIC_ADVANCE = NO
    TPC317_FIXED_POWER_CREDIT = 0
    TPC317_FULL_GATE_B = OPEN
    TPC317_TWIN_PRIME_RESULT = NONE
    TPC317_STATUS = NUMERICALLY_CERTIFIED_FINITE_SCHATTEN4_COMPRESSION_AND_OPERATOR_ENVELOPE

## 0.110 previous：TPC-316 literal arithmetic L2 fresh-panel envelope

项目：papers/tpc-316-literal-arithmetic-l2-fresh-panel/

类型：**PROVED_EXACT_FINITE_LITERAL_ARITHMETIC_L2_ENVELOPE_PLUS_TWO_SCALE_OBSTRUCTION**。

TPC-316 承接 TPC-315 的 literal arithmetic `L2` open gate，把同一 TPC-268
deleted-diagonal centered prime-shell formula 提升为完整的 source-to-output operator
`A_(Q,s,X): ell^2(I_X)->ell^2(S_Q x I_X)`。在两个 disjoint panels
`I_640={321,...,640}` 与 `I_1280={641,...,1280}` 上，对
`Q={24,36,54,80}`、`s={1,2}` 的 16 个 rows，用 exact signed-difference/residue-count
identity 计算 Hilbert--Schmidt mass，并对每行 5 个坐标列给出 exact lower witnesses。

最强正结果：有限 Frobenius interface
`N^(-1)||A beta||_2^2 <= (||A||_HS^2/N)||beta||_2^2` 的系数由 exact rational
counting identity 给出；16/16 rows、80/80 probes 均由 independent replay 重建。

最强 obstruction：normalized Hilbert--Schmidt upper envelope 从 `X=640` 到
`X=1280` 在 8/8 matched rows 上升，倍率为 1.074367--1.316043；fresh panel 上
Frobenius/probe ratio 为 517.635--581.975。该上升只作 NUMERICAL_OBSERVATION，不能
推出 true operator norm 上升；它仅在声明的两面板范围内 REFUTED_SCOPED 了“HS envelope
是衰减 proxy”的用法。

开放定理：true growing operator-norm estimate、arithmetic cancellation beyond
Frobenius、canonical normalization、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。该项目使用同一锁定 engine，非 external physical holdout；
Session-named evaluator files absent，故不宣称 official pass。

可复用结构：`literal matrix -> signed-difference count -> exact HS envelope ->
coordinate lower witness -> finite sandwich -> growth firewall`。

ROUND2_CLUE：REPLACE_THE_FROBENIUS_ENVELOPE_BY_A_GROWING_OPERATOR_OR_ARITHMETIC_CANCELLATION_ESTIMATE_WITHOUT_IMPORTING_A_POWER_CLAIM。

    TPC316_ROUTE_ADVANCE = YES_SCOPED_LITERAL_FINITE_L2_ENVELOPE
    TPC316_LITERAL_OPERATOR = PROVED_EXACT_FINITE
    TPC316_FROBENIUS_L2_ENVELOPE = PROVED_EXACT_FINITE
    TPC316_DIFFERENCE_RESIDUE_COUNT = PROVED_EXACT_FINITE
    TPC316_COORDINATE_LOWER_WITNESSES = PROVED_EXACT_FINITE_5_PER_ROW
    TPC316_ROWS = NUMERICALLY_CERTIFIED_FINITE_16
    TPC316_PROBES = NUMERICALLY_CERTIFIED_FINITE_80
    TPC316_NORMALIZED_HS_TWO_SCALE_RISE = NUMERICALLY_CERTIFIED_FINITE_8_OF_8
    TPC316_FRESH_PANEL_PROBE_GAP = NUMERICALLY_CERTIFIED_FINITE_8_OF_8_ABOVE_517
    TPC316_HS_DECAY_PROXY = REFUTED_SCOPED_TWO_DECLARED_PANELS
    TPC316_GROWING_ARITHMETIC_L2 = OPEN
    TPC316_TRUE_OPERATOR_NORM_DECAY = OPEN
    TPC316_ARITHMETIC_ADVANCE = NO
    TPC316_FIXED_POWER_CREDIT = 0
    TPC316_FULL_GATE_B = OPEN
    TPC316_TWIN_PRIME_RESULT = NONE
    TPC316_STATUS = PROVED_EXACT_FINITE_LITERAL_ARITHMETIC_L2_ENVELOPE_PLUS_TWO_SCALE_OBSTRUCTION

## 0.109 previous：TPC-315 fresh-source locked-weight holdout

项目：papers/tpc-315-fresh-source-locked-weight-holdout/

类型：**PROVED_EXACT_FINITE_FRESH_SOURCE_LOCKED_WEIGHT_MENU_HOLDOUT_REPLICATION_AND_LAW_ORDER_SHIFT**。

TPC-315 承接 TPC-314 的 fresh-source clue。它先验证并锁定 TPC-314 的三-law menu（counting
`1`、reduced-residue `1/(p-1)`、prime von-Mangoldt `log(p)`），然后把同一 locked literal
engine 移到 fresh source interval `I=(640,1280]`，重新构造 8 个 `(Q,s)` physical Gram rows。
每行都在 exact rational arithmetic 上重新枚举 global-sign classes，得到 fresh Gram minimum
与 all-positive maximum；目标标签不从 TPC-312/TPC-314 继承。三种权的 48 个 finite cases
经过 `10^-36` directed outward interval replay，24/24 fresh minima 严格低于 1，24/24
all-positive controls 严格高于 1。

最强正结果：menu 在 fresh target readout 前锁定后，粗粒度 separation class 在 8/8 rows
复现；producer、independent checker 与 stress suite 的 normal/optimized Bridge-B 检查均通过。

最强 obstruction：幅度的 law ordering 仍不稳定。minimum order 有三种 strict types：
`VON_MANGOLDT<COUNTING<REDUCED_RESIDUE` 六行、`REDUCED_RESIDUE<COUNTING<VON_MANGOLDT`
一行、`COUNTING<VON_MANGOLDT<REDUCED_RESIDUE` 一行；positive order 有两种：
`REDUCED_RESIDUE<COUNTING<VON_MANGOLDT` 六行、`VON_MANGOLDT<REDUCED_RESIDUE<COUNTING`
两行。因此 fresh class replication 不能识别 canonical amplitude law。

开放定理：literal arithmetic `L2` interface on the fresh panel；uniform growing weighted
theorem、external physical independence、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。该 holdout 使用同一 engine，且 fresh minimum 仍是 Gram-dependent
target，故不作外部统计独立或 predictive validation 声明。

可复用结构：`pre-target menu lock -> fresh rational Gram -> exhaustive sign extrema ->
rational/log interval -> class/order firewall`。

ROUND2_CLUE：PROBE_LITERAL_ARITHMETIC_L2_INTERFACE_ON_THE_FRESH_PANEL_BEFORE_ANY_GROWING_CLAIM。

    TPC315_ROUTE_ADVANCE = YES_SCOPED_FRESH_SOURCE_CLASS_REPLICATION_AND_ORDER_OBSTRUCTION
    TPC315_FRESH_SOURCE_TARGET_RECOMPUTATION = PROVED_EXACT_FINITE_8_ROWS
    TPC315_LOCKED_WEIGHT_MENU = PROVED_EXACT_FINITE_PRE_TARGET
    TPC315_MINIMUM_BELOW_ONE = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC315_POSITIVE_ABOVE_ONE = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC315_HOLDOUT_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_8_OF_8
    TPC315_MINIMUM_LAW_ORDER_SHIFT = NUMERICALLY_CERTIFIED_FINITE_3_TYPES
    TPC315_POSITIVE_LAW_ORDER_SHIFT = NUMERICALLY_CERTIFIED_FINITE_2_TYPES
    TPC315_EXTERNAL_INDEPENDENCE = NONE_SAME_LOCKED_ENGINE
    TPC315_TARGET_GENERATION_LEAKAGE = FRESH_SOURCE_GRAM_DEPENDENT_LABELS
    TPC315_CANONICAL_WEIGHTING = OPEN
    TPC315_FRESH_PHYSICAL_HOLDOUT = NONE_SAME_LOCKED_ENGINE
    TPC315_UNIFORM_GROWING_WEIGHTED_THEOREM = OPEN
    TPC315_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC315_FIXED_POWER_CREDIT = 0
    TPC315_FULL_GATE_B = OPEN
    TPC315_TWIN_PRIME_RESULT = NONE
    TPC315_STATUS = PROVED_EXACT_FINITE_FRESH_SOURCE_LOCKED_WEIGHT_MENU_HOLDOUT_REPLICATION_AND_LAW_ORDER_SHIFT
    TPC315_STRONGEST_POSITIVE = FRESH_8_OF_8_CLASS_REPLICATION_WITH_48_EXACT_INTERVAL_CASES
    TPC315_STRONGEST_OBSTRUCTION = FRESH_LAW_ORDER_IS_NOT_STABLE_OR_CANONICAL
    TPC315_OPEN_THEOREM = LITERAL_ARITHMETIC_L2_BOUND_FOR_THE_FRESH_PHYSICAL_PANEL
    TPC315_REUSABLE_STRUCTURE = PRE_TARGET_MENU_LOCK_PLUS_FRESH_GRAM_EXTREMUM_AND_OUTWARD_LAW_AUDIT
    TPC315_ROUND2_CLUE = PROBE_LITERAL_ARITHMETIC_L2_INTERFACE_ON_THE_FRESH_PANEL_BEFORE_ANY_GROWING_CLAIM

## 0.108 previous：TPC-314 externally motivated weight-law audit

项目：papers/tpc-314-canonical-weight-law-audit/

类型：**PROVED_EXACT_FINITE_EXTERNALLY_MOTIVATED_WEIGHT_LAW_ENCLOSURE_AND_NEW_PANEL_ROBUSTNESS_AUDIT**。

TPC-314 承接 TPC-313 的 weighting-law open gate，冻结 TPC-312 的 8 个 source-shell rows，
在同一 I=(320,640]、H=66、Q={24,36,54,80}、exponent {1,2} 面板上固定审计三种
正权：counting 1、reduced-residue 1/(p-1) 与 prime von-Mangoldt log(p)。前两种
权为 rational；log(p) 用 120 项 range-reduced atanh 正项级数与显式 geometric tail
做 rational enclosure，随后所有 weighted numerator/denominator/ratio 在 10^-36 grid
上 outward-rounding。共 48 个 target/law cases，24/24 Gram-minimum intervals 严格低于
1，24/24 all-positive control intervals 严格高于 1。

最强正结果：三种 externally motivated candidate laws 在这组 finite panel 上都保留
minimum-versus-positive separation，且 logarithmic law 有独立 exact interval replay。

最强 obstruction：幅度不是 law-invariant；minimum law order 在 8 行中有 1 个
counting < log < reduced-residue crossover，positive control 有 4 种 strict order
types。因此有限 class robustness 不能选择 canonical weighting，也不能支持“最方便的
权重就是正确权重”。

开放定理：把相同 weight menu 在 fresh source interval 上先锁定，再重算 physical targets
并检验 holdout；uniform growing weighted theorem、arithmetic L2、fixed-power credit、
full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

可复用结构：frozen physical Gram -> declared positive laws -> rational/log interval ->
weighted ratio -> class/order firewall。

ROUND2_CLUE：REPLICATE_THE_LOCKED_WEIGHT_LAW_MENU_ON_A_FRESH_SOURCE_INTERVAL_WITH_WEIGHTS_FIXED_BEFORE_TARGET_RECOMPUTATION。

    TPC314_ROUTE_ADVANCE = YES_SCOPED_FINITE_WEIGHT_CLASS_ROBUSTNESS
    TPC314_WEIGHTED_GRAM_IDENTITY = PROVED_EXACT_FINITE
    TPC314_LOG_ATANH_ENCLOSURE = PROVED_EXACT_FINITE_120_TERMS
    TPC314_DIRECTED_INTERVAL_PROPAGATION = PROVED_EXACT_FINITE_GRID_1E_MINUS_36
    TPC314_MINIMUM_BELOW_ONE = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC314_POSITIVE_ABOVE_ONE = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
    TPC314_MINIMUM_ORDER = NUMERICALLY_CERTIFIED_FINITE_7_OF_8_LOG_LT_COUNT_LT_RECIP_ONE_CROSSOVER
    TPC314_POSITIVE_ORDER = NUMERICALLY_CERTIFIED_FINITE_8_OF_8_FOUR_ORDER_TYPES
    TPC314_EXTERNAL_INDEPENDENCE = NONE_SAME_LOCKED_ENGINE
    TPC314_TARGET_GENERATION_LEAKAGE = INHERITED_TPC312_SOURCE_FIRST_GRAM_LABEL
    TPC314_CANONICAL_WEIGHTING = OPEN
    TPC314_FRESH_PHYSICAL_HOLDOUT = OPEN
    TPC314_UNIFORM_GROWING_WEIGHTED_THEOREM = OPEN
    TPC314_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC314_FIXED_POWER_CREDIT = 0
    TPC314_FULL_GATE_B = OPEN
    TPC314_TWIN_PRIME_RESULT = NONE
    TPC314_STATUS = PROVED_EXACT_FINITE_EXTERNALLY_MOTIVATED_WEIGHT_LAW_ENCLOSURE_AND_NEW_PANEL_ROBUSTNESS_AUDIT
    TPC314_ROUND2_CLUE = REPLICATE_THE_LOCKED_WEIGHT_LAW_MENU_ON_A_FRESH_SOURCE_INTERVAL_WITH_WEIGHTS_FIXED_BEFORE_TARGET_RECOMPUTATION

## 0.107 previous：TPC-313 outward-rounded profile-budget interval certificate

项目：`papers/tpc-313-outward-budget-interval-certificate/`

类型：**PROVED_EXACT_FINITE_PROFILE_PREFIX_FEASIBILITY_AND_OUTWARD_INTERVAL_BUDGET_CERTIFICATES_PLUS_NUMERICALLY_CERTIFIED_NEW_PANEL_SEPARATION**。

TPC-313 承接 TPC-312 的 new source-shell atlas，在相同锁定 literal engine 的
`I=(320,640]`、`H=66`、`Q={24,36,54,80}`、exponent `{1,2}` 上构造 17-column source
profile image。对每个 row，先用 exact least-squares scan 找到 weighted Gram-minimum
target 的 first-feasible prefix `k*`（归一化残差 `tau=1/2`），再在同一 `k*` 上同时审计
minimum target 与 all-positive control。16 个 rational ridge systems 都给出可行 primal
upper witness 与 weak-dual lower witness；每个 residual、objective、dual、ratio 与 gap
都经过 `10^-36` decimal grid 的 outward endpoint propagation，并由 independent checker
逐项重放。

最强正结果：8/8 weighted dual budget ratios 的 outward lower bound 严格高于 `5e-5`，
8/8 all-positive primal budget ratios 的 outward upper bound 严格低于 `1e-5`，且两者
使用同一个 common prefix。first-feasible prefix 的 `k*` 依次为
`6,4,7,7,12,8,13,12`（按 `Q=24,36,54,80`、exponent `1,2` 排列）。

最强 obstruction：这仍是 source-first finite diagnostic；weighted label 来自正在诊断
的 physical Gram，profile ladder、`tau`、ridge seeds 与 common-prefix rule 也是
modeling choices。新证书没有创造 external independence、canonical weighting、uniform
growing budget 或 arithmetic `L2`。

开放定理：在不使用 target-Gram 选择的前提下，固定一个外部可辩护的 weighting law，
并在 genuinely fresh physical source interval 上完成 holdout replication 与 growing
budget control；fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

可复用结构：`source profile -> exact image/Gram -> first feasible prefix -> rational
primal/dual pair -> outward interval -> threshold firewall`。

ROUND2_CLUE：`AUDIT_EXTERNALLY_JUSTIFIED_WEIGHTING_ON_A_FRESH_PHYSICAL_HOLDOUT_AFTER_FORMAL_BUDGET_CERTIFICATION`。

```text
TPC313_ROUTE_ADVANCE = YES_SCOPED_OUTWARD_PROFILE_BUDGET_CERTIFICATE
TPC313_PROFILE_PREFIX_FEASIBILITY = PROVED_EXACT_FINITE_8_OF_8
TPC313_RATIONAL_PRIMAL_WITNESSES = PROVED_EXACT_FINITE_16_OF_16
TPC313_RATIONAL_DUAL_LOWER_BOUNDS = PROVED_EXACT_FINITE_16_OF_16
TPC313_OUTWARD_GRID_ENCLOSURES = PROVED_EXACT_FINITE_16_OF_16_GRID_1E_MINUS_36
TPC313_WEIGHTED_LOWER_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_8_OF_8_ABOVE_5E_MINUS_5
TPC313_POSITIVE_UPPER_SEPARATION = NUMERICALLY_CERTIFIED_FINITE_8_OF_8_BELOW_1E_MINUS_5
TPC313_EXTERNAL_INDEPENDENCE = NONE_SAME_LOCKED_ENGINE
TPC313_TARGET_GENERATION_LEAKAGE = INHERITED_TPC312_SOURCE_FIRST_GRAM_LABEL
TPC313_EXTERNAL_WEIGHTING = OPEN
TPC313_FRESH_PHYSICAL_HOLDOUT = OPEN
TPC313_UNIFORM_GROWING_BUDGET = OPEN
TPC313_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC313_FIXED_POWER_CREDIT = 0
TPC313_FULL_GATE_B = OPEN
TPC313_TWIN_PRIME_RESULT = NONE
TPC313_STATUS = PROVED_EXACT_FINITE_PROFILE_PREFIX_FEASIBILITY_AND_OUTWARD_INTERVAL_BUDGET_CERTIFICATES_PLUS_NUMERICALLY_CERTIFIED_NEW_PANEL_SEPARATION
TPC313_ROUND2_CLUE = AUDIT_EXTERNALLY_JUSTIFIED_WEIGHTING_ON_A_FRESH_PHYSICAL_HOLDOUT_AFTER_FORMAL_BUDGET_CERTIFICATION
```

## 0.106 previous：TPC-312 new source-shell Gram and sign-separation atlas

项目：`papers/tpc-312-new-source-shell-separation-atlas/`

类型：**PROVED_EXACT_FINITE_NEW_SOURCE_SHELL_GRAM_AND_SIGN_SEPARATION_ATLAS**。

TPC-312 按 TPC-311 的 route clue 把物理计算移到新 source-shell panel：同一锁定 literal
engine 上使用 `I=(320,640]`、`H=66`、`Q={24,36,54,80}` 与 exponent `{1,2}`，共 8 个
此前未用过的 source/parameter rows。每行的物理输出、Gram entries 与 sign energies 都
在 `Fraction` 上计算；固定首个 sign 为 `+1` 后，完整 Gray enumeration 共覆盖
`2(2^5+2^8+2^11+2^14)=37,440` 个 global-sign classes，shell targets 共 84 个。

最强正结果：8/8 Gram 在 `1000000007` 下得到 full modular rank，8/8 行的 exact sign
minimum `<1`、all-positive maximum `>1`，且对每个 exponent minimum 沿
`Q=24,36,54,80` 严格下降、positive maximum 严格上升；exponent 2 在每个 Q 上进一步
扩大这两个方向的分离。

最强 obstruction：这些 sign labels 仍由正在诊断的 physical Gram source-first 生成，
所以“新”不是 external independent holdout，也不能提供 canonical weighting。profile
budget 的 outward rounding、uniform growing theorem、arithmetic `L2`、fixed-power credit、
full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。这里的有限 order 只对锁定的 8 行
负责，不能外推到 growing shell。

开放定理：在这组 exact physical rows 上完成 outward-rounded profile-budget certificate，
并在不偷换 source-first labels 的前提下测试 externally justified weighting law 与真正
独立的 physical holdout。

可复用结构：`literal physical operator -> rational Gram/PSD -> global-sign quotient ->
exact finite sign atlas -> explicit freshness/leakage firewall`。

ROUND2_CLUE：`CERTIFY_NEW_PANEL_PROFILE_BUDGETS_WITH_OUTWARD_ROUNDING_BEFORE_ANY_HOLDOUT_PREFERENCE_CLAIM`。

```text
TPC312_ROUTE_ADVANCE = YES_SCOPED_NEW_SOURCE_SHELL_ATLAS
TPC312_NEW_SOURCE_SHELL_ROWS = PROVED_EXACT_FINITE_8_ROWS
TPC312_PHYSICAL_GRAM_PSD = PROVED_EXACT_FINITE
TPC312_RATIONAL_FULL_RANK = PROVED_EXACT_FINITE_8_OF_8
TPC312_SIGN_EXTREMA = PROVED_EXACT_FINITE_37440_CLASSES
TPC312_STRICT_SIGN_SEPARATION = PROVED_EXACT_FINITE_8_OF_8
TPC312_Q_SPINE_ORDERING = PROVED_EXACT_FINITE_4_Q_BY_2_EXPONENTS
TPC312_FRESHNESS = NEW_SOURCE_SHELL_ROWS_WITHIN_SAME_LOCKED_ENGINE
TPC312_EXTERNAL_INDEPENDENCE = NONE
TPC312_PROFILE_BUDGET_INTERVAL_CERTIFICATE = OPEN
TPC312_EXTERNAL_WEIGHT_JUSTIFICATION = OPEN
TPC312_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC312_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC312_FIXED_POWER_CREDIT = 0
TPC312_FULL_GATE_B = OPEN
TPC312_TWIN_PRIME_RESULT = NONE
TPC312_STATUS = PROVED_EXACT_FINITE_NEW_SOURCE_SHELL_GRAM_AND_SIGN_SEPARATION_ATLAS
TPC312_ROUND2_CLUE = CERTIFY_NEW_PANEL_PROFILE_BUDGETS_WITH_OUTWARD_ROUNDING_BEFORE_ANY_HOLDOUT_PREFERENCE_CLAIM
```


## 0.105 current：TPC-311 declared stratification and tau-slice holdout replication

项目：`papers/tpc-311-stratified-tau-holdout-replication/`

类型：**PROVED_EXACT_FINITE_STRATIFIED_HOLDOUT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_TAU_SLICE_NONREPLICATION_ATLAS**。

TPC-311 承接 TPC-310 的 aggregation-order obstruction，固定一个明确的两阶段规则：先在
每个 `(transition, exponent, tau, radius)` design cell 内 pool `LOW/BASE/HIGH` 三个
profile ladders 的 completion extrema，再对 design cells 等权做 arithmetic interval map。
完整 factorial 有 `3x2x3x3=54` 个 profile-pooled strata、162 个 parent observations。
calibration 使用 `tau={0.25,0.5}`，confirmation 使用不相交的 `tau={0.75}`；native
`r=0` 为主结果，`r=1,2` 为压力控制。

native calibration 区间为 `[4.0615814676,4.0617439341]`、class `LEFT`，native
confirmation 区间为 `[0.6818442327,0.6818715070]`、class `RIGHT`，所以固定规则在该
finite parameter-slice 上发生 strict reversal。加入全部 radii 后 calibration 仍 `LEFT`，
confirmation 为 `[0.3840496869,2.9038163322]`、`UNRESOLVED`。删除 BASE 会把 native
calibration 改为 `RIGHT`，exponent 1 与 2 也给出不同 calibration class。

最强正结果：54-cell 两阶段 protocol、独立 profile extrema 与 equal-stratum interval
map 有 exact finite proof，并由独立 replay 锁定 54 strata、6 blocks 与 22 sensitivity
blocks。

最强 obstruction：即使把 weighting rule 明确固定，native calibration 的 `LEFT` 仍不在
held-out `tau=.75` slice 复现；all-radius stress 进一步扩大为 unresolved。

开放定理：外部可辩护的 weighting law 与 genuinely fresh physical holdout 上的稳定
profile/exponent/transition/tolerance preference；directed rounding、causal identification、
uniform asymptotic budget、arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。本文的 child protocol 不是 externally timestamped preregistration，
confirmation 也不是新物理数据。

可复用结构：`profile-pooled design cell -> equal-cell interval map -> disjoint parameter
slice -> replication classification`。

ROUND2_CLUE：`REQUIRE_FRESH_SOURCE_HOLDOUT_AND_EXTERNALLY_JUSTIFIED_WEIGHT_LAW_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM`。

```text
TPC311_ROUTE_ADVANCE = YES_SCOPED_TAU_SLICE_HOLDOUT_OBSTRUCTION
TPC311_STRATIFIED_PROTOCOL = PROVED_EXACT_FINITE
TPC311_PROFILE_POOL_EXTREMA = PROVED_EXACT_FINITE
TPC311_EQUAL_STRATUM_INTERVAL_MAP = PROVED_EXACT_FINITE
TPC311_TAU_PARTITION = PROVED_EXACT_FINITE
TPC311_STRATIFIED_ATLAS = NUMERICALLY_REPRODUCED_FINITE_54_STRATA_6_BLOCKS_22_SENSITIVITY_BLOCKS
TPC311_NATIVE_TAU_REPLICATION = REFUTED_FINITE_STRICT_CALIBRATION_LEFT_CONFIRMATION_RIGHT
TPC311_ALL_RADII_TAU_REPLICATION = REFUTED_FINITE_CALIBRATION_LEFT_CONFIRMATION_UNRESOLVED
TPC311_PROFILE_ROBUSTNESS = REFUTED_FINITE_BASE_OMISSION_CHANGES_NATIVE_CALIBRATION_CLASS
TPC311_EXPONENT_ROBUSTNESS = REFUTED_FINITE_NATIVE_CALIBRATION_EXPONENT_1_LEFT_EXPONENT_2_RIGHT
TPC311_REGISTRATION_STATUS = DECLARED_CHILD_PROTOCOL_NOT_EXTERNALLY_TIMESTAMPED_PREREGISTRATION
TPC311_FRESH_PHYSICAL_HOLDOUT = NONE_SAME_LOCKED_PARENT_ATLAS
TPC311_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS
TPC311_CAUSAL_IDENTIFICATION = NONE_PARAMETER_SLICE_DIAGNOSTIC_ONLY
TPC311_FORMAL_INTERVAL_CERTIFICATE = OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING
TPC311_EXTERNAL_WEIGHT_JUSTIFICATION = OPEN
TPC311_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC311_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC311_FIXED_POWER_CREDIT = 0
TPC311_FULL_GATE_B = OPEN
TPC311_TWIN_PRIME_RESULT = NONE
TPC311_STATUS = PROVED_EXACT_FINITE_STRATIFIED_HOLDOUT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_TAU_SLICE_NONREPLICATION_ATLAS
TPC311_ROUND2_CLUE = REQUIRE_FRESH_SOURCE_HOLDOUT_AND_EXTERNALLY_JUSTIFIED_WEIGHT_LAW_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM
```

## 0.104 previous：TPC-310 cross-holdout aggregation order

项目：`papers/tpc-310-cross-holdout-aggregation-order/`

类型：**PROVED_EXACT_FINITE_CROSS_HOLDOUT_AGGREGATION_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_AGGREGATION_ORDER_OBSTRUCTION_ATLAS**。

TPC-310 冻结 TPC-309 的 profile/completion atlas，不再选择单一 ladder，而是枚举
`LOW/BASE/HIGH` 的全部 7 个非空 profile subsets 与 `{0,1,2}` 的全部 7 个非空
radius subsets，形成 49 个 selectors。对每个 selector 同时计算 pooled MSE、equal-case
arithmetic ratio 与 geometric ratio 三种正区间聚合，共 147 个 aggregate rows。

全 selector（3 ladders、3 radii）上，pooled 区间为
`[0.2423655855,0.3112477031]`、class `RIGHT`；balanced 区间为
`[5.2417686281,14.4871333704]`、class `LEFT`；geometric 区间为
`[0.1993188213,0.8609189559]`、class `RIGHT`。全 49-selector class census 为
pooled `42/1/6`、balanced `1/32/16`、geometric `26/0/23`（顺序均为
right/left/unresolved）。因此 pooled 与 equal-case arithmetic 在 29 个 selectors 上
发生 `RIGHT/LEFT` strict reversal；这不是阈值边界噪声，而是 denominator-weighted 与
equal-case aggregation 的结构差异。

最强正结果：selector lattice、独立 completion extrema、positive interval maps 与
`sum a_i/sum b_i` 的 denominator-weighted mean identity 均有 exact finite proof，且
147 rows 有独立 replay。

最强 obstruction：声明的三种 aggregation maps 没有共同的 finite strict class；在未
预注册 weighting/stratification law 前，不能把 pooled 的 `RIGHT` 解读为 profile-
independent preference。

开放定理：是否存在独立算术依据、预先固定且可跨 holdout 复现的 weighting/stratification
law；formal directed rounding、causal identification、uniform asymptotic budget、
arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

可复用结构：`parent interval atlas -> nonempty selector lattice -> pooled/balanced/geometric
maps -> weighted-mean identity -> class/reversal census`。

ROUND2_CLUE：`TEST_PREREGISTERED_STRATIFIED_WEIGHTS_AND_HOLDOUT_REPLICATION_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM`。

```text
TPC310_ROUTE_ADVANCE = YES_SCOPED_AGGREGATION_ORDER_OBSTRUCTION
TPC310_SELECTOR_PROTOCOL = PROVED_EXACT_FINITE
TPC310_POOLED_EXTREMA = PROVED_EXACT_FINITE
TPC310_POSITIVE_INTERVAL_MAPS = PROVED_EXACT_FINITE
TPC310_WEIGHTED_MEAN_IDENTITY = PROVED_EXACT_FINITE
TPC310_AGGREGATION_ATLAS = NUMERICALLY_REPRODUCED_FINITE_49_SELECTORS_147_AGGREGATES
TPC310_FULL_SELECTOR_REVERSAL = NUMERICALLY_REPRODUCED_FINITE_POOLED_RIGHT_BALANCED_LEFT_GEOMETRIC_RIGHT
TPC310_PROFILE_ROBUSTNESS = REFUTED_FINITE_NO_UNIVERSAL_AGGREGATION_CLASS
TPC310_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS
TPC310_CAUSAL_IDENTIFICATION = NONE_AGGREGATION_DIAGNOSTIC_ONLY
TPC310_FORMAL_INTERVAL_CERTIFICATE = OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING
TPC310_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC310_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC310_FIXED_POWER_CREDIT = 0
TPC310_FULL_GATE_B = OPEN
TPC310_TWIN_PRIME_RESULT = NONE
TPC310_STATUS = PROVED_EXACT_FINITE_CROSS_HOLDOUT_AGGREGATION_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_AGGREGATION_ORDER_OBSTRUCTION_ATLAS
TPC310_ROUND2_CLUE = TEST_PREREGISTERED_STRATIFIED_WEIGHTS_AND_HOLDOUT_REPLICATION_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM
```

## 0.103 previous：TPC-309 profile-prefix shift sensitivity

项目：`papers/tpc-309-profile-prefix-shift-sensitivity/`

类型：**PROVED_EXACT_FINITE_PROFILE_LADDER_SHIFT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_PROFILE_SENSITIVITY_ATLAS**。

TPC-309 承接 TPC-308 的 common-ambient holdout 与 Hamming completion envelope。它在一个
19-prime cutoff pool 中取相邻的三个 17-cutoff windows：`LOW/BASE/HIGH`；shell、labels、
alignment、union/overlap/exclusive partition 与 completion radii 冻结，但每个 profile ladder
重新求 feasible common prefix、frontier、source-budget ratio 与 holdout envelope。

三窗口共 54 profile cases、162 envelope observations，候选数跨 ladder 为 `108/558/1440`
(radii `0/1/2`)。BASE 在三个半径上恢复 TPC-308 的 `13/3/2`、`11/2/5`、`10/1/7`。
LOW 的 agreement 为 `13/4/1`、`10/2/6`、`8/1/9`，HIGH 为 `10/5/3`、`5/0/13`、
`5/0/13`。radius-zero strict discordance 在 LOW/BASE/HIGH 的 transition counts 分别为
`(2,1,1)`、`(0,0,3)`、`(2,2,1)`；radius-two 为 `(1,0,0)`、`(0,0,1)`、`(0,0,0)`。
因此 BASE 的 final-transition obstruction 在声明的相邻 profile shifts 下不具位置或
持续性不变性；这是 finite model-selection obstruction，不是 profile-independent theorem。

最强正结果：同维度、source-backed、相邻的 profile perturbation 协议有 exact finite
定义、独立 NumPy replay、exact stress suite 与 PDF/Bridge-B release。

最强 obstruction：改变 profile ladder 会迁移 strict discordance，并在较宽 completion
envelope 下显著扩大 unresolved band；不能从 BASE 选择推出 profile-independent preference。

开放定理：是否存在有独立算术依据的 profile-selection law，使 holdout preference 在
growing regime 中稳定；formal directed-rounding enclosure、causal identification、uniform
asymptotic budget、arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion
仍 OPEN/NONE。

可复用结构：`source-backed cutoff windows -> common-prefix frontier -> budget/holdout
interval -> Hamming completion envelope -> discordance-location census`。

ROUND2_CLUE：`TEST_CROSS_HOLDOUT_AGGREGATION_AND_PROFILE_ROBUSTNESS_BEFORE_ANY_PREFERENCE_CLAIM`。

```text
TPC309_ROUTE_ADVANCE = YES_SCOPED_PROFILE_SENSITIVITY_OBSTRUCTION
TPC309_WINDOW_PROTOCOL = PROVED_EXACT_FINITE
TPC309_PREFIX_NESTING = PROVED_EXACT_FINITE
TPC309_HAMMING_EXTREMA = PROVED_EXACT_FINITE
TPC309_NORMALIZER_INVARIANCE = PROVED_EXACT_FINITE
TPC309_PROFILE_ATLAS = NUMERICALLY_REPRODUCED_FINITE_54_PROFILE_CASES_162_ENVELOPES
TPC309_BASELINE_RECOVERY = NUMERICALLY_REPRODUCED_FINITE_TPC308_CLASSES
TPC309_PROFILE_ROBUSTNESS = OPEN_PROFILE_INDEPENDENT_PREFERENCE
TPC309_CAUSAL_IDENTIFICATION = NONE_PROFILE_SENSITIVITY_DIAGNOSTIC_ONLY
TPC309_FORMAL_INTERVAL_CERTIFICATE = OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING
TPC309_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC309_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC309_FIXED_POWER_CREDIT = 0
TPC309_FULL_GATE_B = OPEN
TPC309_TWIN_PRIME_RESULT = NONE
TPC309_STATUS = PROVED_EXACT_FINITE_PROFILE_LADDER_SHIFT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_PROFILE_SENSITIVITY_ATLAS
TPC309_ROUND2_CLUE = TEST_CROSS_HOLDOUT_AGGREGATION_AND_PROFILE_ROBUSTNESS_BEFORE_ANY_PREFERENCE_CLAIM
```

## 0.102 previous：TPC-308 adversarial exclusive-completion envelope

项目：`papers/tpc-308-adversarial-exclusive-completion-envelope/`

类型：**PROVED_EXACT_FINITE_HAMMING_COMPLETION_ENVELOPE_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_HOLDOUT_STABILITY_ATLAS**。

TPC-308 承接 TPC-307 的 common-ambient directional holdout。它冻结 overlap fit、common
ambient operator、coefficients、selected profile prefix 与 budget preference，只对每个
exclusive holdout 的 binary labels 做 Hamming 半径 `r=0,1,2` 的 exhaustive completion
enumeration。Hamming-ball protocol、candidate-count formula、fixed-prediction extrema、
radius monotonicity、radius-zero recovery 与 global-sign invariance 为 exact finite。

锁定 TPC-307 的 18 个 parent cells 后，得到 54 个 envelope observations 与候选总数
`36/186/480`。agreement census（concordant/discordant/unresolved）为 `13/3/2`、
`11/2/5`、`10/1/7`，随半径呈 `3->2->1` 的 discordance attenuation；所有残留
discordance 仍在 `Q=70->90`、exponent 1，且 radius-two 尚有一个。与此同时 unresolved
cells 增至 7，说明宽 envelope 会跨越 strict threshold band。producer 与独立 NumPy
replay 一致，但这是 padded float replay，不是 directed-rounding formal certificate。

最强正结果：把“completion sensitivity”变成可证明、可枚举、可独立复核的有限对象。

最强 obstruction：final transition 的 discordance 在 radius two 仍未完全消失；但其
强度随 envelope 变宽而衰减，不能宣称 completion-invariant preference。

开放定理：在保留 completion envelope 控制的同时，检验 surviving cells 对 profile-prefix
perturbation 是否稳定；formal directed-rounding enclosure、completion generation/causal
identification、uniform asymptotic budget、arithmetic `L2`、fixed-power credit、full Gate B
与 twin-prime conclusion 仍 OPEN/NONE。

可复用结构：`frozen overlap fit -> binary Hamming balls -> exact finite extrema ->
conservative ratio interval -> radius stability census`。

ROUND2_CLUE：`TEST_PROFILE_PREFIX_PERTURBATION_AND_COMPLETION_INVARIANCE_ON_THE_SURVIVING_DISCORDANCE_CELLS_BEFORE_ANY_PREFERENCE_CLAIM`。

```text
TPC308_ROUTE_ADVANCE = YES_SCOPED_ADVERSARIAL_EXCLUSIVE_COMPLETION_ENVELOPE_AUDIT
TPC308_HAMMING_ENVELOPE_PROTOCOL = PROVED_EXACT_FINITE
TPC308_FIXED_PREDICTION_EXTREMA = PROVED_EXACT_FINITE
TPC308_RADIUS_MONOTONICITY = PROVED_EXACT_FINITE
TPC308_RADIUS_ZERO_RECOVERY = PROVED_EXACT_FINITE
TPC308_FINITE_STABILITY_ATLAS = NUMERICALLY_REPRODUCED_FINITE_54_ENVELOPE_OBSERVATIONS
TPC308_AGREEMENT_R0 = NUMERICALLY_REPRODUCED_FINITE_13_CONCORDANT_3_DISCORDANT_2_UNRESOLVED
TPC308_AGREEMENT_R1 = NUMERICALLY_REPRODUCED_FINITE_11_CONCORDANT_2_DISCORDANT_5_UNRESOLVED
TPC308_AGREEMENT_R2 = NUMERICALLY_REPRODUCED_FINITE_10_CONCORDANT_1_DISCORDANT_7_UNRESOLVED
TPC308_DISCORDANCE_SURVIVAL = NUMERICALLY_REPRODUCED_FINITE_3_TO_2_TO_1_AS_RADIUS_0_TO_2
TPC308_DISCORDANCE_LOCALIZATION = NUMERICALLY_REPRODUCED_FINITE_FINAL_PAIR_70_TO_90_ONLY
TPC308_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS
TPC308_CAUSAL_IDENTIFICATION = NONE_FIXED_PREDICTION_ENVELOPE_DIAGNOSTIC_ONLY
TPC308_FORMAL_INTERVAL_CERTIFICATE = OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING
TPC308_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC308_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC308_FIXED_POWER_CREDIT = 0
TPC308_FULL_GATE_B = OPEN
TPC308_TWIN_PRIME_RESULT = NONE
TPC308_STATUS = PROVED_EXACT_FINITE_HAMMING_COMPLETION_ENVELOPE_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_HOLDOUT_STABILITY_ATLAS
TPC308_ROUND2_CLUE = TEST_PROFILE_PREFIX_PERTURBATION_AND_COMPLETION_INVARIANCE_ON_THE_SURVIVING_DISCORDANCE_CELLS_BEFORE_ANY_PREFERENCE_CLAIM
```

## 0.101 previous：TPC-307 common-ambient union-shell holdout

项目：`papers/tpc-307-common-ambient-union-shell-holdout/`

类型：**PROVED_EXACT_FINITE_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_BUDGET_HOLDOUT_DISCORDANCE_ATLAS**。

TPC-307 承接 TPC-306 的 two-way operator/target interaction diagnostic。对每个相邻
`Q` pair 构造一个共同 ambient union `U`，并分解为 overlap `O` 与 exclusive pieces
`E_left,E_right`。两种 aligned directional target 只在 `O` 上进入 constrained profile
frontier；系数选定后，分别在自己的 exclusive piece 上作 withheld holdout。这样得到
一个可审计的有限 holdout protocol，而不是把 overlap 上可能冲突的两个 label 任意拼成
一个 union target。

协议的 partition、overlap-only separation、global-sign invariance 与 common-prefix
feasibility 为 exact finite。锁定 TPC-302/305/306 的 source、shell、profile 与 kernel
conventions 后，18 个 cases 产生 36 个 directional fits 与 54 个 normalizer rows。
独立 NumPy replay 与 producer 一致：budget/holdout preference 为 `13 concordant`、
`3 discordant`、`2 unresolved`；三处 discordance 全部位于 `Q=70->90`、exponent 1，
恰对应三个 tolerance。由于物理矩阵使用 vectorized float64 重放再做高精度 frontier，
该数值结论标为 `NUMERICALLY_REPRODUCED_FINITE`，不是 directed-rounding formal
certificate。

最强正结果：common-ambient directional holdout 把拟合域和检验域严格分开，并给出可
复现的有限 atlas。

最强 obstruction：即使 ambient operator 已共享，三处 budget orientation 在 exclusive
holdout 上反转，另有两处 holdout unresolved；因此 completion-invariant 或 causal
preference 仍不可宣称。

开放定理：在明确的 alternative off-overlap completion envelopes 与 profile-prefix
perturbations 下检验这三处 discordance 是否保持；formal directed-rounding enclosure、
uniform asymptotic budget、arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。

可复用结构：`U/O/E partition -> overlap constrained frontier -> exclusive holdout ->
ratio classification and discordance localization`。

ROUND2_CLUE：`STRESS_COMMON_AMBIENT_HOLDOUT_AGAINST_EXCLUSIVE_COMPLETION_ENVELOPES_AND_PROFILE_PREFIX_PERTURBATIONS_BEFORE_ANY_CAUSAL_PREFERENCE_CLAIM`。

```text
TPC307_ROUTE_ADVANCE = YES_SCOPED_COMMON_AMBIENT_DIRECTIONAL_HOLDOUT_DIAGNOSTIC
TPC307_COMMON_AMBIENT_UNION = PROVED_EXACT_FINITE
TPC307_OVERLAP_ONLY_FIT = PROVED_EXACT_FINITE
TPC307_EXCLUSIVE_HOLDOUT = PROVED_EXACT_FINITE
TPC307_FINITE_HOLDOUT_ATLAS = NUMERICALLY_REPRODUCED_FINITE_18_CASES_36_DIRECTIONAL_FITS_54_NORMALIZER_ROWS
TPC307_AGREEMENT_CENSUS = NUMERICALLY_REPRODUCED_FINITE_CONCORDANT_13_DISCORDANT_3_UNRESOLVED_2
TPC307_DISCORDANCE_LOCALIZATION = NUMERICALLY_REPRODUCED_FINITE_ALL_3_AT_Q70_TO_90_EXPONENT_1
TPC307_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS
TPC307_CAUSAL_IDENTIFICATION = NONE_DIRECTIONAL_HOLDOUT_DIAGNOSTIC_ONLY
TPC307_FORMAL_INTERVAL_CERTIFICATE = OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING
TPC307_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC307_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC307_FIXED_POWER_CREDIT = 0
TPC307_FULL_GATE_B = OPEN
TPC307_TWIN_PRIME_RESULT = NONE
TPC307_STATUS = PROVED_EXACT_FINITE_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_BUDGET_HOLDOUT_DISCORDANCE_ATLAS
TPC307_ROUND2_CLUE = STRESS_COMMON_AMBIENT_HOLDOUT_AGAINST_EXCLUSIVE_COMPLETION_ENVELOPES_AND_PROFILE_PREFIX_PERTURBATIONS_BEFORE_ANY_CAUSAL_PREFERENCE_CLAIM
```

## 0.100 previous：TPC-306 two-way operator/target interaction

项目：`papers/tpc-306-two-way-operator-target-interaction/`

类型：**PROVED_EXACT_TWO_WAY_LOG_BUDGET_DECOMPOSITION_AND_DOMINANCE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_TARGET_INTERACTION_ATLAS**。

TPC-306 承接 TPC-305 的 fixed-operator transported-label atlas，将四个正 budget cells
组织为 operator-by-target table。对共同 target switch 定义
`d_L=log(B_LR/B_LL)`、`d_R=log(B_RR/B_RL)`，并令
`m=(d_L+d_R)/2`、`i=(d_L-d_R)/2`。严格证明
`d_L=m+i`、`d_R=m-i` 与 `m^2-i^2=d_Ld_R`，从而同号 row effects 等价于
target-main dominance，异号 row effects 等价于 operator-interaction dominance；独立
正 row scaling 不改变这些量。

锁定 TPC-305 的 18 个 cases 后，三种 source normalizer 形成 54 个 derived rows：
target-main dominance 为 `12/18`，operator-interaction dominance 为 `6/18`，无
unresolved。中心 `Q=60->70` 为 `5/6` 对 `1/6`，继承的 same-prefix cases 为
`3/3` target-main。main-dominant rows 的 `|i|/|m|` 全部低于 `0.88`，
interaction-dominant rows 全部高于 `1.2`。

最强正结果：两行 operator 差异被显式分解，且有限 atlas 在中心 transition 给出清晰
的 target-main / interaction separation gap。

最强 obstruction：`6/18` cases 为 interaction-dominant（中心仍有 `1/6`），且
shell-specific off-overlap completion 与不同 physical operator 使该表尚非 common-
ambient causal intervention。

开放定理：构造 common-ambient union-shell completion 与 operator holdout，检验该
interaction gap 是否稳定；uniform asymptotic budget、arithmetic `L2`、fixed-power
credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

可复用结构：`fixed-operator target swap -> four-cell table -> log effects -> exact
main/interaction identity -> finite dominance atlas`。

ROUND2_CLUE：`TEST_COMMON_AMBIENT_UNION_SHELL_COMPLETIONS_AND_INTERACTION_STABILITY_BEFORE_ANY_GROWING_TARGET_PREFERENCE_CLAIM`。

```text
TPC306_ROUTE_ADVANCE = YES_SCOPED_TWO_WAY_INTERACTION_DECOMPOSITION
TPC306_LOG_DECOMPOSITION = PROVED_EXACT_FINITE
TPC306_SQUARED_DOMINANCE_IDENTITY = PROVED_EXACT_FINITE
TPC306_ROW_SCALING_INVARIANCE = PROVED_EXACT_FINITE
TPC306_DECOMPOSITION_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_CASES_54_ROWS
TPC306_TARGET_MAIN_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_12_OF_18
TPC306_INTERACTION_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_6_OF_18
TPC306_MIDDLE_TARGET_MAIN = NUMERICALLY_CERTIFIED_FINITE_5_OF_6
TPC306_MIDDLE_SAME_PREFIX_TARGET_MAIN = NUMERICALLY_CERTIFIED_FINITE_3_OF_3
TPC306_RATIO_GAP = NUMERICALLY_CERTIFIED_FINITE_MAIN_LT_0_88_INTERACTION_GT_1_2
TPC306_CAUSAL_IDENTIFICATION = OPEN_COMMON_AMBIENT_HOLDOUT
TPC306_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC306_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC306_FIXED_POWER_CREDIT = 0
TPC306_FULL_GATE_B = OPEN
TPC306_TWIN_PRIME_RESULT = NONE
TPC306_STATUS = PROVED_EXACT_TWO_WAY_LOG_BUDGET_DECOMPOSITION_AND_DOMINANCE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_TARGET_INTERACTION_ATLAS
TPC306_ROUND2_CLUE = TEST_COMMON_AMBIENT_UNION_SHELL_COMPLETIONS_AND_INTERACTION_STABILITY_BEFORE_ANY_GROWING_TARGET_PREFERENCE_CLAIM
```

## 0.99 previous：TPC-305 counterfactual transported-label native budget

项目：`papers/tpc-305-counterfactual-transported-label-budget/`

类型：**PROVED_EXACT_FINITE_COUNTERFACTUAL_TARGET_SWAP_PROTOCOL_PLUS_NUMERICALLY_CERTIFIED_FIXED_OPERATOR_TRANSPORTED_LABEL_BUDGET_ATLAS**。

TPC-305 承接 TPC-304 的 overlap fracture，构造 full-shell counterfactual：在相邻 shell
的公共素数上使用 optimally aligned neighboring label，off-overlap 保留 native label，
然后在每个固定 physical operator 上，将 native 与 transported target 放在同一个
最大可行 profile prefix 中重算约束 native budget。冻结 `(N,H,z)=(512,58,5)`、
`Q=50,60,70,90`、两种 exponent、三档 tolerance 与三种 source normalization，共有
18 个 target-swap cases、36 个 operator tables。

中心 `Q=60->70` 的 six-case orientation census 为 right-label-cheaper `5/6`、
home-operator-favored `1/6`；TPC-303 继承的 three same-prefix cases 全部为
right-label-cheaper。外侧分别为 `(left=4,cross=2)` 与
`(left=3,cross=1,home=2)`，且所有三种 normalizer 给出同一严格分类。这是 finite
partial counterfactual control：within-row target effect 已被隔离，但两个 shell 的
physical operator 仍不同，故不能称为 causal separation 或 asymptotic theorem。

最强正结果：中间 fracture 上五个 case 在两侧 fixed operator 都偏向 right-neighbor
label，且所有 same-prefix parent descent 都落入该类。

最强 obstruction：外侧 orientation 发生反转/混合，说明 target identity 与 operator
identity 仍有 interaction；当前尚无 two-way holdout 的 interaction contrast。

开放定理：在四格 operator/target holdout table 上定义并解释 home effect、target
effect 与 interaction term；uniform profile-budget growth、arithmetic `L2` 仍 OPEN。

可复用结构：`overlap alignment -> native off-overlap extension -> common prefix ->
fixed-operator budget -> two-row orientation atlas`。

ROUND2_CLUE：`TEST_TWO_WAY_OPERATOR_HOLDOUT_AND_INTERACTION_TERM_BEFORE_ANY_CAUSAL_TARGET_OPERATOR_CLAIM`。

```text
TPC305_ROUTE_ADVANCE = YES_SCOPED_COUNTERFACTUAL_TARGET_CONTROL
TPC305_ALIGNMENT_EXTENSION = PROVED_EXACT_FINITE
TPC305_COMMON_PREFIX_FEASIBILITY = PROVED_EXACT_FINITE
TPC305_FIXED_OPERATOR_TARGET_SWAP = PROVED_EXACT_FINITE
TPC305_COUNTERFACTUAL_BUDGET_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_CASES_36_TABLES
TPC305_MIDDLE_TARGET_ORIENTATION = NUMERICALLY_CERTIFIED_FINITE_RIGHT_LABEL_CHEAPER_5_OF_6
TPC305_MIDDLE_SAME_PREFIX_ORIENTATION = NUMERICALLY_CERTIFIED_FINITE_RIGHT_LABEL_CHEAPER_3_OF_3
TPC305_OUTER_ORIENTATION_CENSUS = NUMERICALLY_CERTIFIED_FINITE_4_2__5_1__3_1_2
TPC305_CAUSAL_SEPARATION = PARTIAL_COUNTERFACTUAL_ONLY
TPC305_OPERATOR_INTERACTION_TERM = OPEN
TPC305_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC305_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC305_FIXED_POWER_CREDIT = 0
TPC305_FULL_GATE_B = OPEN
TPC305_TWIN_PRIME_RESULT = NONE
TPC305_STATUS = PROVED_EXACT_FINITE_COUNTERFACTUAL_TARGET_SWAP_PROTOCOL_PLUS_NUMERICALLY_CERTIFIED_FIXED_OPERATOR_TRANSPORTED_LABEL_BUDGET_ATLAS
TPC305_ROUND2_CLUE = TEST_TWO_WAY_OPERATOR_HOLDOUT_AND_INTERACTION_TERM_BEFORE_ANY_CAUSAL_TARGET_OPERATOR_CLAIM
```

## 0.98 previous：TPC-304 overlapping-shell sign-label transport

项目：`papers/tpc-304-overlapping-shell-label-transport/`

类型：**PROVED_EXACT_FINITE_GAUGE_INVARIANT_OVERLAP_CORRELATION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_LABEL_TRANSPORT_FRACTURE_AND_BUDGET_DESCENT_LOCALIZATION**。

TPC-304 承接 TPC-303 的 fixed-source cardinality obstruction，直接把相邻 moving
prime shells 的 source-first weighted labels 限制到公共素数上。对两个独立的 global
sign gauge 做最优对齐后，严格得到 binary-label overlap correlation
`rho=|sum a(p)b(p)|/|O|` 与 aligned disagreement `d=(1-rho)/2`，从而消除了首个
shell prime 的 arbitrary gauge。

在冻结 `(N,H,z)=(512,58,5)`、`Q=50,60,70,90`、kernel exponent `1,2` 的六个
transport rows 上，三组 transition 的 mean correlation 精确为 `1/2,1/11,1/2`。
因此 `Q=60->70` 是唯一的低相关 fracture（两种 exponent 均为 `1/11`，公共重叠
大小为 11）；TPC-303 的 independently replayed budget descent census 同步为
`3,15,3`，same-prefix descent 为 `0,9,0`。中间 transition 同时是 correlation
最小组、descent 最大组，并承载全部 9 个 same-prefix descent。

最强正结果：global-sign-invariant transport observable 与 parent budget census
在同一个 finite transition 上精确对齐，且不是单一 exponent 的现象。

最强 obstruction：该 coincidence 仍不能区分 target-label switching 与 physical
shell/operator change；当前尚未计算 transported label 的 counterfactual native budget。

开放定理：固定 physical shell/operator，运输相邻 shell label 并重算 native budget，
以建立或否定 target/operator separation principle；uniform profile-budget growth 与
arithmetic `L2` 也仍开放。

可复用结构：`overlap -> global-sign gauge alignment -> exact mismatch census ->
parent budget crosswalk`。

ROUND2_CLUE：`COMPUTE_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGETS_TO_SEPARATE_TARGET_SWITCHING_FROM_OPERATOR_CHANGE`。

```text
TPC304_ROUTE_ADVANCE = YES_SCOPED_OVERLAPPING_SHELL_LOCALIZATION
TPC304_OVERLAP_CORRELATION_IDENTITY = PROVED_EXACT_FINITE
TPC304_GLOBAL_SIGN_GAUGE_INVARIANCE = PROVED_EXACT_FINITE
TPC304_LABEL_TRANSPORT_CROSSWALK = NUMERICALLY_CERTIFIED_FINITE_6_ROWS
TPC304_TRANSPORT_FRACTURE = NUMERICALLY_CERTIFIED_FINITE_Q60_TO_70_2_OF_2_EXPONENTS
TPC304_BUDGET_DESCENT_LOCALIZATION = NUMERICALLY_CERTIFIED_FINITE_15_3_3_AND_SAME_PREFIX_9_0_0
TPC304_CAUSAL_SEPARATION = OPEN
TPC304_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC304_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC304_FIXED_POWER_CREDIT = 0
TPC304_FULL_GATE_B = OPEN
TPC304_TWIN_PRIME_RESULT = NONE
TPC304_STATUS = PROVED_EXACT_FINITE_GAUGE_INVARIANT_OVERLAP_CORRELATION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_LABEL_TRANSPORT_FRACTURE_AND_BUDGET_DESCENT_LOCALIZATION
TPC304_ROUND2_CLUE = COMPUTE_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGETS_TO_SEPARATE_TARGET_SWITCHING_FROM_OPERATOR_CHANGE
```

## 0.97 previous: TPC-303 fixed-source cardinality-monotonicity obstruction

项目：`papers/tpc-303-cardinality-monotonicity-obstruction/`

类型：**PROVED_EXACT_INTERVAL_DESCENT_CRITERION_PLUS_NUMERICALLY_CERTIFIED_FIXED_SOURCE_CARDINALITY_MONOTONICITY_OBSTRUCTION**。

TPC-303 承接 TPC-302 的 growing-shell budget-gap stability，冻结
`(N,H,z)=(512,58,5)`，沿 `Q=50,60,70,90` 的 moving-shell spine 测试一个更强的
cardinality-only shortcut：shell cardinality 增大是否必然使 native weighted budget
增大。两种 kernel exponent、三档 relative RMS tolerance 与三种 source normalization
形成 18 个 parameter series、54 个 adjacent transitions。outward interval criterion
严格给出 21 个 descents、33 个 ascents、0 个 unresolved；18/18 series 均含 ascent
与 descent，且 9 个 descent 的 common profile prefix 不变。

最强正结果：该 obstruction 同时出现在全部 exponent/tolerance/normalizer series，
不是单一 normalization 或单一参数点的异常；interval order 本身是 exact finite
logic。最强 obstruction：`Q=60\to70` 在 exponent 2、`tau=3/4` 的 same-prefix
case 中，right/left interval ratio 小于 `0.284422`；总体最强 ratio 小于 `0.224974`。

开放定理：解释 source/profile/target label 如何共同制造 budget descent，并决定在
何种附加结构下还能恢复 uniform native profile-budget growth。该 finite spine 不是
asymptotic lower-bound refutation，且 Q-shells 不是 nested inclusion family。

可复用结构：`fixed-source shell spine -> outward interval order -> adjacent transition
census -> same-prefix descent firewall`。

ROUND2_CLUE：`LOCALIZE_BUDGET_DESCENTS_BY_TRANSPORTING_SIGN_LABELS_ACROSS_OVERLAPPING_SHELLS`。

```text
TPC303_ROUTE_ADVANCE = YES_SCOPED_CARDINALITY_ONLY_GROWTH_REFUTATION
TPC303_INTERVAL_ORDER = PROVED_EXACT_FINITE
TPC303_CARDINALITY_MONOTONICITY = REFUTED_SCOPED_DECLARED_FINITE_SPINE
TPC303_TRANSITION_CENSUS = NUMERICALLY_CERTIFIED_FINITE_21_DESCENTS_33_ASCENTS_0_UNRESOLVED
TPC303_NONMONOTONE_SERIES = NUMERICALLY_CERTIFIED_FINITE_18_OF_18
TPC303_SAME_PREFIX_DESCENTS = NUMERICALLY_CERTIFIED_FINITE_9
TPC303_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC303_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC303_FIXED_POWER_CREDIT = 0
TPC303_FULL_GATE_B = OPEN
TPC303_TWIN_PRIME_RESULT = NONE
TPC303_STATUS = PROVED_EXACT_INTERVAL_DESCENT_CRITERION_PLUS_NUMERICALLY_CERTIFIED_FIXED_SOURCE_CARDINALITY_MONOTONICITY_OBSTRUCTION
TPC303_ROUND2_CLUE = LOCALIZE_BUDGET_DESCENTS_BY_TRANSPORTING_SIGN_LABELS_ACROSS_OVERLAPPING_SHELLS
```

## 0.96 previous: TPC-302 growing-shell budget-gap audit

项目：`papers/tpc-302-growing-shell-budget-gap-audit/`

类型：**PROVED_EXACT_FINITE_SOURCE_FIRST_SIGN_ENUMERATION_AND_BUDGET_MONOTONICITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_GRID_AUDIT**。

TPC-302 将 TPC-301 的 tolerance/common-prefix/source-normalization hostile audit
扩展到 TPC-288 的 34-row growing/control grid。关键变化是 target provenance：每行
都从 literal physical output Gram 重新穷举 equal-sign classes，生成自己的 weighted
minimum label，再进入 native profile budget；不借用旧 18-row 标签。34 行共含 430
个显式 shell targets，父级 1,380-edge metadata 仍单独记录。

在 `tau=1/4,1/2,3/4` 下，common-prefix weighted/positive budget gap 的最小值为
`85.3203517096`、`38.2186652435`、`39.2637006403`，34/34 rows 在每档均超过 10；
三种 source normalizer 下 common weighted budget 在 102/102 cases 均超过 `1e-5`。
这是 finite growing-grid stability certificate，不是 uniform growing theorem。

最强正结果：source-first physical Gram、全符号类精确枚举与 native budget 的同一行
闭环，且 tolerance/common-prefix/normalization robustness 在 34 行保持。

最强 obstruction：有限 growing-grid 的稳定性仍没有给出 profile budget 随 shell/scale
增长的统一下界，arithmetic `L2` interface 也没有被支付。

开放定理：证明 uniform native profile-budget growth，或构造第一个 growing-shell
budget-gap collapse。

可复用结构：`physical Gram -> exact sign target -> literal profile image ->
constrained native budget frontier`。

ROUND2_CLUE：`TEST_UNIFORM_NATIVE_BUDGET_GROWTH_OR_CONSTRUCT_A_GROWING_SHELL_COUNTEREXAMPLE`。

```text
TPC302_ROUTE_ADVANCE = YES_SCOPED_FINITE_GROWING_GRID_SOURCE_FIRST_EXTENSION
TPC302_SOURCE_FIRST_SIGN_ENUMERATION = PROVED_EXACT_FINITE
TPC302_PHYSICAL_GRAM_PSD = PROVED_EXACT_FINITE
TPC302_BUDGET_MONOTONICITY = PROVED_EXACT_FINITE
TPC302_COMMON_GAP_TAU_025 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10
TPC302_COMMON_GAP_TAU_050 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10
TPC302_COMMON_GAP_TAU_075 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10
TPC302_FULL_GAP_TAU_075 = NUMERICALLY_CERTIFIED_FINITE_34_OF_34_ABOVE_10
TPC302_SOURCE_FIRST_LABELS = NUMERICALLY_CERTIFIED_FINITE_34_OF_34
TPC302_COMMON_BUDGET_FLOOR = NUMERICALLY_CERTIFIED_FINITE_102_OF_102_PER_NORMALIZATION
TPC302_EXPLICIT_SHELL_TARGET_COUNT = 430
TPC302_INHERITED_GRID_EDGE_COUNT = 1380
TPC302_UNIFORM_GROWING_PROFILE_BUDGET = OPEN
TPC302_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC302_FIXED_POWER_CREDIT = 0
TPC302_FULL_GATE_B = OPEN
TPC302_TWIN_PRIME_RESULT = NONE
TPC302_STATUS = PROVED_EXACT_FINITE_SOURCE_FIRST_SIGN_ENUMERATION_AND_BUDGET_MONOTONICITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_GRID_AUDIT
TPC302_ROUND2_CLUE = TEST_UNIFORM_NATIVE_BUDGET_GROWTH_OR_CONSTRUCT_A_GROWING_SHELL_COUNTEREXAMPLE
```

## 0.95 previous: TPC-301 budget-gap robustness audit

项目：`papers/tpc-301-budget-gap-robustness-audit/`

类型：**PROVED_EXACT_FINITE_TOLERANCE_MONOTONICITY_AND_HOMOGENEITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_GAP_ROBUSTNESS_ATLAS**。

TPC-301 承接 TPC-300 的 finite native budget dual certificate，把单一容差下的
weighted/positive budget separation 做 hostile audit。对相对 RMS
`tau=1/4,1/2,3/4`，每行先选取 weighted target 的首个可行 profile prefix，再把
weighted 与 all-positive control 放在同一个 common prefix 中比较，同时保留
target-specific 与 full-prefix controls。common-prefix gap 在三档容差、18/18 rows
均超过 10，最小值分别为 `155.1685273879`、`69.9448236917`、`39.2637006403`；
weighted common budget 在三种 target-independent source normalization 下均有
54/54 cases 超过 `3e-5`。实际显式 shell target 数为 219，父级 inherited grid
count 1,380 单独记录。

最强正结果：tolerance nesting、relative target homogeneity、threshold-prefix
nesting 与 common-prefix normalization cancellation 的有限精确定理。

最强 obstruction：即使把目标放入同一 source space，weighted/positive gap 在
最宽的测试容差 `3/4` 仍保留 `>39.26` 的 finite minimum。

开放定理：growing literal profile/source budget bound 与 arithmetic `L2` interface。

可复用结构：`tolerance ladder -> common weighted prefix -> three source normalizers -> gap atlas`。

ROUND2_CLUE：`EXTEND_TOLERANCE_AND_SOURCE_NORMALIZATION_AUDIT_TO_GROWING_SHELLS_AND_ARITHMETIC_L2_INTERFACE`。

```text
TPC301_ROUTE_ADVANCE = YES_SCOPED_SINGLE_TOLERANCE_TO_COMMON_PREFIX_ROBUSTNESS_LADDER
TPC301_TOLERANCE_MONOTONICITY = PROVED_EXACT_FINITE
TPC301_TARGET_HOMOGENEITY = PROVED_EXACT_FINITE
TPC301_PREFIX_THRESHOLD_MONOTONICITY = PROVED_EXACT_FINITE
TPC301_COMMON_NORMALIZATION_INVARIANCE = PROVED_EXACT_FINITE
TPC301_COMMON_GAP_TAU_025 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10
TPC301_COMMON_GAP_TAU_050 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10
TPC301_COMMON_GAP_TAU_075 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10
TPC301_FULL_GAP_TAU_025 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10
TPC301_FULL_GAP_TAU_050 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10
TPC301_FULL_GAP_TAU_075 = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_10
TPC301_COMMON_WEIGHTED_BUDGET_FLOOR_BETA = NUMERICALLY_CERTIFIED_FINITE_54_OF_54_ABOVE_3E_MINUS_5
TPC301_COMMON_WEIGHTED_BUDGET_FLOOR_TRACE = NUMERICALLY_CERTIFIED_FINITE_54_OF_54_ABOVE_3E_MINUS_5
TPC301_COMMON_WEIGHTED_BUDGET_FLOOR_FIRST = NUMERICALLY_CERTIFIED_FINITE_54_OF_54_ABOVE_3E_MINUS_5
TPC301_COMMON_GAP_NORMALIZATION_CHECKS = NUMERICALLY_CERTIFIED_FINITE_54
TPC301_FULL_TOLERANCE_MONOTONICITY_CHECKS = NUMERICALLY_CERTIFIED_FINITE_36
TPC301_SHELL_TARGET_COUNT = 219
TPC301_INHERITED_GRID_EDGE_COUNT = 1380
TPC301_PROFILE_BUDGET_GROWTH = OPEN
TPC301_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC301_FIXED_POWER_CREDIT = 0
TPC301_FULL_GATE_B = OPEN
TPC301_TWIN_PRIME_RESULT = NONE
TPC301_STATUS = PROVED_EXACT_FINITE_TOLERANCE_MONOTONICITY_AND_HOMOGENEITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_GAP_ROBUSTNESS_ATLAS
TPC301_ROUND2_CLUE = EXTEND_TOLERANCE_AND_SOURCE_NORMALIZATION_AUDIT_TO_GROWING_SHELLS_AND_ARITHMETIC_L2_INTERFACE
```

## 0.94 V153：TPC-300 native budget dual certificate

项目：`papers/tpc-300-native-budget-dual-certificate/`

类型：**PROVED_EXACT_FINITE_NATIVE_BUDGET_DUALITY_AND_RECIPROCAL_MULTIPLIER_CORRECTION_PLUS_NUMERICALLY_CERTIFIED_FINITE_RATIONAL_DUAL_WITNESS_ATLAS**。

TPC-300 承接 TPC-299 的 native profile budget frontier，给出 target-space dual
certificate。令 `(V^T V+rho M)c_rho=V^T b`，`R` 为 residual radius，并定义
`D_rho=(||b||^2-R^2-b^T Vc_rho)/rho`。严格证明任意 `rho>0` 时
`D_rho<=B_R(b)`；在 strict active finite frontier 上通过 Slater/KKT 取等号。
同时明确 KKT multiplier `mu` 与 ridge parameter `rho` 的关系为 `mu=1/rho`，
修正 TPC-299 producer 字段的记号语义而不改变其预算数值。

在继承的 18-row、1,380-edge grid 上，选取冻结 TPC-299 ridge interval 的
20-significant-digit rational midpoint，使用 exact Fraction Gauss--Jordan
生成 72 个 rational dual fractions（每行 threshold 的 minimum/maxcut/plus，
以及 full-prefix 的 weighted minimum）。所有 72 个 dual fraction 与
coefficient-vector hashes 通过 independent source-first replay；最小
dual/primal lower-bound ratio 为约 `0.9999999999999623`。weighted dual
threshold floor `9e-5/5e-4/1e-3` 的计数为 `18/15/14`，full-prefix
`1e-3` obstruction 为 `11/18`。这是 finite restricted certificate，
不等同于 growing native budget theorem。

```text
STRONGEST_POSITIVE_RESULT = EXACT_RATIONAL_TARGET_SPACE_DUAL_CERTIFICATE_COMPILER_AND_72_CASE_REPLAY
STRONGEST_OBSTRUCTION = TPC299_WEIGHTED_NATIVE_BUDGET_OBSTRUCTION_SURVIVES_DUAL_TRANSPORT
OPEN_THEOREM = GROWING_PROFILE_BUDGET_BOUND_AND_LITERAL_ARITHMETIC_L2
REUSABLE_STRUCTURE = NATIVE_PROFILE_FRONTIER -> RIDGE_PARAMETER -> EXACT_DUAL_FRACTION -> SUPPORTING_WITNESS
ROUND2_CLUE = HOSTILE_TEST_THE_DUAL_BUDGET_GAP_ACROSS_TOLERANCE_AND_SOURCE_NORMALIZATION_LADDERS
```

TPC300_ROUTE_ADVANCE = YES_SCOPED_PRIMAL_FRONTIER_TO_RATIONAL_DUAL_CERTIFICATE
TPC300_DUAL_LOWER_BOUND = PROVED_EXACT_FINITE
TPC300_STRONG_DUALITY_ACTIVE_FRONTIER = PROVED_EXACT_FINITE_SLATER
TPC300_RIDGE_KKT_RECIPROCITY = PROVED_EXACT_FINITE
TPC300_TPC299_PARAMETER_LABEL = CORRECTED_SCOPED_RIDGE_PARAMETER_NOT_KKT_MULTIPLIER
TPC300_RATIONAL_DUAL_WITNESSES = NUMERICALLY_CERTIFIED_FINITE_72_OF_72
TPC300_DUAL_TIGHTNESS = NUMERICALLY_CERTIFIED_FINITE_72_OF_72_ABOVE_0_999999999
TPC300_WEIGHTED_THRESHOLD_DUAL_FLOOR = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_9E_MINUS_5
TPC300_WEIGHTED_THRESHOLD_DUAL_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_14_OF_18_ABOVE_1E_MINUS_3
TPC300_WEIGHTED_FULL_PREFIX_DUAL_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_11_OF_18_ABOVE_1E_MINUS_3
TPC300_PROFILE_BUDGET_GROWTH = OPEN
TPC300_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC300_FIXED_POWER_CREDIT = 0
TPC300_FULL_GATE_B = OPEN
TPC300_TWIN_PRIME_RESULT = NONE

## 0.93 V152：TPC-299 native profile budget frontier

项目：`papers/tpc-299-native-profile-budget-frontier/`

类型：**PROVED_EXACT_FINITE_PROFILE_BUDGET_KKT_FRONTIER_PLUS_NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_OBSTRUCTION_ATLAS**。

TPC-299 承接 TPC-298 的完整 literal prefix ladder，定义
`B_(k,tau)(b)=min{c^T M_k c: ||V_kc-b||<=tau||b||}`，其中
`V_k=A^T U_k`、`M_k=U_k^T U_k`。严格证明这是实际 native source norm 的
quadratically constrained least-norm frontier，给出 KKT/ridge 路径、budget feasibility
iff 判据和 nested-prefix budget monotonicity。

在继承的 18-row、1,380-edge grid 和 17 个 literal prefixes 上，`tau=1/2` 的
weighted threshold budget 在 18/18 行超过 `9e-5||beta||^2`，15/18 超过
`5e-4`，14/18 超过 `1e-3`；full prefix 仍有 11/18 超过 `1e-3`。all-positive
control 在 18/18 行低于 `1e-4`，weighted/positive threshold-budget gap 在 18/18
行超过 20。producer、source-first independent replay、stress suite 与 Bridge-B
checker 均在 normal/optimized 两种模式下通过；这是 restricted finite obstruction，
不等同于 growing native budget theorem。

```text
STRONGEST_POSITIVE_RESULT = EXACT_KKT_RIDGE_PROFILE_BUDGET_FRONTIER_AND_FINITE_NATIVE_BUDGET_ATLAS
STRONGEST_OBSTRUCTION = WEIGHTED_TARGET_BUDGET_EXCEEDS_POSITIVE_CONTROL_BY_MORE_THAN_20_ON_ALL_18_ROWS
OPEN_THEOREM = GROWING_PROFILE_BUDGET_BOUND_AND_LITERAL_ARITHMETIC_L2
REUSABLE_STRUCTURE = NESTED_NATIVE_PROFILE_PREFIX -> QCQP_FRONTIER -> KKT_RIDGE_PATH -> BUDGET_FEASIBILITY
ROUND2_CLUE = BUILD_AN_EXACT_DUAL_SUPPORTING_HYPERPLANE_CERTIFICATE_FOR_THE_NATIVE_BUDGET_FRONTIER
```

TPC299_ROUTE_ADVANCE = YES_SCOPED_PROFILE_ANGLE_TO_NATIVE_BUDGET_FRONTIER
TPC299_PROFILE_BUDGET_KKT_FRONTIER = PROVED_EXACT_FINITE
TPC299_NESTED_BUDGET_MONOTONICITY = PROVED_EXACT_FINITE
TPC299_WEIGHTED_HALF_RMS_BUDGET_FLOOR = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_9E_MINUS_5
TPC299_WEIGHTED_HALF_RMS_BUDGET_MID_FLOOR = NUMERICALLY_CERTIFIED_FINITE_15_OF_18_ABOVE_5E_MINUS_4
TPC299_WEIGHTED_HALF_RMS_BUDGET_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_14_OF_18_ABOVE_1E_MINUS_3
TPC299_WEIGHTED_FULL_PREFIX_BUDGET_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_11_OF_18_ABOVE_1E_MINUS_3
TPC299_PLUS_HALF_RMS_BUDGET_CEILING = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_1E_MINUS_4
TPC299_WEIGHTED_PLUS_BUDGET_GAP = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_20
TPC299_PROFILE_BUDGET_GROWTH = OPEN
TPC299_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC299_FIXED_POWER_CREDIT = 0
TPC299_FULL_GATE_B = OPEN
TPC299_TWIN_PRIME_RESULT = NONE

## 0.92 V151：TPC-298 literal source-profile angle and dimension ladder

项目：`papers/tpc-298-profile-angle-dimension-ladder/`

类型：**PROVED_EXACT_FINITE_PRINCIPAL_ANGLE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_PROFILE_DIMENSION_LADDER**。

TPC-298 承接 TPC-297 的四个 literal cutoff profiles，按 cutoff 排序形成 17-profile
prefix ladder
`3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61`。令
U_k 为前缀 source matrix、A 为冻结 physical shell matrix、V_k=A^T U_k，
严格证明 least-squares projection、principal-angle identity 与 nested-prefix
monotonicity；threshold dimension k_tau 因而是一个可审计的有限几何量。

在继承的 18-row literal grid、1,380 edges 上，双模 replay 对 17 个 prefixes 共完成
306 项 rank checks，全部符合 min(k,|S|)；70 位 producer 与独立 source-first replay
显示 weighted target 首次达到 half-RMS 1/2 所需维度比例在 18/18 行至少为 2/3，
all-positive control 在 18/18 行至多使用 6 个 profiles，最后一个有限 prefix 在
18/18 行覆盖有限 target space。最大 prefix condition upper 约为 4.24e4，只作为
finite diagnostic。cutoff ladder、threshold 与 finite grid 都是 modeling choices，
不产生 arithmetic 或 exponent credit。

```text
STRONGEST_POSITIVE_RESULT = COMPLETE_EXPECTED_PREFIX_RANK_LADDER_AND_FINITE_TARGET_CAPTURE
STRONGEST_OBSTRUCTION = WEIGHTED_HALF_RMS_REQUIRES_AT_LEAST_TWO_THIRDS_OF_SHELL_DIMENSION
OPEN_THEOREM = GROWING_NATIVE_PROFILE_DIMENSION_ANGLE_CONDITIONING_AND_BUDGET_BOUND
REUSABLE_STRUCTURE = NESTED_LITERAL_SOURCE_PREFIX -> IMAGE -> PRINCIPAL_ANGLE -> THRESHOLD_DIMENSION
ROUND2_CLUE = TEST_WEIGHTED_PROFILE_DIMENSION_AGAINST_LEAST_NORM_SOURCE_BUDGET_AND_CONDITIONING
```

```text
TPC298_ROUTE_ADVANCE = YES_SCOPED_FOUR_PROFILE_SNAPSHOT_TO_COMPLETE_LITERAL_PREFIX_LADDER
TPC298_PROJECTION_IDENTITY = PROVED_EXACT_FINITE
TPC298_PRINCIPAL_ANGLE_IDENTITY = PROVED_EXACT_FINITE
TPC298_NESTED_PREFIX_MONOTONICITY = PROVED_EXACT_FINITE
TPC298_TWO_MODULUS_PREFIX_RANK = NUMERICALLY_CERTIFIED_FINITE_18_OF_18
TPC298_WEIGHTED_HALF_RMS_DIMENSION = NUMERICAL_OBSERVATION_18_OF_18_RATIO_AT_LEAST_2_OVER_3
TPC298_PLUS_HALF_RMS_DIMENSION = NUMERICAL_OBSERVATION_18_OF_18_AT_MOST_6
TPC298_FULL_PREFIX_CAPTURE = NUMERICALLY_CERTIFIED_FINITE_18_OF_18
TPC298_GROWING_DIMENSION_THEOREM = OPEN
TPC298_CONDITIONING_GROWTH = OPEN
TPC298_SOURCE_BUDGET_GROWTH = OPEN
TPC298_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC298_FIXED_POWER_CREDIT = 0
TPC298_FULL_GATE_B = OPEN
TPC298_TWIN_PRIME_RESULT = NONE
TPC298_STATUS = PROVED_EXACT_FINITE_PRINCIPAL_ANGLE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_PROFILE_DIMENSION_LADDER
```

## 0.91 V150：TPC-297 literal source-profile span and weighted-angle obstruction

项目：`papers/tpc-297-literal-source-profile-span-audit/`

类型：**PROVED_EXACT_FINITE_RESTRICTED_PROFILE_PROJECTION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_FOUR_CUTOFF_PROFILE_ATLAS**。

TPC-297 承接 TPC-296 的冻结一维 native ray，定义四个 source-side literal cutoff profiles
`beta_z(t)=lambda(t)-sum_{d<=z,d|t}mu(d)`，其中 `z=3,5,7,11`。令 `U` 为四列 profile
matrix、`A` 为冻结 physical shell matrix、`V=A^T U`，严格证明受限 least-squares
identity `min_c||Vc-b||^2=b^T(I-P_V)b`，并证明加入 source direction 不能增加最优
残差。

在继承的 18-row literal grid、1,380 edges 上，两模 Gaussian rank replay 给出 rank 3
（三素数 shell）1 行、rank 4 17 行。70 位 producer 与独立 source-first replay 显示
all-positive target 的 profile RMS `<=0.15` 为 18/18；weighted target 的 RMS `>=0.6`
为 17/17 个至少五素数的 large-shell rows。四-profile residual 在 18/18 行不劣于
TPC-296 冻结 ray。这是一个真实的 finite native-profile 正进展，同时也是 weighted
方向的明确 obstruction；cutoff family 是 modeling choice，不产生 asymptotic 或
arithmetic credit。

```text
STRONGEST_POSITIVE_RESULT = FOUR_LITERAL_CUTOFF_PROFILES_HAVE_RANK_4_AND_CAPTURE_ALL_POSITIVE_TARGETS
STRONGEST_OBSTRUCTION = WEIGHTED_TARGETS_STAY_OUTSIDE_THE_FOUR_PROFILE_IMAGE_ON_17_LARGE_SHELLS
OPEN_THEOREM = GROWING_NATIVE_PROFILE_DIMENSION_OR_PRINCIPAL_ANGLE_BOUND
REUSABLE_STRUCTURE = SOURCE_PROFILE_MATRIX -> CORRELATION_IMAGE -> ORTHOGONAL_PROJECTION -> TARGET_RESIDUAL
ROUND2_CLUE = TEST_NATIVE_PROFILE_PRINCIPAL_ANGLES_AND_MINIMUM_DIMENSION
```

```text
TPC297_ROUTE_ADVANCE = YES_SCOPED_NATIVE_PROFILE_RAY_TO_FOUR_LITERAL_CUTOFF_SPAN
TPC297_PROJECTION_IDENTITY = PROVED_EXACT_FINITE
TPC297_NESTED_PROFILE_MONOTONICITY = PROVED_EXACT_FINITE
TPC297_TWO_MODULUS_IMAGE_RANK = NUMERICALLY_CERTIFIED_FINITE_3_PLUS_4
TPC297_WEIGHTED_PROFILE_SEPARATION = NUMERICAL_OBSERVATION_17_OF_17_AT_LEAST_0_6
TPC297_ALL_POSITIVE_PROFILE_CAPTURE = NUMERICAL_OBSERVATION_18_OF_18_AT_MOST_0_15
TPC297_PROFILE_FAMILY = MODELING_CHOICE_LITERAL_CUTOFFS_3_5_7_11
TPC297_GROWING_PROFILE_DIMENSION = OPEN
TPC297_PRINCIPAL_ANGLE_THEOREM = OPEN
TPC297_SOURCE_BUDGET_GROWTH = OPEN
TPC297_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC297_FIXED_POWER_CREDIT = 0
TPC297_FULL_GATE_B = OPEN
TPC297_TWIN_PRIME_RESULT = NONE
TPC297_STATUS = PROVED_EXACT_FINITE_RESTRICTED_PROFILE_PROJECTION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_FOUR_CUTOFF_PROFILE_ATLAS
```

## 0.90 V149：TPC-296 least-norm source budget and native-ray obstruction

项目：`papers/tpc-296-source-norm-budget-interface/`

类型：**PROVED_EXACT_LEAST_NORM_SOURCE_BUDGET_AND_SOURCE_ENERGY_TRADEOFF_PLUS_NUMERICALLY_CERTIFIED_FINITE_COST_PROFILE_ATLAS**。

TPC-296 承接 TPC-295 的 unrestricted finite source-correlation image，把“存在 witness”
推进成“witness 需要多少 source budget”。令 physical columns 为 `A`、`G=A^T A`，严格
证明
`S_A(b)=min_{A^T h=b}||h||_2^2=b^T G^(-1)b`，显式最小解为 `h=A G^(-1)b`；从而
`S_A(b)<=B` 是预算可行性的 iff criterion。进一步由 Cauchy--Schwarz 严格得到
`S_A(b)(b^TGb)>=(b^Tb)^2`，把 source cost 与 physical target energy 接在同一个
可复用接口上。

在继承的 18-row literal grid、1,380 edges 上，70 位高精度 producer、独立 source-first
replay 与 exact stress suite 完成 finite audit。weighted minimizer、unit-edge max-cut
与 all-positive targets 的 unrestricted cost ratio 都低于声明的 `1e-3` 阈值（各 18/18）；
source-energy tradeoff 的 54 个 target checks 全部通过，最大 finite Gram condition
number 约为 `2497.29180077`。另一方面，weighted minimizer 与 max-cut 到冻结一维
proxy `span{A^T beta}` 的 normalized RMS 在 18/18 rows 均至少为 `0.9`；这说明 ambient
least-norm budget 在有限样本中并非主障碍，真正未支付的是 native profile 的 image/
dimension 与 growing-shell control。

预算阈值 `1e-3` 与冻结-beta 一维 ray 是明确的 modeling choices，不是 native arithmetic
profile theorem，也不产生 exponent 或 fixed-power credit。该项目的 strongest positive
result 是 exact least-norm budget compiler 加 18-row high-precision cost/profile atlas；
strongest obstruction 是 unrestricted cheap witnesses 仍远离冻结 native ray。下一步最小
自然问题是构造 2--4 维的 literal native profile basis，并同时审计 growing source budget。
Session-named Route-A/Route-B evaluator 文件在 checkout 中缺失，因此这里不宣称官方
evaluator pass；本地 proof package、canonical certificate、independent replay、stress
与 Bridge-B checker 是 fail-closed fallback。

```text
STRONGEST_POSITIVE_RESULT = EXACT_LEAST_NORM_BUDGET_COMPILER_PLUS_18_ROW_HIGH_PRECISION_COST_ATLAS
STRONGEST_OBSTRUCTION = CHEAP_UNRESTRICTED_WITNESSES_ARE_FAR_FROM_THE_FROZEN_NATIVE_RAY
OPEN_THEOREM = GROWING_RESTRICTED_PROFILE_IMAGE_WITH_A_PAYABLE_SOURCE_NORM_BUDGET
REUSABLE_STRUCTURE = GRAM_INVERSE -> LEAST_NORM_SOURCE_COST -> ENERGY_TRADEOFF -> PROFILE_PROJECTION
ROUND2_CLUE = TEST_RESTRICTED_PROFILE_DIMENSION_AND_GROWING_SOURCE_BUDGET
```

```text
TPC296_ROUTE_ADVANCE = YES_SCOPED_SOURCE_IMAGE_TO_LEAST_NORM_BUDGET_AND_PROFILE_GEOMETRY
TPC296_LEAST_NORM_IDENTITY = PROVED_EXACT_FINITE
TPC296_BUDGET_FEASIBILITY_CRITERION = PROVED_EXACT_FINITE
TPC296_SOURCE_ENERGY_TRADEOFF = PROVED_EXACT_FINITE
TPC296_COST_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_ROWS_HIGH_PRECISION_REPLAY
TPC296_UNRESTRICTED_BUDGET_TEST = NUMERICAL_OBSERVATION_FINITE_18_OF_18_BELOW_1E_MINUS_3
TPC296_ONE_RAY_PROFILE_OBSTRUCTION = NUMERICAL_OBSERVATION_FINITE_18_OF_18_RMS_AT_LEAST_0_9
TPC296_NATIVE_RESTRICTED_PROFILE = OPEN_LITERAL_SOURCE
TPC296_GROWING_SOURCE_BUDGET = OPEN
TPC296_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC296_FIXED_POWER_CREDIT = 0
TPC296_FULL_GATE_B = OPEN
TPC296_TWIN_PRIME_RESULT = NONE
TPC296_STATUS = PROVED_EXACT_LEAST_NORM_SOURCE_BUDGET_AND_SOURCE_ENERGY_TRADEOFF_PLUS_NUMERICALLY_CERTIFIED_FINITE_COST_PROFILE_ATLAS
```

## 0.89 当前：TPC-295 source-correlation image and finite signed feasibility

项目：`papers/tpc-295-source-correlation-image-audit/`

类型：**PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION_SURJECTIVITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_MODULAR_FULL_RANK_ATLAS**。

TPC-295 承接 TPC-294 的 ambient magnitude-weighted sign minimizer，令物理 shell vectors
为 rational matrix `A` 的 columns，定义 source-correlation map
`C=A^T:Q^I -> Q^S`。严格证明：若 `G=A^T A` 非奇异，则 `C` surjective，且任意 target
`b` 的显式 witness 为 `h=A G^(-1)b`；同时该 witness 是实数解中的 least-norm solution。

在继承的 18-row literal grid 上，使用两个独立模数 `1000000007` 与 `998244353` 做
exact modular determinant/rank replay：18/18 rows 在两个模数均 full rank，覆盖 1,380
shell edges。故 unrestricted finite rational source space 中，TPC-294 weighted minimizer、
unit-edge max-cut target 与 all-positive target 均 18/18 可达，并通过两模 target residual
replay。

这里的“source-realizable”严格限定为 unrestricted `Q^I` image。native Mobius/comparison
profile 是否包含这些 witness、least-norm cost 是否在 growing shell 中可控、arithmetic
`L2` 与 Gate B 是否得到 credit，均没有被这篇论文解决。

```text
STRONGEST_POSITIVE_RESULT = EXACT_FULL_RANK_TO_SOURCE_SURJECTIVITY_COMPILER_PLUS_TWO_MODULUS_18_ROW_ATLAS
STRONGEST_OBSTRUCTION = UNRESTRICTED_FINITE_SOURCE_IMAGE_DOES_NOT_CONTROL_NATIVE_PROFILE_OR_WITNESS_NORM
OPEN_THEOREM = RESTRICTED_NATIVE_PROFILE_IMAGE_AND_GROWING_LEAST_NORM_SOURCE_BUDGET
REUSABLE_STRUCTURE = PHYSICAL_COLUMNS -> GRAM_RANK -> SOURCE_CORRELATION_IMAGE -> LEAST_NORM_WITNESS
ROUND2_CLUE = TEST_SOURCE_NORM_COST_AND_RESTRICTED_NATIVE_PROFILE_IMAGE
```

```text
TPC295_ROUTE_ADVANCE = YES_SCOPED_AMBIENT_SIGN_TARGETS_TO_UNRESTRICTED_FINITE_SOURCE_IMAGE
TPC295_FULL_RANK_IMPLICATION = PROVED_EXACT_FINITE
TPC295_LEAST_NORM_WITNESS_FORMULA = PROVED_EXACT_FINITE
TPC295_MODULAR_FULL_RANK_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_TWO_MODULI
TPC295_UNRESTRICTED_SOURCE_CORRELATION_SURJECTIVITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18
TPC295_WEIGHTED_MINIMIZER_SOURCE_REALIZABILITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_UNRESTRICTED
TPC295_MAXCUT_SOURCE_REALIZABILITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_UNRESTRICTED
TPC295_NATIVE_RESTRICTED_PROFILE = OPEN_LITERAL_SOURCE
TPC295_SOURCE_WITNESS_NORM = OPEN
TPC295_GROWING_SOURCE_IMAGE = OPEN
TPC295_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC295_FIXED_POWER_CREDIT = 0
TPC295_FULL_GATE_B = OPEN
TPC295_TWIN_PRIME_RESULT = NONE
TPC295_STATUS = PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION_SURJECTIVITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_MODULAR_FULL_RANK_ATLAS
```

## 0.88 当前：TPC-294 magnitude-weighted signed Rayleigh atlas

项目：`papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/`

类型：**PROVED_EXACT_TRACE_NORMALIZED_SIGNED_QUADRATIC_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_GLOBAL_SIGN_ATLAS**。

TPC-294 承接 TPC-293 的 unit-edge signed max-cut，把真实 Gram magnitudes 恢复到
equal-coefficient sign 的 trace-normalized quadratic objective
`R(a)=a^T G a/tr(G)`。严格证明 diagonal-plus-cross-term identity、Gram
nonnegativity，以及 common-denominator exhaustive enumeration 在 global sign reversal
下给出 finite global optimum。

沿用 18-row literal grid，完整审计 1,380 edges。18/18 rows 的 global weighted minima
低于 1，18/18 rows 的 all-positive quotient 高于 1，18/18 rows 的 weighted optimum
与 unit-edge max-cut witness 不同；13/18 个 minimum 不超过 `1/4`，8/18 不超过 `1/10`。
最强 finite minimum 为 `(512,58,90,5,2)` row 的 `0.0496374497659`；早期 crossover
row 的 max-cut quotient 为 `0.988974603760`，真正 weighted optimum 为 `0.519059163428`。

最强正结果是：把 shell sign problem 提升为可全局求解的 magnitude-weighted Rayleigh
layer，并以独立 source-first replay 与 Gray/brute/PSD stress 固化。最强 obstruction
是：所有 sign vectors 仍在 ambient coefficient-sign cube 中，未证明落入 native source
image；有限 contraction 不能直接兑换 growing-shell 或 arithmetic credit。

```text
STRONGEST_POSITIVE_RESULT = EXACT_TRACE_NORMALIZED_WEIGHTED_SIGN_IDENTITY_PLUS_GLOBAL_FINITE_18_ROW_ATLAS
STRONGEST_OBSTRUCTION = WEIGHTED_OPTIMA_ARE_AMBIENT_SIGN_WITNESSES_WITH_SOURCE_IMAGE_UNPROVED
OPEN_THEOREM = SOURCE_RESTRICTED_WEIGHTED_MINIMUM_OR_APPROXIMATE_ATTAINABILITY
REUSABLE_STRUCTURE = PHYSICAL_GRAM -> SIGNED_MAXCUT -> MAGNITUDE_WEIGHTED_RAYLEIGH -> SOURCE_IMAGE AUDIT
ROUND2_CLUE = TEST_SOURCE_IMAGE_OF_WEIGHTED_OPTIMAL_SIGN_PATTERNS_AND_DIFFUSE_SIGNED_WEIGHTS
```

```text
TPC294_ROUTE_ADVANCE = YES_SCOPED_FINITE_SIGN_LAYER_TO_MAGNITUDE_WEIGHTED_RAYLEIGH_LAYER
TPC294_TRACE_NORMALIZED_IDENTITY = PROVED_EXACT_FINITE
TPC294_GLOBAL_SIGN_ENUMERATION = PROVED_EXACT_FINITE
TPC294_GRAM_NONNEGATIVITY = PROVED_EXACT_FINITE
TPC294_WEIGHTED_RAYLEIGH_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC294_EQUAL_SIGNED_CONTRACTION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_ONE
TPC294_ALL_POSITIVE_AMPLIFICATION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_ONE
TPC294_WEIGHTED_VS_MAXCUT = NUMERICALLY_CERTIFIED_FINITE_DIFFERENT_18_OF_18
TPC294_SOURCE_NATIVE_COEFFICIENT_IMAGE = OPEN_LITERAL_SOURCE
TPC294_GROWING_WEIGHTED_THEOREM = OPEN
TPC294_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC294_FIXED_POWER_CREDIT = 0
TPC294_FULL_GATE_B = OPEN
TPC294_TWIN_PRIME_RESULT = NONE
TPC294_STATUS = PROVED_EXACT_TRACE_NORMALIZED_SIGNED_QUADRATIC_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_GLOBAL_SIGN_ATLAS
```

## 0.87 当前：TPC-293 signed shell max-cut atlas

项目：`papers/tpc-293-signed-shell-maxcut-atlas/`

类型：**PROVED_EXACT_ALL_POSITIVE_MAXCUT_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGNED_SHELL_FRUSTRATION_ATLAS**。

TPC-293 承接 TPC-292 的 triangle parity obstruction，把局部兼容性提升为 whole-shell
signed complete graph。对 edge signs `sigma_ij`，maximize
`#{i<j:a_i a_j sigma_ij=-1}`；严格证明 all-positive `K_m` 的 optimum 为
`floor(m^2/4)`，minimum unsatisfied 等于总边数减 optimum，并证明 vertex switching
保持该 objective。

沿用 18-row literal grid，完整审计 1,380 个 Gram edges 与所有 shell labelings。
17 rows 的所有 cross signs 均为正，exact optimum 与 all-positive benchmark 相同；唯一
`(256,38,27,5,1)` row 有 3 个 negative edges，signed optimum 为 15、benchmark 为 12。
总计 max favorable 为 744、minimum unsatisfied 为 636、sign-only gain 为 3。

最强正结果是 exact whole-shell sign compiler 与完整 finite atlas；最强 obstruction 是
17/18 shells 直接落在 all-positive max-cut wall，唯一异常也只有 unit-edge `+3`。该 gain
没有包含 Gram magnitudes，故不能兑换 physical energy 或 arithmetic `L2` credit。

```text
STRONGEST_POSITIVE_RESULT = EXACT_ALL_POSITIVE_MAXCUT_SWITCHING_COMPILER_PLUS_1380_EDGE_ATLAS
STRONGEST_OBSTRUCTION = WHOLE_SHELL_SIGN_OPTIMUM_MATCHES_ALL_POSITIVE_WALL_ON_17_OF_18_ROWS
OPEN_THEOREM = MAGNITUDE_WEIGHTED_SIGNED_RAYLEIGH_BOUND_WITH_LITERAL_SOURCE_IMAGE
REUSABLE_STRUCTURE = PHYSICAL_GRAM -> SIGNED_COMPLETE_GRAPH -> MAXCUT/FRUSTRATION -> WEIGHTED_TEST
ROUND2_CLUE = TEST_MAGNITUDE_WEIGHTED_SIGNED_RAYLEIGH_AND_SOURCE_IMAGE
```

```text
TPC293_ROUTE_ADVANCE = YES_SCOPED_THREE_PRIME_TO_WHOLE_SHELL_SIGNED_GRAPH
TPC293_ALL_POSITIVE_MAXCUT = PROVED_EXACT_CONDITIONAL
TPC293_SIGNED_OBJECTIVE = PROVED_EXACT_FINITE
TPC293_SWITCHING_INVARIANCE = PROVED_EXACT_FINITE
TPC293_SIGNED_MAXCUT_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC293_EDGE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_1380_EDGES
TPC293_MAX_FAVORABLE = NUMERICALLY_CERTIFIED_FINITE_744
TPC293_MINIMUM_UNSATISFIED = NUMERICALLY_CERTIFIED_FINITE_636
TPC293_EXCEPTIONAL_GAIN = NUMERICALLY_CERTIFIED_FINITE_PLUS_3_EDGES_ONE_ROW
TPC293_GROWING_SIGNED_GRAPH = OPEN
TPC293_MAGNITUDE_WEIGHTED_RAYLEIGH = OPEN
TPC293_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE
TPC293_FIXED_POWER_CREDIT = 0
TPC293_FULL_GATE_B = OPEN
TPC293_TWIN_PRIME_RESULT = NONE
TPC293_STATUS = PROVED_EXACT_ALL_POSITIVE_MAXCUT_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGNED_SHELL_FRUSTRATION_ATLAS
```

## 0.86 当前：TPC-292 three-prime sign frustration atlas

项目：`papers/tpc-292-three-prime-sign-frustration-atlas/`

类型：**PROVED_EXACT_TRIANGLE_SIGN_PARITY_AND_THREE_VECTOR_SCHUR_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGN_FRUSTRATION_ATLAS**。

TPC-292 承接 TPC-291 的 pairwise Schur cancellation，把下一步问题收缩为三素数符号
兼容性。对三个非零 Gram edges，严格证明 coefficient signs 能让三个 pair contributions
同时非正，当且仅当 edge-sign product 为 `-1`；product 为 `+1` 的 triangle 是
sign-frustrated。对三向量同时严格证明 Schur projection residual
`det(G)/(d_i det(G_(j,k)))` 与 normalized Gram volume identity。

沿用同一 18-row literal grid，完整审计 5,727 个 unordered prime triples：5,718 个
sign-frustrated、9 个 anti-alignable、0 个 zero-edge，且 5,727 个 normalized volumes
全为正。edge patterns 为 `+++:5715, ++-:1, +-+:8, +--:3`；late
`(512,58,90,5,2)` row 的 680 个 triples 全为 `+++`。最小 target Schur residual
约为 `0.0115083261`，见 triple `(167,173,179)`。

最强正结果是 exact triangle parity / three-vector Schur compiler 加完整 finite atlas；
最强 obstruction 是 pairwise signed cancellation 在三角 cycle 上通常不能同时实现。
growing-shell compatibility、source-native arithmetic `L2`、fixed-power credit 与 full
Gate B 仍 OPEN/NONE。

```text
STRONGEST_POSITIVE_RESULT = EXACT_TRIANGLE_PARITY_AND_THREE_VECTOR_SCHUR_COMPILER_PLUS_5727_TRIPLE_ATLAS
STRONGEST_OBSTRUCTION = PAIRWISE_SIGNED_CANCELLATION_IS_GENERICALLY_FRUSTRATED_ON_TRIANGLES
OPEN_THEOREM = GROWING_SIGNED_GRAPH_COMPATIBILITY_WITH_LITERAL_SOURCE_IMAGE
REUSABLE_STRUCTURE = SIGNED_GRAM_GRAPH -> CYCLE PARITY -> SCHUR RESIDUAL -> SOURCE TEST
ROUND2_CLUE = TEST_SIGNED_GRAPH_MAXCUT_AND_MULTI_PRIME_RAYLEIGH_COMPATIBILITY
```

```text
TPC292_ROUTE_ADVANCE = YES_SCOPED_PAIRWISE_TO_THREE_PRIME_COMPATIBILITY_OBSTRUCTION
TPC292_TRIANGLE_SIGN_PARITY = PROVED_EXACT_CONDITIONAL
TPC292_THREE_VECTOR_SCHUR_IDENTITY = PROVED_EXACT_FINITE
TPC292_NORMALIZED_VOLUME = PROVED_EXACT_FROM_GRAM_PSD
TPC292_TRIANGLE_ATLAS = NUMERICALLY_CERTIFIED_FINITE_5727_TRIPLES
TPC292_SIGN_FRUSTRATION = NUMERICALLY_CERTIFIED_FINITE_5718_OF_5727
TPC292_ANTI_ALIGNABLE = NUMERICALLY_CERTIFIED_FINITE_9_OF_5727
TPC292_GROWING_TRIANGLE_COMPATIBILITY = OPEN
TPC292_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE
TPC292_FIXED_POWER_CREDIT = 0
TPC292_FULL_GATE_B = OPEN
TPC292_TWIN_PRIME_RESULT = NONE
TPC292_STATUS = PROVED_EXACT_TRIANGLE_SIGN_PARITY_AND_THREE_VECTOR_SCHUR_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGN_FRUSTRATION_ATLAS
```

## 0.85 当前：TPC-291 signed Schur cancellation atlas

项目：`papers/tpc-291-signed-schur-cancellation-atlas/`

类型：**PROVED_EXACT_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_COHERENCE_TO_CANCELLATION_ATLAS**。

TPC-291 承接 TPC-290 的 adaptive weighted-Gram firewall，把 cross-prime coherence 精确
编译成 two-prime signed cancellation。对任意 nonzero physical component pair，严格证明
投影系数 `rho*=G_(i,j)/d_j`、归一化 Schur residual `1-Gamma_(i,j)`，以及 signed
two-vector Rayleigh minimum `1-sqrt(Gamma_(i,j))`；系数符号同时给出 opposite-sign 与
same-sign cancellation 的必要方向。

沿用 TPC-289 的 18-row literal grid，完整审计 1,380 个 unordered pairs：1,377 个
positive、3 个 negative、0 个 zero cross terms；Schur residual `<=1/2`、`<=1/4`、
`<=1/10` 的 pair 数分别为 1,074、852、477，`Gamma>=9/25` 与 `Gamma>=3/4` 的
pair 数为 1,189、852。全球最佳 pair 是 late growth row
`(N,H,Q,z,s)=(512,58,90,5,2)` 中的 `(173,179)`，residual 约为 `0.0151239493`；
三个 same-sign negative witnesses `(29,53),(31,53),(41,53)` 全部位于早期
`(256,38,27,5,1)` crossover row。

最强正结果是 exact Schur/Rayleigh cancellation compiler 加完整有限 atlas；最强
obstruction 是 1,377 个高相干正 pair 的方向需要 signed reassembly，而不是自动落在
nonnegative shell cone 内。multi-prime signed reassembly、growing signed theorem、
source-native arithmetic `L2`、fixed-power credit 与 full Gate B 仍 OPEN/NONE。

```text
STRONGEST_POSITIVE_RESULT = EXACT_SCHUR_RESIDUAL_AND_SIGNED_RAYLEIGH_COMPILER_PLUS_1380_PAIR_ATLAS
STRONGEST_OBSTRUCTION = PAIRWISE_CANCELLATION_DOES_NOT_ASSEMBLE_ITSELF_INTO_FULL_PRIME_SHELL
OPEN_THEOREM = MULTI_PRIME_SIGNED_REASSEMBLY_WITH_LITERAL_SOURCE_ARITHMETIC_L2
REUSABLE_STRUCTURE = COHERENCE -> SCHUR RESIDUAL -> SIGN COST -> REASSEMBLY TEST
ROUND2_CLUE = TEST_SOURCE_RESTRICTED_DIFFUSE_WEIGHTS_OR_MULTI_PRIME_SIGNED_NULL_DIRECTIONS
```

```text
TPC291_ROUTE_ADVANCE = YES_SCOPED_SIGNED_SCHUR_COHERENCE_TO_CANCELLATION_ATLAS
TPC291_SCHUR_PROJECTION_IDENTITY = PROVED_EXACT_FINITE
TPC291_SIGNED_TWO_PRIME_CANCELLATION = PROVED_EXACT_CONDITIONAL
TPC291_RESIDUAL_NONNEGATIVITY = PROVED_EXACT_FROM_CAUCHY
TPC291_COHERENCE_TO_CANCELLATION_ATLAS = NUMERICALLY_CERTIFIED_FINITE_1380_PAIRS
TPC291_LOW_RESIDUAL_COUNTS = NUMERICALLY_CERTIFIED_FINITE_1074_852_477
TPC291_SIGN_COST_CENSUS = NUMERICALLY_CERTIFIED_FINITE_1377_OPPOSITE_3_SAME
TPC291_GROWING_SIGNED_THEOREM = OPEN
TPC291_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE
TPC291_FIXED_POWER_CREDIT = 0
TPC291_FULL_GATE_B = OPEN
TPC291_TWIN_PRIME_RESULT = NONE
TPC291_STATUS = PROVED_EXACT_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_COHERENCE_TO_CANCELLATION_ATLAS
```

## 0.84 当前：TPC-290 adaptive shell weighting obstruction

项目：`papers/tpc-290-adaptive-shell-weighting-obstruction/`

类型：**PROVED_EXACT_NONNEGATIVE_WEIGHTED_GRAM_NO_DECAY_BOUND_PLUS_NUMERICALLY_CERTIFIED_FINITE_ADAPTIVE_WEIGHTING_OBSTRUCTION**。

TPC-290 承接 TPC-289 的 physical output Gram，把 adaptive shell weighting 写成
`R(w)=||sum_q w_q g_q||^2/sum_q w_q^2 d_q`，并定义 effective support
`kappa(w)=(sum_q w_q)^2/sum_q w_q^2`。严格证明 weighted Gram identity；若权重非负且
所有 cross-Gram entries 非负，则 `R(w)>=1`，在 `Gamma>=9/25` 与
`d_min/d_max>=4/5` 下进一步有 `R(w)>=1+(3/5)(4/5)(kappa(w)-1)`。

沿用 TPC-289 的 18-row grid，uniform、inverse-diagonal、linear-taper 三种 full-support
policies 共 54/54 amplified，18/18 leave-one-out minima 仍 amplified；所有 equal
two-prime supports 中恰有 3 个 subunit witnesses，全部来自早期 `(256,38,27,5,1)` 的
三个 negative pairs。因而 adaptive route 被严格拆成 diffuse positive branch 与 sparse
sign-flip escape：前者仍被 coherence wall 拦住，后者只在牺牲 full-shell support 后出现。

最强正结果是 exact effective-support coherence envelope 加 54/54 full-support finite
obstruction；最强负结果是 sparse equal-pair sign-flip escape，它 refute 了声明网格上
“所有 nonnegative supports 都不衰减”的无条件说法，但不构成 full-shell saving。growing
weighted theorem、source-uniform arithmetic `L2`、fixed-power credit 与 full Gate B 仍
OPEN/NONE。

```text
STRONGEST_POSITIVE_RESULT = EXACT_EFFECTIVE_SUPPORT_COHERENCE_ENVELOPE_PLUS_54_FULL_SUPPORT_POLICY_OBSTRUCTION
STRONGEST_OBSTRUCTION = THREE_SPARSE_NONNEGATIVE_EQUAL_PAIR_SUBUNIT_WITNESSES_IN_ONE_SIGN_FLIP_ROW
OPEN_THEOREM = GROWING_DIFFUSE_WEIGHTED_COHERENCE_OR_SOURCE_RESTRICTION
REUSABLE_STRUCTURE = WEIGHTED_GRAM -> EFFECTIVE_SUPPORT -> POSITIVE_BLOCK / SPARSE ESCAPE
ROUND2_CLUE = TEST_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_OR_SOURCE_RESTRICTED_DIFFUSE_WEIGHTS
```

```text
TPC290_ROUTE_ADVANCE = YES_SCOPED_EFFECTIVE_SUPPORT_WEIGHTED_GRAM_FIREWALL
TPC290_WEIGHTED_IDENTITY = PROVED_EXACT_FINITE
TPC290_NONNEGATIVE_NO_DECAY = PROVED_EXACT_CONDITIONAL
TPC290_DIFFUSE_ACCUMULATION_BOUND = PROVED_EXACT_CONDITIONAL
TPC290_FULL_SUPPORT_POLICY_SCAN = NUMERICALLY_CERTIFIED_FINITE_54_OF_54_AMPLIFIED
TPC290_SPARSE_SIGN_FLIP_ESCAPE = NUMERICALLY_CERTIFIED_FINITE_3_PAIRS_ONE_ROW
TPC290_DROP_ONE_SCAN = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_AMPLIFIED
TPC290_UNIFORM_NONNEGATIVE_NO_DECAY = REFUTED_FINITE_BY_SPARSE_SIGN_FLIP
TPC290_GROWING_WEIGHTED_THEOREM = OPEN
TPC290_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE
TPC290_FIXED_POWER_CREDIT = 0
TPC290_FULL_GATE_B = OPEN
TPC290_TWIN_PRIME_RESULT = NONE
TPC290_STATUS = PROVED_EXACT_NONNEGATIVE_WEIGHTED_GRAM_NO_DECAY_BOUND_PLUS_NUMERICALLY_CERTIFIED_FINITE_ADAPTIVE_WEIGHTING_OBSTRUCTION
```

## 0.83 当前：TPC-289 cross-prime Gram coherence

项目：`papers/tpc-289-cross-prime-gram-coherence/`

类型：**PROVED_EXACT_NORMALIZED_GRAM_COHERENCE_ACCUMULATION_BOUND_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGN_PHASE_DIAGRAM**。

TPC-289 承接 TPC-288 的 source-output Gram，在同一个 literal physical
deleted-diagonal operator 上定义
`Gamma_(q,r)=G_(q,r)^2/(G_(q,q)G_(r,r))`，严格证明 `0<=Gamma<=1` 以及在
positive coherence floor 与 diagonal balance 下的 conditional accumulation lower bound。
18 个 growth/exponent/control rows 共 1,380 个 unordered pair comparisons：17/18 rows
pairwise positive，但 `(256,38,27,5,1)` 的早期 `s=1` crossover 有 3 个精确 negative
pairs，其中 `(31,53)` 的 squared coherence 约 `1.3746e-7`；8 个 late-shell rows
满足 `eta=3/5, delta=4/5` strong block，18/18 rows 的 aggregate energy ratio 都大于 1。
六个 source-control rows 在两个 fixed heights 上形成两组相同的 recorded
coherence/energy signatures，提示有限 controls 不能直接当作独立 source family。

最强正结果是 exact conditional coherence-accumulation envelope 与 8-row late block；
最强 obstruction 是早期 sign flip/near-zero coherence，因而 refute 了声明网格上的
uniform pairwise positivity/coherence-floor shortcut。source-restricted/growing-shell
coherence、literal arithmetic `L2`、fixed-power credit 与 full Gate B 仍 OPEN/NONE。

```text
STRONGEST_POSITIVE_RESULT = EXACT_CONDITIONAL_COHERENCE_ACCUMULATION_ENVELOPE_PLUS_8_ROW_LATE_BLOCK
STRONGEST_OBSTRUCTION = THREE_EXACT_NEGATIVE_CROSS_PRIME_PAIRS_AND_NEAR_ZERO_COHERENCE_AT_N256_S1
OPEN_THEOREM = SOURCE_RESTRICTED_OR_GROWING_SHELL_COHERENCE_BOUND
REUSABLE_STRUCTURE = OUTPUT_GRAM -> SIGN_CENSUS -> NORMALIZED_COHERENCE -> CONDITIONAL_ENERGY_ENVELOPE
ROUND2_CLUE = TEST_ADAPTIVE_SHELL_WEIGHTING_OR_SOURCE_RESTRICTED_COHERENCE_BEYOND_FINITE_BLOCK
```

```text
TPC289_ROUTE_ADVANCE = YES_SCOPED_EXACT_COHERENCE_ENVELOPE_AND_FINITE_SIGN_PHASE_DIAGRAM
TPC289_EXACT_GRAM_COHERENCE = PROVED_EXACT_FINITE
TPC289_EXACT_ACCUMULATION_BOUND = PROVED_EXACT_CONDITIONAL
TPC289_PAIRWISE_POSITIVITY = NUMERICALLY_CERTIFIED_FINITE_17_OF_18_ROWS
TPC289_SIGN_FLIP_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_3_PAIRS_ONE_ROW
TPC289_STRONG_COHERENCE_BLOCK = NUMERICALLY_CERTIFIED_FINITE_8_ROWS
TPC289_ENERGY_AMPLIFIED = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ROWS
TPC289_TOTAL_PAIR_COMPARISONS = 1380
TPC289_CONTROL_EQUIVALENCE_GROUPS = 2
TPC289_UNIFORM_PAIRWISE_POSITIVITY = REFUTED_FINITE_DECLARED_GRID
TPC289_GROWING_COHERENCE_STABILITY = OPEN
TPC289_SOURCE_CONTROL_UNIFORMITY = OPEN
TPC289_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC289_FIXED_POWER_CREDIT = 0
TPC289_FULL_GATE_B = OPEN
TPC289_TWIN_PRIME_RESULT = NONE
TPC289_STATUS = PROVED_EXACT_NORMALIZED_GRAM_COHERENCE_ACCUMULATION_BOUND_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGN_PHASE_DIAGRAM
```

## 0.82 已发布：TPC-288 growing-shell Gram obstruction

项目：`papers/tpc-288-growing-shell-gram-obstruction/`

类型：**PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_SHELL_FULL_RANK_OBSTRUCTION**。

TPC-288 是 TPC-287 的直接增长/谱层追踪。保持同一个 literal physical
deleted-diagonal operator，把每个 prime component 的完整 output vector `g_q` 保留下来，
构造 `G_(q,r)=<g_q,g_r>`。finite operator/output/attachment additivity、Gram PSD 与
`1^T G 1=||g_shell||^2` 均严格证明。8 个 growth-path anchors 加 18 个 height/cutoff
controls 形成 34 rows，最大 shell 含 17 个素数；34/34 output Gram 通过模
`1000000007` 的 full-rank witness，6/6 selected aggregate physical active matrices 也
full rank。所有 34 行的 vector energy ratio `R_E=||g_shell||^2/sum_q||g_q||^2` 都大于
1，其中 13 行同时有 interval-certified scalar retention upper `R_C^+<1/10`。

这给出一个明确的 scalar-to-energy obstruction：小 scalar attachment 不能自动支付
physical `L2` saving；但它仍是有限证书，不是 uniform growing-shell theorem。最强正结果
是 source-output Gram 的 exact structure 与 finite positive spectrum；最强 obstruction
是 13 个 scalar cancellation / vector amplification 交集。可复用结构为
`prime components -> output Gram -> active rank -> scalar/energy firewall`。

```text
STRONGEST_POSITIVE_RESULT = EXACT_OUTPUT_GRAM_PSD_ENERGY_IDENTITY_PLUS_34_FULL_RANK_GRAMS
STRONGEST_OBSTRUCTION = 13_ROWS_SCALAR_RETENTION_LT_1/10_BUT_VECTOR_ENERGY_GT_1
OPEN_THEOREM = SOURCE_NATIVE_CROSS_PRIME_GRAM_BOUND_BEYOND_FINITE_FULL_RANK
REUSABLE_STRUCTURE = PRIME_COMPONENTS -> OUTPUT_GRAM -> ACTIVE_OPERATOR_RANK -> SCALAR_ENERGY_FIREWALL
ROUND2_CLUE = TEST_SOURCE_NATIVE_CROSS_PRIME_GRAM_BOUNDS_BEYOND_FINITE_FULL_RANK_OBSTRUCTION
```

```text
TPC288_ROUTE_ADVANCE = YES_SCOPED_GROWING_SHELL_GRAM_OBSTRUCTION_AND_FULL_RANK_AUDIT
TPC288_EXACT_OPERATOR_ADDITIVITY = PROVED_EXACT_FINITE
TPC288_EXACT_OUTPUT_GRAM_IDENTITY = PROVED_EXACT_FINITE
TPC288_GRAM_PSD = PROVED_EXACT_FINITE
TPC288_GRAM_FULL_RANK = NUMERICALLY_CERTIFIED_FINITE_34_OF_34
TPC288_OPERATOR_FULL_ACTIVE_RANK = NUMERICALLY_CERTIFIED_FINITE_6_OF_6_SELECTED
TPC288_SCALAR_ENERGY_MISMATCH = NUMERICALLY_CERTIFIED_FINITE_13_ROWS
TPC288_ENERGY_AMPLIFIED = NUMERICALLY_CERTIFIED_FINITE_34_OF_34
TPC288_MAX_SHELL_CARDINALITY = 17
TPC288_GROWING_SHELL_STABILITY = OPEN
TPC288_SOURCE_CONTROL_UNIFORMITY = OPEN
TPC288_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC288_FIXED_POWER_CREDIT = 0
TPC288_FULL_GATE_B = OPEN
TPC288_TWIN_PRIME_RESULT = NONE
TPC288_STATUS = PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_SHELL_FULL_RANK_OBSTRUCTION
```

## 0.81 已发布：TPC-287 prime-shell cancellation depth

项目：`papers/tpc-287-prime-shell-cancellation-depth/`

类型：**PROVED_EXACT_FINITE_SHELL_ADDITIVE_ATTACHMENT_DECOMPOSITION_PLUS_NUMERICALLY_CERTIFIED_FINITE_CANCELLATION_DEPTH_LEDGER**。

TPC-287 承接 TPC-286 的 diagonal-deletion ledger，把 physical deleted-diagonal prime
shell 按素数拆成 `g_q`，并严格证明 finite shell 的 `g_shell=sum_q g_q` 与 linear
attachment 的 `C_shell=sum_q C_q`。同时给出 component-separated interval 下的
conditional retention envelope。七个声明的 shell anchors 分别含 1--7 个素数；与六个
frozen source baselines、两个 kernel exponents 组合成 84 rows / 336 components。
所有 component intervals 均 sign-separated，57 行 mixed-sign；retention upper 小于
`1/2`、`1/4`、`1/10` 的行数为 31/22/8，另有 5 行小于 `1/20`。leave-one-prime-out
产生 48 个非零 sign flips、12 个 zero remainders、276 个 same-sign events。

最强正结果是 exact prime-component/additivity structure 与可复用的 interval retention
envelope；最强 obstruction 是有限抵消依赖 shell anchor 与 source control，无法自动
提升为 growing-shell cancellation theorem。可复用结构为
`physical shell -> prime components -> signed sum -> retention envelope -> leave-one-out`。
这篇论文明确记录 `ROUND2_CLUE`：测试 growing shell 与 source controls 的抵消稳定性；
literal arithmetic `L2`、fixed-power credit 与 full Gate B 仍 open。

```text
STRONGEST_POSITIVE_RESULT = EXACT_FINITE_SHELL_AND_LINEAR_ATTACHMENT_ADDITIVITY_PLUS_57_MIXED_SIGN_ROWS
STRONGEST_OBSTRUCTION = FINITE_CANCELLATION_IS_SHELL_AND_SOURCE_CONTROL_DEPENDENT
OPEN_THEOREM = GROWING_SHELL_AND_SOURCE_CONTROL_CANCELLATION_STABILITY
REUSABLE_STRUCTURE = PRIME_COMPONENTS -> SIGNED SUM -> RETENTION ENVELOPE -> LEAVE_ONE_OUT
ROUND2_CLUE = TEST_CANCELLATION_STABILITY_UNDER_GROWING_SHELL_AND_SOURCE_CONTROLS
```

```text
TPC287_ROUTE_ADVANCE = YES_SCOPED_PRIME_COMPONENT_LEDGER_AND_FINITE_CANCELLATION_DEPTH
TPC287_SHELL_ADDITIVITY = PROVED_EXACT_FINITE
TPC287_ATTACHMENT_ADDITIVITY = PROVED_EXACT_FINITE
TPC287_RETENTION_ENVELOPE = PROVED_CONDITIONAL_INTERVAL
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
TPC287_STATUS = PROVED_EXACT_FINITE_SHELL_ADDITIVE_ATTACHMENT_DECOMPOSITION_PLUS_NUMERICALLY_CERTIFIED_FINITE_CANCELLATION_DEPTH_LEDGER
```

## 0.80 已发布：TPC-286 diagonal-deletion attachment ledger

项目：`papers/tpc-286-diagonal-deletion-attachment-ledger/`

类型：**PROVED_EXACT_LINEAR_DIAGONAL_DELETION_ATTACHMENT_SPLIT_PLUS_NUMERICALLY_CERTIFIED_FINITE_DIAGONAL_SENSITIVITY_LEDGER**。

TPC-286 承接 TPC-285，将 centered residue block 的 diagonal-including output、显式
diagonal correction 与 physical deleted-diagonal output 分开。对任意声明的有限 shell，
精确证明 `g_phys=g_full-g_diag`，其中
`g_diag(u)=sum_q q K_H(0)(q-2)/(q-1)m_q(u)beta(u)`；对四-block linear attachment
进一步有 `C_phys=C_full-C_diag`。在 TPC-284 的全部 72 个 controls 上，三类 component
interval 全部 sign-separated：full 为 49 negative/23 positive，diagonal 为 34/38，
physical 为 60/12；full-versus-physical 有 15 个 sign flips，对角修正与 physical
相反 30 行，严格大于 physical 绝对幅度 21 行，ratio lower bound 超过 2/10 的行数为
13/4。

最强正结果是 exact operator/attachment diagonal split；最强 obstruction 是 finite
diagonal sensitivity can reverse or dominate the physical attachment。该 ledger 不提供
asymptotic diagonal dominance、signed full-shell cancellation 或 arithmetic `L2`，这些
仍是 open。可复用结构为 `centered block -> diagonal correction -> physical ledger`。

```text
STRONGEST_POSITIVE_RESULT = EXACT_OPERATOR_AND_ATTACHMENT_DIAGONAL_SPLIT
STRONGEST_OBSTRUCTION = FINITE_DIAGONAL_SENSITIVITY_WITH_15_FULL_PHYSICAL_SIGN_FLIPS
OPEN_THEOREM = SIGNED_FULL_SHELL_CANCELLATION_AFTER_DIAGONAL_SPLIT
REUSABLE_STRUCTURE = CENTERED_RESIDUE_BLOCK -> DIAGONAL_CORRECTION -> PHYSICAL_LEDGER
ROUND2_CLUE = SEEK_SIGNED_FULL_SHELL_CANCELLATION_AFTER_DIAGONAL_ATTACHMENT_LEDGER
```

```text
TPC286_ROUTE_ADVANCE = YES_SCOPED_EXACT_DIAGONAL_SPLIT_AND_FINITE_SENSITIVITY_LEDGER
TPC286_ATTACHMENT_SPLIT = PROVED_EXACT_LINEARITY
TPC286_COMPONENT_SIGN_LEDGER = NUMERICALLY_CERTIFIED_FINITE_72_ROWS
TPC286_FULL_VS_PHYSICAL_FLIPS = NUMERICALLY_CERTIFIED_FINITE_15_ROWS
TPC286_DIAGONAL_OPPOSITION = NUMERICALLY_CERTIFIED_FINITE_30_ROWS
TPC286_DIAGONAL_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_21_ROWS
TPC286_ASYMPTOTIC_DIAGONAL_DOMINANCE = OPEN
TPC286_SIGNED_FULL_SHELL_CANCELLATION = OPEN
TPC286_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC286_FIXED_POWER_CREDIT = 0
TPC286_FULL_GATE_B = OPEN
TPC286_TWIN_PRIME_RESULT = NONE
TPC286_STATUS = PROVED_EXACT_LINEAR_DIAGONAL_DELETION_ATTACHMENT_SPLIT_PLUS_NUMERICALLY_CERTIFIED_FINITE_DIAGONAL_SENSITIVITY_LEDGER
```

## 0.79 已发布：TPC-285 prime-shell residue factorization and deleted-diagonal rank obstruction

项目：`papers/tpc-285-prime-shell-residue-rank-obstruction/`

类型：**PROVED_EXACT_CENTERED_RESIDUE_FACTORIZATION_AND_DELETED_DIAGONAL_FULL_RANK_PLUS_NUMERICALLY_CERTIFIED_KERNEL_RANK**。

TPC-285 承接 TPC-284 的 72-row control atlas，抽出每个 prime-shell residue block 的
精确结构。对奇素数 `q`，令 `R_q` 为 nonzero residue indicators，则
`B_q=R_q(I-11^T/(q-1))R_q^T`，rank 至多 `q-2`，full class coverage 时恰为 `q-2`。
物理矩阵使用 deleted diagonal `D_q=B_q-diag(B_q)`；按 within-class zero-sum 与
block-constant 子空间分解，matrix-determinant-lemma 因子严格非零，故 `D_q` 在
active coordinates 上 full rank。20 个 registered `(X,H,Q,s,q)` rows 的 kernel Schur
blocks 又由模 `1000000007` 的独立 witness 认证 full active rational rank。

最强正结果是 exact deleted-diagonal full-rank theorem；最强 obstruction 是 centered
`q-2` low-rank shortcut 不经过 physical diagonal deletion。该 obstruction 不否定
signed cross-prime cancellation、singular-value decay 或 arithmetic `L2`，它们仍是
open。可复用结构为 `residue factor -> diagonal split -> class subspaces`。

```text
STRONGEST_POSITIVE_RESULT = EXACT_DELETED_DIAGONAL_FULL_ACTIVE_RANK_THEOREM
STRONGEST_OBSTRUCTION = CENTERED_Q_MINUS_2_RANK_DOES_NOT_SURVIVE_PHYSICAL_DIAGONAL_DELETION
OPEN_THEOREM = SIGNED_FULL_SHELL_SPECTRAL_OR_L2_BOUND_USING_MORE_THAN_RANK
REUSABLE_STRUCTURE = RESIDUE_FACTOR -> DIAGONAL_SPLIT -> CLASS_SUBSPACE_DECOMPOSITION
ROUND2_CLUE = SEPARATE_RESIDUE_MODE_FACTORIZATION_FROM_DELETED_DIAGONAL_AND_KERNEL_RANK_BEFORE_LITERAL_L2
```

```text
TPC285_ROUTE_ADVANCE = YES_SCOPED_EXACT_RESIDUE_FACTORIZATION_AND_RANK_OBSTRUCTION
TPC285_RESIDUE_FACTORIZATION = PROVED_EXACT
TPC285_CENTERED_RANK_BOUND = PROVED_EXACT_RANK_LE_Q_MINUS_2
TPC285_DELETED_DIAGONAL_FULL_RANK = PROVED_EXACT_UNDER_FULL_CLASS_COVERAGE
TPC285_KERNEL_SCHUR_FULL_RANK = NUMERICALLY_CERTIFIED_FINITE_20_ROWS
TPC285_LOW_RANK_TRANSFER = REFUTED_AS_DIRECT_SHORTCUT
TPC285_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC285_FIXED_POWER_CREDIT = 0
TPC285_FULL_GATE_B = OPEN
TPC285_TWIN_PRIME_RESULT = NONE
TPC285_STATUS = PROVED_EXACT_CENTERED_RESIDUE_FACTORIZATION_AND_DELETED_DIAGONAL_FULL_RANK_PLUS_NUMERICALLY_CERTIFIED_KERNEL_RANK
```

## 0.78 已发布：TPC-284 finite admissible source-control atlas

项目：`papers/tpc-284-admissible-source-control-atlas/`

类型：**NUMERICALLY_CERTIFIED_FINITE_ADMISSIBLE_CONTROL_ATLAS_PLUS_SIGN_FLIP_OBSTRUCTION**。

TPC-284 承接 TPC-283 的 unrestricted zeroing-radius obstruction，声明六类局部
schedule controls：`H-2/H+2`、`z-1/z+1`、`Q-1/Q+1`。六个 registered baseline
tuples、两个 kernel exponents 与六类 controls 组成 72-row literal-source atlas。
Hash-locked TPC-268 replay 与独立重放均认证所有行的 attachment interval 与零分离：
60 个 negative、12 个 positive、0 个 crossing；相对 TPC-283 baseline 有 8 个 sign
flips。最弱 controlled `rho^2` 下界约为 `1.4118e-5`，最大 upper endpoint 约为
`0.1539`。

最强正结果是一个可复核的有限 source-control atlas；最强 obstruction 是 named
controls 下的 8 个 orientation flips，说明 finite non-vanishing 不能替代 sign
stability。开放定理是明确 source class 上的 growing-schedule stability 与
arithmetic `L2`；六类 controls 不声称 exhaustive。可复用结构为
`hashed baseline -> declared control map -> interval sign census`。

```text
STRONGEST_POSITIVE_RESULT = FINITE_72_ROW_LITERAL_SOURCE_CONTROL_ATLAS
STRONGEST_OBSTRUCTION = 8_BASELINE_SIGN_FLIPS_UNDER_DECLARED_CONTROLS
OPEN_THEOREM = GROWING_SCHEDULE_CONTROL_STABILITY_WITH_DECLARED_SOURCE_CLASS
REUSABLE_STRUCTURE = HASHED_BASELINE -> CONTROL_MAP -> EXACT_INTERVAL_CENSUS
ROUND2_CLUE = COMPILE_PRIME_SHELL_CONTROL_CONSTRAINTS_BEFORE_ANY_ASYMPTOTIC_STABILITY_CLAIM
```

```text
TPC284_ROUTE_ADVANCE = YES_SCOPED_FINITE_CONTROL_ATLAS_AND_SIGN_FLIP_OBSTRUCTION
TPC284_CONTROL_ATLAS = NUMERICALLY_CERTIFIED_FINITE_72_ROWS
TPC284_CONTROL_SIGN_CENSUS = 60_NEGATIVE_12_POSITIVE_0_CROSSING
TPC284_SIGN_FLIP_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_8_FLIPS
TPC284_ASYMPTOTIC_CONTROL_STABILITY = OPEN
TPC284_LITERAL_SOURCE_CLASS_THEOREM = OPEN
TPC284_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC284_FIXED_POWER_CREDIT = 0
TPC284_FULL_GATE_B = OPEN
TPC284_TWIN_PRIME_RESULT = NONE
TPC284_STATUS = NUMERICALLY_CERTIFIED_FINITE_ADMISSIBLE_CONTROL_ATLAS_PLUS_SIGN_FLIP_OBSTRUCTION
```

## 0.77 已发布：TPC-283 source-attachment stability radius and adversarial zeroing

项目：`papers/tpc-283-source-attachment-stability-radius/`

类型：**PROVED_EXACT_HILBERT_SOURCE_ZEROING_RADIUS_PLUS_NUMERICALLY_CERTIFIED_FINITE_VULNERABILITY_AUDIT**。

TPC-283 承接 TPC-282。对非零 projected output `S`、source representative `w`，令
`C=<w,S>`、`W=||w||^2`、`Y=||S||^2`，精确证明最近 zero-attachment source 为
`w-(C/Y)S`，且相对平方距离为 `C^2/(WY)`。将 TPC-282 的 12 个 actual-source
interval 转移后，所有行的相对归零半径严格小于 `3/10`，其中 6 行严格小于 `1/10`。

最强正结果是一个无需有限维假设的 Hilbert-space zeroing theorem；最强 obstruction
是 unrestricted source direction 的低稳定半径。该方向未证明保持 prime shell、cutoff
或 Möbius source class，因此只能标为 information-model adversary；admissible literal
source stability、arithmetic `L2` 与 full Gate B 仍 open。可复用结构为
`attachment -> zero hyperplane distance -> radius budget`。

```text
STRONGEST_POSITIVE_RESULT = EXACT_HILBERT_DISTANCE_TO_ZERO_ATTACHMENT
STRONGEST_OBSTRUCTION = ALL_12_ROWS_ZEROABLE_WITHIN_30_PERCENT_INFORMATION_MODEL
OPEN_THEOREM = ADMISSIBLE_LITERAL_SOURCE_STABILITY
REUSABLE_STRUCTURE = ATTACHMENT_C -> HYPERPLANE_DISTANCE -> RADIUS_BUDGET
ROUND2_CLUE = TEST_ADMISSIBLE_LITERAL_SOURCE_CONTROLS_AFTER_UNRESTRICTED_ZEROING_OBSTRUCTION
```

```text
TPC283_ROUTE_ADVANCE = YES_SCOPED_EXACT_ZEROING_RADIUS_AND_FINITE_VULNERABILITY_AUDIT
TPC283_ZEROING_RADIUS = PROVED_EXACT
TPC283_FINITE_VULNERABILITY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC283_UNRESTRICTED_ADVERSARY = INFORMATION_MODEL_ONLY
TPC283_ADMISSIBLE_LITERAL_SOURCE_STABILITY = OPEN
TPC283_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC283_FIXED_POWER_CREDIT = 0
TPC283_FULL_GATE_B = OPEN
TPC283_TWIN_PRIME_RESULT = NONE
TPC283_STATUS = PROVED_EXACT_HILBERT_SOURCE_ZEROING_RADIUS_PLUS_NUMERICALLY_CERTIFIED_FINITE_VULNERABILITY_AUDIT
```

## 0.76 已发布：TPC-282 literal source attachment and finite source-lock audit

项目：`papers/tpc-282-literal-source-attachment-audit/`

类型：**NUMERICALLY_CERTIFIED_FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK_PLUS_ASYMPTOTIC_NONDEGENERACY_OPEN**。

TPC-282 承接 TPC-281，将 typed attachment 的抽象缺口放回实际的 frozen literal V59
source。令 `S=(I-P_3)A beta`、`w_perp=(I-P_3)w`、`C=<w_perp,S>`，并以
`rho^2=C^2/(||w_perp||^2||S||^2)` 量化附着。六个 registered growing-cutoff scales
与两个 kernel exponents 的 12 行均由 outward intervals 重放并与 TPC-275 signed output
绑定：11 行 `C<0`、1 行 `C>0`、0 行 crossing zero；最弱行 `(256,38,6,2)` 的
`rho^2` 下界约为 `3.36e-5`。这是真实 source readout 的有限锁定，不是渐近统一下界。

最强正结果是 actual source attachment 在当前 12 行均非零；最强 obstruction 是弱
归一化附着与一次符号翻转。开放定理是同一 growing schedule 上的 uniform source
nondegeneracy，另有 literal arithmetic `L2` 未支付。可复用结构为
`projected source/output -> C,W,Y -> normalized attachment`。

```text
STRONGEST_POSITIVE_RESULT = ACTUAL_LITERAL_SOURCE_ATTACHMENT_LOCKED_AND_NONZERO_ON_12_ROWS
STRONGEST_OBSTRUCTION = WEAKEST_RHO_SQUARED_ABOUT_3.36E-5_AND_ONE_SIGN_FLIP
OPEN_THEOREM = UNIFORM_ASYMPTOTIC_SOURCE_ATTACHMENT_NONDEGENERACY
REUSABLE_STRUCTURE = PROJECT_SOURCE_AND_OUTPUT -> C,W,Y -> NORMALIZED_ATTACHMENT
ROUND2_CLUE = QUANTIFY_SOURCE_ATTACHMENT_STABILITY_RADIUS_AND_SIGN_FLIPS
```

```text
TPC282_ROUTE_ADVANCE = YES_SCOPED_FINITE_SOURCE_ATTACHMENT_AUDIT
TPC282_SOURCE_ATTACHMENT = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC282_SOURCE_SIGN = 11_NEGATIVE_1_POSITIVE_FINITE
TPC282_UNIFORM_ASYMPTOTIC_NONDEGENERACY = OPEN
TPC282_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC282_FIXED_POWER_CREDIT = 0
TPC282_FULL_GATE_B = OPEN
TPC282_TWIN_PRIME_RESULT = NONE
TPC282_STATUS = NUMERICALLY_CERTIFIED_FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK_PLUS_ASYMPTOTIC_NONDEGENERACY_OPEN
```

## 0.75 已发布：TPC-281 typed arithmetic `L2` / Gate-B interface audit

项目：`papers/tpc-281-arithmetic-l2-gate-b-interface-audit/`

类型：**PROVED_EXACT_TYPED_ARITHMETIC_L2_INTERFACE_FIREWALL_PLUS_NUMERICALLY_CERTIFIED_ATTACHMENT_AUDIT**。

TPC-281 承接 TPC-280 的 two-term gain compiler，把下一步所需的 arithmetic `L2` 写成
明确的 typed hypothesis：`A_X:H_X -> ell^2(I_X)` 且
`||A_X||_(2->2)<=K X^(-sigma)`。对四个 packet 的
`S=sum V_j`、`D=sum||V_j||^2`、`G=||S||^2`，若 `G/D<=Q_X`、`D<=d_+X^a`，则由
operator contraction 精确得到
`||A_XS||_2^2<=K^2X^(-2sigma)Q_XD`；接入 TPC-280 的
`Q_X<=(B+ell/d)X^(-kappa)` 后得到 collapsed exponent `a-2sigma-kappa`。
scalar readout 只再使用 dual-norm contraction。

同时，TPC-281 给出一个 exact attachment firewall：对同一个非零
`S=(S_1,S_2)`，`u_parallel=S` 与 `u_perp=(-S_2,S_1)` 代表的 rank-one functionals
具有相同 operator norm，但 attachment squared 分别为 `G^2` 与 `0`。因此 packet
geometry 加 `L2` norm 不能自动识别 arithmetic attachment，必须另有 typed
nondegeneracy/source-identification theorem。4 个 exact packet fixtures、4 个
interface cases 与 TPC-280 全部 12 行 transfer 均通过 independent/stress/Bridge-B
checks；literal source arithmetic `L2`、typed attachment、fixed-power credit、full Gate B
与 twin-prime conclusion 仍 OPEN/NONE。

```text
STRONGEST_POSITIVE_RESULT = EXACT_TYPED_ARITHMETIC_L2_TO_GATE_B_OUTPUT_INTERFACE
STRONGEST_OBSTRUCTION = EQUAL_NORM_ORTHOGONAL_ATTACHMENT_CAN_BE_ZERO
OPEN_THEOREM = LITERAL_SOURCE_ARITHMETIC_L2_PLUS_TYPED_ATTACHMENT_NONDEGENERACY
REUSABLE_STRUCTURE = PACKET_GEOMETRY -> TYPED_L2 -> OUTPUT_ENERGY -> SCALAR_READOUT
ROUND2_CLUE = REQUIRE_LITERAL_SOURCE_ARITHMETIC_L2_AND_TYPED_ATTACHMENT_NONDEGENERACY
```

```text
TPC281_MAXIMUM_CLAIM = PROVED_EXACT_TYPED_ARITHMETIC_L2_INTERFACE_FIREWALL_PLUS_NUMERICALLY_CERTIFIED_ATTACHMENT_AUDIT
TPC281_ROUTE_ADVANCE = YES_SCOPED_TYPED_ARITHMETIC_L2_GATE_B_INTERFACE_AUDIT
TPC281_TYPED_ARITHMETIC_L2 = PROVED_CONDITIONAL_INTERFACE_ONLY
TPC281_ATTACHMENT_IDENTIFIABILITY = REFUTED_EXACT_BY_ORTHOGONAL_FUNCTIONAL
TPC281_FINITE_ATTACHMENT_AUDIT = NUMERICALLY_CERTIFIED_FINITE_4_PACKET_FIXTURES
TPC281_FINITE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC281_ARITHMETIC_ADVANCE = NO
TPC281_L2 = OPEN_LITERAL_SOURCE
TPC281_FIXED_POWER_CREDIT = 0
TPC281_FULL_GATE_B = OPEN
TPC281_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC281_TWIN_PRIME_RESULT = NONE
TPC281_STATUS = PROVED_EXACT_TYPED_ARITHMETIC_L2_INTERFACE_FIREWALL_PLUS_NUMERICALLY_CERTIFIED_ATTACHMENT_AUDIT
TPC281_ROUND2_CLUE = REQUIRE_LITERAL_SOURCE_ARITHMETIC_L2_AND_TYPED_ATTACHMENT_NONDEGENERACY
```

## 0.74 已发布：TPC-280 additive-leakage-aware gain and endpoint compiler

项目：`papers/tpc-280-leakage-aware-endpoint-compiler/`

类型：**PROVED_CONDITIONAL_TWO_TERM_LEAKAGE_ENDPOINT_COMPILER_PLUS_NUMERICALLY_CERTIFIED_TRANSFER**。

TPC-280 承接 TPC-279 的 exact deficit criterion，处理 source bound 中同时存在的
multiplicative main term 与 additive leakage。若 `D>=dX^a` 且
`G<=B X^(-gamma)D+ell X^(a-delta)`，精确归一化为
`G/D<=B X^(-gamma)+(ell/d)X^(-delta)`，从而得到 two-term reciprocal gain bound。
令 `kappa=min(gamma,delta)`，可进一步编译为
`D/G>=(B+ell/d)^(-1)X^kappa`，并通过 TPC-279 的
`m^2=(D/G)m_D^2` 接回 `eta_eff=max(0,eta_D-kappa/2)` 与 strict
`sigma-eta_eff>1/400` endpoint budget。

形式 equality family `D=dX^a`、`G=BX^(-gamma)D+ell X^(a-delta)` 证明 two-term
denominator 在该信息模型下 sharp；当 `delta<gamma` 且 `ell>0` 时，慢 leakage
是不可绕过的 exponent bottleneck。6 个 budget、4 个 margin、4 个 endpoint
exact rational fixtures，以及 TPC-279 的 12-row coordinate transfer 均通过
independent/stress/bridge checks。该结果仍是 conditional compiler，不提供 literal
source decomposition、arithmetic `L2`、fixed-power credit 或 twin-prime conclusion。

```text
STRONGEST_POSITIVE_RESULT = EXACT_TWO_TERM_ADDITIVE_LEAKAGE_GAIN_AND_MARGIN_COMPILER
STRONGEST_OBSTRUCTION = SLOWER_LEAKAGE_EXPONENT_CAPS_THE_GAIN_EXPONENT
OPEN_THEOREM = LITERAL_GROWING_SOURCE_DECOMPOSITION_WITH_ARITHMETIC_L2
REUSABLE_STRUCTURE = SOURCE_FLOOR -> NORMALIZE_TWO_TERMS -> DOMINANT_EXPONENT -> ENDPOINT_BUDGET
ROUND2_CLUE = AUDIT_TYPED_ARITHMETIC_L2_INTERFACE_FOR_FULL_GATE_B
```

```text
TPC280_ROUTE_ADVANCE = YES_SCOPED_ADDITIVE_LEAKAGE_ENDPOINT_COMPILER
TPC280_TWO_TERM_COMPILER = PROVED_CONDITIONAL
TPC280_DOMINANT_EXPONENT = PROVED_KAPPA_EQUALS_MIN_GAMMA_DELTA
TPC280_MARGIN_COMPILER = PROVED_CONDITIONAL_ETA_EFF_EQUALS_MAX_ZERO_ETA_D_MINUS_KAPPA_OVER_2
TPC280_LEAKAGE_BOTTLENECK = PROVED_CONDITIONAL_DELTA_LT_GAMMA
TPC280_SHARPNESS = PROVED_CONDITIONAL_EQUALITY_FAMILY
TPC280_FINITE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC280_FIXED_POWER_CREDIT = 0
TPC280_ARITHMETIC_ADVANCE = NO
TPC280_L2 = NONE
TPC280_FULL_GATE_B = OPEN
TPC280_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC280_TWIN_PRIME_RESULT = NONE
TPC280_STATUS = PROVED_CONDITIONAL_TWO_TERM_LEAKAGE_ENDPOINT_COMPILER_PLUS_NUMERICALLY_CERTIFIED_TRANSFER
```

## 0.73 已发布：TPC-279 minimal coherence-to-gain criterion and finite coordinate transfer

项目：`papers/tpc-279-coherence-to-gain-theorem/`

类型：**PROVED_EXACT_MINIMAL_COHERENCE_TO_GAIN_CRITERION_PLUS_NUMERICALLY_CERTIFIED_TRANSFER**。

TPC-279 承接 TPC-278 暴露的 signed-gain 稳定性缺口，但只研究其最小 source-level
interface。对四个 Hilbert-space packets 定义 `D=sum||V_j||^2`、`G=||sum V_j||^2`、
`q=G/D`、`Delta=1-q` 与 `r=D/G`，精确证明
`r>=b X^gamma` 当且仅当 `q<=b^(-1)X^(-gamma)`，也当且仅当
`Delta>=1-b^(-1)X^(-gamma)`。这给出 power gain 所需 source input 的必要且充分
形式，而不隐藏 normalization。

进一步，令 `mu` 为 pairwise absolute coherence，证明 sharp envelope
`G<=D+2mu sum_{j<k}||V_j||||V_k||<=(1+3mu)D`，与四包 universal bound 合并为
`q<=min(4,1+3mu)`。equicorrelation Gram family 对每个 `mu in [0,1]` 达到等号；
正交包说明 coherence alone 不能支付正幂，`(1,1,1,-(3-epsilon))` scalar family
说明即使 `mu=1` 也可产生 arbitrarily large gain。该 sharp theorem 是 reusable
structural result，但不是 literal growing source estimate。

TPC-278 的 12 个 outward gain intervals 经过 exact reciprocal transform，并与独立
存储的 cancellation intervals 取 certified intersection，得到 8 个 positive-deficit
与 4 个 negative-deficit rows；这是有限坐标 transfer，不升级为 asymptotic theorem。
arithmetic `L2`、full Gate B、strict endpoint payment 与 twin-prime conclusion 仍为
OPEN/OPEN/UNPAID/NONE。

```text
STRONGEST_POSITIVE_RESULT = EXACT_MINIMAL_DEFICIT_CRITERION_PLUS_SHARP_COHERENCE_ENVELOPE
STRONGEST_OBSTRUCTION = PAIRWISE_ABSOLUTE_COHERENCE_CANNOT_PAY_POSITIVE_POWER
OPEN_THEOREM = GROWING_SOURCE_LEVEL_DEFICIT_BOUND_FOR_G_OVER_D
REUSABLE_STRUCTURE = D,G,E -> q,Delta,r -> NECESSARY_AND_SUFFICIENT_GAIN_INPUT
ROUND2_CLUE = COMPILE_ADDITIVE_LEAKAGE_INTO_SOURCE_TO_MARGIN_ENDPOINT_BUDGET
```

```text
TPC279_ROUTE_ADVANCE = YES_SCOPED_EXACT_COHERENCE_TO_GAIN_CRITERION
TPC279_EXACT_DEFICIT_IDENTITY = PROVED_EXACT_FINITE
TPC279_PAIRWISE_COHERENCE_ENVELOPE = PROVED_EXACT_SHARP
TPC279_PAIRWISE_COHERENCE_POWER = REFUTED_EXACT_BY_ORTHOGONAL_WITNESS
TPC279_NEAR_CANCELLATION_ADVERSARY = PROVED_EXACT_SCALAR_FAMILY
TPC279_FINITE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC279_FINITE_TRANSFER_CENSUS = 8_POSITIVE_DEFICIT_4_NEGATIVE_DEFICIT
TPC279_SOURCE_LEVEL_DEFICIT = OPEN_ASYMPTOTIC
TPC279_FIXED_POWER_CREDIT = 0
TPC279_ARITHMETIC_ADVANCE = NO
TPC279_L2 = NONE
TPC279_FULL_GATE_B = OPEN
TPC279_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC279_TWIN_PRIME_RESULT = NONE
TPC279_STATUS = PROVED_EXACT_MINIMAL_COHERENCE_TO_GAIN_CRITERION_PLUS_NUMERICALLY_CERTIFIED_TRANSFER
```

## 0.72 已发布：TPC-278 cross-scale signed-gain stability and shell/clock counterexample

项目：`papers/tpc-278-cross-scale-gain-stability/`

类型：**NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_GAIN_STABILITY_OBSTRUCTION**。

TPC-278 冻结 TPC-277 的 literal source、beta、masks、deleted diagonal、四个实际
packets、rank-three Haar projection 与 `s=2`，只改变有限 prime-shell endpoint `Q`
或 clock `H`。对 12 个精确有理数 rows，`G-D=2E` 给出 8 个 negative-cross 与
4 个 positive-cross cases，并认证三条 shell sign-flip paths 与一条 clock sign-flip
path。三个不变 natural controls 与 TPC-277 hash-locked rows 精确一致。

因此 finite shortcut `D/G>=1` 在声明的邻近 Q/H 接口上被 scoped 否定；这个结论
既不是 intended growing schedule 的渐近反例，也不提供 fixed-power credit。
真正的下一输入必须是对精确 source schedule 的 coherence/deficit theorem。
arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍为 OPEN/OPEN/NONE。

```text
STRONGEST_POSITIVE_RESULT = EXACT_12_ROW_SOURCE_CENSUS_WITH_FOUR_DECLARED_SIGN_FLIPS
STRONGEST_OBSTRUCTION = NEARBY_SHELL_OR_CLOCK_CHOICE_CAN_REVERSE_SIGNED_GAIN
OPEN_THEOREM = SCHEDULE_SPECIFIC_SOURCE_LEVEL_G_OVER_D_DEFICIT_BOUND
REUSABLE_STRUCTURE = EXACT_SOURCE_REPLAY -> CROSS_SIGN_CENSUS -> STABILITY_FIREWALL
ROUND2_CLUE = FORMULATE_MINIMAL_SOURCE_LEVEL_COHERENCE_TO_GAIN_THEOREM
```

```text
TPC278_ROUTE_ADVANCE = YES_SCOPED_SIGNED_GAIN_STABILITY_OBSTRUCTION
TPC278_LITERAL_SOURCE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC278_NATURAL_CONTROLS = NUMERICALLY_CERTIFIED_FINITE_3_ROWS
TPC278_SHELL_CLOCK_FLIPS = NUMERICALLY_CERTIFIED_FINITE_4_FLIPS
TPC278_SIGNED_GAIN_STABILITY = REFUTED_SCOPED_FINITE
TPC278_SOURCE_LEVEL_UNIFORMITY = OPEN_ASYMPTOTIC
TPC278_FIXED_POWER_CREDIT = 0
TPC278_ARITHMETIC_ADVANCE = NO
TPC278_L2 = NONE
TPC278_FULL_GATE_B = OPEN
TPC278_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC278_TWIN_PRIME_RESULT = NONE
TPC278_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_GAIN_STABILITY_OBSTRUCTION
```

## 0.71 已发布：TPC-277 four-packet gain floor and source-level lower-bound attack

项目：`papers/tpc-277-four-packet-gain-floor/`

类型：**PROVED_EXACT_UNIVERSAL_FOUR_PACKET_GAIN_FLOOR_PLUS_NUMERICALLY_CERTIFIED_SOURCE_SCAN**。

TPC-277 直接攻击 TPC-276 留下的 source-level signed-gain 问题。对四个实际 packet
vectors 定义 `D=sum||V_j||^2`、`G=||sum V_j||^2` 与
`E=sum_{j<k} Re<V_j,V_k>`，精确证明 `G<=4D`、`D/G>=1/4`，并在 `E<=0` 时得到
`D/G>=1`。新的 cancellation coordinate
`kappa=(D-G)/D` 满足 `r=D/G=(1-kappa)^(-1)`，因此任何正幂 gain 都要求
`G/D` 有 quantified near-cancellation，而不是只要求 cross term 为负。

同一 literal TPC source 在 `s=2` 的 8 个 registered/extended rows 上以 exact
matrix-free rational replay 认证 `E<0`、`r>1` 全部成立；其中 `N=192` 行的
`r<101/100`，并且跨尺度不单调。这是有限 source diagnostic 与 one-percent
floor 的 scoped obstruction，不是渐近反例；fixed-power credit、arithmetic `L2`、
full Gate B 与 twin-prime conclusion 仍为 0/OPEN/NONE。

```text
STRONGEST_POSITIVE_RESULT = SHARP_FOUR_PACKET_GEOMETRIC_FLOOR_PLUS_EXACT_8_ROW_SOURCE_SCAN
STRONGEST_OBSTRUCTION = GEOMETRY_ALONE_HAS_NO_POSITIVE_POWER; ONE_PERCENT_FLOOR_REFUTED_SCOPED
OPEN_THEOREM = UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_OR_G_OVER_D_DEFICIT_BOUND
REUSABLE_STRUCTURE = D,G,E -> kappa -> r=(1-kappa)^(-1) -> endpoint input
ROUND2_CLUE = TEST_CROSS_SCALE_SIGNED_GAIN_STABILITY_AND_SHELL_SENSITIVITY
```

```text
TPC277_ROUTE_ADVANCE = YES_SCOPED_SOURCE_GAIN_FLOOR_AND_FINITE_ATTACK
TPC277_UNIVERSAL_FOUR_PACKET_FLOOR = PROVED_EXACT_R>=1_OVER_4
TPC277_NONPOSITIVE_CROSS_FLOOR = PROVED_CONDITIONAL_R>=1
TPC277_CANCELLATION_COORDINATE = PROVED_EXACT_r=(1-kappa)^(-1)
TPC277_GEOMETRIC_POWER_PROMOTION = REFUTED_EXACT_BY_ORTHOGONAL_ADVERSARY
TPC277_SOURCE_SCAN = NUMERICALLY_CERTIFIED_FINITE_ALL_8_ROWS
TPC277_ONE_PERCENT_FLOOR = REFUTED_SCOPED_FINITE
TPC277_SOURCE_LEVEL_POWER_GAIN = OPEN_ASYMPTOTIC
TPC277_FIXED_POWER_CREDIT = 0
TPC277_ARITHMETIC_ADVANCE = NO
TPC277_L2 = NONE
TPC277_FULL_GATE_B = OPEN
TPC277_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC277_TWIN_PRIME_RESULT = NONE
TPC277_STATUS = PROVED_EXACT_UNIVERSAL_FOUR_PACKET_GAIN_FLOOR_PLUS_NUMERICALLY_CERTIFIED_SOURCE_SCAN
```

## 0.70 当前：TPC-276 signed-gain margin recovery and strict endpoint budget

项目：`papers/tpc-276-signed-gain-endpoint-budget/`

类型：**PROVED_CONDITIONAL_SIGNED_GAIN_STRICT_ENDPOINT_BUDGET_PLUS_FINITE_TRANSFER**。

TPC-276 是 TPC-275 的 source-attached continuation，保持 literal V59 finite physical
operator、exact beta、prime shell、projection 与 growing-cutoff registry 不变。它把
四个实际 source-block packet 的 signed energy `G` 与 packet diagonal `D` 接回
correlation margin，精确证明
`m^2=(D/G)m_D^2`。进一步，在 source-level hypotheses
`m_D>=c*x^(-eta_D-epsilon)` 与 `D/G>=b*x^gamma` 下，定义
`eta_eff=max(0,eta_D-gamma/2)`，得到 strict endpoint compiler
`sigma-eta_eff>1/400`；gain 的 exponent 以一半进入 margin。

冻结的 TPC-275 certificate 经过 exact rational transfer 形成 12 rows：12/12 行有
`D/G>1`，3 行的 signed margin 高于 `1/16`，5 行高于 `1/64`，且没有区间跨越阈值。
这是明确的 finite threshold recovery 与 conditional theorem；有限正 gain 没有
`sufficiently-large-x` 量词，因此 fixed-power credit 仍为 0。source-level signed
gain lower bound、arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍 open/none。

```text
STRONGEST_POSITIVE_RESULT = EXACT_SIGNED_GAIN_MARGIN_IDENTITY_PLUS_CONDITIONAL_HALF_EXPONENT_COMPILER
STRONGEST_OBSTRUCTION = FINITE_SIGNED_GAIN_TABLE_HAS_ZERO_FIXED_POWER_CREDIT
OPEN_THEOREM = UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND_WITH_MARGIN_CONTROL
REUSABLE_STRUCTURE = D_OVER_G -> MARGIN_SQUARED -> GAMMA_OVER_2 -> STRICT_ENDPOINT_BUDGET
ROUND2_CLUE = SEEK_UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND
```

```text
TPC276_ROUTE_ADVANCE = YES_SCOPED_SIGNED_GAIN_MARGIN_RECOVERY
TPC276_SIGNED_GAIN_MARGIN_IDENTITY = PROVED_EXACT_FINITE
TPC276_CONDITIONAL_BUDGET_COMPILER = PROVED_CONDITIONAL_WITH_EFFECTIVE_LOSS_MAX_ZERO_ETA_D_MINUS_GAMMA_OVER_2
TPC276_FINITE_SIGNED_MARGIN_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC276_SIGNED_QUARTER_CROSSING = NUMERICALLY_CERTIFIED_FINITE_THREE_ROWS
TPC276_SIGNED_EIGHTH_CROSSING = NUMERICALLY_CERTIFIED_FINITE_FIVE_ROWS
TPC276_GAIN_STRICTLY_ABOVE_ONE = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC276_FINITE_POWER_PROMOTION = REFUTED_SCOPED
TPC276_FIXED_POWER_CREDIT = 0
TPC276_SOURCE_LEVEL_SIGNED_GAIN = OPEN_ASYMPTOTIC
TPC276_ARITHMETIC_ADVANCE = NO
TPC276_L2 = NONE
TPC276_FULL_GATE_B = OPEN
TPC276_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC276_TWIN_PRIME_RESULT = NONE
TPC276_STATUS = PROVED_CONDITIONAL_SIGNED_GAIN_STRICT_ENDPOINT_BUDGET_PLUS_FINITE_TRANSFER
```

## 0.69 当前：TPC-275 signed four-packet reassembly

项目：`papers/tpc-275-signed-four-packet-reassembly/`

类型：**NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT**。

TPC-275 承接 TPC-274 的 projected Frobenius gap，首次在同一个 literal V59
physical operator 上保留四个实际 source-block packets，而不是使用 TPC-260 的
synthetic completion。对 `V_j=A_perp beta^(j)` 定义 packet Gram、signed output
energy `G`、diagonal energy `D`，并证明 exact Gram expansion、四点 DFT
Parseval/mode-zero 和 real polarization。六个 registered scale triples、两个 kernel
exponents 的 12 rows 与 72 个 pairwise probes 均以 exact rational arithmetic replay。
结果为所有 rows 的 `G-D<0`、`1<D/G<12/5`、`F/G>50` 与 `m_D^2<1/16`；因此 signed
packet reassembly 在有限 literal interface 上确实带来可测量的 cancellation，但
保守 diagonal margin proxy 仍不能支付 quarter-margin，更没有产生渐近 signed
cross-Gram、fixed-power credit、arithmetic `L2` 或 twin-prime 结论。

```text
STRONGEST_POSITIVE_RESULT = EXACT_SIGNED_GRAM_DFT_POLARIZATION_PLUS_LITERAL_REPLAY
STRONGEST_OBSTRUCTION = DIAGONAL_ENVELOPE_CANNOT_CERTIFY_QUARTER_MARGIN_ON_12_ROWS
OPEN_THEOREM = SOURCE_LEVEL_SIGNED_CROSS_GRAM_WITH_EFFECTIVE_SAVING
REUSABLE_STRUCTURE = SOURCE_BLOCKS -> PACKET_GRAM -> POLARIZATION/DFT -> SIGNED_OUTPUT
ROUND2_CLUE = COMPILE_SIGNED_CROSS_GRAM_WITH_MARGIN_AND_ENDPOINT_BUDGET
```

```text
TPC275_ROUTE_ADVANCE = YES_SCOPED_LITERAL_SIGNED_FOUR_PACKET_REASSEMBLY
TPC275_SIGNED_GRAM_IDENTITY = PROVED_EXACT_FINITE
TPC275_DFT_LEDGER = PROVED_EXACT_FINITE
TPC275_POLARIZATION = PROVED_EXACT_FINITE
TPC275_LITERAL_PACKET_REPLAY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC275_NET_CROSS_TERM = NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_ALL_12_ROWS
TPC275_DIAGONAL_GAIN = NUMERICALLY_CERTIFIED_FINITE_BETWEEN_1_AND_12_OVER_5
TPC275_FROBENIUS_COMPARISON = NUMERICALLY_CERTIFIED_FINITE_ABOVE_50
TPC275_DIAGONAL_MARGIN = NUMERICALLY_CERTIFIED_FINITE_BELOW_QUARTER
TPC275_DIAGONAL_ROUTE = INSUFFICIENT_SCOPED
TPC275_SOURCE_LEVEL_SIGNED_CROSS_GRAM = OPEN_ASYMPTOTIC
TPC275_FIXED_POWER_CREDIT = 0
TPC275_ARITHMETIC_ADVANCE = NO
TPC275_L2 = NONE
TPC275_FULL_GATE_B = OPEN
TPC275_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC275_TWIN_PRIME_RESULT = NONE
TPC275_STATUS = NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT
```

## 0.68 当前：TPC-274 projected output Frobenius envelope

项目：`papers/tpc-274-projected-output-frobenius-envelope/`

类型：**NUMERICALLY_CERTIFIED_FINITE_PROJECTED_FROBENIUS_ENVELOPE_GAP**。

TPC-274 承接 TPC-273 的有限 margin instability，转而审计最便宜的
cancellation-free output estimate。它冻结 TPC-268 的 literal V59 finite physical
operator、exact beta source、三块 Haar projection 与 TPC-269 growing-cutoff registry，
定义 `A_perp=(I-P_3)A`、`G_perp=||A_perp beta||_2^2`，并证明 exact inequality
`G_perp <= ||A_perp||_F^2 ||beta||_2^2 = G_F`。六个 registered scales 与两个 kernel
exponents 给出 12 个 rows；exact rational matrix construction、parent interval
transfer、independent replay 与 five-mutation stress 全部通过。每一行均有
`G_F/G_perp>50`，且 conservative proxy `m_F^2=|C_perp|^2/(W_perp G_F)<1/64`；phase
census 为 11 negative-real、1 positive-real、0 crossing。

这关闭的是一个方法级 shortcut，而不是 actual margin 的上界：`m_F^2<1/64` 只说明
Frobenius envelope 不能证明 `m>1/8`，不说明实际 `m` 小。因而该结果是
`INSUFFICIENT_SCOPED` 的 finite obstruction，不是渐近反例，不支付 fixed-power
credit，也不推进 arithmetic `L2`、signed four-packet reassembly、full Gate B 或
twin-prime conclusion。

```text
STRONGEST_POSITIVE_RESULT = EXACT_PROJECTED_FROBENIUS_ENVELOPE_PLUS_12_ROW_REPLAY
STRONGEST_OBSTRUCTION = CANCELLATION_FREE_ENVELOPE_GAP_ABOVE_50_ON_ALL_ROWS
OPEN_THEOREM = SOURCE_LEVEL_SIGNED_OUTPUT_REASSEMBLY_WITH_EFFECTIVE_SAVING
REUSABLE_STRUCTURE = A_PERP -> FROBENIUS_ENVELOPE -> MARGIN_PROXY -> GAP_CERTIFICATE
ROUND2_CLUE = TEST_SIGNED_OUTPUT_REASSEMBLY_BEYOND_CANCELLATION_FREE_ENVELOPES
```

```text
TPC274_ROUTE_ADVANCE = YES_SCOPED_PROJECTED_FROBENIUS_ENVELOPE_GAP
TPC274_PROJECTED_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE_INEQUALITY
TPC274_FINITE_GAP = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC274_CANCELLATION_FREE_ROUTE = INSUFFICIENT_SCOPED
TPC274_ENVELOPE_MARGIN = NOT_AN_ACTUAL_MARGIN_UPPER_BOUND
TPC274_SOURCE_LEVEL_OUTPUT_BOUND = OPEN_ASYMPTOTIC
TPC274_SIGNED_OUTPUT_REASSEMBLY = OPEN
TPC274_FIXED_POWER_CREDIT = 0
TPC274_ARITHMETIC_ADVANCE = NO
TPC274_L2 = NONE
TPC274_FULL_GATE_B = OPEN
TPC274_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC274_TWIN_PRIME_RESULT = NONE
TPC274_STATUS = NUMERICALLY_CERTIFIED_FINITE_PROJECTED_FROBENIUS_ENVELOPE_GAP
```

## 0.67 当前：TPC-273 finite margin-stability matrix

项目：`papers/tpc-273-margin-stability-matrix/`

类型：**NUMERICALLY_CERTIFIED_FINITE_MARGIN_STABILITY_OBSTRUCTION**。

TPC-273 承接 TPC-272 的 margin coordinate，但把问题从“如何将 margin loss 编译进
endpoint budget”推进到“声明的有限 interface 是否稳定”。它冻结 TPC-268 的 literal
V59 finite physical operator，在 4 个 scale、4 个 comparison cutoff、2 个 kernel
exponent 的 32-row grid 上由 parent outward intervals 精确转移
`m^2=rho^2`、`m^6=(rho^2)^3`。阈值 `m<1/8` 与 `m>1/4` 给出 12 low、11 middle、9
high rows；固定 `(N,s)=(64,1)` 的 `z=2 -> 5` 和固定 `(N,s)=(128,1)` 的
`z=2 -> 3` 均发生 cutoff-only 跨带 flip。phase census 保留 30 negative-real、2
positive-real、0 crossing，kernel-only control 则不制造高带外的额外解释。

该结果严格是 registered finite family 的 `REFUTED_SCOPED` stability obstruction。
它不是 growing sequence 的 asymptotic counterexample，也不支付 fixed-power credit；
source-level margin uniformity、arithmetic `L2`、signed four-packet reassembly、full
Gate B 与 twin-prime conclusion 仍 open/none。

```text
STRONGEST_POSITIVE_RESULT = EXACT_MARGIN_TRANSFER_PLUS_32_ROW_OUTWARD_MATRIX
STRONGEST_OBSTRUCTION = CUTOFF_ONLY_FLIPS_ACROSS_LOW_MIDDLE_HIGH_MARGIN_BANDS
OPEN_THEOREM = SOURCE_LEVEL_MARGIN_UNIFORMITY_ON_THE_LITERAL_GROWING_CUTOFF
REUSABLE_STRUCTURE = RHO2_INTERVAL -> MARGIN2 -> TWO_THRESHOLD_BANDS -> HOSTILE_TRANSITION
ROUND2_CLUE = TEST_SOURCE_LEVEL_MARGIN_UNIFORMITY_ON_THE_LITERAL_GROWING_CUTOFF
```

```text
TPC273_ROUTE_ADVANCE = YES_SCOPED_FINITE_MARGIN_STABILITY_OBSTRUCTION
TPC273_MARGIN_STABILITY_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE
TPC273_CUTOFF_FLIPS = NUMERICALLY_CERTIFIED
TPC273_PHASE_FLIP = NUMERICALLY_CERTIFIED_FINITE_TWO_ROWS
TPC273_SOURCE_LEVEL_MARGIN = OPEN_ASYMPTOTIC
TPC273_GROWING_UNIFORMITY = OPEN_ASYMPTOTIC
TPC273_FIXED_POWER_CREDIT = 0
TPC273_ARITHMETIC_ADVANCE = NO
TPC273_L2 = NONE
TPC273_FULL_GATE_B = OPEN
TPC273_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC273_TWIN_PRIME_RESULT = NONE
TPC273_STATUS = NUMERICALLY_CERTIFIED_FINITE_MARGIN_STABILITY_OBSTRUCTION
```

## 0.66 当前：TPC-272 correlation-margin to endpoint-budget compiler

项目：`papers/tpc-272-correlation-margin-budget-compiler/`

类型：**PROVED_CONDITIONAL_CORRELATION_MARGIN_TO_RADIUS_BUDGET_COMPILER**。

TPC-272 承接 TPC-271 的 phase--radius 坐标，定义
`m=|C_perp|/R`，并证明 exact finite identity
`m^6=Xi_C/Xi`。在 `E0=5/3`、`E*=1997/1200` 的 endpoint ledger 中，若
signed scalar 有 effective saving `sigma`、而 margin 只损失 `eta`，则
`R=|C_perp|/m` 给出 endpoint saving `sigma-eta`；严格支付条件是
`sigma-eta>1/400`。二维 exact witness 证明 negative phase sign alone 对 `m`
没有正下界。

由 TPC-271 parent certificate 进行的 9-row/4-dyadic rational audit 显示：
`96->192` 的 margin sixth-power ratio 严格小于 `(1/32)^6`，而 phase sign 保持
`NEGATIVE_REAL_AXIS`；`192->384` 则高于 `4^6`。这是真实的新 conditional theorem
与 finite numerical certificate，但不激活 source-level margin hypothesis，不支付
fixed-power credit，也不产生 arithmetic `L2`、full Gate B 或 twin-prime conclusion。

```text
STRONGEST_POSITIVE_RESULT = CONDITIONAL_SIGMA_MINUS_ETA_ENDPOINT_COMPILER
STRONGEST_OBSTRUCTION = SIGN_ONLY_PHASE_DOES_NOT_LOWER_BOUND_MARGIN
OPEN_THEOREM = SOURCE_LEVEL_MARGIN_LOWER_BOUND_COUPLED_TO_SIGNED_SCALAR
REUSABLE_STRUCTURE = Xi_C/Xi -> MARGIN_SIXTH_POWER -> MARGIN_LOSS -> ENDPOINT_BUDGET
ROUND2_CLUE = AUDIT_SOURCE_LEVEL_MARGIN_LOWER_BOUND_BEFORE_ANY_PHASE_PROMOTION
```

## 0.65 当前：TPC-271 phase--radius decoupling

项目：`papers/tpc-271-phase-radius-decoupling/`

类型：**NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT**。

TPC-271 承接 TPC-270，冻结同一个 literal V59 finite interface，并把 signed scalar
`C_perp`、source residual lane `W_perp` 与 output residual lane `G_perp` 放进同一
证书。定义 `Xi_W=W_perp^3/N^5`、`Xi_G=G_perp^3/N^5`、
`Xi_C=|C_perp|^6/N^10` 后，精确得到
`Xi=Xi_W*Xi_G` 与 `Xi/Xi_C=|kappa|^(-6)`。六个 base rows 与三个 profile controls
的 scalar intervals 全部严格为负实轴；但四个 dyadic lane records 仍呈
`DROP_RISE_RISE_DROP`。尤其 `96->192` 的 radius ratio 高于 `23`，同时 source lane
低于 `1/8`、output lane 高于 `230`，因而该有限 spike 被 output lane 归因。

这是一个新的 finite analytic structure 与 numerical certificate，不是 phase/radius
渐近定理、统计独立性命题或 arithmetic `L2` closure；fixed-power credit 仍为 0，
full Gate B 与 twin-prime conclusion 仍 open。

```text
STRONGEST_POSITIVE_RESULT = EXACT_LANE_FACTORIZATION_PLUS_PHASE_LOCKED_OUTPUT_SPIKE_CERTIFICATE
STRONGEST_OBSTRUCTION = GREATER_THAN_23_RADIUS_RISE_WITH_NEGATIVE_PHASE_PRESERVED
OPEN_THEOREM = SOURCE_LEVEL_SIGNED_PHASE_BOUND_WITH_EXPLICIT_RADIUS_LANE_CONTROL
REUSABLE_STRUCTURE = (C_perp,W_perp,G_perp) -> Xi_C,Xi_W,Xi_G -> LANE_RATIO_ATTRIBUTION
ROUND2_CLUE = TEST_SOURCE_LEVEL_SIGNED_PHASE_BOUND_WITH_EXPLICIT_RADIUS_LANE_CONTROL
```

## 0.64 已发布：TPC-270 cross-scale endpoint-normalized radius

项目：`papers/tpc-270-cross-scale-radius-normalization/`

类型：**NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT**。

TPC-270 承接 TPC-269，冻结同一个 literal V59 finite physical operator、registered
`z_N=floor(log N)` cutoff 与 convex profile interface，首次把 residual radius 写成
可跨尺度比较的 exact observable
`Xi=(R_squared)^3/N^10=(R/N^(5/3))^6`。六个 base rows、四个 dyadic ratios、五个
adjacent ratios 与三个 profile controls 均由 outward interval、独立重算和 stress
audit 认证。四个 dyadic intervals 的分类为
`DROP_RISE_RISE_DROP`：`64->128<1/4`，`96->192>23`，`128->256>7`，而
`192->384` 落在 `(3/4,1)`；profile controls 均落在 `(1/2,3/4)`。

这给出一个新的 finite normalization audit 与 scoped stability obstruction，但不构成
source-level radius bound、渐近反例或 fixed-power saving。arithmetic `L2`、full Gate B
与 twin-prime conclusion 仍 open。

```text
STRONGEST_POSITIVE_RESULT = EXACT_ENDPOINT_NORMALIZATION_PLUS_4_DYADIC_RATIO_CERTIFICATES
STRONGEST_OBSTRUCTION = NORMALIZED_RADIUS_HAS_GREATER_THAN_23_RISE_AND_SUBQUARTER_DROP
OPEN_THEOREM = SOURCE_LEVEL_RADIUS_UPPER_BOUND_WITH_EXPLICIT_POWER_AND_UNIFORMITY
REUSABLE_STRUCTURE = RADIUS_INTERVAL -> SIXTH_POWER NORMALIZATION -> POSITIVE SCALE RATIO
ROUND2_CLUE = TEST_SOURCE_LEVEL_RADIUS_UPPER_BOUND_WITH_EXPLICIT_POWER_NORMALIZATION
```

## 0.63 已发布：TPC-269 growing-cutoff and convex-profile transfer

项目：`papers/tpc-269-growing-cutoff-profile-transfer/`

类型：**NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER**。

TPC-269 保持 TPC-268 的 finite literal V59 prime shell、outer `q` weight、unit masks、
deleted diagonal、source `beta` 与 rank-three projection 不变。comparison cutoff 使用
注册的 finite proxy `z_N=floor(log N)`；两个 normalized nonnegative kernel
representatives 通过 `A_theta=(1-theta)A_1+theta A_2` exact affine transfer。outward
rational intervals 对 12 个 rows 给出 8 个 contractions 与 4 个 obstructions。

在同一 `(N,H,Q,z_N)=(64,15,4,4)` 上，`theta=9/10` 的 `rho^2` interval 完全高于
`1/16`，而 `theta=24/25` 的 interval 完全低于 `1/16`。因此 finite growing proxy
并不自动给 profile-uniform quarter contraction。这个结果不控制 actual source-level
cutoff/profile，也不控制跨尺度 residual radius；fixed-power credit 仍为 0，arithmetic
`L2`、full Gate B 与 twin-prime conclusion 仍 open。

```text
STRONGEST_POSITIVE_RESULT = EXACT_AFFINE_PROFILE_TRANSFER_PLUS_12_ROW_CERTIFICATE
STRONGEST_OBSTRUCTION = PROFILE_PATH_FLIP_AT_FIXED_GROWING_CUTOFF
OPEN_THEOREM = UNIFORM_SOURCE_COMPATIBLE_GROWING_CUTOFF_PROFILE_BOUND
REUSABLE_STRUCTURE = GROWING_CUTOFF -> AFFINE_PROFILE_PATH -> RHO2_INTERVAL
ROUND2_CLUE = TEST_CROSS_SCALE_RADIUS_NORMALIZATION_AFTER_SOURCE_COMPATIBLE_PROFILE
```

```text
TPC269_ROUTE_ADVANCE = YES_SCOPED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER
TPC269_GROWING_CUTOFF_PROXY = NUMERICALLY_CERTIFIED_FINITE
TPC269_PROFILE_MIXTURE_IDENTITY = PROVED_EXACT_FINITE
TPC269_PROFILE_PATH_FLIP = NUMERICALLY_CERTIFIED_FINITE
TPC269_GROWING_UNIFORMITY = OPEN_ASYMPTOTIC
TPC269_ACTUAL_V59_RADIUS = OPEN_ASYMPTOTIC
TPC269_ACTUAL_V59_PHASE = OPEN_ASYMPTOTIC
TPC269_FIXED_POWER_CREDIT = 0
TPC269_ARITHMETIC_ADVANCE = NO
TPC269_L2 = NONE
TPC269_FULL_GATE_B = OPEN
TPC269_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC269_TWIN_PRIME_RESULT = NONE
TPC269_STATUS = NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER
```

## 0.62 已发布：TPC-268 finite cutoff-sensitivity obstruction

项目：`papers/tpc-268-finite-cutoff-sensitivity-obstruction/`

类型：**NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION**。

TPC-268 固定 TPC-267 的实际有限 operator、source beta、prime shell、unit masks、
deleted diagonal 与 rank-three Haar residual，只改变声明的 local comparison cutoff、
rounded clock 和 kernel exponent。outward rational intervals 对 16 个 rows 给出 10 个
contractions 与 6 个 obstructions；同一 central row `(64,15,4,1)` 从 `z=2` 的
`rho^2<1/16` 翻到 `z=3` 的 `rho^2>1/16`。H=13,15,17 的 z=3 rows 保持
obstruction，说明这不是单一 clock rounding 事故。

这是 finite、model-relative 的反例/obstruction，不是 growing V59 counterexample。
`z`、`H`、`s` 都是声明的 finite interface choices；因此不支付 fixed-power credit，
不产生 arithmetic `L2`，也不关闭 full Gate B 或 twin-prime conclusion。

```text
STRONGEST_POSITIVE_RESULT = MATCHED_Z2_CONTROLS_REPRODUCED
STRONGEST_OBSTRUCTION = Z3_CUTOFF_FLIPS_THE_SAME_CENTRAL_ROW_ABOVE_1_OVER_4
OPEN_THEOREM = GROWING_CUTOFF_AND_PROFILE_UNIFORMITY_FOR_LITERAL_V59
REUSABLE_STRUCTURE = MATCHED_CONTROL -> DECLARED_PERTURBATION -> OUTWARD_THRESHOLD_SEPARATION
ROUND2_CLUE = TEST_GROWING_CUTOFF_UNIFORMITY_BEFORE_ANY_PHASE_PROMOTION
```

```text
TPC268_ROUTE_ADVANCE = YES_SCOPED_FINITE_CUTOFF_SENSITIVITY_OBSTRUCTION
TPC268_FINITE_CUTOFF_OBSTRUCTION = NUMERICALLY_CERTIFIED
TPC268_MATCHED_Z2_CONTROLS = NUMERICALLY CERTIFIED
TPC268_CLOCK_STABILITY = REFUTED_SCOPED
TPC268_KERNEL_STABILITY = REFUTED_SCOPED
TPC268_ACTUAL_V59_RADIUS = OPEN_ASYMPTOTIC
TPC268_ACTUAL_V59_PHASE = OPEN_ASYMPTOTIC
TPC268_FIXED_POWER_CREDIT = 0
TPC268_ARITHMETIC_ADVANCE = NO
TPC268_L2 = NONE
TPC268_FULL_GATE_B = OPEN
TPC268_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC268_TWIN_PRIME_RESULT = NONE
TPC268_STATUS = NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION
```

## 0.61 已发布：TPC-267 finite literal V59 residual-radius and signed-phase census

项目：`papers/tpc-267-literal-v59-residual-radius-census/`

类型：**NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS**。

TPC-267 将 TPC-266 留下的 literal V59 residual radius/phase open input，落实为一个
可重放的有限 physical object：实际 prime shell、outer `q` weight、两个 unit masks、
deleted diagonal、source `beta`、`z=2` shifted-prime comparison 与三维 consecutive-block
Haar projection 全部保留。对 12 个自然有限时钟行，outward rational intervals 认证
`R^2>0` 且 `|C_perp|/R<1/4`；最大 upper endpoint 为 `0.2320126753`，相位为 10 个
negative-real 与 2 个 positive-real 行。独立 replay 与 kernel stress 均通过。

这是真实的 finite numerical certificate，而非 growing-parameter theorem：`R` 的
渐近规模没有得到控制，phase 不形成已证明的 uniform sector，两个 kernel 与 rounded
clock 是声明的有限 modeling choices。因此 fixed-power credit 仍为 0，arithmetic
`L2`、full Gate B 与 twin-prime conclusion 仍 open。

```text
STRONGEST_POSITIVE_RESULT = FINITE_LITERAL_PRIME_SHELL_RESIDUAL_PHASE_CONTRACTION
STRONGEST_OBSTRUCTION = FINITE_PHASE_CONTRACTION_DOES_NOT_BOUND_THE_ASYMPTOTIC_RADIUS
OPEN_THEOREM = UNIFORM_LITERAL_V59_RADIUS_OR_SIGNED_PHASE_BOUND_WITH_EFFECTIVE_SAVING_GT_1_OVER_400
REUSABLE_STRUCTURE = EXACT_A_OPERATOR -> P3_PROJECTION -> RADIUS_SQUARED_INTERVAL -> SIGNED_PHASE_RATIO
ROUND2_CLUE = REPEAT_THE_CENSUS_WITH_GROWING_LOCAL_CUTOFF_AND_SMOOTH_PROFILE
```

```text
TPC267_ROUTE_ADVANCE = YES_SCOPED_FINITE_LITERAL_RESIDUAL_CENSUS
TPC267_LITERAL_MASK_OPERATOR = PROVED_EXACT_FINITE
TPC267_BETA_FORMULA = PROVED_EXACT_FINITE
TPC267_HYBRID_EULER_ENCLOSURE = PROVED_INTERVAL_FINITE
TPC267_PROJECTION_SPLIT = PROVED_EXACT_FINITE
TPC267_FINITE_RESIDUAL_RADIUS = NUMERICALLY CERTIFIED
TPC267_FINITE_SIGNED_PHASE = NUMERICALLY CERTIFIED
TPC267_QUARTER_CONTRACTION = NUMERICALLY CERTIFIED_ALL_12_ROWS
TPC267_ACTUAL_V59_RADIUS = OPEN_ASYMPTOTIC
TPC267_ACTUAL_V59_PHASE = OPEN_ASYMPTOTIC
TPC267_FIXED_POWER_CREDIT = 0
TPC267_ARITHMETIC_ADVANCE = NO
TPC267_L2 = NONE
TPC267_FULL_GATE_B = OPEN
TPC267_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC267_TWIN_PRIME_RESULT = NONE
TPC267_STATUS = NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS
```

## 0.60 已发布：TPC-266 typed end-to-end residual claim firewall

项目：`papers/tpc-266-end-to-end-claim-firewall/`

类型：**PROVED_EXACT_END_TO_END_RESIDUAL_CLAIM_FIREWALL**。

TPC-266 对 TPC-263→TPC-264→TPC-265 的整条 Bridge-B 链做 hostile end-to-end
审计。它定义 exact typed compiler：center 与 residual-radius 两条 lane 只有在
属于 `POWER`/`SIGNED_PHASE`、各自 effective saving 严格超过 `1/400` 且 residual
仍被保留时，才可返回 `CLOSED_CONDITIONAL`。fixed-log center、missing radius、
borderline equality、subcritical saving 与 residual deletion 分别落入六状态
firewall；19 个字段突变由独立 checker 全部拒绝。该结果是组合接口定理，不是
literal V59 radius/phase estimate，也不支付 arithmetic `L2` 或 full Gate B。

```text
STRONGEST_POSITIVE_RESULT = EXACT_TYPED_END_TO_END_RESIDUAL_CLAIM_FIREWALL
STRONGEST_OBSTRUCTION = FIXED_LOG_CENTER_PLUS_OPEN_RADIUS_BLOCKS_CLOSURE
OPEN_THEOREM = LITERAL_V59_RADIUS_OR_SIGNED_PHASE_BOUND_WITH_EFFECTIVE_SAVING_GT_1_OVER_400
REUSABLE_STRUCTURE = TPC263_LOG -> TPC264_SCHUR_SET -> TPC265_RADIAL_SUPPORT -> TYPED_BUDGET
ROUND2_CLUE = PROVE_A_LITERAL_V59_RADIUS_OR_SIGNED_PHASE_BOUND_WITH_EFFECTIVE_SAVING_GREATER_THAN_1_OVER_400
```

```text
TPC266_ROUTE_ADVANCE = YES_SCOPED_END_TO_END_CLAIM_FIREWALL
TPC266_TYPED_COMPOSITION = PROVED_EXACT
TPC266_FIXED_LOG_NONPROMOTION = PROVED_EXACT
TPC266_RESIDUAL_RETENTION_FIREWALL = PROVED_EXACT
TPC266_FAILURE_MATRIX = PROVED_EXACT_SIX_STATE
TPC266_STRICT_PAYMENT_THRESHOLD = PROVED_EXACT_ONE_OVER_400
TPC266_CENTER_CURRENT_TYPE = FIXED_LOG
TPC266_RESIDUAL_CURRENT_TYPE = SCHUR_SET_RADIUS_OPEN
TPC266_ACTUAL_V59_RADIUS = OPEN
TPC266_ACTUAL_V59_PHASE = OPEN
TPC266_FIXED_POWER_CREDIT = 0
TPC266_ARITHMETIC_ADVANCE = NO
TPC266_L2 = NONE
TPC266_FULL_GATE_B = OPEN
TPC266_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC266_TWIN_PRIME_RESULT = NONE
TPC266_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC266_STATUS = PROVED_EXACT_END_TO_END_RESIDUAL_CLAIM_FIREWALL
```

## 0.59 已发布：TPC-265 Schur radius to endpoint-budget compiler

项目：`papers/tpc-265-schur-endpoint-budget-compiler/`

类型：**PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER**。

TPC-265 将 TPC-264 的 exact residual disk 接入 endpoint ledger。对 projected
center `c` 与 Schur radius `R`，uniform radial support 恰为
`sup|c+z|=|c|+R`；free-phase circle 也达到同一上边界。因而 residual radius
是必须单独支付的 lane，不能从 norm-only data 中扣除 cancellation credit。结合
`E0=5/3`、`E*=1997/1200`，center/radius 两个 power lanes 各自的 effective
saving 必须严格超过 `1/400` 才能编译出目标；fixed-log control 的 credit 为零。

```text
STRONGEST_POSITIVE_RESULT = SHARP_SCHUR_RADIAL_ENVELOPE_AND_TWO_LANE_THRESHOLD
STRONGEST_OBSTRUCTION = ALIGNED_RESIDUAL_ENDPOINT_ERASES_NORM_ONLY_CANCELLATION
OPEN_THEOREM = LITERAL_V59_RESIDUAL_RADIUS_OR_SIGNED_PHASE_THEOREM
REUSABLE_STRUCTURE = SCHUR_SET -> RADIAL_SUPPORT -> CENTER_PLUS_RADIUS_LANES -> 1/400_TEST
ROUND2_CLUE = TEST_LITERAL_RESIDUAL_RADIUS_OR_PHASE_AGAINST_THE_TWO_LANE_BUDGET
```

```text
TPC265_ROUTE_ADVANCE = YES_SCOPED_RESIDUAL_RADIUS_BUDGET_COMPILER
TPC265_SCHUR_RADIAL_ENVELOPE = PROVED_EXACT
TPC265_DISK_WORST_CASE = PROVED_EXACT
TPC265_CIRCLE_WORST_CASE = PROVED_EXACT
TPC265_TWO_LANE_ENDPOINT_COMPILER = PROVED_EXACT_CONDITIONAL
TPC265_STRICT_PAYMENT_THRESHOLD = PROVED_EXACT_ONE_OVER_400
TPC265_LOG_CENTER_CREDIT = 0
TPC265_LOG_RADIUS_CREDIT = 0
TPC265_ACTUAL_V59_RADIUS = OPEN
TPC265_ACTUAL_V59_PHASE = OPEN
TPC265_FIXED_POWER_CREDIT = 0
TPC265_ARITHMETIC_ADVANCE = NO
TPC265_L2 = NONE
TPC265_FULL_GATE_B = OPEN
TPC265_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC265_TWIN_PRIME_RESULT = NONE
TPC265_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC265_STATUS = PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER
```

## 0.58 已发布：TPC-264 orthogonal-residual Schur firewall

项目：`papers/tpc-264-orthogonal-residual-schur-firewall/`

类型：**PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL**。

TPC-264 承接 TPC-263 的 exact projection split，并对未估计的正交残差给出完整
finite-dimensional Schur classification。固定 `p=P_3w`、`q=P_3g_x`、
`a=||(I-P_3)w||`、`b=||(I-P_3)g_x||` 后，残差
`z=<(I-P_3)w,(I-P_3)g_x>` 的可实现集合在补空间维数至少二时恰为闭圆盘
`|z|<=ab`；维数一且 `ab>0` 时恰为圆 `|z|=ab`；退化时为单点。full scalar
是以 `c=<p,q>` 为中心的平移集合。二维补空间的 endpoint-scale synthetic
radius 仍为 `x^(5/3)`，因此 rank-three log control 加 norm-only residual data
不能自动产生 fixed-power credit。

```text
STRONGEST_POSITIVE_RESULT = EXACT_SCHUR_DISK_CIRCLE_SINGLETON_FIREWALL
STRONGEST_OBSTRUCTION = NORM_ONLY_RESIDUAL_DATA_LEAVE_FULL_RADIUS_IN_DIMENSION_TWO
OPEN_THEOREM = LITERAL_V59_RESIDUAL_RADIUS_OR_SIGNED_PHASE_ESTIMATE
REUSABLE_STRUCTURE = P3_CENTER -> RESIDUAL_GRAM -> SCHUR_FEASIBLE_SET -> ENDPOINT_RADIUS_TEST
ROUND2_CLUE = TURN_THE_SCHUR_RADIUS_OR_RESIDUAL_PHASE_INTO_A_LITERAL_V59_ESTIMATE
```

```text
TPC264_ROUTE_ADVANCE = YES_SCOPED_RESIDUAL_SCHUR_FIREWALL
TPC264_PROJECTION_DATA = PROVED_EXACT
TPC264_RESIDUAL_GRAM_FEASIBLE_SET = PROVED_EXACT
TPC264_COMPLEMENT_DIMENSION_SPLIT = PROVED_EXACT
TPC264_FULL_SCALAR_FEASIBLE_SET = PROVED_EXACT
TPC264_ENDPOINT_SCALE_WITNESS = NUMERICALLY_CERTIFIED_STRUCTURAL
TPC264_FIXED_POWER_CREDIT = 0
TPC264_ARITHMETIC_ADVANCE = NO
TPC264_ACTUAL_V59_RESIDUAL = OPEN
TPC264_L2 = NONE
TPC264_FULL_GATE_B = OPEN
TPC264_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC264_TWIN_PRIME_RESULT = NONE
TPC264_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC264_STATUS = PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL
```

## 0.57 已发布：TPC-263 rank-three physical cross-Gram channel

项目：`papers/tpc-263-rank-three-physical-cross-gram/`

类型：**PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL**。

TPC-263 将 TPC-254 的四个 consecutive block-sum fixed-log control 与
TPC-257 的三个 source-backed adjoint coefficients 接到同一个 exact rank-three
projection。若 `P3` 投影到 source-only frame `span(z0,z1,z2)`，则

```text
C_x=<w,A_x beta>=C_3(x)+C_perp(x),
C_3(x)=sum_i conjugate(<z_i,w>)<z_i,A_x beta>,
C_perp(x)=<(I-P3)w,(I-P3)A_x beta>.
```

对每个固定 admissible `K` 与固定 `M`，新的 source-backed channel 满足
`C_3=O_(M,K)(x^(5/3)/(log x)^(M+3))`。这是同一物理对象上的 rank-three
cross-Gram 进展；`C_perp` 被精确保留且仍未估计，所以该结果只有 logarithmic
credit，不支付 fixed-power `1/400`、arithmetic `L2` 或 full Gate B。

```text
STRONGEST_POSITIVE_RESULT = SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL
STRONGEST_OBSTRUCTION = EXACT_ORTHOGONAL_RESIDUAL_CPERP_REMAINS_UNESTIMATED
OPEN_THEOREM = CONTROL_OR_SHARPLY_OBSTRUCT_THE_ORTHOGONAL_COMPLEMENT
REUSABLE_STRUCTURE = SOURCE_ONLY_HAAR_FRAME -> PHYSICAL_PROJECTION_SPLIT -> SIGNED_CROSS_GRAM_CHANNEL
ROUND2_CLUE = ATTACK_THE_ORTHOGONAL_COMPLEMENT_AFTER_PAYING_THE_RANK_THREE_LOG_CHANNEL
```

```text
TPC263_ROUTE_ADVANCE = YES_SCOPED_RANK_THREE_LOG_CHANNEL
TPC263_W_FRAME_MOMENTS = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER
TPC263_ADJOINT_FRAME_COEFFICIENTS = PROVED_SOURCE_BACKED_TPC257
TPC263_PROJECTION_SPLIT = PROVED_EXACT
TPC263_RANK_THREE_CHANNEL = PROVED_SOURCE_BACKED_X_5_OVER_3_LOG_M_PLUS_3
TPC263_ORTHOGONAL_RESIDUAL = OPEN
TPC263_FIXED_POWER_CREDIT = 0
TPC263_ARITHMETIC_ADVANCE = YES_SCOPED_FIXED_LOG_ONLY
TPC263_L2 = NONE
TPC263_FULL_GATE_B = OPEN
TPC263_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC263_TWIN_PRIME_RESULT = NONE
TPC263_STATUS = PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL
```

## 0.56 已发布：TPC-262 literal signed reduced-residue operator and phase-character firewall

项目：`papers/tpc-262-literal-mode-zero-cross-gram/`

类型：**PROVED_EXACT_LITERAL_SIGNED_REDUCED_RESIDUE_OPERATOR_AND_PHASE_CHARACTER_FIREWALL**。

TPC-262 将 TPC-261 的 endpoint threshold 接到 actual finite reduced-residue
operator。对每个 prime `q`、additive phase `v`，定义

```text
J_(q,v)=S_(q,v)^* C_q S_(q,v)-((q-2)/(q-1))P_q,
C_q=I_(q-1)-(q-1)^(-1)11^T.
```

这保留 unit mask、deleted diagonal 和 outer prime weight，并给出
`V_q^times-D_q^times=<a,J_(q,v)a>` 的 exact phase-by-phase identity。四 packet
输出满足 exact signed cross-Gram/DFT mode-zero ledger；另一个 phase-character
lemma 严格区分 aggregate mode zero 与 V59 polarized character。实际 finite shell
`{5,7,11,13}` 的 literal operator-image witness 在相同 packet diagonals 下实现
`16||Y||^2` 与 `0` 两个 mode-zero 端点，因此 diagonal/PSD-only promotion 被
封口；它不是 growing-shell counterexample。

```text
STRONGEST_POSITIVE_RESULT = EXACT_LITERAL_SIGNED_REMAINDER_OPERATOR_AND_PHASE_TYPING
STRONGEST_OBSTRUCTION = OPERATOR_IMAGE_DIAGONAL_ONLY_CONTROL_IS_INSUFFICIENT
OPEN_THEOREM = IDENTIFY_AND_ESTIMATE_THE_CORRECT_GROWING_V59_PHASE_CHARACTER
REUSABLE_STRUCTURE = UNIT_CLASS_PROJECTION -> WEIGHTED_GRAM -> DFT_MODE_ZERO -> 1/400_CRITERION
ROUND2_CLUE = CENSUS_THE_LITERAL_GROWING_PRIME_SHELL_CROSS_GRAM
```

```text
TPC262_ROUTE_ADVANCE = YES_SCOPED_LITERAL_SIGNED_OPERATOR_INTERFACE
TPC262_UNIT_CLASS_PROJECTION = PROVED_EXACT_FINITE
TPC262_CROSS_GRAM_IDENTITY = PROVED_EXACT
TPC262_SIGNED_REMAINDER_OPERATOR = PROVED_EXACT_FINITE_X
TPC262_DELETED_DIAGONAL = PROVED_EXACT_Q_MINUS_2
TPC262_ENDPOINT_THRESHOLD = PROVED_EXACT_ONE_OVER_400
TPC262_OPERATOR_IMAGE_WITNESS = NUMERICALLY_CERTIFIED_STRUCTURAL
TPC262_PHASE_CHARACTER_SEPARATION = PROVED_EXACT
TPC262_POLARIZED_V59_CHARACTER = OPEN
TPC262_GROWING_SHELL_COUNTEREXAMPLE = NONE
TPC262_ARITHMETIC_ADVANCE = NO
TPC262_FIXED_ATOM_CREDIT = 0
TPC262_L2 = NONE
TPC262_FULL_GATE_B = OPEN
TPC262_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC262_TWIN_PRIME_RESULT = NONE
TPC262_LITERAL_BETA_W_CROSS_GRAM = OPEN
TPC262_STATUS = PROVED_EXACT_LITERAL_SIGNED_REDUCED_RESIDUE_OPERATOR_AND_PHASE_CHARACTER_FIREWALL
```

## 0.55 已发布：TPC-261 strict endpoint-budget compiler

项目：`papers/tpc-261-strict-endpoint-budget-compiler/`

类型：**PROVED_STRUCTURAL_ENDPOINT_BUDGET_OBSTRUCTION_FOR_LITERAL_V59_REASSEMBLY**。

TPC-261 直接承接 TPC-260 的 mode-zero obstruction，将当前 unnormalized baseline
与 target 精确归一为

```text
E0=5/3=2000/1200, E*=1997/1200, E0-E*=1/400.
```

对 finite lane `l`，若 `delta_l` 是 proved saving、`lambda_l` 是 reassembly
loss，则 effective credit 为 `sigma_l=delta_l-lambda_l`。严格 finite-lane
compiler 证明 `min_l sigma_l>1/400` 足以得到目标端点；等号只在 power level
borderline，低于等号不能关闭。另证明 `x^delta/(log x)^M -> infinity`，所以
fixed-log suppression 的 fixed-power credit 为零。缩放 TPC-260 的
plus/alternating families 后，相同 packet marginals 与 Haar/null data 仍允许
full residual `16*x^(5/3)` 与 `0`，构成 structural synthetic obstruction。

```text
STRONGEST_POSITIVE_RESULT = EXACT_LANE_WISE_ENDPOINT_BUDGET_COMPILER_AND_MINIMUM_SUFFICIENT_MODE_ZERO_THRESHOLD
STRONGEST_OBSTRUCTION = LOG_ONLY_NULL_SUPPRESSION_AND_SCALED_NULL_COMPATIBLE_RESIDUAL_PREVENT_ANY_AUTOMATIC_GLOBAL_FIXED_POWER_CREDIT
OPEN_THEOREM = LITERAL_COMMON_CLOCK MODE ZERO OR SIGNED CROSS GRAM ESTIMATE WITH EFFECTIVE SAVING GREATER THAN 1 OVER 400
REUSABLE_STRUCTURE = E0_TO_TARGET_GAP -> LANEWISE_SAVING_MINUS_LOSS -> LOG_POWER_FIREWALL -> SCALED_TPC260_WITNESS -> MINIMUM_LITERAL_THEOREM
ROUND2_CLUE = PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_WITH_EFFECTIVE_SAVING_GREATER_THAN_1_OVER_400
```

```text
TPC261_ROUTE_ADVANCE = YES_SCOPED_ENDPOINT_BUDGET_COMPILER
TPC261_BUDGET_IDENTITY = PROVED_EXACT
TPC261_STRICT_THRESHOLD = PROVED_EXACT_ONE_OVER_400
TPC261_BORDERLINE_EQUALITY = PROVED_EXACT_POWER_LEVEL_ONLY
TPC261_LOG_ONLY_TO_POWER_PROMOTION = REFUTED_SCOPED
TPC261_SCALED_NULL_COMPATIBLE_WITNESS = PROVED_STRUCTURAL_SYNTHETIC
TPC261_GLOBAL_FIXED_POWER_CREDIT = NONE
TPC261_LITERAL_MODE_ZERO_ESTIMATE = OPEN
TPC261_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC261_ARITHMETIC_ADVANCE = NO
TPC261_FIXED_ATOM_CREDIT = 0
TPC261_L2 = NONE
TPC261_FULL_GATE_B = OPEN
TPC261_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC261_TWIN_PRIME_RESULT = NONE
```

## 0.54 已发布：TPC-260 null-compatible four-packet residual reassembly

项目：`papers/tpc-260-four-packet-residual-reassembly/`

类型：**PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION**。

TPC-260 将 TPC-258 的 source-frozen `z_null` 嵌入 TPC-257 的实际四块 Haar
complement，并在不改变 packet marginal 的前提下补入正交 scaling mode。对
`V_j=d_j exp(i theta_j)w` 给出 sharp polygon completion：

```text
max(2*d_max-D,0) <= |<w,sum_j V_j>| <= D,
D=sum_j d_j.
```

随后用四点 DFT 精确记录 `sum_j V_j=2 Vhat_0`、Parseval 以及 full residual
energy 对 mode zero 的依赖。等范数 plus/alternating families 共享
`(1,1,1,1)` packet diagonal、全部 Haar contrast projection 和 TPC-259 null
coefficient，却分别给出 full energy `16` 与 `0`。因此 marginal/null 数据对
full residual 的识别在该结构范围内被严格否定；这不是 literal growing
prime-shell counterexample。

```text
STRONGEST_POSITIVE_RESULT = SHARP_NULL_COMPATIBLE_POLYGON_COMPLETION_AND_MODE_ZERO_DFT_LEDGER
STRONGEST_OBSTRUCTION = IDENTICAL_PACKET_MARGINALS_AND_ZERO_HAAR_NULL_PROJECTIONS_ALLOW_RESIDUAL_ENERGIES_ZERO_AND_SIXTEEN
OPEN_THEOREM = COMMON_CLOCK_LITERAL_V59_MODE_ZERO_OR_SIGNED_CROSS_GRAM_ESTIMATE
REUSABLE_STRUCTURE = FOUR BLOCK HAAR COMPLEMENT -> NULL COMPATIBLE COMPLETION -> DFT MODE LEDGER -> RESIDUAL FIREWALL
ROUND2_CLUE = PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_FOR_THE_COMMON_V59_FOUR_PACKET_OUTPUT
```

```text
TPC260_ROUTE_ADVANCE = YES_SCOPED_MODE_AUDIT
TPC260_HAAR_COMPLEMENT = PROVED_EXACT_FINITE
TPC260_POLYGON_COMPLETION = PROVED_EXACT_FINITE
TPC260_DFT_MODE_LEDGER = PROVED_EXACT
TPC260_NULL_CHANNEL_COMPATIBILITY = PROVED_EXACT_SYNTHETIC
TPC260_FULL_RESIDUAL_IDENTIFIABILITY = REFUTED_SCOPED
TPC260_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC260_ARITHMETIC_ADVANCE = NO
TPC260_FIXED_ATOM_CREDIT = 0
TPC260_L2 = NONE
TPC260_FULL_GATE_B = OPEN
TPC260_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC260_TWIN_PRIME_RESULT = NONE
```

## 0.53 已发布：TPC-259 same-clock null-channel coupling

项目：`papers/tpc-259-same-clock-null-coupling/`

类型：**PROVED_SOURCE_BACKED_SAME_CLOCK_NULL_CHANNEL_SUPPRESSION_FOR_LITERAL_V59_SIGNED_COUPLING**。

TPC-259 places TPC-258's source-frozen null direction and the literal hybrid
residual on one V59 clock.  TPC-254's maximal-interval theorem applies to each
of the four consecutive source blocks and gives, for every fixed finite
`K` and fixed `M>0`，

```text
|<z_null,w>| <<_(M,K) sqrt(x)/(log x)^M.
```

Together with `<z_null,A_x beta>=o(x^(7/6)/log^3(x))`，the exact decomposition

```text
<w,A_x beta>
 =conjugate(<z_null,w>)<z_null,A_x beta>
  +<w_perp,A_x beta>
```

proves that the first rank-one channel is `o(x^(5/3)/log^(M+3)(x))`.  The perpendicular residual is left visible and
open.  A finite real zero-diagonal witness has zero null channel and nonzero
full scalar, so projection algebra alone cannot promote the result.

```text
STRONGEST_POSITIVE_RESULT = THE_SOURCE_FROZEN_NULL_RANK_ONE_SIGNED_COUPLING_CHANNEL_IS_ARBITRARILY_LOG_SMALL_ON_THE_SAME_LITERAL_CLOCK
STRONGEST_OBSTRUCTION = THE_ORTHOGONAL_RESIDUAL_CAN_CARRY_THE_ENTIRE_SIGNED_SCALAR_EVEN_WITH_ZERO_NULL_CHANNEL
OPEN_THEOREM = CONTROL_W_PERP_AGAINST_A_X_BETA_OR_REASSEMBLE_ALL_FOUR_SIGNED_PACKETS_WITH_THE_RESIDUAL_RETAINED
REUSABLE_STRUCTURE = SAME_CLOCK_TO_HAAR_NULL_TO_W_MOMENT_TO_EXACT_RANK_ONE_SPLIT_TO_RESIDUAL_FIREWALL
ROUND2_CLUE = AUDIT_FULL_FOUR_PACKET_SIGNED_REASSEMBLY_WITH_THE_ORTHOGONAL_RESIDUAL_EXPLICITLY_PRESENT
```

```text
TPC259_ROUTE_ADVANCE = YES_SCOPED_NULL_CHANNEL
TPC259_ARITHMETIC_ADVANCE = YES_SCOPED_SIGNED_COUPLING_CHANNEL
TPC259_W_NULL_MOMENT = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER
TPC259_NULL_CHANNEL = PROVED_SOURCE_BACKED_o_ONE
TPC259_RESIDUAL_DECOMPOSITION = PROVED_EXACT
TPC259_RESIDUAL_FULL_SCALAR = OPEN
TPC259_FIXED_POWER_SAVING = NONE
TPC259_L2 = NONE
TPC259_FULL_GATE_B = OPEN
TPC259_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC259_FIXED_ATOM_CREDIT = 0
TPC259_TWIN_PRIME_RESULT = NONE
```

## 0.52 已发布：TPC-258 source-frozen transverse null direction

项目：`papers/tpc-258-source-frozen-transverse-null-direction/`

类型：**PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_FOR_LITERAL_V59_ADJOINT**。

TPC-258 takes the exact four-block frame from TPC-257 and uses only the two
limiting descendant curvature constants
`L1=log(3456/3125)` and `L2=log(884736/823543)` to define the source-frozen
unit vector
`z_null=(L2 z1-L1 z2)/sqrt(L1^2+L2^2)`.  Since
`kappa1=L1/2` and `kappa2=L2/2`, the leading `B_Q` diagonal cancels exactly:

```text
<z_null,A_x beta>=o(x^(7/6)/log^3(x)).
```

The proof retains the literal masks, deleted diagonal, complex kernel,
hard-window lane, and child-jump lane inherited from TPC-255.  An explicit
`O(1/log x)` refinement is recorded only conditionally; an adversarial
`1/sqrt(log x)` error shows why the released `o(1)` statement does not imply
a fixed-power saving.

```text
STRONGEST_POSITIVE_RESULT = A_SOURCE_FROZEN_UNIT_VECTOR_IN_THE_TRANSVERSE_HAAR_PLANE_CANCELS_THE_EXPLICIT_TPC257_BQ_DIAGONAL_MAIN
STRONGEST_OBSTRUCTION = THE_UNCONDITIONAL_NULL_RESULT_IS_ONLY_o_ONE_AND_DOES_NOT_PAY_ANY_FIXED_POWER_ENDPOINT
OPEN_THEOREM = COUPLE_THE_NULL_DIRECTION_TO_THE_LITERAL_SIGNED_W_BETA_LANE_AND_CONTROL_THE_REMAINING_FULL_OUTPUT
REUSABLE_STRUCTURE = CURVATURE_VECTOR_TO_EXACT_ORTHONORMAL_FRAME_TO_FIXED_NULL_COMBINATION_TO_BOUNDARY_GAP_TO_RATE_FIREWALL
ROUND2_CLUE = TEST_THE_SOURCE_FROZEN_NULL_DIRECTION_AGAINST_THE_LITERAL_SIGNED_W_BETA_COUPLING_ON_THE_SAME_CLOCK_BEFORE_ANY_FULL_REASSEMBLY
```

```text
TPC258_ROUTE_ADVANCE = YES_SCOPED_TRANSVERSE_NULL
TPC258_ARITHMETIC_ADVANCE = YES_SCOPED_LOG_CANCELLATION
TPC258_NULL_DIRECTION = PROVED_SOURCE_FROZEN_UNIT_VECTOR
TPC258_LEADING_DIAGONAL_CANCELLATION = PROVED_SOURCE_BACKED
TPC258_RATE_REFINEMENT = CONDITIONAL_THEOREM_LOG_ONE_OVER_X
TPC258_FIXED_POWER_SAVING = NONE
TPC258_L2 = NONE
TPC258_FULL_GATE_B = OPEN
TPC258_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC258_FIXED_ATOM_CREDIT = 0
TPC258_TWIN_PRIME_RESULT = NONE
```

## 0.51 已发布：TPC-257 four-block Haar lift and a transverse norm floor

项目：`papers/tpc-257-four-block-haar-transverse-norm-floor/`

类型：**PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR_FOR_LITERAL_V59_ADJOINT**。

TPC-257 keeps the literal V59 coefficient, operator, prime shell, and real
clock from TPC-256.  It splits both ordered-rank children once more, before
inspecting any coefficient, and forms the exact orthonormal frame
`z0,z1,z2`.  The same divisor-density cancellation and second-order PNT
curvature give

```text
kappa0=log(32/27)/sqrt(2),
kappa1=log(3456/3125)/2,
kappa2=log(884736/823543)/2,
<zi,A_x beta>=-(9/2*kappa_i+o(1))x^(7/6)/log^3(x).
```

Finite Parseval yields the new source-only transverse floor

```text
||P_span(z1,z2) A_x beta||_2
 =((9/2)sqrt(kappa1^2+kappa2^2)+o(1))x^(7/6)/log^3(x),
sqrt(kappa1^2+kappa2^2)=0.061792126717520...
```

This is a lower-bound obstruction: it refutes automatic negligible-remainder
promotion after one midpoint projection, but it is not an upper `L2` theorem.

```text
STRONGEST_POSITIVE_RESULT = THE_SOURCE_ONLY_TWO_DIMENSIONAL_TRANSVERSE_HAAR_PLANE_HAS_AN_EXPLICIT_SAME_ORDER_LITERAL_ADJOINT_LOWER_FLOOR
STRONGEST_OBSTRUCTION = THE_TRANSVERSE_COMPONENT_CANNOT_BE_ASSUMED_LOWER_ORDER_AFTER_ONE_MIDPOINT_PROJECTION
OPEN_THEOREM = FIND_AND_CERTIFY_A_SOURCE_FROZEN_TRANSVERSE_NULL_DIRECTION_OR_PROVE_A_COLLECTIVE_UPPER_BOUND_WITH_ALL_LITERAL_MASKS_AND_BOUNDARIES_RETAINED
REUSABLE_STRUCTURE = FOUR_BLOCK_RANK_HAAR_FRAME_TO_EXACT_ORTHONORMALITY_TO_SECOND_ORDER_LI_CURVATURE_TABLE_TO_BQ_DIAGONAL_TO_BOUNDED_VARIATION_BOUNDARY_COMPILER_TO_PARSEVAL_FLOOR
ROUND2_CLUE = USE_THE_EXPLICIT_TWO_DIMENSIONAL_TRANSVERSE_HAAR_FLOOR_TO_SEARCH_FOR_A_SOURCE_FROZEN_DIAGONAL_NULL_DIRECTION_BEFORE_ATTEMPTING_ANY_FULL_GATE_B_UPPER_BOUND
```

```text
TPC257_ROUTE_ADVANCE = YES_SCOPED_TRANSVERSE_HAAR
TPC257_ARITHMETIC_ADVANCE = YES_SCOPED_TRANSVERSE_LOWER_FLOOR
TPC257_L2 = NONE
TPC257_FULL_GATE_B = OPEN
TPC257_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC257_FIXED_ATOM_CREDIT = 0
TPC257_TWIN_PRIME_RESULT = NONE
```

## 0.50 已发布：TPC-256 literal beta Haar and diagonal-dominant adjoint asymptotic

项目：`papers/tpc-256-literal-beta-haar-adjoint-asymptotic/`

类型：**PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC**。

On TPC-253's ordered-rank children, every truncated divisor layer has the same
`1/d` density and differs only by an endpoint error.  Thus

```text
|<z_mid,sum_(d|dot,d<=U)mu(d)>|<=U/rho=O(x^(-67/400)).
```

The second-order curvature of the de la Vallée Poussin PNT then gives

```text
<z_mid,beta>
 =[log(32/27)/sqrt(2)]sqrt(x)/log^2 x
  +O(sqrt(x)/log^3 x)>0.
```

TPC-255's exact diagonal/boundary ledger, weighted PNT, combined-unit-row
first moment and crossing counts give

```text
B_Q=(9/2+o(1))x^(2/3)/log x,
R_unit=O(x^(5/6+epsilon)),
R_hard,R_jump=O_psi(x^(55/48+epsilon)),

<z_mid,A_x beta>
 =-[9log(32/27)/(2sqrt(2))+o(1)]x^(7/6)/log^3 x.
```

The boundary exponent gap is `1/48`.  The asymptotic is complex: eventual
negative real part, nonzero scalar and normalized phase `->-1` are proved;
reality and an unqualified principal `Arg -> +pi` are not claimed.  One Haar
projection is not a full-output, `L2`, Gate-B or twin-prime theorem.

```text
STRONGEST_POSITIVE_RESULT = THE_LITERAL_BETA_RANK_MIDPOINT_HAS_AN_EXPLICIT_POSITIVE_ASYMPTOTIC_AND_THE_RETURNED_BQ_DIAGONAL_FORCES_A_NONZERO_NEGATIVE_REAL_LEADING_ADJOINT_HAAR_ASYMPTOTIC
STRONGEST_OBSTRUCTION = ONE_FIXED_HAAR_PROJECTION_DOES_NOT_CONTROL_THE_TRANSVERSE_OR_FULL_OUTPUT_COMPONENT_AND_OUTPUT_UNIT_PIECES_CANNOT_BE_POISSON_SPLIT_BEFORE_EXACT_RECENTERING
OPEN_THEOREM = CONTROL_THE_TRANSVERSE_FULL_OUTPUT_COMPONENT_OF_A_X_BETA_AND_COUPLE_IT_TO_THE_PHYSICAL_W_LANE_ON_THE_SAME_V59_CLOCK_WITH_THE_SHELL_MASKS_DIAGONAL_AND_WINDOW_RETAINED
REUSABLE_STRUCTURE = CONSECUTIVE_INTERVAL_DIVISOR_DENSITY_CANCELLATION_TO_SECOND_ORDER_PNT_CURVATURE_TO_EXPLICIT_BETA_HAAR_MAIN_TO_BQ_DIAGONAL_AMPLIFICATION_TO_FIRST_MOMENT_BOUNDARY_LOCALIZATION_TO_ONE_OVER_48_SEPARATION
ROUND2_CLUE = EXPLOIT_EXACT_DIVISOR_DENSITY_CANCELLATION_BEFORE_ANY_TRIANGLE__THEN_USE_THE_BQ_DIAGONAL_MAIN_AND_H2_OVER_Q_BOUNDARY_MOMENT_TO_ISOLATE_THE_TRANSVERSE_FULL_GATE_B_REMAINDER
```

## 0.49 已发布：TPC-255 exact adjoint diagonal and hard-boundary compiler

项目：`papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/`

类型：**PROVED_EXACT_SOURCE_BACKED_L1_ADJOINT_DIAGONAL_HARD_WINDOW_CHILD_JUMP_COMPILER**。

For `q` in the literal shell and `q` not dividing `t`, let

```text
v_(q,t)(u)=1_(q does not divide u)
            [1_(u=t mod q)-1/(q-1)].
```

V43 band-limited Poisson applied to the reflected-conjugate profile proves
that its complete-lattice adjoint row is zero when `H>2Q`; no kernel evenness
or self-adjointness is assumed.  Exact diagonal deletion and boundary
bookkeeping then give

```text
<z_mid,A_x beta>
 = -B_Q<z_mid,beta> + input-unit correction
   - hard-window leakage + child-jump leakage.
```

All outer `q` weights, both unit masks, the deleted diagonal, kernel
conjugations and the real-clock ordered-rank split remain literal.  The output
mask may not be split before Poisson: its two pieces have opposite nonzero
means and are centered only jointly.  This is an exact arithmetic-structure
advance, not an estimate; no surviving lane has a proved sign, nonzero value,
logarithmic saving or power saving.

```text
STRONGEST_POSITIVE_RESULT = THE_LITERAL_V59_ADJOINT_HAAR_SCALAR_IS_EXACTLY_ONE_BQ_WEIGHTED_BETA_MIDPOINT_PLUS_INPUT_UNIT_HARD_WINDOW_AND_CHILD_JUMP_CORRECTIONS_AFTER_THE_COMPLETE_CENTERED_ALIAS_VANISHES
STRONGEST_OBSTRUCTION = COMPLETE_LATTICE_POISSON_REMOVES_ONLY_THE_CENTERED_ALIAS_WHILE_DIAGONAL_DELETION_RETURNS_SHELL_SCALE_BQ_AND_NO_LOCKED_THEOREM_CONTROLS_IT_COLLECTIVELY_WITH_THE_BOUNDARIES
OPEN_THEOREM = ESTIMATE_THE_SIGNED_SUM_OF_THE_BQ_BETA_MIDPOINT_INPUT_UNIT_HARD_WINDOW_AND_CHILD_JUMP_LANES_ON_ONE_V59_CLOCK_WITHOUT_PRIME_SHELL_OR_MASK_TRIANGLE
REUSABLE_STRUCTURE = LITERAL_ADJOINT_TEST_TO_COMPLETE_UNIT_CENTERED_LATTICE_TO_POISSON_ZERO_TO_DIAGONAL_RETURN_TO_OUTER_HARD_WINDOW_TO_INNER_CHILD_JUMP_TO_ONE_LITERAL_BETA_LINEAR_FORM
ROUND2_CLUE = ATTACK_THE_BQ_WEIGHTED_LITERAL_BETA_RANK_MIDPOINT_TOGETHER_WITH_THE_HARD_WINDOW_AND_CHILD_JUMP_CORRECTIONS__DO_NOT_DECLARE_THE_POISSON_ZERO_A_PAYMENT_AND_DO_NOT_SEPARATE_THE_UNIT_MASK_OR_PRIME_SHELL
```

## 0.48 已发布：TPC-254 source-backed rank-midpoint hybrid-mean closure

项目：`papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/`

类型：**PROVED_SOURCE_BACKED_L1_RANK_MIDPOINT_HYBRID_MEAN_CLOSURE_WITH_ADJOINT_LANE_SOURCE_GAP**。

Fix finite admissible `K` and retain TPC-253's ordered-rank midpoint.  The
locked hybrid maximal Type-I theorem is a sum of nonnegative rows.  Freezing
`gamma_0=1/4` and extracting the unit-weight `m=1` row gives, for every fixed
`M>0`,

```text
max(|W_L|,|W_R|)<<_(M,K)x(log x)^(-M),
|W_L/ell-W_R/r|<<_(M,K)(log x)^(-M),
|<z_mid,w>|<<_(M,K)x^(1/2)(log x)^(-M).
```

Both rank children are consecutive integer intervals for every real `x`.
The quantifier order fixes `K` and `gamma_0` before the requested log strength;
no uniformity as `K` grows is claimed.  Since
`x^eta/(log x)^M -> infinity`, the result is not a fixed-power saving.

The second midpoint moment remains exactly
`<z_mid,A_x beta>=<A_x^*z_mid,beta>`.  Cauchy gives the safe upper transfer,
but no frozen source estimates the literal adjoint test.  A real zero-diagonal
derangement realizes arbitrary signed scale, and at `N=2` the Cauchy constant
one is exact.  These controls are synthetic and do not refute the literal V59
operator.

```text
STRONGEST_POSITIVE_RESULT = THE_LITERAL_V59_W_RANK_MIDPOINT_MOMENT_HAS_SOURCE_BACKED_X_ONE_HALF_TIMES_ARBITRARY_FIXED_LOG_POWER_CONTROL
STRONGEST_OBSTRUCTION = THE_SECOND_LITERAL_MIDPOINT_MOMENT_IS_THE_UNESTIMATED_ADJOINT_FORM_A_X_STAR_Z_MID_AGAINST_BETA_AND_NORM_ONLY_CAUCHY_IS_SHARP
OPEN_THEOREM = ESTIMATE_THE_LITERAL_A_X_STAR_Z_MID_BETA_LINEAR_FORM_ON_THE_SAME_V59_CLOCK_WITH_PRIME_SHELL_Q_WEIGHT_BOTH_UNIT_MASKS_DELETED_DIAGONAL_AND_K_H_RETAINED
REUSABLE_STRUCTURE = MAXIMAL_INTERVAL_TYPE_I_TO_NONNEGATIVE_M1_EXTRACTION_TO_RANK_CHILD_MEANS_TO_NORMALIZED_HAAR_MOMENT_TO_LITERAL_ADJOINT_TEST
ROUND2_CLUE = PUSH_THE_FIXED_RANK_MIDPOINT_HAAR_TEST_THROUGH_A_X_STAR_AND_ESTIMATE_THE_LITERAL_BETA_LINEAR_FORM_ON_THE_SAME_CLOCK_BEFORE_ANY_COVARIANCE_OR_MARGIN_PROMOTION__DO_NOT_REUSE_WHOLE_SHELL_OR_AP_AVERAGES
```

## 0.47 已发布：TPC-253 source-frozen rank-midpoint contrast compiler

项目：`papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/`

类型：**PROVED_STRUCTURAL_L1_SOURCE_FROZEN_RANK_MIDPOINT_CONTRAST_COMPILER**。

TPC-253 fixes `L` as the first `floor(N/2)` coordinates of the ordered physical
interval and `R` as the remainder before inspecting any coefficient, margin or
sign.  Its normalized Haar contrast satisfies

```text
M_mid=M_coarse+z tensor z,
C_long(mid)-C_long(coarse)=conjugate(<z,w>)<z,A_x beta>,
Q_trans(mid)-Q_trans(coarse)=-conjugate(<z,w>)<z,A_x beta>.
```

The exact partial-sum compiler includes both longitudinal terms and the
within-child covariance.  Integral clocks crosswalk to `floor(3x/4)`, while the
rank definition remains primary for nonintegral `x`.  Literal substitution
retains the complete TPC-247 kernel and the safe identity
`<z,A_x beta>=<A_x^*z,beta>` without self-adjointness.  Constant and signed
synthetic controls prove that source-free geometry cannot decide sign, nonzero
value or scale; they are not actual V59 replay.

```text
STRONGEST_POSITIVE_RESULT = ONE_COEFFICIENT_INDEPENDENT_PHYSICAL_RANK_MIDPOINT_WITH_EXACT_HAAR_PROJECTOR_PARTIAL_SUM_COVARIANCE_TRANSFER_LITERAL_KERNEL_AND_SAFE_ADJOINT_COMPILER
STRONGEST_OBSTRUCTION = NO_LOCKED_THEOREM_ESTIMATES_EITHER_ACTUAL_MIDPOINT_IMBALANCE_ON_ONE_COMMON_GROWING_V59_CLOCK
OPEN_THEOREM = ESTIMATE_THE_LITERAL_RANK_MIDPOINT_W_AND_A_X_BETA_MOMENTS_OR_THEIR_PRODUCT_WITH_THE_REQUIRED_PROJECTED_RADIUS_ON_ONE_CLOCK
REUSABLE_STRUCTURE = ORDERED_PHYSICAL_INTERVAL_TO_RANK_MIDPOINT_TO_NORMALIZED_HAAR_CONTRAST_TO_PARTIAL_SUM_IMBALANCE_TO_LITERAL_ADJOINT_FORM
ROUND2_CLUE = AUDIT_THE_TWO_LITERAL_RANK_MIDPOINT_IMBALANCES_WITH_EXISTING_PRIME_AND_HYBRID_MEAN_THEOREMS_BEFORE_ANY_DYADIC_EXTENSION
```

## 0.46 已发布：TPC-252 declared-partition refinement degeneracy

项目：`papers/tpc-252-declared-partition-refinement-degeneracy/`

类型：**PROVED_STRUCTURAL_L1_DECLARED_PARTITION_REFINEMENT_DEGENERACY**。

For every binary split of one declared block, the normalized child contrast
`z` gives the exact rank-one update

```text
M_P'=M_P+z tensor z,
C_long(P')-C_long(P)=conjugate(<z,w>)<z,g>,
Q_trans(P')-Q_trans(P)=-conjugate(<z,w>)<z,g>.
```

The exact transverse radius is nonincreasing.  A fixed auxiliary probe family
has the corresponding rank-one projected-Gram subtraction, while native
common input/output repartition is excluded because its probe indexing changes.
At the singleton partition every projected probe, Gram and coherence quantity
vanishes, so for fixed `E>=0`,

```text
max_P [|C_long(P)|-R_coh(P)-E]_+=[|C_x|-E]_+.
```

Thus adaptive optimization over every legal declared partition adds exactly
zero strength over the direct external bound.  One fixed synthetic source
shows existential partition dependence; a stable fixed source refutes the
every-source version.  Neither fixture is literal numerical V59 arithmetic.

```text
STRONGEST_POSITIVE_RESULT = EXACT_BINARY_RANK_ONE_COVARIANCE_TRANSFER_TRUE_RADIUS_MONOTONICITY_SINGLETON_COLLAPSE_AND_ALL_PARTITION_MARGIN_OPTIMALITY
STRONGEST_OBSTRUCTION = FREE_PARTITION_OPTIMIZATION_CAN_MOVE_THE_FULL_KNOWN_SCALAR_INTO_C_LONG_AND_ERASE_THE_PROJECTED_RADIUS_SO_THE_OPTIMUM_IS_TAUTOLOGICAL
OPEN_THEOREM = FREEZE_ONE_NONTRIVIAL_SOURCE_ONLY_PARTITION_AND_ESTIMATE_ITS_LITERAL_V59_CONTRAST_AND_PROJECTED_RADIUS_ON_A_COMMON_CLOCK
REUSABLE_STRUCTURE = BLOCK_AVERAGING_TO_BINARY_CONTRAST_TO_RANK_ONE_COVARIANCE_TRANSFER_TO_SINGLETON_OPTIMIZATION_FIREWALL
ROUND2_CLUE = FREEZE_A_NONTRIVIAL_SOURCE_ONLY_PARTITION_TREE_AND_TEST_ONE_LITERAL_V59_BINARY_CONTRAST_BEFORE_ANY_MARGIN_OPTIMIZATION
```

## 0.45 已发布：TPC-251 literal V59 declared-block longitudinal/transverse margin compiler

项目：`papers/tpc-251-literal-v59-declared-block-longitudinal-transverse-margin-compiler/`

类型：**PROVED_STRUCTURAL_L1_LITERAL_V59_DECLARED_BLOCK_LONGITUDINAL_TRANSVERSE_MARGIN_COMPILER**。

On an exhaustive declared hard partition, specialize the literal TPC-247
weights to one and choose the declared block-flat unit vector `u_c`.  With

```text
g_c=P_cA_x beta,
C_x=sum_c <w_c,g_c>,
```

TPC-251 proves the exact split and projected Gram identity

```text
C_x=C_long+Q_trans,
G_c^perp(b,b')=G_c(b,b')-conj(m_cb)m_cb'.
```

Applying TPC-250 only to the projected probes gives

```text
|C_x-C_long|<=R_trans<=R_coh.
```

Thus every independently certified `|F-C_x|<=E` satisfies
`|F|>=[|C_long|-R_coh-E]_+`, and the strict positive margin certifies
nonvanishing.  A block-flat equality fixture has `C_long=1`, transverse term
`-1`, and total scalar zero, proving that the endpoint cannot be weakened.
The partition and block-flat direction remain declared modeling choices, and
TPC-243 does not automatically provide `E`.

```text
STRONGEST_POSITIVE_RESULT = EXACT_LITERAL_LAMBDA_ONE_LONGITUDINAL_TRANSVERSE_SPLIT_WITH_PROJECTED_GRAM_COHERENCE_RADIUS_AND_CONDITIONAL_STRICT_MARGIN_COMPILER
STRONGEST_OBSTRUCTION = EQUALITY_CAN_CANCEL_EXACTLY_AND_NO_SOURCE_THEOREM_YET_PAYS_THE_ACTUAL_V59_LONGITUDINAL_SURPLUS_PROJECTED_COHERENCE_OR_EXTERNAL_ERROR
OPEN_THEOREM = PROVE_ON_ONE_LITERAL_V59_CLOCK_THAT_ABS_C_LONG_EXCEEDS_R_COH_PLUS_A_SEPARATELY_CERTIFIED_E
REUSABLE_STRUCTURE = SOURCE_OPERATOR_TO_DECLARED_PROJECTION_TO_RANK_ONE_GRAM_SUBTRACTION_TO_COHERENCE_RADIUS_TO_EXTERNAL_ERROR_MARGIN
ROUND2_CLUE = ESTIMATE_THE_LITERAL_BLOCK_LONGITUDINAL_CENTER_AND_PROJECTED_COHERENCE_RADIUS_ON_ONE_V59_CLOCK_OR_BUILD_A_SOURCE_LEVEL_MARGIN_OBSTRUCTION
```

## 0.44 已发布：TPC-250 coherence-controlled Gram quadratic sharpness

项目：`papers/tpc-250-coherence-controlled-gram-quadratic-sharpness/`

类型：**PROVED_STRUCTURAL_L1_COHERENCE_CONTROLLED_GRAM_QUADRATIC_SHARPNESS**。

For `g=sum_i lambda_iv_i`, let

```text
D=sum_i |lambda_i|^2||v_i||^2,
L=sum_i |lambda_i|||v_i||.
```

With total active-coherence convention `mu=0` for fewer than two active
terms, TPC-250 proves

```text
| ||g||^2-D |<=mu(L^2-D),
[D-mu(L^2-D)]_+<=||g||^2<=D+mu(L^2-D).
```

For `D>0`, `mu(L^2/D-1)<1` is a strict noncancellation certificate.
Independent/global TPC-249 radii inherit the envelope.  Equicorrelated,
anti-correlated, simplex, negative-raw-floor and same-marginal PSD examples
prove the universal constants and floor sharp and rule out a marginal-only
improvement.

```text
STRONGEST_POSITIVE_RESULT = SHARP_TOTAL_COHERENCE_ENVELOPE_AND_STRICT_FINITE_NONCANCELLATION_CERTIFICATE_FOR_THE_EXACT_GRAM_QUADRATIC
STRONGEST_OBSTRUCTION = IDENTICAL_MARGINAL_NORMS_AND_WEIGHTS_PERMIT_FULL_ALIGNMENT_OR_EXACT_CANCELLATION
OPEN_THEOREM = FAVORABLE_ASYMPTOTICS_FOR_LITERAL_V59_PROJECTED_OR_UNPROJECTED_DIAGONAL_MASS_AND_COHERENCE
REUSABLE_STRUCTURE = DIAGONAL_ENERGY_PLUS_WEIGHTED_ONE_NORM_PLUS_ACTIVE_COHERENCE_TO_RADIUS_INHERITANCE
ROUND2_CLUE = PROJECT_THE_LITERAL_LAMBDA_EQUALS_ONE_PROBES_ONTO_A_DECLARED_BLOCK_LONGITUDINAL_DIRECTION_AND_TEST_THE_STRICT_MARGIN
```

## 0.43 已发布：TPC-249 sharp weighted shared-lane contraction

项目：`papers/tpc-249-sharp-weighted-shared-lane-contraction/`

类型：**PROVED_STRUCTURAL_L1_SHARP_WEIGHTED_SHARED_LANE_CONTRACTION**。

Weights contract inside each physical shared lane to
`g_c=sum_b lambda_cbv_cb`.  Independent centered lane balls have exact scalar
radius

```text
R=sum_c rho_c sqrt(lambda_c*G_c lambda_c),
```

with explicit reverse realization; a global budget has the direct-sum square
root radius.  The tagged triangle radius dominates exactly, with equality
under common-ray alignment.  Repeated probes and opposite weights give zero
exact radius but positive tagged radius.

```text
STRONGEST_POSITIVE_RESULT = EXACT_SOURCE_ORIENTED_WEIGHTED_GRAM_SUPPORT_RADIUS_WITH_REVERSE_REALIZATION
STRONGEST_OBSTRUCTION = FIXED_MARGINAL_NORMS_ALLOW_THE_TRUE_RADIUS_TO_RANGE_FROM_TAGGED_SATURATION_TO_ZERO
OPEN_THEOREM = ASYMPTOTIC_BOUND_FOR_LITERAL_V59_GRAM_QUADRATIC_FORMS
REUSABLE_STRUCTURE = WITHIN_LANE_WEIGHTED_VECTOR_PLUS_GRAM_SUPPORT_PLUS_BUDGET_LEDGER
ROUND2_CLUE = ESTIMATE_LITERAL_GRAM_QUADRATIC_FORMS_OR_BOUND_THEM_FROM_COMPUTABLE_COHERENCE_DATA
```

## 0.42 已发布：TPC-248 shared-lane Gram-ellipsoid feasible set

项目：`papers/tpc-248-shared-lane-gram-ellipsoid-feasible-set/`

类型：**PROVED_STRUCTURAL_L1_SHARED_LANE_GRAM_ELLIPSOID_FEASIBLE_SET**。

For every fixed TPC-247 output block, the probes `v_cb=A_cb beta_b` share one
physical lane.  Their radius-ball joint covariance image is exactly

```text
{y in ran(G_c): y*G_c^dagger y<=rho_c^2}.
```

The Moore--Penrose energy is the exact minimum preimage norm.  Exact spheres
fill the solid ellipsoid iff an orthogonal kernel direction exists; otherwise
they give the equality shell.  A global norm budget produces one coupled
sum-energy ellipsoid, and repeated probes refute promotion from local disk
marginals to a polydisk.

```text
STRONGEST_POSITIVE_RESULT = EXACT_SHARED_LANE_GRAM_ELLIPSOID_WITH_BALL_SPHERE_AND_GLOBAL_BUDGET_CLASSIFICATION
STRONGEST_OBSTRUCTION = LOCAL_DISK_MARGINALS_CAN_COLLAPSE_TO_A_DIAGONAL_DISK_AND_DO_NOT_CERTIFY_CARTESIAN_REALIZABILITY
OPEN_THEOREM = SHARP_WEIGHTED_GROUP_SUPPORT_RADIUS_FOR_THE_LITERAL_TPC247_PROBES
REUSABLE_STRUCTURE = ANALYSIS_OPERATOR_PLUS_GRAM_RANGE_PLUS_PSEUDOINVERSE_ENERGY_PLUS_ORTHOGONAL_SLACK
ROUND2_CLUE = CONTRACT_WEIGHTED_PROBES_INSIDE_EACH_SHARED_OUTPUT_LANE_BEFORE_SUMMING_ACROSS_OUTPUT_BLOCKS
```

## 0.41 已发布：TPC-247 literal V59 source-operator attachment

项目：`papers/tpc-247-literal-v59-source-operator-attachment/`

类型：**PROVED_STRUCTURAL_L1_LITERAL_V59_SOURCE_OPERATOR_ATTACHMENT_WITH_NORM_OBSTRUCTION**。

The complete V59 scalar is exactly `C_x=<w,A_x beta>` on physical integer
coordinates.  Disjoint support projections give `A_cb=P_cA_xP_b` and

```text
C_x=sum_(b,c)<w_c,A_cb beta_b>,
```

with every admissible `(q,t,u)` triple exactly once.  Tagged external copies
turn this into one covariance, but repeat each output lane over all input
blocks:

```text
||W_ext||^2=m||w||^2.
```

The separated `B` norm can remain positive when `A_x beta=0`, so it is not a
payable primitive-frequency attachment by itself.

```text
STRONGEST_POSITIVE_RESULT = EXACT_LITERAL_V59_SOURCE_OPERATOR_AND_TAGGED_TWO_LANE_BLOCK_COVARIANCE
STRONGEST_OBSTRUCTION = OUTPUT_LANE_SQRT_M_DUPLICATION_AND_LOSS_OF_INPUT_BLOCK_CANCELLATION_IN_THE_EXTERNAL_NORM
OPEN_THEOREM = EXACT_SHARED_OUTPUT_LANE_JOINT_FEASIBLE_SET_AND_SHARP_WEIGHTED_AGGREGATE_RADIUS
REUSABLE_STRUCTURE = SOURCE_OPERATOR_PLUS_HARD_SUPPORT_PROJECTIONS_PLUS_TAGGED_COVARIANCE_LOSS_LEDGER
ROUND2_CLUE = CHARACTERIZE_THE_SHARED_OUTPUT_LANE_JOINT_FEASIBLE_SET_BEFORE_ANY_CARTESIAN_PRODUCT_PROMOTION
```

## 0.40 已发布：TPC-246 weighted covariance-disk reassembly

项目：`papers/tpc-246-weighted-covariance-disk-reassembly/`

类型：**PROVED_STRUCTURAL_L1_WEIGHTED_COVARIANCE_DISK_REASSEMBLY**。

For a finite joint family with local marginals in `c_h+r_h Dbar`, arbitrary
complex covariance weights give the unconditional enclosure

```text
aggregate subset C+R Dbar,
C=sum_h lambda_h c_h,
R=sum_h |lambda_h|r_h.
```

If the joint family is the complete Cartesian product, this containment is an
exact identity.  For `R>0`, every target deviation `d` is realized by

```text
e_h=(conjugate(lambda_h)/|lambda_h|)(r_h/R)d
```

on nonzero-weight blocks.  Hence zero is feasible iff `|C|<=R`, and the exact
minimum modulus is `max(|C|-R,0)`.  For TPC-244 common multipliers the weights
are `|C_h|^2`, not arbitrary complex scalars.  Conditional on the literal
TPC-243 attachment, the hard-window image is contained in the radius-inflated
disk and is uniformly nonzero when

```text
|C_agg| > R_agg + epsilon||W||||B||.
```

```text
TPC246_COUPLED_FAMILY_CONTAINMENT = PROVED
TPC246_WEIGHTED_DISK_IDENTITY = PROVED_EXACT
TPC246_REVERSE_REALIZATION = PROVED_EXPLICIT
TPC246_AGGREGATE_ZERO_CRITERION = PROVED_EXACT
TPC246_COMMON_MULTIPLIER_SPECIALIZATION = PROVED_STRUCTURAL
TPC246_HARD_WINDOW_RADIUS_INFLATION = PROVED_CONDITIONAL_ON_ATTACHMENT
TPC246_HARD_WINDOW_IMAGE_EXACTNESS = NOT_CLAIMED
TPC246_POSITIVE_RADIUS_CIRCLE_AS_DISK = FORBIDDEN
TPC246_ARBITRARY_COMPLEX_WEIGHT_AS_COMMON_MULTIPLIER = FORBIDDEN
TPC246_INDEPENDENT_SOURCE_REALIZABILITY = OPEN
TPC246_LITERAL_V59_TWO_LANE_ATTACHMENT = OPEN
TPC246_CANONICAL_BLOCK_DIRECTIONS = OPEN
TPC246_PAYABLE_ARITHMETIC_MARGIN = OPEN
TPC246_ARITHMETIC_ADVANCE = NO
TPC246_FIXED_ATOM_CREDIT = 0
TPC246_L2 = NONE
TPC246_FULL_GATE_B = OPEN
TPC246_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC246_STATUS = PROVED_STRUCTURAL_L1_WEIGHTED_COVARIANCE_DISK_REASSEMBLY
TPC246_ROUND2_CLUE = SOURCE_NATIVE_WEIGHTED_LONGITUDINAL_DOMINANCE_BEYOND_TRANSVERSE_RADIUS_AND_WINDOW_LEAKAGE
```

strongest positive result：exact weighted disk identity、explicit reverse realization、
sharp zero/margin dichotomy 与 one-transfer window enclosure；strongest obstruction：
`|C_agg|<=R_agg` 时 complete-product model exact cancels，且 local marginals alone do
not imply source product realizability；open theorem：literal V59 two-lane blocks、
source-native projections 与 payable strict aggregate margin；reusable structure：
`local disks -> weighted exact disk -> zero/margin dichotomy -> window-inflated disk`；
`ROUND2_CLUE`：
`SOURCE_NATIVE_WEIGHTED_LONGITUDINAL_DOMINANCE_BEYOND_TRANSVERSE_RADIUS_AND_WINDOW_LEAKAGE`。

## 0.39 已发布：TPC-245 sharp longitudinal--transverse covariance disks

项目：`papers/tpc-245-sharp-longitudinal-transverse-covariance-disks/`

类型：**PROVED_STRUCTURAL_L1_SHARP_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISKS**。

For a complex Hilbert space with conjugate-linear first slot, fix a unit vector
and write

```text
b=<u,B>, w=<u,W>,
c=conjugate(w)b,
r=sqrt(E_B E_W).
```

The exact feasible set of `<W,B>` at fixed moments and transverse energies is
`c+r Dbar` when `dim_C(u^perp)>=2`; it is `c+r T` for one nondegenerate
transverse direction, a singleton when the radius vanishes, and empty in
dimension zero if positive transverse energy is prescribed.  Hence the zero
criterion, exact minimum modulus, and phase cone are all sharp.

```text
TPC245_EXACT_DECOMPOSITION = PROVED_CENTER_PLUS_TRANSVERSE_COVARIANCE
TPC245_DIM_GE_2_FEASIBLE_SET = PROVED_CLOSED_DISK
TPC245_DIM_EQ_1_FEASIBLE_SET = PROVED_CIRCLE_OR_SINGLETON
TPC245_DIM_EQ_0_FEASIBLE_SET = PROVED_SINGLETON_OR_UNREALIZABLE
TPC245_ZERO_FEASIBILITY = PROVED_DIMENSION_SENSITIVE
TPC245_MINIMUM_MODULUS = PROVED_EXACT
TPC245_PHASE_SECTOR = PROVED_SHARP_WHEN_RADIUS_LT_CENTER
TPC245_TPC219_RELATION = PROJECTION_LINEAGE_ONLY_NOT_LITERAL_OBJECT_IDENTITY
TPC245_CANONICAL_BLOCK_DIRECTION = OPEN
TPC245_LITERAL_V59_TWO_LANE_ATTACHMENT = OPEN
TPC245_PAYABLE_MOMENTS_AND_ENERGIES = OPEN
TPC245_SIGNED_ARITHMETIC_MARGIN = NONE
TPC245_ARITHMETIC_ADVANCE = NO
TPC245_FIXED_ATOM_CREDIT = 0
TPC245_L2 = NONE
TPC245_FULL_GATE_B = OPEN
TPC245_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC245_STATUS = PROVED_STRUCTURAL_L1_SHARP_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISKS
TPC245_ROUND2_CLUE = WEIGHTED_MINKOWSKI_REASSEMBLY_OF_INDEPENDENT_LOCAL_DISKS_WITH_HARD_WINDOW_ERROR
```

strongest positive result：complete disk/circle/singleton classification、exact
minimum modulus 与 sharp phase cone；strongest obstruction：one transverse direction
cannot fill disk interior，且 source chain 没有 canonical one-dimensional `u_h`；
open theorem：source-native block projection、literal V59 two-lane attachment 与
payable moments/energies；reusable structure：center-radius feasible set、zero margin、
phase cone；`ROUND2_CLUE`：
`WEIGHTED_MINKOWSKI_REASSEMBLY_OF_INDEPENDENT_LOCAL_DISKS_WITH_HARD_WINDOW_ERROR`。

## 0.38 已发布：TPC-244 common-multiplier sign localization

项目：`papers/tpc-244-common-multiplier-sign-localization/`

类型：**PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION**。

For `H=direct_sum_h H_h` and common block multipliers,

```text
B=direct_sum_h C_h b_h,
W=direct_sum_h C_h w_h,
<W,B>=sum_h |C_h|^2<w_h,b_h>.
```

Therefore a simultaneous outer unit phase on both lanes leaves covariance and
both norms exactly invariant.  Internal Möbius signs inside the sum defining `C_h`
still affect `|C_h|` and are not erased.

For nonorthogonal embeddings and real signs,

```text
Q(s)=D+sum_(h<k)s_hs_kS_hk,
Q(s)-Q(1)=-2sum_(h<k,s_h!=s_k)S_hk.
```

Walsh orthogonality proves that `Q` is invariant for all sign patterns iff every
symmetrized edge `S_hk` vanishes.  Conditional on a literal common two-lane
attachment, TPC-243 further yields

```text
|Q_I(s)-Q_I(t)|<=2epsilon||W||||B||.
```

```text
TPC244_COMMON_MULTIPLIER_COVARIANCE = PROVED_SUM_ABS_C_H_SQUARED_LOCAL_COVARIANCE
TPC244_COMMON_UNIT_PHASE_INVARIANCE = PROVED_EXACT_COVARIANCE_AND_BOTH_NORMS
TPC244_INTERNAL_MOBIUS_CANCELLATION = PRESERVED_NOT_ESTIMATED
TPC244_NONORTHOGONAL_SIGN_CUT = PROVED_EXACT
TPC244_ALL_SIGN_INVARIANCE = PROVED_IFF_EVERY_SYMMETRIZED_EDGE_ZERO
TPC244_HARD_WINDOW_PAIRWISE_VARIATION = PROVED_AT_MOST_TWO_EPSILON_COEFFICIENT_NORM_PRODUCT
TPC244_V59_SPECIALIZATION = CONDITIONAL_ON_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT
TPC244_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT = OPEN
TPC244_COEFFICIENT_NORM_PAYMENT = OPEN
TPC244_SIGNED_C_H_CANCELLATION = NONE
TPC244_ARITHMETIC_ADVANCE = NO
TPC244_FIXED_ATOM_CREDIT = 0
TPC244_L2 = NONE
TPC244_FULL_GATE_B = OPEN
TPC244_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC244_STATUS = PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION
TPC244_ROUND2_CLUE = WITHIN_BLOCK_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISK_BEFORE_ANY_OUTER_SIGN_ARGUMENT
```

strongest positive result：common outer phase exact invisible、nonorthogonal cut
polynomial complete、hard-window factor-two leakage；strongest obstruction：outer
`C_h` sign cannot control same-block main covariance；open theorem：literal V59
phasewise primitive two-lane attachment with payable norms；reusable structure：
common multiplier diagonal、Walsh cut coefficients、TPC-243 transfer；
`ROUND2_CLUE`：`WITHIN_BLOCK_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISK`。

## 0.37 已发布：TPC-243 hard-window near-isometry and signed bilinear transfer

项目：`papers/tpc-243-hard-window-near-isometry-bilinear-transfer/`

类型：**PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER**。

Let `F` be a finite `delta`-separated subset of the circle, let `I` contain `N`
consecutive integers, and set `Tz(n)=sum_alpha z_alpha e(n alpha)`.  With

```text
K=floor(1/(2delta)),
R_delta=delta^(-1)H_K,
epsilon=R_delta/N,
```

the hard-window Gram has diagonal `N` and every absolute off-diagonal row sum at
most `R_delta`.  Hermitian Schur/Gershgorin therefore proves

```text
[1-epsilon]_+||z||_2^2 <= N^(-1)||Tz||_2^2 <= (1+epsilon)||z||_2^2,
|N^(-1)<Tz,Tw>-<z,w>| <= epsilon||z||_2||w||_2.
```

For distinct primitive frequencies of height at most `U`, take `delta=U^(-2)`.
At the literal V59 scales `N=x/2+O(1)` and `U=x^(133/400)`,

```text
epsilon=(133/100+o(1))x^(-67/200)log x=x^(-67/200+o(1)).
```

With `X=N^(-1/2)Tz`, `Y=N^(-1/2)Tw`, the TPC-242 selected mode
`F_1=<Y,X>` approximates `<w,z>` with this oriented error.  The result transports
signed coefficient information but neither identifies the literal physical lanes nor
creates arithmetic cancellation.

```text
TPC243_HARD_WINDOW_DIRICHLET_GRAM = PROVED_EXACT
TPC243_GEOMETRIC_SUM_BOUND = PROVED_ONE_OVER_TWO_CIRCULAR_DISTANCE
TPC243_HARMONIC_CIRCLE_PACKING = PROVED_DELTA_INVERSE_H_K
TPC243_TWO_SIDED_NEAR_ISOMETRY = PROVED_ONE_PLUS_MINUS_EPSILON
TPC243_SIGNED_BILINEAR_TRANSFER = PROVED_WITH_ERROR_EPSILON_NORM_PRODUCT
TPC243_PRIMITIVE_HEIGHT_SPECIALIZATION = PROVED_R_U_EQUALS_U_SQUARED_H_FLOOR_U_SQUARED_OVER_TWO
TPC243_V59_EPSILON = PROVED_133_OVER_100_PLUS_O_ONE_TIMES_X_MINUS_67_OVER_200_LOG_X
TPC243_TPC242_SELECTED_MODE_TRANSFER = PROVED_CONDITIONAL_ON_COEFFICIENT_LANE_ATTACHMENT
TPC243_LITERAL_TOP_PRIME_ATTACHMENT = OPEN
TPC243_LITERAL_C_H_SIGNED_CANCELLATION = NONE
TPC243_ARITHMETIC_ADVANCE = NO
TPC243_FIXED_ATOM_CREDIT = 0
TPC243_L2 = NONE
TPC243_FULL_GATE_B = OPEN
TPC243_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC243_STATUS = PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER
TPC243_ROUND2_CLUE = COMMON_MULTIPLIER_SIGN_AUDIT_FOR_LITERAL_C_H_IN_THE_TWO_POLARIZED_LANES
```

strongest positive result：hard rectangular primitive-frequency synthesis is a
two-sided `1+o(1)` near-isometry and preserves signed coefficient covariance；
strongest obstruction：window geometry cannot manufacture cancellation beyond the
coefficient covariance and its `epsilon||z||||w||` error；open theorem：source-backed
literal two-lane attachment and signed covariance bound；reusable structure：Dirichlet
Gram、harmonic circular packing、Hermitian perturbation and oriented TPC-242 mode
transport；`ROUND2_CLUE`：
`COMMON_MULTIPLIER_SIGN_AUDIT_FOR_LITERAL_C_H_IN_THE_TWO_POLARIZED_LANES`。

## 0.36 已发布：TPC-242 phase-Fourier collision separation

项目：`papers/tpc-242-phase-fourier-collision-separation/`

类型：**PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER**。

For a complex Hilbert space with conjugate-linear first slot, define

```text
E_j=||X+i^jY||^2,
F_k=(1/4)sum_(j=0)^3 i^(kj)E_j.
```

The complete literal-convention spectrum is

```text
F_0=||X||^2+||Y||^2,
F_1=<Y,X>,
F_2=0,
F_3=<X,Y>.
```

A genuinely phase-independent additive scalar contributes only to `F_0`.  At fixed
`S=F_0`, the exact feasible set of `F_1` is the closed disk `|F_1|<=S/2`, including
`S=0`, and the exact defect identity is

```text
S^2-4|F_1|^2
 = (||X||^2-||Y||^2)^2
   +4(||X||^2||Y||^2-|<Y,X>|^2).
```

TPC-241 proves an unsigned norm floor for a standalone common-profile object but no
source theorem identifies it with `T beta`, `T w`, `F_0`, or one common additive term
inside all four physical V59 energies.  It therefore supplies zero direct quantitative
implication for the signed `F_1` channel.  Physical top-prime annihilation is not
claimed.

```text
TPC242_MAXIMUM_CLAIM = EXACT_C4_PHASE_FOURIER_SPECTRUM_SHARP_FIXED_ENERGY_CROSS_DISK_AND_TYPED_NO_TRANSFER
TPC242_ROUTE_ADVANCE = YES_OBSTRUCTION
TPC242_COMPLETE_PHASE_SPECTRUM = PROVED_F0_TOTAL_F1_ORIENTED_CROSS_F2_ZERO_F3_CONJUGATE_CROSS
TPC242_PHASE_BLIND_ADDITIVE_TERM = PROVED_TRIVIAL_CHARACTER_ONLY
TPC242_FIXED_F0_FEASIBLE_SET = PROVED_CLOSED_DISK_RADIUS_F0_OVER_TWO
TPC242_PHASE_DEFECT_IDENTITY = PROVED_IMBALANCE_SQUARED_PLUS_FOUR_GRAM_DETERMINANT
TPC242_TPC241_DIRECT_SIGNED_CREDIT = ZERO
TPC242_TPC241_TO_V59_IDENTIFICATION = OPEN
TPC242_PHYSICAL_TOP_PRIME_ANNIHILATION = NOT_CLAIMED
TPC242_LITERAL_C_H_SIGNED_CANCELLATION = NONE
TPC242_ARITHMETIC_ADVANCE = NO
TPC242_FIXED_ATOM_CREDIT = 0
TPC242_L2 = NONE
TPC242_FULL_GATE_B = OPEN
TPC242_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC242_STATUS = PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER
TPC242_ROUND2_CLUE = EXPRESS_THE_LITERAL_TOP_PRIME_CONTRIBUTION_PHASE_BY_PHASE_BEFORE_SQUARING_AND_COMPUTE_ITS_ACTUAL_K_EQUALS_ONE_COEFFICIENT
```

strongest positive result：complete `C_4` spectrum、sharp fixed-energy disk 与 exact
imbalance/Gram defect；strongest obstruction：even exact `F_0` leaves every
`F_1` in the disk possible；open theorem：source-backed phase-by-phase top-prime
attachment to the literal V59 remainder；reusable structure：phase-energy DFT plus
two-component defect ledger；`ROUND2_CLUE`：
`EXPRESS_THE_LITERAL_TOP_PRIME_CONTRIBUTION_PHASE_BY_PHASE_BEFORE_SQUARING_AND_COMPUTE_ITS_ACTUAL_K_EQUALS_ONE_COEFFICIENT`。

## 0.35 已发布：TPC-241 top-prime collision sharpness

项目：`papers/tpc-241-top-prime-collision-sharpness/`

类型：**PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_COLLISION_SHARPNESS**。

Fix independently of `x` a literal frozen common profile

```text
psi in C_c^infinity(R), 0<=psi<=1,
support(psi) subset [-1,1], integral psi=1.
```

For top primes `U/2<p<=U`, let `B_p(a)=sum_q B_(p,q)^psi(a)` and let
`S_p=sum_((a,p)=1)B_p(a)`.  The normalized profile first moment and weighted
prime first moment give, uniformly on the top shell,

```text
S_p=(3/2+o_psi(1))pQ^2/(H log Q).
```

Since there are `p-1` primitive residues, Cauchy after q-collapse yields

```text
sum_((a,p)=1)|B_p(a)|^2 >= S_p^2/(p-1).
```

With `C_p=-log(p)/p`, weighted PNT and
`Q^4/H^2=x^(1/48)`, this proves

```text
liminf_(x->infinity) [(log x)/x^(1/48)] E_top^psi
 >= 10773 log(2)/1600.
```

The TPC-238 lower frame must first be applied to the complete primitive-frequency
coefficient vector.  Only then is its nonnegative norm restricted to the top-prime
subenergy.  This legal order gives

```text
liminf_(x->infinity) [(log x)/x^(1/48)]
  [N^(-1)sum_(n in I_x)|K_psi(n)|^2]
 >= 10773 log(2)/3200.
```

For every fixed admissible `psi`, fixed `delta>0`, and real `A`, the latter
liminf refutes every eventual upper bound of the form
`O_(psi,delta,A)(x^(1/48-delta)(log x)^A)`.  Thus the TPC-239 unsigned
fixed-power exponent is sharp up to logarithms on the exact common-profile kernel.
No signed `C_h`, four-packet polarization, arithmetic `L2`, or Gate-B saving is
obtained.

```text
TPC241_MAXIMUM_CLAIM = FIXED_PROFILE_UNSIGNED_TOP_PRIME_Q_COLLAPSED_COLLISION_AND_FINITE_WINDOW_LIMINF
TPC241_ROUTE_ADVANCE = YES_OBSTRUCTION
TPC241_FROZEN_COMMON_PROFILE = REQUIRED_FIXED_NONNEGATIVE_NORMALIZED_C_INFINITY
TPC241_TOP_PRIME_ROW_MASS = PROVED_UNIFORM_THREE_OVER_TWO
TPC241_PRIMITIVE_RESIDUE_CAUCHY = PROVED_EXACT
TPC241_COEFFICIENT_LIMINF = PROVED_10773_LOG_2_OVER_1600
TPC241_FINITE_WINDOW_LIMINF = PROVED_10773_LOG_2_OVER_3200
TPC241_NORMALIZED_FIXED_POWER = PROVED_1_OVER_48_SHARP_UP_TO_LOGARITHMS
TPC241_UNSIGNED_FIXED_POWER_IMPROVEMENT = REFUTED_ON_EXACT_FIXED_PROFILE_COMMON_SOURCE_KERNEL
TPC241_FULL_VECTOR_FRAME_BEFORE_TOP_PRIME_RESTRICTION = REQUIRED_EXACT
TPC241_CLASS_UNIFORM_PROFILE_THRESHOLD = NOT_CLAIMED
TPC241_PLATEAU_PROFILE_SUBSTITUTION = FORBIDDEN
TPC241_C_H_SIGNED_CANCELLATION = NONE
TPC241_SIGNED_FOUR_PACKET_GATE_B_SCALAR = OPEN
TPC241_ARITHMETIC_ADVANCE = NO
TPC241_FIXED_ATOM_CREDIT = 0
TPC241_L2 = NONE
TPC241_FULL_GATE_B = OPEN
TPC241_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC241_STATUS = PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_COLLISION_SHARPNESS
TPC241_ROUND2_CLUE = FORCE_THE_NEXT_ARGUMENT_TO_RETAIN_FOUR_PACKET_POLARIZATION_OR_C_H_SIGNS_BEFORE_SQUARING_BECAUSE_THE_UNSIGNED_TOP_PRIME_COLLISION_CHANNEL_IS_FIXED_POWER_SHARP
```

strongest positive result：explicit source-locked coefficient and finite-window
`x^(1/48)/log x` liminfs；strongest obstruction：the exact unsigned common-profile
channel attains the full fixed-power `1/48` scale up to logarithms；open theorem：
whether literal four-packet polarization or signed `C_h` cancels the top-prime
collision mode before absolute squaring；reusable structure：normalized profile first
moment + primitive-residue Cauchy + weighted PNT + full-vector finite-window lower
frame；`ROUND2_CLUE`：
`FORCE_THE_NEXT_ARGUMENT_TO_RETAIN_FOUR_PACKET_POLARIZATION_OR_C_H_SIGNS_BEFORE_SQUARING_BECAUSE_THE_UNSIGNED_TOP_PRIME_COLLISION_CHANNEL_IS_FIXED_POWER_SHARP`。

## 0.34 已发布：TPC-240 top-prime direct-energy floor

项目：`papers/tpc-240-top-prime-direct-energy-floor/`

类型：**PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_DIRECT_ENERGY_FLOOR**。

Fix a literal frozen profile

```text
psi in C_c^infinity(R), 0<=psi<=1,
support(psi) subset [-1,1], integral psi=1,
kappa_psi=integral |psi|^2.
```

For prime denominators `U/2<p<=U`, TPC-215 gives
`C_p=-log(p)/p`.  Since `p<q`, `4Q<H`, and
`2floor(pq/H)<p`, the signed multipliers in one fixed q-row map injectively to
primitive residues.  Therefore

```text
sum_((a,p)=1)|B_(p,q)^psi(a)|^2
 = sum_(0<|m|<=floor(pq/H))|psi(Hm/(pq))|^2
 = kappa_psi pq/H+O_psi(1).
```

The row depth is uniformly large on the top shell because
`pq/H>=(1/2)x^(23/2400)`.  Aggregating with

```text
sum_(Q<q<=2Q)q=(3/2+o(1))Q^2/log Q,
sum_(U/2<p<=U)(log p)^2/p=(log 2+o(1))log U
```

and `log U/log Q=399/400` proves

```text
D_top^psi
 = [1197 kappa_psi log(2)/800+o_psi(1)]Q^2/H
 = x^(1/96+o_psi(1)),
1/2<=kappa_psi<=1.
```

The aggregate Riemann error is relatively
`O_psi(H/(UQ))=O_psi(x^(-23/2400))`.  The quantifier is for every fixed
admissible profile; no class-uniform threshold is claimed.  Hence this exact
q-split unsigned direct object is not `o(Q^2/H)`, and every fixed-power saving
on it is refuted.  The theorem does not estimate q-collapsed collision excess
and does not use the sign of `C_p` after squaring.

```text
TPC240_ROUTE_ADVANCE = YES_OBSTRUCTION
TPC240_TOP_PRIME_COEFFICIENT = PROVED_C_P_EQUALS_MINUS_LOG_P_OVER_P
TPC240_FIXED_Q_PRIMITIVE_ROW_NORM = PROVED_EXACT
TPC240_RIEMANN_ROW_ASYMPTOTIC = PROVED_UNIFORM_ON_TOP_PRIME_SHELL_FOR_EACH_FIXED_PROFILE
TPC240_KAPPA_RANGE = PROVED_ONE_HALF_LE_KAPPA_LE_ONE
TPC240_DIRECT_ENERGY_CONSTANT = PROVED_1197_KAPPA_LOG_2_OVER_800
TPC240_DIRECT_ENERGY_POWER = PROVED_X_1_OVER_96
TPC240_DIRECT_FIXED_POWER_SAVING = REFUTED_ON_EXACT_Q_SPLIT_UNSIGNED_OBJECT
TPC240_OPTIONAL_FINITE_WINDOW_FLOOR = PROVED_AT_ONE_HALF_TIMES_DIRECT_ENERGY
TPC240_X_1_OVER_48_SHARPNESS = NOT_CLAIMED
TPC240_CLASS_UNIFORM_PROFILE_THRESHOLD = NOT_CLAIMED
TPC240_PLATEAU_PROFILE_SUBSTITUTION = FORBIDDEN
TPC240_C_H_SIGNED_CANCELLATION = NONE
TPC240_ARITHMETIC_ADVANCE = NO
TPC240_FIXED_ATOM_CREDIT = 0
TPC240_L2 = NONE
TPC240_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC240_STATUS = PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_DIRECT_ENERGY_FLOOR
TPC240_ROUND2_CLUE = TEST_THE_TOP_PRIME_Q_COLLAPSED_COLLISION_EXCESS_OVER_THE_EXACT_DIRECT_FLOOR_BEFORE_CLAIMING_X_1_OVER_48_SHARPNESS
```

strongest positive result：exact top-prime q-split direct-energy asymptotic with
constant `1197 kappa_psi log(2)/800`；strongest obstruction：this exact unsigned direct
factor has no `o(Q^2/H)` or fixed-power saving；open theorem：top-prime q-collapsed
collision energy and its excess over the direct floor；reusable structure：top-prime
singleton coefficient + primitive fixed-q row + endpoint-safe Riemann sum + factorized
weighted PNT；`ROUND2_CLUE`：
`TEST_THE_TOP_PRIME_Q_COLLAPSED_COLLISION_EXCESS_OVER_THE_EXACT_DIRECT_FLOOR_BEFORE_CLAIMING_X_1_OVER_48_SHARPNESS`。

## 0.33 已发布：TPC-239 Brun--Titchmarsh primitive-bucket envelope

项目：`papers/tpc-239-brun-titchmarsh-primitive-bucket-envelope/`

类型：**PROVED_SOURCE_BACKED_PRIME_DENSITY_L1 / LOGARITHMIC_ONLY**。

For primitive `a mod h`, the physical congruence `m q^(-1)=a (mod h)` implies
`q=a^(-1)m (mod h)` in a reduced residue class.  With
`M_h=floor(2hQ/H)`, dropping only the `q`-dependent multiplier cutoff gives

```text
R_h(a)
 <= sum_(0<|m|<=M_h,(m,h)=1)
      [pi(2Q;h,a^(-1)m)-pi(Q;h,a^(-1)m)].
```

Brun--Titchmarsh and `2M_h<=4hQ/H` therefore prove

```text
R_h(a)
 <=16(Q^2/H)(h/phi(h))/log(2Q/h)
 <<x^(1/96)loglog x/log x.
```

Combining this with the unchanged TPC-237 direct coefficient energy and
reduced-frequency large sieve yields

```text
N^(-1) sum_(n in I_x) sum_j |K_j(n)|^2
 << J M^2 x^(1/48)(log x)^4 loglog x.
```

The gain over TPC-237 is the factor `log x/loglog x`; the fixed-power exponent
and leading unnormalized exponent `49/48+o(1)` do not improve.

```text
TPC239_ROUTE_ADVANCE = YES_LOGARITHMIC_ONLY
TPC239_PRIMITIVE_AP_REDUCTION = PROVED_EXACT_UPPER_COMPILER
TPC239_BRUN_TITCHMARSH_INPUT = SOURCE_BACKED
TPC239_BUCKET_MULTIPLICITY = PROVED_LE_16_Q_SQUARED_OVER_H_TIMES_H_OVER_PHI_H_OVER_LOG_2Q_OVER_H
TPC239_V59_BUCKET_MULTIPLICITY = PROVED_X_1_OVER_96_LOGLOG_X_OVER_LOG_X
TPC239_FINITE_WINDOW_PACKET_TRACE = PROVED_X_1_OVER_48_LOG_FOUR_LOGLOG
TPC239_IMPROVEMENT_OVER_TPC237 = PROVED_FACTOR_LOG_X_OVER_LOGLOG_X
TPC239_FIXED_POWER_IMPROVEMENT = NONE
TPC239_C_H_SIGNED_CANCELLATION = NONE
TPC239_ARITHMETIC_ADVANCE = NO
TPC239_FIXED_ATOM_CREDIT = 0
TPC239_L2 = NONE
TPC239_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC239_STATUS = PROVED_SOURCE_BACKED_PRIME_DENSITY_L1
TPC239_ROUND2_CLUE = TEST_THE_EXACT_TOP_BAND_C_H_BEFORE_SEEKING_FURTHER_UNIFORM_BUCKET_SAVINGS
```

strongest positive result：normalized
`x^(1/48)(log x)^4loglog x` finite-window packet trace；strongest obstruction：prime
density saves only a logarithm and leaves fixed-power `1/48`；open theorem：literal
weighted or signed within-bucket cancellation beyond coefficient-blind prime counting；
reusable structure：primitive residue to reduced prime-AP compiler；`ROUND2_CLUE`：
`TEST_THE_EXACT_TOP_BAND_C_H_BEFORE_SEEKING_FURTHER_UNIFORM_BUCKET_SAVINGS`。

## 0.32 已发布：TPC-238 finite-window lower-frame obstruction

项目：`papers/tpc-238-finite-window-lower-frame-obstruction/`

类型：**PROVED_STRUCTURAL_OBSTRUCTION_L1 / CROSS_REDUCED_FREQUENCY_CANCELLATION_EXCLUDED**。

For any consecutive interval `I` of `N` integers, put
`L=floor((N+1)/2)`.  For coefficients supported on distinct primitive fractions
`a/h` with `h<=U`, TPC-238 proves

```text
E_I(z) >= [L-pi^2 U^4/(12L)]_+ sum|z|^2,
E_I(z)/N >= [1/2-pi^2 U^4/(6N^2)]_+ sum|z|^2.
```

The proof uses a translated triangular minorant, the exact Fejér Gram matrix,
primitive Farey spacing `U^(-2)`, and a circular inverse-square packing row sum.
At V59,

```text
U^4/N^2=x^(-67/100+o(1)),
E_(I_x)(z)/N >= [1/2-O(x^(-67/100+o(1)))]sum|z|^2.
```

Thus, after the prime rows have been collapsed into one coefficient at every
primitive reduced frequency, interference among different frequencies cannot provide
a fixed-power saving relative to the collapsed coefficient energy.  The theorem does
not estimate that coefficient energy and leaves all same-frequency `q`-bucket
cancellation open.

```text
TPC238_TRIANGULAR_WINDOW_LOWER_FRAME = PROVED_EXACT
TPC238_PRIMITIVE_FAREY_SPACING = PROVED_U_TO_MINUS_2
TPC238_FEJER_OFFDIAGONAL = PROVED_LE_1_OVER_4L_DISTANCE_SQUARED
TPC238_CIRCULAR_PACKING_ROW_SUM = PROVED_LE_PI_SQUARED_U_FOUR_OVER_3
TPC238_LOWER_FRAME = PROVED_L_MINUS_PI_SQUARED_U_FOUR_OVER_12L_POSITIVE_PART
TPC238_NORMALIZED_LOWER_FRAME = PROVED_HALF_MINUS_PI_SQUARED_U_FOUR_OVER_6N_SQUARED_POSITIVE_PART
TPC238_V59_FRAME_DEFECT = PROVED_X_MINUS_67_OVER_100
TPC238_CROSS_REDUCED_FREQUENCY_FIXED_POWER_SAVING = REFUTED_SCOPED_AFTER_Q_COLLAPSE
TPC238_WITHIN_Q_BUCKET_CANCELLATION = OPEN
TPC238_C_H_SIGNED_CANCELLATION = NONE
TPC238_ARITHMETIC_ADVANCE = NO
TPC238_FIXED_ATOM_CREDIT = 0
TPC238_L2 = NONE
TPC238_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC238_STATUS = PROVED_STRUCTURAL_OBSTRUCTION_L1
TPC238_ROUND2_CLUE = MOVE_THE_POWER_SAVING_SEARCH_INSIDE_THE_LITERAL_C_H_WEIGHTED_Q_COLLISION_BUCKETS
```

strongest positive result：V59 lower frame `1/2-O(x^(-67/100))`；strongest
obstruction：cross-reduced-frequency signs cannot supply fixed-power saving after
`q`-collapse；open theorem：literal `C_h`-weighted same-frequency collision energy；
reusable structure：triangular-window Fejér minorant plus circular inverse-square
packing；`ROUND2_CLUE`：
`MOVE_THE_POWER_SAVING_SEARCH_INSIDE_THE_LITERAL_C_H_WEIGHTED_Q_COLLISION_BUCKETS`。

## 0.31 已发布：TPC-237 collision-compressed finite-window reassembly

项目：`papers/tpc-237-collision-compressed-finite-window-reassembly/`

类型：**PROVED_STRUCTURAL_L1 / COMMON_SOURCE_PACKET_TRACE_AT_X_1_OVER_48**。

On the exact TPC-218 common-source kernel, TPC-237 first collapses the prime shell
inside each primitive `(h,a)` frequency bucket.  TPC-236 gives

```text
R_h(a)<=4Q^2/H+4hQ/H<=4Q^2/H+4UQ/H.
```

TPC-217 reduced-frequency large sieve then yields

```text
N^(-1) sum_(n in I_x) sum_j |K_j(n)|^2
 << J M^2 [x^(1/48)+x^(1/50)](log x)^5.
```

The leading unnormalized exponent is `49/48`.  The index passed to the large sieve is
always primitive `(a,h)=1`; unreduced frequencies are not legal.  Literal `C_h` is
retained but then appears through `|C_h|^2`, so no signed cancellation or sharpness is
claimed.

```text
TPC237_PRIMITIVE_FREQUENCY_INDEX = REQUIRED_EXACT
TPC237_Q_COLLISION_BEFORE_LARGE_SIEVE = PROVED_EXACT_COMPOSITION
TPC237_PRIMITIVE_BUCKET_FACTOR = PROVED_LE_4Q_SQUARED_OVER_H_PLUS_4UQ_OVER_H
TPC237_FINITE_WINDOW_PACKET_TRACE = PROVED_STRUCTURAL
TPC237_NORMALIZED_MAIN_EXPONENT = PROVED_1_OVER_48
TPC237_NORMALIZED_SECONDARY_EXPONENT = PROVED_1_OVER_50
TPC237_UNNORMALIZED_MAIN_EXPONENT = PROVED_49_OVER_48
TPC237_OLD_P_COLLAPSE = REPLACED_BY_PHYSICAL_COLLISION_FACTOR
TPC237_SIMULTANEOUS_SATURATION = NOT_CLAIMED
TPC237_C_H_SIGNED_CANCELLATION = NONE
TPC237_SIGNED_FOUR_PACKET_GATE_B_SCALAR = OPEN
TPC237_ARITHMETIC_ADVANCE = NO
TPC237_FIXED_ATOM_CREDIT = 0
TPC237_L2 = NONE
TPC237_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC237_STATUS = PROVED_STRUCTURAL_L1
TPC237_ROUND2_CLUE = TEST_THE_ACTUAL_WEIGHTED_COLLISION_ENERGY_BEFORE_SEEKING_CROSS_H_SIGN_CANCELLATION
```

strongest positive result：normalized `x^(1/48)+x^(1/50)` finite-window trace；
strongest obstruction：the proof is unsigned and gives no simultaneous saturation or
`C_h` cancellation；open theorem：actual weighted collision energy beyond the uniform
`R_*` product；reusable structure：primitive bucket collision compression before Farey
large sieve；`ROUND2_CLUE`：
`TEST_THE_ACTUAL_WEIGHTED_COLLISION_ENERGY_BEFORE_SEEKING_CROSS_H_SIGN_CANCELLATION`。

## 0.30 已发布：TPC-236 physical multi-wrap collision envelope

项目：`papers/tpc-236-physical-multiwrap-collision-envelope/`

类型：**PROVED_STRUCTURAL_L1 / SOURCE_VALID_PHYSICAL_FIBER_BESSEL_ENVELOPE**。

For a physical residue `a mod h`, put `g=gcd(a,h)` and
`M_h=floor(2hQ/H)`.  Exact gcd-fiber counting proves

```text
R_h(a) <= 2 floor(M_h/g) ceil(Qg/h)
         <= 4Q^2/H+4hQ/(gH)
         <= 8Q^2/H.
```

Pointwise Cauchy yields an unnormalized fixed-`h` Bessel theorem and an explicit-`C_h`
orthogonal pre-reassembly direct sum.  At V59 the sharper source-uniform toll is
`4x^(1/96)+4x^(23/2400)=(4+o(1))x^(1/96)`.

The exact floor fixture `(Q,H,U,h)=(101,8830,99,80)` satisfies the V59-shaped integer
power relations.  Rows `q=113,127,193` all have support `{17,63}`, so bucket
multiplicity and equal-row Bessel ratio are both three.  Physical transfer of TPC-234
multiplicity two is therefore `REFUTED_SCOPED`.  A second fixture proves that the
reduced modulus `h/g`, rather than `h`, is required.

```text
TPC236_PHYSICAL_ROW_INTERNAL_INJECTIVITY = PROVED_FOR_H_GT_4Q
TPC236_BUCKET_GCD_FIBER_BOUND = PROVED_EXACT
TPC236_BUCKET_MULTIPLICITY = PROVED_LE_8Q_SQUARED_OVER_H
TPC236_WEIGHTED_FIXED_H_BESSEL = PROVED_EXACT_WITHOUT_ROW_NORMALIZATION
TPC236_WEIGHTED_PHYSICAL_H_DIRECT_SUM = PROVED_EXACT
TPC236_COMMON_LINEAR_PACKET_TRANSFORM = PRESERVED_WITH_OPERATOR_NORM
TPC236_DIVISOR_WEIGHT_C_H = PRESERVED_EXPLICITLY
TPC236_V59_MULTIPLICITY_TOLL = PROVED_4X_1_OVER_96_PLUS_4X_23_OVER_2400
TPC236_Q101_TRIPLE_COLLISION = PROVED_EXACT
TPC236_Q101_EQUAL_ROW_RATIO = PROVED_EXACT_3
TPC236_PHYSICAL_MULTIPLICITY_TWO_TRANSFER = REFUTED_SCOPED
TPC236_GCD_FIBER_REDUCTION = REQUIRED
TPC236_CROSS_H_RATIONAL_FREQUENCY_REASSEMBLY = OPEN
TPC236_C_H_WEIGHTED_CANCELLATION = OPEN
TPC236_ARITHMETIC_ADVANCE = NO
TPC236_FIXED_ATOM_CREDIT = 0
TPC236_L2 = NONE
TPC236_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC236_STATUS = PROVED_STRUCTURAL_L1
TPC236_ROUND2_CLUE = COMBINE_PHYSICAL_H_FIBER_ENVELOPE_WITH_REDUCED_FREQUENCY_LARGE_SIEVE_AND_TEST_C_H_WEIGHTED_CANCELLATION
```

strongest positive result：source-valid unnormalized physical-fiber Bessel envelope；
strongest obstruction：exact triple collision refutes multiplicity two and the
surviving loss has exponent `1/96`；open theorem：cross-`h` reduced-frequency
reassembly with signed `C_h` cancellation；reusable structure：gcd-fiber reduction and
coordinate Bessel compiler；`ROUND2_CLUE`：
`COMBINE_PHYSICAL_H_FIBER_ENVELOPE_WITH_REDUCED_FREQUENCY_LARGE_SIEVE_AND_TEST_C_H_WEIGHTED_CANCELLATION`。
Six finite scales, independent checker, adversarial gcd fixture, and 5-page
embedded-font PDF。

## 0.29 已发布：TPC-235 V59 physical-depth crosswalk

项目：`papers/tpc-235-v59-physical-depth-crosswalk/`

类型：**PROVED_STRUCTURAL_L1 / SINGLE_CLOCK_AND_OUTPUT_NORMALIZATION_REFUTED_SCOPED**。

For every physical denominator `h`, define `lambda_h=hQ/H`.  Then the V59 row is
exactly parameterized by

```text
cutoff=floor(lambda_h q/Q),
profile argument=mQ/(lambda_h q),
modulus=h=(H/Q)lambda_h.
```

The TPC-226 modeled clock matches both modulus and cutoff/profile if and only if
`h=4LQ` and `H=4Q^2`.  At V59, `4Q^2/H=4x^(1/96)`, so exact single-clock attachment
is refuted by a growing mismatch.  The active physical depths obey
`1/2<=lambda_h<=x^(23/2400)`; each unit depth has `x^(31/96+o(1))` available integer
denominator-grid points, without claiming that all corresponding `C_h` are nonzero.

The source four-phase identity requires one common linear transform.  Independently
unit-normalizing each output makes all four squared norms one and their signed sum
zero; the scalar fixture `(beta,w)=(1,2)` changes from `2` to `0`.  Thus TPC-234
output normalization is not automatically source-valid.

```text
TPC235_V59_PHYSICAL_DEPTH_VARIABLE = PROVED_EXACT_LAMBDA_H_EQ_HQ_OVER_H
TPC235_PHYSICAL_ROW_REPARAMETERIZATION = PROVED_EXACT
TPC235_SINGLE_CLOCK_COMPATIBILITY_IFF_H_EQ_4Q_SQUARED = PROVED_EXACT
TPC235_V59_CLOCK_RATIO = PROVED_EXACT_4X_TO_1_OVER_96
TPC235_TPC226_EXACT_SINGLE_CLOCK_ATTACHMENT = REFUTED_SCOPED
TPC235_PHYSICAL_DEPTH_RANGE = PROVED_EXACT_HALF_TO_X_23_OVER_2400
TPC235_PHYSICAL_DENOMINATOR_GRID_PER_DEPTH = PROVED_X_31_OVER_96
TPC235_DIVISOR_WEIGHT_C_H = SOURCE_LOCKED_REQUIRED
TPC235_FULL_H_SUM = SOURCE_LOCKED_REQUIRED
TPC235_COMMON_PACKET_TRANSFORM = SOURCE_LOCKED_REQUIRED
TPC235_OUTPUT_UNIT_NORMALIZATION_POLARIZATION = REFUTED_SCOPED
TPC235_SOURCE_VALID_NORMALIZATION = OPEN_WEIGHTED_LINEAR_ONLY
TPC235_ARITHMETIC_ADVANCE = NO
TPC235_FIXED_ATOM_CREDIT = 0
TPC235_L2 = NONE
TPC235_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC235_STATUS = PROVED_STRUCTURAL_L1
TPC235_ROUND2_CLUE = BUILD_PHYSICAL_H_FIBER_DIRECT_SUM_WITH_COMMON_PACKET_TRANSFORM_AND_EXPLICIT_WEIGHTS
```

strongest positive result：exact physical-depth row and compatibility iff theorem；
strongest obstruction：single-clock mismatch and packet-output normalization erase the
source polarization；open theorem：weighted physical `h`-fiber direct sum with common
packet transform；reusable structure：clock/cutoff/profile compatibility triangle and
packet normalization firewall；`ROUND2_CLUE`：
`BUILD_PHYSICAL_H_FIBER_DIRECT_SUM_WITH_COMMON_PACKET_TRANSFORM_AND_EXPLICIT_WEIGHTS`。
Three exact finite reproducers and bridge checker pass in normal and optimized modes；
4-page embedded-font PDF。

## 0.28 已发布：TPC-234 normalized collision-Bessel stability

项目：`papers/tpc-234-normalized-collision-bessel-stability/`

类型：**PROVED_STRUCTURAL_L1 / DEPTH_UNIFORM_NORMALIZED_BESSEL_BOUND**。

TPC-232 residue multiplicity two implies that arbitrary nonzero rows, after unit-norm
normalization, have synthesis Gram operator

```text
0<=G=T*T<=2I,
-I<=G-I<=I,
||G-I||<=1.
```

The constant is independent of depth, raw mass, and profile amplitudes, and is sharp
in the ambient multiplicity-two class.  A literal `Q=39,L=7` block has normalized
symmetric/antisymmetric ratios `4/3` and `2/3`, proving that normalization repairs
conditioning but does not imply strict saving.

```text
TPC234_BUCKET_MULTIPLICITY_TWO = INHERITED_PROVED_EXACT
TPC234_UNIT_ROW_NORMALIZATION = MODELING_TRANSFORM
TPC234_NORMALIZED_SYNTHESIS_BESSEL_BOUND = PROVED_EXACT_2
TPC234_NORMALIZED_GRAM_SPECTRUM = PROVED_EXACT_IN_0_2
TPC234_OFFDIAGONAL_GRAM_NORM = PROVED_EXACT_LE_1
TPC234_DEPTH_UNIFORM_CONDITIONING = PROVED_EXACT
TPC234_AMBIENT_CONSTANT_TWO = PROVED_EXACT_SHARP
TPC234_Q39_LITERAL_NORMALIZED_RATIOS = PROVED_EXACT_4_OVER_3_AND_2_OVER_3
TPC234_NORMALIZATION_AUTOMATIC_SAVING = REFUTED_SCOPED
TPC234_SOURCE_VALID_NORMALIZATION = OPEN
TPC234_ACTUAL_V59_CROSSWALK = OPEN
TPC234_ARITHMETIC_ADVANCE = NO
TPC234_FIXED_ATOM_CREDIT = 0
TPC234_L2 = NONE
TPC234_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC234_STATUS = PROVED_STRUCTURAL_L1
TPC234_ROUND2_CLUE = TRACE_ACTUAL_V59_ROW_WEIGHTS_AND_TEST_SOURCE_VALID_NORMALIZATION
```

strongest positive result：depth-uniform `0<=G<=2I`；strongest obstruction：literal
normalized rows still amplify by `4/3`；open theorem：actual V59 crosswalk and
source-valid normalization；reusable structure：multiplicity-to-Bessel compiler、exact
sum-of-squares residual；`ROUND2_CLUE`：
`TRACE_ACTUAL_V59_ROW_WEIGHTS_AND_TEST_SOURCE_VALID_NORMALIZATION`。5 scales、Q39 exact
block、independent checker；3-page embedded-font PDF。

## 0.27 已发布：TPC-233 critical-depth row-mass obstruction

项目：`papers/tpc-233-critical-depth-row-mass-obstruction/`

类型：**PROVED_ARITHMETIC_OBSTRUCTION_L1 / RAW_ROW_COMPARABILITY_REFUTED_SCOPED**。

Choose `Q_L=2^j product_(prime ell<=L)ell` with `log Q_L=L log L+O(1)`, so
`L~log Q_L/loglog Q_L`.  The classical PNT error term places low/high endpoint
prime rows with cutoffs `L` and `2L-1`.  Their exact uniform-atom support sizes are

```text
N_low=2,
N_high=2(1+pi(2L-1)-pi(L)),
kappa_raw >= (1+o(1))L/log L -> infinity.
```

Every admissible clock has the universal cap `kappa_raw<=2L-1`.  Therefore fixed raw
row-mass comparability is not a theorem of the modeled support.  Row normalization
remains a possible repair, but its collision conditioning and source validity are open.

```text
TPC233_CRITICAL_PRIMORIAL_CLOCK = PROVED_EXACT
TPC233_CRITICAL_SCALE_RELATION = PROVED_ASYMPTOTIC
TPC233_LOW_HIGH_PRIME_ROWS = PROVED_SOURCE_BACKED
TPC233_LOW_ROW_ATOMS = PROVED_EXACT_2
TPC233_HIGH_ROW_ATOMS = PROVED_EXACT_PRIME_INTERVAL_COUNT
TPC233_RAW_COMPARABILITY_DIVERGES = PROVED_ASYMPTOTIC
TPC233_UNIVERSAL_KAPPA_UPPER_BOUND = PROVED_EXACT_2L_MINUS_1
TPC233_FIXED_COMPARABILITY_FROM_GEOMETRY = REFUTED_SCOPED
TPC233_ROW_NORMALIZATION_REPAIR = OPEN
TPC233_ACTUAL_V59_ROW_WEIGHTS = OPEN
TPC233_ARITHMETIC_ADVANCE = NO
TPC233_FIXED_ATOM_CREDIT = 0
TPC233_L2 = NONE
TPC233_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC233_STATUS = PROVED_ARITHMETIC_OBSTRUCTION_L1
TPC233_ROUND2_CLUE = NORMALIZE_ROWS_THEN_TEST_COLLISION_OPERATOR_BEFORE_V59_ATTACHMENT
```

strongest positive result：exact critical primorial clock and low/high mass identities；
strongest obstruction：fixed raw comparability diverges；open theorem：source-valid row
normalization and normalized collision conditioning；reusable structure：primorial
saturation、shrinking endpoint windows、exact coprime-count compiler；`ROUND2_CLUE`：
`NORMALIZE_ROWS_THEN_TEST_COLLISION_OPERATOR_BEFORE_V59_ATTACHMENT`。4 exact clocks，
independent deterministic primality reconstructions；4-page embedded-font PDF。

## 0.26 已发布：TPC-232 subcritical growing resonance depth

项目：`papers/tpc-232-subcritical-growing-resonance-depth/`

类型：**PROVED_ARITHMETIC_OBSTRUCTION_L1 / SUBCRITICAL_GROWING_DEPTH_STOP_SCOPED**。

For the TPC-226 modeled clock `h=4LQ`, prime rows `Q<q<2Q`, and primitive
multipliers `|m|<=floor(Lq/Q)`, every collision in the range `L<Q/4` is an
opposite-sign one-wrap channel

```text
ar+bp=4LQ,  1<=a,b<2L,  gcd(a,b)=1.
```

Each coefficient pair has determinant `4LQ`; separating short grazing parameter
intervals from the Selberg branch gives a coefficient-uniform sieve estimate.  Since
`sum_(a,b<2L) 1/max(a,b)<4L`, uniformly for `L<=(log Q)^A`,

```text
C_L(Q) <<_A LQ loglog(3LQ)/(log Q)^2,
C_L(Q)/P(Q) <<_A L loglog(3LQ)/log Q.
```

Thus `L=o(log Q/loglog Q)` implies zero collision incidence density.  TPC-230's
unmatched-mass floor then rules out every fixed saving under fixed row-mass
comparability throughout this subcritical regime.  The result is an upper-bound
obstruction, not a critical-depth lower bound and not a V59 source attachment.

```text
TPC232_GROWING_COLLISION_NORMAL_FORM = PROVED_EXACT
TPC232_UNIFORM_POLYLOG_DEPTH_SIEVE = PROVED_SOURCE_BACKED
TPC232_COLLISION_INCIDENCE_BOUND = PROVED_ASYMPTOTIC
TPC232_SUBCRITICAL_DEPTH_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC232_SUBCRITICAL_FIXED_SAVING = STOP_SCOPED
TPC232_CRITICAL_DEPTH_SUFFICIENCY = OPEN
TPC232_DILATED_CLOCK = MODELING_CHOICE
TPC232_ACTUAL_V59_CLOCK_ATTACHMENT = OPEN
TPC232_ARITHMETIC_ADVANCE = NO
TPC232_ARITHMETIC_OBSTRUCTION = PROVED_SOURCE_BACKED
TPC232_FIXED_ATOM_CREDIT = 0
TPC232_L2 = NONE
TPC232_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC232_STATUS = PROVED_ARITHMETIC_OBSTRUCTION_L1
TPC232_ROUND2_CLUE = TEST_CRITICAL_DEPTH_CLOCK_MASS_AND_DEGREE_BEFORE_V59_ATTACHMENT
```

strongest positive result：uniform growing-channel sieve theorem；strongest
obstruction：all `o(log Q/loglog Q)` depths have zero incident-row density；open theorem：
critical-depth mass/degree and actual V59 attachment；reusable structure：one-wrap normal
form、coefficient-uniform interval sieve、weighted channel summation；`ROUND2_CLUE`：
`TEST_CRITICAL_DEPTH_CLOCK_MASS_AND_DEGREE_BEFORE_V59_ATTACHMENT`。19-scale independent
scan；4-page embedded-font PDF。

## 0.25 已发布：TPC-231 finite-resonance sieve obstruction

项目：`papers/tpc-231-finite-resonance-sieve-obstruction/`

类型：**PROVED_ARITHMETIC_OBSTRUCTION_L1 / FIXED_FINITE_RESONANCE_STOP_SCOPED**。

For `Q=3t+a`, the primitive `7p+3r=16Q` edge has exact two-form parameterization
`p=3k+a`, `r=16t+3a-7k` and determinant `16Q`. Its local bad-residue count is one at
`2,3,7` and primes dividing `Q`, and two otherwise. The classical dimension-two
Selberg upper-bound sieve therefore gives

```text
E_3716(Q) << S_3716(Q) Q/(log Q)^2,
S_3716(Q) << log log(3Q),
E_3716(Q)/P(Q) -> 0.
```

The determinant argument extends to every fixed finite primitive nondegenerate linear
resonance family. A bounded-degree Cauchy--Schwarz transfer then converts `o(P)` edges
into `o(D)` possible saving for bounded coefficients and comparable row masses. With
TPC-230, the literal first-resonance matched mass tends to zero, so any fixed positive
saving, including `1/400`, is impossible on this scoped branch.

```text
TPC231_3716_PARAMETERIZATION = PROVED_EXACT
TPC231_3716_LOCAL_ROOT_LAW = PROVED_EXACT
TPC231_3716_SELBERG_UPPER_BOUND = PROVED_SOURCE_BACKED
TPC231_3716_EDGE_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC231_FIXED_FINITE_RESONANCE_SUPPORT_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC231_FIRST_PRIMITIVE_3_7_FIXED_SAVING = STOP_SCOPED
TPC231_FIXED_FINITE_RESONANCE_COMPARABLE_ROW_ROUTE = STOP_SCOPED
TPC231_GROWING_RESONANCE_DEPTH = OPEN
TPC231_ACTUAL_V59_SOURCE_MASS_CROSSWALK = OPEN
TPC231_ARITHMETIC_ADVANCE = NO
TPC231_ARITHMETIC_OBSTRUCTION = PROVED_SOURCE_BACKED
TPC231_FIXED_ATOM_CREDIT = 0
TPC231_L2 = NONE
TPC231_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC231_ROUND2_CLUE = TEST_GROWING_RESONANCE_DEPTH_OR_RETURN_TO_THE_ACTUAL_V59_SOURCE_MASS_CROSSWALK
```

strongest positive result：uniform two-form sieve theorem and fixed-finite-family
extension；strongest obstruction：fixed finite comparable-row resonance supports have
zero capacity for fixed global saving；open theorem：growing resonance depth or the
actual V59 source-mass crosswalk；reusable structure：determinant/local-density/singular-
series/support/energy compiler。32,761-scale independent scan；4-page embedded-font PDF。

## 0.24 已发布：TPC-230 matched-resonance mass ceiling

项目：`papers/tpc-230-matched-resonance-mass-ceiling/`

类型：**PROVED_STRUCTURAL_L1 / MATCHED_RESONANCE_MASS_CEILING**。

For total diagonal mass `D` and matched mass `M`, matching decomposition gives the
sharp ceiling `E_AP>=D-M`. Thus `delta` saving requires `M/D>=delta`. If row masses have
ratio `kappa`, then `M/D<=2*kappa*E/P`. Literal aligned rows satisfy `kappa<=4`, yielding
the necessary strict-endpoint density toll `E/P>=1/3200`.

```text
TPC230_MATCHED_MASS_SAVING_CEILING = PROVED_EXACT_SHARP
TPC230_NECESSARY_MASS_FRACTION = PROVED_EXACT
TPC230_COMPARABLE_ROW_DENSITY_TOLL = PROVED_EXACT
TPC230_LITERAL_ALIGNED_KAPPA_LE_4 = PROVED_EXACT
TPC230_STRICT_1_OVER_400_EDGE_DENSITY_TOLL = 1/3200
TPC230_ASYMPTOTIC_RESONANCE_EDGE_DENSITY = OPEN
TPC230_ARITHMETIC_ADVANCE = NO
TPC230_FIXED_ATOM_CREDIT = 0
TPC230_L2 = NONE
TPC230_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC230_ROUND2_CLUE = APPLY_A_TWO_LINEAR_FORM_UPPER_BOUND_SIEVE_TO_THE_3_7_RESONANCE_COUNT
```

strongest positive result：sharp matched-mass capacity theorem；strongest obstruction：
unmatched rows cannot be improved even with perfect edge signs；open theorem：asymptotic
edge density and actual source concentration；reusable structure：mass ceiling and
comparability-to-density compiler。Q25 literal fraction `5/13`; 4089-scale replay；PDF 3 pages。

## 0.23 已发布：TPC-229 primitive resonance matching spectrum

项目：`papers/tpc-229-primitive-resonance-matching-spectrum/`

类型：**PROVED_STRUCTURAL_L1 / PRIMITIVE_RESONANCE_MATCHING_SPECTRUM**。

Every edge satisfies `10Q/7<p<8Q/5<r<2Q`; endpoint separation and uniqueness prove
the graph is a matching for all `Q>=8`. Every two-coordinate block has spectrum
`(-1,-1,+1,+1)`, with exact symmetric/antisymmetric decomposition and sharp AP ratio
range `[0,2]`. A `delta` saving is equivalent to
`(1+delta)E_sym<=(1-delta)E_anti`.

```text
TPC229_RESONANCE_GRAPH_MATCHING = PROVED_EXACT
TPC229_EDGE_SPECTRUM = PROVED_EXACT
TPC229_GLOBAL_BLOCK_DIRECT_SUM = PROVED_EXACT
TPC229_DELTA_SAVING_CRITERION = PROVED_EXACT
TPC229_SOURCE_BILINEAR_BLOCK_BOUND = PROVED_EXACT_SHARP
TPC229_ARITHMETIC_ANTISYMMETRIC_DOMINANCE = OPEN
TPC229_ARITHMETIC_ADVANCE = NO
TPC229_FIXED_ATOM_CREDIT = 0
TPC229_L2 = NONE
TPC229_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC229_ROUND2_CLUE = QUANTIFY_MATCHED_RESONANCE_MASS_BEFORE_SEEKING_A_FIXED_PROPORTIONAL_SAVING
```

strongest positive result：graph exact collapses to independent edge blocks；strongest
obstruction：matched mass 与 antisymmetric source dominance 都不是 geometry consequence；
open theorem：quantify matched resonance mass；reusable structure：endpoint separation、
matching、sym/anti ledger。4089-scale replay covers 13,754 edges；PDF 3 pages。

## 0.22 已发布：TPC-228 source-native polarized collision compiler

项目：`papers/tpc-228-source-native-polarized-collision-compiler/`

类型：**PROVED_STRUCTURAL_L1 / SOURCE_NATIVE_POLARIZED_COLLISION_COMPILER**。

TPC-228 保持 TPC-227 source/profile axis separation，对 common-profile rows
`W_q^(j)=U_q+i^jV_q` 证明 exact identity

```text
1/4 sum_j i^j(E_AP^(j)-E_diag^(j)) = sum_(q!=r)<U_q,V_r>.
```

Q25 first `3--7` resonance 精确成为两个 shared residues 上的四项 beta-w source block。
五个 exact-rational fixtures 给出 `1/40000,-1/40000,0,1/80000,1/160000`，另有
three-row 与 no-collision controls。

```text
TPC228_COMMON_PROFILE_PACKET_RULE = PROVED_EXACT
TPC228_POLARIZED_AP_MINUS_DIAGONAL_COMPILER = PROVED_EXACT
TPC228_SOURCE_LABELLED_COLLISION_SUM = PROVED_EXACT
TPC228_Q25_3_7_SOURCE_BLOCK = PROVED_EXACT_FINITE
TPC228_ACTUAL_V59_TO_PRIMITIVE_ATOM_CROSSWALK = OPEN
TPC228_ARITHMETIC_SIGN_THEOREM = OPEN
TPC228_ARITHMETIC_ADVANCE = NO
TPC228_FIXED_ATOM_CREDIT = 0
TPC228_L2 = NONE
TPC228_FULL_GATE_B = OPEN
TPC228_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC228_ROUND2_CLUE = ANALYZE_THE_SOURCE_NATIVE_3_7_COLLISION_GRAPH_AS_EXACT_TWO_BY_TWO_BLOCKS
```

strongest positive result：正确 typing 下的 exact source collision compiler；strongest
obstruction：同一 geometry 的 source block 可正、负或零；open theorem：actual V59
atom crosswalk 与 arithmetic sign bound；reusable structure：ordered collision bilinear
form、diagonal-first deletion。证据含 5+2 exact controls、8 mutations、独立 checker 与
3 页嵌入字体 PDF。

## 0.21 已发布：TPC-227 packet/profile axis separation

项目：`papers/tpc-227-packet-profile-axis-separation/`

类型：**PROVED_STRUCTURAL_L1 / PACKET_PROFILE_AXIS_SEPARATION**。

TPC-227 对 TPC-226 的 signed-profile clue 做 literal source audit。V59 的四相位属于
source sequences `a^(j)=beta+i^j w`，Poisson profile `psi_+` 对四包共同。若 `T` 是
physical transform、`T_j` 是 packet-dependent replacements，则 exact theorem 给出

```text
1/4 sum_j i^j ||T_j(x+i^j y)||^2 = <Tx,Ty> for all x,y
iff T_j^*T_j=T^*T for all j.
```

证明使用四点 operator DFT。TPC-226 的 Q25 collision block 上，aligned map
`(1,1)/400` 与 row-odd map `(1,-1)/400` 的 off-diagonal Gram difference exact 是
`-1/80000`。所以 global packet phase 虽 Gram-invisible，row-dependent profile sign
却改变 cross-row Gram；把 finite balanced profile 自动解释成 V59 source phase 的推理
被 scoped-refute。

```text
TPC227_ROUTE_ADVANCE = YES
TPC227_V59_PACKET_AXIS = SOURCE_LOCKED
TPC227_V59_PROFILE_AXIS = SOURCE_LOCKED_COMMON
TPC227_FOUR_GRAM_CRITERION = PROVED_EXACT
TPC227_GLOBAL_PACKET_PHASE_VISIBILITY = GRAM_INVISIBLE
TPC227_Q25_ROW_SIGN_GRAM_MISMATCH = PROVED_EXACT
TPC227_TPC226_AUTOMATIC_SOURCE_TRANSFER = REFUTED_SCOPED
TPC227_SOURCE_NATIVE_COMMON_PROFILE_COMPILER = OPEN
TPC227_ARITHMETIC_CANCELLATION = NONE
TPC227_ARITHMETIC_ADVANCE = NO
TPC227_FIXED_ATOM_CREDIT = 0
TPC227_L2 = NONE
TPC227_FULL_GATE_B = OPEN
TPC227_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC227_STATUS = PROVED_STRUCTURAL_L1
TPC227_ROUND2_CLUE = KEEP_THE_V59_PACKET_PHASE_ON_THE_SOURCE_SEQUENCE_AND_THE_POISSON_PROFILE_COMMON
```

strongest positive result：四包 source compatibility 被压成 exact iff Gram criterion，
并由 Q25 rational block 执行验证；strongest obstruction：row-dependent profile sign
不是 packet phase，自动 source transfer 不合法；open theorem：构造 common-profile
source-native collision compiler并估计 literal `3--7` correlation；reusable structure：
four-point Gram DFT、target-Gram test、collision block；`ROUND2_CLUE`：

```text
KEEP_THE_V59_PACKET_PHASE_ON_THE_SOURCE_SEQUENCE_AND_THE_POISSON_PROFILE_COMMON
```

证据包包含 6 个 exact-rational operator fixtures、独立 normal/optimized checker、6 个
mutation adversaries 与 4 页嵌入字体 PDF。Bridge proof/checker 为
`research/tpc-big-road/bridge_b_packet_profile_axis_separation.md` 与
`research/tpc-big-road/tpc_bridge_b_packet_profile_axis_separation_checker.py`。

## 0.20 已发布：TPC-226 first primitive-collision transition

项目：`papers/tpc-226-first-primitive-collision-transition/`

类型：**PROVED_STRUCTURAL_L1 / FIRST_PRIMITIVE_COLLISION_TRANSITION**。

TPC-226 沿 TPC-225 的最小下一步，把 finite clock dilation 到

```text
x=Q^3, H=4Q^2, h_L=4LQ, L in {1,2,3,4}, Q>=8,
```

并严格保留 literal primitive condition `gcd(m,h_L)=1`。collision congruence 与
cutoff/parity sieve 证明：`L=1,2,3` 的 distinct prime rows 仍 pairwise disjoint；
`L=4` 首次出现 legitimate overlap，且所有 collision 都是（差 exchange 与 global sign）

```text
7p+3r=16Q, m_p=3, m_r=-7.
```

`Q=25`, `(p,r)=(37,47)` 是第一个 exact census witness，共享 residues 为
`119,281 mod 400`。同一 resonance geometry 的 signed correction 对 aligned 与 inherited
affine profiles 为正，对 balanced odd-sign profiles 为负；后者还 exact 给出
`E_pol=E_all=0`。所以 legitimate overlap 是 cancellation interface，而非 cancellation
theorem。

```text
TPC226_ROUTE_ADVANCE = YES
TPC226_DILATED_CLOCK_FAMILY = MODELING_CHOICE
TPC226_PRIMITIVE_SOURCE_ROW = PROVED_EXACT
TPC226_L_LE_3_DISJOINTNESS = PROVED_EXACT
TPC226_FIRST_PRIMITIVE_COLLISION_DILATION = 4
TPC226_L4_RESONANCE_CLASSIFICATION = PROVED_EXACT
TPC226_Q25_RESONANCE = PROVED_EXACT
TPC226_ALIGNED_AP_SAVING = REFUTED_SCOPED
TPC226_AFFINE_AP_SAVING = REFUTED_SCOPED
TPC226_BALANCED_SIGN_AP_SAVING = PROVED_EXACT_FINITE_PROFILE
TPC226_BALANCED_SIGN_POLARIZED_CANCELLATION = PROVED_EXACT_FINITE_PROFILE
TPC226_UNIFORM_PROFILE_INDEPENDENT_SAVING = REFUTED_SCOPED
TPC226_V46_PROFILE_TRANSFER = OPEN
TPC226_ARITHMETIC_CANCELLATION = NONE
TPC226_ARITHMETIC_ADVANCE = NO
TPC226_FIXED_ATOM_CREDIT = 0
TPC226_L2 = NONE
TPC226_FULL_GATE_B = OPEN
TPC226_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC226_STATUS = PROVED_STRUCTURAL_L1
TPC226_ROUND2_CLUE = SOURCE_LOCK_THE_SIGN_OF_THE_3_7_RESONANCE_BEFORE_ANY_UNIFORM_AP_SAVING
```

strongest positive result：first legitimate primitive overlap 与完整 `3--7` resonance
classification 已 theorem-level closed，balanced signed profile 在非空 resonance graph 上
严格节省 AP energy；strongest obstruction：相同 geometry 对 aligned/affine profiles
严格放大，uniform profile-independent saving 被 scoped-refute；open theorem：source-lock
真实 V46 profiles 并证明 `3--7` signed correlation 的 arithmetic saving；reusable
structure：primitive multiplier sieve、collision graph 与 exact signed cross-term formula；
`ROUND2_CLUE`：

```text
SOURCE_LOCK_THE_SIGN_OF_THE_3_7_RESONANCE_BEFORE_ANY_UNIFORM_AP_SAVING
```

证据包包括 `Q=8..512` 的 505-scale complete classification、182 个 L4
collision-bearing scales、235 个 resonances、30 个 exact-rational profile records、
normal/optimized byte-identical independent checker、primitive-source adversary 与 5 页
嵌入字体 PDF。Bridge proof/checker 为
`research/tpc-big-road/bridge_b_first_primitive_collision_transition.md` 与
`research/tpc-big-road/tpc_bridge_b_first_primitive_collision_transition_checker.py`。

## 0.19 已发布：TPC-225 cutoff-one shared-clock obstruction

项目：`papers/tpc-225-cutoff-one-shared-clock-obstruction/`

类型：**PROVED_STRUCTURAL_L1 / CUTOFF_ONE_SHARED_CLOCK_OBSTRUCTION**。

TPC-225 直接审计 TPC-224 命名的 source-surrogate clock：

```text
x=Q^3, H=4Q^2, h=4Q, Q<q<=2Q prime
floor(hq/H)=floor(q/Q)=1.
```

每个 literal row 只包含 `m=+1,-1`，支持为
`{q^(-1),-q^(-1)} mod 4Q`。若 distinct prime supports 相交，则
`q_2=+/-q_1 mod 4Q`；shell interval 分别把两种情形压成 prime equality 或
`q_1+q_2=4Q`，后者又强迫两者都是非素数 `2Q`。因此 prime blocks
pairwise orthogonal，并精确得到

```text
E_AP  = E_diag
E_all = E_pol.
```

只要 `E_diag>0`，任何 `delta>0` 的
`E_AP<=(1-delta)E_diag` 都在该 named clock 上失败。该 obstruction
严格 scoped：本篇没有证明所有 V46 clocks 都是 cutoff one，也没有把 finite modulus
`h=4Q` 等同于 physical fixed atom。

```text
TPC225_ROUTE_ADVANCE = YES
TPC225_CUTOFF_ONE = PROVED_EXACT
TPC225_SUPPORT_DISJOINTNESS = PROVED_EXACT
TPC225_AP_EQUALS_DIAGONAL = PROVED_EXACT
TPC225_ALL_EQUALS_POLARIZED = PROVED_EXACT
TPC225_AP_SAVING_ON_NAMED_CLOCK = REFUTED_SCOPED
TPC225_POLARIZED_SAVING = PROFILE_DEPENDENT_OPEN
TPC225_V46_CLOCK_TRANSFER = OPEN
TPC225_ARITHMETIC_CANCELLATION = NONE
TPC225_ARITHMETIC_ADVANCE = NO
TPC225_FIXED_ATOM_CREDIT = 0
TPC225_L2 = NONE
TPC225_FULL_GATE_B = OPEN
TPC225_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC225_STATUS = PROVED_STRUCTURAL_L1
TPC225_ROUND2_CLUE = MOVE_TO_NONTRIVIAL_CUTOFF_CLOCK_BEFORE_CLAIMING_AP_DISPERSION
```

strongest positive result：named cutoff-one clock 诱导 exact prime-block orthogonal
decomposition，且 `E_AP=E_diag`、`E_all=E_pol` 对任意 finite
profile values 成立；strongest obstruction：strict AP marginal saving 在该 clock 上
被 theorem-level scoped-refute；open theorem：找到 source-locked nontrivial-cutoff
clock 并证明其 legitimate cross-prime overlap 的 dispersion，或证明相应 obstruction；
reusable structure：cutoff-one support lemma 与 block decomposition；
`ROUND2_CLUE`：

```text
MOVE_TO_NONTRIVIAL_CUTOFF_CLOCK_BEFORE_CLAIMING_AP_DISPERSION
```

证据包包含 9 个 exact-rational affine scales、7 个 aligned 与 7 个 balanced profile
records、完整 `Q=3..99` boundary geometry replay、normal/optimized
byte-identical independent checker 与 5 页嵌入字体 PDF。Bridge proof/checker 为
`research/tpc-big-road/bridge_b_cutoff_one_shared_clock_obstruction.md` 与
`research/tpc-big-road/tpc_bridge_b_cutoff_one_shared_clock_obstruction_checker.py`。

## 0.18 已发布：TPC-224 literal two-channel compatibility audit

项目：`papers/tpc-224-literal-two-channel-compatibility-audit/`

类型：**PROVED_STRUCTURAL_L1 / LITERAL_TWO_CHANNEL_COMPATIBILITY**。

TPC-223 的共同 literal interface 在本篇中被具体化为同一组 finite Hilbert vectors
`W_(q,j)`。定义

```text
E_AP  = sum_j ||sum_q W_(q,j)||^2
E_pol = sum_q ||sum_j W_(q,j)||^2
E_all = ||sum_(q,j) W_(q,j)||^2.
```

逐方向 Cauchy 与 exact scalar minimization 给出

```text
E_all <= min(J E_AP, P E_pol)
      <= PJ/(P+J) (E_AP+E_pol).
```

系数 `PJ/(P+J)` sharp，所有 `W_(q,j)=u` 时达到等号。对 literal TPC-220 row
rule、共同 `C_h=1/h` normalization 与 actual prime labels，本篇另外冻结两个不作
渐近拼接的 finite clocks：九个 source-surrogate scales 与五个
`H=5Q, h=5, q=1 (mod 5)` collision-stress scales。后者五个尺度均 exact-refute
unit-factor shortcut，说明 cross-label alignment 不能被记号层面的“两个 channel”自动
删除。

```text
TPC224_ROUTE_ADVANCE = YES
TPC224_COMMON_LITERAL_HILBERT_INTERFACE = PROVED_EXACT
TPC224_SHARP_ADDITIVE_CONSTANT = PROVED_EXACT
TPC224_UNIT_INTERFACE = REFUTED_SCOPED
TPC224_SOURCE_CLOCK_AUDIT = NUMERICALLY_CERTIFIED_EXACT_RATIONAL
TPC224_AP_DISPERSION = OPEN
TPC224_POLARIZED_CROSS_CORRELATION = OPEN
TPC224_LITERAL_V46_TRANSFER = OPEN
TPC224_ARITHMETIC_CANCELLATION = NONE
TPC224_ARITHMETIC_ADVANCE = NO
TPC224_FIXED_ATOM_CREDIT = 0
TPC224_L2 = NONE
TPC224_FULL_GATE_B = OPEN
TPC224_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC224_STATUS = PROVED_STRUCTURAL_L1
TPC224_ROUND2_CLUE = PROVE_SHARED_CLOCK_AP_AND_POLARIZED_MARGINAL_SAVINGS
```

strongest positive result：两个 channel 确实可以从同一个 literal vector family 得到，且
兼容性只引入 sharp `O(1)` additive factor；strongest obstruction：unit-factor interface
被 congruence-aligned actual-prime stress family scoped-refute；open theorem：在同一
V46 clock 上把 AP 与 polarized marginals 的 arithmetic savings 接到这组 vectors；
reusable structure：`E_all <= min(J E_AP,P E_pol) <= PJ/(P+J)(E_AP+E_pol)`；
`ROUND2_CLUE`：

```text
PROVE_SHARED_CLOCK_AP_AND_POLARIZED_MARGINAL_SAVINGS
```

Bridge proof/checker：`research/tpc-big-road/bridge_b_literal_two_channel_compatibility_audit.md`
与 `research/tpc-big-road/tpc_bridge_b_literal_two_channel_compatibility_audit_checker.py`。
本篇没有 arithmetic `L2`、fixed-atom credit、strict `1/400` 或 twin-prime conclusion。

## 0.17 已发布：TPC-223 conditional signed-reassembly compiler

项目：`papers/tpc-223-conditional-signed-reassembly-compiler/`

类型：**CONDITIONAL_THEOREM / TWO_CHANNEL_SIGNED_REASSEMBLY_COMPILER**。

TPC-223 将 TPC-220 的 literal prime-AP/collision channel 与 TPC-222 的 phase-labelled
four-packet channel 接入同一个 conditional interface：

```text
A_x << x^(E0-delta_AP+o(1))
P_x << x^(E0-kappa_pol+o(1))
S_x << x^lambda_struct (A_x+P_x)
```

在此接口下，exact exponent compiler 给出

```text
sigma = min(delta_AP,kappa_pol)-lambda_struct.
```

所以 strict endpoint margin 的充分且精确的 ledger 条件是
`sigma>1/400`。canonical `E0=5/3` fixture 取
`delta_AP=1/100`, `kappa_pol=1/80`, `lambda_struct=1/1200`，得到 effective saving
`11/1200`、strict margin `1/150`、compiled exponent `663/400`，目标 exponent 为
`1997/1200`。certificate 同时包含 exact borderline、failed、zero-channel 与
loss-dominated cases，并把 equality 明确标为 `BORDERLINE`。

```text
TPC223_ROUTE_ADVANCE = YES
TPC223_TWO_CHANNEL_COMPILER = PROVED_CONDITIONAL_ALGEBRA
TPC223_AP_DISPERSION = OPEN_CONDITIONAL_INPUT
TPC223_POLARIZED_CROSS_CORRELATION = OPEN_CONDITIONAL_INPUT
TPC223_LITERAL_REASSEMBLY_INTERFACE = OPEN_CONDITIONAL_INPUT
TPC223_EFFECTIVE_SAVING = CERTIFIED_EXACT_MIN_MINUS_LOSS
TPC223_STRICT_1_OVER_400 = CONDITIONAL_ONLY
TPC223_ARITHMETIC_CANCELLATION = NONE
TPC223_ARITHMETIC_ADVANCE = NO
TPC223_FIXED_ATOM_CREDIT = 0
TPC223_L2 = NONE
TPC223_FULL_GATE_B = OPEN
TPC223_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

strongest positive result：两个独立 channel 的 saving 以 exact minimum 合并，并显式
扣除 structural loss；strongest obstruction：任一 channel 为零、loss 主导或刚好
落在 `1/400` 都不能 strict pass；open theorem：在同一个 literal prime shell、clock
与 normalization 上证明三条 conditional inputs；reusable structure：two-channel
minimum-minus-loss exponent compiler；`ROUND2_CLUE`：

```text
PROVE_OR_REFUTE_THE_COMMON_LITERAL_TWO_CHANNEL_INTERFACE
```

Bridge proof/checker：`research/tpc-big-road/bridge_b_conditional_signed_reassembly_compiler.md`
与 `research/tpc-big-road/tpc_bridge_b_conditional_signed_reassembly_compiler_checker.py`。
这是 conditional theorem，不产生 arithmetic `L2`、fixed-atom credit、strict Gate-B
或 twin-prime conclusion。

## 0.16 已发布：TPC-222 four-packet polarization and the PSD cross-term obstruction

项目：`papers/tpc-222-four-packet-cross-term-obstruction/`

类型：**PROVED_STRUCTURAL_L1 / FOUR_PACKET_CROSS_TERM_OBSTRUCTION**。

TPC-222 将 TPC-218--221 反复出现的 four-packet signed interface 单独封装。令
`G_(j,l)=<V_j,V_l>`，`V(c)=sum_j c_j V_j`，则

```text
||V(c)||^2 = c^* G c,
<x,y> = 1/4 sum_(r=0)^3 i^(-r) ||x+i^r y||^2,
0 <= c^* G c <= tr(G)||c||_2^2.
```

四点极化是 exact cross-term compiler；trace envelope 是 sharp 的 unsigned majorant。
更关键的是，`V_j^+=u` 与 `V_j^-=(-1)^j u` 两个 rank-one families 具有相同
diagonal `(1,1,1,1)` 与 trace `4`，但对 all-one coefficient vector 的 signed energies
分别为 `16` 与 `0`。因此 diagonal、trace 或 unsigned PSD envelope 在这个有限 scope
内不能识别 signed reassembly。这是 scoped obstruction，不是对所有 growing literal
prime shells 的反例。

```text
TPC222_ROUTE_ADVANCE = YES
TPC222_PSD_PACKET_GRAM = PROVED_EXACT
TPC222_FOUR_POINT_POLARIZATION = PROVED_EXACT
TPC222_TRACE_RAYLEIGH_ENVELOPE = PROVED_EXACT
TPC222_SIGNED_CROSS_TERM_IDENTIFIABILITY = REFUTED_SCOPED
TPC222_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC222_ARITHMETIC_CANCELLATION = NONE
TPC222_ARITHMETIC_ADVANCE = NO
TPC222_FIXED_ATOM_CREDIT = 0
TPC222_L2 = NONE
TPC222_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC222_FULL_GATE_B = OPEN
TPC222_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

strongest positive result：四点极化精确恢复每个 signed cross-term；strongest obstruction：
相同 diagonal/trace 可产生 `16` 与 `0` 两个目标能量；open theorem：把 phase-labelled
cross-correlation 控制在 growing literal prime shell 上；reusable structure：四相位
energy ledger 与 trace/Rayleigh firewall；`ROUND2_CLUE`：

```text
CONTROL_POLARIZED_LITERAL_PACKET_ENERGIES_WITH_SIGNED_CROSS_CORRELATION
```

Bridge proof/checker：`research/tpc-big-road/bridge_b_four_packet_cross_term_obstruction.md`
与 `research/tpc-big-road/tpc_bridge_b_four_packet_cross_term_obstruction_checker.py`。
无 arithmetic `L2`、fixed-atom credit、strict `1/400` 或 twin-prime conclusion。

## 0.15 已发布：TPC-221 collision-graph Schur envelope and literal saturation

项目：`papers/tpc-221-collision-graph-schur-envelope/`

类型：**PROVED_STRUCTURAL_L1 / COLLISION_GRAPH_SCHUR_ENVELOPE**。

TPC-221 将 TPC-220 的 exact multiplicative collision Gram 变成可复用的 operator
interface。若 `B_q` 是 primitive-residue row vector、`Gamma(q,q')=<B_q,B_q'>`，则

```text
E(lambda) = lambda^* Gamma lambda,
E(lambda) <= max_q p_q^(-1) sum_q' |Gamma(q,q')|p_q' * ||lambda||_2^2.
```

第一式是 PSD Gram identity，第二式是 exact weighted Schur envelope。它给出了 collision
degree 的结构性上界，但绝对值操作没有算术 cancellation。literal saturation fixture
取 `h=5`, `H=500`, constant profile 与 `q={101,151,181,191}`；四个 rows 都为
`e_1+e_4`，因此 `Gamma=2J_4`，Schur radius/top Rayleigh quotient 为 `8`，equal
weights 的 coherent-to-diagonal ratio 恰为 `4=P`。

```text
TPC221_ROUTE_ADVANCE = YES
TPC221_STRUCTURAL_THRESHOLD_A = PASS
TPC221_COLLISION_GRAM_PSD = PROVED_EXACT
TPC221_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_WEIGHTED_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_LITERAL_SATURATION = PROVED_EXACT_FINITE
TPC221_ABSOLUTE_SCHUR_SUBP_SAVING = REFUTED_SCOPED
TPC221_ARITHMETIC_CANCELLATION = NONE
TPC221_ARITHMETIC_ADVANCE = NO
TPC221_FIXED_ATOM_CREDIT = 0
TPC221_L2 = NONE
TPC221_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC221_FULL_GATE_B = OPEN
TPC221_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

strongest positive result：exact PSD/weighted-Schur collision envelope；strongest obstruction：
literal aligned rows saturate the absolute envelope and the `P` factor；open theorem：
growing-scale signed/phase-sensitive collision dispersion；reusable structure：weighted
collision-degree operator interface；`ROUND2_CLUE`：

```text
SEEK_SIGNED_PHASE_DISPERSION_BEYOND_ABSOLUTE_COLLISION_DEGREES
```

Bridge proof/checker：`research/tpc-big-road/bridge_b_collision_graph_schur_envelope.md`
与 `research/tpc-big-road/tpc_bridge_b_collision_graph_schur_envelope_checker.py`。
无 arithmetic `L2`、fixed-atom credit、strict `1/400` 或 twin-prime conclusion。

## 0.14 已发布：TPC-220 prime-AP collision crosswalk

项目：`papers/tpc-220-prime-ap-collision-crosswalk/`

类型：**PROVED_STRUCTURAL_L1 / EXACT_PRIME_AP_MULTIPLICATIVE_CROSSWALK**。

TPC-220 沿 TPC-219 的 `E_perp` 线索回到原始 q-labelled rows。对 primitive residue
`a mod h`，单位条件给出 exact weighted prime-AP crosswalk：

```text
sum_q lambda_q B_(h,q)^(j)(a)
  = sum_(m != 0) Pi_(h,m)^(j)(a^(-1)m; lambda),
```

其中 `Pi` 保留 q-dependent cutoff 与 profile。两行 Gram 的 exact expansion 为

```text
Gamma_h^(j,l)(q,q')
 = sum_(m,m') w_(h,m,q)^(j) conjugate(w_(h,m',q')^(l))
     1_(m q'=m' q mod h).
```

`q=q'` 且 `2L_(h,q)<h` 时还原 fixed-q atom energy；off-diagonal 项组成真实的
multiplicative collision graph。3 个 modulus、4 个 prime、constant/affine 两种 profile
的 exact certificate residual 全为零，并确认 off-diagonal collision 非空。

```text
TPC220_ROUTE_ADVANCE = YES
TPC220_STRUCTURAL_THRESHOLD_A = PASS
TPC220_PRIME_AP_CROSSWALK = PROVED_EXACT
TPC220_MULTIPLICATIVE_COLLISION_GRAM = PROVED_EXACT
TPC220_DIAGONAL_REDUCTION = PROVED_EXACT
TPC220_ARITHMETIC_CANCELLATION = NONE
TPC220_ARITHMETIC_ADVANCE = NO
TPC220_FIXED_ATOM_CREDIT = 0
TPC220_L2 = NONE
TPC220_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC220_FULL_GATE_B = OPEN
TPC220_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

strongest positive result：literal q reassembly 已成为 exact weighted prime-AP operator
与 collision Gram；strongest obstruction：off-diagonal multiplicative collisions 不能
被形式上删去；open theorem：在 Schur/absolute 控制之外量化 collision graph；reusable
structure：primitive AP crosswalk plus diagonal/off-diagonal Gram split；`ROUND2_CLUE`：

```text
QUANTIFY_THE_OFF_DIAGONAL_COLLISION_GRAPH_BEYOND_SCHUR
```

Bridge proof/checker：`research/tpc-big-road/bridge_b_prime_ap_collision_crosswalk.md`
与 `research/tpc-big-road/tpc_bridge_b_prime_ap_collision_crosswalk_checker.py`。
无 arithmetic `L2`、fixed-atom credit、strict `1/400` 或 twin-prime conclusion。

## 0.13 已发布：TPC-219 prime-shell longitudinal ledger and the exact P collapse

项目：`papers/tpc-219-prime-shell-longitudinal-ledger/`

类型：**PROVED_STRUCTURAL_L1 / EXACT_LONGITUDINAL_TRANSVERSE_LEDGER**。

TPC-219 对 TPC-218 保留的 q-labelled packet vectors 做 exact constant-mode projection。
若 `Z_q(n)=(K_(j,q)(n))_j`、`P=#Q_x`、`R_q=Z_q-Zbar`，则任意同一 interval 上

```text
E_shell = P(E_diag-E_perp),
E_shell <= eta P E_diag  <=>  E_perp >= (1-eta)E_diag.
```

因此本篇的明确进展不是另一个 Cauchy upper bound，而是把 scalar `P` collapse 的
必要且充分条件精确化为 literal q-transverse lower bound。aligned exact fixture
有 `E_perp=0` 并饱和 `P`；balanced fixture 有 `E_shell=0`。

```text
TPC219_ROUTE_ADVANCE = YES
TPC219_STRUCTURAL_THRESHOLD_A = PASS
TPC219_LONGITUDINAL_TRANSVERSE_IDENTITY = PROVED_EXACT
TPC219_P_COLLAPSE_EQUIVALENCE = PROVED_EXACT
TPC219_ALIGNED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_BALANCED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_ARITHMETIC_CANCELLATION = NONE
TPC219_ARITHMETIC_ADVANCE = NO
TPC219_FIXED_ATOM_CREDIT = 0
TPC219_L2 = NONE
TPC219_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC219_FULL_GATE_B = OPEN
TPC219_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

strongest positive result：`P` collapse 的 exact iff transverse criterion；strongest
obstruction：aligned q labels have zero transverse energy；open theorem：把 `E_perp`
改写并控制为 literal prime-AP/multiplicative collision data；reusable structure：
constant-mode orthogonal projection and integrated Pythagorean ledger；`ROUND2_CLUE`：

```text
REEXPRESS_TRANSVERSE_ENERGY_AS_LITERAL_PRIME_AP_COLLISION_DATA
```

Bridge proof/checker：`research/tpc-big-road/bridge_b_prime_shell_longitudinal_transverse_ledger.md`
与 `research/tpc-big-road/tpc_bridge_b_prime_shell_longitudinal_transverse_ledger_checker.py`。
无 arithmetic `L2`、fixed-atom credit、strict `1/400` 或 twin-prime conclusion。

## 0.12 已发布：TPC-218 prime-shell Hilbert lift and the sharp collapse barrier

项目：`papers/tpc-218-prime-shell-packet-lift/`

类型：**PROVED_STRUCTURAL_L1 / PRIME_LABEL_AND_PACKET_PRESERVING_LIFT**。

TPC-218 是 TPC-217 的自然后续：不在 finite-window large sieve 前合并 prime shell，
而是把 `(q,j)` 保留为 Hilbert coordinates。对 literal V46 common-source rows，固定-q
cutoff injectivity、active-cluster harmonic bound 与 coordinatewise additive large sieve
证明

```text
N^(-1) sum_(n in I_x)||K_vec(n)||_2^2
  << J M^2 x^(1/96)(log x)^5.
```

最后用 `P=#Q_x<=2Q` 的 pointwise Cauchy 合并 q labels，恢复 scalar packet envelope
`x^(11/32)(log x)^5`。因此本篇的明确进展是：split scale `Q^2/H=x^(1/96)` 与
scalar shell 的 `P` cost 被严格分离；这不是 arithmetic saving。

```text
TPC218_ROUTE_ADVANCE = YES
TPC218_STRUCTURAL_THRESHOLD_A = PASS
TPC218_HILBERT_VALUED_LARGE_SIEVE = PROVED_STANDARD_TENSOR_LIFT
TPC218_PRIME_LABEL_PRESERVATION = PROVED_EXACT
TPC218_PACKET_MATRIX_BOUND = PROVED_EXACT
TPC218_SPLIT_NORMALIZED_EXPONENT = PROVED_1_OVER_96_LOG_FIVE
TPC218_SCALAR_COLLAPSE_RECOVERY = PROVED_X_11_OVER_32_LOG_FIVE
TPC218_Q_COLLAPSE_COST = PROVED_P_FACTOR
TPC218_Q_ORTHOGONALITY = REFUTED_SCOPED
TPC218_PACKET_ALIGNMENT = REFUTED_SCOPED
TPC218_ARITHMETIC_CANCELLATION = NONE
TPC218_ARITHMETIC_ADVANCE = NO
TPC218_FIXED_ATOM_CREDIT = 0
TPC218_L2 = NONE
TPC218_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC218_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC218_FULL_GATE_B = OPEN
TPC218_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

strongest positive result：labels survive a finite-window lift and the exact `P` collapse
is exposed. strongest obstruction：the exact q-aligned fixture attains ratio `P=4`, while
parallel packet geometry has projection ratio `1`. open theorem：prove literal signed
prime-shell/four-packet reassembly beating `P` while retaining zero/nonunit and normalization
interfaces. reusable structure：Hilbert-valued large sieve + PSD packet Gram + four-point
polarization. `ROUND2_CLUE`：

```text
PROVE_A_SIGNED_PRIME_SHELL_REASSEMBLY_BEYOND_THE_EXACT_P_COLLAPSE
```

Bridge proof/checker：`research/tpc-big-road/bridge_b_prime_shell_packet_lift.md` 与
`research/tpc-big-road/tpc_bridge_b_prime_shell_packet_lift_checker.py`。无 arithmetic
`L2`、fixed-atom credit、strict `1/400` 或 twin-prime conclusion。

## 0.11 已发布：TPC-217 finite-window attachment by reduced rational-frequency large sieve

项目：`papers/tpc-217-finite-window-rational-large-sieve/`

类型：**PROVED_STRUCTURAL_L1 / FINITE_WINDOW_ATTACHMENT**。

TPC-217 直接执行 TPC-216 的 finite-window `ROUND2_CLUE`。保持同一个 literal
common-source kernel，先按 reduced rational frequencies 精确重组，再用分母不超过
`U` 的 Farey spacing `delta>=U^(-2)` 与 standard additive large sieve，将
complete-period direct-sum envelope 接到 `I_x=(x/2,x]`。由 TPC-214/215 的 exact
cluster regrouping/majorant 与 TPC-216 的 direct envelope 得到

```text
N^(-1) sum_(n in I_x)|K(n)|^2
  <<_psi x^(11/32)(log x)^5,
U^2/x=x^(-67/200),
```

对应的 unnormalized finite-window exponent 是 `43/32+o(1)`。有限 certificate 覆盖
14 个 active divisors、16 个 reduced denominators 与 3 个 translated windows；独立
aligned one-point fixture 的 exact coherent-to-diagonal ratio 为 `2`，因此 free
finite-window orthogonality 只在该 scope 被 `REFUTED_SCOPED`。

```text
TPC217_ROUTE_ADVANCE = YES
TPC217_STRUCTURAL_THRESHOLD_A = PASS
TPC217_REDUCED_FREQUENCY_REGROUPING = PROVED_EXACT
TPC217_FAREY_SPACING = PROVED_EXACT
TPC217_ADDITIVE_LARGE_SIEVE = PROVED_STANDARD
TPC217_FINITE_WINDOW_ATTACHMENT = PROVED_X_11_OVER_32_LOG_FIVE_NORMALIZED
TPC217_UNNORMALIZED_WINDOW_EXPONENT = PROVED_43_OVER_32
TPC217_WINDOW_LOSS = PROVED_1_PLUS_U2_OVER_N
TPC217_FINITE_WINDOW_OFF_FREQUENCY_GRAM = CONTROLLED_BY_LARGE_SIEVE
TPC217_ALIGNED_ONE_POINT_ORTHOGONALITY = REFUTED_SCOPED
TPC217_PRIME_SHELL_REASSEMBLY = OPEN
TPC217_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC217_ARITHMETIC_CANCELLATION = NONE
TPC217_ARITHMETIC_ADVANCE = NO
TPC217_FIXED_ATOM_CREDIT = 0
TPC217_L2 = NONE
TPC217_FULL_GATE_B = OPEN
TPC217_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

```text
STRONGEST_POSITIVE_RESULT = LITERAL_COMMON_SOURCE_FINITE_WINDOW_BOUND_AT_X_11_OVER_32_LOG_FIVE_NORMALIZED
STRONGEST_OBSTRUCTION = ONE_POINT_ALIGNED_SHELL_HAS_EXACT_COHERENT_TO_DIAGONAL_RATIO_TWO
OPEN_THEOREM = REASSEMBLE_THE_FINITE_WINDOW_BOUND_INTO_THE_LITERAL_SIGNED_PRIME_SHELL_AND_FOUR_PACKET_GATE_B_SCALAR
REUSABLE_STRUCTURE = EXACT_REDUCED_REGROUPING_PLUS_FAREY_SPACING_PLUS_ADDITIVE_LARGE_SIEVE_PLUS_TPC215_TPC216_ENVELOPES
ROUND2_CLUE = PRESERVE_THE_FINITE_WINDOW_LARGE_SIEVE_ATTACHMENT_WHILE_REINTRODUCING_LITERAL_PRIME_SHELL_AND_FOUR_PACKET_REASSEMBLY
```

Route A remains not applicable; Route-B structural threshold A passes. The paper PDF,
certificate, independent checker and frequency-crowding adversary are released under
the same author lock. There is still no arithmetic `L2`, fixed-atom credit, strict
`1/400`, full Gate B, or twin-prime conclusion.

## 0.10 已发布：TPC-216 direct-sum row-energy envelope and the Cauchy bottleneck

项目：`papers/tpc-216-direct-sum-row-energy-envelope/`

类型：**PROVED_STRUCTURAL_L1 / DIRECT_SUM_ROW_ENERGY_ENVELOPE**。

TPC-216 直接推进 TPC-215 留下的 direct-sum quantity。source inequality `4Q<H`
使每个 fixed-q cutoff 的 integer atoms 在模 `d` 下 exact 不碰撞；一次 shell Cauchy、
`P<=2Q` 与 elementary divisor harmonic sum 证明

```text
L^(-1)E_direct <<_psi (Q^3/H)(log U)^3
                    = x^(11/32)(log x)^3.
```

finite exact adversary 中 `d=5`, `H=500`, `q={101,131,151,181}` 的四个 rows 全部
支撑在 `{1,4}`，coherence ratio 约为 `3.70568607565`，因此 shell Cauchy 不能靠
structural orthogonality 免费删除。

```text
TPC216_ROUTE_ADVANCE = YES
TPC216_STRUCTURAL_THRESHOLD_A = PASS
TPC216_FIXED_Q_NO_COLLISION = PROVED_EXACT
TPC216_FIXED_Q_ROW_ENERGY = PROVED_EXACT
TPC216_SHELL_CAUCHY_ENVELOPE = PROVED_EXACT
TPC216_PRIME_SHELL_CARDINALITY = PROVED_P_LE_2Q
TPC216_NORMALIZED_EXPONENT = PROVED_11_OVER_32
TPC216_DIRECT_SUM_ROW_ENERGY_ENVELOPE = PROVED_X_11_OVER_32_LOG_CUBED
TPC216_ARITHMETIC_CANCELLATION = NONE
TPC216_ALIGNED_SUPPORT_ADVERSARY = NUMERICALLY_CERTIFIED_EXACT_RATIONAL
TPC216_FREE_Q_ORTHOGONALITY = REFUTED_SCOPED
TPC216_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN
TPC216_PRIME_SHELL_REASSEMBLY = OPEN
TPC216_FULL_GATE_B = OPEN
TPC216_ARITHMETIC_ADVANCE = NO
TPC216_FIXED_ATOM_CREDIT = 0
TPC216_L2 = NONE
TPC216_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

```text
STRONGEST_POSITIVE_RESULT = SOURCE_LOCKED_COMPLETE_PERIOD_DIRECT_SUM_ROW_ENERGY_IS_AT_MOST_X_11_OVER_32_LOG_CUBED
STRONGEST_OBSTRUCTION = FINITE_PRIME_SHELL_ROWS_CAN_HAVE_EXACTLY_ALIGNED_RESIDUE_SUPPORT
OPEN_THEOREM = ATTACH_COMPLETE_PERIOD_DIRECT_SUM_ENVELOPE_TO_LITERAL_FINITE_WINDOW
REUSABLE_STRUCTURE = FIXED_Q_INJECTIVE_ATOMS_PLUS_SHELL_CAUCHY_PLUS_MOBIUS_LOG_DIVISOR_SUM
ROUND2_CLUE = ATTACH_THE_COMPLETE_PERIOD_DIRECT_SUM_ENVELOPE_TO_THE_LITERAL_FINITE_WINDOW_WITHOUT_FREE_SHELL_ORTHOGONALITY
```

Bridge proof/checker：`research/tpc-big-road/bridge_b_direct_sum_row_energy_envelope.md`
与 `research/tpc-big-road/tpc_bridge_b_direct_sum_row_energy_envelope_checker.py`。
没有 arithmetic `L2`、fixed-atom credit、strict `1/400` 或 twin-prime conclusion。

## 0.9 已发布：TPC-215 short-quotient Möbius tails and the no-power-loss majorant

项目：`papers/tpc-215-short-quotient-mobius-majorant/`

类型：**PROVED_STRUCTURAL_L1 / SHORT_QUOTIENT_CLUSTER_MAJORANT**。

TPC-215 直接推进 TPC-214 的 literal cluster tail。对 V46 的完整 squarefree band
`Y0<d<=U`，非零 emitter cutoff 强制每个 active reduced denominator 满足
`h>=H/q_max>=H/(2Q)=2Y0`，故 `h` 自身属于 band。写 `d=hk` 得到 exact
short-quotient normal form，且 `k<=2UQ/H=2x^(23/2400+o(1))`。`d=h` 项给出
direct coefficient mass 的 diagonal anchor；harmonic triangle 和 row-norm divisor
decomposition 从而证明

```text
E_cluster <= A_x E_direct,
A_x=O((log x)^2)=x^(o(1)).
```

该 theorem 排除了 cluster algebra 的 fixed-power amplification，但不提供 saving。
对每个 active `U/2<h<=U`，唯一 band multiple 是 `d=h`，所以 coefficient ratio
`|C_h|^2/D_h=1` exact，形成 sharp scoped obstruction。有限 fixture 有 14 个 active
rows 与 7 个 top-shell rows；global ratio `0.5969532588` 是 numerical observation。

```text
TPC215_ROUTE_ADVANCE = YES
TPC215_STRUCTURAL_THRESHOLD_A = PASS
TPC215_ACTIVATION_FLOOR = PROVED_EXACT
TPC215_SHORT_QUOTIENT_NORMAL_FORM = PROVED_EXACT
TPC215_QUOTIENT_LENGTH_EXPONENT = PROVED_23_OVER_2400
TPC215_ROW_NORM_DIVISOR_DECOMPOSITION = PROVED_EXACT
TPC215_CLUSTER_TO_DIRECT_MAJORANT = PROVED_O_LOG_X_SQUARED
TPC215_FIXED_POWER_CLUSTER_AMPLIFICATION = EXCLUDED
TPC215_TOP_SHELL_RATIO_ONE = PROVED_EXACT
TPC215_UNIFORM_ROWWISE_POWER_SAVING = REFUTED_SCOPED
TPC215_FINITE_RATIOS = NUMERICAL_OBSERVATION
TPC215_DIRECT_SUM_ARITHMETIC_ENERGY_BOUND = OPEN
TPC215_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN
TPC215_PRIME_SHELL_REASSEMBLY = OPEN
TPC215_ARITHMETIC_ADVANCE = NO
TPC215_FIXED_ATOM_CREDIT = 0
TPC215_L2 = NONE
TPC215_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

```text
STRONGEST_POSITIVE_RESULT = SOURCE_LOCKED_COMPLETE_PERIOD_CLUSTER_GRAM_IS_AT_MOST_O_LOG_X_SQUARED_TIMES_DIVISOR_DIRECT_SUM_ENERGY
STRONGEST_OBSTRUCTION = EVERY_ACTIVE_TOP_SHELL_DENOMINATOR_HAS_EXACT_CLUSTER_TO_DIRECT_COEFFICIENT_RATIO_ONE
OPEN_THEOREM = PHYSICAL_INTERVAL_DIRECT_SUM_ROW_ENERGY_BOUND_WITH_FINITE_WINDOW_AND_PRIME_SHELL_REASSEMBLY
REUSABLE_STRUCTURE = ACTIVATION_FLOOR_PLUS_SHORT_QUOTIENT_TAIL_PLUS_DIAGONAL_ANCHOR_PLUS_ROW_NORM_DIVISOR_DECOMPOSITION
ROUND2_CLUE = BOUND_THE_DIRECT_SUM_PHYSICAL_ROW_ENERGY_BEFORE_REINTRODUCING_CROSS_FREQUENCIES
```

Bridge proof/checker：`research/tpc-big-road/bridge_b_short_quotient_mobius_majorant.md`
与 `research/tpc-big-road/tpc_bridge_b_short_quotient_mobius_majorant_checker.py`。
证书使用 exact rational emitter rows；normal/optimized independent checker 和
adversarial sanity 均通过。没有 arithmetic `L2`、fixed-atom credit、strict `1/400`
或 twin-prime conclusion。

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

## 0.7 已发布：TPC-213 physical profile pullback and the cross-divisor Gram

项目：`papers/tpc-213-physical-profile-cross-gram/`

类型：**PROVED_STRUCTURAL_L1 / THRESHOLD_A / CROSS_DIVISOR_COUPLING**。

TPC-213 直接回答 TPC-212 的 `ROUND2_CLUE`：在 direct-sum Cauchy 或 outer absolute
之前，把 literal V46 profile 视为一个 common physical source，经 residue lift `C_d`
送入每个 divisor residue space，再由 reciprocal emitter pull back 到同一个 physical
support。主要结果为：

1. **PROVED** — `R_d=C_d(v-b_d)` 时，所有 divisor scalar 的 exact affine pullback
   identity 保留共同 source term `K=sum_d K_d` 与 divisor-dependent profile correction；
2. **PROVED** — complete lcm period 上，`C_d C_e^*` 恰为
   `(L/lcm(d,e)) 1_(a=b mod gcd(d,e))`；
3. **PROVED_FINITE** — emitter pullback Gram 恰为 shared rational frequency 的
   intersection sum；
4. **PROVED_FINITE** — fixture `d={5,7,35}`, `q={11,13,17}`, `H=40` 有 joint lift
   rank `35`、codomain dependency `12`，cross-Gram 分别为 `0,560,770`；
5. **REFUTED_SCOPED** — 将 literal common-source family 替换为 orthogonal direct sum
   不是恒等式；非零 nested-divisor cross terms 在 exact fixture 中出现；
6. **OPEN** — smooth `psi`、`mu(d)log(d)/d`、four-packet signs、zero-axis、prime shell
   和 actual V46 range 下的 joint asymptotic Gram bound。

```text
TPC213_ROUTE_ADVANCE = YES
TPC213_STRUCTURAL_THRESHOLD_A = PASS
TPC213_PHYSICAL_PROFILE_EMITTER_PULLBACK = PROVED_EXACT
TPC213_RESIDUE_LIFT_GCD_ALIASING = PROVED_EXACT
TPC213_CROSS_DIVISOR_FREQUENCY_GRAM = PROVED_EXACT_FINITE
TPC213_PHYSICAL_DIRECT_SUM_REPLACEMENT = REFUTED_SCOPED
TPC213_LITERAL_V46_ASYMPTOTIC_GRAM_BOUND = OPEN
TPC213_PRIME_SHELL_REASSEMBLY = OPEN
TPC213_ARITHMETIC_ADVANCE = NO
TPC213_FIXED_ATOM_CREDIT = 0
TPC213_L2 = NONE
TPC213_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC213_TPC_TRIGGER = true
```

```text
STRONGEST_POSITIVE_RESULT = EXACT_COMMON_SOURCE_PULLBACK_AND_SHARED_FREQUENCY_GRAM
STRONGEST_OBSTRUCTION = NONZERO_NESTED_DIVISOR_CROSS_TERMS_REFUTE_PHYSICAL_DIRECT_SUM_REPLACEMENT
OPEN_THEOREM = JOINT_LITERAL_V46_PULLBACK_KERNEL_BOUND_WITH_SMOOTH_PSI_AND_PRIME_SHELL
REUSABLE_STRUCTURE = COMMON_SOURCE -> RESIDUE LIFT -> EMITTER PULLBACK -> GCD/LCM ALIASING -> FREQUENCY GRAM
ROUND2_CLUE = GROUP_LITERAL_V46_KERNEL_BY_SHARED_RATIONAL_FREQUENCY_BEFORE_D_OR_Q_TRIANGLE_AND_TEST_SIGNED_CLUSTER_CANCELLATION
```

The certificate covers 47 Euler-profile coordinates, 3 lift cases, 3 emitter rows and 3
cross-Gram cases.  Unit reciprocal weights and the omitted logarithmic scalar are explicit
finite modeling choices; they are not arithmetic evidence.

## 0.8 已发布：TPC-214 Möbius-weighted shared-frequency clusters

项目：`papers/tpc-214-mobius-frequency-clusters/`

类型：**PROVED_STRUCTURAL_L1 / THRESHOLD_A / MOBIUS_CLUSTER_REDUCTION**。

TPC-214 恢复 TPC-213 暂时剥离的 literal coefficient
`c_d=mu(d)log(d)/d`，并证明了两个相互锁定的 exact 结果：

1. **PROVED_EXACT** — 对 `h|d`，实际整数 cutoff 下的 coefficient-free emitter
   满足 `B_d((d/h)r)=B_h(r)`；
2. **PROVED_EXACT** — 在完整 `L=lcm(D)` 周期上，common-source Gram 按 reduced
   rational denominator factor，系数是 `C_h=sum_(d:h|d)c_d`；
3. **PROVED_EXACT** — `max(Q)<H` 时 additive zero axis 消失；四包复极化在线性
   cluster reduction 后仍保持 exact；
4. **PROVED_EXACT_FINITE_SIGN** — `{5,7,35}` 的总 cross-energy sign 为负，
   `{3,5,7,105}` 的总 sign 为正；
5. **REFUTED_SCOPED** — shared-frequency coupling 本身没有普遍 favorable saving
   sign。两个物理/直和 energy ratios (`0.59634355565371822` 与
   `1.2119952512624363`) 是 numerical observations。

```text
TPC214_ROUTE_ADVANCE = YES
TPC214_STRUCTURAL_THRESHOLD_A = PASS
TPC214_EMITTER_DILATION_COVARIANCE = PROVED_EXACT
TPC214_REDUCED_DENOMINATOR_CLUSTER_FACTOR = PROVED_EXACT
TPC214_ZERO_AXIS_SCOPE = PROVED_EXACT
TPC214_FOUR_PACKET_POLARIZATION = PROVED_EXACT_LINEAR_EXTENSION
TPC214_NESTED_CLUSTER_CANCELLATION = PROVED_EXACT_FINITE_SIGN
TPC214_COMPOSITE_QUOTIENT_ENHANCEMENT = PROVED_EXACT_FINITE_SIGN
TPC214_FINITE_ENERGY_RATIOS = NUMERICAL_OBSERVATION
TPC214_UNIVERSAL_CLUSTER_SAVING_SIGN = REFUTED_SCOPED
TPC214_LITERAL_V46_ASYMPTOTIC_CLUSTER_BOUND = OPEN
TPC214_PRIME_SHELL_REASSEMBLY = OPEN
TPC214_ARITHMETIC_ADVANCE = NO
TPC214_FIXED_ATOM_CREDIT = 0
TPC214_L2 = NONE
TPC214_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

```text
STRONGEST_POSITIVE_RESULT = EXACT_REDUCED_DENOMINATOR_CLUSTER_FACTOR_OF_THE_COMMON_SOURCE_GRAM
STRONGEST_OBSTRUCTION = FINITE_COMPOSITE_QUOTIENT_ENHANCEMENT_REFUTES_UNIVERSAL_CLUSTER_SAVING_SIGN
OPEN_THEOREM = UNIFORM_LITERAL_V46_MOBIUS_LOG_CLUSTER_BOUND_WITH_PRIME_SHELL_REASSEMBLY
REUSABLE_STRUCTURE = DILATION_COVARIANCE_PLUS_REDUCED_FREQUENCY_CLUSTER_TAIL
ROUND2_CLUE = ESTIMATE_THE_MOBIUS_LOG_TAILS_C_h_BEFORE_ANY_PRIME_SHELL_OR_Q_TRIANGLE
```

The bridge proof is `research/tpc-big-road/bridge_b_mobius_frequency_clusters.md` and
the independent release checker is
`research/tpc-big-road/tpc_bridge_b_mobius_frequency_clusters_checker.py`.  The
certificate covers two fixture families, 12 reduced-denominator rows, 22 dilation pairs,
and five nonzero cross-pair rows.  It supplies no arithmetic `L2`, fixed-atom credit,
strict `1/400` payment, or twin-prime conclusion.

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
| 2026-08-31 | V170 | PSD Gram trace-power chain、24-row Schatten-4/Frobenius opposite-trend certificate、exact small rational trace anchor、independent replay 与 finite spectral-compression firewall | **NUMERICALLY_CERTIFIED_FINITE_SCHATTEN4_COMPRESSION_AND_OPERATOR_ENVELOPE / TPC-317** |
| 2026-08-30 | V169 | literal source-to-output operator、exact signed-difference/residue Hilbert--Schmidt identity、finite Frobenius L2 envelope、80 coordinate lower probes、8/8 normalized-HS two-panel rise 与 fresh-panel gap obstruction | **PROVED_EXACT_FINITE_LITERAL_ARITHMETIC_L2_ENVELOPE_PLUS_TWO_SCALE_OBSTRUCTION / TPC-316** |
| 2026-08-25 | V96 | hard rectangular window 的 harmonic Gram row bound、双边 `1+-epsilon` near-isometry、signed bilinear transfer 与 V59 `x^(-67/200)log x` error | **PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER / TPC-243** |
| 2026-08-25 | V95 | literal `C_4` phase-energy complete spectrum、sharp fixed-total-energy cross disk、imbalance/Gram defect 与 TPC-241-to-V59 typed no-transfer | **PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER / TPC-242** |
| 2026-08-24 | V94 | fixed frozen common profile 的 top-prime q-collapsed coefficient与 finite-window explicit liminf，证明 unsigned `1/48` fixed-power sharp up to logarithms | **PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_COLLISION_SHARPNESS / TPC-241** |
| 2026-08-24 | V93 | fixed frozen profile 的 top-prime q-split direct-energy exact asymptotic、explicit `1197 kappa_psi log2/800` constant 与 no-fixed-power-saving obstruction | **PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_DIRECT_ENERGY_FLOOR / TPC-240** |
| 2026-08-24 | V89 | physical gcd-fiber multiplicity theorem、unnormalized weighted Bessel envelope 与 exact triple-collision obstruction | **PROVED_STRUCTURAL_L1 / TPC-236** |
| 2026-08-24 | V88 | V59 physical-depth exact crosswalk、single-clock iff obstruction 与 packet-output normalization firewall | **PROVED_STRUCTURAL_L1 / TPC-235** |
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
| 2026-08-22 | V70 | reduced rational-frequency regrouping、Farey spacing、finite-window additive large-sieve attachment；aligned one-point ratio-two obstruction | **PROVED_STRUCTURAL_L1 / FINITE_WINDOW_ATTACHMENT** |
| 2026-08-17 | V60 | moving-hole projector、exact diagonal lift与 `x^(53/32+o(1))` collective translation payment | **PROVED_STRUCTURAL_L1 / TPC-207** |
| 2026-08-17 | V61 | complete-graph zero-hole additive edge frame、edgewise diagonal deletion与 literal-edge no-sparsification | **PROVED_STRUCTURAL_L1 / TPC-208** |
| 2026-08-18 | V65 | truncated divisor-band Boolean boundary、reciprocal occupancy collision Gram 与 scoped emitter-only obstruction | **PROVED_STRUCTURAL_L1 / TPC-212** |
| 2026-08-19 | V66 | common-source physical profile pullback、gcd/lcm residue aliasing 与 shared-frequency cross-divisor Gram | **PROVED_STRUCTURAL_L1 / TPC-213** |

下一次更新应优先回答：

TPC-316 之后的 immediate priority 是：在同一 literal source-to-output operator 上，寻找
真正 growing 的 operator-norm estimate 或 arithmetic cancellation；不得把 finite
Frobenius envelope、coordinate probes 或两面板趋势升级成 asymptotic power claim。
以下条目保留为既有路线的候选 backlog。

1. 能否对 TPC-213 的 shared rational-frequency clusters，在保留 `mu(d)log(d)/d`、smooth
   `psi`、four-packet signs、zero-axis 与 prime shell 的前提下证明 signed cancellation
   或给出更强的 positive-Gram obstruction；
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
