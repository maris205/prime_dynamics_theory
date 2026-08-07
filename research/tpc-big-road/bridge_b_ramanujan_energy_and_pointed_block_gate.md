# Bridge B V27: Ramanujan energy, zero-axis main, and pointed block gates

Date: 2026-08-08

Status:

~~~text
EXACT_L0_RAMANUJAN_HILBERT_GATE_AND_PARAMETER_AVERAGING_FIREWALL
MAXIMUM_CLAIM = EXACT_PRIME_SHELL_WEIGHT_ENERGY_AND_ENDPOINT_REDUCTION_PLUS_SOURCE_CORPUS_STOPS_AND_POINTED_WHOLE_SHELL_ROUTE
ROUTE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
~~~

This note does not add another fixed Kloosterman cell.  It identifies the
single Hilbert-space estimate that would pay the V26 compensated prime
dilation, exposes the diagonal value that prevents a free smooth-main
argument, and separates the only honest dynamical reserve from parameter
averaging that cannot select the arithmetic seed.

The outcome is a theorem contract and a route decision.  No arithmetic
power saving is proved.

## 1. Frozen physical scalar

Keep the V19/V25/V26 objects literally:

\[
h_0=2,\qquad x=2X,\qquad I_x=(x/2,x]\cap\mathbb Z,
\tag{1.1}
\]

\[
w_x^{(z)}(u)=\Lambda(u+2)-b_x^{(z)}(u),
\qquad z=(\log x)^K,
\tag{1.2}
\]

and the ordered raw coefficient \(\beta_x^{\rm raw}\), including its
literal \(+2,-1\) HB2 channel coefficients, source-order slots, occurrence
multiplicity, MASTER/H2 routing, Mobius/log factors and \(1/\log T_o\)
normalization.

For \(h\ne0\), put

\[
r_x(h)=
\sum_{\substack{t,t+h\in I_x}}
 \beta_x^{\rm raw}(t)w_x^{(z)}(t+h).
\tag{1.3}
\]

The variable \(h\) in (1.3) is a correlation shift.  It is not the fixed
physical gap \(h_0=2\), which already occurs inside (1.2).

Use the V23 prime shell

\[
Q=x^{1/3},\qquad H=\delta^{-1}=x^{21/32},
\qquad
\mathcal Q=\{q\ {\rm prime}:Q<q\le2Q\},
\tag{1.4}
\]

\[
R=\#\mathcal Q,\qquad
L_{\rm pr}=\sum_{q\in\mathcal Q}(q-1).
\tag{1.5}
\]

With the V25 convention

\[
\widehat\psi_+(\xi)=\int_{\mathbb R}\psi(v)e(\xi v)\,dv,
\tag{1.6}
\]

the exact V26 error is

\[
\boxed{
E_x=-\frac1{L_{\rm pr}}
 \sum_{h\ne0}\widehat\psi_+(h/H)A_Q(h)r_x(h),
}
\tag{1.7}
\]

where

\[
A_Q(h)=\sum_{q\in\mathcal Q}c_q(h)
=-R+\sum_{\substack{q\in\mathcal Q\\q\mid h}}q.
\tag{1.8}
\]

Formula (1.7) is exact \(L0\).  It retains one outer signed ensemble and all
physical coefficients.  It does not bound \(E_x\), and it does not pay the
separate V23 Jutila-main compiler.

## 2. Exact finite energy of the prime-shell weight

Let \(N<Q_{\min}^{(2)}\), where

\[
Q_{\min}^{(2)}=\min_{q<q'\in\mathcal Q}qq'.
\tag{2.1}
\]

Then every nonzero \(|h|\le N\) is divisible by at most one prime in
\(\mathcal Q\).  Hence the hard-window identity is

\[
\boxed{
\sum_{0<|h|\le N}|A_Q(h)|^2
=2\left[
 NR^2+\sum_{q\in\mathcal Q}
 \left\lfloor\frac Nq\right\rfloor(q^2-2qR)
\right].
}
\tag{2.2}
\]

This hypothesis is substantive.  Once \(N\) reaches a product \(qq'\), the
cross term \(2qq'\) occurs and (2.2) is false.

For the literal Schwartz multiplier, define

\[
W(v)=|\widehat\psi_+(v)|,
\qquad
\mathcal N_A^2=
\sum_{0<|h|<x/2}W(h/H)|A_Q(h)|^2.
\tag{2.3}
\]

The multiplier is never declared to have hard support.  For an all-integer
nonnegative weight, the exact expansion before physical truncation is

\[
\begin{aligned}
\sum_{h\ne0}W(h/H)A_Q(h)^2
={}&R^2\sum_{h\ne0}W(h/H)\\
&+\sum_q(q^2-2Rq)\sum_{k\ne0}W(qk/H)\\
&+2\sum_{q<q'}qq'\sum_{k\ne0}W(qq'k/H).
\end{aligned}
\tag{2.4}
\]

Here \(W\) is continuous, integrable, rapidly decreasing and of bounded
variation; indeed
\(\operatorname{Var}(|\widehat\psi_+|)
\le\int_{\mathbb R}|\widehat\psi_+'(v)|\,dv\), while
\(\widehat\psi_+(0)=\int\psi=1\) makes \(\int W>0\).
Since \(Q_{\min}^{(2)}/H=x^{1/96+o(1)}\), the region containing two shell
prime divisors is a Schwartz tail.  Splitting before that region, using
(2.2), and applying Riemann sums gives

\[
\mathcal N_A^2
=H\left(\int_{\mathbb R}W(v)\,dv\right)
 \left(\sum_{q\in\mathcal Q}q-R^2\right)(1+o(1))
=x^{127/96+o(1)}.
\tag{2.5}
\]

Here \(127/96=21/32+2/3\) is the exponent of the squared norm.  Equivalently,

\[
\mathcal N_A=x^{127/192+o(1)},
\qquad
\frac{\mathcal N_A}{L_{\rm pr}}
=x^{-1/192+o(1)}.
\tag{2.6}
\]

The outer physical cutoff also costs only a Schwartz tail because
\((x/2)/H=x^{11/32}/2\).  Thus (2.5) applies to the physically truncated
norm (2.3), not merely to the all-integer auxiliary sum.
All constants in the tail estimate are fixed Schwartz seminorms of the
predeclared \(\psi\).  A future proof may not replace (2.3) by
\(|h|\le H\) without paying the tail.  In particular, for two distinct
shell primes the omitted contribution contains

\[
2qq'W(qq'/H)>0
\tag{2.7}
\]

whenever the multiplier is nonzero there.

Thus

~~~text
V27_PRIME_SHELL_HARD_WINDOW_RAMANUJAN_L2_IDENTITY
  = PROVED_EXACT_L0_FOR_N_LT_FIRST_DISTINCT_PRIME_PRODUCT.
V27_PRIME_SHELL_RAMANUJAN_WEIGHTED_ENERGY
  = PROVED_EXACT_FINITE_PLUS_SCHWARTZ_ASYMPTOTIC.
V27_EFFECTIVE_HORIZON_AS_HARD_SUPPORT
  = STOP_SCOPED_FALSE_SCHWARTZ_TAIL_AND_DOUBLE_DIVISOR_CROSS_TERMS.
~~~

This is a norm theorem for a deterministic multiplier, not arithmetic
\(L2\) credit.

## 3. The exact Hilbert gate and the strict endpoint

The single occurrence of \(\widehat\psi_+\) in (1.7) must not be counted
twice.  Write its phase into either factor and split only its absolute value:

\[
\mathcal N_r^2=
\sum_{0<|h|<x/2}W(h/H)|r_x(h)|^2.
\tag{3.1}
\]

Weighted Cauchy gives the exact legal inequality

\[
|E_x|\le
\frac{\mathcal N_A}{L_{\rm pr}}\mathcal N_r.
\tag{3.2}
\]

It follows from (2.6) that a theorem of the form

\[
\boxed{
\mathcal N_r\ll_{K,\psi,\varepsilon}
x^{1+\theta+\varepsilon}
\quad\hbox{for one fixed}\quad
\theta<\frac{13}{4800}
}
\tag{3.3}
\]

would give

\[
E_x\ll x^{191/192+\theta+\varepsilon}.
\tag{3.4}
\]

The exact endpoint calculation is

\[
1-\frac1{192}=\frac{191}{192},
\qquad
\frac{399}{400}-\frac{191}{192}=\frac{13}{4800}.
\tag{3.5}
\]

Equality in (3.3) is insufficient for a strict power margin.  A fixed gap
below \(13/4800\), together with all physical losses, is required.

The selected analytic theorem target is therefore

~~~text
V27_ONE_PSI_WEIGHTED_CAUCHY_INTERFACE
  = PROVED_EXACT_ABS_PSI_HALF_WEIGHT_ON_BOTH_FACTORS.
V27_LITERAL_PRIME_SHELL_RAMANUJAN_VECTOR_COVARIANCE
  = SELECTED_OPEN_NEW_THEOREM.
~~~

Its input is the complete literal (1.1)--(1.8), both signs of \(h\), the
actual shifted shell intersection, the prime-only ensemble, nonunit and
divisibility incidences, and the Schwartz tail.  The estimate must be
uniform in the legal order of \(K,\theta,\varepsilon,x_0\).  No good-shift,
good-modulus or density-one selection can replace (3.3).

## 4. The zero-axis obstruction to a free smooth main

The usual slogan that a zero-mean Ramanujan weight kills every smooth main
is false after the physical zero shift is removed.

For a Schwartz function \(F\), with

\[
\widehat F(\xi)=\int_{\mathbb R}F(v)e(-\xi v)\,dv,
\tag{4.1}
\]

Poisson summation gives the exact identity

\[
\begin{aligned}
\sum_{h\ne0}A_Q(h)F(h/H)
={}&-L_{\rm pr}F(0)\\
&+H\sum_{q\in\mathcal Q}\sum_{\ell\ne0}
 \left[\widehat F(\ell H/q)-\widehat F(\ell H)\right].
\end{aligned}
\tag{4.2}
\]

For every integer \(s\ge2\), the second line is at most

\[
\frac{2\zeta(s)}{(2\pi)^s}
\|F^{(s)}\|_1 H^{1-s}
\left(\sum_{q\in\mathcal Q}q^s+R\right).
\tag{4.3}
\]

After division by \(L_{\rm pr}\), this is
\(O_s(\|F^{(s)}\|_1(Q/H)^{s-1})\).  But the first line of (4.2) is
\(-F(0)\), with no power saving.

The finite complete-period version is already decisive.  For
\(\mathcal Q=\{11,13\}\) and period \(143\),

\[
\sum_{h=0}^{142}A_Q(h)=0,
\qquad
\sum_{h=1}^{142}A_Q(h)=-22=-L_{\rm pr}.
\tag{4.4}
\]

Therefore a local-main decomposition

\[
r_x(h)=M_x(h)+e_x(h)
\tag{4.5}
\]

is useful only if it supplies both:

1. the residual energy bound (3.3) for \(e_x\); and
2. a separate bound for the Ramanujan pairing of \(M_x\), including its
   diagonal value and hard-shell endpoints.

If a uniformly smooth scaled extension of \(M_x\) has value zero at the
origin, (4.2)--(4.3) can give a power saving.  Merely changing the single
lattice value \(M_x(0)\) to zero does not produce such an extension: its
derivative seminorms or a discrete boundary term must then be paid.

Hence

~~~text
V27_FULL_LATTICE_SMOOTH_MAIN_POISSON_IDENTITY
  = PROVED_EXACT_DETERMINISTIC_INTERFACE.
V27_AUTOMATIC_SMOOTH_LOCAL_MAIN_ANNIHILATION_AFTER_CORRELATION_ZERO_SHIFT_DELETION
  = STOP_SCOPED_ZERO_AXIS_MINUS_F_OF_ZERO.

V27_SIGNED_LOCAL_MAIN_ZERO_AXIS_AND_RESIDUAL_REASSEMBLY
  = OPEN_NEW_THEOREM.
~~~

The deleted coordinate in the first status token is the correlation zero
shift; it is not the fixed physical gap \(h_0=2\).

## 5. Why current long-shift theorems do not pay (3.3)

The closest primary-source families were checked at their literal inputs.

### 5.1 MRT long-shift correlations

Matomaki--Radziwill--Tao, arXiv:1707.01315v3, Theorem 1.3, covers almost all
shifts once \(H\ge x^{8/33+\varepsilon}\), so the V27 scale
\(H=x^{21/32}\) is inside its range.  But the theorem treats full
\(\Lambda\) and \(d_k\) correlations with pointwise error
\(x\log^{-A}x\).  Its proof-level energy has scale

\[
\|r-M\|_2\ll x\sqrt H\log^{-A}x=x^{85/64}\log^{-A}x.
\tag{5.1}
\]

Pairing (5.1) with (2.5) at the numerator level gives exponent

\[
\frac{85}{64}+\frac{127}{192}=\frac{191}{96},
\tag{5.2}
\]

whereas the numerator ceiling is

\[
\frac23+\frac{399}{400}=\frac{1997}{1200}.
\tag{5.3}
\]

The exact deficit is

\[
\frac{191}{96}-\frac{1997}{1200}=\frac{781}{2400}.
\tag{5.4}
\]

No fixed logarithmic saving pays this power gap.  Moreover the source's
full-Lambda Type \(d_1,\ldots,d_4\)/II decomposition does not preserve the
V19 ordered occurrences, MASTER selector, hybrid species or one signed
prime-shell outer sum.

### 5.2 Higher Uniformity I and II

Matomaki--Shao--Tao--Teravainen, arXiv:2204.03754, and
Matomaki--Radziwill--Shao--Tao--Teravainen, arXiv:2411.05770v2, give genuine local Fourier,
nilsequence and progression control for \(\Lambda-\Lambda^\sharp\).  The
all-interval threshold \(5/8\) is below \(21/32\) by exactly \(1/32\).

This is a source-backed local logarithmic input, not (3.3).  Expanding
\(A_Q\) into all rational phases and then using triangle with the outer
\(\beta_x^{\rm raw}\) has power scale

\[
x\,H\,L_{\rm pr}=x^{223/96+o(1)}.
\tag{5.5}
\]

The missing operation is a collective rational-frequency square function
before supremum or triangle.

There is also no equality between the source approximant

\[
\Lambda^\sharp(n)=
\frac{P(R_0)}{\varphi(P(R_0))}
1_{(n,P(R_0))=1},
\qquad R_0=\exp((\log x)^{1/10}),
\tag{5.6}
\]

and the physical \(b_x^{(z)}\), which contains the distinct cutoff
\(z=(\log x)^K\), the rough-divisor tensor, \(C_z\), and simultaneous
dependence on \(u\) and \(u+2\).

### 5.3 Arbitrary-shift-weight architecture

Leung, arXiv:2210.13081v2, Theorems 1.1--1.2, is a genuine arbitrary
shift-weight and factorable-shift architecture for GL(3) x GL(2)
coefficients.  It is not a physical attachment.  Even before the coefficient
mismatch, its relevant raw exponent here is

\[
\frac34+\frac{21}{64}+\frac{127}{192}
=\frac{167}{96},
\tag{5.7}
\]

which exceeds (5.3) by \(181/2400\).

The remaining DI/Kuznetsov, Drappeau, Bettin--Chandee,
Blomer--Pascadi and Pascadi sources retain the V26 verdict: they are
post-compiler local engines or different coefficient families, not a
theorem for (1.7).

The source atlas is therefore

~~~text
V27_MRSTT_ALL_INTERVAL_LAMBDA_MINUS_LAMBDASHARP_LINEAR_PHASE
  = SOURCE_BACKED_LOCAL_LOG_INPUT
V27_MRSTT_LAMBDASHARP_TO_TENSOR_LOCAL_BZ_TRANSFER
  = OPEN_NEW_COMPARISON_THEOREM
V27_MRT_MRSTT_TO_LITERAL_PRIME_RAMANUJAN_WEIGHTED_NUMERATOR
  = STOP_SCOPED_NO_COLLECTIVE_POWER_NORM
V27_LEUNG_ARBITRARY_WEIGHTED_SHIFT_ARCHITECTURE
  = SOURCE_BACKED_AUTOMORPHIC_ANALOGUE_ONLY
V27_EXISTING_SHIFTED_CONVOLUTION_SPECTRAL_CORPUS_DIRECT_ATTACHMENT
  = STOP_SCOPED_NO_LITERAL_WHOLE_PHYSICAL_SCALAR
~~~

These are versioned corpus stops, not literature nonexistence claims.

## 6. The mixed-HB theorem remains a typed direct sum

V26 supplied one source-backed J1-by-J1 local error and exact finite
falsifiers against a rank-one MASTER selector.  The correct whole-object
repair is not a common scalar array.  It is a tagged direct sum retaining at
least:

~~~text
J1/J2 source species and ordered slots;
original occurrence mask and MASTER/H2 route;
literal +2,-1 coefficient and 1/log(T_o);
prime versus hybrid determinant channel;
q versus lcm(q,d_rough) modulus species;
zero/nonunit axis and gcd signature;
good/bad auxiliary-prime incidence;
source main, source error and outer provenance.
~~~

Before any species-wise absolute value, a new theorem must prove the exact
signed-main identity

\[
\sum_\sigma\varepsilon_\sigma M_\sigma
=M_{\rm physical}
\tag{6.1}
\]

and then pay (or cancel) the zero-axis term exposed in Section 4.  MRT or
Higher Uniformity cannot be used to erase these type tags.

Thus

~~~text
V27_MIXED_HB2_ONE_COMMON_SOURCE_ARRAY
  = STOP_SCOPED_FINITE_SELECTOR_MINOR_ONE
V27_TAGGED_VECTOR_MIXED_HB2_DETERMINANT_REASSEMBLY
  = OPEN_NEW_THEOREM
~~~

The analytic route order is now:

1. literal Ramanujan vector covariance (3.3);
2. signed local-main/zero-axis reassembly;
3. tagged mixed-HB determinant compiler as the main construction reserve.

## 7. Dynamical parameter averaging: the exact dichotomy

V26 correctly replaced one lacunary event by the whole-shell block

\[
\mathcal B_j(y)=
\sum_{x_j/2<t\le x_j}1_{E_t}(T^t y).
\tag{7.1}
\]

The existing Haar estimates

\[
\mathbb E\mathcal B_j\asymp\frac{x_j}{\log^2x_j},
\qquad
\operatorname{Var}\mathcal B_j=O(x_j)
\tag{7.2}
\]

give summable bad mass \(O(\log^4x_j/x_j)\).  This is a valid metric
whole-shell theorem, but it does not select the arithmetic seed.

Suppose a parameter set \(C\) with \(0<\nu(C)<\infty\) and a critical-orbit
block \(S_j(a)\) are proposed as the repair.  Write
\(\nu_C(A)=\nu(A\cap C)/\nu(C)\).  The two candidate designs audited here
are as follows.

**Same-output carrier.**  If exact physical intertwining gives

\[
S_j(a)=B_j^{\rm arith}
\qquad\hbox{for every }a\in C,
\tag{7.3}
\]

then the normalized conditional parameter mean is already

\[
\int_C S_j(a)\,d\nu_C(a)=B_j^{\rm arith},
\qquad
\operatorname{Var}_{\nu_C}(S_j)=0.
\tag{7.4}
\]

A positive normalized conditional parameter mean in this setting is exactly the desired arithmetic
positivity, not an independent consequence of mixing.

**Null-graph carrier.**  If exact intertwining holds only at one parameter
or on the fiber that maps to arithmetic phase \(0\), that set has measure
zero under any nonatomic parameter law pushing forward to Haar measure.
An almost-everywhere ASIP, DBC or variance theorem cannot certify it.

Stagewise transversality does not create a common parameter.  For
\(T_a(y)=ay(1-y)\) and critical seed \(1/2\),

\[
x_1(a)=a/4,\qquad x_2(a)=a^2(4-a)/16.
\tag{7.5}
\]

The equation \(x_1(a)=3/4\) selects \(a=3\), whereas
\(x_2(a)=49/128\) has the transverse solution \(a=7/2\); at \(a=3\)
the second residual is \(23/128\).  Separate good parameters at successive
stages do not yield one physical orbit.

Aspenberg--Baladi--Persson remains a genuine source interface for the
critical seed \(1/2\), but only for one fixed Holder observable on an
almost-everywhere parameter space.  It does not change the dichotomy above.

Consequently,

~~~text
V27_PARAMETER_AVERAGED_EXACT_SAME_ARITHMETIC_OUTPUT_CARRIER
  = STOP_SCOPED_TAUTOLOGICAL_MEAN_OR_NULL_GRAPH
V27_STAGEWISE_TRANSVERSE_PARAMETER_RESELECTION
  = STOP_SCOPED_NO_COMMON_PARAMETER
V27_POINTED_CRITICAL_SECTION_WHOLE_SHELL_DISCREPANCY
  = OPEN_NEW_THEOREM_AFTER_EXACT_SINGLE_PARAMETER_FACTOR
V27_HENON_POINTED_WHOLE_SHELL_SECTION_TRANSFER
  = OPEN_ONLY_AFTER_EXACT_NATURAL_SECTION_DIAGRAM
~~~

The surviving dynamics theorem must be pointed at one explicitly named
parameter/section and prove, for the actual growing block family,

\[
|S_j(a^\dagger)-M_j(a^\dagger)|
=o\!\left(\frac{x_j}{\log^2x_j}\right),
\qquad
M_j(a^\dagger)\gg\frac{x_j}{\log^2x_j},
\tag{7.6}
\]

with an exact stage/time/event/measure/normalization diagram.  This is harder
than parameter averaging, but it is noncircular and targets the required
seed.

## 8. Route decision and complete loss ledger

The post-V27 route order is:

~~~text
ANALYTIC PRIMARY:
  literal prime-shell Ramanujan vector covariance
  + signed local-main zero-axis reassembly.

ANALYTIC CONSTRUCTION RESERVE:
  tagged vector mixed-HB2 determinant theorem.

DYNAMICAL POINTED RESERVE:
  exact single-parameter factor
  + pointed critical-section whole-shell discrepancy.
~~~

The unpaid ledger is:

~~~text
literal residual weighted ell2 theorem                 UNPAID
strict theta gap below 13/4800                         UNPAID
local main and zero-axis signed reassembly              UNPAID
Schwartz and hard-shell endpoint tails                  UNPAID
ordered J1/J2/hybrid species aggregation                UNPAID
zero/nonunit axes and bad-incidence norms               UNPAID
Jutila main compiler and one-outer-absolute reassembly  UNPAID
all-D uniformity and exactly-once physical cover        UNPAID
original/global normalization                           UNPAID
tail-failure and A/B selection                          UNPAID
actual packet attachment and provenance                 UNPAID
single pointed dynamics parameter/factor                UNPAID
growing block discrepancy and positive physical main    UNPAID
~~~

Accordingly,

~~~text
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
~~~

The two O161 pointwise parents, pair-native route, H1, A1/A2 and the global
architecture remain open and independent.  No V1/common-k/tail-failure/A/B
or full-ultra STOP cell is reopened.

## 9. Source locks

The primary interfaces reviewed for this note are:

1. Matomaki--Radziwill--Tao, arXiv:1707.01315v3, Theorem 1.3,
   Propositions 3.1, 3.4 and 6.1;
2. Matomaki--Shao--Tao--Teravainen,
   arXiv:2204.03754, Theorem 1.1(ii);
3. Matomaki--Radziwill--Shao--Tao--Teravainen,
   arXiv:2411.05770v2, Theorem 1.1(ii),
   Corollary 1.2 and Theorems 1.5, 1.8;
4. Leung, arXiv:2210.13081v2, Theorems 1.1--1.2;
5. Bettin--Chandee, arXiv:1502.00769v1, Corollary 1;
6. Drappeau, arXiv:1504.05549v4, Theorems 2.1 and 5.1;
7. Aspenberg--Baladi--Persson, arXiv:2212.12202v2, Theorem 1.1;
8. Haydn--Nicol--Torok--Vaienti, arXiv:1406.4266, Theorems 3.1 and 4.1;
9. Korepanov, arXiv:1703.09176, the fixed-observable ASIP interface.

The source-backed labels in this note are limited to their literal local
inputs.  None is promoted to (3.3), (6.1) or (7.6).

## 10. Reopen gates

The selected analytic gate may advance only if one theorem supplies all of:

~~~text
literal beta_raw and Lambda-b_z coefficient;
fixed physical h0=2;
actual shifted hard shell and both shift signs;
prime-only Q=x^(1/3) ensemble and L_pr normalization;
weighted all-h ell2 norm with Schwartz tails;
uniform theta<13/4800 after every physical loss;
explicit local-main/zero-axis treatment;
one outer absolute and exactly-once reassembly.
~~~

The pointed dynamics gate may advance only after an exact single-parameter
natural-section diagram and a theorem for the actual growing block family.
Positive measure, a.e. parameter genericity or separate parameters by stage
do not trigger reopening.

Even a positive result at either local gate does not automatically create
TPC-207.  The all-D, physical-cover, global-normalization, tail-failure,
A/B-selection, packet-attachment and provenance gates remain separate.
