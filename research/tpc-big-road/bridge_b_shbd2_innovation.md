# Bridge B V19: exact HB2 raw rows and the mandatory source-innovation fork

This note continues the V18 typed backward-dual gate.  It answers two
questions that V18 deliberately left separate:

1. can the selected modified-Heath--Brown reduction produce an actual finite
   primorial covector without pretending that an unspecified Mellin template
   is already a row; and
2. can the literal shifted-prime residual be the same homogeneous
   replication--deletion source state used by V16?

The answers are respectively **yes for the combined raw MASTER row** and
**no for the literal residual as a homogeneous primal state**.  The resulting
architecture is an inhomogeneous source cocycle with a typed innovation term.
This is an exact L0 interface theorem, not the missing SHB-D2 estimate and not
an arithmetic advance.

## 1. Decision first

The V19 state is

```text
HB2_TWO_TYPE_RAW_EMITTER
  = PROVED_EXACT_SOURCE_LOCKED_PLUS_DERIVED_ROUTING,

HB2_RAW_MASTER_TO_PRIMORIAL_COVECTOR
  = PROVED_EXACT,

HB2_RAW_MASTER_K5_B7
  = 120 ROWS, 92 ACTIVE COORDINATES, EXACT RANK 56,

SHB_D2_SEPARATED_MELLIN_PERRON_TEMPLATE_REGISTRY
  = ABSENT,

LITERAL_SHB_D2_RESIDUAL_AS_HOMOGENEOUS_R_SOURCE
  = STOP_SCOPED_EXACT_FIBER_RANGE_VIOLATION,

SOURCE_LEVEL_INNOVATION
  = MANDATORY_IF_THE_RESIDUAL_IS_PRIMAL,

SOURCE_INNOVATION_TO_V16_INTERTWINER_ERR
  = ABSENT_TYPED_CROSSWALK.
```

Thus V18's placeholder-family fatal has been split correctly.  There is a
canonical, source-backed *physical reassembly row* that Bridge B can carry.
There is still no enumerated separated template family and no analytic
`x/log^A x` bound.  The next bridge must control the source innovation after
physical evaluation; it cannot hide that innovation inside V16's different
operator defect.

## 2. Exact source lock: the two HB2 raw types

The primary source is Ford--Maynard, *On the theory of prime-producing
sieves*, Lemma 5.2, printed page 19:

<https://www.ford126.web.illinois.edu/wwwpapers/prime-producing-sieves.pdf>

The checked PDF SHA-256 is

```text
49718b030ec4552dbf6b0cb8e3af541def02ca0def2447dad45bf41459a416f9.
```

Rename the source root index to `s`, to avoid collision with the determinant
variable `r`.  For every positive integer `h` and every integer `1<=t<=x`,
the source identity is

```text
(log t) 1_(t prime)
 =sum_(1<=j<=h)(-1)^(j-1) binom(h,j)
  sum_(1<=s<=log(x)/log(2)) mu(s)
  sum_(t=(e_1...e_j f_1...f_j)^s,
       e_i^s<=x^(1/h))
       log(f_1) product_i mu(e_i).                    (2.1)
```

All slots are labelled positive integers.  The source does not quotient by
permutations of the `e_i` or `f_i`; unit slots are allowed, `mu(1)=1`, and a
term with `f_1=1` vanishes through `log(f_1)=0` only after it has been emitted.

At `h=2,s=1`, the two and only two raw term types are

```text
HB2-J1:
  +2 sum_(t=e_1 f_1, e_1<=sqrt(x)) mu(e_1) log(f_1),

HB2-J2:
  -1 sum_(t=e_1e_2f_1f_2, e_1,e_2<=sqrt(x))
     mu(e_1)mu(e_2)log(f_1).                         (2.2)
```

In particular, the phrase “up to a fixed combinatorial constant” in the
earlier compiler is now replaced by the literal constants

```text
c_1=+2,  c_2=-1.                                      (2.3)
```

The root-one combination in (2.2) is the exact von Mangoldt identity

```text
2A_1(t)-A_2(t)=Lambda(t).                              (2.4)
```

The full prime-indicator identity (2.1) also has `s>=2` perfect-power terms.
Those terms remain the separately paid `x^(1/2+o(1))` branch; isolating
`s=1` must not be described as a prime-only identity.

On the dyadic shell, multiplying by `w_x^(z)(t)/log t` gives the exact factor

```text
c_j product_i mu(e_i) log(f_1)/log(t)
 =c_j product_i mu(e_i)
  rho_x(t) log(f_1)/log(x),

rho_x(t)=log(x)/log(t).                                (2.5)
```

This source-locks the atoms used by `C_HB2` without yet claiming that their
coupled finite-region selector has been separated.

## 3. A deterministic exactly-once routing convention

The earlier reduction said “choose the first component” and “choose the first
admissible subset” but did not freeze either order.  V19 makes the following
derived convention explicit:

```text
component order:
  (e_1,...,e_j,f_1,...,f_j);

unit policy:
  retain unit slots in the occurrence record,
  remove them only while choosing a group,
  retain their original bit positions;

large-component order:
  first slot in source order with u_i^2>=t;

no-large subset order:
  increasing nonzero proper original-slot bitmask.    (3.1)
```

For a large `f_i`, put `D=t/f_i`.  The occurrence is assigned to H2 exactly
when

```text
D<=x^J,  equivalently D^400<=x^133.                   (3.2)
```

Otherwise it is a MASTER occurrence and its group is `D`.  A large `e_i` is
always MASTER and its group is that `e_i`.  If there is no large component,
choose the first subset whose product `M` satisfies

```text
M^400>=t^133,  M^2<=t.                                (3.3)
```

The already proved emptiness of `R(P_TPC)` supplies such a subset.  Since
`x/2<t<=x`, (3.2)--(3.3) and the large-component alternatives all put the
MASTER group in the literal window

```text
(x/2)^J<M<=sqrt(x).                                   (3.4)
```

Every nonzero root-one occurrence therefore has exactly one of the labels

```text
H2 | MASTER.                                          (3.5)
```

Changing the deterministic order changes a separated presentation but not
the combined raw MASTER scalar, because an occurrence enters that scalar once
whenever its route is MASTER.  The convention is nevertheless recorded so a
future separated emitter has stable provenance.

## 4. The combined raw MASTER covector

For a fixed integer `x`, let `O_x^M(t)` be the finite set of labelled
root-one occurrences with product `t` and route MASTER.  Define the exact raw
coefficient

```text
beta_x^raw(t)
 =1_(x/2<t<=x)
  sum_(o in O_x^M(t))
    c_(j(o)) product_i mu(e_i(o)) log(f_1(o))/log(t).
                                                               (4.1)
```

Equivalently, its numerator is a finite formal prime-log vector:

```text
N_(x,t)=sum_(o in O_x^M(t))
          c_(j(o)) product_i mu(e_i(o)) log(f_1(o)),

beta_x^raw(t)=N_(x,t)/log(t).                          (4.2)
```

Unique factorization makes a nonzero integer prime-log vector nonzero as a
real number.  Thus support can be checked exactly without floating point.

For a primorial modulus `P_k`, the raw coordinate-sum covector is the exact
periodization

```text
v_(k,x)^raw(a)
 =sum_(x/2<t<=x, t=a mod P_k) beta_x^raw(t),

L_(k,x)^raw(F)
 =sum_(a mod P_k)v_(k,x)^raw(a)F(a).                  (4.3)
```

For `j>=k`, its algebraic pullback is the periodized covector

```text
u_(k<-j,x)^raw(a)
 =sum_(x/2<t<=x, t=a mod P_k)
   beta_x^raw(t)
   product_(k<s<=j)1_(p_s does not divide t(t+2)).     (4.4)
```

Equation (4.4) is an actual primorial covector.  In the no-wrap regime
`P_k>x`, each residue has at most one shell representative and (4.4) reduces
to the pointwise coefficient times the deletion masks.  It is not an
arbitrary `Xi,Kappa` placeholder.

The analytic and physical scales are bound explicitly by

```text
analytic x=2*physical X.                               (4.5)
```

This is a derived exact crosswalk: the analytic shell `(x/2,x]` becomes the
V17 physical shell `(X,2X]`.  The fields remain distinct in the registry.

## 5. Exact `k=5,b=7` raw-row fixture

At base stage `k=5`, `P_5=2310`.  The three source-stage bands are

| source stage | physical `X` | analytic `x=2X` | backward masks | row count |
|---:|---:|---:|---|---:|
| 5 | `60..83` | `120..166` | none | 24 |
| 6 | `84..143` | `168..286` | `13` | 60 |
| 7 | `144..179` | `288..358` | `13,17` | 36 |

All physical integers are below `P_5`, hence there is no wrap or coordinate
collision.  Exact occurrence enumeration gives

```text
MASTER occurrences before pullback = 259551,
H2 occurrences before pullback     = 153885.           (5.1)
```

After exact Möbius/log-vector aggregation and the masks in (4.4):

| family | rows | union support | exact row rank |
|---|---:|---:|---:|
| stage 5 | 24 | 43 | 17 |
| stage 6 | 60 | 51 | 29 |
| stage 7 | 36 | 41 | 12 |
| cumulative through stage 5 | 24 | 43 | 17 |
| cumulative through stage 6 | 84 | — | 44 |
| cumulative through stage 7 | 120 | 92 | 56 |

Thus the cumulative incremental ranks are

```text
(17,27,12).                                            (5.2)
```

The rank is exact, not a floating singular-value count.  For every active
coordinate `t`, all fixture numerators `N_(x,t)` lie on one primitive integer
prime-log direction `D_t`.  Write

```text
N_(x,t)=c_(x,t)D_t,  c_(x,t) in Z.                    (5.3)
```

Then

```text
beta_x^raw(t)
 =c_(x,t) [D_t/log(t)].                               (5.4)
```

The bracket is a nonzero column scalar, so the physical rank equals the
rational rank of the integer matrix `(c_(x,t))`.  Exact `Fraction`
elimination gives 56.

This fixture changes the V18 verdict in one precise sense: the physical raw
HB2 family is no longer empty or untyped.  It does **not** certify the
separated SHB-D2 family.

## 6. Covector/Riesz normalization and the conditioning boundary

With normalized Haar inner product

```text
<F,H>_k=P_k^(-1)sum_a F(a)conjugate(H(a)),             (6.1)
```

the raw row `v` represents the functional `sum_a v(a)F(a)`.  Its Riesz vector
and norm are

```text
H_v=P_k conjugate(v),
||L_v||=sqrt(P_k)||v||_(ell2).                         (6.2)
```

For the base-`P_5` fixture, a 70-digit Decimal evaluation of the exact
prime-log formulas gives the following rounded diagnostic extrema:

```text
min ||v||_2 approximately 4.134038918270820752,
max ||v||_2 approximately 6.416130930016243918,

min ||L_v|| approximately 1.986920775135905278e2,
max ||L_v|| approximately 3.083750320902564035e2.     (6.3)
```

These values reproduce the literal formulas; they are not used to certify
rank.  A physical singular-value/condition-number certificate would require
rigorous interval control of all retained logarithmic column scalars and a
declared basis/scaling.  V19 therefore records

```text
K5_B7_RAW_ROW_CONDITIONING = NOT_CERTIFIED.             (6.4)
```

No conditioning claim is inferred from the small norm spread in (6.3).

## 7. Why the separated SHB-D2 registry is still absent

The combined raw row (4.1) keeps the coupled finite-region indicator intact.
The analytic master instead writes that indicator as separated
`Xi(m)Kappa(n)` pieces using Perron/Mellin transforms or an equivalent
bounded-polytope partition.  A literal separated registry must still contain

```text
template_id,
raw occurrence/source IDs,
selected subset and grouping,
all earlier failed-subset selectors,
Xi and Kappa formulas,
transform variables, domain, kernel and measure,
free-mode versus integrated-reconstruction semantics,
truncation height, total L1 norm and tail,
closed sqrt(x) endpoint,
uniform A,K constants and source locator.              (7.1)
```

None of these transform records is committed.  Consequently

```text
RAW_MASTER_ROW_GENERATION = PROVED_EXACT_FINITE,

SEPARATED_SHB_D2_TEMPLATE_REGISTRY = ABSENT,

SHB_D2 <<_(A,K) x/log^A(x) = OPEN_NEW_THEOREM.         (7.2)
```

The raw family is the canonical physical reassembly target.  A future
analytic proof may use many separated rows internally, but their template
count, a continuous Mellin parameter count, or a Parseval norm cannot be
substituted for the physical rank 56.

## 8. Exact range theorem for the primal replication map

Fix a parent modulus `P` and a new odd prime `p` with `gcd(P,p)=1`, and

```text
m_p(r+jP)=1_(p does not divide (r+jP)(r+jP+2)),

(R_pF)(r+jP)=m_p(r+jP)F(r).                           (8.1)
```

Every parent fiber has exactly two deleted copies and `p-2` surviving copies.
For `V in C^(Z/pPZ)`,

```text
V in ran(R_p)                                          (8.2)
```

if and only if, on every parent fiber,

1. `V` vanishes on the two deleted copies; and
2. `V` is constant on all surviving copies.

Necessity is immediate from (8.1).  For sufficiency, define the parent value
to be the common survivor value.  It is unique.

If `alpha_p=(p-2)/p`, V16 proved `R_p^*R_p=alpha_p I`.  Hence the exact
pseudoinverse and orthogonal projection are

```text
R_p^dagger=alpha_p^(-1)R_p^*,

Pi_p=alpha_p^(-1)R_pR_p^*.                            (8.3)
```

Every child state has the canonical orthogonal decomposition

```text
V=R_pF+eta_p(V),

F=alpha_p^(-1)R_p^*V,

eta_p(V)=(I-Pi_p)V perpendicular to ran(R_p).          (8.4)
```

The source innovation vanishes exactly when the two fiber conditions hold.

## 9. Literal residual counterexamples

Put

```text
w_x^(z)(t)=Lambda(t+2)-b_x^(z)(t).                    (9.1)
```

The smallest no-wrap same-shell survivor-constancy witness uses

```text
P_2=6,  p_3=5,  P_3=30,
x=26,  X=13.                                          (9.2)
```

The stage clock is exact because `5^2<=x+2<7^2`.  In the shell `(13,26]`, the
integers 14 and 26 are distinct surviving children of the same parent
`2 mod 6` under `R_5`.  For every `z>=2`, the prime-2 local factor makes

```text
b_26^(z)(14)=b_26^(z)(26)=0.                          (9.3)
```

But

```text
w_26^(z)(14)=Lambda(16)=log(2),
w_26^(z)(26)=Lambda(28)=0.                            (9.4)
```

This violates survivor-fiber constancy, so the literal residual is not in
`ran(R_5)`.  At child stage 2 there is only one survivor per fiber; at the
preceding stage-3 scale `x=24` the exact baseline-zero survivor pairs have
equal residual.  Thus (9.2) is the first witness of this explicitly stated
same-shell, baseline-zero survivor-constancy type; it is not claimed to be
the first possible deleted-copy range violation.

The obstruction is not small-stage noise.  For `k>=4`,

```text
P_k>p_(k+2)^2.                                        (9.5)
```

The base case is `P_4=210>13^2`; repeated Bertrand and `p_(k+1)>4` give the
induction.  At every terminal stage `s>=5`, a physical shell lies below the
parent modulus.  A nonzero shell-supported state either occupies a deleted
copy or differs from its zero siblings, and hence is outside `ran(R_(p_s))`.

There are arbitrarily large literal nonzero residuals.  For fixed `K`, choose
distinct sufficiently large odd primes `a,b>(log x)^K`, and put

```text
x=ab+1,  t=ab-2=x-3.                                  (9.6)
```

Then `x/2<t<=x`, `Lambda(t+2)=Lambda(ab)=0`, while every local factor of
`b_x^(z)(t)` with `z=(log x)^K` is positive.  Hence

```text
w_x^(z)(t)=-b_x^(z)(t)<0.                             (9.7)
```

This proves the scoped stop

```text
LITERAL_SHB_D2_RESIDUAL_AS_HOMOGENEOUS_R_SOURCE_STATE
  = STOP_SCOPED_EXACT_FIBER_RANGE_VIOLATION.           (9.8)
```

It does not stop a dual-row attachment, an inhomogeneous source, or an
enlarged state.

## 10. Source innovation and exact Duhamel return

Let `beta` be any raw covector row at the child stage and decompose a primal
residual `V` by (8.4).  The algebraic covector pullback gives the exact identity

```text
L_beta(V)
 =L_(R_p^vee beta)(F)+L_beta(eta_p(V)).                (10.1)
```

Iterating (10.1) yields a finite source-side Duhamel expansion: a backward
pulled base functional plus one physically evaluated innovation at each
stage.  No probability, mixing, or approximation is used.

The types are important:

```text
eta_p(V) in V_child
  = primal source-level innovation,

Err_k: V_k -> B_(k+1)^dyn
  = V16 carrier/intertwiner defect.                    (10.2)
```

V16's allowance `Err_k!=0` does not alter its homogeneous source equation
`f_(k+1)=R_pf_k`.  Therefore it does not pay `eta_p(V)`.  A future construction
must either

1. replace the homogeneous source contract by a typed affine recursion and
   map each `eta` into the dynamical carrier; or
2. enlarge the source state so the literal residual is a physical observable
   rather than the homogeneous primal vector.

Absorbing `w_x^(z)` into the covector and evaluating it on the constant state
would make the declared coefficient depend on the actual shifted-prime
sequence.  That is a type change, not a solution.

## 11. The retyped big road

The honest Bridge B highway after V19 is

```text
source-locked two-type raw HB2 emitter
        |
        v
exact physical raw MASTER covectors
        |
        +---- analytic separated proof certificate
        |       [registry/L1/tails/theorem OPEN]
        |
        v
affine source cocycle
  V_(j+1)=R_(p_(j+1))V_j+eta_(j+1)
        |
        v
target-independent dynamical carrier
  + explicit eta-to-dynamics map
  + V16 Err kept separately
        |
        v
uniform physical innovation estimate
  sum_j |L_(pulled beta_j)(eta_j)|
       << x/log^A(x)
        |
        v
PBAPT reassembly and fixed h0=2 endpoint.               (11.1)
```

The selected next theorem is therefore

```text
BRIDGE_B_SHBD2_LONG_HORIZON_SOURCE_INNOVATION_RETURN
  = SELECTED_OPEN_NEW_THEOREM.                         (11.2)
```

It must freeze, on one source ledger,

```text
base and terminal prime clocks,
analytic x and physical X,
raw row ID and representation,
primal state or enlarged-state role,
eta support/norm and canonical projection,
eta-to-dynamical map,
V16 Err separately,
backward covector normalization,
all transform/reassembly losses,
uniform A,K constants,
strict 1/400 payment.                                  (11.3)
```

A fixed-horizon support theorem is not enough here: the primes between the
hybrid cutoff `z=(log x)^K` and the physical square-root clock form a growing
horizon.  Conversely, ambient primorial dimension alone is not a fatal: the
physical raw rows in the V19 fixture have exact rank 56.  The new question is
whether the growing sequence of physically evaluated innovations admits a
uniform deterministic estimate.

## 12. Claim firewall and status registry

The checker validates 30 canonical rows with final-LF SHA-256

```text
f17522e84c5c3a3de0ef0ab7ceb4f429e9aea8e89eee92d255d1b5d0fdc42342.
```

It also rejects 22 strict contract mutations, 34 full-registry semantic
mutations, 15 raw-type mutations, and 9 routing mutations.  Normal and
optimized Python execution are required to agree.

The mathematical ceiling is

```text
EXACT_L0_RAW_ROW_AND_SOURCE_INNOVATION_INTERFACE.
```

In particular,

```text
SHB_D2_ANALYTIC_SAVING = OPEN,
SOURCE_INNOVATION_PHYSICAL_EVALUATION = OPEN,
ARITHMETIC_ADVANCE = NO,
FIXED_ATOM_CREDIT = 0,
STRICT_1_OVER_400 = UNPAID,
L2 = NONE,
TPC_207_TRIGGER = false.                               (12.1)
```

The checker is

```text
research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py
```

and is read-only under

```powershell
python -B research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py --check
```
