# TPC big-road paper candidate ledger

更新时间：2026-08-24

状态：**TPC236_PROVED_STRUCTURAL_L1_RELEASED / PHYSICAL_MULTIWRAP_BESSEL_ENVELOPE / CROSS_H_REASSEMBLY_OPEN**

本文件与路线图平行维护，作用是把连续探索中的可发表材料从长篇 handoff 中逐步抽出。
它不是 theorem evidence；正式数学状态仍以
当前 proof、checker、TPC_HANDOFF.md 页首及 current section 为准。

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
