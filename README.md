# Exploring Prime Distribution via Dynamical Methods

## 1. Exploring the Hilbert–Pólya Conjecture
- **A**: Construct a canonical dynamical spectral determinant.
- **B**: Complete non-self-adjoint dynamical objects into scattering/unitary objects that preserve the time direction.
- **C**: Obtain a genuinely self-adjoint operator and derive the $T \log T$ counting law intrinsically.
- **D**: Extract prime powers and von Mangoldt weights from the dynamical trace.
- **E**: Prove that the spectral divisor coincides exactly with the divisor of the completed zeta function.

## 2. Exploring the Twin Prime Conjecture

当前主线状态：TPC-337--368 已完成一条连续的 twin-prime finite audit chain。TPC-337
把四个 source masks 接入五个 coordinate controls 的 output covariance；TPC-338 将
control orbit 扩展到九个并发现 signed covariance 的 ensemble sign reversal；TPC-339
用 support-restricted Frobenius envelope 替代 sign heuristic；TPC-340 再加入 global
Schur envelope；TPC-341 在三个 fresh windows 上用 leave-one-control-out 检验
nuisance orthogonalization 的稳定性；TPC-342 又在三个完全 disjoint、cutoff-safe 的
新窗口上独立复现 aggregate-versus-holdout split。TPC-343 将 TPC-341 与 TPC-342 合并成
跨面板 meta-certificate：row-block fit 仍通过，但 shared nuisance coefficient 在两种
权重下均失败。TPC-344 随后加入预声明的 panel-contrast nuisance basis：raw pooled
retention 降到 `0.2962189247`，但 equal-row retention 回升到 `0.3186506700`，
形成 weighting-sensitive partial repair。TPC-345 再把比较提升到不依赖坐标的
principal-angle/Grassmann 几何：两个 panel 保留一个强对齐方向，但第一主角在
raw 到 equal-row weighting 下由约 `5.31°` 移到 `23.87°`，且双向 transfer
均失败。TPC-346 又加入一个预声明、disjoint、cutoff-safe 的第三 panel：fresh
own-fit 在 raw/equal-row 下为 `0.3159173453/0.3294074741`，三 panel
panel-adaptive fit 只有 raw `0.2999630726` 的窄幅 crossing，equal-row 回到
`0.3222362713305`；全部 transfer、leave-one-panel-out 与 fresh control-LOO 均失败，
因此只冻结该有限 panel-adaptive 分支。整条链仍是有限 declared-model certificate：
source-uniform arithmetic $L^2$、uniform masked operator bound、fixed-power credit 与
twin-prime endpoint 均未关闭。TPC-347 随后把 literal masked prime-shell block
精确拆成 unmasked translation-invariant convolution 加上 divisibility-mask defect：
192 个 finite spectral rows 中有 93 个 defect/ideal ratio 超过 `1/4`，而
`96/96` 个 ideal origin pairs 保持 translation invariance。因此 mask shortcut 在
声明面板上被 refute，但 masked operator bound 与 source-uniform arithmetic $L^2$ 仍然
open。

TPC-348 紧接着把 TPC-347 的 defect 进一步定位到预声明的 mask-hit positions：对
`J_I={t: p|t}` 上的坐标列给出 exact induced-norm lower witness。锁定面板的
`192/192` 行都有正 witness，best-hit witness/defect ratio 为
`0.453958762219--0.897148966365`，position formula 的最大 replay discrepancy 为
`2.0872192863e-14`。这仍是 finite position audit；source-uniform arithmetic $L^2$、
uniform masked operator bound、fixed-power credit 与 twin-prime endpoint 继续 open。

TPC-349 再把 mask-hit coordinates 组合成零和 prime-incidence contrast：升序 shell
primes 取等量 `+1/-1`（奇数 shell 留一个中性 prime），得到 exact incidence Gram
展开与 induced-norm lower witness。`192/192` 行有正响应，signed/defect ratio 为
`0.39083565842--0.954375010719`；`136/192` 行超过最佳单坐标基线，`175/192`
行达到 defect norm 的一半。但 56 行仍低于坐标基线，所以 universal balanced gain
只可记为 `REFUTED_SCOPED`；arithmetic advance 仍为 NO。

TPC-350 将同一 zero-sum incidence witness 移到三个 fresh origins、四个长度与
`Q=36,80,128,256` 的扩展 shell ladder。`192/192` 行仍有正响应，
signed/defect ratio 为 `0.0657381187306--0.8797933448`，但只有 `70/192` 行超过
coordinate baseline、`91/192` 行达到 half-defect，长度序列仅 `24/48`
nondecreasing。特别地，`Q=256` 的 48 行全部低于 half-defect，所以 fresh finite
replication 成立，而 universal quarter-floor 在声明面板上为 `REFUTED_SCOPED`。

TPC-351 随后冻结一个不按 row 拟合的 reciprocal-shell contrast：对
`Q<p_j<=2Q` 取 `gamma_j=1/p_j-r^(-1)sum_k 1/p_k`。该有理规则 exact zero-sum，
并保留 incidence Gram 展开与 induced-norm lower witness。在与 TPC-350 完全相同的
192-row panel 上，`192/192` 行有正响应，`180/192` 行改善 parent，ratio 提升到
`0.0917557319271--0.901734353382`；coordinate baseline census 为 `86/192`，
half-defect census 为 `111/192`。不过仍有 12 行退化、ratio floor 低于 `1/4`，
且只有 `25/48` length series nondecreasing，因此它是有限 scale repair，不是
source-uniform arithmetic theorem；下一步必须在 disjoint holdout 上 hostile 验证。

TPC-352 按该 clue 在三个完全 disjoint origins、三种长度与新的
`Q=64,128,256,512` shell ladder 上做 adversarial holdout。`144/144` 行的 reciprocal
witness 仍有正响应，但只在 `118/144` 行超过 balanced parent；reciprocal/defect
ratio 为 `0.0801262572786--0.829632172143`，`49/144` 达到 half-defect，`47/144`
超过 coordinate baseline，且仅 `22/48` length series nondecreasing。关键是
`Q=256` 的 reciprocal floor `0.0801262572786` 低于 parent 的 `0.099642909832`，
所以 TPC-351 的 finite repair 不具备 uniform holdout transfer；该 incidence branch
冻结，主路返回 source-native masked arithmetic `L2`。

TPC-353 将这条主路具体化为 literal source-native masked operator：把继承的 V59
有限 residual `beta=Lambda-b` 直接送入 two-endpoint divisibility-masked matrix，并
以 operator-level polarization identity 与 Cauchy envelope 逐行审计。三个 origins、
三种 source counts、三个 shell anchors、两种 exponent 和四种 sign laws 形成
`216` rows；`216/216` 个 operator images 的 alignment 为正。all-plus 的 output
coefficient `kappa_A` 为 `0.69291151430780062--0.99626802812598902`，而同一窗口的
source coefficient 只有 `0.39570365481042707--0.43581376702257324`；其他 sign laws
的 output range 则降到 `0.00774850--0.739230` 等量级。由此确认 source/output
cross-term 是真实的 operator interface，同时也形成 obstruction：有限正 alignment
不能升级为 source-uniform masked arithmetic `L2`，下一关转向 disjoint higher-origin
holdout 或 position-aware masked bound。

TPC-354 随后冻结所有非-origin protocol fields，只把同一 source/operator attachment
移到 disjoint higher origins `21001,23001,25001`。在相同 counts、shell anchors、
exponents、四种 sign laws、`H=66` 与 source cutoff 下，`216/216` rows 仍有正
output alignment；all-plus output `kappa_A` 为
`0.65076036812307647--0.99135023146539858`，mean 为 `0.87436211602135017`，
source coefficient 为 `0.36357606682978283--0.38648419369238701`。相对
TPC-353 parent，all-plus minimum/mean shift 为 `-0.042151146184724153` /
`-0.021249745559872912`，所以 positive transfer 保留而 floor transfer 为
`REFUTED_SCOPED`。这是 higher-origin finite obstruction，不是 source-uniform
arithmetic `L2`、power saving、Route-B reassembly 或 twin-prime conclusion；下一关
测试 position-aware masked normalization/bound。

```text
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
TPC354_ROUND2_CLUE = TEST_POSITION_AWARE_MASKED_BOUND_ORIGIN_SCALE_NORMALIZATION_OR_CONTROLLED_SIGN_LAW_SUBSPACE
```

TPC-355 接着测试了一个预先固定、只依赖 unsigned mask geometry 的 position-aware
对称归一化：对每个 prime component `B_p` 取
`G_u=sum_(p,t) B_p(u,t)^2`，再用 `A#=D_G^(-1/2) A D_G^(-1/2)`。在 TPC-353
低-origin、TPC-354 higher-origin 与全新 `29001,33001,37001` fresh panel 的
`648` rows 上，raw 与 normalized 两套度量各有 `647/648` positive、`1/648`
negative、`0` unresolved。all-plus minimum 的 low-to-higher drop 从
`0.042151146184724153` 降为 `0.026236988152766205`，有限 reduction fraction
为 `0.37754982894688971`；但 mean drop 从 `0.021249745559872912` 变为
`0.024839744603963321`，且 fresh mod-4 row 仍为负。因此这是 finite partial
repair 与 law/mean obstruction，不是 source-uniform bound 或 arithmetic advance。

```text
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
TPC355_ROUND2_CLUE = TEST_ADVERSARIAL_POSITION_NORMALIZATION_OR_LAW_INVARIANT_BOUND_ON_FRESH_ORIGINS
```

TPC-356 紧接着冻结 TPC-355 normalization，并把 origins 的选择本身变成一个
response-blind adversarial test：在 38001+211j、0<=j<=50 的 51 个候选上，
以 count 256 的六个 (Q,s) unsigned geometry spread 排序，按最小间隔 1536
的 greedy rule 选出 (38423,42010,45597)。随后按父代完整 protocol 重放
216 rows；raw 与 normalized alignment 均为 216/216 positive。all-plus
minimum 从 0.63140161782616067 升至 0.65046429467683675，mean 从
0.8687258535297816 升至 0.87560762679420479，有限 gain 分别为
0.019062676850676086 与 0.0068817732644231855。这是 geometry-only
selection 下的 finite transfer signal；origin/scale uniformity、source-uniform
arithmetic L2、masked operator bound、fixed-power credit、Route-B reassembly
与 twin-prime endpoint 仍 open，arithmetic advance 仍为 NO。

```text
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
TPC356_ROUND2_CLUE = TEST_ORIGIN_SCALE_STABILITY_OR_OPERATOR_NORM_CERTIFICATE_BEFORE_ANY_ARITHMETIC_REASSEMBLY
```

```text
TPC343_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE
TPC343_STACKED_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC343_ROW_BLOCK_META = NUMERICALLY_CERTIFIED_FINITE_6_ROW_POOLED_PROJECTION
TPC343_SHARED_COEFFICIENT_STABILITY = REFUTED_SCOPED
TPC343_HOLDOUT_META = NUMERICALLY_CERTIFIED_FINITE_54_RECORDS
TPC343_ARITHMETIC_ADVANCE = NO
TPC343_FIXED_POWER_CREDIT = 0
TPC343_SOURCE_UNIFORM_L2 = OPEN
TPC343_FULL_GATE_B = OPEN
TPC343_TWIN_PRIME_RESULT = NONE
TPC343_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE
TPC343_ROUND2_CLUE = ALTERNATIVE_NUISANCE_BASIS_OR_PRINCIPAL_ANGLE_AUDIT

```text
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
```

```text
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
```

```text
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
```

```text
TPC347_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_CONVOLUTION_MASK_DEFECT_INTERFACE_PLUS_NUMERICALLY_CERTIFIED_FINITE_SPECTRAL_AUDIT
TPC347_MASK_FACTORISATION = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC347_UNMASKED_FOURIER_INTERFACE = PROVED_EXACT_CONDITIONAL
TPC347_TRANSLATION_INVARIANCE = NUMERICALLY_CERTIFIED_FINITE_96_OF_96
TPC347_MASK_DEFECT_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
TPC347_DEFECT_DISCARDABILITY = REFUTED_SCOPED
TPC347_ARITHMETIC_ADVANCE = NO
TPC347_FIXED_POWER_CREDIT = 0
TPC347_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
TPC347_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC347_FULL_GATE_B = OPEN
TPC347_TWIN_PRIME_RESULT = NONE
TPC347_STATUS = PROVED_EXACT_FINITE_CONVOLUTION_MASK_DEFECT_INTERFACE_PLUS_NUMERICALLY_CERTIFIED_FINITE_SPECTRAL_AUDIT
TPC347_ROUND2_CLUE = QUANTIFY_MASK_DEFECT_LOWER_WITNESSES_BEFORE_SOURCE_NATIVE_L2
```

```text
TPC348_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_COORDINATE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_POSITION_AUDIT
TPC348_COORDINATE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
TPC348_MASK_HIT_SELECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC348_POSITION_FORMULA = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC348_FINITE_POSITION_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
TPC348_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
TPC348_MASK_DISCARDABILITY = REFUTED_SCOPED
TPC348_BEST_HIT_TO_DEFECT_RATIO = 0.453958762219--0.897148966365
TPC348_BEST_HIT_TO_IDEAL_RATIO = 0.0183057714619--0.336311065586
TPC348_ARITHMETIC_ADVANCE = NO
TPC348_FIXED_POWER_CREDIT = 0
TPC348_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
TPC348_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC348_FULL_GATE_B = OPEN
TPC348_TWIN_PRIME_RESULT = NONE
TPC348_STATUS = PROVED_EXACT_FINITE_COORDINATE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_POSITION_AUDIT
TPC348_ROUND2_CLUE = TEST_PRIME_BALANCED_DEFECT_WITNESSES_BEFORE_SOURCE_NATIVE_L2
```

```text
TPC349_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_PRIME_BALANCED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_AUDIT
TPC349_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
TPC349_PRIME_BALANCE_RULE = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC349_INCIDENCE_GRAM_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC349_FINITE_SIGNED_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
TPC349_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
TPC349_COORDINATE_BASELINE_BEATEN = NUMERICALLY_CERTIFIED_FINITE_136_OF_192
TPC349_HALF_DEFECT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_175_OF_192
TPC349_UNIVERSAL_BALANCED_GAIN = REFUTED_SCOPED
TPC349_ARITHMETIC_ADVANCE = NO
TPC349_FIXED_POWER_CREDIT = 0
TPC349_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
TPC349_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC349_FULL_GATE_B = OPEN
TPC349_TWIN_PRIME_RESULT = NONE
TPC349_STATUS = PROVED_EXACT_FINITE_PRIME_BALANCED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_AUDIT
TPC349_ROUND2_CLUE = REPLICATE_SIGNED_INCIDENCE_GRAM_ON_GROWING_FRESH_PANELS
```

```text
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
TPC350_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
TPC350_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC350_FULL_GATE_B = OPEN
TPC350_TWIN_PRIME_RESULT = NONE
TPC350_STATUS = PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT
TPC350_ROUND2_CLUE = TEST_SCALE_ADAPTIVE_ZERO_SUM_CONTRAST_ON_HIGH_SHELLS
```

```text
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
TPC351_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
TPC351_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC351_FULL_GATE_B = OPEN
TPC351_TWIN_PRIME_RESULT = NONE
TPC351_STATUS = PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT
TPC351_ROUND2_CLUE = ADVERSARIAL_HOLDOUT_FOR_RECIPROCAL_CONTRAST_BEFORE_BRANCH_FREEZE
```

```text
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
TPC352_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
TPC352_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC352_FULL_GATE_B = OPEN
TPC352_TWIN_PRIME_RESULT = NONE
TPC352_STATUS = PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT
TPC352_ROUND2_CLUE = FREEZE_FINITE_RECIPROCAL_BRANCH_AND_RETURN_TO_SOURCE_NATIVE_L2
```

```text
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
TPC353_ROUND2_CLUE = TEST_SOURCE_NATIVE_L2_CROSS_TERM_ON_DISJOINT_HIGHER_ORIGINS_OR_BUILD_POSITION_AWARE_MASKED_BOUND
```

TPC-331（更早阶段）承接 TPC-330，把五个预声明的 coordinate controls 视为一个
finite control orbit，并对 energy、coordinate diagonal 与 off-diagonal response 给出
exact mean/centered decomposition。锁定同一两个 held-out origins={28001,36001}、
scales={4096,8192}、四个 laws 与 V59 source-native residual；32 个 rows 形成
128 个 law-level decompositions。all-plus 的 control-average 与 centered-position
components 都是 32/32 positive，coherent mean 为 31/32 positive。这是 finite
position-response localization，不是 growing arithmetic theorem、fixed-power credit
或 full Gate B。

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

papers/tpc-331-control-average-centered-response-decomposition - TPC-331 已完成项目 -
五控制 orbit 的 exact mean/centered identity、128 条 decomposition 明细、independent
replay、stress、PDF 与 local Bridge-B checker。

papers/tpc-332-growing-control-average-ensemble - TPC-332 已完成项目 - 两 origin、三
scale 的 48-row control-average/centered replication、source polarization ledger、
independent replay、stress、PDF 与 local Bridge-B checker。

papers/tpc-333-source-polarization-cross-term - TPC-333 已完成项目 - 六窗口 source
cross-term coefficient ledger；near-orthogonality 与 near-total-cancellation 的
有限面板假设被 scoped refute，arithmetic advance 仍为 NO。

papers/tpc-334-cross-term-support-ledger - TPC-334 已完成项目 - 将 cross term 按
twin/non-twin/prime-power/zero support 精确分账；6/6 行显示 non-twin background
占主导，含 independent replay、stress、PDF 与 local Bridge-B checker。

papers/tpc-335-twin-isolated-source-norm - TPC-335 已完成项目 - 对四个 disjoint
support masks 完成 residual $L^2$ norm split；twin 占 9.56%--12.24%，含
independent replay、stress、PDF 与 local Bridge-B checker。

papers/tpc-337-control-covariance-masked-response - TPC-337 已完成项目 - 五-control
orbit 下四类 masked output 的 covariance Gram ledger；centered energy 占
78.50%--85.53%，并建立 signed covariance sign firewall。

papers/tpc-338-growing-control-covariance-spectrum - TPC-338 已完成项目 - 九-control
扩展保持 centered spectral energy，却在 twin/zero covariance 上出现 6/6 sign reversal，
否定 ensemble-invariant signed law。

papers/tpc-339-mask-aware-frobenius-envelope - TPC-339 已完成项目 - 216 条记录的
support-restricted Frobenius bound 全部通过，但 broad-mask occupancy 低于 0.2，说明
该 elementary envelope 不够 sharp。

papers/tpc-340-schur-frobenius-hybrid-envelope - TPC-340 已完成项目 - Schur/Frobenius
hybrid bound 216/216 无 violation，zero-support branch 获得有限改善，但 broad-mask
tightness 仍未解决。

papers/tpc-341-fresh-holdout-nuisance-orthogonalization - TPC-341 前一项目 - 三个
fresh windows 的样本内 nuisance 投影很强，但 27/27 leave-one-control-out 检验暴露
control-stability obstruction。

papers/tpc-342-independent-fresh-holdout-reproduction - TPC-342 已完成项目 - 在三个
完全 disjoint 的新窗口上独立复现 aggregate-versus-holdout split；样本内 retention
为 0.270--0.296，而 27/27 held-out retention 为 0.589--0.943。

papers/tpc-343-cross-panel-meta-certificate - TPC-343 已完成项目 - 两个独立 panel
的 row-block pooled retention 为 0.2325，但 shared coefficient retention 为
0.3198/0.3549；形成 scoped cross-panel stability obstruction。

papers/tpc-344-panel-contrast-nuisance-basis - TPC-344 已完成项目 - 预声明
panel-contrast basis 使 raw pooled retention 为 0.2962，但 equal-row 为 0.3187；
完成 exact span identity、18 个 holdout、4 个 cross-fit、independent replay、stress、
PDF 与 local Bridge-B checker，arithmetic advance 仍为 NO。

papers/tpc-345-principal-angle-grassmann-audit - TPC-345 已完成项目 - 对
TPC-341/TPC-342 两个 panel 完成 basis-invariant principal-angle、projector、
weighting-stability、mutual-transfer 与 18 个 leave-one-control-out 几何审计；
第一主角由 5.31° 移到 23.87°，panel-adaptive 路线的 finite freeze/no-go
测试因此成为下一步。

papers/tpc-346-third-panel-hostile-replication - TPC-346 已完成项目 - 在
TPC-341/TPC-342 之后加入 disjoint fresh third panel；324 raw records、261
nonempty records、18 个 fresh control-LOO 与 panel-transfer audit 全部可重放；
raw panel-adaptive crossing 为 0.299963，但 equal-row 为 0.322236，故冻结该
finite branch，arithmetic advance 仍为 NO。

papers/tpc-347-convolution-mask-defect-interface - TPC-347 已完成项目 - 将 literal
masked block 精确分解为 unmasked convolution 与 mask defect；192 条 finite rows、
96 个 translation checks、exact rational anchor、独立 replay、mutation stress、
PDF 与 local Bridge-B checker 均已封存；mask shortcut 为 scoped refuted，
arithmetic advance 仍为 NO。

papers/tpc-348-position-aware-mask-defect-lower-witness - TPC-348 已完成项目 - 对
TPC-347 defect 建立 exact position-aware coordinate lower witness；192/192 行有正
mask-hit witness，含 exact rational anchor、独立 reverse replay、mutation stress、
PDF 与 local Bridge-B checker；仅形成 finite scoped obstruction，arithmetic advance
仍为 NO。

papers/tpc-349-prime-balanced-signed-defect-witness - TPC-349 已完成项目 - 建立零和
prime-incidence Gram 与 signed lower witness；192/192 正响应、136/192 超过坐标
基线、175/192 达到 half-defect，含 exact multi-hit anchor、独立 reverse replay、
mutation stress、PDF 与 local Bridge-B checker；universal gain scoped refuted，
arithmetic advance 仍为 NO。

papers/tpc-350-fresh-growth-signed-incidence - TPC-350 已完成项目 - 在三个 fresh
origins、四个长度与四级 shell scale 上重放 zero-sum incidence witness；192/192
正响应，但 Q=256 的全部 rows 低于 half-defect，含 48-series growth ledger、exact
fresh anchor、reverse replay、mutation stress、PDF 与 local Bridge-B checker；
arithmetic advance 仍为 NO。

papers/tpc-351-reciprocal-shell-contrast - TPC-351 已完成项目 - 建立 exact rational
reciprocal-shell zero-sum contrast；同一 192-row panel 上 180/192 改善 TPC-350，
half-defect census 从 91 提升到 111，含 exact anchor、reverse-shell independent
replay、8-mutation stress、PDF 与 local Bridge-B checker；uniform quarter-floor 仍
scoped refuted，arithmetic advance 仍为 NO。

papers/tpc-352-reciprocal-shell-adversarial-holdout - TPC-352 已完成项目 - 在三个
disjoint origins 与新 shell ladder 上 hostile 重放 reciprocal contrast；144/144
正响应、118/144 改善 balanced parent，但 Q=256 floor 低于 parent，含 exact
holdout anchor、reverse replay、8-mutation stress、PDF 与 local Bridge-B checker；
uniform repair transfer scoped refuted，arithmetic advance 仍为 NO。

papers/tpc-353-source-native-masked-l2-polarization - TPC-353 已完成项目 - 将 V59
有限 residual 直接接入 literal divisibility-masked operator，给出 exact polarization
与 Cauchy envelope；216/216 rows 正 alignment，但 source/output coefficient 明显
不一致，含 exact anchor、independent reverse replay、mutation stress、PDF 与 local
Bridge-B checker；source-uniform arithmetic L2 仍为 OPEN，arithmetic advance 仍为 NO。

papers/tpc-354-higher-origin-masked-l2-holdout - TPC-354 已完成项目 - 将同一
source/operator attachment 移到 disjoint higher origins；216/216 rows 正 alignment，
但 all-plus floor/mean 相对 TPC-353 parent 分别下降 0.04215/0.02125，形成
`REFUTED_SCOPED` 的 uniform floor-transfer obstruction；含 exact anchor、独立
reverse replay、8-mutation stress、PDF 与 local Bridge-B checker，arithmetic advance
仍为 NO。

papers/tpc-355-position-aware-mask-energy-normalization - TPC-355 已完成项目 - 引入
response/source/sign-law-independent 的 unsigned mask-energy diagonal congruence；三
panels 共 648 rows，all-plus minimum drop 有限缓解 37.75%，但 mean repair 与
law-uniform alignment 均 scoped refuted；含 exact anchor、独立 reverse replay、10-
mutation stress、PDF 与 local Bridge-B checker，arithmetic advance 仍为 NO。

papers/tpc-356-geometry-adversarial-normalization-holdout - TPC-356 已完成项目 - 冻结
TPC-355 normalization，并用 51 候选的 geometry-only adversarial selection 选出三个
late origins；216 rows raw/normalized 均 216/216 positive，all-plus minimum/mean
分别获得 0.01906/0.00688 的有限 scoped gain；含 exact anchor、独立 reverse-shell
replay、10-mutation stress、PDF 与 local Bridge-B checker，uniform transfer 与
arithmetic advance 仍为 OPEN/NO。

papers/tpc-357-operator-norm-scale-ladder - TPC-357 已完成项目 - 在 TPC-356 锁定的
三个 geometry-adversarial origins 上把 count ladder 扩展到 256/512/1024/2048；四种
sign laws 共 288 rows，全部有 Schur/Frobenius envelope，all-plus 另有 72 rows 的真谱
范数重放。normalized Schur 最大值为 0.80778，all-plus normalized spectral 最大值
为 0.62665，raw 最大值为 1542.75；normalized spectral transition 为 15 增、35 降、
4 平，故 monotone-decay 仅在该有限梯子上 `REFUTED_SCOPED`；含 exact anchor、独立
reverse-shell replay、12-mutation stress、PDF 与 local Bridge-B checker，growing
operator bound 与 arithmetic advance 仍为 OPEN/NO。

papers/tpc-358-fresh-origin-spectral-holdout - TPC-358 已完成项目 - 将 TPC-357 的
finite operator-envelope protocol 移到预注册且 disjoint 的 fresh origins
`52001,120001,220001`（origin span `168000`）；288 rows 的 normalized Schur max 为
`0.80850510742101689`，all-plus normalized spectral max 为
`0.62663944469203836`，均落在 parent caps `0.83/0.64` 内且保持 `0.001` transfer
tolerance。normalized spectral ladder 仍有 `13/34/7` 增/降/平 transitions；含 exact
anchor、独立 reverse-shell replay、14-mutation stress、PDF 与 local Bridge-B checker，
origin-uniform/growing operator bound、source-uniform arithmetic L2 与 arithmetic
advance 仍为 OPEN/NO。

papers/tpc-359-geometry-adversarial-high-origin-holdout - TPC-359 已完成项目 - 在
全新高起点候选 `260001+211j`（51 个）上只用 unsigned geometry spread 做
response-blind adversarial selection，选出 `(267175,261267,269074)`；288 rows 的
normalized Schur/spectral maxima 为 `0.80834744529310265/0.6271657593674812`，均在
TPC-358 caps 内，raw spectral max 为 `1542.7354827195263`，但 transition 仍为
`12/36/6` 增/降/平。含 exact anchor、独立 reverse-shell replay、14-mutation stress、
PDF 与 local Bridge-B checker；growing operator bound、source-uniform arithmetic L2
与 arithmetic advance 仍为 OPEN/NO。

papers/tpc-360-schur-tightness-law-uniform-audit - TPC-360 已完成项目 - 在 TPC-359
锁定的三个 high-origin origins 上，将真谱范数扩展到四种 sign laws 与两档 counts，
共 144 rows。normalized spectral/Schur 最大 ratio 为 `0.77628391453148915`，
spectral/Frobenius 最大 ratio 为 `0.62110877254133434`；all-plus 在 36 个 setting
中赢 30 次，mod-4 赢 6 次。该 finite slack/law-uniform audit 不形成 growing
operator theorem；含 exact anchor、独立 reverse-shell replay、14-mutation stress、
PDF 与 local Bridge-B checker，arithmetic advance 仍为 NO。

papers/tpc-361-independent-high-origin-tightness-replication - TPC-361 已完成项目 - 在
全新 `310001+233j`（51 个）候选上只用六组 unsigned geometry spread 做
response-blind selection，选出 `(313030,311166,321651)`；288 rows、180 个真谱记录的
normalized Schur/spectral maxima 为 `0.80830232610282304/0.62690716242733457`，最大
spectral/Schur ratio 为 `0.77585950058997`。all-plus ladder 仍为 `12/36/6` 增/降/平，
含 exact anchor、独立 reverse-shell replay、15-mutation stress、PDF 与 local Bridge-B
checker；growing operator bound、source-uniform arithmetic L2 与 arithmetic advance
仍为 OPEN/NO。

papers/tpc-362-shell-scale-cap-obstruction - TPC-362 已完成项目 - 固定 TPC-361 的三个
high-origin origins，把 shell ladder 扩展到 `Q=12,24,36,54,80,128,256,512`，完成
384 个四-law spectral rows；旧 cap 在 `Q<=80` 保持（Schur/spectral max
`0.8083023261/0.6269071624`），但 `Q=128` 首次越界，全 ladder maxima 为
`1.7172665119/1.6398895499`，Schur/spectral violations 为 `33/30`。含 exact anchor、
独立 reverse-shell replay、15-mutation stress、PDF 与 local Bridge-B checker；这是
shell-scale 的 finite scoped obstruction，growing operator bound 与 arithmetic advance
仍为 OPEN/NO。

papers/tpc-363-bulk-persistence-localization - TPC-363 已完成项目 - 承接 TPC-362 的
`Q=128` 首次 cap failure，在同一 frozen high-origin panel 上审计 `Q=80,128,256`、
两档 counts、两种 exponent 与四种 sign laws，共 144 个真谱 rows；18 个 cap-violating
rows（Q=128 为 6、Q=256 为 12）全部为 all-plus，且在按 Schur row mass 或 principal
eigenvector mass 删除 `floor(N/20)` 行后仍越过 `0.64`，最小 retained spectrum 为
`0.86120283374232454`。这是 single-row/single-coordinate explanation 的 scoped
bulk obstruction，不是 universal renormalization theorem；含 exact anchor、独立
reverse-shell replay、16-mutation stress、PDF 与 local Bridge-B checker，growing
operator bound、source-uniform arithmetic L2 与 arithmetic advance 仍为 OPEN/NO。

papers/tpc-364-shell-tilt-phase-diagram - TPC-364 已完成项目 - 在同一 frozen panel
上对 `w_(p,beta)=(p/Q)^beta` 的五个整数 tilt、四种 sign laws、两档 counts 与
`Q=80,128,256,512` 完成 960 个真谱 rows；beta `-2,-1,0,1,2` 的 spectral-cap
violations 为 `63/36/30/30/0`，beta=2 的最大 normalized spectrum 为
`0.61628753962786131`，最小 shell-effective fraction 为 `0.66938300094026681`。
这是 reused panel 上的 finite modeling-choice phase diagram，beta=2 的 repair
必须由 disjoint holdout 验证；含 exact anchor、独立 reverse-shell replay、18-mutation
stress、PDF 与 local Bridge-B checker，growing operator bound、source-uniform arithmetic
L2 与 arithmetic advance 仍为 OPEN/NO。

papers/tpc-365-beta2-fresh-holdout - TPC-365 已完成项目 - 将 TPC-364 固定的 beta=2
规则先在 51 个候选起点的 unsigned geometry 上做 response-blind greedy selection，选出
`(413342,410258,416940)`，再在新 panel 的 384 个全法谱 rows 上与 beta=0 对照。beta=2
在 192/192 行低于 `0.64`，最大 normalized spectrum 为 `0.61633188509480319`，相对
TPC-364 最大值差 `4.4345466941875245e-05`；beta=0 有 30/192 个 violation。这是
geometry-selected finite transfer evidence，不是随机独立样本、source-valid normalization
或 asymptotic theorem；含 exact anchor、独立 reverse-shell replay、19-mutation stress、
PDF 与 local Bridge-B checker，growing operator bound、source-uniform arithmetic L2 与
arithmetic advance 仍为 OPEN/NO。

papers/tpc-366-beta2-higher-q-ladder - TPC-366 已完成项目 - 冻结 beta=2，在新
geometry-selected panel 上把 shell ladder 扩展到 `Q=512,1024,2048,4096,8192`，完成
480 个全法真谱 rows；beta=2 的 240/240 行低于 spectral `0.64` 与 Schur `0.83` caps，
最大 normalized spectrum/Schur 为 `0.6244828776/0.6536827829`，beta=0 对照各有
60/240 个 violation。这是有限 higher-Q scale audit，非 shell-uniform theorem、source-valid
normalization 或 arithmetic advance；含 exact anchor、独立 reverse-shell replay、23-mutation
stress、PDF 与 local Bridge-B checker，growing operator bound、source-uniform arithmetic
L2 与 arithmetic advance 仍为 OPEN/NO。

papers/tpc-367-predeclared-long-window-obstruction - TPC-367 已完成项目 - 去除
geometry-ranked origin selection，预声明 `(620001,626141,632281)` 三个等距 origins，
在 counts `512,1024` 与 `Q=512,2048,8192` 上完成 288 个全法真谱 rows。beta=2 在
count=512 全部通过 spectral cap，但 count=1024 在 `Q=2048,8192` 的 all-plus、exponent-1
行出现 6/144 个 spectral violations，Schur 为 0/144；beta=0 对照为 36/36。这是
有限长窗口 transfer 的 scoped obstruction，非 asymptotic theorem、source-valid normalization
或 arithmetic advance；含 exact anchor、独立 reverse-shell replay、28-mutation stress、PDF
与 local Bridge-B checker，growing operator bound、source-uniform arithmetic L2 与
arithmetic advance 仍为 OPEN/NO。

papers/tpc-368-predeclared-origin-replication - TPC-368 已完成项目 - 在第二个
predeclared origin family `810001+353j` 的 indices `(0,20,40)` 上复现 TPC-367 的
long-window phase，得到 `(810001,817061,824121)`；在 exponent=1、counts `512,1024`、
`Q=512,2048,8192` 与四种 sign laws 的 144 个全法真谱 rows 中，beta=2 再次出现
6 个 count=1024、高-Q、all-plus spectral violations，Schur 为 0/72，beta=0 对照为
18/18。这是第二 origin family 的 finite scoped replication，不是 origin/window uniformity
或 asymptotic theorem；含 exact anchor、独立 reverse-shell replay、29-mutation stress、
PDF 与 local Bridge-B checker，growing operator bound、source-uniform arithmetic L2 与
arithmetic advance 仍为 OPEN/NO。

papers/tpc-336-masked-signed-gram-response - TPC-336 前置项目 - 固定 signed-Gram
operator 的 6-row masked response ledger；zero/background/twin/prime-power gain
ordering 与 6/6 destructive interaction 已独立复现，arithmetic advance 仍为 NO。

TPC-330（上一位置）仍保留 affine-family placement obstruction，作为 TPC-331 的
直接 parent lock。

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

papers/tpc-330-multi-permutation-response-spectrum - TPC-330 previous project - 五个
coordinate controls 的 finite response spectrum、640 条明细、independent replay、
stress、PDF 与 local Bridge-B checker。

TPC-329（上一位置）仍保留 held-out growing source-native placement obstruction，作为
TPC-330 的直接 parent lock。

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

papers/tpc-329-heldout-growing-source-native-audit - TPC-329 previous project - held-out 两尺度 source-native 审计与置换 placement obstruction，含 32-row certificate、独立重放、stress、PDF 与 local Bridge-B checker。

TPC-328（更早位置）仍保留 source-native finite Gram cancellation/obstruction
atlas 及其 96-row certificate，作为 TPC-329 的祖先 lock。

papers/tpc-328-source-native-l2-cancellation - TPC-328 previous project；含 source-native
V59 residual、exact finite Gram decomposition、96-row four-law certificate、independent
replay、stress suite、PDF 与 local Bridge-B checker。

TPC-327（上一位置）承接 TPC-326，在第三个完全 disjoint 的 source origin
20001 重跑同一四档 N={320,640,1280,2560}，并把 12001、16001、20001
三个 origin 的 envelope 合并成 finite triangulation。保持 H=66、
Q={24,36,54,80}、s={1,2} 和四个 sign laws 不变；第三 origin 的 32 个 rows
all-plus normalized profile 在 32/32 行 majorizes direct profile，四种 profile/
energy census 同时匹配两个父面板。三-origin 最大 TV/energy range 分别为
0.000797...<0.001、0.004552...<0.005。这是 finite three-origin triangulation，
不是 uniform-in-source theorem、source-native arithmetic L2、fixed-power credit 或
full Gate B。

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

papers/tpc-327-three-origin-scale-triangulation - TPC-327 previous project；含第三
disjoint origin 的 32-row certificate、三-origin envelope range、independent replay、
residue stress、PDF 与 local Bridge-B checker。

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

papers/tpc-326-cross-origin-scale-replication - TPC-326 previous project；含第二
disjoint origin 的 32-row cross-origin certificate、independent reverse/einsum replay、
residue-perturbation stress、PDF 与 local Bridge-B checker。

TPC-325 是上一位置：承接 TPC-324 的 source-location holdout，在同一
literal deleted-diagonal centered prime-shell blocks 上冻结新 origin `12001`，
只改变嵌套 source cardinality `160,320,640,1280`。四个 scale rungs 与
`Q={24,36,54,80}`、`s={1,2}` 形成 32 rows；all-plus normalized profile 在
32/32 行 majorizes direct profile，且 outward lower TV envelope 与 outward upper
energy envelope 均沿四档严格下降。这个结果是 finite source-scale audit；它不提供
uniform growing theorem、source-native arithmetic L2、fixed-power credit 或 full
Gate B。

    TPC325_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT
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

papers/tpc-325-scale-ladder-profile - TPC-325 previous project；含固定 origin 的
四档 nested scale ladder、32-row profile certificate、independent reverse/einsum
replay、stress suite、PDF 与 local Bridge-B checker。

TPC-324 是上一位置：
literal deleted-diagonal centered prime-shell blocks 上做预注册的 source-location
holdout。两个与训练 union 完全 disjoint 的 source panels 共 48 rows；all-plus
profile 在 48/48 行 majorizes direct profile，且每个 panel 单独为 24/24。alternating、
mod-4、half-split 的 majorizing/mixed 计数为 34/14、42/6、36/12，复现了 parent
panel 的比例；all-plus energy ratio 仍为 6/48 below、42/48 above。这个结果是
finite source-location replication：conditional translation covariance 为
PROVED_EXACT_FINITE，但 source-native arithmetic L2、渐近 power saving、fixed-power
credit 与 full Gate B 仍 OPEN，不把 holdout 复现写成 arithmetic cancellation。

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

papers/tpc-324-source-profile-holdout - TPC-324 current project；含 exact conditional
translation covariance、双 source-location holdout、48-row profile certificate、
independent replay、stress suite、PDF 与 local Bridge-B checker。

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
    TPC323_ROUND2_CLUE = TEST_PROFILE_MAJORISATION_HOLDOUT_OR_SOURCE_NATIVE_ARITHMETIC_L2

papers/tpc-323-signed-profile-majorization - TPC-323 current project；含 exact
trace/profile factorisation、24-row signed-profile certificate、independent replay、
stress suite、PDF 与 local Bridge-B checker。

TPC-321 承接 TPC-320 的 trace-normalized spectral profile，在同一
literal deleted-diagonal centered prime-shell Gram 上把比较轴改为固定 X、s 下的相邻
prime-shell Q。X=640,1280,2560、Q={24,36,54,80}、s={1,2} 给出 24 行和 18 个
adjacent-Q comparisons；完整排序 profile 的 total-variation 与 cumulative
Lorenz/Ky Fan 距离在 18/18 上分别严格超过 0.03 与 0.02。majorization 标签为
3 个 forward、2 个 reverse、13 个 mixed，故统一 shell-monotone profile rule 在该
有限面板上被 refute，但不外推为渐近定理。

这是 NUMERICALLY_CERTIFIED_FINITE_CROSS_SHELL_PROFILE_SEPARATION_AUDIT，且
trace-normalized profile 的正标量不变性是 PROVED_EXACT_FINITE。它给出同一系统族的
shell-sensitivity obstruction，不是 arithmetic cancellation、渐近 power theorem 或
twin-prime result；fixed-power credit 为 0，full Gate B 仍 OPEN。Session-named
evaluator files absent，故不宣称 official Route-A/Route-B pass。

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
    TPC321_ROUND2_CLUE = TEST_SIGNED_PROJECTOR_REASSEMBLY_OR_PROVE_A_UNIFORM_SHELL_PROFILE_BOUND_BEFORE_ANY_ARITHMETIC_POWER_CLAIM

papers/tpc-322-signed-projector-reassembly - TPC-322 current project；含完整
operator-level signed projector identity、24-row exhaustive sign atlas、independent
replay、stress suite、PDF 与 local Bridge-B checker。

papers/tpc-321-cross-shell-profile-stability - TPC-321 current project；含完整
trace-normalized ordered-profile distance certificate、majorization obstruction、
independent reverse/einsum replay、metric stress suite、PDF 与 local Bridge-B checker。

当前主线状态：TPC-320 承接 TPC-319 的 normalization firewall，在完全相同的 literal
deleted-diagonal centered prime-shell Gram 上改用 trace-normalized spectral measure
\(C_k=F_k/\operatorname{tr}(G)\)。在
X=640,1280,2560、Q={24,36,54,80}、s={1,2} 的 24 行和
k={1,2,4,8,16} 五层簇大小上，120 个有限区间与 80 个相邻尺度比较全部通过；
trace-normalized top-k share 全部严格下降。stable rank 与 participation rank 在
16/16 transitions 上升，但只记作有限数值观察；normalized entropy 为 mixed control
(14 增、2 减)，因此不把单一指标扩张成全谱定理。

这是 NUMERICALLY_CERTIFIED_FINITE_TRACE_NORMALIZED_SPECTRAL_CONCENTRATION_AUDIT，
并且 positive-scalar invariance 是 PROVED_EXACT_FINITE。它是同一系统族中的
scale-invariant spectral-shape obstruction，不是 arithmetic cancellation、渐近
power theorem 或 twin-prime result；fixed-power credit 为 0，full Gate B 仍 OPEN。
Session-named evaluator files absent，故不宣称 official Route-A/Route-B pass。

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
    TPC320_ROUND2_CLUE = AUDIT_SPECTRAL_PROFILE_STABILITY_ACROSS_SHELLS_OR_TEST_SIGNED_PROJECTOR_REASSEMBLY_BEFORE_ANY_ARITHMETIC_POWER_CLAIM

papers/tpc-320-trace-normalized-spectral-concentration - TPC-320 current project；含
exact scale-invariance proof、trace-normalized concentration certificate、independent
full-spectrum replay、scalar/PSD/Weyl stress suite、PDF 与 local Bridge-B checker。

当前主线状态：TPC-319 承接 TPC-318，将最大特征值推广为 Ky Fan top-\(k\) 簇质量
\(F_k=\sum_{j\le k}\lambda_j\)，其中 \(k={1,2,4,8,16}\)。在同一
`X=640,1280,2560`、`Q={24,36,54,80}`、`s={1,2}` 的 24 行上，5 个簇大小共
80 个相邻尺度比较全部显示 normalized \(F_k/N\) 严格下降，同时 unnormalized
\(F_k\) 全部严格上升；精确的 factor-of-two normalization identity 解释了这个
方向翻转。gap/effective-rank census 还显示顶端谱簇并非统一的一维对象。

这是 `NUMERICALLY_CERTIFIED_FINITE_KY_FAN_CLUSTER_NORMALIZATION_AUDIT`，贡献是
有限的 cluster readout 与 normalization firewall，不是 arithmetic cancellation 或
渐近 power theorem。它没有支付 fixed-power credit、full Gate B 或 twin-prime endpoint；
Session-named evaluator files absent，故不宣称 official Route-A/Route-B pass。

`text
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
TPC319_ROUND2_CLUE = AUDIT_A_SCALE_INVARIANT_SPECTRAL_MEASURE_OR_PROVE_A_SOURCE_NORMALIZATION_LAW_BEFORE_ANY_POWER_CLAIM
`

papers/tpc-319-kyfan-cluster-normalization-firewall - TPC-319 current project；含
Ky Fan variational proof、dual finite cluster certificate、normalization flip firewall、
independent replay、stress suite、PDF 与 local Bridge-B checker。

当前主线状态：TPC-318 承接 TPC-317，直接读取同一 deleted-diagonal centered
prime-shell Gram 的最大特征值。固定 `X=640,1280,2560`、`Q={24,36,54,80}`、
`s={1,2}` 的 24 行上，双 shell 顺序、SciPy/NumPy 对称求解器和残差/Weyl guard
共同给出 finite top-eigenvalue audit；16 个相邻 normalized top-eigenvalue intervals
全部严格下降。另一方面，10/24 行的 top/second gap 小于 `0.01`，最小约为
`0.001704`，所以归一化有限趋势仍不能支付 unnormalized growing power 或 canonical
arithmetic eigenvector。

这是 `NUMERICALLY_CERTIFIED_FINITE_TOP_EIGENVALUE_AUDIT`，不是渐近定理。它没有
支付 arithmetic cancellation、fixed-power credit、full Gate B 或 twin-prime endpoint；
Session-named evaluator files absent，故不宣称 official Route-A/Route-B pass。

```text
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
TPC318_ROUND2_CLUE = AUDIT_THE_TOP_EIGENSPACE_CLUSTER_AND_NORMALIZATION_LAW_BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION
```

papers/tpc-318-top-eigenvalue-prime-shell-audit - TPC-318 current project；含 dual
top-spectrum certificate、independent replay、spectral stress、PDF 与 local Bridge-B checker。

当前主线状态：TPC-317 承接 TPC-316 的 Frobenius/operator-norm 分离，保留同一
deleted-diagonal centered prime-shell operator，并加入 PSD Gram 的 Schatten-4
trace-power envelope。对 X=640,1280,2560、Q={24,36,54,80}、s={1,2} 的 24 行，
16 个相邻尺度比较显示 normalized Schatten-4 envelope 全部严格下降，而同一
normalized Frobenius envelope 全部严格上升；小面板的 trace(G) 与 trace(G^2)
由 exact rational arithmetic 锚定。

这是 PROVED_EXACT_FINITE 的有限 trace-power/L2 chain，外加
NUMERICALLY_CERTIFIED_FINITE 的 24-row opposite-trend certificate；大面板数值不
等同于 true operator norm 的渐近衰减。它没有支付 growing arithmetic L2、fixed-power
credit、full Gate B 或 twin-prime endpoint；仍是同一锁定 engine，非 external physical
holdout。Session-named evaluator files absent，故不宣称 official Route-A/Route-B pass。

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
TPC317_ROUND2_CLUE = AUDIT_THE_TRUE_TOP_EIGENVALUE_OR_A_CERTIFIED_TRACE_POWER_LADDER_BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION

papers/tpc-317-schatten-four-prime-shell-compression - TPC-317 current project；含 finite
PSD trace-power chain、24-row Schatten-4/Frobenius opposite-trend certificate、exact
small rational anchor、independent replay、stress suite、PDF 与 local Bridge-B checker。

papers/tpc-316-literal-arithmetic-l2-fresh-panel - 上一项目；含 literal source-to-output
operator、exact difference/residue HS certificate、80 coordinate probes 与 two-scale
Frobenius obstruction。

papers/tpc-316-literal-arithmetic-l2-fresh-panel - TPC-316 previous project；含 literal
source-to-output operator、exact difference/residue HS certificate、80 coordinate probes、
independent replay、stress suite、PDF 与 local Bridge-B checker。

上一位置 TPC-315 已将 TPC-314 的三-law menu 在读取新目标前锁定，并把同一
literal engine 移到 fresh source interval `I=(640,1280]`。8 个 `(Q,s)` rows 的 Gram
minimum 与 all-positive maximum 均重新由 exact rational sign enumeration 计算；3 个 laws
与 2 个 targets 共 48 个 cases，24/24 minimum intervals 严格低于 1，24/24 positive
controls 严格高于 1。log(p) 由 120 项 rational atanh range reduction 与 geometric tail
outward-enclose，所有 weighted forms 在 `10^-36` grid 上由 independent checker 重放。

粗粒度 separation class 在 fresh panel 上 8/8 复现；细粒度幅度次序并不稳定：minimum
order 有 3 类（6/1/1），positive control 有 2 类（6/2）。这是 same-engine fresh-source
holdout 与 canonical-weight obstruction，不是 external physical independence、uniform
growing theorem、arithmetic `L2`、fixed-power credit、full Gate B 或 twin-prime proof；
Session-named evaluator files absent，故不宣称 official Route-A/Route-B pass。

TPC315_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_FRESH_SOURCE_LOCKED_WEIGHT_MENU_HOLDOUT_REPLICATION_AND_LAW_ORDER_SHIFT
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
TPC315_ROUND2_CLUE = PROBE_LITERAL_ARITHMETIC_L2_INTERFACE_ON_THE_FRESH_PANEL_BEFORE_ANY_GROWING_CLAIM

papers/tpc-315-fresh-source-locked-weight-holdout - TPC-315 current project；含 fresh-source
locked-menu certificate、exact target recomputation、independent replay、stress suite、PDF
与 local Bridge-B checker。

当前主线状态：TPC-314 在 TPC-312 的新 source-shell panel 上完成三种 externally
motivated positive weighting law 的有限审计：counting 1、reduced-residue 1/(p-1)、
prime von-Mangoldt log(p)。8 个 rows、3 个 laws、2 个 targets 共 48 cases；24/24
Gram-minimum intervals 严格低于 1，24/24 all-positive controls 严格高于 1。log(p)
由 120 项 rational atanh range reduction 与 geometric tail outward-enclose，并在
10^-36 grid 上由 independent checker 重放。幅度存在 law dependence：minimum order
有一次 counting/log crossover，positive control 有四种 strict order types。

这是 finite same-engine/source-first robustness audit，不是 canonical weighting theorem、
external physical holdout、uniform growing theorem、arithmetic L2、fixed-power credit、
full Gate B 或 twin-prime proof；Session-named evaluator files absent，故不宣称 official
Route-A/Route-B pass。

TPC314_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_EXTERNALLY_MOTIVATED_WEIGHT_LAW_ENCLOSURE_AND_NEW_PANEL_ROBUSTNESS_AUDIT
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

papers/tpc-314-canonical-weight-law-audit - TPC-314 current project；含
README、proof/theorem ledger、exact producer、independent checker、stress suite、
canonical JSON certificate、PDF 与 local Bridge-B checker。

当前主线状态：TPC-313 将 TPC-312 的新 source-shell panel 推进到正式的
profile-budget interface。对 `I=(320,640]`、`H=66`、`Q={24,36,54,80}` 与
exponent `{1,2}` 的 8 行，精确扫描 weighted Gram-minimum target 的 first-feasible
profile prefix；在同一 prefix 上构造 16 个 rational primal/dual witnesses，并用
`10^-36` outward decimal grid 重放。8/8 weighted dual lower ratios `>5e-5`，8/8
all-positive primal upper ratios `<1e-5`。这是有限 source-first certificate，不是
external physical holdout、uniform growing theorem、arithmetic `L2` 或 twin-prime proof。

```text
TPC313_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_PROFILE_PREFIX_FEASIBILITY_AND_OUTWARD_INTERVAL_BUDGET_CERTIFICATES_PLUS_NUMERICALLY_CERTIFIED_NEW_PANEL_SEPARATION
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

`papers/tpc-313-outward-budget-interval-certificate` - TPC-313 current project，包含
8 个 common-prefix scans、16 个 exact rational budget witnesses、outward interval
replay、independent checker、stress suite、proof package、PDF 与本地 Bridge-B checker。
Session-named evaluator files absent，故不宣称 official pass。

当前主线状态：TPC-312 将 Bridge-B 推进到一个新的 source-shell panel。固定同一 literal
physical engine 的新源区间 `I=(320,640]`、`H=66`、`Q={24,36,54,80}` 与 exponent
`{1,2}`，重新构造 8 个 rational physical Gram rows，不导入旧 atlas 的 sign labels。
84 个 shell targets、37,440 个 global-sign classes 均完成 exact replay；8/8 Gram 在
`1000000007` 下满秩，8/8 行的 sign minimum `<1` 而 all-positive maximum `>1`，且沿
每个 Q spine minimum 严格下降、positive maximum 严格上升。这里的“新”只指同一锁定引擎
内的新 source indices/parameter rows，不是外部独立物理样本；uniform growing theorem、
profile-budget outward rounding、arithmetic `L2`、full Gate B 与 twin-prime theorem 仍
OPEN/NONE。

```text
TPC312_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_NEW_SOURCE_SHELL_GRAM_AND_SIGN_SEPARATION_ATLAS
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

`papers/tpc-312-new-source-shell-separation-atlas` - TPC-312 current project，包含 8-row
new source-shell certificate、独立 exact replay、stress suite、proof package、PDF 与
local Bridge-B checker。Session-named evaluator files absent，故不宣称 official pass。

当前主线状态：TPC-311 承接 TPC-310，检验一个声明的两阶段 stratification rule 能否跨
tolerance slice 复现。固定 TPC-309/TPC-310 的 parent certificates，在每个
`(transition, exponent, tau, radius)` design cell 内先 pool `LOW/BASE/HIGH` 三个 profile
ladders，再给每个 design cell 等权。native `r=0` 的 calibration `tau={0.25,0.5}` 区间为
`[4.0615814676,4.0617439341]`、class `LEFT`；held-out `tau={0.75}` 区间为
`[0.6818442327,0.6818715070]`、class `RIGHT`，形成 strict finite reversal。将 `r=1,2`
纳入压力测试后 calibration 仍 `LEFT`，confirmation 变为 `UNRESOLVED`；删除 BASE 会改变
native calibration class，exponent 1/2 也给出不同方向。这是同一 locked parent 内的
parameter-slice obstruction，不是 fresh physical replication、externally timestamped
preregistration、causal、asymptotic、arithmetic 或 twin-prime theorem。

```text
TPC311_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_STRATIFIED_HOLDOUT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_TAU_SLICE_NONREPLICATION_ATLAS
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

`papers/tpc-311-stratified-tau-holdout-replication` - TPC-311 current project，包含
54-stratum certificate、独立 replay、exact stress suite、proof package、PDF 与本地
Bridge-B checker。Session-named evaluator files absent，故不宣称 official pass。

此前阶段状态：TPC-310 承接 TPC-309，审计 cross-holdout aggregation order 与 profile
robustness。固定 TPC-309 的 162 个 envelope observations，枚举三个 profile ladders 与
三个 completion radii 的全部非空子集，得到 49 个 selector、147 个 aggregate rows。
Pooled MSE 在全 selector 上给出 `RIGHT`，equal-case arithmetic ratio 给出 `LEFT`，
geometric ratio 给出 `RIGHT`；对应区间分别为
`[0.2423655855,0.3112477031]`、`[5.2417686281,14.4871333704]`、
`[0.1993188213,0.8609189559]`。这是远离阈值的 aggregation-order obstruction：不能
在未预注册 weighting/stratification law 的情况下宣称 profile-independent preference。
有限 selector、独立 completion extrema、positive interval maps 与 ratio-of-sums
weighted-mean identity 是 exact finite；parent float replay、directed rounding、causal
identification、uniform budget、arithmetic `L2`、fixed-power credit、full Gate B 与
twin-prime conclusion 仍 OPEN/NONE。

```text
TPC310_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_CROSS_HOLDOUT_AGGREGATION_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_AGGREGATION_ORDER_OBSTRUCTION_ATLAS
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

`papers/tpc-310-cross-holdout-aggregation-order` - TPC-310 previous project，包含
49-selector aggregation atlas、独立 replay、精确有理数 stress suite、proof package、
PDF 与本地 Bridge-B checker。Session-named evaluator files absent，故不宣称 official pass。

TPC-309 阶段状态：

当前主线状态：TPC-309 承接 TPC-308，检验 common-ambient holdout 对 source-profile prefix
选择的敏感性。在同一个 19-prime cutoff pool 中，使用相邻的 17-cutoff windows
`LOW/BASE/HIGH`，保持 shell、labels、alignment、exclusive completion protocol 不变，
但对每个 ladder 重新计算 feasible common prefix、frontier、budget 与 holdout envelope。
三种 ladder 共 54 个 profile cases、162 个 envelope observations，候选数跨 ladder 为
`108/558/1440`。BASE 在三个半径上精确恢复 TPC-308 的 `13/3/2`、`11/2/5`、
`10/1/7`；LOW/HIGH 把 strict discordance 移到更早 transition 或扩大 unresolved band，
说明该 finite obstruction 在声明的 profile shifts 下不具 location-invariance。这是
finite model-selection sensitivity obstruction，不是 causal、asymptotic、arithmetic 或
twin-prime theorem；formal directed-rounding enclosure、profile-independent preference、
uniform budget、arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion
仍 OPEN/NONE。

```text
TPC309_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_PROFILE_LADDER_SHIFT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_PROFILE_SENSITIVITY_ATLAS
TPC309_ROUTE_ADVANCE = YES_SCOPED_PROFILE_SENSITIVITY_OBSTRUCTION
TPC309_WINDOW_PROTOCOL = PROVED_EXACT_FINITE
TPC309_PREFIX_NESTING = PROVED_EXACT_FINITE
TPC309_HAMMING_EXTREMA = PROVED_EXACT_FINITE
TPC309_NORMALIZER_INVARIANCE = PROVED_EXACT_FINITE
TPC309_PROFILE_ATLAS = NUMERICALLY_REPRODUCED_FINITE_54_PROFILE_CASES_162_ENVELOPES
TPC309_BASELINE_RECOVERY = NUMERICALLY_REPRODUCED_FINITE_TPC308_CLASSES
TPC309_PROFILE_ROBUSTNESS = OPEN_PROFILE_INDEPENDENT_PREFERENCE
TPC309_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS
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

`papers/tpc-309-profile-prefix-shift-sensitivity` - TPC-309 current project，包含三窗口
profile sensitivity atlas、独立 replay、exact stress suite、proof package、PDF 与本地
Bridge-B checker。Session-named evaluator files absent，故不宣称 official pass。

此前 TPC-308：

当前主线状态：TPC-308 在 TPC-307 的 common-ambient holdout 上做 adversarial
exclusive-completion envelope。冻结 overlap fit、coefficients、profile prefix 与 budget
class，对每个 exclusive holdout 枚举 Hamming radii `r=0,1,2` 的全部 binary completions。
有限协议、候选计数、fixed-prediction extrema、radius monotonicity、radius-zero recovery
与 sign invariance 是 exact finite；18 个 parent cases 形成 54 个 envelope observations、
候选数 `36/186/480`。agreement census 为 `13/3/2`、`11/2/5`、`10/1/7`，分别对应
`r=0,1,2` 的 concordant/discordant/unresolved；discordance 从 `3→2→1` 衰减但在
`Q=70→90,e=1` 仍存留，且全部 final-pair localized。这是 completion stability/fragility
的 finite numerical replay，不是 causal、asymptotic、arithmetic 或 twin-prime theorem；
formal directed-rounding enclosure、uniform budget、arithmetic `L2`、fixed-power credit、
full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC308_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_HAMMING_COMPLETION_ENVELOPE_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_HOLDOUT_STABILITY_ATLAS
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

`papers/tpc-308-adversarial-exclusive-completion-envelope` - TPC-308 current project，
including independent replay, exact stress suite, proof package, PDF and local Bridge-B
checker. Session-named evaluator files are absent from this checkout; no official evaluator
pass is asserted.

上一阶段 TPC-307：

当前主线状态：TPC-307 在 TPC-306 的 interaction diagnostic 上构造了 common-ambient
union-shell holdout。对每个相邻 shell pair 使用同一个 `U` operator，在 overlap `O`
上分别拟合两种 aligned directional target，并把 `E_left,E_right` 作为 withheld
exclusive holdouts。协议中的 partition、holdout separation、global-sign invariance
与 common-prefix feasibility 是 exact finite；18 个 cases、36 个 directional fits、
54 个 normalizer rows 的 numerical replay 给出 `13 concordant / 3 discordant /
2 unresolved`，三处 discordance 全部定位在 `Q=70→90`、exponent 1 的三个 tolerance。
这是 finite completion-stability obstruction，不是 causal separation 或 asymptotic
theorem；formal directed-rounding enclosure、uniform budget、arithmetic `L2`、
fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC307_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_BUDGET_HOLDOUT_DISCORDANCE_ATLAS
TPC307_ROUTE_ADVANCE = YES_SCOPED_COMMON_AMBIENT_DIRECTIONAL_HOLDOUT_DIAGNOSTIC
TPC307_COMMON_AMBIENT_UNION = PROVED_EXACT_FINITE
TPC307_OVERLAP_ONLY_FIT = PROVED_EXACT_FINITE
TPC307_EXCLUSIVE_HOLDOUT = PROVED_EXACT_FINITE
TPC307_FINITE_HOLDOUT_ATLAS = NUMERICALLY_REPRODUCED_FINITE_18_CASES_36_DIRECTIONAL_FITS_54_NORMALIZER_ROWS
TPC307_AGREEMENT_CENSUS = NUMERICALLY_REPRODUCED_FINITE_CONCORDANT_13_DISCORDANT_3_UNRESOLVED_2
TPC307_BUDGET_PREFERENCE = NUMERICALLY_REPRODUCED_FINITE_RIGHT_13_LEFT_5_UNRESOLVED_0
TPC307_HOLDOUT_PREFERENCE = NUMERICALLY_REPRODUCED_FINITE_RIGHT_13_LEFT_3_UNRESOLVED_2
TPC307_DISCORDANCE_LOCALIZATION = NUMERICALLY_REPRODUCED_FINITE_ALL_3_AT_Q70_TO_90_EXPONENT_1
TPC307_TARGET_GENERATION_LEAKAGE = INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS
TPC307_CAUSAL_IDENTIFICATION = NONE_DIRECTIONAL_HOLDOUT_DIAGNOSTIC_ONLY
TPC307_FORMAL_INTERVAL_CERTIFICATE = OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING
TPC307_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
TPC307_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC307_FIXED_POWER_CREDIT = 0
TPC307_FULL_GATE_B = OPEN
TPC307_TWIN_PRIME_RESULT = NONE
TPC307_ROUND2_CLUE = STRESS_COMMON_AMBIENT_HOLDOUT_AGAINST_EXCLUSIVE_COMPLETION_ENVELOPES_AND_PROFILE_PREFIX_PERTURBATIONS_BEFORE_ANY_CAUSAL_PREFERENCE_CLAIM
```

`tpc-307-common-ambient-union-shell-holdout` - `PROVED_EXACT_FINITE_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_PROTOCOL_PLUS_NUMERICALLY_REPRODUCED_FINITE_BUDGET_HOLDOUT_DISCORDANCE_ATLAS` - common `U/O/E` holdout protocol，18 cases 中 `13/3/2` concordant/discordant/unresolved，三处 discordance 均在 `70→90,e=1`。

```text
TPC306_MAXIMUM_CLAIM = PROVED_EXACT_TWO_WAY_LOG_BUDGET_DECOMPOSITION_AND_DOMINANCE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_TARGET_INTERACTION_ATLAS
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

`tpc-306-two-way-operator-target-interaction` - `PROVED_EXACT_TWO_WAY_LOG_BUDGET_DECOMPOSITION_AND_DOMINANCE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_TARGET_INTERACTION_ATLAS` - 四格 log decomposition，有限 atlas 为 target-main `12/18`、interaction `6/18`，中心 `5/6`，same-prefix `3/3`。

此前 TPC-305 承接 TPC-304 的 overlap fracture，构造 full-shell
counterfactual transported target：在相邻 shell 的公共素数上使用最优 global-sign 对齐
标签，非公共素数保留 native label；随后在每个固定 physical operator 上，以 native
与 transported 两者的共同可行 profile prefix 重算 native budget。冻结
`(N,H,z)=(512,58,5)`、`Q=50,60,70,90`、两种 kernel exponent、三档 tolerance 与
三种 source normalization，共得到 18 个 target-swap cases、36 个 operator tables。
中心 `Q=60→70` 的 6 个 cases 中，right-neighbor label 在两侧 fixed operator 上均更便宜
的有 `5/6`，home-operator-favored 有 `1/6`；TPC-303 的 `3/3` same-prefix cases
全部落入 right-label-cheaper 类别。外侧 orientation 分别为 `(left=4,cross=2)` 与
`(left=3,cross=1,home=2)`。这是 finite partial counterfactual control，不是 causal
separation 或 asymptotic theorem；operator interaction、arithmetic `L2`、fixed-power
credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC305_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_COUNTERFACTUAL_TARGET_SWAP_PROTOCOL_PLUS_NUMERICALLY_CERTIFIED_FIXED_OPERATOR_TRANSPORTED_LABEL_BUDGET_ATLAS
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

`tpc-305-counterfactual-transported-label-budget` - `PROVED_EXACT_FINITE_COUNTERFACTUAL_TARGET_SWAP_PROTOCOL_PLUS_NUMERICALLY_CERTIFIED_FIXED_OPERATOR_TRANSPORTED_LABEL_BUDGET_ATLAS` - 固定 operator 的 18-case target-swap atlas，中心 transition 为 right-label-cheaper `5/6`，same-prefix `3/3`。

当前主线状态：TPC-304 承接 TPC-303 的 fixed-source cardinality obstruction，把相邻
moving prime shells 限制到公共素数上，先消除各自 source-first sign label 的 global-sign
gauge，再计算 overlap transport。六个 label-transport rows 的三组平均对齐相关度为
`1/2, 1/11, 1/2`（`Q=50→60, 60→70, 70→90`）；`Q=60→70` 是唯一的
`rho<=1/3` fracture。TPC-303 的 budget descent census 同步为 `3,15,3`，same-prefix
descent 为 `0,9,0`，因此全部 9 个 same-prefix descent 都落在中间 fracture。这个
结果是 finite localization crosswalk，不是因果分离或 asymptotic theorem；需要
counterfactual transported-label budget 才能区分 target switching 与 physical
operator change。arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。

```text
TPC304_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_GAUGE_INVARIANT_OVERLAP_CORRELATION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_LABEL_TRANSPORT_FRACTURE_AND_BUDGET_DESCENT_LOCALIZATION
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

`tpc-304-overlapping-shell-label-transport` - `PROVED_EXACT_FINITE_GAUGE_INVARIANT_OVERLAP_CORRELATION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_LABEL_TRANSPORT_FRACTURE_AND_BUDGET_DESCENT_LOCALIZATION` - 六个 overlap rows 的平均相关度为 `1/2,1/11,1/2`，中间 transition 同时承载 `15/18` budget descent 与全部 `9` 个 same-prefix descent。

当前主线状态：TPC-303 在 TPC-302 的 growing-shell budget-gap stability 之后，冻结
`(N,H,z)=(512,58,5)` 与 `Q=50,60,70,90` 的 moving-shell spine，直接测试“shell
cardinality 增大就迫使 native weighted budget 增大”的 shortcut。两种 kernel exponent、
三档 tolerance、三种 source normalization 共 54 个相邻 transition 中，区间严格认证
21 个 descent、33 个 ascent、0 个 unresolved；18/18 parameter series nonmonotone，
其中 9 个 descent 保持相同 common profile prefix，最强 same-prefix contraction 的
right/left ratio 小于 `0.284422`（总体最强小于 `0.224974`）。这是 declared finite
spine 上的 scoped obstruction，不是 asymptotic lower-bound refutation；uniform
profile-budget growth、arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。

```text
TPC303_MAXIMUM_CLAIM = PROVED_EXACT_INTERVAL_DESCENT_CRITERION_PLUS_NUMERICALLY_CERTIFIED_FIXED_SOURCE_CARDINALITY_MONOTONICITY_OBSTRUCTION
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

`tpc-303-cardinality-monotonicity-obstruction` - `PROVED_EXACT_INTERVAL_DESCENT_CRITERION_PLUS_NUMERICALLY_CERTIFIED_FIXED_SOURCE_CARDINALITY_MONOTONICITY_OBSTRUCTION` - 固定 source spine 的 54 个相邻 transition 中 21 descent、33 ascent、0 unresolved，9 个为 same-prefix descent。

TPC-302 将 TPC-301 的 tolerance/common-prefix/source-normalization
hostile audit 扩展到 TPC-288 的 34-row growing/control grid，并对每行从物理 Gram
source-first 重编 weighted sign target。`tau=1/4,1/2,3/4` 的 common-prefix gap
最小值为 `85.3204`、`38.2187`、`39.2637`，34/34 rows 在三档容差均超过 10；102
个 row-tolerance cases 在三种 source normalization 下的 weighted budget 均超过
`1e-5`。显式 shell target 数为 430；父级 inherited grid count 1,380 单独记录。
这是 finite growing-grid stability certificate，uniform profile-budget growth、
arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC302_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_SOURCE_FIRST_SIGN_ENUMERATION_AND_BUDGET_MONOTONICITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_GRID_AUDIT
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

`tpc-302-growing-shell-budget-gap-audit` - `PROVED_EXACT_FINITE_SOURCE_FIRST_SIGN_ENUMERATION_AND_BUDGET_MONOTONICITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_GRID_AUDIT` - 34-row source-first growing/control grid，三档容差 common gap 34/34 超过 10，102/102 budget floors per normalization 超过 `1e-5`。

```text
TPC301_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_TOLERANCE_MONOTONICITY_AND_HOMOGENEITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_GAP_ROBUSTNESS_ATLAS
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

`tpc-301-budget-gap-robustness-audit` - `PROVED_EXACT_FINITE_TOLERANCE_MONOTONICITY_AND_HOMOGENEITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_GAP_ROBUSTNESS_ATLAS` - 三档容差、共同 source prefix 与三种归一化下，weighted/positive gap 在 18/18 rows 均超过 10；weighted budget floor 54/54 超过 `3e-5`。

此前 TPC-300 承接 TPC-299 的 native budget frontier，把 primal budget obstacle
进一步编译成可独立核验的 target-space dual certificate。对有限 source Gram `M`、physical
image `V`、radius `R` 和任意正 ridge parameter `rho`，严格证明
`D_rho=(||b||^2-R^2-b^T V c_rho)/rho <= B_R(b)`，active frontier 上取等号，并校正
KKT multiplier 与 ridge parameter 的 reciprocal 关系 `mu=1/rho`。72 个 exact rational
dual witnesses 在继承的 18-row、1,380-edge grid 上通过 source-first replay；最小
dual/primal lower-bound ratio 约为 `0.9999999999999623`，weighted threshold 的
`18/15/14` 与 full-prefix `11` 个 `1e-3` obstruction 全部保留。该进展仍是 finite
restricted structural certificate；profile-budget growth、arithmetic `L2`、fixed-power
credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
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
```

`tpc-300-native-budget-dual-certificate` - `PROVED_EXACT_FINITE_NATIVE_BUDGET_DUALITY_AND_RECIPROCAL_MULTIPLIER_CORRECTION_PLUS_NUMERICALLY_CERTIFIED_FINITE_RATIONAL_DUAL_WITNESS_ATLAS` - 72 个 exact rational dual cases 全部通过；对偶下界紧度、参数 reciprocal correction 与 weighted budget obstruction 均被锁定。

此前 TPC-299 承接 TPC-298 的 profile-angle/dimension ladder，把“达到目标需要
多少个方向”进一步编译成“实际 native source 向量需要多少预算”。对 literal prefix
`U_k`、物理像 `V_k=A^T U_k` 与 source Gram `M_k=U_k^T U_k`，严格证明
quadratically constrained least-norm frontier 的 KKT/ridge 表达、预算可行性 iff 判据与
nested-prefix budget monotonicity。70 位 producer 与独立 source-first replay 在同一
18-row、1,380-edge grid 上显示：normalized RMS `1/2` 时 weighted target 的 threshold
budget 在 18/18 行超过 `9e-5||beta||^2`，15/18 超过 `5e-4`，14/18 超过 `1e-3`；
即便使用完整 17-profile prefix，仍有 11/18 行超过 `1e-3`。all-positive control 在
18/18 行低于 `1e-4`，weighted/positive threshold-budget gap 在 18/18 行超过 20。
这是 restricted finite native-budget obstruction；growing budget theorem、arithmetic
`L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```
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
```

`tpc-299-native-profile-budget-frontier` - `PROVED_EXACT_FINITE_PROFILE_BUDGET_KKT_FRONTIER_PLUS_NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_OBSTRUCTION_ATLAS` - KKT budget frontier exact；weighted half-RMS budget 在 14/18 个 threshold rows、11/18 个 full-prefix rows 超过 `1e-3`，positive control 18/18 低于 `1e-4`，gap 18/18 超过 20。

当前主线状态：TPC-298 承接 TPC-297，把四个 literal cutoff profiles 扩展为按 cutoff
排序的 17-profile prefix ladder
`Z=(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61)`。严格证明每个受限
source image 的 principal-angle identity 与 nested-prefix monotonicity；双模 replay 在
继承的 18-row、1,380-edge grid 上完成 306 个前缀秩检查。70 位独立 replay 显示 weighted
target 达到 normalized RMS `1/2` 至少需要 shell dimension 的 `2/3`（18/18），
all-positive control 至多需要 6 个 profiles（18/18），最后一个有限 prefix 在 18/18
行达到有限 target 空间。这个结果是 dimension/angle obstruction 的有限审计；growing
profile theorem、conditioning/source-budget growth、arithmetic `L2`、fixed-power
credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
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
```

`tpc-298-profile-angle-dimension-ladder` - `PROVED_EXACT_FINITE_PRINCIPAL_ANGLE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_PROFILE_DIMENSION_LADDER` - 17 个 literal cutoff 前缀的 306 项秩阶梯全部通过双模检查；weighted target 的 half-RMS 维度比例在 18/18 行至少为 `2/3`，all-positive 在 18/18 行不超过 6。

当前主线状态：TPC-297 承接 TPC-296 的 native-ray obstruction，把冻结一维 ray 扩展为
四个真实 Möbius/Euler cutoff profiles `beta_z`（`z=3,5,7,11`）。严格证明受限 source
correlation image 的正交投影公式与加方向单调性；两模 rank replay 在继承的 18-row grid
上得到 3-prime shell 为 rank 3、其余 17 行为 rank 4。70 位 replay 显示 all-positive
target 的 profile RMS 在 18/18 行不超过 `0.15`，但 weighted target 在 17/17 个大 shell
上仍不低于 `0.6`。因此四维 native-profile span 已有明确正信息，但 weighted direction
仍被 profile geometry 卡住；growing dimension、principal angle、arithmetic `L2`、
fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC297_PROJECTION_IDENTITY = PROVED_EXACT_FINITE
TPC297_NESTED_PROFILE_MONOTONICITY = PROVED_EXACT_FINITE
TPC297_TWO_MODULUS_IMAGE_RANK = NUMERICALLY_CERTIFIED_FINITE_3_PLUS_4
TPC297_WEIGHTED_PROFILE_SEPARATION = NUMERICAL_OBSERVATION_17_OF_17_AT_LEAST_0_6
TPC297_ALL_POSITIVE_PROFILE_CAPTURE = NUMERICAL_OBSERVATION_18_OF_18_AT_MOST_0_15
TPC297_GROWING_PROFILE_DIMENSION = OPEN
TPC297_PRINCIPAL_ANGLE_THEOREM = OPEN
TPC297_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC297_FIXED_POWER_CREDIT = 0
TPC297_FULL_GATE_B = OPEN
TPC297_TWIN_PRIME_RESULT = NONE
```

`tpc-297-literal-source-profile-span-audit` - `PROVED_EXACT_FINITE_RESTRICTED_PROFILE_PROJECTION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_FOUR_CUTOFF_PROFILE_ATLAS` - 四个 literal cutoff source profiles 形成 3/4 维受限像；all-positive 18/18 行被捕获到 RMS `0.15` 内，而 weighted target 在 17 个大 shell 上保留 RMS `0.6` obstruction。

当前主线状态：TPC-296 承接 TPC-295 的 unrestricted finite source-image 结果，继续量化
source-side least-norm budget 与 native-profile 几何。对 physical column matrix `A`、
`G=A^T A`，严格证明
`S_A(b)=min_{A^T h=b}||h||_2^2=b^T G^(-1)b`、预算可行性的 iff 判据，以及
`S_A(b)(b^TGb)>=(b^Tb)^2` 的 source/physical-energy tradeoff。70 位高精度独立 replay
在同一 18-row literal grid、1,380 edges 上显示：weighted minimizer、max-cut 与
all-positive targets 的 unrestricted budget ratio 均在声明的 `1e-3` 阈值内（18/18）；
但 weighted minimizer 与 max-cut 到冻结一维 ray `span{A^T beta}` 的 RMS 距离分别在
18/18 行至少为 `0.9`。因此当前有限坑不再是 ambient source norm，而是 native profile
的维数、像与 growing-shell budget；arithmetic `L2`、fixed-power credit、full Gate B
与 twin-prime conclusion 仍 OPEN/NONE。

```text
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
```

当前主线状态：TPC-295 承接 TPC-294 的 magnitude-weighted signed Rayleigh atlas，检查
ambient weighted minimizer 是否落在一个明确的 source-correlation image 中。令物理 shell
vectors 为 rational matrix `A` 的 columns，严格证明 `G=A^T A` 非奇异时
`A^T:Q^I -> Q^S` surjective，且显式 witness 为 `h=A G^(-1)b`；同时证明该 witness
是实数解中的 least-norm solution。对继承的 18-row literal grid，用两个独立模数
`1000000007`、`998244353` 完成 18/18 full-rank certificates，1,380 edges 上
18/18 unrestricted source images surjective，TPC-294 weighted minimizers、unit-edge
max-cut targets 与 all-positive targets 均 18/18 可达。这里的 source space 是明确声明的
unrestricted finite `Q^I`；native Mobius/comparison profile、witness norm growth、literal
arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
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
```

当前主线状态：TPC-294 承接 TPC-293 的 whole-shell signed max-cut，把真实 Gram magnitudes
恢复到 equal-sign quadratic objective。严格证明 trace-normalized identity、Gram
nonnegativity 与 common-denominator exhaustive sign optimization；同一 18-row literal
grid 的 1,380 edges 上，18/18 个 global weighted minima 都小于 1，18/18 个 all-positive
quotients 都大于 1，且 18/18 个 weighted optima 都不同于 unit-edge max-cut。13/18 个
minimum 不超过 `1/4`，8/18 不超过 `1/10`；最强 finite minimum 约为 `0.0496374497659`。
这确认 sign compatibility 与 physical energy compatibility 是两个不同层；source-native
coefficient image、growing weighted theorem、literal arithmetic `L2`、fixed-power credit、
full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
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
```

当前主线状态：TPC-293 把 TPC-292 的 triangle parity obstruction 提升到 whole-shell
signed complete graph。严格证明 all-positive `K_m` 的 favorable-edge maximum 是
`floor(m^2/4)`，并证明 finite signed frustration complement 与 switching invariance。
同一 18-row literal grid 的 1,380 个 Gram edges 上，17/18 rows 完全 all-positive；唯一
`(256,38,27,5,1)` crossover row 的 3 个 negative edges 把 signed maximum 从 12 提到
15。总计 max favorable 为 744、minimum unsatisfied 为 636、sign-only gain 仅 `+3`。
这把主要坑定位为 shell-level compatibility，并明确下一关必须恢复 Gram magnitudes；
growing signed theorem、magnitude-weighted Rayleigh、literal arithmetic `L2`、fixed-power
credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC293_ALL_POSITIVE_MAXCUT = PROVED_EXACT_CONDITIONAL
TPC293_SIGNED_OBJECTIVE = PROVED_EXACT_FINITE
TPC293_SWITCHING_INVARIANCE = PROVED_EXACT_FINITE
TPC293_SIGNED_MAXCUT_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC293_EDGE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_1380_EDGES
TPC293_MAX_FAVORABLE = NUMERICALLY_CERTIFIED_FINITE_744
TPC293_MINIMUM_UNSATISFIED = NUMERICALLY_CERTIFIED_FINITE_636
TPC293_EXCEPTIONAL_GAIN = NUMERICALLY_CERTIFIED_FINITE_PLUS_3_EDGES_ONE_ROW
TPC293_MAGNITUDE_WEIGHTED_RAYLEIGH = OPEN
TPC293_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE
TPC293_FIXED_POWER_CREDIT = 0
TPC293_FULL_GATE_B = OPEN
TPC293_TWIN_PRIME_RESULT = NONE
```

当前主线状态：TPC-292 承接 TPC-291 的 pairwise Schur cancellation，把问题推进到三素数
兼容性。对三个非零 Gram edges，严格证明 coefficient signs 能让三个 pair contributions
同时非正，当且仅当 edge-sign product 为 `-1`；product 为 `+1` 的三角形是 exact
sign-frustration。对三向量还严格证明 Schur projection residual
`det(G)/(d_i det(G_(j,k)))`。在同一 18-row literal grid 的 5,727 个 prime triples 上，
exact-rational certificate 得到 5,718 个 frustrated、9 个 anti-alignable，且 5,727 个
normalized volumes 全为正；late row 的 680 个 triples 全为 `+++`。这把 pairwise
cancellation 的主要障碍明确定位为 cycle compatibility，但 growing-shell compatibility、
literal arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍
OPEN/NONE。

```text
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
```

当前主线状态：TPC-291 承接 TPC-290 的 adaptive weighted-Gram firewall，把“相干是否
真的能抵消”精确化为两素数向量的 Schur projection。对任意非零 component pair，严格
证明最小归一化残差 `1-Gamma` 与 signed two-vector Rayleigh minimum `1-sqrt(Gamma)`，
并由 Gram 符号判定最优方向需要 opposite-sign 还是 same-sign coefficients。在同一
18-row grid 的 1,380 个 unordered pairs 上，exact-rational certificate 得到 1,377 个
positive、3 个 negative、0 个 zero cross terms；残差不超过 `1/2`、`1/4`、`1/10` 的
pair 数分别为 1,074、852、477，全球最强 pair `(173,179)` 的 residual 约为
`0.0151239493`。这确认了 pairwise signed cancellation mechanism，但 multi-prime
reassembly、literal arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。

```text
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
```

当前主线状态：TPC-289 承接 TPC-288 的 source-output Gram obstruction，在不改变
literal physical deleted-diagonal operator 的前提下，研究跨素数 Gram 交叉项的符号与
归一化相干。18 个 growth/exponent/control rows 共 1,380 个 unordered pair comparisons：
17/18 rows 的全部 cross terms 为正，但 `(N,H,Q,z,s)=(256,38,27,5,1)` 有 3 个精确
负 pair，其中 `(31,53)` 的 squared coherence 约 `1.3746e-7`；另一方面 8 个 late-shell
rows 满足 `Gamma>=9/25`、`d_min/d_max>=4/5` 的有限 strong block，且 18/18 rows
的 aggregate energy ratio 都大于 1。TPC-289 严格证明 Gram PSD、`0<=Gamma<=1` 与
conditional accumulation lower bound；这把“晚期相干模式”与“早期 sign-flip 坑”分开，
但 growing-shell/source-restricted coherence、arithmetic `L2`、fixed-power credit、
full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC289_EXACT_GRAM_COHERENCE = PROVED_EXACT_FINITE
TPC289_EXACT_ACCUMULATION_BOUND = PROVED_EXACT_CONDITIONAL
TPC289_PAIRWISE_POSITIVITY = NUMERICALLY_CERTIFIED_FINITE_17_OF_18_ROWS
TPC289_SIGN_FLIP_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_3_PAIRS_ONE_ROW
TPC289_STRONG_COHERENCE_BLOCK = NUMERICALLY_CERTIFIED_FINITE_8_ROWS
TPC289_ENERGY_AMPLIFIED = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ROWS
TPC289_GROWING_COHERENCE_STABILITY = OPEN
TPC289_SOURCE_CONTROL_UNIFORMITY = OPEN
TPC289_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC289_FIXED_POWER_CREDIT = 0
TPC289_FULL_GATE_B = OPEN
TPC289_TWIN_PRIME_RESULT = NONE
```

当前主线状态：TPC-290 承接 TPC-289 的 coherence phase diagram，把 adaptive weighting
写成加权 physical Gram quotient `R(w)=||sum_q w_q g_q||^2/sum_q w_q^2 d_q`。它严格证明
非负权重在全正 cross-Gram block 中不能产生 `R(w)<1`，并在 coherence floor 与 diagonal
balance 下证明 effective-support lower bound `R(w)>=1+eta*delta*(kappa(w)-1)`。在同一
18-row grid 上，uniform、inverse-diagonal、linear-taper 三种 full-support policies 共
54/54 amplified，18/18 leave-one-out minima 仍 amplified；恰有 3 个 equal-pair subunit
witness，全部来自早期 sign-flip row。这把“adaptive”细分为 diffuse positive branch 与
sparse sign-flip escape，但 growing weighted theorem、literal arithmetic `L2`、fixed-power
credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
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
```

当前主线状态：TPC-288 沿着 TPC-287 的 growing-shell clue，把同一个 literal
physical deleted-diagonal operator 的每个 prime component 保留为完整输出向量，构造
source-output Gram matrix，并在 34 个 scale/shell/control rows 上做 full-rank audit。
Gram 的 PSD、trace/all-ones energy identity 与 finite shell additivity 均严格证明；
34/34 个 output Gram 通过模 `1000000007` 的 full-rank witness，6 个 selected aggregate
physical active matrices 也 full rank。所有 34 行的 vector energy ratio
`||g_shell||^2/sum_q||g_q||^2>1`，其中 13 行同时有 interval-certified scalar retention
upper `<1/10`。这是一个明确的 scalar-to-energy obstruction：小 attachment 不能直接
兑换 physical `L2` saving；growing-shell theorem、source-native Gram bound、arithmetic
`L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC288_GRAM_IDENTITY = PROVED_EXACT_FINITE
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
```

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
tpc-294-magnitude-weighted-signed-rayleigh-atlas - 当前阶段 - 严格证明 trace-normalized
signed quadratic identity、Gram nonnegativity 与 finite global sign optimization；18 rows /
1,380 edges 完成 exact weighted atlas，18/18 weighted minima `<1`、18/18 all-positive
quotients `>1`、18/18 weighted optima 与 unit-edge max-cut 不同，13/18 `<=1/4`、8/18
`<=1/10`；source-native image、literal `L2`、full Gate B 仍 OPEN，fixed-power credit 为 0。
tpc-293-signed-shell-maxcut-atlas - 当前阶段 - 严格证明 all-positive complete-graph
max-cut、signed frustration complement 与 switching invariance；18 rows / 1,380 edges
完成 whole-shell exact-rational atlas（744 favorable、636 unsatisfied），17/18 rows 与
all-positive benchmark 相同，唯一 crossover row 有 `+3` sign-only gain；magnitude-weighted
Rayleigh、literal `L2`、full Gate B 仍 OPEN，fixed-power credit 为 0。
tpc-292-three-prime-sign-frustration-atlas - 当前阶段 - 严格证明 triangle sign parity
criterion、three-vector Schur residual 与 normalized Gram-volume identity；18 rows / 5,727
triples 完成 5,718 sign-frustrated、9 anti-alignable、5,727 positive-volume 的
exact-rational atlas；growing signed compatibility、literal `L2`、full Gate B 仍 OPEN，
fixed-power credit 为 0。
tpc-291-signed-schur-cancellation-atlas - 当前阶段 - 严格证明 two-prime Schur projection
identity、signed Rayleigh minimum 与 coefficient sign rule；18 个 rows / 1,380 个 pairs
完成 coherence-to-cancellation atlas（1,377 opposite-sign、3 same-sign，残差阈值
`1/2,1/4,1/10` 为 `1074/852/477`）；multi-prime reassembly、literal `L2`、full Gate B
仍 OPEN，fixed-power credit 为 0。
tpc-290-adaptive-shell-weighting-obstruction - 当前阶段 - 严格证明 weighted Gram identity、
nonnegative coherence wall 与 effective-support accumulation bound；同一 18-row grid 的
54/54 full-support policies 和 18/18 leave-one-out minima 均 amplified，仅早期 sign-flip
row 的 3 个 equal-pair supports subunit；growing weighted theorem、literal `L2`、full Gate B
仍 OPEN，fixed-power credit 为 0。
tpc-289-cross-prime-gram-coherence - 当前阶段 - 严格证明 normalized Gram coherence
的 Cauchy bound 与 conditional accumulation envelope；18 个 rows / 1,380 个 pair
comparisons 中 17/18 rows pairwise positive，早期 crossover 有 3 个 negative pairs，
8 个 late-shell rows 通过 `eta=3/5, delta=4/5` finite strong block，18/18 rows
energy ratio `>1`；uniform growing-shell coherence、literal `L2`、full Gate B 仍 OPEN，
fixed-power credit 为 0。
tpc-288-growing-shell-gram-obstruction - 当前阶段 - 严格证明 finite operator/output/attachment
additivity、Gram PSD 与 energy identity；在 34 个 growth/control rows 上认证 34/34
output Gram full rank、6/6 selected physical active matrices full rank，并发现 13 行
scalar retention upper `<1/10` 但 vector energy ratio `>1` 的 obstruction；uniform
growing-shell Gram bound、literal `L2`、full Gate B 仍 OPEN，fixed-power credit 为 0。
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
