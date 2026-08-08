# Bridge B V31: whole-object major mismatch and terminal compiler

Status: unnumbered, fail-closed, exact-interface audit.  The maximum claim is

~~~text
EXACT_WHOLE_OBJECT_MODEL_LEVEL_MAJOR_ATTACHMENT_COMPILER_PLUS_CONDITIONAL_ENDPOINT_BUDGET_PLUS_EQUIVARIANT_QUOTIENT_NO_GO
~~~

This artifact starts from the sealed V30 literal object.  It does not change
the physical shift, the ordered Heath--Brown rows, the MASTER/H2 routing, the
hybrid subtraction, or the Jutila prime shell.  Its purpose is to replace the
opaque statement `MT=Mloc+a` by an exact whole-object construction with a
single, auditable Parseval payment.  No estimate proved below implies an
arithmetic power saving by itself.

## 1. Frozen object and Fourier convention

Let

\[
 \mathcal B_x(\alpha)=\sum_{t\in I_x}\beta_x^{\rm raw}(t)e(t\alpha),
 \qquad
 \mathcal W_x(\alpha)=\sum_{u\in I_x}w_x^{(z)}(u)e(u\alpha),
\tag{1.1}
\]

where

\[
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

The plus sign is forced: the integrand contains
\(e((t-u+h)\alpha)\), so (1.3) selects \(u=t+h\).  All measures on
\(\mathbb T\) are normalized Haar measures.

The V28--V30 occurrence-native local carrier is retained on the finite physical
difference lattice and is extended by zero outside it.  Define its spectrum

\[
 L_x(\alpha)=\sum_{|h|<x/2}M_x^{\rm loc}(h)e(-h\alpha).
\tag{1.4}
\]

Then

\[
 M_x^{\rm loc}(h)=\int_{\mathbb T}L_x(\alpha)e(+h\alpha)\,d\alpha,
 \qquad M_x^{\rm loc}(0)=0.
\tag{1.5}
\]

The tagged residual is

\[
 e_x(h)=r_x(h)-M_x^{\rm loc}(h),
 \qquad e_x(0)=S_x^{\rm physical}.
\tag{1.6}
\]

## 2. Canonical model-only level major

Fix once and for all

\[
 0<\nu<\frac{13}{4800},
 \qquad \lambda_x=x^{1+\nu}.
\tag{2.1}
\]

Before inspecting \(P_x-L_x\), any cell energy, or the target scalar, declare

\[
 \mathfrak M_\lambda
 =\{\alpha\in\mathbb T:|L_x(\alpha)|>\lambda_x\},
 \qquad
 \mathfrak m_\lambda=\mathbb T\setminus\mathfrak M_\lambda.
\tag{2.2}
\]

This hard major is determined by the frozen model \(L_x\), not by a detected
common spike of \(\mathcal B_x\) and \(\mathcal W_x\).  Equality belongs to the
minor side.  Any later enlargement of \(\mathfrak M_\lambda\) is outside the
canonical contract.

Define, with the same plus-sign Fourier coefficient,

\[
 MT_{\lambda,h}
 =\widehat{\mathbf1_{\mathfrak M_\lambda}P_x}(h),
\tag{2.3}
\]

\[
 a_{\lambda}(h)
 =\widehat{\mathbf1_{\mathfrak M_\lambda}P_x-L_x}(h),
 \qquad
 n_{\lambda}(h)
 =\widehat{\mathbf1_{\mathfrak m_\lambda}P_x}(h).
\tag{2.4}
\]

The parentheses matter: \(a_\lambda\) is the transform of
\(\mathbf1_{\mathfrak M}P_x-L_x\), not the transform of
\(\mathbf1_{\mathfrak M}(P_x-L_x)\).

## 3. Exact attachment and residual identities

Equations (1.5), (2.3), and (2.4) give on the full lattice

\[
 \boxed{MT_{\lambda,h}=M_x^{\rm loc}(h)+a_\lambda(h).}
\tag{3.1}
\]

Also

\[
 \boxed{e_x(h)=n_\lambda(h)+a_\lambda(h).}
\tag{3.2}
\]

These are exact identities, not estimates.  They do not pay the attachment:
the analytic content is the norm of the uniquely emitted defect
\(a_\lambda\).

Although \(P_x\) and \(L_x\) are finite trigonometric polynomials, sharp
masking generally makes \(a_\lambda\) and \(n_\lambda\) infinite-support
\(\ell^2\) Fourier sequences.  The endpoint reassembly uses only
\(0<|h|<x/2\); the full Parseval norm below is a stronger sufficient bound,
not an equivalent reformulation of the weighted finite-window attachment.

At the zero coordinate,

\[
 a_\lambda(0)=MT_{\lambda,0},
 \qquad
 n_\lambda(0)=S_x^{\rm physical}-MT_{\lambda,0},
\tag{3.3}
\]

and hence

\[
 \boxed{S_x^{\rm physical}=a_\lambda(0)+n_\lambda(0).}
\tag{3.4}
\]

No zero-axis cancellation or arithmetic credit has occurred.

## 4. Parseval major-mismatch interface

On the two disjoint pieces of the circle,

\[
 \mathbf1_{\mathfrak M_\lambda}P_x-L_x
 =\begin{cases}
 P_x-L_x,&\alpha\in\mathfrak M_\lambda,\\
 -L_x,&\alpha\in\mathfrak m_\lambda.
 \end{cases}
\tag{4.1}
\]

Parseval therefore gives the exact whole-object identity

\[
 \boxed{
 \sum_h|a_\lambda(h)|^2
 =\int_{\mathfrak M_\lambda}|P_x-L_x|^2\,d\alpha
  +\int_{\mathfrak m_\lambda}|L_x|^2\,d\alpha.}
\tag{4.2}
\]

Set

\[
 \mathscr D_\lambda(x)
 =\int_{\mathfrak M_\lambda}|P_x-L_x|^2\,d\alpha.
\tag{4.3}
\]

Because \(|L_x|\le\lambda_x\) on the minor side,

\[
 \int_{\mathfrak m_\lambda}|L_x|^2\,d\alpha
 \le\lambda_x^2=x^{2+2\nu}.
\tag{4.4}
\]

Thus the former opaque attachment gate has been reduced to the explicit open
theorem

\[
 \boxed{\mathscr D_\lambda(x)\ll x^{2+2\nu+o(1)}.}
\tag{4.5}
\]

If (4.5) holds, then

\[
 \|a_\lambda\|_{\ell^2}\ll x^{1+\nu+o(1)}.
\tag{4.6}
\]

The Jutila bump is nonnegative with integral one, so
\(|\widehat\psi_+(\xi)|\le1\); hence (4.6) dominates the required off-zero
weighted norm.  This is a compiler theorem only: (4.5) remains unproved for
the literal physical coefficients.

## 5. Minor cell-product compiler

For each dyadic \(H\le Y\le x\), partition \(\mathbb T\) into the half-open
cells

\[
 I_{Y,j}=\left[\frac j{2Y},\frac{j+1}{2Y}\right),
 \qquad 0\le j<2Y.
\tag{5.1}
\]

On the same fixed minor set define

\[
 u_{Y,j}=\|\mathcal B_x\|_{L^2(I_{Y,j}\cap\mathfrak m_\lambda)},
 \quad
 v_{Y,j}=\|\mathcal W_x\|_{L^2(I_{Y,j}\cap\mathfrak m_\lambda)},
 \quad c_{Y,j}=u_{Y,j}v_{Y,j}.
\tag{5.2}
\]

The V30 partition geometry and Cauchy--Schwarz give

\[
 P_0\le\|c_Y\|_1\ll x^{1+o(1)},
 \qquad P_Y\le3\|c_Y\|_\infty.
\tag{5.3}
\]

MRT, arXiv:1707.01315v3, Proposition 3.1 and equation (54), then imply

\[
 \sum_{|h-h_*|\le Y}|n_\lambda(h)|^2
 \ll3Y\|c_Y\|_1\|c_Y\|_\infty.
\tag{5.4}
\]

for every integer center \(h_*\).  The quantifier is part of the source-backed
abstract interface; no special shift is silently selected.

The remaining literal minor theorem is: for one fixed \(\sigma_c\), uniformly
for every dyadic \(H\le Y\le x\),

\[
 \boxed{
 \|c_Y\|_\infty
 \ll\frac{x^{1+2\sigma_c+o(1)}}Y
 \quad(H\le Y\le x),}
\tag{5.5}
\]

uniformly on the original tagged pair.  Existing source applications of MRT
do not prove (5.5) for \(\beta_x^{\rm raw}\) and
\(\Lambda(\cdot+2)-b_x^{(z)}\).

## 6. B aggregate exponent and endpoint

Let

\[
 \sigma_B=\max\{\nu,\sigma_c\}.
\tag{6.1}
\]

The weighted reassembly is elementary and is included here rather than assumed.
For every fixed \(A>1\), smoothness of the frozen bump gives

\[
 |\widehat\psi_+(h/H)|\ll_A(1+|h|/H)^{-A}.
\tag{6.2}
\]

Choose a dyadic \(Y_0\in[H,2H)\).  Handle the innermost block
\(0<|h|\le Y_0\) directly by (5.4)--(5.5) with \(h_*=0\) and
\(Y=Y_0\).  For \(k\ge1\), apply the same bounds with
\(Y=2^kY_0\) to the shells
\(2^{k-1}Y_0<|h|\le2^kY_0\).  Each unweighted prefix is
\(\ll x^{2+2\sigma_c+o(1)}\), while (6.2) contributes
\(O_A(2^{-A(k-1)})\) on the \(k\)-th shell.  Summing until
\(|h|<x/2\) gives

\[
 \left(
 \sum_{0<|h|<x/2}|\widehat\psi_+(h/H)|\,|n_\lambda(h)|^2
 \right)^{1/2}
 \ll x^{1+\sigma_c+o(1)}.
\tag{6.3}
\]

Combining (4.6), (6.3), and the weighted \(\ell^2\) triangle inequality in
(3.2) gives

\[
 \left(
 \sum_{0<|h|<x/2}|\widehat\psi_+(h/H)|\,|e_x(h)|^2
 \right)^{1/2}
 \ll x^{1+\sigma_B+o(1)}.
\tag{6.4}
\]

The strict B condition is

\[
 \boxed{\sigma_B<\frac{13}{4800}.}
\tag{6.5}
\]

Under (6.5), the V27 coefficient norm pays

\[
 |E(e_x)|
 \ll x^{191/192+\sigma_B+o(1)}
 =x^{399/400-\eta_E+o(1)},
\tag{6.6}
\]

where

\[
 \eta_E=\frac{13}{4800}-\sigma_B>0.
\tag{6.7}
\]

Endpoint equality is not allowed.  Any auxiliary smoothing or reassembly loss
must be included inside \(\sigma_B\), rather than hidden in an \(o(1)\) term.

## 7. Formula-predeclared large-spectrum variant

There is a stronger exact decomposition, retained only as a scoped survivor:

\[
 \mathfrak M_*
 =\{|L_x|>x^{1+\nu}\}
  \cup\{|\mathcal B_x|>x^{1/2+\nu}\}
  \cup\{|\mathcal W_x|>x^{1/2+\nu}\}.
\tag{7.1}
\]

If this formula is frozen before cells are inspected, then on its complement

\[
 c_{Y,j}\le\frac{x^{1+2\nu}}{2Y},
\tag{7.2}
\]

so the minor cross-flatness gate is automatic.  The whole B gate would reduce
to

\[
 \int_{\mathfrak M_*}|P_x-L_x|^2\,d\alpha
 \ll x^{2+2\nu+o(1)}.
\tag{7.3}
\]

However \(\mathfrak M_*\) depends on the physical factor
\(\mathcal W_x\).  It is therefore not the canonical model-only major and
receives zero theorem credit.  It is a legitimate formula-predeclared
conditional compiler only if this dependence is explicitly accepted and
(7.3) is independently proved.  Moving cells after seeing a common spike is
still forbidden.

## 8. Terminal A gate and conditional closure

V30 gives the exact normal form

\[
 J(e_x)=\mathfrak R_x^{q\mathrm{loc}}
       +O(x^{95/96+o(1)}),
 \qquad
 \frac{399}{400}-\frac{95}{96}=\frac{19}{2400}.
\tag{8.1}
\]

The terminal theorem remains

\[
 |\mathfrak R_x^{q\mathrm{loc}}|
 \ll x^{399/400-\eta_R},
 \qquad \eta_R>0.
\tag{8.2}
\]

If (4.5), (5.5), (6.5), and (8.2) all hold on the same literal object, then

\[
 \boxed{
 |S_x^{\rm physical}|
 \ll x^{399/400-\eta_*+o(1)},}
\tag{8.3}
\]

for every

\[
 \boxed{
 0<\eta_*<
 \min\left\{\eta_R,\frac{19}{2400},
                    \frac{13}{4800}-\sigma_B\right\}.}
\tag{8.4}
\]

This is an exact conditional implication, not an arithmetic advance.  Once B
is paid, \(S=J+E\) and \(J=S-E\) make the strict-power A theorem
terminal-equivalent to the physical theorem.

## 9. Finite fixtures and no-go ledger

On normalized \(\mathbb Z/4\mathbb Z\), take

\[
 P=(5,1,-1,3),\qquad L=(2,1,-2,-1),\qquad
 \lambda=\frac32,qquad \mathfrak M=\{0,2\}.
\tag{9.1}
\]

With the plus-sign normalized DFT,

\[
 r(0)=2,\quad \widehat L(0)=0,\quad MT(0)=1,
 \quad a(0)=1,\quad n(0)=1,\quad e(0)=2.
\tag{9.2}
\]

Parseval gives exactly

\[
 \sum_h|a(h)|^2
 =3=\frac52+\frac12
 =\int_{\mathfrak M}|P-L|^2
  +\int_{\mathfrak m}|L|^2.
\tag{9.3}
\]

The mutation \(a=\widehat{\mathbf1_{\mathfrak M}(P-L)}\) fails (3.1)--(4.2).

Two universal four-point falsifiers remain.  With \(L=0\) and a fixed
nontrivial hard set, for example \(\mathfrak M=\{0\}\subset\mathbb Z/4\mathbb Z\),
a physical atom placed in the major side makes the minor term zero but
leaves \(a(0)\ne0\); the same atom placed in the minor side makes \(a=0\) but
leaves \(n(0)\ne0\).  Hence no hard-set algebra alone pays both B pieces or the
terminal A gate.

The V30 translation-equivariant quotient no-go is unchanged: exact point
evaluation on the full cyclic coordinate space forces an equivariant quotient
to be injective, with \(\kappa=N\) and \(\kappa_0=N-1\).  The finite
\(q=5\) kernel remains a low-Christoffel carrier, not a positive prime main.

## 10. Source boundary, canonical registry, and next theorem

The only direct source-backed analytic step is the abstract MRT reduction in
(5.4).  MRT's applied propositions use standard \(\Lambda,d_k\) and
polylogarithmic major arcs.  Matomäki--Shao--Tao--Teräväinen,
arXiv:2204.03754v4, Theorem 1.1, uses
\(\Lambda-\Lambda^\sharp\), fixed-complexity nilsequences, and logarithmic
savings.  Neither source emits (4.5) or (5.5).  The finite primary-source
screen is fail-closed and does not claim that the entire literature has been
exhausted.

The historical registry key `V31_MRSTT_NILSEQUENCE_ATTACHMENT` is retained as
a repository label; it does not assert that Radziwiłł is an author of
arXiv:2204.03754v4.

~~~text
V31_MAXIMUM_CLAIM = EXACT_WHOLE_OBJECT_MODEL_LEVEL_MAJOR_ATTACHMENT_COMPILER_PLUS_CONDITIONAL_ENDPOINT_BUDGET_PLUS_EQUIVARIANT_QUOTIENT_NO_GO
V31_ROUTE_ADVANCE = YES
V31_ARITHMETIC_ADVANCE = NO
V31_FIXED_ATOM_CREDIT = 0
V31_STRICT_1_OVER_400 = UNPAID
V31_L2 = NONE
V31_TPC_207_TRIGGER = false
V31_NUMBERED_RELEASE = NO
V31_SELECTED_RESEARCH_ROUTE = B_MODEL_MAJOR_MISMATCH_AND_MINOR_CROSS_FLATNESS_THEN_A_TERMINAL_COVARIANCE_THEN_C_SYMMETRY_BREAK
V31_WHOLE_OBJECT_SPACE = SAME_LITERAL_TAGGED_P_EQUALS_B_TIMES_WBAR_AND_OCCURRENCE_NATIVE_MLOC
V31_FOURIER_COEFFICIENT_CONVENTION = PROVED_EXACT_PLUS_H_COEFFICIENT
V31_MODEL_SPECTRUM = L_X_EQUALS_SUM_H_MLOC_H_E_MINUS_H_ALPHA
V31_MODEL_ONLY_LEVEL_MAJOR = PROVED_EXACT_PREDECLARED_FROM_FROZEN_MODEL
V31_MAJOR_PREDECLARATION = REQUIRED_BEFORE_MISMATCH_OR_CELL_INSPECTION
V31_MT_DEFINITION = MT_M_H_EQUALS_HAT_OF_ONE_M_P_H
V31_ATTACHMENT_IDENTITY = PROVED_EXACT_MT_EQUALS_MLOC_PLUS_A
V31_ATTACHMENT_PARSEVAL_IDENTITY = PROVED_EXACT_MAJOR_MISMATCH_PLUS_MINOR_MODEL_ENERGY
V31_MAJOR_MISMATCH_ENERGY = SELECTED_PRIMARY_OPEN_NEW_THEOREM
V31_ACTUAL_ATTACHMENT_BOUND = OPEN_X_1_PLUS_NU_WITH_NU_BELOW_13_OVER_4800
V31_MINOR_COEFFICIENT_IDENTITY = PROVED_EXACT_E_EQUALS_N_PLUS_A
V31_MRT_PRODUCT_LOCAL_REDUCTION = SOURCE_BACKED_REDUCTION_ONLY_PROP_3_1_EQ_54
V31_CELL_PRODUCT_COMPILER = PROVED_EXACT_3Y_L1_LINF
V31_CELL_L1_GLOBAL_BOUND = PROVED_ELEMENTARY_X_1_PLUS_O1
V31_CELL_LINF_CROSS_FLATNESS = OPEN_ACTUAL_TAGGED_UNIFORM_THEOREM
V31_B_AGGREGATE_EXPONENT = PROVED_EXACT_SIGMA_B_EQUALS_MAX_NU_SIGMA_C
V31_B_ENDPOINT_CONDITION = SIGMA_B_STRICTLY_LESS_THAN_13_OVER_4800
V31_FORMULA_PREDECLARED_LARGE_SPECTRUM = SURVIVES_SCOPED_W_DEPENDENT_ZERO_CREDIT
V31_FORMULA_PREDECLARED_MINOR_FLATNESS = PROVED_EXACT_POINTWISE_THRESHOLD_COMPILER
V31_ZERO_AXIS_REASSEMBLY = PROVED_EXACT_S_EQUALS_N_ZERO_PLUS_A_ZERO
V31_OFFZERO_B_ALONE = STOP_SCOPED_AXIS_SURVIVES_ATTACHMENT_AND_MINOR_SPLIT
V31_QLOCAL_MODEL_BOUND = PROVED_ELEMENTARY_X_95_OVER_96_PLUS_O1
V31_A_TERMINAL_COVARIANCE = SELECTED_TERMINAL_OPEN_NEW_THEOREM
V31_A_B_TERMINAL_EQUIVALENCE = PROVED_EXACT_AFTER_B_STRICT_EXPONENT_CLASS
V31_WHOLE_OBJECT_CLOSURE_THEOREM = PROVED_EXACT_CONDITIONAL_ETA_STAR
V31_ENDPOINT_MARGIN_FORMULA = MIN_ETA_R_19_OVER_2400_13_OVER_4800_MINUS_SIGMA_B
V31_C_EQUIVARIANT_WHOLE_SHELL_QUOTIENT = STOP_SCOPED_TRANSLATION_INVARIANCE_FORCES_INJECTIVITY
V31_C_FULL_COORDINATE_CHRISTOFFEL = PROVED_EXACT_KAPPA_N_KAPPA0_N_MINUS_1
V31_Q5_GAP2_LOCAL_DENSITY_KERNEL = PROVED_EXACT_FINITE_LOW_CHRISTOFFEL_CARRIER
V31_Q5_TO_PHYSICAL_POSITIVE_MAIN = STOP_SCOPED_LOCAL_ADMISSIBILITY_DOES_NOT_FORCE_PRIME_MASS
V31_FIXED_HARD_SET_ALONE = STOP_SCOPED_MAJOR_MINOR_MASS_RELOCATION
V31_MRT_APPLIED_MAJOR_ATTACHMENT = STOP_SCOPED_STANDARD_LAMBDA_DK_OBJECTS_NOT_LITERAL_MASTER
V31_MRSTT_NILSEQUENCE_ATTACHMENT = STOP_SCOPED_WRONG_PROXY_PAIR_FIXED_COMPLEXITY_AND_LOGARITHMIC_SAVING
V31_DIRECT_PRIMARY_SOURCE_ATTACHMENT = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_08
V31_NEXT_THEOREM = MODEL_LEVEL_MAJOR_MISMATCH_ENERGY_AND_MINOR_CROSS_FLATNESS_AT_COMMON_SIGMA_BELOW_13_OVER_4800
V31_FIRST_FATAL = MODEL_LEVEL_MAJOR_MISMATCH_ENERGY_FOR_LITERAL_P_MINUS_L
V31_SOURCE_LOCK_POLICY = PRIMARY_SOURCES_ONLY_FAIL_CLOSED
V31_PROVENANCE_CASCADE = REQUIRED
~~~

The maximum supported claim is the exact model-level major compiler, its
Parseval payment interface, the conditional endpoint budget, and the retained
quotient no-go.  It is not a proof of (4.5), (5.5), (8.2), or the twin-prime
conclusion.  The next whole-object theorem must prove (4.5) and (5.5) on the
same literal occurrence object with \(\sigma_B<13/4800\); no atomwise or
micro-cell substitute is accepted.
