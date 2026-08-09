# Bridge A / Gate B V38: canonical packet--Kloosterman Schatten emitter

Date: 2026-08-09

Status: unnumbered big-road research artifact; exact scalar emitter proved,
canonical aggregate Schatten bound open; no arithmetic trigger.

## 1. Scope and invariant object

Put

\[
 I_x=(x/2,x]\cap\mathbb Z,\qquad
 H=x^{21/32},\qquad Q=x^{1/3},
 \tag{1.1}
\]

\[
 \mathcal Q=\{q\ {\rm prime}:Q<q\leq2Q\},\qquad
 K_H(h)=\widehat\psi_+(h/H),
 \tag{1.2}
\]

and retain the exact V36 physical arrays

\[
 \beta(t)=\beta_x^{\rm raw}(t),\qquad
 w(u)=\Lambda(u+2)-b_x^{(z)}(u).
 \tag{1.3}
\]

The V37 invariant scalar is

\[
 \mathfrak C_x=
 \sum_{q\in\mathcal Q}q
 \sum_{\substack{t,u\in I_x\\t\ne u,\ q\nmid tu}}
 \beta(t)w(u)K_H(u-t)u_1(u\bar t;q),
 \tag{1.4}
\]

where

\[
 u_1(a;q)=\mathbf1_{a\equiv1\ ({\rm mod}\ q)}-\frac1{q-1}.
 \tag{1.5}
\]

V35--V37 proved the exact reduction

\[
 \mathfrak D_x=\mathfrak C_x+\mathfrak P_x+\mathfrak N_x,
 \qquad
 |\mathfrak P_x|+|\mathfrak N_x|\ll x^{53/32+o(1)}.
 \tag{1.6}
\]

Thus the current off-zero gate would close if

\[
 |\mathfrak C_x|\ll x^{5/3-\delta+o(1)},
 \qquad \delta>\frac1{400}.
 \tag{1.7}
\]

V38 does not prove (1.7).  It proves that the existential emitter in V37
can be replaced by a canonical Fourier--Kloosterman block decomposition with
zero remainder.  The remaining hypothesis is a single explicit Schatten
aggregate for the literal physical packet.

## 2. Collapse the centered packets to one residue vector

For prime \(q\in\mathcal Q\), unit \(t\), and
\(b\in\mathbb F_q\setminus\{-t\}\), retain the V37 packet

\[
 F_{q,t}(b)=
 \sum_{\substack{u\in I_x\\u\ne t,\ u-t\equiv b\ ({\rm mod}\ q)}}
 w(u)K_H(u-t).
 \tag{2.1}
\]

Define its centered value

\[
 G_{q,t}=F_{q,t}(0)-\frac1{q-1}
 \sum_{b\ne-t}F_{q,t}(b),
 \tag{2.2}
\]

and the physical unit-residue vector

\[
 \boxed{
 d_q(r)=
 \sum_{\substack{t\in I_x\\t\equiv r\ ({\rm mod}\ q)}}
 \beta(t)G_{q,t},\qquad r\in\mathbb F_q^\times.}
 \tag{2.3}
\]

The V37 packet identity immediately becomes

\[
 \boxed{
 \mathfrak C_x=\sum_{q\in\mathcal Q}q
 \sum_{r\in\mathbb F_q^\times}d_q(r).}
 \tag{2.4}
\]

This is an exact regrouping of the final physical scalar, not an occurrence
majorant.  V35--V36 already proved

\[
 \beta(t)=\sum_{\substack{dk=t\\d,k\geq2}}
 \mu(d)\omega_x(d,k),
 \tag{2.5}
\]

and proved that the proper-factor occurrence sum may be re-collapsed to the
same \(\beta(t)\) in (1.4).  Consequently V38 is allowed to operate on
(2.4).  It does **not** claim that the redundant occurrence and dyadic labels
survive separately, and it does not use this relaxation for the
occurrence-native local Euler carrier of V28--V31.

## 3. Canonical Fourier--Kloosterman intertwiner

Use the Blomer--Pascadi convention

\[
 S(m,n;q)=\sum_{x\in\mathbb F_q^\times}
 e_q(mx+n\bar x),\qquad e_q(y)=e^{2\pi i y/q}.
 \tag{3.1}
\]

For \(m,n\in\mathbb F_q\), define

\[
 \boxed{
 M_q(m,n)=\frac1{q^2}
 \sum_{r\in\mathbb F_q^\times}
 d_q(r)e_q(-mr-n\bar r).}
 \tag{3.2}
\]

Opening (3.1), inserting (3.2), and using additive orthogonality twice gives

\[
\begin{aligned}
 \sum_{m,n\in\mathbb F_q}M_q(m,n)S(m,n;q)
 &=\frac1{q^2}\sum_{r,x\in\mathbb F_q^\times}d_q(r)
   \sum_m e_q(m(x-r))
   \sum_n e_q(n(\bar x-\bar r))\\
 &=\sum_{r\in\mathbb F_q^\times}d_q(r).
\end{aligned}
 \tag{3.3}
\]

Equation (3.3) is a canonical, exact Kloosterman emitter.  It has no
existence choice, smoothing loss, missing axis, or reassembly remainder.

### 3.1 The zero-axis self-return

The single inadmissible pair for prime \(q\) is \((m,n)=(0,0)\).  Here

\[
 M_q(0,0)=\frac1{q^2}\sum_r d_q(r),\qquad
 S(0,0;q)=q-1.
 \tag{3.4}
\]

Set

\[
 \lambda_q=1-\frac{q-1}{q^2}
 =\frac{q^2-q+1}{q^2}.
 \tag{3.5}
\]

Subtracting only the \((0,0)\) entry from (3.3) gives the exact nonzero-axis
identity

\[
 \boxed{
 \sum_r d_q(r)=\lambda_q^{-1}
 \sum_{\substack{m,n\in\mathbb F_q\\(m,n)\ne(0,0)}}
 M_q(m,n)S(m,n;q).}
 \tag{3.6}
\]

Let \(M_q^\circ\) denote \(M_q\) with precisely its \((0,0)\) entry set to
zero.  Since \(q\) is prime, every entry in the support of \(M_q^\circ\)
satisfies

\[
 (m,n,q)=1.
 \tag{3.7}
\]

Thus the zero-axis is not discarded: its exact self-return is moved to the
left through the harmless factor \(\lambda_q^{-1}=1+O(q^{-1})\).

## 4. Balanced blocks and exact SVD cells

Represent \(\mathbb F_q\) by \(\{0,1,\ldots,q-1\}\).  Put

\[
 B_q=\lfloor\sqrt q\rfloor
 \tag{4.1}
\]

and partition this representative interval into \(B_q\) consecutive,
balanced intervals \(\mathcal I_{q,i}\), whose lengths differ by at most
one.  Hence

\[
 B_q\asymp q^{1/2},\qquad
 |\mathcal I_{q,i}|\asymp q^{1/2}.
 \tag{4.2}
\]

For every ordered block pair \((i,j)\), take the singular-value
decomposition

\[
 M_q^\circ[\mathcal I_{q,i},\mathcal I_{q,j}]
 =\sum_{\ell=1}^{r_{q,i,j}}
 \sigma_{q,i,j,\ell}
 u_{q,i,j,\ell}\,v_{q,i,j,\ell}^{*}.
 \tag{4.3}
\]

Define coefficient arrays on the two intervals by

\[
 \alpha_{q,i,j,\ell}(m)=
 \frac q{\lambda_q}\sigma_{q,i,j,\ell}
 u_{q,i,j,\ell}(m),\qquad
 \gamma_{q,i,j,\ell}(n)=
 \overline{v_{q,i,j,\ell}(n)}.
 \tag{4.4}
\]

Combining (2.4), (3.6), and (4.3)--(4.4) gives

\[
 \boxed{
 \mathfrak C_x=
 \sum_{q\in\mathcal Q}\sum_{i,j,\ell}
 \sum_{\substack{m\in\mathcal I_{q,i},\ n\in\mathcal I_{q,j}\\
                  (m,n,q)=1}}
 \alpha_{q,i,j,\ell}(m)
 \gamma_{q,i,j,\ell}(n)S(m,n;q).}
 \tag{4.5}
\]

Every summand in (4.5) is a Blomer--Pascadi Theorem 1.1 cell with
\(a=1\), modulus \(q\), and interval lengths \(\asymp\sqrt q\).  Every
matrix coefficient belongs to one block, every block is reconstructed by
its SVD, and (4.5) has zero remainder.  This proves the V38 scalar
exactly-once emitter.

The source-native trivial scale of one cell is

\[
 q\|\alpha_{q,i,j,\ell}\|_2
  \|\gamma_{q,i,j,\ell}\|_2
 =\frac{q^2}{\lambda_q}\sigma_{q,i,j,\ell}.
 \tag{4.6}
\]

Therefore define the canonical physical atomic budget

\[
 \boxed{
 \mathfrak A_q(d_q)=
 \frac{q^2}{\lambda_q}
 \sum_{i,j}
 \bigl\|M_q^\circ[\mathcal I_{q,i},\mathcal I_{q,j}]\bigr\|_{S_1}.}
 \tag{4.7}
\]

There is no hidden template count in (4.7): it is exactly the aggregate
critical trivial scale of the canonical cells in (4.5).

## 5. The one remaining K-lane hypothesis

For \(\omega\geq0\), define

\[
 \boxed{\mathsf H_{\rm Sch}(\omega):\qquad
 \sum_{q\in\mathcal Q}\mathfrak A_q(d_q)
 \ll x^{5/3+o(1)}Q^\omega.}
 \tag{5.1}
\]

Unlike V37's existential emitter, (5.1) is a bound for a completely
specified physical norm.  It is still an open conjectural input and is not
inferred from the exact construction.

Blomer--Pascadi Theorem 1.1 states, for arbitrary coefficient arrays on
intervals of length at most \(N\leq q\),

\[
 \sum_{m,n\atop(m,n,q)=1}\alpha_m\gamma_nS(am,n;q)
 \ll \|\alpha\|_2\|\gamma\|_2q^{1+o(1)}
 \left(\frac{N^{1/8}}{q^{3/32}}
 +\frac{N^{5/16}}{q^{3/16}}
 +\frac{N^{2/3}}{q^{7/18}}\right).
 \tag{5.2}
\]

At \(N\asymp\sqrt q\), this gives \(q^{-1/32+o(1)}\) relative to (4.6).
Applying it only after (4.5) and assuming (5.1) yields

\[
 |\mathfrak C_x|
 \ll x^{5/3+o(1)}Q^{\omega-1/32}
 =x^{53/32+\omega/3+o(1)}.
 \tag{5.3}
\]

The strict endpoint margin is therefore

\[
 \left(\frac53-\frac1{400}\right)
 -\left(\frac{53}{32}+\frac\omega3\right)
 =\frac{19}{2400}-\frac\omega3.
 \tag{5.4}
\]

Hence

\[
 \boxed{0\leq\omega<\frac{19}{800}.}
 \tag{5.5}
\]

The concrete benchmark \(\omega=1/100\) would give output exponent
\(3983/2400\) and retain margin \(11/2400\).  It remains a conjectural
benchmark, not theorem credit.

## 6. Generic norm baselines and the L2 overpayment firewall

The canonical matrix itself has a useful exact singular-value formula.  Let

\[
 U_{m,r}=q^{-1/2}e_q(-mr),\qquad
 V_{n,r}=q^{-1/2}e_q(-n\bar r).
 \tag{6.1}
\]

The columns of \(U\) and \(V\) are orthonormal, and

\[
 M_q=q^{-1}U\,\operatorname{diag}(d_q(r))\,\overline{V}^{\,*}.
 \tag{6.2}
\]

Thus the nonzero singular values of \(M_q\) are \(|d_q(r)|/q\), and

\[
 \|M_q\|_F=q^{-1}\|d_q\|_2,
 \qquad \|M_q^\circ\|_F\leq q^{-1}\|d_q\|_2.
 \tag{6.3}
\]

For a balanced block, rank is \(O(q^{1/2})\), so

\[
 \|M_q^\circ[I,J]\|_{S_1}
 \ll q^{1/4}\|M_q^\circ[I,J]\|_F.
 \tag{6.4}
\]

There are \(O(q)\) block pairs.  Cauchy over blocks and (6.3) give the
unconditional generic baseline

\[
 \boxed{
 \sum_{i,j}\|M_q^\circ[I_i,I_j]\|_{S_1}
 \ll q^{-1/4}\|d_q\|_2,\qquad
 \mathfrak A_q(d_q)\ll q^{7/4}\|d_q\|_2.}
 \tag{6.5}
\]

Opening (3.2) one residue at a time also gives

\[
 \sum_{i,j}\|M_q[I_i,I_j]\|_{S_1}
 \ll q^{-1/2}\|d_q\|_1.
 \tag{6.6}
\]

The correction from \(M_q\) to \(M_q^\circ\) is supported at one entry and
has nuclear norm

\[
 |M_q(0,0)|\leq q^{-2}\|d_q\|_1.
 \tag{6.7}
\]

Thus (6.6) also holds with \(M_q^\circ\), and after multiplication by
\(q^2/\lambda_q\) it gives

\[
 \mathfrak A_q(d_q)\ll q^{3/2}\|d_q\|_1.
 \tag{6.8}
\]

Neither (6.5) nor (6.8) proves (5.1).  More importantly, a strong packet
\(L^2\) theorem is the wrong way to justify the BP route.  Put

\[
 \mathcal E_{\rm pack}=
 \sum_{q\in\mathcal Q}\sum_{r\in\mathbb F_q^\times}|d_q(r)|^2.
 \tag{6.9}
\]

From (6.5),

\[
 \sum_q\mathfrak A_q(d_q)
 \ll Q^{9/4+o(1)}\mathcal E_{\rm pack}^{1/2}.
 \tag{6.10}
\]

For (6.10) to imply (5.1), one would need

\[
 \mathcal E_{\rm pack}
 \ll x^{11/6+2\omega/3+o(1)}.
 \tag{6.11}
\]

At \(\omega=1/100\), the exponent in (6.11) is \(46/25\).  But the original
scalar (2.4) already satisfies direct Cauchy

\[
 |\mathfrak C_x|
 \ll Q^{2+o(1)}\mathcal E_{\rm pack}^{1/2}.
 \tag{6.12}
\]

The same hypothesis (6.11) would therefore give

\[
 |\mathfrak C_x|\ll x^{19/12+\omega/3+o(1)},
 \tag{6.13}
\]

which is stronger than the BP output (5.3) by exactly \(x^{7/96}\).
Equivalently, the generic block Frobenius loss \(Q^{1/4}\) overwhelms the
BP gain \(Q^{1/32}\).  Therefore

> proving (5.1) through the generic packet energy (6.11) is a scoped
> overpayment, not the selected K-lane theorem.

The selected next theorem is the direct physical block-Schatten aggregate
(5.1), where cross-block structure may be used before taking nuclear norms.

## 7. Primary-source boundary

The source screen was performed against primary theorem texts current on
2026-08-09.

1. [Blomer--Pascadi, arXiv:2607.24311v1, Theorem 1.1](https://arxiv.org/abs/2607.24311)
   accepts arbitrary coefficient arrays on two intervals and supplies the
   \(q^{-1/32}\) critical saving in (5.2).  It attaches exactly to each cell
   in (4.5), but it does not bound the outer canonical atomic norm (4.7).

2. [Harper, arXiv:2412.19644v1, Theorems 1--2](https://arxiv.org/abs/2412.19644)
   treats the progression variance of one fixed general sequence under
   progression, non-concentration, and hereditary-sparsity or
   integer-resemblance conditions, with \(Q>\sqrt{2x}\).  The V38 vector
   \(d_q\) is a \(q\)-dependent two-sequence centered packet at
   \(q=x^{1/3}\); those hypotheses and quantifiers are not a literal
   attachment.

3. [Lewko--Lewko, arXiv:1111.6190v2](https://arxiv.org/abs/1111.6190)
   proves variational BDH statements for prime-counting discrepancies.  It
   does not accept the \(\beta\times w\) packet or the block Schatten norm.

4. [Le Duc Hieu, arXiv:2509.04883v2, Appendix A](https://arxiv.org/abs/2509.04883)
   uses a short-interval BDH/multiplicative-large-sieve bound for the single
   \(\Lambda\) sequence.  It does not preserve the outer \(\beta(t)\), the
   centered background, or the inverse-frequency block matrix.

No checked source proves (5.1).  This is the first fatal for arithmetic
closure.  The source-backed status applies only to the post-emission BP
cells.

## 8. Finite and adversarial fixtures

The checker freezes the following independent diagnostics.

### 8.1 Double orthogonality and zero axis

Take \(q=5\), units \(1,2,3,4\), and

\[
 (d(1),d(2),d(3),d(4))=(3,-2,5,1).
 \tag{8.1}
\]

Then

\[
 \sum_r d(r)=7,\qquad M(0,0)=\frac7{25},\qquad
 \lambda_5=\frac{21}{25}.
 \tag{8.2}
\]

The zero-axis contribution is \(28/25\), the off-axis contribution is
\(147/25\), and multiplying the latter by \(25/21\) recovers \(7\).  The
checker also enumerates both additive orthogonality conditions and rejects a
wrong \(q^{-1}\) normalization, a missing inverse, or omission of
\(\lambda_q^{-1}\).

### 8.2 Frobenius and block ledger

For (8.1),

\[
 \|d\|_2^2=39,\qquad \|M\|_F^2=\frac{39}{25}.
 \tag{8.3}
\]

The balanced \(q=5\) partition has two blocks of sizes \(3,2\).  The checker
verifies that the blocks are disjoint and exhaustive, that only \((0,0)\) is
removed, and that the rank/Frobenius/nuclear exponents in (6.5)--(6.10) are
\(1/4,7/4,9/4\).

### 8.3 Endpoint and overpayment

The rational ledger freezes

\[
 \omega_{\rm sample}=\frac1{100},\quad
 \frac{11}{6}+\frac{2\omega}{3}=\frac{46}{25},\quad
 \frac{53}{32}+\frac\omega3=\frac{3983}{2400},
 \tag{8.4}
\]

\[
 \left(\frac53-\frac1{400}\right)-\frac{3983}{2400}
 =\frac{11}{2400},
 \tag{8.5}
\]

and the direct-energy output

\[
 \frac{19}{12}+\frac1{300}=\frac{119}{75},\qquad
 \left(\frac53-\frac1{400}\right)-\frac{119}{75}
 =\frac{31}{400}.
 \tag{8.6}
\]

Thus finite fixtures certify identities and exponent arithmetic only.  They
do not certify (5.1).

## 9. Research route after V38

V38 changes the K lane in one material way:

```text
V37: construct some exactly-once BP emitter + prove its aggregate norm
  -> V38: canonical Fourier/Kloosterman/block-SVD emitter is exact
  -> prove one named physical block-Schatten aggregate H_Sch(omega)
  -> apply source-backed BP q^(-1/32)
  -> terminal q-local A remains independent
  -> dynamics C remains reserve.
```

The recommended benchmark is \(\mathsf H_{\rm Sch}(1/100)\).  Harder
occurrence-native or local-carrier questions are not silently folded into
this scalar route.  If direct block-Schatten control stalls, the independent
E and X lanes remain available; a packet-energy theorem should be routed
directly through (6.12), not detoured through BP.

## 10. Canonical status registry

```text
V38_MAXIMUM_CLAIM = EXACT_CANONICAL_FOURIER_KLOOSTERMAN_BALANCED_BLOCK_SVD_EMITTER_PLUS_OPEN_PHYSICAL_SCHATTEN_AGGREGATE_AND_SOURCE_BACKED_BP_CELL_ENGINE
V38_ROUTE_ADVANCE = YES
V38_CONDITIONAL_BRIDGE_ADVANCE = YES
V38_ARITHMETIC_ADVANCE = NO
V38_FIXED_ATOM_CREDIT = 0
V38_STRICT_1_OVER_400 = UNPAID
V38_L2 = NONE
V38_TPC_207_TRIGGER = false
V38_NUMBERED_RELEASE = NO
V38_DERIVATION_STATUS = COHERENT_AFTER_EXACT_SCALAR_RECOLLAPSE_DOUBLE_ORTHOGONALITY_ZERO_AXIS_REMOVAL_AND_BLOCK_SVD
V38_ASSUMPTION_POLICY = ONLY_CANONICAL_PHYSICAL_SCHATTEN_AGGREGATE_IS_OPEN_AND_NEVER_PROMOTED
V38_SELECTED_RESEARCH_ROUTE = K_CANONICAL_SCHATTEN_AGGREGATE_FIRST__E_SECOND__X_THIRD__A_TERMINAL_AFTER_B__C_RESERVE
V38_V37_CENTERED_PACKET = RETAINED_EXACT_WITH_FULL_BACKGROUND_AND_DELETED_DIAGONAL
V38_PHYSICAL_RESIDUE_VECTOR = PROVED_EXACT_FINAL_SCALAR_REGROUPING
V38_CANONICAL_FOURIER_KLOOSTERMAN_MATRIX = PROVED_EXACT_DOUBLE_ADDITIVE_ORTHOGONALITY
V38_ZERO_AXIS_SELF_RETURN = PROVED_EXACT_LAMBDA_Q_FACTOR
V38_ZERO_AXIS_FACTOR = LAMBDA_Q_EQUALS_Q_SQUARED_MINUS_Q_PLUS_ONE_OVER_Q_SQUARED
V38_PRIME_COPRIMALITY_AFTER_ZERO_REMOVAL = PROVED_EXACT_ONLY_ZERO_ZERO_EXCLUDED
V38_BALANCED_FREQUENCY_PARTITION = PROVED_EXACT_CONSECUTIVE_BLOCKS_OF_LENGTH_ASYMPTOTIC_SQRT_Q
V38_BLOCK_SVD = PROVED_EXACT_RANK_ONE_BP_ARRAY_DECOMPOSITION
V38_CANONICAL_SCALAR_EMITTER = PROVED_EXACT_ZERO_REMAINDER
V38_EXACTLY_ONCE_POLICY = FINAL_PHYSICAL_SCALAR_AND_EVERY_MATRIX_ENTRY_EXACTLY_ONCE
V38_TEMPLATE_LABEL_RELAXATION = VALID_ONLY_AFTER_V35_V36_FINAL_SCALAR_RECOLLAPSE_NOT_FOR_LOCAL_CARRIER
V38_CELL_TRIVIAL_SCALE = Q_SQUARED_OVER_LAMBDA_Q_TIMES_SINGULAR_VALUE
V38_CANONICAL_ATOMIC_BUDGET = Q_SQUARED_OVER_LAMBDA_Q_TIMES_SUM_BLOCK_SCHATTEN_ONE
V38_CANONICAL_SCHATTEN_GATE = OPEN_CONJECTURE_AGGREGATE_X_POWER_5_OVER_3_TIMES_Q_POWER_OMEGA
V38_PACKET_OVERHEAD_THRESHOLD = OMEGA_STRICTLY_LESS_THAN_19_OVER_800
V38_BLOMER_PASCADI_CELL_ENGINE = SOURCE_BACKED_Q_POWER_MINUS_1_OVER_32_AFTER_EXACT_EMISSION
V38_CONDITIONAL_OUTPUT = X_POWER_53_OVER_32_PLUS_OMEGA_OVER_3
V38_CONDITIONAL_ENDPOINT_MARGIN = 19_OVER_2400_MINUS_OMEGA_OVER_3
V38_SAMPLE_OMEGA = 1_OVER_100
V38_SAMPLE_OUTPUT = 3983_OVER_2400
V38_SAMPLE_ENDPOINT_MARGIN = 11_OVER_2400
V38_FULL_MATRIX_SINGULAR_VALUES = PROVED_EXACT_ABS_D_R_OVER_Q
V38_FULL_MATRIX_FROBENIUS = PROVED_EXACT_Q_INVERSE_TIMES_D_L2
V38_GENERIC_BLOCK_SCHATTEN_BASELINE = Q_POWER_MINUS_1_OVER_4_TIMES_D_L2
V38_GENERIC_ATOMIC_L2_BASELINE = Q_POWER_7_OVER_4_TIMES_D_L2
V38_GENERIC_ATOMIC_L1_BASELINE = Q_POWER_3_OVER_2_TIMES_D_L1
V38_PACKET_ENERGY_TO_ATOMIC = PROVED_Q_POWER_9_OVER_4_TIMES_ENERGY_SQUARE_ROOT
V38_PACKET_ENERGY_REQUIRED_BY_GENERIC_ATOMIC_ROUTE = X_POWER_11_OVER_6_PLUS_2_OMEGA_OVER_3
V38_SAMPLE_PACKET_ENERGY_EXPONENT = 46_OVER_25
V38_DIRECT_PACKET_ENERGY_CAUCHY = PROVED_Q_SQUARED_TIMES_ENERGY_SQUARE_ROOT
V38_DIRECT_PACKET_ENERGY_OUTPUT = X_POWER_19_OVER_12_PLUS_OMEGA_OVER_3
V38_PACKET_ENERGY_VIA_BP = STOP_SCOPED_GENERIC_BLOCK_LOSS_Q_1_OVER_4_EXCEEDS_BP_GAIN_Q_1_OVER_32
V38_PACKET_ENERGY_BP_OVERPAY = X_POWER_7_OVER_96
V38_HARPER_GENERAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_ONE_Q_INDEPENDENT_SEQUENCE_Q_RANGE_AND_DISTRIBUTION_HYPOTHESES_MISMATCH
V38_LEWKO_VARIATIONAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_PRIME_COUNTING_ONE_SEQUENCE_WRONG_PACKET_AND_NORM
V38_HIEU_SHORT_INTERVAL_BDH_DIRECT_ATTACHMENT = STOP_SCOPED_SINGLE_LAMBDA_SEQUENCE_NO_BETA_CENTERED_INVERSE_BLOCK
V38_DIRECT_PRIMARY_SOURCE_FOR_CANONICAL_SCHATTEN_GATE = NONE_FOUND_FAIL_CLOSED_AS_OF_2026_08_09
V38_ROUTE_E = RETAINED_OPEN_WHOLE_RESIDUAL_SIGMA_LT_13_OVER_4800
V38_ROUTE_X = RETAINED_OPEN_JOINT_CHARACTER_KAPPA_GT_403_OVER_1200
V38_TERMINAL_A = OPEN_TERMINAL_EQUIVALENT_SIGNED_QLOCAL_COVARIANCE_AFTER_B
V38_DYNAMICS_C = RESERVE_DISTINGUISHED_SEED_ATTACHMENT_STILL_OPEN
V38_NEXT_THEOREM = DIRECT_LITERAL_CANONICAL_BLOCK_SCHATTEN_AGGREGATE_WITH_OMEGA_1_OVER_100_BENCHMARK
V38_FIRST_FATAL = NO_LITERAL_THEOREM_BOUNDS_THE_CANONICAL_PHYSICAL_BLOCK_SCHATTEN_AGGREGATE_WITH_OMEGA_LESS_THAN_19_OVER_800
V38_ROUTE_POSITION = ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B_K_LANE_CANONICAL_EMITTER_BUILT_ATOMIC_PIER_OPEN
V38_SOURCE_LOCK_POLICY = PRIMARY_THEOREM_TEXTS_ONLY_FAIL_CLOSED
V38_ROUTE_MAP_REFERENCE = TPC_ROUTE_MAP_MD_ANALYTIC_ELIMINATION_ISLAND_BRIDGE_A_GATE_B
```

## 11. Maximum-claim boundary

The maximum V38 claim is the exact canonical scalar emitter (4.5), the exact
zero-axis factor, the generic norm baselines, and the conditional implication
from (5.1) through the source-backed BP cell theorem.  V38 does not prove
(5.1), does not obtain an arithmetic saving or fixed-atom credit, does not pay
terminal A or dynamics C, and does not trigger a numbered release.
