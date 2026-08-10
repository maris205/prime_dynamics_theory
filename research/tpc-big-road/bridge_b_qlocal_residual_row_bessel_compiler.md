# Bridge A / Gate B V41: q-local model payment and the residual row-Bessel bridge

Date: 2026-08-10

Status: unnumbered big-road research artifact; the literal q-local row split,
the complete elementary model payment, the residual-row endpoint compiler,
and the zero-coordinate firewall are proved.  The residual row covariance
theorem remains open; there is no arithmetic trigger.

## 1. Scope and inherited scalar

Keep the V40 data

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

For \(q\in\mathcal Q\), put

\[
 c'_q(h)=\mathbf1_{q\mid h}-\frac1{q-1}.
 \tag{1.4}
\]

The exact V40 row and scalar are

\[
 s_q=\sum_{\substack{t,u\in I_x\\t\ne u\\q\nmid tu}}
 \beta(t)w(u)K_H(u-t)c'_q(u-t),
 \tag{1.5}
\]

\[
 \mathcal E_{\rm row}=\sum_{q\in\mathcal Q}|s_q|^2,
 \qquad
 \mathfrak C_x=\sum_{q\in\mathcal Q}q s_q.
 \tag{1.6}
\]

Thus

\[
 |\mathfrak C_x|\ll Q^{3/2+o(1)}\mathcal E_{\rm row}^{1/2}.
 \tag{1.7}
\]

The strict numerator target is

\[
 |\mathfrak C_x|\ll x^{1997/1200-\varepsilon+o(1)}
 \tag{1.8}
\]

for some fixed \(\varepsilon>0\).  The historical V40 display (2.6) has a
missing TeX backslash before `ll`; throughout the current artifact its intended
and mathematically forced relation is the `\(\ll\)` relation (1.7).  The sealed
V40 bytes are not rewritten.

## 2. The exact q-local row split

For sufficiently large \(x\), every \(q\in\mathcal Q\) is larger than the
hybrid cutoff \(z\).  Reuse the V30 formal local-density profile

\[
 \Gamma_q(u)=
 \begin{cases}
 -q(q-2)/(q-1)^2,&u\equiv-2\pmod q,\\
 0,&u\equiv0\pmod q,\\
 q/(q-1)^2,&u\not\equiv0,-2\pmod q.
 \end{cases}
 \tag{2.1}
\]

It satisfies

\[
 \frac1q\sum_{u\bmod q}\Gamma_q(u)=0.
 \tag{2.2}
\]

Define the model row and q-local residual row by

\[
 m_q=\sum_{\substack{t,u\in I_x\\t\ne u\\q\nmid tu}}
 \beta(t)\Gamma_q(u)K_H(u-t)c'_q(u-t),
 \tag{2.3}
\]

\[
 \rho_q=\sum_{\substack{t,u\in I_x\\t\ne u\\q\nmid tu}}
 \beta(t)\bigl(w(u)-\Gamma_q(u)\bigr)
 K_H(u-t)c'_q(u-t).
 \tag{2.4}
\]

No approximation has occurred:

\[
 \boxed{s_q=m_q+\rho_q.}
 \tag{2.5}
\]

The V19 occurrence weights may be collapsed to the literal
\(\beta_x^{\rm raw}(t)\) before (2.3), because \(\Gamma_q\) depends only on the
physical endpoint \(u\).  Every ordered \(+2,-1\), Möbius/log, MASTER/H2,
unit, hard-shell, and hybrid contribution is still present exactly once.
There is no atom-dependent prime ensemble.

## 3. Elementary payment of the complete model row

For \(q\geq5\), the three values in (2.1) give

\[
 |\Gamma_q(u)|\leq
 \mathbf1_{u\equiv-2\ (q)}+\frac2q
 \mathbf1_{u\not\equiv0,-2\ (q)},
 \tag{3.1}
\]

while

\[
 |c'_q(h)|\leq
 \mathbf1_{q\mid h}+\frac2q\mathbf1_{q\nmid h}.
 \tag{3.2}
\]

Schwartz decay and \(H/q\to\infty\) imply, uniformly in residue classes,

\[
 \sum_{h\equiv a\ (q)}|K_H(h)|\ll_\psi\frac Hq,
 \qquad
 \sum_h|K_H(h)|\ll_\psi H.
 \tag{3.3}
\]

Fix a unit \(t\pmod q\).  There are three disjoint contributions.

1. If \(q\mid u-t\), then \(u\equiv t\pmod q\).  This costs
   \(H/q\) only for the exceptional row \(t\equiv-2\pmod q\), and
   \(H/q^2\) otherwise.
2. If \(q\nmid u-t\) and \(u\equiv-2\pmod q\), the factor
   \(1/(q-1)\) in \(c'_q\) gives \(H/q^2\).
3. For the remaining \(u\), both \(\Gamma_q(u)\) and the noncongruent
   multiplier cost \(1/q\), giving \(H/q^2\) after summing all shifts.

Therefore

\[
 \sum_{\substack{u\in I_x\\u\ne t\\q\nmid u}}
 |\Gamma_q(u)K_H(u-t)c'_q(u-t)|
 \ll_\psi \frac H{q^2}
 +\mathbf1_{t\equiv-2\ (q)}\frac Hq.
 \tag{3.4}
\]

The inherited pointwise divisor envelope is
\(|\beta(t)|\ll x^{o(1)}\), and there are \(O(x/q+1)\) integers
\(t\in I_x\) in the exceptional residue.  Hence

\[
 \boxed{|m_q|\ll x^{1+o(1)}\frac H{q^2}.}
 \tag{3.5}
\]

This estimate retains the hard endpoints and off-diagonal deletion; extending
either sum would only enlarge the absolute majorant.  Summing over the prime
shell gives the complete model energy

\[
 \boxed{
 \mathcal E_{\rm model}:=\sum_{q\in\mathcal Q}|m_q|^2
 \ll x^{2+o(1)}H^2\sum_{q\in\mathcal Q}q^{-4}
 \ll \frac{x^{2+o(1)}H^2}{Q^3}
 =x^{37/16+o(1)}.}
 \tag{3.6}
\]

Consequently

\[
 \left|\sum_{q\in\mathcal Q}q m_q\right|
 \ll Q^{3/2+o(1)}\mathcal E_{\rm model}^{1/2}
 \ll x^{53/32+o(1)}.
 \tag{3.7}
\]

The model alone has strict endpoint margin

\[
 \frac{1997}{1200}-\frac{53}{32}=\frac{19}{2400}.
 \tag{3.8}
\]

Thus V40's scoped `rowwise local carrier unpaid` obstruction is removed at
exactly the preferred \(\tau=1/3\) benchmark.  This is an elementary
whole-shell payment, not a source theorem and not an estimate for the residual.

## 4. The residual row theorem is the unique Gate-B target

Set

\[
 \mathcal E_{\rm res}=\sum_{q\in\mathcal Q}|\rho_q|^2.
 \tag{4.1}
\]

By (2.5),

\[
 \mathcal E_{\rm row}\leq
 2\mathcal E_{\rm model}+2\mathcal E_{\rm res}.
 \tag{4.2}
\]

For \(\kappa>0\), declare the literal residual-row hypothesis

\[
 \boxed{
 \mathsf H_{QR2}(\kappa):\qquad
 \mathcal E_{\rm res}\ll x^{7/3-\kappa+o(1)}.}
 \tag{4.3}
\]

Since \(37/16=7/3-1/48\), equations (1.7), (3.6), and (4.2)
show that (4.3) reaches the endpoint exactly when

\[
 \boxed{\kappa>\frac1{200}.}
 \tag{4.4}
\]

More precisely,

\[
 |\mathfrak C_x|\ll
 x^{\max\{53/32,\,5/3-\kappa/2\}+o(1)},
 \tag{4.5}
\]

with strict margin

\[
 \boxed{
 \min\left\{\frac{19}{2400},
 \frac\kappa2-\frac1{400}\right\}.}
 \tag{4.6}
\]

The benchmark \(\kappa=1/48\) gives

\[
 \mathcal E_{\rm res}\ll x^{37/16+o(1)},\qquad
 |\mathfrak C_x|\ll x^{53/32+o(1)}.
 \tag{4.7}
\]

This is a genuine narrowing of V40: the open theorem no longer has to discover
or reproduce the \(q\)-local Euler row.  It must control only the same literal
\(\beta\times(w-\Gamma_q)\) residual across the whole prime shell.

## 5. Restricted residual row-Bessel and exact dual forms

Define

\[
 G^{\rm res}_{q,t}=
 \sum_{\substack{u\in I_x\\u\ne t\\q\nmid u}}
 \bigl(w(u)-\Gamma_q(u)\bigr)K_H(u-t)c'_q(u-t),
 \tag{5.1}
\]

so that

\[
 \rho_q=\sum_{\substack{t\in I_x\\q\nmid t}}
 \beta(t)G^{\rm res}_{q,t}.
 \tag{5.2}
\]

Because \(|w(u)-\Gamma_q(u)|\ll x^{o(1)}\), the V40 diagonal
payment survives unchanged:

\[
 \boxed{
 \mathcal D_{\rm res}:=
 \sum_{q\in\mathcal Q}\sum_{\substack{t\in I_x\\q\nmid t}}
 |\beta(t)G^{\rm res}_{q,t}|^2
 \ll x^{95/48+o(1)}.}
 \tag{5.3}
\]

The preferred implementation theorem is therefore

\[
 \boxed{
 \mathsf H_{QRB}(\tau):\qquad
 \mathcal E_{\rm res}\ll x^{\tau+o(1)}\mathcal D_{\rm res},
 \qquad \tau<\frac{419}{1200}.}
 \tag{5.4}
\]

The sample \(\tau=1/3\) gives exactly (4.7).  Equivalently, Hilbert-space
duality gives the one-outer-absolute interface

\[
 \boxed{
 \mathcal E_{\rm res}^{1/2}=
 \sup_{\sum_q|\lambda_q|^2=1}
 \left|\sum_{q\in\mathcal Q}\lambda_q\rho_q\right|.}
 \tag{5.5}
\]

This makes the missing operation explicit: it is a collective modulus-family
theorem, not a collection of unrelated pointwise estimates.

There is also an exact same-index character form.  Put

\[
 W^{\rm res}_{q,\chi}(v)=
 \sum_{\substack{u\in I_x\\q\nmid u}}
 \bigl(w(u)-\Gamma_q(u)\bigr)\chi(u)e(-vu/H),
 \tag{5.6}
\]

\[
 Z_q^{\rm res}=\sum_{\substack{t\in I_x\\q\nmid t}}
 \beta(t)\bigl(w(t)-\Gamma_q(t)\bigr).
 \tag{5.7}
\]

With \(B_{q,\chi}\) as in V40, character orthogonality and the explicit
off-diagonal subtraction give

\[
 \boxed{
 \rho_q=\frac1{q-1}\int_{\mathbb R}\psi_+(v)
 \sum_{\substack{\chi\ ({\rm mod}\ q)\\\chi\ne\chi_0}}
 \bigl(B_{q,\chi}(v)W^{\rm res}_{q,\chi}(v)
       -Z_q^{\rm res}\bigr)\,dv.}
 \tag{5.8}
\]

Separate marginal large-sieve bounds still do not control the same
\((q,\chi,v)\) product covariance in (5.8).

## 6. The zero-coordinate firewall is unchanged

Every row in (1.5), (2.3), and (2.4) deletes \(u=t\), hence sees only
nonzero shifts \(h=u-t\).  Let an abstract tagged residual be

\[
 e(h)=T\mathbf1_{h=0}.
 \tag{6.1}
\]

Then every off-diagonal residual row \(\rho_q\) is zero, while the physical
zero-coordinate is \(e(0)=T\), which is arbitrary.  Therefore neither
(4.3), (5.4), nor (5.8) pays terminal Gate A.

This agrees with the exact V30 diagonal ledger.  The q-local residual
diagonal is

\[
 S_x^{\rm physical}+O(x^{2/3+o(1)}),
 \tag{6.2}
\]

not zero.  If one augments the row theorem by restoring \(h=0\), its energy
contains \(\#\mathcal Q\,|S_x^{\rm physical}+O(x^{2/3+o(1)})|^2\).
A strict augmented-row estimate is therefore already a terminal theorem in
disguise, not an easier preliminary bridge.  Gate A remains

\[
 |\mathfrak R_x^{q\mathrm{loc}}|
 \ll x^{399/400-\eta_R}
 \tag{6.3}
\]

for some fixed \(\eta_R>0\), independently of Gate B.

## 7. Primary-source WHY / HOW / WHAT boundary

The following screen uses primary theorem texts current on 2026-08-10.

### 7.1 WHY: shift averages do not give this sparse residual row

1. [Matomäki--Radziwiłł--Tao, arXiv:1707.01315v3, Theorem 1.3](https://arxiv.org/abs/1707.01315)
   proves almost-all-shift asymptotics with logarithmic saving for the
   source-native \(\Lambda\times\Lambda\), \(d_k\times d_\ell\), and
   \(\Lambda\times d_k\) families.  Its abstract minor-arc Proposition 3.1
   is a useful reduction, but no theorem identifies the literal
   \(\beta_x^{\rm raw}\times(w-\Gamma_q)\) row or supplies the required fixed
   power.

2. [Merikoski, arXiv:1605.04757v1, Main Theorem 1 and Corollary 1](https://arxiv.org/abs/1605.04757)
   gives the unweighted first average of \(\pi_{2k}(x)\) for
   \(2k\le x^\theta\), \(\theta>7/12\).  It is not a centered second moment,
   carries no \(q\)-dependent Euler subtraction, and does not estimate the
   modulus rows (2.4).

3. [Lichtman--Teräväinen, arXiv:2111.08912v3, Theorem 1.1](https://arxiv.org/abs/2111.08912)
   proves Hardy--Littlewood--Chowla correlations for all but \(o(H)\)
   shifts.  The active set \(h=qk\), \(q\sim Q\), has only
   \(H/\log Q=x^{21/32+o(1)}/\log x=o(H)\) elements, so a qualitative
   exceptional set may contain the entire row support.  Its fixed finite
   product coefficients also differ from the ordered MASTER/hybrid residual.

4. [Evans, arXiv:2102.12297v3, Theorems 1.1 and 1.4](https://arxiv.org/abs/2102.12297)
   obtains almost-all-shift asymptotics for restricted \(E_2\times E_2\)
   and prime--\(E_2\) correlations.  The bilinear \(E_2\) factor windows and
   qualitative/logarithmic exceptional-shift output are not (2.4).

### 7.2 HOW: marginal AP theorems do not control the joint row

5. [Koukoulopoulos, arXiv:1405.6592v2, Theorems 1.1--1.3](https://arxiv.org/abs/1405.6592)
   controls primes in short arithmetic progressions for most moduli and
   interval locations under source ranges including \(Q^2\le H/x^\alpha\)
   with \(\alpha>0\).  Here \(Q^2/H=x^{1/96}\), so even \(Q^2\le H\) fails;
   moreover the theorem is a one-sequence AP marginal, not a square of the
   joint rows.

6. [Harper, arXiv:2412.19644v1, Theorems 1--2](https://arxiv.org/abs/2412.19644)
   treats the progression variance of one fixed sequence under additional
   sparsity/divisibility hypotheses and a large-modulus regime.  The sequence
   in (2.4) changes with \(q\), and \(q=x^{1/3}\); the hypotheses do not attach.

### 7.3 WHAT: coefficient-native local engines remain one-sided

7. [Bazin, arXiv:2607.15137v1, Theorem 8](https://arxiv.org/abs/2607.15137)
   accepts the collapsed \(\beta\)-marginal through a Type-I/II interface,
   as recorded in V33.  It does not simultaneously accept
   \(w-\Gamma_q\) or prove the collective product row.  The V33
   \(H^{1/4}\) loss remains larger than the endpoint allowance.

No checked primary theorem controls

\[
 \sum_{q\in\mathcal Q}\left|
 \sum_{\substack{t,u\in I_x\\t\ne u\\q\nmid tu}}
 \beta(t)(w(u)-\Gamma_q(u))K_H(u-t)c'_q(u-t)
 \right|^2
 \tag{7.1}
\]

at exponent \(7/3-\kappa\) with \(\kappa>1/200\).

## 8. Route after V41

The macro route is now

```text
V38 canonical packet emitter
  -> V39 packet-energy pivot
  -> V40 constant residue row s_q
  -> V41 exact split s_q=m_q+rho_q
       m_q model energy x^(37/16) = PAID
       rho_q residual row energy = ACTIVE OPEN
          preferred implementation: residual row-Bessel tau<419/1200
          equivalent one-outer-absolute dual and same-index character forms
  -> terminal q-local signed covariance A = INDEPENDENT OPEN
  -> dynamics C = RESERVE.
```

The bridge has moved one pier forward: the local Euler row is on the paid
side.  The first fatal is now the whole prime-shell covariance of the literal
q-local residual, not the raw row and not a collection of marginal AP bounds.

## 9. Finite exact fixtures retained by the checker

For \(q=5\),

\[
 (\Gamma_5(0),\ldots,\Gamma_5(4))
 =(0,5/16,5/16,-15/16,5/16),
 \tag{9.1}
\]

whose sum is zero.  With the negative background \(c'_5\), full-period
convolution gives

\[
 \sum_{u\bmod5}\Gamma_5(u)c'_5(u-t)=\Gamma_5(t),
 \tag{9.2}
\]

while deleting the diagonal leaves \(\Gamma_5(t)/4\).  This catches the
off-diagonal/zero-axis distinction.

For the exact toy shell

\[
 I=(1,2,3,4,6,7,8,9),\quad
 \beta(t)=(t\bmod7)-3,
 \tag{9.3}
\]

\[
 w(u)=((2u+1)\bmod9)-4,\qquad K(h)=\frac1{1+|h|},
 \tag{9.4}
\]

direct rational summation gives

\[
 s_5=-\frac{11717}{5040},\qquad
 m_5=\frac{307}{1792},\qquad
 \rho_5=-\frac{201287}{80640},
 \tag{9.5}
\]

and \(s_5=m_5+\rho_5\).  The checker also freezes the exponent ledger and the
fixture (6.1), for which every off-zero row vanishes while the atom is \(T\).

## 10. Canonical status registry

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
