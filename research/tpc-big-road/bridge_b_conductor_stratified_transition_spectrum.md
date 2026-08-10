# Bridge A / Gates A--B V45: conductor-stratified transition spectrum

Date: 2026-08-10

Status: unnumbered big-road research artifact.  This note revisits the V44
transition reciprocal variance at the point where imprimitive characters were
treated as an \(x^{o(1)}\) nuisance.  That treatment is not uniform: a primitive
character of small conductor is induced into many reduced moduli \(s\).  The
correct decomposition is by primitive conductor.  The high-conductor spectrum
is paid unconditionally by interpolating a second-moment large-sieve bound with
a fourth-moment large-sieve bound.  The principal character and all remaining
low-conductor characters form one explicit Gauss--Ramanujan structured major
spectrum.  Only that structured spectrum remains open in the transition
window.  Long-Mobius windows and the independent Gate-B numerator remain open.
There is route advance, but no arithmetic trigger.

## 1. Frozen V44 transition object

Keep

\[
 H=x^{21/32},\qquad Q=x^{1/3},\qquad
 U=x^{133/400},\qquad Y_0=\frac{H}{4Q}=x^{31/96+o(1)},
 \tag{1.1}
\]

\[
 P=\frac{Q^2}{H}=x^{1/96},\qquad
 D_0=P^{1/2}=x^{1/192}.
 \tag{1.2}
\]

For \(s\) on the support of V44's coefficient

\[
 \lambda_s=-\sum_{\substack{g\geq1,(g,s)=1\\Y_0<gs\leq U}}
 \frac{\mu(gs)\log(gs)}{gs},
 \qquad |\lambda_s|\ll \frac{x^{o(1)}}s,
 \tag{1.3}
\]

one has \(s\) square-free, \(H/(2Q)\leq s\leq U<Q\), and

\[
 0<|n|\leq\frac{sq}{H},\qquad (n,s)=1.
 \tag{1.4}
\]

On \(G_s=(\mathbb Z/s\mathbb Z)^\times\), put

\[
 C_s(r)=\lambda_s\sum_{q\in\mathcal Q}
 \sum_n\psi\!\left(\frac{Hn}{sq}\right)
 \mathbf1_{r\equiv n\overline q\pmod s},
 \tag{1.5}
\]

\[
 F_s(r)=\sum_{u\in I_x}b(u)e_s(ru),\qquad
 b(u)=\mathbf1_{I_x}(u)\frac{\Lambda(u+2)-b_x^{(z)}(u)}{\log u}.
 \tag{1.6}
\]

The common primary spike is exactly

\[
 \mathfrak T_x^{\rm com}=H\sum_s\sum_{r\in G_s}C_s(r)F_s(r).
 \tag{1.7}
\]

V44 already paid the physical \(q\mid u\) correction and the centered
background:

\[
 \mathfrak A_x^{\rm tr}=\mathfrak T_x^{\rm com}
 +O\!\left(x^{319/192+o(1)}+x^{7171/4800+o(1)}\right).
 \tag{1.8}
\]

Nothing in V45 changes these terms, their signs, or the one-outer-absolute
reassembly.

## 2. Exact character inversion and conductor split

For a character \(\chi\pmod s\), define

\[
 \widehat C_s(\chi)=\sum_{r\in G_s}C_s(r)\overline{\chi(r)},
 \qquad
 \check F_s(\chi)=\sum_{r\in G_s}F_s(r)\chi(r).
 \tag{2.1}
\]

Then

\[
 \widehat C_s(\chi)=\lambda_s\sum_{q\in\mathcal Q}\sum_n
 \psi\!\left(\frac{Hn}{sq}\right)
 \overline{\chi(n)}\chi(q),
 \tag{2.2}
\]

and finite Fourier inversion gives

\[
 \boxed{
 \mathfrak T_x^{\rm com}
 =H\sum_s\frac1{\varphi(s)}\sum_{\chi\ ({\rm mod}\ s)}
 \widehat C_s(\chi)\check F_s(\chi).}
 \tag{2.3}
\]

Because \(s\) is square-free, every \(\chi\pmod s\) is induced from a unique
primitive character \(\chi^*\pmod d\), where \(d\mid s\).  Its primitive
conductor is denoted by \({\rm cond}(\chi)=d\).  Define

\[
 \mathfrak M_{<D_0}^{\rm tr}
 =H\sum_s\frac1{\varphi(s)}
 \sum_{\substack{\chi\ ({\rm mod}\ s)\\{\rm cond}(\chi)<D_0}}
 \widehat C_s(\chi)\check F_s(\chi),
 \tag{2.4}
\]

\[
 \mathfrak V_{\geq D_0}^{\rm tr}
 =H\sum_s\frac1{\varphi(s)}
 \sum_{\substack{\chi\ ({\rm mod}\ s)\\{\rm cond}(\chi)\geq D_0}}
 \widehat C_s(\chi)\check F_s(\chi).
 \tag{2.5}
\]

Thus, before any outer absolute value,

\[
 \boxed{
 \mathfrak T_x^{\rm com}
 =\mathfrak M_{<D_0}^{\rm tr}+\mathfrak V_{\geq D_0}^{\rm tr}.}
 \tag{2.6}
\]

The conductor-one summand in (2.4) is exactly V44's principal Ramanujan
mean.  The remaining summands in (2.4) are nonprincipal characters modulo
\(s\), but they have small primitive conductor.  Centering only deletes the
conductor-one row; it does not delete this induced low-conductor tower.

## 3. Exact Gauss--Ramanujan form of the low spectrum

Write \(s=de\), \((d,e)=1\), and let \(\chi\pmod s\) be induced from primitive
\(\chi^*\pmod d\).  With

\[
 \tau(\chi^*)=\sum_{a\ ({\rm mod}\ d)}\chi^*(a)e_d(a),
 \tag{3.1}
\]

the Chinese remainder theorem and the primitive Gauss identity give

\[
 \sum_{r\in G_{de}}\chi(r)e_{de}(ru)
 =\tau(\chi^*)\chi^*(e)\overline{\chi^*(u)}c_e(u).
 \tag{3.2}
\]

The extension of \(\chi^*\) by zero makes (3.2) valid also when
\((u,d)>1\).  Consequently

\[
 \boxed{
 \check F_{de}(\chi)=
 \tau(\chi^*)\chi^*(e)
 \sum_{u\in I_x}b(u)\overline{\chi^*(u)}c_e(u).}
 \tag{3.3}
\]

Together with (2.2), this writes the low spectrum as one explicit signed
sum of a prime character polynomial, a short integer character polynomial,
and a physical character--Ramanujan polynomial.  It is not an unspecified
exceptional set.

There is additional exact local structure.  For square-free \(e\),

\[
 \boxed{
 \mu(e)c_e(u)=\mu((e,u))\varphi((e,u)).}
 \tag{3.4}
\]

Indeed, with \(h=(e,u)\), the standard formula
\(c_e(u)=\mu(e/h)\varphi(e)/\varphi(e/h)\) and square-freeness give (3.4).
Since \(\lambda_{de}\) contains the factor \(\mu(e)\), the induced-modulus
part of (3.3) is an Euler/Ramanujan local-density tower.  This is the reason
for retaining all \(d<D_0\) modes together with the principal mode as a
structured major spectrum.

## 4. Collision geometry and the corrected imprimitive ledger

On a dyadic block \(s\asymp S\), let

\[
 N\asymp\frac{SQ}{H}.
 \tag{4.1}
\]

Two reciprocal occupancies collide precisely when

\[
 n_1\overline{q_1}\equiv n_2\overline{q_2}\pmod s,
 \qquad\text{equivalently}\qquad
 n_1q_2-n_2q_1=\ell s.
 \tag{4.2}
\]

The support gives \(|\ell|\ll Q^2/H=P\).  Thus the variance is a short
integer--prime multiplicative collision energy.

Now place the primitive conductor in a dyadic block \(d\asymp D\).  For
fixed \(d\), the modulus \(s=de\asymp S\) runs through about \(S/D\) induced
extensions.  From (1.3), uniformly in such extensions,

\[
 \sum_{\substack{s\asymp S\\d\mid s}}
 \frac{|\lambda_s|^2}{\varphi(s)}
 \ll\frac{x^{o(1)}}{D S^2}.
 \tag{4.3}
\]

This factor \(1/D\) is the correct induction ledger.  Saying merely that
imprimitive characters cost \(x^{o(1)}\) loses the repeated low-conductor
tower and is not a valid uniform replacement for (4.3).

The smooth factor in (2.2) is Mellin-separated on dyadic \(s,q,n\) blocks.
The two signs of \(n\) are treated separately.  The condition
\((n,e)=1\) is inserted by Mobius inversion; its divisor weights cost only
\(x^{o(1)}\).  Apply the primitive estimate uniformly for each fixed induced
cofactor \(e\asymp S/D\), and only then sum the \(O(S/D)\) possible
cofactors.  The conductor block is bounded by

\[
 \mathcal V_D(S)\ll\frac{x^{o(1)}}{D S^2}
 \sup_{e\asymp S/D}
 \sum_{d\asymp D}\sum_{\chi^*\ ({\rm mod}\ d)}^*
 |Q_{\chi^*}|^2|N_{e,\chi^*}|^2,
 \tag{4.4}
\]

where \(Q_{\chi^*}\) is supported on primes \(q\asymp Q\),
\(N_{e,\chi^*}\) is supported on \(|n|\asymp N\), and both coefficient
families have divisor-bounded energy.

## 5. Two primitive large-sieve bounds

The primitive multiplicative large sieve applied to the \(q\)-polynomial,
while the \(n\)-polynomial is bounded trivially, gives

\[
 \boxed{
 \mathcal V_D^{(2)}(S)
 \ll \frac{N^2}{D S^2}(D^2+Q)Qx^{o(1)}
 =P^2\left(\frac DQ+\frac1D\right)x^{o(1)}.}
 \tag{5.1}
\]

For the fourth-moment alternative, square each polynomial and apply the
same primitive large sieve to its Dirichlet convolution.  The convolution
energies are \(Q^2x^{o(1)}\) and \(N^2x^{o(1)}\), respectively.  Hence

\[
 \sum_{d\asymp D}\sum_{\chi^*}^*|Q_{\chi^*}|^4
 \ll(D^2+Q^2)Q^2x^{o(1)},
 \tag{5.2}
\]

\[
 \sum_{d\asymp D}\sum_{\chi^*}^*|N_{\chi^*}|^4
 \ll(D^2+N^2)N^2x^{o(1)}.
 \tag{5.3}
\]

Since \(D\leq S<U<Q\), Cauchy in (4.4) gives

\[
 \boxed{
 \mathcal V_D^{(4)}(S)
 \ll
 \begin{cases}
 P^2N^{-1}x^{o(1)},&D>N,\\
 P^2D^{-1}x^{o(1)},&D\leq N.
 \end{cases}}
 \tag{5.4}
\]

Equations (5.1) and (5.4) are estimates for the same conductor block.  No
unproved independence is used when their minimum is taken.

## 6. The high-conductor spectrum is paid

Let \(D\geq D_0=P^{1/2}\).  If

\[
 D\leq\frac Q{P^{1/2}},
 \tag{6.1}
\]

then both terms in (5.1) are at most \(P^{3/2}\).  If instead

\[
 D>\frac Q{P^{1/2}},
 \tag{6.2}
\]

the relation \(D\leq S=NQ/P\) implies \(N>P^{1/2}\).  In either branch of
(5.4), the fourth-moment estimate is then at most \(P^{3/2}\).  Summing the
dyadic \(S,D\) blocks costs \(x^{o(1)}\), and therefore

\[
 \boxed{
 \mathcal V_{\geq D_0}\ll P^{3/2}x^{o(1)}
 =x^{1/64+o(1)}.}
 \tag{6.3}
\]

The physical additive large sieve from V44 remains

\[
 \sum_s\sum_{r\in G_s}|F_s(r)|^2\ll x^{2+o(1)}.
 \tag{6.4}
\]

Character Parseval, (6.3), and (6.4) yield the unconditional strict payment

\[
 \boxed{
 |\mathfrak V_{\geq D_0}^{\rm tr}|
 \ll HxP^{3/4}x^{o(1)}
 =x^{213/128+o(1)}.}
 \tag{6.5}
\]

Its exact margin below the transition numerator target is

\[
 \boxed{
 \frac{1997}{1200}-\frac{213}{128}=\frac1{9600}.}
 \tag{6.6}
\]

This pays a genuine physical subcomponent.  It does not estimate the
low-conductor spectrum and does not create fixed-atom credit.

## 7. The one remaining transition gate

The structured low spectrum has the unconditional ceiling

\[
 |\mathfrak M_{<D_0}^{\rm tr}|\ll x^{5/3+o(1)},
 \tag{7.1}
\]

because its conductor-one part is V44's principal ceiling and its
nonprincipal projection is bounded by the corrected aggregate
\(P^2x^{o(1)}\) character energy obtained by summing (5.1)--(5.4) over all
conductor blocks.

Neither (5.1) nor (5.4) supplies a uniform fixed power for
\(d<D_0\).  In particular, the second term \(P^2/D\) in (5.1) returns the
V44 endpoint at small \(D\).  The low-conductor theorem gate is

\[
 \boxed{
 \mathsf H_{<D_0}(\eta_<):\quad
 |\mathfrak M_{<D_0}^{\rm tr}|
 \ll x^{1997/1200-\eta_<+o(1)},
 \qquad \eta_<>0.}
 \tag{7.2}
\]

Combining (1.8), (2.6), and (6.5), hypothesis (7.2) gives, for every

\[
 0<\eta_{\rm tr}<
 \min\left\{\eta_<,\frac1{9600},\frac{13}{4800},
 \frac{817}{4800}\right\},
 \tag{7.3}
\]

the conditional transition estimate

\[
 \boxed{
 |\mathfrak A_x^{\rm tr}|
 \ll x^{1997/1200-\eta_{\rm tr}+o(1)}.}
 \tag{7.4}
\]

Thus V44's two open transition gates are replaced by one structured
low-conductor major-spectrum gate.  The balanced window \(d>U,k>U\), the
reverse-Type-I window \(d>U,k\leq U\), and V42's positive-Gram Gate B remain
independent open spans.

The selected road after V45 is

```text
high-conductor transition spectrum PAID
  -> principal + low-conductor structured major spectrum
  -> balanced / reverse-Type-I long-Mobius alias
  -> V42 positive-Gram Gate B in parallel
  -> V43 A+B zero-axis reassembly
  -> distinguished-seed dynamics reserve.
```

## 8. Primary-source boundary

The screen is primary-source-only and fail-closed as of 2026-08-10.

1. Bombieri--Friedlander--Iwaniec,
   [*Primes in arithmetic progressions to large moduli*, (1.6), Theorem 0,
   and its proof](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6385-11511_2006_Article_BF02399204.pdf),
   states the primitive multiplicative large sieve used in (5.1)--(5.3).
   Its proof of Theorem 0 explicitly writes an imprimitive character as one
   induced from conductor \(d\), treats small conductors by the
   Siegel--Walfisz hypothesis, and large conductors by (1.6).  This supports
   the conductor split and the high-conductor estimates.  The small-
   conductor input is logarithmic; it does not prove (7.2).

2. Conrey--Iwaniec--Soundararajan,
   [*Asymptotic Large Sieve*, arXiv:1105.1176](https://arxiv.org/abs/1105.1176),
   develops an asymptotic large sieve for primitive characters.  It confirms
   that primitive-conductor organization is structural, but its hypotheses
   and asymptotic bilinear form do not identify the physical polynomial in
   (3.3) or prove (7.2).

3. Matomaki--Teravainen,
   [*Products of primes in arithmetic progressions*,
   arXiv:2301.07679](https://arxiv.org/abs/2301.07679), explicitly separates
   possible quadratic-character obstructions and uses a multiplicative dense
   model because a uniform maximum bound for prime character sums at
   conductor scale is unavailable.  Their ternary product problem and Burgess
   length hypotheses do not match the V45 short \(n\)-polynomial or the
   physical \(b(u)c_e(u)\) factor.  It is a warning against deleting the low
   spectrum, not a theorem attachment.

4. Standard Bombieri--Vinogradov, Barban--Davenport--Halberstam, and
   Siegel--Walfisz estimates give logarithmic savings in the relevant
   small-conductor source interface.  A fixed logarithmic power cannot pay
   the strict \(1/400\) endpoint.  Landau--Page isolation of a possible
   exceptional real character limits multiplicity but does not estimate the
   full signed tower (3.3).

No checked primary theorem accepts the principal plus induced
low-conductor Gauss--Ramanujan spectrum with the literal
\(\Lambda(u+2)-b_x^{(z)}(u)\) physical coefficient and proves (7.2).

## 9. Finite exact diagnostics

The checker freezes the following algebra and loss ledger.

1. For \(s=5\), \((q_1,q_2,n_1,n_2)=(7,11,1,3)\), both reciprocal
   residues are \(3\pmod5\), and

   \[
   n_1q_2-n_2q_1=-10=-2s.
   \tag{9.1}
   \]

2. For \(s=6,d=3,e=2\), the nonprincipal quadratic character modulo \(3\)
   induces a nonprincipal character modulo \(6\).  With
   \(\zeta=e_6(1)\) and \(\zeta^2-\zeta+1=0\), (3.2) at \(u=1\) is

   \[
   \zeta-\zeta^5=\zeta^2-\zeta^4=-1+2\zeta.
   \tag{9.2}
   \]

   The centered occupancy \((-1/2,1/2)\) on residues \((1,5)\) has a
   nonzero coefficient against this conductor-three character.  Principal
   centering therefore does not remove all low-conductor modes.

3. For every tested square-free \(e\), the checker verifies
   \(\mu(e)c_e(u)=\mu((e,u))\varphi((e,u))\).  A mutation that drops
   \(\mu(e)\) is rejected.

4. The conductor interpolation is checked in both regions
   \(D\leq Q/P^{1/2}\) and \(D>Q/P^{1/2}\), including the implication
   \(D\leq S=NQ/P\Rightarrow N>P^{1/2}\) in the second region.

5. The exact exponent ledger freezes
   \(D_0=1/192\), high-conductor variance exponent \(1/64\), output
   \(213/128\), and strict margin \(1/9600\).

These are finite identity and typing tests, not asymptotic theorem evidence.

## 10. Canonical status registry

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

The maximum claim is a source-backed strict payment for one conductor
component plus an exact route reduction.  Arithmetic advance remains `NO`,
fixed-atom credit remains zero, strict \(1/400\) remains unpaid, global
\(L^2\) remains `NONE`, and `TPC_207_TRIGGER=false`.
