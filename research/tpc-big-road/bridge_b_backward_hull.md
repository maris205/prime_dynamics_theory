# Bridge B V18: typed backward-dual core and the forced-innovation highway

This is an unnumbered route artifact.  It is not TPC-207, a paper, a proof of
the twin-prime conjecture, or an arithmetic `L2` advance.  It continues V17 by
computing the part of the backward dual hull that is actually typed in the
repository and by failing closed on the still-untyped PBAPT Type-II part.

The current claim ceiling is

```text
EXACT_NORMALIZED_HAAR_ADJOINT_ALGEBRA
+ EXACT_CANONICAL_MEAN_INTERVAL_BACKWARD_HULL_GEOMETRY
+ EXACT_DELETION_INNOVATION_FORMULA
+ FIXED_HORIZON_WINDOWED_SUBPRIMORIAL_SUPPORT
+ COMPLETE_UNTYPED_HULL_NOT_TESTABLE
+ TYPED_WINDOWED_FORCED_INNOVATION_SELECTED_OPEN
+ NO_ARITHMETIC_ADVANCE.
```

The physical shift remains fixed at `h0=2`.  Fixed-atom credit is `0`, the
strict `1/400` is unpaid, `L2=NONE`, and `TPC_207_TRIGGER=false`.

## 1. The first correction: covectors are not Hilbert vectors

Write

```text
P=P_k,
p=p_(k+1),
alpha_p=(p-2)/p,
G_k=Z/P_k Z,
V_k=C^(G_k).
```

Every child residue is uniquely `x=r+jP`, and

```text
m_p(x)=1_(p does not divide x(x+2)),
(R_p f)(r+jP)=m_p(r+jP)f(r).                           (1.1)
```

There are two different pullbacks.

For a raw coefficient row `w` defining

```text
L_w(h)=sum_(x mod pP) w(x)h(x),
```

the algebraic covector pullback is

```text
(R_p^vee w)(r)
 =sum_(0<=j<p)m_p(r+jP)w(r+jP).                        (1.2)
```

For the normalized-Haar inner product

```text
<f,h>_k=P_k^(-1)sum_(r mod P_k)f(r)conjugate(h(r)),
```

the Hilbert adjoint is

```text
(R_p^*h)(r)
 =p^(-1)sum_(0<=j<p)m_p(r+jP)h(r+jP).                 (1.3)
```

Thus, when the same coordinate array is used on both sides,

```text
R_p^vee w=p R_p^*w.                                   (1.4)
```

More invariantly, the Riesz vector of `L_w` on `V_j` is
`P_j conjugate(w)`, and

```text
R_(j:k)^*(P_j conjugate(w))
 =P_k conjugate(R_(j:k)^vee w).                        (1.5)
```

The nonzero stage scalar in (1.4)--(1.5) does not change rank or support, but
it does change literal coefficients, dual norms, conditioning, and the
physical-loss ledger.  V17's informal `R^* ell` notation is therefore replaced
by `R^vee ell` whenever a functional is meant.

## 2. Exact backward adjoint geometry

Equations (1.1)--(1.3) give, for a coordinate atom `e_x`,

```text
R_p^*e_x
 = p^(-1)e_(x mod P), if m_p(x)=1,
 = 0,                 if m_p(x)=0.                    (2.1)
```

The forward and backward directions behave oppositely:

```text
R_p e_r = sum over its p-2 surviving child atoms,
R_p^*e_x = zero or one scaled parent atom.             (2.2)
```

For `j>=k`, put

```text
D_(j:k)=P_j/P_k,
M_(j:k)(x)=product_(k<t<=j)1_(p_t does not divide x(x+2)).
```

Then

```text
(R_(j:k)^*h)(r)
 =D_(j:k)^(-1)
  sum_(x mod P_j, x=r mod P_k)M_(j:k)(x)h(x),          (2.3)

R_(j:k)^*e_x
 =D_(j:k)^(-1)M_(j:k)(x)e_(x mod P_k).                (2.4)
```

In particular, a three-sparse interval increment cannot expand under
backward pullback.

The mean and deletion forcing also have exact formulas.  If

```text
g_(k,p)=R_p1-alpha_p1 in V_(k+1),
```

then

```text
R_p^*1=alpha_p1,
R_p^*g_(k,p)=alpha_p(1-alpha_p)1.                      (2.5)
```

Every later-stage forcing pulled to an earlier base is therefore only a
scalar mean.  The incoming `g_(k-1,p_k)` already living in `V_k` can add one
direction, but it is a primal vector, not a canonical physical covector.
Adding it directly to a dual registry without an explicit Riesz conversion
is a type error.

## 3. The canonical typed core

The repository currently canonically declares only

```text
D_k^core
 = {normalized Haar mean}
   union {ell_(k,X):X in X_k^int},                     (3.1)
```

where

```text
X_k^int
 = {(p_k^2-1)/2,...,(p_(k+1)^2-3)/2},

ell_(k,X)(f)
 = sum_(X<n<=2X)f(n mod P_k).                          (3.2)
```

For `j>=k`, let `w_(j,X)` be the raw interval row on `V_j` and define

```text
u_(k<-j,X)=R_(j:k)^vee w_(j,X).                        (3.3)
```

Its literal coefficient is

```text
u_(k<-j,X)(r)
 =sum_(X<n<=2X, n=r mod P_k)
   product_(k<t<=j)1_(p_t does not divide n(n+2)).     (3.4)
```

The canonical interval--mean diagnostic hull is

```text
H_(k,b)^IM
 =span_Q({1_k}
          union {u_(k<-j,X):
                 k<=j<=b, X in X_j^int}).             (3.5)
```

Using normalized `R^*` instead of raw `R^vee` gives the same rational span,
because each source-stage family differs only by the nonzero factor
`D_(j:k)`.

## 4. Backward increments stay sparse

At the source stage,

```text
w_(j,X)-w_(j,X-1)
 =-e_X+e_(2X-1)+e_(2X).                               (4.1)
```

Pulling (4.1) to `V_k` gives

```text
R_(j:k)^vee(w_(j,X)-w_(j,X-1))
 =-M_(j:k)(X)e_(X mod P_k)
  +M_(j:k)(2X-1)e_((2X-1) mod P_k)
  +M_(j:k)(2X)e_(2X mod P_k),                          (4.2)
```

with equal residues combined.  Its support is therefore `0,1,2`, or `3`,
never larger than three.

The exact support histograms for all source stages through `j=6` are:

| base `k` | increments | support 0 | support 1 | support 2 | support 3 |
|---:|---:|---:|---:|---:|---:|
| 2 | 135 | 33 | 62 | 31 | 9 |
| 3 | 128 | 10 | 33 | 55 | 30 |
| 4 | 117 | 2 | 14 | 36 | 65 |
| 5 | 82 | 0 | 5 | 19 | 58 |
| 6 | 59 | 0 | 0 | 0 | 59 |

This exactly rejects the feared direction error in which `R_p^*` is said to
replicate one atom into `p-2` atoms.  That is the forward map `R_p`, not its
adjoint.

## 5. Exact finite core-hull ranks

All ranks below are characteristic-zero ranks obtained from exact integer
rows and rational elimination.  `rows` includes one mean row.  The last
column is only a diagnostic that additionally inserts the incoming primal
forcing after Riesz identification; it is not part of (3.1).

| `k` | `b` | `P_k` | rows | `dim H_(k,b)^IM` | with incoming `g` |
|---:|---:|---:|---:|---:|---:|
| 2 | 2 | 6 | 9 | 5 | 5 |
| 2 | 3 | 6 | 21 | 6 | 6 |
| 2 | 4 | 6 | 57 | 6 | 6 |
| 2 | 5 | 6 | 81 | 6 | 6 |
| 2 | 6 | 6 | 141 | 6 | 6 |
| 3 | 3 | 30 | 13 | 13 | 14 |
| 3 | 4 | 30 | 49 | 30 | 30 |
| 3 | 5 | 30 | 73 | 30 | 30 |
| 3 | 6 | 30 | 133 | 30 | 30 |
| 4 | 4 | 210 | 37 | 37 | 38 |
| 4 | 5 | 210 | 61 | 61 | 62 |
| 4 | 6 | 210 | 121 | 119 | 120 |
| 5 | 5 | 2310 | 25 | 25 | 26 |
| 5 | 6 | 2310 | 85 | 85 | 86 |
| 6 | 6 | 30030 | 61 | 61 | 62 |

The tiny wrap controls `k=2,3` saturate quickly and are not asymptotic
evidence.  At the larger fixtures, the core rank remains on the scale of the
number of supplied rows rather than the ambient primorial dimension.

There are two literal deletion collisions at `k=4,j=6`:

```text
u_(4<-6,103)=u_(4<-6,104),
u_(4<-6,109)=u_(4<-6,110).                             (5.1)
```

For the first relation, the three increment atoms are deleted because

```text
13 divides 104,
11 divides 207+2=209,
13 divides 208.
```

For the second,

```text
11 divides 110,
13 divides 219+2=221,
11 divides 220.
```

Thus `121` supplied rows have rank `119` for an exact arithmetic reason, not
because of floating point, modular rank, or a normalization mismatch.

## 6. A uniform fixed-horizon support theorem

Fix a horizon `h=b-k`.  Consider any explicitly typed dual row at a source
stage `j<=k+h` whose coefficients are supported on physical integers
`n in (X,2X]` with `X in X_j^int`.  Algebraic pullback deletes terms and maps
`n` to `n mod P_k`; it never enlarges coordinate support.  Hence mean plus any
number of such windowed rows satisfies

```text
dimension
 <=1+p_(k+h+1)^2
 <=1+4^(h+1)p_k^2.                                    (6.1)
```

The second inequality is repeated Bertrand.  Also

```text
P_k>=product_(1<=j<=k)(j+1)=(k+1)!,
p_k<2^k,
```

so `P_k/p_k^2 -> infinity`.  For every fixed `h`, (6.1) is therefore

```text
O_h(p_k^2)=o(P_k).                                     (6.2)
```

For an arbitrary typed window family, (6.2) is only an upper bound; no
`BANDCOUNT_k+1` lower bound is asserted.  If `k>=4` and the typed family also
contains the V17 canonical mean/interval core, then combining its exact core
rank with (6.2) gives

```text
BANDCOUNT_k+1
 <= dimension
 <=1+4^(h+1)p_k^2
 =o(P_k).                                              (6.3)
```

Thus fixed rank is impossible for the required core-containing exact-return
family, while no fixed-horizon physical-window family can cause full
primorial explosion.  This theorem does not cover global characters, an
unbounded horizon, or an analytic Type-II object until that object is
literally materialized as a window-supported `V_j^vee` row.

## 7. The exact deletion innovation and its missing registry

For a fixed physical interval and `q=p_(k+1)`, define

```text
F_(k,X,q,a)(f)
 =sum_(X<n<=2X)f(n mod P_k)e_q(an),                    (7.1)
```

and

```text
E_(k,X,q)(f)
 =sum_(X<n<=2X)f(n mod P_k)
   [1_(q divides n(n+2))-2/q].                         (7.2)
```

Additive orthogonality gives the exact identity

```text
E_(k,X,q)
 =q^(-1)sum_(1<=a<q)(1+e_q(2a))F_(k,X,q,a).           (7.3)
```

The zero mode is excluded.  The same object has an adjacent-stage form:

```text
E_(k,X,q)
 =(1-2/q)ell_(k,X)-ell_(k+1,X) composed with R_q.      (7.4)
```

Equations (7.3)--(7.4) are source-backed exact formulas.  They do not decide
whether the physical family should contain only the aggregate `E` or each of
the `q-1` modes separately.  The repository has no active tuple registry for
`(k,X,q,A,h0)` and never canonically enumerates the individual modes into
`L_(k,X,A)`.  Consequently

```text
DELETION_INNOVATION_FORMULA = PROVED_EXACT,
DELETION_INNOVATION_ACTIVE_REGISTRY = ABSENT,
INDIVIDUAL_DELETION_MODES = CONDITIONAL_NOT_CANONICAL. (7.5)
```

The forcing `g_(k,q)` is a primal vector in the source recursion.  It must not
be substituted for the covector (7.2).

## 8. A conditional maximal windowed Fourier bank

It is useful to test the strongest natural completion without declaring it
canonical.  Include `a=0,...,q-1` in (7.1).  The discrete Fourier transform in
`a` identifies their span with the residue-sliced intervals

```text
V_(X,c)(f)
 =sum_(X<n<=2X, n=c mod q)f(n mod P_k).                (8.1)
```

Let `X_0=min X_k^int` and `B=BANDCOUNT_k`.  The `q` rows `V_(X_0,c)` form a
base bank.  For every later `X`,

```text
V_(X,c)-V_(X-1,c)
```

is obtained by distributing the three atoms

```text
-e_X+e_(2X-1)+e_(2X)                                  (8.2)
```

among their residue classes modulo `q`.  Across all `c`, at most three new
rows are nonzero.  Therefore the complete windowed bank has the exact upper
bound

```text
rank <=q+3(B-1).                                       (8.3)
```

For `k>=4`, including the mean adds at most one.  Since the bank contains
`a=0`, its rank is at least the V17 interval rank `B`.  Moreover (8.3) is
`O(q^2)=o(P_k)`.
Thus even the maximal same-stage windowed Fourier completion does not kill the
sparse highway.  It remains a conditional construction because the canonical
family choice in (7.5) is absent.

## 9. Global characters are a different and fatal family

In CRT coordinates `G_(k+1)=G_k x F_p`, (1.1) becomes

```text
R_pf(r,t)=f(r)1_(t not in {0,-2}).                     (9.1)
```

For a tensor character `chi_a(r)psi_b(t)`,

```text
R_p^*(chi_a psi_b)=m_p(b)chi_a,

m_p(0)=(p-2)/p,
m_p(b)=-(1+e_p(-2b))/p, b!=0.                          (9.2)
```

All multipliers in (9.2) are nonzero for odd `p`.  Hence complete global
characters pull back by a rank-one tensor multiplier, which is a positive
exact compression law.  But mean plus all nonzero global characters already
form the full Fourier basis of `V_k`, so

```text
ALL_GLOBAL_ADDITIVE_CHARACTERS
  = STOP_SCOPED_FULL_PRIMORIAL_RANK.                   (9.3)
```

The actual deletion modes in (7.1) are window-truncated.  Complete-frequency
Parseval, a full-cycle mean, or a TPC-32 auxiliary frequency cannot be used to
replace their physical window.

## 10. Why the complete hull is not yet defined

V16 says that the declared family should contain mean, actual intervals,
deletion-bias Fourier functionals, and the Type-II tests required by PBAPT.
Only the first two are currently canonical.  The repository does not freeze:

- aggregate versus individual deletion modes;
- active `(stage,X,A,frequency)` tuples;
- the coefficient class `A`;
- covector versus Haar-Riesz representation;
- a linear crosswalk from the selected analytic Type-II form to `V_j^vee`.

The Ford--Maynard universal arbitrary-coefficient family is not a candidate:
the mod-3 rank-one witness already stopped it.  The selected `SHB-D2` analytic
master is source-emitted as a bilinear formula, but its templates are not
materialized as primorial covectors.  The TPC-32 packet functional has another
clock, auxiliary modulus, masks, raw channels, and normalization; there is no
coefficientwise packet-to-primorial dual map.

Therefore

```text
COMPLETE_DECLARED_PHYSICAL_DUAL_FAMILY = NOT_TYPED,
PBAPT_TYPEII_TO_PRIMORIAL_CROSSWALK = ABSENT,
COMPLETE_HULL_RANK = NOT_TESTABLE_FAIL_CLOSED.          (10.1)
```

An empty PBAPT family, a template count, a Parseval norm, or a packet
frequency bank cannot be used to manufacture a rank.  This is the first fatal
of the complete-hull gate, not a failure of the canonical sparse core.

## 11. Zero defect versus the actual V16 error contract

Suppose first that the intertwiner is exact:

```text
J_jR_(j:k)=Q_(j:k)J_k,
ell_j=lambda_j composed with J_j.                      (11.1)
```

Then

```text
R_(j:k)^vee ell_j
 =J_k^vee Q_(j:k)^vee lambda_j,                        (11.2)
```

and a typed hull gives the necessary obstruction

```text
rank(J_k)>=dim H_(k,b)^vee.                            (11.3)
```

V16, however, allows a nonzero propagated defect:

```text
J_jR_(j:k)=Q_(j:k)J_k+Delta_(j:k).                    (11.4)
```

Now

```text
R_(j:k)^vee ell_j
 =J_k^vee Q_(j:k)^vee lambda_j
  +Delta_(j:k)^vee lambda_j.                           (11.5)
```

The V16 ledger controls the last term only after evaluation on actual source
trajectories.  It does not say that the defect functional vanishes on every
`f`, nor that it factors through `J_k`.  Hence

```text
ZERO_DEFECT_HULL_RANK = VALID_NECESSARY_OBSTRUCTION,
NONZERO_ERR_HULL_RANK = DIAGNOSTIC_ONLY.                (11.6)
```

For a minimal same-stage carrier, the missing lookahead directions must enter
through the physical defect/innovation.  That is not an implementation bug;
it is the analytic content that the future Type-II theorem must control.

## 12. The typed interface selected for the next gate

Every candidate dual row must now carry at least

```text
representation:
  COVECTOR_COORDINATE_SUM | HAAR_RIESZ_VECTOR

active_tuple:
  stage, next_prime, X, terminal_stage, A_id, h0

dual:
  dual_id, dual_kind, literal_formula_id,
  source_domain, frequency_domain,
  normalization, source_locator,
  attachment = ACTUAL_PRIMORIAL | DERIVED | CONDITIONAL_UNATTACHED.
```

The next unnumbered gate is to materialize the selected `SHB-D2` templates as
literal rows or prove that no coefficientwise map to `V_k^vee` exists.  It
must keep the analytic `x,m,n,rho`, primorial stage `k`, physical interval
`X`, and packet auxiliary modulus separate.  The first executable fixture is
`k=5,b=7`, with three disjoint families:

```text
physical innovation aggregate,
individually selected windowed modes,
source-emitted SHB-D2 Type-II rows.                    (12.1)
```

It must report incremental rank, support, transition sparsity, Riesz/physical
dual norms, conditioning, and the accumulated loss.  A continuous Mellin
parameter must be tested by its actual linear span rather than counted as one
template.

The selected route is therefore

```text
BRIDGE_B_TYPED_WINDOWED_FORCED_INNOVATION
  = SELECTED_OPEN_NEW_THEOREM.                         (12.2)
```

It is a growing sparse physical carrier with an explicit innovation port, not
a zero-defect fixed dictionary and not an a.e.-to-seed recurrence claim.

## 13. Canonical V18 status registry

The checker freezes 32 rows, sorted by key with final-LF canonical rows
`key<TAB>value<LF>`:

```text
BRIDGE_B_ADJOINT_ATOM_PULLBACK	PROVED_EXACT_SURVIVOR_COLLAPSE
BRIDGE_B_ALGEBRAIC_DUAL_PULLBACK	PROVED_EXACT
BRIDGE_B_ALL_GLOBAL_CHARACTERS	STOP_SCOPED_FULL_PRIMORIAL_RANK
BRIDGE_B_ARITHMETIC_ADVANCE	NO
BRIDGE_B_BACKWARD_INCREMENT_SUPPORT	PROVED_EXACT_AT_MOST_THREE
BRIDGE_B_BASE_INCOMING_FORCING	PRIMAL_VECTOR_NOT_CANONICAL_DUAL
BRIDGE_B_COMPLETE_DECLARED_DUAL_FAMILY	NOT_TYPED
BRIDGE_B_COMPLETE_HULL_RANK	NOT_TESTABLE_FAIL_CLOSED
BRIDGE_B_CORE_DUAL_FAMILY	CANONICAL_MEAN_PLUS_ACTUAL_INTERVALS
BRIDGE_B_CORE_HULL_ASYMPTOTIC	OPEN_NO_UNIFORM_HORIZON_THEOREM
BRIDGE_B_CORE_HULL_K4_B6	PROVED_EXACT_RANK_119_OF_210
BRIDGE_B_CORE_HULL_K5_B6	PROVED_EXACT_RANK_85_OF_2310
BRIDGE_B_CORE_HULL_K6_B6	PROVED_EXACT_RANK_61_OF_30030
BRIDGE_B_DELETION_INNOVATION_ACTIVE_REGISTRY	ABSENT
BRIDGE_B_DELETION_INNOVATION_AGGREGATE	PROVED_EXACT_FORMULA
BRIDGE_B_FIXED_HORIZON_WINDOWED_SUPPORT	PROVED_O_H_LOWERCASE_P_K_SQUARED_AND_O_PRIMORIAL
BRIDGE_B_HAAR_ADJOINT	PROVED_EXACT_P_INVERSE_AVERAGE
BRIDGE_B_INDIVIDUAL_DELETION_MODES	CONDITIONAL_NOT_CANONICAL_FAMILY
BRIDGE_B_LATER_DELETION_FORCING_PULLBACK	PROVED_EXACT_SCALAR_MEAN
BRIDGE_B_MAXIMAL_WINDOWED_FOURIER_BANK	CONDITIONAL_RANK_AT_MOST_Q_PLUS_3_BANDCOUNT_MINUS_3
BRIDGE_B_NONZERO_ERR_HULL_RANK	DIAGNOSTIC_ONLY_NOT_NECESSARY_OBSTRUCTION
BRIDGE_B_PBAPT_TYPEII_PRIMORIAL_CROSSWALK	ABSENT
BRIDGE_B_RIESZ_SCALING	PROVED_EXACT_SOURCE_OVER_TARGET_MODULUS
BRIDGE_B_SHB_D2_TYPEII_ROWS	OPEN_MATERIALIZATION_GATE
BRIDGE_B_TPC32_PACKET_TO_PRIMORIAL_DUAL	ABSENT
BRIDGE_B_TYPED_WINDOWED_FORCED_INNOVATION	SELECTED_OPEN_NEW_THEOREM
BRIDGE_B_UNTYPED_PLACEHOLDER_TO_COMPLETE_HULL	STOP_SCOPED_FAIL_CLOSED
BRIDGE_B_ZERO_DEFECT_HULL_RANK	VALID_NECESSARY_OBSTRUCTION
FIXED_ATOM_CREDIT	0
L2	NONE
STRICT_1_OVER_400	UNPAID
TPC_207_TRIGGER	false
```

The final-LF SHA-256 is

```text
57ddfe6635fe56020516680d9be5732ea39196d0bac5f6d4492a9c7d7890cd9b
```

Run the exact read-only checker with

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -B research/tpc-big-road/tpc_bridge_b_backward_hull_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_backward_hull_checker.py --check
```

It verifies the exact adjoint and Riesz scale, atom and forcing collapse,
15 core-hull ranks, five increment-support histograms, two literal zero
increments, six adjacent-stage deletion aggregates, exact cyclotomic deletion
identities, three conditional windowed-bank bounds, 24 fail-closed contract
mutations, and 34 registry-semantic mutations.  The contract requires an
exact key set and literal Boolean types; it freezes the PBAPT row registry to
the empty tuple, its source locator to `null`, `pbapt_attachment=false`, and
`complete_hull_rank=null`.  All 32 registry keys and values are independently
locked; every row rewrite, a key replacement, and a coordinated false release
are rejected even after the mutated registry hash is recomputed.

## 14. Route verdict

```text
CANONICAL_MEAN_INTERVAL_CORE = PROVED_EXACT
BACKWARD_ATOM_EXPLOSION = STOP_SCOPED_FALSE_DIRECTION
LATER_FORCING_NEW_DUAL_DIRECTIONS = STOP_SCOPED_FALSE_COLLAPSES_TO_MEAN
FIXED_HORIZON_WINDOWED_HULL = PROVED_SUBPRIMORIAL_GROWING
FULL_GLOBAL_CHARACTER_DICTIONARY = STOP_SCOPED_FULL_RANK
COMPLETE_UNTYPED_HULL = NOT_TESTABLE_FAIL_CLOSED
ZERO_DEFECT_TYPED_HULL_OBSTRUCTION = VALID
NONZERO_ERR_V16_ROUTE = DIAGNOSTIC_ONLY
TYPED_WINDOWED_FORCED_INNOVATION = SELECTED_OPEN_NEW_THEOREM
SHB_D2_PRIMORIAL_ROW_MATERIALIZATION = NEXT_GATE
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
```

The sparse road remains open for a precise reason: actual backward atoms stay
sparse and every fixed physical horizon is subprimorial.  The road is not yet
proved because its decisive Type-II rows, norms, conditioning, and loss ledger
do not exist on the primorial side.  The next move is to build that interface,
not to infer a complete hull from placeholders.
