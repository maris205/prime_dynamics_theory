# Bridge A / Gates A--B V48: exact conductor--Euler splice and the low-conductor signed prime--hybrid gate

Date: 2026-08-11

Status: unnumbered big-road research artifact. V45 decomposed the common
transition scalar by primitive conductor, V46 decomposed the same scalar into
an occurrence-native Euler profile and an AP residual, and V47 centered the
additive AP residual. V48 proves that these are two exact decompositions of one
literal scalar. The previously open V45-to-V47 splice is therefore closed
before the first outer absolute value. The source-backed V45 high-conductor
payment and the V46 local Euler payment leave one low-conductor signed
prime--hybrid scalar. A stronger character-energy formulation is recorded as
a theorem-friendly sufficient gate. No checked primary theorem proves either
gate with the fixed power required at the \(1/400\) endpoint. Thus V48 is a
macro route advance, not arithmetic credit.

## 1. Frozen transition scalar and scales

Keep

\[
 H=x^{21/32},\qquad Q=x^{1/3},\qquad
 U=x^{133/400},\qquad Y_0=\frac{H}{4Q}=x^{31/96+o(1)},
 \tag{1.1}
\]

\[
 P=\frac{Q^2}{H}=x^{1/96},\qquad
 D_0=P^{1/2}=x^{1/192},\qquad
 L_{\rm pr}=x^{2/3+o(1)}.
 \tag{1.2}
\]

Let

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},
 \tag{1.3}
\]

\[
 w(u)=\Lambda(u+2)-b_x^{(z)}(u).
 \tag{1.4}
\]

The common transition scalar frozen in V43--V47 is

\[
 \begin{aligned}
 \mathfrak T_x^{\rm com}
 ={}&-H\sum_{q\in\mathcal Q}
 \sum_{Y_0<D\leq U}\frac{\mu(D)\log D}{D}
 \sum_{\substack{m\ne0\\|m|\leq Dq/H}}
 \psi\!\left(\frac{Hm}{Dq}\right)\\
 &\hspace{18mm}\times
 \sum_{u\in I_x}\frac{w(u)}{\log u}
 e_D(mu\overline q_D).
 \end{aligned}
 \tag{1.5}
\]

All inverse residues in (1.5) are legal because \(D<U<Q<q\), while
\(\mu(D)\ne0\) restricts \(D\) to square-free moduli. The V44 physical
\(q\mid u\) correction and background remain

\[
 \mathfrak A_x^{\rm tr}=\mathfrak T_x^{\rm com}
 +O\!\left(x^{319/192+o(1)}+x^{7171/4800+o(1)}\right).
 \tag{1.6}
\]

Nothing below changes the signs, the \(+2\) shift, the hybrid comparator, the
hard shell, or the single outer absolute in this identity.

## 2. Exact gcd reduction: the V45 object is (1.5)

For each active pair \((D,m)\), put

\[
 g=(|m|,D),\qquad s=D/g,\qquad n=m/g.
 \tag{2.1}
\]

Since \(D\) is square-free,

\[
 (g,s)=1,\qquad (n,s)=1.
 \tag{2.2}
\]

Reduction of a rational additive phase gives, for every integer \(u\),

\[
 \boxed{
 e_D(mu\overline q_D)=e_s(nu\overline q_s),\qquad
 \psi\!\left(\frac{Hm}{Dq}\right)
 =\psi\!\left(\frac{Hn}{sq}\right).}
 \tag{2.3}
\]

Conversely, every square-free \(D=gs\) with \((g,s)=1\) and every
\((n,s)=1\) reconstructs the original frequency \(m=gn\). Summing the
original coefficient over \(g\) produces exactly the V44--V45 coefficient

\[
 \boxed{
 \lambda_s=-\sum_{\substack{g\geq1,(g,s)=1\\Y_0<gs\leq U}}
 \frac{\mu(gs)\log(gs)}{gs}.}
 \tag{2.4}
\]

Thus the V45 reduced-modulus scalar is not a model or a second copy of the
transition window. It is exactly (1.5), reorganized by the reduced modulus
\(s=D/(m,D)\). In particular,

\[
 \boxed{
 \mathfrak T_x^{\rm com}
 =\mathfrak M_{<D_0}^{\rm tr}
 +\mathfrak V_{\geq D_0}^{\rm tr}.}
 \tag{2.5}
\]

Here the two terms are V45's primitive-conductor split. The closing
identity is exact before any outer absolute. In the remainder of this note we
also use the equivalent unboxed form

\[
 \mathfrak T_x^{\rm com}
 =\mathfrak M_{<D_0}^{\rm tr}
 +\mathfrak V_{\geq D_0}^{\rm tr}.
 \tag{2.6}
\]

## 3. Exact scalar splice with V46--V47

V46 proved, before the first outer absolute,

\[
 \boxed{
 \mathfrak T_x^{\rm com}
 =\mathfrak L_x^{\rm pf}+\mathfrak R_x^{\rm AP}.}
 \tag{3.1}
\]

Combining (2.6) and (3.1) gives the missing splice:

\[
 \boxed{
 \mathfrak R_x^{\rm AP}
 =\mathfrak M_{<D_0}^{\rm tr}
 +\mathfrak V_{\geq D_0}^{\rm tr}
 -\mathfrak L_x^{\rm pf}.}
 \tag{3.2}
\]

Define

\[
 \mathfrak E_x^{\rm splice}
 :=\mathfrak V_{\geq D_0}^{\rm tr}-\mathfrak L_x^{\rm pf}.
 \tag{3.3}
\]

The two already proved bounds are

\[
 |\mathfrak V_{\geq D_0}^{\rm tr}|
 \ll x^{213/128+o(1)},\qquad
 |\mathfrak L_x^{\rm pf}|
 \ll x^{1057/640+o(1)}.
 \tag{3.4}
\]

Therefore

\[
 \boxed{
 |\mathfrak E_x^{\rm splice}|
 \ll x^{213/128+o(1)},\qquad
 \frac{1997}{1200}-\frac{213}{128}=\frac1{9600}.}
 \tag{3.5}
\]

Equations (3.2)--(3.5) close V47's `OPEN_EXACT_PROJECTION_COMPILER` at the
scalar level. They do not assert that either summand is an orthogonal
projection of the V47 centered AP energy.

## 4. Why energy subtraction is invalid

The gcd reduction in Section 2 aggregates all original fibers \(D=gs\) into
one coefficient at the same reduced modulus \(s\). Aggregation occurs before
the character transform. Squaring before and after this aggregation gives
different objects:

\[
 \sum_g|a_{g,s}|^2\ne\left|\sum_g a_{g,s}\right|^2
 \tag{4.1}
\]

in general. The two-fiber fixture \(a_{g_1,s}=1\), \(a_{g_2,s}=-1\) has
direct energy \(2\) and aggregate energy \(0\). Hence

```text
V45 high-conductor energy
  is not an orthogonal subenergy of
V47 centered all-residue AP energy.
```

Subtracting those energies would be false. The legal operation is the signed
scalar splice (3.2), before the first outer absolute.

There is a second, complementary decomposition inside one original modulus
\(D\). Partition residues by \(h=(a,D)\), set \(s=D/h\), and write
\(a=hb\) with \(b\in G_s\). For a centered residue vector
\(R_D^\circ\), define

\[
 \mu_{D,h}=\frac1{\varphi(s)}\sum_{b\in G_s}R_D^\circ(hb).
 \tag{4.2}
\]

Character Parseval on each gcd stratum gives the exact ANOVA identity

\[
 \boxed{
 \begin{aligned}
 \sum_{a\bmod D}|R_D^\circ(a)|^2
 ={}&\sum_{h\mid D}\frac1{\varphi(s)}
 \sum_{\substack{\chi\ ({\rm mod}\ s)\\\chi\ne\chi_0}}
 \left|\sum_{b\in G_s}R_D^\circ(hb)\overline{\chi(b)}\right|^2\\
 &+\sum_{h\mid D}\varphi(s)|\mu_{D,h}|^2.
 \end{aligned}}
 \tag{4.3}
\]

Global additive centering gives only

\[
 \sum_{h\mid D}\varphi(s)\mu_{D,h}=0.
 \tag{4.4}
\]

It does not delete the principal mean of each gcd stratum. Identity (4.3)
explains why V47's additive centering does not remove the low multiplicative
principal/induced tower. It is not the same operation as the cross-\(D\)
aggregation in Section 2.

## 5. Explicit low-conductor signed block

Write a reduced square-free modulus as \(s=ce\), with
\((c,e)=1\), and let \(\chi^*\pmod c\) be primitive. Define

\[
 \begin{aligned}
 K_{c,e}(\chi^*)
 :=\sum_{q\in\mathcal Q}
 \sum_{\substack{0<|n|\le ceq/H\\(n,ce)=1}}
 \psi\!\left(\frac{Hn}{ceq}\right)
 \overline{\chi^*(n)}\chi^*(q),
 \end{aligned}
 \tag{5.1}
\]

\[
 W_{c,e}(\chi^*)
 :=\sum_{u\in I_x}\frac{\Lambda(u+2)-b_x^{(z)}(u)}{\log u}
 \overline{\chi^*(u)}c_e(u).
 \tag{5.2}
\]

The V45 Gauss--Ramanujan identity gives exactly

\[
 \boxed{
 \begin{aligned}
 \mathfrak M_{<D_0}^{\rm tr}
 =H\sum_{\substack{s=ce,\ \mu^2(ce)=1\\(c,e)=1,\ c<D_0}}
 \frac{\lambda_{ce}}{\varphi(ce)}
 \sum_{\chi^*\ ({\rm mod}\ c)}^*
 \tau(\chi^*)\chi^*(e)
 K_{c,e}(\chi^*)W_{c,e}(\chi^*).
 \end{aligned}}
 \tag{5.3}
\]

The extension of \(\chi^*\) by zero handles \((u,c)>1\). The signed physical
block splits, still exactly, as

\[
 W_{c,e}=W_{c,e}^{\Lambda}-W_{c,e}^{B}.
 \tag{5.4}
\]

The conductor-one principal row, every \(1<c<D_0\) induced row, and any
possible exceptional real character remain inside (5.3). V48 does not delete,
average away, or rename them.

## 6. One source-native sufficient energy gate

In the V45 notation, let

\[
 \mathcal K_<
 :=\sum_s\frac1{\varphi(s)}
 \sum_{\substack{\chi\ ({\rm mod}\ s)\\{\rm cond}(\chi)<D_0}}
 |\widehat C_s(\chi)|^2.
 \tag{6.1}
\]

The already proved conductor-block ledger gives

\[
 \boxed{\mathcal K_<\ll P^2x^{o(1)}.}
 \tag{6.2}
\]

Define the physical signed low-conductor energy

\[
 \mathcal W_<
 :=\sum_s\frac1{\varphi(s)}
 \sum_{\substack{\chi\ ({\rm mod}\ s)\\{\rm cond}(\chi)<D_0}}
 |\check F_s(\chi)|^2,
 \tag{6.3}
\]

where \(\check F_s\) contains the literal coefficient
\((\Lambda(u+2)-b_x^{(z)}(u))/\log u\). Full character Parseval only gives

\[
 \mathcal W_<\leq x^{2+o(1)}.
 \tag{6.4}
\]

Cauchy in the exact character expansion yields

\[
 |\mathfrak M_{<D_0}^{\rm tr}|
 \leq H\mathcal K_<^{1/2}\mathcal W_<^{1/2}.
 \tag{6.5}
\]

The ceiling (6.4) therefore gives only

\[
 HPx=x^{5/3+o(1)},
 \tag{6.6}
\]

which misses the numerator target \(x^{1997/1200}\) by exactly \(1/400\).
A sufficient source-native theorem is

\[
 \boxed{
 \mathsf E_{<}(\delta):\quad
 \mathcal W_<\ll x^{2-\delta+o(1)},\qquad
 \delta>\frac1{200}.}
 \tag{6.7}
\]

Indeed, (6.2), (6.5), and (6.7) give

\[
 \boxed{
 |\mathfrak M_{<D_0}^{\rm tr}|
 \ll x^{5/3-\delta/2+o(1)},\qquad
 \eta_< <\frac\delta2-\frac1{400}.}
 \tag{6.8}
\]

This energy theorem is sufficient, not equivalent to the scalar target. It
retains the prime--hybrid sign inside one squared whole object, but it still
pays all low rows in \(L^2\).

## 7. Weakest scalar gate and terminal compiler

The weakest gate exposed by the exact splice is simply

\[
 \boxed{
 \mathsf H_{<D_0}(\eta_<):\quad
 |\mathfrak M_{<D_0}^{\rm tr}|
 \ll x^{1997/1200-\eta_<+o(1)},\qquad \eta_<>0.}
 \tag{7.1}
\]

It is logically weaker as a requested theorem contract than (6.7); no
literal-family converse or strictness theorem is claimed. Under (7.1),
(3.2)--(3.5) give the same fixed-power estimate for the V47 AP residual.
Conversely, a fixed-power theorem for that residual gives (7.1) after adding
the paid splice. Thus the two scalar formulations are terminal-equivalent
modulo already paid terms; the V47 centered energy hypothesis is a stronger
sufficient theorem.

Combining (1.6), (2.6), (3.4), and (7.1), the transition window is paid with
any

\[
 \boxed{
 \eta_{\rm tr}<\min\!\left\{
 \eta_<,\frac1{9600},\frac{13}{4800},\frac{817}{4800}
 \right\}.}
 \tag{7.2}
\]

If the energy gate (6.7) is used, one may take

\[
 \eta_<<\frac\delta2-\frac1{400}.
 \tag{7.3}
\]

No endpoint equality is accepted.

## 8. Source screen and first fatal

The screen is primary-source-only and fail-closed as of 2026-08-11.

1. Bombieri--Friedlander--Iwaniec,
   [*Primes in arithmetic progressions to large moduli*, Theorem 0 and
   (1.6)](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6385-11511_2006_Article_BF02399204.pdf),
   supports the primitive-conductor split and the high-conductor second/fourth
   moment machinery used by V45. Its low-conductor branch is based on a
   Siegel--Walfisz hypothesis and gives logarithmic, not fixed-power, control.

2. Conrey--Iwaniec--Soundararajan,
   [*Asymptotic Large Sieve*, arXiv:1105.1176](https://arxiv.org/abs/1105.1176),
   gives an asymptotic primitive-character large sieve. Its coefficient class
   and bilinear asymptotic do not identify the literal signed block (5.2).

3. Matomaki--Teravainen,
   [*Products of primes in arithmetic progressions*,
   arXiv:2301.07679](https://arxiv.org/abs/2301.07679), uses a multiplicative
   dense model and explicitly retains a possible quadratic obstruction. Its
   ternary prime-product problem and Burgess-scale interface do not prove
   (6.7) or (7.1).

4. Runbo Li,
   [*Primes in arithmetic progressions to large moduli and refinements of
   Harman's sieve*, arXiv:2602.20917v6](https://arxiv.org/abs/2602.20917),
   proves mean-value theorems for primes with bilinear/trilinear modulus
   weights and constructs separate prime majorants and minorants. Those are
   fixed-residue or averaged-distribution estimates with logarithmic error;
   they do not preserve the exact comparator \(b_x^{(z)}\), the Ramanujan
   factor \(c_e(u)\), and the signed character energy (6.3) jointly.

5. Daniel R. Johnston,
   [*An effective Bombieri--Vinogradov error term for sifting problems*,
   arXiv:2510.10853v2](https://arxiv.org/abs/2510.10853), makes classical
   Bombieri--Vinogradov sifting errors effective by avoiding a Siegel-zero
   obstruction. It does not change the asymptotic norm or supply the literal
   fixed-power signed low-conductor estimate.

No checked theorem accepts the occurrence-native

\[
 \frac{\Lambda(u+2)-b_x^{(z)}(u)}{\log u}
 \overline{\chi^*(u)}c_e(u)
 \tag{8.1}
\]

for the complete V48 low-conductor tower and proves either (6.7) with
\(\delta>1/200\) or the direct scalar gate (7.1). This is the first analytic
fatal. It is a new-theorem boundary, not evidence that the theorem is false.

## 9. Finite exact diagnostics

The checker freezes the following facts.

1. For \(D\in\{6,10,15,30\}\), \(q=7\), and every
   \(0<|m|<D\), all 114 gcd-reduction rows satisfy (2.2)--(2.3).

2. On the two-point unit group \(G_3\), take occupancy \(C=(3,1)\), total
   physical vector \(F=(5,2)\), local vector \(L=(1,2)\), and residual
   \(R=F-L=(4,0)\). Then

   \[
   T=17=14+3,\qquad L=5=6-1,\qquad
   R=12=8+4=14+3-5.
   \tag{9.1}
   \]

   This catches the sign in (3.2) and verifies low/high reassembly.

3. Prime and hybrid physical vectors \((8,3)\) and \((3,1)\) have principal
   transforms \(11\) and \(4\); the signed transform is \(7=11-4\).

4. The two-fiber aggregation fixture has direct energy \(2\) and aggregate
   energy \(0\), rejecting energy subtraction.

5. For \(D=6\), the centered vector
   \((5,-2,1,-3,0,-1)\) has total energy \(40\). Its four gcd strata have
   within-character energy \(1\) and principal-stratum energy \(39\), exactly
   as in (4.3). Global centering does not remove those principal strata.

6. The rational exponent ledger freezes
   \(HPx=x^{5/3}\), the endpoint deficit \(1/400\), the energy threshold
   \(\delta>1/200\), the V45 high margin \(1/9600\), and the V46 local margin
   \(121/9600\).

These diagnostics prove only finite algebra, typing, and loss arithmetic.

## 10. Canonical status registry

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

The maximum claim is the exact crosswalk and paid scalar splice. Arithmetic
advance remains `NO`, fixed-atom credit remains zero, strict \(1/400\) remains
`UNPAID`, global \(L^2\) remains `NONE`, and `TPC_207_TRIGGER=false`.
