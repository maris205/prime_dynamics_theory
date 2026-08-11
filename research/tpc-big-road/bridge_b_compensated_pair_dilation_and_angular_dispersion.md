# Bridge A / Gate A V52: compensated pair dilation and angular-dispersion endpoint law

Date: 2026-08-11

Status:

```text
UNNUMBERED_BIG_ROAD_CHECKPOINT
ROUTE_ADVANCE = YES
CONDITIONAL_BRIDGE_ADVANCE = YES
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
NUMBERED_RELEASE = NO
```

V52 keeps the V51 fold intact and asks the next whole-object question: can
the single mixed-plus-balanced aggregate be presented as one modulus-family
dispersion object without recovering the two orientations or taking
lane-wise absolute values?  The answer is exact at the compiler level.  The
folded aggregate is one compensated prime-dilation covariance, and its
coefficient has simultaneously a pair-native form and a truncated-sieve
form.  The answer remains open at the analytic level.  Even granting
diagonal-scale Bombieri--Davenport--Halberstam bounds for both marginal
packets, ordinary Cauchy misses the numerator endpoint by exactly $1/400$.
The missing theorem must therefore provide a joint angular/cross-dispersion
saving, a super-diagonal marginal saving, or a mixture of the two.

No asymptotic estimate is proved below.  `PROVED`,
`SOURCE_BACKED_CONDITIONAL`, `CONJECTURAL`, and `NO_GO` are kept separate.

## 1. Frozen object and claim ceiling

Keep

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad
 H=x^{21/32},\qquad Q=x^{1/3},\qquad U=x^{133/400},
 \tag{1.1}
\]

\[
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},\qquad
 w(u)=\Lambda(u+2)-b_x^{(z)}(u),
 \tag{1.2}
\]

\[
 K_H(h)=\widehat\psi_+(h/H),\qquad
 c'_q(h)=\mathbf1_{q\mid h}-\frac1{q-1}.
 \tag{1.3}
\]

The numerator target is

\[
 T_A=\frac{1997}{1200}=\frac53-\frac1{400}.
 \tag{1.4}
\]

V51 defined, for $s<\ell$,

\[
 \Omega_U(s,\ell)=\frac{F_U(s,\ell)}{\log(s\ell)},
 \tag{1.5}
\]

\[
 F_U(s,\ell)=
 \begin{cases}
  (\mu(\ell)-\mu(s))\log s,&s\leq U<\ell,\\[1mm]
  \mu(s)\log\ell+\mu(\ell)\log s,&U<s<\ell.
 \end{cases}
 \tag{1.6}
\]

Put

\[
 \beta^\circ(t)=
 \sum_{\substack{s<\ell\\s\ell=t}}\Omega_U(s,\ell),
 \qquad
 \beta^\square(t)=
 \mathbf1_{t=r^2}\frac{\mu(r)}2.
 \tag{1.7}
\]

The V51 identity is

\[
 \boxed{\beta(t)=\beta^\circ(t)+\beta^\square(t).}
 \tag{1.8}
\]

The square contribution to the diagonal-completed Gate-A aggregate is
already paid:

\[
 |\mathfrak F_x^\square|\ll x^{143/96+o(1)},\qquad
 T_A-\frac{143}{96}=\frac{419}{2400}.
 \tag{1.9}
\]

Thus V52 works only with

\[
 \mathfrak F_x^\circ
 :=\mathfrak F_x^{\rm mix}+\mathfrak F_x^{\rm bal}.
 \tag{1.10}
\]

The maximum claim is an exact compensated-dilation representation of

\[
 \mathfrak F_x^\circ
 \tag{1.11}
\]

and an exact endpoint budget for possible marginal and joint estimates.  It
does not assert any of those estimates.

## 2. One coefficient with two exact interfaces

V33 proved the root-one MASTER marginal identity

\[
 \boxed{
 \beta(t)=\frac{\Lambda(t)}{\log t}
 -\sum_{\substack{d\mid t\\d\leq U}}\mu(d),
 \qquad t\in I_x.}
 \tag{2.1}
\]

Here $d\leq U$ is the same exact condition as
$d^{400}\leq x^{133}$.  Combining (1.8) and (2.1) gives

\[
 \boxed{
 \beta^\circ(t)=\frac{\Lambda(t)}{\log t}
 -\sum_{\substack{d\mid t\\d\leq U}}\mu(d)
 -\mathbf1_{t=r^2}\frac{\mu(r)}2.}
 \tag{2.2}
\]

Equations (1.5)--(1.7) and (2.2) are two interfaces for the same frozen
coefficient.  The pair interface retains the exact cancellation between the
two V43 orientations.  The sieve interface exposes a prime term minus a
truncated Möbius divisor sum.  They must not be estimated separately and
then reassembled by an outer triangle: for a prime $p\in I_x$, the two
terms in (2.1) are both $1$, while their difference is zero.

There is also a useful exact semiprime slice.  Let $p<r$ be primes and
$pr\in I_x$.  Then

\[
 \boxed{
 \beta(pr)=
 \begin{cases}
 0,&p\leq U<r,\\
 -1,&U<p<r.
 \end{cases}}
 \tag{2.3}
\]

For $p^2\in I_x$, $p>U$ and

\[
 \boxed{\beta(p^2)=-\frac12.}
 \tag{2.4}
\]

Thus the balanced pair lane contains the signed indicator of semiprimes
whose two prime factors lie above $U$.  Its product with
$\Lambda(t+2)$ is a reverse-Chen semiprime--prime channel.  The remaining
Möbius-parity rows and the subtraction $b_x^{(z)}$ are part of the same
literal scalar; (2.3) is a source-facing interpretation, not permission to
delete them.

For a composite fixture with more than one unordered factor pair, take
$U=4,t=12$.  The two pairs $(2,6)$ and $(3,4)$ contribute

\[
 \frac{2\log2}{\log12}+\frac{\log3}{\log12}=1,
 \tag{2.5}
\]

which agrees with

\[
 -\sum_{d\mid12,\ d\leq4}\mu(d)=1.
 \tag{2.6}
\]

This checks the collective pair-to-sieve collapse without replacing formal
logarithms by floating-point values.

## 3. Exact compensated prime-dilation normal form

For $q\in\mathcal Q$ and $q\nmid t$, define the one-row compensated
dilation operator

\[
 \begin{aligned}
 \mathcal R_q(t)={}&
 \sum_{\substack{k\in\mathbb Z\\t+qk\in I_x}}
 w(t+qk)K_H(qk)\\
 &-\frac1{q-1}
 \sum_{\substack{u\in I_x\\q\nmid u}}
 w(u)K_H(u-t).
 \end{aligned}
 \tag{3.1}
\]

If $q\mid u-t$ and $q\nmid t$, then $q\nmid u$.  Therefore the first
sum in (3.1) is exactly the divisibility part of $c'_q(u-t)$, including
the physical diagonal $k=0$.  Substitution into the V51 row gives

\[
 \boxed{
 \mathfrak F_x^\circ
 =\sum_{q\in\mathcal Q}q
 \sum_{\substack{t\in I_x\\q\nmid t}}
 \beta^\circ(t)\mathcal R_q(t).}
 \tag{3.2}
\]

Using the pair interface before any absolute value gives the equivalent
whole-object form

\[
 \boxed{
 \mathfrak F_x^\circ
 =\sum_{q\in\mathcal Q}q
 \sum_{\substack{s<\ell,\ s\ell\in I_x\\q\nmid s\ell}}
 \Omega_U(s,\ell)\mathcal R_q(s\ell).}
 \tag{3.3}
\]

The natural smooth dilation length in the first line of (3.1) is

\[
 \frac Hq=x^{31/96+o(1)}.
 \tag{3.4}
\]

This is not a hard support assertion: $K_H$ is Schwartz and the exact sum
is the hard condition $t+qk\in I_x$.  Its tails may be removed only with
the corresponding Schwartz ledger.

Separating the two lines of (3.1) and taking absolute values gives the raw
ceiling

\[
 xHQ=x^{191/96+o(1)}.
 \tag{3.5}
\]

It misses the target by

\[
 \frac{191}{96}-\frac{1997}{1200}=\frac{781}{2400}.
 \tag{3.6}
\]

Hence the bracket in (3.1), the mixed-plus-balanced fold in (3.3), and the
prime shell must remain inside one signed estimate.  Formula (3.3) is the
desired modulus-family object; it is an exact rewrite, not its estimate.

At $q=5,t=6$, take $\beta^\circ(t)=2$, and endpoint weights

\[
 (w(4),w(6),w(11))=(2,-1,3),\qquad K_H\equiv1
 \tag{3.7}
\]

on this finite fixture.  Directly using $5c'_5$ gives $10$.  The first
line of (3.1), after multiplication by $q\beta^\circ(t)$, is $20$, and
the compensating line is $10$, again giving $10$.  Changing
$1/(q-1)$ to $1/q$, deleting $k=0$, or dropping the unit restriction
breaks the identity.

## 4. Character packet and one Hilbert inner product

Extend Dirichlet characters modulo $q$ by zero on nonunits and put

\[
 W_{q,\chi}(\alpha)=
 \sum_{u\in I_x}w(u)\chi(u)e(+\alpha u),
 \tag{4.1}
\]

\[
 B^\circ_{q,\chi}(\alpha)=
 \sum_{t\in I_x}\beta^\circ(t)
 \overline{\chi(t)}e(-\alpha t).
 \tag{4.2}
\]

By V51 character orthogonality and Fourier separation,

\[
 \boxed{
 \mathfrak F_x^\circ=
 \sum_{q\in\mathcal Q}\frac q{q-1}
 \sum_{\substack{\chi\ ({\rm mod}\ q)\\\chi\ne\chi_0}}
 \int_{\mathbb R}\psi(v)
 W_{q,\chi}(v/H)B^\circ_{q,\chi}(v/H)\,dv.}
 \tag{4.3}
\]

Let $\mathscr H_x$ be the Hilbert packet with norm

\[
 \|Z\|_{\mathscr H_x}^2=
 \sum_{q\in\mathcal Q}\frac q{q-1}
 \sum_{\chi\ne\chi_0}
 \int_{\mathbb R}|\psi(v)|\,|Z(q,\chi,v)|^2\,dv.
 \tag{4.4}
\]

Define $\varepsilon_\psi(v)=\psi(v)/|\psi(v)|$ when
$\psi(v)\ne0$, and $0$ otherwise, and set

\[
 X(q,\chi,v)=\varepsilon_\psi(v)W_{q,\chi}(v/H),
 \qquad
 Y(q,\chi,v)=\overline{B^\circ_{q,\chi}(v/H)}.
 \tag{4.5}
\]

With the inner product linear in its first entry, (4.3) becomes

\[
 \boxed{\mathfrak F_x^\circ=\langle X,Y\rangle_{\mathscr H_x}.}
 \tag{4.6}
\]

Write

\[
 \mathcal E_W=\|X\|_{\mathscr H_x}^2,
 \qquad
 \mathcal E_B=\|Y\|_{\mathscr H_x}^2,
 \tag{4.7}
\]

and, when both norms are nonzero,

\[
 \varrho_{BW}=
 \frac{|\langle X,Y\rangle|}
 {\sqrt{\mathcal E_W\mathcal E_B}};
 \tag{4.8}
\]

put $\varrho_{BW}=0$ if either norm vanishes.  Then

\[
 0\leq\varrho_{BW}\leq1,
 \qquad
 |\mathfrak F_x^\circ|
 =\varrho_{BW}\sqrt{\mathcal E_W\mathcal E_B}.
 \tag{4.9}
\]

Equation (4.9) is an identity.  It is useful only because source theorems
normally attack the two marginal energies and the cross angle by different
mechanisms.  Defining $\varrho_{BW}$ is not an arithmetic estimate.

## 5. The diagonal scale and the exact endpoint law

For a coefficient sequence $a=(a_n)$, the literal character-diagonal
piece of the corresponding packet energy is

\[
 \mathcal D(a)=\|\psi\|_1
 \sum_{q\in\mathcal Q}\frac{q(q-2)}{q-1}
 \sum_{\substack{n\in I_x\\q\nmid n}}|a_n|^2.
 \tag{5.1}
\]

Indeed, for $q\nmid n$, exactly $q-2$ nonprincipal characters have
$|\chi(n)|^2=1$.  The divisor envelopes

\[
 \sum_{t\in I_x}|\beta^\circ(t)|^2
 +\sum_{u\in I_x}|w(u)|^2\ll x^{1+o(1)}
 \tag{5.2}
\]

therefore put both diagonal pieces at most at the benchmark

\[
 xQ^2=x^{5/3+o(1)}.
 \tag{5.3}
\]

The off-diagonal part of a packet energy can have either sign after
expansion, so (5.3) is not asserted as a lower bound for
$\mathcal E_B$ or $\mathcal E_W$.  `Diagonal-scale BDH` below means the
strong hypothetical upper bounds

\[
 \mathcal E_B,\mathcal E_W\ll x^{5/3+o(1)}.
 \tag{5.4}
\]

Even granting (5.4), ordinary Cauchy gives only

\[
 |\mathfrak F_x^\circ|\ll x^{5/3+o(1)},
 \tag{5.5}
\]

which misses (1.4) by exactly $1/400$.  Thus two marginal BDH estimates
at the natural diagonal scale do not close Gate A.

The complete endpoint ledger is as follows.  Suppose, for fixed
$\delta_B,\delta_W,\kappa\geq0$, that the same literal packets satisfy

\[
 \mathcal E_B\ll x^{5/3-\delta_B+o(1)},\qquad
 \mathcal E_W\ll x^{5/3-\delta_W+o(1)},
 \tag{5.6}
\]

\[
 \varrho_{BW}\ll x^{-\kappa+o(1)}.
 \tag{5.7}
\]

Then (4.9) gives

\[
 |\mathfrak F_x^\circ|
 \ll x^{5/3-\kappa-(\delta_B+\delta_W)/2+o(1)}.
 \tag{5.8}
\]

Consequently V51's whole-object hypothesis holds for every

\[
 0<\eta_L<
 \boxed{\kappa+\frac{\delta_B+\delta_W}{2}-\frac1{400}},
 \tag{5.9}
\]

provided the boxed quantity is positive.  Three endpoint regimes follow.

1. At diagonal-scale marginals, $\delta_B=\delta_W=0$, one needs
   $\kappa>1/400$.
2. With no angular gain, one needs
   $\delta_B+\delta_W>1/200$.
3. With only one super-diagonal marginal, its saving must exceed $1/200$.

If one marginal remains at the generic character-large-sieve exponent $2$
and the other reaches $5/3$, Cauchy gives $11/6$, missing the target by

\[
 \frac{11}{6}-\frac{1997}{1200}=\frac{203}{1200}.
 \tag{5.10}
\]

If both remain generic, the deficit is V51's

\[
 2-\frac{1997}{1200}=\frac{403}{1200}.
 \tag{5.11}
\]

The endpoint law (5.9) is exact, but its hypotheses are open.

## 6. Why marginal theorems cannot manufacture the angle

Separate norm information contains no information about
$\varrho_{BW}$.  In the two-dimensional real Hilbert fixture, let

\[
 X=(3,4),\qquad Y_+=(3,4),\qquad Y_0=(-4,3).
 \tag{6.1}
\]

Then

\[
 \|X\|^2=\|Y_+\|^2=\|Y_0\|^2=25,
 \tag{6.2}
\]

but

\[
 \langle X,Y_+\rangle=25,
 \qquad
 \langle X,Y_0\rangle=0.
 \tag{6.3}
\]

Thus any theorem package that sees only the two marginal energies accepts
both a parallel packet and an orthogonal packet.  It cannot imply a fixed
angular power.  This is a finite logical falsifier for a marginal-only
compiler, not a model of the arithmetic coefficients.

Likewise, a diagonal-majorant proof that expands either energy and takes
absolute values is naturally pinned at (5.3); it cannot claim a
sub-diagonal power merely because the original signed scalar might be small.
This is the precise scope of the no-go.  It does not rule out a genuine
super-BDH theorem for one special marginal, and it does not rule out a
joint dispersion theorem.

## 7. The selected whole-object theorem package

V52 names the source-facing sufficient package

\[
 \boxed{\mathsf H_{\rm PAD}(\delta_B,\delta_W,\kappa)}
 \tag{7.1}
\]

(`pair-angular dispersion') as the simultaneous validity of (5.6)--(5.7)
for the exact packets (4.1)--(4.5), with

\[
 \kappa+\frac{\delta_B+\delta_W}{2}>\frac1{400}.
 \tag{7.2}
\]

It is deliberately a joint theorem package.  The mixed and balanced lanes
are added before $\mathcal E_B$ is formed; the positive and compensating
parts of (3.1) are not separated; and the same prime shell, physical
$w=\Lambda(\cdot+2)-b_x^{(z)}$, hard shell, unit masks, square payment,
and normalization are retained.

The preferred first attack is the baseline-marginal/angular road

\[
 \delta_B=\delta_W=0,\qquad \kappa>\frac1{400},
 \tag{7.3}
\]

because the exact semiprime slice (2.3) makes a power saving below both
diagonal scales heuristically less plausible than a signed cross-dispersion
saving.  This is a route judgment, not a theorem.  A super-BDH marginal
package satisfying (7.2) remains a legal alternative.

Put

\[
 \eta_{\rm PAD}
 =\kappa+\frac{\delta_B+\delta_W}{2}-\frac1{400}.
 \tag{7.4}
\]

If $\mathsf H_{\rm PAD}$ holds and the independent V42 Gate-B theorem
holds with saving $\eta_B>0$, V43 yields the physical endpoint for every

\[
 0<\eta<\min\left\{
 \eta_{\rm PAD},\eta_B,\frac{419}{2400},
 \frac{19}{2400},\frac{11}{600}-\varepsilon
 \right\}.
 \tag{7.5}
\]

Gate B is not paid by (7.1), and Gate A is not paid by Gate B.  The V50
unbounded-Siegel-quality conditional exit remains logically prior; the V50
bounded-quality sequential core remains an alternative to (7.1).

## 8. Primary-source boundary

The screen below uses primary theorem texts current on 2026-08-11.

1. [Zheng, arXiv:2512.22798v1, Theorems 1.1--1.2](https://arxiv.org/pdf/2512.22798)
   is the closest simultaneous-progression architecture.  Theorem 1.1 uses
   fixed residues $a_1,a_2$, a well-factorable $d$-weight, and
   $q=x^\theta$ with $\theta\leq7/36$.  The quadrilinear Theorem 1.2
   requires fixed product residues, a Siegel--Walfisz short sequence, a rough
   factor, and $\theta\leq2/23$.  V52 has $\theta=1/3$, the residue
   $s\ell+2$ moves with the folded pair, and the literal endpoint is
   $\Lambda-b_x^{(z)}$.  The result is an architecture analogue, not a
   direct or conditional attachment to (3.3).

2. [Drappeau, arXiv:1504.05549v4, Theorem 5.1](https://arxiv.org/pdf/1504.05549)
   gives a deep dispersion theorem for fixed product congruences with
   modulus-independent divisor-bounded dyadic arrays.  Inverting
   $u-s\ell=qk$ makes the V52 residue and coefficients move together;
   opening them separately destroys the fold.  There is no literal
   attachment.

3. [Wright, arXiv:2604.25177v2](https://arxiv.org/abs/2604.25177)
   proves unbalanced fixed-residue convolution estimates when one short
   sequence has a Siegel--Walfisz property.  It neither accepts the reverse-
   Chen parity residual (2.2) nor provides the joint angle (5.7).

4. [Blomer--Pascadi, arXiv:2607.24311v1, Theorem 1.1](https://arxiv.org/abs/2607.24311)
   gives a $c^{-1/32+o(1)}$ saving for a fixed-modulus critical bilinear
   Kloosterman cell.  It remains a `SOURCE_BACKED_CONDITIONAL` local engine
   after a legal pair-native transform.  It does not provide the common-$q$
   emitter, packet norms, cross angle, or signed reassembly.

5. [Pascadi, arXiv:2404.04239v3](https://arxiv.org/abs/2404.04239)
   proves exceptional-Maass large sieves for special sparse-Fourier
   sequences and associated multilinear Kloosterman estimates.  It may be a
   horizontal engine after the exact transform species and norms are built;
   it does not prove (5.6)--(5.7) for the V52 packet.

No screened primary theorem controls the compensated moving-product
covariance (3.3) or supplies a power-saving angle for the literal pair and
physical endpoint.  The direct source attachment is therefore `NONE`.

## 9. Route decision and paper ledger

V52 advances the route in three ways.

1. It identifies one exact modulus-family object, (3.3), rather than a list
   of mixed, balanced, orientation, or character cells.
2. It identifies the arithmetic content as a reverse-Chen parity residual
   through the simultaneous identities (1.7) and (2.2).
3. It proves the endpoint budget (5.9) and the marginal-only no-go (6.1)--
   (6.3).  The new theorem must be joint unless the marginals themselves are
    super-diagonal by a total saving $>1/200$.

The first fatal is now

```text
NO_LITERAL_THEOREM_PROVES_A_POWER_SAVING_PAIR_ENDPOINT_ANGLE_OR_TOTAL_SUPER_BDH_SAVING_ABOVE_1_OVER_200_FOR_THE_COMPENSATED_MOVING_PRODUCT_PRIME_DILATION
```

This is still Bridge A / Gate A.  Arithmetic advance is `NO`, fixed atom
credit is $0$, strict $1/400$ is unpaid, `L2=NONE`, and
`TPC_207_TRIGGER=false`.

The paper-candidate ledger may promote the exact compensated dilation,
reverse-Chen slice, endpoint simplex, and marginal-only obstruction to
`PROVED` structural units.  The PAD theorem remains `CONJECTURAL`; the
source theorems remain analogues or conditional local engines.  This does
not meet the repository's numbered-paper gate.

## 10. Canonical V52 registry

```text
V52_MAXIMUM_CLAIM = EXACT_COMPENSATED_PAIR_DILATION_AND_PACKET_ENDPOINT_COMPILER_IDENTIFIES_THE_FOLDED_GATE_A_AS_A_REVERSE_CHEN_PARITY_RESIDUAL_AND_PROVES_THE_MARGINAL_BDH_PLUS_CAUCHY_COMPILER_MISSES_BY_1_OVER_400
V52_ROUTE_ADVANCE = YES
V52_CONDITIONAL_BRIDGE_ADVANCE = YES
V52_ARITHMETIC_ADVANCE = NO
V52_FIXED_ATOM_CREDIT = 0
V52_STRICT_1_OVER_400 = UNPAID
V52_L2 = NONE
V52_TPC_207_TRIGGER = false
V52_NUMBERED_RELEASE = NO
V52_DERIVATION_STATUS = COHERENT_AFTER_DUAL_PAIR_SIEVE_IDENTITY_COMPENSATED_DILATION_HILBERT_PACKET_AND_ENDPOINT_SIMPLEX
V52_ASSUMPTION_POLICY = PAIR_ANGULAR_DISPERSION_IS_CONJECTURAL__MARGINAL_AND_LOCAL_SOURCE_RESULTS_RECEIVE_NO_JOINT_CREDIT
V52_SELECTED_RESEARCH_ROUTE = UNBOUNDED_SIEGEL_QUALITY_CONDITIONAL_EXIT__OTHERWISE_PAIR_ANGULAR_GATE_A__V42_GATE_B__V43_JOIN__DYNAMICS_RESERVE
V52_CLAIM_CLASS_POLICY = PROVED__SOURCE_BACKED_CONDITIONAL__CONJECTURAL__NO_GO
V52_FROZEN_SCALES = H_21_OVER_32__Q_1_OVER_3__U_133_OVER_400__DILATION_31_OVER_96
V52_FOLDED_PAIR_INTERFACE = RETAINED_EXACT_MIXED_PLUS_BALANCED_OMEGA_U
V52_TRUNCATED_SIEVE_INTERFACE = RETAINED_EXACT_LAMBDA_OVER_LOG_MINUS_MU_LE_U_CONVOLUTION
V52_DUAL_COEFFICIENT_INTERFACE = PROVED_EXACT_SAME_BETA_AFTER_SQUARE_ROW_SUBTRACTION
V52_PRIME_ROW_CANCELLATION = PROVED_EXACT_ONE_MINUS_ONE_EQUALS_ZERO
V52_MIXED_SEMIPRIME_SLICE = PROVED_EXACT_ZERO_FOR_P_LE_U_LT_R
V52_BALANCED_SEMIPRIME_SLICE = PROVED_EXACT_MINUS_ONE_FOR_U_LT_P_LT_R
V52_SQUARE_PRIME_SLICE = PROVED_EXACT_MINUS_ONE_HALF
V52_REVERSE_CHEN_INTERPRETATION = PROVED_EXACT_SUBCHANNEL_NOT_A_STANDALONE_ESTIMATE
V52_MULTI_PAIR_T12_FIXTURE = PROVED_FORMAL_LOG_COLLAPSE_TO_ONE
V52_COMPENSATED_PAIR_DILATION_ROW = PROVED_EXACT_DIVISIBILITY_MINUS_UNIT_PRINCIPAL_MEAN
V52_COMPENSATED_PAIR_DILATION_SCALAR = PROVED_EXACT_ONE_COMMON_PRIME_SHELL_AND_ONE_SIGNED_AGGREGATE
V52_DILATION_NATURAL_LENGTH = H_OVER_Q_EQUALS_X_31_OVER_96
V52_DILATION_HARD_SUPPORT_POLICY = EXACT_T_PLUS_QK_IN_I_WITH_SCHWARTZ_NOT_COMPACT_K_TAIL
V52_DILATION_SPLIT_ABSOLUTE_CEILING = X_191_OVER_96_PLUS_O1
V52_DILATION_SPLIT_DEFICIT = 781_OVER_2400
V52_Q5_DILATION_FIXTURE = PROVED_EXACT_20_MINUS_10_EQUALS_10
V52_PAIR_CHARACTER_PACKET = RETAINED_EXACT_NONPRINCIPAL_CHARACTER_FOURIER_AGGREGATE
V52_HILBERT_PACKET_IDENTITY = PROVED_EXACT_F_CIRCLE_EQUALS_INNER_PRODUCT_X_Y
V52_PACKET_COHERENCE = DEFINED_EXACT_ZERO_TO_ONE_NO_ARITHMETIC_CREDIT
V52_CHARACTER_DIAGONAL_FORMULA = PROVED_EXACT_Q_Q_MINUS_2_OVER_Q_MINUS_1_WEIGHT
V52_DIAGONAL_SCALE = X_5_OVER_3_PLUS_O1_UPPER_BENCHMARK
V52_DIAGONAL_SCALE_LOWER_BOUND = NOT_ASSERTED_OFFDIAGONAL_CAN_HAVE_EITHER_SIGN
V52_MARGINAL_BDH_BASELINE = CONJECTURAL_E_B_AND_E_W_LE_X_5_OVER_3_PLUS_O1
V52_MARGINAL_BDH_PLUS_CAUCHY = NO_GO_MISSES_TARGET_BY_EXACT_1_OVER_400
V52_PACKET_ENDPOINT_LAW = PROVED_CONDITIONAL_KAPPA_PLUS_HALF_DELTA_SUM_MINUS_1_OVER_400
V52_BASELINE_MARGINAL_ANGULAR_THRESHOLD = KAPPA_GT_1_OVER_400
V52_ZERO_ANGLE_TOTAL_SUPER_BDH_THRESHOLD = DELTA_B_PLUS_DELTA_W_GT_1_OVER_200
V52_ONE_SIDED_SUPER_BDH_THRESHOLD = DELTA_GT_1_OVER_200
V52_ONE_GENERIC_ONE_BDH_DEFICIT = 203_OVER_1200
V52_TWO_GENERIC_CHARACTER_DEFICIT = 403_OVER_1200
V52_MARGINAL_NORMS_DETERMINE_ANGLE = NO_GO_PARALLEL_ORTHOGONAL_EQUAL_NORM_FIXTURE
V52_PAIR_ANGULAR_DISPERSION_GATE = CONJECTURAL_H_PAD_DELTA_B_DELTA_W_KAPPA
V52_PREFERRED_PAD_REGIME = DIAGONAL_SCALE_MARGINALS_AND_KAPPA_GT_1_OVER_400
V52_SUPER_BDH_REGIME = RETAINED_LEGAL_ALTERNATIVE_IF_TOTAL_SAVING_GT_1_OVER_200
V52_PAD_TO_V51_H_FOLD = PROVED_CONDITIONAL_WITH_ETA_PAD_POSITIVE
V52_PAD_TO_PHYSICAL_ENDPOINT = PROVED_CONDITIONAL_AFTER_INDEPENDENT_V42_GATE_B_AND_V43_JOIN
V52_TWO_GATE_MARGIN = MIN_ETA_PAD_ETA_B_419_OVER_2400_19_OVER_2400_AND_11_OVER_600_MINUS_EPSILON
V52_ZHENG_SIMULTANEOUS_AP = NO_GO_DIRECT_THETA_FIXED_RESIDUE_SIEGEL_WALFISZ_AND_MOVING_PRODUCT_MISMATCH
V52_DRAPPEAU_DISPERSION = NO_GO_DIRECT_FIXED_PRODUCT_AND_MODULUS_INDEPENDENT_ARRAY_MISMATCH
V52_WRIGHT_UNBALANCED_CONVOLUTION = NO_GO_DIRECT_FIXED_RESIDUE_AND_SHORT_SIEGEL_WALFISZ_SEQUENCE_MISMATCH
V52_BLOMER_PASCADI_FIXED_MODULUS = SOURCE_BACKED_CONDITIONAL_LOCAL_CELL_ONLY
V52_PASCADI_EXCEPTIONAL_SIEVE = SOURCE_BACKED_CONDITIONAL_AFTER_LITERAL_TRANSFORM_AND_NORM
V52_DIRECT_PRIMARY_SOURCE_FOR_H_PAD = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_11
V52_FIRST_FATAL = NO_LITERAL_THEOREM_PROVES_A_POWER_SAVING_PAIR_ENDPOINT_ANGLE_OR_TOTAL_SUPER_BDH_SAVING_ABOVE_1_OVER_200_FOR_THE_COMPENSATED_MOVING_PRODUCT_PRIME_DILATION
V52_V42_GATE_B = RETAINED_PARALLEL_OPEN_POSITIVE_GRAM_MPD_ROUTE
V52_V50_BOUNDED_CORE = RETAINED_SEQUENTIAL_CONJECTURAL_ALTERNATIVE
V52_PAPER_CANDIDATE_LEDGER = UPDATED_WITH_COMPENSATED_DILATION_REVERSE_CHEN_SLICE_ENDPOINT_SIMPLEX_AND_MARGINAL_NO_GO
V52_SMALL_PAPER_STATUS = UNNUMBERED_OUTLINE_ONLY_NO_STANDALONE_ASYMPTOTIC_THEOREM
V52_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_PAIR_ANGULAR_GATE_A_MAPPED_ARITHMETIC_BOUND_OPEN
V52_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V52_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATES_A_B
```
