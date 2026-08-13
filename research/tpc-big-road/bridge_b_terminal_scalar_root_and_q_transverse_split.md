# Bridge A / Gate B V58: terminal scalar root and q-transverse variance split

Date: 2026-08-13

## 0. Outcome and claim firewall

V57 used one full-shell Gate-A root together with a full Gate-B row-Bessel
theorem.  V58 separates what that Gate-B row theorem was doing.  Its
longitudinal component is exactly the V35 proper-factor centered ratio core;
that one signed scalar, rather than the whole row energy, is all that the
physical endpoint consumes.  The orthogonal (q)-transverse component is
needed only if one also wants uniform moving prime-shell prefixes.

This is a route-level exact compiler.  It proves no new cancellation:

~~~text
V58_ROUTE_ADVANCE = YES
V58_CONDITIONAL_BRIDGE_ADVANCE = YES
V58_ARITHMETIC_ADVANCE = NO
V58_FIXED_ATOM_CREDIT = 0
V58_STRICT_1_OVER_400 = UNPAID
V58_L2 = NONE
V58_TPC_207_TRIGGER = false
V58_NUMBERED_RELEASE = NO
~~~

The maximum legal claim is that the selected physical-endpoint route now has
two signed scalar roots: the V51 full-shell Gate-A fold and the V35
proper-factor Gate-B core.  Neither root estimate is proved here.

## 1. Frozen rows and the full-shell scalar

Keep

\[
 H=x^{21/32},\qquad Q=x^{1/3},\qquad
 T_{\rm num}=\frac{1997}{1200},
 \tag{1.1}
\]

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},
 \tag{1.2}
\]

\[
 w(u)=\Lambda(u+2)-b_x^{(z)}(u),\qquad
 K_H(h)=\widehat\psi_+(h/H).
 \tag{1.3}
\]

V54 supplies the literal paired rows

\[
 P_q=\sum_{\substack{t\in I_x\\q\nmid t}}
       \beta^\circ(t)\mathcal R_q(t),\qquad
 C_q=\sum_{\substack{t\in I_x\\q\nmid t}}
       \beta(t)\mathcal G_q(t),
 \tag{1.4}
\]

and the exact identity

\[
 \boxed{P_q-C_q=\kappa_qS_x-E_q},\qquad
 \kappa_q=\frac{q-2}{q-1}.
 \tag{1.5}
\]

Here \(S_x=\sum_t\beta(t)w(t)\), \(E_q=\kappa_qU_q+Y_q^\square\),
and all (+2/-1), Möbius, hybrid, square, unit-mask, and deleted-diagonal
data are retained.  Define

\[
 A_*:=\sum_{q\in\mathcal Q}qP_q,\qquad
 C_*:=\sum_{q\in\mathcal Q}qC_q,
 \tag{1.6}
\]

\[
 E_*:=\sum_{q\in\mathcal Q}qE_q,\qquad
 K_*:=\sum_{q\in\mathcal Q}q\kappa_q=x^{2/3+o(1)}.
 \tag{1.7}
\]

Summing (1.5) gives the terminal readout

\[
 \boxed{S_x=\frac{A_*-C_*+E_*}{K_*}.}
 \tag{1.8}
\]

The already-paid error satisfies

\[
 |E_*|\ll x^{143/96+o(1)},\qquad
 \frac{143}{96}-\frac23=\frac{79}{96},
 \tag{1.9}
\]

\[
 \frac{399}{400}-\frac{79}{96}=\frac{419}{2400}.
 \tag{1.10}
\]

## 2. Exact V35--V57 scalar crosswalk

For \(q\nmid t\), expanding the definition of \(\mathcal R_q\) and deleting
the physical diagonal gives

\[
 \boxed{
 \mathcal G_q(t)=
 \sum_{\substack{u\in I_x\\u\ne t\\q\nmid u}}
 w(u)K_H(u-t)c'_q(u-t),}
 \tag{2.1}
\]

where

\[
 c'_q(h)=\mathbf1_{q\mid h}-\frac1{q-1}.
 \tag{2.2}
\]

On the unit rows,

\[
 c'_q(u-t)=u_1(u\overline t;q),\qquad
 u_1(a;q)=\mathbf1_{a\equiv1\pmod q}-\frac1{q-1}.
 \tag{2.3}
\]

The full marginal in (1.4) is exactly V35's

\[
 \beta(t)=\beta_x^{\rm raw}(t)
 =\sum_{\substack{dk=t\\d,k\geq2}}\mu(d)\omega_x(d,k).
 \tag{2.4}
\]

Substituting (2.1)--(2.4) into \(C_*\), before any absolute value, proves

\[
 \begin{aligned}
 C_*={}&\sum_{q\in\mathcal Q}q
 \sum_{\substack{dk,u\in I_x\\d,k\geq2,\ u\ne dk\\q\nmid dku}}
 \mu(d)\omega_x(d,k)w(u)K_H(u-dk)
 u_1(u\overline{dk};q)\\
 ={}&\boxed{\mathfrak C_x^{\rm V35}}.
 \end{aligned}
 \tag{2.5}
\]

This is not a comparison up to remainders.  V35's unit-principal and nonunit
terms belong to its larger compensated numerator \(\mathfrak D_x\); the
V57 row \(\mathcal G_q\) is already unit-restricted and centered, so its
full-shell scalar is precisely the surviving core (2.5).

Consequently the V35 open theorem

\[
 \boxed{|\mathfrak C_x|\ll x^{5/3-\delta+o(1)},\qquad
 \delta>\frac1{400}}
 \tag{2.6}
\]

is exactly a Gate-B theorem for \(C_*\), not merely an architectural
analogue.

## 3. Exact longitudinal--transverse decomposition of the row

Put

\[
 \mathbf C=(C_q)_{q\in\mathcal Q},\qquad
 \mathbf v=(q)_{q\in\mathcal Q},\qquad
 V_*:=\|\mathbf v\|_2^2=\sum_{q\in\mathcal Q}q^2=x^{1+o(1)}.
 \tag{3.1}
\]

With \(\langle a,b\rangle=\sum_q a_q\overline{b_q}\), one has

\[
 C_*=\langle\mathbf C,\mathbf v\rangle.
 \tag{3.2}
\]

Define the orthogonal component

\[
 \mathbf C^\perp=
 \mathbf C-\frac{C_*}{V_*}\mathbf v.
 \tag{3.3}
\]

Then

\[
 \boxed{\langle\mathbf C^\perp,\mathbf v\rangle=0},
 \tag{3.4}
\]

and Pythagoras gives the exact direct sum

\[
 \boxed{
 \sum_{q\in\mathcal Q}|C_q|^2
 =\frac{|C_*|^2}{V_*}+\|\mathbf C^\perp\|_2^2.}
 \tag{3.5}
\]

V53 formulated a relative row-Bessel hypothesis using the collision diagonal
\(\mathcal D_B^{\rm row}\).  Since only the proved upper bound

\[
 \mathcal D_B^{\rm row}\ll x^{95/48+o(1)}
 \tag{3.6}
\]

is consumed by V57, it is useful to distinguish the resulting absolute
power-scale envelope

\[
 \mathsf H_B^{\rm abs}(\tau):\qquad
 \|\mathbf C\|_2^2\ll x^{95/48+\tau+o(1)}
 \tag{3.7}
\]

from the stronger relative V53 statement.  By (3.5), (3.7) is equivalent up
to an absolute factor two, hence with no exponent loss, to the conjunction

\[
 \frac{|C_*|^2}{V_*}\ll x^{95/48+\tau_\parallel+o(1)},
 \qquad
 \|\mathbf C^\perp\|_2^2\ll
 x^{95/48+\tau_\perp+o(1)},
 \tag{3.8}
\]

with \(\max(\tau_\parallel,\tau_\perp)\leq\tau\).  No converse from
the absolute envelope to the relative collision-diagonal inequality is
claimed.

## 4. Exact exponent crosswalk

If (2.6) holds, then the longitudinal energy in (3.8) has exponent

\[
 \frac{|C_*|^2}{V_*}
 \ll x^{2(5/3-\delta)-1+o(1)}
 =x^{7/3-2\delta+o(1)}.
 \tag{4.1}
\]

Relative to the paid diagonal exponent (95/48), this corresponds to

\[
 \boxed{\tau_\parallel=\frac{17}{48}-2\delta.}
 \tag{4.2}
\]

The strict thresholds match exactly:

\[
 \delta>\frac1{400}
 \quad\Longleftrightarrow\quad
 \tau_\parallel<\frac{17}{48}-\frac1{200}
 =\boxed{\frac{419}{1200}}.
 \tag{4.3}
\]

At the standard point

\[
 \delta=\frac1{96},\qquad
 \tau_\parallel=\frac13,
 \tag{4.4}
\]

and

\[
 |C_*|\ll x^{53/32+o(1)},\qquad
 \frac{53}{32}-\frac23=\frac{95}{96}.
 \tag{4.5}
\]

Thus V35's scalar saving and V57's longitudinal portion of the selected row
loss are the same exponent ledger in two coordinate systems.

## 5. Two-scalar endpoint compiler

Retain the V51 full-shell Gate-A hypothesis

\[
 \mathsf H_{A,*}(\eta_A):\qquad
 |A_*|\ll x^{1997/1200-\eta_A+o(1)},\qquad \eta_A>0,
 \tag{5.1}
\]

and the V35 Gate-B scalar hypothesis (2.6).

### Theorem 5.1 (conditional two-scalar endpoint compiler)

Assume (5.1) and (2.6) for fixed \(\eta_A>0\) and
\(\delta>1/400\).  Then

\[
 |S_x|\ll x^{399/400-\eta+o(1)}
 \tag{5.2}
\]

for every

\[
 \boxed{
 0<\eta<\min\left\{
 \eta_A,\ \delta-\frac1{400},\ \frac{419}{2400}
 \right\}.}
 \tag{5.3}
\]

### Proof

Insert (5.1), (2.6), and (1.9) into (1.8), then use
\(K_*=x^{2/3+o(1)}\).  The three physical exponents are respectively
\(399/400-\eta_A\), \(1-\delta\), and \(79/96\).  Their margins to
\(399/400\) are the three entries in (5.3).  \(\square\)

At \(\delta=1/96\), the Gate-B term gives

\[
 |S_x|\ll x^{95/96+o(1)},\qquad
 \frac{399}{400}-\frac{95}{96}=\frac{19}{2400},
 \tag{5.4}
\]

provided Gate A has at least the same margin.  The theorem uses no estimate
for \(\mathbf C^\perp\).  Therefore a full Gate-B row-Bessel theorem is not a
necessary premise on the selected physical-endpoint route.

## 6. Optional maximal-prefix extension

The transverse component still has a precise role.  For \(Q<Y\leq2Q\), put

\[
 \mathbf v_Y=(q\mathbf1_{q\leq Y})_{q\in\mathcal Q},\qquad
 V(Y)=\|\mathbf v_Y\|_2^2,qquad s_Y=\frac{V(Y)}{V_*}.
 \tag{6.1}
\]

Then

\[
 \boxed{C(Y)-s_YC_*=\langle\mathbf C^\perp,\mathbf v_Y\rangle,}
 \tag{6.2}
\]

and

\[
 \left\|\mathbf v_Y-s_Y\mathbf v\right\|_2^2
 =V(Y)\left(1-\frac{V(Y)}{V_*}\right)
 \leq\frac{V_*}{4}.
 \tag{6.3}
\]

Consequently the transverse estimate in (3.8) gives

\[
 \sup_Y|C(Y)-s_YC_*|
 \ll x^{143/96+\tau_\perp/2+o(1)}.
 \tag{6.4}
\]

V57 uses instead \(r_Y=K(Y)/K_*\).  The exact conversion is

\[
 C(Y)-r_YC_*
 =[C(Y)-s_YC_*]+(s_Y-r_Y)C_*.
 \tag{6.5}
\]

Thus the V35 scalar root plus a transverse row theorem controls all V57
prefixes.  The scalar root alone controls the physical endpoint but not the
moving prefixes.  The transverse theorem is therefore an optional maximal
Gate-A railing, not an endpoint pier.

## 7. Route consequences and firewalls

1. **Selected endpoint route.**  Prove the V51 signed full-shell root (5.1)
   and the V35 signed ratio core (2.6).  This is now the narrowest explicit
   two-pier sufficient package.
2. **Optional maximal route.**  Add a (q)-transverse estimate for
   \(\mathbf C^\perp\) only if all Gate-A prefixes are required.
3. **V53/V57 row-Bessel remains valid but stronger for the endpoint.**  Its
   relative collision-diagonal form implies the consumed absolute row
   envelope, which bundles both (2.6)'s direction and the transverse
   variance.
4. **No cancellation is borrowed.**  Bounding \(A_*-C_*\) directly is the
   physical terminal theorem itself by (1.8); it is not a preliminary gate.
5. **Neither scalar may be dropped.**  A bound for \(A_*\) alone leaves
   \(C_*\) arbitrary, and conversely.
6. **No transverse credit enters the endpoint.**  Projection onto
   \(\mathbf v^\perp\) deletes the coordinate read by \(C_*\).
7. **No theorem promotion.**  The exact split and crosswalk receive L0 route
   credit only; arithmetic status remains NO.

## 8. Primary-source boundary

The source screen is fail-closed as of 2026-08-13.

1. [Wright, arXiv:2604.25177v2](https://arxiv.org/html/2604.25177v2),
   Corollary 2.2, treats two divisor-bounded, \(q\)-independent convolution
   arrays, a fixed residue \(a\), an outer \(L^1\) modulus average, and a
   Siegel--Walfisz input.  The literal core (2.5) has a moving ratio
   \(u\overline{dk}\), a third physical \(w\)-array, short difference support,
   and a deleted diagonal.
2. [Drappeau, arXiv:1504.05549](https://arxiv.org/abs/1504.05549)
   provides powerful dispersion/Kloosterman architecture for convolution
   sequences in progressions.  It does not supply the occurrence-native
   three-array scalar (2.5) with the V19 signs and hybrid coefficient.
3. [Fouvry--Radziwiłł, arXiv:1811.08672](https://arxiv.org/abs/1811.08672)
   treats unbalanced two-sequence convolutions with a tiny
   Siegel--Walfisz factor.  It has no literal compiler for (2.5).
4. [Blomer--Pascadi, arXiv:2607.24311](https://arxiv.org/abs/2607.24311)
   is a fixed-modulus bilinear Kloosterman engine after an emitter has been
   constructed; it does not prove the whole prime-shell scalar.
5. [Harper, arXiv:2412.19644](https://arxiv.org/abs/2412.19644)
   gives general-sequence BDH asymptotics for one fixed sequence in a
   different modulus regime, not the moving-ratio scalar or its transverse
   row.

No checked primary theorem proves either (5.1) or (2.6).  The first fatal is
now two explicit signed scalar theorems, rather than one signed scalar plus a
full Gate-B row-energy theorem.

## 9. Finite exact fixtures

Take

\[
 \mathbf v=(5,7,11),\qquad \mathbf C=(4,-5,6).
 \tag{9.1}
\]

Then

\[
 V_*=195,\qquad C_*=51,\qquad \frac{C_*}{V_*}=\frac{17}{65},
 \tag{9.2}
\]

\[
 \mathbf C^\perp=
 \left(\frac{35}{13},-\frac{444}{65},\frac{203}{65}\right),
 \qquad \langle\mathbf C^\perp,\mathbf v\rangle=0.
 \tag{9.3}
\]

The exact energy split is

\[
 77=\frac{867}{65}+\frac{4138}{65}.
 \tag{9.4}
\]

For the first two nontrivial prefixes, (6.2) gives

\[
 20-\frac5{39}\,51=\frac{175}{13},
 \tag{9.5}
\]

\[
 -15-\frac{74}{195}\,51=-\frac{2233}{65}.
 \tag{9.6}
\]

For the kernel crosswalk, at \(q=5,t=6\), the choices \(u=11\) and \(u=8\)
give respectively

\[
 c'_5(u-t)=u_1(u\overline t;5)=\frac34,qquad -\frac14.
 \tag{9.7}
\]

The checker also freezes the strict threshold, the benchmark
\((\delta,\tau_\parallel)=(1/96,1/3)\), the prefix projection norm, and
mutations of the (q)-weight, centering coefficient, deleted diagonal, and
error sign.

## 10. Canonical registry

~~~text
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
~~~
