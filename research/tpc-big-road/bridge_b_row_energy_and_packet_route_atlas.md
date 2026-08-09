# Bridge A / Gate B V40: constant-residue compression and the q-row energy route

Date: 2026-08-09

Status: unnumbered big-road research artifact; exact scalar compression,
diagonal payment, route comparison, and endpoint ledger proved; the literal
q-row covariance theorem remains open; no arithmetic trigger.

## 1. Scope and inherited packet scalar

Keep the V37--V39 parameters and physical data

\[
 H=x^{21/32},\qquad Q=x^{1/3},\qquad
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},
 \tag{1.1}
\]

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad
 \beta(t)=\beta_x^{\rm raw}(t),\qquad
 w(u)=\Lambda(u+2)-b_x^{(z)}(u),
 \tag{1.2}
\]

and

\[
 K_H(h)=\widehat\psi_+(h/H).
 \tag{1.3}
\]

For a prime \(q\in\mathcal Q\), a unit \(t\pmod q\), and

\[
 \mathcal B_{q,t}=\mathbb F_q\setminus\{-t\},
 \tag{1.4}
\]

V37 defined

\[
 F_{q,t}(b)=
 \sum_{\substack{u\in I_x\\u\ne t\\u-t\equiv b\ ({\rm mod}\ q)}}
 w(u)K_H(u-t),
 \tag{1.5}
\]

\[
 G_{q,t}=F_{q,t}(0)-\frac1{q-1}
 \sum_{b\in\mathcal B_{q,t}}F_{q,t}(b).
 \tag{1.6}
\]

V38 regrouped the same physical packet into

\[
 d_q(r)=
 \sum_{\substack{t\in I_x\\t\equiv r\ ({\rm mod}\ q)}}
 \beta(t)G_{q,t},\qquad r\in\mathbb F_q^\times,
 \tag{1.7}
\]

and proved the exact scalar identity

\[
 \boxed{\mathfrak C_x=
 \sum_{q\in\mathcal Q}q\sum_{r\in\mathbb F_q^\times}d_q(r).}
 \tag{1.8}
\]

The strict numerator target remains

\[
 |\mathfrak C_x|\ll x^{1997/1200-\varepsilon+o(1)}
 \tag{1.9}
\]

for some fixed \(\varepsilon>0\).  V39 selected the full packet energy
\(\sum_{q,r}|d_q(r)|^2\) as the best generic Schatten lane.  V40 asks a
more basic question: which part of \(d_q\) is actually read by (1.8)?

## 2. Exact constant-residue compression

Define the one-dimensional row scalar and its shell energy by

\[
 s_q=\sum_{r\in\mathbb F_q^\times}d_q(r)
 =\sum_{\substack{t\in I_x\\q\nmid t}}\beta(t)G_{q,t},
 \tag{2.1}
\]

\[
 \boxed{\mathcal E_{\rm row}=\sum_{q\in\mathcal Q}|s_q|^2.}
 \tag{2.2}
\]

Then (1.8) reads simply

\[
 \mathfrak C_x=\sum_{q\in\mathcal Q}q s_q.
 \tag{2.3}
\]

Cauchy only over the prime shell gives

\[
 \boxed{
 |\mathfrak C_x|^2
 \leq\left(\sum_{q\in\mathcal Q}q^2\right)\mathcal E_{\rm row},
 \qquad
 |\mathfrak C_x|\ll Q^{3/2+o(1)}\mathcal E_{\rm row}^{1/2}.}
 \tag{2.4}
\]

For \(\kappa>0\), declare the literal row-energy hypothesis

\[
 \boxed{
 \mathsf H_{R2}(\kappa):\qquad
 \mathcal E_{\rm row}\ll x^{7/3-\kappa+o(1)}.}
 \tag{2.5}
\]

Equations (2.4)--(2.5) imply

\[
 |\mathfrak C_x|ll x^{5/3-\kappa/2+o(1)}.
 \tag{2.6}
\]

Thus the exact threshold and margin are

\[
 \boxed{
 \kappa>\frac1{200},\qquad
 \text{margin}=\frac\kappa2-\frac1{400}.}
 \tag{2.7}
\]

This is the same endpoint clock as V39, but on a strictly smaller norm.
Indeed,

\[
 |s_q|^2\leq(q-1)\sum_{r\in\mathbb F_q^\times}|d_q(r)|^2,
 \tag{2.8}
\]

so V39's packet hypothesis implies (2.5), up to the expected factor
\(Q=x^{1/3}\).  The converse is false on the ambient packet space.  For
\(q=5\) and

\[
 d=(1,-1,1,-1),
 \tag{2.9}
\]

one has \(s_5=0\) but \(\sum_r|d(r)|^2=4\).  Transverse residue modes can
therefore carry energy while being exactly invisible to the physical scalar.
The V39 packet-energy and Schatten lanes remain valid stronger reserves; they
are no longer the primary norm.

## 3. Collision expansion and the paid diagonal

Put

\[
 a_q(t)=\mathbf1_{q\nmid t}\,\beta(t)G_{q,t}.
 \tag{3.1}
\]

Then \(s_q=\sum_ta_q(t)\), and hence

\[
 \mathcal E_{\rm row}=\mathcal D_{\rm row}+\mathcal O_{\rm row},
 \tag{3.2}
\]

where

\[
 \mathcal D_{\rm row}=\sum_q\sum_t|a_q(t)|^2,
 \qquad
 \mathcal O_{\rm row}=
 \sum_q\sum_{t_1\ne t_2}a_q(t_1)\overline{a_q(t_2)}.
 \tag{3.3}
\]

The ordered off-diagonal sum in (3.3) is real, but it is not nonnegative.
For \(a=(1,-2,4,-1)\), the diagonal is \(22\), the row energy is \(4\),
and the off-diagonal is \(-18\).  It must not be renamed as a positive
energy.

The inherited divisor envelopes give \(|\beta(t)|+|w(t)|\ll x^{o(1)}\).
Schwartz decay and \(H/Q=x^{31/96}\to\infty\) give uniformly in admissible
\(q,t,b\)

\[
 \sum_{\substack{h\ne0\\h\equiv b\ ({\rm mod}\ q)}}|K_H(h)|
 \ll_{\psi}\frac Hq+1\ll\frac Hq,
 \qquad
 |G_{q,t}|\ll x^{o(1)}\frac Hq.
 \tag{3.4}
\]

Consequently the literal diagonal is already paid:

\[
 \boxed{
 \mathcal D_{\rm row}
 \ll x^{1+o(1)}\sum_{q\in\mathcal Q}\left(\frac Hq\right)^2
 \ll x^{95/48+o(1)}.}
 \tag{3.5}
\]

This exposes the next non-micro theorem.  For \(\tau\geq0\), define the
restricted row-Bessel hypothesis

\[
 \boxed{
 \mathsf H_{RB}(\tau):\qquad
 \mathcal E_{\rm row}\ll x^{\tau+o(1)}\mathcal D_{\rm row}.}
 \tag{3.6}
\]

Using (3.5), it reaches the strict endpoint precisely in the range

\[
 \boxed{
 \tau<\frac73-\frac1{200}-\frac{95}{48}
 =\frac{419}{1200}.}
 \tag{3.7}
\]

The natural benchmark \(\tau=1/3\), corresponding to at most one full
\(Q\)-loss beyond the paid diagonal, gives

\[
 \mathcal E_{\rm row}\ll x^{37/16+o(1)},\qquad
 \kappa=\frac1{48},
 \tag{3.8}
\]

\[
 |\mathfrak C_x|\ll x^{53/32+o(1)},\qquad
 \text{margin}=\frac{19}{2400}.
 \tag{3.9}
\]

By comparison, the V39 full-packet Bessel benchmark allowed relative loss
only \(<19/1200\).  The new row gate allows \(<419/1200\).  This is the
quantitative reason for the V40 reroute.

## 4. Exact shift-dispersion normal form

Opening (1.5)--(1.6) in (2.1) gives the exact physical row

\[
 \boxed{
 s_q=\sum_{\substack{t,u\in I_x\\t\ne u\\q\nmid tu}}
 \beta(t)w(u)K_H(u-t)
 \left(\mathbf1_{q\mid u-t}-\frac1{q-1}\right).}
 \tag{4.1}
\]

Let

\[
 r_x(h)=\sum_{\substack{t,t+h\in I_x}}\beta(t)w(t+h),
 \tag{4.2}
\]

and first omit only the two unit masks:

\[
 \widetilde s_q=
 \sum_{h\ne0}K_H(h)r_x(h)
 \left(\mathbf1_{q\mid h}-\frac1{q-1}\right).
 \tag{4.3}
\]

The omitted rows are elementary.  If \(q\mid h\), both endpoints are
nonunits together and there are \(O(x/q)\) such \(t\)'s for each of the
\(O(H/q)\) effective shifts.  If \(q\nmid h\), either endpoint can be a
nonunit, and the background coefficient contributes another factor
\(1/q\).  Thus

\[
 \boxed{
 \Delta_q:=s_q-\widetilde s_q
 \ll x^{1+o(1)}\frac H{q^2},
 \qquad
 \sum_{q\in\mathcal Q}|\Delta_q|^2
 \ll x^{37/16+o(1)}.}
 \tag{4.4}
\]

This is already at the benchmark exponent (3.8); it is not part of the open
row covariance.

Now put \(f(h)=K_H(h)r_x(h)\) and \(T=\sum_{h\ne0}f(h)\).  Then

\[
 \widetilde s_q=\sum_{\substack{h\ne0\\q\mid h}}f(h)-\frac{T}{q-1}.
 \tag{4.5}
\]

For every fixed \(0<\varepsilon<1/96\), Schwartz decay makes
\(|h|\geq Q^2\) negligible to any prescribed power, while

\[
 Hx^\varepsilon<Q^2.
 \tag{4.6}
\]

Two distinct primes in \((Q,2Q]\) cannot both divide a nonzero
\(|h|<Q^2\).  Weighted Cauchy therefore gives

\[
 \sum_{q\in\mathcal Q}
 \left|\sum_{\substack{h\ne0\\q\mid h}}f(h)\right|^2
 \ll\frac HQ
 \sum_{h\ne0}|K_H(h)|\,|r_x(h)|^2+O_B(x^{-B}).
 \tag{4.7}
\]

Also

\[
 \sum_q\frac1{(q-1)^2}\ll\frac1Q,
 \qquad
 |T|^2\ll H\sum_{h\ne0}|K_H(h)|\,|r_x(h)|^2.
 \tag{4.8}
\]

Combining (4.4)--(4.8), one obtains the exact conditional compiler

\[
 \boxed{
 \mathcal E_{\rm row}
 \ll\frac HQ
 \sum_{h\ne0}|K_H(h)|\,|r_x(h)|^2
 +x^{37/16+o(1)}.}
 \tag{4.9}
\]

Hence the stronger full-shift hypothesis

\[
 \sum_{h\ne0}|K_H(h)|\,|r_x(h)|^2
 \ll x^{2+2\sigma+o(1)}
 \tag{4.10}
\]

would give

\[
 \mathcal E_{\rm row}\ll x^{223/96+2\sigma+o(1)},
 \qquad
 |\mathfrak C_x|\ll x^{319/192+\sigma+o(1)}.
 \tag{4.11}
\]

The endpoint condition is exactly

\[
 \sigma<\frac{13}{4800}.
 \tag{4.12}
\]

This recovers the V36 Route-E clock but not its theorem interface.  V36's
open energy is for the tagged residual \(e_x=r_x-M_x^{\rm loc}\), after a
separate local-carrier payment.  Equation (4.10) is for the full physical
\(r_x\).  A successful transfer must decompose the row scalar and pay the
same local carrier rowwise; replacing \(r_x\) by \(e_x\) without that
identity is a scoped type error.

## 5. Exact joint-character row form

Use the V36 definitions

\[
 B_{q,\chi}(v)=
 \sum_{\substack{t\in I_x\\q\nmid t}}
 \beta(t)\overline{\chi(t)}e(vt/H),
 \tag{5.1}
\]

\[
 W_{q,\chi}(v)=
 \sum_{\substack{u\in I_x\\q\nmid u}}
 w(u)\chi(u)e(-vu/H),
 \qquad
 Z_q=\sum_{\substack{t\in I_x\\q\nmid t}}\beta(t)w(t).
 \tag{5.2}
\]

Character orthogonality gives, modulus by modulus,

\[
 \boxed{
 s_q=\frac1{q-1}\int_{\mathbb R}\psi_+(v)
 \sum_{\substack{\chi\ ({\rm mod}\ q)\\\chi\ne\chi_0}}
 \bigl(B_{q,\chi}(v)W_{q,\chi}(v)-Z_q\bigr)\,dv.}
 \tag{5.3}
\]

Jensen in \(v\), followed by Cauchy in \(\chi\), yields the stronger
sufficient interface

\[
 \mathcal E_{\rm row}
 \ll_{\psi}
 \int_{\mathbb R}|\psi_+(v)|
 \sum_{q\in\mathcal Q}\frac1{q-1}
 \sum_{\chi\ne\chi_0}
 |B_{q,\chi}(v)W_{q,\chi}(v)-Z_q|^2\,dv.
 \tag{5.4}
\]

Thus a joint centered character fourth-moment theorem at exponent
\(7/3-\kappa\), \(\kappa>1/200\), would prove the row gate.  Separate
marginal second-moment large-sieve estimates for \(B\) and \(W\) do not
bound (5.4): the same \((q,\chi,v)\) covariance and the subtraction \(Z_q\)
must remain inside the norm.

## 6. What the route comparison proves

The exact implications are

```text
V39 full packet energy H_P2(kappa)
  -> V40 row energy H_R2(kappa)
  -> strict scalar bound when kappa>1/200.

V40 restricted row-Bessel H_RB(tau)
  + paid diagonal x^(95/48)
  -> H_R2 with strict endpoint for tau<419/1200.

full physical shift energy (stronger)
  + exact unit-deletion payment
  -> H_R2 for sigma<13/4800.

joint centered character fourth moment (stronger)
  -> H_R2.
```

None of the arrows proves its open analytic premise.  The route-selection
advance is that the physical scalar reads only the constant residue direction,
and that the paid diagonal leaves a generous \(Q^{419/400-o(1)}\)-scale
relative Bessel budget.  Full packet energy, canonical block Schatten,
whole-residual energy, and character decoupling remain independent stronger
or implementation lanes.  After any Gate-B lane closes, terminal q-local
signed covariance A remains a separate theorem.  Distinguished-seed dynamics
C stays reserve.

## 7. Primary-source boundary

The screen below uses primary theorem texts current on 2026-08-09.

1. [Harper, arXiv:2412.19644v1, Theorems 1--2](https://arxiv.org/html/2412.19644)
   studies the progression variance of one fixed sequence, with additional
   sparsity/divisibility hypotheses and \(Q>\sqrt{2x}\).  Here the coefficient
   row depends on \(q\), contains the centered \(\beta\times w\) packet, and
   uses \(q=x^{1/3}\).  There is no literal attachment.

2. [Zheng, arXiv:2512.22798v1, Theorems 1.1--1.2](https://arxiv.org/html/2512.22798)
   proves mean values for primes in simultaneous arithmetic progressions with
   source-specific divisor-bounded or well-factorable arrays and smaller
   modulus exponents.  It is an architecture analogue, not a theorem for
   (2.2) or (4.1).

3. [Pascadi, arXiv:2304.11696v3](https://arxiv.org/abs/2304.11696)
   proves distribution of smooth numbers to large moduli by dispersion and
   Deshouillers--Iwaniec type Kloosterman estimates.  The smooth-number triple
   convolution is not the literal ordered MASTER/hybrid \(\beta\times w\)
   row covariance.

4. [Blomer--Fouvry--Kowalski--Michel--Milićević,
   arXiv:1411.4467v3](https://arxiv.org/abs/1411.4467) develops shifted
   convolution and bilinear Kloosterman tools for twisted automorphic
   \(L\)-function moments.  Its automorphic coefficient families and
   source-specific shifted sums do not equal (4.1).

5. [Blomer--Pascadi, arXiv:2607.24311v1, Theorem 1.1](https://arxiv.org/html/2607.24311v1)
   gives a powerful fixed-modulus separable bilinear Kloosterman engine.  It
   acts after an admissible emitter and does not prove the prime-shell row
   energy (2.2).

No screened source proves \(\mathsf H_{R2}\), \(\mathsf H_{RB}\), the full
shift input (4.10), or the joint character moment (5.4) for the literal
physical coefficients.  These are theorem-design targets, not attributed
consequences.

## 8. Finite falsifiers and endpoint fixtures

### 8.1 Constant direction versus transverse packet energy

At \(q=5\), the packet \(d=(3,-2,5,1)\) has

\[
 s=7,\qquad |s|^2=49,
 \qquad \sum_r|d(r)|^2=39,
 \tag{8.1}
\]

and \(49\leq4\cdot39\), as required by (2.8).  The alternating packet
(2.9) has row energy zero and packet energy four, disproving the converse.

### 8.2 Signed collision is not a positive energy

For \(a=(2,-1,3)\),

\[
 |\textstyle\sum a|^2=16,qquad
 \sum|a|^2=14,qquad
 \sum_{i\ne j}a_i\overline{a_j}=2.
 \tag{8.2}
\]

For \(a=(1,-2,4,-1)\), the corresponding triple is \((4,22,-18)\).
Both signs occur.

### 8.3 The strict exponent ledger

The checker recomputes exactly

\[
 \frac73-\frac1{200}-\frac{95}{48}=\frac{419}{1200},
 \qquad
 \frac{95}{48}+\frac13=\frac{37}{16},
 \tag{8.3}
\]

\[
 \frac73-\frac{37}{16}=\frac1{48},
 \qquad
 \frac12+\frac12\frac{37}{16}=\frac{53}{32},
 \qquad
 \frac{1997}{1200}-\frac{53}{32}=\frac{19}{2400}.
 \tag{8.4}
\]

Equality at \(419/1200\) or at \(1/200\) cannot absorb \(x^{o(1)}\).

### 8.4 The unique-divisor firewall

For primes \(5,7\), every nonzero \(|h|<35\) is divisible by at most one
of them; \(h=35\) is the first collision.  This freezes the strict
\(|h|<Q^2\) condition in (4.6)--(4.7).  It is a finite type check, not an
asymptotic estimate.

## 9. Route map after V40

```text
V38 canonical residue/Kloosterman emitter
  -> V39 exposes the nuclear toll and selects generic p=2 packet energy
  -> V40 observes that C_x reads only s_q=sum_r d_q(r)
  -> primary Gate-B theorem: row energy H_R2(kappa), kappa>1/200
       preferred implementation: restricted row-Bessel tau<419/1200
       alternate implementations: full-shift or joint-character normal form
  -> stronger reserves: V39 packet P2, specialized Schatten K, residual E, X
  -> terminal q-local signed covariance A
  -> distinguished-seed dynamics C reserve.
```

The first fatal is now the absence of a literal theorem controlling
\(\sum_q|\sum_t\beta(t)G_{q,t}|^2\) at the row threshold, or proving the
restricted row-Bessel benchmark.  Transverse residue energy is no longer part
of the primary toll.

## 10. Canonical status registry

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
