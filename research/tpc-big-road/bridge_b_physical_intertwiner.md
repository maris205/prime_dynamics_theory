# Bridge B V16: scaled-isometry firewall and the physical-observable highway

This is an unnumbered route artifact.  It is not TPC-207, a paper, a proof of
the twin-prime conjecture, or an arithmetic `L2` advance.  Its purpose is to
separate one exact structural no-go from the surviving nonautonomous
Logistic/symbolic construction.

The current claim ceiling is

```text
EXACT_FINITE_OPERATOR_GEOMETRY
+ FULL_CENTERED_SPACE_INTERTWINER_STOP_SCOPED
+ PHYSICAL_OBSERVABLE_INTERTWINER_OPEN
+ NO_ARITHMETIC_ADVANCE.
```

Throughout, the physical shift is fixed at `h0=2`.  No result below supplies
fixed-atom credit, the strict `1/400`, all-`D` uniformity, an exactly-once
physical packet cover, or the packet/provenance gates required for TPC-207.

## 1. Frozen arithmetic object

Let

```text
P_k = product_(j<=k) p_j,
G_k = Z/P_k Z,
V_k = C^(G_k),
<f,g>_k = (1/P_k) sum_(r in G_k) f(r) conjugate(g(r)).
```

For a new odd prime `p` not dividing `P_k`, each element of
`G_(k+1)=Z/(pP_k)Z` is written uniquely as `r+jP_k`, with `r in G_k` and
`0<=j<p`.  The exact pair replication--deletion operator is

```text
(R_p f)(r+jP_k)
  = f(r)
    1_(p does not divide r+jP_k)
    1_(p does not divide r+jP_k+2).
```

Set

```text
alpha_p = 1-2/p,
B_k(r) = 1_((r,P_k)=1) 1_((r+2,P_k)=1),
a_k = mean_k(B_k),
W_k = B_k-a_k*1.
```

The two deleted copy indices are distinct because `p>2` and `P_k` is
invertible modulo `p`.  Hence every parent residue has exactly `p-2`
surviving children.  This elementary fact fixes the full Hilbert geometry.

## 2. Exact scaled-isometry theorem

For all `f,g in V_k`,

```text
<R_p f,R_p g>_(k+1) = alpha_p <f,g>_k,                 (2.1)
mean_(k+1)(R_p f) = alpha_p mean_k(f).                 (2.2)
```

Equivalently,

```text
R_p^* R_p = alpha_p I,                                (2.3)
S_p := alpha_p^(-1/2) R_p is an exact isometric
       injection (not a surjection).                    (2.4)
```

Proof: for fixed `r`, the inner sum over `j` contains exactly `p-2`
copies of `f(r)conjugate(g(r))`.  Division by `pP_k` gives (2.1), and the
same count without conjugation gives (2.2).  No asymptotic estimate, random
model, or spectral approximation enters.

In particular, the centered subspace

```text
V_k^0 = {f:mean_k(f)=0}
```

is mapped into `V_(k+1)^0`, and the normalized sieve evolution does not
contract it.  Indeed `alpha_p^(-1)R_p`, the linear part after dividing by the
new pair mass, has squared `L2` norm ratio `alpha_p^(-1)>1`.

For a block of new primes, write

```text
R_(b:a)=R_(p_b)...R_(p_(a+1)),
beta_(b:a)=product_(a<j<=b)(1-2/p_j).
```

Use `R_(a:a)=I`.  For any dynamical carrier below, similarly set
`Q_(b:a)=Q_(b-1)...Q_a` for `b>a` and `Q_(a:a)=I`.

Then the exact product identity is

```text
||R_(b:a)f||_b = sqrt(beta_(b:a)) ||f||_a.             (2.5)
```

Prime Mertens estimates give, away from the finitely many initial primes,

```text
sqrt(beta_(b:a))
  = (log p_a/log p_b)^(1+o(1)),                        (2.6)
```

so the raw centered geometry loses only logarithmically in prime scale, not
exponentially in the number of stages.

## 3. Orthogonal forcing is exact, not a perturbative story

Define the deletion forcing

```text
g_(k,p) = R_p 1-alpha_p*1.
```

It satisfies

```text
mean_(k+1)(g_(k,p)) = 0,
||g_(k,p)||_(k+1)^2 = alpha_p(1-alpha_p),               (3.1)
<R_p f,g_(k,p)>_(k+1)=0 for every f in V_k^0.           (3.2)
```

The centered survivor state therefore evolves by the exact forced triangular
recursion

```text
W_(k+1)=R_pW_k+a_k g_(k,p),                            (3.3)
```

and the two terms on the right are orthogonal.  Consequently,

```text
||W_(k+1)||^2
 = alpha_p||W_k||^2+a_k^2 alpha_p(1-alpha_p)
 = a_(k+1)(1-a_(k+1)).                                (3.4)
```

After pair-mass normalization,

```text
||W_k/a_k||^2 = 1/a_k-1 asymp (log p_k)^2.             (3.5)
```

Thus the actual normalized Haar-centered state grows in `L2`.  A future
Logistic carrier cannot assume a homogeneous invariant complement and cannot
erase the injection term in (3.3).

## 4. Full-centered-space exponential-mixing no-go

The following is the precise broad stop produced by (2.5).

Suppose Hilbert spaces `H_k^0`, maps

```text
J_k:V_k^0 -> H_k^0,
Q_k:H_k^0 -> H_(k+1)^0
```

have all three properties:

1. uniform coercivity and boundedness:

   ```text
   c||f||_k <= ||J_kf|| <= C||f||_k                     (4.1)
   ```

   for constants `0<c<=C<infinity` independent of `k`;

2. uniform arbitrary-product exponential memory loss:

   ```text
   ||Q_(b-1)...Q_a|| <= C_Q theta^(b-a),  0<theta<1;    (4.2)
   ```

3. exact full-centered-space intertwining:

   ```text
   J_(k+1)R_(p_(k+1))=Q_kJ_k.                           (4.3)
   ```

For a unit vector `f in V_a^0`, (2.5) and (4.1)--(4.3) would imply

```text
c sqrt(beta_(b:a))
 <= ||J_bR_(b:a)f||
 <= C_Q C theta^(b-a).                                 (4.4)
```

The left side has only logarithmic prime-scale decay while the right side has
exponential stage decay, which is impossible for long blocks.  Therefore

```text
UNIFORMLY_COERCIVE_FULL_CENTERED_SIEVE_TO_EXPONENTIALLY_MIXING_
LOGISTIC_INTERTWINER
  = STOP_SCOPED_EXACT_SCALED_ISOMETRY_RATE_MISMATCH.    (4.5)
```

This is not a no-go for every dynamical representation.  It stops only the
simultaneous use of full centered-space coercivity, uniform exponential
memory loss, and exact intertwining.  In particular it does not stop a
noncoercive quotient map, an observable seminorm, nonuniform `Q` products, or
a forced physical trajectory controlled only after applying `ell_X`.

The same firewall survives a quasi-intertwiner.  Put

```text
Err_k=J_(k+1)R_(p_(k+1))-Q_kJ_k.
```

The telescoped Duhamel defect is

```text
Delta_(b:a)
 = J_bR_(b:a)-Q_(b:a)J_a
 = sum_(a<=j<b) Q_(b:j+1) Err_j R_(j:a).                (4.6)
```

Under (4.1)--(4.2), (2.5) gives

```text
||Delta_(b:a)||
 >= c sqrt(beta_(b:a))-C_Q C theta^(b-a).               (4.7)
```

Hence the accumulated full-operator defect cannot be
`o(sqrt(beta_(b:a)))`.  Small per-stage plots are irrelevant unless their
propagated physical loss is audited in the correct norm.

## 5. Why the direct distinguished-seed road is not the next bridge

The repository already has, on the exact profinite base,

```text
mu(E_n) asymp 1/(log n)^2,
sum_n mu(E_n)=infinity,
Var_mu(sum_(n<=N)1_(E_n)(T^n x))=O(N),
```

and therefore Haar-a.e. infinite moving recurrence.  It also has the exact
fixed-`h0=2` identity

```text
T^n(0) in E_n iff n and n+2 are prime.
```

So a pointed theorem for seed `0` on that exact event family is already an
endpoint-equivalent formulation of TPC.  Positive mass, divergent mass,
unique ergodicity, full-measure DBC, absolute continuity, or a generic
Logistic/Henon fiber cannot select this Dirac seed.

The sharp countermodel is the independent product space with
`P(omega_n=1)=1/log^2(n+2)`: the events are independent, the total mass
diverges, and the limsup has full measure, while the named all-zero sequence
never hits.  Thus no improvement of the metric covariance calculation alone
can close the named seed.

Separately, divergent mass without dependence control does not even imply an
a.e. limsup law: on `([0,1],Leb)` the nested events `F_n=(0,1/n]` satisfy
`sum_n Leb(F_n)=infinity` but `limsup_n F_n` is empty.

## 6. The surviving highway: a physical-observable quotient

The no-go theorem dictates the architecture.  A useful carrier must abandon
full-space coercivity and act only on a target-independent observable quotient
or physical cyclic subspace.  The selected theorem target is

```text
BRIDGE_B_PHYSICAL_OBSERVABLE_QUOTIENT_INTERTWINER.      (6.1)
```

It must supply all of the following on one source ledger.

### 6.1 Independent input class

Choose in advance a class `A` of admissible affine-pattern/coefficient
systems.  The class cannot be selected using future prime or twin locations;
fixed `h0=2` is an application, not the definition of the theorem.
At scale `X`, write `A_X` for its predeclared active members and
`f_(j,X,A) in V_j` for the exact stage-`j` source trajectory attached to
`A in A_X`.  One common predeclared start `j_0`, independent of `X` and `A`,
and the initial source must obey

```text
f_(j+1,X,A)=R_(p_(j+1))f_(j,X,A),
f_(j,X,A)=R_(j:j_0)f_(j_0,X,A),  j_0<=j<=k_X.          (6.1a)
```

These objects and their literal source normalization must be defined before
any future hit data are examined.  For all sufficiently large `X`, `k_X>j_0`
and `A_X` must be nonempty.  Arithmetic promotion additionally requires a separately
source-locked member realizing the actual nonzero fixed-`h0=2` trajectory; an
abstract nonempty class alone receives only method-candidate status.

### 6.2 Observable quotient, not one-vector fitting

Let `L_(k,X,A)` be a separating family of physical functionals, with their
literal physical normalizations frozen, containing the Haar mean, actual
interval evaluation, deletion-bias Fourier functionals, and the Type-II tests
required by PBAPT.  The quotient may discard directions annihilated by all
these functionals, but it must preserve every declared physical output.
Fitting only `B_k`, its mean, or a finite numerical trajectory is circular and
fails the gate.

### 6.3 Forced nonautonomous evolution

Construct paired nonautonomous transfer blocks `Q_k`, spaces `B_k^dyn`, and
maps `J_k` such that

```text
J_(k+1)R_p=Q_kJ_k+Err_k,                               (6.2)
```

while (3.3), the pair event, stage, clock, masks, and fixed physical shift are
all retained.  A word-level `RLR^infinity` match is insufficient.

### 6.4 Deterministic physical return

For each `A in A_X` and `ell in L_(k_X,X,A)` there must be a dynamical dual
functional `Lambda_(X,A,ell)^dyn` satisfying the exact return identity on the
declared quotient, for every `f in V_(k_X)`,

```text
ell(f)=Lambda_(X,A,ell)^dyn(J_(k_X)f).                  (6.3)
```

The propagated defect must be paid uniformly after physical evaluation.
There must be one function `epsilon(X)->0`, independent of the active `A` and
declared `ell`, such that

```text
sup_(A in A_X, ell in L_(k_X,X,A))
 sum_(j_0<=j<k_X)
 |Lambda_(X,A,ell)^dyn(
    Q_(k_X:j+1) Err_j f_(j,X,A))|
   <= epsilon(X) X/(log X)^2.                          (6.4)
```

or must give the stronger literal Type-II saving required by PBAPT.  An
abstract Banach norm with uncontrolled evaluation amplification gives no
credit.

### 6.5 Required output

The first success target is a deterministic `H_dyn/H3_phys` estimate for the
predeclared affine class.  It must feed PBAPT or the exact packet reassembly;
it is not an a.e. recurrence statement.  Only after that theorem exists may a
Logistic construction receive arithmetic attachment credit.

This route genuinely bypasses the invalid a.e.-to-point promotion: it controls
the deterministic physical count as a dual functional rather than declaring
the arithmetic seed typical.

## 7. Two reserves and their early falsifiers

### 7.1 Bratteli--Vershik/S-adic aging clock

The exact changing-alphabet replication--deletion system has a natural
nonstationary Bratteli description.  The open reserve is to find a
target-independent low-complexity quotient and an aging-clock suspension with
`ds=dn/(log n)^2`.  Ordinary unique ergodicity is already insufficient, and an
all-path discrepancy theorem stated only for seed `0` and the `h0=2` events
would merely rename the endpoint.

The first falsifier is event-preserving rank growth.  If any exact quotient
retaining the required physical functionals has rank or condition number
comparable with the primorial state complexity, the finite-rank road is
deprioritized.  General finite-rank Bratteli theory supplies invariant-measure
and unique-ergodicity tools, but not this arithmetic moving-depth attachment;
see [Bezuglyi--Kwiatkowski--Medynets--Solomyak](https://arxiv.org/abs/1003.2816).

### 7.2 Deterministic shadowing/natural extension

A Logistic schedule may instead be verified by deterministic sequential
Lasota--Yorke/covering estimates, but a.e. environments or a.e. initial points
still do not select the arithmetic section.  Shadowing transfers a shrinking
target only with explicit boundary margins and a deterministic physical-return
identity.

Henon remains optional until an exact natural-extension diagram preserves the
same event, measure, stage, and physical functional.  Area preservation and
reversibility alone do not change (4.5) or the named-seed firewall.  Standard
shrinking-target results are metric statements under their own map/target
hypotheses; for the relevant claim boundary see
[Haydn--Nicol--Persson--Vaienti](https://arxiv.org/abs/1103.2113).

## 8. Canonical V16 status registry

The checker freezes 20 rows, sorted by key with final-LF canonical rows
`key<TAB>value<LF>`:

```text
BRIDGE_B_ARITHMETIC_ADVANCE	NO
BRIDGE_B_BRATTELI_S_ADIC_AGING_CLOCK	OPEN_RESERVE_RANK_GROWTH_FALSIFIER
BRIDGE_B_CENTERED_ENERGY_RECURSION	PROVED_EXACT_FINITE
BRIDGE_B_CENTERED_SUBSPACE_INVARIANCE	PROVED_EXACT_FINITE
BRIDGE_B_EXACT_PAIR_REPLICATION_DELETION	PROVED_EXACT_FINITE
BRIDGE_B_FORCING_MEAN_ZERO	PROVED_EXACT_FINITE
BRIDGE_B_FORCING_ORTHOGONAL_TO_CENTERED_IMAGE	PROVED_EXACT_FINITE
BRIDGE_B_FULL_SPACE_COERCIVE_EXP_MIX_EXACT_INTERTWINER	STOP_SCOPED_EXACT_SCALED_ISOMETRY_RATE_MISMATCH
BRIDGE_B_FULL_SPACE_COERCIVE_EXP_MIX_NEGLIGIBLE_DEFECT	STOP_SCOPED_EXACT_DUHAMEL_RATE_MISMATCH
BRIDGE_B_HAAR_L2_GRAM	PROVED_EXACT_FINITE
BRIDGE_B_HENON_NATURAL_EXTENSION	OPTIONAL_OPEN_EXACT_FACTOR_REQUIRED
BRIDGE_B_METRIC_DBC_TO_NAMED_SEED	STOP_SCOPED_FALSE_COUNTERMODEL
BRIDGE_B_NORMALIZED_CENTERED_HAAR_CONTRACTION	STOP_SCOPED_FALSE_EXACT_ENERGY_GROWTH
BRIDGE_B_NORMALIZED_SCALED_ISOMETRY	PROVED_EXACT_FINITE
BRIDGE_B_PHYSICAL_OBSERVABLE_QUOTIENT_INTERTWINER	SELECTED_OPEN_NEW_THEOREM
BRIDGE_B_POINTED_DIRECT_GATE	OPEN_ENDPOINT_EQUIVALENT_TARGET
FIXED_ATOM_CREDIT	0
L2	NONE
STRICT_1_OVER_400	UNPAID
TPC_207_TRIGGER	false
```

The final-LF SHA-256 is

```text
cc63154e3a1bb21513ed7b86fe30236133d110d48eef191bc3bfab7841bc9fb1
```

Run the read-only exact checker with

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python -B research/tpc-big-road/tpc_bridge_b_carrier_checker.py --check
python -B -O research/tpc-big-road/tpc_bridge_b_carrier_checker.py --check
```

It verifies (2.1)--(3.5) on four exact primorial extensions, a four-stage
product fixture, and mutations for one-deletion, wrong forcing centering, and
false normalized contraction.  These finite checks support the algebra only;
the asymptotic no-go follows from the displayed proof, and (6.1) remains an
open new theorem.

## 9. Route verdict

```text
DIRECT_RLR_INFINITY_RECURRENCE = STRUCTURAL_DEAD_END
METRIC_DBC_TO_SEED_0 = STOP_SCOPED_FALSE
FULL_CENTERED_EXP_MIX_LOGISTIC_INTERTWINER = STOP_SCOPED
PHYSICAL_OBSERVABLE_QUOTIENT_INTERTWINER = SELECTED_OPEN_NEW_THEOREM
BRATTELI_AGING_CLOCK = OPEN_RESERVE
HENON_NATURAL_EXTENSION = OPTIONAL_OPEN
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
```

The next finite gate is not another ordinary DBC theorem.  It is to construct
or broadly falsify a target-independent observable quotient preserving the
deletion forcing and the complete physical dual family.  A positive finite
fit is navigation only; a theorem-state advance requires uniform analytic
control and the full physical loss ledger.
