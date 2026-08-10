# Bridge A / Gates A--B V43: proper-factor Poisson transference and the long-Möbius frontier

Date: 2026-08-10

Status: unnumbered big-road research artifact.  The V35 proper-factor scalar
is transformed before any outer absolute value.  A complete centered Poisson
identity removes every nonzero alias with outer Möbius factor
\(d\leq H/(4Q)\), while the deleted physical diagonal returns exactly as the
zero-axis scalar.  Thus the small-factor lane is transferred from Gate B to
Gate A rather than falsely declared paid.  The remaining transition, Type-II,
and reverse-Type-I inverse-residue alias is explicit; no checked primary
source proves its whole-object bound.  There is no arithmetic trigger.

## 1. Frozen scalar and endpoint clock

Keep

\[
 H=x^{21/32},\qquad Q=x^{1/3},\qquad
 U=x^{133/400},
 \tag{1.1}
\]

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},
 \tag{1.2}
\]

\[
 \beta(t)=\beta_x^{\rm raw}(t),\qquad
 w(u)=\Lambda(u+2)-b_x^{(z)}(u),\qquad
 K_H(h)=\widehat\psi_+(h/H),
 \tag{1.3}
\]

where

\[
 \widehat\psi_+(\xi)=\int_{\mathbb R}\psi(v)e(+\xi v)\,dv,
 \qquad \operatorname{supp}\psi\subset[-1,1],
 \qquad \int\psi=1.
 \tag{1.4}
\]

For prime \(q\), put

\[
 c'_q(h)=\mathbf1_{q\mid h}-\frac1{q-1}.
 \tag{1.5}
\]

The V35/V40 centered core is

\[
 \boxed{
 \mathfrak C_x=\sum_{q\in\mathcal Q}q s_q,\qquad
 s_q=\sum_{\substack{t,u\in I_x\\t\ne u,\ q\nmid tu}}
 \beta(t)w(u)K_H(u-t)c'_q(u-t).}
 \tag{1.6}
\]

V35 proved the exact decomposition

\[
 \mathfrak D_x=\mathfrak C_x+\mathfrak P_x+\mathfrak N_x,
 \qquad
 |\mathfrak P_x|+|\mathfrak N_x|\ll x^{53/32+o(1)},
 \tag{1.7}
\]

and V34 proved

\[
 E(r_x)=-\frac{\mathfrak D_x}{L_{\rm pr}},\qquad
 L_{\rm pr}=\sum_{q\in\mathcal Q}(q-1)=x^{2/3+o(1)}.
 \tag{1.8}
\]

Write

\[
 S_x^{\rm physical}=r_x(0)=\sum_{u\in I_x}\beta(u)w(u).
 \tag{1.9}
\]

The numerator target remains

\[
 x^{1997/1200-\eta},\qquad \eta>0,
 \tag{1.10}
\]

and the physical target is \(x^{399/400-\eta}\).  V43 does not
assume either target.  It identifies the exact transform joining them.

## 2. Ordered factor freeze and the folded atlas

V35 gives

\[
 \boxed{
 \beta(t)=\sum_{\substack{dk=t\\d,k\geq2}}
 \mu(d)\omega_x(d,k),}
 \tag{2.1}
\]

\[
 \omega_x(d,k)=
 \begin{cases}
 -\log d/\log(dk),&d\leq U,\\[2mm]
 \log k/\log(dk),&d>U.
 \end{cases}
 \tag{2.2}
\]

For \(u\in I_x\) and \(2\leq d\leq x/2\), define the product-frozen
ordered coefficient

\[
 \vartheta_x(d;u)=
 \begin{cases}
 -\mu(d)\log d/\log u,&d\leq U,\\[2mm]
 \mu(d)\log(u/d)/\log u,&d>U.
 \end{cases}
 \tag{2.3}
\]

If \(t=dk\in I_x\), then the mean-value theorem gives uniformly

\[
 \mu(d)\omega_x(d,k)
 =\vartheta_x(d;u)
 +O\!\left(\frac{|u-t|}{x\log x}\right).
 \tag{2.4}
\]

At the diagonal there is no error:

\[
 \boxed{
 \sum_{\substack{d\mid u\\2\leq d\leq x/2}}
 \vartheta_x(d;u)=\beta(u).}
 \tag{2.5}
\]

The absent endpoints \(d=1\) and \(k=1\) have their true zero
coefficients.  Equation (2.5), rather than a divisor envelope, is what will
reassemble the zero axis.

There is also an exact unordered view.  If \(t=s\ell\), \(s<\ell\), then
the two ordered occurrences fold to

\[
 \mu(s)\omega_x(s,\ell)+\mu(\ell)\omega_x(\ell,s)
 =
 \begin{cases}
 (\mu(\ell)-\mu(s))\dfrac{\log s}{\log t},&s\leq U,\\[3mm]
 \dfrac{\mu(s)\log\ell+\mu(\ell)\log s}{\log t},&s>U.
 \end{cases}
 \tag{2.6}
\]

For a square \(t=s^2\), necessarily \(s>U\), and its single ordered
coefficient is

\[
 \frac{\mu(s)}2.
 \tag{2.7}
\]

Because \(U^2=x^{266/400}<x/2\) eventually, both factors can never be at
most \(U\).  Formula (2.6) also records a firewall: a square-free
semiprime with \(s,\ell>1\), \(s\leq U\), and
\(\mu(s)=\mu(\ell)=-1\) has zero folded coefficient.  Taking absolute
values of its two orientations creates false mass.

## 3. Complete centered Poisson identity

Fix \(q\in\mathcal Q\) and integers \(d,u\) with \(q\nmid du\).  Let

\[
 r\equiv u\overline d\pmod q
 \tag{3.1}
\]

and define the q-periodic unit-centered vector

\[
 v_{q,r}(k)=\mathbf1_{q\nmid k}
 \left(\mathbf1_{k\equiv r\ (q)}-\frac1{q-1}\right).
 \tag{3.2}
\]

Its mean is exactly zero.  With normalized discrete Fourier transform,

\[
 \widehat v_{q,r}(0)=0,
 \qquad
 \widehat v_{q,r}(a)=
 \frac1q\left(e_q(-ar)+\frac1{q-1}\right)
 \quad(a\ne0).
 \tag{3.3}
\]

Set

\[
 \mathcal P_{q,d}(u)=
 \sum_{k\in\mathbb Z}K_H(u-dk)v_{q,r}(k).
 \tag{3.4}
\]

Fourier inversion in (3.3), followed by Poisson summation with the convention
(1.4), gives

\[
 \begin{aligned}
 \mathcal P_{q,d}(u)
 ={}&\frac H{dq}
 \sum_{\substack{m\in\mathbb Z\setminus\{0\}\\q\nmid m}}
 \psi\!\left(\frac{Hm}{dq}\right)\\
 &\times\left{
 e_d\!\left(mu\overline q\right)
 +\frac1{q-1}e_{dq}(mu)
 \right}.
 \end{aligned}
 \tag{3.5}
\]

Here \(\overline q\) is the inverse of \(q\pmod d\).  The phase sign is
forced.  If \(d\overline d=1+\ell q\), then

\[
 e_q(-mu\overline d)e_{dq}(mu)
 =e_d(-mu\ell)=e_d(mu\overline q).
 \tag{3.6}
\]

The zero Fourier mode is absent.  Define the safe cutoff

\[
 Y_0=\frac H{4Q}=x^{31/96+o(1)}.
 \tag{3.7}
\]

For \(d\leq Y_0\) and \(q\leq2Q\), one has \(dq/H\leq1/2\).  Since
\(m\ne0\) and \(\operatorname{supp}\psi\subset[-1,1]\), (3.5) gives the
exact support gap

\[
 \boxed{\mathcal P_{q,d}(u)=0\qquad(d\leq Y_0).}
 \tag{3.8}
\]

This is an exact full-lattice statement.  It is not yet a statement about
the physical off-diagonal row, because that row deletes \(u=dk\).

## 4. Hard-shell and coefficient errors

Define the proper-factor Poisson alias row

\[
 \boxed{
 \mathcal A_q=
 \sum_{\substack{u\in I_x\\q\nmid u}}w(u)
 \sum_{\substack{2\leq d\leq x/2\\q\nmid d}}
 \vartheta_x(d;u)\mathcal P_{q,d}(u).}
 \tag{4.1}
\]

By (3.8), only \(d>Y_0\) contributes to (4.1).

Fix

\[
 T=Hx^\varepsilon,\qquad 0<\varepsilon<\frac{11}{600}.
 \tag{4.2}
\]

The following bookkeeping keeps the hard shell literal.

1. On \(t=dk\in I_x\), (2.4) and the divisor bound give
   \[
   \sum_{t\in I_x}\sum_u
   \frac{|u-t|}{x}|K_H(u-t)c'_q(u-t)|\tau(t)
   \ll \frac{H^2}{q}x^{o(1)}.
   \tag{4.3}
   \]
2. For the \(O(T)\) endpoints \(u\) within distance \(T\) of
   \(x/2\) or \(x\), the complete-lattice extension costs
   \[
   \ll \frac{TH}{q}x^{o(1)}.
   \tag{4.4}
   \]
3. For interior \(u\), every added hard-shell term has
   \(|u-dk|\geq T\); arbitrary-order Schwartz decay makes their total
   \(O_B(x^{-B})\).  The true \(k=1\) endpoint in the positive branch is
   zero.  Its product-frozen extension is absorbed by the boundary estimate
   (4.4) when \(u\) lies in the endpoint layer and by the same Schwartz tail
   in the interior.

For fixed \(t\), the weighted centered first moment used in (4.3) is

\[
 \sum_h|hK_H(h)c'_q(h)|\ll_\psi\frac{H^2}{q}.
 \tag{4.5}
\]

Thus the physical row satisfies uniformly in \(q\)

\[
 \boxed{
 s_q=\mathcal A_q-c'_q(0)
 \sum_{\substack{u\in I_x\\q\nmid u}}\beta(u)w(u)
 +O\!\left(\frac{H^2}{q}x^{\varepsilon+o(1)}\right).}
 \tag{4.6}
\]

The minus sign is essential: the full lattice in (3.4) contains the
diagonal \(k=u/d\), while (1.6) deletes it.  Formula (2.5) reassembles that
deleted diagonal to \(\beta(u)w(u)\).  Consequently the tempting statement
“small \(d\) is paid because (3.8) vanishes” is false.  Small \(d\) has no
nonzero alias, but its zero-axis share survives.

## 5. Scalar transference from Gate B to Gate A

Put

\[
 \mathfrak A_x=\sum_{q\in\mathcal Q}q\mathcal A_q
 \tag{5.1}
\]

and

\[
 B_Q=\sum_{q\in\mathcal Q}\frac{q(q-2)}{q-1}.
 \tag{5.2}
\]

Since

\[
 \frac{q(q-2)}{q-1}=(q-1)-\frac1{q-1},
 \tag{5.3}
\]

one has \(B_Q=L_{\rm pr}+O(x^{o(1)})\).  The unit omission costs

\[
 \sum_{q\in\mathcal Q}q
 \sum_{\substack{u\in I_x\\q\mid u}}|\beta(u)w(u)|
 \ll x^{4/3+o(1)}.
 \tag{5.4}
\]

Multiplying (4.6) by \(q\), summing the prime shell, and using
\(|S_x^{\rm physical}|\leq x^{1+o(1)}\) therefore gives

\[
 \boxed{
 \mathfrak C_x=\mathfrak A_x-L_{\rm pr}S_x^{\rm physical}
 +O\!\left(x^{79/48+\varepsilon+o(1)}+x^{4/3+o(1)}\right).}
 \tag{5.5}
\]

Indeed

\[
 2\cdot\frac{21}{32}+\frac13=\frac{79}{48},
 \qquad
 \frac{1997}{1200}-\frac{79}{48}=\frac{11}{600}.
 \tag{5.6}
\]

Combining (5.5) with the already-paid V35 remainders (1.7) gives

\[
 \boxed{
 \mathfrak D_x=\mathfrak A_x-L_{\rm pr}S_x^{\rm physical}
 +O\!\left(x^{53/32+o(1)}+x^{79/48+\varepsilon+o(1)}\right).}
 \tag{5.7}
\]

The two error margins are

\[
 \frac{1997}{1200}-\frac{53}{32}=\frac{19}{2400},
 \qquad
 \frac{1997}{1200}-\left(\frac{79}{48}+\varepsilon\right)
 =\frac{11}{600}-\varepsilon.
 \tag{5.8}
\]

Using (1.8) and \(S_x^{\rm physical}=J(r_x)+E(r_x)\), (5.7) is
equivalently

\[
 \boxed{
 J(r_x)=\frac{\mathfrak A_x}{L_{\rm pr}}
 +O\!\left(x^{95/96+o(1)}+x^{47/48+\varepsilon+o(1)}\right).}
 \tag{5.9}
\]

After subtracting the already-paid local carrier, the same alias represents
\(J(e_x)\) up to the V29 \(x^{1891/1920+o(1)}\) term.  Thus
\(\mathfrak A_x\) is a literal Gate-A numerator.  Equation (5.7) is not a
proof of the physical target; it is an exact bridge joining the two terminal
requirements.

## 6. Three surviving transform windows

The exact alias (4.1) has the following atlas.

| lane | ordered support | dual support in (3.5) | status |
|---|---|---|---|
| \(\mathsf I_0\) | \(d\leq Y_0\) | empty | exact nonzero-alias deletion; zero axis transferred |
| \(\mathsf I_{\rm tr}\) | \(Y_0<d\leq U\) | \(0<|m|\leq dq/H\leq x^{23/2400+o(1)}\) | short inverse-residue transition |
| \(\mathsf{II}\) | \(d>U,\ k>U\) | nonempty, generally long | balanced/two-long frontier |
| \(\mathsf I_\leftarrow\) | \(d>U,\ k\leq U\) | nonempty; Möbius remains on long \(d\) | reverse Type-I frontier |

The transition exponent is exact:

\[
 \frac{133}{400}+\frac13-\frac{21}{32}
 =\frac{23}{2400}.
 \tag{6.1}
\]

At the balanced center \(d=x^{1/2}\), the dual length is

\[
 \frac12+\frac13-\frac{21}{32}=\frac{17}{96}.
 \tag{6.2}
\]

The square sublane is harmless by an absolute estimate.  There are
\(x^{1/2+o(1)}\) squares in the shell, each row kernel has mass
\(H/q\), and hence

\[
 \sum_q|s_q^{\square}|^2
 \ll x^{1+o(1)}\frac{H^2}{Q}=x^{95/48+o(1)},
 \tag{6.3}
\]

with margin \(1/3\) to \(37/16\).  Directly at scalar level,

\[
 \sum_q q|s_q^{\square}|\ll x^{143/96+o(1)}.
 \tag{6.4}
\]

What remains is not a single symmetric Type-II array.  Formula (2.6) shows
that the long-Möbius orientation and the short-Möbius orientation must both
be retained until their signed reassembly.

## 7. The honest two-gate compiler

Declare two independent hypotheses on the same physical data:

\[
 \mathsf H_A(\eta_A):\quad
 |\mathfrak A_x|\ll x^{1997/1200-\eta_A+o(1)},
 \tag{7.1}
\]

\[
 \mathsf H_B(\eta_B):\quad
 |\mathfrak D_x|\ll x^{1997/1200-\eta_B+o(1)}.
 \tag{7.2}
\]

Then (5.7) gives

\[
 |S_x^{\rm physical}|\ll
 x^{399/400-\eta+o(1)}
 \tag{7.3}
\]

for every

\[
 0<\eta<\min\left\{
 \eta_A,\eta_B,\frac{19}{2400},
 \frac{11}{600}-\varepsilon\right\}.
 \tag{7.4}
\]

This is an AND compiler, not an OR shortcut.  V42's positive-Gram/MPD gate
remains a sufficient implementation of \(\mathsf H_B\).  V43 replaces the
previously opaque Gate-A covariance by the explicit \(d>Y_0\)
inverse-residue alias \(\mathsf H_A\).  The small-factor Poisson gap narrows
the Gate-A theorem; it does not borrow Gate-B credit.

## 8. Primary-source boundary

The source screen is finite, primary-source only, and current on
2026-08-10.

1. [Bettin--Chandee, arXiv:1502.00769v1, Theorem 1](https://arxiv.org/abs/1502.00769)
   accepts three arbitrary arrays in a trilinear Kloosterman-fraction form.
   In (3.5), however, the physical \(w(u)\) is coupled to the numerator
   \(mu\), the denominator \(d\), the moving cutoff \(dq/H\), and the
   ordered \(\vartheta_x(d;u)\).  No source theorem supplies the exact array
   norm and one-outer-scalar reassembly.

2. [Pascadi, arXiv:2404.04239v3, Corollaries 17--18](https://arxiv.org/abs/2404.04239)
   is the strongest horizontal alternative because it accepts a
   level-dependent sequence and an external \(L^2\) weight.  Its input is
   already a smooth incomplete Kloosterman-fraction form.  An exact map from
   (3.5), including the physical coefficient norm and the background term,
   is absent.  Even under the optimistic literal map
   \((r,s,c,d_{\rm aux},n)=(q,d,1,1,|m|u)\), its first inverse-fraction
   summand has ceiling \(x^{2399/1200+o(1)}\), a deficit \(67/200\) from
   the numerator target.  Separating the centered background gives only
   \(x^{1999/1200+o(1)}\), still a deficit \(1/600\), and destroys the
   exact \(d\)-zero-mode cancellation.

3. [Blomer--Pascadi, arXiv:2607.24311v1, Theorem 1.1](https://arxiv.org/abs/2607.24311)
   gives the source-backed \(q^{-1/32}\) saving for a fixed balanced
   Kloosterman cell.  It does not estimate the varying-\(d\), varying-\(q\),
   physical-\(u\) alias (4.1) or its aggregate coefficient budget.

4. [Runbo Li, arXiv:2602.20917v6, Theorem 1.1](https://arxiv.org/abs/2602.20917)
   assumes a fixed residue class and divisor-bounded arrays on two factors of
   the modulus, with
   \[
   Q_1^2Q_2<x^{1-\varepsilon},\qquad
   Q_1^7Q_2^{12}<x^{4-\varepsilon}.
   \tag{8.1}
   \]
   Treating \(U\) and \(Q\) as those factors fails the second condition in
   either order:
   \[
   2U+Q=\frac{599}{600}<1,
   \qquad 7U+12Q=\frac{2531}{400}>4,
   \tag{8.2}
   \]
   \[
   2Q+U=\frac{1199}{1200}<1,
   \qquad 7Q+12U=\frac{1897}{300}>4.
   \tag{8.3}
   \]
   More fundamentally, those are modulus factors, not the proper factors of
   the physical endpoint, and the theorem has neither \(w(u)\) nor the
   zero-deleted centered row.

5. Bazin's arXiv:2607.15137v1 Theorem 8 remains a valid collapsed
   \(\beta\)-marginal input only.  It does not estimate the joint alias
   \(\vartheta_x(d;u)w(u)\mathcal P_{q,d}(u)\).

No checked theorem proves either the whole centered transition alias or the
combined long-Möbius reverse-Type-I and balanced alias at the required power.

## 9. Finite exact falsifiers

The checker retains the following diagnostics.

1. For \(q=5,d=2,u=3\), the vector (3.2) is
   \[
   (0,-1/4,-1/4,-1/4,3/4)
   \tag{9.1}
   \]
   and has mean zero.
2. For \((q,d,H)=(5,2,11)\), (3.5) has no active \(m\); replacing
   \(H=11\) by \(H=9\) activates exactly \(m=\pm1\).
3. For \((q,d,u,m)=(5,3,2,1)\),
   \[
   -\frac{mu\overline d}{q}+\frac{mu}{dq}
   \equiv\frac{mu\overline q}{d}\pmod1.
   \tag{9.2}
   \]
4. For \(q=5,d=2,u=4\), the full centered period has sum zero, but
   deleting the diagonal \(k=2\) leaves \(-3/4\).  This rejects the false
   “small-factor lane paid” claim.
5. With finite cutoff \(U=4\), the folded pair \((s,\ell)=(3,5)\) has
   coefficient zero, \((2,6)\) has a nonzero coefficient, and the square
   \(36=6^2\) has coefficient \(1/2\).
6. The rational exponent ledger freezes (3.7), (5.6), (6.1)--(6.4), and
   both failed Runbo-Li conditions.

These are algebra and typing checks.  They are not asymptotic theorem
evidence.

## 10. Canonical status registry

~~~text
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
~~~

The maximum claim is structural and conditional.  Arithmetic advance remains
`NO`, fixed-atom credit remains zero, strict \(1/400\) remains unpaid,
\(L^2\) remains `NONE`, and `TPC_207_TRIGGER=false`.
