# Bridge A / Gate B V39: Schatten duality barrier and packet-energy pivot

Date: 2026-08-09

Status: unnumbered big-road research artifact; exact duality and route
comparison proved, packet-energy theorem open; no arithmetic trigger.

## 1. Scope and inherited scalar

Retain the V38 parameters

\[
 H=x^{21/32},\qquad Q=x^{1/3},\qquad
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},
 \tag{1.1}
\]

the literal centered residue vector

\[
 d_q(r)=
 \sum_{\substack{t\in I_x\\t\equiv r\ ({\rm mod}\ q)}}
 \beta_x^{\rm raw}(t)G_{q,t},
 \qquad r\in\mathbb F_q^\times,
 \tag{1.2}
\]

and the exact scalar

\[
 \boxed{\mathfrak C_x=
 \sum_{q\in\mathcal Q}q\sum_{r\in\mathbb F_q^\times}d_q(r).}
 \tag{1.3}
\]

Here $G_{q,t}$ is the full V37 centered packet: it retains the physical
$w(u)=\Lambda(u+2)-b_x^{(z)}(u)$, the Schwartz shift kernel, the deleted
diagonal, and the complete compensating background.  V38 proved the exact
canonical Fourier--Kloosterman matrix

\[
 M_q(m,n)=\frac1{q^2}
 \sum_{r\in\mathbb F_q^\times}
 d_q(r)e_q(-mr-n\bar r),
 \tag{1.4}
\]

and, with

\[
 \lambda_q=\frac{q^2-q+1}{q^2},
 \tag{1.5}
\]

the exact zero-axis-corrected identity

\[
 \sum_r d_q(r)=\lambda_q^{-1}
 \sum_{(m,n)\ne(0,0)}M_q(m,n)S(m,n;q).
 \tag{1.6}
\]

Let $M_q^\circ$ be $M_q$ with only its $(0,0)$ entry set to zero, and
retain the V38 balanced consecutive partition $\mathcal P_q$ of
\(\{0,\ldots,q-1\}\) into blocks of length \(\asymp\sqrt q\).  The V38
atomic budget is

\[
 \mathfrak A_q(d_q)=\frac{q^2}{\lambda_q}
 \sum_{I,J\in\mathcal P_q}
 \|M_q^\circ[I,J]\|_{S_1}.
 \tag{1.7}
\]

The current numerator gate is

\[
 |\mathfrak C_x|\ll x^{5/3-\delta+o(1)},
 \qquad \delta>\frac1{400},
 \tag{1.8}
\]

whose strict endpoint is $x^{1997/1200+o(1)}$.  V39 asks a macro
question: is the nuclear atomization in (1.7) actually the best next bridge,
or does it discard cancellation already visible in (1.3)?

## 2. Exact block-projective duality

For each ordered block pair $I,J\in\mathcal P_q$, let $T_{I,J}$ be a
matrix of the same shape and impose

\[
 \|T_{I,J}\|_{\rm op}\leq1.
 \tag{2.1}
\]

Write $\mathcal T_q$ for the product of these independent blockwise
operator balls.  Nuclear/operator duality, followed by independence of the
block suprema, gives the exact identity

\[
 \sum_{I,J}\|M_q^\circ[I,J]\|_{S_1}
 =\sup_{T\in\mathcal T_q}
 \Re\sum_{m,n\ ({\rm mod}\ q)}
 \overline{T(m,n)}M_q^\circ(m,n).
 \tag{2.2}
\]

Define the block-contraction curve test

\[
 \Phi_{q,T}(r)=
 \sum_{\substack{m,n\ ({\rm mod}\ q)\\(m,n)\ne(0,0)}}
 \overline{T(m,n)}e_q(-mr-n\bar r).
 \tag{2.3}
\]

Inserting (1.4) into (2.2) yields

\[
 \boxed{
 \mathfrak A_q(d_q)=\lambda_q^{-1}
 \sup_{T\in\mathcal T_q}
 \Re\sum_{r\in\mathbb F_q^\times}d_q(r)\Phi_{q,T}(r).}
 \tag{2.4}
\]

The suprema for different $q$ are independent, so

\[
 \sum_{q\in\mathcal Q}\mathfrak A_q(d_q)
 =\sup_{(T_q)\in\prod_q\mathcal T_q}
 \Re\sum_{q\in\mathcal Q}\lambda_q^{-1}
 \sum_r d_q(r)\Phi_{q,T_q}(r).
 \tag{2.5}
\]

This also has a literal physical expansion:

\[
 \sum_r d_q(r)\Phi_{q,T}(r)
 =\sum_{\substack{t\in I_x\\q\nmid t}}
 \beta_x^{\rm raw}(t)G_{q,t}
 \Phi_{q,T}(t\bmod q).
 \tag{2.6}
\]

Thus the V38 Schatten conjecture is exactly a uniform theorem over a broad
family of $q$-dependent block-contraction curve tests.  It is not merely
the original scalar estimate in another notation.

## 3. The absolute-mass lower barrier

V38 proved that the nonzero singular values of the full $M_q$ are

\[
 \frac{|d_q(r)|}{q},\qquad r\in\mathbb F_q^\times.
 \tag{3.1}
\]

Consequently

\[
 \|M_q\|_{S_1}=q^{-1}\|d_q\|_1.
 \tag{3.2}
\]

Moreover

\[
 M_q-M_q^\circ=M_q(0,0)E_{00},\qquad
 |M_q(0,0)|=q^{-2}\left|\sum_r d_q(r)\right|.
 \tag{3.3}
\]

Since the sum of block nuclear norms dominates the nuclear norm of their
reassembled matrix, the reverse triangle inequality gives

\[
 \boxed{
 \mathfrak A_q(d_q)\geq\lambda_q^{-1}
 \left(q\|d_q\|_1-\left|\sum_r d_q(r)\right|\right).}
 \tag{3.4}
\]

This is the key structural toll.  If the scalar sum cancels strongly while
the packet retains large absolute mass, the canonical nuclear budget can
remain large.  Therefore no theorem of the form

\[
 \mathfrak A_q(d_q)\ll q\left|\sum_r d_q(r)\right|
 \tag{3.5}
\]

can hold on the ambient packet space.  A successful V38 Schatten theorem
must use special physical structure before the block nuclear norms erase
that scalar cancellation.

## 4. The certified generic Schatten continuum

Let $2\leq p\leq\infty$ and $p'=p/(p-1)$.  For a balanced Kloosterman
block

\[
 K_q[I,J]=
 \bigl(S(m,n;q)\mathbf1_{(m,n,q)=1}\bigr)_{m\in I,n\in J},
\]

Blomer--Pascadi Theorem 1.1 formally gives

\[
 \|K_q[I,J]\|_{S_\infty}\ll q^{31/32+o(1)}.
 \tag{4.1}
\]

The Weil bound and $O(q)$ entries give

\[
 \|K_q[I,J]\|_{S_2}\ll q^{1+o(1)}.
 \tag{4.2}
\]

Schatten interpolation therefore certifies

\[
 \|K_q[I,J]\|_{S_p}
 \ll q^{31/32+1/(16p)+o(1)}.
 \tag{4.3}
\]

On the coefficient side, rank/Frobenius followed by Cauchy over the
$O(q)$ blocks gives

\[
 \sum_{I,J}\|M_q^\circ[I,J]\|_{S_{p'}}
 \ll q^{-1/4-1/(2p)}\|d_q\|_2.
 \tag{4.4}
\]

Applying Schatten Hölder blockwise in (1.6), then Cauchy over the prime
shell, yields

\[
 \boxed{
 |\mathfrak C_x|
 \ll Q^{\alpha_{\rm cert}(p)+o(1)}
 \mathcal E_{\rm pack}^{1/2},\qquad
 \alpha_{\rm cert}(p)=\frac{71}{32}-\frac{7}{16p},}
 \tag{4.5}
\]

where

\[
 \mathcal E_{\rm pack}=
 \sum_{q\in\mathcal Q}\sum_{r\in\mathbb F_q^\times}|d_q(r)|^2.
 \tag{4.6}
\]

If $\mathcal E_{\rm pack}\ll x^{e+o(1)}$, the certified route reaches the
strict endpoint only when

\[
 e<\eta_{\rm cert}(p)
 :=\frac{2219}{1200}+\frac{7}{24p}.
 \tag{4.7}
\]

The three anchor values are

\[
\begin{array}{c|c|c}
 p&\alpha_{\rm cert}(p)&\eta_{\rm cert}(p)\\ \hline
 2&2&399/200\\
 4&135/64&4613/2400\\
 \infty&71/32&2219/1200.
\end{array}
 \tag{4.8}
\]

The admissible energy exponent decreases strictly as $p$ increases.
Among all generic consequences of the formally stated BP operator bound,
the endpoint $p=2$ is best.

## 5. The optimistic fourth-moment stress test

The proof architecture of Blomer--Pascadi uses a fourth moment of the
Kloosterman matrix in the prime square-root sketch and $k=\ell=2$ in the
general-modulus proof.  The published theorem, however, states a rank-one
bilinear/operator-norm estimate; it does not separately state a uniform
$S_4$ theorem for every ordered V38 block.

To make the route decision robust, grant the strongest favorable
counterfactual input

\[
 \|K_q[I,J]\|_{S_4}\ll q^{31/32+o(1)}
 \tag{5.1}
\]

for every V38 block.  This is an optimistic stress test, not source-backed
credit.  Interpolating $S_2$ with (5.1), and using monotonicity beyond
$p=4$, gives

\[
 \alpha_{\rm opt}(p)=
 \begin{cases}
 35/16-3/(8p),&2\leq p\leq4,\\
 71/32-1/(2p),&4\leq p\leq\infty,
 \end{cases}
 \tag{5.2}
\]

and the admissible energy exponent

\[
 \eta_{\rm opt}(p)=
 \begin{cases}
 187/100+1/(4p),&2\leq p\leq4,\\
 2219/1200+1/(3p),&4\leq p\leq\infty.
 \end{cases}
 \tag{5.3}
\]

In particular

\[
\begin{array}{c|c|c}
 p&\alpha_{\rm opt}(p)&\eta_{\rm opt}(p)\\ \hline
 2&2&399/200\\
 4&67/32&773/400\\
 \infty&71/32&2219/1200.
\end{array}
 \tag{5.4}
\]

Even after this favorable unproved grant, $p=2$ remains strictly best.
Thus no clarification of the proof-level fourth moment can reverse the
generic route ranking.

## 6. The direct packet-energy bridge

Returning to the literal scalar (1.3), Cauchy over all $(q,r)$ gives

\[
 \boxed{
 |\mathfrak C_x|
 \ll Q^{2+o(1)}\mathcal E_{\rm pack}^{1/2}.}
 \tag{6.1}
\]

For $\kappa>0$, define the one-line physical packet-energy hypothesis

\[
 \boxed{
 \mathsf H_{P2}(\kappa):\qquad
 \mathcal E_{\rm pack}
 \ll x^{2-\kappa+o(1)}.}
 \tag{6.2}
\]

Then (6.1) gives

\[
 |\mathfrak C_x|\ll x^{5/3-\kappa/2+o(1)}.
 \tag{6.3}
\]

Hence the exact threshold and margin are

\[
 \boxed{\kappa>\frac1{200},\qquad
 \text{margin}=\frac{\kappa}{2}-\frac1{400}.}
 \tag{6.4}
\]

The benchmark $\kappa=1/100$ gives output $x^{997/600+o(1)}$ and
retains margin $1/400$.

This does not prove $\mathsf H_{P2}$.  It proves a route-selection
theorem:

> among every generic Schatten route certified by the BP theorem statement,
> and even under the favorable fourth-moment grant (5.1), direct packet
> energy $p=2$ asks for the weakest power-saving energy estimate.

The V38 Schatten lane remains logically alive as a **specialized
non-generic compression theorem**: it could exploit physical cross-block
structure unavailable to (4.4).  It is no longer the primary generic lane.

## 7. Primary-source boundary

The source screen uses primary theorem texts current on 2026-08-09.

1. [Blomer--Pascadi, arXiv:2607.24311v1, Theorem 1.1 and Sections 1.4--1.5](https://arxiv.org/html/2607.24311v1)
   gives arbitrary **separable** coefficient arrays and the critical
   $q^{-1/32}$ operator saving.  Its proof uses a fourth-moment
   architecture, but the theorem does not state the V39 block-projective
   dual estimate, the packet energy (6.2), or a uniform matrix-weighted
   theorem for arbitrary block contractions.

2. [Kerr--Shparlinski--Wu--Xi, arXiv:2204.05038v5](https://arxiv.org/abs/2204.05038)
   proves several bilinear Kloosterman estimates, including one variable
   from an arbitrary set.  The inputs remain separable bilinear arrays and
   do not equal the $q$-dependent physical vector $d_q(r)$ or its prime
   shell energy.

3. [Kowalski--Michel--Sawin, arXiv:1511.01636v5](https://arxiv.org/abs/1511.01636)
   proves general bilinear forms in hyper-Kloosterman sums.  It supplies no
   theorem for the blockwise matrix coefficient class in (2.5) and no
   $\beta\times w$ centered-packet energy.

4. [Harper, arXiv:2412.19644v1, Theorems 1--2](https://arxiv.org/abs/2412.19644)
   treats the progression variance of one fixed general sequence subject
   to additional distribution hypotheses and a different modulus regime.
   Here $d_q$ itself depends on $q$, contains the centered physical
   $w$-packet, and is required at $q=x^{1/3}$.  There is no literal
   attachment.

No screened primary theorem proves $\mathsf H_{P2}(\kappa)$ for any
$\kappa>1/200$, or proves the non-generic V38 Schatten compression.
The first fatal on the selected route is therefore the missing literal
packet-energy theorem (6.2).

## 8. Finite and adversarial fixtures

### 8.1 A physical block-dual test

Take $q=5$, $d=(3,-2,5,1)$ on units $1,2,3,4$, and let $T$ be the
$5\times5$ identity matrix.  Every balanced block restriction of $T$
has operator norm at most one.  Formula (2.3) becomes

\[
 \Phi_{5,T}(r)=
 \sum_{m=0}^{4}e_5(-m(r+\bar r))-1
 =\begin{cases}4,&r=2,3,\\-1,&r=1,4.\end{cases}
 \tag{8.1}
\]

Therefore

\[
 \sum_r d(r)\Phi_{5,T}(r)=8.
 \tag{8.2}
\]

This freezes the inverse phase, the deleted $(0,0)$ term, and the
physical dual expansion.

### 8.2 Scalar cancellation does not pay the atomic budget

Take instead

\[
 d=(1,-1,1,-1).
 \tag{8.3}
\]

Then

\[
 \sum_r d(r)=0,\qquad \|d\|_1=4,\qquad
 \|M\|_{S_1}=\frac45,
 \tag{8.4}
\]

while (3.4) gives

\[
 \mathfrak A_5(d)\geq\frac{500}{21}.
 \tag{8.5}
\]

Thus the scalar is exactly zero while the canonical atomic lower bound is
strictly positive.

### 8.3 A synthetic projective-duality certificate

For the two blocks

\[
 A_1=\begin{pmatrix}3&0\\0&-2\end{pmatrix},\qquad
 A_2=\begin{pmatrix}0&4\\0&0\end{pmatrix},
 \tag{8.6}
\]

their nuclear norms sum to $5+4=9$.  The contractions

\[
 T_1=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
 T_2=\begin{pmatrix}0&1\\0&0\end{pmatrix}
 \tag{8.7}
\]

have operator norm one and attain dual value $9$.  This is a finite
certificate of the product-ball duality in (2.2), not a certificate of the
open arithmetic estimate.

## 9. Route map after V39

The macro route is now

```text
canonical V38 packet/Kloosterman emitter
  -> V39 exact block-projective duality exposes the Schatten test class
  -> V39 absolute-mass lower barrier exposes the nuclear toll
  -> primary B bridge: prove H_P2(kappa), kappa>1/200
  -> specialized reserve: prove genuinely non-generic H_Sch compression
  -> independent E and X bridges remain open
  -> terminal q-local A remains open after B
  -> distinguished-seed dynamics C remains reserve.
```

This is a route advance, not arithmetic credit.  The packet-energy theorem
must act on the literal $d_q$ from (1.2); replacing it by a divisor
majorant, a $q$-independent sequence, or an unsigned occurrence family
does not satisfy the gate.

## 10. Canonical status registry

```text
V39_MAXIMUM_CLAIM = EXACT_BLOCK_PROJECTIVE_DUALITY_ABSOLUTE_MASS_LOWER_BARRIER_AND_GENERIC_SCHATTEN_CONTINUUM_SELECT_DIRECT_PACKET_ENERGY_AS_PRIMARY_OPEN_BRIDGE
V39_ROUTE_ADVANCE = YES
V39_CONDITIONAL_BRIDGE_ADVANCE = YES
V39_ARITHMETIC_ADVANCE = NO
V39_FIXED_ATOM_CREDIT = 0
V39_STRICT_1_OVER_400 = UNPAID
V39_L2 = NONE
V39_TPC_207_TRIGGER = false
V39_NUMBERED_RELEASE = NO
V39_DERIVATION_STATUS = COHERENT_AFTER_BLOCK_NUCLEAR_DUALITY_MASS_BARRIER_CERTIFIED_AND_OPTIMISTIC_SCHATTEN_COMPARISON
V39_ASSUMPTION_POLICY = PACKET_ENERGY_AND_SPECIALIZED_SCHATTEN_COMPRESSION_REMAIN_EXPLICIT_OPEN_THEOREMS
V39_SELECTED_RESEARCH_ROUTE = P2_DIRECT_PACKET_ENERGY_FIRST__K_SPECIALIZED_SCHATTEN_SECOND__E_THIRD__X_FOURTH__A_TERMINAL_AFTER_B__C_RESERVE
V39_V38_CANONICAL_EMITTER = RETAINED_EXACT_ZERO_REMAINDER
V39_BLOCK_PROJECTIVE_DUALITY = PROVED_EXACT_PRODUCT_OF_BLOCK_OPERATOR_BALLS
V39_BLOCK_DUAL_CURVE_TEST = PROVED_EXACT_PHI_Q_T_ON_R_AND_R_INVERSE
V39_PHYSICAL_DUAL_EXPANSION = PROVED_EXACT_BETA_TIMES_CENTERED_G_TIMES_PHI
V39_ATOMIC_ABSOLUTE_MASS_LOWER_BARRIER = PROVED_LAMBDA_INVERSE_TIMES_Q_D_L1_MINUS_ABS_SUM_D
V39_SCALAR_ZERO_ATOMIC_ZERO_IMPLICATION = STOP_SCOPED_Q5_ALTERNATING_PACKET_COUNTEREXAMPLE
V39_CANONICAL_SCHATTEN_GATE = RETAINED_OPEN_SPECIALIZED_NON_GENERIC_COMPRESSION_LANE
V39_BLOMER_PASCADI_FORMAL_INTERFACE = SOURCE_BACKED_SEPARABLE_BILINEAR_OPERATOR_NORM_Q_MINUS_1_OVER_32
V39_BLOMER_PASCADI_FOURTH_MOMENT = PROOF_ARCHITECTURE_NOT_STANDALONE_ALL_BLOCK_S4_THEOREM
V39_OPTIMISTIC_S4_POLICY = COUNTERFACTUAL_GRANT_FOR_ROUTE_STRESS_TEST_NO_THEOREM_CREDIT
V39_CERTIFIED_SCHATTEN_ALPHA = 71_OVER_32_MINUS_7_OVER_16P
V39_CERTIFIED_SCHATTEN_ENERGY_CEILING = 2219_OVER_1200_PLUS_7_OVER_24P
V39_CERTIFIED_P2_ENERGY_CEILING = 399_OVER_200
V39_CERTIFIED_P4_ENERGY_CEILING = 4613_OVER_2400
V39_CERTIFIED_PINFINITY_ENERGY_CEILING = 2219_OVER_1200
V39_OPTIMISTIC_S4_P4_ENERGY_CEILING = 773_OVER_400
V39_GENERIC_SCHATTEN_OPTIMUM = PROVED_P_EQUALS_2_EVEN_AFTER_OPTIMISTIC_S4_GRANT
V39_PACKET_ENERGY = SUM_Q_SUM_R_ABS_D_Q_R_SQUARED
V39_DIRECT_PACKET_ENERGY_CAUCHY = PROVED_Q_SQUARED_TIMES_PACKET_ENERGY_SQUARE_ROOT
V39_PACKET_ENERGY_GATE = OPEN_CONJECTURE_X_POWER_2_MINUS_KAPPA
V39_PACKET_ENERGY_KAPPA_THRESHOLD = KAPPA_STRICTLY_GREATER_THAN_1_OVER_200
V39_PACKET_ENERGY_CONDITIONAL_OUTPUT = X_POWER_5_OVER_3_MINUS_KAPPA_OVER_2
V39_PACKET_ENERGY_ENDPOINT_MARGIN = KAPPA_OVER_2_MINUS_1_OVER_400
V39_SAMPLE_KAPPA = 1_OVER_100
V39_SAMPLE_OUTPUT = 997_OVER_600
V39_SAMPLE_ENDPOINT_MARGIN = 1_OVER_400
V39_KERR_SHPARLINSKI_WU_XI_DIRECT_ATTACHMENT = STOP_SCOPED_SEPARABLE_BILINEAR_ARRAYS_NO_LITERAL_Q_DEPENDENT_PACKET_ENERGY
V39_KOWALSKI_MICHEL_SAWIN_DIRECT_ATTACHMENT = STOP_SCOPED_SEPARABLE_HYPER_KLOOSTERMAN_BILINEAR_WRONG_MATRIX_AND_PACKET_NORM
V39_HARPER_GENERAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_Q_INDEPENDENT_SEQUENCE_MODULUS_RANGE_AND_DISTRIBUTION_HYPOTHESES_MISMATCH
V39_DIRECT_PRIMARY_SOURCE_FOR_PACKET_ENERGY_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V39_ROUTE_E = RETAINED_OPEN_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800
V39_ROUTE_X = RETAINED_OPEN_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200
V39_TERMINAL_A = OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B
V39_DYNAMICS_C = RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN
V39_NEXT_THEOREM = DIRECT_LITERAL_Q_DEPENDENT_CENTERED_PACKET_ENERGY_WITH_KAPPA_1_OVER_100_BENCHMARK
V39_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_SUM_Q_R_ABS_D_Q_R_SQUARED_BY_X_POWER_2_MINUS_KAPPA_FOR_KAPPA_GREATER_THAN_1_OVER_200
V39_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_CANONICAL_EMITTER_BUILT_PACKET_ENERGY_PIER_SELECTED_SCHATTEN_TOLL_EXPOSED
V39_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V39_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
```
