# Bridge A / Gates A--B V44: transition reciprocal variance and the principal Ramanujan mean

Date: 2026-08-10

Status: unnumbered big-road research artifact.  Starting from the exact V43
proper-factor Poisson alias, this note completely compiles the short transition
window \(H/(4Q)<d\leq U\).  A gcd reduction removes the common divisor of the
Poisson frequency and the proper factor, after which the primary inverse-residue
alias splits exactly into a principal Ramanujan mean and a centered reciprocal
variance.  The physical \(q\mid u\) correction and the centered background are
paid unconditionally.  The two surviving terms each have a natural
\(x^{5/3+o(1)}\) ceiling and require a fixed power beyond \(1/400\).  No checked
primary source supplies either required whole-object saving.  There is route
advance, but no arithmetic trigger.

## 1. Frozen transition scalar

Keep the V43 data

\[
 H=x^{21/32},\qquad Q=x^{1/3},\qquad
 U=x^{133/400},\qquad Y_0=\frac{H}{4Q}=x^{31/96+o(1)},
 \tag{1.1}
\]

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},
 \tag{1.2}
\]

\[
 w(u)=\Lambda(u+2)-b_x^{(z)}(u),\qquad
 b(u)=\mathbf1_{I_x}(u)\frac{w(u)}{\log u}.
 \tag{1.3}
\]

The V43 scalar alias is

\[
 \mathfrak A_x=\sum_{q\in\mathcal Q}q\mathcal A_q,
 \tag{1.4}
\]

where the transition part \(Y_0<d\leq U\) of the spike phase in the
complete Poisson identity is

\[
 \begin{aligned}
 \mathfrak T_x^{\rm unit}
 ={}&-H\sum_{q\in\mathcal Q}
 \sum_{Y_0<d\leq U}\frac{\mu(d)\log d}{d}
 \sum_{\substack{m\ne0\\ |m|\leq dq/H}}
 \psi\!\left(\frac{Hm}{dq}\right)\\
 &\hspace{21mm}\times
 \sum_{\substack{u\in I_x\\q\nmid u}}
 \frac{w(u)}{\log u}
 e_d(mu\overline q).
 \end{aligned}
 \tag{1.5}
\]

There are no hidden \(q\)-nonunit rows in \(d\) or \(m\).  Indeed, eventually

\[
 d\leq U<Q<q,
 \qquad
 |m|\leq\frac{2UQ}{H}=x^{23/2400+o(1)}<q.
 \tag{1.6}
\]

The corresponding background term is

\[
 \begin{aligned}
 \mathfrak B_x^{\rm unit}
 ={}&-H\sum_{q\in\mathcal Q}
 \sum_{Y_0<d\leq U}\frac{\mu(d)\log d}{d(q-1)}
 \sum_{\substack{m\ne0\\ |m|\leq dq/H}}
 \psi\!\left(\frac{Hm}{dq}\right)\\
 &\hspace{21mm}\times
 \sum_{\substack{u\in I_x\\q\nmid u}}
 \frac{w(u)}{\log u}e_{dq}(mu).
 \end{aligned}
 \tag{1.7}
\]

Thus the full V43 transition component is

\[
 \mathfrak A_x^{\rm tr}=\mathfrak T_x^{\rm unit}
 +\mathfrak B_x^{\rm unit}.
 \tag{1.8}
\]

All V43 hard-shell, coefficient-freeze, and zero-axis errors remain paid and
are not reopened here.

## 2. Exact gcd reduction

Because \(\mu(d)\ne0\), write uniquely

\[
 g=(|m|,d),\qquad d=gs,\qquad m=gn,
 \qquad (g,s)=(n,s)=1,
 \tag{2.1}
\]

with \(g,s\) square-free and \(n\ne0\).  Both the cutoff and the spike phase
lose \(g\):

\[
 \psi\!\left(\frac{Hm}{dq}\right)
 =\psi\!\left(\frac{Hn}{sq}\right),
 \qquad
 e_d(mu\overline q)=e_s(nu\overline q).
 \tag{2.2}
\]

The background phase retains \(q\) but also loses \(g\):

\[
 e_{dq}(mu)=e_{sq}(nu).
 \tag{2.3}
\]

Define the exact reduced-modulus coefficient

\[
 \boxed{
 \lambda_s=-\sum_{\substack{g\geq1\\(g,s)=1\\Y_0<gs\leq U}}
 \frac{\mu(gs)\log(gs)}{gs}.}
 \tag{2.4}
\]

It satisfies

\[
 |\lambda_s|\ll\frac{x^{o(1)}}s.
 \tag{2.5}
\]

Nonempty dual support forces

\[
 \frac{H}{2Q}\leq s\leq U,
 \qquad
 0<|n|\leq\frac{sq}{H}\leq\frac{2UQ}{H}
 =x^{23/2400+o(1)}.
 \tag{2.6}
\]

In prime-shell units this is

\[
 Q^{31/32+o(1)}\leq s\leq Q^{399/400+o(1)}.
 \tag{2.7}
\]

The common divisor \(g\) is therefore only a harmonic outer multiplicity;
it is neither a new dual length nor a phase conductor.

## 3. Reciprocal occupancy and exact mean--fluctuation split

For \(r\in(\mathbb Z/s\mathbb Z)^\times\), define

\[
 C_s(r)=\lambda_s\sum_{q\in\mathcal Q}
 \sum_{\substack{n\ne0, (n,s)=1\\|n|\leq sq/H}}
 \psi\!\left(\frac{Hn}{sq}\right)
 \mathbf1_{r\equiv n\overline q\pmod s},
 \tag{3.1}
\]

and the physical additive transform

\[
 F_s(r)=\sum_{u\in I_x}b(u)e_s(ru).
 \tag{3.2}
\]

Removing the mask \(q\nmid u\) for the moment gives the exact common spike

\[
 \boxed{
 \mathfrak T_x^{\rm com}
 =H\sum_s\sum_{r\in(\mathbb Z/s\mathbb Z)^\times}C_s(r)F_s(r).}
 \tag{3.3}
\]

Put

\[
 \overline C_s=\frac1{\varphi(s)}\sum_{r\in(\mathbb Z/s\mathbb Z)^\times}C_s(r),
 \qquad
 C_s^\circ(r)=C_s(r)-\overline C_s.
 \tag{3.4}
\]

Since

\[
 \sum_{r\in(\mathbb Z/s\mathbb Z)^\times}e_s(ru)=c_s(u),
 \tag{3.5}
\]

where \(c_s\) is the Ramanujan sum, (3.3) splits exactly as

\[
 \boxed{
 \mathfrak T_x^{\rm com}=\mathfrak M_x^{\rm tr}
 +\mathfrak V_x^{\rm tr},}
 \tag{3.6}
\]

\[
 \boxed{
 \mathfrak M_x^{\rm tr}
 =H\sum_s\overline C_s\sum_{u\in I_x}b(u)c_s(u),}
 \tag{3.7}
\]

\[
 \boxed{
 \mathfrak V_x^{\rm tr}
 =H\sum_s\sum_{r\in(\mathbb Z/s\mathbb Z)^\times}
 C_s^\circ(r)F_s(r).}
 \tag{3.8}
\]

This split occurs before the first outer absolute value.  The principal term
is not dropped and the centered term is not called random.

Character Parseval gives the exact identity

\[
 \sum_{r}|C_s^\circ(r)|^2
 =\frac{|\lambda_s|^2}{\varphi(s)}
 \sum_{\substack{\chi\ ({\rm mod}\ s)\\\chi\ne\chi_0}}
 \left|
 \sum_{q\in\mathcal Q}\sum_n
 \psi\!\left(\frac{Hn}{sq}\right)
 \chi(n)\overline{\chi(q)}
 \right|^2.
 \tag{3.9}
\]

Thus the new variance is a literal prime--short-integer reciprocal-residue
variance, not a generic Kloosterman cell.

## 4. The generic fourth-moment ceiling and the missing power

Set

\[
 P=\frac{Q^2}{H}=x^{1/96}.
 \tag{4.1}
\]

Define the coefficient variance

\[
 \mathcal V_{\rm rec}
 =\sum_s\sum_{r\in(\mathbb Z/s\mathbb Z)^\times}|C_s^\circ(r)|^2.
 \tag{4.2}
\]

On a dyadic block \(s\asymp S\), Mellin separation of the smooth factor in
(3.9) costs \(x^{o(1)}\).  Put \(N\asymp SQ/H\).  Applying the multiplicative
large sieve to the squares of the \(q\)-sum and the \(n\)-sum gives

\[
 \sum_{s\asymp S}\frac{s}{\varphi(s)}
 \sum_\chi^*\left|\sum_{q\asymp Q}a_q\chi(q)\right|^4
 \ll (S^2+Q^2)Q^2x^{o(1)},
 \tag{4.3}
\]

\[
 \sum_{s\asymp S}\frac{s}{\varphi(s)}
 \sum_\chi^*\left|\sum_{|n|\asymp N}b_n\chi(n)\right|^4
 \ll (S^2+N^2)N^2x^{o(1)}.
 \tag{4.4}
\]

The product energies in (4.3)--(4.4) are divisor-bounded.  Inducing
imprimitive characters costs \(x^{o(1)}\).  Cauchy and (2.5) give

\[
 \mathcal V_{\rm rec}(S)
 \ll \frac{Q^2N}{S^2}x^{o(1)}
 =\frac{Q^3}{SH}x^{o(1)}.
 \tag{4.5}
\]

Since \(S\geq H/(2Q)\), summing the dyadic blocks yields the unconditional
large-sieve ceiling

\[
 \boxed{
 \mathcal V_{\rm rec}\ll P^2x^{o(1)}=x^{1/48+o(1)}.}
 \tag{4.6}
\]

On the physical side, the additive large sieve and
\(\lVert b\rVert_2^2\ll x^{1+o(1)}\) give

\[
 \sum_s\sum_{r\in(\mathbb Z/s\mathbb Z)^\times}|F_s(r)|^2
 \ll(x+U^2)\|b\|_2^2x^{o(1)}
 \ll x^{2+o(1)}.
 \tag{4.7}
\]

Consequently (4.6) gives only

\[
 |\mathfrak V_x^{\rm tr}|
 \ll H\,x\,P\,x^{o(1)}=x^{5/3+o(1)}.
 \tag{4.8}
\]

The strict numerator target is \(x^{1997/1200-\eta}\), and

\[
 \frac53-\frac{1997}{1200}=\frac1{400}.
 \tag{4.9}
\]

Thus ordinary fourth-moment large sieve lands exactly on the wrong side of
the endpoint.

The precise new variance gate is

\[
 \boxed{
 \mathsf H_{\rm var}(\kappa):\quad
 \mathcal V_{\rm rec}\ll P^2x^{-\kappa+o(1)},
 \qquad \kappa>\frac1{200}.}
 \tag{4.10}
\]

It implies

\[
 |\mathfrak V_x^{\rm tr}|
 \ll x^{5/3-\kappa/2+o(1)}.
 \tag{4.11}
\]

The diagonal/random benchmark is

\[
 \mathcal V_{\rm rec}\ll Px^{o(1)}.
 \tag{4.12}
\]

At that benchmark

\[
 |\mathfrak V_x^{\rm tr}|
 \ll x^{319/192+o(1)},
 \qquad
 \frac{1997}{1200}-\frac{319}{192}=\frac{13}{4800}.
 \tag{4.13}
\]

Equation (4.12) is a design target, not a proved estimate.

## 5. The two paid corrections

### 5.1 The physical \(q\mid u\) mask

Let \(\mathfrak U_x^{\rm tr}\) be the term removed from
\(\mathfrak T_x^{\rm com}\) by restoring \(q\nmid u\).  For fixed \(q\), the
map \(n\mapsto n\overline q\pmod s\) is injective on the dual support because
\(|n|=o(s)\).  Therefore the direct-sum coefficient energy is

\[
 \sum_{q,s,n}|\lambda_s|^2
 \left|\psi\!\left(\frac{Hn}{sq}\right)\right|^2
 \ll \frac{Q^2}{H}x^{o(1)}=Px^{o(1)}.
 \tag{5.1}
\]

Every \(u\in I_x\) is divisible by at most three primes in \(\mathcal Q\),
since four such primes have product greater than \(x\).  Hence

\[
 \sum_{q\in\mathcal Q}\|b\mathbf1_{q\mid u}\|_2^2
 \ll x^{1+o(1)}.
 \tag{5.2}
\]

The additive large sieve in each \(q\)-fiber and (5.1)--(5.2) give

\[
 \boxed{
 |\mathfrak U_x^{\rm tr}|
 \ll H\,P^{1/2}x^{1+o(1)}
 =x^{319/192+o(1)}.}
 \tag{5.3}
\]

This is a genuine payment; it does not assume (4.10).

### 5.2 The background phase

After (2.1), the background is

\[
 \mathfrak B_x^{\rm unit}
 =H\sum_{q,s}\frac{\lambda_s}{q-1}
 \sum_n\psi\!\left(\frac{Hn}{sq}\right)
 \sum_{\substack{u\in I_x\\q\nmid u}}b(u)e_{sq}(nu).
 \tag{5.4}
\]

Because \(|n|<q\), the reduced denominator of \(n/(sq)\) retains the prime
\(q\).  Fractions with different \(q\)'s cannot collide; the remaining
multiplicity is divisor-bounded.  The coefficient energy is

\[
 \sum_{q,s,n}\left|\frac{\lambda_s}{q-1}\right|^2
 \left|\psi\!\left(\frac{Hn}{sq}\right)\right|^2
 \ll H^{-1}x^{o(1)}.
 \tag{5.5}
\]

The largest denominator is \(O(QU)\).  Removing the unit mask first and
paying its sparse correction as in (5.2), the additive large sieve gives

\[
 \boxed{
 |\mathfrak B_x^{\rm unit}|
 \ll x^{\frac12\cdot\frac{21}{32}+\frac12+\frac13+\frac{133}{400}+o(1)}
 =x^{7171/4800+o(1)}.}
 \tag{5.6}
\]

The sparse background correction is smaller,
\(x^{1+21/64+o(1)}=x^{85/64+o(1)}\).  Since

\[
 \frac{1997}{1200}-\frac{7171}{4800}
 =\frac{817}{4800},
 \tag{5.7}
\]

the full background lane is safely paid.

Combining (3.6), (5.3), and (5.6), the exact transition reassembly is

\[
 \boxed{
 \mathfrak A_x^{\rm tr}
 =\mathfrak M_x^{\rm tr}+\mathfrak V_x^{\rm tr}
 +O\!\left(x^{319/192+o(1)}+x^{7171/4800+o(1)}\right).}
 \tag{5.8}
\]

## 6. The principal Ramanujan mean

From (3.1) and (2.5),

\[
 |\overline C_s|\ll\frac{P}{s}x^{o(1)}.
 \tag{6.1}
\]

The elementary identity

\[
 c_s(u)=\sum_{r\mid(s,u)}r\mu(s/r)
 \tag{6.2}
\]

shows that

\[
 \sum_{u\in I_x}b(u)c_s(u)
 =\sum_{r\mid s}r\mu(s/r)
 \sum_{\substack{u\in I_x\\u\equiv0\pmod r}}b(u).
 \tag{6.3}
\]

Thus \(\mathfrak M_x^{\rm tr}\) is a principal-character AP/Ramanujan
residual, not part of the centered variance.  Since
\(|b(u)|\leq x^{o(1)}\),

\[
 \left|\sum_{u\in I_x}b(u)c_s(u)\right|
 \ll x^{1+o(1)},
 \tag{6.4}
\]

and (6.1) gives the unconditional ceiling

\[
 \boxed{
 |\mathfrak M_x^{\rm tr}|\ll HPx^{1+o(1)}
 =x^{5/3+o(1)}.}
 \tag{6.5}
\]

The shifted-prime and \(b_x^{(z)}\) Euler densities agree on the row
\(u\equiv0\pmod r\) after the forced/excluded rough-prime factors are kept.
V13 proves the required finite-AP comparison for its prime-shell modulus.
For the composite divisors \(r\mid s\) in (6.3), a multiplicative
Euler/CRT extension must be written before maximal Bombieri--Vinogradov and
the Rosser--Iwaniec comparison can be invoked.  Even granting that legal
extension, those inputs provide logarithmic rather than fixed-power saving.
They do not turn (6.5) into the power required by (4.9).

The exact second transition gate is therefore

\[
 \boxed{
 \mathsf H_{\rm mean}(\delta_M):\quad
 |\mathfrak M_x^{\rm tr}|
 \ll x^{5/3-\delta_M+o(1)},
 \qquad \delta_M>\frac1{400}.}
 \tag{6.6}
\]

No cancellation between (6.6) and (4.10) is borrowed.  A theorem may
estimate their signed sum directly, but then it must retain the exact
decomposition (3.6) and one outer absolute value.

## 7. Conditional transition compiler and remaining bridge

If \(\mathsf H_{\rm var}(\kappa)\) and
\(\mathsf H_{\rm mean}(\delta_M)\) hold, then for every

\[
 0<\eta_{\rm tr}<
 \min\left\{
 \frac\kappa2-\frac1{400},
 \delta_M-\frac1{400},
 \frac{13}{4800},
 \frac{817}{4800}
 \right\},
 \tag{7.1}
\]

equation (5.8) gives

\[
 |\mathfrak A_x^{\rm tr}|
 \ll x^{1997/1200-\eta_{\rm tr}+o(1)}.
 \tag{7.2}
\]

This closes the entire V43 transition window conditionally.  It does not
estimate the balanced window \(d>U,k>U\), the reverse-Type-I window
\(d>U,k\leq U\), or the independent V42 Gate-B numerator.  V43's exact
zero-axis transference remains the final AND compiler.

The selected road after V44 is

```text
transition mean + reciprocal variance
  -> balanced / reverse-Type-I long-Mobius alias
  -> V42 positive-Gram Gate B in parallel
  -> V43 A+B zero-axis reassembly
  -> distinguished-seed dynamics reserve.
```

## 8. Primary-source boundary

The screen is primary-source-only and fail-closed as of 2026-08-10.

1. Bombieri--Friedlander--Iwaniec,
   [*Primes in arithmetic progressions to large moduli*, Theorem 0 and
   (1.6)](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6385-11511_2006_Article_BF02399204.pdf),
   supplies the multiplicative large sieve used in (4.3)--(4.6) and a
   general single-sequence Siegel--Walfisz/BDH statement.  The large sieve
   gives the \(P^2\) ceiling here; Theorem 0 does not directly identify the
   reciprocal-ratio fourth moment and, in its native AP interface, provides
   logarithmic rather than fixed-power saving.  Neither statement gives the
   \(x^{-\kappa}\), \(\kappa>1/200\), required in (4.10).

2. Maynard,
   [arXiv:2006.06572v2, Theorem 1.1](https://arxiv.org/abs/2006.06572),
   treats a fixed residue class and moduli with a convenient factor up to
   prime-size exponent \(11/21\).  The V44 moduli have relative exponent
   from \(31/32\) to \(399/400\), and the requested quantity is an
   all-residue reciprocal variance.  There is no literal attachment.

3. Maynard's well-factorable theorem and Runbo Li's large-modulus
   majorants/minorants accept specially factorized modulus weights.  V44
   needs every square-free reduced \(s\), the short numerator \(n\), the
   inverse prime \(q\), and the physical Fourier family \(F_s(r)\) in one
   reassembly.  No checked theorem supplies that interface.

4. Dong--Robles--Zeindler,
   [arXiv:2601.00292v1, main bilinear Kloosterman-fraction theorem](https://arxiv.org/abs/2601.00292),
   accepts two arbitrary arrays in
   \(e(a\overline m/(bn))\) for fixed \(a,b\).  It does not accept the
   moving physical numerator \(nu\), the reciprocal-residue fourth moment,
   or the principal Ramanujan mean.  It is a possible local engine only.

5. Pascadi's horizontal Kuznetsov theorem remains a source-backed local
   alternative after an incomplete Kloosterman form has already been
   emitted.  It does not prove either (4.10) or (6.6) from (1.5).

Therefore the previous single four-variable transition fatal is narrowed to
two explicit endpoint gates, but neither gate receives source-backed
arithmetic credit.

## 9. Finite exact diagnostics

The checker freezes the following algebra and loss ledger.

1. For \((d,m,q,u)=(10,2,7,1)\), one has \((g,s,n)=(2,5,1)\) and

   \[
   e_{10}(2\cdot1\cdot\overline7)
   =e_5(1\cdot1\cdot\overline7)=e_5(3).
   \tag{9.1}
   \]

   The false phase retaining \(g\) is \(e_5(1)\).

2. For \(s=5\), \(q\in\{7,11\}\), and \(n\in\{1,2\}\), the reciprocal
   occupancy on the four unit residues is

   \[
   (2,1,1,0).
   \tag{9.2}
   \]

   Its mean is \(1\), uncentered energy is \(6\), and centered variance is
   \(2\).  This catches omission of the principal term.

3. If \((q,s,n)=(11,6,4)\), then \(n/(sq)=2/33\); the reduced denominator still
   contains \(q\).  Deleting \(q\) from the background conductor is false.

4. A constant occupancy has zero centered variance but a nonzero principal
   mean.  Conversely a zero-mean fluctuation can have positive variance.
   Neither gate implies the other.

5. The exact exponent ledger freezes
   \(P=1/96\), \(P^2=1/48\), the generic output \(5/3\), the endpoint deficit
   \(1/400\), the ideal output \(319/192\), its margin \(13/4800\), and the
   background output \(7171/4800\).

These are finite identity and typing tests, not asymptotic theorem evidence.

## 10. Canonical status registry

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

The maximum claim is structural and conditional.  Arithmetic advance remains
`NO`, fixed-atom credit remains zero, strict \(1/400\) remains unpaid,
\(L^2\) remains `NONE`, and `TPC_207_TRIGGER=false`.
