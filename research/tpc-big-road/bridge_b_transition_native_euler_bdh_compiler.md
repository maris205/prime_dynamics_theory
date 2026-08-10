# Bridge A / Gates A--B V46: transition-native Euler carrier and the AP--BDH residual gate

Date: 2026-08-10

Status: unnumbered big-road research artifact. V45 paid the primitive
high-conductor part of the short transition spectrum but left the principal
character and the induced low-conductor tower as one structured major. This
note changes coordinates before trying to estimate that tower character by
character. At the original proper-factor modulus, the physical coefficient
splits exactly into its local shifted-prime/hybrid Euler profile and one
all-residue arithmetic-progression residual. The transition-native Euler
carrier is paid by the already source-backed reduced-radical
Bettin--Chandee compiler. Every principal, low-conductor and possible
exceptional mode is then contained in one explicit AP--BDH energy. A
natural-scale bound for that energy would close the complete transition
window with a large margin. No checked primary theorem proves it in the
modulus range \(x^{31/96}<d\le x^{133/400}<x^{1/2}\). Thus the route advances,
but arithmetic credit, the strict endpoint and the long-Mobius windows remain
open.

## 1. Frozen proper-factor transition scalar

Keep

\[
 H=x^{21/32},\qquad Q=x^{1/3},\qquad
 U=x^{133/400},\qquad Y_0=\frac{H}{4Q}=x^{31/96+o(1)},
 \tag{1.1}
\]

\[
 P=\frac{Q^2}{H}=x^{1/96},\qquad
 L_{\rm pr}=\sum_{q\in\mathcal Q}(q-1)=x^{2/3+o(1)},
 \tag{1.2}
\]

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad
 \mathcal Q=\{q\ {\rm prime}:Q<q\le2Q\},
 \tag{1.3}
\]

\[
 w(u)=\Lambda(u+2)-b_x^{(z)}(u),\qquad
 b(u)=\mathbf1_{I_x}(u)\frac{w(u)}{\log u}.
 \tag{1.4}
\]

After the V43 product freeze and complete centered Poisson transform, the
common spike in the transition window is

\[
 \begin{aligned}
 \mathfrak T_x^{\rm com}
 ={}&-H\sum_{q\in\mathcal Q}
 \sum_{Y_0<d\le U}\frac{\mu(d)\log d}{d}
 \sum_{\substack{m\ne0\\|m|\le dq/H}}
 \psi\!\left(\frac{Hm}{dq}\right)\\
 &\hspace{19mm}\times
 \sum_{u\in I_x}\frac{w(u)}{\log u}
 e_d(mu\overline q).
 \end{aligned}
 \tag{1.5}
\]

Here \(d<U<Q<q\), and \(|m|<q\), so every inverse in (1.5) is legal.
V44 paid the physical \(q\mid u\) correction and the centered background:

\[
 \boxed{
 \mathfrak A_x^{\rm tr}=\mathfrak T_x^{\rm com}
 +O\!\left(x^{319/192+o(1)}+x^{7171/4800+o(1)}\right).}
 \tag{1.6}
\]

V45 instead decomposed (1.5) by primitive conductor and paid the part
\(\operatorname{cond}(\chi)\ge P^{1/2}\). V46 retains that theorem as an
independent paid lane, but does not mix the conductor decomposition with the
new proper-factor decomposition term by term.

## 2. The proper-factor local profile and exact split

For each prime \(p\), define

\[
 F_p(a)=\frac p{p-1}\mathbf1_{a\not\equiv-2\pmod p},
 \tag{2.1}
\]

\[
 G_{p,z}(a)=
 \begin{cases}
 F_p(a),&p\le z,\\[1mm]
 p/(p-1),&p>z,\ a\equiv0\pmod p,\\[1mm]
 p(p-2)/(p-1)^2,&p>z,\ a\not\equiv0\pmod p.
 \end{cases}
 \tag{2.2}
\]

Because \(\mu(d)\ne0\) in (1.5), \(d\) is square-free. Put

\[
 P_d(a)=\prod_{p\mid d}F_p(a),\qquad
 B_{d,z}(a)=\prod_{p\mid d}G_{p,z}(a),\qquad
 \Delta_{d,z}(a)=P_d(a)-B_{d,z}(a).
 \tag{2.3}
\]

The V28 finite Euler identities give

\[
 \Delta_{d,z}(0)=0,\qquad
 \sum_{a\bmod d}\Delta_{d,z}(a)=0.
 \tag{2.4}
\]

If \(t=dk\) and \(u=t+h\), then \(h\equiv u\pmod d\), and hence

\[
 \boxed{\Delta_{d,z}(h)=\Delta_{d,z}(u).}
 \tag{2.5}
\]

This congruence is the exact bridge between the occurrence-native local
profile and the proper-factor Poisson modulus. Define the common local and
residual scalars by replacing \(w(u)\) in (1.5), respectively, with
\(\Delta_{d,z}(u)\) and \(w(u)-\Delta_{d,z}(u)\):

\[
 \boxed{
 \mathfrak T_x^{\rm com}
 =\mathfrak L_x^{\rm pf}+\mathfrak R_x^{\rm AP}.}
 \tag{2.6}
\]

This is an identity before the first outer absolute value. It does not
delete the principal character, a low-conductor character, or an exceptional
real character. They are merely reorganized inside the residual term.

Equivalently, the transition-native shift carrier is

\[
 M_x^{\rm pf}(h)=
 -\sum_{\substack{t,t+h\in I_x}}
 \sum_{\substack{d\mid t\\Y_0<d\le U}}
 \mu(d)\frac{\log d}{\log(t+h)}\Delta_{d,z}(h).
 \tag{2.7}
\]

It satisfies

\[
 \boxed{M_x^{\rm pf}(0)=0.}
 \tag{2.8}
\]

The denominator \(\log(t+h)\) is the literal V43 product-frozen
coefficient. Replacing it by \(\log t\) is allowed only with V43's already
paid coefficient-freeze error; V46 never silently identifies the two.

## 3. The transition-native local carrier is paid

For a square-free proper factor \(D\) in the transition range, the total
absolute mass of its occurrences is

\[
 \sum_{\substack{t\in I_x\\D\mid t}}
 \left|\mu(D)\frac{\log D}{\log t}\right|
 \ll\frac{x^{1+o(1)}}D.
 \tag{3.1}
\]

Thus the radical collapse used in V29 is available with the actual proper
factor \(D=d\), without the selected-group relabelling that separated V29
from V43. After the full-lattice extension, write

\[
 g=(n,D),\qquad D=gR,\qquad n=\epsilon ga,
 \quad \epsilon\in\{\pm1\}.
 \tag{3.2}
\]

The active corridor is

\[
 (a,qR)=1,\qquad 0<a\le\frac{qR}{H},\qquad
 R\ge\frac Hq=x^{31/96+o(1)}.
 \tag{3.3}
\]

With normalized local Fourier transform, the two literal Euler branches are

\[
 \widehat P_D(n\overline q)
 =\frac{\mu(R)}{\varphi(R)}e_R(2\epsilon a\overline q),
 \tag{3.4}
\]

\[
 \widehat B_{D,z}(n\overline q)
 =\frac{\mu(R_0)}{\varphi(R_0)\varphi(R_1)^2}
 e_{R_0}(2\epsilon a\overline{qR_1}),
 \qquad R=R_0R_1,
 \tag{3.5}
\]

where \(p\mid R_0\) exactly when \(p\le z\). The \(R_1=1\) rows cancel
before absolute values. Coprimality Mobius inversion gives the same
Bettin--Chandee variables as V29:

\[
 (a_{\rm BC},m_{\rm BC},n_{\rm BC})=(b,q,r)
 \tag{3.6}
\]

in the \(P\)-branch and

\[
 (a_{\rm BC},m_{\rm BC},n_{\rm BC})=(b,q\ell,s)
 \tag{3.7}
\]

in the \(B\)-branch after fixing the exact rough cofactor \(\ell\). From
(3.1), the dyadic coefficient norms are

\[
 \|\beta_R\|_{2,R\asymp S}\ll x^{1+o(1)}S^{-3/2},
 \tag{3.8}
\]

\[
 \|\beta_{R_0}(\,\cdot\,;R_1)\|_{2,R_0\asymp S}
 \ll x^{1+o(1)}S^{-3/2}R_1^{-3}.
 \tag{3.9}
\]

All hard-shell endpoints, both Fourier signs, the \(q\mid D\) complete-unit
cancellation, smooth separation and the exact-\(\ell\) triangle are therefore
identical to the already audited V29 compiler. Bettin--Chandee Theorem 1
gives

\[
 \boxed{
 \frac{|\mathfrak L_x^{\rm pf}|}{L_{\rm pr}}
 \ll x^{1891/1920+o(1)}.}
 \tag{3.10}
\]

Equivalently, at numerator level,

\[
 \boxed{
 |\mathfrak L_x^{\rm pf}|
 \ll x^{1057/640+o(1)}.}
 \tag{3.11}
\]

The exact margin is

\[
 \boxed{
 \frac{1997}{1200}-\frac{1057}{640}
 =\frac{121}{9600}.}
 \tag{3.12}
\]

This is a source-backed payment for the local proper-factor component, not a
claim about the residual or the physical zero coordinate.

## 4. One all-residue AP residual

For every square-free \(d\) in \(Y_0<d\le U\) and \(a\pmod d\), define

\[
 \mathcal R_d(a)=
 \sum_{\substack{u\in I_x\\u\equiv a\pmod d}}
 \frac{w(u)-\Delta_{d,z}(a)}{\log u}.
 \tag{4.1}
\]

Its unnormalized additive transform is

\[
 \widehat{\mathcal R}_d(r)=
 \sum_{a\bmod d}\mathcal R_d(a)e_d(ra).
 \tag{4.2}
\]

Parseval is exact:

\[
 \boxed{
 \sum_{r\bmod d}|\widehat{\mathcal R}_d(r)|^2
 =d\sum_{a\bmod d}|\mathcal R_d(a)|^2.}
 \tag{4.3}
\]

Put

\[
 A_d(r)=\frac{\mu(d)\log d}{d}
 \sum_{q\in\mathcal Q}
 \sum_{\substack{m\ne0\\|m|\le dq/H}}
 \psi\!\left(\frac{Hm}{dq}\right)
 \mathbf1_{r\equiv m\overline q\pmod d}.
 \tag{4.4}
\]

Then the residual scalar is the exact one-outer-sum pairing

\[
 \boxed{
 \mathfrak R_x^{\rm AP}
 =-H\sum_{Y_0<d\le U}\sum_{r\bmod d}
 A_d(r)\widehat{\mathcal R}_d(r).}
 \tag{4.5}
\]

No character projection is discarded in (4.5). In particular, the
conductor-one row, every induced low-conductor row, and a possible exceptional
real row all remain inside the same physical residual.

## 5. Elementary reciprocal-occupancy energy

On a dyadic block \(d\asymp D\), put

\[
 M=\frac{DQ}{H}=\frac{DP}{Q}.
 \tag{5.1}
\]

Two occupancies in (4.4) collide exactly when

\[
 m_1q_2-m_2q_1=\ell d,
 \qquad |\ell|\ll\frac{Q^2}{H}=P.
 \tag{5.2}
\]

The \(q_1=q_2\) contribution is diagonal because \(2M<d\). For
\(q_1\ne q_2\), fix \(m_1,m_2,\ell\). Integrality of

\[
 q_2=\frac{m_2q_1+\ell d}{m_1}
 \tag{5.3}
\]

restricts \(q_1\) to a residue class modulo
\(|m_1|/(|m_1|,|m_2|)\). Summing the elementary bound

\[
 O\!\left(\frac{Q(|m_1|,|m_2|)}{|m_1|}+1\right)
 \tag{5.4}
\]

over \(m_1,m_2,\ell\), for each fixed \(d\asymp D\), and using

\[
 \sum_{1\le |m_2|\le M}(|m_1|,|m_2|)
 \ll M\tau(|m_1|),
 \tag{5.5}
\]

gives \(O(DP^2x^{o(1)})\) collisions for that \(d\). The factor
\((\log d/d)^2\) in (4.4), followed by the sum over \(d\asymp D\), therefore
gives

\[
 \boxed{
 \sum_{Y_0<d\le U}\sum_{r\bmod d}|A_d(r)|^2
 \ll P^2x^{o(1)}=x^{1/48+o(1)}.}
 \tag{5.6}
\]

This coefficient estimate is elementary and unconditional. The missing
arithmetic theorem is entirely on the physical AP side of (4.5).

## 6. The natural AP--BDH gate and its payoff

Define the literal transition variance

\[
 \mathcal E_{\rm AP}^{\rm tr}
 =\sum_{\substack{Y_0<d\le U\\\mu^2(d)=1}}
 d\sum_{a\bmod d}|\mathcal R_d(a)|^2.
 \tag{6.1}
\]

The natural BDH scale is

\[
 \boxed{
 \mathsf H_{\rm AP}(\rho):\quad
 \mathcal E_{\rm AP}^{\rm tr}
 \ll xU^2x^{\rho+o(1)},
 \qquad 0\le\rho<\frac{33}{100}.}
 \tag{6.2}
\]

The benchmark case is \(\rho=0\). It is a conjectural theorem gate, not a
consequence of the definition of \(\mathcal R_d\). Cauchy in (4.5), (4.3),
and (5.6) give

\[
 |\mathfrak R_x^{\rm AP}|
 \ll HP\,(xU^2x^\rho)^{1/2}x^{o(1)}
 =x^{1799/1200+\rho/2+o(1)}.
 \tag{6.3}
\]

Since \(HP=L_{\rm pr}x^{o(1)}=x^{2/3+o(1)}\), the normalized form is

\[
 \boxed{
 \frac{|\mathfrak R_x^{\rm AP}|}{L_{\rm pr}}
 \ll x^{333/400+\rho/2+o(1)}.}
 \tag{6.4}
\]

At numerator level the exact residual margin is

\[
 \boxed{
 \frac{1997}{1200}
 -\left(\frac{1799}{1200}+\frac\rho2\right)
 =\frac{33}{200}-\frac\rho2.}
 \tag{6.5}
\]

Combining (1.6), (2.6), (3.11), and (6.3), hypothesis (6.2) gives

\[
 \boxed{
 |\mathfrak A_x^{\rm tr}|
 \ll x^{1997/1200-\eta_{\rm tr}+o(1)}}
 \tag{6.6}
\]

for every

\[
 0<\eta_{\rm tr}<
 \min\left\{
 \frac{121}{9600},\frac{33}{200}-\frac\rho2,
 \frac{13}{4800},\frac{817}{4800}
 \right\}.
 \tag{6.7}
\]

Thus one all-residue AP theorem replaces the entire V45 principal plus
low-conductor structured gate. It does not pay the balanced window
\(d>U,k>U\), the reverse-Type-I window \(d>U,k\le U\), or V42's independent
positive-Gram Gate B.

## 7. Relation to the V45 conductor atlas

The two decompositions have different jobs.

1. V45's conductor split is unconditional and already proves
   \[
   |\mathfrak V_{\ge P^{1/2}}^{\rm tr}|
   \ll x^{213/128+o(1)}.
   \tag{7.1}
   \]
2. V46's proper-factor split is exact at the physical local-profile
   interface. It pays the local Euler component and packages all remaining
   character modes into (6.1).
3. The AP gate is stronger than merely bounding V45's low-conductor tower,
   because it controls the full proper-factor residual. That strength buys a
   clean theorem statement and the large margin (6.5). V46 does not call it
   an equivalent or weakest reformulation.
4. Landau--Page isolation may show that at most one exceptional primitive
   character is relevant in a conductor range. It does not remove that row
   from (6.1) and supplies no fixed-power estimate for it.

Hence the selected route is now

~~~text
transition-native proper-factor Euler carrier              PAID
  -> one all-residue local-profile AP--BDH energy           OPEN
  -> balanced and reverse-Type-I long-Mobius windows        OPEN
  -> V42 positive-Gram Gate B in parallel                   OPEN
  -> V43 exact A+B zero-axis reassembly
  -> distinguished-seed dynamics reserve.
~~~

## 8. Primary-source boundary

The screen is primary-source-only and fail-closed as of 2026-08-10.

1. Bettin--Chandee,
   [*Trilinear forms with Kloosterman fractions*, arXiv:1502.00769v1,
   Theorem 1](https://arxiv.org/abs/1502.00769), accepts the three arbitrary
   arrays in (3.6)--(3.9). Together with the already proved V29 shell and
   coprimality compiler, it proves (3.10). It does not estimate the AP
   residual (6.1).

2. Lewko--Lewko,
   [*A Variational Barban--Davenport--Halberstam Theorem*,
   arXiv:1111.6190v2, Theorem 1](https://arxiv.org/abs/1111.6190), records
   the classical natural-scale theorem for
   \(x(\log x)^{-A}\le Q\le x\). Our largest proper-factor modulus is
   \(U=x^{133/400}\), far below that lower endpoint. Its variational
   strengthening does not repair the range or the \(d\)-dependent hybrid
   profile.

3. Harper,
   [*Simple Barban--Davenport--Halberstam type asymptotics for general
   sequences*, arXiv:2412.19644v1, Theorems 1--2](https://arxiv.org/abs/2412.19644),
   assumes \(\sqrt{2x}<Q\le x\), plus progression/non-concentration and,
   in Theorem 2, integer-resemblance hypotheses. The inequality
   \(U<x^{1/2}\) is already fatal. The literal sequence also depends on its
   modulus through \(\Delta_{d,z}\).

4. Fiorilli,
   [*The distribution of the variance of primes in arithmetic
   progressions*, arXiv:1301.5663](https://arxiv.org/abs/1301.5663),
   explains that the expected variance \(V(x;q)\asymp x\log q\) below the
   square-root range is a Hooley-type conjectural regime; its GRH/LI random
   model is evidence, not a uniform theorem for (6.1). V46 uses the natural
   scale only as a declared hypothesis.

5. Klurman--Mangerel--Teravainen,
   [*Multiplicative functions in short arithmetic progressions*,
   arXiv:1909.12280](https://arxiv.org/abs/1909.12280), proves strong
   almost-all-modulus variance results for bounded multiplicative functions,
   with explicit exceptional-modulus qualifications. The physical
   \(\Lambda(\cdot+2)-b_x^{(z)}\) residual is neither a bounded multiplicative
   function nor a modulus-independent coefficient sequence, and (6.1)
   requires the whole square-free transition family.

No screened theorem proves (6.2), even with \(\rho=0\), for the literal
shifted-prime minus hybrid profile. The first fatal is therefore a precise
new AP second-moment theorem, not an unspecified low-character estimate.

## 9. Finite exact diagnostics

The checker freezes the following identities and loss ledger.

1. For \(p=5>z\), the local difference on residues \(0,1,2,3,4\) is
   \[
   \Delta_{5,z}=(0,5/16,5/16,-15/16,5/16).
   \tag{9.1}
   \]
   It has zero mean and zero value at the zero coordinate.
2. If \(d=5,t=35,h=2,u=37\), then \(d\mid t\) and
   \(\Delta_{5,z}(h)=\Delta_{5,z}(u)=5/16\).
3. For \(d=4\) and the AP residual vector \((2,-1,3,-4)\), the additive
   transforms are
   \[
   (0,-1+3i,10,-1-3i),
   \tag{9.2}
   \]
   so Parseval gives \(120=4(2^2+(-1)^2+3^2+(-4)^2)\).
4. For \(d=5\), \(q\in\{7,11\}\), and
   \(m\in\{\pm1,\pm2\}\), each unit residue has occupancy two. The
   occupancy energy and the number of ordered determinant collisions are
   both \(16\).
5. The rational ledger freezes the natural AP energy exponent \(333/200\),
   coefficient exponent \(1/48\), residual numerator \(1799/1200\),
   normalized residual \(333/400\), residual margin \(33/200\), local
   numerator \(1057/640\), and local margin \(121/9600\).
6. A constant-mode mutation is not allowed to delete the AP residual: the
   AP profile is fixed by (2.1)--(2.3), not chosen after observing \(w\).

These are exact finite algebra and typing tests. They are not evidence for
the asymptotic hypothesis (6.2).

## 10. Canonical status registry

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

The maximum claim is a source-backed payment for the transition-native local
component and an exact whole-object reduction of the remaining transition
problem. The AP--BDH estimate is a declared open theorem. Arithmetic advance
remains NO, fixed-atom credit remains zero, strict \(1/400\) remains UNPAID,
global \(L^2\) remains NONE, and \(TPC_207_TRIGGER=false\).
