# Bridge A / Gate B V37: a loss-budgeted shift-packet compiler

Status:

```text
UNNUMBERED_BIG_ROAD_CHECKPOINT
DERIVATION_STATUS = COHERENT_AFTER_EXACT_PACKETIZATION_AND_LOSS_BUDGETING
ROUTE_ADVANCE = YES
CONDITIONAL_BRIDGE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
NUMBERED_RELEASE = NO
```

V36 ranked Route K first but formulated its hard pier as a lossless
\(Q^{-31/32}\) collective compiler.  V37 replaces that single all-or-nothing
sentence by an exact centered-residue packet, a source-native Kloosterman-cell
budget, and a strict loss window.  The resulting theorem target may lose a
factor \(Q^\omega\), provided

\[
 \boxed{\omega<\frac{19}{800}.}
 \tag{0.1}
\]

This is a genuine relaxation of the V36 conjecture.  It is still an open
arithmetic theorem: no checked source constructs the required packet emitter.
The local Blomer--Pascadi cell saving remains source-backed only after that
emission has been proved.

## 1. Research question, assumptions, and invariant object

Keep the V36 data

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad H=x^{21/32},\qquad Q=x^{1/3},
 \tag{1.1}
\]

\[
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},\qquad
 \beta(t)=\beta_x^{\rm raw}(t),\qquad
 w(u)=\Lambda(u+2)-b_x^{(z)}(u),
 \tag{1.2}
\]

and

\[
 K_H(h)=\widehat\psi_+(h/H),\qquad
 u_1(a;q)=\mathbf1_{a\equiv1\ ({\rm mod}\ q)}-\frac1{q-1}.
 \tag{1.3}
\]

The invariant object is the exact V36 binary, off-diagonal, coprime ratio
core

\[
 \boxed{
 \mathfrak C_x=
 \sum_{q\in\mathcal Q}q
 \sum_{\substack{t,u\in I_x\\t\ne u,\ q\nmid tu}}
 \beta(t)w(u)K_H(u-t)u_1(u\bar t;q).}
 \tag{1.4}
\]

V35--V36 already proved

\[
 \mathfrak D_x=\mathfrak C_x+\mathfrak P_x+\mathfrak N_x,
 \qquad
 |\mathfrak P_x|+|\mathfrak N_x|\ll x^{53/32+o(1)}.
 \tag{1.5}
\]

The research question is therefore:

> Can (1.4) be emitted, exactly once and without a per-shift triangle, into
> balanced fixed-modulus Kloosterman cells whose aggregate source-native
> trivial norm costs at most \(Q^\omega\) beyond the ideal packet scale?

The derivation map is

```text
V36 binary ratio core
  -> exact centered residue packets
  -> short shift chains of occupancy H/Q
  -> conjectural exactly-once balanced BP-cell emitter with Q^omega overhead
  -> source-backed BP q^(-1/32) cell saving
  -> strict endpoint if and only if omega<19/800.
```

All divisor envelopes, short-tail payments, and source applications use the
same physical \(\beta,w,K_H\).  The only new hypothesis is the packet emitter
in Section 4.  It is declared before its desired conclusion and is not inferred
from any finite fixture.

## 2. Exact centered-residue packetization

Fix \(q\in\mathcal Q\) and \(t\in I_x\) with \(q\nmid t\).  Put

\[
 \mathcal B_{q,t}=(\mathbb Z/q\mathbb Z)\setminus\{-t\},
 \tag{2.1}
\]

and, for \(b\in\mathcal B_{q,t}\), define the physical shift-chain packet

\[
 F_{q,t}(b)=
 \sum_{\substack{u\in I_x\\u\ne t\\u-t\equiv b\ ({\rm mod}\ q)}}
 w(u)K_H(u-t).
 \tag{2.2}
\]

The map

\[
 a\longmapsto b=(a-1)t
 \tag{2.3}
\]

is a bijection from \((\mathbb Z/q\mathbb Z)^\times\) to
\(\mathcal B_{q,t}\).  The distinguished ratio \(a=1\) maps to \(b=0\).
Consequently (1.4) is exactly

\[
 \boxed{
 \mathfrak C_x=
 \sum_{q\in\mathcal Q}q
 \sum_{\substack{t\in I_x\\q\nmid t}}
 \beta(t)
 \left(
 F_{q,t}(0)-\frac1{q-1}
 \sum_{b\in\mathcal B_{q,t}}F_{q,t}(b)
 \right).}
 \tag{2.4}
\]

This formula carries two non-negotiable details.

First, the deleted physical diagonal occurs only in the \(b=0\) chain:

\[
 u=t+\ell q,\qquad \ell\ne0.
 \tag{2.5}
\]

Second, the compensating background is the average over every
\(b\ne-t\), not merely over the congruent chain.  In particular a constant
packet is annihilated:

\[
 F_{q,t}(b)\equiv c
 \quad\Longrightarrow\quad
 F_{q,t}(0)-\frac1{q-1}\sum_bF_{q,t}(b)=0.
 \tag{2.6}
\]

Equations (2.1)--(2.6) are exact \(L0\) identities.  They do not assert
cancellation inside a physical packet.

## 3. Occupancy and the precise triangle loss

For a representative \(\widetilde b\) of \(b\), the rows in (2.2) have

\[
 u-t=\widetilde b+\ell q.
 \tag{3.1}
\]

Since \(K_H\) is Schwartz,

\[
 |K_H(h)|\ll_{A,\psi}(1+|h|/H)^{-A}.
 \tag{3.2}
\]

The frozen V35 divisor envelopes give
\(\sum_{t\in I_x}|\beta(t)|\ll x^{1+o(1)}\) and a polynomial total envelope
for \(w\), while the prime shell and the outer factor \(q\) also have only
fixed-power mass.  Hence, for every prescribed \(B>0\), choosing \(A\) in
(3.2) in terms of \(B/\varepsilon\) makes the rows
\(|h|>Hx^\varepsilon\) contribute \(O_B(x^{-B})\).  After this truncation,
each residue chain has effective occupancy

\[
 L=\frac HQ=x^{31/96}=Q^{31/32}.
 \tag{3.3}
\]

Taking absolute values first in the distinguished term and in the compensating
average gives, per \(q\), the scale \(xH\).  Summing the prime shell gives

\[
 xHQ=x^{191/96+o(1)}.
 \tag{3.4}
\]

The difference between (3.4) and the balanced pre-cell scale is exactly

\[
 x^{191/96}L^{-1}=x^{5/3}.
 \tag{3.5}
\]

Thus \(L^{-1}=Q^{-31/32}\) is not being postulated as random-sign
cancellation.  It records the full cost of the forbidden per-\(\ell\)
triangle.  A successful compiler must estimate the joint packet before that
triangle is taken.

## 4. The loss-budgeted packet-emitter hypothesis

For prime \(q\), call a cell BP-admissible if it has the form

\[
 \mathcal K_{\nu,q}=
 \sum_{\substack{m\in\mathcal I_{\nu,q},\ n\in\mathcal J_{\nu,q}\\
                  (m,n,q)=1}}
 \alpha_{\nu,q}(m)\gamma_{\nu,q}(n)
 S(a_{\nu,q}m,n;q),
 \tag{4.1}
\]

where \(a_{\nu,q}\in(\mathbb Z/q\mathbb Z)^\times\), the two intervals have
lengths

\[
 |\mathcal I_{\nu,q}|,|\mathcal J_{\nu,q}|\asymp q^{1/2},
 \tag{4.2}
\]

and every scalar prefactor is absorbed into one of the two coefficient arrays.
Define its source-native critical trivial scale by

\[
 \mathcal T_{\nu,q}=q
 \|\alpha_{\nu,q}\|_2\|\gamma_{\nu,q}\|_2.
 \tag{4.3}
\]

For \(\omega\geq0\), the V37 construction hypothesis is:

\[
 \boxed{\mathsf H_{\rm pack}(\omega):}
 \tag{4.4}
\]

1. there is an exactly-once identity
   \[
    \mathfrak C_x=\sum_{q\in\mathcal Q}\sum_{\nu}\mathcal K_{\nu,q}
                   +\mathcal R_x;
    \tag{4.5}
   \]
2. every cell in (4.5) is BP-admissible and is derived from the same signed
   packet (2.4), preserving \(\beta,w,K_H\), the prime shell, the deleted
   diagonal, units/nonunits, and all dyadic template labels;
3. the remainder and aggregate cell norm obey
   \[
    |\mathcal R_x|\ll x^{53/32+o(1)},\qquad
    \sum_{q,\nu}\mathcal T_{\nu,q}
       \ll x^{5/3+o(1)}Q^\omega.
    \tag{4.6}
   \]

The aggregate inequality in (4.6) is the analytic heart.  It must be proved
before summing absolute cell bounds and it absorbs the number of templates,
coefficient norms, endpoint pieces, and reassembly.  Merely declaring cells or
renormalizing their coefficients cannot make \(\mathcal T_{\nu,q}\) smaller.

Relative to (3.4), (4.6) gives the effective pre-cell gain

\[
 Q^{-31/32+\omega}.
 \tag{4.7}
\]

V36 used the sufficient special case \(\omega=0\).  V37 leaves a quantified,
strictly positive loss budget.

## 5. Source-backed cell engine and strict endpoint

Blomer--Pascadi Theorem 1.1, equivalently the critical specialization of
Theorem 5.5, gives for every BP-admissible cell

\[
 |\mathcal K_{\nu,q}|
 \ll q^{-1/32+o(1)}\mathcal T_{\nu,q}.
 \tag{5.1}
\]

Applying (5.1) only after (4.5)--(4.6) yields

\[
 |\mathfrak C_x|
 \ll x^{5/3+o(1)}Q^{\omega-1/32}+x^{53/32+o(1)}
 =x^{53/32+\omega/3+o(1)}.
 \tag{5.2}
\]

Thus the conditional K-route saving is

\[
 \delta_K(\omega)=\frac1{96}-\frac\omega3,
 \tag{5.3}
\]

and its strict margin over the required \(1/400\) is

\[
 \boxed{
 \delta_K(\omega)-\frac1{400}
 =\frac{19}{2400}-\frac\omega3.}
 \tag{5.4}
\]

Therefore the exact admissible window is

\[
 \boxed{0\leq\omega<\frac{19}{800}.}
 \tag{5.5}
\]

Equality is insufficient.  Under \(\mathsf H_{\rm pack}(\omega)\), the final
off-zero B saving may be any

\[
 0<\eta_B<\frac{19}{2400}-\frac\omega3.
 \tag{5.6}
\]

This uses the already-paid \(19/2400\) remainder margin and the larger
\(121/9600\) local-carrier margin.  It does not pay terminal A.

## 6. General interpolation and generic-Cauchy no-go

It is useful to separate the pre-cell saving \(Q^{-\rho}\) from a local cell
saving \(Q^{-\gamma}\).  Starting from (3.4), the output exponent is

\[
 \frac{191}{96}-\frac{\rho+\gamma}{3}.
 \tag{6.1}
\]

The strict endpoint condition is exactly

\[
 \boxed{\rho+\gamma>\frac{781}{800}.}
 \tag{6.2}
\]

For \(\gamma=1/32\), this becomes

\[
 \boxed{\rho>\frac{189}{200}.}
 \tag{6.3}
\]

Since \(\rho=31/32-\omega\), equations (6.2)--(6.3) are equivalent to
(5.5).

A generic Cauchy--Schwarz estimate over \(\ell\) saves only the square root of
the occupancy:

\[
 \rho_{\ell^2}=\frac{31}{64}.
 \tag{6.4}
\]

Even after the BP gain, this gives

\[
 \frac{191}{96}-\frac13\left(\frac{31}{64}+\frac1{32}\right)
 =\frac{349}{192},
 \tag{6.5}
\]

which exceeds the target \(1997/1200\) by

\[
 \boxed{\frac{349}{192}-\frac{1997}{1200}=\frac{737}{4800}.}
 \tag{6.6}
\]

Hence the missing input is not an \(\ell^2\) bound in isolation.  It must be a
joint transform/reassembly theorem that avoids almost all of the \(L^1\)
packet cost; its permitted overhead exponent is only \(19/800\).

## 7. Primary-source verification matrix

The source screen was performed against theorem texts, not abstracts alone.

1. **Blomer--Pascadi, arXiv:2607.24311v1.**  Theorem 1.1 accepts arbitrary
   two-array coefficients on two intervals and, at length \(q^{1/2}\), gives
   the exact \(q^{-1/32}\) saving in (5.1).  It is fixed-modulus and starts
   after a Kloosterman cell already exists.  It does not provide (4.5) or the
   aggregate norm (4.6).
2. **Pascadi, arXiv:2404.04239v3.**  Theorem 13 and Corollaries 17--18 genuinely
   average levels/moduli, but require frequency-concentrated sequences,
   Assumption 14, and smooth spectral weights.  No theorem identifies the
   literal MASTER/hybrid packet (2.4) with those sequences or proves the
   required concentration measure.
3. **Wright, arXiv:2604.25177v1.**  Theorem 2.1 improves a trilinear
   Kloosterman-fraction form with a partially fixed denominator.  Its
   dispersion application uses divisor-bounded arrays and a
   Siegel--Walfisz input.  It does not preserve the centered residue packet,
   physical \(w\), and zero deletion in one exactly-once compiler.
4. **Bettin--Chandee, arXiv:1502.00769.**  Their arbitrary-coefficient
   trilinear fraction theorem is a valid local architecture analogue, not a
   theorem for the prime-shell packet norm (4.6).
5. **Blomer--Risager--Shparlinski, arXiv:2411.17823.**  Their triple
   Kloosterman-sum bounds average a specified modular-inverse family.  They do
   not accept the two physical arrays and the centered congruent/background
   difference in (2.4).

Accordingly, the source-backed statement stops at (5.1).  Direct attachment
to (1.4) remains `NONE_FOUND` as of 2026-08-09.

## 8. Devil's Advocate checkpoint and heuristic charter

The strongest objection is that \(\mathsf H_{\rm pack}(\omega)\) may merely
rename the desired power saving.  It would be circular if it only asserted a
small value for \(\mathfrak C_x\).  It does not: (4.1)--(4.3) prescribe a
source theorem's input type and norm, (4.5) requires an exact physical
identity, and (4.6) is an independently falsifiable aggregate coefficient
bound.  A proposed compiler fails if any row is duplicated, any diagonal or
background row is discarded, any coefficient is replaced by an envelope, or
the source-native \(\ell^2\) norms exceed the budget.

The second objection is that random signs should already save the shift
length.  Section 6 disproves that shortcut at the isolated packet level:
square-root \(\ell\)-cancellation misses by \(737/4800\).  V36's much smaller
global random-model exponent \(223/192\) used hypothetical independence across
several additional variables.  It remains a heuristic consistency check, not
evidence for (4.6).

The following firewalls are therefore mandatory:

1. `AVOIDED_TRIANGLE_LOSS` is not `PROVED_RANDOM_CANCELLATION`;
2. the average over all \(b\ne-t\) in (2.4) may not be replaced by the
   congruent branch alone;
3. the \(b=0,\ell=0\) diagonal may not be restored;
4. a fixed-\(q\) BP estimate cannot be applied until the physical compiler and
   aggregate norm are proved;
5. finite packet identities and exponent arithmetic create no arithmetic
   credit.

Devil's Advocate verdict: `PASS_AS_A_CONDITIONAL_RESEARCH_BLUEPRINT`, with the
open theorem (4.4)--(4.6) classified as a major unresolved hypothesis.

## 9. Finite fixtures and map position

For \(q=5\), \(t=2\), the allowed difference residues are
\(b\in\{0,1,2,4\}\).  The packet

\[
 (F(0),F(1),F(2),F(4))=(7,-2,3,1)
 \tag{9.1}
\]

has mean \(9/4\), so the centered projector gives

\[
 5\left(F(0)-\frac14\sum_bF(b)\right)=\frac{95}{4}.
 \tag{9.2}
\]

Using the concrete rows \(u=(7,3,4,1)\), the direct ratio-kernel evaluation
gives the same value.  A constant packet gives zero.  The checker also freezes
(5.2)--(6.6), the strict failure at \(\omega=19/800\), a valid sample
\(\omega=1/100\) with margin \(11/2400\), and the difference between packet
\(L^1\) and packet \(L^2\).

On the route map, V37 remains at the red Bridge A / Gate B crossing on the
analytic-elimination island.  The K lane now has a measured construction pier:

```text
centered residue packet
  -> exactly-once balanced BP emitter, overhead Q^omega (OPEN)
  -> omega<19/800
  -> BP q^(-1/32) cell engine (SOURCE-BACKED)
  -> off-zero B gate
  -> terminal q-local A still OPEN.
```

## 10. Canonical registry

```text
V37_MAXIMUM_CLAIM = EXACT_CENTERED_RESIDUE_PACKETIZATION_PLUS_LOSS_BUDGETED_K_ROUTE_THRESHOLD_AND_SOURCE_BACKED_CELL_ENGINE_AFTER_CONJECTURAL_EMISSION
V37_ROUTE_ADVANCE = YES
V37_CONDITIONAL_BRIDGE_ADVANCE = YES
V37_ARITHMETIC_ADVANCE = NO
V37_FIXED_ATOM_CREDIT = 0
V37_STRICT_1_OVER_400 = UNPAID
V37_L2 = NONE
V37_TPC_207_TRIGGER = false
V37_NUMBERED_RELEASE = NO
V37_DERIVATION_STATUS = COHERENT_AFTER_EXACT_PACKETIZATION_AND_LOSS_BUDGETING
V37_ASSUMPTION_POLICY = PACKET_EMITTER_IS_EXPLICIT_CONJECTURE_AND_NEVER_PROMOTED_TO_THEOREM
V37_SELECTED_RESEARCH_ROUTE = K_LOSS_BUDGETED_PACKET_EMITTER_FIRST__E_SECOND__X_THIRD__A_TERMINAL_AFTER_B__C_RESERVE
V37_V36_BINARY_CORE = RETAINED_EXACT_OFF_DIAGONAL_COPRIME_RATIO_COVARIANCE
V37_CENTERED_RESIDUE_PACKET = PROVED_EXACT_BINARY_CORE_PACKET_IDENTITY
V37_UNIT_TO_DIFFERENCE_BIJECTION = PROVED_EXACT_A_TO_B_EQUALS_A_MINUS_ONE_TIMES_T
V37_PACKET_DIAGONAL = PROVED_EXACT_ONLY_B_ZERO_ELL_ZERO_ROW_DELETED
V37_PACKET_BACKGROUND = PROVED_EXACT_ALL_B_NOT_EQUAL_MINUS_T_REQUIRED
V37_CONSTANT_PACKET = PROVED_EXACT_ANNIHILATED
V37_SCHWARTZ_TAIL = PROVED_NEGLIGIBLE_AFTER_H_X_EPSILON_TRUNCATION
V37_SHIFT_OCCUPANCY = Q_POWER_31_OVER_32
V37_RAW_POSITIVE_COMPENSATING_TRIANGLE = X_POWER_191_OVER_96
V37_PACKET_EMITTER_STATUS = OPEN_CONJECTURE_BP_ADMISSIBLE_EXACTLY_ONCE_JOINT_PACKET
V37_PACKET_EXACTLY_ONCE_POLICY = PHYSICAL_BETA_W_K_PRIME_SHELL_ZERO_DELETION_AND_ALL_TEMPLATE_LABELS_PRESERVED
V37_PACKET_PRE_CELL_BUDGET = X_POWER_5_OVER_3_TIMES_Q_POWER_OMEGA
V37_PACKET_EFFECTIVE_GAIN = Q_POWER_MINUS_31_OVER_32_PLUS_OMEGA
V37_PACKET_OVERHEAD_THRESHOLD = OMEGA_STRICTLY_LESS_THAN_19_OVER_800
V37_BLOMER_PASCADI_CELL_ENGINE = SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_AT_CRITICAL_SQUARE_ROOT_RANGE
V37_CONDITIONAL_OUTPUT = X_POWER_53_OVER_32_PLUS_OMEGA_OVER_3
V37_CONDITIONAL_DELTA = 1_OVER_96_MINUS_OMEGA_OVER_3
V37_CONDITIONAL_ENDPOINT_MARGIN = 19_OVER_2400_MINUS_OMEGA_OVER_3
V37_GENERAL_GAIN_CONDITION = RHO_PLUS_GAMMA_STRICTLY_GREATER_THAN_781_OVER_800
V37_WITH_BP_RHO_THRESHOLD = RHO_STRICTLY_GREATER_THAN_189_OVER_200
V37_V36_ZERO_LOSS_COMPILER = SUFFICIENT_SPECIAL_CASE_OMEGA_ZERO_NOT_NECESSARY
V37_ELL_CAUCHY = STOP_SCOPED_EFFECTIVE_RHO_31_OVER_64_INSUFFICIENT
V37_ELL_CAUCHY_OUTPUT = X_POWER_349_OVER_192
V37_ELL_CAUCHY_ENDPOINT_DEFICIT = 737_OVER_4800
V37_PACKET_COMPILER_NOT_RANDOM_CANCELLATION = PROVED_STATUS_FIREWALL
V37_GLOBAL_RANDOM_PHASE_BENCHMARK = RETAINED_HEURISTIC_ONLY_X_POWER_223_OVER_192
V37_BLOMER_PASCADI_DIRECT_ATTACHMENT = STOP_SCOPED_REQUIRES_PRIOR_PHYSICAL_PACKET_EMISSION_AND_AGGREGATE_NORM
V37_PASCADI_FREQUENCY_CONCENTRATION_DIRECT_ATTACHMENT = STOP_SCOPED_ASSUMPTION14_AND_SMOOTH_LEVEL_SEQUENCE_NOT_VERIFIED_FOR_LITERAL_PACKET
V37_WRIGHT_PARTIALLY_FIXED_MODULUS_DIRECT_ATTACHMENT = STOP_SCOPED_WRONG_DISPERSION_ARRAYS_AND_NO_CENTERED_PACKET_REASSEMBLY
V37_BETTIN_CHANDEE_DIRECT_ATTACHMENT = STOP_SCOPED_LOCAL_TRILINEAR_FRACTION_NO_PRIME_SHELL_PACKET_NORM
V37_BLOMER_RISAGER_SHPARLINSKI_DIRECT_ATTACHMENT = STOP_SCOPED_SPECIFIED_TRIPLE_MODULAR_INVERSE_FAMILY_WRONG_PHYSICAL_COEFFICIENTS
V37_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V37_ROUTE_E = RETAINED_OPEN_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800
V37_ROUTE_X = RETAINED_OPEN_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200
V37_TERMINAL_A = OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B
V37_DYNAMICS_C = RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN
V37_NEXT_THEOREM = EXACTLY_ONCE_BP_ADMISSIBLE_CENTERED_SHIFT_PACKET_EMITTER_WITH_AGGREGATE_OVERHEAD_OMEGA_LT_19_OVER_800
V37_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_THE_BP_ADMISSIBLE_PACKET_EMITTER_AND_AGGREGATE_NORM_WITH_OMEGA_LT_19_OVER_800
V37_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_K_LANE_LOSS_BUDGETED_PIER_MARKED
V37_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V37_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
```

The maximum claim is an exact packet identity and a conditional theorem
compiler.  It is not the packet estimate itself, an arithmetic saving, a fixed
atom, or a numbered release.
