# Bridge B V26: compensated prime dilation and critical-section block highways

Date: 2026-08-08

Status:

~~~text
EXACT_L0_HIGHWAY_NORMAL_FORMS_AND_SOURCE_LOCAL_INTERFACES
MAXIMUM_CLAIM = EXACT_L0_COMPENSATED_PRIME_DILATION_AND_FACTORIZABLE_J1_SHORT_DUAL_NORMAL_FORMS_PLUS_SOURCE_BACKED_CRITICAL_SEED_ASIP_INTERFACE_AND_WHOLE_SHELL_BLOCK_RETYPE
ROUTE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
~~~

This note does not add another fixed Kloosterman cell.  It compresses the
V25 error into one compensated prime-dilation covariance, records the one
factorable determinant species for which a short-dual compiler really exists,
and corrects the dynamical reserve from a lacunary single-event problem to a
whole-shell block-transfer problem.

The outcome is a route choice, not a twin-prime theorem.  No reviewed primary
source accepts the complete literal physical scalar, and no exact arithmetic
critical-section carrier has been constructed.

## 1. Frozen physical object and type boundary

Keep

\[
h_0=2,\qquad x=2X,\qquad I_x=\{t\in\mathbb Z:x/2<t\le x\},
\]

\[
w_x^{(z)}(u)=\Lambda(u+2)-b_x^{(z)}(u),
\]

and the V19 ordered HB2 coefficient \(\beta_x^{\rm raw}\), including the
literal \(+2,-1\) channel coefficients, occurrence multiplicities,
Möbius/log factors and \(1/\log T_o\) normalization.  V25 gives the exact
Jutila-error multiplier identity

\[
E_x=-\sum_{D\ne0}B_x(D)\kappa(D).
\tag{1.1}
\]

This is an exact \(L0\) rewrite.  It is not a bound for \(E_x\), and it does
not change the original physical main term.

The following indices remain different types:

~~~text
physical shell variables t,u and difference h=u-t;
prime-shell modulus q and dilation index k with h=qk;
factorable auxiliary q_aux=p_aux t_aux;
HB2 rough/smooth slots e_i,f_i and their selected MASTER occurrence;
physical Lambda determinant variables R,S;
hybrid d_rough,e_sieve,r_h;
Farey c,z,u_F and Fourier/rational dummy indices.
~~~

In particular, the prime shell below is not the factorable auxiliary shell,
and the difference \(h\) is not the physical fixed gap \(h_0=2\).  The latter
is already inside \(w_x^{(z)}\).

## 2. Exact compensated prime-dilation normal form

Use the V23 prime shell

\[
Q=x^{1/3},\qquad
\delta=x^{-21/32},\qquad
\mathcal Q=\{q\text{ prime}:Q<q\le2Q\},
\]

\[
R=\#\mathcal Q,\qquad
L_{\rm pr}=\sum_{q\in\mathcal Q}(q-1)=x^{2/3+o(1)}.
\tag{2.1}
\]

For \(h\ne0\), define the literal shifted correlation

\[
\mathcal C_x(h)=\widehat\psi_+(\delta h)
 \sum_{\substack{t,t+h\in I_x}}
 \beta_x^{\rm raw}(t)w_x^{(z)}(t+h).
\tag{2.2}
\]

For prime \(q\), \(c_q(h)=q\mathbf1_{q\mid h}-1\).  Substitution into
the V25 multiplier gives, without an absolute value inside the ensemble,

\[
\boxed{
E_x=-\frac1{L_{\rm pr}}
\sum_{q\in\mathcal Q}
\sum_{\substack{t,u\in I_x\\u\ne t}}
\beta_x^{\rm raw}(t)w_x^{(z)}(u)
\widehat\psi_+(\delta(u-t))
\bigl(q\mathbf1_{u\equiv t\pmod q}-1\bigr).
}
\tag{2.3}
\]

Grouping the divisible branch by \(h=qk\) gives the second exact form

\[
\boxed{
E_x=-\frac1{L_{\rm pr}}
\left[
 \sum_{q\in\mathcal Q}q\sum_{k\ne0}\mathcal C_x(qk)
 -R\sum_{h\ne0}\mathcal C_x(h)
\right].
}
\tag{2.4}
\]

The two terms in brackets are a single compensated object.  Estimating them
separately loses the Ramanujan cancellation.  Replacing (2.3) by a complete
centered projector without using the joint literal coefficient structure
returns exactly to the V21/V22 projector STOP cells.

Thus the selected analytic theorem contract is

~~~text
V26_PRIME_SHELL_RAMANUJAN_COMPENSATED_DILATION_COVARIANCE
  = OPEN_NEW_THEOREM.
~~~

## 3. The exact endpoint window

The Schwartz-effective difference horizon and dilation length are

\[
H=\delta^{-1}=x^{21/32},\qquad
|k|\asymp H/Q=x^{31/96}.
\tag{3.1}
\]

To pay the strict endpoint, the unnormalized bracket in (2.4) must satisfy

\[
\left|
 \sum_q q\sum_{k\ne0}\mathcal C_x(qk)
 -R\sum_{h\ne0}\mathcal C_x(h)
\right|
\ll L_{\rm pr}x^{399/400-\varepsilon_0},
\tag{3.2}
\]

whose exponent ceiling is

\[
\frac23+\frac{399}{400}=\frac{1997}{1200}.
\tag{3.3}
\]

Under the elementary \(x^{1+o(1)}\) per-shift divisor envelope, full
square-root cancellation over the \(H\)-family has unnormalized exponent

\[
1+\frac13+\frac{21}{64}=\frac{319}{192}.
\tag{3.4}
\]

After division by \(L_{\rm pr}\), this is

\[
x^{191/192+o(1)}=x^{1-1/192+o(1)}.
\tag{3.5}
\]

The exact positive margin over the required endpoint is

\[
\frac{399}{400}-\frac{191}{192}=\frac{13}{4800}>0.
\tag{3.6}
\]

Equations (3.2)--(3.6) are a design ledger.  They do not assert the
square-root theorem.

The direct Jutila energy formulation has the same margin requirement:

\[
\|1-\chi_{\rm pr}\|_2\ll x^{-1/192+o(1)},\qquad
\|G_x\|_2\le x^{1+\theta+o(1)},\quad
\theta<\frac{13}{4800}.
\tag{3.7}
\]

The factorable auxiliary gives the wider conditional requirement
\(\theta<193/2800\), but no current theorem supplies the physical norm.

## 4. Primary-source screen and its precise stop

The reviewed corpus contains useful engines but no direct attachment:

1. Blomer--Li Lemma 1 supplies the Jutila approximant and true Ramanujan
   coefficients, not \(\|(1-\chi)G_x\|_2\).
2. Blomer--Li's final estimates use GL(3) Hecke and divisor/two-smooth
   coefficients, the corresponding Voronoi transforms and a different
   source clock.
3. Deshouillers--Iwaniec/Kuznetsov and Drappeau's spectral theorem require
   modulus-independent smooth arrays and their own gcd domains.
4. Drappeau Theorem 5.1 averages all dyadic moduli with fixed product
   congruence and modulus-independent divisor-bounded sequences.  Inverting
   the literal moving equation makes the TPC coefficients modulus-dependent.
5. Blomer--Pascadi and Pascadi remain fixed-modulus short-cell engines after
   a legal compiler; they do not provide the compiler, axes or outer norm.
6. Bettin--Chandee estimates one determinant species described below, not
   the ordered mixed J1/J2/hybrid family.

Accordingly,

~~~text
V26_DECLARED_DI_KUZNETSOV_DISPERSION_SHIFTED_CONVOLUTION_
JUTILA_BP_PASCADI_PRIMARY_CORPUS_DIRECT_ATTACHMENT_V1
  = STOP_SCOPED_NO_LITERAL_COLLECTIVE_PHYSICAL_SCALAR_THEOREM.
~~~

This stop covers only the stated sources and versions as black-box direct
attachments.  It does not stop a new compensated covariance theorem, a new
coefficient-native compiler, later source versions, A1/A2, the O161 parents,
pair-native/H1, the dynamical block road or the global architecture.

## 5. A real factorable local engine and short-dual skeleton

For a smooth J1-by-J1 cell, write the literal determinant

\[
RS-EF=2,
\tag{5.1}
\]

where \(E,R\le\sqrt x\), \(F\asymp x/E\), and
\(S\asymp x/R\).  The ordered coefficients retain the \(+2\)
coefficient on each J1 row (hence their literal product \(+4\)),
\(\mu(E)\mu(R)\), \(\log F\log S\), and the physical normalization.

Bettin--Chandee Corollary 1 attaches to a smooth determinant cell under

~~~text
m1=S, n2=R, m2=F, n1=E, Delta=2.
~~~

The source balance ratio is \(O(1)\), since both cross-products have size
\(x\).  If the two smooth cutoffs satisfy the Corollary's derivative
condition with \(\eta=x^{o(1)}\), and the literal outer sequences obey their
natural divisor-envelope bounds
\(\|\alpha\|_2\le E^{1/2}x^{o(1)}\) and
\(\|\beta\|_2\le R^{1/2}x^{o(1)}\), then, for \(E=x^e\),
\(R=x^r\), the source error exponent is

\[
\frac{17}{20}(e+r)+\frac14\max(e,r)+o(1)
\le\frac{39}{40}+o(1).
\tag{5.2}
\]

This has gross margin \(9/400\) over \(399/400\), but it is an error term
before the source main integral, hard-shell Mellin/variation losses and
signed J1/J2/hybrid reassembly.  Hence its status is conditional-local only.

The same cell has a common-factorable exact Poisson skeleton.  Rename
\(M:=E\), write \(N\) for the smooth variable represented by the earlier
\(F\), and write \(F_0\asymp x/M\) for its dyadic scale.  For
\((MR,q)=1\), with
\(\widehat U(\xi)=\int U(v)e(-\xi v)\,dv\), set

\[
\begin{aligned}
\mathcal T={}&\sum_{a\bmod q}^{*}e(-2(a/q+z))
 \sum_N U(N/F_0)e(-(a/q+z)MN)\\
&\qquad\qquad\times
 \sum_S V(S/S_0)e((a/q+z)RS).
\end{aligned}
\tag{5.3}
\]

Two one-dimensional Poisson transformations give exactly

\[
\begin{aligned}
\mathcal T={}&F_0S_0e(-2z)
\sum_{\substack{K,H\\(KH,q)=1\\KR+HM\equiv0\pmod q}}
 e_q(-2KM^{-1})\\
&\quad\times
 \widehat U(F_0(K/q+zM))
 \widehat V(S_0(H/q-zR)),
\end{aligned}
\tag{5.4}
\]

Here the Poisson indices satisfy \(K\equiv aM\pmod q\) and
\(H\equiv-aR\pmod q\); this is exactly why the displayed congruence and
phase occur.  Formula (5.4) is restricted to the coprime nonzero rows;
the zero and nonunit axes are retained outside this display.  At
\(q=x^{4/7}\),

\[
|K|\ll qM/x\le x^{1/14},\qquad
|H|\ll qR/x\le x^{1/14},
\tag{5.5}
\]

and \(KR+HM=\ell q\) has only \(O(1)\) effective copies.  For every fixed
\(\varepsilon>0\), on \(|z|\le x^{-1}\), if
\(M\le x^{3/7-\varepsilon}\) (respectively
\(R\le x^{3/7-\varepsilon}\)), the corresponding nonzero \(K\)-row
(respectively \(H\)-row) is \(O_{A,\varepsilon}(x^{-A})\) for every fixed
\(A\), by Schwartz decay.  The transition range
\(M,R=x^{3/7-o(1)}\) is not covered by that statement.  This is a genuine
exact \(L0\) short-dual skeleton, not a whole-object estimate.

## 6. Why the whole factorable compiler still fails

The common ensemble need not be changed atom by atom.  Within the same
\(\omega(q)=\sum_{pt=q}\rho(t/Q_2)\), one may partition each fixed
template into \(p\)-good and \(p\)-bad incidences.  A fixed nonzero slope
has only \(O(1)\) prime divisors in the \(p\)-shell, so this partition is
exact and sparse per fixed label.  Its analytic bad-row cost remains open.

The first whole-object fatal is the ordered J2 transform species.  A J2 row
has two smooth slots.  If \(E=e_1e_2\) and \(F_1F_2\asymp x/E\), the
double-Poisson dual area is

\[
\frac q{F_1}\frac q{F_2}
=\frac{q^2}{F_1F_2}=x^{1/7}E,
\tag{6.1}
\]

not the J1 support or normalization.  Active rows exist with both smooth
slots shorter than \(\sqrt x\); they cannot be declared negligible or
collapsed to a scalar divisor coefficient before the ordered MASTER route.

The hybrid branch is a second independent mismatch.  Its congruence lives
on an \({\rm lcm}(q,d_{\rm rough})\) progression, its sieve variable is not
uniformly \(\le\sqrt x\), and its main term must cancel against the prime
channel under the original signs and normalization.

The first falsifier is tied to the V19 ordered physical routing, not to a
synthetic matrix.  At analytic \(x=100\), take rough rows
\((e_1,e_2)=(2,3),(2,2)\), smooth columns
\((f_1,f_2)=(16,1),(2,7)\), and preserve the V19 slot order
\((e_1,e_2,f_1,f_2)\).  The product and route tables are

\[
\begin{pmatrix}96&84\\64&56\end{pmatrix},
\qquad
\begin{pmatrix}{\rm MASTER}&{\rm MASTER}\\{\rm H2}&{\rm MASTER}\end{pmatrix}.
\tag{6.2}
\]

Here the route is recomputed from the V19 rule: choose the first source-order
slot with \(u_i^2\ge T\); a large smooth slot is H2 exactly when its complement
\(D\) satisfies \(D^{400}\le100^{133}\); otherwise use the first increasing
proper active-slot bitmask with \(M^{400}\ge T^{133}\) and \(M^2\le T\).
Thus the MASTER indicator has determinant one.  Finite exact falsifiers
retained by the checker are:

~~~text
x=100 four-cell MASTER selector has a nonzero 2x2 minor;
x=100,t=54 contains an active degenerate J2 row with f1=f2=3;
q=5 constant double-Poisson cell has periodic DFT support only at (0,0),
    where the zero-axis Ramanujan mass is 4;
q=6,A=2 has 8 solutions but only 2 unit solutions;
~~~

Thus

~~~text
V26_J1xJ1_SMOOTH_DETERMINANT_CELL
  = SOURCE_BACKED_CONDITIONAL_LOCAL_ENGINE_ERROR_39_OVER_40_BEFORE_MAIN_REASSEMBLY
V26_COMMON_FACTORABLE_J1_SHORT_DUAL_DETERMINANT
  = PROVED_EXACT_L0_COPRIME_SMOOTH_CELL
V26_COMMON_ENSEMBLE_GOOD_BAD_p_INCIDENCE
  = PROVED_EXACT_L0_ANALYTIC_COST_OPEN
V26_SINGLE_TEMPLATE_MASTER_FACTORIZATION
  = STOP_SCOPED_FINITE_2X2_MINOR
V26_ALL_HB2_TYPES_ONE_COMMON_SOURCE_ARRAY
  = STOP_SCOPED_J2_DEGENERATE_AXIS_AND_NORMALIZATION_MISMATCH
V26_HYBRID_TO_SAME_ARRAYS
  = STOP_SCOPED_PROGRESS_MODULUS_MAIN_REASSEMBLY_MISMATCH
V26_FACTORIZABLE_LITERAL_TRANSFORM_COMPILER
  = STOP_SCOPED_PARTIAL_J1_ONLY_NO_WHOLE_OBJECT
V26_MIXED_HB_DETERMINANT_COMPILER
  = OPEN_NEW_THEOREM_RANK1.
~~~

## 7. The dynamical route: single events stop, shell blocks survive

Use the V23 predeclared schedule

\[
x_n=\text{least safe even integer in }[8^n,2\cdot8^n].
\tag{7.1}
\]

For one moving gap-two event,

\[
\mu(E_{x_n})\asymp\frac1{(\log x_n)^2}\asymp\frac1{n^2},
\qquad
\sum_n\mu(E_{x_n})<\infty.
\tag{7.2}
\]

Therefore a dynamical Borel--Cantelli theorem applied only once per selected
endpoint cannot prove infinitude.  The correct object is the entire shell

\[
I_n=(x_n/2,x_n],\qquad
\mathcal B_n(y)=\sum_{t\in I_n}\mathbf1_{E_t}(T^t y).
\tag{7.3}
\]

The existing metric estimates give

\[
\mathbb E_\mu\mathcal B_n\asymp\frac{x_n}{(\log x_n)^2},
\qquad
\operatorname{Var}_\mu(\mathcal B_n)=O(x_n).
\tag{7.4}
\]

Chebyshev then gives

\[
\mu(\mathcal B_n=0)
\ll\frac{(\log x_n)^4}{x_n},
\qquad
\sum_n\mu(\mathcal B_n=0)<\infty.
\tag{7.5}
\]

This proves eventual positive block counts for Haar-a.e. phase.  It does not
select the arithmetic seed \(0\), where the event identity is already the
twin-prime endpoint.

## 8. What the Logistic source really advances

Aspenberg--Baladi--Persson, arXiv:2212.12202v2, Theorem 1.1, treats the
quadratic Logistic family \(T_a(y)=ay(1-y)\) at the distinguished critical
seed \(y=1/2\).  Near a transversal mixing Misiurewicz parameter \(a_*\) it
gives a positive-measure set \(\Omega_*\) of mixing Collet--Eckmann
parameters.  For a fixed Hölder observable \(\varphi\) with
\(\sigma_{a_*}(\varphi)\ne0\), there is an \(\varepsilon_\varphi>0\) such
that, on normalized Lebesgue measure over
\(\Omega_*\cap[a_*-\varepsilon_\varphi,a_*+\varepsilon_\varphi]\), the
parameter functions
\[
\xi_n(a)=
\frac{\varphi(T_a^{n+1}(1/2))-\int\varphi\,d\mu_a}
     {\sigma_a(\varphi)}
\tag{8.1}
\]
satisfy an ASIP with every error exponent \(\gamma>2/5\).
Here \(\sigma_a(\varphi)\) is the source's parameter-dependent asymptotic
standard deviation.  This is an almost-everywhere parameter-space statement,
not a theorem for a preassigned fixed parameter.

This invalidates the blanket statement that a distinguished critical seed
can never be parameter-typical.  It does not provide:

~~~text
an exact map from the TPC arithmetic seed 0 to that critical section;
the same return locus for the arithmetic carrier and parameter ASIP;
the growing triangular family of literal physical observables;
uniform Hölder/BV norms and constants across n;
the positive physical block mean and exactly-once output.
~~~

Haydn--Nicol--Török--Vaienti and Korepanov supply strong sequential or fixed-
observable metric theorems on their own probability spaces.  They do not
close the same arithmetic section and triangular-carrier contract.

The strongest honest dynamics target is therefore

~~~text
V26_SAFE_LACUNARY_CRITICAL_SECTION_BLOCK_TRANSFER_THEOREM
  = OPEN_NEW_THEOREM.
~~~

It must give one fixed parameter, an exact stage-preserving physical event
intertwiner, the actual growing observable/norm ledger, uniform block first
and second moments or summable pointed bad sets, and the actual positive
twin count or a fully reassembled power-saving physical scalar.

For Hénon, the same target remains legal only after an exact natural-section
diagram preserves stage, event, measure, seed and physical functional.

## 9. Highway decision and claim boundary

The selected route order after V26 is:

~~~text
ANALYTIC PRIMARY:
  V26_PRIME_SHELL_RAMANUJAN_COMPENSATED_DILATION_COVARIANCE
  supported by the rank-1 J1 short-dual determinant skeleton.

DYNAMICAL PRIMARY RESERVE:
  V26_SAFE_LACUNARY_CRITICAL_SECTION_BLOCK_TRANSFER_THEOREM,
  using whole-shell block counts, not single lacunary events.

ANALYTIC SECONDARY CONSTRUCTION:
  V26_MIXED_HB_DETERMINANT_COMPILER,
  which must unify J1, ordered J2, hybrid, axes, bad incidences and mains.
~~~

The reviewed primary corpus has no theorem for the first object.  The second
has a genuine critical-seed ASIP source interface but no exact physical
carrier.  The third has one source-backed local species but no whole-family
compiler.  Hence

~~~text
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false.
~~~

The two O161 parents, pair-native route, H1, A1/A2 and global architecture
remain open and independent.  No V1/common-k/tail-failure/A/B/full-ultra
STOP cell is reopened.

## 10. Source locks

Primary source interfaces used in this note are:

1. Ford--Maynard, Lemma 5.2, for the literal ordered HB2 rows;
2. Blomer--Li, arXiv:2511.03294v1, Lemma 1 and the factorable source shape;
3. Blomer--Pascadi, arXiv:2607.24311v1, Theorems 1.1 and 5.5;
4. Pascadi, arXiv:2404.04239v3, Proposition 10;
5. Drappeau, arXiv:1504.05549v4, Theorems 2.1 and 5.1;
6. Bettin--Chandee, arXiv:1502.00769v1, Corollary 1;
7. Aspenberg--Baladi--Persson, arXiv:2212.12202v2, Theorem 1.1;
8. Haydn--Nicol--Török--Vaienti, arXiv:1406.4266, Theorems 3.1 and 4.1;
9. Korepanov, arXiv:1703.09176, the fixed-observable ASIP interface.

The finite MASTER/H2 routing certificates additionally lock the repository
V19 proof and checker; they are derived finite provenance, not a new external
source theorem.

Only the stated theorem bodies and quantifiers are source-backed.  The
prime-dilation identity, rational endpoint ledger, common-incidence split,
short-dual algebra and block Chebyshev reduction are repository/audit-derived
exact or elementary statements.  The collective cancellations and physical
carrier are not source-backed.

## 11. Maximum supported claim

~~~text
EXACT_L0_COMPENSATED_PRIME_DILATION_AND_FACTORIZABLE_J1_SHORT_DUAL_NORMAL_FORMS_PLUS_SOURCE_BACKED_CRITICAL_SEED_ASIP_INTERFACE_AND_WHOLE_SHELL_BLOCK_RETYPE
~~~

This maximum claim is intentionally below an arithmetic theorem, below a
physical \(L2\) estimate, and below any TPC-207 release trigger.
