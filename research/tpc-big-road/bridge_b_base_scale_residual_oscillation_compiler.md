# Bridge B V32: base-scale residual oscillation and quotient Fejer compiler

Status: unnumbered, fail-closed, exact-interface audit.  The maximum claim is

~~~text
EXACT_SINGLE_SCALE_ZERO_AXIS_QUOTIENTED_WIENER_CELL_COMPILER_FOR_THE_LITERAL_WHOLE_RESIDUAL
~~~

This artifact starts from the sealed V31 literal object.  It changes neither
the fixed physical gap nor any ordered Heath--Brown coefficient, MASTER route,
hybrid term, hard shell, Jutila normalization, or terminal covariance gate.
It replaces the two V31 B hypotheses by one strictly weaker whole-object
oscillation theorem at the single physical Fourier scale \(H=x^{21/32}\).
The compiler below is exact; the new oscillation estimate is open.  Hence no
arithmetic power saving is claimed.

## 1. Frozen whole residual and Fourier convention

Retain

\[
 \mathcal B_x(\alpha)=\sum_{t\in I_x}\beta_x^{\rm raw}(t)e(t\alpha),
 \qquad
 \mathcal W_x(\alpha)=\sum_{u\in I_x}w_x^{(z)}(u)e(u\alpha),
\tag{1.1}
\]

where

\[
 I_x=(x/2,x]\cap\mathbb Z,
 \qquad
 w_x^{(z)}(u)=\Lambda(u+2)-b_x^{(z)}(u).
\tag{1.2}
\]

Put

\[
 P_x(\alpha)=\mathcal B_x(\alpha)\overline{\mathcal W_x(\alpha)},
 \qquad
 r_x(h)=\int_{\mathbb T}P_x(\alpha)e(+h\alpha)\,d\alpha.
\tag{1.3}
\]

All circle measures are normalized Haar measures.  The plus sign in (1.3)
selects \(u=t+h\).

The occurrence-native V28--V31 carrier remains

\[
 L_x(\alpha)=\sum_{|h|<x/2}M_x^{\rm loc}(h)e(-h\alpha),
 \qquad
 M_x^{\rm loc}(0)=0.
\tag{1.4}
\]

Define the complete tagged residual

\[
 R_x(\alpha)=P_x(\alpha)-L_x(\alpha),
 \qquad
 e_x(h)=r_x(h)-M_x^{\rm loc}(h).
\tag{1.5}
\]

Then, on the full integer lattice,

\[
 \boxed{\widehat R_x(h)=e_x(h)},
 \qquad
 \widehat f(h):=\int_{\mathbb T}f(\alpha)e(+h\alpha)\,d\alpha.
\tag{1.6}
\]

In particular,

\[
 \widehat R_x(0)=e_x(0)=S_x^{\rm physical}.
\tag{1.7}
\]

The symbol \(h\) is a correlation shift.  The physical prime gap remains the
fixed \(h_0=2\) already built into \(w_x^{(z)}\).

## 2. Exact occurrence emitter

Let \(\mathcal O_x^{(1)}\) be the labelled root-\(s=1\) HB2 occurrences
whose product \(t_o\) lies in \(I_x\).  For every occurrence \(o\), define

\[
 a_o^M=
 \mathbf 1_{\operatorname{route}(o)=\mathrm{MASTER}}
 c_{j(o)}\prod_i\mu(e_i(o))
 \frac{\log f_1(o)}{\log t_o},
 \qquad c_1=+2,\quad c_2=-1.
\tag{2.1}
\]

For a MASTER occurrence put

\[
 \Delta_o(h)=\Delta_{m(o),z}(h),
\tag{2.2}
\]

and set \(\Delta_o=0\) outside MASTER if the masked all-route notation in
(2.1) is used.  The V19 coefficient and the V28 local carrier are exactly

\[
 \beta_x^{\rm raw}(t)
 =\mathbf 1_{t\in I_x}
  \sum_{\substack{o\in\mathcal O_x^{(1)}\\t_o=t}}a_o^M,
\tag{2.3}
\]

\[
 M_x^{\rm loc}(h)=
 \sum_{\substack{o\in\mathcal O_x^{(1)}\\
                   t_o,t_o+h\in I_x}}
 a_o^M\Delta_o(h).
\tag{2.4}
\]

Reindexing \(u=t_o+h\), with no triangle inequality, gives the literal
whole-object emitter

\[
 \boxed{
 R_x(\alpha)=
 \sum_{o\in\mathcal O_x^{(1)}}a_o^M
 \sum_{u\in I_x}
 \bigl[w_x^{(z)}(u)-\Delta_o(u-t_o)\bigr]
 e((t_o-u)\alpha).}
\tag{2.5}
\]

Consequently,

\[
 \boxed{
 e_x(h)=
 \sum_{\substack{o\in\mathcal O_x^{(1)}\\
                   t_o,t_o+h\in I_x}}
 a_o^M
 \bigl[w_x^{(z)}(t_o+h)-\Delta_o(h)\bigr].}
\tag{2.6}
\]

The sign in (2.6) is forced by the \(+h\) Fourier convention.  Both physical
indices lie in \(I_x\), so \(|h|<x/2\).  Unit slots, the ordered \(+2,-1\)
coefficients, all Mobius/log weights, and occurrence multiplicities remain.
An \(f_1=1\) row vanishes only through \(\log f_1=0\).  H2 routes are removed
only by the explicit MASTER mask.  Source roots \(s\ge2\) remain the separately
paid perfect-power branch and are not inserted into (2.5).  Prime and hybrid
terms remain combined inside \(w_x^{(z)}\).

Since \(\Delta_o(0)=0\), equation (2.6) at \(h=0\) reproduces (1.7), rather
than deleting the physical axis.

## 3. One base-scale quotient Wiener functional

Let

\[
 H=x^{21/32},
 \qquad
 Y_0=2^{\lceil\log_2H\rceil},
 \qquad H\le Y_0<2H.
\tag{3.1}
\]

For any integer \(Y\ge1\), partition the circle into the aligned half-open
cells

\[
 I_{Y,j}=\left[\frac j{2Y},\frac{j+1}{2Y}\right),
 \qquad 0\le j<2Y.
\tag{3.2}
\]

For one global complex constant \(c\), define

\[
 q_{Y,j}(R;c)=\int_{I_{Y,j}}|R(\alpha)-c|\,d\alpha
\tag{3.3}
\]

and

\[
 \boxed{
 \mathfrak Q_Y^{\rm osc}(R)=
 \inf_{c\in\mathbb C}
 Y\sum_{j=0}^{2Y-1}q_{Y,j}(R;c)^2.}
\tag{3.4}
\]

The objective in (3.4) is continuous and coercive because

\[
 Y\sum_jq_{Y,j}(R;c)^2
 \ge\frac12\left(\int_{\mathbb T}|R-c|\right)^2
 \ge\frac12\bigl(|c|-\|R\|_1\bigr)^2.
\tag{3.5}
\]

Thus its infimum is attained, although the later proof needs only minimizing
sequences.  The quotient is translation invariant:

\[
 \mathfrak Q_Y^{\rm osc}(R+C)=\mathfrak Q_Y^{\rm osc}(R)
 \quad(C\in\mathbb C).
\tag{3.6}
\]

Only one global constant is allowed.  Cell-dependent constants would create
nonzero Fourier modes and are illegal.  The minimizing constant may depend on
\(Y\): for every \(h\ne0\),

\[
 \widehat{R-c_Y}(h)=\widehat R(h),
\tag{3.7}
\]

so this scale-wise optimization can modify only the zero coordinate.  It is a
fixed quotient norm, not an adaptively selected arithmetic major set.

The single new arithmetic theorem selected by V32 is

\[
 \boxed{
 \mathfrak Q_{Y_0}^{\rm osc}(R_x)
 \ll x^{2+2\sigma+o(1)}
 \quad\hbox{for one fixed}\quad
 0\le\sigma<\frac{13}{4800}.}
\tag{3.8}
\]

Equation (3.8) is open for the literal emitter (2.5).

## 4. Fejer band-to-cell theorem

For \(N\ge1\), use the Fejer kernel

\[
 K_N(\theta)=
 \sum_{|r|<N}\left(1-\frac{|r|}{N}\right)e(r\theta)
 =\frac1N\left|\sum_{m=0}^{N-1}e(m\theta)\right|^2.
\tag{4.1}
\]

It obeys

\[
 K_N(\theta)\le
 \min\left\{N,\frac1{4N\|\theta\|_{\mathbb T}^2}\right\}.
\tag{4.2}
\]

The second bound follows from
\(|\sin\pi\theta|\ge2\|\theta\|_{\mathbb T}\).

Let \(f\in L^1(\mathbb T)\).  Since the weights in \(K_{2Y}\) are at least
\(1/2\) for \(|h|\le Y\),

\[
 \sum_{|h|\le Y}|\widehat f(h)|^2
 \le
 2\iint_{\mathbb T^2}
 f(\alpha)\overline{f(\beta)}K_{2Y}(\alpha-\beta)
 \,d\alpha\,d\beta.
\tag{4.3}
\]

For the cells (3.2), the same cell and its two circular neighbours cost at
most \(2Y\) each.  Cells at circular index distance \(d\ge2\) cost at most

\[
 \frac{Y}{2(d-1)^2}.
\tag{4.4}
\]

Hence the absolute cell-kernel matrix has row sum

\[
 <6Y+Y\sum_{m\ge1}\frac1{m^2}<8Y.
\tag{4.5}
\]

Schur's test in (4.3) gives the safe exact interface

\[
 \boxed{
 \sum_{|h|\le Y}|\widehat f(h)|^2
 \le16Y\sum_{j=0}^{2Y-1}
 \left(\int_{I_{Y,j}}|f(\alpha)|\,d\alpha\right)^2.}
\tag{4.6}
\]

Apply (4.6) to \(f=R_x-c\), discard its zero Fourier coefficient, and take
the infimum over \(c\).  This proves

\[
 \boxed{
 \sum_{0<|h|\le Y}|e_x(h)|^2
 \le16\mathfrak Q_Y^{\rm osc}(R_x).}
\tag{4.7}
\]

The constant (16) is deliberately retained even though a dual large-sieve
argument gives (8) under the same aligned-cell convention.

## 5. Dyadic refinement and complete Schwartz reassembly

Every \(I_{Y,j}\) is the disjoint union of \(I_{2Y,2j}\) and
\(I_{2Y,2j+1}\).  For fixed \(c\),

\[
 q_{Y,j}(R;c)
 =q_{2Y,2j}(R;c)+q_{2Y,2j+1}(R;c).
\tag{5.1}
\]

Therefore

\[
 \boxed{
 \mathfrak Q_{2Y}^{\rm osc}(R)
 \le2\mathfrak Q_Y^{\rm osc}(R).}
\tag{5.2}
\]

Indeed, use a minimizing sequence for the right side and
\(q_1^2+q_2^2\le(q_1+q_2)^2\).  Iteration gives

\[
 \mathfrak Q_{2^kY_0}^{\rm osc}(R_x)
 \le2^k\mathfrak Q_{Y_0}^{\rm osc}(R_x).
\tag{5.3}
\]

For every fixed \(A>1\), smoothness of the frozen bump gives

\[
 |\widehat\psi_+(h/H)|
 \ll_A(1+|h|/H)^{-A}.
\tag{5.4}
\]

The innermost block \(0<|h|\le Y_0\) is bounded by (4.7).  On the \(k\)-th
shell \(2^{k-1}Y_0<|h|\le2^kY_0\), equations (4.7), (5.3), and (5.4) give

\[
 \sum_{2^{k-1}Y_0<|h|\le2^kY_0}
 |\widehat\psi_+(h/H)|\,|e_x(h)|^2
 \ll_{A}2^{-A(k-1)}2^k
 \mathfrak Q_{Y_0}^{\rm osc}(R_x).
\tag{5.5}
\]

The series converges for \(A>1\).  Since the physical difference support is
\(|h|<x/2\), this pays every shell without treating \(H\) as hard support:

\[
 \boxed{
 \sum_{0<|h|<x/2}
 |\widehat\psi_+(h/H)|\,|e_x(h)|^2
 \ll_{\psi}
 \mathfrak Q_{Y_0}^{\rm osc}(R_x).}
\tag{5.6}
\]

Thus (3.8) implies

\[
 \mathcal N_e:=
 \left(
 \sum_{0<|h|<x/2}
 |\widehat\psi_+(h/H)|\,|e_x(h)|^2
 \right)^{1/2}
 \ll x^{1+\sigma+o(1)}.
\tag{5.7}
\]

Using the already frozen prime-shell coefficient norm,

\[
 \boxed{
 |E(e_x)|
 \ll x^{191/192+\sigma+o(1)}
 =x^{399/400-\eta_E+o(1)},
 \qquad
 \eta_E=\frac{13}{4800}-\sigma>0.}
\tag{5.8}
\]

Endpoint equality is not allowed.

## 6. Strict relation to the V31 pair

Let the V31 model major and minor be
\(\mathfrak M_\lambda\) and \(\mathfrak m_\lambda\), with
\(\lambda=x^{1+\nu}\).  Write

\[
 \mathscr D_\lambda
 =\int_{\mathfrak M_\lambda}|R_x|^2,
\tag{6.1}
\]

and on a \(Y\)-cell set

\[
 C_{Y,j}=
 \|\mathcal B_x\|_{L^2(I_{Y,j}\cap\mathfrak m_\lambda)}
 \|\mathcal W_x\|_{L^2(I_{Y,j}\cap\mathfrak m_\lambda)}.
\tag{6.2}
\]

Taking \(c=0\), split each cell integral of \(|R_x|\) into the major
\(|P_x-L_x|\), minor \(|P_x|\), and minor \(|L_x|\) pieces.  Cell
Cauchy--Schwarz and Minkowski give

\[
 \boxed{
 \sqrt{\mathfrak Q_Y^{\rm osc}(R_x)}
 \le
 \sqrt{\frac{\mathscr D_\lambda}{2}}
 +\sqrt{Y\|C_Y\|_1\|C_Y\|_\infty}
 +\frac{\lambda}{\sqrt2}.}
\tag{6.3}
\]

Hence the two V31 hypotheses imply (3.8) with

\[
 \sigma=\max\{\nu,\sigma_c\}.
\tag{6.4}
\]

The converse is false.  On one cell, put two factors on disjoint subatoms.
Then \(P=\mathcal B\overline{\mathcal W}=0\), and with \(L=0\) the V32
functional vanishes, while the marginal product
\(\|\mathcal B\|_2\|\mathcal W\|_2\) is arbitrarily large.  Moreover a narrow
spike can have small cell \(L^1\)-square but arbitrarily larger \(L^2\)
energy.  Thus (3.8) is a sufficient whole-object replacement that is strictly
weaker than the V31 pair; it is not an equivalent reformulation of either V31
hypothesis or of full Parseval energy.

Requiring the same-size bound for all \(H\le Y\le x\) would overpay: at a
terminal \(Y\asymp x\), the finite spectrum makes (4.7) comparable to the
full unweighted off-zero \(L^2\) norm.  Equations (5.2)--(5.6) are precisely
why V32 asks only for the one base scale.

## 7. Zero axis and unchanged terminal gate

If \(R_x(\alpha)\equiv T\), then

\[
 \mathfrak Q_{Y_0}^{\rm osc}(R_x)=0,
 \qquad
 \widehat R_x(h)=0\ (h\ne0),
 \qquad
 \widehat R_x(0)=T.
\tag{7.1}
\]

Therefore the quotient compiler yields exactly zero information about the
physical scalar.  The V28--V31 identity remains

\[
 S_x^{\rm physical}=J(e_x)+E(e_x).
\tag{7.2}
\]

The \(q\)-local terminal decomposition is also unchanged:

\[
 J(e_x)=\mathfrak R_x^{q\mathrm{loc}}+O(x^{95/96+o(1)}).
\tag{7.3}
\]

If, independently,

\[
 |\mathfrak R_x^{q\mathrm{loc}}|
 \ll x^{399/400-\eta_R}
 \quad(\eta_R>0),
\tag{7.4}
\]

then a conditional final saving may use any

\[
 \boxed{
 0<\eta_*<
 \min\left\{
 \eta_R,\frac{19}{2400},
 \frac{13}{4800}-\sigma
 \right\}.}
\tag{7.5}
\]

Gate B remains the research priority, but it does not pay terminal gate A.

## 8. Primary-source boundary

The Fejer and refinement compiler (4.1)--(5.6) is repository-derived and
elementary.  The current primary-source screen is finite and fail-closed as
of 2026-08-08:

1. Matomaki--Radziwill--Tao,
   [arXiv:1707.01315v3](https://arxiv.org/abs/1707.01315v3), Proposition 3.1
   and equation (54), accepts arbitrary finite coefficient pairs and a
   measurable major portion.  It does not estimate the quotient cell-square
   of the already combined residual \(P_x-L_x\).  Its applied estimates use
   standard \(\Lambda,d_k\) or listed Type-I/II objects.
2. Guth--Maynard,
   [arXiv:2405.20552v2](https://arxiv.org/abs/2405.20552v2), Theorem 1.1,
   bounds large values of multiplicative-phase Dirichlet polynomials
   \(\sum b_nn^{it}\).  It is not an additive base-cell theorem for (2.5).
3. Harper,
   [arXiv:2412.19644v1](https://arxiv.org/abs/2412.19644v1), Theorems 1--2,
   gives BDH-type variance statements for one general sequence under explicit
   sparsity/non-concentration hypotheses and averages over moduli and residue
   classes.  It does not control the signed product-model residual in every
   frequency cell.
4. Bazin,
   [arXiv:2607.15137v1](https://arxiv.org/abs/2607.15137v1), Theorems 2 and 8,
   treats particular finite Type-I/II convolution classes in narrow rational
   tubes and averages over moduli/characters.  No literal tag-preserving map
   from (2.5), nor a quotient Wiener estimate, is supplied.
5. Granville--Lamzouri,
   [arXiv:2604.02306v1](https://arxiv.org/abs/2604.02306v1), Theorem 1.1,
   concerns a single 1-bounded multiplicative coefficient at additive large
   values.  Neither literal factor in (2.5) belongs to that class.

Marginal large-value theorems do not imply a collective estimate for
\(P_x-L_x\).  No screened theorem accepts the ordered \(+2,-1\) occurrence
emitter, shifted hybrid term, hard shell, axes, and one outer norm and proves
(3.8).  Consequently

\[
 \boxed{
 \text{V32 first fatal: no source-backed bound for }
 \mathfrak Q_{Y_0}^{\rm osc}(R_x).}
\tag{8.1}
\]

## 9. Finite fixtures and no-go ledger

The checker freezes the following exact type diagnostics.

1. On normalized \(\mathbb Z/4\mathbb Z\), take
   \(P=(5,1,-1,3)\), \(L=(2,1,-2,-1)\), and
   \(R=P-L=(3,0,1,4)\).  In the singleton-cell \(Y=2\) analogue the minimizing
   constant is \(c=2\),

   \[
   \mathfrak Q_2^{\rm osc}(R)=\frac54,
   \qquad
   \sum_{h\ne0}|\widehat R(h)|^2=\frac52.
   \tag{9.1}
   \]

   The uncentered cell value is \(13/4\).
2. Adding any constant to all four entries leaves \(5/4\) unchanged.  A
   constant vector has quotient value zero but an arbitrary zero Fourier
   coordinate.
3. A rational nested eight-atom fixture verifies
   \(\mathfrak Q_{2Y}^{\rm osc}\le2\mathfrak Q_Y^{\rm osc}\), including the
   normalization factor \(Y\).
4. On a two-atom cell, disjoint supports of \(\mathcal B\) and
   \(\mathcal W\) make \(P=0\) but leave the marginal \(L^2\)-product
   positive.
5. A width-\(\varepsilon\) spike has \(L^2\)-to-cell-square ratio
   \(1/(Y\varepsilon)\), so full Parseval energy cannot be inferred from one
   base-scale cell-square.
6. A signed finite occurrence table recomputes (2.5)--(2.6) with the
   \(+h\) Fourier convention and rejects the opposite sign or a deleted
   MASTER mask.

These fixtures establish typing and strictness only.  They provide no growing
arithmetic estimate.

## 10. Canonical registry and next theorem

~~~text
V32_MAXIMUM_CLAIM = EXACT_SINGLE_SCALE_ZERO_AXIS_QUOTIENTED_WIENER_CELL_COMPILER_FOR_THE_LITERAL_WHOLE_RESIDUAL
V32_ROUTE_ADVANCE = YES
V32_ARITHMETIC_ADVANCE = NO
V32_FIXED_ATOM_CREDIT = 0
V32_STRICT_1_OVER_400 = UNPAID
V32_L2 = NONE
V32_TPC_207_TRIGGER = false
V32_NUMBERED_RELEASE = NO
V32_SELECTED_RESEARCH_ROUTE = B_SINGLE_SCALE_RESIDUAL_OSCILLATION_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK
V32_WHOLE_OBJECT_SPACE = SAME_LITERAL_TAGGED_P_MINUS_OCCURRENCE_NATIVE_L
V32_LITERAL_OCCURRENCE_EMITTER = PROVED_EXACT_MASTER_MASKED_PLUS2_MINUS1_MOBIUS_LOG_HYBRID_FORM
V32_FOURIER_COEFFICIENT_IDENTITY = PROVED_EXACT_HAT_R_PLUS_H_EQUALS_E_H
V32_PHYSICAL_DIFFERENCE_SUPPORT = PROVED_EXACT_ABS_H_LESS_THAN_X_OVER_2
V32_BASE_SCALE = Y0_SMALLEST_DYADIC_WITH_H_LE_Y0_LESS_THAN_2H
V32_ALIGNED_CELL_PARTITION = PROVED_EXACT_2Y_HALF_OPEN_CELLS
V32_GLOBAL_CONSTANT_QUOTIENT = PROVED_EXACT_COMPLEX_ONE_CONSTANT_PER_SCALE
V32_QUOTIENT_INFIMUM = PROVED_ATTAINED_CONTINUOUS_COERCIVE
V32_QUOTIENT_TRANSLATION_INVARIANCE = PROVED_EXACT_ZERO_FOURIER_ONLY
V32_CELL_DEPENDENT_CONSTANTS = STOP_SCOPED_NONZERO_FOURIER_CONTAMINATION
V32_FEJER_KERNEL = PROVED_EXACT_POSITIVE_TRIANGULAR_KERNEL
V32_FEJER_BAND_CELL_BOUND = PROVED_EXACT_SAFE_CONSTANT_16
V32_DYADIC_REFINEMENT = PROVED_EXACT_Q_2Y_LE_2_Q_Y
V32_SINGLE_SCALE_TO_ALL_SCHWARTZ_SHELLS = PROVED_EXACT_A_GREATER_THAN_1_GEOMETRIC_REASSEMBLY
V32_BASE_SCALE_OSCILLATION_BOUND = SELECTED_PRIMARY_OPEN_NEW_THEOREM
V32_BASE_SCALE_OSCILLATION_EXPONENT = OPEN_SIGMA_STRICTLY_BELOW_13_OVER_4800
V32_WEIGHTED_RESIDUAL_NORM = PROVED_CONDITIONAL_X_1_PLUS_SIGMA
V32_E_ERROR_EXPONENT = PROVED_CONDITIONAL_191_OVER_192_PLUS_SIGMA
V32_E_ENDPOINT_MARGIN = PROVED_EXACT_13_OVER_4800_MINUS_SIGMA
V32_V31_PAIR_IMPLIES_V32_GATE = PROVED_EXACT_MINKOWSKI_CELL_COMPILER
V32_V32_GATE_IMPLIES_V31_PAIR = STOP_SCOPED_DISJOINT_FACTOR_AND_NARROW_SPIKE_FALSIFIERS
V32_FULL_PARSEVAL_EQUIVALENCE = STOP_SCOPED_SINGLE_BASE_SCALE_ONLY
V32_UNIFORM_ALL_SCALE_SAME_BOUND = STOP_SCOPED_TERMINAL_SCALE_OVERPAYMENT
V32_ZERO_AXIS_FIREWALL = PROVED_EXACT_CONSTANT_RESIDUAL_HAS_Q_ZERO_AND_AXIS_ARBITRARY
V32_OFFZERO_B_ALONE = STOP_SCOPED_TERMINAL_A_SURVIVES
V32_QLOCAL_MODEL_BOUND = RETAINED_PROVED_ELEMENTARY_X_95_OVER_96_PLUS_O1
V32_A_TERMINAL_COVARIANCE = RETAINED_SELECTED_TERMINAL_OPEN_NEW_THEOREM
V32_CONDITIONAL_ENDPOINT_FORMULA = MIN_ETA_R_19_OVER_2400_13_OVER_4800_MINUS_SIGMA
V32_MRT_DIRECT_ATTACHMENT = STOP_SCOPED_NO_LITERAL_RESIDUAL_OSCILLATION_BOUND
V32_GUTH_MAYNARD_DIRECT_ATTACHMENT = STOP_SCOPED_MULTIPLICATIVE_PHASE_MARGINAL_LARGE_VALUES
V32_HARPER_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_SINGLE_SEQUENCE_MODULUS_AVERAGE_WRONG_NORM
V32_BAZIN_DIRECT_ATTACHMENT = STOP_SCOPED_TYPE_I_II_RATIONAL_TUBES_NO_LITERAL_EMITTER
V32_GRANVILLE_LAMZOURI_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_BOUNDED_MULTIPLICATIVE_WRONG_COEFFICIENT
V32_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V32_NEXT_THEOREM = BASE_SCALE_COLLECTIVE_OSCILLATION_FOR_LITERAL_MASTER_HYBRID_OCCURRENCE_EMITTER
V32_FIRST_FATAL = BASE_SCALE_COLLECTIVE_OSCILLATION_BOUND_FOR_LITERAL_MASTER_HYBRID_OCCURRENCE_EMITTER
V32_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
V32_PROVENANCE_CASCADE = REQUIRED
~~~

The next action is one theorem, not another decomposition: prove (3.8) for
the exact signed emitter (2.5), with one global constant quotient and one
collective outer norm.  No occurrencewise, prime/hybrid, or cell-selection
triangle may be substituted.  Until that theorem and terminal gate (7.4) are
both paid, arithmetic advancement, fixed-atom credit, strict \(1/400\), L2,
TPC-207, and a numbered release all remain forbidden.
