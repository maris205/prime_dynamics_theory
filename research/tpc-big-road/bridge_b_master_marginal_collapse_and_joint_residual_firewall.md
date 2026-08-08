# Bridge A / Gate B V33: MASTER marginal collapse and the joint-residual firewall

Status:

```text
UNNUMBERED_BIG_ROAD_CHECKPOINT
ROUTE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
NUMBERED_RELEASE = NO
```

This artifact stays on the V32 main road.  It does not replace the
single-scale oscillation gate, the terminal q-local covariance, or the
dynamics reserve.  Its new contribution is narrower and exact: after all
root-one HB2 occurrences with route `MASTER` are combined at a fixed physical
integer, their scalar marginal is a two-term arithmetic function.  The
occurrence-native local Euler carrier does not undergo the same collapse.

## 1. Frozen object and claim ceiling

Let \(x\geq 8\), let

\[
 I_x=(x/2,x]\cap\mathbb Z,
 \qquad
 U_x=\{d\in\mathbb N:d^{400}\leq x^{133}\},
 \tag{1.1}
\]

and retain the V19 source slot order, unit policy, first-large rule and first
admissible-bitmask rule.  The root-one rows are exactly

\[
 2\mu(e_1)\log f_1
 \quad (t=e_1f_1),
 \qquad
 -\mu(e_1)\mu(e_2)\log f_1
 \quad (t=e_1e_2f_1f_2).
 \tag{1.2}
\]

Their combined MASTER numerator and normalized coefficient are

\[
 N_x^M(t)=\sum_{o:t_o=t,\ \operatorname{route}(o)=M}
 c_{j(o)}\prod_i\mu(e_i(o))\log f_1(o),
 \qquad
 \beta_x^{\rm raw}(t)={N_x^M(t)\over\log t}.
 \tag{1.3}
\]

The maximum claim of V33 is the exact identity

\[
 \boxed{
 \beta_x^{\rm raw}(t)
 ={\Lambda(t)\over\log t}
 -\sum_{\substack{d\mid t\\d^{400}\leq x^{133}}}\mu(d),
 \qquad t\in I_x .}
 \tag{1.4}
\]

This is a collective scalar marginal identity.  It is not a separated HB2
template theorem and is not an identity for the occurrence-native local Euler
carrier.

## 2. Why the cutoff is strictly below the large-component boundary

Write \(J=133/400\).  Since

\[
 {1\over2}-J={67\over400},
 \qquad
 x^{67/400}\geq 8^{67/400}
 =2^{201/400}>2^{200/400}=\sqrt2
 \quad (x\geq8),
 \tag{2.1}
\]

we have

\[
 x^J<\sqrt{x/2}<\sqrt t
 \qquad (t\in I_x).
 \tag{2.2}
\]

Consequently, whenever a complement \(d\) satisfies
\(d^{400}\leq x^{133}\), every factor of \(d\) occurs before the unique
complementary large \(F\)-slot.  All corresponding \(E\)-slots also satisfy
the source cutoff \(e_i\leq\sqrt x\).  No asymptotic replacement of the endpoint is
being made: the condition remains the exact integer-power comparison in
(1.1).

## 3. The three H2 branches

The already source-locked root-one HB2 identity says that the sum of all
root-one rows, before the `H2 | MASTER` split, is \(\Lambda(t)\).  It therefore
suffices to aggregate the H2 rows.

Fix \(d\mid t\) with \(d^{400}\leq x^{133}\).

1. The J1 large-\(f_1\) branch has \(e_1=d\), hence contributes

   \[
   2\mu(d)\log(t/d).
   \tag{3.1}
   \]

2. In the J2 large-\(f_1\) branch, \(e_1e_2f_2=d\).  Since
   \(\mu*\mu*1=\mu\), its aggregate contribution is

   \[
   -\mu(d)\log(t/d).
   \tag{3.2}
   \]

3. In the J2 large-\(f_2\) branch, \(e_1e_2f_1=d\).  Since

   \[
   \mu*\mu*\log=\mu*\Lambda=-\mu\log,
   \tag{3.3}
   \]

   the outer minus sign gives

   \[
   +\mu(d)\log d.
   \tag{3.4}
   \]

The two J2 large-\(F\) branches cannot overlap.  Indeed their two complements
\(D_1,D_2\) satisfy

\[
 D_1D_2=(e_1e_2)t\geq t>x/2,
 \tag{3.5}
\]

whereas simultaneous H2 membership would give
\(D_1D_2\leq x^{266/400}<x/2\) for \(x\geq8\).

Adding (3.1), (3.2) and (3.4) gives exactly

\[
 \mu(d)\log t.
 \tag{3.6}
\]

Thus the full H2 numerator equals

\[
 N_x^{H2}(t)=\log t
 \sum_{\substack{d\mid t\\d^{400}\leq x^{133}}}\mu(d).
 \tag{3.7}
\]

Subtracting (3.7) from the full root-one numerator \(\Lambda(t)\) proves
(1.4).

## 4. Prime powers and the separate root remainder

Equation (1.4) includes the root-one row at prime powers.  For \(t=p^a\),

\[
 {\Lambda(t)\over\log t}={1\over a}.
 \tag{4.1}
\]

In particular, for a prime \(p\in I_x\), only \(d=1\) lies below the cutoff,
so \(\beta_x^{\rm raw}(p)=0\).  This cancellation is exact.  It must not be
misstated as deletion of every prime-power term: the modified-HB identity's
separate root \(s\geq2\) remainder remains governed by the previously paid
\(x^{1/2+o(1)}\) estimate, while (1.4) describes only the root-one MASTER
marginal.

The identity may be written as

\[
 \beta_x^{\rm raw}
 ={\Lambda\over\log}-(\mu_{U_x}*1)
 \quad\hbox{on }I_x,
 \qquad
 \mu_{U_x}(d)=\mu(d){\bf1}_{d^{400}\leq x^{133}}.
 \tag{4.2}
\]

It exposes a truncated sieve remainder, not an arbitrary divisor-bounded
coefficient.

## 5. Exact finite checks

Independent integer-power enumeration over every \(8\leq x\leq320\) and
every \(t\in I_x\) gives 25,744 exact cases, containing 422,101 MASTER and
257,830 H2 occurrences.  Formal prime-log vectors are used throughout; no
floating logarithm is compared.

The first wrong-J2-sign witness is \(x=8,t=6\).  The correct numerator is
\(-\log2-\log3\); changing the J2 outer coefficient from \(-1\) to \(+1\)
gives \(\log2-3\log3\).  The first checked wrong-cutoff witness obtained by
replacing \(133\) with \(132\) is \(x=127,t=65\): the correct row is zero,
whereas the mutated row is \(-\log5-\log13\).

At \(x=100,t=84\), the cutoff sum is \(-1\), so the exact MASTER numerator
is \(\log84\).  At \(x=100,t=64\), the cutoff sum is zero and the root-one
MASTER numerator is \(\log2\); at \(x=100,t=100\), both terms vanish.
These examples lock composite, prime-power, and zero behavior separately.

## 6. Why the local carrier does not collapse

V32 uses

\[
 M_x^{\rm loc}(h)=\sum_o a_o^M\Delta_{m(o),z}(h),
 \tag{6.1}
\]

where the selected group \(m(o)\) remains occurrence data.  The scalar sum in
(1.3) forgets that label.

There is an exact finite collision at \(x=121,t=77,z=5\).  The two J2 MASTER
occurrences

\[
 (e_1,e_2,f_1,f_2)=(1,1,7,11),\quad c=-1,\quad m=7,
 \tag{6.2}
\]

and

\[
 (e_1,e_2,f_1,f_2)=(1,11,7,1),\quad c=+1,\quad m=11
 \tag{6.3}
\]

contribute \(-\log7\) and \(+\log7\) to the marginal, hence cancel there.
Both selected primes exceed \(z\), but

\[
 \Delta_{7,5}(5)=-{35\over36},
 \qquad
 \Delta_{11,5}(5)={11\over100}.
 \tag{6.4}
\]

Their local-carrier contribution is therefore nonzero.  A theorem accepting
only the collapsed coefficient may control \(\mathcal B_x\), but it cannot
be declared a theorem for \(L_x\), \(R_x=P_x-L_x\), or
\(\mathfrak Q_{Y_0}^{\rm osc}(R_x)\) without a new occurrence-to-main
compiler.

## 7. Bazin's genuine marginal interface

Let

\[
 \Xi(f,x,Q,\vartheta)=
 \sum_{q\leq Q}{q\over\phi(q)}
 \sum_{\chi\bmod q}^{*}
 \max_{|\lambda|\leq\vartheta}
 \left|\sum_{n\leq x}f(n)\chi(n)e(\lambda n)\right|.
 \tag{7.1}
\]

Bazin, arXiv:2607.15137v1, Theorem 8, accepts a finite linear combination of
Dirichlet convolutions whose factors are log-bounded and are either Type I
character-sum factors or supported in \([1,x^{2/3}]\).  In (4.2), \(1\) is
Type I by Pólya--Vinogradov and \(\mu_{U_x}\) is Type II because
\(133/400<2/3\).  The source itself records Vaughan's identity for
\(\Lambda\).  Abel summation on \(I_x\) supplies the factor \(1/\log t\), and
subtracting the two endpoint sums supplies the hard shell.  Hence the source
gives the honest marginal bound

\[
 \Xi(\beta_x^{\rm raw}{\bf1}_{I_x},x,Q,\vartheta)
 \ll
 \{x^{1/2}Q^2+x^{5/6}Q+x+xQ^2\vartheta^{1/2}\}
 (\log x)^{O(1)}.
 \tag{7.2}
\]

This corrects the V32 source boundary: Bazin does accept the collapsed
\(\beta\)-marginal.  It does not accept the joint physical product or the
occurrence-native subtraction.

## 8. The natural rational-tube loss

At the V32 cell scale

\[
 H=x^{21/32},\qquad Q_0=H^{1/2}=x^{21/64},qquad
 \vartheta_0=H^{-1}=x^{-21/32}.
 \tag{8.1}
\]

The four exponents in (7.2) are

\[
 {37\over32},\qquad {223\over192},\qquad1,
 \qquad {85\over64}.
 \tag{8.2}
\]

The last term dominates.  Bazin's own conversion from character sums to the
additive rational-tube discrepancy costs \(Q_0^{-1/2}\), leaving

\[
 {85\over64}-{21\over128}={149\over128}
 =1+{21\over128}.
 \tag{8.3}
\]

Relative to the largest norm exponent compatible with V32,
\(1+13/4800\), this natural one-marginal route misses by

\[
 {21\over128}-{13\over4800}={1549\over9600}.
 \tag{8.4}
\]

This is a route-loss ledger, not an impossibility theorem: (7.2) and the V32
oscillation functional are different norms.  It does prove that simply
feeding the newly collapsed marginal through the source's advertised
rational-tube conversion does not pay the endpoint.  It reproduces the
one-sided \(H^{1/4}\) loss already isolated in V28--V30.

## 9. Other primary-source boundaries

MRT, arXiv:1707.01315v3, Proposition 3.1 remains an abstract product-energy
reduction.  Its one-sided \(\Lambda/d_k\) input and the Bazin marginal do not
produce the required two-sided product-local power norm.

Evans, arXiv:2102.12297v3, Theorem 1.4 proves prime--\(E_2\) correlations for
almost all shifts and its proof contains a genuine minor-arc mean square, but
the quantitative scale is \(Hx^2(\log x)^{-B}\).  Its square root is
\(xH^{1/2}(\log x)^{-B/2}\), not \(x^{1+\sigma}\).  The coefficient is a
fixed \(E_2\) indicator, and the theorem has no occurrence-native
\(M_x^{\rm loc}\).

Matomäki--Radziwiłł--Shao--Tao--Teräväinen,
arXiv:2411.05770v2, Theorem 1.5 gives the Hardy--Littlewood formula for a
proportion \(1-o(1)\) of shifts in the relevant \(H\)-range.  It supplies no
power-rate all-shift \(\ell^2\) estimate for the literal residual.  Neither
source attaches directly to V32.

## 10. Route decision and canonical registry

The new exact identity makes the prime-side marginal source-native and
removes the phrase "no literal Bazin emitter" from that marginal.  The first
fatal has moved one level downstream:

\[
 \boxed{\text{No checked source proves a power mean square for the collapsed
 sieve remainder times the physical hybrid, with the same occurrence-native
 local carrier subtracted.}}
 \tag{10.1}
\]

The selected road remains

```text
B: literal joint residual power mean square / base-scale oscillation
  -> A: terminal q-local covariance
  -> C: symmetry-breaking pointed dynamics reserve.
```

Canonical status:

```text
V33_MAXIMUM_CLAIM = EXACT_ROOT_ONE_MASTER_MARGINAL_COLLAPSE_TO_TRUNCATED_MOBIUS_SIEVE_REMAINDER_PLUS_BAZIN_MARGINAL_INTERFACE_AND_LOCAL_CARRIER_FIREWALL
V33_ROUTE_ADVANCE = YES
V33_ARITHMETIC_ADVANCE = NO
V33_FIXED_ATOM_CREDIT = 0
V33_STRICT_1_OVER_400 = UNPAID
V33_L2 = NONE
V33_TPC_207_TRIGGER = false
V33_NUMBERED_RELEASE = NO
V33_SELECTED_RESEARCH_ROUTE = B_JOINT_RESIDUAL_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK
V33_ROOT_ONE_SCOPE = EXACT_MASTER_MARGINAL_ONLY
V33_PHYSICAL_SHELL = X_OVER_2_LT_T_LE_X_WITH_X_GE_8
V33_EXACT_CUTOFF = D_POWER_400_LE_X_POWER_133
V33_CUTOFF_BELOW_SQRT_T = PROVED_EXACT_FROM_67_OVER_400_AND_X_GE_8
V33_HB2_FULL_ROOT_ONE_NUMERATOR = RETAINED_SOURCE_LOCKED_LAMBDA_T
V33_H2_J1_BRANCH = PROVED_EXACT_2_MU_D_LOG_T_OVER_D
V33_H2_J2_LARGE_F1_BRANCH = PROVED_EXACT_MINUS_MU_D_LOG_T_OVER_D
V33_H2_J2_LARGE_F2_BRANCH = PROVED_EXACT_PLUS_MU_D_LOG_D
V33_MU_MU_ONE_IDENTITY = PROVED_EXACT_MU
V33_MU_MU_LOG_IDENTITY = PROVED_EXACT_MINUS_MU_LOG
V33_TWO_J2_H2_BRANCHES = PROVED_DISJOINT_ON_X_GE_8
V33_MASTER_MARGINAL_IDENTITY = PROVED_EXACT_LAMBDA_OVER_LOG_MINUS_TRUNCATED_MU_CONV_ONE
V33_PRIME_MASTER_MARGINAL = PROVED_EXACT_ZERO
V33_ROOT_ONE_PRIME_POWER_TERM = RETAINED_EXACT_LAMBDA_OVER_LOG
V33_ROOT_GE_2_PERFECT_POWER_REMAINDER = RETAINED_SEPARATE_X_1_OVER_2_PLUS_O1
V33_FINITE_ROUTING_RECOMPUTATION = PROVED_25744_SHELL_CASES_422101_MASTER_257830_H2
V33_WRONG_J2_SIGN = STOP_SCOPED_X8_T6_FORMAL_LOG_VECTOR
V33_WRONG_CUTOFF_132 = STOP_SCOPED_X127_T65_FORMAL_LOG_VECTOR
V33_OCCURRENCE_LOCAL_COLLISION = PROVED_EXACT_X121_T77_Z5_GROUPS_7_AND_11
V33_MARGINAL_TO_OCCURRENCE_LOCAL_CARRIER = STOP_SCOPED_SELECTED_GROUP_DATA_NOT_ACCEPTED_BY_MARGINAL_THEOREM
V33_BAZIN_BETA_MARGINAL = SOURCE_BACKED_TYPE_I_II_XI_ATTACHMENT
V33_BAZIN_BASE_CELL_Q = X_POWER_21_OVER_64
V33_BAZIN_BASE_CELL_THETA = X_POWER_MINUS_21_OVER_32
V33_BAZIN_XI_DOMINANT_EXPONENT = 85_OVER_64
V33_BAZIN_ADDITIVE_TUBE_EXPONENT = 149_OVER_128
V33_BAZIN_ENDPOINT_DEFICIT = 1549_OVER_9600
V33_BAZIN_TO_V32_QOSC = STOP_SCOPED_MARGINAL_WRONG_NORM_AND_H_QUARTER_LOSS
V33_EVANS_PRIME_E2_TO_LITERAL_RESIDUAL = STOP_SCOPED_FIXED_E2_LOG_SAVING_AND_NO_LOCAL_CARRIER
V33_MRSTT_ALMOST_ALL_SHIFT_TO_LITERAL_RESIDUAL_L2 = STOP_SCOPED_QUALITATIVE_DENSITY_ONE_WRONG_NORM
V33_DIRECT_PRIMARY_SOURCE_ATTACHMENT_TO_QOSC = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V33_NEXT_THEOREM = POWER_MEAN_SQUARE_FOR_COLLAPSED_SIEVE_REMAINDER_TIMES_PHYSICAL_HYBRID_WITH_OCCURRENCE_NATIVE_LOCAL_CARRIER
V33_FIRST_FATAL = NO_JOINT_POWER_MEAN_SQUARE_FOR_COLLAPSED_SIEVE_REMAINDER_TIMES_PHYSICAL_HYBRID_WITH_OCCURRENCE_NATIVE_LOCAL_CARRIER
V33_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
V33_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
```

The checkpoint is an exact compiler and source-boundary advance.  It is not a
physical \(L^2\) estimate, does not pay the terminal axis, and does not create
TPC-207.
