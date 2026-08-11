# Bridge A / Gates A--B V51: fold-first long-Mobius pair compiler

Date: 2026-08-11

Status: unnumbered big-road research artifact.  V51 does not prove a new
arithmetic saving.  It replaces the orientation-by-orientation long-Mobius
atlas by one exact unordered-pair diagonal-completed Gate-A emitter.  The mixed
transition/reverse-Type-I lane and the balanced two-long lane are folded before
Poisson, character expansion, or any outer absolute value.  The resulting
coefficient numerator has rank at most two on every product-cut cell, and the
factor $1/\log(s\ell)$ is removed by an exact one-dimensional Abel compiler.
The new preferred theorem is a single signed bound for the mixed plus balanced
pair aggregate.  That theorem remains conjectural; Gate B remains independently
open.

V51 uses four claim classes throughout:

* `PROVED` means an exact identity, support statement, finite-dimensional
  compiler, or an already-paid upstream estimate;
* `SOURCE_BACKED_CONDITIONAL` means that a primary theorem is a legitimate
  local engine only after the stated emitter and norm hypotheses are proved;
* `CONJECTURAL` means a new asymptotic theorem required by the route;
* `NO_GO` means only the displayed interface is invalid, not that every future
  method is impossible.

## 1. Frozen scalar and endpoint clock

Retain

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
 K_H(h)=\widehat\psi_+(h/H),
 \tag{1.3}
\]

where

\[
 \widehat\psi_+(\xi)=\int_{\mathbb R}\psi(v)e(+\xi v)\,dv,
 \qquad \int\psi=1.
 \tag{1.4}
\]

For prime $q$, set

\[
 c'_q(h)=\mathbf 1_{q\mid h}-\frac1{q-1}.
 \tag{1.5}
\]

The physical centered row and Gate-B numerator are

\[
 s_q=\sum_{\substack{t,u\in I_x\\t\ne u,\ q\nmid tu}}
 \beta(t)w(u)K_H(u-t)c'_q(u-t),
 \qquad
 \mathfrak C_x=\sum_{q\in\mathcal Q}q s_q.
 \tag{1.6}
\]

The Gate-A numerator target remains

\[
 T_{\rm num}=\frac{1997}{1200},
 \tag{1.7}
\]

and V43 proved

\[
 \mathfrak C_x=\mathfrak A_x-L_{\rm pr}S_x^{\rm physical}
 +O\!\left(x^{79/48+\varepsilon+o(1)}+x^{4/3+o(1)}\right),
 \tag{1.8}
\]

for every fixed $0<\varepsilon<11/600$.  Here

\[
 S_x^{\rm physical}=\sum_{u\in I_x}\beta(u)w(u),\qquad
 L_{\rm pr}=\sum_{q\in\mathcal Q}(q-1)=x^{2/3+o(1)}.
 \tag{1.9}
\]

## 2. Exact unordered fold

The V43 ordered proper-factor identity is

\[
 \beta(t)=\sum_{\substack{dk=t\\d,k\geq2}}\mu(d)\omega_x(d,k),
 \tag{2.1}
\]

\[
 \omega_x(d,k)=
 \begin{cases}
 -\log d/\log(dk),&d\leq U,\\[1mm]
 \log k/\log(dk),&d>U.
 \end{cases}
 \tag{2.2}
\]

For $t=s\ell$, $s<\ell$, define

\[
 F_U(s,\ell)=
 \begin{cases}
 (\mu(\ell)-\mu(s))\log s,&s\leq U,\\[1mm]
 \mu(s)\log\ell+\mu(\ell)\log s,&s>U,
 \end{cases}
 \tag{2.3}
\]

and

\[
 \Omega_U(s,\ell)=\frac{F_U(s,\ell)}{\log(s\ell)}.
 \tag{2.4}
\]

Then the two ordered occurrences fold exactly to

\[
 \boxed{
 \mu(s)\omega_x(s,\ell)+\mu(\ell)\omega_x(\ell,s)
 =\Omega_U(s,\ell).}
 \tag{2.5}
\]

Since

\[
 U^2=x^{133/200}<x/2,
 \tag{2.6}
\]

the first case in (2.3) automatically has $s\leq U<\ell$.  Thus it is
the exact signed union of the short-orientation transition lane and the
long-orientation reverse-Type-I lane.  The second case is the balanced
two-long lane.  For a square $t=s^2\in I_x$, necessarily $s>U$, and the
single ordered coefficient is

\[
 \Omega_U^\square(s)=\frac{\mu(s)}2.
 \tag{2.7}
\]

Equations (2.5)--(2.7) give the coefficientwise identity

\[
 \boxed{
 \beta(t)=
 \sum_{\substack{s<\ell\\s\ell=t}}\Omega_U(s,\ell)
 +\mathbf 1_{t=s^2}\frac{\mu(s)}2.}
 \tag{2.8}
\]

## 3. Rank-two numerator and exact Abel compiler

The logarithmic numerator in each nonsquare cell has rank at most two.  In
the mixed lane,

\[
 F_U(s,\ell)
 =(\log s)\mu(\ell)+(-\mu(s)\log s)\,\mathbf 1_\ell,
 \tag{3.1}
\]

while in the balanced lane,

\[
 F_U(s,\ell)=\mu(s)\log\ell+\mu(\ell)\log s.
 \tag{3.2}
\]

The denominator $1/\log(s\ell)$ is a product variable, so V51 does not
call the full coefficient matrix rank two.  Instead it removes that one
factor exactly.  For any complex cell weight $G(s,\ell)$, put

\[
 A_G(T)=\sum_{\substack{s<\ell\\x/2<s\ell\leq T}}
 F_U(s,\ell)G(s,\ell).
 \tag{3.3}
\]

Abel summation gives

\[
 \boxed{
 \sum_{\substack{s<\ell\\s\ell\in I_x}}
 \Omega_U(s,\ell)G(s,\ell)
 =\frac{A_G(x)}{\log x}
 +\int_{x/2}^{x}\frac{A_G(T)}{T(\log T)^2}\,dT.}
 \tag{3.4}
\]

Thus every smooth dyadic pair cell has two separated numerator tensors and
one one-dimensional product-cut integral.  The integral costs logarithms,
not a power of $x$, provided a bound is uniform in $T\in[x/2,x]$.

## 4. Pair-native diagonal-completed Gate-A emitter

For each $q\in\mathcal Q$, define the unit-restricted diagonal

\[
 S_q=\sum_{\substack{u\in I_x\\q\nmid u}}\beta(u)w(u).
 \tag{4.1}
\]

Define the diagonal-completed folded row

\[
 \begin{aligned}
 \mathcal F_q={}&
 \sum_{\substack{s<\ell,\ s\ell\in I_x\\q\nmid s\ell}}
 \Omega_U(s,\ell)
 \sum_{\substack{u\in I_x\\q\nmid u}}
 w(u)K_H(u-s\ell)c'_q(u-s\ell)\\
 &+\sum_{\substack{s^2\in I_x\\q\nmid s}}
 \frac{\mu(s)}2
 \sum_{\substack{u\in I_x\\q\nmid u}}
 w(u)K_H(u-s^2)c'_q(u-s^2).
 \end{aligned}
 \tag{4.2}
\]

Unlike (1.6), (4.2) includes $u=s\ell$ and $u=s^2$.  The fold (2.8)
and $K_H(0)=1$ therefore give the exact row identity

\[
 \boxed{\mathcal F_q=s_q+c'_q(0)S_q,\qquad
 c'_q(0)=\frac{q-2}{q-1}.}
 \tag{4.3}
\]

Set

\[
 \mathfrak F_x=\sum_{q\in\mathcal Q}q\mathcal F_q,
 \qquad
 B_Q=\sum_{q\in\mathcal Q}\frac{q(q-2)}{q-1}.
 \tag{4.4}
\]

Then

\[
 \mathfrak F_x
 =\mathfrak C_x+B_QS_x^{\rm physical}+O(x^{4/3+o(1)}),
 \tag{4.5}
\]

where the error is exactly the already-paid $q\mid u$ omission.  Since

\[
 B_Q=L_{\rm pr}+O(x^{o(1)}),
 \tag{4.6}
\]

equation (1.8) yields the Gate-A crosswalk

\[
 \boxed{
 \mathfrak F_x=\mathfrak A_x
 +O\!\left(x^{79/48+\varepsilon+o(1)}+x^{4/3+o(1)}
 +x^{1+o(1)}\right).}
 \tag{4.7}
\]

Thus $\mathfrak F_x$ is not a new physical scalar with an unstated
normalization.  It is an exact fold-first representation of the V43 Gate-A
numerator up to previously paid terms.

## 5. Exact character--Fourier normal form

Extend Dirichlet characters modulo $q$ by zero on nonunits.  For
$q\nmid tu$, multiplicative orthogonality gives

\[
 \boxed{
 c'_q(u-t)=\frac1{q-1}
 \sum_{\substack{\chi\ ({\rm mod}\ q)\\\chi\ne\chi_0}}
 \chi(u)\overline{\chi(t)}.}
 \tag{5.1}
\]

Also

\[
 K_H(u-t)=\int_{\mathbb R}\psi(v)
 e\!\left(\frac{(u-t)v}{H}\right)\,dv.
 \tag{5.2}
\]

For $\alpha\in\mathbb R$, define

\[
 W_{q,\chi}(\alpha)=
 \sum_{u\in I_x}w(u)\chi(u)e(+\alpha u),
 \tag{5.3}
\]

\[
 B^{\rm mix}_{q,\chi}(\alpha)=
 \sum_{\substack{s<\ell,\ s\ell\in I_x\\s\leq U}}
 \Omega_U(s,\ell)\overline{\chi(s\ell)}e(-\alpha s\ell),
 \tag{5.4}
\]

\[
 B^{\rm bal}_{q,\chi}(\alpha)=
 \sum_{\substack{s<\ell,\ s\ell\in I_x\\s>U}}
 \Omega_U(s,\ell)\overline{\chi(s\ell)}e(-\alpha s\ell),
 \tag{5.5}
\]

and

\[
 B^{\square}_{q,\chi}(\alpha)=
 \sum_{s^2\in I_x}\frac{\mu(s)}2
 \overline{\chi(s^2)}e(-\alpha s^2).
 \tag{5.6}
\]

Substituting (5.1)--(5.6) into (4.2) gives the exact single-aggregate emitter

\[
 \boxed{
 \mathfrak F_x=
 \sum_{q\in\mathcal Q}\frac{q}{q-1}
 \sum_{\substack{\chi\ ({\rm mod}\ q)\\\chi\ne\chi_0}}
 \int_{\mathbb R}\psi(v)W_{q,\chi}(v/H)
 \bigl(B^{\rm mix}_{q,\chi}+B^{\rm bal}_{q,\chi}
 +B^{\square}_{q,\chi}\bigr)(v/H)\,dv.}
 \tag{5.7}
\]

The same prime shell, the literal $w=\Lambda(\cdot+2)-b_x^{(z)}$, both
ordered signs, the hard product shell, the physical unit restrictions through
character extension by zero, and one outer signed sum are retained.  Formula
(5.7) is an exact source-facing normal form, not an estimate.

## 6. Why folding must precede orientation-wise Poisson

The fold cannot be reconstructed after taking absolute values of separately
transformed orientations.

First, with $U\geq2$, $s=2$, and $\ell=3$, one has

\[
 \mu(2)=\mu(3)=-1,\qquad \Omega_U(2,3)=0,
 \tag{6.1}
\]

while the two ordered absolute masses sum to

\[
 2\frac{\log2}{\log6}>0.
 \tag{6.2}
\]

Second, take the finite transform fixture

\[
 (s,\ell,U,q,H_0)=(6,10,7,11,50).
 \tag{6.3}
\]

Here $\mu(6)=\mu(10)=1$, so the mixed folded coefficient is again zero.
But V43's orientation-wise Poisson support lengths are

\[
 \left\lfloor\frac{s q}{H_0}\right\rfloor=1,
 \qquad
 \left\lfloor\frac{\ell q}{H_0}\right\rfloor=2.
 \tag{6.4}
\]

The short orientation emits $m=\pm1$, whereas the long orientation emits
$m=\pm1,\pm2$, with different reciprocal phases even on the shared
frequencies.  Consequently the exact zero in (6.3) is not a termwise zero of
the two Poisson outputs.  The legal order is

\[
 \boxed{\text{fold orientations}\ \longrightarrow\
 \text{separate product cells}\ \longrightarrow\
 \text{transform}\ \longrightarrow\
 \text{one outer absolute}.}
 \tag{6.5}
\]

Orientation-first triangle reassembly is therefore `NO_GO` for the literal
coefficient, while a future pair-native double-Poisson or character-spectral
compiler remains open.

## 7. The one whole-object Gate-A theorem

Split (5.7) before the square row as

\[
 \mathfrak F_x=\mathfrak F_x^{\rm mix}
 +\mathfrak F_x^{\rm bal}+\mathfrak F_x^{\square}.
 \tag{7.1}
\]

V43 already proved the physical off-diagonal square estimate.  The
diagonal-completed row adds only its diagonal, bounded by
$L_{\rm pr}x^{1/2+o(1)}=x^{7/6+o(1)}$, so

\[
 |\mathfrak F_x^{\square}|\ll x^{143/96+o(1)},
 \qquad
 \frac{1997}{1200}-\frac{143}{96}=\frac{419}{2400}.
 \tag{7.2}
\]

The preferred V51 conjectural theorem is

\[
 \boxed{
 \mathsf H_{\rm fold}(\eta_L):\qquad
 |\mathfrak F_x^{\rm mix}+\mathfrak F_x^{\rm bal}|
 \ll x^{1997/1200-\eta_L+o(1)},\qquad \eta_L>0.}
 \tag{7.3}
\]

This is one signed theorem.  Separate mixed and balanced estimates are a
stronger sufficient package, not an equivalent reformulation.  Equations
(4.7) and (7.2) show that (7.3) implies the V43 Gate-A hypothesis for every

\[
 0<\eta_A<\min\left\{
 \eta_L,\frac{419}{2400},\frac{11}{600}-\varepsilon
 \right\}.
 \tag{7.4}
\]

Combining this with an independent Gate-B saving $\eta_B>0$, V43 yields the
physical endpoint for every

\[
 0<\eta<\min\left\{
 \eta_L,\eta_B,\frac{419}{2400},
 \frac{19}{2400},\frac{11}{600}-\varepsilon
 \right\}.
 \tag{7.5}
\]

Thus V51 supplies a broad bypass around the sequential
`bounded-quality core -> reverse Type I -> balanced Type II` construction.
The V50 bounded-quality core remains a legitimate conjectural alternative,
not a proved lemma needed by (7.3).

Bounded Siegel quality alone does not provide the missing power.  If
$d=x^\gamma$ and

\[
 \beta_\chi=1-\frac1{\eta\log d},
 \tag{7.6}
\]

then

\[
 x^{\beta_\chi}
 =x\exp\!\left(-\frac1{\eta\gamma}\right).
 \tag{7.7}
\]

For bounded $\eta$, the factor in (7.7) is only a fixed relative constant,
not $x^{-\delta}$.  Hence V50's bounded-world hypothesis remains genuinely
conjectural; it cannot be promoted by a pointwise zero-free slogan.

## 8. Energy and primary-source boundary

The generic multiplicative large sieve does not reach (7.3).  The divisor
envelopes give

\[
 \sum_{t\in I_x}|\beta(t)|^2+\sum_{u\in I_x}|w(u)|^2
 \ll x^{1+o(1)}.
 \tag{8.1}
\]

Applying the ordinary character large sieve independently to the two factors
in (5.7), then Cauchy, gives only

\[
 |\mathfrak F_x|\ll x^{2+o(1)}.
 \tag{8.2}
\]

The deficit is

\[
 2-\frac{1997}{1200}=\frac{403}{1200}.
 \tag{8.3}
\]

The current primary-source screen gives local engines and firewalls, not the
whole-object theorem.

1. [Blomer--Pascadi, arXiv:2607.24311v1, Theorem 1.1](https://arxiv.org/abs/2607.24311)
   proves, for fixed modulus $c$, arbitrary coefficient arrays in a
   bilinear Kloosterman-sum cell; at critical length it saves
   $c^{-1/32+o(1)}$.  It is a `SOURCE_BACKED_CONDITIONAL` cell engine after
   an exact pair-native Kloosterman emitter.  It does not supply the
   $(q,\chi,v,s,\ell,u)$ aggregate, its norms, or signed reassembly in (5.7).

2. [Pascadi, arXiv:2404.04239v3](https://arxiv.org/abs/2404.04239), now
   published in *Forum of Mathematics, Pi* 14 (2026), gives exceptional-form
   large sieves for sequences with sparse Fourier transforms and strong
   incomplete Kloosterman corollaries.  It remains the strongest horizontal
   `SOURCE_BACKED_CONDITIONAL` candidate after a literal pair emitter; no
   theorem there accepts (5.7) directly.

3. [Wright, arXiv:2604.25177v2](https://arxiv.org/abs/2604.25177) improves
   unbalanced convolution estimates and trilinear Kloosterman fractions with
   a partially fixed denominator.  Its AP theorem assumes a short sequence
   satisfying a Siegel--Walfisz condition and has neither the physical
   $w=\Lambda(\cdot+2)-b_x^{(z)}$ joint factor nor the fold-first mixed plus
   balanced aggregate.  Direct attachment is `NO_GO` at this interface.

4. [Milicevic--Qin--Wu, arXiv:2511.07550v1](https://arxiv.org/abs/2511.07550)
   proves power-saving bilinear Kloosterman-sum bounds for arbitrary fixed
   moduli.  It is post-transform and fixed-modulus; it does not construct the
   pair emitter, retain the common prime shell, or pay the outer reassembly.

5. [Dong--Robles--Zeindler, arXiv:2601.00292v2](https://arxiv.org/abs/2601.00292)
   is withdrawn.  The author comment states that a missing $L^2$ factor in
   equation (2.53) changes $L^5$ to $L^7$, so the claimed improvement does
   not follow.  No V51 exponent ledger uses that claimed saving.

No checked primary theorem proves (7.3).  The first arithmetic fatal is the
absence of a literal fold-first pair-native collective theorem for the same
physical coefficient, shell, prime ensemble, and one outer signed scalar.

## 9. Finite diagnostics and paper extraction

The checker freezes the following finite facts.

1. Mixed pairs $(2,3)$ and $(6,10)$ have exact zero folded numerator but
   nonzero orientation-wise absolute mass.
2. The pair $(2,6)$ has mixed numerator $2\log2$; the balanced pair
   $(5,7)$ has numerator $-\log5-\log7$; the square $36=6^2$ has
   coefficient $1/2$.
3. For $q=3$, the unique nonprincipal character gives exactly
   $c'_3(0)=1/2$ and $c'_3(1)=-1/2$ on the two unit residues.
4. A finite diagonal-completed row verifies (4.3) before any estimate.
5. A rational discrete Abel fixture verifies the endpoint term plus all
   cumulative differences; it does not replace the asymptotic theorem.
6. The exponent ledger freezes (31/96,23/2400,17/96,143/96), the square
   margin (419/2400), and the generic-large-sieve deficit (403/1200).

V51 also starts a parallel paper-candidate ledger at
[`PAPER_CANDIDATE_LEDGER.md`](PAPER_CANDIDATE_LEDGER.md).  It records only
results at or above the following thresholds:

* exact lemmas suitable for a proof section;
* source-backed conditional propositions with every hypothesis stated;
* explicit conjectures whose implication chain is proved;
* finite counterexamples that prevent a false theorem formulation.

This does not create a numbered paper.  A small-paper draft becomes justified
only after one coherent theorem package has a complete statement, proof, and
source boundary independent of the TPC endgame.

## 10. Canonical status registry

~~~text
V51_MAXIMUM_CLAIM = EXACT_FOLD_FIRST_UNORDERED_PAIR_DIAGONAL_COMPLETED_EMITTER_REPRESENTS_THE_V43_GATE_A_NUMERATOR_UP_TO_PAID_ERRORS_AND_REDUCES_MIXED_PLUS_BALANCED_LONG_MOBIUS_TO_ONE_CONJECTURAL_SIGNED_THEOREM
V51_ROUTE_ADVANCE = YES
V51_CONDITIONAL_BRIDGE_ADVANCE = YES
V51_ARITHMETIC_ADVANCE = NO
V51_FIXED_ATOM_CREDIT = 0
V51_STRICT_1_OVER_400 = UNPAID
V51_L2 = NONE
V51_TPC_207_TRIGGER = false
V51_NUMBERED_RELEASE = NO
V51_DERIVATION_STATUS = COHERENT_AFTER_UNORDERED_FOLD_RANK_TWO_NUMERATOR_ABEL_COMPILER_DIAGONAL_COMPLETED_CROSSWALK_AND_CHARACTER_FOURIER_EMITTER
V51_ASSUMPTION_POLICY = FOLD_FIRST_MIXED_PLUS_BALANCED_BOUND_IS_CONJECTURAL__LOCAL_SPECTRAL_RESULTS_ARE_SOURCE_BACKED_CONDITIONAL__ORIENTATION_FIRST_TRIANGLE_IS_NO_GO
V51_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_FOLD_FIRST_GATE_A_WHOLE_OBJECT__V42_GATE_B__V43_JOIN__DYNAMICS_RESERVE
V51_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO
V51_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__Y0_31_OVER_96
V51_ORDERED_PROPER_FACTOR_IDENTITY = RETAINED_EXACT_FROM_V43
V51_FOLDED_NONSQUARE_IDENTITY = PROVED_EXACT_TWO_ORIENTATION_SUM
V51_FOLDED_SQUARE_IDENTITY = PROVED_EXACT_MU_S_OVER_2
V51_U_SQUARED_SUPPORT = PROVED_X_133_OVER_200_LT_X_OVER_2
V51_MIXED_PAIR_NUMERATOR = PROVED_EXACT_MU_L_MINUS_MU_S_TIMES_LOG_S
V51_BALANCED_PAIR_NUMERATOR = PROVED_EXACT_MU_S_LOG_L_PLUS_MU_L_LOG_S
V51_PAIR_NUMERATOR_SEPARATION_RANK = PROVED_AT_MOST_TWO_BEFORE_PRODUCT_LOG_DENOMINATOR
V51_PRODUCT_LOG_DENOMINATOR = PROVED_EXACT_ONE_DIMENSIONAL_ABEL_COMPILER
V51_PAIR_DIAGONAL_COMPLETED_ROW = DEFINED_WITH_DIAGONAL_AND_LITERAL_PHYSICAL_DATA
V51_PAIR_ROW_CROSSWALK = PROVED_EXACT_F_Q_EQUALS_S_Q_PLUS_C_Q_ZERO_TIMES_S_Q_UNIT
V51_PAIR_SCALAR_CROSSWALK = PROVED_F_EQUALS_C_PLUS_B_Q_S_PHYSICAL_PLUS_UNIT_ERROR
V51_PAIR_TO_V43_GATE_A = PROVED_UP_TO_X_79_OVER_48_PLUS_EPSILON_X_4_OVER_3_AND_X_1_ERRORS
V51_UNIT_OMISSION = RETAINED_PAID_X_4_OVER_3_PLUS_O1
V51_SHELL_FREEZE_ERROR = RETAINED_PAID_X_79_OVER_48_PLUS_EPSILON_PLUS_O1
V51_NONPRINCIPAL_CHARACTER_PROJECTOR = PROVED_EXACT_FOR_UNIT_RESIDUES
V51_FOURIER_KERNEL_SEPARATION = PROVED_EXACT_FROM_PSI_TRANSFORM_CONVENTION
V51_PAIR_CHARACTER_FOURIER_EMITTER = PROVED_EXACT_ONE_OUTER_SIGNED_AGGREGATE
V51_LITERAL_DATA_RETENTION = PROVED_COMMON_Q_SHELL_W_HARD_PRODUCT_SHELL_SIGNS_PHYSICAL_UNIT_RESTRICTIONS_AND_ZERO_AXIS
V51_PAIR_LANE_SPLIT = PROVED_EXACT_MIXED_PLUS_BALANCED_PLUS_SQUARE
V51_SQUARE_SCALAR_PAYMENT = RETAINED_X_143_OVER_96_PLUS_O1
V51_SQUARE_MARGIN_TO_TARGET = 419_OVER_2400
V51_FOLD_FIRST_WHOLE_OBJECT_GATE = CONJECTURAL_H_FOLD_ETA_L
V51_FOLD_FIRST_GATE_IMPLIES_V43_GATE_A = PROVED_CONDITIONAL_WITH_PAID_ERROR_MARGINS
V51_FOLD_FIRST_BYPASS = SELECTED_BROAD_ALTERNATIVE_TO_SEQUENTIAL_BOUNDED_CORE_REVERSE_TYPE_I_AND_BALANCED_TYPE_II
V51_BOUNDED_QUALITY_CORE = RETAINED_V50_CONJECTURAL_ALTERNATIVE
V51_BOUNDED_QUALITY_POINTWISE_POWER = NO_GO_CONSTANT_RELATIVE_DECAY_NOT_X_POWER
V51_SEMIPRIME_FOLD_CANCELLATION = PROVED_EXACT_ZERO_WITH_NONZERO_ORIENTATION_ABSOLUTE_MASS
V51_ORIENTATION_SUPPORT_MISMATCH = PROVED_FINITE_6_10_Q11_H50_LENGTHS_1_AND_2
V51_ORIENTATION_FIRST_POISSON = NO_GO_DESTROYS_EXACT_FOLD_BEFORE_OUTER_ABSOLUTE
V51_POST_TRANSFORM_ORIENTATION_REASSEMBLY = NO_GO_NO_TERMWISE_RECOVERY_OF_FOLDED_ZERO
V51_GENERIC_CHARACTER_LARGE_SIEVE = PROVED_CEILING_X_2_PLUS_O1
V51_GENERIC_CHARACTER_LARGE_SIEVE_DEFICIT = 403_OVER_1200
V51_BLOMER_PASCADI_FIXED_MODULUS_CELL = SOURCE_BACKED_CONDITIONAL_C_MINUS_1_OVER_32_CRITICAL_SAVING
V51_PASCADI_HORIZONTAL_EXCEPTIONAL_SIEVE = SOURCE_BACKED_CONDITIONAL_AFTER_LITERAL_PAIR_EMITTER_AND_NORM
V51_WRIGHT_UNBALANCED_CONVOLUTION = NO_GO_SIEGEL_WALFISZ_SHORT_SEQUENCE_AND_WRONG_JOINT_OBJECT
V51_MILICEVIC_QIN_WU_FIXED_MODULUS = NO_GO_POST_TRANSFORM_CELL_WITHOUT_COMMON_Q_PAIR_EMITTER_OR_REASSEMBLY
V51_DONG_ROBLES_ZEINDLER_2601_00292 = NO_GO_WITHDRAWN_MISSING_L_SQUARED_FACTOR
V51_DIRECT_PRIMARY_SOURCE_FOR_H_FOLD = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V51_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_THE_FOLD_FIRST_MIXED_PLUS_BALANCED_PAIR_NATIVE_GATE_A_AGGREGATE_WITH_PHYSICAL_W_AND_ONE_OUTER_SIGN_AT_FIXED_POWER
V51_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V51_TWO_GATE_COMPILER = RETAINED_V43_GATE_A_AND_GATE_B
V51_TWO_GATE_MARGIN = MIN_ETA_L_ETA_B_419_OVER_2400_19_OVER_2400_AND_11_OVER_600_MINUS_EPSILON
V51_PAPER_CANDIDATE_LEDGER = CREATED_PARALLEL_PROVED_CONDITIONAL_CONJECTURAL_NO_GO_TRACK
V51_SMALL_PAPER_STATUS = UNNUMBERED_OUTLINE_ONLY_NO_STANDALONE_THEOREM_PACKAGE_YET
V51_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_FOLD_FIRST_PAIR_NATIVE_GATE_A_MAPPED_ARITHMETIC_BOUND_OPEN
V51_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V51_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
~~~

The maximum claim is structural and conditional.  Arithmetic advance remains
`NO`, fixed-atom credit remains zero, strict $1/400$ remains unpaid,
$L^2$ remains `NONE`, and `TPC_207_TRIGGER=false`.
