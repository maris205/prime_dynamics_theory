# Bridge A / Gate B V34: paid local carrier and the compensated prime frame

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

V34 remains at the red crossing of Bridge A.  It does not prove a new
arithmetic estimate.  Its exact contribution is to remove one unnecessary
hypothesis from the selected road.  V29 already paid the scalar Jutila
contribution of the occurrence-native Euler carrier.  Therefore the new
arithmetic theorem for the off-zero gate need not control that carrier in a
mean square.  It may act directly on one collapsed, source-native scalar
covariance.

## 1. Frozen object and claim ceiling

Keep

\[
 I_x=(x/2,x]\cap\mathbb Z,
 \qquad H=x^{21/32},
 \qquad Q=x^{1/3},
 \tag{1.1}
\]

\[
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},
 \qquad
 L_{\rm pr}=\sum_{q\in\mathcal Q}(q-1)=x^{2/3+o(1)},
 \tag{1.2}
\]

and the physical hybrid

\[
 w_x^{(z)}(u)=\Lambda(u+2)-b_x^{(z)}(u).
 \tag{1.3}
\]

The V33 root-one MASTER marginal is

\[
 \beta_x^{\rm raw}(t)
 =\frac{\Lambda(t)}{\log t}
 -\sum_{\substack{d\mid t\\d^{400}\leq x^{133}}}\mu(d),
 \qquad t\in I_x.
 \tag{1.4}
\]

Define

\[
 r_x(h)=
 \sum_{\substack{t,t+h\in I_x}}
 \beta_x^{\rm raw}(t)w_x^{(z)}(t+h).
 \tag{1.5}
\]

The maximum claim of V34 is an exact reduction of the B gate to one
compensated prime-frame scalar involving only (1.4), (1.3), the hard shell,
and the frozen smooth difference weight.  No occurrence label is required in
the statement of the new arithmetic theorem.

## 2. Exact large-divisor Möbius tail

For every \(t>1\),

\[
 \sum_{d\mid t}\mu(d)=0.
 \tag{2.1}
\]

Consequently (1.4) is equivalently

\[
 \boxed{
 \beta_x^{\rm raw}(t)
 =\frac{\Lambda(t)}{\log t}
 +\sum_{\substack{d\mid t\\d^{400}>x^{133}}}\mu(d).}
 \tag{2.2}
\]

On \(I_x\), the divisor \(d=t\) is outside the cutoff.  Indeed,

\[
 t^{400}>\left(\frac{x}{2}\right)^{400}>x^{133},
 \qquad x\geq8,
 \tag{2.2a}
\]

because \(x^{267}\geq8^{267}=2^{801}>2^{400}\).  Splitting off
\(d=t\) and writing \(t=dk\) gives

\[
 \boxed{
 \beta_x^{\rm raw}(t)
 =\rho(t)+
 \sum_{\substack{dk=t\\k\geq2\\d^{400}>x^{133}}}\mu(d),
 \qquad
 \rho(t)=\frac{\Lambda(t)}{\log t}+\mu(t).}
 \tag{2.3}
\]

The endpoint coefficient is prime-deleted:

\[
 \rho(p)=0
 \qquad(p\ {\rm prime}).
 \tag{2.4}
\]

Thus the V33 scalar is not a hidden prime--prime coefficient.  It consists
of a prime-deleted Möbius endpoint and a genuine large-divisor bilinear tail.
This is an exact coefficient identity, not a correlation estimate.

## 3. The already-paid local carrier

Let \(M_x^{\rm loc}\) be the V28 occurrence-native Euler carrier and set

\[
 e_x(h)=r_x(h)-M_x^{\rm loc}(h).
 \tag{3.1}
\]

For the frozen Jutila operators,

\[
 J(f)+E(f)=f(0),
 \qquad
 E(f)=-\sum_{h\ne0}\kappa_x(h)f(h).
 \tag{3.2}
\]

V29 proved, using the literal reduced-radical Bettin--Chandee compiler,

\[
 \boxed{
 |E(M_x^{\rm loc})|, |J(M_x^{\rm loc})|
 \ll x^{1891/1920+o(1)}.}
 \tag{3.3}
\]

Linearity gives the exact scalar identity

\[
 \boxed{
 E(e_x)=E(r_x)-E(M_x^{\rm loc}).}
 \tag{3.4}
\]

Therefore a direct power bound for \(E(r_x)\) pays the B gate after adding
the already-paid term (3.3).  The new theorem does not need to accept the
selected-group label \(m(o)\), the local tensor, or the circle function
\(L_x\).

This reduction is scalar.  It does **not** say that the off-zero mean square
of \(r_x\) is small.  A large carrier can have a small signed Jutila pairing.
Replacing the V32 residual \(P_x-L_x\) by \(P_x\) inside
\(\mathfrak Q^{\rm osc}\) would reintroduce that large off-zero main and is
not justified by (3.3).

## 4. Three exact normal forms for the compensated frame

For a prime \(q\), put

\[
 c_q(h)=q\mathbf1_{q\mid h}-1,
 \qquad
 A_Q(h)=\sum_{q\in\mathcal Q}c_q(h).
 \tag{4.1}
\]

Define the zero-deleted smooth correlation

\[
 \Phi_x(h)=
 \mathbf1_{h\ne0}\widehat\psi_+(h/H)r_x(h).
 \tag{4.2}
\]

The direct numerator is

\[
 \boxed{
 \mathfrak D_x=
 \sum_{h\in\mathbb Z}A_Q(h)\Phi_x(h),
 \qquad
 E(r_x)=-\frac{\mathfrak D_x}{L_{\rm pr}}.}
 \tag{4.3}
\]

Using \(c_q(h)=q\mathbf1_{q\mid h}-1\) gives the compensated dilation form

\[
 \boxed{
 \mathfrak D_x=
 \sum_{q\in\mathcal Q}
 q\sum_{k\ne0}\Phi_x(qk)
 -|\mathcal Q|\sum_{h\ne0}\Phi_x(h).}
 \tag{4.4}
\]

Equivalently, substituting (1.5) gives the pair form

\[
 \boxed{
 \begin{aligned}
 \mathfrak D_x
  ={}&\sum_{q\in\mathcal Q}
 \sum_{\substack{t,u\in I_x\\t\ne u}}
 \beta_x^{\rm raw}(t)w_x^{(z)}(u)
 \widehat\psi_+\!\left(\frac{u-t}{H}\right)\\
 &\hspace{25mm}\times
 \left(q\mathbf1_{u\equiv t\pmod q}-1\right).
 \end{aligned}}
 \tag{4.5}
\]

There is one outer signed scalar in (4.5).  The two terms in the last
parenthesis must be estimated jointly.  Separating them by triangle returns
the previously rejected centered-projector ceiling.

## 5. The strict (1/400) clock

Because \(L_{\rm pr}=x^{2/3+o(1)}\), the clean source-ready theorem is

\[
 \boxed{
 |\mathfrak D_x|
 \ll x^{5/3-\delta+o(1)}
 \quad\hbox{for one fixed}\quad
 \delta>\frac1{400}.}
 \tag{5.1}
\]

Indeed, (4.3) then gives

\[
 |E(r_x)|\ll x^{1-\delta+o(1)}.
 \tag{5.2}
\]

Combining (3.3), (3.4), and (5.2),

\[
 |E(e_x)|
 \ll x^{1-\delta+o(1)}+x^{1891/1920+o(1)}.
 \tag{5.3}
\]

The two exact margins to (399/400) are

\[
 \frac{399}{400}-(1-\delta)
 =\delta-\frac1{400},
 \qquad
 \frac{399}{400}-\frac{1891}{1920}
 =\frac{121}{9600}.
 \tag{5.4}
\]

Hence the B gate receives any saving

\[
 \boxed{
 0<\eta_B<
 \min\left\{
 \delta-\frac1{400},\frac{121}{9600}
 \right\}.}
 \tag{5.5}
\]

Equality \(\delta=1/400\) is insufficient.  The benchmark \(x^{5/3}\)
is the square-root-per-prime-frame design scale; it is not asserted as a
proved asymptotic or a lower bound.

## 6. What V33 changes at the source interface

Before V33, the first marginal in (4.5) was only an occurrence sum.  Equations
(1.4) and (2.2) make it a source-native Type-I/II coefficient.

At the actual prime-frame parameters

\[
 Q=x^{1/3},
 \qquad
 \vartheta=H^{-1}=x^{-21/32},
 \tag{6.1}
\]

Bazin's Theorem 8 character-sum bound has exponents

\[
 \frac76,qquad\frac76,qquad1,qquad\frac{257}{192}.
 \tag{6.2}
\]

The last term dominates.  The source's additive conversion costs
\(Q^{-1/2}=x^{-1/6}\), so the honest one-marginal additive exponent is

\[
 \frac{257}{192}-\frac16=\frac{75}{64}.
 \tag{6.3}
\]

This is a real marginal input.  It is not (5.1): no checked source couples it
to the physical \(\Lambda(\cdot+2)-b_x^{(z)}\) factor in the same compensated
prime frame with a power \(\delta>1/400\).

## 7. Why the direct scalar is the selected road

The following implications are exact:

```text
V32 Qosc(P-L) theorem
    -> weighted off-zero norm for e
    -> bound for E(e),

V34 direct compensated covariance theorem
    -> bound for E(r)
    + already-paid E(Mloc)
    -> bound for E(e).
```

The second route is strictly weaker as a requested theorem.  It does not
control all off-zero coefficients and does not pay terminal \(J(e_x)\).

To see why \(Q^{\rm osc}(P_x)\) is not a valid intermediate replacement,
take a finite carrier with \(M(0)=0\), \(M(1)=T\), \(M(2)=-T\), and a kernel
whose two nonzero weights agree.  Then \(E(M)=0\) while the off-zero energy is
\(2T^2\).  A scalar payment for \(E(M)\) cannot be promoted to a mean-square
payment for \(M\).

The selected order is therefore

```text
B: direct collapsed compensated prime-frame covariance with delta>1/400
  -> A: terminal q-local signed covariance
  -> C: distinguished-seed dynamics reserve.
```

The V32 quotient-oscillation theorem remains a valid stronger alternative,
not the selected first theorem after V34.

## 8. Primary-source boundary

The screen is primary-source-only and fail-closed as of 2026-08-08.

1. Bettin--Chandee,
   [arXiv:1502.00769](https://arxiv.org/abs/1502.00769), supplies the
   trilinear Kloosterman-fraction engine already compiled in V29.  It pays
   (3.3), not the physical covariance (4.5).
2. Bazin,
   [arXiv:2607.15137v1](https://arxiv.org/abs/2607.15137v1), Theorem 8,
   accepts the collapsed marginal and proves (6.2).  It does not accept the
   second physical factor or prove a joint signed prime-frame covariance.
3. Matomäki--Radziwiłł--Tao,
   [arXiv:1707.01315v3](https://arxiv.org/abs/1707.01315v3), Proposition
   3.1, is an abstract shift-energy reduction.  Its applied coefficient
   classes and logarithmic almost-all-shift outputs do not imply (5.1).
4. Evans,
   [arXiv:2102.12297v3](https://arxiv.org/abs/2102.12297v3), Theorem 1.4,
   treats a fixed prime--\(E_2\) correlation for almost all shifts with a
   logarithmic mean-square scale.  It has neither the coefficient (2.2) nor
   the compensated frame (4.5).
5. Matomäki--Radziwiłł--Shao--Tao--Teräväinen,
   [arXiv:2411.05770v2](https://arxiv.org/abs/2411.05770v2), Theorem 1.5,
   gives a density-one shift statement without the quantitative all-frame
   power needed in (5.1).

No direct source attachment to (5.1) was found.  The arithmetic advance
therefore remains `NO`.

## 9. Exact finite fixtures

The checker freezes seven independent boundaries.

1. For every shell integer with \(8\leq x\leq320\), it verifies (2.2),
   (2.3), and the strict upper-cutoff inequality.  This is 25,744 cases,
   including 4,945 prime rows, 13,824 nonzero proper-tail rows, and 44,205
   nonzero proper-tail terms.
2. For prime \(q=5\), the vector \(c_5(h)\), \(0\leq h<5\), is
   \((4,-1,-1,-1,-1)\), and equals
   \(\sum_{a=1}^{4}e_5(ah)\).
3. On a ten-point rational fixture with \(\mathcal Q=\{5,7\}\), the
   \(h\)-form, dilation form, and pair form of \(\mathfrak D\) all equal
   \(-6061/315\).
4. The same prime-frame normalization is \(L_{\rm pr}=10\), so
   \(E(r)=6061/3150\).
5. With \(M(1)=3\), \(M(2)=-3\), and the normalized \(c_5\) kernel,
   \(E(M)=0\) but the off-zero energy is \(18\).  This rejects the illegal
   promotion of the paid scalar carrier to \(Q^{\rm osc}(P)\).
6. Taking \(\delta=1/300\) gives
   \(\delta-1/400=1/1200\), while the independent local-carrier margin is
   \(121/9600\).  The combined admissible margin is therefore strictly below
   \(1/1200\).
7. At \(Q=x^{1/3}\) and \(\vartheta=x^{-21/32}\), it recomputes the four
   Bazin exponents and the exact additive exponent \(75/64\).

Finite fixtures prove identities and type boundaries only.  They do not
estimate the growing arithmetic covariance.

## 10. Canonical registry and next theorem

```text
V34_MAXIMUM_CLAIM = EXACT_PAID_LOCAL_CARRIER_ELIMINATION_TO_COLLAPSED_COMPENSATED_PRIME_FRAME_COVARIANCE_WITH_STRICT_DELTA_GT_1_OVER_400_GATE
V34_ROUTE_ADVANCE = YES
V34_ARITHMETIC_ADVANCE = NO
V34_FIXED_ATOM_CREDIT = 0
V34_STRICT_1_OVER_400 = UNPAID
V34_L2 = NONE
V34_TPC_207_TRIGGER = false
V34_NUMBERED_RELEASE = NO
V34_SELECTED_RESEARCH_ROUTE = B_DIRECT_COLLAPSED_PRIME_FRAME_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK
V34_BETA_MASTER_MARGINAL = RETAINED_EXACT_V33_LAMBDA_OVER_LOG_MINUS_TRUNCATED_MU_CONV_ONE
V34_BETA_LARGE_DIVISOR_TAIL = PROVED_EXACT_LAMBDA_OVER_LOG_PLUS_MU_ABOVE_CUTOFF
V34_PRIME_DELETED_ENDPOINT = PROVED_EXACT_RHO_EQUALS_LAMBDA_OVER_LOG_PLUS_MU_AND_RHO_P_EQUALS_ZERO
V34_GENUINE_BILINEAR_TAIL = PROVED_EXACT_K_GE_2_D_ABOVE_CUTOFF
V34_LOCAL_CARRIER_E_PAYMENT = RETAINED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1
V34_LOCAL_CARRIER_J_PAYMENT = RETAINED_SOURCE_BACKED_X_1891_OVER_1920_PLUS_O1
V34_DIRECT_SCALAR_ELIMINATION = PROVED_EXACT_E_OF_E_EQUALS_E_OF_R_MINUS_E_OF_MLOC
V34_OCCURRENCE_LABEL_IN_NEW_B_THEOREM = REMOVED_BY_SEPARATELY_PAID_SCALAR_LOCAL_CARRIER
V34_QOSC_P_REPLACEMENT = STOP_SCOPED_REINTRODUCES_LARGE_OFFZERO_LOCAL_MAIN
V34_V32_QOSC_P_MINUS_L = RETAINED_VALID_STRONGER_ALTERNATIVE
V34_RAMANUJAN_PRIME_VECTOR = PROVED_EXACT_C_Q_EQUALS_Q_DIVISIBILITY_MINUS_ONE
V34_ZERO_DELETED_SMOOTH_CORRELATION = PROVED_EXACT_PHI_H
V34_COMPENSATED_DILATION_FORM = PROVED_EXACT_QK_MINUS_ALL_H
V34_COMPENSATED_PAIR_FORM = PROVED_EXACT_ONE_OUTER_SIGNED_SCALAR
V34_L_PR_NORMALIZATION = X_POWER_2_OVER_3_PLUS_O1
V34_DIRECT_NUMERATOR_TARGET = X_POWER_5_OVER_3_MINUS_DELTA_PLUS_O1
V34_REQUIRED_DELTA = STRICTLY_GREATER_THAN_1_OVER_400
V34_DIRECT_E_R_EXPONENT = X_POWER_1_MINUS_DELTA_PLUS_O1
V34_DIRECT_ENDPOINT_MARGIN = DELTA_MINUS_1_OVER_400
V34_LOCAL_CARRIER_ENDPOINT_MARGIN = 121_OVER_9600
V34_COMBINED_B_MARGIN = MIN_DELTA_MINUS_1_OVER_400_AND_121_OVER_9600
V34_BAZIN_ACTUAL_FRAME_Q = X_POWER_1_OVER_3
V34_BAZIN_ACTUAL_FRAME_THETA = X_POWER_MINUS_21_OVER_32
V34_BAZIN_ACTUAL_FRAME_XI_EXPONENT = 257_OVER_192
V34_BAZIN_ACTUAL_FRAME_ADDITIVE_EXPONENT = 75_OVER_64
V34_BAZIN_TO_DIRECT_COVARIANCE = STOP_SCOPED_ONE_MARGINAL_NO_PHYSICAL_PRODUCT
V34_MRT_TO_DIRECT_COVARIANCE = STOP_SCOPED_LOGARITHMIC_SHIFT_ENERGY_WRONG_COEFFICIENT_AND_FRAME
V34_EVANS_TO_DIRECT_COVARIANCE = STOP_SCOPED_FIXED_E2_ALMOST_ALL_SHIFTS_WRONG_COEFFICIENT
V34_MRSTT_TO_DIRECT_COVARIANCE = STOP_SCOPED_DENSITY_ONE_NO_QUANTITATIVE_FRAME_POWER
V34_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V34_NEXT_THEOREM = DELTA_GT_1_OVER_400_POWER_SAVING_FOR_COLLAPSED_SIEVE_REMAINDER_TIMES_PHYSICAL_HYBRID_IN_COMPENSATED_PRIME_FRAME
V34_FIRST_FATAL = NO_POWER_SAVING_BEYOND_X_5_OVER_3_FOR_COLLAPSED_PHYSICAL_COMPENSATED_PRIME_FRAME
V34_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
V34_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
```

V34 removes the occurrence-native carrier from the **statement of the new B
theorem**, because its scalar contribution is already paid.  It does not pay
the new covariance, the terminal zero axis, or any fixed-atom arithmetic
credit.
