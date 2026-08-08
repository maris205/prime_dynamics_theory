# Bridge A / Gate B V35: proper factors and the coprime fixed-shift ratio core

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

V35 stays at the red crossing of Bridge A.  It does not prove the missing
power saving.  It removes three false complications from the V34 compensated
prime frame: both divisor endpoints vanish exactly, every prime row is empty,
and the nonunit and unit-principal modulus rows are already below the strict
endpoint.  The remaining object is one prime-only, zero-deleted, coprime
fixed-shift-two ternary ratio core.

## 1. Frozen object and claim ceiling

Keep

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad H=x^{21/32},\qquad Q=x^{1/3},
 \tag{1.1}
\]

\[
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},\qquad
 L_{\rm pr}=\sum_{q\in\mathcal Q}(q-1)=x^{2/3+o(1)},
 \tag{1.2}
\]

and

\[
 w_x^{(z)}(u)=\Lambda(u+2)-b_x^{(z)}(u).
 \tag{1.3}
\]

The V33/V34 collapsed sieve marginal is

\[
 \beta_x^{\rm raw}(t)=
 \frac{\Lambda(t)}{\log t}
 -\sum_{\substack{d\mid t\\d^{400}\leq x^{133}}}\mu(d).
 \tag{1.4}
\]

V34 reduced the B gate to the zero-deleted compensated numerator

\[
 \mathfrak D_x=
 \sum_{q\in\mathcal Q}
 \sum_{\substack{t,u\in I_x\\t\ne u}}
 \beta_x^{\rm raw}(t)w_x^{(z)}(u)
 \widehat\psi_+\!\left(\frac{u-t}{H}\right)
 \left(q\mathbf1_{u\equiv t\ ({\rm mod}\ q)}-1\right).
 \tag{1.5}
\]

The maximum V35 claim is an exact reduction of (1.5), plus absolute payment
of two harmless remainders.  No new estimate for the surviving core is
claimed.

## 2. Endpoint-free proper-factor identity

For every integer \(t>1\),

\[
 \Lambda(t)=-\sum_{d\mid t}\mu(d)\log d.
 \tag{2.1}
\]

Since \(t\in I_x\) and \(x\geq8\), one has \(t^{400}>x^{133}\).  Combining
(1.4) and (2.1) gives

\[
 \beta_x^{\rm raw}(t)=
 \sum_{dk=t}\mu(d)
 \left(\mathbf1_{d^{400}>x^{133}}-\frac{\log d}{\log t}\right).
 \tag{2.2}
\]

The \(d=1\) coefficient is zero.  The \(k=1,d=t\) coefficient is also zero:

\[
 1-\frac{\log t}{\log t}=0.
 \tag{2.3}
\]

Consequently the sharp support identity is

\[
 \boxed{
 \beta_x^{\rm raw}(t)=
 \sum_{\substack{dk=t\\d,k\geq2}}\mu(d)\omega_x(d,k),}
 \tag{2.4}
\]

where

\[
 \omega_x(d,k)=
 \begin{cases}
 -\dfrac{\log d}{\log(dk)},&d^{400}\leq x^{133},\\[2mm]
 \dfrac{\log k}{\log(dk)},&d^{400}>x^{133}.
 \end{cases}
 \qquad |\omega_x(d,k)|\leq1.
 \tag{2.5}
\]

Thus both factors in every active term are proper factors.  In particular,

\[
 \boxed{\beta_x^{\rm raw}(p)=0\quad(p\ {\rm prime}).}
 \tag{2.6}
\]

The checker verifies (2.4) on 25,744 shell cases by multiplying by
\(\log t\) and comparing exact prime-log coefficient vectors.  It never uses
floating logarithms.  It also checks 4,945 prime rows and 72,237 nonzero
proper-factor contributions.  Including \(k=1\) with its true zero
coefficient is semantically identical to (2.4), so it is not advertised as a
mutation.

## 3. Exact unit-ratio decomposition

Put

\[
 A_x(d,k,u)=\mu(d)\omega_x(d,k)w_x^{(z)}(u)
 \widehat\psi_+\!\left(\frac{u-dk}{H}\right).
 \tag{3.1}
\]

For prime \(q\) and \(a\in(\mathbb Z/q\mathbb Z)^\times\), define

\[
 u_1(a;q)=\mathbf1_{a\equiv1\ ({\rm mod}\ q)}-\frac1{q-1}
 =\frac1{q-1}\sum_{\substack{\chi\ ({\rm mod}\ q)\\\chi\ne\chi_0}}\chi(a).
 \tag{3.2}
\]

On \(q\nmid dku\),

\[
 \boxed{
 q\mathbf1_{u\equiv dk\ ({\rm mod}\ q)}-1
 =q\,u_1(u\overline{dk};q)+\frac1{q-1}.}
 \tag{3.3}
\]

Partitioning (1.5) before taking any absolute value yields

\[
 \boxed{\mathfrak D_x=\mathfrak C_x+\mathfrak P_x+\mathfrak N_x,}
 \tag{3.4}
\]

with coprime centered core

\[
 \boxed{
 \mathfrak C_x=
 \sum_{q\in\mathcal Q}q
 \sum_{\substack{dk,u\in I_x\\d,k\geq2,\ u\ne dk\\q\nmid dku}}
 A_x(d,k,u)u_1(u\overline{dk};q),}
 \tag{3.5}
\]

unit-principal remainder

\[
 \mathfrak P_x=
 \sum_{q\in\mathcal Q}\frac1{q-1}
 \sum_{\substack{dk,u\in I_x\\d,k\geq2,\ u\ne dk\\q\nmid dku}}
 A_x(d,k,u),
 \tag{3.6}
\]

and nonunit remainder

\[
 \mathfrak N_x=
 \sum_{q\in\mathcal Q}
 \sum_{\substack{dk,u\in I_x\\d,k\geq2,\ u\ne dk\\q\mid dku}}
 A_x(d,k,u)
 \left(q\mathbf1_{u\equiv dk\ ({\rm mod}\ q)}-1\right).
 \tag{3.7}
\]

Equations (3.3)--(3.7) are exact.  In particular, the centered character
kernel and the principal correction must travel together until (3.6) is
paid.

## 4. The two paid remainders

The frozen divisor envelopes give

\[
 |\beta_x^{\rm raw}(t)|,\ |w_x^{(z)}(u)|\leq x^{o(1)},
 \tag{4.1}
\]

and the Schwartz difference weight has total mass \(O(Hx^{o(1)})\) for
each outer variable.  On the nonunit rows, exactly one divisible coordinate
has kernel size one; if both are divisible, the kernel may have size \(q\)
but the second divisibility saves another factor \(q\).  Hence, for each
\(q\sim Q\),

\[
 \mathfrak N_x(q)\ll x^{o(1)}\left(\frac{xH}{q}+x\right).
 \tag{4.2}
\]

Summing the prime shell gives

\[
 \boxed{|\mathfrak N_x|\ll x^{53/32+o(1)}.}
 \tag{4.3}
\]

For (3.6), the coefficient \((q-1)^{-1}\) pays the full unit pair mass:

\[
 \boxed{
 |\mathfrak P_x|
 \ll xH\,x^{o(1)}\sum_{q\in\mathcal Q}\frac1q
 \ll x^{53/32+o(1)}.}
 \tag{4.4}
\]

The precise numerator saving and endpoint margin are

\[
 \frac53-\frac{53}{32}=\frac1{96},
 \qquad
 \left(\frac53-\frac1{400}\right)-\frac{53}{32}
 =\boxed{\frac{19}{2400}}.
 \tag{4.5}
\]

After division by \(L_{\rm pr}\), the paid terms have exponent

\[
 \frac{53}{32}-\frac23=\frac{95}{96},
 \qquad
 \frac{399}{400}-\frac{95}{96}=\frac{19}{2400}.
 \tag{4.6}
\]

## 5. Fixed-shift-two geometry of the surviving core

Writing \(n=u+2\), the congruence in (3.5) becomes

\[
 n\equiv dk+2\pmod q,
 \qquad n\ne dk+2,
 \qquad q\nmid(n-2)dk,
 \tag{5.1}
\]

while the physical coefficient and short-difference weight are

\[
 \Lambda(n)-b_x^{(z)}(n-2),
 \qquad
 \widehat\psi_+\!\left(\frac{n-2-dk}{H}\right).
 \tag{5.2}
\]

Thus (3.5) is not a binary fixed-residue convolution.  It is a prime-only,
zero-deleted, three-array shifted-product ratio frame.  The exact character
form is

\[
 \mathfrak C_x=
 \sum_{q\in\mathcal Q}\frac{q}{q-1}
 \sum_{\substack{\chi\ ({\rm mod}\ q)\\\chi\ne\chi_0}}
 \sum_{\substack{dk,u\in I_x\\d,k\geq2,\ u\ne dk\\q\nmid dku}}
 A_x(d,k,u)\chi(u)\overline{\chi(dk)}.
 \tag{5.3}
\]

The \(d,k\) weight remains coupled, the \(u\)-coefficient is physical, and
the diagonal is deleted.  These are theorem inputs, not disposable notation.

## 6. Strict endpoint compiler

The only remaining B theorem is

\[
 \boxed{
 |\mathfrak C_x|\ll x^{5/3-\delta+o(1)},
 \qquad \delta>\frac1{400}.}
 \tag{6.1}
\]

Together with (4.3)--(4.4), it gives an effective numerator saving smaller
than \(\min(\delta,1/96)\).  V29 already paid the local carrier at exponent
\(1891/1920\), leaving margin

\[
 \frac{399}{400}-\frac{1891}{1920}=\frac{121}{9600}.
 \tag{6.2}
\]

Therefore any final B saving must obey

\[
 \boxed{
 0<\eta_B<\min\left(
 \delta-\frac1{400},\frac{19}{2400},\frac{121}{9600}
 \right).}
 \tag{6.3}
\]

Equality \(\delta=1/400\) is insufficient.

## 7. Diagonal and triangle firewalls

The condition \(u\ne dk\) may not be removed to manufacture a factorization.
Restoring the diagonal in the original compensated frame adds

\[
 L_{\rm pr}S_x^{\rm physical},
 \qquad
 S_x^{\rm physical}=\sum_{t\in I_x}\beta_x^{\rm raw}(t)w_x^{(z)}(t),
 \tag{7.1}
\]

which is the unknown scalar itself.  Restoring only the centered core adds

\[
 \boxed{
 \sum_{q\in\mathcal Q}\frac{q(q-2)}{q-1}
 \sum_{\substack{t\in I_x\\q\nmid t}}
 \beta_x^{\rm raw}(t)w_x^{(z)}(t).}
 \tag{7.2}
\]

Its absolute ledger is \(x^{5/3+o(1)}\), so it loses every fixed saving.
Likewise, separating the positive divisibility part from the compensation in
(1.5) gives the raw ceiling

\[
 x^{191/96+o(1)}.
 \tag{7.3}
\]

No source application may silently reinsert the diagonal, take a per-modulus
triangle, or take a per-shift triangle.

## 8. Primary-source boundary

For prime \(q\), Drappeau's \(u_R\) kernel at \(R=1\) agrees with (3.2) on
units.  Theorem 5.1 nevertheless controls

\[
 \sum_{Q<q\leq2Q}\sum_{m,n}\alpha_m\beta_n
 u_R(mna_1a_2;q),
 \tag{8.1}
\]

with two \(q\)-independent dyadic arrays and fixed \(a_1,a_2\), averaged over
all dyadic moduli.  It does not accept the third physical array, the variable
ratio \(u\overline{dk}\), prime-only moduli, the short difference, and the
deleted diagonal simultaneously.  Taking \(R=1\) also removes the advertised
\(R^{-1}\) source saving; taking \(R>1\) introduces unpaid low-conductor
characters.  See [Drappeau, Theorem 5.1 and (5.1), (5.3)--(5.7)](https://arxiv.org/pdf/1504.05549#page=23).

The fixed-residue binary interfaces of
[Fouvry--Radziwiłł, Theorems 1.1--1.2](https://arxiv.org/pdf/1811.08672#page=7)
and [Wright, Corollary 2.2](https://arxiv.org/pdf/2604.25177#page=4) have the
same object mismatch.  Bettin--Chandee controls trilinear Kloosterman
fractions and a fixed determinant, not the moving relation
\(n-dk=2+\ell q\); see [Theorem 1 and Corollary 1](https://arxiv.org/pdf/1502.00769#page=2).
Even an optimistic \(x^{39/40}\) balanced fixed-determinant cell, triangulated
over the weighted \((q,\ell)\)-family of exponent \(95/96\), gives

\[
 x^{39/40+95/96+o(1)}=x^{943/480+o(1)},
 \tag{8.2}
\]

which misses the required numerator exponent by

\[
 \frac{943}{480}-\left(\frac53-\frac1{400}\right)
 =\frac{721}{2400}.
 \tag{8.3}
\]

Bazin's Theorem 8 controls one marginal convolution norm, not the physical
product in (3.5).  No screened primary source proves (6.1).

## 9. Finite exact fixtures

Besides the formal prime-log census, the checker freezes a rational
ten-point fixture with primes \(5,7\).  It obtains

\[
 \mathfrak D=-\frac{6061}{315},\quad
 \mathfrak N=-\frac{537}{140},\quad
 \mathfrak C=-\frac{39583}{2160},\quad
 \mathfrak P=\frac{6307}{2160},
 \tag{9.1}
\]

and verifies \(\mathfrak D=\mathfrak N+\mathfrak C+\mathfrak P\) exactly.
The same fixture has

\[
 S^{\rm physical}=-12,\qquad L_{\rm pr}S^{\rm physical}=-120,
 \tag{9.2}
\]

so diagonal restoration is visibly nonzero.  All values use
`fractions.Fraction`.

## 10. Canonical status registry

```text
V35_MAXIMUM_CLAIM = EXACT_ENDPOINT_FREE_PROPER_FACTOR_AND_PAID_NONUNIT_PRINCIPAL_REDUCTION_TO_ZERO_DELETED_COPRIME_FIXED_SHIFT_TWO_TERNARY_RATIO_CORE
V35_ROUTE_ADVANCE = YES
V35_ARITHMETIC_ADVANCE = NO
V35_FIXED_ATOM_CREDIT = 0
V35_STRICT_1_OVER_400 = UNPAID
V35_L2 = NONE
V35_TPC_207_TRIGGER = false
V35_NUMBERED_RELEASE = NO
V35_SELECTED_RESEARCH_ROUTE = B_COPRIME_FIXED_SHIFT_RATIO_CORE_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK
V35_V34_COMPENSATED_FRAME = RETAINED_EXACT_ZERO_DELETED_ONE_OUTER_SIGNED_SCALAR
V35_PROPER_FACTOR_IDENTITY = PROVED_EXACT_BETA_EQUALS_SUM_MU_TIMES_OMEGA
V35_D_EQ_1_ENDPOINT = PROVED_EXACT_ZERO_COEFFICIENT
V35_K_EQ_1_ENDPOINT = PROVED_EXACT_ZERO_COEFFICIENT
V35_PROPER_FACTOR_SUPPORT = PROVED_EXACT_D_AND_K_AT_LEAST_2
V35_PROPER_FACTOR_WEIGHT = PROVED_EXACT_PIECEWISE_NEG_LOG_D_OR_POS_LOG_K_OVER_LOG_DK
V35_PROPER_FACTOR_WEIGHT_BOUND = PROVED_EXACT_ABSOLUTE_VALUE_AT_MOST_1
V35_PRIME_ROWS = PROVED_EXACT_EMPTY
V35_UNIT_RATIO_VECTOR = PROVED_EXACT_Q_U1_PLUS_ONE_OVER_Q_MINUS_1
V35_UNIT_CHARACTER_EXPANSION = PROVED_EXACT_NONPRINCIPAL_CHARACTER_AVERAGE
V35_EXACT_DECOMPOSITION = PROVED_EXACT_D_EQUALS_CORE_PLUS_PRINCIPAL_PLUS_NONUNIT
V35_NONUNIT_PAYMENT = PROVED_ABSOLUTE_X_POWER_53_OVER_32_PLUS_O1
V35_UNIT_PRINCIPAL_PAYMENT = PROVED_ABSOLUTE_X_POWER_53_OVER_32_PLUS_O1
V35_PAID_REMAINDER_E_EXPONENT = X_POWER_95_OVER_96_PLUS_O1
V35_PAID_REMAINDER_NUMERATOR_SAVING = 1_OVER_96
V35_PAID_REMAINDER_ENDPOINT_MARGIN = 19_OVER_2400
V35_COPRIME_CORE = PROVED_EXACT_PRIME_ONLY_ZERO_DELETED_THREE_ARRAY_RATIO_FRAME
V35_FIXED_SHIFT_TWO_FORM = PROVED_EXACT_N_CONGRUENT_DK_PLUS_2
V35_CORE_NUMERATOR_TARGET = X_POWER_5_OVER_3_MINUS_DELTA_PLUS_O1
V35_REQUIRED_DELTA = STRICTLY_GREATER_THAN_1_OVER_400
V35_CORE_E_EXPONENT = X_POWER_1_MINUS_DELTA_PLUS_O1
V35_LOCAL_CARRIER_PAYMENT = RETAINED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1
V35_LOCAL_CARRIER_ENDPOINT_MARGIN = 121_OVER_9600
V35_COMBINED_B_MARGIN = MIN_DELTA_MINUS_1_OVER_400_AND_19_OVER_2400_AND_121_OVER_9600
V35_FULL_DIAGONAL_REINSERTION = STOP_SCOPED_CIRCULAR_L_PR_TIMES_PHYSICAL_SCALAR
V35_CORE_DIAGONAL_CORRECTION = STOP_SCOPED_ABSOLUTE_X_POWER_5_OVER_3
V35_RAW_POSITIVE_COMPENSATION_TRIANGLE = STOP_SCOPED_X_POWER_191_OVER_96
V35_DRAPPEAU_UNIT_KERNEL = MATCHES_U1_ONLY_AT_R_EQUALS_1_ON_PRIME_UNITS
V35_DRAPPEAU_DIRECT_ATTACHMENT = STOP_SCOPED_BINARY_FIXED_PRODUCT_ALL_MODULI_NO_THIRD_PHYSICAL_ARRAY_OR_ZERO_DELETION
V35_FOUVRY_RADZIWILL_DIRECT_ATTACHMENT = STOP_SCOPED_BINARY_FIXED_RESIDUE_WRONG_OBJECT_AND_SUBPOWER_OUTPUT
V35_WRIGHT_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_RESIDUE_SIEGEL_WALFISZ_ARRAY_NO_MOVING_RATIO
V35_BETTIN_CHANDEE_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_DETERMINANT_NO_COLLECTIVE_Q_ELL_REASSEMBLY
V35_BETTIN_CHANDEE_PER_SHIFT_TRIANGLE_EXPONENT = 943_OVER_480
V35_BETTIN_CHANDEE_PER_SHIFT_TRIANGLE_DEFICIT = 721_OVER_2400
V35_BAZIN_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_MARGINAL_NO_PHYSICAL_PRODUCT
V35_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V35_NEXT_THEOREM = DELTA_GT_1_OVER_400_POWER_SAVING_FOR_PRIME_ONLY_ZERO_DELETED_THREE_ARRAY_FIXED_SHIFT_TWO_RATIO_CORE
V35_FIRST_FATAL = NO_BINARY_SOURCE_PARAMETERIZATION_PRESERVES_Q_INDEPENDENT_COEFFICIENTS_PRIME_ONLY_ZERO_DELETION_AND_PHYSICAL_THIRD_ARRAY
V35_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
V35_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
```

The route position is unchanged: analytic elimination island, Bridge A,
Gate B.  What changed is the size of the red crossing.  Endpoint, prime,
nonunit, and principal rows are no longer part of it.
