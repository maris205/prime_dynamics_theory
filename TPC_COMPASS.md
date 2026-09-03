# TPC distilled map and bold channel

## V217 / TPC-364 current anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc364_shell_tilt_phase_diagram.md，checker 为
tpc_bridge_b_tpc364_shell_tilt_phase_diagram_checker.py，编号论文为
papers/tpc-364-shell-tilt-phase-diagram/。

TPC-364 承接 TPC-363 的 finite bulk-persistence obstruction，在同一 frozen high-origin
panel 上对显式 shell tilt `w_(p,beta)=(p/Q)^beta` 做完整 phase diagram。协议包含
`beta=-2,-1,0,1,2`、四种 sign laws、counts `256,512`、`Q=80,128,256,512` 与
exponents `1,2`，共 `960` 个全真谱 rows。五个 beta 的 spectral-cap violations
分别为 `63/36/30/30/0`；beta=2 的最大 normalized spectrum 为
`0.61628753962786131`，最大 normalized Schur 为 `0.64531400360759594`，最小
shell-effective fraction 为 `0.66938300094026681`。

这是 reused panel 上的 finite modeling-choice phase diagram：beta=2 的 cap repair
尚不是 holdout transfer、source-valid normalization 或 asymptotic theorem。它不产生
growing operator bound、source-uniform arithmetic `L2`、fixed-power credit、Route-B
reassembly 或 twin-prime result；arithmetic advance 为 NO。official evaluator files
仍 absent，local Bridge-B 仍 fail-closed。下一步是 response-blind disjoint holdout。

    TPC364_WEIGHTED_BLOCK_DEFINITION = PROVED_EXACT_FINITE
    TPC364_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
    TPC364_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_960_ROWS
    TPC364_PHASE_DIAGRAM = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC364_BETA2_PANEL_CAP_REPAIR = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC364_BETA2_ASYMPTOTIC_REPAIR = OPEN
    TPC364_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
    TPC364_GROWING_OPERATOR_BOUND = OPEN
    TPC364_SOURCE_UNIFORM_L2 = OPEN
    TPC364_ARITHMETIC_ADVANCE = NO
    TPC364_FIXED_POWER_CREDIT = 0
    TPC364_FULL_GATE_B = OPEN
    TPC364_TWIN_PRIME_RESULT = NONE
    TPC364_STATUS = NUMERICALLY_CERTIFIED_FINITE_SHELL_TILT_PHASE_DIAGRAM
    TPC364_ROUND2_CLUE = TEST_BETA2_ON_RESPONSE_BLIND_FRESH_HOLDOUT

## V216 / TPC-363 previous anchor

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc363_bulk_persistence_localization.md，checker 为
tpc_bridge_b_tpc363_bulk_persistence_localization_checker.py，编号论文为
papers/tpc-363-bulk-persistence-localization/。

TPC-363 承接 TPC-362 在 `Q=128` 的首个 finite spectral-cap failure，固定同一组
high-origin origins `(313030,311166,321651)`，并在 `Q=80,128,256`、counts `256,512`、
exponents `1,2` 与四种 sign laws 上完成 `144` 个全真谱 rows。`Q=80` 控制没有
`0.64` cap violation；`Q=128` 有 6 个、`Q=256` 有 12 个 violation，18 个全部为
all-plus。对每行分别删除按 normalized Schur row mass 与 principal-eigenvector
coordinate mass 选出的 `floor(N/20)` 个坐标，并重算 principal-submatrix spectrum；
18/18 个 failing rows 在两种删减下均保留越界，全部 failure 的最小 retained spectrum
为 `0.86120283374232454`，Q=128 子集最小为 `1.1843597700033823`。

这是 finite bulk-persistence obstruction：它只 refute 声明删减范围内的
single-row/single-coordinate explanation，不产生 universal renormalization、growing
operator theorem、source-uniform arithmetic `L2`、fixed-power credit、Route-B
reassembly 或 twin-prime result。arithmetic advance 为 NO；official evaluator files
absent，local Bridge-B 仍 fail-closed。

    TPC363_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_BULK_PERSISTENCE_OBSTRUCTION
    TPC363_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
    TPC363_FINITE_ENVELOPE_INEQUALITIES = PROVED_EXACT_FINITE
    TPC363_FIRST_Q128_FAILURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC363_BULK_PERSISTENCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC363_SINGLE_ROW_SPIKE_EXPLANATION = REFUTED_SCOPED_ON_DECLARED_TRIMS
    TPC363_EIGENVECTOR_DELOCALIZATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC363_RENORMALIZED_REPAIR = OPEN
    TPC363_GROWING_OPERATOR_BOUND = OPEN
    TPC363_SOURCE_UNIFORM_L2 = OPEN
    TPC363_ARITHMETIC_ADVANCE = NO
    TPC363_FIXED_POWER_CREDIT = 0
    TPC363_FULL_GATE_B = OPEN
    TPC363_TWIN_PRIME_RESULT = NONE
    TPC363_STATUS = NUMERICALLY_CERTIFIED_FINITE_BULK_PERSISTENCE_OBSTRUCTION
    TPC363_ROUND2_CLUE = TEST_RENORMALIZED_HIGH_Q_REPAIR_ON_EXPLICIT_HOLDOUT

## V215 / TPC-362 previous anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc362_shell_scale_cap_obstruction.md，checker 为
tpc_bridge_b_tpc362_shell_scale_cap_obstruction_checker.py，编号论文为
papers/tpc-362-shell-scale-cap-obstruction/。

TPC-362 固定 TPC-361 的三个 high-origin origins `(313030,311166,321651)`，将 shell
ladder 扩展为 `Q=12,24,36,54,80,128,256,512`，在 counts `256,512`、exponents
`1,2` 与四种 sign laws 上完成 `384` 个真谱 rows。旧 working caps `0.83`（Schur）与
`0.64`（spectral）在 `Q<=80` 保持；`Q=128` 首次出现 cap violations，整条 ladder
的 normalized Schur/spectral maxima 为 `1.7172665118910415/1.6398895499394266`，
violations 为 `33/30`。law winners 为 all-plus/alternating-index/mod-4/half-split
`78/4/14/0`，336 个 Q transitions 为 `200/136/0` 增/降/平。

这是 shell-scale finite obstruction：low-Q cap 只对声明范围成立，不产生 shell-uniform
或 growing operator theorem、source-uniform arithmetic `L2`、fixed-power credit、
Route-B reassembly 或 twin-prime result。arithmetic advance 为 NO；official evaluator
files absent，local Bridge-B 仍 fail-closed。

    TPC362_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SHELL_SCALE_CAP_OBSTRUCTION
    TPC362_SHELL_SCALE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_384_ROWS
    TPC362_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
    TPC362_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
    TPC362_LOW_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC362_HIGH_Q_CAP_EXTENSION = REFUTED_SCOPED_ON_DECLARED_Q_LADDER
    TPC362_LAW_WINNER_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC362_GROWING_OPERATOR_BOUND = OPEN
    TPC362_SOURCE_UNIFORM_L2 = OPEN
    TPC362_ARITHMETIC_ADVANCE = NO
    TPC362_FIXED_POWER_CREDIT = 0
    TPC362_FULL_GATE_B = OPEN
    TPC362_TWIN_PRIME_RESULT = NONE
    TPC362_STATUS = NUMERICALLY_CERTIFIED_FINITE_SHELL_SCALE_CAP_OBSTRUCTION
    TPC362_ROUND2_CLUE = LOCALIZE_HIGH_Q_OBSTRUCTION_BY_LAW_AND_ROW_GEOMETRY

## V214 / TPC-361 previous anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc361_independent_high_origin_tightness_replication.md，checker 为
tpc_bridge_b_tpc361_independent_high_origin_tightness_replication_checker.py，编号论文为
papers/tpc-361-independent-high-origin-tightness-replication/。

TPC-361 在全新的 51 个候选 origins `310001+233j`、`0<=j<=50` 上，以 pilot count
256 的六组 unsigned geometry spread 做 response-blind selection，并按最小间隔 1536
的 greedy rule 选出 `(313030,311166,321651)`。随后以 counts `256,512,1024,2048`、
`Q=24,54,80`、exponents `1,2` 与四种 sign laws 完成 288 rows；四 law 在短 counts
与 all-plus 在长 counts 共记录 180 个真谱。normalized Schur max 为
`0.80830232610282304`，normalized spectral max 为 `0.62690716242733457`，最大
spectral/Schur ratio 为 `0.77585950058997`；短 panel winner 为 all-plus/mod-4
`30/6`。all-plus ladder 的 54 transitions 为 `12/36/6` 增/降/平。

这是 independent high-origin tightness replication：finite envelope、selection
response-independence 与 rational anchor 为 exact finite，数值 cap、tightness ratio、
law census 与 transition census 只对声明 panel 有效。growing operator theorem、
source-uniform arithmetic `L2`、fixed-power credit、Route-B reassembly 与 twin-prime
result 仍 open，arithmetic advance 为 NO；official evaluator files absent，local
Bridge-B 仍 fail-closed。

    TPC361_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION
    TPC361_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
    TPC361_HIGH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
    TPC361_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
    TPC361_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
    TPC361_TIGHTNESS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC361_LAW_UNIFORM_SHORT_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC361_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
    TPC361_GROWING_OPERATOR_BOUND = OPEN
    TPC361_SOURCE_UNIFORM_L2 = OPEN
    TPC361_ARITHMETIC_ADVANCE = NO
    TPC361_FIXED_POWER_CREDIT = 0
    TPC361_FULL_GATE_B = OPEN
    TPC361_TWIN_PRIME_RESULT = NONE
    TPC361_STATUS = NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION
    TPC361_ROUND2_CLUE = TEST_SCALE_LADDER_AND_SIGN_LAW_INTERACTION_ON_A_NEW_PANEL

## V213 / TPC-360 previous anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc360_schur_tightness_law_uniform_audit.md，checker 为
tpc_bridge_b_tpc360_schur_tightness_law_uniform_audit_checker.py，编号论文为
papers/tpc-360-schur-tightness-law-uniform-audit/。

TPC-360 在 TPC-359 的三个 fixed hostile origins 上，以 counts `256,512`、
`Q=24,54,80`、exponents `1,2` 与四种 sign laws 完成 144-row all-law spectral
replay。normalized spectral/Schur 最大 ratio 为 `0.77628391453148915`，
spectral/Frobenius 最大 ratio 为 `0.62110877254133434`；144 个 spectra 均低于
`0.64`，36 个 setting-wise comparisons 中 all-plus 赢 30、mod-4 赢 6。

这是 finite Schur-tightness 与 law-uniformity audit：envelope inequalities 为 exact
finite，ratio slack 与 winner census 都只对声明 panel 有效，不产生 growing operator
theorem、source-uniform arithmetic `L2`、fixed-power credit、Route-B reassembly 或
twin-prime result。official evaluator files absent，local Bridge-B 仍 fail-closed。

    TPC360_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT
    TPC360_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
    TPC360_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
    TPC360_ALL_LAW_SPECTRAL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
    TPC360_SCHUR_SLACK = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC360_LAW_UNIFORM_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC360_GROWING_OPERATOR_BOUND = OPEN
    TPC360_SOURCE_UNIFORM_L2 = OPEN
    TPC360_ARITHMETIC_ADVANCE = NO
    TPC360_FIXED_POWER_CREDIT = 0
    TPC360_FULL_GATE_B = OPEN
    TPC360_TWIN_PRIME_RESULT = NONE
    TPC360_STATUS = NUMERICALLY_CERTIFIED_FINITE_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT
    TPC360_ROUND2_CLUE = TEST_INDEPENDENT_HIGH_ORIGIN_REPLICATION_WITH_TIGHTNESS_LEDGER

## V212 / TPC-359 previous anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc359_geometry_adversarial_high_origin_holdout.md，checker 为
tpc_bridge_b_tpc359_geometry_adversarial_high_origin_holdout_checker.py，编号论文为
papers/tpc-359-geometry-adversarial-high-origin-holdout/。

TPC-359 在全新高起点候选 `260001+211j`、`0<=j<=50` 上，以 count-256 的 unsigned
geometry spread 做 response-blind selection，并以最小间隔 1536 的 greedy rule 选出
`267175,261267,269074`。完整 protocol 为 288 rows（counts `256,512,1024,2048`，
`Q=24,54,80`，exponents `1,2`，四种 sign laws）；normalized Schur max 为
`0.80834744529310265`，all-plus normalized spectral max 为 `0.6271657593674812`，
raw spectral max 为 `1542.7354827195263`，均把 TPC-358 的 finite cap transfer 保持在
`0.001` 内。normalized spectral transitions 为 `12/36/6`。

这是 geometry-adversarial high-origin 的 scoped finite holdout；Schur/Frobenius 为
exact finite，非单调性仍 `REFUTED_SCOPED_ON_DECLARED_LADDER`，不产生 growing
operator theorem、source-uniform arithmetic `L2`、fixed-power credit、Route-B
reassembly 或 twin-prime result。official evaluator files absent，local Bridge-B
仍 fail-closed。

    TPC359_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_HIGH_ORIGIN_HOLDOUT
    TPC359_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
    TPC359_HIGH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
    TPC359_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
    TPC359_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
    TPC359_PARENT_CAP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC359_NORMALIZED_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC359_SPECTRAL_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
    TPC359_GROWING_OPERATOR_BOUND = OPEN
    TPC359_SOURCE_UNIFORM_L2 = OPEN
    TPC359_ARITHMETIC_ADVANCE = NO
    TPC359_FIXED_POWER_CREDIT = 0
    TPC359_FULL_GATE_B = OPEN
    TPC359_TWIN_PRIME_RESULT = NONE
    TPC359_STATUS = NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_HIGH_ORIGIN_HOLDOUT
    TPC359_ROUND2_CLUE = TEST_SCHUR_TIGHTNESS_AND_INDEPENDENT_HIGH_ORIGIN_REPLICATION

## V211 / TPC-358 previous anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc358_fresh_origin_spectral_holdout.md，checker 为
tpc_bridge_b_tpc358_fresh_origin_spectral_holdout_checker.py，编号论文为
papers/tpc-358-fresh-origin-spectral-holdout/。

TPC-358 将 TPC-357 的 finite operator-envelope protocol 移到预注册且 disjoint 的
fresh origins `52001,120001,220001`，origin span 为 `168000`。在 counts
`256,512,1024,2048`、`Q=24,54,80`、exponents `1,2` 与四种 sign laws 上完成
`288` rows；所有 rows 有 raw/normalized Schur 与 Frobenius envelopes，all-plus 的
`72` rows 另有真谱范数。fresh normalized Schur maximum 为
`0.80850510742101689`，all-plus normalized spectral maximum 为
`0.62663944469203836`，均低于 parent caps `0.83/0.64` 且在 `0.001` 内转移。
normalized spectral ladder 的 54 个 transitions 为 `13` 增、`34` 降、`7` 平。

这是 scoped finite fresh-origin transfer；Schur/Frobenius inequalities 为 exact finite，
但不产生 origin-uniform/growing operator theorem。monotone decay 仍为
`REFUTED_SCOPED_ON_DECLARED_LADDER`；source-uniform arithmetic L2、fixed-power credit、
Route-B reassembly、full Gate B 与 twin-prime endpoint 仍 open，arithmetic advance 为
NO。official evaluator files absent，local Bridge-B 继续 fail-closed。

    TPC358_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_FRESH_ORIGIN_SPECTRAL_HOLDOUT
    TPC358_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
    TPC358_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
    TPC358_FRESH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
    TPC358_PARENT_CAP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC358_NORMALIZED_SCHUR_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC358_ALL_PLUS_SPECTRAL_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
    TPC358_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
    TPC358_GROWING_OPERATOR_BOUND = OPEN
    TPC358_SOURCE_UNIFORM_L2 = OPEN
    TPC358_ARITHMETIC_ADVANCE = NO
    TPC358_FIXED_POWER_CREDIT = 0
    TPC358_FULL_GATE_B = OPEN
    TPC358_TWIN_PRIME_RESULT = NONE
    TPC358_STATUS = NUMERICALLY_CERTIFIED_FINITE_FRESH_ORIGIN_SPECTRAL_HOLDOUT
    TPC358_ROUND2_CLUE = TEST_A_GEOMETRY_ADVERSARIAL_FRESH_ORIGIN_OR_SCHUR_TIGHTNESS_HOLDOUT_BEFORE_ANY_SOURCE_UNIFORM_OPERATOR_CLAIM

## V210 / TPC-357 previous anchor

TPC-357 冻结 TPC-356 的三个 geometry-adversarial origins
`38423,42010,45597`，将 count ladder 扩展为 `256,512,1024,2048`，并在
`Q=24,54,80`、exponents `1,2` 与四种 sign laws 上完成 `288` 个 operator rows。
所有 rows 都记录 raw/normalized Schur row-sum 与 Frobenius envelopes；all-plus 的
`72` 个 raw/normalized rows 另计算真谱范数。normalized Schur 最大值为
`0.8077815961017315`，all-plus normalized spectral 最大值为
`0.62665294142584216`，raw all-plus spectral 最大值为 `1542.7455490253569`。
在 54 个相邻 count transitions 中，normalized all-plus spectral 为 `15` 增、`35`
降、`4` 平（guard `1e-6`）。

这是 finite operator-envelope certificate 与 scoped monotonicity obstruction：
Schur/Frobenius inequalities 是 exact finite，数值 cap 只属于声明 panel，而
monotone decay 在该 ladder 上 `REFUTED_SCOPED`。source-uniform arithmetic L2、
growing masked-operator bound、fixed-power credit、full Gate B、Route-B reassembly
与 twin-prime endpoint 仍 open，arithmetic advance 为 NO。official evaluator files
absent，local Bridge-B 仍是 fail-closed fallback。

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
    TPC357_ROUND2_CLUE = ATTACK_THE_FINITE_NORMALIZED_SPECTRAL_CAP_ON_A_PREREGISTERED_FRESH_ORIGIN_SCALE_HOLDOUT_BEFORE_ANY_UNIFORM_CLAIM

## V209 / TPC-356 previous anchor

TPC-356 冻结 TPC-355 的 unsigned mask-energy congruence，并在 51 个晚期候选 origins
上只用 count 256 的六组 unsigned geometry spread 做 adversarial 选择；按 descending
score 与最小间隔 1536 的 greedy rule 选出 38423、42010、45597。选择不读取 source
response 或 sign law。随后以 counts 256/512/1024、Q=24/54/80、exponents 1/2 与四种
sign laws 重放 216 rows；raw 与 normalized 各为 216/216 positive。all-plus minimum
从 0.63140161782616067 升到 0.65046429467683675，mean 从 0.8687258535297816
升到 0.87560762679420479，有限 gains 为 0.019062676850676086 与
0.0068817732644231855。

这是 geometry-only adversarial finite transfer signal；它不提供 origin/scale uniform
bound。source-uniform arithmetic L2、masked operator bound、fixed-power credit、full
Gate B、Route-B reassembly 与 twin-prime endpoint 仍 open，arithmetic advance 为 NO。
official evaluator files absent，local Bridge-B 仍是 fail-closed fallback。

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

## V208 / TPC-355 previous anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc355_position_aware_mask_energy_normalization.md，
checker 为
tpc_bridge_b_tpc355_position_aware_mask_energy_normalization_checker.py，编号论文为
papers/tpc-355-position-aware-mask-energy-normalization/。

TPC-355 在 TPC-353 low-origin、TPC-354 higher-origin 与 fresh origins
`29001,33001,37001` 三面板上，冻结同一 V59 source、literal two-endpoint masked
operator、counts `256,512,1024`、shell anchors `Q=24,54,80`、exponents `1,2`、
四种 sign laws、`H=66` 与 cutoff `50000`。预先定义 unsigned component geometry
`G_u=sum_(p,t)B_p(u,t)^2`，并测试 `A#=D_G^(-1/2) A D_G^(-1/2)`。共 `648`
rows；raw 与 normalized 各有 `647/648` positive、`1/648` negative、`0`
unresolved。all-plus low-to-higher minimum drop 从
`0.042151146184724153` 降为 `0.026236988152766205`，有限 reduction fraction
为 `0.37754982894688971`；但 normalized mean drop 反而为
`0.024839744603963321`，高于 raw 的 `0.021249745559872912`。

这是 exact finite geometry/congruence/polarization interface 与 numerically
certified finite partial floor repair；fresh mod-4 negative row 与 mean failure
使 law-uniform repair 被 `REFUTED_SCOPED`。source-uniform arithmetic `L2`、uniform
masked operator bound、fixed-power credit、full Gate B、Route-B reassembly 与
twin-prime endpoint 仍 open。official evaluator files absent，local Bridge-B 继续
fail-closed；下一关为 adversarial position/origin normalization holdout。

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

## V207 / TPC-354 previous anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc354_higher_origin_masked_l2_holdout.md，checker 为
tpc_bridge_b_tpc354_higher_origin_masked_l2_holdout_checker.py，编号论文为
papers/tpc-354-higher-origin-masked-l2-holdout/。

TPC-354 把同一 finite V59 residual 与 literal two-endpoint
divisibility-masked operator 原样移到 disjoint higher origins
`21001,23001,25001`；counts `256,512,1024`、shell anchors `Q=24,54,80`、
exponents `1,2`、四个 sign laws、`H=66` 与 source cutoff `50000` 全部冻结。
`216/216` operator images 都有正 alignment；all-plus output `kappa_A` 为
`0.65076036812307647--0.99135023146539858`，mean 为
`0.87436211602135017`，source-level coefficient 为
`0.36357606682978283--0.38648419369238701`。相对 hash-locked TPC-353 parent，
all-plus minimum/mean shift 为 `-0.042151146184724153` /
`-0.021249745559872912`。

这是 exact finite operator polarization、Cauchy envelope 与 declared-model
attachment，加上 numerically certified finite higher-origin replay；不是
source-uniform arithmetic `L2`。正 transfer 保留，但 all-plus floor/mean transfer
为 `REFUTED_SCOPED`，且 source/output mismatch 仍存在。uniform masked operator
bound、fixed-power credit、full Gate B、Route-B reassembly 与 twin-prime endpoint
仍 open。Session-named official evaluator files absent，local Bridge-B 继续
fail-closed；下一关测试 position-aware masked normalization/bound。

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

## V206 / TPC-353 previous anchor

TPC-353 是 TPC-354 的 hash-locked parent：它在 origins `6001,8001,10001` 上把
V59 residual 接入 literal masked operator，完成 `216/216` positive-alignment
finite polarization replay；all-plus `kappa_A` 为
`0.69291151430780062--0.99626802812598902`。source/operator mismatch 使
source-uniform masked `L2` 仍保持 `OPEN`。

## V205 / TPC-352 previous anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc352_reciprocal_shell_adversarial_holdout.md，checker 为
tpc_bridge_b_tpc352_reciprocal_shell_adversarial_holdout_checker.py，编号论文为
papers/tpc-352-reciprocal-shell-adversarial-holdout/。

TPC-352 是对 TPC-351 reciprocal-shell repair 的 disjoint adversarial holdout。冻结
origins `96097,120097,144097`、lengths `256,512,1024` 与新 shell anchors
`Q=64,128,256,512`，不改变 reciprocal coefficient rule，也不按 holdout response
拟合。`144/144` 行有正响应，`118/144` 行改善 balanced parent；ratio 为
`0.0801262572786--0.829632172143`，`49/144` 达到 half-defect，`47/144` 超过
coordinate baseline，`22/48` series nondecreasing。`Q=256` 的 reciprocal floor
低于 parent，故有限 repair 的 uniform transfer 被 `REFUTED_SCOPED`，该 branch
冻结并返回 source-native masked arithmetic `L2`。

这是 `PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT`；
exact statements 仍限于 rational balance、incidence Gram 与 induced-norm witness，
arithmetic `L2`、uniform masked operator bound、fixed-power credit、Route-B
reassembly 与 twin-prime endpoint 均 open。official evaluator files absent，故只记
local Bridge-B fail-closed。

    TPC352_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT
    TPC352_RECIPROCAL_RULE = PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE
    TPC352_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
    TPC352_DISJOINT_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
    TPC352_RECIPROCAL_POSITIVE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_144_OF_144
    TPC352_PARENT_IMPROVEMENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_118_OF_144
    TPC352_UNIFORM_REPAIR_TRANSFER = REFUTED_SCOPED
    TPC352_HIGH_SHELL_REPAIR = REFUTED_SCOPED
    TPC352_ARITHMETIC_ADVANCE = NO
    TPC352_FIXED_POWER_CREDIT = 0
    TPC352_FULL_GATE_B = OPEN
    TPC352_TWIN_PRIME_RESULT = NONE
    TPC352_STATUS = PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT
    TPC352_ROUND2_CLUE = FREEZE_FINITE_RECIPROCAL_BRANCH_AND_RETURN_TO_SOURCE_NATIVE_L2

## V204 / TPC-351 previous anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc351_reciprocal_shell_contrast.md，checker 为
tpc_bridge_b_tpc351_reciprocal_shell_contrast_checker.py，编号论文为
papers/tpc-351-reciprocal-shell-contrast/。

TPC-351 承接 TPC-350 的 high-shell floor obstruction，冻结一个不依赖 origin、
length、source law、矩阵 entries 或 observed response 的 reciprocal-shell rule：
`gamma_j=1/p_j-r^(-1)sum_k 1/p_k`。该有理 coefficient vector exact zero-sum，
因此 prime-incidence Gram identity 与 normalized induced-norm lower witness 都是
exact finite algebra。原 192-row panel 上，所有 reciprocal witnesses 有正响应，
`180/192` rows 改善 TPC-350；reciprocal/defect ratio 为
`0.0917557319271--0.901734353382`，`86/192` 超过 coordinate baseline，
`111/192` 达到 half-defect，`25/48` length series nondecreasing。

这是 `PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT`；
reciprocal centering 构成真实 finite repair，但 12 rows 没有改善，floor 仍低于
`1/4`，因此 universal quarter-floor 继续 `REFUTED_SCOPED`。source-uniform
arithmetic `L2`、uniform masked operator bound、fixed-power credit、Route-B
reassembly 与 twin-prime endpoint 继续 open。Session-named evaluator files absent，
故只记录 local Bridge-B fail-closed；下一步是 disjoint adversarial holdout。

    TPC351_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT
    TPC351_RECIPROCAL_ZERO_SUM_RULE = PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE
    TPC351_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
    TPC351_SCALE_REPAIR_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
    TPC351_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
    TPC351_PARENT_IMPROVEMENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_180_OF_192
    TPC351_COORDINATE_BASELINE_BEATEN = NUMERICALLY_CERTIFIED_FINITE_86_OF_192
    TPC351_HALF_DEFECT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_111_OF_192
    TPC351_NONDECREASING_GROWTH_SERIES = NUMERICALLY_CERTIFIED_FINITE_25_OF_48
    TPC351_UNIFORM_QUARTER_FLOOR = REFUTED_SCOPED
    TPC351_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
    TPC351_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
    TPC351_ARITHMETIC_ADVANCE = NO
    TPC351_FIXED_POWER_CREDIT = 0
    TPC351_FULL_GATE_B = OPEN
    TPC351_TWIN_PRIME_RESULT = NONE
    TPC351_STATUS = PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT
    TPC351_ROUND2_CLUE = ADVERSARIAL_HOLDOUT_FOR_RECIPROCAL_CONTRAST_BEFORE_BRANCH_FREEZE

## V203 / TPC-350 previous anchor

更新时间：2026-09-03

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc350_fresh_growth_signed_incidence.md，checker 为
tpc_bridge_b_tpc350_fresh_growth_signed_incidence_checker.py，编号论文为
papers/tpc-350-fresh-growth-signed-incidence/。

TPC-350 承接 TPC-349 的 zero-sum prime-incidence witness，把位置移到三个 fresh
origins，并把区间长度扩展为 `256,512,1024,2048`，同时测试
`Q=36,80,128,256` 的 shell-scale ladder。两种 source law、两种 exponent 形成
`192` 行与 `48` 条 length series。所有 rows 仍有正响应，signed/defect ratio 为
`0.0657381187306--0.8797933448`，但 `Q=256` 的 48 行全部低于 half-defect；
整体仅 `70/192` 超过 coordinate baseline、`91/192` 达到 half-defect，且只有
`24/48` length series nondecreasing。

这是 `PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT`；
fresh finite replication 成立，但 universal quarter-floor 记为 `REFUTED_SCOPED`。
source-uniform arithmetic `L2`、uniform masked operator bound、fixed-power credit、
Route-B reassembly 与 twin-prime endpoint 继续 open。Session-named evaluator files
仍 absent，故只记录 local Bridge-B fail-closed。

    TPC350_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT
    TPC350_SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
    TPC350_FRESH_GROWTH_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
    TPC350_POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
    TPC350_SIGNED_TO_DEFECT_FLOOR = NUMERICALLY_CERTIFIED_FINITE_0.0657381187306
    TPC350_COORDINATE_BASELINE_BEATEN = NUMERICALLY_CERTIFIED_FINITE_70_OF_192
    TPC350_HALF_DEFECT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_91_OF_192
    TPC350_NONDECREASING_GROWTH_SERIES = NUMERICALLY_CERTIFIED_FINITE_24_OF_48
    TPC350_UNIFORM_QUARTER_FLOOR = REFUTED_SCOPED
    TPC350_SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
    TPC350_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
    TPC350_ARITHMETIC_ADVANCE = NO
    TPC350_FIXED_POWER_CREDIT = 0
    TPC350_FULL_GATE_B = OPEN
    TPC350_TWIN_PRIME_RESULT = NONE
    TPC350_STATUS = PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT
    TPC350_ROUND2_CLUE = TEST_SCALE_ADAPTIVE_ZERO_SUM_CONTRAST_ON_HIGH_SHELLS

## V202 / TPC-349 previous anchor

更新时间：2026-09-02

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc349_prime_balanced_signed_defect_witness.md，checker 为
tpc_bridge_b_tpc349_prime_balanced_signed_defect_witness_checker.py，编号论文为
papers/tpc-349-prime-balanced-signed-defect-witness/。

TPC-349 承接 TPC-348 的 coordinate defect witness，对升序 shell primes 取等量
正负、总和为零的 `beta` split（奇数 shell 留一个中性 prime），并定义
`b_I(t)=sum_j beta_j 1_(p_j|t)`。它证明 exact prime-incidence Gram expansion 与
`||D_I||_(2->2)>=||D_Ib_I||_2/||b_I||_2`。冻结的 `192` rows 全部有非零 signed
vector 与正响应；signed/defect ratio 为 `0.39083565842--0.954375010719`，
`136/192` rows 超过 TPC-348 coordinate baseline，`175/192` rows 达到 half-defect。

这是 `PROVED_EXACT_FINITE_PRIME_BALANCED_INCIDENCE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_AUDIT`；
56 rows 不超过 coordinate baseline，因此 universal balanced gain 为
`REFUTED_SCOPED`。source-uniform arithmetic `L2`、uniform masked operator bound、
fixed-power credit、Route-B reassembly 与 twin-prime endpoint 继续 open。Session-named
evaluator files absent，故只记录 local Bridge-B fail-closed。

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

## V201 / TPC-348 previous anchor

更新时间：2026-09-02

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc348_position_aware_mask_defect_lower_witness.md，checker 为
tpc_bridge_b_tpc348_position_aware_mask_defect_lower_witness_checker.py，编号论文为
papers/tpc-348-position-aware-mask-defect-lower-witness/。

TPC-348 承接 TPC-347 的 exact convolution-plus-defect interface，继续保留 literal
divisibility masks。对 defect `D_I=A_I-T_I`，定义 mask-hit positions
`J_I={t in I: exists active p with p|t}`，并证明
`||D_I||_(2->2) >= max_(t in J_I)||D_I e_t||_2`。同时保留左右 projection
defect 的 exact position formula；它不是 leading-eigenvector fit。两 origin、三
source counts、四个 `Q` anchors、两种 exponent 与四个 sign laws 共 `192` rows，
`192/192` 行有严格正的 best-hit witness，best-hit/defect ratio 为
`0.453958762219--0.897148966365`，position-formula replay 最大误差为
`2.0872192863e-14`，并通过 exact rational six-point anchor 与 hostile mutations。

这是 `PROVED_EXACT_FINITE_COORDINATE_LOWER_WITNESS_PLUS_NUMERICALLY_CERTIFIED_FINITE_POSITION_AUDIT`；
它把 TPC-347 的 mask-discard obstruction 定位到确定坐标，但没有产生 growing
lower bound。source-uniform arithmetic `L2`、uniform masked operator bound、fixed-power
credit、Route-B reassembly 与 twin-prime endpoint 仍 open。Session-named evaluator
文件仍缺失，因此只记录 local Bridge-B fail-closed，不宣称 official Route-A/Route-B
pass。

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

## V200 / TPC-347 previous anchor

更新时间：2026-09-02

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc347_convolution_mask_defect_interface.md，checker 为
tpc_bridge_b_tpc347_convolution_mask_defect_interface_checker.py，编号论文为
papers/tpc-347-convolution-mask-defect-interface/。

TPC-347 承接 TPC-346 冻结的 arithmetic-L2 回归方向，保留 literal divisibility
masks，并把物理 finite block 精确写成
`A_I=T_I+D_I`，其中 `T_I` 是 unmasked translation-invariant convolution 的
interval compression，`D_I` 是显式 projection defect。Fourier multiplier norm、
compression inequality 与 Young tail envelope 在相应的 unmasked/finite 条件下是
exact；两 origin、三 source counts、四个 shell anchors、两种 exponent 与四个
sign laws 共 `192` rows，`96/96` ideal origin checks 和 `192/192` combined-bound
checks 通过。defect/ideal spectral ratio 为 `0.0312337689685--0.467075645603`，
其中 `93/192` 超过 `1/4`。

这是 `PROVED_EXACT_FINITE_CONVOLUTION_MASK_DEFECT_INTERFACE_PLUS_NUMERICALLY_CERTIFIED_FINITE_SPECTRAL_AUDIT`；
它 refute 了声明面板上的 mask-discard shortcut，但没有给出 source-uniform
arithmetic `L2` 或 uniform masked operator bound。Session-named evaluator 文件仍
缺失，因此只记录 local Bridge-B fail-closed，不宣称 official Route-A/Route-B pass。

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

## V199 / TPC-346 previous anchor

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc346_third_panel_hostile_replication.md，checker 为
tpc_bridge_b_tpc346_third_panel_hostile_replication_checker.py，编号论文为
papers/tpc-346-third-panel-hostile-replication/。

TPC-346 在 TPC-345 的 basis-invariant geometry 后加入预声明的 disjoint fresh
third panel `[44097,44609,45217]`。fresh own-fit retention 为
`0.3159173453/0.3294074741`（raw/equal-row），三 panel adaptive retention 为
`0.2999630726/0.3222362713`；因此 raw crossing 不具 weighting stability。
六个 directed predictions、三个 leave-one-panel-out predictions 与十八个 fresh
control-LOO projections 全部超过 `0.30`。

这是 `NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION`；shared-to-adaptive
nested identity 与 projection identities 是 exact finite linear algebra，fresh own-fit、
weighting stability、third-panel transfer 与 control-LOO 均为 scoped finite
obstruction。panel-adaptive branch 仅作 finite freeze；source-uniform arithmetic `L2`、
uniform masked operator bound、fixed-power credit 与 twin-prime endpoint 仍 open。
Session-named evaluator files absent，故只记 local Bridge-B fail-closed，不宣称
official Route-A/Route-B pass。

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

## V198 / TPC-345 previous anchor

TPC-345 的 principal-angle/Grassmann geometry 仍作为 TPC-346 的 parent lock：
raw 第一主角 `5.3142°`、equal-row 第一主角 `23.8720°`，双向 transfer 与
weighting-stability 均已 scoped refute。

## V197 / TPC-344 previous anchor

TPC-344 的 panel-contrast basis 对 raw pooled fit 给出 `0.2962189247` 的窄幅
partial repair，但 equal-row `0.3186506700` 与四个 cross-fits 均未通过；
TPC-345 已将该坐标模型升级为 subspace-level stability audit。

## V196 / TPC-343 previous anchor

TPC-343 锁定 TPC-341 与 TPC-342 两个 protocol-compatible panels，共六个
cutoff-safe windows。它比较 row-block nuisance projection（每行独立系数）与
shared projection（六行共用一个系数向量）。row-block raw-energy retention 为
`0.2325429101`，而 shared raw 与 equal-row retention 分别为
`0.3198013104` 与 `0.3549335801`。

这是 `NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE`；stacked projection
identity 是 declared finite linear algebra，shared-coefficient failure 是 scoped finite fact，
不是 arithmetic estimate。source-uniform arithmetic `L2`、uniform masked operator bound、
fixed-power credit 与 twin-prime endpoint 仍 open。Session-named evaluator files absent，
故只记 local Bridge-B fail-closed，不宣称 official Route-A/Route-B pass。

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

## V195 / TPC-342 previous anchor

TPC-342 independently reproduced TPC-341 on windows `[40097,40608]`, `[40609,41120]`,
and `[41121,41632]`; its in-sample retention was `0.2701410521--0.2951006120` and
its 27 held-out retentions were `0.5894842476--0.9429165296`.

## V194 / TPC-341 previous anchor

TPC-341 established the parent fresh-window aggregate-versus-holdout split: in-sample
retention was `0.2010894086--0.2560626551`, while all 27 held-out records retained
`0.4435267486--0.8904473564`. TPC-342 is its protocol-locked independent reproduction.

## V193 / TPC-340 previous anchor

TPC-340 将 TPC-339 的 support-restricted Frobenius envelope 与 global Schur envelope
合并为 `||Ax||^2 <= min(||A[:,S]||_F^2,R^2)||x||^2`。六 windows、九 controls、四
masks 的 216 条记录全部无 violation；Schur branch 为 54 条，Frobenius branch 为
162 条，zero-support 的有限 improvement factor 为 `1.250245--4.698443`。但 broad
mask hybrid occupancy 仍不超过 `0.1868550366`，所以这只是 sign-free finite
improvement，不是 sharp uniform response theorem。

    TPC340_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE
    TPC340_HYBRID_BOUND = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC340_HYBRID_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_RECORDS
    TPC340_BOUND_CENSUS = NUMERICALLY_CERTIFIED_FINITE_0_VIOLATIONS
    TPC340_SCHUR_BRANCH_CENSUS = NUMERICALLY_CERTIFIED_FINITE_54_RECORDS
    TPC340_FROBENIUS_BRANCH_CENSUS = NUMERICALLY_CERTIFIED_FINITE_162_RECORDS
    TPC340_BROAD_TIGHTNESS = REFUTED_SCOPED
    TPC340_ARITHMETIC_ADVANCE = NO
    TPC340_FIXED_POWER_CREDIT = 0
    TPC340_SOURCE_UNIFORM_L2 = OPEN
    TPC340_FULL_GATE_B = OPEN
    TPC340_TWIN_PRIME_RESULT = NONE
    TPC340_STATUS = NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE
    TPC340_ROUND2_CLUE = TEST_NUISANCE_ORTHOGONALIZATION_OR_ADVERSARIAL_HOLDOUT

## V192 / TPC-339 previous anchor

TPC-339 在 TPC-338 的九-control panel 上建立 sign-free support-restricted bound
`||Ax||^2 <= ||A[:,S]||_F^2||x||^2`。216 条 mask/control records 中 198 条非空且
全部通过；broad masks 的 occupancy 均低于 `0.2`，而 prime-power singleton-like
records 可达到 equality。它证明了有限 envelope 的可靠性，同时 refute 了其在 broad
mask 上自动 sharp 的解释，下一步自然加入 global Schur branch。

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

## V191 / TPC-338 previous anchor

TPC-338 把 TPC-337 的五-control orbit 扩展到九个 controls。六 rows 的 centered
fraction 仍为 `0.8771801838--0.8972635786`，normalized covariance spectrum 的
`L1` 距离为 `0.0264396313--0.0440591812`；但 twin/zero covariance 从五-control 的
`6/6` negative 变成九-control 的 `6/6` positive。能量集中比 signed interaction
更稳定，因此选定 sign-free masked bound 作为下一关。

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

## V190 / TPC-337 previous anchor

TPC-337 将 TPC-336 的四个 source masks 经过五个 predeclared coordinate bijections，
形成 class-output covariance Gram ledger。六 rows 的 centered fraction 为
`0.7850322548--0.8552982168`；twin/background covariance 在 `6/6` 为正，
twin/zero 与 background/zero 在 `6/6` 为负。mean/centered identity 与 covariance
Gram PSD 是 exact finite algebra，但 signed interaction 的 canonicality 被留作开放
问题，并由 TPC-338 的 growing-control sign audit 直接攻击。

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

## V189 / TPC-336 previous anchor

TPC-336 将四个 source masks 送入固定 all-plus signed-Gram operator；六 rows 的 gain
ordering 全部为 `zero_support > non_twin_prime_shift > twin_prime > prime_power_shift`，
并全部出现 destructive output interaction。它是 TPC-337 covariance ledger 的直接
parent；该 finite response 仍不提供 uniform masked operator bound。

## V188 / TPC-335 previous anchor

TPC-335 对 TPC-334 的四个 support masks 做 exact disjoint residual norm split。六行
twin norm fraction 为 `9.556%--12.242%`，non-twin background 为 `67.050%--69.657%`，
而 twin 相对 raw cross share 的 amplification 为 `1.7065--1.7706`。它确认 twin
component 非零但不是 residual-energy 主导类，下一关因此转入固定 operator response。

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

## V187 / TPC-334 previous anchor

TPC-334 将 TPC-333 cross term 按 twin、non-twin prime-shift、prime-power 与 zero
support 精确分账。六行 twin share 为 `5.43%--7.17%`，non-twin share 为
`92.83%--94.42%`，因此 raw cross term 不是 twin-prime proxy；下一关是 twin-isolated
residual norm，而非 arithmetic conclusion。

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

## V186 / TPC-333 previous anchor

TPC-333 在六个 source windows 上测得 `kappa` 区间
`[0.35486589921455675,0.36250235375855522]`，并将 near-orthogonality 与
near-total-cancellation 的极端解释限制为 scoped finite refutations。它把下一关
明确为 support attribution。

    TPC333_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER
    TPC333_POLARIZATION_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
    TPC333_SIX_WINDOW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS
    TPC333_CANCELLATION_COEFFICIENT = NUMERICALLY_CERTIFIED_FINITE_0.35_TO_0.37
    TPC333_ARITHMETIC_ADVANCE = NO
    TPC333_FIXED_POWER_CREDIT = 0
    TPC333_SOURCE_UNIFORM_L2 = OPEN
    TPC333_FULL_GATE_B = OPEN
    TPC333_TWIN_PRIME_RESULT = NONE
    TPC333_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER
    TPC333_ROUND2_CLUE = CLASSIFY_CROSS_TERM_SUPPORT_BY_PRIME_POWER_AND_TWIN_MASK

## V185 / TPC-332 previous anchor

TPC-332 在两个 disjoint origins、三个 nested scales 上复现 TPC-331 的 control-average /
centered split，48 rows 中 all-plus average/centered 为 `48/48`、coherent 为 `47/48`；
它首次把 source polarization 纳入同一 growing finite certificate。

## V183 / TPC-330 previous anchor

TPC-330 的 affine-family response spectrum 仍是本关的直接 parent certificate 与
placement-obstruction provenance。

## V181 / TPC-328 previous anchor

TPC-328 的 source-native finite Gram cancellation/obstruction atlas 仍保留为本关的
parent certificate 与 direct engine provenance。

## V180 / TPC-327 previous anchor

## V179 / TPC-326 previous anchor

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc326_cross_origin_scale_replication.md，checker 为
tpc_bridge_b_tpc326_cross_origin_scale_replication_checker.py，编号论文为
papers/tpc-326-cross-origin-scale-replication/。

TPC-326 承接 TPC-325 的 source-scale ladder，把同一 literal
deleted-diagonal centered prime-shell operator 搬到完全 disjoint 的第二个 source
origin 16001。四个 nested source counts 仍为 160,320,640,1280；H=66、
Q={24,36,54,80}、s={1,2} 与四个 sign laws 全部冻结。新的 32 rows 中 all-plus
normalized profile 在 32/32 行 majorizes direct profile，四种 profile/energy census
与 TPC-325 完全匹配；TV envelope 最大差 0.000797...、energy upper envelope 最大差
0.004552...，均低于预声明阈值 0.001、0.005。

这是 NUMERICALLY_CERTIFIED_FINITE_CROSS_ORIGIN_SCALE_LADDER_REPLICATION。它是
有限 adversarial replication，不是 source-uniform theorem、arithmetic L2、
fixed-power credit 或 twin-prime endpoint；Session-named evaluator files absent，
故只记 local Bridge-B fail-closed，不宣称 official Route-A/Route-B pass。

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

## V178 / TPC-325 previous anchor

TPC-325 的完整入口与 finite source-scale audit 仍保留在下方；它是本关的直接
parent certificate 与 engine provenance。

## V178 / TPC-325 release details

更新时间：2026-09-01

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc325_scale_ladder_profile.md，checker 为
tpc_bridge_b_tpc325_scale_ladder_profile_checker.py，编号论文为
papers/tpc-325-scale-ladder-profile/。

TPC-325 承接 TPC-324 的 source-location holdout，在同一 literal
deleted-diagonal centered prime-shell blocks 上冻结新 origin `12001`，只改变嵌套
source cardinality `160,320,640,1280`。四个 scale rungs 与
`Q={24,36,54,80}`、`s={1,2}` 形成 32 rows；all-plus normalized profile 在 32/32
行 majorizes direct profile。outward lower TV envelope 与 outward upper energy
envelope 均沿四档严格下降；替代 sign laws 的 majorizing/mixed 计数为
`21/11`、`26/6`、`23/9`。

这是 `NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT`；四档趋势仍只是
finite numerical observation，不提供 uniform growing theorem、source-native
arithmetic `L2`、fixed-power credit 或 twin-prime endpoint。Session-named evaluator
files absent，故不宣称 official Route-A/Route-B pass。

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

## V177 / TPC-324 previous anchor

更新时间：2026-09-01

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc324_source_profile_holdout.md，checker 为
tpc_bridge_b_tpc324_source_profile_holdout_checker.py，编号论文为
papers/tpc-324-source-profile-holdout/。

TPC-324 承接 TPC-323 的 signed profile majorization，在同一 literal
deleted-diagonal centered prime-shell blocks 上只改变 source location。两个与
TPC-323 training union disjoint 的 holdout panels 共 48 rows；all-plus normalized
profile 在 48/48 行 majorizes direct profile，且每个 panel 都是 24/24。alternating、
mod-4、half-split 的 majorizing/mixed 计数为 34/14、42/6、36/12，和 parent panel
完全相同；all-plus energy ratio 为 6/48 below、42/48 above。

这是 `NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION`；
conditional translation covariance 是 `PROVED_EXACT_FINITE_CONDITIONAL`，但 holdout
复现仍是有限数值结果，不提供 source-native arithmetic `L2`、渐近 power saving、
fixed-power credit 或 twin-prime endpoint。Session-named evaluator files absent，故
不宣称 official Route-A/Route-B pass。

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

## V176 / TPC-323 previous anchor

更新时间：2026-09-01

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc323_signed_profile_majorization.md，checker 为
tpc_bridge_b_tpc323_signed_profile_majorization_checker.py，编号论文为
papers/tpc-323-signed-profile-majorization/。

TPC-323 承接 TPC-322 的 signed-projector interface，在同一 literal
deleted-diagonal centered prime-shell blocks 上把总能量 ratio 与归一化谱 profile
分开读取。对 `X={640,1280,2560}`、`Q={24,36,54,80}`、`s={1,2}` 的 24 rows，
all-plus coherent Gram 的 normalized profile 在 24/24 行 majorizes direct profile；
alternating、mod-4、half-split 三个 declared laws 的 majorizing/mixed 计数分别为
17/7、21/3、18/6。all-plus energy ratio 同时为 3/24 below、21/24 above，说明
amplitude 与 shape 不是同一个读数。

这是 `NUMERICALLY_CERTIFIED_FINITE_SIGNED_PROFILE_MAJORISATION_AUDIT`；
trace/profile factorisation 是 `PROVED_EXACT_FINITE`，但结果仍是有限
operator-level profile audit，不提供 source-native arithmetic `L2`、渐近 power
saving、fixed-power credit 或 twin-prime endpoint。Session-named evaluator files
absent，故不宣称 official Route-A/Route-B pass。

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

## V175 / TPC-322 previous anchor

更新时间：2026-09-01

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc322_signed_projector_reassembly.md，checker 为
tpc_bridge_b_tpc322_signed_projector_reassembly_checker.py，编号论文为
papers/tpc-322-signed-projector-reassembly/。

TPC-322 承接 TPC-321 的 shell-sensitive trace-normalized profile，在同一 literal
deleted-diagonal centered prime-shell blocks 上把 direct-sum output 投影到
sign-labelled diagonal copy。精确恒等式给出
`||P_e A_\oplus||_HS^2=m^{-1}||sum_p e_p B_p||_F^2`，并由 24-row exhaustive
finite atlas 验证每行同时存在 `rho<1` 与 `rho>1` 的 sign。all-plus law 在 3/24
行低于 1、21/24 行高于 1；index-alternating law 在 21/24 行低于 1、3/24 行高于 1。

这是 `NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_REASSEMBLY_ATLAS`，
signed projector identity 为 `PROVED_EXACT_FINITE`。它只证明 operator-level finite
interface 与 sign-law flexibility；不提供 canonical Möbius sign、source-native
arithmetic `L2`、渐近 power saving、fixed-power credit 或 twin-prime endpoint。
Session-named evaluator files absent，故不宣称 official Route-A/Route-B pass。

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
    TPC322_ROUND2_CLUE = TEST_CANONICAL_SIGN_LAWS_AGAINST_OPERATOR_SPECTRAL_PROFILES_AND_SOURCE_NATIVE_ARITHMETIC_L2

## V174 / TPC-321 previous anchor

更新时间：2026-08-31

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc321_cross_shell_profile.md，checker 为
tpc_bridge_b_tpc321_cross_shell_profile_checker.py，编号论文为
papers/tpc-321-cross-shell-profile-stability/。

TPC-321 承接 TPC-320 的 trace-normalized spectral profile，在同一 literal
deleted-diagonal centered prime-shell Gram 上比较固定 X、s 下的相邻 Q 壳层。24 rows、
18 adjacent-Q comparisons、三条 producer profile path 与 independent reverse/einsum
replay 给出 TV 和 Lorenz/Ky Fan cumulative distance 在 18/18 上分别严格超过 0.03
和 0.02；majorization pattern 为 3 forward / 2 reverse / 13 mixed。该结果是有限
shell-sensitivity obstruction，uniform profile law、arithmetic cancellation、fixed-power
credit 与 full Gate B 仍 open；不宣称 official Route-A/Route-B pass。

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

## V173 / TPC-320 current anchor

更新时间：2026-08-31

当前入口：proof 为
research/tpc-big-road/bridge_b_tpc320_trace_normalized_spectral_concentration.md，
checker 为
tpc_bridge_b_tpc320_trace_normalized_spectral_concentration_checker.py，编号论文为
papers/tpc-320-trace-normalized-spectral-concentration/。

TPC-320 承接 TPC-319 的 normalization firewall，在同一 literal deleted-diagonal
centered prime-shell Gram 上定义 trace-normalized spectral mass
C_k=F_k/trace(G)。24 rows、五个 k 值、双 shell 顺序与双谱路径给出
80/80 strict finite concentration decreases；positive-scalar invariance、
stable rank、participation rank 和 entropy 的状态分别由 exact identity、
finite observations 与 mixed control 区分记录。uniform spectral law、arithmetic
cancellation、fixed-power credit 与 full Gate B 仍 open；不宣称 official
Route-A/Route-B pass。

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

更新时间：2026-09-01
状态：`BOLD_CHANNEL_V180 / THREE_ORIGIN_SCALE_TRIANGULATION`
claim level：`NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION`
编号事实终点：TPC-327；TPC-327 trigger：`true`

TPC-327 的三源 pooled readout：第三 origin `20001` 的新 32 rows 保持 all-plus
profile majorization `32/32`，四-law profile/energy census 与 `12001`、`16001`
两个父 origin 都匹配；三-origin 最大 TV/energy range 为
`0.000797...<0.001`、`0.004552...<0.005`。这是 finite triangulation，
source-native arithmetic `L2`、fixed-power credit 与 full Gate B 仍 open。

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

此前 TPC-320 入口：proof 为
`research/tpc-big-road/bridge_b_tpc320_trace_normalized_spectral_concentration.md`，checker 为
`tpc_bridge_b_tpc320_trace_normalized_spectral_concentration_checker.py`，编号论文为
`papers/tpc-320-trace-normalized-spectral-concentration/`。它给出 80/80
trace-normalized concentration decreases 与 16/16 stable/participation observations；
本关沿其 ROUND2 clue 转向跨壳层 full-profile sensitivity。

此前 TPC-319 入口：proof 为
`research/tpc-big-road/bridge_b_tpc319_kyfan_cluster.md`，checker 为
`tpc_bridge_b_tpc319_kyfan_cluster_checker.py`，编号论文为
`papers/tpc-319-kyfan-cluster-normalization-firewall/`。它在 TPC-318 的同一 literal
Gram 上使用 Ky Fan 簇质量 `F_k=sum_{j<=k} lambda_j`，审计
`k={1,2,4,8,16}`。24 rows、双 shell 顺序和双 solver 支持 80/80 normalized
decreases 与 80/80 unnormalized increases；精确 normalization-flip identity 将这
两个方向统一为一个 firewall。gap/effective-rank 仅作有限观察，uniform normalization
law、arithmetic cancellation、fixed-power credit 与 full Gate B 仍 open。Session-named
evaluator files absent，故不宣称 official Route-A/Route-B pass。

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

当前 TPC-318 入口：proof 为
`research/tpc-big-road/bridge_b_tpc318_top_eigenvalue.md`，checker 为
`tpc_bridge_b_tpc318_top_eigenvalue_checker.py`，编号论文为
`papers/tpc-318-top-eigenvalue-prime-shell-audit/`。它在 TPC-317 的同一 literal
operator 上直接读取 Gram 最大特征值；24 rows 由正反 shell 顺序、SciPy/NumPy 双路径、
残差与有限 Weyl guard 审计，16 个 adjacent normalized top-eigenvalue intervals 全部
严格下降。10/24 rows 的相对 top gap 小于 `0.01`，故 clustered eigenspace、normalization
law、unnormalized growing estimate 与 arithmetic cancellation 仍 open。该结果是
finite numerical audit，不能计入 power saving；Session-named evaluator files absent，
故不宣称 official Route-A/Route-B pass。

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

当前 TPC-317 入口：proof 为
`research/tpc-big-road/bridge_b_tpc317_schatten_four_checker.md`，checker 为
`tpc_bridge_b_tpc317_schatten_four_checker.py`，编号论文为
`papers/tpc-317-schatten-four-prime-shell-compression/`。它保留 TPC-316 的
deleted-diagonal centered prime-shell source operator，并用 PSD Gram 的
`sqrt(trace(G^2))` 替代 Frobenius `trace(G)` 作为有限 L2 envelope。在
`X=640,1280,2560`、`Q={24,36,54,80}`、`s={1,2}` 的 24 rows 上，16 个 adjacent
Schatten-4 intervals 严格下降，而同一 16 个 Frobenius intervals 严格上升；小面板
的两个 trace powers 由 exact rational arithmetic 锚定。这是 finite spectral
compression，不是 true operator-norm decay、growing arithmetic theorem、external
holdout 或 twin-prime proof；Session-named evaluator files absent，故不宣称 official pass。

```text
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
```

TPC-316 remains the immediate predecessor: its normalized Frobenius envelope rose
on 8/8 two-panel rows, motivating the trace-power replacement below.

```text
TPC316_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_LITERAL_ARITHMETIC_L2_ENVELOPE_PLUS_TWO_SCALE_OBSTRUCTION
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
TPC316_ROUND2_CLUE = REPLACE_THE_FROBENIUS_ENVELOPE_BY_A_GROWING_OPERATOR_OR_ARITHMETIC_CANCELLATION_ESTIMATE_WITHOUT_IMPORTING_A_POWER_CLAIM
```

上一位置 TPC-315 入口：proof 为
`research/tpc-big-road/bridge_b_tpc315_fresh_source_locked_weight_holdout.md`，checker 为
`tpc_bridge_b_tpc315_fresh_source_locked_weight_holdout_checker.py`，编号论文为
`papers/tpc-315-fresh-source-locked-weight-holdout/`。它先锁定 TPC-314 的 counting、
reduced-residue、von-Mangoldt 三-law menu，再把同一 literal engine 移到 fresh
`I=(640,1280]`，重新计算 8 个 Gram target rows。48 个 target/law cases 完成 directed
outward replay；24/24 fresh minima 严格低于 1，24/24 all-positive controls 严格高于 1。
minimum law order 有 3 类（6/1/1），positive control 有 2 类（6/2），形成 canonical
amplitude 的 finite obstruction。该 holdout 仍是 same-engine、非 external physical data；
uniform growing theorem、arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。Session-named evaluator files absent，故不宣称 official pass。

```text
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
```

当前 TPC-314 入口：proof 为
`research/tpc-big-road/bridge_b_tpc314_canonical_weight_law_audit.md`，checker 为
`tpc_bridge_b_tpc314_canonical_weight_law_audit_checker.py`，编号论文为
`papers/tpc-314-canonical-weight-law-audit/`。它冻结 TPC-312 的 8 个新
source-shell rows，固定审计 counting、reduced-residue 与 von-Mangoldt 三类正权；48 个
target/law cases 均完成 directed outward replay，24/24 minimum 严格低于 1，24/24
all-positive control 严格高于 1。log(p) 由 120 项 rational atanh enclosure 支持。
这是 same-engine、source-first 的有限 robustness audit；law-dependent amplitude、canonical
weighting、fresh physical holdout、uniform growing theorem、arithmetic `L2`、fixed-power
credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。Session-named evaluator files
absent，故不宣称 official Route-A/Route-B pass。

```text
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
```

当前 TPC-313 入口：proof 为
`research/tpc-big-road/bridge_b_tpc313_outward_budget_interval_certificate.md`，checker 为
`tpc_bridge_b_tpc313_outward_budget_interval_certificate_checker.py`，编号论文为
`papers/tpc-313-outward-budget-interval-certificate/`。它在 TPC-312 的 8 个新
source-shell rows 上扫描 first-feasible profile prefix，并在同一 prefix 上完成 16 个
exact rational primal/dual witnesses 与 `10^-36` outward interval replay。8/8 weighted
dual lower ratios `>5e-5`，8/8 all-positive primal upper ratios `<1e-5`。这是有限
source-first interface certificate；external weighting、fresh physical holdout、uniform
budget、arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍
OPEN/NONE。Session-named evaluator files absent，故不宣称 official pass。

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

当前 TPC-312 入口：proof 为
`research/tpc-big-road/bridge_b_tpc312_new_source_shell_separation.md`，checker 为
`tpc_bridge_b_tpc312_new_source_shell_separation_checker.py`，编号论文为
`papers/tpc-312-new-source-shell-separation-atlas/`。它把物理引擎移到新源区间
`I=(320,640]`，固定 `H=66`、`Q={24,36,54,80}`、exponent `{1,2}`，重建 8 个
rational Gram rows。84 个 shell targets 上共枚举 37,440 个 global-sign classes；8/8
Gram 在 `1000000007` 下满秩，8/8 rows 均有 minimum `<1` 与 all-positive maximum `>1`，
且两条 Q-spine order chains 均严格成立。这是同一锁定引擎内的新 source/parameter rows，
不是 external independent sample；profile-budget outward rounding、external weighting、
uniform budget、arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion
仍 OPEN/NONE。Session-named evaluator files absent，故不宣称 official pass。

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

当前 TPC-311 入口：proof 为
`research/tpc-big-road/bridge_b_tpc311_stratified_tau_holdout_replication.md`，checker 为
`tpc_bridge_b_tpc311_stratified_tau_holdout_replication_checker.py`，编号论文为
`papers/tpc-311-stratified-tau-holdout-replication/`。它固定一个两阶段规则：每个
`(transition, exponent, tau, radius)` design cell 内先 pool `LOW/BASE/HIGH` profile
ladders，再对 design cells 等权；calibration 为 `tau={0.25,0.5}`，confirmation 为
`tau={0.75}`。native `r=0` 的区间分别为
`[4.0615814676,4.0617439341]`（`LEFT`）与 `[0.6818442327,0.6818715070]`（`RIGHT`），
因此 strict class 反转；all-radius confirmation 跨阈值为 `UNRESOLVED`。这是同一
locked parent 的 parameter-slice obstruction，不是 fresh physical replication 或
externally timestamped preregistration；uniform budget、arithmetic `L2`、fixed-power
credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。Session-named evaluator files
absent，故不宣称 official pass。

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

此前 TPC-310 入口：proof 为
`research/tpc-big-road/bridge_b_tpc310_cross_holdout_aggregation_order.md`，checker 为
`tpc_bridge_b_tpc310_cross_holdout_aggregation_order_checker.py`，编号论文为
`papers/tpc-310-cross-holdout-aggregation-order/`。它冻结 TPC-309 的 162 个
profile/completion envelope observations，枚举 7 个非空 profile subsets 与 7 个非空
radius subsets 的 49 个 selectors，并对每个 selector计算 pooled-MSE、equal-case
arithmetic-ratio、geometric-ratio 三种 aggregate intervals，共 147 rows。全量 selector
上 pooled 为 `RIGHT`、balanced 为 `LEFT`、geometric 为 `RIGHT`，前两者区间分别为
`[0.2423655855,0.3112477031]` 与 `[5.2417686281,14.4871333704]`，形成远离阈值的
aggregation-order reversal。这是 finite weighting obstruction，不是 causal 或
asymptotic theorem；canonical weighting、formal directed rounding、uniform budget、
arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。
Session-named evaluator files absent，故不宣称 official pass。

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

TPC-310 的 strongest positive 是 exact finite selector/aggregation algebra 与
weighted-mean identity；strongest obstruction 是 pooled 与 equal-case arithmetic 在
full selector 上给出相反 strict classes。任何后续 preference claim 都需要先验固定的
weighting/stratification law 与独立 holdout replication。

此前 TPC-309 入口：proof 为
`research/tpc-big-road/bridge_b_tpc309_profile_prefix_shift_sensitivity.md`，checker 为
`tpc_bridge_b_tpc309_profile_prefix_shift_sensitivity_checker.py`，编号论文为
`papers/tpc-309-profile-prefix-shift-sensitivity/`。它承接 TPC-308 的 common-ambient
holdout 与 Hamming completion envelope，在同一个 19-prime cutoff pool 中测试相邻的
`LOW/BASE/HIGH` 三个 17-cutoff profile windows；shell、labels、alignment 与 completion
规则冻结，但每个 ladder 重新求 feasible prefix、frontier、budget 和 holdout。三窗口
共 54 profile cases、162 envelope observations，候选数 `108/558/1440`；BASE 恢复
TPC-308 的 `13/3/2`、`11/2/5`、`10/1/7`，LOW/HIGH 则改变 strict discordance 的位置
并扩大 unresolved band。这是 finite profile-sensitivity obstruction，不是 causal 或
asymptotic theorem；profile-independent preference、formal directed-rounding certificate、
uniform budget、arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion
仍 OPEN/NONE。Session-named evaluator files absent，故不宣称 official pass。

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

TPC-309 的 strongest positive 是同维度、相邻、source-backed profile perturbation 的
独立 finite replay；strongest obstruction 是 BASE 的 final-transition discordance 在
LOW/HIGH 下迁移或消失，且 radius-two 的 unresolved band 明显扩大。

此前 TPC-308 入口：

此前 TPC-308 入口：proof 为
`research/tpc-big-road/bridge_b_tpc308_adversarial_exclusive_completion_envelope.md`，checker 为
`tpc_bridge_b_tpc308_adversarial_exclusive_completion_envelope_checker.py`，编号论文为
`papers/tpc-308-adversarial-exclusive-completion-envelope/`。它承接 TPC-307 的 common-
ambient overlap-fit/exclusive-holdout diagnostic，冻结全部拟合对象，仅对独占 holdout
做 Hamming 半径 `0,1,2` 的 binary completion enumeration。Hamming protocol、candidate
count、fixed-prediction extrema、radius monotonicity、radius-zero recovery 与 sign
invariance 是 exact finite；18 cases 形成 54 observations、候选数 `36/186/480`，agreement
为 `13/3/2`、`11/2/5`、`10/1/7`，discordance `3→2→1` 且仍只在 `70->90,e=1`。这是
finite adversarial stability atlas，不是 causal 或 asymptotic theorem；formal interval
certificate、uniform budget、arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。Session-named evaluator files absent，故不宣称 official pass。

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

此前 TPC-307 入口与 marker block 保留如下，作为当前论文的直接上游记录。

当前 TPC-307 入口：proof 为
`research/tpc-big-road/bridge_b_tpc307_common_ambient_union_shell_holdout.md`，checker 为
`tpc_bridge_b_tpc307_common_ambient_union_shell_holdout_checker.py`，编号论文为
`papers/tpc-307-common-ambient-union-shell-holdout/`。它承接 TPC-306 的 interaction
diagnostic，把每个相邻 shell pair 放进同一个 union ambient `U`，在 overlap `O` 上
分别拟合 aligned left/right directional targets，并在 `E_left,E_right` 上做 withheld
exclusive holdout。partition、overlap-only fit、holdout separation、global-sign
invariance 与 common-prefix feasibility 是 exact finite；18 cases、36 directional fits、
54 normalizer rows 的 numerical replay 为 `13 concordant / 3 discordant / 2 unresolved`，
且三处 discordance 全在 `Q=70->90`, exponent 1 的三个 tolerance。这是 finite
completion-stability diagnostic/obstruction，不是 causal 或 asymptotic theorem；formal
directed-rounding enclosure、uniform budget、arithmetic `L2`、fixed-power credit、full
Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC307_ROUTE_ADVANCE = YES_SCOPED_COMMON_AMBIENT_DIRECTIONAL_HOLDOUT_DIAGNOSTIC
TPC307_COMMON_AMBIENT_UNION = PROVED_EXACT_FINITE
TPC307_OVERLAP_ONLY_FIT = PROVED_EXACT_FINITE
TPC307_EXCLUSIVE_HOLDOUT = PROVED_EXACT_FINITE
TPC307_GLOBAL_SIGN_INVARIANCE = PROVED_EXACT_FINITE
TPC307_COMMON_PREFIX_FEASIBILITY = PROVED_EXACT_FINITE
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
TPC306_ROUND2_CLUE = TEST_COMMON_AMBIENT_UNION_SHELL_COMPLETIONS_AND_INTERACTION_STABILITY_BEFORE_ANY_GROWING_TARGET_PREFERENCE_CLAIM
```

当前 TPC-305 入口：proof 为
`research/tpc-big-road/bridge_b_tpc305_counterfactual_transported_label_budget.md`，checker 为
`tpc_bridge_b_tpc305_counterfactual_transported_label_budget_checker.py`，编号论文为
`papers/tpc-305-counterfactual-transported-label-budget/`。它承接 TPC-304 的
overlap fracture，在每个 full physical operator 内只替换 target：公共素数上使用
optimally aligned neighboring label，off-overlap 保留 native label，再以 native 与
transported target 的共同 feasible prefix 重算 budget。18 个 cases、36 个 operator
tables 在三种 normalization 下均有严格一致的 orientation；中心 `Q=60->70` 为
right-label-cheaper `5/6`、home `1/6`，且 same-prefix `3/3` 全为 right。该结果是
finite partial counterfactual control，不是 causal separation；operator interaction、
uniform profile-budget growth、arithmetic `L2`、full Gate B 与 twin-prime conclusion
仍 OPEN/NONE。

```text
TPC305_ROUTE_ADVANCE = YES_SCOPED_COUNTERFACTUAL_TARGET_CONTROL
TPC305_FIXED_OPERATOR_TARGET_SWAP = PROVED_EXACT_FINITE
TPC305_COUNTERFACTUAL_BUDGET_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_CASES_36_TABLES
TPC305_MIDDLE_TARGET_ORIENTATION = NUMERICALLY_CERTIFIED_FINITE_RIGHT_LABEL_CHEAPER_5_OF_6
TPC305_MIDDLE_SAME_PREFIX_ORIENTATION = NUMERICALLY_CERTIFIED_FINITE_RIGHT_LABEL_CHEAPER_3_OF_3
TPC305_CAUSAL_SEPARATION = PARTIAL_COUNTERFACTUAL_ONLY
TPC305_OPERATOR_INTERACTION_TERM = OPEN
TPC305_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC305_FIXED_POWER_CREDIT = 0
TPC305_FULL_GATE_B = OPEN
TPC305_TWIN_PRIME_RESULT = NONE
TPC305_ROUND2_CLUE = TEST_TWO_WAY_OPERATOR_HOLDOUT_AND_INTERACTION_TERM_BEFORE_ANY_CAUSAL_TARGET_OPERATOR_CLAIM
```

此前 TPC-304 入口：proof 为
`research/tpc-big-road/bridge_b_tpc304_overlapping_shell_label_transport.md`，checker 为
`tpc_bridge_b_tpc304_overlapping_shell_label_transport_checker.py`，编号论文为
`papers/tpc-304-overlapping-shell-label-transport/`。它承接 TPC-303 的 fixed-source
cardinality obstruction，把相邻 `Q=50,60,70,90` shells 限制到公共素数并消除
global-sign gauge。六个 transport rows 的三组平均 aligned correlation 为
`1/2,1/11,1/2`；`Q=60->70` 是唯一 fracture，同时 TPC-303 的 budget descents 为
`3,15,3`、same-prefix descents 为 `0,9,0`。这是 finite localization crosswalk，
不是 causal separation；counterfactual transported-label budget、arithmetic `L2`、
fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

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

此前 TPC-303 入口：proof 为
`research/tpc-big-road/bridge_b_tpc303_cardinality_monotonicity_obstruction.md`，checker 为
`tpc_bridge_b_tpc303_cardinality_monotonicity_obstruction_checker.py`，编号论文为
`papers/tpc-303-cardinality-monotonicity-obstruction/`。它承接 TPC-302 的 finite
growing-shell budget-gap audit，在固定 `(N,H,z)=(512,58,5)` 的 `Q=50,60,70,90`
spine 上审计 cardinality-only budget growth。54 个 adjacent transitions 中区间严格
认证 21 descent、33 ascent、0 unresolved；18/18 parameter series nonmonotone，9 个
descent 保持相同 common profile prefix。这是 finite scoped obstruction；uniform
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

此前 TPC-301 入口：proof 为
`research/tpc-big-road/bridge_b_tpc301_budget_gap_robustness_audit.md`，checker 为
`tpc_bridge_b_tpc301_budget_gap_robustness_audit_checker.py`，编号论文为
`papers/tpc-301-budget-gap-robustness-audit/`。它承接 TPC-300 的 finite native
dual certificate，在 `tau=1/4,1/2,3/4` 和 common weighted-selected prefix 下审计
weighted/all-positive budget gap。18/18 rows 在三档容差均有 gap `>10`，最小值为
`155.1685/69.9448/39.2637`；三种 source normalization 下 weighted common budget
均在 54/54 cases 超过 `3e-5`。这是 finite robustness advance；growing profile-budget、
arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

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

此前 TPC-300 入口：proof 为
`research/tpc-big-road/bridge_b_tpc300_native_budget_dual_certificate.md`，checker 为
`tpc_bridge_b_tpc300_native_budget_dual_certificate_checker.py`，编号论文为
`papers/tpc-300-native-budget-dual-certificate/`。它承接 TPC-299 的 native budget
frontier，对任意正 ridge parameter rho 严格证明 dual lower bound
`D_rho=(||b||^2-R^2-b^T Vc_rho)/rho`，active finite frontier 上强对偶，并校正
`mu=1/rho`。在 18-row、1,380-edge grid 上，72 个 exact rational dual witnesses
全部通过 independent source-first replay；最小 dual/primal lower-bound ratio 为
约 `0.9999999999999623`，weighted threshold 的 `9e-5/5e-4/1e-3` 计数为
`18/15/14`，full-prefix `1e-3` obstruction 为 `11/18`。这是 finite restricted
structural advance；growing budget、arithmetic `L2`、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE，fixed-power credit 为 0。

```text
TPC300_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_NATIVE_BUDGET_DUALITY_AND_RECIPROCAL_MULTIPLIER_CORRECTION_PLUS_NUMERICALLY_CERTIFIED_FINITE_RATIONAL_DUAL_WITNESS_ATLAS
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
TPC300_STATUS = PROVED_EXACT_FINITE_NATIVE_BUDGET_DUALITY_AND_RECIPROCAL_MULTIPLIER_CORRECTION_PLUS_NUMERICALLY_CERTIFIED_FINITE_RATIONAL_DUAL_WITNESS_ATLAS
TPC300_ROUND2_CLUE = HOSTILE_TEST_THE_DUAL_BUDGET_GAP_ACROSS_TOLERANCE_AND_SOURCE_NORMALIZATION_LADDERS
```

此前 TPC-299 入口：proof 为
`research/tpc-big-road/bridge_b_tpc299_native_profile_budget_frontier.md`，checker 为
`tpc_bridge_b_tpc299_native_profile_budget_frontier_checker.py`，编号论文为
`papers/tpc-299-native-profile-budget-frontier/`。它承接 TPC-298 的 17-profile angle/
dimension ladder，令 `M_k=U_k^T U_k`，把目标容差编译成实际 source norm frontier
`B_(k,tau)(b)=min{c^T M_k c: ||V_kc-b||<=tau||b||}`。严格证明 KKT/ridge 表达、
budget feasibility 与 nested-prefix monotonicity。继承的 18-row/1,380-edge finite
audit 在 `tau=1/2` 下得到 weighted threshold budget `>9e-5`（18/18）、`>1e-3`
（14/18），full prefix `>1e-3`（11/18）；positive control `<1e-4`（18/18），
weighted/positive gap `>20`（18/18）。这是 finite restricted-profile obstruction，
不是 growing budget theorem；arithmetic `L2`、full Gate B 与 twin-prime conclusion
仍 OPEN/NONE，fixed-power credit 为 0。

```
TPC299_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_PROFILE_BUDGET_KKT_FRONTIER_PLUS_NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_OBSTRUCTION_ATLAS
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
TPC299_STATUS = PROVED_EXACT_FINITE_PROFILE_BUDGET_KKT_FRONTIER_PLUS_NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_OBSTRUCTION_ATLAS
TPC299_ROUND2_CLUE = TEST_BUDGET_CONSTRAINED_PROFILE_FRONTIER_ON_GROWING_SHELLS_AND_SOURCE_NORMALIZATION
```

当前 TPC-298 入口：proof 为
`research/tpc-big-road/bridge_b_tpc298_profile_angle_dimension_ladder.md`，checker 为
`tpc_bridge_b_tpc298_profile_angle_dimension_ladder_checker.py`，编号论文为
`papers/tpc-298-profile-angle-dimension-ladder/`。它承接 TPC-297 的四维 literal
cutoff span，按 cutoff 排序形成 17-profile prefix ladder。严格证明
`V_k=A^T U_k` 的 projection/principal-angle identity 与 nested-prefix monotonicity；
双模 replay 在 18 rows 上完成 306 个 prefix-rank checks。70 位独立 replay 显示 weighted
target 的 half-RMS dimension ratio 在 18/18 行至少 `2/3`，all-positive control 在
18/18 行至多 6 个 profiles，且最后一个有限 prefix 在 18/18 行达到有限 target space。
这是 finite dimension/angle advance，不是 growing native theorem；conditioning/source
budget growth、arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE，
fixed-power credit 为 0。Session-named evaluator 文件缺失，当前仍只记录 local
fail-closed validation。

```text
TPC298_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_PRINCIPAL_ANGLE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_PROFILE_DIMENSION_LADDER
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
TPC298_ROUND2_CLUE = TEST_WEIGHTED_PROFILE_DIMENSION_AGAINST_LEAST_NORM_SOURCE_BUDGET_AND_CONDITIONING
```

此前 TPC-297 入口：proof 为
`research/tpc-big-road/bridge_b_tpc297_literal_source_profile_span_audit.md`，checker 为
`tpc_bridge_b_tpc297_literal_source_profile_span_audit_checker.py`，编号论文为
`papers/tpc-297-literal-source-profile-span-audit/`。它承接 TPC-296 的冻结一维
`span{A^T beta}` obstruction，改用四个 source-side literal cutoff profiles
`beta_z(t)=lambda(t)-sum_{d<=z,d|t}mu(d)`（`z=3,5,7,11`）。严格证明受限像
`V=A^T U` 的 projection identity 与 nested-span monotonicity；两模 rank replay 在
18 rows 上得到 rank `3+17*4`。70 位独立 replay 显示 all-positive target 的 RMS 在
18/18 行不超过 `0.15`，weighted target 在 17/17 个大 shell 上仍至少 `0.6`。
这确认四维 source geometry 有实质正信息，但尚未解释 weighted direction；growing
dimension、principal angles、source budget、arithmetic `L2`、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE，fixed-power credit 为 0。Session-named evaluator 文件缺失，
当前仍只记录 local fail-closed validation。

```text
TPC297_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_RESTRICTED_PROFILE_PROJECTION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_FOUR_CUTOFF_PROFILE_ATLAS
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
TPC297_ROUND2_CLUE = TEST_NATIVE_PROFILE_PRINCIPAL_ANGLES_AND_MINIMUM_DIMENSION
```

当前 TPC-296 入口：proof 为
`research/tpc-big-road/bridge_b_tpc296_source_norm_budget_interface.md`，checker 为
`tpc_bridge_b_tpc296_source_norm_budget_interface_checker.py`，编号论文为
`papers/tpc-296-source-norm-budget-interface/`。它承接 TPC-295 的 unrestricted finite
source image，令 `G=A^T A`，严格证明 least-norm source cost
`S_A(b)=b^T G^(-1)b`、预算可行性的 iff criterion，以及
`S_A(b)(b^TGb)>=(b^Tb)^2` 的 source-energy tradeoff。70 位独立 replay 在 18 rows /
1,380 edges 上得到 weighted/min-cut/all-positive targets 的 unrestricted budget ratio
均低于声明的 `1e-3`（18/18）；同时 weighted/min-cut 到冻结 ray `span{A^T beta}` 的
RMS 均至少 `0.9`（18/18）。这把坑从“是否有 ambient source witness”推进到“native
profile 是否有足够维数与 growing budget”；native profile、arithmetic `L2`、full Gate B
与 twin-prime conclusion 仍 OPEN/NONE，fixed-power credit 为 0。Session-named
Route-A/Route-B evaluator 文件缺失，当前只记录本地 fail-closed validation。

```text
TPC296_MAXIMUM_CLAIM = PROVED_EXACT_LEAST_NORM_SOURCE_BUDGET_AND_SOURCE_ENERGY_TRADEOFF_PLUS_NUMERICALLY_CERTIFIED_FINITE_COST_PROFILE_ATLAS
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
TPC296_ROUND2_CLUE = TEST_RESTRICTED_PROFILE_DIMENSION_AND_GROWING_SOURCE_BUDGET
```

当前 TPC-295 入口：proof 为
`research/tpc-big-road/bridge_b_tpc295_source_correlation_image_audit.md`，checker 为
`tpc_bridge_b_tpc295_source_correlation_image_audit_checker.py`，编号论文为
`papers/tpc-295-source-correlation-image-audit/`。它承接 TPC-294 的 ambient weighted
sign minimizer，令 physical shell vectors 为 rational matrix `A` 的 columns，严格证明
`G=A^T A` full rank 时 source-correlation map `A^T:Q^I -> Q^S` surjective，并给出
least-norm witness `h=A G^(-1)b`。两个独立模数在继承的 18 rows 全部给出 nonzero
determinants；因此 18/18 unrestricted finite source images surjective，TPC-294 weighted
minimizer、unit-edge max-cut 与 all-positive targets 均 18/18 可达。该结论明确限定在
unrestricted rational source coordinates；native profile、witness norm/growing control、
literal arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE，fixed-power
credit 为 0。

```text
TPC295_MAXIMUM_CLAIM = PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION_SURJECTIVITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_MODULAR_FULL_RANK_ATLAS
TPC295_ROUTE_ADVANCE = YES_SCOPED_AMBIENT_SIGN_TARGETS_TO_UNRESTRICTED_FINITE_SOURCE_IMAGE
TPC295_FULL_RANK_IMPLICATION = PROVED_EXACT_FINITE
TPC295_LEAST_NORM_WITNESS_FORMULA = PROVED_EXACT_FINITE
TPC295_MODULAR_FULL_RANK_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_TWO_MODULI
TPC295_UNRESTRICTED_SOURCE_CORRELATION_SURJECTIVITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18
TPC295_WEIGHTED_MINIMIZER_SOURCE_REALIZABILITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_UNRESTRICTED
TPC295_NATIVE_RESTRICTED_PROFILE = OPEN_LITERAL_SOURCE
TPC295_SOURCE_WITNESS_NORM = OPEN
TPC295_GROWING_SOURCE_IMAGE = OPEN
TPC295_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC295_FIXED_POWER_CREDIT = 0
TPC295_FULL_GATE_B = OPEN
TPC295_TWIN_PRIME_RESULT = NONE
TPC295_STATUS = PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION_SURJECTIVITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_MODULAR_FULL_RANK_ATLAS
TPC295_ROUND2_CLUE = TEST_SOURCE_NORM_COST_AND_RESTRICTED_NATIVE_PROFILE_IMAGE
```

当前 TPC-294 入口：proof 为
`research/tpc-big-road/bridge_b_magnitude_weighted_signed_rayleigh_atlas.md`，checker 为
`tpc_bridge_b_magnitude_weighted_signed_rayleigh_atlas_checker.py`，编号论文为
`papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/`。它承接 TPC-293 的 unit-edge
signed max-cut，把 exact Gram magnitudes 恢复到 trace-normalized equal-sign quadratic
objective。严格证明 identity、Gram nonnegativity 与 finite global enumeration；18-row
grid 上 18/18 weighted minima `<1`、18/18 all-positive states `>1`，且 18/18 weighted
optima 与 max-cut label 不同。该结果仍是 frozen finite/source-unconstrained diagnostic；
source-native image、growing weighted theorem、literal arithmetic `L2`、full Gate B 与
twin-prime conclusion 仍 OPEN/NONE，fixed-power credit 为 0。

```text
TPC294_MAXIMUM_CLAIM = PROVED_EXACT_TRACE_NORMALIZED_SIGNED_QUADRATIC_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_GLOBAL_SIGN_ATLAS
TPC294_ROUTE_ADVANCE = YES_SCOPED_FINITE_SIGN_LAYER_TO_MAGNITUDE_WEIGHTED_RAYLEIGH_LAYER
TPC294_TRACE_NORMALIZED_IDENTITY = PROVED_EXACT_FINITE
TPC294_GLOBAL_SIGN_ENUMERATION = PROVED_EXACT_FINITE
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
TPC294_ROUND2_CLUE = TEST_SOURCE_IMAGE_OF_WEIGHTED_OPTIMAL_SIGN_PATTERNS_AND_DIFFUSE_SIGNED_WEIGHTS
```

当前 TPC-293 入口：proof 为
`research/tpc-big-road/bridge_b_signed_shell_maxcut_atlas.md`，checker 为
`tpc_bridge_b_signed_shell_maxcut_atlas_checker.py`，编号论文为
`papers/tpc-293-signed-shell-maxcut-atlas/`。它承接 TPC-292 的 triangle parity，把
whole prime shell 编译为 signed complete graph。严格证明 all-positive `K_m` benchmark
`floor(m^2/4)`、frustration complement 与 switching invariance；同一 18-row grid 的
1,380 edges 上，17 rows all-positive，唯一 crossover row 由 3 个 negative edges 得到
`+3` sign-only gain。总 max favorable / minimum unsatisfied 为 `744/636`。该有限 gain
尚未恢复 Gram magnitudes，故 magnitude-weighted Rayleigh、growing theorem、source-native
arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC293_MAXIMUM_CLAIM = PROVED_EXACT_ALL_POSITIVE_MAXCUT_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGNED_SHELL_FRUSTRATION_ATLAS
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
TPC293_ROUND2_CLUE = TEST_MAGNITUDE_WEIGHTED_SIGNED_RAYLEIGH_AND_SOURCE_IMAGE
```

当前 TPC-292 入口：proof 为
`research/tpc-big-road/bridge_b_three_prime_sign_frustration_atlas.md`，checker 为
`tpc_bridge_b_three_prime_sign_frustration_atlas_checker.py`，编号论文为
`papers/tpc-292-three-prime-sign-frustration-atlas/`。它承接 TPC-291 的 pairwise Schur
cancellation，严格证明三角 edge-sign parity criterion 与 three-vector Schur residual。
同一 18-row literal grid 的 5,727 个 triples 中，5,718 个 sign-frustrated、9 个
anti-alignable，全部 normalized volumes 为正；late `(512,58,90,5,2)` row 的 680 个
triples 全为 `+++`。这确认 pairwise optimum 的主要新障碍是 cycle compatibility；
growing theorem、source-native arithmetic `L2`、fixed-power credit、full Gate B 与
twin-prime conclusion 仍 OPEN/NONE。

```text
TPC292_MAXIMUM_CLAIM = PROVED_EXACT_TRIANGLE_SIGN_PARITY_AND_THREE_VECTOR_SCHUR_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGN_FRUSTRATION_ATLAS
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
TPC292_ROUND2_CLUE = TEST_SIGNED_GRAPH_MAXCUT_AND_MULTI_PRIME_RAYLEIGH_COMPATIBILITY
```

当前 TPC-291 入口：proof 为
`research/tpc-big-road/bridge_b_signed_schur_cancellation_atlas.md`，checker 为
`tpc_bridge_b_signed_schur_cancellation_atlas_checker.py`，编号论文为
`papers/tpc-291-signed-schur-cancellation-atlas/`。它承接 TPC-290 的 weighted-Gram
firewall，对每个 nonzero cross-prime pair 精确证明 Schur projection residual
`1-Gamma`、signed two-vector Rayleigh minimum `1-sqrt(Gamma)`，并把 Gram sign 编译为
opposite-sign / same-sign cancellation cost。在同一 18-row grid 的 1,380 个 pairs 上，
exact-rational replay 得到 1,377 positive、3 negative、0 zero；残差阈值
`1/2,1/4,1/10` 的计数为 `1074/852/477`，最佳 pair `(173,179)` 的 residual 约
`0.0151239493`。这把晚期 coherence island 接到明确的 pairwise signed direction，
但 multi-prime signed reassembly、source-native arithmetic `L2`、fixed-power credit、
full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC291_MAXIMUM_CLAIM = PROVED_EXACT_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_COHERENCE_TO_CANCELLATION_ATLAS
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
TPC291_ROUND2_CLUE = TEST_SOURCE_RESTRICTED_DIFFUSE_WEIGHTS_OR_MULTI_PRIME_SIGNED_NULL_DIRECTIONS
```

当前 TPC-290 入口：proof 为
`research/tpc-big-road/bridge_b_adaptive_shell_weighting_obstruction.md`，checker 为
`tpc_bridge_b_adaptive_shell_weighting_obstruction_checker.py`，编号论文为
`papers/tpc-290-adaptive-shell-weighting-obstruction/`。它承接 TPC-289 的 physical
output Gram，把 adaptive weighting 写成
`R(w)=||sum_q w_q g_q||^2/sum_q w_q^2 d_q`，严格证明非负权重在全正 cross-Gram block
中不能产生 decay，并证明 effective-support lower bound
`R(w)>=1+eta*delta*(kappa(w)-1)`。同一 18-row grid 上 3 个 full-support policies 共
54/54 amplified，18/18 leave-one-out minima 仍 amplified；唯一的 3 个 subunit equal-pair
witness 全在早期 sign-flip row。growing diffuse weighted theorem、literal arithmetic `L2`、
fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC290_MAXIMUM_CLAIM = PROVED_EXACT_NONNEGATIVE_WEIGHTED_GRAM_NO_DECAY_BOUND_PLUS_NUMERICALLY_CERTIFIED_FINITE_ADAPTIVE_WEIGHTING_OBSTRUCTION
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
TPC290_ROUND2_CLUE = TEST_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_OR_SOURCE_RESTRICTED_DIFFUSE_WEIGHTS
```

当前 TPC-289 入口：proof 为
`research/tpc-big-road/bridge_b_cross_prime_gram_coherence.md`，checker 为
`tpc_bridge_b_cross_prime_gram_coherence_checker.py`，编号论文为
`papers/tpc-289-cross-prime-gram-coherence/`。它承接 TPC-288 的完整 physical output
Gram，在同一个 literal operator/source 上定义 `Gamma_(q,r)=G_(q,r)^2/(G_(q,q)G_(r,r))`
并证明 exact conditional accumulation bound。18 个 rows、1,380 个 unordered pairs
中 17/18 rows pairwise positive；早期 `(256,38,27,5,1)` 有 3 个 negative pairs 和
near-zero coherence，8 个 late-shell rows 通过 `eta=3/5,delta=4/5` strong block，
18/18 rows energy amplification。uniform source-restricted/growing-shell coherence、
arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC289_MAXIMUM_CLAIM = PROVED_EXACT_NORMALIZED_GRAM_COHERENCE_ACCUMULATION_BOUND_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGN_PHASE_DIAGRAM
TPC289_ROUTE_ADVANCE = YES_SCOPED_EXACT_COHERENCE_ENVELOPE_AND_FINITE_SIGN_PHASE_DIAGRAM
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
TPC289_ROUND2_CLUE = TEST_ADAPTIVE_SHELL_WEIGHTING_OR_SOURCE_RESTRICTED_COHERENCE_BEYOND_FINITE_BLOCK
```

当前 TPC-288 入口：proof 为
`research/tpc-big-road/bridge_b_growing_shell_gram_obstruction.md`，checker 为
`tpc_bridge_b_growing_shell_gram_obstruction_checker.py`，编号论文为
`papers/tpc-288-growing-shell-gram-obstruction/`。它沿用 TPC-287 的 literal physical
deleted-diagonal operator，把每个 prime component 的完整 output vector 保留下来并构造
source-output Gram。finite operator/output/attachment additivity、Gram PSD 与
`1^T G 1=||g_shell||^2` 均严格证明；34 个 growth/control rows（最大 shell 17 个素数）
中 34/34 output Gram full rank，6/6 selected aggregate active matrices full rank；所有
34 行 energy ratio 都大于 1，13 行同时有 scalar retention upper `<1/10`。这严格封住
“scalar cancellation 自动支付 physical `L2`”的 shortcut；uniform growing-shell Gram
bound、source-native arithmetic `L2`、fixed-power credit、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。

```text
TPC288_MAXIMUM_CLAIM = PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_SHELL_FULL_RANK_OBSTRUCTION
TPC288_ROUTE_ADVANCE = YES_SCOPED_GROWING_SHELL_GRAM_OBSTRUCTION_AND_FULL_RANK_AUDIT
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
TPC288_STATUS = PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_SHELL_FULL_RANK_OBSTRUCTION
TPC288_ROUND2_CLUE = TEST_SOURCE_NATIVE_CROSS_PRIME_GRAM_BOUNDS_BEYOND_FINITE_FULL_RANK_OBSTRUCTION
```

当前 TPC-287 入口：proof 为
`research/tpc-big-road/bridge_b_prime_shell_cancellation_depth.md`，checker 为
`tpc_bridge_b_prime_shell_cancellation_depth_checker.py`，编号论文为
`papers/tpc-287-prime-shell-cancellation-depth/`。它承接 TPC-286 的 diagonal-split
ledger，把 physical deleted-diagonal shell 按 prime 拆成 `g_q`，严格证明 finite
shell 与 linear attachment 的 `g_shell=sum_q g_q`、`C_shell=sum_q C_q`。七个明确声明的
shell anchors 覆盖 1--7 个素数，配合六个 frozen source baselines 与两个 exponents，
得到 84 rows / 336 components：336/336 intervals sign-separated，57 mixed-sign rows，
retention upper `<1/2/<1/4/<1/10` 分别为 31/22/8，leave-one-out 有 48 个非零 sign
flips 与 12 个 zero remainders。这是 finite cancellation-depth map，不是 growing-shell
theorem；source-control uniformity、arithmetic `L2`、fixed-power credit、full Gate B 与
twin-prime conclusion 仍 OPEN/NONE。

```text
TPC287_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_SHELL_ADDITIVE_ATTACHMENT_DECOMPOSITION_PLUS_NUMERICALLY_CERTIFIED_FINITE_CANCELLATION_DEPTH_LEDGER
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
TPC287_ROUND2_CLUE = TEST_CANCELLATION_STABILITY_UNDER_GROWING_SHELL_AND_SOURCE_CONTROLS
```

当前 TPC-286 入口：proof 为
`research/tpc-big-road/bridge_b_diagonal_deletion_attachment_ledger.md`，checker 为
`tpc_bridge_b_diagonal_deletion_attachment_ledger_checker.py`，编号论文为
`papers/tpc-286-diagonal-deletion-attachment-ledger/`。它承接 TPC-285，将
diagonal-including prime-shell output、显式 diagonal correction 与 physical
deleted-diagonal output 精确拆分：`g_phys=g_full-g_diag`，并由 attachment linearity
得到 `C_phys=C_full-C_diag`。TPC-284 的全部 72 个 controls 均完成三分量 interval
ledger：full 为 49 negative/23 positive，diagonal 为 34/38，physical 为 60/12；
15 行 full/physical sign flips，30 行 diagonal-opposition，21 行严格 diagonal
dominance。该 finite result 不等于 asymptotic dominance、signed full-shell cancellation
或 arithmetic `L2`；fixed-power credit 与 full Gate B 仍 OPEN/NONE。

```text
TPC286_MAXIMUM_CLAIM = PROVED_EXACT_LINEAR_DIAGONAL_DELETION_ATTACHMENT_SPLIT_PLUS_NUMERICALLY_CERTIFIED_FINITE_DIAGONAL_SENSITIVITY_LEDGER
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
TPC286_ROUND2_CLUE = SEEK_SIGNED_FULL_SHELL_CANCELLATION_AFTER_DIAGONAL_ATTACHMENT_LEDGER
```

当前 TPC-285 入口：proof 为
`research/tpc-big-road/bridge_b_prime_shell_residue_rank_obstruction.md`，checker 为
`tpc_bridge_b_prime_shell_residue_rank_obstruction_checker.py`，编号论文为
`papers/tpc-285-prime-shell-residue-rank-obstruction/`。它承接 TPC-284 的控制图谱，
对奇素数 `q` 精确证明 centered residue block 的 `q-2` mode factorization，并证明
physical deleted-diagonal block 在 full class coverage 下恢复 full active rank；20 个
registered prime/exponent rows 的 kernel Schur blocks 进一步通过模 `1000000007` 的
独立 full-rank witness。该结果关闭 low-rank residue shortcut，但不等于 signed
full-shell cancellation 或 arithmetic `L2`；fixed-power credit 与 full Gate B 仍 OPEN/NONE。

```text
TPC285_MAXIMUM_CLAIM = PROVED_EXACT_CENTERED_RESIDUE_FACTORIZATION_AND_DELETED_DIAGONAL_FULL_RANK_PLUS_NUMERICALLY_CERTIFIED_KERNEL_RANK
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
TPC285_ROUND2_CLUE = SEPARATE_RESIDUE_MODE_FACTORIZATION_FROM_DELETED_DIAGONAL_AND_KERNEL_RANK_BEFORE_LITERAL_L2
```

当前 TPC-284 入口：proof 为
`research/tpc-big-road/bridge_b_admissible_source_control_atlas.md`，checker 为
`tpc_bridge_b_admissible_source_control_atlas_checker.py`，编号论文为
`papers/tpc-284-admissible-source-control-atlas/`。它承接 TPC-283 的 unrestricted
zeroing radius，声明 `H±2`、`z±1`、`Q±1` 六类 schedule controls，在六个 scales、
两个 exponents 上完成 72-row literal-source atlas：60 negative、12 positive、0
crossing，但有 8 个相对 baseline 的 sign flips，最弱 controlled `rho^2` 下界约
`1.4118e-5`。这是有限控制图谱与 scoped sign-stability obstruction，不是 exhaustive
admissible-source theorem 或 asymptotic stability；arithmetic `L2`、fixed-power credit
与 full Gate B 仍 OPEN/NONE。

```text
TPC284_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_ADMISSIBLE_CONTROL_ATLAS_PLUS_SIGN_FLIP_OBSTRUCTION
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
TPC284_ROUND2_CLUE = COMPILE_PRIME_SHELL_CONTROL_CONSTRAINTS_BEFORE_ANY_ASYMPTOTIC_STABILITY_CLAIM
```

当前 TPC-283 入口：proof 为
`research/tpc-big-road/bridge_b_source_attachment_stability_radius.md`，checker 为
`tpc_bridge_b_source_attachment_stability_radius_checker.py`，编号论文为
`papers/tpc-283-source-attachment-stability-radius/`。它证明 source representative 到
zero-attachment hyperplane 的 exact radius formula，并将 TPC-282 的 12-row intervals
转成 `12/12` under `30%`、`6/12` under `10%` 的 finite vulnerability certificate。
该 adversary 只在 unrestricted projected Hilbert space 中成立，不替代 admissible
literal-source theorem；arithmetic `L2`、fixed-power credit 与 full Gate B 仍 OPEN/NONE。

```text
TPC283_MAXIMUM_CLAIM = PROVED_EXACT_HILBERT_SOURCE_ZEROING_RADIUS_PLUS_NUMERICALLY_CERTIFIED_FINITE_VULNERABILITY_AUDIT
TPC283_ROUTE_ADVANCE = YES_SCOPED_EXACT_ZEROING_RADIUS_AND_FINITE_VULNERABILITY_AUDIT
TPC283_ZEROING_RADIUS = PROVED_EXACT
TPC283_FINITE_VULNERABILITY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC283_UNRESTRICTED_ADVERSARY = INFORMATION_MODEL_ONLY
TPC283_ADMISSIBLE_LITERAL_SOURCE_STABILITY = OPEN
TPC283_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC283_FIXED_POWER_CREDIT = 0
TPC283_FULL_GATE_B = OPEN
TPC283_TWIN_PRIME_RESULT = NONE
TPC283_ROUND2_CLUE = TEST_ADMISSIBLE_LITERAL_SOURCE_CONTROLS_AFTER_UNRESTRICTED_ZEROING_OBSTRUCTION
```

当前 TPC-282 入口：proof 为
`research/tpc-big-road/bridge_b_literal_source_attachment_audit.md`，checker 为
`tpc_bridge_b_literal_source_attachment_audit_checker.py`，编号论文为
`papers/tpc-282-literal-source-attachment-audit/`。它在 frozen literal V59 operator
上直接计算 `C=<w_perp,(I-P_3)A beta>` 与
`rho^2=C^2/(||w_perp||^2||S||^2)`；12 行全部 sign-separated（11 negative、1 positive），
但最小 `rho^2` 约 `3.36e-5`。因此 finite source identification 已锁定，uniform
asymptotic nondegeneracy、literal arithmetic `L2`、fixed-power credit 与 full Gate B
仍 OPEN/NONE。

```text
TPC282_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK_PLUS_ASYMPTOTIC_NONDEGENERACY_OPEN
TPC282_ROUTE_ADVANCE = YES_SCOPED_FINITE_SOURCE_ATTACHMENT_AUDIT
TPC282_SOURCE_ATTACHMENT = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC282_SOURCE_SIGN = 11_NEGATIVE_1_POSITIVE_FINITE
TPC282_UNIFORM_ASYMPTOTIC_NONDEGENERACY = OPEN
TPC282_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC282_FIXED_POWER_CREDIT = 0
TPC282_FULL_GATE_B = OPEN
TPC282_TWIN_PRIME_RESULT = NONE
TPC282_ROUND2_CLUE = QUANTIFY_SOURCE_ATTACHMENT_STABILITY_RADIUS_AND_SIGN_FLIPS
```

当前 TPC-281 入口：proof 为
`research/tpc-big-road/bridge_b_arithmetic_l2_gate_b_interface_audit.md`，checker 为
`tpc_bridge_b_arithmetic_l2_gate_b_interface_audit_checker.py`，编号论文为
`papers/tpc-281-arithmetic-l2-gate-b-interface-audit/`。它把 arithmetic `L2` 明确
类型化为 `A_X:H_X -> ell^2(I_X)` 的 conditional operator hypothesis，并由
`D<=d_+X^a`、`G/D<=Q_X` 精确推出
`||A_X S||_2^2<=K^2 X^(-2sigma)Q_XD`；接入 TPC-280 的 two-term budget 后得到
`K^2d_+(B+ell/d)X^(a-2sigma-kappa)`。同时，`R^2` 中 equal-norm 的 parallel/
perpendicular functionals 对同一 packet sum 给出 `G^2/0` attachment，证明 geometry
与 operator norm 不能替代 typed attachment/nondegeneracy。4+4 个 exact fixtures 与
TPC-280 的 12-row transfer 通过，但 literal source `L2`、attachment theorem、fixed-power
credit 与 full Gate B 仍 OPEN/NONE。

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

strongest positive result：typed `L2` 到 output-energy 的 exact conditional interface；
strongest obstruction：equal norm/geometry 仍允许 zero attachment；open theorem：literal
source arithmetic `L2` 与 typed attachment nondegeneracy。

当前 TPC-280 入口：proof 为
`research/tpc-big-road/bridge_b_leakage_aware_endpoint_compiler.md`，checker 为
`tpc_bridge_b_leakage_aware_endpoint_compiler_checker.py`，编号论文为
`papers/tpc-280-leakage-aware-endpoint-compiler/`。它从
`D>=dX^a` 与 `G<=B X^(-gamma)D+ell X^(a-delta)` 精确编译出 two-term normalized
bound、`kappa=min(gamma,delta)` dominant exponent、signed-margin half-exponent
与 strict `1/400` endpoint test；equality family 证明 information-model sharpness。
6+4+4 个 rational fixtures 与 TPC-279 的 12-row transfer 通过，但 literal source
decomposition、arithmetic `L2` 与 full Gate B 仍未支付。

```text
TPC280_MAXIMUM_CLAIM = PROVED_CONDITIONAL_TWO_TERM_LEAKAGE_ENDPOINT_COMPILER_PLUS_NUMERICALLY_CERTIFIED_TRANSFER
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
TPC280_ROUND2_CLUE = AUDIT_TYPED_ARITHMETIC_L2_INTERFACE_FOR_FULL_GATE_B
```

strongest positive result：exact two-term normalization, dominant exponent compiler, and
sharp equality family；strongest obstruction：a slower additive leakage exponent caps gain;
open theorem：literal source-level leakage decomposition with arithmetic `L2`。

TPC-279 upstream entry: proof 为
`research/tpc-big-road/bridge_b_coherence_to_gain_theorem.md`，checker 为
`tpc_bridge_b_coherence_to_gain_theorem_checker.py`，编号论文为
`papers/tpc-279-coherence-to-gain-theorem/`。它提供 TPC-280 的 exact deficit parent
与 12-row coordinate transfer。

TPC-278 上游入口：proof 为
`research/tpc-big-road/bridge_b_cross_scale_gain_stability.md`，checker 为
`tpc_bridge_b_cross_scale_gain_stability_checker.py`，编号论文为
`papers/tpc-278-cross-scale-gain-stability/`。它保留为 TPC-279 的 finite source
transfer parent；邻近 shell/clock choices 的 four sign flips 仍是 scoped obstruction，
不提供 asymptotic credit。

TPC-277 上游入口：proof 为
`research/tpc-big-road/bridge_b_four_packet_gain_floor.md`，checker 为
`tpc_bridge_b_four_packet_gain_floor_checker.py`，编号论文为
`papers/tpc-277-four-packet-gain-floor/`。它沿用 TPC-276 的四个实际 source-block
packets，证明通用 `G<=4D` 与 `E<=0 => G<=D`，并把增益写成
`r=(1-kappa)^(-1)`。8 个 registered/extended rows 全部有负 net cross term、`r>1`，
但一行低于 `1.01`；因此下一关是 cross-scale signed-gain stability 与 shell sensitivity，
不是有限表的幂次升级。

```text
TPC277_MAXIMUM_CLAIM = PROVED_EXACT_UNIVERSAL_FOUR_PACKET_GAIN_FLOOR_PLUS_NUMERICALLY_CERTIFIED_SOURCE_SCAN
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
TPC277_ROUND2_CLUE = TEST_CROSS_SCALE_SIGNED_GAIN_STABILITY_AND_SHELL_SENSITIVITY
```

strongest positive result：sharp four-packet floor plus an exact source replay extending
to `N=2048`；strongest obstruction：geometry alone has no positive power gain and the
finite one-percent floor fails；open theorem：uniform source-level lower control for `G/D`。

当前 TPC-276 入口：proof 为
`research/tpc-big-road/bridge_b_signed_gain_endpoint_budget.md`，checker 为
`tpc_bridge_b_signed_gain_endpoint_budget_checker.py`，编号论文为
`papers/tpc-276-signed-gain-endpoint-budget/`。它冻结 TPC-275 的实际四包 signed
output，证明 exact `m^2=(D/G)m_D^2`，并给出带
`eta_eff=max(0,eta_D-gamma/2)` 的 conditional compiler：严格目标为
`sigma-eta_eff>1/400`。12 个 rows 全部有 `D/G>1`，3 行超过 `m^2=1/16`、5 行超过
`m^2=1/64`；这些是 finite exact-rational transfer，不能升级为 source-level power
bound，fixed-power credit 仍为 0，arithmetic `L2`、full Gate B 与 twin-prime
conclusion 仍 OPEN/NONE。

```text
TPC276_MAXIMUM_CLAIM = PROVED_CONDITIONAL_SIGNED_GAIN_STRICT_ENDPOINT_BUDGET_PLUS_FINITE_TRANSFER
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
TPC276_ROUND2_CLUE = SEEK_UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND
```

strongest positive result：exact signed gain-to-margin bridge plus conditional half-exponent
endpoint compiler；strongest obstruction：finite `D/G` values do not pay a fixed power；
open theorem：uniform source-level signed gain lower bound coupled to the margin lane。

当前 TPC-275 入口：proof 为
`research/tpc-big-road/bridge_b_signed_four_packet_reassembly.md`，checker 为
`tpc_bridge_b_signed_four_packet_reassembly_checker.py`，编号论文为
`papers/tpc-275-signed-four-packet-reassembly/`。它冻结 TPC-274 的 literal V59
physical operator、exact beta、projection 与 growing-cutoff registry，保留四个实际
source-block packets `V_j=A_perp beta^(j)`，并证明 exact signed Gram、四点 DFT 与
real polarization identities。12 个 rows 由 exact rational replay 认证 `G-D<0`、
`1<D/G<12/5`、`F/G>50` 与 `m_D^2<1/16`；这是 signed reassembly 的
`YES_SCOPED` finite advance，source-level signed cross-Gram、margin/endpoint payment、
fixed-power credit、arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC275_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT
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
TPC275_ROUND2_CLUE = COMPILE_SIGNED_CROSS_GRAM_WITH_MARGIN_AND_ENDPOINT_BUDGET
```

strongest positive result：actual source-block signed packet Gram/DFT/polarization
ledger plus 12-row exact replay；strongest obstruction：the packet-diagonal proxy still
has `m_D^2<1/16` everywhere and cannot pay a quarter margin；open theorem：a growing
source-level signed cross-Gram estimate with explicit endpoint budget.

当前 TPC-274 入口：proof 为
`research/tpc-big-road/bridge_b_projected_output_frobenius_envelope.md`，checker 为
`tpc_bridge_b_projected_output_frobenius_envelope_checker.py`，编号论文为
`papers/tpc-274-projected-output-frobenius-envelope/`。它冻结 TPC-273/TPC-268 的
literal V59 finite physical operator、exact beta source、三块 Haar projection 与
TPC-269 growing-cutoff registry，定义 `A_perp=(I-P_3)A`，并证明
`G_perp<=||A_perp||_F^2||beta||_2^2=G_F`。6 个 scale、2 个 kernel exponent 的 12
个 rows 均由 exact rational matrix replay 认证 `G_F/G_perp>50` 与 envelope proxy
`m_F^2<1/64`；phase census 为 11 negative-real、1 positive-real、0 crossing。这是
`INSUFFICIENT_SCOPED` 的 cancellation-free envelope obstruction，不是 actual margin
upper bound、渐近反例或 source-level output theorem；signed output reassembly、fixed-
power credit、arithmetic `L2`、full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC274_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_PROJECTED_FROBENIUS_ENVELOPE_GAP
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
TPC274_ROUND2_CLUE = TEST_SIGNED_OUTPUT_REASSEMBLY_BEYOND_CANCELLATION_FREE_ENVELOPES
```

strongest positive result：exact projected Frobenius inequality plus independent
12-row matrix replay；strongest obstruction：the cancellation-free envelope loses more
than a factor of 50 on every registered row；open theorem：source-level signed output
reassembly with an effective saving and explicit margin control。

当前 TPC-273 入口：proof 为
`research/tpc-big-road/bridge_b_margin_stability_matrix.md`，checker 为
`tpc_bridge_b_margin_stability_matrix_checker.py`，编号论文为
`papers/tpc-273-margin-stability-matrix/`。它冻结 TPC-268 的 literal V59 finite
physical operator，扫描 4 个尺度、4 个 cutoff 与 2 个 kernel exponent，精确使用
`m^2=rho^2`、`m^6=(rho^2)^3` 形成 32-row matrix。outward intervals 给出 12 low、11
middle、9 high rows；`N=64` 和 `N=128` 的 cutoff-only comparisons 各有一个跨带
flip，phase census 为 30 negative-real、2 positive-real、0 crossing。这是
`REFUTED_SCOPED` 的 finite stability obstruction，不是 source-level asymptotic
counterexample；source-level margin uniformity、fixed-power credit、arithmetic `L2`、
full Gate B 与 twin-prime conclusion 仍 OPEN/NONE。

```text
TPC273_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_MARGIN_STABILITY_OBSTRUCTION
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
TPC273_ROUND2_CLUE = TEST_SOURCE_LEVEL_MARGIN_UNIFORMITY_ON_THE_LITERAL_GROWING_CUTOFF
```

strongest positive result：exact margin transfer plus independently replayed 32-row
matrix；strongest obstruction：cutoff-only finite flips across both quantitative bands；
open theorem：source-level margin uniformity on the literal growing cutoff.

当前 TPC-272 入口：proof 为
`research/tpc-big-road/bridge_b_correlation_margin_budget.md`，checker 为
`tpc_bridge_b_correlation_margin_budget_checker.py`，编号论文为
`papers/tpc-272-correlation-margin-budget-compiler/`。它在 TPC-271 的同一有限
坐标上定义 `m=|C_perp|/R`，证明 `m^6=Xi_C/Xi`，并把 source-level signed scalar
saving `sigma` 与 margin loss `eta` 编译成 endpoint saving `sigma-eta`；严格目标
条件是 `sigma-eta>1/400`。二维 sharp converse 证明负 phase sign 本身不能保证
正 margin。9 行/4 个 dyadic finite records 由 exact rational division 认证，
其中 `96->192` 的 margin sixth-power ratio `<(1/32)^6` 且 phase sign 保持。
这是条件 theorem 加 finite audit；source-level margin、arithmetic `L2`、full Gate B
和 twin-prime conclusion 仍 OPEN/NONE，fixed-power credit 仍为 0。

```text
TPC272_MAXIMUM_CLAIM = PROVED_CONDITIONAL_CORRELATION_MARGIN_TO_RADIUS_BUDGET_COMPILER
TPC272_ROUTE_ADVANCE = YES_SCOPED_CONDITIONAL_MARGIN_BUDGET_AND_FINITE_AUDIT
TPC272_CONDITIONAL_BUDGET_COMPILER = PROVED_CONDITIONAL
TPC272_MARGIN_IDENTITY = PROVED_EXACT_FINITE
TPC272_SHARP_CONVERSE = PROVED_EXACT
TPC272_FINITE_MARGIN_AUDIT = NUMERICALLY_CERTIFIED
TPC272_SOURCE_LEVEL_MARGIN = OPEN_ASYMPTOTIC
TPC272_FIXED_POWER_CREDIT = 0
TPC272_ARITHMETIC_ADVANCE = NO
TPC272_L2 = NONE
TPC272_FULL_GATE_B = OPEN
TPC272_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC272_TWIN_PRIME_RESULT = NONE
TPC272_STATUS = PROVED_CONDITIONAL_CORRELATION_MARGIN_TO_RADIUS_BUDGET_COMPILER
TPC272_ROUND2_CLUE = AUDIT_SOURCE_LEVEL_MARGIN_LOWER_BOUND_BEFORE_ANY_PHASE_PROMOTION
```

strongest positive result：`sigma-eta` endpoint budget compiler；strongest obstruction：
sign-only phase admits arbitrarily small margin；open theorem：literal V59 source-level
margin lower bound coupled to the signed scalar estimate。

当前 TPC-271 入口：proof 为
`research/tpc-big-road/bridge_b_phase_radius_decoupling.md`，checker 为
`tpc_bridge_b_phase_radius_decoupling_checker.py`，编号论文为
`papers/tpc-271-phase-radius-decoupling/`。它在 TPC-270 的同一 finite interface
中同时记录 signed scalar `C_perp`、source lane `W_perp`、output lane `G_perp`，
并证明 exact finite identities
`Xi=Xi_W*Xi_G` 与 `Xi/Xi_C=|kappa|^(-6)`。9 个 rows 的 phase 全为
`NEGATIVE_REAL_AXIS`，但 `96->192` 的 radius ratio `>23` 由 source ratio `<1/8`
与 output ratio `>230` 的乘积驱动。这是 scoped finite phase-radius decoupling，
不是 source-level phase/radius theorem；fixed-power credit、arithmetic `L2` 与
full Gate-B 仍 OPEN/NONE。

```text
TPC271_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT
TPC271_ROUTE_ADVANCE = YES_SCOPED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT
TPC271_LANE_FACTORIZATION = PROVED_EXACT_FINITE
TPC271_PHASE_SIGN_CENSUS = NUMERICALLY_CERTIFIED_FINITE
TPC271_PHASE_RADIUS_DECOUPLING = NUMERICALLY_CERTIFIED_FINITE
TPC271_SOURCE_LANE_PROFILE_INVARIANCE = PROVED_EXACT_FINITE
TPC271_OUTPUT_LANE_SPIKE = NUMERICALLY_CERTIFIED_FINITE
TPC271_SOURCE_LEVEL_SIGNED_PHASE = OPEN_ASYMPTOTIC
TPC271_SOURCE_LEVEL_RADIUS = OPEN_ASYMPTOTIC
TPC271_FIXED_POWER_CREDIT = 0
TPC271_ARITHMETIC_ADVANCE = NO
TPC271_L2 = NONE
TPC271_FULL_GATE_B = OPEN
TPC271_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC271_TWIN_PRIME_RESULT = NONE
TPC271_STATUS = NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT
TPC271_ROUND2_CLUE = TEST_SOURCE_LEVEL_SIGNED_PHASE_BOUND_WITH_EXPLICIT_RADIUS_LANE_CONTROL
```

strongest positive result：exact lane factorization plus a phase-locked,
output-lane-dominated finite spike；strongest obstruction：constant finite phase
sign does not stabilize normalized radius；open theorem：source-compatible signed
phase bound coupled to explicit radius-lane control。

## Upstream TPC-270

TPC-270 入口：proof 为
`research/tpc-big-road/bridge_b_cross_scale_radius_normalization.md`，checker 为
`tpc_bridge_b_cross_scale_radius_normalization_checker.py`，编号论文为
`papers/tpc-270-cross-scale-radius-normalization/`。它保持 literal V59 finite
physical operator 与 TPC-269 的 growing-cutoff registry 不变，定义
`Xi=(R_squared)^3/N^10=(R/N^(5/3))^6`，并认证 6 个 base rows、4 个 dyadic
ratios、5 个 adjacent ratios 与 3 个 profile controls。dyadic pattern 为
`DROP_RISE_RISE_DROP`；这是 scoped finite normalization audit，不是 source-level
radius theorem，fixed-power credit、arithmetic `L2` 与 full Gate-B 仍 OPEN/NONE。

```text
TPC270_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT
TPC270_ROUTE_ADVANCE = YES_SCOPED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT
TPC270_ENDPOINT_NORMALIZATION = PROVED_EXACT_FINITE_IDENTITY
TPC270_CROSS_SCALE_VARIATION = NUMERICALLY_CERTIFIED_FINITE
TPC270_PROFILE_CONTROL = NUMERICALLY_CERTIFIED_FINITE
TPC270_FINITE_STABILITY = REFUTED_SCOPED
TPC270_SOURCE_LEVEL_RADIUS = OPEN_ASYMPTOTIC
TPC270_SOURCE_LEVEL_PHASE = OPEN_ASYMPTOTIC
TPC270_FIXED_POWER_CREDIT = 0
TPC270_ARITHMETIC_ADVANCE = NO
TPC270_L2 = NONE
TPC270_FULL_GATE_B = OPEN
TPC270_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC270_TWIN_PRIME_RESULT = NONE
TPC270_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT
TPC270_ROUND2_CLUE = TEST_SOURCE_LEVEL_RADIUS_UPPER_BOUND_WITH_EXPLICIT_POWER_NORMALIZATION
```

strongest positive result：exact sixth-power endpoint normalization and a
threshold-separated finite dyadic certificate；strongest obstruction：the same
registry has both a greater-than-23-fold rise and a drop below `1/4`；open theorem：
source-compatible radius bound with explicit power and uniformity。

## Upstream TPC-269

TPC-269 入口：proof 为
`research/tpc-big-road/bridge_b_growing_cutoff_profile_transfer.md`，checker 为
`tpc_bridge_b_growing_cutoff_profile_transfer_checker.py`，编号论文为
`papers/tpc-269-growing-cutoff-profile-transfer/`。它保持 literal V59 finite
physical operator 不变，采用注册的 `z_N=floor(log N)` cutoff proxy，并通过
`K_theta=(1-theta)K_1+theta K_2` 精确转移 convex profile。12 行中 8 个
contraction、4 个 obstruction；同一 central row 的 `theta=9/10` 与 `24/25`
跨过 `rho=1/4`。这是 scoped finite transfer，不是 source-level growing theorem；
cross-scale radius normalization、arithmetic `L2` 与 full Gate-B 仍 OPEN/NONE。

```text
TPC269_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER
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
TPC269_ROUND2_CLUE = TEST_CROSS_SCALE_RADIUS_NORMALIZATION_AFTER_SOURCE_COMPATIBLE_PROFILE
```

strongest positive result：exact affine profile transfer plus eight independently
audited contractions；strongest obstruction：the `9/10` to `24/25` profile path
crosses the quarter threshold at a fixed growing-proxy clock；open theorem：
source-compatible growing uniformity and cross-scale radius normalization。

## Upstream TPC-268: finite cutoff-sensitivity obstruction

TPC-268 入口：proof 为
`research/tpc-big-road/bridge_b_finite_cutoff_sensitivity_obstruction.md`，checker 为
`tpc_bridge_b_finite_cutoff_sensitivity_obstruction_checker.py`，编号论文为
`papers/tpc-268-finite-cutoff-sensitivity-obstruction/`。它固定 TPC-267 的 literal
physical operator，仅改变声明的 finite cutoff/clock/kernel 参数；16 行中 10 个
contraction、6 个 obstruction，中心 `z=2`/`z=3` 在同一 `(N,H,Q,s)` 上翻过
`1/4` 阈值。这是 scoped finite obstruction，不是 growing V59 counterexample，
fixed-power credit 仍为 0，growing profile uniformity、arithmetic `L2` 与 full Gate-B
仍 OPEN/NONE。

```text
TPC268_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION
TPC268_ROUTE_ADVANCE = YES_SCOPED_FINITE_CUTOFF_SENSITIVITY_OBSTRUCTION
TPC268_FINITE_CUTOFF_OBSTRUCTION = NUMERICALLY_CERTIFIED
TPC268_MATCHED_Z2_CONTROLS = NUMERICALLY_CERTIFIED
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
TPC268_ROUND2_CLUE = TEST_GROWING_CUTOFF_UNIFORMITY_BEFORE_ANY_PHASE_PROMOTION
```

strongest positive result：matched `z=2` controls are reproduced while the same
finite construction is tested under explicit perturbations；strongest obstruction：
`z=3` flips the central row above the quarter threshold；open theorem：growing
cutoff/profile uniformity for the literal V59 residual。


## Upstream TPC-267: finite literal V59 residual census

TPC-267 入口：proof 为
`research/tpc-big-road/bridge_b_literal_v59_residual_radius_census.md`，checker 为
`tpc_bridge_b_literal_v59_residual_radius_census_checker.py`，编号论文为
`papers/tpc-267-literal-v59-residual-radius-census/`。它在同一 literal V59 有限接口上
保留 prime shell、unit masks、deleted diagonal、beta、shifted-prime comparison 与
rank-three residual，12 个自然有限行全部通过 outward interval 的 `|C_perp|/R<1/4`
证书；这是 finite signed-phase census，不能升级为渐近 radius/sector theorem，
fixed-power credit 仍为 0，arithmetic `L2` 与 full Gate-B 仍 OPEN/NONE。

```text
TPC267_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS
TPC267_ROUTE_ADVANCE = YES_SCOPED_FINITE_LITERAL_RESIDUAL_CENSUS
TPC267_FINITE_RESIDUAL_RADIUS = NUMERICALLY_CERTIFIED
TPC267_FINITE_SIGNED_PHASE = NUMERICALLY_CERTIFIED
TPC267_QUARTER_CONTRACTION = NUMERICALLY_CERTIFIED_ALL_12_ROWS
TPC267_ACTUAL_V59_RADIUS = OPEN_ASYMPTOTIC
TPC267_ACTUAL_V59_PHASE = OPEN_ASYMPTOTIC
TPC267_FIXED_POWER_CREDIT = 0
TPC267_ARITHMETIC_ADVANCE = NO
TPC267_L2 = NONE
TPC267_FULL_GATE_B = OPEN
TPC267_STATUS = NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS
```

当前 TPC-266 入口：proof 为
`research/tpc-big-road/bridge_b_typed_end_to_end_claim_firewall.md`，checker 为
`tpc_bridge_b_typed_end_to_end_claim_firewall_checker.py`，编号论文为
`papers/tpc-266-end-to-end-claim-firewall/`。它把 TPC-263 的 fixed-log center、
TPC-264 的 Schur residual set 与 TPC-265 的 sharp radial endpoint 组成一个
typed compiler，并以 exact six-state hostile matrix 封住 fixed-log promotion、
residual deletion、borderline equality 与 subcritical lane 的非法 closure。
actual V59 radius/phase、arithmetic `L2` 与 full Gate-B 仍 OPEN/NONE。

```text
TPC266_MAXIMUM_CLAIM = PROVED_EXACT_END_TO_END_RESIDUAL_CLAIM_FIREWALL
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
TPC266_ROUND2_CLUE = PROVE_A_LITERAL_V59_RADIUS_OR_SIGNED_PHASE_BOUND_WITH_EFFECTIVE_SAVING_GREATER_THAN_1_OVER_400
```

strongest positive result：typed chain composition and exact six-state hostile
classification；strongest obstruction：fixed-log center plus open Schur radius
cannot close the endpoint；open theorem：literal V59 radius or signed-phase
bound with effective saving strictly above `1/400`。

当前 TPC-265 入口：proof 为
`research/tpc-big-road/bridge_b_schur_endpoint_budget_compiler.md`，checker 为
`tpc_bridge_b_schur_endpoint_budget_compiler_checker.py`，编号论文为
`papers/tpc-265-schur-endpoint-budget-compiler/`。它承接 TPC-264 的 Schur
feasible set，证明 projected center `c` 与 residual radius `R` 的 uniform
reassembly cost 恰为 `|c|+R`，并把 center/radius 两 lane 接入
`E0-E*=1/400` 的严格 endpoint compiler。fixed-log center/radius credit 均为零；
actual V59 radius/phase、arithmetic `L2` 与 full Gate-B 仍 OPEN/NONE。

```text
TPC265_MAXIMUM_CLAIM = PROVED_EXACT_SCHUR_TO_ENDPOINT_BUDGET_COMPILER
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
TPC265_ROUND2_CLUE = TEST_LITERAL_RESIDUAL_RADIUS_OR_PHASE_AGAINST_THE_TWO_LANE_BUDGET
```

strongest positive result：Schur radius 的 exact radial support 与 strict two-lane
budget compiler；strongest obstruction：free residual phase 总能实现 aligned endpoint，
norm-only data 没有 cancellation credit；open theorem：literal V59 residual radius 或
signed phase theorem。

当前 TPC-264 入口：proof 为
`research/tpc-big-road/bridge_b_orthogonal_residual_schur_firewall.md`，checker 为
`tpc_bridge_b_orthogonal_residual_schur_firewall_checker.py`，编号论文为
`papers/tpc-264-orthogonal-residual-schur-firewall/`。它承接 TPC-263 的 exact
`C_3+C_perp` split，证明在固定 projected data 与 residual norms 下，`C_perp`
的 Schur feasible set 按补空间维数精确分成 disk/circle/singleton。二维补空间
仍允许 endpoint-scale `x^(5/3)` residual；这是 structural firewall，不是 literal
prime-shell counterexample，也不产生 fixed-power、arithmetic `L2` 或 full Gate-B
payment。

```text
TPC264_MAXIMUM_CLAIM = PROVED_EXACT_ORTHOGONAL_RESIDUAL_SCHUR_FIREWALL
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
TPC264_ROUND2_CLUE = TURN_THE_SCHUR_RADIUS_OR_RESIDUAL_PHASE_INTO_A_LITERAL_V59_ESTIMATE
```

strongest positive result：正交残差的 Schur disk/circle/singleton 分类 exact 且 sharp；
strongest obstruction：仅凭 `P3` 数据与 norm-only residual information 不能压缩二维
补空间中的 full-radius residual；open theorem：actual V59 residual radius 或 signed
phase estimate。

当前 TPC-263 入口：proof 为
`research/tpc-big-road/bridge_b_rank_three_physical_cross_gram.md`，checker 为
`tpc_bridge_b_rank_three_physical_cross_gram_checker.py`，编号论文为
`papers/tpc-263-rank-three-physical-cross-gram/`。它把 TPC-254 的四个物理
block-sum fixed-log control 与 TPC-257 的三个 adjoint coefficients 在 exact
rank-three projection `P3` 上相乘，得到
`C_3=O(x^(5/3)/(log x)^(M+3))`。正交残差 `C_perp` 被精确保留但仍 OPEN；
该结果不产生 fixed-power credit、arithmetic `L2` 或 full Gate B payment。

```text
TPC263_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_RANK_THREE_PHYSICAL_CROSS_GRAM_CHANNEL
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
TPC263_ROUND2_CLUE = ATTACK_THE_ORTHOGONAL_COMPLEMENT_AFTER_PAYING_THE_RANK_THREE_LOG_CHANNEL
```

strongest positive result：rank-three physical cross-Gram channel has arbitrary
fixed logarithmic suppression；strongest obstruction：the exact orthogonal
complement remains unestimated；open theorem：residual cross-Gram estimate or
natural residual obstruction。

当前 TPC-262 入口：proof 为
`research/tpc-big-road/bridge_b_literal_mode_zero_cross_gram.md`，checker 为
`tpc_bridge_b_literal_mode_zero_cross_gram_checker.py`，编号论文为
`papers/tpc-262-literal-mode-zero-cross-gram/`。它精确锁定
`J_(q,v)=S_(q,v)^*C_qS_(q,v)-((q-2)/(q-1))P_q`，并把四 packet mode zero 写成
signed cross-Gram/DFT identity；phase-character lemma 明确区分 aggregate mode zero
与 V59 polarized character。finite operator-image witness 只证明 diagonal/PSD
不足以支付端点，不是 growing-shell counterexample；actual `beta,w` cross-Gram、
arithmetic `L2` 与 full Gate B 仍 OPEN。

```text
TPC262_MAXIMUM_CLAIM = PROVED_EXACT_LITERAL_SIGNED_REDUCED_RESIDUE_OPERATOR_AND_PHASE_CHARACTER_FIREWALL
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
TPC262_ROUND2_CLUE = CENSUS_THE_LITERAL_GROWING_PRIME_SHELL_CROSS_GRAM
```

strongest positive result：literal signed operator and phase typing are exact at
finite `x`；strongest obstruction：finite literal operator image admits aligned and
alternating endpoints with identical diagonals；open theorem：growing actual V59
character-specific cross-Gram estimate with effective saving `>1/400`。

TPC-261 上游入口：proof 为
`research/tpc-big-road/bridge_b_strict_endpoint_budget_compiler.md`，checker 为
`tpc_bridge_b_strict_endpoint_budget_compiler_checker.py`，编号论文为
`papers/tpc-261-strict-endpoint-budget-compiler/`。它把当前 baseline `E0=5/3` 与
target `E*=1997/1200` 的差距精确写成 `1/400`，证明有限 lane 的 effective
saving `sigma=min(delta_l-lambda_l)` 必须严格大于 `1/400`；fixed-log suppression
没有 fixed-power credit，并以 scaled TPC-260 witness 保留 structural residual
ambiguity。

```text
TPC261_MAXIMUM_CLAIM = PROVED_STRUCTURAL_ENDPOINT_BUDGET_OBSTRUCTION_FOR_LITERAL_V59_REASSEMBLY
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
TPC261_STATUS = PROVED_STRUCTURAL_ENDPOINT_BUDGET_OBSTRUCTION_FOR_LITERAL_V59_REASSEMBLY
TPC261_ROUND2_CLUE = PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_WITH_EFFECTIVE_SAVING_GREATER_THAN_1_OVER_400
```

strongest positive result：exact lane-wise endpoint budget compiler；strongest obstruction：
log-only null suppression 与 scaled null-compatible residual 不能自动支付任何 global
fixed-power credit；open theorem：literal common-clock mode-zero 或 signed cross-Gram
estimate with effective saving `>1/400`；reusable structure：gap -> saving-minus-loss
-> log/power firewall -> scaled witness -> minimum literal theorem。

TPC-260 直接上游入口：proof 为
`research/tpc-big-road/bridge_b_four_packet_residual_reassembly.md`，checker 为
`tpc_bridge_b_four_packet_residual_reassembly_checker.py`，编号论文为
`papers/tpc-260-four-packet-residual-reassembly/`。它把 TPC-258 的 source-frozen
null direction 嵌入四块 Haar complement，证明 null-compatible 四 packet completion
的 sharp polygon interval，并用 four-point DFT 精确标出 mode zero：固定 packet
marginals 与全部已知 Haar/null projections 仍允许 residual energy `0` 和 `16`。
这是 scoped structural obstruction；literal mode-zero/cross-Gram、arithmetic `L2`
与 full Gate B 仍 OPEN。

```text
TPC260_MAXIMUM_CLAIM = PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION
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
TPC260_STATUS = PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION
TPC260_ROUND2_CLUE = PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_FOR_THE_COMMON_V59_FOUR_PACKET_OUTPUT
```

TPC-259 直接上游入口：proof 为
`research/tpc-big-road/bridge_b_same_clock_null_coupling.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_same_clock_null_coupling_checker.py`，编号论文为
`papers/tpc-259-same-clock-null-coupling/`。它在同一 literal V59 clock 上将
TPC-258 的 source-frozen `z_null` 与四块 hybrid `w` moment 接入 exact
rank-one/residual decomposition，证明 null signed-coupling channel 为
`o(x^(5/3)/log^(M+3)(x))`（每个固定 `M,K`）。这是 scoped source-backed
advance；`<w_perp,A_x beta>` 仍 OPEN，fixed-power、arithmetic `L2` 与 full Gate B
仍未支付。

```text
TPC259_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_SAME_CLOCK_NULL_CHANNEL_SUPPRESSION_FOR_LITERAL_V59_SIGNED_COUPLING
TPC259_ROUTE_ADVANCE = YES_SCOPED_NULL_CHANNEL
TPC259_ARITHMETIC_ADVANCE = YES_SCOPED_SIGNED_COUPLING_CHANNEL
TPC259_W_NULL_MOMENT = PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER
TPC259_NULL_CHANNEL = PROVED_SOURCE_BACKED_o_ONE
TPC259_RESIDUAL_DECOMPOSITION = PROVED_EXACT
TPC259_RESIDUAL_FULL_SCALAR = OPEN
TPC259_FIXED_POWER_SAVING = NONE
TPC259_L2 = NONE
TPC259_FIXED_ATOM_CREDIT = 0
TPC259_FULL_GATE_B = OPEN
TPC259_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC259_TWIN_PRIME_RESULT = NONE
TPC259_STATUS = PROVED_SOURCE_BACKED_SAME_CLOCK_NULL_CHANNEL_SUPPRESSION_FOR_LITERAL_V59_SIGNED_COUPLING
TPC259_ROUND2_CLUE = AUDIT_FULL_FOUR_PACKET_SIGNED_REASSEMBLY_WITH_THE_ORTHOGONAL_RESIDUAL_EXPLICITLY_PRESENT
```

TPC-258 直接上游入口：proof 为
`research/tpc-big-road/bridge_b_source_frozen_transverse_null_direction.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_source_frozen_transverse_null_direction_checker.py`，编号论文为
`papers/tpc-258-source-frozen-transverse-null-direction/`。它提供 TPC-259 使用的
source-frozen unit null direction 与 `o(x^(7/6)/log^3(x))` adjoint moment。

```text
TPC258_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_FOR_LITERAL_V59_ADJOINT
TPC258_ROUTE_ADVANCE = YES_SCOPED_TRANSVERSE_NULL
TPC258_ARITHMETIC_ADVANCE = YES_SCOPED_LOG_CANCELLATION
TPC258_NULL_DIRECTION = PROVED_SOURCE_FROZEN_UNIT_VECTOR
TPC258_LEADING_DIAGONAL_CANCELLATION = PROVED_SOURCE_BACKED
TPC258_RATE_REFINEMENT = CONDITIONAL_THEOREM_LOG_ONE_OVER_X
TPC258_FIXED_POWER_SAVING = NONE
TPC258_L2 = NONE
TPC258_FIXED_ATOM_CREDIT = 0
TPC258_FULL_GATE_B = OPEN
TPC258_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC258_TWIN_PRIME_RESULT = NONE
TPC258_STATUS = PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_FOR_LITERAL_V59_ADJOINT
TPC258_ROUND2_CLUE = TEST_THE_SOURCE_FROZEN_NULL_DIRECTION_AGAINST_THE_LITERAL_SIGNED_W_BETA_COUPLING_ON_THE_SAME_CLOCK_BEFORE_ANY_FULL_REASSEMBLY
```

TPC-257 更上游入口：proof 为
`research/tpc-big-road/bridge_b_four_block_haar_transverse_norm_floor.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_four_block_haar_transverse_norm_floor_checker.py`，编号论文为
`papers/tpc-257-four-block-haar-transverse-norm-floor/`。它在同一 literal V59 clock 上
把两个 rank children 各 source-only 二分，得到 exact orthonormal 的三向 Haar frame；
strong PNT curvature 与 `B_Q` diagonal 给出 `z1,z2` transverse plane 的显式同阶
lower floor。该结果是 obstruction/下界，不是 arithmetic `L2` 上界。

```text
TPC257_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR_FOR_LITERAL_V59_ADJOINT
TPC257_ROUTE_ADVANCE = YES_SCOPED_TRANSVERSE_HAAR
TPC257_ARITHMETIC_ADVANCE = YES_SCOPED_TRANSVERSE_LOWER_FLOOR
TPC257_THREE_MODE_HAAR_ORTHOGONALITY = PROVED_EXACT
TPC257_TRANSVERSE_OUTPUT_FLOOR = PROVED_SOURCE_BACKED
TPC257_FULL_OUTPUT_NORM_FLOOR = PROVED_SOURCE_BACKED
TPC257_L2 = NONE
TPC257_FIXED_ATOM_CREDIT = 0
TPC257_FULL_GATE_B = OPEN
TPC257_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC257_TWIN_PRIME_RESULT = NONE
TPC257_STATUS = PROVED_SOURCE_BACKED_TRANSVERSE_HAAR_NORM_FLOOR
TPC257_ROUND2_CLUE = USE_THE_EXPLICIT_TWO_DIMENSIONAL_TRANSVERSE_HAAR_FLOOR_TO_SEARCH_FOR_A_SOURCE_FROZEN_DIAGONAL_NULL_DIRECTION_BEFORE_ATTEMPTING_ANY_FULL_GATE_B_UPPER_BOUND
```

TPC-256 上游入口：proof 为
`research/tpc-big-road/bridge_b_literal_beta_haar_adjoint_asymptotic.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_literal_beta_haar_adjoint_asymptotic_checker.py`，编号论文为
`papers/tpc-256-literal-beta-haar-adjoint-asymptotic/`。它支付 literal beta rank-midpoint
的显式正主项与 adjoint midpoint scalar；TPC-257 证明其正交 descendant plane 也不能
被当作低阶 remainder。

```text
TPC256_LITERAL_BETA_DIVISOR_DENSITY_CANCELLATION = PROVED_EXACT_ENDPOINT_BOUND
TPC256_LITERAL_BETA_HAAR_ASYMPTOTIC = PROVED_SOURCE_BACKED
TPC256_BQ_WEIGHTED_PRIME_ASYMPTOTIC = PROVED_SOURCE_BACKED
TPC256_INPUT_UNIT_BOUND = PROVED_SOURCE_BACKED
TPC256_HARD_WINDOW_BOUND = PROVED_SOURCE_BACKED
TPC256_CHILD_JUMP_BOUND = PROVED_SOURCE_BACKED
TPC256_BOUNDARY_POWER_SEPARATION = PROVED_EXACT_ONE_OVER_48
TPC256_ADJOINT_NORMALIZED_COMPLEX_ASYMPTOTIC = PROVED_SOURCE_BACKED
TPC256_REAL_PART_EVENTUALLY_NEGATIVE = PROVED
TPC256_SCALAR_EVENTUALLY_NONZERO = PROVED
TPC256_NORMALIZED_PHASE_TO_MINUS_ONE = PROVED
TPC256_SCALAR_IS_REAL = NOT_CLAIMED
TPC256_UNQUALIFIED_PRINCIPAL_ARGUMENT_TO_PLUS_PI = NOT_CLAIMED
TPC256_ROUTE_ADVANCE = YES_LITERAL_ARITHMETIC
TPC256_ARITHMETIC_ADVANCE = YES_SCOPED_LITERAL_BETA_ADJOINT_HAAR_LANE
TPC256_FIXED_ATOM_CREDIT = 0
TPC256_L2 = NONE
TPC256_FULL_GATE_B = OPEN
TPC256_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC256_TWIN_PRIME_RESULT = NONE
TPC256_STATUS = PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC
TPC256_ROUND2_CLUE = EXPLOIT_EXACT_DIVISOR_DENSITY_CANCELLATION_BEFORE_ANY_TRIANGLE__THEN_USE_THE_BQ_DIAGONAL_MAIN_AND_H2_OVER_Q_BOUNDARY_MOMENT_TO_ISOLATE_THE_TRANSVERSE_FULL_GATE_B_REMAINDER
```

TPC-255 上游入口：proof 为
`research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_exact_adjoint_diagonal_boundary_compiler_checker.py`，编号论文为
`papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/`。它提供 TPC-256 使用的 exact
`B_Q` diagonal、input-unit、hard-window 与 child-jump ledger。

TPC-254 上游入口：proof 为
`research/tpc-big-road/bridge_b_source_backed_rank_midpoint_hybrid_mean_closure.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_source_backed_rank_midpoint_hybrid_mean_closure_checker.py`，编号论文为
`papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/`。它支付 literal `w`
rank-midpoint moment 到 `x^(1/2)(log x)^(-M)`，并把第二 lane 定位为 TPC-255 已展开的
literal adjoint test。

TPC-253 上游入口：proof 为
`research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_source_frozen_rank_midpoint_contrast_compiler_checker.py`，编号论文为
`papers/tpc-253-source-frozen-rank-midpoint-contrast-compiler/`。它提供 TPC-254 使用的
coefficient-independent rank midpoint、exact partial-sum identity 与 safe adjoint。

TPC-252 上游入口：proof 为
`research/tpc-big-road/bridge_b_declared_partition_refinement_degeneracy.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_declared_partition_refinement_degeneracy_checker.py`，编号论文为
`papers/tpc-252-declared-partition-refinement-degeneracy/`。它封口 unrestricted partition
optimization，并要求 TPC-253 的 source-frozen nontrivial split。

TPC-251 更上游入口：proof 为
`research/tpc-big-road/bridge_b_literal_v59_declared_block_longitudinal_transverse_margin_compiler.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_literal_v59_declared_block_longitudinal_transverse_margin_compiler_checker.py`，编号论文为
`papers/tpc-251-literal-v59-declared-block-longitudinal-transverse-margin-compiler/`。它提供
TPC-252 审计的 exact longitudinal/transverse split 与 projected coherence margin。

TPC-250 上游入口：proof 为
`research/tpc-big-road/bridge_b_coherence_controlled_gram_quadratic_sharpness.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_coherence_controlled_gram_quadratic_sharpness_checker.py`，编号论文为
`papers/tpc-250-coherence-controlled-gram-quadratic-sharpness/`。它为 projected probe
family 提供 `D,L,mu` sharp Gram envelope 与 empty-pair convention。

TPC-249 上游入口：proof 为
`research/tpc-big-road/bridge_b_sharp_weighted_shared_lane_contraction.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_sharp_weighted_shared_lane_contraction_checker.py`，编号论文为
`papers/tpc-249-sharp-weighted-shared-lane-contraction/`。它在每个 shared lane 内先形成
`g_c=sum_b lambda_cbv_cb`，将 exact support radius 压成
`rho_c sqrt(lambda_c*G_c lambda_c)`，再按 independent/global budget 精确重组；
TPC-250 对该 quadratic 给出 coherence envelope。

TPC-248 上游入口：proof 为
`research/tpc-big-road/bridge_b_shared_lane_gram_ellipsoid_feasible_set.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_shared_lane_gram_ellipsoid_feasible_set_checker.py`，编号论文为
`papers/tpc-248-shared-lane-gram-ellipsoid-feasible-set/`。它提供 TPC-249 所收缩的 exact
joint Gram 椭球、sphere/slack 和 group-budget 几何。

TPC-247 更上游入口：proof 为
`research/tpc-big-road/bridge_b_literal_v59_source_operator_attachment.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_literal_v59_source_operator_attachment_checker.py`，编号论文为
`papers/tpc-247-literal-v59-source-operator-attachment/`。它提供 literal source operator、
hard-block exactly-once sum 和 `v_cb=A_cb beta_b`/单一 `w_c` source object；
TPC-248 闭合其 shared-lane joint feasible set。

TPC-246 更上游入口：proof 为
`research/tpc-big-road/bridge_b_weighted_covariance_disk_reassembly.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_weighted_covariance_disk_reassembly_checker.py`，编号论文为
`papers/tpc-246-weighted-covariance-disk-reassembly/`。它给出 complete-product weighted
disk 与 margin calculus；TPC-247 现在说明 actual source block pairs 在同一 output block
共享一个 lane，不能未经 audit 直接套用 pairwise Cartesian product。

TPC-245 上游入口：proof 为
`research/tpc-big-road/bridge_b_sharp_longitudinal_transverse_covariance_disks.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_sharp_longitudinal_transverse_covariance_disks_checker.py`，编号论文为
`papers/tpc-245-sharp-longitudinal-transverse-covariance-disks/`。它把 fixed local
moments/energies 的 feasible set exact classified 为 disk/circle/singleton/empty，并给出
TPC-246 使用的 local centers、radii 与 dimension firewall。

TPC-244 更上游入口：proof 为
`research/tpc-big-road/bridge_b_common_multiplier_sign_localization.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_common_multiplier_sign_localization_checker.py`，编号论文为
`papers/tpc-244-common-multiplier-sign-localization/`。它把 orthogonal same-block main
covariance 精确压成 `sum_h|C_h|^2<w_h,b_h>`，并把 nonorthogonal sign dependence
定位到 cut edges；这给出 TPC-246 的 source-compatible weights。

TPC-243 上游入口：proof 为
`research/tpc-big-road/bridge_b_hard_window_near_isometry_bilinear_transfer.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_hard_window_near_isometry_bilinear_transfer_checker.py`，编号论文为
`papers/tpc-243-hard-window-near-isometry-bilinear-transfer/`。它提供 TPC-244 使用的
hard-window oriented bilinear transfer 与 V59 `x^(-67/200+o(1))` leakage scale。

TPC-242 上游入口：proof 为
`research/tpc-big-road/bridge_b_phase_fourier_collision_separation.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_phase_fourier_collision_separation_checker.py`，编号论文为
`papers/tpc-242-phase-fourier-collision-separation/`。它提供 complete `C_4` spectrum、
sharp fixed-energy disk 与 TPC-241 typed no-transfer；TPC-243 把其 selected coefficient
接到 hard-window bilinear interface。

TPC-241 上游入口：proof 为
`research/tpc-big-road/bridge_b_top_prime_collision_sharpness.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_top_prime_collision_sharpness_checker.py`，编号论文为
`papers/tpc-241-top-prime-collision-sharpness/`。它证明 unsigned fixed-profile channel
达到 `x^(1/48)/log x`，TPC-242 则严格隔离该 trivial-character 信息与 signed mode。

TPC-240 上游入口：proof 为
`research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_top_prime_direct_energy_floor_checker.py`，编号论文为
`papers/tpc-240-top-prime-direct-energy-floor/`。它提供 q-split `x^(1/96)` exact floor；
TPC-241 的 first-moment collision theorem 产生第二个 `x^(1/96)` factor。

TPC-239 上游入口：proof 为
`research/tpc-big-road/bridge_b_brun_titchmarsh_primitive_bucket_envelope.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_brun_titchmarsh_primitive_bucket_envelope_checker.py`，编号论文为
`papers/tpc-239-brun-titchmarsh-primitive-bucket-envelope/`。它把 primitive bucket 编译为
reduced prime progressions并给出 logarithmic-only improvement；TPC-240 则证明 direct
floor 本身已经 fixed-power 饱和。

TPC-238 上游入口：proof 为
`research/tpc-big-road/bridge_b_finite_window_lower_frame_obstruction.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_finite_window_lower_frame_obstruction_checker.py`，编号论文为
`papers/tpc-238-finite-window-lower-frame-obstruction/`。它排除了 collapsed
cross-frequency fixed-power cancellation，并把 TPC-239 的搜索位置锁到 same-frequency
prime buckets。

TPC-237 更上游入口：proof 为
`research/tpc-big-road/bridge_b_collision_compressed_finite_window_reassembly.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_collision_compressed_finite_window_reassembly_checker.py`，编号论文为
`papers/tpc-237-collision-compressed-finite-window-reassembly/`。它提供 TPC-238 所审计的
collapsed primitive-frequency coefficient object 与 finite-window scale。

TPC-236 更上游入口：proof 为
`research/tpc-big-road/bridge_b_physical_multiwrap_collision_envelope.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_physical_multiwrap_collision_envelope_checker.py`，编号论文为
`papers/tpc-236-physical-multiwrap-collision-envelope/`。它提供 TPC-237 使用的 fixed-`h`
physical collision factor，并保留 Q101 ratio-three obstruction。

TPC-235 上游入口：proof 为
`research/tpc-big-road/bridge_b_v59_physical_depth_crosswalk.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_v59_physical_depth_crosswalk_checker.py`，编号论文为
`papers/tpc-235-v59-physical-depth-crosswalk/`。它冻结了 TPC-236 使用的 actual
depth/cutoff/profile/modulus 与 source-weight firewall。

TPC-234 上游入口：proof 为
`research/tpc-big-road/bridge_b_normalized_collision_bessel_stability.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_normalized_collision_bessel_stability_checker.py`，编号论文为
`papers/tpc-234-normalized-collision-bessel-stability/`。其 depth-uniform normalized
Bessel theorem 保留，但 source-valid normalization 已由 TPC-235 限定为
`OPEN_WEIGHTED_LINEAR_ONLY`。

TPC-233 上游入口：proof 为
`research/tpc-big-road/bridge_b_critical_depth_row_mass_obstruction.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_critical_depth_row_mass_obstruction_checker.py`，编号论文为
`papers/tpc-233-critical-depth-row-mass-obstruction/`。critical primorial clock 满足
`L~log Q/loglog Q`；endpoint prime rows 的 atom counts exact 是 `2` 与
`2(1+pi(2L-1)-pi(L))`，故 `kappa_raw>>(L/log L)->infinity`。fixed raw
comparability 不是 clock geometry theorem；normalization repair 仍开放。

```text
TPC233_CRITICAL_PRIMORIAL_CLOCK = PROVED_EXACT
TPC233_LOW_HIGH_PRIME_ROWS = PROVED_SOURCE_BACKED
TPC233_RAW_COMPARABILITY_DIVERGES = PROVED_ASYMPTOTIC
TPC233_UNIVERSAL_KAPPA_UPPER_BOUND = PROVED_EXACT_2L_MINUS_1
TPC233_FIXED_COMPARABILITY_FROM_GEOMETRY = REFUTED_SCOPED
TPC233_ROW_NORMALIZATION_REPAIR = OPEN
TPC233_ACTUAL_V59_ROW_WEIGHTS = OPEN
TPC233_ARITHMETIC_ADVANCE = NO
TPC233_L2 = NONE
TPC233_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC233_STATUS = PROVED_ARITHMETIC_OBSTRUCTION_L1
TPC233_ROUND2_CLUE = NORMALIZE_ROWS_THEN_TEST_COLLISION_OPERATOR_BEFORE_V59_ATTACHMENT
```

TPC-232 上游入口：proof 为
`research/tpc-big-road/bridge_b_subcritical_growing_resonance_depth.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_subcritical_growing_resonance_depth_checker.py`，编号论文为
`papers/tpc-232-subcritical-growing-resonance-depth/`。modeled clock `h=4LQ` 的 exact
collision normal form 为 `ar+bp=4LQ`。coefficient-uniform Selberg sieve 与
`sum 1/max(a,b)<4L` 给出
`C_L(Q)<<_A LQ log log(3LQ)/(log Q)^2`；故
`L=o(log Q/log log Q)` 时 `C_L/P->0`，fixed-comparability rows 不能支付 fixed saving。

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

TPC-231 上游入口：proof 为
`research/tpc-big-road/bridge_b_finite_resonance_sieve_obstruction.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_finite_resonance_sieve_obstruction_checker.py`，编号论文为
`papers/tpc-231-finite-resonance-sieve-obstruction/`。first `3--7` resonance 的 exact
two-form determinant 为 `16Q`，complete local root law 给出 Selberg upper bound
`E(Q)<<Q log log(3Q)/(log Q)^2`，故 `E/P->0`。TPC-230 transfer 随即给出 literal
matched mass `M/D->0`；bounded-degree comparable-row energy lemma 把同一 stop 推广到
任意 fixed finite primitive linear resonance family。

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
TPC231_STATUS = PROVED_ARITHMETIC_OBSTRUCTION_L1
TPC231_ROUND2_CLUE = TEST_GROWING_RESONANCE_DEPTH_OR_RETURN_TO_THE_ACTUAL_V59_SOURCE_MASS_CROSSWALK
```

TPC-230 上游入口：proof 为
`research/tpc-big-road/bridge_b_matched_resonance_mass_ceiling.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_matched_resonance_mass_ceiling_checker.py`，编号论文为
`papers/tpc-230-matched-resonance-mass-ceiling/`。If `D` is total diagonal mass and `M`
matched mass, exact sharp ceiling is `E_AP>=D-M`. Under row comparability,
`M/D<=2*kappa*E/P`; literal aligned `kappa<=4`, so strict `1/400` requires
`E/P>=1/3200`.

```text
TPC230_UNMATCHED_ENERGY_FLOOR = PROVED_EXACT
TPC230_MATCHED_MASS_SAVING_CEILING = PROVED_EXACT_SHARP
TPC230_NECESSARY_MASS_FRACTION = PROVED_EXACT
TPC230_COMPARABLE_ROW_DENSITY_TOLL = PROVED_EXACT
TPC230_LITERAL_ALIGNED_KAPPA_LE_4 = PROVED_EXACT
TPC230_STRICT_1_OVER_400_EDGE_DENSITY_TOLL = 1/3200
TPC230_ASYMPTOTIC_RESONANCE_EDGE_DENSITY = RESOLVED_BY_TPC231_ZERO
TPC230_ARITHMETIC_ADVANCE = NO
TPC230_FIXED_ATOM_CREDIT = 0
TPC230_L2 = NONE
TPC230_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC230_STATUS = PROVED_STRUCTURAL_L1
TPC230_ROUND2_CLUE = APPLY_A_TWO_LINEAR_FORM_UPPER_BOUND_SIEVE_TO_THE_3_7_RESONANCE_COUNT
```

TPC-229 上游入口：proof 为
`research/tpc-big-road/bridge_b_primitive_resonance_matching_spectrum.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_primitive_resonance_matching_spectrum_checker.py`，编号
论文为 `papers/tpc-229-primitive-resonance-matching-spectrum/`。每条 resonance edge 满足
`10Q/7<p<8Q/5<r<2Q`，故 graph 是 matching；edge spectrum 为
`(-1,-1,+1,+1)`，AP saving iff antisymmetric-mode dominance。

```text
TPC229_RESONANCE_GRAPH_MATCHING = PROVED_EXACT
TPC229_LOW_HIGH_ENDPOINT_SEPARATION = PROVED_EXACT
TPC229_EDGE_SPECTRUM = PROVED_EXACT
TPC229_GLOBAL_BLOCK_DIRECT_SUM = PROVED_EXACT
TPC229_SHARP_AP_RATIO_RANGE = PROVED_EXACT
TPC229_DELTA_SAVING_CRITERION = PROVED_EXACT
TPC229_SOURCE_BILINEAR_BLOCK_BOUND = PROVED_EXACT_SHARP
TPC229_ARITHMETIC_ANTISYMMETRIC_DOMINANCE = OPEN
TPC229_ARITHMETIC_ADVANCE = NO
TPC229_FIXED_ATOM_CREDIT = 0
TPC229_L2 = NONE
TPC229_FULL_GATE_B = OPEN
TPC229_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC229_STATUS = PROVED_STRUCTURAL_L1
TPC229_ROUND2_CLUE = QUANTIFY_MATCHED_RESONANCE_MASS_BEFORE_SEEKING_A_FIXED_PROPORTIONAL_SAVING
```

TPC-228 上游入口：proof 为
`research/tpc-big-road/bridge_b_source_native_polarized_collision_compiler.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_source_native_polarized_collision_compiler_checker.py`，
编号论文为 `papers/tpc-228-source-native-polarized-collision-compiler/`。对 common-profile
source rows `W_q^(j)=U_q+i^jV_q`，exact theorem 给出

```text
1/4 sum_j i^j(E_AP^(j)-E_diag^(j)) = sum_(q!=r)<U_q,V_r>.
```

Q25 first `3--7` resonance 被编译成两个 shared residues 上的四项 beta-w source block；
五个 exact controls 实现正、负、零、单向与单 coordinate，故 geometry 不决定 sign，
但 missing arithmetic object 已被 source-label。

```text
TPC228_ROUTE_ADVANCE = YES
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
TPC228_STATUS = PROVED_STRUCTURAL_L1
TPC228_ROUND2_CLUE = ANALYZE_THE_SOURCE_NATIVE_3_7_COLLISION_GRAPH_AS_EXACT_TWO_BY_TWO_BLOCKS
```

TPC-227 上游入口：proof 为
`research/tpc-big-road/bridge_b_packet_profile_axis_separation.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_packet_profile_axis_separation_checker.py`，编号论文为
`papers/tpc-227-packet-profile-axis-separation/`。V59 literal compiler 把四相位放在
`a^(j)=beta+i^j w` 的 source sequence 上，四包共享一个 `psi_+` profile。TPC-227 对
任意 proposed packet transforms `T_j` 证明 exact iff criterion

```text
1/4 sum_j i^j ||T_j(x+i^j y)||^2 = <Tx,Ty> for every x,y
iff T_j^*T_j=T^*T for all j.
```

global packet signs 是 Gram-invisible；row-dependent signs 可以改变 collision Gram。
TPC-226 Q25 first-resonance block 的 aligned/odd off-diagonal mismatch exact 为
`-1/80000`，所以 finite balanced profile sign 不能自动解释为 V59 source phase。

TPC-227 claim firewall：

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

TPC-226 上游入口：proof 为
`research/tpc-big-road/bridge_b_first_primitive_collision_transition.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_first_primitive_collision_transition_checker.py`，编号论文为
`papers/tpc-226-first-primitive-collision-transition/`。在 finite modeling family
`x=Q^3,H=4Q^2,h_L=4LQ` 上保留 primitive multipliers 后，本篇证明

```text
L=1,2,3: distinct prime rows are pairwise disjoint
L=4: every collision is 7p+3r=16Q with multipliers +/-3 and -/+7.
```

`Q=25`, `(p,r)=(37,47)` 给出 residues `{119,281} mod 400`。aligned 与 inherited
affine profiles 在每个 resonance 上放大 AP energy；balanced odd-sign profiles 则
严格降低 AP energy，并 exact 给出 `E_pol=E_all=0`。505 个尺度的完整分类与 30 个
exact-rational profile records 通过 producer、independent normal/optimized checker 和
primitive-source adversary。dilated clock 是 `MODELING_CHOICE`，V46 transfer 与
arithmetic sign theorem 尚未建立。

TPC-226 claim firewall：

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
TPC226_ARITHMETIC_ADVANCE = NO
TPC226_FIXED_ATOM_CREDIT = 0
TPC226_L2 = NONE
TPC226_FULL_GATE_B = OPEN
TPC226_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC226_STATUS = PROVED_STRUCTURAL_L1
TPC226_ROUND2_CLUE = SOURCE_LOCK_THE_SIGN_OF_THE_3_7_RESONANCE_BEFORE_ANY_UNIFORM_AP_SAVING
```

TPC-225 上游入口：proof 为
`research/tpc-big-road/bridge_b_cutoff_one_shared_clock_obstruction.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_cutoff_one_shared_clock_obstruction_checker.py`，编号论文为
`papers/tpc-225-cutoff-one-shared-clock-obstruction/`。在 TPC-224 的
named source-surrogate clock `x=Q^3,H=4Q^2,h=4Q` 上，literal rows 的 cutoff
严格为 one，distinct prime supports `{q^(-1),-q^(-1)}` 两两不交，因此本篇证明

```text
E_AP = E_diag
E_all = E_pol
```

named clock 上的 strict AP saving 被 scoped-refute。9 个 affine scales、14 个 profile
records 和完整 `Q=3..99` boundary replay 均通过 exact rational checker；这是
structural L1 obstruction，不是 arithmetic advance 或对所有 V46 clocks 的 transfer。

TPC-225 claim firewall：

```text
TPC225_ROUTE_ADVANCE = YES
TPC225_CUTOFF_ONE = PROVED_EXACT
TPC225_SUPPORT_DISJOINTNESS = PROVED_EXACT
TPC225_AP_EQUALS_DIAGONAL = PROVED_EXACT
TPC225_ALL_EQUALS_POLARIZED = PROVED_EXACT
TPC225_AP_SAVING_ON_NAMED_CLOCK = REFUTED_SCOPED
TPC225_POLARIZED_SAVING = PROFILE_DEPENDENT_OPEN
TPC225_V46_CLOCK_TRANSFER = OPEN
TPC225_ARITHMETIC_ADVANCE = NO
TPC225_FIXED_ATOM_CREDIT = 0
TPC225_L2 = NONE
TPC225_FULL_GATE_B = OPEN
TPC225_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC225_STATUS = PROVED_STRUCTURAL_L1
TPC225_ROUND2_CLUE = MOVE_TO_NONTRIVIAL_CUTOFF_CLOCK_BEFORE_CLAIMING_AP_DISPERSION
```

当前 TPC-224 上游入口：proof 为
`research/tpc-big-road/bridge_b_literal_two_channel_compatibility_audit.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_literal_two_channel_compatibility_audit_checker.py`，编号论文为
`papers/tpc-224-literal-two-channel-compatibility-audit/`。对同一组 literal
prime-label/packet-label vectors，定义 `E_AP`、`E_pol` 与 `E_all`，本篇证明

```text
E_all <= min(J E_AP, P E_pol)
      <= PJ/(P+J) (E_AP+E_pol).
```

`PJ/(P+J)` exact sharp；五个独立 collision-stress scales 以 actual primes 与
exact rational rows refute 朴素 unit-factor interface。这个结果只支付 `O(1)` 的
结构兼容性，不支付 AP dispersion、polarized cross-correlation 或 arithmetic `L2`。

TPC-224 claim firewall：

```text
TPC224_ROUTE_ADVANCE = YES
TPC224_COMMON_LITERAL_HILBERT_INTERFACE = PROVED_EXACT
TPC224_SHARP_ADDITIVE_CONSTANT = PROVED_EXACT
TPC224_UNIT_INTERFACE = REFUTED_SCOPED
TPC224_SOURCE_CLOCK_AUDIT = NUMERICALLY_CERTIFIED_EXACT_RATIONAL
TPC224_AP_DISPERSION = OPEN
TPC224_POLARIZED_CROSS_CORRELATION = OPEN
TPC224_LITERAL_V46_TRANSFER = OPEN
TPC224_ARITHMETIC_ADVANCE = NO
TPC224_FIXED_ATOM_CREDIT = 0
TPC224_L2 = NONE
TPC224_FULL_GATE_B = OPEN
TPC224_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

当前 TPC-223 入口：proof 为
`research/tpc-big-road/bridge_b_conditional_signed_reassembly_compiler.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_conditional_signed_reassembly_compiler_checker.py`，编号论文为
`papers/tpc-223-conditional-signed-reassembly-compiler/`。在共同 literal interface
假设

```text
A_x << x^(E0-delta_AP+o(1))
P_x << x^(E0-kappa_pol+o(1))
S_x << x^lambda_struct (A_x+P_x)
```

下，exact compiler 给出

```text
sigma = min(delta_AP,kappa_pol) - lambda_struct.
```

严格 endpoint 条件是 `sigma>1/400`。`E0=5/3` 的 canonical rational fixture
取 `delta_AP=1/100`, `kappa_pol=1/80`, `lambda_struct=1/1200`，得到 effective
saving `11/1200`、strict margin `1/150`、compiled exponent `663/400`；这只是
conditional ledger，三个输入均未被证明。

TPC-223 claim firewall：

```text
TPC223_ROUTE_ADVANCE = YES
TPC223_TWO_CHANNEL_COMPILER = PROVED_CONDITIONAL_ALGEBRA
TPC223_AP_DISPERSION = OPEN_CONDITIONAL_INPUT
TPC223_POLARIZED_CROSS_CORRELATION = OPEN_CONDITIONAL_INPUT
TPC223_LITERAL_REASSEMBLY_INTERFACE = OPEN_CONDITIONAL_INPUT
TPC223_EFFECTIVE_SAVING = CERTIFIED_EXACT_MIN_MINUS_LOSS
TPC223_STRICT_1_OVER_400 = CONDITIONAL_ONLY
TPC223_ARITHMETIC_ADVANCE = NO
TPC223_FIXED_ATOM_CREDIT = 0
TPC223_L2 = NONE
TPC223_FULL_GATE_B = OPEN
TPC223_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

当前 TPC-222 入口：proof 为
`research/tpc-big-road/bridge_b_four_packet_cross_term_obstruction.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_four_packet_cross_term_obstruction_checker.py`，编号论文为
`papers/tpc-222-four-packet-cross-term-obstruction/`。对四个 packet vectors `V_j` 与
Gram matrix `G_(j,l)=<V_j,V_l>`，证明

```text
||sum_j c_j V_j||^2 = c^* G c,
<x,y> = 1/4 sum_(r=0)^3 i^(-r) ||x+i^r y||^2,
0 <= c^* G c <= tr(G) ||c||_2^2.
```

两组 rank-one fixtures `V_j^+=u` 与 `V_j^-=(-1)^j u` 具有相同 diagonal
`(1,1,1,1)` 和 trace `4`，但对 `c=(1,1,1,1)` 的 signed energies 分别为 `16` 与
`0`。因此无符号 diagonal/trace/PSD envelope 在此有限 scope 内不能识别 signed
reassembly；四点极化精确指出缺失的数据是 phase-labelled cross-correlation。

TPC-222 claim firewall：

```text
TPC222_ROUTE_ADVANCE = YES
TPC222_PSD_PACKET_GRAM = PROVED_EXACT
TPC222_FOUR_POINT_POLARIZATION = PROVED_EXACT
TPC222_TRACE_RAYLEIGH_ENVELOPE = PROVED_EXACT
TPC222_SIGNED_CROSS_TERM_IDENTIFIABILITY = REFUTED_SCOPED
TPC222_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC222_ARITHMETIC_ADVANCE = NO
TPC222_FIXED_ATOM_CREDIT = 0
TPC222_L2 = NONE
TPC222_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC222_FULL_GATE_B = OPEN
TPC222_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

当前 TPC-221 入口：proof 为
`research/tpc-big-road/bridge_b_collision_graph_schur_envelope.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_collision_graph_schur_envelope_checker.py`，编号论文为
`papers/tpc-221-collision-graph-schur-envelope/`。TPC-220 的 collision Gram 现在被
组织成 PSD quadratic form，并对任意 q-weights 证明 weighted Schur envelope：

```text
E(lambda) = lambda^* Gamma lambda
  <= max_q p_q^(-1) sum_q' |Gamma(q,q')| p_q' * ||lambda||_2^2.
```

literal saturation fixture 取 `h=5`, `H=500`, constant profile 与
`q={101,151,181,191}`；所有 rows 都是 `e_1+e_4`，所以 `Gamma=2J_4`，Schur radius
和 top Rayleigh quotient 都是 `8`，coherent/diagonal ratio 精确为 `P=4`。这证明
absolute collision-degree control 是结构性上包络，但不能单独击破 q-collapse。

TPC-221 claim firewall：

```text
TPC221_ROUTE_ADVANCE = YES
TPC221_COLLISION_GRAM_PSD = PROVED_EXACT
TPC221_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_WEIGHTED_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_LITERAL_SATURATION = PROVED_EXACT_FINITE
TPC221_ABSOLUTE_SCHUR_SUBP_SAVING = REFUTED_SCOPED
TPC221_ARITHMETIC_ADVANCE = NO
TPC221_FIXED_ATOM_CREDIT = 0
TPC221_L2 = NONE
TPC221_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC221_FULL_GATE_B = OPEN
TPC221_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

当前 TPC-220 入口：proof 为
`research/tpc-big-road/bridge_b_prime_ap_collision_crosswalk.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_prime_ap_collision_crosswalk_checker.py`，编号论文为
`papers/tpc-220-prime-ap-collision-crosswalk/`。TPC-219 的 q-transverse target 现在被
精确写成 literal weighted prime-AP packet：

```text
sum_q lambda_q B_(h,q)^(j)(a)
  = sum_(m != 0) Pi_(h,m)^(j)(a^(-1)m; lambda).
```

同一 literal row family 的 Gram 精确为

```text
Gamma_h^(j,l)(q,q')
  = sum_(m,m') w_(h,m,q)^(j) conjugate(w_(h,m',q')^(l))
      1_(m q' = m' q mod h).
```

在 `q=q'` 且 cutoff injective 时还原 fixed-q atom energy；`q!=q'` 的碰撞边没有被
假设消失。TPC-220 的 exact rational certificate 覆盖 3 个模数、4 个 primes、2 个
profiles，并明确观察到 off-diagonal collision。下一座桥是对该 collision graph 做
Schur 之外的定量控制。

TPC-220 claim firewall：

```text
TPC220_ROUTE_ADVANCE = YES
TPC220_PRIME_AP_CROSSWALK = PROVED_EXACT
TPC220_MULTIPLICATIVE_COLLISION_GRAM = PROVED_EXACT
TPC220_DIAGONAL_REDUCTION = PROVED_EXACT
TPC220_ARITHMETIC_ADVANCE = NO
TPC220_FIXED_ATOM_CREDIT = 0
TPC220_L2 = NONE
TPC220_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC220_FULL_GATE_B = OPEN
TPC220_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

当前 TPC-219 入口：proof 为
`research/tpc-big-road/bridge_b_prime_shell_longitudinal_transverse_ledger.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_prime_shell_longitudinal_transverse_ledger_checker.py`，编号论文为
`papers/tpc-219-prime-shell-longitudinal-ledger/`。对 TPC-218 的 packet vectors
`Z_q(n)=(K_(j,q)(n))_j` 定义 q-mean 与 residual `R_q=Z_q-Zbar`，得到 exact ledger

```text
E_shell = P (E_diag - E_perp).
```

所以要把 `P` collapse 改善到 `eta P`，充要条件是
`E_perp >= (1-eta)E_diag`。aligned fixture 使 `E_perp=0` 并饱和 `P`；balanced
fixture 使 `E_shell=0`。本篇把下一条算术问题精确收窄为 literal prime-AP collision
data 的 transverse lower bound，不把 abstract Hilbert geometry当成 cancellation。

TPC-219 claim firewall：

```text
TPC219_ROUTE_ADVANCE = YES
TPC219_STRUCTURAL_THRESHOLD_A = PASS
TPC219_LONGITUDINAL_TRANSVERSE_IDENTITY = PROVED_EXACT
TPC219_P_COLLAPSE_EQUIVALENCE = PROVED_EXACT
TPC219_ALIGNED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_BALANCED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_ARITHMETIC_ADVANCE = NO
TPC219_FIXED_ATOM_CREDIT = 0
TPC219_L2 = NONE
TPC219_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC219_FULL_GATE_B = OPEN
TPC219_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

当前 TPC-218 入口：proof 为
`research/tpc-big-road/bridge_b_prime_shell_packet_lift.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_prime_shell_packet_lift_checker.py`，编号论文为
`papers/tpc-218-prime-shell-packet-lift/`。在 TPC-217 的 literal finite-window object
上保留 prime label `q` 与 four-packet label `j`，coordinatewise large sieve 给出

```text
N^(-1) sum_(n in I_x)||K_vec(n)||_2^2
  << J M^2 x^(1/96)(log x)^5.
```

逐点合并 q labels 只用 `P<=2Q` 的 Cauchy，恢复
`N^(-1)sum_(n in I_x)sum_j|K_j(n)|^2 << J M^2 x^(11/32)(log x)^5`。
四个 q 的 exact aligned fixture 给出 coherent/diagonal ratio `4=P`；平行 packet
fixture 的 unit-projection ratio 为 `1`。因此 TPC-218 的真实新信息是“split exponent
`1/96` 与 scalar `P` bottleneck 被分离并可审计”，不是 arithmetic saving。

TPC-218 claim firewall：

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
TPC218_ARITHMETIC_ADVANCE = NO
TPC218_FIXED_ATOM_CREDIT = 0
TPC218_L2 = NONE
TPC218_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC218_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC218_FULL_GATE_B = OPEN
TPC218_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
```

当前 TPC-217 入口：proof 为
`research/tpc-big-road/bridge_b_finite_window_rational_large_sieve.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_finite_window_rational_large_sieve_checker.py`，编号论文为
`papers/tpc-217-finite-window-rational-large-sieve/`。在同一个 literal V46 common-source
kernel 上，TPC-217 exact regrouping by reduced rational frequencies、Farey spacing 与
standard additive large sieve 将 TPC-216 的 complete-period envelope 接到
`I_x=(x/2,x]`：
`N^(-1)sum_(n in I_x)|K(n)|^2 <<_psi x^(11/32)(log x)^5`，且
`U^2/x=x^(-67/200)` 为 lower-order window term。finite aligned one-point fixture 的
coherent-to-diagonal ratio 恰为 `2`，所以 free finite-window orthogonality 仍为
`REFUTED_SCOPED`。prime-shell/four-packet signed reassembly、arithmetic `L2`、full Gate B、
fixed-atom credit、strict `1/400` 与 TPC endpoint 仍 OPEN/UNPAID/NO。

当前 TPC-216 入口：proof 为
`research/tpc-big-road/bridge_b_direct_sum_row_energy_envelope.md`，checker 为
`research/tpc-big-road/tpc_bridge_b_direct_sum_row_energy_envelope_checker.py`，编号论文为
`papers/tpc-216-direct-sum-row-energy-envelope/`。source inequality `4Q<H` 使 fixed-q
integer atoms 在模 `d` 下 exact 不碰撞；shell Cauchy、`P<=2Q` 与 Mobius-log divisor
sum 给出 complete-period normalized envelope
`L^(-1)E_direct <<_psi x^(11/32)(log x)^3`。exact rational fixture 中四个 prime rows
全部支撑在 `{1,4} mod 5`，所以 free q-orthogonality 被 `REFUTED_SCOPED`。finite-window
off-frequency Gram 已由 TPC-217 以 large sieve 控制；prime-shell/four-packet reassembly、
full Gate B、`L2`、fixed-atom credit 与 TPC endpoint 仍 OPEN。

TPC-215 直接上游入口：proof 为
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
