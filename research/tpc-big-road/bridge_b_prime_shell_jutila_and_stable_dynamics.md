# Bridge B V23: prime-shell Jutila highway and stable nonautonomous blocks

Date: 2026-08-07

Status:

```text
UNNUMBERED_WORKING_ARTIFACT
EXACT_L0_ROUTE_SELECTION_WITH_ONE_NEW_CONDITIONAL_ANALYTIC_HIGHWAY
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
```

This artifact does not prove a new estimate for the twin-prime problem.  It
does four larger pieces of route work at once.

1. It freezes the literal `SHB-D2` diagonal before an auxiliary prime modulus
   is introduced.
2. It stops three tempting but incorrectly typed delta-symbol shortcuts.
3. It exhibits a nonempty exponent window for a prime-shell Jutila method
   intertwined with a second Kloosterman-sensitive refinement.
4. It gives an exact adjacent-stage and stable-block falsifier for the current
   Logistic common-return ansatz, while preserving a growing nonautonomous
   route.

The maximum claim is therefore

```text
EXACT_L0_PRIME_SHELL_JUTILA_EXPONENT_INTERFACE_AND_FINITE_TRANSPORT_FALSIFIERS
```

The words `OPEN_CONDITIONAL` below are route selection, not part of the proved
claim ceiling.

## 1. Frozen physical object

Keep the V19--V22 conventions

```text
h0=2,
x=2X,
I_x={t in Z:x/2<t<=x},
z=(log x)^K,
w_x^(z)(t)=Lambda(t+2)-b_x^(z)(t),
Q_mes=x^(1/3),
Q_src=2Q_mes,
Q_x={q prime:Q_mes<q<=2Q_mes},
R_x=#Q_x.
```

For exponent bookkeeping below, `Q` abbreviates `Q_mes`; the upper-cutoff
parameter in the Blomer--Li source lemma is always `Q_src=2Q_mes`.

The literal V19 coefficient is

```text
beta_x^raw(t)
 =1_(I_x)(t) sum_(o:T(o)=t, o routed MASTER) a_x(o),

a_x(o)=c_(j(o)) product_i mu(e_i(o)) log(f_1(o))/log(T(o)),
c_1=+2, c_2=-1.                                      (1.1)
```

No sign, occurrence multiplicity, shell endpoint, or normalization may be
changed.  The target is

```text
S_x=sum_(t in I_x) beta_x^raw(t) w_x^(z)(t).          (1.2)
```

V21 proved the complete equal-weight mean estimate

```text
S_x=Hbar_Q+Cbar_Q,
Hbar_Q<<_(A,K)x/log^A x.                              (1.3)
```

V22 proved that a transform applied only to the centered residue projector
rewrites the paid `Hbar_Q` branch and leaves the identity branch `S_x`.
Consequently every analytic construction below starts from (1.2), and only
after rebuilding (1.2) may it use (1.3).

The prime part of (1.2) also has the exact occurrence form

```text
sum_o a_x(o) sum_(d r-T(o)=2) mu(d)log r,             (1.4)
```

with the hybrid channel subtracted separately.  Formula (1.4), not a
congruence with the same symbols, is the source object.

## 2. Why an external prime `q` is not already a determinant modulus

Averaging the same scalar gives only the tautology

```text
S_x=R_x^(-1)sum_(q in Q_x)S_x.                       (2.1)
```

For a separated finite box and determinant mismatch `D=dr-t-2`, exact
equality and one congruence are related by

```text
D_=(q)=D_cong(q)-D_off(q),                            (2.2)

D_cong(q)=sum F(d,r,t)1_(D=0 mod q),
D_off(q)=sum_(ell!=0)sum F(d,r,t)1_(D=q ell).
```

Replacing `D=0` by `D=0 mod q` without the second line inserts every far
copy.  On the coprime part of the enlarged congruence one may perform

```text
r=(t+2) inverse(d) mod q                              (2.3)
```

and Poisson summation.  If

```text
A_q(c)=sum_(d=c mod q)mu(d)W_D(d),
Ahat_q(k)=sum_(c mod q)A_q(c)e_q(-kc),
```

then the exact finite transform is

```text
sum_(c mod q)^* A_q(c)e_q(v inverse(c))
 =q^(-1)sum_(k mod q)Ahat_q(k)S(k,v;q).              (2.4)
```

It contains one generally full-`q` coefficient, a still-coupled second
argument, all nonzero copies from (2.2), and separate zero/nonunit branches.
It is not yet two independent short Blomer--Pascadi arrays.

### 2.1 Three exact scoped stops

The following shortcuts are now closed.

First, the Heath--Brown/DFI delta symbol with parameter `C` contains

```text
h(c/C,D/C^2)!=0 only if c/C<=max(1,2|D|/C^2).
```

For `|D|<<x` and `C=x^(1/3)`, moduli as large as `x^(2/3)` remain.  The
natural uniform scale is `C=sqrt(x)`, not the desired prime shell.  Hence

```text
STANDARD_HB_DFI_C_EQ_X_1_3_SINGLE_MODULUS_COMPILER
 = STOP_SCOPED_WRONG_MODULUS_SUPPORT.                 (2.5)
```

Second, standard conductor lowering with `K=C=x^(1/3)` has rational phase
modulus `Kc=x^(2/3)`.  Keeping the condition modulo `K` instead creates two
modulus ensembles and retains a four-coordinate congruence.  Thus

```text
PHYSICAL_K_EQ_Q_CONDUCTOR_LOWERING_TO_SINGLE_BP_Q
 = STOP_SCOPED_SECOND_MODULUS_OR_RETAINED_CONGRUENCE. (2.6)
```

Third,

```text
q^(-1)sum_(a mod q)e_q(aD)=1_(q divides D),           (2.7)
```

not `1_(D=0)`.  Enforcing `|D|<q` needs about `x/q=q^2` determinant windows;
black-box Cauchy across them may cost `q`.  Three prime moduli can make their
product exceed `x`, but then the Kloosterman modulus is the product and the
physical `1/R_x` ensemble has been replaced by a triple label.  Therefore

```text
SINGLE_Q_FINITE_FOURIER_EXACT_DIAGONAL
 = STOP_SCOPED_DIVISIBILITY_ONLY.                     (2.8)
```

These stops do not apply to an overlapping-arc approximation with a separately
proved physical error theorem.

## 3. The prime-shell Jutila survivor

The source-backed input is Blomer--Li,
[*A higher rank shifted convolution problem with applications to
L-functions*](https://arxiv.org/abs/2511.03294v1), Section 2.1, Lemma 1.
Fix a smooth `psi:R->[0,1]` supported on `[-1,1]` with `integral psi=1`.
The lemma takes a nonnegative modulus weight supported on
`1<=q<=Q_src`, requires `0<delta<1/2`, and uses a nonzero normalizer `L`.
For these inputs it defines

```text
chi(alpha)=1/(delta L)
 sum_q omega(q) sum_(a mod q)^* sum_(k in Z)
 psi((alpha-a/q+k)/delta),

L=sum_q phi(q)omega(q),                               (3.1)
```

and proves

```text
integral_0^1 |1-chi(alpha)|^2 dalpha
 << Q_src^2 ||omega||_infinity |log delta|^3/(L^2 delta). (3.2)
```

Choose, before seeing any arithmetic outcome,

```text
Q=Q_mes, Q_src=2Q_mes,
omega(q)=1_(q prime,Q_mes<q<=2Q_mes),
L=sum_(q in Q_x)(q-1) asymp Q^2/log Q,
delta=Q^(-2+eta).                                    (3.3)
```

For every sufficiently large `x`, the prime shell is nonempty, `L>0`, and
the fixed positive `eta=1/32` gives `0<delta<1/2`.  These thresholds are part
of the source specialization; no empty ensemble is admitted.

Then

```text
||1-chi||_2<<Q^(-eta/2+o(1)).                        (3.4)
```

Define the literal finite Fourier polynomial

```text
A_x(alpha)=sum_(t in I_x)beta_x^raw(t)e(-t alpha),
W_x(alpha)=sum_(u in I_x)w_x^(z)(u)e(u alpha),
G_x(alpha)=A_x(alpha)W_x(alpha).                      (3.5)
```

Thus

```text
S_x=integral_0^1 G_x(alpha)dalpha.                    (3.6)
```

The Jutila main is honestly normalized as

```text
S_tilde_x=1/R_x sum_(q in Q_x) R_x/(delta L)
 sum_(a mod q)^* integral psi(beta/delta)
 G_x(a/q+beta)dbeta.                                 (3.7)
```

Equation (3.7) is not an exact delta identity.  It is useful only together
with a proof for the error `integral (1-chi)G_x`.

### 3.1 A nonempty exponent window

Suppose a source-native separation of the literal HB rows produces two macro
coordinates of length `Q^(3/2)`.  On an arc of width (3.3), the archimedean
shift enlarges each dual support only to

```text
q delta Q^(3/2)=Q^(1/2+eta).                         (3.8)
```

Blomer--Pascadi,
[*Bilinear forms with Kloosterman sums via quadratic
characters*](https://arxiv.org/abs/2607.24311v1), Theorems 1.1, 5.2 and
5.5, accepts arbitrary complex arrays on such intervals after an exact
compiler.  Substitution into all three source terms gives the `q`-saving

```text
s(eta)=min(1/32-5eta/16, 1/18-2eta/3).               (3.9)
```

Because `q=x^(1/3)`, the corresponding `x`-saving is `s(eta)/3`.  The Jutila
error would save `eta/6` in `x` if `||G_x||_2<=x^(1+o(1))`.  Hence the two
strict endpoint inequalities have the nonempty formal window

```text
3/200<eta<173/2400.                                  (3.10)
```

The canonical choice in this artifact is

```text
eta=1/32,
dual support exponent=17/32 in q,
BP q-saving=11/512,
BP x-saving=11/1536,
BP margin beyond 1/400=179/38400.                    (3.11)
```

The arc-width loss from the V22 ideal `1/96` is

```text
1/96-11/1536=5/1536,                                 (3.12)
```

which is smaller than the original `19/2400` margin.  Thus the exponent
geometry is real: local analytic strength is not the first obstruction.

### 3.2 Why black-box Jutila still fails

The committed divisor bounds alone give only

```text
||G_x||_2<<x^(3/2+o(1)).                              (3.13)
```

Cauchy with (3.4) then gives

```text
|S_x-S_tilde_x|<<x^(3/2-eta/6+o(1)),                 (3.14)
```

which cannot reach the `x^(1-1/400)` target for any legal short-support
`eta`.  For the canonical `eta=1/32`, a pure-energy proof would require

```text
||G_x||_2<<x^(1+theta), theta<13/4800.                (3.15)
```

No such literal physical theorem is currently source-backed, so `L2` remains
`NONE`.

Blomer--Li explicitly encounter the same methodological issue for divisor
exponential sums: Jutila's `L2` approximation alone is too weak on major arcs,
and their proof intertwines a second Kloosterman-sensitive circle method.
Their proved `GL(3)`--divisor theorem, factorable moduli, Voronoi transforms,
and character sums are not the physical HB2 `+2,-1`, Möbius/log and hybrid
coefficients.  The paper is a source-backed mechanism analogue, not a direct
attachment.

The surviving gate is therefore

```text
V23_PRIME_SHELL_JUTILA_KLOOSTERMAN_INTERTWINED_PHYSICAL_COMPILER_GATE
 = OPEN_CONDITIONAL.                                 (3.16)
```

It must prove both

```text
|integral_0^1(1-chi(alpha))G_x(alpha)dalpha|
 <<x^(1-1/400-epsilon_0),                             (3.17)
```

and a main-arc expansion into physical BP cells whose dual supports are at
most `q^(17/32+o(1))` and whose entire additional polynomial loss is strictly
less than `179/38400` in `x`.  Zero frequencies, nonunits, prime powers,
perfect powers, determinant diagonals, small/large cells, rough and
archimedean tails, endpoints, and the hybrid channel must have separate
registry rows.  The original one outer absolute value and exactly-once
occurrence cover must be retained.

## 4. Native cell audit and the moving-unit wall

The minimal HB2-B3 cell

```text
sum_(d r-c e_1e_2=2)
 mu(d)mu(e_1)mu(e_2)log r W - hybrid cell             (4.1)
```

has three rough coordinates and only one long smooth coordinate.  Cauchy in
`e_2` produces modulus `[d_1,d_2]`; its zero mode is the already-open
quadratic CRT/BDH covariance, not the linear hybrid main.  It does not natively
emit two independent critical BP arrays:

```text
MINIMAL_HB2_B3_TO_TWO_CRITICAL_BP_ARRAYS
 = STOP_SCOPED_NO_SECOND_SMOOTH_VARIABLE_AND_QUADRATIC_CRT_ZERO_MODE. (4.2)
```

There is nevertheless one exact local island in the factorized `J2` row.
On the slice `d=q`, put `A=e_1e_2`, assume `q` does not divide `A`, and take
smooth `f_i` weights of lengths `F_1,F_2` comparable with `sqrt(q)`.  Double
Poisson gives

```text
sum_(f_1,f_2)U(f_1/F_1)V(f_2/F_2)
 1_(A f_1f_2=-2 mod q)

 =F_1F_2/q^2 sum_(k,h in Z)
  Uhat(kF_1/q)Vhat(hF_2/q)S(k,-2h inverse(A);q).      (4.3)
```

This is a genuine BP kernel.  It is not a physical compiler.  At
`q=x^(1/3)` the scale is

```text
f_1,f_2,h,k ~ q^(1/2),
e_1,e_2 ~ q,
A=e_1e_2 ~ q^2,
r ~ q^2.                                             (4.4)
```

There are `q^2` physical `(e_1,e_2)` pairs but only `q-1` residue units.
Aggregation creates the structured coefficient

```text
P_q(A)=sum_(e_1e_2=A mod q)
 mu(e_1)mu(e_2)W_1(e_1)W_2(e_2).                    (4.5)
```

For one frozen physical pair, the Poisson prefactor, coefficient norms and
fixed-unit BP theorem give

```text
q^(-1) q^(1/2) q^(31/32+o(1))=q^(15/32+o(1)),       (4.6)
```

where the original congruence count per pair has scale one.  Triangling over
the physical pairs reproduces the V8 `F^(15/16)` deficit with `F=sqrt(q)`.
The exact character eigenmode from V8 applies to the kernel in (4.3), so a
cost-free arbitrary moving-unit vector extension is false.

The present cell is an unbalanced long-`e` sibling of V8, not the identical
input: here each `e_i` has length `q`, the physical pair family has size
`q^2`, and `r` has length `q^2`.  A valid theorem must exploit the literal
long Möbius coefficient (4.5) before outer triangle.  The statuses are

```text
V23_J2_UNBALANCED_LONG_E_DOUBLE_POISSON_ISLAND
 = PROVED_EXACT_LOCAL_CONGRUENCE_IDENTITY;

V23_FIX_A_APPLY_BP_THEN_OUTER_TRIANGLE
 = STOP_SCOPED_Q_15_OVER_32_DEFICIT;

V23_ARBITRARY_MOVING_UNIT_BP_VECTOR_LIFT
 = STOP_SCOPED_FALSE_CHARACTER_EIGENMODE;

V23_LONG_E_MOBIUS_MOVING_UNIT_COLLECTIVE_ASSEMBLER
 = OPEN_NEW_THEOREM_AFTER_PHYSICAL_REGISTRY.          (4.7)
```

This island does not cover `J1`, `d!=q`, the hybrid zero mode, Poisson axes,
or the nonzero copies in (2.2).

## 5. Exact adjacent-stage nonautonomous atlas

The mesoscopic ensemble has the integer description

```text
q in Q_x iff x<q^3<=8x.                              (5.1)
```

The first useful channel-birth fixture is:

| field | `x=166` | `x=168` |
|---|---:|---:|
| shell | `84..166` | `85..168` |
| shell size | 83 | 84 |
| ensemble | `{7}` | `{7,11}` |
| q=7 fiber counts | `(12,12,12,12,12,12,11)` | `(12,12,12,12,12,12,12)` |
| q=11 fiber counts | absent | `(8,8,8,8,7,7,7,7,8,8,8)` |

Let

```text
Pbar_x=R_x^(-1)sum_(q in Q_x)E_(x,q),
C_x=I-Pbar_x.                                        (5.2)
```

Exact rational linear algebra gives

```text
rank(Pbar_166)=7,       rank(C_166)=76,
rank(Pbar_168)=17,      rank(C_168)=83,
rank(Pbar_168^2-Pbar_168)=16.                        (5.3)
```

Thus an average of two conditional expectations is generally not a
projector, while its centered complement is full rank except for constants.
On the union `84..168`, natural zero extension gives

```text
rank(Pbar_168-Pbar_166)=19,
rank(C_168-C_166)=19.                                (5.4)
```

On the fixed new shell, adding `q=11` changes the centered operator by
`(E_7-E_11)/2`, of rank `16`.  Operator increments are relatively low rank;
the carried state is not bounded rank.

The literal raw rows satisfy

```text
beta_168^raw-beta_166^raw=-e_84+e_168                (5.5)
```

on the union, and agree coefficientwise on the overlap.  This does not make
the centered carrier sparse: the corresponding centered-covector update has
support `81/85`.

On the common overlap `K={85,...,166}`, the old and new `q=7` maps already
differ by rank one because one ragged fiber changes denominator from `11` to
`12`.  The restricted centered maps have ranks `76` and `82`; their stacked
rank is `82`.  Consequently any coefficientwise common linear quotient for
all overlap inputs has rank at least `82`:

```text
V23_LOCALLY_CONSTANT_WORD_ONLY_COMMON_PHYSICAL_CARRIER
 = STOP_SCOPED_EXACT_OVERLAP_RANK_82.                (5.6)
```

This does not stop a growing state, a time word of growing length, or a
nonlinear construction.  It stops a fixed low-dimensional dictionary from
being renamed as the common physical carrier.

### 5.1 Exact Fourier support warning

At `x=166,q=7`, periodization of the literal raw coefficient is

```text
(0,3,51/14,2,4,3,13/3),                              (5.7)
```

with sum `839/42`.  The entries are not all equal.  Since the minimal
polynomial of a nontrivial seventh root is `Phi_7`, all six nonzero Fourier
coefficients are nonzero; the zero coefficient is also nonzero.  The support
is exactly `7/7`.

The two-point change (5.5) vanishes after periodization modulo `7`, because
both endpoints are residue zero.  The newly born modulus `11` sees
`delta_3-delta_7`; its zero Fourier coefficient vanishes and all ten nonzero
coefficients are nonzero.  Sparse physical-coordinate aging therefore does
not imply short residue-frequency support.

## 6. Stable cells: a legal schedule, not cancellation

Fix `K` and `J=133/400`.  A conservative wall set consists of

```text
x=m^2,
d^400=x^133,
x=q^3/8 or x=q^3,
(log x)^K=p for a prime p.                            (6.1)
```

The number of such walls below `Y` is at most

```text
O(Y^(1/2)+Y^(133/400)+Y^(1/3)+(log Y)^K)=o(Y).       (6.2)
```

Hence safe even stages have density one.  One may predeclare a lacunary
sequence by taking the least safe even integer in `[8^n,2*8^n]`; for large
`n` it exists and the dyadic shells are disjoint.  This selection uses no
future prime event.

Inside one safe adjacent step, the raw coefficient, prime ensemble and set
of local primes below `z` agree on the overlap.  Only shell endpoints and
actual fiber normalization change.  Even that update is dense along residue
fibers.  For

```text
gamma_x=(I-Pbar_x)beta_x^raw,                         (6.3)
```

exact stable-pair fixtures give:

| pair | overlap raw changes | `support(delta gamma)` / union | squared norm |
|---|---:|---:|---:|
| `170->172` | 0 | `51/87` | `11647/61152` |
| `172->174` | 0 | `51/88` | `48695/78624` |
| `180->182` | 0 | `45/92` | `439/312` |
| `200->202` | 0 | `62/102` | `12157/54432` |

When `z` crosses a prime `p`, the local hybrid factor changes from

```text
G_p(0)=p/(p-1),
G_p(r)=p(p-2)/(p-1)^2 for r!=0
```

to

```text
F_p(-2)=0,
F_p(r)=p/(p-1) for r!=-2.                             (6.4)
```

It changes on every residue except zero: by `O(1)` on residue `-2` and by
`p/(p-1)^2` on the ordinary residues.  Any unbounded schedule crosses
infinitely many `J`, prime-window and `z` walls.  Choosing cell interiors
places the jumps between selected stages; it does not remove them.

Accordingly

```text
V23_PREDECLARED_INFINITE_LOCALLY_STABLE_EVEN_SUBSEQUENCE
 = PROVED_ELEMENTARY_DENSITY_ONE_SAFE_STAGES;

V23_STABLE_CELL_SHELL_UPDATE_HAS_BOUNDARY_SUPPORTED_COMPLEXITY
 = STOP_SCOPED_EXACT_DENSE_RESIDUE_FIBER_RENORMALIZATION;

V23_STABLE_CELL_SCHEDULING_AUTOMATICALLY_SAVES_COVARIANCE
 = STOP_SCOPED_EXACT_S_x_MINUS_PAID_Hbar_EQUIVALENCE. (6.5)
```

A subsequence theorem would be enough at the terminal logical level: a
positive twin count in pairwise disjoint shells for unbounded selected `x_n`
implies infinitely many distinct twin pairs.  It still needs every physical
cell, main term and reassembly gate on those shells.

## 7. Logistic transversality after the adjacent-stage falsifier

An exact finite orbit table can always be placed on a Logistic or odometer
orbit by adding a time/stage tag.  If the arithmetic table ignores the
Logistic coordinate, this is only `L0`: its mean, variation, variance and
cancellation have not changed.

There is also a precise quantifier obstruction.  If the same coefficientwise
physical evaluation is independent of a parameter on an open interval,

```text
G_(x,t)(lambda)=c_x(t),                               (7.1)
```

then

```text
partial_lambda G_(x,t)(lambda)=0.                    (7.2)
```

Nonzero derivatives of orbit coordinates may exist, but if the physical
functional cancels them they are auxiliary directions.  Therefore

```text
V23_PARAMETER_INDEPENDENT_EXACT_RETURN_WITH_TRANSVERSALITY_OF_THE_SAME_EVALUATION
 = STOP_SCOPED_EXACT_DERIVATIVE_ZERO.                 (7.3)
```

The repair is to use two different functions:

1. a structurally exact arithmetic return/intertwiner, allowed to have a
   growing state and explicit shell/`J`/`q`/`z` innovation ports;
2. an independent, predeclared critical-relation or bad-parameter function
   to which transversality applies.

The strongest surviving dynamical theorem is

```text
V23_LACUNARY_STABLE_BLOCK_AFFINE_COCYCLE_WITH_SUMMABLE_TRANSVERSAL_BAD_SETS
 = OPEN_NEW_THEOREM.                                  (7.4)
```

It requires one fixed parameter and critical/arithmetic seed, a
coefficientwise exact carrier on the predeclared safe sequence, a source-
independent small carrier mean, summable bad parameter sets, and a uniform
pointed estimate

```text
|Cbar_Q(x_n)|<<x_n^(1-delta_0)(log x_n)^M            (7.5)
```

for one fixed `delta_0>0`.  Lacunarity makes a genuinely power-decaying
exceptional-set bound summable, but no current sequential ASIP, Logistic
parameter-typicality theorem, or Hénon natural extension supplies the literal
carrier and the prescribed-seed triangular estimate together.

## 8. Route decision

The route order after V23 is:

1. **Prime-shell Jutila plus a second Kloosterman refinement.**  This is the
   primary construction.  Its exponent window is nonempty, and it introduces
   the correct prime shell without pretending a congruence is equality.  The
   first missing theorem is the physical major-arc error plus main-arc
   exactly-once compiler in (3.16)--(3.17).
2. **Long-`e` moving-unit collective assembler.**  This is a concrete local
   arithmetic subproblem after the physical registry emits (4.3).  Fixed-unit
   BP followed by outer triangle is stopped.
3. **Stable-block transversal dynamics.**  This remains a real conditional
   highway, now with an explicit density-one schedule and innovation ports.
   It still lacks a non-tautological common carrier and a pointed theorem.
4. **Hénon.**  It remains optional until an exact factor, section, event,
   measure and physical-functional diagram is constructed.

The first analytic fatal is no longer “there is no strong Kloosterman
theorem.”  It is

```text
NO_SOURCE_BACKED_LITERAL_HB2_HYBRID_MAJOR_ARC_ERROR_AND_MAIN_ARC_
EXACTLY_ONCE_COMPILER_FOR_THE_PRIME_SHELL_JUTILA_WEIGHT.          (8.1)
```

The first dynamical fatal is

```text
NO_NONTAUTOLOGICAL_GROWING_PHYSICAL_CARRIER_PLUS_ONE_FIXED_PARAMETER_
PRESCRIBED_SEED_UNIFORM_TRIANGULAR_THEOREM.                       (8.2)
```

Neither status is a theorem nonexistence claim beyond the declared source
corpus.

## 9. Conditional endpoint theorem and release boundary

If (3.16) is proved with the canonical exponent ledger and total additional
physical compiler loss `lambda_comp` satisfying
`0<=lambda_comp<179/38400`, then

```text
S_x<<x^(1-11/1536+lambda_comp+o(1))
     +x^(1-1/400-epsilon_0),                          (9.1)
```

before the downstream global physical ledger.  V21 then also controls
`Cbar_Q`.  Alternatively, if (7.4) gives any fixed power saving along the
predeclared disjoint-shell subsequence and all physical cells are reassembled
there, then the covariance gate is paid along a sequence sufficient for twin
infinitude.

Neither conditional conclusion automatically supplies:

```text
all-D uniformity,
exactly-once full physical cover,
original/global normalization,
tail-failure,
A/B selection,
actual packet attachment,
complete provenance,
positive prime-producing main dominance.
```

Therefore the current release boundary is

```text
V23_PRIME_SHELL_JUTILA_KLOOSTERMAN_INTERTWINED_PHYSICAL_COMPILER_GATE
 = OPEN_CONDITIONAL
V23_LONG_E_MOBIUS_MOVING_UNIT_COLLECTIVE_ASSEMBLER
 = OPEN_AFTER_PHYSICAL_REGISTRY
V23_LACUNARY_STABLE_BLOCK_AFFINE_COCYCLE_WITH_SUMMABLE_TRANSVERSAL_BAD_SETS
 = OPEN_NEW_THEOREM
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false.                              (9.2)
```

The source screen is finite and primary-source based.  Besides the two papers
linked above, the scoped delta and conductor-lowering audits use
Holowinsky--Munshi--Qi, arXiv:1409.3797v1, Section 2.2, and Munshi,
arXiv:1211.5731v2, Lemma 3 and Section 3.  Their coefficients and theorem
outputs are not promoted to the physical TPC object.

The companion checker verifies only exact rational exponent arithmetic,
finite raw/projector/transport fixtures, dependency hashes, and this claim
boundary.  It does not certify (3.16), (7.4), an arithmetic saving, or TPC.

## 10. Checker trust boundary

The read-only checker is

```text
research/tpc-big-road/tpc_bridge_b_prime_shell_jutila_checker.py
```

It locks the canonical-LF hashes of the V19, V21 and V22 checkers, a 33-field
contract and an exact 48-row registry.  The registry SHA-256 is

```text
15e40e8c20050549c3e244be59747019f115ebb8ccb9356f95fd449250073b07. (10.1)
```

The checker independently recomputes the rational exponent ledger, the
`x=166,168` beta/projector/DFT fixtures, four stable-pair updates and the
100--400 wall census.  Its 102 contract mutations and 151 registry mutations
must all be rejected.  These computations certify finite identities and the
claim firewall only.  The primary-source lemma, the missing physical
Kloosterman compiler, the growing dynamics theorem, an arithmetic saving and
TPC remain outside the executable claim.
