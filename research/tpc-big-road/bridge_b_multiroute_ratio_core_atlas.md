# Bridge A / Gate B V36: a multiroute atlas for the ratio core

Status:

```text
UNNUMBERED_BIG_ROAD_CHECKPOINT
DERIVATION_STATUS = COHERENT_AFTER_REFRAMING_AND_EXPLICIT_EXTRA_ASSUMPTIONS
ROUTE_ADVANCE = YES
CONDITIONAL_BRIDGE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
NUMBERED_RELEASE = NO
```

V36 adopts a bridge-network policy.  It does not require one speculative
method to carry the whole proof.  Instead it gives three independently
sufficient routes from the same V35 ratio core to the off-zero analytic gate.
Every unproved input is labelled `CONJECTURE`; source-backed local estimates,
exact identities, and heuristic benchmarks are kept in different ledgers.

The new exact step is that the V35 proper-factor array may be re-collapsed
*after* the nonunit and principal rows have been paid.  The surviving object
is therefore a binary off-diagonal hybrid character covariance.  The
proper-factor expansion remains available to any transform that needs it, but
it is no longer compulsory at theorem-input level.

## 1. Target, invariant object, and non-claims

Keep the V35 parameters

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad H=x^{21/32},\qquad
 Q=x^{1/3},
 \tag{1.1}
\]

\[
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},\qquad
 L_{\rm pr}=\sum_{q\in\mathcal Q}(q-1)=x^{2/3+o(1)},
 \tag{1.2}
\]

and

\[
 \beta(t)=\beta_x^{\rm raw}(t),\qquad
 w(u)=\Lambda(u+2)-b_x^{(z)}(u),\qquad
 K_H(h)=\widehat\psi_+(h/H).
 \tag{1.3}
\]

The invariant object is the V35 centered coprime core

\[
 \mathfrak C_x=
 \sum_{q\in\mathcal Q}q
 \sum_{\substack{dk,u\in I_x\\d,k\geq2,\ u\ne dk\\q\nmid dku}}
 \mu(d)\omega_x(d,k)w(u)K_H(u-dk)
 u_1(u\overline{dk};q).
 \tag{1.4}
\]

V35 proved

\[
 \mathfrak D_x=\mathfrak C_x+\mathfrak P_x+\mathfrak N_x,
 \qquad
 |\mathfrak P_x|+|\mathfrak N_x|\ll x^{53/32+o(1)}.
 \tag{1.5}
\]

Thus any estimate

\[
 |\mathfrak C_x|\ll x^{5/3-\delta+o(1)},
 \qquad \delta>1/400,
 \tag{1.6}
\]

pays the current off-zero B gate.  V36 does not prove (1.6), does not pay the
terminal zero coordinate, and does not move the distinguished-seed dynamics
reserve.

## 2. Exact re-collapse to a binary ratio covariance

V35 established the proper-factor identity

\[
 \beta(t)=
 \sum_{\substack{dk=t\\d,k\geq2}}\mu(d)\omega_x(d,k).
 \tag{2.1}
\]

For prime \(q\), the conditions \(q\nmid dku\) and \(q\nmid tu\) are equivalent
when \(t=dk\).  Hence summing (1.4) first over the proper-factor occurrences
gives the exact binary form

\[
 \boxed{
 \mathfrak C_x=
 \sum_{q\in\mathcal Q}q
 \sum_{\substack{t,u\in I_x\\t\ne u\\q\nmid tu}}
 \beta(t)w(u)K_H(u-t)u_1(u\bar t;q).}
 \tag{2.2}
\]

This is not a replacement of the literal coefficient by a divisor envelope.
The full signed proper-factor coefficient has already been summed exactly into
the same \(\beta(t)\).  A future theorem may use either (1.4) or (2.2), but it
may not mix their normalizations or count the two representations twice.

Equation (2.2) is the first V36 route advance.  It removes the claim that every
source interface must accept three independent arrays.  The remaining typing
obstruction is sharper: a theorem must accept the *joint* additive-short and
multiplicative-ratio geometry, with the diagonal deleted.

## 3. Exact hybrid character normal form

Use

\[
 \widehat\psi_+(y)=\int_{\mathbb R}\psi_+(v)e(-vy)\,dv,
 \qquad \int_{\mathbb R}\psi_+(v)\,dv=1.
 \tag{3.1}
\]

For \(q\in\mathcal Q\) and nonprincipal \(\chi\pmod q\), define

\[
 B_{q,\chi}(v)=
 \sum_{\substack{t\in I_x\\q\nmid t}}
 \beta(t)\overline{\chi(t)}e(vt/H),
 \tag{3.2}
\]

\[
 W_{q,\chi}(v)=
 \sum_{\substack{u\in I_x\\q\nmid u}}
 w(u)\chi(u)e(-vu/H),
 \qquad
 Z_q=\sum_{\substack{t\in I_x\\q\nmid t}}\beta(t)w(t).
 \tag{3.3}
\]

Character orthogonality and the explicit subtraction of \(u=t\) give

\[
 \boxed{
 \mathfrak C_x=
 \int_{\mathbb R}\psi_+(v)
 \sum_{q\in\mathcal Q}\frac q{q-1}
 \sum_{\substack{\chi\ ({\rm mod}\ q)\\\chi\ne\chi_0}}
 \bigl(B_{q,\chi}(v)W_{q,\chi}(v)-Z_q\bigr)\,dv.}
 \tag{3.4}
\]

The term \(Z_q\) is compulsory.  Dropping it restores the V35 core diagonal,
whose absolute scale is \(x^{5/3+o(1)}\).  Formula (3.4) is a binary spectral
normal form, not a proof of decorrelation.

## 4. Route E: whole-object additive energy

Let

\[
 r_x(h)=\sum_{\substack{t,t+h\in I_x}}\beta(t)w(t+h),
 \qquad
 A_Q(h)=\sum_{q\in\mathcal Q}\bigl(q\mathbf1_{q\mid h}-1\bigr).
 \tag{4.1}
\]

V27--V34 give the exact additive form and pay the occurrence-native local
carrier.  The remaining sufficient energy hypothesis is

\[
 \boxed{\mathsf H_E(\sigma):\quad
 \left(\sum_{h\ne0}|K_H(h)|\,|e_x(h)|^2\right)^{1/2}
 \ll x^{1+\sigma+o(1)},
 \qquad \sigma<13/4800,}
 \tag{4.2}
\]

where \(e_x=r_x-M_x^{\rm loc}\) is the same tagged residual as in V27--V32.
This is an `OPEN_CONJECTURE`, not a theorem assertion.

The prime-shell multiplier has weighted norm

\[
 \left(\sum_{h\ne0}|K_H(h)|A_Q(h)^2\right)^{1/2}
 =x^{127/192+o(1)}.
 \tag{4.3}
\]

Consequently (4.2) gives numerator exponent

\[
 \frac{127}{192}+1+\sigma
 =\frac{319}{192}+\sigma
 =\frac53-\left(\frac1{192}-\sigma\right).
 \tag{4.4}
\]

Thus

\[
 \delta_E=\frac1{192}-\sigma,
 \qquad
 \delta_E-\frac1{400}=\frac{13}{4800}-\sigma>0.
 \tag{4.5}
\]

Route E is exact as a conditional compiler.  Its unresolved input is the
literal arithmetic estimate (4.2).

## 5. Route K: collective determinant compiler plus a local source engine

The V35 raw positive/compensating triangle has exponent

\[
 x^{191/96+o(1)}.
 \tag{5.1}
\]

Writing \(u-dk=\ell q\), the shift variable has length

\[
 |\ell|\ll H/Q=x^{31/96}=Q^{31/32}.
 \tag{5.2}
\]

This identifies the exact structural loss.  A fixed-\(q\), fixed-\(\ell\)
triangle cannot reach the endpoint.  The proposed construction bridge is the
following explicitly conjectural compiler.

\[
 \boxed{\mathsf H_{K0}:\quad
 \text{the signed }(q,\ell)\text{ family is emitted and reassembled
 collectively with gain }Q^{-31/32},}
 \tag{5.3}
\]

leaving a balanced Kloosterman-cell baseline \(x^{5/3+o(1)}\).  The compiler
must preserve the prime shell, physical \(w\), zero deletion, proper-factor
signs, and one outer absolute value.  It is not currently proved.

Once (5.3) has produced balanced cells, Blomer--Pascadi's fixed-modulus
bilinear Kloosterman theorem supplies a source-backed saving \(q^{-1/32}\) in
the critical square-root range.  Since \(q\asymp Q=x^{1/3}\), this is

\[
 Q^{-1/32}=x^{-1/96}.
 \tag{5.4}
\]

The proposed (31+1) exponent split is therefore

\[
 Q^{-31/32}\cdot Q^{-1/32}=Q^{-1}=x^{-1/3},
 \tag{5.5}
\]

and the conditional output is

\[
 \boxed{|\mathfrak C_x|\ll x^{5/3-1/96+o(1)}=x^{53/32+o(1)}.}
 \tag{5.6}
\]

Thus \(\delta_K=1/96\), and

\[
 \delta_K-1/400=19/2400.
 \tag{5.7}
\]

Only the \(q^{-1/32}\) cell estimate in this route is source-backed.  The much
larger \(Q^{-31/32}\) collective compiler (5.3), including its coefficient
norms and reassembly, is the hard conjectural bridge pier.

## 6. Route X: joint hybrid-character decoupling

Define the stronger spectral majorant

\[
 \mathcal H_\chi=
 \int_{\mathbb R}|\psi_+(v)|
 \left|
 \sum_{q\in\mathcal Q}\frac q{q-1}
 \sum_{\chi\ne\chi_0}
 \bigl(B_{q,\chi}(v)W_{q,\chi}(v)-Z_q\bigr)
 \right|\,dv.
 \tag{6.1}
\]

By (3.4), \(|\mathfrak C_x|\leq\mathcal H_\chi\).  The character bridge
hypothesis is

\[
 \boxed{\mathsf H_\chi(\kappa):\quad
 \mathcal H_\chi\ll x^{2-\kappa+o(1)},
 \qquad \kappa>\frac{403}{1200}.}
 \tag{6.2}
\]

Indeed,

\[
 2-\kappa=\frac53-\delta_\chi,
 \qquad
 \delta_\chi=\kappa-\frac13,
 \tag{6.3}
\]

and \(\delta_\chi>1/400\) is exactly

\[
 \kappa>\frac13+\frac1{400}=\frac{403}{1200}.
 \tag{6.4}
\]

Applying the multiplicative large sieve separately to \(B_{q,\chi}\) and
\(W_{q,\chi}\), followed by Cauchy, gives only the \(x^{2+o(1)}\) baseline.
It corresponds to \(\kappa=0\) and misses the strict target by \(403/1200\).
Route X therefore requires a *joint centered covariance theorem*; two marginal
large-sieve bounds are not enough.

## 7. One-of-three compiler and downstream ledger

The three inputs are alternatives:

\[
 \boxed{
 \mathsf H_E(\sigma)\quad\mathbf{OR}\quad
 \mathsf H_{K0}+\text{BP cell saving}\quad\mathbf{OR}\quad
 \mathsf H_\chi(\kappa).}
 \tag{7.1}
\]

If any one holds with its strict parameter range, then (1.6) follows.  The
available B saving may be chosen as follows:

\[
 0<\eta_B<
 \begin{cases}
 \min\{13/4800-\sigma,\ 19/2400,\ 121/9600\},&\mathsf H_E,\\
 19/2400,&\mathsf H_{K0}+\text{BP},\\
 \min\{\kappa-403/1200,\ 19/2400,\ 121/9600\},&\mathsf H_\chi.
 \end{cases}
 \tag{7.2}
\]

The middle line uses

\[
 \min\{1/96-1/400,19/2400,121/9600\}=19/2400.
 \tag{7.3}
\]

Closing B does not close the theorem.  V29's exact identity leaves the terminal
q-local signed covariance A, which is terminal-equivalent to the physical
scalar once the off-zero error is paid.  The dynamics distinguished-seed route
C remains a separate reserve.  V36 records these as downstream open bridges,
not as consequences of the three conjectures above.

## 8. Heuristic benchmark and adversarial firewalls

For orientation only, suppose occurrence signs and physical residual values
behave as independent centered variables of unit variance.  For one prime
\(q\asymp Q\), the congruent part has about \(xH/q\) terms of size \(q\), hence
variance \(qxH\).  Summing independently over the prime shell predicts standard
deviation

\[
 Q\sqrt{xH}=x^{1/3+53/64}=x^{223/192+o(1)}.
 \tag{8.1}
\]

This is below \(x^{5/3}\) by

\[
 \frac53-\frac{223}{192}=\frac{97}{192}.
 \tag{8.2}
\]

Equation (8.1) is a `HEURISTIC_RANDOM_PHASE_BENCHMARK`, not evidence about
Möbius or primes.  It only says that the required fixed saving is compatible
with a random-sign model.

The following shortcuts remain forbidden:

1. separate marginal \(L^2\) bounds do not imply joint covariance saving;
2. restoring \(u=t\) inserts the unpaid diagonal;
3. applying a fixed-\(q\) theorem and triangulating over \((q,\ell)\) loses the
   \(Q^{-31/32}\) structural gain in (5.3);
4. replacing \(w\) by a divisor envelope changes the theorem object;
5. a heuristic, numerical fixture, or source analogy cannot set
   `ARITHMETIC_ADVANCE=YES`.

The fixed-\(q\) route would need nearly the whole shift-length saving

\[
 Q^{-31/32-3\delta},
 \tag{8.3}
\]

before summing moduli.  A local \(Q^{-1/32}\) estimate alone is therefore not
the missing theorem.

## 9. Primary-source matrix and route ranking

1. **Matomäki--Radziwiłł--Tao.**  Proposition 3.1 gives the abstract
   measurable-major energy reduction used upstream by Route E, but does not
   prove the literal \(\beta\times w\) residual estimate (4.2):
   [arXiv:1707.01315v3](https://arxiv.org/abs/1707.01315).
2. **Blomer--Pascadi.**  Their Theorem 1.1 and Theorem 5.5 bound fixed-modulus
   bilinear Kloosterman sums with arbitrary outer sequences; in the critical
   square-root range the saving is \(c^{-1/32}\).  This supports only the cell
   engine (5.4), not the conjectural emitter/reassembly (5.3):
   [arXiv:2607.24311](https://arxiv.org/abs/2607.24311).
3. **Fouvry--Shparlinski--Xi.**  Theorems 2.5 and 2.7 give power-saving
   trilinear/quadrilinear character sums for one fixed prime modulus and
   specified cross-weight types.  Their variables lie below the modulus and
   their weights do not encode the literal long-shell
   \(w(dk+h)\mu(d)\omega(d,k)\), zero deletion, and collective prime-modulus
   reassembly simultaneously:
   [arXiv:2404.09295v4](https://arxiv.org/pdf/2404.09295).
4. **Dong--Robles--Zeindler.**  Their improved bilinear Kloosterman-fraction
   bounds accept arbitrary two-array coefficients, but remain fixed bilinear
   fraction forms rather than the V36 joint ratio/additive covariance:
   [arXiv:2601.00292](https://arxiv.org/abs/2601.00292).
5. **Runbo Li.**  The large-modulus arithmetic-progression results use
   Harman-sieve prime majorants/minorants and special bilinear/trilinear modulus
   forms; they do not attach to the signed \(\beta\times w\) covariance:
   [arXiv:2602.20917](https://arxiv.org/abs/2602.20917).

No checked source proves any of \(\mathsf H_E\), \(\mathsf H_{K0}\), or
\(\mathsf H_\chi\) for the literal object.  The recommended research ranking is:

```text
1. Route K: construct the collective Q^(-31/32) emitter/reassembly;
2. Route E: seek a whole-residual power mean square with sigma<13/4800;
3. Route X: use the binary spectral form as a new-theorem interface;
4. terminal A and dynamics C remain explicitly downstream/reserve.
```

Route K ranks first because it already has a source-backed final \(1/32\) cell
gain.  Route E is algebraically shortest.  Route X is the cleanest binary
statement but currently lacks a joint-decoupling source.

## 10. Finite fixtures and canonical registry

The checker freezes an exact rational occurrence fixture with four collapsed
values

\[
 \beta(6)=\frac12,\qquad \beta(8)=-\frac13,
 \qquad \beta(9)=2,\qquad \beta(10)=\frac13.
 \tag{10.1}
\]

For \(q=5,7\), rational physical weights, and
\(K(h)=(1+|h|)^{-1}\), it verifies all three exact evaluations

\[
 \mathfrak C_{\rm occurrence}
 =\mathfrak C_{\rm binary}
 =\mathfrak C_{\rm character}
 =-\frac{2257}{432}.
 \tag{10.2}
\]

The character evaluation includes the diagonal in the product and subtracts
it explicitly.  It also freezes the exponent identities (4.4)--(8.3), an
aligned-vector witness showing saturation of marginal Cauchy, and the logical
`OR` compiler.

```text
V36_MAXIMUM_CLAIM = EXACT_PROPER_FACTOR_RECOLLAPSE_TO_BINARY_OFF_DIAGONAL_HYBRID_CHARACTER_COVARIANCE_PLUS_ONE_OF_THREE_CONDITIONAL_GATE_B_COMPILER_AND_EXPLICIT_HEURISTIC_CHARTER
V36_ROUTE_ADVANCE = YES
V36_CONDITIONAL_BRIDGE_ADVANCE = YES
V36_ARITHMETIC_ADVANCE = NO
V36_FIXED_ATOM_CREDIT = 0
V36_STRICT_1_OVER_400 = UNPAID
V36_L2 = NONE
V36_TPC_207_TRIGGER = false
V36_NUMBERED_RELEASE = NO
V36_DERIVATION_STATUS = COHERENT_AFTER_REFRAMING_AND_EXPLICIT_EXTRA_ASSUMPTIONS
V36_ASSUMPTION_POLICY = CONJECTURES_EXPLICIT_AND_NEVER_PROMOTED_TO_THEOREMS
V36_SELECTED_RESEARCH_ROUTE = K_COLLECTIVE_COMPILER_FIRST__E_ENERGY_SECOND__X_CHARACTER_THIRD__A_TERMINAL_AFTER_B__C_DYNAMICS_RESERVE
V36_V35_CORE = RETAINED_EXACT_PRIME_ONLY_ZERO_DELETED_COPRIME_RATIO_CORE
V36_PROPER_FACTOR_RECOLLAPSE = PROVED_EXACT_SUM_OCCURRENCES_BACK_TO_BETA_OF_T
V36_BINARY_RATIO_CORE = PROVED_EXACT_TWO_ARRAY_OFF_DIAGONAL_FORM
V36_HYBRID_CHARACTER_INVERSION = PROVED_EXACT_FOURIER_CHARACTER_NORMAL_FORM
V36_CHARACTER_DIAGONAL_SUBTRACTION = PROVED_EXACT_Z_Q_REQUIRED
V36_ONE_OF_THREE_COMPILER = PROVED_EXACT_CONDITIONAL_OR_GATE
V36_ROUTE_E_STATUS = OPEN_CONJECTURE_WHOLE_OBJECT_WEIGHTED_RESIDUAL_ENERGY
V36_ROUTE_E_INPUT = N_E_LE_X_POWER_1_PLUS_SIGMA_WITH_SIGMA_LT_13_OVER_4800
V36_ROUTE_E_DELTA = 1_OVER_192_MINUS_SIGMA
V36_ROUTE_E_ENDPOINT_MARGIN = 13_OVER_4800_MINUS_SIGMA
V36_ROUTE_K0_STATUS = OPEN_CONJECTURE_COLLECTIVE_Q_ELL_EMITTER_AND_REASSEMBLY
V36_ROUTE_K0_STRUCTURAL_GAIN = Q_POWER_MINUS_31_OVER_32
V36_ROUTE_K1_STATUS = SOURCE_BACKED_FIXED_MODULUS_CELL_ENGINE_AFTER_EXACT_EMISSION
V36_ROUTE_K1_CELL_GAIN = Q_POWER_MINUS_1_OVER_32
V36_ROUTE_K_TOTAL_GAIN = Q_POWER_MINUS_1_EQUALS_X_POWER_MINUS_1_OVER_3
V36_ROUTE_K_DELTA = 1_OVER_96
V36_ROUTE_K_ENDPOINT_MARGIN = 19_OVER_2400
V36_ROUTE_X_STATUS = OPEN_CONJECTURE_JOINT_HYBRID_CHARACTER_DECOUPLING
V36_ROUTE_X_BASELINE = X_POWER_2_PLUS_O1_FROM_SEPARATE_LARGE_SIEVE_CAUCHY
V36_ROUTE_X_REQUIRED_KAPPA = STRICTLY_GREATER_THAN_403_OVER_1200
V36_ROUTE_X_DELTA = KAPPA_MINUS_1_OVER_3
V36_ROUTE_X_ENDPOINT_MARGIN = KAPPA_MINUS_403_OVER_1200
V36_RANDOM_PHASE_BENCHMARK = HEURISTIC_ONLY_X_POWER_223_OVER_192
V36_RANDOM_PHASE_GAP_TO_X_5_OVER_3 = 97_OVER_192
V36_SEPARATE_MARGINAL_LARGE_SIEVE = STOP_SCOPED_X_POWER_2_DEFICIT_403_OVER_1200
V36_FIXED_Q_TRIANGLE = STOP_SCOPED_REQUIRES_Q_POWER_MINUS_31_OVER_32_MINUS_3_DELTA_BEFORE_MODULUS_SUM
V36_BLOMER_PASCADI_CELL_ENGINE = SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_AT_CRITICAL_FIXED_MODULUS_RANGE
V36_BLOMER_PASCADI_DIRECT_ATTACHMENT = STOP_SCOPED_NO_COLLECTIVE_Q_ELL_EMITTER_COEFFICIENT_COMPILER_OR_REASSEMBLY
V36_FOUVRY_SHPARLINSKI_XI_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_PRIME_SHORT_VARIABLES_WRONG_CROSS_WEIGHT_AND_NO_MODULUS_REASSEMBLY
V36_DONG_ROBLES_ZEINDLER_DIRECT_ATTACHMENT = STOP_SCOPED_FIXED_BILINEAR_FRACTION_NO_PHYSICAL_JOINT_COVARIANCE
V36_RUNBO_LI_DIRECT_ATTACHMENT = STOP_SCOPED_SPECIAL_HARMAN_MAJORANTS_AND_MODULUS_FORMS_WRONG_SIGNED_OBJECT
V36_TERMINAL_A = OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B
V36_DYNAMICS_C = RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN
V36_HEURISTIC_DOES_NOT_IMPLY_ARITHMETIC_ADVANCE = PROVED_STATUS_FIREWALL
V36_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V36_NEXT_THEOREM = COLLECTIVE_Q_POWER_MINUS_31_OVER_32_DETERMINANT_EMITTER_OR_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800_OR_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200
V36_FIRST_FATAL = NO_LITERAL_THEOREM_SUPPLIES_ANY_ONE_OF_THE_THREE_CONJECTURAL_BRIDGE_INPUTS
V36_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_THREE_CONDITIONAL_LANES_MARKED
V36_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
```

The map position is still the red crossing at Bridge A / Gate B.  The advance
is that the crossing now has three separately typed lanes and exact toll
ledgers.  None is yet an arithmetic crossing.
