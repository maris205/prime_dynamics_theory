# Bridge A / Gate B V61: zero-hole additive edge-frame compiler

Date: 2026-08-17

## 0. Outcome, reframe, and claim firewall

V60 paid the moving-hole translation defect and left one exact arithmetic
object: the standard-zero-hole, prime-only, `q`-weighted,
kernel-localized, `(q-2)`-diagonal-subtracted signed four-packet BDH
remainder.  Its `ROUND2_CLUE` proposed separating equal and unequal additive
frequencies.  V61 proves that such a separation is not stable: a row supported
only at residue zero has zero zero-hole variance, while its frequency-diagonal
and frequency-off-diagonal pieces are individually of equal nonzero size and
cancel exactly.

The correct invariant object is instead the complete-graph Laplacian on the
`q-1` nonzero additive frequencies.  If

\[
 \Delta_{k,l}(n)=e_q(-kn)-e_q(-ln),
 \qquad k,l\in\mathbb F_q^\times,
 \tag{0.1}
\]

then the zero-hole variance is the exact tight-frame average

\[
 \boxed{
 V_0(a;v)=\frac1{q(q-1)}
 \sum_{\{k,l\}\subset\mathbb F_q^\times}
 \left|\sum_n a_n e(vn/H)\Delta_{k,l}(n)\right|^2.}
 \tag{0.2}
\]

Moreover,

\[
 \sum_{\{k,l\}}|\Delta_{k,l}(n)|^2
 =q(q-2)\mathbf1_{q\nmid n}.
 \tag{0.3}
\]

Thus the mandatory `(q-2)/(q-1)` diagonal can be distributed exactly over
the same edge cells.  Every resulting cell is pure coefficient-off-diagonal,
and the full V59 scalar becomes a signed average of these additive edge
pre-emitters.  The two-frequency decomposition is canonical: any scalar-weight
decomposition of the projection by literal vectors `e_k-e_l` must contain
every edge with the same forced weight.

This is an exact structural compiler and no-sparsification theorem.  It does
not estimate the edge cells, turn them into Kloosterman cells, prove a power
saving, close Gate B, produce fixed-atom credit, or prove a twin-prime result.

~~~text
V61_ROUTE_ADVANCE = YES
V61_STRUCTURAL_THRESHOLD_A = PASS
V61_ZERO_HOLE_ADDITIVE_EDGE_FRAME = PROVED_EXACT
V61_CELLWISE_Q_MINUS_2_DIAGONAL_CANCELLATION = PROVED_EXACT
V61_TWO_FREQUENCY_NO_SPARSIFICATION = PROVED_EXACT_IN_LITERAL_EDGE_CLASS
V61_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
V61_ARITHMETIC_ADVANCE = NO
V61_FIXED_ATOM_CREDIT = 0
V61_L2 = NONE
V61_TPC_208_TRIGGER = true
~~~

## 1. Frozen zero-hole object

Let `q` be prime.  For `q=2` every object below is zero; until the explicit
degenerate check we may assume `q>2`.  Let `a=(a_n)` have finite support and
put

\[
 x_n(v)=a_ne(vn/H),
 \qquad
 A_r(a;v)=\sum_{n\equiv r\,(q)}x_n(v).
 \tag{1.1}
\]

The standard zero-hole mean and variance are

\[
 \overline A^\times=\frac1{q-1}\sum_{r\ne0}A_r,
 \qquad
 V_0(a;v)=\sum_{r\ne0}|A_r-\overline A^\times|^2.
 \tag{1.2}
\]

The V59 reduced-residue diagonal and remainder are

\[
 D_0(a)=\frac{q-2}{q-1}
 \sum_{q\nmid n}|a_n|^2,
 \qquad
 R_0(a;v)=V_0(a;v)-D_0(a).
 \tag{1.3}
\]

The outer physical row is `q R_0`.  The prime shell, kernel integral, four
literal packets, and ordered block partition remain exactly those of V59.
V61 changes only the internal representation of `R_0`.

Use the additive DFT convention

\[
 \widehat A(k)=\sum_{r\bmod q}A_r e_q(-kr)
 =\sum_n x_n(v)e_q(-kn).
 \tag{1.4}
\]

No multiplicative character, inverse residue, or asymptotic estimate has
entered.

## 2. Zero-hole projection in additive frequency

Let `d=q-1`, enumerate `\mathbb F_q^\times`, and write

\[
 y=(\widehat A(k))_{k\ne0}\in\mathbb C^d,
 \qquad
 P_d=I_d-\frac1d\mathbf1\mathbf1^*.
 \tag{2.1}
\]

### Theorem 2.1 (zero-hole frequency projection)

For every row `A`,

\[
 \boxed{V_0(a;v)=\frac1q\,y^*P_dy.}
 \tag{2.2}
\]

In particular, the projection has rank `q-2`; its null direction is the
constant nonzero-frequency vector.

### Proof

Let `\mu=q^{-1}\sum_r A_r`.  V60 Theorem 1.1 with deleted residue zero gives

\[
 V_0=V_{\rm all}-\frac q{q-1}|A_0-\mu|^2.
 \tag{2.3}
\]

Parseval and Fourier inversion give

\[
 V_{\rm all}=\frac1q\sum_{k\ne0}|\widehat A(k)|^2,
 \qquad
 A_0-\mu=\frac1q\sum_{k\ne0}\widehat A(k).
 \tag{2.4}
\]

Substitution yields

\[
 V_0=\frac1q\sum_{k\ne0}|\widehat A(k)|^2
 -\frac1{q(q-1)}
 \left|\sum_{k\ne0}\widehat A(k)\right|^2,
 \tag{2.5}
\]

which is (2.2).  Since `P_d` is the orthogonal projection onto
`\mathbf1^\perp`, its rank is `d-1=q-2`.  `square`

## 3. Complete-graph tight frame

Let `K_d` be the complete graph on the nonzero frequency vertices.  For an
unordered edge `e={k,l}`, put

\[
 g_e=e_k-e_l.
 \tag{3.1}
\]

Its graph Laplacian satisfies

\[
 \sum_{e\in E(K_d)}g_eg_e^*
 =dI_d-\mathbf1\mathbf1^*=dP_d.
 \tag{3.2}
\]

Combining (2.2) and (3.2) proves the main frame identity.

### Theorem 3.1 (canonical additive edge frame)

For every finitely supported complex sequence `a`, every real `v`, and every
prime `q`,

\[
 \boxed{
 V_0(a;v)=\frac1{q(q-1)}
 \sum_{e=\{k,l\}\in E(K_{q-1})}
 |T_e[a](v)|^2,}
 \tag{3.3}
\]

where

\[
 T_{\{k,l\}}[a](v)
 :=\widehat A(k)-\widehat A(l)
 =\sum_n a_ne(vn/H)\Delta_{k,l}(n).
 \tag{3.4}
\]

For `q=2`, the edge set is empty and both sides vanish.

The normalized edge vectors form a Parseval frame on a space of dimension
`q-2`.  There are

\[
 |E(K_{q-1})|=\frac{(q-1)(q-2)}2
 \tag{3.5}
\]

edges, so the frame redundancy is `(q-1)/2`.  The redundancy is exact
bookkeeping, not a saving and not an admissible cellwise triangle loss.

## 4. Exact edgewise diagonal cancellation

The frequency difference automatically removes the excluded residue:

\[
 q\mid n\quad\Longrightarrow\quad\Delta_{k,l}(n)=0.
 \tag{4.1}
\]

### Lemma 4.1 (edge mass)

For every integer `n`,

\[
 \boxed{
 \sum_{e\in E(K_{q-1})}|\Delta_e(n)|^2
 =q(q-2)\mathbf1_{q\nmid n}.}
 \tag{4.2}
\]

### Proof

If `q|n`, every nonzero additive character has value one at `n`, so every
difference is zero.  If `q\nmid n`, put

\[
 u(n)=(e_q(-kn))_{k\ne0}.
 \tag{4.3}
\]

Then `||u(n)||_2^2=q-1` and `\sum_{k\ne0}e_q(-kn)=-1`.  The complete-graph
identity gives

\[
 \sum_e|\langle g_e,u(n)\rangle|^2
 =(q-1)||u(n)||_2^2-|\langle\mathbf1,u(n)\rangle|^2
 =(q-1)^2-1=q(q-2).
 \tag{4.4}
\]

This is (4.2).  `square`

Define the edge diagonal and edge remainder by

\[
 D_e[a]=\sum_n|a_n|^2|\Delta_e(n)|^2,
 \tag{4.5}
\]

\[
 \mathcal E_e^\circ[a](v)
 :=|T_e[a](v)|^2-D_e[a].
 \tag{4.6}
\]

The subtraction in (4.6) is not an approximation.  Expanding the square
gives the pure coefficient-off-diagonal identity

\[
 \boxed{
 \mathcal E_e^\circ[a](v)
 =\sum_{t\ne u}a_t\overline{a_u}
 e(v(t-u)/H)\Delta_e(t)\overline{\Delta_e(u)}.}
 \tag{4.7}
\]

Lemma 4.1 distributes the V59 diagonal exactly:

\[
 \frac1{q(q-1)}\sum_eD_e[a]
 =\frac{q-2}{q-1}\sum_{q\nmid n}|a_n|^2=D_0(a).
 \tag{4.8}
\]

### Corollary 4.2 (zero-hole off-diagonal edge compiler)

\[
 \boxed{
 R_0(a;v)=\frac1{q(q-1)}\sum_e\mathcal E_e^\circ[a](v),
 \qquad
 qR_0(a;v)=\frac1{q-1}\sum_e\mathcal E_e^\circ[a](v).}
 \tag{4.9}
\]

Thus the mandatory outer `q` is retained and every emitted edge cell is
already coefficient-off-diagonal.

## 5. Literal polarized Gate-B scalar

For two sequences `beta,w`, define the bilinear edge cell

\[
 \begin{aligned}
 \mathcal E_e^\circ(\beta,w;v)
 :={}&T_e[\beta](v)\overline{T_e[w](v)}\\
 &-\sum_n\beta(n)\overline{w(n)}|\Delta_e(n)|^2.
 \end{aligned}
 \tag{5.1}
\]

It is exactly

\[
 \mathcal E_e^\circ(\beta,w;v)
 =\sum_{t\ne u}\beta(t)\overline{w(u)}
 e(v(t-u)/H)\Delta_e(t)\overline{\Delta_e(u)}.
 \tag{5.2}
\]

For `a^(j)=beta+i^jw`, complex polarization gives, edge by edge,

\[
 \frac14\sum_{j=0}^3i^j
 \mathcal E_e^\circ[a^{(j)}](v)
 =\mathcal E_e^\circ(\beta,w;v).
 \tag{5.3}
\]

Consequently the frozen V59/V60 scalar has the exact normal form

\[
 \boxed{
 \mathfrak C_x=
 \int_{\mathbb R}\psi_+(v)
 \sum_{q\in\mathcal Q}\frac1{q-1}
 \sum_{e\in E(K_{q-1})}
 \mathcal E_e^\circ(\beta,w;v)\,dv.}
 \tag{5.4}
\]

The ordered V59 block decomposition also commutes with (5.4): replace
`beta,w` by `beta_b,w_c` and sum over `(b,c)` before any outer absolute
value.  Integrating in `v` first changes (5.2) into

\[
 \sum_{t\ne u}\beta_b(t)\overline{w_c(u)}K_H(u-t)
 \Delta_e(t)\overline{\Delta_e(u)}.
 \tag{5.5}
\]

Equation (5.5) is the V61 additive edge pre-emitter.  It is not yet a
Kloosterman cell.

### Physical-kernel verification

For residues `r,s mod q`, let

\[
 \mathcal K_q(r,s)=\sum_e
 (e_q(-kr)-e_q(-lr))
 (e_q(ks)-e_q(ls)).
 \tag{5.6}
\]

Complete-graph contraction gives

\[
 \boxed{
 \mathcal K_q(r,s)=
 \begin{cases}
 0,&rs\equiv0\pmod q,\\
 q(q-2),&r=s\ne0,\\
 -q,&r,s\ne0,\ r\ne s.
 \end{cases}}
 \tag{5.7}
\]

Therefore, for unit residues,

\[
 \frac1{q-1}\mathcal K_q(r,s)
 =q\left(\mathbf1_{r=s}-\frac1{q-1}\right),
 \tag{5.8}
\]

which is exactly the V59 `q u_1(s\bar r;q)` coefficient.  Formula (5.8)
verifies the literal outer weight, both signs, the zero-residue deletion,
and the same-residue coefficient.

## 6. Oriented difference-fiber normal form

Writing `l=k+d` and counting each unordered edge twice gives

\[
 \sum_{e\in E(K_{q-1})}\mathcal E_e^\circ
 =\frac12\sum_{d\in\mathbb F_q^\times}
 \sum_{\substack{k\in\mathbb F_q^\times\\k\ne-d}}
 \mathcal E_{k,k+d}^\circ.
 \tag{6.1}
\]

The edge factor becomes

\[
 \boxed{
 \Delta_{k,k+d}(n)=e_q(-kn)(1-e_q(-dn)).}
 \tag{6.2}
\]

Hence (5.4) may equivalently be written

\[
 \boxed{
 \mathfrak C_x=
 \int\psi_+(v)
 \sum_{q\in\mathcal Q}\frac1{2(q-1)}
 \sum_{d\ne0}\sum_{k\ne0,-d}
 \mathcal E_{k,k+d}^\circ(\beta,w;v)\,dv.}
 \tag{6.3}
\]

This is the preferred next-compiler interface.  It exposes a base additive
twist `k` and a unit-annihilating difference factor `1-e_q(-dn)` while
retaining the complete tight frame.  Applying a triangle inequality over
`d` or `k` before a source theorem would discard the exact frame geometry.

## 7. Unique two-frequency representation and no-sparsification

The complete graph is not a decorative choice.

### Theorem 7.1 (literal edge no-sparsification)

Suppose scalar weights `w_{k,l}` satisfy

\[
 P_d=\sum_{1\le k<l\le d}
 w_{k,l}(e_k-e_l)(e_k-e_l)^*.
 \tag{7.1}
\]

Then necessarily

\[
 \boxed{w_{k,l}=\frac1d=\frac1{q-1}
 \quad\text{for every edge }\{k,l\}.}
 \tag{7.2}
\]

In particular no strict subset of literal two-frequency differences can
represent the zero-hole projection with scalar edge weights.

### Proof

For `k\ne l`, the `(k,l)` matrix entry on the left of (7.1) is `-1/d`.
On the right, the only edge outer product with a nonzero `(k,l)` entry is
the edge `{k,l}`, and that entry is `-w_{k,l}`.  Hence
`w_{k,l}=1/d` for every pair.  The diagonal entries then agree
automatically.  `square`

This theorem is scoped to literal two-sparse edge vectors and scalar
weights.  It does not exclude dense orthonormal bases, signed higher-rank
decompositions, or a source theorem that estimates the whole frame jointly.

## 8. Sharp falsifiers

### 8.1 Equal/off-equal frequency split is not estimate-stable

Take `A_0=L` and `A_r=0` for every `r\ne0`.  Then `V_0=0`, while
`\widehat A(k)=L` for all `k\ne0`.  The two terms in (2.5) are

\[
 \frac1q\sum_{k\ne0}|\widehat A(k)|^2
 =\frac{q-1}{q}|L|^2,
 \tag{8.1}
\]

\[
 -\frac1{q(q-1)}
 \left|\sum_{k\ne0}\widehat A(k)\right|^2
 =-\frac{q-1}{q}|L|^2.
 \tag{8.2}
\]

Thus separate absolute estimates manufacture a large term from an exactly
zero row.  Every edge difference in (3.3) instead vanishes before an
estimate is taken.

### 8.2 One coefficient cancels inside every edge cell

If `a` has one nonzero coefficient at a unit residue, then
`|T_e[a]|^2=D_e[a]` for every edge individually.  Hence
`\mathcal E_e^\circ[a]=0` edge by edge, as required for a genuinely
coefficient-off-diagonal remainder.

### 8.3 Mandatory factors

Using ordered edges without the factor `1/2` doubles the scalar.  Including
frequency zero changes `K_{q-1}` to `K_q` and produces all-residue variance,
not the zero-hole row.  Replacing `q-1` by `q`, dropping the edge diagonal,
or summing a strict edge subset changes the physical kernel (5.7).

## 9. Source boundary and bounded novelty statement

Harper, arXiv:2412.19644v1, supplies a general-sequence BDH architecture
under explicit Progressions, Non-concentration, and additional hypotheses.
It does not state (5.4), verify those hypotheses uniformly for the literal
V59 packets, select prime moduli after a signed diagonal subtraction, or
perform the block/packet reassembly.

Blomer--Pascadi, arXiv:2607.24311v1, Theorem 1.1, accepts an already-emitted
fixed-modulus bilinear form

\[
 \sum_{m,n}\alpha_m\beta_n S(am,n;c)
 \tag{9.1}
\]

and gives the critical `c^{-1/32+o(1)}` saving.  The additive edge form
(5.5) is upstream of (9.1): V61 proves no Poisson/Voronoi transformation
from the literal `beta,w` coefficients to such arrays and no collective
prime-shell reassembly.  Pascadi, arXiv:2404.04239v3, likewise supplies
post-emitter sparse-Fourier/Kloosterman machinery, not (5.4).

A bounded arXiv metadata query for the exact combinations
`reduced residue + graph Laplacian`, `BDH + additive Fourier`, and
`leave-one-out variance + Fourier` returned no direct match on 2026-08-17.
This is not a proof of literature-wide novelty.  The complete-graph
Laplacian identity itself is standard linear algebra; the claim here is the
exact attachment, diagonal distribution, and no-sparsification statement
for the frozen V59 zero-hole object.

## 10. Route decision and canonical registry

The initial V61 candidate was

~~~text
zero-hole DFT
  -> estimate equal frequencies
  -> estimate unequal frequencies.
~~~

The zero-residue spike refutes that estimate order.  The corrected route is

~~~text
zero-hole DFT
  -> complete-graph Laplacian on nonzero frequencies
  -> edgewise coefficient-diagonal cancellation
  -> oriented (d,k) difference fibers
  -> future joint Poisson/Kloosterman compiler
  -> future prime-shell signed reassembly.
~~~

The strongest positive result is the exact canonical additive edge frame
with local diagonal deletion.  The strongest obstruction is Theorem 7.1:
literal two-frequency emission cannot be sparsified.  The open theorem is a
joint compiler that transforms the complete `(d,k)` frame into source-valid
Kloosterman cells and retains a fixed saving after all blocks, packets, and
prime moduli are reassembled.

~~~text
V61_MAXIMUM_CLAIM = EXACT_ZERO_HOLE_COMPLETE_GRAPH_ADDITIVE_EDGE_FRAME_WITH_CELLWISE_Q_MINUS_2_DIAGONAL_CANCELLATION_AND_UNIQUE_LITERAL_TWO_FREQUENCY_NO_SPARSIFICATION
V61_ROUTE_ADVANCE = YES
V61_STRUCTURAL_THRESHOLD_A = PASS
V61_ZERO_HOLE_FREQUENCY_PROJECTION = PROVED_V_0_EQUALS_ONE_OVER_Q_TIMES_Y_STAR_P_Y_WITH_RANK_Q_MINUS_2
V61_COMPLETE_GRAPH_FRAME = PROVED_V_0_EQUALS_ONE_OVER_Q_Q_MINUS_1_TIMES_SUM_UNORDERED_EDGE_TRANSFORM_SQUARED
V61_EDGE_COUNT = PROVED_Q_MINUS_1_TIMES_Q_MINUS_2_OVER_2
V61_FRAME_REDUNDANCY = PROVED_Q_MINUS_1_OVER_2
V61_ZERO_RESIDUE_ANNIHILATION = PROVED_DELTA_K_L_N_ZERO_WHEN_Q_DIVIDES_N
V61_EDGE_MASS = PROVED_SUM_EDGE_ABS_DELTA_SQUARED_EQUALS_Q_Q_MINUS_2_ON_UNITS_AND_ZERO_OFF_UNITS
V61_Q_MINUS_2_DIAGONAL_DISTRIBUTION = PROVED_EXACT_ONE_OVER_Q_Q_MINUS_1_EDGE_DIAGONAL_EQUALS_Q_MINUS_2_OVER_Q_MINUS_1_UNIT_DIAGONAL
V61_EDGEWISE_OFFDIAGONAL_CELL = PROVED_E_CELL_EQUALS_SUM_T_NOT_EQUAL_U_WITH_NO_COEFFICIENT_DIAGONAL
V61_OUTER_Q_NORMALIZATION = PROVED_Q_R_0_EQUALS_ONE_OVER_Q_MINUS_1_SUM_EDGE_E_CELL
V61_FOUR_PACKET_POLARIZATION = PROVED_EXACT_EDGE_BY_EDGE_BEFORE_ANY_ABSOLUTE_VALUE
V61_PHYSICAL_KERNEL = PROVED_ZERO_ON_NONUNITS_Q_Q_MINUS_2_ON_EQUAL_UNIT_RESIDUES_AND_MINUS_Q_ON_DISTINCT_UNIT_RESIDUES
V61_LITERAL_SCALAR_CROSSWALK = PROVED_EDGE_KERNEL_OVER_Q_MINUS_1_EQUALS_Q_TIMES_U_1
V61_ORIENTED_DIFFERENCE_FIBER = PROVED_DELTA_K_K_PLUS_D_EQUALS_E_MINUS_K_N_TIMES_ONE_MINUS_E_MINUS_D_N_WITH_FACTOR_ONE_HALF
V61_TWO_FREQUENCY_DECOMPOSITION_UNIQUENESS = PROVED_EVERY_EDGE_WEIGHT_FOR_P_EQUALS_ONE_OVER_Q_MINUS_1
V61_LITERAL_EDGE_SPARSIFICATION = REFUTED_NO_STRICT_EDGE_SUBSET_REPRESENTS_THE_PROJECTION
V61_EQUAL_OFF_EQUAL_SEPARATE_ESTIMATION = REFUTED_ZERO_RESIDUE_SPIKE_HAS_EQUAL_NONZERO_PIECES_AND_ZERO_SUM
V61_SINGLE_UNIT_CELL_DIAGONAL = PROVED_CANCELS_INSIDE_EVERY_EDGE
V61_HARPER_ATTACHMENT = OPEN_INPUT_HYPOTHESES_PRIME_SUBSET_SIGNED_DIAGONAL_AND_REASSEMBLY_UNPAID
V61_BLOMER_PASCADI_ATTACHMENT = OPEN_ADDITIVE_EDGE_PRE_EMITTER_NOT_YET_A_KLOOSTERMAN_CELL
V61_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
V61_ARITHMETIC_ADVANCE = NO
V61_GLOBAL_GATE_B_ADVANCE = NO
V61_FIXED_ATOM_CREDIT = 0
V61_L2 = NONE
V61_TPC_208_TRIGGER = true
V61_NUMBERED_RELEASE = TPC_208_STRUCTURAL_THRESHOLD_A
V61_FIRST_FATAL = NO_THEOREM_JOINTLY_COMPILES_THE_COMPLETE_ORIENTED_D_K_ADDITIVE_EDGE_FRAME_OF_THE_LITERAL_BLOCK_PACKETS_INTO_SOURCE_VALID_KLOOSTERMAN_CELLS_AND_REASSEMBLES_ALL_BLOCKS_FOUR_PACKET_SIGNS_AND_PRIME_MODULI_WITH_A_FIXED_SAVING
V61_ROUND2_CLUE = APPLY_MOBIUS_AND_POISSON_TRANSFORMS_TO_THE_WHOLE_D_K_TIGHT_FRAME_BEFORE_ANY_EDGE_OR_FIBER_TRIANGLE_AND_TEST_WHETHER_ONE_DUAL_VARIABLE_IS_SHARED_ACROSS_THE_FRAME
V61_REUSABLE_STRUCTURE = ZERO_HOLE_PROJECTOR_AS_COMPLETE_GRAPH_LAPLACIAN_PLUS_EDGEWISE_DIAGONAL_DELETION_AND_ORIENTED_UNIT_ANNIHILATING_DIFFERENCE_FIBERS
V61_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_ZERO_HOLE_PRE_EMITTER_BUILT_COLLECTIVE_KLOOSTERMAN_COMPILER_OPEN
~~~
